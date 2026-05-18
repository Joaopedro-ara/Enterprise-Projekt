from titanflow_enterprise.Mitarbeiter.db_Mitarbeiter import Datenbank
from datetime import datetime

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

    def zufalls_fehler_abrufen(self):
        sql="Select Fehlercode,Infor_Text,Priorität From fehler_katalog ORDER BY  RAND() LIMIT 1"
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    def logbuch_eintrag(self,maschinen_id,fehlercode,info_text,prio):
       #hier ist die Funktion um die werte in den Maschinen logbuch einzutragen
       sql=("Insert into maschinen_logbuch (Maschinen_id,Fehlercode,Info_Fehler,Datum,Dauer_in_min,Status,Dienstnummer,"
            "Prioritaet) Values (%s,%s,%s,%s,%s,%s,%s,%s)" )
       status = "offen"
       datum = datetime.now()
       dauer_min = 0
       dienstnummer = None
       val=(maschinen_id,fehlercode,info_text,datum,dauer_min,status,dienstnummer,prio)
       self.cursor.execute(sql,val)
       self.db.connection.commit()

    def maschineerroer(self,fehlercode,info_text,prioritaet):
        #Hier ist die funktion wo wir
        try:
            sql=("Insert into fehler_katalog(Fehlercode,Infor_text,Priorität) VALUES (%s,%s,%s)")
            val=(fehlercode,info_text,prioritaet)
            self.cursor.execute(sql,val)
            self.db.connection.commit()
            return "Fehlereientag wurde erfolgreich in die Datenbank aufgenommen"
        except Exception as e:
            print("Fehler beim Insert:", e)
    def logbuch_eintrag_abschliessen(self,maschinen_id):
        # Findet das offene Ticket der Maschine und setzt den Status von 'offen' auf 'gelöst'.
        sql= ("Update maschinen_logbuch "
              "Set status='Gelöst' "
              "Where maschinen_id=%s "
              "AND Status='offen'")
        self.cursor.execute(sql,(maschinen_id))
        #führt den sql befehl aus und {suche den platzhalte:maschine--id und ersterte den wert der phxthon variable maschinen_id}
        #sql = "WHERE maschinen_id = :maschinen_id" ->cursor.execute(sql, {"maschinen_id": maschinen_id})

        self.db.connection.commit()










