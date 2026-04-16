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
        elif Status==("Störung"):
            zufal=random.randint(1,100)
            if zufal<=10:
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



    #zufaelig=random.randint(1,100)
    #if zufaelig < 5:
         #maschinen=prod.maschinen_abrufen()
         #if maschinen:
             #opfer=random.choice(maschinen) #hier wählen wir eine zufällige maschine
             #opfern_id=opfer[0]#Maschinend id ist das erste index im Tupel
             #prod.status_aendern(opfern_id,"Defekt") # hier setzen wir den status auf opfer um

    #aktuele_daten=prod.maschinen_abrufen() # hoeön der Aktuelen daten aus den Maschinen abrufen
    #manschinen_pake=[] # hier machen wir die Maschinnen informationen rein
    #for maschinen in aktuele_daten: # hier geht die For_schleife durch die Aktuelnen daten:
        #maschinen_dict={
           #"maschinen_id": maschinen[0],
            #"Bezeichnung": maschinen[1],
            #"Produktions_ort":maschinen[5],
           # "Halle":maschinen[6],
           # "Status": maschinen[7]

        #}
        #manschinen_pake.append(maschinen_dict)
    #return jsonify(manschinen_pake)

