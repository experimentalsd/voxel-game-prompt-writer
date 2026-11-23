---
name: voxel-game-prompt-writer
description: Trasforma un'idea breve di gioco (per esempio "mini golf sull'isola" o "gara di kart") in un prompt lungo e dettagliato in inglese, 1.500-2.000 parole, che un altro modello userà per costruire un gioco HTML5 in un solo file, in pixel art 3D a voxel su un'isola fluttuante (three.js r128, nessun asset esterno), con la stessa struttura, densità e stile del modello Beach Volleyball. Usala quando l'utente chiede "scrivimi il prompt per un gioco voxel", "prompt come quello del beach volley", "/voxel-game-prompt-writer", o dà un'idea di gioco in pixel art 3D da trasformare in prompt.
---

# Voxel game prompt writer

Da un'idea di poche parole a un prompt in inglese, in testo semplice, pronto da copiare, che fa costruire a un altro modello un gioco HTML5 in un solo file, in pixel art 3D a voxel. Il prompt ha lo stesso livello di dettaglio, la stessa struttura e lo stesso stile del modello di riferimento, più cinque miglioramenti che il modello non ha.

## File della skill

- `references/reference-beach-volleyball.txt`: il modello originale. Leggilo per tono, densità e ritmo degli elenchi. Non copiarne i difetti (vedi "Miglioramenti obbligatori").
- `references/common-blocks.md`: i blocchi comuni in inglese da riprendere quasi identici, con segnaposto `{...}`.
- `references/game-specific.md`: nomi delle sezioni per genere, cosa inventare per ogni sezione, numeri di partenza, insidie da scrivere come regole.
- `references/example-kart-race.txt`: un prompt completo già conforme (gara di kart). Usalo per calibrare lunghezza e densità, non come testo da riciclare.
- `scripts/check_prompt.py`: verifica automatica del prompt finito.

Leggi sempre `common-blocks.md` e `game-specific.md` prima di scrivere. Leggi il riferimento e l'esempio la prima volta che usi la skill in una conversazione.

## Procedura

### 1. Capire l'idea

Ricava dall'idea: genere (tabella in `game-specific.md`, sezione 1), lati o squadre, numero di attori, oggetto di gioco (palla, kart, disco...), come finisce una partita, che cosa rende il gioco diverso dal modello. Scegli i nomi delle sezioni dalla tabella.

### 2. Domande: al massimo 3, solo se servono

Chiedi solo se manca un'informazione che cambia molto il gioco:
- numero di giocatori o di attori per lato (1 contro 1, 2 contro 2, sei kart...);
- vista o inquadratura principale (panoramica sull'isola, dietro all'attore, dall'alto);
- durata di una partita (punti, giri, buche, tempo);
- modalità (solo Watch e un giocatore, due giocatori sulla stessa tastiera, torneo).

Usa `AskUserQuestion` con una sola chiamata, da 1 a 3 domande, ciascuna con 2-4 opzioni; la prima opzione è quella che consigli e porta "(consigliata)". Non chiedere mai di ciò che è fisso o deducibile: rendering, palette, isola, interfaccia, tasti, suoni, camere, test. Se l'idea basta, non chiedere nulla: decidi tu e dichiara le scelte nello schema. Se lo strumento non c'è, decidi e dichiara.

### 3. Schema (in italiano, nella chat)

Prima del prompt scrivi uno schema breve con tre parti:

- **Scelte fatte**: 3-6 righe con le decisioni prese senza chiedere (attori, durata, modalità, inquadratura, elementi di gioco inventati).
- **Sezioni**: i titoli in ordine, come compariranno nel prompt.
- **Punti specifici del gioco**: 8-15 voci con numeri (regole chiave, fisica, azioni, livelli di difficoltà, IA, segnalazioni a schermo, statistiche, suoni, obiettivi di bilanciamento per il QUALITY BAR).

Non aspettare conferma: dopo lo schema scrivi subito il prompt.

### 4. Prompt (in inglese)

Ordine fisso:

1. Riga del titolo.
2. Riga di presentazione con i vincoli tecnici e le dipendenze che richiedono internet (blocco "Title and pitch line").
3. ARCHITECTURE
4. LOOK (pipeline di rendering, isola, campo o pista, dintorni, effetto casa delle bambole)
5. Attori (PLAYERS, KARTS AND DRIVERS, FIGHTERS...)
6. Fisica (BALL AND PHYSICS, DRIVING PHYSICS...)
7. Regole (RULES, RACE RULES...)
8. Azioni (ACTIONS AND CONTACT, SHOTS AND CONTACT...)
9. AI
10. HUMAN CONTROL
11. CAMERAS
12. UI (con i suoni)
13. SCOPE
14. PERFORMANCE
15. QUALITY BAR
16. REPORT

Le parti comuni vengono da `common-blocks.md`: riprendile quasi identiche e cambia solo ciò che dipende dal gioco. Le parti specifiche (campo, attori e pose, fisica, regole, azioni, IA, contesto dei tasti, regia delle camere, statistiche, suoni, metriche del QUALITY BAR) vanno inventate seguendo `game-specific.md`, sezione 3.

### 5. Verifica

Fai girare lo script passando il testo su stdin, senza creare file:

```bash
python3 "<cartella della skill>/scripts/check_prompt.py" --forbid "volleyball,spike,setter,Azure,Amber" - <<'PROMPT_EOF'
...testo del prompt...
PROMPT_EOF
```

In `--forbid` metti i termini del modello che non c'entrano con questo gioco (per un gioco di pallavolo lascia l'opzione vuota). Correggi ogni FAIL e rileggi ogni WARN, poi ripeti finché il risultato è PASS. Lo script controlla: presenza e ordine delle sezioni, vincoli tecnici nella riga di presentazione, numeri concreti in regole e fisica, 120 Hz, QUALITY BAR con test deterministici e semi, SCOPE con MUST e IF ROOM, obiettivo di fps, REPORT, lunghezza, caratteri non ASCII, caratteri rovinati (come "5le" al posto di "file"), righe di impaginazione, segnaposto rimasti, dati personali.

Controlla poi a mano ciò che lo script non vede:
- ogni blocco comune è presente e adattato (nessun riferimento al gioco del modello, come rete o battuta in una gara di kart);
- ogni azione ha durata, finestra di contatto e raggio; i livelli Easy / Normal / Pro hanno numeri;
- le segnalazioni a schermo sono 8-14 nomi esatti in maiuscolo;
- c'è un ordine di priorità dove convivono più modalità, livelli o camere (umano contro autopilota, regia contro trascinamento, MUST contro IF ROOM);
- le insidie rilevanti di `game-specific.md`, sezione 5, sono scritte come regole.

Se non puoi eseguire comandi, fai tutti questi controlli a mano e dillo.

### 6. Consegna

Un solo messaggio nella chat, senza file né artefatti:
1. lo schema;
2. il prompt dentro un blocco di codice ```text, così si copia in un clic;
3. una riga finale con l'esito della verifica (per esempio "Verifica: PASS, 1.840 parole, 14 sezioni").

Non salvare il prompt su disco.

## Stile del prompt

- Frasi imperative e compatte. Nessuna introduzione, nessuna spiegazione del perché, nessun "you should".
- Elenchi puntati densi con `* ` sotto titoli in maiuscolo su righe proprie. Nessun altro markdown dentro il prompt.
- Numeri concreti ovunque contino: durate, raggi, velocità, tolleranze, frequenza di simulazione, attrito, resistenza, quante prove.
- Elenchi di nomi esatti: testi delle segnalazioni, tasti, opzioni dei menu, nomi delle camere, voci delle statistiche.
- Avvertenze sui punti in cui un modello sbaglia, scritte come regole: "X must be ... BEFORE ..., otherwise ...".
- Ordine di priorità esplicito quando ci sono più modalità, livelli o camere.
- Ortografia del modello (colour, initialised, metres). Solo caratteri ASCII: virgolette dritte, `-` per intervalli e trattini, `x` per "per".
- Nomi originali per squadre, piloti, luoghi. Nessun marchio, nessun personaggio o gioco esistente da ricreare.
- Quando ti riferisci a una persona nel prompt (arbitro, giocatore), usa "they" o riformula.

## Miglioramenti obbligatori (il modello non li ha)

1. **Simulazione separata dalla grafica**: sezione ARCHITECTURE con sim in puro JS, passo fisso, PRNG con seme, API per l'input, stato in dati semplici, coda di eventi, esecuzione in Node senza browser.
2. **Indispensabili e secondari**: sezione SCOPE con MUST e IF ROOM, più l'ordine di taglio.
3. **Obiettivo di prestazioni**: sezione PERFORMANCE con 30 fps su un portatile medio, budget e cosa semplificare, in quale ordine, se non si raggiunge.
4. **Criteri misurabili**: il QUALITY BAR dice quante partite simulare per livello e per modalità, con quali semi, quali valori medi devono uscire, quali parametri regolare e cosa fare se dopo 3 tentativi non rientrano.
5. **Rapporto onesto**: sezione REPORT con fatto, verificato e come, non verificato, semplificato o tagliato, bug noti.

Inoltre: la riga di presentazione dichiara che three.js e i font richiedono internet e indica la riserva (secondo CDN, messaggio in pagina, font di sistema); il testo finale non ha caratteri rovinati né righe di impaginazione.

## Lunghezza

1.500-2.000 parole, meglio 1.700-1.950 (lo script conta come parole solo i gruppi che contengono lettere o cifre, quindi "/" e "*" non contano). I blocchi comuni, una volta compilati, occupano circa 1.100 parole: restano circa 850 parole per le parti specifiche. Se sfori, accorcia prima le spiegazioni dentro i blocchi comuni, poi gli oggetti decorativi; non togliere mai numeri, nomi esatti o avvertenze. Se resti sotto, aggiungi dettaglio a regole, azioni e IA, non ai dintorni.
