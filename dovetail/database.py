from sqlalchemy import (create_engine, MetaData, Table, Column,
    Integer, String, Date)

# TODO: Use an environment/config variable for this
engine = create_engine('sqlite:////Users/rjose/database/dovetail_dev.db',
        convert_unicode=True)
metadata = MetaData(bind=engine)

people_table = Table('people', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('picture', String(200)),
        Column('team', String(200)),
        Column('title', String(200)))

projects_table = Table('projects', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('target_date', Date()),
        Column('est_date', Date())
        )

project_participants_table = Table('project_participants', metadata,
        Column('project_id', Integer),
        Column('person_id', Integer)
        )
