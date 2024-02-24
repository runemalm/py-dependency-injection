from dependency_injection.scope import Scope


class Registration():

    def __init__(self, interface, class_, scope: Scope):
        self.interface = interface
        self.class_ = class_
        self.scope = scope
