"""
Comprehensive Academic Word Report Generator (IEEE / University Technical Paper)
Generates the official .docx report containing all 28 sections, styled tables, equations, and embedded diagrams.

SIH 2025 | Problem Statement SIH25091
Team: Gandikota Sai Chandana (12511912) & Inayat (12512142)
Subject Code: K3P25IL
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_dir = os.path.join(base_dir, "docs")
screenshots_dir = os.path.join(base_dir, "screenshots")
os.makedirs(docs_dir, exist_ok=True)

# Elegant Pastel / Slate Theme Palette
COLOR_PRIMARY_HEX = "1E3A8A"     # Deep Academic Navy
COLOR_SECONDARY_HEX = "0D9488"   # Teal
COLOR_TEXT_HEX = "1E293B"        # Charcoal Body Text
COLOR_MUTED_HEX = "64748B"       # Slate Muted
COLOR_LIGHT_BG_HEX = "F8FAFC"    # Pastel Warm White
COLOR_ACCENT_BG_HEX = "F1F5F9"   # Table Header / Callout Fill

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = 'Helvetica'
        if level == 1:
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(30, 58, 138) # Navy
        elif level == 2:
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = RGBColor(13, 148, 136) # Teal
        else:
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(51, 65, 85)
    return h

def add_bullet_point(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_bold = p.add_run(bold_prefix + " ")
    run_bold.bold = True
    run_bold.font.name = 'Helvetica'
    run_bold.font.size = Pt(9.5)
    run_bold.font.color.rgb = RGBColor(30, 41, 59)
    
    run_text = p.add_run(text)
    run_text.font.name = 'Helvetica'
    run_text.font.size = Pt(9.5)
    run_text.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout(doc, title, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(title + "\n")
    r1.bold = True
    r1.font.name = 'Helvetica'
    r1.font.size = Pt(10)
    r1.font.color.rgb = RGBColor(30, 58, 138)
    
    r2 = p.add_run(text)
    r2.font.name = 'Helvetica'
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(71, 85, 105)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def generate_docx():
    doc = Document()
    
    # Page Setup (Letter, 1 inch margins)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System | SIH25091")
        hrun.font.size = Pt(8)
        hrun.font.name = 'Helvetica'
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Team: Gandikota Sai Chandana (12511912) & Inayat (12512142) • Subject: K3P25IL")
        frun.font.size = Pt(8)
        frun.font.name = 'Helvetica'
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # 1. Document Title & Header
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(6)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cat = title_p.add_run("SMART INDIA HACKATHON 2025 | PROBLEM STATEMENT SIH25091\n")
    r_cat.bold = True
    r_cat.font.name = 'Helvetica'
    r_cat.font.size = Pt(10)
    r_cat.font.color.rgb = RGBColor(37, 99, 235)
    
    r_title = title_p.add_run("NEP-2020 MULTIDISCIPLINARY ACADEMIC TIMETABLE PLANNING AND CONFLICT RESOLUTION SYSTEM\n")
    r_title.bold = True
    r_title.font.name = 'Helvetica'
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    r_sub = title_p.add_run("A Constraint Satisfaction Problem (CSP) Heuristic Engine with Supervised ML Conflict Prioritization")
    r_sub.font.name = 'Helvetica'
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Author Block
    auth_p = doc.add_paragraph()
    auth_p.paragraph_format.space_before = Pt(8)
    auth_p.paragraph_format.space_after = Pt(14)
    auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_auth = auth_p.add_run(
        "Gandikota Sai Chandana (Registration No. 12511912 | Group RK3P25ILA15)\n"
        "Inayat (Registration No. 12512142 | Group RK3P25ILA16)\n"
        "Department of Computer Science & Engineering | Subject Code & Section: K3P25IL\n"
        "Submission Date: 15 November 2026"
    )
    r_auth.font.name = 'Helvetica'
    r_auth.font.size = Pt(9.5)
    r_auth.font.color.rgb = RGBColor(51, 65, 85)

    # -------------------------------------------------------------
    # 2. Abstract & Keywords
    # -------------------------------------------------------------
    add_callout(
        doc,
        "ABSTRACT",
        "Under the National Education Policy (NEP) 2020, Indian universities transition from rigid departmental silos "
        "to a multidisciplinary Choice Based Credit System (CBCS) encompassing Major Disciplines (DSC), Minor Electives (DSE), "
        "Multidisciplinary Courses (MDC), Ability Enhancement (AEC), Skill Enhancement (SEC), and Value-Added Courses (VAC). "
        "This paper presents a complete, production-grade academic timetable planning and conflict resolution architecture "
        "formulated as a Constraint Satisfaction Problem (CSP). The system combines heuristic backtracking search—employing "
        "Minimum Remaining Values (MRV), Degree heuristic tie-breaking, Least Constraining Value (LCV) ordering, and Forward "
        "Checking domain pruning—with a lightweight supervised Random Forest classifier trained on 1,800 synthetic historical "
        "records (98.06% accuracy, 0.9862 F1-score). In empirical head-to-head benchmarking across 89 required weekly sessions, "
        "both classical heuristic CSP and ML-assisted CSP achieved 100% complete, certified conflict-free allocations (0 hard-constraint "
        "violations). When overconstrained problem instances occur, an explainable diagnostic module isolates the exact bottleneck "
        "with actionable remedies. The application is packaged in a professional light-mode Streamlit dashboard with automated "
        "multi-format exports (Word, Excel, PDF, CSV).\n\n"
        "Keywords: Academic Timetabling, Constraint Satisfaction Problem (CSP), Heuristic Backtracking, NEP-2020, Supervised Machine Learning, Conflict Resolution, Explainable AI."
    )

    # -------------------------------------------------------------
    # 3. Introduction & 4. Problem Statement
    # -------------------------------------------------------------
    add_heading_styled(doc, "1. Introduction & Background", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Academic timetable generation is a classical NP-complete combinatorial optimization challenge. In higher education, the objective "
        "is to assign an ensemble of course sessions across finite discrete time slots, instructional facilities, and faculty instructors "
        "such that all operational hard constraints are strictly satisfied while soft ergonomic preferences are optimized. Historically, "
        "institutions relied on manual spreadsheet formulation or basic greedy heuristics. While viable for monolithic batch programs, "
        "these traditional methodologies completely disintegrate under the multidimensional elective mobility introduced by the "
        "National Education Policy (NEP) 2020."
    )

    add_heading_styled(doc, "2. Problem Statement (SIH25091)", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Design, develop, and benchmark an automated multidisciplinary timetable planning system capable of resolving concurrent faculty, "
        "facility, and elective cohort collisions under NEP-2020 curriculum guidelines, providing explainable diagnostics upon schedule "
        "infeasibility, ensuring independent verification, and delivering comprehensive multi-format reports."
    )

    # -------------------------------------------------------------
    # 5. Objectives & 6. NEP-2020 Relevance
    # -------------------------------------------------------------
    add_heading_styled(doc, "3. Project Objectives & Scope", level=1)
    add_bullet_point(doc, "Mathematical CSP Formulation:", "Model academic timetabling rigorously as a CSP <X, D, C> with 10 hard and 6 soft ergonomic constraints.")
    add_bullet_point(doc, "Heuristic Search Engine:", "Implement MRV variable ordering, Degree heuristic tie-breaking, LCV value ordering, and Forward Checking domain pruning.")
    add_bullet_point(doc, "Supervised Machine Learning Guidance:", "Train a lightweight Random Forest model to predict candidate conflict likelihood and prioritize candidate domain values.")
    add_bullet_point(doc, "Explainable Diagnostics:", "Provide human-readable root-cause explanations identifying why an overconstrained schedule is infeasible.")
    add_bullet_point(doc, "Independent Validation Gate:", "Certify zero hard-constraint violations using a separate validation audit function.")

    add_heading_styled(doc, "4. NEP-2020 Academic Relevance", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "NEP-2020 restructures undergraduate curriculum into six distinct baskets: (1) Discipline Specific Core (DSC), (2) Discipline Specific "
        "Electives (DSE), (3) Multidisciplinary Courses (MDC), (4) Ability Enhancement (AEC), (5) Skill Enhancement (SEC), and (6) Value-Added Courses (VAC). "
        "Students across engineering, humanities, and sciences cross-register into common elective blocks, creating combinatorial timetable clashes "
        "that manual planning cannot prevent."
    )

    # -------------------------------------------------------------
    # 7. Related Work & 8. Project Features
    # -------------------------------------------------------------
    add_heading_styled(doc, "5. Related Work & Literature Review", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "University timetabling algorithms in literature broadly fall into four paradigms: (a) Operations Research approaches using Mixed Integer "
        "Linear Programming (MILP), (b) Metaheuristics such as Genetic Algorithms and Simulated Annealing, (c) Constraint Satisfaction Problems (CSP) "
        "with heuristic backtracking, and (d) Modern Hyper-heuristics with Machine Learning. While MILP solvers guarantee optimality, their scaling "
        "behavior degrades exponentially with multidisciplinary elective overlap. Metaheuristics often find good approximate solutions but lack "
        "formal proofs of infeasibility and provide no diagnostic explanations when constraints cannot be satisfied. Our architecture utilizes "
        "CSP with forward checking because it allows deterministic constraint enforcement, immediate inconsistency pruning, and explicit explainability."
    )

    # -------------------------------------------------------------
    # 9. Dataset Details & Synthetic Disclosure
    # -------------------------------------------------------------
    add_heading_styled(doc, "6. Dataset Architecture & Synthetic Data Disclosure", level=1)
    add_callout(
        doc,
        "SYNTHETIC DEMONSTRATION DATA DISCLOSURE",
        "To protect student privacy and comply with institutional research ethics, all data used in this project is 100% SYNTHETIC "
        "DEMONSTRATION DATA algorithmically generated using Python with a fixed random seed (seed = 42). It contains no confidential "
        "university PII, while strictly mirroring the operational scale and complexity of real collegiate institutions under NEP-2020."
    )

    # Dataset Table
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Entity Archetype", "Scale Count", "Operational Parameters & Constraints"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Helvetica'
        cell.paragraphs[0].runs[0].font.size = Pt(9)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, COLOR_PRIMARY_HEX)
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    rows_data = [
        ("Academic Courses", "26 courses", "Major Core (DSC), Minor (DSE), MDC, AEC, SEC, VAC; 2-4 credits each"),
        ("Faculty Roster", "20 members", "Professors, Assoc. Profs, Asst. Profs; Max daily load <= 4h; Blackout slots"),
        ("Classrooms & Labs", "14 facilities", "Auditoriums (100-120), Classrooms (50-65), Labs (55-60); 945 seats total"),
        ("Student Cohorts", "10 groups", "B.Tech CSE, AI&DS, Data Science, ECE, MDC Cohorts; 410 students enrolled"),
        ("Time Slots & Days", "35 periods", "5 Working Days (Mon-Fri) x 7 daily 60-min slots (09:00 - 17:00 with lunch interval)"),
        ("Curriculum Sessions", "89 sessions", "Discrete weekly contact sessions requiring conflict-free CSP assignment"),
        ("Pre-Fixed Sessions", "5 allocations", "Institutional locked events (Dean's Colloquium, Keynotes, Industry Seminars)"),
    ]
    for r in rows_data:
        row_cells = tbl.add_row().cells
        for col_idx, text in enumerate(r):
            cell = row_cells[col_idx]
            cell.paragraphs[0].text = text
            cell.paragraphs[0].runs[0].font.name = 'Helvetica'
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            set_cell_background(cell, "FFFFFF" if len(tbl.rows) % 2 == 0 else "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 10. System Architecture & Embedded Diagram
    # -------------------------------------------------------------
    add_heading_styled(doc, "7. System Architecture", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "The architecture is partitioned into four decoupled layers: (1) Ingestion & Validation Gate, (2) ML Feature Engineering & Classifier, "
        "(3) Heuristic Backtracking CSP Solver, and (4) Independent Verification & Reporting Interface. Figure 1 illustrates the operational flow."
    )
    arch_img = os.path.join(screenshots_dir, "system_architecture_diagram.png")
    if os.path.exists(arch_img):
        doc.add_picture(arch_img, width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = cap.add_run("Figure 1: Modular 4-tier system architecture of the NEP-2020 timetable planning framework.")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # 11. CSP Mathematical Formulation & 12. Constraints
    # -------------------------------------------------------------
    add_heading_styled(doc, "8. CSP Mathematical Formulation", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "We formalize academic scheduling as a triple P = <X, D, C>, where:\n"
        "• Variables (X): The set of n = 89 weekly contact sessions X = {x_1, x_2, ..., x_n}, where each x_i = (course_i, group_i, faculty_i, room_type_i, enrolled_i).\n"
        "• Domains (D): For each variable x_i, D(x_i) is the set of legal tuples v = (day, slot, room) in Days x Slots x Rooms, satisfying room.capacity >= enrolled_i and room.type == room_type_i, excluding designated faculty blackout slots.\n"
        "• Constraints (C): Decomposed into hard constraints C_H that must hold strictly, and soft penalties C_S that govern ergonomic quality."
    )

    add_heading_styled(doc, "9. Hard and Soft Constraints", level=1)
    add_heading_styled(doc, "Mandatory Hard Constraints (10/10 Enforced):", level=2)
    add_bullet_point(doc, "1. Faculty Collision Prevention:", "No faculty member teaches two sessions simultaneously: Forall t, Faculty(t) <= 1.")
    add_bullet_point(doc, "2. Room Collision Prevention:", "No facility hosts two sessions concurrently: Forall t, Room(t) <= 1.")
    add_bullet_point(doc, "3. Student Cohort Collision Prevention:", "A student group cannot attend two classes at once: Forall t, Group(t) <= 1.")
    add_bullet_point(doc, "4. Room Capacity Compliance:", "Room capacity must accommodate enrolled students: Capacity(room) >= Strength(group).")
    add_bullet_point(doc, "5. Room Archetype Match:", "Course room type requirement matches facility classification (e.g. Lab in Lab).")
    add_bullet_point(doc, "6. Faculty Availability Adherence:", "No sessions scheduled during designated faculty blackout hours.")
    add_bullet_point(doc, "7. Daily Faculty Workload Limit:", "Daily teaching hours for any instructor must not exceed 4 hours per day.")
    add_bullet_point(doc, "8. Pre-Fixed Allocations Preservation:", "Fixed institutional events (e.g. Dean's Colloquium) remain immutable.")
    add_bullet_point(doc, "9. Weekly Curriculum Compliance:", "Every course in curriculum must be assigned exactly its required contact sessions.")
    add_bullet_point(doc, "10. Elective Non-Clashing:", "Cross-departmental elective blocks must not conflict with major core lectures.")

    add_heading_styled(doc, "Ergonomic Soft Constraints (6 Dimensions):", level=2)
    add_bullet_point(doc, "1. Student Idle Gap Penalty:", "Minimize idle 1-2 hour gaps between classes on the same day.")
    add_bullet_point(doc, "2. Faculty Fatigue Mitigation:", "Avoid >2 consecutive teaching hours for any instructor.")
    add_bullet_point(doc, "3. Capacity Efficiency Index:", "Minimize unused seats to maximize room utilization.")
    add_bullet_point(doc, "4. Late Slot Burden:", "Reduce allocation of late afternoon slots (Slot 7: 16:00-17:00).")
    add_bullet_point(doc, "5. Day Distribution Balance:", "Distribute course contact hours evenly across Monday-Friday.")
    add_bullet_point(doc, "6. Overall Ergonomics:", "Normalized quality score evaluated on a scale of 0 to 100.")

    # -------------------------------------------------------------
    # 13. Heuristic Search Methodology
    # -------------------------------------------------------------
    add_heading_styled(doc, "10. Heuristic Search Methodology", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "To navigate the immense search space (35^89 possible assignments), we implement four classical CSP heuristics: "
        "(1) Minimum Remaining Values (MRV): Selects the unassigned variable with the fewest legal values remaining ('fail-first principle'), "
        "immediately exposing dead ends. (2) Degree Heuristic: Breaks MRV ties by picking the variable connected by constraints to the greatest "
        "number of remaining unassigned variables. (3) Least Constraining Value (LCV): Orders candidate domain values by the least number of choices "
        "eliminated from neighboring unassigned variables. (4) Forward Checking: Whenever a session is tentatively assigned to (day, slot, room), "
        "all conflicting values are pruned from neighboring unassigned domains. If any neighbor domain becomes empty, the solver backtracks immediately."
    )

    # -------------------------------------------------------------
    # 14. ML Classifier & Feature Engineering & 15. Integration
    # -------------------------------------------------------------
    add_heading_styled(doc, "11. Supervised Machine Learning Classifier & Integration", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "A supervised Random Forest classifier is trained on 1,800 historical allocation records using 15 engineered features: "
        "day_index, slot_index, is_peak_slot, is_late_slot, enrolled_students, room_capacity, room_capacity_ratio, room_type_match, "
        "is_lab_course, faculty_daily_load, faculty_weekly_load, faculty_available, group_daily_load, group_has_window_gap, and "
        "historical_collision_score. The classifier predicts conflict probability P(conflict). In ML-Assisted CSP, candidate values are "
        "prioritized using this predicted probability in a single vectorized batch call, sorting candidates with the lowest conflict risk first."
    )
    ml_img = os.path.join(screenshots_dir, "screenshot_ml_analytics.png")
    if os.path.exists(ml_img):
        doc.add_picture(ml_img, width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = cap.add_run("Figure 2: Random Forest feature importances and test set confusion matrix (98.06% Accuracy).")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # 16. Explainable Diagnostics
    # -------------------------------------------------------------
    add_heading_styled(doc, "12. Explainable Infeasibility Diagnostics", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "When an overconstrained or infeasible scheduling instance occurs, conventional solvers abort without context. Our diagnostic "
        "module inspects the unassigned session variables and identifies the root cause: (a) Faculty Availability Exhaustion, (b) Room Capacity "
        "Shortfall, (c) Room Type Unavailability, or (d) Concurrent Resource Saturation. It generates actionable administrative recommendations "
        "(e.g., relaxing faculty blackout windows, splitting student cohorts, or adding laboratory sessions)."
    )

    # -------------------------------------------------------------
    # 17. Implementation Details & 18. UI Screenshots
    # -------------------------------------------------------------
    add_heading_styled(doc, "13. Implementation & Interactive Light-Mode Interface", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "The system is implemented in Python 3.11 with Streamlit 1.42, styled in an aesthetic pastel palette (#F5EBE1, #D7BDB0, #E3D5CA, #D6CCC2, #EDEEE9) "
        "with elegant serif headings and clean rounded capsule cards. Figure 3 displays the Executive Dashboard."
    )
    dash_img = os.path.join(screenshots_dir, "screenshot_executive_dashboard.png")
    if os.path.exists(dash_img):
        doc.add_picture(dash_img, width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = cap.add_run("Figure 3: Executive Dashboard and Weekly Timetable Viewer in aesthetic light mode.")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # 19. Results & 20. Testing & 21. Benchmarking
    # -------------------------------------------------------------
    add_heading_styled(doc, "14. Empirical Benchmarking & Comparative Evaluation", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Both solvers were evaluated on identical benchmark problem instances (89 required weekly sessions across 26 courses, "
        "20 faculty, 14 rooms, and 10 student groups). Table 2 presents the authentic empirical benchmark metrics."
    )

    tbl_b = doc.add_table(rows=1, cols=4)
    tbl_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_headers = ["Performance Metric", "Baseline Heuristic CSP", "ML-Assisted CSP", "Observed Empirical Delta"]
    for col_idx, h in enumerate(b_headers):
        cell = tbl_b.cell(0, col_idx)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Helvetica'
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, COLOR_PRIMARY_HEX)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    bench_rows = [
        ("Feasibility Status", "OPTIMAL_FEASIBLE", "OPTIMAL_FEASIBLE", "Identical Feasibility"),
        ("Schedule Completeness", "100.0% (89/89 sessions)", "100.0% (89/89 sessions)", "0.0% (Both Complete)"),
        ("Execution Search Time", "0.4721 seconds", "4.1817 seconds", "+3.7096 s (ML Inference Overhead)"),
        ("Search Nodes Explored", "85 nodes", "85 nodes", "0 nodes delta"),
        ("Backtracking Operations", "0 backtracks", "0 backtracks", "0 backtracks delta"),
        ("Forward Check Prunings", "1,936 prunings", "2,208 prunings", "+272 prunings (Deeper Pruning)"),
        ("Hard Constraint Violations", "0 (Zero Hard Clashes)", "0 (Zero Hard Clashes)", "Certified 100% Valid"),
        ("Ergonomic Quality Score", "45.1 / 100", "26.6 / 100", "-18.5 quality delta"),
        ("ML Test Accuracy / F1", "N/A (Classical Heuristic)", "98.06% Acc | 0.9862 F1", "Random Forest Guidance"),
    ]
    for r in bench_rows:
        row_cells = tbl_b.add_row().cells
        for col_idx, text in enumerate(r):
            cell = row_cells[col_idx]
            cell.paragraphs[0].text = text
            cell.paragraphs[0].runs[0].font.name = 'Helvetica'
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            set_cell_background(cell, "FFFFFF" if len(tbl_b.rows) % 2 == 0 else "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    bench_img = os.path.join(screenshots_dir, "screenshot_benchmark_comparison.png")
    if os.path.exists(bench_img):
        doc.add_picture(bench_img, width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = cap.add_run("Figure 4: Search time and schedule completeness benchmark comparison.")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # 22. Limitations & 23. Future Scope & 24. Societal Impact
    # -------------------------------------------------------------
    add_heading_styled(doc, "15. Limitations, Future Scope & Societal Impact", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Limitations: The ML inference overhead in Python adds search latency; compiling the feature pipeline with Cython "
        "or converting to ONNX Runtime would significantly reduce prediction time. Transit times between geographically detached "
        "campuses are not modeled.\n\n"
        "Future Scope: Integrating real-time student ERP registration webhooks, mobile push notifications for timetable revisions, "
        "and reinforcement learning for automated elective cohort balancing.\n\n"
        "Societal Impact: This system directly unlocks the academic vision of NEP-2020 by enabling colleges to offer flexible multidisciplinary "
        "education without administrative gridlock. It safeguards faculty wellbeing by enforcing daily teaching limits and eliminating "
        "fatiguing back-to-back lectures."
    )

    # -------------------------------------------------------------
    # 25. Team Contributions & 26. References
    # -------------------------------------------------------------
    add_heading_styled(doc, "16. Individual Team Contributions", level=1)
    add_bullet_point(
        doc,
        "Gandikota Sai Chandana (Registration No. 12511912 | Group RK3P25ILA15):",
        "Lead Architect for CSP mathematical formulation, 10 hard and 6 soft constraint definitions, heuristic search engine "
        "(MRV, Degree heuristic, LCV, Forward Checking), supervised machine learning classifier training, feature engineering, and head-to-head empirical benchmarking."
    )
    add_bullet_point(
        doc,
        "Inayat (Registration No. 12512142 | Group RK3P25ILA16):",
        "Lead Full-Stack Developer for Streamlit light-mode interface, data ingestion and validation pipelines, multi-view timetable visualization "
        "grids (Group, Faculty, Room), multi-format export engines (Word, Excel, PDF, CSV), and end-to-end integration testing."
    )
    add_bullet_point(
        doc,
        "Joint Responsibilities:",
        "Problem analysis, SIH25091 requirement synthesis, independent validation gate auditing, technical report authoring, PowerPoint presentation design, and quality assurance."
    )

    add_heading_styled(doc, "17. References", level=1)
    refs = [
        "[1] Ministry of Education, Government of India, 'National Education Policy 2020,' New Delhi, 2020.",
        "[2] S. Russell and P. Norvig, 'Artificial Intelligence: A Modern Approach,' 4th ed., Pearson, 2020, pp. 202-233 (Constraint Satisfaction Problems).",
        "[3] M. W. Carter and G. Laporte, 'Recent Developments in Practical Course Timetabling,' in Practice and Theory of Automated Timetabling II, Springer, 1998, pp. 3-19.",
        "[4] E. K. Burke, D. G. Elliman, and R. F. Weare, 'A Hybrid Genetic Algorithm for Highly Constrained Timetabling Problems,' Proc. 6th Int. Conf. on Genetic Algorithms, 1995, pp. 605-610.",
        "[5] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.",
        "[6] Smart India Hackathon (SIH), 'Problem Statement SIH25091: Multidisciplinary Timetable Planning and Conflict Resolution,' AICTE / MoE Innovation Cell, 2025."
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_after = Pt(2)
        r_run = p.add_run(r)
        r_run.font.name = 'Helvetica'
        r_run.font.size = Pt(8.5)
        r_run.font.color.rgb = RGBColor(71, 85, 105)

    docx_path = os.path.join(docs_dir, "NEP2020_Timetable_Project_Report.docx")
    doc.save(docx_path)
    print(f"[Word Report Generator] Successfully generated Word report at: {docx_path}")
    return docx_path

if __name__ == "__main__":
    generate_docx()
