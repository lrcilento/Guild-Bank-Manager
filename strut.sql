CREATE DATABASE `MyWoWGuild` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `Ranks` (
  `name` varchar(45) NOT NULL,
  `payment` double NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Council` (
  `counselor` varchar(45) NOT NULL,
  `rank_name` varchar(45) NOT NULL,
  PRIMARY KEY (`counselor`),
  UNIQUE KEY `counselor_UNIQUE` (`counselor`),
  KEY `fk_Council_1_idx` (`rank_name`),
  CONSTRAINT `fk_Council_1` FOREIGN KEY (`rank_name`) REFERENCES `Ranks` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Itens` (
  `name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Earnings` (
  `id` varchar(45) NOT NULL,
  `month` varchar(45) NOT NULL,
  `year` int NOT NULL,
  `boe_earnings` int NOT NULL,
  `total_purchases` int NOT NULL,
  `total_salaries` int NOT NULL,
  `result` int NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item` varchar(45) NOT NULL,
  `qnt` int NOT NULL,
  `total` int NOT NULL,
  `transaction_date` varchar(45) NOT NULL,
  `transaction_day` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_id_UNIQUE` (`id`),
  KEY `fk_Purchases_1_idx` (`item`),
  KEY `fk_Purchases_2_idx` (`transaction_date`),
  CONSTRAINT `fk_Purchases_1` FOREIGN KEY (`item`) REFERENCES `Itens` (`name`),
  CONSTRAINT `fk_Purchases_2` FOREIGN KEY (`transaction_date`) REFERENCES `Earnings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `BoEs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item` varchar(45) NOT NULL,
  `price` int NOT NULL,
  `ilvl` int NOT NULL,
  `socket` varchar(45) NOT NULL,
  `transaction_date` varchar(45) NOT NULL,
  `transaction_day` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_BoEs_1_idx` (`item`),
  KEY `fk_BoEs_2_idx` (`transaction_date`),
  CONSTRAINT `fk_BoEs_1` FOREIGN KEY (`item`) REFERENCES `Itens` (`name`),
  CONSTRAINT `fk_BoEs_2` FOREIGN KEY (`transaction_date`) REFERENCES `Earnings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;