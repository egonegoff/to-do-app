from dataclasses import dataclass

@dataclass
class TodoDataclass:
    id: int
    text: str
    done: bool = False
