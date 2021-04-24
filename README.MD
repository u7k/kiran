
# kiran
### minimum viable programming language
    focus on the problem, not the language

This programming language is written 100% in Python and may be a valuable source for someone to understand how the interpreters work.
--or you can create original programs and have fun with it...
The entire source code of kiran is based on [CodePulse's videos](https://www.youtube.com/channel/UCUVahoidFA7F3Asfvamrm7w) 
and [Ruslan's blog](https://ruslanspivak.com/lsbasi-part1/).

### INTERACTIVE SHELL
    python3 shell.py

    kiran > VAR name = "John"
    kiran > PRINT("Hello, " + name)

### RUNNING PROGRAMS
    python3 shell.py

    kiran > RUN(<filepath>)

    Eg. kiran > RUN("examples/guess_game.krn")

## DOCS

### Arithmetic Operators
    -----------------------------------------------------
     + : Addition
    -----------------------------------------------------
     - : Subtraction
    -----------------------------------------------------
     * : Multiplication
    -----------------------------------------------------
     / : Division
    -----------------------------------------------------
     § : Safe Division
    -----------------------------------------------------
        Exm: 
        2 / 0       # "Runtime Error: Division by zero"
        2 § 0       # returns 0.0 without any error
        2 § (2-2)   # also 0.0
    -----------------------------------------------------
     ^ : Exponentiation (Power Operator)
    -----------------------------------------------------
        Exm:
        2 ^ 2   #  4
        2 ^ 3   #  8
        2 ^ 8   #  256

### Variables
    You can use the VAR keyword to create a variable.

        VAR <identifier> = <value>

    Variable is created the moment you first assign a value to it.

        VAR x = 42
        VAR y = (7 * 7)
        7 + (VAR a = 3)

Assigning multiple variables to same value:
        
        VAR a = VAR b = VAR c = 42

You can change a variable's value by reusing the "VAR" keyword:

        VAR price = 20
        VAR price = 19.99

        # "price" variable is now equals to 19.99

Built-in variables:

    -----------------------------------------------------
        NULL        # is equal to 0 by default
    -----------------------------------------------------
        MATH_PI     # 3.141592653589793

### Booleans

    TRUE        # 1
    FALSE       # 0
    NOT TRUE    # 0

### Comparison Operators
    -----------------------------------------------------
     == : Equal
    -----------------------------------------------------
     != : Not Equal
    -----------------------------------------------------
     < : Less than
    -----------------------------------------------------
     > : Greater than
    -----------------------------------------------------
     <= : Less than or equal to
    -----------------------------------------------------
     >= : Greater than or equal to
    -----------------------------------------------------

     Examples:
        7 == 7        # TRUE
        3 + 7 == 10   # TRUE
        3 != 7        # TRUE
        7 == 3        # FALSE
        4 > 6         # FALSE

### Comparison Operators
    -----------------------------------------------------
     AND : Returns TRUE if both statements are TRUE
    -----------------------------------------------------
        Exm:
            3 >= 3 AND 7 == 7   # TRUE
            3 < 3  AND 7 == 7   # FALSE
    -----------------------------------------------------
     OR  : Returns TRUE if one of the statements is TRUE
    -----------------------------------------------------
     NOT : Reverses the result,
           returns FALSE if the result is TRUE
    -----------------------------------------------------

### IF...ELSE
    -----------------------------------------------------
     IF...THEN : IF <TRUE> THEN <execute this>
    -----------------------------------------------------
        Exm:
            IF 7 == 7 THEN 42   # returns 42
            IF 7 != 7 THEN 42

            IF NOT TRUE THEN RETURN

    -----------------------------------------------------
     ELIF...THEN : Checks other conditions.
    -----------------------------------------------------
        Exm:
            VAR a = 3
            IF a >= 7 THEN 100 ELIF a < 7 THEN 200
                                # returns 200
    -----------------------------------------------------
     ELSE : Catches anything that isn't caught by
            preceding conditions.
    -----------------------------------------------------
        Exm:
            VAR age = 17
            VAR price = IF age >= 18 THEN 20 ELSE 15
                                # price = 15

## FOR LOOP
    -----------------------------------------------------
     FOR <var-name> = <start-value> TO <end-value> STEP <count> THEN <expr>
    -----------------------------------------------------
        TO keyword creates a range, incremented by 1 by default, 
        and stops before a specified number (x ..< y):
            VAR result = 1
            FOR i = 1 TO 11 THEN VAR result = result * i

        You can change the increment with the STEP keyword:
            FOR i = 0 TO 10 STEP 2 THEN VAR result = result + i

        Negative STEP values are also allowed:
            VAR res = 1
            FOR i = 10 TO 0 STEP -1 THEN VAR res = res * i

        All loops return a list of values:
            VAR bits = FOR i = 1 TO 9 THEN 2 ^ i
                # bits = [2, 4, 8, 16, 32, 64, 128, 256]

        CONTINUE & BREAK statements:
            VAR a = []
            FOR i = 0 TO 10 THEN; IF i == 4 THEN CONTINUE ELIF i == 8 THEN BREAK; VAR a = a + i; END
                # a = [0, 1, 2, 3, 5, 6, 7]

## WHILE LOOP
    -----------------------------------------------------
     WHILE <condition> THEN <expr>
    -----------------------------------------------------
        VAR i = 0
        WHILE i < 100 THEN VAR i = i + 1    --> i = 100

     CONTINUE & BREAK statements:
        VAR a = []
        VAR i = 0
        WHILE i < 10 THEN; VAR i = i + 1; IF i == 4 THEN CONTINUE; IF i == 8 THEN BREAK; VAR a = a + i; END
                # a = [1, 2, 3, 5, 6, 7]

## FUNCTIONS
    -----------------------------------------------------
     FUNC <identifier> (args) -> <body>
    -----------------------------------------------------
     Creating a function:

        FUNC add (a, b) -> a + b
        
     Calling a function:

        add(3,7)

     Assigning functions to variables:

        VAR myAddFunc = add
        myAddFunc(5,5)

    -----------------------------------------------------
     ANONYMOUS FUNCTIONS: FUNC (args) -> <body>
    -----------------------------------------------------
        
        VAR someFunc = FUNC (a) -> a * 100
        someFunc(10)

    -----------------------------------------------------
     MULTILINE FUNCTIONS
    -----------------------------------------------------
        FUNC foo()
            RETURN 42
        END

     You can use semicolons to separate statements:
        FUNC return_foo(); VAR foo = 42; RETURN foo; END

        return_foo()    # 42

    -----------------------------------------------------


## BUILT-IN FUNCTIONS
    -----------------------------------------------------
     PRINT("Hello World!")
    -----------------------------------------------------
     INPUT()

        Exm:
            VAR name = INPUT()
    
    -----------------------------------------------------
     INPUT_INT()

        Exm:
            VAR age = INPUT_INT()

    -----------------------------------------------------
     IS_NUM(3)          # returns TRUE
    -----------------------------------------------------
     IS_STR("")         # returns TRUE
    -----------------------------------------------------
     IS_LIST([])        # returns TRUE
    -----------------------------------------------------
     IS_FUNC(PRINT)     # returns TRUE
    -----------------------------------------------------
     POP(<list>, <index-num>)
    -----------------------------------------------------
     EXTEND(<list>, <list>)
    -----------------------------------------------------


## LIST
    -----------------------------------------------------
     Empty List:

        []

    -----------------------------------------------------
     Accessing list elements:
        <list> / <index-number>

        VAR exm = [1, 2, 3, 4]
        exm/0               # 1

    -----------------------------------------------------
     Adding new elements:

        [1, 2, 3] + 4       # [1, 2, 3, 4]

    -----------------------------------------------------
     Joining lists:

        [1, 2] * [3, 4]     # [1, 2, 3, 4]

    -----------------------------------------------------
     Removing an element:
        <list> - <index-number>

        VAR exm = [1, 2, 3, 4]
        exm - 3             # exm = [1, 2, 3]

    -----------------------------------------------------
     Returning the number of items in a list:
        LEN(<list>)        

        VAR a = [1, 2, 3, 5, 6, 7]
        LEN(a)              # 6
