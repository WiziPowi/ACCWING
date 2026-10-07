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
  ECRAN DE BARRE (tactile, mer / Garmin)  -  HELM SCREEN
================================================================
La page s'ouvre sur l'ecran BARRE : vue de dessus (bateau, 4 ailes
a leur angle reel, vent reel / apparent, poussee, optimum en
pointilles), 6 grands chiffres et de gros boutons.
  - MODE : MANUEL / AUTO / DRAPEAU (ailes dans le vent, sans poussee).
  - ANGLE AILES et CAMBRURE : boutons - / + (maintenir = repetition).
  - REGLAGE RAPIDE : A PLAT, OPTIMUM (applique l'optimum une fois).
  - RIS : PLEIN / 1 RIS / 2 RIS / AFFALER.
Bouton INGENIERIE (en haut) : l'ancienne page complete (moteur, IMU,
vues 2D/3D, polaire). Maintenir 1 s pour y aller. Pour revenir : le
bouton BARRE (fleche retour, seul bouton colore de l'en-tete) ou le
geste RETOUR du telephone / navigateur. Apres un redemarrage la page
s'ouvre toujours sur la BARRE.

Reglage aile par aile : selecteur TOUTES / 1 / 2 / 3 / 4 (a gauche
de la vue de dessus sur la page Barre, sous COACH/AUTO/PRO sur la page
Ingenierie ; toucher une aile sur la vue la selectionne aussi).
Tous les boutons (mode, angle, cambrure, reglage rapide, ris)
agissent sur la ou les ailes selectionnees ; avec TOUTES, - / +
decalent chaque aile de la meme valeur. Chaque aile a son propre mode
(ex. 3 ailes en AUTO, 1 en DRAPEAU), son angle, sa cambrure et son ris ;
la poussee totale est la somme des 4 ailes.
  1 = avant babord, 2 = avant tribord, 3 = arriere babord,
  4 = arriere tribord. Le moteur du banc pilote le cambreur 1 de l'aile 1.
Limite : l'interaction entre ailes (sillage) n'est pas modelisee.

Per-wing control: ALL / 1 / 2 / 3 / 4 selector; every button acts on
the selected wing(s). Each wing has its own mode, angle, camber and
reef; total thrust is the sum of the four. Wing-to-wing wake effects
are not modelled.

Reglages AUTO - hysteresis (page Ingenierie, colonne Controles, sous
"Prise de ris") ; curseur + boutons - / + pour chaque seuil :
  - Seuil cambrure (defaut 2,5 %) : AUTO n'adopte une nouvelle
    cambrure optimale que si elle s'ecarte de plus de ce seuil de la
    cambrure appliquee (l'optimum est calcule par pas de 1 %).
  - Seuil angle aile (defaut 5 deg) : idem pour l'angle de l'aile.
  - Portant : entree au-dela de 130 deg, sortie en deca de 120 deg de
    vent apparent (indication MODE VOILE) ; l'entree reste toujours au
    moins 2 deg au-dessus de la sortie.
  - En direct : optimum calcule / optimum applique par AUTO.
  - VALEURS PAR DEFAUT remet les valeurs d'origine (CONFIG.opt et
    CONFIG.modes dans le code).
Les reglages sont memorises par le navigateur de l'ecran (Jetson) :
lancer Chromium avec un profil persistant (pas en navigation privee /
--incognito), sinon ils reviennent aux valeurs par defaut a chaque
demarrage.

AUTO tuning - hysteresis (Engineering page, Controls column, below
Reefing): camber dead band (2.5 %), wing angle dead band (5 deg),
downwind on beyond 130 deg / off below 120 deg apparent wind (kept at
least 2 deg apart), live computed vs applied optimum, DEFAULT VALUES.
Saved by the screen's browser: run Chromium on the Jetson with a
persistent profile (not incognito) or they reset at every start.

Securites tactiles :
  - Actions qui font bouger l'aile = MAINTENIR 1 s : AUTO (activation),
    ris / affaler, armer le moteur, aller a la page Ingenierie.
  - Les touches tres breves (gouttes, embruns) et a plusieurs doigts
    sont ignorees (CONFIG.helm.minTouchMs = 40 ms).
  - VERROU : bloque tout l'ecran sauf l'ARRET D'URGENCE ;
    deverrouiller = maintenir 1,5 s.
  - AIDE : touchez ensuite n'importe quel element pour savoir a quoi
    il sert (remplace les info-bulles, inutilisables au doigt).
ARRET D'URGENCE : toujours en haut a droite, sur toutes les pages.
Un toucher coupe le moteur ; REARMER = maintenir 1,5 s.
Affichage : JOUR (contraste maximal au soleil) -> NUIT -> NUIT ROUGE
(vision de nuit) ; attenuation 100/75/50/30 % la nuit.
Alarmes (bandeau + bip, bouton ACQUITTER) : surchauffe / defaut /
perte de liaison moteur, perte IMU, vent apparent >= 25 nds
(CONFIG.helm.windAlarmKt). Vue 3D : FLUIDE / ECO / PAUSE (bouton dans
le panneau 3D) pour economiser le processeur.

A FAIRE COTE BATEAU (hors de ce fichier) :
  - Garmin n'ouvre pas un fichier HTML : la page doit etre servie par
    un boitier a bord (Raspberry Pi / controleur ACCWing) sur le reseau
    Garmin, via le programme OneHelm (HTML5, decouverte mDNS + UPnP ;
    partenariat Garmin a prevoir).
  - Le navigateur du traceur n'a pas Web Serial : le pilotage moteur /
    IMU doit passer dans ce boitier ; la page lui enverra les ordres.
  - Vent et vitesse viendront du NMEA 2000 (puce DONNEES = SIMULATION
    tant que ce n'est pas branche).
  - Securite perte de liaison : le controleur doit mettre les ailes en
    drapeau seul si l'ecran ne repond plus (chien de garde). L'ecran
    ne peut pas le garantir.

The page opens on the HELM screen (big numbers, big buttons, top
view of the wings). ENGINEERING (hold 1 s) is the former full page;
back with the coloured HELM button (back arrow) or the phone/browser
BACK gesture. A restart always opens on the HELM page.
Wing-moving actions need a 1 s hold; very short / multi-finger
touches are ignored; LOCK leaves only the EMERGENCY STOP live;
HELP explains any item you tap; DAY / NIGHT / RED NIGHT themes.
On a Garmin plotter the page must be served by an onboard box
(OneHelm), which also has to drive the motors (no Web Serial on the
plotter), read NMEA 2000 and feather the wings on link loss.

================================================================
  SECURITE (moteur, cybersecurite)  -  SAFETY / SECURITY
================================================================
Regles du pilote moteur (banc) :
  - ARRET D'URGENCE verrouille : il reste actif apres une
    deconnexion / reconnexion ; seul REARMER (maintenir 1,5 s) l'efface.
  - Armer exige un moteur qui repond (telemetrie < 1 s), sans defaut
    ni surchauffe (>= 70 degC, CONFIG.helm.motorCritC).
  - Desarmement automatique : plus de telemetrie pendant 1 s, defaut
    moteur, surchauffe, perte de liaison (une trame d'arret est tentee
    puis le port est ferme), changement de limite pendant le pilotage.
  - Mode Position : aucun ordre n'est envoye avant d'armer ; l'armement
    part de l'angle mesure du moteur (pas de saut vers 0 deg) ; armement
    Camber refuse si le moteur est loin de la consigne ; "Zero position"
    ne refait pas le trajet.
  - Le champ Limite peut baisser la limite, jamais depasser celle du
    code (MODE_DEFAULTS : 100 %, 10 A, 50000 ERPM, 3500 deg).
  - Valeur non numerique / infinie : la trame n'est pas envoyee. L'arret
    d'urgence passe devant les ordres en attente.
Page : aucun script, police ou connexion exterieurs (politique CSP dans
l'en-tete) ; ne parle qu'a son propre dossier / serveur.

A FAIRE COTE BATEAU (cybersecurite, hors de ce fichier) :
  - La securite ne doit pas dependre de l'ecran : limites, chien de
    garde (ailes en drapeau si plus d'ordres) et ARRET D'URGENCE
    CABLE (coupe l'alimentation moteur) dans le controleur. Activer
    aussi la temporisation de commande du firmware moteur si elle existe.
  - Boitier de bord : reseau de commande separe du Wi-Fi invites /
    marina / Internet ; ordres authentifies (appairage, jeton) et
    limites / plausibilite verifiees cote controleur ; en-tetes HTTP
    (CSP + frame-ancestors 'none') ; mises a jour signees ; journal.
  - NMEA 2000 n'a pas d'authentification : controler la plausibilite
    du vent / de la vitesse (bornes, variations) avant de laisser AUTO
    agir.
  - Lanceurs (.bat / .ps1 / .command) : le petit serveur doit ecouter
    sur 127.0.0.1 seulement (jamais sur le reseau du bateau).

Motor bench driver: the e-stop stays latched across reconnects (only
RESET, held 1.5 s, clears it); arming needs live telemetry and no
fault/overheating; telemetry loss (1 s), fault, overheating or link
loss disarm; Position mode never moves before arming and starts from
the measured angle; limits can't exceed MODE_DEFAULTS; invalid numbers
are never sent; stop frames jump the queue. The page loads no outside
code and talks only to where it was served from (CSP).
Boat side: safety must live in the controller (limits, watchdog,
hard-wired e-stop), not the screen; keep the control network apart
from guest/marina Wi-Fi and the Internet; authenticate commands;
sanity-check NMEA 2000 data (no authentication on the bus); signed
updates; the launcher's local server must listen on 127.0.0.1 only.

================================================================
  MOTEUR / WEB SERIAL
================================================================
Le pilotage du moteur (CubeMars AK45-36) necessite un navigateur
Chromium : Chrome, Edge ou Brave (pas Safari ni Firefox). Le lanceur
essaie d'ouvrir Chrome/Edge/Brave en priorite.

Motor control (CubeMars AK45-36) needs a Chromium browser: Chrome,
Edge or Brave (not Safari/Firefox). The launcher opens one if present.
================================================================
