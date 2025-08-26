"""
Database models and schema definitions for Task Reminder System.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(Enum):
    """Task status options."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class Task:
    """Task model representing a single task."""
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    created_at: str = ""

    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'dueDate': self.due_date,
            'priority': self.priority,
            'status': self.status,
            'createdAt': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create task from dictionary."""
        priority = data.get('priority', 'medium')
        if isinstance(priority, Priority):
            priority = priority.value
        if not validate_priority(priority):
            priority = 'medium'

        status = data.get('status', 'pending')
        if isinstance(status, Status):
            status = status.value
        if not validate_status(status):
            status = 'pending'

        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description'),
            due_date=data.get('dueDate'),
            priority=priority,
            status=status,
            created_at=data.get('createdAt', '')
        )
    
    @classmethod
    def from_db_row(cls, row) -> 'Task':
        """Create task from database row."""
        priority = row['priority']
        if not validate_priority(priority):
            priority = 'low'

        status = row['status']
        if not validate_status(status):
            status = 'pending'

        return cls(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            due_date=row['due_date'],
            priority=priority,
            status=status,
            created_at=row['created_at']
        )

class TaskSchema:
    """Database schema definitions."""
    
    CREATE_TASKS_TABLE = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT NOT NULL CHECK(priority IN ('low','medium','high')) DEFAULT 'medium',
            status TEXT NOT NULL CHECK(status IN ('pending','in_progress','completed')) DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    '''
    
    @classmethod
    def get_all_schemas(cls) -> List[str]:
        """Get all CREATE TABLE statements."""
        return [cls.CREATE_TASKS_TABLE]

# Utility functions
def format_datetime(dt: datetime) -> str:
    """Format datetime in readable format (e.g., '21 August 2025, 3:45pm')."""
    hour = dt.hour % 12 or 12
    am_pm = 'am' if dt.hour < 12 else 'pm'
    minute = dt.minute
    return f"{dt.day} {dt.strftime('%B %Y')}, {hour}:{minute:02d}{am_pm}"

def get_current_timestamp() -> str:
    """Get current timestamp in the application's format."""
    return format_datetime(datetime.now())


def validate_task_description(description: str) -> bool:
    """
    Validate that the description is non-empty and not just whitespace.
    """
    return bool(description and description.strip())

def validate_priority(priority: str) -> bool:
    """
    Validate that priority is one of allowed values.
    """
    allowed_priorities = {"Low", "Medium", "High"}
    return priority in allowed_priorities

# Validation functions
def validate_priority(priority: str) -> bool:
    return priority in [p.value for p in Priority]

def validate_status(status: str) -> bool:
    return status in [s.value for s in Status]

def validate_task_title(title: str) -> tuple[bool, str]:
    if not title or not title.strip():
        return False, "Task title cannot be empty"
    if len(title.strip()) < 3:
        return False, "Task title must be at least 3 characters long"
    if len(title.strip()) > 100:
        return False, "Task title must be less than 100 characters"
    return True, ""
