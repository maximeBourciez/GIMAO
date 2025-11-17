INSERT INTO gimao_role (nomRole) VALUES 
('Operateur'),
('Magasinier'),
('Technicien'),
('Responsable GMAO'),
('Administrateur');

INSERT INTO gimao_lieu (nomLieu, typeLieu, lieuParent_id) VALUES
-- Niveau 1 : Bâtiments principaux
('Bâtiment Principal', 'Bâtiment', NULL),
('Bibliothèque Universitaire', 'Bâtiment', NULL),
('Centre de Recherche', 'Laboratoire', NULL),
('Complexe Administratif', 'Bureau', NULL),

-- Niveau 2 : Zones dans le Bâtiment Principal
('Salle de Cours A', 'Salle de cours', 1),
('Salle de Cours B', 'Salle de cours', 1),
('Atelier de Prototypage', 'Atelier', 1),
('Salle de Contrôle Qualité', 'Laboratoire', 1),

-- Niveau 3 : Sous-zones dans la Salle de Cours A
('Poste de Présentation', 'Poste de travail', 5),
('Zone de Discussion', 'Zone de travail', 5),

-- Niveau 3 : Sous-zones dans la Salle de Cours B
('Zone de Repos', 'Zone de détente', 6),
('Poste de Travail Collaboratif', 'Poste de travail', 6),

-- Niveau 2 : Zones dans la Bibliothèque Universitaire
('Zone de Lectures', 'Zone de lecture', 2),
('Salle de Référence', 'Salle de recherche', 2),
('Salle d''Étude Collaborative', 'Salle de travail', 2),
('Espace Multimédia', 'Zone de technologie', 2),

-- Niveau 3 : Sous-zones dans la Zone de Lectures
('Zone Silencieuse', 'Zone calme', 10),
('Zone de Groupes d''Étude', 'Zone de travail', 10),

-- Niveau 2 : Zones dans le Centre de Recherche
('Laboratoire de Biologie', 'Laboratoire', 3),
('Laboratoire de Chimie', 'Laboratoire', 3),
('Salle de Prototypage', 'Atelier', 3),
('Salle de Conférence Scientifique', 'Salle de réunion', 3),

-- Niveau 3 : Sous-zones dans le Laboratoire de Biologie
('Salle d''Analyse Génétique', 'Salle d''analyse', 14),
('Salle de Culture Cellulaire', 'Salle d''expérimentation', 14),

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

INSERT INTO gimao_fabricant (nomFabricant, paysFabricant, mailFabricant, numTelephoneFabricant, serviceApresVente) VALUES
('Université Équipements', 'France', 'contact@universite-equipements.fr', '+33123456789', True),
('Technologies Avancées', 'Canada', 'support@techavances.ca', '+14123456789', False),
('Solutions Éducatives', 'Belgique', 'info@solutionseducatives.be', '+32123456789', True),
('Matériel Scientifique', 'États-Unis', 'sales@materielscientifique.com', '+11234567890', True),
('Innovations Pédagogiques', 'Suisse', 'enquiries@innovationspedagogiques.ch', '+41234567890', False);

-- Ajout de nouveaux consommables/pièces
INSERT INTO gimao_consommable (designation, lienImageConsommable, fabricant_id) VALUES
('Joint en Plastique', 'images/consommable/joint_plastique.jpg', 1),
('Vis en Acier Inoxydable', 'images/consommable/vis_acier.jpg', 2),
('Ressort de Compression', 'images/consommable/ressort_compression.jpg', 3),
('Garniture d''Étanchéité', 'images/consommable/garniture_etancheite.jpg', 4),
('Filtre à Air', 'images/consommable/filtre_air.jpg', 5),
('Joint Torique', 'images/consommable/joint_torique.jpg', 1),
('Boulon à Tête Hexagonale', 'images/consommable/boulon_hexagonal.jpg', 2),
('Câble de Connexion', 'images/consommable/cable_connexion.jpg', 3),
('Raccord en Plastique', 'images/consommable/raccord_plastique.jpg', 4),
('Lubrifiant pour Mécanismes', 'images/consommable/lubrifiant.jpg', 5),
('Roulement à Billes', 'images/consommable/roulement_billes.jpg', 1),
('Support de Montage', 'images/consommable/support_montage.jpg', 2),
('Plaque de Base', 'images/consommable/plaque_base.jpg', 3),
('Amortisseur', 'images/consommable/amortisseur.jpg', 4),
('Capteur de Température', 'images/consommable/capteur_temperature.jpg', 5),
('Tuyau Flexible', 'images/consommable/tuyau_flexible.jpg', 1),
('Protection en Caoutchouc', 'images/consommable/protection_caoutchouc.jpg', 2),
('Connecteur Électrique', 'images/consommable/connecteur_electrique.jpg', 3),
('Plaque de Circuit Imprimé', 'images/consommable/pc_imprime.jpg', 4),
('Élément Chauffant', 'images/consommable/element_chauffant.jpg', 5);

INSERT INTO gimao_fournisseur (nomFournisseur, numRue, nomRue, codePostal, ville, paysFournisseur, mailFournisseur, numTelephoneFournisseur, serviceApresVente) VALUES
('Fournitures Universitaires', 321, 'Université Avenue', '75001', 'Paris', 'France', 'contact@fournituresuniversitaires.fr', '+33123456789', True),
('Matériel Technique', 654, 'Innovation Street', '10001', 'Toronto', 'Canada', 'support@materieltechnique.ca', '+14161234567', False),
('Équipements de Laboratoire', 987, 'Research Blvd', '90210', 'Los Angeles', 'USA', 'info@equipementslaboratoire.com', '+1234567890', True),
('Fournisseurs Scientifiques', 234, 'Science Way', '75002', 'Londres', 'Royaume-Uni', 'sales@fournisseurscientifiques.co.uk', '+442012345678', True),
('Accessoires Éducatifs', 456, 'Learning Lane', '75003', 'Bruxelles', 'Belgique', 'enquiries@accessoireseducatifs.be', '+32123456789', False);

INSERT INTO gimao_modeleequipement (
    nomModeleEquipement,
    fabricant_id
) VALUES
-- Fournitures Universitaires (id: 1)
('Projecteur Multimédia PM-1000', 1),
('Tableau Interactif TI-500', 1),
('Système de Son SSS-750', 1),

-- Matériel Technique (id: 2)
('Imprimante 3D Avancée IA-2000', 2),
('Scanner de Documents SD-3000', 2),
('Écran Tactile Éducatif ET-1500', 2),

-- Équipements de Laboratoire (id: 3)
('Microscope Électronique ME-X', 3),
('Analyseur de Spectre AS-4D', 3),
('Centrifugeuse Haute Vitesse CHV-3000', 3),

-- Fournisseurs Scientifiques (id: 4)
('Robot de Manipulation RM-5000', 4),
('Drone de Recherche DR-X1', 4),
('Système d’Observation Astronomique SOA-2000', 4),

-- Accessoires Éducatifs (id: 5)
('Kit de Robotique Éducative KRE-X', 5),
('Stabilisateur de Présentation SP-1000', 5),
('Table de Montage pour Projets TMP-500', 5),

-- Additional entries for variety
('Caméra HD pour Cours en Ligne HD-3000', 1),
('Système de Réalité Virtuelle SV-2000', 2),
('Équipement de Mesure Précise EMP-2000', 3),
('Système de Gestion de Laboratoire SGL-5000', 4),
('Module de Formation en Ligne MFL-X1', 5);

INSERT INTO gimao_equipement (
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
('EQ-001', '2023-01-15 09:00:00', 'Projecteur Multimédia PM-1000', '2023-01-20', 1500.00, 'images/equipement/projecteur.jpg', 1, 9, 1, 1, TRUE, 30),
('EQ-002', '2023-02-01 10:30:00', 'Tableau Interactif TI-500', '2023-02-05', 2500.00, 'images/equipement/tableau_interactif.jpg', 2, 10, 2, 2, FALSE, 60),
('EQ-003', '2023-03-10 11:45:00', 'Système de Son SSS-750', '2023-03-15', 1200.00, 'images/equipement/systeme_son.jpg', 3, 11, 3, 3, TRUE, 90),
('EQ-004', '2023-04-05 14:00:00', 'Imprimante 3D Avancée IA-2000', '2023-04-10', 3500.00, 'images/equipement/imprimante_3D.jpg', 1, 13, 4, 4, FALSE, 120),
('EQ-005', '2023-05-20 16:15:00', 'Scanner de Documents SD-3000', '2023-05-25', 800.00, 'images/equipement/scanner.jpg', 2, 14, 5, 5, TRUE, 180),
('EQ-006', '2023-06-07 08:30:00', 'Écran Tactile Éducatif ET-1500', '2023-06-12', 2000.00, 'images/equipement/ecran_tactile.jpg', 3, 15, 6, 1, FALSE, 45),
('EQ-007', '2023-07-18 13:45:00', 'Microscope Électronique ME-X', '2023-07-23', 5000.00, 'images/equipement/microscope.jpg', 1, 22, 7, 2, TRUE, 75),
('EQ-008', '2023-08-30 11:00:00', 'Analyseur de Spectre AS-4D', '2023-09-04', 3000.00, 'images/equipement/analyseur.jpg', 2, 23, 8, 3, FALSE, 100),
('EQ-009', '2023-09-12 15:30:00', 'Centrifugeuse Haute Vitesse CHV-3000', '2023-09-17', 4500.00, 'images/equipement/centrifugeuse.jpg', 3, 24, 9, 4, TRUE, 150),
('EQ-010', '2023-10-25 10:15:00', 'Robot de Manipulation RM-5000', '2023-10-30', 10000.00, 'images/equipement/robot_manipulation.jpg', 1, 25, 10, 5, FALSE, 200);

INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) VALUES
('En fonctionnement', NULL, 'EQ-001', NULL, 1),
('Dégradé', NULL, 'EQ-002', NULL, 2),
('À l''arrêt', NULL, 'EQ-003', NULL, 3),
('En fonctionnement', NULL, 'EQ-004', NULL, 1),
('À l''arrêt', NULL, 'EQ-005', NULL, 2),
('À l''arrêt', NULL, 'EQ-006', NULL, 3),
('Dégradé', NULL, 'EQ-007', NULL, 1),
('Dégradé', NULL, 'EQ-008', NULL, 2),
('En fonctionnement', NULL, 'EQ-009', NULL, 3),
('Dégradé', NULL, 'EQ-010', NULL, 1);

INSERT INTO gimao_defaillance (
    commentaireDefaillance,
    niveau,
    utilisateur_id,
    equipement_id,
    dateTraitementDefaillance
) VALUES
('Problème de calibration du projecteur', 'Mineur', 1, 'EQ-001', NULL),
('Panne de l''imprimante 3D', 'Critique', 2, 'EQ-002', NULL),
('Bruit anormal lors du fonctionnement du système de son', 'Mineur', 3, 'EQ-003', NULL),
('Défaillance du scanner de documents', 'Majeur', 2, 'EQ-005', NULL),
('Dysfonctionnement de la centrifugeuse', 'Critique', 3, 'EQ-009', NULL);

-- Insert pour EQ-004
INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'Dégradé', CURRENT_TIMESTAMP, 'EQ-004',
(SELECT id FROM (SELECT id FROM gimao_informationstatut WHERE equipement_id = 'EQ-004' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-006
INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'À l''arrêt', CURRENT_TIMESTAMP, 'EQ-006',
(SELECT id FROM (SELECT id FROM gimao_informationstatut WHERE equipement_id = 'EQ-006' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-007
INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'Dégradé', CURRENT_TIMESTAMP, 'EQ-007',
(SELECT id FROM (SELECT id FROM gimao_informationstatut WHERE equipement_id = 'EQ-007' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-009
INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'À l''arrêt', CURRENT_TIMESTAMP, 'EQ-009',
(SELECT id FROM (SELECT id FROM gimao_informationstatut WHERE equipement_id = 'EQ-009' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

INSERT INTO gimao_defaillance (
    commentaireDefaillance,
    niveau,
    utilisateur_id,
    equipement_id,
    dateTraitementDefaillance
) VALUES
('Fluctuations de puissance du laser', 'Mineur', 2, 'EQ-007',NULL),
('Défaillance du système de refroidissement optique', 'Critique', 3, 'EQ-007',NULL);

-- Insert pour EQ-007
INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'Dégradé', CURRENT_TIMESTAMP, 'EQ-007',
(SELECT id FROM (SELECT id FROM gimao_informationstatut WHERE equipement_id = 'EQ-007' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

-- Insert pour EQ-007
INSERT INTO gimao_informationstatut (
    statutEquipement,
    dateChangement,
    equipement_id,
    informationStatutParent_id,
    ModificateurStatut_id
) SELECT 'À l''arrêt', CURRENT_TIMESTAMP, 'EQ-007',
(SELECT id FROM (SELECT id FROM gimao_informationstatut WHERE equipement_id = 'EQ-007' ORDER BY dateChangement DESC LIMIT 1) AS temp),
3;

INSERT INTO gimao_intervention
(nomIntervention, interventionCurative, dateAssignation, dateCloture, dateDebutIntervention,
dateFinIntervention, tempsEstime, commentaireIntervention, commentaireRefusCloture, 
createurIntervention_id, defaillance_id, responsable_id) 
VALUES 
('Fissure de l''optique', True, CURRENT_TIMESTAMP, NULL, NULL, NULL, '03:30:00', NULL,NULL,1, 6, 3),
('Maintenance du système d''alimentation du microscope', True, CURRENT_TIMESTAMP, NULL, NULL, NULL, '07:00:00', NULL,NULL,1, 2, 3);

-- Association des consommables aux équipements
INSERT INTO gimao_constituer (equipement_id, consommable_id) VALUES
('EQ-001', 1), ('EQ-001', 6), ('EQ-001', 11),
('EQ-002', 2), ('EQ-002', 7), ('EQ-002', 12),
('EQ-003', 3), ('EQ-003', 8), ('EQ-003', 13),
('EQ-004', 4), ('EQ-004', 9), ('EQ-004', 14),
('EQ-005', 5), ('EQ-005', 10), ('EQ-005', 15),
('EQ-006', 1), ('EQ-006', 16), ('EQ-006', 11),
('EQ-007', 15), -- Capteur de Température
('EQ-007', 18), -- Connecteur Électrique
('EQ-007', 19), -- Plaque de Circuit Imprimé
('EQ-007', 17), -- Protection en Caoutchouc
('EQ-007', 20); -- Élément Chauffant

-- Insertion des documents de défaillance pour EQ-007
INSERT INTO gimao_documentdefaillance (nomDocumentDefaillance, lienDocumentDefaillance, defaillance_id)
VALUES
('Rapport fluctuations laser EQ-007', 'documents/documentDefaillance/rapport_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Analyse fluctuations laser EQ-007', 'documents/documentDefaillance/analyse_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Rapport défaillance refroidissement EQ-007', 'documents/documentDefaillance/rapport_defaillance_refroidissement_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007')),
('Diagnostic système refroidissement EQ-007', 'documents/documentDefaillance/diagnostic_systeme_refroidissement_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007'));

-- Insertion des documents d'intervention pour l'intervention avec id = 1 (EQ-007)
INSERT INTO gimao_documentintervention (nomDocumentIntervention, lienDocumentIntervention, intervention_id) VALUES
('Procédure de réparation du système de refroidissement LPN-X', 'documents/documentIntervention/procedure_reparation_refroidissement_LPN-X.pdf', 1),
('Rapport d''intervention sur le système de refroidissement LPN-X', 'documents/documentIntervention/rapport_intervention_refroidissement_LPN-X.pdf', 1),
('Checklist de maintenance du système de refroidissement LPN-X', 'documents/documentIntervention/checklist_maintenance_refroidissement_LPN-X.pdf', 1),
('Schéma du système de refroidissement LPN-X', 'documents/documentIntervention/schema_systeme_refroidissement_LPN-X.pdf', 1);

-- Association des consommables compatibles avec les équipements
INSERT INTO gimao_estcompatible (modeleEquipement_id, consommable_id) VALUES
(1, 1), (1, 6), (1, 11),  -- Projecteur Multimédia PM-1000
(2, 2), (2, 7), (2, 12),  -- Tableau Interactif TI-500
(3, 3), (3, 8), (3, 13),  -- Système de Son SSS-750
(4, 4), (4, 9), (4, 14),  -- Imprimante 3D Avancée IA-2000
(5, 5), (5, 10), (5, 15), -- Scanner de Documents SD-3000
(6, 1), (6, 16), (6, 11), -- Écran Tactile Éducatif ET-1500
(7, 15), (7, 17), (7, 18), -- Microscope Électronique ME-X
(8, 3), (8, 18), (8, 13), -- Analyseur de Spectre AS-4D
(9, 4), (9, 19), (9, 14), -- Centrifugeuse Haute Vitesse CHV-3000
(10, 5), (10, 20), (10, 15); -- Robot de Manipulation RM-5000

-- Insertion des documents techniques
INSERT INTO gimao_documenttechnique (nomDocumentTechnique, lienDocumentTechnique) VALUES
('Manuel d''utilisation LPN-X', 'documents/documentTecnique/manuel_utilisation_LPN-X.pdf'),
('Guide de maintenance LPN-X', 'documents/documentTecnique/guide_maintenance_LPN-X.pdf'),
('Manuel d''utilisation PM-1000', 'documents/documentTechnique/manuel_utilisation_PM-1000.pdf'),
('Guide de maintenance PM-1000', 'documents/documentTechnique/guide_maintenance_PM-1000.pdf');

-- Association des documents techniques au modèle d'équipement (ID 7)
INSERT INTO gimao_correspondre (documentTechnique_id, modeleEquipement_id) VALUES
((SELECT id FROM gimao_documenttechnique WHERE nomDocumentTechnique = 'Manuel d''utilisation LPN-X'), 7),
((SELECT id FROM gimao_documenttechnique WHERE nomDocumentTechnique = 'Guide de maintenance LPN-X'), 7);

-- Association des documents techniques au modèle d'équipement (ID 1)
INSERT INTO gimao_correspondre (documentTechnique_id, modeleEquipement_id) VALUES
((SELECT id FROM gimao_documenttechnique WHERE nomDocumentTechnique = 'Manuel d''utilisation PM-1000'), 1),
((SELECT id FROM gimao_documenttechnique WHERE nomDocumentTechnique = 'Guide de maintenance PM-1000'), 1);

-- Insertion des documents de défaillance pour EQ-007
INSERT INTO gimao_documentdefaillance (nomDocumentDefaillance, lienDocumentDefaillance, defaillance_id)
VALUES
('Rapport fluctuations laser EQ-007', 'documents/documentDefaillance/rapport_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Analyse fluctuations laser EQ-007', 'documents/documentDefaillance/analyse_fluctuations_laser_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Fluctuations de puissance du laser' AND equipement_id = 'EQ-007')),
('Rapport défaillance refroidissement EQ-007', 'documents/documentDefaillance/rapport_defaillance_refroidissement_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007')),
('Diagnostic système refroidissement EQ-007', 'documents/documentDefaillance/diagnostic_systeme_refroidissement_EQ-007.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Défaillance du système de refroidissement optique' AND equipement_id = 'EQ-007')),
('Rapport calibration projecteur EQ-001', 'documents/documentDefaillance/rapport_calibration_projecteur_EQ-001.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Problème de calibration du projecteur' AND equipement_id = 'EQ-001')),
('Analyse calibration projecteur EQ-001', 'documents/documentDefaillance/analyse_calibration_projecteur_EQ-001.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Problème de calibration du projecteur' AND equipement_id = 'EQ-001')),
('Rapport défaillance scanner EQ-005', 'documents/documentDefaillance/rapport_defaillance_scanner_EQ-005.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Défaillance du scanner de documents' AND equipement_id = 'EQ-005')),
('Diagnostic scanner EQ-005', 'documents/documentDefaillance/diagnostic_scanner_EQ-005.pdf', 
 (SELECT id FROM gimao_defaillance WHERE commentaireDefaillance = 'Défaillance du scanner de documents' AND equipement_id = 'EQ-005'));

-- Insertion des documents d'intervention pour l'intervention avec id = 1 (EQ-007)
INSERT INTO gimao_documentintervention (nomDocumentIntervention, lienDocumentIntervention, intervention_id) VALUES
('Procédure de réparation du projecteur PM-1000', 'documents/documentIntervention/procedure_reparation_PM-1000.pdf', 1),
('Rapport d''intervention sur le projecteur PM-1000', 'documents/documentIntervention/rapport_intervention_PM-1000.pdf', 1),
('Checklist de maintenance du projecteur PM-1000', 'documents/documentIntervention/checklist_maintenance_PM-1000.pdf', 1),
('Schéma du projecteur PM-1000', 'documents/documentIntervention/schema_PM-1000.pdf', 1),
('Procédure de réparation du système de refroidissement LPN-X', 'documents/documentIntervention/procedure_reparation_refroidissement_LPN-X.pdf', 1),
('Rapport d''intervention sur le système de refroidissement LPN-X', 'documents/documentIntervention/rapport_intervention_refroidissement_LPN-X.pdf', 1),
('Checklist de maintenance du système de refroidissement LPN-X', 'documents/documentIntervention/checklist_maintenance_refroidissement_LPN-X.pdf', 1),
('Schéma du système de refroidissement LPN-X', 'documents/documentIntervention/schema_systeme_refroidissement_LPN-X.pdf', 1);