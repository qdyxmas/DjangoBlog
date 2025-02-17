import base64
import gzip
import json
import datetime
import logging
from hashids import Hashids
from django.shortcuts import render
from djangoblog.decode_utils import aes_ecb
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from jsondata.models import JsonData
from jsondata.jsondata_controller import JsonDataSerializer



logger = logging.getLogger(__name__)
ALPHABET = 'abcdefghijklmnopqstuvwxyz123456789'
hashids = Hashids(alphabet=ALPHABET)


def decode(request):
    """主页就是输入请求页面"""
    # print()
    if request.method == 'GET':
        result = {"input_data": "", "output_data": ""}
        return render(request, 'decode.html', result)
    elif request.method == 'POST':
        # print(request.__dict__)
        request_data = list(request.POST.items())
        request_data_dict = {}
        for key, value in request_data:
            request_data_dict[key] = value
        post_data = aes_ecb.decrypt(request_data_dict["input_data"])
        #post_data = json.dumps(post_data,indent=4,separators=(',',':')).encode('utf-8').decode('raw_unicode_escape')
        #print(post_data)
        result = {"input_data": request_data_dict["input_data"], "output_data": post_data}
        # print(result)
        return render(request, 'decode.html', {"r": result})


def encode(request):
    """主页就是输入请求页面"""
    if request.method == 'GET':
        result = {"input_data": "", "output_data": ""}
        return render(request, 'decode.html', result)
    elif request.method == 'POST':
        # print(request.__dict__)
        request_data = list(request.POST.items())
        request_data_dict = {}
        for key, value in request_data:
            request_data_dict[key] = value
        post_data = aes_ecb.encrypt(request_data_dict["input_data"])
        result = {"input_data": request_data_dict["input_data"], "output_data": post_data}
        # print(result)
        return render(request, 'decode.html', {"r": result})

def wssdecode(request):
    """主页就是输入请求页面"""
    if request.method == 'GET':
        result = {"input_data": "", "output_data": ""}
        return render(request, 'decode.html', result)
    elif request.method == 'POST':
        # print(request.__dict__)
        request_data = list(request.POST.items())
        request_data_dict = {}
        for key, value in request_data:
            request_data_dict[key] = value
            
        gzipdata = base64.b64decode(request_data_dict["input_data"])
        post_data=gzip.decompress(gzipdata).decode('utf-8')
        result = {"input_data": request_data_dict["input_data"], "output_data": post_data}
        # print(result)
        return render(request, 'decode.html', {"r": result})


def id_encode(request):
    if request.method == 'GET':
        result = {"input_data": "", "output_data": ""}
        return render(request, 'decode.html', result)
    elif request.method == 'POST':
        # print(request.__dict__)
        request_data = list(request.POST.items())
        request_data_dict = {}
        for key, value in request_data:
            request_data_dict[key] = value
            
        post_data = hashids.encode(int(request_data_dict["input_data"]))
        result = {"input_data": request_data_dict["input_data"], "output_data": post_data}
        # print(result)
        return render(request, 'decode.html', {"r": result})



def id_decode(request):
    if request.method == 'GET':
        result = {"input_data": "", "output_data": ""}
        return render(request, 'decode.html', result)
    elif request.method == 'POST':
        # print(request.__dict__)
        request_data = list(request.POST.items())
        request_data_dict = {}
        for key, value in request_data:
            request_data_dict[key] = value
            
        t = hashids.decode(request_data_dict["input_data"])
        post_data = t[0] if len(t) > 0 else None
        result = {"input_data": request_data_dict["input_data"], "output_data": post_data}
        # print(result)
        return render(request, 'decode.html', {"r": result})


def sms(request, methods=['GET']):
    """主页就是输入请求页面"""
    if request.method == 'GET':
        user_agent = request.META['HTTP_USER_AGENT']
        if "iPhone" in user_agent:
            SMS_DATA = "0;url=tel:{}".format(request.GET.get("tel"))
        else:
            SMS_DATA = "0;url=tel:{}".format(request.GET.get("tel"))
        return render(request, 'sms.html', {"SMS_DATA":SMS_DATA,"user_agent":user_agent})


def save_json(request, methods=['POST']):
    """把request转换成post"""
    request_data = list(request.POST.items())
    request_data_dict = {}
    for key, value in request_data:
        request_data_dict[key] = value

    output_data = {"data":request_data_dict["output_data"]}
    jsondata_serializer = JsonData(data=output_data)
    jsondata_serializer.save()
    url = """0.5;http://{}/get_json?id={}""".format(request.get_host(),jsondata_serializer.id)
    return render(request, 'post_json.html', {"JSONDATA":url,"ID":jsondata_serializer.id})

@api_view(["GET"])
def get_json(request):
    """把request转换成get"""
    pk = request.GET.get("id")
    try:
        apiservice = JsonData.objects.get(id=pk)
    except JsonData.DoesNotExist: 
        return render(request, 'json.html', {"JSONDATA":"数据为空"})
    #jsondata_serializer = JsonDataSerializer(data=apiservice)
    #data = json.dumps(apiservice.data,sort_keys=True,indent=4,separators=(',',':')).encode('utf-8').decode('raw_unicode_escape')
    #logger.info("jsondata=:{}".format(apiservice.data["data"]))
    return render(request, 'json.html', {"JSONDATA":apiservice.data["data"]})

