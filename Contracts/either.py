import functools
import sys
from dataclasses import dataclass
from typing import (TypeVar, Generic, Union, Callable, ParamSpec,
                     NoReturn, get_args,
                     cast
)

import traceback

from contracts.errors import AppError,HandledToken,UnexpectedError
from shared.logger import get_logger
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
@dataclass(frozen=True,slots=True)
class Ok(Generic[R]):
    value: R
    def unwrap(self) -> R:
        return self.value

@dataclass(frozen=True,slots=True)
class Error(Generic[L]):
    error: L
    def unwrap(self) -> NoReturn:
        raise HandledToken().with_traceback(None)  # Prevents stack trace for control flow token

# THE FIX: L must be listed first so Either[AppError, ReturnType] maps correctly!
Either = Union[Error[L], Ok[R]]

# ==========================================
# 3. THE DECORATOR
# ==========================================
def railway(func: Callable[P, R]) -> Callable[P, Either[AppError, R]]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[AppError, R]:
        try:
            ok_res =func(*args, **kwargs)
            return Ok(ok_res)
        except HandledToken as token:
            return Error(token)
        except Exception as e:
            logger  = get_logger(func.__module__)
            _, _, exc_tb = sys.exc_info()
            # Extract the lowest/deepest frame from the stack trace
            summary = traceback.extract_tb(exc_tb)[-1]
            location_info = f"{summary.name} ({summary.filename}:{summary.lineno})"
            if isinstance(e, APP_ERRORS_TUPLE):
                error_result = Error(cast(AppError, e))
                logger.warning(f"AppError {e} -> at {location_info}")
                return error_result
            else:
                logger.error(
                    f"Unexpected Exception in {e} at {location_info}", 
                    exc_info=True
                )
                return Error(UnexpectedError(e))
    return wrapper