from flask import Flask,render_template,request,redirect,url_for,session,send_file
from use_case import usermanger
from Lager_manager import Lagermanger
from routes_produktion import produktion_bp



app=Flask(__name__)
app.secret_key="Hilde-super-geheim-2026"
app.register_blueprint(produktion_bp)
manger=usermanger()
Lager=Lagermanger()


def format_euro(betrag):
    return f"{betrag:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@app.route('/')

def index():
    return render_template('index.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":
        Mitarbeiter_id=request.form['mitarbeiter_id']
        Mitarbeiter_vorname=request.form['vorname']
        Mitarbeiter_Nachname=request.form['nachname']
        Mitarbeiter_password=request.form['passwort']
        Mitarbeiter_rolle=request.form['rolle']
        Mitarbeiter_standort=request.form['standort']
        result=manger.registrireen_web(Mitarbeiter_id,Mitarbeiter_vorname,Mitarbeiter_Nachname,Mitarbeiter_password,Mitarbeiter_rolle
                                       ,Mitarbeiter_standort)
        if result=="Registrierung Erfolgreich":
            return redirect(url_for('index'))
        else:
            return result
    else:
        return render_template('register.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        Mitarbeiter_id=request.form['mitarbeiter_id']
        Mitarbeiter_password=request.form['password']
        result=manger.login_html(Mitarbeiter_id,Mitarbeiter_password)
        if result:
            session['nutzer_id']=Mitarbeiter_id
            session['rolle']=result
            return redirect(url_for('dashboards'))
        else:
            return "Password falsch oder Nutzer existiert nicht"
    return render_template('login.html')


@app.route("/lager",methods=['GET','POST'])
def lager_a():
    if 'nutzer_id' not in  session:
        return redirect(url_for('index'))
    aktuelle_rolle = session.get("rolle")
    produktion_rolle = ["Produktionsarbeiter", "Produktionsschichtleiter", "Produktionsleiter", "Werksleiter"]
    if aktuelle_rolle in produktion_rolle:
        return redirect(url_for('dashboards'))
    else:
        daten=Lager.bestand_abrzufen()
        return render_template('lager.html',bestandsliste=daten,nutzer_Rolle=session.get('rolle'))


@app.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route("/dashboard",methods=['GET','Post'])
def dashboards():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))

    return render_template('dashboard.html',nutzer_id=session['nutzer_id'],nutzer_Rolle=session.get('rolle'))

@app.route("/artikel_anlegen",methods=['GET','POST'])
def artikel_anlegen():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    if request.method == "GET": # wenn wir seite anzeigen lassen wollen
        return  render_template("artikel_anlegen.html")
    if request.method=="POST": # Daten speichern
        Artikelnumb=request.form['Artikelnummer']
        Bezeich=request.form['Bezeichnung']
        kat=request.form['Kategorie']
        Meng=int(request.form["Menge"])
        einheit=request.form["Einheit"]
        Preis=float(request.form["Preis"])
        lagerort=request.form["Lagerort"]
        Lager.Artikel_anlegen(Artikelnumb,Bezeich,kat,Meng,einheit,Preis,lagerort)
        return redirect(url_for('lager_a'))

@app.route("/bestand_aendern",methods=['GET','POST'])
def artikel_aendern():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    if request.method=="GET":
        return  render_template("bestand_aendern.html")
    if request.method=="POST":
        Artikelnumb = request.form['Artikelnummer']
        Meng = int(request.form["Menge"])
        Lager.bestand_andern(Artikelnumb,diferenz=Meng)
        return redirect(url_for('lager_a'))
@app.route("/warnung",methods=['GET','POST'])
def warnungen():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    if request.method=="GET":
        return render_template("warnung.html")
    if request.method=="POST":
        lim=int(request.form["limit"])
        kritische_daten=Lager.bestand_warnung_abrufen(lim)
        return render_template('lager.html',bestandsliste=kritische_daten,nutzer_Rolle=session.get('rolle'))

@app.route("/lagerwert",methods=['GET'])
def lagerwert():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    if request.method=="GET":
        gesamtwert=Lager.lagerwert_berechnen()
        gesamtwerte=format_euro(gesamtwert)
        werte_orte=[(ort,format_euro(wert))
        for ort,wert in Lager.lagerwert_pro_ort()]

        return render_template('lagerwert.html',wert=gesamtwerte,orte=werte_orte)

@app.route("/excel_export",methods=['GET','POST'])
def excel_export():
    if 'nutzer_id' not in session:
        return redirect(url_for('index'))
    if request.method=="GET":
        return render_template("export.html")
    if request.method=="POST":
        art=request.form['Export-Art']
        wert=request.form['filter_wert']
        if art=="alle":
            Lager.bestand_abrufen_excel("alle")
            return send_file("Alle_Bestaende.xlsx", as_attachment=True)
        elif art=="Kategorie":
            Lager.bestand_abrufen_excel("gefilter",kategorie=wert)
            return send_file("Alle_Bestande_nach_Kategorien.xlsx", as_attachment=True)

        elif art=="Lagerort":
            Lager.bestand_abrufen_excel("gefiltert",lagerort=wert)
            return send_file("Alle_Bestande_nach_Lagerort.xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run()