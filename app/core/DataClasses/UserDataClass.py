from dataclasses import dataclass


@dataclass
class UserData:
    name: str
    uuid: str
    role: str
    permission: list[str]
