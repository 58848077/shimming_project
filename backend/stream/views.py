import json
import yt_dlp

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
# from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from datetime import datetime
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage,send_mail
from django.contrib.sessions.models import Session 
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

class StreamStatus(APIView):
    def check_url(self, url: str):
        """
        檢查網址
        1. 是否為空
        2. 開頭是否為 https://www.youtube.com/
        """
        result = {
            "status": False,
            "message": "",
        }
        
        if not url:
            result["message"] = "url_required"
            return result
        
        youtube_prefix = "https://www.youtube.com/"
        if not url.startswith(youtube_prefix):
            result["message"] = "unsupported_url"
            return result
        
        result["status"] = True
        return result
        
    def get_stream_status(self, url: str):
        """取得直播狀態"""
        result = {
            "status": False,
            "message": "",
            "data": {
                "stream_status": ""
            },
        }
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            result["status"] = True
            result["data"] = {}
            result["data"]["stream_status"] = info["is_live"]
        except yt_dlp.utils.DownloadError as e:
            # 無法處理的url
            result["message"] = "unsupported_url"
        except Exception as ex:
            # 處理未考量到的例外情況
            result["message"] = "api_error"
            
        return result

    def get(self, request, format=None):
        """
        透過yt_dlp API取得youtube直播狀態。
        
        Params
            - url: str, 欲確認的直播地址網址
        
        Return
            - status: bool, 此次呼叫狀態，True為成功；False為失敗。
            - message: str, 若status為False，則回傳失敗原因。
            - data: dict, 回傳請求資料
                - stream_status: bool, 欲確認的直播地址網址的狀態
        """
        result = {
            "status": False,
            "message": "",
        }
        
        URL = request.query_params.get("url", "")
        check_url = self.check_url(url=URL)
        if not check_url["status"]:
            result["message"] = check_url["message"]
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        stream_status = self.get_stream_status(url=URL)
        if stream_status["status"]:
            result["status"] = True
            result["data"] = {}
            result["data"]["stream_status"] = stream_status["data"]["stream_status"]
        else:
            result["message"] = stream_status["message"]
        
        return Response(result) if result["status"] else Response(result, status=status.HTTP_400_BAD_REQUEST)
