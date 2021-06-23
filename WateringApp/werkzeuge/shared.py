
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from WateringApp.extensions import db, metadata

from WateringApp.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)


menu_items = [
    {
        'href': '/restart',
        'text': 'Restart'
    },
    {
        'href': '/user',
        'text': 'User Management'
    },
    {
        'href': '/statistics',
        'text': 'Statistics'
    },

    {
        'href': 'settings',
        'text': 'Settings'
    },
    {
        'href': '/',
        'text': 'Widget'
    }
]
