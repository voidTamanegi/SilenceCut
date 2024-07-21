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
        self.root.geometry("600x500+200+200")

        # frameの作成
        self.input_frame = tk.LabelFrame(self.root, text="入力ファイル")
        self.output_frame = tk.LabelFrame(self.root, text="出力フォルダ")
        self.settei_frame = tk.LabelFrame(self.root, text="詳細オプション")
        self.start_frame = tk.Frame(self.root, bd=1, relief=tk.RIDGE)
        self.log_frame = tk.Frame(self.root, bd=1, relief=tk.RIDGE)

        # # labelの作成
        self.log_label = tk.Label(self.log_frame, text="", font=setumeiFont)

        self.option_label00 = tk.Label(
            self.settei_frame, text="無音判定閾値 : ", font=setumeiFont
        )

        self.option_label01 = tk.Label(
            self.settei_frame, text="[-dB]", font=setumeiFont
        )

        self.option_label10 = tk.Label(
            self.settei_frame, text="無音判定時間 : ", font=setumeiFont
        )

        self.option_label11 = tk.Label(self.settei_frame, text="[ms]", font=setumeiFont)

        self.option_label20 = tk.Label(
            self.settei_frame, text="処理ステップ : ", font=setumeiFont
        )

        self.option_label21 = tk.Label(self.settei_frame, text="[ms]", font=setumeiFont)

        # self.saizenmen_var = tk.BooleanVar()
        # saizenmen_ch = tk.Checkbutton(
        #     self.settei_frame, text="常に手前に表示する", variable=self.saizenmen_var
        # )

        # Listboxの作成
        self.item_list = []
        self.file_name_list_var = tk.StringVar(self.settei_frame, value=self.item_list)
        self.file_name_listbox = tk.Listbox(
            self.input_frame, listvariable=self.file_name_list_var, height=5, width=80
        )

        # Entryの作成
        self.outFolderEntry = tk.Entry(self.output_frame, width=80)

        # spinbox
        self.threshold_spinbox = tk.Spinbox(
            self.settei_frame,
            from_=-80,
            to=0,
            increment=1,
            width=5,
        )

        self.duration_spinbox = tk.Spinbox(
            self.settei_frame,
            from_=100,
            to=1000,
            increment=10,
            width=5,
        )

        self.seek_spinbox = tk.Spinbox(
            self.settei_frame,
            from_=1,
            to=100,
            increment=1,
            width=5,
        )

        # buttonの作成
        self.file_button = tk.Button(
            self.input_frame, text="ファイル選択", command=self.doChoice, width=10
        )
        self.out_folder_button = tk.Button(
            self.output_frame, text="フォルダ選択", command=self.doOutFolder, width=10
        )
        self.delete_button = tk.Button(
            self.input_frame, text="削除", command=self.doDelete, width=10
        )
        self.shori_button = tk.Button(
            self.start_frame, text="処理開始", command=self.doShori, width=10
        )
        self.cancel_button = tk.Button(
            self.start_frame, text="キャンセル", command=self.doCancel, width=10
        )
        self.initialize_button = tk.Button(
            self.start_frame,
            text="初期設定に戻す",
            command=self.doInitialize,
            width=14,
        )

        # オブジェクトの配置
        self.input_frame.pack(pady=(30, 0))
        # self.input_label1.pack(anchor=tk.W)
        self.file_name_listbox.pack(padx=10, pady=(5, 0))
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.file_button.pack(side=tk.RIGHT, pady=10)

        self.output_frame.pack(pady=(20, 0))
        # self.output_label1.pack(anchor=tk.W)
        self.outFolderEntry.pack(padx=10, pady=(5, 0))
        self.out_folder_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.settei_frame.pack(pady=(20, 0))
        self.option_label00.grid(row=0, column=0, padx=(10, 0))
        self.option_label10.grid(row=1, column=0, padx=(10, 0))
        self.option_label20.grid(row=2, column=0, padx=(10, 0))
        self.threshold_spinbox.grid(row=0, column=1)
        self.duration_spinbox.grid(row=1, column=1)
        self.seek_spinbox.grid(row=2, column=1)
        self.option_label01.grid(row=0, column=2, padx=(0, 10))
        self.option_label11.grid(row=1, column=2, padx=(0, 10))
        self.option_label21.grid(row=2, column=2, padx=(0, 10))

        self.start_frame.pack()
        self.shori_button.pack(pady=(20, 0))
        self.cancel_button.pack()
        self.initialize_button.pack(pady=(20, 0))

        self.log_frame.pack()
        self.log_label.pack()

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
        setting = const.INITIAL_SETTIMG.copy()
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
        setting = self.screenGet()
        cutLogic = muon_cut.CutLogic(
            setting["threshold"], -setting["duration"], setting["seek"]
        )

        self.log_label["text"] = "処理開始"

        muon_lists = cutLogic.get_yusei_list(self.item_list)
        out_folder_path = self.get_out_folder_entry()

        self.log_label["text"] = "音声ファイルの出力を開始:"
        for path in self.item_list:
            if not (cutLogic.get_nonslience(path, out_folder_path, muon_lists)):
                print("err:")
                return

        self.log_label["text"] = "処理完了"

    """
    getter&setter
    """

    # 画面項目を取得
    def screenGet(self):

        setting = const.INITIAL_SETTIMG.copy()

        setting["input_file_path"] = self.item_list
        setting["out_folder_path"] = self.get_out_folder_entry()
        setting["threshold"] = self.get_threshold_spinbox()
        setting["duration"] = self.get_duration_spinbox()
        setting["seek"] = self.get_seek_spinbox()

        return setting

    # 画面項目を設定
    def screenSet(self, setting):

        self.set_file_name_list(setting["input_file_path"])
        self.set_out_folder_entry(setting["out_folder_path"])
        self.set_threshold_spinbox(setting["threshold"])
        self.set_duration_spinbox(setting["duration"])
        self.set_seek_spinbox(setting["seek"])

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

    def get_threshold_spinbox(self):

        val = self.threshold_spinbox.get()

        # 値が空 or 数値以外の場合、初期値に変更
        if val == "" or not (str.isdigit(val)):
            val = const.INITIAL_SETTIMG["threshold"]
            self.set_threshold_spinbox(val)

        return int(val)

    def set_threshold_spinbox(self, str):
        # 値の設定
        if len(self.threshold_spinbox.get()) != 0:
            self.threshold_spinbox.delete(0, tk.END)
        self.threshold_spinbox.insert(0, str)

    def get_duration_spinbox(self):

        val = self.duration_spinbox.get()

        # 値が空 or 数値以外の場合、初期値に変更
        if val == "" or not (str.isdigit(val)):
            val = const.INITIAL_SETTIMG["duration"]
            self.set_threshold_spinbox(val)

        return int(val)

    def set_duration_spinbox(self, str):
        # 値の設定
        if len(self.duration_spinbox.get()) != 0:
            self.duration_spinbox.delete(0, tk.END)
        self.duration_spinbox.insert(0, str)

    def get_seek_spinbox(self):
        val = self.seek_spinbox.get()

        # 値が空 or 数値以外の場合、初期値に変更
        if val == "" or not (str.isdigit(val)):
            val = const.INITIAL_SETTIMG["seek"]
            self.set_threshold_spinbox(val)

        return int(val)

    def set_seek_spinbox(self, str):
        # 値の設定
        if len(self.seek_spinbox.get()) != 0:
            self.seek_spinbox.delete(0, tk.END)
        self.seek_spinbox.insert(0, str)


# メイン関数
if __name__ == "__main__":
    m = Screen()
