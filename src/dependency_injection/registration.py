from typing import Any, Dict

from dependency_injection.scope import Scope


class Registration():

    def __init__(self, interface, class_, scope: Scope, constructor_args: Dict[str, Any] = None):
        self.interface = interface
        self.class_ = class_
        self.scope = scope
        self.constructor_args = constructor_args or {}
