import logging
from functools import wraps
import inspect
from typing import Callable, TypeVar, Any, Union, Awaitable


Func = TypeVar('Func', bound = Callable[..., Any])


def funclog(func: Func) -> Func:
    """
    Logs the start and ending a function executing.

    Args:
        func (Func): The function to be logged.

    Returns:
        Func: Wrapped function with logging instance.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Union[Any, Awaitable[Any]]:
        logger = logging.getLogger(func.__module__)
        is_debug = logger.getEffectiveLevel() == logging.DEBUG

        if is_debug:
            logger.debug(f"Starting {func.__name__}...")
        
        if inspect.iscoroutinefunction(func):

            async def async_wrapper() -> Any:
                result = await func(*args, **kwargs)
                if is_debug:
                    logger.debug(f"Ending {func.__name__}...")    
                return result
            
            return async_wrapper()

        else:
            result = func(*args, **kwargs)
            if is_debug:
                logger.debug(f"Ending {func.__name__}...")

            return result

    return wrapper                
