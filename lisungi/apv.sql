-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 15 août 2026 à 12:58
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `apv`
--

-- --------------------------------------------------------

--
-- Structure de la table `beneficiaries`
--

CREATE TABLE `beneficiaries` (
  `id` bigint(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `borough` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `date_existence` date NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `public_id` binary(16) NOT NULL,
  `type` enum('ASSOCIATION','AUTRE','ECOLE','EGLISE','ONG','ORPHELINAT','PARTICULIER') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `beneficiaries`
--

INSERT INTO `beneficiaries` (`id`, `address`, `borough`, `city`, `country`, `date_existence`, `email`, `name`, `phone`, `public_id`, `type`) VALUES
(1, '25 Rue de Vaugirard', '15e arrondissement', 'Paris', 'France', '2018-05-15', 'contact@solidariteplus.fr', 'Association Solidarité Plus', '+33145678901', 0xfa72908e0441463f9a499679c551605d, 'ASSOCIATION'),
(2, '25 Rue de Vaugirard', '15e arrondissement', 'Paris', 'France', '2018-05-15', 'contact@solidariteplus.fr', 'Agneaux de Dieu', '+33145678901', 0x069a1241f98d4f32928abdda6a6b0b08, 'ORPHELINAT');

-- --------------------------------------------------------

--
-- Structure de la table `contacts`
--

CREATE TABLE `contacts` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `message` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `contacts`
--

INSERT INTO `contacts` (`id`, `public_id`, `created_at`, `email`, `first_name`, `last_name`, `message`, `phone`, `status`) VALUES
(1, 0xbe1262b2ddd44b07bc214a0e7241cf4c, '2026-07-24 03:05:33.000000', 'brunelebata2@gmail.com', 'Paunel', 'ITOUA', 'Bonjour', '0755873258', 2),
(2, 0xb222e9f2fb1e44fb98f95d86753a113c, '2026-07-30 01:42:24.000000', 'brunelebata2@gmail.com', 'Brunel', 'EBATA-ATIPO', 'Je veux me renseigner sur les critère de l\'intégration de l\'association.', '0755873258', 2),
(3, 0x8e8af2941bf2410aa9692417aa80263e, '2026-08-06 03:59:14.000000', 'brunelebata4@gmail.com', 'Brunel', 'ATIPO', 'No commet', '0787543214', 2);

-- --------------------------------------------------------

--
-- Structure de la table `contributions`
--

CREATE TABLE `contributions` (
  `id` bigint(20) NOT NULL,
  `amount` decimal(38,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `status` bit(1) NOT NULL,
  `contributed_id` bigint(20) NOT NULL,
  `event_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `contributions`
--

INSERT INTO `contributions` (`id`, `amount`, `created_at`, `public_id`, `status`, `contributed_id`, `event_id`, `user_id`) VALUES
(1, '20000.11', '2026-07-24 02:48:12.000000', 0x9f106321c48546ea8c4f01715b308de6, b'0', 3, 2, 1),
(4, '145000.00', '2026-08-02 21:31:11.000000', 0x87654a160bf24b728ae07c6831615e3c, b'1', 1, 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `donations`
--

CREATE TABLE `donations` (
  `id` bigint(20) NOT NULL,
  `closure_status` bit(1) NOT NULL,
  `date_donation` date NOT NULL,
  `description` text NOT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `public_id` binary(16) NOT NULL,
  `public_status` bit(1) NOT NULL,
  `title` varchar(300) NOT NULL,
  `beneficiary_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `donations`
--

INSERT INTO `donations` (`id`, `closure_status`, `date_donation`, `description`, `photo`, `public_id`, `public_status`, `title`, `beneficiary_id`) VALUES
(1, b'1', '2026-08-30', 'No comment for the moment, i will give more informations tomorow', '27cf8c9f-073b-4df8-8d5e-3de854364204.jpg', 0x4a579dd080c94a979b8211a7e381d8a1, b'1', 'Don des ordinateurs', 1),
(2, b'0', '2026-08-01', 'Je ne comprends pas', '7e0ab30a-f77e-4337-8600-3efc9be3f1c7.jpg', 0x6b8ceffcbdb543c89fd1fd567f39d4f6, b'1', 'Je sais ', 2),
(3, b'1', '2026-08-04', 'ttttttttt', NULL, 0x5ca2caf4e4f3427a9ce8dd97597b9f1b, b'0', '	Je sais', 2),
(4, b'0', '2026-08-04', 'ppppppppppppprff', 'f6f67c79-d021-415d-96be-0d27c3ef63aa.jpg', 0x1cd4e3e3f8f047c8b8b680ffb2121e4d, b'1', '  Je sais', 1);

-- --------------------------------------------------------

--
-- Structure de la table `donation_participants`
--

CREATE TABLE `donation_participants` (
  `id` bigint(20) NOT NULL,
  `amount` decimal(38,2) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `item_type` enum('ASSOCIATION','AUTRE','ENTREPRISE','FOUNDATION','GOUVERNEMENT','PARTICULIER') NOT NULL,
  `name` varchar(200) NOT NULL,
  `participation_date` datetime(6) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `donation_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `donation_participants`
--

INSERT INTO `donation_participants` (`id`, `amount`, `description`, `item_type`, `name`, `participation_date`, `public_id`, `donation_id`, `user_id`) VALUES
(1, NULL, 'Livraison de 346000', 'PARTICULIER', 'ITOUA Paunel', '2026-08-01 15:29:48.000000', 0x6fd56a8b2e0f4c749d403648328c8381, 1, 1),
(2, NULL, 'Livraison de 6000', 'ENTREPRISE', 'Argil', '2026-08-02 20:54:08.000000', 0x6ea89c0d5d104c9da7548ea4874e04f1, 1, 1),
(3, '45000.00', '', 'PARTICULIER', 'ONDELE Bénie', '2026-08-04 21:58:09.000000', 0x8e70539064e6480083734adbb9503c12, 1, 1),
(4, NULL, '', 'PARTICULIER', 'NGAKALA Roy', '2026-08-04 22:23:47.000000', 0x1905e61f48314eb6889df7bf2cc91658, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `events`
--

CREATE TABLE `events` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `name` varchar(200) NOT NULL,
  `closure_status` bit(1) NOT NULL,
  `comment` text DEFAULT NULL,
  `event_date` date NOT NULL,
  `mount` decimal(38,2) NOT NULL,
  `event_type_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `amount_total` decimal(38,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `events`
--

INSERT INTO `events` (`id`, `public_id`, `name`, `closure_status`, `comment`, `event_date`, `mount`, `event_type_id`, `user_id`, `amount_total`) VALUES
(2, 0x7cb3de9a04c24679abe531e57849ee60, 'Mariage Réligieuse', b'0', 'Paiement du client', '2026-07-24', '25000.50', 1, 1, '165000.11'),
(3, 0xd7afcaf2e8f746099e205748cbbc3138, 'Décès de l\'oncle de Le Prince', b'0', 'No comment', '2026-07-25', '500000.00', 1, 3, NULL),
(6, 0x28d9df774fe14ab29751ceec774a4d17, 'Vente en ligne', b'0', '', '2026-08-04', '700000.00', 6, 3, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `event_type`
--

CREATE TABLE `event_type` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `public_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `event_type`
--

INSERT INTO `event_type` (`id`, `name`, `public_id`) VALUES
(1, 'Maladie', 0xf108d9cd7355411f80bb28789b4aadbb),
(2, 'Mariage', 0x6015653d470a44adaff3a93b08584efb),
(5, 'Décès', 0x1c13f11939644bd9b999786d8e0e2c27),
(6, 'Projet', 0x8f5dfc3e4d874a519c3a377465952087),
(7, 'Naissance', 0x87bd10134cf144748a2751bf17caea80),
(8, 'Anniversaire', 0x61265efade5447fa8a713341ea35d2f6);

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

CREATE TABLE `messages` (
  `id` bigint(20) NOT NULL,
  `content` text NOT NULL,
  `public_id` binary(16) NOT NULL,
  `sent_at` datetime(6) NOT NULL,
  `status` enum('DELIVERED','READ','SENT') NOT NULL,
  `receiver_id` bigint(20) DEFAULT NULL,
  `sender_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `messages`
--

INSERT INTO `messages` (`id`, `content`, `public_id`, `sent_at`, `status`, `receiver_id`, `sender_id`) VALUES
(1, 'Okay', 0x00000000000000000000000000000000, '2026-07-12 00:54:35.000000', 'READ', 3, 1),
(6, 'Bonjour', 0xcee5088e95fa4324bb7a3f1f17552b9c, '2026-08-06 21:05:21.000000', 'READ', 3, 1),
(9, 'Je ne veux rien savoir de ton histoire', 0x6718732164254578b49801e1ff0876c6, '2026-08-06 23:26:47.000000', 'READ', 6, 1),
(10, 'Actuellement tu parcours deux fois la liste (filter pour SUPADMIN puis ADMIN). Si tu as beaucoup d\'utilisateurs, tu peux faire un seul passage :', 0xdda456d2d7674bd0aa45f9ef84d20f20, '2026-08-06 23:36:56.000000', 'READ', 6, 1),
(11, 'Bonjour.', 0xccb97eeb4ff5462bb008052be591eb3a, '2026-08-07 02:09:35.000000', 'READ', 1, 6),
(12, 'J\'espère que tu vas bien ?', 0x78fa8bc4e80149219419ce43933a01c5, '2026-08-07 02:09:54.000000', 'READ', 1, 6);

-- --------------------------------------------------------

--
-- Structure de la table `news`
--

CREATE TABLE `news` (
  `id` bigint(20) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `public_id` binary(16) NOT NULL,
  `status` bit(1) NOT NULL,
  `title` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `news`
--

INSERT INTO `news` (`id`, `content`, `created_at`, `photo`, `public_id`, `status`, `title`) VALUES
(1, 'Saisissez le texte intégral à lire dans la zone de texte principale. Vous pouvez également saisir l\'adresse d\'une page Web dont vous souhaitez lire le texte. Appuyez ensuite sur le bouton Lire pour commencer la lecture ; le bouton Pauser interrompt la lecture pour la poursuivre lorsque le bouton Lire est à nouveau enfoncé. Annuler arrête la lecture, laissant l\'application prête à redémarrer. Dégager supprime le texte saisi, laissant la zone prête pour une nouvelle saisie. Le menu déroulant vous permet de sélectionner la langue de la voix avec laquelle la lecture est effectuée et dans certains cas le pays d\'origine. Ces voix sont naturelles, certaines masculines et d\'autres féminines.', NULL, '3de28da3-7145-48cb-b6c5-ed5798380dd9.jpg', 0x284adda24e92484aa4d56e77d1e83f56, b'0', 'Mariage de MB GOLA'),
(2, 'Les collectivités territoriales jouent un rôle essentiel dans le dynamisme associatif de nos territoires. C’est pourquoi nous avons tissé des partenariats solides avec elles, afin de faciliter l’accès aux ressources et aux solutions numériques pour les associations locales. Ensemble, nous travaillons à promouvoir des initiatives qui renforcent le tissu social, soutiennent les projets de solidarité et encouragent l\'engagement citoyen.', '2026-08-02 23:36:06.000000', '4c287729-3aa6-459e-9a0a-69ee11f45579.jpg', 0x0739bfebb1fc4bd1b2d58ac33d631a84, b'0', 'Première Dot de Paunel'),
(5, 'Saisissez le texte intégral à lire dans la zone de texte principale. Vous pouvez également saisir l\'adresse d\'une page Web dont vous souhaitez lire le texte. Appuyez ensuite sur le bouton Lire pour commencer la lecture ; le bouton Pauser interrompt la lecture pour la poursuivre lorsque le bouton Lire est à nouveau enfoncé. Annuler arrête la lecture, laissant l\'application prête à redémarrer. Dégager supprime le texte saisi, laissant la zone prête pour une nouvelle saisie. Le menu déroulant vous permet de sélectionner la langue de la voix avec laquelle la lecture est effectuée et dans certains cas le pays d\'origine. Ces voix sont naturelles, certaines masculines et d\'autres féminines.', '2026-08-05 12:08:29.000000', NULL, 0x929321a02ea140f8bd111b663d0153fe, b'0', 'Naissance de l\'enfant de MB');

-- --------------------------------------------------------

--
-- Structure de la table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `id` bigint(20) NOT NULL,
  `expiration_date` datetime(6) DEFAULT NULL,
  `token` varchar(255) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`id`, `expiration_date`, `token`, `user_id`) VALUES
(1, '2026-07-29 14:00:55.000000', '0acf5db4-6da5-4188-8575-71e1de78704e', 1),
(15, '2026-08-08 03:55:17.000000', '772545b8-c91b-40c1-aae1-aa748bf4507f', 6);

-- --------------------------------------------------------

--
-- Structure de la table `regulations`
--

CREATE TABLE `regulations` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `description` text NOT NULL,
  `name` varchar(50) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `update_at` datetime(6) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `regulations`
--

INSERT INTO `regulations` (`id`, `created_at`, `description`, `name`, `public_id`, `update_at`, `user_id`) VALUES
(1, NULL, 'Saisissez le texte intégral à lire dans la zone de texte principale. Vous pouvez également saisir l\'adresse d\'une page Web dont vous souhaitez lire le texte. Appuyez ensuite sur le bouton Lire pour commencer la lecture ; le bouton Pauser interrompt la lecture pour la poursuivre lorsque le bouton Lire est à nouveau enfoncé. Annuler arrête la lecture, laissant l\'application prête à redémarrer. Dégager supprime le texte saisi, laissant la zone prête pour une nouvelle saisie. Le menu déroulant vous permet de sélectionner la langue de la voix avec laquelle la lecture est effectuée et dans certains cas le pays d\'origine. Ces voix sont naturelles, certaines masculines et d\'autres féminines.', 'Regle 1', 0xf19e9d48966045e89c8626caf518ab87, '2026-08-09 14:58:28.000000', 1),
(2, NULL, 'Saisissez le texte intégral à lire dans la zone de texte principale. Vous pouvez également saisir l\'adresse d\'une page Web dont vous souhaitez lire le texte. Appuyez ensuite sur le bouton Lire pour commencer la lecture ; le bouton Pauser interrompt la lecture pour la poursuivre lorsque le bouton Lire est à nouveau enfoncé. Annuler arrête la lecture, laissant l\'application prête à redémarrer. Dégager supprime le texte saisi, laissant la zone prête pour une nouvelle saisie. Le menu déroulant vous permet de sélectionner la langue de la voix avec laquelle la lecture est effectuée et dans certains cas le pays d\'origine. Ces voix sont naturelles, certaines masculines et d\'autres féminines.', 'Regle 2', 0x833164a243bd4deeac43d78f9d6f716c, '2026-07-28 15:09:26.000000', 1),
(3, '2026-08-03 02:16:59.000000', 'Saisissez le texte intégral à lire dans la zone de texte principale. Vous pouvez également saisir l\'adresse d\'une page Web dont vous souhaitez lire le texte. Appuyez ensuite sur le bouton Lire pour commencer la lecture ; le bouton Pauser interrompt la lecture pour la poursuivre lorsque le bouton Lire est à nouveau enfoncé. Annuler arrête la lecture, laissant l\'application prête à redémarrer. Dégager supprime le texte saisi, laissant la zone prête pour une nouvelle saisie. Le menu déroulant vous permet de sélectionner la langue de la voix avec laquelle la lecture est effectuée et dans certains cas le pays d\'origine. Ces voix sont naturelles, certaines masculines et d\'autres féminines.', 'Regle 3', 0xc42ba08e6c674bc6a2937f94f09360ba, '2026-08-03 02:16:59.000000', 1),
(4, '2026-08-09 14:49:09.000000', 'Saisissez le texte intégral à lire dans la zone de texte principale. Vous pouvez également saisir l\'adresse d\'une page Web dont vous souhaitez lire le texte. Appuyez ensuite sur le bouton Lire pour commencer la lecture ; le bouton Pauser interrompt la lecture pour la poursuivre lorsque le bouton Lire est à nouveau enfoncé. Annuler arrête la lecture, laissant l\'application prête à redémarrer. Dégager supprime le texte saisi, laissant la zone prête pour une nouvelle saisie. Le menu déroulant vous permet de sélectionner la langue de la voix avec laquelle la lecture est effectuée et dans certains cas le pays d\'origine. Ces voix sont naturelles, certaines masculines et d\'autres féminines.', 'Regle 4', 0x8c2ab078b9b543b7b8e03db94a0ce9a2, '2026-08-09 14:49:09.000000', 1);

-- --------------------------------------------------------

--
-- Structure de la table `role`
--

CREATE TABLE `role` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `role`
--

INSERT INTO `role` (`id`, `public_id`, `name`) VALUES
(1, 0xaf47a3ff5af8452eb8d9314cfe23db79, 'ROLE_ADMIN'),
(2, 0x1a9971a6f2114644a26d3c6fd716c10f, 'ROLE_SUPADMIN'),
(3, 0x3ed63ae4091042f8a01eefa23f3eaf41, 'ROLE_CUSTOMER');

-- --------------------------------------------------------

--
-- Structure de la table `settings`
--

CREATE TABLE `settings` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `address` varchar(255) NOT NULL,
  `currency` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `height` int(11) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `name_app` varchar(255) NOT NULL,
  `name_dev` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `text_color` varchar(255) NOT NULL,
  `theme` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  `width` int(11) NOT NULL,
  `body_theme` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `settings`
--

INSERT INTO `settings` (`id`, `public_id`, `address`, `currency`, `email`, `height`, `logo`, `name_app`, `name_dev`, `phone`, `text_color`, `theme`, `version`, `width`, `body_theme`) VALUES
(1, 0x8db1a695cc894930bdea5ee7a019abc0, '5 rue de Tours', '€', 'contact@ecommerce.com', 50, '9e66f9b4-e765-40a0-909d-269a043a51a4.png', 'APV', 'EBATA-ATIPO Brunel', '+33 0000000', 'text-white', 'bg-maroon', '1.0.0', 70, 'bg-maroon');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `enabled` bit(1) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `public_id`, `email`, `enabled`, `password`, `username`) VALUES
(1, 0xd001b268322f42d19a7593d619538958, 'admin@gmail.com', b'1', '$2a$10$IL8laXO0R7jIUDlOWCoS6OzSDFS6hzUeAPBsbWAaEFED18Ll7KlkW', 'admin'),
(3, 0x2142f1e4121743d6b9236e0442ad9458, 'espoirngalebo@gmail.com', b'1', '$2a$10$fU.9kb0opKtcyrip80vIV.e5RJJP9qP9C0LjSasXKlzAtwO0p1xrW', 'leprince'),
(6, 0x4ae875e7f93c46449ebf17c28dec103d, 'brunelebata2@gmail.com', b'1', '$2a$10$.l7Z8VGcpoUnO3gRrwcbCur6BLtWZCCzA8j0bfwKf2nNNhvc1qJSq', 'despiero');

-- --------------------------------------------------------

--
-- Structure de la table `user_profile`
--

CREATE TABLE `user_profile` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `borough` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `gender` enum('FEMININ','MASCULIN') DEFAULT NULL,
  `profession` varchar(255) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `reason_removal` enum('JE_SUIS_INTERESSE','JE_NE_SUIS_PLUS_INTERESSE','JE_NE_SUIS_PLUS_DISPONIBLE','JE_VAIS_PRENDRE_UNE_PAUSE','ORGANISATION_N_EST_PAS_BONNE','AUTRES') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user_profile`
--

INSERT INTO `user_profile` (`id`, `public_id`, `address`, `borough`, `city`, `country`, `first_name`, `last_name`, `phone`, `photo`, `user_id`, `gender`, `profession`, `registration_date`, `reason_removal`) VALUES
(2, 0x8e4b2e89de194c448273144b9ab772da, '5  rue de Tours', 'La source', 'Orléans', 'France', 'Le Prince Espoir', 'NGALEBO', '0755873258', '40f41258-b323-45fe-9d8b-8db25fc2bb79.jpg', 3, 'FEMININ', NULL, '2026-08-07', 'JE_SUIS_INTERESSE'),
(3, 0x00000000000000000000000000000000, '3 rue de Vendôme', 'La source', 'Orléans', 'France', 'Rodrigue', 'MPIKA', '0967436345', 'b7e4f973-a350-49a5-b74c-6abb5fcab0d7.jpg', 1, 'MASCULIN', 'Data Analyst', '2026-08-07', 'JE_SUIS_INTERESSE'),
(6, 0x9dcd9e43caba4385ad52da7f1ea6582b, 'Bâtiment les Hêtres, Chambre 159', 'Talangaî', 'Orléans', NULL, 'Brunel', 'EBATA-ATIPO', '0755873258', '1c4b1e5e-f43f-4f5e-98dd-d4a58ae65739.jpg', 6, 'MASCULIN', NULL, '2026-08-07', 'JE_SUIS_INTERESSE');

-- --------------------------------------------------------

--
-- Structure de la table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_id` bigint(20) NOT NULL,
  `role_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user_roles`
--

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(6, 3);

-- --------------------------------------------------------

--
-- Structure de la table `views`
--

CREATE TABLE `views` (
  `id` bigint(20) NOT NULL,
  `public_id` binary(16) NOT NULL,
  `status` bit(1) NOT NULL,
  `admin_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `views`
--

INSERT INTO `views` (`id`, `public_id`, `status`, `admin_id`, `user_id`) VALUES
(1, 0x8eedca502ce64c049ddf39f5b84f6393, b'1', 6, 1),
(2, 0xdd69bf3ccc164fd399ff04598f4025f9, b'1', 6, 3),
(3, 0x4a6f4a96f0fd4920aacaacbb0d13ae63, b'1', 1, 3),
(4, 0x7c9df46833744893a61120ee625dab08, b'1', 1, 6);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `beneficiaries`
--
ALTER TABLE `beneficiaries`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK8n5dnwuoil3sj7p7aw6e8inre` (`public_id`);

--
-- Index pour la table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK3ogbwdrc62p70kj621agqmqat` (`public_id`);

--
-- Index pour la table `contributions`
--
ALTER TABLE `contributions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKivqc6jeqf0n0v9dhi0ug2rer8` (`public_id`),
  ADD KEY `FK8cfo7mx8ykbuwlx8ir34jmubb` (`contributed_id`),
  ADD KEY `FK6k4j1jvoupan0ugd1jggxhl99` (`event_id`),
  ADD KEY `FK4qcv0c1wgs0m7vwo4pwyvel3i` (`user_id`);

--
-- Index pour la table `donations`
--
ALTER TABLE `donations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK9ymec5n8lnprjl6y10tw4vavp` (`public_id`),
  ADD UNIQUE KEY `UKn7vobv69rab59ms1vowx8wuoj` (`title`),
  ADD UNIQUE KEY `UK8l1gwftc94nekn7w3f9xt3pav` (`photo`),
  ADD KEY `FKpmwsb0wrjruv9fi5r49jjkay9` (`beneficiary_id`);

--
-- Index pour la table `donation_participants`
--
ALTER TABLE `donation_participants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK43w9xs88brtk21mmwdrc29mpl` (`name`),
  ADD UNIQUE KEY `UKsppokvldnw8p9m9p3aqn2pfw4` (`public_id`),
  ADD KEY `FKgohfw3oi6ghg94kfpy2svh9t5` (`donation_id`),
  ADD KEY `FKcokjlpg4b9ljjyu5bec6s96hy` (`user_id`);

--
-- Index pour la table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKi4birsrlskr9r453y42sf94o8` (`public_id`),
  ADD UNIQUE KEY `UKfn2r8jg0sm5v6vhoa7yqw55vy` (`name`),
  ADD UNIQUE KEY `UKhcw1pwhheab85j2obakvtyspy` (`comment`) USING HASH,
  ADD KEY `FK9lh2nikd9fqq3vtpclva4daal` (`event_type_id`),
  ADD KEY `FKat8p3s7yjcp57lny4udqvqncq` (`user_id`);

--
-- Index pour la table `event_type`
--
ALTER TABLE `event_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKdunk58vf3o8hxdjjspls1jrl` (`name`),
  ADD UNIQUE KEY `UK7244ywc8v7bdwi5hskc32a70h` (`public_id`);

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKhj7un9hohyyvirrtpd8qycy1q` (`public_id`),
  ADD KEY `FKt05r0b6n0iis8u7dfna4xdh73` (`receiver_id`),
  ADD KEY `FK4ui4nnwntodh6wjvck53dbk9m` (`sender_id`);

--
-- Index pour la table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKpkwwiketd5vlr6iu25ldhn1t1` (`public_id`),
  ADD UNIQUE KEY `UK9tfgiwqioj4gn86792hj5fgx3` (`title`),
  ADD UNIQUE KEY `UK3fbdcxfa40vncjbvfhv9arube` (`photo`);

--
-- Index pour la table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK71lqwbwtklmljk3qlsugr1mig` (`token`),
  ADD UNIQUE KEY `UKla2ts67g4oh2sreayswhox1i6` (`user_id`);

--
-- Index pour la table `regulations`
--
ALTER TABLE `regulations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKlx8eq2mbkxeld3j7l380b0uve` (`name`),
  ADD UNIQUE KEY `UKl6kpm64wm2fkk6am6n1bvuev4` (`public_id`),
  ADD KEY `FKk1frvq31845w164apqskeoe2m` (`user_id`);

--
-- Index pour la table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK4qh0ib7j5nbejq1vxmnlm02n3` (`public_id`),
  ADD UNIQUE KEY `UK8sewwnpamngi6b1dwaa88askk` (`name`);

--
-- Index pour la table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKrypn4ipawou3thelxrwjnq01w` (`public_id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKs24bux761rbgowsl7a4b386ba` (`public_id`);

--
-- Index pour la table `user_profile`
--
ALTER TABLE `user_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKrh8e2ahfkprk7ppo6o0vwxtse` (`public_id`),
  ADD UNIQUE KEY `UKebc21hy5j7scdvcjt0jy6xxrv` (`user_id`);

--
-- Index pour la table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `FKrhfovtciq1l558cw6udg0h0d3` (`role_id`);

--
-- Index pour la table `views`
--
ALTER TABLE `views`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKhw6oyfx6vl1yb1eptrhut92ae` (`public_id`),
  ADD KEY `FKcby66tnrtwtns0rmsio6ap122` (`admin_id`),
  ADD KEY `FKfpjhiw62pqb70q2j46jp3h4vk` (`user_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `beneficiaries`
--
ALTER TABLE `beneficiaries`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `contributions`
--
ALTER TABLE `contributions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `donations`
--
ALTER TABLE `donations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `donation_participants`
--
ALTER TABLE `donation_participants`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `events`
--
ALTER TABLE `events`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `event_type`
--
ALTER TABLE `event_type`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `news`
--
ALTER TABLE `news`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT pour la table `regulations`
--
ALTER TABLE `regulations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `role`
--
ALTER TABLE `role`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `settings`
--
ALTER TABLE `settings`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `user_profile`
--
ALTER TABLE `user_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `views`
--
ALTER TABLE `views`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `contributions`
--
ALTER TABLE `contributions`
  ADD CONSTRAINT `FK4qcv0c1wgs0m7vwo4pwyvel3i` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FK6k4j1jvoupan0ugd1jggxhl99` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`),
  ADD CONSTRAINT `FK8cfo7mx8ykbuwlx8ir34jmubb` FOREIGN KEY (`contributed_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `donations`
--
ALTER TABLE `donations`
  ADD CONSTRAINT `FKpmwsb0wrjruv9fi5r49jjkay9` FOREIGN KEY (`beneficiary_id`) REFERENCES `beneficiaries` (`id`);

--
-- Contraintes pour la table `donation_participants`
--
ALTER TABLE `donation_participants`
  ADD CONSTRAINT `FKcokjlpg4b9ljjyu5bec6s96hy` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FKgohfw3oi6ghg94kfpy2svh9t5` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`id`);

--
-- Contraintes pour la table `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `FK9lh2nikd9fqq3vtpclva4daal` FOREIGN KEY (`event_type_id`) REFERENCES `event_type` (`id`),
  ADD CONSTRAINT `FKat8p3s7yjcp57lny4udqvqncq` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `FK4ui4nnwntodh6wjvck53dbk9m` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FKt05r0b6n0iis8u7dfna4xdh73` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD CONSTRAINT `FKk3ndxg5xp6v7wd4gjyusp15gq` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `regulations`
--
ALTER TABLE `regulations`
  ADD CONSTRAINT `FKk1frvq31845w164apqskeoe2m` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `user_profile`
--
ALTER TABLE `user_profile`
  ADD CONSTRAINT `FKuganfwvnbll4kn2a3jeyxtyi` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `FKhfh9dx7w3ubf1co1vdev94g3f` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FKrhfovtciq1l558cw6udg0h0d3` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);

--
-- Contraintes pour la table `views`
--
ALTER TABLE `views`
  ADD CONSTRAINT `FKcby66tnrtwtns0rmsio6ap122` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FKfpjhiw62pqb70q2j46jp3h4vk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
