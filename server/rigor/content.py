import json
from dataclasses import asdict, dataclass
from typing import Dict, Any


@dataclass
class Content:
    title: str
    body: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))
