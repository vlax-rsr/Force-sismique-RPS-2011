"""Rendu de la formule de calcul : LaTeX (matplotlib mathtext) avec repli en texte enrichi."""

import io

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel

LATEX = r"$F \;=\; \dfrac{\upsilon \cdot I \cdot D \cdot S \cdot W}{K}$"
TEXTE = "F = υ.I.D.S.W / K"
LARGEUR_MAX = 420
HAUTEUR_CIBLE = 52

# Couleur fixe : noir profond, lisible sur fond clair
COULEUR_FORMULE = "#1a1a1a"


def est_mode_sombre() -> bool:
    """Détecte si l'application ou l'OS est actuellement en mode sombre."""
    app = QApplication.instance()
    if app is not None:
        hints = app.styleHints()
        if hasattr(hints, "colorScheme"):
            return hints.colorScheme() == Qt.ColorScheme.Dark
        from PySide6.QtGui import QPalette
        return app.palette().color(QPalette.Window).lightness() < 128
    return True


def repli_html(sombre: bool | None = None) -> str:  # noqa: ARG001
    """Texte enrichi de secours — toujours en noir, avec fraction CSS élégante."""
    return (
        '<span style="'
        "font-family: 'Cambria Math', Cambria, Georgia, serif;"
        "font-size: 15pt;"
        f"color: {COULEUR_FORMULE};"
        '">'
        "<i>F</i>"
        ' <span style="font-size:13pt; vertical-align:middle;">=</span> '
        '<span style="display:inline-block; text-align:center; vertical-align:middle;">'
        '<span style="display:block; border-bottom:1.5px solid #1a1a1a; padding-bottom:1px;">'
        "<i>υ</i>&thinsp;·&thinsp;<i>I</i>&thinsp;·&thinsp;<i>D</i>"
        "&thinsp;·&thinsp;<i>S</i>&thinsp;·&thinsp;<i>W</i>"
        "</span>"
        '<span style="display:block; padding-top:2px;"><i>K</i></span>'
        "</span>"
        "</span>"
    )


def pixmap_formule(
    largeur_max: int = LARGEUR_MAX,
    sombre: bool | None = None,  # noqa: ARG001  — ignoré, on force le noir
    hauteur_cible: int = HAUTEUR_CIBLE,
) -> QPixmap | None:
    """Formule rasterisée en PNG haute résolution ; None si matplotlib est indisponible."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
    except Exception:
        return None

    try:
        figure = Figure(figsize=(5.5, 0.9), dpi=180)
        figure.patch.set_alpha(0.0)
        ax = figure.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        ax.patch.set_alpha(0.0)
        ax.text(
            0.5,
            0.5,
            LATEX,
            ha="center",
            va="center",
            fontsize=22,
            color=COULEUR_FORMULE,
            transform=ax.transAxes,
        )
        tampon = io.BytesIO()
        figure.savefig(
            tampon,
            format="png",
            transparent=True,
            bbox_inches="tight",
            pad_inches=0.04,
            dpi=180,
        )
        plt.close(figure)
    except Exception:
        return None

    pixmap = QPixmap()
    if not pixmap.loadFromData(tampon.getvalue(), "PNG") or pixmap.isNull():
        return None

    if pixmap.height() > hauteur_cible:
        pixmap = pixmap.scaledToHeight(hauteur_cible, Qt.SmoothTransformation)
    if pixmap.width() > largeur_max:
        pixmap = pixmap.scaledToWidth(largeur_max, Qt.SmoothTransformation)
    return pixmap


def etiquette_formule(largeur_max: int = LARGEUR_MAX, sombre: bool | None = None) -> QLabel:
    """QLabel contenant la formule en LaTeX, ou son équivalent en texte enrichi."""
    etiquette = QLabel()
    etiquette.setAlignment(Qt.AlignCenter)
    etiquette.setObjectName("formule")
    etiquette.setToolTip(f"{TEXTE}  ({LATEX})")
    etiquette.setContentsMargins(0, 4, 0, 6)

    # On ignore le paramètre sombre : la formule est toujours en noir
    pixmap = pixmap_formule(largeur_max)
    if pixmap is None:
        etiquette.setTextFormat(Qt.RichText)
        etiquette.setText(repli_html())
    else:
        etiquette.setPixmap(pixmap)
    return etiquette
