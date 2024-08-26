from abc import ABC
from pydantic import BaseModel


class BaseMpicOrchestrationParameters(BaseModel, ABC):
    perspective_count: int
    quorum_count: int


class MpicRequestOrchestrationParameters(BaseMpicOrchestrationParameters):
    domain_or_ip_target: str
    max_attempts: int | None = None
    perspectives: list[str] | None = None  # for diagnostic purposes


class MpicEffectiveOrchestrationParameters(BaseMpicOrchestrationParameters):
    attempt_count: int | None = 1

