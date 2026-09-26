from rps import amplification


def test_facteur_amplification():
    assert amplification.facteur_amplification(zone_acceleration=1, zone_vitesse=1, T=0.25, direction="D").valeur == 2.5
    assert amplification.facteur_amplification(zone_acceleration=2, zone_vitesse=3, T=0.40, direction="D").valeur == 1.9
    assert amplification.facteur_amplification(zone_acceleration=4, zone_vitesse=3, T=0.42, direction="D").valeur == -6.40 * 0.42 + 5.1