import pygame as pg

# pg.init()
from pathlib import Path
import src.data.loaders
from src.data.Loger import log, status, log_step
import src.data.screen as screen
import json


class App:
    def __init__(self):
        status("App init started")

        self._set_start_parameters()

        self.main_screen = screen.MainScreen(self)

        self._create_functions_dict()


        status("App init complete")
        log_step(2)

    def run(self):
        status("App start")
        while self.WORK:
            self.tick += 1
            self.clock.tick(self.TPS)
            self.main_screen.draw()

    def exit(self):
        self.WORK = False
        log("App exit")

    def _set_start_parameters(self):
        self.clock = pg.time.Clock()
        self.TPS = 20
        self.tick = 0
        self.path = Path.cwd()
        self.WORK = True
        self.pets = {}
        self.select_pet = None

        with self.path.joinpath("data/configs/core.json").open("r") as f:
            self.core = json.load(f)
        self.version = list(map(int, self.core["version"].split(".")))

        status(f"App version: {self.version}")
        status("Set App parameters complete")

    def _create_functions_dict(self):
        sist = {
            "exit": [self.exit, None]
        }
        self.function_rans = {"sistem": sist, "mods": {}}

        status("Function giver generate complete")

    def add_functions(self, dict_functions: dict):
        """
        {"key": {"name": [lambda x: print(1), None]}}
        :param dict_functions:
        :return:
        """
        for key, functions in dict_functions.items():
            if key != "sistem":
                if key not in self.function_rans:
                    self.function_rans[key] = {}
                for name, function in functions.items():
                    self.function_rans[key][name] = function

    def give_function(self, data, passw=None):
        m: dict | list = self.function_rans
        for i in data:
            if i in m:
                m = m[i]
            else:
                return {"result": False, "error": [0, f"{i} from {data} undefined"]}
        if type(m) == dict:
            return {"result": False, "error": [1, f"{data} is unfull address"]}
        elif m[1] == passw:
            return {"result": True, "function": m[0]}
        else:
            return {"result": False, "error": [3, f"uncorrect passw"]}



