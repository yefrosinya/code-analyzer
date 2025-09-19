#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from script import HalsteadParser

# Тестовый код с оператором =>
test_code = """<?php
$array = ['name' => 'John', 'age' => 25, 'city' => 'New York'];
$filtered = array_filter($array, fn($value) => $value !== 'John');
$mapped = array_map(fn($key, $value) => "$key: $value", array_keys($array), array_values($array));
?>"""

def main():
    parser = HalsteadParser()
    parser.parse_code(test_code)
    
    print("=== ТЕСТ ОПЕРАТОРА => ===")
    print()
    
    # Показываем операторы
    print("ОПЕРАТОРЫ:")
    for operator, count in parser.operators_dict.items():
        if '=>' in operator or '=' in operator or '>' in operator:
            print(f"'{operator}': {count} раз")
    
    print()
    print("=== ПРОВЕРКА ===")
    
    # Проверяем оператор =>
    arrow_equals = parser.operators_dict.get('=>', 0)
    single_equals = parser.operators_dict.get('=', 0)
    single_greater = parser.operators_dict.get('>', 0)
    
    print(f"Оператор '=>': {arrow_equals} раз")
    print(f"Отдельный символ '=': {single_equals} раз")
    print(f"Отдельный символ '>': {single_greater} раз")
    
    if arrow_equals > 0 and single_equals == 0 and single_greater == 0:
        print("✅ УСПЕХ: Оператор => обрабатывается правильно!")
    else:
        print("❌ ОШИБКА: Оператор => обрабатывается неправильно!")

if __name__ == "__main__":
    main()
