from typing import Dict, Any, Callable, List
from collections import ChainMap

# Context is used to pass variables
Context = ChainMap

# template file path -> template function
Templates = Dict[str, Callable]

# template file path -> List of K8S objects
Rendering = Dict[str, List[Any]]


class IgnoredListItem:
    """Placeholder list item to be ignored for deep merges of lists"""

    ...
