from .scraping_tool import grab_card_list, dump_data, grab_year_links

if __name__ == "__main__":
    dump_data(grab_card_list(grab_year_links(['2023'])))
