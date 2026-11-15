"""
Comprehensive Pytest Test Suite for NEP-2020 Timetable System

SIH 2025 | Problem Statement SIH25091
Team: Gandikota Sai Chandana (12511912) & Inayat (12512142)
Subject Code: K3P25IL
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# Ensure project root is accessible
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from src.data.loader import TimetableDataLoader, DataValidator
from src.data.generator import generate_all_datasets
from src.ml.classifier import TimetableConflictClassifier
from src.csp.solver import TimetableCSPSolver
from src.csp.constraints import ScheduleState, SessionVariable, AssignmentValue
from src.validation.validator import IndependentTimetableValidator
from src.diagnostics.explainer import ConflictExplainer
from src.exports.exporter import TimetableExporter

@pytest.fixture(scope="session")
def project_data():
    """Load core dataset for testing."""
    data_dir = os.path.join(base_dir, "data", "synthetic")
    if not os.path.exists(os.path.join(data_dir, "courses.csv")):
        generate_all_datasets(os.path.join(base_dir, "data"))
    loader = TimetableDataLoader(data_dir=data_dir)
    return loader.load_all()

@pytest.fixture(scope="session")
def trained_model(project_data):
    """Ensure ML model is trained and available."""
    clf = TimetableConflictClassifier(model_dir=os.path.join(base_dir, "models"))
    if not clf.load_model():
        clf.train(project_data["historical_allocations"])
    return clf

def test_dataset_reproducibility_and_scale(project_data):
    """Test 1: Validate dataset scale and referential integrity."""
    assert len(project_data["courses"]) >= 24, "Should have 24-30 courses"
    assert len(project_data["faculty"]) >= 18, "Should have 18-22 faculty"
    assert len(project_data["rooms"]) >= 12, "Should have 12-15 rooms"
    assert len(project_data["student_groups"]) >= 8, "Should have 8-12 student groups"
    
    is_valid, errs = DataValidator.validate_schema(project_data)
    assert is_valid, f"Schema validation failed: {errs}"
    
    is_ref_valid, ref_errs = DataValidator.validate_referential_integrity(project_data)
    assert is_ref_valid, f"Referential integrity failed: {ref_errs}"

def test_faculty_collision_prevention():
    """Test 2: Ensure state rejects assigning faculty to two concurrent sessions."""
    state = ScheduleState(faculty_max_daily={"FAC01": 4})
    var1 = SessionVariable(
        var_id="V1", curriculum_id="C1", course_id="CS101", course_name="CS",
        group_id="G1", faculty_id="FAC01", faculty_name="Dr. Raman",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    var2 = SessionVariable(
        var_id="V2", curriculum_id="C2", course_id="CS201", course_name="DSA",
        group_id="G2", faculty_id="FAC01", faculty_name="Dr. Raman",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    val = AssignmentValue(day="Monday", slot_id=2, room_id="ROOM_CR201")
    
    # First assignment succeeds
    is_v1, _ = state.is_valid_assignment(var1, val)
    assert is_v1 is True
    state.assign(var1, val)
    
    # Second assignment with same faculty at same time must be rejected
    is_v2, reason = state.is_valid_assignment(var2, val)
    assert is_v2 is False
    assert "Faculty FAC01 already scheduled" in reason

def test_room_collision_prevention():
    """Test 3: Ensure state rejects assigning room to two concurrent classes."""
    state = ScheduleState(faculty_max_daily={"FAC01": 4, "FAC02": 4})
    var1 = SessionVariable(
        var_id="V1", curriculum_id="C1", course_id="CS101", course_name="CS",
        group_id="G1", faculty_id="FAC01", faculty_name="Dr. Raman",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    var2 = SessionVariable(
        var_id="V2", curriculum_id="C2", course_id="MA101", course_name="Math",
        group_id="G2", faculty_id="FAC02", faculty_name="Dr. Patel",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    val = AssignmentValue(day="Tuesday", slot_id=3, room_id="ROOM_CR201")
    state.assign(var1, val)
    
    is_v2, reason = state.is_valid_assignment(var2, val)
    assert is_v2 is False
    assert "Room ROOM_CR201 already booked" in reason

def test_student_group_collision_prevention():
    """Test 4: Ensure state rejects assigning student group to two concurrent classes."""
    state = ScheduleState(faculty_max_daily={"FAC01": 4, "FAC02": 4})
    var1 = SessionVariable(
        var_id="V1", curriculum_id="C1", course_id="CS101", course_name="CS",
        group_id="GRP_CSE_A", faculty_id="FAC01", faculty_name="Dr. Raman",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    var2 = SessionVariable(
        var_id="V2", curriculum_id="C2", course_id="PH101", course_name="Physics",
        group_id="GRP_CSE_A", faculty_id="FAC02", faculty_name="Dr. Joshi",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    val1 = AssignmentValue(day="Wednesday", slot_id=1, room_id="ROOM_CR201")
    val2 = AssignmentValue(day="Wednesday", slot_id=1, room_id="ROOM_CR202")
    state.assign(var1, val1)
    
    is_v2, reason = state.is_valid_assignment(var2, val2)
    assert is_v2 is False
    assert "Student Group GRP_CSE_A has concurrent session" in reason

def test_faculty_daily_workload_limit():
    """Test 5: Ensure faculty cannot exceed daily workload limit (4 hours)."""
    state = ScheduleState(faculty_max_daily={"FAC01": 4})
    var = SessionVariable(
        var_id="V1", curriculum_id="C1", course_id="CS101", course_name="CS",
        group_id="G1", faculty_id="FAC01", faculty_name="Dr. Raman",
        session_index=1, required_room_type="Classroom", enrolled_count=40, is_lab=False
    )
    # Assign 4 slots on Thursday
    for s in [1, 2, 3, 4]:
        val = AssignmentValue(day="Thursday", slot_id=s, room_id=f"ROOM_CR20{s}")
        state.assign(var, val)
        
    # 5th slot must be blocked
    val5 = AssignmentValue(day="Thursday", slot_id=5, room_id="ROOM_CR205")
    is_valid, reason = state.is_valid_assignment(var, val5)
    assert is_valid is False
    assert "exceeds daily workload limit" in reason

def test_ml_model_metrics_and_generalization(trained_model, project_data):
    """Test 6: Verify classifier accuracy, ROC-AUC, and leakage-safe test results."""
    metrics = trained_model.metrics
    assert metrics["accuracy"] >= 0.85, "Classifier accuracy must be >= 85%"
    assert metrics["f1_score"] >= 0.85, "Classifier F1 must be >= 85%"
    assert metrics["roc_auc"] >= 0.90, "Classifier ROC-AUC must be >= 90%"
    assert len(metrics["feature_importances"]) == 15, "All 15 engineered features must be evaluated"

def test_baseline_csp_end_to_end_validation(project_data):
    """Test 7: Verify baseline CSP generates conflict-free, 100% complete schedule."""
    solver = TimetableCSPSolver(
        data_dict=project_data,
        solver_mode="baseline",
        max_backtracks=2000,
        timeout_seconds=15.0
    )
    res = solver.solve()
    assert res["status"] == "OPTIMAL_FEASIBLE"
    assert res["is_complete"] is True
    assert res["completeness_pct"] == 100.0
    
    # Independent certification
    is_valid, violations = IndependentTimetableValidator.validate(res["schedule_records"], project_data)
    assert is_valid is True, f"Independent validator detected violations: {violations}"
    assert len(violations) == 0

def test_ml_assisted_csp_end_to_end_validation(project_data, trained_model):
    """Test 8: Verify ML-assisted CSP generates conflict-free, 100% complete schedule."""
    solver = TimetableCSPSolver(
        data_dict=project_data,
        solver_mode="ml_assisted",
        max_backtracks=2000,
        timeout_seconds=20.0,
        ml_classifier=trained_model
    )
    res = solver.solve()
    assert res["status"] == "OPTIMAL_FEASIBLE"
    assert res["is_complete"] is True
    
    # Independent certification
    is_valid, violations = IndependentTimetableValidator.validate(res["schedule_records"], project_data)
    assert is_valid is True, f"ML-assisted schedule failed validation: {violations}"
    assert len(violations) == 0

def test_infeasible_problem_diagnostics(project_data):
    """Test 9: Verify infeasible problem is trapped and explainable root causes are reported."""
    loader = TimetableDataLoader(data_dir=os.path.join(base_dir, "data", "synthetic"))
    infeasible_data = loader.get_infeasible_benchmark_instance()
    
    solver = TimetableCSPSolver(
        data_dict=infeasible_data,
        solver_mode="baseline",
        max_backtracks=300,
        timeout_seconds=5.0
    )
    res = solver.solve()
    assert res["status"] in ["INFEASIBLE", "MAX_BACKTRACKS_EXCEEDED", "TIMEOUT"]
    
    unassigned = [v for v in solver.variables if not v.is_assigned()]
    diagnostics = ConflictExplainer.diagnose_unassigned_sessions(
        unassigned, infeasible_data, solver.rooms_dict
    )
    assert len(diagnostics) > 0
    # Must identify faculty availability or room type/capacity constraint
    categories = [d["constraint_violated"] for d in diagnostics]
    assert any("Faculty" in c or "Room" in c or "Concurrent" in c for c in categories)

def test_export_deliverables(project_data):
    """Test 10: Verify multi-format exports (CSV, multi-sheet Excel, PDF)."""
    solver = TimetableCSPSolver(data_dict=project_data, solver_mode="baseline", max_backtracks=1000)
    res = solver.solve()
    records = res["schedule_records"]
    
    test_out = os.path.join(base_dir, "outputs", "test_runs")
    os.makedirs(test_out, exist_ok=True)
    
    csv_f = os.path.join(test_out, "test_sched.csv")
    excel_f = os.path.join(test_out, "test_sched.xlsx")
    pdf_f = os.path.join(test_out, "test_sched.pdf")
    
    TimetableExporter.export_to_csv(records, csv_f)
    TimetableExporter.export_to_excel(records, excel_f, audit_summary={"audit_status": "PASSED", "total_hard_violations": 0})
    TimetableExporter.export_to_pdf(records, pdf_f, sample_group_id="GRP_CSE_A")
    
    assert os.path.exists(csv_f) and os.path.getsize(csv_f) > 0
    assert os.path.exists(excel_f) and os.path.getsize(excel_f) > 0
    assert os.path.exists(pdf_f) and os.path.getsize(pdf_f) > 0
