from rest_framework import viewsets, status
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny, ]

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk):
        if 'stars' in request.data:
            movie = Movie.objects.get(pk=pk)
            stars = request.data['stars']
            user = User.objects.get(id=1)
            try:
                rating = Rating.objects.get(user=user, movie=movie)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Updated', 'result': serializer}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Created', 'result': serializer}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'We need to provide'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication, ]
