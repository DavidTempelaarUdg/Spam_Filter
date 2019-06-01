import os
import math
import random


print ("Pràctica filtre SPAM")

#path = 'C:\\Users\\David\\Downloads\\emailsENRON\\emailsENRON'

percentatge_prova=0.8
timesWordsH = {}
timesWordsS = {}
totals =[0,0] #primer valor total Ham i el segon total Spam
fileHam = []
fileSpam = []
lambd = 50
totalEvaluats =0
totalEvaluatsH = 0
totalEvaluatsS = 0
k = 0.30000000000001208
PHI = 7.3
paraules_diferents = 0
margeSpam = 0.5 #Si el percentatge de que un correu sigui Spam és major que aquest valor es marcarà com a Spam

Fals_negatiu = 0
Fals_positiu = 0
Correcte_positiu = 0
Correcte_negatiu = 0

def llegirNomsFiles():
    global fileHam
    global fileSpam
    fileHam =[]
    fileSpam = []
    for r, d, f in os.walk(path):
        for folder in d:
            for q, di, n in os.walk(os.path.join(r,folder)):
                for file in n:
                    if '.txt' in file:
                        if folder=="HAM" :
                            fileHam.append(os.path.join(q, file))
                        else :
                            fileSpam.append(os.path.join(q,file))
                    

def llegirParaulesEmails():
    compt=0
    for i in fileHam:
        if (percentatge_prova*fileHam.__len__() < compt) :
            break
        wordsHam = open(i, encoding = "latin-1").read().split()
        afegirParaula(wordsHam,timesWordsH, False)
        compt+=1

    compt=0
    for j in fileSpam:
        if (percentatge_prova*fileSpam.__len__() < compt) :
            break
        wordsSpam = open(j, encoding = "latin-1").read().split()
        afegirParaula(wordsSpam,timesWordsS,True)
        compt+=1


def afegirParaula(paraules, timesWords,op):
    for i in paraules:
        global paraules_diferents
        if not(i in timesWordsS) and not(i in timesWordsH) :
            timesWordsH[i]=0
            timesWordsS[i]=0
            paraules_diferents+=1

        timesWords[i]+=1
        totals[int(op)]+=1
        



def naiveBayes(llistaParaules):
    pCorreu = 0
    pSpam = 0
    pHam = 0

    for i in llistaParaules :
        if(i in timesWordsH and i in timesWordsS):
            pSpam += math.log((timesWordsS[i]+k)/(totals[1]+paraules_diferents*k))
            pHam += math.log((timesWordsH[i]+k)/(totals[0]+paraules_diferents*k))

    pHam+=math.log(totals[0]/(totals[0]+totals[1]))
    pSpam+=math.log(totals[1]/(totals[0]+totals[1]))
    pHam+=math.log(PHI)
    return pSpam>pHam



def evaluar() :

    global Fals_positiu
    global Fals_negatiu
    global Correcte_negatiu
    global Correcte_positiu
    global totalEvaluats
    global totalEvaluatsH 
    global totalEvaluatsS 
    global path


    Fals_positiu=0
    Fals_negatiu=0
    Correcte_negatiu=0
    Correcte_positiu=0
    totalEvaluats = 0
    totalEvaluatsH = 0
    totalEvaluatsS = 0
    
    if(path=="C:\Home\SpamFilter_IA\emailsENRON\emailsENRON"):
        compt = 0
        for i in fileHam :
            compt += 1
            if compt > fileHam.__len__()*0.8:
                if naiveBayes(open(i, encoding = "latin-1").read().split()) :
                    Fals_negatiu += 1
                else :
                    Correcte_positiu += 1

                totalEvaluats += 1
                totalEvaluatsH += 1

        compt = 0
        for i in fileSpam:
            compt += 1
            if compt > fileSpam.__len__()*0.8:
                if naiveBayes(open(i, encoding = "latin-1").read().split()) :
                    Correcte_negatiu += 1
                else :
                    Fals_positiu += 1

                totalEvaluats += 1
                totalEvaluatsS += 1
    else :
        totalEvaluats = 0
        totalEvaluatsH = 0
        totalEvaluatsS = 0
        llegirNomsFiles()
        llegirParaulesEmails()
        for i in fileHam :
            if naiveBayes(open(i, encoding = "latin-1").read().split()) :
                Fals_negatiu+=1
            else :
                Correcte_positiu+=1
            totalEvaluats+=1
            totalEvaluatsH+=1

        for i in fileSpam :
            if naiveBayes(open(i, encoding = "latin-1").read().split()) :
                Correcte_negatiu+=1
            else :
                Fals_positiu+=1
            totalEvaluats+=1
            totalEvaluatsS+=1




def estudiMillorVariables():
    global k
    global PHI

    aux_k = 2
    aux_PHI = 2
    aux_false_Negatiu = 100000
    aux_false_Positiu = 100000

    for i in range(0, 100 ): #int((totals[0]+totals[1])/4
        if (Fals_negatiu == 0 and Fals_positiu == 0 and Correcte_positiu == 0 and Correcte_negatiu == 0):
            evaluar()
        else:
            k += random.randint(-(Fals_negatiu+Fals_positiu/5)*10, (Fals_negatiu+Fals_positiu/5)*10)/10
            PHI += random.randint(-(Fals_negatiu+Fals_positiu/5)*10, (Fals_negatiu+Fals_positiu/5)*10)/10
            while(k<=0):
                k += random.randint(0, (Fals_negatiu+Fals_positiu/5)*10)/10
            
            while(PHI<=0):
                PHI += random.randint(0, (Fals_negatiu+Fals_positiu/5)*10)/10

            evaluar()
            if (Fals_negatiu+Fals_positiu/5)<(aux_false_Negatiu+aux_false_Positiu/5) :
                aux_k=k
                aux_PHI=PHI
                aux_false_Negatiu = Fals_negatiu
                aux_false_Positiu = Fals_positiu

    print("aux_k: " + (str)(aux_k))
    k = aux_k
    PHI = aux_PHI


path= input("Entri la ubicacio de les carpetes HAM i SPAM \n")


llegirNomsFiles()
llegirParaulesEmails()
""" print(timesWordsH) """

#estudiMillorVariables()

path = input("Entri el path a les dades a evaluar\n")

evaluar()


print("Totals evaluatsH: " + (str)(totalEvaluatsH))
print("Totals evaluatsS: " + (str)(totalEvaluatsS))
print("Totals evaluats: " + (str)(totalEvaluats))
print("millor k: "+ (str)(k))
print("millor PHI: " + (str)(PHI))
print("Accuracy: (%): "+ (str)(((Correcte_positiu+Correcte_negatiu)/totalEvaluats)*100))
""" print(Correcte_negatiu)
print(Correcte_positiu) """
print("False positive rate (%): "+(str)((Fals_positiu/totalEvaluats)*100))
print("False negative rate (%): "+(str)((Fals_negatiu/totalEvaluats)*100))


werr = (lambd * Fals_positiu + Fals_negatiu) / (lambd * totalEvaluatsH + totalEvaluatsS)
werr_base = totalEvaluatsS / (lambd * totalEvaluatsH + totalEvaluatsS)
ratio = werr_base/werr

print("Total cost ratio: "+(str)(ratio))
