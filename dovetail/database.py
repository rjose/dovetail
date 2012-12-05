from datetime import datetime
from sqlalchemy import (create_engine, MetaData, Table, Column,
    Integer, String, Date, Float, Boolean)

# TODO: Use an environment/config variable for this
engine = create_engine('sqlite:////Users/rjose/database/dovetail_dev.db')
metadata = MetaData(bind=engine)

people = Table('people', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('picture', String(200)),
        Column('team', String(200)),
        Column('title', String(200)))

projects = Table('projects', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('is_deleted', Boolean, default = False),
        Column('is_done', Boolean, default = False),
        Column('value', Float),
        Column('target_date', Date()),
        Column('est_end_date', Date())
        )

project_participants = Table('project_participants', metadata,
        Column('project_id', Integer),
        Column('person_id', Integer)
        )

work = Table('work', metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String(200)),
        Column('is_deleted', Boolean, default = False),
        Column('is_done', Boolean, default = False),
        Column('assignee_id', Integer),
        Column('multiple_assignee_ids', String(200)),
        Column('project_id', Integer),
        Column('effort_left_d', Float),

        Column('topo_order', Integer),
        Column('value', Float),
        Column('key_date', Date()),
        Column('start_date', Date()),
        Column('end_date', Date()),
        Column('prereqs', String(200))
        )


