from odoo import http
from odoo.http import request
from datetime import datetime, timedelta

class AwesomeDashboard(http.Controller):

    @http.route('/my_dashboard/static', type='json', auth='user')
    def dashboard_statistics(self):
        today = datetime.today()
        first_day = today.replace(day=1)

        orders = request.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day),
        ])

        new_orders = orders.filtered(lambda o: o.state == 'draft')
        cancelled_orders = orders.filtered(lambda o: o.state == 'cancel')
        sent_or_cancelled_orders = orders.filtered(lambda o: o.state in ['cancel', 'sent'])

        total_amount = sum(orders.mapped('amount_total'))
        avg_tshirt_amount = 0
        tshirt_orders = orders.filtered(lambda o: any(p.product_id.name.lower() == 't-shirt' for p in o.order_line))
        if tshirt_orders:
            avg_tshirt_amount = sum(
                sum(l.product_uom_qty for l in o.order_line if l.product_id.name.lower() == 't-shirt')
                for o in tshirt_orders
            ) / len(tshirt_orders)

        def compute_avg_time(order):
            if order.state in ['cancel', 'sent'] and order.date_order and order.write_date:
                return (order.write_date - order.date_order).days
            return 0

        avg_time = 0
        if sent_or_cancelled_orders:
            avg_time = sum(compute_avg_time(o) for o in sent_or_cancelled_orders) / len(sent_or_cancelled_orders)

        return {
            'new_orders': len(new_orders),
            'total_amount': total_amount,
            'avg_tshirt_amount': round(avg_tshirt_amount, 2),
            'cancelled_orders': len(cancelled_orders),
            'avg_time_to_sent_or_cancelled': round(avg_time, 1)
        }
