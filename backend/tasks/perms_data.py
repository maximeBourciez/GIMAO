# Structure : nom_permission -> (description, type, permission_parente)
# type : 'affichage' | 'action'
# permission_parente : nom de la permission parente (str) ou None

perms = {
    # Demandes d'intervention
    'di:viewList':    ("Voir la liste des demandes d'intervention",         'affichage', None),
    'di:viewDetail':  ("Voir le détail d'une demande d'intervention",        'affichage', None),
    'di:create':      ("Créer une demande d'intervention",                   'action',    None),
    'di:editAll':     ("Modifier toutes les demandes d'intervention",        'action',    None),
    'di:editCreated': ("Modifier ses propres demandes d'intervention",       'action',    'di:editAll'),
    'di:delete':      ("Supprimer une demande d'intervention",               'action',    None),
    'di:accept':      ("Accepter une demande d'intervention",                'action',    None),
    'di:refuse':      ("Refuser une demande d'intervention",                 'action',    None),
    'di:transform':   ("Transformer une demande d'intervention en bon de travail", 'action', None),
    'di:export':      ("Exporter les demandes d'intervention",               'action',    None),
    'di:archive':     ("Archiver une demande d'intervention",                'action',    None),

    # Bons de travail
    'bt:viewList':               ("Voir la liste des bons de travail",              'affichage', None),
    'bt:viewDetail':             ("Voir le détail d'un bon de travail",             'affichage', None),
    'bt:create':                 ("Créer un bon de travail",                        'action',    None),
    'bt:editAll':                ("Modifier tous les bons de travail",              'action',    None),
    'bt:editAssigned':           ("Modifier les bons de travail assignés",          'action',    'bt:editAll'),
    'bt:delete':                 ("Supprimer un bon de travail",                    'action',    None),
    'bt:start':                  ("Démarrer un bon de travail",                     'action',    None),
    'bt:end':                    ("Clôturer un bon de travail",                     'action',    None),
    'bt:refuse':                 ("Refuser un bon de travail",                      'action',    None),
    'bt:refuseClosure':          ("Refuser la clôture d'un bon de travail",        'action',    None),
    'bt:acceptClosure':          ("Accepter la clôture d'un bon de travail",       'action',    None),
    'bt:acceptConsumableRequest':("Valider une demande de consommable",             'action',    None),
    'bt:export':                 ("Exporter les bons de travail",                   'action',    None),
    'bt:archive':                ("Archiver un bon de travail",                     'action',    None),

    # Équipements
    'eq:viewList':      ("Voir la liste des équipements",                    'affichage', None),
    'eq:viewDetail':    ("Voir le détail d'un équipement",                   'affichage', None),
    'eq:create':        ("Créer un équipement",                              'action',    None),
    'eq:edit':          ("Modifier un équipement",                           'action',    None),
    'eq:delete':        ("Supprimer un équipement",                          'action',    None),
    'eq:export':        ("Exporter les équipements",                         'action',    None),
    'eq:archive':       ("Archiver un équipement",                           'action',    None),
    'eq:view.calendar': ("Voir le calendrier des maintenances d'un équipement", 'affichage', None),

    # Compteurs
    'cp:viewList':   ("Voir la liste des compteurs",    'affichage', None),
    'cp:viewDetail': ("Voir le détail d'un compteur",   'affichage', None),
    'cp:create':     ("Créer un compteur",              'action',    None),
    'cp:edit':       ("Modifier un compteur",           'action',    None),
    'cp:delete':     ("Supprimer un compteur",          'action',    None),
    'cp:export':     ("Exporter les compteurs",         'action',    None),

    # Maintenance préventive
    'mp:viewList':   ("Voir la liste des maintenances préventives",         'affichage', None),
    'mp:viewDetail': ("Voir le détail d'une maintenance préventive",        'affichage', None),
    'mp:create':     ("Créer une maintenance préventive",                   'action',    None),
    'mp:edit':       ("Modifier une maintenance préventive",                'action',    None),
    'mp:delete':     ("Supprimer une maintenance préventive",               'action',    None),
    'mp:export':     ("Exporter les maintenances préventives",              'action',    None),
    'mp:calendar':   ("Voir le calendrier des maintenances préventives",    'affichage', None),

    # Stocks
    'stock:view':             ("Voir les stocks",                           'affichage', None),
    'stock:export':           ("Exporter les stocks",                       'action',    None),
    'stock:viewReservations': ("Voir les mises de côté",                    'affichage', None),
    'stock:addPurchase':      ("Enregistrer un achat",                      'action',    None),
    'stock:transfer':         ("Transférer du stock entre magasins",        'action',    None),

    # Consommables
    'cons:viewDetail': ("Voir le détail d'un consommable",  'affichage', None),
    'cons:create':     ("Créer un consommable",             'action',    None),
    'cons:edit':       ("Modifier un consommable",          'action',    None),
    'cons:delete':     ("Supprimer un consommable",         'action',    None),
    'cons:export':     ("Exporter les consommables",        'action',    None),
    'cons:archive':    ("Archiver un consommable",          'action',    None),

    # Magasins
    'mag:viewList':   ("Voir la liste des magasins",    'affichage', None),
    'mag:viewDetail': ("Voir le détail d'un magasin",   'affichage', None),
    'mag:create':     ("Créer un magasin",              'action',    None),
    'mag:edit':       ("Modifier un magasin",           'action',    None),
    'mag:delete':     ("Supprimer un magasin",          'action',    None),
    'mag:export':     ("Exporter les magasins",         'action',    None),
    'mag:archive':    ("Archiver un magasin",           'action',    None),

    # Utilisateurs
    'user:viewList':   ("Voir la liste des utilisateurs",   'affichage', None),
    'user:viewDetail': ("Voir le détail d'un utilisateur",  'affichage', None),
    'user:create':     ("Créer un utilisateur",             'action',    None),
    'user:edit':       ("Modifier un utilisateur",          'action',    None),
    'user:disable':    ("Désactiver un utilisateur",        'action',    None),
    'user:enable':     ("Activer un utilisateur",           'action',    None),
    'user:delete':     ("Supprimer un utilisateur",         'action',    None),
    'user:export':     ("Exporter les utilisateurs",        'action',    None),

    # Rôles
    'role:viewList':   ("Voir la liste des rôles",   'affichage', None),
    'role:viewDetail': ("Voir le détail d'un rôle",  'affichage', None),
    'role:create':     ("Créer un rôle",             'action',    None),
    'role:edit':       ("Modifier un rôle",          'action',    None),
    'role:delete':     ("Supprimer un rôle",         'action',    None),
    'role:export':     ("Exporter les rôles",        'action',    None),

    # Lieux
    'loc:viewList':   ("Voir la liste des lieux",   'affichage', None),
    'loc:viewDetail': ("Voir le détail d'un lieu",  'affichage', None),
    'loc:create':     ("Créer un lieu",             'action',    None),
    'loc:edit':       ("Modifier un lieu",          'action',    None),
    'loc:delete':     ("Supprimer un lieu",         'action',    None),
    'loc:export':     ("Exporter les lieux",        'action',    None),
    'loc:archive':    ("Archiver un lieu",          'action',    None),

    # Fournisseurs
    'sup:viewList':   ("Voir la liste des fournisseurs",   'affichage', None),
    'sup:viewDetail': ("Voir le détail d'un fournisseur",  'affichage', None),
    'sup:create':     ("Créer un fournisseur",             'action',    None),
    'sup:edit':       ("Modifier un fournisseur",          'action',    None),
    'sup:delete':     ("Supprimer un fournisseur",         'action',    None),
    'sup:export':     ("Exporter les fournisseurs",        'action',    None),
    'sup:archive':    ("Archiver un fournisseur",          'action',    None),

    # Fabricants
    'man:viewList':   ("Voir la liste des fabricants",   'affichage', None),
    'man:viewDetail': ("Voir le détail d'un fabricant",  'affichage', None),
    'man:create':     ("Créer un fabricant",             'action',    None),
    'man:edit':       ("Modifier un fabricant",          'action',    None),
    'man:delete':     ("Supprimer un fabricant",         'action',    None),
    'man:export':     ("Exporter les fabricants",        'action',    None),
    'man:archive':    ("Archiver un fabricant",          'action',    None),

    # Modèles d'équipement
    'eqmod:viewList':   ("Voir la liste des modèles d'équipement",   'affichage', None),
    'eqmod:viewDetail': ("Voir le détail d'un modèle d'équipement",  'affichage', None),
    'eqmod:create':     ("Créer un modèle d'équipement",             'action',    None),
    'eqmod:edit':       ("Modifier un modèle d'équipement",          'action',    None),
    'eqmod:delete':     ("Supprimer un modèle d'équipement",         'action',    None),
    'eqmod:export':     ("Exporter les modèles d'équipement",        'action',    None),
    'eqmod:archive':    ("Archiver un modèle d'équipement",          'action',    None),

    # Export global
    'export:view': ("Accéder aux exports de données", 'affichage', None),

    # Menu
    'menu:view':           ("Accéder au menu de navigation",      'affichage', None),
    'menu:dataManagement': ("Accéder au menu de gestion des données", 'affichage', None),
    'menu:calendar':       ("Accéder au calendrier",              'affichage', None),

    # Dashboard
    'dash:display.di':         ("Afficher les demandes d'intervention sur le tableau de bord", 'affichage', None),
    'dash:display.diCreated':  ("Afficher ses demandes d'intervention sur le tableau de bord", 'affichage', 'dash:display.di'),
    'dash:display.bt':         ("Afficher les bons de travail sur le tableau de bord",         'affichage', None),
    'dash:display.btAssigned': ("Afficher ses bons de travail assignés sur le tableau de bord",'affichage', 'dash:display.bt'),
    'dash:display.eq':         ("Afficher les équipements sur le tableau de bord",             'affichage', None),
    'dash:display.mag':        ("Afficher les magasins sur le tableau de bord",                'affichage', None),
    'dash:display.vertical':   ("Afficher le tableau de bord en mode vertical",               'affichage', None),
    'dash:stats.full':         ("Voir toutes les statistiques",                               'affichage', None),
    'dash:stats.bt':           ("Voir les statistiques des bons de travail",                  'affichage', 'dash:stats.full'),
    'dash:stats.di':           ("Voir les statistiques des demandes d'intervention",          'affichage', 'dash:stats.full'),
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
