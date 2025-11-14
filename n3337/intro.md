# General <a id="intro">[[intro]]</a>

## Scope <a id="intro.scope">[[intro.scope]]</a>

This International Standard specifies requirements for implementations
of the C++programming language. The first such requirement is that they
implement the language, and so this International Standard also defines
C++. Other requirements and relaxations of the first requirement appear
at various places within this International Standard.

C++is a general purpose programming language based on the C programming
language as described in ISO/IEC 9899:1999 *Programming languages — C*
(hereinafter referred to as the *C standard*). In addition to the
facilities provided by C, C++provides additional data types, classes,
templates, exceptions, namespaces, operator overloading, function name
overloading, references, free store management operators, and additional
library facilities.

## Normative references <a id="intro.refs">[[intro.refs]]</a>

The following referenced documents are indispensable for the application
of this document. For dated references, only the edition cited applies.
For undated references, the latest edition of the referenced document
(including any amendments) applies.

- Ecma International, *ECMAScript Language Specification*, Standard
  Ecma-262, third edition, 1999.
- ISO/IEC 2382 (all parts), *Information technology — Vocabulary*
- ISO/IEC 9899:1999, *Programming languages — C*
- ISO/IEC 9899:1999/Cor.1:2001(E), *Programming languages — C, Technical
  Corrigendum 1*
- ISO/IEC 9899:1999/Cor.2:2004(E), *Programming languages — C, Technical
  Corrigendum 2*
- ISO/IEC 9899:1999/Cor.3:2007(E), *Programming languages — C, Technical
  Corrigendum 3*
- ISO/IEC 9945:2003, *Information Technology — Portable Operating System
  Interface (POSIX)*
- ISO/IEC 10646-1:1993, *Information technology — Universal
  Multiple-Octet Coded Character Set (UCS) — Part 1: Architecture and
  Basic Multilingual Plane*
- ISO/IEC TR 19769:2004, *Information technology — Programming
  languages, their environments and system software interfaces —
  Extensions for the programming language C to support new character
  data types*

The library described in Clause 7 of ISO/IEC 9899:1999 and Clause 7 of
ISO/IEC 9899:1999/Cor.1:2001 and Clause 7 of ISO/IEC
9899:1999/Cor.2:2003 is hereinafter called the *C standard library*.[^1]

The library described in ISO/IEC TR 19769:2004 is hereinafter called the
*C Unicode TR*.

The operating system interface described in ISO/IEC 9945:2003 is
hereinafter called *POSIX*.

The ECMAScript Language Specification described in Standard Ecma-262 is
hereinafter called *ECMA-262*.

## Terms and definitions <a id="intro.defs">[[intro.defs]]</a>

For the purposes of this document, the following definitions apply.

[[definitions]] defines additional terms that are used only in Clauses 
[[library]] through  [[thread]] and Annex  [[depr]].

Terms that are used only in a small portion of this International
Standard are defined where they are used and italicized where they are
defined.

#### 1 argument <a id="defns.argument">[defns.argument]</a>

actual argument  
actual parameter  
\<function call expression\> expression in the comma-separated list
bounded by the parentheses

#### 2 argument <a id="defns.argument.macro">[defns.argument.macro]</a>

actual argument  
actual parameter  
\<function-like macro\> sequence of preprocessing tokens in the
comma-separated list bounded by the parentheses

#### 3 argument <a id="defns.argument.throw">[defns.argument.throw]</a>

actual argument  
actual parameter  
\<throw expression\> the operand of `throw`

#### 4 argument <a id="defns.argument.templ">[defns.argument.templ]</a>

actual argument  
actual parameter  
\<template instantiation\> expression, *type-id* or *template-name* in
the comma-separated list bounded by the angle brackets

#### 5 conditionally-supported <a id="defns.cond.supp">[defns.cond.supp]</a>

program construct that an implementation is not required to support  
Each implementation documents all conditionally-supported constructs
that it does not support.

#### 6 diagnostic message <a id="defns.diagnostic">[defns.diagnostic]</a>

message belonging to an *implementation-defined* subset of the
implementation’s output messages

#### 7 dynamic type <a id="defns.dynamic.type">[defns.dynamic.type]</a>

\<glvalue\> type of the most derived object ([[intro.object]]) to which
the glvalue denoted by a glvalue expression refers  
if a pointer ([[dcl.ptr]]) `p` whose static type is “pointer to class
`B`” is pointing to an object of class `D`, derived from `B` (Clause 
[[class.derived]]), the dynamic type of the expression `*p` is “`D`.”
References ([[dcl.ref]]) are treated similarly.

#### 8 dynamic type <a id="defns.dynamic.type.prvalue">[defns.dynamic.type.prvalue]</a>

\<prvalue\> static type of the prvalue expression

#### 9 ill-formed program <a id="defns.ill.formed">[defns.ill.formed]</a>

program that is not well formed

#### 10 implementation-defined behavior <a id="defns.impl.defined">[defns.impl.defined]</a>

behavior, for a well-formed program construct and correct data, that
depends on the implementation and that each implementation documents

#### 11 implementation limits <a id="defns.impl.limits">[defns.impl.limits]</a>

restrictions imposed upon programs by the implementation

#### 12 locale-specific behavior <a id="defns.locale.specific">[defns.locale.specific]</a>

behavior that depends on local conventions of nationality, culture, and
language that each implementation documents

#### 13 multibyte character <a id="defns.multibyte">[defns.multibyte]</a>

sequence of one or more bytes representing a member of the extended
character set of either the source or the execution environment  
The extended character set is a superset of the basic character set (
[[lex.charset]]).

#### 14 parameter <a id="defns.parameter">[defns.parameter]</a>

formal argument  
formal parameter  
\<function or catch clause\> object or reference declared as part of a
function declaration or definition or in the catch clause of an
exception handler that acquires a value on entry to the function or
handler

#### 15 parameter <a id="defns.parameter.macro">[defns.parameter.macro]</a>

formal argument  
formal parameter  
\<function-like macro\> identifier from the comma-separated list bounded
by the parentheses immediately following the macro name

#### 16 parameter <a id="defns.parameter.templ">[defns.parameter.templ]</a>

formal argument  
formal parameter  
\<template\> *template-parameter*

#### 17 signature <a id="defns.signature">[defns.signature]</a>

\<function\> name, parameter type list ([[dcl.fct]]), and enclosing
namespace (if any)  
Signatures are used as a basis for name mangling and linking.

#### 18 signature <a id="defns.signature.templ">[defns.signature.templ]</a>

\<function template\> name, parameter type list ([[dcl.fct]]),
enclosing namespace (if any), return type, and template parameter list

#### 19 signature <a id="defns.signature.spec">[defns.signature.spec]</a>

\<function template specialization\> signature of the template of which
it is a specialization and its template arguments (whether explicitly
specified or deduced)

#### 20 signature <a id="defns.signature.member">[defns.signature.member]</a>

\<class member function\> name, parameter type list ([[dcl.fct]]),
class of which the function is a member, cv-qualifiers (if any), and
*ref-qualifier* (if any)

#### 21 signature <a id="defns.signature.member.templ">[defns.signature.member.templ]</a>

\<class member function template\> name, parameter type list (
[[dcl.fct]]), class of which the function is a member, cv-qualifiers (if
any), *ref-qualifier* (if any), return type, and template parameter list

#### 22 signature <a id="defns.signature.member.spec">[defns.signature.member.spec]</a>

\<class member function template specialization\> signature of the
member function template of which it is a specialization and its
template arguments (whether explicitly specified or deduced)

#### 23 static type <a id="defns.static.type">[defns.static.type]</a>

type of an expression ([[basic.types]]) resulting from analysis of the
program without considering execution semantics  
The static type of an expression depends only on the form of the program
in which the expression appears, and does not change while the program
is executing.

#### 24 undefined behavior <a id="defns.undefined">[defns.undefined]</a>

behavior for which this International Standard imposes no requirements  
Undefined behavior may be expected when this International Standard
omits any explicit definition of behavior or when a program uses an
erroneous construct or erroneous data. Permissible undefined behavior
ranges from ignoring the situation completely with unpredictable
results, to behaving during translation or program execution in a
documented manner characteristic of the environment (with or without the
issuance of a diagnostic message), to terminating a translation or
execution (with the issuance of a diagnostic message). Many erroneous
program constructs do not engender undefined behavior; they are required
to be diagnosed.

#### 25 unspecified behavior <a id="defns.unspecified">[defns.unspecified]</a>

behavior, for a well-formed program construct and correct data, that
depends on the implementation  
The implementation is not required to document which behavior occurs.
The range of possible behaviors is usually delineated by this
International Standard.

#### 26 well-formed program <a id="defns.well.formed">[defns.well.formed]</a>

C++program constructed according to the syntax rules, diagnosable
semantic rules, and the One Definition Rule ([[basic.def.odr]]).

## Implementation compliance <a id="intro.compliance">[[intro.compliance]]</a>

The set of *diagnosable rules* consists of all syntactic and semantic
rules in this International Standard except for those rules containing
an explicit notation that “no diagnostic is required” or which are
described as resulting in “undefined behavior.”

Although this International Standard states only requirements on C++
implementations, those requirements are often easier to understand if
they are phrased as requirements on programs, parts of programs, or
execution of programs. Such requirements have the following meaning:

- If a program contains no violations of the rules in this International
  Standard, a conforming implementation shall, within its resource
  limits, accept and correctly execute[^2] that program.
- If a program contains a violation of any diagnosable rule or an
  occurrence of a construct described in this Standard as
  “conditionally-supported” when the implementation does not support
  that construct, a conforming implementation shall issue at least one
  diagnostic message.
- If a program contains a violation of a rule for which no diagnostic is
  required, this International Standard places no requirement on
  implementations with respect to that program.

For classes and class templates, the library Clauses specify partial
definitions. Private members (Clause  [[class.access]]) are not
specified, but each implementation shall supply them to complete the
definitions according to the description in the library Clauses.

For functions, function templates, objects, and values, the library
Clauses specify declarations. Implementations shall supply definitions
consistent with the descriptions in the library Clauses.

The names defined in the library have namespace scope (
[[basic.namespace]]). A C++translation unit ([[lex.phases]]) obtains
access to these names by including the appropriate standard library
header ([[cpp.include]]).

The templates, classes, functions, and objects in the library have
external linkage ([[basic.link]]). The implementation provides
definitions for standard library entities, as necessary, while combining
translation units to form a complete C++program ([[lex.phases]]).

Two kinds of implementations are defined: a *hosted implementation* and
a *freestanding implementation*. For a hosted implementation, this
International Standard defines the set of available libraries. A
freestanding implementation is one in which execution may take place
without the benefit of an operating system, and has an
*implementation-defined* set of libraries that includes certain
language-support libraries ([[compliance]]).

A conforming implementation may have extensions (including additional
library functions), provided they do not alter the behavior of any
well-formed program. Implementations are required to diagnose programs
that use such extensions that are ill-formed according to this
International Standard. Having done so, however, they can compile and
execute such programs.

Each implementation shall include documentation that identifies all
conditionally-supported constructs that it does not support and defines
all locale-specific characteristics.[^3]

## Structure of this International Standard <a id="intro.structure">[[intro.structure]]</a>

Clauses  [[lex]] through  [[cpp]] describe the C++programming language.
That description includes detailed syntactic specifications in a form
described in  [[syntax]]. For convenience, Annex  [[gram]] repeats all
such syntactic specifications.

Clauses  [[support]] through  [[thread]] and Annex  [[depr]] (the
*library clauses*) describe the Standard C++library. That description
includes detailed descriptions of the templates, classes, functions,
constants, and macros that constitute the library, in a form described
in Clause  [[library]].

Annex  [[implimits]] recommends lower bounds on the capacity of
conforming implementations.

Annex  [[diff]] summarizes the evolution of C++since its first published
description, and explains in detail the differences between C++and C.
Certain features of C++exist solely for compatibility purposes; Annex 
[[depr]] describes those features.

Throughout this International Standard, each example is introduced by “”
and terminated by “”. Each note is introduced by “” and terminated by
“”. Examples and notes may be nested.

## Syntax notation <a id="syntax">[[syntax]]</a>

In the syntax notation used in this International Standard, syntactic
categories are indicated by *italic* type, and literal words and
characters in `constant` `width` type. Alternatives are listed on
separate lines except in a few cases where a long set of alternatives is
marked by the phrase “one of.” If the text of an alternative is too long
to fit on a line, the text is continued on subsequent lines indented
from the first one. An optional terminal or non-terminal symbol is
indicated by the subscript “’ₒₚₜ’, so

``` bnf
\terminal{\ expression\terminal ₒₚₜ{\}}
```

indicates an optional expression enclosed in braces.

Names for syntactic categories have generally been chosen according to
the following rules:

- *X-name* is a use of an identifier in a context that determines its
  meaning (e.g., *class-name*, *typedef-name*).
- *X-id* is an identifier with no context-dependent meaning (e.g.,
  *qualified-id*).
- *X-seq* is one or more *X*’s without intervening delimiters (e.g.,
  *declaration-seq* is a sequence of declarations).
- *X-list* is one or more *X*’s separated by intervening commas (e.g.,
  *expression-list* is a sequence of expressions separated by commas).

## The C++memory model <a id="intro.memory">[[intro.memory]]</a>

The fundamental storage unit in the C++memory model is the *byte*. A
byte is at least large enough to contain any member of the basic
execution character set ([[lex.charset]]) and the eight-bit code units
of the Unicode UTF-8 encoding form and is composed of a contiguous
sequence of bits, the number of which is *implementation-defined*. The
least significant bit is called the *low-order bit*; the most
significant bit is called the *high-order bit*. The memory available to
a C++program consists of one or more sequences of contiguous bytes.
Every byte has a unique address.

The representation of types is described in  [[basic.types]].

A *memory location* is either an object of scalar type or a maximal
sequence of adjacent bit-fields all having non-zero width. Various
features of the language, such as references and virtual functions,
might involve additional memory locations that are not accessible to
programs but are managed by the implementation. Two or more threads of
execution ([[intro.multithread]]) can update and access separate memory
locations without interfering with each other.

Thus a bit-field and an adjacent non-bit-field are in separate memory
locations, and therefore can be concurrently updated by two threads of
execution without interference. The same applies to two bit-fields, if
one is declared inside a nested struct declaration and the other is not,
or if the two are separated by a zero-length bit-field declaration, or
if they are separated by a non-bit-field declaration. It is not safe to
concurrently update two bit-fields in the same struct if all fields
between them are also bit-fields of non-zero width.

A structure declared as

``` cpp
struct {
  char a;
  int b:5,
  c:11,
  :0,
  d:8;
  struct {int ee:8;} e;
}
```

contains four separate memory locations: The field `a` and bit-fields
`d` and `e.ee` are each separate memory locations, and can be modified
concurrently without interfering with each other. The bit-fields `b` and
`c` together constitute the fourth memory location. The bit-fields `b`
and `c` cannot be concurrently modified, but `b` and `a`, for example,
can be.

## The C++object model <a id="intro.object">[[intro.object]]</a>

The constructs in a C++program create, destroy, refer to, access, and
manipulate objects. An *object* is a region of storage. A function is
not an object, regardless of whether or not it occupies storage in the
way that objects do. An object is created by a *definition* (
[[basic.def]]), by a *new-expression* ([[expr.new]]) or by the
implementation ([[class.temporary]]) when needed. The properties of an
object are determined when the object is created. An object can have a
*name* (Clause  [[basic]]). An object has a *storage duration* (
[[basic.stc]]) which influences its *lifetime* ([[basic.life]]). An
object has a *type* ([[basic.types]]). The term *object type* refers to
the type with which the object is created. Some objects are
*polymorphic* ([[class.virtual]]); the implementation generates
information associated with each such object that makes it possible to
determine that object’s type during program execution. For other
objects, the interpretation of the values found therein is determined by
the type of the *expression*s (Clause  [[expr]]) used to access them.

Objects can contain other objects, called *subobjects*. A subobject can
be a *member subobject* ([[class.mem]]), a *base class subobject*
(Clause  [[class.derived]]), or an array element. An object that is not
a subobject of any other object is called a *complete object*.

For every object `x`, there is some object called the *complete object
of* `x`, determined as follows:

- If `x` is a complete object, then `x` is the complete object of `x`.
- Otherwise, the complete object of `x` is the complete object of the
  (unique) object that contains `x`.

If a complete object, a data member ([[class.mem]]), or an array
element is of class type, its type is considered the *most derived
class*, to distinguish it from the class type of any base class
subobject; an object of a most derived class type or of a non-class type
is called a *most derived object*.

Unless it is a bit-field ([[class.bit]]), a most derived object shall
have a non-zero size and shall occupy one or more bytes of storage. Base
class subobjects may have zero size. An object of trivially copyable or
standard-layout type ([[basic.types]]) shall occupy contiguous bytes of
storage.

Unless an object is a bit-field or a base class subobject of zero size,
the address of that object is the address of the first byte it occupies.
Two objects that are not bit-fields may have the same address if one is
a subobject of the other, or if at least one is a base class subobject
of zero size and they are of different types; otherwise, they shall have
distinct addresses.[^4]

``` cpp
static const char test1 = 'x';
static const char test2 = 'x';
const bool b = &test1 != &test2;      // always true
```

C++provides a variety of fundamental types and several ways of composing
new types from existing types ([[basic.types]]).

## Program execution <a id="intro.execution">[[intro.execution]]</a>

The semantic descriptions in this International Standard define a
parameterized nondeterministic abstract machine. This International
Standard places no requirement on the structure of conforming
implementations. In particular, they need not copy or emulate the
structure of the abstract machine. Rather, conforming implementations
are required to emulate (only) the observable behavior of the abstract
machine as explained below.[^5]

Certain aspects and operations of the abstract machine are described in
this International Standard as implementation-defined (for example,
`sizeof(int)`). These constitute the parameters of the abstract machine.
Each implementation shall include documentation describing its
characteristics and behavior in these respects.[^6] Such documentation
shall define the instance of the abstract machine that corresponds to
that implementation (referred to as the “corresponding instance” below).

Certain other aspects and operations of the abstract machine are
described in this International Standard as unspecified (for example,
order of evaluation of arguments to a function). Where possible, this
International Standard defines a set of allowable behaviors. These
define the nondeterministic aspects of the abstract machine. An instance
of the abstract machine can thus have more than one possible execution
for a given program and a given input.

Certain other operations are described in this International Standard as
undefined (for example, the effect of attempting to modify a `const`
object). This International Standard imposes no requirements on the
behavior of programs that contain undefined behavior.

A conforming implementation executing a well-formed program shall
produce the same observable behavior as one of the possible executions
of the corresponding instance of the abstract machine with the same
program and the same input. However, if any such execution contains an
undefined operation, this International Standard places no requirement
on the implementation executing that program with that input (not even
with regard to operations preceding the first undefined operation).

When the processing of the abstract machine is interrupted by receipt of
a signal, the values of objects which are neither

- of type `volatile std::sig_atomic_t` nor
- lock-free atomic objects ([[atomics.lockfree]])

are unspecified during the execution of the signal handler, and the
value of any object not in either of these two categories that is
modified by the handler becomes undefined.

An instance of each object with automatic storage duration (
[[basic.stc.auto]]) is associated with each entry into its block. Such
an object exists and retains its last-stored value during the execution
of the block and while the block is suspended (by a call of a function
or receipt of a signal).

The least requirements on a conforming implementation are:

- Access to volatile objects are evaluated strictly according to the
  rules of the abstract machine.
- At program termination, all data written into files shall be identical
  to one of the possible results that execution of the program according
  to the abstract semantics would have produced.
- The input and output dynamics of interactive devices shall take place
  in such a fashion that prompting output is actually delivered before a
  program waits for input. What constitutes an interactive device is
  *implementation-defined*.

These collectively are referred to as the *observable behavior* of the
program. More stringent correspondences between abstract and actual
semantics may be defined by each implementation.

Operators can be regrouped according to the usual mathematical rules
only where the operators really are associative or commutative.[^7] For
example, in the following fragment

``` cpp
int a, b;
/*...*/
a = a + 32760 + b + 5;
```

the expression statement behaves exactly the same as

``` cpp
a = (((a + 32760) + b) + 5);
```

due to the associativity and precedence of these operators. Thus, the
result of the sum `(a + 32760)` is next added to `b`, and that result is
then added to 5 which results in the value assigned to `a`. On a machine
in which overflows produce an exception and in which the range of values
representable by an `int` is \[`-32768`, `+32767`\], the implementation
cannot rewrite this expression as

``` cpp
a = ((a + b) + 32765);
```

since if the values for `a` and `b` were, respectively, -32754 and -15,
the sum `a + b` would produce an exception while the original expression
would not; nor can the expression be rewritten either as

``` cpp
a = ((a + 32765) + b);
```

or

``` cpp
a = (a + (b + 32765));
```

since the values for `a` and `b` might have been, respectively, 4 and -8
or -17 and 12. However on a machine in which overflows do not produce an
exception and in which the results of overflows are reversible, the
above expression statement can be rewritten by the implementation in any
of the above ways because the same result will occur.

A *full-expression* is an expression that is not a subexpression of
another expression. If a language construct is defined to produce an
implicit call of a function, a use of the language construct is
considered to be an expression for the purposes of this definition. A
call to a destructor generated at the end of the lifetime of an object
other than a temporary object is an implicit full-expression.
Conversions applied to the result of an expression in order to satisfy
the requirements of the language construct in which the expression
appears are also considered to be part of the full-expression.

``` cpp
struct S {
  S(int i): I(i) { }
  int& v() { return I; }
private:
  int I;
};

 S s1(1);           // full-expression is call of S::S(int)
 S s2 = 2;          // full-expression is call of S::S(int)

void f() {
  if (S(3).v())     // full-expression includes lvalue-to-rvalue and
                    // int to bool conversions, performed before
                    // temporary is deleted at end of full-expression
  { }
}
```

The evaluation of a full-expression can include the evaluation of
subexpressions that are not lexically part of the full-expression. For
example, subexpressions involved in evaluating default arguments (
[[dcl.fct.default]]) are considered to be created in the expression that
calls the function, not the expression that defines the default
argument.

Accessing an object designated by a `volatile` glvalue (
[[basic.lval]]), modifying an object, calling a library I/O function, or
calling a function that does any of those operations are all *side
effects*, which are changes in the state of the execution environment.
*Evaluation* of an expression (or a sub-expression) in general includes
both value computations (including determining the identity of an object
for glvalue evaluation and fetching a value previously assigned to an
object for prvalue evaluation) and initiation of side effects. When a
call to a library I/O function returns or an access to a `volatile`
object is evaluated the side effect is considered complete, even though
some external actions implied by the call (such as the I/O itself) or by
the `volatile` access may not have completed yet.

*Sequenced before* is an asymmetric, transitive, pair-wise relation
between evaluations executed by a single thread (
[[intro.multithread]]), which induces a partial order among those
evaluations. Given any two evaluations *A* and *B*, if *A* is sequenced
before *B*, then the execution of *A* shall precede the execution of
*B*. If *A* is not sequenced before *B* and *B* is not sequenced before
*A*, then *A* and *B* are *unsequenced*. The execution of unsequenced
evaluations can overlap. Evaluations *A* and *B* are *indeterminately
sequenced* when either *A* is sequenced before *B* or *B* is sequenced
before *A*, but it is unspecified which. Indeterminately sequenced
evaluations cannot overlap, but either could be executed first.

Every value computation and side effect associated with a
full-expression is sequenced before every value computation and side
effect associated with the next full-expression to be evaluated.[^8].

Except where noted, evaluations of operands of individual operators and
of subexpressions of individual expressions are unsequenced. In an
expression that is evaluated more than once during the execution of a
program, unsequenced and indeterminately sequenced evaluations of its
subexpressions need not be performed consistently in different
evaluations. The value computations of the operands of an operator are
sequenced before the value computation of the result of the operator. If
a side effect on a scalar object is unsequenced relative to either
another side effect on the same scalar object or a value computation
using the value of the same scalar object, the behavior is undefined.

``` cpp
void f(int, int);
void g(int i, int* v) {
  i = v[i++];         // the behavior is undefined
  i = 7, i++, i++;    // i becomes 9

  i = i++ + 1;        // the behavior is undefined
  i = i + 1;          // the value of i is incremented

  f(i = -1, i = -1);  // the behavior is undefined
}
```

When calling a function (whether or not the function is inline), every
value computation and side effect associated with any argument
expression, or with the postfix expression designating the called
function, is sequenced before execution of every expression or statement
in the body of the called function. Value computations and side effects
associated with different argument expressions are unsequenced. Every
evaluation in the calling function (including other function calls) that
is not otherwise specifically sequenced before or after the execution of
the body of the called function is indeterminately sequenced with
respect to the execution of the called function.[^9] Several contexts in
C++cause evaluation of a function call, even though no corresponding
function call syntax appears in the translation unit. Evaluation of a
`new` expression invokes one or more allocation and constructor
functions; see  [[expr.new]]. For another example, invocation of a
conversion function ([[class.conv.fct]]) can arise in contexts in which
no function call syntax appears. The sequencing constraints on the
execution of the called function (as described above) are features of
the function calls as evaluated, whatever the syntax of the expression
that calls the function might be.

## Multi-threaded executions and data races <a id="intro.multithread">[[intro.multithread]]</a>

A *thread of execution* (also known as a *thread*) is a single flow of
control within a program, including the initial invocation of a specific
top-level function, and recursively including every function invocation
subsequently executed by the thread. When one thread creates another,
the initial call to the top-level function of the new thread is executed
by the new thread, not by the creating thread. Every thread in a program
can potentially access every object and function in a program.[^10]
Under a hosted implementation, a C++program can have more than one
thread running concurrently. The execution of each thread proceeds as
defined by the remainder of this standard. The execution of the entire
program consists of an execution of all of its threads. Usually the
execution can be viewed as an interleaving of all its threads. However,
some kinds of atomic operations, for example, allow executions
inconsistent with a simple interleaving, as described below. Under a
freestanding implementation, it is *implementation-defined* whether a
program can have more than one thread of execution.

Implementations should ensure that all unblocked threads eventually make
progress. Standard library functions may silently block on I/O or locks.
Factors in the execution environment, including externally-imposed
thread priorities, may prevent an implementation from making certain
guarantees of forward progress.

The value of an object visible to a thread *T* at a particular point is
the initial value of the object, a value assigned to the object by *T*,
or a value assigned to the object by another thread, according to the
rules below. In some cases, there may instead be undefined behavior.
Much of this section is motivated by the desire to support atomic
operations with explicit and detailed visibility constraints. However,
it also implicitly supports a simpler view for more restricted programs.

Two expression evaluations *conflict* if one of them modifies a memory
location ([[intro.memory]]) and the other one accesses or modifies the
same memory location.

The library defines a number of atomic operations (Clause  [[atomics]])
and operations on mutexes (Clause  [[thread]]) that are specially
identified as synchronization operations. These operations play a
special role in making assignments in one thread visible to another. A
synchronization operation on one or more memory locations is either a
consume operation, an acquire operation, a release operation, or both an
acquire and release operation. A synchronization operation without an
associated memory location is a fence and can be either an acquire
fence, a release fence, or both an acquire and release fence. In
addition, there are relaxed atomic operations, which are not
synchronization operations, and atomic read-modify-write operations,
which have special characteristics. For example, a call that acquires a
mutex will perform an acquire operation on the locations comprising the
mutex. Correspondingly, a call that releases the same mutex will perform
a release operation on those same locations. Informally, performing a
release operation on *A* forces prior side effects on other memory
locations to become visible to other threads that later perform a
consume or an acquire operation on *A*. “Relaxed” atomic operations are
not synchronization operations even though, like synchronization
operations, they cannot contribute to data races.

All modifications to a particular atomic object *M* occur in some
particular total order, called the *modification order* of *M*. If *A*
and *B* are modifications of an atomic object *M* and *A* happens before
(as defined below) *B*, then *A* shall precede *B* in the modification
order of *M*, which is defined below. This states that the modification
orders must respect the “happens before” relationship. There is a
separate order for each atomic object. There is no requirement that
these can be combined into a single total order for all objects. In
general this will be impossible since different threads may observe
modifications to different objects in inconsistent orders.

A *release sequence* headed by a release operation *A* on an atomic
object *M* is a maximal contiguous sub-sequence of side effects in the
modification order of *M*, where the first operation is `A`, and every
subsequent operation

- is performed by the same thread that performed `A`, or
- is an atomic read-modify-write operation.

Certain library calls *synchronize with* other library calls performed
by another thread. For example, an atomic store-release synchronizes
with a load-acquire that takes its value from the store (
[[atomics.order]]). Except in the specified cases, reading a later value
does not necessarily ensure visibility as described below. Such a
requirement would sometimes interfere with efficient implementation. The
specifications of the synchronization operations define when one reads
the value written by another. For atomic objects, the definition is
clear. All operations on a given mutex occur in a single total order.
Each mutex acquisition “reads the value written” by the last mutex
release.

An evaluation *A* *carries a dependency* to an evaluation *B* if

- the value of *A* is used as an operand of *B*, unless:
  - *B* is an invocation of any specialization of
    `std::kill_dependency` ([[atomics.order]]), or
  - *A* is the left operand of a built-in logical AND (`&&`, see 
    [[expr.log.and]]) or logical OR (`||`, see  [[expr.log.or]])
    operator, or
  - *A* is the left operand of a conditional (`?:`, see  [[expr.cond]])
    operator, or
  - *A* is the left operand of the built-in comma (`,`) operator (
    [[expr.comma]]);

  or
- *A* writes a scalar object or bit-field *M*, *B* reads the value
  written by *A* from *M*, and *A* is sequenced before *B*, or
- for some evaluation *X*, *A* carries a dependency to *X*, and *X*
  carries a dependency to *B*.

“Carries a dependency to” is a subset of “is sequenced before”, and is
similarly strictly intra-thread.

An evaluation *A* is *dependency-ordered before* an evaluation *B* if

- *A* performs a release operation on an atomic object *M*, and, in
  another thread, *B* performs a consume operation on *M* and reads a
  value written by any side effect in the release sequence headed by
  *A*, or
- for some evaluation *X*, *A* is dependency-ordered before *X* and *X*
  carries a dependency to *B*.

The relation “is dependency-ordered before” is analogous to
“synchronizes with”, but uses release/consume in place of
release/acquire.

An evaluation *A* *inter-thread happens before* an evaluation *B* if

- *A* synchronizes with *B*, or
- *A* is dependency-ordered before *B*, or
- for some evaluation *X*
  - *A* synchronizes with *X* and *X* is sequenced before *B*, or
  - *A* is sequenced before *X* and *X* inter-thread happens before *B*,
    or
  - *A* inter-thread happens before *X* and *X* inter-thread happens
    before *B*.

The “inter-thread happens before” relation describes arbitrary
concatenations of “sequenced before”, “synchronizes with” and
“dependency-ordered before” relationships, with two exceptions. The
first exception is that a concatenation is not permitted to end with
“dependency-ordered before” followed by “sequenced before”. The reason
for this limitation is that a consume operation participating in a
“dependency-ordered before” relationship provides ordering only with
respect to operations to which this consume operation actually carries a
dependency. The reason that this limitation applies only to the end of
such a concatenation is that any subsequent release operation will
provide the required ordering for a prior consume operation. The second
exception is that a concatenation is not permitted to consist entirely
of “sequenced before”. The reasons for this limitation are (1) to permit
“inter-thread happens before” to be transitively closed and (2) the
“happens before” relation, defined below, provides for relationships
consisting entirely of “sequenced before”.

An evaluation *A* *happens before* an evaluation *B* if:

- *A* is sequenced before *B*, or
- *A* inter-thread happens before *B*.

The implementation shall ensure that no program execution demonstrates a
cycle in the “happens before” relation. This cycle would otherwise be
possible only through the use of consume operations.

A *visible side effect* *A* on a scalar object or bit-field *M* with
respect to a value computation *B* of *M* satisfies the conditions:

- *A* happens before *B* and
- there is no other side effect *X* to *M* such that *A* happens before
  *X* and *X* happens before *B*.

The value of a non-atomic scalar object or bit-field *M*, as determined
by evaluation *B*, shall be the value stored by the visible side effect
*A*. If there is ambiguity about which side effect to a non-atomic
object or bit-field is visible, then the behavior is either unspecified
or undefined. This states that operations on ordinary objects are not
visibly reordered. This is not actually detectable without data races,
but it is necessary to ensure that data races, as defined below, and
with suitable restrictions on the use of atomics, correspond to data
races in a simple interleaved (sequentially consistent) execution.

The *visible sequence of side effects* on an atomic object *M*, with
respect to a value computation *B* of *M*, is a maximal contiguous
sub-sequence of side effects in the modification order of *M*, where the
first side effect is visible with respect to *B*, and for every side
effect, it is not the case that *B* happens before it. The value of an
atomic object *M*, as determined by evaluation *B*, shall be the value
stored by some operation in the visible sequence of *M* with respect to
*B*. It can be shown that the visible sequence of side effects of a
value computation is unique given the coherence requirements below.

If an operation *A* that modifies an atomic object *M* happens before an
operation *B* that modifies *M*, then *A* shall be earlier than *B* in
the modification order of *M*. This requirement is known as write-write
coherence.

If a value computation *A* of an atomic object *M* happens before a
value computation *B* of *M*, and *A* takes its value from a side effect
*X* on *M*, then the value computed by *B* shall either be the value
stored by *X* or the value stored by a side effect *Y* on *M*, where *Y*
follows *X* in the modification order of *M*. This requirement is known
as read-read coherence.

If a value computation *A* of an atomic object *M* happens before an
operation *B* on *M*, then *A* shall take its value from a side effect
*X* on *M*, where *X* precedes *B* in the modification order of *M*.
This requirement is known as read-write coherence.

If a side effect *X* on an atomic object *M* happens before a value
computation *B* of *M*, then the evaluation *B* shall take its value
from *X* or from a side effect *Y* that follows *X* in the modification
order of *M*. This requirement is known as write-read coherence.

The four preceding coherence requirements effectively disallow compiler
reordering of atomic operations to a single object, even if both
operations are relaxed loads. This effectively makes the cache coherence
guarantee provided by most hardware available to C++atomic operations.

The visible sequence of side effects depends on the “happens before”
relation, which depends on the values observed by loads of atomics,
which we are restricting here. The intended reading is that there must
exist an association of atomic loads with modifications they observe
that, together with suitably chosen modification orders and the “happens
before” relation derived as described above, satisfy the resulting
constraints as imposed here.

The execution of a program contains a *data race* if it contains two
conflicting actions in different threads, at least one of which is not
atomic, and neither happens before the other. Any such data race results
in undefined behavior. It can be shown that programs that correctly use
mutexes and `memory_order_seq_cst` operations to prevent all data races
and use no other synchronization operations behave as if the operations
executed by their constituent threads were simply interleaved, with each
value computation of an object being taken from the last side effect on
that object in that interleaving. This is normally referred to as
“sequential consistency”. However, this applies only to data-race-free
programs, and data-race-free programs cannot observe most program
transformations that do not change single-threaded program semantics. In
fact, most single-threaded program transformations continue to be
allowed, since any program that behaves differently as a result must
perform an undefined operation.

Compiler transformations that introduce assignments to a potentially
shared memory location that would not be modified by the abstract
machine are generally precluded by this standard, since such an
assignment might overwrite another assignment by a different thread in
cases in which an abstract machine execution would not have encountered
a data race. This includes implementations of data member assignment
that overwrite adjacent members in separate memory locations. Reordering
of atomic loads in cases in which the atomics in question may alias is
also generally precluded, since this may violate the “visible sequence”
rules.

Transformations that introduce a speculative read of a potentially
shared memory location may not preserve the semantics of the C++program
as defined in this standard, since they potentially introduce a data
race. However, they are typically valid in the context of an optimizing
compiler that targets a specific machine with well-defined semantics for
data races. They would be invalid for a hypothetical machine that is not
tolerant of races or provides hardware race detection.

The implementation may assume that any thread will eventually do one of
the following:

- terminate,
- make a call to a library I/O function,
- access or modify a volatile object, or
- perform a synchronization operation or an atomic operation.

This is intended to allow compiler transformations such as removal of
empty loops, even when termination cannot be proven.

An implementation should ensure that the last value (in modification
order) assigned by an atomic or synchronization operation will become
visible to all other threads in a finite period of time.

## Acknowledgments <a id="intro.ack">[[intro.ack]]</a>

The C++programming language as described in this International Standard
is based on the language as described in Chapter R (Reference Manual) of
Stroustrup: *The C++Programming Language* (second edition,
Addison-Wesley Publishing Company, ISBN 0-201-53992-6, copyright ©1991
AT&T). That, in turn, is based on the C programming language as
described in Appendix A of Kernighan and Ritchie: *The C Programming
Language* (Prentice-Hall, 1978, ISBN 0-13-110163-3, copyright ©1978
AT&T).

Portions of the library Clauses of this International Standard are based
on work by P.J. Plauger, which was published as *The Draft Standard
C++Library* (Prentice-Hall, ISBN 0-13-117003-1, copyright ©1995 P.J.
Plauger).

POSIX is a registered trademark of the Institute of Electrical and
Electronic Engineers, Inc.

All rights in these originals are reserved.

<!-- Section link definitions -->
[intro]: #intro
[intro.ack]: #intro.ack
[intro.compliance]: #intro.compliance
[intro.defs]: #intro.defs
[intro.execution]: #intro.execution
[intro.memory]: #intro.memory
[intro.multithread]: #intro.multithread
[intro.object]: #intro.object
[intro.refs]: #intro.refs
[intro.scope]: #intro.scope
[intro.structure]: #intro.structure
[syntax]: #syntax

<!-- Link reference definitions -->
[atomics]: atomics.md#atomics
[atomics.lockfree]: atomics.md#atomics.lockfree
[atomics.order]: atomics.md#atomics.order
[basic]: basic.md#basic
[basic.compound]: basic.md#basic.compound
[basic.def]: basic.md#basic.def
[basic.def.odr]: basic.md#basic.def.odr
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lval]: basic.md#basic.lval
[basic.namespace]: dcl.md#basic.namespace
[basic.stc]: basic.md#basic.stc
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.types]: basic.md#basic.types
[class.access]: class.md#class.access
[class.bit]: class.md#class.bit
[class.conv.fct]: special.md#class.conv.fct
[class.derived]: class.md#class.derived
[class.mem]: class.md#class.mem
[class.temporary]: special.md#class.temporary
[class.virtual]: class.md#class.virtual
[compliance]: library.md#compliance
[cpp]: cpp.md#cpp
[cpp.include]: cpp.md#cpp.include
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[definitions]: library.md#definitions
[depr]: #depr
[diff]: #diff
[diff.library]: compatibility.md#diff.library
[expr]: expr.md#expr
[expr.comma]: expr.md#expr.comma
[expr.cond]: expr.md#expr.cond
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.new]: expr.md#expr.new
[gram]: #gram
[implimits]: #implimits
[intro.compliance]: #intro.compliance
[intro.defs]: #intro.defs
[intro.execution]: #intro.execution
[intro.memory]: #intro.memory
[intro.multithread]: #intro.multithread
[intro.object]: #intro.object
[lex]: lex.md#lex
[lex.charset]: lex.md#lex.charset
[lex.phases]: lex.md#lex.phases
[library]: library.md#library
[support]: #support
[syntax]: #syntax
[thread]: thread.md#thread

[^1]: With the qualifications noted in Clauses  [[support]] through 
    [[thread]] and in  [[diff.library]], the C standard library is a
    subset of the C++standard library.

[^2]: “Correct execution” can include undefined behavior, depending on
    the data being processed; see  [[intro.defs]] and 
    [[intro.execution]].

[^3]: This documentation also defines implementation-defined behavior;
    see  [[intro.execution]].

[^4]: Under the “as-if” rule an implementation is allowed to store two
    objects at the same machine address or not store an object at all if
    the program cannot observe the difference ([[intro.execution]]).

[^5]: This provision is sometimes called the “as-if” rule, because an
    implementation is free to disregard any requirement of this
    International Standard as long as the result is *as if* the
    requirement had been obeyed, as far as can be determined from the
    observable behavior of the program. For instance, an actual
    implementation need not evaluate part of an expression if it can
    deduce that its value is not used and that no side effects affecting
    the observable behavior of the program are produced.

[^6]: This documentation also includes conditionally-supported
    constructs and locale-specific behavior. See  [[intro.compliance]].

[^7]: Overloaded operators are never assumed to be associative or
    commutative.

[^8]: As specified in  [[class.temporary]], after a full-expression is
    evaluated, a sequence of zero or more invocations of destructor
    functions for temporary objects takes place, usually in reverse
    order of the construction of each temporary object.

[^9]: In other words, function executions do not interleave with each
    other.

[^10]: An object with automatic or thread storage duration (
    [[basic.stc]]) is associated with one specific thread, and can be
    accessed by a different thread only indirectly through a pointer or
    reference ([[basic.compound]]).
