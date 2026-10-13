
 SIMULATEUR DE COMMUNICATION NUMERIQUE
 Numérisation d'un signal : échantillonnage, quantification, codage



1. PRESENTATION
Ce projet simule la numérisation d'un signal analogique 
et sa transmission sous forme de bits.

Un signal analogique contient une quantité infinie d'amplitudes. Un
ordinateur ne sait manipuler qu'un nombre fini de valeurs (des 0 et des
1). La numérisation transforme donc le signal en 3 étapes successives :

    Signal analogique
          |
          v
    1. Echantillonnage   -> découpe le TEMPS
          |
          v
    2. Quantification    -> découpe les VALEURS (amplitudes)
          |
          v
    3. Codage binaire    -> écrit chaque valeur avec des 0 et des 1
          |
          v
    Séquence binaire (ex. 100 110 111 110 ...)

L'ordre est obligatoire : on ne peut pas quantifier sans échantillons,
et on ne peut pas coder sans un nombre fini de valeurs possibles.


2. PARAMETRES DE L'EXEMPLE

    Fréquence du signal        f   = 5 Hz
    Fréquence d'échantillonnage fe = 40 Hz
    Durée                          = 1 s
    Nombre de bits             Nb  = 3
    Amplitude                      de -1 V à +1 V


3. ETAPE 1 : L'ECHANTILLONNAGE            (fichier B-sampler.py)

3.1 Principe
    L'échantillonnage consiste à prélever la valeur du signal à des
    intervalles de temps réguliers. Il produit une suite de valeurs
    discrètes (une liste de nombres) à la place d'une courbe continue.

3.2 Formules
    Te = 1 / fe          Te : période d'échantillonnage (en secondes)
    fe = 1 / Te          fe : fréquence d'échantillonnage (en Hz)
    t(n) = n x Te        instant de la n-ième mesure
    Nombre d'échantillons = fe x durée

3.3 Application numérique
    Te = 1 / 40 = 0,025 s    (une mesure toutes les 0,025 s)
    Nombre d'échantillons = 40 x 1 = 40
    Echantillon n = 1 : x = sin(2 x pi x 5 x 0,025) = sin(45°) = 0,707
    Valeurs obtenues : 0 ; 0,707 ; 1 ; 0,707 ; 0 ; -0,707 ; -1 ; ...

3.4 Choix de fe : théorème de Shannon
    Pour pouvoir reconstruire le signal, il faut :

        fe > 2 x f(max)

    Ici : 40 > 2 x 5 = 10  (condition respectée, 8 échantillons par
    période).
    - fe grande : signal fidèle, mais beaucoup de données à stocker.
    - fe trop petite : on perd des détails et le signal est déformé
      (sous-échantillonnage). Essayer SAMPLING_RATE = 8 pour le voir.


4. ETAPE 2 : LA QUANTIFICATION            (fichier C-quantizer.py)

4.1 Problème à résoudre
    Après l'échantillonnage, le temps est discret, mais chaque valeur
    peut encore être n'importe quel nombre (0,707 ; 0,70711 ; ...), soit
    une infinité de possibilités. On ne peut pas les écrire avec un
    nombre fini de bits.

4.2 Principe
    On divise l'intervalle [Vmin ; Vmax] en L zones de même largeur.
    Chaque échantillon est ramené à la valeur du MILIEU de sa zone.
    Chaque zone reçoit un numéro de 0 à L-1.

4.3 Formules
    L = 2^Nb                         nombre de zones (niveaux)
    delta = (Vmax - Vmin) / L        pas de quantification
    zone  = partie entière de ((x - Vmin) / delta), limitée à 0..L-1
    valeur quantifiée = Vmin + (zone + 0,5) x delta

4.4 Application numérique (Nb = 3, de -1 V à +1 V)
    L = 2^3 = 8 zones
    delta = (1 - (-1)) / 8 = 0,25 V

    Exemple avec x = 0,707 :
      (0,707 + 1) / 0,25 = 6,83     -> zone 6
      valeur quantifiée = -1 + (6 + 0,5) x 0,25 = 0,625

    Remarque : x = +1 donne (1 + 1) / 0,25 = 8, mais les zones vont de
    0 à 7. On limite donc à 7 (c'est le rôle de np.clip dans le code).

4.5 Exemple du cours (de -20 V à +20 V, L = 8)
    delta = (20 - (-20)) / 8 = 5 V
    Les 8 zones : -20 à -15, -15 à -10, -10 à -5, -5 à 0, 0 à 5, 5 à 10,
    10 à 15, 15 à 20.
    Echantillon -6 V : (-6 + 20) / 5 = 2,8 -> zone 2 -> valeur -7,5 V

4.6 Erreur de quantification
    La quantification est la seule étape qui PERD de l'information.
    L'erreur maximale est de delta / 2 (ici 0,125 V). Elle diminue quand
    on augmente le nombre de bits (donc L), mais le débit augmente.


5. ETAPE 3 : LE CODAGE BINAIRE        (fichier D-binary_encoder.py)

5.1 Principe
    Chaque zone (donc chaque valeur quantifiée) reçoit un code binaire.
    On écrit simplement le numéro de la zone en binaire.

5.2 Formules
    Nb = log2(L)                nombre de bits par échantillon
    Débit = fe x Nb             en bit/s

5.3 Application numérique
    Nb = log2(8) = 3 bits par échantillon
    Les 8 codes : 000, 001, 010, 011, 100, 101, 110, 111
    Débit = 40 x 3 = 120 bit/s

5.4 Exemple de résultat
    Echantillon   Valeur    Zone   Quantifiée   Code
        0          0,000     4      +0,125       100
        1          0,707     6      +0,625       110
        2          1,000     7      +0,875       111
        3          0,707     6      +0,625       110
        4          0,000     4      +0,125       100
        5         -0,707     1      -0,625       001
        6         -1,000     0      -0,875       000

    Séquence transmise : 100 110 111 110 100 001 000 ...


6. RECONSTRUCTION                   (fichier E-signal_reconstructor.py)

Pour vérifier le résultat, on reconstruit le signal en reliant les
valeurs quantifiées par des segments de droite (interpolation
linéaire). L'écart avec le signal d'origine vient de la quantification
et des segments de droite entre les échantillons.


7. ORGANISATION DES FICHIERS (dossier src/)

    A-signal-generator.py       génère le signal analogique
    B-sampler.py                étape 1 : échantillonnage
    C-quantizer.py              étape 2 : quantification
    D-binary_encoder.py         étape 3 : codage binaire
    E-signal_reconstructor.py   reconstruction du signal
    F-visualizer.py             affiche toutes les étapes dans une fenêtre
    G-main.py                   exécute toute la chaîne
    _loader.py                  fichier outil (charge les fichiers
                                ci-dessus, dont le nom contient "-")


8. UTILISATION
Installation :
    pip install numpy matplotlib

Exécution (depuis l'intérieur du dossier src) :
    python A-signal-generator.py       résultat de l'étape signal
    python B-sampler.py                résultat de l'échantillonnage
    python C-quantizer.py              résultat de la quantification
    python D-binary_encoder.py         résultat du codage binaire
    python E-signal_reconstructor.py   résultat de la reconstruction
    python G-main.py                   toutes les étapes ensemble

Les paramètres (fréquence, fe, nombre de bits) se modifient à la fin de
chaque fichier et en haut de G-main.py.


9. A RETENIR

    Echantillonnage  : on découpe le temps         -> Te = 1 / fe
    Quantification   : on découpe les amplitudes   -> delta = (Vmax - Vmin) / L
    Codage binaire   : on écrit en 0 et 1          -> Nb = log2(L)
    Débit            : fe x Nb