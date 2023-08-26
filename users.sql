-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2023 at 02:34 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qpfinder`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(50) NOT NULL,
  `email` varchar(200) NOT NULL,
  `role` varchar(30) NOT NULL,
  `branch` varchar(10) NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT 0,
  `organization` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `email`, `role`, `branch`, `verified`, `organization`) VALUES
('', '', 'student', 'ece', 0, 'RGUKT-NUZVID'),
('ewfef', 'werfwer@gmail.com', 'Student', 'cse', 0, 'rgukt'),
('jyothikiran.thammana@sayukth.com', 'jyothikiran.thammana@sayukth.com', 'student', 'ece', 0, 'RGUKT'),
('jyothikiran30', 'jyothikiran30', 'student', 'ece', 0, 'RGUKT-SKLM'),
('n180333@rguktn.ac.in', 'n180333@rguktn.ac.in', 'student', '', 0, 'Not Company');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `email_index` (`email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
