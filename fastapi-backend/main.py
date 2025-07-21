#!/usr/bin/env python3
"""
CodeFlowOps Test FastAPI Application
====================================

A simple FastAPI application for testing CodeFlowOps deployment capabilities.
This application includes:
- REST API endpoints
- Database integration
- Authentication
- Environment configuration
- Health checks
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn
from datetime import datetime, timedelta
import jwt

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="CodeFlowOps Test API",
    description="A test FastAPI application for CodeFlowOps deployment testing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    completed: bool = False
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

# In-memory data store (for testing purposes)
tasks_db = []
users_db = []
task_id_counter = 1
user_id_counter = 1

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CodeFlowOps Test FastAPI Application",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "tasks": "/api/v1/tasks",
            "users": "/api/v1/users",
            "auth": "/api/v1/auth"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": "connected",  # In real app, check actual DB
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/v1/status")
async def api_status():
    """API status with detailed information"""
    return {
        "api_version": "1.0.0",
        "fastapi_version": "0.104.1",
        "python_version": "3.11+",
        "features": [
            "REST API endpoints",
            "JWT authentication",
            "CORS support",
            "Database integration ready",
            "Environment configuration",
            "Health monitoring"
        ],
        "endpoints_count": len(app.routes),
        "uptime": "Running",
        "last_restart": datetime.utcnow().isoformat()
    }

# Task Management API
@app.post("/api/v1/tasks", response_model=Task)
async def create_task(task: TaskCreate, username: str = Depends(verify_token)):
    """Create a new task"""
    global task_id_counter
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        priority=task.priority,
        created_at=datetime.utcnow()
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task

@app.get("/api/v1/tasks", response_model=List[Task])
async def get_tasks(username: str = Depends(verify_token)):
    """Get all tasks"""
    return tasks_db

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, username: str = Depends(verify_token)):
    """Get a specific task"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/v1/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate, username: str = Depends(verify_token)):
    """Update a task"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority
    return task

@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: int, username: str = Depends(verify_token)):
    """Delete a task"""
    global tasks_db
    tasks_db = [t for t in tasks_db if t.id != task_id]
    return {"message": "Task deleted successfully"}

@app.patch("/api/v1/tasks/{task_id}/complete")
async def complete_task(task_id: int, username: str = Depends(verify_token)):
    """Mark a task as completed"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    return task

# User Management API
@app.post("/api/v1/users", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    global user_id_counter
    
    # Check if user already exists
    if any(u.username == user.username for u in users_db):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        created_at=datetime.utcnow()
    )
    users_db.append(new_user)
    user_id_counter += 1
    return new_user

@app.get("/api/v1/users", response_model=List[User])
async def get_users():
    """Get all users"""
    return users_db

# Authentication API
@app.post("/api/v1/auth/login", response_model=Token)
async def login(username: str, password: str):
    """Login and get access token"""
    # Simple authentication (in production, verify password hash)
    user = next((u for u in users_db if u.username == username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me", response_model=User)
async def get_current_user(username: str = Depends(verify_token)):
    """Get current user information"""
    user = next((u for u in users_db if u.username == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Analytics endpoint
@app.get("/api/v1/analytics")
async def get_analytics():
    """Get application analytics"""
    return {
        "total_tasks": len(tasks_db),
        "completed_tasks": len([t for t in tasks_db if t.completed]),
        "total_users": len(users_db),
        "api_calls": "tracked",
        "average_response_time": "< 50ms",
        "uptime": "99.9%",
        "last_updated": datetime.utcnow().isoformat()
    }

# Environment info endpoint
@app.get("/api/v1/environment")
async def get_environment():
    """Get environment information"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_url": os.getenv("DATABASE_URL", "sqlite:///./test.db"),
        "secret_key_set": bool(os.getenv("SECRET_KEY")),
        "cors_enabled": True,
        "features_enabled": {
            "authentication": True,
            "task_management": True,
            "user_management": True,
            "analytics": True
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )
