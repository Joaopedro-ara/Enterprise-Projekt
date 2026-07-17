import unittest
from unittest.mock import patch,MagicMock
from flask import session,Flask
from titanflow_enterprise.Mitarbeiter.routes_auftrag import auftrag_bp,lager_bp,auf
from titanflow_enterprise.Mitarbeiter.app2 import app

class TestRoutesAuftrag(unittest.TestCase):
    #Den Manger Mocken, der in routes_auftrag.py verwendet wird
    def setUp(self):
        # 1. Patcher definieren
        self.patcher = patch('titanflow_enterprise.Mitarbeiter.routes_auftrag.auf')
        # 2. Patcher manuell STARTEN und den Mock speichern
        self.mock_manager = self.patcher.start()
        #kuonfiguration der App für das testing
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False # ausschalten des csrf schutz für tests
        #virtueller Browser
        self.client = app.test_client()
    def tearDown(self):
        # Nach jedem Test den Mock wieder stoppen
        self.patcher.stop()


    #test security rollen
    # hier testen wir in den ersten testfall den zugriff ohne login

    def test_kundenauftraege_ohne_login(self):
        #test clienbt route
        response=self.client.get('/kunden_auftraege')
        #Server prüfen mit einen redisrat und code status 302 antwortet(302 bedeutet das der server
        # den browser auf einen anderen url leitet vorübergehend.
        self.assertEqual(response.status_code, 302)
        #prpüfen ob es wirklich zum login umgeletet wird
        self.assertIn('/',response.headers['Location'])

    #testen zugriff ohne login bei rohmaterial


    #testfal2: mit falsche rolle
    def test_kunden_auftrage_falsche_rolle(self):
        #fake seesion vortäuschen falsche rolle
        with self.client.session_transaction() as sess:
            sess['nutzer_id']='123'
            sess['rolle']='Porduktionsarbeiter' # falsche rolle für die route
        response = self.client.get('/kunden_auftraege')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])


    def test_kunden_auftrag_get_erfolgreich(self):
        with self.client.session_transaction() as sess:
            sess['nutzer_id'] = '123'
            sess['rolle'] = 'Werksleiter'
        self.mock_manager.alles_auftraege_anzeigen.return_value=["KA-001","Kunde A"]
        response = self.client.get('/kunden_auftraege')
        self.assertEqual(response.status_code, 200)
        self.mock_manager.alles_auftraege_anzeigen.assert_called_once()
        self.assertIn("Kundenaufträge Übersicht",response.get_data(as_text=True))
#testfall mit kunden_auftrag get =neu
    def test_kunden_auftrag_get_neu_erfolgreich(self):
        with self.client.session_transaction() as sess:
            sess['nutzer_id'] = '123'
            sess['rolle'] = 'Werksleiter'

        response = self.client.get('/kunden_auftraege?aktion=neu')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Kundenaufträge anlegen", response.get_data(as_text=True))
#testfall mit den post
    def test_kunden_auftrag_post_erfolgreich(self):
        #fake session herstellen.
        with self.client.session_transaction() as sess:
            sess['nutzer_id'] = '123'
            sess['rolle'] = 'Werksleiter'
        #Rückgabewerte des manages festlegen:
        self.mock_manager.kundenauftrag_anlegen.return_value = ("Daten erfolgreich in die Tabelle eingefügt")
        self.mock_manager.alles_auftraege_anzeigen.return_value = []
        #post-Anfrage senden
        response=self.client.post("/kunden_auftraege",data={
            "kundenauftrag_id":"KA-001",
            "kunde_name":"BM",
            "produkt_id":"P-001",
            "menge": "100",
            "liefertermin": "2026-08-01",
            "prioritaet": "A",
            "status": "Eingegangen",
            "werk_id": "W-01",
            "ersteelungsdatum": "2026-07-17"})
        #Antwort prüfen
        self.assertEqual(response.status_code, 200)
        # Prüfen, ob der Manager mit den richtigen Daten aufgerufen wurde
        self.mock_manager.kundenauftrag_anlegen.assert_called_once_with( "KA-001","BM","P-001",
        "100","2026-08-01","A","Eingegangen","W-01","2026-07-17")
        #prüfen, ob danach die Auftragsübersicht neu gleaden wurden
        self.mock_manager.alles_auftraege_anzeigen.assert_called_once()
        #prüfen, ob die übersicht angezeigt wird
        self.assertIn("Kundenaufträge Übersicht",response.get_data(as_text=True))

    def test_kunden_aftrag_post_nicht_erfolgreich(self):
        def test_kunden_auftrag_post_datenbankfehler(self):
            # Fake-Session
            with self.client.session_transaction() as sess:
                sess['nutzer_id'] = '123'
                sess['rolle'] = 'Werksleiter'

            # Manager soll eine Exception werfen
            self.mock_manager.kundenauftrag_anlegen.side_effect = Exception("DB Fehler")

            # POST-Anfrage
            response = self.client.post("/kunden_auftraege", data={
                "kundenauftrag_id": "KA-001",
                "kunde_name": "BM",
                "produkt_id": "P-001",
                "menge": "100",
                "liefertermin": "2026-08-01",
                "prioritaet": "A",
                "status": "Eingegangen",
                "werk_id": "W-01",
                "ersteelungsdatum": "2026-07-17"
            })

            # Prüfen, dass der Manager aufgerufen wurde
            self.mock_manager.kundenauftrag_anlegen.assert_called_once()

            # ein 500-Fehler
            self.assertEqual(response.status_code, 500)

    #testfall für  rohmaterial ohne login
    def test_rohmaterial_ansicht_ohne_login(self):
        response=self.client.get("/rohmaterial")
        self.assertEqual(response.status_code,302)
        self.assertIn('/',response.headers['Location'])

    def test_rohmaterail_uebersicht_falsche_rolle(self):
        # fake seesion vortäuschen falsche rolle
        with self.client.session_transaction() as sess:
            sess['nutzer_id'] = '123'
            sess['rolle'] = 'Porduktionsarbeiter'  # falsche rolle für die route
        response = self.client.get('/rohmaterial')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])


    #testfall: richtige Rolle get rohmaterial
    def test_rohmaterial_ansicht_erfolgreich(self):
        #fake seesion vortäuschen richtiger rolle
        with self.client.session_transaction() as sess:
            sess['nutzer_id']='123'
            sess['rolle']='Werksleiter'
        # Mock-manger sagen was er bei alle_materialen-aufrufen zurückgeben soll
        self.mock_manager.alle_rohmateriallen_abrufen.return_value = [("RM-01", "Stahl", 100, 50, "Stück", "Lager A")]
        response=self.client.get('/rohmaterial')
        self.assertEqual(response.status_code, 200) # ok muss sein das die Anfrtage erfolgreich ist
        self.assertIn('Rohmaterial anlegen', response.get_data(as_text=True))

    # testfall mit rohmaterial_uebersicht get=neu
    def test_Rohmaterial_ansicht_get_neu_erfolgreich(self):
        with self.client.session_transaction() as sess:
            sess['nutzer_id'] = '123'
            sess['rolle'] = 'Werksleiter'

        response = self.client.get('/rohmaterial?aktion=neu')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Rohmaterial anlegen", response.get_data(as_text=True))

    #testfall Rohmaterial anlgegen post erfolgreich
    def test_rohmaterial_anlegen_erfolgreich(self):
        with self.client.session_transaction() as sess:
            sess['nutzer_id'] = '123'
            sess['rolle'] = 'Werksleiter'
            # Rückgabewerte des manages festlegen:
            self.mock_manager.kundenauftrag_anlegen.return_value = ("Daten erfolgreich in die Tabelle eingefügt")
            self.mock_manager.alles_auftraege_anzeigen.return_value = []


        #b für bytes
    #testfall 3  post method
    def test_mrp_pruefung_post(self):
        #fake session erstellen:
        with self.client.session_transaction() as sess:
            sess['nutzer_id']='123'
            sess['rolle']='Werksleiter'
        self.mock_manager.verfuegbarkeit_pruefen.return_value = [{"Material-ID": "RM-01", "Status": "Ausreichend"}]
        self.mock_manager.alles_auftraege_anzeigen.return_value = []
        response = self.client.post('/auftrag/mrp_pruefung', data={'auftrags_id': 'KA-001'})
        self.assertEqual(response.status_code, 200)
        self.mock_manager.verfuegbarkeit_pruefen.assert_called_once_with('KA-001')




if __name__ == '__main__':
    unittest.main()


