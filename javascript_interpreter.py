import javascript_optimize

def eval_elt(elt, env):
    elttype = elt[0]
    if elttype == 'function':
        fname = elt[1]
        fparams = elt[2]
        fbody = elt[3]
        fvalue = ("function", fparams, fbody, env)
        env[1][fname] = fvalue
    elif elttype == "stmt":
        eval_stmt(elt[1], env)
    else:
        print("Interpret Error: wrong element", elttype)
        
def eval_stmts(stmts, env):
    for stmt in stmts:
        eval_stmt(stmt, env)
        
def eval_stmt(stmt, env):
    stmttype = stmt[0]
    if stmttype == 'if-then':
        exp = stmt[1]
        compoundstmt = stmt[2]
        if eval_exp(exp, env):
            eval_stmts(compoundstmt, env)
    elif stmttype == 'if-then-else':
        exp = stmt[1]
        then_compoundstmt = stmt[2]
        else_compoundstmt = stmt[3]
        if eval_exp(exp, env):
            eval_stmts(then_compoundstmt, env)
        else:
            eval_stmts(else_compoundstmt, env)            
    elif stmttype == 'while':
        exp = stmt[1]
        compoundstmt = stmt[2]        
        while eval_exp(exp, env):
            eval_stmts(compoundstmt, env)                    
    elif stmttype == 'var':
        vname = stmt[1]
        exp = stmt[2]
        env[1][vname] = eval_exp(exp, env)
    elif stmttype == 'assign':
        vname = stmt[1]
        exp = stmt[2]
        new_value = eval_exp(exp, env)
        env_update(vname, new_value, env)
    elif stmttype == 'return':
        exp = stmt[1]
        retval = eval_exp(exp, env)
        raise Exception(retval)
    elif stmttype == 'exp':
        eval_exp(stmt[1], env)
    else:
        print("Interpret Error: wrong statement", stmttype)

def eval_exp(exp, env):
    newexp = javascript_optimize.optimize(exp)    
    etype = newexp[0]
    if etype == "identifier":
        vname = newexp[1]
        value = env_lookup(vname, env)
        if value == None:
            print("Interpret Error: unbound variable", vname)
        else:
            return value
    elif etype == "number":
        return newexp[1]
    elif etype == "string":
        return newexp[1]
    elif etype == "true":
        return True
    elif etype == "false":
        return False
    elif etype == "not":
        return not(eval_exp(newexp[1], env))    
    elif etype == "binop":
        a = eval_exp(newexp[1],env)
        op = newexp[2]
        b = eval_exp(newexp[3],env)
        if op == "*":
            return a*b
        elif op == "/":
            return a/b
        elif op == "+":
            return a+b
        elif op == "-":
            return a-b
        elif op == "%":
            return a%b
        elif op == "&&":
            return a and b
        elif op == "||":
            return a or b
        elif op == "==":
            return a==b
        elif op == ">=":
            return a>=b
        elif op == ">":
            return a>b
        elif op == "<=":
            return a<=b
        elif op == "<":
            return a<b
        else:
            print("Interpret Error: wrong operator", op)
    elif etype == "call":
        fname = newexp[1]
        args = newexp[2]
        fvalue = env_lookup(fname, env)
        if fname == "write":
            argval = eval_exp(args[0], env)
            output_sofar = env_lookup("javascript output", env)            
            env_update("javascript output", output_sofar + str(argval), env)            
        elif fvalue[0] == "function":
            fparams = fvalue[1]
            fbody = fvalue[2]
            fenv = fvalue[3]
            if len(fparams) != len(args):
                print("Interprete Error: wrong number of args", fname)
            else:
                newenv = (fenv, {})
                for i in range(len(args)):
                    argval = eval_exp(args[i], env)
                    (newenv[1])[fparams[i]] = argval
                try:
                    eval_stmts(fbody, newenv)
                    return None
                except Exception as retval:
                    return retval
        else:
            print("Interpret ERROR: wrong function", fname)
    else:
        print("Interpret Error: wrong expression", etype)
        return None

def env_lookup(vname, env):
    if vname in env[1]:
        return (env[1])[vname]
    elif env[0] == None:
        return None
    else:
        return env_lookup(vname, env[0])

def env_update(vname, value, env):
    if vname in env[1]:
        env[1][vname] = value
    elif not (env[0] == None):
        env_update(vname, value, env[0])

def interpret(ast):
    global_env = (None, {"javascript output" : ""})
    for elt in ast:
        eval_elt(elt, global_env)
    return (global_env[1])["javascript output"]
