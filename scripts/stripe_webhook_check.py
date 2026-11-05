import os
import sys

KEYS = ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET")

missing = [k for k in KEYS if not os.environ.get(k)]
for k in KEYS:
    print(f"{k}: {'missing' if k in missing else 'present'}")
sys.exit(1 if missing else 0)
