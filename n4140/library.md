# Library introduction <a id="library">[[library]]</a>

## General <a id="library.general">[[library.general]]</a>

This Clause describes the contents of the *C++standard library*, how a
well-formed C++program makes use of the library, and how a conforming
implementation may provide the entities in the library.

The following subclauses describe the definitions ([[definitions]]),
method of description ([[description]]), and organization (
[[organization]]) of the library. Clause  [[requirements]], Clauses 
[[support]] through  [[thread]], and Annex  [[depr]] specify the
contents of the library, as well as library requirements and constraints
on both well-formed C++programs and conforming implementations.

Detailed specifications for each of the components in the library are in
Clauses  [[support]]– [[thread]], as shown in Table 
[[tab:library.categories]].

The language support library (Clause  [[language.support]]) provides
components that are required by certain parts of the C++language, such
as memory allocation ([[expr.new]], [[expr.delete]]) and exception
processing (Clause  [[except]]).

The diagnostics library (Clause  [[diagnostics]]) provides a consistent
framework for reporting errors in a C++program, including predefined
exception classes.

The general utilities library (Clause  [[utilities]]) includes
components used by other library elements, such as a predefined storage
allocator for dynamic storage management ([[basic.stc.dynamic]]), and
components used as infrastructure in C++programs, such as a tuples,
function wrappers, and time facilities.

The strings library (Clause  [[strings]]) provides support for
manipulating text represented as sequences of type `char`, sequences of
type `char16_t`, sequences of type `char32_t`, sequences of type
`wchar_t`, and sequences of any other character-like type.

The localization library (Clause  [[localization]]) provides extended
internationalization support for text processing.

The containers (Clause  [[containers]]), iterators (Clause 
[[iterators]]), and algorithms (Clause  [[algorithms]]) libraries
provide a C++program with access to a subset of the most widely used
algorithms and data structures.

The numerics library (Clause  [[numerics]]) provides numeric algorithms
and complex number components that extend support for numeric
processing. The `valarray` component provides support for *n*-at-a-time
processing, potentially implemented as parallel operations on platforms
that support such processing. The random number component provides
facilities for generating pseudo-random numbers.

The input/output library (Clause  [[input.output]]) provides the
`iostream` components that are the primary mechanism for C++program
input and output. They can be used with other elements of the library,
particularly strings, locales, and iterators.

The regular expressions library (Clause  [[re]]) provides regular
expression matching and searching.

The atomic operations library (Clause  [[atomics]]) allows more
fine-grained concurrent access to shared data than is possible with
locks.

The thread support library (Clause  [[thread]]) provides components to
create and manage threads, including mutual exclusion and interthread
communication.

## The C standard library <a id="library.c">[[library.c]]</a>

The C++standard library also makes available the facilities of the C
standard library, suitably adjusted to ensure static type safety.

The descriptions of many library functions rely on the C standard
library for the signatures and semantics of those functions. In all such
cases, any use of the `restrict` qualifier shall be omitted.

## Definitions <a id="definitions">[[definitions]]</a>

#### 1 arbitrary-positional stream <a id="defns.arbitrary.stream">[defns.arbitrary.stream]</a>

a stream (described in Clause  [[input.output]]) that can seek to any
integral position within the length of the stream  
Every arbitrary-positional stream is also a repositional stream.

#### 2 block <a id="defns.block">[defns.block]</a>

place a thread in the blocked state

#### 3 blocked thread <a id="defns.blocked">[defns.blocked]</a>

a thread that is waiting for some condition (other than the availability
of a processor) to be satisfied before it can continue execution[^1]

#### 4 character <a id="defns.character">[defns.character]</a>

\<Clauses  [[strings]], [[localization]], [[input.output]], and 
[[re]]\> any object which, when treated sequentially, can represent
text  
The term does not mean only `char`, `char16_t`, `char32_t`, and
`wchar_t` objects, but any value that can be represented by a type that
provides the definitions specified in these Clauses.

#### 5 character container type <a id="defns.character.container">[defns.character.container]</a>

a class or a type used to represent a *character*  
It is used for one of the template parameters of the string, iostream,
and regular expression class templates. A character container type is a
POD ([[basic.types]]) type.

#### 6 comparison function <a id="defns.comparison">[defns.comparison]</a>

an operator function ([[over.oper]]) for any of the equality (
[[expr.eq]]) or relational ([[expr.rel]]) operators

#### 7 component <a id="defns.component">[defns.component]</a>

a group of library entities directly related as members, parameters, or
return types  
For example, the class template `basic_string` and the non-member
function templates that operate on strings are referred to as the
*string component*.

#### 8 deadlock <a id="defns.deadlock">[defns.deadlock]</a>

one or more threads are unable to continue execution because each is
blocked waiting for one or more of the others to satisfy some condition

#### 9 default behavior <a id="defns.default.behavior.impl">[defns.default.behavior.impl]</a>

\<implementation\> any specific behavior provided by the implementation,
within the scope of the *required behavior*

#### 10 default behavior <a id="defns.default.behavior.func">[defns.default.behavior.func]</a>

\<specification\> a description of *replacement function* and *handler
function* semantics

#### 11 handler function <a id="defns.handler">[defns.handler]</a>

a *non-reserved function* whose definition may be provided by a
C++program  
A C++program may designate a handler function at various points in its
execution by supplying a pointer to the function when calling any of the
library functions that install handler functions (Clause 
[[language.support]]).

#### 12 iostream class templates <a id="defns.iostream.templates">[defns.iostream.templates]</a>

templates, defined in Clause  [[input.output]], that take two template
arguments  
The arguments are named `charT` and `traits`. The argument `charT` is a
character container class, and the argument `traits` is a class which
defines additional characteristics and functions of the character type
represented by `charT` necessary to implement the iostream class
templates.

#### 13 modifier function <a id="defns.modifier">[defns.modifier]</a>

a class member function ([[class.mfct]]) other than a constructor,
assignment operator, or destructor that alters the state of an object of
the class

#### 14 move construction <a id="defns.move.constr">[defns.move.constr]</a>

direct-initialization of an object of some type with an rvalue of the
same type

#### 15 move assignment <a id="defns.move.assign">[defns.move.assign]</a>

assignment of an rvalue of some object type to a modifiable lvalue of
the same type

#### 16 object state <a id="defns.obj.state">[defns.obj.state]</a>

the current value of all non-static class members of an object (
[[class.mem]])  
The state of an object can be obtained by using one or more *observer
functions*.

#### 17 NTCTS <a id="defns.ntcts">[defns.ntcts]</a>

a sequence of values that have *character type* that precede the
terminating null character type value `charT()`

#### 18 observer function <a id="defns.observer">[defns.observer]</a>

a class member function ([[class.mfct]]) that accesses the state of an
object of the class but does not alter that state  
Observer functions are specified as `const` member functions (
[[class.this]]).

#### 19 referenceable type <a id="defns.referenceable">[defns.referenceable]</a>

An object type, a function type that does not have cv-qualifiers or a
*ref-qualifier*, or a reference type. The term describes a type to which
a reference can be created, including reference types.

#### 20 replacement function <a id="defns.replacement">[defns.replacement]</a>

a *non-reserved function* whose definition is provided by a C++program  
Only one definition for such a function is in effect for the duration of
the program’s execution, as the result of creating the program (
[[lex.phases]]) and resolving the definitions of all translation units (
[[basic.link]]).

#### 21 repositional stream <a id="defns.repositional.stream">[defns.repositional.stream]</a>

a stream (described in Clause  [[input.output]]) that can seek to a
position that was previously encountered

#### 22 required behavior <a id="defns.required.behavior">[defns.required.behavior]</a>

a description of *replacement function* and *handler function* semantics
applicable to both the behavior provided by the implementation and the
behavior of any such function definition in the program  
If such a function defined in a C++program fails to meet the required
behavior when it executes, the behavior is undefined.

#### 23 reserved function <a id="defns.reserved.function">[defns.reserved.function]</a>

a function, specified as part of the C++standard library, that must be
defined by the implementation  
If a C++program provides a definition for any reserved function, the
results are undefined.

#### 24 stable algorithm <a id="defns.stable">[defns.stable]</a>

an algorithm that preserves, as appropriate to the particular algorithm,
the order of elements  
Requirements for stable algorithms are given in  [[algorithm.stable]].

#### 25 traits class <a id="defns.traits">[defns.traits]</a>

a class that encapsulates a set of types and functions necessary for
class templates and function templates to manipulate objects of types
for which they are instantiated  
Traits classes defined in Clauses  [[strings]], [[localization]] and 
[[input.output]] are *character traits*, which provide the character
handling support needed by the string and iostream classes.

#### 26 unblock <a id="defns.unblock">[defns.unblock]</a>

place a thread in the unblocked state

#### 27 valid but unspecified state <a id="defns.valid">[defns.valid]</a>

an object state that is not specified except that the object’s
invariants are met and operations on the object behave as specified for
its type  
If an object `x` of type `std::vector<int>` is in a valid but
unspecified state, `x.empty()` can be called unconditionally, and
`x.front()` can be called only if `x.empty()` returns `false`.

## Additional definitions <a id="defns.additional">[[defns.additional]]</a>

[[intro.defs]] defines additional terms used elsewhere in this
International Standard.

## Method of description (Informative) <a id="description">[[description]]</a>

This subclause describes the conventions used to specify the C++standard
library. [[structure]] describes the structure of the normative Clauses 
[[support]] through  [[thread]] and Annex  [[depr]]. [[conventions]]
describes other editorial conventions.

### Structure of each clause <a id="structure">[[structure]]</a>

#### Elements <a id="structure.elements">[[structure.elements]]</a>

Each library clause contains the following elements, as applicable:[^2]

- Summary
- Requirements
- Detailed specifications
- References to the Standard C library

#### Summary <a id="structure.summary">[[structure.summary]]</a>

The Summary provides a synopsis of the category, and introduces the
first-level subclauses. Each subclause also provides a summary, listing
the headers specified in the subclause and the library entities provided
in each header.

Paragraphs labeled “Note(s):” or “Example(s):” are informative, other
paragraphs are normative.

The contents of the summary and the detailed specifications include:

- macros
- values
- types
- classes and class templates
- functions and function templates
- objects

#### Requirements <a id="structure.requirements">[[structure.requirements]]</a>

Requirements describe constraints that shall be met by a C++program that
extends the standard library. Such extensions are generally one of the
following:

- Template arguments
- Derived classes
- Containers, iterators, and algorithms that meet an interface
  convention

The string and iostream components use an explicit representation of
operations required of template arguments. They use a class template
`char_traits` to define these constraints.

Interface convention requirements are stated as generally as possible.
Instead of stating “class X has to define a member function
`operator++()`,” the interface requires “for any object `x` of class
`X`, `++x` is defined.” That is, whether the operator is a member is
unspecified.

Requirements are stated in terms of well-defined expressions that define
valid terms of the types that satisfy the requirements. For every set of
well-defined expression requirements there is a table that specifies an
initial set of the valid expressions and their semantics. Any generic
algorithm (Clause  [[algorithms]]) that uses the well-defined expression
requirements is described in terms of the valid expressions for its
template type parameters.

Template argument requirements are sometimes referenced by name. See 
[[type.descriptions]].

In some cases the semantic requirements are presented as C++code. Such
code is intended as a specification of equivalence of a construct to
another construct, not necessarily as the way the construct must be
implemented.[^3]

#### Detailed specifications <a id="structure.specifications">[[structure.specifications]]</a>

The detailed specifications each contain the following elements:

- name and brief description
- synopsis (class definition or function prototype, as appropriate)
- restrictions on template arguments, if any
- description of class invariants
- description of function semantics

Descriptions of class member functions follow the order (as
appropriate):[^4]

- constructor(s) and destructor
- copying, moving & assignment functions
- comparison functions
- modifier functions
- observer functions
- operators and other non-member functions

Descriptions of function semantics contain the following elements (as
appropriate):[^5]

- *Requires:* the preconditions for calling the function
- *Effects:* the actions performed by the function
- *Synchronization:* the synchronization operations (
  [[intro.multithread]]) applicable to the function
- *Postconditions:* the observable results established by the function
- *Returns:* a description of the value(s) returned by the function
- *Throws:* any exceptions thrown by the function, and the conditions
  that would cause the exception
- *Complexity:* the time and/or space complexity of the function
- *Remarks:* additional semantic constraints on the function
- *Error conditions:* the error conditions for error codes reported by
  the function.
- *Notes:* non-normative comments about the function

Whenever the *Effects:* element specifies that the semantics of some
function `F` are *Equivalent to* some code sequence, then the various
elements are interpreted as follows. If `F`’s semantics specifies a
*Requires:* element, then that requirement is logically imposed prior to
the *equivalent-to* semantics. Next, the semantics of the code sequence
are determined by the *Requires:* , *Effects:* , *Postconditions:* ,
*Returns:* , *Throws:* , *Complexity:* , *Remarks:* , *Error
conditions:* , and *Notes:* specified for the function invocations
contained in the code sequence. The value returned from `F` is specified
by `F`’s *Returns:* element, or if `F` has no *Returns:* element, a
non-`void` return from `F` is specified by the *Returns:* elements in
the code sequence. If `F`’s semantics contains a *Throws:* ,
*Postconditions:* , or *Complexity:* element, then that supersedes any
occurrences of that element in the code sequence.

For non-reserved replacement and handler functions, Clause 
[[language.support]] specifies two behaviors for the functions in
question: their required and default behavior. The *default behavior*
describes a function definition provided by the implementation. The
*required behavior* describes the semantics of a function definition
provided by either the implementation or a C++program. Where no
distinction is explicitly made in the description, the behavior
described is the required behavior.

If the formulation of a complexity requirement calls for a negative
number of operations, the actual requirement is zero operations.[^6]

Complexity requirements specified in the library clauses are upper
bounds, and implementations that provide better complexity guarantees
satisfy the requirements.

Error conditions specify conditions where a function may fail. The
conditions are listed, together with a suitable explanation, as the
`enum class errc` constants ([[syserr]]).

#### C library <a id="structure.see.also">[[structure.see.also]]</a>

Paragraphs labeled “” contain cross-references to the relevant portions
of this International Standard and the ISO C standard, which is
incorporated into this International Standard by reference.

### Other conventions <a id="conventions">[[conventions]]</a>

This subclause describes several editorial conventions used to describe
the contents of the C++standard library. These conventions are for
describing implementation-defined types ([[type.descriptions]]), and
member functions ([[functions.within.classes]]).

#### Type descriptions <a id="type.descriptions">[[type.descriptions]]</a>

##### General <a id="type.descriptions.general">[[type.descriptions.general]]</a>

The Requirements subclauses may describe names that are used to specify
constraints on template arguments.[^7] These names are used in library
Clauses to describe the types that may be supplied as arguments by a
C++program when instantiating template components from the library.

Certain types defined in Clause  [[input.output]] are used to describe
implementation-defined types. They are based on other types, but with
added constraints.

##### Enumerated types <a id="enumerated.types">[[enumerated.types]]</a>

Several types defined in Clause  [[input.output]] are *enumerated
types*. Each enumerated type may be implemented as an enumeration or as
a synonym for an enumeration.[^8]

The enumerated type *enumerated* can be written:

``` cpp
enum enumerated { V0, V1, V2, V3, ..... };

static const enumerated C0 (V0);
static const enumerated C1 (V1);
static const enumerated C2 (V2);
static const enumerated C3 (V3);
  .....
```

Here, the names *C0*, *C1*, etc. represent *enumerated elements* for
this particular enumerated type. All such elements have distinct values.

##### Bitmask types <a id="bitmask.types">[[bitmask.types]]</a>

Several types defined in Clauses  [[support]] through  [[thread]] and
Annex  [[depr]] are *bitmask types*. Each bitmask type can be
implemented as an enumerated type that overloads certain operators, as
an integer type, or as a `bitset` ([[template.bitset]]).

The bitmask type *bitmask* can be written:

``` cpp
// For exposition only.
// int_type is an integral type capable of
// representing all values of the bitmask type.
enum bitmask : int_type {
  V0 = 1 << 0, V1 = 1 << 1, V2 = 1 << 2, V3 = 1 << 3, .....
};

constexpr bitmask C0(V0{});
constexpr bitmask C1(V1{});
constexpr bitmask C2(V2{});
constexpr bitmask C3(V3{});
  .....

constexpr bitmask{} operator&(bitmask{} X, bitmask{} Y) {
  return static_cast<bitmask{}>(
    static_cast<int_type>(X) & static_cast<int_type>(Y));
}
constexpr bitmask{} operator|(bitmask{} X, bitmask{} Y) {
  return static_cast<bitmask{}>(
    static_cast<int_type>(X) | static_cast<int_type>(Y));
}
constexpr bitmask{} operator^(bitmask{} X, bitmask{} Y){
  return static_cast<bitmask{}>(
    static_cast<int_type>(X) ^ static_cast<int_type>(Y));
}
constexpr bitmask{} operator~(bitmask{} X){
  return static_cast<bitmask{}>(~static_cast<int_type>(X));
}
bitmask{}& operator&=(bitmask{}& X, bitmask{} Y){
  X = X & Y; return X;
}
bitmask{}& operator|=(bitmask{}& X, bitmask{} Y) {
  X = X | Y; return X;
}
bitmask{}& operator^=(bitmask{}& X, bitmask{} Y) {
  X = X ^ Y; return X;
}
```

Here, the names *C0*, *C1*, etc. represent *bitmask elements* for this
particular bitmask type. All such elements have distinct, nonzero values
such that, for any pair *Ci* and *Cj* where *i* != *j*, *Ci* & *Ci* is
nonzero and *Ci* & *Cj* is zero. Additionally, the value 0 is used to
represent an *empty bitmask*, in which no bitmask elements are set.

The following terms apply to objects and values of bitmask types:

- To *set* a value *Y* in an object *X* is to evaluate the expression
  *X* `|=` *Y*.
- To *clear* a value *Y* in an object *X* is to evaluate the expression
  *X* `&= ~`*Y*.
- The value *Y* *is set* in the object *X* if the expression *X* `&` *Y*
  is nonzero.

##### Character sequences <a id="character.seq">[[character.seq]]</a>

The C standard library makes widespread use of characters and character
sequences that follow a few uniform conventions:

- A *letter* is any of the 26 lowercase or 26 uppercase letters in the
  basic execution character set.[^9]
- The *decimal-point character* is the (single-byte) character used by
  functions that convert between a (single-byte) character sequence and
  a value of one of the floating-point types. It is used in the
  character sequence to denote the beginning of a fractional part. It is
  represented in Clauses  [[support]] through  [[thread]] and Annex 
  [[depr]] by a period, `'.'`, which is also its value in the `"C"`
  locale, but may change during program execution by a call to
  `setlocale(int, const char*)`,[^10] or by a change to a `locale`
  object, as described in Clauses  [[locales]] and  [[input.output]].
- A *character sequence* is an array object ([[dcl.array]]) *A* that
  can be declared as `T A[N]`, where *T* is any of the types `char`,
  `unsigned char`, or `signed char` ([[basic.fundamental]]), optionally
  qualified by any combination of `const` or `volatile`. The initial
  elements of the array have defined contents up to and including an
  element determined by some predicate. A character sequence can be
  designated by a pointer value *S* that points to its first element.

###### Byte strings <a id="byte.strings">[[byte.strings]]</a>

A *null-terminated byte string*, or NTBS, is a character sequence whose
highest-addressed element with defined content has the value zero (the
*terminating null* character); no other element in the sequence has the
value zero. [^11]

The *length* of an NTBS is the number of elements that precede the
terminating null character. An *empty* NTBS has a length of zero.

The *value* of an NTBS is the sequence of values of the elements up to
and including the terminating null character.

A *static* NTBS is an NTBSwith static storage duration.[^12]

###### Multibyte strings <a id="multibyte.strings">[[multibyte.strings]]</a>

A *null-terminated multibyte string,* or NTMBS, is an NTBSthat
constitutes a sequence of valid multibyte characters, beginning and
ending in the initial shift state.[^13]

A *static* NTMBS is an NTMBSwith static storage duration.

#### Functions within classes <a id="functions.within.classes">[[functions.within.classes]]</a>

For the sake of exposition, Clauses  [[support]] through  [[thread]] and
Annex  [[depr]] do not describe copy/move constructors, assignment
operators, or (non-virtual) destructors with the same apparent semantics
as those that can be generated by default ([[class.ctor]],
[[class.dtor]], [[class.copy]]).

It is unspecified whether the implementation provides explicit
definitions for such member function signatures, or for virtual
destructors that can be generated by default.

#### Private members <a id="objects.within.classes">[[objects.within.classes]]</a>

Clauses  [[support]] through  [[thread]] and Annex  [[depr]] do not
specify the representation of classes, and intentionally omit
specification of class members ([[class.mem]]). An implementation may
define static or non-static class members, or both, as needed to
implement the semantics of the member functions specified in Clauses 
[[support]] through  [[thread]] and Annex  [[depr]].

Objects of certain classes are sometimes required by the external
specifications of their classes to store data, apparently in member
objects. For the sake of exposition, some subclauses provide
representative declarations, and semantic requirements, for private
member objects of classes that meet the external specifications of the
classes. The declarations for such member objects and the definitions of
related member types are followed by a comment that ends with
*exposition only*, as in:

``` cpp
streambuf* sb;  // exposition only
```

An implementation may use any technique that provides equivalent
external behavior.

## Library-wide requirements <a id="requirements">[[requirements]]</a>

This subclause specifies requirements that apply to the entire
C++standard library. Clauses  [[support]] through  [[thread]] and Annex 
[[depr]] specify the requirements of individual entities within the
library.

Requirements specified in terms of interactions between threads do not
apply to programs having only a single thread of execution.

Within this subclause, [[organization]] describes the library’s contents
and organization, [[using]] describes how well-formed C++programs gain
access to library entities, [[utility.requirements]] describes
constraints on types and functions used with the C++standard library,
[[constraints]] describes constraints on well-formed C++programs, and
[[conforming]] describes constraints on conforming implementations.

### Library contents and organization <a id="organization">[[organization]]</a>

[[contents]] describes the entities defined in the C++standard library.
[[headers]] lists the standard library headers and some constraints on
those headers. [[compliance]] lists requirements for a freestanding
implementation of the C++ standard library.

#### Library contents <a id="contents">[[contents]]</a>

The C++standard library provides definitions for the following types of
entities: macros, values, types, templates, classes, functions, objects.

All library entities except macros, `operator new` and `operator delete`
are defined within the namespace `std` or namespaces nested within
namespace `std`.[^14] It is unspecified whether names declared in a
specific namespace are declared directly in that namespace or in an
inline namespace inside that namespace.[^15]

Whenever a name `x` defined in the standard library is mentioned, the
name `x` is assumed to be fully qualified as `::std::x`, unless
explicitly described otherwise. For example, if the Effects section for
library function `F` is described as calling library function `G`, the
function `::std::G` is meant.

#### Headers <a id="headers">[[headers]]</a>

Each element of the C++standard library is declared or defined (as
appropriate) in a *header*.[^16]

The C++standard library provides 53 *C++library headers*, as shown in
Table  [[tab:cpp.library.headers]].

**Table: C++library headers**

|                        |                      |             |                      |                   |
| ---------------------- | -------------------- | ----------- | -------------------- | ----------------- |
| `<algorithm>`          | `<fstream>`          | `<list>`    | `<regex>`            | `<tuple>`         |
| `<array>`              | `<functional>`       | `<locale>`  | `<scoped_allocator>` | `<type_traits>`   |
| `<atomic>`             | `<future>`           | `<map>`     | `<set>`              | `<typeindex>`     |
| `<bitset>`             | `<initializer_list>` | `<memory>`  | `<sstream>`          | `<typeinfo>`      |
| `<chrono>`             | `<iomanip>`          | `<mutex>`   | `<stack>`            | `<unordered_map>` |
| `<codecvt>`            | `<ios>`              | `<new>`     | `<stdexcept>`        | `<unordered_set>` |
| `<complex>`            | `<iosfwd>`           | `<numeric>` | `<streambuf>`        | `<utility>`       |
| `<condition_variable>` | `<iostream>`         | `<ostream>` | `<string>`           | `<valarray>`      |
| `<deque>`              | `<istream>`          | `<queue>`   | `<strstream>`        | `<vector>`        |
| `<exception>`          | `<iterator>`         | `<random>`  | `<system_error>`     |                   |
| `<forward_list>`       | `<limits>`           | `<ratio>`   | `<thread>`           |                   |


The facilities of the C standard Library are provided in 26 additional
headers, as shown in Table  [[tab:cpp.c.headers]].

**Table: C++headers for C library facilities**

|              |               |               |             |             |
| ------------ | ------------- | ------------- | ----------- | ----------- |
| `<cassert>`  | `<cinttypes>` | `<csignal>`   | `<cstdio>`  | `<cwchar>`  |
| `<ccomplex>` | `<ciso646>`   | `<cstdalign>` | `<cstdlib>` | `<cwctype>` |
| `<cctype>`   | `<climits>`   | `<cstdarg>`   | `<cstring>` |             |
| `<cerrno>`   | `<clocale>`   | `<cstdbool>`  | `<ctgmath>` |             |
| `<cfenv>`    | `<cmath>`     | `<cstddef>`   | `<ctime>`   |             |
| `<cfloat>`   | `<csetjmp>`   | `<cstdint>`   | `<cuchar>`  |             |


Except as noted in Clauses  [[support]] through  [[thread]] and Annex 
[[depr]], the contents of each header `cname` shall be the same as that
of the corresponding header `name.h`, as specified in the C standard
library ([[intro.refs]]) or the C Unicode TR, as appropriate, as if by
inclusion. In the C++standard library, however, the declarations (except
for names which are defined as macros in C) are within namespace scope (
[[basic.scope.namespace]]) of the namespace `std.` It is unspecified
whether these names are first declared within the global namespace scope
and are then injected into namespace `std` by explicit
*using-declaration*s ([[namespace.udecl]]).

Names which are defined as macros in C shall be defined as macros in the
C++ standard library, even if C grants license for implementation as
functions. The names defined as macros in C include the following:
`assert`, `offsetof`, `setjmp`, `va_arg`, `va_end`, and `va_start`.

Names that are defined as functions in C shall be defined as functions
in the C++standard library.[^17]

Identifiers that are keywords or operators in C++shall not be defined as
macros in C++standard library headers.[^18]

[[depr.c.headers]], C standard library headers, describes the effects of
using the `name.h` (C header) form in a C++program.[^19]

#### Freestanding implementations <a id="compliance">[[compliance]]</a>

Two kinds of implementations are defined: *hosted* and *freestanding* (
[[intro.compliance]]). For a hosted implementation, this International
Standard describes the set of available headers.

A freestanding implementation has an *implementation-defined* set of
headers. This set shall include at least the headers shown in Table 
[[tab:cpp.headers.freestanding]].

**Table: C++headers for freestanding implementations**

| Subclause              |                           | Header                                 |
| ---------------------- | ------------------------- | -------------------------------------- |
|                        |                           | `<ciso646>`                            |
| [[support.types]]      | Types                     | `<cstddef>`                            |
| [[support.limits]]     | Implementation properties | `<cfloat>` `<limits>` `<climits>`      |
| [[cstdint]]            | Integer types             | `<cstdint>`                            |
| [[support.start.term]] | Start and termination     | `<cstdlib>`                            |
| [[support.dynamic]]    | Dynamic memory management | `<new>`                                |
| [[support.rtti]]       | Type identification       | `<typeinfo>`                           |
| [[support.exception]]  | Exception handling        | `<exception>`                          |
| [[support.initlist]]   | Initializer lists         | `<initializer_list>`                   |
| [[support.runtime]]    | Other runtime support     | `<cstdalign>` `<cstdarg>` `<cstdbool>` |
| [[meta]]               | Type traits               | `<type_traits>`                        |
| [[atomics]]            | Atomics                   | `<atomic>`                             |


The supplied version of the header `<cstdlib>` shall declare at least
the functions `abort`, `atexit`, `at_quick_exit`, `exit`, and
`quick_exit` ([[support.start.term]]). The other headers listed in this
table shall meet the same requirements as for a hosted implementation.

### Using the library <a id="using">[[using]]</a>

#### Overview <a id="using.overview">[[using.overview]]</a>

This section describes how a C++program gains access to the facilities
of the C++standard library. [[using.headers]] describes effects during
translation phase 4, while  [[using.linkage]] describes effects during
phase 8 ([[lex.phases]]).

#### Headers <a id="using.headers">[[using.headers]]</a>

The entities in the C++standard library are defined in headers, whose
contents are made available to a translation unit when it contains the
appropriate `#include` preprocessing directive ([[cpp.include]]).

A translation unit may include library headers in any order (Clause 
[[lex]]). Each may be included more than once, with no effect different
from being included exactly once, except that the effect of including
either `<cassert>` or `<assert.h>` depends each time on the lexically
current definition of `NDEBUG`.[^20]

A translation unit shall include a header only outside of any external
declaration or definition, and shall include the header lexically before
the first reference in that translation unit to any of the entities
declared in that header. No diagnostic is required.

#### Linkage <a id="using.linkage">[[using.linkage]]</a>

Entities in the C++standard library have external linkage (
[[basic.link]]). Unless otherwise specified, objects and functions have
the default `extern "C++"` linkage ([[dcl.link]]).

Whether a name from the C standard library declared with external
linkage has `extern "C"` or `extern "C++"` linkage is
*implementation-defined*. It is recommended that an implementation use
`extern "C++"` linkage for this purpose.[^21]

Objects and functions defined in the library and required by a
C++program are included in the program prior to program startup.

replacement functions ([[replacement.functions]]), run-time changes (
[[handler.functions]]).

### Requirements on types and expressions <a id="utility.requirements">[[utility.requirements]]</a>

[[utility.arg.requirements]] describes requirements on types and
expressions used to instantiate templates defined in the C++standard
library. [[swappable.requirements]] describes the requirements on
swappable types and swappable expressions.
[[nullablepointer.requirements]] describes the requirements on
pointer-like types that support null values. [[hash.requirements]]
describes the requirements on hash function objects.
[[allocator.requirements]] describes the requirements on storage
allocators.

#### Template argument requirements <a id="utility.arg.requirements">[[utility.arg.requirements]]</a>

The template definitions in the C++standard library refer to various
named requirements whose details are set out in tables 
[[equalitycomparable]]– [[destructible]]. In these tables, `T` is an
object or reference type to be supplied by a C++program instantiating a
template; `a`, `b`, and `c` are values of type (possibly `const`) `T`;
`s` and `t` are modifiable lvalues of type `T`; `u` denotes an
identifier; `rv` is an rvalue of type `T`; and `v` is an lvalue of type
(possibly `const`) `T` or an rvalue of type `const T`.

In general, a default constructor is not required. Certain container
class member function signatures specify `T()` as a default argument.
`T()` shall be a well-defined expression ([[dcl.init]]) if one of those
signatures is called using the default argument ([[dcl.fct.default]]).

**Table: `EqualityComparable` requirements**

|          |                       |                                                                                                                                                                          |
| -------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `a == b` | convertible to `bool` | `==` is an equivalence relation, that is, it has the following properties: For all `a`, `a == a`.; If `a == b`, then `b == a`.; If `a == b` and `b == c`, then `a == c`. |

**Table: `LessThanComparable` requirements**

|         |                       |                                                           |
| ------- | --------------------- | --------------------------------------------------------- |
| `a < b` | convertible to `bool` | `<` is a strict weak ordering relation~([[alg.sorting]]) |

**Table: `DefaultConstructible` requirements**

|          |                                                     |
| -------- | --------------------------------------------------- |
| `T t;`   | object `t` is default-initialized                   |
| `T u{};` | object `u` is value-initialized                     |
| `T()`    | a temporary object of type `T` is value-initialized |
| `T{}`    |                                                     |

**Table: `MoveConstructible` requirements**

|             |                                                                    |
| ----------- | ------------------------------------------------------------------ |
| `T u = rv;` | `u` is equivalent to the value of `rv` before the construction     |
| `T(rv)`     | `T(rv)` is equivalent to the value of `rv` before the construction |
| *[spans 2 columns]*  `rv`'s state is unspecified \enternote `rv` must still meet the requirements of the library component that is using it. The operations listed in those requirements must work as specified whether `rv` has been moved from or not. \exitnote |

**Table: `CopyConstructible` requirements (in addition to `MoveConstructible`)**

|            |                                                           |
| ---------- | --------------------------------------------------------- |
| `T u = v;` | the value of `v` is unchanged and is equivalent to ` u`   |
| `T(v)`     | the value of `v` is unchanged and is equivalent to `T(v)` |

**Table: `MoveAssignable` requirements**

|          |      |     |                                                              |
| -------- | ---- | --- | ------------------------------------------------------------ |
| `t = rv` | `T&` | `t` | `t` is equivalent to the value of `rv` before the assignment |
| *[spans 4 columns]*  `rv`'s state is unspecified. \enternote\ `rv` must still meet the requirements of the library component that is using it. The operations listed in those requirements must work as specified whether `rv` has been moved from or not. \exitnote |

**Table: `CopyAssignable` requirements (in addition to `MoveAssignable`)**

|         |      |     |                                                         |
| ------- | ---- | --- | ------------------------------------------------------- |
| `t = v` | `T&` | `t` | `t` is equivalent to `v`, the value of `v` is unchanged |


**Table: `Destructible` requirements**

|          |                                                                       |
| -------- | --------------------------------------------------------------------- |
| `u.~T()` | All resources owned by `u` are reclaimed, no exception is propagated. |


#### `Swappable` requirements <a id="swappable.requirements">[[swappable.requirements]]</a>

This subclause provides definitions for swappable types and expressions.
In these definitions, let `t` denote an expression of type `T`, and let
`u` denote an expression of type `U`.

An object `t` is *swappable with* an object `u` if and only if:

- the expressions `swap(t, u)` and `swap(u, t)` are valid when evaluated
  in the context described below, and
- these expressions have the following effects:
  - the object referred to by `t` has the value originally held by `u`
    and
  - the object referred to by `u` has the value originally held by `t`.

The context in which `swap(t, u)` and `swap(u, t)` are evaluated shall
ensure that a binary non-member function named “swap” is selected via
overload resolution ([[over.match]]) on a candidate set that includes:

- the two `swap` function templates defined in `<utility>` (
  [[utility]]) and
- the lookup set produced by argument-dependent lookup (
  [[basic.lookup.argdep]]).

If `T` and `U` are both fundamental types or arrays of fundamental types
and the declarations from the header `<utility>` are in scope, the
overall lookup set described above is equivalent to that of the
qualified name lookup applied to the expression `std::swap(t, u)` or
`std::swap(u, t)` as appropriate.

It is unspecified whether a library component that has a swappable
requirement includes the header `<utility>` to ensure an appropriate
evaluation context.

An rvalue or lvalue `t` is *swappable* if and only if `t` is swappable
with any rvalue or lvalue, respectively, of type `T`.

A type `X` satisfying any of the iterator requirements (
[[iterator.requirements]]) satisfies the requirements of
`ValueSwappable` if, for any dereferenceable object `x` of type `X`,
`*x` is swappable.

User code can ensure that the evaluation of `swap` calls is performed in
an appropriate context under the various conditions as follows:

``` cpp
#include <utility>

// Requires: std::forward<T>(t) shall be swappable with std::forward<U>(u).
template <class T, class U>
void value_swap(T&& t, U&& u) {
  using std::swap;
  swap(std::forward<T>(t), std::forward<U>(u)); // OK: uses ``swappable with'' conditions
                                                // for rvalues and lvalues
}

// Requires: lvalues of T shall be swappable.
template <class T>
void lv_swap(T& t1 T& t2) {
  using std::swap;
  swap(t1, t2);                                 // OK: uses swappable conditions for
}                                               // lvalues of type T

namespace N {
  struct A { int m; };
  struct Proxy { A* a; };
  Proxy proxy(A& a) { return Proxy{ &a }; }

  void swap(A& x, Proxy p) {
    std::swap(x.m, p.a->m);                     // OK: uses context equivalent to swappable
                                                // conditions for fundamental types
  }
  void swap(Proxy p, A& x) { swap(x, p); }      // satisfy symmetry constraint
}

int main() {
  int i = 1, j = 2;
  lv_swap(i, j);
  assert(i == 2 && j == 1);

  N::A a1 = { 5 }, a2 = { -5 };
  value_swap(a1, proxy(a2));
  assert(a1.m == -5 && a2.m == 5);
}
```

#### `NullablePointer` requirements <a id="nullablepointer.requirements">[[nullablepointer.requirements]]</a>

A `NullablePointer` type is a pointer-like type that supports null
values. A type `P` meets the requirements of `NullablePointer` if:

- `P` satisfies the requirements of `EqualityComparable`,
  `DefaultConstructible`, `CopyConstructible`, `CopyAssignable`, and
  `Destructible`,
- lvalues of type `P` are swappable ([[swappable.requirements]]),
- the expressions shown in Table  [[nullablepointer]] are valid and have
  the indicated semantics, and
- `P` satisfies all the other requirements of this subclause.

A value-initialized object of type `P` produces the null value of the
type. The null value shall be equivalent only to itself. A
default-initialized object of type `P` may have an indeterminate value.
Operations involving indeterminate values may cause undefined behavior.

An object `p` of type `P` can be contextually converted to `bool`
(Clause  [[conv]]). The effect shall be as if `p != nullptr` had been
evaluated in place of `p`.

No operation which is part of the `NullablePointer` requirements shall
exit via an exception.

In Table  [[nullablepointer]], `u` denotes an identifier, `t` denotes a
non-`const` lvalue of type `P`, `a` and `b` denote values of type
(possibly `const`) `P`, and `np` denotes a value of type (possibly
`const`) `std::nullptr_t`.

**Table: `NullablePointer` requirements**

|                |                                    |                          |
| -------------- | ---------------------------------- | ------------------------ |
| `P u(np);`<br> |                                    | post: `u == nullptr`     |
| `P u = np;`    |                                    |                          |
| `P(np)`        |                                    | post: `P(np) == nullptr` |
| `t = np`       | `P&`                               | post: `t == nullptr`     |
| `a != b`       | contextually convertible to `bool` | `!(a == b)`              |
| `a == np`      | contextually convertible to `bool` | `a == P()`               |
| `np == a`      |                                    |                          |
| `a != np`      | contextually convertible to `bool` | `!(a == np)`             |
| `np != a`      |                                    |                          |


#### Hash requirements <a id="hash.requirements">[[hash.requirements]]</a>

A type `H` meets the `Hash` requirements if:

- it is a function object type ([[function.objects]]),
- it satisfies the requirements of `CopyConstructible` and
  `Destructible` ([[utility.arg.requirements]]), and
- the expressions shown in Table  [[hash]] are valid and have the
  indicated semantics.

Given `Key` is an argument type for function objects of type `H`, in
Table  [[hash]] `h` is a value of type (possibly `const`) `H`, `u` is an
lvalue of type `Key`, and `k` is a value of a type convertible to
(possibly `const`) `Key`.

**Table: `Hash` requirements**

|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `h(k)` | `size_t` | The value returned shall depend only on the argument `k` for the duration of the program. \enternote Thus all evaluations of the expression `h(k)` with the same value for `k` yield the same result for a given execution of the program. \exitnote \enternote For two different values `t1` and `t2`, the probability that `h(t1)` and `h(t2)` compare equal should be very small, approaching `1.0 / numeric_limits<size_t>::max()`. \exitnote |
| `h(u)` | `size_t` | Shall not modify `u`.                                                                                                                                                                                                                                                                                                                                                                                                                             |


#### Allocator requirements <a id="allocator.requirements">[[allocator.requirements]]</a>

The library describes a standard set of requirements for *allocators*,
which are class-type objects that encapsulate the information about an
allocation model. This information includes the knowledge of pointer
types, the type of their difference, the type of the size of objects in
this allocation model, as well as the memory allocation and deallocation
primitives for it. All of the string types (Clause  [[strings]]),
containers (Clause  [[containers]]) (except array), string buffers and
string streams (Clause  [[input.output]]), and `match_results` (Clause 
[[re]]) are parameterized in terms of allocators.

The template struct `allocator_traits` ([[allocator.traits]]) supplies
a uniform interface to all allocator types. Table  [[tab:desc.var.def]]
describes the types manipulated through allocators. Table 
[[tab:utilities.allocator.requirements]] describes the requirements on
allocator types and thus on types used to instantiate
`allocator_traits`. A requirement is optional if the last column of
Table  [[tab:utilities.allocator.requirements]] specifies a default for
a given expression. Within the standard library `allocator_traits`
template, an optional requirement that is not supplied by an allocator
is replaced by the specified default expression. A user specialization
of `allocator_traits` may provide different defaults and may provide
defaults for different requirements than the primary template. Within
Tables  [[tab:desc.var.def]] and 
[[tab:utilities.allocator.requirements]], the use of `move` and
`forward` always refers to `std::move` and `std::forward`, respectively.

Note A: The member class template `rebind` in the table above is
effectively a typedef template. In general, if the name `Allocator` is
bound to `SomeAllocator<T>`, then `Allocator::rebind<U>::other` is the
same type as `SomeAllocator<U>`, where `SomeAllocator<T>::value_type` is
`T` and `SomeAllocator<U>::{}value_type` is `U`. If `Allocator` is a
class template instantiation of the form `SomeAllocator<T, Args>`, where
`Args` is zero or more type arguments, and `Allocator` does not supply a
`rebind` member template, the standard `allocator_traits` template uses
`SomeAllocator<U, Args>` in place of `Allocator::{}rebind<U>::other` by
default. For allocator types that are not template instantiations of the
above form, no default is provided.

An allocator type `X` shall satisfy the requirements of
`CopyConstructible` ([[utility.arg.requirements]]). The `X::pointer`,
`X::const_pointer`, `X::void_pointer`, and `X::const_void_pointer` types
shall satisfy the requirements of `NullablePointer` (
[[nullablepointer.requirements]]). No constructor, comparison operator,
copy operation, move operation, or swap operation on these types shall
exit via an exception. `X::pointer` and `X::const_pointer` shall also
satisfy the requirements for a random access iterator (
[[iterator.requirements]]).

Let `x1` and `x2` denote objects of (possibly different) types
`X::void_pointer`, `X::const_void_pointer`, `X::pointer`, or
`X::const_pointer`. Then, `x1` and `x2` are *equivalently-valued*
pointer values, if and only if both `x1` and `x2` can be explicitly
converted to the two corresponding objects `px1` and `px2` of type
`X::const_pointer`, using a sequence of `static_cast`s using only these
four types, and the expression `px1 == px2` evaluates to `true`.

Let `w1` and `w2` denote objects of type `X::void_pointer`. Then for the
expressions

``` cpp
w1 == w2
w1 != w2
```

either or both objects may be replaced by an equivalently-valued object
of type `X::const_void_pointer` with no change in semantics.

Let `p1` and `p2` denote objects of type `X::pointer`. Then for the
expressions

``` cpp
p1 == p2
p1 != p2
p1 < p2
p1 <= p2
p1 >= p2
p1 > p2
p1 - p2
```

either or both objects may be replaced by an equivalently-valued object
of type `X::const_pointer` with no change in semantics.

An allocator may constrain the types on which it can be instantiated and
the arguments for which its `construct` member may be called. If a type
cannot be used with a particular allocator, the allocator class or the
call to `construct` may fail to instantiate.

the following is an allocator class template supporting the minimal
interface that satisfies the requirements of Table 
[[tab:utilities.allocator.requirements]]:

``` cpp
template <class Tp>
struct SimpleAllocator {
  typedef Tp value_type;
  SimpleAllocator(ctor args);

  template <class T> SimpleAllocator(const SimpleAllocator<T>& other);

  Tp* allocate(std::size_t n);
  void deallocate(Tp* p, std::size_t n);
};

template <class T, class U>
bool operator==(const SimpleAllocator<T>&, const SimpleAllocator<U>&);
template <class T, class U>
bool operator!=(const SimpleAllocator<T>&, const SimpleAllocator<U>&);
```

If the alignment associated with a specific over-aligned type is not
supported by an allocator, instantiation of the allocator for that type
may fail. The allocator also may silently ignore the requested
alignment. Additionally, the member function `allocate` for that type
may fail by throwing an object of type `std::bad_alloc`.

### Constraints on programs <a id="constraints">[[constraints]]</a>

#### Overview <a id="constraints.overview">[[constraints.overview]]</a>

This section describes restrictions on C++programs that use the
facilities of the C++standard library. The following subclauses specify
constraints on the program’s use of namespaces ([[namespace.std]]), its
use of various reserved names ([[reserved.names]]), its use of
headers ([[alt.headers]]), its use of standard library classes as base
classes ([[derived.classes]]), its definitions of replacement
functions ([[replacement.functions]]), and its installation of handler
functions during execution ([[handler.functions]]).

#### Namespace use <a id="namespace.constraints">[[namespace.constraints]]</a>

##### Namespace `std` <a id="namespace.std">[[namespace.std]]</a>

The behavior of a C++program is undefined if it adds declarations or
definitions to namespace `std` or to a namespace within namespace `std`
unless otherwise specified. A program may add a template specialization
for any standard library template to namespace `std` only if the
declaration depends on a user-defined type and the specialization meets
the standard library requirements for the original template and is not
explicitly prohibited.[^22]

The behavior of a C++program is undefined if it declares

- an explicit specialization of any member function of a standard
  library class template, or
- an explicit specialization of any member function template of a
  standard library class or class template, or
- an explicit or partial specialization of any member class template of
  a standard library class or class template.

A program may explicitly instantiate a template defined in the standard
library only if the declaration depends on the name of a user-defined
type and the instantiation meets the standard library requirements for
the original template.

A translation unit shall not declare namespace `std` to be an inline
namespace ([[namespace.def]]).

##### Namespace `posix` <a id="namespace.posix">[[namespace.posix]]</a>

The behavior of a C++program is undefined if it adds declarations or
definitions to namespace `posix` or to a namespace within namespace
`posix` unless otherwise specified. The namespace `posix` is reserved
for use by ISO/IEC 9945 and other POSIX standards.

#### Reserved names <a id="reserved.names">[[reserved.names]]</a>

The C++standard library reserves the following kinds of names:

- macros
- global names
- names with external linkage

If a program declares or defines a name in a context where it is
reserved, other than as explicitly allowed by this Clause, its behavior
is undefined.

##### Macro names <a id="macro.names">[[macro.names]]</a>

A translation unit that includes a standard library header shall not
`#define` or `#undef` names declared in any standard library header.

A translation unit shall not `#define` or `#undef` names lexically
identical to keywords, to the identifiers listed in Table 
[[tab:identifiers.special]], or to the *attribute-token*s described in 
[[dcl.attr]].

##### Global names <a id="global.names">[[global.names]]</a>

Certain sets of names and function signatures are always reserved to the
implementation:

- Each name that contains a double underscore `__` or begins with an
  underscore followed by an uppercase letter ([[lex.key]]) is reserved
  to the implementation for any use.
- Each name that begins with an underscore is reserved to the
  implementation for use as a name in the global namespace.

##### External linkage <a id="extern.names">[[extern.names]]</a>

Each name declared as an object with external linkage in a header is
reserved to the implementation to designate that library object with
external linkage, [^23] both in namespace `std` and in the global
namespace.

Each global function signature declared with external linkage in a
header is reserved to the implementation to designate that function
signature with external linkage. [^24]

Each name from the Standard C library declared with external linkage is
reserved to the implementation for use as a name with `extern "C"`
linkage, both in namespace std and in the global namespace.

Each function signature from the Standard C library declared with
external linkage is reserved to the implementation for use as a function
signature with both `extern "C"` and `extern "C++"` linkage, [^25] or as
a name of namespace scope in the global namespace.

##### Types <a id="extern.types">[[extern.types]]</a>

For each type T from the Standard C library,[^26] the types `::T` and
`std::T` are reserved to the implementation and, when defined, `::T`
shall be identical to `std::T`.

##### User-defined literal suffixes <a id="usrlit.suffix">[[usrlit.suffix]]</a>

Literal suffix identifiers that do not start with an underscore are
reserved for future standardization.

#### Headers <a id="alt.headers">[[alt.headers]]</a>

If a file with a name equivalent to the derived file name for one of the
C++standard library headers is not provided as part of the
implementation, and a file with that name is placed in any of the
standard places for a source file to be included ([[cpp.include]]), the
behavior is undefined.

#### Derived classes <a id="derived.classes">[[derived.classes]]</a>

Virtual member function signatures defined for a base class in the
C++standard library may be overridden in a derived class defined in the
program ([[class.virtual]]).

#### Replacement functions <a id="replacement.functions">[[replacement.functions]]</a>

Clauses  [[support]] through  [[thread]] and Annex  [[depr]] describe
the behavior of numerous functions defined by the C++standard library.
Under some circumstances, however, certain of these function
descriptions also apply to replacement functions defined in the
program ([[definitions]]).

A C++program may provide the definition for any of twelve dynamic memory
allocation function signatures declared in header `<new>` (
[[basic.stc.dynamic]], [[support.dynamic]]):

- `operator new(std::size_t)`
- `operator new(std::size_t, const std::nothrow_t&)`
- `operator new[](std::size_t)`
- `operator new[](std::size_t, const std::nothrow_t&)`
- `operator delete(void*)`
- `operator delete(void*, const std::nothrow_t&)`
- `operator delete[](void*)`
- `operator delete[](void*, const std::nothrow_t&)`
- `operator delete(void*, std::size_t)`
- `operator delete(void*, std::size_t, const std::nothrow_t&)`
- `operator delete[](void*, std::size_t)`
- `operator delete[](void*, std::size_t, const std::nothrow_t&)`

The program’s definitions are used instead of the default versions
supplied by the implementation ([[support.dynamic]]). Such replacement
occurs prior to program startup ([[basic.def.odr]], [[basic.start]]).
The program’s definitions shall not be specified as `inline`. No
diagnostic is required.

#### Handler functions <a id="handler.functions">[[handler.functions]]</a>

The C++standard library provides default versions of the following
handler functions (Clause  [[language.support]]):

- `unexpected_handler`
- `terminate_handler`

A C++program may install different handler functions during execution,
by supplying a pointer to a function defined in the program or the
library as an argument to (respectively):

- `set_new_handler`
- `set_unexpected`
- `set_terminate` subclauses  [[alloc.errors]], Storage allocation
  errors, and  [[support.exception]], Exception handling.

A C++program can get a pointer to the current handler function by
calling the following functions:

- `get_new_handler`
- `get_unexpected`
- `get_terminate`

Calling the `set_*` and `get_*` functions shall not incur a data race. A
call to any of the `set_*` functions shall synchronize with subsequent
calls to the same `set_*` function and to the corresponding `get_*`
function.

#### Other functions <a id="res.on.functions">[[res.on.functions]]</a>

In certain cases (replacement functions, handler functions, operations
on types used to instantiate standard library template components), the
C++standard library depends on components supplied by a C++program. If
these components do not meet their requirements, the Standard places no
requirements on the implementation.

In particular, the effects are undefined in the following cases:

- for replacement functions ([[new.delete]]), if the installed
  replacement function does not implement the semantics of the
  applicable *Required behavior:* paragraph.
- for handler functions ([[new.handler]], [[terminate.handler]],
  [[unexpected.handler]]), if the installed handler function does not
  implement the semantics of the applicable *Required behavior:*
  paragraph
- for types used as template arguments when instantiating a template
  component, if the operations on the type do not implement the
  semantics of the applicable subclause ([[allocator.requirements]],
  [[container.requirements]], [[iterator.requirements]],
  [[numeric.requirements]]). Operations on such types can report a
  failure by throwing an exception unless otherwise specified.
- if any replacement function or handler function or destructor
  operation exits via an exception, unless specifically allowed in the
  applicable *Required behavior:* paragraph.
- if an incomplete type ([[basic.types]]) is used as a template
  argument when instantiating a template component, unless specifically
  allowed for that component.

#### Function arguments <a id="res.on.arguments">[[res.on.arguments]]</a>

Each of the following applies to all arguments to functions defined in
the C++standard library, unless explicitly stated otherwise.

- If an argument to a function has an invalid value (such as a value
  outside the domain of the function or a pointer invalid for its
  intended use), the behavior is undefined.
- If a function argument is described as being an array, the pointer
  actually passed to the function shall have a value such that all
  address computations and accesses to objects (that would be valid if
  the pointer did point to the first element of such an array) are in
  fact valid.
- If a function argument binds to an rvalue reference parameter, the
  implementation may assume that this parameter is a unique reference to
  this argument. If the parameter is a generic parameter of the form
  `T&&` and an lvalue of type `A` is bound, the argument binds to an
  lvalue reference ([[temp.deduct.call]]) and thus is not covered by
  the previous sentence. If a program casts an lvalue to an xvalue while
  passing that lvalue to a library function (e.g. by calling the
  function with the argument `move(x)`), the program is effectively
  asking that function to treat that lvalue as a temporary. The
  implementation is free to optimize away aliasing checks which might be
  needed if the argument was an lvalue.

#### Shared objects and the library <a id="res.on.objects">[[res.on.objects]]</a>

The behavior of a program is undefined if calls to standard library
functions from different threads may introduce a data race. The
conditions under which this may occur are specified in 
[[res.on.data.races]]. Modifying an object of a standard library type
that is shared between threads risks undefined behavior unless objects
of that type are explicitly specified as being sharable without data
races or the user supplies a locking mechanism.

In particular, the program is required to ensure that completion of the
constructor of any object of a class type defined in the standard
library happens before any other member function invocation on that
object and, unless otherwise specified, to ensure that completion of any
member function invocation other than destruction on such an object
happens before destruction of that object. This applies even to objects
such as mutexes intended for thread synchronization.

#### Requires paragraph <a id="res.on.required">[[res.on.required]]</a>

Violation of the preconditions specified in a function’s *Requires:*
paragraph results in undefined behavior unless the function’s *Throws:*
paragraph specifies throwing an exception when the precondition is
violated.

### Conforming implementations <a id="conforming">[[conforming]]</a>

#### Overview <a id="conforming.overview">[[conforming.overview]]</a>

This section describes the constraints upon, and latitude of,
implementations of the C++standard library.

An implementation’s use of headers is discussed in  [[res.on.headers]],
its use of macros in  [[res.on.macro.definitions]], global functions in 
[[global.functions]], member functions in  [[member.functions]], data
race avoidance in  [[res.on.data.races]], access specifiers in 
[[protection.within.classes]], class derivation in  [[derivation]], and
exceptions in  [[res.on.exception.handling]].

#### Headers <a id="res.on.headers">[[res.on.headers]]</a>

A C++header may include other C++headers. A C++header shall provide the
declarations and definitions that appear in its synopsis. A C++header
shown in its synopsis as including other C++headers shall provide the
declarations and definitions that appear in the synopses of those other
headers.

Certain types and macros are defined in more than one header. Every such
entity shall be defined such that any header that defines it may be
included after any other header that also defines it (
[[basic.def.odr]]).

The C standard headers ([[depr.c.headers]]) shall include only their
corresponding C++standard header, as described in  [[headers]].

#### Restrictions on macro definitions <a id="res.on.macro.definitions">[[res.on.macro.definitions]]</a>

The names and global function signatures described in  [[contents]] are
reserved to the implementation.

All object-like macros defined by the C standard library and described
in this Clause as expanding to integral constant expressions are also
suitable for use in `#if` preprocessing directives, unless explicitly
stated otherwise.

#### Global and non-member functions <a id="global.functions">[[global.functions]]</a>

It is unspecified whether any global or non-member functions in the
C++standard library are defined as `inline` ([[dcl.fct.spec]]).

A call to a global or non-member function signature described in
Clauses  [[support]] through  [[thread]] and Annex  [[depr]] shall
behave as if the implementation declared no additional global or
non-member function signatures.[^27]

An implementation shall not declare a global or non-member function
signature with additional default arguments.

Unless otherwise specified, global and non-member functions in the
standard library shall not use functions from another namespace which
are found through *argument-dependent name lookup* (
[[basic.lookup.argdep]]). The phrase “unless otherwise specified” is
intended to allow argument-dependent lookup in cases like that of
`ostream_iterator::operator=` ([[ostream.iterator.ops]]):

*Effects:*

``` cpp
*out_stream << value;
if (delim != 0)
  *out_stream << delim;
return *this;
```

#### Member functions <a id="member.functions">[[member.functions]]</a>

It is unspecified whether any member functions in the C++standard
library are defined as `inline` ([[dcl.fct.spec]]).

An implementation may declare additional non-virtual member function
signatures within a class:

- by adding arguments with default values to a member function
  signature; [^28] An implementation may not add arguments with default
  values to virtual, global, or non-member functions.
- by replacing a member function signature with default values by two or
  more member function signatures with equivalent behavior; and
- by adding a member function signature for a member function name.

A call to a member function signature described in the C++standard
library behaves as if the implementation declares no additional member
function signatures.[^29]

#### `constexpr` functions and constructors <a id="constexpr.functions">[[constexpr.functions]]</a>

This standard explicitly requires that certain standard library
functions are `constexpr` ([[dcl.constexpr]]). An implementation shall
not declare any standard library function signature as `constexpr`
except for those where it is explicitly required. Within any header that
provides any non-defining declarations of `constexpr` functions or
constructors an implementation shall provide corresponding definitions.

#### Requirements for stable algorithms <a id="algorithm.stable">[[algorithm.stable]]</a>

When the requirements for an algorithm state that it is “stable” without
further elaboration, it means:

- For the *sort* algorithms the relative order of equivalent elements is
  preserved.
- For the *remove* and *copy* algorithms the relative order of the
  elements that are not removed is preserved.
- For the *merge* algorithms, for equivalent elements in the original
  two ranges, the elements from the first range (preserving their
  original order) precede the elements from the second range (preserving
  their original order).

#### Reentrancy <a id="reentrancy">[[reentrancy]]</a>

Except where explicitly specified in this standard, it is
*implementation-defined* which functions in the Standard C++ library may
be recursively reentered.

#### Data race avoidance <a id="res.on.data.races">[[res.on.data.races]]</a>

This section specifies requirements that implementations shall meet to
prevent data races ([[intro.multithread]]). Every standard library
function shall meet each requirement unless otherwise specified.
Implementations may prevent data races in cases other than those
specified below.

A C++standard library function shall not directly or indirectly access
objects ([[intro.multithread]]) accessible by threads other than the
current thread unless the objects are accessed directly or indirectly
via the function’s arguments, including `this`.

A C++standard library function shall not directly or indirectly modify
objects ([[intro.multithread]]) accessible by threads other than the
current thread unless the objects are accessed directly or indirectly
via the function’s non-const arguments, including `this`.

This means, for example, that implementations can’t use a static object
for internal purposes without synchronization because it could cause a
data race even in programs that do not explicitly share objects between
threads.

A C++standard library function shall not access objects indirectly
accessible via its arguments or via elements of its container arguments
except by invoking functions required by its specification on those
container elements.

Operations on iterators obtained by calling a standard library container
or string member function may access the underlying container, but shall
not modify it. In particular, container operations that invalidate
iterators conflict with operations on iterators associated with that
container.

Implementations may share their own internal objects between threads if
the objects are not visible to users and are protected against data
races.

Unless otherwise specified, C++standard library functions shall perform
all operations solely within the current thread if those operations have
effects that are visible ([[intro.multithread]]) to users.

This allows implementations to parallelize operations if there are no
visible side effects.

#### Protection within classes <a id="protection.within.classes">[[protection.within.classes]]</a>

It is unspecified whether any function signature or class described in
Clauses  [[support]] through  [[thread]] and Annex  [[depr]] is a
`friend` of another class in the C++standard library.

#### Derived classes <a id="derivation">[[derivation]]</a>

An implementation may derive any class in the C++standard library from a
class with a name reserved to the implementation.

Certain classes defined in the C++standard library are required to be
derived from other classes in the C++standard library. An implementation
may derive such a class directly from the required base or indirectly
through a hierarchy of base classes with names reserved to the
implementation.

In any case:

- Every base class described as `virtual` shall be virtual;
- Every base class described as non-`virtual` shall not be virtual;
- Unless explicitly stated otherwise, types with distinct names shall be
  distinct types.[^30]

#### Restrictions on exception handling <a id="res.on.exception.handling">[[res.on.exception.handling]]</a>

Any of the functions defined in the C++standard library can report a
failure by throwing an exception of a type described in its paragraph.
An implementation may strengthen the *exception-specification* for a
non-virtual function by adding a non-throwing *noexcept-specification*.

A function may throw an object of a type not listed in its clause if its
type is derived from a type named in the clause and would be caught by
an exception handler for the base type.

Functions from the C standard library shall not throw exceptions [^31]
except when such a function calls a program-supplied function that
throws an exception.[^32]

Destructor operations defined in the C++standard library shall not throw
exceptions. Every destructor in the C++standard library shall behave as
if it had a non-throwing exception specification. Any other functions
defined in the C++standard library that do not have an
*exception-specification* may throw *implementation-defined* exceptions
unless otherwise specified.[^33] An implementation may strengthen this
implicit *exception-specification* by adding an explicit one.[^34]

#### Restrictions on storage of pointers <a id="res.on.pointer.storage">[[res.on.pointer.storage]]</a>

Objects constructed by the standard library that may hold a
user-supplied pointer value or an integer of type `std::intptr_t` shall
store such values in a traceable pointer location (
[[basic.stc.dynamic.safety]]). Other libraries are strongly encouraged
to do the same, since not doing so may result in accidental use of
pointers that are not safely derived. Libraries that store pointers
outside the user’s address space should make it appear that they are
stored and retrieved from a traceable pointer location.

#### Value of error codes <a id="value.error.codes">[[value.error.codes]]</a>

Certain functions in the C++standard library report errors via a
`std::error_code` ([[syserr.errcode.overview]]) object. That object’s
`category()` member shall return `std::system_category()` for errors
originating from the operating system, or a reference to an
*implementation-defined* `error_category` object for errors originating
elsewhere. The implementation shall define the possible values of
`value()` for each of these error categories. For operating systems that
are based on POSIX, implementations are encouraged to define the
`std::system_category()` values as identical to the POSIX `errno`
values, with additional values as defined by the operating system’s
documentation. Implementations for operating systems that are not based
on POSIX are encouraged to define values identical to the operating
system’s values. For errors that do not originate from the operating
system, the implementation may provide enums for the associated values.

#### Moved-from state of library types <a id="lib.types.movedfrom">[[lib.types.movedfrom]]</a>

Objects of types defined in the C++standard library may be moved from (
[[class.copy]]). Move operations may be explicitly specified or
implicitly generated. Unless otherwise specified, such moved-from
objects shall be placed in a valid but unspecified state.

<!-- Link reference definitions -->
[alg.c.library]: algorithms.md#alg.c.library
[alg.sorting]: algorithms.md#alg.sorting
[algorithm.stable]: #algorithm.stable
[algorithms]: algorithms.md#algorithms
[alloc.errors]: language.md#alloc.errors
[allocator.requirements]: #allocator.requirements
[allocator.traits]: utilities.md#allocator.traits
[alt.headers]: #alt.headers
[atomics]: atomics.md#atomics
[bad.alloc]: language.md#bad.alloc
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.link]: basic.md#basic.link
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.start]: basic.md#basic.start
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[basic.types]: basic.md#basic.types
[bitmask.types]: #bitmask.types
[byte.strings]: #byte.strings
[c.locales]: localization.md#c.locales
[c.strings]: strings.md#c.strings
[character.seq]: #character.seq
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.dtor]: special.md#class.dtor
[class.mem]: class.md#class.mem
[class.mfct]: class.md#class.mfct
[class.this]: class.md#class.this
[class.virtual]: class.md#class.virtual
[compliance]: #compliance
[conforming]: #conforming
[conforming.overview]: #conforming.overview
[constexpr.functions]: #constexpr.functions
[constraints]: #constraints
[constraints.overview]: #constraints.overview
[container.requirements]: containers.md#container.requirements
[containers]: containers.md#containers
[contents]: #contents
[conv]: conv.md#conv
[conventions]: #conventions
[cpp.include]: cpp.md#cpp.include
[cstdint]: language.md#cstdint
[dcl.array]: dcl.md#dcl.array
[dcl.attr]: dcl.md#dcl.attr
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.fct.spec]: dcl.md#dcl.fct.spec
[dcl.init]: dcl.md#dcl.init
[dcl.link]: dcl.md#dcl.link
[definitions]: #definitions
[defns.additional]: #defns.additional
[depr]: #depr
[depr.c.headers]: future.md#depr.c.headers
[derivation]: #derivation
[derived.classes]: #derived.classes
[description]: #description
[destructible]: #destructible
[diagnostics]: diagnostics.md#diagnostics
[enumerated.types]: #enumerated.types
[equalitycomparable]: #equalitycomparable
[except]: except.md#except
[expr.delete]: expr.md#expr.delete
[expr.eq]: expr.md#expr.eq
[expr.new]: expr.md#expr.new
[expr.rel]: expr.md#expr.rel
[extern.names]: #extern.names
[extern.types]: #extern.types
[function.objects]: utilities.md#function.objects
[functions.within.classes]: #functions.within.classes
[global.functions]: #global.functions
[global.names]: #global.names
[handler.functions]: #handler.functions
[hash]: #hash
[hash.requirements]: #hash.requirements
[headers]: #headers
[input.output]: input.md#input.output
[intro.compliance]: intro.md#intro.compliance
[intro.defs]: intro.md#intro.defs
[intro.multithread]: intro.md#intro.multithread
[intro.refs]: intro.md#intro.refs
[iterator.requirements]: iterators.md#iterator.requirements
[iterators]: iterators.md#iterators
[language.support]: language.md#language.support
[lex]: lex.md#lex
[lex.key]: lex.md#lex.key
[lex.phases]: lex.md#lex.phases
[lib.types.movedfrom]: #lib.types.movedfrom
[library]: #library
[library.c]: #library.c
[library.general]: #library.general
[locales]: localization.md#locales
[localization]: localization.md#localization
[macro.names]: #macro.names
[member.functions]: #member.functions
[meta]: utilities.md#meta
[multibyte.strings]: #multibyte.strings
[namespace.constraints]: #namespace.constraints
[namespace.def]: dcl.md#namespace.def
[namespace.posix]: #namespace.posix
[namespace.std]: #namespace.std
[namespace.udecl]: dcl.md#namespace.udecl
[new.delete]: language.md#new.delete
[new.handler]: language.md#new.handler
[nullablepointer]: #nullablepointer
[nullablepointer.requirements]: #nullablepointer.requirements
[numeric.requirements]: numerics.md#numeric.requirements
[numerics]: numerics.md#numerics
[objects.within.classes]: #objects.within.classes
[organization]: #organization
[ostream.iterator.ops]: iterators.md#ostream.iterator.ops
[over.match]: over.md#over.match
[over.oper]: over.md#over.oper
[protection.within.classes]: #protection.within.classes
[re]: re.md#re
[reentrancy]: #reentrancy
[replacement.functions]: #replacement.functions
[requirements]: #requirements
[res.on.arguments]: #res.on.arguments
[res.on.data.races]: #res.on.data.races
[res.on.exception.handling]: #res.on.exception.handling
[res.on.functions]: #res.on.functions
[res.on.headers]: #res.on.headers
[res.on.macro.definitions]: #res.on.macro.definitions
[res.on.objects]: #res.on.objects
[res.on.pointer.storage]: #res.on.pointer.storage
[res.on.required]: #res.on.required
[reserved.names]: #reserved.names
[std.exceptions]: diagnostics.md#std.exceptions
[stream.types]: input.md#stream.types
[strings]: strings.md#strings
[structure]: #structure
[structure.elements]: #structure.elements
[structure.requirements]: #structure.requirements
[structure.see.also]: #structure.see.also
[structure.specifications]: #structure.specifications
[structure.summary]: #structure.summary
[support]: #support
[support.dynamic]: language.md#support.dynamic
[support.exception]: language.md#support.exception
[support.initlist]: language.md#support.initlist
[support.limits]: language.md#support.limits
[support.rtti]: language.md#support.rtti
[support.runtime]: language.md#support.runtime
[support.start.term]: language.md#support.start.term
[support.types]: language.md#support.types
[swappable.requirements]: #swappable.requirements
[syserr]: diagnostics.md#syserr
[syserr.errcode.overview]: diagnostics.md#syserr.errcode.overview
[tab:cpp.c.headers]: #tab:cpp.c.headers
[tab:cpp.headers.freestanding]: #tab:cpp.headers.freestanding
[tab:cpp.library.headers]: #tab:cpp.library.headers
[tab:desc.var.def]: #tab:desc.var.def
[tab:identifiers.special]: #tab:identifiers.special
[tab:library.categories]: #tab:library.categories
[tab:utilities.allocator.requirements]: #tab:utilities.allocator.requirements
[temp.deduct.call]: temp.md#temp.deduct.call
[template.bitset]: utilities.md#template.bitset
[terminate.handler]: language.md#terminate.handler
[thread]: thread.md#thread
[type.descriptions]: #type.descriptions
[type.descriptions.general]: #type.descriptions.general
[unexpected.handler]: future.md#unexpected.handler
[using]: #using
[using.headers]: #using.headers
[using.linkage]: #using.linkage
[using.overview]: #using.overview
[usrlit.suffix]: #usrlit.suffix
[utilities]: utilities.md#utilities
[utility]: utilities.md#utility
[utility.arg.requirements]: #utility.arg.requirements
[utility.requirements]: #utility.requirements
[value.error.codes]: #value.error.codes

[^1]: This definition is taken from POSIX.

[^2]: To save space, items that do not apply to a Clause are omitted.
    For example, if a Clause does not specify any requirements, there
    will be no “Requirements” subclause.

[^3]: Although in some cases the code given is unambiguously the optimum
    implementation.

[^4]: To save space, items that do not apply to a class are omitted. For
    example, if a class does not specify any comparison functions, there
    will be no “Comparison functions” subclause.

[^5]: To save space, items that do not apply to a function are omitted.
    For example, if a function does not specify any further
    preconditions, there will be no “Requires” paragraph.

[^6]: This simplifies the presentation of complexity requirements in
    some cases.

[^7]: Examples from  [[utility.requirements]] include:
    `EqualityComparable`, `LessThanComparable`, `CopyConstructible`.
    Examples from  [[iterator.requirements]] include: `InputIterator`,
    `ForwardIterator`, `Function`, `Predicate`.

[^8]: Such as an integer type, with constant integer values (
    [[basic.fundamental]]).

[^9]: Note that this definition differs from the definition in ISO C
    7.1.1.

[^10]: declared in `<clocale>` ([[c.locales]]).

[^11]: Many of the objects manipulated by function signatures declared
    in `<cstring>` ([[c.strings]]) are character sequences or NTBSs.
    The size of some of these character sequences is limited by a length
    value, maintained separately from the character sequence.

[^12]: A string literal, such as `"abc"`, is a static NTBS.

[^13]: An NTBSthat contains characters only from the basic execution
    character set is also an NTMBS. Each multibyte character then
    consists of a single byte.

[^14]: The C standard library headers (Annex  [[depr.c.headers]]) also
    define names within the global namespace, while the C++headers for C
    library facilities ([[headers]]) may also define names within the
    global namespace.

[^15]: This gives implementers freedom to use inline namespaces to
    support multiple configurations of the library.

[^16]: A header is not necessarily a source file, nor are the sequences
    delimited by `<` and `>` in header names necessarily valid source
    file names ([[cpp.include]]).

[^17]: This disallows the practice, allowed in C, of providing a masking
    macro in addition to the function prototype. The only way to achieve
    equivalent inline behavior in C++is to provide a definition as an
    extern inline function.

[^18]: In particular, including the standard header `<iso646.h>` or
    `<ciso646>` has no effect.

[^19]: The `".h"` headers dump all their names into the global
    namespace, whereas the newer forms keep their names in namespace
    `std`. Therefore, the newer forms are the preferred forms for all
    uses except for C++programs which are intended to be strictly
    compatible with C.

[^20]: This is the same as the Standard C library.

[^21]: The only reliable way to declare an object or function signature
    from the Standard C library is by including the header that declares
    it, notwithstanding the latitude granted in 7.1.4 of the C Standard.

[^22]: Any library code that instantiates other library templates must
    be prepared to work adequately with any user-supplied specialization
    that meets the minimum requirements of the Standard.

[^23]: The list of such reserved names includes `errno`, declared or
    defined in `<cerrno>`.

[^24]: The list of such reserved function signatures with external
    linkage includes `setjmp(jmp_buf)`, declared or defined in
    `<csetjmp>`, and `va_end(va_list)`, declared or defined in
    `<cstdarg>`.

[^25]: The function signatures declared in `<cuchar>`, `<cwchar>`, and
    `<cwctype>` are always reserved, notwithstanding the restrictions
    imposed in subclause 4.5.1 of Amendment 1 to the C Standard for
    these headers.

[^26]: These types are `clock_t`, `div_t`, `FILE`, `fpos_t`, `lconv`,
    `ldiv_t`, `mbstate_t`, `ptrdiff_t`, `sig_atomic_t`, `size_t`,
    `time_t`, `tm`, `va_list`, `wctrans_t`, `wctype_t`, and `wint_t`.

[^27]: A valid C++program always calls the expected library global or
    non-member function. An implementation may also define additional
    global or non-member functions that would otherwise not be called by
    a valid C++program.

[^28]: Hence, the address of a member function of a class in the
    C++standard library has an unspecified type.

[^29]: A valid C++program always calls the expected library member
    function, or one with equivalent behavior. An implementation may
    also define additional member functions that would otherwise not be
    called by a valid C++program.

[^30]: There is an implicit exception to this rule for types that are
    described as synonyms for basic integral types, such as `size_t` (
    [[support.types]]) and `streamoff` ([[stream.types]]).

[^31]: That is, the C library functions can all be treated as if they
    are marked `noexcept`. This allows implementations to make
    performance optimizations based on the absence of exceptions at
    runtime.

[^32]: The functions `qsort()` and `bsearch()` ([[alg.c.library]]) meet
    this condition.

[^33]: In particular, they can report a failure to allocate storage by
    throwing an exception of type `bad_alloc`, or a class derived from
    `bad_alloc` ([[bad.alloc]]). Library implementations should report
    errors by throwing exceptions of or derived from the standard
    exception classes ([[bad.alloc]], [[support.exception]],
    [[std.exceptions]]).

[^34]: That is, an implementation may provide an explicit
    *exception-specification* that defines the subset of “any”
    exceptions thrown by that function. This implies that the
    implementation may list implementation-defined types in such an
    *exception-specification*.
