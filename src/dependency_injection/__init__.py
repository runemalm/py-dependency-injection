from .container import DependencyContainer
from .decorator import inject
from .tags.tagged import Tagged
from .tags.any_tagged import AnyTagged
from .tags.all_tagged import AllTagged
from .version import __version__

__all__ = [
    "DependencyContainer",
    "inject",
    "Tagged",
    "AnyTagged",
    "AllTagged",
    "__version__",
]
