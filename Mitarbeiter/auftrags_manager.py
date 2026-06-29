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

    def rohmaterial_anlegen(self,material_id,material_bezeichnung,bestand,mindestbestand,typ,lagerort):
        try:
            sql=("Insert into Materials_lager(Material_id,Material_bezeichnung,Bestand_Aktuell,"
                 "Mindestbestand,Typ,lagerort) values(%s,%s,%s,%s,%s,%s)")
            values=(material_id,material_bezeichnung,bestand,mindestbestand,typ,lagerort)
            self.cursor.execute(sql,values)
            self.db.connection.commit()
            return " Daten erfolgreich in die tabelle eingefügt"
        except Exception as e:
            self.db.connection.rollback()
            return f"Fehler beim Einfügen der Daten: {e}"

    def alle_rohmateriallen_abrufen(self):
        sql=("Select *From Materials_lager")
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #Funktion um zu speichern wie viele Ein produkt von welche menge material es braucht
    def stuecklisten_position_anlegen(self,pordukt_id,material_id,menge):
        try:
            sql=("Insert Into BOM_Stueckliste(Uebergeordnet_Produkt_Id,Untergeordnet_Material_ID,Menge_benoetigt)"
                 "values(%s,%s,%s)")
            val=(pordukt_id,material_id,menge)
            self.cursor.execute(sql,val)
            self.db.connection.commit()
            return " Daten erfolgreich in die tabelle eingefügt"
        except Exception as e:
            self.db.connection.rollback()
        return f"Fehler beim Einfügen der Daten: {e}"
    # Abrufen der informationen von der mysql tabelle
    def stueckliste_fuer_produkt_abrufen(self,produkt_id):
        sql= ("Select Uebergeordnet_Produkt_Id,Untergeordnet_Material_ID,Menge_benoetigt From BOM_Stueckliste "
              "Join  Materials_lager  on Untergeordnet_Material_ID=Material_id Where Uebergeordnet_Produkt_Id= %s")
        #Der Sql befehl wählt für ein bestimtes produkt(uebergeordnetet_produkt_id) alle in der Stückliste enthaltende Materialen
        #sowie auch die jeweils benötigte menge aus und verküpft sie mit der Materialtabelle.
        self.cursor.execute(sql,(produkt_id,))
        #übergibt die Produkt_id and die Sql-Abfrage und führt sie sicher in die datenbank aus.
        return self.cursor.fetchall()
