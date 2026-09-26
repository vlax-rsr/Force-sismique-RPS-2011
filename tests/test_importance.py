from rps import importance
from rps.utils import ClasseConstruction


def test_coeff_i_1():
    assert importance.coefficient_importance(ClasseConstruction.CLASSE_I).valeur == 1.30

def test_coeff_i_2():
    assert importance.coefficient_importance(ClasseConstruction.CLASSE_II).valeur == 1.20