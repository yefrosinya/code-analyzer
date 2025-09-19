#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Тестовый код
test_code = """<?php
$arr = ['a' => 1];
if ($x !== null) { }
?>"""

def test_regex():
    print("=== ТЕСТ РЕГУЛЯРНЫХ ВЫРАЖЕНИЙ ===")
    print("Код:", test_code.strip())
    print()
    
    # Тестируем !==
    pattern = r'!=='
    matches = list(re.finditer(pattern, test_code))
    print(f"Паттерн '{pattern}':")
    for match in matches:
        start, end = match.start(), match.end()
        context = test_code[max(0, start-5):end+5]
        print(f"  Найдено: '{match.group()}' в позиции {start}-{end}, контекст: '{context}'")
    
    if not matches:
        print("  НЕ НАЙДЕНО!")
    
    print()
    
    # Тестируем =>
    pattern = r'=>'
    matches = list(re.finditer(pattern, test_code))
    print(f"Паттерн '{pattern}':")
    for match in matches:
        start, end = match.start(), match.end()
        context = test_code[max(0, start-5):end+5]
        print(f"  Найдено: '{match.group()}' в позиции {start}-{end}, контекст: '{context}'")
    
    print()
    
    # Тестируем все символы
    print("Все символы '!', '=', '>':")
    for i, char in enumerate(test_code):
        if char in '!=>':
            context = test_code[max(0, i-3):i+4]
            print(f"  Позиция {i}: '{char}' в контексте: '{context}'")

if __name__ == "__main__":
    test_regex()
