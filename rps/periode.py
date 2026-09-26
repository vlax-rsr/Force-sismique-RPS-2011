import logging

from .utils import (
    Params,
    Source,
    SystemeContreventement,
)

logger = logging.getLogger(__name__)

# ---- Période fondamentale de vibration ----

def calcul_periode(
        hauteur: float,
        longueur: float,
        type_ossature: SystemeContreventement,
        direction: str
    ) -> Params:
    """
    Retourne la période fondamentale de vibration dans la direction spécifiée en fonction de la géométrie et du type d'ossature.

    Args:
        geometrie (Geometrie): La géométrie de la structure.
        type_ossature (TypeOssatures): Le type d'ossature.
        direction (str | None): La direction de la période fondamentale.

    Returns:
        Params: La période fondamentale de vibration dans la direction spécifiée.
    """
    if type_ossature not in SystemeContreventement:
        raise ValueError(f"Type d'ossature non pris en charge pour le calcul de la période fondamentale: {type_ossature}")
    
    if type_ossature == SystemeContreventement.PORTIQUE_BA or type_ossature == SystemeContreventement.OSSATURE_ACIER_CONTREVENTEE:
        T = 0.075 * hauteur ** (3/4)
        formule = f"T({direction}) = 0.075×H^(3/4)"
    elif type_ossature == SystemeContreventement.PORTIQUE_ACIER_RIGIDE:
        T = 0.085 * hauteur ** (3/4)
        formule = f"T{direction} = 0.085×H^(3/4)"
    else:
        T = 0.09 * hauteur / longueur ** 0.5
        formule = f"T{direction} = 0.09×H / L^(0.5)"

    logger.debug("T(%s) = %.2f s", direction, T)
    return Params(
            nom=f"Période fondamentale {direction}",
            symbole="T",
            valeur=T,
            unite="s",
            description="Période fondamentale de vibration dans la direction spécifiée",
            formule= formule if formule else None,
            source=Source.CALCULE,
            remarque=None
        )