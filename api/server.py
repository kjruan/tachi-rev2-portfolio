"""
FastAPI Server for Rev2 Portfolio Management
Provides API endpoints for integration with tachi-cli main application
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import uuid
from datetime import datetime

from config import APIConfig
from crews.portfolio_crew import PortfolioAnalysisCrew

# Initialize FastAPI app
app = FastAPI(
    title="Rev2 Portfolio Management API",
    description="Multi-agent AI portfolio analysis powered by Claude",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=APIConfig.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize crew (shared instance)
crew = PortfolioAnalysisCrew(verbose=False)

# Task storage (in-memory for now)
analysis_tasks = {}


# Pydantic Models
class PortfolioRequest(BaseModel):
    """Portfolio analysis request"""
    portfolio: Dict[str, float] = Field(..., description="Map of ticker to shares")
    description: Optional[str] = Field(None, description="Optional portfolio description")


class StockRequest(BaseModel):
    """Single stock analysis request"""
    ticker: str = Field(..., description="Stock ticker symbol")


class TaskResponse(BaseModel):
    """Task creation response"""
    task_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    """Task status response"""
    task_id: str
    status: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Rev2 Portfolio Management API",
        "version": "0.1.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "analyze_portfolio": "/api/v1/portfolio/analyze",
            "analyze_stock": "/api/v1/stock/analyze",
            "task_status": "/api/v1/tasks/{task_id}",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": {
            "data_fetcher": "ready",
            "market_analyst": "ready",
            "sentiment_analyst": "ready",
            "risk_manager": "ready",
            "strategist": "ready",
        },
    }


@app.post("/api/v1/portfolio/analyze", response_model=TaskResponse)
async def analyze_portfolio(
    request: PortfolioRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze a portfolio using multi-agent system.
    Returns immediately with task_id for async processing.
    """
    # Generate task ID
    task_id = str(uuid.uuid4())

    # Store task info
    analysis_tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "request": request.dict(),
        "result": None,
        "error": None,
    }

    # Run analysis in background
    background_tasks.add_task(
        run_portfolio_analysis,
        task_id,
        request.portfolio
    )

    return TaskResponse(
        task_id=task_id,
        status="pending",
        message=f"Portfolio analysis started for {len(request.portfolio)} positions"
    )


@app.post("/api/v1/stock/analyze", response_model=TaskResponse)
async def analyze_stock(
    request: StockRequest,
    background_tasks: BackgroundTasks
):
    """
    Quick analysis of a single stock.
    Returns immediately with task_id for async processing.
    """
    # Generate task ID
    task_id = str(uuid.uuid4())

    # Store task info
    analysis_tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "request": request.dict(),
        "result": None,
        "error": None,
    }

    # Run analysis in background
    background_tasks.add_task(
        run_stock_analysis,
        task_id,
        request.ticker
    )

    return TaskResponse(
        task_id=task_id,
        status="pending",
        message=f"Stock analysis started for {request.ticker}"
    )


@app.get("/api/v1/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get status of an analysis task"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = analysis_tasks[task_id]

    return TaskStatusResponse(
        task_id=task["task_id"],
        status=task["status"],
        created_at=task["created_at"],
        completed_at=task.get("completed_at"),
        result=task.get("result"),
        error=task.get("error"),
    )


@app.get("/api/v1/tasks")
async def list_tasks(limit: int = 10):
    """List recent analysis tasks"""
    tasks = sorted(
        analysis_tasks.values(),
        key=lambda x: x["created_at"],
        reverse=True
    )[:limit]

    return {
        "count": len(analysis_tasks),
        "tasks": tasks,
    }


@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del analysis_tasks[task_id]

    return {"message": "Task deleted successfully"}


# Background task functions

async def run_portfolio_analysis(task_id: str, portfolio: Dict[str, float]):
    """Run portfolio analysis in background"""
    try:
        analysis_tasks[task_id]["status"] = "running"

        # Run analysis
        result = crew.analyze_portfolio(portfolio)

        # Update task with results
        analysis_tasks[task_id].update({
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "result": result,
        })

    except Exception as e:
        analysis_tasks[task_id].update({
            "status": "failed",
            "completed_at": datetime.now().isoformat(),
            "error": str(e),
        })


async def run_stock_analysis(task_id: str, ticker: str):
    """Run stock analysis in background"""
    try:
        analysis_tasks[task_id]["status"] = "running"

        # Run analysis
        result = crew.quick_analysis(ticker)

        # Update task with results
        analysis_tasks[task_id].update({
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "result": result,
        })

    except Exception as e:
        analysis_tasks[task_id].update({
            "status": "failed",
            "completed_at": datetime.now().isoformat(),
            "error": str(e),
        })


# Run server
if __name__ == "__main__":
    import uvicorn

    print(f"Starting Rev2 API Server on {APIConfig.HOST}:{APIConfig.PORT}")
    print(f"API Documentation: http://{APIConfig.HOST}:{APIConfig.PORT}/docs")

    uvicorn.run(
        app,
        host=APIConfig.HOST,
        port=APIConfig.PORT,
        log_level="info",
    )
