from typing import Type, Tuple, Set, Union


class AllTagged:
    def __init__(self, tags: Tuple[Type, ...]):
        self.tags: Set[Type] = set(tags)

    @classmethod
    def __class_getitem__(cls, item: Union[Type, Tuple[Type, ...]]) -> "AllTagged":
        if not isinstance(item, tuple):
            item = (item,)
        return cls(item)
