perms = [
    # Demandes d'intervention
    'di:viewList', 'di:viewDetail', 'di:create', 'di:editCreated', 'di:editAll', 'di:delete', 'di:accept', 'di:transform', 'di:refuse', 'di:export',

    # Demandes d'intervention
    'bt:viewList', 'bt:viewDetail', 'bt:create', 'bt:editAll', 'bt:editAssigned', 'bt:delete', 'bt:start', 'bt:end', 'bt:refuse', 'bt:refuseClosure', 'bt:acceptClosure', 'bt:acceptConsumableRequest', 'bt:export',

    # Equipements
    'eq:viewList', 'eq:viewDetail', 'eq:create', 'eq:edit', 'eq:delete', 'eq:export',

    # Compteurs
    'cp:viewList', 'cp:viewDetail', 'cp:create', 'cp:edit', 'cp:delete', 'cp:export',

    # Maintenance préventive
    'mp:viewList', 'mp:viewDetail', 'mp:create', 'mp:edit', 'mp:delete', 'mp:export',

    # Gestion des stocks
    'stock:view', 'stock:export',
    'cons:viewDetail', 'cons:create', 'cons:edit', 'cons:delete', 'cons:export',
    'mag:viewList', 'mag:viewDetail', 'mag:create', 'mag:edit', 'mag:delete', 'mag:export',

    # Gestion des utilisateurs
    'user:viewList', 'user:viewDetail', 'user:create', 'user:edit', 'user:disable', 'user:enable', 'user:delete', 'user:export',

    # Gestion des rôles
    'role:viewList', 'role:viewDetail', 'role:create', 'role:edit', 'role:delete', 'role:export',

    # Données secondaires
    'loc:viewList', 'loc:viewDetail', 'loc:create', 'loc:edit', 'loc:delete', 'loc:export',
    'sup:viewList', 'sup:viewDetail', 'sup:create', 'sup:edit', 'sup:delete', 'sup:export',
    'man:viewList', 'man:viewDetail', 'man:create', 'man:edit', 'man:delete', 'man:export',
    'eqmod:viewList', 'eqmod:viewDetail', 'eqmod:create', 'eqmod:edit', 'eqmod:delete', 'eqmod:export',

    # Export de données
    'export:view', 

    # Menu
    'menu:view',

    # Dashboard
    'dash:display.di', 'dash:display.bt', 'dash:display.eq', 'dash:display.mag',
    'dash:stats.full', 'dash:stats.bt', 'dash:stats.di',
    'dash:display.vertical',
]

perms_map = {
    "Responsable GMAO": [
        perm for perm in perms if perm not in ['dash:display.vertical', 'dash:display.eq', 'dash:display.mag' ]
    ],

    "Technicien": [
        'di:viewList', 'di:viewDetail', 'di:create', 'di:editCreated',

        'bt:viewList', 'bt:viewDetail', 'bt:start', 'bt:end', 'bt:editAssigned',

        'eq:viewList', 'eq:viewDetail', 'eq:edit',

        'cp:viewList', 'cp:viewDetail', 'cp:edit',

        'mp:viewList', 'mp:viewDetail',

        'stock:view',

        'dash:display.di', 'dash:display.bt', 'dash:stats.bt',
    ],

    "Opérateur": [
        'di:viewList', 'di:viewDetail', 'di:create', 'di:editCreated',

        'bt:viewList', 'bt:viewDetail',

        'eq:viewList', 'eq:viewDetail',

        'dash:display.di', 'dash:display.eq', 'dash:stats.di','dash:display.vertical',
    ],

    "Magasinier": [
        'bt:viewList', 'bt:viewDetail', 'bt:acceptConsumableRequest',

        'stock:view', 'stock:export',

        'cons:viewDetail', 'cons:create', 'cons:edit', 'cons:delete', 'cons:export',

        'mag:viewList', 'mag:viewDetail', 'mag:create', 'mag:edit', 'mag:delete', 'mag:export',

        'export:view',

        'dash:display.mag'
    ],
}


