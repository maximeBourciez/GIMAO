# Structure : nom_permission -> (description, type)
# type : 'affichage' | 'action'

perms = {
    # ── Demandes d'intervention ──────────────────────────────────────────────
    'di:viewList':    ("Voir la liste des demandes d'intervention",              'affichage'),
    'di:viewDetail':  ("Voir le détail d'une demande d'intervention",            'affichage'),
    'di:create':      ("Créer une demande d'intervention",                       'action'),
    'di:editAll':     ("Modifier toutes les demandes d'intervention",            'action'),
    'di:editCreated': ("Modifier ses propres demandes d'intervention",           'action'),
    'di:delete':      ("Supprimer une demande d'intervention",                   'action'),
    'di:accept':      ("Accepter une demande d'intervention",                    'action'),
    'di:refuse':      ("Refuser une demande d'intervention",                     'action'),
    'di:transform':   ("Transformer une demande d'intervention en bon de travail",'action'),
    'di:export':      ("Exporter les demandes d'intervention",                   'action'),
    'di:archive':     ("Archiver une demande d'intervention",                    'action'),

    # ── Bons de travail ──────────────────────────────────────────────────────
    'bt:viewList':               ("Voir la liste des bons de travail",              'affichage'),
    'bt:viewDetail':             ("Voir le détail d'un bon de travail",             'affichage'),
    'bt:create':                 ("Créer un bon de travail",                        'action'),
    'bt:editAll':                ("Modifier tous les bons de travail",              'action'),
    'bt:editAssigned':           ("Modifier les bons de travail assignés",          'action'),
    'bt:delete':                 ("Supprimer un bon de travail",                    'action'),
    'bt:start':                  ("Démarrer un bon de travail",                     'action'),
    'bt:end':                    ("Clôturer un bon de travail",                     'action'),
    'bt:refuse':                 ("Refuser un bon de travail",                      'action'),
    'bt:refuseClosure':          ("Refuser la clôture d'un bon de travail",         'action'),
    'bt:acceptClosure':          ("Accepter la clôture d'un bon de travail",        'action'),
    'bt:acceptConsumableRequest':("Valider une demande de consommable",             'action'),
    'bt:export':                 ("Exporter les bons de travail",                   'action'),
    'bt:archive':                ("Archiver un bon de travail",                     'action'),

    # ── Équipements ──────────────────────────────────────────────────────────
    'eq:viewList':      ("Voir la liste des équipements",                       'affichage'),
    'eq:viewDetail':    ("Voir le détail d'un équipement",                      'affichage'),
    'eq:view.calendar': ("Voir le calendrier des maintenances d'un équipement", 'affichage'),
    'eq:create':        ("Créer un équipement",                                 'action'),
    'eq:edit':          ("Modifier un équipement",                              'action'),
    'eq:delete':        ("Supprimer un équipement",                             'action'),
    'eq:export':        ("Exporter les équipements",                            'action'),
    'eq:archive':       ("Archiver un équipement",                              'action'),

    # ── Compteurs ────────────────────────────────────────────────────────────
    'cp:viewList':   ("Voir la liste des compteurs",    'affichage'),
    'cp:viewDetail': ("Voir le détail d'un compteur",   'affichage'),
    'cp:create':     ("Créer un compteur",              'action'),
    'cp:edit':       ("Modifier un compteur",           'action'),
    'cp:delete':     ("Supprimer un compteur",          'action'),
    'cp:export':     ("Exporter les compteurs",         'action'),

    # ── Maintenance préventive ───────────────────────────────────────────────
    'mp:viewList':   ("Voir la liste des maintenances préventives",  'affichage'),
    'mp:viewDetail': ("Voir le détail d'une maintenance préventive", 'affichage'),
    'mp:calendar':   ("Voir le calendrier des maintenances préventives", 'affichage'),
    'mp:create':     ("Créer une maintenance préventive",            'action'),
    'mp:edit':       ("Modifier une maintenance préventive",         'action'),
    'mp:delete':     ("Supprimer une maintenance préventive",        'action'),
    'mp:export':     ("Exporter les maintenances préventives",       'action'),

    # ── Stocks ───────────────────────────────────────────────────────────────
    'stock:view':             ("Voir les stocks",                           'affichage'),
    'stock:viewReservations': ("Voir les mises de côté",                    'affichage'),
    'stock:export':           ("Exporter les stocks",                       'action'),
    'stock:addPurchase':      ("Enregistrer un achat",                      'action'),
    'stock:transfer':         ("Transférer du stock entre magasins",        'action'),

    # ── Consommables ─────────────────────────────────────────────────────────
    'cons:viewDetail': ("Voir le détail d'un consommable",  'affichage'),
    'cons:create':     ("Créer un consommable",             'action'),
    'cons:edit':       ("Modifier un consommable",          'action'),
    'cons:delete':     ("Supprimer un consommable",         'action'),
    'cons:export':     ("Exporter les consommables",        'action'),
    'cons:archive':    ("Archiver un consommable",          'action'),

    # ── Magasins ─────────────────────────────────────────────────────────────
    'mag:viewList':   ("Voir la liste des magasins",    'affichage'),
    'mag:viewDetail': ("Voir le détail d'un magasin",   'affichage'),
    'mag:create':     ("Créer un magasin",              'action'),
    'mag:edit':       ("Modifier un magasin",           'action'),
    'mag:delete':     ("Supprimer un magasin",          'action'),
    'mag:export':     ("Exporter les magasins",         'action'),
    'mag:archive':    ("Archiver un magasin",           'action'),

    # ── Utilisateurs ─────────────────────────────────────────────────────────
    'user:viewList':   ("Voir la liste des utilisateurs",   'affichage'),
    'user:viewDetail': ("Voir le détail d'un utilisateur",  'affichage'),
    'user:create':     ("Créer un utilisateur",             'action'),
    'user:edit':       ("Modifier un utilisateur",          'action'),
    'user:disable':    ("Désactiver un utilisateur",        'action'),
    'user:enable':     ("Activer un utilisateur",           'action'),
    'user:delete':     ("Supprimer un utilisateur",         'action'),
    'user:export':     ("Exporter les utilisateurs",        'action'),

    # ── Rôles ────────────────────────────────────────────────────────────────
    'role:viewList':   ("Voir la liste des rôles",   'affichage'),
    'role:viewDetail': ("Voir le détail d'un rôle",  'affichage'),
    'role:create':     ("Créer un rôle",             'action'),
    'role:edit':       ("Modifier un rôle",          'action'),
    'role:delete':     ("Supprimer un rôle",         'action'),
    'role:export':     ("Exporter les rôles",        'action'),

    # ── Lieux ────────────────────────────────────────────────────────────────
    'loc:viewList':   ("Voir la liste des lieux",   'affichage'),
    'loc:viewDetail': ("Voir le détail d'un lieu",  'affichage'),
    'loc:create':     ("Créer un lieu",             'action'),
    'loc:edit':       ("Modifier un lieu",          'action'),
    'loc:delete':     ("Supprimer un lieu",         'action'),
    'loc:export':     ("Exporter les lieux",        'action'),
    'loc:archive':    ("Archiver un lieu",          'action'),

    # ── Fournisseurs ─────────────────────────────────────────────────────────
    'sup:viewList':   ("Voir la liste des fournisseurs",   'affichage'),
    'sup:viewDetail': ("Voir le détail d'un fournisseur",  'affichage'),
    'sup:create':     ("Créer un fournisseur",             'action'),
    'sup:edit':       ("Modifier un fournisseur",          'action'),
    'sup:delete':     ("Supprimer un fournisseur",         'action'),
    'sup:export':     ("Exporter les fournisseurs",        'action'),
    'sup:archive':    ("Archiver un fournisseur",          'action'),

    # ── Fabricants ───────────────────────────────────────────────────────────
    'man:viewList':   ("Voir la liste des fabricants",   'affichage'),
    'man:viewDetail': ("Voir le détail d'un fabricant",  'affichage'),
    'man:create':     ("Créer un fabricant",             'action'),
    'man:edit':       ("Modifier un fabricant",          'action'),
    'man:delete':     ("Supprimer un fabricant",         'action'),
    'man:export':     ("Exporter les fabricants",        'action'),
    'man:archive':    ("Archiver un fabricant",          'action'),

    # ── Modèles d'équipement ─────────────────────────────────────────────────
    'eqmod:viewList':   ("Voir la liste des modèles d'équipement",   'affichage'),
    'eqmod:viewDetail': ("Voir le détail d'un modèle d'équipement",  'affichage'),
    'eqmod:create':     ("Créer un modèle d'équipement",             'action'),
    'eqmod:edit':       ("Modifier un modèle d'équipement",          'action'),
    'eqmod:delete':     ("Supprimer un modèle d'équipement",         'action'),
    'eqmod:export':     ("Exporter les modèles d'équipement",        'action'),
    'eqmod:archive':    ("Archiver un modèle d'équipement",          'action'),

    # ── Export global ────────────────────────────────────────────────────────
    'export:view': ("Accéder aux exports de données", 'affichage'),

    # ── Menu ─────────────────────────────────────────────────────────────────
    'menu:view':           ("Accéder au menu de navigation",         'affichage'),
    'menu:dataManagement': ("Accéder au menu de gestion des données",'affichage'),
    'menu:calendar':       ("Accéder au calendrier",                 'affichage'),

    # ── Dashboard ────────────────────────────────────────────────────────────
    'dash:display.di':         ("Afficher les demandes d'intervention sur le tableau de bord", 'affichage'),
    'dash:display.diCreated':  ("Afficher ses demandes d'intervention sur le tableau de bord", 'affichage'),
    'dash:display.bt':         ("Afficher les bons de travail sur le tableau de bord",         'affichage'),
    'dash:display.btAssigned': ("Afficher ses bons de travail assignés sur le tableau de bord",'affichage'),
    'dash:display.eq':         ("Afficher les équipements sur le tableau de bord",             'affichage'),
    'dash:display.mag':        ("Afficher les magasins sur le tableau de bord",                'affichage'),
    'dash:display.vertical':   ("Afficher le tableau de bord en mode vertical",               'affichage'),
    'dash:stats.full':         ("Voir toutes les statistiques",                               'affichage'),
    'dash:stats.bt':           ("Voir les statistiques des bons de travail",                  'affichage'),
    'dash:stats.di':           ("Voir les statistiques des demandes d'intervention",          'affichage'),
}

perms_map = {
    "Responsable GMAO": [
        perm for perm in perms.keys() if perm not in [
            'dash:display.vertical', 'dash:display.eq', 'dash:display.mag',
            'dash:display.btAssigned', 'dash:display.diCreated',
        ]
    ],

    "Technicien": [
        'di:viewList', 'di:viewDetail', 'di:create', 'di:editCreated',
        'bt:viewList', 'bt:viewDetail', 'bt:start', 'bt:end', 'bt:editAssigned',
        'eq:viewList', 'eq:viewDetail', 'eq:edit',
        'cp:viewList', 'cp:viewDetail', 'cp:edit',
        'mp:viewList', 'mp:viewDetail',
        'stock:view',
        'menu:view',
        'dash:display.eq', 'dash:display.btAssigned', 'dash:stats.bt',
    ],

    "Opérateur": [
        'di:viewList', 'di:viewDetail', 'di:create', 'di:editCreated',
        'bt:viewList', 'bt:viewDetail',
        'eq:viewList', 'eq:viewDetail',
        'menu:view',
        'dash:display.diCreated', 'dash:display.eq', 'dash:stats.di', 'dash:display.vertical',
    ],

    "Magasinier": [
        'bt:viewList', 'bt:viewDetail', 'bt:acceptConsumableRequest',
        'stock:view', 'stock:export', 'stock:viewReservations', 'stock:addPurchase', 'stock:transfer',
        'cons:viewDetail', 'cons:create', 'cons:edit', 'cons:delete', 'cons:export',
        'mag:viewList', 'mag:viewDetail', 'mag:create', 'mag:edit', 'mag:delete', 'mag:export',
        'menu:view',
        'export:view',
        'dash:display.mag',
    ],
}
