-- Schéma de la base "gpu" (PostgreSQL 16)
-- btree_gist permet de combiner "=" (sur gpu_id) et "&&" (chevauchement d'intervalles)
-- dans une même contrainte d'exclusion.
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE IF NOT EXISTS app_user (
    id                  SERIAL PRIMARY KEY,
    nom                 TEXT NOT NULL,
    role                TEXT NOT NULL DEFAULT 'USER' CHECK (role IN ('USER', 'ADMIN')),
    quota_hebdo_heures  INT  NOT NULL DEFAULT 10 CHECK (quota_hebdo_heures >= 0)
);

CREATE TABLE IF NOT EXISTS gpu (
    id   SERIAL PRIMARY KEY,
    nom  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reservation (
    id                   SERIAL PRIMARY KEY,
    user_id              INT NOT NULL REFERENCES app_user(id),
    gpu_id               INT NOT NULL REFERENCES gpu(id),
    start_at             TIMESTAMPTZ NOT NULL,
    end_at               TIMESTAMPTZ NOT NULL,
    status               TEXT NOT NULL DEFAULT 'CONFIRMED'
                         CHECK (status IN ('CONFIRMED', 'CANCELLED', 'EXPIRED')),
    started_at           TIMESTAMPTZ,
    rappel_debut_envoye  BOOLEAN NOT NULL DEFAULT FALSE,
    alerte_fin_envoyee   BOOLEAN NOT NULL DEFAULT FALSE,
    CHECK (end_at > start_at),
    -- Deux réservations CONFIRMED du même GPU ne peuvent pas se chevaucher.
    -- tstzrange est semi-ouvert [début, fin) : 10h-12h et 12h-14h sont compatibles.
    EXCLUDE USING gist (
        gpu_id WITH =,
        tstzrange(start_at, end_at) WITH &&
    ) WHERE (status = 'CONFIRMED')
);

-- Notifications simulées (UC04, UC05)
CREATE TABLE IF NOT EXISTS notification (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES app_user(id),
    reservation_id  INT NOT NULL REFERENCES reservation(id),
    type            TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);