"""
플레이어 입력을 관리하고 액션을 실행하는 컨트롤러.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Iterable, Tuple

from .actions import ActionContext, PlayerAction
from .interface import WorldGateway


@dataclass
class PlayerState:
    """플레이어의 핵심 상태 정보를 보관합니다."""

    player_id: str
    position: Tuple[int, int] = (0, 0)
    inventory: list[str] = field(default_factory=list)


@dataclass
class PlayerController:
    """플레이어 액션 큐를 처리하는 컨트롤러."""

    state: PlayerState
    gateway: WorldGateway
    _queue: Deque[PlayerAction] = field(default_factory=deque)

    def enqueue(self, action: PlayerAction) -> None:
        """새로운 액션을 큐에 추가합니다."""
        self._queue.append(action)

    def enqueue_many(self, actions: Iterable[PlayerAction]) -> None:
        """여러 액션을 한 번에 큐에 추가합니다."""
        for action in actions:
            self.enqueue(action)

    def tick(self) -> None:
        """시뮬레이션 틱마다 호출되어 큐의 액션을 하나 실행합니다."""
        if not self._queue:
            return

        action = self._queue.popleft()
        context = ActionContext(gateway=self.gateway, state=self.state)
        action.execute(context)

    def clear(self) -> None:
        """남아있는 액션을 모두 제거합니다."""
        self._queue.clear()

