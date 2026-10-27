-- Données de démonstration (base "gpu" uniquement, pas la base de test)
INSERT INTO app_user (nom, role, quota_hebdo_heures) VALUES
    ('Alice', 'USER', 10),
    ('Bilel', 'USER', 10),
    ('Admin', 'ADMIN', 40);

INSERT INTO gpu (nom) VALUES ('GPU-0');