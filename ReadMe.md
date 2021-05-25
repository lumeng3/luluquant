# 卢克量化交易

## 目录

1. 项目安装
1. 使用方法
3. 常见Git指令


## 项目安装

首先，下载python到您的本地，编译器可自行选择，推荐PyCharm

- [Python](https://www.python.org/downloads/) 
- [PyCharm](https://www.jetbrains.com/pycharm/download/#section=mac) 

其次，打开终端，执行以下操作：
1. pip install TA-Lib
2. pip install requests
3. python3 trade.py
4. pip install pandas==1.1.5 numpy==1.19.4 scipy==1.5.4
5. pip install alpaca-backtrader-api
6. pip install matplotlib
7. pip install get-all-tickers

## 使用方法

1. 安装步骤1后，进入./src/strategy/,添加、运行策略。
  比如，执行吞噬线策略，则运行./src/strategy/tunShiXian.py
2. 本项目采用BackTrade library，回测代码实例如下:
```python
    cerebro = bt.Cerebro() #初始化
    cerebro.addstrategy(TunShiXian) #添加策略
    cerebro.adddata(data0) #添加数据
```
  BackTrade文档：
    - [BackTrade](https://www.backtrader.com/docu/) 

3. 获取数据，请调用
```importData.py``` 中的函数
   
## 常见Git指令
```
新建一个branch
git checkout -b MyBranch 

进行您的修改后，查询已修改的文件
git status

回到别的branch
git checkout OtherBranch

添加文件
git add File

添加commit
git commit -m "your commit"

上传您的修改
git push
```