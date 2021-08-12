#!/usr/bin python3
# -*- encoding: utf-8 -*-
'''
@File    :   video_cut.py   
@Contact :   
@License :   

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/5/6 1:30   lgh        1.0         None
'''

from ffmpy import FFmpeg
import ffmpeg
import easygui
from tkinter import filedialog


def cut_v(input_file, output_file, start_time, end_time):
    ff = FFmpeg(
        inputs={input_file: None},
        outputs={output_file: '-ss '+start_time+' -to '+end_time+' -c copy -y'}
    )
    print(ff.cmd)
    ff.run()
    print('剪辑完成')


def merge_video(input_file1, input_file2, output_file):
    pass
    ff = FFmpeg(
        inputs={input_file1, input_file2}
    )


def get_out_path():
    print("请输入编辑后文件保存的名称，包含后缀")
    output_path = filedialog.asksaveasfilename()

    return output_path


def get_in_path():
    # input_path = easygui.fileopenbox()
    # output_path = easygui.filesavebox()
    print('请选择需要进行编辑的视频文件')
    input_path = filedialog.askopenfilename()
    # print('请输入编辑后文件保存的名称，包含后缀')
    # output_path = filedialog.asksaveasfilename()
    # print(input_path)
    # print(output_path)

    return input_path   # , output_path


def get_time():
    print('请输入剪切的起始时间，格式: 00:00:00')
    start_time = input()
    print('请输入剪切的中止时间，格式: 00:00:00')
    end_time = input()

    return start_time, end_time


def get_ff_video(video_list):
    ff_list = []
    for video_addr in video_list:
        ff = (
            ffmpeg
            .input(video_addr)
        )
        ff_list.append(ff)
    return ff_list


if __name__ == "__main__":
    print("请选择需要的操作，输入操作前面的数字：")
    print("1.剪切")
    print('2.合并')
    action = input()
    if action != '1'or action != '2':
        print("请重新输入指定的选项")
    if action == '1':
        in_path = get_in_path()
        out_path = get_out_path()
        start_time, end_time = get_time()
        cut_v(in_path, out_path, start_time, end_time)
    elif action == '2':
        addr_list = []
        print("请选择需要合并的视频文件")
        x = '1'
        while x == '1':
            in_path = get_in_path()
            addr_list.append(in_path)
            print("请选择需要的操作，输入操作前面的数字：")
            print("1.继续添加")
            print("0.完成")
            x = input()
        print(addr_list)
        fv_list = get_ff_video(addr_list)
        print(fv_list)
        fv_str = ','.join(fv_list)
        print(fv_str)
        (
            ffmpeg
            .concat(fv_str)
            .output('D:\\beinvod\\142.155\\0824-0825\\output.ts')
            .run()
        )






    else:
        print('你所输入的操作不存在')