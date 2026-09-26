"""Résultats du calcul présentés sous forme de widgets ordonnés."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from affichage import unite_texte, valeur_texte
from rps import Params, PoidsSismiques, Resultats

PLACEHOLDER = "—"
COLONNES = ("Symbole", "Désignation", "Valeur", "Unité")


class _Tableau(QGroupBox):
    """Tableau de résultats : chaque cellule est un widget, rempli par `remplir`."""

    def __init__(self, titre: str) -> None:
        super().__init__(titre)
        self.grille = QGridLayout(self)
        self.grille.setContentsMargins(10, 4, 10, 6)
        self.grille.setHorizontalSpacing(10)
        self.grille.setVerticalSpacing(3)
        self.grille.setColumnStretch(1, 1)

        for colonne, entete in enumerate(COLONNES):
            etiquette = QLabel(entete)
            etiquette.setObjectName("enteteTableau")
            if entete == "Valeur":
                etiquette.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            elif entete == "Symbole":
                etiquette.setAlignment(Qt.AlignHCenter)
            self.grille.addWidget(etiquette, 0, colonne)

        self._valeurs: dict[int, QLabel] = {}
        self._unites: dict[int, QLabel] = {}
        self._prochaine = 1

    def ajouter(self, symbole: str, designation: str, mise_en_avant: bool = False) -> int:
        """Crée la ligne et renvoie son index pour un remplissage ultérieur."""
        ligne = self._prochaine
        self._prochaine += 1

        etiquette_symbole = QLabel(symbole)
        etiquette_symbole.setObjectName("symbole")
        etiquette_symbole.setAlignment(Qt.AlignCenter)

        etiquette_designation = QLabel(designation)
        etiquette_designation.setObjectName("designation")

        valeur = QLabel(PLACEHOLDER)
        valeur.setObjectName("valeurFinale" if mise_en_avant else "valeur")
        valeur.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        valeur.setTextInteractionFlags(Qt.TextSelectableByMouse)

        unite = QLabel("")
        unite.setObjectName("unite")
        unite.setAlignment(Qt.AlignHCenter)

        self.grille.addWidget(etiquette_symbole, ligne, 0)
        self.grille.addWidget(etiquette_designation, ligne, 1)
        self.grille.addWidget(valeur, ligne, 2)
        self.grille.addWidget(unite, ligne, 3)

        self._valeurs[ligne] = valeur
        self._unites[ligne] = unite
        return ligne

    def remplir(self, ligne: int, valeur: str, unite: str = "") -> None:
        self._valeurs[ligne].setText(valeur)
        self._unites[ligne].setText(unite)

    def remplir_param(self, ligne: int, param: Params, decimales: int = 3) -> None:
        self.remplir(
            ligne,
            valeur_texte(param, decimales),
            unite_texte(param),
        )

    def vider(self) -> None:
        for ligne in self._valeurs:
            self.remplir(ligne, PLACEHOLDER)

    def supprimer_lignes(self) -> None:
        for ligne in list(self._valeurs):
            for colonne in range(len(COLONNES)):
                element = self.grille.itemAtPosition(ligne, colonne)
                widget = element.widget() if element is not None else None
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
        self._valeurs.clear()
        self._unites.clear()
        self._prochaine = 1


class PanneauResultats(QScrollArea):
    """Sections ordonnées : Paramètres RPS, Direction X, Direction Y."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)

        contenu = QWidget()
        self._racine = QVBoxLayout(contenu)
        self._racine.setContentsMargins(0, 0, 6, 0)
        self._racine.setSpacing(10)

        self._rps = _Tableau("Paramètres RPS")
        self._direction_x = _Tableau("Direction X")
        self._direction_y = _Tableau("Direction Y")

        for tableau in (self._rps, self._direction_x, self._direction_y):
            self._racine.addWidget(tableau)
        self._racine.addStretch(1)
        self.setWidget(contenu)

    def afficher(self, resultats: Resultats, poids_sismique: PoidsSismiques) -> None:
        """(Re)construit les tableaux puis affiche les valeurs du calcul."""
        for tableau in (self._rps, self._direction_x, self._direction_y):
            tableau.supprimer_lignes()

        self._afficher_parametres(resultats)
        self._afficher_direction(
            self._direction_x, resultats.Tx, resultats.Dx, poids_sismique.Wx, resultats.Fx
        )
        self._afficher_direction(
            self._direction_y, resultats.Ty, resultats.Dy, poids_sismique.Wy, resultats.Fy
        )

    def vider(self) -> None:
        for tableau in (self._rps, self._direction_x, self._direction_y):
            tableau.vider()

    def _afficher_parametres(self, resultats: Resultats) -> None:
        for param in (resultats.upsilon, resultats.I, resultats.S, resultats.nd, resultats.K):
            ligne = self._rps.ajouter(param.symbole or PLACEHOLDER, param.nom)
            self._rps.remplir_param(ligne, param)

    def _afficher_direction(
        self, tableau: _Tableau, periode: Params, amplification: Params,
        poids: Params, force: Params,
    ) -> None:
        for param in (periode, amplification, poids):
            ligne = tableau.ajouter(param.symbole or PLACEHOLDER, param.nom)
            tableau.remplir_param(ligne, param)
        ligne_force = tableau.ajouter(force.symbole or "F", force.nom, mise_en_avant=True)
        tableau.remplir_param(ligne_force, force, decimales=2)
