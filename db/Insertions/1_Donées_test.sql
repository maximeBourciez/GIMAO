
INSERT INTO myApp_role (nomRole) VALUES 
('Operateur'),
('Magasinier'),
('Technicien'),
('Responsable GMAO'),
('Administrateur');

INSERT INTO myApp_lieu (nomLieu, typeLieu, lieuParent_id) VALUES
-- Niveau 1 : Bâtiments principaux
('Bâtiment Principal', 'Bâtiment', NULL),
('Entrepôt Logistique', 'Entrepôt', NULL),
('Centre de Recherche', 'Laboratoire', NULL),
('Complexe Administratif', 'Bureau', NULL),

-- Niveau 2 : Zones dans le Bâtiment Principal
('Zone de Production A', 'Zone de production', 1),
('Zone de Production B', 'Zone de production', 1),
('Atelier de Maintenance', 'Atelier', 1),
('Salle de Contrôle Qualité', 'Laboratoire', 1),

-- Niveau 3 : Sous-zones dans la Zone de Production A
('Ligne d''Assemblage 1', 'Ligne de production', 5),
('Ligne d''Assemblage 2', 'Ligne de production', 5),
('Poste de Soudure', 'Poste de travail', 5),
('Zone de Test', 'Zone de test', 5),

-- Niveau 3 : Sous-zones dans la Zone de Production B
('Unité de Moulage', 'Unité de production', 6),
('Unité de Peinture', 'Unité de production', 6),
('Zone d''Emballage', 'Zone logistique', 6),

-- Niveau 2 : Zones dans l'Entrepôt Logistique
('Zone de Réception', 'Zone logistique', 2),
('Zone de Stockage A', 'Zone de stockage', 2),
('Zone de Stockage B', 'Zone de stockage', 2),
('Zone d''Expédition', 'Zone logistique', 2),

-- Niveau 3 : Sous-zones dans la Zone de Stockage A
('Rack de Stockage 1', 'Rack', 17),
('Rack de Stockage 2', 'Rack', 17),
('Zone de Préparation des Commandes', 'Zone de travail', 17),

-- Niveau 2 : Zones dans le Centre de Recherche
('Laboratoire de Chimie', 'Laboratoire', 3),
('Laboratoire de Physique', 'Laboratoire', 3),
('Salle de Prototypage', 'Atelier', 3),
('Salle de Conférence Scientifique', 'Salle de réunion', 3),

-- Niveau 3 : Sous-zones dans le Laboratoire de Chimie
('Salle d''Analyse Spectrale', 'Salle d''analyse', 22),
('Salle de Synthèse', 'Salle d''expérimentation', 22),

-- Niveau 2 : Zones dans le Complexe Administratif
('Département des Ressources Humaines', 'Bureau', 4),
('Département Financier', 'Bureau', 4),
('Salle de Conférence Principale', 'Salle de réunion', 4),
('Cafétéria', 'Zone de restauration', 4),

-- Niveau 3 : Sous-zones dans le Département des Ressources Humaines
('Bureau du Directeur RH', 'Bureau individuel', 26),
('Espace de Recrutement', 'Espace ouvert', 26),
('Salle de Formation', 'Salle de formation', 26);


INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES 
('pbkdf2_sha256$260000$JGwJdrWhq8cltnqkfAHWLm$d2Wnocq6bdcS09QEwab8NcgeN5KJNAe6h32qNGb3n1U=', NULL, 1, 'admin','admin','admin', 'admin@a.com',1, 1, '2024-12-22 14:02:29.239568' ),
('pbkdf2_sha256$260000$phb2aIcIzdG1lvJw1bl59D$ozBponKnswZsjxZnnVNdV2tcQk1TVz3CoLPc9b4IdZk=', NULL, 1, 'root','root','root', 'root@r.com',1, 1, '2024-12-22 14:02:58.710980' ),
('pbkdf2_sha256$260000$ILKUledv9DGixmggCi2G76$n2vIEsYTSIIqI9OFIxvcRyBRkuvsipe61akibvHXomo=', NULL, 1, 'dev','dev','dev', 'dev@d.com',1, 1, '2024-12-22 14:03:17.251897' );



INSERT INTO myApp_fabricant (nomFabricant, paysFabricant, mailFabricant, numTelephoneFabricant, serviceApresVente) VALUES
('Acme Corporation', 'USA', 'contact@acmecorp.com', '+1234567890', True),
('Beta Industries', 'France', 'support@betaindustries.fr', '+33987654321', False),
('Gamma Tech', 'Germany', 'info@gammatech.de', '+491234567890', True),
('Delta Solutions', 'Japan', 'sales@deltasolutions.jp', '+811234567890', True),
('Epsilon Innovations', 'UK', 'enquiries@epsiloninnovations.co.uk', '+441234567890', False);

-- Ajout de nouveaux consommables/pièces
INSERT INTO myApp_consommable (designation, lienImageConsommable, fabricant_id) VALUES
('Cellule de Plasma Confiné', 'images/consomable/cellule_plasma.jpg', 1),
('Cristal de Focalisation Quantique', 'images/consomable/cristal_quantique.jpg', 2),
('Nanofiltre Gravitationnel', 'images/consomable/nanofiltre.jpg', 3),
('Bobine de Confinement Magnétique', 'images/consomable/bobine_magnetique.jpg', 4),
('Gel de Refroidissement Moléculaire', 'images/consomable/gel_refroidissement.jpg', 5),
('Catalyseur de Fusion Froide', 'images/consomable/catalyseur_fusion.jpg', 1),
('Membrane de Filtrage Dimensionnel', 'images/consomable/membrane_dimensionnelle.jpg', 2),
('Condensateur de Tachyons', 'images/consomable/condensateur_tachyons.jpg', 3),
('Stabilisateur d''Antimatière', 'images/consomable/stabilisateur_antimatiere.jpg', 4),
('Module d''Intelligence Quantique', 'images/consomable/module_ia_quantique.jpg', 5),
('Injecteur de Particules Subatomiques', 'images/consomable/injecteur_particules.jpg', 1),
('Filtre à Ondes Gravitationnelles', 'images/consomable/filtre_ondes.jpg', 2),
('Capteur de Fluctuations Temporelles', 'images/consomable/capteur_temporel.jpg', 3),
('Générateur de Champ de Stase', 'images/consomable/generateur_stase.jpg', 4),
('Matrice de Calcul Quantique', 'images/consomable/matrice_quantique.jpg', 5),
('Régulateur de Flux Dimensionnel', 'images/consomable/regulateur_flux.jpg', 1),
('Amplificateur de Résonance Neutrino', 'images/consomable/amplificateur_neutrino.jpg', 2),
('Convertisseur d''Énergie du Vide', 'images/consomable/convertisseur_vide.jpg', 3),
('Stabilisateur de Singularité', 'images/consomable/stabilisateur_singularite.jpg', 4),
('Modulateur de Phase Quantique', 'images/consomable/modulateur_phase.jpg', 5);







INSERT INTO myApp_fournisseur (nomFournisseur, numRue, nomRue, codePostal, ville, paysFournisseur, mailFournisseur, numTelephoneFournisseur, serviceApresVente) VALUES
('Alpha Supplies', 123, 'Main Street', '12345', 'New York', 'USA', 'orders@alphasupplies.com', '+1987654321', True),
('Bravo Parts', 456, 'Elm Street', '67890', 'Los Angeles', 'USA', 'sales@bravoparts.com', '+1234567890', False),
('Charlie Components', 789, 'Oak Avenue', '12345', 'Chicago', 'USA', 'info@charliecomponents.com', '+1345678901', True),
('Delta Distributors', 101, 'Pine Road', '67890', 'Houston', 'USA', 'support@deltadistributors.com', '+1456789012', True),
('Echo Equipment', 112, 'Maple Lane', '12345', 'Miami', 'USA', 'enquiries@echoequipment.com', '+1567890123', False);



INSERT INTO myApp_modeleequipement (
    nomModeleEquipement,
    fabricant_id
) VALUES
-- Alpha Corp (id: 1)
('Excavatrice Quantique XQ-1000', 1),
('Foreuse Moléculaire FM-500', 1),
('Compresseur Gravitationnel CG-750', 1),

-- Beta Industries (id: 2)
('Laminoir Magnétique LM-2000', 2),
('Presse Hydrostatique PH-3000', 2),
('Extrudeuse à Plasma EP-1500', 2),

-- Gamma Tech (id: 3)
('Laser de Précision Nanométrique LPN-X', 3),
('Scanner Holographique SH-4D', 3),
('Imprimante Biomoléculaire IB-3000', 3),

-- Delta Solutions (id: 4)
('Robot Assembleur Intelligent RAI-5000', 4),
('Drone de Maintenance Autonome DMA-X1', 4),
('Système d Inspection Quantique SIQ-2000', 4),

-- Epsilon Innovations (id: 5)
('Générateur de Champ de Force GCF-X', 5),
('Stabilisateur Temporel ST-1000', 5),
('Analyseur de Matière Noire AMN-500', 5),

-- Additional entries for variety
('Synthétiseur de Matériaux SM-3000', 1),
('Tour à Commande Neuronale TCN-X', 2),
('Recycleur Moléculaire RM-2000', 3),
('Fabricateur Quantique FQ-5000', 4),
('Téléporteur de Particules TP-X1', 5);


INSERT INTO myApp_equipement (
    reference,
    dateCreation,
    designation,
    dateMiseEnService,
    prixAchat,
    lienImageEquipement,
    createurEquipement_id,
    lieu_id,
    modeleEquipement_id,
    fournisseur_id,
    preventifGlissant,
    joursIntervalleMaintenance
) VALUES
('EQ-001', '2023-01-15 09:00:00', 'Excavatrice Quantique XQ-1000', '2023-01-20', 500000.00, 'images/equipement/excavatrice.jpg', 1, 9, 1, 1, TRUE, 30),
('EQ-002', '2023-02-01 10:30:00', 'Foreuse Moléculaire FM-500', '2023-02-05', 350000.00, 'images/equipement/foreuse.jpg', 2, 10, 2, 2, FALSE, 60),
('EQ-003', '2023-03-10 11:45:00', 'Compresseur Gravitationnel CG-750', '2023-03-15', 420000.00, 'images/equipement/compresseur.jpg', 3, 11, 3, 3, TRUE, 90),
('EQ-004', '2023-04-05 14:00:00', 'Laminoir Magnétique LM-2000', '2023-04-10', 380000.00, 'images/equipement/laminoir.jpg', 1, 13, 4, 4, FALSE, 120),
('EQ-005', '2023-05-20 16:15:00', 'Presse Hydrostatique PH-3000', '2023-05-25', 450000.00, 'images/equipement/presse.jpg', 2, 14, 5, 5, TRUE, 180),
('EQ-006', '2023-06-07 08:30:00', 'Extrudeuse à Plasma EP-1500', '2023-06-12', 320000.00, 'images/equipement/extrudeuse.jpg', 3, 15, 6, 1, FALSE, 45),
('EQ-007', '2023-07-18 13:45:00', 'Laser de Précision Nanométrique LPN-X', '2023-07-23', 550000.00, 'images/equipement/laser.jpg', 1, 22, 7, 2, TRUE, 75),
('EQ-008', '2023-08-30 11:00:00', 'Scanner Holographique SH-4D', '2023-09-04', 480000.00, 'images/equipement/scanner.jpg', 2, 23, 8, 3, FALSE, 100),
('EQ-009', '2023-09-12 15:30:00', 'Imprimante Biomoléculaire IB-3000', '2023-09-17', 620000.00, 'images/equipement/imprimante.jpg', 3, 24, 9, 4, TRUE, 150),
('EQ-010', '2023-10-25 10:15:00', 'Robot Assembleur Intelligent RAI-5000', '2023-10-30', 700000.00, 'images/equipement/robot.jpg', 1, 25, 10, 5, FALSE, 200);


INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) VALUES
('En fonctionnement', NULL, 'EQ-001', NULL, 1),
('En fonctionnement', NULL, 'EQ-002', NULL, 2),
('En fonctionnement', NULL, 'EQ-003', NULL, 3),
('En fonctionnement', NULL, 'EQ-004', NULL, 1),
('En fonctionnement', NULL, 'EQ-005', NULL, 2),
('En fonctionnement', NULL, 'EQ-006', NULL, 3),
('En fonctionnement', NULL, 'EQ-007', NULL, 1),
('En fonctionnement', NULL, 'EQ-008', NULL, 2),
('En fonctionnement', NULL, 'EQ-009', NULL, 3),
('En fonctionnement', NULL, 'EQ-010', NULL, 1);


INSERT INTO myApp_defaillance (
    commentaireDefaillance,
    niveau,
    utilisateur_id,
    equipement_id,
    dateTraitementDefaillance
) VALUES
('Usure anormale des rouleaux magnétiques', 'Mineur', 2, 'EQ-004',NULL),
('Problème de surchauffe dans le système de plasma', 'Critique', 3, 'EQ-006',NULL),
('Perte de précision dans la focalisation du laser', 'Mineur', 1, 'EQ-007',NULL),
('Dysfonctionnement du système d''alimentation', 'Majeur', 3, 'EQ-009',NULL);

-- Insert pour EQ-004
INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'Dégradé', CURRENT_TIMESTAMP, 'EQ-004',
(SELECT id FROM (SELECT id FROM myApp_informationstatut WHERE equipement_id = 'EQ-004' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-006
INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'A l''arret', CURRENT_TIMESTAMP, 'EQ-006',
(SELECT id FROM (SELECT id FROM myApp_informationstatut WHERE equipement_id = 'EQ-006' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-007
INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'Dégradé', CURRENT_TIMESTAMP, 'EQ-007',
(SELECT id FROM (SELECT id FROM myApp_informationstatut WHERE equipement_id = 'EQ-007' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-009
INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'A l''arret', CURRENT_TIMESTAMP, 'EQ-009',
(SELECT id FROM (SELECT id FROM myApp_informationstatut WHERE equipement_id = 'EQ-009' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;




INSERT INTO myApp_defaillance (
    commentaireDefaillance,
    niveau,
    utilisateur_id,
    equipement_id,
    dateTraitementDefaillance
) VALUES
('Fluctuations de puissance du laser', 'Mineur', 2, 'EQ-007',NULL),
('Défaillance du système de refroidissement optique', 'Critique', 3, 'EQ-007',NULL);




-- Insert pour EQ-007
INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'Dégradé', CURRENT_TIMESTAMP, 'EQ-007',
(SELECT id FROM (SELECT id FROM myApp_informationstatut WHERE equipement_id = 'EQ-007' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;



-- Insert pour EQ-007
INSERT INTO myApp_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'A l''arret', CURRENT_TIMESTAMP, 'EQ-007',
(SELECT id FROM (SELECT id FROM myApp_informationstatut WHERE equipement_id = 'EQ-007' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;


INSERT INTO myApp_intervention
(nomIntervention, interventionCurative, dateAssignation, dateCloture, dateDebutIntervention,
dateFinIntervention, tempsEstime, commentaireIntervention, commentaireRefusCloture, 
createurIntervention_id, defaillance_id, responsable_id) 
VALUES 
('Maintenance curative du système de refroidissement optique', True, CURRENT_TIMESTAMP, NULL, NULL, NULL, '03:30:00', NULL,NULL,1, 6, 3),
('Maintenance curative du système de plasma', True, CURRENT_TIMESTAMP, NULL, NULL, NULL, '07:00:00', NULL,NULL,1, 2, 3);


-- Association des consommables aux équipements
INSERT INTO myApp_constituer (equipement_id, consommable_id) VALUES
('EQ-001', 1), ('EQ-001', 6), ('EQ-001', 11),
('EQ-002', 2), ('EQ-002', 7), ('EQ-002', 12),
('EQ-003', 3), ('EQ-003', 8), ('EQ-003', 13),
('EQ-004', 4), ('EQ-004', 9), ('EQ-004', 14),
('EQ-005', 5), ('EQ-005', 10), ('EQ-005', 15),
('EQ-006', 1), ('EQ-006', 16), ('EQ-006', 11),
('EQ-007', 2),  -- Cristal de Focalisation Quantique
('EQ-007', 8),  -- Condensateur de Tachyons
('EQ-007', 13), -- Capteur de Fluctuations Temporelles
('EQ-007', 17), -- Amplificateur de Résonance Neutrino
('EQ-007', 20); -- Modulateur de Phase Quantique


-- Insertion des documents de défaillance pour EQ-007
INSERT INTO myApp_documentdefaillance (nomDocumentDefaillance, lienDocumentDefaillance, defaillance_id)
VALUES
('Rapport fluctuations laser EQ-007', 'documents/documentDefaillance/rapport_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Analyse fluctuations laser EQ-007', 'documents/documentDefaillance/analyse_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Rapport défaillance refroidissement EQ-007', 'documents/documentDefaillance/rapport_defaillance_refroidissement_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007')),
('Diagnostic système refroidissement EQ-007', 'documents/documentDefaillance/diagnostic_systeme_refroidissement_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007'));



-- Association des consommables compatibles avec les équipements
INSERT INTO myApp_estcompatible (modeleEquipement_id, consommable_id) VALUES
(1, 1), (1, 6), (1, 11),  -- Excavatrice Quantique XQ-1000
(2, 2), (2, 7), (2, 12),  -- Foreuse Moléculaire FM-500
(3, 3), (3, 8), (3, 13),  -- Compresseur Gravitationnel CG-750
(4, 4), (4, 9), (4, 14),  -- Laminoir Magnétique LM-2000
(5, 5), (5, 10), (5, 15), -- Presse Hydrostatique PH-3000
(6, 1), (6, 16), (6, 11), -- Extrudeuse à Plasma EP-1500
(7, 2), (7, 17), (7, 12), -- Laser de Précision Nanométrique LPN-X
(8, 3), (8, 18), (8, 13), -- Scanner Holographique SH-4D
(9, 4), (9, 19), (9, 14), -- Imprimante Biomoléculaire IB-3000
(10, 5), (10, 20), (10, 15); -- Robot Assembleur Intelligent RAI-5000


-- Insertion des documents techniques
INSERT INTO myApp_documenttechnique (nomDocumentTechnique, lienDocumentTechnique) VALUES
('Manuel d''utilisation LPN-X', 'documents/documentTecnique/manuel_utilisation_LPN-X.pdf'),
('Guide de maintenance LPN-X', 'documents/documentTecnique/guide_maintenance_LPN-X.pdf');

-- Association des documents techniques au modèle d'équipement (ID 7)
INSERT INTO myApp_correspondre (documentTechnique_id, modeleEquipement_id) VALUES
((SELECT id FROM myApp_documenttechnique WHERE nomDocumentTechnique = 'Manuel d''utilisation LPN-X'), 7),
((SELECT id FROM myApp_documenttechnique WHERE nomDocumentTechnique = 'Guide de maintenance LPN-X'), 7);


-- Insertion des documents de défaillance pour EQ-007
INSERT INTO myApp_documentdefaillance (nomDocumentDefaillance, lienDocumentDefaillance, defaillance_id)
VALUES
('Rapport fluctuations laser EQ-007', 'documents/documentDefaillance/rapport_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Analyse fluctuations laser EQ-007', 'documents/documentDefaillance/analyse_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Rapport défaillance refroidissement EQ-007', 'documents/documentDefaillance/rapport_defaillance_refroidissement_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007')),
('Diagnostic système refroidissement EQ-007', 'documents/documentDefaillance/diagnostic_systeme_refroidissement_EQ-007.pdf', 
 (SELECT id FROM myApp_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007'));


 -- Insertion des documents d'intervention pour l'intervention avec id = 1 (EQ-007)
INSERT INTO myApp_documentintervention (nomDocumentIntervention, lienDocumentIntervention, intervention_id) VALUES
('Procédure de réparation du système de refroidissement LPN-X', 'documents/documentIntervention/procedure_reparation_refroidissement_LPN-X.pdf', 1),
('Rapport d''intervention sur le système de refroidissement LPN-X', 'documents/documentIntervention/rapport_intervention_refroidissement_LPN-X.pdf', 1),
('Checklist de maintenance du système de refroidissement LPN-X', 'documents/documentIntervention/checklist_maintenance_refroidissement_LPN-X.pdf', 1),
('Schéma du système de refroidissement LPN-X', 'documents/documentIntervention/schema_systeme_refroidissement_LPN-X.pdf', 1);