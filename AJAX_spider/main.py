#encoding:utf8
# 动态加载页面的抓取：腾讯视频最新短评

import re, requests, json

# main_url 是视频主页的 url，代码中并未用到，仅用于对照提取video_id
video_id = 'wi8e2p5kirdaf3j'
main_url = 'https://v.qq.com/x/cover/%s.html'%video_id
# comment_id_url 与 comment_url 的结构通过浏览器手动解析出来，没有出现在主页源码中
comment_id_url = 'https://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&cid=%s'%video_id
comment_url = 'https://coral.qq.com/article/%s/comment?commentid=0&reqnum=10' # 此处的 commentid=0 指的是第一条评论的id，
                                                                              # reqnum=10 指的是该页面加载10条评论
# comment_id_url的源代码中有目标网页comment_url 需要的关键参数comment_id
html = requests.get(comment_id_url).text
comment_id = re.search(r'"comment_id":"(.*?)"', html, re.S).group(1)
comment_url = comment_url%comment_id

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
html = requests.get(comment_url, headers=headers).text
jsdic = json.loads(html)
jsdata = jsdic['data']
comments = jsdata['commentid']
for each in comments:
    print '评论人：%s'%each['userinfo']['nick'].encode('utf8')
    print '内容：%s'%each['content'].encode('utf8')
    print '时间：%s\n'%each['timeDifference'].encode('utf8')
