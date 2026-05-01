import mysql.connector
import os

class Datenbank:
    def __init__(self):
        try:
            db_pass = os.environ.get('DB_PASSWORD')
            self.connection=mysql.connector.connect(
                host="localhost",
                user="root",
                passwd=db_pass,
                database="firma_intern"
            )
            self.cursor=self.connection.cursor()
            print("DB Verbindung steht ")
        except mysql.connector.Error as err:
            raise RuntimeError("Datenbankverbindung fehlgeschlagen") from err

    def tabelle_erstellen(self):
        try:
            self.cursor.execute("Create Table if not exists Employers(ID int auto_increment Primary key,"
                                "Dienstnummer Varchar(255) Unique,"
                                "Vorname Text,"
                                "Nachname Text,"
                                "Passwort Blob Not Null,"
                                "Rolle Varchar(255),"
                                "Standort Varchar (255))")
            self.cursor.execute(" Create table if not exists Lagerbestand(Id Int auto_increment Primary key,"
                               "Artikelnummer Varchar(255) Unique,"
                               "Bezeichnung Text,"
                               "Kategorie Varchar(255),"
                               "Menge Int,"
                               "Einheit Varchar(255),"
                               "Preis Decimal(10,2),"
                               "Lagerort Varchar(255))")
            self.cursor.execute("Create Table if not exists prod_Maschinen(ID Int auto_increment Primary key,"
                                "Maschinen_id Varchar(255) Unique,"
                                "Bezeichnung Varchar(255),"
                                "Kategorie Varchar(255),"
                                "Baujahr int,"
                                "Anschaffungskosten Decimal(10,2),"
                                "Restwert Decimal(10,2),"
                                "Letze_wartung Date,"
                                "Naechste_wartung Date,"
                                "Produktions_Ort Varchar(255),"
                                "Halle Varchar(255),"
                                "Status Varchar(255))")
            self.cursor.execute("Create Table if not exists maschinen_logbuch(Log_id Int auto_increment Primary key,"
                                "Maschinen_id Varchar(255) ,"
                                "Fehlercode Varchar(255),"
                                "Info_Fehler Text,"
                                "Datum Datetime," # Wann ist der fehler Passeirt
                                "Dauer_in_min Integer," # Wie lange dauert der Ausdfall der Maschine
                                "Status Varchar(255)," # Wie ist der Status der maschine reperatur: 1: offen,2:In beaberitung,3: gelöst 
                                "Dienstnummer Varchar(255)," #Welche Mitarbeiter es bearbeitet hat
                                "Prioritaet Integer," # hier 1:Wichtig,2: Milltel 3:Nicht so wichtigg 
                                "FOREIGN KEY(Maschinen_id) References prod_Maschinen(Maschinen_id),"
                                "FOREIGN KEY(Dienstnummer) References Employers(Dienstnummer))")
            self.cursor.execute("Create Table if not exists fehler_katalog(Fehler_ID Int auto_increment Primary key,"
                                "Fehlercode text,"
                                "Infor_Text Varchar(255),"
                                "Priorität Integer(20))")
            self.connection.commit()
            print("Tabelle wurde erfolgreich hergestellt")
        except Exception as e:
            print(f"Fehler bei  der Datenbank herstellung {e}")
    def close(self):

        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Verbindung wurde getrent ")

db=Datenbank()
db.tabelle_erstellen()
db.close()



