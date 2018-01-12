create SCHEMA test;

create table test.model_statistic (
  score_name varchar(32),
  period varchar(32),
  score varchar(32),
  counts int
) charset=utf8;

create table test.feature_statistic (
  score_name varchar(32),
  period varchar(32),
  feature_name varchar(32),
  value varchar(32),
  counts int
) charset=utf8;

DROP TABLE test.model_statistic;
DROP TABLE test.feature_statistic;
