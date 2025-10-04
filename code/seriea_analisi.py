import os
import matplotlib.pyplot as plt
import numpy as np


def openFile(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, "..", "data", filename)
    return open(filepath, "r", encoding="utf-8", errors="ignore")

def closeFile(fil):
    fil.close()
    return "ok"

def stampaPartite(sc, sa):
    f = openFile("matches_serie_A.csv")
    val_sq = 0
    val_avv = 0
    val_equal = 0
    count = 0
    set = 0
    
    risultati = []  # Lista per memorizzare i risultati testuali
    
    riga = f.readline()
    while riga != "":
        new = riga
        i = 0

        while i < 10:
            pos = new.find(',')
            if i == 1:
                data = new[0:pos:1]
            elif i == 6:
                posto = new[0:pos:1]
            elif i == 8:
                gol_squadra = new[0:pos:1]
            elif i == 9:
                gol_avversari = new[0:pos:1]
            new = new[pos+1::1]
            i += 1

        pos = new.find(',')
        squadra_avversaria = new[0:pos:1]
        
        while i < 28:
            pos = new.find(',')
            if i == 26:
                s = new[pos+1:pos+5:1]
            new = new[pos+1::1]
            i += 1

        squadra_scelta = new.strip()


        if (sc == squadra_scelta and sa == squadra_avversaria):
            if count == 0:
                stagione = "STAGIONE " + str(int(s)-1) + ' - ' + s
                risultati.append(stagione)
                count += 1
           
            else:
                count = 0
            
            
            if(posto == 'Away'):
                risultato = data + " " + squadra_avversaria + ' ' + gol_avversari + " - " + squadra_scelta + " " + gol_squadra
                set += 1
            else:
                risultato = data + " " + squadra_scelta + ' ' + gol_squadra + " - " + squadra_avversaria + " " + gol_avversari
                set += 1
            
            risultati.append(risultato)
            
            if(set == 2):
                spazio = ' \n'
                risultati.append(spazio)
                set = 0

            if(int(gol_squadra) > int(gol_avversari)):
                val_sq = val_sq + 1
            elif(int(gol_avversari) > int(gol_squadra)):
                val_avv = val_avv + 1
            else:
                val_equal = val_equal + 1  

        riga = f.readline()

    closeFile(f)

    # CREA E SALVA IL GRAFICO COME IMMAGINE
    if val_sq + val_avv + val_equal > 0:
        y = np.array([val_sq, val_avv, val_equal])
        labels = [sc, sa, "Pareggio"]

        def make_label(pct, allvals):
            total = sum(allvals)
            val = int(round(pct*total/100.0))
            return f"{val} ({pct:.1f}%)"

        # AUMENTATE le dimensioni del grafico
        plt.figure(figsize=(12, 8))  # Aumentato da (8,6) a (12,8)
        plt.pie(y, labels=labels, autopct=lambda pct: make_label(pct, y), textprops={'fontsize': 14})
        plt.axis('equal')
        plt.title(f"Confronti tra {sc} e {sa}", fontsize=16, fontweight='bold')
        
        # Salva il grafico invece di mostrarlo
        graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "grafico.png")
        plt.savefig(graph_path, dpi=100, bbox_inches='tight')  # Aumentato DPI per migliore qualità
        plt.close()  # Chiude la figura per liberare memoria
        
        # Restituisce sia i risultati che il percorso del grafico
        return "\n".join(risultati), True
    else:
        return "Nessuna partita trovata", False

def stampaPartitaSingola(sc, sa, stagione):
    f = openFile("matches_serie_A.csv")
    
    risultati = []  # Lista per memorizzare i risultati
    
    riga = f.readline()
    while riga != "":
        new = riga
        i = 0

        while i < 10:
            pos = new.find(',')
            if i == 1:
                data = new[0:pos:1]
            elif i == 6:
                posto = new[0:pos:1]
            elif i == 8:
                gol_squadra = new[0:pos:1]
            elif i == 9:
                gol_avversari = new[0:pos:1]
            new = new[pos+1::1]
            i += 1

        pos = new.find(',')
        squadra_avversaria = new[0:pos:1]
        
        while i < 28:
            pos = new.find(',')
            if i == 27:
                s = new[0:pos:1]
            new = new[pos+1::1]
            i += 1

        squadra_scelta = new.strip()

        if sc == squadra_scelta and sa == squadra_avversaria and s == stagione and posto == 'Home':
            st = "STAGIONE " + str(int(s)-1) + ' - ' + s
            risultati.append(st)
            risultato = data + " " + squadra_scelta + ' ' + gol_squadra + " - " + squadra_avversaria + " " + gol_avversari
            risultati.append(risultato)

        riga = f.readline()

    closeFile(f)
    
    return "\n".join(risultati) if risultati else "Nessuna partita trovata"

def stampaPuntiInClassifica(squad,stagiones):
    f = openFile("matches_serie_A.csv")
    
    result = 0
    
    riga = f.readline()
    while riga != "":
        new = riga
        i = 0

        while i < 10:
            pos = new.find(',')
            if i == 8:
                gol_squadra = new[0:pos:1]
            elif i == 9:
                gol_avversari = new[0:pos:1]
            new = new[pos+1::1]
            i += 1

        while i < 28:
            pos = new.find(',')
            if i == 26:
                s = new[pos+1:pos+5:1]
            new = new[pos+1::1]
            i += 1

        squadra_scelta = new.strip()

        if(squad == squadra_scelta and s == stagiones):
            if(gol_squadra > gol_avversari):
                result += 3
            elif(gol_avversari == gol_squadra):
                result += 1

        riga = f.readline()

    closeFile(f)

    return "La squadra " + squad + " nella stagione " + str(int(stagiones)-1) + ' - ' + stagiones+ " ha totalizzato " + str(result) + " punti"

def classificaStagione(stag):
    f = openFile("matches_serie_A.csv")

    risultati = []

    result = 0
    partite = 0
    gol_fatti = 0
    gol_subiti = 0
    partite_pareggiate = 0
    partite_perse = 0
    partite_vinte = 0 

    riga = f.readline()
    riga = f.readline()
    while riga != "":
        new = riga
        i = 0

        while i < 10:
            pos = new.find(',')
            if i == 8:
                gol_squadra = new[0:pos:1]
                gol_fatti += int(gol_squadra)
            elif i == 9:
                gol_avversari = new[0:pos:1]
                gol_subiti += int(gol_avversari)
            new = new[pos+1::1]
            i += 1

        while i < 28:
            pos = new.find(',')
            if i == 26:
                s = new[pos+1:pos+5:1]
            new = new[pos+1::1]
            i += 1

        squadra_scelta = new.strip()

        if(s == stag):
            if(gol_squadra > gol_avversari):
                result += 3
                partite_vinte += 1
            elif(gol_avversari == gol_squadra):
                result += 1
                partite_pareggiate += 1
            else:
                partite_perse += 1
            partite += 1
        else:
            gol_fatti = 0
            gol_subiti = 0

        if(partite == 38):
            dict = {"Squadra": squadra_scelta, "Punti": str(result),"Partite Giocate": "38", "Partite Vinte":str(partite_vinte),"Partite Pareggiate":str(partite_pareggiate),"Partite Perse":str(partite_perse), "Gol Fatti": str(gol_fatti), "Gol Subiti": str(gol_subiti), "Differenza Reti": str(gol_fatti - gol_subiti)},
            risultati.append(dict)
            gol_fatti = 0
            gol_subiti = 0
            result = 0
            partite_pareggiate = 0
            partite_perse = 0
            partite_vinte = 0
            partite = 0
        
        riga = f.readline()

    closeFile(f)

    print(f"{'Pos':<4}{'Squadra':<15}{'Pt':>4}{'PG':>5}{'V':>5}{'N':>5}{'P':>5}{'GF':>6}{'GS':>6}{'Diff':>7}")
    print("-" * 68)

    for i, squadra_tuple in enumerate(risultati, start=1):
        s = squadra_tuple[0]  # estrai il dizionario dalla tupla
        print(f"{i:<4}{s['Squadra']:<15}"
            f"{s['Punti']:>4}{s['Partite Giocate']:>5}"
            f"{s['Partite Vinte']:>5}{s['Partite Pareggiate']:>5}"
            f"{s['Partite Perse']:>5}{s['Gol Fatti']:>6}"
            f"{s['Gol Subiti']:>6}{s['Differenza Reti']:>7}")

    return risultati

# MODIFICA: Non eseguire più automaticamente, ma solo se chiamato direttamente
if __name__ == "__main__":
    print("Seleziona l'azione che vuoi eseguire")
    print("1 - Guarda gli ultimi confronti tra le due squadre selezionate\n2 - Dimmi quanto è finita una determinata partita selezionata\n3 - Punti di una squadra in una determinata stagione\n4 - Classifica della stagione selezionata")
    select = int(input())

    while select != 1 and select != 2 and select != 3 and select != 4:
        print("Il numero selezionato non è giusto. Riprova")
        select = int(input())

    if select == 1:
        print("Inserisci la prima squadra")
        sq1 = input()

        print("Inserisci la seconda squadra")
        sq2 = input()

        risultati, ha_grafico = stampaPartite(sq1, sq2)
        print(risultati)
        if ha_grafico:
            print("\n[GRAFICO GENERATO]")
    elif select == 2:
        print("Inserisci la squadra di casa")
        sq1 = input()

        print("Inserisci la squadra ospite")
        sq2 = input()

        print("Seleziona la stagione (N.B Nel mettere la stagione si conta la seconda data)\n Esempio: Stagione 2020-2021 --> 2021")
        season = input()

        risultati = stampaPartitaSingola(sq1, sq2, season)
        print(risultati)
    elif select == 3:
        print("Inserisci la squadra")
        sq1 = input()

        print("Seleziona la stagione (N.B Nel mettere la stagione si conta la seconda data)\n Esempio: Stagione 2020-2021 --> 2021")
        season = input()

        risultati = stampaPuntiInClassifica(sq1,season)

        print(risultati)
    else:
        print("Inserisci la stagione")

        season = input()

        risultati = classificaStagione(season)


