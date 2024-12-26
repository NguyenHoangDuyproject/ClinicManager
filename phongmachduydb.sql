-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 24, 2024 at 11:11 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `phongkham`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('f86e9c4c386f');

-- --------------------------------------------------------

--
-- Table structure for table `examination_bill`
--

CREATE TABLE `examination_bill` (
  `examination_date` date DEFAULT NULL,
  `medicine_money` float DEFAULT NULL,
  `examination_money` float DEFAULT NULL,
  `medical_bill_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `paid` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `examination_bill`
--

INSERT INTO `examination_bill` (`examination_date`, `medicine_money`, `examination_money`, `medical_bill_id`, `patient_id`, `paid`, `id`) VALUES
('2024-12-15', 100000, 100000, 1, 15, 1, 1),
('2024-12-13', 260000, 100000, 2, 18, 1, 2),
('2024-12-23', -1, 100000, 3, 26, 1, 3),
('2024-12-23', -1, 100000, 4, 27, 0, 4),
('2024-12-23', 6000, 100000, 5, 31, 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `medical_bill`
--

CREATE TABLE `medical_bill` (
  `examination_date` date DEFAULT NULL,
  `symptom` text NOT NULL,
  `disease_prediction` text DEFAULT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `medical_bill`
--

INSERT INTO `medical_bill` (`examination_date`, `symptom`, `disease_prediction`, `patient_id`, `doctor_id`, `id`) VALUES
('2024-12-15', 'Đau đầu', 'Cảm cúm', 15, 16, 1),
('2024-12-13', 'Ho', 'Sốt', 18, 21, 2),
('2024-12-23', 'mn;lm;', 'l;ml;mm', 26, 23, 3),
('2024-12-23', '', '', 27, 23, 4),
('2024-12-23', 'Ho', 'Sốt', 31, 23, 5);

-- --------------------------------------------------------

--
-- Table structure for table `medical_bill_detail`
--

CREATE TABLE `medical_bill_detail` (
  `quantity` int(11) DEFAULT NULL,
  `medicine_id` int(11) NOT NULL,
  `medical_bill_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `medical_bill_detail`
--

INSERT INTO `medical_bill_detail` (`quantity`, `medicine_id`, `medical_bill_id`, `id`) VALUES
(10, 31, 1, 1),
(20, 21, 2, 2),
(2, 15, 5, 3);

-- --------------------------------------------------------

--
-- Table structure for table `medicine`
--

CREATE TABLE `medicine` (
  `name` varchar(255) NOT NULL,
  `price` float DEFAULT NULL,
  `description` text DEFAULT NULL,
  `direction` text DEFAULT NULL,
  `unit_in_stock` int(11) DEFAULT NULL,
  `unit_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `medicine`
--

INSERT INTO `medicine` (`name`, `price`, `description`, `direction`, `unit_in_stock`, `unit_id`, `id`) VALUES
('A.T Alugela', 1500, 'Viêm thực quản, viêm dạ dày cấp và mạn tính, viêm loét dạ dày tá tràng, kích ứng dạ dày, ợ chua, rát bỏng', '1-2 gói thuốc, từ 2-3 lần mỗi ngày, uống trước ăn 30 phút.', 100, 4, 1),
('A.T Bisoprolol 5', 500, 'điều trị tăng huyết áp, đau thắt ngực ổn định mạn tính, suy tim mạn tính', 'Uống thuốc với nhiều nước, nên dùng thuốc vào buổi sáng khi đói hoặc lúc điểm tâm. Không được nhai.', 100, 3, 2),
('A.T Furosemid inj', 750, 'điều trị phù, tăng huyết áp thể nhẹ và trung bình', 'uống ngay sau khi ăn bữa ăn chính.', 100, 1, 3),
('A.T Hydrocortisone', 5000, 'sử dụng điều trị chống viêm như viêm khớp, lupus, bệnh gout, viêm khớp vảy nến, viêm loét ruột.', 'Dùng thuốc đường tiêm khi người bệnh không thể tiếp nhận thuốc bằng đường khác.', 100, 1, 4),
('A.T Nitroglycerin inj', 50000, 'Suy tim, nhồi máu cơ tim cấp, phù phổi cấp do tim, đau thắt ngực trầm trọng.', 'i pha loãng trong dextrose 5% hoặc natri clorid 0,9% trước khi truyền tinh mach.', 100, 1, 5),
('A.T Sucralfate', 1100, 'điều trị viêm loét dạ dày tá tràng.', '1g/lần, 4 lần/ngày (uống 1 giờ trước 3 bữa ăn và trước khi đi ngủ)', 100, 4, 6),
('Acecyst ', 200, 'Acecyst thuốc có tác dụng long đờm, được sử dụng để làm thông đường hô hấp', 'Sử dụng liều 1 viên/ lần, ngày 3 lần.', 100, 3, 7),
('Acefalgan', 550, 'giảm đau và hạ sốt, có tác dụng giảm đau từ nhẹ đến trung bình và hạ sốt.', 'Uống một viên mỗi 4 đến 6 giờ, nếu bạn cần. Không uống nhiều hơn 4 viên trong bất kỳ 24 giờ nào.', 100, 3, 8),
('Adrenalin', 2500, 'ác dụng kích thích hệ thần kinh giao cảm, kích thích cả thụ thể alpha và thụ thể beta của thần kinh giao cảm', 'Tiêm dưới da hoặc tiêm bắp từ 0,3-0,5 ml dung dịch tỷ lệ 1:1000, nhắc lại 5 phút một lần tùy theo huyết áp của bệnh nhân.', 100, 1, 9),
('Agifuros', 90, 'làm tăng thải trừ các ion kéo theo nước, tăng lưu lượng máu, tăng độ lọc ở cầu thận', 'Thuốc Agifuros 40mg được dùng đường uống. Nên uống trọn viên thuốc với một ly nước đầy.', 100, 2, 10),
('Bepracid 20', 500, 'có tác dụng ức chế tiết acid dạ dày trong điều kiện bình thường và trong cả tình trạng kích thích ', '20 mg/ lần/ ngày trong 4 – 8 tuần.', 100, 2, 11),
('Bicebid 200', 1000, 'sử dụng trong việc điều trị các bệnh nhiễm khuẩn như: nhiễm khuẩn đường tiết niệu và nhiễm khuẩn đường hô hấp trên - dưới', 'dùng liều 300mg/ngày', 100, 2, 12),
('Bifucil', 600, 'Bifucil thuộc nhóm thuốc trị ký sinh trùng, chống nhiễm khuẩn, kháng virus và kháng nấm.', 'Uống 1 viên/ lần, 1 – 2 lần/ngày. Dùng trong 7 - 14 ngày.', 100, 2, 13),
('Captagim', 76, 'Captagim thuộc nhóm thuốc tim mạch, được bào chế dưới dạng viên nén', '25mg x 2 - 3 lần/ ngày. Trường hợp bệnh nặng có thể tăng liều Captagim đến 50mg x 3 lần/ ngày;', 100, 3, 14),
('Cerecaps', 3000, 'thuốc điều trị thiếu máu não là một thuốc có nguồn gốc dược liệu, được điều chế ở dạng viên nang cứng', 'uống 2-3 viên mỗi lần, ngày dùng 2 lần.', 100, 2, 15),
('Ciloxan', 69000, 'Thuốc Ciloxan có dạng bào chế là dung dịch nhỏ mắt.', 'Trong 6 giờ đầu nhỏ 2 giọt sau mỗi 15 phút, 4 giờ sau thì 2 giọt sau mỗi 30 phút.', 100, 1, 16),
('Clanzen', 200, 'thuốc chống dị ứng', ' 5mg/ngày, 2 ngày dùng 1 lần.', 100, 3, 17),
('Comegim', 365, 'thành phần chính là perindopril erbumin, là thuốc điều trị tăng huyết áp.', 'Thuốc thường được cho uống một lần/ngày vào buổi sáng, lúc đói (trước bữa ăn).', 100, 3, 18),
('Daflon', 3258, 'Thuốc có tác dụng làm giảm sức căng và tình trạng ứ trệ của tĩnh mạch, bảo vệ, làm tăng bền của các mạch máu nhỏ.', 'uống 1 viên x2 lần/ngày vào các bữa ăn.', 100, 3, 19),
('Desloratadin', 160, 'giúp người bệnh nâng cao hiệu quả điều trị và tránh được những tác dụng phụ không mong muốn.', 'liều khuyến cáo là 5 mg, 2 ngày uống 1 lần (uống cách ngày).', 100, 3, 20),
('Dextrose', 13000, 'bổ sung glucose cho những đối tượng dễ bị hạ đường huyết như suy dinh dưỡng', 'sử dụng từ 10- 25g, có thể lặp lại trong trường hợp nghiêm trọng;', 100, 1, 21),
('Dimedrol', 650, 'tác dụng kháng histamin, an thần, chống nôn và chống co thắt', 'Tiêm bắp hoặc tĩnh mạch, 10 – 50mg/lần.', 100, 1, 22),
('Entacron 25', 1500, 'thuốc được sử dụng trong các bệnh lý như bệnh thận, bệnh gan, bệnh tim gây ra phù, cổ chướng và cũng được dùng phối hợp trong bệnh tăng huyết áp.', 'Liều ban đầu uống 50- 100 mg/ngày, chia từ 2 đến 4 lần, dùng ít nhất 2 tuần', 100, 3, 23),
('Erolin', 2500, 'Thuốc được sử dụng trong điều trị dị ứng, mày đay,... ', 'Dùng liều 10mg/ngày, tương đương 1 viên thuốc Erolin 10mg/ngày;', 100, 2, 24),
('Expas 40', 760, 'một loại thuốc chống co thắt được sử dụng để thư giãn các cơ trơn như của đường tiêu hóa', 'Uống 1-2 viên một lần uống 3 lần/ngày.', 100, 2, 25),
('Fefasdin', 10500, 'thuốc chống dị ứng (thuộc nhóm thuốc kháng Histamin thế hệ 2) thường dùng trong các trường hợp quá mẫn cảm, dị ứng theo mùa, ...', 'Uống 60mg/lần, ngày chia 2 lần. Nếu dùng Fefasdin 120 hay 180 thì uống 1 viên trong ngày;', 100, 1, 26),
('Fenilham', 11500, 'thuốc giảm đau thuộc nhóm opioid, thường được chỉ định giảm đau trong ung thư, phẫu thuật gây mê và giảm đau sau phẫu thuật.', ' 50 – 100 microgam/ lần. Tiêm tĩnh mạch tốc độ chậm.', 100, 1, 27),
('Galanmer', 400, 'huộc nhóm vitamin và khoáng chất, thuốc Galanmer có tác dụng điều trị và phòng ngừa thiếu vitamin B12', '1 lần/ viên và uống 3 lần/ ngày.', 100, 2, 28),
('Gyoryg', 600, 'người tăng glucose máu (đặc biệt tăng glucose máu sau khi ăn) không kiểm soát được chỉ bằng chế độ ăn và tập luyện.', 'Uống acarbose vào đầu bữa ăn để giảm nồng độ glucose máu sau ăn', 100, 3, 29),
('Hapacol', 1500, 'Hapacol được sử dụng phổ biến trong điều trị các triệu chứng thường gặp như sốt cao, đau đầu, mệt mỏi,…', '1 viên/lần, nếu người bệnh bị đau nhức nghiêm trọng có thể dùng 2 viên/lần hoặc sử dụng theo chỉ định của bác sĩ.', 100, 4, 30),
('Paracetamol', 10000, 'Thuốc giảm đau, hạ sốt.', 'Uống 1-2 viên mỗi lần, cách nhau 4-6 tiếng.', 100, 7, 31),
('Amoxicillin', 15000, 'Kháng sinh điều trị nhiễm trùng.', 'Uống theo chỉ định của bác sĩ.', 50, 8, 32);

-- --------------------------------------------------------

--
-- Table structure for table `medicine_tag`
--

CREATE TABLE `medicine_tag` (
  `tag_id` int(11) NOT NULL,
  `medicine_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `medicine_tag`
--

INSERT INTO `medicine_tag` (`tag_id`, `medicine_id`, `id`) VALUES
(1, 31, 1),
(2, 32, 2);

-- --------------------------------------------------------

--
-- Table structure for table `registration_form`
--

CREATE TABLE `registration_form` (
  `user_id` int(11) NOT NULL,
  `examination_date` date NOT NULL,
  `accepted` tinyint(1) DEFAULT NULL,
  `used` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_form`
--

INSERT INTO `registration_form` (`user_id`, `examination_date`, `accepted`, `used`, `id`) VALUES
(21, '2024-12-25', 1, 0, 5),
(23, '2024-12-26', 0, 0, 6),
(24, '2024-12-24', 0, 0, 7),
(26, '2024-12-23', 1, 1, 9),
(27, '2024-12-23', 1, 1, 10),
(31, '2024-12-23', 1, 1, 11),
(23, '2025-01-03', 0, 0, 12),
(33, '2024-12-24', 0, 0, 13);

-- --------------------------------------------------------

--
-- Table structure for table `regulation`
--

CREATE TABLE `regulation` (
  `key` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `value` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `regulation`
--

INSERT INTO `regulation` (`key`, `description`, `value`, `user_id`, `id`) VALUES
('user_in_1_day', 'Số bệnh nhân khám trong 1 ngày', 40, 1, 1),
('examination_price', 'Giá khám bệnh', 100000, NULL, 2);

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `name` varchar(255) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`name`, `id`) VALUES
('Giảm đau', 1),
('Kháng sinh', 2);

-- --------------------------------------------------------

--
-- Table structure for table `unit`
--

CREATE TABLE `unit` (
  `name` varchar(50) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `unit`
--

INSERT INTO `unit` (`name`, `id`) VALUES
('Chai', 1),
('Vĩ', 2),
('Viên', 3),
('Gói', 4),
('Chai', 5),
('Vĩ', 6),
('Viên', 7),
('Gói', 8);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `fullname` varchar(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(11) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `role` enum('Admin','Customer','Nurse','Doctor') DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`fullname`, `username`, `password`, `avatar`, `gender`, `birthday`, `email`, `phone`, `active`, `created_date`, `role`, `id`) VALUES
('Admin', 'admin', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2024-12-02', NULL, '0386904554', 1, '2024-12-02 15:59:42', 'Admin', 1),
('NguoiKham 0', 'nguoikham0', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0900000000', 1, '2024-12-02 15:59:42', 'Customer', 2),
('NguoiKham 1', 'nguoikham1', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0911111111', 1, '2024-12-02 15:59:42', 'Customer', 3),
('NguoiKham 2', 'nguoikham2', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0922222222', 1, '2024-12-02 15:59:42', 'Customer', 4),
('NguoiKham 3', 'nguoikham3', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0933333333', 1, '2024-12-02 15:59:42', 'Customer', 5),
('NguoiKham 4', 'nguoikham4', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0944444444', 1, '2024-12-02 15:59:42', 'Customer', 6),
('NguoiKham 5', 'nguoikham5', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0955555555', 1, '2024-12-02 15:59:42', 'Customer', 7),
('NguoiKham 6', 'nguoikham6', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0966666666', 1, '2024-12-02 15:59:42', 'Customer', 8),
('NguoiKham 7', 'nguoikham7', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0977777777', 1, '2024-12-02 15:59:42', 'Customer', 9),
('NguoiKham 8', 'nguoikham8', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0988888888', 1, '2024-12-02 15:59:42', 'Customer', 10),
('NguoiKham 9', 'nguoikham9', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Female', '2024-12-02', NULL, '0999999999', 1, '2024-12-02 15:59:42', 'Customer', 11),
('Đỗ Xuân Trọng', 'esmart211203@gmail.com', '63fcd343bad2ac8fab4de3415b29d15c', '', 'Male', '2024-12-02', 'esmart2111203@gmail.com', '0989748659', 1, '2024-12-02 16:03:12', 'Nurse', 14),
('John Doe', 'johndoe', '696d29e0940a4957748fe3fc9efd22a3', NULL, 'Male', '1990-01-01', 'john.doe@example.com', '0123456789', 1, '2024-12-02 16:09:48', 'Customer', 15),
('Jane Smith', 'janesmith', '696d29e0940a4957748fe3fc9efd22a3', NULL, 'Female', '1992-02-02', 'jane.smith@example.com', '0987654321', 1, '2024-12-02 16:09:48', 'Doctor', 16),
('Cô y tá', 'coyta', '63fcd343bad2ac8fab4de3415b29d15c', '', 'Male', '2003-02-11', 'coyta@gmail.com', '0989748658', 1, '2024-12-03 20:05:09', 'Nurse', 17),
('Đỗ Xuân Trọng', 'emtrongne', '63fcd343bad2ac8fab4de3415b29d15c', '', 'Male', '2024-12-25', 'haha@gmail.com', '0989748659', 1, '2024-12-05 01:42:14', 'Admin', 18),
('đăng ký thử', 'hahaha', '101a6ec9f938885df0a44f20458d2eb4', '', 'Male', '2024-12-27', 'hahahaha@gmail.com', '0989748669', 1, '2024-12-07 17:23:21', 'Customer', 19),
('Đỗ Xuân Trọng', 'admin1', '63fcd343bad2ac8fab4de3415b29d15c', '', 'Male', '2024-12-11', 'admin1@yomail.com', '0989748759', 1, '2024-12-11 17:08:39', 'Nurse', 20),
('Hà Sỹ Khôi', 'duydoc1', 'df9059fadd09b1a978945acd6ae9a8cd', '', 'Male', '2024-12-13', 'mduy2k3@gmail.com', '0123456789', 1, '2024-12-13 07:53:27', 'Admin', 21),
('Duy nurse 1', 'duynu1', '61051a26c12b172c76a1e30881e2d93d', '', 'Male', '0000-00-00', 'mduy2k3@gmail.com', '0000000000', 1, '2024-12-13 07:53:27', 'Nurse', 22),
('Duy Doctor 1', 'duydoc2', 'c00835d6da909fb9622cd87600a630cd', '', 'Female', '2023-05-23', 'mduy2k3@gmail.com', '0000000000', 1, '2024-12-23 01:10:19', 'Nurse', 23),
('Duy Doctor 1', '0000000000', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2023-07-06', 'michealduy2003@gmail.com', '0000000000', 1, '2024-12-23 01:10:19', 'Customer', 24),
('Duy Doctor 1', '0962517550', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2024-12-04', 'michealduy2003@gmail.com', '0962517550', 1, '2024-12-23 01:40:30', 'Customer', 25),
('Duy Doctor 1', '0123456789', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2024-12-18', 'michealduy2003@gmail.com', '0123456789', 1, '2024-12-23 09:12:30', 'Customer', 26),
('Duy nurse 1', '0898443499', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2024-12-17', 'michealduy2003@gmail.com', '0898443499', 1, '2024-12-23 09:12:30', 'Customer', 27),
('Duy nurse 00', '0898443498', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2024-12-12', 'michealduy2003@gmail.com', '0898443498', 1, '2024-12-23 09:12:30', 'Customer', 31),
('Nguyễn Văn A', '0898443491', 'e10adc3949ba59abbe56e057f20f883e', NULL, 'Male', '2024-12-10', 'mrbianlam@gmail.com', '0898443491', 1, '2024-12-24 10:22:55', 'Customer', 33);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `examination_bill`
--
ALTER TABLE `examination_bill`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `medical_bill_id` (`medical_bill_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `medical_bill`
--
ALTER TABLE `medical_bill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `medical_bill_detail`
--
ALTER TABLE `medical_bill_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `medical_bill_id` (`medical_bill_id`),
  ADD KEY `medicine_id` (`medicine_id`);

--
-- Indexes for table `medicine`
--
ALTER TABLE `medicine`
  ADD PRIMARY KEY (`id`),
  ADD KEY `unit_id` (`unit_id`);

--
-- Indexes for table `medicine_tag`
--
ALTER TABLE `medicine_tag`
  ADD PRIMARY KEY (`id`),
  ADD KEY `medicine_id` (`medicine_id`),
  ADD KEY `tag_id` (`tag_id`);

--
-- Indexes for table `registration_form`
--
ALTER TABLE `registration_form`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `regulation`
--
ALTER TABLE `regulation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `examination_bill`
--
ALTER TABLE `examination_bill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `medical_bill`
--
ALTER TABLE `medical_bill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `medical_bill_detail`
--
ALTER TABLE `medical_bill_detail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `medicine`
--
ALTER TABLE `medicine`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `medicine_tag`
--
ALTER TABLE `medicine_tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_form`
--
ALTER TABLE `registration_form`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `regulation`
--
ALTER TABLE `regulation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `unit`
--
ALTER TABLE `unit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `examination_bill`
--
ALTER TABLE `examination_bill`
  ADD CONSTRAINT `examination_bill_ibfk_1` FOREIGN KEY (`medical_bill_id`) REFERENCES `medical_bill` (`id`),
  ADD CONSTRAINT `examination_bill_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `medical_bill`
--
ALTER TABLE `medical_bill`
  ADD CONSTRAINT `medical_bill_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `medical_bill_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `medical_bill_detail`
--
ALTER TABLE `medical_bill_detail`
  ADD CONSTRAINT `medical_bill_detail_ibfk_1` FOREIGN KEY (`medical_bill_id`) REFERENCES `medical_bill` (`id`),
  ADD CONSTRAINT `medical_bill_detail_ibfk_2` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`);

--
-- Constraints for table `medicine`
--
ALTER TABLE `medicine`
  ADD CONSTRAINT `medicine_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`id`);

--
-- Constraints for table `medicine_tag`
--
ALTER TABLE `medicine_tag`
  ADD CONSTRAINT `medicine_tag_ibfk_1` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`),
  ADD CONSTRAINT `medicine_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

--
-- Constraints for table `registration_form`
--
ALTER TABLE `registration_form`
  ADD CONSTRAINT `registration_form_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `regulation`
--
ALTER TABLE `regulation`
  ADD CONSTRAINT `regulation_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
