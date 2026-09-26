# Construction de l'exécutable Windows

L'application est distribuée sous forme d'un **fichier unique**
`ForceSismiqueRPS2011.exe` : il embarque Python, PySide6 et le code, et ne
dépend ni du script, ni du catalogue `data/`, ni d'une installation Python.

## Construction locale

```bash
# Dépendances de construction
pip install -e ".[build]"
pip install PySide6

# Construction (depuis la racine du dépôt)
pyinstaller spec/force_sismique.spec --noconfirm

# Résultat
dist/ForceSismiqueRPS2011.exe
```

Le fichier produit se trouve dans `dist/` (le dossier de travail `build/` est
ignoré par Git). Exécutable sur toute machine Windows x64, sans installation.

Pour vérifier l'artefact avant de le diffuser :

```powershell
Get-FileHash dist\ForceSismiqueRPS2011.exe -Algorithm SHA256
```

## Construction automatique (GitHub Actions)

`.github/workflows/release.yml` reproduit exactement ces étapes :

| Déclencheur | Effet |
|-------------|-------|
| Push sur `master` / `main`, pull request, `workflow_dispatch` | Analyse statique, tests, construction, **artifact** de 7 jours |
| Push d'un tag `v*` (ex. `v1.0.0`) | Idem + **Release** GitHub avec l'exécutable et sa somme SHA-256 |

Publier une version :

```bash
git tag v1.0.0
git push origin v1.0.0
```

La Release est créée par `softprops/action-gh-release` avec les notes de version
générées automatiquement par GitHub. Le job de tests doit être vert avant la
publication (`needs: verifier`).

## Choix techniques

- **Un seul fichier** : `--onefile` (défaut de la recette). L'exécutable se
  décompresse dans `%TEMP%` au lancement, d'où un démarrage légèrement plus
  lent qu'une installation par dossier.
- **Point d'entrée `lancer.py`** : sans argument, la commande ouvre l'interface.
  Aucun script de lancement séparé n'est nécessaire.
- **`console=False`** : pas de fenêtre console au double-clic. `lancer.py` renvoie
  alors `sys.stdout` / `sys.stderr` vers le périphérique nul, car PyInstaller les
  met à `None` dans ce mode.
- **Ni `data/` ni `matplotlib`** : aucune ligne de code ne lit le catalogue CSV,
  et le rendu LaTeX (`interface/formule.py`) n'est appelé par aucun widget de
  l'interface — le header affiche la formule en texte. Ces deux éléments
  ajouteraient plusieurs dizaines de mégaoctets pour rien.
- **Modules Qt inutilisés exclus** (`QtWebEngine`, `QtQuick`, `Qt3D`,
  `QtMultimedia`…) : liste explicite dans `spec/force_sismique.spec`.
- **Métadonnées Windows** : `spec/version.txt` fournit le nom du produit, la
  société et la version dans les propriétés du fichier.

## Mise à jour de la version

Le numéro de version est présent à trois endroits, à faire évoluer ensemble :

1. `pyproject.toml` → `version`
2. `spec/force_sismique.spec` → `VERSION`
3. `spec/version.txt` → `filevers`, `FileVersion`, `ProductVersion`
