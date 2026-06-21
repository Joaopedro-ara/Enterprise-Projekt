import io

from flask import render_template,request,redirect,url_for,session, Blueprint,jsonify,send_file
import random
import pandas as pd
import mysql.connector
from titanflow_enterprise.Mitarbeiter.db_Mitarbeiter import Datenbank

class AuftragsManager:
    def __init__(self):
        self.db=Datenbank()
        self.cursor =self.db.cursor

    def kundenauftrag_anlegen(self,kundenauftrag_id,kunde_name,produkt_id,menge,liefertermin,prioritaet,status,
                              werk_id,ersteelungsdatum):
        try:
            sql=("Insert into Kunden_auftraege(Kundenauftrag_id,Kunde_Name,Produkt_id,MENGE,Liefertermin,"
                 "Priorität,Status,werk_id,Erstellungsdatum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            val=(kundenauftrag_id,kunde_name,produkt_id,menge,liefertermin,prioritaet,status,werk_id,ersteelungsdatum)
            self.cursor.execute(sql,val)
            self.db.connection.commit()
            return "Daten erfolgreich in die Tabelle eingefügt"
        except Exception as e:
            self.db.connection.rollback()  # macht änderung rückgängig
            return f"Fehler beim Einfügen der Daten: {e}"

    def alles_auftraege_anzeigen(self):
        sql=("Select *From Kunden_auftraege")
        self.cursor.execute(sql)
        return self.cursor.fetchall()