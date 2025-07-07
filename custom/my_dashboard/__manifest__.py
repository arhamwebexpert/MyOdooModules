{
    "name": "My Dashboard",
    "version": "1.0",
    "category": "Tools",
    "summary": "Custom Dashboard using OWL",
    "depends": ["base", "web" , "sale"],
    "data": [
        "views/dashboard_menu.xml",
      
    ],
    "assets": {
        "web.assets_backend": [
            "my_dashboard/static/src/js/my_dashboard.js",
            "my_dashboard/static/src/xml/my_dashboard.xml",
        ],
    },
    "installable": True,
    "application": True
}
