# Vorlesungs-Lernstudio

Aus Vorlesungsfolien werden Anki-Karteikarten und Übungsquizze.

**Zur Seite: https://johannes491.github.io/lernstudio/**

## Was es kann

- **Karteikarten:** liest PDF, PowerPoint (.pptx), Word (.docx), Text und Transkripte von Vorlesungsaufzeichnungen (.vtt, .srt, z. B. aus Panopto, Zoom oder Teams; Karten nennen dann die Minute). Claude schreibt daraus Karten (Frage – Antwort, Umkehrkarten, Lückentext) mit Folienangabe. Ein zweiter Durchgang sucht Lücken und Dubletten. Der Export ist eine `.apkg`-Datei mit Unterdeck, Schlagwörtern und auf Wunsch dem Folienbild auf der Rückseite.
- **Quiz:** Wahr/Falsch, Single Choice, Multiple Choice und offene Fragen, mit Begründung zu jeder Antwortoption. Das Quiz beginnt mit der ersten fertigen Frage, die übrigen kommen beim Beantworten dazu. Offene Antworten bewertet Claude nach einem Punkteraster, im Klausurmodus schon beim Weiterblättern. Falsch beantwortete Fragen lassen sich wiederholen oder als Anki-Karten speichern.
- **Altklausuren:** Pro Fach Altklausuren hochladen (PDF, auch gescannt, Fotos, Word, Text). Claude liest jede Seite auch als Bild, also auch R-Outputs, Grafiken und ausgefüllte Antwortbögen, und erstellt pro Klausur einen Bauplan: Aufgaben, Themen, Formulierungen, Lösungen, Zeit und Bewertung. Klausuren aus einem anderen Fach werden gemeldet und weggelassen.
- **Probeklausuren:** folgen einer gewählten Altklausur oder einem jedes Mal neu gemischten Mix aus allen. Themen und Aufgabenarten bleiben gleich, Aussagen und Zahlen sind neu. Aufgaben mit mehreren Aussagen (a–e, keine bis alle richtig) werden wie in der Klausur Aussage für Aussage bewertet, mit Zeitlimit und Punktabzug wie im Original.
- **Formel-Modus:** jede Formel als eigene Karte plus Rechenbeispiel.
- **Bildverdeckung:** Bei beschrifteten Diagrammen in PDFs schlägt Claude eine Bildverdeckungskarte vor (braucht „Folienbilder an Claude mitsenden“). Jede verdeckte Beschriftung wird eine eigene Anki-Karte: vorne die Folie mit der gefragten Stelle rot, die anderen gelb, hinten die Stelle aufgedeckt. Im Editor verdeckst du per Klick weitere Texte oder ziehst eigene Flächen auf.
- **Schwächen-Training:** Jede Quizantwort wird gespeichert. Falsch beantwortete Fragen kommen in eine Wiederholungsbox und kehren nach 1, 3, 7, 14 und 30 Tagen zurück; die schwächsten Themen pro Kurs lassen sich gezielt abfragen.
- **Lernplan:** Klausurtermin, Lerntage, Minuten pro Tag und die Vorlesungen (gern mit Datum) eintragen. Der Plan verteilt neuen Stoff, Wiederholungen nach 1, 3, 7, 14 und 30 Tagen, eine Gesamtwiederholung und Probeklausuren bis zur Klausur, warnt bei zu knappem Zeitbudget und lässt sich als Kalender (.ics) speichern.
- **Eigene Decks:** Vorhandene Anki-Decks (.apkg) hochladen. Neue Karten, die es dort schon gibt, werden markiert; auf Wunsch übernimmt Claude den Stil dieser Decks. Exporte werden pro Kurs festgehalten, und „Nur neue Karten“ exportiert nur, was noch fehlt.
- **Direkt nach Anki** (nur Website): mit dem Add-on AnkiConnect landen die Karten ohne Datei direkt in Anki.
- **Folienauswahl:** „Nur diese Folien“ (z. B. 1–16) oder eine Angabe in den Anforderungen wie „nur die ersten 16 Folien“ gilt verbindlich für Karten, Lückensuche und Quiz.
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
