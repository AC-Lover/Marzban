from datetime import datetime as dt
from typing import Optional

from app import telegram
from app.db import Session, create_notification_reminder
from app.db.models import UserStatus
from app.models.admin import Admin
from app.models.user import ReminderType, UserResponse
from app.utils.notification import (ActionType, ReachedDaysLeft,
                                    ReachedUsagePercent, UserCreated,
                                    UserDeleted, UserDisabled, UserEnabled,
                                    UserExpired, UserLimited, UserUpdated,
                                    notify)


def status_change(username: str, status: UserStatus, user: UserResponse, by: Optional[Admin] = None) -> None:
    try:
        telegram.report_status_change(username, status)
    except Exception:
        pass
    if status == UserStatus.limited:
        notify(UserLimited(username=username, action=ActionType.user_limited, user=user))
    elif status == UserStatus.expired:
        notify(UserExpired(username=username, action=ActionType.user_expired, user=user))
    elif status == UserStatus.disabled:
        notify(UserDisabled(username=username, action=ActionType.user_disabled, user=user, by=by))
    elif status == UserStatus.active:
        notify(UserEnabled(username=username, action=ActionType.user_enabled, user=user, by=by))


def user_created(user: UserResponse, by: Admin) -> None:
    try:
        telegram.report_new_user(
            user_id=user.id,
            username=user.username,
            by=by.username,
            expire_date=user.expire,
            usage=user.data_limit,
            proxies=user.proxies,
        )
    except Exception:
        pass
    notify(UserCreated(username=user.username, action=ActionType.user_created, by=by, user=user))


def user_updated(user: UserResponse, by: Admin) -> None:
    try:
        telegram.report_user_modification(
            username=user.username,
            expire_date=user.expire,
            usage=user.data_limit,
            proxies=user.proxies,
            by=by.username,
        )
    except Exception:
        pass
    notify(UserUpdated(username=user.username, action=ActionType.user_updated, by=by, user=user))


def user_deleted(username: str, by: Admin) -> None:
    try:
        telegram.report_user_deletion(username=username, by=by.username)
    except Exception:
        pass
    notify(UserDeleted(username=username, action=ActionType.user_deleted, by=by))


def data_usage_percent_reached(
        db: Session, percent: float, user: UserResponse, user_id: int, expire: Optional[int] = None) -> None:
    notify(ReachedUsagePercent(username=user.username, user=user, used_percent=percent))
    create_notification_reminder(db, ReminderType.data_usage,
                                 expires_at=dt.utcfromtimestamp(expire) if expire else None, user_id=user_id)


def expire_days_reached(db: Session, days: int, user: UserResponse, user_id: int, expire: int) -> None:
    notify(ReachedDaysLeft(username=user.username, user=user, days_left=days))
    create_notification_reminder(
        db, ReminderType.expiration_date, expires_at=dt.utcfromtimestamp(expire),
        user_id=user_id)
