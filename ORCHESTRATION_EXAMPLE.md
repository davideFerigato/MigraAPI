# Esempio di orchestrazione con il tool `Task` (Claude Code)

Quando usi MigraAPI con Claude Code, l'orchestratore (l'agente principale) esegue una sequenza simile a questa:

## 1. Attivazione della skill

L'utente scrive:
```
Migra il codice in examples/before/ dalla vecchia API alla nuova.
```

Claude rileva la skill `api-migration` (tramite `name`/`description`) e carica l'intero `SKILL.md`.

## 2. Orchestrazione con `Task`

Claude (orchestratore) genera e invia comandi come:

```
Task(subagent="scanner", prompt="Analizza il file examples/before/sample.py usando i pattern: old_api\.get_user, old_api\.fetch_posts. Restituisci JSON.")
```

Riceve output JSON:
```json
{
  "status": "success",
  "file": "examples/before/sample.py",
  "occurrences": [
    {"line": 2, "code": "from old_api import Client", "pattern": "import old_api"},
    {"line": 4, "code": "user = client.get_user(user_id=123)", "pattern": "old_api.get_user"}
  ]
}
```

## 3. Esecuzione in parallelo

Per più file, Claude può lanciare più `Task` contemporaneamente:

```
Task(subagent="scanner", prompt="Analizza file1.py...")
Task(subagent="scanner", prompt="Analizza file2.py...")
```

Attende tutti i risultati.

## 4. Riscrittura

Per ogni risultato dello scanner, Claude invoca il rewriter:

```
Task(subagent="rewriter", prompt="Applica le seguenti trasformazioni al file examples/before/sample.py: [mapping JSON]. Usa le occorrenze trovate: {...}")
```

## 5. Validazione

Dopo la riscrittura, Claude invoca il validator su ogni file modificato:

```
Task(subagent="validator", prompt="Valida il file examples/before/sample.py (linguaggio Python). Esegui controllo sintattico.")
```

## 6. Sintesi finale

Claude raccoglie tutti i risultati JSON e produce un report riassuntivo per l'utente.

---

**Nota**: Questo flusso è automatico quando usi la skill. Non devi scrivere manualmente i comandi `Task`; Claude li genera in base alle istruzioni della skill.
