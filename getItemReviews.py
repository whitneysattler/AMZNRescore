from bs4 import BeautifulSoup
import requests
import re
import time

def printCsv(data):
    csv="user|||userURI|||reviewText|||stars|||postDate|||productText\n"
    for review in data:
        csv+=review["user"]+"|||"+review["userURI"]+"|||"+review["reviewText"]+"|||"+review["stars"]+"|||"+review["postDate"]+"|||"+review["productText"]+"\n"
    print(csv)


def requestItemReviews(url,verbose):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    reviewList = []
    reviews = soup.find_all(attrs={'id': re.compile(r".*customer_review-.*")})
    productText = soup.find(attrs={'class':"a-link-normal",'data-hook':"product-link"}).text

    for review in reviews:
        reviewSoup = BeautifulSoup(str(review),'html.parser')
        author = reviewSoup.find(attrs={'class':"a-size-base a-link-normal author"})
        reviewText = reviewSoup.find(attrs={'class':"a-size-base review-text"})
        stars = reviewSoup.find(attrs={'class': "a-icon-alt"}).text[:1]
        postDate = reviewSoup.find(attrs={'class': "a-size-base a-color-secondary review-date"}).text[3:]
        if verbose:
            print("\n#####################\n",author.text,"\n",author['href'],"\n",reviewText.text,"\n###################\n")
        reviewList.append({"user":author.text,\
                           "userURI":author['href'].split(".")[2].split("/")[0],\
                           "reviewText":reviewText.text,\
                           "stars":stars,\
                           "postDate":postDate,\
                           "productText":productText})
    return reviewList

def gatherData(verbose):
    firstRun=1
    pagesExist=1
    count = 2
    itemReviews = []
    while(pagesExist):
        time.sleep(2)
        if not(firstRun):
            print("Scraping Page: "+str(count))
            data = requestItemReviews(url + pageIterationTag + str(count), verbose)
            if len(data) == 0:
                pagesExist = 0
                print("done")
            count+=1
            for item in data:
                itemReviews.append(item)
        else:
            data = requestItemReviews(url, verbose)
            for item in data:
                itemReviews.append(item)
            firstRun=0
    return itemReviews

url='https://www.amazon.com/William-Painter-Titanium-Polarized-Sunglasses/product-reviews/B01AH0PVMO/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
pageIterationTag = "&pageNumber="
verbose = 0
data = gatherData(verbose)
print(data)
#printCsv(data)
