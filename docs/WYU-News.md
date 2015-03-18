校园新闻
------

### 获得新闻列表

**example**

```python
from service.wyunews import WyuNews
import json
if __name__ == '__main__':
    wyunews = WyuNews()
    print (json.dumps(wyunews.get_wyu_news(1)))
```

**Response**

```json
[
    {
        "url": "http://www.wyu.cn/news/news_zxtz/201531811280913123.htm", //新闻详情链接
        "from": "团委", //来源
        "type": "最新通知", //类型
        "posttime": "2015-3-18 11:28:09", //发布时间
        "title": "关于组织开展2015年清明扫墓活动的通知 " //标题
    },
    ......

]

```

### 查看新闻详情


**example**

```python
from service.wyunews import WyuNews
import json
if __name__ == '__main__':
    wyunews = WyuNews()
    print wyunews.get_news_content('http://www.wyu.cn/news/news_xnxw/20153181021141118.htm')
```

**Response**

内容部分的html代码

```html
<tr>
<td class="p2" colspan="2" id="zoom"><p align="left"><font style="FONT-SIZE: 16px; FONT-FAMILY: 宋体">    3月17日下午，学生学业指导中心邀请了应用物理与材料学院王忆教授在北主楼201室举行大学物理学习指导讲座。</font></p>
<p align="left"><font style="FONT-SIZE: 16px; FONT-FAMILY: 宋体">    王忆教授引用名人名言进入讲座主题――怎样才能学好大学物理这门课。他主要从学习大学物理课程的目的，对专业学习有多大的支撑作用，学习方法和要点，大学物理的学习与综合素质提高相结合，大学物理学习与原始创新能力培养的关系以及如何学好其他专业基础课六方面为同学们进行了学习指导。通过结合大学物理在高铁、航空、化纤、通讯等高端领域中广泛应用，王忆教授深入浅出地讲解了大学物理课程的重要性，对提高同学们的学习兴趣起到了积极的作用。</font></p>
<p align="left"><font style="FONT-SIZE: 16px; FONT-FAMILY: 宋体">    讲座在一片轻松愉快的氛围以及与同学们热烈互动中圆满完成。（文/图 学生学业指导中心）</font></p>
<p align="left"><img src="http://www.wyu.cn/news/UploadFiles/2015031837149185.JPG" style="HEIGHT: 504px; TEXT-ALIGN: center; MARGIN: 4px auto; DISPLAY: block; WIDTH: 760px"/></p>
<p align="left"> </p></td>
</tr>
```

