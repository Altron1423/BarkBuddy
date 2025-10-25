from pathlib import Path

class Translator:
    def __init__(self):
        self.dictionary = {}

    def add_dict(self, name: str, dictionary: dict):
        self.dictionary[name] = dictionary
        print(self.dictionary)

    def load_from(self, path: Path, name_dict: str):
        dictionary = {}
        with path.open("r") as file:
            for line in file:
                line = line.strip().split("#")[0]
                if line:
                    if line.count("=") == 1:
                        key, value = [l.strip() for l in line.split("=")]
                        dictionary[key] = value
                    # print(line)
        self.add_dict(name_dict, dictionary)

    def load_from_file(self, path: Path, name_dict: str):
        dictionary = {}
        with path.open("r") as file:
            for line in file:
                line = line.strip().split("#")[0]
                if line:
                    if line.count("=") == 1:
                        key, value = [l.strip() for l in line.split("=")]
                        dictionary[key] = value
                    # print(line)
        self.add_dict(name_dict, dictionary)

    def translation(self, word:str, dict_name:str|None=None, return_in:bool=True) -> str | None:
        if dict_name == None:
            for name, dictionary in self.dictionary.items():
                for key_word, translation in dictionary.items():
                    if key_word == word:
                        return translation
        else:
            for key_word, translation in self.dictionary[dict_name].items():
                if key_word == word:
                    return translation
        if return_in:
            return word
        return None


if __name__ == "__main__":
    translator = Translator()

    translator.load_from(Path.cwd().joinpath("Translator.py"), "test")
    print(translator.translation("self.dictionary[name]"))