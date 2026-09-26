"""Génère l'aperçu de l'interface pour le README (docs/apercu.png)."""

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

from PySide6.QtWidgets import QApplication  # noqa: E402

from interface.app import creer_application  # noqa: E402
from interface.fenetre import FenetrePrincipale  # noqa: E402

SORTIE = RACINE / "docs" / "apercu.png"


def main() -> int:
    application = QApplication.instance() or creer_application([])
    fenetre = FenetrePrincipale()
    fenetre.resize(1180, 720)
    fenetre.show()
    application.processEvents()

    formulaire = fenetre.formulaire
    formulaire.za.setCurrentIndex(3)
    formulaire.zv.setCurrentIndex(3)
    formulaire.hauteur.setValue(10.0)
    formulaire.longueur_x.setValue(20.0)
    formulaire.longueur_y.setValue(15.0)
    formulaire.ossature.setCurrentIndex(2)
    formulaire.classe.setCurrentIndex(1)
    formulaire.classe_site.setCurrentIndex(2)
    formulaire.poids_x.setValue(3111.61)
    formulaire.poids_y.setValue(3111.61)
    application.processEvents()

    fenetre.calculer()
    application.processEvents()

    SORTIE.parent.mkdir(exist_ok=True)
    fenetre.grab().save(str(SORTIE))
    fenetre.close()
    print(f"Aperçu écrit dans {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
