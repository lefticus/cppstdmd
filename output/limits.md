---
current_file: limits
label_index_file: converted/cppstdmd/output/cpp_std_labels.lua
source_dir: ../../cplusplus-draft/source
---

Because computers are finite, C++ implementations are inevitably limited
in the size of the programs they can successfully process. Every
implementation shall document those limitations where known. This
documentation may cite fixed limits where they exist, say how to compute
variable limits as a function of available resources, or say that fixed
limits do not exist or are unknown.

The limits may constrain quantities that include those described below
or others. The bracketed number following each quantity is recommended
as the minimum for that quantity. However, these quantities are only
guidelines and do not determine compliance.

- Nesting levels of compound statements [[stmt.block]], iteration
  control structures [[stmt.iter]], and selection control structures
  [[stmt.select]] \[256\].
- Nesting levels of conditional inclusion [[cpp.cond]] \[256\].
- Pointer [[dcl.ptr]], pointer-to-member [[dcl.mptr]], array
  [[dcl.array]], and function [[dcl.fct]] declarators (in any
  combination) modifying a type in a declaration \[256\].
- Nesting levels of parenthesized expressions [[expr.prim.paren]] within
  a full-expression \[256\].
- Number of characters in an internal identifier [[lex.name]] or macro
  name [[cpp.replace]] \[1 024\].
- Number of characters in an external identifier
  [[lex.name]], [[basic.link]] \[1 024\].
- External identifiers [[basic.link]] in one translation unit
  \[65 536\].
- Identifiers with block scope declared in one block
  [[basic.scope.block]] \[1 024\].
- Structured bindings [[dcl.struct.bind]] introduced in one declaration
  \[256\].
- Macro identifiers [[cpp.replace]] simultaneously defined in one
  translation unit \[65 536\].
- Parameters in one function definition [[dcl.fct.def.general]] \[256\].
- Arguments in one function call [[expr.call]] \[256\].
- Parameters in one macro definition [[cpp.replace]] \[256\].
- Arguments in one macro invocation [[cpp.replace]] \[256\].
- Characters in one logical source line [[lex.phases]] \[65 536\].
- Characters in a *string-literal* [[lex.string]] (after concatenation
  [[lex.phases]]) \[65 536\].
- Size of an object [[intro.object]] \[262 144\].
- Nesting levels for `#include` files [[cpp.include]] \[256\].
- Case labels for a `switch` statement [[stmt.switch]] (excluding those
  for any nested `switch` statements) \[16 384\].
- Non-static data members (including inherited ones) in a single class
  [[class.mem]] \[16 384\].
- Lambda-captures in one *lambda-expression*
  [[expr.prim.lambda.capture]] \[256\].
- Enumeration constants in a single enumeration [[dcl.enum]] \[4 096\].
- Levels of nested class definitions [[class.nest]] in a single
  *member-specification* \[256\].
- Functions registered by `atexit()` [[support.start.term]] \[32\].
- Functions registered by `at_quick_exit()` [[support.start.term]]
  \[32\].
- Direct and indirect base classes [[class.derived]] \[16 384\].
- Direct base classes for a single class [[class.derived]] \[1 024\].
- Class members declared in a single *member-specification* (including
  member functions) [[class.mem]] \[4 096\].
- Final overriding virtual functions in a class, accessible or not
  [[class.virtual]] \[16 384\].
- Direct and indirect virtual bases of a class [[class.mi]] \[1 024\].
- Static data members of a class [[class.static.data]] \[1 024\].
- Friend declarations in a class [[class.friend]] \[4 096\].
- Access control declarations in a class [[class.access.spec]]
  \[4 096\].
- Member initializers in a constructor definition [[class.base.init]]
  \[6 144\].
- *initializer-clause* in one *braced-init-list* [[dcl.init]]
  \[16 384\].
- Scope qualifications of one identifier [[expr.prim.id.qual]] \[256\].
- Nested *linkage-specification*s [[dcl.link]] \[1 024\].
- Recursive constexpr function invocations [[dcl.constexpr]] \[512\].
- Full-expressions evaluated within a core constant expression
  [[expr.const]] \[1 048 576\].
- Template parameters in a template declaration [[temp.param]]
  \[1 024\].
- Recursively nested template instantiations [[temp.inst]], including
  substitution during template argument deduction [[temp.deduct]]
  \[1 024\].
- Handlers per try block [[except.handle]] \[256\].
- Number of placeholders [[func.bind.place]] \[10\].

<!-- Link reference definitions -->
[basic.link]: basic.md#basic.link
[basic.scope.block]: basic.md#basic.scope.block
[class.access.spec]: class.md#class.access.spec
[class.base.init]: class.md#class.base.init
[class.derived]: class.md#class.derived
[class.friend]: class.md#class.friend
[class.mem]: class.md#class.mem
[class.mi]: class.md#class.mi
[class.nest]: class.md#class.nest
[class.static.data]: class.md#class.static.data
[class.virtual]: class.md#class.virtual
[cpp.cond]: cpp.md#cpp.cond
[cpp.include]: cpp.md#cpp.include
[cpp.replace]: cpp.md#cpp.replace
[dcl.array]: dcl.md#dcl.array
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def.general]: dcl.md#dcl.fct.def.general
[dcl.init]: dcl.md#dcl.init
[dcl.link]: dcl.md#dcl.link
[dcl.mptr]: dcl.md#dcl.mptr
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.struct.bind]: dcl.md#dcl.struct.bind
[except.handle]: except.md#except.handle
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.prim.id.qual]: expr.md#expr.prim.id.qual
[expr.prim.lambda.capture]: expr.md#expr.prim.lambda.capture
[expr.prim.paren]: expr.md#expr.prim.paren
[func.bind.place]: utilities.md#func.bind.place
[intro.object]: basic.md#intro.object
[lex.name]: lex.md#lex.name
[lex.phases]: lex.md#lex.phases
[lex.string]: lex.md#lex.string
[stmt.block]: stmt.md#stmt.block
[stmt.iter]: stmt.md#stmt.iter
[stmt.select]: stmt.md#stmt.select
[stmt.switch]: stmt.md#stmt.switch
[support.start.term]: support.md#support.start.term
[temp.deduct]: temp.md#temp.deduct
[temp.inst]: temp.md#temp.inst
[temp.param]: temp.md#temp.param
