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
    Riceve i dati dal form web, esegue il tuo script Python e restituisce i risultati puliti
    """
    try:
        # LEGGE I DATI INVIATI DAL FORM
        action = request.form['action']             # 1 o 2
        team1 = request.form['team1']               # Prima squadra
        team2 = request.form['team2']               # Seconda squadra
        season = request.form.get('season', '')     # Stagione (solo per azione 2)
        
        # PREPARA L'INPUT PER IL TUO SCRIPT ORIGINALE
        # Simula quello che digiti nel terminale
        inputs = f"{action}\n{team1}\n{team2}\n"
        if action == "2":
            inputs += f"{season}\n"
        
        # ESEGUE IL TUO SCRIPT COME SE FOSSE NEL TERMINALE
        result = subprocess.run(
            [sys.executable, "seriea_analisi.py"],              # Comando: python seriea_analisi.py
            input=inputs,                                       # Input simulato
            text=True,                                          # Testo invece di bytes
            capture_output=True,                                # Cattura output e errori
            cwd=os.path.dirname(os.path.abspath(__file__))      # Esegui dalla cartella corretta
        )
        
        # CONTROLLA SE L'ESECUZIONE È ANDATA BENE
        if result.returncode == 0:
            # PULISCE L'OUTPUT: rimuove menu e domande, tiene solo risultati
            output_lines = result.stdout.split('\n')
            cleaned_lines = []
            
            for line in output_lines:
                # Mantiene solo le righe con i risultati delle partite
                if 'Punteggio finale' in line:
                    cleaned_lines.append(line.strip())
            
            # PREPARA L'OUTPUT FINALE
            if cleaned_lines:
                final_output = '\n'.join(cleaned_lines)
            else:
                final_output = "Nessun risultato trovato per i criteri di ricerca"
                
            return jsonify({"result": final_output})
        else:
            # GESTISCE GLI ERRORI
            error_msg = result.stderr
            if "No such file or directory" in error_msg:
                error_msg += "\n\n💡 SUGGERIMENTO: Controlla il percorso del file CSV nel codice!"
            return jsonify({"error": error_msg})
            
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
    
    # debug=True: Ricarica automaticamente quando modifichi i file
    # host='0.0.0.0': Accessibile da altri dispositivi nella rete
    # port=5000: Porta su cui ascolta il server