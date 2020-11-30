import ply.lex as lex

tokens = ('NAME', 'NUMBER', 'PLUS', 'MINUS', 'EQUALS')
# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_EQUALS  = r'='
t_NAME    = r'\$[a-zA-Z]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer

lex.lex()

# dictionary of names (for storing variables)
names = { }

def p_a_assignment(p):
    'a : assignment'
    p[0] = p[1]

def p_a_equation(p):
    'a : equation'
    p[0] = p[1]

def p_statement_assign(p):
    'assignment : constant EQUALS term'
    names[p[1]] = p[3]
    p[0] = p[3]

def p_equation_binop(p):
    'equation : constant EQUALS term PLUS term'
    names[p[1]] = p[3] + p[5]
    p[0] = p[3] + p[5]

def p_equation_minus(p):
    'equation : constant EQUALS term MINUS term'
    names[p[1]] = p[3] - p[5]
    p[0] = p[3] - p[5]

def p_term_int_literal(p):
    'term : int_literal'
    p[0] = p[1]

def p_term_constant(p):
    'term : constant'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_int_literal(p):
    'int_literal : NUMBER'
    p[0] = p[1]

def p_constant(p):
    'constant : NAME'
    p[0] = p[1]

def p_error(p):
    print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = yacc.parse(s)
    print(result)
