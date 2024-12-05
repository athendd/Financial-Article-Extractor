-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: financial_information
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `link` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `sum_body` varchar(255) DEFAULT NULL,
  `stocks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (7,'https://finance.yahoo.com/news/elon-musk-drama-intensifies-as-tesla-shareholders-vote-on-his-56b-pay-package-heres-whats-at-stake-145645586.html','Pras Subramanian','Elon Musk drama intensifies as Tesla shareholders vote on his $56B pay package: Here\'s what\'s at stakeWhile Tesla bulls want Musk to get paid and recommit to the EV maker, others believe Musk\'s pay package is excessive and his loyalties are split.','2024-06-13 01:00:00',NULL,NULL,'TSLA, BRK-B'),(8,'https://finance.yahoo.com/news/inflation-eases-in-may-as-consumer-prices-rise-at-slower-than-expected-pace-123413485.html','Alexandra Canal','Inflation eases in May as consumer prices rise at slower-than-expected pace','2024-06-12 05:51:00',NULL,NULL,'IXIC, GSPC, DJI'),(9,'https://finance.yahoo.com/news/tesla-jumps-after-musk-says-shareholders-backed-pay-package-093140071.html','Dana Hull','Tesla jumps after Musk says shareholders backed pay package','2024-06-13 04:44:00',NULL,NULL,'TSLA'),(10,'https://finance.yahoo.com/news/elon-musk-drama-intensifies-as-tesla-shareholders-vote-on-his-56b-pay-package-heres-whats-at-stake-145645586.html','Pras Subramanian','Elon Musk drama intensifies as Tesla shareholders vote on his $56B pay package: Here\'s what\'s at stakeWhile Tesla bulls want Musk to get paid and recommit to the EV maker, others believe Musk\'s pay package is excessive and his loyalties are split.','2024-06-13 01:00:00',NULL,NULL,'TSLA, BRK-B'),(11,'https://finance.yahoo.com/news/jpmorgan-wager-weight-loss-craze-113000634.html','Hannah Levitt','JPMorgan to Wager on Weight-Loss Craze With $500 Million Fund','2024-06-13 04:30:00',NULL,NULL,'JPM'),(12,'https://finance.yahoo.com/news/us-wholesale-prices-dropped-may-123828032.html','PAUL WISEMAN','US wholesale prices dropped in May, adding to evidence that inflation pressures are cooling','2024-06-13 05:38:00',NULL,NULL,NULL);
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-04 21:12:04
