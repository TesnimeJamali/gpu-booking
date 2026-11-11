# UC02 : Réserver un créneau (UC à risque)

**Ticket** : #2 · **Branche** : `uc02-reserver-creneau` · **Priorité** : 9/9 (itération 1 : base, itération 2 : complet)

## Acteur principal
Utilisateur (étudiant ou chercheur), identifié par l'en-tête `X-User-Id`.

## Objectif
Réserver un GPU sur un créneau donné, sans chevauchement avec une autre réservation. Le quota hebdomadaire prévu par la vision n'est pas traité dans cette version (voir « Hors périmètre »).

## Préconditions
- L'utilisateur et le GPU existent en base.
- La base PostgreSQL est disponible.

## Déclencheur
`POST /reservations` avec `gpu_id`, `start`, `end`.

## Scénario nominal
1. L'utilisateur envoie la demande de réservation (gpu_id, start, end) avec son identifiant.
2. Le système vérifie que `end` est strictement après `start`.
3. Le système vérifie que `start` n'est pas dans le passé.
4. Le système vérifie que la durée ne dépasse pas la durée maximale (8 h, valeur provisoire).
5. Le système vérifie que le créneau est libre pour ce GPU et enregistre la réservation.
6. Le système répond **201** avec la réservation créée.

## Scénarios alternatifs
- **2a** `end` ≤ `start` : rejet, **422**.
- **3a** `start` dans le passé : rejet, **422**.
- **4a** durée supérieure à la durée maximale : rejet, **422**.
- **5a** le créneau chevauche une réservation existante : rejet, **409**.
- **5b** GPU ou utilisateur inexistant : rejet, **422**.
- **5c** deux demandes simultanées sur le même créneau : une seule réussit (201), l'autre reçoit **409**.

## Postconditions
- Succès : une réservation est enregistrée.
- Échec : aucune réservation n'est créée.

## Règles métier
- Durée maximale : 8 h (valeur provisoire, à confirmer avec l'équipe).
- Aucun chevauchement sur un même GPU (contrainte d'exclusion PostgreSQL).

## Risque technique
Double réservation en cas de demandes simultanées : contrainte d'exclusion en base, verrou consultatif par GPU, test de concurrence.

## Hors périmètre (version actuelle)
- Quota hebdomadaire : prévu par la vision, à ajouter à UC02 ou à traiter avec UC06 selon la décision de l'équipe. Si ajouté, la fiche, les diagrammes, le code et les tests devront être mis à jour dans cet ordre.

## Traçabilité
- UML : `docs/uml/classes-uc02.puml`, `docs/uml/sequence-uc02.puml`
- Code : `app/controller.py`, `app/services/reservation_service.py`, `app/repositories/reservation_repository.py`, `app/errors.py`, `app/main.py`
- Tests : chaque test cite le numéro d'étape de cette fiche (ex. « étape 5 », « alternatif 5a »).