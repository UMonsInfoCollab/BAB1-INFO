# UMons Info Collab
Dépôt collaboratif pour s'échanger des synthèses, notes de cours, formulaires, flashcards... concernant la formation sciences informatiques à l'UMons.

## Licence
La licence utilisée est la GPL V3.0. Elle dérive du fait que certaines ressources étaient initialement sur un des dépôts de https://github.com/UMonsIT, dont certains sont sous la licence GPL V3.0 et d'autres sous licence MIT.
Un fichier licence résume les implications de cette licence.

Notez bien que le support de cours trouvé sur moodle ne vous appartient pas et donc vous ne pouvez pas le mettre sur le dépôt sans autorisation explicite du propriétaire du cours.

## Fonctionnement Général

### Structure
Contrairement à UMonsIT, tous les cours seront dans un même dépôt. Cela empêche de pouvoir télécharger les cours un à un, mais simplifie les transactions pour plusieurs raisons :

  * Il y a une licence unique pour tous les documents
  * Il est également plus facile d'imposer la même structure pour tous les cours.
  * Cela simplifie la vérification de doublons (argument principal)
  * Des documents de nature générale y auront leur place (todo-list, ...)

Toutefois, il est possible de revenir à la structure un cours qui reste plus facile à utiliser en pratique pour collaborer.

!!!
Les projets étant trop volumineux, ils auront éventuellement leurs propre dépôts. Un lien sera laissé dans ce dépôt principal.
!!!

### Qualité des documents
Il est complique d'exiger des documents de parfaite qualité car ils sont trop peu nombreux. C'est pour cette raison qu'une notation sera attribuée a chaque document selon une échelle a 3 niveaux.
* [***] Qualité excellente (ex: document PDF LateX)
* [** ] Qualité moyenne (ex: notes manuscrites parfaitement lisibles
* [*  ] Qualité médiocre (ex: notes manuscrites standard)

### Administration
Pour éviter au dépôt de mourir prématurément, il serait préférable d'avoir en permanence plusieurs administrateurs dans des années différentes.

Ainsi donc, à chaque proclamation, il faut trouver un nouvel étudiant volontaire pour évaluer les pull requests et animer le dépôt.

### Pull request
Pour participer, faites un fork du dépôt sur votre propre compte. Vous pourrez alors le modifier à votre guise, voir y inviter autant de gens que vous voulez pour contribuer.

Une fois une modification jugée satisfaisante, vous pouvez la commit sur votre dépôt avec le message en FRANÇAIS.
Une fois vos modifications terminées, faites un pull-request avec la modification et une brève explication.

L'administrateur aura alors à charge de soit valider la modification, soit expliquer ce qui ne va pas.

## Animation
Un des soucis pour une communauté est de s'éteindre. C'est là que prend place l'animation. C'est un mot assez vague qui peut englober des marathons-synthèses, des concours, des séances d'étude en groupe, des dîners au salon bleu, ...


## Structure interne

Voici le template de structure interne à suivre au maximum. A noter que pour conserver l'intégrité de certains anciens travaux, la structure peut légèrement différer.

```
NOM_COURS
└─── Théorie
│   └─── Nom_Prenom <- NOTES (pas synthèses) personnelles
│       │    Notes.pdf
│       │    Notes.tex
│       └─── Images
│   └─── Nom_Prenom
│       │    Notes.pdf
│       │    Notes.tex
│       └─── Images
│   ...
└─── TP
│   └─── TP_1
│       └─── Nom_Prenom
│           │    rapport.pdf
│           │    rapport.tex
│           └─── Images
│       ...
│    └─── TP_2
│    ...
└─── Synthèses
│    └─── Nom_Prenom
│        │    synthese.pdf
│        │    synthese.tex
│        └─── Images
│    └─── Nom_Prenom
│    ...
└─── Flashcards
│    └─── Nom_Prenom
│        └───deck.apkg
│    └─── Nom_Prenom
│    ...
```
