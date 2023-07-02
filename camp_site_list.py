import requests
from bs4 import BeautifulSoup
import json
import re


def crawl_camping_sites():
    url = "https://gocamping.or.kr/bsite/camp/info/list.do"
    params = {
        "searchKrwd": "",  # 원하는 키워드로 필터링하려면 이 부분을 채워넣으세요.
        "listOrdrTrget": "last_updusr_pnttm",  # 최근 업데이트 순으로 정렬
        "listOrdr": "desc",  # 내림차순 정렬
        "pageIndex": 1,  # 페이지 인덱스
        "listRowPerPage": 2,  # 페이지당 보여줄 개수 (100으로 설정)
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        camping_sites = soup.select(
            "div.camp_search_list > ul > li > div.c_list"
        )  # 클래스 이름이 "camp_search_list"인 경우

        # ul_element = div_element.find("ul")
        # camping_sites = ul_element.find_all("li")
        print(len(camping_sites))
        camping_list = []
        for camping_site in camping_sites:
            site_url = camping_site.find("a")["href"]
            # print(camping_site.find("a", {"class": "dc_none"})["href"])
            e_addr = camping_site.find("li", {"class": "addr"})  # 클래스 이름이 "addr"인 경우
            e_call = camping_site.find(
                "li", {"class": "call_num"}
            )  # 클래스 이름이 "call_num"인 경우
            site_address = e_addr.text if e_addr else ""
            site_phone = e_call.text if e_call else ""

            # site_url_element = camping_site.select_one("div.camp_cont > h2.camp_tt > a")

            # site_url = site_url_element["href"]
            # print(site_url)

            # site_url_element = camping_site.find("a", {"class": "dc_none"})
            # site_url = site_url_element["href"] if site_url_element else ""
            # print("url :" + site_url)

            site_response = requests.get("https://gocamping.or.kr" + site_url)
            if site_response.status_code == 200:
                site_soup = BeautifulSoup(site_response.content, "html.parser")
                links = site_soup.find_all("a", attrs={"title": "새창열림"})
                for link in links:
                    href = link.get("href")

                site_homepage = href

                site_name_element = site_soup.select_one("p.camp_name")
                site_name = (
                    site_soup.select_one("p.camp_name").text
                    if site_name_element
                    else ""
                )

            else:
                site_name = ""
                site_homepage = ""

            camping = {
                "캠핑장명": site_name,
                "주소": site_address,
                "홈페이지": site_homepage,
                "전화번호": site_phone,
            }

            camping_list.append(camping)

        with open("camping_info.json", "w", encoding="utf-8") as f:
            json.dump(camping_list, f, ensure_ascii=False, indent=4)
            print("JSON 파일로 저장되었습니다.")
    else:
        print("Failed to retrieve data.")


crawl_camping_sites()


if __name__ == "__main__":
    crawl_camping_sites()
