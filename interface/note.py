"""Fenêtre d'affichage de la note de calcul."""

from collections.abc import Callable

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FenetreNote(QDialog):
    """Affiche la note de calcul, telle qu'elle peut être enregistrée sur disque."""

    def __init__(
        self,
        note: str,
        sur_enregistrement: Callable[[], None] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Note de calcul")
        self.resize(920, 700)
        self._sur_enregistrement = sur_enregistrement

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 8)
        layout.setSpacing(6)

        titre = QLabel("Note de calcul")
        titre.setObjectName("titreNote")
        layout.addWidget(titre)

        self.texte = QPlainTextEdit()
        self.texte.setReadOnly(True)
        self.texte.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.texte.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        self.texte.setPlainText(note)
        layout.addWidget(self.texte, 1)

        barre = QHBoxLayout()
        barre.setSpacing(8)

        self.bouton_enregistrer = QPushButton("Enregistrer sous…")
        self.bouton_enregistrer.setObjectName("exporter")
        self.bouton_enregistrer.setToolTip("Enregistrer la note de calcul dans un fichier texte (.txt)")
        self.bouton_enregistrer.setEnabled(sur_enregistrement is not None)
        self.bouton_enregistrer.clicked.connect(self._enregistrer)
        barre.addWidget(self.bouton_enregistrer)

        barre.addStretch(1)

        self.bouton_fermer = QPushButton("Fermer")
        self.bouton_fermer.setDefault(True)
        self.bouton_fermer.clicked.connect(self.accept)
        barre.addWidget(self.bouton_fermer)

        layout.addLayout(barre)

    def _enregistrer(self) -> None:
        if self._sur_enregistrement is not None:
            self._sur_enregistrement()
