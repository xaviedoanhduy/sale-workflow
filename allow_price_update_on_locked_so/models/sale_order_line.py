# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import AccessError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_protected_fields(self):
        """
        Override to remove 'price_unit' from the list of protected fields
        for users with specific permissions.
        """
        protected_fields = super()._get_protected_fields()
        group_can_edit = self.env.user.has_group(
            "allow_price_update_on_locked_so.group_edit_unit_price_on_sol"
        )
        if "price_unit" in protected_fields:
            if not group_can_edit:
                raise AccessError(
                    _(
                        "You don't have the permission to edit "
                        "the unit price on locked sale orders."
                    )
                )
            protected_fields.remove("price_unit")
        return protected_fields
