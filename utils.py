import fasttext
import ft
import numpy as np
import re
from random import randint
from math import*

def load_model():
    return ft.FastVector(vector_file="wiki.tr.vec")

def test_for_all_texts(model):
    num_of_tests = 52 # Change it when nessecery
    total_performance0 = 0.0
    total_performance1 = 0.0
    total_performance2 = 0.0
    total_performance3 = 0.0
    total_performance4 = 0.0
    total_performance5 = 0.0
    total_performance6 = 0.0

    total_performance1_mrr = 0.0
    total_performance2_mrr = 0.0
    total_performance3_mrr = 0.0
    total_performance4_mrr = 0.0
    total_performance5_mrr = 0.0
    total_performance6_mrr = 0.0


    for i in range(1,num_of_tests):
        text = []
        questions = []
        real_answers = []
        answers0 = []
        answers1 = []
        answers2 = []
        answers3 = []
        answers4 = []
        answers5 = []
        answers6 = []
       
        answers1_mrr = []
        answers2_mrr = []
        answers3_mrr = []
        answers4_mrr = []
        answers5_mrr = []
        answers6_mrr = []

        num_of_lines = 0
        
        text_file_name = "./test_outsourced/"+str(i)+"/"+"EachRowOneSentence.txt"
        text_file = open(text_file_name, "r")
        for line in text_file:
            if len(line)>1:
                text.append(line)
                num_of_lines = num_of_lines + 1

        questions_file_name = "./test_outsourced/"+str(i)+"/"+"Questions.txt"
        questions_file = open(questions_file_name,"r")
        for line in questions_file:
            if len(line)>1:
                line = line.replace("\n","")
                questions.append(line)
                
        rq_file_name = "./test_outsourced/"+str(i)+"/"+"AnswersNumbered.txt"
        rq_file = open(rq_file_name,"r")
        for line in rq_file:
            line = line.replace("\n","")
            real_answers.append(int(line))
                
        for question in questions:
            answers0.append(randint(1,num_of_lines)) # 0 RASTGELE

            #--------
            answer1 = word_similarity(text,question) # 1 KELIME BENZERLIGI
            answers1.append(answer1+1)
            
            answer_set1 = ws_mrr(text,question) # KELIME BENZERLIGI MRR
            answers1_mrr.append(answer_set1)

            #-------------
            answer2 = six_letter_similarity(text,question) # 2 ALTI HARF BENZERLIGI
            answers2.append(answer2+1)

            answer_set2 = sls_mrr(text,question) # ALTI HARF BENZERLIGI MRR
            answers2_mrr.append(answer_set2)
           
            #----------------
            answer3 = jaccard_similarity(text,question) # 3 KELIME SHINGLE JACCARD
            answers3.append(answer3+1)

            answer_set3 = js_mrr(text,question)
            answers3_mrr.append(answer_set3)
            
            #---------------
            answer4 = where_is_the_answer(text,question,model) # 4 MODELI KULLANAN BIZIM YONTEM
            answers4.append(answer4+1)

            answer_set4 = wita_mrr(text,question,model)
            answers4_mrr.append(answer_set4)

            #--------------
            answer5 = calculate_sentence_vector_similarity(text,question,model) # 5 MODELI KULLANAN HOCANIN ONERDIGI YONTEM
            answers5.append(answer5+1)
            
            answer_set = csvs_mrr(text,question,model) # 7 MODELI KULLANAN HOCANIN YONTEMI UC CEVAP ONERME
            answers5_mrr.append(answer_set)            
            
            #-------------
            answer6 = calculate_sentence_vector_similarity_euclidean(text,question,model) # 6 MODELI KULLANAN HOCANIN YONTEMINI OKLITLE DENEDIM
            answers6.append(answer6+1)



        print(i,". Metin Sonuclar")
        print("Gercek Cevaplar                   > ",real_answers)
        print("0. Yontem:[RASTGELE]              > ",answers0,"Dogruluk Orani > ",compare_arrays(real_answers,answers0))
        print("1. Yontem:[KELIME BENZERLIGI]     > ",answers1,"Dogruluk Orani > ",compare_arrays(real_answers,answers1))
        print("2. Yontem:[6 HARF BENZERLIGI]     > ",answers2,"Dogruluk Orani > ",compare_arrays(real_answers,answers2))
        print("3. Yontem:[JACCARD BENZERLIGI]    > ",answers3,"Dogruluk Orani > ",compare_arrays(real_answers,answers3))
        print("4. Yontem:[KELIME VEKTORU]        > ",answers4,"Dogruluk Orani > ",compare_arrays(real_answers,answers4))
        print("5. Yontem:[CUMLE VEKTORU COSINE]  > ",answers5,"Dogruluk Orani > ",compare_arrays(real_answers,answers5))
        print("6. Yontem:[CUMLE VEKTORU OKLIT]   > ",answers6,"Dogruluk Orani > ",compare_arrays(real_answers,answers6))
        #print("7. Yontem:[CUMLE VEKTOR VE MRR]   > ",answers7)

        print("-----------------------------------\n")
        
        total_performance0 = total_performance0 + compare_arrays(real_answers,answers0)
        total_performance1 = total_performance1 + compare_arrays(real_answers,answers1)
        total_performance2 = total_performance2 + compare_arrays(real_answers,answers2)
        total_performance3 = total_performance3 + compare_arrays(real_answers,answers3)
        total_performance4 = total_performance4 + compare_arrays(real_answers,answers4)
        total_performance5 = total_performance5 + compare_arrays(real_answers,answers5)
        total_performance6 = total_performance6 + compare_arrays(real_answers,answers6)
        total_performance1_mrr = total_performance1_mrr + handle_mrr(real_answers,answers1_mrr)
        total_performance2_mrr = total_performance5_mrr + handle_mrr(real_answers,answers2_mrr)
        total_performance3_mrr = total_performance5_mrr + handle_mrr(real_answers,answers3_mrr)
        total_performance4_mrr = total_performance5_mrr + handle_mrr(real_answers,answers4_mrr)
        total_performance5_mrr = total_performance5_mrr + handle_mrr(real_answers,answers5_mrr)

        text_file.close()
        questions_file.close()
        rq_file.close()

    print("0. Yontemin basarimi[RASTGELE]             > ","{:.4f}".format(total_performance0/num_of_tests)," > [MRR] > ")
    print("1. Yontemin basarimi[KELIME BENZERLIGI]    > ","{:.4f}".format(total_performance1/num_of_tests)," > [MRR] > ","{:.6f}".format(total_performance1_mrr/num_of_tests))
    print("2. Yontemin basarimi[6 HARF BENZERLIGI]]   > ","{:.4f}".format(total_performance2/num_of_tests)," > [MRR] > ","{:.6f}".format(total_performance2_mrr/num_of_tests))
    print("3. Yontemin basarimi[JACCARD BENZERLIGI]   > ","{:.4f}".format(total_performance3/num_of_tests)," > [MRR] > ","{:.6f}".format(total_performance3_mrr/num_of_tests))
    print("4. Yontemin basarimi[KELIME VEKTORU]       > ","{:.4f}".format(total_performance4/num_of_tests)," > [MRR] > ","{:.6f}".format(total_performance4_mrr/num_of_tests))
    print("5. Yontemin basarimi[CUMLE VEKTORU COSINE] > ","{:.4f}".format(total_performance5/num_of_tests)," > [MRR] > ","{:.6f}".format(total_performance5_mrr/num_of_tests))
    print("6. Yontemin basarimi[CUMLE VEKTORU OKLIT]  > ","{:.4f}".format(total_performance6/num_of_tests)," > [MRR] > ")
    #print("7. Yontemin basarimi[CUMLE VEKTORU VE MRR] > ","{:.4f}".format(total_performance5_mrr/num_of_tests)," > [MRR] > ")

def test_for_all_texts_question_based(model):
    num_of_tests = 52    # Change it when nessecery
    total_performance0 = 0.0
    total_performance1 = 0.0
    total_performance2 = 0.0
    total_performance3 = 0.0
    total_performance4 = 0.0
    total_performance5 = 0.0
    total_performance6 = 0.0

    total_performance1_mrr = 0.0
    total_performance2_mrr = 0.0
    total_performance3_mrr = 0.0
    total_performance4_mrr = 0.0
    total_performance5_mrr = 0.0
    total_performance6_mrr = 0.0


    for i in range(1,num_of_tests):
        text = []
        questions = []
        real_answers = []
        answers0 = []
        answers1 = []
        answers2 = []
        answers3 = []
        answers4 = []
        answers5 = []
        answers6 = []
       
        answers1_mrr = []
        answers2_mrr = []
        answers3_mrr = []
        answers4_mrr = []
        answers5_mrr = []
        answers6_mrr = []

        num_of_lines = 0
        
        text_file_name = "./test_outsourced/"+str(i)+"/"+"EachRowOneSentence.txt"
        text_file = open(text_file_name, "r")
        for line in text_file:
            if len(line)>1:
                text.append(line)
                num_of_lines = num_of_lines + 1

        questions_file_name = "./test_outsourced/"+str(i)+"/"+"Questions.txt"
        questions_file = open(questions_file_name,"r")
        for line in questions_file:
            if len(line)>1:
                line = line.replace("\n","")
                questions.append(line)
                
        rq_file_name = "./test_outsourced/"+str(i)+"/"+"AnswersNumbered.txt"
        rq_file = open(rq_file_name,"r")
        for line in rq_file:
            line = line.replace("\n","")
            real_answers.append(int(line))
                
        for question in questions:
            answers0.append(randint(1,num_of_lines)) # 0 RASTGELE

            #--------
            answer1 = word_similarity(text,question) # 1 KELIME BENZERLIGI
            answers1.append(answer1+1)
            
            answer_set1 = ws_mrr(text,question) # KELIME BENZERLIGI MRR
            answers1_mrr.append(answer_set1)

            #-------------
            answer2 = six_letter_similarity(text,question) # 2 ALTI HARF BENZERLIGI
            answers2.append(answer2+1)

            answer_set2 = sls_mrr(text,question) # ALTI HARF BENZERLIGI MRR
            answers2_mrr.append(answer_set2)
           
            #----------------
            #answer3 = jaccard_similarity(text,question) # 3 KELIME SHINGLE JACCARD
            #answers3.append(answer3+1)

            #answer_set3 = js_mrr(text,question)
            #answers3_mrr.append(answer_set3)
            
            #---------------
            answer4 = where_is_the_answer(text,question,model) # 4 MODELI KULLANAN BIZIM YONTEM
            answers4.append(answer4+1)

            answer_set4 = wita_mrr(text,question,model)
            answers4_mrr.append(answer_set4)

            #--------------
            answer5 = calculate_sentence_vector_similarity(text,question,model) # 5 MODELI KULLANAN HOCANIN ONERDIGI YONTEM
            answers5.append(answer5+1)
            
            answer_set = csvs_mrr(text,question,model) # 7 MODELI KULLANAN HOCANIN YONTEMI UC CEVAP ONERME
            answers5_mrr.append(answer_set)            
            
            #-------------
            answer6 = calculate_sentence_vector_similarity_euclidean(text,question,model) # 6 MODELI KULLANAN HOCANIN YONTEMINI OKLITLE DENEDIM
            answers6.append(answer6+1)
            
            answer_set6 = csvse_mrr(text,question,model)
            answers6_mrr.append(answer_set6)

        
        print(i,". Metin Sonuclar")
        print("Gercek Cevaplar                   > ",real_answers)
        print("0. Yontem:[RASTGELE]              > ",answers0,"Dogruluk Orani > ","{:.3f}".format(compare_arrays(real_answers,answers0)))
        print("1. Yontem:[KELIME BENZERLIGI]     > ",answers1,"Dogruluk Orani > ","{:.3f}".format(compare_arrays(real_answers,answers1)))
        print("2. Yontem:[6 HARF BENZERLIGI]     > ",answers2,"Dogruluk Orani > ","{:.3f}".format(compare_arrays(real_answers,answers2)))
        #print("3. Yontem:[JACCARD BENZERLIGI]    > ",answers3,"Dogruluk Orani > ",compare_arrays(real_answers,answers3))
        print("3. Yontem:[KELIME VEKTORU]        > ",answers4,"Dogruluk Orani > ","{:.3f}".format(compare_arrays(real_answers,answers4)))
        print("4. Yontem:[CUMLE VEKTORU COSINE]  > ",answers5,"Dogruluk Orani > ","{:.3f}".format(compare_arrays(real_answers,answers5)))
        print("5. Yontem:[CUMLE VEKTORU OKLIT]   > ",answers6,"Dogruluk Orani > ","{:.3f}".format(compare_arrays(real_answers,answers6)))
        #print("7. Yontem:[CUMLE VEKTOR VE MRR]   > ",answers7)

        print("-----------------------------------\n")
        
        total_performance0 = total_performance0 + compare_arrays_question_based(real_answers,answers0)
        total_performance1 = total_performance1 + compare_arrays_question_based(real_answers,answers1)
        total_performance2 = total_performance2 + compare_arrays_question_based(real_answers,answers2)
        #total_performance3 = total_performance3 + compare_arrays_question_based(real_answers,answers3)
        total_performance4 = total_performance4 + compare_arrays_question_based(real_answers,answers4)
        total_performance5 = total_performance5 + compare_arrays_question_based(real_answers,answers5)
        total_performance6 = total_performance6 + compare_arrays_question_based(real_answers,answers6)
        total_performance1_mrr = total_performance1_mrr + handle_mrr_question_based(real_answers,answers1_mrr)
        total_performance2_mrr = total_performance2_mrr + handle_mrr_question_based(real_answers,answers2_mrr)
        total_performance6_mrr = total_performance6_mrr + handle_mrr_question_based(real_answers,answers6_mrr)
        total_performance4_mrr = total_performance4_mrr + handle_mrr_question_based(real_answers,answers4_mrr)
        total_performance5_mrr = total_performance5_mrr + handle_mrr_question_based(real_answers,answers5_mrr)

        text_file.close()
        questions_file.close()
        rq_file.close()

    print("0. Yontemin basarimi[RASTGELE]             > ","{:.4f}".format(total_performance0/250)," > [MRR] > ")
    print("1. Yontemin basarimi[KELIME BENZERLIGI]    > ","{:.4f}".format(total_performance1/250)," > [MRR] > ","{:.8f}".format(total_performance1_mrr/250))
    print("2. Yontemin basarimi[6 HARF BENZERLIGI]]   > ","{:.4f}".format(total_performance2/250)," > [MRR] > ","{:.8f}".format(total_performance2_mrr/250))
    #print("3. Yontemin basarimi[JACCARD BENZERLIGI]   > ","{:.4f}".format(total_performance3/500)," > [MRR] > ","{:.8f}".format(total_performance3_mrr/500))
    print("3. Yontemin basarimi[KELIME VEKTORU]       > ","{:.4f}".format(total_performance4/250)," > [MRR] > ","{:.8f}".format(total_performance4_mrr/250))
    print("4. Yontemin basarimi[CUMLE VEKTORU COSINE] > ","{:.4f}".format(total_performance5/250)," > [MRR] > ","{:.8f}".format(total_performance5_mrr/250))
    print("5. Yontemin basarimi[CUMLE VEKTORU OKLIT]  > ","{:.4f}".format(total_performance6/250)," > [MRR] > ","{:.8f}".format(total_performance6_mrr/250))
    #print("7. Yontemin basarimi[CUMLE VEKTORU VE MRR] > ","{:.4f}".format(total_performance5_mrr/num_of_tests)," > [MRR] > ")

def where_is_the_answer(text,question,model):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        max_similarity = 0.0
        temp_summary = 0.0
        average_similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                if t_word in model and q_word in model:
                    similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                else:
                    if t_word == q_word:
                        similarity = 1.0
                    else:
                        union = list(set(t_word+q_word))
                        intersection = list(set(t_word) - (set(t_word)-set(q_word)))
                        jaccard_coeff = float(len(intersection))/len(union)
                        similarity = jaccard_coeff
                        #similarity = 0.0
                if similarity>max_similarity:
                    max_similarity = similarity
            temp_summary += max_similarity
        
        average_similarity = temp_summary/len(tokenized_question)
        similarities.append(average_similarity)

    return similarities.index(max(similarities))

def wita_mrr(text,question,model):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        max_similarity = 0.0
        temp_summary = 0.0
        average_similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                if t_word in model and q_word in model:
                    similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                else:
                    if t_word == q_word:
                        similarity = 1.0
                    else:
                        union = list(set(t_word+q_word))
                        intersection = list(set(t_word) - (set(t_word)-set(q_word)))
                        jaccard_coeff = float(len(intersection))/len(union)
                        similarity = jaccard_coeff
                        #similarity = 0.0
                if similarity>max_similarity:
                    max_similarity = similarity
            temp_summary += max_similarity
        
        average_similarity = temp_summary/len(tokenized_question)
        similarities.append(average_similarity)
    answers =[]
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers 

def word_similarity(text,question):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                if t_word == q_word:
                    similarity = similarity + 1

        average_similarity = similarity / len(t_sent)
        similarities.append(average_similarity)
    return similarities.index(max(similarities))

def ws_mrr(text,question):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                if t_word == q_word:
                    similarity = similarity + 0.7

        average_similarity = similarity / len(t_sent)
        similarities.append(average_similarity)
    answers =[]
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers 

def six_letter_similarity(text,question):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                w1 = t_word[0:6]
                w2 = q_word[0:6]
                if w1 == w2:
                    similarity = similarity + 1

        average_similarity = similarity / len(tokenized_question)
        similarities.append(average_similarity)
    return similarities.index(max(similarities))

def sls_mrr(text,question):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                w1 = t_word
                w2 = q_word
                if w1[0:6] == w2[0:6]:
                    similarity = similarity + 1

        average_similarity = similarity / len(tokenized_question)
        similarities.append(average_similarity)
    answers =[]
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers 

def jaccard_similarity(text,question):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)
 
    for t_sent in tokenized_sents:
        similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                union = list(set(t_sent+tokenized_question))
                intersection = list(set(t_sent) - (set(t_sent)-set(tokenized_question)))
                jaccard_coeff = float(len(intersection))/len(union)
                similarity = similarity+jaccard_coeff

        average_similarity = similarity / len(t_sent)
        similarities.append(average_similarity)
    return similarities.index(max(similarities))  

def js_mrr(text,question):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)
 
    for t_sent in tokenized_sents:
        similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                union = list(set(t_sent+tokenized_question))
                intersection = list(set(t_sent) - (set(t_sent)-set(tokenized_question)))
                jaccard_coeff = float(len(intersection))/len(union)
                similarity = similarity+jaccard_coeff

        average_similarity = similarity / len(t_sent)
        similarities.append(average_similarity)
    answers =[]
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers  

def where_is_the_answer_euclidean(text,question,model):
    similarities = []
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    for t_sent in tokenized_sents:
        max_similarity = 0.0
        temp_summary = 0.0
        average_similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                if t_word in model and q_word in model:
                    similarity = euclidean_similarity(model[q_word],model[t_word])
                else:
                    similarity = 0.0
                if similarity>max_similarity:
                    max_similarity = similarity
            temp_summary += max_similarity
        
        average_similarity = temp_summary/len(tokenized_question)
        similarities.append(average_similarity)

    return similarities.index(max(similarities))

def calculate_sentence_vector_similarity_euclidean(text,question,model):
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)
    
    similarities = []
    max_similarity = 0.0
    text_vectors = []
    question_vector = model["kanarya"]-model["kanarya"]
    temp_vector = model["kanarya"]-model["kanarya"]
    
    for t_sent in tokenized_sents:
        for t_word in t_sent:
            if t_word in model:
                #similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                temp_vector += model[t_word]
        avg_vector = temp_vector / len(t_sent)
        text_vectors.append(avg_vector)
        temp_vector = model["kanarya"]-model["kanarya"]
    
    for q_word in tokenized_question:
        if q_word in model:
            question_vector += model[q_word]
    question_vector = question_vector / len(tokenized_question)

    for t_vector in text_vectors:
        similarity = euclidean_similarity(question_vector,t_vector)
        similarities.append(similarity)
    
    return similarities.index(max(similarities))  

def csvse_mrr(text,question,model):
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)
    
    similarities = []
    max_similarity = 0.0
    text_vectors = []
    question_vector = model["kanarya"]-model["kanarya"]
    temp_vector = model["kanarya"]-model["kanarya"]
    
    for t_sent in tokenized_sents:
        for t_word in t_sent:
            if t_word in model:
                #similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                temp_vector += model[t_word]
        avg_vector = temp_vector / len(t_sent)
        text_vectors.append(avg_vector)
        temp_vector = model["kanarya"]-model["kanarya"]
    
    for q_word in tokenized_question:
        if q_word in model:
            question_vector += model[q_word]
    question_vector = question_vector / len(tokenized_question)

    for t_vector in text_vectors:
        similarity = euclidean_similarity(question_vector,t_vector)
        similarities.append(similarity)
    
    for t_vector in text_vectors:
        similarity = euclidean_similarity(question_vector,t_vector)
        similarities.append(similarity)
    
    answers =[]
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers     

def euclidean_similarity(x,y):
    edist = sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
    edist = edist/10
    return 1-edist

def print_possible_answer(text,question,model):
    regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
    res = re.split(regex,text)
    print(res[where_is_the_answer(text,question,model)])
    
def calculate_sentence_vector_similarity(text,question,model):
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    similarities = []
    max_similarity = 0.0
    text_vectors = []
    question_vector = model["kanarya"]-model["kanarya"]
    temp_vector = model["kanarya"]-model["kanarya"]
    
    for t_sent in tokenized_sents:
        c = 0
        for t_word in t_sent:
            if t_word in model:
                #similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                temp_vector += model[t_word]
            else:
                c = c + 1
        avg_vector = temp_vector / (len(t_sent)-c)
        text_vectors.append(avg_vector)
        temp_vector = model["kanarya"]-model["kanarya"]
    
    for q_word in tokenized_question:
        c =0
        if q_word in model:
            question_vector += model[q_word]
        else:
            c = c + 1
    question_vector = question_vector / (len(tokenized_question)-c)

    for t_vector in text_vectors:
        similarity = ft.FastVector.cosine_similarity(question_vector,t_vector)
        similarities.append(similarity)
    
    return similarities.index(max(similarities))   

def csvs_mrr(text,question,model):
    tokenized_sents = tokenize(text)
    tokenized_question = tokenize_words(question)

    similarities = []
    max_similarity = 0.0
    text_vectors = []
    question_vector = model["kanarya"]-model["kanarya"]
    temp_vector = model["kanarya"]-model["kanarya"]
    
    for t_sent in tokenized_sents:
        c = 0
        for t_word in t_sent:
            if t_word in model:
                #similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                temp_vector += model[t_word]
            else:
                if t_word[0:6] in model:
                    temp_vector +=model[t_word[0:6]]
                else:
                    c = c + 1
                #print("<<"+t_word+">>")
        avg_vector = temp_vector / (len(t_sent)-c)
        text_vectors.append(avg_vector)
        temp_vector = model["kanarya"]-model["kanarya"]
    
    for q_word in tokenized_question:
        c =0
        if q_word in model:
            question_vector += model[q_word]
        else:
            if t_word[0:6] in model:
                temp_vector +=model[t_word[0:6]]
            else:
                c = c+1
    question_vector = question_vector / (len(tokenized_question)-c)

    for t_vector in text_vectors:
        similarity = ft.FastVector.cosine_similarity(question_vector,t_vector)
        similarities.append(similarity)  
    answers = []
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers

def handle_mrr(real_answers,answer_sets):
    total = 0.0
    for i in range(0,len(real_answers)):
        for j in range(0,3):
            if answer_sets[i][j] == real_answers[i]:
                total = total + 1/(j+1)
    return total/len(real_answers)

def handle_mrr_question_based(real_answers,answer_sets):
    total = 0.0
    for i in range(0,len(real_answers)):
        for j in range(0,3):
            if answer_sets[i][j] == real_answers[i]:
                total = total + 1/(j+0.9)
    return total

def compare_arrays(real,method):
    counter = 0.0
    for i in range(0,len(real)):
        if real[i]==method[i]:
            counter=counter+1
    return counter/len(real)

def compare_arrays_question_based(real,method):
    counter = 0.0
    for i in range(0,len(real)):
        if real[i]==method[i]:
            counter=counter+1
    return counter
def find_3_answers(text,question,model):
    similarities = []
    answers = []
    tokenized_sents = utils.tokenize(text)
    tokenized_question = utils.tokenize_words(question)

    for t_sent in tokenized_sents:
        max_similarity = 0.0
        temp_summary = 0.0
        average_similarity = 0.0
        for q_word in tokenized_question:
            for t_word in t_sent:
                if t_word in model and q_word in model:
                    similarity = ft.FastVector.cosine_similarity(model[q_word],model[t_word])
                else:
                    similarity = 0.0
                if similarity>max_similarity:
                    max_similarity = similarity
            temp_summary += max_similarity
            max_similarity = 0.0
        
        average_similarity = temp_summary/len(t_sent)
        similarities.append(average_similarity)
    for i in range (0,3):
        max_val = max(similarities)
        answers.append(similarities.index(max_val)+1)
        temp = similarities.index(max_val)
        similarities[temp] = -1
    return answers
    #return similarities.index(max(similarities))

def tokenize(text):
    res = text
    tokenized = []
    if res:
        for sent in res:
            sent = sent + " "
            tokenized.append(tokenize_words(sent))
        tokenized.pop()
        return tokenized
    else:
        return -1

def tokenize_words(cumle):
    kelimeler = []
    kelime = ""
    for harf in cumle:
        if(harf!=" "):
            if(harf in "0 1234567890!@#$%^&*()–-_;:’',./?\" \n\t\r"):
               pass
            else:
                kelime+=harf
        else:
            if(len(kelime)>0):
                kelime = kelime.lower()
                kelime = kelime.replace(" ","")
                kelime = kelime.replace("i̇","i")
                kelimeler.append(kelime)
                kelime = ""    
    return kelimeler

