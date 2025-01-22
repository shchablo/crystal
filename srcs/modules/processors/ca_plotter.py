import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import os
import numpy as np

class CaTopPlotter:
    def __init__(self, core, plotter):
        """
        Initializes the CaPlotter class with the provided plotter and plotter.

        :param plotter: Object that contains profiles and related data.
        :param plotter: Object responsible for managing plot paths.
        """
        self.core = core
        self.plotter = plotter

    def all(
            self,
            verbose: str = "y",

            folder: str = "result/plots", 
            extension: str = "png", 
            figsize: tuple = (10, 6),
            title_prefix: str = "Профиль №",
            xlabel: str = "Расстояние, м",
            ylabel: str = "Абс. высота, м",
            
            
            line_colors: dict = {'h': '#1f77b4', 'h_sec': '#2ca02c'},
            line_styles: dict = {'h': '-.', 'h_sec': '--'},
            line_widths: dict = {'h': 0.7, 'h_sec': 0.7},
            line_labels: dict = {'h': 'Продольный профиль', 'h_sec': 'Секущая профиля'},
            
            dist_marker_style: str = 'x',
            dist_marker_color: str = '#d62728',
            text_offset: tuple = (-5, -10),
            
            xlabel_fontsize: int = 12,
            ylabel_fontsize: int = 12,
            
            legend_loc: str = 'upper right',
            legend_fontsize: int = 10,
            
            grid_linestyle: str = '--',
            grid_linewidth: float = 0.5,
            grid_alpha: float = 0.7,
            
            offset_x: int = 50,
            offset_y: int = -30,

            arc_radius = 20,
            arc_width_factor = 6,
            arc_height_factor = 2,
            arc_arc_color = 'orange',
            arc_linestyle = '-',
            arc_linewidth = 1,
            arc_annotation_color = 'orange',
            arc_font_size = 10,
            arc_font_weight = 'normal',
            arc_annotation_color_offset_x = 4,
            arc_annotation_color_offset_y = 0.2
    ):
        is_verbose = verbose.strip().lower() in {"1", "y", "yes", "true"}

        if is_verbose:
            print("Plotting profiles...")

        plots_dir = os.path.join(self.plotter.handler.path, folder)
        os.makedirs(plots_dir, exist_ok=True)

        for key, df in self.plotter.handler.profiles.items():
            try:
                matching_objects = self.plotter.handler.objects.loc[
                    self.plotter.handler.objects['name'].astype(str) == str(key)
                ]

                l_max = self.plotter.handler.main.loc[self.plotter.handler.main['name'].astype(str) == str(key), str('L_max')]
                dist_values = {}
                if not matching_objects.empty:
                    dist_values = {
                        idx: (obj_row['dist'], obj_row['object'])  # Сохраняем и дистанцию, и подпись
                        for idx, obj_row in matching_objects.iterrows()
                    }

                plt.figure(figsize=figsize)

                h_cut = 0
                l_cut = df['l'].max()
                for col in ['h', 'h_sec']:
                    if col in df:

                        # Добавляем точки для дистанций
                        obj_heights = []
                        if col == 'h' and dist_values:
                            for dist, obj_label in dist_values.values():
                                # Найти ближайшее значение высоты
                                closest_row = df.iloc[(df['l'] - dist).abs().idxmin()]
                                height = closest_row[col]
                                obj_heights.append(height)
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

                            # Находим значение ограничения графика.

                            if dist_values:
                                # Находим максимальное значение height
                                max_dist = max(value[0] for value in dist_values.values())

                                # Преобразуем L_max в числовой формат для сравнения
                                l_max_value = float(l_max.iloc[0]) if not l_max.empty else 0

                                # Сравниваем max_dist с L_max
                                if max_dist > l_max_value:
                                    l_cut = max_dist + offset_x
                                else:
                                    l_cut = l_max_value + offset_x

                            # Находим значение ограничения графика.
                            l_max_y = self.plotter.handler.internal_main.loc[self.plotter.handler.internal_main['name'].astype(str) == str(key), 'L_max_y']
                            # Преобразуем L_max в числовой формат для сравнения
                            l_max_y_value = float(l_max_y.iloc[0]) if not l_max_y.empty else 0

                            if obj_heights:
                                # Находим максимальное значение dist
                                min_height = min(value for value in obj_heights)
                                if min_height < l_max_y_value:
                                    h_cut = min_height + offset_y
                                else:
                                    h_cut = l_max_y_value + offset_y


                        # перед тем как строит находим минимальную высоту объекта и фильтруем данные
                        filtered_data = df[( (df['l'] >= 0) & (df['l'] <= l_cut) ) & ( (df[col] > h_cut) )]

                        # Линия на графике
                        plt.title(f"{title_prefix} {key}")
                        plt.plot(
                            filtered_data['l'],
                            filtered_data[col],
                            color=line_colors.get(col, 'black'),
                            linestyle=line_styles.get(col, '-'),
                            linewidth=line_widths.get(col, 0.7),
                            label=line_labels.get(col, col)  # Добавляем подпись для легенды
                        )

                        if (col == "h_sec"):                        
                            
                            # Находим коэффициенты наклона линии
                            x = filtered_data['l']
                            y = filtered_data[col]
                            coefficients = np.polyfit(x, y, 1)  # Линейная аппроксимация
                            slope = coefficients[0]  # Наклон линии

                            # Вычисление угла в радианах и градусах
                            angle_radians = np.arctan(slope)
                            angle_degrees = np.degrees(angle_radians)
                            # Добавление арки для отображения угла
                            center_x, center_y = x.iloc[0], y.iloc[0]  # Начальная точка
                            arc = patches.Arc(
                                (center_x, center_y),  # Центр
                                width=arc_width_factor*arc_radius, height=arc_height_factor*arc_radius,  # Размер арки
                                angle=0,  # Угол поворота арки
                                theta1=angle_degrees, theta2=0,  # Углы начала и конца
                                color=arc_arc_color, linestyle=arc_linestyle, linewidth=arc_linewidth
                            )
                            plt.gca().add_patch(arc)

                            # Добавление аннотации угла
                            plt.annotate(
                                f"tgψ={abs(slope):.3f}", 
                                xy=(center_x + arc_radius * arc_annotation_color_offset_x, center_y - arc_radius * arc_annotation_color_offset_y), 
                                color=arc_annotation_color,
                                fontsize=arc_font_size,
                                fontweight=arc_font_weight
                            )

                # Настройки осей
                plt.xlabel(xlabel, fontsize=xlabel_fontsize)
                plt.ylabel(ylabel, fontsize=ylabel_fontsize)

                # Легенда
                plt.legend(loc=legend_loc, fontsize=legend_fontsize)  # Легенда в правом верхнем углу

                # Общие настройки
                plt.grid(True, which='both', linestyle=grid_linestyle, linewidth=grid_linewidth, alpha=grid_alpha)
                plt.tight_layout()
                plt.savefig(os.path.join(plots_dir, f"{key}.{extension}"))
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
