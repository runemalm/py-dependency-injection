from typing import Generic, Set, Tuple, Type, TypeVar, Union

T = TypeVar("T")


class AllTagged(Generic[T]):
    def __init__(self, tags: Tuple[Type[T], ...]):
        self.tags: Set[Type[T]] = set(tags)

    @classmethod
    def __class_getitem__(
        cls, item: Union[Type[T], Tuple[Type[T], ...]]
    ) -> Type["AllTagged"]:
        if not isinstance(item, tuple):
            item = (item,)
        return type(
            f'AllTagged_{"_".join([t.__name__ for t in item])}',
            (cls,),
            {"tags": set(item)},
        )
