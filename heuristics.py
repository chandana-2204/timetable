"""
NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System
CSP Heuristic Strategies Module (MRV, Degree Heuristic, LCV, Forward Checking)

SIH 2025 | Problem Statement SIH25091
Team: Gandikota Sai Chandana (12511912) & Inayat (12512142)
Subject Code: K3P25IL
"""

from typing import List, Dict, Tuple, Optional, Any, Callable
from .constraints import SessionVariable, AssignmentValue, ScheduleState

class VariableOrdering:
    """Implements Minimum Remaining Values (MRV) with Degree Heuristic tie-breaking."""
    
    @staticmethod
    def select_unassigned_variable(
        variables: List[SessionVariable],
        state: ScheduleState
    ) -> Optional[SessionVariable]:
        """
        MRV + Degree Heuristic:
        1. Filter for unassigned variables.
        2. Calculate valid domain size for each unassigned variable given current state.
        3. Find variable with smallest valid domain size (MRV).
        4. Tie-break using Degree Heuristic (most constraint connections with remaining variables).
        """
        unassigned = [v for v in variables if not v.is_assigned()]
        if not unassigned:
            return None
            
        scored_candidates = []
        for var in unassigned:
            # Count valid domain values given current schedule state
            valid_count = 0
            for val in var.domain:
                is_valid, _ = state.is_valid_assignment(var, val)
                if is_valid:
                    valid_count += 1
                    
            # Degree: count how many other unassigned variables share faculty or student group
            degree = sum(
                1 for other in unassigned 
                if other.var_id != var.var_id and (other.faculty_id == var.faculty_id or other.group_id == var.group_id)
            )
            
            # (valid_domain_count, -degree, var)
            scored_candidates.append((valid_count, -degree, var))
            
        # Sort ascending by valid domain count (MRV), then by -degree (highest degree first)
        scored_candidates.sort(key=lambda item: (item[0], item[1]))
        return scored_candidates[0][2]


class ValueOrdering:
    """Implements Least Constraining Value (LCV) and ML-Guided Value Ordering."""
    
    @staticmethod
    def order_values_lcv(
        var: SessionVariable,
        variables: List[SessionVariable],
        state: ScheduleState
    ) -> List[AssignmentValue]:
        """
        Least Constraining Value (LCV):
        Orders candidate values so that the value ruling out the fewest choices
        for neighboring unassigned variables is tried first.
        """
        valid_values = []
        for val in var.domain:
            is_valid, _ = state.is_valid_assignment(var, val)
            if is_valid:
                valid_values.append(val)
                
        if len(valid_values) <= 1:
            return valid_values
            
        unassigned_neighbors = [
            other for other in variables 
            if not other.is_assigned() and other.var_id != var.var_id and 
            (other.faculty_id == var.faculty_id or other.group_id == var.group_id)
        ]
        
        value_scores = []
        for val in valid_values:
            # Simulate constraint impact: count how many neighbor choices are eliminated
            constraints_count = 0
            time_key = (val.day, val.slot_id)
            for neighbor in unassigned_neighbors:
                for n_val in neighbor.domain:
                    if n_val.day == val.day and n_val.slot_id == val.slot_id:
                        # Conflict created if neighbor shares faculty or group
                        if neighbor.faculty_id == var.faculty_id or neighbor.group_id == var.group_id:
                            constraints_count += 1
            value_scores.append((constraints_count, val))
            
        # Sort ascending by constraints created (least constraining first)
        value_scores.sort(key=lambda x: x[0])
        return [val for _, val in value_scores]

    @staticmethod
    def order_values_ml_assisted(
        var: SessionVariable,
        variables: List[SessionVariable],
        state: ScheduleState,
        ml_predict_fn: Optional[Callable[[SessionVariable, List[AssignmentValue], ScheduleState], List[float]]] = None
    ) -> List[AssignmentValue]:
        """
        ML-Assisted Value Ordering:
        Uses supervised machine learning model to estimate conflict probability P(conflict)
        for candidate (day, slot, room) assignments in a single vectorized batch.
        Values with lowest predicted conflict probability are prioritized first.
        """
        valid_values = []
        for val in var.domain:
            is_valid, _ = state.is_valid_assignment(var, val)
            if is_valid:
                valid_values.append(val)
                
        if len(valid_values) <= 1:
            return valid_values
            
        if ml_predict_fn is not None:
            try:
                probs = ml_predict_fn(var, valid_values, state)
            except Exception:
                probs = [0.5] * len(valid_values)
        else:
            probs = [0.5] * len(valid_values)
            
        scored_values = []
        for val, prob in zip(valid_values, probs):
            # Prioritize low conflict probability, with slight tie-breaker for morning/balanced slots
            score = prob + (0.02 if val.slot_id in [1, 2, 3] else 0.05)
            scored_values.append((score, val))
            
        # Lowest predicted conflict risk first
        scored_values.sort(key=lambda x: x[0])
        return [val for _, val in scored_values]


class ForwardChecker:
    """Forward Checking: Prunes inconsistent values from neighbor domains upon assignment."""
    
    @staticmethod
    def prune_domains(
        assigned_var: SessionVariable,
        assigned_val: AssignmentValue,
        variables: List[SessionVariable],
        state: ScheduleState
    ) -> Tuple[bool, Dict[str, List[AssignmentValue]]]:
        """
        Prune domain values from unassigned variables that directly clash with the newly assigned value.
        Returns:
            (success, pruned_records_dict)
            If any neighbor domain is wiped out to 0, returns (False, pruned_records_dict) for immediate backtrack.
        """
        pruned_records: Dict[str, List[AssignmentValue]] = {}
        
        for other in variables:
            if other.is_assigned() or other.var_id == assigned_var.var_id:
                continue
                
            # Check if this variable shares faculty or student group
            shares_faculty = (other.faculty_id == assigned_var.faculty_id)
            shares_group = (other.group_id == assigned_var.group_id)
            
            if not (shares_faculty or shares_group):
                continue
                
            to_remove = []
            for val in other.domain:
                if val.day == assigned_val.day and val.slot_id == assigned_val.slot_id:
                    # Incompatible time slot
                    to_remove.append(val)
                    
            if to_remove:
                pruned_records[other.var_id] = to_remove
                for val in to_remove:
                    other.domain.remove(val)
                    
                # Domain wipeout check (Wipeout Detection)
                if len(other.domain) == 0:
                    return False, pruned_records
                    
        return True, pruned_records

    @staticmethod
    def restore_domains(pruned_records: Dict[str, List[AssignmentValue]], variables: List[SessionVariable]):
        """Restore pruned domain values upon backtracking."""
        var_map = {v.var_id: v for v in variables}
        for var_id, restored_vals in pruned_records.items():
            if var_id in var_map:
                var_map[var_id].domain.extend(restored_vals)
