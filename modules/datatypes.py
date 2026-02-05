import typing
from typing import List, Optional, Any

import pydantic


# Backend datatypes migrated to match the frontend model shapes.
# These keep the original class names (UserInfo, BuildHabitInfo, BreakHabitInfo,
# HabitInfo) so existing backend modules that import them do not need to be
# updated. Field names and types follow the frontend `src/models/index.js`.


class UserInfo(pydantic.BaseModel):
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    # password fields are optional on responses but accepted at creation time
    password: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = "user"
    createdAt: Optional[typing.Union[int, str]] = None
    # keep a permissive `type` since frontend uses a variety of values
    type: Optional[str] = None
    theme: Optional[str] = "pink"
    profilePic: Optional[str] = ""
    stats: Optional[dict] = {}
    code: Optional[str] = None
    # allow arbitrary extra data
    meta: Optional[dict] = {}


class BuildHabitInfo(pydantic.BaseModel):
    id: Optional[int] = None
    account_id: Optional[int] = None
    goal: str = ""
    cue: str = ""
    steps: List[str] = []


class BreakHabitInfo(pydantic.BaseModel):
    id: Optional[int] = None
    account_id: Optional[int] = None
    habit: str = ""
    replacements: List[str] = []
    microSteps: List[str] = []
    savedOn: Optional[typing.Union[int, str]] = None


class HabitInfo(pydantic.BaseModel):
    # Represents a formed habit in the system (frontend's FormedHabit)
    id: Optional[int] = None
    userId: Optional[int] = None
    title: str = ""
    type: str = "build"
    createdAt: Optional[typing.Union[int, str]] = None
    details: Optional[Any] = None
    completedAt: Optional[typing.Union[int, str]] = None
    meta: Optional[dict] = {}


class FormedHabitInfo(pydantic.BaseModel):
    """Alias-like model for frontend FormedHabit objects."""
    id: Optional[typing.Union[int, str]] = None
    userId: Optional[typing.Union[int, str]] = None
    title: str = ""
    type: str = "build"
    createdAt: Optional[typing.Union[int, str]] = None
    details: Optional[typing.Any] = None
    completedAt: Optional[typing.Union[int, str]] = None
    meta: Optional[dict] = {}


class TaskInfo(pydantic.BaseModel):
    """Backend model representing a frontend Task."""
    id: Optional[typing.Union[int, str]] = None
    assigneeId: Optional[typing.Union[int, str]] = None
    assigneeName: Optional[str] = ""
    title: str = ""
    notes: Optional[str] = ""
    taskType: Optional[str] = "simple"
    steps: List[str] = []
    habitToBreak: Optional[str] = ""
    replacements: List[str] = []
    frequency: Optional[typing.Any] = None
    streak: int = 0
    completedDates: List[str] = []
    status: str = "pending"
    createdAt: Optional[typing.Union[int, str]] = None
    createdById: Optional[typing.Union[int, str]] = None
    createdByName: Optional[str] = None
    createdByRole: Optional[str] = None
    needsApproval: bool = False
    targetType: Optional[str] = None
    targetName: Optional[str] = None
    meta: Optional[dict] = {}