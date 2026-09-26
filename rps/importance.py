import logging

from .utils import ClasseConstruction, Params, Source

logger = logging.getLogger(__name__)    

# ---- Coefficient d'importance ----

COEF_IMPORTANCE = {
    ClasseConstruction.CLASSE_I: 1.30,
    ClasseConstruction.CLASSE_II: 1.20,
    ClasseConstruction.CLASSE_III: 1.00,
}

def coefficient_importance(classe_construction: ClasseConstruction) -> Params:
    """
    Retourne le coefficient d'importance en fonction de la classe de construction.

    Args:
        classe_construction (ClasseConstruction): La classe de construction.

    Returns:
        Params: Les paramètres du coefficient d'importance correspondant.
    """
    if classe_construction not in COEF_IMPORTANCE:
        message = f"Classe de construction non prise en charge: {classe_construction}. Utilisation de la valeur par défaut (I = 1.0)."
        logger.warning(message)
        coef_i = 1.0
    coef_i = COEF_IMPORTANCE.get(classe_construction, 1.0)
    return Params(
        nom="Coefficient d'importance",
        symbole="I",
        valeur=coef_i,
        unite="-",
        description="Coefficient d'importance",
        formule="f(classe_construction)",
        source=Source.COEFF_IMPORTANCE,
        remarque=message if classe_construction not in COEF_IMPORTANCE else None
    )