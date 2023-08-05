# django_xz_queue

 - 一个django的app可以独立安装的结合django来用

### TODO

 - 单元测试和可持续集成测试
 - python3.6兼容 


### requirments

 -  需要安装阿里云mns [mns-sdk下载](https://help.aliyun.com/document_detail/32305.html?spm=5176.7739214.6.673.Ly76Et)

```
pip install git+https://github.com/AoAoStudio/aliyun-mns-sdk.git@master
```

 - install django-xz-queue

```
 pip install django-xz-queue

```

### 消费mns队列使用(requirements安装完毕后)

 > 具体可以通过test_django_xz_queue 看怎么使用 下面是简单使用步骤

 - aliyun创建队列 -> 'queuexz'
 - django settings 里配置

 ```
XZ_QUEUES = {
    'queuexz': {
        'QUEUE_TYPE': 'mns', # queue type msn-> aliyun
        'QUEUE_CONSUMER_MODULE': 'path.to.queuexz_consumer', # consumer module
        'QUEUE_CONNECTION': {  # queue save mns 的链接信息
            'ENDPOINT': ENDPOINT,
            'ACCID': ACCID,
            'ACCKEY': ACCKEY
        }
    }
}

 ```

  - python manage.py xzworker queuexz





