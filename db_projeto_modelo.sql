DROP SCHEMA IF EXISTS `db_projeto_modelo`;
CREATE SCHEMA `db_projeto_modelo` ;

-- Tabela Conta de Usuário
DROP TABLE IF EXISTS `db_projeto_modelo`.`conta_con`;
CREATE TABLE `db_projeto_modelo`.`conta_con` (
  `id_conta` INT(11) NOT NULL AUTO_INCREMENT,
  `ds_usuario_con` VARCHAR(45) NOT NULL,
  `ds_email_con` VARCHAR(120) NOT NULL,
  `ds_foto_con` VARCHAR(20) NOT NULL,
  `ds_senha_con` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`id_conta`));

-- Tabela Modelo
DROP TABLE IF EXISTS `db_projeto_modelo`.`modelo_mod`;
CREATE TABLE `db_projeto_modelo`.`modelo_mod` (
  `id_modelo` INT(11) NOT NULL AUTO_INCREMENT,
  `ds_sigla_mod` VARCHAR(45) NOT NULL,
  `ds_nome_mod` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_modelo`));

-- ONE-TO-MANY Relationship
-- Tabela Mestre
DROP TABLE IF EXISTS `db_projeto_modelo`.`detalhe_dtl`;
DROP TABLE IF EXISTS `db_projeto_modelo`.`mestre_mst`;
CREATE TABLE `mestre_mst` (
  `id_mst` int(11) NOT NULL AUTO_INCREMENT,
  `ds_nome_mst` varchar(100) NOT NULL,
  `ds_sexo_mst` varchar(1) NOT NULL,
  `ds_estadocivil_mst` varchar(1) NOT NULL,
  `dt_nascimento_mst` datetime NOT NULL,
  `lg_situacao_mst` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_mst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Tabela Detalhe
DROP TABLE IF EXISTS `db_projeto_modelo`.`detalhe_dtl`;
CREATE TABLE `detalhe_dtl` (
  `id_dtl` int(11) NOT NULL AUTO_INCREMENT,
  `ds_nome_dtl` varchar(60) NOT NULL,
  `ds_endereco_dtl` varchar(200) NOT NULL,
  `ds_bairro_dtl` varchar(30) NOT NULL,
  `ds_cidade_dtl` varchar(30) NOT NULL,
  `ds_telefone_dtl` varchar(15) NOT NULL,
  `mestre_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_dtl`),
  KEY `mestre_id` (`mestre_id`),
  CONSTRAINT `detalhe_dtl_ibfk_1` FOREIGN KEY (`mestre_id`) REFERENCES `mestre_mst` (`id_mst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- MANY-TO-MANY Relationship
-- Tabela Autor
DROP TABLE IF EXISTS `db_projeto_modelo`.`autor_aut`;
CREATE TABLE `db_projeto_modelo`.`autor_aut` (
  `id_aut` INT NOT NULL AUTO_INCREMENT,
  `ds_nome_aut` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`id_aut`));

-- Tabela Livro
DROP TABLE IF EXISTS `db_projeto_modelo`.`livro_liv`;
CREATE TABLE `db_projeto_modelo`.`livro_liv` (
  `id_liv` INT NOT NULL AUTO_INCREMENT,
  `ds_nome_liv` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`id_liv`));

-- Tabela Autor-Livro
DROP TABLE IF EXISTS `db_projeto_modelo`.`autor_livro_lvt`;
CREATE TABLE `db_projeto_modelo`.`autor_livro_lvt` (
  `id_lvt` INT NOT NULL AUTO_INCREMENT,
  `id_aut` INT NOT NULL,
  `id_liv` INT NOT NULL,
  `dt_publicacao_lvt` DATETIME NOT NULL,
  PRIMARY KEY (`id_lvt`),
  FOREIGN KEY (`id_aut`) REFERENCES `db_projeto_modelo`.`autor_aut` (`id_aut`),
  FOREIGN KEY (`id_liv`) REFERENCES `db_projeto_modelo`.`livro_liv` (`id_liv`));



-- CREATE TABLE `person` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `name` varchar(20) DEFAULT NULL,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- CREATE TABLE `pet` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `name` varchar(20) DEFAULT NULL,
--   `owner_id` int(11) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   KEY `owner_id` (`owner_id`),
--   CONSTRAINT `pet_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `person` (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

