---
title: "Was ist SSTI-Schwachstelle?"
date: 2025-01-15 12:00:00 +0300
lang: de
slug: ssti-nedir
---

# Was ist SSTI-Schwachstelle?

Heutzutage verwenden die meisten Websites dynamische Webseiten. Dynamische Seiten generieren Inhalte serverseitig (server-side) oder clientseitig (client-side) entsprechend dem Benutzer. Während dieses Generierungsprozesses kommen Template-Engines ins Spiel. Server-seitige Angriffe zielen auf eine Anwendung oder einen Dienst ab, der von einem Server bereitgestellt wird, während Client-seitige Angriffe auf dem Computer des Clients auftreten, nicht auf dem Server selbst. Wo und auf welcher Seite der Inhalt generiert wird, zeigt den grundlegenden Unterschied zwischen SSTI- und CSTI-Schwachstellen auf.

Bei SSTI-Schwachstellen wird der Inhalt, wie oben erwähnt, von einer Template-Engine gerendert, die serverseitig läuft, und die Ausgabe wird als HTML an den Client gesendet. Wenn Eingaben ohne ausreichende Filterung direkt an die Template-Engine übergeben werden, können diese Ausdrücke von der Template-Engine als Template-Ausdrücke (template expressions) oder Funktionsaufrufe interpretiert werden, anstatt als Variablen. Der häufig anzutreffende Ausdruck `{{7*7}}` ist zu einem:

Bekannten Payload geworden, um zu bestimmen, ob die Template-Engine die Eingabe wie vorgesehen als Variable interpretiert oder ob eine Injektion durchgeführt werden kann.

Bei CSTI wird die Template-Verarbeitung im Browser des Benutzers durchgeführt. Viele heute verwendete Frontend-Frameworks können auch Template-Rendering clientseitig durchführen. Daher können CSTI-Schwachstellen durch Benutzereingaben entstehen, die Template-Ausdrücke enthalten.

## Beispiel für sicheren Code

Zum Beispiel ein sicheres Template-Beispiel in jinja2:

![Beispiel für sicheren Code](/arda.tc/images/ssti-nedir/page_1_img_1.jpeg)

```python
Das an die render()-Funktion gesendete Template "Hello {{name}}" ist ein statischer Wert, die Eingabe
"Arda" wird nur als Wert der Variable namens "name" zugewiesen.
```

Die Ausgabe dieses Codes wird `Hello Arda` sein und der Ausdruck `{{7*7}}` funktioniert hier nicht.

![Ausgabe des sicheren Codes](/arda.tc/images/ssti-nedir/page_1_img_2.jpeg)

## Beispiel für anfälligen Code

Das Beispiel für anfälligen Code ist wie folgt:

![Beispiel für anfälligen Code](/arda.tc/images/ssti-nedir/page_2_img_1.jpeg)

```python
template = "Hello " + user_input
render_template_string(template)
```

In diesem Code ist der gefährliche Teil, dass das Template, das render() erhalten wird, nicht nur `{{7*7}}` sein wird, sondern `"Hello {{7*7}}"`. Dies gibt die Ausgabe als `Hello 49`. Diese und ähnliche Situationen verursachen SSTI-Schwachstellen.

# SSTI-Angriffsmethodik

Die Existenz dieser Schwachstelle im Zielsystem wird offenbart, wenn wir Fehlercodes interpretieren oder ob die von uns gesendete Eingabe gerendert wird. Verschiedene Template-Engines können leicht unterschiedliche Syntaxen verwenden.

## SSTI-Erkennung

Der Prozess zur Erkennung von SSTI ähnelt der Erkennung anderer Injektionen. Um eine Fehlermeldung auf der anderen Seite zu erstellen oder zu sehen, welche Sonderzeichen gerendert werden:

```
${{<%[%'"}}\.
```

Wir geben diesen Payload als Eingabe. Dies ähnelt dem Brechen der SQL-Abfragesyntax und dem Auftreten eines Fehlers durch Eingabe eines einfachen Anführungszeichens (') bei SQL-Injektionserkennungen. Nachdem ich diesen Payload gegeben habe, erwarte ich entweder einen Fehler und versuche, Informationen darüber zu erhalten, ob eine Template-Injektion vorliegt, und wenn ja, welche Template-Art verwendet wird, oder ich setze einen Marker in einen bestimmten Teil, zum Beispiel arda:

```
${{<%[arda%'"}}\.
```

Auf diese Weise schauen wir, wo diese Template die Ausgabe auf der Seite schreibt, und sehen, welche Sonderzeichen gerendert wurden, und in diese Richtung versuchen wir zu verstehen, welche Template-Engine verwendet wurde.

Wenn wir die von uns gegebene Eingabe und die Ausgabe vergleichen, sehen wir, dass die Sonderzeichen `<%` fehlen.

![SSTI-Erkennungsbeispiel](/arda.tc/images/ssti-nedir/page_3_img_1.jpeg)

## ANGRIFFSSZENARIO 1

Wenn wir dieses Verhalten im Internet recherchieren (book.hacktricks.wiki wird empfohlen und kann verwendet werden), sehen wir, dass es mit häufig verwendeten Template-Engines wie ERB (Ruby), Mako (Python) zusammenhängt.

Wenn wir versuchen, die passwd-Datei mit ERB als Beispiel zu lesen:

```erb
<%= system('cat /etc/passwd') %>
```

![ERB-Angriffsbeispiel](/arda.tc/images/ssti-nedir/page_3_img_2.jpeg)

Wir sind in diesem System erfolgreich. Wenn wir nicht erfolgreich gewesen wären, würden wir andere Template-Engines ausprobieren, die (`<%`) verwenden, oder wenn wir sicher sind, dass ERB-Template in diesem System verwendet wird und wir denken, dass es eine Schwachstelle gibt, denken wir, dass der Zugriff auf Befehlsausführungsfunktionen im System blockiert ist. Dank Ruby und anderen OOP-Sprachen können wir jedoch verschiedene Wege ausprobieren, da in OOP alles ein Objekt ist. Unser Denkweise ist also, dass jedes Objekt eine Klasse hat, wir können auf Methoden zugreifen, die von dieser Klasse kommen, und mit einigen Methoden können wir andere Klassen und Methoden erreichen.

Wir können es als Kette wie `Object → Class → Method → Execute` denken.

## ANGRIFFSSZENARIO 2

Nachdem wir verstanden haben, dass es eine Template-Injektion im System gibt:

Zuerst schreiben wir `<%= "arda".class %>` und sehen seine Ausgabe, dies ist der erste Schritt. Da wir wissen, wo wir uns jetzt befinden und dass jede Klasse in Ruby von einer anderen Klasse abgeleitet ist, ist dies die erste Stufe der Kette. Danach werden wir zu einer übergeordneten Klasse aufsteigen.

![Angriffsszenario 2 - Schritt 1](/arda.tc/images/ssti-nedir/page_4_img_1.jpeg)

In der anderen Stufe werden wir zur Superklasse aufsteigen, wenn wir `<%= "arda".class.superclass %>` schreiben, erhalten wir die Ausgabe `Object`. Die Object-Klasse ist die grundlegendste Klasse in Ruby und enthält viele Methoden, die für uns nützlich sein können.

![Angriffsszenario 2 - Schritt 2](/arda.tc/images/ssti-nedir/page_4_img_2.jpeg)

In der Methodenstufe verwenden wir die Eingabe `<%= Object.methods %>`, um die Methoden zu sehen. Hier erhalten wir eine lange Methodenausgabe.

Besonders die oben von mir unterstrichenen Methoden sind leistungsstarke Methoden zum Ausführen von Befehlen und zum Durchführen von RCE:

- `:send`
- `:__send__`
- `:instance_eval`
- `:instance_exec`

Wir können versuchen, die passwd-Datei mit den von oben gesammelten Informationen zu lesen:

```erb
<%= Object.const_get("File").read("/etc/passwd") %>
```

![Angriffsszenario 2 - Finale](/arda.tc/images/ssti-nedir/page_4_img_3.jpeg)

Wenn wir die passwd-Datei nicht direkt als `<%= system('cat /etc/passwd') %>` lesen konnten, gingen wir durch das Szenario und lasen sie mit dem Payload, den wir am Ende verwendet haben.

---

> **Hinweis**: Dieser Artikel wurde aus PDF-Inhalten konvertiert. Klicken Sie [hier](/arda.tc/pdfs/ssti-nedir.pdf) für die ursprüngliche PDF-Datei.

