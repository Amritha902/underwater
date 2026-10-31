"""Tiny discrete-event scheduler."""
import heapq
import itertools


class Engine:
    def __init__(self):
        self.now = 0.0
        self._q = []
        self._seq = itertools.count()

    def schedule(self, delay: float, fn, *args) -> None:
        heapq.heappush(self._q, (self.now + delay, next(self._seq), fn, args))

    def run(self, until: float = float("inf")) -> None:
        while self._q and self._q[0][0] <= until:
            t, _, fn, args = heapq.heappop(self._q)
            self.now = t
            fn(*args)
        self.now = max(self.now, min(until, self.now if not self._q else until))
