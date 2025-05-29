from datetime import datetime
from io import BytesIO
from .models import Authority, CTFQuestionPort
import requests
import json
import arabic_reshaper
from rest_framework.permissions import IsAuthenticated

import pandas as pd
from bidi.algorithm import get_display
from django.http import HttpResponse
from pytz import timezone, UTC
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from rest_framework import generics, filters
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import exceptions

from contestant import models
from contestant import serializers
from .models import TeamEscapeRoomQuestion
from .serializers import TeamEscapeRoomQuestionReportSerializer, CTFQuestionPortSerializer
import os
from django.conf import settings
from django.shortcuts import render

font_path = os.path.join(settings.BASE_DIR, "uploads", "bahij-nazanin.ttf")
pdfmetrics.registerFont(TTFont("BahijNazanin", font_path))


class TeamListAPIView(generics.ListAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name', 'score', 'coin', 'status'
    ]
    ordering_fields = [
        'name', 'score', 'coin', 'status'
    ]


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class TeamUpdateNameAPIView(generics.UpdateAPIView):
    serializer_class = serializers.TeamUpdateNameSerializer

    def get_object(self):
        try:
            return models.Team.objects.get(id=self.request.user.team.id)
        except models.Team.DoesNotExist:
            raise exceptions.TeamDoesntExist()


class TeamMemberListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        return models.TeamMember.objects.filter(team=self.request.user.team)

    serializer_class = serializers.TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'team__name',
        'name',
        'university_entry_year',
        'phone_number',
        'student_number',
        'email',
    ]

    ordering_fields = [
        'team__name',
        'name',
        'university_entry_year',
        'phone_number',
        'student_number',
        'email',
    ]


def leaderboard(request):
    return render(request, "staff/teams.html")


class TeamMemberDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TeamMember.objects.all()
    serializer_class = serializers.TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class EscapeRoomQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionListCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
        'description',
        'floor',
        'x_coordinate',
        'y_coordinate',
        'score',
        'answer_limitation',
        'flag',
        'coin',
        'creator',
        'created_at',
    ]


class EscapeRoomQuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionListCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class EscapeRoomQuestionForContestantsListAPIView(generics.ListAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionForContestantsListSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
        'description',
        'score',
        'coin',
    ]


class CTFQuestionListAPIView(generics.ListAPIView):
    serializer_class = serializers.CTFQuestionListCreateSerializer
    queryset = models.CTFQuestion.objects.filter(is_shown=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name', 'description', 'type', 'topic', 'file', 'is_shown',
        'created_at'
    ]
    ordering_fields = [
        'name', 'type', 'topic', 'file', 'is_shown',
        'creator', 'created_at'
    ]


class CTFQuestionListCreateForStaffAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CTFQuestionListCreateSerializer
    queryset = models.CTFQuestion.objects.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name', 'description', 'type', 'topic', 'file', 'is_shown',
        'created_at'
    ]
    ordering_fields = [
        'name', 'type', 'topic', 'file', 'is_shown',
        'creator', 'created_at'
    ]


class CTFQuestionDetailForStaffAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CTFQuestion.objects.all()
    serializer_class = serializers.CTFQuestionDetailForStaffSerializer
    permission_classes = [permissions.IsAdminUser]


class CTFQuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = models.CTFQuestion.objects.all()
    serializer_class = serializers.CTFQuestionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CTFFlagsListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.CTFFlags.objects.all()
    serializer_class = serializers.CTFFlagsSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'ctf_question__name',
        'flag',
        'hint',
    ]

    ordering_fields = [
        'ctf_question__name',
        'flag',
        'hint',
        'score',
        'coin',
        'created_at',
    ]


class CTFFlagsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CTFFlags.objects.all()
    serializer_class = serializers.CTFFlagsSerializer
    permission_classes = [permissions.IsAdminUser]


class TeamEscapeRoomQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.TeamEscapeRoomQuestion.objects.all()
    serializer_class = serializers.TeamEscapeRoomQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'team__name',
        'escape_room_question__name',
    ]

    ordering_fields = [
        'team__name',
        'escape_room_question__name',
        'created_at'
    ]

    def create(self, request, *args, **kwargs):
        raise exceptions.AnswerSubmissionEnded()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({
            "message": "پاسخ شما صحیح میباشد.",
            "instance": self.get_serializer(instance).data
        }, status=status.HTTP_201_CREATED)


class TeamEscapeRoomQuestionReport(APIView):
    def get(self, request, output_format=None):
        export_format = request.GET.get("output_format", "json")
        queryset = TeamEscapeRoomQuestion.objects.all().order_by("-created_at")
        serializer = TeamEscapeRoomQuestionReportSerializer(
            queryset, many=True)

        tehran_tz = timezone("Asia/Tehran")

        data = [
            {
                "id": item["id"],
                "team_name": item["team"]["name"],
                "escape_room_question_name": item["escape_room_question"]["name"],
                "created_at": self.convert_to_tehran_time(item["created_at"], tehran_tz),
            }
            for item in serializer.data
        ]

        if export_format == "excel":
            return self.export_to_excel(data)
        elif export_format == "pdf":
            return self.export_to_pdf(data)
        else:
            return Response(data, status=status.HTTP_200_OK)

    def convert_to_tehran_time(self, created_at, tehran_tz):
        """
        Converts a datetime object to Tehran time (HH:MM:SS) format.
        Handles both naive and timezone-aware datetime objects.
        """
        if isinstance(created_at, str):
            created_at = datetime.strptime(
                created_at[:-1], "%Y-%m-%dT%H:%M:%S.%f")
            created_at = created_at.replace(tzinfo=UTC)

        if created_at.tzinfo is None:
            created_at = tehran_tz.localize(created_at)
        else:
            created_at = created_at.astimezone(tehran_tz)

        return created_at.strftime("%H:%M:%S")

    def export_to_excel(self, data):
        df = pd.DataFrame(data)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Escape Room Questions", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Escape Room Questions"]
        worksheet.set_column("A:D", 20, None, {"font": "Arial Unicode MS"})
        writer.close()
        output.seek(0)

        response = HttpResponse(output,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="team_escape_room_questions.xlsx"'
        return response

    def export_to_pdf(self, data):
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        elements = []

        pdfmetrics.registerFont(
            TTFont("BahijNazanin", r"D:\Downloads\bahij-nazanin.ttf"))

        title_style = ParagraphStyle(
            "TitleStyle",
            fontName="BahijNazanin",
            fontSize=16,  # Keep the title font large
            spaceAfter=10,
            alignment=1  # Center-align the title
        )

        header_style = ParagraphStyle(
            "HeaderStyle",
            fontName="BahijNazanin",
            fontSize=14,
            spaceAfter=5,
            alignment=1
        )

        cell_style = ParagraphStyle(
            "CellStyle",
            fontName="BahijNazanin",
            fontSize=12,
            spaceAfter=5,
            alignment=1
        )

        title = Paragraph("Escape Room Questions Report", title_style)
        elements.append(title)

        table_data = [[
            Paragraph("ID", header_style),
            Paragraph("Team Name", header_style),
            Paragraph("Question", header_style),
            Paragraph("Time (Tehran)", header_style)
        ]]

        for item in data:
            team_name = self.fix_persian_text(item["team_name"])
            question_name = self.fix_persian_text(
                item["escape_room_question_name"])
            created_at = item["created_at"]

            table_data.append([
                Paragraph(str(item["id"]), cell_style),
                Paragraph(team_name, cell_style),
                Paragraph(question_name, cell_style),
                Paragraph(created_at, cell_style),
            ])

        table = Table(table_data, colWidths=[50, 150, 200, 100])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "BahijNazanin"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),  # Larger font size for header
            # Normal font size for other rows
            ("FONTSIZE", (0, 1), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgreen),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        output.seek(0)
        response = HttpResponse(output, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="team_escape_room_questions.pdf"'
        return response

    def fix_persian_text(self, text):
        """
        Fix Persian text by reshaping it and handling RTL/LTR issues.
        """
        if self.is_persian(text):
            reshaped_text = arabic_reshaper.reshape(
                text)  # Fix letter connections
            return get_display(reshaped_text)  # Fix direction (RTL)
        return text

    def is_persian(self, text):
        """
        Checks if the provided text contains Persian characters.
        """
        return any('\u0600' <= char <= '\u06FF' for char in text)


class TeamCTFFlagReport(APIView):
    def get(self, request, output_format=None):
        export_format = request.GET.get("output_format", "json")
        queryset = models.TeamCTFFlag.objects.all().order_by("-created_at")
        serializer = serializers.TeamCTFFlagSerializer(queryset, many=True)

        tehran_tz = timezone("Asia/Tehran")

        data = [
            {
                "id": item["id"],
                "team_name": item["team"]["name"],  # Team's name
                # The flag's name (from flag field)
                "flag_name": item["flag"]["flag"],
                # The CTF question's name
                "ctf_question_name": item["flag"]["ctf_question"]["name"],
                "created_at": self.convert_to_tehran_time(item["created_at"], tehran_tz),
            }
            for item in serializer.data
        ]

        if export_format == "excel":
            return self.export_to_excel(data)
        elif export_format == "pdf":
            return self.export_to_pdf(data)
        else:
            return Response(data, status=status.HTTP_200_OK)

    def convert_to_tehran_time(self, created_at, tehran_tz):
        """
        Converts a datetime object to Tehran time (HH:MM:SS) format.
        Handles both naive and timezone-aware datetime objects.
        """
        if isinstance(created_at, str):
            created_at = datetime.strptime(
                created_at[:-1], "%Y-%m-%dT%H:%M:%S.%f")
            created_at = created_at.replace(tzinfo=UTC)

        if created_at.tzinfo is None:
            created_at = tehran_tz.localize(created_at)
        else:
            created_at = created_at.astimezone(tehran_tz)

        return created_at.strftime("%H:%M:%S")

    def export_to_excel(self, data):
        df = pd.DataFrame(data)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="CTF Flags", index=False)

        workbook = writer.book
        worksheet = writer.sheets["CTF Flags"]
        worksheet.set_column("A:D", 20, None, {"font": "Arial Unicode MS"})
        writer.close()
        output.seek(0)

        response = HttpResponse(output,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="team_ctf_flags.xlsx"'
        return response

    def export_to_pdf(self, data):
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        elements = []

        pdfmetrics.registerFont(
            TTFont("BahijNazanin", r"D:\Downloads\bahij-nazanin.ttf"))

        title_style = ParagraphStyle(
            "TitleStyle",
            fontName="BahijNazanin",
            fontSize=16,
            spaceAfter=10,
            alignment=1
        )

        header_style = ParagraphStyle(
            "HeaderStyle",
            fontName="BahijNazanin",
            fontSize=14,
            spaceAfter=5,
            alignment=1
        )

        cell_style = ParagraphStyle(
            "CellStyle",
            fontName="BahijNazanin",
            fontSize=12,
            spaceAfter=5,
            alignment=1
        )

        title = Paragraph("CTF Flags Report", title_style)
        elements.append(title)

        table_data = [[
            Paragraph("ID", header_style),
            Paragraph("Team Name", header_style),
            Paragraph("Flag", header_style),
            Paragraph("CTF Question", header_style),
            Paragraph("Time (Tehran)", header_style)
        ]]

        for item in data:
            team_name = self.fix_persian_text(item["team_name"])
            flag_name = self.fix_persian_text(item["flag_name"])
            ctf_question_name = self.fix_persian_text(
                item["ctf_question_name"])
            created_at = item["created_at"]

            table_data.append([
                Paragraph(str(item["id"]), cell_style),
                Paragraph(team_name, cell_style),
                Paragraph(flag_name, cell_style),
                Paragraph(ctf_question_name, cell_style),
                Paragraph(created_at, cell_style),
            ])

        table = Table(table_data, colWidths=[50, 150, 150, 150, 100])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "BahijNazanin"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("FONTSIZE", (0, 1), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgreen),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        output.seek(0)
        response = HttpResponse(output, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="team_ctf_flags.pdf"'
        return response

    def fix_persian_text(self, text):
        """
        Fix Persian text by reshaping it and handling RTL/LTR issues.
        """
        if self.is_persian(text):
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        return text

    def is_persian(self, text):
        """
        Checks if the provided text contains Persian characters.
        """
        return any('\u0600' <= char <= '\u06FF' for char in text)


class TeamsReport(APIView):
    def get(self, request, output_format=None):
        export_format = request.GET.get("output_format", "json")
        queryset = models.Team.objects.all().order_by("-score")
        serializer = serializers.TeamSerializer(queryset, many=True)

        data = serializer.data

        if export_format == "excel":
            return self.export_to_excel(data)
        elif export_format == "pdf":
            return self.export_to_pdf(data)
        else:
            return Response(data, status=status.HTTP_200_OK)

    def export_to_excel(self, data):
        df = pd.DataFrame(data)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Teams", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Teams"]
        worksheet.set_column("A:D", 20, None, {"font": "Arial Unicode MS"})
        writer.close()
        output.seek(0)

        response = HttpResponse(output,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="teams.xlsx"'
        return response

    def export_to_pdf(self, data):
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        elements = []

        pdfmetrics.registerFont(
            TTFont("BahijNazanin", r"D:\Downloads\bahij-nazanin.ttf"))

        title_style = ParagraphStyle(
            "TitleStyle", fontName="BahijNazanin", fontSize=16, spaceAfter=10, alignment=1)
        header_style = ParagraphStyle(
            "HeaderStyle", fontName="BahijNazanin", fontSize=14, spaceAfter=5, alignment=1)
        cell_style = ParagraphStyle(
            "CellStyle", fontName="BahijNazanin", fontSize=12, spaceAfter=5, alignment=1)

        title = Paragraph("Teams Report", title_style)
        elements.append(title)

        table_data = [
            [Paragraph("ID", header_style), Paragraph("Team Name", header_style), Paragraph("Score", header_style),
             Paragraph("Coins", header_style), Paragraph("Status", header_style)]]

        for item in data:
            table_data.append([
                Paragraph(str(item["id"]), cell_style),
                Paragraph(self.fix_persian_text(item["name"]), cell_style),
                Paragraph(str(item["score"]), cell_style),
                Paragraph(str(item["coin"]), cell_style),
                Paragraph(item["status"], cell_style),
            ])

        table = Table(table_data, colWidths=[50, 150, 100, 100, 100])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "BahijNazanin"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("FONTSIZE", (0, 1), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgreen),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        output.seek(0)
        response = HttpResponse(output, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="teams.pdf"'
        return response

    def fix_persian_text(self, text):
        if self.is_persian(text):
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        return text

    def is_persian(self, text):
        return any('\u0600' <= char <= '\u06FF' for char in text)


class TeamCTFFlagListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.TeamCTFFlag.objects.all()
    serializer_class = serializers.TeamCTFFlagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'team__name',
        'flag__flag',
    ]

    ordering_fields = [
        'team__name',
        'flag__flag'
    ]

    def create(self, request, *args, **kwargs):
        raise exceptions.AnswerSubmissionEnded()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({
            "message": "پاسخ شما صحیح میباشد.",
            "instance": self.get_serializer(instance).data
        }, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class TeamCTFHintListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.TeamCTFHint.objects.all()
    serializer_class = serializers.TeamCTFHintSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'team__name',
        'hint__hint',
    ]

    ordering_fields = [
        'team__name',
        'hint__hint'
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        hint_text = instance.hint.hint

        return Response({
            "hint": hint_text
        }, status=status.HTTP_201_CREATED)


class Pay(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Initiate Zarinpal Payment",
        responses={
            200: openapi.Response(
                description="Payment initiated successfully",
                examples={
                    "application/json": {
                        "status": True,
                        "url": "https://zarinpal.com/startpay/<authority>",
                        "authority": "<authority>"
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def get(self, request):
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": settings.AMOUNT,
            "description": settings.DESCRIPTION,
            "callback_url": settings.CALLBACK_URL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                   'content-length': str(len(data))}
        try:
            response = requests.post(
                settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()['data']

                if response['code'] == 100:
                    authority = response['authority']
                    Authority.objects.create(
                        team=request.user.team, authority=response['authority'])
                    return Response(
                        {'status': True, 'url': settings.ZP_API_STARTPAY + str(authority), 'authority': authority})
                else:
                    return Response({'status': False, 'code': str(response['code'])},
                                    status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(response)

        except requests.exceptions.Timeout:
            return Response({'status': False, 'code': 'timeout'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return Response({'status': False, 'code': 'connection error'}, status=status.HTTP_400_BAD_REQUEST)


class Vrify(APIView):

    def get(self, request):
        authority = request.GET.get('Authority', '')
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": settings.AMOUNT,
            "authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                   'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY,
                                 data=data, headers=headers)
        redirect_url = settings.REDIRECT_PATH

        if response.status_code == 200:
            response = response.json()['data']
            if response['code'] == 100:
                authority_object = None
                try:
                    authority_object = Authority.objects.get(
                        authority=authority)
                except Authority.DoesNotExist:

                    return Response(status=302, headers={
                        'Location': f"{redirect_url}?status:False&RefID={response['ref_id']}&message=Authority Doesnt Exist"})

                authority_object.team.status = "payed"
                authority_object.team.save()
                setattr(authority_object, "verified", True)
                authority_object.save()

                return Response(status=302, headers={
                    'Location': f"{redirect_url}?status:True&RefID={response['ref_id']}&message=transaction complete"})
            elif response['code'] == 101:
                return Response(status=302, headers={
                    'Location': f"{redirect_url}?status:False&RefID={response['ref_id']}&message=transaction already verified"})
            else:
                return Response(status=302, headers={
                    'Location': f"{redirect_url}?status:False&RefID={response['ref_id']}&message={str(response['code'])}"})

        return Response(status=302, headers={
            'Location': f"{redirect_url}?status:False&RefID={response['ref_id']}&message={response.status_code}"})


class ListCTFQuestionPortApiView(ListAPIView):
    serializer_class = CTFQuestionPortSerializer

    def get_queryset(self):
        return CTFQuestionPort.objects.filter(question_id=self.kwargs['question_pk'], hidden=False)
