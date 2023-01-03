from typing import Union

from aiogram.types import User

from db_api.db_services import get_attempts_number, set_user_ban


def rate_limit(limit: int, key=None):
    """Decorator for configuring rate limit and key in different functions."""

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


def is_banned(key: bool = False):
    def decorator(func):
        if key:
            setattr(func, 'key', key)
        return func

    return decorator


async def is_user_banned(user: User) -> Union[bool, int]:
    """Проверяет сколько попыток ввода кода было и если больше 5 - банит юзера"""
    attempts = await get_attempts_number(user)
    if attempts >= 5:
        await set_user_ban(user)
        return True
    return False
