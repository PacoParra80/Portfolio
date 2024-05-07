from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#engine
engine = create_engine("sqlite:///database/tareas.db", connect_args={"check_same_thread":False})

#sesión
Session = sessionmaker(bind=engine)
session = Session()


#vinculación
Base = declarative_base()

#Ahora en models.py, en cada clase (modelo), añadimos esta variable si queremos vincularla a la tabla