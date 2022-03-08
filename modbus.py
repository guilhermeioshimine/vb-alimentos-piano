from utils.modbus_utils import *
from models.models import *
from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
import time
import logging

logging.basicConfig(
    filename = "modbus.log",
    level = logging.DEBUG,
    format = "%(asctime)s :: %(levelno)s :: %(lineno)d")

logger = logging.getLogger('root')

def modbus_read():
    # client = ModbusTcpClient('192.168.1.12', port=502)  # Specify the port.
    client = ModbusTcpClient('192.168.0.10', port=502)  # Specify the port.
    connection = client.connect()
    result = []
    leitura = False
    if connection:
        print("Conectou")
        leitura = client.read_holding_registers(8002, 1)  # Specify the unit.       16bits tenho que ler o 5 
        if(leitura.isError() == False):
            leitura = leitura.registers
        else:
            return
        print(leitura[0])
        if(leitura[0] != 0):
            print("Lendo Registradores")
            time.sleep(2)

            receita = read_string(client, 8684, 10)
            result.append(receita)

            produto01 = read_string(client, 8694, 10)
            result.append(produto01)

            peso01 = read_decimal(client, 8844, 2)
            result.append(peso01)

            produto02 = read_string(client, 8704, 10)
            result.append(produto02)

            peso02 = read_decimal(client, 8846, 2)
            result.append(peso02)

            produto03 = read_string(client, 8714, 10)
            result.append(produto03)

            peso03 = read_decimal(client, 8848, 2)
            result.append(peso03)

            produto04 = read_string(client, 8724, 10)
            result.append(produto04)

            peso04 = read_decimal(client, 8850, 2)
            result.append(peso04)

            produto05 = read_string(client, 8734, 10)
            result.append(produto05)

            peso05 = read_decimal(client, 8852, 2)
            result.append(peso05)

            produto06 = read_string(client, 8744, 10)
            result.append(produto06)

            peso06 = read_decimal(client, 8854, 2)
            result.append(peso06)

            produto07 = read_string(client, 8754, 10)
            result.append(produto07)
            
            peso07 = read_decimal(client, 8856, 2)
            result.append(peso07)

            produto08 = read_string(client, 8764, 10)
            result.append(produto08)

            peso08 = read_decimal(client, 8858, 2)
            result.append(peso08)

            produto09 = read_string(client, 8774, 10)
            result.append(produto09)

            peso09 = read_decimal(client, 8860, 2)
            result.append(peso09)

            produto10 = read_string(client, 8784, 10)
            result.append(produto10)

            peso10 = read_decimal(client, 8862, 2)
            result.append(peso10)

            produto11 = read_string(client, 8794, 10)
            result.append(produto11)

            peso11 = read_decimal(client, 8864, 2)
            result.append(peso11)

            produto12 = read_string(client, 8804, 10)
            result.append(produto12)

            peso12 = read_decimal(client, 8866, 2)
            result.append(peso12)

            produto13 = read_string(client, 8814, 10)
            result.append(produto13)

            peso13 = read_decimal(client, 8868, 2)
            result.append(peso13)

            produto14 = read_string(client, 8824, 10)
            result.append(produto14)

            peso14 = read_decimal(client, 8870, 2)
            result.append(peso14)

            produto15 = read_string(client, 8834, 10)
            result.append(produto15)

            peso15 = read_decimal(client, 8872, 2)
            result.append(peso15)

            
            
            writeInt(0, 8002, client)
    
        client.close()
        return result
        
    else:
        print('Connection lost, Try again')

while True:
    x = modbus_read()
    time.sleep(1)
    if(x):   
        try:
            Report.create(
                report_data = datetime.now(),
                recipe      = x[0],
                product1    = x[1],
                weight1     = x[2],
                product2    = x[3],
                weight2     = x[4],
                product3    = x[5],
                weight3     = x[6],
                product4    = x[7],
                weight4     = x[8],
                product5    = x[9],
                weight5     = x[10],
                product6    = x[11],
                weight6     = x[12],
                product7    = x[13],
                weight7     = x[14],
                product8    = x[15],
                weight8     = x[16],
                product9    = x[17],
                weight9     = x[18],
                product10   = x[19],
                weight10    = x[20],
                product11   = x[21],
                weight11    = x[22],
                product12   = x[23],
                weight12    = x[24],
                product13   = x[25],
                weight13    = x[26],
                product14   = x[27],
                weight14    = x[28],
                product15   = x[29],
                weight15    = x[30],
                sum1        = x[2] + x[4] + x[6] + x[8] + x[10] + x[12] + x[14] + x[16] + x[18] + x[20] + x[22],
                sum2        = x[24] + x[26] + x[28] + x[30]
            )       
        except Exception as er: 
            print(er)
            logger.debug("Erro ao salvar Relatório")
