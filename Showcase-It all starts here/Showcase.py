from os import system

system("scrapy crawl ndtv -t json -o Output.json")

system("scrapy crawl firstpost -t json -o Output.json")

system("scrapy crawl indiatoday -t json -o Output.json")

system("scrapy crawl indianexp -t json -o Output.json")

system("scrapy crawl gadgets360 -t json -o Output.json")

print("Crawled")

system("python3 PrepareJSON.py")

print("Prepared")

system("python3 Classify.py")

print("Done")