from django.shortcuts import render, redirect
from django.views.generic import View
from utils.UserUtil import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection
from user.models import Address
from goods.models import GoodsSKU
from django.db import transaction
from django.http import JsonResponse
from order.models import OrderInfo, OrderGoods
from datetime import datetime


# Create your views here.

# /order/confirm_order
class OrderPageView(LoginRequiredMixin, View):
    '''提交订单页面显示'''

    def post(self, request):
        user = request.user
        sku_ids = request.POST.getlist('sku_ids')  # 从前台提交过来的name为sku_ids的数据，里边存放了所有被选中的商品id，为列表形式

        # 看看传过来的id对不对，如果不对，就跳转到购物车页面
        if not sku_ids:
            return redirect(reverse('cart:cartinfo'))

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        skus = []
        # 保存商品的总件数和总价格
        total_count = 0
        total_price = 0
        # 遍历sku_ids获取用户要购买的商品的信息
        for sku_id in sku_ids:
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 获取用户所要购买的商品的数量
            count = conn.hget(cart_key, sku_id)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给sku增加属性count,保存购买商品的数量
            sku.count = count
            # 动态给sku增加属性amount,保存购买商品的小计
            sku.amount = amount
            # 追加
            skus.append(sku)
            # 累加计算商品的总件数和总价格
            total_count += int(count)
            total_price += amount

        # 运费
        postage = 0  # 写死

        # 实付款
        total_pay = total_price + postage

        # 获取用户的收件地址
        addrs = Address.objects.filter(user=user)

        # 组织上下文
        sku_ids = ','.join(sku_ids)  # [1,25]->1,25
        context = {'skus': skus,
                   'cart_count': total_count,
                   'cart_price': total_price,
                   'postage': postage,
                   'total_price': total_pay,
                   'addrs': addrs,
                   'sku_ids': sku_ids}

        # 使用模板
        return render(request, 'order.html', context)


# /order/submit_order
class OrderSubmitView(View):
    '''创建一个新的订单'''

    @transaction.atomic
    def post(self, request):
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'status': -1, 'msg': '用户未登录'})  # 返回-1的话，需要跳转，所以要和其他的status值区别开

        # 接收参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        teaching_mode = request.POST.get('teaching_mode')
        sku_ids = request.POST.get('sku_ids')  # 1,2,3

        # 校验参数
        if not all([addr_id, pay_method, teaching_mode, sku_ids]):
            return JsonResponse({'status': 0, 'msg': '参数不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'status': 0, 'msg': '无效的支付方式'})

            # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            # 地址不存在
            return JsonResponse({'status': 0, 'msg': '无效的授业地址'})
        # 开始创建订单

        # 组织参数
        # 订单id: 当前时间+用户id
        # order_id = str(time.time(), 2).replace('.', '') + str(user.id)
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # 运费
        postage = 0

        # 总数目和总金额
        total_count = 0
        total_price = 0

        # 设置事务保存点
        save_id = transaction.savepoint()
        try:
            # 向df_order_info表中添加一条记录
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             addr=addr,
                                             pay_method=pay_method,
                                             teaching_mode=teaching_mode,
                                             total_count=total_count,
                                             total_price=total_price,
                                             transit_price=postage)

            # 用户的订单中有几个商品，需要向df_order_goods表中加入几条记录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')
            for sku_id in sku_ids:
                for i in range(3):
                    # 获取商品的信息
                    try:
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except:
                        # 商品不存在
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'status': 0, 'msg': '商品不存在'})

                    # 从redis中获取用户所要购买的商品的数量
                    count = conn.hget(cart_key, sku_id)

                    # 判断商品的库存
                    if int(count) > sku.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'status': 0, 'msg': '商品库存不足'})

                    # 更新商品的库存和销量
                    orgin_stock = sku.stock
                    new_stock = orgin_stock - int(count)
                    new_sales = sku.sales + int(count)

                    # 返回受影响的行数
                    # 在这里用了简单的乐观锁，不过只是判断了库存是不是和之前一致，如果项目说不要有库存这个东西啦，那么我们就判断销量好了
                    res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)
                    if res == 0:
                        if i == 2:
                            # 尝试的第3次
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'status': 0, 'msg': '下单失败'})
                        continue

                    # 向df_order_goods表中添加一条记录
                    OrderGoods.objects.create(order=order,
                                              sku=sku,
                                              count=count,
                                              price=sku.price)

                    # 累加计算订单商品的总数量和总价格
                    amount = sku.price * int(count)
                    total_count += int(count)
                    total_price += amount

                    # 跳出循环
                    break

            # 更新订单信息表中的商品的总数量和总价格
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'status': 0, 'msg': '下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # 清除用户购物车中对应的记录,因为sku_ids是列表，所以用*拆开
        conn.hdel(cart_key, *sku_ids)

        # 返回应答
        return JsonResponse({'status': 1, 'msg': '下单成功'})
