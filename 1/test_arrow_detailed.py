#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from script import HalsteadParser

# Тестовый код с оператором =>
test_code = """<?php
$array = ['name' => 'John', 'age' => 25];
$filtered = array_filter($array, fn($value) => $value !== 'John');
?>"""

def main():
    parser = HalsteadParser()
    parser.parse_code(test_code)
    
    print("=== ДЕТАЛЬНЫЙ ТЕСТ ОПЕРАТОРА => ===")
    print()
    print("Исходный код:")
    print(test_code)
    print()
    
    # Показываем все операторы
    print("ВСЕ ОПЕРАТОРЫ:")
    for operator, count in sorted(parser.operators_dict.items()):
        print(f"'{operator}': {count} раз")
    
    print()
    print("=== АНАЛИЗ ===")
    
    # Анализируем конкретные случаи
    arrow_equals = parser.operators_dict.get('=>', 0)
    single_equals = parser.operators_dict.get('=', 0)
    single_greater = parser.operators_dict.get('>', 0)
    not_equals = parser.operators_dict.get('!==', 0)
    
    print(f"Оператор '=>': {arrow_equals} раз (должно быть 2)")
    print(f"Оператор '!==': {not_equals} раз (должно быть 1)")
    print(f"Отдельный символ '=': {single_equals} раз (должно быть 2: $array = и $filtered =)")
    print(f"Отдельный символ '>': {single_greater} раз (должно быть 0)")
    
    print()
    print("Ожидаемые результаты:")
    print("- '=>' должно быть 2 раза: в массиве и в fn")
    print("- '!==' должно быть 1 раз: в условии")
    print("- '=' должно быть 2 раза: присваивания переменным")
    print("- '>' должно быть 0 раз: все > должны быть частью => или !==")

if __name__ == "__main__":
    main()
