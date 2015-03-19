import html_tokens
import ply.lex as lex
import ply.yacc as yacc

tokens = ("LANGLE",         # <
          "LANGLESLASH",    # </
          "RANGLE",         # >
          "SLASHRANGLE",    # />
          "EQUAL",          # =
          "STRING",         # "144"
          "WORD",           # 'Welcome' in "Welcome to my webpage."
          "JAVASCRIPT",     # var a = 1
)

start = 'html'

def p_html(p):
    'html : element html'
    p[0] = [p[1]] + p[2]

def p_html_empty(p):
    'html : '
    p[0] = [ ]

def p_element_word(p):
    'element : WORD'
    p[0] = ('word-element',p[1])

def p_element_word_string(p):
    'element : STRING'
    p[0] = ('word-element',p[1])
        
def p_element_tag(p):
    'element : LANGLE tagname tagarguments RANGLE html LANGLESLASH tagnameend RANGLE'
    p[0] = ('tag-element',p[2],p[3],p[5],p[7])
        
def p_element_tag_empty(p):
    'element : LANGLE tagname tagarguments SLASHRANGLE'
    p[0] = ('tag-element',p[2],p[3],[],p[2])
        
def p_tagname(p):
    'tagname : WORD'
    p[0] = p[1]

def p_tagname_end(p):
    'tagnameend : WORD'
    p[0] = p[1]
        
def p_tagarguments(p):
    'tagarguments : tagargument tagarguments'
    p[0] = dict(list(p[1].items())+list(p[2].items()))

def p_tagarguments_empty(p):
    'tagarguments : '
    p[0] = { }

def p_tagargument_word(p):
    'tagargument : WORD EQUAL WORD'
    p[0] = {p[1] : p[3]}        

def p_tagargument_string(p):
    'tagargument : WORD EQUAL STRING'
    p[0] = {p[1] : p[3]}

def p_element_javascript(p):
    'element : JAVASCRIPT'
    p[0] = ("javascript-element",p[1])

def p_error(p):
    if p!=None:
        print ("Syntax Error : ", "LineNo = ", p.lineno, ", Value = ", p.value)
    else:
        print ("Syntax Error")        
         
"""
htmllexer = lex.lex(module=html_tokens)
htmlparser = yacc.yacc()
htmlast = htmlparser.parse(exdata, lexer=htmllexer)
print (htmlast)
"""
