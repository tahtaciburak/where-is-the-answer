import fasttext
import ft
import numpy as np
import re
import utils
import os
import cli_helper


os.system("clear")
model = utils.load_model()
while True:
	os.system("clear")
	print("Cevap Nerede - Turkish Question Answering System")
	print(" 1.Rastgele Bir Metni Analiz Et")
	print(" 2.Test Kumesindeki Tum Metinleri Analiz Et")
	#print(" 3.Manuel Olarak Soru Gir")
	print(" 3.Dokumantasyon")
	print("===============================================")
	secim = input("Isleminizi Seciniz > ")

	if secim == "1":
		cli_helper.one(model)
	elif secim == "2":
		cli_helper.two(model)
	elif secim == "3":
		print("3 Secildi")
	elif secim == "4":
		print("4 Secildi")