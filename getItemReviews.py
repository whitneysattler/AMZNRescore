##########################
#Author: NB. 3/29/18 - 11:55
##########################

from bs4 import BeautifulSoup
import requests
import re
import time

def requestItemReviews(url,verbose):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    reviewList = []
    reviews = soup.find_all(attrs={'id': re.compile(r".*customer_review-.*")})

    for review in reviews:
        reviewSoup = BeautifulSoup(str(review),'html.parser')
        author = reviewSoup.find(attrs={'class':"a-size-base a-link-normal author"})
        reviewText = reviewSoup.find(attrs={'class':"a-size-base review-text"})
        if verbose:
            print("\n#####################\n",author.text,"\n",author['href'],"\n",reviewText.text,"\n###################\n")
        reviewList.append({"user":author.text, "userURI":author['href'], "reviewText":reviewText.text})
    return reviewList

def gatherData(verbose):
    firstRun=1
    pagesExist=1
    count = 2
    itemReviews = []
    while(pagesExist):
        time.sleep(2)
        if not(firstRun):
            print(count)
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
print(gatherData(verbose))
