# voxel-game-prompt-writer

Una skill per Claude che trasforma un'idea breve di gioco ("mini golf sull'isola", "gara di kart") in un prompt lungo e dettagliato in inglese, 1.500-2.000 parole. Il prompt serve a far costruire a un modello un gioco HTML5 in un solo file, in pixel art 3D a voxel su un'isola fluttuante (three.js r128, nessun asset esterno).

I prompt generati seguono la struttura, la densità e lo stile di un prompt di riferimento (Beach Volleyball) e aggiungono cinque cose che il riferimento non ha:

1. simulazione separata dalla grafica, eseguibile e testabile in Node senza browser, con passo fisso e seme;
2. requisiti divisi in MUST e IF ROOM, con l'ordine in cui tagliare;
3. un obiettivo di prestazioni (30 fps su un portatile medio) e cosa semplificare se non si raggiunge;
4. criteri di accettazione misurabili: quante partite simulare, quali medie devono uscire, cosa fare se non rientrano;
5. un rapporto finale onesto su cosa è fatto, verificato, non verificato e semplificato.

## Download

Scarica `voxel-game-prompt-writer.zip` dalla pagina [Releases](../../releases/latest), oppure clona il repository.

## Installazione

**Claude Code**: estrai lo zip in `~/.claude/skills/`, così da avere `~/.claude/skills/voxel-game-prompt-writer/SKILL.md`.

```bash
unzip voxel-game-prompt-writer.zip -d ~/.claude/skills/
```

**claude.ai / app Claude**: Impostazioni > Capacità > Skill > carica `voxel-game-prompt-writer.zip`.

## Uso

Scrivi a Claude, per esempio:

- "Scrivimi il prompt per una gara di kart sull'isola"
- "/voxel-game-prompt-writer mini golf a 9 buche"

La skill fa al massimo 3 domande a scelta multipla solo se manca qualcosa che cambia molto il gioco (giocatori, inquadratura, durata, modalità). Poi scrive uno schema con le scelte fatte e i punti specifici del gioco, quindi il prompt completo in un blocco di testo pronto da copiare, e infine controlla il prompt con uno script.

## Contenuto

```
voxel-game-prompt-writer/
  SKILL.md                                    istruzioni della skill
  references/reference-beach-volleyball.txt   prompt di riferimento originale
  references/common-blocks.md                 blocchi comuni da riusare (rendering, isola, UI, test...)
  references/game-specific.md                 sezioni per genere, cosa inventare, numeri, insidie
  references/example-kart-race.txt            esempio completo già conforme
  scripts/check_prompt.py                     verifica automatica (solo libreria standard Python 3)
```

Lo script si può usare anche da solo:

```bash
python3 voxel-game-prompt-writer/scripts/check_prompt.py --forbid "volleyball,spike" mio-prompt.txt
```

Controlla sezioni e loro ordine, vincoli tecnici, numeri concreti in regole e fisica, test deterministici nel QUALITY BAR, lunghezza, caratteri non ASCII o rovinati (per esempio "5le" al posto di "file"), righe di impaginazione, segnaposto rimasti e dati personali.
