from Produktions_manager import produktion


def test_maschine_existiert():
    manager = produktion()
    ergebnis=manager.Produktions_Masch_pruefen("TD-002")
    assert ergebnis is True