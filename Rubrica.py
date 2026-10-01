import json

rubrica = {}


def salva_rubrica():
    with open('rubrica.json', 'w') as file:
        json.dump(rubrica, file)

def carica_rubrica():
    try:
        with open('rubrica.json', 'r') as file:
            dati = json.load(file)
            rubrica.update(dati)
    except FileNotFoundError:
        pass

def chiedi_conferma():
    conferma = input('Premi INVIO per continuare o digita 5 per tornare al menu: ')
    return conferma == '5'

def rubrica_vuota():
    if len(rubrica) == 0:
        print('La rubrica è vuota!')
        return True
    return False

def trova_nome(nome_cercato):
    for nome in rubrica:
        if nome.lower() == nome_cercato.lower():
            return nome
    return None

def cerca_contatti(testo):
    risultati = []

    for nome, numero in rubrica.items():
        if testo.lower() in nome.lower() or testo in numero:
            risultati.append(nome)

    return risultati

def chiedi_nome():
    while True:
        nome = input('Digita il nome: ').strip()

        if not nome:
            print('Il nome non può essere vuoto.')
            continue

        return nome

def chiedi_numero():
    while True:
        numero = input('Digita il numero: ').strip()

        if not numero.isdigit():
            print('Il numero deve contenere solo cifre.')
            continue

        if len(numero) < 7:
            print('Il numero è troppo corto.')
            continue

        if numero in rubrica.values():
            print('Questo numero è già in rubrica!')
            continue

        return numero

def agg_contatto():
    print('\n-- AGGIUNGI UN CONTATTO --')
    if chiedi_conferma():
        return

    while True:
        nuovo_nome = chiedi_nome()

        if trova_nome(nuovo_nome):
            print('Questo nome esiste già!')
        else:
            break

    nuovo_numero = chiedi_numero()

    rubrica[nuovo_nome] = nuovo_numero
    salva_rubrica()

    print(f'Hai aggiunto {nuovo_nome} alla rubrica!')

def cerca_contatto():
    print('\n-- CERCA CONTATTO --')
    if chiedi_conferma():
        return

    testo = input('Digita nome o numero da cercare: ').strip()

    risultati = cerca_contatti(testo)

    if not risultati:
        print(f'{testo} non trovato.')
        return

    for nome in risultati:
        print(f'{nome}: {rubrica[nome]}')

def mostra_contatti():
    print('\n-- MOSTRA CONTATTI --')
    if chiedi_conferma():
        return

    if rubrica_vuota():
        return

    for nome, numero in sorted(rubrica.items()):
        print(f'{nome} - {numero}')

def elimina_contatto():
    print('\n-- ELIMINA CONTATTO --')
    if chiedi_conferma():
        return

    if rubrica_vuota():
        return

    for nome, numero in sorted(rubrica.items()):
        print(f'{nome} - {numero}')

    nome_cercato = input('Quale contatto vuoi eliminare? ')
    nome = trova_nome(nome_cercato)

    if nome:
        del rubrica[nome]
        salva_rubrica()
        print(f'Hai eliminato {nome}.')
    else:
        print(f'{nome_cercato} non trovato.')

def modifica_contatto():
    print('\n-- MODIFICA CONTATTO --')
    if chiedi_conferma():
        return

    if rubrica_vuota():
        return

    nome_cercato = input('Digita il nome del contatto da modificare: ')
    nome = trova_nome(nome_cercato)

    if not nome:
        print(f'{nome_cercato} non trovato.')
        return

    print(f'\nContatto trovato: {nome} - {rubrica[nome]}')
    print('1. Modifica nome')
    print('2. Modifica numero')

    scelta_mod = input('Cosa vuoi modificare? ')

    if scelta_mod == '1':
        while True:
            nuovo_nome = chiedi_nome()

            if trova_nome(nuovo_nome):
                print('Questo nome esiste già!')
            else:
                break

        rubrica[nuovo_nome] = rubrica.pop(nome)
        salva_rubrica()
        print(f'Nome aggiornato a {nuovo_nome}!')


    elif scelta_mod == '2':

        nuovo_numero = chiedi_numero()

        rubrica[nome] = nuovo_numero

        salva_rubrica()

        print(f'Numero di {nome} aggiornato!')

    else:
        print('Scelta non valida.')

carica_rubrica()

while True:
    print('\n-- RUBRICA --')
    print('1. Aggiungi contatto')
    print('2. Cerca contatto')
    print('3. Mostra tutti i contatti')
    print('4. Elimina contatto')
    print('5. Modifica contatto')
    print('6. Esci')

    try:
        scelta = int(input('Scelta: '))
    except ValueError:
        print('Inserisci solo un numero!')
        continue

    if scelta == 1:
        agg_contatto()
    elif scelta == 2:
        cerca_contatto()
    elif scelta == 3:
        mostra_contatti()
    elif scelta == 4:
        elimina_contatto()
    elif scelta == 5:
        modifica_contatto()
    elif scelta == 6:
        print('Arrivederci!')
        break
    else:
        print('Inserisci un numero valido!')