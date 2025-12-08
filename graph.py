from random import random
import numpy as np

class BasicGraph:
    """
    Клас, що реалізовує базові характеристики графу.
    Є основою для класів GraphList та GraphMatrix
    """
    def __init__(self, vertices: int = 0, edges: int = 0, probability: float = 0.5, graph = None):
        """
        Магічний метод
        Створює змінні в класі BasicGraph
        
        Приймає 3 аргументи:
        :param vertices: кількість вершин у графа, які пронумеровані від 1 до vertices, за замовчуванням = 0
        :param edges: кількість ребер у графа, за замовчуванням = 0
        :param probability: ймовірність існування ребра між двома вершинами, за замовчуванням = 0
        """
        self.vertices = vertices
        self.edges = edges
        self.probability = probability

        if graph:
            self.graph = graph
        else:
            self.graph = []

    def __str__(self) -> str:
        """
            Повертає текст довгої інформації про граф:
            1. Кількість вершин
            2. Кількість ребер
            3. Яка була ймовірність існування ребра між вершинами a та b
        """
        if self.edges and self.vertices:
            actual_probability = round(self.edges/(self.vertices*(self.vertices-1))*100,2)
        else:
            actual_probability = 0

        return f'''
        Інформація про граф:
        1) Кількість вершин = {self.vertices}
        2) Кількість ребер = {self.edges}
        3) Очікувана щільність = {self.probability*100}%
        4) Фактична щільність = {actual_probability}%
        5) Модуль різниці очікуваної та фактичної щільності = {round(abs(self.probability*100-actual_probability),2)}%
        '''

class  GraphList(BasicGraph):
    """
        Клас GraphList, що наслідує клас BasicGraph, де граф представлений
        у вигляді списку суміжності з елементами (a, b), що
        означає, що з вершини a є ребро до вершини b
    """
    def generate(self, vertices: int = 100, probability: float = 0.5) -> None:
        """
        Метод, що генерує граф, як список суміжності

        Приймає два аргументи:
        :param vertices: кількість вершин, за замовчуванням = 100
        :param probability: ймовірність того, що в списку суміжності
            буде впорядкована пара (a, b), за замовчуванням = 0.5
        """
        self.graph = [[] for _ in range(0, vertices)]
        self.edges = 0
        for row in range(0, vertices):
            for column in range(0, vertices):
                if row == column:
                    continue
                if random() <= probability:
                    self.graph[row].append(column)
                    self.edges += 1
        self.vertices = vertices
        self.probability = probability

    def show(self) -> None:
        """
        Метод, що виводить в консоль список суміжносні
        """
        print(self.graph)

    def reverse(self) -> 'GraphList':
        reverse_list = [[] for _ in range(0, self.vertices)]
        for a in range(0, self.vertices):
            for b in self.graph[a]:
                reverse_list[b].append(a)
        return GraphList(self.vertices, self.edges, self.probability, reverse_list)

    def display(self) -> None:
        """
        Метод, що виводить в консоль інформацію про всі з'єднання графу
        """
        for vertice in range(0, self.vertices):
            if self.graph[vertice]:
                print(f"Вершина {vertice + 1} з'єднана з вершинами {', '.join([str(i+1) for i in self.graph[vertice]])}")
            else:
                print(f"Вершина {vertice + 1} ні з ким не з'єднана")

    def transform_to_matrix(self) -> 'GraphMatrix':
        """
        Метод, що перетворює клас зі списком суміжності на клас з матрицею суміжності
        """
        graph_matrix = [[False for _ in range(0, self.vertices)] for _ in range(0, self.vertices)]
        for a in range(0, self.vertices):
            for b in self.graph[a]:
                graph_matrix[a][b] = True

        return GraphMatrix(self.vertices, self.edges, self.probability, graph_matrix)

    def __add__(self, edge: tuple):
        """
        Магічний метод, що дозволяє додавати до графу нове ребро,
        при умові, що існують такі вершини у графі, і такого ребра ще немає

        Приймає один аргумент edge
        :param edge: це впорядкована пара (a, b)

        Повертає клас GraphList, де додалось ребро edge
        """
        if not isinstance(edge, tuple):
            return NotImplemented
        a,b = [i-1 for i in edge]
        if 0 <= a < self.vertices and 0 <= b < self.vertices:
            if b in self.graph[a]:
                print("Таке ребро вже є у графі!")
                return NotImplemented
            else:
                self.graph[a].append(b)
            return GraphList(self.vertices, self.edges, self.probability, self.graph)
        print("Таких вершин/Такої вершини немає у графі!")
        return NotImplemented

    def __repr__(self) -> str:
        """
        Магічний метод
        Повертає текст стислої інформації про граф
        """
        return f'''GraphList(
            graph={self.graph[0]}...{self.graph[99]}
            vertices={self.vertices}
            edges={self.edges}
            probability={self.probability}
        )'''

    def __str__(self):
        base = super().__str__()
        return f'''
        {base.strip()}
        6) Структура даних для графу - список суміжносні'''

class GraphMatrix(BasicGraph):
    """
    Клас GraphMatrix, що наслідує клас BasicGraph, де
    граф представлений у вигляді матриці суміжності
    """
    def generate(self, vertices: int = 100, probability: float = 0.5) -> None:
        """
        Метод, що генерує граф, як матрицю суміжності

        Приймає два аргументи:
        :param vertices: кількість вершин, за замовчуванням = 100
        :param probability: ймовірність того, що в матриці суміжності
            буде існувати ребро між вершинами a та b, за замовчуванням = 0.5
        """
        for row in range(0, vertices):
            self.graph.append([False for _ in range(0, vertices)])
            for column in range(0, vertices):
                if row == column:
                    continue
                if random() <= probability:
                    self.graph[row][column] = True
                    self.edges += 1

        self.vertices = vertices
        self.probability = probability

    def show(self) -> None:
        """
        Метод, що виводить в термінал матрицю суміжності
        """
        for row in self.graph:
            print(row)

    def reverse(self) -> 'GraphMatrix':
        """
        Метод, що повертає транспонований (обернений) граф до вже існуючого
        """
        reverse_matrix = [[False for _ in range(self.vertices)] for _ in range(self.vertices)]
        for row in range(0, self.vertices):
            for column in range(0, self.vertices):
                if self.graph[row][column]:
                    reverse_matrix[column][row] = True
        return GraphMatrix(self.vertices, self.edges, self.probability, reverse_matrix)

    def display(self) -> None:
        """
        Метод, що виводить в консоль інформацію про всі ребра графу
        """

        for row in range(0, self.vertices):
            vertices = []
            for column in range(0, self.vertices):
                if self.graph[row][column]:
                    vertices.append(column + 1)
            if vertices:
                print(f"Вершина {row + 1} з'єднана з вершинами {', '.join([str(i) for i in vertices])}")
            else:
                print(f"Вершина {row + 1} ні з ким не з'єднана")

    def transform_to_list(self) -> 'GraphList':
        """
        Метод, що перетворює граф зі списком суміжності на граф з матрицею суміжності
        """
        graph_list = [[] for _ in range(self.vertices)]
        for row in range(0, self.vertices):
            for column in range(0, self.vertices):
                if self.graph[row][column]:
                    graph_list[row].append(column)

        return GraphList(self.vertices, self.edges, self.probability, graph_list)

    def __repr__(self) -> str:
        """
        Магічний метод
        Повертає текст стислої інформації про граф
        """

        return f'''GraphMatrix(
            graph=
            {self.graph[0]}
            ...
            {self.graph[-1]},
            vertices={self.vertices},
            edges={self.edges},
            probability={self.probability})'''

    def __add__(self, edge: tuple) -> 'GraphMatrix':
        """
        Магічний метод, що дозволяє додавати до графу нове ребро,
        при умові, що існують такі вершини у графі, і такого ребра ще немає

        Приймає один аргумент edge
        :param edge: це впорядкована пара (a, b)

        Повертає клас GraphMatrix, де додалось ребро edge
        """

        if not isinstance(edge, tuple):
            return NotImplemented
        a,b = [x-1 for x in edge]
        if 0 <= a < self.vertices and 0 <= b < self.vertices:
            if not self.graph[a][b]:
                graph_copy = self.graph.copy()
                graph_copy[a][b] = True
                return GraphMatrix(self.vertices, self.edges, self.probability, graph_copy)
            else:
                print("Таке ребро вже існує!")
        else:
            print("Таких вершин/Такої вершини немає у графі!")
        return NotImplemented

    def __str__(self):
        base = super().__str__()
        return f'''
        {base.strip()}
        6) Структура даних для графу - матриця суміжності'''
