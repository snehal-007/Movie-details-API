from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blog.serializers import CategorySerializer ,PostSerializer ,UserSerializer
from blog.models import MovieCategory ,MoviePost
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly 
from rest_framework.filters import OrderingFilter ,SearchFilter
import requests
from bs4 import BeautifulSoup
from .models import MoviePost
from rest_framework.pagination import LimitOffsetPagination ,PageNumberPagination
from rest_framework.reverse import reverse
from rest_framework.response import Response



# Data Store in Database functions

# Get Request
def getData(url):
    r = requests.get(url)
    return r.text

# Fetch a Movie Data in Database
def movies_collect(requests):
    try:

        # data fetch from website
        data = getData('https://www.imdb.com/chart/top?ref_=nv_mv_250')

        soup = BeautifulSoup(data,'html.parser')

        # Store Html Data in List
        # title list
        title = []
        res=[]

        # rating list
        rating = []

        #release year list
        release_year = []



        # Fetch all movie title
        for item in soup.find_all("table",class_="chart full-width"):
            # print(item)
            for td in item.find_all("tr"):
                for a in td.find_all("a"):
                    # print(a.get_text())
                    if a != "\n":
                        title.append(a.get_text())

        # print(title)

        # title in list
        for i in title:
            if i not in res:
                res.append(i)

        # print(res[1:])

        # final title
        final_title = res[1:]


        #  Fetch all movie rating
        for item in soup.find_all("table",class_="chart full-width"):
            # print(item)
            for td in item.find_all("tr"):
                for strong in td.find_all("strong"):
                    # print(strong.get_text())
                    if strong != "\n":
                        rating.append(strong.get_text())

        # print(rating)  


        #  Fetch all movie Release year
        for item in soup.find_all("table",class_="chart full-width"):
            # print(item)
            for td in item.find_all("tr"):
                for span in td.find_all("span",class_="secondaryInfo"):
                    #print(span.get_text())
                    release_year.append(span.get_text())


        # print(release_year)
        # print("final Title",len(final_title))


        # data store in database
        for item in range (len(final_title)):
            # print(item)
            # movies[f"Movies:-{item}"] = {"title":final_title[item],"rating":rating[item],"release year":release_year[item]}

            movie_title = final_title[item]
            #print(movie_title)

            movie_rating = rating[item]
            # print(movie_rating)

            movie_year = release_year[item]
            # print(movie_year)


            # Alert it is only for use to save data in database so it is hardCode 
            # database write in sqlite3

            # details_save = MoviePost(title=movie_title,rating=movie_rating,release_year=movie_year)
            # details_save.save()

    except Exception as e:
        return HttpResponse("Network Error")

    return HttpResponse("Data Has Been Collected Successfully")


# Pagination
class PersonViewPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 5

# movie Details in Rest API
class PostList(generics.ListCreateAPIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PersonViewPagination
    queryset = MoviePost.objects.all()
    serializer_class = PostSerializer
    filter_backends = (OrderingFilter,SearchFilter)
    ordering_fields = ('rating','title')
    search_fields = ('title','id')
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly] 
    queryset = MoviePost.objects.all()
    serializer_class = PostSerializer   

# user details
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # permission_classes = [IsAdminUser]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# hyperlinks provide in Root Page
class ApiRoot(APIView):
    def get(self,request,format=None):
        return Response({
        'posts': reverse('posts', request=request, format=format)
    })