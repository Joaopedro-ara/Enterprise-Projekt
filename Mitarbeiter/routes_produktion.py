#Hoier machen wir die Blueflask für die prodution damit wir später in der app.py benutzen können
from flask import Flask,render_template,request,redirect,url_for,session,send_file,Blueprint
#Ein blueprint ist ähnlich wie eine Mehrfachsteckdoese wo wir unseren viel stecker hinzufügen können
from Produktions_manager import produktion
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

