#!/usr/bin/env python3
"""Report whether Stripe env vars are set. Never prints their values."""
import os
import sys

NAMES = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    ok = True
    for name in NAMES:
        present = bool(os.environ.get(name))
        print(f"{name}: {'present' if present else 'missing'}")
        ok = ok and present
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
