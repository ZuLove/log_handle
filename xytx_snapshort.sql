CREATE DATABASE IF NOT EXISTS `xytx_snapshort` DEFAULT CHARSET=UTF8;
USE `xytx_snapshort`;


DROP TABLE IF EXISTS `game_account`;
CREATE TABLE `game_account`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `date` DATETIME,
    `user_name` VARCHAR(32),
    `password` VARCHAR(32),
    `char_name1` VARCHAR(32),
    `server_name1` VARCHAR(32),
    `bo_change_char_name1` INT,
    `ip_addr` VARCHAR(32),
    `make_date` DATETIME,
    `last_date` DATETIME,
    `anti_addiction` INT,
    `current_day_fist_login_time` DATETIME,
    `online_minutes` INT,

    PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `user_name` VARCHAR(32) DEFAULT NULL,
  `role_name` VARCHAR(32) NOT NULL,
  `primary_key` VARCHAR(32) NOT NULL,
  `paid_type` VARCHAR(32) NOT NULL,
  `master_name` VARCHAR(32) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `group_key` INT DEFAULT NULL,
  `guild_name` VARCHAR(32) DEFAULT NULL,
  `last_date` DATETIME DEFAULT NULL,
  `create_date` DATETIME DEFAULT NULL,
  `sex` INT DEFAULT NULL,
  `x` INT DEFAULT NULL,
  `y` INT DEFAULT NULL,
  `gold_money` INT DEFAULT NULL,
  `light` INT DEFAULT NULL,
  `dark` INT DEFAULT NULL,
  `in_power` INT DEFAULT NULL,
  `out_power` INT DEFAULT NULL,
  `life` INT DEFAULT NULL,
  `adaptive` INT DEFAULT NULL,
  `revival` INT DEFAULT NULL,
  `immunity` INT DEFAULT NULL,
  `virtue` INT DEFAULT NULL,
  `current_in_power` INT DEFAULT NULL,
  `current_out_power` INT DEFAULT NULL,
  `current_life` INT DEFAULT NULL,
  `current_health` INT DEFAULT NULL,
  `current_satiety` INT DEFAULT NULL,
  `current_poisoning` INT DEFAULT NULL,
  `current_head_seek` INT DEFAULT NULL,
  `current_arm_seek` INT DEFAULT NULL,
  `current_leg_seek` INT DEFAULT NULL,

  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `wear_item`;
CREATE TABLE `wear_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `owner` VARCHAR(32) NOT NULL,
  `index` INT NOT NULL,
  `item_id` INT NOT NULL,
  `item_name` VARCHAR(32) NOT NULL,
  `count` INT DEFAULT NULL,
  `color` INT DEFAULT NULL,
  `durability` INT DEFAULT NULL,
  `durabilityMax` INT DEFAULT NULL,
  `smithingLevel` INT DEFAULT NULL,
  `attach` INT DEFAULT NULL,
  `lockState` INT DEFAULT NULL,
  `lockTime` INT DEFAULT NULL,
  `dateTime` DATETIME DEFAULT NULL,
  `boident` INT DEFAULT NULL,
  `startLevel` INT DEFAULT NULL,
  `bBlueprint` INT DEFAULT NULL,
  `specialExp` INT DEFAULT NULL,
  `createName` VARCHAR(32) DEFAULT NULL,
  `dummy1` INT DEFAULT NULL,
  `dummy2` INT DEFAULT NULL,
  `dummy3` INT DEFAULT NULL,
  `dummy4` INT DEFAULT NULL,
  `setting1` VARCHAR(32) DEFAULT NULL,
  `setting2` VARCHAR(32) DEFAULT NULL,
  `setting3` VARCHAR(32) DEFAULT NULL,
  `setting4` VARCHAR(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `bag_item`;
CREATE TABLE `bag_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `owner` VARCHAR(32) NOT NULL,
  `index` INT NOT NULL,
  `item_id` INT NOT NULL,
  `item_name` VARCHAR(32) NOT NULL,
  `count` INT DEFAULT NULL,
  `color` INT DEFAULT NULL,
  `durability` INT DEFAULT NULL,
  `durabilityMax` INT DEFAULT NULL,
  `smithingLevel` INT DEFAULT NULL,
  `attach` INT DEFAULT NULL,
  `lockState` INT DEFAULT NULL,
  `lockTime` INT DEFAULT NULL,
  `dateTime` DATETIME DEFAULT NULL,
  `boident` INT DEFAULT NULL,
  `startLevel` INT DEFAULT NULL,
  `bBlueprint` INT DEFAULT NULL,
  `specialExp` INT DEFAULT NULL,
  `createName` VARCHAR(32) DEFAULT NULL,
  `dummy1` INT DEFAULT NULL,
  `dummy2` INT DEFAULT NULL,
  `dummy3` INT DEFAULT NULL,
  `dummy4` INT DEFAULT NULL,
  `setting1` VARCHAR(32) DEFAULT NULL,
  `setting2` VARCHAR(32) DEFAULT NULL,
  `setting3` VARCHAR(32) DEFAULT NULL,
  `setting4` VARCHAR(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `base_magic`;
CREATE TABLE `base_magic` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `owner` VARCHAR(32) NOT NULL,
  `index` INT NOT NULL,
  `name` VARCHAR(32) NOT NULL,
  `exp` INT NOT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `advanced_magic`;
CREATE TABLE `advanced_magic` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `owner` VARCHAR(32) NOT NULL,
  `index` INT NOT NULL,
  `name` VARCHAR(32) NOT NULL,
  `exp` INT NOT NULL,
  PRIMARY KEY (`id`)
)