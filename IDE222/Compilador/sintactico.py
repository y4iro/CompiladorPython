#Clases
class Nodo(object):
    def __init__(self,hij=None,her=None,lin=0,cat=None,tip=None,cont=None,tabs=0):
        self.hijos=[]
        if hij is not None:
            for i in hij:
                self.hijos.append(i)
        self.hermano=her
        self.linea=lin
        self.categoria=cat
        self.tipo=tip
        self.contenido=cont
        self.tabuladores=tabs
        #Nuevo
        #Aqui le cambie
        self.value=0
        self.type=None
        
class tokens:
    contenido=""
    tipo=""
    Filaa=0

    #Funciones

#programa-->main { listadeclaracion listasentencias }
def programa():
    global token
    #checkinput(pprograma,sprograma)
    arbol=Nodo()
    arbol.contenido="main"
    match("main")
    match("{")
    t=listadeclaracion()
    u=listasentencias()
    if t!= None:
        arbol.hijos.append(t)
    if u!= None:
        arbol.hijos.append(u)
    matchFin("}")
    #checkinput(sprograma,pprograma)
    return arbol

#listadeclaracion --> {declaracion;}
def listadeclaracion():
    global token
    #checkinput(plistadeclaracion,sdeclaracion)
    q=None
    if (token.contenido=="int" or token.contenido=="real" or token.contenido=="boolean"):
        t=declaracion()
        q=t
        matchFin(";")
        while(token.contenido=="int" or token.contenido=="real" or token.contenido=="boolean"):
            p=declaracion()
            t.hermano=p
            t=p
            matchFin(";")
    #checkinput(slistadeclaracion,pdeclaracion)
    return q
            
    
#declaracion --> tipo listavariables
def declaracion():
    global token
    checkinput(pdeclaracion,sdeclaracion)
    if(token.contenido=="int"):
        t=nodoDeclaracion("tipo")
        t.contenido="int"
        match("int")
        t.hijos.append(listavariables())
        return t
    elif(token.contenido=="real"):
        t=nodoDeclaracion("tipo")
        t.contenido="real"
        match("real")
        t.hijos.append(listavariables())
        return t
    elif(token.contenido=="boolean"):
        t=nodoDeclaracion("tipo")
        t.contenido="boolean"
        match("boolean")
        q=listavariables()
        t.hijos.append(q)
        
        return t
    else:
        #print("ERROR: token inesperado "+token.contenido)
        return None
    checkinput(sdeclaracion,pdeclaracion)
    return None

#listavariables --> { identificador , } identificador
def listavariables():
    global token
    checkinput(plistavariables,slistavariables)
    t=nodoDeclaracion("variable")
    t.contenido=token.contenido
    matchTipo("Identificador")
    p=t
    while(token.contenido==","):
        match(",")
        q=nodoDeclaracion("variable")
        q.contenido=token.contenido
        matchTipo("Identificador")
        p.hermano=q
        p=q
    checkinput(slistavariables,plistavariables)
    return t

#listasentencias --> { sentencia } [ sentencia ]
def listasentencias():
    global token
    #checkinput(plistasentencias,slistasentencias)
    q=None
    if (token.contenido=="if" or token.contenido=="while" or
        token.contenido=="repeat" or token.contenido=="cin" or token.contenido=="cout" or token.contenido=="{" or token.tipo=="Identificador"):
        t=sentencia()
        #if t!=None:
        q=t
        while (token.contenido=="if" or token.contenido=="while" or token.contenido=="repeat" or token.contenido=="cin" or token.contenido=="cout" or token.contenido=="{" or token.tipo=="Identificador"):
            p=sentencia()
            t.hermano=p
            t=p
    #checkinput(slistasentencias,plistasentencias)
    return q

#aparecio FIN
#sentencia --> seleccion | iteracion | repeticion | sentcin | sentcout | bloque | asignacion
def sentencia():
    global token
    checkinput(psentencia,ssentencia)
    if(token.contenido=="if"):
        t=seleccion()
    elif(token.contenido=="while"):
        t=iteracion()
    elif(token.contenido=="repeat"):
        t=repeticion()
    elif(token.contenido=="cin"):
        t=sentcin()
    elif(token.contenido=="cout"):
        t=sentcout()
    elif(token.contenido=="{"):
        t=bloque()
    elif(token.tipo=="Identificador"):
        t=asignacion()
        if(t==None):
            return None
    else:
        errores.append("ERROR: token esperado "+token.contenido +" Fila: " +str(token.linea))
        #print("ERROR: token esperado "+token.contenido +" Fila: " +str(token.linea))
        return None
    checkinput(ssentencia,psentencia)
    return t

#seleccion --> if ( expresion ) then bloque [ else bloque ]
def seleccion():
    global token
    checkinput(pseleccion,sseleccion)

    t=nodoSentencia("seleccion")
    t.contenido=token.contenido
    match("if")
    match ("(")
    u=Nodo()
    u.contenido="Condicion"
    t.hijos.append(u)
    u.hijos.append(expresion())
    matchFin(")")
    match("then")
    verdadero=Nodo()
    verdadero.contenido="Verdadero"
    t.hijos.append(verdadero)
    verdadero.hijos.append(bloque())
    if(token.contenido=="else"):
        match("else")
        falso=Nodo()
        falso.contenido="Falso"
        t.hijos.append(falso)
        falso.hijos.append(bloque())

    checkinput(sseleccion,pseleccion)
    return t

#aparecio FIN
#iteracion --> while ( expresion ) bloque
def iteracion():
    global token
    checkinput(piteracion,siteracion)
    u=Nodo()
    u.contenido="Condicion"
    t=nodoSentencia("iteracion")
    t.contenido=token.contenido
    match("while")
    match("(")
    p=expresion()
    t.hijos.append(u)
    u.hijos.append(p)
    matchFin(")")
    a=Nodo()
    a.contenido="Bloque"
    q=bloque()
    t.hijos.append(a)
    a.hijos.append(q)
    checkinput(siteracion,piteracion)
    return t
    

#repeticion --> repeat bloque until ( expresion );
def repeticion():
    global token
    checkinput(prepeticion,srepeticion)
    t=nodoSentencia("repeticion")
    t.contenido=token.contenido
    match("repeat")
    p=bloque()
    b=Nodo()
    b.contenido="bloque"
    t.hijos.append(b)
    b.hijos.append(p)
    u=Nodo()
    u.contenido="until"
    t.hijos.append(u)
    match("until")
    match("(")
    q=expresion()
    u.hijos.append(q)
    matchFin(")")
    matchFin(";")
    checkinput(srepeticion,prepeticion)
    return t
    

#sentcin --> cin identificador;
def sentcin():
    global token
    checkinput(psentcin,ssentcin)
    t=nodoSentencia("sentcin")
    t.contenido=token.contenido
    match("cin")
    p=nodoExpresion("identificador")
    p.contenido=token.contenido
    t.hijos.append(p)
    matchTipo("Identificador")
    matchFin(";")
    checkinput(ssentcin,psentcin)
    return t

#sentcout --> cout expresion;
def sentcout():
    global token
    checkinput(psentcout,ssentcout)
    t=nodoSentencia("sentcout")
    t.contenido=token.contenido
    match("cout")
    p=expresion()
    t.hijos.append(p)
    matchFin(";")
    checkinput(ssentcout,psentcout)
    return t

#bloque --> { listasentencia }
def bloque():
    global token
    checkinput(pbloque,sbloque)
    match("{")
    t=listasentencias()
    matchFin("}")
    checkinput(sbloque,pbloque)
    return t

#asignacion --> identificador := expresion;
def asignacion():
    global token
    checkinput(pasignacion,sasignacion)
    
    t=nodoSentencia("asignacion")
    t.contenido=token.contenido
    matchTipo("Identificador")
    if(token.contenido=="++"):
        match("++")
        Nodo1=nodoExpresion("operador")
        Nodo1.contenido="+"
        t.hijos.append(Nodo1)
        Nodo2=nodoExpresion("identificador")
        Nodo2.contenido=t.contenido
        Nodo1.hijos.append(Nodo2)
        Nodo3=nodoExpresion("numero")
        Nodo3.contenido="1"
        Nodo1.hijos.append(Nodo3)
    elif(token.contenido=="--"):
        match("--")
        Nodo1=nodoExpresion("operador")
        Nodo1.contenido="-"
        t.hijos.append(Nodo1)
        Nodo2=nodoExpresion("identificador")
        Nodo2.contenido=t.contenido
        Nodo1.hijos.append(Nodo2)
        Nodo3=nodoExpresion("numero")
        Nodo3.contenido="1"
        Nodo1.hijos.append(Nodo3)
    else:
        match(":=")
        p=expresion()
        t.hijos.append(p)
    matchFin(";")
    checkinput(sasignacion,pasignacion)
    return t
    

#expresion --> expresionsimple [ relacion expresionsimple ]
def expresion():
    global token
    #checkinput(pexpresion,sexpresion)
    t=expresionsimple()
    if(token.contenido == "<=" or token.contenido == "<" or token.contenido == ">" or token.contenido == ">=" or token.contenido == "==" or token.contenido == "!="):
        p=nodoExpresion("operador")
        p.contenido=token.contenido
        p.hijos.append(t)
        match(token.contenido)
        t=p
        q=expresionsimple()
        p.hijos.append(q)
    #checkinput(sexpresion,pexpresion)
    return t
     

#expresionsimple --> termino { suma-op termino } 
def expresionsimple():
    global token
    #checkinput(pexpresionsimple,sexpresionsimple)
    t=termino()
    while(token.contenido == "+" or token.contenido == "-"):
          p=nodoExpresion("operador")
          p.contenido=token.contenido
          p.hijos.append(t)
          match(token.contenido)
          t=p
          q=termino()
          p.hijos.append(q)
    #checkinput(sexpresionsimple,pexpresionsimple)
    return t

#termino --> factor { mult-op factor }
def termino():
    global token
    #checkinput(ptermino,stermino)
    t=factor()
    while(token.contenido == "*" or token.contenido == "/"):
          p=nodoExpresion("operador")
          p.contenido=token.contenido
          p.hijos.append(t)
          match(token.contenido)
          t=p
          q=factor()
          p.hijos.append(q)
    #checkinput(stermino,ptermino)
    return t          
          
#factor-->(expresion)|numero|identificador
def factor():
    global token
    #checkinput(pfactor,sfactor)
    if(token.contenido=="("):
        match("(")
        Nodo=expresion()
        matchFin(")")
        return Nodo
    elif(token.tipo=="Entero"):
        Nodo=nodoExpresion("numero")
        Nodo.contenido=token.contenido
        matchTipo(token.tipo)
        return Nodo
    elif(token.tipo=="Flotante"):
        Nodo=nodoExpresion("flotante")
        Nodo.contenido=token.contenido
        matchTipo(token.tipo)
        return Nodo
    elif(token.tipo=="Identificador"):
        Nodo=nodoExpresion("identificador")
        Nodo.contenido=token.contenido
        matchTipo(token.tipo)
        return Nodo
    else:
        errores.append("ERROR: token inesperado '"+token.contenido+"' Fila: "+str(token.linea))
        #print("ERROR: token inesperado '"+token.contenido+"' Fila: "+str(token.linea))
        return None
    #checkinput(sfactor,pfactor)
    return None

    #Generales
def nodoSentencia(tip):
    global actual
    sentencia=Nodo()
    sentencia.categoria="Sentencia"
    sentencia.tipo=tip
    sentencia.contenido=sintactico[actual].contenido
    sentencia.linea=sintactico[actual].linea
    return sentencia
    

def nodoExpresion(tip):
    global actual
    expresion=Nodo()
    expresion.categoria="Expresion"
    expresion.tipo=tip
    expresion.contenido=sintactico[actual].contenido
    expresion.linea=sintactico[actual].linea
    return expresion

def nodoTipo(tip):
    global actual
    tipo=Nodo()
    tipo.categoria="Tipo"
    tipo.tipo=tip
    tipo.contenido=sintactico[actual].contenido
    tipo.linea=sintactico[actual].linea
    return tipo

def nodoDeclaracion(tip):
    global actual
    declaracion=Nodo()
    declaracion.categoria="Declaracion"
    declaracion.tipo=tip
    declaracion.contenido=sintactico[actual].contenido
    declaracion.linea=sintactico[actual].linea
    return declaracion

def match(expected):
    global actual
    global token
    #print( "match: " + sintactico[actual].contenido )
    if sintactico[actual].contenido==expected:
        token=getToken()
        return True
    else:
        errores.append("ERROR: token esperado '"+expected+"' Fila: "+str(token.linea))
        #print("ERROR: token esperado '"+expected+"' Fila: "+str(token.linea))
        return False

def matchFin(expected):
    global actual
    global token
    #print( "match: " + sintactico[actual].contenido )
    if sintactico[actual].contenido==expected:
        token=getToken()
        return True
    else:
        errores.append("ERROR: token esperado '"+expected+"' Fila: "+str(sintactico[actual-1].linea))
        #print("ERROR: token esperado '"+expected+"' Fila: "+str(sintactico[actual-1].linea))
        return False

def matchTipo(expected):
    global actual
    global token
    #print( "matchTipo: " + sintactico[actual].contenido )
    if sintactico[actual].tipo==expected:
        token=getToken()
        return True
    else:
        errores.append("ERROR: token esperado '"+expected+"' Fila: "+str(token.linea))
        #print("ERROR: token esperado '"+expected+"' Fila: "+str(token.linea))
        return False

def getToken():
    global actual
    actual+=1
    if actual==len(sintactico):
        return None
    #print("..."+sintactico[actual].contenido)
    return sintactico[actual]

def imprime(arbol,tabs):
    if(arbol != None):
        arbol.tabs = tabs
        texto = ""
        for i in range(tabs):
            texto+="\t"
        if(arbol.tipo==None):
            arbol.tipo="None"
        if(arbol.categoria==None):
            arbol.categoria="None"
        print( texto + " " + arbol.contenido )
        outfile = open('MuestraSintaxis.txt', 'a')
        outfile.write(texto + " " + arbol.contenido + "\n")
        outfile.close()
        for i in range (len(arbol.hijos)):
            imprime(arbol.hijos[i],tabs+1)
            """i=0
            while i<len(arbol.hijos):
                imprime(arbol.hijos[i],tabs+1)
                i+=1"""
        imprime(arbol.hermano,tabs)

#Recuperacion de ERRORES
def checkinput(p,s):
    global token
    #print(token.contenido)
    #print(token.contenido in p or token.tipo in p)
    if not (token.contenido in p or token.tipo in p or token.contenido=='FIN'):
        errores.append("ERROR: token inesperado '"+token.contenido+"' Fila: "+str(token.linea))
        #print("ERROR: token inesperado '"+token.contenido+"' Fila: "+str(token.linea))
        p+=s
        scanto(p)

def scanto(p):
    global token
    global actual
    #print(token.contenido + token.tipo+str(p))
    #print((token.contenido in p) or (token.tipo in p ) or (actual!=len(sintactico)))

    while not ((token.contenido in p) or (token.tipo in p ) or (actual==len(sintactico)) or (token.contenido=="FIN")):
        #print("ENTROOO")
        token=getToken()

def sintaxis():
    global arbol
    archivo = open("Lexema.txt","r")

    for linea in archivo.readlines():
        auxiliar = tokens()
        partir = (linea.split())
        if len(partir) == 4:
            auxiliar.contenido = partir[0]
            auxiliar.tipo=partir[1]+" " +partir[2]
            auxiliar.linea=partir[3]
            sintactico.append(auxiliar)
        else:
            auxiliar.contenido = partir[0]
            auxiliar.tipo=partir[1]
            auxiliar.linea=partir[2]
            sintactico.append(auxiliar)

    token = sintactico[0]
    #Aqui le cambie
    Tokk=tokens()
    Tokk.contenido="FIN"
    sintactico.append(Tokk)
    arbol=programa()
    
    return arbol

def archivos_errores():
    arbol=sintaxis()
    import os.path
    if os.path.exists('MuestraSintaxis.txt'):
        import os
        os.remove('MuestraSintaxis.txt')
    else:
        outfile = open('MuestraSintaxis.txt', 'a')

    outfile = open('Errores.txt', 'a')
    outfile.write("\n\n\tERRORES SINTACTICO\n\n")

    for i in range(0,len(errores)):
        outfile.write(errores[i]+"\n")

    outfile.close()

    imprime(arbol,0)


    for i in errores:
        print("["+i+"]")



#import sys
#ruta=sys.argv[1]

#Principal
sentencias=['seleccion','iteracion','repeticion','sentcin','sentcout','bloque','asignacion']
expresiones=['numero','identificador','flotante','operador']
tipos=['int','real','boolean']
declaraciones=['tipo','variable']

#Primeros
pprograma=['main']
plistadeclaracion=['int','real','boolean']#vacio??
pdeclaracion=['int','real','boolean']
plistavariables=['Identificador']
plistasentencias=['if','while','repeat','cin','cout','{','Identificador']#vacio??
psentencia=['if','while','repeat','cin','cout','{','Identificador']#vacio??
pseleccion=['if']
piteracion=['while']
prepeticion=['repeat']
psentcin=['cin']
psentcout=['cout']
pbloque=['{']
pasignacion=['Identificador']
pexpresion=['(','numero','Identificador']
pexpresionsimple=['(','numero','Identificador']
ptermino=['(','numero','Identificador']
pfactor=['(','numero','Identificador']

#Siguientes
sprograma=['FIN']
slistadeclaracion=['if','while','repeat','cin','cout','{','Identificador','}']
sdeclaracion=[';']
slistavariables=[';']
slistasentencias=['}']
ssentencia=['if','while','repeat','cin','cout','{','Identificador','}']
sseleccion=['if','while','repeat','cin','cout','{','Identificador','}']
siteracion=['if','while','repeat','cin','cout','{','Identificador','}']
srepeticion=['if','while','repeat','cin','cout','{','Identificador','}']
ssentcin=['if','while','repeat','cin','cout','{','Identificador','}']
ssentcout=['if','while','repeat','cin','cout','{','Identificador','}']
sbloque=['if','while','repeat','cin','cout','{','Identificador','}','else','until']
sasignacion=['if','while','repeat','cin','cout','{','Identificador','}']
sexpresion=[')',';']
sexpresionsimple=['<=','<','>','>=','==','!=',')',';']
stermino=['+','-','<=','<','>','>=','==','!=',')',';']
sfactor=['*','/','+','-','<=','<','>','>=','==','!=',')',';']

sintactico=[]
errores=[]
global actual
actual=0
global token
global arbol

