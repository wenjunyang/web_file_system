#!/usr/bin/env python
import web
import os
import time
import config
from urllib import quote

# load config file
root = config.root

types = [
    ".h",".cpp",".cxx",".cc",".c",".cs",".html",".js",
    ".php",".java",".py",".rb",".as",".jpeg",".jpg",".png",
    ".gif",".ai",".psd",".mp3",".avi",".rmvb",".mp4",".wmv",
    ".mkv",".doc",".docx",".ppt",".pptx",".xls",".xlsx",
    ".zip",".tar",".gz",".7z",".rar",".pdf",".txt",".exe",
    ".apk","dir"
]


class Ico:
    def GET(self):
        return open("static/img/favicon.ico").read()


class Index:
    def __init__(self):
        self.render = web.template.render('template')

    def process_dir(self, request_dir):
        web.header('Content-Type', 'text/html;charset=utf-8')
        list = []
        absolute_dir = os.path.join(root, request_dir)
        items = sorted(os.listdir(absolute_dir), key=unicode.lower)
        for item in items:
            absolute_path = os.path.join(absolute_dir, item)
            temp = {"name": '/' + item}
            if os.path.isdir(absolute_path):
                temp['type'] = 'dir'
            else:
                temp["type"] = '.' + item.split('.')[-1]
            try:
                types.index(temp['type'])
            except:
                temp['type'] = "general"

            temp["time"] = time.strftime("%H:%M:%S %Y-%m-%d",
                time.localtime(os.path.getmtime(absolute_path)))

            size = os.path.getsize(absolute_path)
            if size < 1024:
                size = str(size) + ".0 B"
            elif size < 1024 * 1024:
                size = "%0.1f KB" % (size/1024.0)
            elif size < 1024 * 1024 * 1024:
                size = "%0.1f MB" % (size/1024.0/1024.0)
            else :
                size = "%0.1f GB" % (size/1024.0/1024.0/1024.0)

            temp["size"] = size
            temp["encode"] = quote(os.path.join(request_dir, item))

            list.append(temp)

        return self.render.layout(list)

    def process_file(self, request_file):
        web.header('Content-Type', 'text/plain;charset=utf-8')
        with open(os.path.join(root, request_file)) as target:
            return target.read()

    def GET(self, path):
        file_path = os.path.join(root, path)
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                return self.process_dir(path)
            else:
                return self.process_file(path)
        else:
            return "bad request"
            
    def DELETE(self, filename):
        try:
            filename = filename.encode('utf-8')
            os.remove(os.path.join(root, filename))
        except:
            return "success"


if __name__ == "__main__":
    urls = (
        '/favicon.ico', "Ico",
        '/(.*)', 'Index',
    )
    app = web.application(urls, globals())
    application = app.wsgifunc()
    app.run()