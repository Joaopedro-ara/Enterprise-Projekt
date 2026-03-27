from Produktions_manager import produktion
from datetime import datetime
from decimal import Decimal
while True:
    print("Wähle eins von den punkte: ")
    print("1: Maschine Anlegen")
    print("2: Maschinen Abrufen")
    print("3: Neuer status aendern")
    print ("4 Benden")
    auswahl=input("Welche von den 3 Punkte wählst du ?")
    if auswahl=="1":
        print("Maschinen eintragen")
        n=int(input("Bitte wähle wie aus wie viele einträge machen wollen ?:"))
        c=0
        produkt = produktion()
        while c<n:
            maschineni_id=input("Name der Maschine: ")
            beze = input("Bezeichnung der Maschine: ")
            kategorie = input("Maschinen Kategorie: ")
            baujahr = int(input("baujahr der Maschine: "))
            Ansch_kosteb=Decimal(input("Anschafungskosten der Maschine:"))
            Restwert=Decimal(input("Restwert  der Maschine: "))
            letze_wartung=input("Letze Wartung:")
            letzte_wartung = datetime.strptime(letze_wartung, "%d.%m.%Y")
            Naete_wartung=input("Wan ist die nächste wartung: ")
            naetch_wartung = datetime.strptime(Naete_wartung, "%d.%m.%Y")
            prodt_ort=input("In Welchen produktionsort ist die Maschine: ")
            halle=input("In welche Halle/Abteilung ist die maschine: ")
            status=input("Wie ist der status der Maschine(Aktiv/Wartung/Defekt/Abgeschaltet): ")
            produkt.Maschine_anlegen(maschineni_id,beze,kategorie,baujahr,Ansch_kosteb,Restwert,letzte_wartung,naetch_wartung,
                                 prodt_ort,halle,status)
            c+=1
    elif auswahl=="2":
        produkt=produktion()
        meine_maschinen=produkt.maschinen_abrufen()
        for zeile in meine_maschinen:
            print(zeile)

    elif auswahl=="3":
        print("Status der maschine Ändern")
        maschinen_id=input("Gib die Maschinen_id an:")
        neuer_status=input("Neuer Status: ")
        pro=produktion()
        pro.status_aendern(maschinen_id,neuer_status)

    elif auswahl=="4":
        break
    else:
        print("Nur zahlen eingeben")



