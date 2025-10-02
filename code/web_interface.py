"""
FILE: web_interface.py
SCOPO: Creare un'interfaccia web per il codice esistente senza modificarlo
TECNOLOGIE: Flask (micro web framework Python)
CHE COSA FA: Prende l'input dal browser, esegue il tuo script, e mostra i risultati
"""

from flask import Flask, request, jsonify, render_template
import subprocess
import sys
import os
import importlib.util

# INIZIALIZZA L'APP FLASK
app = Flask(__name__)

# ROTTA PRINCIPALE: Quando si visita http://localhost:5000/
@app.route('/')
def home():
    """
    Mostra la pagina HTML principale
    Non restituisce più HTML direttamente, ma usa un template
    """
    return render_template('index.html')

# ROTTA PER L'ANALISI: Gestisce i dati inviati dal form
@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Riceve i dati dal form web, esegue le funzioni direttamente e restituisce i risultati
    """
    try:
        # LEGGE I DATI INVIATI DAL FORM
        action = request.form['action']             # 1 o 2
        team1 = request.form['team1']               # Prima squadra
        team2 = request.form['team2']               # Seconda squadra
        season = request.form.get('season', '')     # Stagione (solo per azione 2)
        
        # Importa e usa direttamente le funzioni invece di eseguire subprocess
        from seriea_analisi import stampaPartite, stampaPartitaSingola, stampaPuntiInClassifica
        
        if action == "1":
            # Ultimi confronti tra squadre
            risultati, ha_grafico = stampaPartite(team1, team2)
            
            # Prepara la risposta
            response = {
                "result": risultati,
                "has_graph": ha_grafico
            }
            
        elif action == "2":
            # Partita specifica
            risultati = stampaPartitaSingola(team1, team2, season)
            response = {
                "result": risultati,
                "has_graph": False
            }
        
        else:
            risultati = stampaPuntiInClassifica(team1,season)
            response = {
                "result": risultati,
                "has_graph": False
            }
            
        return jsonify(response)
            
    except Exception as e:
        # GESTISCE ECCEZIONI IMPREVISTE
        return jsonify({"error": str(e)})

# AVVIA IL SERVER
if __name__ == '__main__':
    """
    Questo blocco viene eseguito solo se il file è runnato direttamente,
    non se è importato da altri script
    """
    app.run(debug=True, host='0.0.0.0', port=5000)