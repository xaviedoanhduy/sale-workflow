# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError, UserError
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged("post_install", "-at_install")
class TestSaleOrderLocked(TestSaleCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        # Create the SO with four order lines
        cls.sale_order = (
            cls.env["sale.order"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "partner_id": cls.partner_a.id,
                    "partner_invoice_id": cls.partner_a.id,
                    "partner_shipping_id": cls.partner_a.id,
                    "pricelist_id": cls.company_data["default_pricelist"].id,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": cls.company_data["product_order_no"].id,
                                "product_uom_qty": 5,
                                "tax_id": False,
                            }
                        ),
                        Command.create(
                            {
                                "product_id": cls.company_data[
                                    "product_service_delivery"
                                ].id,
                                "product_uom_qty": 4,
                                "tax_id": False,
                            }
                        ),
                        Command.create(
                            {
                                "product_id": cls.company_data[
                                    "product_service_order"
                                ].id,
                                "product_uom_qty": 3,
                                "tax_id": False,
                            }
                        ),
                        Command.create(
                            {
                                "product_id": cls.company_data[
                                    "product_delivery_no"
                                ].id,
                                "product_uom_qty": 2,
                                "tax_id": False,
                            }
                        ),
                    ],
                }
            )
        )

    def test_price_update_on_locked_so(self):
        self.assertEqual(self.sale_order.state, "draft")
        self.env["ir.config_parameter"].sudo().set_param(
            "sale.group_auto_done_setting", "True"
        )
        group_auto_done_setting = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale.group_auto_done_setting")
        )
        self.assertTrue(group_auto_done_setting)
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, "done")
        # all values of data fields cannot be changed
        # except for the price_unit
        with self.assertRaises(UserError):
            self.sale_order.order_line[0].product_uom_qty = 3
            self.sale_order.order_line[0].name = "Product 4"
            tax_a = self.env["account.tax"].create(
                {
                    "name": "Test tax",
                    "type_tax_use": "sale",
                    "price_include": False,
                    "amount_type": "percent",
                    "amount": 15.0,
                }
            )
            self.sale_order.order_line[0].tax_id = tax_a.ids
        with self.assertRaises(AccessError):
            self.sale_order.order_line[0].price_unit = 100
        self.env.user.groups_id += self.env.ref(
            "allow_price_update_on_locked_so.group_edit_unit_price_on_sol"
        )
        self.sale_order.order_line[0].price_unit = 100
        old_subtotal = self.sale_order.amount_total
        self.sale_order.order_line[1].price_unit = 400
        self.assertNotEqual(old_subtotal, self.sale_order.amount_total)
