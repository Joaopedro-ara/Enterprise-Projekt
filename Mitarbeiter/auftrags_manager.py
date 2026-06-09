import io

from flask import render_template,request,redirect,url_for,session, Blueprint,jsonify,send_file
import random
import pandas as pd
import mysql.connector

class AuftragsManager:
    def __init__(self,db_connection):
        self.db=db_connection
        self.cursor = db_connection.cursor()

    def kundenauftrag_anlegen(self,kundenauftrag_id,kunde_name,produkt_id,menge,liefertermin,priorität,status,werk_id,ersteelungsdatum):
        try:
            sql="Insert into Kunden_auftraege()"