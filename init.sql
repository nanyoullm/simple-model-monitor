create SCHEMA test;

create table test.model_statistic (
  score_name varchar(32), -- 评分模型名
  period varchar(32), -- 账期
  score varchar(32), -- 分值
  counts int -- 统计值
) charset=utf8;

create table test.feature_statistic (
  score_name varchar(32), -- 评分模型名
  period varchar(32), -- 账期
  feature_name varchar(32), -- 特征名
  value varchar(32), -- 特征取值
  counts int  -- 统计值
) charset=utf8;

DROP TABLE test.model_statistic;
DROP TABLE test.feature_statistic;
