from scrapy import cmdline

name = 'meizitu'
cmd = 'scrapy crawl %s' % name

cmdline.execute(cmd.split())
