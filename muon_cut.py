# prompt: Get audio from a specified time using pydub
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
from tkinter import filedialog

#音声ファイルのパスを取得
def get_wav_path():
    typ = [('wavファイル','*.wav')] 
    dir = './'
    tit = '音声ファイルを複数選択してください'
    path = filedialog.askopenfilenames(filetypes = typ, initialdir = dir ,title = tit) 
    return path

#有声部分の時間を取得[開始(ms):終了(ms)]
def get_yusei_list(path):
    #最も長い音声ファイルの時間を取得[s]
    max_time = 0.0

    print('音声ファイルの読み取りを開始:')
    for pa in path:
        print(pa)
        sound  = AudioSegment.from_wav(pa)
        time = sound.duration_seconds
        if(time > max_time):
            max_time = time
    
    #無音ファイルを作成
    sum_sound = AudioSegment.silent(duration=(max_time + 1)*1000)

    #音声をすべて加算する
    for pa in path:
        sound  = AudioSegment.from_wav(pa)
        sum_sound = sum_sound.overlay(sound, position=0)

    print('有声区間の検出を開始:')
    muon_lists = detect_nonsilent(sum_sound, min_silence_len=min_silence_duration, silence_thresh=silence_threshold,seek_step=2)
    print(muon_lists)

    return muon_lists


#有声区間のみ結合し出力
def get_nonslience(pa,wk_muon_lists):
    no_silence_audio = AudioSegment.empty()
    wk_sound  = AudioSegment.from_wav(pa)
    
    for muon_list in wk_muon_lists:
        no_silence_audio += wk_sound[muon_list[0]:muon_list[1]+min_silence_duration]

    out_file_path = add_outpath_filename(pa)
    print(out_file_path)
    no_silence_audio.export(out_file_path, format='wav')
    
    # Check if the file exists
    if os.path.exists(out_file_path):
        print(f"Successfully extracted audio.")
    else:
        print("An error occurred while extracting the audio.")

#パスのファイル名に文字を追加
def add_outpath_filename(pa):
    dir_name = os.path.dirname(pa)
    file_name = os.path.splitext(os.path.basename(pa))
    new_file_path =dir_name + '/' +file_name[0] + '_cut' + file_name[1]
    return new_file_path



#無音の閾値[dB?]
silence_threshold= -60

#指定秒数以上の無音のみ検出[ms]
min_silence_duration = 500

audio_path = get_wav_path()
muon_lists = get_yusei_list(audio_path)

print('音声ファイルの出力を開始:')
for pa in audio_path:
    get_nonslience(pa,muon_lists);

#exe作成時は有効化する
print('処理完了 何かキーを入力してください...')
input()
