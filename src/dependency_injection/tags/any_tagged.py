from typing import Type, Tuple, Set, Union


class AnyTagged:
    def __init__(self, tags: Union[Tuple[Type, ...], Type]):
        if not isinstance(tags, tuple):
            tags = (tags,)
        self.tags: Set[Type] = set(tags)

    @classmethod
    def __class_getitem__(cls, item: Union[Type, Tuple[Type, ...]]) -> "AnyTagged":
        return cls(item)
