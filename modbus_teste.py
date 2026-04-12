from utils.modbus_utils import *
from pymodbus.client.sync import ModbusTcpClient
import time

while True:
    client = ModbusTcpClient('192.168.2.90', port=502)  # Specify the port.
    connection = client.connect()
    if connection:
        print("Conectou")
        produto = read_string(client, 8724, 10)
        print("Produto: ",produto)
        produto = read_decimal(client, 8850, 2)
        print("Peso: ",produto)
        produto = read_lote(client, 28596, 2)
        print("Lote: ",produto)
    else:
        print("Não Conectou")
    time.sleep(5)