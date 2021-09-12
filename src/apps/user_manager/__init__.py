from .handlers import dp
from .filters import IsAdmin

_filters = [IsAdmin]

__all__ = ['dp', '_filters']
