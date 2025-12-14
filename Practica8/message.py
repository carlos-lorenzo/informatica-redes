from dataclasses import dataclass, field


@dataclass
class Message:
    sender_id: str
    sender_username: str
    content: str