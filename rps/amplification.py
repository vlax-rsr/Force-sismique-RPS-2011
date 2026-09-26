import logging

from .utils import (
    Params,
    Source,
)

logger = logging.getLogger(__name__)

# ---- Facteur d'amplification ----

def facteur_amplification(
        zone_acceleration: int,
        zone_vitesse: int,
        T: float,
        direction: str
    ) -> Params:
    """
    Calcule D(T) selon le rapport Za/Zv.

    Tableau 5.3 :
        Za/Zv < 1 : T≤0.25 → 1.9 ; 0.25<T<0.50 → 1.9 ; T≥0.50 → 1.20/T^(2/3)
        Za/Zv = 1 : T≤0.25 → 2.5 ; 0.25<T<0.50 → -2.4T+3.1 ; T≥0.50 → 1.20/T^(2/3)
        Za/Zv > 1 : T≤0.25 → 3.5 ; 0.25<T<0.50 → -6.4T+5.1 ; T≥0.50 → 1.20/T^(2/3)
    
    Args:
        zone_acceleration (int): Zone d'accélération Za (0 à 4).
        zone_vitesse (int): Zone de vitesse Zv (0 à 4).
        T (float): Période fondamentale de vibration.
        direction (str): La direction de la période fondamentale.
    Returns:
        Params: D(T) selon le rapport Za/Zv.
    """
    Za = zone_acceleration
    Zv = zone_vitesse
    signe = ">" if Za > Zv else ("<" if Za < Zv else "=")

    if T <= 0.25:
        if Za < Zv:
            D = 1.9
        elif Za == Zv:
            D = 2.5
        else:
            D = 3.5
        formule = f"D{direction} = valeur forfaitaire (T ≤ 0.25 s, Za/Zv {signe} 1)"
    elif T < 0.5:
        if Za < Zv:
            D = 1.9
            formule = f"D{direction} = 1.9 (0.25 ≤ T < 0.5, Za/Zv {signe} 1)"
        elif Za == Zv:
            D = -2.4 * T + 3.1
            formule = f"D{direction} = -2.4×T + 3.1 = -2.4×{T:.4f} +3.1 (0.25 ≤ T < 0.5, Za/Zv {signe} 1)"
        else:
            D = -6.4 * T + 5.1
            formule = f"D{direction} = -6.4×T + 5.1 = -6.4×{T:.4f} +5.1 (0.25 ≤ T < 0.5, Za/Zv {signe} 1)"
    else: # T >= 0.5
        D = 1.2 / T ** (2/3)
        formule = f"D{direction} = 1.2 / T^(2/3) = 1.2 / {T:.4f}^(2/3) (T ≥ 0.5, Za/Zv {signe} 1)"

    logger.debug("D%s(T=%.4f, Za%sZv) = %.4f", direction, T, signe, D)
    return Params(
        nom=f"Facteur d'amplification {direction}",
        symbole="D",
        valeur=D,
        unite="-",
        description=f"D{direction} pour la période fondamentale de vibration",
        formule=formule,
        source=Source.COEFF_AMPLIFICATION,
        remarque=None
    )