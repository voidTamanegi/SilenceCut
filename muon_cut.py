# prompt: Get audio from a specified time using pydub
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


class CutLogic:

    # 有声部分の時間を取得[開始(ms):終了(ms)]
    def get_yusei_list(self, path):
        # 最も長い音声ファイルの時間を取得[s]
        max_time = 0.0

        print("音声ファイルの読み取りを開始:")
        for pa in path:
            print(pa)
            sound = AudioSegment.from_wav(pa)
            time = sound.duration_seconds
            if time > max_time:
                max_time = time

        # 無音ファイルを作成
        sum_sound = AudioSegment.silent(duration=(max_time + 1) * 1000)

        # 音声をすべて加算する
        for pa in path:
            sound = AudioSegment.from_wav(pa)
            sum_sound = sum_sound.overlay(sound, position=0)

        print("有声区間の検出を開始:")
        muon_lists = detect_nonsilent(
            sum_sound,
            min_silence_len=self.min_silence_duration,
            silence_thresh=self.silence_threshold,
            seek_step=2,
        )
        print(muon_lists)

        return muon_lists

    # 有声区間のみ結合し出力
    def get_nonslience(self, pa, out_folder_path, wk_muon_lists):
        no_silence_audio = AudioSegment.empty()
        wk_sound = AudioSegment.from_wav(pa)

        for muon_list in wk_muon_lists:
            no_silence_audio += wk_sound[
                muon_list[0] : muon_list[1] + self.min_silence_duration
            ]

        # ファイルの出力
        # out_file_path = self.add_outpath_filename(pa)
        out_file_path = os.path.join(out_folder_path, os.path.basename(pa))
        print(out_file_path)
        no_silence_audio.export(out_file_path, format="wav")

        # ファイルの存在チェック
        if os.path.exists(out_file_path):
            print(f"Successfully extracted audio.")
            return True
        else:
            print("An error occurred while extracting the audio.")
            return False

    # パスのファイル名に文字を追加
    def add_outpath_filename(self, pa):
        dir_name = os.path.dirname(pa)
        file_name = os.path.splitext(os.path.basename(pa))
        new_file_path = os.path.join(dir_name, file_name[0] + "_cut" + file_name[1])
        return new_file_path

    # 画像の初期化
    def __init__(self):
        # 無音の閾値[dB?]
        self.silence_threshold = -60

        # 指定秒数以上の無音のみ検出[ms]
        self.min_silence_duration = 500
