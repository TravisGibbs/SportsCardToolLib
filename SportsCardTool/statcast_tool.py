from typing import Optional

import pandas as pd
import requests

from SportsCardToolLib.SportsCardTool.util import (
    STATCAST_TABLES_BATTER,
    STATCAST_TABLES_PITCHER,
    statcast_clean_column_names,
)


def statcast_batter_player_stats(
    player_id: str, tables_names: Optional[list] = ["ALL"]
) -> dict[str, pd.DataFrame]:
    """
    Retrieves tables from individual batters page on Baseball Savant with options to select table of interest.
    ARGUMENTS
        player_id : INT : the player's MLBAM ID. Find this by calling pybaseball.playerid_lookup(last_name, first_name),
            finding the correct player, and selecting their key_mlbam.
        table_names : A list of strings containing the names of the tables to be extracted from the player's savant,
            alternatively left blank and all named tables will be gathered
    """
    url = f"https://baseballsavant.mlb.com/savant-player/{str(player_id)}?stats=statcast-r-hitting-mlb&playerType=batter"
    res = requests.get(url).content
    data = pd.read_html(res)
    dfs = {}

    for df in data:
        for table_name in STATCAST_TABLES_BATTER:
            if list(df.columns) == STATCAST_TABLES_BATTER[table_name] and (
                table_name in tables_names or "ALL" in tables_names
            ):
                df.columns = [statcast_clean_column_names(name) for name in df.columns]
                dfs[table_name] = df

    return dfs


def statcast_pitcher_page_stats(player_id: str, tables_names: Optional[list] = ["ALL"]):
    """
    Retrieves tables from individual batters page on Baseball Savant with options to select table of interest.
    ARGUMENTS
        player_id : INT : the player's MLBAM ID. Find this by calling pybaseball.playerid_lookup(last_name, first_name),
            finding the correct player, and selecting their key_mlbam.
        table_names : A list of strings containing the names of the tables to be extracted from the player's savant,
            alternatively left blank and all named tables will be gathered
    """
    url = f"https://baseballsavant.mlb.com/savant-player/{str(player_id)}?stats=statcast-r-hitting-mlb&playerType=batter"
    res = requests.get(url).content
    data = pd.read_html(res)
    dfs = {}

    for df in data:
        for table_name in STATCAST_TABLES_PITCHER:
            if list(df.columns) == STATCAST_TABLES_PITCHER[table_name] and (
                table_name in tables_names or "ALL" in tables_names
            ):
                df.columns = [statcast_clean_column_names(name) for name in df.columns]
                dfs[table_name] = df

    return dfs
