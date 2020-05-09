-- MariaDB dump 10.17  Distrib 10.4.12-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: safeway
-- ------------------------------------------------------
-- Server version	10.4.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `street_number` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `apartment_suite` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ZIP` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,'Wanda Avenue','1156','','Seaside','CA','93955'),(2,'Wanda Avenue','1156',NULL,'Seaside','CA','93955i-4415');
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `brand_addresses`
--

DROP TABLE IF EXISTS `brand_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brand_addresses` (
  `brand_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  KEY `brand_id` (`brand_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `brand_addresses_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`id`),
  CONSTRAINT `brand_addresses_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand_addresses`
--

LOCK TABLES `brand_addresses` WRITE;
/*!40000 ALTER TABLE `brand_addresses` DISABLE KEYS */;
INSERT INTO `brand_addresses` VALUES (1,1);
/*!40000 ALTER TABLE `brand_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `brands`
--

DROP TABLE IF EXISTS `brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brands` (
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brands`
--

LOCK TABLES `brands` WRITE;
/*!40000 ALTER TABLE `brands` DISABLE KEYS */;
INSERT INTO `brands` VALUES ('Nabisco','a brand for safeway',1,'nbc@brash.ru','555555555');
/*!40000 ALTER TABLE `brands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `store_department_number` int(11) DEFAULT NULL,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'grocery',3336,'descriptions go here'),(2,'General Merchandise',3812,'general merchanise department'),(3,'system_admin',1000,'system administration department'),(4,'Beverege',1002,'a drinks department');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledger`
--

DROP TABLE IF EXISTS `ledger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledger`
--

LOCK TABLES `ledger` WRITE;
/*!40000 ALTER TABLE `ledger` DISABLE KEYS */;
INSERT INTO `ledger` VALUES (1,'2020-03-05 12:17:10'),(2,'2020-03-10 22:11:09'),(3,'2020-03-10 22:12:36'),(4,'2020-03-10 22:21:29'),(5,'2020-03-10 22:27:27'),(6,'2020-03-10 22:28:10');
/*!40000 ALTER TABLE `ledger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledger_products`
--

DROP TABLE IF EXISTS `ledger_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledger_products` (
  `ledger_id` int(11) DEFAULT NULL,
  `productCount_id` int(11) DEFAULT NULL,
  KEY `ledger_id` (`ledger_id`),
  KEY `productCount_id` (`productCount_id`),
  CONSTRAINT `ledger_products_ibfk_1` FOREIGN KEY (`ledger_id`) REFERENCES `ledger` (`id`),
  CONSTRAINT `ledger_products_ibfk_2` FOREIGN KEY (`productCount_id`) REFERENCES `productCount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledger_products`
--

LOCK TABLES `ledger_products` WRITE;
/*!40000 ALTER TABLE `ledger_products` DISABLE KEYS */;
INSERT INTO `ledger_products` VALUES (1,1);
/*!40000 ALTER TABLE `ledger_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledger_user`
--

DROP TABLE IF EXISTS `ledger_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledger_user` (
  `ledger_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  KEY `ledger_id` (`ledger_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ledger_user_ibfk_1` FOREIGN KEY (`ledger_id`) REFERENCES `ledger` (`id`),
  CONSTRAINT `ledger_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledger_user`
--

LOCK TABLES `ledger_user` WRITE;
/*!40000 ALTER TABLE `ledger_user` DISABLE KEYS */;
INSERT INTO `ledger_user` VALUES (1,1);
/*!40000 ALTER TABLE `ledger_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manufacturer_addresses`
--

DROP TABLE IF EXISTS `manufacturer_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `manufacturer_addresses` (
  `manufacturer_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  KEY `manufacturer_id` (`manufacturer_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `manufacturer_addresses_ibfk_1` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturers` (`id`),
  CONSTRAINT `manufacturer_addresses_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manufacturer_addresses`
--

LOCK TABLES `manufacturer_addresses` WRITE;
/*!40000 ALTER TABLE `manufacturer_addresses` DISABLE KEYS */;
INSERT INTO `manufacturer_addresses` VALUES (1,1);
/*!40000 ALTER TABLE `manufacturer_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manufacturers`
--

DROP TABLE IF EXISTS `manufacturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `manufacturers` (
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manufacturers`
--

LOCK TABLES `manufacturers` WRITE;
/*!40000 ALTER TABLE `manufacturers` DISABLE KEYS */;
INSERT INTO `manufacturers` VALUES ('Lucerne',1,'Safeway Product Manufacturer',555555555,'lucerne@brash.ru');
/*!40000 ALTER TABLE `manufacturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price`
--

DROP TABLE IF EXISTS `price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `price` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price`
--

LOCK TABLES `price` WRITE;
/*!40000 ALTER TABLE `price` DISABLE KEYS */;
INSERT INTO `price` VALUES (3,1);
/*!40000 ALTER TABLE `price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `priceUnits`
--

DROP TABLE IF EXISTS `priceUnits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `priceUnits` (
  `name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priceUnits`
--

LOCK TABLES `priceUnits` WRITE;
/*!40000 ALTER TABLE `priceUnits` DISABLE KEYS */;
INSERT INTO `priceUnits` VALUES ('Dollar','$',1,'unit of US Currency');
/*!40000 ALTER TABLE `priceUnits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price_priceUnits`
--

DROP TABLE IF EXISTS `price_priceUnits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `price_priceUnits` (
  `price_id` int(11) DEFAULT NULL,
  `priceUnits_id` int(11) DEFAULT NULL,
  KEY `price_id` (`price_id`),
  KEY `priceUnits_id` (`priceUnits_id`),
  CONSTRAINT `price_priceUnits_ibfk_1` FOREIGN KEY (`price_id`) REFERENCES `price` (`id`),
  CONSTRAINT `price_priceUnits_ibfk_2` FOREIGN KEY (`priceUnits_id`) REFERENCES `priceUnits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price_priceUnits`
--

LOCK TABLES `price_priceUnits` WRITE;
/*!40000 ALTER TABLE `price_priceUnits` DISABLE KEYS */;
INSERT INTO `price_priceUnits` VALUES (3,1);
/*!40000 ALTER TABLE `price_priceUnits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productCount`
--

DROP TABLE IF EXISTS `productCount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productCount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `units` int(11) DEFAULT NULL,
  `cases` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productCount`
--

LOCK TABLES `productCount` WRITE;
/*!40000 ALTER TABLE `productCount` DISABLE KEYS */;
INSERT INTO `productCount` VALUES (1,12,1);
/*!40000 ALTER TABLE `productCount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productCount_product`
--

DROP TABLE IF EXISTS `productCount_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productCount_product` (
  `product_id` int(11) DEFAULT NULL,
  `productCount_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `productCount_id` (`productCount_id`),
  CONSTRAINT `productCount_product_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `productCount_product_ibfk_2` FOREIGN KEY (`productCount_id`) REFERENCES `productCount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productCount_product`
--

LOCK TABLES `productCount_product` WRITE;
/*!40000 ALTER TABLE `productCount_product` DISABLE KEYS */;
INSERT INTO `productCount_product` VALUES (1,1);
/*!40000 ALTER TABLE `productCount_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_brands`
--

DROP TABLE IF EXISTS `product_brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_brands` (
  `product_id` int(11) DEFAULT NULL,
  `brands_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `brands_id` (`brands_id`),
  CONSTRAINT `product_brands_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_brands_ibfk_2` FOREIGN KEY (`brands_id`) REFERENCES `brands` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_brands`
--

LOCK TABLES `product_brands` WRITE;
/*!40000 ALTER TABLE `product_brands` DISABLE KEYS */;
INSERT INTO `product_brands` VALUES (1,1);
/*!40000 ALTER TABLE `product_brands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_departments`
--

DROP TABLE IF EXISTS `product_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_departments` (
  `product_id` int(11) DEFAULT NULL,
  `departments_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `departments_id` (`departments_id`),
  CONSTRAINT `product_departments_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_departments_ibfk_2` FOREIGN KEY (`departments_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_departments`
--

LOCK TABLES `product_departments` WRITE;
/*!40000 ALTER TABLE `product_departments` DISABLE KEYS */;
INSERT INTO `product_departments` VALUES (1,1);
/*!40000 ALTER TABLE `product_departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_manufacturers`
--

DROP TABLE IF EXISTS `product_manufacturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_manufacturers` (
  `product_id` int(11) DEFAULT NULL,
  `manufacturers_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `manufacturers_id` (`manufacturers_id`),
  CONSTRAINT `product_manufacturers_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_manufacturers_ibfk_2` FOREIGN KEY (`manufacturers_id`) REFERENCES `manufacturers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_manufacturers`
--

LOCK TABLES `product_manufacturers` WRITE;
/*!40000 ALTER TABLE `product_manufacturers` DISABLE KEYS */;
INSERT INTO `product_manufacturers` VALUES (1,1);
/*!40000 ALTER TABLE `product_manufacturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_price`
--

DROP TABLE IF EXISTS `product_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_price` (
  `product_id` int(11) DEFAULT NULL,
  `price_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `price_id` (`price_id`),
  CONSTRAINT `product_price_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_price_ibfk_2` FOREIGN KEY (`price_id`) REFERENCES `price` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_price`
--

LOCK TABLES `product_price` WRITE;
/*!40000 ALTER TABLE `product_price` DISABLE KEYS */;
INSERT INTO `product_price` VALUES (1,3);
/*!40000 ALTER TABLE `product_price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_vendors`
--

DROP TABLE IF EXISTS `product_vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_vendors` (
  `product_id` int(11) DEFAULT NULL,
  `vendors_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `vendors_id` (`vendors_id`),
  CONSTRAINT `product_vendors_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_vendors_ibfk_2` FOREIGN KEY (`vendors_id`) REFERENCES `vendors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_vendors`
--

LOCK TABLES `product_vendors` WRITE;
/*!40000 ALTER TABLE `product_vendors` DISABLE KEYS */;
INSERT INTO `product_vendors` VALUES (1,1);
/*!40000 ALTER TABLE `product_vendors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_weight`
--

DROP TABLE IF EXISTS `product_weight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_weight` (
  `product_id` int(11) DEFAULT NULL,
  `weight_id` int(11) DEFAULT NULL,
  KEY `product_id` (`product_id`),
  KEY `weight_id` (`weight_id`),
  CONSTRAINT `product_weight_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_weight_ibfk_2` FOREIGN KEY (`weight_id`) REFERENCES `weight` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_weight`
--

LOCK TABLES `product_weight` WRITE;
/*!40000 ALTER TABLE `product_weight` DISABLE KEYS */;
INSERT INTO `product_weight` VALUES (1,3);
/*!40000 ALTER TABLE `product_weight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `case_count` int(11) DEFAULT NULL,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `upc` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `home_code` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `upc_image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'OpenNature',0,'','','',NULL,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_addresses`
--

DROP TABLE IF EXISTS `user_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_addresses` (
  `user_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `user_addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_addresses_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_addresses`
--

LOCK TABLES `user_addresses` WRITE;
/*!40000 ALTER TABLE `user_addresses` DISABLE KEYS */;
INSERT INTO `user_addresses` VALUES (1,1);
/*!40000 ALTER TABLE `user_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_departments`
--

DROP TABLE IF EXISTS `user_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_departments` (
  `user_id` int(11) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `user_departments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_departments_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_departments`
--

LOCK TABLES `user_departments` WRITE;
/*!40000 ALTER TABLE `user_departments` DISABLE KEYS */;
INSERT INTO `user_departments` VALUES (1,1),(1,1),(1,2),(2,1),(2,1),(2,2);
/*!40000 ALTER TABLE `user_departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `carrier` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  `region` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`active` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`admin` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','first_name','middle_name','last_name','admin@localhost','1000000000',NULL,1,1,NULL,'$6$rounds=656000$QKjStbdSsH5zhsTk$NZ/Pg2370I5YQLzPPVG.xbJ1fWV7MqWW/RVjfBLn5r7RXFvrr.UWIAos3miSOOXAmcxjoDQ.Og0nR2nlTPe3B/'),(2,'carl','carl','joseph','hirner','k.j.hirner.wisdom@gmail.com','8048544057','boost',1,1,'US','$6$rounds=656000$Q4IozmfKj1OGVWsP$ZwCzpJiiksXbuuOJKSmRk2nV0xof4FSUeYv9cJJ611.wbC1KGaHiK3.NtVNAsuoHK1bmT8RWUzsKX9CazoJ75/'),(6,'karl','Karl','Joseph','Hirner','k.j.hirner.wisdom@gmail.com','8048544057','BOOST',1,0,'US','$6$rounds=656000$xRvisDnNC2pPTS5H$oh8iWr721.wY/JIvSE1PhwfoRibh0f8UoEYJYSwbBvP3nASG6/z.n8gcWb3ix5QbiXdWsphEZBlaJFL.0HcN91'),(7,'karl','Karl','Joseph','Hirner','k.j.hirner.wisdom@gmail.com','8048544057','BOOST',1,0,'US','$6$rounds=656000$lWhdCbVrEUUCroAT$r0ZHeeUyX5TT1avC2NdrbDbc62ygqK6fGBoPuhSjFKTBXR0FcoUeuM6EPIm2UEwucBRnVpbLc3eOAMr4/.aK90'),(8,'karl','Karl','Joseph','Hirner','k.j.hirner.wisdom@gmail.com','8048544057','BOOST',1,0,'US','$6$rounds=656000$AvIcTxbvXi88OSgw$V2xnuA.hEqUS1Kx20V2mr3qXlscW1z7CdgkIDDsuNWQ0CGMONyqK8XTtuxt5NDBpsQlPnKiolBzx1aXH1R/dQ.');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_addresses`
--

DROP TABLE IF EXISTS `vendor_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendor_addresses` (
  `vendor_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  KEY `vendor_id` (`vendor_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `vendor_addresses_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`),
  CONSTRAINT `vendor_addresses_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_addresses`
--

LOCK TABLES `vendor_addresses` WRITE;
/*!40000 ALTER TABLE `vendor_addresses` DISABLE KEYS */;
INSERT INTO `vendor_addresses` VALUES (1,1);
/*!40000 ALTER TABLE `vendor_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors`
--

DROP TABLE IF EXISTS `vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendors` (
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors`
--

LOCK TABLES `vendors` WRITE;
/*!40000 ALTER TABLE `vendors` DISABLE KEYS */;
INSERT INTO `vendors` VALUES ('Nabisco','a vendor for safeway',1,'nbc@brash.ru','555555555');
/*!40000 ALTER TABLE `vendors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight`
--

DROP TABLE IF EXISTS `weight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weight` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight`
--

LOCK TABLES `weight` WRITE;
/*!40000 ALTER TABLE `weight` DISABLE KEYS */;
INSERT INTO `weight` VALUES (3,1),(4,4);
/*!40000 ALTER TABLE `weight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weightUnits`
--

DROP TABLE IF EXISTS `weightUnits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weightUnits` (
  `name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weightUnits`
--

LOCK TABLES `weightUnits` WRITE;
/*!40000 ALTER TABLE `weightUnits` DISABLE KEYS */;
INSERT INTO `weightUnits` VALUES ('Pound','lb',1,'unit of weight');
/*!40000 ALTER TABLE `weightUnits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_weightUnits`
--

DROP TABLE IF EXISTS `weight_weightUnits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weight_weightUnits` (
  `weight_id` int(11) DEFAULT NULL,
  `weightUnits_id` int(11) DEFAULT NULL,
  KEY `weight_id` (`weight_id`),
  KEY `weightUnits_id` (`weightUnits_id`),
  CONSTRAINT `weight_weightUnits_ibfk_1` FOREIGN KEY (`weight_id`) REFERENCES `weight` (`id`),
  CONSTRAINT `weight_weightUnits_ibfk_2` FOREIGN KEY (`weightUnits_id`) REFERENCES `weightUnits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_weightUnits`
--

LOCK TABLES `weight_weightUnits` WRITE;
/*!40000 ALTER TABLE `weight_weightUnits` DISABLE KEYS */;
INSERT INTO `weight_weightUnits` VALUES (3,1);
/*!40000 ALTER TABLE `weight_weightUnits` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-23 23:07:39
