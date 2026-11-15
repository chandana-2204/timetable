"""
Visual Screenshot and Diagram Generator for Project Report & Presentation Deliverables
Generates crisp, high-resolution figures in vibrant aesthetic pastels (Teal, Pearl Blue, Sea Green, Lilac).
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
screenshot_dir = os.path.join(base_dir, "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)

# Set clean academic light theme
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def generate_dashboard_screenshot():
    """Generates an executive dashboard UI mockup screenshot in aesthetic pastel palette."""
    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300)
    fig.patch.set_facecolor('#FAF7F2')
    ax.set_facecolor('#FAF7F2')
    ax.axis('off')

    # Header Banner Card
    header_box = patches.FancyBboxPatch((0.02, 0.86), 0.96, 0.12, boxstyle="round,pad=0.01", ec="#99F6E4", fc="#FFFFFF", lw=1.5)
    ax.add_patch(header_box)
    ax.text(0.045, 0.94, "NEP-2020 MULTIDISCIPLINARY ACADEMIC TIMETABLE PLANNING SYSTEM", fontsize=13.5, fontweight='bold', color="#0F172A")
    ax.text(0.045, 0.89, "Smart India Hackathon 2025 | Problem Statement SIH25091 | Team: Gandikota Sai Chandana & Inayat | Code: K3P25IL", fontsize=8.8, color="#0D9488", fontweight='bold')

    # 4 Metric Cards in Vibrant Aesthetic Pastel Tints
    cards_data = [
        ("TOTAL COURSES", "26", "6 NEP Categories", 0.02, "#EFF6FF", "#BFDBFE", "#1E40AF", "#2563EB"),
        ("FACULTY ROSTER", "20", "Workload Capped (<=4h)", 0.265, "#F0FDFA", "#99F6E4", "#0F766E", "#0D9488"),
        ("CLASSROOMS & LABS", "14", "945 Total Capacity", 0.51, "#FAF5FF", "#E9D5FF", "#6B21A8", "#7C3AED"),
        ("STUDENT GROUPS", "10", "410 Enrolled Students", 0.755, "#F0FDF4", "#BBF7D0", "#166534", "#10B981")
    ]
    for label, val, sub, x_pos, bg, border, val_c, sub_c in cards_data:
        box = patches.FancyBboxPatch((x_pos, 0.67), 0.225, 0.16, boxstyle="round,pad=0.01", ec=border, fc=bg, lw=1.2)
        ax.add_patch(box)
        ax.text(x_pos + 0.02, 0.79, label, fontsize=8, fontweight='bold', color=val_c)
        ax.text(x_pos + 0.02, 0.72, val, fontsize=20, fontweight='bold', color="#0F172A")
        ax.text(x_pos + 0.02, 0.685, sub, fontsize=7.5, color=sub_c, fontweight='bold')

    # Lower Left Panel: Solver Comparison
    box_l = patches.FancyBboxPatch((0.02, 0.04), 0.46, 0.60, boxstyle="round,pad=0.01", ec="#99F6E4", fc="#FFFFFF", lw=1.2)
    ax.add_patch(box_l)
    ax.text(0.045, 0.59, "Head-to-Head Solver Performance", fontsize=11, fontweight='bold', color="#0F172A")
    ax.text(0.045, 0.56, "Empirical comparison on 89 weekly session allocations", fontsize=8, color="#0D9488", fontweight='bold')

    table_rows = [
        ["Metric", "Baseline CSP", "ML-Assisted CSP"],
        ["Feasibility Status", "OPTIMAL_FEASIBLE", "OPTIMAL_FEASIBLE"],
        ["Completeness", "100.0% (89/89)", "100.0% (89/89)"],
        ["Search Time", "0.472 s", "4.182 s"],
        ["Backtracks", "0 nodes", "0 nodes"],
        ["Forward Prunings", "1,936 prunings", "2,208 prunings (+272)"],
        ["Hard Clashes", "0 (Certified)", "0 (Certified)"]
    ]
    y_t = 0.50
    for r_idx, r in enumerate(table_rows):
        weight = 'bold' if r_idx == 0 else 'normal'
        bg = "#F0FDFA" if r_idx == 0 else ("#FFFFFF" if r_idx % 2 == 1 else "#F8FAFC")
        color = "#0D9488" if r_idx == 0 else "#0F172A"
        t_box = patches.Rectangle((0.038, y_t - 0.015), 0.424, 0.045, ec="#E2E8F0", fc=bg, lw=0.5)
        ax.add_patch(t_box)
        ax.text(0.045, y_t, r[0], fontsize=7.5, fontweight=weight, color=color)
        ax.text(0.21, y_t, r[1], fontsize=7.5, fontweight=weight, color=color)
        ax.text(0.33, y_t, r[2], fontsize=7.5, fontweight=weight, color=color)
        y_t -= 0.05

    # Lower Right Panel: Weekly Grid Preview with Lilac Header & Multi-color Pills
    box_r = patches.FancyBboxPatch((0.51, 0.04), 0.47, 0.60, boxstyle="round,pad=0.01", ec="#E9D5FF", fc="#FFFFFF", lw=1.2)
    ax.add_patch(box_r)
    ax.text(0.535, 0.59, "Study Timetable Grid: B.Tech CSE (GRP_CSE_A)", fontsize=11, fontweight='bold', color="#4C1D95")
    ax.text(0.535, 0.56, "Weekly 5-day slot allocation grid (Certified 0 clashes)", fontsize=8, color="#7C3AED", fontweight='bold')

    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    slots = ["S1 (9-10)", "S2 (10-11)", "S3 (11-12)", "S4 (12-1)", "S5 (2-3)", "S6 (3-4)", "S7 (4-5)"]
    
    grid_x = 0.535
    grid_y = 0.49
    cell_w = 0.06
    cell_h = 0.06

    # Lilac Slot header pills
    for s_idx, sl in enumerate(slots):
        s_box = patches.FancyBboxPatch((grid_x + 0.045 + s_idx * cell_w, grid_y + 0.015), cell_w - 0.005, 0.03, boxstyle="round,pad=0.003", ec="#C4B5FD", fc="#DDD6FE", lw=0.8)
        ax.add_patch(s_box)
        ax.text(grid_x + 0.05 + s_idx * cell_w, grid_y + 0.022, f"Slot {s_idx+1}", fontsize=6.5, fontweight='bold', color="#4C1D95")

    sample_allocs = [
        ["CS101", "CS101*", "MA101", "FREE", "PH101", "FREE", "FREE"],
        ["FREE", "FREE", "MA101", "FREE", "CS102", "CS102", "FREE"],
        ["FREE", "FREE", "EN101", "FREE", "PH102", "PH102", "FREE"],
        ["MA101", "FREE", "FREE", "FREE", "CS101", "FREE", "FREE"],
        ["NEP_MDC", "FREE", "EN101", "FREE", "PH101", "FREE", "FREE"]
    ]
    for d_idx, d in enumerate(days):
        ax.text(grid_x, grid_y - d_idx * cell_h, d, fontsize=7.5, fontweight='bold', color="#0F172A")
        for s_idx in range(7):
            val = sample_allocs[d_idx][s_idx]
            if "CS102" in val or "PH102" in val: # Lab -> Sea Green
                bg_c = "#F0FDF4"; border_c = "#10B981"; text_c = "#14532D"
            elif "CS" in val or "MA" in val: # Core -> Pearl Blue
                bg_c = "#EFF6FF"; border_c = "#3B82F6"; text_c = "#1E40AF"
            elif "NEP" in val: # MDC -> Lilac Purple
                bg_c = "#FAF5FF"; border_c = "#A855F7"; text_c = "#6B21A8"
            elif val != "FREE": # Others -> Aesthetic Teal
                bg_c = "#F0FDFA"; border_c = "#14B8A6"; text_c = "#0F766E"
            else:
                bg_c = "#F8FAFC"; border_c = "#E2E8F0"; text_c = "#94A3B8"
                
            c_box = patches.FancyBboxPatch((grid_x + 0.045 + s_idx * cell_w, grid_y - d_idx * cell_h - 0.015), cell_w - 0.005, cell_h - 0.01, boxstyle="round,pad=0.005", ec=border_c, fc=bg_c, lw=0.9)
            ax.add_patch(c_box)
            ax.text(grid_x + 0.048 + s_idx * cell_w, grid_y - d_idx * cell_h + 0.005, val[:7], fontsize=6, fontweight='bold' if val != "FREE" else 'normal', color=text_c)

    out_path = os.path.join(screenshot_dir, "screenshot_executive_dashboard.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def generate_benchmark_chart():
    """Generates the benchmark comparison chart in aesthetic pearl blue and teal."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    
    # Execution Time Comparison
    algorithms = ['Baseline CSP\n(MRV+Degree+LCV)', 'ML-Assisted CSP\n(MRV+Degree+ML)']
    times = [0.472, 4.182]
    colors = ['#2563EB', '#0D9488'] # Pearl Blue & Aesthetic Teal
    
    bars1 = ax1.bar(algorithms, times, color=colors, width=0.45, edgecolor='#0F172A', linewidth=1)
    ax1.set_ylabel('Search Time (seconds)', fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_title('Execution Search Time Comparison', fontsize=11, fontweight='bold', color='#0F172A', pad=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.3f} s', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax1.set_ylim(0, 5.0)
    
    # Solution Completeness & Validation in Sea Green
    comp = [100.0, 100.0]
    bars2 = ax2.bar(algorithms, comp, color=['#10B981', '#10B981'], width=0.45, edgecolor='#047857', linewidth=1)
    ax2.set_ylabel('Completeness & Feasibility (%)', fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_title('Schedule Completeness & Validation Gate', fontsize=11, fontweight='bold', color='#0F172A', pad=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval - 12, f'{yval:.1f}%\n(0 Violations)', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax2.set_ylim(0, 115)
    
    plt.tight_layout()
    out_path = os.path.join(screenshot_dir, "screenshot_benchmark_comparison.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def generate_ml_metrics_chart():
    """Generates the ML feature importance and confusion matrix figure in vibrant aesthetic pastels."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    
    # Feature Importances in Teal
    features = ['room_capacity_ratio', 'faculty_available', 'room_type_match', 'faculty_daily_load', 'enrolled_students', 'is_peak_slot', 'room_capacity', 'historical_collision_score']
    importances = [0.264, 0.218, 0.185, 0.112, 0.084, 0.056, 0.045, 0.036]
    
    y_pos = np.arange(len(features))
    ax1.barh(y_pos, importances, color='#14B8A6', edgecolor='#0F766E', height=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(features, fontsize=8.5)
    ax1.invert_yaxis()
    ax1.set_xlabel('Gini Importance', fontsize=10, fontweight='bold')
    ax1.set_title('Random Forest Feature Importances', fontsize=11, fontweight='bold', pad=10)
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Confusion Matrix in Lilac & Purple
    cm = np.array([[216, 0], [7, 137]])
    im = ax2.imshow(cm, cmap='Purples', interpolation='nearest')
    ax2.set_title('Test Set Confusion Matrix (Accuracy: 98.06%)', fontsize=11, fontweight='bold', pad=10)
    tick_marks = np.arange(2)
    ax2.set_xticks(tick_marks)
    ax2.set_xticklabels(['Feasible (0)', 'Conflict (1)'], fontsize=9)
    ax2.set_yticks(tick_marks)
    ax2.set_yticklabels(['Feasible (0)', 'Conflict (1)'], fontsize=9)
    ax2.set_ylabel('True Label', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
    
    for i in range(2):
        for j in range(2):
            val = cm[i, j]
            color = "white" if val > 100 else "#4C1D95"
            ax2.text(j, i, str(val), ha="center", va="center", color=color, fontsize=12, fontweight='bold')
            
    plt.tight_layout()
    out_path = os.path.join(screenshot_dir, "screenshot_ml_analytics.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def generate_system_architecture_diagram():
    """Generates the system architecture block diagram in vibrant aesthetic pastel layers."""
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.axis('off')
    
    # 4 Architecture Layers: Pearl Blue, Aesthetic Teal, Lilac, Sea Green
    layers = [
        ("Layer 1: Ingestion & Validation", ["Synthetic Generator (Seed 42)", "7-Sheet Excel / CSV Ingestion", "Referential Integrity Gate"], 0.05, "#EFF6FF", "#2563EB"),
        ("Layer 2: ML Conflict Classifier", ["15 Engineered Features", "Random Forest Classifier", "Leakage-Safe Train/Test Split"], 0.29, "#F0FDFA", "#0D9488"),
        ("Layer 3: Heuristic CSP Engine", ["MRV Variable Ordering", "Degree Tie-Breaking", "LCV / ML-Guided Prioritization", "Forward Checking Pruning"], 0.53, "#FAF5FF", "#7C3AED"),
        ("Layer 4: Verification & UI", ["Independent Hard Validator", "Explainable Diagnostics", "Streamlit Light Mode UI", "Multi-Format Exporters"], 0.77, "#F0FDF4", "#059669")
    ]
    
    for title, items, y_top, bg_c, border_c in layers:
        box = patches.FancyBboxPatch((0.05, 1.0 - y_top - 0.16), 0.90, 0.15, boxstyle="round,pad=0.01", ec=border_c, fc=bg_c, lw=1.5)
        ax.add_patch(box)
        ax.text(0.08, 1.0 - y_top - 0.04, title, fontsize=11, fontweight='bold', color=border_c)
        for i_idx, item in enumerate(items):
            x_item = 0.08 + i_idx * 0.28
            item_box = patches.FancyBboxPatch((x_item, 1.0 - y_top - 0.14), 0.25, 0.08, boxstyle="round,pad=0.005", ec=border_c, fc="#FFFFFF", lw=1.0)
            ax.add_patch(item_box)
            ax.text(x_item + 0.015, 1.0 - y_top - 0.095, item, fontsize=7.5, color="#0F172A", fontweight='500')

    out_path = os.path.join(screenshot_dir, "system_architecture_diagram.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate_dashboard_screenshot()
    generate_benchmark_chart()
    generate_ml_metrics_chart()
    generate_system_architecture_diagram()
    print("All aesthetic screenshots generated successfully.")
