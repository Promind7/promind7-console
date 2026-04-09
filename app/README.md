# Application ProMind7 (code)

Point d’entrée Streamlit : `promind7_console.py`.

Depuis la **racine du dépôt** `V2/` :

```powershell
.\.venv\Scripts\streamlit run app\promind7_console.py
# équivalent : streamlit run promind7_console.py  (shim à la racine V2/)
```

Les scripts outils sont sous `tools/` (ex. `app/tools/format_module00_scripts.py`). Les docs projet sous `docs/`, les livrables agent sous `reports/`.

La base SQLite `db/` peut rester à la racine `V2/db` le temps de fermer les verrous ; l’app ajoute la racine au `sys.path` pour importer `db`.
