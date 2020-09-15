# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Column, Integer, String, Sequence, Table
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

horario_curso = Table('horario_curso',
                      Base.metadata,
                      Column('curso_id', Integer, ForeignKey('curso_bd.id'),
                             primary_key=True),
                      Column('horario_id', Integer, ForeignKey('horariocursos.id'),
                             primary_key=True))


horario_profesor = Table('horario_profesor',
                         Base.metadata,
                         Column('profesor_id', Integer, ForeignKey('profesor.id'),
                                primary_key=True),
                         Column('horario_id', Integer, ForeignKey('horario.id'),
                                primary_key=True))


class Horario(Base):
    __tablename__ = 'horario'
    id = Column(Integer, Sequence('horario_id_seq'), primary_key=True)
    dia = Column(String)
    turno = Column(String)
    code_curso = Column(String)

    # Relación muchos a muchos de profesor-curso
    t_profesores = relationship('Profesor', secondary=horario_profesor,
                                back_populates='t_horarios')

    def __rep__(self):
        return "{}{}".format(self.dia, self.hora)


class Profesor(Base):
    __tablename__ = 'profesor'
    id = Column(Integer, Sequence('profesor_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    # Relación muchos a muchos de profesor-curso
    t_horarios = relationship('Horario', secondary=horario_profesor,
                              back_populates='t_profesores')


    def __rep__(self):
        return "{}{}".format(self.firstname, self.lastname)


class Alumno(Base):
    __tablename__ = 'alumno'
    id = Column(Integer, Sequence('alumno_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    # Relación uno a uno con el alumno-curso
    r_curso = relationship("Curso", uselist=False, back_populates="r_alumno")

    def __rep__(self):
        return "{}{}".format(self.firstname, self.lastname)


class Curso(Base):
    __tablename__ = 'curso'
    id = Column(Integer, Sequence('curso_id_seq'), primary_key=True)
    code_personal = Column(String)
    code_curso = Column(String)

    # Relación uno a uno con el alumno-curso
    alumno_id = Column(Integer, ForeignKey('alumno.id'))
    r_alumno = relationship("Alumno", back_populates="r_curso")

    def __rep__(self):
        return "{}{}".format(self.code_personal, self.code_curso)


class Curso_BD(Base):
    __tablename__ = 'curso_bd'
    id = Column(Integer, Sequence('curso_bd_id_seq'), primary_key=True)
    code = Column(String)
    name = Column(String)
    descrip = Column(String)
    cpe = Column(String)

    # Relación muchos a muchos de horario-curso
    horarios_cursos = relationship('HorarioCurso', secondary=horario_curso,
                                   back_populates='horarios')

    def __rep__(self):
        return "{}{}".format(self.code, self.name,
                             self.descrip, self.cpe)


class HorarioCurso(Base):
    __tablename__ = 'horariocursos'
    id = Column(Integer, Sequence('horario_curso_id_seq'), primary_key=True)
    code_curso=Column(Integer)
    dia=Column(Integer)
    turno=Column(Integer)

    horarios = relationship('Curso_BD', secondary=horario_curso,
                            back_populates='horarios_cursos')

    def __rep__(self):
        return "{}".format(self.name)


engine = create_engine('sqlite:///escuela.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class MenuPrincipal:
    def __init__(self):
        self.elecciones = {
            "1": self.registro,
            "2": self.consultar,
            "3": self.eliminar,
            "4": self.salir
        }

    def mostrar_menu(self):
        print("""
            Menu Principal Escolar

            1  Registrar
            2  Consultar
            3  Eliminar
            4  Salir
            """)

    def run(self):
        while True:
            self.mostrar_menu()
            eleccion = input("Seleccione una opción: ")
            accion = self.elecciones.get(eleccion)
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def registro(self):
        r = MenuRegistro()
        r.run()

    def consultar(self):
        c = MenuConsulta()
        c.run()

    def eliminar(self):
        e = MenuElimina()
        e.run()

    def salir(self):
        print("\n Gracias por usar nuestro sistema Escolar")
        sys.exit(0)


class MenuRegistro:
    def __init__(self):
        self.elecciones = {
            "1": self.registrar_alumno,
            "2": self.registrar_alumno_curso,
            "3": self.registrar_profesor,
            "4": self.registrar_curso,
            "5": self.registrar_curso_horario,
            "6": self.registrar_profesor_horario,
            "7": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Registro

            1  Registrar Alumno
            2  Asignar Curso al Alumno
            3  Registrar Profesor
            4  Registrar Cursos
            5  Registrar Horario de los Cursos
            6  Registrar Horario de los Profesores
            7  Regresar al Menu Anterior
            """)

    def run(self):
        while True:
            self.mostrar_menu()
            eleccion = input("Seleccione una opción: ")
            accion = self.elecciones.get(eleccion)
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def registrar_alumno(self):
        v_codigo = input("\nIndique la identificación del alumno a registrar: ")
        x = session.query(Alumno).filter_by(code_personal=v_codigo).first()
        if x is None:
            v_name = input('\nIndique nombre: ')
            v_apellido = input('\nIndique apellido: ')
            v_persona = Alumno(code_personal=v_codigo, firstname=v_name, lastname=v_apellido)
            session.add(v_persona)
            session.commit()
        else:
            print('\n Alumno:', x.firstname, x.lastname, 'Código:', x.id)

    def registrar_alumno_curso(self):
        codigo_curso = input("\nIndique curso para asignar: ")
        x = session.query(Curso_BD).filter_by(code=codigo_curso).first()
        if x is None:
            print('\nCurso', codigo_curso, 'no existe en la base de datos')
        else:
            codigo_personal = input("\nIndique la identificación del alumno a registrar: ")
            v_alumno = session.query(Alumno).filter_by(code_personal=codigo_personal).first()
            if v_alumno is None:
                print('\nAlumno', codigo_personal, 'no existe en la base de datos')
            else:
                v_curso = session.query(Curso).filter_by(code_curso=codigo_curso)\
                    .filter_by(code_personal=codigo_personal).all()
                if not v_curso:
                    v_curso = Curso(code_curso=codigo_curso, code_personal=codigo_personal,
                                    alumno_id=v_alumno.id)
                    session.add(v_curso)
                    session.commit()
                else:
                    print('\nEl alumno: ',
                          codigo_personal, 'ya está inscrito en el curso: ', codigo_curso)


    def registrar_profesor(self):
        v_codigo = input("\nIndique la identificación del profesor a registrar: ")
        x = session.query(Profesor).filter_by(code_personal=v_codigo).first()
        if x is None:
            v_name = input('\nIndique nombre: ')
            v_apellido = input('\nIndique apellido: ')
            v_persona = Profesor(code_personal=v_codigo, firstname=v_name, lastname=v_apellido)
            session.add(v_persona)
            session.commit()
        else:
            print('\n Profesor:', x.firstname, x.lastname, 'Código:', x.id)

    def registrar_curso(self):
        v_codigo = input("\nIndique código del curso: ")
        x = session.query(Curso_BD).filter_by(code=v_codigo).first()
        if x is None:
            v_name = input('\nIndique nombre del curso: ')
            v_descrip = input('\nDescripción del curso: ')
            v_cpe = input('\nCantidad de créditos: ')
            v_curso = Curso_BD(code=v_codigo, name=v_name,
                            descrip=v_descrip, cpe=v_cpe)
            session.add(v_curso)
            session.commit()
        else:
            print('\n Código: ', x.code, 'Curso:', x.name,
                  'Créditos:', x.cpe)

    def registrar_curso_horario(self):
        codigo_curso = input("\nIndique curso para para programar horario: ")
        x = session.query(Curso_BD).filter_by(code=codigo_curso).first()
        if x is None:
            print('\nCurso', codigo_curso, 'no existe en la base de datos')
        else:
            dia_curso = input('\nIndique el día de la semana que desea asignar el curso: ')
            turno_curso = input('\n Indique el turno que desea asignar al curso (AM/PM): ')
            h_curso = session.query(Horario).filter_by(code_curso=codigo_curso)\
                .filter_by(dia=dia_curso)\
                .filter_by(turno=turno_curso).all()
            if not h_curso:
                h_curso = Horario(code_curso=codigo_curso, dia=dia_curso, turno=turno_curso)
                session.add(h_curso)
                x.horarios_cursos.append(HorarioCurso(code_curso=codigo_curso,
                                                           dia=dia_curso, turno=turno_curso))
                session.commit()

                pass
            else:
                print('\nEl curso ', codigo_curso, 'ya está asignado el ', dia_curso,
                      'en el turno' , turno_curso)


    def registrar_profesor_horario(self):
        pass

    def regresar(self):
        m.run()


class MenuConsulta:
    def __init__(self):
        self.elecciones = {
            "1": self.consultar_alumno,
            "2": self.consultar_profesor,
            "3": self.consultar_curso,
            "4": self.exportar_alumno,
            "5": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Consulta y Exportación de Alumnos

            1  Consultar Programa por Alumno 
            2  Consultar Programa por Profesor
            3  Consultar Programa por Curso
            4  Exportar Alumno
            5  Regresar al Menu Anterior
            """)

    def run(self):
        while True:
            self.mostrar_menu()
            eleccion = input("Seleccione una opción: ")
            accion = self.elecciones.get(eleccion)
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def consultar_alumno(self):
        v_codigo = input("\nIndique la identificación del alumno: ")
        x = session.query(Alumno).filter_by(code_personal=v_codigo).first()
        if x is None:
            print('\nAlumno no está registrado en la base de datos')
        else:
            code = x.id
            x = session.query(Curso).filter_by(id=code).first()
            if x is None:
                print('\nAlumno no se encuentra asignado a ningún programa')
            else:
                code = x.id
                for an_alumno, a_prg in session.query(Alumno, Curso). \
                        filter(Alumno.id == Curso.alumno_id). \
                        filter(Curso.id == code).all():
                    print(an_alumno.lastname, an_alumno.firstname)
                    print(a_prg, a_prg)


    def consultar_profesor(self):
        v_codigo = input("\nIndique la identificación del profesor: ")
        x = session.query(Profesor).filter_by(code_personal=v_codigo).first()
        if x is None:
            print('\nProfesor no se encuentra asignado a ningún programa')
        else:
            pass



    def consultar_curso(self):
        v_codigo = input("\nIndique el código del curso a buscar: ")
        x = session.query(Curso).filter_by(subject_code=v_codigo).first()
        if x is None:
            print('\nEl código de curso no se ha asignado a ningún programa')
        else:
            pass

    def exportar_alumno(self):
        pass

    def regresar(self):
        m.run()


class MenuElimina:
    def __init__(self):
        self.elecciones = {
            "1": self.eliminar_alumno,
            "2": self.eliminar_profesor,
            "3": self.eliminar_curso,
            "4": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Eliminación de Registros

            1  Eliminar Alumno
            2  Eliminar Profesor
            3  Eliminar Curso
            4  Regresar al Menu Anterior
            """)

    def run(self):
        while True:
            self.mostrar_menu()
            eleccion = input("Seleccione una opción: ")
            accion = self.elecciones.get(eleccion)
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def eliminar_alumno(self):
        v_codigo = input("\nIndique la identificación del alumno que desea eliminar: ")
        x = session.query(Alumno).filter_by(code_personal=v_codigo).first()
        if x == None:
            print('\nAlumno no se encuentra registrado')
        else:
            print('\n Alumno:', x.firstname, x.lastname, 'Código:', x.id,
                  'ha sido eliminado en conjunto con sus relaciones')
            session.delete(x)
            session.commit()

    def eliminar_profesor(self):
        v_codigo = input("\nIndique la identificación del profesor que desea eliminar: ")
        x = session.query(Profesor).filter_by(code_personal=v_codigo).first()
        if x == None:
            print('\nProfesor no se encuentra registrado')
        else:
            print('\n Profesor:', x.firstname, x.lastname, 'Código:', x.id,
                  'ha sido eliminado en conjunto con sus relaciones')
            session.delete(x)
            session.commit()

    def eliminar_curso(self):
        v_codigo = input("\nIndique el código del curso: ")
        x = session.query(Curso).filter_by(subject_code=v_codigo).first()
        if x == None:
            print('\nEl código no corresponde a algún curso escolar')
        else:
            print('\n Código: ', x.subject_code, 'Curso:', x.subject_name,
                  'ha sido eliminado en conjunto con sus relaciones')
            session.delete(x)
            session.commit()

    def regresar(self):
        m.run()


m = MenuPrincipal()
m.run()