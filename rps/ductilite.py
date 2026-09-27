import logging

from .utils import (
    ClasseConstruction,
    NiveauDuctilite,
    Params,
    Source,
)

logger = logging.getLogger(__name__)


def niveau_ductilite(
        classe: ClasseConstruction,
        coef_vitesse: float
    )-> Params:
    """
    Détermine le niveau de ductilité en fonction de la classe de construction et du coefficient de vitesse.

    Args:
        classe_construction (ClasseConstruction): La classe de construction.
        coefficient_vitesse (float): Le coefficient de vitesse.

    Returns:
        Params: Le niveau de ductilité en fonction de la classe de construction et du coefficient de vitesse.
    """
    if classe not in ClasseConstruction:
        raise ValueError(f"Classe de construction non prise en charge: {classe}")
    if coef_vitesse < 0.00:
        raise ValueError(f"Le coefficient de vitesse ne doit pas être négatif: {coef_vitesse}")
    if classe in (ClasseConstruction.CLASSE_I, ClasseConstruction.CLASSE_II):
        if coef_vitesse <= 0.10:
            nd = NiveauDuctilite.ND1
        elif coef_vitesse <= 0.20:
            nd = NiveauDuctilite.ND2
        else:
            nd = NiveauDuctilite.ND3
    elif classe == ClasseConstruction.CLASSE_III:
        nd = NiveauDuctilite.ND1 if coef_vitesse <= 0.20 else NiveauDuctilite.ND2
    else:
        raise ValueError(f"Classe d'importance inconnue : {classe}")
    
    logger.debug("ND(%s, v=%.3f) = %s", classe.value, coef_vitesse, nd.value)

    return Params(
        nom="Niveau de ductilité",
        symbole="ND",
        valeur=nd,
        unite="-",
        description="Niveau de ductilité en fonction de la classe de construction et du coefficient de vitesse",
        formule=f"ND = f({classe.value}, {coef_vitesse})",
        source=Source.DUCTILITE,
        remarque=None
    )