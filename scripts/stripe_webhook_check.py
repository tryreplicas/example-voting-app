#!/usr/bin/env python3
"""Report whether Stripe env vars are set. Never prints their values."""
import os
import sys

REQUIRED = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    missing = 0
    for name in REQUIRED:
        if os.environ.get(name):
            print(f"{name}: present")
        else:
            print(f"{name}: missing")
            missing += 1
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
