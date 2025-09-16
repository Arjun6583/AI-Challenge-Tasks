from fastapi import APIRouter, Form
from pathlib import Path
import multiprocessing
from services.llm_service import SimpleLLMService

router = APIRouter()
llm_service = SimpleLLMService()


@router.on_event("startup")
async def startup_event():
    print("LLM Service Router is up and running!")
    llm_service.start()


@router.on_event("shutdown")
async def shutdown_event():
    print("LLM Service Router is shutting down.")
    llm_service.stop()


@router.post("/summarize/")
async def summarize(text: str = Form(...)):
    summary = llm_service.summarize(text)
    print(f"Summary: {summary}")

