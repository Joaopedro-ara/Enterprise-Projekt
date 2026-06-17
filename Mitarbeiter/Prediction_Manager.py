import pandas as pd
from sklearn.linear_model import LinearRegression
from titanflow_enterprise.Mitarbeiter.db_Mitarbeiter import Datenbank
from titanflow_enterprise.Mitarbeiter.Produktions_manager import produktion
from titanflow_enterprise.Mitarbeiter.routes_produktion import produktion_bp

class Prediction:
    def __init__(self):
        self.db=Datenbank()
        self.cursor =self.db.cursor

    def prediction_maschine_gelöst(self):
        sql =("Select Prioritaet, Dauer_in_min from maschinen_logbuch where status='Gelöst'")
        self.cursor.execute(sql)
        daten=self.cursor.fetchall()
        df=pd.DataFrame(daten,columns=["Prioritaet", "Dauer_in_min"])
        X=df[["Prioritaet"]] # Features
        Y=df["Dauer_in_min"] #zielwert
        model=LinearRegression()
        model.fit(X,Y)
        gesuchte_prio=1
        eingabe =pd.DataFrame([[gesuchte_prio]],columns=["Prioritaet"])
        vorhersage=model.predict(eingabe)
        return vorhersage
prediction=Prediction()
vorhersage=prediction.prediction_maschine_gelöst()
print(f"Geschätzte Reparaturdauer: {vorhersage[0]:.2f} Minuten")

#Erste Version der ML-Vorhersage.
# Geplant sind weitere Optimierungen mit zusätzlichen Features,
# umfangreicheren Trainingsdaten und leistungsfähigeren Machine-Learning-Modellen.