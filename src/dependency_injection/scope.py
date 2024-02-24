from enum import Enum

class Scope(Enum):
    TRANSIENT = "transient"
    SCOPED = "scoped"
    SINGLETON = "singleton"
