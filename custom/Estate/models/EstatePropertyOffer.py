from odoo import models , fields  , api 
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted','Accepted') ,
            ('refused','Refused')
        ] ,
        copy = False 
    )

    partner_id = fields.Many2one("res.partner" , string = "partner" , copy = False , required = True) 
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string = "validity (days) ", default = 7)
    date_deadline = fields.Date(string= "DeadLine" , compute = "_compute_date_deadline" , inverse = "_inverse_date_deadline" , store =True)
    
    @api.depends('create_date' , 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = (create_date + timedelta(days = offer.validity)).date()
    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.validity = (offer.date_deadline - create_date.date()).days if offer.date_deadline else 0    
    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("Cannot accept an offer for a sold property.")
            other_offers =  offer.property_id.offer_id.filtered(lambda o: o.id != offer.id)
            other_offers.write({'status': 'refused'})
            offer.status = 'accepted'
            offer.property_id.state = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
    def action_refuse(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("You cannot refuse an offer for a sold property.")
            offer.status = 'refused'
