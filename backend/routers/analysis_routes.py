from fastapi import APIRouter
from pathlib import Path
from services.analysis_service import generate_report

router = APIRouter()

TEXT_DIR = Path("data/texts")
FILE_DIR = Path("data/files")
REPORT_DIR = Path("data/reports")

@router.get("/analysis/")
async def analysis_report():
    report_content, report_path = generate_report(TEXT_DIR, FILE_DIR, REPORT_DIR)
    return {
        "status": "success",
        "report": report_content,
        "path": str(report_path)
    }
