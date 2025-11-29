# Implementation quantities (informative) <a id="implimits" data-annex="true" data-annex-type="informative">[[implimits]]</a>

Because computers are finite, C++implementations are inevitably limited
in the size of the programs they can successfully process. Every
implementation shall document those limitations where known. This
documentation may cite fixed limits where they exist, say how to compute
variable limits as a function of available resources, or say that fixed
limits do not exist or are unknown.

The limits may constrain quantities that include those described below
or others. The bracketed number following each quantity is recommended
as the minimum for that quantity. However, these quantities are only
guidelines and do not determine compliance.

- Nesting levels of compound statements, iteration control structures,
  and selection control structures \[256\].
- Nesting levels of conditional inclusion \[256\].
- Pointer, array, and function declarators (in any combination)
  modifying a class, arithmetic, or incomplete type in a declaration
  \[256\].
- Nesting levels of parenthesized expressions within a full-expression
  \[256\].
- Number of characters in an internal identifier or macro name
  \[1 024\].
- Number of characters in an external identifier \[1 024\].
- External identifiers in one translation unit \[65 536\].
- Identifiers with block scope declared in one block \[1 024\].
- Structured bindings introduced in one declaration \[256\].
- Macro identifiers simultaneously defined in one translation unit
  \[65 536\].
- Parameters in one function definition \[256\].
- Arguments in one function call \[256\].
- Parameters in one macro definition \[256\].
- Arguments in one macro invocation \[256\].
- Characters in one logical source line \[65 536\].
- Characters in a string literal (after concatenation) \[65 536\].
- Size of an object \[262 144\].
- Nesting levels for `#include` files \[256\].
- Case labels for a `switch` statement (excluding those for any nested
  `switch` statements) \[16 384\].
- Data members in a single class \[16 384\].
- Lambda-captures in one *lambda-expression* \[256\].
- Enumeration constants in a single enumeration \[4 096\].
- Levels of nested class definitions in a single *member-specification*
  \[256\].
- Functions registered by `atexit()` \[32\].
- Functions registered by `at_quick_exit()` \[32\].
- Direct and indirect base classes \[16 384\].
- Direct base classes for a single class \[1 024\].
- Members declared in a single class \[4 096\].
- Final overriding virtual functions in a class, accessible or not
  \[16 384\].
- Direct and indirect virtual bases of a class \[1 024\].
- Static members of a class \[1 024\].
- Friend declarations in a class \[4 096\].
- Access control declarations in a class \[4 096\].
- Member initializers in a constructor definition \[6 144\].
- *initializer-clause*s in one *braced-init-list* \[16 384\].
- Scope qualifications of one identifier \[256\].
- Nested external specifications \[1 024\].
- Recursive constexpr function invocations \[512\].
- Full-expressions evaluated within a core constant expression
  \[1 048 576\].
- Template arguments in a template declaration \[1 024\].
- Recursively nested template instantiations, including substitution
  during template argument deduction ([[temp.deduct]]) \[1 024\].
- Handlers per try block \[256\].
- Number of placeholders ([[func.bind.place]]) \[10\].

<!-- Link reference definitions -->
[func.bind.place]: utilities.md#func.bind.place
[implimits]: #implimits
[temp.deduct]: temp.md#temp.deduct
