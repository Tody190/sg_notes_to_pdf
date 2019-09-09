# -*- coding: utf-8 -*-
__author__ = "yangtao"
__version__ = "1.1"


import os
import sys
import shutil
import platform

import dezerlin_welcome
import sg_data
import data_converter
import ui




# dezerlin welcome
dezerlin_welcome.show(__author__, __version__)

# response
def run(playlist, output_path):
    print("--- START ---")
    # 转换名称中不可用字符
    file_name = data_converter.name_filter(playlist)
    # html 附件保存路径
    attachments = os.path.join(output_path, file_name)
    # playlist 获取 shotgun notes 数据
    print("Download Data ...")

    pn = sg_data.Playlist_Notes(playlist)
    notes_data = pn.get(attachments_download_path=attachments)
    if notes_data:
        # 写入 pdf 文件
        html_file = data_converter.notes_to_html(notes_data, output_path, file_name)
        print("Convert Data...")
        if html_file:
            pdf_file = data_converter.htm_to_pdf(html_file,
                                                 os.path.join(output_path, "%s.pdf" % file_name))
            print("Conversion Completed: %s"%pdf_file)

            # 删除临时文件
            if os.path.exists(attachments):
                shutil.rmtree(attachments)
            os.remove(html_file)

    print("--- DONE ---")

# UI
main_ui = ui.Main_Window()
main_ui.window_name = 'DeZerlin SG Notes to pdf %s by %s'%(__version__, __author__)
root_file = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
if "Darwin" in platform.system():
    icon_file = root_file + "/sg_notes_to_pdf.icns"
else:
    icon_file = root_file + "/sg_notes_to_pdf.ico"
main_ui.window_icon = icon_file
main_ui.run_fun = run