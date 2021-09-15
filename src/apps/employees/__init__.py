from .handlers import dp
from .filters import IsEmployee

_filters = [IsEmployee]

__all__ = ['dp', '_filters']
