-- QA侧测试用数据
INSERT INTO "tester" ("name", "email")
VALUES
	("QA侧测试1", "test1@mail.com"),
	("QA侧测试2", "test2@mail.com"),
	("QA侧测试3", "test3@mail.com");


-- 开发侧测试用数据
INSERT INTO "developer" ("name", "type_id", "email")
VALUES
	("开发侧测试1", 1, "develop1@mail.com"),
	("开发侧测试2", 2, "develop2@mail.com"),
	("开发侧测试3", 3, "develop3@mail.com"),
	("开发侧测试4", 4, "develop4@mail.com");
	

-- 策划侧测试用数据
INSERT INTO "planner" ("name", "email")
VALUES
	("策划侧测试1", "planner1@mail.com"),
	("策划侧测试2", "planner2@mail.com"),
	("策划侧测试3", "planner3@mail.com");


-- 测试用项目
INSERT INTO "project" ("planner_id", "project_name")
VALUES
	(1, "测试用项目1"),
	(2, "测试用项目2"),
	(3, "测试用项目3");


-- 测试用测试跟进数据
INSERT INTO "test" ("tester_id", "project_id")
VALUES
	(1, 1),
	(2, 1),
	(3, 1),
	(2, 2),
	(2, 3),
	(3, 3);


-- 测试用开发跟进数据
INSERT INTO "develop" ("developer_id", "project_id")
VALUES
	(1, 1),
	(2, 1),
	(1, 2),
	(1, 3),
	(2, 3),
	(3, 3),
	(4, 3);
	
-- 测试用项目进度
INSERT INTO "project_phases" ("project_id", "plan_id")
VALUES
	(1, 1),
	(1, 2),
	(1, 3),
	(2, 1),
	(3, 1),
	(3, 2),
	(3, 3);


-- 测试用BUG
INSERT INTO "bug" ("tester_id", "developer_id", "phase_id", "bug_type", "category", "title", "create_time", "close_time", "is_finished", "is_closed", "is_online")
VALUES
	(1, 2, 1, 1, 1, "测试用冒烟异常", 1607153287000, NULL, "false", "false", "true"),
	(2, 1, 3, 1, 1, "测试用回归异常", 1607153287000, NULL, "false", "false", "true"),
	(2, 1, 2, 1, 1, "测试用冒烟异常", 1607153287000, NULL, "false", "false", "false"),
	(1, 1, 4, 1, 1, "测试用冒烟异常", 1607153287000, NULL, "false", "false", "false"),
	(2, 2, 4, 1, 1, "测试用一轮异常", 1607153287000, NULL, "false", "false", "true"),
	(3, 3, 5, 1, 1, "测试用二轮异常", 1607153287000, NULL, "false", "false", "false"),
	(3, 4, 5, 1, 1, "测试用兼容性异常", 1607153287000, NULL, "false", "false", "true");







