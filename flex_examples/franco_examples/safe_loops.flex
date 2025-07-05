// Safe Franco Loop Examples
// CORRECTED: Franco l7d loops specify iteration count - use length(array) for complete access

etb3("=== Safe Franco Loop Examples ===")

// Safe array iteration - THE CORRECT WAY
dorg numbers = [1, 2, 3, 4, 5, 10, 15, 20]

etb3("Array contents using CORRECT Franco loop:")
karr i=0 l7d length(numbers) {
    etb3("numbers[" + i + "] = " + numbers[i])
}

// Safe counting loop
etb3("\nCounting from 0 to 9 (safe Franco style):")
karr counter=0 l7d 9 {
    etb3("Count: " + counter)
}

// Safe nested loops
etb3("\nMultiplication table (safe nested Franco loops):")
karr row=1 l7d 3 {
    klma line = ""
    karr col=1 l7d 3 {
        rakm product = row * col
        line = line + product + " "
    }
    etb3("Row " + row + ": " + line)
}

// Safe while loop equivalent
etb3("\nSafe while-style loop in Franco:")
rakm value = 1
talama value <= 5 {
    etb3("Value: " + value)
    value = value + 1
}

etb3("\n=== Remember: Franco l7d N means exactly N iterations (0 to N-1)! ===")