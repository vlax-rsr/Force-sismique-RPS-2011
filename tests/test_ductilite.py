from rps import ductilite
from rps.utils import ClasseConstruction, NiveauDuctilite


def test_niveau_ductilite_1():
    assert ductilite.niveau_ductilite(ClasseConstruction.CLASSE_I, 0.13).valeur == NiveauDuctilite.ND2
    assert ductilite.niveau_ductilite(ClasseConstruction.CLASSE_II, 0.17).valeur == NiveauDuctilite.ND2
    assert ductilite.niveau_ductilite(ClasseConstruction.CLASSE_III, 0.13).valeur == NiveauDuctilite.ND1