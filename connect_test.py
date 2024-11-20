import pymssql

server = '52.167.231.145'
port = 51433
database = 'CreditoYCobranza'
username = 'credito'
password = 'Cr3d$.23xme'

try:
    conn = pymssql.connect(
        server=server,
        port=port,
        user=username,
        password=password,
        database=database
    )
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
