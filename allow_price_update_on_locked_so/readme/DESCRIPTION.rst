In Odoo standard, it is impossible to modify a product's price on a locked sales order.
The goal of this development is to enable authorized users to modify a product's price on a locked sales order for invoicing purposes.
The idea is that sales users can edit a sale price (following an error, for example) at the level of the sale order (not wait for an invoice).
On sale.order with state = done,
