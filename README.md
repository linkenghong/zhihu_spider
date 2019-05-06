# zhihu_spider 知乎爬虫
关于知乎的各种爬虫，目前打算一种爬虫一个程序，后期可以考虑结合成一个总的。
## 1. 专栏模块
### (1). zhihu\_spider\_column_img：知乎专栏下文章内图片爬取
**有些知乎专栏下的文章是以图片为主的，可以借助此程序下载专栏所有文章内的图片，只需修改main()中两处即可。**

程序是先将专栏内所有文章链接爬取下来，存在artList列表，再依次访问所有文章，并把其中的图片链接存在imgList列表中，然后再把imgList列表中的图片依次下载下来。

后期可以考虑一篇文章内的图片一起下载在一个文件夹，然后把文章的其他信息写在文件夹下的文档中。再后期可以考虑接入数据库。

爬取的主要问题如下：

* 专栏url

如果直接用专栏地址，如：https://zhuanlan.zhihu.com/maqianzu ，会发现直接爬的话，是查不到任何东西的。此时按F12键，点Network，然后把页面往下滑，会发现网页发起了个请求，其中一个以articles开头的会看到里面的Request URL如下：
```
https://zhuanlan.zhihu.com/api/columns/maqianzu/articles?include=data%5B%2A%5D.admin_closed_comment%2Ccomment_count%2Csuggest_edit%2Cis_title_image_full_screen%2Ccan_comment%2Cupvoted_followees%2Ccan_open_tipjar%2Ccan_tip%2Cvoteup_count%2Cvoting%2Ctopics%2Creview_info%2Cauthor.is_following%2Cis_labeled%2Clabel_info&limit=10&offset=10
```
这个才是我们真正需要的，后面的limit是每页显示文章数，offset是指从第几篇后起显示，上述url可简化成：
```
https://zhuanlan.zhihu.com/api/columns/maqianzu/articles?limit=10&offset=0
```

* 文章链接url

爬取上述专栏url后在其中可以找到文章一般在"url"与 "comment_permission"两个属性之间，所以用下列正则表达式来匹配。
> "url".{0,60}, "comment
