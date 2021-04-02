'''
Description: AudioFiles Segmentation
Version: 0.1
Author: Nettor
Date: 2021-04-01 08:42:49
LastEditors: Nettor
LastEditTime: 2021-04-02 13:31:20
'''

import argparse
import audioread
import os
from pathlib import Path
from pydub import AudioSegment

def slice_one_wav(input_wav_path, start_time, end_time, output_wav_path):
    """
    音频切片，获取部分音频，单位秒
    :param main_wav_path: 原音频文件路径
    :param start_time: 截取的开始时间
    :param end_time: 截取的结束时间
    :param part_wav_path: 截取后的音频路径
    :return:
    """
    
    start_time = start_time * 1000
    end_time = end_time * 1000

    sound = AudioSegment.from_wav(input_wav_path)
    word = sound[start_time:end_time]

    word.export(output_wav_path, format="wav")

def segment_wav(input_wav_path,output_wav_path,cut_ends,window_size):
    # 分类path, filename和ext
    (filename, ext) = os.path.splitext(input_wav_path)
    # 检查是不是wav文件
    if ext != '.wav':
        print(os.path.basename(filename)+ext+' is not a wav file.')
    else:
        # 设置start time和end time
        wav_len = get_wav_len(input_wav_path)
        start_time = cut_ends
        end_time = wav_len - cut_ends
        if end_time <=0:
            print('The duration of wav is '+str(wav_len)+'less than cut ends('+str(cut_ends)+').')
            return
        if window_size > (end_time - start_time):
            print('The windows size('+str(window_size)+') is longer than wav size('+str(end_time - start_time)+').')
            return
        # 切割
        for i in range(int(start_time),int(end_time),window_size):      
            output_filename = os.path.basename(filename)+'_s'+str(i)+ext
            slice_one_wav(input_wav_path, i, i+window_size,os.path.join(output_wav_path,output_filename))
            print('OUTPUT: '+ os.path.join(output_wav_path,output_filename))
        print('DONE')

def segment_wav_in_dir(input_path,output_path,cut_ends,window_size):
    # 把所有文件和文件夹入栈
    input_path, dirlist, filenames = next(os.walk(input_path))
    for filename in filenames:
        input_wav_path = os.path.join(os.path.abspath(input_path),filename)
        output_wav_path = os.path.join(os.path.abspath(output_path),'output')
        # 确保输出文件夹存在
        if not os.path.exists(output_wav_path):
            os.makedirs(output_wav_path)
        segment_wav(input_wav_path,output_wav_path,cut_ends,window_size)
    for dirname in dirlist:
        sub_input_path = os.path.join(input_path,dirname)
        dirname = dirname+'_output'
        sub_output_path = os.path.join(os.path.abspath(output_path),dirname)
        if not os.path.exists(sub_output_path):
            os.makedirs(sub_output_path)
        segment_wav_in_dir(sub_input_path,sub_output_path,cut_ends,window_size)

def get_wav_len(input_wav_path):
    with audioread.audio_open(input_wav_path) as f:
        return f.duration

def main():
    parser = argparse.ArgumentParser(description='Batch AudioFiles Segmentation')
    parser.add_argument('audiofile', type=str, metavar='[Path]',
                    help='specify an audio file path or dir path')
    parser.add_argument('-w','--window-size', type=int, default=50, metavar='[SIZE]',
                    help='input segment window size(second) (default: 1)')
    parser.add_argument('-c','--cut-ends', type=int, default=0, metavar='[TIME]',
                    help='break off both ends(second) (default: 1)')
    parser.add_argument('-o','--output', type=str, default='./output/', metavar='[Path]',
                    help='specify an output path (default: ./output/)')
    args = parser.parse_args()

    input_path = args.audiofile
    output_path = args.output
    window_size = args.window_size

    input_dir_path, input_wav_filename = os.path.split(os.path.abspath(input_path))

    # 单文件分割
    if os.path.isfile(input_path):
        if output_path == './output/':
            output_path = os.path.join(input_dir_path,'output')
        # 确保输出文件夹存在
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        segment_wav(input_path,output_path,args.cut_ends,window_size)
    # 文件夹分割
    else:
        segment_wav_in_dir(input_path,output_path,args.cut_ends,window_size)
        


if __name__ == '__main__':
    main()
    