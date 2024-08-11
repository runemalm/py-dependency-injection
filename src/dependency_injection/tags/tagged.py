from typing import Type


class Tagged:
    def __init__(self, tag: Type):
        self.tag = tag

    @classmethod
    def __class_getitem__(cls, item: Type) -> "Tagged":
        return cls(item)
