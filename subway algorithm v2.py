import math, csv, random, time

def clear_results_file():
    results = open(r".vscode\tspsubway\musical-trains\tsp results.txt", "w")
    results.write("")
    results.close()

class Node:
    def __init__(self, name, kind, delay, visits):
        self.name = name
        self.kind = kind
        self.delay = delay
        self.visits = visits
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
    with open(r".vscode\tspsubway\musical-trains\subway 1\nodes.txt", newline = "") as f:
        file_test_reader = csv.reader(f, delimiter = ",", skipinitialspace = True)
        for f in file_test_reader:
            tuple(f)
            nodes_raw.append(f)
    global nodes
    nodes = []
    for node in nodes_raw:
        r = Node(node[0], node[1], node[2], 0)
        for i in range(3, len(node)):
            r.lines.append(node[i])
        nodes.append(r)
    lines_raw = []
    with open(r".vscode\tspsubway\musical-trains\subway 1\lines.txt", newline = "") as f:
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
    with open(r".vscode\tspsubway\musical-trains\subway 1\paths.txt", newline = "") as f:
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

def run_test():
    for item in dead_ends:
        run_time = 0
        route = []
        for node in nodes:
            node.visits = 0
        previous_node = item
        current_node = item
        current_line = random.choice(current_node.lines)
        for line in lines:
            if line.name == current_line:
                current_line = line
        transfer = False
        route.append("s: " + current_line.name)
        node_least_visits = 0
        # print("Current run time:", run_time)
        # print("Previous:", previous_node, "current:", current_node)
        # print("Current line:", current_line)
        while True:
            route.append(current_node.name)
            # print("Visiting", current_node, " with prior visits", current_node.visits)
            for line in lines:
                line_nodes_tmp = []
                for item in line.nodes:
                    for node in nodes:
                        if node.name == item:
                            line_nodes_tmp.append(node)
                line.zeros = sum(n.visits == 0 for n in line_nodes_tmp)
            if current_node.kind == "hub" or current_node.kind == "dead":
                if current_line.zeros == 0:
                    # print("   choosing least visited line: line exhausted")
                    available_lines = []
                    for item in current_node.lines:
                        for line in lines:
                            if line.name == item:
                                available_lines.append(line)
                    random.shuffle(available_lines)
                    available_lines = sorted(available_lines, key=lambda line: line.zeros)
                    # print(available_lines)
                    next_line = available_lines[-1]
                    # print(next_line)
                elif current_line.zeros > 0 and current_line.zeros < len(current_line.nodes) * 0.5:
                    if random.random() < 0.5:
                        # print("   choosing least visited line: near end, high probability")
                        available_lines = []
                        for item in current_node.lines:
                            for line in lines:
                                if line.name == item:
                                    available_lines.append(line)
                        random.shuffle(available_lines)
                        available_lines = sorted(available_lines, key=lambda line: line.zeros)
                        # print(available_lines)
                        next_line = available_lines[-1]
                        # print(next_line)
                    else:
                        # print("   choosing current line: near end, low probability")
                        next_line = current_line
                else:
                    if random.random() < 0.2:
                        # print("   choosing least visited line: near beginning, low probability")
                        available_lines = []
                        for item in current_node.lines:
                            for line in lines:
                                if line.name == item:
                                    available_lines.append(line)
                        random.shuffle(available_lines)
                        available_lines = sorted(available_lines, key=lambda line: line.zeros)
                        # print(available_lines)
                        next_line = available_lines[-1]
                        # print(next_line)
                    else:
                        # print("   choosing current line: near beginning, high probability")
                        next_line = current_line
            else:
                next_line = current_line
            # print("   now on", next_line.name, "line with", next_line.zeros, "zeros")
            if next_line != current_line:
                transfer = True
            else:
                transfer = False
            next_adjacent = []
            if next_line.nodes.index(current_node.name) > 0:
                s_b = next_line.nodes[next_line.nodes.index(current_node.name) - 1]
                for node in nodes:
                    if node.name == s_b:
                        s_b = node
                next_adjacent.append(s_b)
            try:
                s_f = next_line.nodes[next_line.nodes.index(current_node.name) + 1]
                for node in nodes:
                    if node.name == s_f:
                        s_f = node
                next_adjacent.append(s_f)
            except IndexError:
                pass
            next_adjacent = sorted(next_adjacent, key=lambda node: node.visits)
            # print("   unfiltered adjacent nodes:", next_adjacent)
            for node in next_adjacent:
                if node == previous_node:
                    if len(next_adjacent) > 1:
                        next_adjacent.remove(node)
                        # print("   removing node just visited from next_adjacent")
                        continue
                    else:
                        # print("   cannot remove only node from next_adjacent")
                        continue
            # print("   filtered adjacent nodes:", next_adjacent)
            random.shuffle(next_adjacent)
            next_node = next_adjacent[0]
            if transfer == True:
                for path in paths:
                    if path.start == current_node.name and path.end == next_node.name:
                        delay = float(path.delay) + float(current_node.delay)
                        # print("   changing lines, added transfer penalty")
                        route.append("t: " + next_line.name)
            else:
                for path in paths:
                    if path.start == current_node.name and path.end == next_node.name:
                        delay = float(path.delay)
                        # print("   staying on current line")
            # print("   time to next station:", delay)
            # print("   previous:", previous_node, "current:", current_node, "next:", next_node)
            current_node.visits += 1
            previous_node = current_node
            current_node = next_node
            current_line = next_line
            node_least_visited = min(nodes, key=lambda node: node.visits)
            node_least_visits = node_least_visited.visits
            if node_least_visits != 0:
                break
            run_time += delay
            # print("Current run time:", run_time)
            # time.sleep(0.01)
        results = " " + str(run_time) + " time with path: " + str(route) + "\n"
        with open(r".vscode\tspsubway\musical-trains\tsp results.txt", "a") as results_file:
            results_file.write(results)
        # print(run_time)

def search():
    with open(r".vscode\tspsubway\musical-trains\tsp results.txt", "r") as results_file:
        iterations_list = []
        for line in results_file:
            run_time = line[:line.find("time")]
            route = line[line.find("time"):]
            run_time = float(run_time)
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