""" Main routine for the program
    This program is intended for students that want to revise level 3 Calculus in the NCEA syllabus
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from hashlib import sha256
from difflib import SequenceMatcher
import datetime

from database import DB
from math_operations import Surds, ComplexNumbers, Polynomials, Differentiation


class App(tk.Tk):
    """ Root for the GUI
        Will contain all the frames for each individual screen that is to be shown
    """

    def __init__(self):
        """Call init from Tk class in tk's init. This makes this class the master or root window of the GUI.
            The default window size is set to be 1/4 of a 1080p 16:9 screen as the size is adequate and 1080p 16:9 is
            a very common screen size.
            The return or enter key is bind to the proceed button of each screen. This makes navigating the program
            for experienced users much quicker and easier.
        """
        tk.Tk.__init__(self)
        self.title('Level 3 Calculus Revision')
        self.geometry('960x540+0+0')

        self.bind('<Return>', lambda event: self.proceed())

        self.columnconfigure(0, weight=1)
        [self.rowconfigure(row, weight=weight) for row, weight in zip([0, 1], [1, 3])]

    # Set to static as tho it does not use any variables from the class but this class is the only one that uses it
    @staticmethod
    def proceed():
        name = type(current_screen[0]).__name__
        event_dict = {'IntroScreen': intro_screen.login, 'Signup': register_screen.register,
                      'MainMenu': screen_change, 'SelectMenu': select_menu.proceed,
                      'Question': question.frame_check, 'ResultsScreen': screen_change}

        if name == 'MainMenu':
            return event_dict[name](current_screen, select_menu)

        elif name == 'ResultsScreen':
            return event_dict[name](current_screen, main_menu)

        else:
            return event_dict[name]()


class Header(tk.Frame):
    """The header will stay on throughout the whole program hence why it is another class"""
    def __init__(self, master):
        tk.Frame.__init__(self, master, background='#00a876')
        style = ttk.Style()
        style.configure('header.TLabel', background='black', font=('Helvetica', 40), foreground='white')

        self.columnconfigure(0, weight=1)
        self.header_text = ttk.Label(self, text='Level 3 Calculus Revision',
                                     style='header.TLabel', anchor='center', padding=20)

    def grid_frames(self):
        self.grid(row=0, column=0, sticky='nsew')
        self.header_text.grid(row=0, column=0, sticky='nsew')


class IntroScreen(tk.Frame):
    """This screen is the login screen.
    """

    def __init__(self, master):
        """The entry boxes could not be styled with ttk as it made customisation a lot harder to due some missing
            features that are included in the normal entry widget.
            The current_user is imported into the class through parameters instead of the use of global as it is better
            practice to keep my variables as localised as possible. This is because having many global variables
            will cause errors such as namespace, resulting in very messy or spaghetti code.
        """
        tk.Frame.__init__(self, master=master, background='#00a876')

        self.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('login.TLabel', background='#00a876', foreground='white', font=('Helvetica', 20))
        style.configure('TButton', foreground='#00a876', font=('Helvetica', 10, 'bold'), relief='flat')

        self.login_frame = tk.Frame(self, background='#00a876')
        self.login_frame.columnconfigure(0, weight=1)
        self.login_text = ttk.Label(self.login_frame, text='Login or Create an Account',
                                    style='login.TLabel', font=('Helvetica', 30))
        self.username_text = ttk.Label(self.login_frame, text='Username:', style='login.TLabel')
        self.username_entry = tk.Entry(self.login_frame, font=('Helvetica', 15), foreground='#00a876', justify='center')
        self.password_text = ttk.Label(self.login_frame, text='Password:', style='login.TLabel')
        self.password_entry = ttk.Entry(self.login_frame, font=('Helvetica', 15), foreground='#00a876',
                                        justify='center', show='*')

        self.buttons_frame = tk.Frame(self.login_frame, background='#00a876')
        self.register_button = ttk.Button(self.buttons_frame, text='Register', style='TButton',
                                          command=lambda: screen_change(current_screen, register_screen))
        self.login_button = ttk.Button(self.buttons_frame, text='Login', style='TButton',
                                       command=self.login)

    def login(self):
        """To check the password it will try and match the hashed value of users value with the already hashed actual
            password in the database
        """
        if self.username_entry.get() and self.password_entry.get():
            for existing_user in users:
                if self.username_entry.get() != existing_user.username or \
                   hash_password(self.password_entry.get()) != existing_user.password:
                    messagebox.showerror('Error', 'Incorrect username or password')
                    return

                else:
                    [widget.delete(0, 'end') for widget in [self.username_entry, self.password_entry]]
                    current_user.append(existing_user)
                    main_menu.tv_configure()
                    screen_change(current_screen, main_menu)
                    return

        else:
            messagebox.showerror('Error', 'Please enter your username or password')
            return

    def grid_frames(self):
        self.grid(row=1, column=0, sticky='nsew')

        self.login_frame.grid(row=1, column=0, sticky='nsew')
        self.login_text.grid(row=0, column=0, pady=20)

        self.username_text.grid(row=1, column=0)
        self.username_entry.grid(row=2, column=0)

        self.password_text.grid(row=3, column=0)
        self.password_entry.grid(row=4, column=0)

        self.buttons_frame.grid(row=5, column=0, pady=10)
        self.register_button.grid(row=0, column=0, padx=20)
        self.login_button.grid(row=0, column=1, padx=20)

        self.username_entry.focus_set()


class Signup(tk.Frame):
    """Also known as the register screen
        The user password is hidden and can be revealed by the show password button which will be explained below.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master=master, background='#00a876')

        self.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('register.TLabel', background='#00a876', foreground='white', font=('Helvetica', 20))

        self.back_button = ttk.Button(self, text='Back', style='TButton', command=self.back)
        self.register_text = ttk.Label(self, text='Please enter your details',
                                       style='register.TLabel', font=('Helvetica', 30))
        self.name_text = ttk.Label(self, text='Name:', style='register.TLabel')
        self.name_entry = tk.Entry(self, font=('Helvetica', 15), foreground='#00a876', justify='center')

        self.username_text = ttk.Label(self, text='Username:', style='register.TLabel')
        self.username_entry = tk.Entry(self, font=('Helvetica', 15), foreground='#00a876', justify='center')
        
        self.password_text = ttk.Label(self, text='Password:', style='register.TLabel')
        self.password_restriction = ttk.Label(self, text='Please enter 8 or more characters', style='register.TLabel',
                                              font=('Helvetica', 10))
        self.password_entry = tk.Entry(self, font=('Helvetica', 15), foreground='#00a876', justify='center', show='*')

        self.show_password_button = ttk.Button(self, text='Show password', style='TButton')
        self.register_button = ttk.Button(self, text='Register', style='TButton', command=self.register)

    def back(self):
        """Pressing the back button will clear the entry boxes to prevent other users from checking what the previous
        user entered and other security flaws like that."""
        [widget.delete(0, 'end') for widget in [intro_screen.username_entry, intro_screen.password_entry]]
        screen_change(current_screen, intro_screen)
        [widget.delete(0, 'end') for widget in [self.name_entry, self.username_entry, self.password_entry]]

    def register(self):
        for existing_user in users:
            if not self.name_entry.get():
                messagebox.showerror('Error', 'Please enter your name')
                return

            elif not self.username_entry.get() or not self.password_entry.get():
                messagebox.showerror('Error', 'Please enter your desired username or password')
                return

            elif existing_user.username == self.username_entry.get():
                messagebox.showerror('Error', 'This username has been taken')
                return

            elif len(self.password_entry.get()) < 8:
                messagebox.showerror('Error', 'Your password is shorter than 8 characters')
                return

        db.add_user(len(users), self.name_entry.get(), self.username_entry.get(),
                    hash_password(self.password_entry.get()))

        update_users(users)

        messagebox.showinfo('Registration success!', 'You have successfully registered your account')

        self.back()

    def grid_frames(self):
        self.back_button.grid(row=0, column=0, sticky='nw', padx=20)

        self.register_text.grid(row=1, column=0)

        self.name_text.grid(row=2, column=0)
        self.name_entry.grid(row=3, column=0)

        self.username_text.grid(row=4, column=0)
        self.username_entry.grid(row=5, column=0)

        self.password_text.grid(row=6, column=0)
        self.password_restriction.grid(row=7, column=0)
        self.password_entry.grid(row=8, column=0)

        self.show_password_button.grid(row=8, column=1, sticky='w')
        self.show_password_button.bind('<ButtonPress-1>', lambda event: self.password_entry.configure(show=''))
        self.show_password_button.bind('<ButtonRelease-1>', lambda event: self.password_entry.configure(show='*'))

        self.register_button.grid(row=9, column=0, pady=10)


class MainMenu(tk.Frame):
    """Main menu of the program. Includes instructions on how to use the program, as well as the users' history /
        previous scores sorted by first date, then score.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master=master)

        style = ttk.Style()
        style.configure('description.TLabel', background='#00a876', foreground='black', font=('Helvetica', 11))
        style.configure('heading.TLabel', background='#00a876', foreground='white', font=('Helvetica', 20))

        self.columnconfigure([0, 1],  weight=1)
        [self.rowconfigure(row, weight=weight) for row, weight in zip([0, 1, 2], [1, 5, 1])]
        self.configure(background='#00a876')

        self.top_left_frame = tk.Frame(self, background='#00a876')
        [self.top_left_frame.columnconfigure(column, weight=weight) for column, weight in zip([0, 1], [1, 5])]

        self.logout_button = ttk.Button(self.top_left_frame, text='Logout', style='TButton', command=self.logout)
        text = None
        self.description_title = ttk.Label(self.top_left_frame, text=text, style='heading.TLabel')

        # The text is formatted to look nicer on the program itself. It saves the trouble of going through padding.
        text = """This program is meant for revision of the fundamentals that are in Level 3 Calculus. 
To enter an answer, please follow our guidelines below:

    1) Powers are represented as x^(y)
    2) Square root, logs, ln, are sqrt(x), log(b)(x), ln(x) respectively
    3) For division, put the numerator and denominator in brackets, e.g. (x-y)/(x+y)
    4) For polynomials, write answer then r, followed  by the remainder, e.g. ax+brc
    5) For sin, cos, tan operators, the answer should be in the form a*sin(b)
    6) Decimals are rounded to the nearest 2 d.p
    
    Example answers:
    Surds - 48*sqrt(2)
    Complex Numbers - 5+5i or 5*cis(5)
    Polynomials - 5x+5r5
    Differentiation - 5*sec^2(5x)
    """
        self.description_text = ttk.Label(self, text=text, style='description.TLabel')

        self.user_scores_title = ttk.Label(self, text='You previous scores:',
                                           style='heading.TLabel')
        self.user_scores_tv = ttk.Treeview(self)

        self.proceed_button = ttk.Button(self, text='Proceed', style='TButton',
                                         command=lambda: screen_change(current_screen, select_menu))

    def tv_configure(self):
        self.user_scores_tv['columns'] = ('score', 'date')

        self.user_scores_tv.heading('#0', text='Subject', anchor='w')
        self.user_scores_tv.column('#0', anchor='w')

        self.user_scores_tv.heading('score', text='Score')
        self.user_scores_tv.column('score', anchor='center', width=50)

        self.user_scores_tv.heading('date', text='Date')
        self.user_scores_tv.column('date', anchor='w', width=100)

    def tv_insert(self):
        self.user_scores_tv.delete(*self.user_scores_tv.get_children())

        update_scores(scores)
        scores.sort(key=lambda score: (score.date, score.score), reverse=True)

        [self.user_scores_tv.insert('', 'end', text=score.subject, values=(score.score, score.date))
         for score in scores]

    @staticmethod
    def logout():
        """Static method as it really doesn't utilise any local variables in this class, but the function is only used
            in this class.
        """
        current_user.clear()
        scores.clear()
        screen_change(current_screen, intro_screen)

    def grid_frames(self):
        self.description_title['text'] = f'Welcome {current_user[0].name}'

        self.tv_insert()  # Convenient place to put the call as it is only needed every time grid_frames() is called

        self.top_left_frame.grid(row=0, column=0, sticky='nsew')
        self.logout_button.grid(row=0, column=0)
        self.description_title.grid(row=1, column=1)
        self.description_text.grid(row=1, column=0, sticky='nsew', padx=20)
        self.user_scores_title.grid(row=0, column=1)
        self.user_scores_tv.grid(row=1, column=1, sticky='nsew', padx=20)

        self.proceed_button.grid(row=2, column=1, sticky='e', padx=20)


class SelectMenu(tk.Frame):
    """For the style of this select menu, I decided to go with a more clean look of having the radio buttons as a huge
        layout. This improves the bland look of the default radio buttons.
        A list is used for the radio buttons as it is about 30% more efficient to iterate over a list than a dictionary.
        Python 3 likes to create a view of the dictionary before iteration hence the slower performance. In this case, 
        the increase in speed is almost negligible since there are only 4 items in the list but it is good to maintain
        good practice.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master=master, background='#00a876')

        self.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.rowconfigure(1, weight=1)

        style = ttk.Style()
        style.configure('title.TLabel', background='#00a876', foreground='black', font=('Helvetica', 20))

        self.back_button = ttk.Button(self, text='Back', style='TButton',
                                      command=lambda: screen_change(current_screen, main_menu))
        self.select_text = ttk.Label(self, text='Please choose a subject:', style='title.TLabel')

        self.radio_buttons_frame = tk.Frame(self, background='#00a876')
        self.radio_buttons_frame.columnconfigure([0, 1, 2, 3], weight=1)
        self.radio_buttons_frame.rowconfigure(0, weight=1)
        
        self.var = tk.StringVar()
        self.var.set('0')

        # Long spacing in the string so the boxes are roughly the same size
        radio_buttons = ['         Surds         ', 'Complex Numbers', '  Polynomials  ', 'Differentiation']

        self.radio_buttons = [tk.Radiobutton(self.radio_buttons_frame, text=text, variable=self.var, value=value,
                                             indicator=0, selectcolor='#00a876')
                              for value, text in enumerate(radio_buttons)]

        self.proceed_button = ttk.Button(self, text='Proceed', style='TButton', command=self.proceed)

    def proceed(self):
        question.subject = self.var.get()
        screen_change(current_screen, question)

    def grid_frames(self):
        self.back_button.grid(row=0, column=0, sticky='nw', padx=20)
        self.select_text.grid(row=0, column=2, sticky='nsew', columnspan=3, pady=10)

        self.radio_buttons_frame.grid(row=1, column=0, columnspan=5, sticky='nsew')
        [widget.grid(row=0, column=index, sticky='nsew', padx=20) for index, widget in enumerate(self.radio_buttons)]
        self.proceed_button.grid(row=2, column=4, sticky='w', pady=10)


class Question(tk.Frame):
    """The question frame is just a sort of main frame of placeholder for the question objects. Though the visual effect
        is not affected, on the backend it makes more sense as it seems more organised in this way as compared to
        replacing the question object, hence better practice. This method also makes much more sense as I can store
        the question objects in a list to go through when calculating the results. If I were to store the data in the
        results class, it would result in very messy code and scuffed methods of grid-ing the result frame when needed.
        The quiz length is going to be 5 questions long. This means that after 5 runs or replacements of the question
        frame, the questions list will need to be cleared as this instance of the question class will remain througout
        the whole program.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master=master, background='#00a876')

        self.columnconfigure(0, weight=1)
        [self.rowconfigure(row, weight=weight) for row, weight in zip([0, 1], [1, 3])]

        self.counter = ttk.Label(self, text='0/5 Questions Answered', style='title.TLabel')

        self.subject = None

        self.questions = []

    def frame_check(self):
        if not self.questions[len(self.questions) - 1].answer_entry.get():
            messagebox.showerror('Error', 'Please do not leave answer field empty')
            return

        if self.questions[len(self.questions) - 1].submit_button['text'] == 'Submit answer':
            self.questions[len(self.questions) - 1].show_answer()
            return

        if len(self.questions) == 5:
            results.user_answers = self.questions[:]
            results.subject = self.questions[4].var_dict[self.subject]
            self.questions.clear()
            results.get_results()
            screen_change(current_screen, results)
            self.counter['text'] = '0/5 Questions Answered'
            return

        self.counter['text'] = f'{len(self.questions)}/5 Questions Answered'
        self.grid_frames()

    def grid_frames(self):
        self.counter.grid(row=0, column=0, sticky='ne', padx=20)
        if self.questions:
            self.questions[len(self.questions) - 2].grid_forget()

        self.questions.append(QuestionObj(parent=self, subject=self.subject))
        self.questions[len(self.questions) - 1].grid(row=1, column=0, sticky='nsew')
        self.questions[len(self.questions) - 1].var.set(self.questions[len(self.questions) - 1].var_dict[self.subject])
        self.questions[len(self.questions) - 1].grid_frames()


class QuestionObj(tk.Frame):
    """This class usage is described above in the question class. In a nutshell, the question class abuses the fact this
        is an instance variable meaning I am able to reuse the same class as many times as I like.
        Itself contains the class it is using from math operations. Because it gets the instance of that class, I am
        able to later access the class methods set up in that class from math operations.
    """
    def __init__(self, parent, subject):
        tk.Frame.__init__(self, master=parent, background='#00a876')
        self.parent = parent
        self.user_answers = None
        self.var_dict = {'0': Surds(3), '1': ComplexNumbers(), '2': Polynomials(), '3': Differentiation()}
        self.subject = self.var_dict[subject]

        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1, 2], weight=1)

        self.var = tk.StringVar()
        self.answer_var = tk.StringVar()
        self.question = ttk.Label(self, textvariable=self.var, style='title.TLabel')
        self.answer_entry = ttk.Entry(self)
        self.answer = ttk.Label(self, textvariable=self.answer_var, style='title.TLabel')

        self.submit_button = ttk.Button(self, text='Submit answer', style='TButton',
                                        command=lambda: self.parent.frame_check)

    def show_answer(self):
        if SequenceMatcher(None, self.subject.get_answer(), self.answer_entry.get()).ratio() > (3 / 4):
            answer = 'You are correct'

        else:
            answer = f'You are incorrect. The answer was {self.subject.get_answer()}'

        self.answer_var.set(answer)
        self.answer.grid(row=2, column=0)
        self.submit_button['text'] = 'Next'

    def grid_frames(self):
        self.question.grid(row=0, column=0, sticky='s', pady=10)
        self.answer_entry.grid(row=1, column=0, sticky='n', pady=10)
        self.submit_button.grid(row=3, column=0, sticky='e', padx=20, pady=10)

        self.answer_entry.focus_set()


class ResultsScreen(tk.Frame):
    """A very simple frame. To calculate the results, it uses string similarity to check for a similarity index of at
        least 0.75. This means that 1/4 of the string can be different. This exception may be a bit too high as a tiny
        bit of wrong answers will make it through but considering how annoying typos are, it should work out in the
        end for the end user.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master=master, background='#00a876')
        self.user_answers = []
        self.subject = None
        self.results = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1, 2], weight=1)

        self.results_label = ttk.Label(self, text='Here are your results', style='title.TLabel', anchor='center')
        self.user_results = ttk.Label(self, textvariable=self.results, style='title.TLabel', anchor='center')
        self.return_button = ttk.Button(self, text='Return', style='TButton',
                                        command=lambda: screen_change(current_screen, main_menu))

    def get_results(self):
        count = 0
        for answer in self.user_answers:
            ratio = SequenceMatcher(None, answer.subject.get_answer(), answer.answer_entry.get()).ratio()
            if ratio > (3 / 4):
                count += 1
        self.results.set(f'You have scored {count} out of 5')

        db.add_score(current_user[0].user_id, datetime.date.today(),
                     self.subject.__class__.__name__, count)

    def grid_frames(self):
        self.results_label.grid(row=0, column=0, sticky='nsew')
        self.user_results.grid(row=1, column=0, sticky='nsew')
        self.return_button.grid(row=2, column=0, sticky='e', padx=20, pady=10)


class User:
    """Parse the data of the login from the database into an object for each user. Makes accessing the information
        as well as managing it easier.
    """
    def __init__(self, user_data):
        self.user_id = user_data[0]
        self.name = user_data[1]
        self.username = user_data[2]
        self.password = user_data[3]


def update_users(user_list):
    user_list.clear()
    login_creds = db.fetch('login_creds')
    if login_creds:
        for user in login_creds:
            user_list.append(User(user))


def hash_password(password):
    """Method of encryption where the only logical way to hack is to brute force it as decryption is impossible due to
        password being hashed."""
    return sha256(password.encode()).hexdigest()


class Scores:
    """Like the User class, parsing the data makes it easy to access as each score becomes an object. Indexing through
        a very big 2d list of scores is very messy as it would require a lot of loops to achieve the same thing. The
        speed difference is also almost negligible, though the end user won't notice any delay until the scores database
        gets very very big.
    """
    def __init__(self, score_set):
        self.user_id = score_set[0]
        self.date = score_set[1]
        self.subject = score_set[2]
        self.score = score_set[3]


def update_scores(user_list):
    user_list.clear()
    user_scores = db.fetch('scores', user_id=current_user[0].user_id)
    if user_scores:
        for score in user_scores:
            user_list.append(Scores(score))


def screen_change(screen, new_screen):
    """Function that forgets the current screen and replaces it with the desired screen
       The frames are not destroyed as they will be reused and there is no point in destroying it
    """
    screen[0].grid_forget()
    screen[0] = new_screen
    screen[0].grid(row=1, column=0, sticky='nsew')
    screen[0].grid_frames()
    return


# These are the main classes. As they are the main classes, they only need to be initialised once, hence why there are
# initialised here. This works out as each instance may be used in other classes and the permeability of classes is
# not taken into consideration.
db = DB()
app = App()
header = Header(master=app)
intro_screen = IntroScreen(master=app)
register_screen = Signup(master=app)
main_menu = MainMenu(master=app)
select_menu = SelectMenu(master=app)
question = Question(master=app)
results = ResultsScreen(master=app)

# Setting the current screen to the login screen as that is the first screen the user is shown on program
# run/start
current_user = []
current_screen = [intro_screen]

# Takes the check from the initialisation of the DB class and checks if it is empty, if so meaning the tables need
# to be initialised
if not db.check:
    db.initialise()

users = []
scores = []
update_users(users)

header.grid_frames()
intro_screen.grid_frames()
app.mainloop()
