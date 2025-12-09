import matplotlib.pyplot as plt
from graph import GraphList, GraphMatrix
from algorithms import kosaraju_list, kosaraju_matrix
import pandas as pd

SIZES = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
DENSITIES = [0.1, 0.3, 0.5, 0.7, 0.9]
REPEATS = 1000

def experiment():
    """
    Основна функція, що запускає всі експерименти та збирає дані.
    Повертає словник з даними для візуалізації
    """
    results = {
        'List': {d: [] for d in DENSITIES},
        'Matrix': {d: [] for d in DENSITIES}
    }
    for density in DENSITIES:
        for size in SIZES:
            # list
            total_time = 0
            for _ in range(REPEATS):
                g_list = GraphList()
                g_list.generate(vertices=size, probability=density)

                _, time = kosaraju_list(g_list)
                total_time += time
                
            avg_time = total_time / REPEATS * 1000
            results['List'][density].append(avg_time)

            # matrix
            total_time = 0
            for _ in range(REPEATS):
                g_matrix = GraphMatrix()
                g_matrix.generate(vertices=size, probability=density)

                _, time = kosaraju_matrix(g_matrix)
                total_time += time

            avg_time_matrix = total_time / REPEATS * 1000
            results['Matrix'][density].append(avg_time_matrix)

    return results

# використовувався ші, для консультації з документацією matplotlib
def visual(results):
    """
    Функція для візуалізації даних
    """
    _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))

    all_times = []
    for method in results:
        for density in results[method]:
            all_times.extend(results[method][density])

    global_max_time = max(all_times)
    y_limit = global_max_time * 1.1

    # GraphList
    for density in DENSITIES:
        ax1.plot(SIZES, results['List'][density], marker='o', label=f'Щільність {density}')

    x_label_text = "Кількість вершин N"
    y_label_text = "Час t, мілісекунди"
    ax1.set_title("Час виконання алгоритму зі списками суміжності")
    ax1.set_xlabel(x_label_text)
    ax1.set_ylabel(y_label_text)
    ax1.set_ylim(0, y_limit)
    ax1.legend()
    ax1.grid(True)

    # GraphMatrix
    for density in DENSITIES:
        ax2.plot(SIZES, results['Matrix'][density], marker='s', label=f'Щільність {density}')

    ax2.set_title("Час виконання алгоритму з матрицями суміжності")
    ax2.set_xlabel(x_label_text)
    ax2.set_ylabel(y_label_text)
    ax2.set_ylim(0, y_limit)
    ax2.legend()
    ax2.grid(True)

    # List vs Matrix
    ax3.plot(SIZES, results['List'][0.5], marker='o', label='Списки', color='blue')
    ax3.plot(SIZES, results['Matrix'][0.5], marker='s', label='Матриці', color='red')

    ax3.set_title("Списки vs Матриці (Щільність 0.5)")
    ax3.set_xlabel(x_label_text)
    ax3.set_ylabel(y_label_text)
    ax3.set_ylim(0, y_limit)
    ax3.legend()
    ax3.grid(True)

    plt.tight_layout()
    plt.show()

# використовувався ші для консультації того, як перевести дані в ексель табличку, щоб потім було комфортно її
# вставити в роботу
def save_to_excel(results, filename="kosaraju_results.xlsx"):
    """
    Зберігає результати експериментів у Excel файл.
    """
    data_rows = []

    for i, size in enumerate(SIZES):
        row = {'Кількість вершин': size}

        for density in DENSITIES:
            time_list = results['List'][density][i]
            time_matrix = results['Matrix'][density][i]

            row[f'List ({density})'] = time_list
            row[f'Matrix ({density})'] = time_matrix

        data_rows.append(row)

    df = pd.DataFrame(data_rows)

    df = df.round(4)

    df.to_excel(filename, index=False)

if __name__ == '__main__':
    data = experiment()
    save_to_excel(data)
    visual(data)