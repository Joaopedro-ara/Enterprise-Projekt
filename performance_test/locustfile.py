from locust import HttpUser,task,between
#HtppUser = Die Basisklasse für die virtuelen Benutzer
#task= Ein dekurasotionset @task, mit dem wir den Locust sagen: Das hier ist eine Aktion
#between = Das werkzeug für die relaistsichen pausen

class TitanFlowAnsturnm(HttpUser):
    #vierutele classe setzen mit wait_tme _>  damit wartet jeder virteule mitarbeiter zufällig zwischen 1 und 3 sekunden
    wait_time = between(1,3)
    #--------------
    # hier schreiben wir die Funktionen auf des ap2.py
    #jede funktionen muss ein self entgegenehmen und ein @task darüberstehen haben
    @task(1)
    def dashboard_aufrufen(self):
        self.client.get("/dashboard")

    @task(3)
    def chart_ap_stressen(self):
        self.client.get('/api/maschinen_logbuch/chart_daten')
