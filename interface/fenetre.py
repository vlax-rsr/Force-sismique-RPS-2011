"""Fenêtre principale : en-tête, saisie, résultats, barre d'actions et journal."""

import logging
import platform
from datetime import datetime
from pathlib import Path

from PySide6 import __version__ as PYSIDE_VERSION
from PySide6.QtCore import Qt, qVersion
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from affichage import rendre_bilan
from rps import calcul_force_sismique, creer_localisation

from .journal import Alerte, creer_journal
from .note import FenetreNote
from .resultats import PanneauResultats
from .saisie import FormulaireSaisie

TITRE = "Force sismique"
SOUS_TITRE = "RPS 2011"
QT_VERSION = qVersion()
MESSAGE_ETAT = "Renseignez les données puis cliquez sur Calculer."
MESSAGE_MODIFIE = "Données modifiées — cliquez sur Calculer pour actualiser les résultats."
MESSAGE_SUCCES = "Calcul réalisé avec succès"
MESSAGE_ERREUR = "Les valeurs saisies sont erronées : "
FICHIER_ETAT = "Fichiers texte (*.txt)"
TONS = {"info": "etat", "succes": "etatSucces", "alerte": "etatAlerte", "erreur": "etatErreur"}


class FenetrePrincipale(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{TITRE} — {SOUS_TITRE}")
        # Dimensions adaptées aux écrans d'ordinateurs portables (ex: 1366x768 ou 1080p avec scaling)
        self.resize(1020, 620)
        self.setMinimumSize(780, 480)
        self._note: str | None = None
        self.alerte = Alerte()
        self.journal = creer_journal(self.alerte)
        self._construire()
        self.alerte.declenche.connect(self._evenement)
        self.formulaire.changement.connect(self._sur_saisie)
        self.journal.info(
            "Session ouverte — fenêtre %dx%d, Python %s, PySide6 %s, Qt %s",
            self.width(), self.height(), platform.python_version(),
            PYSIDE_VERSION, QT_VERSION,
        )
        self.reinitialiser()


    def _construire(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        layout.addWidget(self._entete())

        splitter = QSplitter(Qt.Horizontal)
        self.formulaire = FormulaireSaisie()

        # QScrollArea pour que la zone de saisie reste intégralement accessible sur tout petit écran
        self.zone_saisie = QScrollArea()
        self.zone_saisie.setWidgetResizable(True)
        self.zone_saisie.setFrameShape(QFrame.NoFrame)
        self.zone_saisie.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.zone_saisie.setWidget(self.formulaire)
        self.zone_saisie.setMinimumWidth(320)
        self.zone_saisie.setMaximumWidth(420)

        self.resultats = PanneauResultats()
        splitter.addWidget(self.zone_saisie)
        splitter.addWidget(self.resultats)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([350, 670])
        layout.addWidget(splitter, 1)

        layout.addWidget(self._separateur())
        layout.addLayout(self._barre_actions())

    def _entete(self) -> QWidget:
        conteneur = QWidget()
        layout = QVBoxLayout(conteneur)
        layout.setContentsMargins(0, 4, 0, 2)
        layout.setSpacing(2)

        titre = QLabel(TITRE)
        titre.setAlignment(Qt.AlignCenter)
        font_titre = QFont("Georgia, 'Times New Roman', serif")
        font_titre.setPointSize(70)
        font_titre.setWeight(QFont.Weight.Bold)
        font_titre.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        titre.setFont(font_titre)
        titre.setStyleSheet("color: #1a1a1a; letter-spacing: 1px;")

        sous_titre = QLabel(SOUS_TITRE)
        sous_titre.setAlignment(Qt.AlignCenter)
        font_sous = QFont("Georgia, 'Times New Roman', serif")
        font_sous.setPointSize(20)
        font_sous.setItalic(True)
        sous_titre.setFont(font_sous)
        sous_titre.setStyleSheet("color: #6b7178; letter-spacing: 2px;")

        layout.addWidget(titre)
        layout.addWidget(sous_titre)
        return conteneur

    @staticmethod
    def _separateur() -> QFrame:
        trait = QFrame()
        trait.setObjectName("separateur")
        trait.setFrameShape(QFrame.HLine)
        trait.setFrameShadow(QFrame.Sunken)
        return trait

    def _barre_actions(self) -> QHBoxLayout:
        """État à gauche, puis Calculer, Exporter, Réinitialiser."""
        barre = QHBoxLayout()
        barre.setContentsMargins(0, 0, 0, 0)
        barre.setSpacing(8)

        self.etat = QLabel(MESSAGE_ETAT)
        self.etat.setObjectName("etat")
        barre.addWidget(self.etat, 1)

        self.bouton_calculer = QPushButton("Calculer")
        self.bouton_calculer.setObjectName("calculer")
        self.bouton_calculer.setDefault(True)
        self.bouton_calculer.clicked.connect(self.calculer)
        barre.addWidget(self.bouton_calculer)

        self.bouton_exporter = QPushButton("Note de calcul")
        self.bouton_exporter.setObjectName("exporter")
        self.bouton_exporter.setToolTip("Afficher la note de calcul (enregistrable en .txt)")
        self.bouton_exporter.clicked.connect(self.afficher_note)
        barre.addWidget(self.bouton_exporter)

        self.bouton_reinitialiser = QPushButton("Réinitialiser")
        self.bouton_reinitialiser.setObjectName("reinitialiser")
        self.bouton_reinitialiser.setToolTip("Vider le formulaire et effacer les résultats")
        self.bouton_reinitialiser.clicked.connect(self.reinitialiser)
        barre.addWidget(self.bouton_reinitialiser)
        return barre

    def _calculer(self):
        """Enchaîne lecture du formulaire et procédure ; lève ValueError si les données sont refusées."""
        za, zv, geometrie, batiment, poids, _ = self.formulaire.lire()
        localisation = creer_localisation(za.value, zv.value)
        resultats = calcul_force_sismique(
            localisation=localisation,
            geometrie=geometrie,
            batiment=batiment,
            loads=poids,
        )
        return localisation, geometrie, batiment, poids, resultats

    def _sur_saisie(self) -> None:
        """Le formulaire a changé : les champs fautifs sont déjà signalés en rouge, l'état reste neutre."""
        self._dire(MESSAGE_MODIFIE if self._note is not None else MESSAGE_ETAT)

    def _refus(self, message: str) -> None:
        """Données refusées : l'état passe en rouge et les actions dépendantes sont bloquées."""
        self.journal.error("Données refusées — %s", message)
        self._note = None
        self.resultats.vider()
        self.bouton_exporter.setEnabled(False)
        self._dire(message, "erreur")

    def calculer(self) -> None:
        self.formulaire.reveler_erreurs()
        fautes = self.formulaire.etiquettes_invalides()
        if fautes:
            self._refus(MESSAGE_ERREUR + ", ".join(fautes))
            return

        try:
            localisation, geometrie, batiment, poids, resultats = self._calculer()
        except ValueError as erreur:
            self._refus(str(erreur))
            return

        self._note = self._horodate(rendre_bilan(resultats, localisation, geometrie, batiment, poids))
        self.resultats.afficher(resultats, poids)
        self.bouton_exporter.setEnabled(True)
        self.journal.info(
            "Calcul réussi — Fx = %.2f %s, Fy = %.2f %s",
            resultats.Fx.valeur, resultats.Fx.unite.value,
            resultats.Fy.valeur, resultats.Fy.unite.value,
        )
        self._dire(MESSAGE_SUCCES, "succes")

    @staticmethod
    def _horodate(note: str) -> str:
        """Inscrit la date et l'heure du calcul sous le bandeau de la note."""
        lignes = note.split("\n")
        for index, ligne in enumerate(lignes[1:], start=1):
            if ligne and set(ligne) <= {"="}:
                horodatage = f"Calcul réalisé le {datetime.now():%d/%m/%Y à %H:%M:%S}"
                return "\n".join([*lignes[: index + 1], horodatage, "", *lignes[index + 1:]])
        return note

    def afficher_note(self) -> None:
        """Ouvre la note de calcul dans une fenêtre dédiée."""
        if self._note is None:
            self.journal.warning("Note de calcul demandée sans calcul disponible.")
            self._dire("Aucun calcul à afficher : cliquez sur Calculer.", "alerte")
            return

        self.journal.info("Note de calcul affichée (%d caractères)", len(self._note))
        FenetreNote(self._note, sur_enregistrement=self.exporter, parent=self).exec()

    def exporter(self) -> None:
        if self._note is None:
            self.journal.warning("Export demandé sans calcul disponible.")
            self._dire("Aucun calcul à exporter : cliquez sur Calculer.", "alerte")
            return

        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
        chemin, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter la note de calcul",
            f"note_de_calcul_{horodatage}.txt",
            FICHIER_ETAT,
        )
        if not chemin:
            self.journal.info("Export annulé par l'utilisateur.")
            self._dire("Export annulé.", "alerte")
            return

        if not chemin.lower().endswith(".txt"):
            chemin += ".txt"
        try:
            Path(chemin).write_text(self._note, encoding="utf-8")
        except OSError as erreur:
            self.journal.error("Export impossible (%s) — %s", chemin, erreur)
            self._dire(f"Export impossible : {erreur}", "erreur")
            QMessageBox.critical(self, "Export impossible", str(erreur))
            return
        self.journal.info("Note de calcul exportée — %s (%d caractères)", chemin, len(self._note))
        self._dire(f"Note de calcul exportée : {Path(chemin).name}", "succes")

    def reinitialiser(self) -> None:
        self.journal.info("Réinitialisation — formulaire vidé, résultats effacés")
        self.resultats.vider()
        self._note = None
        self.bouton_exporter.setEnabled(False)
        self.formulaire.reinitialiser()
        self._dire(MESSAGE_ETAT)

    def _dire(self, message: str, ton: str = "info") -> None:
        """Affiche un message dans la barre d'état : rouge, orange, vert ou gris selon le ton."""
        self.etat.setText(message)
        self.etat.setToolTip(message)
        self.etat.setObjectName(TONS[ton])
        self.etat.style().unpolish(self.etat)
        self.etat.style().polish(self.etat)

    def _evenement(self, message: str, niveau: int) -> None:
        """Un avertissement ou une erreur du domaine est relayé dans la barre d'état."""
        self._dire(message, "erreur" if niveau >= logging.ERROR else "alerte")

    def note_de_calcul(self) -> str | None:
        """Texte de la note de calcul du dernier calcul réussi, s'il y en a un."""
        return self._note
