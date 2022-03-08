from utils.modbus_utils import *
from pymodbus.client.sync import ModbusTcpClient

while True:
    client = ModbusTcpClient('192.168.0.10', port=502)  # Specify the port.
    connection = client.connect()
    if connection:
        print("Conectou")
        leitura = client.read_holding_registers(9251, 1)
        print(leitura[0])
    else:
        print("Não Conectou")