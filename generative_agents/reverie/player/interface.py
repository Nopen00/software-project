"""
시뮬레이션 엔진과 플레이어 모듈 사이의 추상 인터페이스 정의.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Protocol, Tuple


class WorldEvent(Protocol):
    """월드 내에서 발생한 이벤트를 표현하기 위한 최소 프로토콜."""

    type: str
    payload: dict


class WorldGateway(ABC):
    """플레이어가 월드와 상호작용하기 위해 필요한 최소 API 집합."""

    @abstractmethod
    def get_player_position(self, player_id: str) -> Tuple[int, int]:
        """플레이어의 현재 좌표를 반환합니다."""

    @abstractmethod
    def move_player(self, player_id: str, new_pos: Tuple[int, int]) -> None:
        """플레이어를 새로운 좌표로 이동시킵니다."""

    @abstractmethod
    def publish_event(self, event: WorldEvent) -> None:
        """월드 전역 이벤트 스트림에 이벤트를 발행합니다."""

    @abstractmethod
    def nearby_entities(self, player_id: str, radius: int = 1) -> Iterable[dict]:
        """플레이어 주변의 엔티티 정보를 반환합니다."""

