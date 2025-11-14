# Scope <a id="intro.scope">[[intro.scope]]</a>

This document specifies requirements for implementations of the C++
programming language. The first such requirement is that they implement
the language, so this document also defines C++. Other requirements and
relaxations of the first requirement appear at various places within
this document.

C++ is a general purpose programming language based on the C programming
language as described in ISO/IEC 9899:2018 *Programming languages — C*
(hereinafter referred to as the *C standard*). C++ provides many
facilities beyond those provided by C, including additional data types,
classes, templates, exceptions, namespaces, operator overloading,
function name overloading, references, free store management operators,
and additional library facilities.

# Normative references <a id="intro.refs">[[intro.refs]]</a>

The following documents are referred to in the text in such a way that
some or all of their content constitutes requirements of this document.
For dated references, only the edition cited applies. For undated
references, the latest edition of the referenced document (including any
amendments) applies.[^1]

The library described in ISO/IEC 9899:2018, Clause 7, is hereinafter
called the *C standard library*.[^2]

The operating system interface described in ISO/IEC 9945:2009 is
hereinafter called *POSIX*.

The ECMAScript Language Specification described in Standard Ecma-262 is
hereinafter called *ECMA-262*.

# Terms and definitions <a id="intro.defs">[[intro.defs]]</a>

For the purposes of this document, the terms and definitions given in
ISO/IEC 2382, the terms, definitions, and symbols given in ISO
80000-2:2009, and the following apply.

ISO and IEC maintain terminology databases for use in standardization at
the following addresses:

- ISO Online browsing platform: available at <https://www.iso.org/obp>
- IEC Electropedia: available at <https://www.electropedia.org/>

Terms that are used only in a small portion of this document are defined
where they are used and italicized where they are defined.

#### 1 access <a id="defns.access">[defns.access]</a>

⟨execution-time action⟩ read or modify the value of an object

[*Note 1 to entry*: Only glvalues of scalar type can be used to access
objects. Reads of scalar objects are described in [[conv.lval]] and
modifications of scalar objects are described in [[expr.ass]],
[[expr.post.incr]], and [[expr.pre.incr]]. Attempts to read or modify an
object of class type typically invoke a constructor [[class.ctor]] or
assignment operator [[class.copy.assign]]; such invocations do not
themselves constitute accesses, although they may involve accesses of
scalar subobjects. — *end note*]

#### 2 arbitrary-positional stream <a id="defns.arbitrary.stream">[defns.arbitrary.stream]</a>

⟨library⟩ stream that can seek to any integral position within the
length of the stream

[*Note 1 to entry*: Every arbitrary-positional stream is also a
repositional stream [[defns.repositional.stream]]. — *end note*]

#### 3 argument <a id="defns.argument">[defns.argument]</a>

⟨function call expression⟩ expression in the comma-separated list
bounded by the parentheses

#### 4 argument <a id="defns.argument.macro">[defns.argument.macro]</a>

⟨function-like macro⟩ sequence of preprocessing tokens in the
comma-separated list bounded by the parentheses

#### 5 argument <a id="defns.argument.throw">[defns.argument.throw]</a>

⟨throw expression⟩ operand of `throw`

#### 6 argument <a id="defns.argument.templ">[defns.argument.templ]</a>

⟨template instantiation⟩ *constant-expression*, *type-id*, or
*id-expression* in the comma-separated list bounded by the angle
brackets

#### 7 block <a id="defns.block">[defns.block]</a>

⟨execution⟩ wait for some condition (other than for the implementation
to execute the execution steps of the thread of execution) to be
satisfied before continuing execution past the blocking operation

#### 8 block <a id="defns.block.stmt">[defns.block.stmt]</a>

⟨statement⟩ compound statement

#### 9 character <a id="defns.character">[defns.character]</a>

⟨library⟩ object which, when treated sequentially, can represent text

[*Note 1 to entry*: The term does not mean only `char`, `char8_t`,
`char16_t`, `char32_t`, and `wchar_t` objects [[basic.fundamental]], but
any value that can be represented by a type that provides the
definitions specified in [[strings]], [[localization]],
[[input.output]], or  [[re]]. — *end note*]

#### 10 character container type <a id="defns.character.container">[defns.character.container]</a>

⟨library⟩ class or a type used to represent a character

[*Note 1 to entry*: It is used for one of the template parameters of
the string, iostream, and regular expression class
templates. — *end note*]

#### 11 collating element <a id="defns.regex.collating.element">[defns.regex.collating.element]</a>

sequence of one or more characters within the current locale that
collate as if they were a single character

#### 12 component <a id="defns.component">[defns.component]</a>

⟨library⟩ group of library entities directly related as members,
parameters, or return types

[*Note 1 to entry*: For example, the class template `basic_string` and
the non-member function templates that operate on strings are referred
to as the *string component*. — *end note*]

#### 13 conditionally-supported <a id="defns.cond.supp">[defns.cond.supp]</a>

program construct that an implementation is not required to support

[*Note 1 to entry*: Each implementation documents all
conditionally-supported constructs that it does not
support. — *end note*]

#### 14 constant subexpression <a id="defns.const.subexpr">[defns.const.subexpr]</a>

expression whose evaluation as subexpression of a
*conditional-expression* `CE` would not prevent `CE` from being a core
constant expression

#### 15 deadlock <a id="defns.deadlock">[defns.deadlock]</a>

⟨library⟩ situation wherein one or more threads are unable to continue
execution because each is blocked waiting for one or more of the others
to satisfy some condition

#### 16 default behavior <a id="defns.default.behavior.impl">[defns.default.behavior.impl]</a>

⟨library implementation⟩ specific behavior provided by the
implementation, within the scope of the required behavior

#### 17 diagnostic message <a id="defns.diagnostic">[defns.diagnostic]</a>

message belonging to an *implementation-defined* subset of the
implementation’s output messages

#### 18 direct-non-list-initialization <a id="defns.direct.non.list.init">[defns.direct.non.list.init]</a>

direct-initialization that is not list-initialization

#### 19 dynamic type <a id="defns.dynamic.type">[defns.dynamic.type]</a>

⟨glvalue⟩ type of the most derived object to which the glvalue refers

[*Example 1*: If a pointer [[dcl.ptr]] `p` whose static type is
“pointer to class `B`” is pointing to an object of class `D`, derived
from `B` [[class.derived]], the dynamic type of the expression `*p` is
“`D`”. References [[dcl.ref]] are treated similarly. — *end example*]

#### 20 dynamic type <a id="defns.dynamic.type.prvalue">[defns.dynamic.type.prvalue]</a>

⟨prvalue⟩ static type of the prvalue expression

#### 21 expression-equivalent <a id="defns.expression.equivalent">[defns.expression.equivalent]</a>

⟨library⟩ expressions that all have the same effects, either are all
potentially-throwing or are all not potentially-throwing, and either are
all constant subexpressions or are all not constant subexpressions

[*Example 1*: For a value `x` of type `int` and a function `f` that
accepts integer arguments, the expressions `f(x + 2)`, `f(2 + x)`, and
`f(1 + x + 1)` are expression-equivalent. — *end example*]

#### 22 finite state machine <a id="defns.regex.finite.state.machine">[defns.regex.finite.state.machine]</a>

⟨regular expression⟩ unspecified data structure that is used to
represent a regular expression, and which permits efficient matches
against the regular expression to be obtained

#### 23 format specifier <a id="defns.regex.format.specifier">[defns.regex.format.specifier]</a>

⟨regular expression⟩ sequence of one or more characters that is to be
replaced with some part of a regular expression match

#### 24 handler function <a id="defns.handler">[defns.handler]</a>

⟨library⟩ non-reserved function whose definition may be provided by a
C++ program

[*Note 1 to entry*: A C++ program may designate a handler function at
various points in its execution by supplying a pointer to the function
when calling any of the library functions that install handler functions
[[support]]. — *end note*]

#### 25 ill-formed program <a id="defns.ill.formed">[defns.ill.formed]</a>

program that is not well-formed [[defns.well.formed]]

#### 26 implementation-defined behavior <a id="defns.impl.defined">[defns.impl.defined]</a>

behavior, for a well-formed program construct and correct data, that
depends on the implementation and that each implementation documents

#### 27 implementation-defined strict total order over pointers <a id="defns.order.ptr">[defns.order.ptr]</a>

⟨library⟩ *implementation-defined* strict total ordering over all
pointer values such that the ordering is consistent with the partial
order imposed by the builtin operators `<`, `>`, `<=`, `>=`, and `<=>`

#### 28 implementation limits <a id="defns.impl.limits">[defns.impl.limits]</a>

restrictions imposed upon programs by the implementation

#### 29 iostream class templates <a id="defns.iostream.templates">[defns.iostream.templates]</a>

⟨library⟩ templates that are declared in header `<iosfwd>` and take two
template arguments

[*Note 1 to entry*: The arguments are named `charT` and `traits`. The
argument `charT` is a character container class, and the argument
`traits` is a class which defines additional characteristics and
functions of the character type represented by `charT` necessary to
implement the iostream class templates. — *end note*]

#### 30 locale-specific behavior <a id="defns.locale.specific">[defns.locale.specific]</a>

behavior that depends on local conventions of nationality, culture, and
language that each implementation documents

#### 31 matched <a id="defns.regex.matched">[defns.regex.matched]</a>

⟨regular expression⟩ condition when a sequence of zero or more
characters correspond to a sequence of characters defined by the pattern

#### 32 modifier function <a id="defns.modifier">[defns.modifier]</a>

⟨library⟩ class member function other than a constructor, assignment
operator, or destructor that alters the state of an object of the class

#### 33 move assignment <a id="defns.move.assign">[defns.move.assign]</a>

⟨library⟩ assignment of an rvalue of some object type to a modifiable
lvalue of the same type

#### 34 move construction <a id="defns.move.constr">[defns.move.constr]</a>

⟨library⟩ direct-initialization of an object of some type with an rvalue
of the same type

#### 35 non-constant library call <a id="defns.nonconst.libcall">[defns.nonconst.libcall]</a>

invocation of a library function that, as part of evaluating any
expression `E`, prevents `E` from being a core constant expression

#### 36 NTCTS <a id="defns.ntcts">[defns.ntcts]</a>

⟨library⟩ sequence of values that have character type that precede the
terminating null character type value `charT()`

#### 37 observer function <a id="defns.observer">[defns.observer]</a>

⟨library⟩ class member function that accesses the state of an object of
the class but does not alter that state

[*Note 1 to entry*: Observer functions are specified as `const` member
functions. — *end note*]

#### 38 parameter <a id="defns.parameter">[defns.parameter]</a>

⟨function or catch clause⟩ object or reference declared as part of a
function declaration or definition or in the catch clause of an
exception handler that acquires a value on entry to the function or
handler

#### 39 parameter <a id="defns.parameter.macro">[defns.parameter.macro]</a>

⟨function-like macro⟩ identifier from the comma-separated list bounded
by the parentheses immediately following the macro name

#### 40 parameter <a id="defns.parameter.templ">[defns.parameter.templ]</a>

⟨template⟩ member of a *template-parameter-list*

#### 41 primary equivalence class <a id="defns.regex.primary.equivalence.class">[defns.regex.primary.equivalence.class]</a>

⟨regular expression⟩ set of one or more characters which share the same
primary sort key: that is the sort key weighting that depends only upon
character shape, and not accents, case, or locale specific tailorings

#### 42 program-defined specialization <a id="defns.prog.def.spec">[defns.prog.def.spec]</a>

⟨library⟩ explicit template specialization or partial specialization
that is not part of the C++ standard library and not defined by the
implementation

#### 43 program-defined type <a id="defns.prog.def.type">[defns.prog.def.type]</a>

⟨library⟩ non-closure class type or enumeration type that is not part of
the C++ standard library and not defined by the implementation, or a
closure type of a non-implementation-provided lambda expression, or an
instantiation of a program-defined specialization

[*Note 1 to entry*: Types defined by the implementation include
extensions [[intro.compliance]] and internal types used by the
library. — *end note*]

#### 44 projection <a id="defns.projection">[defns.projection]</a>

⟨library⟩ transformation that an algorithm applies before inspecting the
values of elements

[*Example 1*:

``` cpp
std::pair<int, std::string_view> pairs[] = {{2, "foo"}, {1, "bar"}, {0, "baz"}};
std::ranges::sort(pairs, std::ranges::less{}, [](auto const& p) { return p.first; });
```

sorts the pairs in increasing order of their `first` members:

``` cpp
{{0, "baz"}, {1, "bar"}, {2, "foo"}}
```

— *end example*]

#### 45 referenceable type <a id="defns.referenceable">[defns.referenceable]</a>

type that is either an object type, a function type that does not have
cv-qualifiers or a *ref-qualifier*, or a reference type

[*Note 1 to entry*: The term describes a type to which a reference can
be created, including reference types. — *end note*]

#### 46 regular expression <a id="defns.regex.regular.expression">[defns.regex.regular.expression]</a>

pattern that selects specific strings from a set of character strings

#### 47 replacement function <a id="defns.replacement">[defns.replacement]</a>

⟨library⟩ non-reserved function whose definition is provided by a C++
program

[*Note 1 to entry*: Only one definition for such a function is in
effect for the duration of the program’s execution, as the result of
creating the program [[lex.phases]] and resolving the definitions of all
translation units [[basic.link]]. — *end note*]

#### 48 repositional stream <a id="defns.repositional.stream">[defns.repositional.stream]</a>

⟨library⟩ stream that can seek to a position that was previously
encountered

#### 49 required behavior <a id="defns.required.behavior">[defns.required.behavior]</a>

⟨library⟩ description of replacement function and handler function
semantics applicable to both the behavior provided by the implementation
and the behavior of any such function definition in the program

[*Note 1 to entry*: If such a function defined in a C++ program fails
to meet the required behavior when it executes, the behavior is
undefined.  — *end note*]

#### 50 reserved function <a id="defns.reserved.function">[defns.reserved.function]</a>

⟨library⟩ function, specified as part of the C++ standard library, that
is defined by the implementation

[*Note 1 to entry*: If a C++ program provides a definition for any
reserved function, the results are undefined.  — *end note*]

#### 51 signature <a id="defns.signature">[defns.signature]</a>

⟨function⟩ name, parameter-type-list, and enclosing namespace

[*Note 1 to entry*: Signatures are used as a basis for name mangling
and linking. — *end note*]

#### 52 signature <a id="defns.signature.friend">[defns.signature.friend]</a>

⟨non-template friend function with trailing \grammarterm{requires-clause⟩
name, parameter-type-list, enclosing class, and trailing
*requires-clause*

#### 53 signature <a id="defns.signature.templ">[defns.signature.templ]</a>

⟨function template⟩ name, parameter-type-list, enclosing namespace,
return type, signature of the *template-head*, and trailing
*requires-clause* (if any)

#### 54 signature <a id="defns.signature.templ.friend">[defns.signature.templ.friend]</a>

⟨friend function template with constraint involving enclosing template parameters⟩
name, parameter-type-list, return type, enclosing class, signature of
the *template-head*, and trailing *requires-clause* (if any)

#### 55 signature <a id="defns.signature.spec">[defns.signature.spec]</a>

⟨function template specialization⟩ signature of the template of which it
is a specialization and its template arguments (whether explicitly
specified or deduced)

#### 56 signature <a id="defns.signature.member">[defns.signature.member]</a>

⟨class member function⟩ name, parameter-type-list, class of which the
function is a member, cv-qualifiers (if any), *ref-qualifier* (if any),
and trailing *requires-clause* (if any)

#### 57 signature <a id="defns.signature.member.templ">[defns.signature.member.templ]</a>

⟨class member function template⟩ name, parameter-type-list, class of
which the function is a member, cv-qualifiers (if any), *ref-qualifier*
(if any), return type (if any), signature of the *template-head*, and
trailing *requires-clause* (if any)

#### 58 signature <a id="defns.signature.member.spec">[defns.signature.member.spec]</a>

⟨class member function template specialization⟩ signature of the member
function template of which it is a specialization and its template
arguments (whether explicitly specified or deduced)

#### 59 signature <a id="defns.signature.template.head">[defns.signature.template.head]</a>

⟨\grammarterm{template-head⟩ template parameter list, excluding template
parameter names and default arguments, and *requires-clause* (if any)

#### 60 stable algorithm <a id="defns.stable">[defns.stable]</a>

⟨library⟩ algorithm that preserves, as appropriate to the particular
algorithm, the order of elements

[*Note 1 to entry*: Requirements for stable algorithms are given in
[[algorithm.stable]]. — *end note*]

#### 61 static type <a id="defns.static.type">[defns.static.type]</a>

type of an expression resulting from analysis of the program without
considering execution semantics

[*Note 1 to entry*: The static type of an expression depends only on
the form of the program in which the expression appears, and does not
change while the program is executing. — *end note*]

#### 62 sub-expression <a id="defns.regex.subexpression">[defns.regex.subexpression]</a>

⟨regular expression⟩ subset of a regular expression that has been marked
by parentheses

#### 63 traits class <a id="defns.traits">[defns.traits]</a>

⟨library⟩ class that encapsulates a set of types and functions necessary
for class templates and function templates to manipulate objects of
types for which they are instantiated

#### 64 unblock <a id="defns.unblock">[defns.unblock]</a>

satisfy a condition that one or more blocked threads of execution are
waiting for

#### 65 undefined behavior <a id="defns.undefined">[defns.undefined]</a>

behavior for which this document imposes no requirements

[*Note 1 to entry*: Undefined behavior may be expected when this
document omits any explicit definition of behavior or when a program
uses an erroneous construct or erroneous data. Permissible undefined
behavior ranges from ignoring the situation completely with
unpredictable results, to behaving during translation or program
execution in a documented manner characteristic of the environment (with
or without the issuance of a diagnostic message), to terminating a
translation or execution (with the issuance of a diagnostic message).
Many erroneous program constructs do not engender undefined behavior;
they are required to be diagnosed. Evaluation of a constant expression
[[expr.const]] never exhibits behavior explicitly specified as undefined
in [[intro]] through [[cpp]]. — *end note*]

#### 66 unspecified behavior <a id="defns.unspecified">[defns.unspecified]</a>

behavior, for a well-formed program construct and correct data, that
depends on the implementation

[*Note 1 to entry*: The implementation is not required to document
which behavior occurs. The range of possible behaviors is usually
delineated by this document. — *end note*]

#### 67 valid but unspecified state <a id="defns.valid">[defns.valid]</a>

⟨library⟩ value of an object that is not specified except that the
object’s invariants are met and operations on the object behave as
specified for its type

[*Example 1*: If an object `x` of type `std::vector<int>` is in a valid
but unspecified state, `x.empty()` can be called unconditionally, and
`x.front()` can be called only if `x.empty()` returns
`false`. — *end example*]

#### 68 well-formed program <a id="defns.well.formed">[defns.well.formed]</a>

C++ program constructed according to the syntax and semantic rules

# General principles <a id="intro">[[intro]]</a>

## Implementation compliance <a id="intro.compliance">[[intro.compliance]]</a>

### General <a id="intro.compliance.general">[[intro.compliance.general]]</a>

The set of *diagnosable rules* consists of all syntactic and semantic
rules in this document except for those rules containing an explicit
notation that “no diagnostic is required” or which are described as
resulting in “undefined behavior”.

Although this document states only requirements on C++ implementations,
those requirements are often easier to understand if they are phrased as
requirements on programs, parts of programs, or execution of programs.
Such requirements have the following meaning:

- If a program contains no violations of the rules in [[lex]] through
  [[thread]] and [[depr]], a conforming implementation shall, within its
  resource limits as described in [[implimits]], accept and correctly
  execute[^3] that program.
- If a program contains a violation of a rule for which no diagnostic is
  required, this document places no requirement on implementations with
  respect to that program.
- Otherwise, if a program contains a violation of any diagnosable rule
  or an occurrence of a construct described in this document as
  “conditionally-supported” when the implementation does not support
  that construct, a conforming implementation shall issue at least one
  diagnostic message.

[*Note 1*: During template argument deduction and substitution, certain
constructs that in other contexts require a diagnostic are treated
differently; see  [[temp.deduct]]. — *end note*]

Furthermore, a conforming implementation

- shall not accept a preprocessing translation unit containing a
  `#error` preprocessing directive [[cpp.error]],
- shall issue at least one diagnostic message for each `#warning` or
  `#error` preprocessing directive not following a `#error`
  preprocessing directive in a preprocessing translation unit, and
- shall not accept a translation unit with a *static_assert-declaration*
  that fails [[dcl.pre]].

For classes and class templates, the library Clauses specify partial
definitions. Private members [[class.access]] are not specified, but
each implementation shall supply them to complete the definitions
according to the description in the library Clauses.

For functions, function templates, objects, and values, the library
Clauses specify declarations. Implementations shall supply definitions
consistent with the descriptions in the library Clauses.

A C++ translation unit [[lex.phases]] obtains access to the names
defined in the library by including the appropriate standard library
header or importing the appropriate standard library named header unit
[[using.headers]].

The templates, classes, functions, and objects in the library have
external linkage [[basic.link]]. The implementation provides definitions
for standard library entities, as necessary, while combining translation
units to form a complete C++ program [[lex.phases]].

Two kinds of implementations are defined: a *hosted implementation* and
a *freestanding implementation*. A freestanding implementation is one in
which execution may take place without the benefit of an operating
system. A hosted implementation supports all the facilities described in
this document, while a freestanding implementation supports the entire
C++ language described in [[lex]] through [[cpp]] and the subset of the
library facilities described in [[compliance]].

A conforming implementation may have extensions (including additional
library functions), provided they do not alter the behavior of any
well-formed program. Implementations are required to diagnose programs
that use such extensions that are ill-formed according to this document.
Having done so, however, they can compile and execute such programs.

Each implementation shall include documentation that identifies all
conditionally-supported constructs that it does not support and defines
all locale-specific characteristics.[^4]

### Abstract machine <a id="intro.abstract">[[intro.abstract]]</a>

The semantic descriptions in this document define a parameterized
nondeterministic abstract machine. This document places no requirement
on the structure of conforming implementations. In particular, they need
not copy or emulate the structure of the abstract machine. Rather,
conforming implementations are required to emulate (only) the observable
behavior of the abstract machine as explained below.[^5]

Certain aspects and operations of the abstract machine are described in
this document as implementation-defined (for example, `sizeof(int)`).
These constitute the parameters of the abstract machine. Each
implementation shall include documentation describing its
characteristics and behavior in these respects.[^6]

Such documentation shall define the instance of the abstract machine
that corresponds to that implementation (referred to as the
“corresponding instance” below).

Certain other aspects and operations of the abstract machine are
described in this document as unspecified (for example, order of
evaluation of arguments in a function call [[expr.call]]). Where
possible, this document defines a set of allowable behaviors. These
define the nondeterministic aspects of the abstract machine. An instance
of the abstract machine can thus have more than one possible execution
for a given program and a given input.

Certain other operations are described in this document as undefined
(for example, the effect of attempting to modify a const object).

[*Note 1*: This document imposes no requirements on the behavior of
programs that contain undefined behavior. — *end note*]

A conforming implementation executing a well-formed program shall
produce the same observable behavior as one of the possible executions
of the corresponding instance of the abstract machine with the same
program and the same input. However, if any such execution contains an
undefined operation, this document places no requirement on the
implementation executing that program with that input (not even with
regard to operations preceding the first undefined operation).

The least requirements on a conforming implementation are:

- Accesses through volatile glvalues are evaluated strictly according to
  the rules of the abstract machine.
- At program termination, all data written into files shall be identical
  to one of the possible results that execution of the program according
  to the abstract semantics would have produced.
- The input and output dynamics of interactive devices shall take place
  in such a fashion that prompting output is actually delivered before a
  program waits for input. What constitutes an interactive device is
  *implementation-defined*.

These collectively are referred to as the *observable behavior* of the
program.

[*Note 2*: More stringent correspondences between abstract and actual
semantics can be defined by each implementation. — *end note*]

## Structure of this document <a id="intro.structure">[[intro.structure]]</a>

[[lex]] through [[cpp]] describe the C++ programming language. That
description includes detailed syntactic specifications in a form
described in  [[syntax]]. For convenience, [[gram]] repeats all such
syntactic specifications.

[[support]] through [[thread]] and [[depr]] (the *library clauses*)
describe the C++ standard library. That description includes detailed
descriptions of the entities and macros that constitute the library, in
a form described in [[library]].

[[implimits]] recommends lower bounds on the capacity of conforming
implementations.

[[diff]] summarizes the evolution of C++ since its first published
description, and explains in detail the differences between C++ and C.
Certain features of C++ exist solely for compatibility purposes;
[[depr]] describes those features.

## Syntax notation <a id="syntax">[[syntax]]</a>

In the syntax notation used in this document, syntactic categories are
indicated by type, and literal words and characters in `constant`
`width` type. Alternatives are listed on separate lines except in a few
cases where a long set of alternatives is marked by the phrase “one of”.
If the text of an alternative is too long to fit on a line, the text is
continued on subsequent lines indented from the first one. An optional
terminal or non-terminal symbol is indicated by the subscript “ₒₚₜ”, so

``` bnf
\terminal{\ expressionₒₚₜ \terminal{\}}
```

indicates an optional expression enclosed in braces.

Names for syntactic categories have generally been chosen according to
the following rules:

-  is a use of an identifier in a context that determines its meaning
  (e.g., *class-name*, *typedef-name*).
-  is an identifier with no context-dependent meaning (e.g.,
  *qualified-id*).
-  is one or more ’s without intervening delimiters (e.g.,
  *declaration-seq* is a sequence of declarations).
-  is one or more ’s separated by intervening commas (e.g.,
  *identifier-list* is a sequence of identifiers separated by commas).

<!-- Section link definitions -->
[intro]: #intro
[intro.abstract]: #intro.abstract
[intro.compliance]: #intro.compliance
[intro.compliance.general]: #intro.compliance.general
[intro.defs]: #intro.defs
[intro.refs]: #intro.refs
[intro.scope]: #intro.scope
[intro.structure]: #intro.structure
[syntax]: #syntax

<!-- Link reference definitions -->
[algorithm.stable]: library.md#algorithm.stable
[basic.fundamental]: basic.md#basic.fundamental
[basic.link]: basic.md#basic.link
[class.access]: class.md#class.access
[class.copy.assign]: class.md#class.copy.assign
[class.ctor]: class.md#class.ctor
[class.derived]: class.md#class.derived
[compliance]: library.md#compliance
[conv.lval]: expr.md#conv.lval
[cpp]: cpp.md#cpp
[cpp.error]: cpp.md#cpp.error
[dcl.pre]: dcl.md#dcl.pre
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[defns.repositional.stream]: #defns.repositional.stream
[defns.well.formed]: #defns.well.formed
[depr]: #depr
[diff]: #diff
[diff.library]: compatibility.md#diff.library
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.post.incr]: expr.md#expr.post.incr
[expr.pre.incr]: expr.md#expr.pre.incr
[gram]: #gram
[implimits]: #implimits
[input.output]: input.md#input.output
[intro]: #intro
[intro.abstract]: #intro.abstract
[intro.compliance]: #intro.compliance
[intro.compliance.general]: #intro.compliance.general
[intro.defs]: #intro.defs
[intro.execution]: basic.md#intro.execution
[lex]: lex.md#lex
[lex.phases]: lex.md#lex.phases
[library]: library.md#library
[localization]: localization.md#localization
[re]: re.md#re
[strings]: strings.md#strings
[support]: support.md#support
[syntax]: #syntax
[temp.deduct]: temp.md#temp.deduct
[thread]: thread.md#thread
[using.headers]: library.md#using.headers

[^1]: POSIX is a registered trademark of the Institute of Electrical and
    Electronic Engineers, Inc. This information is given for the
    convenience of users of this document and does not constitute an
    endorsement by ISO or IEC of this product.

[^2]: With the qualifications noted in [[support]] through [[thread]]
    and in [[diff.library]], the C standard library is a subset of the
    C++ standard library.

[^3]: “Correct execution” can include undefined behavior, depending on
    the data being processed; see [[intro.defs]] and 
    [[intro.execution]].

[^4]: This documentation also defines implementation-defined behavior;
    see  [[intro.abstract]].

[^5]: This provision is sometimes called the “as-if” rule, because an
    implementation is free to disregard any requirement of this document
    as long as the result is *as if* the requirement had been obeyed, as
    far as can be determined from the observable behavior of the
    program. For instance, an actual implementation need not evaluate
    part of an expression if it can deduce that its value is not used
    and that no side effects affecting the observable behavior of the
    program are produced.

[^6]: This documentation also includes conditionally-supported
    constructs and locale-specific behavior. See 
    [[intro.compliance.general]].
