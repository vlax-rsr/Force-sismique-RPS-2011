from rps import utils
from rps.zone_sismique import coefficient_vitesse


def test_coeff_vitesse_0():
    assert coefficient_vitesse(utils.ZoneVitesse.ZONE_0).valeur == 0.00

def test_coeff_vitesse_1():
    assert coefficient_vitesse(utils.ZoneVitesse.ZONE_1).valeur == 0.07