import tkinter as tk
import tkinter.messagebox as messagebox
import common
import math


# associate each color letter to a tuple :
# (color full name, bg colors (default, active=lighter), fg color)
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
BACKGROUND_COLOR = '#d3926c'  # light brown
CONTOUR_COLOR = '#ad6944'  # warmer brown
PADY_VALUE = 5  # vertical spaces (in pixel) around each widget
# maximum 4 colors per line in the color choice frame
COLORS_PER_LINE = 4
# at least 2 feebacks per line, but adapt to a "high" value for common.LENGTH
# by making the feedbacks as much squared as possible
FEEDBACK_PER_LINE = max(round(common.LENGTH ** 0.5), 2)

# store the original setting of common to be able to restore them after they
# have been modified when playing
OLD_COLORS = common.COLORS[:]
OLD_LENGTH = common.LENGTH

AVAILABLE_COLORS = list(COLORS_CONVERSION.keys())  # COLORS used for the GUI
common.COLORS = AVAILABLE_COLORS


class InvalidCombinationError(Exception):
    """
    Custom error that allows the GUI to know if the combination is ready to be
    used to play, else the GUI will display an error message
    """
    pass


class GameWindow(tk.Tk):

    """
    The main window of the GUI, uses other components inside two frames (top
    and bottom) for good visual placement.
    Controls the overall behaviour of the window and refresh widgets when
    settings are changed.
    """

    def __init__(self, codemaker, n_memory=8):
        """
        Initialise the window, the user will be playing against the choosen
        codemaker and will be able to see his `n_memory` last moves.
        """

        # initialise the tkinter window
        super().__init__()
        self['bg'] = BACKGROUND_COLOR
        self.title('Mastermind')
        # do not allow the window to be resized, mainly because the window
        # needs a minimal size to be "pretty" and shouldn't be changed
        self.resizable(False, False)

        self.n_memory = n_memory
        self.codemaker = codemaker
        self.make_window(init=True)

        # bind a key to quit the window
        self.bind('<Escape>', lambda event: self.quit())

    def make_window(self, *, init=False):
        """
        Make (and refresh) the window with the last settings for the game.

        init : used to specify that this is the first making of the window,
        shouldn't be used once the window is fully created and displayed. Its
        main purpose is to avoid flickering when refreshing the window.
        """

        global FEEDBACK_PER_LINE
        FEEDBACK_PER_LINE = max(round(common.LENGTH ** 0.5), 2)

        if init:
            SCREEN_WIDTH = self.winfo_screenwidth()
            SCREEN_HEIGHT = self.winfo_screenheight()
            # arbitrary choosen value for the window width, it allows the window
            # to fit nicely in the screen without hiding widgets and compromising
            # game behaviour
            self.ROOT_WIDTH = 550
    
            # window height is defined to not take too much space in the screen
            # vertically. Note that on small screen, you might have to reduce
            # n_memory for the window to fully fit in this height requirement
            ROOT_HEIGHT = SCREEN_HEIGHT // 2
            LEFT_BORDER_POS = (SCREEN_WIDTH - self.ROOT_WIDTH) // 2
            UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
    
            # temporarly place the window in the middle of the screen until
            # all widget have been defined and placed on the window, only
            # necessary when initialising the window
            self.geometry(
                f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'
                f'+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
            )

        # this button serves as a reference for minimal height or width of
        # some widgets
        placeholder_button = tk.Button(
            self, height=2, width=7,
        )
        ROW_MIN_HEIGHT = placeholder_button.winfo_reqheight()
        placeholder_button.destroy()

        # only create top and bottom frame at initialisition
        if init:
            # top frame keeps track of previously played combinations
            self.top_frame = tk.Frame(
                self, height=ROW_MIN_HEIGHT*self.n_memory, bg=self['bg']
            )

            # bottom frame controls the current combination and color select,
            # as well as the settings
            self.bottom_frame = tk.Frame(
                self, height=ROW_MIN_HEIGHT*3, bg=self['bg']
            )

        # "memory" frames, they keep track of the previous combinations played
        self.result_frames = []
        for i in range(self.n_memory):
            # '' is for an empty comination
            curr_frame = GuessResultFrame(
                self.top_frame, '', (0, 0), self.ROOT_WIDTH
            )
            curr_frame.grid(row=i, pady=2)
            self.result_frames.append(curr_frame)

        # first create the color selection and the current combination frame
        self.colors_frame = ColorSelectionFrame(self.bottom_frame)
        self.guess_frame = CurrGuessFrame(
            self.bottom_frame, self.colors_frame, self.ROOT_WIDTH
        )
        # associate the guess frame's button with the command of making a move
        self.guess_frame.set_command(self.make_move)

        # place these frames
        self.guess_frame.grid(row=0, columnspan=2, pady=5)
        self.colors_frame.grid(row=1, column=0)

        if init:
            # on initialisation, update the color frame and take its sizes
            # (which at maximal at that moment) : they will be the reference
            # sizes for the last row of the bottom frame so that the placement
            # is consistent, even after the settings have changed
            self.colors_frame.update()
            self.bottom_frame.columnconfigure(0, minsize=self.colors_frame.winfo_reqwidth())
            self.bottom_frame.rowconfigure(1, minsize=self.colors_frame.winfo_reqheight())

            # create the settings frame. It will never been deleted, so do it
            # only on initialisation
            self.settings_frame = SettingsFrame(self.bottom_frame, self.reset)

        # place the setting frame
        self.settings_frame.grid(row=1, column=1)

        # finally, place the two main frames of the window
        self.top_frame.grid(row=0)
        self.bottom_frame.grid(row=1)

        # finally, all widgets have been placed, replace the window at the
        # center of the screen and adjust its size. Only necessary at
        # initialisation since the window dimension won't change
        if init:
            self.top_frame.update()
            self.bottom_frame.update()
            ROOT_HEIGHT = (
                self.top_frame.winfo_reqheight()
                + self.bottom_frame.winfo_reqheight()
                + PADY_VALUE
            )
            LEFT_BORDER_POS = (SCREEN_WIDTH - self.ROOT_WIDTH) // 2
            UPPER_BORDER_POS = (SCREEN_HEIGHT - ROOT_HEIGHT) // 2
            self.geometry(
                f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'
                f'+{LEFT_BORDER_POS}+{UPPER_BORDER_POS}'
            )

    def make_move(self):
        """
        Try to make a move in the game, and add the codemaker response on the
        screen if successful.
        In case the combination is invalid, shows an information message
        telling the user to ensure the combination is valid.
        In case of win, ask the user wether he wants to keep playing or not.
        """

        try:
            # ask the guess frame for the current combination
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

        # evaluate the combination with the codemaker
        feedback = self.codemaker.codemaker(comb)

        # make a new frame for the last try, with comb and feeback
        new_result_frame = GuessResultFrame(
            self.top_frame, comb, feedback, self.ROOT_WIDTH
        )

        # delete old guess frames and replace them after the new one as been
        # inserted
        for curr_frame in self.result_frames:
            curr_frame.grid_forget()

        self.result_frames.pop(0)
        self.result_frames.append(new_result_frame)

        for i, curr_frame in enumerate(self.result_frames):
            curr_frame.grid(row=i, pady=2)

        # the player hasn't won yet
        if feedback != (common.LENGTH, 0):
            return

        # the player has won
        user_choice = messagebox.askyesno(
            'Fin de partie',
            'Bravo, vous avez gagné !\nVoulez vous rejouer ?',
            icon='info'
            )

        # restart the game or finish the window depeding on the user's choice
        if user_choice:
            self.reboot()
        else:
            self.quit()

    def reboot(self):
        """
        Starts a new game against the codemaker.
        This purges the guesses memory for the new game.
        """
        self.codemaker.init()
        print('Current combination :', self.codemaker.solution, flush=True)

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
            self, height=2, width=7,
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
            (CELL_WIDTH * 0.5) / max(n_lines, FEEDBACK_PER_LINE)
        )

        for index, feedback_color in enumerate(feedback_colors):

            y_pos, x_pos = divmod(index, FEEDBACK_PER_LINE)

            x_center = CELL_WIDTH * (x_pos + 1/2) - .7
            y_center = CELL_HEIGHT * (y_pos + 1/2) - .5

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
            height=2, width=7,
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
            self, from_=1, to=9, resolution=1, orient='horizontal',
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

    # réduire n_memory pour les écrans de faible hauteur afin que la fenêtre
    # ne soit pas trop grande verticalement
    window = GameWindow(codemaker1, n_memory=6)
    window.mainloop()

    common.LENGTH = OLD_LENGTH
    common.COLORS = OLD_COLORS
