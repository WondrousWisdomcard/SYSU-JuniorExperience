import math
from datetime import datetime, time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def show_plot_1(x, y_b, y_g):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    l1, = ax1.plot(x, y_b, c='#AACCFF', label='Bitcoin')
    l2, = ax2.plot(x, y_g, c='#CCAAFF', label='Gold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('BTC Price')
    ax2.set_ylabel('Gold Price')
    plt.xticks(())

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.legend(
        handles=[l1, l2, ],
        labels=["Bitcoin", "Gold", ],
        loc='upper left'
    )
    plt.grid()
    plt.show()

def show_plot_2(x, y_b, y_g):
    plt.figure()

    # 两行两列 第一个
    plt.subplot(2, 1, 1)
    plt.plot(x, y_b, label='Bitcoin', c='#AACCFF')
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(x, y_g, label='Gold', c='#CCAAFF')
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.show()

def show_plot_3(x, y_b, y_g):
    # 两行两列 第一个
    plt.subplot(2, 1, 1)
    plt.plot(x, y_b, label=f'$\Delta SMA(BTC)$', c='#AACCFF')
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(x, y_g, label=f'$\Delta SMA(Gold)$', c='#CCAAFF')
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.show()

def AAA(price_btc, price_gold, windowsize=15):
    price_btc = price_gold
    length = len(price_btc)
    sma_btc = []
    sma_gold = []
    for date in range(windowsize, length):
        sma_btc.append(price_btc[date - windowsize: date].std())
        sma_gold.append(price_gold[date - windowsize: date].std())

    print(np.array(sma_btc[:365]).mean())
    print(np.array(sma_btc[365+1:365*2]).mean())
    print(np.array(sma_btc[365*2+1:365*3]).mean())
    print(np.array(sma_btc[365*3+1:365*4]).mean())
    print(np.array(sma_btc[365*4+1:]).mean())

# 5个指标的计算
# Also Compute Delta SMA
def SMA(price_btc, price_gold, windowsize = 15):
    length = len(price_btc)
    sma_btc = []
    sma_gold = []
    # for i in range(windowsize):
    #     sma_btc.append(0)
    #     sma_gold.append(0)

    for date in range(windowsize, length):
        sma_btc.append(price_btc[date - windowsize: date].mean())
        sma_gold.append(price_gold[date - windowsize: date].mean())

    print("标准差")
    print(np.array(sma_btc).std())
    print(np.array(sma_gold).std())


    d4 = {
        "SMA_BTC": sma_btc,
        "SMA_Gold": sma_gold,
    }
    df = pd.DataFrame(d4)
    print(df.describe())

    a1 = pd.Series(sma_btc)
    a2 = pd.Series(sma_gold)
    corr = a1.corr(a2, method='spearman')
    print(corr)

    dsma_btc = []
    dsma_gold = []
    for i in range(len(sma_gold) - 1):
        dsma_gold.append(sma_gold[i + 1] - sma_gold[i])
        dsma_btc.append(sma_btc[i + 1] - sma_btc[i])

    a1 = pd.Series(dsma_btc)
    a2 = pd.Series(dsma_gold)
    corr = a1.corr(a2, method='spearman')
    print(corr)

    # show_plot_3(range(len(dsma_btc)), dsma_btc, dsma_gold)


    # plt.plot(range(len(sma_btc)), sma_btc, label='Bitcoin', c='#AADDFF')
    # plt.plot(range(len(sma_gold)), sma_gold, label='Gold', c='#DDAAFF')
    # plt.title("SMA (Window Size = 15)", fontsize=20)
    # plt.xticks(())
    # plt.legend()

    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # l1, = ax1.plot(range(len(sma_btc)), sma_btc, label='Bitcoin', c='#AADDFF')
    # l2, = ax2.plot(range(len(sma_gold)), sma_gold, label='Gold', c='#DDAAFF')
    # ax1.set_xlabel('Date')
    # ax1.set_ylabel('SMA(BTC)')
    # ax2.set_ylabel('SMA(Gold)')
    # plt.xticks(())
    #
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    #
    # plt.legend(
    #     handles=[l1, l2, ],
    #     labels=["Bitcoin", "Gold", ],
    #     loc='upper left'
    # )
    # plt.grid()
    # plt.show()

    return sma_btc, sma_gold

def MACD(price_btc, price_gold):
    length = len(price_btc)
    macd_btc = []
    macd_gold = []
    ema12_btc = []
    ema12_gold = []
    ema26_btc = []
    ema26_gold = []

    ema12_btc.append(price_btc[0])
    ema12_gold.append(price_gold[0])
    ema26_btc.append(price_btc[0])
    ema26_gold.append(price_gold[0])

    for date in range(1, length):

        ema12_btc.append(ema12_btc[-1] * 11 / 13 + price_btc[date] * 2 / 13)
        ema12_gold.append(ema12_gold[-1] * 11 / 13 + price_gold[date] * 2 / 13)

        ema26_btc.append(ema26_btc[-1] * 25 / 27 + price_btc[date] * 2 / 27)
        ema26_gold.append(ema26_gold[-1] * 25 / 27 + price_gold[date] * 2 / 27)

    dif_btc = []
    dif_gold = []
    for i in range(length):
        dif_btc.append(ema12_btc[i] - ema26_btc[i])
        dif_gold.append(ema12_gold[i] - ema26_gold[i])

    dif_btc2 = np.array(dif_btc)
    dif_gold2 = np.array(dif_gold)

    for date in range(9, length):
        macd_btc.append(dif_btc2[date - 9: date].mean())
        macd_gold.append(dif_gold2[date - 9: date].mean())

    # d4 = {
    #     "MACD_BTC": macd_btc,
    #     "MACD_GOLD": macd_gold,
    # }
    # df = pd.DataFrame(d4)
    # print(df.describe())

    # plt.plot(range(len(macd_btc)), macd_btc, label='Bitcoin', c='#AADDFF')
    # plt.plot(range(len(macd_gold)), macd_gold, label='Gold', c='#DDAAFF')
    # plt.title("MACD", fontsize=20)
    # plt.xticks(())
    # plt.legend()

    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # l1, = ax1.plot(range(len(macd_btc)), macd_btc, label='Bitcoin', c='#AADDFF')
    # l2, = ax2.plot(range(len(macd_gold)), macd_gold, label='Gold', c='#DDAAFF')
    # ax1.set_xlabel('Date')
    # ax1.set_ylabel('MACD(BTC)')
    # ax2.set_ylabel('MACD(Gold)')
    # plt.xticks(())
    #
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    #
    # plt.legend(
    #     handles=[l1, l2, ],
    #     labels=["Bitcoin", "Gold", ],
    #     loc='upper left'
    # )
    # plt.title("MACD", fontsize=20)
    # plt.grid()
    # plt.show()

    return dif_btc, dif_gold, macd_btc, macd_gold

def KD(price_btc, price_gold, t = 15):
    length = len(price_btc)
    k_btc = []
    k_gold = []
    d_btc = []
    d_gold = []

    low_btc = []
    low_gold = []
    high_btc = []
    high_gold = []

    for i in range(t, length):
        low_btc.append(price_btc[i - t: i + 1].min())
        low_gold.append(price_gold[i - t: i + 1].min())

        high_btc.append(price_btc[i - t: i + 1].max())
        high_gold.append(price_gold[i - t: i + 1].max())

    for i in range(t, length):
        k_btc.append((price_btc[i] - low_btc[i - t]) / (high_btc[i - t] - low_btc[i - t]))
        k_gold.append((price_gold[i] - low_gold[i - t]) / (high_gold[i - t] - low_gold[i - t]))

    for i in range(0, length - t):
        d_btc.append((k_btc[i - 2] + k_btc[i - 1] + k_btc[i]) / 3)
        d_gold.append((k_gold[i - 2] + k_gold[i - 1] + k_gold[i]) / 3)

    d4 = {
        "K_BTC": k_btc,
        "K_GOLD": k_gold,
        "D_BTC": d_btc,
        "D_GOLD": d_gold
    }
    df = pd.DataFrame(d4)
    print(df.describe())

    plt.figure()

    plt.subplot(4, 1, 1)
    plt.plot(range(len(k_btc)), k_btc, label='K-Bitcoin', c='#AADDFF')
    # plt.plot(range(len(k_gold)), k_gold, label='K-Gold', c='#DDAAFF')
    plt.title("K-Line(Bitcoin)", fontsize=10)
    plt.xticks(())
    plt.legend(loc='upper right')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.subplot(4, 1, 2)
    plt.plot(range(len(d_btc)), d_btc, label='D-Bitcoin', c='#FFAADD')
    # plt.plot(range(len(d_gold)), d_gold, label='D-Gold', c='#FFDDAA')
    plt.title("D-Line(Bitcoin)", fontsize=10)
    plt.xticks(())
    plt.legend(loc='upper right')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.subplot(4, 1, 3)
    plt.plot(range(len(k_gold)), k_gold, label='K-Gold', c='#DDAAFF')
    # plt.plot(range(len(k_btc)), k_btc, label='K-Bitcoin', c='#AADDFF')
    # plt.plot(range(len(d_btc)), d_btc, label='D-Bitcoin', c='#FFAADD')
    plt.title("K-Line(Gold)", fontsize=10)
    plt.xticks(())
    plt.legend(loc='upper right')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.subplot(4, 1, 4)
    # plt.plot(range(len(k_gold)), k_gold, label='K-Gold', c='#DDAAFF')
    plt.plot(range(len(d_gold)), d_gold, label='D-Gold', c='#FFDDAA')
    plt.title("D-Line(Gold)", fontsize=10)
    plt.xticks(())
    plt.legend(loc='upper right')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.show()

    return k_btc, k_gold, d_btc, d_gold

def RSI(price_btc, price_gold, windowsize = 15):
    length = len(price_btc)
    rsi_btc = []
    rsi_gold = []
    rs_btc = []
    rs_gold = []
    dprice_btc = []
    dprice_gold = []

    for i in range(1, length):
        dprice_btc.append(price_btc[i] - price_btc[i - 1])
        dprice_gold.append(price_gold[i] - price_gold[i - 1])

    for i in range(windowsize, length-1):
        temp = dprice_gold[i - windowsize: i]
        count_pos = 0
        count_neg = 0
        sum_pos = 0
        sum_neg = 0
        for j in temp:
            if j > 0:
                count_pos += 1
                sum_pos += j
            elif j < 0:
                count_neg += 1
                sum_neg -= j

        if sum_neg != 0 and sum_pos != 0:
            ans = (sum_pos / count_pos) / (sum_neg / count_neg)
        else:
            ans = 0
        rs_gold.append(ans)
        rsi_gold.append(100 - 100 / (1 + ans))

    for i in range(windowsize, length - 1):
        temp = dprice_btc[i - windowsize: i]
        count_pos = 0
        count_neg = 0
        sum_pos = 0
        sum_neg = 0
        for j in temp:
            if j > 0:
                count_pos += 1
                sum_pos += j
            elif j < 0:
                count_neg += 1
                sum_neg -= j

        if sum_neg != 0 and sum_pos != 0:
            ans= (sum_pos / count_pos) / (sum_neg / count_neg)
        else:
            ans = 0
        rs_btc.append(ans)
        rsi_btc.append(100 - 100 / (1 + ans))


    d4 = {
        "RSI_BTC": rsi_btc,
        "RSI_Gold": rsi_gold,
    }
    df = pd.DataFrame(d4)
    print(df.describe())

    plt.plot(range(len(rsi_btc)), rsi_btc, label='Bitcoin', c='#AADDFF')
    plt.plot(range(len(rsi_gold)), rsi_gold, label='Gold', c='#DDAAFF')
    plt.title(f"RSI (Window Size = %d)" % windowsize, fontsize=20)
    plt.xticks(())
    plt.legend()
    #
    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # l1, = ax1.plot(range(len(sma_btc)), sma_btc, label='Bitcoin', c='#AADDFF')
    # l2, = ax2.plot(range(len(sma_gold)), sma_gold, label='Gold', c='#DDAAFF')
    # ax1.set_xlabel('Date')
    # ax1.set_ylabel('SMA(BTC)')
    # ax2.set_ylabel('SMA(Gold)')
    # plt.xticks(())
    #
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    #
    # plt.legend(
    #     handles=[l1, l2, ],
    #     labels=["Bitcoin", "Gold", ],
    #     loc='upper left'
    # )
    # plt.grid()
    plt.show()

    return rsi_btc, rsi_gold

def R(price_btc, price_gold, t = 15):
    length = len(price_btc)
    r_btc = []
    r_gold = []

    low_btc = []
    low_gold = []
    high_btc = []
    high_gold = []

    for i in range(t, length):
        low_btc.append(price_btc[i - t: i + 1].min())
        low_gold.append(price_gold[i - t: i + 1].min())

        high_btc.append(price_btc[i - t: i + 1].max())
        high_gold.append(price_gold[i - t: i + 1].max())

    for i in range(t, length):
        r_btc.append((- price_btc[i] + high_btc[i - t]) / (high_btc[i - t] - low_btc[i - t]))
        r_gold.append((- price_gold[i] + high_gold[i - t]) / (high_gold[i - t] - low_gold[i - t]))


    d4 = {
        "R_BTC": r_btc,
        "R_GOLD": r_gold,
    }
    df = pd.DataFrame(d4)
    print(df.describe())

    plt.figure()

    plt.subplot(2, 1, 1)
    plt.plot(range(len(r_btc)), r_btc, label='R-Bitcoin', c='#AADDFF')
    plt.title("R-Line(Bitcoin)", fontsize=15)
    plt.xticks(())
    plt.legend(loc='upper right')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(range(len(r_gold)), r_gold, label='R-Gold', c='#DDAAFF')
    plt.title("R-Line(Gold)", fontsize=15)
    plt.xticks(())
    plt.legend(loc='upper right')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()

    plt.show()

    return r_btc, r_gold


# 参数：买/卖比特币/黄金数目；比特币/黄金价格（四个数组）
def F(delta_btc, delta_gold, price_btc, price_gold):
    cycle = 10
    hold_cash = 1000
    hold_btc = 0
    hold_gold = 0

    for i in range(cycle):
        cost = 0.02 * delta_btc[i] + 0.01 * delta_gold[i]

        if (delta_gold[i] < 0) & (delta_gold[i] + hold_gold < 0):
            delta_gold[i] = -hold_gold
        elif (delta_btc[i] < 0) & (delta_btc[i] + hold_btc < 0):
            delta_btc[i] = -hold_btc
        elif cost > hold_cash:
            continue

        hold_btc += delta_btc[i]
        hold_gold += delta_gold[i]

        hold_cash -= delta_btc[i] * price_btc[i]
        hold_cash -= delta_gold[i] * price_gold[i]
        hold_cash -= cost

    hold_sum = hold_cash + hold_btc * price_btc[cycle - 1] + hold_gold * price_gold[cycle - 1]
    return hold_sum

# 给定 i 天 和 i 天之前的 14 天的数据，还有 i + 1 天的数据，计算最优决策
def modeling_best_vtc(price_gold, a = 0.01, windowsize=15):
    # 优先级：黄金 > 比特币
    # 优先级：买 > 卖

    a_gold = a

    dec = [0.4, 0.2, 0.1, 0, -0.1, -0.4, -0.9]
    best_vtc_gold = []
    best_vtc_total = []

    cash = 1800
    btc = 0
    gold = 0
    total = cash + btc * price_btc[0] + gold * price_gold[0]

    for i in range(0, len(price_btc) - 1):
        # 做判断时不用考虑组合
        # 计算实际值才考虑优先级
        price_gold_now = price_gold[i]
        price_gold_next = price_gold[i + 1]

        best_dec_gold = 3
        best_total = cash + gold * price_gold_next


        for i in range(0, len(dec), 1):
            # 买入过程
            if dec[i] > 0.01:
                buy_gold_cash = cash * dec[i]
                new_cash = cash - buy_gold_cash * (1 + a_gold)
                buy_gold = buy_gold_cash / price_gold_now
                new_gold = gold + buy_gold
                new_total = new_cash + new_gold * price_gold_next
                if new_total > best_total:
                    best_dec_gold = i
            elif dec[i] < 0.01:
                sell_gold = gold * dec[i]  # 负数
                new_gold = gold + sell_gold
                sell_gold_cash = sell_gold * price_gold_now  # 负数
                new_cash = cash - sell_gold_cash * (1 - a_gold)
                new_total = new_cash + new_gold * price_gold_next
                if new_total > best_total:
                    best_dec_gold = i


        # 根据最优决策更改Cash和Gold的状态

        best_vtc_gold.append(best_dec_gold)
        best_vtc_total.append(best_total)

        if dec[best_dec_gold] > 0:
            buy_gold_cash_best = cash * dec[best_dec_gold]
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best
        elif dec[best_dec_gold] < 0:
            sell_gold_best = gold * dec[best_dec_gold]  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)

        # print(cash, gold, best_dec_gold, best_total)


    return best_vtc_gold, best_vtc_total

# SMA5 - SMA15 / SMA5 模型求取决策结果
def modeling_stpuid(price_btc, price_gold, a_btc=0.02, a_gold=0.01):
    # 优先级：黄金 > 比特币
    # 优先级：买 > 卖

    d = {
        "比特币操作": [],
        "黄金操作": [],
        "现金": [],
        "比特币": [],
        "黄金": [],
        "比特币价格": [],
        "黄金价格": [],
        "资产总值": []
    }
    df1 = pd.DataFrame(d)

    for i in range(15):
        s1 = pd.Series(
            {
                "比特币操作": "不动",
                "黄金操作": "不动",
                "现金": 1000,
                "比特币": 0,
                "黄金": 0,
                "比特币价格": price_btc[i],
                "黄金价格": price_gold[i],
                "资产总值": 1000
            }
        )

        df1 = df1.append(s1, ignore_index=True)

    sma15_btc, sma15_gold = SMA(price_btc, price_gold, windowsize=15)
    sma5_btc, sma5_gold = SMA(price_btc, price_gold, windowsize=5)

    div_sma_btc = []
    div_sma_gold = []
    for i in range(len(sma15_btc)):
        div_sma_btc.append((sma5_btc[i] - sma15_btc[i]) / sma5_btc[i])
        div_sma_gold.append((sma5_gold[i] - sma15_gold[i]) / sma5_gold[i])

    print(len(div_sma_btc))
    print(len(div_sma_gold))

    p = 0.8
    np = -0.8
    m = 0.03
    cash = 1000
    btc = 0
    gold = 0

    t_his = []

    for i in range(0, len(div_sma_gold)):

        # 做判断时不用考虑组合
        # 计算实际值才考虑优先级
        price_gold_now = price_gold[i]
        price_btc_now = price_btc[i]

        gmove = "Gold不动 "
        bmove = "BTC不动 "

        if div_sma_btc[i] > m:
            bmove = "买BTC"
            buy_btc_cash_best = cash * p
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best
        elif div_sma_gold[i] < -m and btc != 0:
            bmove = "卖BTC"
            sell_btc_best = btc * np  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)

        if div_sma_gold[i] > m:
            gmove = "买Gold"
            buy_gold_cash_best = cash * p
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best
        elif div_sma_gold[i] < -m and gold != 0:
            gmove = "卖GOLD"
            sell_gold_best = gold * np  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        t_his.append(best_total)

        if btc < 10e-10:
            btc = 0
        if gold < 10e-8:
            gold = 0

        s1 = pd.Series(
            {
                "比特币操作": bmove,
                "黄金操作": gmove,
                "现金": cash,
                "比特币": btc,
                "黄金": gold,
                "比特币价格": price_btc_now,
                "黄金价格": price_gold_now,
                "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print(bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)

    df1.to_excel("../Data/MA_RESULT.xlsx", index=False)
    print(df1.head())
    print(df1.head(-1))
    # plt.figure()
    #
    # # 两行两列 第一个
    # plt.subplot(3, 1, 1)

    plt.plot(range(len(t_his)), t_his, c='#AACCFF', label="MA Model(2016.11 - 2018.11)")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()
    plt.show()

def modeling_ma(price_btc, price_gold, a_btc=0.02, a_gold=0.01, level=0):

    # bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total
    d = {
        "比特币操作": [],
        "黄金操作": [],
        "现金": [],
        "比特币": [],
        "黄金": [],
        "比特币价格": [],
        "黄金价格": [],
        "资产总值": []
    }
    df1 = pd.DataFrame(d)

    for i in range(9):
        s1 = pd.Series(
            {
                "比特币操作": "不动",
                "黄金操作": "不动",
                "现金": 1000,
                "比特币": 0,
                "黄金": 0,
                "比特币价格": price_btc[i],
                "黄金价格": price_gold[i],
                "资产总值": 1000
            }
        )

        df1 = df1.append(s1, ignore_index=True)


    dif_btc, dif_gold, macd_btc, macd_gold = MACD(price_btc, price_gold)

    mp = 0.25 # 0.25 - 24W
    ss = -0.25

    cash = 1000
    btc = 0
    gold = 0

    t_his = []

    dif_btc = dif_btc[9:]
    dif_gold = dif_gold[9:]

    print(len(dif_btc), len(macd_btc))
    for i in range(len(macd_btc) - 1):

        price_gold_now = price_gold[i + level]
        price_btc_now = price_btc[i + level]

        gmove = "不动"
        bmove = "不动"

        if dif_btc[i] > 0 and macd_btc[i] > 0:
            if dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best
            elif dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif dif_btc[i] < 0 and macd_btc[i] < 0:
            if dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
            elif dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best

        if dif_gold[i] > 0 and macd_gold[i] > 0:
            if dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best
            elif dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif dif_gold[i] < 0 and macd_gold[i] < 0:
            if dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
            elif dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        if btc < 10e-8:
            btc = 0
        if gold < 10e-6:
            gold = 0

        s1 = pd.Series(
            {
            "比特币操作": bmove,
            "黄金操作": gmove,
            "现金": cash,
            "比特币": btc,
            "黄金": gold,
            "比特币价格": price_btc_now,
            "黄金价格": price_gold_now,
            "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print(bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)

    df1.to_excel("../Data/MA_RESULT.xlsx", index=False)
    print(df1.head())
    print(df1.head(-1))


    plt.figure()

    ccc = "#FF1493"
    cc = "#FF69B4"
    # 两行两列 第一个
    plt.plot(range(len(t_his)), t_his, c=ccc, label="Total Assets")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.title("MA Model (2016.11 - 2021.11)")

    plt.show()


    # 两行两列 第一个
    plt.subplot(3, 1, 1)
    d = 365 * 2
    plt.plot(range(len(t_his[:d])), t_his[:d], c=cc, label="Total Assets (2016.11 - 2018.11)")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.subplot(3, 1, 2)
    d2 = 365 * 4
    plt.plot(range(len(t_his[d:d2])), t_his[d:d2], c=cc, label="Total Assets (2018.11 - 2020.11)")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.subplot(3, 1, 3)
    plt.plot(range(len(t_his[-d:])), t_his[-d:], c=cc, label="Total Assets (2020.11 - 2021.11)")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # print(t_his[360:365])
    # print(t_his[-5:])

    plt.show()

# （乱写的）
# 判断状态：大降(-3) 中降(-2) 小降(-1) 持平(0) 小涨(+1) 中涨(+2) 大涨(+3)
def rise_or_fall(price_btc, price_gold, date, windowsize):

    n = 5

    ma_btc_all = price_btc[date - windowsize: date].mean()
    ma_btc_part = price_btc[date - n: date].mean()
    rof_degree_btc = math.log(ma_btc_all / ma_btc_part)

    ma_gold_all = price_gold[date - windowsize: date].mean()
    ma_gold_part = price_gold[date - n: date].mean()
    rof_degree_gold = math.log(ma_gold_all / ma_gold_part)

    print(rof_degree_btc, rof_degree_gold)
    if price_btc[date] - price_btc[date - 1] > 50:
        b = 3
    elif price_btc[date] - price_btc[date - 1] > 25:
        b = 2
    elif price_btc[date] - price_btc[date - 1] > 5:
        b = 1
    elif price_btc[date] - price_btc[date - 1] > -5:
        b = 0
    elif price_btc[date] - price_btc[date - 1] > -25:
        b = -1
    elif price_btc[date] - price_btc[date - 1] > -50:
        b = -2
    else:
        b = -3

    if price_gold[date] - price_gold[date - 1] > 50:
        g = 3
    elif price_gold[date] - price_gold[date - 1] > 20:
        g = 2
    elif price_gold[date] - price_gold[date - 1] > 5:
        g = 1
    elif price_gold[date] - price_gold[date - 1] > -5:
        g = 0
    elif price_gold[date] - price_gold[date - 1] > -20:
        g = -1
    elif price_gold[date] - price_gold[date - 1] > -50:
        g = -2
    else:
        g = -3

    return b, g

# （乱写的）
# 判断状态：大卖(-3) 中卖(-2) 小卖(-1) 不动(0) 小买(+1) 中买(+2) 大买(+3)
def buy_or_sell(price_btc, price_gold, date, windowsize):
    return np.random.randint(-3, 4), np.random.randint(-3, 4)
    # return 1, 1
    # return rise_or_fall(price_btc, price_gold, date, windowsize)


def mu_ps(x, w=0.01):
    if (x >= 0) and (x <= 2 * w):
        return 1 - math.fabs(x - w) / w
    else:
        return 0

def mu_pm(x, w=0.01):
    if (x >= w) and (x <= 3 * w):
        return 1 - math.fabs(x - 2 * w) / w
    else:
        return 0

def mu_pl(x, w=0.01):
    if x >= 3 * w:
        return 1
    elif (x >= 2 * w) and (x <= 3 * w):
        return (x - 2 * w) / w
    else:
        return 0

def mu_ns(x, w=0.01):
    if (x >= -2 * w) and (x <= 0):
        return 1 - math.fabs(x + w) / w
    else:
        return 0

def mu_nm(x, w=0.01):
    if (x >= -3 * w) and (x <= -1 * w):
        return 1 - math.fabs(x + 2 * w) / w
    else:
        return 0

def mu_nl(x, w=0.01):
    if x <= -3 * w:
        return 1
    elif (x >= -3 * w) and (x <= -2 * w):
        return 1 - math.fabs(x + 3 * w) / w
    else:
        return 0

def mu_az(x, w=0.01):
    if (x >= -w) and (x <= w):
        return 1 - math.fabs(x) / w
    else:
        return 0

def ed_gold_f2y(x, w=0.01):
    a = -2 * w * mu_pl(x, w) - 2 * w * mu_pm(x, w) + 2 * w * mu_nl(x, w) + 2 * w * mu_nm(x, w)
    b = mu_pl(x, w) + mu_pm(x, w) + mu_nl(x, w) + mu_nm(x, w)
    if b == 0:
        return 0
    else:
        return a / b

def ed_btc_f2y(x, w=0.01):

    a = 4 * w * mu_pl(x, w) - 4 * w * mu_nl(x, w)
    b = mu_pl(x, w) + mu_nl(x, w)
    if b == 0:
        return 0
    else:
        return a / b

def ed_gold_f4y(x, w=0.01):
    a = 2 * w * mu_pm(x, w) + 2 * w * mu_ns(x, w) - 2 * w * mu_nl(x, w) + w * mu_ps(x, w) + w * mu_pm(x, w)
    b = mu_pm(x, w) + mu_ns(x, w) + mu_nl(x, w) + mu_ps(x, w) + mu_pm(x, w)
    if b == 0:
        return 0
    else:
        return a / b

def ed_btc_f4y(x, w=0.01):

    a = 4 * w * mu_pl(x, w) - 4 * w * mu_nl(x, w)
    b = mu_pl(x, w) + mu_nl(x, w)
    if b == 0:
        return 0
    else:
        return a / b




def modeling_ma_final(price_btc, price_gold, a_btc=0.02, a_gold=0.01):

    # bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total
    d = {
        "比特币操作": [],
        "黄金操作": [],
        "现金": [],
        "比特币": [],
        "黄金": [],
        "比特币价格": [],
        "黄金价格": [],
        "资产总值": []
    }
    df1 = pd.DataFrame(d)

    for i in range(9):
        s1 = pd.Series(
            {
                "比特币操作": "不动",
                "黄金操作": "不动",
                "现金": 1000,
                "比特币": 0,
                "黄金": 0,
                "比特币价格": price_btc[i],
                "黄金价格": price_gold[i],
                "资产总值": 1000
            }
        )

        df1 = df1.append(s1, ignore_index=True)


    dif_btc, dif_gold, macd_btc, macd_gold = MACD(price_btc, price_gold)

    cash = 1000
    btc = 0
    gold = 0

    t_his = []
    dif_btc = dif_btc[9:]
    dif_gold = dif_gold[9:]

    # print(len(dif_btc), len(macd_btc))

    ##### 1 - 2 Year    0 -- 2*365
    ##### 3 - 4 Year    2*365+1 -- 4*365
    ##### 5     Year    4*365+1 -- len(macd_btc) - 1

    level = 9
    mp = 0.25  # 0.25 - 24W
    ss = -0.25
    for i in range(0, 2*365):

        price_gold_now = price_gold[i + level]
        price_btc_now = price_btc[i + level]

        gmove = "不动"
        bmove = "不动"

        if dif_btc[i] > 0 and macd_btc[i] > 0:
            if dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best
            elif dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif dif_btc[i] < 0 and macd_btc[i] < 0:
            if dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
            elif dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best

        if dif_gold[i] > 0 and macd_gold[i] > 0:
            if dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best
            elif dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif dif_gold[i] < 0 and macd_gold[i] < 0:
            if dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
            elif dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        if btc < 10e-8:
            btc = 0
        if gold < 10e-6:
            gold = 0

        s1 = pd.Series(
            {
            "比特币操作": bmove,
            "黄金操作": gmove,
            "现金": cash,
            "比特币": btc,
            "黄金": gold,
            "比特币价格": price_btc_now,
            "黄金价格": price_gold_now,
            "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print("1", bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)


    ##### 3 - 4 Year    2*365+1 -- 4*365
    level = 0
    mp = 0.9  # 0.25 - 24W
    ss = -0.9
    for i in range(2 * 365 + 1, 4 * 365):

        price_gold_now = price_gold[i + level]
        price_btc_now = price_btc[i + level]

        gmove = "不动"
        bmove = "不动"

        if dif_btc[i] > 0 and macd_btc[i] > 0:
            if dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best
            elif dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif dif_btc[i] < 0 and macd_btc[i] < 0:
            if dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
            elif dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best

        if dif_gold[i] > 0 and macd_gold[i] > 0:
            if dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best
            elif dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif dif_gold[i] < 0 and macd_gold[i] < 0:
            if dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
            elif dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        if btc < 10e-8:
            btc = 0
        if gold < 10e-6:
            gold = 0

        s1 = pd.Series(
            {
                "比特币操作": bmove,
                "黄金操作": gmove,
                "现金": cash,
                "比特币": btc,
                "黄金": gold,
                "比特币价格": price_btc_now,
                "黄金价格": price_gold_now,
                "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print("2", bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)


    ##### 5     Year    4*365+1 -- len(macd_btc) - 1
    level = 0
    mp = 0.95  # 0.25 - 24W
    ss = -0.95
    for i in range(4*365+1, len(macd_btc)-1):

        price_gold_now = price_gold[i + level]
        price_btc_now = price_btc[i + level]

        gmove = "不动"
        bmove = "不动"

        if dif_btc[i] > 0 and macd_btc[i] > 0:
            if dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best
            elif dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif dif_btc[i] < 0 and macd_btc[i] < 0:
            if dif_btc[i + 1] < dif_btc[i] and macd_btc[i + 1] < macd_btc[i] and btc > 0:
                bmove = "卖"
                sell_btc_best = btc * ss  # 负数
                btc = btc + sell_btc_best
                sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
                cash = cash - sell_btc_cash_best * (1 - a_btc)
            elif dif_btc[i + 1] > dif_btc[i] and macd_btc[i + 1] > macd_btc[i] and cash > 10:
                bmove = "买"
                buy_btc_cash_best = cash * mp
                cash = cash - buy_btc_cash_best * (1 + a_btc)
                buy_btc_best = buy_btc_cash_best / price_btc_now
                btc = btc + buy_btc_best

        if dif_gold[i] > 0 and macd_gold[i] > 0:
            if dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best
            elif dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif dif_gold[i] < 0 and macd_gold[i] < 0:
            if dif_gold[i + 1] < dif_gold[i] and macd_gold[i + 1] < macd_gold[i] and gold > 0:
                gmove = "卖"
                sell_gold_best = gold * ss  # 负数
                gold = gold + sell_gold_best
                sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
                cash = cash - sell_gold_cash_best * (1 - a_gold)
            elif dif_gold[i + 1] > dif_gold[i] and macd_gold[i + 1] > macd_gold[i] and cash > 10:
                gmove = "买"
                buy_gold_cash_best = cash * mp
                cash = cash - buy_gold_cash_best * (1 + a_gold)
                buy_gold_best = buy_gold_cash_best / price_gold_now
                gold = gold + buy_gold_best

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        if btc < 10e-8:
            btc = 0
        if gold < 10e-6:
            gold = 0

        s1 = pd.Series(
            {
                "比特币操作": bmove,
                "黄金操作": gmove,
                "现金": cash,
                "比特币": btc,
                "黄金": gold,
                "比特币价格": price_btc_now,
                "黄金价格": price_gold_now,
                "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print("3",bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)



    df1.to_excel("../Data/MA_RESULT.xlsx", index=False)
    # print(df1.head())
    print(df1.head(-1))


    # plt.figure()
    #
    # ccc = "#FF1493"
    # cc = "#FF69B4"
    # # 两行两列 第一个
    # plt.plot(range(len(t_his)), t_his, c=ccc, label="Total Assets")
    # plt.xticks(())
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.show()
    #
    # # 两行两列 第一个
    # plt.subplot(3, 1, 1)
    # d = 365 * 2
    # plt.plot(range(len(t_his[:d])), t_his[:d], c=cc, label="Total Assets")
    # plt.xticks(())
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.title("Stage I (2016.9 - 2018.9)")
    #
    # plt.subplot(3, 1, 2)
    # d2 = 365 * 4
    # plt.plot(range(len(t_his[d:d2])), t_his[d:d2], c=cc, label="Total Assets")
    # plt.xticks(())
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.title("Stage II (2018.9 - 2020.9)")
    #
    # plt.subplot(3, 1, 3)
    # plt.plot(range(len(t_his[-d:])), t_his[-d:], c=cc, label="Total Assets")
    # plt.xticks(())
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.title("Stage III (2020.9 - 2021.9)")
    #
    # # print(t_his[360:365])
    # # print(t_his[-5:])

    # plt.show()




# 判断状态：大降(-3) 中降(-2) 小降(-1) 持平(0) 小涨(+1) 中涨(+2) 大涨(+3)
# 每一天都有，0 - 14 天为全 0 返回 btc, gold
def modeling_rof_vtc(price_btc, price_gold, windowsize=15):

    n = 5

    length = len(price_btc)

    # x_{1,t}^{(m,n)}
    rof_degree_btcs = []
    rof_degree_golds = []

    for i in range(windowsize):
        rof_degree_btcs.append(0)
        rof_degree_golds.append(0)

    for date in range(windowsize, length):
        ma_btc_all = price_btc[date - windowsize: date].mean()
        ma_btc_part = price_btc[date - n: date].mean()
        rof_degree_btcs.append(math.log(ma_btc_all / ma_btc_part))

        ma_gold_all = price_gold[date - windowsize: date].mean()
        ma_gold_part = price_gold[date - n: date].mean()
        rof_degree_golds.append(math.log(ma_gold_all / ma_gold_part))

    # plt.plot(range(length), rof_degree_btcs, label='Bitcoin', c='#AADDFF')
    # plt.plot(range(length), rof_degree_golds, label='Gold', c='#DDAAFF')
    # plt.title(r"$\ln(MA_m / MA_n)$", fontsize=20)
    # plt.xticks(())
    # plt.legend()
    # plt.show()

    w = 0.01

    # 1
    mu_ps_btcs = []
    mu_ps_golds = []

    for i in range(len(rof_degree_golds)):
        x = rof_degree_btcs[i]
        if(x >= 0) and (x <= 2 * w):
            mu_ps_btcs.append(1 - math.fabs(x - w) / w)
        else:
            mu_ps_btcs.append(0)

        x = rof_degree_golds[i]
        if (x >= 0) and (x <= 2 * w):
            mu_ps_golds.append(1 - math.fabs(x - w) / w)
        else:
            mu_ps_golds.append(0)

    # 2
    mu_pm_btcs = []
    mu_pm_golds = []

    for i in range(len(rof_degree_golds)):
        x = rof_degree_btcs[i]
        if(x >= w) and (x <= 3 * w):
            mu_pm_btcs.append(1 - math.fabs(x - 2 * w) / w)
        else:
            mu_pm_btcs.append(0)

        x = rof_degree_golds[i]
        if (x >= w) and (x <= 3 * w):
            mu_pm_golds.append(1 - math.fabs(x - 2 * w) / w)
        else:
            mu_pm_golds.append(0)

    # 3
    mu_pl_btcs = []
    mu_pl_golds = []

    for i in range(len(rof_degree_golds)):
        x = rof_degree_btcs[i]
        if x >= 3 * w:
            mu_pl_btcs.append(1)
        elif (x >= 2 * w) and (x <= 3 * w):
            mu_pl_btcs.append((x - 2 * w) / w)
        else:
            mu_pl_btcs.append(0)

        x = rof_degree_golds[i]
        if x >= 3 * w:
            mu_pl_golds.append(1)
        elif (x >= 2 * w) and (x <= 3 * w):
            mu_pl_golds.append((x - 2 * w) / w)
        else:
            mu_pl_golds.append(0)

    # 4
    mu_ns_btcs = []
    mu_ns_golds = []

    for i in range(len(rof_degree_golds)):
        x = rof_degree_btcs[i]
        if(x >= -2 * w) and (x <= 0):
            mu_ns_btcs.append(1 - math.fabs(x + w) / w)
        else:
            mu_ns_btcs.append(0)

        x = rof_degree_golds[i]
        if (x >= -2 * w) and (x <= 0):
            mu_ns_golds.append(1 - math.fabs(x + w) / w)
        else:
            mu_ns_golds.append(0)

    # 5
    mu_nm_btcs = []
    mu_nm_golds = []

    for i in range(len(rof_degree_golds)):
        x = rof_degree_btcs[i]
        if(x >= -3 * w) and (x <= -1 * w):
            mu_nm_btcs.append(1 - math.fabs(x + 2 * w) / w)
        else:
            mu_nm_btcs.append(0)

        x = rof_degree_golds[i]
        if (x >= -3 * w) and (x <= -1 * w):
            mu_nm_golds.append(1 - math.fabs(x + 2 * w) / w)
        else:
            mu_nm_golds.append(0)

    # 6
    mu_nl_btcs = []
    mu_nl_golds = []

    for i in range(len(rof_degree_golds)):
        x = rof_degree_btcs[i]
        if x <= -3 * w:
            mu_nl_btcs.append(1)
        elif (x >= -3 * w) and (x <= -2 * w):
            mu_nl_btcs.append(1 - math.fabs(x + 3 * w) / w)
        else:
            mu_nl_btcs.append(0)

        x = rof_degree_golds[i]
        if x <= -3 * w:
            mu_nl_golds.append(1)
        elif (x >= -3 * w) and (x <= -2 * w):
            mu_nl_golds.append(1 - math.fabs(x + 3 * w) / w)
        else:
            mu_nl_golds.append(0)

    # 7
    mu_az_btcs = []
    mu_az_golds = []

    for i in range(len(rof_degree_golds)):
        x =rof_degree_btcs[i]
        if(x >= -w) and (x <= w):
            mu_az_btcs.append(1 - math.fabs(x) / w)
        else:
            mu_az_btcs.append(0)

        x = rof_degree_golds[i]
        if (x >= -w) and (x <= w):
            mu_az_golds.append(1 - math.fabs(x) / w)
        else:
            mu_az_golds.append(0)


    a_in_vec_btc = np.zeros((len(mu_ps_btcs), 7))
    a_in_vec_gold = np.zeros((len(mu_ps_golds), 7))

    for i in range(len(mu_ps_btcs)):
        a_in_vec_btc[i, 0] = mu_nl_btcs[i]
        a_in_vec_btc[i, 1] = mu_nm_btcs[i]
        a_in_vec_btc[i, 2] = mu_ns_btcs[i]
        a_in_vec_btc[i, 3] = mu_az_btcs[i]
        a_in_vec_btc[i, 4] = mu_ps_btcs[i]
        a_in_vec_btc[i, 5] = mu_pm_btcs[i]
        a_in_vec_btc[i, 6] = mu_pl_btcs[i]

        a_in_vec_gold[i, 0] = mu_nl_golds[i]
        a_in_vec_gold[i, 1] = mu_nm_golds[i] 
        a_in_vec_gold[i, 2] = mu_ns_golds[i]
        a_in_vec_gold[i, 3] = mu_az_golds[i]
        a_in_vec_gold[i, 4] = mu_ps_golds[i]
        a_in_vec_gold[i, 5] = mu_pm_golds[i]
        a_in_vec_gold[i, 6] = mu_pl_golds[i]

    # length = 100
    # plt.figure()
    #
    # # 两行两列 第一个
    # plt.subplot(2, 1, 1)
    # plt.plot(range(length), mu_ps_btcs[:length], label='PS', c='#800000')
    # plt.plot(range(length), mu_pm_btcs[:length], label='PM', c='#B22222')
    # plt.plot(range(length), mu_pl_btcs[:length], label='PL', c='#FF0000')
    #
    # plt.plot(range(length), mu_ns_btcs[:length], label='NS', c='#0000CD')
    # plt.plot(range(length), mu_nm_btcs[:length], label='NM', c='#1E90EF')
    # plt.plot(range(length), mu_nl_btcs[:length], label='NL', c='#00BFFF')
    #
    # plt.plot(range(length), mu_az_btcs[:length], label='AZ', c='#333333')
    # plt.xticks(())
    # plt.xlabel("Date")
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.grid()
    # plt.title(f"Fuzzy set of price fluctuation(Bitcoin), $\omega = 0.01$", fontsize=20)
    #
    # plt.subplot(2, 1, 2)
    # plt.plot(range(length), mu_ps_golds[:length], label='PS', c='#800000')
    # plt.plot(range(length), mu_pm_golds[:length], label='PM', c='#B22222')
    # plt.plot(range(length), mu_pl_golds[:length], label='PL', c='#FF0000')
    #
    # plt.plot(range(length), mu_ns_golds[:length], label='NS', c='#0000CD')
    # plt.plot(range(length), mu_nm_golds[:length], label='NM', c='#1E90EF')
    # plt.plot(range(length), mu_nl_golds[:length], label='NL', c='#00BFFF')
    #
    # plt.plot(range(length), mu_az_golds[:length], label='AZ', c='#333333')
    # plt.xticks(())
    # plt.xlabel("Date")
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.grid()
    # plt.title(f"Fuzzy set of price fluctuation(Gold), $\omega = 0.01$", fontsize=20)
    #
    # plt.show()

    return a_in_vec_btc, a_in_vec_gold

# 最后一天没有，返回 btc, gold
# 判断状态：大卖(-3) 中卖(-2) 小卖(-1) 不动(0) 小买(+1) 中买(+2) 大买(+3)
def modeling_bos_vtc(price_btc, price_gold):

    length = len(price_btc)

    ed_btc = []
    ed_gold = []

    for i in range(length - 1):
        ed_btc.append((price_btc[i + 1] - price_btc[i]) / price_btc[i])
        ed_gold.append((price_gold[i + 1] - price_gold[i]) / price_gold[i])

    bos_vec_btc = []
    bos_vec_gold = []

    for i in range(length - 1):
        bos_vec_btc.append(compute_bos_vtc(ed_btc[i]))
        bos_vec_gold.append(compute_bos_vtc(ed_gold[i]))

    print(bos_vec_gold[:10])
    print(bos_vec_btc[:10])

    mu_bb_btcs = []
    mu_bm_btcs = []
    mu_bs_btcs = []
    mu_n_btcs = []
    mu_ss_btcs = []
    mu_sm_btcs = []
    mu_sb_btcs = []

    for i in range(length - 1):
        mu_bb_btcs.append(bos_vec_btc[i][0])
        mu_bm_btcs.append(bos_vec_btc[i][1])
        mu_bs_btcs.append(bos_vec_btc[i][2])
        mu_n_btcs.append(bos_vec_btc[i][3])
        mu_ss_btcs.append(bos_vec_btc[i][4])
        mu_sm_btcs.append(bos_vec_btc[i][5])
        mu_sb_btcs.append(bos_vec_btc[i][6])


    mu_bb_golds = []
    mu_bm_golds = []
    mu_bs_golds = []
    mu_n_golds = []
    mu_ss_golds = []
    mu_sm_golds = []
    mu_sb_golds = []

    for i in range(length - 1):
        mu_bb_golds.append(bos_vec_gold[i][0])
        mu_bm_golds.append(bos_vec_gold[i][1])
        mu_bs_golds.append(bos_vec_gold[i][2])
        mu_n_golds.append(bos_vec_gold[i][3])
        mu_ss_golds.append(bos_vec_gold[i][4])
        mu_sm_golds.append(bos_vec_gold[i][5])
        mu_sb_golds.append(bos_vec_gold[i][6])

    # length = 100
    # plt.figure()
    # # 两行两列 第一个
    # plt.subplot(2, 1, 1)
    # plt.plot(range(length), mu_bs_btcs[:length], label='BS', c='#800000')
    # plt.plot(range(length), mu_bm_btcs[:length], label='BM', c='#B22222')
    # plt.plot(range(length), mu_bb_btcs[:length], label='BB', c='#FF0000')
    #
    # plt.plot(range(length), mu_ss_btcs[:length], label='SS', c='#0000CD')
    # plt.plot(range(length), mu_sm_btcs[:length], label='SM', c='#1E90EF')
    # plt.plot(range(length), mu_sb_btcs[:length], label='SB', c='#00BFFF')
    #
    # plt.plot(range(length), mu_n_btcs[:length], label='N', c='#333333')
    # plt.xticks(())
    # plt.xlabel("Date")
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.grid()
    # plt.title(f"Fuzzy set of Buy&Sell(Bitcoin)", fontsize=20)
    #
    # plt.subplot(2, 1, 2)
    # plt.plot(range(length), mu_bs_golds[:length], label='BS', c='#800000')
    # plt.plot(range(length), mu_bm_golds[:length], label='BM', c='#B22222')
    # plt.plot(range(length), mu_bb_golds[:length], label='BB', c='#FF0000')
    #
    # plt.plot(range(length), mu_ss_golds[:length], label='SS', c='#0000CD')
    # plt.plot(range(length), mu_sm_golds[:length], label='SM', c='#1E90EF')
    # plt.plot(range(length), mu_sb_golds[:length], label='SB', c='#00BFFF')
    #
    # plt.plot(range(length), mu_n_golds[:length], label='N', c='#333333')
    # plt.xticks(())
    # plt.xlabel("Date")
    # plt.legend(loc='upper left')
    # ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.grid()
    # plt.title(f"Fuzzy set of Buy&Sell(Gold)", fontsize=20)
    #
    # plt.show()

    return bos_vec_btc, bos_vec_gold

def nhsyl(file):
    df = pd.read_excel(file)
    # print(df.shape[0], df.index)
    day = df.shape[0] - 1
    money = df.loc[day, "资产总值"]
    print(((money - 1000) / 1000) / (day / 365) * 100)

def RSquard(price_btc, price_gold, windowsize=15, n=5, y=2):
    length = len(price_btc)
    ed_btc = []
    ed_gold = []

    for i in range(length - 1):
        ed_btc.append((price_btc[i + 1] - price_btc[i]) / price_btc[i])
        ed_gold.append((price_gold[i + 1] - price_gold[i]) / price_gold[i])

    print(ed_btc[:10])
    rof_degree_btcs = []
    rof_degree_golds = []

    for i in range(windowsize):
        rof_degree_btcs.append(0)
        rof_degree_golds.append(0)

    for date in range(windowsize, length):
        ma_btc_all = price_btc[date - windowsize: date].mean()
        ma_btc_part = price_btc[date - n: date].mean()
        rof_degree_btcs.append(math.log(ma_btc_all / ma_btc_part))

        ma_gold_all = price_gold[date - windowsize: date].mean()
        ma_gold_part = price_gold[date - n: date].mean()
        rof_degree_golds.append(math.log(ma_gold_all / ma_gold_part))

    ed_btc_a = []
    ed_gold_a = []
    ed_btc_a = ed_btc_a[-366:]
    ed_gold_a = ed_gold_a[-366:]

    if y == 2:
        for i in range(length - 1):
            ed_btc_a.append(ed_btc_f2y(rof_degree_btcs[i]))
            ed_gold_a.append(ed_gold_f2y(rof_degree_golds[i]))
    else:
        for i in range(length - 1):
            ed_btc_a.append(ed_btc_f4y(rof_degree_btcs[i]))
            ed_gold_a.append(ed_gold_f4y(rof_degree_golds[i]))

    var_ed_btc = np.array(ed_btc[-365: -1]).std() ** 2
    var_ed_gold = np.array(ed_gold[-365: -1]).std() ** 2


    sum_btc = 0
    sum_gold = 0
    for i in range(len(ed_btc_a)):
        sum_btc += (ed_btc_a[i]  - ed_btc[i]) ** 2
        sum_gold += (ed_gold_a[i] - ed_gold[i]) ** 2

    r2_btc = 1 - sum_btc / var_ed_btc
    r2_gold = 1 - sum_gold / var_ed_gold

    print("BTC")
    print(ed_btc)
    print(ed_btc_a)

    print("GOLD")
    print(ed_gold)
    print(ed_gold_a)

    print(sum_btc, sum_gold)
    print(var_ed_btc, var_ed_gold)
    print(r2_btc, r2_gold)

def testing_bos_vtc(price_btc, price_gold, windowsize=15, y = 2):
    n = 5

    length = len(price_btc)

    # x_{1,t}^{(m,n)}
    rof_degree_btcs = []
    rof_degree_golds = []

    for i in range(windowsize):
        rof_degree_btcs.append(0)
        rof_degree_golds.append(0)

    for date in range(windowsize, length):
        ma_btc_all = price_btc[date - windowsize: date].mean()
        ma_btc_part = price_btc[date - n: date].mean()
        rof_degree_btcs.append(math.log(ma_btc_all / ma_btc_part))

        ma_gold_all = price_gold[date - windowsize: date].mean()
        ma_gold_part = price_gold[date - n: date].mean()
        rof_degree_golds.append(math.log(ma_gold_all / ma_gold_part))

    length = len(price_btc)

    ed_btc = []
    ed_gold = []

    if y == 2:
        for i in range(length - 1):
            ed_btc.append(ed_btc_f2y(rof_degree_btcs[i]))
            ed_gold.append(ed_gold_f2y(rof_degree_golds[i]))
    else:
        for i in range(length - 1):
            ed_btc.append(ed_btc_f4y(rof_degree_btcs[i]))
            ed_gold.append(ed_gold_f4y(rof_degree_golds[i]))

    # print("ED_BTC", ed_btc[:10])
    # print("ED_GOLD", ed_gold[:10])

    bos_vec_btc = []
    bos_vec_gold = []

    for i in range(length - 1):
        bos_vec_btc.append(compute_bos_vtc(ed_btc[i]))
        bos_vec_gold.append(compute_bos_vtc(ed_gold[i]))

    # print(bos_vec_gold[:10])
    # print(bos_vec_btc[:10])

    mu_bb_btcs = []
    mu_bm_btcs = []
    mu_bs_btcs = []
    mu_n_btcs = []
    mu_ss_btcs = []
    mu_sm_btcs = []
    mu_sb_btcs = []

    for i in range(length - 1):
        mu_bb_btcs.append(bos_vec_btc[i][0])
        mu_bm_btcs.append(bos_vec_btc[i][1])
        mu_bs_btcs.append(bos_vec_btc[i][2])
        mu_n_btcs.append(bos_vec_btc[i][3])
        mu_ss_btcs.append(bos_vec_btc[i][4])
        mu_sm_btcs.append(bos_vec_btc[i][5])
        mu_sb_btcs.append(bos_vec_btc[i][6])

    mu_bb_golds = []
    mu_bm_golds = []
    mu_bs_golds = []
    mu_n_golds = []
    mu_ss_golds = []
    mu_sm_golds = []
    mu_sb_golds = []

    for i in range(length - 1):
        mu_bb_golds.append(bos_vec_gold[i][0])
        mu_bm_golds.append(bos_vec_gold[i][1])
        mu_bs_golds.append(bos_vec_gold[i][2])
        mu_n_golds.append(bos_vec_gold[i][3])
        mu_ss_golds.append(bos_vec_gold[i][4])
        mu_sm_golds.append(bos_vec_gold[i][5])
        mu_sb_golds.append(bos_vec_gold[i][6])

    length = len(mu_bb_btcs)
    plt.figure()
    # 两行两列 第一个
    plt.subplot(2, 1, 1)
    plt.plot(range(length), mu_bs_btcs[:length], label='BS', c='#800000')
    plt.plot(range(length), mu_bm_btcs[:length], label='BM', c='#B22222')
    plt.plot(range(length), mu_bb_btcs[:length], label='BB', c='#FF0000')

    plt.plot(range(length), mu_ss_btcs[:length], label='SS', c='#0000CD')
    plt.plot(range(length), mu_sm_btcs[:length], label='SM', c='#1E90EF')
    plt.plot(range(length), mu_sb_btcs[:length], label='SB', c='#00BFFF')

    # plt.plot(range(length), mu_n_btcs[:length], label='N', c='#333333')
    plt.xticks(())
    plt.xlabel("Date")
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()
    plt.title(f"Fuzzy set of Buy&Sell(Bitcoin)", fontsize=20)

    plt.subplot(2, 1, 2)
    plt.plot(range(length), mu_bs_golds[:length], label='BS', c='#800000')
    plt.plot(range(length), mu_bm_golds[:length], label='BM', c='#B22222')
    plt.plot(range(length), mu_bb_golds[:length], label='BB', c='#FF0000')

    plt.plot(range(length), mu_ss_golds[:length], label='SS', c='#0000CD')
    plt.plot(range(length), mu_sm_golds[:length], label='SM', c='#1E90EF')
    plt.plot(range(length), mu_sb_golds[:length], label='SB', c='#00BFFF')

    # plt.plot(range(length), mu_n_golds[:length], label='N', c='#333333')
    plt.xticks(())
    plt.xlabel("Date")
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()
    plt.title(f"Fuzzy set of Buy&Sell(Gold)", fontsize=20)

    plt.show()

    return bos_vec_btc, bos_vec_gold


def compute_bos_vtc(ed):
    b = 0.01
    mu_bb = 0
    if ed >= 4 * b:
        mu_bb = 1
    elif ed >= 2 * b and ed <= 4 * b:
        mu_bb = (ed - 2 * b) / 2 * b

    mu_bm = 0
    if ed >= 1 * b and ed <= 2 * b:
        mu_bm = (ed - b) / b
    elif ed >= 2 * b and ed <= 4 * b:
        mu_bm = (4 * b - ed) / 2 * b

    mu_bs = 0
    if ed >= 0 and ed <= 1 * b:
        mu_bs = ed / b
    elif ed >= 1 * b and ed <= 2 * b:
        mu_bs = (2 * b - ed) / b

    mu_n = 0
    if ed >= -1 * b and ed <= 1 * b:
        mu_n = 1 - math.fabs(ed) / b

    mu_ss = 0
    if ed >= -1 * b and ed <= 0:
        mu_ss = -ed / 1 * b
    elif ed >= -2 * b and ed <= -1 * b:
        mu_ss = (2 * b + ed) / b

    mu_sm = 0
    if ed >= -2 * b and ed <= -1 * b:
        mu_sm = (-ed - b) / b
    elif ed >= -4 * b and ed <= -2 * b:
        mu_sm = (4 * b + ed) / 2 * b

    mu_sb = 0
    if ed <= -4 * b:
        mu_sb = 1
    elif ed >= -4 * b and ed <= -2 * b:
        mu_sb = (-2 * b - ed) / 2 * b

    # res = np.array((
    #     mu_bb,
    #     mu_bm,
    #     mu_bs,
    #     mu_n,
    #     mu_ss,
    #     mu_sm,
    #     mu_sb
    # ))
    res = [
        mu_bb,
        mu_bm,
        mu_bs,
        mu_n,
        mu_ss,
        mu_sm,
        mu_sb
    ]
    # print(res)
    return res

def compute_bos_vtc(ed):
    b = 0.01
    mu_bb = 0
    if ed >= 4 * b:
        mu_bb = 1
    elif ed >= 2 * b and ed <= 4 * b:
        mu_bb = (ed - 2 * b) / 2 * b

    mu_bm = 0
    if ed >= 1 * b and ed <= 2 * b:
        mu_bm = (ed - b) / b
    elif ed >= 2 * b and ed <= 4 * b:
        mu_bm = (4 * b - ed) / 2 * b

    mu_bs = 0
    if ed >= 0 and ed <= 1 * b:
        mu_bs = ed / b
    elif ed >= 1 * b and ed <= 2 * b:
        mu_bs = (2 * b - ed) / b

    mu_n = 0
    if ed >= -1 * b and ed <= 1 * b:
        mu_n = 1 - math.fabs(ed) / b

    mu_ss = 0
    if ed >= -1 * b and ed <= 0:
        mu_ss = -ed / 1 * b
    elif ed >= -2 * b and ed <= -1 * b:
        mu_ss = (2 * b + ed) / b

    mu_sm = 0
    if ed >= -2 * b and ed <= -1 * b:
        mu_sm = (-ed - b) / b
    elif ed >= -4 * b and ed <= -2 * b:
        mu_sm = (4 * b + ed) / 2 * b

    mu_sb = 0
    if ed <= -4 * b:
        mu_sb = 1
    elif ed >= -4 * b and ed <= -2 * b:
        mu_sb = (-2 * b - ed) / 2 * b

    # res = np.array((
    #     mu_bb,
    #     mu_bm,
    #     mu_bs,
    #     mu_n,
    #     mu_ss,
    #     mu_sm,
    #     mu_sb
    # ))
    res = [
        mu_bb,
        mu_bm,
        mu_bs,
        mu_n,
        mu_ss,
        mu_sm,
        mu_sb
    ]
    # print(res)
    return res

# 建立目标决策图（未完成）
def build_bncmap(price_btc, price_gold, windowsize = 15):
    length = len(price_btc)
    bos_btc = np.zeros(length)
    bos_gold = np.zeros(length)
    rof_btc = np.zeros(length)
    rof_gold = np.zeros(length)

    # 滑动窗口
    for i in range(windowsize, length):
        bos_btc[i], bos_gold[i] = buy_or_sell(price_btc, price_gold, i, windowsize)
        rof_btc[i], rof_gold[i] = rise_or_fall(price_btc, price_gold, i, windowsize)

    # print(rof_btc)
    # print(rof_gold)

    # 取众数
    bnc_btc_count = np.zeros((7, 7, 7))
    bnc_gold_count = np.zeros((7, 7, 7))
    for i in range(length):
        bnc_btc_count[int(rof_btc[i] + 3), int(rof_gold[i] + 3), int(bos_btc[i] + 3)] += 1
        bnc_gold_count[int(rof_btc[i] + 3), int(rof_gold[i] + 3), int(bos_gold[i] + 3)] += 1

    # print(bnc_btc_count)
    # print(bnc_gold_count)

    bnc_map = []
    bnc_vec_btc = []
    bnc_vec_gold = []
    for i in range(7):
        bnc_map_i = []
        for j in range(7):
            k = bnc_btc_count[i, j].argmax() - 3
            l = bnc_gold_count[i, j].argmax() - 3
            b1 = (bnc_btc_count[i, j] == bnc_btc_count[i, j, 0]).all()
            b2 = (bnc_gold_count[i, j] == bnc_gold_count[i, j, 0]).all()

            if b1 and b2:
                bnc_map_i.append((0, 0))
                bnc_vec_btc.append(0)
                bnc_vec_gold.append(0)
            elif b1:
                bnc_map_i.append((0, l))
                bnc_vec_btc.append(0)
                bnc_vec_gold.append(l)
            elif b2:
                bnc_map_i.append((k, 0))
                bnc_vec_btc.append(k)
                bnc_vec_gold.append(0)
            else:
                bnc_map_i.append((k, l))
                bnc_vec_btc.append(k)
                bnc_vec_gold.append(l)

        bnc_map.append(bnc_map_i)

    return bnc_map, bnc_vec_btc, bnc_vec_gold

# 显示目标决策图（未完成）
def show_img(vec_btc, vec_gold):

    img_btc = np.array(vec_btc).reshape(7, 7)
    img_btc = np.flip(img_btc, 1)
    img_gold = np.array(vec_gold).reshape(7, 7)
    img_gold = np.flip(img_gold, 1)

    plt.figure()

    # 两行两列 第一个
    plt.subplot(1, 2, 1)
    plt.imshow(img_btc, interpolation='nearest', origin='upper')
    plt.colorbar(shrink=0.6, label='Sell - Buy')
    plt.title("Decision Map of Bitcoin", fontsize=20)
    plt.xlabel("Bitcoin: Fall & Rise", fontsize=15)
    plt.ylabel("Gold: Fall & Rise", fontsize=15)
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Fall III', 'Fall II', 'Fall I', 'Stay', 'Rise I', 'Rise II', 'Rise III'])
    plt.yticks([0, 1, 2, 3, 4, 5, 6], ['Rise III', 'Rise II', 'Rise I', 'Stay', 'Fall I', 'Fall II', 'Fall III'])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')

    plt.subplot(1, 2, 2)
    plt.imshow(img_gold, interpolation='nearest', origin='upper')
    plt.colorbar(shrink=0.6, label='Sell - Buy')
    plt.title("Decision Map of Gold", fontsize=20)
    plt.xlabel("Bitcoin: Fall & Rise", fontsize=15)
    plt.ylabel("Gold: Fall & Rise", fontsize=15)
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Fall III', 'Fall II', 'Fall I', 'Stay', 'Rise I', 'Rise II', 'Rise III'])
    plt.yticks([0, 1, 2, 3, 4, 5, 6], ['Rise III', 'Rise II', 'Rise I', 'Stay', 'Fall I', 'Fall II', 'Fall III'])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')

    plt.show()

# 生成 Apriori 算法输入
def get_a_input(l_in, l_out, file):
    res = []
    for i in range(15, len(l_out)):
        series = []
        if l_in[i][0] != 0:
            series.append("NL")
        if l_in[i][1] != 0:
            series.append("NM")
        if l_in[i][2] != 0:
            series.append("NS")
        if l_in[i][3] != 0:
            series.append("AZ")
        if l_in[i][4] != 0:
            series.append("PS")
        if l_in[i][5] != 0:
            series.append("PM")
        if l_in[i][6] != 0:
            series.append("PL")

        if l_out[i][0] != 0:
            series.append("BB")
        if l_out[i][1] != 0:
            series.append("BM")
        if l_out[i][2] != 0:
            series.append("BS")
        if l_out[i][3] != 0:
            series.append("N")
        if l_out[i][4] != 0:
            series.append("SS")
        if l_out[i][5] != 0:
            series.append("SM")
        if l_out[i][6] != 0:
            series.append("SB")

        if ("N" not in series) and ("AZ" not in series):
            res.append(series)

    # print(res[:5])
    df1 = pd.DataFrame(res)
    print(df1.head(), df1.shape)

    df1.to_csv(file, index=False)

# 生成 Apriori 算法输入
def get_a_input_nmnl(l_in, l_out, file):
    res = []
    for i in range(15, len(l_out)):
        series = []
        if l_in[i][0] != 0:
            series.append("NL")
        if l_in[i][1] != 0:
            series.append("NM")
        if l_in[i][2] != 0:
            series.append("NS")
        if l_in[i][3] != 0:
            series.append("AZ")
        if l_in[i][4] != 0:
            series.append("PS")
        if l_in[i][5] != 0:
            series.append("PM")
        if l_in[i][6] != 0:
            series.append("PL")

        if l_out[i][0] != 0:
            series.append("BB")
        if l_out[i][1] != 0:
            series.append("BM")
        if l_out[i][2] != 0:
            series.append("BS")
        if l_out[i][3] != 0:
            series.append("N")
        if l_out[i][4] != 0:
            series.append("SS")
        if l_out[i][5] != 0:
            series.append("SM")
        if l_out[i][6] != 0:
            series.append("SB")

        if ("N" not in series) and ("AZ" not in series):
            if("NM" in series) or ("NL" in series):
                res.append(series)

    # print(res[:5])
    df1 = pd.DataFrame(res)
    print(df1.head(), df1.shape)

    df1.to_csv(file, index=False)

# 生成 Apriori 算法输入
def get_a_input_pmpl(l_in, l_out, file):
    res = []
    for i in range(15, len(l_out)):
        series = []
        if l_in[i][0] != 0:
            series.append("NL")
        if l_in[i][1] != 0:
            series.append("NM")
        if l_in[i][2] != 0:
            series.append("NS")
        if l_in[i][3] != 0:
            series.append("AZ")
        if l_in[i][4] != 0:
            series.append("PS")
        if l_in[i][5] != 0:
            series.append("PM")
        if l_in[i][6] != 0:
            series.append("PL")

        if l_out[i][0] != 0:
            series.append("BB")
        if l_out[i][1] != 0:
            series.append("BM")
        if l_out[i][2] != 0:
            series.append("BS")
        if l_out[i][3] != 0:
            series.append("N")
        if l_out[i][4] != 0:
            series.append("SS")
        if l_out[i][5] != 0:
            series.append("SM")
        if l_out[i][6] != 0:
            series.append("SB")

        if ("N" not in series) and ("AZ" not in series):
            if("PM" in series) or ("PL" in series):
                res.append(series)

    # print(res[:5])
    df1 = pd.DataFrame(res)
    print(df1.head(), df1.shape)

    df1.to_csv(file, index=False)


# 处理 Apriori 算法输出
def apriori_out_process(file="../Data/NM_NL_GOLD.txt"):
    data = pd.read_csv(file,
                       header=None,
                       names=["FROM", "TO", "Confidence"])

    # print(data.head())

    li = np.array(data).tolist()
    li_chosen = []

    for l in li:
        l_in = l[0]
        l_out = l[1]

        l[0] = l[0].replace("'", "").replace("(", "").replace(")", "")
        l[1] = l[1].replace("'", "").replace("(", "").replace(")", "")
        s = True

        if ("BB" in l_in) or ("BM" in l_in) or \
                ("BS" in l_in) or ("'N'" in l_in) or \
                ("SS" in l_in) or ("SM" in l_in) or \
                ("SB" in l_in):
            s = False

        if ("NL" in l_out) or ("NM" in l_out) or \
                ("NS" in l_out) or ("AZ" in l_out) or \
                ("PS" in l_out) or ("PM" in l_out) or \
                ("PL" in l_out):
            s = False

        if s:
            li_chosen.append(l)
            print(l)

    return li_chosen

bs = 0.1
ss = -0.1
bm = 0.2
sm = -0.2
bb = 0.4
sb = -0.4

def testing_compute(price_btc, price_gold, a_btc=0.02, a_gold=0.01):
    time = 365 * 5
    # bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total
    bos_vec_btc, bos_vec_gold = testing_bos_vtc(price_btc[: time], price_gold[: time])

    d = {
        "比特币操作": [],
        "黄金操作": [],
        "现金": [],
        "比特币": [],
        "黄金": [],
        "比特币价格": [],
        "黄金价格": [],
        "资产总值": []
    }
    df1 = pd.DataFrame(d)

    # bs = 0.1
    # ss = -0.1
    # bm = 0.2
    # sm = -0.2
    # bb = 0.4
    # sb = -0.4

    cash = 1000
    btc = 0
    gold = 0

    t_his = []

    for i in range(time - 1):

        price_gold_now = price_gold[i]
        price_btc_now = price_btc[i]

        gmove = "不动"
        bmove = "不动"

        if bos_vec_btc[i][0] != 0 and btc > 0:
            bmove = "大卖"
            sell_btc_best = btc * sb  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif bos_vec_btc[i][1] != 0 and btc > 0:
            bmove = "中卖"
            sell_btc_best = btc * sm  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif bos_vec_btc[i][2] != 0 and btc > 0:
            bmove = "小卖"
            sell_btc_best = btc * ss  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif bos_vec_btc[i][4] != 0 and cash > 10:
            bmove = "小买"
            buy_btc_cash_best = cash * bs
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best
        elif bos_vec_btc[i][5] != 0 and cash > 10:
            bmove = "中买"
            buy_btc_cash_best = cash * bm
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best
        elif bos_vec_btc[i][6] != 0 and cash > 10:
            bmove = "大买"
            buy_btc_cash_best = cash * bb
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best

        if bos_vec_gold[i][0] != 0 and gold > 0:
            gmove = "大卖"
            sell_gold_best = gold * sb  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif bos_vec_gold[i][1] != 0 and gold > 0:
            gmove = "中卖"
            sell_gold_best = gold * sm  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif bos_vec_gold[i][2] != 0 and gold > 0:
            gmove = "小卖"
            sell_gold_best = gold * ss  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif bos_vec_gold[i][4] != 0 and cash > 10:
            gmove = "小买"
            buy_gold_cash_best = cash * bs
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best
        elif bos_vec_gold[i][5] != 0 and cash > 10:
            gmove = "中买"
            buy_gold_cash_best = cash * bm
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best
        elif bos_vec_gold[i][6] != 0 and cash > 10:
            gmove = "大买"
            buy_gold_cash_best = cash * bb
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        if btc < 10e-8:
            btc = 0
        if gold < 10e-6:
            gold = 0

        s1 = pd.Series(
            {
            "比特币操作": bmove,
            "黄金操作": gmove,
            "现金": cash,
            "比特币": btc,
            "黄金": gold,
            "比特币价格": price_btc_now,
            "黄金价格": price_gold_now,
            "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print(bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)

    df1.to_excel("../Data/MA_RESULT_2.xlsx", index=False)
    print(df1.head())
    print(df1.head(-1))
    # plt.figure()
    #
    # # 两行两列 第一个
    # plt.subplot(3, 1, 1)

    plt.plot(range(len(t_his)), t_his, c = '#AACCFF', label="MA Model(2016.11 - 2019.11)")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()


    # 两行两列 第一个
    # plt.subplot(3, 1, 2)
    # d = 365
    # plt.plot(range(len(t_his[:d])), t_his[:d])
    #
    # plt.subplot(3, 1, 3)
    # d = 365
    # plt.plot(range(len(t_his[-d:])), t_his[-d:])

    # print(t_his[360:365])
    # print(t_his[-5:])

    plt.show()

def testing_compute_4(price_btc, price_gold, a_btc=0.02, a_gold=0.01):
    time = 365 * 5
    # bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total
    bos_vec_btc, bos_vec_gold = testing_bos_vtc(price_btc[: time], price_gold[: time], y=4)

    d = {
        "比特币操作": [],
        "黄金操作": [],
        "现金": [],
        "比特币": [],
        "黄金": [],
        "比特币价格": [],
        "黄金价格": [],
        "资产总值": []
    }
    df1 = pd.DataFrame(d)

    # bs = 0.1
    # ss = -0.1
    # bm = 0.2
    # sm = -0.2
    # bb = 0.4
    # sb = -0.4

    cash = 1000
    btc = 0
    gold = 0

    t_his = []

    for i in range(time - 1):

        price_gold_now = price_gold[i]
        price_btc_now = price_btc[i]

        gmove = "不动"
        bmove = "不动"

        if bos_vec_btc[i][0] != 0 and btc > 0:
            bmove = "大卖"
            sell_btc_best = btc * sb  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif bos_vec_btc[i][1] != 0 and btc > 0:
            bmove = "中卖"
            sell_btc_best = btc * sm  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif bos_vec_btc[i][2] != 0 and btc > 0:
            bmove = "小卖"
            sell_btc_best = btc * ss  # 负数
            btc = btc + sell_btc_best
            sell_btc_cash_best = sell_btc_best * price_btc_now  # 负数
            cash = cash - sell_btc_cash_best * (1 - a_btc)
        elif bos_vec_btc[i][4] != 0 and cash > 10:
            bmove = "小买"
            buy_btc_cash_best = cash * bs
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best
        elif bos_vec_btc[i][5] != 0 and cash > 10:
            bmove = "中买"
            buy_btc_cash_best = cash * bm
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best
        elif bos_vec_btc[i][6] != 0 and cash > 10:
            bmove = "大买"
            buy_btc_cash_best = cash * bb
            cash = cash - buy_btc_cash_best * (1 + a_btc)
            buy_btc_best = buy_btc_cash_best / price_btc_now
            btc = btc + buy_btc_best

        if bos_vec_gold[i][0] != 0 and gold > 0:
            gmove = "大卖"
            sell_gold_best = gold * sb  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif bos_vec_gold[i][1] != 0 and gold > 0:
            gmove = "中卖"
            sell_gold_best = gold * sm  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif bos_vec_gold[i][2] != 0 and gold > 0:
            gmove = "小卖"
            sell_gold_best = gold * ss  # 负数
            gold = gold + sell_gold_best
            sell_gold_cash_best = sell_gold_best * price_gold_now  # 负数
            cash = cash - sell_gold_cash_best * (1 - a_gold)
        elif bos_vec_gold[i][4] != 0 and cash > 10:
            gmove = "小买"
            buy_gold_cash_best = cash * bs
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best
        elif bos_vec_gold[i][5] != 0 and cash > 10:
            gmove = "中买"
            buy_gold_cash_best = cash * bm
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best
        elif bos_vec_gold[i][6] != 0 and cash > 10:
            gmove = "大买"
            buy_gold_cash_best = cash * bb
            cash = cash - buy_gold_cash_best * (1 + a_gold)
            buy_gold_best = buy_gold_cash_best / price_gold_now
            gold = gold + buy_gold_best

        best_total = cash + gold * price_gold_now + btc * price_btc_now

        t_his.append(best_total)

        if btc < 10e-8:
            btc = 0
        if gold < 10e-6:
            gold = 0

        s1 = pd.Series(
            {
            "比特币操作": bmove,
            "黄金操作": gmove,
            "现金": cash,
            "比特币": btc,
            "黄金": gold,
            "比特币价格": price_btc_now,
            "黄金价格": price_gold_now,
            "资产总值": best_total
            }
        )

        df1 = df1.append(s1, ignore_index=True)
        # print(bmove, gmove, cash, btc, gold, price_btc_now, price_gold_now, best_total)

    df1.to_excel("../Data/MA_RESULT_4.xlsx", index=False)
    print(df1.head())
    print(df1.head(-1))
    # plt.figure()
    #
    # # 两行两列 第一个
    # plt.subplot(3, 1, 1)

    plt.plot(range(len(t_his)), t_his, c = '#AACCFF', label="MA Model(2016.11 - 2019.11)")
    plt.xticks(())
    plt.legend(loc='upper left')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.grid()


    # 两行两列 第一个
    # plt.subplot(3, 1, 2)
    # d = 365
    # plt.plot(range(len(t_his[:d])), t_his[:d])
    #
    # plt.subplot(3, 1, 3)
    # d = 365
    # plt.plot(range(len(t_his[-d:])), t_his[-d:])

    # print(t_his[360:365])
    # print(t_his[-5:])

    plt.show()




if __name__ == "__main__":

    path_btc = "../Data/BCHAIN-MKPRU.csv"
    path_gold = "../Data/LBMA-GOLD.csv"

    data_btc = pd.read_csv(path_btc)
    data_gold = pd.read_csv(path_gold)

    # print(data_btc.describe())
    # print(data_gold.describe())

    data_btc.set_index("Date", inplace=True, drop=True)
    data_gold.set_index("Date", inplace=True, drop=True)
    data = pd.concat([data_btc, data_gold], axis=1)
    # 用 0 填充
    # data.fillna({"USD (PM)": 0}, inplace=True)
    # 用前一个值填充
    data.fillna(inplace=True, method="bfill")
    data.reset_index(inplace=True)
    data.rename(columns={'index': 'Date', 'Value': 'BTC_Value', 'USD (PM)': 'Gold_Value'}, inplace=True)
    # print(data.head(3))
    # print(data.describe())

    x = data["Date"]
    y_b = data["BTC_Value"]
    y_g = data["Gold_Value"]

    # show_plot_1(x, y_b, y_g)
    # show_plot_2(x, y_b, y_g)

    price_btc = np.array(y_b)
    price_gold = np.array(y_g)


    # 大买(+3) 中买(+2) 小买(+1) 保持(0) 小卖(-1） 中卖(-2) 大卖(-3)
    # 买：现有现金的百分之多少拿来买
    # 卖：现有比特币/黄金的百分之多少拿来卖
    # 二元组表示输出状态，例如：(2, 0) 表示中买比特币，保持黄金

    # 计算相关系数
    # a1 = pd.Series(price_btc)
    # a2 = pd.Series(price_gold)
    # corr = a1.corr(a2, method='spearman')
    # print(corr)

    # 计算预测最优结果（未采用？）
    # best_vtc_btc, best_vtc_btc_total = modeling_best_vtc(price_btc, 0.02)
    # best_vtc_gold, best_vtc_gold_total = modeling_best_vtc(price_gold, 0.01)
    # print(best_vtc_btc)
    # print(best_vtc_gold)
    # show_plot_2(range(len(best_vtc_btc_total)), best_vtc_btc_total, best_vtc_gold_total)

    # 计算模糊集向量：包括涨跌模糊集和买卖模糊集
    # l_in_btc, l_in_gold = modeling_rof_vtc(price_btc[:365 * 4], price_gold[:365 * 4])
    # l_out_btc, l_out_gold = modeling_bos_vtc(price_btc[:365 * 4], price_gold[:365 * 4])


    # Apriori 算法：
    # get_a_input(l_in_btc, l_out_btc, "../Apriori-python3/APRIORI_IN_NMNL_BTC_4.csv")
    # get_a_input(l_in_btc, l_out_btc, "../Apriori-python3/APRIORI_IN_PMPL_BTC_4.csv")
    #
    # get_a_input_nmnl(l_in_gold, l_out_gold, "../Apriori-python3/APRIORI_IN_NMNL_GOLD_4.csv")
    # get_a_input_pmpl(l_in_gold, l_out_gold, "../Apriori-python3/APRIORI_IN_PMPL_GOLD_4.csv")

    # get_a_input(l_in_btc, l_out_btc, "../Apriori-python3/APRIORI_IN_BTC_4.csv")
    # get_a_input(l_in_gold, l_out_gold, "../Apriori-python3/APRIORI_IN_GOLD_4.csv")

    # 处理 Apriori 算法结果

    # print("Gold:")
    # apriori_out_process(file="../Data/NEW/NM_NL_GOLD.txt")
    # apriori_out_process(file="../Data/NEW/PM_PL_GOLD.txt")
    # print("Bitcoin:")
    # apriori_out_process(file="../Data/NEW/NM_NL_BTC.txt")
    # apriori_out_process(file="../Data/NEW/PM_PL_BTC.txt")

    # print("Gold:")
    # apriori_out_process(file="../Data/GOLD.txt")
    # print("Bitcoin:")
    # apriori_out_process(file="../Data/BTC.txt")

    # SMA5 - SMA15 / SMA5 模型求取决策结果（效果一般）
    # modeling_stpuid(price_btc[:365 * 2], price_gold[: 365 * 2])
    # modeling_stpuid(price_btc, price_gold)

    # MA模型
    # modeling_ma_final(price_btc, price_gold, a_btc=0.002, a_gold=0.001)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.01, a_gold=0.005)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.02, a_gold=0.01)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.04, a_gold=0.02)

    # modeling_ma_final(price_btc, price_gold, a_btc=0.005, a_gold=0.01)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.01, a_gold=0.02)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.02, a_gold=0.04)

    # modeling_ma_final(price_btc, price_gold, a_btc=0.005, a_gold=0.005)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.01, a_gold=0.01)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.02, a_gold=0.02)
    # modeling_ma_final(price_btc, price_gold, a_btc=0.04, a_gold=0.04)


    # modeling_ma(price_btc[:2*365], price_gold[:2*365], level=9)

    # SMA(price_btc, price_gold)

    # 生成美美的决策图
    # SMA(price_btc, price_gold)
    # bncmap, vec_btc, vec_gold = build_bncmap(price_btc, price_gold)
    # show_img(vec_btc, vec_gold)


    # 测试过程
    # bos_vec_btc, bos_vec_gold = testing_bos_vtc(price_btc[:365 * 3], price_gold[:365 * 3])
    # testing_compute(price_btc, price_gold)
    # testing_compute_4(price_btc, price_gold)
    # print("Result")

    # RSquard(price_btc, price_gold)
    # nhsyl("../Data/MA_RESULT.xlsx")
    # nhsyl("../Data/MA_RESULT_2.xlsx")
    # nhsyl("../Data/MA_RESULT_4.xlsx")

    # modeling_ma(price_btc, price_gold, level=9)
    # day = 1824
    # money = 6084.422197
    # print(((money - 1000) / 1000) / (day / 365) * 100)

    AAA(price_btc, price_gold)

# 寻找可能存在的映射关系
# 大卖 中卖 小卖 保持 小买 中买 大买 7 * 7 = 49
# 大涨 中涨 小涨 持平 小降 中降 大降 7 * 7 = 49

# 1. 构建输入输出集合
# 2. 找联合趋势（模糊集）
# 3. 机器学习/神经网络算映射

# 稳定性加大投资力度，不稳定性减少与投资力度（投资频率）

