#!/usr/bin/env python3
"""Utils module for accessing nested maps and JSON data."""

from typing import Mapping, Any, Sequence
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a value in a nested dictionary using a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> dict:
    """Get JSON response from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Decorator to cache method output."""
    attr_name = "_memoized_" + method.__name__

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper

