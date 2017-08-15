#coding=utf-8

'''
Created on 2017年8月12日

@author: Administrator
'''


class HtmlOutputter(object):
    def __init__(self):
        self.data = []
    
    def collect_data(self, data):
        if data == None:
            return
        self.data.append(data)

    
    def output_html(self):
        fout = open('output.html', 'w')
        
        fout.write('<html>')
        #添加如下这句html代码让浏览器知道要什么编码显示
        fout.write("<meta charset=\"utf-8\">")
        fout.write('<body>')
        fout.write('<table>')
        
        for d in self.data:
            fout.write('<tr>')
            fout.write('<td>%s</td>' %d['url'])
            fout.write('<td>%s</td>' %d['title'].encode('utf-8'))
            fout.write('<td>%s</td>' %d['summary'].encode('utf-8'))
            fout.write('</tr>')
        
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        
        fout.close()
    
    
    
    



