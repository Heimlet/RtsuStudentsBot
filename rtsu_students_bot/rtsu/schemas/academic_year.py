from pydantic import Field

from .base import Base


class AcademicYear(Base):
    id: int = Field(alias='ID')
    year: str = Field(alias="AcademicYear")
