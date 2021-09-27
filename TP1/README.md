# Travaux pratiques : séance 1

Nous utiliserons l'[interface Python](https://docs.opencv.org/master/d0/de3/tutorial_py_intro.html) d'[OpenCV](https://opencv.org/) pour les travaux pratiques.

## Exercice 1 : manipulations de base


Écrire un programme Python qui :

- lit une image couleur RGB dont le nom est passé sur la ligne de commande
- affiche sur la sortie standard : la taille de l'image, le nombre de canaux, le type des valeurs
- affiche l'image d'entrée et les trois images en niveaux de gris correspondant aux canaux « rouge », « vert », « bleu »
- convertit l'image RGB d'entrée en une image dans l'espace HSV, puis affiche l'image d'entrée et les trois images en niveaux de gris correspondant aux canaux « teinte », « saturation », « valeur »
- écrit une image en niveaux de gris correspondant au canal « valeur »

## Exercice 2 : calcul d'histogramme

Écrire un programme Python qui :

- lit une image couleur RGB dont le nom est passé sur la ligne de commande
- calcule les histogrammes des trois canaux RGB de l'image
- affiche l'image d'entrée et, dans une deuxième fenêtre, la superposition des trois histogrammes, chacun avec leur couleur (rouge, vert, bleu)

## Exercice 3 : égalisation de contraste

Écrire un programme qui :

- lit une image en niveaux de gris passée dont le nom est passé en ligne de commande
- effectue une égalisation de contraste (ou d'histogramme) sur l'image
- affiche l'image avant et après égalisation de contraste, ainsi que l'histogramme de l'image avant et après égalisation

## Exercice 4 : égalisation de contraste sur image RGB

Même programme que l'exercice 3 mais prenant en entrée une image RGB.
Considérer et comparer deux stratégies :

- égalisation d'histogramme indépendante sur chaque canal
- conversion de l'image dans l'espace HSV, puis égalisation de contraste du canal « valeur »

## Exercice 5 : traitement temps réel

Écrire un programme qui capture un flux vidéo en temps réel : vous pourrez par exemple utiliser la webcam de votre ordinateur, ou celle de votre smartphone en utilisant l'application [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=fr&gl=US) puis :

1. convertit l'image RGB en niveau de gris, puis affiche l'image capturée et l'histogramme de l'image dans une seconde figure
2. affiche l'image d'entrée RGB ainsi que les 3 histogrammes (avec leur couleur correspondante) des canaux RGB de l'image  dans une seconde figure.
3. calcule une égalisation de contraste dans l'espace HSV (voir exercice précédent) et affiche l'image avant et après traitement.

