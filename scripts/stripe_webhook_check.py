#!/usr/bin/env python3
"""Report whether Stripe env vars are set. Never prints their values."""
import os
import sys

NAMES = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")

missing = [n for n in NAMES if not os.environ.get(n)]
for n in NAMES:
    print(f"{n}: {'missing' if n in missing else 'present'}")
sys.exit(1 if missing else 0)
