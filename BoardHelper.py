#-*- coding: utf-8 -*-
import const
from re import search as ReSearch

def __parseBoards(fp):
    boardsinfo = {}
    cur_board_name = ""
    for line in fp.readlines():
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        value = line.split("=")[-1]
        if ReSearch(const.boards_name_matcher, line):
            cur_board_name = value
            boardsinfo[cur_board_name] = {}
        if cur_board_name == "":
            continue
            
        if ReSearch(const.boards_upload_protocol_matcher, line):
            boardsinfo[cur_board_name]["protocol"] = value
        if ReSearch(const.boards_upload_maximum_size_matcher, line):
            boardsinfo[cur_board_name]["maximum_size"] = int(value)
        if ReSearch(const.boards_upload_speed_matcher, line):
            boardsinfo[cur_board_name]["speed"] = value
        if ReSearch(const.boards_mcu_matcher, line):
            boardsinfo[cur_board_name]["mcu"] = value
    
    return boardsinfo
    
def getBoardsInfo():
    try:
        with open(const.boards_txt, "r", encoding="utf-8", errors="replace") as fp:
            boardsinfo = __parseBoards(fp)
        return True, boardsinfo
    except Exception as exc:
        return False, repr(exc)
