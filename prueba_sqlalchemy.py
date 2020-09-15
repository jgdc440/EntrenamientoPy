# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, ForeignKey, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import aliased

engine = create_engine('sqlite:///prueba_indices.db')
Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    personal_id = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    books = relationship("Book", order_by="Book.id", back_populates='author',
                         cascade="all, delete, delete-orphan")

    def __rep__(self):
        return "{}{}".format(self.firtsname, self.lastname)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    isbn = Column(String)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates='books')

    def __rep__(self):
        return "{}{}".format(self.firtsname, self.lastname)


def ver_datos():  # Esta función la hice para ver el efecto en las tablas
    print("")
    print("   ID \t    Apellidos  \t  Nombres")
    print("__________________________________")
    for campos in session.query(Author).order_by(Author.lastname):
        print(campos.personal_id, campos.lastname, campos.firstname)
    session.close()
    print('')


def ver_datos_dos():  # Esta función la hice para ver el efecto en las tablas
    print("")
    print("   ID \t    Campo I    \t  Campo II     \t  Campo III")
    print("_______________________________________________________")
    for campos in session.query(Book).order_by(Book.id):
        print(campos.id, campos.isbn, campos.title, campos.description)
    session.close()
    print('')


# Guardar objetos en la BD - Agregar un registro
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
author = Author(personal_id='111979464', firstname='Joanne', lastname='Rowling')
session.add(author)

our_author = session.query(Author).filter_by(firstname='Joanne').first()
if author is our_author:  # Validar si un campo coincide
    print("\nNuestro autor coincide con el primer registro de la tabla")

# Puedo agregar múltiples registros
session.add_all([
    Author(personal_id='111979461', firstname='John Ronald Reuel', lastname='Talkien'),
    Author(personal_id='111979457', firstname='Jose', lastname='Hernandez'),
    Author(personal_id='111979458', firstname='Robert Louis', lastname='Stevenson'),
    Author(personal_id='111979459', firstname='Arthur Ignatius', lastname='Conan Doyle'),
    Author(personal_id='111979460', firstname='Honore', lastname='Balzac'),
    Author(personal_id='111979456', firstname='Jose', lastname='Duran'),
    Author(personal_id='111979462', firstname='Fiodor', lastname='Dostoyevski')])

another_author = Author(personal_id='111979463', firstname='Jose', lastname='Saramago')
session.add(another_author)

print("Cuántos registros nuevos: ", len(session.new))  # Permite saber que hay nuevo antes del commit()

session.query(Author).filter_by(firstname='Joanne')
author.firstname = 'Joanne K.'  # Para cambiar antes de un commit

for autores in session.query(Author):  # Esta es una mejor forma de corregir errores en campos antes del commit()
    if autores.lastname == 'Duran':
        autores.firstname = 'Jose G.'

print("Cuántos registros que cambian antes del commit: ", len(session.dirty))  # Saber qué cambia antes del commit()

session.commit()

# Otras Consultas
print('\nQuery:1')
for instance in session.query(Author).order_by(Author.id):
    print(instance.firstname, instance.lastname)

print('\nQuery:2')
for firtsname, lastname in session.query(Author.firstname, Author.lastname).order_by(Author.lastname):
    print(firtsname, lastname)

print('\nQuery:3')
for row in session.query(Author.lastname).order_by(Author.id).all():
    print(row.lastname)

print('\nQuery:4')
for row in session.query(Author.lastname.label('firstname_label')).order_by(Author.id).all():
    print(row.firstname_label)

print('\nQuery:5')
author_alias = aliased(Author, name='author_alias')
for row in session.query(author_alias, author_alias.firstname):
    print(row.firstname)

print('\nQuery:6')
for an_author in session.query(Author).order_by(Author.id)[1:3]:
    print(an_author.lastname)

print('\nQuery:7')
for name in session.query(Author).filter_by(firstname='Jose'):
    print(name.lastname)

print('\nQuery:8')
for name in session.query(Author.id, Author.firstname, Author.lastname).filter_by(lastname='Saramago'):
    print(name)

print('\nQuery:9')
for an_author in session.query(Author.id). \
        filter_by(firstname='Jose'). \
        filter_by(lastname='Hernandez'):
    print(an_author)

print('\nQuery:10')
print(session.query(Author.firstname).filter_by(firstname='Jose').count())

print('\nQuery:11')
print(session.query(Author).filter(Author.firstname.like('Jo%')).count())

# Agregar registros con una relacion
j_autor = Author(personal_id='111979464', firstname='Joanne', lastname='Rowling')

j_autor.books = [Book(isbn='9788498387087', title='Harry Potter y la Piedra Filosofal',
                 description='La vida de Harry Potter cambia para siempre el...'),
                 Book(isbn='9788498382679',
                 title='Harry Potter y la cámara secreta',
                 description='Tras derrotar una vez más a lord Voldemort,...')]


session.add(j_autor)
session.commit()

j_autor = session.query(Author).filter_by(firstname='Joanne').one()

print("")
print("Query #1")
for an_author, a_book in session.query(Author, Book). \
        filter(Author.id == Book.author_id). \
        filter(Book.isbn == '9788498387087'). \
        all():
    print(an_author.lastname)
    print(a_book.title)

ver_datos()
ver_datos_dos()

print("Query #2")
print(session.query(Author.firstname, Author.lastname).join(Book).
      filter(Book.isbn == '9788498387087').
      all())

print("Query #3")
print(session.query(Author).join(Book, Author.id == Book.author_id).all())

print("Query #4")
print(session.query(Author).join(Author.books).all())

print("Query #5")
print(session.query(Author).join(Book, Author.books).all())

print("Query #6")
print(session.query(Author).join('books').all())

print("Query #7")
stmt = exists().where(Book.author_id == Author.id)
for name in session.query(Author.firstname).filter(stmt):
    print(name)

print("Query #8")
for name in session.query(Author.firstname). \
        filter(Author.books.any(Author.lastname.like('%Row%'))):
    print(name)

print("Query #10")
print(session.query(Book).filter(Book.author.has(Author.firstname == 'Joanne')).all())

# Borrado de autor
session.delete(j_autor)

print(session.query(Author.firstname).filter_by(firstname='Joanne').count())
print(session.query(Book.isbn).filter(Book.isbn.in_(['9788498387087', '9788498382679'])).count())
