from tkinter import filedialog
import json
import os
import const


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

        setting = None

        # ファイルの存在チェック
        if not (os.path.exists(path)):
            return const.InitialSettimg

        # 設定ファイルの読み取り
        with open(path, encoding="utf-8") as file:
            setting = json.load(file)

        # デフォルトとキーが一致しているか確認
        if self.check_common_keys(setting, const.InitialSettimg):
            return setting
        else:
            return const.InitialSettimg

    # settingJSONの書き込み
    def writeJSON(self, path, jsondata):

        # デフォルトとキーが一致しているか確認
        if not self.check_common_keys(jsondata, const.InitialSettimg):
            return False

        # ファイルの存在チェック
        if not (os.path.exists(path)):
            return False

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

        return True

    # 2つの辞書のキーがすべて一致するか確認する
    def check_common_keys(self, dict1, dict2):
        return set(dict1.keys()) == set(dict2.keys())
