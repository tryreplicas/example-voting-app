#!/usr/bin/env python3
"""Check that the Stripe webhook environment variables are set.

Reports whether STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET are present and
non-empty, without ever printing their values.

Usage:
    python scripts/stripe_webhook_check.py

Exits 0 if both are set, 1 if either is missing.
"""
import os
import sys

REQUIRED_VARS = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    missing = False
    for name in REQUIRED_VARS:
        if os.environ.get(name):
            print(f"{name}: set")
        else:
            print(f"{name}: missing")
            missing = True
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
