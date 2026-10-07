MENNO v0.1
==========

Doel van deze versie
--------------------
Dit is de eerste lichte lokale basis van Menno.

Hij heeft:
- een altijd-zichtbare rode noodstop/afsluitknop
- globale 3x ESC noodstop
- schermresolutie uitlezen
- cursorpositie uitlezen
- een veilige cursor-test naar het midden van het scherm
- een aparte SafetyCore die niet afhankelijk is van een AI-API

Installatie op Windows
----------------------
1. Open deze map in Verkenner.
2. Open een terminal in deze map.
3. Maak eventueel een virtuele omgeving:

   python -m venv .venv

4. Activeer deze:

   .venv\Scripts\activate

5. Installeer de kleine dependencies:

   python -m pip install -r requirements.txt

6. Start:

   python main.py

Noodstop
--------
Druk overal in Windows 3 keer snel op ESC (binnen 1,5 seconde).

Of klik op:
    MENNO AFSLUITEN / NOODSTOP

Na een noodstop sluit Menno v0.1 zichzelf af en start hij niet automatisch opnieuw.

Belangrijk
----------
Deze versie heeft expres nog GEEN AI-API-koppeling en GEEN vrije toegang tot je computer.
Eerst testen we de lokale veiligheid en cursorlaag.

Later bouwen we hier veilig omheen:
- screenshots
- venster/UI-herkenning
- bestanden
- terminal
- browser
- API-router
- voice
- memory
- taakplanner
- gecontroleerde game-automatisering

Vanuit de AI mag de SafetyCore nooit worden uitgeschakeld.
