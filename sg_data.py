# -*- coding: utf-8 -*-
__author__ = "yangtao"


import collections
import os

import shotgun_api3

try:
    import sg_script
    url = sg_script.URL
    script_name = sg_script.SCRIPT_NAME
    api_key = sg_script.API_KEY
except:
    import config_tool
    url = config_tool.read("SG", "url")
    script_name = config_tool.read("SG", "script_name")
    api_key = config_tool.read("SG", "api_key")
    if not url or not script_name or not  api_key:
        raise Exception("config.ini 需要填写一些必要信息")




SG = shotgun_api3.Shotgun(url,
                          script_name=script_name,
                          api_key=api_key)


class Playlist_Notes:
    def __init__(self, playlist_name: str):
        self.playlist_name = playlist_name

    def get(self) -> "{version_name: [notes]}":
        # 获取所有 version 实例
        version_entitys = self.get_playlist_versions(self.playlist_name)
        if not version_entitys:
            return
        # 获取对应 notes
        notes = collections.OrderedDict()
        for v in version_entitys:
            notes[v["name"]] = []
            note_entitys = self.get_version_notes(v)
            print("Get: %s"%v["name"])
            for n in note_entitys:
                note = collections.OrderedDict()
                note["subject"] = n["subject"]
                note["content"] = n["content"]
                note["attachments"] = n["attachments"]
                notes[v["name"]].append(note)
        return notes

    def get_playlist_versions(self, playlist_name) -> list:
        # 获取所有版本文件
        fields = ["versions"]
        filters = [["code", "is", playlist_name]]
        playlists_entity = SG.find("Playlist", filters, fields)
        if len(playlists_entity) == 1:
            return playlists_entity[0]["versions"]
        elif len(playlists_entity) == 0:
            raise Exception("找不到名为：\"%s\" 的 Playlist" % playlist_name)
        else:
            raise Exception("多于一个 Playlist 实体名字为：%s"%playlist_name)

    def get_version_notes(self, version_entity):
        fields = ["id", "subject", "content", "user", "addressings_to", "attachments"]
        filters = [["note_links", "in", version_entity]]
        note_entitys = SG.find("Note", filters, fields)
        return note_entitys


def download_attachment(attachment_entity, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    attachment_file = os.path.join(download_path, attachment_entity["name"])
    SG.download_attachment(attachment_entity, attachment_file)
    #print("Download: %s"%attachment_file)

    if os.path.exists(attachment_file):
        return attachment_file


def get_notes_data(playlist, attachments_download_path=None):
    pn = Playlist_Notes(playlist)
    notes_data = pn.get()

    for notes_list in notes_data.values():
        for note in notes_list:
            attachments = note["attachments"]
            new_attachments = []
            # 下载附件并将保存地址替换原值
            for attachment in attachments:
                if attachments_download_path:
                    attachment_url = download_attachment(attachment, attachments_download_path)
                else:
                    attachment_url = SG.get_attachment_download_url(attachment)

                if attachment_url:
                    new_attachments.append(attachment_url)

            note["attachments"] = new_attachments
    return notes_data




if __name__ == "__main__":
    import pprint
    notes_data = get_notes_data("choki-cfx.sim-QC-20190827", r"D:\temp\html\choki-cfx.sim-QC-20190827\test")
    pprint.pprint(notes_data)
