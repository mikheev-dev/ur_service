from typing import Callable, Any

import os


def get_env(name: str, default: Any = None, cast: Callable[[Any], Any] = lambda x: x):
    value = os.getenv(name) or default
    return cast(value)


class PSQLConfig:
    DB_HOST = get_env('DB_HOST', default='0.0.0.0')
    DB_PORT = get_env('DB_PORT', default='5432', cast=int)
    DB_USER = get_env('DB_USER', default='uradmin')
    DB_PASSWORD = get_env('DB_PASS', default='test77')
    DB_NAME = get_env('DB_NAME', default='urdb')

    @staticmethod
    def connection_string() -> str:
        return (f"postgres://{PSQLConfig.DB_USER}:{PSQLConfig.DB_PASSWORD}@"
                f"{PSQLConfig.DB_HOST}:{PSQLConfig.DB_PORT}/{PSQLConfig.DB_NAME}")
