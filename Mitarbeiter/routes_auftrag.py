import io

from flask import render_template,request,redirect,url_for,session, Blueprint,jsonify,send_file
from titanflow_enterprise.Mitarbeiter.auftrags_manager import AuftragsManager

import random
import pandas as pd
import mysql.connector
auftrag_bp=Blueprint('auftrag',__name__)
auf=AuftragsManager()

@auftrag_bp.route('/kunden_auftraege', methods=["GET", "POST"])
def auftrag_anlegen():
    #Rollen schutz
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    aktuelle_rolle = session.get("rolle")
    produktion_rolle = ["Produktionsleiter", "Werksleiter"]
    if aktuelle_rolle not in produktion_rolle:
        return redirect(url_for('dashboards'))
    if request.method=="GET":
        daten=auf.alles_auftraege_anzeigen()
        return render_template('auftraege/kunden_auftraege.html',auftraege=daten)
    if request.method=="POST":
        try:
            k_id=request.form.get('kundenauftrag_id')
            k_name=request.form.get('kunde_name')
            p_id=request.form.get('produkt_id')
            meng=request.form.get('menge')
            liefer_ter=request.form.get('liefertermin')
            prio=request.form.get('priorität')
            status=request.form.get('status')
            werk_id=request.form.get('werk_id')
            datum=request.form.get('ersteelungsdatum')
            ergebnis=auf.kundenauftrag_anlegen(k_id,k_name,p_id,meng,liefer_ter,prio,status,werk_id,datum)
            daten=auf.alles_auftraege_anzeigen()
            return render_template('auftraege/kunden_auftraege.html',meldung=ergebnis,auftraege=daten)
        except Exception as e:
            print(f" datenbank fehler {e}")
