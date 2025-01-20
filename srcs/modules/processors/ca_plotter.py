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

        # Создание директории, если её нет
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
                        idx: obj_row['dist']
                        for idx, obj_row in matching_objects.iterrows()
                    }

                plt.figure(figsize=(10, 6))
                for col in ['h', 'h_sec']:
                    if col in df:
                        plt.plot(df['l'], df[col], label=col)

                plt.xlabel("Altitude")
                plt.ylabel("Distance")
                plt.title(f"Plot for {key}")
                plt.legend()
                plt.grid(True)
                plt.savefig(os.path.join(plots_dir, f"{key}.png"))
                plt.close()

                #if is_verbose:
                #    print(f"Plot saved for profile: {key}")

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
