import fasttext
import ft
import numpy as np
import re
import utils
import os
from random import randint

NUM_OF_TESTS = 20

def one(model):
	os.system("clear")
	rand = randint(1,NUM_OF_TESTS)
	text = []
	questions = []
	real_answers = []
	method0 = []
	method1 = []
	method2 = []
	method3 = []
	method4 = []
	text_arr = []

	print("Metin "+str(rand)+"\n================================================")
	text_file_name = "./test_new/"+str(rand)+"/"+"EachRowOneSentence.txt"
	text_file = open(text_file_name, "r")
	for line in text_file:
		if len(line)>1:
			text.append(line)
			line = line.replace("\n","")
			#text_arr.append(line)

	for cumle in text:
		cumle = cumle.replace("\n","")
		print(cumle)
	print("================================================\nSorular:\n")
	sayac = 1
	questions_file_name = "./test_new/"+str(rand)+"/"+"Questions.txt"
	questions_file = open(questions_file_name,"r")
	for line in questions_file:
		if len(line)>1:
			line = line.replace("\n","")
			print(str(sayac)+". "+line)
			questions.append(line)
			sayac = sayac + 1

	rq_file_name = "./test_new/"+str(rand)+"/"+"AnswersNumbered.txt"
	rq_file = open(rq_file_name,"r")
	for line in rq_file:
		line = line.replace("\n","")
		real_answers.append(int(line))
	
	print("================================================\nGercek Cevaplar:\n")
	sayac = 1
	ans_sents_file_name = "./test_new/"+str(rand)+"/"+"AnswersSentences.txt"
	ans_sents_file = open(ans_sents_file_name,"r")
	for line in ans_sents_file:
		line = line.replace("\n","")
		print(str(sayac)+". "+line)
		sayac = sayac + 1

	for question in questions:
		
		m1=utils.calculate_sentence_vector_similarity(text,question,model)
		method1.append(m1+1)		

		m2=utils.where_is_the_answer(text,question,model)
		method2.append(m2+1)
		
		m3=utils.calculate_sentence_vector_similarity_euclidean(text,question,model)
		method3.append(m3+1)

		m4_set = utils.csvs_mrr(text,question,model)
		method4.append(m4_set)

	#metot1
	
	print("================================================")
	print("Metot 1: Cumle vektorlerinin karsilastirilmasi")
	#print("Metot 1'e dair bir aciklama ne olduguna nasil calistigina vs. Bulunan cevaplar asagida verilmistir")
	m1_dogruluk = 0.0
	print(len(text))
	print(method1)
	print(real_answers)
	for i in range(0,len(method1)):
		if method1[i] <= len(text):
			if method1[i] == real_answers[i]:
				print(str(i)+". "+text[method1[i]-1]+"[DOGRU]")
				m1_dogruluk = m1_dogruluk + 1
			else:
				print(str(i)+". "+text[method1[i]-1]+"[YANLIS]")
		else:
			print(str(i)+". "+"Uygun Cevap Yok"+"[YALNIS]")
	print("\n1. Metodun Dogruluk Orani> "+str(m1_dogruluk/len(method1)))
	#metot2
	print("================================================")
	print("Metot 2: Kelime vektorlerinin karsilastirilmasi")
	#print("Metot 2'e dair bir aciklama ne olduguna nasil calistigina vs. Bulunan cevaplar asagida verilmistir")
	m2_dogruluk = 0.0
	for i in range(0,len(method2)):
		if method2[i] <= len(text):
			if method2[i] == real_answers[i]:
				print(str(i)+". "+text[method2[i]-1]+"[DOGRU]")
				m2_dogruluk = m2_dogruluk + 1
			else:
				print(str(i)+". "+text[method2[i]-1]+"[YANLIS]")
		else:
			print(str(i)+". "+"Uygun Cevap Yok"+"[YANLIS]")
	print("\n2. Metodun Dogruluk Orani> "+str(m2_dogruluk/len(method2)))
	#metot3

	print("================================================")
	print("Metot 3: Cumle vektorlerinin oklid uzakligiyla karsilastirilmasi")
	#print("Metot 2'e dair bir aciklama ne olduguna nasil calistigina vs. Bulunan cevaplar asagida verilmistir")
	m3_dogruluk = 0.0
	for i in range(0,len(method3)):
		if method3[i] <= len(text):
			if method3[i] == real_answers[i]:
				print(str(i)+". "+text[method3[i]-1]+"[DOGRU]")
				m3_dogruluk = m3_dogruluk + 1
			else:
				print(str(i)+". "+text[method3[i]-1]+"[YANLIS]")
		else:
			print(str(i)+". "+"Uygun Cevap Yok"+"[YANLIS]")
	print("\n3. Metodun Dogruluk Orani> "+str(m3_dogruluk/len(method3)))
	#metot3
	
	print("================================================")
	print("Metot 4: Cumle vektorlerinin MRR kullanilarak karsilastirilmasi")
	#print("Metot 3'e dair bir aciklama ne olduguna nasil calistigina vs. Bulunan cevaplar asagida verilmistir")
	for i in range(0,len(method4)):
		for j in range(0,len(method4[i])):
			if len(text)>method4[i][j]:
				text[method4[i][j]] = text[method4[i][j]].replace("\n","")
				print(str(i)+". "+text[method4[i][j]])
		print("------")

	#print("4. Metodun Dogruluk Orani > ",utils.handle_mrr(real_answers,method3))
	devam = input("DEVAM ETMEK ICIN ENTER TUSUNA BASIN")
	return
	
def two(model):
	#utils.test_for_all_texts(model)
	utils.test_for_all_texts_question_based(model)
	devam = input("DEVAM ETMEK ICIN ENTER TUSUNA BASIN")
def three():
	
	return

def four():
	print("Dokumantasyon ile ilgili temel seyler buraya gelecek. Burasi en son is.")
	return