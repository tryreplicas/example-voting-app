#!/usr/bin/env python3
"""Check that the Stripe webhook env vars are set, without revealing their values."""
import os
import sys

KEYS = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    missing = 0
    for key in KEYS:
        is_set = bool(os.environ.get(key))
        print(f"{key}: {'set' if is_set else 'MISSING'}")
        missing += not is_set
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
