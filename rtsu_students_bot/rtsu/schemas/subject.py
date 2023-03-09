from typing import List
from pydantic import Field

from .base import Base


class SubjectName(Base):
    ru: str = Field(alias='RU')
    tj: str = Field(alias='TJ')


class TeacherName(SubjectName):
    ...


class RatingWeek(Base):
    number: int = Field(alias='WeekNumber')
    point: float = Field(alias='Point')
    max_point: int = Field(alias='MaxPoint')
    is_current_week: bool = Field(alias='IsCurrentWeek')


class Subject(Base):
    id: int = Field(alias='SubjectID')
    name: SubjectName = Field(alias='SubjectName')
    first_rating_weeks: List[RatingWeek] = Field(alias='FirstRatingWeeks')
    second_rating_weeks: List[RatingWeek] = Field(alias='SecondRatingWeeks')
    exam_point: float = Field(alias='ExamPoint')
    total_point: float = Field(alias='TotalPoint')
    admin_point: float = Field(alias='AdminPoint')
    mark: str = Field(alias="Mark")
