# Scope <a id="intro.scope">[[intro.scope]]</a>

This document specifies requirements for implementations of the
C++programming language. The first such requirement is that they
implement the language, so this document also defines C++. Other
requirements and relaxations of the first requirement appear at various
places within this document.

C++is a general purpose programming language based on the C programming
language as described in ISO/IEC 9899:2011 *Programming languages — C*
(hereinafter referred to as the *C standard*). In addition to the
facilities provided by C, C++provides additional data types, classes,
templates, exceptions, namespaces, operator overloading, function name
overloading, references, free store management operators, and additional
library facilities.

# Normative references <a id="intro.refs">[[intro.refs]]</a>

The following documents are referred to in the text in such a way that
some or all of their content constitutes requirements of this document.
For dated references, only the edition cited applies. For undated
references, the latest edition of the referenced document (including any
amendments) applies.

- Ecma International, *ECMAScript Language Specification*, Standard
  Ecma-262, third edition, 1999.
- ISO/IEC 2382 (all parts), *Information technology — Vocabulary*
- ISO/IEC 9899:2011, *Programming languages — C*
- ISO/IEC 9899:2011/Cor.1:2012(E), *Programming languages — C, Technical
  Corrigendum 1*
- ISO/IEC 9945:2003, *Information Technology — Portable Operating System
  Interface (POSIX)*
- ISO/IEC 10646-1:1993, *Information technology — Universal
  Multiple-Octet Coded Character Set (UCS) — Part 1: Architecture and
  Basic Multilingual Plane*
- ISO/IEC 10967-1:2012, *Information technology — Language independent
  arithmetic — Part 1: Integer and floating point arithmetic*
- ISO/IEC/IEEE 60559:2011, *Information technology — Microprocessor
  Systems — Floating-Point arithmetic*
- ISO 80000-2:2009, *Quantities and units — Part 2: Mathematical signs
  and symbols to be used in the natural sciences and technology*

The library described in Clause 7 of ISO/IEC 9899:2011 is hereinafter
called the *C standard library*. [^1]

The operating system interface described in ISO/IEC 9945:2003 is
hereinafter called *POSIX*.

The ECMAScript Language Specification described in Standard Ecma-262 is
hereinafter called *ECMA-262*.

The arithmetic specification described in ISO/IEC 10967-1:2012 is
hereinafter called *LIA-1*.

# Terms and definitions <a id="intro.defs">[[intro.defs]]</a>

For the purposes of this document, the terms and definitions given in
ISO/IEC 2382-1:1993, the terms, definitions, and symbols given in ISO
80000-2:2009, and the following apply.

ISO and IEC maintain terminological databases for use in standardization
at the following addresses:

- IEC Electropedia: available at <http://www.electropedia.org/>
- ISO Online browsing platform: available at <http://www.iso.org/obp>

[[definitions]] defines additional terms that are used only in Clauses 
[[library]] through  [[thread]] and Annex  [[depr]].

Terms that are used only in a small portion of this document are defined
where they are used and italicized where they are defined.

to read or modify the value of an object

expression in the comma-separated list bounded by the parentheses (
[[expr.call]])

sequence of preprocessing tokens in the comma-separated list bounded by
the parentheses ([[cpp.replace]])

the operand of `throw` ([[expr.throw]])

*constant-expression*, *type-id*, or *id-expression* in the
comma-separated list bounded by the angle brackets ([[temp.arg]])

a thread of execution that blocks is waiting for some condition (other
than for the implementation to execute its execution steps) to be
satisfied before it can continue execution past the blocking operation

program construct that an implementation is not required to support  

[*Note 1*: Each implementation documents all conditionally-supported
constructs that it does not support. — *end note*]

message belonging to an *implementation-defined* subset of the
implementation’s output messages

type of the most derived object ([[intro.object]]) to which the glvalue
refers  

[*Example 1*: If a pointer ([[dcl.ptr]]) `p` whose static type is
“pointer to class `B`” is pointing to an object of class `D`, derived
from `B` (Clause  [[class.derived]]), the dynamic type of the expression
`*p` is “`D`”. References ([[dcl.ref]]) are treated
similarly. — *end example*]

static type of the prvalue expression

program that is not well-formed ([[defns.well.formed]])

behavior, for a well-formed program construct and correct data, that
depends on the implementation and that each implementation documents

restrictions imposed upon programs by the implementation

behavior that depends on local conventions of nationality, culture, and
language that each implementation documents

sequence of one or more bytes representing a member of the extended
character set of either the source or the execution environment  

[*Note 2*: The extended character set is a superset of the basic
character set ([[lex.charset]]). — *end note*]

object or reference declared as part of a function declaration or
definition or in the catch clause of an exception handler that acquires
a value on entry to the function or handler

identifier from the comma-separated list bounded by the parentheses
immediately following the macro name

member of a *template-parameter-list*

name, parameter type list ([[dcl.fct]]), and enclosing namespace (if
any)  

[*Note 3*: Signatures are used as a basis for name mangling and
linking. — *end note*]

name, parameter type list ([[dcl.fct]]), enclosing namespace (if any),
return type, and template parameter list

signature of the template of which it is a specialization and its
template arguments (whether explicitly specified or deduced)

name, parameter type list ([[dcl.fct]]), class of which the function is
a member, cv-qualifiers (if any), and *ref-qualifier* (if any)

name, parameter type list ([[dcl.fct]]), class of which the function is
a member, cv-qualifiers (if any), *ref-qualifier* (if any), return type
(if any), and template parameter list

signature of the member function template of which it is a
specialization and its template arguments (whether explicitly specified
or deduced)

type of an expression ([[basic.types]]) resulting from analysis of the
program without considering execution semantics  

[*Note 4*: The static type of an expression depends only on the form of
the program in which the expression appears, and does not change while
the program is executing. — *end note*]

satisfy a condition that one or more blocked threads of execution are
waiting for

behavior for which this International Standard imposes no requirements  

[*Note 5*: Undefined behavior may be expected when this International
Standard omits any explicit definition of behavior or when a program
uses an erroneous construct or erroneous data. Permissible undefined
behavior ranges from ignoring the situation completely with
unpredictable results, to behaving during translation or program
execution in a documented manner characteristic of the environment (with
or without the issuance of a diagnostic message), to terminating a
translation or execution (with the issuance of a diagnostic message).
Many erroneous program constructs do not engender undefined behavior;
they are required to be diagnosed. Evaluation of a constant expression
never exhibits behavior explicitly specified as undefined (
[[expr.const]]). — *end note*]

behavior, for a well-formed program construct and correct data, that
depends on the implementation  

[*Note 6*: The implementation is not required to document which
behavior occurs. The range of possible behaviors is usually delineated
by this International Standard. — *end note*]

C++program constructed according to the syntax rules, diagnosable
semantic rules, and the one-definition rule ([[basic.def.odr]]).

# General principles <a id="intro">[[intro]]</a>

## Implementation compliance <a id="intro.compliance">[[intro.compliance]]</a>

The set of *diagnosable rules* consists of all syntactic and semantic
rules in this International Standard except for those rules containing
an explicit notation that “no diagnostic is required” or which are
described as resulting in “undefined behavior”.

Although this International Standard states only requirements on C++
implementations, those requirements are often easier to understand if
they are phrased as requirements on programs, parts of programs, or
execution of programs. Such requirements have the following meaning:

- If a program contains no violations of the rules in this International
  Standard, a conforming implementation shall, within its resource
  limits, accept and correctly execute[^2] that program.
- If a program contains a violation of any diagnosable rule or an
  occurrence of a construct described in this International Standard as
  “conditionally-supported” when the implementation does not support
  that construct, a conforming implementation shall issue at least one
  diagnostic message.
- If a program contains a violation of a rule for which no diagnostic is
  required, this International Standard places no requirement on
  implementations with respect to that program.

[*Note 1*: During template argument deduction and substitution, certain
constructs that in other contexts require a diagnostic are treated
differently; see  [[temp.deduct]]. — *end note*]

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

## Structure of this document <a id="intro.structure">[[intro.structure]]</a>

Clauses  [[lex]] through  [[cpp]] describe the C++programming language.
That description includes detailed syntactic specifications in a form
described in  [[syntax]]. For convenience, Annex  [[gram]] repeats all
such syntactic specifications.

Clauses  [[support]] through  [[thread]] and Annex  [[depr]] (the
*library clauses*) describe the C++standard library. That description
includes detailed descriptions of the entities and macros that
constitute the library, in a form described in Clause  [[library]].

Annex  [[implimits]] recommends lower bounds on the capacity of
conforming implementations.

Annex  [[diff]] summarizes the evolution of C++since its first published
description, and explains in detail the differences between C++and C.
Certain features of C++exist solely for compatibility purposes; Annex 
[[depr]] describes those features.

Throughout this document, each example is introduced by “” and
terminated by “”. Each note is introduced by “” and terminated by “”.
Examples and notes may be nested.

## Syntax notation <a id="syntax">[[syntax]]</a>

In the syntax notation used in this document, syntactic categories are
indicated by *italic* type, and literal words and characters in
`constant` `width` type. Alternatives are listed on separate lines
except in a few cases where a long set of alternatives is marked by the
phrase “one of”. If the text of an alternative is too long to fit on a
line, the text is continued on subsequent lines indented from the first
one. An optional terminal or non-terminal symbol is indicated by the
subscript “’ₒₚₜ’, so

``` bnf
\terminal{\ expressionₒₚₜ \terminal{\}}
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
  *identifier-list* is a sequence of identifiers separated by commas).

## The C++memory model <a id="intro.memory">[[intro.memory]]</a>

The fundamental storage unit in the C++memory model is the *byte*. A
byte is at least large enough to contain any member of the basic
execution character set ([[lex.charset]]) and the eight-bit code units
of the Unicode UTF-8 encoding form and is composed of a contiguous
sequence of bits,[^4] the number of which is *implementation-defined*.
The least significant bit is called the *low-order bit*; the most
significant bit is called the *high-order bit*. The memory available to
a C++program consists of one or more sequences of contiguous bytes.
Every byte has a unique address.

[*Note 1*: The representation of types is described in 
[[basic.types]]. — *end note*]

A *memory location* is either an object of scalar type or a maximal
sequence of adjacent bit-fields all having nonzero width.

[*Note 2*: Various features of the language, such as references and
virtual functions, might involve additional memory locations that are
not accessible to programs but are managed by the
implementation. — *end note*]

Two or more threads of execution ([[intro.multithread]]) can access
separate memory locations without interfering with each other.

[*Note 3*: Thus a bit-field and an adjacent non-bit-field are in
separate memory locations, and therefore can be concurrently updated by
two threads of execution without interference. The same applies to two
bit-fields, if one is declared inside a nested struct declaration and
the other is not, or if the two are separated by a zero-length bit-field
declaration, or if they are separated by a non-bit-field declaration. It
is not safe to concurrently update two bit-fields in the same struct if
all fields between them are also bit-fields of nonzero
width. — *end note*]

[*Example 1*:

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

— *end example*]

## The C++object model <a id="intro.object">[[intro.object]]</a>

The constructs in a C++program create, destroy, refer to, access, and
manipulate objects. An *object* is created by a definition (
[[basic.def]]), by a *new-expression* ([[expr.new]]), when implicitly
changing the active member of a union ([[class.union]]), or when a
temporary object is created ([[conv.rval]], [[class.temporary]]). An
object occupies a region of storage in its period of construction (
[[class.cdtor]]), throughout its lifetime ([[basic.life]]), and in its
period of destruction ([[class.cdtor]]).

[*Note 1*: A function is not an object, regardless of whether or not it
occupies storage in the way that objects do. — *end note*]

The properties of an object are determined when the object is created.
An object can have a name (Clause  [[basic]]). An object has a storage
duration ([[basic.stc]]) which influences its lifetime (
[[basic.life]]). An object has a type ([[basic.types]]). Some objects
are polymorphic ([[class.virtual]]); the implementation generates
information associated with each such object that makes it possible to
determine that object’s type during program execution. For other
objects, the interpretation of the values found therein is determined by
the type of the *expression*s (Clause  [[expr]]) used to access them.

Objects can contain other objects, called *subobjects*. A subobject can
be a *member subobject* ([[class.mem]]), a *base class subobject*
(Clause  [[class.derived]]), or an array element. An object that is not
a subobject of any other object is called a *complete object*. If an
object is created in storage associated with a member subobject or array
element *e* (which may or may not be within its lifetime), the created
object is a subobject of *e*’s containing object if:

- the lifetime of *e*’s containing object has begun and not ended, and
- the storage for the new object exactly overlays the storage location
  associated with *e*, and
- the new object is of the same type as *e* (ignoring cv-qualification).

[*Note 2*: If the subobject contains a reference member or a `const`
subobject, the name of the original subobject cannot be used to access
the new object ([[basic.life]]). — *end note*]

[*Example 1*:

``` cpp
struct X { const int n; };
union U { X x; float f; };
void tong() {
  U u = {{ 1 }};
  u.f = 5.f;                          // OK, creates new subobject of u ([class.union])
  X *p = new (&u.x) X {2};            // OK, creates new subobject of u
  assert(p->n == 2);                  // OK
  assert(*std::launder(&u.x.n) == 2); // OK
  assert(u.x.n == 2);                 // undefined behavior, u.x does not name new subobject
}
```

— *end example*]

If a complete object is created ([[expr.new]]) in storage associated
with another object *e* of type “array of N `unsigned char`” or of type
“array of N `std::byte`” ([[cstddef.syn]]), that array *provides
storage* for the created object if:

- the lifetime of *e* has begun and not ended, and
- the storage for the new object fits entirely within *e*, and
- there is no smaller array object that satisfies these constraints.

[*Note 3*: If that portion of the array previously provided storage for
another object, the lifetime of that object ends because its storage was
reused ([[basic.life]]). — *end note*]

[*Example 2*:

``` cpp
template<typename ...T>
struct AlignedUnion {
  alignas(T...) unsigned char data[max(sizeof(T)...)];
};
int f() {
  AlignedUnion<int, char> au;
  int *p = new (au.data) int;     // OK, au.data provides storage
  char *c = new (au.data) char(); // OK, ends lifetime of *p
  char *d = new (au.data + 1) char();
  return *c + *d; // OK
}

struct A { unsigned char a[32]; };
struct B { unsigned char b[16]; };
A a;
B *b = new (a.a + 8) B;      // a.a provides storage for *b
int *p = new (b->b + 4) int; // b->b provides storage for *p
                             // a.a does not provide storage for *p (directly),
                             // but *p is nested within a (see below)
```

— *end example*]

An object *a* is *nested within* another object *b* if:

- *a* is a subobject of *b*, or
- *b* provides storage for *a*, or
- there exists an object *c* where *a* is nested within *c*, and *c* is
  nested within *b*.

For every object `x`, there is some object called the *complete object
of* `x`, determined as follows:

- If `x` is a complete object, then the complete object of `x` is
  itself.
- Otherwise, the complete object of `x` is the complete object of the
  (unique) object that contains `x`.

If a complete object, a data member ([[class.mem]]), or an array
element is of class type, its type is considered the *most derived
class*, to distinguish it from the class type of any base class
subobject; an object of a most derived class type or of a non-class type
is called a *most derived object*.

Unless it is a bit-field ([[class.bit]]), a most derived object shall
have a nonzero size and shall occupy one or more bytes of storage. Base
class subobjects may have zero size. An object of trivially copyable or
standard-layout type ([[basic.types]]) shall occupy contiguous bytes of
storage.

Unless an object is a bit-field or a base class subobject of zero size,
the address of that object is the address of the first byte it occupies.
Two objects *a* and *b* with overlapping lifetimes that are not
bit-fields may have the same address if one is nested within the other,
or if at least one is a base class subobject of zero size and they are
of different types; otherwise, they have distinct addresses.[^5]

[*Example 3*:

``` cpp
static const char test1 = 'x';
static const char test2 = 'x';
const bool b = &test1 != &test2;      // always true
```

— *end example*]

[*Note 4*: C++provides a variety of fundamental types and several ways
of composing new types from existing types (
[[basic.types]]). — *end note*]

## Program execution <a id="intro.execution">[[intro.execution]]</a>

The semantic descriptions in this International Standard define a
parameterized nondeterministic abstract machine. This International
Standard places no requirement on the structure of conforming
implementations. In particular, they need not copy or emulate the
structure of the abstract machine. Rather, conforming implementations
are required to emulate (only) the observable behavior of the abstract
machine as explained below.[^6]

Certain aspects and operations of the abstract machine are described in
this International Standard as implementation-defined (for example,
`sizeof(int)`). These constitute the parameters of the abstract machine.
Each implementation shall include documentation describing its
characteristics and behavior in these respects.[^7] Such documentation
shall define the instance of the abstract machine that corresponds to
that implementation (referred to as the “corresponding instance” below).

Certain other aspects and operations of the abstract machine are
described in this International Standard as unspecified (for example,
evaluation of expressions in a *new-initializer* if the allocation
function fails to allocate memory ([[expr.new]])). Where possible, this
International Standard defines a set of allowable behaviors. These
define the nondeterministic aspects of the abstract machine. An instance
of the abstract machine can thus have more than one possible execution
for a given program and a given input.

Certain other operations are described in this International Standard as
undefined (for example, the effect of attempting to modify a `const`
object).

[*Note 1*: This International Standard imposes no requirements on the
behavior of programs that contain undefined behavior. — *end note*]

A conforming implementation executing a well-formed program shall
produce the same observable behavior as one of the possible executions
of the corresponding instance of the abstract machine with the same
program and the same input. However, if any such execution contains an
undefined operation, this International Standard places no requirement
on the implementation executing that program with that input (not even
with regard to operations preceding the first undefined operation).

An instance of each object with automatic storage duration (
[[basic.stc.auto]]) is associated with each entry into its block. Such
an object exists and retains its last-stored value during the execution
of the block and while the block is suspended (by a call of a function
or receipt of a signal).

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

[*Note 3*:

Operators can be regrouped according to the usual mathematical rules
only where the operators really are associative or commutative.[^8] For
example, in the following fragment

``` cpp
int a, b;
...
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

— *end note*]

A *constituent expression* is defined as follows:

- The constituent expression of an expression is that expression.
- The constituent expressions of a *braced-init-list* or of a (possibly
  parenthesized) *expression-list* are the constituent expressions of
  the elements of the respective list.
- The constituent expressions of a *brace-or-equal-initializer* of the
  form `=` *initializer-clause* are the constituent expressions of the
  *initializer-clause*.

[*Example 1*:

``` cpp
struct A { int x; };
struct B { int y; struct A a; };
B b = { 5, { 1+1 } };
```

The constituent expressions of the *initializer* used for the
initialization of `b` are `5` and `1+1`.

— *end example*]

The *immediate subexpressions* of an expression `e` are

- the constituent expressions of `e`’s operands (Clause [[expr]]),
- any function call that `e` implicitly invokes,
- if `e` is a *lambda-expression* ([[expr.prim.lambda]]), the
  initialization of the entities captured by copy and the constituent
  expressions of the *initializer* of the *init-capture*s,
- if `e` is a function call ([[expr.call]]) or implicitly invokes a
  function, the constituent expressions of each default argument (
  [[dcl.fct.default]]) used in the call, or
- if `e` creates an aggregate object ([[dcl.init.aggr]]), the
  constituent expressions of each default member initializer (
  [[class.mem]]) used in the initialization.

A *subexpression* of an expression `e` is an immediate subexpression of
`e` or a subexpression of an immediate subexpression of `e`.

[*Note 4*: Expressions appearing in the *compound-statement* of a
*lambda-expression* are not subexpressions of the
*lambda-expression*. — *end note*]

A *full-expression* is

- an unevaluated operand (Clause [[expr]]),
- a *constant-expression* ([[expr.const]]),
- an *init-declarator* (Clause [[dcl.decl]]) or a *mem-initializer* (
  [[class.base.init]]), including the constituent expressions of the
  initializer,
- an invocation of a destructor generated at the end of the lifetime of
  an object other than a temporary object ([[class.temporary]]), or
- an expression that is not a subexpression of another expression and
  that is not otherwise part of a full-expression.

If a language construct is defined to produce an implicit call of a
function, a use of the language construct is considered to be an
expression for the purposes of this definition. Conversions applied to
the result of an expression in order to satisfy the requirements of the
language construct in which the expression appears are also considered
to be part of the full-expression. For an initializer, performing the
initialization of the entity (including evaluating default member
initializers of an aggregate) is also considered part of the
full-expression.

[*Example 2*:

``` cpp
struct S {
  S(int i): I(i) { }       // full-expression is initialization of I
  int& v() { return I; }
  ~S() noexcept(false) { }
private:
  int I;
};

S s1(1);                   // full-expression is call of S::S(int)
void f() {
  S s2 = 2;                // full-expression is call of S::S(int)
  if (S(3).v())            // full-expression includes lvalue-to-rvalue and
                           // int to bool conversions, performed before
                           // temporary is deleted at end of full-expression
  { }
  bool b = noexcept(S());  // exception specification of destructor of S
                           // considered for noexcept
  // full-expression is destruction of s2 at end of block
}
struct B {
      B(S = S(0));
   };
   B b[2] = { B(), B() };  // full-expression is the entire initialization
                           // including the destruction of temporaries
```

— *end example*]

[*Note 5*: The evaluation of a full-expression can include the
evaluation of subexpressions that are not lexically part of the
full-expression. For example, subexpressions involved in evaluating
default arguments ([[dcl.fct.default]]) are considered to be created in
the expression that calls the function, not the expression that defines
the default argument. — *end note*]

Reading an object designated by a `volatile` glvalue ([[basic.lval]]),
modifying an object, calling a library I/O function, or calling a
function that does any of those operations are all *side effects*, which
are changes in the state of the execution environment. *Evaluation* of
an expression (or a subexpression) in general includes both value
computations (including determining the identity of an object for
glvalue evaluation and fetching a value previously assigned to an object
for prvalue evaluation) and initiation of side effects. When a call to a
library I/O function returns or an access through a volatile glvalue is
evaluated the side effect is considered complete, even though some
external actions implied by the call (such as the I/O itself) or by the
`volatile` access may not have completed yet.

*Sequenced before* is an asymmetric, transitive, pair-wise relation
between evaluations executed by a single thread (
[[intro.multithread]]), which induces a partial order among those
evaluations. Given any two evaluations *A* and *B*, if *A* is sequenced
before *B* (or, equivalently, *B* is *sequenced after* *A*), then the
execution of *A* shall precede the execution of *B*. If *A* is not
sequenced before *B* and *B* is not sequenced before *A*, then *A* and
*B* are *unsequenced*.

[*Note 6*: The execution of unsequenced evaluations can
overlap. — *end note*]

Evaluations *A* and *B* are *indeterminately sequenced* when either *A*
is sequenced before *B* or *B* is sequenced before *A*, but it is
unspecified which.

[*Note 7*: Indeterminately sequenced evaluations cannot overlap, but
either could be executed first. — *end note*]

An expression *X* is said to be sequenced before an expression *Y* if
every value computation and every side effect associated with the
expression *X* is sequenced before every value computation and every
side effect associated with the expression *Y*.

Every value computation and side effect associated with a
full-expression is sequenced before every value computation and side
effect associated with the next full-expression to be evaluated.[^9]

Except where noted, evaluations of operands of individual operators and
of subexpressions of individual expressions are unsequenced.

[*Note 8*: In an expression that is evaluated more than once during the
execution of a program, unsequenced and indeterminately sequenced
evaluations of its subexpressions need not be performed consistently in
different evaluations. — *end note*]

The value computations of the operands of an operator are sequenced
before the value computation of the result of the operator. If a side
effect on a memory location ([[intro.memory]]) is unsequenced relative
to either another side effect on the same memory location or a value
computation using the value of any object in the same memory location,
and they are not potentially concurrent ([[intro.multithread]]), the
behavior is undefined.

[*Note 9*: The next section imposes similar, but more complex
restrictions on potentially concurrent computations. — *end note*]

[*Example 3*:

``` cpp
void g(int i) {
  i = 7, i++, i++;    // i becomes 9

  i = i++ + 1;        // the value of i is incremented
  i = i++ + i;        // the behavior is undefined
  i = i + 1;          // the value of i is incremented
}
```

— *end example*]

When calling a function (whether or not the function is inline), every
value computation and side effect associated with any argument
expression, or with the postfix expression designating the called
function, is sequenced before execution of every expression or statement
in the body of the called function. For each function invocation *F*,
for every evaluation *A* that occurs within *F* and every evaluation *B*
that does not occur within *F* but is evaluated on the same thread and
as part of the same signal handler (if any), either *A* is sequenced
before *B* or *B* is sequenced before *A*.[^10]

[*Note 10*: If *A* and *B* would not otherwise be sequenced then they
are indeterminately sequenced. — *end note*]

Several contexts in C++cause evaluation of a function call, even though
no corresponding function call syntax appears in the translation unit.

[*Example 4*: Evaluation of a *new-expression* invokes one or more
allocation and constructor functions; see  [[expr.new]]. For another
example, invocation of a conversion function ([[class.conv.fct]]) can
arise in contexts in which no function call syntax
appears. — *end example*]

The sequencing constraints on the execution of the called function (as
described above) are features of the function calls as evaluated,
whatever the syntax of the expression that calls the function might be.

If a signal handler is executed as a result of a call to the
`std::raise` function, then the execution of the handler is sequenced
after the invocation of the `std::raise` function and before its return.

[*Note 11*: When a signal is received for another reason, the execution
of the signal handler is usually unsequenced with respect to the rest of
the program. — *end note*]

## Multi-threaded executions and data races <a id="intro.multithread">[[intro.multithread]]</a>

A *thread of execution* (also known as a *thread*) is a single flow of
control within a program, including the initial invocation of a specific
top-level function, and recursively including every function invocation
subsequently executed by the thread.

[*Note 1*: When one thread creates another, the initial call to the
top-level function of the new thread is executed by the new thread, not
by the creating thread. — *end note*]

Every thread in a program can potentially access every object and
function in a program.[^11] Under a hosted implementation, a C++program
can have more than one thread running concurrently. The execution of
each thread proceeds as defined by the remainder of this International
Standard. The execution of the entire program consists of an execution
of all of its threads.

[*Note 2*: Usually the execution can be viewed as an interleaving of
all its threads. However, some kinds of atomic operations, for example,
allow executions inconsistent with a simple interleaving, as described
below. — *end note*]

Under a freestanding implementation, it is *implementation-defined*
whether a program can have more than one thread of execution.

For a signal handler that is not executed as a result of a call to the
`std::raise` function, it is unspecified which thread of execution
contains the signal handler invocation.

### Data races <a id="intro.races">[[intro.races]]</a>

The value of an object visible to a thread *T* at a particular point is
the initial value of the object, a value assigned to the object by *T*,
or a value assigned to the object by another thread, according to the
rules below.

[*Note 1*: In some cases, there may instead be undefined behavior. Much
of this section is motivated by the desire to support atomic operations
with explicit and detailed visibility constraints. However, it also
implicitly supports a simpler view for more restricted
programs. — *end note*]

Two expression evaluations *conflict* if one of them modifies a memory
location ([[intro.memory]]) and the other one reads or modifies the
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
which have special characteristics.

[*Note 2*: For example, a call that acquires a mutex will perform an
acquire operation on the locations comprising the mutex.
Correspondingly, a call that releases the same mutex will perform a
release operation on those same locations. Informally, performing a
release operation on *A* forces prior side effects on other memory
locations to become visible to other threads that later perform a
consume or an acquire operation on *A*. “Relaxed” atomic operations are
not synchronization operations even though, like synchronization
operations, they cannot contribute to data races. — *end note*]

All modifications to a particular atomic object *M* occur in some
particular total order, called the *modification order* of *M*.

[*Note 3*: There is a separate order for each atomic object. There is
no requirement that these can be combined into a single total order for
all objects. In general this will be impossible since different threads
may observe modifications to different objects in inconsistent
orders. — *end note*]

A *release sequence* headed by a release operation *A* on an atomic
object *M* is a maximal contiguous sub-sequence of side effects in the
modification order of *M*, where the first operation is `A`, and every
subsequent operation

- is performed by the same thread that performed `A`, or
- is an atomic read-modify-write operation.

Certain library calls *synchronize with* other library calls performed
by another thread. For example, an atomic store-release synchronizes
with a load-acquire that takes its value from the store (
[[atomics.order]]).

[*Note 4*: Except in the specified cases, reading a later value does
not necessarily ensure visibility as described below. Such a requirement
would sometimes interfere with efficient implementation. — *end note*]

[*Note 5*: The specifications of the synchronization operations define
when one reads the value written by another. For atomic objects, the
definition is clear. All operations on a given mutex occur in a single
total order. Each mutex acquisition “reads the value written” by the
last mutex release. — *end note*]

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

[*Note 6*: “Carries a dependency to” is a subset of “is sequenced
before”, and is similarly strictly intra-thread. — *end note*]

An evaluation *A* is *dependency-ordered before* an evaluation *B* if

- *A* performs a release operation on an atomic object *M*, and, in
  another thread, *B* performs a consume operation on *M* and reads a
  value written by any side effect in the release sequence headed by
  *A*, or
- for some evaluation *X*, *A* is dependency-ordered before *X* and *X*
  carries a dependency to *B*.

[*Note 7*: The relation “is dependency-ordered before” is analogous to
“synchronizes with”, but uses release/consume in place of
release/acquire. — *end note*]

An evaluation *A* *inter-thread happens before* an evaluation *B* if

- *A* synchronizes with *B*, or
- *A* is dependency-ordered before *B*, or
- for some evaluation *X*
  - *A* synchronizes with *X* and *X* is sequenced before *B*, or
  - *A* is sequenced before *X* and *X* inter-thread happens before *B*,
    or
  - *A* inter-thread happens before *X* and *X* inter-thread happens
    before *B*.

[*Note 8*: The “inter-thread happens before” relation describes
arbitrary concatenations of “sequenced before”, “synchronizes with” and
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
consisting entirely of “sequenced before”. — *end note*]

An evaluation *A* *happens before* an evaluation *B* (or, equivalently,
*B* *happens after* *A*) if:

- *A* is sequenced before *B*, or
- *A* inter-thread happens before *B*.

The implementation shall ensure that no program execution demonstrates a
cycle in the “happens before” relation.

[*Note 9*: This cycle would otherwise be possible only through the use
of consume operations. — *end note*]

An evaluation *A* *strongly happens before* an evaluation *B* if either

- *A* is sequenced before *B*, or
- *A* synchronizes with *B*, or
- *A* strongly happens before *X* and *X* strongly happens before *B*.

[*Note 10*: In the absence of consume operations, the happens before
and strongly happens before relations are identical. Strongly happens
before essentially excludes consume operations. — *end note*]

A *visible side effect* *A* on a scalar object or bit-field *M* with
respect to a value computation *B* of *M* satisfies the conditions:

- *A* happens before *B* and
- there is no other side effect *X* to *M* such that *A* happens before
  *X* and *X* happens before *B*.

The value of a non-atomic scalar object or bit-field *M*, as determined
by evaluation *B*, shall be the value stored by the visible side effect
*A*.

[*Note 11*: If there is ambiguity about which side effect to a
non-atomic object or bit-field is visible, then the behavior is either
unspecified or undefined. — *end note*]

[*Note 12*: This states that operations on ordinary objects are not
visibly reordered. This is not actually detectable without data races,
but it is necessary to ensure that data races, as defined below, and
with suitable restrictions on the use of atomics, correspond to data
races in a simple interleaved (sequentially consistent)
execution. — *end note*]

The value of an atomic object *M*, as determined by evaluation *B*,
shall be the value stored by some side effect *A* that modifies *M*,
where *B* does not happen before *A*.

[*Note 13*: The set of such side effects is also restricted by the rest
of the rules described here, and in particular, by the coherence
requirements below. — *end note*]

If an operation *A* that modifies an atomic object *M* happens before an
operation *B* that modifies *M*, then *A* shall be earlier than *B* in
the modification order of *M*.

[*Note 14*: This requirement is known as write-write
coherence. — *end note*]

If a value computation *A* of an atomic object *M* happens before a
value computation *B* of *M*, and *A* takes its value from a side effect
*X* on *M*, then the value computed by *B* shall either be the value
stored by *X* or the value stored by a side effect *Y* on *M*, where *Y*
follows *X* in the modification order of *M*.

[*Note 15*: This requirement is known as read-read
coherence. — *end note*]

If a value computation *A* of an atomic object *M* happens before an
operation *B* that modifies *M*, then *A* shall take its value from a
side effect *X* on *M*, where *X* precedes *B* in the modification order
of *M*.

[*Note 16*: This requirement is known as read-write
coherence. — *end note*]

If a side effect *X* on an atomic object *M* happens before a value
computation *B* of *M*, then the evaluation *B* shall take its value
from *X* or from a side effect *Y* that follows *X* in the modification
order of *M*.

[*Note 17*: This requirement is known as write-read
coherence. — *end note*]

[*Note 18*: The four preceding coherence requirements effectively
disallow compiler reordering of atomic operations to a single object,
even if both operations are relaxed loads. This effectively makes the
cache coherence guarantee provided by most hardware available to
C++atomic operations. — *end note*]

[*Note 19*: The value observed by a load of an atomic depends on the
“happens before” relation, which depends on the values observed by loads
of atomics. The intended reading is that there must exist an association
of atomic loads with modifications they observe that, together with
suitably chosen modification orders and the “happens before” relation
derived as described above, satisfy the resulting constraints as imposed
here. — *end note*]

Two actions are *potentially concurrent* if

- they are performed by different threads, or
- they are unsequenced, at least one is performed by a signal handler,
  and they are not both performed by the same signal handler invocation.

The execution of a program contains a *data race* if it contains two
potentially concurrent conflicting actions, at least one of which is not
atomic, and neither happens before the other, except for the special
case for signal handlers described below. Any such data race results in
undefined behavior.

[*Note 20*: It can be shown that programs that correctly use mutexes
and `memory_order_seq_cst` operations to prevent all data races and use
no other synchronization operations behave as if the operations executed
by their constituent threads were simply interleaved, with each value
computation of an object being taken from the last side effect on that
object in that interleaving. This is normally referred to as “sequential
consistency”. However, this applies only to data-race-free programs, and
data-race-free programs cannot observe most program transformations that
do not change single-threaded program semantics. In fact, most
single-threaded program transformations continue to be allowed, since
any program that behaves differently as a result must perform an
undefined operation. — *end note*]

Two accesses to the same object of type `volatile std::sig_atomic_t` do
not result in a data race if both occur in the same thread, even if one
or more occurs in a signal handler. For each signal handler invocation,
evaluations performed by the thread invoking a signal handler can be
divided into two groups *A* and *B*, such that no evaluations in *B*
happen before evaluations in *A*, and the evaluations of such
`volatile std::sig_atomic_t` objects take values as though all
evaluations in *A* happened before the execution of the signal handler
and the execution of the signal handler happened before all evaluations
in *B*.

[*Note 21*: Compiler transformations that introduce assignments to a
potentially shared memory location that would not be modified by the
abstract machine are generally precluded by this International Standard,
since such an assignment might overwrite another assignment by a
different thread in cases in which an abstract machine execution would
not have encountered a data race. This includes implementations of data
member assignment that overwrite adjacent members in separate memory
locations. Reordering of atomic loads in cases in which the atomics in
question may alias is also generally precluded, since this may violate
the coherence rules. — *end note*]

[*Note 22*: Transformations that introduce a speculative read of a
potentially shared memory location may not preserve the semantics of the
C++program as defined in this International Standard, since they
potentially introduce a data race. However, they are typically valid in
the context of an optimizing compiler that targets a specific machine
with well-defined semantics for data races. They would be invalid for a
hypothetical machine that is not tolerant of races or provides hardware
race detection. — *end note*]

### Forward progress <a id="intro.progress">[[intro.progress]]</a>

The implementation may assume that any thread will eventually do one of
the following:

- terminate,
- make a call to a library I/O function,
- perform an access through a volatile glvalue, or
- perform a synchronization operation or an atomic operation.

[*Note 1*: This is intended to allow compiler transformations such as
removal of empty loops, even when termination cannot be
proven. — *end note*]

Executions of atomic functions that are either defined to be lock-free (
[[atomics.flag]]) or indicated as lock-free ([[atomics.lockfree]]) are
*lock-free executions*.

- If there is only one thread that is not blocked ([[defns.block]]) in
  a standard library function, a lock-free execution in that thread
  shall complete. \[*Note 2*: Concurrently executing threads may prevent
  progress of a lock-free execution. For example, this situation can
  occur with load-locked store-conditional implementations. This
  property is sometimes termed obstruction-free. — *end note*]
- When one or more lock-free executions run concurrently, at least one
  should complete. \[*Note 3*: It is difficult for some implementations
  to provide absolute guarantees to this effect, since repeated and
  particularly inopportune interference from other threads may prevent
  forward progress, e.g., by repeatedly stealing a cache line for
  unrelated purposes between load-locked and store-conditional
  instructions. Implementations should ensure that such effects cannot
  indefinitely delay progress under expected operating conditions, and
  that such anomalies can therefore safely be ignored by programmers.
  Outside this document, this property is sometimes termed
  lock-free. — *end note*]

During the execution of a thread of execution, each of the following is
termed an *execution step*:

- termination of the thread of execution,
- performing an access through a volatile glvalue, or
- completion of a call to a library I/O function, a synchronization
  operation, or an atomic operation.

An invocation of a standard library function that blocks (
[[defns.block]]) is considered to continuously execute execution steps
while waiting for the condition that it blocks on to be satisfied.

[*Example 1*: A library I/O function that blocks until the I/O
operation is complete can be considered to continuously check whether
the operation is complete. Each such check might consist of one or more
execution steps, for example using observable behavior of the abstract
machine. — *end example*]

[*Note 4*: Because of this and the preceding requirement regarding what
threads of execution have to perform eventually, it follows that no
thread of execution can execute forever without an execution step
occurring. — *end note*]

A thread of execution *makes progress* when an execution step occurs or
a lock-free execution does not complete because there are other
concurrent threads that are not blocked in a standard library function
(see above).

For a thread of execution providing *concurrent forward progress
guarantees*, the implementation ensures that the thread will eventually
make progress for as long as it has not terminated.

[*Note 5*: This is required regardless of whether or not other threads
of executions (if any) have been or are making progress. To eventually
fulfill this requirement means that this will happen in an unspecified
but finite amount of time. — *end note*]

It is *implementation-defined* whether the implementation-created thread
of execution that executes `main` ([[basic.start.main]]) and the
threads of execution created by `std::thread` ([[thread.thread.class]])
provide concurrent forward progress guarantees.

[*Note 6*: General-purpose implementations are encouraged to provide
these guarantees. — *end note*]

For a thread of execution providing *parallel forward progress
guarantees*, the implementation is not required to ensure that the
thread will eventually make progress if it has not yet executed any
execution step; once this thread has executed a step, it provides
concurrent forward progress guarantees.

[*Note 7*: This does not specify a requirement for when to start this
thread of execution, which will typically be specified by the entity
that creates this thread of execution. For example, a thread of
execution that provides concurrent forward progress guarantees and
executes tasks from a set of tasks in an arbitrary order, one after the
other, satisfies the requirements of parallel forward progress for these
tasks. — *end note*]

For a thread of execution providing *weakly parallel forward progress
guarantees*, the implementation does not ensure that the thread will
eventually make progress.

[*Note 8*: Threads of execution providing weakly parallel forward
progress guarantees cannot be expected to make progress regardless of
whether other threads make progress or not; however, blocking with
forward progress guarantee delegation, as defined below, can be used to
ensure that such threads of execution make progress
eventually. — *end note*]

Concurrent forward progress guarantees are stronger than parallel
forward progress guarantees, which in turn are stronger than weakly
parallel forward progress guarantees.

[*Note 9*: For example, some kinds of synchronization between threads
of execution may only make progress if the respective threads of
execution provide parallel forward progress guarantees, but will fail to
make progress under weakly parallel guarantees. — *end note*]

When a thread of execution *P* is specified to *block with forward
progress guarantee delegation* on the completion of a set *S* of threads
of execution, then throughout the whole time of *P* being blocked on
*S*, the implementation shall ensure that the forward progress
guarantees provided by at least one thread of execution in *S* is at
least as strong as *P*’s forward progress guarantees.

[*Note 10*: It is unspecified which thread or threads of execution in
*S* are chosen and for which number of execution steps. The
strengthening is not permanent and not necessarily in place for the rest
of the lifetime of the affected thread of execution. As long as *P* is
blocked, the implementation has to eventually select and potentially
strengthen a thread of execution in *S*. — *end note*]

Once a thread of execution in *S* terminates, it is removed from *S*.
Once *S* is empty, *P* is unblocked.

[*Note 11*: A thread of execution *B* thus can temporarily provide an
effectively stronger forward progress guarantee for a certain amount of
time, due to a second thread of execution *A* being blocked on it with
forward progress guarantee delegation. In turn, if *B* then blocks with
forward progress guarantee delegation on *C*, this may also temporarily
provide a stronger forward progress guarantee to *C*. — *end note*]

[*Note 12*: If all threads of execution in *S* finish executing (e.g.,
they terminate and do not use blocking synchronization incorrectly),
then *P*’s execution of the operation that blocks with forward progress
guarantee delegation will not result in *P*’s progress guarantee being
effectively weakened. — *end note*]

[*Note 13*: This does not remove any constraints regarding blocking
synchronization for threads of execution providing parallel or weakly
parallel forward progress guarantees because the implementation is not
required to strengthen a particular thread of execution whose too-weak
progress guarantee is preventing overall progress. — *end note*]

An implementation should ensure that the last value (in modification
order) assigned by an atomic or synchronization operation will become
visible to all other threads in a finite period of time.

## Acknowledgments <a id="intro.ack">[[intro.ack]]</a>

The C++programming language as described in this document is based on
the language as described in Chapter R (Reference Manual) of Stroustrup:
*The C++Programming Language* (second edition, Addison-Wesley Publishing
Company, ISBN 0-201-53992-6, copyright ©1991 AT&T). That, in turn, is
based on the C programming language as described in Appendix A of
Kernighan and Ritchie: *The C Programming Language* (Prentice-Hall,
1978, ISBN 0-13-110163-3, copyright ©1978 AT&T).

Portions of the library Clauses of this document are based on work by
P.J. Plauger, which was published as *The Draft Standard C++Library*
(Prentice-Hall, ISBN 0-13-117003-1, copyright ©1995 P.J. Plauger).

POSIX® is a registered trademark of the Institute of Electrical and
Electronic Engineers, Inc.

ECMAScript® is a registered trademark of Ecma International.

All rights in these originals are reserved.

<!-- Link reference definitions -->
[atomics]: atomics.md#atomics
[atomics.flag]: atomics.md#atomics.flag
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
[basic.start.main]: basic.md#basic.start.main
[basic.stc]: basic.md#basic.stc
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.types]: basic.md#basic.types
[class.access]: class.md#class.access
[class.base.init]: special.md#class.base.init
[class.bit]: class.md#class.bit
[class.cdtor]: special.md#class.cdtor
[class.conv.fct]: special.md#class.conv.fct
[class.derived]: class.md#class.derived
[class.mem]: class.md#class.mem
[class.temporary]: special.md#class.temporary
[class.union]: class.md#class.union
[class.virtual]: class.md#class.virtual
[compliance]: library.md#compliance
[conv.rval]: conv.md#conv.rval
[cpp]: cpp.md#cpp
[cpp.include]: cpp.md#cpp.include
[cpp.replace]: cpp.md#cpp.replace
[cstddef.syn]: language.md#cstddef.syn
[dcl.decl]: dcl.md#dcl.decl
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[definitions]: library.md#definitions
[defns.block]: #defns.block
[defns.well.formed]: #defns.well.formed
[depr]: #depr
[diff]: #diff
[diff.library]: compatibility.md#diff.library
[expr]: expr.md#expr
[expr.call]: expr.md#expr.call
[expr.comma]: expr.md#expr.comma
[expr.cond]: expr.md#expr.cond
[expr.const]: expr.md#expr.const
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.new]: expr.md#expr.new
[expr.prim.lambda]: expr.md#expr.prim.lambda
[expr.throw]: expr.md#expr.throw
[gram]: #gram
[implimits]: #implimits
[intro]: #intro
[intro.ack]: #intro.ack
[intro.compliance]: #intro.compliance
[intro.defs]: #intro.defs
[intro.execution]: #intro.execution
[intro.memory]: #intro.memory
[intro.multithread]: #intro.multithread
[intro.object]: #intro.object
[intro.progress]: #intro.progress
[intro.races]: #intro.races
[intro.refs]: #intro.refs
[intro.scope]: #intro.scope
[intro.structure]: #intro.structure
[lex]: lex.md#lex
[lex.charset]: lex.md#lex.charset
[lex.phases]: lex.md#lex.phases
[library]: library.md#library
[support]: #support
[syntax]: #syntax
[temp.arg]: temp.md#temp.arg
[temp.deduct]: temp.md#temp.deduct
[thread]: thread.md#thread
[thread.thread.class]: thread.md#thread.thread.class

[^1]: With the qualifications noted in Clauses  [[support]] through 
    [[thread]] and in  [[diff.library]], the C standard library is a
    subset of the C++standard library.

[^2]: “Correct execution” can include undefined behavior, depending on
    the data being processed; see Clause  [[intro.defs]] and 
    [[intro.execution]].

[^3]: This documentation also defines implementation-defined behavior;
    see  [[intro.execution]].

[^4]: The number of bits in a byte is reported by the macro `CHAR_BIT`
    in the header `<climits>`.

[^5]: Under the “as-if” rule an implementation is allowed to store two
    objects at the same machine address or not store an object at all if
    the program cannot observe the difference ([[intro.execution]]).

[^6]: This provision is sometimes called the “as-if” rule, because an
    implementation is free to disregard any requirement of this
    International Standard as long as the result is *as if* the
    requirement had been obeyed, as far as can be determined from the
    observable behavior of the program. For instance, an actual
    implementation need not evaluate part of an expression if it can
    deduce that its value is not used and that no side effects affecting
    the observable behavior of the program are produced.

[^7]: This documentation also includes conditionally-supported
    constructs and locale-specific behavior. See  [[intro.compliance]].

[^8]: Overloaded operators are never assumed to be associative or
    commutative.

[^9]: As specified in  [[class.temporary]], after a full-expression is
    evaluated, a sequence of zero or more invocations of destructor
    functions for temporary objects takes place, usually in reverse
    order of the construction of each temporary object.

[^10]: In other words, function executions do not interleave with each
    other.

[^11]: An object with automatic or thread storage duration (
    [[basic.stc]]) is associated with one specific thread, and can be
    accessed by a different thread only indirectly through a pointer or
    reference ([[basic.compound]]).
