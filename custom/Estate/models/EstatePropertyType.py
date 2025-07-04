from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"


    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    
    _sql_constraints = [
        (
            'unique_type_name' ,
            'UNIQUE(name)' ,
            'Property type name must be unique'
        )
    ]

