{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/inherited_users_view.xml",
        "report/estate_property_report_templates.xml",
        "report/estate_property_report.xml",
        "views/estate_property_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
    "license": "LGPL-3",
    "assets": {
        "web.assets_backend": [
            "/real-estate/static/src/js/**/*",
        ],
    },
}
