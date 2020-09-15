# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Column, Integer, String, Sequence, Table
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

horario_curso = Table('horario_curso', Base.metadata,
                      Column('curso_id', Integer, ForeignKey('curso.id')),
                      Column('horario_id', Integer, ForeignKey('horario.id')))


class Horario(Base):
    __tablename__ = 'horario'
    id = Column(Integer, Sequence('horario_id_seq'), primary_key=True)
    dia = Column(String)
    hora = Column(String)

    cursos_hrs = relationship('Curso', secondary='horario_curso',
                              back_populates='horarios_cursos')
    prfs_hrs = relationship('Profesor', secondary='horario_curso',
                            back_populates='horarios_prfs')

    def __rep__(self):
        return "{}{}".format(self.dia, self.hora)

class Alumno(Base):
    __tablename__ = 'alumno'
    id = Column(Integer, Sequence('alumno_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    cursos_alumnos = relationship("Curso", order_by="Alumno.id", uselist=False,
                                  back_populates='alumnos_cursos')

    def __rep__(self):
        return "{}{}".format(self.firtsname, self.lastname)


class Curso(Base):
    __tablename__ = 'curso'
    id = Column(Integer, Sequence('curso_id_seq'), primary_key=True)
    subject_code = Column(String)
    subject_name = Column(String)
    subject_desc = Column(String)
    subject_cpe = Column(String)
    profesor_id = Column(Integer, ForeignKey('profesor.id'))
    alumno_id = Column(Integer, ForeignKey('alumno.id'))
    alumnos_cursos = relationship("Alumno", order_by="Alumno.id",
                                  back_populates='cursos_alumnos')

    horarios_cursos = relationship('Horario', back_populates='cursos_hrs',
                                    cascade="all, delete, delete-orphan")
    profesores_cursos = relationship("Profesor", back_populates='curso_prfs',
                                     cascade="all, delete, delete-orphan")

    def __rep__(self):
        return "{}{}".format(self.subject_code, self.subject_name,
                             self.subject_desc, self.subject_cpe)


class Profesor(Base):
    __tablename__ = 'profesor'
    id = Column(Integer, Sequence('profesor_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    curso_prfs = relationship('Curso', order_by='Curso.id', back_populates='profesores_cursos',
                              cascade='all, delete, delete-orphan')

    def __rep__(self):
        return "{}{}".format(self.firtsname, self.lastname)


engine = create_engine('sqlite:///escuela.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class MenuPrincipal:
    def __init__(self):
        self.elecciones = {
            "1": self.registro,
            "2": self.buscar,
            "3": self.asignar,
            "4": self.consultar,
            "5": self.eliminar,
            "6": self.salir
        }

    def mostrar_menu(self):
        print("""
            Menu Principal Escolar

            1  Registrar
            2  Buscar
            3  Asignar de recursos
            4  Consultar
            5  Eliminar
            6  Salir
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

    def buscar(self):
        b = MenuBuscar()
        b.run()

    def asignar(self):
        a = MenuAsignacion()
        a.run()

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
            "2": self.registrar_profesor,
            "3": self.registrar_curso,
            "4": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Registro

            1  Registrar Alumno
            2  Registrar Profesor
            3  Registrar Curso
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
        x = session.query(Curso).filter_by(subject_code=v_codigo).first()
        if x is None:
            v_name = input('\nIndique nombre del curso: ')
            v_descrip = input('\nDescripción del curso: ')
            v_cpe = input('\nCantidad de créditos: ')
            v_curso = Curso(subject_code=v_codigo, subject_name=v_name,
                            subject_desc=v_descrip, subject_cpe=v_cpe)
            session.add(v_curso)
            session.commit()
        else:
            print('\n Código: ', x.subject_code, 'Curso:', x.subject_name,
                  'Créditos:', x.subject_cpe)

    def regresar(self):
        m.run()


class MenuBuscar:
    def __init__(self):
        self.elecciones = {
            "1": self.buscar_alumno,
            "2": self.buscar_profesor,
            "3": self.buscar_curso,
            "4": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Búsqueda

            1  Buscar Alumno
            2  Buscar Profesor
            3  Buscar Curso
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

    def buscar_alumno(self):
        v_codigo = input("\nIndique la identificación del alumno: ")
        x = session.query(Alumno).filter_by(code_personal=v_codigo).first()
        if x is None:
            print('\nAlumno no se encuentra registrado')
        else:
            print('\n Alumno:', x.firstname, x.lastname, 'Código:', x.id)

    def buscar_profesor(self):
        v_codigo = input("\nIndique la identificación del profesor: ")
        x = session.query(Profesor).filter_by(code_personal=v_codigo).first()
        if x is None:
            print('\nProfesor no se encuentra registrado')
        else:
            print('\n Profesor:', x.firstname, x.lastname, 'Código:', x.id)

    def buscar_curso(self):
        v_codigo = input("\nIndique el código del curso: ")
        x = session.query(Curso).filter_by(subject_code=v_codigo).first()
        if x == None:
            print('\nEl código no corresponde a algún curso escolar')
        else:
            print('\n Código: ', x.subject_code, 'Curso:', x.subject_name,
                  'Créditos:', x.subject_cpe)

    def regresar(self):
        m.run()


class MenuAsignacion:
    def __init__(self):
        self.elecciones = {
            "1": self.asignar_curso_alumno,
            "2": self.asignar_curso_profesor,
            "3": self.asignar_horario_curso,
            "4": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Asignación de Materias

            1  Asignación de curso al alumno
            2  Asignación de curso al profesor
            3  Asignación de horario al curso
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

    def asignar_curso_alumno(self):
        v_codigo = input("\nIndique la identificación del alumno: ")
        x = session.query(Alumno).filter_by(code_personal=v_codigo).first()
        if x is None:
            print('\nAlumno no está registrado en la base de datos')
        else:
            v_curso = input("\nIndique el curso que desea asignar al alumno:")
            y = session.query(Curso).filter_by(subject_code=v_curso).first()
            if y is None:
                print('\nCurso no está registrado en la base de datos')
            else:
                pass

            #v_codigo.programas[Programa()]


    def asignar_curso_profesor(self):
        pass

    def asignar_horario_curso(self):
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
                    print(an_alumno.lastname, an_alumno.firtsname)
                    print(a_prg.prg_code, a_prg.prg_name)


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