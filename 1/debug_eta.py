#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from script import HalsteadParser

# Простой тест для отладки eta1
test_code = """<?php
function test() {
    return $a + $b;
}
?>"""

def debug_eta():
    parser = HalsteadParser()
    
    print("=== ОТЛАДКА ETA1 ===")
    print("Код:", test_code.strip())
    print()
    
    # Сброс метрик
    parser._reset_metrics()
    print("После сброса:")
    print(f"  eta1: {parser.eta1}")
    print(f"  N1: {parser.N1}")
    print(f"  len(operators_dict): {len(parser.operators_dict)}")
    print(f"  sum(operators_dict.values()): {sum(parser.operators_dict.values())}")
    print()
    
    # Извлекаем операторы
    parser._extract_operators(test_code)
    
    print("После _extract_operators:")
    print(f"  eta1: {parser.eta1}")
    print(f"  N1: {parser.N1}")
    print(f"  len(operators_dict): {len(parser.operators_dict)}")
    print(f"  sum(operators_dict.values()): {sum(parser.operators_dict.values())}")
    print()
    
    print("Содержимое operators_dict:")
    for operator, count in sorted(parser.operators_dict.items()):
        print(f"  '{operator}': {count}")
    
    print()
    print("Проверка:")
    print(f"  eta1 == len(operators_dict): {parser.eta1 == len(parser.operators_dict)}")
    print(f"  N1 == sum(operators_dict.values()): {parser.N1 == sum(parser.operators_dict.values())}")

if __name__ == "__main__":
    debug_eta()
