{
    'name': "To-Do List Module",
    'version': '17.0.0.1.0',
    'depends': ['mail','sale_management','contacts'],
    'author': "Mounir",
    'category': 'To-Do app',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/todo_views.xml',
        'views/menu.xml',
        'reports/todo_report.xml',

    ],
    'assets':{
        # 'web.assets_backend':['hospital/static/src/css/hospital.css']
    },
    'installable': True,
    'application':True,
}

