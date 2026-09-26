"""Conteneur de sortie de la procédure de calcul."""

from dataclasses import dataclass

from .utils import Params


@dataclass
class Resultats:
    """Output final du calcul : chaque attribut est un Params (valeur + traçabilité)."""

    upsilon: Params                    # υ
    I: Params                          # I
    S: Params                          # S
    nd: Params                         # niveau de ductilité
    K: Params                          # K
    Tx: Params                         # période X
    Ty: Params                         # période Y
    Dx: Params                         # amplification X
    Dy: Params                         # amplification Y
    Wx: Params                         # poids sismique X
    Wy: Params                         # poids sismique Y
    Fx: Params                         # force sismique X
    Fy: Params                         # force sismique Y
