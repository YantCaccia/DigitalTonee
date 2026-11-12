# DigitalTonee

A chatbot that answers professional and career-related questions **as you**, based on your CV and LinkedIn profile. Let them ask about your experience, skills and availability.

Built with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), the **Gemini API** (via its OpenAI-compatible endpoint) and [Gradio](https://www.gradio.app/). It runs entirely on free tiers.

## Features

- Answers in the first person, in the language of the question (the interface also follows the visitor's browser language: Italian or English).
- Your documents (CV, LinkedIn, a hand-written "about me" file) are injected into the system prompt: no vector database needed for a few pages of text.
- Two tools: the twin records recruiters' contact details and the questions it could not answer. Both are saved to `logs/` and, optionally, sent to you on Telegram.
- iMessage-style interface, with a rate limit per visitor, a message length cap and prompt-injection rules.
- Personal data never lives in the repository: documents are read from `data/` locally, or from environment variables (Secrets) when deployed.

## How it works

```
data/cv.md, data/linkedin.md, data/about.md   ->  system prompt  ->  Agent (Agents SDK) -> Gemini
                                                                        |-> record_contact
                                                                        |-> record_unknown_question
```

## Quick start

You need [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS, `winget install --id astral-sh.uv` on Windows) and a free API key from [Google AI Studio](https://aistudio.google.com/).

```bash
uv sync
cp .env.example .env        # then set GEMINI_API_KEY and OWNER_NAME
```

Add your documents to `data/`. Templates are provided:

| File | What it contains |
|---|---|
| `data/cv.md` | your CV (copy `data/cv.example.md`) |
| `data/linkedin.md` | your LinkedIn profile (copy `data/linkedin.example.md`) |
| `data/about.md` | tone of voice, what you are looking for, FAQ, example answers (copy `data/about.example.md`) |

You can also generate `cv.md` and `linkedin.md` from PDFs: put `cv.pdf` and `linkedin.pdf` in `data/` and run

```bash
uv run --group parse python scripts/parse_pdfs.py
```

then **review the generated Markdown by hand**: PDF extraction is never perfect. Everything in `data/` except the `*.example.md` templates is git-ignored.

Run the app:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 7860    # http://127.0.0.1:7860
```

## Configuration

All settings are environment variables (see `.env.example`):

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | required |
| `GEMINI_MODEL` | Gemini model name |
| `GEMINI_REASONING_EFFORT` | optional, e.g. `minimal` or `low`: lower means faster answers |
| `GEMINI_FALLBACK_MODEL` | model used when the main one returns 429 or is overloaded (empty disables it; quotas are per model) |
| `GLOBAL_RPM`, `GLOBAL_RPD` | global cap on messages per minute / per day. A message costs 1-2 Gemini requests, so set `GLOBAL_RPM` to half of your model's RPM |
| `OWNER_NAME`, `DISPLAY_NAME`, `LINKEDIN_URL` | name used in the prompt, name and link shown in the header |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | optional notifications |
| `CV_MD`, `LINKEDIN_MD`, `ABOUT_MD` | the documents' text, used instead of `data/*.md` (for deployments) |

Put your photo in `assets/avatar.jpg` (square, a few hundred pixels; `.png` and `.webp` work too). Without it the header shows your initials. The photo is git-ignored, so on a deployment pass it as the `AVATAR_B64` secret (base64 of a small image, e.g. `base64 -i assets/avatar.jpg | tr -d '\n' | pbcopy` on macOS; keep the image under ~50 KB).

### Telegram notifications (optional)

Create a bot with [@BotFather](https://t.me/BotFather) to get the token, send it a message, then read your chat id from `https://api.telegram.org/bot<TOKEN>/getUpdates`. Without Telegram, contacts and unanswered questions are only written to `logs/*.jsonl`.

## Deploy for free on Render

Hugging Face Spaces now requires a paid plan for Gradio apps, so this project deploys to a free [Render](https://render.com) web service (`render.yaml` is included).

1. Generate the requirements file (Render installs dependencies from it) and commit it:
   ```bash
   uv export --no-hashes --no-dev --no-emit-project -o requirements.txt
   ```
2. On Render: **New > Blueprint**, connect the GitHub repository and apply `render.yaml`. Render asks for the values marked `sync: false`: the API key, the three documents (`CV_MD`, `LINKEDIN_MD`, `ABOUT_MD`), the photo (`AVATAR_B64`), Telegram and the other settings above. `pbcopy < data/cv.md` is a convenient way to copy a document on macOS.
3. Wait for the build, then open the `onrender.com` URL and try it.

Notes:
- A free service is spun down after 15 minutes without traffic and takes about a minute to wake up. Open it once before sending the link around, or ping it periodically.
- The filesystem is not persistent, so `logs/` is lost on restart: Telegram is the reliable way to receive contacts.
- The app listens on the `PORT` that Render provides.
- The Gemini free tier has low rate limits, and free-tier data may be used by Google to improve its products. Tell visitors not to share sensitive information.

## Project structure

```
app.py               Gradio app: two chats (it/en), language switch, streaming, rate limit
twin/agent.py        system prompt and Agents SDK agent (Gemini through the OpenAI-compatible API)
twin/tools.py        record_contact, record_unknown_question
twin/notify.py       logs/*.jsonl and Telegram
twin/ui.py          theme, CSS and header
scripts/parse_pdfs.py  PDF -> Markdown (optional "parse" dependency group)
data/                your documents (git-ignored) and *.example.md templates
```

## License

MIT, see [LICENSE](LICENSE). PDF parsing uses PyMuPDF, which is AGPL-licensed; it is an optional dependency used only by `scripts/parse_pdfs.py` and is not needed to run or deploy the app.
