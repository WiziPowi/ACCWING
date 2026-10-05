================================================================
  SIMULATEUR ACCWING / WINDELO  —  COMMENT LANCER
  ACCWING / WINDELO SIMULATOR  —  HOW TO LAUNCH
================================================================

--- IMPORTANT ---------------------------------------------------
Gardez TOUS les fichiers ensemble dans le meme dossier.
Keep ALL files together in the same folder.

  - interface_graphique EO3.html       (la page / the page)
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
  TELEPHONE / TABLETTE  -  PHONE / TABLET
================================================================
Sur telephone, le fichier HTML suffit : pas de lanceur. Le modele
3D y est integre (version allegee).
1. Copiez "interface_graphique EO3.html" sur le telephone
   (Fichiers / Documents, e-mail, AirDrop, WhatsApp...).
2. Ouvrez-le (iPhone : app Fichiers ; Android : ouvrir avec Chrome).
3. Onglets en haut : Controles / Profils 2D / Aile 3D / Systeme.
* Si le modele n'est pas integre, le bouton "Charger le STL..."
  permet de choisir le fichier STL sur le telephone.
* Le pilotage moteur / IMU (Web Serial) reste prevu pour PC.

On a phone the HTML file is enough: no launcher. A lighter copy
of the 3D model is embedded in it. Copy the file to the phone and
open it (iPhone: Files app; Android: open with Chrome). Tabs at
the top: Controls / 2D / 3D / System. If the model is not
embedded, "Charger le STL..." lets you pick the STL on the phone.
Motor / IMU control (Web Serial) is still meant for a PC.

Mettre a jour le modele integre / update the embedded model
(python3 + pip install numpy fast-simplification) :
    python3 tools/embed_stl.py "3D Windelo pour IHM test.stl"
    (option --tris 60000 pour plus de detail / for more detail)

================================================================
  MOTEUR / WEB SERIAL
================================================================
Le pilotage du moteur (CubeMars AK45-36) necessite un navigateur
Chromium : Chrome, Edge ou Brave (pas Safari ni Firefox). Le lanceur
essaie d'ouvrir Chrome/Edge/Brave en priorite.

Motor control (CubeMars AK45-36) needs a Chromium browser: Chrome,
Edge or Brave (not Safari/Firefox). The launcher opens one if present.
================================================================
