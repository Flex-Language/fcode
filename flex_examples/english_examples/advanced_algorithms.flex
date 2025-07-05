// Advanced Algorithms and Data Structures - English Syntax
// This file demonstrates sophisticated programming concepts in Flex

print("=== Advanced Algorithms and Data Structures ===")

// 1. Graph Algorithms - Dijkstra's Shortest Path
fun Graph(int num_vertices) {
    list adjacency_list = []
    int vertex_count = num_vertices
    
    // Initialize adjacency list
    for(i=0; i<num_vertices; i++) {
        list neighbors = []
        adjacency_list.push(neighbors)
    }
    
    fun add_edge(int from, int to, float weight) {
        list edge = [to, weight]
        adjacency_list[from].push(edge)
    }
    
    fun dijkstra(int start) {
        list distances = []
        list visited = []
        list previous = []
        
        // Initialize arrays
        for(i=0; i<vertex_count; i++) {
            distances.push(999999.0)  // Infinity
            visited.push(false)
            previous.push(-1)
        }
        
        distances[start] = 0.0
        
        for(count=0; count<vertex_count; count++) {
            int min_vertex = find_minimum_distance(distances, visited)
            if(min_vertex == -1) break
            
            visited[min_vertex] = true
            
            list neighbors = adjacency_list[min_vertex]
            for(i=0; i<length(neighbors); i++) {
                int neighbor = neighbors[i][0]
                float weight = neighbors[i][1]
                
                if(!visited[neighbor]) {
                    float new_distance = distances[min_vertex] + weight
                    if(new_distance < distances[neighbor]) {
                        distances[neighbor] = new_distance
                        previous[neighbor] = min_vertex
                    }
                }
            }
        }
        
        return [distances, previous]
    }
    
    fun find_minimum_distance(list distances, list visited) {
        float min_dist = 999999.0
        int min_vertex = -1
        
        for(i=0; i<length(distances); i++) {
            if(!visited[i] && distances[i] < min_dist) {
                min_dist = distances[i]
                min_vertex = i
            }
        }
        
        return min_vertex
    }
    
    fun print_path(list previous, int start, int end) {
        if(end == start) {
            print(start + " ")
            return
        }
        
        if(previous[end] == -1) {
            print("No path exists")
            return
        }
        
        print_path(previous, start, previous[end])
        print(end + " ")
    }
}

// Demonstrate Dijkstra's algorithm
print("=== Dijkstra's Shortest Path Demo ===")
Graph graph = Graph(6)

// Add edges (from, to, weight)
graph.add_edge(0, 1, 4.0)
graph.add_edge(0, 2, 2.0)
graph.add_edge(1, 2, 1.0)
graph.add_edge(1, 3, 5.0)
graph.add_edge(2, 3, 8.0)
graph.add_edge(2, 4, 10.0)
graph.add_edge(3, 4, 2.0)
graph.add_edge(3, 5, 6.0)
graph.add_edge(4, 5, 3.0)

list result = graph.dijkstra(0)
list distances = result[0]
list previous = result[1]

print("Shortest distances from vertex 0:")
for(i=0; i<length(distances); i++) {
    print("To vertex " + i + ": " + distances[i])
}

print("Shortest path from 0 to 5: ")
graph.print_path(previous, 0, 5)
print("")

// 2. Advanced Sorting - Merge Sort
fun merge_sort(list arr) {
    if(length(arr) <= 1) return arr
    
    int mid = length(arr) / 2
    list left = []
    list right = []
    
    // Split array
    for(i=0; i<mid; i++) {
        left.push(arr[i])
    }
    for(i=mid; i<length(arr); i++) {
        right.push(arr[i])
    }
    
    // Recursively sort both halves
    left = merge_sort(left)
    right = merge_sort(right)
    
    // Merge sorted halves
    return merge(left, right)
}

fun merge(list left, list right) {
    list result = []
    int left_idx = 0
    int right_idx = 0
    
    // Merge while both arrays have elements
    while(left_idx < length(left) && right_idx < length(right)) {
        if(left[left_idx] <= right[right_idx]) {
            result.push(left[left_idx])
            left_idx++
        } else {
            result.push(right[right_idx])
            right_idx++
        }
    }
    
    // Add remaining elements
    while(left_idx < length(left)) {
        result.push(left[left_idx])
        left_idx++
    }
    while(right_idx < length(right)) {
        result.push(right[right_idx])
        right_idx++
    }
    
    return result
}

// Demonstrate merge sort
print("=== Merge Sort Demo ===")
list unsorted_array = [38, 27, 43, 3, 9, 82, 10, 15, 1, 56]
print("Original array: " + array_to_string(unsorted_array))

list sorted_array = merge_sort(unsorted_array)
print("Sorted array: " + array_to_string(sorted_array))
print("")

// 3. Dynamic Programming - Longest Common Subsequence
fun longest_common_subsequence(string str1, string str2) {
    int m = length(str1)
    int n = length(str2)
    
    // Create DP table
    list dp = []
    for(i=0; i<=m; i++) {
        list row = []
        for(j=0; j<=n; j++) {
            row.push(0)
        }
        dp.push(row)
    }
    
    // Fill DP table
    for(i=1; i<=m; i++) {
        for(j=1; j<=n; j++) {
            if(str1[i-1] == str2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            }
        }
    }
    
    // Reconstruct LCS
    string lcs = ""
    int i = m
    int j = n
    
    while(i > 0 && j > 0) {
        if(str1[i-1] == str2[j-1]) {
            lcs = str1[i-1] + lcs
            i--
            j--
        } else if(dp[i-1][j] > dp[i][j-1]) {
            i--
        } else {
            j--
        }
    }
    
    return [dp[m][n], lcs]
}

fun max(int a, int b) {
    return a > b ? a : b
}

// Demonstrate LCS
print("=== Longest Common Subsequence Demo ===")
string text1 = "ABCDGH"
string text2 = "AEDFHR"

list lcs_result = longest_common_subsequence(text1, text2)
print("String 1: " + text1)
print("String 2: " + text2)
print("LCS Length: " + lcs_result[0])
print("LCS: " + lcs_result[1])
print("")

// 4. Advanced Data Structure - Red-Black Tree (Simplified)
fun RBNode(int value) {
    int data = value
    string color = "red"  // red or black
    RBNode left = null
    RBNode right = null
    RBNode parent = null
    
    fun is_red() return color == "red"
    fun is_black() return color == "black"
    fun set_red() { color = "red" }
    fun set_black() { color = "black" }
}

fun RedBlackTree() {
    RBNode root = null
    
    fun insert(int value) {
        RBNode new_node = RBNode(value)
        
        if(root == null) {
            root = new_node
            root.set_black()
            return
        }
        
        // Standard BST insertion
        RBNode current = root
        RBNode parent = null
        
        while(current != null) {
            parent = current
            if(value < current.data) {
                current = current.left
            } else if(value > current.data) {
                current = current.right
            } else {
                return  // Duplicate value
            }
        }
        
        new_node.parent = parent
        if(value < parent.data) {
            parent.left = new_node
        } else {
            parent.right = new_node
        }
        
        // Fix Red-Black properties
        fix_insert(new_node)
    }
    
    fun fix_insert(RBNode node) {
        while(node.parent != null && node.parent.is_red()) {
            RBNode grandparent = node.parent.parent
            
            if(node.parent == grandparent.left) {
                RBNode uncle = grandparent.right
                
                if(uncle != null && uncle.is_red()) {
                    // Case 1: Uncle is red
                    node.parent.set_black()
                    uncle.set_black()
                    grandparent.set_red()
                    node = grandparent
                } else {
                    // Case 2 & 3: Uncle is black
                    if(node == node.parent.right) {
                        node = node.parent
                        rotate_left(node)
                    }
                    node.parent.set_black()
                    grandparent.set_red()
                    rotate_right(grandparent)
                }
            } else {
                // Mirror case
                RBNode uncle = grandparent.left
                
                if(uncle != null && uncle.is_red()) {
                    node.parent.set_black()
                    uncle.set_black()
                    grandparent.set_red()
                    node = grandparent
                } else {
                    if(node == node.parent.left) {
                        node = node.parent
                        rotate_right(node)
                    }
                    node.parent.set_black()
                    grandparent.set_red()
                    rotate_left(grandparent)
                }
            }
        }
        
        root.set_black()
    }
    
    fun rotate_left(RBNode node) {
        RBNode right_child = node.right
        node.right = right_child.left
        
        if(right_child.left != null) {
            right_child.left.parent = node
        }
        
        right_child.parent = node.parent
        
        if(node.parent == null) {
            root = right_child
        } else if(node == node.parent.left) {
            node.parent.left = right_child
        } else {
            node.parent.right = right_child
        }
        
        right_child.left = node
        node.parent = right_child
    }
    
    fun rotate_right(RBNode node) {
        RBNode left_child = node.left
        node.left = left_child.right
        
        if(left_child.right != null) {
            left_child.right.parent = node
        }
        
        left_child.parent = node.parent
        
        if(node.parent == null) {
            root = left_child
        } else if(node == node.parent.right) {
            node.parent.right = left_child
        } else {
            node.parent.left = left_child
        }
        
        left_child.right = node
        node.parent = left_child
    }
    
    fun inorder_traversal() {
        inorder_helper(root)
        print("")
    }
    
    fun inorder_helper(RBNode node) {
        if(node != null) {
            inorder_helper(node.left)
            print(node.data + "(" + node.color + ") ")
            inorder_helper(node.right)
        }
    }
    
    fun search(int value) {
        RBNode current = root
        while(current != null) {
            if(value == current.data) return true
            if(value < current.data) {
                current = current.left
            } else {
                current = current.right
            }
        }
        return false
    }
}

// Demonstrate Red-Black Tree
print("=== Red-Black Tree Demo ===")
RedBlackTree rbt = RedBlackTree()

list values_to_insert = [10, 20, 30, 15, 25, 5, 1, 35]
for(i=0; i<length(values_to_insert); i++) {
    rbt.insert(values_to_insert[i])
    print("Inserted " + values_to_insert[i])
}

print("Inorder traversal (showing colors):")
rbt.inorder_traversal()

print("Search for 15: " + (rbt.search(15) ? "Found" : "Not found"))
print("Search for 50: " + (rbt.search(50) ? "Found" : "Not found"))
print("")

// 5. Advanced Algorithm - A* Pathfinding
fun AStarPathfinder(int width, int height) {
    list grid = []
    int grid_width = width
    int grid_height = height
    
    // Initialize grid
    for(i=0; i<height; i++) {
        list row = []
        for(j=0; j<width; j++) {
            row.push(0)  // 0 = walkable, 1 = obstacle
        }
        grid.push(row)
    }
    
    fun set_obstacle(int x, int y) {
        if(x >= 0 && x < grid_width && y >= 0 && y < grid_height) {
            grid[y][x] = 1
        }
    }
    
    fun heuristic(int x1, int y1, int x2, int y2) {
        // Manhattan distance
        return abs(x1 - x2) + abs(y1 - y2)
    }
    
    fun find_path(int start_x, int start_y, int end_x, int end_y) {
        list open_set = []
        list closed_set = []
        
        // Node structure: [x, y, g_cost, h_cost, f_cost, parent_x, parent_y]
        list start_node = [start_x, start_y, 0, 0, 0, -1, -1]
        start_node[3] = heuristic(start_x, start_y, end_x, end_y)  // h_cost
        start_node[4] = start_node[2] + start_node[3]  // f_cost
        
        open_set.push(start_node)
        
        while(length(open_set) > 0) {
            // Find node with lowest f_cost
            int current_index = 0
            for(i=1; i<length(open_set); i++) {
                if(open_set[i][4] < open_set[current_index][4]) {
                    current_index = i
                }
            }
            
            list current = open_set[current_index]

            // Workaround for open_set.remove(current_index)
            list new_open_set = []
            for(i=0; i<length(open_set); i++) {
                if(i != current_index) {
                    new_open_set.push(open_set[i])
                }
            }
            open_set = new_open_set
            
            closed_set.push(current)
            
            // Check if we reached the goal
            if(current[0] == end_x && current[1] == end_y) {
                return reconstruct_path(closed_set, current)
            }
            
            // Check neighbors
            list neighbors = [
                [current[0]+1, current[1]],    // Right
                [current[0]-1, current[1]],    // Left
                [current[0], current[1]+1],    // Down
                [current[0], current[1]-1]     // Up
            ]
            
            for(i=0; i<length(neighbors); i++) {
                int nx = neighbors[i][0]
                int ny = neighbors[i][1]
                
                // Check bounds and obstacles
                if(nx < 0 || nx >= grid_width || ny < 0 || ny >= grid_height) continue
                if(grid[ny][nx] == 1) continue  // Obstacle
                
                // Check if in closed set
                if(in_closed_set(closed_set, nx, ny)) continue
                
                int tentative_g = current[2] + 1
                list neighbor_node = find_in_open_set(open_set, nx, ny)
                
                if(neighbor_node == null) {
                    // New node
                    int h_cost = heuristic(nx, ny, end_x, end_y)
                    list new_node = [nx, ny, tentative_g, h_cost, tentative_g + h_cost, current[0], current[1]]
                    open_set.push(new_node)
                } else if(tentative_g < neighbor_node[2]) {
                    // Better path found
                    neighbor_node[2] = tentative_g
                    neighbor_node[4] = tentative_g + neighbor_node[3]
                    neighbor_node[5] = current[0]
                    neighbor_node[6] = current[1]
                }
            }
        }
        
        return null  // No path found
    }
    
    fun reconstruct_path(list closed_set, list end_node) {
        list path = []
        list current = end_node
        
        while(current[5] != -1 && current[6] != -1) {
            path.insert(0, [current[0], current[1]])
            
            // Find parent
            for(i=0; i<length(closed_set); i++) {
                if(closed_set[i][0] == current[5] && closed_set[i][1] == current[6]) {
                    current = closed_set[i]
                    break
                }
            }
        }
        
        path.insert(0, [current[0], current[1]])  // Add start
        return path
    }
    
    fun in_closed_set(list closed_set, int x, int y) {
        for(i=0; i<length(closed_set); i++) {
            if(closed_set[i][0] == x && closed_set[i][1] == y) return true
        }
        return false
    }
    
    fun find_in_open_set(list open_set, int x, int y) {
        for(i=0; i<length(open_set); i++) {
            if(open_set[i][0] == x && open_set[i][1] == y) return open_set[i]
        }
        return null
    }
}

// Demonstrate A* pathfinding
print("=== A* Pathfinding Demo ===")
AStarPathfinder pathfinder = AStarPathfinder(10, 10)

// Add some obstacles
pathfinder.set_obstacle(3, 3)
pathfinder.set_obstacle(3, 4)
pathfinder.set_obstacle(3, 5)
pathfinder.set_obstacle(4, 3)
pathfinder.set_obstacle(5, 3)

list path = pathfinder.find_path(0, 0, 8, 8)

if(path != null) {
    print("Path found with " + length(path) + " steps:")
    for(i=0; i<length(path); i++) {
        print("(" + path[i][0] + ", " + path[i][1] + ")")
    }
} else {
    print("No path found!")
}

print("")

// Helper functions
fun array_to_string(list arr) {
    string result = "["
    for(i=0; i<length(arr); i++) {
        result += arr[i]
        if(i < length(arr) - 1) result += ", "
    }
    result += "]"
    return result
}

fun abs(int x) {
    return x < 0 ? -x : x
}

print("🎯 Advanced algorithms demonstration complete! 🎯") 