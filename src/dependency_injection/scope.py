from enum import Enum


DEFAULT_SCOPE_NAME = "default-scope"

class Scope(Enum):
    TRANSIENT = "transient"
    SCOPED = "scoped"
    SINGLETON = "singleton"
