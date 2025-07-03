// Safe Loop Examples in English syntax
// English loops are naturally safe (non-inclusive)

print("=== Safe English Loop Examples ===")

// Safe array iteration - English style
list numbers = [1, 2, 3, 4, 5, 10, 15, 20]

print("Array contents using English loops:")
for(i=0; i<length(numbers); i++) {
    print("numbers[" + i + "] = " + numbers[i])
}

// Safe counting loop
print("\nCounting from 0 to 9 (English style):")
for(counter=0; counter<10; counter++) {
    print("Count: " + counter)
}

// Safe nested loops
print("\nMultiplication table (English nested loops):")
for(row=1; row<=3; row++) {
    string line = ""
    for(col=1; col<=3; col++) {
        int product = row * col
        line = line + product + " "
    }
    print("Row " + row + ": " + line)
}

// While loop
print("\nWhile loop in English:")
int value = 1
while (value <= 5) {
    print("Value: " + value)
    value = value + 1
}

print("\n=== English loops are naturally safe! ===")