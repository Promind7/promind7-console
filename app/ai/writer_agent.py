"""
Agent de rédaction ProMind7 — scripts, darija, ancrage sources.

Backends : **Claude** (Anthropic) ou **OpenAI**, selon les clés disponibles.

Règles : pas d'invention de faits ; citer les URLs fournies ; suivre style_guide + overrides
+ writer_editing_instructions (édition / révision).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Sequence

from ai.document_loaders import load_local_reference, read_text_file
from ai.paths import (
    content_root,
    style_guide_path,
    writer_editing_instructions_path,
    writer_mba_agent_consignes_path,
    writer_overrides_path,
)
from ai.research_tools import format_sources_for_prompt, search_videos, search_web

Provider = Literal["anthropic", "openai"]


@dataclass
class WriterResult:
    assistant_markdown: str
    sources_markdown: str
    error: str | None = None


def _build_system_prompt(
    style_guide: str,
    overrides: str,
    reference_snippet: str,
) -> str:
    ref = (
        f"\n## Extrait de référence (imiter le style, pas copier)\n{reference_snippet}\n"
        if reference_snippet.strip()
        else ""
    )
    ov = overrides.strip() or "(Aucune règle supplémentaire pour l'instant.)"
    return f"""Tu es l'agent de rédaction ProMind7 pour la formation en ligne (promind7.com).

## Guide de style interne (obligatoire)
{style_guide}

## Règles personnelles / apprentissage (obligatoire)
{ov}

## Consignes anti-hallucination
- N'invente **aucun** chiffre, date, loi, citation ou statistique qui ne figure pas explicitement dans le contexte fourni (sources web, document utilisateur, ou consigne).
- Si une information manque, dis-le clairement et propose une formulation prudente ou des questions de clarification.
- Pour la **darija** (arabe dialectal marocain) : reste naturel et réaliste ; si tu n'es pas sûr d'une expression, indique une alternative ou laisse un marqueur [à valider darija].
- Structure en markdown clair (titres ## ###, listes, gras pour les idées clés).
- Termine par une section **Sources** listant les URLs utilisées ; si aucune source externe, écris "Sources : consigne utilisateur + guide interne uniquement."

{ref}
"""


def _resolve_provider(
    explicit: Provider | None,
    anthropic_key: str,
    openai_key: str,
) -> tuple[Provider, str] | tuple[None, str]:
    """
    Choisit le backend et la clé.
    PROMIND7_WRITER_PROVIDER=anthropic|openai force le fournisseur (si la clé existe).
    Sinon : Claude si ANTHROPIC_API_KEY, sinon OpenAI si OPENAI_API_KEY.
    """
    forced = (os.getenv("PROMIND7_WRITER_PROVIDER") or "").strip().lower()
    if explicit:
        forced = explicit

    if forced == "openai":
        if openai_key:
            return "openai", openai_key
        return None, "openai"
    if forced == "anthropic":
        if anthropic_key:
            return "anthropic", anthropic_key
        return None, "anthropic"

    if anthropic_key:
        return "anthropic", anthropic_key
    if openai_key:
        return "openai", openai_key
    return None, ""


def _call_openai(messages: List[dict], model: str, api_key: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )
    return (resp.choices[0].message.content or "").strip()


def _call_anthropic(
    system: str,
    claude_messages: List[dict],
    model: str,
    api_key: str,
) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    out = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system,
        messages=claude_messages,
        temperature=0.5,
    )
    parts: List[str] = []
    for block in out.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "".join(parts).strip()


def run_writer_request(
    user_message: str,
    *,
    history: Sequence[dict] | None = None,
    use_web: bool = False,
    use_videos: bool = False,
    research_query: str | None = None,
    uploaded_reference_text: str | None = None,
    local_reference_path: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
    provider: Provider | None = None,
    anthropic_api_key: str | None = None,
    openai_api_key: str | None = None,
    inject_lesson_corpus: bool = False,
    lesson_corpus_pack_root: str | None = None,
) -> WriterResult:
    """
    api_key : rétrocompatibilité — traité comme clé OpenAI si aucune autre logique.
    anthropic_api_key / openai_api_key : préférences explicites (ex. depuis Streamlit secrets).
    lesson_corpus_pack_root : si ``inject_lesson_corpus``, racine du pack à lire (sinon env / Stage & emploi).
    """
    oa = (openai_api_key or os.getenv("OPENAI_API_KEY") or "").strip()
    an = (anthropic_api_key or os.getenv("ANTHROPIC_API_KEY") or "").strip()
    # Ancien paramètre unique = OpenAI uniquement
    if api_key and api_key.strip():
        oa = api_key.strip()

    resolved = _resolve_provider(provider, an, oa)
    if resolved[0] is None:
        need = resolved[1]
        if need == "openai":
            return WriterResult(
                "",
                "",
                error="Clé **OPENAI_API_KEY** manquante (fournisseur forcé à OpenAI).",
            )
        if need == "anthropic":
            return WriterResult(
                "",
                "",
                error="Clé **ANTHROPIC_API_KEY** manquante (fournisseur forcé à Claude).",
            )
        return WriterResult(
            "",
            "",
            error=(
                "Aucune clé LLM : définissez **ANTHROPIC_API_KEY** (Claude, recommandé) "
                "ou **OPENAI_API_KEY** dans l'environnement ou `.streamlit/secrets.toml`."
            ),
        )

    backend, key = resolved

    sg_path = style_guide_path()
    style_guide = read_text_file(sg_path) if sg_path.is_file() else "# (style_guide.md absent)"
    wo_path = writer_overrides_path()
    overrides = read_text_file(wo_path) if wo_path.is_file() else ""
    parcours_path = content_root() / "parcours_stage_emploi_consignes.md"
    parcours_block = (
        read_text_file(parcours_path, max_chars=20_000)
        if parcours_path.is_file()
        else ""
    )
    edit_path = writer_editing_instructions_path()
    editing_block = (
        read_text_file(edit_path, max_chars=20_000) if edit_path.is_file() else ""
    )
    mba_path = writer_mba_agent_consignes_path()
    mba_block = read_text_file(mba_path, max_chars=30_000) if mba_path.is_file() else ""

    ref_parts: List[str] = []
    if uploaded_reference_text and uploaded_reference_text.strip():
        ref_parts.append("### Document téléchargé\n" + uploaded_reference_text.strip()[:20_000])
    if local_reference_path and local_reference_path.strip():
        txt, err = load_local_reference(local_reference_path)
        if err:
            return WriterResult("", "", error=f"Référence locale : {err}")
        if txt:
            ref_parts.append("### Fichier local\n" + txt)
    reference_block = "\n\n".join(ref_parts)

    sources_md = ""
    research_block = ""
    q = (research_query or user_message).strip()[:500]
    if use_web or use_videos:
        text_hits = search_web(q) if use_web else []
        video_hits = search_videos(q) if use_videos else []
        research_block = format_sources_for_prompt(text_hits, video_hits)
        sources_md = research_block

    system = _build_system_prompt(style_guide, overrides, reference_block)
    if editing_block.strip():
        system += (
            "\n\n## Agent d’édition / révision (obligatoire)\n"
            + editing_block.strip()
        )
    if parcours_block.strip():
        system += (
            "\n\n## Parcours Stage & emploi (cohérence équipe)\n"
            + parcours_block.strip()
        )
    if mba_block.strip():
        system += (
            "\n\n## Brief MBA / technicien & parcours (obligatoire)\n"
            + mba_block.strip()
        )

    user_blocks: List[str] = []
    env_corpus = (os.getenv("PROMIND7_WRITER_INJECT_LESSON_CORPUS") or "").strip().lower()
    do_corpus = inject_lesson_corpus or env_corpus in ("1", "true", "yes", "on")
    if do_corpus:
        from ai.lesson_corpus import build_module_corpus_text, mba_corpus_pack_root

        max_c = int(os.getenv("PROMIND7_MBA_CORPUS_MAX_CHARS") or "70000")
        pack: Path | None = None
        if lesson_corpus_pack_root:
            pr = Path(lesson_corpus_pack_root)
            if pr.is_dir():
                pack = pr
        if pack is None:
            pack = mba_corpus_pack_root()
        if pack:
            corpus = build_module_corpus_text(pack, max_total_chars=max_c)
            if corpus.strip():
                user_blocks.append(
                    "## Corpus leçons (modules ciblés — lire pour cohérence)\n\n"
                    + corpus.strip()
                )
            else:
                user_blocks.append(
                    "## Corpus leçons\n\n"
                    "(Aucun .docx trouvé pour les préfixes de modules configurés "
                    "dans ce dossier pack — fournir les scripts ou vérifier "
                    "`PROMIND7_MBA_CORPUS_PACK_ROOT` / `PROMIND7_MBA_CORPUS_PREFIXES`.)"
                )
        else:
            user_blocks.append(
                "## Corpus leçons\n\n"
                "(Dossier pack introuvable — définir `PROMIND7_MBA_CORPUS_PACK_ROOT`.)"
            )

    if research_block:
        user_blocks.append(research_block)
    user_blocks.append("## Consigne utilisateur\n" + user_message)
    user_content = "\n\n".join(user_blocks)

    try:
        if backend == "openai":
            messages: List[dict] = [{"role": "system", "content": system}]
            if history:
                for m in history:
                    if m.get("role") in ("user", "assistant") and m.get("content"):
                        messages.append({"role": m["role"], "content": m["content"]})
            messages.append({"role": "user", "content": user_content})
            mdl = model or os.getenv("PROMIND7_WRITER_MODEL", "gpt-4o-mini")
            content = _call_openai(messages, mdl, key)
            return WriterResult(assistant_markdown=content, sources_markdown=sources_md or "")

        # Anthropic : system séparé, pas de rôle system dans messages
        claude_messages: List[dict] = []
        if history:
            for m in history:
                if m.get("role") in ("user", "assistant") and m.get("content"):
                    claude_messages.append({"role": m["role"], "content": m["content"]})
        claude_messages.append({"role": "user", "content": user_content})
        mdl = model or os.getenv(
            "PROMIND7_CLAUDE_MODEL",
            "claude-3-5-sonnet-20241022",
        )
        content = _call_anthropic(system, claude_messages, mdl, key)
        return WriterResult(assistant_markdown=content, sources_markdown=sources_md or "")
    except Exception as exc:  # noqa: BLE001
        return WriterResult("", sources_md or "", error=str(exc))
