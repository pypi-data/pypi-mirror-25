"""
Functions, programs and meta-nodes

+----------------------------------------------------+-------------------------+
| Functions                                          | Description             |
+====================================================+=========================+
| :py:func:`~matlab2cpp.tree.functions.program`      | Program outer shell     |
+----------------------------------------------------+-------------------------+
| :py:func:`~matlab2cpp.tree.functions.function`     | Explicit functions      |
+----------------------------------------------------+-------------------------+
| :py:func:`~matlab2cpp.tree.functions.main`         | Main script             |
+----------------------------------------------------+-------------------------+
| :py:func:`~matlab2cpp.tree.functions.lambda_assign`| Anonymous function      |
|                                                    | assignment              |
+----------------------------------------------------+-------------------------+
| :py:func:`~matlab2cpp.tree.functions.lambda_func`  | Anonymous function      |
|                                                    | content                 |
+----------------------------------------------------+-------------------------+
"""
from __future__ import print_function
from . import constants, findend, iterate, identify
from .. import collection


def program(self, name):
    """
    The outer shell of the program

    Args:
        self (Builder):
            Code constructor
        name (str):
            Name of the program

    Returns:
        Node: The root node of the constructed node tree

    Example:
        >>> from matlab2cpp.tree import Builder
        >>> builder = Builder(True)
        >>> builder.load("unamed", "a") # doctest: +NORMALIZE_WHITESPACE
        loading unamed
             Program    functions.program
           0 Main       functions.main
           0 Codeblock  codeblock.codeblock
           0   Statement    codeblock.codeblock 'a'
           0     Expression expression.create   'a'
           0     Var        variables.variable  'a'
        >>> builder.configure(suggest=False)
        >>> print(matlab2cpp.qtree(builder)) # doctest: +NORMALIZE_WHITESPACE
        Program    program      TYPE    unamed
        | Includes   program      TYPE
        1 1| Funcs      program      TYPE    unamed
        1 1| | Main       func_return  TYPE    main
        1 1| | | Declares   func_return  TYPE
        1 1| | | Returns    func_return  TYPE
        1 1| | | Params     func_return  TYPE
        1 1| | | Block      code_block   TYPE
        1 1| | | | Statement  code_block   TYPE
        1 1| | | | | Var        unknown      TYPE    a
        | Inlines    program      TYPE    unamed
        | Structs    program      TYPE    unamed
        | Headers    program      TYPE    unamed
        | Log        program      TYPE    unamed
    """
    if self.disp:
        print("     Program    ", end="")
        print("functions.program")

    # Create intial nodes
    program = collection.Program(self.project, name=name, cur=0, code=self.code)
    includes = collection.Includes(program, value=name, code='')
    funcs = collection.Funcs(program, name=name)

    collection.Inlines(program, name=name)
    collection.Structs(program, name=name)
    collection.Headers(program, name=name)
    collection.Log(program, name=name)

    #includes.include("armadillo")
    #includes.include("mconvert")
    # Start processing

    cur = 0

    while True:

        if self.code[cur] in " \t;\n":
            pass

        elif self.code[cur] == "%":
            cur = findend.comment(self, cur)

        elif self.code[cur:cur+8] == "function":
            cur = self.create_function(funcs, cur)

        else:
            self.create_main(funcs, cur)
            break

        if len(self.code)-cur<=2:
            break
        cur += 1

    #includes.include("namespace_arma")

    return program


def function(self, parent, cur):
    """
    Explicit functions

    Args:
        self (Builder): Code constructor
        parent (Node): Parent node
        cur (int): Current position in code

    Returns:
        int : Index to end of function

    Example:
        >>> from matlab2cpp.tree import Builder
        >>> builder = Builder(True)
        >>> builder.load("unnamed", "function f(); end") # doctest: +NORMALIZE_WHITESPACE
        loading unnamed
             Program    functions.program
           0 Function       functions.function  'function f()'
          12 Codeblock  codeblock.codeblock
        >>> builder.configure(suggest=False)
        >>> print(matlab2cpp.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
        1  1Funcs      program      TYPE    unnamed
        1  1| Func       func_returns TYPE    f
        1  1| | Declares   func_returns TYPE
        1  1| | Returns    func_returns TYPE
        1 11| | Params     func_returns TYPE
        1 13| | Block      code_block   TYPE

        >>> builder = Builder(True)
        >>> builder.load("unnamed", "function y=f(x); y=x") # doctest: +NORMALIZE_WHITESPACE
        loading unnamed
             Program    functions.program
           0 Function       functions.function  'function y=f(x)'
           0   Return       'y'
          12   Param        functions.function  'x'
          15 Codeblock  codeblock.codeblock
          17   Assign     assign.single       'y=x'
          17     Var        variables.assign    'y'
          19     Expression expression.create   'x'
          19     Var        variables.variable  'x'
        >>> builder.configure(suggest=False)
        >>> print(matlab2cpp.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
         1   1Funcs      program      TYPE    unnamed
         1   1| Func       func_return  TYPE    f
         1   1| | Declares   func_return  TYPE
         1   1| | | Var        unknown      TYPE    y
         1   1| | Returns    func_return  TYPE
         1  10| | | Var        unknown      TYPE    y
         1  13| | Params     func_return  TYPE
         1  14| | | Var        unknown      TYPE    x
         1  16| | Block      code_block   TYPE
         1  18| | | Assign     unknown      TYPE    x
         1  18| | | | Var        unknown      TYPE    y
         1  20| | | | Var        unknown      TYPE    x
    """
    if self.code[cur:cur+8] != "function":
        self.syntaxerror(cur, "function start")
    if self.code[cur+8] not in constants.k_end+"[":
        self.syntaxerror(cur, "function name or return values")

    START = cur
    k = cur + 8

    while self.code[k] in " \t":
        k += 1

    if  self.code[k] not in constants.letters+"[":
        self.syntaxerror(k, "function name or return values")
    start = k

    k = findend.expression(self, k)
    end = k

    k += 1
    while self.code[k] in " \t":
        k += 1

    # with return values
    if self.code[k] == "=":

        k += 1
        while self.code[k] in " \t.":
            if self.code[k:k+3] == "...":
                k = findend.dots(self, k)+1
            else:
                k += 1

        l = k
        if  self.code[l] not in constants.letters:
            self.syntaxerror(l, "function name")

        while self.code[l+1] in constants.letters+constants.digits+"_":
            l += 1

        m = l+1

        while self.code[m] in " \t":
            m += 1

        if self.code[m] == "(":
            m = findend.paren(self, m)
        else:
            m = l

        if self.disp:
            print("%4d Function       " % cur, end="")
            print("%-20s" % "functions.function", end="")
            print(repr(self.code[START:m+1]))

        name = self.code[k:l+1]
        func = collection.Func(parent, name, cur=cur)
        collection.Declares(func, code="")
        returns = collection.Returns(func, code=self.code[start:end+1])

        # multi-return
        if self.code[start] == "[":
            if identify.space_delimited(self, start):
                L = iterate.space_list(self, start)
            else:
                L = iterate.comma_list(self, start)
            end = START
            for array in L:
                for s,e in array:
                    end = s

                    if self.disp:
                        print("%4d   Return       " % cur, end="")
                        print("%-20s" % "functions.function", end="")
                        print(repr(self.code[s:e+1]))

                    if not any([a in constants.letters+constants.digits+"_@" \
                                for a in self.code[s:e+1]]):
                        self.syntaxerror(s, "return value")

                    collection.Var(returns, self.code[s:e+1], cur=s,
                                   code=self.code[s:e+1])

        # single return
        else:
            end = findend.expression(self, start)

            if self.disp:
                print("%4d   Return       " % cur, end="")
                print(repr(self.code[start:end+1]))

            collection.Var(returns, self.code[start:end+1], cur=start,
                           code=self.code[start:end+1])


        cur = l+1
        while self.code[cur] in " \t":
            cur += 1

    # No returns
    else:
        m = k
        if self.code[m] == "(":
            m = findend.paren(self, m)
        else:
            m = end


        if self.disp:
            print("%4d Function       " % cur, end="")
            print("%-20s" % "functions.function", end="")
            print(repr(self.code[START:m+1]))

        end = start+1
        while self.code[end] in constants.letters+"_":
            end += 1

        name = self.code[start:end]
        func = collection.Func(parent, name, cur=cur)

        collection.Declares(func)
        returns = collection.Returns(func)

        cur = end

    # Parameters
    params = collection.Params(func, cur=cur)
    if self.code[cur] == "(":

        end = findend.paren(self, cur)
        params.code = self.code[cur+1:end]

        L = iterate.comma_list(self, cur)
        for array in L:
            for s,e in array:

                if self.disp:
                    print("%4d   Param        " % cur, end="")
                    print("%-20s" % "functions.function", end="")
                    print(repr(self.code[s:e+1]))

                var = collection.Var(params, self.code[s:e+1], cur=s,
                                     code=self.code[s:e+1])

        cur = end

    cur += 1

    cur = self.create_codeblock(func, cur)

    # Postfix
    for var in returns:
        var.create_declare()

    end = cur
    func.code = self.code[START:end+1]

    collection.Header(func.program[4], func.name)

    return cur


def main(self, parent, cur):
    """
    Main script

    Args:
        self (Builder): Code constructor
        parent (Node): Parent node
        cur (int): Current position in code

    Returns:
        int : Index to end of script

    Example:
        >>> from matlab2cpp.tree import Builder
        >>> builder = Builder(True)
        >>> builder.load("unnamed", "a") # doctest: +NORMALIZE_WHITESPACE
        loading unnamed
             Program    functions.program
           0 Main       functions.main
           0 Codeblock  codeblock.codeblock
           0   Statement    codeblock.codeblock 'a'
           0     Expression expression.create   'a'
           0     Var        variables.variable  'a'
        >>> builder.configure(suggest=False)
        >>> print(matlab2cpp.qtree(builder)) # doctest: +NORMALIZE_WHITESPACE
        Program    program      TYPE    unnamed
        | Includes   program      TYPE
        1 1| Funcs      program      TYPE    unnamed
        1 1| | Main       func_return  TYPE    main
        1 1| | | Declares   func_return  TYPE
        1 1| | | Returns    func_return  TYPE
        1 1| | | Params     func_return  TYPE
        1 1| | | Block      code_block   TYPE
        1 1| | | | Statement  code_block   TYPE
        1 1| | | | | Var        unknown      TYPE    a
        | Inlines    program      TYPE    unnamed
        | Structs    program      TYPE    unnamed
        | Headers    program      TYPE    unnamed
        | Log        program      TYPE    unnamed
    """

    if self.disp:
        print("%4d Main       " % cur, end="")
        print("functions.main")

    func = collection.Main(parent)

    collection.Declares(func)#, backend="func_return")
    collection.Returns(func)#, backend="func_return")
    collection.Params(func)#, backend="func_return")

    return self.create_codeblock(func, cur)


def lambda_assign(self, node, cur, eq_loc):
    """
    Anonymous function constructor

    Args:
        self (Builder): Code constructor
        parent (Node): Parent node
        cur (int): Current position in code
        eq_loc (int): location of assignment sign ('=')

    Returns:
        int : Index to end of function line

    Example:
        >>> from matlab2cpp.tree import Builder
        >>> builder = Builder(True)
        >>> builder.load("unnamed", "f = @(x) 2*x") # doctest: +NORMALIZE_WHITESPACE
        loading unnamed
             Program    functions.program
           0 Main       functions.main
           0 Codeblock  codeblock.codeblock
           0   Assign       'f = @(x) 2*x' functions.lambda_assign
           0     Var        variables.assign    'f'
           4   Lambda       functions.lambda_func'@(x) 2*x'
           6     Expression expression.create   'x'
           6     Var        variables.variable  'x'
           9     Expression expression.create   '2*x'
           9     Expression expression.create   '2'
           9     Int        misc.number         '2'
          11     Expression expression.create   'x'
          11     Var        variables.variable  'x'
        >>> builder.configure(suggest=False)
        >>> print(matlab2cpp.qtree(builder)) # doctest: +NORMALIZE_WHITESPACE
        Program    program      TYPE    unnamed
        | Includes   program      TYPE
        1  1| Funcs      program      TYPE    unnamed
        1  1| | Main       func_return  TYPE    main
        1  1| | | Declares   func_return  TYPE
        1  1| | | | Var        func_lambda  TYPE    f
        1  1| | | Returns    func_return  TYPE
        1  1| | | Params     func_return  TYPE
        1  1| | | Block      code_block   TYPE
        1  1| | | | Assign     func_lambda  func_lambda
        1  1| | | | | Var        func_lambda  TYPE    f
        1  1| | | | | Lambda     func_lambda  func_lambda_f
        1  5| | Func       func_lambda  TYPE    _f
        1  5| | | Declares   func_lambda  TYPE
        1  5| | | | Var        unknown      TYPE    _retval
        1  5| | | Returns    func_lambda  TYPE
        1  5| | | | Var        unknown      TYPE    _retval
        1  5| | | Params     func_lambda  TYPE
        1  7| | | | Var        unknown      TYPE    x
        1  5| | | Block      code_block   TYPE
        1  5| | | | Assign     expression   TYPE
        1  5| | | | | Var        unknown      TYPE    _retval
        1 10| | | | | Mul        expression   TYPE
        1 10| | | | | | Int        int          int
        1 12| | | | | | Var        unknown      TYPE    x
        | Inlines    program      TYPE    unnamed
        | Structs    program      TYPE    unnamed
        | Headers    program      TYPE    unnamed
        | Log        program      TYPE    unnamed
    """

    if  self.code[cur] not in constants.letters:
        self.syntaxerror(cur, "anonymous function name")

    if  self.code[eq_loc] != "=":
        self.syntaxerror(cur, "anonymous function assignment (=)")

    if self.disp:
        print("%4d   Assign       " % cur, end="")
        print(repr(self.code[cur:self.code.find("\n", cur)]), end=" ")
        print("functions.lambda_assign")

    assign = collection.Assign(node, cur=cur)#, backend="func_lambda")

    self.create_assign_variable(assign, cur, eq_loc)

    k = eq_loc+1
    while self.code[k] in " \t":
        k += 1

    end = self.create_lambda_func(assign, k)
    assign.code = self.code[cur:end+1]

    return end

def lambda_func(self, node, cur):
    """
    Anonymous function content. Support function of `lambda_assign`.

    Args:
        self (Builder): Code constructor
        parent (Node): Parent node
        cur (int): Current position in code

    Returns:
        int : Index to end of function line
    """
    if  self.code[cur] != "@":
        self.syntaxerror(cur, "anonymous function indicator (@)")

    end = cur +1
    while self.code[end] in " \t":
        end += 1

    if  self.code[end] != "(":
        self.syntaxerror(end, "anonymous function argument list")

    end = findend.paren(self, end)

    end += 1
    while self.code[end] in " \t":
        end += 1

    end = findend.expression(self, end)

    if self.disp:
        print("%4d   Lambda       " % cur, end="")
        print("%-20s" % "functions.lambda_func", end="")
        print(repr(self.code[cur:end+1]))

    if node.cls == "Assign":
        name = node[0].name
    else:
        name = "lambda"

    funcs = node.program[1]
    name = "_%s" % (name)
    if name in funcs.names:
        i = 0
        while name+"%d" % i in funcs.names:
            i += 1
        name = name + "%d" % i

    func = collection.Func(funcs, name, cur=cur, code=self.code[cur:end+1])

    declares = collection.Declares(func)
    returns = collection.Returns(func)
    params = collection.Params(func)

    k = cur+1
    while self.code[k] in " \t":
        k += 1

    if  self.code[k] != "(":
        self.syntaxerror(k, "anonymous function argument list")

    cur = self.create_list(params, k)

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    block = collection.Block(func)
    assign = collection.Assign(block)
    var = collection.Var(assign, "_retval")

    cur = self.create_expression(assign, cur, end=end)

    for n in assign[1].flatten():
        if (n.cls in ("Get", "Cget", "Var", "Fvar", "Fget",
                      "Sget")) and n.name in node.func[0].names + node.func[2].names:

            n.create_declare()


    var = collection.Var(returns, "_retval")
    var.create_declare()

    lamb = collection.Lambda(node, name)

    lamb.reference = func

    return cur

if __name__ == "__main__":
    import doctest
    doctest.testmod()
