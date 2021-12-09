# Travaux pratiques : séance 6

L'objectif de ce TP est de créer une image panoramique construite à partir de deux images ou plus acquises en rotation sur un pied. 
On rappelle qu'il existe une transformation homographique $`H`$ entre ces images.


Estimation d'une transformation projective à partir de correspondances imparfaites.

On considérera les images disponibles dans le répertoire `/img`.


On souhaite utiliser les points d’intérêt extraits et mis en correspondance entre les deux images pour calculer H. En utilisant sift (voir TP précédent), vérifier que les correspondances extraites sont bien utilisables. Vous trouverez dans le fichier matchesReduit.txt le fichier des points en cor- respondance extraits: sur chaque ligne les deux premières coordonnées représentent le point m1 de l’image 1 mis en correspondance avec les deux derniers coordonnées représentant le point m2 de l’image 2. Utiliser les fonction de lecture fopne et fscanf pour lire les données et remplir les tableaux p1 et p2 contenant les points d’intérêt des images 1 et 2.
En utilisant la fonction ransacfithomography, calculer l’homographie H transformant au mieux l’ensemble des points d’intérêt de l’image 1 sur l’ensemble des points d’intérêt de l’image 2.
que représente H−1(I2)?
Construisez maintenant le panoramique c’est a dire l’image contenant I1
et et l’image I transformée par H−1(I )?. Pour limiter la place utilisée, 22
vous construirez l’image panoramique I de taille [r, 2*c] ou [r,c] est la taille d’une des images. Vous placerez I dans la partie gauche de l’image et compléterez les autres points en utilisant I2 si c’est possible. Vous me rendrez le code du programme et l’image panoramique obtenue.


## Exercice 1 : appariement des points d'intérêt de Harris

Dans un premier temps, on souhaite s'appuyer sur le détecteur de coins de Harris pour apparier les points similaires entre deux images.
Pour ce faire, on va associer à chaque point de Harris un descripteur de son voisinage local. Plus précisément, le descripteur associé à un point d'intérêt sera formé par un vecteur contenant les valeurs des pixels dans un voisinage $`n*n`$ autour de ce point.

L'appariement des points selon leur descripteur se fera au plus proche voisin, en utilisant la norme $`L_2`$.

## Appariement 

Écrire un programme qui prend deux images A et B en entrée, calcule les points d'intérêt de Harris en fonction d'un certain nombre de paramètres passés en ligne de commande et affiche les deux images côte à côte avec les appariements calculés sous forme de points reliés par des lignes.

## Calcul d'homographie

Le programme calcule maintenant l'homographie $`H`$ entre les images à partir des points appariés, et affiche les deux images A et H(B) côte à côte.
Vous pourrez vous appuyer sur l'algorithme RANSAC qui permet de calculer une homographie entre deux ensemble de points contenant potentiellement des outliers :

1. Faire :
2. Tirage aléatoire de quatre couples de points appariés (ensemble A vers ensemble B)
3. Calcul d'une homographie H' à partir de ces points
4. Transformation des points de l'ensemble B par l'homographie H'
5. Calcul de la distance moyenne entre les points A et H'(B)
6. Tant que cette distance est supérieure à un seuil $`\epsilon`$


## Assemblage des images

Le programme final assemble maintenant les deux images obtenues et affiche le résultat

## Exercice 2 : assemblage d'image à partir de SIFT et ORB

Les descripteurs calculés précédemment ont un problème important : ils sont peu robustes, et en particuliers pas invariants à la rotation et au changement d'échelle.
Les descripteurs codés dans SIFT sont plus robustes, car ils sont invariants à un certain nombre de transformations. 

En vous appuyant sur les documentations https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html et https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html , écrire un programme permettant d'assembler deux images ou plus en vous appuyant sur les descripteurs SIFT puis ORB.



