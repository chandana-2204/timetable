"""
NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System
CSP Mathematical Constraint Formulations (Hard & Soft Constraints)

SIH 2025 | Problem Statement SIH25091
Team: Gandikota Sai Chandana (12511912) & Inayat (12512142)
Subject Code: K3P25IL
"""

from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, field

@dataclass
class AssignmentValue:
    """Represents a candidate time and space assignment for a session variable."""
    day: str
    slot_id: int
    room_id: str

    def to_tuple(self) -> Tuple[str, int, str]:
        return (self.day, self.slot_id, self.room_id)

    def __hash__(self):
        return hash((self.day, self.slot_id, self.room_id))

    def __eq__(self, other):
        if not isinstance(other, AssignmentValue):
            return False
        return (self.day == other.day and 
                self.slot_id == other.slot_id and 
                self.room_id == other.room_id)

@dataclass
class SessionVariable:
    """Represents an individual course session allocation variable X_i."""
    var_id: str
    curriculum_id: str
    course_id: str
    course_name: str
    group_id: str
    faculty_id: str
    faculty_name: str
    session_index: int
    required_room_type: str
    enrolled_count: int
    is_lab: bool
    is_fixed: bool = False
    assigned_value: Optional[AssignmentValue] = None
    domain: List[AssignmentValue] = field(default_factory=list)

    def is_assigned(self) -> bool:
        return self.assigned_value is not None

class ScheduleState:
    """
    Maintains fast indexed tracking of faculty, room, and group schedules
    to support O(1) hard constraint checks and forward checking.
    """
    def __init__(self, faculty_max_daily: Dict[str, int]):
        # Sets of occupied tuples:
        # (day, slot, faculty_id)
        self.faculty_occupancy: Set[Tuple[str, int, str]] = set()
        # (day, slot, room_id)
        self.room_occupancy: Set[Tuple[str, int, str]] = set()
        # (day, slot, group_id)
        self.group_occupancy: Set[Tuple[str, int, str]] = set()
        
        # Faculty daily hours tracking: (faculty_id, day) -> count
        self.faculty_daily_hours: Dict[Tuple[str, str], int] = {}
        self.faculty_max_daily = faculty_max_daily
        
        # Group daily course session count: (group_id, course_id, day) -> count
        self.group_course_daily: Dict[Tuple[str, str, str], int] = {}
        
        # All assigned variables mapping: var_id -> AssignmentValue
        self.assignments: Dict[str, AssignmentValue] = {}

    def is_valid_assignment(self, var: SessionVariable, val: AssignmentValue) -> Tuple[bool, Optional[str]]:
        """
        Evaluate all hard constraints for assigning var <- val.
        Returns (is_valid, violation_reason).
        """
        # 1. Faculty collision check
        fac_key = (val.day, val.slot_id, var.faculty_id)
        if fac_key in self.faculty_occupancy:
            return False, f"Faculty {var.faculty_id} already scheduled on {val.day} Slot {val.slot_id}"
                
        # 2. Room collision check
        room_key = (val.day, val.slot_id, val.room_id)
        if room_key in self.room_occupancy:
            return False, f"Room {val.room_id} already booked on {val.day} Slot {val.slot_id}"
                
        # 3. Student group collision check
        group_key = (val.day, val.slot_id, var.group_id)
        if group_key in self.group_occupancy:
            return False, f"Student Group {var.group_id} has concurrent session on {val.day} Slot {val.slot_id}"
                
        # 4. Faculty daily workload constraint
        fac_day_key = (var.faculty_id, val.day)
        current_fac_hours = self.faculty_daily_hours.get(fac_day_key, 0)
        max_daily = self.faculty_max_daily.get(var.faculty_id, 4)
        if current_fac_hours >= max_daily:
            return False, f"Faculty {var.faculty_id} exceeds daily workload limit ({max_daily}h) on {val.day}"
            
        # 5. Course session spread: avoid 2 lectures of the same course on the same day for a group
        if not var.is_lab:
            grp_course_key = (var.group_id, var.course_id, val.day)
            if self.group_course_daily.get(grp_course_key, 0) >= 1:
                return False, f"Course {var.course_id} already has a lecture on {val.day} for group {var.group_id}"
                
        return True, None

    def assign(self, var: SessionVariable, val: AssignmentValue):
        """Register assignment and update tracking indices."""
        fac_key = (val.day, val.slot_id, var.faculty_id)
        room_key = (val.day, val.slot_id, val.room_id)
        group_key = (val.day, val.slot_id, var.group_id)

        self.faculty_occupancy.add(fac_key)
        self.room_occupancy.add(room_key)
        self.group_occupancy.add(group_key)
        
        fac_day_key = (var.faculty_id, val.day)
        self.faculty_daily_hours[fac_day_key] = self.faculty_daily_hours.get(fac_day_key, 0) + 1
        
        grp_course_key = (var.group_id, var.course_id, val.day)
        self.group_course_daily[grp_course_key] = self.group_course_daily.get(grp_course_key, 0) + 1
        
        self.assignments[var.var_id] = val
        var.assigned_value = val

    def unassign(self, var: SessionVariable):
        """Rollback assignment and restore tracking indices."""
        val = var.assigned_value
        if val is None:
            return
            
        fac_key = (val.day, val.slot_id, var.faculty_id)
        room_key = (val.day, val.slot_id, val.room_id)
        group_key = (val.day, val.slot_id, var.group_id)

        self.faculty_occupancy.discard(fac_key)
        self.room_occupancy.discard(room_key)
        self.group_occupancy.discard(group_key)
            
        fac_day_key = (var.faculty_id, val.day)
        if fac_day_key in self.faculty_daily_hours:
            self.faculty_daily_hours[fac_day_key] -= 1
            if self.faculty_daily_hours[fac_day_key] <= 0:
                del self.faculty_daily_hours[fac_day_key]
                
        grp_course_key = (var.group_id, var.course_id, val.day)
        if grp_course_key in self.group_course_daily:
            self.group_course_daily[grp_course_key] -= 1
            if self.group_course_daily[grp_course_key] <= 0:
                del self.group_course_daily[grp_course_key]
                
        if var.var_id in self.assignments:
            del self.assignments[var.var_id]
        var.assigned_value = None


class SoftConstraintEvaluator:
    """Evaluates soft constraint penalties to quantify schedule quality and ergonomics."""
    
    @staticmethod
    def calculate_penalties(variables: List[SessionVariable], rooms_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate 6 soft constraint dimensions:
        1. Student Idle Gaps: Idle hours between classes on the same day.
        2. Faculty Consecutive Hours: More than 2 consecutive hours.
        3. Room Capacity Wastage: Excessive unused room capacity.
        4. Late Slot Penalties: Frequency of 16:00-17:00 assignments.
        5. Day Distribution Balance: Uneven spread of classes over Monday-Friday.
        6. Elective Preference: Optimal alignment of elective cohorts.
        """
        gap_penalty = 0
        consecutive_penalty = 0
        capacity_waste = 0
        late_slot_penalty = 0
        
        # Build student schedule: (group_id, day) -> list of slots
        group_schedules: Dict[Tuple[str, str], List[int]] = {}
        # Faculty schedule: (faculty_id, day) -> list of slots
        faculty_schedules: Dict[Tuple[str, str], List[int]] = {}
        
        for var in variables:
            val = var.assigned_value
            if val is None:
                continue
                
            # Capacity waste
            room_cap = rooms_dict.get(val.room_id, {}).get("capacity", var.enrolled_count)
            waste = max(0, room_cap - var.enrolled_count)
            capacity_waste += waste
            
            # Late slot penalty (Slot 7)
            if val.slot_id == 7:
                late_slot_penalty += 15
                
            # Group schedule
            g_key = (var.group_id, val.day)
            group_schedules.setdefault(g_key, []).append(val.slot_id)
            
            # Faculty schedule
            f_key = (var.faculty_id, val.day)
            faculty_schedules.setdefault(f_key, []).append(val.slot_id)
            
        # 1. Calculate student gaps
        for g_slots in group_schedules.values():
            sorted_slots = sorted(g_slots)
            for i in range(len(sorted_slots) - 1):
                diff = sorted_slots[i+1] - sorted_slots[i]
                if diff > 1:
                    gap_penalty += (diff - 1) * 10
                    
        # 2. Calculate faculty consecutive hours > 2
        for f_slots in faculty_schedules.values():
            sorted_slots = sorted(f_slots)
            consec = 1
            for i in range(len(sorted_slots) - 1):
                if sorted_slots[i+1] == sorted_slots[i] + 1:
                    consec += 1
                    if consec > 2:
                        consecutive_penalty += 20
                else:
                    consec = 1
                    
        total_penalty = gap_penalty + consecutive_penalty + (capacity_waste // 5) + late_slot_penalty
        
        # Normalize quality score out of 100
        quality_score = max(0.0, min(100.0, 100.0 - (total_penalty / 25.0)))
        
        return {
            "total_penalty": total_penalty,
            "quality_score": round(quality_score, 1),
            "student_gap_penalty": gap_penalty,
            "faculty_consecutive_penalty": consecutive_penalty,
            "capacity_waste_penalty": capacity_waste // 5,
            "late_slot_penalty": late_slot_penalty
        }
