import pytest

from rps import periode
from rps.utils import SystemeContreventement


def test_periode_1():
    T = periode.calcul_periode(
        hauteur=10,
        longueur=10,
        type_ossature=SystemeContreventement.PORTIQUE_BA,
        direction='X'
    )
    assert T.valeur == pytest.approx(expected=0.42175, abs=1e-5)
    assert T.unite == 's'
    assert T.formule == 'T(X) = 0.075×H^(3/4)'