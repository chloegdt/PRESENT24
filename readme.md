# Cryptographie PRESENT24

*GODET Chloé & GROSJACQUES Marwane*
*L3 informatique*

## Présentation du projet
Ce projet permet le chiffrement ou le déchiffrement d'un message dont l'utilisateur fournit la clé.

Il permet également de réaliser une attaque 'Meet in the Middle' sur la version double du chiffrement PRESENT24 : 2PRESENT24. On utilise alors deux couples de clair-chiffré. 

## Prérequis
- Version de Python : 3.10.8
- Pip (lien pour un guide d'installation Linux/Windows/MacOS : https://pip.pypa.io/en/stable/installation
- Module numba (installation : ```pip install numba```)
module utilisé pour compiler le programme python afin d'améliorer les performances.

## Contenu du dossier
Le dossier PRESENT24 contient 8 fichiers :
- attaque.py
- cadencement_cle.py
- chiffrement.py
- dechiffrement.py
- opti.py
- test.py
- README.md
- GODET-Chloe_GROSJACQUES-Marwane.pdf

## Utilisation
### Chiffrement
Il est possible de réaliser un chiffrement uniquement. Pour cela, il faut exécuter la commande suivante dans un terminal : 
```python3 chiffrement.py message clé```
où *message* et *clé* sont des entiers en hexadécimal (précédé ou non de 0x).

Il s'affichera alors dans le terminal un message contenant le chiffré.
- Exemple :

```pyhton3 chiffrement.py 0x0 b3d5e6```

```
> Chiffrement PRESENT24 du message clair 000000 avec la clé b3d5e6
Le chiffré est 3fa671.
```


### Déchiffrement
Il est également possible de réaliser un déchiffrement. Pour cela, il faut exécuter la commande suivante dans un terminal : 
```python3 dechiffrement.py message clé```
où *message* et *clé* sont des entiers en hexadécimal (précédé ou non de 0x).

Il s'affichera alors dans le terminal un message contenant le message déchiffré.
- Exemple :

```pyhton3 dechiffrement.py 3fa671 b3d5e6```

```
> Déhiffrement PRESENT24 du message chiffré 3fa671 avec la clé b3d5e6
Le message clair est 000000.
```

### Attaque
Pour réaliser une attaque 'Meet in the Middle', il sera nécessaire de fournir deux couples clair-chiffré. 

Vous devez ensuite taper dans le terminal la commande suivante : 
```python3 attaque.py clair1 chiffre1 clair2 chiffre2```
où *clair1, chiffre1, clair2, chiffre2* sont des entiers en hexadecimal. 

Pour plus de praticité, vous avez également la possibilité de tester les deux couples de clair-chiffré de Chloé en tapant :
```python3 attaque.py -c```
et ceux de Marwane en tapant : 
```python3 attaque.py -m```

Lors de l'exécution, vous pourrez suivre étape par étape l'attaque. Il s'affichera dans le terminal un message indiquant le début de l'attaque, puis le début de la création des listes. Celui-ci sera accompagné d'une barre de chargement afin que vous puissiez en suivre la progression. 
Le temps de création des listes s'affichera à l'issue de cette étape. 
Le temps de tri des listes sera également renseigné. 

Un message indiquant la suite de l'attaque s'affichera alors, en rappelant le deuxième couple clair-chiffré. 
A nouveau, une barre de chargement indiquera la progression de la recherche des collisions entre les deux listes. Le temps de cette recherche sera indiqué et le nombre d'éléments communs trouvés également. 

A la fin de l'attaque, le nombre de couple de clés trouvé(s) vous sera indiqué et les clés vous seront renseignés en hexadécimal.

Enfin, la durée entière de l'attaque vous sera fournie. 

- Exemple :

```pyhton3 attaque.py -c```

```
> Début de l'attaque avec le message clair : 0x4efbd3 et le chiffré : 0x9c45fa
Création des listes...
[#################]
Listes crées en 7.392288446426392 secondes.

Liste_m triée en 3.6093602180480957 secondes.
Liste_c triée en 3.5849967002868652 secondes.

Suite de l'attaque avec le message clair : 0xfdd4e0 et le chiffré : 0x4ae29b
Recherche et test des elements communs entre les deux listes...
[#################]
16782676 elements communs trouvés et testés en 10.273966550827026 secondes.

1 couple(s) de clés trouvé(s) :
k1 = 0x673e22 | k2 = 0xae673a
Attaque terminée en 24.862444400787354 secondes.
```

### Test
Afin de tester le bon fonctionnement de nos fonctions cadencement_cle, chiffrement, dechiffrement, nous avons créé un fichier test.
Les données utilisées sont celles fournies dans l'énoncé du DM. 

Vous pouvez lancer ce test à l'aide de la commande : 
```python3 test.py``` 
qui affichera alors plusieurs messages clairs, leur clé, le chiffré attendu (celui fourni dans l'énoncé), le chiffré obtenu avec notre fonction de chiffrement, et le résultat du déchiffrement du chiffré obtenu. 

Ainsi, nous avons confirmer que nos fonctions étaient correctes. 


------------



## Nos résultats
Pour Chloé, comme indiqué dans l'exemple ci-dessus, un seul couple de clé a été trouvé : 
k1 = 0x673e22
k2 = 0xae673a

Pour Marwane, un couple de clé a été trouvé également : 
k1 = 0xc44276
k2 = 0xa47390

Nous avons, bien sûr, testé ces résultats pour vérifier que nous obtenions bien nos chiffrés à partir de nos messages clairs avec ces clés. 

## Optimisation

#### Choix d'implémentation
Etant donné les performances limitées de python (en termes de vitesse d'exécution comparé à C), nous avons décidé, dans un premier temps, d'optimiser notre code en python. Nous avons donc utilisé des simples opérations sur les bits (décalage, XOR, masques etc...). 
Nos messages clairs, chiffrés, clés sont tous des entiers. 

En python, il n'est pas possible de renseigner le nombre de bits de l'entier donc nous les avons mis chacun sur un entier respectivement. 

#### Tri des listes
En ce qui concerne le tri de nos listes Lm et Lc, crées lors de l'attaque, nous avons utilisé la fonction native sort(). Cette dernière étant codée en C, il s'agit de l'alternative la plus rapide que nous puissions utiliser. En effet, en coder une autre en python aurait ralentit notre programme.

#### Premier bilan
Notre code, ainsi terminé, avait une durée d'exécution de 32 minutes au mieux (le temps varie selon l'ordinateur utilisé). Il prenait également presque 7Go de RAM.

Nous avons donc cherché à le rendre plus rapide et moins gourmand en mémoire. 

#### Allègement de la mémoire
Nous avons pris la décision, une fois un élément commun trouvé entre les deux listes Lm et Lc, de tester le couple de clés candidates correspondantes immédiatement (avec le deuxième couple clair-chiffré). Ainsi, nous ne gardons plus les éléments en communs trouvés (sachant que nous avions plus de 16 780 000 collisions). Nous nous contentons de les compter et de stocker uniquement les couples de clés qui fonctionnent. 

#### Réduction du temps d'exécution
Si de cette façon nous avons largement soulagé la RAM, il était aussi important de gagner en temps. Nous avons importé le module numba permettant de compiler notre code. 
C'est pourquoi, dans nos fonctions, un décorateur @njit est présent. 

Avec ce module, le temps d'exécution de notre programme est passé de 32 minutes à une minute. 

#### Davantage de réduction
Nous avons testé le temps d'exécution de nos fonctions séparement et nous nous sommes rendu compte que faire appel à d'autres fonctions les rendaient plus lentes. 
C'est pour cette raison que le fichier opti.py a vu le jour. Ce dernier comporte nos fonctions de chiffrement et déchifrrement sans appel à d'autres fonctions (permutation, substitution). 

Cette modification a permis la réduction du temps par 2 (passant d'une minute à trente secondes en moyenne).

#### Pourquoi pas de multithreading ?
Nous n'avons pas utilisé de multithreading, bien que cela paraisse une bonne idée pour la création des listes et la recherche des éléments en commun, ces derniers étant parallélisables. 
Cependant, après avoir testé, il s'avère que cela ralentit notre programme de plusieurs secondes, ou dans le moins pire des cas, ne l'améliore pas. En effet, la répartition des tâches et la création des threads ainsi que la réduction des threads prend le même temps, voir plus, que notre programme sur un seul thread. 
Nous avons donc renoncé à l'utiliser. 







