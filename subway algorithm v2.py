import math, csv, random, time

def clear_results_file():
    results = open(r".vscode\tspsubway\tsp results.txt", "w")
    results.write("")
    results.close()

class Node:
    def __init__(self, name, kind, visits, previous):
        self.name = name
        self.kind = kind
        self.visits = visits
        self.previous = previous
        self.lines = []
    def __repr__(self):
        return f"(node {self.name}: {self.lines}, visits: {self.visits})"

class Line:
    def __init__(self, name, zeros):
        self.name = name
        self.zeros = zeros
        self.nodes = []
    def __repr__(self):
        return f"(line {self.name}: {self.nodes}, zeros: {self.zeros})"

class Path:
    def __init__(self, start, end, delay):
        self.start = start
        self.end = end
        self.delay = delay
    def __repr__(self):
        return f"({self.start} to {self.end}, dist {self.delay})"

def define():
    nodes_raw = []
    with open(r".vscode\tspsubway\subway 1\nodes.txt", newline = "") as f:
            file_test_reader = csv.reader(f, delimiter = ",", skipinitialspace = True)
            for f in file_test_reader:
                tuple(f)
                nodes_raw.append(f)
    global nodes
    nodes = []
    for node in nodes_raw:
        r = Node(node[0], node[1], 0, False)
        for i in range(2, len(node)):
            r.lines.append(node[i])
        nodes.append(r)
    lines_raw = []
    with open(r".vscode\tspsubway\subway 1\lines.txt", newline = "") as f:
            file_test_reader = csv.reader(f, delimiter = ",", skipinitialspace = True)
            for f in file_test_reader:
                tuple(f)
                lines_raw.append(f)
    global lines
    lines = []
    for line in lines_raw:
        l = Line(line[0], 0)
        for i in range(1, len(line)):
            l.nodes.append(line[i])
        l.zeros = len(l.nodes)
        lines.append(l)
    paths_raw = []
    with open(r".vscode\tspsubway\subway 1\paths.txt", newline = "") as f:
            file_test_reader = csv.reader(f, delimiter = ",", skipinitialspace = True)
            for f in file_test_reader:
                tuple(f)
                paths_raw.append(f)
    global paths
    paths = []
    for path in paths_raw:
        p = Path(path[0], path[1], path[2])
        paths.append(p)
    global dead_ends
    dead_ends = []
    for node in nodes:
        if node.kind == "dead":
            dead_ends.append(node)

def next(Node):
    global current_node
    global next_line
    global transfer
    current_node = Node
    Node.previous = True
    Node.visits += 1
    route.append(Node.name)
    for line in lines:
        line_nodes_tmp = []
        for item in line.nodes:
            for node in nodes:
                if node.name == item:
                    line_nodes_tmp.append(node)
        line.zeros = sum(n.visits == 0 for n in line_nodes_tmp)
    # print(Node.lines)
    if Node.kind == "dead" or Node.kind == "hub":
        if current_line.zeros == 0:
            # print("   choosing least visited line: line exhausted")
            available_lines = []
            for item in Node.lines:
                for line in lines:
                    if line.name == item:
                        available_lines.append(line)
            random.shuffle(available_lines)
            available_lines = sorted(available_lines, key=lambda line: line.zeros)
            # print(available_lines)
            next_line = available_lines[-1]
            # print(next_line)
            if next_line != current_line:
                transfer = True
            else:
                transfer = False
        elif current_line.zeros > 0 and current_line.zeros < len(current_line.nodes) / 2:
            if random.random() < 0.5:
                # print("   choosing least visited line: probability method")
                available_lines = []
                for item in Node.lines:
                    for line in lines:
                        if line.name == item:
                            available_lines.append(line)
                random.shuffle(available_lines)
                available_lines = sorted(available_lines, key=lambda line: line.zeros)
                # print(available_lines)
                next_line = available_lines[-1]
                # print(next_line)
                if next_line != current_line:
                    transfer = True
                else:
                    transfer = False
            else:
                # print("   choosing current line: probability method")
                next_line = current_line
                transfer = False
        else:
            # print("   choosing current line: economy method")
            next_line = current_line
            transfer = False
    else:
        next_line = current_line
        transfer = False
    # print("   Now on", next_line.name, "line")
    global next_adjacent
    next_adjacent = []
    if next_line.nodes.index(Node.name) > 0:
        s_b = next_line.nodes[next_line.nodes.index(Node.name) - 1]
        for node in nodes:
            if node.name == s_b:
                s_b = node
        next_adjacent.append(s_b)
    try:
        s_f = next_line.nodes[next_line.nodes.index(Node.name) + 1]
        for node in nodes:
            if node.name == s_f:
                s_f = node
        next_adjacent.append(s_f)
    except IndexError:
        pass
    next_adjacent = sorted(next_adjacent, key=lambda node: node.visits)
    # print("   adjacent nodes:", next_adjacent)

def run_test():
    for item in dead_ends:
        global route
        global next_node
        global delay
        global current_line
        global transfer
        run_time = 0
        route = []
        for node in nodes:
            node.visits = 0
        next_node = item
        # print("Visiting", next_node, " with prior visits", next_node.visits)
        current_line = random.choice(next_node.lines)
        for line in lines:
            if line.name == current_line:
                current_line = line
        next(next_node)
        transfer = False
        node_least_visits = 0
        while node_least_visits == 0:
            for s_i in next_adjacent:
                if s_i.previous == True:
                    s_i.previous = False
                    if len(next_adjacent) > 1:
                        next_adjacent.remove(s_i)
                        # print("   Removing node just visited from next_adjacent")
                        continue
                    else:
                        # print("   Cannot remove only node from next_adjacent")
                        continue
            # print("   adjacent nodes:", next_adjacent)
            next_node = next_adjacent[0]
            if transfer == True:
                for path in paths:
                    if path.start == current_node.name and path.end == next_node.name:
                        delay = float(path.delay) + 1
                        # print("   Changing lines, added transfer penalty")
            else:
                for path in paths:
                    if path.start == current_node.name and path.end == next_node.name:
                        delay = float(path.delay)
                        # print("   Staying on current line")
            # print("   Time to next station:", delay)
            current_line = next_line
            run_time += delay
            # print("Visiting", next_node, " with prior visits", next_node.visits)
            # print("   Current run time:", run_time)
            next(next_node)
            node_least_visited = min(nodes, key=lambda node: node.visits)
            node_least_visits = node_least_visited.visits
            # time.sleep(0.05)
        results = str(run_time) + " time with path: " + str(route) + "\n"
        with open(r".vscode\tspsubway\tsp results.txt", "a") as results_file:
            results_file.write(results)
    

def search():
    with open(r".vscode\tspsubway\tsp results.txt", "r") as results_file:
        iterations_list = []
        for line in results_file:
            run_time = line[:line.find("time")]
            route = line[line.find("time"):]
            run_time = float(run_time)
            # except ValueError:
            #     print("value error")
            iterations_list.append((run_time, route))
    minimum_route = min(iterations_list, key=lambda x: x[0])
    print(minimum_route[0], minimum_route[1])

def start_program():
    clear_results_file()
    n = int(input("Enter number of full iterations: "))
    for i in range(n):
        define()
        run_test()
        print(n - i)
    search()

start_program()
