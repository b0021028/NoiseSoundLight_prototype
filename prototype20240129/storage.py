from pathlib import Path
import json


_IR_DATA_PATH = Path(__file__).parent / "ir_signals"
_FUNC_DATA_PATH = Path(__file__).parent / "functions"


class Storage:
    JSON_TYPE = dict | list

    def _setup_dir(self, _path: Path):
        if not _path.exists():
            _path.mkdir()
        elif _path.is_file():
            raise ImportError(f"not found directory {_path}")

    def _get_file_paths(self, _path: Path):
        yield from (
            path for path in _path.iterdir() if path.is_file() and path.match("*.json")
        )

    def _get_json_obj(self, _path: Path):
        with _path.open("r", errors="ignore") as f:
            json_obj = json.load(f)
        if isinstance(json_obj, self.JSON_TYPE):
            return json_obj

    def _get_files_json_obj(self, _path: Path):
        for path in self._get_file_paths(_path):
            json_obj = self._get_json_obj(path)
            if json_obj is None:
                continue
            yield path, json_obj

    def __init__(self, _path: Path):
        self._setup_dir(_path)
        self.d = dict()
        # .json で jsonの辞書で  ~~.jsonだった時 keyが ~~_keyname であり valueが list[int]の物のみ

    def get(self, key):
        return self.d.get(key)


class IRStorage(Storage):
    JSON_TYPE = dict

    def __init__(self):
        super().__init__(_IR_DATA_PATH)
        # .json で jsonの辞書で  ~~.jsonだった時 keyが ~~_keyname であり valueが list[int]の物のみ
        for path, json_obj in self._get_files_json_obj(_IR_DATA_PATH):
            base_name = path.stem + "_"
            for key in json_obj.keys():
                if any(
                    (x != y)
                    for x, y in zip(
                        str(key).partition(base_name)[:2],
                        ("", base_name),
                    )
                ):
                    continue

                value = json_obj.get(key)
                if isinstance(value, list) and all(isinstance(i, int) for i in value):
                    self.d.setdefault(str(key), value)


class FunctionStorage(Storage):
    JSON_TYPE = list

    def __init__(self):
        super().__init__(_FUNC_DATA_PATH)
        # .json で jsonの辞書で  ~~.jsonだった時 keyが ~~_keyname であり valueが list[int]の物のみ
        self.functions_cache = dict()
        for path, json_obj in self._get_files_json_obj(_FUNC_DATA_PATH):
            for onefunc in json_obj:
                (catch, func, name) = (
                    onefunc["catch"],
                    onefunc["func"],
                    onefunc["name"],
                )
                self.d.setdefault(name, dict(catch=catch, func=func))
                for d in catch:
                    knock = d.get("knock")
                    if knock is not None:
                        self.functions_cache[knock] = name

    def _get_func_name(self, ct):
        return self.functions_cache.get(ct)

    def get(self, ct) -> list:
        name = self._get_func_name(ct)
        if name is None:
            return []
        d = self.d.get(name)
        if d is None:
            return []
        func = d.get("func")
        if not isinstance(func, list):
            return []
        return func
