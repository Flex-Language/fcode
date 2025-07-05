// Test script for the non-interactive calculator
geeb "./calculator.flex"

fun run_all_tests() {
    rakm failures = 0

    // Test case 1: Addition
    lw (calculate(10, 5, '+') != 15) { failures = failures + 1 }

    // Test case 2: Subtraction
    lw (calculate(10, 5, '-') != 5) { failures = failures + 1 }

    // Test case 3: Multiplication
    lw (calculate(10, 5, '*') != 50) { failures = failures + 1 }

    // Test case 4: Division
    lw (calculate(10, 5, '/') != 2) { failures = failures + 1 }

    // Test case 5: Division by zero
    calculate(10, 0, '/')

    rg3 failures
}

// The script will now rely on the process exit code,
// which is implicitly the value of the last expression.
run_all_tests() 