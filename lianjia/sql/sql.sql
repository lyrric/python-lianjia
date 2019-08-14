CREATE TABLE `community` (
  `id` varchar(255) NOT NULL COMMENT '小区ID',
  `name` varchar(255) DEFAULT NULL COMMENT '小区名称',
  `selling_count` int(11) DEFAULT NULL COMMENT '售出数量',
  `sold_avg_price` int(10) DEFAULT NULL COMMENT '售出平均价格',
  `district` varchar(255) DEFAULT NULL COMMENT '区域',
  `gmt_create` datetime DEFAULT NULL COMMENT '数据采集时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='小区列表';

