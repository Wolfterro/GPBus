#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
The MIT License (MIT)

Copyright (c) 2016 Wolfgang Almeida <wolfgang.almeida@yahoo.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#========================================
# Criado por: Wolfterro
# Versão: 1.0.0 - Python 2.x
# Data: 19/09/2016
#========================================

from __future__ import print_function

import os
import sys
import json
import urllib2

# Chave API do Google Maps
# Necessária caso queira um controle maior de verificações de endereços ou um
# limite maior caso possua um plano pago, mas não é obrigatória.
#
# Deixe em branco caso não tenha, mas lembre-se que o limite de verificação
# é de 2.500 vezes por dia (1 ônibus = 1 verificação)!
#
# Para obter uma chave, utilize o endereço abaixo (requer conta do Google):
# https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=pt-br
# ===============================================================================
GOOGLEAPI_KEY = ""

# API do sistema de transporte da Prefeitura do Rio de Janeiro
# ============================================================
BUS_API = "http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes.json"

# Versão
# ======
VERSION = "1.0.0"

# COLUNAS:
# ========
DATAHORA = 0
ORDEM = 1
LINHA = 2
LATITUDE = 3
LONGITUDE = 4
VELOCIDADE = 5

# Alterando codificação padrão
# ============================
reload(sys)
sys.setdefaultencoding('utf-8')

# Resgatando informações
# ======================
def getJSONData(jsonFile):
	informsList = []
	for infos in jsonFile['DATA']:
		informsList.append(infos)
	return informsList

# Resgatando o arquivo JSON
# =========================
def getJSONFile(BUS_API):
	response = urllib2.urlopen(BUS_API)
	jsonFile = json.loads(response.read())
	return jsonFile

# Resgatando localização do ônibus
# ================================
def getBusLocation(latit, longit):
	urlApiGoogleMaps = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s" % (latit, longit, GOOGLEAPI_KEY)
	
	try:
		responseMaps = urllib2.urlopen(urlApiGoogleMaps)
		jsonFileMaps = json.loads(responseMaps.read())
	except Exception:
		return "Endereço não disponível!"

	if jsonFileMaps['status'] == "OVER_QUERY_LIMIT":
		return "Limite de verificação excedido!"
	
	elif jsonFileMaps['status'] == "OK":
		for elements in jsonFileMaps['results']:
			if 'formatted_address' in elements:
				return str(elements['formatted_address'])
			else:
				return "Endereço não disponível!"

# Iniciando processo de busca por número de ordem do ônibus
# =========================================================
def beginSearchProcessByOrder(userOrdem):
	try:
		jsonFile = getJSONFile(BUS_API)
		informsList = getJSONData(jsonFile)
	except Exception:
		print("[GPBus] Erro! Não foi possível acessar informações da API! Saindo ...")
		sys.exit(1)

	print("[GPBus] Imprimindo informações de ônibus da ordem '%s' ...\n" % (userOrdem))

	for infs in informsList:
		if userOrdem == "":
			break
		elif infs[ORDEM] == userOrdem:
			pprintInfo = "Data/Hora: %s\nOrdem: %s\nLinha: %s\nLocalização: %s\nLatitude: %s\nLongitude: %s\nVelocidade: %s km/h" % (infs[DATAHORA], 
			infs[ORDEM], str(infs[LINHA]).replace(".0", ""), getBusLocation(infs[LATITUDE], infs[LONGITUDE]), 
			infs[LATITUDE], infs[LONGITUDE], infs[VELOCIDADE])
			
			print("======================================")
			print(pprintInfo)
			print("======================================\n")

# Iniciando processo de busca por linha de ônibus
# ===============================================
def beginSearchProcessByLine(userLinha):
	try:
		jsonFile = getJSONFile(BUS_API)
		informsList = getJSONData(jsonFile)
	except Exception:
		print("[GPBus] Erro! Não foi possível acessar informações da API! Saindo ...")
		sys.exit(1)

	print("[GPBus] Imprimindo informações de ônibus da linha '%s' ...\n" % (str(userLinha).replace(".0", "")))

	for infs in informsList:
		if userLinha == "":
			break
		elif infs[LINHA] == userLinha:
			pprintInfo = "Data/Hora: %s\nOrdem: %s\nLinha: %s\nLocalização: %s\nLatitude: %s\nLongitude: %s\nVelocidade: %s km/h" % (infs[DATAHORA], 
			infs[ORDEM], str(infs[LINHA]).replace(".0", ""), getBusLocation(infs[LATITUDE], infs[LONGITUDE]), 
			infs[LATITUDE], infs[LONGITUDE], infs[VELOCIDADE])
			
			print("======================================")
			print(pprintInfo)
			print("======================================\n")

# Resgatando número de ordem do ônibus desejado pelo 
# usuário, caso não tenha inserido pela linha de comando
# ======================================================
def getBusOrder():
	userOrdem = raw_input("[GPBus] Insira o número de ordem do ônibus desejado: ")
	return userOrdem.upper()

# Resgatando linha de ônibus desejada pelo usuário,
# caso não tenha inserido pela linha de comando
#
# Por algum motivo, linhas com números simples são
# retornados pela API como números fracionários, portanto
# é necessário convertê-los para fazer a comparação logo adiante
# ==============================================================
def getBusLine(userLinha):
	if userLinha == None:
		userLinha = raw_input("[GPBus] Insira a linha do ônibus desejada: ")
		try:
			userLinha = float(userLinha)
		except Exception:
			userLinha = userLinha.upper()		# Caso seja uma linha com letras (exemplo: SV917)
		
		return userLinha
	
	else:
		try:
			userLinha = float(userLinha)
		except Exception:
			userLinha = userLinha.upper()		# Caso seja uma linha com letras (exemplo: SV917)
		
		return userLinha

# Escolhendo o modo de busca, caso o usuário não
# tenha utilizado as opções da linha de comando
# ==============================================
def chooseSearchMode():
	print("[GPBus] Escolha o modo de busca: ")
	print("--------------------------------\n")

	print("(1) Por linha de ônibus (exemplo: 363)")
	print("(2) Por número de ordem do ônibus (exemplo: D13128)\n")

	chooseMode = raw_input("[GPBus] Escolha o modo desejado (qualquer outra tecla para sair): ")

	if chooseMode == "1":
		userLinha = getBusLine(None)
		beginSearchProcessByLine(userLinha)
	elif chooseMode == "2":
		userOrdem = getBusOrder()
		beginSearchProcessByOrder(userOrdem)
	else:
		print("[GPBus] Saindo ...")
		sys.exit(0)

# Menu de Ajuda
# =============
def helpMenu():
	print("Uso: ./GPBus.py [OPÇÕES] [LINHA / ORDEM]")
	print("----------------------------------------\n")

	print("[Opções]")
	print("--------")
	print(" -a || --ajuda\t\t\tMostra este menu de ajuda.")
	print(" -h || --help\t\t\tMostra este menu de ajuda.")
	print(" -l || --linha\t\t\tFaz a busca pelos ônibus da linha desejada.")
	print(" -o || --ordem\t\t\tFaz a busca pelo ônibus com o número de ordem desejado.\n")

	print("Nota:")
	print("-----\n")
	print("Este programa faz uso da API do Google Maps para decodificar a localização exata dos ônibus.\n")
	
	print("Porém, há um limite diário de 2.500 verificações (1 ônibus = 1 verificação), caso exceda")
	print("este limite, você poderá ficar sem a localização exata dos ônibus, mas poderá ainda possuir a") 
	print("latitude e longitude dos mesmos, podendo então verificar manualmente suas localizações.\n")

	print("----------------------------------------------------------------------------------------------\n")

	print(" *** Este programa é licenciado sob a licença MIT ***\n")
	print("Copyright (c) 2016 Wolfgang Almeida <wolfgang.almeida@yahoo.com>")
	print("Repositório no GitHub: https://github.com/Wolfterro/GPBus\n")

# Método principal
# ================
def main():
	argc = len(sys.argv)

	print("========================")
	print("GPBus: RJ - Versão %s" % (VERSION))
	print("========================\n")

	if argc > 2:
		if str(sys.argv[1]) == "-l" or str(sys.argv[1]) == "--linha":
			userLinha = getBusLine(str(sys.argv[2]))
			beginSearchProcessByLine(userLinha)

		elif str(sys.argv[1]) == "-o" or str(sys.argv[1]) == "--ordem":
			userOrdem = str(sys.argv[2]).upper()
			beginSearchProcessByOrder(userOrdem)

		elif str(sys.argv[1]) == "-a" or str(sys.argv[1]) == "--ajuda":
			helpMenu()

		elif str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help":
			helpMenu()

		else:
			print("[GPBus] Erro! Argumento desconhecido! Use -a ou --ajuda para uma lista de opções!\n")
			sys.exit(1)
	
	elif argc == 2:
		if str(sys.argv[1]) == "-l" or str(sys.argv[1]) == "--linha":
			print("[GPBus] Erro! Falta o número da linha! Saindo ...\n")
			sys.exit(1)

		elif str(sys.argv[1]) == "-o" or str(sys.argv[1]) == "--ordem":
			print("[GPBus] Erro! Falta o número de ordem! Saindo ...\n")
			sys.exit(1)

		elif str(sys.argv[1]) == "-a" or str(sys.argv[1]) == "--ajuda":
			helpMenu()

		elif str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help":
			helpMenu()

		else:
			print("[GPBus] Erro! Argumento desconhecido! Use -a ou --ajuda para uma lista de opções!\n")
			sys.exit(1)
	
	else:
		chooseSearchMode()

# Inicializando programa
# ======================
if __name__ == "__main__":
	main()