import os
import json
from datetime import datetime

from . import intent_classifier, context_builder, response_merger, cloud_client


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.path.join(ROOT_DIR, "logs", "runtime")
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_LOG = os.path.join(LOG_DIR, "session_log.jsonl")


def _log_event(record: dict) -> None:
    try:
        with open(SESSION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        # Logging must never crash Starlight
        pass


def run_turn(user_input: str, runtime_root: str | None = None) -> dict:
    """
    Core hybrid reasoning loop for Starlight.

    - Classifies intent
    - Builds context bundle
    - Decides whether to use cloud or stay local
    - Calls cloud_client when available
    - Falls back to local response if cloud is offline
    - Returns a structured dict and logs it
    """
    ts = datetime.utcnow().isoformat() + "Z"

    intent = intent_classifier.classify_intent(user_input)

    context_bundle = context_builder.build_context(
        user_input=user_input,
        intent=intent,
        runtime_root=runtime_root or ROOT_DIR,
    )

    cloud_available = cloud_client.is_cloud_available()
    used_cloud = False
    cloud_payload = None
    local_reply = None

    if cloud_available and intent["kind"] in {"chat", "task", "memory"}:
        cloud_payload = cloud_client.cloud_reason(
            user_input=user_input,
            context=context_bundle,
        )
        used_cloud = True
    else:
        local_reply = response_merger.local_fallback_reply(
            user_input=user_input,
            intent=intent,
            context=context_bundle,
            cloud_available=cloud_available,
        )

    final = response_merger.merge_response(
        user_input=user_input,
        intent=intent,
        context=context_bundle,
        cloud_response=cloud_payload,
        local_reply=local_reply,
        used_cloud=used_cloud,
        timestamp=ts,
    )

    _log_event(final)

    return final


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a single Starlight turn from the CLI.")
    parser.add_argument("text", help="User input text")
    parser.add_argument(
        "--root",
        help="Optional runtime root (defaults to autodetected USB root)",
        default=None,
    )
    args = parser.parse_args()

    result = run_turn(args.text, runtime_root=args.root)
    print(result.get("reply", "[no reply generated]"))
