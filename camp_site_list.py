import requests
from bs4 import BeautifulSoup
import json
import re

def crawl_camping_sites():

    url = "https://gocamping.or.kr/bsite/camp/info/list.do?pageUnit=3664"
    # params = {
    #     "searchKrwd": "",  # 원하는 키워드로 필터링하려면 이 부분을 채워넣으세요.
    #     "listOrdrTrget": "last_updusr_pnttm",  # 최근 업데이트 순으로 정렬
    #     "listOrdr": "desc",  # 내림차순 정렬
    #     "pageIndex": 1,  # 페이지 인덱스
    #     "pageUnit": 3524,  # 페이지당 보여줄 개수 (100으로 설정)
    # }

    response = requests.get(url)
    # response = requests.get(url, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        camping_sites = soup.select(
            "div.camp_search_list > ul > li > div.c_list"
        )  # 클래스 이름이 "camp_search_list"인 경우

        # ul_element = div_element.find("ul")
        # camping_sites = ul_element.find_all("li")
        print(len(camping_sites))
        camping_list = []
        idx = 0
        for camping_site in camping_sites:
            site_url = camping_site.find("a")["href"]
            # print(camping_site.find("a", {"class": "dc_none"})["href"])
            
            e_addr = camping_site.find("li", {"class": "addr"})  # 클래스 이름이 "addr"인 경우
            e_call = camping_site.find(
                "li", {"class": "call_num"}
            )  # 클래스 이름이 "call_num"인 경우
            site_address = e_addr.text if e_addr else ""
            site_phone = e_call.text if e_call else ""

            pattern = r"\[([^]]+)\]"

            temp = camping_site.select_one("div.camp_cont > h2.camp_tt > a").text
            idx = idx + 1
            print(idx)
            match = re.search(pattern, temp)

            if match:
                site_address_all = match.group(1)  # 첫 번째 그룹의 값 (하하하)
                site_address_filter1, site_address_filter2 = site_address_all.split(" ")
                
                # site_address_filter2 = match.group(2)  # 두 번째 그룹의 값 (호호호)
                
                # print(site_address_filter2)
            else:
                print("일치하는 패턴을 찾을 수 없습니다.")




     

            # site_url_element = camping_site.select_one("div.camp_cont > h2.camp_tt > a")

            # site_url = site_url_element["href"]
            # print(site_url)

            # site_url_element = camping_site.find("a", {"class": "dc_none"})
            # site_url = site_url_element["href"] if site_url_element else ""
            # print("url :" + site_url)
            try:
                site_response = requests.get("https://gocamping.or.kr" + site_url)
            except:
                continue
            if site_response.status_code == 200:
                site_soup = BeautifulSoup(site_response.content, "html.parser")
                links = site_soup.find_all("a", attrs={"title": "새창열림"})
                for link in links:
                    href = link.get("href")

                site_homepage = href if href else ""

                site_name_element = site_soup.select_one("p.camp_name")
                site_name = (
                    site_soup.select_one("p.camp_name").text
                    if site_name_element
                    else ""
                )

                site_image_element = site_soup.select_one("div.img_b > img")
                site_image = (
                    site_soup.select_one("div.img_b > img")["src"]
                    if site_image_element
                    else ""
                )
                

            else:
                site_name = ""
                site_homepage = ""

            camping = {
                "name": site_name,
                "address": site_address,
                "region1": site_address_filter1,
                "region2": site_address_filter2,
                "homePage": site_homepage,
                "phone": site_phone,
                "image": site_image,
            }

            camping_list.append(camping)

        with open("camping_info.json", "w", encoding="utf-8") as f:
            json.dump(camping_list, f, ensure_ascii=False, indent=4)
            print("JSON 파일로 저장되었습니다.")
    else:
        print("Failed to retrieve data.")


crawl_camping_sites()


# if __name__ == "__main__":
#     crawl_camping_sites()
