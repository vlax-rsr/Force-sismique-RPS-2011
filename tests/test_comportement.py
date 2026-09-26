from rps import comportement
from rps.utils import NiveauDuctilite, SystemeContreventement


def test_facteur_comportement():
    assert comportement.facteur_comportement(NiveauDuctilite.ND1, SystemeContreventement.PORTIQUE_BA).valeur == 2.0
    assert comportement.facteur_comportement(NiveauDuctilite.ND2, SystemeContreventement.OSSATURE_ACIER_CONTREVENTEE).valeur == 3.0
    assert comportement.facteur_comportement(NiveauDuctilite.ND3, SystemeContreventement.VOILE_COUPLE_BA).valeur == 3.5