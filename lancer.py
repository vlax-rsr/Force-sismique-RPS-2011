"""Point d'entrée du projet : `main` (interface graphique) ou `main demo` (terminal).

- `main`       ouvre l'interface PySide6 ;
- `main demo`  affiche un exemple de calcul complet dans le terminal.

L'interface et la ligne de commande importent leurs modules à l'exécution : la
commande `demo` fonctionne donc sans PySide6 installé, et `main --help` reste
disponible même si l'interface n'a pas pu être construite.
"""

from __future__ import annotations

import argparse
import os
import sys

DESCRIPTION = "Calcul de la force sismique équivalente selon la RPS 2011."


def _fenetre() -> None:
    """PyInstaller en mode fenêtre (`console=False`) met sys.stdout / sys.stderr
    à None : `print()` lèverait une AttributeError. On les renvoie vers le périphérique
    nul, ce qui ne change rien pour l'utilisateur et protège le domaine et le journal."""
    if getattr(sys, "frozen", False):
        for nom in ("stdout", "stderr"):
            if getattr(sys, nom) is None:
                setattr(sys, nom, open(os.devnull, "w", encoding="utf-8"))


def _utf8() -> None:
    """Force l'UTF-8 sur la console : cp437 / cp1252 ne savent pas écrire υ, ≤, ×."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _demo() -> int:
    """Rendu terminal de la note de calcul produite par le jeu d'exemple."""
    from affichage import afficher_note
    from exemple import executer, exemple

    _utf8()
    entree = exemple()
    afficher_note(executer(*entree), *entree)
    return 0


def _gui() -> int:
    try:
        from interface.app import main as ouvrir_interface
    except ImportError:
        print(
            "PySide6 est requis pour l'interface : pip install \"force-sismique[gui]\"",
            file=sys.stderr,
        )
        return 1

    return ouvrir_interface([sys.argv[0] if sys.argv else "main"])


def _analyser(argv: list[str]) -> argparse.Namespace:
    analyseur = argparse.ArgumentParser(prog="main", description=DESCRIPTION)
    sous_commandes = analyseur.add_subparsers(dest="commande", metavar="[gui|demo]")
    sous_commandes.add_parser("gui", help="interface graphique PySide6 (par défaut)")
    sous_commandes.add_parser("demo", help="exemple de calcul complet, en ligne de commande")
    return analyseur.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _fenetre()
    arguments = _analyser(sys.argv[1:] if argv is None else argv)
    if arguments.commande == "demo":
        return _demo()
    return _gui()


if __name__ == "__main__":
    raise SystemExit(main())
