# -*- coding: utf-8 -*-
__author__ = "yangtao"


import tkinter as tk
import config_tool




class Main_Window:
    def __init__(self):
        self.window_icon = ""
        self.window_name = ""
        self.geometry = "400x100"

    def run_fun(self):
        pass

    def start(self):
        playlist_name = self.playlist_entry.get()
        output_path = self.output_entry.get()
        # 写入配置文件
        config_tool.write("UI", {"path": output_path})
        if playlist_name and output_path:
            self.run_fun(playlist_name, output_path)

    def show(self):
        main_window = tk.Tk()
        main_window.title(self.window_name)
        main_window.iconbitmap(self.window_icon)
        main_window.geometry(self.geometry)
        # palylist frame
        playlist_frame = tk.Frame(main_window)
        playlist_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        # palylist 便签
        playlist_label = tk.Label(playlist_frame, text="Playlist: ")
        playlist_label.pack(side=tk.LEFT)
        # palylist 输入框
        self.playlist_entry = tk.Entry(playlist_frame)
        self.playlist_entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        # output frame
        output_frame = tk.Frame(main_window)
        output_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        # output 便签
        output_label = tk.Label(output_frame, text="Output Path: ")
        output_label.pack(side=tk.LEFT)
        # output 输入框
        output_var = tk.StringVar()
        output_var.set(config_tool.read("UI", "path"))
        self.output_entry = tk.Entry(output_frame, textvariable=output_var)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        # 开始按钮
        start_button = tk.Button(main_window, text='开始', command=self.start)
        start_button.pack(fill=tk.X, anchor=tk.S, expand=tk.YES)

        main_window.mainloop()