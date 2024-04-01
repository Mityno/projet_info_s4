import tkinter as tk
import common


# associate each color letter to a tuple :
# (color name, bg colors (default, active=lighter), fg color)
COLORS_CONVERSION = {
    'R': ('Rouge', ('#ff3921', '#ff6e5c'), 'white'),
    'V': ('Vert', ('#1fff14', '#9cff98'), 'black'),
    'B': ('Bleu', ('#0619ff', '#7681ff'), 'white'),
    'J': ('Jaune', ('#fbff0a', '#fdffa3'), 'black'),
    'N': ('Noir', ('#000000', '#737373'), 'white'),
    'M': ('Marron', ('#d16508', '#e79650'), 'white'),
    'O': ('Orange', ('#ff6c00', '#ffac59'), 'white'),
    'G': ('Gris', ('#9b9b9b', '#bfbfbf'), 'white'),
}
# maximum 4 colors per line in the color choice frame
COLORS_PER_LINE = 4


class GameWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.mainloop()


class OneGuessFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)


class CurrGuessFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self['bg'] = 'white'

        CANVAS_WIDTH, CANVAS_HEIGHT = int(ROOT_WIDTH * 0.9), 50
        BUTTON_WIDTH, BUTTON_HEIGHT = ROOT_WIDTH - CANVAS_WIDTH, 50

        choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='red',
            border=0, highlightthickness=0,
        )
        choices_canvas.grid(row=0, column=0, padx=5)

        check_button = tk.Button(
            self, text='Valider',
            bg='#27ff00', activebackground='#a7ff96',
            highlightbackground='#a7ff96',
            relief=tk.FLAT, overrelief=tk.RIDGE,
            height=3, width=7,
        )
        check_button.grid(row=0, column=1, padx=5)


class ColorSelectionFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self['bg'] = 'white'

        self.color_buttons = []
        self.curr_color = tk.StringVar(value=common.COLORS[0])

        for index, color in enumerate(common.COLORS):

            color_name, bg_colors, fg_color = COLORS_CONVERSION[color]
            default_bg, active_bg = bg_colors

            # creating the radiobutton
            button = tk.Radiobutton(
                self, value=color, indicatoron=0, text=color_name,
                variable=self.curr_color,
                bg=default_bg, highlightbackground=default_bg,
                activebackground=active_bg, selectcolor=active_bg,
                fg=fg_color, highlightcolor=fg_color,
                activeforeground=fg_color,
                offrelief=tk.FLAT, overrelief=tk.RIDGE, relief=tk.GROOVE,
                border=1, highlightthickness=0, width=8, height=2,
            )

            # placing it on the grid
            line = index // COLORS_PER_LINE
            column = index % COLORS_PER_LINE
            button.grid(
                row=line, column=column,
                pady=10, padx=10,
            )
            self.color_buttons.append(button)

    def get_value(self):
        return self.curr_color.get()


if __name__ == '__main__':
    # window = GameWindow()
    root = tk.Tk()
    root['bg'] = 'white'

    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()
    ROOT_WIDTH, ROOT_HEIGHT = SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2
    LEFT_BORDER_POS = (SCREEN_WIDTH - ROOT_WIDTH) // 2
    UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
    root.geometry(
        f'{ROOT_WIDTH}x{ROOT_HEIGHT}+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
    )

    guess_frame = CurrGuessFrame(root)
    guess_frame.pack()

    # colors_frame = ColorSelectionFrame(root)
    # colors_frame.pack()

    root.mainloop()
