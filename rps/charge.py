from .utils import Params, Unite

UNITE_POIDS = [Unite.kN, Unite.daN, Unite.kgf]
def saisir_charge(
    nom: str,
    symbole: str | None = None,
    valeur: float = 0.0,
    unite: Unite = Unite.daN,
    ) -> Params:
    if unite not in UNITE_POIDS:
        raise ValueError(f"L'unité de poids n'est pas reconnue : {unite}")
    if valeur <= 0:
        raise ValueError(f"{nom} : la valeur doit être supérieure à 0 (champ non renseigné)")
    
    return Params(
        nom=nom,
        symbole=symbole,
        valeur=valeur,
        unite=unite,
    )