import json
import time
import datetime
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers, models
from .utils.webscraper import ESPNWebScraper


class GetLeagueStandings(APIView):
    serializers_class = serializers.ScrapeEndpointSerializer

    def get(self, request, format=None):
        """Get all Leagues"""
        try:
            leagues = models.League.objects.all().values()

            return Response({'data': list(leagues)})
        except Exception as exception:
            print(exception)
            return Response({'error': str(exception)})

    def post(self, request):
        """Scrape League Standings"""
        try:
            serializer = self.serializers_class(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                league, was_league_created = models.League.objects.get_or_create(
                    league_id=validated_data['league_id'])

                season, was_season_created = models.Season.objects.get_or_create(
                    league=league, year=2019)

                # League and Season exist
                if False and not was_league_created and not was_season_created:
                    # Return Database Data

                    returns_data = {
                        'data': season.standings,
                        'last_scrape': season.last_standings_scrape
                    }
                else:
                    # Scrape New Data
                    options = {
                        'league_id': str(league.league_id),
                        'username': validated_data['username'],
                        'password': validated_data['password'],
                        'headless': False
                    }
                    espn_scraper = ESPNWebScraper.ESPNWebScraper(
                        options)
                    standings = espn_scraper.getLeagueStandings()
                    espn_scraper.closeBrowser()

                    returns_data = {
                        'data': standings,
                        'last_scrape': 'now'
                    }
                return Response(returns_data)

            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as exception:
            print(exception)
            return Response({'error': str(exception)})


class GetDraftRecap(APIView):
    serializers_class = serializers.ScrapeEndpointSerializer

    def get(self, request, format=None):
        """DEVELOP ONLY - Get all Leagues"""
        try:
            leagues = models.League.objects.all().values()

            return Response({'data': list(leagues)})
        except Exception as exception:
            print(exception)
            return Response({'error': str(exception)})

    def post(self, request):
        """Scrape League Standings"""
        try:
            serializer = self.serializers_class(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                league, was_league_created = models.League.objects.get_or_create(
                    league_id=validated_data['league_id'])
                season, was_season_created = models.Season.objects.get_or_create(
                    league=league, year=2019)
                
                # League and Season exist
                if not validated_data['force_scrape'] and not was_league_created and not was_season_created:
                    # Return Database Data

                    returns_data = {
                        'data': season.draft_recap,
                        'last_scrape': season.last_draft_recap_scrape
                    }
                else:
                    # Scrape New Data
                    options = {
                        'league_id': str(league.league_id),
                        'headless': False
                    }

                    # Scrape Data
                    espn_scraper = ESPNWebScraper.ESPNWebScraper(
                        options)
                    draft_recap = espn_scraper.getDraftRecap()
                    espn_scraper.closeBrowser()

                    # Store in DB
                    season.draft_recap = draft_recap
                    season.last_draft_recap_scrape = datetime.datetime.now(
                        tz=timezone.utc)
                    season.save()

                    returns_data = {
                        'data': draft_recap,
                        'last_scrape': season.last_draft_recap_scrape
                    }
                return Response(returns_data)

            else:
                return Response(
                    {'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as exception:
            print(exception)
            return Response({'error': str(exception)})
