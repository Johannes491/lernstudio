# Vorlesungs-Lernstudio

Aus Vorlesungsfolien werden Anki-Karteikarten und Übungsquizze.

**Zur Seite: https://johannes491.github.io/lernstudio/**

## Was es kann

- **Karteikarten:** liest PDF, PowerPoint (.pptx), Word (.docx) und Text. Claude schreibt daraus Karten (Frage – Antwort, Umkehrkarten, Lückentext) mit Folienangabe. Ein zweiter Durchgang sucht Lücken und Dubletten. Der Export ist eine `.apkg`-Datei mit Unterdeck, Schlagwörtern und auf Wunsch dem Folienbild auf der Rückseite.
- **Quiz:** Wahr/Falsch, Single Choice, Multiple Choice und offene Fragen, mit Begründung zu jeder Antwortoption. Offene Antworten bewertet Claude nach einem Punkteraster. Falsch beantwortete Fragen lassen sich wiederholen oder als Anki-Karten speichern.
- **Altklausuren:** Pro Fach Altklausuren hochladen (PDF, auch gescannt, Fotos, Word, Text). Claude liest jede Seite auch als Bild, also auch R-Outputs, Grafiken und ausgefüllte Antwortbögen, und erstellt pro Klausur einen Bauplan: Aufgaben, Themen, Formulierungen, Lösungen, Zeit und Bewertung. Klausuren aus einem anderen Fach werden gemeldet und weggelassen.
- **Probeklausuren:** folgen einer gewählten Altklausur oder einem jedes Mal neu gemischten Mix aus allen. Themen und Aufgabenarten bleiben gleich, Aussagen und Zahlen sind neu. Aufgaben mit mehreren Aussagen (a–e, keine bis alle richtig) werden wie in der Klausur Aussage für Aussage bewertet, mit Zeitlimit und Punktabzug wie im Original.
- **Formel-Modus:** jede Formel als eigene Karte plus Rechenbeispiel.
- **Schwierige PDFs:** Folien, deren Text beim Auslesen Formeln verliert oder als Zeichensalat ankommt, gehen automatisch als Bild an Claude.
- **Fortsetzen:** Claude arbeitet nur, solange die Seite offen ist. Wird sie mitten in einem Lauf geschlossen, bleibt alles Fertige gespeichert, und „Fortsetzen“ erstellt beim nächsten Öffnen nur den Rest.

Mehr: [Bisherige Schritte](SCHRITTE.md) · [Roadmap](ROADMAP.md)

## Was du brauchst

Einen eigenen API-Schlüssel von Anthropic:

1. Konto in der [Claude Console](https://platform.claude.com) anlegen.
2. Unter [Billing](https://platform.claude.com/settings/billing) Guthaben kaufen und ein Monatslimit setzen.
3. Unter [API Keys](https://platform.claude.com/settings/keys) einen Schlüssel erstellen und auf der Seite einfügen.

Die Kosten rechnet Anthropic direkt mit dir ab. Grobe Schätzung für eine Vorlesung mit rund 50 Folien: Karteikarten etwa 0,50–1 $ mit „Gründlich“ (Claude Opus 5.5) oder 0,25–0,50 $ mit „Schnell“ (Claude Sonnet 5.5); ein Quiz mit 15 Fragen etwa 0,15–0,45 $. Die Seite zeigt nach jedem Durchlauf die ungefähren Kosten an.

## Datenschutz

Die Seite hat keinen Server. Alles läuft in deinem Browser:

- Der API-Schlüssel wird nur an `api.anthropic.com` gesendet. Eine Content Security Policy blockiert alle anderen Verbindungen.
- Ohne „Auf diesem Gerät merken“ vergisst der Browser den Schlüssel, wenn du den Tab schließt.
- Material, Karten und Quizze bleiben im Speicher deines Browsers. An Anthropic gehen nur die Inhalte, aus denen Claude Karten und Fragen erstellt.

## Aufbau des Repositorys

| Datei | Inhalt |
|---|---|
| `docs/index.html` | Die öffentliche Seite (wird von GitHub Pages ausgeliefert) |
| `index.html` | Dieselbe App als Artifact für claude.ai, dort über das eigene Claude-Abo |
| `make_site.py` | Erzeugt `docs/index.html` aus `index.html`: `python3 make_site.py` |

Änderungen werden in `index.html` gemacht; danach erzeugt `make_site.py` die öffentliche Seite neu.

Dies ist ein privates Studienprojekt und kein Angebot von Anthropic.
