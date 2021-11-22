import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-stock-logistics-warehouse",
    description="Meta package for oca-stock-logistics-warehouse Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-account_move_line_product',
        'odoo10-addon-account_move_line_stock_info',
        'odoo10-addon-packaging_uom',
        'odoo10-addon-procurement_auto_create_group',
        'odoo10-addon-purchase_packaging',
        'odoo10-addon-sale_packaging',
        'odoo10-addon-stock_account_change_product_valuation',
        'odoo10-addon-stock_account_quant_merge',
        'odoo10-addon-stock_available',
        'odoo10-addon-stock_available_immediately',
        'odoo10-addon-stock_available_sale',
        'odoo10-addon-stock_available_unreserved',
        'odoo10-addon-stock_change_qty_reason',
        'odoo10-addon-stock_cycle_count',
        'odoo10-addon-stock_demand_estimate',
        'odoo10-addon-stock_inventory_chatter',
        'odoo10-addon-stock_inventory_discrepancy',
        'odoo10-addon-stock_inventory_exclude_sublocation',
        'odoo10-addon-stock_inventory_lockdown',
        'odoo10-addon-stock_inventory_preparation_filter',
        'odoo10-addon-stock_inventory_revaluation',
        'odoo10-addon-stock_inventory_verification_request',
        'odoo10-addon-stock_lot_sale_tracking',
        'odoo10-addon-stock_mts_mto_rule',
        'odoo10-addon-stock_operation_package_mandatory',
        'odoo10-addon-stock_orderpoint_automatic_creation',
        'odoo10-addon-stock_orderpoint_manual_procurement',
        'odoo10-addon-stock_orderpoint_manual_procurement_uom',
        'odoo10-addon-stock_orderpoint_uom',
        'odoo10-addon-stock_putaway_product',
        'odoo10-addon-stock_quant_manual_assign',
        'odoo10-addon-stock_quant_merge',
        'odoo10-addon-stock_quant_reserved_qty_uom',
        'odoo10-addon-stock_removal_location_by_priority',
        'odoo10-addon-stock_reserve',
        'odoo10-addon-stock_warehouse_orderpoint_stock_info',
        'odoo10-addon-stock_warehouse_orderpoint_stock_info_unreserved',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
