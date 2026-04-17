from utils.modbus_utils import *
from models.models import *
from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
import time

def modbus_read():
    client = ModbusTcpClient('192.168.2.90', port=502)  # Specify the port.
    #client = ModbusTcpClient('192.168.0.10', port=502)  # Specify the port.
    connection = client.connect()
    result = []
    leitura = False
    if connection:
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

            produto01 = read_string(client, 8694, 9)
            result.append(produto01)

            peso01 = read_decimal(client, 8844, 2)
            result.append(peso01)

            lote01 = read_lote(client, 28590, 2)
            result.append(lote01)

            produto02 = read_string(client, 8704, 9)
            result.append(produto02)

            peso02 = read_decimal(client, 8846, 2)
            result.append(peso02)

            lote02 = read_lote(client, 28592, 2)
            result.append(lote02)

            produto03 = read_string(client, 8714, 9)
            result.append(produto03)

            peso03 = read_decimal(client, 8848, 2)
            result.append(peso03)

            lote03 = read_lote(client, 28594, 2)
            result.append(lote03)

            produto04 = read_string(client, 8724, 9)
            result.append(produto04)

            peso04 = read_decimal(client, 8850, 2)
            result.append(peso04)

            lote04 = read_lote(client, 28596, 2)
            result.append(lote04)

            produto05 = read_string(client, 8734, 9)
            result.append(produto05)

            peso05 = read_decimal(client, 8852, 2)
            result.append(peso05)

            lote05 = read_lote(client, 28598, 2)
            result.append(lote05)

            produto06 = read_string(client, 8744, 9)
            result.append(produto06)

            peso06 = read_decimal(client, 8854, 2)
            result.append(peso06)

            lote06 = read_lote(client, 28600, 2)
            result.append(lote06)

            produto07 = read_string(client, 8754, 9)
            result.append(produto07)
            
            peso07 = read_decimal(client, 8856, 2)
            result.append(peso07)

            lote07 = read_lote(client, 28602, 2)
            result.append(lote07)

            produto08 = read_string(client, 8764, 9)
            result.append(produto08)

            peso08 = read_decimal(client, 8858, 2)
            result.append(peso08)

            lote08 = read_lote(client, 28604, 2)
            result.append(lote08)

            produto09 = read_string(client, 8774, 9)
            result.append(produto09)

            peso09 = read_decimal(client, 8860, 2)
            result.append(peso09)

            lote09 = read_lote(client, 28606, 2)
            result.append(lote09)

            produto10 = read_string(client, 8784, 9)
            result.append(produto10)

            peso10 = read_decimal(client, 8862, 2)
            result.append(peso10)

            lote10 = read_lote(client, 28608, 2)
            result.append(lote10)

            produto11 = read_string(client, 8794, 9)
            result.append(produto11)

            peso11 = read_decimal(client, 8864, 2)
            result.append(peso11)

            lote11 = read_lote(client, 28610, 2)
            result.append(lote11)

            produto12 = read_string(client, 8804, 9)
            result.append(produto12)

            peso12 = read_decimal(client, 8866, 2)
            result.append(peso12)

            lote12 = read_lote(client, 28612, 2)
            result.append(lote12)

            produto13 = read_string(client, 8814, 9)
            result.append(produto13)

            peso13 = read_decimal(client, 8868, 2)
            result.append(peso13)

            lote13 = read_lote(client, 28614, 2)
            result.append(lote13)

            produto14 = read_string(client, 8824, 9)
            result.append(produto14)

            peso14 = read_decimal(client, 8870, 2)
            result.append(peso14)

            lote14 = read_lote(client, 28616, 2)
            result.append(lote14)

            produto15 = read_string(client, 8834, 9)
            result.append(produto15)

            peso15 = read_decimal(client, 8872, 2)
            result.append(peso15)

            lote15 = read_lote(client, 28618, 2)
            result.append(lote15)

            sequencia = read_word(client, 8874)
            result.append(sequencia)

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
                allotment1  = x[3],
                product2    = x[4],
                weight2     = x[5],
                allotment2  = x[6],
                product3    = x[7],
                weight3     = x[8],
                allotment3  = x[9],
                product4    = x[10],
                weight4     = x[11],
                allotment4  = x[12],
                product5    = x[13],
                weight5     = x[14],
                allotment5  = x[15],
                product6    = x[16],
                weight6     = x[17],
                allotment6  = x[18],
                product7    = x[19],
                weight7     = x[20],
                allotment7  = x[21],
                product8    = x[22],
                weight8     = x[23],
                allotment8  = x[24],
                product9    = x[25],
                weight9     = x[26],
                allotment9  = x[27],
                product10   = x[28],
                weight10    = x[29],
                allotment10 = x[30],
                product11   = x[31],
                weight11    = x[32],
                allotment11 = x[33],
                product12   = x[34],
                weight12    = x[35],
                allotment12 = x[36],
                product13   = x[37],
                weight13    = x[38],
                allotment13 = x[39],
                product14   = x[40],
                weight14    = x[41],
                allotment14 = x[42],
                product15   = x[43],
                weight15    = x[44],
                allotment15 = x[45],
                sequencia   = x[46],
                sum1        = x[2] + x[5] + x[8] + x[11] + x[14] + x[17] + x[20] + x[23] + x[26] + x[29] + x[32],
                sum2        = x[35] + x[38] + x[41] + x[44]
            )   
            data = datetime.now()
            
        except Exception as er: 
            print(er)
