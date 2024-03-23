from typing import Any, Dict, Optional, Type

from dependency_injection.scope import Scope


class Registration():

    def __init__(self, dependency: Type, implementation: Type, scope: Scope, tags: Optional[set] = None, constructor_args: Optional[Dict[str, Any]] = None):
        self.dependency = dependency
        self.implementation = implementation
        self.scope = scope
        self.tags = tags or set()
        self.constructor_args = constructor_args or {}
