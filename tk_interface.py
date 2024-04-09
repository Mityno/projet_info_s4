import tkinter as tk
import tkinter.messagebox as messagebox
import common
import math


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
# at least 2 feebacks per line
FEEDBACK_PER_LINE = max(round(common.LENGTH ** 0.5), 2)

PADY_VALUE = 5


class InvalidCombinationError(Exception):
    pass


class GameWindow(tk.Tk):

    def __init__(self, codemaker, n_memory=8):
        super().__init__()
        self['bg'] = 'white'
        self.resizable(False, False)

        self.n_memory = n_memory
        self.codemaker = codemaker
        self.codemaker.init()
        print(self.codemaker.solution, flush=True)

        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        self.ROOT_WIDTH = int(SCREEN_WIDTH / 2.5)
        ROOT_HEIGHT = SCREEN_HEIGHT // 2
        LEFT_BORDER_POS = (SCREEN_WIDTH - self.ROOT_WIDTH) // 2
        UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
        self.geometry(
            f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'
            f'+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
        )

        placeholder_button = tk.Button(
            self, height=3, width=7,
        )

        ROW_MIN_HEIGHT = placeholder_button.winfo_reqheight()

        self.top_frame = tk.Frame(
            self, height=ROW_MIN_HEIGHT*self.n_memory, bg='white'
        )
        self.bottom_frame = tk.Frame(
            self, height=ROW_MIN_HEIGHT*3, bg='white', bd=5
        )

        self.result_frames = []
        for i in range(self.n_memory):
            curr_frame = GuessResultFrame(
                self.top_frame, '', (0, 0), self.ROOT_WIDTH
            )
            curr_frame.grid(row=i)
            self.result_frames.append(curr_frame)

        self.colors_frame = ColorSelectionFrame(self.bottom_frame)
        self.guess_frame = CurrGuessFrame(
            self.bottom_frame, self.colors_frame, self.ROOT_WIDTH
        )
        self.guess_frame.set_command(self.make_move)

        self.guess_frame.pack()
        self.colors_frame.pack()

        self.top_frame.pack()
        self.bottom_frame.pack()

        ROOT_HEIGHT = (
            self.top_frame.winfo_reqheight()
            + self.bottom_frame.winfo_reqheight()
            + PADY_VALUE * (2 * self.n_memory + 4)
        )
        LEFT_BORDER_POS = (SCREEN_WIDTH - self.ROOT_WIDTH) // 2
        UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
        self.geometry(
            f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'
            f'+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
        )

    def make_move(self):
        try:
            comb = self.guess_frame.get_combination()
        except InvalidCombinationError:
            messagebox.showinfo(
                'Combinaison invalide',
                'La combinaison essayée n\'est pas valide.',
                detail='Assurez vous d\'avoir rentré '
                'toutes les couleurs avant de valider.',
                icon='question'
                )
            return

        feedback = self.codemaker.codemaker(comb)
        new_result_frame = GuessResultFrame(
            self.top_frame, comb, feedback, self.ROOT_WIDTH
        )

        for curr_frame in self.result_frames:
            curr_frame.grid_forget()

        self.result_frames.pop(0)
        self.result_frames.append(new_result_frame)

        for i, curr_frame in enumerate(self.result_frames):
            curr_frame.grid(row=i)

        # le joueur n'a pas encore gagné
        if feedback != (common.LENGTH, 0):
            return

        user_choice = messagebox.askyesno(
            'Fin de partie',
            'Bravo, vous avez gagné !\nVoulez vous rejouer ?',
            icon='info'
            )

        if user_choice:
            self.reboot()
        else:
            self.destroy()

    def reboot(self):
        self.codemaker.init()
        print(self.codemaker.solution, flush=True)

        for curr_frame in self.result_frames:
            curr_frame.grid_forget()

        self.result_frames = []
        for i in range(self.n_memory):
            curr_frame = GuessResultFrame(
                self.top_frame, '', (0, 0), self.ROOT_WIDTH
            )
            curr_frame.grid(row=i)
            self.result_frames.append(curr_frame)


class GuessResultFrame(tk.Frame):

    def __init__(self, parent, combination, feedback, ROOT_WIDTH):
        super().__init__(parent)
        self['bg'] = 'white'

        placeholder_button = tk.Button(
            self, height=3, width=7,
        )

        FEEDBACK_WIDTH = placeholder_button.winfo_reqwidth()
        FEEDBACK_HEIGHT = placeholder_button.winfo_reqheight()

        feedback_canvas = tk.Canvas(
            self, width=FEEDBACK_WIDTH, height=FEEDBACK_HEIGHT,
            bg='#ca6f1e',
            border=0, highlightthickness=0
        )

        feedback_colors = ['white'] * feedback[0] + ['red'] * feedback[1]
        feedback_colors += ['#f0b27a'] * (common.LENGTH - len(feedback_colors))

        CELL_WIDTH = FEEDBACK_WIDTH / FEEDBACK_PER_LINE
        n_lines = math.ceil(common.LENGTH / FEEDBACK_PER_LINE)
        CELL_HEIGHT = FEEDBACK_HEIGHT / n_lines

        FEEDBACK_RADIUS = math.ceil(
            (CELL_WIDTH * 0.8) / max(n_lines, FEEDBACK_PER_LINE)
        )

        for index, feedback_color in enumerate(feedback_colors):

            y_pos, x_pos = divmod(index, FEEDBACK_PER_LINE)

            x_center = CELL_WIDTH * (x_pos + 1/2)
            y_center = CELL_HEIGHT * (y_pos + 1/2)

            top_left = (x_center - FEEDBACK_RADIUS, y_center - FEEDBACK_RADIUS)
            bottom_right = (
                x_center + FEEDBACK_RADIUS, y_center + FEEDBACK_RADIUS
            )

            feedback_canvas.create_oval(
                *top_left, *bottom_right,
                fill=feedback_color
                )

        feedback_canvas.grid(row=0, column=1, padx=5, pady=PADY_VALUE)

        CANVAS_WIDTH = (ROOT_WIDTH - FEEDBACK_WIDTH) * 0.97
        CANVAS_HEIGHT = FEEDBACK_HEIGHT

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='#ca6f1e',
            border=0, highlightthickness=0,
        )
        self.choices_canvas.grid(row=0, column=0, padx=5)

        # there are common.LENGTH cells in the canvas
        CELL_WIDTH = CANVAS_WIDTH // common.LENGTH
        CELL_HEIGHT = CANVAS_HEIGHT

        CIRCLE_RADIUS = (CELL_HEIGHT * 0.8) / 2

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

    def __init__(self, parent, color_selector, ROOT_WIDTH):
        super().__init__(parent)
        self['bg'] = 'white'

        self.color_selector = color_selector
        self.colors_value = [None] * common.LENGTH

        self.check_button = tk.Button(
            self, text='Valider',
            bg='#27ff00', activebackground='#a7ff96',
            highlightbackground='#a7ff96',
            relief=tk.FLAT, overrelief=tk.RIDGE,
            height=3, width=7,
        )
        self.check_button.grid(row=0, column=1, padx=5, pady=PADY_VALUE)

        BUTTON_WIDTH = self.check_button.winfo_reqwidth()
        BUTTON_HEIGHT = self.check_button.winfo_reqheight()

        CANVAS_WIDTH = (ROOT_WIDTH - BUTTON_WIDTH) * 0.97
        CANVAS_HEIGHT = BUTTON_HEIGHT

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='#ca6f1e',
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

            circle_id = self.choices_canvas.create_oval(
                *top_left, *bottom_right, fill='white'
            )
            self.choices_canvas.tag_bind(
                circle_id, '<Button-1>', func=self.change_choice_color
            )

    def set_command(self, func):
        self.check_button['command'] = func

    def change_choice_color(self, event, circle_id):
        color_value = self.color_selector.get_value()
        self.colors_value[circle_id - 1] = color_value
        _, (color_name, _), _ = COLORS_CONVERSION[color_value]
        self.choices_canvas.itemconfigure(
            circle_id, fill=color_name
        )

    def get_combination(self):
        if None in self.colors_value:
            raise InvalidCombinationError(self.colors_value)
        return ''.join(self.colors_value[:])


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
                pady=2 * PADY_VALUE, padx=10,
            )
            self.color_buttons.append(button)

    def get_value(self):
        return self.curr_color.get()


class SettingsFrame(tk.Frame):
    pass


if __name__ == '__main__':
    import codemaker1
    window = GameWindow(codemaker1, n_memory=8)
    window.mainloop()
