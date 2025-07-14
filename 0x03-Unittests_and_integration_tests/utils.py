#!/usr/bin/env python3
"""Utils module for accessing nested maps."""

from typing import Mapping, Any, Sequence
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a value in a nested dictionary using a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> dict:
    """Send a GET request to the given URL and return the JSON response."""
    response = requests.get(url)
    return response.json()
