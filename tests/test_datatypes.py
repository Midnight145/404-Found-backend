import pytest
from pydantic import ValidationError

from modules.datatypes import HabitInfo, UserInfo


def test_habitinfo_validation_success():
    info = HabitInfo(
        account_id=1,
        habit_name="Exercise",
        habit_desc="Do morning exercise",
        steps=["stretch", "run"],
        repeat=True,
        repeat_type="Daily",
        reward="Badge",
        reward_frequency="Weekly",
    )

    assert info.account_id == 1
    assert info.steps == ["stretch", "run"]
    assert info.repeat_type == "Daily"


def test_habitinfo_invalid_repeat_type():
    with pytest.raises(ValidationError):
        HabitInfo(
            account_id=1,
            habit_name="X",
            habit_desc="Y",
            steps=["a"],
            repeat=False,
            repeat_type="Monthly",  # invalid literal
            reward="r",
            reward_frequency="f",
        )


def test_userinfo_validation_success():
    u = UserInfo(username="bob", email="bob@example.com", password_hash="hash")
    assert u.username == "bob"
