-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: dbquantum
-- ------------------------------------------------------
-- Server version	5.5.47-0+deb7u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_account`
--

DROP TABLE IF EXISTS `tb_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_account` (
  `ID` varchar(36) NOT NULL DEFAULT '',
  `U_State` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1: OK, 0: Bad',
  `U_Type` int(11) NOT NULL DEFAULT '3' COMMENT '7: super,3 admin,1 audit',
  `U_Name` varchar(128) NOT NULL DEFAULT '',
  `U_UKey` varchar(36) NOT NULL DEFAULT '' COMMENT 'UKEY Id',
  `U_LdapUid` varchar(128) NOT NULL DEFAULT '' COMMENT 'Ldap User Id',
  `U_Password` varchar(128) NOT NULL DEFAULT '',
  `U_Email` varchar(128) NOT NULL DEFAULT '',
  `U_PhoneNumber` varchar(32) NOT NULL DEFAULT '',
  `U_LastLogin` bigint(20) NOT NULL DEFAULT '0',
  `U_CreateTime` bigint(20) NOT NULL DEFAULT '0',
  `U_LastSync` bigint(20) NOT NULL DEFAULT '0',
  `U_Description` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`),
  KEY `tb_account_id` (`ID`),
  KEY `tb_account_state` (`U_State`),
  KEY `tb_account_name` (`U_Name`),
  KEY `tb_account_type` (`U_Type`),
  KEY `tb_account_ukey` (`U_UKey`),
  KEY `tb_account_ldapuid` (`U_LdapUid`),
  KEY `tb_account_email` (`U_Email`),
  KEY `tb_account_phonenumber` (`U_PhoneNumber`),
  KEY `tb_account_password` (`U_Password`),
  KEY `tb_account_createtime` (`U_CreateTime`),
  KEY `tb_account_lastlogin` (`U_LastLogin`),
  KEY `tb_account_lastsync` (`U_LastSync`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_account`
--

LOCK TABLES `tb_account` WRITE;
/*!40000 ALTER TABLE `tb_account` DISABLE KEYS */;
INSERT INTO `tb_account` VALUES ('c0000000000000000000000000000000',1,7,'admin','','','292f137f691469948acd0e72b141e373','','',0,1513926520000,0,'');
/*!40000 ALTER TABLE `tb_account` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trigger_delete_account AFTER DELETE ON tb_account FOR EACH ROW
BEGIN
DELETE FROM tb_session WHERE S_UserId=old.ID;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `tb_apitrace`
--

DROP TABLE IF EXISTS `tb_apitrace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_apitrace` (
  `ID` varchar(36) NOT NULL DEFAULT '',
  `AT_AccountId` varchar(36) NOT NULL DEFAULT '',
  `AT_Type` varchar(16) NOT NULL DEFAULT 'api' COMMENT 'api or task',
  `AT_ApiId` varchar(200) NOT NULL DEFAULT '',
  `AT_State` varchar(16) NOT NULL DEFAULT 'New' COMMENT 'New,Loaded,Running,ServerRunning,Failed,Finished',
  `AT_Name` varchar(128) NOT NULL DEFAULT '',
  `AT_CreateTime` bigint(20) NOT NULL DEFAULT '0',
  `AT_StartTime` bigint(20) NOT NULL DEFAULT '0',
  `AT_FinishTime` bigint(20) NOT NULL DEFAULT '0',
  `AT_User` varchar(64) NOT NULL DEFAULT '',
  `AT_ServerTaskId` varchar(36) NOT NULL DEFAULT '',
  `AT_Request` varchar(8192) NOT NULL DEFAULT '{}',
  `AT_ServerRequest` varchar(8192) NOT NULL DEFAULT '{}',
  `AT_Reply` text NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `tb_apitrace_id` (`ID`),
  KEY `tb_apitrace_type` (`AT_Type`),
  KEY `tb_apitrace_apiid` (`AT_ApiId`),
  KEY `tb_apitrace_staskid` (`AT_ServerTaskId`),
  KEY `tb_apitrace_user` (`AT_User`),
  KEY `tb_apitrace_accountId` (`AT_AccountId`),
  KEY `tb_apitrace_createtime` (`AT_CreateTime`),
  KEY `tb_apitrace_finishtime` (`AT_FinishTime`),
  KEY `tb_apitrace_starttime` (`AT_StartTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_apitrace`
--

LOCK TABLES `tb_apitrace` WRITE;
/*!40000 ALTER TABLE `tb_apitrace` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_apitrace` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_misc`
--

DROP TABLE IF EXISTS `tb_misc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_misc` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `M_Name` varchar(64) NOT NULL DEFAULT '',
  `M_Value` varchar(64) NOT NULL DEFAULT '',
  `M_Type` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`),
  KEY `tb_misc_id` (`ID`),
  KEY `tb_misc_name` (`M_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_misc`
--

LOCK TABLES `tb_misc` WRITE;
/*!40000 ALTER TABLE `tb_misc` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_misc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_session`
--

DROP TABLE IF EXISTS `tb_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_session` (
  `ID` varchar(36) NOT NULL DEFAULT '',
  `S_UserId` varchar(36) NOT NULL DEFAULT '',
  `S_UserType` tinyint(4) NOT NULL DEFAULT '0' COMMENT '7:superadmin,3:admin,1:audit,0:user',
  `S_UserName` varchar(128) NOT NULL DEFAULT '',
  `S_Cookie` varchar(1024) NOT NULL DEFAULT '',
  `S_CreateTime` bigint(20) NOT NULL DEFAULT '0',
  `S_LastSync` bigint(20) NOT NULL DEFAULT '0',
  `S_ExpireTime` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `tb_session_id` (`ID`),
  KEY `tb_session_userid` (`S_UserId`),
  KEY `tb_session_username` (`S_UserName`),
  KEY `tb_session_createtime` (`S_CreateTime`),
  KEY `tb_session_lastsync` (`S_LastSync`),
  KEY `tb_session_expiretime` (`S_ExpireTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_session`
--

LOCK TABLES `tb_session` WRITE;
/*!40000 ALTER TABLE `tb_session` DISABLE KEYS */;
INSERT INTO `tb_session` VALUES ('00000000000000000000000000000000','c0000000000000000000000000000000',7,'admin','{\"role\": 7, \"id\": \"c0000000000000000000000000000000\", \"name\": \"admin\"}',1511429620148,0,1826789620148);
/*!40000 ALTER TABLE `tb_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'dbquantum'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-22 15:08:40
