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


def genStmt(t):
    global ac
    global gp
    global loc
    savedLoc1=0
    savedLoc2=0
    currentLoc=0
    bandera=True
    p1=Nodo()
    p2=Nodo()
    p3=Nodo()
    if(t.tipo == "seleccion"):
        """
        p1=t.hijos[0].hijos[0]
        p2=t.hijos[1].hijos[0]
        cGen(p1)
        savedLoc1 = emitSkip(1)
        #emitComment("if: jump to else belongs here")
        #recurse on then part
        cGen(p2)
        savedLoc2 = emitSkip(1)
        #emitComment("if: jump to end belongs here")
        currentLoc = emitSkip(0)
        emitBackup(savedLoc1)
        emitRM_Abs("JEQ",ac,currentLoc," ")
        emitRestore()
        #recurse on else part
        if(len(t.hijos) == 3):
            p3=t.hijos[2].hijos[0]
            cGen(p3)
            currentLoc = emitSkip(0)
            emitBackup(savedLoc2)
            emitRM_Abs("LDA",pc,currentLoc," ")
            emitRestore()"""
        if(len(t.hijos)==3):
            p1=t.hijos[0].hijos[0]
            p2=t.hijos[1].hijos[0]
            p3=t.hijos[2].hijos[0]
            cGen(p1)
            savedLoc1=emitSkip(1)
            cGen(p2)
            savedLoc2=emitSkip(1)
            currentLoc=emitSkip(0)
            emitBackup(savedLoc1)
            emitRM_Abs("JEQ",ac,currentLoc," ")
            emitRestore()
            cGen(p3)
            currentLoc = emitSkip(0)
            emitBackup(savedLoc2)
            emitRM_Abs("LDA",pc,currentLoc," ")
            emitRestore()
        elif(len(t.hijos)==2):
            p1=t.hijos[0].hijos[0]
            p2=t.hijos[1].hijos[0]
            cGen(p1)
            savedLoc1=emitSkip(1)
            cGen(p2)
            currentLoc=emitSkip(0)
            emitBackup(savedLoc1)
            emitRM_Abs("JEQ",ac,currentLoc," ")
            emitRestore()
            
    elif(t.tipo == "iteracion"):
        p1=t.hijos[0]
        p2=t.hijos[1]
        savedLoc1=emitSkip(0)
        cGen(p1)
        savedLoc2=emitSkip(1)
        cGen(p2)
        currentLoc=emitSkip(0)
        emitBackup(savedLoc2)
        emitRM_Abs("JEQ",ac,currentLoc+1,"while: jump back to body")
        emitRestore()
        emitRM_Abs("LDA",pc,savedLoc1,"")
    elif(t.tipo == "repeticion"):
        p1=t.hijos[0].hijos[0]
        p2=t.hijos[1].hijos[0]
        savedLoc1 = emitSkip(0)
        #emitComment("repeat: jump after body comes back here")
        #generate code for body
        cGen(p1)
        #generate code for test
        cGen(p2)
        emitRM_Abs("JNE",ac,savedLoc1,"repeat: jmp back to body")
        
    elif(t.tipo == "asignacion"):
        #generate code for rhs
        cGen(t.hijos[0])
        #now store value
        loc=st_lookup(t.contenido)
        emitRM("ST",ac,loc,gp,"assign: store value")
    elif(t.tipo == "sentcin"):
        emitRO("IN",ac,0,0,"read: integer value")
        loc = st_lookup(t.hijos[0].contenido)
        emitRM("ST",ac,loc,gp,"read: store value")
    elif(t.tipo == "sentcout"):
        #generate code for expression to write
        cGen(t.hijos[0])
        #now output it
        emitRO("OUT",ac,0,0,"write ac")

def genExp(t):
    global loc
    global tmpOffset
    global mp
    p1 = Nodo()
    p2 = Nodo()
    if(t.tipo == "numero"):
        #gen code to load integer constant using LDC
        emitRM("LDC",ac,t.contenido,0,"load const")
    elif(t.tipo == "flotante"):
        emitRM("LDC",ac,t.contenido,0,"load float")
    elif(t.tipo == "identificador"):
        loc = st_lookup(t.contenido)
        emitRM("LD",ac,loc,gp,"load id value")
    elif(t.tipo == "operador"):
        p1=t.hijos[0]
        p2=t.hijos[1]
        #gen code for ac = left arg
        cGen(p1)
        #Gen code to push left operand
        
        emitRM("ST",ac,tmpOffset,mp,"op: push left")
        tmpOffset=tmpOffset - 1
        #gen code for ac = right operand
        cGen(p2)
        #now load left operand
        tmpOffset=tmpOffset + 1
        emitRM("LD",ac1,(tmpOffset),mp,"op: load left")
        
        if(t.contenido == "+"):
            emitRO("ADD",ac,ac1,ac,"op +")
        elif(t.contenido == "-"):
            emitRO("SUB",ac,ac1,ac,"op -")
        elif(t.contenido == "*"):
            emitRO("MUL",ac,ac1,ac,"op *")
        elif(t.contenido == "/"):
            emitRO("DIV",ac,ac1,ac,"op /")
        elif(t.contenido == "<"):
            emitRO("SUB",ac,ac1,ac,"op <")
            emitRM("JLT",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")
        elif(t.contenido == "=="):
            emitRO("SUB",ac,ac1,ac,"op == ")
            emitRM("JEQ",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")
        elif(t.contenido == "!="):
            emitRO("SUB",ac,ac1,ac,"op != ")
            emitRM("JNE",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")
        elif(t.contenido == "<="):
            emitRO("SUB",ac,ac1,ac,"op <= ")
            emitRM("JLE",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")
        elif(t.contenido == ">="):
            emitRO("SUB",ac,ac1,ac,"op >= ")
            emitRM("JGE",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")
        elif(t.contenido == ">"):
            emitRO("SUB",ac,ac1,ac,"op > ")
            emitRM("JGT",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")
        else:
            emitComment("BUG: Unknown operator")

def cGen(t):
    #if(t!=None):
        #outfile.write("__"+t.contenido+"\n")
    global aux
    if(t != None):
        #print(t.categoria+"==="+t.contenido+"=="+str(t.tabuladores))
        if(t.categoria == "Sentencia"):
            genStmt(t)
            cGen(t.hermano)
        elif(t.categoria == "Expresion"):
            genExp(t)
            cGen(t.hermano)
        elif((t.categoria == None or t.categoria == "_")and t.contenido=="main"):
            cGen(t.hijos[1])
        
        

def codeGen(t):
    global mp
    global ac
    #emitComment("File: code.txt")
    #emitComment("Standard prelude")
    #emitRM("LD",mp,0,ac,"load maxaddress from location 0 ")
    #emitRM("ST",ac,0,ac,"clear location 0")
    #emitComment("End of standard prelude")
    imprime(t,0) ##NO BORRAR
    cGen(t)
    #emitComment("End of execution")
    emitRO("HALT",0,0,0,"")
    

#Funciones extras
#def emitComment(c):
 #   if(tracecode == True):
  #      outfile.write("\n")

"""/* Procedure emitRO emits a register-only
 * TM instruction
 * op = the opcode
 * r = target register
 * s = 1st source register
 * t = 2nd source register
 * c = a comment to be printed if TraceCode is True
 */"""
def emitRO(op,r,s,t,c):
    global emitLoc
    global highEmitLoc
    outfile.write(str(emitLoc)+": "+op+" "+str(r)+","+str(s)+","+str(t));
    outfile2.write(str(emitLoc)+"\t"+op+"\t"+str(r)+"\t"+str(s)+"\t"+str(t));
    emitLoc+=1
    outfile.write("\n")
    outfile2.write("\n")
    if(highEmitLoc < emitLoc):
        highEmitLoc = emitLoc

"""/* Procedure emitRM emits a register-to-memory
 * TM instruction
 * op = the opcode
 * r = target register
 * d = the offset
 * s = the base register
 * c = a comment to be printed if TraceCode is True
 */"""
def emitRM(op,r,d,s,c):
    global emitLoc
    global highEmitLoc
    outfile.write(str(emitLoc)+": "+op+" "+str(r)+","+str(d)+"("+str(s)+")")
    outfile2.write(str(emitLoc)+"\t"+op+"\t"+str(r)+"\t"+str(d)+"\t"+str(s))
    emitLoc+=1
    outfile.write("\n")
    outfile2.write("\n")
    if(highEmitLoc < emitLoc):
        highEmitLoc = emitLoc

"""/* Function emitSkip skips "howMany" code
 * locations for later backpatch. It also
 * returns the current code position
 */"""
def emitSkip(howMany):
    global emitLoc
    global highEmitLoc
    i=emitLoc
    emitLoc += howMany
    if(highEmitLoc < emitLoc):
        highEmitLoc = emitLoc
    return i

"""/* Procedure emitBackup backs up to 
 * loc = a previously skipped location
 */"""
def emitBackup(loc):
    global emitLoc
    global highEmitLoc
    #if(loc > highEmitLoc):
        #emitComment("BUG in emitBackup");
    emitLoc=loc

"""/* Procedure emitRestore restores the current 
 * code position to the highest previously
 * unemitted position
 */"""
def emitRestore():
    global emitLoc
    global highEmitLoc
    emitLoc = highEmitLoc

"""/* Procedure emitRM_Abs converts an absolute reference 
 * to a pc-relative reference when emitting a
 * register-to-memory TM instruction
 * op = the opcode
 * r = target register
 * a = the absolute location in memory
 * c = a comment to be printed if TraceCode is True
 */"""

def emitRM_Abs(op,r,a,c):
    global emitLoc
    global highEmitLoc
    global pc
    aux1=(a-(emitLoc+1))
    outfile.write(str(emitLoc)+": "+op+" "+str(r)+","+str(aux1)+"("+str(pc)+")")
    outfile2.write(str(emitLoc)+"\t"+op+"\t"+str(r)+"\t"+str(aux1)+"\t"+str(pc))
    emitLoc+=1
    outfile.write("\n")
    outfile2.write("\n")
    if(highEmitLoc < emitLoc):
        highEmitLoc = emitLoc

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

#Funcion que imprime el arbol 
def imprime(arbol,tabs):
    if(arbol != None):
        arbol.tabuladores = tabs
        texto = ""
        for i in range(tabs):
            texto+=" "
        if(arbol.type==None): #Caso tipos None
            arbol.type="_"
        if(arbol.value==None): #Caso valores None
            arbol.value="_"
        if(arbol.tipo==None): #Caso valores None
            arbol.tipo="_"
        if(arbol.categoria==None): #Caso valores None
            arbol.categoria="_"    
        print( texto + " " + arbol.contenido+".."+arbol.categoria+".."+arbol.tipo)
        for i in range (len(arbol.hijos)):
            imprime(arbol.hijos[i],tabs+1)
        imprime(arbol.hermano,tabs)

#Funcion que imprime en un archivo txt la tabla de simbolos y su contenido
def printSymTab(listing):
    i=0
    #print("VariableName    Location       Value    Type    LineNumbers\n")
    #print("------------    --------       -----    ----    -----------\n")
    for i in range(0,size):
        if(hashtable[i]!=None):
            l=BucketListRec();
            l=hashtable[i];
            while(l!=None): #Va imprimiendo el contenido de la tabla
                t=LineListRec();
                t=l.lines;
                #print("\t"+str(l.name))
                #print("\t   "+str(l.memloc))
                #print("\t\t"+str(l.valor))
                #print("\t"+l.ttype)
                #print("\t"+str(t.linea))
                t=t.sig;
                while(t!=None): #imprime todas las lineas en donde se encuentra la variable
                    #print(" "+t.linea)
                    t=t.sig;
                #print("\n")
                l=l.sig;

#funcion hash
def hasha(key):
    global size;
    global shift;
    temp=0;
    for i in key :
        temp=((temp << shift) + ord(i)) %size;
    return temp

#PRINCIPAL
from semantico import semantica
global hashtable
hashtable=[]
arbol,hashtable=semantica()
global tmpOffset
tmpOffset=0
global tracecode
tracecode=True
global emitLoc
emitLoc=0
global highEmitLoc
highEmitLoc=0
global pc
pc=7
global ac
ac=0
global size
size=211
global shift #Variable usada como multiplicador de la funcion hash
shift=4
global gp
gp=5
global loc
loc=0
global mp
mp=6
global ac1
ac1=1
global aux
aux=Nodo()

printSymTab(hashtable)

outfile = open('code.txt','w')
outfile2 = open('code2.txt','w')
print(arbol)
codeGen(arbol)
outfile.close()
outfile2.close()
#imprime(arbol,0)
