import ply.lex as lex

tokens = ("LANGLE",         # <
          "LANGLESLASH",    # </
          "RANGLE",         # >
          "SLASHRANGLE",    # />
          "EQUAL",          # =
          "STRING",         # "144"
          "WORD",           # 'Welcome' in "Welcome to my webpage."
          "JAVASCRIPT",     # var a = 1
)

states = (        
        ('htmlcomment', 'exclusive'),   # <!--
        ('javascript', 'exclusive'),    # <script type="text/javascript">
)

def t_htmlcomment(t):
    r'<!--'
    t.lexer.begin('htmlcomment')

def t_htmlcomment_end(t):
    r'-->'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    pass

def t_htmlcomment_error(t):
    t.lexer.skip(1)

def t_javascript(t):
    r'\<script\ type\ *=\ *\"text\/javascript\"\>'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin('javascript')

def t_javascript_end(t):
    r'</script>'
    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-9]
    t.type = "JAVASCRIPT"
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    return t
    
def t_javascript_error(t):
    t.lexer.skip(1)

def t_SLASHRANGLE(t):
    r'/>'
    return t

def t_STRING(t):
    r'(?:"[^"]*"|\'[^\']*\')'    
    t.value = t.value[1:-1]
    return t

def t_WORD(t):
    r'[^ <>\n=]+'    
    return t

t_LANGLESLASH = r'</'
t_LANGLE = r'<'
t_RANGLE = r'>'
t_EQUAL = r'='

t_ignore             = ' \t\v\r'        # shortcut for whitespace
t_htmlcomment_ignore = ' \t\v\r'        # shortcut for whitespace
t_javascript_ignore  = ' \t\v\r'        # shortcut for whitespace

def t_newline(t):    
    r'\n'
    t.lexer.lineno += 1
    pass

def t_error(t):
    print ("Lexical Error : ", "LineNo = ", t.lineno, ", Value = ", t.value)
    t.lexer.skip(1)

"""
def find_column(input,token):
    if token == None:
        return
    lc = input.rfind('\n',0,token.lexpos)+1        
    if lc < 1:        
        lc = 0
    column = (token.lexpos - lc) + 1
    return column


#exdata = all <b> 'aaa' <script type  =  "text/javascript">write(a<b);</script>
#aaa aaa

htmllexer = lex.lex()
htmllexer.input(exdata)
while True:
    tok = htmllexer.token()
    find_column(exdata, tok)    
    if not tok: break
    print(tok)
"""
