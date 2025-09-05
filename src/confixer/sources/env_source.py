from .base import ConfigSource
import os
from dotenv import dotenv_values
from typing import Any, Optional


class EnvSource(ConfigSource):
    def __init__(self, path: Optional[str] = None, prefix: Optional[str] = None):
        self.path = path
        self.prefix = prefix

    def load(self) -> dict[str, Any]:
        data: dict[str, str] = dict(os.environ)

        if self.path:
            dotenv_data = dotenv_values(self.path)
            # Drop None values
            cleaned = {k: v for k, v in dotenv_data.items() if v not in (None, "")}

            data.update(cleaned)

        if self.prefix:
            data = {
                k[len(self.prefix) :]: v
                for k, v in data.items()
                if k.startswith(self.prefix)
            }

        # TODO: add nesting + coercion
        return self._nest_keys(data)

    def _nest_keys(self, flat: dict[str, str]) -> dict[str, Any]:
        # Example: DB__HOST=localhost -> {"DB": {"HOST": "localhost"}}
        return flat
