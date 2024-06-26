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
        self.bind('<Escape>', lambda _: self.quit())

    def make_window(self, *, init=False):
        """
        Make (and refresh) the window with the last settings for the game.

        init : used to specify that this is the first making of the window,
        shouldn't be used once the window is fully created and displayed. Its
        main purpose is to avoid flickering when refreshing the window.
        """

        global FEEDBACK_PER_LINE
        FEEDBACK_PER_LINE = max(round(common.LENGTH ** 0.5), 2)
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()

        if init:
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
                f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'+
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
                f'{self.ROOT_WIDTH}x{ROOT_HEIGHT}'+
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
                detail='Assurez vous d\'avoir rentré '+
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
        # initialise the codemaker and cheat by showing to the user the
        # combination
        self.codemaker.init()
        print('Current combination :', self.codemaker.solution, flush=True)

        # remove all former guesses (if any)
        for curr_frame in self.result_frames:
            curr_frame.destroy()

        # create new blank guess frames
        self.result_frames = []
        for i in range(self.n_memory):
            curr_frame = GuessResultFrame(
                self.top_frame, '', (0, 0), self.ROOT_WIDTH
            )
            curr_frame.grid(row=i, pady=2)
            self.result_frames.append(curr_frame)

    def reset(self):
        """
        Reloads the whole window, used to update the window when settings
        are changed.
        """
        # destroy old color_frame and curr_guess_frame (and other if any)
        # without destroying the settings frame
        for child in self.bottom_frame.winfo_children():
            if child != self.settings_frame:
                child.destroy()
        self.make_window()  # rebuild the window
        self.reboot()  # start a new game


class GuessResultFrame(tk.Frame):

    """
    This frame stores a previously played (or blank) move of the user.
    It shows both the played combination and the feedback given by the
    codemaker.
    """

    def __init__(self, parent, combination, feedback, ROOT_WIDTH):
        """
        Build the frame with the combination and the feedback.
        Uses ROOT_WIDTH to be able to resize its components without overflowing
        from its parent.
        """

        super().__init__(parent)
        self['bg'] = parent['bg']

        # this button serves as a reference for minimal height or width of
        # some widgets (here the feedback canvas)
        placeholder_button = tk.Button(
            self, height=2, width=7,
        )

        # the feedback canvas will be the same size as the button
        FEEDBACK_WIDTH = placeholder_button.winfo_reqwidth()
        FEEDBACK_HEIGHT = placeholder_button.winfo_reqheight()

        feedback_canvas = tk.Canvas(
            self, width=FEEDBACK_WIDTH, height=FEEDBACK_HEIGHT,
            bg=CONTOUR_COLOR,
            border=0, highlightthickness=0
        )

        # make a list of colors for the feedback pegs
        # white stands for a well placed colors
        # red stands for a badly placed colors
        feedback_colors = ['white'] * feedback[0] + ['red'] * feedback[1]
        # fill the missing pegs with a default color
        feedback_colors += ['#f0b27a'] * (common.LENGTH - len(feedback_colors))

        # each cell will contain a feedback peg
        CELL_WIDTH = FEEDBACK_WIDTH / FEEDBACK_PER_LINE
        n_lines = math.ceil(common.LENGTH / FEEDBACK_PER_LINE)
        CELL_HEIGHT = FEEDBACK_HEIGHT / n_lines

        # pegs are circles of radius FEEDBACK_RADIUS
        FEEDBACK_RADIUS = math.ceil(
            (CELL_WIDTH * 0.5) / max(n_lines, FEEDBACK_PER_LINE)
        )

        # create and place each peg
        # index is used for placement
        # feeback_color is for the color of the peg
        for index, feedback_color in enumerate(feedback_colors):

            # get the position of the peg on a rectangle
            y_pos, x_pos = divmod(index, FEEDBACK_PER_LINE)

            # coordinates of the center of the cell
            x_center = CELL_WIDTH * (x_pos + 1/2) - .7
            y_center = CELL_HEIGHT * (y_pos + 1/2) - .5

            # coordinates of the border of the circle for the canvas
            top_left = (x_center - FEEDBACK_RADIUS, y_center - FEEDBACK_RADIUS)
            bottom_right = (
                x_center + FEEDBACK_RADIUS, y_center + FEEDBACK_RADIUS
            )

            # create a circular peg of feedback_color
            feedback_canvas.create_oval(
                *top_left, *bottom_right,
                fill=feedback_color, width=0
                )

        feedback_canvas.grid(row=0, column=1, padx=5, pady=PADY_VALUE)

        # create the canvas that will contain the played combination
        # takes 95% of the remaining width
        CANVAS_WIDTH = (ROOT_WIDTH - FEEDBACK_WIDTH) * 0.95
        CANVAS_HEIGHT = FEEDBACK_HEIGHT  # same height as the feedback canvas

        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='#d38053', highlightbackground=CONTOUR_COLOR,
            border=0, highlightthickness=3,
        )
        self.choices_canvas.grid(row=0, column=0, padx=5)

        # there are common.LENGTH cells in the canvas
        CELL_WIDTH = CANVAS_WIDTH / common.LENGTH
        CELL_HEIGHT = CANVAS_HEIGHT

        # each color of the combination is shown in a circle
        CIRCLE_RADIUS = (CELL_HEIGHT * 0.8) / 2

        # get the hex code of the color associated with each color_value
        color_names = [
            COLORS_CONVERSION[color_value][1][0]
            for color_value in combination
        ]

        # create and place each color circle
        for cell_num, color_name in zip(range(common.LENGTH), color_names):

            # coordinates of the center of the cell
            x_center = CELL_WIDTH * (cell_num + 1/2) + 2
            y_center = CELL_HEIGHT / 2 + 2

            # coordinates of the border of the circle for the canvas
            top_left = (round(x_center - CIRCLE_RADIUS), y_center - CIRCLE_RADIUS)
            bottom_right = (round(x_center + CIRCLE_RADIUS), y_center + CIRCLE_RADIUS)

            # create a circle for the color
            self.choices_canvas.create_oval(
                *top_left, *bottom_right,
                fill=color_name, width=0
            )


class CurrGuessFrame(tk.Frame):

    """
    This frame allows the user to make a move (thanks to a button).
    It shows the current combination.

    It takes a color selector as an argument and will call it to get the
    currently selected color when a color circle is clicked in the canvas.
    """

    def __init__(self, parent, color_selector, ROOT_WIDTH):
        """
        Build the frame with the combination and a validation button.
        Uses ROOT_WIDTH to be able to resize its components without overflowing
        from its parent.
        """

        super().__init__(parent)
        self['bg'] = parent['bg']

        # stores the color selector that will be called to know which color
        # is currently selected
        self.color_selector = color_selector
        # stores the current theoretical combination
        self.colors_value = [""] * common.LENGTH

        # make the button that allows to validate the current combination
        self.check_button = tk.Button(
            self, text='Valider',
            bg='#27ff00', activebackground='#a7ff96',
            highlightbackground='#a7ff96',
            relief=tk.FLAT, overrelief=tk.RIDGE,
            height=2, width=7,
        )
        self.check_button.grid(row=0, column=1, padx=5, pady=PADY_VALUE)

        # stores the button dimensions
        BUTTON_WIDTH = self.check_button.winfo_reqwidth()
        BUTTON_HEIGHT = self.check_button.winfo_reqheight()

        # and use them to get the canvas dimensions
        CANVAS_WIDTH = (ROOT_WIDTH - BUTTON_WIDTH) * 0.95
        CANVAS_HEIGHT = BUTTON_HEIGHT

        # create the canvas were the combination will be displayed
        self.choices_canvas = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg='#d38053', highlightbackground=CONTOUR_COLOR,
            border=0, highlightthickness=3,
        )
        self.choices_canvas.grid(row=0, column=0, padx=5)

        # there are common.LENGTH cells in the canvas
        CELL_WIDTH = CANVAS_WIDTH / common.LENGTH
        CELL_HEIGHT = CANVAS_HEIGHT

        # each color of the combination is shown in a circle
        CIRCLE_RADIUS = (CELL_HEIGHT * 0.8) / 2

        # create and place each color circle
        for cell_num in range(common.LENGTH):

            # coordinates of the center of the cell
            x_center = CELL_WIDTH * (cell_num + 1/2) + 2
            y_center = CELL_HEIGHT / 2 + 2

            # coordinates of the border of the circle for the canvas
            top_left = (round(x_center - CIRCLE_RADIUS), y_center - CIRCLE_RADIUS)
            bottom_right = (round(x_center + CIRCLE_RADIUS), y_center + CIRCLE_RADIUS)

            # create a circle for the color
            circle_id = self.choices_canvas.create_oval(
                *top_left, *bottom_right,
                fill='white', width=0
            )
            # bind each circle to the mouse
            # will call the function that changes the color of a circle
            self.choices_canvas.tag_bind(
                circle_id, '<Button-1>', func=self.change_choice_color
            )

    def set_command(self, func):
        """
        Set the validation button function.
        Should be used by a parent manage the game behaviour.
        """
        self.check_button['command'] = func

    def change_choice_color(self, event):
        """
        Get the current color from the color selector and changes the color
        of the current guess circle that has been clicked.
        """

        # get the circle that has been clicked
        circle_id, = self.choices_canvas.find_closest(event.x, event.y)
        # get the new color value
        color_value = self.color_selector.get_value()
        # update the stored combination
        self.colors_value[circle_id - 1] = color_value
        # get the hex code of the color
        _, (color_name, _), _ = COLORS_CONVERSION[color_value]
        self.choices_canvas.itemconfigure(
            circle_id, fill=color_name  # change the circle color
        )

    def get_combination(self):
        """
        Returns the current combination
        """
        # if the combination isn't fully defined, raise an error
        if "" in self.colors_value:
            raise InvalidCombinationError(self.colors_value)
        # else return a string of the combination
        return ''.join(self.colors_value)


class ColorSelectionFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=parent['bg'],
            highlightbackground=CONTOUR_COLOR, highlightthickness=5
        )

        # tkinter StrinVar stores the current selected color
        self.curr_color = tk.StringVar(value=common.COLORS[0])

        # create and place each color button
        for index, color in enumerate(common.COLORS):

            # get all the color attributes
            color_name, bg_colors, fg_color = COLORS_CONVERSION[color]
            default_bg, active_bg = bg_colors  # unpack backgroud colors

            # creating the radiobutton
            button = tk.Radiobutton(
                self, value=color, indicatoron=False, text=color_name,
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

    def get_value(self):
        """
        Returns the current selected color value
        """
        return self.curr_color.get()


class SettingsFrame(tk.LabelFrame):
    """
    This frame is used to control the game settings with scales widget.
    It communicates with its parent by taking a `parent_update` argument that
    will be called when a setting changes in order to update the window with
    the made change.
    """

    def __init__(self, parent, parent_update):
        """
        Build the frame with both settings scales.
        `parent_update` will be called when a setting changes to refresh the
        main window.
        """
        super().__init__(
            parent, text='Paramètres de jeu', labelanchor='n',
            fg='white',
            bg=parent['bg'], bd=0,
            highlightbackground=CONTOUR_COLOR, highlightthickness=2,
            )
        self.parent_update = parent_update

        # create the scales
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

        # set the initial values
        self.length_box.set(common.LENGTH)
        self.colors_box.set(len(OLD_COLORS))

        # set the command for both scales
        self.length_box['command'] = self.update_settings
        self.colors_box['command'] = self.update_settings

        # place the scales
        self.length_box.grid(row=0, pady=3, padx=3)
        self.colors_box.grid(row=1, pady=3)

        # update the main window after it is ready to be refreshed
        # (5ms should be enough for the program to be ready)
        self.after(5, self.update_settings, None)

    def update_settings(self, _):
        # used for comparison, ensure to update the window only and only if
        # these values have actually changed
        old_values = (common.LENGTH, common.COLORS[:])

        # get changed values
        common.LENGTH = self.length_box.get()
        nb_colors = self.colors_box.get()
        common.COLORS = AVAILABLE_COLORS[:nb_colors]

        # refresh the window only if the values have changed
        if old_values != (common.LENGTH, common.COLORS):
            self.parent_update()


if __name__ == '__main__':

    # store the original setting of common to be able to restore them after they
    # have been modified when playing
    OLD_COLORS = common.COLORS[:]
    OLD_LENGTH = common.LENGTH

    import codemaker1

    # réduire n_memory pour les écrans de faible hauteur afin que la fenêtre
    # ne soit pas trop grande verticalement
    window = GameWindow(codemaker1, n_memory=6)
    window.mainloop()

    # on remet les valeurs initiales après exécution du programme
    common.LENGTH = OLD_LENGTH
    common.COLORS = OLD_COLORS
