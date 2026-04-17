import time
import struct
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import sqlite3

def decimalDecoder(instance):
	if not instance.isError():
		regs = instance.registers
		raw = struct.pack('>HH', regs[1], regs[0])
		value = struct.unpack('>f', raw)[0]
		return float('{0:.2f}'.format(value))
	else:
		print("Erro: registradores não disponíveis.")
		return None

def read_decimal(client, address, qtd):
	if client.connect():
		request = client.read_holding_registers(address, count=qtd, device_id=UNIT_ID)
		value = decimalDecoder(request)
		time.sleep(1)
		return value
	else:
		return read_decimal(client, address, qtd)

def read_dword(client, address):
	if client.connect():
		request = client.read_holding_registers(address, count=2, device_id=UNIT_ID)
		if not request.isError():
			return (request.registers[1] << 16) | request.registers[0]  # DWORD = inteiro 32 bits sem sinal (low word first)
		else:
			print("Erro: registrador DWORD não disponível.")
			return None
	else:
		return read_dword(client, address)

def read_word(client, address):
	if client.connect():
		request = client.read_holding_registers(address, count=1, device_id=UNIT_ID)
		if not request.isError():
			return request.registers[0]  # Word = inteiro 16 bits sem sinal (0-65535)
		else:
			print("Erro: registrador não disponível.")
			return None
	else:
		return read_word(client, address)

def read_string(client, address, num_words):
	if client.connect():
		# Try a few attempts before giving up
		attempts = 3
		for attempt in range(attempts):
			request = client.read_holding_registers(address, count=num_words, device_id=UNIT_ID)
			if not request.isError():
				# Build two variants: low-high (existing) and high-low (alternative)
				chars_lh = []
				chars_hl = []
				for reg in request.registers:
					high_byte = (reg >> 8) & 0xFF
					low_byte = reg & 0xFF
					chars_lh.append(chr(low_byte) if low_byte != 0 else '')
					chars_lh.append(chr(high_byte) if high_byte != 0 else '')
					chars_hl.append(chr(high_byte) if high_byte != 0 else '')
					chars_hl.append(chr(low_byte) if low_byte != 0 else '')

				str_lh = ''.join(chars_lh).strip()
				str_hl = ''.join(chars_hl).strip()

				# Heuristics: prefer variant that matches common patterns (digits and optional space)
				import re
				# If either variant contains a 10-digit substring, return it (handles continuous or spaced forms)
				for s in (str_lh, str_hl):
					m = re.search(r"(\d{10})", s)
					if m:
						return m.group(1)
				# If there are at least 10 digits after removing non-digits, return the last 10 (likely significant)
				for s in (str_lh, str_hl):
					digits = re.sub(r'\D', '', s)
					if len(digits) >= 10:
						return digits[-10:]

				pattern = re.compile(r'^[0-9]{5}\s?[0-9]{5}$')
				if pattern.match(str_lh):
					return str_lh.replace(' ', '') if ' ' in str_lh else str_lh
				if pattern.match(str_hl):
					return str_hl.replace(' ', '') if ' ' in str_hl else str_hl

				# Otherwise prefer the one with more printable characters
				def printable_ratio(s):
					if not s:
						return 0
					printable = sum(1 for ch in s if 32 <= ord(ch) <= 126)
					return printable / len(s)

				if printable_ratio(str_hl) > printable_ratio(str_lh):
					return str_hl
				return str_lh
			else:
				print(f"Tentativa {attempt+1}/{attempts}: erro lendo string no endereço {address} (count={num_words}).")
				time.sleep(0.25)

		# Se tudo falhar, log e retorne string vazia para não quebrar fluxo
		print(f"Erro: registrador string não disponível. Endereço: {address}, count: {num_words}")
		return ''
	else:
		return read_string(client, address, num_words)

def read_bit(client, address, bit_position):
	if client.connect():
		request = client.read_holding_registers(address, count=1, device_id=UNIT_ID)
		if not request.isError():
			return (request.registers[0] >> bit_position) & 1
		else:
			print(f"Erro: registrador do bit não disponível. Endereço: {address}, Resposta: {request}")
			return None
	else:
		return read_bit(client, address, bit_position)

def clear_bit(client, address, bit_position):
	if client.connect():
		request = client.read_holding_registers(address, count=1, device_id=UNIT_ID)
		if not request.isError():
			new_value = request.registers[0] & ~(1 << bit_position)
			client.write_register(address, new_value, device_id=UNIT_ID)
			print(f"Bit {bit_position} do registrador {address} zerado.")
		else:
			print("Erro ao ler registrador para zerar bit.")
	else:
		clear_bit(client, address, bit_position)

try:
	# pymodbus 2.x
	from pymodbus.client.sync import ModbusTcpClient
except Exception:
	try:
		# fallback for other versions
		from pymodbus.client import ModbusTcpClient
	except Exception:
		ModbusTcpClient = None

IP = "192.168.2.90"
PORT = 502
UNIT_ID = 1
RECEITA_REGISTRADOR = 9113
SEQUENCIA_REGISTRADOR = 9123
CODIGO_REGISTRADOR = 9124
PRODUTO_REGISTRADOR = 9128
LOTE_REGISTRADOR = 9145
UNIDADE_REGISTRADOR = 9151
PESO_REGISTRADOR = 9154

BIT_TRIGGER_REGISTRADOR = 9071
BIT_TRIGGER_POSICAO = 1

API_URL = ""
POLL_INTERVAL = 1  # segundos entre cada verificação do bit
DB_FILE = "dosagem.db"


def init_db(db_path=DB_FILE):
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	cur.execute('''
		CREATE TABLE IF NOT EXISTS dosagens (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			receita TEXT,
			sequencia INTEGER,
			codigo TEXT,
			produto TEXT,
			lote TEXT,
			unidade TEXT,
			peso REAL,
			timestamp TEXT
		)
	''')
	conn.commit()
	conn.close()


def ler_e_gravar(client):
	print("Bit de disparo ativo. Lendo registradores...")

	MAX_TENTATIVAS = 5
	for tentativa in range(1, MAX_TENTATIVAS + 1):
		receita   = read_string(client, RECEITA_REGISTRADOR, 10)
		sequencia = read_word(client, SEQUENCIA_REGISTRADOR)
		codigo    = read_string(client, CODIGO_REGISTRADOR, 3)
		produto   = read_string(client, PRODUTO_REGISTRADOR, 16)
		lote      = read_string(client, LOTE_REGISTRADOR, 6)
		unidade   = read_string(client, UNIDADE_REGISTRADOR, 2)
		peso      = read_decimal(client, PESO_REGISTRADOR, 2)

		if None not in (receita, sequencia, codigo, produto, lote, unidade, peso):
			break

		print(f"Leitura incompleta (tentativa {tentativa}/{MAX_TENTATIVAS}), aguardando e repetindo...")
		time.sleep(1)
	else:
		print("Erro: não foi possível ler todos os registradores após várias tentativas. Abortando gravação.")
		return

	clear_bit(client, BIT_TRIGGER_REGISTRADOR, BIT_TRIGGER_POSICAO)

	payload = {
		"receita": receita,
		"sequencia": sequencia,
		"codigo": codigo,
		"produto": produto,
		"lote": lote,
		"unidade": unidade,
		"peso": peso,
		"timestamp": datetime.now(ZoneInfo("America/Cuiaba")).isoformat(),
	}
	print(payload)

	# Gravar no banco SQLite
	try:
		conn = sqlite3.connect(DB_FILE)
		cur = conn.cursor()
		cur.execute(
			"""
			INSERT INTO dosagens (receita, sequencia, codigo, produto, lote, unidade, peso, timestamp)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?)
			""",
			(
				receita,
				sequencia,
				codigo,
				produto,
				lote,
				unidade,
				peso,
				payload["timestamp"],
			),
		)
		conn.commit()
		conn.close()
		print("Dados gravados localmente no SQLite.")
	except Exception as e:
		print(f"Erro ao gravar no SQLite: {e}")


def main():
	print(f"Conectando ao CLP em {IP}:{PORT} (ID {UNIT_ID})...")
	# Garantir que o banco e a tabela existem
	init_db()
	if ModbusTcpClient is None:
		print("Erro: `ModbusTcpClient` não disponível. Instale uma versão compatível do `pymodbus` (ex: `pip install pymodbus==2.5.3`).")
		return

	client = ModbusTcpClient(IP, port=PORT)
	if not client.connect():
		print("Falha ao conectar ao CLP.")
		return
	print(f"Conectado. Monitorando bit {BIT_TRIGGER_POSICAO} do registrador {BIT_TRIGGER_REGISTRADOR}...")

	try:
		while True:
			bit = read_bit(client, BIT_TRIGGER_REGISTRADOR, BIT_TRIGGER_POSICAO)
			if bit == 1:
				print("Bit de disparo detectado!")
				ler_e_gravar(client)
			time.sleep(POLL_INTERVAL)
	except KeyboardInterrupt:
		print("\nEncerrando monitoramento.")
	finally:
		client.close()


if __name__ == "__main__":
	main()