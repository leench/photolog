photolog
========

第一个阶段暂时完成了，基本上实现了网站的功能。

- 通过使用ftp或其他方式上传原始文件到指定的目录，向服务器发出指令对照片进行处理：保存EXIF信息，并提取出拍摄时间，对照片进行归档。因为原始照片占用空间太大，所以将照片的尺寸调整到了长边1200，质量100。使用了Django的[StreamingHttpResponse](https://docs.djangoproject.com/en/1.6/ref/request-response/#streaminghttpresponse-objects "streaminghttpresponse-objects")做实时的显示到显示器上。在nginx上加了这个参数才能够正确的显示：

	response['X-Accel-Buffering'] = 'no'

- 存储方面使用了[七牛云存储](http://www.qiniu.com/ "七牛")的镜像。因为第一次使用，所以完全保存在他那边还不是那么放心，先看看流量情况再说。加速作用到是非常明显。始终服务器没有在国内。
七牛的镜像似乎要删除了空间里的文件之后，通过在静态文件上加版本参数才能更新（没有做太多测试）。解决方法是在服务器端通过signal检测到保存文件或者生成thumbnail的时候去删除七牛空间里的key。没有去做验证key是否存在的情况，没有什么必要。然后在通过加版本参数来强制CDN刷新缓存。[http://kb.qiniu.com/Qiniu-Cloud-Storage-Cache-Strategy](http://kb.qiniu.com/Qiniu-Cloud-Storage-Cache-Strategy "七牛云存储缓存机制")

- 最后使用了Bootstrap库，前台开发会相对轻松一点，移动设备的兼容还是需要自己来动手。

### 用到的东西：
- [Django](https://www.djangoproject.com "Django")
- [Grappelli](https://github.com/sehmaschine/django-grappelli "django-grappelli")
- [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails "easy-thumbnails")
- [django-endless-pagination](https://github.com/frankban/django-endless-pagination "django-endless-pagination")
- [django-threadedcomments](https://github.com/HonzaKral/django-threadedcomments "django-threadedcomments")
- [django-taggit](https://github.com/alex/django-taggit "django-taggit")
- [Bootstrap](http://getbootstrap.com/ "Bootstrap")
- CDN/存储： [七牛云存储](http://www.qiniu.com "七牛云存储") [通过我的邀请注册](https://portal.qiniu.com/signup?code=3ld1t7xu8r1w2 "注册")
- VPS：[DigitalOcean](https://www.digitalocean.com/ "DigitalOcean") [通过我的邀请注册](https://www.digitalocean.com/?refcode=3fcc67aec829 "通过我的邀请注册")

代码：[https://github.com/leench/photolog](https://github.com/leench/photolog "https://github.com/leench/photolog")
