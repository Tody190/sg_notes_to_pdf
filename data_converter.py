# -*- coding: utf-8 -*-
__author__ = "yangtao"


import codecs
import os
import subprocess
import platform




class Html_Notes:
    def __html(self, body):
        html = "<!DOCTYPE html>\n"
        html += "<html lang=\"zh-cn\">\n"
        html += self.__head()
        html += body
        html += "</html>"
        return html

    def __head(self):
        head = "<head>\n"
        head += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n"
        head += self.__style()
        head += "</head>\n"
        return head

    def __style(self):
        style = "<style type=\"text/css\">\n"
        style += "h1 {color:red}\n"
        style += "h2 {color:gray}\n"
        style += "p {font-weight: 700}\n"
        style += "</style>\n"
        return style

    def __note(self, subject, content, attachments):
        # subject
        note = ""
        note += "<h2>\n"
        note += "%s\n"%subject
        note += "</h2>\n"
        # content
        note += "<p>\n"
        note += "%s\n"%content
        note += "</p>\n"
        # attachments
        for attachment in attachments:
            #body += "<a href=\"%s\" target=\"_blank\">\n" % attachment
            #body += "<img src=\"%s\" width=\"480\" height=\"270\"/>\n" % attachment
            note += "<img src=\"%s\" />\n" % attachment
            note += "</a>\n"
        note += "<br />\n"
        note += "<br />\n"
        return note

    def __body(self, version, notes):
        body = "\n"
        # version
        body += "<h1>\n"
        body += "%s\n"%version
        body += "</h1>\n"
        if notes:
            for n in notes:
                body += self.__note(subject=n["subject"],
                                    content=n["content"],
                                    attachments=n["attachments"])
        else:
            body += "<h2>\n"
            body += "No notes"
            body += "</h2>\n"
        return body

    def build(self, notes_data):
        # add body
        body = ""
        for version_name in notes_data:
            body += self.__body(version_name, notes_data[version_name])

        return self.__html(body)


def name_filter(playlist_name):
    # 将不可以命名的字符改为空格
    special_symbol = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    new_name = " "
    for s in playlist_name:
        if s in special_symbol:
            s = " "
        new_name += s
    return new_name.lstrip()


def write_html(html_file, info):
    html_path = os.path.dirname(html_file)
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    with codecs.open(html_file, 'w', 'utf-8') as f:
        f.write(info)


def notes_to_html(notes_data, output_path, file_name):
    hn = Html_Notes()
    html_info = hn.build(notes_data)
    # html 文件路径
    html_file = os.path.join(output_path, "%s.html" % file_name)
    write_html(html_file, html_info)
    if os.path.exists(html_file):
        return html_file


def htm_to_pdf(html_file, pdf_file):
    if "Windows" in platform.system():
        wkhtmltopdf = os.path.dirname(__file__).replace('\\', '/') + '/wkhtmltox/bin/wkhtmltopdf.exe'
    else:
        wkhtmltopdf = "wkhtmltopdf"
    p = subprocess.Popen([wkhtmltopdf, html_file, pdf_file])
    p.communicate()
    if os.path.exists(pdf_file):
        return pdf_file




if __name__ == "__main__":
    from collections import OrderedDict
    notes_data = OrderedDict([('h45010.cfx.sim.v003', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 27th'), ('content', '动态ok，进预渲染'), ('attachments', [])])), ('h45130.cfx.sim.v003', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 27th'), ('content', 'fox 夹克内T恤应该是紧身，不要松垮'), ('attachments', ['D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18841.188.png', 'D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18841.280.png'])])), ('h95470.cfx.sim.v002', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 29th'), ('content', '抱歉！我必须补充一点，这个镜头是表现飞船超快速下落，头发和衣服都必须表现出惯性的晃动，等同于有风在45度向画面右上方吹。'), ('attachments', [])])), ('h95530.cfx.sim.v001', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 29th'), ('content', '头发请加个持续晃动！'), ('attachments', [])])), ('i20150.cfx.sim.v004', OrderedDict([('subject', "ella's Note on i20150.cfx.sim.v004 and i20150"), ('content', '拍屏文件多了一帧'), ('attachments', [])])), ('i20190.cfx.sim.v001', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 27th'), ('content', '布料错误太多'), ('attachments', ['D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18846.101.png', 'D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18846.36.png', 'D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18846.94.png'])])), ('i20250.cfx.sim.v003', OrderedDict([('subject', "ella's Note on i20250.cfx.sim.v003 and i20250"), ('content', '拍屏文件多了3帧'), ('attachments', [])])), ('i20270.cfx.sim.v004', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 27th'), ('content', '夹克太飘，其他ok'), ('attachments', ['D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18849.110.png', 'D:\\temp\\html\\choki-cfx.sim-QC-20190827\\test\\attachments\\annot_version_18849.79.png'])])), ('i20390.cfx.sim.v002', OrderedDict([('subject', "ella's Note on i20390.cfx.sim.v002 and i20390"), ('content', '拍屏文件多了6帧'), ('attachments', [])])), ('i20410.cfx.sim.v002', OrderedDict([('subject', 'choki-cfx.sim-QC-20190827 - August 29th'), ('content', 'Dylan头发垂度有点错误'), ('attachments', [])]))])
    notes_to_html(notes_data)