# Prüfung vor Lamborghini realistic v2

**Status: technisch blockiert; kein neuer 3-Sekunden-Test gerendert.**
`preview/lamborghini-realistic-v2.mp4` wurde nicht erstellt. Die bisherige statische Methode wird nicht erneut als Verbesserung ausgegeben. Originalvideo und bisherige Projekte bleiben unverändert.

## Umfang und Belege

292 Originalframes und alle 60 Frames des vorhandenen v1-Tests wurden dekodiert und automatisch je Frame protokolliert. Alle 60 v1-Frames wurden in vier Vergleichstafeln ihrem Originalframe gegenübergestellt und visuell geprüft. Das ist keine Behauptung, dass alle 292 Originalframes in voller Auflösung manuell retuschiert oder visuell abgenommen wurden.

- [Vergleich 1: v1-Frames 0–14](comparison-1.jpg)
- [Vergleich 2: v1-Frames 15–29](comparison-2.jpg)
- [Vergleich 3: v1-Frames 30–44](comparison-3.jpg)
- [Vergleich 4: v1-Frames 45–59](comparison-4.jpg)
- `original-frame-checks.csv`, `composite-frame-checks.csv`, `checks.json`: technische Einzelbildprotokolle und Dateiprüfsummen; keine objektiven Fotorealismus-Scores.

## Konkrete Fehler

| Bereich | Befund | Erforderliche Korrektur |
| --- | --- | --- |
| Perspektive/Kamera | Niedrige, aufwärts gerichtete Ausgangskamera. Die generierte Kabine wurde nach Beschreibung geschätzt; Brennweite, 3D-Sitzposition und Kamerahöhe wurden nicht kalibriert. Kopfstütze und Körper sind deshalb nur grob passend. | An die Quelle angepasste Kamera und echte/validierte Kabinengeometrie oder passende Referenzaufnahme; kein nachträgliches Verziehen des Menschen. |
| Körperhaltung | Körper lehnt seitlich und stützt sich am Tisch ab. Ein Sitzbild allein erklärt diese Abstützung nicht. | Sitz, Armauflage und ihre Tiefe passend zur vorhandenen Körperhaltung modellieren. |
| Konturen | In den Vergleichsframes sind helle Haar-/Schulterränder und teils graue Stuhlreste erkennbar. Randentfärbung aus angenommener Wandfarbe ist keine belastbare Rekonstruktion. | Zeitlich geführte Rotoskopie mit manuellen Korrekturen und sauberer Edge-Decontamination, Originalperson als separate Ebene. |
| Hände/Dose | v1-Frames etwa 43–59, Original etwa 3,93–4,47 s: bewegte Dose und Finger zeigen die Grenzen der Masken. Farbbasierte Reparaturen sind räumlich begrenzt und berücksichtigen weder Objekttiefe noch vollständigen Bewegungsblur. | Person, Hände und Dose separat verfolgen; richtige Löcher, Bewegungsunschärfe und Verdeckungsreihenfolge erhalten. |
| Sitzkontakt/Überdeckung | Die Vordergrundarmlehne ist ein statisch ausgeschnittenes Stück desselben Fotos. Die Körperunterkante wird durch eine feste Polygonkante verdeckt; die Hand wird mit einem weiteren festen Ausschnitt darübergelegt. Das ist keine körperbezogene Sitzverdeckung. | Tiefenabhängige Sitz-/Armlehnen-Layer, korrekte Kontaktstellen und bewegungsabhängige Verdeckung. Hinter dem Tisch fehlen tatsächlich aufgenommene Körperpixel. |
| Licht/Schatten | Die Person behält die diffuse Raumbeleuchtung, während die Kulisse Seitenfenster und dunkles Leder zeigt. Der angewendete 2D-Drop-Shadow folgt der Silhouette statt einer Sitzoberfläche. | Kabinenbeleuchtung passend zur Originalperson; geometrisch begründete Kontakt-/Okklusionsschatten. Kein Diffusions-Relighting des Gesichts. |
| Hintergrundbewegung | Die Kulisse bleibt statisch. Für ein geparktes Auto ist das grundsätzlich sinnvoll. Es fehlen jedoch korrekt gekoppelte Interaktionen; künstliche Fahrbewegung würde weitere Fehler erzeugen. | Kamerabewegung nur bei nachgewiesener Bewegung der Originalkamera übernehmen; keine erfundene Parallaxe. |
| Schärfe/Körnung | Die generierte Kabine hat sichtbar saubere Materialdetails und hohen Kontrast; die Person stammt aus stärker komprimierter, weicherer Handy-/TikTok-Aufnahme. | Nach Lösung von Geometrie und Masken die reale Schärfe-/Rauschcharakteristik messen und anpassen. Unschärfe oder Grain allein beheben keine Geometriefehler. |
| Urus-Modelltreue | Die KI-Kabine ist nicht als exakte Urus-Geometrie verifiziert. | Verifizierte Referenzen oder ein passend lizenziertes, authentisches 3D-Modell. |

## Erneute Prüfung der Verarbeitung

- Lokale Ausführung: CPU-Quota 4 Kerne, 32 GiB RAM, keine nachgewiesene NVIDIA-/CUDA-GPU. ONNX Runtime bietet CPU und AzureExecutionProvider; Letzterer ist kein Nachweis eines verbundenen Azure-GPU-Backends.
- Verfügbare verbundene Werkzeuge: Bildgenerierung, keine Video-to-Video-/Video-Inpainting-Schnittstelle und kein verbundener GPU-Runner.
- Konfigurationsmetadaten enthalten keine Dienst-Secrets. Relevante Prozessvariablen für Fal, Replicate, Runway und Hugging Face sind nicht gesetzt. Das allein beweist nicht die weltweite Nichterreichbarkeit dieser Dienste; es fehlt hier eine nutzbare, konfigurierte Verarbeitungsschnittstelle. Es wurden keine kostenpflichtigen Jobs gestartet oder Dateien an einen solchen Dienst übertragen.
- Die offiziellen SAM-2-Tiny-, VideoPainter- und CogVideoX-Endpunkte wurden außerhalb der lokalen Sandbox lesend erneut geprüft. Alle drei Anfragen endeten am Proxy mit `403 Forbidden`.
- Robust Video Matting läuft bereits, seine vorhandene automatische Matte reicht jedoch nicht. SAM 2 wäre eine Hilfe für Objektmasken, keine alleinige Garantie für weiche Haarkanten oder überzeugende Sitzgeometrie.
- ProPainter ist keine semantische Lamborghini-Kabinengenerierung. CPU-Fähigkeit dieses Tools löst die eigentliche Aufgabe nicht.

## Konkrete fehlende Voraussetzung

Benötigt wird eine innerhalb dieser Arbeitsumgebung erreichbare **GPU-Verarbeitung für maskiertes Video-Inpainting**, mit freigegebenem Zugriff auf die erforderlichen Modellgewichte, plus korrigierbare zeitliche Masken und eine perspektivisch geprüfte Kabinenvorlage/Geometrie. Eine mögliche Open-Source-Basis ist [TencentARC VideoPainter](https://github.com/TencentARC/VideoPainter) mit CogVideoX-5B-I2V und SAM 2 für Objektmasken. Modellgröße, Hardware und Lizenzbedingungen müssen zur konkret gewählten Variante passen; bloßes Freischalten einer Domain garantiert keine lauffähige Pipeline oder Fotorealismus.

Ein freigegebener GPU-Runner könnte von Codex aus gesteuert werden, ohne dass der Nutzer selbst ein Schnittprogramm bedienen muss. Er ist derzeit aber nicht verbunden. Auch ein pauschaler Video-to-Video-API-Zugang reicht nicht: Er muss maskierte Verarbeitung ermöglichen und das unveränderte Originalsubjekt in einem anschließenden Compositing erlauben.

Sobald diese Voraussetzung besteht: zuerst drei Sekunden der Originalquelle bei unverändertem Timing maskieren, nur die Umgebung bearbeiten, die echte Person inklusive Lippen/Händen/Dose wieder einsetzen, Sitzkontakte prüfen, mit dem vorhandenen v1 vergleichen und erst bei deutlicher Verbesserung in Remotion exportieren. Ein generiertes Gesicht ist ausgeschlossen. Remotion bleibt für Timing, Originalton und Export zuständig, ersetzt aber die fehlende Rekonstruktion nicht.

Aktuell kann kein ehrlicher neuer Videolink angegeben werden. Die Analyse dokumentiert den Blocker, statt eine gleichartige Montage als v2 hochzuladen.
