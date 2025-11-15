import os
import sys

# Ensure imports work when run directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMON_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.abspath(os.path.join(COMMON_DIR, "..", ".."))

if COMMON_DIR not in sys.path:
    sys.path.append(COMMON_DIR)

from core import starlight_cycle  # type: ignore


BANNER = r"""
⭐ Starlight Hybrid Shell ⭐
Type your message and press Enter.
Type /exit to quit.
"""


def main() -> None:
    print(BANNER)
    runtime_root = ROOT_DIR

    while True:
        try:
            text = input("you › ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[starlight] goodbye for now.")
            break

        if not text:
            continue

        if text.lower() in {"/exit", "/quit"}:
            print("[starlight] session ended.")
            break

        result = starlight_cycle.run_turn(text, runtime_root=runtime_root)
        reply = result.get("reply", "")
        used_cloud = result.get("used_cloud", False)

        prefix = "starlight (cloud+local)" if used_cloud else "starlight (local)"
        print(f"{prefix} › {reply}")


if __name__ == "__main__":
    main()
