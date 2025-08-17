from typing import Any, Callable, Dict, Optional, Type

from dependency_injection.scope import Scope


class Registration:
    def __init__(
        self,
        service: Type,
        implementation: Optional[Type],
        scope: Scope,
        tags: Optional[set] = None,
        constructor_kwargs: Optional[Dict[str, Any]] = None,
        factory: Optional[Callable[[Any], Any]] = None,
        factory_kwargs: Optional[Dict[str, Any]] = None,
    ):
        self.service = service
        self.implementation = implementation
        self.scope = scope
        self.tags = tags or set()
        self.constructor_kwargs = constructor_kwargs or {}
        self.factory = factory
        self.factory_kwargs = factory_kwargs or {}

        if not any([self.implementation, self.factory]):
            raise Exception("There must be either an implementation or a factory.")
