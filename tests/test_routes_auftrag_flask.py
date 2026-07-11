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
