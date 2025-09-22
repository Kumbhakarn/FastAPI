"""
FastAPI Config Management with Dependency Injection
===================================================

This file demonstrates how to manage **application configuration** in FastAPI
using **Dependency Injection (DI)**.

Why Configuration Management?
-----------------------------
- Centralizes all important settings (API keys, debug flags, DB URLs, etc.).
- Makes it easy to **change settings in one place** instead of scattered constants.
- Keeps sensitive values (like API keys) in a structured object.
- Enables **different environments** (development, testing, production) with minimal changes.

Concept:
--------
- Define a `Settings` class that holds configuration values.
- Use a dependency function (`get_settings`) to provide an instance of `Settings`.
- Inject the configuration into any endpoint using `Depends`.

Flow:
-----
1. A client requests `/config`.
2. FastAPI sees `settings: Settings = Depends(get_settings)`.
3. `get_settings()` is executed, returning a `Settings` object.
4. The endpoint receives this `settings` object as an argument.
5. The endpoint can now safely access configuration values (e.g., API key).

"""

from fastapi import FastAPI, Depends

# Initialize FastAPI app
app = FastAPI()


class Settings:
    """
    Application settings class.

    Attributes:
        api_key (str): A secret API key (mocked here).
        debug (bool): Flag to enable/disable debug mode.
    """

    def __init__(self):
        # In a real-world scenario, these values may come from
        # environment variables or config files.
        self.api_key = 'my_secret'
        self.debug = True


def get_settings():
    """
    Dependency function that returns application settings.

    Returns:
        Settings: An instance of the Settings class.
    """
    return Settings()


@app.get('/config')
def get_config(settings: Settings = Depends(get_settings)):
    """
    Endpoint to fetch application configuration.

    Args:
        settings (Settings): Injected dependency containing application settings.

    Returns:
        dict: A dictionary with selected configuration values.
    """
    return {'api_key': settings.api_key}
