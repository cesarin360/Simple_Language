from sly import Lexer, Parser

#Análizador Léxico
class CalcLexer(Lexer):
    tokens = { ID, NUMBER, NAME1, NAME2, APELL, CARNE }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')' }

    #IDENTIFICADORES
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    #PALABRAS RESERVADAS
    ID['CESAR'] = NAME1
    ID['JOSUE'] = NAME2
    ID['GARCIA'] = APELL
    CARNE = r'0905\-18\-13296'

    #NUMEROS
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        try:
            print("\033[91mError léxico en '%s'" % t.value[0]+'\033[0m')
            self.index += 1
        except:
            pass

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
        self.OK = '\033[92m' #GREEN

    #IGUALAR VARIABLE
    @_('ID "=" expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr) if p.expr != None else "" 

    #SUMA
    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    #RESTA
    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    #MULTIPLICACIÓN
    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    #DIVISIÓN
    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    #NUMERO NEGATIVO
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    #IMPRIME PRIMER NOMBRE
    @_('NAME1')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return p.NAME1

    #IMPRIME PRIMER NOMBRE, SEGUNDO NOMBRE Y APELLIDO
    @_('NAME1 NAME2 APELL')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return p.NAME1+' '+p.NAME2+' '+p.APELL
    
    #IMPRIME PRIMER NOMBRE Y SEGUNDO NOMBRE
    @_('NAME1 NAME2')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return p.NAME1+' '+p.NAME2

    #IMPRIME PRIMER NOMBRE Y APELLIDO
    @_('NAME1 APELL')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return p.NAME1+' '+p.APELL

    #IMPRIME SEGUNDO NOMBRE
    @_('NAME2')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return p.NAME2

    #IMPRIME APELLIDO
    @_('APELL')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return  p.APELL

    #IMPRIME CARNÉ
    @_('CARNE')
    def expr(self, p):
        print(self.OK+"La expresión es válida"+self.RESET)
        print(self.OK+"Análisis Léxico Exitoso"+self.RESET)
        return  p.CARNE

    #RETORNA NÚMERO
    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    #RETORNA VARIABLE
    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            print(self.FAIL+"La expresión es inválida '%s'" % p.ID+self.RESET)
            return 

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    count = 1


    while True:
        try:
            text = input('Linea '+str(count)+'> ')
            count += 1
        except EOFError:
            break
        if text:
            try:
                parser.parse(lexer.tokenize(text))
            except:
                print("Error de sintaxis.")
