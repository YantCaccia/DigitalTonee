import base64
import os
from pathlib import Path

import gradio as gr

ASSETS = Path(__file__).resolve().parent.parent / "assets"
DISPLAY_NAME = os.getenv("DISPLAY_NAME", "Antonio Cacciapuoti")
LINKEDIN_URL = os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/antonio-cacciapuoti-45a883220/")

# Stile "iMessage": blu per l'utente, grigio per il twin, bolle molto arrotondate, font di sistema Apple.
THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.gray,
    radius_size=gr.themes.sizes.radius_xxl,
    font=["-apple-system", "BlinkMacSystemFont", "SF Pro Text", "Helvetica Neue", "sans-serif"],
)

CSS = """
/* larghezza fissa rispetto alla finestra (senza width esplicita, margin:auto in un flex la fa restringere al contenuto) */
.gradio-container { width: min(92vw, 820px) !important; max-width: none !important; margin: 0 auto !important; }
.gradio-container .main, .gradio-container .wrap, .gradio-container .fillable { width: 100% !important; }
footer { display: none !important; }

/* altezza della chat legata alla finestra: 100dvh meno intestazione, campo di input e margini */
#chat-it, #chat-en { height: calc(100dvh - 270px) !important; min-height: 320px; }

/* bolle */
.message { border-radius: 20px !important; border: none !important; box-shadow: none !important;
           padding: 6px 15px !important; line-height: 1.3 !important; font-size: 15px !important; }
.message p { margin: 0 !important; }
/* angolo "a coda" come su iMessage: più stretto in basso, dal lato di chi scrive */
.message.user, .user.message { border-bottom-right-radius: 5px !important; }
.message.bot, .bot.message { border-bottom-left-radius: 5px !important; }
/* le variabili del tema colorano il testo di grigio: le ridefiniamo dentro le bolle */
.message.user, .user.message {
    background: #0b84fe !important; color: #fff !important;
    --body-text-color: #fff; --body-text-color-subdued: #fff; --link-text-color: #fff;
}
.message.bot, .bot.message {
    background: #e9e9eb !important; color: #000 !important;
    --body-text-color: #000; --body-text-color-subdued: #000;
}
.dark .message.bot, .dark .bot.message {
    background: #3a3a3c !important; color: #fff !important;
    --body-text-color: #fff; --body-text-color-subdued: #fff;
}
.message.user, .message.user *, .user.message, .user.message * { color: #fff !important; opacity: 1 !important; }
.message.bot *, .bot.message * { opacity: 1 !important; }
.dark .message.bot *, .dark .bot.message * { color: #fff !important; }

/* "sta scrivendo": tre pallini grigi che pulsano uno dopo l'altro */
.typing { display: inline-flex; align-items: center; gap: 4px; height: 20px; }
.typing span { font-size: 9px; line-height: 1; color: #8e8e93; animation: imsg-typing 1.2s infinite ease-in-out; }
.typing span:nth-child(2) { animation-delay: .2s; }
.typing span:nth-child(3) { animation-delay: .4s; }
@keyframes imsg-typing { 0%, 60%, 100% { opacity: .25; transform: translateY(0); }
                         30% { opacity: 1; transform: translateY(-2px); } }

/* suggerimenti iniziali: altezza data solo dal padding (uguale sopra e sotto), contenuto di altezza naturale */
button.example, .examples button, [class*="example"] > button {
    display: flex !important; align-items: center !important; justify-content: flex-start !important;
    height: auto !important; min-height: 0 !important;
    padding: 12px 20px !important; line-height: 1.3 !important; font-size: 15px !important;
}
button.example *, .examples button *, [class*="example"] > button * {
    margin: 0 !important; padding: 0 !important; height: auto !important; min-height: 0 !important;
    flex: 0 1 auto !important; align-self: center !important; line-height: 1.3 !important;
}
.example-icon-container:empty, .example-image-container:empty { display: none !important; }

/* niente avatar accanto alle bolle */
.avatar-container, .avatar-image { display: none !important; }

/* campo di testo e pulsanti di invio/stop: stessa altezza, stessa spaziatura, nessun movimento tra i due stati */
:root { --imsg-control: 38px; --imsg-gap: 8px; }

/* il riquadro che contiene tutto: stesso respiro su tutti i lati */
form, .block:has(textarea) { padding: var(--imsg-gap) !important; }
form:has(textarea), .block:has(textarea), div:has(> textarea) { align-items: center !important; }

/* campo di testo: pillola alta quanto i pulsanti, sempre su una riga */
textarea, input[type=text] {
    box-sizing: border-box !important; border-radius: calc(var(--imsg-control) / 2) !important;
    height: var(--imsg-control) !important; min-height: var(--imsg-control) !important;
    max-height: var(--imsg-control) !important; padding: 9px 16px !important;
    line-height: 20px !important; overflow: hidden !important;
}

/* invio e stop: stesso identico cerchio blu, cambia solo l'icona */
button[class*="submit"], button[class*="stop"] {
    box-sizing: border-box !important; display: inline-flex !important; align-items: center !important;
    justify-content: center !important; align-self: center !important;
    width: var(--imsg-control) !important; min-width: var(--imsg-control) !important;
    max-width: var(--imsg-control) !important; height: var(--imsg-control) !important;
    flex: 0 0 var(--imsg-control) !important; margin: 0 0 0 var(--imsg-gap) !important;
    padding: 0 !important; border: none !important; border-radius: 50% !important;
    background: #0b84fe !important; color: #fff !important;
}
/* stesso sfondo in tutti gli stati (Gradio ridefinisce hover/active/disabled e le variabili dei pulsanti secondari) */
button[class*="submit"], button[class*="stop"] {
    --button-secondary-background-fill: #0b84fe; --button-secondary-background-fill-hover: #0b84fe;
    --button-primary-background-fill: #0b84fe; --button-primary-background-fill-hover: #0b84fe;
}
button[class*="submit"]:hover, button[class*="stop"]:hover,
button[class*="submit"]:active, button[class*="stop"]:active,
button[class*="submit"]:focus, button[class*="stop"]:focus,
button[class*="submit"]:disabled, button[class*="stop"]:disabled {
    background: #0b84fe !important; background-color: #0b84fe !important; opacity: 1 !important;
}
button[class*="submit"] svg, button[class*="stop"] svg {
    width: 16px !important; height: 16px !important; color: #fff !important;
}
button[class*="submit"] svg * { stroke: #fff !important; }
button[class*="stop"] svg, button[class*="stop"] svg * { fill: #fff !important; stroke: #fff !important; }

/* intestazione in stile iMessage: foto tonda e nome in una pillola */
.imsg-header { display: flex; flex-direction: column; align-items: center; gap: 6px; margin: 4px 0 8px; }
.imsg-photo { width: 76px; height: 76px; border-radius: 50%; overflow: hidden; background: #9a9aa0;
              display: flex; align-items: center; justify-content: center;
              color: #fff; font-size: 28px; font-weight: 600; }
.imsg-photo img { width: 100%; height: 100%; object-fit: cover; }
.imsg-name { display: inline-flex; align-items: center; gap: 4px; padding: 4px 14px; border-radius: 999px;
             background: #fff; border: 1px solid #e5e5ea; box-shadow: 0 1px 4px rgba(0,0,0,.08);
             color: #000 !important; font-size: 16px; font-weight: 600; text-decoration: none !important; }
.imsg-name .chev { color: #b0b0b6; font-weight: 400; }
.dark .imsg-name { background: #1c1c1e; border-color: #3a3a3c; color: #fff !important; }
"""


def _mime(data: bytes) -> str:
    """Tipo dell'immagine dai primi byte (la foto può arrivare da un Secret, senza estensione)."""
    if data.startswith(b"\x89PNG"):
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return "jpeg"


def _photo_html() -> str:
    """Foto tonda incorporata nella pagina (data URI). Fonti, in ordine: variabile AVATAR_B64 (per i deploy,
    dove il file non è nel repo), file assets/avatar.*. Senza foto: iniziali del nome."""
    data = None
    if encoded := os.getenv("AVATAR_B64"):
        try:
            data = base64.b64decode(encoded)
        except ValueError:
            print("[ui] AVATAR_B64 non è base64 valido: uso i file o le iniziali")
    if data is None:
        for ext in ("jpg", "jpeg", "png", "webp"):
            path = ASSETS / f"avatar.{ext}"
            if path.exists():
                data = path.read_bytes()
                break
    if data is None:
        return "".join(w[0] for w in DISPLAY_NAME.split()[:2]).upper()
    encoded = base64.b64encode(data).decode()
    return f'<img src="data:image/{_mime(data)};base64,{encoded}" alt="{DISPLAY_NAME}">'


def header_html() -> str:
    # Su una sola riga e senza rientri: il Markdown tratterebbe altrimenti le righe indentate come codice.
    return (
        f'<div class="imsg-header"><div class="imsg-photo">{_photo_html()}</div>'
        f'<a class="imsg-name" href="{LINKEDIN_URL}" target="_blank" rel="noopener">'
        f'{DISPLAY_NAME}<span class="chev">›</span></a></div>'
    )
