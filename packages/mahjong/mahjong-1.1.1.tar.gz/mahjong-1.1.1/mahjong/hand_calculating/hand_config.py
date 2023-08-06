# -*- coding: utf-8 -*-
from mahjong.constants import EAST
from mahjong.hand_calculating.yaku_config import YakuConfig


class HandConfig(object):
    """
    Special class to pass various settings to the hand calculator object
    """
    yaku = None

    is_tsumo = False
    is_riichi = False
    is_ippatsu = False
    is_rinshan = False
    is_chankan = False
    is_haitei = False
    is_houtei = False
    is_daburu_riichi = False
    is_nagashi_mangan = False
    is_tenhou = False
    is_renhou = False
    is_chiihou = False

    is_dealer = False
    player_wind = None
    round_wind = None

    has_open_tanyao = False
    has_aka_dora = False

    disable_double_yakuman = False

    def __init__(self,
                 is_tsumo=False,
                 is_riichi=False,
                 is_ippatsu=False,
                 is_rinshan=False,
                 is_chankan=False,
                 is_haitei=False,
                 is_houtei=False,
                 is_daburu_riichi=False,
                 is_nagashi_mangan=False,
                 is_tenhou=False,
                 is_renhou=False,
                 is_chiihou=False,
                 player_wind=None,
                 round_wind=None,
                 has_open_tanyao=False,
                 has_aka_dora=False,
                 disable_double_yakuman=False):

        self.yaku = YakuConfig()

        self.is_tsumo = is_tsumo
        self.is_riichi = is_riichi
        self.is_ippatsu = is_ippatsu
        self.is_rinshan = is_rinshan
        self.is_chankan = is_chankan
        self.is_haitei = is_haitei
        self.is_houtei = is_houtei
        self.is_daburu_riichi = is_daburu_riichi
        self.is_nagashi_mangan = is_nagashi_mangan
        self.is_tenhou = is_tenhou
        self.is_renhou = is_renhou
        self.is_chiihou = is_chiihou

        self.player_wind = player_wind
        self.round_wind = round_wind
        self.is_dealer = player_wind == EAST

        self.has_open_tanyao = has_open_tanyao
        self.has_aka_dora = has_aka_dora

        self.disable_double_yakuman = disable_double_yakuman
