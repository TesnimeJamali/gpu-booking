# gpu-booking

Réservation de créneaux GPU sur un serveur partagé.
TP1 – Processus unifié et approches agiles (INSAT).

## Équipe
| Rôle | Membre |
|---|---|
| P1 – Pilote du processus | Tesnime Jamali |
| P2 – Base de données et CI | ... |
| P3 – Backend UC02 | ... |
| P4 – Tests et qualité | ... |
| P5 – UML et documentation | ... |

## Règles de travail
1. `main` reste toujours vert : la CI doit passer.
2. Une branche par cas d'utilisation, nommée ainsi :
   `uc01-consulter-disponibilite`, `uc02-reserver-creneau`,
   `uc03-annuler-reservation`, `uc04-rappels-alertes`,
   `uc05-liberation-automatique`, `uc06-quotas-statistiques`.
3. Chaque commit cite son ticket : `UC02: route POST /reservations (#2)`.
4. Chaque pull request contient `Closes #N` et désigne un relecteur
   (champ Reviewers). Ce relecteur est une autre personne que l'auteur.
5. On fusionne seulement si la CI est verte et la PR approuvée.
6. On ne pousse jamais directement sur `main` (sauf le README et les
   documents de vision au tout début).
7. Une carte passe en « En cours » quand on commence, et en « Terminé »
   à la fusion (automatique avec `Closes #N`).

## Correspondance UC / tickets
| UC | Ticket | Branche |
|---|---|---|
| UC01 Consulter la disponibilité | #1 | uc01-consulter-disponibilite |
| UC02 Réserver un créneau | #2 | uc02-reserver-creneau |
| UC03 Annuler une réservation | #3 | uc03-annuler-reservation |
| UC04 Recevoir rappels et alertes | #4 | uc04-rappels-alertes |
| UC05 Libérer automatiquement un créneau | #5 | uc05-liberation-automatique |
| UC06 Gérer quotas et statistiques | #6 | uc06-quotas-statistiques |

## Jalons (tags Git)
v0.0-vision · v0.1-elaboration · v0.5-iteration2 · v0.9-beta · v1.0-transition
