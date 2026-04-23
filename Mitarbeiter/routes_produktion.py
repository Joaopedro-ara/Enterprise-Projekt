#Hoier machen wir die Blueflask für die prodution damit wir später in der app.py benutzen können
from flask import Flask,render_template,request,redirect,url_for,session,send_file,Blueprint,jsonify
#Ein blueprint ist ähnlich wie eine Mehrfachsteckdoese wo wir unseren viel stecker hinzufügen können
from Produktions_manager import produktion
import random

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
        elif Status=="Störung":
            zufall=random.randint(1,100)
            if zufall<=10:
                prod.status_aendern(maschinen_id, "Defekt")
        elif Status=="Wartung":
            zufall=random.randint(1,100)
            if zufall<=20: #in jeden takt gibnbt es eine 20% chance, dass die wartung fertig ist
                prod.status_aendern(maschinen_id, "Testlauf")
        elif Status=="Testlauf":
            zufall=random.randint(1,100)
            if zufall <=70:
                prod.status_aendern(maschinen_id, "Aktiv")
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



