import csv
import requests
from bs4 import BeautifulSoup

url="https://movie.naver.com/movie/running/current.nhn"
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
movie_list = soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li ')


final_data=[]
for movie in movie_list:
    a_tag = movie.select_one('dl > dt > a')
    movie_code = a_tag['href'].split("code=")[1]
    movie_name = a_tag.contents[0]
    
    movie_data={
        "code" : movie_code,
        "name" : movie_name
    }
    final_data.append(movie_data)


for review in final_data:
    movie_code = review['code']

    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)
    soup = BeautifulSoup(response.text,"html.parser")
    review_list = soup.select("div.score_result > ul > li")
    # print(review_list)

    count=0

    for review in review_list:
        score = review.select_one('div.star_score > em ').text
        # reple=""

        # reple = review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} ').text.strip()
        if  review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count} '):
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count} > a ')['data-src']

        elif review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} '):
             reple = review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} ').text.strip()
        print(score,reple)

        count += 1
        

