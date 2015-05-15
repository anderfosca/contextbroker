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

--
-- Dumping data for table `providers`
--

INSERT INTO `providers` (`provider_id`, `name`, `url`, `version`, `location`, `location_desc`, `updated_at`) VALUES
(8, 'testProv', 'http://testProv', '1.0.0', '49.425323;7.754138', 'Paul-Ehrlich-Strasse 34, TU Kaiserslautern, 67663 Kaiserslautern, Deutschland', '2015-05-04 22:21:30'),
(10, 'testProv3', 'http://testProv3', '1.0.0', ';', '', '2015-05-07 17:49:12'),
(11, 'provTeste', 'http://provTeste', '1.0.0', '0;0', 'aqui', '2015-05-07 18:20:01');

-- --------------------------------------------------------

--
-- Table structure for table `registryTable`
--

CREATE TABLE IF NOT EXISTS `registryTable` (
  `registry_id` int(11) NOT NULL,
  `provider_id` int(11) NOT NULL,
  `entity` varchar(80) CHARACTER SET utf8 NOT NULL,
  `scope_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `expires` datetime NOT NULL,
  `dataPart` varchar(100) CHARACTER SET utf8 NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `scopes`
--

CREATE TABLE IF NOT EXISTS `scopes` (
  `scope_id` int(11) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `urlPath` varchar(100) CHARACTER SET utf8 NOT NULL,
  `entityTypes` varchar(100) CHARACTER SET utf8 NOT NULL,
  `inputs` varchar(100) CHARACTER SET utf8 NOT NULL,
  `provider_id` int(11) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `scopes`
--

INSERT INTO `scopes` (`scope_id`, `name`, `urlPath`, `entityTypes`, `inputs`, `provider_id`, `updated_at`) VALUES
(5, 'test1', '/test/getTest1', 'username,mobile', '[''phone;currentSettings:mobile'', ''cgi;cell:cgi'', ''btList;bt:btList'', ''wfList;wf:wfList'']', 8, '2015-05-04 22:21:30'),
(6, 'test2', '/test/getTest2', 'username', '[''lat;position:latitude'', ''lon;position:longitude'']', 8, '2015-05-04 22:21:30'),
(7, 'test1', '/test/getTest1', 'mobile', '[''phonenr;string'']', 10, '2015-05-07 17:49:12'),
(8, 'scope1', '/scope1', 'username,mobile', '[''lat;position:latitude'', ''lon;position:longitude'']', 11, '2015-05-07 18:20:01'),
(9, 'scope2', '/scope2', 'username,mobile', '[''lat;position:latitude'', ''lon;position:longitude'']', 11, '2015-05-07 18:20:01');

-- --------------------------------------------------------

--
-- Table structure for table `subscriptions`
--

CREATE TABLE IF NOT EXISTS `subscriptions` (
  `subscription_id` int(11) NOT NULL,
  `callbackUrl` varchar(100) CHARACTER SET utf8 NOT NULL,
  `entityID` varchar(30) CHARACTER SET utf8 NOT NULL,
  `entityType` varchar(30) CHARACTER SET utf8 NOT NULL,
  `scopeList` varchar(100) CHARACTER SET utf8 NOT NULL,
  `time` int(11) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  ADD PRIMARY KEY (`registry_id`);

--
-- Indexes for table `scopes`
--
ALTER TABLE `scopes`
  ADD PRIMARY KEY (`scope_id`),
  ADD KEY `provider_id` (`provider_id`);

--
-- Indexes for table `subscriptions`
--
ALTER TABLE `subscriptions`
  ADD PRIMARY KEY (`subscription_id`);

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
  MODIFY `registry_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `scopes`
--
ALTER TABLE `scopes`
  MODIFY `scope_id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `subscriptions`
--
ALTER TABLE `subscriptions`
  MODIFY `subscription_id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;