# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import QUANTAXIS as QA
from QUANTAXIS import QA_Backtest as QB


"""
写在前面:
===============QUANTAXIS BACKTEST STOCK_DAY中的变量
常量:
QB.backtest_type 回测类型 'day','min'
QB.account.message  当前账户消息
QB.account.cash  当前可用资金
QB.account.hold  当前账户持仓
QB.account.history  当前账户的历史交易记录
QB.account.assets 当前账户总资产
QB.account.detail 当前账户的交易对账单
QB.account.init_assest 账户的最初资金
QB.strategy_gap 前推日期
QB.strategy_name 策略名称

QB.strategy_stock_list 回测初始化的时候  输入的一个回测标的
QB.strategy_start_date 回测的开始时间
QB.strategy_end_date  回测的结束时间


QB.today  在策略里面代表策略执行时的日期
QB.now  在策略里面代表策略执行时的时间
QB.benchmark_code  策略业绩评价的对照行情




函数:
获取市场(基于gap)行情:
QB.QA_backtest_get_market_data(QB,code,QB.today,type)
type 可以指定是 pandas,numpy或者list 默认返回numpy格式

拿到开高收低量
Open,High,Low,Close,Volume=QB.QA_backtest_get_OHLCV(QB,QB.QA_backtest_get_market_data(QB,item,QB.today))

获取市场自定义时间段行情:
QA.QA_fetch_stock_day(code,start,end,model)

一键平仓:
QB.QA_backtest_sell_all(QB)

报单:
QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)

order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交
3.收盘价成交模式 order['bid_model']=3或者c,C

查询当前一只股票的持仓量
QB.QA_backtest_hold_amount(QB,code)


"""


@QB.backtest_init
def init():
    QB.backtest_type='day'
    QB.strategy_name='test_daily'
    #QB.backtest_type='5min' # 日线回测
    QB.setting.QA_util_sql_mongo_ip='127.0.0.1' #回测数据库
    QB.account.init_assest=2500000 # 初始资金
    QB.strategy_name='test_example' # 策略名称
    #benchmark 必须是指数代码
    QB.benchmark_code='399300'

    QB.strategy_stock_list=['000001','000002','600010','601801'] # 回测的股票列表
    QB.strategy_start_date='2016-07-01'  # 回测开始日期
    QB.strategy_end_date='2017-07-10'    # 回测结束日期

@QB.before_backtest
def before_backtest():
    global risk_position
    #QA.QA_util_log_info(QB.benchmark_data) 
    
    
@QB.load_strategy
def strategy():

    QA.QA_util_log_info(QB.account.sell_available)  
    QA.QA_util_log_info('LEFT Cash: %s'%QB.account.cash_available)
    for item in QB.strategy_stock_list:
        #QA.QA_util_log_info(QB.QA_backtest_get_market_data(QB,item,QB.today).data) 
        if QB.QA_backtest_hold_amount(QB,item)==0:
            QB.QA_backtest_send_order(QB,item,10000,1,{'bid_model':'Market'}) 

    
        else:
            #print(QB.QA_backtest_hold_amount(QB,item))
            QB.QA_backtest_send_order(QB,item,10000,-1,{'bid_model':'Market'})

@QB.end_backtest
def after_backtest():
    pass