

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session


engine = create_engine('sqlite:///wsys_db.db')
session = Session(engine)


has_table = inspect(engine).has_table('Widget')
# has_table = engine.dialect.has_table(engine,'widget')


if has_table:
    print('table widget exists')
else:
    print('table doesnt exist')
