-- phpMyAdmin SQL Dump
-- version 4.4.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 15, 2015 at 03:31 PM
-- Server version: 5.5.41-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `broker`
--
CREATE DATABASE IF NOT EXISTS `broker` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `broker`;

-- --------------------------------------------------------

--
-- Table structure for table `entities`
--

CREATE TABLE IF NOT EXISTS `entities` (
  `entity_id` int(11) NOT NULL,
  `name` varchar(80) CHARACTER SET utf8 NOT NULL,
  `type` varchar(80) CHARACTER SET utf8 NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `providers`
--

CREATE TABLE IF NOT EXISTS `providers` (
  `provider_id` int(11) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `url` varchar(100) CHARACTER SET utf8 NOT NULL,
  `version` varchar(100) CHARACTER SET utf8 NOT NULL,
  `location` varchar(100) CHARACTER SET utf8 NOT NULL,
  `location_desc` varchar(255) CHARACTER SET utf8 NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `registryTable`
--

CREATE TABLE IF NOT EXISTS `registryTable` (
  `registry_id` int(11) NOT NULL,
  `provider_id` int(11) NOT NULL,
  `scope_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL,
  `timestamp` varchar(80) CHARACTER SET utf8 NOT NULL,
  `expires` varchar(80) CHARACTER SET utf8 NOT NULL,
  `dataPart` varchar(100) CHARACTER SET utf8 NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `scopes`
--

CREATE TABLE IF NOT EXISTS `scopes` (
  `scope_id` int(11) NOT NULL,
  `provider_id` int(11) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `urlPath` varchar(100) CHARACTER SET utf8 NOT NULL,
  `entityTypes` varchar(100) CHARACTER SET utf8 NOT NULL,
  `inputs` varchar(100) CHARACTER SET utf8 NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `scopes_subscriptions`
--

CREATE TABLE IF NOT EXISTS `scopes_subscriptions` (
  `scope_id` int(11) NOT NULL,
  `subscription_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `subscriptions`
--

CREATE TABLE IF NOT EXISTS `subscriptions` (
  `subscription_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL,
  `callbackUrl` varchar(100) CHARACTER SET utf8 NOT NULL,
  `minutes` int(11) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `entities`
--
ALTER TABLE `entities`
  ADD PRIMARY KEY (`entity_id`);

--
-- Indexes for table `providers`
--
ALTER TABLE `providers`
  ADD PRIMARY KEY (`provider_id`),
  ADD UNIQUE KEY `unique_name` (`name`),
  ADD UNIQUE KEY `unique_url` (`url`);

--
-- Indexes for table `registryTable`
--
ALTER TABLE `registryTable`
  ADD PRIMARY KEY (`registry_id`),
  ADD KEY `scope` (`scope_id`),
  ADD KEY `providerid` (`provider_id`) USING BTREE,
  ADD KEY `entityid` (`entity_id`) USING BTREE;

--
-- Indexes for table `scopes`
--
ALTER TABLE `scopes`
  ADD PRIMARY KEY (`scope_id`),
  ADD KEY `provider_id` (`provider_id`);

--
-- Indexes for table `scopes_subscriptions`
--
ALTER TABLE `scopes_subscriptions`
  ADD KEY `subscription_subscriptions` (`subscription_id`),
  ADD KEY `scope_scopes` (`scope_id`) USING BTREE;

--
-- Indexes for table `subscriptions`
--
ALTER TABLE `subscriptions`
  ADD PRIMARY KEY (`subscription_id`),
  ADD KEY `entity` (`entity_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `entities`
--
ALTER TABLE `entities`
  MODIFY `entity_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `providers`
--
ALTER TABLE `providers`
  MODIFY `provider_id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `registryTable`
--
ALTER TABLE `registryTable`
  MODIFY `registry_id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `scopes`
--
ALTER TABLE `scopes`
  MODIFY `scope_id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `subscriptions`
--
ALTER TABLE `subscriptions`
  MODIFY `subscription_id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `registryTable`
--
ALTER TABLE `registryTable`
  ADD CONSTRAINT `entity` FOREIGN KEY (`entity_id`) REFERENCES `entities` (`entity_id`),
  ADD CONSTRAINT `providerid` FOREIGN KEY (`provider_id`) REFERENCES `providers` (`provider_id`),
  ADD CONSTRAINT `scope` FOREIGN KEY (`scope_id`) REFERENCES `scopes` (`scope_id`);

--
-- Constraints for table `scopes`
--
ALTER TABLE `scopes`
  ADD CONSTRAINT `provider` FOREIGN KEY (`provider_id`) REFERENCES `providers` (`provider_id`);

--
-- Constraints for table `scopes_subscriptions`
--
ALTER TABLE `scopes_subscriptions`
  ADD CONSTRAINT `subscription_subscriptions` FOREIGN KEY (`subscription_id`) REFERENCES `subscriptions` (`subscription_id`);

--
-- Constraints for table `subscriptions`
--
ALTER TABLE `subscriptions`
  ADD CONSTRAINT `entityid` FOREIGN KEY (`entity_id`) REFERENCES `entities` (`entity_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;