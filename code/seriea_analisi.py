def openFile(filename):
   result = open(filename,'r')
   return result


def closeFile(fil):
   fil.flush()
   fil.close()
   return "ok"


def stampaPartite (sc,sa):
    file = "data/matches_serie_A.csv"
    f = openFile(file)
    
    riga = f.readline()

    while riga != "" :
        new = riga
        i = 0

        while i < 10 :
            pos = new.find(',')
            if i == 1 :
                data = new[0:pos:1]
            elif i == 6:
                posto = new[0:pos:1]
            elif i == 8:
                gol_squadra = new[0:pos:1]
            elif i == 9:
                gol_avversari = new[0:pos:1]
            new = new[pos+1::1]
            i = i+1
        pos = new.find(',')
        squadra_avversaria = new[0:pos:1]
        
        while i < 28 :
            pos = new.find(',')
            new = new[pos+1::1]
            i = i+1

        squadra_scelta = new.strip()

        if (sc == squadra_scelta and sa == squadra_avversaria) :
            if(posto == 'Away') :
                print(data + " " + squadra_avversaria + "-" + squadra_scelta + " Punteggio finale: " + gol_avversari + "-" + gol_squadra)
            else:
                print(data + " " + squadra_scelta + "-" + squadra_avversaria + " Punteggio finale: " + gol_squadra + "-" + gol_avversari)

        riga = f.readline()

    closeFile(f)

def stampaPartitaSingola(sc,sa,stagione) :
    file = "data/matches_serie_A.csv"
    f = openFile(file)
    
    riga = f.readline()

    while riga != "" :
        new = riga
        i = 0

        while i < 10 :
            pos = new.find(',')
            if i == 1 :
                data = new[0:pos:1]
            elif i == 6:
                posto = new[0:pos:1]
            elif i == 8:
                gol_squadra = new[0:pos:1]
            elif i == 9:
                gol_avversari = new[0:pos:1]
            new = new[pos+1::1]
            i = i+1
        pos = new.find(',')
        squadra_avversaria = new[0:pos:1]
        
        while i < 28 :
            pos = new.find(',')
            if i == 27 :
                s = new[0:pos:1]
            new = new[pos+1::1]
            i = i+1

        squadra_scelta = new.strip()

        if sc == squadra_scelta and sa == squadra_avversaria and s == stagione and posto == 'Home':
            print(data + " " + squadra_scelta + "-" + squadra_avversaria + " Punteggio finale: " + gol_squadra + "-" + gol_avversari)

        riga = f.readline()

    closeFile(f)


print("Seleziona l'azione che vuoi eseguire")
print("1 - Guarda gli ultimi confronti tra le due squadre selezionate\n2 - Dimmi quanto è finita una determinata partita selezioanata")
select = int(input())

while(select!=1 and select!=2):
    print("Il numero selezionato non è giusto. Riprova")
    select = int(input())

if(select == 1):
    print("Inserisci la prima squadra")
    sq1 = input()

    print("Inserisci la seconda squadra")
    sq2 = input()

    stampaPartite(sq1,sq2)
else:
    print("Inserisci la squadra di casa")
    sq1 = input()

    print("Inserisci la squadra ospite")
    sq2 = input()

    print("Seleziona la stagione (N.B Nel mettere la stagione si conta la seconda data)\n Esempio: Stagione 2020-2021 --> 2021")
    season = input()

    stampaPartitaSingola(sq1,sq2,season)