import functools
from dataclasses import dataclass
from typing import (TypeVar, Generic, Union, Callable, ParamSpec,
                     NoReturn, get_args,
                     cast
)

from contracts.errors import AppError

# ==========================================
# 1. TYPES & EXCEPTIONS
# ==========================================
L = TypeVar('L', bound=Exception, covariant=True)
R = TypeVar('R', covariant=True)
P = ParamSpec('P')



# Type hint the tuple so the IDE knows exactly what it is
APP_ERRORS_TUPLE: tuple[type[Exception], ...] = get_args(AppError)

# ==========================================
# 2. THE DATACLASS VARIANTS & UNION
# ==========================================
@dataclass(frozen=True)
class Ok(Generic[R]):
    value: R
    def unwrap(self) -> R:
        return self.value

@dataclass(frozen=True)
class Error(Generic[L]):
    error: L
    def unwrap(self) -> NoReturn:
        raise self.error

# THE FIX: L must be listed first so Either[AppError, ReturnType] maps correctly!
Either = Union[Error[L], Ok[R]]

# ==========================================
# 3. THE DECORATOR
# ==========================================
def railway(func: Callable[P, R]) -> Callable[P, Either[AppError, R]]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[AppError, R]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            if isinstance(e, APP_ERRORS_TUPLE):
                # We cast 'e' to AppError because we just verified it with isinstance.
                # This satisfies the type checker's requirement that L must be AppError.
                return Error(cast(AppError, e))
            raise e
    return wrapper
