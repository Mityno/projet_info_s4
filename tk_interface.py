import tkinter as tk
import tkinter.messagebox as messagebox
import common
import math


# associate each color letter to a tuple :
# (color name, bg colors (default, active=lighter), fg color)
COLORS_CONVERSION = {
    'r': ('Rose', ('#e91e63', '#f48fb1'), 'white'),
    'I': ('Violet', ('#8e44ad', '#bb8fce'), 'white'),
    'M': ('Marron', ('#d16508', '#e79650'), 'white'),
    'R': ('Rouge', ('#ff3921', '#ff6e5c'), 'white'),
    'O': ('Orange', ('#ff6c00', '#ffac59'), 'white'),
    'J': ('Jaune', ('#fbff0a', '#fdffa3'), 'black'),
    'V': ('Vert', ('#1fff14', '#9cff98'), 'black'),
    'S': ('Sapin', ('#1abc9c', '#abebc6'), 'white'),
    'C': ('Cyan', ('#4de7f4', '#48d7ff'), 'white'),
    'B': ('Bleu', ('#0619ff', '#7681ff'), 'white'),
    'N': ('Noir', ('#000000', '#737373'), 'white'),
    'G': ('Gris', ('#9b9b9b', '#bfbfbf'), 'white'),
}
BACKGROUND_COLOR = '#d3926c'
CONTOUR_COLOR = '#ad6944'
PADY_VALUE = 5
# maximum 4 colors per line in the color choice frame
COLORS_PER_LINE = 4
# at least 2 feebacks per line
FEEDBACK_PER_LINE = max(round(common.LENGTH ** 0.5), 2)

# store the original setting inside common to be able to restore them after
# they have been modified when playing
OLD_COLORS = common.COLORS[:]
OLD_LENGTH = common.LENGTH
AVAILABLE_COLORS = list(COLORS_CONVERSION.keys())
common.COLORS = AVAILABLE_COLORS

class InvalidCombinationError(Exception):
    pass


class GameWindow(tk.Tk):

    def __init__(self, codemaker, n_memory=8):
        super().__init__()
        self['bg'] = BACKGROUND_COLOR
        self.title('Mastermind')
        self.resizable(False, False)

        self.n_memory = n_memory
        self.codemaker = codemaker
        self.make_window(init=True)

        self.bind('<Escape>', lambda event: self.quit())

    def make_window(self, *, init=False):
        global FEEDBACK_PER_LINE
        FEEDBACK_PER_LINE = max(round(common.LENGTH ** 0.5), 2)

        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        self.ROOT_WIDTH = 700 # min(max(660, int(SCREEN_WIDTH / 3)), 700)
        ROOT_HEIGHT = SCREEN_HEIGHT // 2
        LEFT_BORDER_POS = (SCREEN_WIDTH - self.ROOT_WIDTH) // 2
        UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
        if init:
            self.geometry(
                f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'
                f'+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
            )

        placeholder_button = tk.Button(
            self, height=3, width=7,
        )

        ROW_MIN_HEIGHT = placeholder_button.winfo_reqheight()

        self.top_frame = tk.Frame(
            self, height=ROW_MIN_HEIGHT*self.n_memory, bg=self['bg']
        )
        if 'bottom_frame' not in vars(self):
            self.bottom_frame = tk.Frame(
                self, height=ROW_MIN_HEIGHT*3, bg=self['bg']
            )

        self.result_frames = []
        for i in range(self.n_memory):
            curr_frame = GuessResultFrame(
                self.top_frame, '', (0, 0), self.ROOT_WIDTH
            )
            curr_frame.grid(row=i, pady=2)
            self.result_frames.append(curr_frame)

        self.colors_frame = ColorSelectionFrame(self.bottom_frame)
        self.guess_frame = CurrGuessFrame(
            self.bottom_frame, self.colors_frame, self.ROOT_WIDTH
        )
        self.guess_frame.set_command(self.make_move)

        self.guess_frame.grid(row=0, columnspan=2, pady=5)
        self.colors_frame.grid(row=1, column=0)
        if init:
            self.colors_frame.update()
            self.bottom_frame.columnconfigure(0, minsize=self.colors_frame.winfo_reqwidth())
            self.bottom_frame.rowconfigure(1, minsize=self.colors_frame.winfo_reqheight())

        if 'settings_frame' not in vars(self):
            self.settings_frame = SettingsFrame(self.bottom_frame, self.reset)
        self.settings_frame.grid(row=1, column=1)

        self.top_frame.grid(row=0)
        self.bottom_frame.grid(row=1)

        if init:
            # self.update()

            LEFT_BORDER_POS = (SCREEN_WIDTH - self.ROOT_WIDTH) // 2
            UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2

        self.top_frame.update()
        self.bottom_frame.update()
        ROOT_HEIGHT = (
            self.top_frame.winfo_reqheight()
            + self.bottom_frame.winfo_reqheight()
            + PADY_VALUE
        )
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
            curr_frame.grid(row=i, pady=2)

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
            curr_frame.destroy()

        self.result_frames = []
        for i in range(self.n_memory):
            curr_frame = GuessResultFrame(
                self.top_frame, '', (0, 0), self.ROOT_WIDTH
            )
            curr_frame.grid(row=i, pady=2)
            self.result_frames.append(curr_frame)

    def reset(self):
        for child in self.winfo_children():
            if child != self.bottom_frame:
                child.destroy()
                continue
        for child in self.bottom_frame.winfo_children():
            if child != self.settings_frame:
                child.destroy()
        self.make_window()
        self.reboot()


class GuessResultFrame(tk.Frame):

    def __init__(self, parent, combination, feedback, ROOT_WIDTH):
        super().__init__(parent)
        self['bg'] = parent['bg']

        placeholder_button = tk.Button(
            self, height=3, width=7,
        )

        FEEDBACK_WIDTH = placeholder_button.winfo_reqwidth()
        FEEDBACK_HEIGHT = placeholder_button.winfo_reqheight()

        feedback_canvas = tk.Canvas(
            self, width=FEEDBACK_WIDTH, height=FEEDBACK_HEIGHT,
            bg=CONTOUR_COLOR,
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
                fill=feedback_color, width=0
                )

        feedback_canvas.grid(row=0, column=1, padx=5, pady=PADY_VALUE)

        CANVAS_WIDTH = (ROOT_WIDTH - FEEDBACK_WIDTH) * 0.95
        CANVAS_HEIGHT = FEEDBACK_HEIGHT

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='#d38053', highlightbackground=CONTOUR_COLOR,
            border=0, highlightthickness=3,
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

            x_center = CELL_WIDTH * (cell_num + 1/2) + 2
            y_center = CELL_HEIGHT // 2 + 2

            top_left = (x_center - CIRCLE_RADIUS, y_center - CIRCLE_RADIUS)
            bottom_right = (x_center + CIRCLE_RADIUS, y_center + CIRCLE_RADIUS)

            self.choices_canvas.create_oval(
                *top_left, *bottom_right,
                fill=color_name, width=0
            )


class CurrGuessFrame(tk.Frame):

    def __init__(self, parent, color_selector, ROOT_WIDTH):
        super().__init__(parent)
        self['bg'] = parent['bg']

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

        CANVAS_WIDTH = (ROOT_WIDTH - BUTTON_WIDTH) * 0.95
        CANVAS_HEIGHT = BUTTON_HEIGHT

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='#d38053', highlightbackground=CONTOUR_COLOR,
            border=0, highlightthickness=3,
        )
        self.choices_canvas.grid(row=0, column=0, padx=5)

        # there are common.LENGTH cells in the canvas
        CELL_WIDTH = CANVAS_WIDTH / common.LENGTH
        CELL_HEIGHT = CANVAS_HEIGHT

        CIRCLE_RADIUS = (CELL_HEIGHT * 0.8) / 2

        for cell_num in range(common.LENGTH):

            x_center = CELL_WIDTH * (cell_num + 1/2) + 2
            y_center = CELL_HEIGHT / 2 + 2

            top_left = (round(x_center - CIRCLE_RADIUS), y_center - CIRCLE_RADIUS)
            bottom_right = (round(x_center + CIRCLE_RADIUS), y_center + CIRCLE_RADIUS)

            circle_id = self.choices_canvas.create_oval(
                *top_left, *bottom_right,
                fill='white', width=0
            )
            self.choices_canvas.tag_bind(
                circle_id, '<Button-1>', func=self.change_choice_color
            )

    def set_command(self, func):
        self.check_button['command'] = func

    def change_choice_color(self, event):
        circle_id, = self.choices_canvas.find_closest(event.x, event.y)
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
        super().__init__(
            parent,
            bg=parent['bg'],
            highlightbackground=CONTOUR_COLOR, highlightthickness=5
        )

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


class SettingsFrame(tk.LabelFrame):

    def __init__(self, parent, parent_update):
        super().__init__(
            parent, text='Paramètres de jeu', labelanchor='n',
            fg='white',
            bg=parent['bg'], bd=0,
            highlightbackground=CONTOUR_COLOR, highlightthickness=2,
            )
        self.parent_update = parent_update
        self.length_box = tk.Scale(
            self, from_=1, to=12, resolution=1, orient='horizontal',
            width=14, sliderlength=20, bd=1, length=180,
            label='Longueur des combinaisons',
            fg='white',
            bg=self['bg'], activebackground=self['bg'],
            highlightbackground=CONTOUR_COLOR, highlightthickness=1,
            troughcolor=CONTOUR_COLOR,
        )
        self.colors_box = tk.Scale(
            self, from_=1, to=len(AVAILABLE_COLORS), resolution=1, orient='horizontal',
            width=14, sliderlength=20, bd=1, length=180,
            label='Nombre de couleurs disponibles',
            fg='white',
            bg=self['bg'], activebackground=self['bg'],
            highlightbackground=CONTOUR_COLOR, highlightthickness=1,
            troughcolor=CONTOUR_COLOR,
        )

        self.length_box.set(common.LENGTH)
        self.colors_box.set(len(OLD_COLORS))

        self.length_box['command'] = self.update_settings
        self.colors_box['command'] = self.update_settings

        self.length_box.grid(row=0, pady=3, padx=3)
        self.colors_box.grid(row=1, pady=3)

        self.last_update_command = None
        self.after(0, self.update_settings, None)

    def update_settings(self, event):
        global COLORS
        # used for comparison, ensure to update the window only and only if
        # these values have actually changed
        old_values = (common.LENGTH, common.COLORS[:])

        common.LENGTH = self.length_box.get()
        nb_colors = self.colors_box.get()
        common.COLORS = AVAILABLE_COLORS[:nb_colors]

        if old_values != (common.LENGTH, common.COLORS):
            self.parent_update()


if __name__ == '__main__':
    import codemaker1
    window = GameWindow(codemaker1, n_memory=8)
    window.mainloop()

    common.LENGTH = OLD_LENGTH
    common.COLORS = OLD_COLORS
