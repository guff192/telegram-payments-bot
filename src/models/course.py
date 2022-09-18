from typing import Optional

from dataclasses import dataclass


@dataclass
class Course:
    name: str
    price: float
    chat_id: Optional[int] = None

