"""Point d'entrée de l'interface graphique : python -m interface"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from .fenetre import FenetrePrincipale

STYLE_SOMBRE = """
QWidget {
    color: #e6edf3;
    font-size: 12px;
}
QGroupBox {
    font-weight: 600;
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 6px;
    color: #f0f6fc;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #f0f6fc;
}
QPushButton {
    min-width: 90px;
    padding: 5px 12px;
    border-radius: 5px;
    border: 1px solid #30363d;
    background: #21262d;
    color: #c9d1d9;
    font-weight: 500;
}
QPushButton:hover {
    background: #30363d;
    color: #f0f6fc;
}
QPushButton:pressed {
    background: #161b22;
}
QPushButton#calculer {
    background: #1f6feb;
    color: #ffffff;
    border: 1px solid #388bfd;
    font-weight: 600;
}
QPushButton#calculer:hover {
    background: #388bfd;
}
QPushButton#calculer:pressed {
    background: #1656c0;
}
QPushButton#exporter {
    background: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
}
QPushButton#exporter:hover {
    background: #30363d;
    color: #f0f6fc;
}
QPushButton#reinitialiser {
    background: #cf3b3b;
    color: #ffffff;
    border: 1px solid #b32e2e;
    font-weight: 600;
}
QPushButton#reinitialiser:hover {
    background: #e04a4a;
}
QPushButton#reinitialiser:pressed {
    background: #b32e2e;
}
QPushButton:disabled {
    background: #161b22;
    color: #484f58;
    border-color: #21262d;
}
QComboBox, QDoubleSpinBox {
    padding: 4px 6px;
    border: 1px solid #30363d;
    border-radius: 4px;
    background: #21262d;
    color: #f0f6fc;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
}
QComboBox:hover, QDoubleSpinBox:hover {
    border-color: #58a6ff;
}
QComboBox:focus, QDoubleSpinBox:focus {
    border-color: #388bfd;
}
QComboBox:disabled, QDoubleSpinBox:disabled {
    background: #161b22;
    color: #484f58;
    border-color: #21262d;
}
QComboBox QAbstractItemView {
    background: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    outline: none;
    padding: 2px;
}
QLabel#etat {
    color: #8b949e;
    padding-left: 4px;
}
QLabel#etatAlerte {
    color: #d29922;
    font-weight: 600;
    padding-left: 4px;
}
QLabel#etatErreur {
    color: #ff7b72;
    font-weight: 700;
    padding-left: 4px;
}
QLabel#etatSucces {
    color: #3fb950;
    font-weight: 600;
    padding-left: 4px;
}
QDoubleSpinBox[invalide="true"], QComboBox[invalide="true"] {
    border: 2px solid #ff7b72;
    color: #ff7b72;
}
QFrame#separateur {
    color: #30363d;
}
QLabel#enteteTableau {
    font-weight: 600;
    color: #8b949e;
    padding-bottom: 3px;
    border-bottom: 1px solid #30363d;
}
QLabel#symbole {
    font-family: Consolas, "Courier New", monospace;
    font-weight: 700;
    color: #58a6ff;
}
QLabel#valeur {
    font-family: Consolas, "Courier New", monospace;
    font-weight: 600;
    color: #f0f6fc;
}
QLabel#valeurFinale {
    font-family: Consolas, "Courier New", monospace;
    font-size: 14px;
    font-weight: 700;
    color: #3fb950;
}
QLabel#source {
    color: #8b949e;
    font-size: 11px;
}
QLabel#designation {
    color: #c9d1d9;
}
QLabel#unite {
    color: #8b949e;
}
QScrollArea {
    background: transparent;
    border: none;
}
QScrollBar:vertical {
    background: transparent;
    width: 7px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #30363d;
    min-height: 20px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #484f58;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""

STYLE_CLAIR = """
QWidget {
    color: #1f2328;
    font-size: 12px;
}
QGroupBox {
    font-weight: 600;
    border: 1px solid #c8ccd4;
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 6px;
    color: #16202b;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #16202b;
}
QPushButton {
    min-width: 90px;
    padding: 5px 12px;
    border-radius: 5px;
    border: 1px solid #8a9099;
    background: #f2f3f5;
    color: #1f2328;
    font-weight: 500;
}
QPushButton:hover {
    background: #e6e8eb;
}
QPushButton:pressed {
    background: #dcdfe3;
}
QPushButton#calculer {
    background: #1f6feb;
    color: #ffffff;
    border: 1px solid #1a5fc4;
    font-weight: 600;
}
QPushButton#calculer:hover {
    background: #2a7bf5;
}
QPushButton#calculer:pressed {
    background: #1656c0;
}
QPushButton#exporter {
    background: #eef0f3;
    color: #1f2328;
    border: 1px solid #8a9099;
}
QPushButton#exporter:hover {
    background: #e0e3e7;
}
QPushButton#reinitialiser {
    background: #cf3b3b;
    color: #ffffff;
    border: 1px solid #b32e2e;
    font-weight: 600;
}
QPushButton#reinitialiser:hover {
    background: #e04a4a;
}
QPushButton#reinitialiser:pressed {
    background: #b32e2e;
}
QPushButton:disabled {
    background: #eceef0;
    color: #a4a9b0;
    border-color: #d4d7db;
}
QComboBox, QDoubleSpinBox {
    padding: 4px 6px;
    border: 1px solid #c8ccd4;
    border-radius: 4px;
    background: #ffffff;
    color: #1f2328;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
}
QComboBox:hover, QDoubleSpinBox:hover {
    border-color: #0969da;
}
QComboBox:focus, QDoubleSpinBox:focus {
    border-color: #1f6feb;
}
QComboBox:disabled, QDoubleSpinBox:disabled {
    background: #f1f2f4;
    color: #a4a9b0;
    border-color: #d4d7db;
}
QComboBox QAbstractItemView {
    background: #ffffff;
    color: #1f2328;
    border: 1px solid #c8ccd4;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    outline: none;
    padding: 2px;
}
QLabel#etat {
    color: #4a5058;
    padding-left: 4px;
}
QLabel#etatAlerte {
    color: #bf8700;
    font-weight: 600;
    padding-left: 4px;
}
QLabel#etatErreur {
    color: #cf222e;
    font-weight: 700;
    padding-left: 4px;
}
QLabel#etatSucces {
    color: #1a7f37;
    font-weight: 600;
    padding-left: 4px;
}
QDoubleSpinBox[invalide="true"], QComboBox[invalide="true"] {
    border: 2px solid #cf222e;
    color: #cf222e;
}
QFrame#separateur {
    color: #d4d7db;
}
QLabel#enteteTableau {
    font-weight: 600;
    color: #6b7178;
    padding-bottom: 3px;
    border-bottom: 1px solid #e2e5e9;
}
QLabel#symbole {
    font-family: Consolas, "Courier New", monospace;
    font-weight: 700;
    color: #1a5fc4;
}
QLabel#valeur {
    font-family: Consolas, "Courier New", monospace;
    font-weight: 600;
    color: #16202b;
}
QLabel#valeurFinale {
    font-family: Consolas, "Courier New", monospace;
    font-size: 14px;
    font-weight: 700;
    color: #0b7a34;
}
QLabel#source {
    color: #7a8087;
    font-size: 11px;
}
QLabel#designation {
    color: #1f2328;
}
QLabel#unite {
    color: #6b7178;
}
QScrollArea {
    background: transparent;
    border: none;
}
QScrollBar:vertical {
    background: transparent;
    width: 7px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #c8ccd4;
    min-height: 20px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #a4a9b0;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""

STYLE = STYLE_CLAIR


def est_mode_sombre(app: QApplication | None = None) -> bool:
    """Vérifie si le mode sombre est actif pour l'application."""
    if app is None:
        app = QApplication.instance()
    if app is not None:
        hints = app.styleHints()
        if hasattr(hints, "colorScheme"):
            return hints.colorScheme() == Qt.ColorScheme.Dark
        return app.palette().color(QPalette.Window).lightness() < 128
    return True


def _palette_claire() -> QPalette:
    """Construit une QPalette explicitement claire (fond blanc, texte sombre)."""
    p = QPalette()
    blanc      = QColor("#ffffff")
    gris_clair = QColor("#f2f3f5")
    gris_bord  = QColor("#e2e5e9")
    texte      = QColor("#1f2328")
    texte_gris = QColor("#6b7178")
    bleu       = QColor("#1f6feb")

    p.setColor(QPalette.Window,          gris_clair)
    p.setColor(QPalette.WindowText,      texte)
    p.setColor(QPalette.Base,            blanc)
    p.setColor(QPalette.AlternateBase,   gris_clair)
    p.setColor(QPalette.Text,            texte)
    p.setColor(QPalette.BrightText,      texte)
    p.setColor(QPalette.Button,          gris_clair)
    p.setColor(QPalette.ButtonText,      texte)
    p.setColor(QPalette.Highlight,       bleu)
    p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.ToolTipBase,     blanc)
    p.setColor(QPalette.ToolTipText,     texte)
    p.setColor(QPalette.PlaceholderText, texte_gris)
    p.setColor(QPalette.Mid,             gris_bord)
    p.setColor(QPalette.Midlight,        gris_bord)
    p.setColor(QPalette.Dark,            QColor("#c8ccd4"))
    p.setColor(QPalette.Shadow,          QColor("#a4a9b0"))
    p.setColor(QPalette.Link,            bleu)
    return p


def appliquer_style(application: QApplication) -> None:
    """Force la palette claire ET le stylesheet clair, quel que soit le thème système."""
    application.setPalette(_palette_claire())
    application.setStyleSheet(STYLE_CLAIR)


def creer_application(argv: list[str] | None = None) -> QApplication:
    application = QApplication.instance() or QApplication(argv or sys.argv)
    application.setApplicationName("Force sismique - RPS 2011")
    application.setOrganizationName("RPS")
    application.setStyle("Fusion")
    appliquer_style(application)
    hints = application.styleHints()
    if hasattr(hints, "colorSchemeChanged"):
        hints.colorSchemeChanged.connect(lambda _: appliquer_style(application))
    return application


def main(argv: list[str] | None = None) -> int:
    application = creer_application(argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
