from functools import wraps
from typing import List, Optional, Dict, Any, Callable
import inspect

def command_metadata(
    tags: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None,
    mitre_attack: Optional[List[str]] = None,
    **kwargs: Any
) -> Callable:
    """
    Decorator to attach metadata to command functions.
    
    Args:
        tags: List of tags associated with the command
        dependencies: List of other commands that must be run before this one
        **kwargs: Additional metadata key-value pairs
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Store metadata in function attributes
        wrapper.__metadata__ = {
            'risk_level': tags or [],
            'dependencies': dependencies or [],
            'mitre_attack': mitre_attack or [],
            **kwargs
        }
        return wrapper
    return decorator

def get_command_metadata(func: Callable) -> Dict[str, Any]:
    """
    Retrieve metadata from a decorated function.
    
    Args:
        func: The function to get metadata from
    
    Returns:
        Dictionary containing the function's metadata
    """
    return getattr(func, '__metadata__', {})

def get_commands_by_module(tag: str, module) -> List[Callable]:
    """
    Find all command functions with a specific tag.
    
    Args:
        tag: The tag to search for
        module: The module to search in
    
    Returns:
        List of functions that have the specified tag
    """
    commands = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            metadata = get_command_metadata(obj)
            if tag in metadata.get('module', []):
                commands.append(obj)
    return commands

def get_commands_by_mitre(mitre_attack: str, module) -> List[Callable]:
    """
    Find all command functions with a specific tag.
    
    Args:
        tag: The tag to search for
        module: The module to search in
    
    Returns:
        List of functions that have the specified tag
    """
    commands = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            metadata = get_command_metadata(obj)
            if mitre_attack in metadata.get('mitre_attack', []):
                commands.append(obj)
    return commands