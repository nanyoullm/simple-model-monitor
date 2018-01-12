# -*- coding: utf-8 -*-
import pymysql
import numpy as np
import pandas as pd
import json

score_names = {'A4': 'A4分', 'A5': 'A5分', 'Wo': '沃信用分'}


class Mysql(object):
    def __init__(self, host, db):
        self.host = host
        self.port = 3306
        self.user = 'root'
        self.db = db

    def connect(self):
        return pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               db=self.db,
                               charset='utf8')


def generate_fake_data(x_axis_, types):
    if types == 'model':
        data = []
        for i in x_axis_:
            value = int(np.random.normal(len(x_axis_) / 2, 5))
            data.append(value)
        return data
    else:
        data = []
        for i in x_axis_:
            value = int(np.random.normal(20, 10)) + 10
            data.append(value)
        return data


def generate_show_data(period, output, legends, types, data_source):
    output.append(data_source)
    output.append(data_source)
    legends.append(period.encode('utf-8') + '-b')
    legends.append(period.encode('utf-8') + '-l')
    types.append('bar')
    types.append('line')


def make_json(data):
    for d in data:
        d = json.dumps(d)


def model_data_for_front_begin(sql, connect, periods):
    df = pd.read_sql(sql, con=connect)
    df.columns = ['score', 'counts']
    df = df.sort_values('score')
    model_axis = df['score'].astype(str).values.tolist()
    distribution = df['counts'].astype(int).values.tolist()
    period_show = max(periods)

    model_data = []
    model_legend = []
    model_type = []
    model_selected = 'A5'
    generate_show_data(period_show, model_data, model_legend, model_type, distribution)
    # 如果是list，则需要转变成json格式传递
    make_json([model_data, model_legend, model_type, model_axis, periods, model_selected, period_show])

    return {'model_data': model_data,
            'model_legend': model_legend,
            'model_type': model_type,
            'model_axis': model_axis,
            'model_selected': model_selected,
            'periods': periods,
            'period_show': period_show}


def model_data_for_front_form(sql, connect, period_selected, model_selected):
    df = pd.read_sql(sql, con=connect)
    df.columns = ['score', 'counts', 'period']
    df = df.sort_values('score')
    model_axis = df['score'].astype(str).unique().tolist()

    model_data = []
    model_legend = []
    model_type = []
    for period in period_selected:
        distribution = df[df['period'] == period]['counts'].astype(int).values.tolist()
        generate_show_data(period, model_data, model_legend, model_type, distribution)

    return {'model_data': model_data,
            'model_legend': model_legend,
            'model_type': model_type,
            'model_axis': model_axis,
            'model_title': score_names[model_selected] + '全国分布'}


def feature_data_for_front_begin(sql, connect, periods):
    df = pd.read_sql(sql, con=connect)
    df.columns = ['feature_name', 'feature_value', 'counts']
    period_show = max(periods)
    feature_axis_dict = {}
    feature_data_dict = {}
    feature_legends_dict = {}
    feature_type_dict = {}
    feature_list = df['feature_name'].unique().tolist()
    make_json([feature_list])
    for feature in feature_list:
        feature_axis = df[(df['feature_name'] == feature)]['feature_value'].astype(str).values.tolist()
        distribution = df[(df['feature_name'] == feature)]['counts'].astype(int).values.tolist()
        feature_data = []
        feature_legends = []
        feature_types = []
        generate_show_data(period_show, feature_data, feature_legends, feature_types, distribution)
        make_json([feature_data, feature_legends, feature_types])
        feature_axis_dict[feature] = feature_axis
        feature_data_dict[feature] = feature_data
        feature_legends_dict[feature] = feature_legends
        feature_type_dict[feature] = feature_types

    return {'feature_name': feature_list,
            'feature_data': feature_data_dict,
            'feature_axis': feature_axis_dict,
            'feature_legend': feature_legends_dict,
            'feature_type': feature_type_dict}


def feature_data_for_front_form(sql, connect, period_selected):
    df = pd.read_sql(sql, con=connect)
    df.columns = ['feature_name', 'feature_value', 'period', 'counts']
    feature_list = df['feature_name'].unique().tolist()
    feature_axis_dict = {}
    feature_data_dict = {}
    feature_legends_dict = {}
    feature_type_dict = {}
    for feature in feature_list:
        sub_feature_data_list = []
        sub_feature_legends_list = []
        sub_feature_type_list = []
        sub_feature_axis_list = df[(df['feature_name'] == feature)]['feature_value'] \
            .astype(str).unique().tolist()
        for period in period_selected:
            distribution = df[(df['feature_name'] == feature) & (df['period'] == period)]['counts']\
                .astype(int).values.tolist()
            feature_data = []
            feature_legends = []
            feature_types = []
            generate_show_data(period, feature_data, feature_legends, feature_types, distribution)
            make_json([feature_data, feature_legends, feature_types])
            sub_feature_data_list.extend(feature_data)
            sub_feature_legends_list.extend(feature_legends)
            sub_feature_type_list.extend(feature_types)
        feature_axis_dict[feature] = sub_feature_axis_list
        feature_data_dict[feature] = sub_feature_data_list
        feature_legends_dict[feature] = sub_feature_legends_list
        feature_type_dict[feature] = sub_feature_type_list

    return {'feature_name': feature_list,
            'feature_data': feature_data_dict,
            'feature_axis': feature_axis_dict,
            'feature_legend': feature_legends_dict,
            'feature_type': feature_type_dict}


if __name__ == '__main__':
    pass
