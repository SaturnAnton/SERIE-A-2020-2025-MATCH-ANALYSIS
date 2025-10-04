import io
import sys
from flask import Flask, request, jsonify, render_template
from seriea_analisi import (
    stampaPartite,
    stampaPartitaSingola,
    stampaPuntiInClassifica,
    classificaStagione
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        action = request.form['action']
        team1 = request.form.get('team1', '')
        team2 = request.form.get('team2', '')
        season = request.form.get('season', '')

        buffer = io.StringIO()
        sys_stdout_originale = sys.stdout
        sys.stdout = buffer

        ha_grafico = False
        output_stampato = ""

        if action == "1":
            risultati, ha_grafico = stampaPartite(team1, team2)
            output_stampato = risultati
        elif action == "2":
            output_stampato = stampaPartitaSingola(team1, team2, season)
        elif action == "3":
            output_stampato = stampaPuntiInClassifica(team1, season)
        else:  # azione 4
            classificaStagione(season)  # stampa direttamente
            # output_stampato sarà tutto ciò che è stato stampato
            output_stampato = buffer.getvalue().strip()

        sys.stdout = sys_stdout_originale

        # fallback se output_stampato è vuoto
        if not output_stampato:
            output_stampato = "Nessun risultato disponibile"

        return jsonify({"result": output_stampato, "has_graph": ha_grafico})

    except Exception as e:
        sys.stdout = sys.__stdout__
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
