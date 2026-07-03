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

    #hier wird die definition sein für das MRP-Algorithmus (Material Requirements Planning)
    def bruttobedarf_berechnen(self,kundenauftrag_id):
        try:
            sql=("Select Produkt_id,MENGE from Kunden_auftraege where Kundenauftrag_id=%s ")
            self.cursor.execute(sql,(kundenauftrag_id,))
            auftrag=self.cursor.fetchone()
            #prüfen ob es ein auftrag gibt
            if auftrag is None:
                return "Kein Auftrag gefunden"
            produkt_id=auftrag[0]
            menge=auftrag[1]
            #Stueckliste_laden
            stuekliste=self.stueckliste_fuer_produkt_abrufen(produkt_id)
            #leres dict erstellen:
            gesamter_bedarf={}
            #for schleife die das rezept holt
            for eintrag in stuekliste:
                # # Material-ID und benötigte Menge aus dem aktuellen Stücklisteneintrag auslese
                zutat_id=eintrag[1] #Matreial:id aus der Stücliste= Untergeordnet_Material_ID
                rezept_menge=eintrag[2] # benötigte menge aus den  Menge_benoetigt
                gesamt_benoetigt=rezept_menge*menge # wie viel matrial ein produkt benötigt * menge den der kunde bestellt hat
                gesamter_bedarf[zutat_id]=gesamt_benoetigt
            return gesamter_bedarf

        except Exception as e:
            self.db.connection.rollback()
            return f"Fehler beim Einfügen der Daten: {e}"

    #verfübarprüfen
    def verfuegbarkeit_pruefen(self,kundenauftrag_id):
        try:
            # Schritt 1: Bruttobedarf berechnen
            bedarf_dict = self.bruttobedarf_berechnen(kundenauftrag_id)
            # Prüfen, ob beim Berechnen des Bruttobedarfs ein Fehler aufgetreten ist
            if isinstance(bedarf_dict, str):  # mit isinstnca prüfen ob die variable zu ein String gehört.
                return bedarf_dict
            pruef_bericht = []  # gibt später an das frontent weiter die werte
            for material_id, benoetigte_menge in bedarf_dict.items():
                sql = ("Select Material_bezeichnung,Bestand_Aktuell From Materials_lager where Material_id=%s")
                self.cursor.execute(sql, (material_id,))
                ergebnis = self.cursor.fetchone()
                bezeichnung = ergebnis[0]
                aktueller_bestand = ergebnis[1]
                # Algorithmus  logik die Diferenz  zuzschen aktuelne_bestand und benötigte menge
                differenz = aktueller_bestand - benoetigte_menge
                if differenz < 0:
                    status = "Kritsich 🔴"
                    fehlmenge = abs(differenz)
                if differenz >= 0:
                    status = "Ausreichend ✅"
                    fehlmenge =0

                # Dictonary um den bericht zuschreiben
                material_bericht = {
                    "Material-ID": material_id,
                    "Bezeichnung": bezeichnung,
                    "Bedarf": benoetigte_menge,
                    "Lagerbestand": aktueller_bestand,
                    "Fehlmenge": fehlmenge,
                    "Status": status,
                }
                pruef_bericht.append(material_bericht)
            return pruef_bericht

        except Exception as e:
            self.db.connection.rollback()
            return f"Fehler beim Einfügen der Daten: {e}"






