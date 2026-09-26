from dataclasses import dataclass

from .utils import (
    ClasseConstruction,
    ClasseSite,
    Geometrie,
    Params,
    Source,
    SystemeContreventement,
    ZoneAcceleration,
    ZoneSismique,
    ZoneVitesse,
)
from .amplification import facteur_amplification
from .comportement import facteur_comportement
from .ductilite import niveau_ductilite
from .force_sismique import force_sismique
from .importance import coefficient_importance
from .parametre import Resultats
from .periode import calcul_periode
from .site_sismique import coefficient_site
from .zone_sismique import coefficient_vitesse


def creer_localisation(Za: int, Zv: int) -> ZoneSismique:
    """
    Crée une localisation de la structure.
    Args:
        Za (int): Zone d'accélération.
        Zv (int): Zone de vitesse.
    Returns:
        ZoneSismique: La localisation de la structure.
    """
    if Za not in {zone.value for zone in ZoneAcceleration}:
        raise ValueError(f"La valeur de Za : {Za} non reconnue")
    if Zv not in {zone.value for zone in ZoneVitesse}:
        raise ValueError(f"La valeur de Zv : {Zv} non reconnue")
    
    return ZoneSismique(
        zone_acceleration=ZoneAcceleration(Za),
        zone_vitesse=ZoneVitesse(Zv),
    )

def creer_geometrie(
        hauteur: float,
        longueur_x: float,
        longueur_y: float
    ) -> Geometrie:
    if hauteur <= 0:
        raise ValueError("La hauteur doit être supérieure à 0")
    if longueur_x <= 0:
        raise ValueError("La longueur_x doit être supérieure à 0")
    if longueur_y <= 0:
        raise ValueError("La longueur_y doit être supérieure à 0")
    
    return Geometrie(hauteur=hauteur, longueur_x=longueur_x, longueur_y=longueur_y)

@dataclass
class Batiment:
    type_ossature: SystemeContreventement
    classe: ClasseConstruction
    classe_site: ClasseSite
    coef_site_manuel: float | None = None

@dataclass
class PoidsSismiques:
    Wx: Params
    Wy: Params

def calcul_force_sismique(
    localisation: ZoneSismique,
    geometrie: Geometrie,
    batiment: Batiment,
    loads: PoidsSismiques,
) -> Resultats:
    
    # Coefficient de vitesse
    za = localisation.za.value
    zv = localisation.zv.value
    upsilon = coefficient_vitesse(localisation.zv)

    # Coefficient d'importance
    I = coefficient_importance(batiment.classe)

    # Periode
    Tx = calcul_periode(
        hauteur=geometrie.hauteur,
        longueur=geometrie.longueur_x,
        type_ossature=batiment.type_ossature,
        direction="X",
    )
    Ty = calcul_periode(
        hauteur=geometrie.hauteur,
        longueur=geometrie.longueur_y,
        type_ossature=batiment.type_ossature,
        direction="Y",
    )

    # Facteur d'amplification
    Dx = facteur_amplification(
        zone_acceleration=za,
        zone_vitesse=zv,
        T=Tx.valeur,
        direction="X",
    )
    Dy = facteur_amplification(
        zone_acceleration=za,
        zone_vitesse=zv,
        T=Ty.valeur,
        direction="Y",
    )

    # Coefficient de site
    S = coefficient_site(batiment.classe_site, batiment.coef_site_manuel)

    # Niveau de ductilité
    nd = niveau_ductilite(batiment.classe, upsilon.valeur)

    # Facteur de comportement
    K = facteur_comportement(nd.valeur, batiment.type_ossature)

    # Forces sismiques
    Fx = force_sismique(
        v=upsilon.valeur,
        I=I.valeur,
        D=Dx.valeur,
        S=S.valeur,
        W=loads.Wx.valeur,
        K=K.valeur,
    )
    Fy = force_sismique(
        v=upsilon.valeur,
        I=I.valeur,
        D=Dy.valeur,
        S=S.valeur,
        W=loads.Wy.valeur,
        K=K.valeur,
    )

    return Resultats(
        upsilon=upsilon,
        I=I,
        S=S,
        nd=nd,
        K=K,
        Tx=Tx,
        Ty=Ty,
        Dx=Dx,
        Dy=Dy,
        Wx=loads.Wx,
        Wy=loads.Wy,
        Fx=force_params("X", Fx, loads.Wx),
        Fy=force_params("Y", Fy, loads.Wy),
    )


def force_params(direction: str, force: float, poids: Params) -> Params:
    return Params(
        nom=f"Force sismique {direction}",
        symbole="F",
        valeur=force,
        unite=poids.unite,
        description=f"Force sismique équivalente dans la direction {direction}",
        formule="F = υ.I.D.S.W/K",
        source=Source.CALCULE,
        remarque=None
    )
