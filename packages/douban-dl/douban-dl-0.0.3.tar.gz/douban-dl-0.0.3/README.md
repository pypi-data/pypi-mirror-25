douban downloader
=======================

A simple python script to download douban albums and celebrity


Introduction
-----

目前支持的下载类型

1. 豆瓣相册，比如

        douban-dl https://www.douban.com/photos/album/1641641224/

2. 影人相册图片

        douban-dl https://movie.douban.com/celebrity/1335340/
        douban-dl https://movie.douban.com/celebrity/1335340/photos
    
3. 用户所有相册

        douban-dl https://www.douban.com/people/einverne/
    

Installation
------------

    $ pip install douban-dl


Usage
-----

    $ douban-dl url [path]

`url` should be like this:

    https://www.douban.com/photos/album/<album_id>
    https://movie.douban.com/celebrity/<celebrity_id>
    https://www.douban.com/people/<douban_id>/photos

`path` is the folder where images saved, defaults to `./douban`.

License
-------

MIT


Contribute
----------

Feel free to file an issue, or make a pr.
