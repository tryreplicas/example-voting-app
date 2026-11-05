#!/usr/bin/env python3
"""Check that the Stripe webhook environment variables are present.

Reports only whether each variable is set; never prints the values.
Exits 0 if all are set, 1 otherwise.
"""

import os
import sys

REQUIRED_KEYS = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")


def main():
    all_set = True
    for key in REQUIRED_KEYS:
        present = bool(os.environ.get(key))
        all_set = all_set and present
        print(f"{key}: {'set' if present else 'missing'}")
    return 0 if all_set else 1


if __name__ == "__main__":
    sys.exit(main())
