# Rapport du TP5 sur les points d'intérêts

## Descripteur Harris

### Robustesse à la rotation

En faisant varier l'angle de rotation, on se rend compte que le descripteur Harris est invariant à la rotation, mise à part les points détectés qui sortent de l'image et ceux qui deviennent détectés pour certains angles.

![0°](Harris/Rotation/harris_0.png)
![270°](Harris/Rotation/harris_270.png)
![45°](Harris/Rotation/harris_45.png)
![135°](Harris/Rotation/harris_135.png)


### Robustesse à la mise à l'échelle

Le descripteur Harris n'est pas solide concernant les changements d'échelles. En effet, si un pixel forme un coin à 50% de l'image de base, alors plusieurs coins seront détectés à 150% par exemple.
![](Scale_Edge.png)

C'est bien ce que j'ai pu remarquer lors de mes tests : 

![](Harris/Scale/harris_0.5.png)
![](Harris/Scale/harris_1.0.png)
![](Harris/Scale/harris_1.5.png)

On voit par exemple que un des côtés du triangle rectangle se remplit de point d'intérêts en grandissant, de même pour la tête de flèche.

## Descripteur My Harris

### Robustesse à la rotation

### Robustesse à la mise à l'échelle

### Robustesse au bruit

## Descripteur Shi-Tomasi

### Robustesse à la rotation

Tout comme Harris, Shi-Tomasi est invariant à la rotation : 

![](Shi-Tomasi/Rotation/Shi-Tomasi_0.png)
![](Shi-Tomasi/Rotation/Shi-Tomasi_45.png)
![](Shi-Tomasi/Rotation/Shi-Tomasi_90.png)
![](Shi-Tomasi/Rotation/Shi-Tomasi_135.png)

### Robustesse à la mise à l'échelle

De la même manière, Shi-Tomasi n'est pas invariant à l'échelle, on voit nettement la différence entre la première image à 50% et les deux suivantes à 100/150% :

![](Shi-Tomasi/Scale/Shi-Tomasi_0.5.png)
![](Shi-Tomasi/Scale/Shi-Tomasi_1.0.png)
![](Shi-Tomasi/Scale/Shi-Tomasi_1.5.png)

### Robustesse au bruit

En comparant les images pour différentes valeurs de \sigma, on se rend compte que Shi-Tomasi est plutôt robuste au bruit :

![](Shi-Tomasi/Noise/Shi-Tomasi_Noise_0.png)
![](Shi-Tomasi/Noise/Shi-Tomasi_Noise_7.png)
![](Shi-Tomasi/Noise/Shi-Tomasi_Noise_14.png)

Sur d'autres images cependant, on se rend compte que le caractère est beaucoup plus aléatoire, ce qui n'en fait pas une solution viable.

### Robustesse à la transformation projective

On peut voir que les points d'intérêts sont conservées en plus de voir l'ajout de nouveaux.

![](Shi-Tomasi/Projection/Shi-Tomasi_original.png)
![](Shi-Tomasi/Projection/Shi-Tomasi_projection.png)

## Descripteur SIFT

### Robustesse à la rotation

SIFT attribue à chaque point-clé une ou plusieurs orientations déterminées localement sur l'image à partir de la direction des gradients dans un voisinage autour du point. De ce fait, SIFT est invariant à la rotation.

![](SIFT/Rotation/SIFT_0.png)
![](SIFT/Rotation/SIFT_90.png)
![](SIFT/Rotation/SIFT_180.png)

### Robustesse à la mise à l'échelle

Comme l'indique son nom, le descripteur Scale-Invariant Features Transform est invariant à l'échelle car pour chaque point clé, le calcul s'effectue sur le gradient de la pyramide dont le paramètre est le plus proche du facteur d'échelle du point.
Cependant, lors de mes tests, je n'ai pas forcément pu retrouver cette propriété :

![](SIFT/Scale/SIFT_0.5.png)
![](SIFT/Scale/SIFT_1.0.png)
![](SIFT/Scale/SIFT_1.5.png)

### Robustesse au bruit

SIFT est plutôt robuste pour les modifications affines mais le bruit étant aléatoire, le descripteur semble très sensible à cette notion.

![](SIFT/Noise/SIFT_Noise_0.png)
![](SIFT/Noise/SIFT_Noise_7.png)
![](SIFT/Noise/SIFT_Noise_14.png)
![](SIFT/Noise/SIFT_Noise_20.png)

### Robustesse à la transformation projective

Avec cette image de base :

![](SIFT/Projection/SIFT_Original.png)

En zoomant sur le carré blanc en bas, on obtient ceci : 

![](SIFT/Projection/SIFT_Projection.png)

Il semble ainsi que SIFT soit plutôt robuste concernant les transformations projectives.

## Descripteur FAST

### Robustesse à la rotation

FAST semble plutôt robuste à la rotation sauf pour la rotation à 180°.

![](FAST/Rotation/FAST_0.png)
![](FAST/Rotation/FAST_45.png)
![](FAST/Rotation/FAST_135.png)
![](FAST/Rotation/FAST_180.png)
![](FAST/Rotation/FAST_225.png)
![](FAST/Rotation/FAST_315.png)

### Robustesse à la mise à l'échelle

FAST à 50% trouve moins de points que à 100/150%.

![](FAST/Scale/FAST_0.5.png)
![](FAST/Scale/FAST_1.0.png)
![](FAST/Scale/FAST_1.5.png)

### Robustesse au bruit

On voit rapidement que FAST est très sensible au bruit.

![](FAST/Noise/FAST_Noise_0.png)
![](FAST/Noise/FAST_Noise_7.png)
![](FAST/Noise/FAST_Noise_14.png)
![](FAST/Noise/FAST_Noise_20.png)

## Descripteur SURF

Je n'arrive plus à faire fonctionner SURF.create() mais le code est disponible.

## Descripteur BRIEF

Je n'arrive plus à faire fonctionner BRIEF.create() mais le code est disponible.

## Descripteur ORB

### Robustesse à la rotation
ORB, qui correspond à Orientied FAST and Rotated BRIEF m'a l'air, au vu des tests, robuste à la rotation sans pour autant y être invariant.

![](ORB/Rotation/ORB_0.png)
![](ORB/Rotation/ORB_45.png)
![](ORB/Rotation/ORB_135.png)
![](ORB/Rotation/ORB_180.png)
![](ORB/Rotation/ORB_225.png)
![](ORB/Rotation/ORB_315.png)

### Robustesse à la mise à l'échelle
A 50%, on obtient tous les points centrés au centre, là où cela est plus stable entre 100 et 150%.

![](ORB/Scale/ORB_0.5.png)
![](ORB/Scale/ORB_1.0.png)
![](ORB/Scale/ORB_1.5.png)

### Robustesse au bruit

De la même manière que certains autres descripteurs vus plus haut, ORB semble assez stable avec le bruit.

![](ORB/Noise/ORB_Noise_0.png)
![](ORB/Noise/ORB_Noise_7.png)
![](ORB/Noise/ORB_Noise_14.png)
![](ORB/Noise/ORB_Noise_20.png)