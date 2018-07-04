from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import *

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields =('id','username')

class QuestionSerializer(serializers.ModelSerializer):
        class Meta:
            model=Question
            fields ='__all__'

class CompanySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
            model=Company
            fields = '__all__'

class ClustersSerializer(serializers.ModelSerializer):
   company= CompanySerializer(read_only=True)
   class Meta:
            model=Clusters
            fields = '__all__'

class QuestionsWeightsSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    cluster = ClustersSerializer(read_only=True)
    class Meta:
        model = Questions_weights
        fields = '__all__'


class InterviweSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = '__all__'


class SubmissionsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    interviewer = CompanySerializer(read_only=True)
    class Meta:
        model = Submissions
        fields = '__all__'


#'''
#class ArtistSerializer(serializers.ModelSerializer):
#        class Meta:
#            model=Artist
#            fields = '__all__'
#
#
#class AlbumSerializer(serializers.ModelSerializer):
#        class Meta:
#            model=Album
#            fields = '__all__'
#
#            '''
#

        