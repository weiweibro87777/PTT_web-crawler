import requests
from bs4 import BeautifulSoup
import pandas as pd

titles = []
push = []
date = []
url_list = []
not_exist = BeautifulSoup('<a>(本文已被刪除)</a>', 'lxml').a ## '本文已被刪除'的結構不同，自行生成<a>

#程式歡迎語
print("**歡迎來到PTT_搜尋引擎**")
print("\n")
print("18歲以上看板爬取功能尚未置入")
print("請注意！看板名稱英文大小寫需正確！")
w = str(input("請輸入想爬取的版："))
x = str(input("請輸入想爬取的關鍵字："))
print("日期格式輸入範例(MDD)：813")
print("\n")
start_date = int(input("請輸入起始日期："))
end_date = int(input("請輸入結束日期："))

#抓使用者輸入之關鍵字所有網頁
z = 0
while(True):
	z += 1
	real_request_url = "https://www.ptt.cc/bbs/" + str(w) + "/search?page=" + str(z) + "&q=" + x
	response = requests.get(real_request_url)
	response_text = response.text
	soup = BeautifulSoup(response_text, "html.parser")

#判斷這一頁目錄有沒有文章(有就接下一步，沒有就break)
	if soup.select(".title"):
		pass
	else:
		break

#抓發文日期
	for i in soup.find_all('div', 'r-ent'):
		meta = i.find('div', 'title').find('a') or not_exist
		b = i.find('div', 'date').getText()
		#print(b)
		re_b = int(b.replace('/', ''))
		#print(re_a)
		#date.append(b)
		#print(b)

#判斷發文日期是否符合使用者需求並丟到list
		if (start_date <= re_b and re_b <= end_date):
			pass
		else:
			continue
		date.append(b)
		print(b)

#抓網址
		url = i.find('div', 'title').find('a')
		a = 'https://www.ptt.cc'
		if url is not None:
			url_list.append(a + url.get('href'))
		else:
			url_list.append("(本文已被刪除)")
		print(a + url.get('href'))

#抓標題
		c = i.find('div', 'title').find('a')
		if c is not None:
			titles.append(c.text)
		else:
			titles.append('(本文已被刪除)')
		print(c.text)

#抓推文數
		push_count = i.find('div', 'nrec').find('span')
		if push_count is not None:
			push.append(push_count.text)
		else:
			push.append("0")

print("\n")
print("轉檔中...請稍後")

#轉為DataFrame
df = pd.DataFrame(
    {
        '標題' : titles,
		'推文數' : push,
        '發文日期' : date,
        '文章連結' : url_list
    }
)

#另存為csv
df.to_csv( x +"回傳結果.csv", index = False, encoding = "utf_8_sig")

#程式結束
len_titles = len(titles)
print("本次共爬出 {} 篇文章".format(len_titles))
print("\n")
end = input("請輸入任意鍵結束程式：")