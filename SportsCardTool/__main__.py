from .scraping_tool import grab_card_list, dump_data

if __name__ == "__main__":
    dump_data(grab_card_list())
