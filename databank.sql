-- Active: 1754614651844@@127.0.0.1@3306@projeto_integrador_fase2
CREATE TABLE expenses (id INT PRIMARY KEY AUTO_INCREMENT, expense_type VARCHAR(100), expense_date DATE, expense_value INT);
CREATE TABLE earnings (id INT PRIMARY KEY AUTO_INCREMENT, earning_type VARCHAR(100), earning_date DATE, earning_value INT);