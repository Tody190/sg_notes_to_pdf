# coding=utf-8
__author__ = "yangtao"
__version__ = "1.0"


import os

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
    notes_data = sg_data.get_notes_data(playlist,
                                        attachments_download_path=attachments)
    if notes_data:
        # 写入 pdf 文件
        html_file = data_converter.notes_to_html(notes_data, output_path, file_name)
        print("Convert Data...")
        if html_file:
            pdf_file = data_converter.htm_to_pdf(html_file,
                                                 os.path.join(output_path, "%s.pdf" % file_name))
            print("Conversion Completed: %s"%pdf_file)
            # 删除 其它文件
            data_converter.yt_remove(attachments)
            data_converter.yt_remove(html_file)
    print("--- DONE ---")

# UI
main_ui = ui.Main_Window()
main_ui.window_name = 'DeZerlin SG Notes to pdf %s by %s'%(__version__, __author__)
main_ui.window_icon = os.path.dirname(__file__).replace('\\', '/') + '/sg_notes_to_pdf.ico'
main_ui.run_fun = run
main_ui.show()




if __name__ == "__main__":
    run("choki-cfx.sim-QC-20190827", r"D:\temp\pdf\p d f")
