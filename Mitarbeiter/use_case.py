from titanflow_enterprise.Mitarbeiter.db_Mitarbeiter import Datenbank
import bcrypt
print("Willkomen im TitanEnterprise Menü")

class usermanger:
    #verbindung herstellen zu der datenbank firma intern
    def __init__(self):
        self.db=Datenbank()
        self.cursor = self.db.cursor

    def dienstnummer_pruefen(self,Dienstnummer):
        #hier wollen wir pruefen ob die dienstnummer schon existiert
        sql="Select Dienstnummer from  Employers where Dienstnummer =%s"
        self.cursor.execute(sql,(Dienstnummer,))
        return self.cursor.fetchone()

    def Mitarbeiter_registrieren(self):
        print("\n Bitter hier Registriene mit Dienstnummer,Name,Vorname,und einen Password.")
        while True:
            Dienstnummer=input("Wie ist Ihre Dienstnummer: ")
            if self.dienstnummer_pruefen(Dienstnummer):
                print("Die Dienstnummer gibt es schon. Bitte enbtwerde Anmelden oder neue anfordern !")
            else:
                print("Ihre Dienstnummer ist verfügbar!")
                break
        while True:
            print("/N Bitte wählen sie >in passwort mit eine Zahl,und einen Großbuchstabe der länge 5")
            passwort=input("Welches Passwort wählen sie: ")
            if len(passwort)<5:
                print("Bitte geben sie mindesten 5 zeichen ein")
                continue
            elif not any(c.isdigit() for c in passwort):
                print("Bitte mindesten eine zahl hinzufügen")
                continue
            elif not any(c.isupper() for c in passwort):
                print("Bitte Mindesten ein großbuschtabe einfügen")
                continue
            elif not any(c.islower() for c in passwort):
                print("Bitte mindestens ein kleinbuchstabe hinzufüggen")
                continue
            else:
                print("password wurde erfolgreich eingeben")
                break
        password_hash = bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt())
        vorname=input("Wie ist ihrer Vorname: ")
        nachname=input("Wie ist Ihrer Nachname: ")
        rolle=input("Iwe ist Ihrer Rolle des Unternehmens: ")
        sql="Insert into Employers(Dienstnummer,Vorname,Nachname,Passwort,Rolle) values (%s,%s,%s,%s,%s)"
        value=(Dienstnummer,vorname,nachname,password_hash,rolle)
        self.cursor.execute(sql,value)
        self.db.connection.commit()
        print("Registrierung erfolgreich gespeichert!")
    def login(self):
        print("\n Bitte geben sie Ihre Dienstnummer und Ihren passwort ein")
        dienst=input("Bitte geben sie Ihre Dienstnummer ein:")
        password=input("Bette geben sie Ihren passwort ein: ")
        sql= "Select Passwort,Rolle from Employers where Dienstnummer=%s"
        #prüfen ob die Dienstnummer gibt
        self.cursor.execute(sql,(dienst,))
        ergebnis=self.cursor.fetchone()
        if ergebnis is None:
            print("Die  von Ihrnen geschreiben Dinestnummer gibt es nicht ")
            return False
        gespeicherter_hash, rolle = ergebnis
        if bcrypt.checkpw(password.encode('utf-8'), gespeicherter_hash):
            print(f"Login erfolgreich! Herzlich wilkommen {dienst} ihre Rolle ist {rolle}")
            return rolle
        else:
            print("Passwort falsch:")
            return False

    def registrireen_web(self,dienstnummer,vorname,nachname,password,rolle,standort):
        #prüfen ob der user schon existiert:
        if self.dienstnummer_pruefen(dienstnummer):
            return "Diese Dienstnummer existiert schon"
        #paswordprüfen
        if len(password)<6:
            return "pass password muss mindestens 6 zeichen haben"
        password_hash=bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
        #in die Datenbankj speichen
        sql="Insert into Employers(Dienstnummer,Vorname,Nachname,Passwort,Rolle,Standort) values(%s,%s,%s,%s,%s,%s)"
        val=(dienstnummer,vorname,nachname,password_hash,rolle,standort)
        self.cursor.execute(sql,val)
        self.db.connection.commit()
        return "Registrierung Erfolgreich"

    def login_html(self,dienstnummer,password):
        sql="Select Passwort,Dienstnummer,Rolle from Employers where Dienstnummer=%s"
        self.cursor.execute(sql,(dienstnummer,))
        ergebnis=self.cursor.fetchone()
        if ergebnis is None:
            return False
        gespeichter_hash,Dienstnummer,rolle=ergebnis
        if bcrypt.checkpw(password.encode('utf-8'), gespeichter_hash):
            return rolle
        else:
            return False

    def maschinelog(self,maschinen_id,fehlercode,info_fehler,datum,Dauer,Status,Dienstnummer,prioritaet):
        try:
            sql=("Insert into  maschinen_logbuch(Maschinen_id,Fehlercode,Info_Fehler,Datum,Dauer_in_min,Status,Dienstnummer,Prioritaet )"
             "values(%s,%s,%s,%s,%s,%s,%s,%s)")
            val=(maschinen_id,fehlercode,info_fehler,datum,Dauer,Status,Dienstnummer,prioritaet)
            self.cursor.execute(sql,val)
            self.db.connection.commit()
            return "Eintrag erfolgrreich ins Maschine logbuch"
        except Exception as e:
            print("❌ Fehler beim Insert:", e)














