#!/usr/bin/env python3
"""Install the HubSpot SDK in development mode."""

import subprocess
import sys


def main() -> None:
    print("Installing hubspot-sdk in development mode...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
    print("\nDone! You can now use:")
    print("  - Python: from hubspot_sdk import HubSpotClient")
    print("  - CLI:    hubspot --help")
    print("\nSet your token: export HUBSPOT_ACCESS_TOKEN=pat-xxx")


if __name__ == "__main__":
    main()
