import os
import time
from collections import defaultdict, deque

import gradio as gr
from agents import Runner
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

from twin import ui  # noqa: E402
from twin.agent import build_agent  # noqa: E402 (dopo load_dotenv)
from twin.limits import GlobalLimiter  # noqa: E402

# Modello di riserva: le quote di Gemini sono per modello, quindi se il principale va in 429 (o è sovraccarico)
# si riprova con questo. GEMINI_FALLBACK_MODEL vuoto = nessun riserva.
FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite")
agents = [build_agent(max_retries=0 if FALLBACK_MODEL else 2)]
if FALLBACK_MODEL:
    agents.append(build_agent(FALLBACK_MODEL, max_retries=1))

global_limiter = GlobalLimiter()

MAX_INPUT_CHARS = 1000
MAX_MSGS_PER_HOUR = 30
_hits: dict[str, deque] = defaultdict(deque)

# Tutto ciò che il visitatore vede, per lingua. Italiano se il browser è in italiano, altrimenti inglese.
TEXTS = {
    "it": {
        "welcome": "Chiedimi di esperienza, competenze e progetti.",
        "input": "Scrivi un messaggio…",
        "examples": ["Parlami della tua esperienza", "Quali sono le tue competenze principali?", "Sei disponibile a lavorare da remoto?"],
        "rate_limited": "Hai raggiunto il limite di messaggi per ora. Riprova più tardi.",
        "too_long": f"Messaggio troppo lungo (max {MAX_INPUT_CHARS} caratteri).",
        "busy": "Ci sono molte richieste in questo momento. Riprova tra qualche minuto.",
        "error": "Si è verificato un errore. Riprova tra poco.",
    },
    "en": {
        "welcome": "Ask me about my experience, skills and projects.",
        "input": "Type a message…",
        "examples": ["Tell me about your experience", "What are your main skills?", "Are you open to remote work?"],
        "rate_limited": "You've reached the message limit for this hour. Please try again later.",
        "too_long": f"Message too long (max {MAX_INPUT_CHARS} characters).",
        "busy": "There are a lot of requests right now. Please try again in a few minutes.",
        "error": "Something went wrong. Please try again shortly.",
    },
}


# Indicatore "sta scrivendo" in stile iMessage: tre pallini animati via CSS (vedi twin/ui.py).
# Se il sanitizer di Gradio togliesse le classi, resterebbero tre pallini statici.
TYPING = '<span class="typing"><span>●</span><span>●</span><span>●</span></span>'


def _client_ip(request: gr.Request | None) -> str:
    if request is None:
        return "anon"
    # Dietro il proxy di Hugging Face Spaces client.host è sempre il proxy: l'IP reale sta in X-Forwarded-For.
    forwarded = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    return forwarded or (request.client.host if request.client else "anon")


def _language(request: gr.Request | None) -> str:
    """Lingua del visitatore dalla prima voce di Accept-Language: 'it' se italiano, altrimenti 'en'."""
    header = request.headers.get("accept-language", "") if request else ""
    first = header.split(",")[0].strip().lower()
    return "it" if first.split("-")[0] == "it" else "en"


def _rate_limited(key: str) -> bool:
    now = time.time()
    q = _hits[key]
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= MAX_MSGS_PER_HOUR:
        return True
    q.append(now)
    return False


def _text(content) -> str:
    """Il contenuto dello storico può essere una stringa o una lista di blocchi {"type": "text", "text": ...}."""
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if isinstance(b, dict))


def _is_overload(e: BaseException | None) -> bool:
    """True per quota esaurita (429) o modello sovraccarico/non disponibile (5xx), anche se l'errore è annidato."""
    while e is not None:
        if getattr(e, "status_code", None) in (429, 500, 502, 503, 504):
            return True
        e = e.__cause__ or e.__context__
    return False


async def _stream(agent, messages: list[dict], state: dict):
    """Testo accumulato della risposta; `state["tool"]` segnala se un tool è già stato eseguito."""
    text = ""
    tool_called = False
    result = Runner.run_streamed(agent, messages)
    async for event in result.stream_events():
        if event.type == "run_item_stream_event" and event.name == "tool_called":
            tool_called = state["tool"] = True
        elif event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            if tool_called:  # nuovo turno dopo un tool: mostra solo la risposta finale
                text, tool_called = "", False
            text += event.data.delta
            yield text


def make_chat(lang: str):
    t = TEXTS[lang]

    async def chat(message: str, history: list[dict], request: gr.Request):
        if _rate_limited(_client_ip(request)):
            yield t["rate_limited"]
            return
        if len(message) > MAX_INPUT_CHARS:
            yield t["too_long"]
            return
        if not global_limiter.try_acquire():
            print("[limite globale] richiesta rifiutata")
            yield t["busy"]
            return

        messages = [{"role": m["role"], "content": _text(m["content"])} for m in history]
        # Promemoria solo nella copia inviata al modello (non nello storico mostrato): i documenti sono in italiano
        # e senza questo il modello tende a rispondere in italiano anche a domande in inglese.
        messages.append({"role": "user", "content": f"{message}\n\n[Reply in the same language as the message above.]"})

        start = time.perf_counter()
        yield TYPING  # i tre puntini animati, sostituiti dal primo token
        for attempt, agent in enumerate(agents):
            state = {"tool": False}
            first_token = None
            try:
                async for text in _stream(agent, messages, state):
                    if first_token is None:
                        first_token = time.perf_counter() - start
                    yield text
                print(f"[timing] modello {agent.model.model}: primo token {first_token or 0:.1f}s, "
                      f"totale {time.perf_counter() - start:.1f}s")
                return
            except Exception as e:
                overload = _is_overload(e)
                print(f"[errore dopo {time.perf_counter() - start:.1f}s, modello {agent.model.model}] "
                      f"{type(e).__name__}: {e}")
                # Si passa al riserva solo se non è stato mostrato testo né eseguito un tool
                # (altrimenti si duplicherebbe, ad esempio, la registrazione di un contatto).
                if overload and first_token is None and not state["tool"] and attempt + 1 < len(agents):
                    print("[fallback] passo al modello di riserva")
                    continue
                yield t["busy"] if overload else t["error"]
                return

    return chat


def build_chat_interface(lang: str) -> gr.ChatInterface:
    t = TEXTS[lang]
    return gr.ChatInterface(
        make_chat(lang),
        chatbot=gr.Chatbot(
            show_label=False,
            elem_id=f"chat-{lang}",
            placeholder=t["welcome"],
            layout="bubble",
            buttons=["copy", "copy_all"],  # senza "share" (condivisione su Hugging Face)
        ),
        # Con un textbox personalizzato ChatInterface non imposta i pulsanti: vanno attivati qui.
        textbox=gr.Textbox(
            show_label=False,
            placeholder=t["input"],
            lines=1,
            max_lines=1,
            scale=7,
            autofocus=True,
            submit_btn=True,
            stop_btn=True,
        ),
        examples=t["examples"],
        show_progress="hidden",  # niente "processing | 4.8/5.9s"
    )


with gr.Blocks(title=ui.DISPLAY_NAME) as demo:
    gr.HTML(ui.header_html())
    # Entrambe le chat partono nascoste: al caricamento si mostra solo quella nella lingua del visitatore.
    with gr.Column(visible=False) as col_it:
        build_chat_interface("it")
    with gr.Column(visible=False) as col_en:
        build_chat_interface("en")

    def show_language(request: gr.Request):
        it = _language(request) == "it"
        return gr.Column(visible=it), gr.Column(visible=not it)

    demo.load(show_language, None, [col_it, col_en])

if __name__ == "__main__":
    demo.launch(theme=ui.THEME, css=ui.CSS)
