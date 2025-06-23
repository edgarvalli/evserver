menu_options = [
    {
        "sequence": 1,
        "name": "Contabilidad",
        "children": [
            {"name": "Balance General", "path": "/app/contabilidad/balanceGeneral"}
        ],
    },
    {
        "sequence": 2,
        "name": "Nominas",
        "children": [{"name": "Empleados", "path": "/app/nominas/empleados"}],
    },
    {
        "sequence": 3,
        "name": "Configuración",
        "children": [
            {"name": "Usuarios", "path": "/app/configuracion/usuarios", 'sequence':1},
            {"name": "Roles", "path": "/app/configuracion/roles", 'sequence': 2},
            {"name": "Endpoints", "path": "/app/configuracion/endpoints", 'sequence': 3},
        ],
    },
]
