import pybaseball as pyb
import pandas as pd
import requests
from typing import Optional


def find_player_ids(bref_id: str) -> dict:
    """Finds a list of ids based on the bref id for future development

    Returns a keyed dict of the player ids from different sources including pybaseball

    Args:
        bref_id: A string indicitive of the cards bref id.

    Returns:
        A dictionary containing the debut information of the player along with ids for linking.

    """
    return pyb.playerid_reverse_lookup([bref_id], "bbref").iloc[0].to_dict()
