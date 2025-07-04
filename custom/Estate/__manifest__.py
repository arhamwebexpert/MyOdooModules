{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Manage Real Estate Properties',
    'description': 'Module to manage real estate properties and their details.',
    'category': 'Sales',
    'author': 'Your Name or Company',
    'depends': ['base'],
    'data': [
         'security/ir.model.access.csv',
         'views/estate_property_views.xml',
         'views/estate_property_type_views.xml',
         'views/estate_property_tag_views.xml' ,
         'views/estate_property_offer_views.xml'
         
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
