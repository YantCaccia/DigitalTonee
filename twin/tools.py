from agents import function_tool

from .notify import notify


@function_tool
def record_contact(email: str, name: str = "", notes: str = "") -> str:
    """Registra i dati di contatto di un recruiter o di una persona interessata a contattare il proprietario.

    Args:
        email: Indirizzo email della persona.
        name: Nome della persona, se noto.
        notes: Contesto utile (azienda, ruolo proposto, richieste).
    """
    notify(
        "contacts",
        {"email": email, "name": name, "notes": notes},
        f"📩 Nuovo contatto: {name or 'n/d'} <{email}>\n{notes}",
    )
    return "Contatto registrato."


@function_tool
def record_unknown_question(question: str) -> str:
    """Registra una domanda a cui non sai rispondere con le informazioni disponibili.

    Args:
        question: La domanda dell'utente.
    """
    notify("unknown_questions", {"question": question}, f"❓ Domanda senza risposta:\n{question}")
    return "Domanda registrata."
