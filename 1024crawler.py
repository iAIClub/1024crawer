import urllib.request
from lxml import etree
proxy_handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:1080/'})
opener = urllib.request.build_opener(proxy_handler)
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
    }
def crawerEach(url,urldir):
    request = urllib.request.Request(url, headers = headers)
    resp=opener.open(request)
    html=resp.read().decode('gbk')
    selector = etree.HTML(html)
    content_field = selector.xpath('//tbody[1]/tr/td/h3/a')
    for each in content_field:
        urldir[each.xpath('string(.)')] = "http://cc.bearhk.info/"+each.attrib['href']
    return urldir
#爬下所有文章的标题的URL地址    
def crawer():
    urldir={}
    for i in range(27):
        url="http://cc.bearhk.info/thread0806.php?fid=20&page="+str(i+1)
        print("=====================正在爬取第"+str(i+1)+"页=========")
        urldir=crawerEach(url,urldir)
        # if i%4==0:
        #     time.sleep(5)
    f=open("all.xml",'w',encoding="utf-8")
    for key,url in urldir.items():
        firstColumn="<article title="+"\""+key+"\">"
        secondColumn="   "+"<url>"+url+"</url>"
        thirdColumn="</article>"
        f.write(firstColumn+'\n'+secondColumn+'\n'+thirdColumn+'\n')
    f.close()
    
    
#以文章的标题模糊搜索
def search():
    keyword = input("请输入关键字：")
    file=open("all.xml",'r',encoding='utf-8')
    content=file.read()
    selector = etree.HTML(content)
    name = selector.xpath("//article[contains(@title,'%s')]/@title"%keyword)#要区分大小写 蛋疼
    url = selector.xpath("//article[contains(@title,'%s')]/url/text()"%keyword)
    for i in range(len(url)):
        print(name[i],url[i])


#获得文章内容
def getContent(html ,url, pageAccount):
    selector = etree.HTML(html)
    contents = selector.xpath('//div[@class="tpc_content do_not_catch"]/text()')
    tid = url[-12:-5]
    print (tid)
    #获得首页的文章内容
    for item in contents:
        writeContent(item)
        print(item)
        print("")
    pageInt = int(pageAccount)
    i = 2
    while i<=pageInt:
        pageUrl = "http://cc.bearhk.info/read.php?tid=" + tid + "&page=" + str(i)
        print(pageUrl)
        getAuthorFloorContent(pageUrl)
        i=i+1
        print(pageUrl)
#获得第2页以后的页面的作者的楼层中的内容
def getAuthorFloorContent(pageUrl):
    request = urllib.request.Request(pageUrl, headers = headers)
    resp=opener.open(request)
    html=resp.read().decode('gbk')
    selector = etree.HTML(html)
    contents = selector.xpath('//div[@class="tpc_content"]')
    for item in contents:
        if len(''.join(item.xpath('./text()')))>500:
            writeContent('\n'.join(item.xpath('./text()')))
            print(''.join(item.xpath('./text()')))
            print("")


#把内容写入文件
def writeContent(content):
    f=open('content1.txt','a',encoding='utf-8')
    f.write(content)
    f.write('\n')
    f.close()

#获得帖子中共有多少页
def getContentPage(html):
    selector = etree.HTML(html)
    lastpage = selector.xpath('//*[@id="last"]')[0].attrib['href']
    pageAccount = ''.join(list(filter(str.isdigit,lastpage[-5:])))
    print("页数为：" + pageAccount)
    return pageAccount

#获得文章
def getArtilcle(url):
    # url='http://cc.bearhk.info/htm_data/20/1509/1639779.html'
    request = urllib.request.Request(url, headers = headers)
    resp=opener.open(request)
    html=resp.read().decode('gbk')
    #取得帖子的页数
    account = getContentPage(html)
    #取得内容，并将内容存入txt
    content = getContent(html, url ,account)
    

#获得图片
def getPicture(url):
    url="http://cc.bearhk.info/htm_data/8/1412/1313643.html"
    page=url[-12:-5]
    request = urllib.request.Request(url, headers = headers)
    resp=opener.open(request)
    selector = etree.HTML(resp.read())
    contents = selector.xpath('//input[@type="image"]/@src')
    #获得网页内容
    i = 0
    for item in contents:
        print(item)
        request = urllib.request.Request(item, headers = headers)
        conn = opener.open(request)
        f=open(page+'-'+str(i)+".jpg",'wb')
        i += 1
        f.write(conn.read())
        f.close()


if __name__ == "__main__":
    print("1--更新")
    print("2--查询")
    print("3--取得文章")
    print("4--取得图片")
    choose=input("请输入结果：")
    if choose=="1":
        crawer()
    else :
        if choose=="3":
            url = input("请输入文章的网址:")
            getArtilcle(url)
        else:
            if choose=="4":
                url = input("请出入图片的网址:")
                getPicture(url)
            else:
                search()
    print("The End")

    
