from typing import List

from src.models.course import Course


def list_courses() -> List[Course]:
    return [
            Course('Programming', 1000000, -1001697197382),
            Course('SMM', 500000)
            ]


def get_course_price(course_name: str) -> int:
    if course_name == 'Programming':
        return 100000
    return 100000


async def get_course_chat_id(course_name: str) -> int:
    if course_name == 'Programming':
        return -1001697197382
    return 0

async def get_course_name_by_chat_id(chat_id: int) -> str:
    if chat_id == -1001697197382:
        return 'Programming'
    return ''

