from rest_framework.views import APIView
from rest_framework.response import Response
from webapp.data_handling.bikeshare import load_city_data


class BikeShareDataAPIView(APIView):
    def get(self, request):
        # data = request.GET.get('name')
        days = request.GET.get('days').lower().split(',')
        months = request.GET.get('months').lower().split(',')
        city = request.GET.get('city').lower()
        row_count = int(request.GET.get('count'))
        # direction = request.GET.get('direction') # sorting is now done on the front end
        # print(city, months, days, sep=" - ")
        return Response(load_city_data(city, months, days, row_count))

    def post(self, request):
        print("message is", request.data['city name'])

        # city = get_city(request.data["city name"])
        # print(city)
        # load_city_data(city)
        return Response({"message": request.data})
