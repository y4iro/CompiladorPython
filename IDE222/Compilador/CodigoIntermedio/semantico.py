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
        self.value=None
        self.type=None
         
#clase para las lineas de los datos de la tabla hash
class LineListRec:
    linea=0;
    sig=None;
 
#clase para los datos de la tabla hash
class BucketListRec:
    name="";
    lines=LineListRec();
    memloc="";
    valor=None
    ttype=None
    sig=None;
 
#FUNCIONES    
 
#funcion hash
def hasha(key):
    global size;
    global shift;
    temp=0;
    for i in key :
        temp=((temp << shift) + ord(i)) %size;
    return temp
 
#Funcion que inserta los numeros de linea en la tabla hash
def st_insert(name,linea,loc,val,ty):
    global hashtable;
    h=hasha(name)
    l=BucketListRec();
    l=hashtable[h];
    while((l!=None) and (name is not l.name)):
        l=l.sig;
    if(l==None): #Si la variable no se encuentra en la tabla
        l=BucketListRec()
        l.name=name
        l.lines=LineListRec();
        l.lines.linea=linea
        l.memloc=loc
        l.valor=val
        l.ttype=ty
        l.lines.sig=None
        l.sig=hashtable[h]
        hashtable[h]=l;
    else: #Si si se encuentra en la tabla
        t=LineListRec();
        t=l.lines;
        while(t.sig != None):
            t=t.sig;
        t.sig=LineListRec();
        t.sig.linea=linea;
        t.sig.sig=None;
 
#Funcion que actualiza en la tabla hash el valor que tiene la variable 
def st_value(name,val,linea):
    global hashtable;
    global size;
    h=hasha(name);
    l=BucketListRec();
    l=hashtable[h];
    while((l!=None) and (name is not l.name)):
        l=l.sig;
    if(l==None): #Si no se encuentra en la tabla --> No esta declarada 
        errores.append("Error en linea "+str(linea)+" : "+"Variable no declarada"+"  "+name);
        #print("Error en linea "+str(linea)+" : "+"Variable no declarada"+"  "+name);
    else: #Si se encuentra en la tabla cambia el valor de la variable
        l.valor=val
        #if(name=="a"):
         #   print("..."+str(val))
 
#Funcion que retorna la posicion en memoria de la variable
#Si esta no se encuentra retorna un -1
def st_lookup(name):
    global hashtable;
    global size;
    h=hasha(name);
    l=BucketListRec();
    l=hashtable[h];
    while((l!=None) and (name is not l.name)):
        l=l.sig;
    if(l==None): #Si la variable no se encuentra en la tabla
        return -1;
    else: #Si la variable se encuentra en la tabla regresa la posicion en memoria
        return l.memloc;
 
#Funcion que imprime en un archivo txt la tabla de simbolos y su contenido
def printSymTab(listing):
    i=0
    listing.write("VariableName    Location       Value    Type    LineNumbers\n")
    listing.write("------------    --------       -----    ----    -----------\n")
    for i in range(0,size):
        if(hashtable[i]!=None):
            l=BucketListRec();
            l=hashtable[i];
            while(l!=None): #Va imprimiendo el contenido de la tabla
                t=LineListRec();
                t=l.lines;
                listing.write("\t"+str(l.name))
                listing.write("\t   "+str(l.memloc))
                listing.write("\t\t"+str(l.valor))
                listing.write("\t"+l.ttype)
                listing.write("\t"+str(t.linea))
                t=t.sig;
                while(t!=None): #imprime todas las lineas en donde se encuentra la variable
                    listing.write(" "+t.linea)
                    t=t.sig;
                listing.write("\n")
                l=l.sig;
 
#Funcion recursiva que hace el recorrido a traves del arbol ya sea preorden o postorden
#de acuerdo a como se le indique
def traverse(raiz,preproc=None,postproc=None):
    if(raiz!=None):
        if(postproc==None):
            preproc(raiz)
            i=0
            for i in range(len(raiz.hijos)):
                traverse(raiz.hijos[i],preproc,postproc)
        else:
            i=0
            for i in range(len(raiz.hijos)):
                traverse(raiz.hijos[i],preproc,postproc)
            postproc(raiz)
        traverse(raiz.hermano,preproc,postproc)
 
#Funcion que inserta valores en la tabla
def insertNode(t):
    global location
    #Caso sentencia
    if(t.categoria=="Sentencia"):
        if(t.tipo=="asignacion" or t.tipo=="sentcin"):
            if(st_lookup(t.contenido) != -1):
                st_insert(t.contenido,t.linea,0,t.value,"")
    #Caso expresion
    elif(t.categoria=="Expresion"):
        if(t.tipo=="identificador"):
            if(st_lookup(t.contenido) != -1):
                st_insert(t.contenido,t.linea,0,t.value,"")
    #Caso declaracion
    elif(t.categoria=="Declaracion"):
        #Caso variable entera
        if(t.tipo=="tipo" and t.contenido=="int"): 
            if(st_lookup(t.hijos[0].contenido) == -1):
                location+=1
                st_insert(t.hijos[0].contenido,t.linea,location,t.value,"int")
            else:
                typeError(t.hijos[0],"Variable ya declarada")
                t.hijos[0].type="int"
        #Caso variable real
        elif(t.tipo=="tipo" and t.contenido=="real"): 
            if(st_lookup(t.hijos[0].contenido) == -1):
                location+=1
                st_insert(t.hijos[0].contenido,t.linea,location,t.value,"real")
            else:
                typeError(t.hijos[0],"Variable ya declarada")
                t.hijos[0].type="real"
        #Caso variable booleana
        elif(t.tipo=="tipo" and t.contenido=="boolean"):
            if(st_lookup(t.hijos[0].contenido) == -1):
                location+=1
                st_insert(t.hijos[0].contenido,t.linea,location,t.value,"boolean")
            else:
                typeError(t.hijos[0],"Variable ya declarada")
                t.hijos[0].type="boolean"
        #Caso declaraciones en una misma linea
        #Va pasandole su tipo a sus hermanos
        elif(t.tipo=="variable"):
            if(t.hermano!=None):
                if(st_lookup(t.hermano.contenido) == -1):
                    location+=1
                    st_insert(t.hermano.contenido,t.linea,location,t.value,t.type)
                else:
                    typeError(t.hermano,"Variable ya declarada")
                    t.hermano.valor="Error"
 
#Funcion que construye la tabla de simbolos recorriendo el arbol en preorden
def buildSymtab(t):
    traverse(t,insertNode,None)
 
#Funcion que recibe un nodo y un mensaje de error y lo imprime en el archivo de errores
def typeError(t,mensaje):
    errores.append("Error en linea "+t.linea+" : "+mensaje+"  "+t.contenido);
    #print("Error en linea "+t.linea+" : "+mensaje+"  "+t.contenido);
 
#Funcion que pasa todos los tipos en el arbol
def pasaTipo(t):
    if(t!=None):
        if(t.categoria=="Declaracion"):
            if(t.tipo=="tipo"):
                t.type=t.contenido
                t.hijos[0].type=t.contenido
            elif(t.tipo=="variable"):
                if(t.hermano!=None):
                    t.hermano.type=t.type
                     
 
#Funcion que retorna el tipo de dato de la variable
#Si esta no se encuentra retorna un -1
def checkType(name):
    global hashtable;
    global size;
    h=hasha(name);
    l=BucketListRec();
    l=hashtable[h];
    while((l!=None) and (name is not l.name)):
        l=l.sig;
    if(l==None): #No se encuentra en la tabla hash
        return -1;
    else: #Retorna el tipo de dato de la variable
        return l.ttype;
 
#Funcion que checa que la variable este en la tabla de simbolos
#y retorna su valor, si no la encuentra retorna un -1
def checkValue(name):
    global hashtable;
    global size;
    h=hasha(name);
    l=BucketListRec();
    l=hashtable[h];
    while((l!=None) and (name is not l.name)):
        l=l.sig;
    if(l==None): #La variable no se encuentra en la tabla hash
        return -1;
    else: #Retorna el valor de la variable
        return l.valor;
 
#Funcion que hace todo el paso de tipos, de valores y chequeo de tipos
#en el arbol de analisis sintactico
def semantic(t):
    if(t!=None):
        #Pasa tipo a numeros
        if(t.tipo=="numero"):
            t.type="int"
            t.value=int(t.contenido)
        #Pasa tipo a reales
        if(t.tipo=="flotante"):
            t.type="real"
            t.value=float(t.contenido)
        #Si es una signacion o un identificador busca su tipo de dato en la tabla
        #y se lo asigna
        if(t.tipo=="asignacion" or t.tipo=="identificador"):
            if(st_lookup(t.contenido) != -1):
                t.type=checkType(t.contenido)
            else: #Caso variable no declarada
                typeError(t,"Variable no declarada")
                t.value="Error"
        #Asigna valores a las variables ya declaradas
        if(t.tipo=="identificador"):
            t.value=checkValue(t.contenido)
             
        #Caso expresion
        if(t.categoria=="Expresion"):
            if(t.tipo=="operador"):
                #Caso operadores ( +, -, *, /)
                if(t.contenido=="+" or t.contenido=="-" or t.contenido=="*" or t.contenido=="/"):
                    semantic(t.hijos[0])
                    semantic(t.hijos[1])
 
                    #Pasa el tipo al operador segun el tipo de sus hijos
                    if(t.hijos[0].type=="int" and t.hijos[1].type=="int"):
                        t.type="int"
                    elif(t.hijos[0].type=="real" and t.hijos[1].type=="int"):
                        t.type="real"
                    elif(t.hijos[0].type=="int" and t.hijos[1].type=="real"):
                        t.type="real"
                    elif(t.hijos[0].type=="real" and t.hijos[1].type=="real"):
                        t.type="real"
                    
                    #else:
                     #   typeError(t,"Los tipos de dato no coinciden")
                      #  t.type="Error"
 
                    #Realiza operaciones de +, -, * y / y le asigna el valor al operador
                    if(t.hijos[0].value!="Error" and t.hijos[1].value!="Error"):
                        if(t.hijos[0].value != None and t.hijos[1].value != None):
                            if(t.contenido=="+"): #Caso suma
                                t.value = t.hijos[0].value + t.hijos[1].value
                            elif(t.contenido=="-"): #Caso resta
                                t.value = t.hijos[0].value - t.hijos[1].value
                            elif(t.contenido=="*"): #Caso multiplicacion
                                t.value = t.hijos[0].value * t.hijos[1].value
                            elif(t.contenido=="/"): #Caso division
                                if(t.hijos[1].value==0): #Caso division entre 0
                                    typeError(t.hijos[1],"Division entre 0")
                                else:
                                    t.value = t.hijos[0].value / t.hijos[1].value
                            #Caso resultado flotante y variable entera se castea
                            """
                            if(t.type=="int"):
                                t.value = int(t.value)
                            else:
                                t.value = float(t.value)"""
                        #Caso error, los hijos del operador no tienen un valor asignado
                        else:
                            if(t.hijos[0].value==None):
                                typeError(t.hijos[0],"No se ha asignado previamente valor a la variable ")
                            else:
                                typeError(t.hijos[1],"No se ha asignado previamente valor a la variable ")
                            t.value="Error"
                    else:
                        t.value="Error" #Caso los hijos son un error
                         
                #Caso operadores ( <, >, <=, >=, !=, ==)
                elif(t.contenido=="<" or t.contenido=="<=" or t.contenido=="==" or t.contenido=="!=" or t.contenido==">=" or t.contenido==">"):
                    semantic(t.hijos[0])
                    semantic(t.hijos[1])
                    t.type="boolean" #Le asigna tipo de dato boolean al operador
                    #Hace las respectivas comparaciones entre los hijos del operador
                    if(t.hijos[0].value!="Error" and t.hijos[1].value!="Error"):
                        if(t.contenido=="<"): #Caso menor que
                            t.value = t.hijos[0].value < t.hijos[1].value
                        elif(t.contenido=="<="): #Caso menor o igual que 
                            t.value = t.hijos[0].value <= t.hijos[1].value
                        elif(t.contenido=="=="): #Caso igual que
                            t.value = t.hijos[0].value == t.hijos[1].value
                        elif(t.contenido=="!="): #Caso diferente que
                            t.value = t.hijos[0].value != t.hijos[1].value
                        elif(t.contenido==">="): #Caso mayor o igual que
                            t.value = t.hijos[0].value >= t.hijos[1].value
                        elif(t.contenido==">"): #Caso mayor que
                            t.value = t.hijos[0].value > t.hijos[1].value
                    #Caso en que los hijos no tienen un valor asignado
                    elif(t.hijos[0].value!=None and t.hijos[1].value!=None):
                        typeError(t,"No se ha asignado valor a una variable")
                        t.value="Error"
                    else:
                        typeError(t,"No se puede comparar un valor")
                        t.value="Error"
 
        #Caso asignacion
        if(t.tipo=="asignacion"):
            if(t.type=="real" and t.hijos[0].type=="int"):
                if(t.hijos[0].value!="Error"): 
                    t.value=float(t.hijos[0].value)
                    st_value(t.contenido,t.value,t.linea)
                 
            elif(t.value !="Error" and t.hijos[0].value!="Error"):
                if(t.type!=t.hijos[0].type):
                    typeError(t,"No se puede asignar un tipo de dato distinto")
                else:
                    t.value = t.hijos[0].value
                    st_value(t.contenido,t.value,t.linea)
 
#Funcion que imprime el arbol en el archivo 
def imprime(arbol,tabs):
    if(arbol != None):
        arbol.tabs = tabs
        texto = ""
        for i in range(tabs):
            texto+="\t"
        if(arbol.type==None): #Caso tipos None
            arbol.type="_"
        if(arbol.value==None): #Caso valores None
            arbol.value="_"
        print( texto + " " + arbol.contenido+".."+arbol.type+".."+str(arbol.value))
        outfile = open('MuestraSemantico.txt', 'a')
        outfile.write( texto + " " + arbol.contenido+" ["+arbol.type+"] ["+str(arbol.value)+ "]\n")
        outfile.close()
        for i in range (len(arbol.hijos)):
            imprime(arbol.hijos[i],tabs+1)
        imprime(arbol.hermano,tabs)
 
def semantica():
    global hashtable
    #Funciones a realizar
    arbol=sintaxis() #Recupera el arbol del sintactico
    traverse(arbol,pasaTipo,None) #Hace el recorrido preorden pasando los tipos
    buildSymtab(arbol) #Construye la tabla de simbolos
    traverse(arbol,None,semantic) #Hace el recorrido postorden haciendo las operaciones y recuperando errores
    return arbol,hashtable
 
def archivos_errores():
    global hashtable
    arbol,hashtable=semantica()
    #Abre el archivo de la tabla hash, la imprime y lo cierra
    listing=open('hashtable.txt','w')
    listing.write("\nSymbol table:\n\n")
    printSymTab(listing);
    listing.close()
     
    #Crea el archivo con el arbol que se mostrara en el ide
    outfile2 = open('MuestraSemantico.txt', 'w')
 
    #Cre el archivo de errores 
    outfile = open('Errores.txt', 'a')
    outfile.write("\n\n\tERRORES SEMANTICO\n\n")
 
    #Imprime los errores en el archivo
    for i in range(0,len(errores)):
        outfile.write(errores[i]+"\n")
 
    outfile.close()
    print(type(arbol))
    imprime(arbol,0) #imprime el arbol en el archivo
     
    outfile2.close()
 
    #imprime los errores en consola
    for i in errores:
        print("["+i+"]")
 
 
#PRINCIPAL
from sintactico import sintaxis
 
#Variables globales
global actual
actual=0
errores=[]
global location
location=0
global size #Variable que guarda el tamanio de la tabla hash 
size=211
global shift #Variable usada como multiplicador de la funcion hash
shift=4
global hashtable #Tabla hash
hashtable=[]
hashtable=[None]*size
global arbol
arbol = Nodo()
