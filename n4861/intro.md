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
amendments) applies.

- Ecma International, *ECMAScript Language Specification*, Standard
  Ecma-262, third edition, 1999.
- ISO/IEC 2382 (all parts), *Information technology — Vocabulary*
- ISO 8601:2004, *Data elements and interchange formats — Information
  interchange — Representation of dates and times*
- ISO/IEC 9899:2018, *Programming languages — C*
- ISO/IEC 9945:2003, *Information Technology — Portable Operating System
  Interface (POSIX)*
- ISO/IEC 10646, *Information technology — Universal Coded Character Set
  (UCS)*
- ISO/IEC 10646-1:1993, *Information technology — Universal
  Multiple-Octet Coded Character Set (UCS) — Part 1: Architecture and
  Basic Multilingual Plane*
- ISO/IEC/IEEE 60559:2011, *Information technology — Microprocessor
  Systems — Floating-Point arithmetic*
- ISO 80000-2:2009, *Quantities and units — Part 2: Mathematical signs
  and symbols to be used in the natural sciences and technology*
- The Unicode Consortium. Unicode Standard Annex, UAX \#29, *Unicode
  Text Segmentation* \[online\]. Edited by Mark Davis. Revision 35;
  issued for Unicode 12.0.0. 2019-02-15 \[viewed 2020-02-23\]. Available
  at <http://www.unicode.org/reports/tr29/tr29-35.html>

The library described in Clause 7 of ISO/IEC 9899:2018 is hereinafter
called the *C standard library*. [^1]

The operating system interface described in ISO/IEC 9945:2003 is
hereinafter called *POSIX*.

The ECMAScript Language Specification described in Standard Ecma-262 is
hereinafter called *ECMA-262*.

[*Note 1*: References to ISO/IEC 10646-1:1993 are used only to support
deprecated features [[depr.locale.stdcvt]]. — *end note*]

# Terms and definitions <a id="intro.defs">[[intro.defs]]</a>

For the purposes of this document, the terms and definitions given in
ISO/IEC 2382-1:1993, the terms, definitions, and symbols given in ISO
80000-2:2009, and the following apply.

ISO and IEC maintain terminological databases for use in standardization
at the following addresses:

- ISO Online browsing platform: available at <https://www.iso.org/obp>
- IEC Electropedia: available at <http://www.electropedia.org/>

[[definitions]] defines additional terms that are used only in
[[library]] through [[thread]] and [[depr]].

Terms that are used only in a small portion of this document are defined
where they are used and italicized where they are defined.

#### 1 access <a id="defns.access">[defns.access]</a>

⟨execution-time action⟩ read [[conv.lval]] or modify ([[expr.ass]],
[[expr.post.incr]], [[expr.pre.incr]]) the value of an object

[*Note 1 to entry*: Only objects of scalar type can be accessed.
Attempts to read or modify an object of class type typically invoke a
constructor [[class.ctor]] or assignment operator [[class.copy.assign]];
such invocations do not themselves constitute accesses, although they
may involve accesses of scalar subobjects. — *end note*]

#### 2 argument <a id="defns.argument">[defns.argument]</a>

⟨function call expression⟩ expression in the comma-separated list
bounded by the parentheses [[expr.call]]

#### 3 argument <a id="defns.argument.macro">[defns.argument.macro]</a>

⟨function-like macro⟩ sequence of preprocessing tokens in the
comma-separated list bounded by the parentheses [[cpp.replace]]

#### 4 argument <a id="defns.argument.throw">[defns.argument.throw]</a>

⟨throw expression⟩ operand of `throw` [[expr.throw]]

#### 5 argument <a id="defns.argument.templ">[defns.argument.templ]</a>

⟨template instantiation⟩ *constant-expression*, *type-id*, or
*id-expression* in the comma-separated list bounded by the angle
brackets [[temp.arg]]

#### 6 block <a id="defns.block">[defns.block]</a>

⟨execution⟩ wait for some condition (other than for the implementation
to execute the execution steps of the thread of execution) to be
satisfied before continuing execution past the blocking operation

#### 7 block <a id="defns.block.stmt">[defns.block.stmt]</a>

⟨statement⟩ compound statement [[stmt.block]]

#### 8 conditionally-supported <a id="defns.cond.supp">[defns.cond.supp]</a>

program construct that an implementation is not required to support

[*Note 1 to entry*: Each implementation documents all
conditionally-supported constructs that it does not
support. — *end note*]

#### 9 diagnostic message <a id="defns.diagnostic">[defns.diagnostic]</a>

message belonging to an *implementation-defined* subset of the
implementation’s output messages

#### 10 dynamic type <a id="defns.dynamic.type">[defns.dynamic.type]</a>

⟨glvalue⟩ type of the most derived object [[intro.object]] to which the
glvalue refers

[*Example 1*: If a pointer [[dcl.ptr]] `p` whose static type is
“pointer to class `B`” is pointing to an object of class `D`, derived
from `B` [[class.derived]], the dynamic type of the expression `*p` is
“`D`”. References [[dcl.ref]] are treated similarly. — *end example*]

#### 11 dynamic type <a id="defns.dynamic.type.prvalue">[defns.dynamic.type.prvalue]</a>

⟨prvalue⟩ static type of the prvalue expression

#### 12 ill-formed program <a id="defns.ill.formed">[defns.ill.formed]</a>

program that is not well-formed [[defns.well.formed]]

#### 13 implementation-defined behavior <a id="defns.impl.defined">[defns.impl.defined]</a>

behavior, for a well-formed program construct and correct data, that
depends on the implementation and that each implementation documents

#### 14 implementation limits <a id="defns.impl.limits">[defns.impl.limits]</a>

restrictions imposed upon programs by the implementation

#### 15 locale-specific behavior <a id="defns.locale.specific">[defns.locale.specific]</a>

behavior that depends on local conventions of nationality, culture, and
language that each implementation documents

#### 16 multibyte character <a id="defns.multibyte">[defns.multibyte]</a>

sequence of one or more bytes representing a member of the extended
character set of either the source or the execution environment

[*Note 1 to entry*: The extended character set is a superset of the
basic character set [[lex.charset]]. — *end note*]

#### 17 parameter <a id="defns.parameter">[defns.parameter]</a>

⟨function or catch clause⟩ object or reference declared as part of a
function declaration or definition or in the catch clause of an
exception handler that acquires a value on entry to the function or
handler

#### 18 parameter <a id="defns.parameter.macro">[defns.parameter.macro]</a>

⟨function-like macro⟩ identifier from the comma-separated list bounded
by the parentheses immediately following the macro name

#### 19 parameter <a id="defns.parameter.templ">[defns.parameter.templ]</a>

⟨template⟩ member of a *template-parameter-list*

#### 20 signature <a id="defns.signature">[defns.signature]</a>

⟨function⟩ name, parameter-type-list [[dcl.fct]], and enclosing
namespace (if any)

[*Note 1 to entry*: Signatures are used as a basis for name mangling
and linking. — *end note*]

#### 21 signature <a id="defns.signature.friend">[defns.signature.friend]</a>

⟨non-template friend function with trailing *requires-clause*⟩ name,
parameter-type-list [[dcl.fct]], enclosing class, and trailing
*requires-clause* [[dcl.decl]]

#### 22 signature <a id="defns.signature.templ">[defns.signature.templ]</a>

⟨function template⟩ name, parameter-type-list [[dcl.fct]], enclosing
namespace (if any), return type, *template-head*, and trailing
*requires-clause* [[dcl.decl]] (if any)

#### 23 signature <a id="defns.signature.templ.friend">[defns.signature.templ.friend]</a>

⟨friend function template with constraint involving enclosing template parameters⟩
name, parameter-type-list [[dcl.fct]], return type, enclosing class,
*template-head*, and trailing *requires-clause* [[dcl.decl]] (if any)

#### 24 signature <a id="defns.signature.spec">[defns.signature.spec]</a>

⟨function template specialization⟩ signature of the template of which it
is a specialization and its template arguments (whether explicitly
specified or deduced)

#### 25 signature <a id="defns.signature.member">[defns.signature.member]</a>

⟨class member function⟩ name, parameter-type-list [[dcl.fct]], class of
which the function is a member, cv-qualifiers (if any), *ref-qualifier*
(if any), and trailing *requires-clause* [[dcl.decl]] (if any)

#### 26 signature <a id="defns.signature.member.templ">[defns.signature.member.templ]</a>

⟨class member function template⟩ name, parameter-type-list [[dcl.fct]],
class of which the function is a member, cv-qualifiers (if any),
*ref-qualifier* (if any), return type (if any), *template-head*, and
trailing *requires-clause* [[dcl.decl]] (if any)

#### 27 signature <a id="defns.signature.member.spec">[defns.signature.member.spec]</a>

⟨class member function template specialization⟩ signature of the member
function template of which it is a specialization and its template
arguments (whether explicitly specified or deduced)

#### 28 static type <a id="defns.static.type">[defns.static.type]</a>

type of an expression [[basic.types]] resulting from analysis of the
program without considering execution semantics

[*Note 1 to entry*: The static type of an expression depends only on
the form of the program in which the expression appears, and does not
change while the program is executing. — *end note*]

#### 29 unblock <a id="defns.unblock">[defns.unblock]</a>

satisfy a condition that one or more blocked threads of execution are
waiting for

#### 30 undefined behavior <a id="defns.undefined">[defns.undefined]</a>

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
never exhibits behavior explicitly specified as undefined in [[intro]]
through [[cpp]] of this document [[expr.const]]. — *end note*]

#### 31 unspecified behavior <a id="defns.unspecified">[defns.unspecified]</a>

behavior, for a well-formed program construct and correct data, that
depends on the implementation

[*Note 1 to entry*: The implementation is not required to document
which behavior occurs. The range of possible behaviors is usually
delineated by this document. — *end note*]

#### 32 well-formed program <a id="defns.well.formed">[defns.well.formed]</a>

C++ program constructed according to the syntax rules, diagnosable
semantic rules, and the one-definition rule [[basic.def.odr]]

# General principles <a id="intro">[[intro]]</a>

## Implementation compliance <a id="intro.compliance">[[intro.compliance]]</a>

The set of *diagnosable rules* consists of all syntactic and semantic
rules in this document except for those rules containing an explicit
notation that “no diagnostic is required” or which are described as
resulting in “undefined behavior”.

Although this document states only requirements on C++ implementations,
those requirements are often easier to understand if they are phrased as
requirements on programs, parts of programs, or execution of programs.
Such requirements have the following meaning:

- If a program contains no violations of the rules in this document, a
  conforming implementation shall, within its resource limits, accept
  and correctly execute[^2] that program.
- If a program contains a violation of any diagnosable rule or an
  occurrence of a construct described in this document as
  “conditionally-supported” when the implementation does not support
  that construct, a conforming implementation shall issue at least one
  diagnostic message.
- If a program contains a violation of a rule for which no diagnostic is
  required, this document places no requirement on implementations with
  respect to that program.

[*Note 1*: During template argument deduction and substitution, certain
constructs that in other contexts require a diagnostic are treated
differently; see  [[temp.deduct]]. — *end note*]

For classes and class templates, the library Clauses specify partial
definitions. Private members [[class.access]] are not specified, but
each implementation shall supply them to complete the definitions
according to the description in the library Clauses.

For functions, function templates, objects, and values, the library
Clauses specify declarations. Implementations shall supply definitions
consistent with the descriptions in the library Clauses.

The names defined in the library have namespace scope
[[basic.namespace]]. A C++ translation unit [[lex.phases]] obtains
access to these names by including the appropriate standard library
header or importing the appropriate standard library named header unit
[[using.headers]].

The templates, classes, functions, and objects in the library have
external linkage [[basic.link]]. The implementation provides definitions
for standard library entities, as necessary, while combining translation
units to form a complete C++ program [[lex.phases]].

Two kinds of implementations are defined: a *hosted implementation* and
a *freestanding implementation*. For a hosted implementation, this
document defines the set of available libraries. A freestanding
implementation is one in which execution may take place without the
benefit of an operating system, and has an *implementation-defined* set
of libraries that includes certain language-support libraries
[[compliance]].

A conforming implementation may have extensions (including additional
library functions), provided they do not alter the behavior of any
well-formed program. Implementations are required to diagnose programs
that use such extensions that are ill-formed according to this document.
Having done so, however, they can compile and execute such programs.

Each implementation shall include documentation that identifies all
conditionally-supported constructs that it does not support and defines
all locale-specific characteristics.[^3]

### Abstract machine <a id="intro.abstract">[[intro.abstract]]</a>

The semantic descriptions in this document define a parameterized
nondeterministic abstract machine. This document places no requirement
on the structure of conforming implementations. In particular, they need
not copy or emulate the structure of the abstract machine. Rather,
conforming implementations are required to emulate (only) the observable
behavior of the abstract machine as explained below.[^4]

Certain aspects and operations of the abstract machine are described in
this document as implementation-defined (for example, `sizeof(int)`).
These constitute the parameters of the abstract machine. Each
implementation shall include documentation describing its
characteristics and behavior in these respects.[^5] Such documentation
shall define the instance of the abstract machine that corresponds to
that implementation (referred to as the “corresponding instance” below).

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
semantics may be defined by each implementation. — *end note*]

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

Throughout this document, each example is introduced by “” and
terminated by “”. Each note is introduced by “” or “” and terminated by
“”. Examples and notes may be nested.

## Syntax notation <a id="syntax">[[syntax]]</a>

In the syntax notation used in this document, syntactic categories are
indicated by type, and literal words and characters in `constant`
`width` type. Alternatives are listed on separate lines except in a few
cases where a long set of alternatives is marked by the phrase “one of”.
If the text of an alternative is too long to fit on a line, the text is
continued on subsequent lines indented from the first one. An optional
terminal or non-terminal symbol is indicated by the subscript “ₒₚₜ”, so

``` bnf
'{' expressionₒₚₜ '}'
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

## Acknowledgments <a id="intro.ack">[[intro.ack]]</a>

The C++ programming language as described in this document is based on
the language as described in Chapter R (Reference Manual) of Stroustrup:
*The C++ Programming Language* (second edition, Addison-Wesley
Publishing Company, ISBN 0-201-53992-6, copyright ©1991 AT&T). That, in
turn, is based on the C programming language as described in Appendix A
of Kernighan and Ritchie: *The C Programming Language* (Prentice-Hall,
1978, ISBN 0-13-110163-3, copyright ©1978 AT&T).

Portions of the library Clauses of this document are based on work by
P.J. Plauger, which was published as *The Draft Standard C++ Library*
(Prentice-Hall, ISBN 0-13-117003-1, copyright ©1995 P.J. Plauger).

POSIX® is a registered trademark of the Institute of Electrical and
Electronic Engineers, Inc.

ECMAScript® is a registered trademark of Ecma International.

Unicode® is a registered trademark of Unicode, Inc.

All rights in these originals are reserved.

<!-- Link reference definitions -->
[basic.def.odr]: basic.md#basic.def.odr
[basic.link]: basic.md#basic.link
[basic.namespace]: dcl.md#basic.namespace
[basic.types]: basic.md#basic.types
[class.access]: class.md#class.access
[class.copy.assign]: class.md#class.copy.assign
[class.ctor]: class.md#class.ctor
[class.derived]: class.md#class.derived
[compliance]: library.md#compliance
[conv.lval]: expr.md#conv.lval
[cpp]: cpp.md#cpp
[cpp.replace]: cpp.md#cpp.replace
[dcl.decl]: dcl.md#dcl.decl
[dcl.fct]: dcl.md#dcl.fct
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[definitions]: library.md#definitions
[defns.well.formed]: #defns.well.formed
[depr]: #depr
[depr.locale.stdcvt]: future.md#depr.locale.stdcvt
[diff]: #diff
[diff.library]: compatibility.md#diff.library
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.post.incr]: expr.md#expr.post.incr
[expr.pre.incr]: expr.md#expr.pre.incr
[expr.throw]: expr.md#expr.throw
[gram]: #gram
[implimits]: #implimits
[intro]: #intro
[intro.abstract]: #intro.abstract
[intro.ack]: #intro.ack
[intro.compliance]: #intro.compliance
[intro.defs]: #intro.defs
[intro.execution]: basic.md#intro.execution
[intro.object]: basic.md#intro.object
[intro.refs]: #intro.refs
[intro.scope]: #intro.scope
[intro.structure]: #intro.structure
[lex]: lex.md#lex
[lex.charset]: lex.md#lex.charset
[lex.phases]: lex.md#lex.phases
[library]: library.md#library
[stmt.block]: stmt.md#stmt.block
[support]: support.md#support
[syntax]: #syntax
[temp.arg]: temp.md#temp.arg
[temp.deduct]: temp.md#temp.deduct
[thread]: thread.md#thread
[using.headers]: library.md#using.headers

[^1]: With the qualifications noted in [[support]] through [[thread]]
    and in [[diff.library]], the C standard library is a subset of the
    C++ standard library.

[^2]: “Correct execution” can include undefined behavior, depending on
    the data being processed; see [[intro.defs]] and 
    [[intro.execution]].

[^3]: This documentation also defines implementation-defined behavior;
    see  [[intro.abstract]].

[^4]: This provision is sometimes called the “as-if” rule, because an
    implementation is free to disregard any requirement of this document
    as long as the result is *as if* the requirement had been obeyed, as
    far as can be determined from the observable behavior of the
    program. For instance, an actual implementation need not evaluate
    part of an expression if it can deduce that its value is not used
    and that no side effects affecting the observable behavior of the
    program are produced.

[^5]: This documentation also includes conditionally-supported
    constructs and locale-specific behavior. See  [[intro.compliance]].
