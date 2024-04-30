from config_bd import obtener_conexion
from datetime import datetime
import uuid
class Estudiante():
    def __init__(self, nombre, apellido, fecha_nacimiento, tipo_documento, num_documento, departamento, municipio, localidad, telefono, email, password, id_administrador):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.tipo_documento = tipo_documento
        self.num_documento = num_documento
        self.departamento = departamento
        self.municipio = municipio
        self.localidad = localidad
        self.telefono = telefono
        self.email = email
        self.password = password
        self.id_administrador = id_administrador

    def guardar(self):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """INSERT INTO estudiantes (id, nombres, apellidos, fecha_nacimiento, email, tipo_documento, num_documento, departamento, municipio, localidad, telefono, password, idAdministrador, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"""
                cursor.execute(consulta, (uuid.uuid4(), self.nombre, self.apellido, self.fecha_nacimiento, self.email, self.tipo_documento, self.num_documento, self.departamento, self.municipio, self.localidad, self.telefono, self.password, self.id_administrador, datetime.now(), datetime.now()))
            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def verificarAdministrador(self):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """SELECT id FROM administrador WHERE id = %s"""
                cursor.execute(consulta, (self.id_administrador))
                resultado = cursor.fetchone()
                if resultado:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False
    def verificarSiExisteEstudiante(self):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """SELECT id FROM estudiantes WHERE email = %s and num_documento = %s and idAdministrador = %s"""
                cursor.execute(consulta, (self.email, self.num_documento, self.id_administrador))
                resultado = cursor.fetchone()
                if resultado:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False
    def verificarSiExisteEmail(self):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                print(self.email)
                consulta = """SELECT id FROM estudiantes WHERE email = %s"""
                cursor.execute(consulta, (self.email))
                resultado = cursor.fetchone()
                if resultado:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False
    def verificarSiExisteNumeroDocumento(self):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                print(self.num_documento)
                consulta = """SELECT id FROM estudiantes WHERE num_documento = %s"""
                cursor.execute(consulta, (self.num_documento))
                resultado = cursor.fetchone()
                if resultado:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False
        
    def guardarResultId(self):
        uudi_estudiante = uuid.uuid4()
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """INSERT INTO estudiantes (id, nombres, apellidos, fecha_nacimiento, email, tipo_documento, num_documento, departamento, municipio, localidad, telefono, password, idAdministrador, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"""
                cursor.execute(consulta, (uudi_estudiante, self.nombre, self.apellido, self.fecha_nacimiento, self.email, self.tipo_documento, self.num_documento, self.departamento, self.municipio, self.localidad, self.telefono, self.password, self.id_administrador, datetime.now(), datetime.now()))
            conexion.commit()
            conexion.close()
            return uudi_estudiante
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def crearEstadoCurso(id_estudiante, id_curso):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """INSERT INTO estado_curso_estudiante (id, idEstudiante, idCurso, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(consulta, (uuid.uuid4(), id_estudiante, id_curso, datetime.now(), datetime.now()))
            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def crearCalificaciones(id_estudiante, id_curso):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """INSERT INTO calificaciones (id, idEstudiante, idCurso, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(consulta, (uuid.uuid4(), id_estudiante, id_curso, datetime.now(), datetime.now()))
            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def obtenerCupoCurso(id_curso):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """SELECT cupo FROM cursos WHERE id = %s"""
                cursor.execute(consulta, (id_curso))
                resultado = cursor.fetchone()

                if resultado:
                    return resultado[0]
                else:
                    return False
                
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def contarEstudiantesCurso(id_curso):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """SELECT COUNT(*) AS cantidad FROM estado_curso_estudiante WHERE idCurso = %s"""
                cursor.execute(consulta, (id_curso))
                resultado = cursor.fetchone()
                if resultado:
                    return resultado[0]
                else:
                    return False
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def obtenerEstudiantePorDocumento(num_documento):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """SELECT id, nombres, apellidos FROM estudiantes WHERE num_documento = %s"""
                cursor.execute(consulta, (num_documento))
                resultado = cursor.fetchone()
                return resultado
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def estudianteYaEnCurso(id_estudiante, id_curso):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = """SELECT id FROM estado_curso_estudiante WHERE idEstudiante = %s AND idCurso = %s"""
                cursor.execute(consulta, (id_estudiante, id_curso))
                resultado = cursor.fetchone()
                return bool(resultado)
        except Exception as e:
            print(e)
            return False
           