from flask import Blueprint, request
import pandas as pd
from io import BytesIO
import bcrypt 
from .estudiante_bd import Estudiante

estudiantes = Blueprint('estudiantes', __name__)


# Este endpoint sube los estudiantes sin asignar a un curso
@estudiantes.route('/estudiantes-excel', methods=['POST'])
def estudiantes_excel():
    if 'file' not in request.files:
        return {"ok": False, "message": "No se ha enviado el archivo"}

    file = request.files['file']
    if file.filename == '':
        return {"ok": False, "message": "No se ha seleccionado ningún archivo"}
    if not file.filename.endswith('.xlsx'):
        return {"ok": False, "message": "El archivo no es un .xlsx"}

    id_admin = request.form.get('id_admin')

    df = pd.read_excel(BytesIO(file.read()), engine='openpyxl', dtype=str)
    df.dropna(how='all', inplace=True)
    estudiantes_guardados = 0
    errores = []

    for index, row in df.iterrows():
        try:
            # Convertir la fecha de Excel a formato de fecha Python
            fecha_nacimiento = pd.to_datetime(row['Fecha de nacimiento'], errors='coerce').strftime('%Y-%m-%d') if pd.notnull(row['Fecha de nacimiento']) else None 
            # Crear y guardar el estudiante
            estudiante = Estudiante(
                str(row['Nombre']), str(row['Apellido']), fecha_nacimiento,
                str(row['Tipo de documento']), str(row['Número de documento']),
                str(row['Departamento']), str(row['Municipio']), str(row['Localidad']),
                str(row['Teléfono']), str(row['Email'].lower()),
                bcrypt.hashpw(str(row['Número de documento']).encode('utf-8'), bcrypt.gensalt()), 
                id_admin
            )
            if not estudiante.verificarAdministrador():
                return {"ok": False, "message": f"El administrador con id {id_admin} no existe"}
            
            if estudiante.verificarSiExisteEmail() or estudiante.verificarSiExisteNumeroDocumento():
                errores.append(f"El estudiante {estudiante.nombre} {estudiante.apellido} ya existe")
                continue
            if estudiante.guardar():
                estudiantes_guardados += 1
            else:
                errores.append(f"Error al guardar el estudiante en la fila {index + 1}")
        except Exception as e:
            errores.append(f"Error en la fila {index + 1}: {e}")

    if estudiantes_guardados > 0 and not errores:
        return {"ok": True, "message": f"{estudiantes_guardados} estudiantes guardados"} , 201
    elif errores:
        print(errores)
        return {"ok": False, "message": "Algunos estudiantes no se guardaron", "errores": errores} , 400
    else:
        return {"ok": False, "message": "Ningún estudiante fue guardado"} , 400
    
# Este endpoint sube los estudiantes y los asigna a un curso
@estudiantes.route('/estudiantes-excel-curso', methods=['POST'])
def estudiantes_excel_curso():
    if 'file' not in request.files:
        return {"ok": False, "message": "No se ha enviado el archivo"}

    file = request.files['file']
    if file.filename == '':
        return {"ok": False, "message": "No se ha seleccionado ningún archivo"}
    if not file.filename.endswith('.xlsx'):
        return {"ok": False, "message": "El archivo no es un .xlsx"}

    id_admin = request.form.get('id_admin')
    id_curso = request.form.get('id_curso')

    cupo_curso = Estudiante.obtenerCupoCurso(id_curso)
    estudiantes_curso = Estudiante.contarEstudiantesCurso(id_curso)
    if estudiantes_curso >= cupo_curso:
        return {"ok": False, "message": "El cupo del curso ya está lleno"}

    df = pd.read_excel(BytesIO(file.read()), engine='openpyxl', dtype=str)
    df.dropna(how='all', inplace=True)
    estudiantes_guardados = 0
    errores = []

    for index, row in df.iterrows():
        try:
            # Convertir la fecha de Excel a formato de fecha Python
            fecha_nacimiento = pd.to_datetime(row['Fecha de nacimiento']).strftime('%Y-%m-%d')
            # Crear y guardar el estudiante
            estudiante = Estudiante(
                str(row['Nombre']), str(row['Apellido']), fecha_nacimiento,
                str(row['Tipo de documento']), str(row['Número de documento']),
                str(row['Departamento']), str(row['Municipio']), str(row['Localidad']),
                str(row['Teléfono']), str(row['Email'].lower()),
                bcrypt.hashpw(str(row['Número de documento']).encode('utf-8'), bcrypt.gensalt()), 
                id_admin
            )
            if estudiante.verificarSiExisteEmail() or estudiante.verificarSiExisteNumeroDocumento():
                errores.append(f"El estudiante {estudiante.nombre} {estudiante.apellido} ya existe")
                continue

            estudiante_id = estudiante.guardarResultId()
            if estudiante_id:
                estudiantes_curso += 1
                if estudiantes_curso > cupo_curso:
                    errores.append(f"No se pudo inscribir a {estudiante.nombre} {estudiante.apellido} porque el cupo del curso está lleno"), 400
                    break
                estudiante.crearEstadoCurso(estudiante_id, id_curso)
                estudiante.crearCalificaciones(estudiante_id, id_curso)
                estudiantes_guardados += 1
            else:
                errores.append(f"Error al guardar el estudiante en la fila {index + 1}")
        except Exception as e:
            errores.append(f"Error en la fila {index + 1}: {e}")

    if estudiantes_guardados > 0 and not errores:
        print(estudiantes_guardados)
        return {"ok": True, "message": f"{estudiantes_guardados} estudiantes guardados"}, 201
    elif errores:
        print(errores)
        return {"ok": False, "message": "Algunos estudiantes no se guardaron", "errores": errores}, 400
    else:
        print(errores)
        return {"ok": False, "message": "Ningún estudiante fue guardado"} , 400

# Este endpoint asigna estudiantes a un curso
@estudiantes.route('/asignar-estudiantes-curso-excel', methods=['POST'])
def asignar_estudiantes_curso_excel():
    if 'file' not in request.files:
        return {"ok": False, "message": "No se ha enviado el archivo"}

    file = request.files['file']
    if file.filename == '':
        return {"ok": False, "message": "No se ha seleccionado ningún archivo"}
    if not file.filename.endswith('.xlsx'):
        return {"ok": False, "message": "El archivo no es un .xlsx"}

    id_curso = request.form.get('id_curso')

    if not id_curso:
        return {"ok": False, "message": "El ID del curso es requerido"}

    df = pd.read_excel(BytesIO(file.read()), engine='openpyxl', dtype=str)
    df.dropna(how='all', inplace=True)
    estudiantes_asignados = 0
    errores = []

    cupo_curso = Estudiante.obtenerCupoCurso(id_curso)
    estudiantes_curso = Estudiante.contarEstudiantesCurso(id_curso)

    for num_documento in df['Número de documento']:
        try:
            if estudiantes_curso >= cupo_curso:
                errores.append(f"El cupo del curso está lleno, no se pueden asignar más estudiantes")
                break

            estudiante = Estudiante.obtenerEstudiantePorDocumento(num_documento)
            if not estudiante:
                errores.append(f"No se encontró el estudiante con número de documento {num_documento}")
                continue
            print(estudiante[0])
            if Estudiante.estudianteYaEnCurso(estudiante[0], id_curso):
                errores.append(f"El estudiante con número de documento {num_documento} ya está asignado a este curso")
                continue

            if Estudiante.crearEstadoCurso(estudiante[0], id_curso) and Estudiante.crearCalificaciones(estudiante[0], id_curso):
                estudiantes_asignados += 1
                estudiantes_curso += 1
            else:
                errores.append(f"Error al asignar el estudiante con número de documento {num_documento} al curso")

        except Exception as e:
            errores.append(f"Error al procesar el estudiante con número de documento {num_documento}: {e}")

    if estudiantes_asignados > 0 and not errores:
        return {"ok": True, "message": f"{estudiantes_asignados} estudiantes asignados al curso"}, 201
    elif errores:
        return {"ok": False, "message": "Algunos estudiantes no se asignaron", "errores": errores}, 400
    else:
        return {"ok": False, "message": "Ningún estudiante fue asignado al curso"}, 400
