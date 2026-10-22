"""The output contract for your agent."""
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source: str
    line_number: int = Field(ge=1)
    excerpt: str


class DebugReport(BaseModel):
    summary: str
    likely_cause: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)
    suggested_fixes: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
