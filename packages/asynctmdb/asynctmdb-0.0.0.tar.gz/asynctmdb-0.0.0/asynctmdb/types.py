import abc
from typing import (Generic,
                    T_co)


def method_defined(cls: type,
                   *,
                   method_name: str) -> bool:
    return any(method_name in cls_or_ancestor.__dict__
               for cls_or_ancestor in cls.__mro__)


class AbstractAsyncContextManager(abc.ABC):
    """An abstract base class for async context managers."""

    def __aenter__(self):
        """Return `self` upon entering the runtime context."""
        return self

    @abc.abstractmethod
    def __aexit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
        return None

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is AbstractAsyncContextManager:
            aenter_is_defined = method_defined(subclass,
                                               method_name='__aenter__')
            aexit_is_defined = method_defined(subclass,
                                              method_name='__aexit__')
            if aenter_is_defined and aexit_is_defined:
                return True
        return NotImplemented


class AsyncContextManager(Generic[T_co],
                          extra=AbstractAsyncContextManager):
    __slots__ = ()
