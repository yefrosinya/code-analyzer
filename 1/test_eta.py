#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from script import HalsteadParser

# Простой тест для проверки eta1
test_code = """<?php
function test() {
    return $a + $b;
}
?>"""

def main():
    parser = HalsteadParser()
    parser.parse_code(test_code)
    
    print("=== ТЕСТ ETA1 ===")
    print("Код:", test_code.strip())
    print()
    
    print("ОПЕРАТОРЫ:")
    for operator, count in sorted(parser.operators_dict.items()):
        print(f"'{operator}': {count} раз")
    
    print()
    print(f"eta1 (уникальные операторы): {parser.eta1}")
    print(f"N1 (общее количество операторов): {parser.N1}")
    print(f"Количество уникальных в словаре: {len(parser.operators_dict)}")
    print(f"Сумма всех значений: {sum(parser.operators_dict.values())}")
    
    print()
    print("ОЖИДАЕМО:")
    print("- eta1 должно быть количеством уникальных операторов")
    print("- N1 должно быть общим количеством операторов")
    print("- Они должны совпадать с len(dict) и sum(dict.values())")

if __name__ == "__main__":
    main()
