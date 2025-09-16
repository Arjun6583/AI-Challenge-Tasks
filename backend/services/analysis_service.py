from pathlib import Path
from services.text_handler import save_text_block

def generate_report(text_dir: Path, file_dir: Path, report_dir: Path):
    report_content = f"""
    📊 **Analysis Report**
    - Total uploaded text files: {len(list(text_dir.glob("*.txt")))}
    - Total uploaded files: {len(list(file_dir.glob("*")))}
    - Report generated successfully ✅
    """
    report_path = save_text_block(report_content, report_dir, ext=".md")
    return report_content, report_path

    