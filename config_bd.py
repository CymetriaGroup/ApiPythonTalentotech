from pymysql import connect

def obtener_conexion():
    host = 'localhost'
    user = 'campusbogota_admin_talento_tech'
    password = '54QPw7#O8]?B'
    db = 'campusbogota_bd_talento_tech'
    try:
        conexion = connect(host=host, user=user, password=password, database=db)
        return conexion
    except Exception as e:
        print(e)
        return None
