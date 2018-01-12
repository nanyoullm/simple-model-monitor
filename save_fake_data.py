# -*- coding: utf-8 -*-
import pandas as pd
from utils import Mysql
from utils import generate_fake_data

mysql = Mysql(host='127.0.0.1', db='unicom')

x_axis_a4 = range(1, 101)
x_axis_a5 = range(1, 151)
x_axis_wo = range(1, 201)

x_axis_a4_features = range(0, 12)
x_axis_a5_features = range(0, 8)
x_axis_wo_features = range(0, 6)
feature_values = range(-5, 20, 6)
periods = ['201710', '201709', '201708']
score_axis = {'A4': x_axis_a4, 'A5': x_axis_a5, 'Wo': x_axis_wo}
model_features = {'A4': x_axis_a4_features, 'A5': x_axis_a5_features, 'Wo': x_axis_wo_features}


def data_for_model():
    print 'fake model data...'
    # n个账期
    for period in periods:
        print ' ' + period
        # m个模型
        for score_name in score_axis.keys():
            print '     ' + score_name
            axis = score_axis[score_name]
            counts = generate_fake_data(axis, 'model')
            s = score_name.decode('utf-8')
            df = pd.DataFrame({'score_name': [score_name.decode('utf-8')] * len(axis),
                               'period': [period] * len(axis),
                               'score': axis,
                               'counts': counts})
            df = df[['score_name', 'period', 'score', 'counts']]
            connect = mysql.connect()
            df.to_sql(name='model_statistic', flavor='mysql', con=connect,
                      if_exists='append', index=False)
            connect.close()


def data_for_feature():
    print 'fake feature data...'
    # n个账期
    for period in periods:
        print ' ' + period
        # m个模型
        for score_name in score_axis.keys():
            print '     ' + score_name
            features = model_features[score_name]
            # 共有len(features)个特征，features为特征名的列表
            for feature in features:
                feature_name = score_name + '_feature_' + str(feature)
                print '         ' + feature_name
                counts = generate_fake_data(feature_values, 'feature')
                df = pd.DataFrame({'score_name': [score_name] * len(feature_values),
                                   'period': [period] * len(feature_values),
                                   'feature_name': [feature_name] * len(feature_values),
                                   'feature_value': feature_values,
                                   'counts': counts})
                connect = mysql.connect()
                df.to_sql(name='feature_statistic', flavor='mysql',con=connect,
                          if_exists='append', index=False)
                connect.close()


if __name__ == '__main__':
    data_for_model()
    data_for_feature()
