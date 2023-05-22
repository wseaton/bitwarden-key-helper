from dataclasses import dataclass
from serde import SerdeSkip, field, serde

from datetime import datetime

from typing import Optional, List


def serializer(cls, o):
    if cls is datetime:
        return o.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        raise SerdeSkip()


def deserializer(cls, o):
    if cls is datetime:
        return datetime.strptime(o, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        raise SerdeSkip()


@serde(serializer=serializer, deserializer=deserializer, rename_all="camelcase")
@dataclass
class Login:
    username: str
    password: str
    totp: Optional[str]
    password_revision_date: Optional[datetime]


@serde(serializer=serializer, deserializer=deserializer, rename_all="camelcase")
@dataclass
class PasswordHistory:
    last_used_date: datetime = field(rename="lastUsedDate")
    password: str


@serde(serializer=serializer, deserializer=deserializer, rename_all="camelcase")
@dataclass
class PasswordEntry:
    _id: str = field(rename="id")
    organization_id: str
    folder_id: str
    _type: int = field(rename="type")
    reprompt: int
    name: str
    notes: Optional[str]
    favorite: bool
    login: Login

    collection_ids: List[str]
    revision_date: datetime
    creation_date: datetime
    deleted_date: Optional[datetime]
    passwordHistory: List[PasswordHistory]
