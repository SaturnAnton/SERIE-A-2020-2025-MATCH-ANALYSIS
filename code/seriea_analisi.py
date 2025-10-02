import os
import matplotlib.pyplot as plt
import numpy as np

def openFile(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, "..", "data", filename)
    return open(filepath, "r")

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

        plt.figure(figsize=(8, 6))
        plt.pie(y, labels=labels, autopct=lambda pct: make_label(pct, y))
        plt.axis('equal')
        plt.title(f"Confronti tra {sc} e {sa}")
        
        # Salva il grafico invece di mostrarlo
        graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "grafico.png")
        plt.savefig(graph_path)
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

# MODIFICA: Non eseguire più automaticamente, ma solo se chiamato direttamente
if __name__ == "__main__":
    print("Seleziona l'azione che vuoi eseguire")
    print("1 - Guarda gli ultimi confronti tra le due squadre selezionate\n2 - Dimmi quanto è finita una determinata partita selezionata")
    select = int(input())

    while select != 1 and select != 2:
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
    else:
        print("Inserisci la squadra di casa")
        sq1 = input()

        print("Inserisci la squadra ospite")
        sq2 = input()

        print("Seleziona la stagione (N.B Nel mettere la stagione si conta la seconda data)\n Esempio: Stagione 2020-2021 --> 2021")
        season = input()

        risultati = stampaPartitaSingola(sq1, sq2, season)
        print(risultati)