from ast import Assign, expr
from sly import Lexer, Parser
import os

#Analizador léxico
class CalcLexer(Lexer):
    tokens = { ID, STRING, NUMBER, IF, ELSE, SPRINT, 
                STR, INT, EQ, ASSIGN_VAR, TRUE, FALSE, 
                EQ, ME, LE, DF, M, L, REPEAT }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', ':' }

    #Strings
    STRING = r'"[a-zA-Z0-9\s_]*"'

    #Identificadores
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    #Palabras reservadas
    ID['IF'] = IF
    ID['ELSE'] = ELSE
    ID['REPEAT'] = REPEAT
    ID['SPRINT'] = SPRINT
    ID['STR'] = STR
    ID['INT'] = INT
    ID['True'] = TRUE
    ID['False'] = FALSE

    #Igualar
    EQ = r'=='
    ME = r'>='
    LE = r'<='
    DF = r'!='
    M = r'>'
    L = r'<'

    #Asignar una variable
    ASSIGN_VAR = r':='

    #Numeros
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("\033[91mCaracter ilegal '%s'" % t.value[0]+"\033[0m")
        self.index += 1

#Analizador Sintáctico
class CalcParser(Parser):
    tokens = CalcLexer.tokens
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.names = { }
        self.FAIL = '\033[91m' #RED
        self.RESET = '\033[0m' #RESET COLOR
        self.GREEN = '\033[92m'

    #Bucle repeat
    @_('REPEAT expr ":" expr')
    def statement(self, p):
        if type(p.expr0) == int:
            if p.expr0 >= 1:
                try:
                    ST = p.expr1
                    for _ in range(p.expr0):
                        print(self.GREEN+ST+self.RESET) if p.expr1 != None else ""
                except:
                    print(self.FAIL+"Ha ocurrido un error de sintaxis."+self.RESET)
            else:
                print(self.FAIL+"El número de repeticiones debe ser igual o mayor a 1."+self.RESET)
        else:
            print(self.FAIL+"Error de tipo: dede ser de tipo numerico."+self.RESET)

    #Asignar una variable al diccionario de variables
    @_('ID ASSIGN_VAR expr')
    def statement(self, p):
        try:
            self.names[p.ID] = p.expr
        except:
            print(self.FAIL+"Error de sintaxis: Ha ocurrido un error")
            print("En la asiganación de la variable."+self.RESET)

    #Asignar una variable dentro de un IF o ELSE
    @_('ID "=" expr')
    def statement(self, p):
        try:
            if p.ID in self.names.keys():
                return (p.ID, p.expr)
            else:
                print(self.FAIL+"Error de asignación. Utilice ':='"+self.RESET)
        except:
            print(self.FAIL+"Ha ocurrido un error en la asignación."+self.RESET)

    @_('expr')
    def statement(self, p):
        if p.expr != None:
            print(self.GREEN+str(p.expr)+self.RESET)

    #SUMA
    @_('expr "+" expr')
    def expr(self, p):
        try:
            return p.expr0 + p.expr1
        except:
            print(self.FAIL+"Ha ocurrido un error en la suma."+self.RESET)

    #RESTA
    @_('expr "-" expr')
    def expr(self, p):
        try:
            return p.expr0 - p.expr1
        except:
            print(self.FAIL+"Ha ocurrido un error en la resta."+self.RESET)

    #MULTIPLICACIÓN
    @_('expr "*" expr')
    def expr(self, p):
        try:
            return p.expr0 * p.expr1
        except:
            print(self.FAIL+"Ha ocurrido un error en la multiplicación."+self.RESET)

    #DIVISIÓN
    @_('expr "/" expr')
    def expr(self, p):
        try:
            return p.expr0 / p.expr1
        except ZeroDivisionError:
            print(self.FAIL+"No es posible dividir entre 0."+self.RESET)
        except:
            print(self.FAIL+"Ha ocurrido un error de sintaxis."+self.RESET)

    #NUMEROS NEGATIVOS   
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        if str(p.expr).isnumeric():
            return -p.expr
        else:
            print(self.FAIL+"Error de tipo: ")
            print("Debe ser de tipo numerico."+self.RESET)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    #CADENAS
    @_('STRING')
    def expr(self, p):
        try:
            String = p.STRING.strip('"')
            return String
        except:
            print(self.FAIL+"Ha ocurrido un error con "+p.STRING + self.RESET)

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('TRUE')
    def expr(self, p):
        return True
    
    @_('FALSE')
    def expr(self, p):
        return False

    #CONDICIÓN IGUAL
    @_('expr EQ expr')
    def condition(self, p):
        try:
            return True if p.expr0 == p.expr1 else False
        except:
            print(self.FAIL+"Error: condición invalida."+self.RESET)

    #CONDICIÓN MAYOR O IGUAL
    @_('expr ME expr')
    def condition(self, p):
        try:
            return True if p.expr0 >= p.expr1 else False
        except:
            print(self.FAIL+"Error: condición invalida."+self.RESET)

    #CONDICIÓN MENOR O IGUAL
    @_('expr LE expr')
    def condition(self, p):
        try:
            return True if p.expr0 <= p.expr1 else False
        except:
            print(self.FAIL+"Error: condición invalida."+self.RESET)
    
    #CONDICIÓN DIFERENTE
    @_('expr DF expr')
    def condition(self, p):
        try:
            return True if p.expr0 != p.expr1 else False
        except:
            print(self.FAIL+"Error: condición invalida."+self.RESET)

    #CONDICIÓN MAYOR QUE
    @_('expr M expr')
    def condition(self, p):
        try:
            return True if p.expr0 > p.expr1 else False
        except:
            print(self.FAIL+"Error: condición invalida."+self.RESET)
    
    #CONDICIÓN MENOR QUE
    @_('expr L expr')
    def condition(self, p):
        try:
            return True if p.expr0 < p.expr1 else False
        except:
            print(self.FAIL+"Error: condición invalida."+self.RESET)

    #CONDICIONAL IF Y ELSE
    @_('IF condition ":" statement ELSE ":" statement')
    def statement(self, p):
        try:
            if p.condition:
                self.names[p.statement0[0]] = p.statement0[1]
            else:
                self.names[p.statement1[0]] = p.statement1[1]
        except:
            print(self.FAIL+"Error de sintaxis en la condicional IF."+self.RESET)

    @_('IF condition ":" statement ELSE statement',
       'IF condition statement ELSE ":" statement',
       'IF condition statement')
    def statement(self, p):
        print(self.FAIL+"Error de sintaxis en la condicional IF. Falto ':'"+self.RESET)

    #CONDICIONAL IF
    @_('IF condition ":" statement')
    def statement(self, p):
        try:
            if p.condition:
                self.names[p.statement[0]] = p.statement[1]
        except:
            print(self.FAIL+"Error de sintaxis. En la condicional IF."+self.RESET)

    #IMPRIMIR
    @_('SPRINT "(" expr ")"')
    def expr(self, p):
        try:
            return p.expr
        except:
            print(self.FAIL+"Ha ocurrido un error en la expresión."+self.RESET)
    
    @_('STR')
    def expr(self, p):
        return p.STR
    
    @_('INT')
    def expr(self, p):
        return p.INT

    #RETORNAR VALOR DE UNA VARIABLE
    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            print(self.FAIL+"Identificador indefinido '%s'" % p.ID+self.RESET)
            return 0

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    os.system('cls')
    line_count = 1
    def encabezado():
        print('\t\t\t'+'\033[93m'+"*********** SL (Simple Language) ***********")
        print('\t\t\t'+"   *********** Versión: 1.0.3 ***********"+'\033[0m')
    encabezado()
    while True:
        try:
            text = input('Line '+str(line_count) + '> ')
            if 'clear' in text:
                clear = lambda: os.system('cls')
                clear()
                text = ""
                encabezado()
                line_count = 0
            line_count += 1 
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))