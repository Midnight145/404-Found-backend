import typing

import pydantic


class HabitInfo(pydantic.BaseModel):
    account_id: int
    habit_name: str
    habit_desc: str
    steps: list[str]
    repeat: bool
    repeat_type: typing.Literal["Daily", "Weekly"]
    reward: str
    reward_frequency: str
