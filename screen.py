# from tkinter import *
import tkinter as tk
import tkinter.font as font
import os
import screen_logic
import muon_cut
import const


class Screen:

    # 画像の初期化
    def __init__(self):

        self.screenLogic = screen_logic.ScreenLogic()

        self.root = tk.Tk()
        self.screenInit()
        self.root.mainloop()

    # 画面の初期化
    def screenInit(self):

        midasiFont = font.Font(self.root, family="Yu Gothic UI", size=10, weight="bold")
        setumeiFont = font.Font(self.root, family="Yu Gothic UI", size=8)

        # rootの作成
        self.root.geometry("600x600+200+200")

        # frameの作成
        self.settei_frame = tk.Frame(self.root, bd=0)

        # labelの作成
        self.midasi_label1 = tk.Label(
            self.settei_frame, text="キャラクター", font=midasiFont
        )

        self.saizenmen_var = tk.BooleanVar()
        saizenmen_ch = tk.Checkbutton(
            self.settei_frame, text="常に手前に表示する", variable=self.saizenmen_var
        )

        self.setumei_label1 = tk.Label(
            self.settei_frame, text="画面の最前面表示", font=setumeiFont
        )

        # Listboxの作成
        self.item_list = ["Easy", "Normal", "Hard"]
        self.file_name_list_var = tk.StringVar(self.settei_frame, value=self.item_list)
        self.file_name_listbox = tk.Listbox(
            self.settei_frame, listvariable=self.file_name_list_var
        )

        # Entryの作成
        self.outFolderEntry = tk.Entry(self.settei_frame)

        # buttonの作成
        self.file_button = tk.Button(
            self.settei_frame, text="ファイル選択", command=self.doChoice
        )
        self.out_folder_button = tk.Button(
            self.settei_frame, text="フォルダ選択", command=self.doOutFolder
        )
        self.delete_button = tk.Button(
            self.settei_frame, text="削除", command=self.doDelete
        )
        self.shori_button = tk.Button(
            self.settei_frame, text="処理開始", command=self.doShori
        )
        self.cancel_button = tk.Button(
            self.settei_frame, text="キャンセル", command=self.doCancel
        )
        self.initialize_button = tk.Button(
            self.settei_frame, text="初期設定に戻す", command=self.doInitialize
        )

        # オブジェクトの配置
        self.settei_frame.place(x=0, y=0)
        self.midasi_label1.pack()
        self.file_name_listbox.pack()
        saizenmen_ch.pack()
        self.setumei_label1.pack()
        self.outFolderEntry.pack()
        self.file_button.pack()
        self.out_folder_button.pack()
        self.delete_button.pack()
        self.shori_button.pack()
        self.cancel_button.pack()
        self.initialize_button.pack()

        # フレームのサイズを不変にする
        self.root.propagate(False)

        # 最前面に表示
        self.root.attributes("-topmost", True)

        """
         イベントバインド
        """
        self.file_name_listbox.bind("<<ListboxSelect>>", self.get_selected)

        # 画面項目の設定
        self.screenLoad()

        # 削除ボタンの活性制御
        self.get_del_button_control()

    # 入力ファイル選択ボタン押下時処理
    def doChoice(self):

        # ファイル選択ダイアログの起動
        path_list = self.screenLogic.get_wav_path()
        self.add_file_name_list(path_list)

    # 出力先フォルダ選択ボタン押下時処理
    def doOutFolder(self):

        # フォルダ選択ダイアログの起動
        path = self.screenLogic.get_folder_path()
        if len(path) == 0:
            return

        # 値の設定
        self.set_out_folder_entry(path)

    # 削除ボタン押下時処理
    def doDelete(self):

        # リストボックスの取得
        choice = self.file_name_listbox.curselection()

        # リストの選択がされていない場合
        if not choice:
            self.delete_button["state"] = tk.DISABLED
            return

        # リストの要素が空の場合
        if not self.item_list:
            self.delete_button["state"] = tk.DISABLED
            return

        # 選択箇所の削除
        del self.item_list[choice[0]]
        self.file_name_list_var.set(self.item_list)

        # ボタンの活性制御
        self.get_del_button_control()

    # 処理開始ボタン押下時処理
    def doShori(self):

        self.screenSave()
        self.cut_process()

    # キャンセルボタン押下時処理
    def doCancel(self):
        self.root.destroy()

    # 初期化ボタン押下時処理
    def doInitialize(self):
        setting = const.INITIAL_SETTIMG
        self.screenSet(setting)

    # リストボックス選択時処理
    def get_selected(self, event):
        self.get_del_button_control()

    # リストボックスの活性制御
    def get_del_button_control(self):

        # リストボックスの取得
        choice = self.file_name_listbox.curselection()

        # リストの選択がされていない場合
        if not choice:
            self.delete_button["state"] = tk.DISABLED
            return

        # リストの要素が空の場合
        if not self.item_list:
            self.delete_button["state"] = tk.DISABLED
            return

        self.delete_button["state"] = tk.NORMAL

    # 画面項目を保存
    def screenSave(self):

        setting = self.screenGet()
        self.screenLogic.writeJSON(const.SETTING_FILE, setting)

    # 画面項目を読み込み
    def screenLoad(self):

        setting = self.screenLogic.readJSON(const.SETTING_FILE)
        self.screenSet(setting)

    def cut_process(self):
        cutLogic = muon_cut.CutLogic()

        muon_lists = cutLogic.get_yusei_list(self.item_list)
        out_folder_path = self.get_out_folder_entry()

        print("音声ファイルの出力を開始:")
        for path in self.item_list:
            if not (cutLogic.get_nonslience(path, out_folder_path, muon_lists)):
                print("err:")
                return

        print("処理完了 何かキーを入力してください...")

    """
    getter&setter
    """

    # 画面項目を取得
    def screenGet(self):

        setting = const.INITIAL_SETTIMG

        setting["input_file_path"] = self.item_list
        setting["out_folder_path"] = self.get_out_folder_entry()

        return setting

    # 画面項目を取得
    def screenSet(self, setting):

        self.set_file_name_list(setting["input_file_path"])
        self.set_out_folder_entry(setting["out_folder_path"])

    # リストボックスを設定
    def set_file_name_list(self, path_list):
        self.item_list.clear()

        if path_list:
            for path in path_list:
                self.item_list.append(path)

        self.file_name_list_var.set(self.item_list)

    # リストボックスに追加
    def add_file_name_list(self, list):
        for str in list:
            self.item_list.append(str)

        self.file_name_list_var.set(self.item_list)

    def get_out_folder_entry(self):
        return self.outFolderEntry.get()

    def set_out_folder_entry(self, str):
        # 値の設定
        if len(self.outFolderEntry.get()) != 0:
            self.outFolderEntry.delete(0, tk.END)
        self.outFolderEntry.insert(0, str)


# メイン関数
if __name__ == "__main__":
    m = Screen()
