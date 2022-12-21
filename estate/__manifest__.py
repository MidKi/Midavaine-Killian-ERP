{
    "name": "Estate",  # The name that will appear in the App list
    "version": "16.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ['base', 'sale_management', 'calendar', 'hr'],  # dependencies
    "installable": True,
    'license': 'LGPL-3',
    'data': ["views/res_groups.xml", "views/res_partner.xml", "views/sale_order.xml"]
}
