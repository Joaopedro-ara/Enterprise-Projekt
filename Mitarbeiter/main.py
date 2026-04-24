from titanflow_enterprise.Mitarbeiter.use_case import usermanger
from titanflow_enterprise.Mitarbeiter.Lager_manager import Lagermanger
from datetime import datetime

while True:
    print("Wähle option:")
    print("1 Registrieren")
    print("2 Anmelden")
    print("3 Maschine log")
    print("4 Benden")
    auswahl=input("Wähle 1- 4 Punkte aus: ")
    try:
        if auswahl =="1":
            user_manger=usermanger()
            user_manger.Mitarbeiter_registrieren()
        elif auswahl =="2":
            user_manger=usermanger()
            rolle=user_manger.login()
            if rolle:
                print(f" Anmeldung ist erfolgreich deine rolle {rolle}")
                while True:
                        print("1 Bestand anzeigen lassen")
                        print("2:Artikel Anlegen")
                        print("3: bestand in excel transferieren")
                        print("4: Bestand ändern")
                        print("5: Bestand Warnung aufprüfen")
                        print("6:Lagerwert ")
                        print("7: testlog")
                        print("8: Benden")
                        auswahl = input("Welcher der punkte 1-7 wählst du ")
                        lager=Lagermanger()

                        if auswahl=="1":
                            if rolle=="Lagerarbeiter" or rolle=="Sichtleiter" or rolle=="Lagermanager":
                                meine_artikel=lager.bestand_anzeigen_data()
                                for zeile in meine_artikel:
                                    print(zeile)
                        elif auswahl=="2":
                            if rolle=="Sichtleiter" or rolle=="Lagermanager":

                                print("Bitte geben sie die Artiekl ein")
                                arktl_num=input("Artikelnummer eingeben: ")
                                bez= input("Bezeichnung des Artikels eingeben: ")
                                kaz = input(" Die Kategorie des Artikels eingeben: ")
                                meng=int(input("Menge des Artikels eingeben: "))
                                Einheit=input("Welche einheit hat das Lager kg..: ")
                                preis=float(input("Wie ist der preis des Artikels: "))
                                ort=input("Welche Lagerort ist der Artiekl gelagert")
                                lager.Artikel_anlegen(arktl_num,bez,kaz,meng,Einheit,preis,ort)



                            else:
                                print("Sie haben Kein zugang für weitere dienste , für weitere Informationen melden sich "
                                      "an den Vorgesetzen")
                        elif auswahl=="3":
                            if rolle == "Sichtleiter" or rolle == "Lagermanager":
                                print("foldende punkte sind da :Alle,nach kategorie und nach Lagerort")
                                auswahl=input("Wähle aus welche exel datei haben möchtest: ")
                                if auswahl=="alle":
                                    lager.bestand_abrufen_excel("alle")
                                if auswahl=="nach kaetegorie":
                                    kat=input("Welche Kategiorie soll gefiltert werden?")
                                    lager.bestand_abrufen_excel("gefiltert",kategorie=kat)
                                if auswahl=="nach Lagerort":
                                    lag=input("Welcher Lagerort soll gefiltert werden?")
                                    lager.bestand_abrufen_excel("gefiltert",lagerort=lag)

                            else:
                                print("Sie haben Kein zugang für weitere dienste , für weitere Informationen melden sich "
                                      "an den Vorgesetzen")
                        elif auswahl=="4":
                            if rolle == "Sichtleiter" or rolle == "Lagermanager":
                                print("Bitte geben sie die Artiekl ein")
                                arktl_num = input("Artikelnummer eingeben: ")
                                menge=int(input("Wie viele menge ist dazu gekommen"))
                                lager.bestand_andern(arktl_num,diferenz=menge)


                            else:
                                print("Sie haben Kein zugang für weitere dienste , für weitere Informationen melden sich "
                                      "an den Vorgesetzen")
                        elif auswahl=="5":
                            if rolle == "Sichtleiter" or rolle == "Lagermanager":
                                au=int(input("Welche ist der kristische bestant nummer:"))
                                ergebnis=lager.bestand_warnung_abrufen(au)
                                print(ergebnis)

                            else:
                                print("Sie haben Kein zugang für weitere dienste , für weitere Informationen melden sich "
                                      "an den Vorgesetzen")
                        elif auswahl=="6":
                            if rolle == "Lagermanager" or rolle == "Einkauf" or rolle== "Lagercontroller":
                                berechnen=lager.lagerwert_berechnen()
                                print(berechnen)
                            else:
                                print("Sie haben Kein zugang für weitere dienste , für weitere Informationen melden sich "
                                      "an den Vorgesetzen")

                        elif auswahl=="7":
                            break
                        else:
                            print("Bitte nur zahlen eingeben")
        elif auswahl=="3":
            print("Maschine ein")
            maschine_id = input("maschinen id: ")
            fehlercode= input("fehlercode eingeben: ")
            info_fehler = input(" info eingeben: ")
            datum_str = input("Datum eingeben (YYYY-MM-DD HH:MM:SS): ")
            datum = datetime.strptime(datum_str, "%Y-%m-%d %H:%M:%S")
            Dauer= int(input("Dauer in min(dauer wie lange maschine stgehen gebliewbewn ist..: "))
            Status = input("Wie ist staurs: ")
            Dienstnummer= input("dienstnummer des mitarbeiters")
            prioritaet=int(input("Welche priorität hat es?: "))
            user_manger = usermanger()
            user_manger.maschinelog(maschine_id,fehlercode,info_fehler,datum, Dauer, Status, Dienstnummer, prioritaet)








        elif auswahl =="4":
            break
        else:
            print("Keine nummer ausgewählt")
    except Exception as e:
        print( f"Bitte nut zahlen eingeben {e}")

