from typing import Any, Callable, Dict, Optional, Type

from dependency_injection.scope import Scope


class Registration:
    def __init__(
        self,
        dependency: Type,
        implementation: Optional[Type],
        scope: Scope,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
        factory: Optional[Callable[[Any], Any]] = None,
        factory_args: Optional[Dict[str, Any]] = None,
    ):
        self.dependency = dependency
        self.implementation = implementation
        self.scope = scope
        self.tags = tags or set()
        self.constructor_args = constructor_args or {}
        self.factory = factory
        self.factory_args = factory_args or {}

        if not any([self.implementation, self.factory]):
            raise Exception("There must be either an implementation or a factory.")
