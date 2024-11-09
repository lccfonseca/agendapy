CREATE DATABASE agenda;

USE agenda;

CREATE TABLE `agenda`.`contatos` (
 `id` INT NOT NULL,
 `nome` VARCHAR(80) NOT NULL,
 `email` VARCHAR(100) NULL,
 `telefone` VARCHAR(15) NULL,
PRIMARY KEY (`id`));

ALTER TABLE `agenda`.`contatos`
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT ,
ADD UNIQUE INDEX `id_UNIQUE` (`id` ASC);
