# -*- coding: utf-8 -*-
# Desarrollado por Jose G. Duran C.
# Interface básica
# Condición de mejora: Absoluta - Puede mejorarse infinitamente
# Septiembre 2020
import sys
from sqlalchemy import Column, Integer, String, Sequence, Table
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

horario_curso = Table('horario_curso',
                      Base.metadata,
                      Column('curso_id', Integer, ForeignKey('cursos.id'),
                             primary_key=True),
                      Column('horario_id', Integer, ForeignKey('horariocursos.id'),
                             primary_key=True))


class Profesor(Base):
    __tablename__ = 'profesor'
    id = Column(Integer, Sequence('profesor_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    # Relación uno a muchos
    r_curso = relationship("ProfesorCurso", back_populates="r_profesor", cascade="all, delete")

    def __rep__(self):
        return "{}{}".format(self.firstname, self.lastname)


class Alumno(Base):
    __tablename__ = 'alumno'
    id = Column(Integer, Sequence('alumno_id_seq'), primary_key=True)
    code_personal = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    # Relación uno a uno con el alumno-curso
    r_curso = relationship("CursoAlumno", uselist=False, back_populates="r_alumno",
                           cascade="all, delete")

    def __rep__(self):
        return "{}{}".format(self.firstname, self.lastname)


class CursoAlumno(Base):
    __tablename__ = 'cursoalumno'
    id = Column(Integer, Sequence('cursoalumno_id_seq'), primary_key=True)
    code_personal = Column(String)
    code_curso = Column(String)

    # Relación uno a uno con el alumno
    alumno_id = Column(Integer, ForeignKey('alumno.id'))
    r_alumno = relationship("Alumno", back_populates="r_curso")

    # Relación uno a uno con el curso
    curso_id = Column(Integer, ForeignKey('cursos.id', ondelete="CASCADE"))
    r_cursos = relationship("Cursos", back_populates="r_alumnocurso")

    def __rep__(self):
        return "{}{}".format(self.code_personal, self.code_curso)


class ProfesorCurso(Base):
    __tablename__ = 'profesorcurso'
    id = Column(Integer, Sequence('profesorcurso_id_seq'), primary_key=True)
    code_personal = Column(String)
    code_curso = Column(String)

    # Relación uno a uno con el profesor
    profesor_id = Column(Integer, ForeignKey('profesor.id'))
    r_profesor = relationship("Profesor", back_populates="r_curso")

    # Relación uno a uno con el curso
    curso_id = Column(Integer, ForeignKey('cursos.id', ondelete="CASCADE"))
    r_cursos = relationship("Cursos", back_populates="r_profesorcurso")

    def __rep__(self):
        return "{}{}".format(self.code_personal, self.code_curso)


class Cursos(Base):
    __tablename__ = 'cursos'
    id = Column(Integer, Sequence('cursos_id_seq'), primary_key=True)
    code = Column(String)
    name = Column(String)
    descrip = Column(String)
    cpe = Column(String)

    # Relación muchos a muchos de horario-curso
    horarios_cursos = relationship('HorarioCurso', secondary=horario_curso,
                                   back_populates='horarios', cascade="all, delete")

    # Relación muchos a uno con el alumno-curso
    r_alumnocurso = relationship("CursoAlumno", back_populates="r_cursos",
                                 cascade="all, delete")

    # Relación muchos a uno con el profesor-curso
    r_profesorcurso = relationship("ProfesorCurso", back_populates="r_cursos",
                                   cascade="all, delete")

    def __rep__(self):
        return "{}{}".format(self.code, self.name,
                             self.descrip, self.cpe)


class HorarioCurso(Base):
    __tablename__ = 'horariocursos'
    id = Column(Integer, Sequence('horario_curso_id_seq'), primary_key=True)
    code_curso = Column(Integer)
    dia = Column(Integer)
    turno = Column(Integer)

    horarios = relationship('Cursos', secondary=horario_curso,
                            back_populates='horarios_cursos')

    def __rep__(self):
        return "{}".format(self.name)


engine = create_engine('sqlite:///escuela.db')
# engine = create_engine('sqlite:///:memory:')
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
            "2": self.registrar_profesor,
            "3": self.registrar_curso,
            "4": self.registrar_alumno_curso,
            "5": self.registrar_profesor_curso,
            "6": self.registrar_curso_horario,
            "7": self.regresar
        }

    def mostrar_menu(self):
        print("""
            Menu de Registro

            1  Registrar Alumno
            2  Registrar Profesor
            3  Registrar Cursos
            4  Asignar Curso al Alumno
            5  Asignar Profesor al Curso
            6  Registrar Horario de los Cursos
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
        x = session.query(Cursos).filter_by(code=v_codigo).first()
        if x is None:
            v_name = input('\nIndique nombre del curso: ')
            v_descrip = input('\nDescripción del curso: ')
            v_cpe = input('\nCantidad de créditos: ')
            v_curso = Cursos(code=v_codigo, name=v_name,
                             descrip=v_descrip, cpe=v_cpe)
            session.add(v_curso)
            session.commit()
        else:
            print('\n Código: ', x.code, 'Curso:', x.name,
                  'Créditos:', x.cpe)

    def registrar_alumno_curso(self):
        codigo_curso = input("\nIndique curso para asignar: ")
        x = session.query(Cursos).filter_by(code=codigo_curso).first()
        if x is None:
            print('\nCurso', codigo_curso, 'no existe en la base de datos')
        else:
            codigo_personal = input("\nIndique la identificación del alumno a registrar al curso: ")
            v_alumno = session.query(Alumno).filter_by(code_personal=codigo_personal).first()
            if v_alumno is None:
                print('\nAlumno', codigo_personal, 'no existe en la base de datos')
            else:
                v_curso = session.query(CursoAlumno).filter_by(code_curso=codigo_curso) \
                    .filter_by(code_personal=codigo_personal).all()
                if not v_curso:
                    v_curso = CursoAlumno(code_curso=codigo_curso, code_personal=codigo_personal,
                                          alumno_id=v_alumno.id, curso_id=x.id)
                    session.add(v_curso)
                    session.commit()
                else:
                    print('\nEl alumno: ',
                          codigo_personal, 'ya está inscrito en el curso: ', codigo_curso)

    def registrar_profesor_curso(self):
        codigo_curso = input("\nIndique curso para asignar: ")
        x = session.query(Cursos).filter_by(code=codigo_curso).first()
        if x is None:
            print('\nCurso', codigo_curso, 'no existe en la base de datos')
        else:
            codigo_personal = input("\nIndique la identificación del profesor a asignar al curso: ")
            v_profesor = session.query(Profesor).filter_by(code_personal=codigo_personal).first()
            if v_profesor is None:
                print('\nProfesor', codigo_personal, 'no existe en la base de datos')
            else:
                v_curso = session.query(ProfesorCurso).filter_by(code_curso=codigo_curso) \
                    .filter_by(code_personal=codigo_personal).all()
                if not v_curso:
                    v_curso = ProfesorCurso(code_curso=codigo_curso, code_personal=codigo_personal,
                                            profesor_id=v_profesor.id, curso_id=x.id)
                    session.add(v_curso)
                    session.commit()
                else:
                    print('\nEl Profesor: ',
                          codigo_personal, 'ya ha sido asignado al curso: ', codigo_curso)

    def registrar_curso_horario(self):
        codigo_curso = input("\nIndique curso para para programar horario: ")
        x = session.query(Cursos).filter_by(code=codigo_curso).first()
        if x is None:
            print('\nCurso', codigo_curso, 'no existe en la base de datos')
        else:
            dia_curso = input('\nIndique el día de la semana que desea asignar el curso: ')
            turno_curso = input('\n Indique el turno que desea asignar al curso (AM/PM): ')
            h_curso = session.query(HorarioCurso).filter_by(code_curso=codigo_curso) \
                .filter_by(dia=dia_curso) \
                .filter_by(turno=turno_curso).all()
            if not h_curso:
                x.horarios_cursos.append(HorarioCurso(code_curso=codigo_curso,
                                                      dia=dia_curso, turno=turno_curso))
                session.commit()
            else:
                print('\nEl curso ', codigo_curso, 'ya está asignado el ', dia_curso,
                      'en el turno ', turno_curso)

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
            Menu de Consultas

            1  Consultar Alumno 
            2  Consultar Profesor
            3  Consultar Curso
            4  Exportar información
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
            y = session.query(CursoAlumno).filter_by(id=code).first()
            if y is None:
                print('\n', x.id, x.lastname, x.firstname)
            else:
                code = x.id
                print(72 * "-")
                print('ID:', x.code_personal, 'Alumno:', x.lastname, x.firstname)
                print(72 * "-")
                for campo_1, campo_2 in session.query(Alumno, CursoAlumno). \
                    filter(Alumno.id == CursoAlumno.alumno_id).all():
                    # Acá debo buscar el curso en la tabla Cursos
                    codigo_curso = campo_2.code_curso
                    v_curso = session.query(Cursos).filter_by(code=codigo_curso).first()
                    # Luego imprimo los valores
                    print(campo_2.code_curso, v_curso.name)
                    # Este proceso puede ser optimizado mucho


    def consultar_profesor(self):
        v_codigo = input("\nIndique la identificación del profesor: ")
        x = session.query(Profesor).filter_by(code_personal=v_codigo).first()
        if y is None:
            print('\nProfesor no se encuentra registrado en la base de datos')
        else:
            code = x.id
            y = session.query(ProfesorCurso).filter_by(id=code).first()
            if y is None:
                print('\n', x.id, x.lastname, x.firstname)
            else:
                code = x.id
                print(72 * "-")
                print('ID:', x.code_personal, 'Profesor:', x.lastname, x.firstname)
                print(72 * "-")
                for campo_1, campo_2 in session.query(Profesor, ProfesorCurso). \
                        filter(Profesor.id == ProfesorCurso.profesor_id).all():
                    # Acá debo buscar el curso en la tabla Cursos
                    codigo_curso = campo_2.code_curso
                    v_curso = session.query(Cursos).filter_by(code=codigo_curso).first()
                    # Luego imprimo los valores
                    print(campo_2.code_curso, v_curso.name)
                    # Este proceso puede ser optimizado mucho

    def consultar_curso(self):
        v_codigo = input("\nIndique el código del curso a buscar: ")
        x = session.query(Cursos).filter_by(code=v_codigo).first()
        if x is None:
            print('\nEl curso', v_codigo, 'no se encuentra registrado en la base de datos')
        else:
            code = x.id
            y = session.query(HorarioCurso).filter(HorarioCurso.horarios.any(id=code)).all()
            if y is None:
                print('\n', x.id, x.name, x.cpe)
            else:
                code = x.id
                print(72 * "-")
                print('ID:', x.code, 'Curso:', x.name, 'UC:', x.cpe)
                print(72 * "-")
                for campo_1 in session.query(HorarioCurso).\
                        filter(HorarioCurso.horarios.any(id=code)).all():
                    # Acá debo buscar el curso en la tabla Cursos
                    codigo_curso = campo_1.code_curso
                    v_curso = session.query(Cursos).filter_by(code=codigo_curso).first()
                    # Luego imprimo los valores
                    print('Horario:', campo_1.id, 'Día:', campo_1.dia, 'Turno:', campo_1.turno)
                    # Este proceso puede ser optimizado mucho

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
            print('\nAlumno', v_codigo, 'no se encuentra registrado')
        else:
            print('\n Alumno:', x.firstname, x.lastname, 'Código:', x.id,
                  'ha sido eliminado en conjunto con sus relaciones')
            session.delete(x)
            session.commit()

    def eliminar_profesor(self):
        v_codigo = input("\nIndique la identificación del profesor que desea eliminar: ")
        x = session.query(Profesor).filter_by(code_personal=v_codigo).first()
        if x == None:
            print('\nProfesor', v_codigo,'no se encuentra registrado')
        else:
            print('\n Profesor:', x.firstname, x.lastname, 'Código:', x.id,
                  'ha sido eliminado en conjunto con sus relaciones')
            session.delete(x)
            session.commit()

    def eliminar_curso(self):
        v_codigo = input("\nIndique el código del curso: ")
        x = session.query(Cursos).filter_by(code=v_codigo).first()
        if x == None:
            print('\nEl código', v_codigo, 'no corresponde a algún curso de la base de datos')
        else:
            print('\n Código: ', x.code, '', x.name,
                  'ha sido eliminado en conjunto con sus relaciones')
            session.delete(x)
            session.commit()

    def regresar(self):
        m.run()


m = MenuPrincipal()
m.run()
