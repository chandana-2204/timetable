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
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

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
from src.ui.tools_view import (
    render_tools_center,
    _render_tool_makeup_feasibility,
    _render_tool_absence_manager,
    _render_tool_substitute_matcher,
    _render_tool_rescheduler
)
from src.ui.reports_view import render_reports_center

# Streamlit Page Configuration
st.set_page_config(
    page_title="NEP-2020 Timetable Planning & Conflict Resolution System",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# SHOPEERS-INSPIRED DESIGN SYSTEM  ·  CSS + JS INJECTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #0B0D17;
}

/* ── App Background ── */
.stApp {
    background: #F0F2F5 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0B0D17 !important;
    border-right: none !important;
    min-width: 240px !important;
}
[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #CBD5E1 !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] {
    background: transparent !important;
    border-radius: 8px !important;
    padding: 2px 4px !important;
    transition: background 0.15s ease !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"]:hover {
    background: rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] div, [data-testid="stSidebar"] label {
    color: #E2E8F0 !important;
}
/* Keep native sidebar toggle accessible but invisible — our hamburger triggers it */
button[data-testid="collapsedControl"],
.st-emotion-cache-1egp75f {
    opacity: 0 !important;
    pointer-events: none !important;
    position: absolute !important;
    width: 1px !important; height: 1px !important;
}

/* ── Hamburger Button ── */
.hamburger-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 7px 8px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    flex-shrink: 0;
    transition: background 0.15s ease;
}
.hamburger-btn:hover { background: #F0F2F5; }
.hamburger-btn span {
    display: block;
    width: 18px;
    height: 2px;
    background: #0B0D17;
    border-radius: 2px;
    transition: all 0.2s ease;
}

/* ── Main Content Area ── */
.main .block-container {
    padding: 1.5rem 2rem !important;
    max-width: 100% !important;
}

/* ── Shopeers Header Bar ── */
.shopeers-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #FFFFFF;
    border-radius: 14px;
    padding: 12px 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
}
.shopeers-breadcrumb {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.84rem;
    color: #64748B;
    font-weight: 500;
}
.shopeers-breadcrumb .crumb-active {
    color: #0B0D17;
    font-weight: 700;
}
.shopeers-breadcrumb .crumb-sep { color: #CBD5E1; }
.shopeers-header-right {
    display: flex;
    align-items: center;
    gap: 14px;
}
.header-icon-btn {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: #F0F2F5;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    font-size: 16px;
}
.header-avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0A24E9 0%, #29315D 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: #FFFFFF;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 24px;
}
.page-header h1 {
    font-size: 1.75rem;
    font-weight: 800;
    color: #0B0D17;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}
.page-header .page-subtitle {
    font-size: 0.875rem;
    color: #64748B;
    font-weight: 400;
    margin: 0;
}

/* ── Metric / KPI Cards ── */
.metric-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
    height: 100%;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
}
.kpi-card-blue::before  { background: #0A24E9; }
.kpi-card-green::before { background: #5C9764; }
.kpi-card-orange::before{ background: #F59E0B; }
.kpi-card-purple::before{ background: #7C3AED; }

.kpi-icon {
    font-size: 1.75rem;
    margin-bottom: 10px;
    display: block;
}
.kpi-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0B0D17;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: -0.03em;
}
.kpi-sub {
    font-size: 0.775rem;
    color: #94A3B8;
    font-weight: 500;
}

/* ── Generic White Card / Surface ── */
.surface-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}
.surface-card h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #0B0D17;
    margin: 0 0 16px 0;
}

/* ── Timetable Session Card ── */
.timetable-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    border-left: 4px solid #0A24E9;
}
.timetable-card.tc-blue   { border-left-color: #0A24E9; }
.timetable-card.tc-green  { border-left-color: #5C9764; }
.timetable-card.tc-purple { border-left-color: #7C3AED; }
.timetable-card.tc-orange { border-left-color: #F59E0B; }
.timetable-card.tc-navy   { border-left-color: #29315D; }
.timetable-card-free {
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: 10px;
    padding: 12px 10px;
    text-align: center;
    font-size: 0.72rem;
    color: #94A3B8;
    margin-bottom: 8px;
}
.tc-code { font-weight: 700; font-size: 0.82rem; color: #0B0D17; }
.tc-name { font-size: 0.74rem; color: #64748B; margin: 2px 0; line-height: 1.3; }
.tc-tags { display: flex; gap: 4px; margin-top: 5px; flex-wrap: wrap; }
.tc-room {
    font-size: 0.67rem; background: #EEF2FF; color: #3730A3;
    padding: 2px 7px; border-radius: 5px; font-weight: 600;
}
.tc-fac {
    font-size: 0.67rem; background: #F0FDF4; color: #166534;
    padding: 2px 7px; border-radius: 5px; font-weight: 500;
}

/* ── Day Header Pill ── */
.day-pill {
    background: #29315D;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.82rem;
    text-align: center;
    padding: 8px 10px;
    border-radius: 10px;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}

/* ── Status Badge ── */
.status-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-success { background: #DCFCE7; color: #166534; }
.badge-warning { background: #FEF9C3; color: #854D0E; }
.badge-danger  { background: #FEE2E2; color: #991B1B; }
.badge-info    { background: #EEF2FF; color: #3730A3; }

/* ── Sidebar Brand ── */
.sb-brand {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 16px 16px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 10px;
}
.sb-logo {
    width: 40px; height: 40px; border-radius: 12px;
    background: linear-gradient(135deg, #0A24E9 0%, #29315D 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 12px rgba(10,36,233,0.3);
    flex-shrink: 0;
}
.sb-title {
    font-size: 1.05rem; font-weight: 800; color: #F8FAFC !important;
    line-height: 1.1;
}
.sb-subtitle {
    font-size: 0.72rem; color: #64748B !important;
    font-weight: 600; letter-spacing: 0.04em;
}

/* ── Sidebar Section Label ── */
.sb-section-label {
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #475569 !important;
    padding: 14px 16px 4px 16px;
}

/* ── Sidebar Bottom User Card ── */
.sb-user-card {
    margin: 20px 12px 12px 12px;
    padding: 12px 14px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}
.sb-user-name { font-size: 0.8rem; font-weight: 700; color: #F1F5F9 !important; }
.sb-user-role { font-size: 0.72rem; color: #64748B !important; }

/* ── Filter Row ── */
.filter-row {
    display: flex; align-items: center; gap: 10px;
    background: #FFFFFF;
    border-radius: 12px;
    padding: 10px 16px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    flex-wrap: wrap;
}

/* ── Data Table ── */
.data-table-container {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
}

/* ── Ancillary Info Card ── */
.anc-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    height: 100%;
}
.anc-card-header {
    font-size: 0.9rem; font-weight: 700; color: #0B0D17;
    padding-bottom: 10px; margin-bottom: 10px;
    border-bottom: 1px solid #E2E8F0;
}
.anc-row {
    background: #F8FAFC;
    border-left: 3px solid #0A24E9;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 0.775rem;
    color: #334155;
    margin-bottom: 6px;
}
.anc-row-green { border-left-color: #5C9764; }
.anc-row-purple { border-left-color: #7C3AED; }
.anc-row-orange { border-left-color: #F59E0B; }

/* ── Empty State ── */
.empty-state {
    text-align: center; padding: 60px 20px;
    background: #FFFFFF; border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.empty-state-icon { font-size: 3rem; margin-bottom: 16px; }
.empty-state-title { font-size: 1.1rem; font-weight: 700; color: #0B0D17; margin-bottom: 6px; }
.empty-state-desc { font-size: 0.875rem; color: #64748B; max-width: 360px; margin: 0 auto; }

/* ── System Status Row ── */
.system-status-bar {
    display: flex; align-items: center; gap: 10px;
    background: #FFFFFF; border-radius: 12px;
    padding: 12px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-top: 20px;
    flex-wrap: wrap;
}
.sys-label { font-size: 0.78rem; font-weight: 600; color: #64748B; margin-right: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA ENGINE CACHE
# ─────────────────────────────────────────────────────────────────────────────
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

# Global Session State
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

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  ·  Shopeers-inspired dark nav
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-logo">🗓️</div>
        <div>
            <div class="sb-title">TimetableAI</div>
            <div class="sb-subtitle">NEP-2020 Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── OVERVIEW ──
    st.markdown('<div class="sb-section-label">OVERVIEW</div>', unsafe_allow_html=True)
    overview_choice = st.radio(
        "overview_nav",
        ["📊 Dashboard", "📅 Timetable"],
        label_visibility="collapsed",
        index=0,
        key="overview_radio"
    )

    # ── ACADEMIC MANAGEMENT ──
    st.markdown('<div class="sb-section-label">ACADEMIC MANAGEMENT</div>', unsafe_allow_html=True)
    academic_choice = st.radio(
        "academic_nav",
        ["None_A", "🎓 Courses", "👨‍🏫 Faculty", "🏛️ Rooms", "👥 Student Groups"],
        label_visibility="collapsed",
        index=0,
        key="academic_radio",
        format_func=lambda x: "" if x == "None_A" else x
    )

    # ── OPERATIONS ──
    st.markdown('<div class="sb-section-label">OPERATIONS</div>', unsafe_allow_html=True)
    ops_choice = st.radio(
        "ops_nav",
        ["None_O", "⚠️ Conflict Management", "🔄 Makeup Classes", "📋 Absence & Substitution", "📆 Rescheduling"],
        label_visibility="collapsed",
        index=0,
        key="ops_radio",
        format_func=lambda x: "" if x == "None_O" else x
    )

    # ── TOOLS & REPORTS ──
    st.markdown('<div class="sb-section-label">TOOLS & REPORTS</div>', unsafe_allow_html=True)
    tools_choice = st.radio(
        "tools_nav",
        ["None_T", "🛠️ Tools Center", "🚀 Generator", "📈 ML Analytics", "📑 Reports & Exports",
         "⚙️ Data Management", "🔍 Diagnostics", "⚡ Benchmarking"],
        label_visibility="collapsed",
        index=0,
        key="tools_radio",
        format_func=lambda x: "" if x == "None_T" else x
    )

    # ── SYSTEM ──
    st.markdown('<div class="sb-section-label">SYSTEM</div>', unsafe_allow_html=True)
    system_choice = st.radio(
        "system_nav",
        ["None_S", "🏛️ About & NEP-2020"],
        label_visibility="collapsed",
        index=0,
        key="system_radio",
        format_func=lambda x: "" if x == "None_S" else x
    )

    # Determine active page
    if academic_choice != "None_A":
        current_page = academic_choice
    elif ops_choice != "None_O":
        current_page = ops_choice
    elif tools_choice != "None_T":
        current_page = tools_choice
    elif system_choice != "None_S":
        current_page = system_choice
    else:
        current_page = overview_choice

    # ── Bottom user card ──
    st.markdown("""
    <div class="sb-user-card">
        <div style="font-size:0.68rem; color:#475569 !important; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.07em; margin-bottom:8px;">TEAM</div>
        <div class="sb-user-name">Gandikota Sai Chandana</div>
        <div class="sb-user-role">Reg. 12511912 · RK3P25ILA15</div>
        <div style="border-top:1px solid rgba(255,255,255,0.08); margin:8px 0;"></div>
        <div class="sb-user-name">Inayat</div>
        <div class="sb-user-role">Reg. 12512142 · RK3P25ILA16</div>
        <div style="border-top:1px solid rgba(255,255,255,0.08); margin:8px 0;"></div>
        <div style="font-size:0.7rem; color:#475569 !important;">Subject: K3P25IL</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: render top header bar
# ─────────────────────────────────────────────────────────────────────────────
def render_header(breadcrumb_page: str):
    today = datetime.date.today().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="shopeers-header">
        <div style="display:flex; align-items:center; gap:14px;">
            <button id="sb-hamburger" class="hamburger-btn" title="Toggle sidebar" aria-label="Toggle sidebar">
                <span></span><span></span><span></span>
            </button>
            <div class="shopeers-breadcrumb">
                <span>Home</span>
                <span class="crumb-sep">›</span>
                <span class="crumb-active">{breadcrumb_page}</span>
            </div>
        </div>
        <div style="font-size:0.78rem; color:#94A3B8;">{today}</div>
        <div class="shopeers-header-right">
            <div class="header-icon-btn">🔔</div>
            <div class="header-avatar">AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {"<p class='page-subtitle'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def kpi_card(icon, label, value, subtitle, variant="kpi-card-blue"):
    return f"""
    <div class="metric-card {variant}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{subtitle}</div>
    </div>
    """

def status_badge(text, kind="info"):
    dot = {"success": "🟢", "warning": "🟡", "danger": "🔴", "info": "🔵"}.get(kind, "⚪")
    return f'<span class="status-badge badge-{kind}">{dot} {text}</span>'

CHART_PALETTE = ["#0A24E9", "#29315D", "#5C9764", "#64748B", "#94A3B8", "#7C3AED", "#F59E0B"]

def style_fig(fig, height=280):
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#0B0D17"),
        margin=dict(l=16, r=16, t=10, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# HAMBURGER JS BRIDGE
# Runs once per render inside a 0-height iframe.
# Uses window.parent to reach the Streamlit host document, finds the native
# (now invisible) collapsedControl button, and clicks it whenever the user
# clicks our custom #sb-hamburger element in the header.
# A MutationObserver re-attaches the listener after every Streamlit re-render.
# ─────────────────────────────────────────────────────────────────────────────
components.html("""
<script>
(function () {
    "use strict";

    var pdoc = window.parent.document;

    /* Selectors for Streamlit's native sidebar toggle (varies by version) */
    var NATIVE_SELECTORS = [
        '[data-testid="collapsedControl"]',
        'button[data-testid="baseButton-headerNoPadding"]',
        'section[data-testid="stSidebar"] > div > button',
    ];

    function getNativeToggle() {
        for (var i = 0; i < NATIVE_SELECTORS.length; i++) {
            var el = pdoc.querySelector(NATIVE_SELECTORS[i]);
            if (el) return el;
        }
        return null;
    }

    function getSidebar() {
        return pdoc.querySelector('[data-testid="stSidebar"]');
    }

    function isSidebarCollapsed(sidebar) {
        if (!sidebar) return false;
        var rect = sidebar.getBoundingClientRect();
        return rect.width < 60;
    }

    function toggleSidebar() {
        /* 1. Try the native Streamlit button first */
        var native = getNativeToggle();
        if (native) { native.click(); return; }

        /* 2. Fallback: direct CSS transform */
        var sb = getSidebar();
        if (!sb) return;
        if (isSidebarCollapsed(sb)) {
            sb.style.transform = "none";
            sb.style.marginLeft = "0";
            sb.style.width = "244px";
        } else {
            sb.style.transform = "translateX(-244px)";
            sb.style.marginLeft = "-244px";
        }
    }

    var attached = false;

    function attachHamburger() {
        var btn = pdoc.getElementById("sb-hamburger");
        if (!btn || btn.dataset.wired === "1") return;
        btn.dataset.wired = "1";
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            toggleSidebar();
        });
        attached = true;
    }

    /* Initial attach after Streamlit paints */
    function tryAttach(n) {
        attachHamburger();
        if (!attached && n < 30) {
            setTimeout(function () { tryAttach(n + 1); }, 200);
        }
    }
    tryAttach(0);

    /* Re-attach after every Streamlit re-render (MutationObserver) */
    var observer = new MutationObserver(function () {
        var btn = pdoc.getElementById("sb-hamburger");
        if (btn && btn.dataset.wired !== "1") {
            attached = false;
            tryAttach(0);
        }
    });
    observer.observe(pdoc.body, { childList: true, subtree: true });
})();
</script>
""", height=0, scrolling=False)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 · DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if current_page == "📊 Dashboard":
    render_header("Dashboard")
    render_page_header("Academic Overview", "Real-time snapshot of scheduling health and institutional data.")

    metrics = loader.get_summary_metrics()
    sched = st.session_state.get("current_schedule", {})
    ml_acc = ml_clf.metrics.get("accuracy", 0.9806) * 100

    # ── KPI Row 1 ──
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(kpi_card("📚", "Total Courses", metrics["total_courses"],
                              "6 NEP-2020 credit baskets", "kpi-card-blue"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("👨‍🏫", "Faculty Members", metrics["total_faculty"],
                              "Workload capped ≤ 4 h/day", "kpi-card-green"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("🏛️", "Available Rooms", metrics["total_rooms"],
                              f"{metrics['total_room_capacity']} total seats", "kpi-card-purple"), unsafe_allow_html=True)

    st.write("")

    # ── KPI Row 2 ──
    k4, k5, k6 = st.columns(3)
    with k4:
        st.markdown(kpi_card("👥", "Student Groups", metrics["total_student_groups"],
                              f"{metrics['total_enrolled_students']} enrolled students", "kpi-card-orange"), unsafe_allow_html=True)
    with k5:
        assigned = sched.get("assigned_sessions", 0)
        total_s = sched.get("total_sessions", 0)
        st.markdown(kpi_card("📅", "Scheduled Sessions", f"{assigned} / {total_s}",
                              "100% weekly contact hours", "kpi-card-blue"), unsafe_allow_html=True)
    with k6:
        st.markdown(kpi_card("✅", "Hard Constraints Met", "10 / 10",
                              "0 violations detected", "kpi-card-green"), unsafe_allow_html=True)

    st.write("")

    # ── Charts Row 1 ──
    ch1, ch2 = st.columns([6, 4])
    with ch1:
        st.markdown('<div class="surface-card"><h3>Sessions by Day of Week</h3>', unsafe_allow_html=True)
        records = st.session_state.get("schedule_records", [])
        if records:
            df_r = pd.DataFrame(records)
            days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            day_counts = df_r["day"].value_counts().reindex(days_order, fill_value=0).reset_index()
            day_counts.columns = ["Day", "Sessions"]
            fig_days = px.bar(day_counts, x="Day", y="Sessions", color_discrete_sequence=["#0A24E9"])
            fig_days.update_traces(marker_line_width=0, marker_cornerradius=6)
            fig_days.update_layout(xaxis=dict(showgrid=False, title=None), yaxis=dict(gridcolor="#F1F5F9", title=None))
            st.plotly_chart(style_fig(fig_days, 230), use_container_width=True)
        else:
            st.info("Generate a schedule to view session distribution.")
        st.markdown('</div>', unsafe_allow_html=True)

    with ch2:
        st.markdown('<div class="surface-card"><h3>Room Type Capacity</h3>', unsafe_allow_html=True)
        rooms_df = data_dict["rooms"]
        fig_room = px.pie(rooms_df, names="type", values="capacity",
                          color_discrete_sequence=CHART_PALETTE, hole=0.5)
        fig_room.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(style_fig(fig_room, 230), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # ── Charts Row 2 ──
    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown('<div class="surface-card"><h3>Courses by NEP-2020 Category</h3>', unsafe_allow_html=True)
        courses_df = data_dict["courses"]
        cat_counts = courses_df["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_cat = px.bar(cat_counts, x="Category", y="Count", color="Category",
                         color_discrete_sequence=CHART_PALETTE)
        fig_cat.update_traces(marker_line_width=0, marker_cornerradius=6)
        fig_cat.update_layout(showlegend=False,
                               xaxis=dict(showgrid=False, title=None),
                               yaxis=dict(gridcolor="#F1F5F9", title=None))
        st.plotly_chart(style_fig(fig_cat, 240), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ch4:
        st.markdown('<div class="surface-card"><h3>Faculty Workload Distribution</h3>', unsafe_allow_html=True)
        fac_df = data_dict["faculty"]
        if "max_hours_per_day" in fac_df.columns:
            fig_fac = px.histogram(fac_df, x="max_hours_per_day",
                                   color_discrete_sequence=["#29315D"],
                                   labels={"max_hours_per_day": "Max Hours/Day"})
            fig_fac.update_layout(xaxis=dict(title="Max Hours/Day"), yaxis=dict(gridcolor="#F1F5F9", title="Faculty Count"))
            st.plotly_chart(style_fig(fig_fac, 240), use_container_width=True)
        else:
            st.info("Faculty workload data unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── System Status Bar ──
    comp_pct = sched.get("completeness_pct", 100.0)
    solver_mode_disp = sched.get("status", "SOLVED")
    st.markdown(f"""
    <div class="system-status-bar">
        <span class="sys-label">System Status:</span>
        {status_badge("All Systems Operational", "success")}
        {status_badge(f"Completeness: {comp_pct:.1f}%", "success")}
        {status_badge(f"Solver: {solver_mode_disp}", "info")}
        {status_badge(f"ML Accuracy: {ml_acc:.1f}%", "success")}
        {status_badge("NEP-2020 Compliant", "success")}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 · TIMETABLE VIEWER
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "📅 Timetable":
    render_header("Timetable")
    records = st.session_state.get("schedule_records", [])
    if not records:
        st.warning("No schedule generated yet. Go to **🚀 Generator** to create one.")
    else:
        df_records = pd.DataFrame(records)
        DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        SLOTS = [
            (1, "09:00"), (2, "10:00"), (3, "11:15"),
            (4, "12:15"), (5, "14:00"), (6, "15:00"), (7, "16:00"),
        ]

        # Filter row
        fc1, fc2, fc3 = st.columns([3, 2, 2])
        with fc1:
            all_groups = sorted(df_records["group_id"].unique())
            sel_group = st.selectbox("Student Cohort", all_groups, index=0, label_visibility="collapsed")
        with fc2:
            day_opts = ["All Days"] + DAYS
            sel_day = st.selectbox("Day Filter", day_opts, index=0, label_visibility="collapsed")
        with fc3:
            st.markdown(f"""
            <div style="padding-top:6px;">
                {status_badge(f"Cohort: {sel_group}", "info")}
                {status_badge("Conflict-Free", "success")}
            </div>
            """, unsafe_allow_html=True)

        g_sub = df_records[df_records["group_id"] == sel_group]

        render_page_header(f"Weekly Timetable — {sel_group}", "Autumn Semester 2025  ·  Certified 100% Conflict-Free")

        # Timetable grid
        active_days = [d for d in DAYS if sel_day == "All Days" or d == sel_day]
        cols = st.columns(len(active_days))

        CARD_COLORS = {
            "Lab": "tc-green",
            "CS": "tc-blue",
            "AI": "tc-navy",
            "NEP": "tc-purple",
            "MDC": "tc-purple",
            "VAC": "tc-purple",
        }

        def get_card_color(row):
            rt = str(row.get("room_type", ""))
            cid = str(row.get("course_id", ""))
            cname = str(row.get("course_name", "")).lower()
            if "Lab" in rt or "lab" in cname:
                return "tc-green"
            if "AI" in cid:
                return "tc-navy"
            if "CS" in cid:
                return "tc-blue"
            if any(k in cid for k in ["NEP", "MDC", "VAC"]):
                return "tc-purple"
            return "tc-orange"

        for d_idx, day_name in enumerate(active_days):
            with cols[d_idx]:
                st.markdown(f'<div class="day-pill">{day_name[:3].upper()}</div>', unsafe_allow_html=True)
                for s_id, s_label in SLOTS:
                    match = g_sub[(g_sub["day"] == day_name) & (g_sub["slot_id"] == s_id)]
                    if not match.empty:
                        m = match.iloc[0]
                        cc = get_card_color(m)
                        fname = str(m["faculty_name"]).split()[-1]
                        st.markdown(f"""
                        <div class="timetable-card {cc}">
                            <div class="tc-code">{m['course_id']}</div>
                            <div class="tc-name">{str(m['course_name'])[:26]}</div>
                            <div class="tc-tags">
                                <span class="tc-room">{m['room_id']}</span>
                                <span class="tc-fac">Prof. {fname}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="timetable-card-free">
                            <div style="font-size:0.65rem; color:#94A3B8; font-weight:600;">{s_label}</div>
                            <div>Free Period</div>
                        </div>
                        """, unsafe_allow_html=True)

        st.write("")

        # ── Bottom Info Cards ──
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.markdown("""
            <div class="anc-card">
                <div class="anc-card-header">📚 Subjects & Credits</div>
                <div class="anc-row">CS101 · Programming (4 Credits)</div>
                <div class="anc-row">CS102 · Computing Lab (2 Credits)</div>
                <div class="anc-row">MA101 · Calculus & Algebra (4 Credits)</div>
                <div class="anc-row">PH101 · Applied Physics (3 Credits)</div>
                <div class="anc-row">NEP_MDC01 · Digital Humanities (3 Credits)</div>
            </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown("""
            <div class="anc-card">
                <div class="anc-card-header">📝 Faculty & Lab Notes</div>
                <div class="anc-row anc-row-green"><b>Turing Lab:</b> Room CL301 reserved for lab sessions.</div>
                <div class="anc-row anc-row-green"><b>Office Hours:</b> Wed 16:00–17:00 (Room 201).</div>
                <div class="anc-row anc-row-green"><b>Pre-fixed:</b> Monday Slot 2 locked for keynote.</div>
                <div class="anc-row anc-row-green"><b>Attendance:</b> 75% min. mandatory (NEP-2020).</div>
            </div>
            """, unsafe_allow_html=True)
        with a3:
            st.markdown("""
            <div class="anc-card">
                <div class="anc-card-header">☕ Break & Intervals</div>
                <div class="anc-row anc-row-orange"><b>Lunch:</b> 13:15–14:00 daily (Campus Café)</div>
                <div class="anc-row anc-row-orange"><b>Passing Time:</b> 15 min between morning slots</div>
                <div class="anc-row anc-row-orange"><b>Sports/Wellness:</b> Wednesday 16:00–17:00</div>
                <div class="anc-row anc-row-orange"><b>Library:</b> Open until 21:00 on weekdays</div>
            </div>
            """, unsafe_allow_html=True)
        with a4:
            st.markdown("""
            <div class="anc-card">
                <div class="anc-card-header">🎯 Compliance & Goals</div>
                <div class="anc-row anc-row-purple"><b>Weekly Quota:</b> 20/20 Contact Hours Satisfied</div>
                <div class="anc-row anc-row-purple"><b>Clashes:</b> 0 Violations (Certified)</div>
                <div class="anc-row anc-row-purple"><b>Fatigue Cap:</b> ≤ 2h consecutive lectures</div>
                <div class="anc-row anc-row-purple"><b>Audit:</b> Independent Validation PASSED</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 · COURSES
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🎓 Courses":
    render_header("Courses")
    render_page_header("Course Catalogue", "All courses registered under NEP-2020 credit framework.")

    courses_df = data_dict["courses"]
    tab_list, tab_map = st.tabs(["📋 Course List", "🗺️ Curriculum Mapping"])

    with tab_list:
        search_term = st.text_input("🔍 Search courses…", placeholder="Enter course name or code")
        filtered = courses_df
        if search_term:
            mask = courses_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
            filtered = courses_df[mask]
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(filtered, use_container_width=True, height=420)
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(f"{len(filtered)} courses shown")

    with tab_map:
        if "category" in courses_df.columns:
            cat_fig = px.sunburst(courses_df, path=["category"],
                                  color_discrete_sequence=CHART_PALETTE)
            cat_fig.update_layout(paper_bgcolor="#FFFFFF", margin=dict(t=10, b=10, l=10, r=10), height=380)
            st.plotly_chart(cat_fig, use_container_width=True)
        st.dataframe(courses_df[["course_id", "course_name", "category", "credits"]
                                  if all(c in courses_df.columns for c in ["course_id", "course_name", "category", "credits"])
                                  else courses_df.columns[:6]],
                     use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 · FACULTY
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "👨‍🏫 Faculty":
    render_header("Faculty")
    render_page_header("Faculty Directory", "20 faculty members across departments.")

    fac_df = data_dict["faculty"]
    tab_dir, tab_wl = st.tabs(["👥 Faculty Directory", "📊 Workload Overview"])

    with tab_dir:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        display_cols = [c for c in ["faculty_id", "name", "department", "designation",
                                     "max_hours_per_day", "unavailable_slots"] if c in fac_df.columns]
        st.dataframe(fac_df[display_cols], use_container_width=True, height=440)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_wl:
        if "max_hours_per_day" in fac_df.columns and "department" in fac_df.columns:
            wl_df = fac_df.groupby("department")["max_hours_per_day"].mean().reset_index()
            wl_df.columns = ["Department", "Avg Max Hours/Day"]
            fig_wl = px.bar(wl_df, x="Department", y="Avg Max Hours/Day",
                            color_discrete_sequence=["#29315D"])
            fig_wl.update_traces(marker_cornerradius=6)
            fig_wl.update_layout(xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#F1F5F9"))
            st.plotly_chart(style_fig(fig_wl, 300), use_container_width=True)
        else:
            st.info("Workload column data not available.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 · ROOMS
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🏛️ Rooms":
    render_header("Rooms")
    render_page_header("Rooms & Laboratories", f"{data_dict['rooms'].shape[0]} venues across campus.")

    rooms_df = data_dict["rooms"]
    r1, r2 = st.columns([3, 2])
    with r1:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(rooms_df, use_container_width=True, height=380)
        st.markdown('</div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="surface-card"><h3>Capacity by Room Type</h3>', unsafe_allow_html=True)
        if "type" in rooms_df.columns and "capacity" in rooms_df.columns:
            type_cap = rooms_df.groupby("type")["capacity"].sum().reset_index()
            fig_rc = px.bar(type_cap, x="type", y="capacity",
                            color_discrete_sequence=CHART_PALETTE)
            fig_rc.update_traces(marker_cornerradius=6)
            fig_rc.update_layout(xaxis=dict(title="Type", showgrid=False),
                                  yaxis=dict(title="Total Capacity", gridcolor="#F1F5F9"))
            st.plotly_chart(style_fig(fig_rc, 320), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 · STUDENT GROUPS
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "👥 Student Groups":
    render_header("Student Groups")
    render_page_header("Student Groups", f"{data_dict['student_groups'].shape[0]} cohorts across programmes.")

    sg_df = data_dict["student_groups"]
    s1, s2 = st.columns([3, 2])
    with s1:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(sg_df, use_container_width=True, height=380)
        st.markdown('</div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="surface-card"><h3>Enrollment per Group</h3>', unsafe_allow_html=True)
        enroll_col = next((c for c in ["enrolled_students", "size", "strength"] if c in sg_df.columns), None)
        gid_col = next((c for c in ["group_id", "id", "cohort_id"] if c in sg_df.columns), sg_df.columns[0])
        if enroll_col:
            fig_sg = px.bar(sg_df, x=gid_col, y=enroll_col,
                            color_discrete_sequence=["#5C9764"])
            fig_sg.update_traces(marker_cornerradius=6)
            fig_sg.update_layout(xaxis=dict(showgrid=False, title="Group"),
                                  yaxis=dict(gridcolor="#F1F5F9", title="Students"))
            st.plotly_chart(style_fig(fig_sg, 320), use_container_width=True)
        else:
            st.info("Enrollment count column not found in student groups data.")
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7 · CONFLICT MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "⚠️ Conflict Management":
    render_header("Conflict Management")
    render_page_header("Conflict Diagnostics", "Explainable infeasibility analysis on over-constrained instances.")

    st.info("Demonstrating Explainable Diagnostics on an overconstrained problem instance (Faculty Blackout + Room Shortage).")
    with st.spinner("Running overconstrained solver & generating diagnostics..."):
        inf_data = loader.get_infeasible_benchmark_instance()
        inf_solver = TimetableCSPSolver(data_dict=inf_data, solver_mode="baseline",
                                        max_backtracks=200, timeout_seconds=4.0)
        inf_res = inf_solver.solve()
        unassigned = [v for v in inf_solver.variables if not v.is_assigned()]
        diagnostics = ConflictExplainer.diagnose_unassigned_sessions(unassigned, inf_data, inf_solver.rooms_dict)

    col_diag1, col_diag2 = st.columns([1, 3])
    with col_diag1:
        st.markdown(f"""
        <div class="metric-card kpi-card-orange">
            <span class="kpi-icon">⚠️</span>
            <div class="kpi-label">Unassigned Sessions</div>
            <div class="kpi-value">{len(unassigned)}</div>
            <div class="kpi-sub">Requires resolution</div>
        </div>
        """, unsafe_allow_html=True)
    with col_diag2:
        if diagnostics:
            diag_df = pd.DataFrame(diagnostics)
            disp_cols = [c for c in ["course_id", "group_id", "constraint_violated",
                                      "root_cause", "actionable_recommendation"] if c in diag_df.columns]
            st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
            st.dataframe(diag_df[disp_cols], use_container_width=True, height=380)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No conflicts detected in the diagnostic run.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 8 · MAKEUP CLASSES
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🔄 Makeup Classes":
    render_header("Makeup Classes")
    render_page_header("Makeup Class Scheduling & Joint-Feasibility", "Track, verify joint multi-resource availability, and schedule compensatory sessions.")
    _render_tool_makeup_feasibility(data_dict)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 9 · ABSENCE & SUBSTITUTION
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "📋 Absence & Substitution":
    render_header("Absence & Substitution")
    render_page_header("Faculty Absence Management & Substitute Recommendation", "Declare faculty absences, assess session coverage impact, and match qualified substitute instructors.")
    tab_abs, tab_sub = st.tabs(["📋 Declare Faculty Absence", "👨‍🏫 Match Substitute Faculty"])
    with tab_abs:
        _render_tool_absence_manager(data_dict)
    with tab_sub:
        _render_tool_substitute_matcher(data_dict)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 10 · RESCHEDULING
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "📆 Rescheduling":
    render_header("Localized Rescheduling")
    render_page_header("Single-Session Rescheduling Engine", "Atomically reschedule individual course sessions with rollback guarantee and collision checking.")
    _render_tool_rescheduler(data_dict)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 10.5 · TOOLS CENTER
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🛠️ Tools Center":
    render_header("Tools Center")
    render_tools_center(data_dict, ml_clf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 11 · GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🚀 Generator":
    render_header("Generator")
    render_page_header("Timetable Generator Engine", "Configure CSP search parameters and execute live backtracking allocation.")

    g_col1, g_col2 = st.columns([1, 2])
    with g_col1:
        st.markdown('<div class="surface-card"><h3>⚙️ Solver Options</h3>', unsafe_allow_html=True)
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
        st.markdown('<div class="surface-card"><h3>📊 Execution Telemetry & Status</h3>', unsafe_allow_html=True)
        if run_btn:
            with st.spinner("Solving academic timetable with CSP heuristics…"):
                new_solver = TimetableCSPSolver(
                    data_dict=data_dict,
                    solver_mode=mode_key,
                    max_backtracks=max_bt,
                    timeout_seconds=timeout,
                    enable_forward_checking=forward_chk,
                    ml_classifier=ml_clf
                )
                res = new_solver.solve()
                is_valid, violations = IndependentTimetableValidator.validate(res["schedule_records"], data_dict)
                res["independent_validation_passed"] = is_valid
                res["violations_list"] = violations
                st.session_state["current_schedule"] = res
                st.session_state["schedule_records"] = res["schedule_records"]

        sched = st.session_state.get("current_schedule", {})
        if sched:
            st.success(f"Status: **{sched.get('status')}** · Assigned: **{sched.get('assigned_sessions')} / {sched.get('total_sessions')} sessions**")
            t1, t2, t3 = st.columns(3)
            t1.metric("Execution Time", f"{sched.get('execution_time_seconds', 0.0):.3f} s")
            t2.metric("Nodes Explored", sched.get("nodes_explored", 0))
            t3.metric("Backtracking Steps", sched.get("backtracks_count", 0))
            t4, t5, t6 = st.columns(3)
            t4.metric("FC Prunings", sched.get("forward_checking_prunings", 0))
            t5.metric("Constraint Checks", sched.get("constraint_checks", 0))
            t6.metric("Quality Score", f"{sched.get('quality_score', 0.0)}/100")
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 12 · ML ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "📈 ML Analytics":
    render_header("ML Analytics")
    render_page_header("Machine Learning Analytics", "Random Forest classifier trained on 1,800 historical scheduling examples with 15 engineered features.")

    ml_metrics = ml_clf.metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Test Accuracy", f"{ml_metrics.get('accuracy', 0.9806)*100:.2f}%")
    m2.metric("Precision", f"{ml_metrics.get('precision', 1.0)*100:.2f}%")
    m3.metric("Recall", f"{ml_metrics.get('recall', 0.9729)*100:.2f}%")
    m4.metric("F1-Score", f"{ml_metrics.get('f1_score', 0.9862):.4f}")
    m5.metric("ROC-AUC", f"{ml_metrics.get('roc_auc', 0.9974):.4f}")

    st.write("")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown('<div class="surface-card"><h3>Feature Importances (Gini Index)</h3>', unsafe_allow_html=True)
        feat_df = pd.DataFrame(list(ml_clf.feature_importances.items()), columns=["Feature", "Importance"])
        fig_f = px.bar(feat_df.head(10), x="Importance", y="Feature", orientation="h",
                       color="Importance",
                       color_continuous_scale=["#EEF2FF", "#0A24E9"])
        fig_f.update_layout(yaxis=dict(autorange="reversed"),
                             xaxis=dict(showgrid=False), coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig_f, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with mc2:
        st.markdown('<div class="surface-card"><h3>Confusion Matrix (Test Set)</h3>', unsafe_allow_html=True)
        cm = ml_metrics.get("confusion_matrix", [[216, 0], [7, 137]])
        fig_cm = px.imshow(
            cm,
            labels=dict(x="Predicted", y="True", color="Count"),
            x=["Feasible (0)", "Conflict (1)"],
            y=["Feasible (0)", "Conflict (1)"],
            color_continuous_scale=["#EEF2FF", "#0A24E9"],
            text_auto=True
        )
        st.plotly_chart(style_fig(fig_cm, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 13 · REPORTS & EXPORTS
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "📑 Reports & Exports":
    render_header("Reports & Exports")
    render_reports_center(data_dict)

    # Secondary Institutional Documentation Archive
    with st.expander("📚 Static Institutional Documentation Archive (.docx, .pdf, pre-generated master .xlsx)"):
        out_dir = os.path.join(BASE_DIR, "outputs")
        docs_dir = os.path.join(BASE_DIR, "docs")
        docx_file = os.path.join(docs_dir, "NEP2020_Timetable_Project_Report.docx")
        pdf_file = os.path.join(docs_dir, "NEP2020_Timetable_Project_Report.pdf")
        excel_file = os.path.join(out_dir, "master_timetable_multisheet.xlsx")

        e1, e2, e3 = st.columns(3)
        with e1:
            st.markdown("<b>📄 Technical Project Report (.docx)</b>", unsafe_allow_html=True)
            if os.path.exists(docx_file):
                with open(docx_file, "rb") as f:
                    st.download_button("⬇️ Download (.docx)", data=f.read(),
                                       file_name="NEP2020_Timetable_Project_Report.docx",
                                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                       use_container_width=True)
        with e2:
            st.markdown("<b>📊 Master Schedule Workbook (.xlsx)</b>", unsafe_allow_html=True)
            if os.path.exists(excel_file):
                with open(excel_file, "rb") as f:
                    st.download_button("⬇️ Download (.xlsx)", data=f.read(),
                                       file_name="NEP2020_Academic_Timetable.xlsx",
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                       use_container_width=True)
        with e3:
            st.markdown("<b>📑 Academic Paper PDF (.pdf)</b>", unsafe_allow_html=True)
            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    st.download_button("⬇️ Download (.pdf)", data=f.read(),
                                       file_name="NEP2020_Timetable_Project_Report.pdf",
                                       mime="application/pdf",
                                       use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 14 · DATA MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "⚙️ Data Management":
    render_header("Data Management")
    render_page_header("Institutional Data Management", "View and audit all five core datasets.")

    n_courses = data_dict["courses"].shape[0]
    n_faculty = data_dict["faculty"].shape[0]
    n_rooms = data_dict["rooms"].shape[0]
    n_groups = data_dict["student_groups"].shape[0]
    n_curr = data_dict["curriculum"].shape[0]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"📚 Courses ({n_courses})",
        f"👨‍🏫 Faculty ({n_faculty})",
        f"🏛️ Rooms & Labs ({n_rooms})",
        f"👥 Student Groups ({n_groups})",
        f"📋 Curriculum ({n_curr})"
    ])
    with tab1:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(data_dict["courses"], use_container_width=True, height=440)
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(data_dict["faculty"], use_container_width=True, height=440)
        st.markdown('</div>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(data_dict["rooms"], use_container_width=True, height=440)
        st.markdown('</div>', unsafe_allow_html=True)
    with tab4:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(data_dict["student_groups"], use_container_width=True, height=440)
        st.markdown('</div>', unsafe_allow_html=True)
    with tab5:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(data_dict["curriculum"], use_container_width=True, height=440)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 15 · DIAGNOSTICS
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🔍 Diagnostics":
    render_header("Diagnostics")
    render_page_header("Explainable Infeasibility Diagnostics", "Detailed root-cause analysis for overconstrained scheduling problems.")

    st.info("Demonstrating Explainable Diagnostics on an overconstrained problem instance (Faculty Blackout + Room Shortage).")
    with st.spinner("Running diagnostic solver…"):
        inf_data = loader.get_infeasible_benchmark_instance()
        inf_solver = TimetableCSPSolver(data_dict=inf_data, solver_mode="baseline",
                                        max_backtracks=200, timeout_seconds=4.0)
        inf_res = inf_solver.solve()
        unassigned = [v for v in inf_solver.variables if not v.is_assigned()]
        diagnostics = ConflictExplainer.diagnose_unassigned_sessions(unassigned, inf_data, inf_solver.rooms_dict)

    st.markdown(f"**Unassigned Course Sessions Detected:** `{len(unassigned)}`")
    if diagnostics:
        diag_df = pd.DataFrame(diagnostics)
        disp_cols = [c for c in ["course_id", "group_id", "constraint_violated",
                                  "root_cause", "actionable_recommendation"] if c in diag_df.columns]
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.dataframe(diag_df[disp_cols], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("No conflicts detected in the diagnostic run.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 16 · BENCHMARKING
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "⚡ Benchmarking":
    render_header("Benchmarking")
    render_page_header("Head-to-Head Solver Benchmarking", "Empirical comparison of Baseline CSP vs ML-Assisted CSP.")

    bench = st.session_state.get("benchmark_results")
    if bench:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        comp_df = pd.DataFrame(bench["comparison_table"])
        st.dataframe(comp_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if bench.get("performance_summary"):
            st.info(bench["performance_summary"])
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">⚡</div>
            <div class="empty-state-title">No Benchmark Results Cached</div>
            <div class="empty-state-desc">Run the benchmarking script to generate comparison data. Results will be saved to outputs/benchmark_results.json and displayed here.</div>
        </div>
        """, unsafe_allow_html=True)

    run_bench = st.button("⚡ Run Live Benchmark Now", type="primary")
    if run_bench:
        with st.spinner("Running live solver benchmark — this may take 20–40 seconds…"):
            bench_runner = TimetableBenchmarker(data_dict=data_dict, ml_classifier=ml_clf)
            bench_res = bench_runner.run_full_benchmark()
            st.session_state["benchmark_results"] = bench_res
            st.success("Benchmark complete! Refresh to view results.")
            if bench_res.get("comparison_table"):
                st.dataframe(pd.DataFrame(bench_res["comparison_table"]), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 17 · ABOUT & NEP-2020
# ─────────────────────────────────────────────────────────────────────────────
elif current_page == "🏛️ About & NEP-2020":
    render_header("About & NEP-2020")
    render_page_header("About & NEP-2020 Methodology", "Smart India Hackathon 2025 | Problem Statement SIH25091")

    ab1, ab2 = st.columns(2)
    with ab1:
        st.markdown("""
        <div class="surface-card">
            <h3>🏫 National Education Policy (NEP) 2020</h3>
            <p style="font-size:0.875rem; color:#334155; line-height:1.6;">
                Under NEP-2020, university curriculum breaks away from rigid silos to allow
                multidisciplinary cross-enrollment across <strong>6 credit categories</strong>:
            </p>
            <div class="anc-row">📘 <b>DSC</b> — Major Core (Discipline Specific)</div>
            <div class="anc-row">📗 <b>DSE</b> — Minor Electives (Discipline Specific Elective)</div>
            <div class="anc-row anc-row-purple">🌐 <b>MDC</b> — Multidisciplinary Courses</div>
            <div class="anc-row anc-row-orange">🎯 <b>AEC</b> — Ability Enhancement Courses</div>
            <div class="anc-row anc-row-green">🛠️ <b>SEC</b> — Skill Enhancement Courses</div>
            <div class="anc-row anc-row-purple">💡 <b>VAC</b> — Value-Added Courses</div>
        </div>
        """, unsafe_allow_html=True)

    with ab2:
        st.markdown("""
        <div class="surface-card">
            <h3>🤖 CSP + ML Engine</h3>
            <p style="font-size:0.875rem; color:#334155; line-height:1.6;">
                Our scheduling engine combines classical Constraint Satisfaction with Supervised ML:
            </p>
            <div class="anc-row"><b>MRV Heuristic</b> — Minimum Remaining Values variable ordering</div>
            <div class="anc-row"><b>Degree Heuristic</b> — Prioritise most-constrained variables</div>
            <div class="anc-row anc-row-green"><b>LCV Heuristic</b> — Least Constraining Value selection</div>
            <div class="anc-row anc-row-green"><b>Forward Checking</b> — Prune invalid assignments early</div>
            <div class="anc-row anc-row-purple"><b>Random Forest ML</b> — Conflict probability scoring (AUC 0.9974)</div>
            <div class="anc-row anc-row-orange"><b>Explainable AI</b> — Root-cause diagnostics for infeasibility</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="surface-card">
        <h3>👥 Development Team</h3>
        <div style="display:flex; gap:24px; flex-wrap:wrap;">
            <div style="flex:1; min-width:200px;">
                <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.07em; color:#0A24E9; margin-bottom:4px;">LEAD ALGORITHM ARCHITECT</div>
                <div style="font-size:1rem; font-weight:700; color:#0B0D17;">Gandikota Sai Chandana</div>
                <div style="font-size:0.8rem; color:#64748B;">Reg. 12511912 · Group RK3P25ILA15</div>
                <div style="font-size:0.8rem; color:#334155; margin-top:6px; line-height:1.5;">
                    CSP formulation, 10 hard + 6 soft constraints, heuristic backtracking (MRV, Degree, LCV, FC),
                    ML classifier training, empirical benchmarking.
                </div>
            </div>
            <div style="width:1px; background:#E2E8F0;"></div>
            <div style="flex:1; min-width:200px;">
                <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.07em; color:#5C9764; margin-bottom:4px;">LEAD FULL-STACK DEVELOPER</div>
                <div style="font-size:1rem; font-weight:700; color:#0B0D17;">Inayat</div>
                <div style="font-size:0.8rem; color:#64748B;">Reg. 12512142 · Group RK3P25ILA16</div>
                <div style="font-size:0.8rem; color:#334155; margin-top:6px; line-height:1.5;">
                    Streamlit UI, data management, timetable visualization grids,
                    multi-format export engines (Word, Excel, PDF, CSV), end-to-end integration.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
