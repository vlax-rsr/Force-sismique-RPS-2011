"""Affichage du bilan de calcul : en-tête, données d'entrée, paramètres RPS, résultats."""

import sys
from enum import Enum

from rps import (
    Batiment,
    Geometrie,
    Params,
    PoidsSismiques,
    Resultats,
    Unite,
    ZoneSismique,
)

LARGEUR = 78


def _regle(caractere: str = "-") -> str:
    return caractere * LARGEUR


def _titre(section: str) -> str:
    return f"\n{section.upper()}\n{_regle()}"


def unite_texte(param: Params) -> str:
    return param.unite.value if isinstance(param.unite, Unite) else param.unite


def source_texte(param: Params) -> str:
    return param.source.value if param.source else ""


def _ligne(symbole: str, libelle: str, valeur: str, unite: str = "", source: str = "") -> str:
    return f"  {symbole:<8} {libelle:<32} {valeur:>11} {unite:<5} {source}".rstrip()


def valeur_texte(param: Params, decimales: int = 4) -> str:
    if isinstance(param.valeur, Enum):
        return str(param.valeur.value)
    return f"{param.valeur:.{decimales}f}".rstrip("0").rstrip(".")


def _ligne_params(param: Params, with_source: bool = False, decimales: int = 2) -> str:
    return _ligne(
        param.symbole or "-",
        param.nom,
        valeur_texte(param, decimales),
        unite_texte(param),
        source_texte(param) if with_source else "",
    )


def rendre_entete(titre: str, formule: str = "F = υ.I.D.S.W/K") -> str:
    return "\n".join((
        _regle("="),
        titre.center(LARGEUR),
        formule.center(LARGEUR),
        _regle("="),
    ))


def rendre_donnees_entree(
    localisation: ZoneSismique,
    geometrie: Geometrie,
    batiment: Batiment,
    poids_sismique: PoidsSismiques,
) -> str:
    return "\n".join((
        _titre("Données d'entrée"),
        "  Localisation",
        f"    Zone d'accélération             Za = {localisation.za.value}",
        f"    Zone de vitesse                 Zv = {localisation.zv.value}",
        "  Géométrie",
        f"    Hauteur                         H  = {geometrie.hauteur:.2f} m",
        f"    Longueur                        Lx = {geometrie.longueur_x:.2f} m",
        f"    Longueur                        Ly = {geometrie.longueur_y:.2f} m",
        "  Structure",
        f"    Ossature                           = {batiment.type_ossature.value}",
        f"    Classe de construction             = {batiment.classe.libelle}",
        f"    Classe de site                     = {batiment.classe_site.value}"
        f"{' (valeur manuelle)' if batiment.coef_site_manuel is not None else ''}",
        "  Charges",
        _ligne_params(poids_sismique.Wx, decimales=2),
        _ligne_params(poids_sismique.Wy, decimales=2),
    ))


def rendre_parametres_rps(resultats: Resultats) -> str:
    lignes = [
        _titre("Paramètres RPS"),
        _ligne("Sym", "Désignation", "Valeur", "Unité", "Source"),
    ]
    for param in (resultats.upsilon, resultats.I, resultats.S, resultats.nd, resultats.K):
        lignes.append(_ligne_params(param, with_source=True))
    return "\n".join(lignes)


def rendre_resultats(resultats: Resultats) -> str:
    lignes = [_titre("Résultats")]
    for direction, T, D, W, F in (
        ("X", resultats.Tx, resultats.Dx, resultats.Wx, resultats.Fx),
        ("Y", resultats.Ty, resultats.Dy, resultats.Wy, resultats.Fy),
    ):
        lignes.append(f"  Direction {direction}")
        lignes.append(_ligne("Symbole", "Désignation", "Valeur", "Unité", ""))
        for param in (T, D):
            lignes.append(_ligne_params(param))
        lignes.append(_ligne_params(F, decimales=2))
    lignes.append(_regle("="))
    return "\n".join(lignes)


def rendre_bilan(
    resultats: Resultats,
    localisation: ZoneSismique,
    geometrie: Geometrie,
    batiment: Batiment,
    poids_sismique: PoidsSismiques,
) -> str:
    """Bilan complet sous forme de texte (réutilisé par l'interface graphique)."""
    return "\n".join((
        rendre_entete("CALCUL DE LA FORCE SISMIQUE ÉQUIVALENTE — RPS 2011"),
        rendre_donnees_entree(localisation, geometrie, batiment, poids_sismique),
        rendre_parametres_rps(resultats),
        rendre_resultats(resultats),
    ))


def afficher_entete(titre: str, formule: str = "F = υ.I.D.S.W/K") -> None:
    print(rendre_entete(titre, formule))


def afficher_donnees_entree(
    localisation: ZoneSismique,
    geometrie: Geometrie,
    batiment: Batiment,
    poids_sismique: PoidsSismiques,
) -> None:
    print(rendre_donnees_entree(localisation, geometrie, batiment, poids_sismique))


def afficher_parametres_rps(resultats: Resultats) -> None:
    print(rendre_parametres_rps(resultats))


def afficher_resultats(resultats: Resultats) -> None:
    print(rendre_resultats(resultats))


def afficher_bilan(
    resultats: Resultats,
    localisation: ZoneSismique,
    geometrie: Geometrie,
    batiment: Batiment,
    poids_sismique: PoidsSismiques,
) -> None:
    print(rendre_bilan(resultats, localisation, geometrie, batiment, poids_sismique))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    from main import executer, exemple

    entree = exemple()
    afficher_bilan(executer(*entree), *entree)
