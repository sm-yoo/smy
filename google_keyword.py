from bs4 import BeautifulSoup
import requests

def get_keyword_number(keyword):
    # keyword = "나루토"
    url = "https://www.google.com/search?q={}".format(keyword)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    # 웹 요청
    res = requests.get(url, headers=headers)
    # print(res.text)
    # print(type(res.text)) # <class 'str'>

    # 구문 분석 - 파싱
    soup = BeautifulSoup(res.text, 'lxml')
    # print(type(soup)) # <class 'bs4.BeautifulSoup'>

    # 원하는 것 추출
    number = soup.select_one('#result-stats')
    # print(number) # <div id="result-stats">검색결과 약 6,960,000개<nobr> (0.53초) </nobr></div>

    # 실질적으로 사람에게 보여지는 부분
    # print(number.text) # 검색결과 약 6,960,000개 (0.53초) 

    number = soup.select_one('#result-stats').text


    # 정리
    # print(number[number.find('약'):number.rfind('개')]) # 약 6,880,000
    # print(number[number.find('약')+2:number.rfind('개')]) # 6,880,000
    # print(number[number.find('약')+2:number.rfind('개')].replace(',','')) # 6880000

    number = int(number[number.find('약')+2:number.rfind('개')].replace(',',''))
    # print(number) # 6880000

    return number

# 테스트 코드
if __name__ == "__main__":
    print(get_keyword_number('침착맨'))
