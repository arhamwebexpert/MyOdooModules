/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

class MyDashboard extends Component {
    static template = "my_dashboard_template";

    setup() {
        this.statistics = {
            new_orders: 0,
            total_amount: 0,
            avg_tshirt_amount: 0,
            cancelled_orders: 0,
            avg_time_to_sent_or_cancelled: 0
        };

        onWillStart(async () => {
            const result = await rpc("/my_dashboard/static");


            this.statistics = {
                new_orders: result.new_orders,
                total_amount: result.total_amount,
                avg_tshirt_amount: result.avg_tshirt_amount,
                cancelled_orders: result.cancelled_orders,
                avg_time_to_sent_or_cancelled: result.avg_time_to_sent_or_cancelled
            };
        });
    }
}

registry.category("actions").add("my_dashboard", MyDashboard);
