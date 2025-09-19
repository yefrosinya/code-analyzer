#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Тестовый код
test_code = """<?php
$array = ['name' => 'John', 'age' => 25];
$filtered = array_filter($array, fn($value) => $value !== 'John');
?>"""

def find_all_matches():
    print("=== ПОИСК ВСЕХ ВХОЖДЕНИЙ ===")
    
    # Ищем =>
    print("Оператор '=>':")
    for match in re.finditer(r'=>', test_code):
        print(f"  Позиция {match.start()}-{match.end()}: '{match.group()}' в контексте: '{test_code[max(0, match.start()-5):match.end()+5]}'")
    
    # Ищем !==
    print("\nОператор '!==':")
    for match in re.finditer(r'!==', test_code):
        print(f"  Позиция {match.start()}-{match.end()}: '{match.group()}' в контексте: '{test_code[max(0, match.start()-5):match.end()+5]}'")
    
    # Ищем отдельные >
    print("\nОтдельные символы '>':")
    for match in re.finditer(r'>', test_code):
        print(f"  Позиция {match.start()}-{match.end()}: '{match.group()}' в контексте: '{test_code[max(0, match.start()-5):match.end()+5]}'")
    
    # Ищем отдельные =
    print("\nОтдельные символы '=':")
    for match in re.finditer(r'=', test_code):
        print(f"  Позиция {match.start()}-{match.end()}: '{match.group()}' в контексте: '{test_code[max(0, match.start()-5):match.end()+5]}'")

if __name__ == "__main__":
    find_all_matches()
