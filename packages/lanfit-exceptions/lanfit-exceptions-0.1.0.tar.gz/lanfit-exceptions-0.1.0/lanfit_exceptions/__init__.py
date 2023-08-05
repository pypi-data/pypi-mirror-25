# -*- coding: utf-8 -*-
import sys

current_module = sys.modules[__name__]


exceptions = [
    ('NoError', 0, 'ok'),

    ('LoginRequired', 1001, 'Login required'),
    ('BindPhoneRequired', 1002, 'Bind phone required'),
    ('CompleteMemberInfoRequired', 1003, '需要完善用户信息.'),
    ('SendSMSWait', 1004, '稍后发送'),
    ('PhoneUsed', 1005, '手机号已经被使用'),
    ('WXAuthNotFound', 1006, '没有找到微信授权信息'),
    ('SMSCodeError', 1007, '验证码错误'),
    ('NotBrandAdmin', 1008, '不是管理员'),
    ('NoBrandError', 1009, '没有品牌'),

    ('FieldRequired', 2002, '字段不能为空'),

    ('ItemNotExist', 3001, 'Item not exist'),
    ('NotExistMembershipType', 3002, '不存在的会员类型'),
    ('TypeDayMembershipCanNotRenew', 3003, '体验卡会员不能续费,请升级或体验期结束后购买'),
    ('MembershipCanNotRenewToTypeDay', 3004, '会员期间不能续费为体验会员'),
    ('NotSupportItemType', 3005, '未支持的商品类型'),
    ('NoMembership', 3006, '需要开通会员'),
    ('MembershipExpired', 3007, '会员已过期'),
    ('SignError', 3008, '签到错误'),

    ('NotFound', 4004, 'Not Found'),

    ('TradeNotExist', 5001, '订单不存在'),
    ('WXOrderPaid', 5002, '该订单已支付'),
    ('NotImplementedTradeItem', 5003, '没有实现的交易类型'),
    ('FinishTradeError', 5004, '完成订单处理错误'),
    ('PayFeeError', 5005, '无效的支付金额'),
    ('WXPayInfoDifferent', 5006, '订单信息不一致'),

]


class BaseCustomException(Exception):
    errcode = 1000
    errmsg = 'Server Unkown Error.'

    def __init__(self, errmsg=None, errcode=None):
        if errmsg:
            self.errmsg = errmsg
        if errcode is not None:
            self.errcode = errcode

    def __str__(self):
        return '%d: %s' % (self.errcode, self.errmsg)

    def __repr__(self):
        return '<%s \'%s\'>' % (self.__class__.__name__, self)


class CustomException(BaseCustomException):
    pass


for name, errcode, errmsg in exceptions:
    cls = type(name,
               (CustomException,),
               {'errcode': errcode, 'errmsg': errmsg})
    setattr(current_module, name, cls)


class FormValidationError(BaseCustomException):
    errcode = 2001
    errmsg = '表单验证错误'

    def __init__(self, form, errmsg=None, show_first_err=False):
        if not errmsg and show_first_err:
            errmsg = next(iter(form.errors.values()))[0]
        super(FormValidationError, self).__init__(errmsg)
        self.errors = form.errors
