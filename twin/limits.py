import os
import time
from collections import deque


class SlidingWindowLimiter:
    """Limite globale a finestra scorrevole: al massimo `max_calls` ogni `seconds` secondi (in memoria).

    Protegge la quota di Gemini da molti visitatori diversi, cosa che il limite per IP non copre.
    Non serve un lock: `try_acquire` è sincrona e Gradio gira in un solo event loop.
    """

    def __init__(self, max_calls: int, seconds: int):
        self.max_calls = max_calls
        self.seconds = seconds
        self._calls: deque[float] = deque()

    def try_acquire(self) -> bool:
        now = time.time()
        while self._calls and now - self._calls[0] > self.seconds:
            self._calls.popleft()
        if len(self._calls) >= self.max_calls:
            return False
        self._calls.append(now)
        return True


class GlobalLimiter:
    """Limite complessivo sui messaggi: al minuto e al giorno (valori da variabili d'ambiente).

    Un messaggio costa 1 richiesta a Gemini, 2 se il modello chiama un tool: i messaggi al minuto vanno quindi
    tenuti a metà del limite RPM del modello (15 RPM -> 7 messaggi/min). Il modello di riserva ha una quota
    separata e non pesa su quella del principale. Verifica i limiti del tuo progetto in Google AI Studio.
    """

    def __init__(self):
        per_minute = int(os.getenv("GLOBAL_RPM", "7"))
        per_day = int(os.getenv("GLOBAL_RPD", "300"))
        self._minute = SlidingWindowLimiter(per_minute, 60)
        self._day = SlidingWindowLimiter(per_day, 86400)

    def try_acquire(self) -> bool:
        # Prima il minuto: se è pieno, il messaggio non consuma la quota giornaliera.
        return self._minute.try_acquire() and self._day.try_acquire()
