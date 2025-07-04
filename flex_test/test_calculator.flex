// Simple calculator in Franco syntax

rakm num1, num2, result
char op
rakm validInput = 0

// Input first number with validation
l7d i from 0 l7d 0 do
    etb3("Edkhol el rakm el awel:")
    input num1
    law (num1 >= 0) // Accepting only non-negative for simplicity
        validInput = 1
    lw
        etb3("Raqm ghalat, hawel tani.")
        validInput = 0
    law_ended
    lw (validInput == 1)
        break
l7d_ended

// Input second number with validation
validInput = 0
l7d i from 0 l7d 0 do
    etb3("Edkhol el rakm el tany:")
    input num2
    law (num2 >= 0)
        validInput = 1
    lw
        etb3("Raqm ghalat, hawel tani.")
        validInput = 0
    law_ended
    lw (validInput == 1)
        break
l7d_ended

// Input operator with validation
validInput = 0
l7d i from 0 l7d 0 do
    etb3("Edkhol el 3amaleya (+, -, *, /):")
    input op
    law (op == '+' || op == '-' || op == '*' || op == '/')
        validInput = 1
    lw
        etb3("3amaleya ghalat, hawel tani.")
        validInput = 0
    law_ended
    lw (validInput == 1)
        break
l7d_ended

// Calculate result with division by zero check
law (op == '+')
    result = num1 + num2
lw (op == '-')
    result = num1 - num2
lw (op == '*')
    result = num1 * num2
lw (op == '/')
    law (num2 == 0)
        etb3("La yumkin al-qisma 3ala sifr.")
        result = 0
    lw
        result = num1 / num2
    law_ended
law_ended

etb3("El natiga hya:")
etb3(result)