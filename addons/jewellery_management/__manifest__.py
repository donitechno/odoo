# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "jewellery management",
    "version": "13.0.0",
    "author": "bandabaru",
    "website": "http://bandabaru.com",
    "license": "AGPL-3",
    "category": "apps",
    "summary": "",
    "depends": ["mrp","purchase","account","sale"],
    "data": ["wizard/product_weight_update_view.xml",
            #"security/jewellery_management_security.xml",
            "security/ir.model.access.csv",
            "views/purchase_order_from_supplier.xml",
            "views/product_view.xml",
            "views/stock_move_inherit.xml",
            "views/purchase_order_inherit.xml",
            "views/penjualan_view.xml",
            "views/mutasi_stock_view.xml",
            "views/mutasi_penerimaan_bdp_stock_view.xml",
            "views/mutasi_kirim_bdp_stock_view.xml",
            "views/mutasi_cash_bank_view.xml",
            "views/penerimaan_cash_bank_view.xml",
            "views/pengeluaran_cash_bank_view.xml",
            "views/mutasi_tarik_setor_modal_stock_view.xml",
            "views/stock_picking_inherit.xml",
            "views/invoice_view.xml",
            "views/sale_order_inherit.xml",
            "views/res_currency_view_inherit.xml",
            "wizard/pembayaran_wizard.xml",

             ],
    "installable": True,    
    'auto_install': False,
    'application': True,
}
