# Дістаємо з файлу graph.py наші замудрені класи
from graph import GraphMatrix, GraphList

# Модуль, щоб ми могли оцінити час роботи алгоритму
import time

# Python не підтримує за замовчуванням більше ніж 995 рекурсій функції,
# тож ми це грубо змінюєм, на випадок, якщо розміри графу будуть екстра-великі :)
import sys
RECURSIONS = 10000
sys.setrecursionlimit(RECURSIONS)

def show_component(component, number: int = 0) -> None:
    """
     Функція, що виводить в термінал всі вершини, що знаходяться в компоненті
     Бере для себе два аргументи:
    :param number: номер компоненти, просто для краси
    :param component: сама компонента, яку будем виводити
    """
    print(f"Компонента №{number}: {', '.join([str(i) for i in component])}")

def kosaraju_matrix(graph: 'GraphMatrix') -> tuple:
    """
    Алгоритм Косорайю, що працює на основі графу представленого у вигляді матриці суміжності
    Приймає один аргумент:
    :param graph: представник класу GraphMatrix, з яким ми і будемо працювати

    Функція повертає всі найбільші компоненти сильної зв'язності графа, а також час виконання алгоритму
    """

    # Витягуємо з нашого представника класу всі необхідні дані
    the_graph = graph.graph
    reverse_graph = graph.reverse().graph
    vertices = graph.vertices

    # Для роботи алгоритму робимо кілька необхідних списків
    used = [False for _ in range(0, vertices)]
    order, component, components = [], [], []


    def dfs_1(vertice_1: int) -> None:
        used[vertice_1] = True
        for vertice_ in range(0, vertices):
            if the_graph[vertice_1][vertice_] and not used[vertice_]:
                dfs_1(vertice_)
        order.append(vertice_1)

    def dfs_2(vertice_1: int) -> None:
        used[vertice_1] = True
        component.append(vertice_1+1)
        for vertice_ in range(0, vertices):
            if reverse_graph[vertice_1][vertice_] and not used[vertice_]:
                dfs_2(vertice_)

    # Саме тут починається обрахунок часу алгоритму
    time_start = time.perf_counter()

    for vertice in range(0, vertices):
        if not used[vertice]:
            dfs_1(vertice)

    used = [False for _ in range(0, vertices)]

    for vertice in range(0, vertices):
        vertice_2 = order[vertices-1-vertice]
        if not used[vertice_2]:
            dfs_2(vertice_2)
            components.append(component.copy())
            component.clear()

    # Саме тут завершується обрахунок часу алгоритму
    time_end = time.perf_counter()

    return components, round(time_end-time_start, 6)

def kosaraju_list(graph: 'GraphList') -> tuple:
    """
        Алгоритм Косорайю, що працює на основі графу представленого у вигляді списку суміжності

        Приймає один аргумент:
        :param graph: представник класу GraphList, з яким ми і будемо працювати

        Функція повертає всі найбільші компоненти сильної зв'язності графа, а також час виконання алгоритму
    """
    the_graph, reverse_graph, vertices = graph.graph, graph.reverse().graph, graph.vertices
    used = [False for _ in range(0, vertices)]
    order, component, components = [], [], []

    def dfs_1(vertice_1: int) -> None:
        used[vertice_1] = True
        for vertice_ in the_graph[vertice_1]:
            if not used[vertice_]:
                dfs_1(vertice_)
        order.append(vertice_1)

    def dfs_2(vertice_1: int) -> None:
        used[vertice_1] = True
        component.append(vertice_1+1)
        for vertice_ in reverse_graph[vertice_1]:
            if not used[vertice_]:
                dfs_2(vertice_)

    # Саме звідси я вирішив почати відрахунок часу алгоритму
    time_start = time.perf_counter()
    for vertice in range(0, vertices):
        if not used[vertice]:
            dfs_1(vertice)

    used = [False for _ in range(0, vertices)]

    for vertice in range(0, vertices):
        vertice_2 = order[vertices-1-vertice]
        if not used[vertice_2]:
            dfs_2(vertice_2)
            components.append(component.copy())
            component.clear()

    # Саме тут завершується час обрахунку алгоритму
    time_end = time.perf_counter()
    return components, round(time_end-time_start, 6)
