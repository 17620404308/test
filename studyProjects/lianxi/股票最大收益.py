'''
给定一个列表，它的第 i 个元素是一支给定股票第 i 天的价格。
如果最多只允许完成一笔交易（即买入和卖出一支股票，并规定每次只买入或卖出1股，或者不买不卖），请计算出所能获取的最大收益。
注意：不能在买入股票前卖出股票。
'''
prices = [7,1,5,3,6,4]
# pro=[]
# for i in range(1,len(price)):
#     for j in range(i,len(price)):
#         profile = price[j]-price[i]
#         pro.append(profile)
# print(max(pro))

# for i in range(0,len(price)):
#     for j in range(i, len(price)):
#         profile = price[j] - price[i]
#         maxpro = max(maxpro,profile)
minprice = prices[0]
maxprofit = 0
for price in prices:
    maxprofit = max(price - minprice, maxprofit)
    minprice = min(price, minprice)
print(maxprofit)
