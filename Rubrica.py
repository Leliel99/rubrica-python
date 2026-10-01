import json

import random

from datetime import datetime

rubrica = {}

def esporta_rubrica():
    print('\n-- ESPORTA RUBRICA --')
    if chiedi_conferma():
        return

    if rubrica_vuota():
        return

    oggi = datetime.now()
    data = f'{oggi.day}/{oggi.month}/{oggi.year}'
    nome_file = f'rubrica_esportata_{oggi.day}{oggi.month}{oggi.year}.txt'

    with open(nome_file, 'w') as file:
        file.write(f'RUBRICA - esportata il {data}\n')
        file.write('=' * 40 + '\n')
        for nome, numero in sorted(rubrica.items()):
            file.write(f'{nome} - {numero}\n')

    print(f'Rubrica esportata in {nome_file}!')

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

def chiedi_numero(numero_attuale=None):
    while True:
        numero = input('Digita il numero: ').strip()

        if not numero.isdigit():
            print('Il numero deve contenere solo cifre.')
            continue

        if len(numero) < 7:
            print('Il numero è troppo corto.')
            continue

        if numero in rubrica.values() and numero != numero_attuale:
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

        nuovo_numero = chiedi_numero(numero_attuale=rubrica[nome])

        rubrica[nome] = nuovo_numero

        salva_rubrica()

        print(f'Numero di {nome} aggiornato!')

    else:
        print('Scelta non valida.')

def ordina_per_numero():
    print('\n-- CONTATTI ORDINATI PER NUMERO --')
    if chiedi_conferma():
        return

    if rubrica_vuota():
        return

    ordinati = sorted(rubrica.items(), key=lambda x: x[1])
    for nome, numero in ordinati:
        print(f'{nome} - {numero}')

def mischia_rubrica():
    print('\n-- MISCHIA RUBRICA --')
    if chiedi_conferma():
        return

    if rubrica_vuota():
        return

    # Salva backup prima di mischare
    with open('rubrica_backup.json', 'w') as file:
        json.dump(rubrica, file)

    nomi = list(rubrica.keys())
    numeri = list(rubrica.values())
    random.shuffle(numeri)

    rubrica_mischiata = dict(zip(nomi, numeri))

    print('Rubrica mischiata:')
    for nome, numero in rubrica_mischiata.items():
        print(f'{nome} - {numero}')

    conferma = input('\nVuoi salvare la versione mischiata? (si/no) ')
    if conferma.lower() == 'si':
        rubrica.update(rubrica_mischiata)
        salva_rubrica()
        print('Rubrica mischiata salvata! Puoi ripristinarla con l\'opzione 10.')
    else:
        print('Nessuna modifica salvata.')

def ripristina_rubrica():
    print('\n-- RIPRISTINA RUBRICA --')
    if chiedi_conferma():
        return

    try:
        with open('rubrica_backup.json', 'r') as file:
            dati = json.load(file)
            rubrica.clear()
            rubrica.update(dati)
            salva_rubrica()
            print('Rubrica ripristinata!')
    except FileNotFoundError:
        print('Nessun backup trovato. Mischia prima la rubrica.')

carica_rubrica()

while True:
    print('\n-- RUBRICA --')
    print('1. Aggiungi contatto')
    print('2. Cerca contatto')
    print('3. Mostra tutti i contatti')
    print('4. Elimina contatto')
    print('5. Modifica contatto')
    print('6. Esporta rubrica')
    print('7. Ordina per numero')
    print('8. Mischia rubrica')
    print('9. Ripristina rubrica originale')
    print('0. Esci')

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
        esporta_rubrica()
    elif scelta == 7:
        ordina_per_numero()
    elif scelta == 8:
        mischia_rubrica()
    elif scelta == 9:
        ripristina_rubrica()
    elif scelta == 0:
        print('Arrivederci!')
        break