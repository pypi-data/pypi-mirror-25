from django.http import HttpResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket

from bamb import Bamb
from domain import user
from common import constants


# Create your views here.

@accept_websocket
def simple_websocket_client(request):
    if not request.is_websocket():#判断是不是websocket连接
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'ui/websocket.html')
    else:
        acc = request.GET['account']
        um = Bamb.bean(constants.SERVICE_USER_MANAGER)
        if len(acc) > 0:
            u = user.User(acc, client=request.websocket)
            um.user_login(u)

        users = um.online_users

        for message in request.websocket:
            for k, u in users.items():
                ws = u.client_object
                if ws is not None:
                    if not ws.closed:
                        ws.send(message)