# Force sismique équivalente — RPS 2011

Application de bureau Python/PySide6 pour le calcul automatisé de la force
sismique équivalente d'une structure en béton armé, selon le **RPS 2011**
(Règlement Parasismique Marocain).

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green?logo=qt)
![Norme](https://img.shields.io/badge/Norme-RPS%202011-orange)
![Licence](https://img.shields.io/badge/Licence-MIT-lightgrey)

---

## Téléchargement

Exécutable Windows autonome : **rien à installer**, ni Python, ni le catalogue
CSV, ni les sources.

[*Releases*](https://github.com/vlax-rsr/Force-sismique-RPS-2011/releases/latest) — `ForceSismiqueRPS2011.exe`

Vérifier le téléchargement avec la somme SHA-256 fournie (`SHA256SUMS.txt`).

---

## Aperçu

![Capture d'écran de l'interface](docs/apercu.png)

L'outil applique la méthode de la force statique équivalente dans les deux
directions du bâtiment, isole chaque coefficient dans un module dédié, et
renseigne pour chaque valeur intermédiaire sa formule, son unité et la table de
la norme dont elle est issue. Les résultats sont également exploitables en ligne
de commande ou directement depuis la bibliothèque.

---

## Fonctionnalités

- **Méthode de la force statique équivalente** — `F = υ.I.D.S.W/K`, dans les deux directions X et Y
- **Un module par coefficient normatif** — υ, I, T, D, S, ND, K, F (tableaux 3.1, 3.2, 3.3, 5.1, 5.2, 5.3 de la RPS 2011)
- **Résultat entièrement traçable** — chaque valeur conserve sa formule, son unité et sa table source ; aucune valeur n'est un scalaire nu
- **Formulaire contrôlé en direct** — le champ fautif passe en rouge, les erreurs sont listées en un clic sur `Calculer`
- **Note de calcul horodatée** — aperçu du texte exact, enregistrable en `.txt` UTF-8
- **Journal des interactions** — fichier rotatif, avertissements de la norme relayés dans la barre d'état
- **Bilan en ligne de commande** — même mise en forme que l'interface, sans aucune dépendance
- **Interface graphique soignée** — thèmes clair et sombre, résultats en widgets

---

## Prérequis

| Dépendance | Version minimale | Rôle |
|------------|------------------|------|
| Python     | 3.12            | Obligatoire |
| PySide6    | 6.6             | Interface graphique — requis pour `main` |
| matplotlib | 3.7             | Rendu LaTeX de la formule — facultatif |

Le cœur du calcul n'a **aucune dépendance** : seule la bibliothèque standard est
nécessaire.

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/vlax-rsr/Force-sismique-RPS-2011.git
cd Force-sismique-RPS-2011

# Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
main
```

Équivalent avec le packaging : `pip install -e ".[gui]"` (extras `latex` et
`dev` disponibles). Le rendu terminal ne demande aucune dépendance :
`python lancer.py demo` imprime la note de calcul complète, horodatée.

---

## Utilisation

1. Renseigner les données du bâtiment :
   - Localisation : zones **Za** et **Zv** (0 à 4)
   - Géométrie : hauteur **H**, longueurs **Lx** et **Ly** (en mètres)
   - Structure : système de contreventement, classe, classe de site **S1** à **S5**
   - Poids sismiques **Wx** et **Wy** (en kN, daN ou kgf)
2. Cliquer sur **Calculer** : les paramètres RPS, les périodes **T**, les
   facteurs **D** et les forces **Fx** / **Fy** s'affichent direction par
   direction
3. Cliquer sur **Note de calcul** pour prévisualiser le texte, puis
   **Enregistrer sous…** pour l'exporter

Le site **S5** n'a pas de valeur forfaitaire : la valeur se saisit manuellement
(étude géotechnique).

---

## Structure du projet

```
Force-sismique-RPS-2011/
├── lancer.py                  # Point d'entrée : main (interface), main demo (terminal)
├── exemple.py                 # Jeu de données d'exemple
├── affichage.py               # Présentation du bilan, en texte
├── rps/                       # Domaine métier : un module par coefficient
├── interface/                 # Interface graphique PySide6
├── spec/                      # Recette PyInstaller de l'exécutable .exe
├── .github/workflows/         # Tests + publication de l'exécutable (Release)
├── data/                      # Catalogue des zones sismiques par commune
├── docs/                      # Aperçu de l'interface, construction de l'exécutable
├── tests/                     # 34 tests
├── requirements.txt
├── pyproject.toml
└── LICENSE
```

L'exécutable Windows est construit par PyInstaller à partir de `spec/` et
publié dans les *Releases* à chaque tag `v*` : voir
[docs/construction.md](docs/construction.md).

---

## Formule

```
υ = coefficient de vitesse          (Tableau 5.1)
I = coefficient d'importance        (Tableau 3.1)
D = facteur d'amplification         (Tableau 5.3)
S = coefficient de site             (Tableau 5.2)
W = poids sismique du bâtiment      (donnée d'entrée)
K = facteur de comportement         (Tableau 3.3)

F = υ.I.D.S.W / K
```

---

## Licence

Distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Auteur
*Riana STELLIA*

Développé dans le cadre d'un portfolio de calcul de structure en béton armé.  
Contributions et retours bienvenus via les *Issues* GitHub.

*Les résultats doivent être vérifiés par un bureau d'études, et la version de la
norme en vigueur sur le projet contrôlée avant tout dimensionnement.*
