# :toolbox: GIMAO – Gestion Informatisée de la Maintenance Assistée par Ordinateur

## :book: Présentation

**GIMAO** est une application web de **GMAO (Gestion de la Maintenance Assistée par Ordinateur)** destinée à simplifier et centraliser la gestion des interventions techniques au sein d’une entreprise.

Le système permet :
- aux **Opérateurs** de signaler facilement une panne ou un dysfonctionnement sur un équipement ;
- au **Responsable GMAO** d’analyser les demandes, de créer et d’affecter des **Bons de Travail (BT)** ;
- aux **Techniciens** de consulter leurs interventions, de les suivre et de les clôturer une fois réalisées.

---

## :jigsaw: Fonctionnalités principales

### :wrench: Cycle de maintenance
- Création de **Demandes d’Intervention (DI)** par les opérateurs.
- Validation ou refus des DI par le Responsable GMAO.
- Génération automatique d’un **Bon de Travail (BT)** pour chaque intervention validée.
- Suivi en temps réel de l’état d’un BT (assigné, en cours, terminé, clos).

### :busts_in_silhouette: Gestion des utilisateurs et des rôles
- Rôles disponibles : `Opérateur`, `Technicien`, `Responsable GMAO`.
- Interface d’administration complète via **Django Admin**.
- Journalisation des actions via une table de **Logs** (table, type, utilisateur, champs modifiés, date).

### :brain: Gestion technique
- Gestion des **équipements**, **pannes**, **pièces détachées** et **historiques d’intervention**.
- Architecture modulaire et extensible pour intégrer d’autres modules de maintenance ou d’analyse.

---

## :construction_site: Architecture technique

| Couche | Technologie | Détails |
|--------|--------------|---------|
| **Backend** | [Python 3](https://www.python.org/) + [Django](https://www.djangoproject.com/) | API REST, gestion des modèles et de l’authentification |
| **Base de données** | MySQL | Gestion relationnelle robuste et compatible JSONB |
| **Frontend** | Vue.js | Interface simple, adaptée aux utilisateurs non-informaticiens |
| **Admin** | Django Admin | Supervision du système |

---
