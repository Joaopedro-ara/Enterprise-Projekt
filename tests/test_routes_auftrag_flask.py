import unittest
from unittest.mock import patch,MagicMock
from flask import session,Flask
from titanflow_enterprise.Mitarbeiter.routes_auftrag import auftrag_bp,lager_bp
from titanflow_enterprise.Mitarbeiter.app2 import app

class TestRoutesAuftrag(unittest.TestCase):
    #Den Manger Mocken, der in routes_auftrag.py verwendet wird
    @patch('titanflow_enterprise.Mitarbeiter.routes_auftrag.auf')
    def setUp(self, mock_manager):
        self.mock_manager = mock_manager
        #kuonfiguration der App für das testing
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False # ausschalten des csrf schutz für tests
        #vietzuelen Browser
        self.client = app.test_client()

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

    #testfal2: mit falsche rolle
    def test_kunden_auftrage_falsche_rolle(self):
        #fake seesion vortäuschen falsche rolle
        with self.client.session_transaction() as sess:
            sess['nutzer_id']='123'
            sess['rolle']='Porduktionsarbeiter' # falsche rolle für die route
        response = self.client.get('/kunden_auftraege')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])

    #testfall3: richtige Rolle
    def test_rohmaterial_ansicht_erfolgreich(self):
        #fake seesion vortäuschen richtiger rolle
        with self.client.session_transaction() as sess:
            sess['nutzer_id']='123'
            sess['rolle']='Werksleiter'
        # Mock-manger sagen was er bei alle_materialen-aufrufen zurückgeben soll
        self.mock_manager.alle_rohmateriallen_abrufen.return_value = [("RM-01", "Stahl", 100, 50, "Stück", "Lager A")]
        response=self.client.get('/rohmaterial')
        self.assertEqual(response.status_code, 200) # ok muss sein das die Anfrtage erfolgreich ist
        self.assertIn('Rohmaterial Übersicht', response.get_data(as_text=True))
        #b für bytes







if __name__ == '__main__':
    unittest.main()


