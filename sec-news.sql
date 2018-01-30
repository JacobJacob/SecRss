/*
 Navicat Premium Data Transfer

 Source Server         : .
 Source Server Type    : MySQL
 Source Server Version : 50635
 Source Host           : localhost:3306
 Source Schema         : sec-news

 Target Server Type    : MySQL
 Target Server Version : 50635
 File Encoding         : 65001

 Date: 30/01/2018 18:26:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sys_collect_count
-- ----------------------------
DROP TABLE IF EXISTS `sys_collect_count`;
CREATE TABLE `sys_collect_count` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `published_time` text NOT NULL COMMENT '采集时间',
  `count` int(11) NOT NULL COMMENT '采集数目',
  `hash` varchar(32) NOT NULL COMMENT '采集日期hash值，用于检索',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search_hash` (`hash`) USING HASH COMMENT '采集日期hash值，用于检索'
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sys_posts
-- ----------------------------
DROP TABLE IF EXISTS `sys_posts`;
CREATE TABLE `sys_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL COMMENT '标题',
  `source_url` text NOT NULL COMMENT '原始url',
  `from` longtext NOT NULL COMMENT '来源网站',
  `content` longtext NOT NULL COMMENT '内容',
  `published_time` text NOT NULL COMMENT '发布时间',
  `hash` varchar(32) NOT NULL COMMENT '采集日期hash值，用于检索',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4;
