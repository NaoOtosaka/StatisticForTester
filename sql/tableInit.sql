/*
 Navicat Premium Data Transfer

 Source Server         : HWMySQL
 Source Server Type    : MySQL
 Source Server Version : 50733
 Source Host           : 121.36.8.249:3306
 Source Schema         : DataStatistic

 Target Server Type    : MySQL
 Target Server Version : 50733
 File Encoding         : 65001

 Date: 24/02/2021 10:56:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bug
-- ----------------------------
DROP TABLE IF EXISTS `bug`;
CREATE TABLE `bug`  (
  `bug_id` int(11) NOT NULL AUTO_INCREMENT,
  `tester_id` int(11) NOT NULL,
  `developer_id` int(11) NOT NULL,
  `phase_id` int(11) NOT NULL,
  `bug_type` int(11) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `kb_id` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `model` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `create_time` int(11),
  `close_time` int(11),
  `is_finished` tinyint(1) DEFAULT NULL,
  `is_closed` tinyint(1) DEFAULT NULL,
  `is_online` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`bug_id`) USING BTREE,
  INDEX `bugTesterId`(`tester_id`) USING BTREE,
  INDEX `bugDeveloperId`(`developer_id`) USING BTREE,
  INDEX `bugPhaseId`(`phase_id`) USING BTREE,
  INDEX `bugType`(`bug_type`) USING BTREE,
  INDEX `bugCategory`(`category`) USING BTREE,
  CONSTRAINT `bugCategory` FOREIGN KEY (`category`) REFERENCES `bug_category` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bugDeveloperId` FOREIGN KEY (`developer_id`) REFERENCES `developer` (`developer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bugPhaseId` FOREIGN KEY (`phase_id`) REFERENCES `project_phases` (`phase_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bugTesterId` FOREIGN KEY (`tester_id`) REFERENCES `tester` (`tester_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bugType` FOREIGN KEY (`bug_type`) REFERENCES `bug_type` (`type_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for bug_category
-- ----------------------------
DROP TABLE IF EXISTS `bug_category`;
CREATE TABLE `bug_category`  (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bug_category
-- ----------------------------
INSERT INTO `bug_category` VALUES (1, '未选定');
INSERT INTO `bug_category` VALUES (2, '需求缺失');
INSERT INTO `bug_category` VALUES (3, '功能缺失');
INSERT INTO `bug_category` VALUES (4, '功能阻塞');
INSERT INTO `bug_category` VALUES (5, '环境异常');
INSERT INTO `bug_category` VALUES (6, '用例缺失');
INSERT INTO `bug_category` VALUES (7, '兼容性异常');
INSERT INTO `bug_category` VALUES (8, '部署异常');
INSERT INTO `bug_category` VALUES (9, '功能异常');

-- ----------------------------
-- Table structure for bug_type
-- ----------------------------
DROP TABLE IF EXISTS `bug_type`;
CREATE TABLE `bug_type`  (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`type_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bug_type
-- ----------------------------
INSERT INTO `bug_type` VALUES (1, '前端BUG');
INSERT INTO `bug_type` VALUES (2, '服务端BUG');
INSERT INTO `bug_type` VALUES (3, 'Android BUG');
INSERT INTO `bug_type` VALUES (4, 'IOS BUG');
INSERT INTO `bug_type` VALUES (5, '前端开发');
INSERT INTO `bug_type` VALUES (6, '服务端开发');
INSERT INTO `bug_type` VALUES (7, 'Android开发');
INSERT INTO `bug_type` VALUES (8, 'IOS开发');

-- ----------------------------
-- Table structure for develop
-- ----------------------------
DROP TABLE IF EXISTS `develop`;
CREATE TABLE `develop`  (
  `project_id` int(11) NOT NULL,
  `developer_id` int(11) NOT NULL,
  INDEX `developProjectId`(`project_id`) USING BTREE,
  INDEX `developDeveloperId`(`developer_id`) USING BTREE,
  CONSTRAINT `developDeveloperId` FOREIGN KEY (`developer_id`) REFERENCES `developer` (`developer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `developProjectId` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for develop_type
-- ----------------------------
DROP TABLE IF EXISTS `develop_type`;
CREATE TABLE `develop_type`  (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`type_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of develop_type
-- ----------------------------
INSERT INTO `develop_type` VALUES (1, '前端开发');
INSERT INTO `develop_type` VALUES (2, '服务端开发');
INSERT INTO `develop_type` VALUES (3, 'Android开发');
INSERT INTO `develop_type` VALUES (4, 'IOS开发');

-- ----------------------------
-- Table structure for developer
-- ----------------------------
DROP TABLE IF EXISTS `developer`;
CREATE TABLE `developer`  (
  `developer_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) DEFAULT NULL,
  `name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`developer_id`) USING BTREE,
  INDEX `typeId`(`type_id`) USING BTREE,
  CONSTRAINT `typeId` FOREIGN KEY (`type_id`) REFERENCES `develop_type` (`type_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for planner
-- ----------------------------
DROP TABLE IF EXISTS `planner`;
CREATE TABLE `planner`  (
  `planner_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`planner_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of planner
-- ----------------------------
INSERT INTO `planner` VALUES (1, '未分配', 'null');

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project`  (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `planner_id` int(11) NOT NULL,
  `project_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	`doc_url` VARCHAR(255),
	`test_time` bigint,
	`publish_time` bigint,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`project_id`) USING BTREE,
  INDEX `plannerId`(`planner_id`) USING BTREE,
  INDEX `projectCategory`(`category`) USING BTREE,
  CONSTRAINT `plannerId` FOREIGN KEY (`planner_id`) REFERENCES `planner` (`planner_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `projectCategory` FOREIGN KEY (`category`) REFERENCES `project_category` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for project_category
-- ----------------------------
DROP TABLE IF EXISTS `project_category`;
CREATE TABLE `project_category`  (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_category
-- ----------------------------
INSERT INTO `project_category` VALUES (1, '未选定');
INSERT INTO `project_category` VALUES (2, 'KM');
INSERT INTO `project_category` VALUES (3, '游戏学院');


-- ----------------------------
-- Table structure for project_phases
-- ----------------------------
DROP TABLE IF EXISTS `project_phases`;
CREATE TABLE `project_phases`  (
  `phase_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `plan_id` int(11) NOT NULL,
  PRIMARY KEY (`phase_id`) USING BTREE,
  INDEX `phasesProjectId`(`project_id`) USING BTREE,
  INDEX `phasesPlanId`(`plan_id`) USING BTREE,
  CONSTRAINT `phasesPlanId` FOREIGN KEY (`plan_id`) REFERENCES `test_plan` (`plan_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `phasesProjectId` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for test_platform
-- ----------------------------
DROP TABLE IF EXISTS `test_platform`;
CREATE TABLE `test_platform` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
	`phase_id`int(11) NOT NULL,
  `start_time` bigint,
	`end_time` bigint,
	`pass_rate` float(4,2),
	PRIMARY KEY (`id`) USING BTREE,
	CONSTRAINT `phasesPlatformId` FOREIGN KEY (`id`) REFERENCES `project_phases` (`phase_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `tester_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  INDEX `testTesterId`(`tester_id`) USING BTREE,
  INDEX `testProjectId`(`project_id`) USING BTREE,
  CONSTRAINT `testProjectId` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `testTesterId` FOREIGN KEY (`tester_id`) REFERENCES `tester` (`tester_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for test_plan
-- ----------------------------
DROP TABLE IF EXISTS `test_plan`;
CREATE TABLE `test_plan`  (
  `plan_id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`plan_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test_plan
-- ----------------------------
INSERT INTO `test_plan` VALUES (1, '冒烟测试');
INSERT INTO `test_plan` VALUES (2, '冒烟复核');
INSERT INTO `test_plan` VALUES (3, '一轮测试');
INSERT INTO `test_plan` VALUES (4, '二轮测试');
INSERT INTO `test_plan` VALUES (5, '兼容性测试');
INSERT INTO `test_plan` VALUES (6, '弱网测试');
INSERT INTO `test_plan` VALUES (7, '压力测试');
INSERT INTO `test_plan` VALUES (8, '灵敏度测试');
INSERT INTO `test_plan` VALUES (9, '性能测试');
INSERT INTO `test_plan` VALUES (10, '单元测试');
INSERT INTO `test_plan` VALUES (11, '回归测试');
INSERT INTO `test_plan` VALUES (12, '线上异常');

-- ----------------------------
-- Table structure for tester
-- ----------------------------
DROP TABLE IF EXISTS `tester`;
CREATE TABLE `tester`  (
  `tester_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`tester_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
