#unut -test für aufrags_manager
# erste Funktion def kundenauftrag_anlegen hir wollen wir den ersten testfall machen :
#test fall 1 <: Funktion bekommt die richtige daten
import unittest
from unittest.mock import patch, MagicMock
from titanflow_enterprise.Mitarbeiter.auftrags_manager import AuftragsManager

class TestAuftragsManager(unittest.TestCase):
    #Ersetzen der Dtaenbank durch ein dummy
    @patch('titanflow_enterprise.Mitarbeiter.auftrags_manager.Datenbank')
    def setUp(self,mock_db_class):

        #vorbereiten des dummys
        self.mock_db_instance=mock_db_class.return_value
        self.mock_cursor=self.mock_db_instance.cursor
        #staten den manager mit de Dummy_datenbank
        self.manager=AuftragsManager()
        #Überschreibten die Atribute  des Mangener mit den Mock
        self.manager.db=self.mock_db_instance
        self.manager.cursor=self.mock_cursor


    def test_kundenauftrag_anlegen_erfolg(self):
        ergebnis=self.manager.kundenauftrag_anlegen("KA-001","Siemens","P-100",
                                                    "19","10-10-2026","A","Eingegangen",
                                                    "Werk-1","07.07.2026")
        #prüfen  ob
        self.assertEqual(ergebnis,"Daten erfolgreich in die Tabelle eingefügt")
        #prüfen ob die methode den ausführ-Befehl an die datenbank geschickt  wurde
        self.mock_cursor.execute.assert_called_once()
        #prüfen, ob es gepeichert ist
        self.mock_db_instance.connection.commit.assert_called_once()

    #testen das die Db failed
    def test_kundenauftrag_fehler(self):
        self.mock_cursor.execute.side_effect=Exception("DB Offline")
        ergebnis = self.manager.kundenauftrag_anlegen("KA-001", "Siemens", "P-100",
                                                      "19", "10-10-2026", "A", "Eingegangen",
                                                      "Werk-1", "07.07.2026")
        self.mock_db_instance.connection.rollback.assert_called_once()
        self.assertEqual(ergebnis,"Fehler beim Einfügen der Daten: DB Offline")

    #testen ob der leere daten beim abrufen
    def test_alles_auftrauege_anzeigen_leer(self):
        self.mock_cursor.fetchall.return_value=[]
        ergebnis=self.manager.alles_auftraege_anzeigen()
        self.assertEqual(ergebnis,[])
        #testen ob daten vorhanden sind
    def test_alle_auftraege_anzeigen_daten_voll(self):
        auftraege=[("KA-001","Siemens","P-100","19","10-10-2026","A","Eingegangen","Werk-1","07.07.2026")]
        self.mock_cursor.fetchall.return_value=auftraege
        #funktion ausfuehren
        ergebnis=self.manager.alles_auftraege_anzeigen()
        #prüfen , ob die daten richtig zurücgegeben werden
        self.assertEqual(ergebnis,auftraege)
        #prüfen . onb select  aus geführt wurde
        self.mock_cursor.execute.assert_called_once_with("Select *From Kunden_auftraege")
        self.mock_cursor.fetchall.assert_called_once()

    def test_rohmaterial_anlegen_erfolg(self):
        ergebnis=self.manager.rohmaterial_anlegen("DP_11","Stahlrohre","20"
                                                  ,"10","Stück","Bremen")
        self.assertEqual(ergebnis," Daten erfolgreich in die tabelle eingefügt")
        # prüfen ob die methode den ausführ-Befehl an die datenbank geschickt  wurde
        self.mock_cursor.execute.assert_called_once()
        # prüfen, ob es gepeichert ist
        self.mock_db_instance.connection.commit.assert_called_once()

    def test_rohmaterial_anlegen_nicht_erfolg(self):
        self.mock_cursor.execute.side_effect = Exception("DB Offline")
        ergebnis = self.manager.rohmaterial_anlegen("DP_11", "Stahlrohre", "20"
                                                    , "10", "Stück", "Bremen")
        self.mock_db_instance.connection.rollback.assert_called_once()
        self.assertEqual(ergebnis, "Fehler beim Einfügen der Daten: DB Offline")

    def test_alle_rohmaterial_anzeigen_leer(self):
        self.mock_cursor.fetchall.return_value = []
        ergebnis = self.manager.alle_rohmateriallen_abrufen()
        self.assertEqual(ergebnis, [])

    def test_alle_rohmatrial_anzeigen_voll(self):
        auftraege = [("DP_11", "Stahlrohre", "20", "10", "Stück", "Bremen")]
        self.mock_cursor.fetchall.return_value = auftraege
        # funktion ausfuehren
        ergebnis = self.manager.alle_rohmateriallen_abrufen()
        # prüfen , ob die daten richtig zurücgegeben werden
        self.assertEqual(ergebnis, auftraege)
        # prüfen . onb select  aus geführt wurde
        self.mock_cursor.execute.assert_called_once_with("Select *From Materials_lager")
        self.mock_cursor.fetchall.assert_called_once()

    def test_stucklisten_position_anlegen_erfolgreich(self):
        ergebnis=self.manager.stuecklisten_position_anlegen("DF_001","DSFGH001","10")
        self.assertEqual(ergebnis, " Daten erfolgreich in die tabelle eingefügt")
        # prüfen ob die methode den ausführ-Befehl an die datenbank geschickt  wurde
        self.mock_cursor.execute.assert_called_once()
        # prüfen, ob es gepeichert ist
        self.mock_db_instance.connection.commit.assert_called_once()
    def test_stuecklisten_position_anlegen_nicht_erfolgreich(self):
        self.mock_cursor.execute.side_effect = Exception("DB Offline")
        ergebnis = self.manager.stuecklisten_position_anlegen("DF_001", "DSFGH001", "10")
        self.mock_db_instance.connection.rollback.assert_called_once()
        self.assertEqual(ergebnis, "Fehler beim Einfügen der Daten: DB Offline")

    def test_stuecklisten_anzeigen_leer(self):
        self.mock_cursor.fetchall.return_value = []
        ergebnis = self.manager.stueckliste_fuer_produkt_abrufen("P-100")
        self.assertEqual(ergebnis, [])
    def test_stuecklisten_anzeigen_vorhanden(self):
        auftraege = [("P-100", "M-001", 5)]
        self.mock_cursor.fetchall.return_value = auftraege
        # funktion ausfuehren
        ergebnis = self.manager.stueckliste_fuer_produkt_abrufen("P-100")
        # prüfen , ob die daten richtig zurücgegeben werden
        self.assertEqual(ergebnis, auftraege)
        # prüfen . onb select  aus geführt wurde
        self.mock_cursor.execute.assert_called_once()
        self.mock_cursor.fetchall.assert_called_once()

    #bruttobedarf_berechnen testen

    #test 1 Auftrag existiert nict
    def test_bruttobedarf_kein_auftrag(self):
        self.mock_cursor.fetchone.return_value=None
        ergenmis=self.manager.bruttobedarf_berechnen("KA-001")
        self.assertEqual(ergenmis,"Kein Auftrag gefunden")

    #test2 aufr´trag existiert und stück berechnen
    def test_bruttobedarf_berechnen_erfolg(self):
        self.mock_cursor.fetchone.return_value=("P-100",10)
        self.manager.stueckliste_fuer_produkt_abrufen=MagicMock(return_value=[("P-100","RM-01",5)])
        ergebnis=self.manager.bruttobedarf_berechnen("KA-001")
        self.assertEqual(ergebnis,{"RM-01":50})

    def  test_brutto_bedarf_leere_stueckliste(self):
        self.mock_cursor.fetchone.return_value = ("P-100", 10)
        self.manager.stueckliste_fuer_produkt_abrufen = MagicMock(return_value=[])
        ergebnis = self.manager.bruttobedarf_berechnen("KA-001")
        self.assertEqual(ergebnis,{})
    #datenbankfehler testen
    def test_bruttobadraf_datenbankfehler(self):
        self.mock_cursor.execute.side_effect = Exception("DB Offline")
        ergebnis = self.manager.bruttobedarf_berechnen("KA-001")
        self.mock_db_instance.connection.rollback.assert_called_once()
        self.assertEqual(ergebnis,"Fehler beim Einfügen der Daten: DB Offline")

    def test_verfuegbarpruefen_ausreuchen(self): #bestand ausreichend testen
        self.manager.bruttobedarf_berechnen=MagicMock(return_value={"RM-01":50})
        self.mock_cursor.fetchone.return_value=("Stahltraeger",100)
        ergebnis=self.manager.verfuegbarkeit_pruefen("KA-001")
        erwartet=[{
            "Material-ID": "RM-01", "Bezeichnung": "Stahltraeger", "Bedarf": 50,
            "Lagerbestand": 100, "Fehlmenge": 0, "Status": "Ausreichend ✅"
        }]
        self.assertEqual(ergebnis, erwartet)

    def test_verfuegbarpruefen_kristisch(self):  # bestand ausreichend testen
        self.manager.bruttobedarf_berechnen = MagicMock(return_value={"RM-01": 110})
        self.mock_cursor.fetchone.return_value = ("Stahltraeger", 100)
        ergebnis = self.manager.verfuegbarkeit_pruefen("KA-001")
        erwartet = [{
            "Material-ID": "RM-01", "Bezeichnung": "Stahltraeger", "Bedarf": 110,
            "Lagerbestand": 100, "Fehlmenge": 10, "Status": "Kritsich 🔴"
        }]
        self.assertEqual(ergebnis, erwartet)

    def test_verfuegbarkeit_pruefen_auftrag_fehler(self): # kein auftrag gefunden testen
        self.manager.bruttobedarf_berechnen = MagicMock(return_value="Kein Auftrag gefunden")
        ergebnis = self.manager.verfuegbarkeit_pruefen("KA-001")
        self.assertEqual(ergebnis, "Kein Auftrag gefunden")
        self.mock_cursor.execute.assert_not_called()

    def test_verfuegbarkeit_pruefen_fehler_db(self):
        # Arrange
        self.manager.bruttobedarf_berechnen = MagicMock(return_value={"RM-01": 50})
        self.mock_cursor.execute.side_effect = Exception("DB Offline")
        ergebnis = self.manager.verfuegbarkeit_pruefen("KA-001")
        self.mock_db_instance.connection.rollback.assert_called_once()
        self.assertEqual(ergebnis,"Fehler beim Einfügen der Daten: DB Offline")















if __name__ == '__main__':
    unittest.main()



