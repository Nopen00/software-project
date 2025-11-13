"""
시뮬레이션 복구 전 테스트용 더미 월드 게이트웨이 구현.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple

from .interface import WorldEvent, WorldGateway


@dataclass
class SimpleEvent:
    """WorldEvent 프로토콜을 만족하는 단순 이벤트 구현."""

    type: str
    payload: dict


@dataclass
class MockWorldGateway(WorldGateway):
    """단위 테스트 및 프로토타입용 월드 게이트웨이."""

    positions: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    events: List[WorldEvent] = field(default_factory=list)
    entities: Dict[str, dict] = field(default_factory=dict)

    def get_player_position(self, player_id: str) -> Tuple[int, int]:
        return self.positions.get(player_id, (0, 0))

    def move_player(self, player_id: str, new_pos: Tuple[int, int]) -> None:
        self.positions[player_id] = new_pos

    def publish_event(self, event: WorldEvent) -> None:
        self.events.append(event)

    def nearby_entities(self, player_id: str, radius: int = 1) -> Iterable[dict]:
        origin = self.get_player_position(player_id)
        for entity in self.entities.values():
            pos = entity.get("position", None)
            if pos is None:
                continue
            if abs(pos[0] - origin[0]) <= radius and abs(pos[1] - origin[1]) <= radius:
                yield entity

