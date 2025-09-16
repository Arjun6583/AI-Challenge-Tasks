from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import file_routes, text_routes, analysis_routes, llm_service, response_feedback

app = FastAPI(title="File & Text Upload API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_routes.router)
app.include_router(file_routes.router)
app.include_router(analysis_routes.router)
app.include_router(llm_service.router) 
app.include_router(response_feedback.router)

