"""
This module defines a base-object for building proton apps using html/css and javascript.
"""

from cefpython3 import cefpython as cef
from werkzeug.serving import run_simple
from threading import Thread

import platform
import sys
import win32con  # todo figure out a nice way of making the functionality used from win32 cross-platform
import win32gui
import win32api
import threading
import os
import queue
import atexit
import os

# todo: bind_to_window is still here even though I've sort of decided I would just expose all functions of the object
def bind_to_window(fun):
    fun.bind_to_window = True
    return fun


def prevent_bind_to_window(fun):
    fun.bind_to_window = True
    return fun


def argument_python_to_javascript(arg):
    if type(arg) is str:
        return '"' + arg + '"'
    else:
        return str(arg)


def daemon_threaded(fun):
    def wrapped(*args, **kwargs):
        t = Thread(target=fun, args=args, daemon=True)  # Offload work and return imidiately en order to not block the gui
        t.start()
    return wrapped


def enum_handler(hwnd, results):
    results[hwnd] = {
        "title": win32gui.GetWindowText(hwnd),
        "visible": win32gui.IsWindowVisible(hwnd),
        "minimized": win32gui.IsIconic(hwnd),
        "rectangle": win32gui.GetWindowRect(hwnd),  # (left, top, right, bottom)
        "next": win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)  # Window handle to below window
    }


def get_windows():
    enumerated_windows = {}
    win32gui.EnumWindows(enum_handler, enumerated_windows)
    return enumerated_windows


def get_window_by_title(title):
    windows = get_windows()
    gotten = next(win for win in windows if windows[win]['title'] == title)
    return gotten


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def load_icon_from_file(iconPath):
    hinst = win32api.GetModuleHandle(None)
    icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
    hicon = win32gui.LoadImage(hinst, iconPath, win32con.IMAGE_ICON, 0, 0, icon_flags, )
    return hicon


class LoadHandler(object):
    def __init__(self, on_load_function=None, window_title="", window_dimensions=(800, 500)):
        self.window_dimensions = window_dimensions
        self.window_title = window_title
        self.on_load_function = on_load_function
        self.windowfixed = False

    def OnBeforeResourceLoad(self, browser, **_):
        if not self.windowfixed:
            app_width = self.window_dimensions[0]    # 1600
            app_height = self.window_dimensions[1]    # 932

            # hwnd = win32gui.GetForegroundWindow()
            hwnd = get_window_by_title(self.window_title)

            win32gui.MoveWindow(hwnd, 0, 0, app_width, app_height, True)

            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            style &= ~win32con.WS_SIZEBOX
            # style &= ~win32con.WS_MINIMIZEBOX
            style &= ~win32con.WS_MAXIMIZEBOX
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)


            icon_path =  os.path.dirname(os.path.abspath(__file__)) + r"\..\resources\icon.ico"

            icon = load_icon_from_file(icon_path)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, icon)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, icon)

            # win32gui.SendMessage(win32gui.GetWindowDC(hwnd), win32con.WM_SETICON, win32con.ICON_SMALL, icon)
            # win32gui.SendMessage(win32gui.GetWindowDC(hwnd), win32con.WM_SETICON, win32con.ICON_BIG, icon)

            # hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
            flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
            nid = (hwnd, 0, flags, win32con.WM_USER + 20, icon, "Python Demo")
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)


            def destroy_icon(icon):
                win32gui.DestroyIcon(icon)
            atexit.register(destroy_icon, icon)

            print('done loading')
            self.windowfixed = True

    def OnLoadEnd(self, browser, frame, http_code):
        if frame.IsMain():
            if self.on_load_function is not None:
                self.on_load_function()

class PysitronApp:
    def __init__(self, landing_page='', target_url = '', window_title=None, port_number=None, window_dimensions = (400, 300)):
        self.window_dimensions = window_dimensions
        self.port_number = get_open_port() if port_number is None else port_number
        self.default_text = landing_page
        self.window_title = window_title if window_title is not None else self.__class__.__name__
        self.target_url = target_url
        self.javascript_bound = False
        self.bindings = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)
        self.queue = queue.Queue()

        check_versions()
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.DpiAware.SetProcessDpiAware()
        cef.Initialize(settings={'context_menu': {'enabled': True}, 'auto_zooming': 'system_dpi', 'multi_threaded_message_loop':True})
        browser = None
        postqueue = queue.Queue()

        def create_browser():
            print('Serving on localhost:' + str(self.port_number))
            postqueue.put(cef.CreateBrowserSync(url=r"http://localhost:" + str(self.port_number) + '/' + self.target_url, window_title=self.window_title))

        # Dance a little jig to do synchronous asynchronous initialisation...
        cef.PostTask(cef.TID_UI, create_browser)

        self.browser = postqueue.get()
        self.window = JSAcessObject(browser=self.browser, queue_ref=self.queue)

    def set_value(self, value):
        object.__getattribute__(self, 'queue').put(value)

    def Slot(*args, **kwargs):
        def wrapper(fun):
            def wrapped(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapped
        return wrapper

    def bind_javascript(self):
        self.bindings.SetFunction('set_value', self.set_value)

        sub_class_methods = [method_name for method_name in dir(self.__class__) if (not method_name.startswith('_'))
                            and (method_name not in dir(PysitronApp))
                            and callable(getattr(self.__class__, method_name))
                            and getattr(getattr(self.__class__, method_name), 'bind_to_window', True)]
        for method in sub_class_methods:
            # Injecting the self object back into bound functions, so it's easier for the python side of things
            # to mess around with things.
            # todo review if it´s a sane thing to make all callbacks threaded
            loaded_method = lambda *args, raw_method=getattr(self.__class__, method): daemon_threaded(raw_method)(self, *args)
            self.bindings.SetFunction(method, loaded_method)
            print(method, getattr(self.__class__, method))
        self.browser.SetJavascriptBindings(self.bindings)
        self.javascript_bound = True

    def setup_server(self, on_load_function = None):

        def no_app(environ, start_response):
            """Dummy app since all files are in static directory"""
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [self.default_text.encode('utf-8')]

        def starter():
            run_simple(r'localhost', self.port_number, no_app, use_reloader=False, use_debugger=False,
                       static_files={'/': os.path.dirname(__file__)})

        th = threading.Thread(target=starter, daemon=True)
        th.start()

        self.browser.SetClientHandler(LoadHandler(on_load_function, window_title=self.window_title, window_dimensions=self.window_dimensions))

    def run(self, onload = None):
        if not self.javascript_bound:
            self.bind_javascript()

        self.setup_server(on_load_function=onload)
        q = queue.Queue()

        q.put('somework')
        q.join()  # Todo: there must be a better way


class JSAcessObject:
    """Ad-hoc object used to make dom assignments act as if they were more naturally supported"""
    # todo: this could likely be build much much better. But for rough solution it works quite well.
    # Note throughout this code. object.__setattr__ and object.__getattribute__ are used to access object attributes,
    # because the JSAcessObject methods themselves are overwritten.
    def __init__(self, build='window', browser=None, queue_ref=None):
        object.__setattr__(self, 'build', build)
        object.__setattr__(self, 'browser', browser)
        object.__setattr__(self, 'queue_ref', queue_ref)

    def set_browser(self, browser):
        print('browser set')
        object.__setattr__(self, 'browser', browser)

    def __getattr__(self, item):
        if item in ('value', 'nodeValue', 'textContent', 'innerHTML'):
            # In this case, a javascript call is made to set the value in python in a queue and this part then waits on that thread to be filled.
            self.browser.ExecuteJavascript('set_value(' + self.build + '.' + item + ')')
            return object.__getattribute__(self, 'queue_ref').get()

        elif item not in ('set_browser', 'build'):
            return JSAcessObject(build=self.build + '.' + item,
                                 browser=object.__getattribute__(self, 'browser'),
                                 queue_ref=object.__getattribute__(self, 'queue_ref'))
        else:
            return object.__getattribute__(self, item)

    def __call__(self, *args, **kwargs):
        return JSAcessObject(self.build + '(' + ','.join(argument_python_to_javascript(x) for x in args) + ')',
                             browser=object.__getattribute__(self, 'browser'),
                             queue_ref=object.__getattribute__(self, 'queue_ref'))

    def __setattr__(self, key, value):
        if value is not None:
            browser = object.__getattribute__(self, 'browser')
            set_string = ''.join([self.build + '.' + key, '=', argument_python_to_javascript(value), ';'])
            if browser is not None:
                browser.ExecuteJavascript(set_string)
            return None

# window = JSAcessObject()

# todo might be obsolete
class document:
    """ Class for referencing the dom"""
    def getElementByID(id):
        return f'document.getElementByID({id})'

    def getElementsByName(name):
        return f'document.getElementsByName({name})'


def check_versions():
    print("[hello_world.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[hello_world.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"

__version__ = '0.0.1-dev'
