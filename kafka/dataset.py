from collections import defaultdict
from typing import Any, Callable

subscribers = defaultdict(list)


def subscribe(dataset: str, fn: Callable) -> None:
    subscribers[dataset].append(fn)


def publish(dataset: str, args: Any) -> None:
    if dataset not in subscribers:
        raise Exception("Invalid dataset")

    for fn in subscribers[dataset]:
        fn(args)
