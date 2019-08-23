/*
Navicat MySQL Data Transfer

Source Server         : ali
Source Server Version : 50640
Source Host           : 47.97.215.50:3306
Source Database       : lianjia

Target Server Type    : MYSQL
Target Server Version : 50640
File Encoding         : 65001

Date: 2019-08-23 17:26:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for community
-- ----------------------------
DROP TABLE IF EXISTS `community`;
CREATE TABLE `community` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '小区代码',
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '小区名称',
  `selling_house_amount` int(11) DEFAULT NULL COMMENT '售卖中房源数量(页面上的值)',
  `sold_house_amount` int(11) DEFAULT NULL COMMENT '已成交房屋数量(页面上的值)',
  `selling_avg_price` double(9,3) DEFAULT NULL COMMENT '售卖中的房屋单价(计算的值)',
  `sold_avg_price` double(9,3) DEFAULT NULL COMMENT '已售出的房屋单价(计算的值)',
  `new_house_amount` int(11) DEFAULT NULL COMMENT '新上架房屋数量(计算的值)',
  `district` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '小区所在地区',
  `gmt_create` datetime DEFAULT NULL COMMENT '采集时间',
  `version` int(11) DEFAULT NULL COMMENT '版本号',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11144 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for selling_house
-- ----------------------------
DROP TABLE IF EXISTS `selling_house`;
CREATE TABLE `selling_house` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '房源代码',
  `community_code` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '小区代码',
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '房源标题',
  `price` double DEFAULT NULL COMMENT '挂牌价格',
  `price_per` double DEFAULT NULL COMMENT '挂牌单价',
  `price_unit` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '价格单位（万）',
  `type` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '类型（两室一厅）',
  `size` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '大小（59.5平米）',
  `on_sale_date` date DEFAULT NULL COMMENT '上架时间',
  `deleted` bit(1) DEFAULT NULL COMMENT '是否下架',
  `gmt_create` datetime DEFAULT NULL COMMENT '采集时间',
  `gmt_update` datetime DEFAULT NULL COMMENT '更新时间（最新一次采集时间）',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `community_code` (`community_code`),
  KEY `on_sale_date` (`on_sale_date`)
) ENGINE=InnoDB AUTO_INCREMENT=98107 DEFAULT CHARSET=utf8 COMMENT='房源信息';

-- ----------------------------
-- Table structure for selling_month_stat
-- ----------------------------
DROP TABLE IF EXISTS `selling_month_stat`;
CREATE TABLE `selling_month_stat` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL COMMENT '挂牌中的房屋数量',
  `avg_price_per` double(9,2) DEFAULT NULL COMMENT '平均单位价格（本月上架的）',
  `increased_amount` int(11) DEFAULT NULL COMMENT '本月新增房源',
  `stat_date` date DEFAULT NULL COMMENT '统计时间(月初)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='挂牌中的房屋月统计';

-- ----------------------------
-- Table structure for selling_week_stat
-- ----------------------------
DROP TABLE IF EXISTS `selling_week_stat`;
CREATE TABLE `selling_week_stat` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL COMMENT '挂牌中的房屋数量',
  `avg_price_per` double(9,2) DEFAULT NULL COMMENT '平均单位价格（本周上架的）',
  `increased_amount` int(11) DEFAULT NULL COMMENT '本周新增房源',
  `stat_date` date DEFAULT NULL COMMENT '统计时间(周一)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='挂牌中的房屋周统计';

-- ----------------------------
-- Table structure for sold_house
-- ----------------------------
DROP TABLE IF EXISTS `sold_house`;
CREATE TABLE `sold_house` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '房源代码',
  `community_code` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '小区代码',
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '房源标题',
  `selling_price` double DEFAULT NULL COMMENT '挂牌价格',
  `sold_price` double DEFAULT NULL COMMENT '成交价格',
  `sold_price_per` double DEFAULT NULL COMMENT '成交单价',
  `price_unit` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '价格单位（万）',
  `type` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '类型（两室一厅）',
  `size` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '大小（59.5平米）',
  `on_sale_date` date DEFAULT NULL COMMENT '上架时间',
  `sold_date` date DEFAULT NULL COMMENT '售出时间',
  `gmt_create` datetime DEFAULT NULL COMMENT '采集时间',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `community_code` (`community_code`),
  KEY `gmt_create` (`gmt_create`),
  KEY `sold_date` (`sold_date`),
  KEY `on_sale_date` (`on_sale_date`)
) ENGINE=InnoDB AUTO_INCREMENT=207309 DEFAULT CHARSET=utf8 COMMENT='房源信息';

-- ----------------------------
-- Table structure for sold_month_stat
-- ----------------------------
DROP TABLE IF EXISTS `sold_month_stat`;
CREATE TABLE `sold_month_stat` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL COMMENT '总共售出房屋数量',
  `avg_price_per` double(9,2) DEFAULT NULL COMMENT '本月售出房源单位平均价格',
  `increased_amount` int(11) DEFAULT NULL COMMENT '本月新增数据',
  `stat_date` date DEFAULT NULL COMMENT '统计时间(月初)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='售出的房屋月统计';

-- ----------------------------
-- Table structure for sold_week_stat
-- ----------------------------
DROP TABLE IF EXISTS `sold_week_stat`;
CREATE TABLE `sold_week_stat` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL COMMENT '总共售出房屋数量',
  `avg_price_per` double(9,2) DEFAULT NULL COMMENT '本周售出房源单位平均价格',
  `increased_amount` int(11) DEFAULT NULL COMMENT '本周新增数据',
  `stat_date` date DEFAULT NULL COMMENT '统计时间(周一)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='售出的房屋周统计';

-- ----------------------------
-- Table structure for version
-- ----------------------------
DROP TABLE IF EXISTS `version`;
CREATE TABLE `version` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `version` int(11) DEFAULT NULL COMMENT '版本号',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
