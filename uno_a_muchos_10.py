# -*- coding: utf-8 -*-
'''Debo crear una tabla para los cursos y dejar la que tengo como la tabla
relacional. Eso lo hago el 22-08'''


from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///relationship.db')
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Alumno(Base):
    __tablename__ = 'alumno'
    id = Column(Integer, Sequence('alumno_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    subjects = relationship("Subject", order_by="Subject.id", back_populates='studs',
                            cascade="all, delete, delete-orphan")

    def __rep__(self):
        return "{}{}".format(self.firtsname, self.lastname)


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, Sequence('subject_id_seq'), primary_key=True)
    subject_code = Column(String)
    subject_name = Column(String)
    subject_cpe = Column(String)
    subject_desc = Column(String)
    alumno_id = Column(Integer, ForeignKey('alumno.id'))
    studs = relationship("Alumno", back_populates='subjects')

    def __rep__(self):
        return "{}{}".format(self.subject_code, self.subject_name)


def ver_datos():  # Esta función la hice para ver el efecto en las tablas
    print("")
    print("   ID \t    Apellidos  \t  Nombres")
    print("__________________________________")
    for campos in session.query(Alumno).order_by(Alumno.lastname):
        print(campos.code_personal, campos.lastname, campos.firstname)
    session.close()
    print('')


def ver_datos_dos():  # Esta función la hice para ver el efecto en las tablas
    print("")
    print("   ID \t    Campo I    \t  Campo II     \t  Campo III    \t  Campo IV")
    print("__________________________________________________________________")
    for campos in session.query(Subject).order_by(Subject.id):
        print(campos.id, campos.subject_name, campos.subject_desc, campos.subject_cpe, campos.alumno_id)
    session.close()
    print('')


session.add_all({
    Alumno(code_personal='111979456', firstname='Victoria', lastname='Duran V.'),
    Alumno(code_personal='111979457', firstname='Javier A.', lastname='Duran A.'),
    Alumno(code_personal='111979458', firstname='Jose A.', lastname='Duran C.'),
    Alumno(code_personal='111979459', firstname='Jose G.', lastname='Duran C.'),
    Alumno(code_personal='111979455', firstname='Betsy N.', lastname='Valenzuela S.'),
    Alumno(code_personal='111979454', firstname='Marcela S.', lastname='Duran E.'),
    Alumno(code_personal='111979453', firstname='Ana F.', lastname='Cáceres O.')})

session.commit()

def agregar_alumno(self, codigo):
    pass


def agregar_materia(self, codigo):
    pass

j_alumno = session.query(Alumno).filter_by(code_personal='111979456').first()



j_alumno.subjects = [Subject(subject_code='9788498387087', subject_name='Introducción a la Programación',
                     subject_desc='Desarrollo de las capacidades para programar', subject_cpe='4'),
                     Subject(subject_code='9788498382679', subject_name='Programación orientada a objeto',
                     subject_desc='Dominio del manejo de objetos en la programación', subject_cpe='4')]


session.add(j_alumno)
session.commit()


ver_datos()
ver_datos_dos()


#print("")
#print("Query #1")
#for an_a, a_s in session.query(Alumno, Subject). \
#        filter(Alumno.id == Subject.alumno_id). \
#        filter(Subject.subject_code == '9788498387087'). \
#        all():
#    print(an_a.lastname, ',', an_a.firstname, '-', a_s.subject_name)