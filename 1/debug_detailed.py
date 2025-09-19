#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Тестовый код
test_code = """<?php
$array = ['name' => 'John', 'age' => 25];
$filtered = array_filter($array, fn($value) => $value !== 'John');
?>"""

def analyze_code():
    print("=== АНАЛИЗ КОДА ПО СИМВОЛАМ ===")
    
    # Показываем код с позициями
    print("Код с позициями:")
    for i, char in enumerate(test_code):
        if char in '=>!':
            print(f"Позиция {i:2d}: '{char}'")
    
    print("\n=== ПОИСК ПАТТЕРНОВ ===")
    
    # Ищем все вхождения =>
    print("Все вхождения '=>':")
    for match in re.finditer(r'=>', test_code):
        start, end = match.start(), match.end()
        context = test_code[max(0, start-10):end+10]
        print(f"  Позиция {start}-{end}: '{match.group()}' в контексте: '{context}'")
    
    # Ищем все вхождения !==
    print("\nВсе вхождения '!==':")
    for match in re.finditer(r'!==', test_code):
        start, end = match.start(), match.end()
        context = test_code[max(0, start-10):end+10]
        print(f"  Позиция {start}-{end}: '{match.group()}' в контексте: '{context}'")
    
    # Ищем все вхождения >
    print("\nВсе вхождения '>':")
    for match in re.finditer(r'>', test_code):
        start, end = match.start(), match.end()
        context = test_code[max(0, start-10):end+10]
        print(f"  Позиция {start}-{end}: '{match.group()}' в контексте: '{context}'")

if __name__ == "__main__":
    analyze_code()
