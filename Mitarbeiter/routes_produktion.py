#Hoier machen wir die Blueflask für die prodution damit wir später in der app.py benutzen können
from flask import Flask,render_template,request,redirect,url_for,session,send_file,Blueprint
#Ein blueprint ist ähnlich wie eine Mehrfachsteckdoese wo wir unseren viel stecker hinzufügen können
from use_case import usermanger
from Lager_manager import Lagermanger
produktion_bp=Blueprint('produktion',__name__)
@produktion_bp.route('/produktion_dashboard')
def prod_dash():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    else:
        return "Willkiomen in der produktionsebene"

