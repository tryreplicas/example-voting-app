#!/usr/bin/env python3
"""Report whether Stripe env vars are set, without printing their values."""
import os
import sys

KEYS = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    ok = True
    for key in KEYS:
        present = bool(os.environ.get(key))
        print(f"{key}: {'present' if present else 'missing'}")
        ok = ok and present
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
