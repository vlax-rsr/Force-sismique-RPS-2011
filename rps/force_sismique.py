"""
Calcul de la force sismique sur un élément de structure

Formule de calcul :
F = υ.I.D.S.W/K

Arguments :
- υ : Paramètre de vitesse
- I : Facteur d'importance
- D : Facteur de distance
- S : Coefficient de site
- W : Poids sismique du bâtiment
- K : Coefficient de comportement
"""

def force_sismique(v, I, D, S, W, K):
    """
    Calcule la force sismique sur un élément de structure.

    Args:
        υ (float): Paramètre de vitesse.
        I (float): Facteur d'importance.
        D (float): Facteur d'amplification.
        S (float): Coefficient de site.
        W (float): Poids sismique du bâtiment.
        K (float): Coefficient de comportement.

    Returns:
        float: La force sismique calculée.
    """
    F = v * I * D * S * W / K
    return F