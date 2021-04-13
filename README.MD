
# kiran
### minimum viable programming language

This language has written 100% in Python and can be a valuable source for someone to understand how the compilers works, due to codebase's readability.
--or you can create original programs and have fun with it...
The project is based on ...

For example codes and projects with kiran, please visit:

...

### HOW TO USE
...

## DOCS

### Index
// insert title links

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
        2 / 0       -> "Runtime Error: Division by zero"
        2 § 0       -> returns 0.0 without any error
        2 § (2-2)   -> also 0.0
    -----------------------------------------------------
     ^ : Exponentiation (Power Operator)
    -----------------------------------------------------
        Exm:
        2 ^ 2   ->  4
        2 ^ 3   ->  8
        2 ^ 8   ->  256

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

        --> "price" variable is now equals to 19.99

Built-in variables:

        NULL   -> is equal to 0 as a default

    but you can change that:

        VAR NULL = -1   -> null is now '-1'

### Booleans

    TRUE        -> 1
    FALSE       -> 0
    NOT TRUE    -> 0

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
        7 == 7        -> TRUE
        3 + 7 == 10   -> TRUE
        3 != 7        -> TRUE
        7 == 3        -> FALSE
        4 > 6         -> FALSE

### Comparison Operators
    -----------------------------------------------------
     AND : Returns TRUE if both statements are TRUE
    -----------------------------------------------------
        Exm:
            3 >= 3 AND 7 == 7   -> TRUE
            3 < 3  AND 7 == 7   -> FALSE
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
            IF 7 == 7 THEN 42   -> returns 42
            IF 7 != 7 THEN 42   -> does nothing
    -----------------------------------------------------
     ELIF...THEN : Checks other conditions.
    -----------------------------------------------------
        Exm:
            VAR a = 3
            IF a >= 7 THEN 100 ELIF a < 7 THEN 200
                                --> returns 200
    -----------------------------------------------------
     ELSE : Catches anything that isn't caught by
            preceding conditions.
    -----------------------------------------------------
        Exm:
            VAR age = 17
            VAR price = IF age >= 18 THEN 20 ELSE 15
                                --> price = 15