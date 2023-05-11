from pydantic import Field

from .base import Base


class FullName(Base):
    ru: str = Field(alias='RU')
    tj: str = Field(alias='TJ')


class Faculty(FullName):
    ...


class Speciality(FullName):
    ...


class Profile(Base):
    id: int = Field(alias='RecordBookNumber')
    full_name: FullName = Field(alias='FullName')
    faculty: Faculty = Field(alias="Faculty")
    course: int = Field(alias='Course')
    training_period: int = Field(alias='TrainingPeriod')
    level: str = Field(alias="TrainingLevel")
    entrance_year: str = Field(alias='YearUniversityEntrance')
    speciality_code: str = Field(alias='CodeSpecialty')
    group: str = Field(alias="Group")
    speciality: FullName = Field(alias='Specialty')
