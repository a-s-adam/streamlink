"""Jobs router for background task management."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from ..celery_app import celery_app

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{task_id}")
async def get_job_status(task_id: str):
    """Get the status of a background job."""
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        response = {
            "task_id": task_id,
            "status": task_result.state,
            "ready": task_result.ready()
        }
        
        if task_result.ready():
            if task_result.successful():
                response["result"] = task_result.result
            else:
                response["error"] = str(task_result.info)
        else:
            response["meta"] = task_result.info
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting job status: {str(e)}"
        )


@router.get("/")
async def list_jobs():
    """List recent jobs (limited functionality in Celery)."""
    try:
        # Note: Celery doesn't provide a simple way to list all tasks
        # This is a basic implementation that shows active tasks
        active_tasks = celery_app.control.inspect().active()
        
        if not active_tasks:
            return {"active_jobs": []}
        
        jobs = []
        for worker, tasks in active_tasks.items():
            for task in tasks:
                jobs.append({
                    "task_id": task["id"],
                    "name": task["name"],
                    "worker": worker,
                    "started": task.get("time_start"),
                    "args": task.get("args", []),
                    "kwargs": task.get("kwargs", {})
                })
        
        return {"active_jobs": jobs}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing jobs: {str(e)}"
        )


@router.delete("/{task_id}")
async def cancel_job(task_id: str):
    """Cancel a running job."""
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.ready():
            return {"message": "Job already completed, cannot cancel"}
        
        # Revoke the task
        celery_app.control.revoke(task_id, terminate=True)
        
        return {"message": f"Job {task_id} cancelled successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cancelling job: {str(e)}"
        )


@router.get("/stats/overview")
async def get_job_stats():
    """Get overview statistics about jobs."""
    try:
        inspect = celery_app.control.inspect()
        
        # Get various statistics
        active = inspect.active()
        reserved = inspect.reserved()
        revoked = inspect.revoked()
        scheduled = inspect.scheduled()
        
        # Count tasks by status
        active_count = sum(len(tasks) for tasks in (active or {}).values())
        reserved_count = sum(len(tasks) for tasks in (reserved or {}).values())
        revoked_count = sum(len(tasks) for tasks in (revoked or {}).values())
        scheduled_count = sum(len(tasks) for tasks in (scheduled or {}).values())
        
        return {
            "active_jobs": active_count,
            "reserved_jobs": reserved_count,
            "revoked_jobs": revoked_count,
            "scheduled_jobs": scheduled_count,
            "total_jobs": active_count + reserved_count + revoked_count + scheduled_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting job stats: {str(e)}"
        )


@router.post("/{task_id}/retry")
async def retry_job(task_id: str):
    """Retry a failed job."""
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if not task_result.ready():
            return {"message": "Job is still running, cannot retry"}
        
        if task_result.successful():
            return {"message": "Job was successful, no need to retry"}
        
        # Get the original task
        original_task = task_result.info
        if not original_task:
            return {"message": "No original task info available for retry"}
        
        # Retry the task
        new_task = celery_app.send_task(
            original_task.get("name", "unknown"),
            args=original_task.get("args", []),
            kwargs=original_task.get("kwargs", {})
        )
        
        return {
            "message": "Job retry initiated",
            "new_task_id": new_task.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrying job: {str(e)}"
        )
