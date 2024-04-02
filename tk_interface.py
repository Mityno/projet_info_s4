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
FEEDBACK_PER_LINE = 2


class GameWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.mainloop()


class OneGuessFrame(tk.Frame):


    def __init__(self, parent, combination, feedback):
        super().__init__(parent)
        self['bg'] = 'white'

        placeholder_button = tk.Button(
            self, height=3, width=7,
        )

        FEEDBACK_WIDTH = placeholder_button.winfo_reqwidth()
        FEEDBACK_HEIGHT = placeholder_button.winfo_reqheight()

        feedback_canvas = tk.Canvas(
            self, width=FEEDBACK_WIDTH, height=FEEDBACK_HEIGHT,
            bg='yellow',
            border=0, highlightthickness=0
        )

        feedback_colors = ['red'] * feedback[0] + ['white'] * feedback[1]
        feedback_colors += [''] * (common.LENGTH - len(feedback_colors))


        CELL_WIDTH = FEEDBACK_WIDTH // FEEDBACK_PER_LINE
        CELL_HEIGHT = FEEDBACK_HEIGHT // (common.LENGTH // FEEDBACK_PER_LINE)

        FEEDBACK_RADIUS = (CELL_WIDTH * 0.8) // 2

        for index, feedback_color in enumerate(feedback_colors):

            y_pos, x_pos = divmod(index, FEEDBACK_PER_LINE)

            x_center = CELL_WIDTH * (x_pos + 1/2)
            y_center = CELL_HEIGHT * (y_pos + 1/2)

            top_left = (x_center - FEEDBACK_RADIUS, y_center - FEEDBACK_RADIUS)
            bottom_right = (x_center + FEEDBACK_RADIUS, y_center + FEEDBACK_RADIUS)

            feedback_canvas.create_oval(
                *top_left, *bottom_right,
                fill=feedback_color
                )

        feedback_canvas.grid(row=0, column=1, padx=5, pady=5)

        CANVAS_WIDTH = (ROOT_WIDTH - FEEDBACK_WIDTH) * 0.95
        CANVAS_HEIGHT = FEEDBACK_HEIGHT

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='yellow',
            border=0, highlightthickness=0,
        )
        self.choices_canvas.grid(row=0, column=0, padx=5)

        # there are common.LENGTH cells in the canvas
        CELL_WIDTH = CANVAS_WIDTH // common.LENGTH
        CELL_HEIGHT = CANVAS_HEIGHT

        CIRCLE_RADIUS = (CELL_HEIGHT * 0.8) / 2

        choices_id = []

        color_names = [
            COLORS_CONVERSION[color_value][1][0]
            for color_value in combination
        ]

        for cell_num, color_name in zip(range(common.LENGTH), color_names):

            x_center = CELL_WIDTH * (cell_num + 1/2)
            y_center = CELL_HEIGHT // 2

            top_left = (x_center - CIRCLE_RADIUS, y_center - CIRCLE_RADIUS)
            bottom_right = (x_center + CIRCLE_RADIUS, y_center + CIRCLE_RADIUS)

            self.choices_canvas.create_oval(
                *top_left, *bottom_right, fill=color_name
            )



class CurrGuessFrame(tk.Frame):

    def __init__(self, parent, color_selector):
        super().__init__(parent)
        self['bg'] = 'white'

        self.color_selector = color_selector

        check_button = tk.Button(
            self, text='Valider',
            bg='#27ff00', activebackground='#a7ff96',
            highlightbackground='#a7ff96',
            relief=tk.FLAT, overrelief=tk.RIDGE,
            height=3, width=7,
        )
        check_button.grid(row=0, column=1, padx=5, pady=5)

        BUTTON_WIDTH = check_button.winfo_reqwidth()
        BUTTON_HEIGHT = check_button.winfo_reqheight()

        CANVAS_WIDTH = (ROOT_WIDTH - BUTTON_WIDTH) * 0.95
        CANVAS_HEIGHT = BUTTON_HEIGHT

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='yellow',
            border=0, highlightthickness=0,
        )
        self.choices_canvas.grid(row=0, column=0, padx=5)

        # there are common.LENGTH cells in the canvas
        CELL_WIDTH = CANVAS_WIDTH // common.LENGTH
        CELL_HEIGHT = CANVAS_HEIGHT

        CIRCLE_RADIUS = (CELL_HEIGHT * 0.8) / 2

        for cell_num in range(common.LENGTH):

            x_center = CELL_WIDTH * (cell_num + 1/2)
            y_center = CELL_HEIGHT // 2

            top_left = (x_center - CIRCLE_RADIUS, y_center - CIRCLE_RADIUS)
            bottom_right = (x_center + CIRCLE_RADIUS, y_center + CIRCLE_RADIUS)

            circle_id = self.choices_canvas.create_oval(*top_left, *bottom_right, fill='white')
            self.choices_canvas.tag_bind(
                circle_id, '<Button-1>',
                func=lambda event, circle_id=circle_id: self.change_choice_color(circle_id)
                )


    def change_choice_color(self, circle_id):
        color_value = self.color_selector.get_value()
        _, (color_name, _), _ = COLORS_CONVERSION[color_value]
        self.choices_canvas.itemconfigure(
            circle_id, fill=color_name
        )


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
    ROOT_WIDTH, ROOT_HEIGHT = int(SCREEN_WIDTH / 2.5), SCREEN_HEIGHT // 2
    LEFT_BORDER_POS = (SCREEN_WIDTH - ROOT_WIDTH) // 2
    UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
    root.geometry(
        f'{ROOT_WIDTH}x{ROOT_HEIGHT}+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
    )

    one_guess_frame = OneGuessFrame(root, 'NGJM', (1, 3))

    colors_frame = ColorSelectionFrame(root)
    guess_frame = CurrGuessFrame(root, colors_frame)

    one_guess_frame.pack()
    guess_frame.pack()
    colors_frame.pack()

    root.mainloop()
