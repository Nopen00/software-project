"""
플레이어가 수행할 수 있는 액션 정의.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Tuple

from .interface import WorldGateway


class MutablePlayerState(Protocol):
    """플레이어 상태 객체가 충족해야 할 최소 인터페이스."""

    player_id: str
    position: Tuple[int, int]


@dataclass
class ActionContext:
    """액션 실행 시 필요한 컨텍스트."""

    gateway: WorldGateway
    state: MutablePlayerState


class PlayerAction(Protocol):
    """플레이어 액션의 기본 프로토콜."""

    name: str

    def execute(self, ctx: ActionContext) -> None:
        """액션을 실행하고 월드 상태를 갱신합니다."""


@dataclass
class MoveAction:
    """플레이어를 지정한 델타만큼 이동시키는 액션."""

    delta: Tuple[int, int]
    name: str = "move"

    def execute(self, ctx: ActionContext) -> None:
        current = ctx.gateway.get_player_position(ctx.state.player_id)
        new_pos = (current[0] + self.delta[0], current[1] + self.delta[1])
        ctx.gateway.move_player(ctx.state.player_id, new_pos)
        ctx.state.position = new_pos
        ctx.gateway.publish_event(
            {"type": "player_moved", "payload": {"player_id": ctx.state.player_id, "position": new_pos}}
        )

