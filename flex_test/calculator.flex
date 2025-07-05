// Simple calculator in Franco syntax - Non-interactive version

fun calculate(rakm num1, rakm num2, klma op) {
    rakm result = 0

    // Calculate result with division by zero check
    lw (op == '+') {
        result = num1 + num2
    }
    aw (op == '-') {
        result = num1 - num2
    }
    aw (op == '*') {
        result = num1 * num2
    }
    aw (op == '/') {
        lw (num2 == 0) {
            etb3("Khata: La yumkin al-qisma 3ala sifr.")
            result = 0  // Or handle as an error
        }
        gher {
            result = num1 / num2
        }
    }
    gher {
        etb3("3amaleya ghalat: " + op)
    }

    rg3 result
} 