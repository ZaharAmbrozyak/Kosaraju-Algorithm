# скрипт, якій показує, в чому суть алгоритму
# повністю згенерований штучним інтелектом і потрібен лише для того, щоб показати приклад графу з чотирма
# сильно зв'язними компонентами. Не використовується в іншах частинах проєкту

import networkx as nx
import matplotlib.pyplot as plt
import random
from graph import GraphList
from algorithms import kosaraju_list


def create_nice_scc_graph(total_vertices=20, num_clusters=4):
    g = GraphList(total_vertices)
    g.graph = [[] for _ in range(total_vertices)]
    g.edges = 0

    all_nodes = list(range(total_vertices))
    cluster_size = total_vertices // num_clusters
    clusters = []
    for i in range(num_clusters):
        start = i * cluster_size
        end = (i + 1) * cluster_size if i != num_clusters - 1 else total_vertices
        clusters.append(all_nodes[start:end])

    for cluster in clusters:
        for i in range(len(cluster)):
            u = cluster[i]
            v = cluster[(i + 1) % len(cluster)]
            g.graph[u].append(v)
            g.edges += 1

        for _ in range(len(cluster)):
            u = random.choice(cluster)
            v = random.choice(cluster)
            if u != v and v not in g.graph[u]:
                g.graph[u].append(v)
                g.edges += 1

    for i in range(num_clusters - 1):
        current_cluster = clusters[i]
        next_cluster = clusters[i + 1]

        num_bridges = random.randint(1, 2)
        for _ in range(num_bridges):
            u = random.choice(current_cluster)
            v = random.choice(next_cluster)
            if v not in g.graph[u]:
                g.graph[u].append(v)
                g.edges += 1

    g.vertices = total_vertices
    return g


def get_distinct_colors(n):
    import matplotlib.cm as cm
    import numpy as np
    colors = cm.rainbow(np.linspace(0, 1, n))
    hex_colors = []
    for c in colors:
        hex_colors.append('#%02x%02x%02x' % (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)))
    return hex_colors


def visualize_graph(custom_graph, components, filename="graph_scc.png"):
    G = nx.DiGraph()
    for u in range(custom_graph.vertices):
        G.add_node(u + 1)
        for v in custom_graph.graph[u]:
            G.add_edge(u + 1, v + 1)

    colors_palette = get_distinct_colors(len(components))
    color_map = {}
    for idx, component in enumerate(components):
        for node in component:
            color_map[node] = colors_palette[idx]
    final_colors = [color_map.get(node, '#000000') for node in G.nodes()]

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color=final_colors, node_size=600, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='gray',
                           arrowstyle='-|>', arrowsize=20,
                           connectionstyle='arc3, rad=0.1')

    plt.title("Візуалізація Сильно Зв'язних Компонент", fontsize=16)
    plt.axis('off')
    plt.tight_layout()

    print(f"Зберігаємо зображення у файл {filename}...")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    my_graph = create_nice_scc_graph(total_vertices=25, num_clusters=4)
    scc_components, time_taken = kosaraju_list(my_graph)
    visualize_graph(my_graph, scc_components)