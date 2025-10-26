import pygame as pg

# import data.base as base
pg.init()
from pathlib import Path
import src.data.loaders
from src.data.Loger import log, status, log_step
import src.data.screen as screen
import json


class Game:
    def __init__(self):
        status("Game init started")

        self._set_start_parameters()


        self.main_screen = screen.MainScreen(self)

        self._create_functions_dict()

        self.load_pet_feed()

        status("Game init complete")
        log_step(2)

    def run(self):
        status("Game start")
        while self.WORK:
            self.tick += 1
            self.clock.tick(self.TPS)
            self.main_screen.draw()

    def exit(self):
        self.WORK = False
        log("Game exit")

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

        status(f"Game version: {self.version}")
        status("Set Game parameters complete")

    def _create_functions_dict(self):
        sist = {
            "exit": [self.exit, None],
            "open_pet_info": [self.open_pet_info, None],
            "open_pet_feed": [self.open_pet_feed, None],
            "open_settings": [self.open_settings, None]
        }
        self.function_rans = {"sistem": sist, "mods": {}}

        status("Function giver generate complete")

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

    def load_pet_feed(self):
        with self.path.joinpath("db.json").open("r", encoding="utf-8") as file:
            self.pets = json.load(file)["pets"]

        mb = self.main_screen.window_manager.get_window("pet_feed")
        config = []
        x, y, dx, dy, sx, sy = mb.cord_new_but
        for i, ipet in enumerate(self.pets):
            pet = self.pets[ipet]
            config.append([
                "button_png",
                f"{pet['name']}, {pet['age']}",
                "run_function:sistem/open_pet_info",
                [
                    x + (dx + sx) * (i % 2),
                    y + (dy + sy) * (i // 2),
                    sx, sy
                ],
                "pet_feed",
                {
                    "pet_name": ipet
                },
                [
                    pet['image'][0],
                    "img_female" if pet['parameters']['gender'] == "Девочка" else "img_male"
                ]
            ])
            # log(config[-1])
        mb._menu_load({"buttons": config})

    def gen_params(self, params):
        st_param = ["Пол:", "Порода:", "Рост:", "Вес:", "Окрас:"]
        for key, value in params.items():
            st_param.append(value)

        return st_param

    def open_pet_info(self, data):
        self.select_pet = self.pets[data.get_parameters("pet_name")]
        pet = self.select_pet
        wm = self.main_screen.window_manager
        bm = wm.get_window("head_info").button_manager
        bm._buttons[0].set_png(pet["image"][1])
        bm._buttons[0].set_text(f"{pet['name']}, {pet['age']}")

        bm = wm.get_window("detailed_information").button_manager
        bm._buttons[0].set_text(pet["descr"])
        bm._buttons[1].set_text(self.gen_params(pet["parameters"]))
        bm._buttons[2].set_text(pet["tags"])

        wm.close_window("find_line")
        wm.open_window("head_info")
        wm.set_main_window("detailed_information")

    def open_settings(self, data):
        wm = self.main_screen.window_manager
        wm.close_window("find_line")
        wm.set_main_window("settings")

    def open_pet_feed(self, data):
        wm = self.main_screen.window_manager
        wm.close_window()
        wm.open_window("find_line")
        wm.open_window("speed_move")
        wm.set_main_window("pet_feed")


if __name__ == "__main__":
    game = Game()
    game.run()
