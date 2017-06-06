from trawler import TrawlIt
import argparse


def main(kw, pages,browser):
    print "Gathering the information with keyword: [%s]:"%kw
    trawl = TrawlIt(kw=kw, generate_kws=False,  max_pages=int(pages), browser=browser)
    trawl.run()
    data = trawl.data
    print data
    print "Found: [%s] results %s" %len(data)
    trawl.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-kw', '--keyword', help='Input keyword to search (ex: python)')
    parser.add_argument('-p', '--pages', help='Number of pages)')
    parser.add_argument('-b', '--browser', help='Browser options (only bing and stackoverflow)')

    arguments = parser.parse_args()
    main(arguments.keyword, arguments.pages, arguments.browser)