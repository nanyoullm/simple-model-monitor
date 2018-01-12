# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, request
from flask import jsonify
import json
import pandas as pd
from utils import Mysql
from utils import model_data_for_front_begin
from utils import feature_data_for_front_begin
from utils import model_data_for_front_form
from utils import feature_data_for_front_form


app = Flask(__name__)
mysql = Mysql('127.0.0.1', 'test')
score_names = {'A': 'A分', 'B': 'B分', 'W': 'W分'}


@app.route('/')
def hello_world():
    '''
    传递参数说明：
    output -> 用于绘制分布数据
    legends -> 分布数据对应的图例
    types -> 分布数据展示类型，bar 或 line
    axis -> x轴
    '''

    # 确定数据库里已有哪些账期
    sql = 'select distinct period from model_statistic'
    connect = mysql.connect()
    df = pd.read_sql(sql, con=connect)
    df.columns = ['period']
    periods = df['period'].values.tolist()
    period_show = max(df['period'].values)

    # 获取绘制模型分布的渲染参数
    sql = 'select score, counts from model_statistic ' \
          'where period=\'{}\' and score_name=\'{}\''.format(period_show, 'A')
    model_data = model_data_for_front_begin(sql, connect, periods)

    # 获取绘制变量分布的渲染参数
    sql = 'select feature_name, feature_value, counts from feature_statistic ' \
          'where period=\'{}\' and score_name=\'{}\''.format(period_show, 'A')
    feature_data = feature_data_for_front_begin(sql, connect, periods)

    connect.close()

    # 所有信息包含到dict对象进行传递，提高可检查性
    json_data = {
        'model_data': model_data['model_data'],
        'model_legend': model_data['model_legend'],
        'model_type': model_data['model_type'],
        'model_axis': model_data['model_axis'],
        'model_selected': model_data['model_selected'],
        'feature_name': feature_data['feature_name'],
        'feature_data': feature_data['feature_data'],
        'feature_axis': feature_data['feature_axis'],
        'feature_legend': feature_data['feature_legend'],
        'feature_type': feature_data['feature_type'],
        'periods': model_data['periods'],
        'period_show': model_data['period_show']
    }

    return render_template('index.html', **locals())


@app.route('/selected', methods=['POST'])
def response_form():
    connect = mysql.connect()
    model_selected = request.form['model'].encode('utf-8')
    # 由于多选项按钮是Array对象，需要加上[]
    period_selected = request.form.getlist('period[]')
    period_selected_string = '\',\''.join(period_selected)

    # 获取绘制模型分布的渲染参数
    sql = 'select score, counts, period from model_statistic ' \
          'where period in (\'{}\') and score_name=\'{}\''
    sql = sql.format(period_selected_string, model_selected)
    model_data = model_data_for_front_form(sql, connect, period_selected, model_selected)

    # 获取绘制变量分布的渲染参数
    sql = 'select feature_name, feature_value, period, counts ' \
          'from feature_statistic where period in (\'{}\') and score_name=\'{}\''
    sql = sql.format(period_selected_string, model_selected)
    feature_data = feature_data_for_front_form(sql, connect, period_selected)

    connect.close()

    return jsonify({'model_data': model_data['model_data'],
                    'model_legend': model_data['model_legend'],
                    'model_type': model_data['model_type'],
                    'model_axis': model_data['model_axis'],
                    'model_title': model_data['model_title'],
                    'feature_name': feature_data['feature_name'],
                    'feature_data': feature_data['feature_data'],
                    'feature_axis': feature_data['feature_axis'],
                    'feature_legend': feature_data['feature_legend'],
                    'feature_type': feature_data['feature_type']})


if __name__ == '__main__':
    app.run(port=7000)
