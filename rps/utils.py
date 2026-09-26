from dataclasses import dataclass
from enum import Enum


class ZoneAcceleration(Enum):
    ZONE_0 = 0
    ZONE_1 = 1
    ZONE_2 = 2
    ZONE_3 = 3
    ZONE_4 = 4

class ZoneVitesse(Enum):
    ZONE_0 = 0
    ZONE_1 = 1
    ZONE_2 = 2
    ZONE_3 = 3
    ZONE_4 = 4

class ClasseConstruction(Enum):
    CLASSE_I = 1
    CLASSE_II = 2
    CLASSE_III = 3

    @property
    def libelle(self) -> str:
        """Libellé affichable : « Classe I », « Classe II », « Classe III »."""
        return f"Classe {self.name.rsplit('_', 1)[-1]}"

class ClasseSite(Enum):
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"

class NiveauDuctilite(Enum):
    ND1 = "ND1"
    ND2 = "ND2"
    ND3 = "ND3"

class SystemeContreventement(Enum):
    # Béton armé
    PORTIQUE_BA = "Portique en béton armé"
    VOILE_PORTIQUE_BA = "Portique et voile en béton armé"
    VOILE_BA = "Voile en béton armé"
    VOILE_COUPLE_BA = "Voiles couplés en béton armé"

    # Acier
    OSSATURE_ACIER_CONTREVENTEE = "Ossature en charpente en acier contreventée"
    PORTIQUE_ACIER_RIGIDE = "Portique en charpente en acier à noeuds rigides"

class ZoneSismique:
    def __init__(self, zone_acceleration: ZoneAcceleration, zone_vitesse: ZoneVitesse):
        self.za = zone_acceleration
        self.zv = zone_vitesse

class Geometrie:
    def __init__(self, hauteur: float, longueur_x: float, longueur_y: float):
        self.hauteur = hauteur
        self.longueur_x = longueur_x
        self.longueur_y = longueur_y

class Source(Enum):
    COEFF_VITESSE = "RPS 2011 - Tableau 5.1"
    COEFF_IMPORTANCE = "RPS 2011 - Tableau 3.1"
    COEFF_SITE = "RPS 2011 - Tableau 5.2"
    COEFF_AMPLIFICATION = "RPS 2011 - Tableau 5.3"
    FACTEUR_COMPORTEMENT = "RPS 2011 - Tableau 3.3"
    DUCTILITE = "RPS 2011 - Tableau 3.2"
    CALCULE = "Calculé selon les formules"

class Unite(Enum):
    kN = "kN"
    daN = "daN"
    kgf = "kgf"
    t = "t"
    s = "s"
    m = "m"

@dataclass (frozen=True)
class Params:
    nom: str
    symbole: str | None = None
    valeur: float = 0.0
    unite: str | Unite = "-"
    description: str | None = None
    formule: str | None = None
    source: Source | None = None
    remarque: str | None = None
