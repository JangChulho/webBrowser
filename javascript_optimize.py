def optimize(exp):    
    etype = exp[0]
    if etype == "binop":       
        a = optimize(exp[1])
        op = exp[2]
        b = optimize(exp[3])

        if op == "*" and (a == ("number", 0) or b == ("number", 0)):
            return ("number", 0)
        elif op == "+" and a == ("number", 0):
            return b
        elif op == "+" and b == ("number", 0):
            return a
        elif op == "*" and a == ("number", 1):
            return b
        elif op == "*" and b == ("number", 1):
            return a
        elif op == "-" and a == b:
            return ("number", 0)

        if a[0] == "number" and b[0] == "number":
            if op == "+":
                return ("number", a[1] + b[1])
            elif op == "-":
                return ("number", a[1] - b[1])
            elif op == "*":
                return ("number", a[1] * b[1])
        return (exp[0], a, op, b)
    return exp
