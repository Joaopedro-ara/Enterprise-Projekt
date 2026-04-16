from db_Mitarbeiter import Datenbank
from openpyxl import Workbook

class produktion:
    def __init__(self):
        self.db=Datenbank()
        self.cursor=self.db.cursor

    def Produktions_Masch_pruefen(self,maschinen_id):
        #prüfen ob die Maschinen_Id existiert
        sql="Select Maschinen_id from prod_Maschinen where Maschinen_id =%s" # hier suche ich die Artikelnummer
        self.cursor.execute(sql,(maschinen_id,)) # hier fürhre ich die anfrage aus
        return self.cursor.fetchone() is not None # hier geben wir die artikeln nummer zurück

    def Maschine_anlegen(self,maschinen_id,bezeichnung,kategorie,Letze_warnung,naechste_wartung,Produktions_ort,
                         halle,status):
        #hier in diese funktion wird die maschine informatione an die datenbank angelegt
        if self.Produktions_Masch_pruefen(maschinen_id): # prüfen ob Artikel schon existirt
            return False # Artikel existiert schon
        else:
            sql=("Insert into prod_Maschinen(Maschinen_id,Bezeichnung,Kategorie,"
                 "Letze_Wartung,Naechste_wartung,Produktions_Ort,Halle,Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
            values=(maschinen_id,bezeichnung,kategorie,Letze_warnung,naechste_wartung,Produktions_ort,
                         halle,status)
            self.cursor.execute(sql,values)
            self.db.connection.commit()
            return "Produkte wurden erfolgreich im Lager hinzugefügt"

    def maschinen_abrufen(self):
        sql=("Select Maschinen_id,Bezeichnung,Kategorie,Letze_Wartung,Naechste_wartung,"
             "Produktions_Ort,Halle,Status from prod_maschinen ")
        self.cursor.execute(sql)
        daten=self.cursor.fetchall()
        return daten
    def status_aendern(self,maschinen_id,neuer_status):
        if not self.Produktions_Masch_pruefen(maschinen_id):
            return "Maschine wurde nicht gefuden"
        else:
            sql="Update prod_Maschinen Set Status=%s where Maschinen_id=%s"
            self.cursor.execute(sql,(neuer_status,maschinen_id))#neue status und maschine id diensen als platzhalter
            self.db.connection.commit()
            return "Update Status erfolgreich"




