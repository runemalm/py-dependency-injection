from typing import Any, Dict, Optional, Type

from dependency_injection.scope import Scope


class Registration():

    def __init__(self, dependency: Type, implementation: Type, scope: Scope, constructor_args: Optional[Dict[str, Any]] = None):
        self.dependency = dependency
        self.implementation = implementation
        self.scope = scope
        self.constructor_args = constructor_args or {}
