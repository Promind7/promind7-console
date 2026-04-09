"""
Navigateur par parcours : leçons .docx — aperçu du script Word courant + téléchargement.
Lecture : jumeau ``-V2`` si présent, sinon fichier canonique seul (ex. copie sans suffixe V2 sur disque).

Pack **Stage & emploi** : aligné sur *Architecture plateforme Promind7* **§5.2** (phases, unités Tutor #1–#20).
Sous-onglets **Script** et **Vidéos veille** (sommaire structuré : à refaire plus tard).
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from ui.stage_emploi_architecture_view import render_stage_emploi_architecture_tab
from services.stage_emploi_service import (
    V2_DIRNAME,
    SOURCES_DIRNAME,
    CONSOLIDATED_VEILLE_VIDEOS_FILENAME,
    canonical_lesson_number_from_stem,
    canonical_word_docx_v2_path,
    normalize_script_display_stem,
    resolve_lesson_script_docx_path,
    consolidated_veille_videos_path,
    format_module_bucket_label,
    format_preview_html_docx_rich,
    format_preview_html_lecture,
    get_pack_root,
    lesson_local_number_by_rel,
    lesson_select_display_labels,
    LIVE_SEGMENT_CAPTION_FR,
    list_lesson_docx_files,
    load_script_text,
    module_bucket_for_rel,
    ordered_module_buckets,
    stage_emploi_script_jump_session_key,
)

_MODULE_FILTER_ALL = "__ALL__"
_STAGE_EMPLOI_PACK = "Parcours stage & emploi"


def _lesson_title_from_filename(filename: str) -> str:
    return normalize_script_display_stem(Path(filename).stem)


def _safe_key_fragment(rel_posix: str) -> str:
    return rel_posix.replace("/", "_").replace("\\", "_").replace("&", "_")[:96]


def _render_docx_preview_block(
    docx_path: Path,
    *,
    rel_caption: str,
    download_label: str,
    key_slug: str,
    sk: str,
    version_tag: str,
) -> None:
    text, err = load_script_text(docx_path)
    if err:
        st.error(err)
        return

    st.caption(f"`{rel_caption}`")

    try:
        docx_bytes = docx_path.read_bytes()
    except OSError as e:
        st.error(f"Impossible de lire le fichier Word : {e}")
        return

    dl_name = f"{normalize_script_display_stem(docx_path.stem)}.docx"
    st.download_button(
        label=download_label,
        data=docx_bytes,
        file_name=dl_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key=f"dl_docx_{version_tag}_{key_slug}_{sk}",
        use_container_width=False,
    )

    force_rtl = True
    rich_html = None
    if docx_path.suffix.lower() == ".docx":
        rich_html = format_preview_html_docx_rich(docx_path, force_rtl=force_rtl)
    if rich_html:
        components.html(rich_html, height=680, scrolling=True)
    else:
        components.html(
            format_preview_html_lecture(text, force_rtl=force_rtl, variant="lecture"),
            height=680,
            scrolling=True,
        )


def render_script_browser_at_path(
    root: Path,
    *,
    display_name: str,
    key_slug: str,
    missing_folder_hint: str | None = None,
    page_heading: str | None = None,
) -> None:
    """
    Aperçu du script Word + export .docx : jumeau ``-V2`` si présent, sinon fichier canonique seul.

    ``key_slug`` : identifiant stable pour les clés Streamlit.
    ``page_heading`` : si renseigné, remplace le sous-titre par défaut « Scripts — {display_name} ».
    """
    st.subheader(page_heading if page_heading is not None else f"Scripts — {display_name}")

    if not root.is_dir():
        hint = missing_folder_hint or (
            "Créez ce dossier sous `Input/Script/` (ou le chemin indiqué), puis y placez les .docx."
        )
        st.info(
            f"Le dossier pour **{display_name}** n’existe pas encore.\n\n"
            f"**Chemin attendu :** `{root}`\n\n{hint}"
        )
        return

    jump_key = stage_emploi_script_jump_session_key(key_slug)
    if jump_key in st.session_state:
        rel_jump = st.session_state.pop(jump_key)
        if isinstance(rel_jump, str) and rel_jump.strip():
            b_jump = module_bucket_for_rel(rel_jump)
            st.session_state[f"smod_{key_slug}"] = b_jump
            st.session_state[f"slesson_{key_slug}_{b_jump}"] = rel_jump.strip()

    all_files = list_lesson_docx_files(root)
    local_by_rel = lesson_local_number_by_rel(all_files)
    bucket_keys = ordered_module_buckets(all_files)
    mod_options: list[str] = [_MODULE_FILTER_ALL] + bucket_keys
    mod_labels = {
        k: "Tous les modules" if k == _MODULE_FILTER_ALL else format_module_bucket_label(k)
        for k in mod_options
    }

    mod_choice = st.selectbox(
        "Module",
        options=mod_options,
        format_func=lambda k: mod_labels[k],
        key=f"smod_{key_slug}",
    )

    files = all_files
    if mod_choice != _MODULE_FILTER_ALL:
        files = [f for f in files if module_bucket_for_rel(f["rel_posix"]) == mod_choice]

    if not files:
        if all_files:
            st.warning("Aucune leçon dans ce module.")
        else:
            st.info(
                f"Aucun .docx (hors `{SOURCES_DIRNAME}/`, `{V2_DIRNAME}/`, `_exports/`)."
            )
        return

    lesson_labels = lesson_select_display_labels(files, local_by_rel=local_by_rel)
    rel_options = [f["rel_posix"] for f in files]
    choice = st.selectbox(
        "Leçon",
        options=rel_options,
        format_func=lambda rel, _m=lesson_labels: _m[rel],
        key=f"slesson_{key_slug}_{mod_choice}",
    )
    entry = next(f for f in files if f["rel_posix"] == choice)
    sk = _safe_key_fragment(entry["rel_posix"])
    docx_script = resolve_lesson_script_docx_path(root, entry["rel_posix"])
    v2_hint_name = canonical_word_docx_v2_path(root, entry["rel_posix"]).name

    if docx_script is None:
        st.warning(
            "Aperçu et export indisponibles pour cette leçon (fichier de script absent). "
            f"Attendu : soit `{entry['name']}` (canonique), soit `{v2_hint_name}` à côté."
        )
        st.caption(f"Leçon (référence disque) : `{entry['rel_posix']}`")
        return

    v2_rel = docx_script.relative_to(root).as_posix()
    _render_docx_preview_block(
        docx_script,
        rel_caption=v2_rel,
        download_label="Exporter le script (.docx)",
        key_slug=key_slug,
        sk=sk,
        version_tag="script",
    )
    stem = _lesson_title_from_filename(entry["name"])
    seg, loc = local_by_rel.get(entry["rel_posix"], (None, None))
    canon = canonical_lesson_number_from_stem(stem)
    if loc is not None and seg is not None and canon is not None:
        hint_seg = LIVE_SEGMENT_CAPTION_FR.get(seg, "")
        st.caption(
            f"Numérotation affichée : **Leçon {loc}** ({hint_seg}). "
            f"Référence technique (fichiers, `moduleNN`, `--lesson`) : **Leçon {canon}**."
        )
    elif canon is not None:
        st.caption(
            "Référence technique (fichiers, `moduleNN`, `--lesson`) : "
            f"**Leçon {canon}**."
        )


def render_veille_videos_consolidated_tab(
    pack_root: Path,
    *,
    display_name: str,
    key_slug: str,
    missing_folder_hint: str | None = None,
) -> None:
    """Onglet : un seul Markdown (transcripts + idées) pour toutes les vidéos de veille."""
    st.caption(
        "Regroupement des fichiers `Sources/videos/transcripts/*.md` : **transcription** "
        "et **Idées clés** par vidéo."
    )
    if not pack_root.is_dir():
        hint = missing_folder_hint or (
            "Créez ce dossier sous `Input/Script/`, puis y placez les contenus du parcours."
        )
        st.info(
            f"Le dossier pour **{display_name}** n’existe pas encore.\n\n"
            f"**Chemin attendu :** `{pack_root}`\n\n{hint}"
        )
        return

    path = consolidated_veille_videos_path(pack_root)
    if not path.is_file():
        st.warning(
            "Fichier consolidé introuvable. Générez-le avec l’outil de consolidation des transcripts "
            "(script à placer dans ce projet ou à lancer depuis votre environnement de production de contenu), "
            "puis déposez le `.md` à l’emplacement attendu ci-dessous."
        )
        st.caption(f"Chemin attendu : `{path}`")
        return

    text = path.read_text(encoding="utf-8")
    st.download_button(
        label="Télécharger le consolidé (.md)",
        data=text.encode("utf-8"),
        file_name=CONSOLIDATED_VEILLE_VIDEOS_FILENAME,
        mime="text/markdown; charset=utf-8",
        key=f"dl_veille_consolidated_{key_slug}",
    )

    blocks = text.split("\n## VIDEO — ")
    intro = blocks[0].strip()
    if intro:
        st.markdown(intro)
    for block in blocks[1:]:
        first_line, _, rest = block.partition("\n")
        title = first_line.strip()
        with st.expander(f"🎬 {title}", expanded=False):
            st.markdown(rest.strip())


def render_stage_emploi_redaction_section(
    pack_root: Path,
    *,
    display_name: str,
    key_slug: str,
    missing_folder_hint: str | None = None,
) -> None:
    """Onglet Stage & emploi : Script, Architecture (§5.2), Vidéos veille (consolidé)."""
    tab_script, tab_arch, tab_veille = st.tabs(["Script", "Architecture", "Vidéos veille"])
    with tab_script:
        render_script_browser_at_path(
            pack_root,
            display_name=display_name,
            key_slug=key_slug,
            missing_folder_hint=missing_folder_hint,
            page_heading="Script",
        )
    with tab_arch:
        render_stage_emploi_architecture_tab(pack_root=pack_root, key_slug=key_slug)
    with tab_veille:
        render_veille_videos_consolidated_tab(
            pack_root,
            display_name=display_name,
            key_slug=f"{key_slug}_veille",
            missing_folder_hint=missing_folder_hint,
        )


def render_script_parcours_browser(pack_folder_name: str) -> None:
    """Navigateur pour un dossier-parcours direct sous ``Input/Script/<nom>/``."""
    root = get_pack_root(pack_folder_name)
    slug = _safe_key_fragment(pack_folder_name)
    hint = f"Vérifiez que `Input/Script/{pack_folder_name}` existe."
    if pack_folder_name == _STAGE_EMPLOI_PACK:
        render_stage_emploi_redaction_section(
            root,
            display_name=pack_folder_name,
            key_slug=slug,
            missing_folder_hint=hint,
        )
        return
    render_script_browser_at_path(
        root,
        display_name=pack_folder_name,
        key_slug=slug,
        missing_folder_hint=hint,
    )


def render_stage_emploi_tab() -> None:
    render_script_parcours_browser(_STAGE_EMPLOI_PACK)


render_script_pack_browser = render_script_parcours_browser
