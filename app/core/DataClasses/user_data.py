from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserData:
    name: str
    uuid: UUID
    role: str
    permissions: list[str]
