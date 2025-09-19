#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Тестовый код
test_code = """<?php
$arr = ['a' => 1];
if ($x !== null) { }
?>"""

def test_if_pattern():
    print("=== ТЕСТ ПАТТЕРНА IF ===")
    print("Код:", test_code.strip())
    print()
    
    # Паттерн if-else
    if_else_pattern = r'if\s*\([^)]*\)\s*\{[^{}]*\}(?:\s*elseif\s*\([^)]*\)\s*\{[^{}]*\})*(?:\s*else\s*\{[^{}]*\})?'
    
    print("Поиск if-else конструкций:")
    for match in re.finditer(if_else_pattern, test_code, re.IGNORECASE):
        start, end = match.start(), match.end()
        matched_text = match.group()
        context = test_code[max(0, start-5):end+5]
        print(f"  Найдено: '{matched_text}' в позиции {start}-{end}")
        print(f"  Контекст: '{context}'")
        print(f"  Содержит вложенные блоки: {bool(re.search(r'\{[^{}]*\{', matched_text))}")
        print()

if __name__ == "__main__":
    test_if_pattern()
