from odoo import fields, models ,api 
from odoo.exceptions import UserError ,ValidationError
from odoo.tools.float_utils import float_compare , float_is_zero 

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
   
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string= "Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    living_area = fields.Float()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    property_type_id = fields.Many2one('estate.property.type' , string="Property Type")
    buyer_id = fields.Many2one("res.partner" , string = "Buyer" , copy = False)
    salesperson_id = fields.Many2one("res.users" , string= "Salesperson" , default = lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_id = fields.One2many(
    "estate.property.offer",  # comodel name
    "property_id",            # inverse_name — the Many2one field in the offer model
    string="Offers"
    )
    total_area = fields.Integer(
        string = "Total Area" ,
        compute = "_compute_total_area" ,
        store = True
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], required=True, copy=False, default='new')
    @api.depends('living_area' , 'garden_area')
    def _compute_total_area(self) :
        for record in self:
            record.total_area = (record.living_area or 0 ) + (record.garden_area or 0)
    @api.depends('offer_id.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_id.mapped('price')
            property.best_price = max(prices) if prices else 0.0 
    @api.onchange('garden')
    def _onchange_garden(self):
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = 'north'
            else:
                self.garden_area = 0
                self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if not record.offer_id.filtered(lambda o: o.status == 'accepted'):
                raise UserError("Cannot mark as sold without an accepted offer.")
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
    @api.constrains('expected_price','selling_price') 
    def _checking_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price , precision_digits=2):
                continue 
            min_acceptable_price = record.expected_price * 0.9  
            if float_compare(record.selling_price , min_acceptable_price , precision_digits=2) < 0 :
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")


  