class token:
    lex=""
    tipo=""
    linea=0
    def token(nombre,tip,linea):
        lex=nombre
        tipo=tip
        return
    def setlex(nombre):
        lex=nombre
        return
    def getlex():
        return lex
    def settipo(tip):
        tipo=tip
        return
    def settipo(lin):
        linea=lin
        return

class error:
    error=""
    linea=0
    columna=0
    def error(nombre,fil,col):
        error=nombre
        linea=fil
        columna=col
        return
    
def lexico(cadena, bandera2, fila, filaerr, colerr):
    i=0
    estado=1
    indice=0
    lexema=""
    x=len(cadena)
    bandera=0
    
    while(i<x):
        lexema=""
        if(bandera2==1):
            while(bandera2==1 and i<x):
                    if i<x and cadena[i]=="*":
                        i+=1
                        if i<x and cadena[i]=="/":
                            #tok=token()
                            #tok.lex=lexema
                            #tok.tipo="Comentario"
                            #tokens.append(tok)
                            #print(lexema)
                            #print("El lexema es un comentario2")
                            lexema=""
                            indice=0
                            estado=1
                            bandera=0
                            bandera2=0
                            i+=1
                        else:
                            #i-=1
                            #lexema=lexema[:indice]+cadena[i]
                            #indice+=1
                            i+=1
                            while(i<x and cadena[i] != '*'):
                                #lexema = lexema[:indice] + cadena[i]
                                #indice+=1
                                i+=1
                    else:
                        while(i<x and cadena[i] != '*'):
                            #lexema = lexema[:indice] + cadena[i]
                            #indice+=1
                            i+=1
        elif esletra(cadena[i]) != 0:
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            estado=2
            while(i<x and esdigitoletra(cadena[i]) != 0 ):
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
        
            for j in range(0,len(p_reservadas)):
                if lexema == p_reservadas[j]:
                    bandera=1
            
            if bandera==1:
                tok=token()
                tok.lex=lexema
                tok.tipo="Palabra Reservada"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es una Palabra reservada")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                tok=token()
                tok.lex=lexema
                tok.tipo="Identificador"+"\t"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Identificador")
                lexema=""
                indice=0
                estado=1
                bandera=0
        elif cadena[i] == "+":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            estado=2
            if cadena[i]=="+":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
        elif esdigito(cadena[i])!=0:
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            while(i<x and esdigito(cadena[i]) != 0):
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
            if cadena[i] == ".":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                if i<x and esdigito(cadena[i]) != 0:
                    
                    lexema = lexema[:indice] + cadena[i]
                    indice+=1
                    i+=1
                    while(i<x and esdigito(cadena[i]) != 0):
                        lexema = lexema[:indice] + cadena[i]
                        indice+=1
                        i+=1
                    tok=token()
                    tok.lex=lexema
                    tok.tipo="Flotante"+"\t"
                    tok.linea=fila
                    tokens.append(tok)
                    #print(lexema)
                    #print("El lexema es un Flotante")
                    lexema=""
                    indice=0
                    estado=1
                    bandera=0
                else:
                    err=error()
                    err.error=lexema
                    err.linea=fila
                    err.columna=i
                    errores.append(err)
                    #print(lexema)
                    #print("Error en fila: " + str(fila) + " columna:"+ str(i))
                    lexema=""
                    indice=0
                    estado=1
                    bandera=0
            else:
                tok=token()
                tok.lex=lexema
                tok.tipo="Entero"+"\t"+"\t"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Entero")
                lexema=""
                indice=0
                estado=1
                bandera=0
        elif cadena[i] == "-":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            estado=2
            if cadena[i]=="-":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
        elif cadena[i]=="<":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            if cadena[i]=="=":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
        elif cadena[i]==">":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            if cadena[i]=="=":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
        elif cadena[i]==":":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            if cadena[i]=="=":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                err=error()
                err.error=lexema
                err.linea=fila
                err.columna=i
                errores.append(err)
                #print(lexema)
                #print("Error en fila: " + str(fila) + " columna:"+ str(i))
                lexema=""
                indice=0
                estado=1
                bandera=0
                #Aqui falta algo else

        elif cadena[i]=="=":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            if cadena[i]=="=":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                err=error()
                err.error=lexema
                err.linea=fila
                err.columna=i
                errores.append(err)
                #print(lexema)
                #print("Error en fila: " + str(fila) + " columna:"+ str(i))
                lexema=""
                indice=0
                estado=1
                bandera=0
                #Aqui falta algo
        elif cadena[i]=="!":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            if cadena[i]=="=":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                tok=token()
                tok.lex=lexema
                tok.tipo="Simbolo Especial"
                tok.linea=fila
                tokens.append(tok)
                #print(lexema)
                #print("El lexema es un Simbolo especial")
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                err=error()
                err.error=lexema
                err.linea=fila
                err.columna=i
                errores.append(err)
                #print(lexema)
                #print("Error en fila: " + str(fila) + " columna:"+ str(i))
                lexema=""
                indice=0
                estado=1
                bandera=0
            #Aqui falta algo
        elif cadena[i]=="/":
            i+=1
            if cadena[i]=="/":
                i+=1
                while cadena[i] != "\n":
                    #lexema = lexema[:indice] + cadena[i]
                    #indice+=1
                    i+=1
                #tok=token()
                #tok.lex=lexema
                #tok.tipo="Comentario"
                #tokens.append(tok)
                #print(lexema)
                #print("El lexema es un comentario1")
                lexema=""
                indice=0
                estado=1
                bandera=0
                #desde aqui
            elif cadena[i] == "*":
                filaerr=fila
                colerr=i
                i+=1
                bandera2=1
                while(i<x and bandera2==1):
                    if i<x and cadena[i]=="*":
                        i+=1
                        if i<x and cadena[i]=="/":
                            #tok=token()
                            #tok.lex=lexema
                            #tok.tipo="Comentario"
                            #tokens.append(tok)
                            #print(lexema)
                            #print("El lexema es un comentario2")
                            lexema=""
                            indice=0
                            estado=1
                            bandera=0
                            bandera2=0
                            i+=1
                        else:
                            #i-=1
                            #lexema=lexema[:indice]+cadena[i]
                            #indice+=1
                            i+=1
                            while(i<x and cadena[i] != '*'):
                                #lexema = lexema[:indice] + cadena[i]
                                #indice+=1
                                i+=1
                    else:
                        while(i<x and cadena[i] != '*'):
                            #lexema = lexema[:indice] + cadena[i]
                            #indice+=1
                            i+=1
            else:
                    i-=1
                    lexema = lexema[:indice] + cadena[i]
                    tok=token()
                    tok.lex=lexema
                    tok.tipo="Simbolo Especial"
                    tok.linea=fila
                    tokens.append(tok)
                    #print(lexema)
                    #print("El lexema es un Simbolo especial")
                    lexema=""
                    indice=0
                    i+=1
                    estado=1
                    bandera=0
                    bandera2=0
            #Hasta aqui
        
        elif cadena[i]=="*" or cadena[i]=="%" or cadena[i]=="," or cadena[i]==";" or cadena[i]=="(" or cadena[i]==")" or cadena[i]=="{" or cadena[i]=="}":
            lexema = lexema[:indice] + cadena[i]
            indice+=1
            i+=1
            tok=token()
            tok.lex=lexema
            tok.tipo="Simbolo Especial"
            tok.linea=fila
            tokens.append(tok)
            #print(lexema)
            #print("El lexema es un Simbolo especial")
            lexema=""
            indice=0
            estado=1
            bandera=0
        else:
            if cadena[i]!=" " and cadena[i]!="\t" and cadena[i]!="\n":
                lexema = lexema[:indice] + cadena[i]
                indice+=1
                i+=1
                
                while(i<x and esletra(cadena[i])!=1 and cadena[i]!="+" and esdigito(cadena[i])!=1 and cadena[i]!="-" and cadena[i]!="<" and cadena[i]!=">" and cadena[i]!=":"  and cadena[i]!="="  and cadena[i]!="!"  and cadena[i]!="/"  and cadena[i]!="*" and cadena[i]!="%" and cadena[i]!="," and cadena[i]!=";" and cadena[i]!="(" and cadena[i]!=")" and cadena[i]!="{" and cadena[i]!="}" and cadena[i]!=" " and cadena[i]!="\t"  and cadena[i]!="\n"):
                    lexema = lexema[:indice] + cadena[i]
                    indice+=1
                    i+=1
                err=error()
                err.error=lexema
                err.linea=fila
                err.columna=i
                errores.append(err)
                #print(lexema)
                #print("Error en fila: " + str(fila) + " columna:"+ str(i))
                lexema=""
                indice=0
                estado=1
                bandera=0
            else:
                i+=1
            

    return (bandera2,filaerr,colerr)

def esletra(letra):
    if letra>='A' and letra<='Z':
        return 1
    elif letra>='a' and letra<='z':
        return 1
    elif letra=='_':
        return 1
    else:
        return 0

def esdigitoletra(letra):
    if letra>='A' and letra<='Z':
        return 1
    elif letra>='a' and letra<='z':
        return 1
    elif letra>='0' and letra<='9':
        return 1
    elif letra=='_':
        return 1
    else:
        return 0

def esdigito(letra):
    if letra>='0' and letra<='9':
        return 1
    else:
        return 0

import sys
ruta=sys.argv[1]

p_reservadas=['main','if','then','else','end','do','while','repeat',
              'until','cin','cout','real','int','boolean']
bandera2=0
archivo = open(ruta, "r")
fila = 1
tokens=[]
errores=[]
filaerr=0
colerr=0

for linea in archivo.readlines():
    bandera2,filaerr,colerr = lexico(linea, bandera2, fila, filaerr, colerr)
    fila+=1

if bandera2!=0:
    err=error()
    err.error="Comentario no cerrado"
    err.linea=filaerr
    err.columna=colerr
    errores.append(err)

import os.path 
if os.path.exists('Lexema.txt'):
    import os
    os.remove('Lexema.txt')
else:
    outfile = open('Lexema.txt', 'a')
    
if os.path.exists('MuestraLexema.txt'):
    import os
    os.remove('MuestraLexema.txt')
else:
    outfile = open('MuestraLexema.txt', 'a')



for i in range(0,len(tokens)):
    outfile = open('Lexema.txt', 'a') 
    outfile.write(tokens[i].lex + "\t" + tokens[i].tipo + "\t" + str(tokens[i].linea) + "\n")
    outfile.close()
    outfile = open('MuestraLexema.txt', 'a') 
    outfile.write(tokens[i].lex + "\t" + tokens[i].tipo + "\n")
    outfile.close()
    
outfile = open('MuestraLexema.txt', 'r') 
print (outfile.read())

import os.path 
if os.path.exists('Errores.txt'):
    import os
    os.remove('Errores.txt')
else:
    outfile = open('Errores.txt', 'a')


outfile = open('Errores.txt', 'a')
outfile.write("\t ERRORES LEXICO \n\n")
outfile.close()



for i in range(0,len(errores)):
    outfile = open('Errores.txt', 'a')
    outfile.write("ERROR: '" + errores[i].error + "'" + "\t Fila:" + str(errores[i].linea) + "   \t Columna:" + str(errores[i].columna) + "\n")
    outfile.close()
    
outfile = open('Errores.txt', 'r') 
print (outfile.read())

    #x=len(cadena)
    #cadena=cadena[:x]+linea

#print(cadena)
#lexico(cadena)


    


    
    
