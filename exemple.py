"""Jeu de données d'exemple et procédure de calcul associée.

Ce module ne fait que construire un jeu d'entrée cohérent (`exemple()`), appeler
la procédure du domaine (`executer()`) et renvoyer le résultat. Il ne contient
aucun point d'entrée : le rendu terminal est produit par `lancer.py demo`, via
`affichage.afficher_note()`.
"""

from rps import (
    Batiment,
    ClasseConstruction,
    ClasseSite,
    Geometrie,
    PoidsSismiques,
    Resultats,
    SystemeContreventement,
    Unite,
    ZoneSismique,
    calcul_force_sismique,
    creer_geometrie,
    creer_localisation,
    saisir_charge,
)


def executer(
    localisation: ZoneSismique,
    geometrie: Geometrie,
    batiment: Batiment,
    poids_sismique: PoidsSismiques,
) -> Resultats:
    return calcul_force_sismique(
        localisation=localisation,
        geometrie=geometrie,
        batiment=batiment,
        loads=poids_sismique,
    )


def exemple() -> tuple[ZoneSismique, Geometrie, Batiment, PoidsSismiques]:
    batiment = Batiment(
        type_ossature=SystemeContreventement.PORTIQUE_BA,
        classe=ClasseConstruction.CLASSE_III,
        classe_site=ClasseSite.S2,
    )
    geometrie = creer_geometrie(hauteur=10.0, longueur_x=20.0, longueur_y=15.0)
    localisation = creer_localisation(Za=4, Zv=3)
    poids_sismique = PoidsSismiques(
        Wx=saisir_charge("Poids sismique X", symbole="Wx", unite=Unite.kN, valeur=3111.61),
        Wy=saisir_charge("Poids sismique Y", symbole="Wy", unite=Unite.kN, valeur=3111.61),
    )
    return localisation, geometrie, batiment, poids_sismique
