from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from analysis.logic import SummaryReportProcessor

class SummaryReportView(APIView, SummaryReportProcessor):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(
                self.processSummary()
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)