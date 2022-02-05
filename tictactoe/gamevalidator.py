from typing import List
from collections import Counter

def validate_conditions(game_board: List[str]) -> bool:
    count = Counter(game_board)
    if abs(count.get("X", 0) - count.get("O", 0)) >= 2:
        return count, False
    return count, True

