"""
NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System
Modular CSP Backtracking Solver Engine (Baseline & ML-Assisted Modes)

SIH 2025 | Problem Statement SIH25091
Team: Gandikota Sai Chandana (12511912) & Inayat (12512142)
Subject Code: K3P25IL
"""

import time
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional, Callable
from .constraints import SessionVariable, AssignmentValue, ScheduleState, SoftConstraintEvaluator
from .heuristics import VariableOrdering, ValueOrdering, ForwardChecker
from ..ml.classifier import TimetableConflictClassifier

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SLOTS = [1, 2, 3, 4, 5, 6, 7]

class TimetableCSPSolver:
    """
    Constraint Satisfaction Problem (CSP) Solver for NEP-2020 Academic Timetabling.
    Supports both Baseline Heuristic Search (MRV + Degree + LCV) and
    ML-Assisted Heuristic Search (MRV + Degree + ML-guided Value Prioritization).
    """

    def __init__(
        self,
        data_dict: Dict[str, pd.DataFrame],
        solver_mode: str = "baseline", # "baseline" or "ml_assisted"
        max_backtracks: int = 3000,
        timeout_seconds: float = 25.0,
        enable_forward_checking: bool = True,
        ml_classifier: Optional[TimetableConflictClassifier] = None
    ):
        self.data_dict = data_dict
        self.solver_mode = solver_mode
        self.max_backtracks = max_backtracks
        self.timeout_seconds = timeout_seconds
        self.enable_forward_checking = enable_forward_checking
        self.ml_classifier = ml_classifier

        # Telemetry metrics
        self.nodes_explored = 0
        self.backtracks_count = 0
        self.forward_checking_prunings = 0
        self.constraint_checks = 0
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.status = "NOT_STARTED" # "OPTIMAL_FEASIBLE", "INFEASIBLE", "TIMEOUT", "MAX_BACKTRACKS_EXCEEDED"

        # Lookup structures
        self.rooms_dict = self._build_rooms_dict()
        self.faculty_df = data_dict["faculty"]
        self.groups_dict = self._build_groups_dict()
        self.faculty_max_daily = self._build_faculty_limits()

        # State and variables
        self.state = ScheduleState(faculty_max_daily=self.faculty_max_daily)
        self.variables: List[SessionVariable] = []
        self._initialize_problem()

    def _build_rooms_dict(self) -> Dict[str, Dict[str, Any]]:
        rooms_df = self.data_dict["rooms"]
        res = {}
        for _, r in rooms_df.iterrows():
            res[r["room_id"]] = {
                "name": r.get("name", r["room_id"]),
                "type": r["type"],
                "capacity": int(r["capacity"]),
                "building": r.get("building", "")
            }
        return res

    def _build_groups_dict(self) -> Dict[str, Dict[str, Any]]:
        groups_df = self.data_dict["student_groups"]
        res = {}
        for _, g in groups_df.iterrows():
            res[g["group_id"]] = {
                "name": g["name"],
                "strength": int(g["strength"]),
                "department": g.get("department", "")
            }
        return res

    def _build_faculty_limits(self) -> Dict[str, int]:
        fac_df = self.data_dict["faculty"]
        res = {}
        for _, f in fac_df.iterrows():
            res[f["faculty_id"]] = int(f.get("max_hours_per_day", 4))
        return res

    def _initialize_problem(self):
        """Construct SessionVariables, initial domains, and lock pre-existing schedules."""
        curriculum_df = self.data_dict["curriculum"]
        courses_df = self.data_dict["courses"].set_index("course_id")
        existing_df = self.data_dict["existing_schedule"]
        
        # Build faculty unavailable slots set: (faculty_id, day:slot)
        fac_unavail: Dict[str, set] = {}
        for _, f in self.faculty_df.iterrows():
            fid = f["faculty_id"]
            unavail_str = str(f.get("unavailable_slots", ""))
            slots_set = set(unavail_str.split(";")) if unavail_str and unavail_str != "nan" else set()
            fac_unavail[fid] = slots_set

        self.variables = []
        
        # 1. Instantiate variables from curriculum
        for _, row in curriculum_df.iterrows():
            cid = row["course_id"]
            gid = row["group_id"]
            fid = row["faculty_id"]
            c_info = courses_df.loc[cid] if cid in courses_df.index else {}
            course_name = c_info.get("name", cid) if hasattr(c_info, "get") else cid
            sessions_count = int(row["sessions_per_week"])
            req_room_type = row["required_room_type"]
            enrolled = self.groups_dict.get(gid, {}).get("strength", 50)
            is_lab = ("Lab" in req_room_type) or ("lab" in str(cid).lower())

            # Candidate rooms matching type and capacity
            suitable_rooms = [
                rid for rid, rdata in self.rooms_dict.items()
                if rdata["type"] == req_room_type and rdata["capacity"] >= enrolled
            ]
            
            # If no room fits, search is infeasible for this variable
            if not suitable_rooms:
                suitable_rooms = []

            # Generate candidate domain (day, slot, room)
            base_domain: List[AssignmentValue] = []
            f_unavail_slots = fac_unavail.get(fid, set())

            for day in DAYS:
                for slot in SLOTS:
                    slot_token = f"{day}:{slot}"
                    if slot_token in f_unavail_slots:
                        continue # Hard constraint: faculty unavailable
                    for rid in suitable_rooms:
                        base_domain.append(AssignmentValue(day=day, slot_id=slot, room_id=rid))

            for s_idx in range(1, sessions_count + 1):
                var_id = f"{row['curriculum_id']}_S{s_idx}"
                s_var = SessionVariable(
                    var_id=var_id,
                    curriculum_id=row["curriculum_id"],
                    course_id=cid,
                    course_name=course_name,
                    group_id=gid,
                    faculty_id=fid,
                    faculty_name=str(self.faculty_df[self.faculty_df["faculty_id"] == fid]["name"].iloc[0]) if not self.faculty_df[self.faculty_df["faculty_id"] == fid].empty else fid,
                    session_index=s_idx,
                    required_room_type=req_room_type,
                    enrolled_count=enrolled,
                    is_lab=is_lab,
                    domain=list(base_domain)
                )
                self.variables.append(s_var)

        # 2. Lock pre-fixed allocations from existing_schedule
        for _, fix_row in existing_df.iterrows():
            c_match = fix_row["course_id"]
            g_match = fix_row["group_id"]
            f_match = fix_row["faculty_id"]
            fixed_val = AssignmentValue(day=fix_row["day"], slot_id=int(fix_row["slot_id"]), room_id=fix_row["room_id"])

            # Find matching unassigned variable to lock
            for v in self.variables:
                if (not v.is_assigned() and v.course_id == c_match and 
                    v.group_id == g_match and v.faculty_id == f_match):
                    v.is_fixed = True
                    self.state.assign(v, fixed_val)
                    break

    def solve(self) -> Dict[str, Any]:
        """Execute heuristic backtracking search with telemetry logging."""
        self.nodes_explored = 0
        self.backtracks_count = 0
        self.forward_checking_prunings = 0
        self.constraint_checks = 0
        self.start_time = time.time()
        
        success = self._backtrack()
        self.elapsed_time = time.time() - self.start_time

        assigned_vars = [v for v in self.variables if v.is_assigned()]
        total_vars = len(self.variables)
        completeness = round((len(assigned_vars) / total_vars) * 100.0, 2)

        if success:
            self.status = "OPTIMAL_FEASIBLE"
        elif self.elapsed_time >= self.timeout_seconds:
            self.status = "TIMEOUT"
        elif self.backtracks_count >= self.max_backtracks:
            self.status = "MAX_BACKTRACKS_EXCEEDED"
        else:
            self.status = "INFEASIBLE"

        # Calculate soft constraint penalties
        soft_eval = SoftConstraintEvaluator.calculate_penalties(self.variables, self.rooms_dict)

        results = {
            "status": self.status,
            "solver_mode": self.solver_mode,
            "is_complete": (len(assigned_vars) == total_vars),
            "assigned_sessions": len(assigned_vars),
            "total_sessions": total_vars,
            "completeness_pct": completeness,
            "execution_time_seconds": round(self.elapsed_time, 4),
            "execution_time_ms": round(self.elapsed_time * 1000, 2),
            "nodes_explored": self.nodes_explored,
            "backtracks_count": self.backtracks_count,
            "forward_checking_prunings": self.forward_checking_prunings,
            "constraint_checks": self.constraint_checks,
            "quality_score": soft_eval["quality_score"],
            "total_soft_penalty": soft_eval["total_penalty"],
            "soft_penalties_breakdown": soft_eval,
            "schedule_records": self._export_solution_records()
        }
        return results

    def _backtrack(self) -> bool:
        """Recursive backtracking search procedure."""
        self.nodes_explored += 1
        
        # Check termination limits
        if (time.time() - self.start_time) > self.timeout_seconds:
            return False
        if self.backtracks_count > self.max_backtracks:
            return False

        # Variable selection: MRV + Degree Heuristic
        var = VariableOrdering.select_unassigned_variable(self.variables, self.state)
        if var is None:
            # All variables assigned successfully
            return True

        # Value selection: LCV or ML-Assisted Prioritization
        if self.solver_mode == "ml_assisted" and self.ml_classifier is not None:
            def batch_ml_eval(v, candidates, st):
                return self.ml_classifier.batch_predict_conflict_probabilities(
                    v, candidates, st, self.rooms_dict, self.faculty_df
                )
            ordered_values = ValueOrdering.order_values_ml_assisted(
                var, self.variables, self.state, batch_ml_eval
            )
        else:
            ordered_values = ValueOrdering.order_values_lcv(
                var, self.variables, self.state
            )

        for val in ordered_values:
            self.constraint_checks += 1
            is_valid, _ = self.state.is_valid_assignment(var, val)
            if not is_valid:
                continue

            # Tentative assignment
            self.state.assign(var, val)

            # Forward Checking
            if self.enable_forward_checking:
                fc_success, pruned_records = ForwardChecker.prune_domains(
                    var, val, self.variables, self.state
                )
                self.forward_checking_prunings += sum(len(v) for v in pruned_records.values())

                if fc_success:
                    result = self._backtrack()
                    if result:
                        return True

                # Restore pruned domains
                ForwardChecker.restore_domains(pruned_records, self.variables)
            else:
                result = self._backtrack()
                if result:
                    return True

            # Backtrack rollback
            self.backtracks_count += 1
            self.state.unassign(var)

        return False

    def _export_solution_records(self) -> List[Dict[str, Any]]:
        """Format assigned schedule variables into tabular format."""
        records = []
        for v in self.variables:
            val = v.assigned_value
            if val is not None:
                r_info = self.rooms_dict.get(val.room_id, {})
                records.append({
                    "variable_id": v.var_id,
                    "curriculum_id": v.curriculum_id,
                    "course_id": v.course_id,
                    "course_name": v.course_name,
                    "group_id": v.group_id,
                    "group_name": self.groups_dict.get(v.group_id, {}).get("name", v.group_id),
                    "faculty_id": v.faculty_id,
                    "faculty_name": v.faculty_name,
                    "session_number": v.session_index,
                    "day": val.day,
                    "slot_id": val.slot_id,
                    "time_label": f"Slot {val.slot_id}",
                    "room_id": val.room_id,
                    "room_name": r_info.get("name", val.room_id),
                    "room_type": r_info.get("type", v.required_room_type),
                    "enrolled_strength": v.enrolled_count,
                    "room_capacity": r_info.get("capacity", 50),
                    "is_fixed": v.is_fixed
                })
        return records
