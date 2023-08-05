def popup_macos(title, content):
    # import os
    # script = 'osascript -e '
    # args = "'display notification \"{}\" with title \"{}\"'".format(content, title)
    # os.system(script + args)
    print(content)

def popup(title, content):
    import tkinter
    import tkinter.scrolledtext
    win = tkinter.Tk()
    win.title(title)
    frame = tkinter.Frame(master=win, bg='#808000')
    frame.pack(fill='both', expand='yes')
    editArea = tkinter.scrolledtext.ScrolledText(
        master=frame, wrap=tkinter.WORD, width=80, height=40)
    editArea.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)
    editArea.insert(tkinter.INSERT, content)
    editArea.configure(state="disabled")
    win.mainloop()


class Logger(object):
    """
    """
    ERROR = '__AVA__PLUGIN__ERROR__'
    IMPORT = '__AVA__PLUGIN__IMPORT__'
    REQUEST = '__AVA__PLUGIN__REQUEST__'
    RESPONSE = '__AVA__PLUGIN__RESPONSE__'
    DELIMITER = '__AVA__PLUGIN__DELIMITER__'

    @staticmethod
    def log_error():
        print(Logger.ERROR)
        print(Logger.DELIMITER)

    @staticmethod
    def log_import():
        print(Logger.IMPORT)
        print(Logger.DELIMITER)

    @staticmethod
    def log_request():
        print(Logger.REQUEST)
        print(Logger.DELIMITER)

    @staticmethod
    def log_response():
        print(Logger.RESPONSE)
        print(Logger.DELIMITER)

    @staticmethod
    def unexpected_error(self):
        return 'An unexpected error occured with the {0}. The error has been print.'.format(
            self.__class__.__name__)

    @staticmethod
    def popup(title, content):
        import platform
        if platform.system() == 'Darwin':
            import threading
            t = threading.Thread(target=popup_macos, args=(title, content))
            t.daemon = True
            t.start()
            return
        import multiprocessing
        p = multiprocessing.Process(
            name='AVA.popup.{0}'.format(title),
            target=popup,
            args=(title, content))
        p.daemon = True
        p.start()
