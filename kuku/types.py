from typing import Dict, Any, Callable, List

from kuku.objects import K8sObject

Context = Dict[str, Any]

Templates = Dict[str, Callable]

# template path -> List of K8S objects
Rendering = Dict[str, List[K8sObject]]
