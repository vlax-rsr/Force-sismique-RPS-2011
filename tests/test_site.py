from rps import site_sismique
from rps.utils import ClasseSite


def test_coeff_site_1():
    assert site_sismique.coefficient_site(ClasseSite.S1).valeur == 1.0

def test_coeff_site_2():
    assert site_sismique.coefficient_site(ClasseSite.S2).valeur == 1.2

def test_coeff_site_5():
    assert site_sismique.coefficient_site(ClasseSite.S5, 2.0).valeur == 2.0

def test_coeff_site_5_sans_valeur_manuelle():
    try:
        site_sismique.coefficient_site(ClasseSite.S5)
    except ValueError:
        return
    raise AssertionError("Une ValueError est attendue pour S5 sans valeur manuelle")
