#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from script import HalsteadParser

# Простой тест только с =>
test_code = """<?php
$arr = ['a' => 1, 'b' => 2];
?>"""

def main():
    parser = HalsteadParser()
    parser.parse_code(test_code)
    
    print("=== ПРОСТОЙ ТЕСТ => ===")
    print("Код:", test_code.strip())
    print()
    
    # Показываем операторы
    print("ОПЕРАТОРЫ:")
    for operator, count in sorted(parser.operators_dict.items()):
        if '=' in operator or '>' in operator:
            print(f"'{operator}': {count} раз")
    
    print()
    print("ОЖИДАЕМО:")
    print("'=>': 2 раза (в массиве)")
    print("'=': 1 раз (присваивание $arr)")
    print("'>': 0 раз (все > должны быть частью =>)")

if __name__ == "__main__":
    main()
