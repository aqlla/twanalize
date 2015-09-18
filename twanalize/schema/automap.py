from sqlalchemy.ext.automap import automap_base


def get_orm_base(engine):
    orm_base = automap_base()
    orm_base.prepare(engine, reflect=True)


