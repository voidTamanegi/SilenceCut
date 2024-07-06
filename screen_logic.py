from tkinter import filedialog
import json


class ScreenLogic:

    # 音声ファイルのパスを取得
    def get_wav_path(self):
        typ = [("wavファイル", "*.wav")]
        dir = "./"
        tit = "音声ファイルを選択してください（複数選択可）"
        path_list = filedialog.askopenfilenames(
            filetypes=typ, initialdir=dir, title=tit
        )
        return path_list

    # フォルダのパスを取得
    def get_folder_path(self):
        dir = "./"
        tit = "出力先フォルダを選択してください"
        path = filedialog.askdirectory(initialdir=dir, title=tit)
        return path

    # settingJSONの読み取り
    def readJSON(self, path):
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    # settingJSONの書き込み
    def writeJSON(self, path, jsondata):
        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                jsondata,
                file,
                indent=2,
                ensure_ascii=False,
            )
