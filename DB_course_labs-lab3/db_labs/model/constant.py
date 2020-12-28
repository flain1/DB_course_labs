from enum import unique, Enum


@unique
class RecruitmentStatus(Enum):
    rejected = "rejected"
    in_progress = "in_progress"
