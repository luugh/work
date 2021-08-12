from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import json
import sys
dir = sys.path[0]+"/watch/interrupt_q"
print(dir)
sys.path.append(dir)
from interrupt_query import export_result


def hello(request):
    return HttpResponse('Hello world')


def ajax_list(request):
    a = list(range(100))
    return JsonResponse(a, safe=False)


def home(request):
    return render(request, 'index.html')


def third(request):
    return render(request, 'third.html')


def test_data(request):
    if request.method == 'GET':
        # ex = [
        #     {
        #         'a': '7',
        #         'b': '8',
        #         'c': '9',
        #         'd': '10',
        #         'e': '11',
        #         'f': '12'
        #     }, {
        #         'a': '7',
        #         'b': '8',
        #         'c': '9',
        #         'd': '10',
        #         'e': '11',
        #         'f': '12'
        #     }
        # ]
        # data = {'data': ex}
        # a = json.dumps(data)

        list_cp_all, cp_name, cp_stream, cp_cdn_s, cp_list_s_all, cp_cdn = export_result()
        print(list_cp_all, cp_name, cp_stream, cp_cdn_s, cp_list_s_all, cp_cdn)
        data_dict = []
        for cpc in list_cp_all:
            data = {
                'cp': cpc,
                'name': cp_name[cpc],
                'stream': cp_stream[cpc],
                'cdn_s': cp_cdn_s[cpc],
                'list_s': cp_list_s_all[cpc],
                'cp_cdn': cp_cdn[cpc]
            }
            data_dict.append(data)
        data_dict1 = {'data': data_dict}
        a = json.dumps(data_dict1)

        return HttpResponse(a, content_type='application/json')
    else:
        return HttpResponse('feifaqingqiu')

# def test():
#     list_cp_all, cp_name, cp_stream, cp_cdn_s, cp_list_s_all, cp_cdn = export_result()
#     data_dict = []
#     for cpc in list_cp_all:
#         data = {
#             'cp': cpc,
#             'name': cp_name[cpc],
#             'stream': cp_stream[cpc],
#             'cdn_s': cp_cdn_s[cpc],
#             'list_s': cp_list_s_all[cpc],
#             'cp_cdn': cp_cdn[cpc]
#         }
#         data_dict.append(data)
#
#     a = json.dumps(data_dict)
#     print(a)
#
#
# if __name__ == '__main__':
#     test()
