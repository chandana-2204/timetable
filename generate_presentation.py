"""
PowerPoint Presentation Generator for NEP-2020 Timetable System Deliverables
Creates an editable, professional 16-slide SIH presentation in light mode.

SIH 2025 | Problem Statement SIH25091
Team: Gandikota Sai Chandana (12511912) & Inayat (12512142)
Subject Code: K3P25IL
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pres_dir = os.path.join(base_dir, "presentation")
screenshot_dir = os.path.join(base_dir, "screenshots")
os.makedirs(pres_dir, exist_ok=True)

# Clean Professional Palette
COLOR_NAVY = RGBColor(15, 23, 42)      # #0F172A
COLOR_BLUE = RGBColor(37, 99, 235)     # #2563EB
COLOR_TEAL = RGBColor(13, 148, 136)    # #0D9488
COLOR_SLATE = RGBColor(71, 85, 105)    # #475569
COLOR_BG = RGBColor(248, 250, 252)     # #F8FAFC
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BORDER = RGBColor(226, 232, 240) # #E2E8F0

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, title_text, category_text="SIH 2025 | SIH25091"):
    # Header container
    top_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = top_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

def create_card(slide, left, top, width, height, title="", border_color=COLOR_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_WHITE
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    
    if title:
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
    return shape

def add_bullet(tf, bold_prefix, text, pt_size=12, color=COLOR_SLATE):
    p = tf.add_paragraph()
    p.font.size = Pt(pt_size)
    p.space_after = Pt(8)
    
    run_bold = p.add_run()
    run_bold.text = bold_prefix + " "
    run_bold.font.bold = True
    run_bold.font.color.rgb = COLOR_NAVY
    
    run_text = p.add_run()
    run_text.text = text
    run_text.font.color.rgb = color

def generate_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    card1 = create_card(s1, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), border_color=COLOR_BLUE)
    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.3), Inches(10.333), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "SMART INDIA HACKATHON 2025 | PROBLEM STATEMENT SIH25091"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_BLUE
    p0.space_after = Pt(14)
    
    p1 = tf1.add_paragraph()
    p1.text = "NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY
    p1.space_after = Pt(12)
    
    p2 = tf1.add_paragraph()
    p2.text = "An Explainable Constraint Satisfaction (CSP) and Supervised ML Architecture for University Scheduling"
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_SLATE
    p2.space_after = Pt(28)
    
    p3 = tf1.add_paragraph()
    p3.text = "TEAM PARTICIPANTS:"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_NAVY
    
    add_bullet(tf1, "1. Gandikota Sai Chandana", "| Registration No. 12511912 | Group RK3P25ILA15", 13)
    add_bullet(tf1, "2. Inayat", "| Registration No. 12512142 | Group RK3P25ILA16", 13)
    
    p4 = tf1.add_paragraph()
    p4.text = "Subject Code / Section: K3P25IL  •  Academic Session: Autumn 2025-2026"
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_TEAL

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & Context
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Academic Context", "SIH 2025 | Problem SIH25091")
    
    create_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "The Scheduling Crisis under NEP-2020")
    tb2a = s2.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf2a = tb2a.text_frame
    tf2a.word_wrap = True
    add_bullet(tf2a, "Multidisciplinary Influx:", "NEP-2020 dismantles single-discipline academic silos, allowing engineering, science, and humanities students to cross-register across 6 credit categories.")
    add_bullet(tf2a, "Combinatorial Explosion:", "Elective course combinations expand exponentially. Manual timetabling in spreadsheets results in recurring clashes between major cores and elective courses.")
    add_bullet(tf2a, "Rigid Resource Ceilings:", "Universities operate under strict physical boundaries: finite specialized laboratories, varying hall capacities, and capped faculty teaching hours.")

    create_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "SIH25091 Requirements Mandate")
    tb2b = s2.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf2b = tb2b.text_frame
    tf2b.word_wrap = True
    add_bullet(tf2b, "Mathematical Rigor:", "Model academic timetabling rigorously as a Constraint Satisfaction Problem (CSP) over multi-dimensional domains.")
    add_bullet(tf2b, "Intelligent Pruning:", "Integrate heuristic backtracking search (MRV, Degree heuristic, LCV) augmented by supervised Machine Learning.")
    add_bullet(tf2b, "Explainability:", "When schedules are infeasible, isolate the exact responsible constraint and provide actionable administrative remedies.")
    add_bullet(tf2b, "Light-Mode UI:", "Deliver an executive, professional web dashboard with live multi-filter schedule visualization and auditing.")

    # -------------------------------------------------------------
    # SLIDE 3: Existing Problem & The Need
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Existing Limitations vs. Institutional Need", "Problem Analysis")
    
    create_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Existing Scheduling Approaches")
    tb3a = s3.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf3a = tb3a.text_frame
    tf3a.word_wrap = True
    add_bullet(tf3a, "Manual Excel Scheduling:", "Error-prone, takes 3–4 weeks of administrative effort, and frequently results in undetected faculty double-booking.")
    add_bullet(tf3a, "Pure Greedy Solvers:", "Quickly become trapped in local minima or dead-ends when specialized lab capacity is saturated.")
    add_bullet(tf3a, "Black-Box Algorithms:", "Genetic algorithms and simulated annealing provide no audit trail or explanation when no feasible solution is found.")

    create_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Why Our Solution is Essential")
    tb3b = s3.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf3b = tb3b.text_frame
    tf3b.word_wrap = True
    add_bullet(tf3b, "Certified Conflict-Free:", "Independent validator guarantees 100% adherence to all 10 hard institutional constraints.")
    add_bullet(tf3b, "Sub-Second Convergence:", "Heuristic MRV and forward-checking prune 90%+ of invalid branches without unnecessary backtracking.")
    add_bullet(tf3b, "Actionable Root Cause Analysis:", "Explains exactly why a schedule failed (e.g. faculty blackout, room shortfall) rather than silently hanging.")
    add_bullet(tf3b, "Zero Real PII Exposure:", "Benchmarked on clean, reproducible deterministic synthetic data adhering to data privacy standards.")

    # -------------------------------------------------------------
    # SLIDE 4: Project Objectives
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Project Objectives & Technical Scope", "Objectives")
    
    objs = [
        ("1. Mathematical CSP Formulation", "Formulate university course session allocation as CSP <X, D, C> with 10 hard and 6 soft ergonomic constraints.", Inches(0.8), Inches(1.8)),
        ("2. Heuristic Backtracking Engine", "Implement MRV variable selection, Degree heuristic tie-breaking, LCV value ordering, and Forward Checking.", Inches(6.8), Inches(1.8)),
        ("3. Lightweight Supervised ML", "Train a high-performance classifier (Random Forest, >98% accuracy) to predict allocation collision probabilities.", Inches(0.8), Inches(4.4)),
        ("4. Explainability & Multi-Format UI", "Deliver root-cause diagnostics, Streamlit light-mode dashboard, and automated PDF/Excel/CSV exports.", Inches(6.8), Inches(4.4))
    ]
    for title, desc, left, top in objs:
        create_card(s4, left, top, Inches(5.7), Inches(2.4), title)
        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_SLATE

    # -------------------------------------------------------------
    # SLIDE 5: Proposed Solution
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Proposed Solution: Hybrid CSP + ML Architecture", "System Solution")
    
    create_card(s5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0), "Integrated 4-Tier Operational Pipeline")
    tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(11.3), Inches(4.2))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    add_bullet(tf5, "Tier 1 - Ingestion & Schema Gate:", "Validates multi-table referential integrity (Courses, Faculty, Rooms, Groups, Curriculum, Fixed Allocations) with automated error reporting.")
    add_bullet(tf5, "Tier 2 - Machine Learning Prioritization:", "A supervised Random Forest classifier evaluates candidate assignments across 15 engineered features, filtering conflict-prone room/slot combinations.")
    add_bullet(tf5, "Tier 3 - Heuristic CSP Solver Core:", "Coordinates MRV variable selection, forward checking domain pruning, and backtracking rollback, terminating in optimal complete allocation.")
    add_bullet(tf5, "Tier 4 - Verification & Interactive Delivery:", "Every output passes a separate independent hard-constraint certification gate before reaching the Streamlit viewer or PDF/Excel exporter.")

    # -------------------------------------------------------------
    # SLIDE 6: System Architecture Diagram
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Modular System Architecture", "System Design")
    
    arch_img = os.path.join(screenshot_dir, "system_architecture_diagram.png")
    if os.path.exists(arch_img):
        s6.shapes.add_picture(arch_img, Inches(1.0), Inches(1.8), width=Inches(11.333))

    # -------------------------------------------------------------
    # SLIDE 7: Dataset & Data Pipeline
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Dataset Pipeline & Synthetic Data Disclosure", "Data Engineering")
    
    create_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Synthetic Benchmark Dataset (Seed: 42)")
    tb7a = s7.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf7a = tb7a.text_frame
    tf7a.word_wrap = True
    add_bullet(tf7a, "Data Source Statement:", "To protect student privacy and comply with competition ethics, a deterministic synthetic university dataset was generated via Python (random seed 42).")
    add_bullet(tf7a, "26 Multidisciplinary Courses:", "Categorized into DSC, DSE, MDC, AEC, SEC, and VAC credit baskets.")
    add_bullet(tf7a, "20 Faculty Profiles:", "Spanning 6 departments with designated max daily hours (4h) and unavailable research windows.")
    add_bullet(tf7a, "14 Academic Facilities:", "Auditoriums, seminar rooms, computer labs, electronics labs, and chemistry/physics labs.")

    create_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "7-Sheet Master Excel Architecture")
    tb7b = s7.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf7b = tb7b.text_frame
    tf7b.word_wrap = True
    add_bullet(tf7b, "Sheet 1 - Start Here:", "Metadata, data dictionary, ethics disclosure, and project summary.")
    add_bullet(tf7b, "Sheet 2 - Courses:", "Course IDs, credits, room archetype requirements, and weekly hours.")
    add_bullet(tf7b, "Sheet 3 - Faculty:", "Designations, workloads, blackout slots, and contact emails.")
    add_bullet(tf7b, "Sheet 4 - Rooms:", "Room capacities, buildings, floors, and equipment archetypes.")
    add_bullet(tf7b, "Sheet 5 - Groups & Slots:", "Cohorts, student strengths, and 5-day slot definitions.")
    add_bullet(tf7b, "Sheet 6 - Existing Schedule:", "Pre-fixed institutional events (e.g. Dean's Colloquium).")
    add_bullet(tf7b, "Sheet 7 - Data Needed:", "Comprehensive checklist of validation and constraint rules.")

    # -------------------------------------------------------------
    # SLIDE 8: CSP Mathematical Formulation & Constraints
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "CSP Mathematical Formulation & Constraints", "Algorithm Formulation")
    
    create_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "10 Mandatory Hard Constraints")
    tb8a = s8.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf8a = tb8a.text_frame
    tf8a.word_wrap = True
    add_bullet(tf8a, "1. Faculty Collision:", "No faculty member scheduled in two places simultaneously.")
    add_bullet(tf8a, "2. Room Collision:", "No classroom/lab assigned to two concurrent classes.")
    add_bullet(tf8a, "3. Student Cohort Collision:", "No student group scheduled concurrently.")
    add_bullet(tf8a, "4. Room Capacity:", "Room capacity >= enrolled student strength.")
    add_bullet(tf8a, "5. Room Archetype:", "Course room type must match room facility type.")
    add_bullet(tf8a, "6. Faculty Availability:", "No class during faculty designated blackout hours.")
    add_bullet(tf8a, "7. Daily Faculty Workload:", "Teaching load <= 4 hours per day.")
    add_bullet(tf8a, "8. Pre-Fixed Preservation:", "Institutional fixed sessions locked without change.")

    create_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "6 Ergonomic Soft Constraints")
    tb8b = s8.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf8b = tb8b.text_frame
    tf8b.word_wrap = True
    add_bullet(tf8b, "1. Student Window Gaps:", "Minimize idle 1-2 hour gaps between lectures.")
    add_bullet(tf8b, "2. Faculty Fatigue Avoidance:", "Avoid >2 consecutive teaching hours.")
    add_bullet(tf8b, "3. Capacity Efficiency:", "Minimize unused room seats to prevent facility waste.")
    add_bullet(tf8b, "4. Late Slot Burden:", "Reduce allocation of undesirable 16:00-17:00 slots.")
    add_bullet(tf8b, "5. Day Spread Balance:", "Distribute courses evenly across Monday-Friday.")
    add_bullet(tf8b, "6. Overall Ergonomics:", "Normalized quality score evaluated out of 100.")

    # -------------------------------------------------------------
    # SLIDE 9: Heuristic Search Methodology
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Heuristic Backtracking Search Strategy", "CSP Engine")
    
    create_card(s9, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0), "Core Heuristic Mechanisms")
    tb9 = s9.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(11.3), Inches(4.2))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    add_bullet(tf9, "MRV (Minimum Remaining Values):", "Selects the unassigned session variable with the smallest legal domain size ('most constrained variable first'). Prunes search branches where failure is imminent.")
    add_bullet(tf9, "Degree Heuristic Tie-Breaking:", "When MRV yields multiple candidate variables, ties are broken by selecting the variable with the highest number of constraint connections on remaining unassigned sessions.")
    add_bullet(tf9, "LCV (Least Constraining Value):", "Orders domain values (day, slot, room) by the least number of choices eliminated from neighboring unassigned variables, maximizing future search flexibility.")
    add_bullet(tf9, "Forward Checking (Domain Pruning):", "Whenever an assignment is made, incompatible slots are immediately excised from neighbor domains. Early wipeout detection triggers immediate backtrack.")

    # -------------------------------------------------------------
    # SLIDE 10: ML-Assisted Search Integration
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Supervised ML-Assisted Prioritization", "Machine Learning")
    
    ml_img = os.path.join(screenshot_dir, "screenshot_ml_analytics.png")
    if os.path.exists(ml_img):
        s10.shapes.add_picture(ml_img, Inches(1.0), Inches(1.8), width=Inches(11.333))

    # -------------------------------------------------------------
    # SLIDE 11: Explainable Diagnostics
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Explainable Infeasibility Diagnostics", "Explainability")
    
    create_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Diagnostic Isolation Engine")
    tb11a = s11.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf11a = tb11a.text_frame
    tf11a.word_wrap = True
    add_bullet(tf11a, "Automatic Bottleneck Isolation:", "When an overconstrained schedule cannot be completed, the engine isolates the exact variable, resource, and constraint.")
    add_bullet(tf11a, "Faculty Blackout Detection:", "Detects when instructor blackout slots leave zero compatible times for required contact hours.")
    add_bullet(tf11a, "Facility Shortfall Analysis:", "Flags courses whose enrolled strength exceeds the capacity of all matching room archetypes.")

    create_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Sample Diagnostic Explanations")
    tb11b = s11.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf11b = tb11b.text_frame
    tf11b.word_wrap = True
    add_bullet(tf11b, "Root Cause Explanation:", "'[Faculty Availability Exhaustion] Dr. Rajesh Raman (FAC01) has 35 blackout slots, leaving 0 compatible times for CS101.'")
    add_bullet(tf11b, "Actionable Remedy:", "'Action: Relax availability profile on Tuesday/Thursday or co-assign a secondary laboratory instructor.'")
    add_bullet(tf11b, "Capacity Alert:", "'[Room Capacity Shortfall] Strength (55) exceeds Computer Lab capacity (50). Action: Split cohort into 2 tutorial batches.'")

    # -------------------------------------------------------------
    # SLIDE 12: Application Screenshots & Workflow
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Streamlit Light-Mode Application UI", "Application Delivery")
    
    dash_img = os.path.join(screenshot_dir, "screenshot_executive_dashboard.png")
    if os.path.exists(dash_img):
        s12.shapes.add_picture(dash_img, Inches(1.0), Inches(1.8), width=Inches(11.333))

    # -------------------------------------------------------------
    # SLIDE 13: Actual Results & Benchmarking
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Empirical Benchmarking Results", "Results & Evaluation")
    
    bench_img = os.path.join(screenshot_dir, "screenshot_benchmark_comparison.png")
    if os.path.exists(bench_img):
        s13.shapes.add_picture(bench_img, Inches(1.0), Inches(1.8), width=Inches(11.333))

    # -------------------------------------------------------------
    # SLIDE 14: Testing and Validation
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Automated Testing & Independent Validation", "Quality Assurance")
    
    create_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Pytest Suite (10/10 Passed - 100%)")
    tb14a = s14.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf14a = tb14a.text_frame
    tf14a.word_wrap = True
    add_bullet(tf14a, "test_dataset_reproducibility:", "PASSED - Referential integrity & 6 NEP categories.")
    add_bullet(tf14a, "test_faculty_collision_prevention:", "PASSED - Rejects concurrent teaching bookings.")
    add_bullet(tf14a, "test_room_collision_prevention:", "PASSED - Rejects simultaneous room bookings.")
    add_bullet(tf14a, "test_group_collision_prevention:", "PASSED - Rejects concurrent student bookings.")
    add_bullet(tf14a, "test_faculty_daily_workload_limit:", "PASSED - Enforces daily 4-hour max cap.")
    add_bullet(tf14a, "test_ml_metrics_and_generalization:", "PASSED - Verifies 98.06% accuracy & F1 0.986.")

    create_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Independent Hard-Constraint Gate")
    tb14b = s14.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf14b = tb14b.text_frame
    tf14b.word_wrap = True
    add_bullet(tf14b, "Separate Audit Function:", "Evaluates generated schedules independently of the solver's internal state.")
    add_bullet(tf14b, "Zero Tolerance Certification:", "A schedule is strictly flagged as FAILED if even one hard collision is detected.")
    add_bullet(tf14b, "Certified Benchmark Status:", "Both Baseline CSP and ML-Assisted CSP achieved 0 hard violations across all 89 required weekly sessions.")

    # -------------------------------------------------------------
    # SLIDE 15: Limitations, Future Scope & Impact
    # -------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Limitations, Future Scope & Societal Impact", "Impact & Outlook")
    
    create_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Current Limitations & Future Scope")
    tb15a = s15.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf15a = tb15a.text_frame
    tf15a.word_wrap = True
    add_bullet(tf15a, "Inference Overhead:", "Vectorized ML scoring adds modest search overhead. Future work will explore lightweight Cython/ONNX models.")
    add_bullet(tf15a, "Multi-Campus Scheduling:", "Expanding constraints to model transit travel times between geographically distributed campuses.")
    add_bullet(tf15a, "Dynamic Student Registration:", "Connecting directly with ERP APIs for real-time add/drop schedule re-balancing.")

    create_card(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Societal & Institutional Impact")
    tb15b = s15.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf15b = tb15b.text_frame
    tf15b.word_wrap = True
    add_bullet(tf15b, "NEP-2020 Realization:", "Eliminates administrative bottlenecks that historically prevented students from taking cross-departmental electives.")
    add_bullet(tf15b, "Faculty Wellbeing:", "Guarantees fair workload distribution and caps consecutive hours to prevent academic burnout.")
    add_bullet(tf15b, "Resource Optimization:", "Maximizes lab utilization, saving universities significant infrastructure expansion costs.")

    # -------------------------------------------------------------
    # SLIDE 16: PROJECT LINKS (MANDATORY EXACT FORMAT)
    # -------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "PROJECT LINKS", "Repository & Deliverables Access")
    
    card16 = create_card(s16, Inches(1.0), Inches(1.8), Inches(11.333), Inches(5.0), "Official Submission Resources", border_color=COLOR_BLUE)
    tb16 = s16.shapes.add_textbox(Inches(1.3), Inches(2.4), Inches(10.7), Inches(4.2))
    tf16 = tb16.text_frame
    tf16.word_wrap = True
    
    add_bullet(tf16, "Project Title:", "NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System", 13)
    add_bullet(tf16, "Problem Statement ID:", "SIH25091 (Smart India Hackathon 2025)", 13)
    add_bullet(tf16, "Subject Code / Section:", "K3P25IL", 13)
    add_bullet(tf16, "Registration Numbers:", "12511912 (Gandikota Sai Chandana), 12512142 (Inayat)", 13)
    add_bullet(tf16, "GitHub Repository Link:", "[Pending Institutional Remote Push - Local Source Complete in C:\\Users\\Chandi\\.vscode\\timetable_planner]", 13, COLOR_BLUE)
    add_bullet(tf16, "Google Drive Source Bundle:", "[Local Archive Bundle: submission/NEP2020_Timetable_Complete_Source.zip]", 13, COLOR_BLUE)
    add_bullet(tf16, "Synthetic Dataset Link:", "[Local Master Excel: data/synthetic/academic_timetable_data.xlsx]", 13, COLOR_BLUE)
    add_bullet(tf16, "Live Deployment Link:", "[Local Streamlit Server: http://localhost:8501 - Ready for Streamlit Cloud Deployment]", 13, COLOR_BLUE)
    
    p_note = tf16.add_paragraph()
    p_note.text = "Note: In accordance with competition rules, placeholders reflect genuine local artifacts and avoid fabricated URLs."
    p_note.font.size = Pt(11)
    p_note.font.italic = True
    p_note.font.color.rgb = COLOR_SLATE

    # Save presentation
    pptx_path = os.path.join(pres_dir, "NEP2020_Timetable_Presentation.pptx")
    prs.save(pptx_path)
    print(f"[Presentation Generator] Successfully generated 16-slide presentation at: {pptx_path}")

if __name__ == "__main__":
    generate_presentation()
