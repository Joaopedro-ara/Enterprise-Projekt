# G-INOS – Global Integrated Neural Operating System 

G-INOS ist ein hochmodernes, modulares Enterprise Resource Planning (ERP) System und Produktionsplanungs- und -steuerungssystem (PPS), entwickelt auf Basis von **Python**, **Flask** und **MySQL**. Das System ist speziell für die verarbeitende Industrie (Hilde AG) konzipiert und implementiert eine strikte rollenbasierte Zugriffskontrolle (RBAC) für maximale Betriebssicherheit.

---

##  Aktueller Entwicklungsstand & Features

Das System befindet sich in der aktiven Entwicklung und deckt bereits die zentralen operativen Säulen eines modernen Industriebetriebs ab:

### 1.  Personal- & Sicherheitsmanagement (`Employers`)
* Sichere Benutzerregistrierung und verschlüsseltes Login-Verfahren.
* Rollenbasierter Zugriffsschutz (Werksleiter, Produktionsleiter, Produktionsschichtleiter, Produktionsarbeiter).

### 2.  Lager- & Bestandsmanagement (`Materials_lager` / `Lagerbestand`)
* Echtzeit-Verwaltung von Materialbeständen und Lagerorten.
* Automatisches Warnsystem bei Unterschreitung von Mindestbeständen.
* Finanzielle Bewertung von Lagerbeständen (Gesamtwert und pro Standort).
* Integrierter Excel-Export für administrative Audits.

### 3. ⚙️ Produktions- & Instandhaltungsmanagement (`prod_Maschinen` & Logbuch)
* Live-Überwachung des Maschinenstatus und zentrale Erfassung von Maschinenausfällen.
* **Intelligente Instandhaltungs-Simulation:** Dynamische Berechnung realistischer Reparaturzeiten gekoppelt an die Fehler-Priorität im System zur automatischen Generierung historischer Trainingsdaten.

### 4.  Kundenauftrags-Zentrale (`Kunden_auftraege`)
* Operative Neuanlage und strategische Steuerung von Kundenaufträgen.
* Automatisierte Zuweisung von Werk-IDs basierend auf der aktiven Benutzersitzung zur Verhinderung werksübergreifender Fehlbuchungen.

---

##  Feature-Teaser: Branch `Aufträge_prediction_manager`

Im aktuellen Entwicklungs-Branch **`Aufträge_prediction_manager`** treiben wir die digitale Transformation von G-INOS zur Industrie 4.0 voran. 

Hier wurde das Fundament für ein echtes **Predictive Maintenance Modul (Vorausschauende Instandhaltung)** gelegt:
* **Echtes Machine Learning im ERP:** Integration eines datenwissenschaftlichen Modells basierend auf **Pandas** und **Scikit-Learn**.
* **Lineare Regression (Linear Regression Modell):** Das System analysiert historische Logbucheinträge und lernt die mathematische Korrelation zwischen Fehler-Prioritäten und tatsächlichen Ausfallzeiten.
* **Prognose-Engine:** Das trainierte Modell berechnet für das Management vollautomatisch eine präzise Schätzung der voraussichtlichen Reparaturdauer zukünftiger Maschinenausfälle, um Stillstandszeiten in der Fabrik drastisch zu minimieren.

---

## 🛠️ Tech-Stack

* **Backend:** Python 3.x, Flask (Blueprints), MySQL Connector
* **Data Science & ML:** Pandas, Scikit-Learn (LinearRegression)
* **Frontend:** HTML5, CSS3 (Ergonomische, zweigeteilte Leitstands-Layouts), Jinja2 Templating
* **Security:** Flask-WTF (CSRF-Protection), PBKDF2-Passworthashing, Session-Schranken
