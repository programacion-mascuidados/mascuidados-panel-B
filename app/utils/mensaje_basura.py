import json


def parse_mensaje_basura(raw: str | None) -> list[str]:
    if raw is None:
        return []

    trimmed = raw.strip()
    if not trimmed:
        return []

    if trimmed.startswith("[") or trimmed.startswith("{"):
        try:
            parsed = json.loads(trimmed)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass

    return [line.strip() for line in trimmed.splitlines() if line.strip()]


def serialize_mensaje_basura(messages: list[str], original: str | None) -> str | None:
    if not messages:
        return None

    original_trimmed = (original or "").strip()
    if original_trimmed.startswith("[") or original_trimmed.startswith("{"):
        try:
            parsed = json.loads(original_trimmed)
            if isinstance(parsed, list):
                return json.dumps(messages, ensure_ascii=False)
        except json.JSONDecodeError:
            pass

    return "\n".join(messages)


def remove_mensaje_basura_at_index(raw: str | None, index: int) -> str | None:
    messages = parse_mensaje_basura(raw)
    if index < 0 or index >= len(messages):
        raise IndexError("message index out of range")

    remaining = messages[:index] + messages[index + 1 :]
    return serialize_mensaje_basura(remaining, raw)
