from flask import Flask
from titanflow_enterprise.Mitarbeiter.app2 import app
from unittest.mock import patch,MagicMock
from titanflow_enterprise.Mitarbeiter.use_case import usermanger
# hier im patch kommt das Ojekt mocking wo es benutzt wird und nicht wie es definiert
#patch weie eine digitaler spion mit eine pfad post adresse wo er ein stund double ersetzen soll
@patch('titanflow_enterprise.Mitarbeiter.routes_produktion.prod.cursor')
# hier im patch kommt das Ojekt mocking wo es benutzt wird und nicht wie es definiert
#patch weie eine digitaler spion mit eine pfad post adresse wo er ein stund double ersetzen soll
def test_chart_daten_api_erfolgreich(mock_cursor):
    client=app.test_client() #viertuelen browser-client indem man app.test_client() hinzufügt
    #Flask cliehnt aufbaeun um die session zu manipolieren,so dass wir trotzdem reimnkommen
    with client.session_transaction() as sess:
        sess["nutzer_id"]=999
        sess["rolle"]="Werksleiter"
    mock_cursor.fetchall.return_value = [("Maschine-A", 5), ("Maschine-B", 2)]
    #Wirteulen browser loschicken
    antwort=client.get('/api/maschinen_logbuch/chart_daten')
    assert antwort.status_code==200 #behauptung das die route erfolgreich antwortet
    daten=antwort.get_json() # json inhalt  behauputung das diese keys in der klammern existieren
    assert daten["Maschinen_id"]==["Maschine-A","Maschine-B"] # hier kommt der name aus den chart paket
    assert daten["Ausfall"]==[5,2]