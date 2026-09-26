import logging

from .utils import (
    NiveauDuctilite,
    Params,
    Source,
    SystemeContreventement,
)

logger = logging.getLogger(__name__)

FACTEUR_COMPORTEMENT = {
    SystemeContreventement.PORTIQUE_BA:                 {NiveauDuctilite.ND1: 2.0, NiveauDuctilite.ND2: 3.5, NiveauDuctilite.ND3: 5.0},
    SystemeContreventement.VOILE_PORTIQUE_BA:           {NiveauDuctilite.ND1: 2.0, NiveauDuctilite.ND2: 3.0, NiveauDuctilite.ND3: 4.0},
    SystemeContreventement.VOILE_BA:                    {NiveauDuctilite.ND1: 1.4, NiveauDuctilite.ND2: 2.1, NiveauDuctilite.ND3: 2.8},
    SystemeContreventement.VOILE_COUPLE_BA:             {NiveauDuctilite.ND1: 1.8, NiveauDuctilite.ND2: 2.5, NiveauDuctilite.ND3: 3.5},# ND3 omis car absent du tableau
    SystemeContreventement.PORTIQUE_ACIER_RIGIDE:       {NiveauDuctilite.ND1: 3.0, NiveauDuctilite.ND2: 4.5, NiveauDuctilite.ND3: 6.0},
    SystemeContreventement.OSSATURE_ACIER_CONTREVENTEE: {NiveauDuctilite.ND1: 2.0, NiveauDuctilite.ND2: 3.0, NiveauDuctilite.ND3: 4.0},
}

definition_F = "Facteur de réduction de la force sismique de calcul caractérisant la capacité d'une structure à dissiper l'énergie par comportement inélastique."

def facteur_comportement(nd: NiveauDuctilite, ossature: SystemeContreventement) -> Params:
    if ossature not in FACTEUR_COMPORTEMENT:
        raise ValueError(
            f"Type d'ossature non pris en charge pour le calcul du facteur de "
            f"comportement : {ossature.value}"
        )
    if nd not in FACTEUR_COMPORTEMENT[ossature]:
        raise ValueError(
            f"Niveau de ductilité {nd.value} absent du tableau 3.3 pour l'ossature "
            f"« {ossature.value} »"
        )

    K = FACTEUR_COMPORTEMENT[ossature][nd]
    logger.debug("K(%s, %s) = %s", ossature.value, nd.value, K)

    return Params(
        nom="Facteur de comportement",
        symbole="K",
        valeur=K,
        unite="-",
        description=definition_F,
        formule=f"K = f({ossature.value}, {nd.value})",
        source=Source.FACTEUR_COMPORTEMENT,
        remarque=None
    )