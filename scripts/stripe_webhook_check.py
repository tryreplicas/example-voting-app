"""Report whether the Stripe env vars are set, without revealing their values.

Exits 0 if STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET are both set, else 1.
Empty or whitespace-only values count as missing.
"""
import os
import sys

REQUIRED = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    missing = False
    for name in REQUIRED:
        present = bool(os.environ.get(name, "").strip())
        missing = missing or not present
        print(f"{name}: {'set' if present else 'missing'}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
