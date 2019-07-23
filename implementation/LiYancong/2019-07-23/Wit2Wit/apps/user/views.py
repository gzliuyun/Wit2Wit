from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from user.models import User, Address
import re
from utils.UserUtil import random_code
from utils.Send_Message import send_message
from django.core.urlresolvers import reverse
import hashlib
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from utils.UserUtil import LoginRequiredMixin
import time
from math import *
from order.models import OrderInfo, OrderGoods


# Create your views here.
# /user/register
class RegisterView(View):
    '''注册'''

    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        # 接收数据
        mobile = request.POST.get('mobile')
        password = request.POST.get('pwd')
        code = request.POST.get('code')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([mobile, password, code]):
            # 数据不完整
            return render(request, 'register.html', {'status': -1, 'msg': '数据不完整'})
        if allow != 'on':
            return render(request, 'register.html', {'status': 0, 'msg': '请同意协议'})
        session_mobile = request.session.get('mobile', None)  # 从session中获取手机号和验证码
        session_code = request.session.get('code', None)
        if session_mobile == mobile and session_code == code:  # 判断手机号和验证码是不是正确
            user = User.objects.create_user(mobile, '', password)
            user.mobile = mobile
            user.save()
            # 存入数据库
            # password = hashlib.md5(bytes(password, encoding="utf8")).hexdigest()  # 先用md5加密
            # User.objects.create(mobile=mobile, password=password, username=mobile)
            user = authenticate(username=mobile, password=password)
            login(request, user)
            # # 将手机号和加密以后的密码存入cookie，表示已经登录了
            # response = redirect(reverse('goods:index'))
            # response.set_cookie('mobile', mobile, max_age=7 * 24 * 3600)
            # response.set_cookie('password', password, max_age=7 * 24 * 3600)
            # 跳转到首页
            # return response
            # return redirect(reverse('goods:index'))
            return render(request, 'index.html', {'status': 1, 'msg': '登录成功'})
        else:
            return render(request, 'register.html', {'status': 2, 'msg': '验证码和手机号不匹配'})


# /user/send_message
class SendMessageView(View):
    '''发送短信获取验证码'''

    def get(self, request):
        status = -1  # -1 表示手机号不合法
        # 获取前台传来的手机号
        mobile = request.GET['mobile']
        # 对手机号进行正则校验
        ret = re.match(r"^1\d{10}$", mobile)

        if not ret:  # 如果不是正确格式的手机号
            return JsonResponse({"status": status, "msg": "请输入正确的手机号"})
        else:  # 如果是正确格式的手机号
            # 判断该手机号是否已经注册
            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                # 用户名不存在
                user = None
            if user:
                status = 0  # 0 表示手机号已注册
                return JsonResponse({'status': status, "msg": "该手机号已注册，请直接登录"})
            else:
                # 随机的6位数字，如果需要字母+数字，则不需要传第二个参数
                code = random_code(6, False)
                # 发送短信，并获取返回值

                time_send_msg = request.session.get('time_send_msg', None)  # 从session里取上一次发送短信的时间
                if time_send_msg:  # 如果发现以前有发送过短信的记录
                    time_now = time.time()  # 那就看看时间是否超过一分钟了
                    if time_now - float(time_send_msg) <= 60:
                        msg = "请于" + str(60 - floor(time_now - float(time_send_msg))) + "秒后再发送短信验证码"
                        return JsonResponse({'status': -1, "msg": msg})
                is_success = True
                # is_success = send_message(mobile, code)  # 这里先被注释掉了，如果需要发短信的话，要取消注释，并修改方法里面的内容
                if is_success:  # 如果发送成功了，返回值是True
                    request.session['time_send_msg'] = time.time()
                    status = 1  # 1表示手机号合法，也发送短信成功了
                    # 把手机号和验证码存到session里面，安全
                    request.session['mobile'] = mobile
                    request.session['code'] = code
                    # return JsonResponse({"status": status, 'msg': '短信发送成功'})
                    return JsonResponse({"status": status, 'msg': code})  # 这里到时候也要注释掉，并且把上一行取消注释
                else:
                    status = 2  # 2表示短信发送失败了，具体为什么失败了，可以去send_message中的返回值调试查看
                    return JsonResponse({"status": status, 'msg': '短信发送失败'})


# /user/login
class LoginView(View):
    '''登录'''

    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'mobile' in request.COOKIES:
            mobile = request.COOKIES.get('mobile')
            checked = 'checked'
        else:
            mobile = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'mobile': mobile, 'checked': checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        mobile = request.POST.get('mobile')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([mobile, password]):
            return render(request, 'login.html', {'status': -1, 'msg': '数据不完整'})
        # 业务处理:登录校验
        user = authenticate(username=mobile, password=password)
        if user is not None:
            # 用户名密码正确
            # 记录用户的登录状态
            login(request, user)
            # 获取登录以后要跳转的地址，如果地址栏中有?next=***，则跳转到该地址，如果没有，则反向解析跳到首页
            next_url = request.GET.get('next', reverse('goods:index'))
            # 跳转到next_url
            response = redirect(next_url)
            # 判断是否需要记住用户名
            remember = request.POST.get('remember')
            if remember == 'on':
                # 记住用户名
                response.set_cookie('mobile', mobile, max_age=7 * 24 * 3600)
            else:
                response.delete_cookie('mobile')
            # 返回response
            return response
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'status': 0, 'msg': '用户名或密码错误'})


# /user/logout
class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    '''用户信息页'''

    def get(self, request):
        return render(request, 'user_center.html', {'page': 'user'})


# /user/order/page
class UserOrderView(LoginRequiredMixin, View):
    '''用户订单页'''

    def get(self, request, page):
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')  # 按创建时间倒序获取订单

        for order in orders:
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)  # 每个订单下面都有哪些商品

            for order_sku in order_skus:
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

        return render(request, 'user_center.html', {'page': 'order'})


# /user/address
class AddressView(LoginRequiredMixin, View):
    '''用户地址页'''

    def get(self, request):
        # 收货地址的获取
        # 先获取当前已经登录的用户
        user = request.user
        try:
            address_list = Address.objects.filter(user=user)  # 把这个用户所有的地址都获取出来
        except Exception as e:
            address_list = None
        return render(request, 'user_center.html', {'page': 'address', 'address_list': address_list})

    def post(self, request):
        # 收货地址的添加
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        mode = str(request.POST.get('mode'))
        if mode == '1':  # 新增
            # 对数据的完整性进行
            if not all([receiver, addr, phone]):
                return render(request, 'user_center.html', {'page': 'address', 'status': -1, 'msg': '数据不完整'})
            # 检查手机号是否符合规范
            if not re.match(r"^1\d{10}$", phone):
                return render(request, 'user_center.html', {'page': 'address', 'status': -1, 'msg': '手机号格式不正确'})
            # 获取到当前已经登录的用户
            user = request.user
            # 判断一下该用户是不是已经有了默认收货地址
            address = Address.objects.get_default_address(user)
            if address:  # 如果有一个默认收货地址了，那就给新添加的收货地址设置为非默认
                is_default = False
            else:  # 如果当前用户还没有默认收货地址，那就给新添加的收货地址设置为默认
                is_default = True
            # 将以上数据添加到数据库的Address表中
            Address.objects.create(user=user,
                                   receiver=receiver,
                                   addr=addr,
                                   zip_code=zip_code,
                                   phone=phone,
                                   is_default=is_default)
            return render(request, 'user_center.html', {'page': 'address', 'status': 1, 'msg': '新增收货地址成功'})
        elif mode == '2':  # 修改
            # 对数据的完整性进行
            if not all([receiver, addr, phone]):
                return render(request, 'user_center.html', {'page': 'address', 'status': -1, 'msg': '数据不完整'})
            # 检查手机号是否符合规范
            if not re.match(r"^1\d{10}$", phone):
                return render(request, 'user_center.html', {'page': 'address', 'status': -1, 'msg': '手机号格式不正确'})
            address_id = request.POST.get("address_id")
            address = Address.objects.get(id=address_id)
            address.receiver = receiver
            address.addr = addr
            address.phone = phone
            address.zip_code = zip_code
            address.save()
            return render(request, 'user_center.html', {'page': 'address', 'status': 1, 'msg': '修改成功'})
        elif mode == '3':  # 删除
            address_id = request.POST.get("address_id")
            Address.objects.filter(id=address_id).delete()
            return render(request, 'user_center.html', {'page': 'address', 'status': 1, 'msg': '删除成功'})
        elif mode == '4':  # 设为默认地址
            # 获取到当前已经登录的用户
            user = request.user
            # 判断一下该用户是不是已经有了默认收货地址
            address = Address.objects.get_default_address(user)
            if address:  # 如果有一个默认收货地址了，那就给新添加的收货地址设置为非默认
                address.is_default = False
                address.save()
            address_id = request.POST.get("address_id")
            address = Address.objects.get(id=address_id)
            address.is_default = True
            address.save()
            return render(request, 'user_center.html', {'page': 'address', 'status': 1, 'msg': '默认地址设置成功'})
        else:
            return redirect(reverse('user:address'))


# 修改登录用户判断
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
