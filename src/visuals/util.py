from typing import Any, Collection, Tuple


def _in(item: Any, pairs: Collection[Tuple[Any, Any]]) -> bool:
    for pair in pairs:
        if item in pair:
            return True

    return False
