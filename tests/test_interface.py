import logging
import os
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QComboBox, QGroupBox, QHBoxLayout, QLabel, QPushButton  # noqa: E402

from interface import fenetre as module_fenetre  # noqa: E402
from interface import journal as module_journal  # noqa: E402
from interface.app import creer_application  # noqa: E402
from interface.fenetre import FenetrePrincipale  # noqa: E402
from interface.formule import etiquette_formule  # noqa: E402
from rps import ClasseConstruction, ClasseSite, ZoneAcceleration, ZoneVitesse  # noqa: E402

FX_ATTENDU = "693.44"  # jeu de données « tout renseigné » défini dans _remplir


@pytest.fixture(scope="module")
def application():
    return creer_application([])


@pytest.fixture
def fenetre(application):
    f = FenetrePrincipale()
    yield f
    f.close()


def _barre_actions(f: FenetrePrincipale) -> list:
    for layout in reversed(f.findChildren(QHBoxLayout)):
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        if any(isinstance(w, QPushButton) for w in widgets):
            return widgets
    raise AssertionError("Barre d'actions introuvable")


def _remplir(f: FenetrePrincipale) -> None:
    """Renseigne un jeu de données complet et valide (Za=Zv=3, Voile BA, Classe II, S2)."""
    formulaire = f.formulaire
    formulaire.za.setCurrentIndex(ZoneAcceleration.ZONE_3.value)
    formulaire.zv.setCurrentIndex(ZoneVitesse.ZONE_3.value)
    formulaire.hauteur.setValue(10.0)
    formulaire.longueur_x.setValue(20.0)
    formulaire.longueur_y.setValue(15.0)
    formulaire.ossature.setCurrentIndex(2)  # Voile en béton armé
    formulaire.classe.setCurrentIndex(1)  # Classe II
    formulaire.classe_site.setCurrentIndex(1)  # S2
    formulaire.poids_x.setValue(3111.61)
    formulaire.poids_y.setValue(3111.61)


def test_ordre_barre_actions(fenetre):
    widgets = [w for w in _barre_actions(fenetre) if w is not None]
    assert widgets[0] is fenetre.etat
    assert [w.objectName() for w in widgets[1:]] == [
        "calculer", "exporter", "reinitialiser",
    ]


def test_reinitialiser_est_rouge(fenetre, application):
    assert fenetre.bouton_reinitialiser.objectName() == "reinitialiser"
    assert "#reinitialiser" in application.styleSheet()


def test_etat_ne_signale_rien_avant_le_clic(fenetre):
    """Tant que Calculer n'a pas été cliqué, l'état reste le message d'accueil, sans mise en rouge."""
    assert fenetre.etat.objectName() == "etat"
    assert fenetre.etat.text() == module_fenetre.MESSAGE_ETAT
    assert fenetre.bouton_calculer.isEnabled() is True
    assert fenetre.bouton_exporter.isEnabled() is False
    for champ in fenetre.formulaire._champs:
        assert champ.property("invalide") is False


def test_champ_edited_invalide_est_rouge(fenetre):
    """Le champ en cours de saisie passe en rouge dès qu'il est vidé, sans message d'état."""
    fenetre.formulaire.poids_x.setValue(1500.0)
    fenetre.formulaire.poids_x.setValue(0.0)
    assert fenetre.formulaire.poids_x.property("invalide") is True
    assert fenetre.etat.objectName() == "etat"
    assert fenetre.formulaire.hauteur.property("invalide") is False

    fenetre.formulaire.poids_x.setValue(1500.0)
    assert fenetre.formulaire.poids_x.property("invalide") is False


def test_calculer_liste_les_champs_errones_en_rouge(fenetre):
    fenetre.calculer()
    assert fenetre.etat.objectName() == "etatErreur"
    assert fenetre.etat.text() == "Les valeurs saisies sont erronées : H, Lx, Ly, Wx, Wy"
    assert fenetre.bouton_exporter.isEnabled() is False
    for nom in ("hauteur", "longueur_x", "longueur_y", "poids_x", "poids_y"):
        assert getattr(fenetre.formulaire, nom).property("invalide") is True


def test_calcul_reussi_affiche_un_etat_vert(fenetre):
    _remplir(fenetre)
    assert fenetre.etat.objectName() == "etat"

    fenetre.calculer()
    assert fenetre.etat.objectName() == "etatSucces"
    assert fenetre.etat.text() == module_fenetre.MESSAGE_SUCCES
    assert fenetre.bouton_exporter.isEnabled() is True


def test_modification_apres_calcul_signale_des_donnees_modifiees(fenetre):
    _remplir(fenetre)
    fenetre.calculer()
    fenetre.formulaire.poids_x.setValue(4000.0)
    assert fenetre.etat.objectName() == "etat"
    assert fenetre.etat.text() == module_fenetre.MESSAGE_MODIFIE
    assert fenetre.bouton_exporter.isEnabled() is True


def test_site_s5_exige_le_coefficient_geotechnique(fenetre):
    _remplir(fenetre)
    formulaire = fenetre.formulaire
    formulaire.classe_site.setCurrentIndex(formulaire.classe_site.findData(ClasseSite.S5))
    assert formulaire.coef_site.isEnabled() is True

    fenetre.calculer()
    assert fenetre.etat.objectName() == "etatErreur"
    assert fenetre.etat.text() == "Les valeurs saisies sont erronées : S"
    assert formulaire.coef_site.property("invalide") is True

    formulaire.coef_site.setValue(1.6)
    assert formulaire.coef_site.property("invalide") is False
    fenetre.calculer()
    assert fenetre.etat.objectName() == "etatSucces"


def test_classe_de_construction_affiche_son_libelle(fenetre):
    libelles = [
        fenetre.formulaire.classe.itemText(i)
        for i in range(fenetre.formulaire.classe.count())
    ]
    assert libelles == ["Classe I", "Classe II", "Classe III"]
    assert ClasseConstruction.CLASSE_I.libelle == "Classe I"


def test_calcul_active_export_et_remplit_les_widgets(fenetre):
    _remplir(fenetre)
    fenetre.calculer()

    valeurs = [
        widget.text()
        for widget in fenetre.resultats.findChildren(QLabel)
        if widget.objectName() in ("valeur", "valeurFinale")
    ]
    assert fenetre.bouton_exporter.isEnabled() is True
    assert FX_ATTENDU in valeurs
    assert any(v != "—" for v in valeurs), "les résultats doivent être des widgets remplis"


def test_bouton_note_de_calcul_ouvre_la_fenetre(fenetre):
    from interface.note import FenetreNote

    assert fenetre.bouton_exporter.text() == "Note de calcul"
    _remplir(fenetre)
    fenetre.calculer()

    dialogue = FenetreNote(fenetre.note_de_calcul())
    assert dialogue.windowTitle() == "Note de calcul"
    assert dialogue.texte.isReadOnly() is True
    assert dialogue.texte.toPlainText() == fenetre.note_de_calcul()
    dialogue.close()


def test_note_de_calcul_porte_la_date_du_calcul(fenetre):
    from datetime import datetime

    _remplir(fenetre)
    fenetre.calculer()
    lignes = fenetre.note_de_calcul().split("\n")
    assert lignes[4].startswith("Calcul réalisé le ")
    horodatage = datetime.strptime(lignes[4].removeprefix("Calcul réalisé le "), "%d/%m/%Y à %H:%M:%S")
    assert abs((datetime.now() - horodatage).total_seconds()) < 300


def test_S_suit_la_classe_de_site(fenetre):
    formulaire = fenetre.formulaire
    for site, attendu in ((ClasseSite.S1, 1.0), (ClasseSite.S2, 1.2),
                          (ClasseSite.S3, 1.4), (ClasseSite.S4, 1.8)):
        formulaire.classe_site.setCurrentIndex(formulaire.classe_site.findData(site))
        assert formulaire.coef_site.value() == pytest.approx(attendu)
        assert formulaire.coef_site.isEnabled() is False

    formulaire.classe_site.setCurrentIndex(formulaire.classe_site.findData(ClasseSite.S5))
    assert formulaire.coef_site.value() == 0.0
    assert formulaire.coef_site.isEnabled() is True


def test_reinitialiser_efface_les_resultats_et_restaure_l_accueil(fenetre):
    _remplir(fenetre)
    fenetre.calculer()
    fenetre.reinitialiser()

    assert fenetre.note_de_calcul() is None
    assert fenetre.bouton_exporter.isEnabled() is False
    assert fenetre.etat.objectName() == "etat"
    assert fenetre.etat.text() == module_fenetre.MESSAGE_ETAT
    for champ in fenetre.formulaire._champs:
        assert champ.property("invalide") is False
    for widget in fenetre.resultats.findChildren(QLabel):
        if widget.objectName() in ("valeur", "valeurFinale"):
            assert widget.text() == "—"


def test_resultats_sans_les_donnees_entree(fenetre):
    _remplir(fenetre)
    fenetre.calculer()

    titres = [
        groupe.title()
        for groupe in fenetre.resultats.findChildren(QGroupBox)
    ]
    assert titres == ["Paramètres RPS", "Direction X", "Direction Y"]
    assert not any("entrée" in titre.lower() for titre in titres)

    entetes = {
        widget.text()
        for widget in fenetre.resultats.findChildren(QLabel)
        if widget.objectName() == "enteteTableau"
    }
    assert entetes == {"Symbole", "Désignation", "Valeur", "Unité"}
    assert "Source" not in entetes


def test_champs_a_largeur_fixe(fenetre):
    for champ in fenetre.formulaire.findChildren(QComboBox):
        assert champ.width() > 0
    assert fenetre.formulaire.classe.width() == 180
    assert fenetre.formulaire.hauteur.width() == 115


def test_export_ecrit_la_note_de_calcul(fenetre, tmp_path, monkeypatch):
    _remplir(fenetre)
    fenetre.calculer()
    cible = tmp_path / "note.txt"

    class FauxDialogue:
        @staticmethod
        def getSaveFileName(*args, **kwargs):
            return str(cible), ""

    monkeypatch.setattr(module_fenetre, "QFileDialog", FauxDialogue)
    fenetre.exporter()

    assert Path(cible).read_text(encoding="utf-8") == fenetre.note_de_calcul()
    assert cible.name in fenetre.etat.text()


def test_export_ajoute_lextension_txt(fenetre, tmp_path, monkeypatch):
    _remplir(fenetre)
    fenetre.calculer()
    cible = tmp_path / "note"

    class FauxDialogue:
        @staticmethod
        def getSaveFileName(*args, **kwargs):
            return str(cible), ""

    monkeypatch.setattr(module_fenetre, "QFileDialog", FauxDialogue)
    fenetre.exporter()
    assert Path(f"{cible}.txt").exists()


def test_export_annule_ffeut_un_avertissement(fenetre, monkeypatch):
    _remplir(fenetre)
    fenetre.calculer()

    class FauxDialogue:
        @staticmethod
        def getSaveFileName(*args, **kwargs):
            return "", ""

    monkeypatch.setattr(module_fenetre, "QFileDialog", FauxDialogue)
    fenetre.exporter()

    assert fenetre.etat.objectName() == "etatAlerte"
    assert "annulé" in fenetre.etat.text()


def test_avertissement_du_domaine_arrive_dans_la_barre_detat(fenetre):
    """Un WARNING du domaine est relayé par le journal jusqu'à la barre d'état."""
    logging.getLogger(module_journal.DOMINE).warning("Coefficient interpolé")
    assert fenetre.etat.objectName() == "etatAlerte"
    assert "interpolé" in fenetre.etat.text()


def test_journal_trace_les_interactions(fenetre):
    fenetre.formulaire.poids_x.setValue(1500.0)
    contenu = module_journal.FICHIER.read_text(encoding="utf-8")
    assert "Session ouverte" in contenu
    assert "Saisie" in contenu
    assert "1 500" in contenu or "1500" in contenu


def test_formule_rendue_en_latex_ou_repli(application):
    etiquette = etiquette_formule()
    assert etiquette.pixmap() is not None or etiquette.text() != ""
