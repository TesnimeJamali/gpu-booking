# Vision du projet – Réservation de créneaux GPU

## 1. Vision (5 lignes)

1. **Problème :** le serveur GPU du laboratoire est partagé, et les réservations par messages ou tableur provoquent des conflits et des créneaux gaspillés.
2. **Utilisateurs :** étudiants, chercheurs et administrateur du serveur.
3. **Fonction principale :** réserver un GPU sur un créneau donné, sans chevauchement avec une autre réservation.
4. **Règles d'équité :** un quota hebdomadaire par utilisateur, modifiable par l'administrateur.
5. **Valeur :** moins de conflits et moins de temps GPU perdu, grâce aux rappels et à la libération automatique des créneaux non utilisés.

## 2. Acteurs

| Acteur | Type | Rôle |
|---|---|---|
| Utilisateur (étudiant ou chercheur) | Principal | Consulte, réserve, annule, confirme le démarrage |
| Administrateur | Principal | Gère les quotas et consulte les statistiques |
| Système de notification | Secondaire (simulé) | Reçoit les rappels et alertes |

## 3. Cas d'utilisation

| ID | Nom | Acteur | En une phrase |
|---|---|---|---|
| UC01 | Consulter la disponibilité | Utilisateur | Voir les créneaux déjà occupés d'un GPU pour un jour donné |
| UC02 | Réserver un créneau (**à risque**) | Utilisateur | Réserver un GPU sans chevauchement, dans la limite du quota hebdomadaire |
| UC03 | Annuler une réservation | Utilisateur | Annuler avant le début ; le créneau redevient disponible |
| UC04 | Recevoir rappels et alertes | Système de notification | Rappel avant le début, alerte avant la fin, une seule fois chacun |
| UC05 | Libérer automatiquement un créneau non démarré | Utilisateur, système de notification | Confirmer son démarrage, sinon libération 15 minutes après le début |
| UC06 | Gérer quotas et statistiques | Administrateur | Modifier le quota d'un utilisateur et consulter l'usage |

**Cas à risque technique : UC02**, à cause du conflit de réservation (deux personnes visent le même créneau en même temps).

## 4. Priorisation

Notes de 1 à 3 sur trois critères : valeur métier, risque, impact sur l'architecture.

| UC | Valeur | Risque | Impact archi. | Total | Traité en |
|---|---|---|---|---|---|
| UC02 | 3 | 3 | 3 | **9** | Itération 1 (base), itération 2 (complet) |
| UC01 | 3 | 1 | 2 | 6 | Itération 2 |
| UC03 | 2 | 2 | 2 | 6 | Itération 2 |
| UC05 | 2 | 2 | 2 | 6 | Itération 3 |
| UC04 | 2 | 2 | 1 | 5 | Itération 3 |
| UC06 | 1 | 1 | 1 | 3 | Itération 3 |

**À traiter en premier : UC02.** C'est là que se concentrent le risque et les décisions d'architecture (base de données, transactions, concurrence). Le Processus unifié demande de traiter tôt ce qui est risqué.

## 5. Risque et parade

| Risque | Parade |
|---|---|
| Double réservation d'un créneau (UC02) | Contrainte d'exclusion en base et test de concurrence dès l'itération 1 |

## 6. Planification : 3 itérations et 4 phases

| Itération | Phase et jalon | Contenu | Tag Git |
|---|---|---|---|
| Préliminaire | Étude préliminaire → **Vision** | Vision, acteurs, liste des UC, priorisation, risques, tableau de bord | `v0.0-vision` |
| It. 1 | Élaboration → **Architecture** | Dépôt, CI, diagramme de cas d'utilisation, UC02 de base de bout en bout, premier test en CI | `v0.1-elaboration` |
| It. 2 | Construction | UC02 complet (quota), UC01, UC03, fiche UC02 et diagrammes de conception | `v0.5-iteration2` |
| It. 3 | Construction → **Version bêta**, puis Transition → **Produit livré** | UC05, UC04, UC06, revue croisée, corrections, recette, documentation | `v0.9-beta`, puis `v1.0-transition` |

## 7. Limites assumées

- Authentification simplifiée.
- Notifications simulées.
- Un seul GPU de démonstration dans les données de départ.
