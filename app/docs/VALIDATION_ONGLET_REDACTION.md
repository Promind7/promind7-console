# Validation de l’onglet **Rédaction**

## Prérequis

1. Environnement activé : `.\.venv\Scripts\activate` (PowerShell).
2. Dépendances : `pip install -r requirements.txt` (dont `duckduckgo-search`, `openai`).
3. **Clé API (au moins une)** :
   - **Recommandé — Claude** : compte sur [console Anthropic](https://console.anthropic.com/) → créer une clé → variable `ANTHROPIC_API_KEY` ou `secrets.toml`.
   - **Optionnel — OpenAI** : `OPENAI_API_KEY` si tu n’utilises pas Claude.

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
# OPENAI_API_KEY = "sk-..."   # optionnel
```

Si les **deux** clés sont définies, l’app utilise **Claude par défaut**. Pour forcer OpenAI : variable `PROMIND7_WRITER_PROVIDER=openai`.

4. Lancer l’app :

```powershell
cd D:\Promind7\IA\V2
.\.venv\Scripts\streamlit run promind7_console.py
```

## Checklist rapide

| # | Test | Résultat attendu |
|---|------|-------------------|
| 1 | Ouvrir l’onglet **Rédaction** | Pas d’erreur ; avertissement jaune **seulement** si pas de clé API. |
| 2 | Sans clé : envoyer un message | Réponse d’erreur explicite (Anthropic ou OpenAI). |
| 3 | Avec clé : message simple (« Écris un plan de script 3 min sur l’orientation ») | Réponse en markdown + section **Sources** en bas. |
| 4 | Cocher recherche web + vidéos | Zone *Sources brutes* remplie ; pas d’erreur bloquante si DDG est capricieux. |
| 5 | Chemin local vers un `.docx` de `Input\Script\...` | Le style / le ton s’inspirent du fichier (aperçu à gauche des options). |
| 6 | Téléverser un petit `.txt` | Contenu pris en compte dans la génération. |
| 7 | *Enregistrer une règle* dans **writer_style_overrides.md** | Fichier `content/writer_style_overrides.md` enrichi ; prochain message tient compte de la règle. |
| 8 | **Sauvegarder** dans `content/redaction_drafts/` | Fichier `.md` créé au chemin affiché. |
| 9 | **Vider la conversation** | Historique et aperçu réinitialisés. |

## Optionnel

- **Claude** : `PROMIND7_CLAUDE_MODEL` (défaut : `claude-3-5-sonnet-20241022`).
- **OpenAI** : `PROMIND7_WRITER_MODEL` (défaut : `gpt-4o-mini`).
- Forcer un fournisseur : `PROMIND7_WRITER_PROVIDER=anthropic` ou `openai`.

## Si ça bloque

- **401 / invalid API key** : clé invalide ou expirée.
- **Recherche vide** : réseau ou limitation DuckDuckGo ; désactiver web/vidéos et réessayer.
- **`.docx` illisible** : vérifier que le fichier n’est pas corrompu ; tester avec un `.txt`.
