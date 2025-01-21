import matplotlib.pyplot as plt
import pandas as pd
import os

class CaTopPlotter:
    def __init__(self, core, plotter):
        """
        Initializes the CaPlotter class with the provided plotter and plotter.

        :param plotter: Object that contains profiles and related data.
        :param plotter: Object responsible for managing plot paths.
        """
        self.core = core
        self.plotter = plotter

    def all(self, verbose: str = "y"):
        """
        Plots all profiles stored in the plotter and saves them as PNG files.

        :param verbose: If 'y', 'yes', '1', or 'true', enables verbose output. Default is 'y'.
        """
        is_verbose = verbose.strip().lower() in {"1", "y", "yes", "true"}

        if is_verbose:
            print("Plotting profiles...")

        plots_dir = os.path.join(self.plotter.handler.path, "result/plots")
        os.makedirs(plots_dir, exist_ok=True)

        for key, df in self.plotter.handler.profiles.items():
            try:
                matching_objects = self.plotter.handler.objects.loc[
                    self.plotter.handler.objects['name'].astype(str) == str(key)
                ]
                
                dist_values = {}
                if not matching_objects.empty:
                    dist_values = {
                        idx: (obj_row['dist'], obj_row['object'])  # Сохраняем и дистанцию, и подпись
                        for idx, obj_row in matching_objects.iterrows()
                    }

                plt.figure(figsize=(10, 6))
                
                # Настройки стилей
                line_colors = {'h': '#1f77b4', 'h_sec': '#2ca02c'}  # Цвета линий
                line_styles = {'h': '-.', 'h_sec': '--'}  # Стили линий
                line_widths = {'h': 0.7, 'h_sec': 0.7}  # Ширина линий
                line_labels = {'h': 'Height', 'h_sec': 'Secondary Height'}  # Подписи для легенды
                
                # Настройки точек
                dist_marker_style = 'x'
                dist_marker_color = '#d62728'  # Красный цвет для точек
                text_offset = (5, -10)  # Смещение подписи
                
                for col in ['h', 'h_sec']:
                    if col in df:
                        filtered_data = df[(df['l'] > 0) & (df[col] > 0)]
                
                        # Линия на графике
                        plt.title(f"Профиль № {key}") 
                        plt.plot(
                            filtered_data['l'],
                            filtered_data[col],
                            color=line_colors.get(col, 'black'),
                            linestyle=line_styles.get(col, '-'),
                            linewidth=line_widths.get(col, 0.7),
                            label=line_labels.get(col, col)  # Добавляем подпись для легенды
                        )
                
                        # Добавляем точки для дистанций
                        if col == 'h' and dist_values:
                            for dist, obj_label in dist_values.values():
                                # Найти ближайшее значение высоты
                                closest_row = filtered_data.iloc[(filtered_data['l'] - dist).abs().idxmin()]
                                height = closest_row[col]
                                plt.scatter(
                                    dist,
                                    height,
                                    color=dist_marker_color,
                                    marker=dist_marker_style,
                                    zorder=5
                                )
                                # Подпись точки
                                plt.text(
                                    dist + text_offset[0],
                                    height + text_offset[1],
                                    f"{obj_label}",
                                    fontsize=9,
                                    color='black',  # Подпись черным цветом
                                    ha='center',
                                    va='center',
                                    alpha=0.8
                                )
                
                # Настройки осей
                plt.xlabel("Distance", fontsize=12)
                plt.ylabel("Height", fontsize=12)
                
                # Легенда
                plt.legend(loc='upper right', fontsize=10)  # Легенда в правом верхнем углу
                
                # Общие настройки
                plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
                plt.tight_layout()
                plt.savefig(os.path.join(plots_dir, f"{key}.png"))
                plt.close()

            except Exception as e:
                print(f"Error while plotting profile {key}: {e}")

        if is_verbose:
            print("All profiles have been saved.")


class CaPlotter:

    def __init__(self, handler):
        """
        Initializes the CaPlotter class with the provided plotter and plotter.

        :param plotter: Object that contains profiles and related data.
        :param plotter: Object responsible for managing plot paths.
        """
        self.handler = handler
