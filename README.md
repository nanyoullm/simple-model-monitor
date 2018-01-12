# simple model monitor
简易的监控定期更新的用户信用分及特征分布界面。  
## 介绍
以一个金融领域的用户信用分为例，我们需要定期按照新观察期的数据，去更新每个用户的信用评分。
更新之后的评分和各变量的分布的分析是必要的，通过多账期评分总体的分布对比，计算一些指标，
可以评价这个模型是否收到了当前业务的影响？在一定周期内是否可以保持稳定？PSI是多少？
申请了金融产品的客户的分数是否满足排序性？整体KS是多少？等等...  
> 特别说明：展示的数据为随机生成数据，库中附带生成伪数据的代码。

## 界面展示
- 可选择不同的评分查看分布，下部分是特征的分布，可拖拽查看；
<br>
<img src="https://github.com/nanyoullm/simple-model-monitor/blob/master/img/monitor1.gif?raw=true">
<br>

- 可选择不同账期的同一评分进行对比，下部分是特征的分布对比，可拖拽查看对比；
<br>
<img src="https://github.com/nanyoullm/simple-model-monitor/blob/master/img/monitor2.gif?raw=true">
<br>

## 技术栈
Python + Mysql + Flask + Ajax + Echarts

## 第三方包
- Python2.7（Flask相对更加兼容Python2.7，使用Python3.6的朋友可以适当修改代码）
- numpy
- pandas 
- flask
- pymysql

## 使用
- 安装本地mysql
自行安装mysql数据库，默认代码使用scheme: test

- 生成伪数据
运行代码
`
python save_fake_data.py
`