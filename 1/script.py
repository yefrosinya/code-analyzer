import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
import math
import re
import os


class HalsteadParser:
    def __init__(self):
        self.operators_dict = {}
        self.operands_dict = {}

        self.eta1 = 0
        self.eta2 = 0
        self.N1 = 0
        self.N2 = 0

        self.eta = 0  # словарь программы
        self.N = 0  # длина
        self.V = 0

    def parse_code(self, code):
        self._reset_metrics()
        self._extract_operators(code)
        self._extract_operands(code)
        self._calculate_metrics()

    def _reset_metrics(self):
        self.operators_dict = {}
        self.operands_dict = {}
        self.eta1 = 0
        self.eta2 = 0
        self.N1 = 0
        self.N2 = 0
        self.eta = 0
        self.N = 0
        self.V = 0

    def _extract_operators(self, code):
        code = self._remove_comments(code)
        code_no_strings = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '', code)

        php_operators = [
            '+', '-', '*', '/', '%', '**', '++', '--',
            '=', '+=', '-=', '*=', '/=', '%=', '.=',
            '==', '===', '!=', '!==', '<>', '>', '<', '>=', '<=', '<=>', '=>',
            '&&', 'and', '||', 'or', 'xor', '!',
            '&', '|', '^', '~', '<<', '>>',
            '.', '->', '::',
            '?', ':', '??',
            '@',
            '(', ')', '[', ']', '{', '}',
            ',', ';',
            'if', 'else', 'elseif', 'switch', 'case', 'default',
            'while', 'do', 'for', 'foreach', 'break', 'continue',
            'function', 'return', 'class', 'interface', 'trait',
            'try', 'catch', 'finally', 'throw',
            'echo', 'print', 'isset', 'empty', 'unset', 'private', 'public',
            '__construct', '__distruct', 'fn', 'new', 'implode', 'unset', 'isset',
            'count', 'execute', 'str_repeat', 'strlen', 'array_intersect_key', 'array_flip', 'array_map',
            'array_keys', 'array_values', 'array_merge', 'array_filter',
            'fetch_assoc', 'getUserById', 'getMessage', 'getUsersByRole', 'addUser'
        ]

        # Сначала обрабатываем составные операторы
        self._extract_composite_operators(code_no_strings)
        
        # Затем простые операторы (исключаем составные)
        operator_patterns = [
            r'\+\+', r'--', r'\*\*', r'\+=', r'-=', r'\*=', r'/=', r'%=', r'\.=',
            r'===', r'!==', r'<=>', r'&&', r'\|\|', r'<<', r'>>', r'->', r'::', r'\?\?',
            r'<=', r'>=', r'==', r'!=', r'<>',
            r'while\s*\(', r'do\b',
            r'for\s*\(', r'foreach\s*\(', r'break\b', r'continue\b',
            r'function\b', r'return\b', r'class\b', r'interface\b', r'trait\b',
            r'throw\b',
            r'echo\b', r'print\b', r'isset\s*\(', r'empty\s*\(', r'unset\s*\(',
            r'\+', r'-', r'\*', r'/', r'%', r'=', r'<', r'>',
            r'&', r'\|', r'\^', r'~', r'!', r'\.', r'\?', r':', r'@',
            r'\(', r'\)', r'\[', r'\]', r'\{', r'\}', r',', r';'
        ]

        for pattern in operator_patterns:
            matches = re.findall(pattern, code_no_strings, re.IGNORECASE)
            for match in matches:
                operator = match.lower() if match.strip().isalpha() else match
                self.operators_dict[operator] = self.operators_dict.get(operator, 0) + 1

        # Считаем только закрытые пары скобок как один оператор
        # Одиночные скобки считаем отдельно
        open_parens = code_no_strings.count('(')
        close_parens = code_no_strings.count(')')
        open_braces = code_no_strings.count('{')
        close_braces = code_no_strings.count('}')
        open_brackets = code_no_strings.count('[')
        close_brackets = code_no_strings.count(']')
        
        # Закрытые пары
        pairs = min(open_parens, close_parens)
        if pairs > 0:
            self.operators_dict['()'] = self.operators_dict.get('()', 0) + pairs
        
        pairs = min(open_braces, close_braces)
        if pairs > 0:
            self.operators_dict['{}'] = self.operators_dict.get('{}', 0) + pairs
            
        pairs = min(open_brackets, close_brackets)
        if pairs > 0:
            self.operators_dict['[]'] = self.operators_dict.get('[]', 0) + pairs
        
        # Одиночные скобки (не закрытые)
        if open_parens > close_parens:
            self.operators_dict['('] = self.operators_dict.get('(', 0) + (open_parens - close_parens)
        if close_parens > open_parens:
            self.operators_dict[')'] = self.operators_dict.get(')', 0) + (close_parens - open_parens)
            
        if open_braces > close_braces:
            self.operators_dict['{'] = self.operators_dict.get('{', 0) + (open_braces - close_braces)
        if close_braces > open_braces:
            self.operators_dict['}'] = self.operators_dict.get('}', 0) + (close_braces - open_braces)
            
        if open_brackets > close_brackets:
            self.operators_dict['['] = self.operators_dict.get('[', 0) + (open_brackets - close_brackets)
        if close_brackets > open_brackets:
            self.operators_dict[']'] = self.operators_dict.get(']', 0) + (close_brackets - open_brackets)

        self.eta1 = len(self.operators_dict)
        self.N1 = sum(self.operators_dict.values())

    def _extract_composite_operators(self, code):
        """Извлекает составные операторы как единые конструкции"""
        # if-elseif-else конструкции
        if_else_pattern = r'if\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}(?:\s*elseif\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})*(?:\s*else\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})?'
        if_else_matches = re.findall(if_else_pattern, code, re.IGNORECASE | re.DOTALL)
        for match in if_else_matches:
            self.operators_dict['if-else'] = self.operators_dict.get('if-else', 0) + 1
        
        # try-catch-finally конструкции
        try_catch_pattern = r'try\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}(?:\s*catch\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})*(?:\s*finally\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})?'
        try_catch_matches = re.findall(try_catch_pattern, code, re.IGNORECASE | re.DOTALL)
        for match in try_catch_matches:
            self.operators_dict['try-catch'] = self.operators_dict.get('try-catch', 0) + 1
        
        # switch-case-default конструкции
        switch_case_pattern = r'switch\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        switch_case_matches = re.findall(switch_case_pattern, code, re.IGNORECASE | re.DOTALL)
        for match in switch_case_matches:
            self.operators_dict['switch-case'] = self.operators_dict.get('switch-case', 0) + 1

    def _extract_operands(self, code):
        code = self._remove_comments(code)
        code_no_strings = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '', code)

        variables = re.findall(r'\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', code_no_strings)
        for var in variables:
            self.operands_dict[var] = self.operands_dict.get(var, 0) + 1

        numbers = re.findall(r'\b\d+\.?\d*\b', code_no_strings)
        for num in numbers:
            self.operands_dict[num] = self.operands_dict.get(num, 0) + 1

        for m in re.finditer(r'(["\'])(?:(?=(\\?))\2.)*?\1', code):
            literal = m.group(0)
            # Извлекаем содержимое между кавычками и нормализуем
            content = literal[1:-1]  # убираем первую и последнюю кавычку
            content = content.strip()  # убираем пробелы в начале и конце
            # Добавляем как операнд с нормализованным содержимым
            self.operands_dict[content] = self.operands_dict.get(content, 0) + 1

        constants = re.findall(r'\b(true|false|null)\b', code_no_strings, re.IGNORECASE)
        for const in constants:
            self.operands_dict[const.lower()] = self.operands_dict.get(const.lower(), 0) + 1

        # Имена функций, классов, методов - это операторы
        # Исключаем зарезервированные слова PHP
        php_keywords = {
            'if', 'else', 'elseif', 'switch', 'case', 'default', 'while', 'do', 'for', 'foreach',
            'break', 'continue', 'function', 'return', 'class', 'interface', 'trait', 'try', 'catch',
            'finally', 'throw', 'echo', 'print', 'isset', 'empty', 'unset', 'private', 'public',
            'protected', 'static', 'abstract', 'final', 'const', 'var', 'global', 'include',
            'require', 'include_once', 'require_once', 'new', 'clone', 'instanceof', 'and', 'or',
            'xor', 'as', 'foreach', 'endfor', 'endif', 'endwhile', 'endswitch', 'endforeach',
            'declare', 'enddeclare', 'list', 'array', 'die', 'exit', 'eval', 'isset', 'unset',
            'empty', 'print', 'echo', 'return', 'yield', 'yield from', 'use', 'namespace',
            'extends', 'implements', 'insteadof', 'trait', 'as', 'public', 'protected', 'private',
            'static', 'abstract', 'final', 'const', 'readonly', 'var', 'global', 'static',
            'include', 'require', 'include_once', 'require_once', 'goto', 'fn', 'match',
            'enum', 'readonly', 'never', 'mixed', 'union', 'intersection', 'true', 'false', 'null'
        }
        
        # Находим все идентификаторы (имена функций, классов, методов) как операторы
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code_no_strings)
        for identifier in identifiers:
            # Пропускаем зарезервированные слова PHP
            if identifier.lower() not in php_keywords:
                self.operators_dict[identifier] = self.operators_dict.get(identifier, 0) + 1

        self.eta2 = len(self.operands_dict)
        self.N2 = sum(self.operands_dict.values())

    def _remove_comments(self, code):
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code

    def _calculate_metrics(self):
        self.eta = self.eta1 + self.eta2
        self.N = self.N1 + self.N2
        if self.eta > 0:
            self.V = self.N * math.log2(self.eta)
        else:
            self.V = 0

    def get_results_table(self):
        results = []
        results.append("j | Оператор | fij")
        results.append("-" * 40)
        for j, (operator, count) in enumerate(self.operators_dict.items(), 1):
            results.append(f"{j} | {operator} | {count}")

        results.append("")
        results.append(f"η1 = {self.eta1} | N1 = {self.N1}")
        results.append("")

        results.append("i | Операнд | fzi")
        results.append("-" * 40)

        for i, (operand, count) in enumerate(self.operands_dict.items(), 1):
            results.append(f"{i} | {operand} | {count}")

        results.append("")
        results.append(f"η2 = {self.eta2} | N2 = {self.N2}")

        return results

    def get_extended_metrics(self):
        return {
            "Словарь программы (η)": self.eta,
            "Длина программы (N)": self.N,
            "Объем программы (V)": round(self.V, 2)
        }


class HalsteadAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор метрик Холстеда для PHP")
        self.root.geometry("900x700")

        self.parser = HalsteadParser()

        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть файл", command=self.open_file)
        file_menu.add_command(label="Сохранить как", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Кнопки для работы с файлами
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        ttk.Button(button_frame, text="Открыть файл", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Сохранить", command=self.save_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Очистить", command=self.clear_text).pack(side=tk.LEFT)

        ttk.Label(main_frame, text="Введите PHP код для анализа:").grid(row=1, column=0, columnspan=2, sticky=tk.W,
                                                                        pady=(0, 5))

        self.code_text = scrolledtext.ScrolledText(main_frame, width=80, height=15, wrap=tk.WORD)
        self.code_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Разрешаем вставку текста
        self.code_text.bind('<Control-v>', self.paste_text)
        self.code_text.bind('<Button-3>', self.show_context_menu)  # Правый клик для контекстного меню

        self.analyze_button = ttk.Button(main_frame, text="Анализировать код", command=self.analyze_code)
        self.analyze_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.basic_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.basic_frame, text="Базовые метрики")
        self.basic_text = scrolledtext.ScrolledText(self.basic_frame, width=80, height=20, wrap=tk.WORD)
        self.basic_text.pack(fill=tk.BOTH, expand=True)

        self.extended_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.extended_frame, text="Расширенные метрики")
        self.extended_text = scrolledtext.ScrolledText(self.extended_frame, width=80, height=10, wrap=tk.WORD)
        self.extended_text.pack(fill=tk.BOTH, expand=True)

        self.insert_example_code()

    def paste_text(self, event=None):
        try:
            self.code_text.event_generate('<<Paste>>')
            return "break"
        except:
            pass

    def show_context_menu(self, event):
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Вставить", command=lambda: self.code_text.event_generate('<<Paste>>'))
        context_menu.add_command(label="Копировать", command=lambda: self.code_text.event_generate('<<Copy>>'))
        context_menu.add_command(label="Вырезать", command=lambda: self.code_text.event_generate('<<Cut>>'))
        context_menu.tk_popup(event.x_root, event.y_root)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Открыть PHP файл",
            filetypes=[("PHP files", "*.php"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert("1.0", content)
                self.root.title(f"Анализатор метрик Холстеда - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить как",
            defaultextension=".php",
            filetypes=[("PHP files", "*.php"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                content = self.code_text.get("1.0", tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Успех", "Файл успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def clear_text(self):
        self.code_text.delete("1.0", tk.END)

    def insert_example_code(self):
        example_code = """<?php
// Пример PHP кода для вычисления факториала
function calculateFactorial($n) {
    if ($n <= 1) {
        return 1;
    } else {
        return $n * calculateFactorial($n - 1);
    }
}

$number = 5;
$result = calculateFactorial($number);
echo "Факториал числа $number равен: " . $result;
?>"""
        self.code_text.insert(tk.END, example_code)

    def analyze_code(self):
        code = self.code_text.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите PHP код для анализа.")
            return

        try:
            self.parser.parse_code(code)
            basic_results = self.parser.get_results_table()
            self.basic_text.delete("1.0", tk.END)
            self.basic_text.insert(tk.END, "\n".join(basic_results))

            extended_metrics = self.parser.get_extended_metrics()
            extended_text = "Расширенные метрики Холстеда:\n\n"
            for metric, value in extended_metrics.items():
                extended_text += f"{metric}: {value}\n"
            self.extended_text.delete("1.0", tk.END)
            self.extended_text.insert(tk.END, extended_text)

            messagebox.showinfo("Успех", "Анализ кода завершен успешно!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при анализе кода: {str(e)}")


def main():
    root = tk.Tk()
    app = HalsteadAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()