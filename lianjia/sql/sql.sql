CREATE TABLE `community` (
  `id` varchar(255) NOT NULL COMMENT '小区ID',
  `name` varchar(255) DEFAULT NULL COMMENT '小区名称',
  `selling_count` int(11) DEFAULT NULL COMMENT '售出数量',
  `sold_avg_price` int(10) DEFAULT NULL COMMENT '售出平均价格',
  `district` varchar(255) DEFAULT NULL COMMENT '区域',
  `gmt_create` datetime DEFAULT NULL COMMENT '数据采集时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='小区列表';

CREATE TABLE `house` (
  `id` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '房源ID',
  `community_id` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '小区ID',
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '房源标题',
  `price` double DEFAULT NULL COMMENT '价格',
  `price_unit` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '价格单位（万）',
  `price_per` double(255,0) DEFAULT NULL COMMENT '单价',
  `price_per_unit` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '单价单位(元/平米)',
  `type` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '类型（两室一厅）',
  `size` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '大小（59.5平米）',
  `on_sale_date` date DEFAULT NULL COMMENT '上架时间',
  `gmt_create` datetime DEFAULT NULL COMMENT '采集时间',
  PRIMARY KEY (`id`,`community_id`),
  KEY `community_id` (`community_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='房源信息';

