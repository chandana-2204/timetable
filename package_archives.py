"""
Archive Packaging Utility
Creates:
1. Individual UMS Submission ZIP: K3P25IL_12511912.zip (Strictly < 5 MB)
2. Complete Source Bundle ZIP: NEP2020_Timetable_Complete_Source.zip
"""

import os
import zipfile

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sub_dir = os.path.join(base_dir, "submission")
os.makedirs(sub_dir, exist_ok=True)

def create_ums_zip():
    zip_path = os.path.join(sub_dir, "K3P25IL_12511912.zip")
    files_to_include = [
        ("docs/NEP2020_Timetable_Project_Report.docx", "NEP2020_Timetable_Project_Report.docx"),
        ("docs/NEP2020_Timetable_Project_Report.pdf", "NEP2020_Timetable_Project_Report.pdf"),
        ("presentation/NEP2020_Timetable_Presentation.pptx", "NEP2020_Timetable_Presentation.pptx"),
        ("PROJECTLINKS.txt", "PROJECTLINKS.txt"),
        ("LINKS.txt", "LINKS.txt"),
        ("README.md", "README.md"),
    ]
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for rel_src, arc_name in files_to_include:
            src_full = os.path.join(base_dir, rel_src)
            if os.path.exists(src_full):
                zf.write(src_full, arc_name)
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[Packaging] Created UMS ZIP: {zip_path} ({size_mb:.2f} MB)")
    assert size_mb < 5.0, f"Error: UMS ZIP exceeds 5 MB ({size_mb:.2f} MB)"

def create_full_source_zip():
    zip_path = os.path.join(sub_dir, "NEP2020_Timetable_Complete_Source.zip")
    exclude_dirs = {'.venv', 'venv', '__pycache__', '.pytest_cache', '.git', '.vscode'}
    exclude_extensions = {'.pyc', '.pyo', '.pyd', '.log'}
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in exclude_extensions):
                    continue
                # Skip existing zip archives in submission to prevent nesting
                if file.endswith('.zip'):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zf.write(full_path, os.path.join("timetable_planner", rel_path))
                
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[Packaging] Created Full Source Bundle: {zip_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_ums_zip()
    create_full_source_zip()
