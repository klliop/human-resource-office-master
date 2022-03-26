import os
from typing import List
from my_db import DB
from to import Token, T, TB, J, JB, M, MB, A, AB, S, SB

class User():
    discord_id: int = 0
    discord_name: str = "----"
    position: str = ""
    win: int = 0
    lose: int = 0
    sold: bool = False
    def __init__(self, id, name, pos, win, lose):
        self.discord_id = id
        self.discord_name = name
        self.position = pos
        self.win = win
        self.lose = lose

    def __eq__(self, other):
        if self.discord_id == other.discord_id:
            return True
        else:
            return False

    def print(self) -> str:
        pos = "{}{}{}{}{}".format(T if self.position[0] == '1' else TB,J if self.position[1] == '1' else JB,M if self.position[2] == '1' else MB,A if self.position[3] == '1' else AB,S if self.position[4] == '1' else SB)
        return pos

class Team():
    identifier: int
    member: list = [0,0,0,0,0]
    def __init__(self, id):
        self.identifier = id
        self.member = [0,0,0,0,0]
    def set_member(self, u:User, p:int):
        if type(self.member[p]) is User and self.member[p].discord_name != "----" :
            return False, "이미 선정된 역할군입니다."
        self.member[p] = u
        return True, "팀원 선정 완료"

class Game:
    game_owner: int = -1
    game_state: int = 0
    # 0 : IDLE / 1 : 모집 / 2 : 모집완료 / 3 : 팀장선정 / 4 : 1팀 2픽 / 5 : 2팀 2픽 / 6 : 2팀 3픽 / 7 : 1팀 3픽 / 8 : 1팀 4픽 / 9 : 2팀 4픽 / 10 : 2팀 5픽 / 11 : 게임 중
    team1_master: int = -1
    team2_master: int = -1
    team1 = Team(1)
    team2 = Team(2)
    participant: list = []
    def new_game(self, owner_id:int):
        if self.game_owner != -1:
            return False, "이미 시작되었습니다."
        self.game_owner = owner_id
        self.game_state = 1
        self.team1_master = -1
        self.team2_master = -1
        self.team1 = Team(1)
        self.team2 = Team(2)
        self.participant = []
        return True, "팀원 모집을 시작 합니다."

    def cancel_game(self, owner_id:int):
        if self.game_state == -1:
            return False, "아직 시작되지 않았습니다."
        if self.game_owner != owner_id:
            return False, "방장이 아닙니다."
        self.game_owner = -1
        self.game_state = 0
        self.team1_master: int = -1
        self.team2_master: int = -1
        self.team1 = Team(1)
        self.team2 = Team(2)
        self.participant = []

    def draft(self):
        if self.game_state == 2:
            return self.game_state, '팀장 선정 \n !팀장 1팀팀장 2팀팀장 포지션(탑/정글/미드/원딜/서폿) \n ex) !팀장 1 2 탑'
        if self.game_state == 3:
            return self.game_state, '1팀에서 1명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 4:
            return self.game_state, '2팀에서 2명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 5:
            return self.game_state, '2팀에서 2명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 6:
            return self.game_state, '1팀에서 2명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 7:
            return self.game_state, '1팀에서 2명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 8:
            return self.game_state, '2팀에서 2명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 9:
            return self.game_state, '2팀에서 2명을 픽해주세요. \n !픽 매물번호 포지션(탑/정글/미드/원딜/서폿) \n ex) !픽 1 탑'
        if self.game_state == 10:
            return self.game_state, '게임을 시작할 수 있습니다.'
        else:
            return self.game_state, "아직 시작할 수 없습니다."

    def win(self, owner_id:int, s:str):
        if self.game_owner != owner_id:
            return False, "방장이 아닙니다."
        if self.game_state != 13:
            return False, "게임 중이 아닙니다."

        if s == "1팀":
            for mem in team1:
                DB.set_win(mem.discord_id)
            for mem in team2:
                DB.set_lose(mem.discord_id)
        elif s == "2팀":
            for mem in team2:
                DB.set_win(mem.discord_id)
            for mem in team1:
                DB.set_lose(mem.discord_id)
        return True, "{} 승리".format(s)

    def swap(self):
        a = self.team1
        self.team1 = self.team2
        self.team2 = a

    def attend(self, u:User):
        if self.game_state != 1:
            return -1, "지금은 참가할 수 없습니다."
        if self.participant.count(u) == 1:
            return -1, "이미 참가중입니다."
        self.participant.append(u)
        if len(self.participant) == 10:
            self.game_state = 2
        return len(self.participant), "참가"

    def absent(self, u:User):
        if self.game_state != 1:
            return -1, "지금은 참가 취소할 수 없습니다."
        if self.participant.count(u) == 1:
            self.participant.remove(u)
            self.game_state = 1
            return len(self.participant), "참가 취소."
        return -1, "참가중이지 않습니다."

    def set_team_master(self, owner_id:int, i1:int, i2:int, p:int):
        if self.game_owner != owner_id:
            return False, "방장이 아닙니다."
        if self.game_state != 2:
            return False, "지금은 팀장을 정할 수 없습니다."
        if i1 > 10 or i1 < 0 or i2 > 10 or i2 < 0:
            return False, "인덱스 오류."
        if p > 4 or p < 0:
            return False, "인덱스 오류."
        if i1 == i2:
            return False, "동일한 인원입니다."

        u1 = self.participant[i1 - 1]
        u2 = self.participant[i2 - 1]
        self.team1_master = u1.discord_id
        self.team2_master = u2.discord_id
        self.team1.set_member(u1, p)
        self.team2.set_member(u2, p)
        self.participant[i1 - 1].sold = True
        self.participant[i2 - 1].sold = True

        self.game_state = 3

        return True, "팀장 선정 완료"

    def set_pick(self, id:int, i:int, p:int):
        if i > 10 or i < 0:
            return False, "인덱스 오류."
        if p > 4 or p < 0:
            return False, "인덱스 오류."

        now_master = -1
        # 0 : IDLE / 1 : 모집 / 2 : 모집완료 / 3 : 팀장선정 / 4 : 1팀 2픽 / 5 : 2팀 2픽 / 6 : 2팀 3픽 / 7 : 1팀 3픽 / 8 : 1팀 4픽 / 9 : 2팀 4픽 / 10 : 2팀 5픽 / 11 : 게임 중

        if self.game_state == 3 or self.game_state == 6 or self.game_state == 7:
            now_master = 1
        elif self.game_state == 4 or self.game_state == 5 or self.game_state == 8 or self.game_state == 9:
            now_master = 2
        else:
            return False, "지금은 픽을 할 수 없습니다."

        if now_master == 1 and id != self.team1_master:
            return False, "1팀 팀장의 픽 순서입니다."
        if now_master == 2 and id != self.team2_master:
            return False, "2팀 팀장의 픽 순서입니다."

        if self.participant[i - 1].sold:
            return False, "이미 판매된 매물입니다."

        ret = 0
        if now_master == 1:
            ret = self.team1.set_member(self.participant[i - 1], p)
        elif now_master == 2:
            ret = self.team2.set_member(self.participant[i - 1], p)

        if ret[0] == False:
            return ret

        self.game_state += 1
        self.participant[i - 1].sold = True

        ret_str = ""

        if self.game_state == 10:
            for mem in self.participant:
                if mem.sold == False:
                    remain = 0
                    for a in self.team1.member:
                        if type(a) is User :
                            remain += 1
                        else:
                            break
                    remain_pos = ""
                    if remain == 0:
                        remain_pos = "탑"
                    elif remain == 1:
                        remain_pos = "정글"
                    elif remain == 2:
                        remain_pos = "미드"
                    elif remain == 3:
                        remain_pos = "원딜"
                    elif remain == 4:
                        remain_pos = "서폿"
                    self.team1.member[remain] = mem
                    ret_str = "{}님은 1팀 {}로 배정됩니다.\n". format(mem.discord_name, remain_pos)

        ret_str += "픽 완료"
        return True, "픽 완료"

