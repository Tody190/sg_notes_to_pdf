# -*- coding: utf-8 -*-
__author__ = "yangtao"


import collections

import shotgun_api3

import config_tool




class Playlist_Notes:
    sg_info = config_tool.read("SG")
    sg = shotgun_api3.Shotgun(sg_info["url"],
                              script_name=sg_info["script_name"],
                              api_key=sg_info["api_key"])

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
            notes[v["name"]] = collections.OrderedDict()
            note_entitys = self.get_version_notes(v)
            for n in note_entitys:
                notes[v["name"]]["subject"] = n["subject"]
                notes[v["name"]]["content"] = n["content"]
        return notes

    def get_playlist_versions(self, playlist_name) -> list:
        # 获取所有版本文件
        fields = ["versions"]
        filters = [["code", "is", playlist_name]]
        playlists_entity = self.sg.find("Playlist", filters, fields)
        if len(playlists_entity) == 1:
            return playlists_entity[0]["versions"]
        else:
            raise Exception("多于一个 Playlist 实体名字为：%s"%playlist_name)

    def get_version_notes(self, version_entity):
        fields = ["subject", "content", "user", "addressings_to"]
        filters = [["note_links", "in", version_entity]]
        note_entitys = self.sg.find("Note", filters, fields)
        return note_entitys

if __name__ == "__main__":
    import pprint
    pn = Playlist_Notes("choki-cfx.sim-QC-20190827")
    print(pn.get())
