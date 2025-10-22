// ----------------- массивы операторов -----------------
const ARRAY_OF_JILBA_OPERATORS = [
  /\bif\b/,
  /\belseif\b/,
  /\belse\b/,
  /\bwhile\b/,
  /\bfor\b/,
  /\bforeach\b/,
  /\bdo\b/,
  /\bunless\b/,
  /\bwhen\b/,
  /\bdefault\b/,
  /\bcase\b/
];

const ARRAY_OF_JILBA_OPERATORS_ABSOLUTE = [
  /\bif\b/,
  /\belseif\b/,
  /\bwhile\b/,
  /\bfor\b/,
  /\bforeach\b/,
  /\bdo\b/,
  /\bunless\b/,
  /\bgiven\b/,
  /\bwhen\b/,
  /\bcase\b/,
];

// длинные операторы первыми
const ARRAY_OF_ALL_OPERATORS = [
  /===/,
  /==/,
  /=/,
  /\bif\b/,
  /\bcase\b/,
  /\bdefault\b/,   // ✅ default как отдельный оператор
  /\belseif\b/,
  /\belse\b/,
  /\bwhile\b/,
  /\bfor\b/,
  /\bforeach\b/,
  /\bdo\b/,
  /\bunless\b/,
  /\bswitch\b/,
  /\bbreak\b/,
  /\bcontinue\b/,
  /&&/,
  /\|\|/,
  /!/,

  /\bnot\b/,
  /\band\b/,
  /\bor\b/,
  /!=/,
  />=/,
  /<=/,
  /</,
  />/,
  /cmp/,
  /eq/,
  /ne/,
  /gt/,
  /lt/,
  /ge/,
  /\ble\b/,
  /\+\+/,
  /--/,
  /\+=/,
  /-=/,
  /\*=/,
  /\/=/,
  /%=/,
  /\+/,
  /-/,
  /\*/,
  /\//,
  /%/,
  /\./,
  /=>/,
  /:/,
  /\bprint\b/,
  /\becho\b/,
  /;/,
  /\\/,
  /{/
];

// ----------------- утилиты -----------------
function cleanLine(line) {
  line = line.replace(/<\?php/g, ""); // убираем <?php
  line = line.replace(/<php/g, "");
  line = line.replace(/\/\/.*$/g, ""); // комментарии
  line = line.replace(/#.*$/g, "");
  line = line.replace(/\/\*[\s\S]*?\*\//g, "");
  line = line.replace(/"(?:\\.|[^"\\])*"/g, ""); // строки в ""
  line = line.replace(/'(?:\\.|[^'\\])*'/g, ""); // строки в ''
  return line;
}

function countOperators(lines, operators) {
  const counts = {};
  for (const op of operators) {
    counts[op.source] = 0;
  }

  for (let line of lines) {
    let clean = cleanLine(line);
    for (const op of operators) {
      const regex = new RegExp(op, "g");
      let match;
      while ((match = regex.exec(clean)) !== null) {
        counts[op.source]++;
        clean =
          clean.substring(0, match.index) +
          " ".repeat(match[0].length) +
          clean.substring(match.index + match[0].length);
      }
    }
  }
  return counts;
}

function countAllOperators(lines) {
  return countOperators(lines, ARRAY_OF_ALL_OPERATORS);
}

function countJilbaOperators(lines) {
  return countOperators(lines, ARRAY_OF_JILBA_OPERATORS_ABSOLUTE);
}

function countNestingLevel(lines) {
  let maxNesting = 0;
  let currentNesting = 0;

  // Стек switch-блоков с фиксацией уровня открытия
  const switchStack = [];

  for (const rawLine of lines) {
    const line = cleanLine(rawLine);
    if (line.startsWith("<php")) continue;

    // Поcимвольный проход по строке для корректного порядка событий
    for (let i = 0; i < line.length; i++) {
      // Ключевые слова
      if (/\bswitch\b/.test(line.slice(i))) {
        // Помечаем, что ждём ближайшую '{' как начало switch-блока
        switchStack.push({ openLevel: null, caseCount: 0, hasDefault: false, awaitingOpen: true });
      }
      if (switchStack.length > 0) {
        if (/\bcase\b/.test(line.slice(i))) {
          switchStack[switchStack.length - 1].caseCount++;
        } else if (/\bdefault\b/.test(line.slice(i))) {
          switchStack[switchStack.length - 1].hasDefault = true;
        }
      }

      const ch = line[i];
      if (ch === '{') {
        currentNesting++;
        if (currentNesting > maxNesting) {
          maxNesting = currentNesting;
        }
        // Фиксируем уровень открытия для верхнего switch, если он ожидал '{'
        if (switchStack.length > 0) {
          const top = switchStack[switchStack.length - 1];
          if (top.awaitingOpen) {
            top.openLevel = currentNesting;
            top.awaitingOpen = false;
          }
        }
      } else if (ch === '}') {
        // Если закрывается именно блок switch (по уровню), сначала считаем вклад
        if (switchStack.length > 0) {
          const top = switchStack[switchStack.length - 1];
          if (top.openLevel !== null && currentNesting === top.openLevel) {
            const extraLevel = Math.max(0, top.caseCount - (top.hasDefault ? 2 : 1));
            const totalLevel = currentNesting + extraLevel;
            if (totalLevel > maxNesting) {
              maxNesting = totalLevel;
            }
            switchStack.pop();
          }
        }
        currentNesting = Math.max(0, currentNesting - 1);
      }
    }
  }

  return maxNesting;
}



// ----------------- анализ -----------------
function analyzeCode() {
  const sourceCode = document.getElementById("sourceCode").value;
  const lines = sourceCode
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  const countAllOperatorsResult = countAllOperators(lines);
  const countJilbaOperatorsResult = countJilbaOperators(lines);
  const maxNesting = countNestingLevel(lines);

  document.getElementById("countIF").innerText = Object.values(countJilbaOperatorsResult).reduce((a, b) => a + b, 0);
  document.getElementById("countAllOperators").innerText = Object.values(countAllOperatorsResult).reduce((a, b) => a + b, 0);
  document.getElementById("maxNesting").innerText = maxNesting;
  document.getElementById("attitude").innerText = (
    Object.values(countJilbaOperatorsResult).reduce((a, b) => a + b, 0) /
    (Object.values(countAllOperatorsResult).reduce((a, b) => a + b, 0) || 1)
  ).toFixed(2);

  // таблица
  const operatorTableBody = document.getElementById("operatorCountsBody");
  operatorTableBody.innerHTML = "";

  let caseDefaultCount = (countAllOperatorsResult["\\bcase\\b"] || 0) + (countAllOperatorsResult["\\bdefault\\b"] || 0);

  for (const [operator, count] of Object.entries(countAllOperatorsResult)) {
    if (operator === "\\bcase\\b" || operator === "\\bdefault\\b") {
      continue; // отдельно обработаем ниже
    }
    if (count > 0) {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${operator}</td><td>${count}</td>`;
      operatorTableBody.appendChild(row);
    }
  }

  // добавляем объединённую строку case/default
  if (caseDefaultCount > 0) {
    const row = document.createElement("tr");
    row.innerHTML = `<td>case/default</td><td>${caseDefaultCount}</td>`;
    operatorTableBody.appendChild(row);
  }
}

// ----------------- кнопки -----------------
document.getElementById("analyzeButton").addEventListener("click", analyzeCode);
document.getElementById("clearButton").addEventListener("click", () => {
  document.getElementById("sourceCode").value = "";
  document.getElementById("countIF").innerText = "0";
  document.getElementById("countAllOperators").innerText = "0";
  document.getElementById("maxNesting").innerText = "0";
  document.getElementById("attitude").innerText = "0";
  const operatorTableBody = document.getElementById("operatorCountsBody");
  operatorTableBody.innerHTML = "";
});

// загрузка кода из файла
document.getElementById("loadButton").addEventListener("click", () => {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      document.getElementById("sourceCode").value = e.target.result;
    };

    reader.readAsText(file);
  } else {
    alert("Please select a file first.");
  }
});

// ----------------- автотесты (консоль) -----------------
function runAutoTests() {
  const log = console.log.bind(console);
  const asSum = (obj) => Object.values(obj).reduce((a, b) => a + b, 0);
  const lines = (code) => code.split("\n").map((l) => l.trim()).filter((l) => l.length > 0);

  const check = (name, code, expectedAbs) => {
    const l = lines(code);
    const abs = asSum(countJilbaOperators(l));
    const all = asSum(countAllOperators(l));
    const ok = abs === expectedAbs;
    log(`${ok ? "✅" : "❌"} ${name}: abs=${abs} (ожидалось ${expectedAbs}), all=${all}`);
  };

  // Базовые кейсы
  check("TC1 if без else", `if (a > 0) { print(a); }`, 1);
  check("TC2 if с else", `if (a > 0) { print(a); } else { print(0); }`, 1);
  check(
    "TC3 if/elseif/else",
    `if (a > 0) { print(1); } elseif (a < 0) { print(-1); } else { print(0); }`,
    2
  );
  check(
    "TC4 switch/case/default",
    `switch (x) { case 1: print(1); break; case 2: print(2); break; default: print(0); }`,
    3
  );

  // Ключевые проверки про else
  const codeNoElse = `if (a) { print(1); }`;
  const codeWithElse = `if (a) { print(1); } else { print(0); }`;
  const absNoElse = asSum(countJilbaOperators(lines(codeNoElse)));
  const absWithElse = asSum(countJilbaOperators(lines(codeWithElse)));
  const allNoElse = asSum(countAllOperators(lines(codeNoElse)));
  const allWithElse = asSum(countAllOperators(lines(codeWithElse)));
  log(`${absNoElse === absWithElse ? "✅" : "❌"} Абсолютная сложность не меняется при добавлении else: ${absNoElse} vs ${absWithElse}`);
  log(`${allWithElse > allNoElse ? "✅" : "❌"} Все операторы учитывают else: ${allNoElse} -> ${allWithElse}`);
}

window.addEventListener("DOMContentLoaded", runAutoTests);
