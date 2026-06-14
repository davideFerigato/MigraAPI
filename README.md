# 🦾 MigraAPI – Claude Agent per migrazione automatica di API

> Agente AI basato su **Claude Skills** e **Subagents** (Anthropic) che migra codice da vecchia API a nuova API in modo automatico, sicuro e scalabile.

## 📌 Indice
- [Introduzione](#introduzione)
- [Architettura](#architrattura)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Come usare MigraAPI](#come-usare-migraapi)
- [Esempi](#esempi)
- [Troubleshooting](#troubleshooting)
- [Roadmap e contributi](#roadmap-e-contributi)
- [Licenza](#licenza)

## Introduzione

MigraAPI è un progetto dimostrativo che implementa i concetti avanzati di **Agent Skills** e **Subagents** insegnati nei corsi ufficiali di Anthropic. Permette di automatizzare la migrazione di chiamate API deprecate in codebase Python e JavaScript, usando un agente orchestratore che delega task a subagent specializzati in isolamento.

## Architettura

Il sistema segue il **pattern dell’orchestratore**:

```
Utente → Orchestratore (Claude Code) → Subagent scanner → Subagent rewriter → Subagent validator
                                        ↑                    ↑                    ↑
                                        (parallel on files)  (parallel)           (parallel)
```

### Componenti

1. **Skill `api-migration`**  
   - Contiene le regole di migrazione (mapping old → new), i pattern regex e lo script scanner.  
   - Segue il meccanismo di **progressive disclosure**: solo `name` e `description` sono caricati all’avvio; il corpo completo viene letto quando la skill viene attivata.

2. **Subagent `scanner`**  
   - Isolato, riceve un file e restituisce JSON con le occorrenze deprecate.  
   - Tool consentiti: solo lettura (`Read`, `Grep`, `Glob`).

3. **Subagent `rewriter`**  
   - Applica le trasformazioni usando le regole di mapping.  
   - Tool consentiti: `Read`, `Write`, `Edit`.

4. **Subagent `validator`**  
   - Verifica la correttezza sintattica (e opzionalmente esegue test).  
   - Restituisce JSON con esito e lista errori (obstacle reporting).

5. **Orchestratore**  
   - L’agente principale (Claude Code) carica la skill e coordina i subagent.  
   - Può eseguire i subagent in **parallelo** su più file per massimizzare l’efficienza.

### Progressive Disclosure in azione

1. **Discovery**: Claude pre-carica solo `name` e `description` della skill.  
2. **Activation**: Quando l’utente chiede di migrare, Claude legge l’intero `SKILL.md`.  
3. **Execution**: Se necessario, esegue `scanner.py` o carica file aggiuntivi (`migration-rules.json`).

### Gestione del contesto

Grazie ai subagent, i file sorgente non vengono mai caricati nella context window principale. Ogni subagent lavora in una context window separata e restituisce solo un riassunto strutturato (JSON). Questo previene l’esplosione del contesto in progetti grandi.

## Prerequisiti

- **Claude Code** (con modalità agentica abilitata) – [guida all’installazione](https://docs.anthropic.com/claude-code)
- **Python 3.9+** (per lo script scanner, opzionale)
- **Node.js** (per testare esempi JavaScript, opzionale)
- Terminale Unix (macOS/Linux)

## Installazione

```bash
git clone https://github.com/tuo-username/MigraAPI
cd MigraAPI
# Nessuna dipendenza esterna necessaria – tutto è bash/python standard
```

## Come usare MigraAPI

### Demo automatica con script orchestratore

Esegui lo script demo che simula l’orchestrazione (senza Claude Code, ma mostrando la logica):

```bash
./demo-script.sh
```

Questo script:
- Scansiona tutti i file in `examples/before/` usando lo scanner integrato.
- Simula l’applicazione delle modifiche (nel reale verrebbe chiamato il subagent `rewriter`).
- Simula la validazione.
- Produce un report finale JSON.

### Utilizzo reale con Claude Code

1. Avvia Claude Code nel progetto:
   ```bash
   claude
   ```

2. Attiva la skill (automaticamente se chiedi una migrazione):
   ```
   Migra il codice in examples/before dalla vecchia API alla nuova usando la skill api-migration
   ```

3. Claude Code:
   - Carica la skill `api-migration`.
   - Esegue lo scanner tramite il subagent `scanner` su ogni file (in parallelo).
   - Raccoglie i JSON.
   - Invoca il subagent `rewriter` per applicare le modifiche.
   - Invoca il subagent `validator` per controllare i risultati.
   - Produce un report finale.

## Esempi

Prima della migrazione (`examples/before/sample.py`):
```python
from old_api import Client
client = Client(api_key="test")
user = client.get_user(user_id=123)
```

Dopo la migrazione (`examples/after/sample.py` – atteso):
```python
from new_api import Client
client = Client(api_key="test")
user = client.fetch_user_by_id(user_id=123)
```

## Troubleshooting

**Skill non si attiva** – Verifica che il nome `api-migration` e la descrizione corrispondano alla richiesta.  
**Scanner non trova occorrenze** – Controlla i pattern in `regex-patterns.md` e aggiornali.  
**Subagent non riesce a scrivere** – Assicurati che `allowed-tools` includa `Write` e `Edit`.  
**Validazione fallisce** – Controlla il JSON di errore; potrebbe indicare sintassi errata dopo la riscrittura.

## Roadmap e contributi

- [ ] Integrazione con Claude Code reale (non solo simulazione).
- [ ] Supporto per più linguaggi (Java, Go).
- [ ] Plugin per Claude Code marketplace.

Contributi sono benvenuti: fork e pull request.

## Licenza

MIT
