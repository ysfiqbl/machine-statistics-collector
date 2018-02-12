CREATE DATABASE IF NOT EXISTS mstats;

DROP DATABASE IF EXISTS mstats_test;

CREATE DATABASE mstats_test;

GRANT ALL PRIVILEGES ON mstats.* to root@'%' IDENTIFIED BY 'root!123';
GRANT ALL PRIVILEGES ON mstats_test.* to root@'%' IDENTIFIED BY 'root!123';

flush privileges;

USE mstats_test;

CREATE TABLE `statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) NOT NULL,
  `response` varchar(150) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

CREATE TABLE `emails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `to` varchar(50) NOT NULL,
  `sender` varchar(50) NOT NULL,
  `message` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `retry_count` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

