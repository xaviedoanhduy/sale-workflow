By default the customer reference field is not displayed on the sale
order form, you have to enable it in the list of optional fields.

We want the customer ref on the package because the label should be printed from there (like all other kind of existing labels).
As we can't get the right stock.move.line/stock.move easily from the package it is easier to store the Customer Ref. of the move/move_line on the package when this one is assigned to the move line.
Also, a (destination) package could contain different products (so different moves), and these moves could have different Customer Ref., all of them will be concatened in the package => ", ".join(customer_ref_of_all_moves_link_to_this_package)
