#Hoier machen wir die Blueflask für die prodution damit wir später in der app.py benutzen können
import io

from flask import render_template,request,redirect,url_for,session, Blueprint,jsonify,send_file
#Ein blueprint ist ähnlich wie eine Mehrfachsteckdoese wo wir unseren viel stecker hinzufügen können
from titanflow_enterprise.Mitarbeiter.Produktions_manager import produktion
import random
import pandas as pd
from io import BytesIO
# io stellt speicher daten bereit und bytes um binärdaten direkt im Ram zu lesen

produktion_bp=Blueprint('produktion',__name__)
prod=produktion()
@produktion_bp.route('/produktion_dashboard')
def prod_dash():

    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    aktuelle_rolle = session.get("rolle")
    produktion_rolle = ["Produktionsarbeiter", "Produktionsschichtleiter", "Produktionsleiter", "Werksleiter"]
    if aktuelle_rolle not in produktion_rolle:
        return redirect(url_for('dashboards'))
    else:
        daten=prod.maschinen_abrufen()
        return render_template('Produktions_templates/Produktion_dashboard.html',bestandsliste=daten,nutzer_Rolle=session.get('rolle'))

@produktion_bp.route('/Maschine-anlegen', methods=["GET", "POST"])
def maschine_anlegen():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    if request.method=="GET":
        return render_template("Produktions_templates/Maschine-anlegen.html")
    if request.method=="POST":
        Maschinen_id=request.form["Maschinen-Id"]
        bezeichnung=request.form["Bezeichnung"]
        kat=request.form["Kategorie"]
        Letze_wartung=request.form["Letzewartung"]
        naechste_wartung = request.form["Naechstewartung"]
        prod_ort = request.form["Produktionsort"]
        halle = request.form["Halle"]
        status = request.form["Status"]
        prod.Maschine_anlegen(Maschinen_id,bezeichnung,kat,Letze_wartung,naechste_wartung,prod_ort,halle,status)
        return redirect(url_for('produktion.prod_dash'))
@produktion_bp.route("/api/maschinen_status")
#polter_geist
def api_maschinen_status():
    maschinen_liste=[] # Wor wir die Maschinen_ Informationen sopeichern
    aktuele_daten= prod.maschinen_abrufen() # hier werden die Aktuelnen dtaen der maschine aufgerufen
    maschinen_liste=aktuele_daten #hier geben wir direkt die Daten ein.
    #for schleifewo es durch jede maschine geht
    for maschine in maschinen_liste:
        maschinen_id=maschine[0]
        Status=maschine[7]
        if Status=="Aktiv":
            zufall=random.randint(1,100)
            if zufall <=5:
                prod.status_aendern( maschinen_id,"Störung")
                zufals_fehler=prod.zufalls_fehler_abrufen()
                fehlercode=zufals_fehler[0]
                info_text=zufals_fehler[1]
                prio=zufals_fehler[2]
                prod.logbuch_eintrag(maschinen_id,fehlercode,info_text,prio)
        elif Status=="Störung":
            zufall=random.randint(1,100)
            if zufall<=10:
                prod.status_aendern(maschinen_id, "Defekt")
                zufals_fehler = prod.zufalls_fehler_abrufen()
                fehlercode = zufals_fehler[0]
                info_text = zufals_fehler[1]
                prio = zufals_fehler[2]
                prod.logbuch_eintrag(maschinen_id, fehlercode, info_text, prio)
        elif Status=="Wartung":
            zufall=random.randint(1,100)
            if zufall<=20: #in jeden takt gibnbt es eine 20% chance, dass die wartung fertig ist
                prod.status_aendern(maschinen_id, "Testlauf")
        elif Status=="Testlauf":
            zufall=random.randint(1,100)
            if zufall <=70:
                prod.status_aendern(maschinen_id, "Aktiv")
                prod.logbuch_eintrag_abschliessen(maschinen_id)
            elif zufall >=71 and zufall<=85:
                prod.status_aendern(maschinen_id, "Störung")
            else:
                prod.status_aendern(maschinen_id, "Defekt")
    frische_daten=prod.maschinen_abrufen()
    maschinen_pake=[]
    for maschinene in frische_daten:
        maschinen_dict={
            "maschinen_id":maschinene[0],
            "Status":maschinene[7]
        }
        maschinen_pake.append(maschinen_dict)
    return jsonify(maschinen_pake)

#Neue Route um die reparier button zu betetigen und die Maschine zu Reparieren manuell
#und auch diue datenbank zu ändern auf den statu defekt zu repariert
@produktion_bp.route('/api/reparieren/<maschinen_id>',methods=["POST"])
def reparieren(maschinen_id):
    prod.status_aendern( maschinen_id,"Wartung") #hier wird der status auf Warung verändert
    if not maschinen_id:
        return jsonify({"status":"fehler"}),400
    return jsonify({"status":"erfolg"})
@produktion_bp.route('/api/maschinen_logbuch',methods=["GET","POST"])
def maschinen_fehler_eintraege():
    # die  Rollenschutz
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    aktuelle_rolle = session.get("rolle")
    produktion_rolle = ["Produktionsschichtleiter", "Produktionsleiter", "Werksleiter"]
    if aktuelle_rolle not in produktion_rolle:
        return redirect(url_for('dashboards'))
    else:
        logs=prod.alle_logs_abrufen() # daten holen und speichern
    return render_template('Produktions_templates/maschinen_logbuch.html',logs=logs)

@produktion_bp.route('/api/maschinen_logbuch/export',methods=["GET","POST"])
def maschinen_logbuch_export():
    #Rollenschutz gewähren
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    aktuelle_rolle=session.get("rolle")
    produktions_rolle=["Produktionsschichtleiter", "Produktionsleiter", "Werksleiter"]
    if aktuelle_rolle not in produktions_rolle:
        return redirect(url_for('dashboards'))
    else:
        log=prod.alle_logs_abrufen() # hier speichen wir die funktion ind die  variable log
        ## als nächste machen wir eine pd-datframe datei wo wir den log variable übergeben
        #und damit pandas die colums weißt geben wir die colums pandas wo wir die sachen abspeichern die atribute in den colums
        df=pd.DataFrame(log,
                        columns=["Log-ID","Maschinen-ID","Fehler_code","Info_fehler","Datum","Dauer_in_Min","Status",
                                "Mitarbeiter","Priorität"])
        excsel_speicher=io.BytesIO() #hier senden wir die dateien direk in den browser das heißt date in Ram
        df.to_excel(excsel_speicher,index=False)# index =false damit pandas nicht ungefragt mit forlaufende nummer links einfügt
        excsel_speicher.seek(0)
        # .seek(0) setzt den Dateizeiger wieder an den Anfang, damit die Datei vollständig gelesen werden kann
    return  send_file(excsel_speicher,mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                      as_attachment=True,download_name="maschinen_fehler_historie.xlsx")
#return send file ans den ram  mit minetype=... ,sagen wir das es um eine excsel datei handelt mit den ofziellen excel wert
#mit as_attachment=true sagen wir das er die datei downloaddet mit den dateiname=maschnen...


#Apri route für den bar chart
@produktion_bp.route('/api/maschinen_logbuch/chart_daten', methods=["GET","POST"])
def chart_daten():
    # Rollenschutz gewähren
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    aktuelle_rolle = session.get("rolle")
    produktions_rolle = ["Produktionsschichtleiter", "Produktionsleiter", "Werksleiter"]
    if aktuelle_rolle not in produktions_rolle:
        return redirect(url_for('dashboards'))
    else:
        roh_daten=prod.excse_barcharts_maschine_logbuch()
        maschinen_ids=[]
        ausfall_anzahl=[]
        for daten in roh_daten:
            maschine=daten[0]
            ausfall=daten[1]
            maschinen_ids.append(maschine)
            ausfall_anzahl.append(ausfall)

        chart_paket = {
            "Maschinen_id": maschinen_ids,
            "Ausfall": ausfall_anzahl
        }
    return jsonify(chart_paket)

