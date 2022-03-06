from pymodbus.constants import Endian
from pymodbus.payload import *
import time

def decimalDecoder(instance):
    if not instance.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            instance.registers,
            byteorder=Endian.Big, wordorder=Endian.Little
        )   
        return float('{0:.2f}'.format(decoder.decode_32bit_float()))

    else:
        # Error handling.
        print("There isn't the registers, Try again.")
        return None

def stringDecoder(instance, length):
    if not instance.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            instance.registers,
            byteorder=Endian.Big, wordorder=Endian.Little
        )   
        return decoder.decode_string(length)

    else:
        # Error handling.
        print("There isn't the registers, Try again.")
        return None
    
def stringSort(string):
    l = [x for x in string]
    it = iter(l)
    result = ''
    for x in it:
        try:
            aux = next(it)
            result += aux + x
        except StopIteration as e:
            break
    return result
    
def writeInt(value, address, client):
    if(client.connect()):
        client.write_registers(address, value)
        time.sleep(0.5)
        request = client.read_holding_registers(address, 1)  # Specify the unit.
        valor = request.registers
        time.sleep(0.5)
        if(valor[0] == value):
            return
        else:
            writeInt(value, address, client)
    else:
        writeInt(value, address, client)

def read_decimal(client, address, qtd):
    if(client.connect()):
        request = client.read_holding_registers(address, qtd)  # Specify the unit.
        value = decimalDecoder(request)        
        time.sleep(1)
        return value
    else:
        read_decimal(client, address, qtd)
    
def read_integer(client, address, qtd):
    if(client.connect()):
        request = client.read_holding_registers(address, qtd)  # Specify the unit.
        value = request.registers
        if(len(value) > 0):
            time.sleep(1)
            return value[0]
        else:
            read_integer(client, address, qtd)
    else:
        read_integer(client, address, qtd)
    
def read_string(client, address, qtd):
    if(client.connect()):
        request = client.read_holding_registers(address, qtd)  # Specify the unit.
        value = stringDecoder(request, 18)
        value = value.decode("utf-8")
        value = stringSort(value)
        value = value.replace("\x00", "")
        value = value.strip()
        time.sleep(1)
        return value
    else:
        read_string(client, address, qtd)     

def stringSort(string):
    l = [x for x in string]
    it = iter(l)
    result = ''
    for x in it:
        try:
            aux = next(it)
            result += aux + x
        except StopIteration as e:
            break
    return result

def writeString(value, address, client):
    builder = BinaryPayloadBuilder(byteorder=Endian.Little)
    aux = stringSort(value)
    builder.add_string(aux)
    payload = builder.build()
    client.write_registers(address, payload, skip_encode=True)
    time.sleep(0.5)
    request = client.read_holding_registers(address, 10)  # Specify the unit.
    valor = stringDecoder(request, 18)
    valor = valor.decode("utf-8")
    valor = stringSort(valor.strip(" "))
    time.sleep(0.5)
    if(valor == value):
        return
    else:
        writeString(value.strip(" "), address, client)

def writeInt(value, address, client):
    client.write_registers(address, value)
    time.sleep(0.5)
    request = client.read_holding_registers(address, 1)  # Specify the unit.
    valor = request.registers
    time.sleep(0.5)
    if(valor[0] == value):
        return
    else:
        writeInt(value, address, client)

def writeDecimal(value, address, client):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    builder.add_32bit_float(value)
    payload = builder.build()
    client.write_registers(address, payload, skip_encode=True)
    time.sleep(0.5)
    request = client.read_holding_registers(address, 2)  # Specify the unit.
    valor = decimalDecoder(request)
    time.sleep(0.5)
    if(valor == value):
        return
    else:
        writeDecimal(value, address, client)   