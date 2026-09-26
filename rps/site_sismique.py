import logging

from .utils import ClasseSite, Params, Source

logger = logging.getLogger(__name__)

COEFF_SITE = {
    ClasseSite.S1: 1.0,
    ClasseSite.S2: 1.2,
    ClasseSite.S3: 1.4,
    ClasseSite.S4: 1.8,
}


# ---- Coefficient de site ----

def coefficient_site(classe_site: str, valeur_manuelle: float | None = None) -> Params:
    """
    Retourne le coefficient de site en fonction de la classe de site.

    Args:
        classe_site (ClasseSite): La classe de site.
        valeur_manuelle (float | None): La valeur de site à utiliser si elle est connue.

    Returns:
        Params: Les paramètres du coefficient de site correspondant.
    """
    if classe_site == ClasseSite.S5:
        if valeur_manuelle is None:
            raise ValueError(
                    "Site S5 : La valeur de S doit être déterminée par une étude "
                    "géotechnique. Veuillez saisir la valeur manuellement."
                )
        logger.info("S5 — valeur manuelle utilisée : S=%s", valeur_manuelle)
        return Params(
            nom="Coefficient de site",
            symbole="S",
            valeur=valeur_manuelle,
            unite="-",
            description="Coefficient de site",
            formule=f"S = f({classe_site.value})",
            source=Source.COEFF_SITE,
            remarque="Valeur issue d'une étude géotechnique spécifique."
        )

    
    if classe_site not in COEFF_SITE:
        raise ValueError(f"Site de classe inconnue: {classe_site}")

    S = COEFF_SITE[classe_site]
    return Params(
        nom="Coefficient de site",
        symbole="S",
        valeur=S,
        unite="-",
        description="Coefficient de site",
        formule=f"S = f({classe_site.value})",
        source=Source.COEFF_SITE,
        remarque=None
    )