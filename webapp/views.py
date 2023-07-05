from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from webapp.data_handling.bikeshare import get_city, load_city_data
import json


class BikeShareDataAPIView(APIView):
    def get(self, request):
        # data = request.GET.get('name')
        days = request.GET.get('days').lower().split(',')
        months = request.GET.get('months').lower().split(',')
        city = request.GET.get('city').lower()
        print(city, months, days, sep=" - ")
        return Response(load_city_data(city))

    def post(self, request):
        print("message is", request.data['city name'])

        city = get_city(request.data["city name"])
        print(city)
        # load_city_data(city)
        return Response({"message": city})
