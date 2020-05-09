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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,'Wanda Avenue','1156','','Seaside','CA','93955');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brands`
--

LOCK TABLES `brands` WRITE;
/*!40000 ALTER TABLE `brands` DISABLE KEYS */;
INSERT INTO `brands` VALUES ('Nabisco','a brand for safeway',1,'nbc@brash.ru','555555555'),('Crystal Geyser','',2,'',''),('Alkaline88','',4,'',''),('Signature Select','',5,'',''),('Arrowhead','',6,'',''),('Figi','',7,'',''),('Hawaiian Springs','',8,'',''),('AquaHydrate','',9,'',''),('Kona Deep','',10,'',''),('Salvare La Vita','',11,'',''),('VitaNourish','',12,'',''),('Black Water','',13,'',''),('Acqua Panna','',14,'',''),('Hemp','',15,'',''),('Penta','',16,'',''),('Pathwater','',17,'',''),('Just','',18,'',''),('Flow','',19,'',''),('Nestle','',20,'',''),('1907','',21,'','');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'grocery',3336,'descriptions go here');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledger`
--

LOCK TABLES `ledger` WRITE;
/*!40000 ALTER TABLE `ledger` DISABLE KEYS */;
INSERT INTO `ledger` VALUES (1,'2020-03-07 11:30:39');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price`
--

LOCK TABLES `price` WRITE;
/*!40000 ALTER TABLE `price` DISABLE KEYS */;
INSERT INTO `price` VALUES (3,1),(4,0),(5,4),(6,99.99),(7,2),(8,6),(9,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priceUnits`
--

LOCK TABLES `priceUnits` WRITE;
/*!40000 ALTER TABLE `priceUnits` DISABLE KEYS */;
INSERT INTO `priceUnits` VALUES ('Dollar','$',1,'unit of US Currency'),('Dollar','$',2,'');
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
INSERT INTO `price_priceUnits` VALUES (3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1);
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
INSERT INTO `product_brands` VALUES (1,1),(58,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1);
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
INSERT INTO `product_departments` VALUES (1,1),(58,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1);
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
INSERT INTO `product_manufacturers` VALUES (1,1),(58,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1);
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
INSERT INTO `product_price` VALUES (1,3),(58,5),(61,4),(62,6),(63,4),(64,4),(65,7),(69,8),(70,9);
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
INSERT INTO `product_vendors` VALUES (1,1),(58,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1);
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
INSERT INTO `product_weight` VALUES (1,3),(58,5),(61,6),(62,7),(63,6),(64,6),(65,8),(69,9),(70,10);
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
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'OpenNature',0,'','1111111111111','',NULL,'upc_image:1:tank.png'),(2,'Alpine Spring water Sport Bottle',12,'','7514000505','03201309',NULL,NULL),(3,'Alpine Spring Water',6,'','7514000515','08200440',NULL,NULL),(4,'Nursery Purified Water with Flouride',6,'','0710917','65110525',NULL,NULL),(5,'Alkaline88 Himalayan Mineral Enhanced',4,'','85315800411','03200240',NULL,NULL),(6,'Refreshe Drinking Water',6,'','2113007447','08200038',NULL,NULL),(7,'Water Purified Drinking',6,'','2113007503','08200107',NULL,NULL),(8,'Alpine Spring Water',0,'','7514000515','08200440',NULL,NULL),(9,'Spring Water',2,'','0711429','08200014',NULL,NULL),(10,'Refreshe Distilled Water',3,'','2113007507','08200776',NULL,NULL),(11,'Refreshe Distilled Water',6,'','2113007507','08200776',NULL,NULL),(12,'Refreshe Drinking Water',3,'','2113007500','08200050',NULL,NULL),(13,'Fiji Water',0,'','6325600010','03200993',NULL,NULL),(14,'Fiji Water',6,'','63256500009','03200980',NULL,NULL),(15,'Fiji Water',6,'','63256500062','03200982',NULL,NULL),(16,'Fiji Artesian Water Pure',12,'','63256500002','08200169',NULL,NULL),(17,'Fiji Water',12,'','63256500065','03201001',NULL,NULL),(18,'TruSol Ph Balanced Sky Drinking Water',18,'','2113023348','03202008',NULL,NULL),(19,'Hawaiian Springs Water',12,'','66710310000','03201649',NULL,NULL),(20,'AquaHydrate Alkalized Water with Electrolytes',12,'','18213600002','03200069',NULL,NULL),(21,'Kona Deep Water',12,'','85360700134','03200500',NULL,NULL),(22,'Alkaline88 Water 1.5Lt',6,'','85315800424','03200975',NULL,NULL),(23,'Alkaline88 Water',12,'','85315800403','03200335',NULL,NULL),(24,'Refreshe Alkaline Electrolyte Water 1.5Lt',12,'','2113033477','03201421',NULL,NULL),(25,'Refreshe Alkaline Electrolyte Water 1Lt',12,'','2113033475','03201711',NULL,NULL),(26,'Salvare La Vita Water',15,'','85476800302','03200082',NULL,NULL),(27,'VitaNourish multi-vitamin luxury bottle',12,'','85543700629','032551202',NULL,NULL),(28,'Black Water Spring Water',12,'','85345100300','03250200',NULL,NULL),(29,'Acqua Panna',4,'','4150840015','08200028',NULL,NULL),(30,'Hemp Hydrate',12,'','69929100000','03201107',NULL,NULL),(31,'Acqua Panna Spring Water',12,'','4150892248','0320236',NULL,NULL),(32,'Acqua Panna Spring Water',12,'','4150860081','03202037',NULL,NULL),(33,'Acqua Panna mineral water',12,'','4150863448','03200541',NULL,NULL),(34,'Penta Water',12,'','67946110006','08200198',NULL,NULL),(35,'PathWater',12,'','86780100010','03200996',NULL,NULL),(36,'PathWater',0,'','86780100013','03201000',NULL,NULL),(37,'Just Water Lemon Infused',12,'','85305700707','03251199',NULL,NULL),(38,'Just Water Tangerine Infused',12,'','85305700705','03251198',NULL,NULL),(39,'Just Water Water',12,'','86655800000','03200575',NULL,NULL),(40,'Flow Alklaline Spring Water Cucumber Mint',12,'','62805542926','03251072',NULL,NULL),(41,'Flow 100 Natural Canadian Spring Water',12,'','62784346382','03201306',NULL,NULL),(42,'Refreshe Purified Drinking Water',1,'','2113024082','03200084',NULL,NULL),(43,'Refreshe Purified Drinking Water',1,'','2113024032','08200008',NULL,NULL),(44,'Nestle Splash Water Wild Berry',4,'','6827434555','03201406',NULL,NULL),(45,'Crystal Geyser Spring Water',1,'','7514035001','08200411',NULL,NULL),(46,'Arrowhead Mountain Spring Water',1,'','7114200400','03201496',NULL,NULL),(47,'Crystal Geyser Natural Spring Water',2,'','7514006505','03200399',NULL,NULL),(48,'Arrowhead Mountain Spring Water',4,'','7114200948','08200762',NULL,NULL),(49,'Crystal Geyser Roxane Alpine Spring Water',4,'','7514006801','03200212',NULL,NULL),(50,'Nestle PureLife Flavored Water Lemon',4,'','6827491146','08100504',NULL,NULL),(51,'Nestle Pure Life Flavored Water Orange',4,'','6827491147','08100085',NULL,NULL),(52,'Arrowhead Mountain Spring Water',18,'','7114200001','08200357',NULL,NULL),(53,'Arrowhead Mountain Spring Water',28,'','7114264337','03200205',NULL,NULL),(54,'1907 New Water NZ Artisan',8,'','85360500602','03201861',NULL,NULL),(55,'Refreshe Distilled 1 Gallon Water',6,'','021130075188','000000',NULL,NULL),(56,'RockStar XDurance Cotton Candy',4,'cotton flavored energy drink','818094005579','None',NULL,NULL),(57,'RockStar XDurance Fruit Punch',12,'fruit punch flavored energy drink','818094005555','None',NULL,NULL),(58,'test',2,'test','test','test',NULL,NULL),(59,'tablor',4,'tasted','tabloon','domo',NULL,NULL),(60,'ttt',0,'','ttt','tttttt',NULL,NULL),(61,'ttt',4,'','tttt','tttt',NULL,'upc_image:61:cheesy.png'),(62,'dnd',4,'','0000000000','000000000000',NULL,'upc_image:62:screwed.png'),(63,'foobar',4,'','3430000000','99990090',NULL,'upc_image:63:tatoo.png'),(64,'ttt',0,'','tttttt','ttttt','upc_image:64:tatoo.png','upc_image:64:g1348.png'),(65,'test',8,'','test02','test02-home','upc_image:65:tatoo.png','product_image:65:g1348.png'),(66,'taboo',0,'','tabboo','booo',NULL,'product_image:66:screwed.png'),(67,'jjj',0,'','kkk','jjjj',NULL,'product_image:67:tatoo.png'),(68,'aaa',0,'','ggg','iiii',NULL,'product_image:68:tatoo.png'),(69,'Product Name',5,'','universal product code','homecode','upc_image:69:g1348.png','product_image:69:tatoo.png'),(70,'Laboratum',7,'just a test of the weather','0000000000','0000ab3','upc_image:70:g1348.png','product_image:70:tatoo.png');
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
INSERT INTO `user_departments` VALUES (1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','first_name','middle_name','last_name','admin@localhost','1000000000',NULL,1,1,NULL,'$6$rounds=656000$zLQ1tn1OBN2hRTpe$UrGX9eppvx.GfeCG2S0RBUWfBn42HVUXBy4VmzikCDIBW.DIgMCkjZ7Ws7ar6/o1WLM/ZgWFvqTbhoaeLRg1R/'),(2,'carl','carl','joseph','hirner','k.j.hirner.wisdom@gmail.com','8048544057','boost',1,1,'US','$6$rounds=656000$xMG0FvdstaswwfJh$21Ni2kyGZVDhiowJdJIbCrVde58lKvomB83U7ZBYt8q/Sus7Py1LNxNNXerSfT1KGT/z5yoHO.5ToCE9B5as0.'),(3,'admin','first_name','middle_name','last_name','admin@localhost','1000000000',NULL,1,1,NULL,'$6$rounds=656000$3cXBM49.wNl66Zef$He5oegJUaTmV2qYX1dAwDkp82lybkxUebQrJOzBrB5a3DB3V.SJ/dFc7L51cyaJdAYPgXJTm9.ZH5ml2OSq8D/');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight`
--

LOCK TABLES `weight` WRITE;
/*!40000 ALTER TABLE `weight` DISABLE KEYS */;
INSERT INTO `weight` VALUES (3,1),(4,4),(5,3),(6,0),(7,2),(8,6),(9,5),(10,10);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weightUnits`
--

LOCK TABLES `weightUnits` WRITE;
/*!40000 ALTER TABLE `weightUnits` DISABLE KEYS */;
INSERT INTO `weightUnits` VALUES ('Pound','lb',1,'unit of weight'),('Ounce','Oz.',2,'smallest industrially used unit of imperical fluid weight'),('ounce','oz',3,''),('Gallon','GA',4,''),('Liter','LT',5,''),('milliliter','ml',6,'');
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
INSERT INTO `weight_weightUnits` VALUES (3,1),(5,1),(6,1),(7,1),(8,1),(9,2),(10,1);
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

-- Dump completed on 2020-04-24 13:40:48
