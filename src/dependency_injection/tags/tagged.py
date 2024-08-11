from typing import Type, Generic, TypeVar

T = TypeVar("T")


class Tagged(Generic[T]):
    def __init__(self, tag: Type[T]):
        self.tag = tag

    @classmethod
    def __class_getitem__(cls, item: Type[T]) -> Type["Tagged"]:
        return type(f"Tagged_{item.__name__}", (cls,), {"tag": item})
