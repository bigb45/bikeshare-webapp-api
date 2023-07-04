from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from webapp.data_handling.bikeshare import get_city, load_city_data


class BikeShareDataAPIView(APIView):
    def get(self, request):
        data = {'message': "Hi mom"}
        return Response(data)

    def post(self, request):
        print("message is", request.data['city name'])

        city = get_city(request.data["city name"])
        print(city)
        # load_city_data(city)
        return Response({"message": city})
