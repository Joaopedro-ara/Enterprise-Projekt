from titanflow_enterprise.Mitarbeiter.Produktions_manager import produktion
from unittest.mock import patch,MagicMock


#Positever test für die def maschne anlegen
@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_anlegen_erfolgreich(mock_db_klasse):
    #none weil es als erste prüft obe eine maschine schon angelegt wurde
    #mit none denkt das prograqm maschine wurde nicht angelegt also kann ich sie anlegen
    mock_db_klasse.return_value.cursor.fetchone.return_value=None
    manager=produktion()
    ergebnis=manager.Maschine_anlegen("Db-002","Müllfraser","Müllanlage","22.04.2026",
                                      "22.08.2026","Leipzig","2","Aktiv")
    assert ergebnis =="Produkte wurden erfolgreich im Lager hinzugefügt"
    mock_db_klasse.return_value.connection.commit.assert_called_once()

#negativer test für die maschine das heißt die maschine extiert schon
@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_anlegen_existert_schon(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchone.return_value=("Test-Maschine",)
    manager=produktion()
    ergenis=manager.Maschine_anlegen("Db-001","Qualitäts-Maschine","Qualität",
                                     "22.05.2026,","22.09.2026","Leipzig",
                                     "2","Aktiv")
    assert ergenis is False


@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_aufrufen_erfolgreich(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchall.return_value=("Test-maschine",)
    manager=produktion()
    ergebnis=manager.maschinen_abrufen()
    assert ergebnis==("Test-maschine",)
@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_aufrufen_nichtErfolgreich(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchall.return_value=None
    manager=produktion()
    ergebnis=manager.maschinen_abrufen()
    assert ergebnis==None


@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_aufrufen_nichtErfolgreich_real(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchall.return_value = []
    manager = produktion()
    ergebnis = manager.maschinen_abrufen()
    assert ergebnis ==[]

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_aufrufen_db_fehler(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchall.side_effect = Exception("DB Fehler")
    manager = produktion()

    try:
        manager.maschinen_abrufen()
        assert False   # sollte nie erreicht werden
    except Exception as e:
        assert str(e) == "DB Fehler"

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_status_aendern_erfolgreich(mock_db_klasse):
     mock_db_klasse.return_value.cursor.fetchall.return_value=("Test-001",)
     manager=produktion()
     ergebnis=manager.status_aendern("Db-001","Aktiv")
     assert ergebnis =="Update Status erfolgreich"




@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_status_ändern_nicht_erfolgreich(mock_db_klasse):
    with patch.object(produktion,"Produktions_Masch_pruefen",return_value=False):
        manager=produktion()
        ergebnis=manager.status_aendern("DB-001","Wartung")
        assert ergebnis == "Maschine wurde nicht gefuden"

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_zufalls_fehler_aufrufen_erfolreich(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchone.return_value=("F001","Störung der daten",1)
    manager=produktion()
    ergebnis=manager.zufalls_fehler_abrufen()
    assert ergebnis==("F001","Störung der daten",1)

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_zufalls_fehler_aufrufen_nicht_erfolgreich(mock_db_klasse):
    mock_db_klasse.return_value.cursor.fetchone.return_value=None
    manager=produktion()
    ergebnis=manager.zufalls_fehler_abrufen()
    assert ergebnis is None
@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_log_eintragr_erfolgreich(mock_db_klasse):
    mock_db=mock_db_klasse.return_value
    mock_db.cursor=MagicMock()
    mock_db.connection=MagicMock()
    manager=produktion()
    manager.logbuch_eintrag_abschliessen("DB-001")
    # Prüfe, dass execute mit einem Tupel (maschinen_id,) aufgerufen wurde
    called_sql,called_vals=mock_db.cursor.execute.call_args[0]
    assert "Update maschinen_logbuch" in called_sql
    assert "DB-001" in called_vals
    # Prüfe, dass commit aufgerufen wurde
    mock_db.connection.commit.assert_called_once()

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_log_eintrag_nicht_erfolgreich(mock_db_klasse):
    mock_db=mock_db_klasse.return_value
    mock_db.cursor=MagicMock()
    mock_db.connection=MagicMock()
    #Simulation db-fehler
    mock_db.cursor.execute.side_effect=Exception("DB-Kaputt")
    manager=produktion()
    try:
        manager.logbuch_eintrag_abschliessen("DB-001")
        assert False  # sollte nicht passeiren
    except Exception as e:
        assert "DB-Kaputt" in str(e)
    mock_db.connection.commit.assert_not_called()


@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschine_existiert(mock_db_klasse):
    # 1. Den mock programieren(zuweisung)
    # Wichtig: Übergeben eines Tuppels mit koma!
    mock_db_klasse.return_value.cursor.fetchone.return_value=("TD-002",)
    #2 Den manger aufrufen
    manager = produktion()
    #3. Ergebnisfunktion ausführen
    ergebnis=manager.Produktions_Masch_pruefen("TD-002")
    #4. Die behauptung aufstellen
    assert ergebnis is True

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
#Testen mit falschen wert
def test_maschine_existiert_nicht(mock_db_klasse):
#1. den Mock für Hacker-fall-programieren(kein ergebnis=none)
    mock_db_klasse.return_value.cursor.fetchone.return_value=None
    #2 den Manger aufrufen
    manager=produktion()
    ergebnis=manager.Produktions_Masch_pruefen("Reperatur-004")
    assert ergebnis is False

#Wir testen hier das try except error
@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschineerror_faengt_abstuzt_ab(mock_db_klasse):
    #mit .side-effect sabotieren wir das und machen ein echten fehler sodas es diese Excepiton kommt
    mock_db_klasse.return_value.cursor.execute.side_effect=Exception("Simulierter Datenbank-Brand!")
    manager=produktion()
    ergebnis=manager.maschineerroer("Db-001","Hand wurde in den sichehrheitsbreich angelegt","3")
    assert ergebnis is None # hier machen wir immer none
    mock_db_klasse.return_value.connection.commit.assert_not_called()

@patch('titanflow_enterprise.Mitarbeiter.Produktions_manager.Datenbank')
def test_maschineerror_faengt_absturturtz_nicht_ab(mock_db_klasse):
    mock_db_klasse.return_value.cursor.execute.side_effect=Exception("Datenbank kaputt")
    manager=produktion()
    ergebnis=manager.maschineerroer("Db-001","Hand wurde in den sichehrheitsbreich angelegt","3")
    assert ergebnis is None
    mock_db_klasse.return_value.connection.commit.assert_not_called()


