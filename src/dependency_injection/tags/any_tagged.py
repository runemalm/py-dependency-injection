from typing import Type, Generic, TypeVar, Tuple, Union, Set

T = TypeVar("T")


class AnyTagged(Generic[T]):
    def __init__(self, tags: Union[Tuple[Type[T], ...], Type[T]]):
        if not isinstance(tags, tuple):
            tags = (tags,)
        self.tags: Set[Type[T]] = set(tags)

    @classmethod
    def __class_getitem__(
        cls, item: Union[Type[T], Tuple[Type[T], ...]]
    ) -> Type["AnyTagged"]:
        if not isinstance(item, tuple):
            item = (item,)
        return type(
            f'AnyTagged_{"_".join([t.__name__ for t in item])}',
            (cls,),
            {"tags": set(item)},
        )
