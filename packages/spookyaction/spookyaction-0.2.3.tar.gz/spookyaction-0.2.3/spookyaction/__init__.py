import os, sys, re
from item_object import Item
from spooky_logs import log
from error_handling import Error
from ui import GUI_INTERFACE

class Ghost(object, GUI_INTERFACE):
    def __init__(self, ocr_key):
        self.METHODS = {}
        self.currentresults = []
        self.ocr_key = ocr_key

        directory = './'+sys.argv[0]+'/imgs' # the ./ may be a problem?
        names = os.listdir(directory)
        self.Items = {
            re.sub('(\.PNG)', '', name): Item(directory+"/"+name, self.ocr_key)
            for name in names
        }

    def __getitem__(self, key):
        return self.Items[key]

    def new_method(self, fn):
        self.METHODS[fn.__name__] = fn
        return fn

    def start(self, obj, cmd):
        raise NotImplementedError("start(obj, cmd) must be implemented.")

    def failed(self, e, obj, cmd):
        raise NotImplementedError("failed(e, obj, cmd) must be implemented")

    def completed(self, obj, cmd):
        raise NotImplementedError("completed(obj, cmd) must be implemented")

    @log
    def click_all(self, *args):
        for i in args:
            self[i].click()

    @log
    def wait_for_all(self, *args, **kwargs):
        theres = []
        while theres != [True]*len(args):
            theres = []
            for i in args:
                theres.append(self[i].found)
            self.keywrite(*kwargs["typewrite_between"])

    def run(self, obj=None, cmd=None, cmd_args=None, cmd_kwargs=None):
        self.start(obj, cmd)
        try:
            currentresults = METHODS[cmd](*cmd_args, **cmd_kwargs)
        except Error as e:
            self.failed(e, obj, cmd)
        else:
            self.completed(obj, cmd)

    # def run_all(filename="commands.csv", model=[]):
    #     self.
