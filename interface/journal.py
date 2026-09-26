"""Journalisation des interactions : fichier rotatif + relais vers la barre d'état."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import QObject, Signal

DOSSIER = Path(__file__).resolve().parent.parent / "logs"
FICHIER = DOSSIER / "interface.log"
FORMAT = "%(asctime)s | %(levelname)-7s | %(name)-14s | %(message)s"
TAILLE_MAX = 512 * 1024
CONSERVES = 3
NIVEAU = logging.DEBUG
NIVEAU_ETAT = logging.WARNING
DOMINE = "rps"

journal = logging.getLogger("interface")
_fichier: RotatingFileHandler | None = None


class Alerte(QObject):
    """Reçoit les messages du journal et les transmet à la fenêtre."""

    declenche = Signal(str, int)

    def signaler(self, message: str, niveau: int) -> None:
        self.declenche.emit(message, niveau)


class RedirectionEtat(logging.Handler):
    """Aiguille les avertissements et erreurs du domaine vers la barre d'état."""

    def __init__(self, alerte: Alerte) -> None:
        super().__init__(level=NIVEAU_ETAT)
        self._alerte = alerte

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self._alerte.signaler(record.getMessage(), record.levelno)
        except Exception:  # la journalisation ne doit jamais interrompre l'interface
            self.handleError(record)


def creer_journal(alerte: Alerte | None = None) -> logging.Logger:
    """Configure le journal de l'interface et celui du domaine, et renvoie celui de l'interface."""
    global _fichier

    if _fichier is None:
        DOSSIER.mkdir(exist_ok=True)
        _fichier = RotatingFileHandler(
            FICHIER, maxBytes=TAILLE_MAX, backupCount=CONSERVES, encoding="utf-8"
        )
        _fichier.setFormatter(logging.Formatter(FORMAT))
        _fichier.setLevel(NIVEAU)
        journal.addHandler(_fichier)
        journal.setLevel(NIVEAU)
        journal.propagate = False

    domaine = logging.getLogger(DOMINE)
    domaine.setLevel(NIVEAU)
    if _fichier not in domaine.handlers:
        domaine.addHandler(_fichier)

    for logger in (journal, domaine):
        for handler in list(logger.handlers):
            if isinstance(handler, RedirectionEtat):
                logger.removeHandler(handler)
    if alerte is not None:
        redirection = RedirectionEtat(alerte)
        journal.addHandler(redirection)
        domaine.addHandler(redirection)
    return journal
