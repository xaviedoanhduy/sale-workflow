# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Allow price update on locked sales orders",
    "summary": """
    The idea is that sales users can edit a sale price (following an error, for example)
    at the level of the sale order (not wait for an invoice).
    On sale.order with state = done,
    add a "pen" icon which allows user to override (edit) the unit_price
    """,
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "category": "Sales",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "depends": ["sale"],
    "data": [
        "security/res_groups.xml",
        "views/sale_order_views.xml",
    ],
}
