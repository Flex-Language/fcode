// Advanced Flex Programming Patterns - Franco Syntax
// This file demonstrates complex programming patterns and best practices

etb3("=== Advanced Flex Programming Patterns ===")

// 1. Object-Oriented Programming Pattern
sndo2 Person(klma name, rakm age) {
    klma this_name = name
    rakm this_age = age
    
    sndo2 introduce() {
        etb3("Ahlan! Ana " + this_name + " wa omri " + this_age + " sana")
    }
    
    sndo2 have_birthday() {
        this_age = this_age + 1
        etb3(this_name + " asbah omro " + this_age + " sana!")
    }
    
    sndo2 get_age() { rg3 this_age }
    sndo2 get_name() { rg3 this_name }
}

// Create and use objects
Person person1 = Person("Ahmed", 25)
Person person2 = Person("Fatima", 30)

person1.introduce()
person2.introduce()
person1.have_birthday()

etb3("")

// 2. Advanced Data Structures - Binary Tree
sndo2 TreeNode(rakm value) {
    rakm this_value = value
    TreeNode this_left = null
    TreeNode this_right = null
    
    sndo2 insert(rakm new_value) {
        lw new_value < this_value {
            lw this_left == null {
                this_left = TreeNode(new_value)
            }
            gher {
                this_left.insert(new_value)
            }
        }
        gher {
            lw this_right == null {
                this_right = TreeNode(new_value)
            }
            gher {
                this_right.insert(new_value)
            }
        }
    }
    
    sndo2 inorder_traversal() {
        lw this_left != null { this_left.inorder_traversal() }
        etb3(this_value + " ")
        lw this_right != null { this_right.inorder_traversal() }
    }
    
    sndo2 search(rakm target) {
        lw target == this_value { rg3 sa7 }
        lw target < this_value && this_left != null {
            rg3 this_left.search(target)
        }
        lw target > this_value && this_right != null {
            rg3 this_right.search(target)
        }
        rg3 ghalt
    }
}

// Demonstrate binary tree usage
etb3("=== Binary Tree Demo ===")
TreeNode root = TreeNode(50)
dorg values = [30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

karr i=0 l7d length(values) - 1 {
    root.insert(values[i])
}

etb3("Inorder traversal (sorted): ")
root.inorder_traversal()
etb3("")

etb3("Searching for 35: " + (root.search(35) ? "Found" : "Not found"))
etb3("Searching for 100: " + (root.search(100) ? "Found" : "Not found"))
etb3("")

// 3. Advanced Error Handling Pattern
sndo2 SafeDivision(kasr numerator, kasr denominator) {
    lw denominator == 0 {
        etb3("Khata: al-qisma ala sifr gher mumkina!")
        rg3 null
    }
    
    lw numerator == 0 {
        rg3 0.0
    }
    
    rg3 numerator / denominator
}

sndo2 CalculateAverage(dorg numbers) {
    lw length(numbers) == 0 {
        etb3("Khata: al-qa'ima farigh!")
        rg3 null
    }
    
    kasr sum = 0.0
    karr i=0 l7d length(numbers) - 1 {
        sum = sum + numbers[i]
    }
    
    rg3 SafeDivision(sum, length(numbers))
}

// Demonstrate error handling
etb3("=== Error Handling Demo ===")
dorg test_numbers = [10, 20, 30, 40, 50]
kasr average = CalculateAverage(test_numbers)
lw average != null {
    etb3("Al-mutawasit: " + average)
}

dorg empty_list = []
kasr bad_average = CalculateAverage(empty_list)

etb3("")

// 4. Advanced Algorithm - Quick Sort
sndo2 QuickSort(dorg arr, rakm low, rakm high) {
    lw low < high {
        rakm pivot_index = Partition(arr, low, high)
        QuickSort(arr, low, pivot_index - 1)
        QuickSort(arr, pivot_index + 1, high)
    }
}

sndo2 Partition(dorg arr, rakm low, rakm high) {
    rakm pivot = arr[high]
    rakm i = low - 1
    
    karr j=low l7d high - 1 {
        lw arr[j] <= pivot {
            i = i + 1
            Swap(arr, i, j)
        }
    }
    
    Swap(arr, i + 1, high)
    rg3 i + 1
}

sndo2 Swap(dorg arr, rakm i, rakm j) {
    rakm temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
}

sndo2 PrintArray(dorg arr, klma title) {
    etb3(title + ": ")
    karr i=0 l7d length(arr) - 1 {
        etb3(arr[i] + " ")
    }
    etb3("")
}

// Demonstrate QuickSort
etb3("=== QuickSort Demo ===")
dorg unsorted = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
PrintArray(unsorted, "Qabl al-tartib")

QuickSort(unsorted, 0, length(unsorted) - 1)
PrintArray(unsorted, "Ba'd al-tartib")

etb3("")

// 5. Advanced Pattern Matching and State Machine
sndo2 StateMachine() {
    klma current_state = "idle"
    dorg valid_transitions = [
        ["idle", "working", "sleeping"],
        ["working", "idle", "break"],
        ["break", "working", "idle"],
        ["sleeping", "idle"]
    ]
    
    sndo2 transition_to(klma new_state) {
        // Check if transition is valid
        dorg current_valid = []
        karr i=0 l7d length(valid_transitions) - 1 {
            lw valid_transitions[i][0] == current_state {
                current_valid = valid_transitions[i]
                break
            }
        }
        
        // Check if new_state is in valid transitions
        so2al found = ghalt
        karr j=1 l7d length(current_valid) - 1 {
            lw current_valid[j] == new_state {
                found = sa7
                break
            }
        }
        
        lw found {
            etb3("Transition: " + current_state + " -> " + new_state)
            current_state = new_state
            rg3 sa7
        }
        gher {
            etb3("Invalid transition: " + current_state + " -> " + new_state)
            rg3 ghalt
        }
    }
    
    sndo2 get_current_state() { rg3 current_state }
}

// Demonstrate state machine
etb3("=== State Machine Demo ===")
StateMachine machine = StateMachine()

etb3("Current state: " + machine.get_current_state())
machine.transition_to("working")
machine.transition_to("break")
machine.transition_to("sleeping")  // Invalid transition
machine.transition_to("idle")
machine.transition_to("sleeping")  // Valid transition

etb3("")

// 6. Advanced Functional Programming Pattern
sndo2 Map(dorg arr, sndo2 func) {
    dorg result = []
    karr i=0 l7d length(arr) - 1 {
        result.push(func(arr[i]))
    }
    rg3 result
}

sndo2 Filter(dorg arr, sndo2 predicate) {
    dorg result = []
    karr i=0 l7d length(arr) - 1 {
        lw predicate(arr[i]) {
            result.push(arr[i])
        }
    }
    rg3 result
}

sndo2 Reduce(dorg arr, sndo2 reducer, rakm initial) {
    rakm accumulator = initial
    karr i=0 l7d length(arr) - 1 {
        accumulator = reducer(accumulator, arr[i])
    }
    rg3 accumulator
}

// Helper functions for functional programming demo
sndo2 Square(rakm x) { rg3 x * x }
sndo2 IsEven(rakm x) { rg3 (x % 2) == 0 }
sndo2 Add(rakm a, rakm b) { rg3 a + b }

// Demonstrate functional programming
etb3("=== Functional Programming Demo ===")
dorg numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

dorg squared = Map(numbers, Square)
PrintArray(squared, "Squared numbers")

dorg evens = Filter(numbers, IsEven)
PrintArray(evens, "Even numbers")

rakm sum = Reduce(numbers, Add, 0)
etb3("Sum of all numbers: " + sum)

etb3("")

// 7. Advanced Memory Management Pattern
sndo2 MemoryPool(rakm pool_size) {
    dorg pool = []
    dorg free_indices = []
    rakm next_index = 0
    
    // Initialize pool
    karr i=0 l7d pool_size - 1 {
        pool.push(null)
        free_indices.push(i)
    }
    
    sndo2 allocate(rakm value) {
        lw length(free_indices) == 0 {
            etb3("Memory pool full!")
            rg3 -1
        }
        
        rakm index = free_indices.pop()
        pool[index] = value
        rg3 index
    }
    
    sndo2 deallocate(rakm index) {
        lw index >= 0 && index < length(pool) {
            pool[index] = null
            free_indices.push(index)
        }
    }
    
    sndo2 get_value(rakm index) {
        lw index >= 0 && index < length(pool) {
            rg3 pool[index]
        }
        rg3 null
    }
    
    sndo2 get_stats() {
        rakm used = pool_size - length(free_indices)
        etb3("Memory Pool Stats:")
        etb3("  Total size: " + pool_size)
        etb3("  Used: " + used)
        etb3("  Free: " + length(free_indices))
    }
}

// Demonstrate memory pool
etb3("=== Memory Pool Demo ===")
MemoryPool memory = MemoryPool(5)

rakm index1 = memory.allocate(100)
rakm index2 = memory.allocate(200)
rakm index3 = memory.allocate(300)

memory.get_stats()

etb3("Value at index " + index1 + ": " + memory.get_value(index1))
etb3("Value at index " + index2 + ": " + memory.get_value(index2))

memory.deallocate(index2)
memory.get_stats()

etb3("")
etb3("=== Advanced Patterns Demo Complete ===")

// 8. Advanced Concurrency Pattern (Simulation)
sndo2 TaskScheduler() {
    dorg task_queue = []
    so2al is_running = ghalt
    
    sndo2 add_task(klma task_name, rakm priority) {
        dorg task = [task_name, priority, "pending"]
        task_queue.push(task)
        
        // Simple priority sort (higher priority first)
        karr i=0 l7d length(task_queue) - 2 {
            karr j=i+1 l7d length(task_queue) - 1 {
                lw task_queue[i][1] < task_queue[j][1] {
                    dorg temp = task_queue[i]
                    task_queue[i] = task_queue[j]
                    task_queue[j] = temp
                }
            }
        }
    }
    
    sndo2 execute_next_task() {
        lw length(task_queue) == 0 {
            rg3 ghalt
        }
        
        dorg task = task_queue[0]  // Get first task
        
        // Workaround for task_queue.shift()
        dorg new_queue = []
        karr i=1 l7d length(task_queue) - 1 {
            new_queue.push(task_queue[i])
        }
        task_queue = new_queue

        task[2] = "running"
        etb3("Executing task: " + task[0] + " (priority: " + task[1] + ")")
        
        // Simulate task execution
        task[2] = "completed"
        rg3 sa7
    }
    
    sndo2 run_all_tasks() {
        etb3("Starting task scheduler...")
        talama length(task_queue) > 0 {
            execute_next_task()
        }
        etb3("All tasks completed!")
    }
    
    sndo2 get_queue_status() {
        etb3("Task Queue Status:")
        lw length(task_queue) == 0 {
            etb3("  No pending tasks")
        }
        gher {
            karr i=0 l7d length(task_queue) - 1 {
                dorg task = task_queue[i]
                etb3("  " + task[0] + " (priority: " + task[1] + ", status: " + task[2] + ")")
            }
        }
    }
}

// Demonstrate task scheduler
etb3("=== Task Scheduler Demo ===")
TaskScheduler scheduler = TaskScheduler()

scheduler.add_task("Initialize system", 1)
scheduler.add_task("Load configuration", 5)
scheduler.add_task("Start database", 8)
scheduler.add_task("Launch web server", 3)
scheduler.add_task("Run health check", 10)

scheduler.get_queue_status()
scheduler.run_all_tasks()

etb3("")
etb3("🚀 Advanced Flex patterns demonstration complete! 🚀") 