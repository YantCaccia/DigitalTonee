import base64
import os
from pathlib import Path

import gradio as gr

ASSETS = Path(__file__).resolve().parent.parent / "assets"
DISPLAY_NAME = os.getenv("DISPLAY_NAME", "Antonio Cacciapuoti")
LINKEDIN_URL = os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/antonio-cacciapuoti-45a883220/")

# Design Tokens: Plus Jakarta Sans typography and theme colors
THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.slate,
    radius_size=gr.themes.sizes.radius_xxl,
    font=[
        gr.themes.Font("Plus Jakarta Sans"),
        gr.themes.Font("-apple-system"),
        gr.themes.Font("BlinkMacSystemFont"),
        gr.themes.Font("sans-serif"),
    ],
).set(
    # Dark Mode defaults
    body_background_fill="#FAFBFD",
    body_background_fill_dark="#0B0D14",
    body_text_color="#0F172A",
    body_text_color_dark="#FFFFFF",
    body_text_color_subdued="#475569",
    body_text_color_subdued_dark="#94A3B8",
    block_background_fill="rgba(255, 255, 255, 0.85)",
    block_background_fill_dark="rgba(26, 27, 35, 0.70)",
    block_border_color="rgba(226, 232, 240, 0.80)",
    block_border_color_dark="rgba(255, 255, 255, 0.08)",
    block_radius="32px",
    input_background_fill="#FFFFFF",
    input_background_fill_dark="rgba(18, 19, 27, 0.85)",
    input_border_color="rgba(226, 232, 240, 0.90)",
    input_border_color_dark="rgba(255, 255, 255, 0.12)",
    input_radius="9999px",
    button_primary_background_fill="#2563EB",
    button_primary_background_fill_hover="#1D4ED8",
    button_primary_text_color="#FFFFFF",
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap');

/* --- Page & Root Canvas Architecture --- */
:root {
    --canvas-bg: #0B0D14;
    --stage-glow: radial-gradient(circle at 50% 12%, rgba(62, 123, 250, 0.30) 0%, rgba(62, 123, 250, 0.14) 35%, rgba(11, 13, 20, 0) 70%);
    --stage-card-bg: rgba(26, 27, 35, 0.70);
    --stage-card-fallback: rgba(26, 27, 35, 0.95);
    --stage-card-border: rgba(255, 255, 255, 0.08);
    --avatar-glow: 0 0 0 3px rgba(62, 123, 250, 0.25);
    --avatar-glow-active: 0 0 15px rgba(59, 130, 246, 0.5), 0 0 0 3px rgba(62, 123, 250, 0.4);
    --text-primary: #FFFFFF;
    --text-secondary: #94A3B8;
    --text-placeholder: #64748B;
    --pill-bg: rgba(255, 255, 255, 0.04);
    --pill-border: rgba(255, 255, 255, 0.10);
    --pill-text: #E2E8F0;
    --pill-hover-bg: rgba(62, 123, 250, 0.15);
    --pill-hover-border: rgba(96, 165, 250, 0.4);
    --input-dock-bg: rgba(18, 19, 27, 0.85);
    --input-dock-border: rgba(255, 255, 255, 0.12);
    --send-btn-bg: #2563EB;
    --send-btn-hover: #1D4ED8;
    --chat-bubble-user-bg: #2563EB;
    --chat-bubble-user-text: #FFFFFF;
    --chat-bubble-bot-bg: rgba(30, 32, 42, 0.85);
    --chat-bubble-bot-border: rgba(255, 255, 255, 0.08);
    --chat-bubble-bot-text: #F1F5F9;
    --footer-text: #64748B;
    --avatar: clamp(40px, 7.5vh, 60px);

    /* Vertical budget: page = pad-top + header + gap + CARD + footer + pad-bottom */
    --pad-top: clamp(0.75rem, 3vh, 2.5rem);
    --pad-bot: clamp(0.5rem, 1.5vh, 1.5rem);
    --header-h: clamp(128px, 23vh, 200px);
    --header-gap: clamp(0.5rem, 2vh, 1.25rem);
    --footer-h: 2.25rem;
    --slack: 3.5rem;                       /* room for Gradio's own gaps between blocks */
    --card-pad-top: clamp(0.75rem, 3vh, 2rem);
    --card-pad-bot: clamp(0.75rem, 2vh, 1.5rem);
    --dock-h: 56px;
    --subtext-h: 0rem;                     /* provenance subtext was removed */
    --card-h: max(24rem, calc(100vh - var(--pad-top) - var(--pad-bot) - var(--header-h) - var(--header-gap) - var(--footer-h) - var(--slack)));
    --card-h: max(24rem, calc(100dvh - var(--pad-top) - var(--pad-bot) - var(--header-h) - var(--header-gap) - var(--footer-h) - var(--slack)));
    --chat-h: calc(var(--card-h) - var(--card-pad-top) - var(--card-pad-bot) - var(--dock-h) - var(--subtext-h) - 1.75rem);
}

body:not(.dark) {
    --canvas-bg: #FAFBFD;
    --stage-glow: radial-gradient(circle at 50% 12%, rgba(165, 160, 240, 0.55) 0%, rgba(147, 197, 253, 0.35) 38%, rgba(243, 244, 246, 0) 70%);
    --stage-card-bg: rgba(255, 255, 255, 0.85);
    --stage-card-fallback: rgba(255, 255, 255, 0.98);
    --stage-card-border: rgba(226, 232, 240, 0.80);
    --avatar-glow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    --avatar-glow-active: 0 0 20px rgba(96, 165, 250, 0.5), 0 0 0 3px rgba(37, 99, 235, 0.15);
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-placeholder: #94A3B8;
    --pill-bg: rgba(255, 255, 255, 0.90);
    --pill-border: rgba(203, 213, 225, 0.60);
    --pill-text: #334155;
    --pill-hover-bg: rgba(241, 245, 249, 1.00);
    --pill-hover-border: rgba(96, 165, 250, 0.6);
    --input-dock-bg: #FFFFFF;
    --input-dock-border: rgba(226, 232, 240, 0.90);
    --send-btn-bg: #2563EB;
    --send-btn-hover: #1D4ED8;
    --chat-bubble-user-bg: #2563EB;
    --chat-bubble-user-text: #FFFFFF;
    --chat-bubble-bot-bg: #FFFFFF;
    --chat-bubble-bot-border: rgba(226, 232, 240, 0.8);
    --chat-bubble-bot-text: #1E293B;
    --footer-text: #94A3B8;
}

html, body {
    background-color: var(--canvas-bg) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    min-height: 100vh;
    min-height: 100dvh;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    overflow-y: auto;
    overscroll-behavior: none;
    scrollbar-width: none;            /* Firefox */
    -ms-overflow-style: none;
}

html::-webkit-scrollbar, body::-webkit-scrollbar { display: none; }  /* Chrome / Safari */

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 100vh;
    background: var(--stage-glow);
    pointer-events: none;
    z-index: 0;
}

.gradio-container {
    position: relative;
    z-index: 1;
    width: min(94vw, 860px) !important;
    max-width: 860px !important;
    min-height: 100vh !important;
    min-height: 100dvh !important;
    height: auto !important;
    overflow: visible !important;
    margin: 0 auto !important;
    padding: var(--pad-top) 1rem var(--pad-bot) !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
}

footer {
    display: none !important;
}

.gradio-container, .gradio-container > .main, .gradio-container .wrap {
    background: transparent !important;
}

.gradio-container .form, .gradio-container .block:has(textarea) {
    background: transparent !important;
}

/* --- Header Avatar & Persona Presence --- */
.twin-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: var(--header-h);
    margin-bottom: var(--header-gap);
    text-align: center;
    animation: fadeInDown 0.6s ease-out;
    flex-shrink: 0;
    overflow: hidden;
}

.avatar-wrapper {
    position: relative;
    width: calc(var(--avatar) + 8px);
    height: calc(var(--avatar) + 8px);
    margin-bottom: clamp(0.35rem, 1.2vh, 0.75rem);
}

.avatar-img-ring {
    width: var(--avatar);
    height: var(--avatar);
    border-radius: 50%;
    overflow: hidden;
    margin: 2px auto;
    box-shadow: var(--avatar-glow-active);
    background: #1E293B;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.avatar-img-ring:hover {
    transform: scale(1.04);
}

.avatar-img-ring img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-initials {
    color: #FFFFFF;
    font-size: 1.25rem;
    font-weight: 700;
}

.avatar-badge {
    position: absolute;
    bottom: 2px;
    right: 2px;
    width: 14px;
    height: 14px;
    background: #38BDF8;
    border: 2px solid var(--canvas-bg);
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(56, 189, 248, 0.8);
}

.persona-name {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    margin: 0 0 0.15rem 0;
    line-height: 1.2;
}

.linkedin-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    margin-top: clamp(0.3rem, 1vh, 0.6rem);
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    line-height: 1.4;
    color: var(--pill-text) !important;
    background: var(--pill-bg);
    border: 1px solid var(--pill-border);
    border-radius: 9999px;
    text-decoration: none !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.linkedin-pill:hover, .linkedin-pill:focus-visible {
    background: var(--pill-hover-bg);
    border-color: var(--pill-hover-border);
    transform: translateY(-1px);
    outline: none;
}

.persona-name a {
    color: inherit !important;
    text-decoration: none !important;
    border-bottom: 1px solid transparent;
    transition: color 0.2s ease, border-color 0.2s ease;
}

.persona-name a:hover, .persona-name a:focus-visible {
    color: #2563EB !important;
    border-bottom-color: currentColor;
    outline: none;
}

.persona-subtitle {
    font-size: 0.875rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    color: var(--text-secondary);
    margin: 0;
}

/* --- Central Stage Card (column wrapping hero, pills, dock, subtext) --- */
.stage-card {
    background: var(--stage-card-fallback) !important;
    background: var(--stage-card-bg) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border: 1px solid var(--stage-card-border) !important;
    border-radius: 2rem !important;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.25) !important;
    width: 100% !important;
    max-width: 860px !important;
    height: var(--card-h) !important;
    min-height: 0 !important;
    max-height: var(--card-h) !important;
    overflow: hidden !important;
    flex: 0 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    margin: 0 auto !important;
    padding: var(--card-pad-top) 2rem var(--card-pad-bot) !important;
    box-sizing: border-box !important;
    gap: 0 !important;
}

.chatbot-stage, .chatbot-stage > .wrapper, #chat-it, #chat-en {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

.chatbot-stage {
    height: var(--chat-h) !important;
    min-height: 0 !important;
    max-height: var(--chat-h) !important;
    flex: 0 0 auto !important;
    overflow: hidden !important;
}

.chatbot-stage > .wrapper {
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
}

#chat-it.chatbot-stage, #chat-en.chatbot-stage {
    height: var(--chat-h) !important;
    min-height: 0 !important;
    max-height: var(--chat-h) !important;
}

/* Greeting block must not stretch to fill the area (that created the big gap between title and pills) */
.placeholder-content > .placeholder {
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Greeting state: center hero + pills in the chat area */
.chatbot-stage .bubble-wrap, .chatbot-stage .panel-wrap {
    height: 100% !important;
    max-height: 100% !important;
    overflow-y: auto !important;
    scrollbar-width: thin;
}

.placeholder-content {
    min-height: 100% !important;
    height: auto !important;
    justify-content: center !important;
    box-sizing: border-box;
}

/* Hide the Gradio top-right toolbar buttons (clear, copy, share, etc.) */
.icon-button-wrapper.top-panel,
.top-panel,
button[aria-label="Clear"],
button[aria-label="Cancella"],
button[title="Clear"],
button[title="Cancella"],
.icon-button-wrapper:has(button[aria-label="Clear"]),
.icon-button-wrapper:has(button[aria-label="Cancella"]) {
    display: none !important;
}

/* Inside the chatbot stage */
.bubble-wrap, .panel-wrap {
    padding: 0 !important;
}

/* --- Hero Greeting & Stage Placeholder --- */
.placeholder-content {
    gap: 0 !important;
    padding: 0 !important;
}

.hero-stage {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0;
    animation: fadeIn 0.5s ease-out;
}

.hero-greeting {
    font-size: clamp(1.5rem, 4.5vh, 2.25rem);
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.25;
    color: var(--text-primary);
    margin: 0 0 clamp(0.35rem, 1vh, 0.75rem) 0;
    max-width: 640px;
}

.hero-description {
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 540px;
    margin: 0 auto;
}

/* --- Suggestion Pills Flow --- */
.examples, [role="list"].examples {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 0.5rem 0.75rem !important;
    margin: clamp(0.5rem, 1.5vh, 1rem) auto clamp(0.5rem, 2vh, 1.25rem) !important;
    max-width: 100% !important;
}

button.example, .examples button, [class*="example"] > button {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: var(--pill-bg) !important;
    border: 1px solid var(--pill-border) !important;
    border-radius: 9999px !important;
    padding: 0.45rem 1rem !important;
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    color: var(--pill-text) !important;
    cursor: pointer !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    height: auto !important;
    min-height: 0 !important;
}

button.example {
    width: auto !important;
    max-width: 100% !important;
    flex: 0 0 auto !important;
}

button.example .example-content, button.example .example-text-content {
    width: auto !important;
    flex: 0 0 auto !important;
    padding: 0 !important;
}

button.example:hover, .examples button:hover, [class*="example"] > button:hover {
    background: var(--pill-hover-bg) !important;
    border-color: var(--pill-hover-border) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(62, 123, 250, 0.15) !important;
}

button.example .example-text, .examples button span {
    color: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
}

/* --- Docked Input Bar Architecture --- */
/* Center the form / row inside the ChatInterface */
form:has(textarea), .block:has(textarea), div:has(> textarea) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0.5rem auto 0.25rem !important;
    width: 100% !important;
    max-width: 780px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    position: relative !important;
    flex-shrink: 0 !important;
}

.gradio-row:has(textarea), div.row:has(textarea) {
    background: var(--input-dock-bg) !important;
    border: 1px solid var(--input-dock-border) !important;
    border-radius: 9999px !important;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15) !important;
    padding: 4px 8px 4px 24px !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: center !important;
    height: var(--dock-h) !important;
    min-height: var(--dock-h) !important;
    max-height: var(--dock-h) !important;
    box-sizing: border-box !important;
    gap: 8px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.gradio-row:has(textarea):focus-within, div.row:has(textarea):focus-within {
    border-color: rgba(37, 99, 235, 0.6) !important;
    box-shadow: 0 6px 24px rgba(37, 99, 235, 0.2) !important;
}

/* Textarea wrapper & container */
.gradio-row:has(textarea) > *, div.row:has(textarea) > * {
    display: flex !important;
    align-items: center !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Textarea inside input dock */
textarea, input[type=text] {
    box-sizing: border-box !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    color: var(--text-primary) !important;
    font-size: 0.9375rem !important;
    font-weight: 400 !important;
    height: 34px !important;
    min-height: 34px !important;
    max-height: 34px !important;
    line-height: 34px !important;
    padding: 0 !important;
    margin: 0 !important;
    flex: 1 1 auto !important;
    align-self: center !important;
    display: flex !important;
    align-items: center !important;
}

textarea::placeholder, input[type=text]::placeholder {
    color: var(--text-placeholder) !important;
    opacity: 1 !important;
    font-size: 0.9375rem !important;
    line-height: 34px !important;
}

/* Circular Send & Stop Action Buttons */
button[class*="submit"], button[class*="stop"] {
    box-sizing: border-box !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    flex: 0 0 40px !important;
    border-radius: 50% !important;
    background: var(--send-btn-bg) !important;
    border: none !important;
    color: #FFFFFF !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
    align-self: center !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.35) !important;
    transition: transform 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease !important;
}

button[class*="submit"]:hover, button[class*="stop"]:hover {
    background: var(--send-btn-hover) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 3px 10px rgba(37, 99, 235, 0.5) !important;
}

button[class*="submit"] svg, button[class*="stop"] svg {
    width: 18px !important;
    height: 18px !important;
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
    margin: auto !important;
}

/* --- Provenance Subtext & Copyright Notice --- */
.stage-subtext {
    text-align: center;
    font-size: 0.75rem;
    line-height: 1.4;
    color: var(--footer-text);
    margin: 0.5rem 0 0;
    height: calc(var(--subtext-h) - 0.5rem);
    overflow: hidden;
    flex-shrink: 0;
}

.twin-copyright {
    text-align: center;
    font-size: 0.72rem;
    color: var(--footer-text);
    margin-top: 0;
    padding-top: 0;
    height: var(--footer-h);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.8;
    flex-shrink: 0;
}

/* --- Message Bubbles Styling ---
   Gradio nests two .message elements: the outer role wrapper (.bot.message / .user.message)
   and the inner .message that holds the text. Only the inner one is the visible bubble. */
.bot.message, .user.message {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
    max-width: 100% !important;
}

.bot.message .message, .user.message .message {
    border-radius: 16px !important;
    padding: 8px 13px !important;
    font-size: 0.9375rem !important;
    line-height: 1.5 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
}

.message p {
    margin: 0 0 0.35rem 0 !important;
}

.message p:last-child {
    margin-bottom: 0 !important;
}

.user.message .message {
    background: var(--chat-bubble-user-bg) !important;
    border: none !important;
    border-radius: 16px 16px 4px 16px !important;
}

.user.message .message, .user.message .message * {
    color: #FFFFFF !important;
}

.bot.message .message {
    background: var(--chat-bubble-bot-bg) !important;
    border: 1px solid var(--chat-bubble-bot-border) !important;
    border-radius: 16px 16px 16px 4px !important;
}

.bot.message .message, .bot.message .message * {
    color: var(--chat-bubble-bot-text) !important;
}

/* Typing animated dots indicator */
.typing {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    height: 20px;
}

.typing span {
    font-size: 9px;
    line-height: 1;
    color: #94A3B8;
    animation: typingPulse 1.2s infinite ease-in-out;
}

.typing span:nth-child(2) { animation-delay: .2s; }
.typing span:nth-child(3) { animation-delay: .4s; }

@keyframes typingPulse {
    0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
    30% { opacity: 1; transform: translateY(-3px); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* --- Responsive --- */
/* Short windows: tighten everything, drop the least important text */
@media (max-height: 760px) {
    :root { --dock-h: 48px; }
    .persona-name { font-size: 1.25rem; }
    .persona-subtitle { font-size: 0.8rem; }
    .stage-card { border-radius: 1.5rem !important; }
    .gradio-row:has(textarea), div.row:has(textarea) {
        height: 48px !important; min-height: 48px !important; max-height: 48px !important;
    }
    button[class*="submit"], button[class*="stop"] {
        width: 36px !important; min-width: 36px !important; max-width: 36px !important;
        height: 36px !important; min-height: 36px !important; max-height: 36px !important;
        flex: 0 0 36px !important;
    }
}

@media (max-height: 620px) {
    :root { --footer-h: 0rem; --header-h: 100px; }
    .persona-subtitle, .linkedin-pill, .stage-subtext, .twin-copyright { display: none !important; }
}

/* Narrow windows / phones */
@media (max-width: 720px) {
    .gradio-container { padding-left: 0.75rem !important; padding-right: 0.75rem !important; }
    .stage-card { padding-left: 1rem !important; padding-right: 1rem !important; border-radius: 1.5rem !important; }
    .hero-greeting { font-size: clamp(1.35rem, 6.2vw, 1.9rem); }
    button.example, .examples button { font-size: 0.8125rem !important; padding: 0.4rem 0.9rem !important; text-align: left !important; }
    .gradio-row:has(textarea), div.row:has(textarea) { padding-left: 16px !important; }
    .stage-subtext { font-size: 0.7rem; }
}

@media (max-width: 420px) {
    .persona-name { font-size: 1.15rem; }
    .hero-greeting { font-size: 1.3rem; }
}

/* Hide unneeded elements */
.avatar-container, .avatar-image {
    display: none !important;
}
"""


def _mime(data: bytes) -> str:
    """Detect image type from signature."""
    if data.startswith(b"\x89PNG"):
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return "jpeg"


def _photo_html() -> str:
    """Generate circular portrait or initials."""
    data = None
    if encoded := os.getenv("AVATAR_B64"):
        try:
            data = base64.b64decode(encoded)
        except ValueError:
            print("[ui] AVATAR_B64 is not valid base64, using local asset")
    if data is None:
        for ext in ("jpg", "jpeg", "png", "webp"):
            path = ASSETS / f"avatar.{ext}"
            if path.exists():
                data = path.read_bytes()
                break
    if data is None:
        initials = "".join(w[0] for w in DISPLAY_NAME.split()[:2]).upper()
        return f'<div class="avatar-initials">{initials}</div>'
    encoded = base64.b64encode(data).decode()
    return f'<img src="data:image/{_mime(data)};base64,{encoded}" alt="{DISPLAY_NAME}">'


def header_html() -> str:
    """Render floating header avatar cluster and persona presence."""
    return (
        f'<div class="twin-header">'
        f'<div class="avatar-wrapper">'
        f'<div class="avatar-img-ring">{_photo_html()}</div>'
        f'<div class="avatar-badge" title="Verified Digital Twin"></div>'
        f'</div>'
        f'<h2 class="persona-name">'
        f'{DISPLAY_NAME}'
        f'</h2>'
        f'<p class="persona-subtitle">Digital Twin</p>'
        f'<a class="linkedin-pill" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a>'
        f'</div>'
    )


def placeholder_html(lang: str) -> str:
    """Hero greeting and model training notice inside the main stage card."""
    if lang == "it":
        return (
            '<div class="hero-stage">'
            '<h1 class="hero-greeting">Chiedimi di esperienza, competenze e progetti.</h1>'
            '<p class="hero-description">'
            'Istruito sulla traiettoria professionale verificata di Antonio, ingegneria dei sistemi, '
            'filosofia di design e casi di studio di produzione.'
            '</p>'
            '</div>'
        )
    return (
        '<div class="hero-stage">'
        '<h1 class="hero-greeting">Ask me about my experience, skills and projects.</h1>'
        '</div>'
    )


def subtext_html(lang: str) -> str:
    """Provenance and inquiry notice below the input dock."""
    if lang == "it":
        return (
            '<div class="stage-subtext">'
             
            '</div>'
        )
    return (
        '<div class="stage-subtext">'
         
        '</div>'
    )


def footer_html() -> str:
    """Copyright bar."""
    return (
        f'<div class="twin-copyright">'
        f'© 2026 {DISPLAY_NAME}. All rights reserved.'
        f'</div>'
    )
