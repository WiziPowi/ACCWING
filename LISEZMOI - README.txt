================================================================
  SIMULATEUR ACCWING / WINDELO  —  COMMENT LANCER
  ACCWING / WINDELO SIMULATOR  —  HOW TO LAUNCH
================================================================

--- IMPORTANT ---------------------------------------------------
Gardez TOUS les fichiers ensemble dans le meme dossier.
Keep ALL files together in the same folder.

  - interface_graphique windelo.html   (la page / the page)
  - 3D Windelo pour IHM test.stl        (le modele 3D / the 3D model)
  - Lancer Windelo.bat                  (Windows)
  - windelo_server.ps1                  (Windows, requis par le .bat)
  - Lancer Windelo (Mac).zip            (macOS)

Pourquoi un lanceur ? Le modele 3D (STL) ne se charge PAS si on
ouvre la page directement (file://). Le lanceur demarre un petit
serveur local (http://localhost) : le STL se charge alors tout seul.
Why a launcher? The 3D model won't load if the page is opened
directly (file://). The launcher starts a small local server
(http://localhost) so the STL loads automatically.

================================================================
  WINDOWS
================================================================
1. Double-cliquez :  Lancer Windelo.bat
2. Une petite fenetre "Serveur ACCWing" s'ouvre : LAISSEZ-LA OUVERTE.
3. Le navigateur s'ouvre sur la page, le modele se charge tout seul.
4. Pour arreter : fermez la fenetre du serveur.

Rien a installer (utilise PowerShell, deja present sur Windows).
Nothing to install (uses PowerShell, built into Windows).

================================================================
  macOS
================================================================
1. Double-cliquez :  Lancer Windelo (Mac).zip
   -> cela extrait le fichier "Lancer Windelo.command" (deja executable).
2. Double-cliquez :  Lancer Windelo.command
3. Une fenetre Terminal s'ouvre : LAISSEZ-LA OUVERTE.
   Le navigateur s'ouvre sur la page, le modele se charge tout seul.
4. Pour arreter : fermez la fenetre du Terminal (ou Ctrl+C).

* 1re fois seulement : si macOS affiche "developpeur non identifie",
  faites CLIC DROIT sur "Lancer Windelo.command" > Ouvrir.
* Necessite python3 OU ruby. Sur un Mac sans outils de developpement,
  le script l'indique : lancez une fois  xcode-select --install
  puis relancez.

First time only: if macOS says "unidentified developer", RIGHT-CLICK
"Lancer Windelo.command" > Open. Needs python3 or ruby; if missing,
run once:  xcode-select --install  then try again.

================================================================
  MOTEUR / WEB SERIAL
================================================================
Le pilotage du moteur (CubeMars AK45-36) necessite un navigateur
Chromium : Chrome, Edge ou Brave (pas Safari ni Firefox). Le lanceur
essaie d'ouvrir Chrome/Edge/Brave en priorite.

Motor control (CubeMars AK45-36) needs a Chromium browser: Chrome,
Edge or Brave (not Safari/Firefox). The launcher opens one if present.
================================================================
