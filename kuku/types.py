from typing import Dict, Any, Callable, List

Context = Dict[str, Any]

Templates = Dict[str, Callable]

# template path -> List of K8S objects
Rendering = Dict[str, List[Any]]
