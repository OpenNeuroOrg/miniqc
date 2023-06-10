import os
import typing as ty
from dataclasses import dataclass

T = ty.TypeVar('T')

CheckResult = ty.NewType('CheckResult', tuple[bool, str])


@dataclass
class CheckList(ty.Generic[T]):
    """Pair a file loader with boolean checks on the loaded file"""

    loader: ty.Callable[[os.PathLike[str]], T]
    checks: list[ty.Callable[[T], CheckResult]]


class FailedCheck(Exception):
    pass
