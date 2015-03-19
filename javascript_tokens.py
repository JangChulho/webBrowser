import ply.lex as lex

tokens = ("ANDAND",     # &&
          "COMMA",      # ,
          "DIVIDE",     # /
          "ELSE",       # else
          "EQUAL",      # =
          "EQUALEQUAL", # ==
          "FALSE",      # false
          "FUNCTION",   # function
          "GE",         # >=
          "GT",         # >
          "IDENTIFIER", # i
          "IF",         # if
          "LBRACE",     # {
          "LE",         # <=
          "LPAREN",     # (
          "LT",         # <
          "MINUS",      # -
          "NOT",        # !
          "NUMBER",     # 123
          "OROR",       # ||
          "PLUS",       # +
          "RBRACE",     # }
          "RETURN",     # return
          "RPAREN",     # )
          "SEMICOLON",  # ;
          "STRING",     # "hello"
          "TIMES",      # *
          "TRUE",       # true
          "VAR",        # var
          "WHILE",      # while
          "MOD",        # %
)

states = (
        ('jscomment', 'exclusive'),
)

def t_jscomment(t):
    r'\/\*'
    t.lexer.begin('jscomment')

def t_jscomment_end(t):
    r'\*\/'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    pass

def t_jscomment_error(t):
    t.lexer.skip(1)

def t_NUMBER(t):
    r'-?[0-9]+(?:\.[0-9]*)?'
    t.value = float(t.value)
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_IF(t):
    r'if'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_VAR(t):
    r'var'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_STRING(t):
    r'(?:"[^"]*"|\'[^\']*\')'    
    t.value = t.value[1:-1]    
    return t

t_ANDAND        = r'&&'
t_COMMA         = r','
t_DIVIDE        = r'/'
t_EQUALEQUAL    = r'=='
t_EQUAL         = r'='
t_GE            = r'>='
t_GT            = r'>'
t_IDENTIFIER    = r'[A-Za-z][A-Za-z_]*'
t_LBRACE        = r'\{'
t_LE            = r'<='
t_LPAREN        = r'\('
t_LT            = r'<'
t_MINUS         = r'-'
t_NOT           = r'!'
t_OROR          = r'\|\|'
t_PLUS          = r'\+'
t_RBRACE        = r'\}'
t_RPAREN        = r'\)'
t_SEMICOLON     = r';'
t_TIMES         = r'\*'
t_MOD           = r'%'

t_ignore             = ' \t\v\r'        # shortcut for whitespace
t_jscomment_ignore   = ' \t\v\r'        # shortcut for whitespace

def t_newline(t):    
    r'\n'
    t.lexer.lineno += 1
    pass

def t_error(t):
    print ("Lexical Error : ", "LineNo = ", t.lineno, ", Value = ", t.value)
    t.lexer.skip(1)
    
"""
def find_column(input,token):
    i = token.lexpos
    while i > 0:
        if input[i] == '\n': break
        i -= 1
    column = (token.lexpos - i)+1
    return column


jslexer = lex.lex()
jslexer.input(exdata)
while True:
    tok = jslexer.token()    
    if not tok: break
    print(tok)
"""
