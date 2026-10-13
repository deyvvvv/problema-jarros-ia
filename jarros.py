import time
from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.children = []

    def get_path(self):
        path = []
        curr = self
        while curr:
            path.append((curr.action, curr.state))
            curr = curr.parent
        return path[::-1]


def get_successors(state):
    j4, j3 = state
    successors = []
    
    # 1. Encher J4
    if j4 < 4:
        successors.append(("Encher Jarro 4L", (4, j3)))
    # 2. Encher J3
    if j3 < 3:
        successors.append(("Encher Jarro 3L", (j4, 3)))
    # 3. Esvaziar J4
    if j4 > 0:
        successors.append(("Esvaziar Jarro 4L", (0, j3)))
    # 4. Esvaziar J3
    if j3 > 0:
        successors.append(("Esvaziar Jarro 3L", (j4, 0)))
    # 5. Despejar J4 em J3
    if j4 > 0 and j3 < 3:
        amount = min(j4, 3 - j3)
        successors.append(("Passar J4 para J3", (j4 - amount, j3 + amount)))
    # 6. Despejar J3 em J4
    if j3 > 0 and j4 < 4:
        amount = min(j3, 4 - j4)
        successors.append(("Passar J3 para J4", (j4 + amount, j3 - amount)))

    return successors


def is_goal(state):
    return state[0] == 2 or state[1] == 2


# Busca em Largura (BFS) 
def bfs(initial_state):
    start_time = time.perf_counter()
    root = Node(initial_state)
    if is_goal(initial_state):
        return root, root, 1, time.perf_counter() - start_time

    frontier = deque([root])
    visited = {initial_state}
    nodes_expanded = 0

    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1

        for action, next_state in get_successors(node.state):
            child = Node(next_state, parent=node, action=action, depth=node.depth + 1)
            node.children.append(child)

            if is_goal(next_state):
                elapsed_time = time.perf_counter() - start_time
                return root, child, nodes_expanded, elapsed_time

            if next_state not in visited:
                visited.add(next_state)
                frontier.append(child)

    return root, None, nodes_expanded, time.perf_counter() - start_time


# Busca em Profundidade (DFS)
def dfs(initial_state):
    start_time = time.perf_counter()
    root = Node(initial_state)
    if is_goal(initial_state):
        return root, root, 1, time.perf_counter() - start_time

    frontier = [root]
    visited = {initial_state}
    nodes_expanded = 0

    while frontier:
        node = frontier.pop()
        nodes_expanded += 1

        if is_goal(node.state):
            elapsed_time = time.perf_counter() - start_time
            return root, node, nodes_expanded, elapsed_time

        for action, next_state in get_successors(node.state):
            if next_state not in visited:
                visited.add(next_state)
                child = Node(next_state, parent=node, action=action, depth=node.depth + 1)
                node.children.append(child)
                frontier.append(child)

    return root, None, nodes_expanded, time.perf_counter() - start_time


# Busca com Aprofundamento Iterativo (IDS) 
def iddfs(initial_state):
    start_time = time.perf_counter()
    nodes_expanded = 0

    def dls(node, limit, visited_in_path):
        nonlocal nodes_expanded
        nodes_expanded += 1

        if is_goal(node.state):
            return node

        if limit <= 0:
            return None

        for action, next_state in get_successors(node.state):
            if next_state not in visited_in_path:
                child = Node(next_state, parent=node, action=action, depth=node.depth + 1)
                node.children.append(child)
                result = dls(child, limit - 1, visited_in_path | {next_state})
                if result is not None:
                    return result
        return None

    depth = 0
    while True:
        root = Node(initial_state)
        sol = dls(root, depth, {initial_state})
        if sol is not None:
            elapsed_time = time.perf_counter() - start_time
            return root, sol, nodes_expanded, elapsed_time
        depth += 1


def print_tree(node, prefix="", is_last=True, solution_path_set=set()):
    is_in_path = node in solution_path_set
    marker = "  [SOLUÇÃO]" if is_in_path else ""
    act_str = f" ({node.action})" if node.action else " (Início)"
    print(f"{prefix}{'└── ' if is_last else '├── '}{node.state}{act_str}{marker}")

    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node.children):
        print_tree(child, child_prefix, i == len(node.children) - 1, solution_path_set)


def get_nodes_in_path(solution_node):
    nodes = set()
    curr = solution_node
    while curr:
        nodes.add(curr)
        curr = curr.parent
    return nodes


def run():
    initial_state = (0, 0)
    algorithms = [("Busca em Largura (BFS)", bfs),
                  ("Busca em Profundidade (DFS)", dfs),
                  ("Aprofundamento Iterativo (IDS)", iddfs)]

    print("=" * 60)
    print(" RESOLUÇÃO DO PROBLEMA DOS JARROS D'ÁGUA")
    print("=" * 60)

    for name, alg in algorithms:
        root, sol, nodes_exp, exec_time = alg(initial_state)
        path = sol.get_path() if sol else []

        print(f"\n>>> ALGORITMO: {name} <<<")
        print(f"- Nos Expandidos/Visitados: {nodes_exp}")
        print(f"- Passos da Solução: {len(path) - 1}")
        print(f"- Tempo de Execucao: {exec_time * 1000:.4f} ms")
        print("\nCaminho Encontrado:")
        for step, (act, st) in enumerate(path):
            if step == 0:
                print(f"  Passo {step}: Estado Inicial {st}")
            else:
                print(f"  Passo {step}: {act} -> Estado {st}")

        print("\nÁrvore de Busca Gerada (Com destaques da solução):")
        sol_set = get_nodes_in_path(sol) if sol else set()
        print_tree(root, solution_path_set=sol_set)
        print("-" * 60)

if __name__ == "__main__":
    run()