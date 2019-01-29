#Version con triplete
import re
import os
import pickle
import random
from random import randint
import time


direccionBase = "D:\\DEMON\\baseWords\\InvertedSaved\\"
dirScann = "D:\\DEMON\\baseWords\\Books\\"
diccionario = {}

def limpiar(c):
	return re.sub('\W+', ' ', c)

def saveAux(inicial, object):
	#debe comprobar si existe la carpeta
	encontrado = 0
	if not os.path.exists(direccionBase + inicial):
		os.mkdir(direccionBase + inicial)
		print("Creando Directorio")

	with open(direccionBase + inicial + "\\" + object[0][0] + "_"+ object[0][1] + ".txt", "wb") as fh:
		pickle.dump(object, fh)

def saveMI(frase):
	with open("D:\\DEMON\\baseWords\\Output\\twitts.txt", 'a') as the_file:
		the_file.write(frase + '\r\n')
	
def construir(sentencia):
	wordList = limpiar(sentencia).lower().split(" ")
	tri = ["$","$"]
	tri.extend(wordList)
	tri.append("<END>")

	for i in range(0,len(tri) - 2):
		if tri[i] == "":
			tri[i] = "a-"
		mod = diccionario.setdefault((tri[i],tri[i + 1]),[0,[(tri[i + 2],0)]])
		enc = 0
		if(mod[1] != None and i + 2 < len(tri)):
			for j in range(len(mod[1])):
				if tri[i + 2] in mod[1][j]:
					mod[0] = mod[0] + 1
					mod[1][j] = (mod[1][j][0],mod[1][j][1] + 1)
					#if mod[1][j][0] == "<END>":
						#print(mod[1][j])
					enc = 1
					break;
			
			if enc == 0:
				clauster = (tri[i + 2],1)
				diccionario[(tri[i],tri[i + 1])][0] = diccionario[(tri[i],tri[i + 1])][0] + 1
				diccionario[(tri[i],tri[i + 1])][1].append(clauster)
			
	#print(diccionario[("$","$")])
			#print("n: " + str(i) + " longitud: " + str(len(tri)))
			#print(str((tri[i],tri[i + 1])))
			#saveAux(tri[i][0],((tri[i],tri[i + 1]),diccionario[(tri[i],tri[i + 1])]))

	#print(diccionario.keys())
		
def cargar(fi):
	obj = pickle.load(open(direccionBase + fi + ".txt", "rb" ))
	
def generarFrase():
	Oracion = ""
	pre = ["$","$"]
	next = "$"
	Oracion = ""
	while next != None:
		if pre[0] == "":
			pre[0] = "a-"
		mid = diccionario[(pre[0],pre[1])]
		#print(pre[0] + ". ." + pre[1])
		
		#print(str(mid))
		
		sum = 0
		cota = random.randint(0,mid[0])
		if mid[1] != None:
			for comb in mid[1]:
				sum = sum + comb[1]
				if sum >= cota:
					next = comb[0]
					break
			if next == "<END>":
				break
			Oracion = Oracion + next + " "
			pre = [pre[1],next]
		else:
			next = None
	print(Oracion)
	return Oracion

bagOfWords = {}
total = []


def archivar(doc, texto):
	txt = limpiar(texto)
	print(os.path.basename(doc))
	documento = bagOfWords.setdefault(os.path.basename(doc),{})
	
	palabras = txt.split(" ")
	palabras[:] = (value for value in palabras if (value != "" and value != " "))
	print(palabras)
	for i in palabras:
		contador = documento.setdefault(i,0)
		contador = contador + 1
		documento[i] = contador
		print("Guardo contador en el documento valor %i de la palabra %s" %(contador,i))
		
	bagOfWords[os.path.basename(doc)] = documento
	total.extend(bagOfWords.keys())

def cargarLibro():
	for doc in os.scandir(dirScann):
		if doc.is_file():
			docPath = doc.path
			print("decode: " + docPath)
			fichero = open(docPath, encoding='utf-8', mode="r" )
			text = fichero.read()
			
			while "" in text:
				text = text.replace("","")
				print("ELiminada rara")
			while "\n" in text:
				text = text.replace("\n","")
				print("ELiminada salto")
			while "\r" in text:
				text = text.replace("\r","")
				print("ELiminada carro")
			while "\t" in text:
				text = text.replace("\r","")
				print("ELiminada TAB")
			while "  " in text:
				text = text.replace("  "," ")
			
			frases = text.split(".")
			
			archivar(doc,text)
			
			for frase in frases:
				construir(frase)
	
	print(bagOfWords['Anime.txt'])
				
cargarLibro()
construir("El cocotero de mi tia sonia es el mejor")
construir("El cocotero de mameluco luco sonia es el mejor")

while True:
	saveMI(generarFrase())
	time.sleep(10)


print("fin del bucle")