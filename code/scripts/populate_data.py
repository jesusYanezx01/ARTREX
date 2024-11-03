from app.models import db
from app.models import Category, Level

category1 = Category(name="Programación", description="Rutas enfocadas en aprender lenguajes de programación")
category2 = Category(name="Ciencia de Datos", description="Rutas que abordan el análisis y manipulación de datos")

level1 = Level(name="Principiante", description="Conceptos básicos para iniciar")
level2 = Level(name="Intermedio", description="Conocimientos necesarios para avanzar a un siguiente nivel")
level3 = Level(name="Avanzado", description="Contenido para expertos en la materia")

db.session.add_all([category1, category2, level1, level2, level3])

db.session.commit()

print("Datos de prueba agregados a las tablas 'categories' y 'levels'.")