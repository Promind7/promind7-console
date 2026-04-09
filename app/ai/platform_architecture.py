"""
Architecture cible des agents ProMind7 (formation uniquement).

Grands blocs prévus — implémentation progressive :

1. **orchestrator** (futur)
   Route les intentions utilisateur vers le bon sous-agent ; mémoire préférences.

2. **writer** (actif — voir writer_agent.py)
   Scripts pédagogiques, darija, respect du style_guide + overrides + sources.

3. **data_platform** (futur)
   Apprenants, inscriptions Tutor, KPI plateforme ; outils SQL/services existants.

4. **planning** (futur)
   Sessions live, calendrier, tâches équipe (Google Calendar déjà intégré).

5. **finance** (futur — hors scope formation stricte si besoin)
   CA, abonnements : uniquement quand source de vérité définie.

6. **research** (partiel — research_tools.py)
   Recherche web / vidéos pour alimenter la rédaction, sans inventer de faits.

Ne pas importer ce module depuis Streamlit pour l’instant : documentation vivante.
"""
