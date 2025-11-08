# Macro Classification Guide

This document provides guidelines for deciding which C++ standard macros should be handled by `simplified_macros.tex` (Pandoc preprocessing) vs `cpp-macros.lua` (Lua filter processing).

## Quick Reference

**Use simplified_macros.tex for:**
- ✅ Simple text substitution (e.g., `\Cpp` → `C++`)
- ✅ No nesting relationships
- ✅ No context-dependent behavior
- ✅ No special parsing requirements

**Use Lua filters for:**
- ❌ Macros that can contain other macros
- ❌ Macros that can be nested inside other macros
- ❌ Context-dependent macros (BNF vs text, tables vs code)
- ❌ Macros requiring complex parsing or AST manipulation

## Why This Matters

### Pandoc Macro Expansion is Context-Unaware

When Pandoc expands macros via `\renewcommand`, it does so **BEFORE** parsing the document structure. This means:

1. **Cannot preserve nesting**: `\tcode{\keyword{unsigned}}` becomes two separate code blocks
2. **Cannot apply context-specific logic**: `\grammarterm{}` in BNF vs regular text needs different output
3. **Cannot access parsed structure**: No way to know if macro is inside a code block, table, or BNF environment

### Lua Filters Have Full AST Access

Lua filters operate on the parsed Abstract Syntax Tree, which enables:

1. **Context awareness**: Know if processing BNF block, table cell, code block, etc.
2. **Nested macro handling**: Process inner macros before outer macros with correct ordering
3. **Complex transformations**: Access to full Pandoc AST manipulation capabilities

## Detailed Examples

### ✅ SAFE for simplified_macros.tex

#### Category A: Simple Text Substitution (20 macros)
```latex
\renewcommand{\Cpp}{C++}
\renewcommand{\CppXI}{C++11}
\renewcommand{\cv}{cv}
\renewcommand{\ntbs}{NTBS}
```

**Why safe:**
- Constant strings with no arguments
- Never nested
- No context-dependent behavior

#### Category D: Library Specifications (7 macros)
```latex
\renewcommand{\seebelow}{\textit{see below}}
\renewcommand{\unspec}{\textit{unspecified}}
\renewcommand{\expos}{\textit{exposition only}}
```

**Why safe:**
- Simple text with italic formatting
- Never contain other macros
- Same output in all contexts

#### Category E: Fundesc Labels (24 macros)
```latex
\renewcommand{\expects}{\textit{Preconditions:} }
\renewcommand{\returns}{\textit{Returns:} }
```

**Why safe:**
- Fixed text labels
- Never nested or context-dependent

### ❌ MUST Use Lua Filters

#### Nesting-Sensitive Macros

##### `\tcode{}` - Contains Nested Macros

**Problem:**
```latex
\tcode{\keyword{unsigned} \keyword{char}}
```

With Pandoc expansion:
1. `\tcode{}` → `\texttt{}` (via simplified_macros.tex)
2. `\keyword{}` → `\texttt{}` (via simplified_macros.tex)
3. Result: ``` `unsigned`` ``char` ``` (TWO code blocks)

With Lua handling:
1. Process `\keyword{}` first → `\texttt{unsigned} \texttt{char}`
2. Process `\tcode{}` second → `\texttt{\texttt{unsigned} \texttt{char}}`
3. Pandoc merges nested `\texttt{}` → ``` `unsigned char` ``` (ONE code block)

**Why Lua required:**
- Must process inner macros (`\keyword{}`, `\ctype{}`, etc.) BEFORE outer `\tcode{}`
- Order matters for correct nesting

##### `\keyword{}` - Nested Inside `\tcode{}`

**Problem:**
```latex
\tcode{\keyword{auto}}
```

If `\keyword{}` is in simplified_macros.tex, Pandoc expands it independently, breaking the nesting.

**Why Lua required:**
- Frequently appears inside `\tcode{}`
- Must be processed in correct order with `\tcode{}`

##### `\ctype{}` - Nested Inside `\tcode{}`

**Problem:**
```latex
\tcode{\ctype{size_t}}
```

Same nesting issue as `\keyword{}`.

**Why Lua required:**
- Can appear inside `\tcode{}`
- Same nesting preservation requirement

#### Context-Dependent Macros

##### `\grammarterm{}` - BNF vs Text Context

**Problem:**
```latex
% Inside BNF block
\begin{ncbnf}
\grammarterm{declarator}  % Should output: declarator (plain text)
\end{ncbnf}

% In regular text
\grammarterm{declarator}  % Should output: *declarator* (italic)
```

With Pandoc expansion: Always outputs `\textit{declarator}`, wrong in BNF context.

With Lua handling: Can check if inside `ncbnf` environment and output plain text or italic accordingly.

**Why Lua required:**
- Different output based on context
- Pandoc cannot distinguish BNF from regular text

**Special case:** `\opt{\grammarterm{...}}` requires brace-balanced parsing in Lua.

##### `\placeholder{}` and `\placeholdernc{}` - Code vs Text

**Problem:**
```latex
% Inside code block
\begin{codeblock}
\placeholder{type}  % Should output: *type* (emphasis in code)
\end{codeblock}

% In regular text
\placeholder{type}  % Should output: *type* (italic)
```

**Why Lua required:**
- Behavior depends on whether inside code block
- Needs AST context to determine correct output

#### Special Processing Requirements

##### `\stage{}` - Description Lists

**Problem:**
```latex
\stage{1}{Expression} This is the description.
```

Needs to be processed into description list format. Requires extracting stage number and name, then restructuring the AST.

**Why Lua required:**
- Complex parsing and restructuring
- Cannot be done with simple text substitution

##### `\impdefx{}` - Nested Macro Extraction

**Problem:**
```latex
\impdefx{the meaning of \tcode{foo}}
```

Needs to extract description with nested macros intact, then process them in correct order.

**Why Lua required:**
- Brace-balanced parsing required
- Must preserve nested macro structure for later processing

## Macro Classification Checklist

When adding or moving a macro, ask these questions:

1. **Can this macro contain other macros?**
   - YES → Lua filter
   - NO → Continue

2. **Can this macro be nested inside other macros?**
   - YES → Lua filter
   - NO → Continue

3. **Does this macro behave differently in different contexts?**
   - YES → Lua filter
   - NO → Continue

4. **Does this macro require special parsing or AST manipulation?**
   - YES → Lua filter
   - NO → simplified_macros.tex is safe

## Current Macro Distribution

### simplified_macros.tex (77 macros, ~73% of usage)

- **Category A**: Simple Text Substitution (20 macros)
  - `\Cpp`, `\CppXI-XXVI`, `\IsoC`, `\cv`, `\ntbs`, etc.

- **Category B**: Code Formatting (7 macros, safe subset)
  - `\libheader{}`, `\libheaderdef{}`, `\libheaderref{}`
  - `\libconcept{}`, `\exposconcept{}`, `\libglobal{}`, `\deflibconcept{}`
  - NOTE: `\tcode{}`, `\keyword{}`, `\ctype{}` removed (nesting issues)

- **Category C**: Emphasis Formatting (6 macros, safe subset)
  - `\exposid{}`, `\exposidnc{}`, `\defn{}`, `\term{}`, `\oldconcept{}`, `\doccite{}`
  - NOTE: `\grammarterm{}`, `\placeholder{}`, `\placeholdernc{}` removed (context-dependent)

- **Category D**: Library Specifications (7 macros)
  - `\seebelow`, `\unspec`, `\unspecnc`, `\expos`, `\impldef`, `\notdef`, `\impdef`

- **Category E**: Fundesc Labels (24 macros)
  - `\expects`, `\requires`, `\constraints`, `\effects`, `\ensures`, `\returns`, etc.

- **Category F**: Ranges (5 macros)
  - `\range{}`, `\crange{}`, `\brange{}`, `\orange{}`, `\countedrange{}`

- **Category G**: Change Descriptions (3 macros)
  - `\change`, `\rationale`, `\effect`

- **Category H**: Special Formatting (3 macros)
  - `\cppver`, `\tablerefheader{}`, `\columnline`

- **Category I**: Phase 3 Additions (2 macros)
  - `\deflibconcept{}`, `\uname{}`

### cpp-macros.lua (Remaining macros requiring Lua)

- **Nesting-sensitive**:
  - `\tcode{}`, `\keyword{}`, `\ctype{}`
  - Special handling for macros that can be nested

- **Context-dependent**:
  - `\grammarterm{}` (BNF vs text)
  - `\placeholder{}`, `\placeholdernc{}` (code vs text)

- **Special processing**:
  - `\stage{}` (description list processing)
  - `\impdefx{}` (nested macro extraction)
  - `\fundescx{}`, fundesc labels (complex expansion)
  - `\defnx{}`, `\defnadj{}` (brace-balanced parsing)
  - `\opt{\grammarterm{...}}` (special case)
  - `\colcol{}`, `\mathrm{}`, `\bigoh{}` (context-dependent)

## Investigation History

### Phase 3d Results (Before Refinement)

After moving macros to simplified_macros.tex:
- **28 test failures** (92% pass rate)

### Phase 3e Results (After Refinement)

After removing context-dependent and nesting-sensitive macros:
- **10 test failures** (97.1% pass rate)
- **18 tests fixed** (64% of failures resolved)

### Remaining Issues (Not Macro-Related)

The 10 remaining failures are not caused by macro preprocessing:

1. **Line wrapping (4-5 tests)**: Pandoc inserts newlines for text flow
   - test_defnx_emphasis
   - test_defn_with_nested_braces
   - test_defnadj_with_nested_braces
   - test_tref_in_description_list_with_linebreak

2. **Markdown escaping (1 test)**: Pandoc escapes special Markdown characters
   - test_range_macro (escapes `[` to `\[`)

3. **Context-specific handling (3-4 tests)**: Require special Lua logic
   - test_caret (BNF context)
   - test_multiple_labels_in_blockquote (fundesc)
   - test_ensures_vs_postconditions (fundesc)
   - test_floattable_with_special_char_macros (table context)
   - test_oldconcepttable_with_tailnote (table context)

## Future Macro Additions

When adding support for new C++ standard macros:

1. **Default to Lua filters first** - Safer approach
2. **Check classification checklist** - Determine if simplified_macros.tex is safe
3. **Add unit test** - Verify macro works in all contexts
4. **Document decision** - Update this guide if classification is non-obvious

## Key Takeaway

**Pandoc macro preprocessing is a performance optimization for simple, context-independent macros.** It reduces Lua filter complexity by ~73%, but cannot replace Lua filters entirely.

**When in doubt, use Lua filters.** The AST access is worth the minimal performance cost for correctness.
