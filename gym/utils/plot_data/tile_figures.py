# 20240710 created by YM

import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from screeninfo import get_monitors

def tileFigures(fig_nums, monitor_num, rows, cols, gap=10):
    # Get screen information
    monitors = get_monitors()
    # print(monitors)
    if monitor_num >= len(monitors):
        print(f"Monitor number {monitor_num} is not available.")
        monitor_num = 0


    monitor = monitors[monitor_num]
    screen_width = monitor.width
    screen_height = monitor.height

    # Determine the size of each plot including gaps
    total_gap_width = (cols + 1) * gap
    total_gap_height = (rows + 1) * gap
    plot_width = (screen_width - total_gap_width) // cols
    plot_height = (screen_height - total_gap_height) // rows

    # Create a Tkinter root window
    root = tk.Tk()
    root.title("close all")
    root.withdraw()  # Hide the root window

    for i in range(fig_nums):
        row = i // cols
        col = i % cols

        # Get the figure by number
        fig = plt.figure(i + 1)

        # Create a Tkinter window for each plot
        plot_window = tk.Toplevel(root)
        plot_window.title(f"Figure {i + 1}")
        x_position = monitor.x + col * (plot_width + gap) + gap
        y_position = monitor.y + row * (plot_height + gap) + gap
        plot_window.geometry(f"{plot_width}x{plot_height}+{x_position}+{y_position}")

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Add toolbar for navigation (zoom, pan, etc.)
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.deiconify()  # Show the root window
    root.mainloop()

# Example usage
# Create some example figures
# for i in range(6):
#     plt.figure(i + 1)
#     plt.plot([0, 1, 2], [0, 1, 4])
#     plt.title(f'Figure {i + 1}')

# Display the plots on screen
# display_plots_on_screen(num_plots=6, monitor_num=0, rows=2, cols=3, gap=20)

