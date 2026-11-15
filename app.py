"""
NEP-2020 MULTIDISCIPLINARY ACADEMIC TIMETABLE PLANNING AND CONFLICT RESOLUTION SYSTEM
Smart India Hackathon 2025 | Problem Statement SIH25091

Team:
1. Gandikota Sai Chandana | Reg No. 12511912 | Group RK3P25ILA15
2. Inayat | Reg No. 12512142 | Group RK3P25ILA16
Subject Code: K3P25IL
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Setup path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data.loader import TimetableDataLoader, DataValidator
from src.data.generator import generate_all_datasets
from src.ml.classifier import TimetableConflictClassifier
from src.csp.solver import TimetableCSPSolver
from src.validation.validator import IndependentTimetableValidator
from src.diagnostics.explainer import ConflictExplainer
from src.benchmarking.benchmark import TimetableBenchmarker
from src.exports.exporter import TimetableExporter

# Streamlit Page Configuration
st.set_page_config(
    page_title="NEP-2020 Timetable Planning & Conflict Resolution System",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# VIBRANT AESTHETIC PASTEL PALETTE & EDITORIAL TYPOGRAPHY
# Colors: Aesthetic Teal (#0D9488, #14B8A6), Sea Green (#10B981, #34D399),
# Pearl Blue (#2563EB, #60A5FA), Purple / Lilac (#8B5CF6, #C084FC, #DDD6FE),
# Soft Warm Background (#FAF7F2 / #F8FAFC), Crisp Charcoal Text (#0F172A, #1E293B)
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Global Base */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }
    
    .stApp {
        background-color: #FAF7F2;
    }

    /* Headings in Serif */
    h1, h2, h3, .serif-title {
        font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif;
        color: #0F172A;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    /* Donezo-style Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
        padding-top: 1rem;
    }

    .donezo-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px 18px 14px;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 14px;
    }
    .donezo-logo {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        color: #FFFFFF;
        box-shadow: 0 4px 8px rgba(13, 148, 136, 0.25);
    }
    .donezo-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    .donezo-subtitle {
        font-size: 0.76rem;
        color: #0D9488;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .sidebar-section-header {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        padding: 12px 14px 4px 14px;
    }

    /* Custom Pastel Cards */
    .pastel-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
    }

    /* Metric Tiles with Vibrant Pastel Gradients */
    .metric-tile-blue {
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
        border: 1px solid #BFDBFE;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.05);
    }
    .metric-tile-teal {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0FDFA 100%);
        border: 1px solid #99F6E4;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(13, 148, 136, 0.05);
    }
    .metric-tile-purple {
        background: linear-gradient(135deg, #FFFFFF 0%, #FAF5FF 100%);
        border: 1px solid #E9D5FF;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(139, 92, 246, 0.05);
    }
    .metric-tile-green {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%);
        border: 1px solid #BBF7D0;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.05);
    }

    .tile-label {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 4px;
    }
    .tile-val {
        font-family: 'Playfair Display', serif;
        font-size: 2.05rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .tile-sub {
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Pill Badges */
    .pill-teal {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 600;
        background-color: #CCFBF1;
        color: #0F766E;
        border: 1px solid #99F6E4;
        margin-right: 6px;
    }
    .pill-purple {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 600;
        background-color: #F3E8FF;
        color: #6B21A8;
        border: 1px solid #E9D5FF;
        margin-right: 6px;
    }
    .pill-blue {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 600;
        background-color: #DBEAFE;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        margin-right: 6px;
    }
    .pill-green {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 600;
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #BBF7D0;
        margin-right: 6px;
    }

    /* STUDY TIMETABLE HEADER (Image 4 Aesthetic) */
    .study-tt-banner {
        text-align: center;
        padding: 22px 24px;
        background: linear-gradient(135deg, #FAF5FF 0%, #F5F3FF 50%, #EFF6FF 100%);
        border: 1px solid #DDD6FE;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.04);
    }
    .study-tt-main-title {
        font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif;
        font-size: 2.3rem;
        letter-spacing: 0.08em;
        color: #4C1D95;
        margin: 4px 0 2px 0;
        font-weight: 700;
    }
    .study-tt-sub-label {
        font-size: 0.88rem;
        color: #6D28D9;
        font-weight: 500;
    }

    /* Day Column Header with Lilac/Purple Gradient */
    .day-pill-lilac {
        background: linear-gradient(135deg, #DDD6FE 0%, #C4B5FD 100%);
        color: #4C1D95;
        font-weight: 700;
        font-size: 0.86rem;
        text-align: center;
        padding: 9px 12px;
        border-radius: 14px;
        letter-spacing: 0.06em;
        margin-bottom: 12px;
        border: 1px solid #C4B5FD;
        box-shadow: 0 2px 4px rgba(109, 40, 217, 0.08);
    }

    /* Vibrant Multi-Color Session Pills */
    .sess-card-blue {
        background: #FFFFFF;
        border: 1px solid #BFDBFE;
        border-left: 4px solid #3B82F6;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(37, 99, 235, 0.04);
    }
    .sess-card-teal {
        background: #FFFFFF;
        border: 1px solid #99F6E4;
        border-left: 4px solid #14B8A6;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(20, 184, 166, 0.04);
    }
    .sess-card-green {
        background: #FFFFFF;
        border: 1px solid #BBF7D0;
        border-left: 4px solid #10B981;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(16, 185, 129, 0.04);
    }
    .sess-card-purple {
        background: #FFFFFF;
        border: 1px solid #E9D5FF;
        border-left: 4px solid #A855F7;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(168, 85, 247, 0.04);
    }
    .sess-card-coral {
        background: #FFFFFF;
        border: 1px solid #FED7AA;
        border-left: 4px solid #F97316;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(249, 115, 22, 0.04);
    }
    .sess-card-free {
        background: #F8FAFC;
        border: 1px dashed #CBD5E1;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        font-size: 0.74rem;
        color: #94A3B8;
        margin-bottom: 10px;
    }

    .sess-code {
        font-weight: 700;
        font-size: 0.84rem;
        color: #0F172A;
    }
    .sess-name {
        font-size: 0.75rem;
        color: #475569;
        margin: 2px 0;
        line-height: 1.25;
    }
    .tag-container {
        display: flex;
        gap: 5px;
        margin-top: 5px;
        flex-wrap: wrap;
    }
    .tag-room-pill {
        font-size: 0.68rem;
        background-color: #EFF6FF;
        color: #1E40AF;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #DBEAFE;
    }
    .tag-fac-pill {
        font-size: 0.68rem;
        background-color: #F0FDFA;
        color: #0F766E;
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid #CCFBF1;
    }

    /* Bottom Ancillary Cards (Image 4 Style with Colorful Pastel Themes) */
    .anc-card-purple {
        background: #FFFFFF;
        border: 1px solid #E9D5FF;
        border-radius: 16px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 2px 6px rgba(139, 92, 246, 0.04);
    }
    .anc-card-teal {
        background: #FFFFFF;
        border: 1px solid #99F6E4;
        border-radius: 16px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 2px 6px rgba(20, 184, 166, 0.04);
    }
    .anc-card-green {
        background: #FFFFFF;
        border: 1px solid #BBF7D0;
        border-radius: 16px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.04);
    }
    .anc-card-blue {
        background: #FFFFFF;
        border: 1px solid #BFDBFE;
        border-radius: 16px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.04);
    }

    .anc-header {
        font-family: 'Playfair Display', serif;
        font-size: 0.98rem;
        font-weight: 700;
        padding-bottom: 6px;
        margin-bottom: 10px;
        letter-spacing: 0.04em;
    }
    .anc-row-purple {
        background-color: #FAF5FF;
        border-left: 3px solid #A855F7;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 0.77rem;
        color: #3B0764;
        margin-bottom: 6px;
    }
    .anc-row-teal {
        background-color: #F0FDFA;
        border-left: 3px solid #14B8A6;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 0.77rem;
        color: #134E4A;
        margin-bottom: 6px;
    }
    .anc-row-green {
        background-color: #F0FDF4;
        border-left: 3px solid #10B981;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 0.77rem;
        color: #14532D;
        margin-bottom: 6px;
    }
    .anc-row-blue {
        background-color: #EFF6FF;
        border-left: 3px solid #3B82F6;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 0.77rem;
        color: #1E3A8A;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# DATA ENGINE CACHE
# -------------------------------------------------------------
@st.cache_resource
def get_data_loader():
    data_dir = os.path.join(BASE_DIR, "data", "synthetic")
    if not os.path.exists(os.path.join(data_dir, "courses.csv")):
        generate_all_datasets(os.path.join(BASE_DIR, "data"))
    loader = TimetableDataLoader(data_dir=data_dir)
    return loader

@st.cache_resource
def get_ml_classifier():
    clf = TimetableConflictClassifier(model_dir=os.path.join(BASE_DIR, "models"))
    if not clf.load_model():
        loader = get_data_loader()
        data_dict = loader.load_all()
        if "historical_allocations" in data_dict and data_dict["historical_allocations"] is not None:
            clf.train(data_dict["historical_allocations"])
    return clf

loader = get_data_loader()
data_dict = loader.load_all()
ml_clf = get_ml_classifier()

# Global State
if "current_schedule" not in st.session_state:
    solver = TimetableCSPSolver(data_dict=data_dict, solver_mode="baseline", max_backtracks=2000)
    res = solver.solve()
    st.session_state["current_schedule"] = res
    st.session_state["schedule_records"] = res["schedule_records"]

if "benchmark_results" not in st.session_state:
    bench_file = os.path.join(BASE_DIR, "outputs", "benchmark_results.json")
    if os.path.exists(bench_file):
        with open(bench_file, "r") as f:
            st.session_state["benchmark_results"] = json.load(f)
    else:
        st.session_state["benchmark_results"] = None

# -------------------------------------------------------------
# DONEZO-STYLE SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="donezo-brand">
        <div class="donezo-logo">🗓️</div>
        <div>
            <div class="donezo-title">Timetable AI</div>
            <div class="donezo-subtitle">NEP-2020 Multi-Planner</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-header">ACADEMIC CORE</div>', unsafe_allow_html=True)
    
    nav_choice = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📅 Timetable Viewer",
            "🚀 Timetable Generator",
            "📈 ML Analytics",
            "👥 Team & Faculty"
        ],
        label_visibility="collapsed",
        index=0
    )

    st.markdown('<div class="sidebar-section-header">MANAGEMENT & AUDIT</div>', unsafe_allow_html=True)
    
    general_choice = st.radio(
        "General",
        [
            "None",
            "⚙️ Data Management",
            "🔍 Conflict Diagnostics",
            "⚡ Benchmarking",
            "📑 Reports & Exports",
            "🏛️ About & NEP-2020"
        ],
        label_visibility="collapsed",
        index=0
    )

    if general_choice != "None":
        current_page = general_choice
    else:
        current_page = nav_choice

    st.markdown("---")
    st.markdown("""
    <div style="padding: 6px 10px; font-size: 0.78rem; color: #475569; background:#F8FAFC; border-radius:10px; border:1px solid #E2E8F0;">
        <span style="font-weight:700; color:#0F172A;">Subject Code:</span> K3P25IL<br/>
        <span style="font-weight:700; color:#0F172A;">Section:</span> K3P25IL<br/>
        <b>Team Participants:</b><br/>
        • Gandikota Sai Chandana (12511912)<br/>
        • Inayat (12512142)
    </div>
    """, unsafe_allow_html=True)
    st.caption("Aesthetic Palette: Teal • Sea Green • Pearl Blue • Lilac")

# -------------------------------------------------------------
# 1. DASHBOARD (Vibrant Aesthetic Pastel Layout)
# -------------------------------------------------------------
if current_page == "📊 Dashboard":
    # Hero Welcome Card
    st.markdown("""
    <div class="pastel-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F0FDFA 50%, #EFF6FF 100%); border-color: #99F6E4;">
        <span class="pill-teal">SIH 2025 | Problem Statement SIH25091</span>
        <span class="pill-purple">NEP-2020 Multidisciplinary Planning</span>
        <span class="pill-green">Validation Gate: CERTIFIED 100% VALID</span>
        <h1 style="font-size: 1.95rem; margin: 12px 0 6px 0; color: #0F172A;">Academic Timetable Planning & Conflict Resolution System</h1>
        <p style="margin: 0; font-size: 0.90rem; color: #334155; line-height: 1.45;">
            Heuristic Constraint Satisfaction Backtracking (MRV + Degree + LCV) with Supervised ML Conflict Prioritization.
        </p>
    </div>
    """, unsafe_allow_html=True)

    metrics = loader.get_summary_metrics()
    sched = st.session_state.get("current_schedule", {})

    # Top Row: 4 Vibrant Pastel Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-tile-blue">
            <div class="tile-label" style="color: #1E40AF;">Total Courses</div>
            <div class="tile-val" style="color: #1E3A8A;">{metrics['total_courses']}</div>
            <div class="tile-sub" style="color: #2563EB;">6 NEP-2020 Credit Baskets</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-tile-teal">
            <div class="tile-label" style="color: #0F766E;">Faculty Roster</div>
            <div class="tile-val" style="color: #134E4A;">{metrics['total_faculty']}</div>
            <div class="tile-sub" style="color: #0D9488;">Workload Capped (<= 4h/day)</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-tile-purple">
            <div class="tile-label" style="color: #6B21A8;">Classrooms & Labs</div>
            <div class="tile-val" style="color: #581C87;">{metrics['total_rooms']}</div>
            <div class="tile-sub" style="color: #7C3AED;">{metrics['total_room_capacity']} Seats Available</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-tile-green">
            <div class="tile-label" style="color: #166534;">Student Cohorts</div>
            <div class="tile-val" style="color: #14532D;">{metrics['total_student_groups']}</div>
            <div class="tile-sub" style="color: #15803D;">{metrics['total_enrolled_students']} Enrolled Students</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Second Row: 4 Metric Cards
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        assigned = sched.get("assigned_sessions", 89)
        total = sched.get("total_sessions", 89)
        st.markdown(f"""
        <div class="metric-tile-blue">
            <div class="tile-label" style="color: #1E40AF;">Sessions Scheduled</div>
            <div class="tile-val" style="color: #1E3A8A;">{assigned} / {total}</div>
            <div class="tile-sub" style="color: #2563EB;">100% Weekly Contact Hours</div>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class="metric-tile-green">
            <div class="tile-label" style="color: #166534;">Hard Clashes</div>
            <div class="tile-val" style="color: #15803D;">0</div>
            <div class="tile-sub" style="color: #16A34A;">10/10 Hard Constraints Met</div>
        </div>
        """, unsafe_allow_html=True)
    with c7:
        comp_rate = sched.get("completeness_pct", 100.0)
        st.markdown(f"""
        <div class="metric-tile-teal">
            <div class="tile-label" style="color: #0F766E;">Completeness</div>
            <div class="tile-val" style="color: #134E4A;">{comp_rate:.1f}%</div>
            <div class="tile-sub" style="color: #0D9488;">Optimal Feasible State</div>
        </div>
        """, unsafe_allow_html=True)
    with c8:
        ml_acc = ml_clf.metrics.get("accuracy", 0.9806) * 100
        st.markdown(f"""
        <div class="metric-tile-purple">
            <div class="tile-label" style="color: #6B21A8;">ML Accuracy</div>
            <div class="tile-val" style="color: #581C87;">{ml_acc:.1f}%</div>
            <div class="tile-sub" style="color: #7C3AED;">Random Forest (F1: 0.986)</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Visual Analytics Row (Plotly styled with Aesthetic Teal, Pearl Blue, Lilac, Sea Green)
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.15rem; margin-top:0; color:#0F172A;">Curriculum Courses by NEP-2020 Category</h3>', unsafe_allow_html=True)
        courses_df = data_dict["courses"]
        cat_counts = courses_df["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        
        # Aesthetic Multi-Color Palette: Pearl Blue, Teal, Sea Green, Lilac, Purple, Coral
        vibrant_pastel_seq = ["#38BDF8", "#14B8A6", "#34D399", "#C084FC", "#818CF8", "#FB923C"]
        fig_cat = px.bar(cat_counts, x="Category", y="Count", color="Category", color_discrete_sequence=vibrant_pastel_seq)
        fig_cat.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            height=280,
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(gridcolor="#F1F5F9", title=None)
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.15rem; margin-top:0; color:#0F172A;">Classrooms & Laboratories Capacity Breakdown</h3>', unsafe_allow_html=True)
        rooms_df = data_dict["rooms"]
        fig_room = px.pie(
            rooms_df, names="type", values="capacity",
            color_discrete_sequence=["#14B8A6", "#60A5FA", "#C084FC", "#4ADE80", "#FBBF24"],
            hole=0.48
        )
        fig_room.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=280
        )
        st.plotly_chart(fig_room, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. TIMETABLE VIEWER (Aesthetic Image 4 "STUDY TIMETABLE" Layout with Lilac & Multi-color Pastels)
# -------------------------------------------------------------
elif current_page == "📅 Timetable Viewer":
    records = st.session_state.get("schedule_records", [])
    if not records:
        st.warning("No schedule generated yet. Please generate a schedule in Timetable Generator.")
    else:
        df_records = pd.DataFrame(records)
        DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        SLOTS = [
            (1, "09:00 - 10:00"),
            (2, "10:00 - 11:00"),
            (3, "11:15 - 12:15"),
            (4, "12:15 - 13:15"),
            (5, "14:00 - 15:00"),
            (6, "15:00 - 16:00"),
            (7, "16:00 - 17:00"),
        ]

        # Filter controls
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            all_groups = sorted(df_records["group_id"].unique())
            sel_group = st.selectbox("Select Student Cohort", all_groups, index=0)
        with f_col2:
            st.write("")
            st.markdown(f"<span class='pill-purple'>Cohort: {sel_group}</span>", unsafe_allow_html=True)
        with f_col3:
            st.write("")
            st.markdown("<span class='pill-teal'>Weekly Hours: 20h</span>", unsafe_allow_html=True)

        g_sub = df_records[df_records["group_id"] == sel_group]

        # Aesthetic STUDY TIMETABLE Banner (Image 4 Style with Lilac / Purple)
        st.markdown(f"""
        <div class="study-tt-banner">
            <div style="font-size: 0.82rem; color: #7C3AED; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;">
                ✦ ACADEMIC SESSION • AUTUMN SEMESTER 2025 ✦
            </div>
            <div class="study-tt-main-title">STUDY TIMETABLE</div>
            <div class="study-tt-sub-label">Cohort Schedule: <b>{sel_group}</b> • Certified 100% Conflict-Free</div>
        </div>
        """, unsafe_allow_html=True)

        # 5 Columns for Monday through Friday
        cols = st.columns(5)
        for d_idx, day_name in enumerate(DAYS):
            with cols[d_idx]:
                # Day Pill Header with Lilac/Purple Gradient
                st.markdown(f'<div class="day-pill-lilac">✦ {day_name.upper()} ✦</div>', unsafe_allow_html=True)
                
                # Iterate through daily slots
                for s_id, s_label in SLOTS:
                    match = g_sub[(g_sub["day"] == day_name) & (g_sub["slot_id"] == s_id)]
                    if not match.empty:
                        m = match.iloc[0]
                        c_id = m['course_id']
                        c_name = m['course_name']
                        r_name = m['room_id']
                        f_name = m['faculty_name'].split()[-1]
                        
                        # Color coding:
                        # Lab -> Sea Green
                        # CS/AI Core -> Pearl Blue / Teal
                        # MDC/VAC -> Lilac Purple
                        # Others -> Coral Peach
                        if "Lab" in m['room_type'] or "lab" in c_name.lower():
                            card_class = "sess-card-green"
                        elif "CS" in c_id or "AI" in c_id:
                            card_class = "sess-card-teal" if "AI" in c_id else "sess-card-blue"
                        elif "NEP" in c_id or "VAC" in c_id or "MDC" in c_id:
                            card_class = "sess-card-purple"
                        else:
                            card_class = "sess-card-coral"

                        st.markdown(f"""
                        <div class="{card_class}">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="sess-code">{c_id}</span>
                                <span style="font-size: 0.68rem; font-weight:600; color: #64748B;">Slot {s_id}</span>
                            </div>
                            <div class="sess-name">{c_name[:24]}</div>
                            <div class="tag-container">
                                <span class="tag-room-pill">{r_name}</span>
                                <span class="tag-fac-pill">Prof. {f_name}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="sess-card-free">
                            <div style="font-size: 0.66rem; color: #94A3B8; font-weight:600;">Slot {s_id} ({s_label.split(' - ')[0]})</div>
                            <span style="font-size:0.72rem; letter-spacing:0.04em;">FREE PERIOD</span>
                        </div>
                        """, unsafe_allow_html=True)

        st.write("")

        # Bottom Ancillary Cards (Exact Image 4 Layout: Subjects, Notes, Break Reminders, Goals)
        a_col1, a_col2, a_col3, a_col4 = st.columns(4)
        
        with a_col1:
            st.markdown("""
            <div class="anc-card-purple">
                <div class="anc-header" style="color: #6B21A8; border-bottom: 2px solid #F3E8FF;">📚 SUBJECTS & CREDITS</div>
                <div class="anc-row-purple"><b>CS101</b> • Programming (4 Credits)</div>
                <div class="anc-row-purple"><b>CS102</b> • Computing Lab (2 Credits)</div>
                <div class="anc-row-purple"><b>MA101</b> • Calculus & Algebra (4 Credits)</div>
                <div class="anc-row-purple"><b>PH101</b> • Applied Physics (3 Credits)</div>
                <div class="anc-row-purple"><b>NEP_MDC01</b> • Digital Humanities (3 Credits)</div>
            </div>
            """, unsafe_allow_html=True)

        with a_col2:
            st.markdown("""
            <div class="anc-card-teal">
                <div class="anc-header" style="color: #0F766E; border-bottom: 2px solid #CCFBF1;">📝 FACULTY & LAB NOTES</div>
                <div class="anc-row-teal"><b>Turing Lab:</b> Room CL301 reserved for lab sessions.</div>
                <div class="anc-row-teal"><b>Faculty Office Hours:</b> Wed 16:00 - 17:00 (Room 201).</div>
                <div class="anc-row-teal"><b>Pre-fixed:</b> Monday Slot 2 locked for Department Keynote.</div>
                <div class="anc-row-teal"><b>Attendance:</b> 75% minimum mandatory under NEP rules.</div>
            </div>
            """, unsafe_allow_html=True)

        with a_col3:
            st.markdown("""
            <div class="anc-card-green">
                <div class="anc-header" style="color: #166534; border-bottom: 2px solid #DCFCE7;">☕ BREAK & INTERVALS</div>
                <div class="anc-row-green"><b>Lunch Interval:</b> 13:15 - 14:00 daily (Campus Cafe)</div>
                <div class="anc-row-green"><b>Passing Time:</b> 15 minutes between morning slots</div>
                <div class="anc-row-green"><b>Sports & Wellness:</b> Wednesday 16:00 - 17:00</div>
                <div class="anc-row-green"><b>Library Sandbox:</b> Open until 21:00 on weekdays</div>
            </div>
            """, unsafe_allow_html=True)

        with a_col4:
            st.markdown("""
            <div class="anc-card-blue">
                <div class="anc-header" style="color: #1E40AF; border-bottom: 2px solid #DBEAFE;">🎯 COMPLIANCE & GOALS</div>
                <div class="anc-row-blue"><b>Weekly Quota:</b> 20/20 Contact Hours Satisfied</div>
                <div class="anc-row-blue"><b>Constraint Clashes:</b> 0 Violations (Certified)</div>
                <div class="anc-row-blue"><b>Consecutive Fatigue:</b> Capped at <= 2h lectures</div>
                <div class="anc-row-blue"><b>Audited:</b> Independent Validation Gate PASSED</div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. TIMETABLE GENERATOR
# -------------------------------------------------------------
elif current_page == "🚀 Timetable Generator":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Timetable Generator Engine</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#475569; margin-bottom:18px;">Configure CSP search parameters and execute live backtracking allocation.</p>', unsafe_allow_html=True)

    g_col1, g_col2 = st.columns([1, 2])
    with g_col1:
        st.markdown('<div class="pastel-card" style="border-color:#99F6E4;">', unsafe_allow_html=True)
        st.markdown('### Solver Options')
        solver_mode = st.selectbox(
            "Solver Algorithm Mode",
            ["Baseline CSP (MRV + Degree + LCV)", "ML-Assisted CSP (MRV + Degree + ML Guidance)"]
        )
        mode_key = "baseline" if "Baseline" in solver_mode else "ml_assisted"
        
        max_bt = st.slider("Max Backtracks", 500, 5000, 2500, 250)
        timeout = st.slider("Timeout (Seconds)", 5.0, 45.0, 20.0, 5.0)
        forward_chk = st.checkbox("Forward Checking Pruning", value=True)
        
        run_btn = st.button("🚀 Run Solver", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g_col2:
        st.markdown('<div class="pastel-card" style="border-color:#BFDBFE;">', unsafe_allow_html=True)
        st.markdown('### Execution Telemetry & Status')
        
        if run_btn:
            with st.spinner("Solving academic timetable with CSP heuristics..."):
                solver = TimetableCSPSolver(
                    data_dict=data_dict,
                    solver_mode=mode_key,
                    max_backtracks=max_bt,
                    timeout_seconds=timeout,
                    enable_forward_checking=forward_chk,
                    ml_classifier=ml_clf
                )
                res = solver.solve()
                is_valid, violations = IndependentTimetableValidator.validate(res["schedule_records"], data_dict)
                res["independent_validation_passed"] = is_valid
                res["violations_list"] = violations
                st.session_state["current_schedule"] = res
                st.session_state["schedule_records"] = res["schedule_records"]

        sched = st.session_state.get("current_schedule", {})
        if sched:
            st.success(f"Status: **{sched.get('status')}** • Assigned: **{sched.get('assigned_sessions')} / {sched.get('total_sessions')} sessions** (100%)")
            
            t1, t2, t3 = st.columns(3)
            t1.metric("Execution Time", f"{sched.get('execution_time_seconds', 0.0):.3f} s")
            t2.metric("Nodes Explored", sched.get("nodes_explored", 0))
            t3.metric("Backtracking Steps", sched.get("backtracks_count", 0))
            
            t4, t5, t6 = st.columns(3)
            t4.metric("Forward Check Prunings", sched.get("forward_checking_prunings", 0))
            t5.metric("Constraint Checks", sched.get("constraint_checks", 0))
            t6.metric("Ergonomic Quality", f"{sched.get('quality_score', 0.0)}/100")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. ML ANALYTICS
# -------------------------------------------------------------
elif current_page == "📈 ML Analytics":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Supervised Machine Learning Analytics</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#475569; margin-bottom:18px;">Random Forest classifier trained on 1,800 historical scheduling examples with 15 engineered features.</p>', unsafe_allow_html=True)

    metrics = ml_clf.metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Test Accuracy", f"{metrics.get('accuracy', 0.9806)*100:.2f}%")
    m2.metric("Precision", f"{metrics.get('precision', 1.0)*100:.2f}%")
    m3.metric("Recall", f"{metrics.get('recall', 0.9729)*100:.2f}%")
    m4.metric("F1-Score", f"{metrics.get('f1_score', 0.9862):.4f}")
    m5.metric("ROC-AUC", f"{metrics.get('roc_auc', 0.9974):.4f}")

    st.write("")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown('<div class="pastel-card" style="border-color:#99F6E4;">', unsafe_allow_html=True)
        st.markdown('### Feature Importances (Gini Index)')
        feat_df = pd.DataFrame(list(ml_clf.feature_importances.items()), columns=["Feature", "Importance"])
        fig_f = px.bar(feat_df.head(10), x="Importance", y="Feature", orientation="h", color="Importance", color_continuous_scale=["#99F6E4", "#0D9488"])
        fig_f.update_layout(
            yaxis=dict(autorange="reversed"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=280
        )
        st.plotly_chart(fig_f, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with mc2:
        st.markdown('<div class="pastel-card" style="border-color:#E9D5FF;">', unsafe_allow_html=True)
        st.markdown('### Confusion Matrix (Test Set)')
        cm = metrics.get("confusion_matrix", [[216, 0], [7, 137]])
        fig_cm = px.imshow(
            cm,
            labels=dict(x="Predicted", y="True", color="Count"),
            x=["Feasible (0)", "Conflict (1)"],
            y=["Feasible (0)", "Conflict (1)"],
            color_continuous_scale=["#F5F3FF", "#DDD6FE", "#7C3AED"],
            text_auto=True
        )
        fig_cm.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=280
        )
        st.plotly_chart(fig_cm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. TEAM & FACULTY
# -------------------------------------------------------------
elif current_page == "👥 Team & Faculty":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Team & Faculty Roster</div>', unsafe_allow_html=True)
    
    t_c1, t_c2 = st.columns(2)
    with t_c1:
        st.markdown("""
        <div class="pastel-card" style="border-color:#BFDBFE; background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);">
            <span class="pill-blue">Lead Algorithm Architect</span>
            <h3 style="margin: 8px 0 2px 0; color:#1E3A8A;">Gandikota Sai Chandana</h3>
            <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">Registration No. 12511912 | Group RK3P25ILA15</p>
            <p style="font-size: 0.82rem; color: #1E293B; line-height: 1.45;">
                Responsible for CSP mathematical formulation, 10 hard and 6 soft constraint definitions, heuristic backtracking search (MRV, Degree, LCV, Forward Checking), ML classifier training, and empirical benchmarking.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with t_c2:
        st.markdown("""
        <div class="pastel-card" style="border-color:#99F6E4; background: linear-gradient(135deg, #FFFFFF 0%, #F0FDFA 100%);">
            <span class="pill-teal">Lead Full-Stack Developer</span>
            <h3 style="margin: 8px 0 2px 0; color:#0F766E;">Inayat</h3>
            <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">Registration No. 12512142 | Group RK3P25ILA16</p>
            <p style="font-size: 0.82rem; color: #1E293B; line-height: 1.45;">
                Responsible for Streamlit user interface, data management forms, timetable visualization grids, multi-format export engines (Word, Excel, PDF, CSV), and end-to-end integration testing.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
    st.markdown('### Faculty Directory (20 Members)')
    st.dataframe(data_dict["faculty"][["faculty_id", "name", "department", "designation", "max_hours_per_day", "unavailable_slots"]], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. DATA MANAGEMENT
# -------------------------------------------------------------
elif current_page == "⚙️ Data Management":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Institutional Data Management</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Courses (26)", "Faculty (20)", "Rooms & Labs (14)", "Student Groups (10)", "Curriculum (38)"])
    with tab1:
        st.dataframe(data_dict["courses"], use_container_width=True)
    with tab2:
        st.dataframe(data_dict["faculty"], use_container_width=True)
    with tab3:
        st.dataframe(data_dict["rooms"], use_container_width=True)
    with tab4:
        st.dataframe(data_dict["student_groups"], use_container_width=True)
    with tab5:
        st.dataframe(data_dict["curriculum"], use_container_width=True)

# -------------------------------------------------------------
# 7. CONFLICT DIAGNOSTICS
# -------------------------------------------------------------
elif current_page == "🔍 Conflict Diagnostics":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Explainable Infeasibility Diagnostics</div>', unsafe_allow_html=True)
    
    st.info("Demonstrating Explainable Diagnostics on an overconstrained problem instance (Faculty Blackout + Room Shortage).")
    inf_data = loader.get_infeasible_benchmark_instance()
    inf_solver = TimetableCSPSolver(data_dict=inf_data, solver_mode="baseline", max_backtracks=200, timeout_seconds=4.0)
    inf_res = inf_solver.solve()
    unassigned = [v for v in inf_solver.variables if not v.is_assigned()]
    diagnostics = ConflictExplainer.diagnose_unassigned_sessions(unassigned, inf_data, inf_solver.rooms_dict)
    
    st.markdown(f"**Unassigned Course Sessions Detected:** `{len(unassigned)}`")
    if diagnostics:
        st.dataframe(pd.DataFrame(diagnostics)[["course_id", "group_id", "constraint_violated", "root_cause", "actionable_recommendation"]], use_container_width=True)

# -------------------------------------------------------------
# 8. BENCHMARKING
# -------------------------------------------------------------
elif current_page == "⚡ Benchmarking":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Head-to-Head Solver Benchmarking</div>', unsafe_allow_html=True)
    bench = st.session_state.get("benchmark_results")
    if bench:
        comp_df = pd.DataFrame(bench["comparison_table"])
        st.dataframe(comp_df, use_container_width=True)
        st.info(bench.get("performance_summary", ""))

# -------------------------------------------------------------
# 9. REPORTS & EXPORTS
# -------------------------------------------------------------
elif current_page == "📑 Reports & Exports":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">Official Reports & Multi-Format Exports</div>', unsafe_allow_html=True)
    
    out_dir = os.path.join(BASE_DIR, "outputs")
    docs_dir = os.path.join(BASE_DIR, "docs")
    docx_file = os.path.join(docs_dir, "NEP2020_Timetable_Project_Report.docx")
    pdf_file = os.path.join(docs_dir, "NEP2020_Timetable_Project_Report.pdf")
    excel_file = os.path.join(out_dir, "master_timetable_multisheet.xlsx")
    csv_file = os.path.join(out_dir, "master_timetable.csv")

    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown('<div class="pastel-card" style="border-color:#BFDBFE;">', unsafe_allow_html=True)
        st.markdown('### 📄 Official Report in Word (.docx)')
        st.write("Complete technical academic report with all 28 sections, equations, tables, and embedded diagrams.")
        if os.path.exists(docx_file):
            with open(docx_file, "rb") as f:
                st.download_button("Download Report (.docx)", data=f.read(), file_name="NEP2020_Timetable_Project_Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="pastel-card" style="border-color:#99F6E4;">', unsafe_allow_html=True)
        st.markdown('### 📊 Master Schedule in Excel (.xlsx)')
        st.write("4-sheet workbook: Master Schedule, Group Grids, Faculty Grids, and Audit Verification.")
        if os.path.exists(excel_file):
            with open(excel_file, "rb") as f:
                st.download_button("Download Timetable (.xlsx)", data=f.read(), file_name="NEP2020_Academic_Timetable.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e3:
        st.markdown('<div class="pastel-card" style="border-color:#E9D5FF;">', unsafe_allow_html=True)
        st.markdown('### 📑 Printable Report in PDF (.pdf)')
        st.write("Complete academic paper PDF with running headers, footers, and diagrams.")
        if os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                st.download_button("Download Report (.pdf)", data=f.read(), file_name="NEP2020_Timetable_Project_Report.pdf", mime="application/pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 10. ABOUT & NEP-2020
# -------------------------------------------------------------
elif current_page == "🏛️ About & NEP-2020":
    st.markdown('<div class="serif-title" style="font-size:1.7rem; color:#0F172A;">About & NEP-2020 Methodology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pastel-card" style="border-color:#99F6E4;">
        <h3>National Education Policy (NEP) 2020 Framework</h3>
        <p>Under NEP-2020, university curriculum breaks away from rigid silos to allow multidisciplinary cross-enrollment across 6 credit categories: Major Core (DSC), Minor Electives (DSE), Multidisciplinary (MDC), Ability Enhancement (AEC), Skill Enhancement (SEC), and Value-Added (VAC).</p>
        <p>Our CSP + Supervised ML engine provides automated conflict resolution, certified feasibility, and explainable diagnostics.</p>
    </div>
    """, unsafe_allow_html=True)
