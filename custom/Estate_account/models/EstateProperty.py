from odoo import models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()

        for property in self:
            if not property.buyer_id:
                raise ValueError("Cannot create invoice: no buyer assigned.")
            if not property.selling_price:
                raise ValueError("Cannot create invoice: selling price is missing.")

            # Fetch an income account
            income_account = self.env['account.account'].search([
                ('account_type', '=', 'income')
            ], limit=1)

            if not income_account:
                raise ValueError("No income account found to create invoice line.")

            commission = property.selling_price * 0.06  
            admin_fee = 100.0

            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': '6% Commission',
                        'quantity': 1,
                        'price_unit': commission,
                        'account_id': income_account.id,
                    }),
                    (0, 0, {
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': admin_fee,
                        'account_id': income_account.id,
                    }),
                ],
            })

        return res
