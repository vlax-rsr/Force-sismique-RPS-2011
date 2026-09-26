"""Formulaire de saisie des données d'entrée du calcul."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from rps import (
    Batiment,
    ClasseConstruction,
    ClasseSite,
    Geometrie,
    PoidsSismiques,
    SystemeContreventement,
    Unite,
    ZoneAcceleration,
    ZoneVitesse,
    coefficient_site,
    creer_geometrie,
    saisir_charge,
)
from rps.charge import UNITE_POIDS

from .journal import journal

LARGEUR_SPIN = 115  # Largeur fixe réduite pour tous les spinbox
LARGEUR_COMBO_COURT = 120  # Largeur fixe réduite pour Za, Zv, Unité
LARGEUR_COMBO_STRUCTURE = 180  # Largeur fixe réduite pour Structure

# Nom court de chaque champ contrôlé, tel qu'il apparaît dans la barre d'état.
NOMS_CHAMPS = {
    "hauteur": "H",
    "longueur_x": "Lx",
    "longueur_y": "Ly",
    "coef_site": "S",
    "poids_x": "Wx",
    "poids_y": "Wy",
}


class FormulaireSaisie(QWidget):
    """Regroupe tous les champs d'entrée et sait en tirer les objets du domaine."""

    changement = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._noms: dict[QWidget, str] = {}
        self._champs: list[QWidget] = []
        self._numeriques: list[QWidget] = []
        self._silencieux = False
        self.revele = False
        self._construire()

    def _construire(self) -> None:
        self.za = QComboBox()
        for zone in ZoneAcceleration:
            self.za.addItem(f"{zone.value}", zone)
        self.za.setFixedWidth(LARGEUR_COMBO_COURT)

        self.zv = QComboBox()
        for zone in ZoneVitesse:
            self.zv.addItem(f"{zone.value}", zone)
        self.zv.setFixedWidth(LARGEUR_COMBO_COURT)

        self.hauteur = self._longueur(0.1, 500.0)
        self.longueur_x = self._longueur(0.1, 500.0)
        self.longueur_y = self._longueur(0.1, 500.0)

        self.ossature = QComboBox()
        for systeme in SystemeContreventement:
            self.ossature.addItem(systeme.value, systeme)
        self.ossature.setFixedWidth(LARGEUR_COMBO_STRUCTURE)
        self.ossature.view().setMinimumWidth(280)

        self.classe = QComboBox()
        for classe in ClasseConstruction:
            self.classe.addItem(classe.libelle, classe)
        self.classe.setFixedWidth(LARGEUR_COMBO_STRUCTURE)

        self.classe_site = QComboBox()
        for site in ClasseSite:
            self.classe_site.addItem(site.value, site)
        self.classe_site.setFixedWidth(LARGEUR_COMBO_STRUCTURE)

        self.coef_site = self._longueur(0.1, 10.0)
        self.coef_site.setEnabled(False)
        self.classe_site.currentIndexChanged.connect(self._basculer_coef_site)

        self.poids_x = self._longueur(0.01, 1e9)
        self.poids_y = self._longueur(0.01, 1e9)
        self.unite = QComboBox()
        for u in UNITE_POIDS:
            self.unite.addItem(u.value, u)
        self.unite.setFixedWidth(LARGEUR_SPIN)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 4, 0)
        layout.setSpacing(5)
        layout.addWidget(self._groupe_localisation())
        layout.addWidget(self._groupe_geometrie())
        layout.addWidget(self._groupe_structure())
        layout.addWidget(self._groupe_charges())
        layout.addStretch(1)
        self.reinitialiser()

    @staticmethod
    def _longueur(minimum: float, maximum: float) -> QDoubleSpinBox:
        champ = QDoubleSpinBox()
        champ.setRange(0.0, maximum)
        champ.setDecimals(2)
        champ.setAlignment(Qt.AlignRight)
        champ.setGroupSeparatorShown(True)
        champ.setFixedWidth(LARGEUR_SPIN)
        champ.setSpecialValueText("0.00")  # Affiché quand valeur == minimum (0)
        champ.setValue(0.0)
        return champ

    @staticmethod
    def _valeur_texte(champ: QWidget) -> str:
        if isinstance(champ, QComboBox):
            return champ.currentText()
        return f"{champ.value():g}"

    def _surveiller(self, champ: QWidget) -> None:
        """Journalise chaque modification et prévient la fenêtre pour un contrôle immédiat."""
        signal = (
            champ.currentIndexChanged if isinstance(champ, QComboBox) else champ.valueChanged
        )
        signal.connect(lambda _emission, champ=champ: self._signaler(champ))

    def _signaler(self, champ: QWidget) -> None:
        if not self._silencieux:
            journal.info("Saisie — %s : %s", self._noms.get(champ, "?"), self._valeur_texte(champ))
        self._marquer(champ)
        self.changement.emit()

    def champs_invalides(self) -> list[QWidget]:
        """Champs dont la valeur est refusée, dans l'ordre du formulaire."""
        return [champ for champ in self._champs if not self._valide(champ)]

    def _valide(self, champ: QWidget) -> bool:
        """Une liste déroulante est toujours valide ; un champ numérique doit être renseigné."""
        if champ not in self._numeriques:
            return True
        if champ is self.coef_site:
            return self.classe_site.currentData() != ClasseSite.S5 or champ.value() > 0
        return champ.value() > 0

    def etiquettes_invalides(self) -> list[str]:
        """Noms courts des champs fautifs, pour le message d'état."""
        invalides = set(self.champs_invalides())
        return [court for nom, court in NOMS_CHAMPS.items() if getattr(self, nom) in invalides]

    def reveler_erreurs(self) -> None:
        """Après une tentative de calcul, tous les champs fautifs restent signalés en rouge."""
        self.revele = True
        self._marquer()

    def _marquer(self, en_cours: QWidget | None = None) -> None:
        """Souligne en rouge le champ en cours d'édition, ou tous les champs fautifs après un calcul."""
        invalides = set(self.champs_invalides())
        for champ in self._champs:
            actif = champ in invalides and (champ is en_cours or self.revele)
            if bool(champ.property("invalide")) == actif:
                continue
            champ.setProperty("invalide", actif)
            champ.style().unpolish(champ)
            champ.style().polish(champ)

    @staticmethod
    def _preparer(champs: dict[str, QWidget]) -> None:
        """Assure que les combobox ont des politiques de dimension adaptées."""
        for champ in champs.values():
            if isinstance(champ, QComboBox):
                champ.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

    def _groupe(self, titre: str, champs: dict[str, QWidget]) -> QGroupBox:
        """Libellés à gauche (étirables), champs de largeur fixe alignés à droite."""
        groupe = QGroupBox(titre)
        grille = QGridLayout(groupe)
        grille.setContentsMargins(10, 4, 10, 6)
        grille.setHorizontalSpacing(10)
        grille.setVerticalSpacing(4)
        grille.setColumnStretch(0, 1)
        grille.setColumnStretch(1, 0)
        self._preparer(champs)

        for ligne, (libelle, champ) in enumerate(champs.items()):
            etiquette = QLabel(libelle)
            etiquette.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            grille.addWidget(etiquette, ligne, 0)
            grille.addWidget(champ, ligne, 1, Qt.AlignRight | Qt.AlignVCenter)
            self._noms[champ] = libelle
            self._champs.append(champ)
            if isinstance(champ, QDoubleSpinBox):
                self._numeriques.append(champ)
            champ.setProperty("invalide", False)
            self._surveiller(champ)
        return groupe

    def _groupe_localisation(self) -> QGroupBox:
        return self._groupe("Localisation", {
            "Zone d'accélération (Za)": self.za,
            "Zone de vitesse (Zv)": self.zv,
        })

    def _groupe_geometrie(self) -> QGroupBox:
        return self._groupe("Géométrie", {
            "Hauteur H (m)": self.hauteur,
            "Longueur Lx (m)": self.longueur_x,
            "Longueur Ly (m)": self.longueur_y,
        })

    def _groupe_structure(self) -> QGroupBox:
        return self._groupe("Structure", {
            "Ossature": self.ossature,
            "Classe de construction": self.classe,
            "Classe de site": self.classe_site,
            "S": self.coef_site,
        })

    def _groupe_charges(self) -> QGroupBox:
        return self._groupe("Poids sismiques", {
            "Wx": self.poids_x,
            "Wy": self.poids_y,
            "Unité": self.unite,
        })

    def _basculer_coef_site(self) -> None:
        """S'affiche la valeur forfaitaire du site ; le champ n'est saisissable que pour S5."""
        site = self.classe_site.currentData()
        if site == ClasseSite.S5:
            self.coef_site.setEnabled(True)
            self.coef_site.setValue(0.0)
            journal.debug("Site S5 — le coefficient S reste à saisir.")
            return

        valeur = coefficient_site(site).valeur
        self.coef_site.setValue(valeur)
        self.coef_site.setEnabled(False)
        journal.debug("Site %s — coefficient S forfaitaire = %s", site.value, valeur)

    def reinitialiser(self) -> None:
        """Vide le formulaire : 0 (ou l'index 0) signifie « non renseigné »."""
        self.revele = False
        self._silencieux = True
        try:
            # Combobox : index 0
            self.za.setCurrentIndex(0)
            self.zv.setCurrentIndex(0)
            self.ossature.setCurrentIndex(0)
            self.classe.setCurrentIndex(0)
            self.classe_site.setCurrentIndex(0)
            self.unite.setCurrentIndex(0)
            # Spinboxes : 0.0 → affiche le placeholder "0.00"
            self.hauteur.setValue(0.0)
            self.longueur_x.setValue(0.0)
            self.longueur_y.setValue(0.0)
            self.coef_site.setValue(0.0)
            self.poids_x.setValue(0.0)
            self.poids_y.setValue(0.0)
            self._basculer_coef_site()
        finally:
            self._silencieux = False
        self._marquer()
        journal.info("Formulaire réinitialisé — tous les champs sont vides")

    def lire(self) -> tuple[ZoneAcceleration, ZoneVitesse, Geometrie, Batiment, PoidsSismiques, Unite]:
        classe_site = self.classe_site.currentData()
        manuel = None
        if classe_site == ClasseSite.S5 and self.coef_site.value() > 0:
            manuel = self.coef_site.value()
        return (
            self.za.currentData(),
            self.zv.currentData(),
            creer_geometrie(
                hauteur=self.hauteur.value(),
                longueur_x=self.longueur_x.value(),
                longueur_y=self.longueur_y.value(),
            ),
            Batiment(
                type_ossature=self.ossature.currentData(),
                classe=self.classe.currentData(),
                classe_site=classe_site,
                coef_site_manuel=manuel,
            ),
            PoidsSismiques(
                Wx=saisir_charge("Poids sismique X", symbole="Wx",
                                valeur=self.poids_x.value(), unite=self.unite.currentData()),
                Wy=saisir_charge("Poids sismique Y", symbole="Wy",
                                valeur=self.poids_y.value(), unite=self.unite.currentData()),
            ),
            self.unite.currentData(),
        )
