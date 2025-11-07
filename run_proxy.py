#!/usr/bin/env python3
"""
Wrapper script to run LiteLLM proxy with asyncio loop on Python 3.14
"""
import sys
import os

# Patch the loop type before importing litellm
sys.path.insert(0, os.path.dirname(__file__))

# Import and patch before litellm loads
from litellm.proxy.proxy_cli import ProxyInitializationHelpers

# Override the _get_loop_type method to return "asyncio" instead of "uvloop"
def _get_loop_type_patched():
    """Patched version that returns asyncio instead of uvloop"""
    return "asyncio"

# Patch the static method
ProxyInitializationHelpers._get_loop_type = staticmethod(_get_loop_type_patched)

# Now import and run litellm
from litellm.proxy.proxy_cli import run_server

if __name__ == "__main__":
    # Pass through all command line arguments (including --config)
    sys.exit(run_server())

