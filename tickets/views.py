from urllib import request
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest,Movie,Reservation ,Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,filters
from .serializers import GusetSerializers ,MovieSerializer,ReservationSerializers,PostSerializer
from rest_framework.views import APIView
from django.http import Http404 
from rest_framework import generics,mixins,viewsets

from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrRedOnly
# Create your views here.

#1 without rest and no model query

def no_rest_no_model(requst):
    gestes=[
        {
            "id":1,
            "name":"ahmed",
            "mobile":7121593,
        },
        {
            "id":2,
            "name":"omer",
            "mobile":96581,
        }
        
    ]
    return JsonResponse (gestes,safe=False)

#2 model data default django without rest
def no_rest_from_model(request):
    data=Guest.objects.all()
    response={
        'gests':list(data.values('name','mobile'))
    }
    return JsonResponse(response)

# list == GET
# create == POST
# pk query == GET
# update == PUT
# delete destroy == DELETE

#3 function based views
#3.1 GET POST  
@api_view(['GET','POST'])
def FBV_List(request):
    # GET
    if request.method=='GET':
        gestes =Guest.objects.all()
        serializer=GusetSerializers(gestes,many=True)
        return Response(serializer.data)
    # POST
    elif request.method=='POST':
        serializer=GusetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data
                            ,status=status.HTTP_201_CREATED)  
        return Response(serializer.data,status.HTTP_400_BAD_REQUEST)   

#3.2 GET PUT DELETE  

@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        gestes=Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    

    # GET
    if request.method=='GET':
        serializer=GusetSerializers(gestes)
        return Response(serializer.data)
    # PUT
    elif request.method=='PUT':
        serializer=GusetSerializers(gestes,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    # DELETE
    if request.method=='DELETE':
        gestes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
# CBV CLASS based views
#4.1 list and creat == GET & POST

class CBV_list(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GusetSerializers(guests,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer= GusetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )
            
#4.2   get put delete class based vies pk
class CBV_pk(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GusetSerializers(guest)
        return Response(serializer.data)
    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer=GusetSerializers(guest,data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
# 5 Mixins
#5.1 mixins list 

class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class= GusetSerializers
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
#5.2 mixins get put delete
class Mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GusetSerializers
    def get(self,request,pk):
        return  self.retrieve(request)
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)

#6 generics
#6.1 get & post
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GusetSerializers
    
    authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    
#6.2 get & put & delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GusetSerializers
    
    authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    
# 7 Viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GusetSerializers

class viewsets_move(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backend=[filters.SearchFilter]
    search_fields=['movie']
    
class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializers   
             
#8 find movie
@api_view(['GET'])
def find_movie(request):
    movies=Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie']
    )
    serializer=MovieSerializer(movies,many=True)
    return Response(serializer.data)
 
#9 creat new reservation
@api_view(['POST'])
def new_reservation(request):
    move=Movie.objects.get(
       hall=request.data['hall'],
        movie=request.data['movie'] 
    )
    guest=Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()
    
    reservation=Reservation()
    reservation.gust=guest
    reservation.movie=move
    reservation.save()
    
    serializer = ReservationSerializers(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
            
      
      
#10   post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthorOrRedOnly]
    queryset=Post.objects.all()
    serializer_class=PostSerializer
 
            