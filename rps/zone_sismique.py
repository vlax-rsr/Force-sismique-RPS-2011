import logging

from .utils import Params, Source, ZoneVitesse

logger = logging.getLogger(__name__)

# --- Coefficient de vitesse ----

COEFF_VITESSE = {
    ZoneVitesse.ZONE_0: 0.00,
    ZoneVitesse.ZONE_1: 0.07,
    ZoneVitesse.ZONE_2: 0.10,
    ZoneVitesse.ZONE_3: 0.13,
    ZoneVitesse.ZONE_4: 0.17,
}

def coefficient_vitesse(zone_vitesse: ZoneVitesse) -> Params:
    """
    Retourne le coefficient de vitesse en fonction de la zone de vitesse.

    Args:
        zone_vitesse (ZoneVitesse): La zone de vitesse.

    Returns:
        float: Le coefficient de vitesse correspondant.
    """
    if zone_vitesse in COEFF_VITESSE:
        coef_v = COEFF_VITESSE[zone_vitesse]
        remarque = None
    else:
        remarque = f"Zone de vitesse non prise en charge: {zone_vitesse}. Utilisation de la valeur maximale (υ = 0.17)."
        logger.warning(remarque)
        coef_v = 0.17

    return Params(
        nom="Coefficient de vitesse",
        symbole="υ",
        valeur=coef_v,
        unite="-",
        description="Coefficient de vitesse",
        formule="f(zone_vitesse)",
        source=Source.COEFF_VITESSE,
        remarque=remarque
    )