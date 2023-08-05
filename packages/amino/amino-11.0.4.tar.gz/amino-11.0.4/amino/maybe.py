from typing import TypeVar, Generic, Callable, Union, Any, cast
from functools import wraps, partial
from operator import eq, is_not
import inspect
import traceback

from amino import boolean
from amino.tc.base import F
from amino.func import call_by_name, I, curried

A = TypeVar('A')
B = TypeVar('B')


class Maybe(Generic[A], F[A], implicits=True):

    __slots__ = ()

    def __new__(tp, value: A, checker=partial(is_not, None)):
        return Maybe.check(value, checker)

    @staticmethod
    def check(value: A, checker=partial(is_not, None)):
        return Just(value) if checker(value) else Nothing

    @staticmethod
    def from_call(f: Callable[..., A], *args, **kwargs):
        exc = kwargs.pop('exc', Exception)
        try:
            return Maybe.check(f(*args, **kwargs))
        except exc:
            if exc == Exception:
                from amino.logging import log
                frame = inspect.currentframe().f_back  # type: ignore
                stack = traceback.format_stack(frame)
                log.exception('Maybe.from_call:')
                log.error(''.join(stack))
            return Nothing

    @staticmethod
    def typed(value: A, tpe: type):
        return Maybe.check(value, lambda a: isinstance(a, tpe))

    @staticmethod
    def wrap(mb: Union['Maybe[A]', None]):
        return mb if mb is not None and isinstance(mb, Just) else Nothing

    @staticmethod
    def getattr(obj, attr):
        return Maybe.check(getattr(obj, attr, None))

    @staticmethod
    @curried
    def iff(cond: bool, a: Union[A, Callable[[], A]]) -> 'Maybe[A]':
        return cast(Maybe, Just(call_by_name(a))) if cond else Nothing

    @staticmethod
    @curried
    def iff_m(cond: bool, a: Union[A, Callable[[], 'Maybe[A]']]) -> 'Maybe[A]':
        return cast(Maybe, call_by_name(a)) if cond else Nothing

    @property
    def _get(self) -> Union[A, None]:
        pass

    def cata(self, f: Callable[[A], B], b: Union[B, Callable[[], B]]) -> B:
        return (
            f(cast(A, self._get))
            if self.is_just
            else call_by_name(b)
        )

    def filter(self, f: Callable[[A], B]):
        l = lambda a: self if f(a) else Nothing
        return self.flat_map(l)

    def get_or_else(self, a: Union[A, Callable[[], A]]):
        return self.cata(I, a)

    __or__ = get_or_else

    def get_or_raise(self, e: Exception):
        def raise_e():
            raise e
        return self.cata(I, raise_e)

    def get_or_fail(self, err):
        return self.get_or_raise(Exception(call_by_name(err)))

    def __contains__(self, v):
        return self.contains(v)

    def error(self, f: Callable[[], Any]) -> 'Maybe[A]':
        self.cata(I, f)
        return self

    def observe(self, f: Callable[[A], Any]):
        self.foreach(f)
        return self

    effect = observe

    def __iter__(self):
        return iter(self.to_list)

    @property
    def is_just(self):
        return boolean.Boolean(isinstance(self, Just))

    @property
    def is_empty(self):
        return not self.is_just

    empty = is_empty

    @property
    def to_list(self):
        from amino.list import List
        return self.cata(lambda v: List(v), List())

    @property
    async def unsafe_await(self):
        if self.is_just:
            ret = await self._get()
            return Maybe(ret)
        else:
            return self

    async def unsafe_await_or(self, b: Union[B, Callable[[], B]]):
        return (Maybe(await(self._get)) if self.is_just  # type: ignore
                else call_by_name(b))

    @property
    def contains_coro(self):
        return self.exists(inspect.iscoroutine)

    @property
    def json_repr(self):
        return self.cata(I, lambda: None)


class Just(Generic[A], Maybe[A]):

    __slots__ = 'x',

    def __new__(tp: type, value: A, *args: Any, **kwargs: Any) -> 'Just[A]':
        return object.__new__(tp)

    def __init__(self, value: A) -> None:
        self.x = value

    @property
    def _get(self) -> Union[A, None]:
        return self.x

    def __str__(self):
        return 'Just({!s})'.format(self.x)

    def __repr__(self):
        return 'Just({!r})'.format(self.x)

    def __eq__(self, other):
        if not isinstance(other, Just):
            return False
        return eq(self.x, other.x)

    def __hash__(self):
        return hash(self._get)


class _Nothing(Generic[A], Maybe[A]):

    __object = None  # type: _Nothing

    def __new__(tp: type, *args: Any, **kwargs: Any) -> '_Nothing[A]':
        if _Nothing.__object is None:
            _Nothing.__object = object.__new__(tp)
        return _Nothing.__object

    def __str__(self):
        return 'Nothing'

    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, _Nothing)

    def __hash__(self):
        return hash('Nothing')

Empty = _Nothing
Nothing: Maybe = _Nothing()


def may(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return Maybe.check(f(*args, **kwargs))
    return wrapper


def flat_may(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        return res if isinstance(res, Maybe) else Maybe(res)
    return wrapper

__all__ = ('Maybe', 'Just', 'may', 'Empty', 'Nothing')
