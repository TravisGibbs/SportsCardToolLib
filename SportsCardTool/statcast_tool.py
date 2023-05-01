from typing import Optional

import pandas as pd
import requests


STATCAST_TABLES_BATTER = {
    "Percentile Rankings": [
        "Year",
        "xwOBA",
        "xBA",
        "xSLG",
        "xISO",
        "xOBP",
        "Brl",
        "Brl%",
        "EV",
        "Max EV",
        "Hard Hit%",
        "K%",
        "BB%",
        "Whiff%",
        "Chase Rate",
        "Speed",
        "OAA",
        "Arm Strength",
    ],
    "Statcast Batting Statistics": [
        "Season",
        "Age",
        "Pitches",
        "Batted Balls",
        "Barrels",
        "Barrel %",
        "Barrel/PA",
        "Exit Velocity",
        "Max EV",
        "Launch Angle",
        "Sweet Spot %",
        "XBA",
        "XSLG",
        "WOBA",
        "XWOBA",
        "XWOBACON",
        "HardHit%",
        "K%",
        "BB%",
    ],
    "Batted Ball Profile": [
        "Season",
        "GB %",
        "FB %",
        "LD %",
        "PU %",
        "Pull %",
        "Straight %",
        "Oppo %",
        "Weak %",
        "Topped %",
        "Under %",
        "Flare/Burner %",
        "Solid %",
        "Barrel %",
        "Barrel/PA",
    ],
    "Run Values by Pitch Type": [
        "Year",
        "Pitch Type",
        "Team",
        "RV/100",
        "Run Value",
        "Pitches",
        "%",
        "PA",
        "BA",
        "SLG",
        "wOBA",
        "Whiff%",
        "K%",
        "PutAway %",
        "xBA",
        "xSLG",
        "xwOBA",
        "Hard Hit %",
    ],
    "Plate Discipline": [
        "Season",
        "Pitches",
        "Zone %",
        "Zone Swing %",
        "Zone Contact %",
        "Chase %",
        "Chase Contact %",
        "Edge %",
        "1st Pitch Swing %",
        "Swing %",
        "Whiff %",
        "Meatball %",
        "Meatball Swing %",
    ],
    "Advanced MLB Batting Statistics": [
        "Season",
        "Tm",
        "LG",
        "PA",
        "TB",
        "LOB",
        "SAC",
        "SF",
        "BABIP",
        "XBH",
        "GIDP",
        "GIDPO",
        "NP",
        "P/PA",
        "K/PA",
        "HR/PA",
        "BB/K",
        "ISO",
        "ROE",
        "WO",
    ],
    "Statcast Outs Above Average": [
        "Year",
        "Team",
        "Pos",
        "OAA",
        "In",
        "Lateral toward 3B",
        "Lateral toward 1B",
        "Back",
        "RHB",
        "LHB",
        "Attempts",
        "Success Rate",
        "Estimated Success Rate",
        "Success Rate Added",
    ],
    "Statcast Fielder Positioning": [
        "Season",
        "Team",
        "Pos",
        "PA",
        "Depth (ft.)",
        "Angle",
    ],
    "Statcast Running Statistics": [
        "Season",
        "Age",
        "Sprint Speed (ft/s)",
        "HP to 1st",
        "Bolts",
        "Pos Rank",
        "Age Rank",
        "Lg Rank",
        "% Rank",
    ],
}

STATCAST_TABLES_PITCHER = {
    "Statcast Statistics": [
        "Season",
        "Age",
        "Pitches",
        "Batted Balls",
        "Barrels",
        "Barrel %",
        "Barrel/PA",
        "Exit Velocity",
        "Max EV",
        "Launch Angle",
        "Sweet Spot %",
        "XBA",
        "XSLG",
        "WOBA",
        "XWOBA",
        "XWOBACON",
        "HardHit%",
        "K%",
        "BB%",
        "ERA",
        "xERA",
    ],
    "Batted Ball Profile": [
        "Season",
        "GB %",
        "FB %",
        "LD %",
        "PU %",
        "Pull %",
        "Straight %",
        "Oppo %",
        "Weak %",
        "Topped %",
        "Under %",
        "Flare/Burner %",
        "Solid %",
        "Barrel %",
        "Barrel/PA",
    ],
    "Pitch Movement": [
        ("Unnamed: 0_level_0", "Year"),
        ("Unnamed: 1_level_0", "Pitch"),
        ("Unnamed: 2_level_0", "Team"),
        ("Unnamed: 3_level_0", "Hand"),
        ("Unnamed: 4_level_0", "#"),
        ("Unnamed: 5_level_0", "MPH"),
        ("Vertical Movement (inches)", "Inches of Drop"),
        ("Vertical Movement (inches)", "vs Avg"),
        ("Vertical Movement (inches)", "% vs Avg"),
        ("Horizontal Movement (inches)", "Inches of Break"),
        ("Horizontal Movement (inches)", "vs Avg"),
        ("Horizontal Movement (inches)", "% Break vs Avg"),
    ],
    "Run Values by Pitch Type": [
        "Year",
        "Pitch Type",
        "Team",
        "RV/100",
        "Run Value",
        "Pitches",
        "%",
        "PA",
        "BA",
        "SLG",
        "wOBA",
        "Whiff%",
        "K%",
        "PutAway %",
        "xBA",
        "xSLG",
        "xwOBA",
        "Hard Hit %",
    ],
    "Spin Direction": [
        "Year",
        "Pitch Type",
        "Pitches",
        "MPH",
        "Active Spin %",
        "Total Movement (In.)",
        "Spin-Based",
        "Observed",
        "Deviation",
    ],
    "Swing/Take": [
        ("Unnamed: 0_level_0", "Year"),
        ("Unnamed: 1_level_0", "Team"),
        ("Unnamed: 2_level_0", "PA"),
        ("Unnamed: 3_level_0", "Pitches"),
        ("Runs", "Heart"),
        ("Runs", "Shadow"),
        ("Runs", "Chase"),
        ("Runs", "Waste"),
        ("Runs", "All"),
    ],
    "Plate Discipline": [
        "Season",
        "Pitches",
        "Zone %",
        "Zone Swing %",
        "Zone Contact %",
        "Chase %",
        "Chase Contact %",
        "Edge %",
        "1st Pitch Strike %",
        "Swing %",
        "Whiff %",
        "Meatball %",
        "Meatball Swing %",
    ],
    "Percentile Rankings": [
        "Year",
        "xwOBA  / xERA",
        "xBA",
        "xSLG",
        "xISO",
        "xOBP",
        "Brl",
        "Brl%",
        "EV",
        "Hard Hit%",
        "K%",
        "BB%",
        "Whiff%",
        "Chase Rate",
        "FB Velo",
        "FB Spin",
        "CB Spin",
        "Extension",
    ],
    "Statcast Shift Statistics": [
        ("Unnamed: 0_level_0", "Year"),
        ("Unnamed: 1_level_0", "PA"),
        ("Unnamed: 2_level_0", "wOBA"),
        ("vs RHH", "PA"),
        ("vs RHH", "Shifts"),
        ("vs RHH", "%"),
        ("vs LHH", "PA"),
        ("vs LHH", "Shifts"),
        ("vs LHH", "%"),
    ],
    "Pitch Tempo": [
        ("Unnamed: 0_level_0", "Season"),
        ("Unnamed: 1_level_0", "Team"),
        ("Bases Empty", "Pitches"),
        ("Bases Empty", "Tempo"),
        ("Bases Empty", "Fast %"),
        ("Bases Empty", "Slow %"),
        ("Runners On Base", "Pitches"),
        ("Runners On Base", "Tempo"),
        ("Runners On Base", "Fast %"),
        ("Runners On Base", "Slow %"),
    ],
}


def statcast_clean_column_names(column_name):
    if type(column_name) is tuple:
        if "Unnamed:" in str(column_name[0]):
            return str(column_name[1])
        else:
            return str(column_name[0]) + " " + str(column_name[1])
    else:
        return column_name.strip()


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
