# Library introduction <a id="library">[[library]]</a>

## General <a id="library.general">[[library.general]]</a>

This Clause describes the contents of the *C++ standard library*, how a
well-formed C++ program makes use of the library, and how a conforming
implementation may provide the entities in the library.

The following subclauses describe the method of description
[[description]] and organization [[organization]] of the library.
[[requirements]], [[support]] through [[thread]], and [[depr]] specify
the contents of the library, as well as library requirements and
constraints on both well-formed C++ programs and conforming
implementations.

Detailed specifications for each of the components in the library are in
[[support]]– [[thread]], as shown in [[library.categories]].

**Table: Library categories**

| Clause           | Category                    |
| ---------------- | --------------------------- |
| [[support]]      | Language support library    |
| [[concepts]]     | Concepts library            |
| [[diagnostics]]  | Diagnostics library         |
| [[mem]]          | Memory management library   |
| [[meta]]         | Metaprogramming library     |
| [[utilities]]    | General utilities library   |
| [[strings]]      | Strings library             |
| [[containers]]   | Containers library          |
| [[iterators]]    | Iterators library           |
| [[ranges]]       | Ranges library              |
| [[algorithms]]   | Algorithms library          |
| [[numerics]]     | Numerics library            |
| [[time]]         | Time library                |
| [[localization]] | Localization library        |
| [[input.output]] | Input/output library        |
| [[re]]           | Regular expressions library |
| [[thread]]       | Concurrency support library |


The language support library [[support]] provides components that are
required by certain parts of the C++ language, such as memory allocation
[[expr.new]], [[expr.delete]] and exception processing [[except]].

The concepts library [[concepts]] describes library components that C++
programs may use to perform compile-time validation of template
arguments and perform function dispatch based on properties of types.

The diagnostics library [[diagnostics]] provides a consistent framework
for reporting errors in a C++ program, including predefined exception
classes.

The memory management library [[mem]] provides components for memory
management, including smart pointers and scoped allocators.

The metaprogramming library [[meta]] describes facilities for use in
templates and during constant evaluation, including type traits, integer
sequences, and rational arithmetic.

The general utilities library [[utilities]] includes components used by
other library elements, such as a predefined storage allocator for
dynamic storage management [[basic.stc.dynamic]], and components used as
infrastructure in C++ programs, such as tuples and function wrappers.

The strings library [[strings]] provides support for manipulating text
represented as sequences of type `char`, sequences of type `char8_t`,
sequences of type `char16_t`, sequences of type `char32_t`, sequences of
type `wchar_t`, and sequences of any other character-like type.

The containers [[containers]], iterators [[iterators]], ranges
[[ranges]], and algorithms [[algorithms]] libraries provide a C++
program with access to a subset of the most widely used algorithms and
data structures.

The numerics library [[numerics]] provides numeric algorithms and
complex number components that extend support for numeric processing.
The `valarray` component provides support for *n*-at-a-time processing,
potentially implemented as parallel operations on platforms that support
such processing. The random number component provides facilities for
generating pseudo-random numbers.

The time library [[time]] provides generally useful time utilities.

The localization library [[localization]] provides extended
internationalization support for text processing.

The input/output library [[input.output]] provides the `iostream`
components that are the primary mechanism for C++ program input and
output. They can be used with other elements of the library,
particularly strings, locales, and iterators.

The regular expressions library [[re]] provides regular expression
matching and searching.

The concurrency support library [[thread]] provides components to create
and manage threads, including atomic operations, mutual exclusion, and
interthread communication.

## The C standard library <a id="library.c">[[library.c]]</a>

The C++ standard library also makes available the facilities of the C
standard library, suitably adjusted to ensure static type safety.

The descriptions of many library functions rely on the C standard
library for the semantics of those functions. In some cases, the
signatures specified in this document may be different from the
signatures in the C standard library, and additional overloads may be
declared in this document, but the behavior and the preconditions
(including any preconditions implied by the use of an ISO C `restrict`
qualifier) are the same unless otherwise stated.

A call to a C standard library function is a non-constant library call
[[defns.nonconst.libcall]] if it raises a floating-point exception other
than `FE_INEXACT`. The semantics of a call to a C standard library
function evaluated as a core constant expression are those specified in
Annex F of the C standard[^1]

to the extent applicable to the floating-point types
[[basic.fundamental]] that are parameter types of the called function.

[*Note 1*: Annex F specifies the conditions under which floating-point
exceptions are raised and the behavior when NaNs and/or infinities are
passed as arguments. — *end note*]

[*Note 2*: Equivalently, a call to a C standard library function is a
non-constant library call if `errno` is set when
`math_errhandling & MATH_ERRNO` is `true`. — *end note*]

## Method of description <a id="description">[[description]]</a>

### General <a id="description.general">[[description.general]]</a>

Subclause [[description]] describes the conventions used to specify the
C++ standard library. [[structure]] describes the structure of
[[support]] through [[thread]] and [[depr]]. [[conventions]] describes
other editorial conventions.

### Structure of each clause <a id="structure">[[structure]]</a>

#### Elements <a id="structure.elements">[[structure.elements]]</a>

Each library clause contains the following elements, as applicable:[^2]

- Summary
- Requirements
- Detailed specifications
- References to the C standard library

#### Summary <a id="structure.summary">[[structure.summary]]</a>

The Summary provides a synopsis of the category, and introduces the
first-level subclauses. Each subclause also provides a summary, listing
the headers specified in the subclause and the library entities provided
in each header.

The contents of the summary and the detailed specifications include:

- macros
- values
- types and alias templates
- classes and class templates
- functions and function templates
- objects and variable templates
- concepts

#### Requirements <a id="structure.requirements">[[structure.requirements]]</a>

Requirements describe constraints that shall be met by a C++ program
that extends the standard library. Such extensions are generally one of
the following:

- Template arguments
- Derived classes
- Containers, iterators, and algorithms that meet an interface
  convention or model a concept

The string and iostream components use an explicit representation of
operations required of template arguments. They use a class template
`char_traits` to define these constraints.

Interface convention requirements are stated as generally as possible.
Instead of stating “class `X` has to define a member function
`operator++()`”, the interface requires “for any object `x` of class
`X`, `++x` is defined”. That is, whether the operator is a member is
unspecified.

Requirements are stated in terms of well-defined expressions that define
valid terms of the types that meet the requirements. For every set of
well-defined expression requirements there is either a named concept or
a table that specifies an initial set of the valid expressions and their
semantics. Any generic algorithm [[algorithms]] that uses the
well-defined expression requirements is described in terms of the valid
expressions for its template type parameters.

The library specification uses a typographical convention for naming
requirements. Names in *italic* type that begin with the prefix *Cpp17*
refer to sets of well-defined expression requirements typically
presented in tabular form, possibly with additional prose semantic
requirements. For example, *Cpp17Destructible* ([[cpp17.destructible]])
is such a named requirement. Names in `constant width` type refer to
library concepts which are presented as a concept definition [[temp]],
possibly with additional prose semantic requirements. For example,
`destructible` [[concept.destructible]] is such a named requirement.

Template argument requirements are sometimes referenced by name. See 
[[type.descriptions]].

In some cases the semantic requirements are presented as C++ code. Such
code is intended as a specification of equivalence of a construct to
another construct, not necessarily as the way the construct must be
implemented.[^3]

Required operations of any concept defined in this document need not be
total functions; that is, some arguments to a required operation may
result in the required semantics failing to be met.

[*Example 1*: The required `<` operator of the `totally_ordered`
concept [[concept.totallyordered]] does not meet the semantic
requirements of that concept when operating on NaNs. — *end example*]

This does not affect whether a type models the concept.

A declaration may explicitly impose requirements through its associated
constraints [[temp.constr.decl]]. When the associated constraints refer
to a concept [[temp.concept]], the semantic constraints specified for
that concept are additionally imposed on the use of the declaration.

#### Detailed specifications <a id="structure.specifications">[[structure.specifications]]</a>

The detailed specifications each contain the following elements:

- name and brief description
- synopsis (class definition or function declaration, as appropriate)
- restrictions on template arguments, if any
- description of class invariants
- description of function semantics

Descriptions of class member functions follow the order (as
appropriate):[^4]

- constructor(s) and destructor
- copying, moving & assignment functions
- comparison operator functions
- modifier functions
- observer functions
- operators and other non-member functions

Descriptions of function semantics contain the following elements (as
appropriate):[^5]

- *Constraints:* the conditions for the function’s participation in
  overload resolution [[over.match]]. \[*Note 1*: Failure to meet such a
  condition results in the function’s silent
  non-viability. — *end note*] \[*Example 1*: An implementation can
  express such a condition via a *constraint-expression*
  [[temp.constr.decl]]. — *end example*]
- *Mandates:* the conditions that, if not met, render the program
  ill-formed. \[*Example 2*: An implementation can express such a
  condition via the *constant-expression* in a
  *static_assert-declaration* [[dcl.pre]]. If the diagnostic is to be
  emitted only after the function has been selected by overload
  resolution, an implementation can express such a condition via a
  *constraint-expression* [[temp.constr.decl]] and also define the
  function as deleted. — *end example*]
- *Preconditions:* the conditions that the function assumes to hold
  whenever it is called; violation of any preconditions results in
  undefined behavior.
- *Effects:* the actions performed by the function.
- *Synchronization:* the synchronization operations
  [[intro.multithread]] applicable to the function.
- *Ensures:* the conditions (sometimes termed observable results)
  established by the function.
- *Result:* for a *typename-specifier*, a description of the named type;
  for an *expression*, a description of the type of the expression; the
  expression is an lvalue if the type is an lvalue reference type, an
  xvalue if the type is an rvalue reference type, and a prvalue
  otherwise.
- *Returns:* a description of the value(s) returned by the function.
- *Throws:* any exceptions thrown by the function, and the conditions
  that would cause the exception.
- *Complexity:* the time and/or space complexity of the function.
- *Remarks:* additional semantic constraints on the function.
- *Error conditions:* the error conditions for error codes reported by
  the function.

Whenever the *Effects* element specifies that the semantics of some
function `F` are *Equivalent to* some code sequence, then the various
elements are interpreted as follows. If `F`’s semantics specifies any
*Constraints* or *Mandates* elements, then those requirements are
logically imposed prior to the *equivalent-to* semantics. Next, the
semantics of the code sequence are determined by the *Constraints*,
*Mandates*, *Preconditions*, *Effects*, *Synchronization*,
*Postconditions*, *Returns*, *Throws*, *Complexity*, *Remarks*, and
*Error conditions* specified for the function invocations contained in
the code sequence. The value returned from `F` is specified by `F`’s
*Returns* element, or if `F` has no *Returns* element, a non-`void`
return from `F` is specified by the `return` statements [[stmt.return]]
in the code sequence. If `F`’s semantics contains a *Throws*,
*Postconditions*, or *Complexity* element, then that supersedes any
occurrences of that element in the code sequence.

For non-reserved replacement and handler functions, [[support]]
specifies two behaviors for the functions in question: their required
and default behavior. The *default behavior* describes a function
definition provided by the implementation. The *required behavior*
describes the semantics of a function definition provided by either the
implementation or a C++ program. Where no distinction is explicitly made
in the description, the behavior described is the required behavior.

If the formulation of a complexity requirement calls for a negative
number of operations, the actual requirement is zero operations.[^6]

Complexity requirements specified in the library clauses are upper
bounds, and implementations that provide better complexity guarantees
meet the requirements.

Error conditions specify conditions where a function may fail. The
conditions are listed, together with a suitable explanation, as the
`enum class errc` constants [[syserr]].

#### C library <a id="structure.see.also">[[structure.see.also]]</a>

Paragraphs labeled “<span class="smallcaps">See also</span>” contain
cross-references to the relevant portions of other standards
[[intro.refs]].

### Other conventions <a id="conventions">[[conventions]]</a>

#### General <a id="conventions.general">[[conventions.general]]</a>

Subclause [[conventions]] describes several editorial conventions used
to describe the contents of the C++ standard library. These conventions
are for describing implementation-defined types [[type.descriptions]],
and member functions [[functions.within.classes]].

#### Exposition-only entities, etc. <a id="expos.only.entity">[[expos.only.entity]]</a>

Several entities and *typedef-name*s defined in [[support]] through
[[thread]] and [[depr]] are only defined for the purpose of exposition.
The declaration of such an entity or *typedef-name* is followed by a
comment ending in *exposition only*.

The following are defined for exposition only to aid in the
specification of the library:

``` cpp
namespace std {
  template<class T>
    requires convertible_to<T, decay_t<T>>
      constexpr decay_t<T> decay-copy(T&& v)
        noexcept(is_nothrow_convertible_v<T, decay_t<T>>)       // exposition only
      { return std::forward<T>(v); }

  constexpr auto synth-three-way =
    []<class T, class U>(const T& t, const U& u)
      requires requires {
        { t < u } -> boolean-testable;
        { u < t } -> boolean-testable;
      }
    {
      if constexpr (three_way_comparable_with<T, U>) {
        return t <=> u;
      } else {
        if (t < u) return weak_ordering::less;
        if (u < t) return weak_ordering::greater;
        return weak_ordering::equivalent;
      }
    };

  template<class T, class U=T>
  using synth-three-way-result = decltype(synth-three-way(declval<T&>(), declval<U&>()));
}
```

#### Type descriptions <a id="type.descriptions">[[type.descriptions]]</a>

##### General <a id="type.descriptions.general">[[type.descriptions.general]]</a>

The Requirements subclauses may describe names that are used to specify
constraints on template arguments.[^7]

These names are used in library Clauses to describe the types that may
be supplied as arguments by a C++ program when instantiating template
components from the library.

Certain types defined in [[input.output]] are used to describe
implementation-defined types. They are based on other types, but with
added constraints.

##### Enumerated types <a id="enumerated.types">[[enumerated.types]]</a>

Several types defined in [[input.output]] are . Each enumerated type may
be implemented as an enumeration or as a synonym for an enumeration.[^8]

The enumerated type `enumerated` can be written:

``` cpp
enum enumerated { V₀, V₁, V₂, V₃, … };

inline const enumerated C₀(V₀);
inline const enumerated C₁(V₁);
inline const enumerated C₂(V₂);
inline const enumerated C₃(V₃);
  ⋮
```

Here, the names `C₀`, `C₁`, etc. represent *enumerated elements* for
this particular enumerated type. All such elements have distinct values.

##### Bitmask types <a id="bitmask.types">[[bitmask.types]]</a>

Several types defined in [[support]] through [[thread]] and [[depr]] are
*bitmask types*. Each bitmask type can be implemented as an enumerated
type that overloads certain operators, as an integer type, or as a
`bitset` [[template.bitset]].

The bitmask type `bitmask` can be written:

``` cpp
// For exposition only.
// int_type is an integral type capable of representing all values of the bitmask type.
enum bitmask : int_type {
  V₀ = 1 << 0, V₁ = 1 << 1, V₂ = 1 << 2, V₃ = 1 << 3, …
};

inline constexpr bitmask C₀(V₀{});
inline constexpr bitmask C₁(V₁{});
inline constexpr bitmask C₂(V₂{});
inline constexpr bitmask C₃(V₃{});
  ⋮

constexpr bitmask operator&(bitmask X, bitmask Y) {
  return static_cast<bitmask>(
    static_cast<int_type>(X) & static_cast<int_type>(Y));
}
constexpr bitmask operator|(bitmask X, bitmask Y) {
  return static_cast<bitmask>(
    static_cast<int_type>(X) | static_cast<int_type>(Y));
}
constexpr bitmask operator^(bitmask X, bitmask Y) {
  return static_cast<bitmask>(
    static_cast<int_type>(X) ^ static_cast<int_type>(Y));
}
constexpr bitmask operator~(bitmask X) {
  return static_cast<bitmask>(~static_cast<int_type>(X));
}
bitmask& operator&=(bitmask& X, bitmask Y) {
  X = X & Y; return X;
}
bitmask& operator|=(bitmask& X, bitmask Y) {
  X = X | Y; return X;
}
bitmask& operator^=(bitmask& X, bitmask Y) {
  X = X ^ Y; return X;
}
```

Here, the names `C₀`, `C₁`, etc. represent *bitmask elements* for this
particular bitmask type. All such elements have distinct, nonzero values
such that, for any pair `Cᵢ` and `Cⱼ` where i ≠ j, `C_i & C_i` is
nonzero and `C_i & C_j` is zero. Additionally, the value `0` is used to
represent an *empty bitmask*, in which no bitmask elements are set.

The following terms apply to objects and values of bitmask types:

- To *set* a value *Y* in an object *X* is to evaluate the expression
  *X* `|=` *Y*.
- To *clear* a value *Y* in an object *X* is to evaluate the expression
  *X* `&= ~`*Y*.
- The value *Y* *is set* in the object *X* if the expression *X* `&` *Y*
  is nonzero.

##### Character sequences <a id="character.seq">[[character.seq]]</a>

###### General <a id="character.seq.general">[[character.seq.general]]</a>

The C standard library makes widespread use of characters and character
sequences that follow a few uniform conventions:

- Properties specified as *locale-specific* may change during program
  execution by a call to `setlocale(int, const char*)` [[clocale.syn]],
  or by a change to a `locale` object, as described in [[locales]] and
  [[input.output]].
- The *execution character set* and the *execution wide-character set*
  are supersets of the basic literal character set [[lex.charset]]. The
  encodings of the execution character sets and the sets of additional
  elements (if any) are locale-specific. Each element of the execution
  wide-character set is encoded as a single code unit representable by a
  value of type `wchar_t`. \[*Note 2*: The encodings of the execution
  character sets can be unrelated to any literal
  encoding. — *end note*]
- A *letter* is any of the 26 lowercase or 26 uppercase letters in the
  basic character set.
- The *decimal-point character* is the locale-specific (single-byte)
  character used by functions that convert between a (single-byte)
  character sequence and a value of one of the floating-point types. It
  is used in the character sequence to denote the beginning of a
  fractional part. It is represented in [[support]] through [[thread]]
  and [[depr]] by a period, `'.'`, which is also its value in the `"C"`
  locale.
- A *character sequence* is an array object [[dcl.array]] `A` that can
  be declared as `T A[N]`, where `T` is any of the types `char`,
  `unsigned char`, or `signed char` [[basic.fundamental]], optionally
  qualified by any combination of `const` or `volatile`. The initial
  elements of the array have defined contents up to and including an
  element determined by some predicate. A character sequence can be
  designated by a pointer value `S` that points to its first element.

###### Byte strings <a id="byte.strings">[[byte.strings]]</a>

A *null-terminated byte string*, or NTBS, is a character sequence whose
highest-addressed element with defined content has the value zero (the
*terminating null character*); no other element in the sequence has the
value zero.[^9]

The *length of an NTBS* is the number of elements that precede the
terminating null character. An *empty NTBS* has a length of zero.

The *value of an NTBS* is the sequence of values of the elements up to
and including the terminating null character.

A *static NTBS* is an NTBS with static storage duration.[^10]

###### Multibyte strings <a id="multibyte.strings">[[multibyte.strings]]</a>

A *multibyte character* is a sequence of one or more bytes representing
the code unit sequence for an encoded character of the execution
character set.

A *null-terminated multibyte string*, or NTMBS, is an NTBS that
constitutes a sequence of valid multibyte characters, beginning and
ending in the initial shift state.[^11]

A *static NTMBS* is an NTMBS with static storage duration.

##### Customization Point Object types <a id="customization.point.object">[[customization.point.object]]</a>

A *customization point object* is a function object [[function.objects]]
with a literal class type that interacts with program-defined types
while enforcing semantic requirements on that interaction.

The type of a customization point object, ignoring cv-qualifiers, shall
model `semiregular` [[concepts.object]].

All instances of a specific customization point object type shall be
equal [[concepts.equality]]. The effects of invoking different instances
of a specific customization point object type on the same arguments are
equivalent.

The type `T` of a customization point object, ignoring *cv-qualifier*s,
shall model `invocable<T&, Args...>`, `invocable<const T&, Args...>`,
`invocable<T, Args...>`, and `invocable<const T, Args...>`
[[concept.invocable]] when the types in `Args...` meet the requirements
specified in that customization point object’s definition. When the
types of `Args...` do not meet the customization point object’s
requirements, `T` shall not have a function call operator that
participates in overload resolution.

For a given customization point object `o`, let `p` be a variable
initialized as if by `auto p = o;`. Then for any sequence of arguments
`args...`, the following expressions have effects equivalent to
`o(args...)`:

- `p(args...)`
- `as_const(p)(args...)`
- `std::move(p)(args...)`
- `std::move(as_const(p))(args...)`

Each customization point object type constrains its return type to model
a particular concept.

#### Functions within classes <a id="functions.within.classes">[[functions.within.classes]]</a>

For the sake of exposition, [[support]] through [[thread]] and [[depr]]
do not describe copy/move constructors, assignment operators, or
(non-virtual) destructors with the same apparent semantics as those that
can be generated by default
[[class.copy.ctor]], [[class.copy.assign]], [[class.dtor]]. It is
unspecified whether the implementation provides explicit definitions for
such member function signatures, or for virtual destructors that can be
generated by default.

#### Private members <a id="objects.within.classes">[[objects.within.classes]]</a>

[[support]] through [[thread]] and [[depr]] do not specify the
representation of classes, and intentionally omit specification of class
members [[class.mem]]. An implementation may define static or non-static
class members, or both, as needed to implement the semantics of the
member functions specified in [[support]] through [[thread]] and
[[depr]].

For the sake of exposition, some subclauses provide representative
declarations, and semantic requirements, for private members of classes
that meet the external specifications of the classes. The declarations
for such members are followed by a comment that ends with *exposition
only*, as in:

``` cpp
streambuf* sb;      // exposition only
```

An implementation may use any technique that provides equivalent
observable behavior.

#### Freestanding items <a id="freestanding.item">[[freestanding.item]]</a>

A *freestanding item* is a declaration, entity, *typedef-name*, or macro
that is required to be present in a freestanding implementation and a
hosted implementation.

Unless otherwise specified, the requirements on freestanding items for a
freestanding implementation are the same as the corresponding
requirements for a hosted implementation, except that not all of the
members of the namespaces are required to be present.

[*Note 1*: This implies that freestanding item enumerations have the
same enumerators on freestanding implementations and hosted
implementations. Furthermore, class types have the same members and
class templates have the same deduction guides on freestanding
implementations and hosted implementations. — *end note*]

A declaration in a header synopsis is a freestanding item if

- it is followed by a comment that includes *freestanding*, or
- the header synopsis begins with a comment that includes *all
  freestanding*.

An entity or *typedef-name* is a freestanding item if it is:

- introduced by a declaration that is a freestanding item,
- an enclosing namespace of a freestanding item,
- a friend of a freestanding item,
- denoted by a *typedef-name* that is a freestanding item, or
- denoted by an alias template that is a freestanding item.

A macro is a freestanding item if it is defined in a header synopsis and

- the definition is followed by a comment that includes *freestanding*,
  or
- the header synopsis begins with a comment that includes *all
  freestanding*.

[*Example 1*:

``` cpp
#define NULL see below      // freestanding
```

— *end example*]

[*Example 2*:

``` cpp
// all freestanding
namespace std {
```

— *end example*]

## Library-wide requirements <a id="requirements">[[requirements]]</a>

### General <a id="requirements.general">[[requirements.general]]</a>

Subclause [[requirements]] specifies requirements that apply to the
entire C++ standard library. [[support]] through [[thread]] and [[depr]]
specify the requirements of individual entities within the library.

Requirements specified in terms of interactions between threads do not
apply to programs having only a single thread of execution.

[[organization]] describes the library’s contents and organization,
[[using]] describes how well-formed C++ programs gain access to library
entities, [[utility.requirements]] describes constraints on types and
functions used with the C++ standard library, [[constraints]] describes
constraints on well-formed C++ programs, and [[conforming]] describes
constraints on conforming implementations.

### Library contents and organization <a id="organization">[[organization]]</a>

#### General <a id="organization.general">[[organization.general]]</a>

[[contents]] describes the entities and macros defined in the C++
standard library. [[headers]] lists the standard library headers and
some constraints on those headers. [[compliance]] lists requirements for
a freestanding implementation of the C++ standard library.

#### Library contents <a id="contents">[[contents]]</a>

The C++ standard library provides definitions for the entities and
macros described in the synopses of the C++ standard library headers
[[headers]], unless otherwise specified.

All library entities except `operator new` and `operator delete` are
defined within the namespace `std` or namespaces nested within namespace
`std`.[^12]

It is unspecified whether names declared in a specific namespace are
declared directly in that namespace or in an inline namespace inside
that namespace.[^13]

Whenever an unqualified name other than `swap`, `make_error_code`, or
`make_error_condition` is used in the specification of a declaration `D`
in [[support]] through [[thread]] or [[depr]], its meaning is
established as-if by performing unqualified name lookup
[[basic.lookup.unqual]] in the context of `D`.

[*Note 1*: Argument-dependent lookup is not performed. — *end note*]

Similarly, the meaning of a *qualified-id* is established as-if by
performing qualified name lookup [[basic.lookup.qual]] in the context of
`D`.

[*Example 1*: The reference to `is_array_v` in the specification of
`std::to_array` [[array.creation]] refers to
`::std::is_array_v`. — *end example*]

[*Note 2*: Operators in expressions [[over.match.oper]] are not so
constrained; see [[global.functions]]. — *end note*]

The meaning of the unqualified name `swap` is established in an overload
resolution context for swappable values [[swappable.requirements]]. The
meanings of the unqualified names `make_error_code` and
`make_error_condition` are established as-if by performing
argument-dependent lookup [[basic.lookup.argdep]].

#### Headers <a id="headers">[[headers]]</a>

Each element of the C++ standard library is declared or defined (as
appropriate) in a *header*.[^14]

The C++ standard library provides the *C++ library headers*, shown in
[[headers.cpp]].

The facilities of the C standard library are provided in the additional
headers shown in [[headers.cpp.c]].[^15]

The headers listed in [[headers.cpp]], or, for a freestanding
implementation, the subset of such headers that are provided by the
implementation, are collectively known as the
*importable C++ library headers*.

[*Note 1*: Importable C++ library headers can be imported
[[module.import]]. — *end note*]

[*Example 1*:

``` cpp
import <vector>;                // imports the <vector> header unit
std::vector<int> vi;            // OK
```

— *end example*]

Except as noted in [[library]] through [[thread]] and [[depr]], the
contents of each header `cname` is the same as that of the corresponding
header `name.h` as specified in the C standard library [[intro.refs]].
In the C++ standard library, however, the declarations (except for names
which are defined as macros in C) are within namespace scope
[[basic.scope.namespace]] of the namespace `std`. It is unspecified
whether these names (including any overloads added in [[support]]
through [[thread]] and [[depr]]) are first declared within the global
namespace scope and are then injected into namespace `std` by explicit
*using-declaration*s [[namespace.udecl]].

Names which are defined as macros in C shall be defined as macros in the
C++ standard library, even if C grants license for implementation as
functions.

[*Note 2*: The names defined as macros in C include the following:
`assert`, `offsetof`, `setjmp`, `va_arg`, `va_end`, and
`va_start`. — *end note*]

Names that are defined as functions in C shall be defined as functions
in the C++ standard library.[^16]

Identifiers that are keywords or operators in C++ shall not be defined
as macros in C++ standard library headers.[^17]

[[support.c.headers]], C standard library headers, describes the effects
of using the `name.h` (C header) form in a C++ program.[^18]

Annex K of the C standard describes a large number of functions, with
associated types and macros, which “promote safer, more secure
programming” than many of the traditional C library functions. The names
of the functions have a suffix of `_s`; most of them provide the same
service as the C library function with the unsuffixed name, but
generally take an additional argument whose value is the size of the
result array. If any C++ header is included, it is
*implementation-defined* whether any of these names is declared in the
global namespace. (None of them is declared in namespace `std`.)

[[c.annex.k.names]] lists the Annex K names that may be declared in some
header. These names are also subject to the restrictions of 
[[macro.names]].

#### Modules <a id="std.modules">[[std.modules]]</a>

The C++ standard library provides the following *C++ library modules*.

The named module `std` exports declarations in namespace `std` that are
provided by the importable C++ library headers ([[headers.cpp]] or the
subset provided by a freestanding implementation) and the C++ headers
for C library facilities ([[headers.cpp.c]]). It additionally exports
declarations in the global namespace for the storage allocation and
deallocation functions that are provided by `<new>`.

The named module `std.compat` exports the same declarations as the named
module `std`, and additionally exports declarations in the global
namespace corresponding to the declarations in namespace `std` that are
provided by the C++ headers for C library facilities (
[[headers.cpp.c]]), except the explicitly excluded declarations
described in [[support.c.headers.other]].

It is unspecified to which module a declaration in the standard library
is attached.

[*Note 1*: Implementations are required to ensure that mixing
`#include` and `import` does not result in conflicting attachments
[[basic.link]]. — *end note*]

*Recommended practice:* Implementations should ensure such attachments
do not preclude further evolution or decomposition of the standard
library modules.

A declaration in the standard library denotes the same entity regardless
of whether it was made reachable through including a header, importing a
header unit, or importing a C++ library module.

*Recommended practice:* Implementations should avoid exporting any other
declarations from the C++ library modules.

[*Note 2*: Like all named modules, the C++ library modules do not make
macros visible [[module.import]], such as `assert` [[cassert.syn]],
`errno` [[cerrno.syn]], `offsetof` [[cstddef.syn]], and `va_arg`
[[cstdarg.syn]]. — *end note*]

#### Freestanding implementations <a id="compliance">[[compliance]]</a>

Two kinds of implementations are defined: hosted and freestanding
[[intro.compliance]]; the kind of the implementation is
*implementation-defined*. For a hosted implementation, this document
describes the set of available headers.

A freestanding implementation has an *implementation-defined* set of
headers. This set shall include at least the headers shown in
[[headers.cpp.fs]].

**Table: C++ headers for freestanding implementations**

| Subclause              |                                  | Header                                           |
| ---------------------- | -------------------------------- | ------------------------------------------------ |
| [[support.types]]      | Common definitions               | `<cstddef>`                                      |
| [[support.limits]]     | Implementation properties        | `<cfloat>`, `<climits>`, `<limits>`, `<version>` |
| [[cstdint.syn]]        | Integer types                    | `<cstdint>`                                      |
| [[support.start.term]] | Start and termination            | `<cstdlib>`                                      |
| [[support.dynamic]]    | Dynamic memory management        | `<new>`                                          |
| [[support.rtti]]       | Type identification              | `<typeinfo>`                                     |
| [[support.srcloc]]     | Source location                  | `<source_location>`                              |
| [[support.exception]]  | Exception handling               | `<exception>`                                    |
| [[support.initlist]]   | Initializer lists                | `<initializer_list>`                             |
| [[cmp]]                | Comparisons                      | `<compare>`                                      |
| [[support.coroutine]]  | Coroutines support               | `<coroutine>`                                    |
| [[support.runtime]]    | Other runtime support            | `<cstdarg>`                                      |
| [[concepts]]           | Concepts library                 | `<concepts>`                                     |
| [[type.traits]]        | Type traits                      | `<type_traits>`                                  |
| [[bit]]                | Bit manipulation                 | `<bit>`                                          |
| [[atomics]]            | Atomics                          | `<atomic>`                                       |
| [[utility]]            | Utility components               | `<utility>`                                      |
| [[tuple]]              | Tuples                           | `<tuple>`                                        |
| [[memory]]             | Memory                           | `<memory>`                                       |
| [[function.objects]]   | Function objects                 | `<functional>`                                   |
| [[ratio]]              | Compile-time rational arithmetic | `<ratio>`                                        |
| [[iterators]]          | Iterators library                | `<iterator>`                                     |
| [[ranges]]             | Ranges library                   | `<ranges>`                                       |


For each of the headers listed in [[headers.cpp.fs]], a freestanding
implementation provides at least the freestanding items
[[freestanding.item]] declared in the header.

### Using the library <a id="using">[[using]]</a>

#### Overview <a id="using.overview">[[using.overview]]</a>

Subclause [[using]] describes how a C++ program gains access to the
facilities of the C++ standard library. [[using.headers]] describes
effects during translation phase 4, while  [[using.linkage]] describes
effects during phase 8 [[lex.phases]].

#### Headers <a id="using.headers">[[using.headers]]</a>

The entities in the C++ standard library are defined in headers, whose
contents are made available to a translation unit when it contains the
appropriate `#include` preprocessing directive [[cpp.include]] or the
appropriate `import` declaration [[module.import]].

A translation unit may include library headers in any order
[[lex.separate]]. Each may be included more than once, with no effect
different from being included exactly once, except that the effect of
including either `<cassert>` or `<assert.h>` depends each time on the
lexically current definition of `NDEBUG`.[^19]

A translation unit shall include a header only outside of any
declaration or definition and, in the case of a module unit, only in its
*global-module-fragment*, and shall include the header or import the
corresponding header unit lexically before the first reference in that
translation unit to any of the entities declared in that header. No
diagnostic is required.

#### Linkage <a id="using.linkage">[[using.linkage]]</a>

Entities in the C++ standard library have external linkage
[[basic.link]]. Unless otherwise specified, objects and functions have
the default `extern "C++"` linkage [[dcl.link]].

Whether a name from the C standard library declared with external
linkage has `extern "C"` or `extern "C++"` linkage is
*implementation-defined*. It is recommended that an implementation use
`extern "C++"` linkage for this purpose.[^20]

Objects and functions defined in the library and required by a C++
program are included in the program prior to program startup.

See also replacement functions [[replacement.functions]], runtime
changes [[handler.functions]].

### Requirements on types and expressions <a id="utility.requirements">[[utility.requirements]]</a>

#### General <a id="utility.requirements.general">[[utility.requirements.general]]</a>

[[utility.arg.requirements]] describes requirements on types and
expressions used to instantiate templates defined in the C++ standard
library. [[swappable.requirements]] describes the requirements on
swappable types and swappable expressions.
[[nullablepointer.requirements]] describes the requirements on
pointer-like types that support null values. [[hash.requirements]]
describes the requirements on hash function objects.
[[allocator.requirements]] describes the requirements on storage
allocators.

#### Template argument requirements <a id="utility.arg.requirements">[[utility.arg.requirements]]</a>

The template definitions in the C++ standard library refer to various
named requirements whose details are set out in Tables 
[[tab:cpp17.equalitycomparable]]– [[tab:cpp17.destructible]]. In these
tables,

- `T` denotes an object or reference type to be supplied by a C++
  program instantiating a template,
- `a`, `b`, and `c` denote values of type (possibly const) `T`,
- `s` and `t` denote modifiable lvalues of type `T`,
- `u` denotes an identifier,
- `rv` denotes an rvalue of type `T`, and
- `v` denotes an lvalue of type (possibly const) `T` or an rvalue of
  type `const T`.

In general, a default constructor is not required. Certain container
class member function signatures specify `T()` as a default argument.
`T()` shall be a well-defined expression [[dcl.init]] if one of those
signatures is called using the default argument [[dcl.fct.default]].

**Table: Cpp17EqualityComparable requirements**

| Expression | Return type |
| ---------- | ----------- |
| `a == b`   | `decltype(a == b)` models \exposconceptx{boolean-testable}{boolean-testable} | `==` is an equivalence relation, that is, it has the following properties: For all `a`, `a == a`.; If `a == b`, then `b == a`.; If `a == b` and `b == c`, then `a == c`. |


**Table: Cpp17LessThanComparable requirements**

| Expression | Return type                                                                 | Requirement                                            |
| ---------- | --------------------------------------------------------------------------- | ------------------------------------------------------ |
| `a < b`    | `decltype(a < b)` models \exposconceptx{boolean-testable}{boolean-testable} | `<` is a strict weak ordering relation [[alg.sorting]] |


**Table: Cpp17DefaultConstructible requirements**

| Expression     | Post-condition                                                      |
| -------------- | ------------------------------------------------------------------- |
| `T t;`         | object `t` is default-initialized                                   |
| `T u{};`       | object `u` is value-initialized or aggregate-initialized            |
| `T()`<br>`T{}` | an object of type `T` is value-initialized or aggregate-initialized |


**Table: Cpp17MoveConstructible requirements**

| Expression  | Post-condition                                                     |
| ----------- | ------------------------------------------------------------------ |
| `T u = rv;` | `u` is equivalent to the value of `rv` before the construction     |
| `T(rv)`     | `T(rv)` is equivalent to the value of `rv` before the construction |
| *[spans 2 columns]*  `rv`'s state is unspecified *`rv` must still meet the requirements of the library component that is using it. The operations listed in those requirements must work as specified whether `rv` has been moved from or not.* |


**Table: Cpp17CopyConstructible requirements (in addition to Cpp17MoveConstructible)**

| Expression | Post-condition                                            |
| ---------- | --------------------------------------------------------- |
| `T u = v;` | the value of `v` is unchanged and is equivalent to ` u`   |
| `T(v)`     | the value of `v` is unchanged and is equivalent to `T(v)` |


**Table: Cpp17MoveAssignable requirements**

| Expression | Return type | Return value | Post-condition                                                                                                |
| ---------- | ----------- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| `t = rv`   | `T&`        | `t`          | If `t` and `rv` do not refer to the same object, `t` is equivalent to the value of `rv` before the assignment |
| *[spans 4 columns]*  `rv`'s state is unspecified. *`rv` must still meet the requirements of the library component that is using it, whether or not `t` and `rv` refer to the same object. The operations listed in those requirements must work as specified whether `rv` has been moved from or not.* |


**Table: Cpp17CopyAssignable requirements (in addition to Cpp17MoveAssignable)**

| Expression | Return type | Return value | Post-condition                                          |
| ---------- | ----------- | ------------ | ------------------------------------------------------- |
| `t = v`    | `T&`        | `t`          | `t` is equivalent to `v`, the value of `v` is unchanged |


**Table: Cpp17Destructible requirements**

| Expression | Post-condition                                                        |
| ---------- | --------------------------------------------------------------------- |
| `u.~T()`   | All resources owned by `u` are reclaimed, no exception is propagated. |
| *[spans 2 columns]*  *Array types and non-object types are not Cpp17Destructible.* |


#### Swappable requirements <a id="swappable.requirements">[[swappable.requirements]]</a>

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
overload resolution [[over.match]] on a candidate set that includes:

- the two `swap` function templates defined in `<utility>` and
- the lookup set produced by argument-dependent lookup
  [[basic.lookup.argdep]].

[*Note 1*: If `T` and `U` are both fundamental types or arrays of
fundamental types and the declarations from the header `<utility>` are
in scope, the overall lookup set described above is equivalent to that
of the qualified name lookup applied to the expression `std::swap(t, u)`
or `std::swap(u, t)` as appropriate. — *end note*]

[*Note 2*: It is unspecified whether a library component that has a
swappable requirement includes the header `<utility>` to ensure an
appropriate evaluation context. — *end note*]

An rvalue or lvalue `t` is *swappable* if and only if `t` is swappable
with any rvalue or lvalue, respectively, of type `T`.

A type `X` meets the *Cpp17Swappable* requirements if lvalues of type
`X` are swappable.

A type `X` meeting any of the iterator requirements
[[iterator.requirements]] meets the *Cpp17ValueSwappable* requirements
if, for any dereferenceable object `x` of type `X`, `*x` is swappable.

[*Example 1*:

User code can ensure that the evaluation of `swap` calls is performed in
an appropriate context under the various conditions as follows:

``` cpp
#include <cassert>
#include <utility>

// Preconditions: std::forward<T>(t) is swappable with std::forward<U>(u).
template<class T, class U>
void value_swap(T&& t, U&& u) {
  using std::swap;
  swap(std::forward<T>(t), std::forward<U>(u)); // OK, uses ``swappable with'' conditions
                                                // for rvalues and lvalues
}

// Preconditions: T meets the Cpp17Swappable requirements.
template<class T>
void lv_swap(T& t1, T& t2) {
  using std::swap;
  swap(t1, t2);                                 // OK, uses swappable conditions for lvalues of type T
}

namespace N {
  struct A { int m; };
  struct Proxy { A* a; };
  Proxy proxy(A& a) { return Proxy{ &a }; }

  void swap(A& x, Proxy p) {
    std::swap(x.m, p.a->m);                     // OK, uses context equivalent to swappable
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

— *end example*]

#### *Cpp17NullablePointer* requirements <a id="nullablepointer.requirements">[[nullablepointer.requirements]]</a>

A *Cpp17NullablePointer* type is a pointer-like type that supports null
values. A type `P` meets the *Cpp17NullablePointer* requirements if:

- `P` meets the *Cpp17EqualityComparable*, *Cpp17DefaultConstructible*,
  *Cpp17CopyConstructible*, *Cpp17CopyAssignable*, *Cpp17Swappable*, and
  *Cpp17Destructible* requirements,
- the expressions shown in [[cpp17.nullablepointer]] are valid and have
  the indicated semantics, and
- `P` meets all the other requirements of this subclause.

A value-initialized object of type `P` produces the null value of the
type. The null value shall be equivalent only to itself. A
default-initialized object of type `P` may have an indeterminate value.

[*Note 1*: Operations involving indeterminate values can cause
undefined behavior. — *end note*]

An object `p` of type `P` can be contextually converted to `bool`
[[conv]]. The effect shall be as if `p != nullptr` had been evaluated in
place of `p`.

No operation which is part of the *Cpp17NullablePointer* requirements
shall exit via an exception.

In [[cpp17.nullablepointer]], `u` denotes an identifier, `t` denotes a
non-`const` lvalue of type `P`, `a` and `b` denote values of type
(possibly const) `P`, and `np` denotes a value of type (possibly const)
`std::nullptr_t`.

**Table: Cpp17NullablePointer requirements**

| Expression     | Return type                                                               | Operational semantics       |
| -------------- | ------------------------------------------------------------------------- | --------------------------- |
| `P u(np);`<br> |                                                                           | Ensures: `u == nullptr`     |
| `P u = np;`    |                                                                           |                             |
| `P(np)`        |                                                                           | Ensures: `P(np) == nullptr` |
| `t = np`       | `P&`                                                                      | Ensures: `t == nullptr`     |
| `a != b`       | `decltype(a != b)` models `boolean-testable`                              | `!(a == b)`                 |
| `a == np`      | `decltype(a == np)` and `decltype(np == a)` each model `boolean-testable` | `a == P()`                  |
| `np == a`      |                                                                           |                             |
| `a != np`      | `decltype(a != np)` and `decltype(np != a)` each model `boolean-testable` | `!(a == np)`                |
| `np != a`      |                                                                           |                             |


#### *Cpp17Hash* requirements <a id="hash.requirements">[[hash.requirements]]</a>

A type `H` meets the requirements if:

- it is a function object type [[function.objects]],
- it meets the *Cpp17CopyConstructible* ([[cpp17.copyconstructible]])
  and *Cpp17Destructible* ([[cpp17.destructible]]) requirements, and
- the expressions shown in [[cpp17.hash]] are valid and have the
  indicated semantics.

Given `Key` is an argument type for function objects of type `H`, in
[[cpp17.hash]] `h` is a value of type (possibly const) `H`, `u` is an
lvalue of type `Key`, and `k` is a value of a type convertible to
(possibly const) `Key`.

[*Note 1*: Thus all evaluations of the expression `h(k)` with the same
value for `k` yield the same result for a given execution of the
program. — *end note*]

#### *Cpp17Allocator* requirements <a id="allocator.requirements">[[allocator.requirements]]</a>

##### General <a id="allocator.requirements.general">[[allocator.requirements.general]]</a>

The library describes a standard set of requirements for *allocators*,
which are class-type objects that encapsulate the information about an
allocation model. This information includes the knowledge of pointer
types, the type of their difference, the type of the size of objects in
this allocation model, as well as the memory allocation and deallocation
primitives for it. All of the string types [[strings]], containers
[[containers]] (except `array`), string buffers and string streams
[[input.output]], and `match_results` [[re]] are parameterized in terms
of allocators.

In subclause [[allocator.requirements]],

- `T`, `U`, `C` denote any cv-unqualified object type
  [[term.object.type]],
- `X` denotes an allocator class for type `T`,
- `Y` denotes the corresponding allocator class for type `U`,
- `XX` denotes the type `allocator_traits<X>`,
- `YY` denotes the type `allocator_traits<Y>`,
- `a`, `a1`, `a2` denote lvalues of type `X`,
- `u` denotes the name of a variable being declared,
- `b` denotes a value of type `Y`,
- `c` denotes a pointer of type `C*` through which indirection is valid,
- `p` denotes a value of type `XX::pointer` obtained by calling
  `a1.allocate`, where `a1 == a`,
- `q` denotes a value of type `XX::const_pointer` obtained by conversion
  from a value `p`,
- `r` denotes a value of type `T&` obtained by the expression `*p`,
- `w` denotes a value of type `XX::void_pointer` obtained by conversion
  from a value `p`,
- `x` denotes a value of type `XX::const_void_pointer` obtained by
  conversion from a value `q` or a value `w`,
- `y` denotes a value of type `XX::const_void_pointer` obtained by
  conversion from a result value of `YY::allocate`, or else a value of
  type (possibly const) `std::nullptr_t`,
- `n` denotes a value of type `XX::size_type`,
- `Args` denotes a template parameter pack, and
- `args` denotes a function parameter pack with the pattern `Args&&`.

The class template `allocator_traits` [[allocator.traits]] supplies a
uniform interface to all allocator types. This subclause describes the
requirements on allocator types and thus on types used to instantiate
`allocator_traits`. A requirement is optional if a default for a given
type or expression is specified. Within the standard library
`allocator_traits` template, an optional requirement that is not
supplied by an allocator is replaced by the specified default type or
expression.

[*Note 1*: There are no program-defined specializations of
`allocator_traits`. — *end note*]

``` cpp
typename X::pointer
```

*Remarks:* Default: `T*`

``` cpp
typename X::const_pointer
```

*Mandates:* `XX::pointer` is convertible to `XX::const_pointer`.

*Remarks:* Default: `pointer_traits<XX::pointer>::rebind<const T>`

``` cpp
typename X::void_pointer
typename Y::void_pointer
```

*Mandates:* `XX::pointer` is convertible to `XX::void_pointer`.
`XX::void_pointer` and `YY::void_pointer` are the same type.

*Remarks:* Default: `pointer_traits<XX::pointer>::rebind<void>`

``` cpp
typename X::const_void_pointer
typename Y::const_void_pointer
```

*Mandates:* `XX::pointer`, `XX::const_pointer`, and `XX::void_pointer`
are convertible to `XX::const_void_pointer`. `XX::const_void_pointer`
and `YY::const_void_pointer` are the same type.

*Remarks:* Default: `pointer_traits<XX::pointer>::rebind<const void>`

``` cpp
typename X::value_type
```

*Result:* Identical to `T`.

``` cpp
typename X::size_type
```

*Result:* An unsigned integer type that can represent the size of the
largest object in the allocation model.

*Remarks:* Default: `make_unsigned_t<XX::difference_type>`

``` cpp
typename X::difference_type
```

*Result:* A signed integer type that can represent the difference
between any two pointers in the allocation model.

*Remarks:* Default: `pointer_traits<XX::pointer>::difference_type`

``` cpp
typename X::template rebind<U>::other
```

*Result:* `Y`

*Ensures:* For all `U` (including `T`), `YY::rebind_alloc<T>` is `X`.

*Remarks:* If `Allocator` is a class template instantiation of the form
`SomeAllocator<T, Args>`, where `Args` is zero or more type arguments,
and `Allocator` does not supply a `rebind` member template, the standard
`allocator_traits` template uses `SomeAllocator<U, Args>` in place of
`Allocator::rebind<U>::other` by default. For allocator types that are
not template instantiations of the above form, no default is provided.

[*Note 1*: The member class template `rebind` of `X` is effectively a
typedef template. In general, if the name `Allocator` is bound to
`SomeAllocator<T>`, then `Allocator::rebind<U>::other` is the same type
as `SomeAllocator<U>`, where `SomeAllocator<T>::value_type` is `T` and
`SomeAllocator<U>::value_type` is `U`. — *end note*]

``` cpp
*p
```

*Result:* `T&`

``` cpp
*q
```

*Result:* `const T&`

*Ensures:* `*q` refers to the same object as `*p`.

``` cpp
p->m
```

*Result:* Type of `T::m`.

*Preconditions:* `(*p).m` is well-defined.

*Effects:* Equivalent to `(*p).m`.

``` cpp
q->m
```

*Result:* Type of `T::m`.

*Preconditions:* `(*q).m` is well-defined.

*Effects:* Equivalent to `(*q).m`.

``` cpp
static_cast<XX::pointer>(w)
```

*Result:* `XX::pointer`

*Ensures:* `static_cast<XX::pointer>(w) == p`.

``` cpp
static_cast<XX::const_pointer>(x)
```

*Result:* `XX::const_pointer`

*Ensures:* `static_cast<XX::const_pointer>(x) == q`.

``` cpp
pointer_traits<XX::pointer>::pointer_to(r)
```

*Result:* `XX::pointer`

*Ensures:* Same as `p`.

``` cpp
a.allocate(n)
```

*Result:* `XX::pointer`

*Effects:* Memory is allocated for an array of `n` `T` and such an
object is created but array elements are not constructed.

[*Example 1*: When reusing storage denoted by some pointer value `p`,
`launder(reinterpret_cast<T*>(new (p) byte[n * sizeof(T)]))` can be used
to implicitly create a suitable array object and obtain a pointer to
it. — *end example*]

*Throws:* `allocate` may throw an appropriate exception.

[*Note 2*: It is intended that `a.allocate` be an efficient means of
allocating a single object of type `T`, even when `sizeof(T)` is small.
That is, there is no need for a container to maintain its own free
list. — *end note*]

*Remarks:* If `n == 0`, the return value is unspecified.

``` cpp
a.allocate(n, y)
```

*Result:* `XX::pointer`

*Effects:* Same as `a.allocate(n)`. The use of `y` is unspecified, but
it is intended as an aid to locality.

*Remarks:* Default: `a.allocate(n)`

``` cpp
a.allocate_at_least(n)
```

*Result:* `allocation_result<XX::pointer, XX::size_type>`

*Returns:* `allocation_result<XX::pointer, XX::size_type>{ptr, count}`
where `ptr` is memory allocated for an array of `count` `T` and such an
object is created but array elements are not constructed, such that
`count` ≥ `n`. If `n == 0`, the return value is unspecified.

*Throws:* `allocate_at_least` may throw an appropriate exception.

*Remarks:* Default: `{a.allocate(n), n}`.

``` cpp
a.deallocate(p, n)
```

*Result:* (not used)

*Preconditions:*

- If `p` is memory that was obtained by a call to `a.allocate_at_least`,
  let `ret` be the value returned and `req` be the value passed as the
  first argument of that call. `p` is equal to `ret.ptr` and `n` is a
  value such that `req` ≤ `n` ≤ `ret.count`.
- Otherwise, `p` is a pointer value obtained from `allocate`. `n` equals
  the value passed as the first argument to the invocation of `allocate`
  which returned `p`.

`p` has not been invalidated by an intervening call to `deallocate`.

*Throws:* Nothing.

``` cpp
a.max_size()
```

*Result:* `XX::size_type`

*Returns:* The largest value `n` that can meaningfully be passed to
`a.allocate(n)`.

*Remarks:* Default:
`numeric_limits<size_type>::max() / sizeof(value_type)`

``` cpp
a1 == a2
```

*Result:* `bool`

*Returns:* `true` only if storage allocated from each can be deallocated
via the other.

*Throws:* Nothing.

*Remarks:* `operator==` shall be reflexive, symmetric, and transitive.

``` cpp
a1 != a2
```

*Result:* `bool`

*Returns:* `!(a1 == a2)`.

``` cpp
a == b
```

*Result:* `bool`

*Returns:* `a == YY::rebind_alloc<T>(b)`.

``` cpp
a != b
```

*Result:* `bool`

*Returns:* `!(a == b)`.

``` cpp
X u(a);
X u = a;
```

*Ensures:* `u == a`

*Throws:* Nothing.

``` cpp
X u(b);
```

*Ensures:* `Y(u) == b` and `u == X(b)`.

*Throws:* Nothing.

``` cpp
X u(std::move(a));
X u = std::move(a);
```

*Ensures:* The value of `a` is unchanged and is equal to `u`.

*Throws:* Nothing.

``` cpp
X u(std::move(b));
```

*Ensures:* `u` is equal to the prior value of `X(b)`.

*Throws:* Nothing.

``` cpp
a.construct(c, args)
```

*Result:* (not used)

*Effects:* Constructs an object of type `C` at `c`.

*Remarks:* Default: `construct_at(c, std::forward<Args>(args)...)`

``` cpp
a.destroy(c)
```

*Result:* (not used)

*Effects:* Destroys the object at `c`.

*Remarks:* Default: `destroy_at(c)`

``` cpp
a.select_on_container_copy_construction()
```

*Result:* `X`

*Returns:* Typically returns either `a` or `X()`.

*Remarks:* Default: `return a;`

``` cpp
typename X::propagate_on_container_copy_assignment
```

*Result:* Identical to or derived from `true_type` or `false_type`.

*Returns:* `true_type` only if an allocator of type `X` should be copied
when the client container is copy-assigned; if so, `X` shall meet the
*Cpp17CopyAssignable* requirements ([[cpp17.copyassignable]]) and the
copy operation shall not throw exceptions.

*Remarks:* Default: `false_type`

``` cpp
typename X::propagate_on_container_move_assignment
```

*Result:* Identical to or derived from `true_type` or `false_type`.

*Returns:* `true_type` only if an allocator of type `X` should be moved
when the client container is move-assigned; if so, `X` shall meet the
*Cpp17MoveAssignable* requirements ([[cpp17.moveassignable]]) and the
move operation shall not throw exceptions.

*Remarks:* Default: `false_type`

``` cpp
typename X::propagate_on_container_swap
```

*Result:* Identical to or derived from `true_type` or `false_type`.

*Returns:* `true_type` only if an allocator of type `X` should be
swapped when the client container is swapped; if so, `X` shall meet the
*Cpp17Swappable* requirements [[swappable.requirements]] and the `swap`
operation shall not throw exceptions.

*Remarks:* Default: `false_type`

``` cpp
typename X::is_always_equal
```

*Result:* Identical to or derived from `true_type` or `false_type`.

*Returns:* `true_type` only if the expression `a1 == a2` is guaranteed
to be `true` for any two (possibly const) values `a1`, `a2` of type `X`.

*Remarks:* Default: `is_empty<X>::type`

An allocator type `X` shall meet the *Cpp17CopyConstructible*
requirements ([[cpp17.copyconstructible]]). The `XX::pointer`,
`XX::const_pointer`, `XX::void_pointer`, and `XX::const_void_pointer`
types shall meet the *Cpp17NullablePointer* requirements (
[[cpp17.nullablepointer]]). No constructor, comparison operator
function, copy operation, move operation, or swap operation on these
pointer types shall exit via an exception. `XX::pointer` and
`XX::const_pointer` shall also meet the requirements for a
*Cpp17RandomAccessIterator* [[random.access.iterators]] and the
additional requirement that, when `p` and `(p + n)` are dereferenceable
pointer values for some integral value `n`,

``` cpp
addressof(*(p + n)) == addressof(*p) + n
```

is `true`.

Let `x1` and `x2` denote objects of (possibly different) types
`XX::void_pointer`, `XX::const_void_pointer`, `XX::pointer`, or
`XX::const_pointer`. Then, `x1` and `x2` are *equivalently-valued*
pointer values, if and only if both `x1` and `x2` can be explicitly
converted to the two corresponding objects `px1` and `px2` of type
`XX::const_pointer`, using a sequence of `static_cast`s using only these
four types, and the expression `px1 == px2` evaluates to `true`.

Let `w1` and `w2` denote objects of type `XX::void_pointer`. Then for
the expressions

``` cpp
w1 == w2
w1 != w2
```

either or both objects may be replaced by an equivalently-valued object
of type `XX::const_void_pointer` with no change in semantics.

Let `p1` and `p2` denote objects of type `XX::pointer`. Then for the
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
of type `XX::const_pointer` with no change in semantics.

An allocator may constrain the types on which it can be instantiated and
the arguments for which its `construct` or `destroy` members may be
called. If a type cannot be used with a particular allocator, the
allocator class or the call to `construct` or `destroy` may fail to
instantiate.

If the alignment associated with a specific over-aligned type is not
supported by an allocator, instantiation of the allocator for that type
may fail. The allocator also may silently ignore the requested
alignment.

[*Note 2*: Additionally, the member function `allocate` for that type
can fail by throwing an object of type `bad_alloc`. — *end note*]

[*Example 1*:

The following is an allocator class template supporting the minimal
interface that meets the requirements of
[[allocator.requirements.general]]:

``` cpp
template<class T>
struct SimpleAllocator {
  using value_type = T;
  SimpleAllocator(ctor args);

  template<class U> SimpleAllocator(const SimpleAllocator<U>& other);

  T* allocate(std::size_t n);
  void deallocate(T* p, std::size_t n);

  template<class U> bool operator==(const SimpleAllocator<U>& rhs) const;
};
```

— *end example*]

##### Allocator completeness requirements <a id="allocator.requirements.completeness">[[allocator.requirements.completeness]]</a>

If `X` is an allocator class for type `T`, `X` additionally meets the
allocator completeness requirements if, whether or not `T` is a complete
type:

- `X` is a complete type, and
- all the member types of `allocator_traits<X>` [[allocator.traits]]
  other than `value_type` are complete types.

### Constraints on programs <a id="constraints">[[constraints]]</a>

#### Overview <a id="constraints.overview">[[constraints.overview]]</a>

Subclause [[constraints]] describes restrictions on C++ programs that
use the facilities of the C++ standard library. The following subclauses
specify constraints on the program’s use of namespaces
[[namespace.std]], its use of various reserved names [[reserved.names]],
its use of headers [[alt.headers]], its use of standard library classes
as base classes [[derived.classes]], its definitions of replacement
functions [[replacement.functions]], and its installation of handler
functions during execution [[handler.functions]].

#### Namespace use <a id="namespace.constraints">[[namespace.constraints]]</a>

##### Namespace `std` <a id="namespace.std">[[namespace.std]]</a>

Unless otherwise specified, the behavior of a C++ program is undefined
if it adds declarations or definitions to namespace `std` or to a
namespace within namespace `std`.

Unless explicitly prohibited, a program may add a template
specialization for any standard library class template to namespace
`std` provided that (a) the added declaration depends on at least one
program-defined type and (b) the specialization meets the standard
library requirements for the original template.[^21]

The behavior of a C++ program is undefined if it declares an explicit or
partial specialization of any standard library variable template, except
where explicitly permitted by the specification of that variable
template.

[*Note 1*: The requirements on an explicit or partial specialization
are stated by each variable template that grants such
permission. — *end note*]

The behavior of a C++ program is undefined if it declares

- an explicit specialization of any member function of a standard
  library class template, or
- an explicit specialization of any member function template of a
  standard library class or class template, or
- an explicit or partial specialization of any member class template of
  a standard library class or class template, or
- a deduction guide for any standard library class template.

A program may explicitly instantiate a class template defined in the
standard library only if the declaration (a) depends on the name of at
least one program-defined type and (b) the instantiation meets the
standard library requirements for the original template.

Let `F` denote a standard library function [[global.functions]], a
standard library static member function, or an instantiation of a
standard library function template. Unless `F` is designated an
*addressable function*, the behavior of a C++ program is unspecified
(possibly ill-formed) if it explicitly or implicitly attempts to form a
pointer to `F`.

[*Note 2*: Possible means of forming such pointers include application
of the unary `&` operator [[expr.unary.op]], `addressof`
[[specialized.addressof]], or a function-to-pointer standard conversion
[[conv.func]]. — *end note*]

Moreover, the behavior of a C++ program is unspecified (possibly
ill-formed) if it attempts to form a reference to `F` or if it attempts
to form a pointer-to-member designating either a standard library
non-static member function [[member.functions]] or an instantiation of a
standard library member function template.

A translation unit shall not declare namespace `std` to be an inline
namespace [[namespace.def]].

##### Namespace `posix` <a id="namespace.posix">[[namespace.posix]]</a>

The behavior of a C++ program is undefined if it adds declarations or
definitions to namespace `posix` or to a namespace within namespace
`posix` unless otherwise specified. The namespace `posix` is reserved
for use by ISO/IEC/IEEE 9945 and other POSIX standards.

##### Namespaces for future standardization <a id="namespace.future">[[namespace.future]]</a>

Top-level namespaces whose *namespace-name* consists of `std` followed
by one or more *digit*s [[lex.name]] are reserved for future
standardization. The behavior of a C++ program is undefined if it adds
declarations or definitions to such a namespace.

[*Example 1*: The top-level namespace `std2` is reserved for use by
future revisions of this International Standard. — *end example*]

#### Reserved names <a id="reserved.names">[[reserved.names]]</a>

##### General <a id="reserved.names.general">[[reserved.names.general]]</a>

The C++ standard library reserves the following kinds of names:

- macros
- global names
- names with external linkage

If a program declares or defines a name in a context where it is
reserved, other than as explicitly allowed by [[library]], its behavior
is undefined.

##### Zombie names <a id="zombie.names">[[zombie.names]]</a>

In namespace `std`, the following names are reserved for previous
standardization:

- `auto_ptr`,
- `auto_ptr_ref`,
- `binary_function`,
- `binary_negate`,
- `bind1st`,
- `bind2nd`,
- `binder1st`,
- `binder2nd`,
- `const_mem_fun1_ref_t`,
- `const_mem_fun1_t`,
- `const_mem_fun_ref_t`,
- `const_mem_fun_t`,
- `declare_no_pointers`,
- `declare_reachable`,
- `get_pointer_safety`,
- `get_temporary_buffer`,
- `get_unexpected`,
- `gets`,
- `is_literal_type`,
- `is_literal_type_v`,
- `mem_fun1_ref_t`,
- `mem_fun1_t`,
- `mem_fun_ref_t`,
- `mem_fun_ref`,
- `mem_fun_t`,
- `mem_fun`,
- `not1`,
- `not2`,
- `pointer_safety`,
- `pointer_to_binary_function`,
- `pointer_to_unary_function`,
- `ptr_fun`,
- `random_shuffle`,
- `raw_storage_iterator`,
- `result_of`,
- `result_of_t`,
- `return_temporary_buffer`,
- `set_unexpected`,
- `unary_function`,
- `unary_negate`,
- `uncaught_exception`,
- `undeclare_no_pointers`,
- `undeclare_reachable`, and
- `unexpected_handler`.

The following names are reserved as members for previous
standardization, and may not be used as a name for object-like macros in
portable code:

- `argument_type`,
- `first_argument_type`,
- `io_state`,
- `open_mode`,
- `preferred`,
- `second_argument_type`,
- `seek_dir`, and.
- `strict`.

The name `stossc` is reserved as a member function for previous
standardization, and may not be used as a name for function-like macros
in portable code.

The header names , , , , and are reserved for previous standardization.

##### Macro names <a id="macro.names">[[macro.names]]</a>

A translation unit that includes a standard library header shall not
`#define` or `#undef` names declared in any standard library header.

A translation unit shall not `#define` or `#undef` names lexically
identical to keywords, to the identifiers listed in
[[lex.name.special]], or to the *attribute-token*s described in 
[[dcl.attr]], except that the names `likely` and `unlikely` may be
defined as function-like macros  [[cpp.replace]].

##### External linkage <a id="extern.names">[[extern.names]]</a>

Each name declared as an object with external linkage in a header is
reserved to the implementation to designate that library object with
external linkage, [^22]

both in namespace `std` and in the global namespace.

Each global function signature declared with external linkage in a
header is reserved to the implementation to designate that function
signature with external linkage.[^23]

Each name from the C standard library declared with external linkage is
reserved to the implementation for use as a name with `extern "C"`
linkage, both in namespace `std` and in the global namespace.

Each function signature from the C standard library declared with
external linkage is reserved to the implementation for use as a function
signature with both `extern "C"` and `extern "C++"` linkage,[^24]

or as a name of namespace scope in the global namespace.

##### Types <a id="extern.types">[[extern.types]]</a>

For each type `T` from the C standard library, the types `::T` and
`std::T` are reserved to the implementation and, when defined, `::T`
shall be identical to `std::T`.

##### User-defined literal suffixes <a id="usrlit.suffix">[[usrlit.suffix]]</a>

Literal suffix identifiers [[over.literal]] that do not start with an
underscore are reserved for future standardization. Literal suffix
identifiers that contain a double underscore `__` are reserved for use
by C++ implementations.

#### Headers <a id="alt.headers">[[alt.headers]]</a>

If a file with a name equivalent to the derived file name for one of the
C++ standard library headers is not provided as part of the
implementation, and a file with that name is placed in any of the
standard places for a source file to be included [[cpp.include]], the
behavior is undefined.

#### Derived classes <a id="derived.classes">[[derived.classes]]</a>

Virtual member function signatures defined for a base class in the C++
standard library may be overridden in a derived class defined in the
program [[class.virtual]].

#### Replacement functions <a id="replacement.functions">[[replacement.functions]]</a>

[[support]] through [[thread]] and [[depr]] describe the behavior of
numerous functions defined by the C++ standard library. Under some
circumstances, however, certain of these function descriptions also
apply to replacement functions defined in the program.

A C++ program may provide the definition for any of the following
dynamic memory allocation function signatures declared in header `<new>`
[[basic.stc.dynamic]], [[new.syn]]:

``` cpp
operator new(std::size_t)
operator new(std::size_t, std::align_val_t)
operator new(std::size_t, const std::nothrow_t&)
operator new(std::size_t, std::align_val_t, const std::nothrow_t&)
```

``` cpp
operator delete(void*)
operator delete(void*, std::size_t)
operator delete(void*, std::align_val_t)
operator delete(void*, std::size_t, std::align_val_t)
operator delete(void*, const std::nothrow_t&)
operator delete(void*, std::align_val_t, const std::nothrow_t&)
```

``` cpp
operator new[](std::size_t)
operator new[](std::size_t, std::align_val_t)
operator new[](std::size_t, const std::nothrow_t&)
operator new[](std::size_t, std::align_val_t, const std::nothrow_t&)
```

``` cpp
operator delete[](void*)
operator delete[](void*, std::size_t)
operator delete[](void*, std::align_val_t)
operator delete[](void*, std::size_t, std::align_val_t)
operator delete[](void*, const std::nothrow_t&)
operator delete[](void*, std::align_val_t, const std::nothrow_t&)
```

The program’s definitions are used instead of the default versions
supplied by the implementation [[new.delete]]. Such replacement occurs
prior to program startup [[basic.def.odr]], [[basic.start]]. The
program’s declarations shall not be specified as `inline`. No diagnostic
is required.

#### Handler functions <a id="handler.functions">[[handler.functions]]</a>

The C++ standard library provides a default version of the following
handler function [[support]]:

- `terminate_handler`

A C++ program may install different handler functions during execution,
by supplying a pointer to a function defined in the program or the
library as an argument to (respectively):

- `set_new_handler`
- `set_terminate`

See also subclauses  [[alloc.errors]], Storage allocation errors, and 
[[support.exception]], Exception handling.

A C++ program can get a pointer to the current handler function by
calling the following functions:

- `get_new_handler`
- `get_terminate`

Calling the `set_*` and `get_*` functions shall not incur a data race. A
call to any of the `set_*` functions shall synchronize with subsequent
calls to the same `set_*` function and to the corresponding `get_*`
function.

#### Other functions <a id="res.on.functions">[[res.on.functions]]</a>

In certain cases (replacement functions, handler functions, operations
on types used to instantiate standard library template components), the
C++ standard library depends on components supplied by a C++ program. If
these components do not meet their requirements, this document places no
requirements on the implementation.

In particular, the behavior is undefined in the following cases:

- For replacement functions [[new.delete]], if the installed replacement
  function does not implement the semantics of the applicable *Required
  behavior:* paragraph.
- For handler functions [[new.handler]], [[terminate.handler]], if the
  installed handler function does not implement the semantics of the
  applicable *Required behavior:* paragraph.
- For types used as template arguments when instantiating a template
  component, if the operations on the type do not implement the
  semantics of the applicable *Requirements* subclause
  [[allocator.requirements]], [[container.requirements]], [[iterator.requirements]], [[algorithms.requirements]], [[numeric.requirements]].
  Operations on such types can report a failure by throwing an exception
  unless otherwise specified.
- If any replacement function or handler function or destructor
  operation exits via an exception, unless specifically allowed in the
  applicable *Required behavior:* paragraph.
- If an incomplete type [[term.incomplete.type]] is used as a template
  argument when instantiating a template component or evaluating a
  concept, unless specifically allowed for that component.

#### Function arguments <a id="res.on.arguments">[[res.on.arguments]]</a>

Each of the following applies to all arguments to functions defined in
the C++ standard library, unless explicitly stated otherwise.

- If an argument to a function has an invalid value (such as a value
  outside the domain of the function or a pointer invalid for its
  intended use), the behavior is undefined.
- If a function argument is described as being an array, the pointer
  actually passed to the function shall have a value such that all
  address computations and accesses to objects (that would be valid if
  the pointer did point to the first element of such an array) are in
  fact valid.
- If a function argument is bound to an rvalue reference parameter, the
  implementation may assume that this parameter is a unique reference to
  this argument, except that the argument passed to a move-assignment
  operator may be a reference to `*this` [[lib.types.movedfrom]].
  \[*Note 3*: If the type of a parameter is a forwarding reference
  [[temp.deduct.call]] that is deduced to an lvalue reference type, then
  the argument is not bound to an rvalue reference. — *end note*]
  \[*Note 4*: If a program casts an lvalue to an xvalue while passing
  that lvalue to a library function (e.g., by calling the function with
  the argument `std::move(x)`), the program is effectively asking that
  function to treat that lvalue as a temporary object. The
  implementation is free to optimize away aliasing checks which would
  possibly be needed if the argument was an lvalue. — *end note*]

#### Library object access <a id="res.on.objects">[[res.on.objects]]</a>

The behavior of a program is undefined if calls to standard library
functions from different threads may introduce a data race. The
conditions under which this may occur are specified in 
[[res.on.data.races]].

[*Note 1*: Modifying an object of a standard library type that is
shared between threads risks undefined behavior unless objects of that
type are explicitly specified as being shareable without data races or
the user supplies a locking mechanism. — *end note*]

If an object of a standard library type is accessed, and the beginning
of the object’s lifetime [[basic.life]] does not happen before the
access, or the access does not happen before the end of the object’s
lifetime, the behavior is undefined unless otherwise specified.

[*Note 2*: This applies even to objects such as mutexes intended for
thread synchronization. — *end note*]

#### Semantic requirements <a id="res.on.requirements">[[res.on.requirements]]</a>

A sequence `Args` of template arguments is said to *model* a concept `C`
if `Args` satisfies `C` [[temp.constr.decl]] and meets all semantic
requirements (if any) given in the specification of `C`.

If the validity or meaning of a program depends on whether a sequence of
template arguments models a concept, and the concept is satisfied but
not modeled, the program is ill-formed, no diagnostic required.

If the semantic requirements of a declaration’s constraints
[[structure.requirements]] are not modeled at the point of use, the
program is ill-formed, no diagnostic required.

### Conforming implementations <a id="conforming">[[conforming]]</a>

#### Overview <a id="conforming.overview">[[conforming.overview]]</a>

Subclause [[conforming]] describes the constraints upon, and latitude
of, implementations of the C++ standard library.

An implementation’s use of headers is discussed in  [[res.on.headers]],
its use of macros in  [[res.on.macro.definitions]], non-member functions
in  [[global.functions]], member functions in  [[member.functions]],
data race avoidance in  [[res.on.data.races]], access specifiers in 
[[protection.within.classes]], class derivation in  [[derivation]], and
exceptions in  [[res.on.exception.handling]].

#### Headers <a id="res.on.headers">[[res.on.headers]]</a>

A C++ header may include other C++ headers. A C++ header shall provide
the declarations and definitions that appear in its synopsis. A C++
header shown in its synopsis as including other C++ headers shall
provide the declarations and definitions that appear in the synopses of
those other headers.

Certain types and macros are defined in more than one header. Every such
entity shall be defined such that any header that defines it may be
included after any other header that also defines it [[basic.def.odr]].

The C standard library headers [[support.c.headers]] shall include only
their corresponding C++ standard library header, as described in 
[[headers]].

#### Restrictions on macro definitions <a id="res.on.macro.definitions">[[res.on.macro.definitions]]</a>

The names and global function signatures described in  [[contents]] are
reserved to the implementation.

All object-like macros defined by the C standard library and described
in this Clause as expanding to integral constant expressions are also
suitable for use in `#if` preprocessing directives, unless explicitly
stated otherwise.

#### Non-member functions <a id="global.functions">[[global.functions]]</a>

It is unspecified whether any non-member functions in the C++ standard
library are defined as inline [[dcl.inline]].

A call to a non-member function signature described in [[support]]
through [[thread]] and [[depr]] shall behave as if the implementation
declared no additional non-member function signatures.[^25]

An implementation shall not declare a non-member function signature with
additional default arguments.

Unless otherwise specified, calls made by functions in the standard
library to non-operator, non-member functions do not use functions from
another namespace which are found through argument-dependent name lookup
[[basic.lookup.argdep]].

[*Note 1*:

The phrase “unless otherwise specified” applies to cases such as the
swappable with requirements [[swappable.requirements]]. The exception
for overloaded operators allows argument-dependent lookup in cases like
that of `ostream_iterator::operator=` [[ostream.iterator.ops]]:

*Effects:*

``` cpp
*out_stream << value;
if (delim != 0)
  *out_stream << delim;
return *this;
```

— *end note*]

#### Member functions <a id="member.functions">[[member.functions]]</a>

It is unspecified whether any member functions in the C++ standard
library are defined as inline [[dcl.inline]].

For a non-virtual member function described in the C++ standard library,
an implementation may declare a different set of member function
signatures, provided that any call to the member function that would
select an overload from the set of declarations described in this
document behaves as if that overload were selected.

[*Note 1*: For instance, an implementation can add parameters with
default values, or replace a member function with default arguments with
two or more member functions with equivalent behavior, or add additional
signatures for a member function name. — *end note*]

#### Friend functions <a id="hidden.friends">[[hidden.friends]]</a>

Whenever this document specifies a friend declaration of a function or
function template within a class or class template definition, that
declaration shall be the only declaration of that function or function
template provided by an implementation.

[*Note 1*: In particular, an implementation is not allowed to provide
an additional declaration of that function or function template at
namespace scope. — *end note*]

[*Note 2*: Such a friend function or function template declaration is
known as a hidden friend, as it is visible neither to ordinary
unqualified lookup [[basic.lookup.unqual]] nor to qualified lookup
[[basic.lookup.qual]]. — *end note*]

#### Constexpr functions and constructors <a id="constexpr.functions">[[constexpr.functions]]</a>

This document explicitly requires that certain standard library
functions are `constexpr` [[dcl.constexpr]]. An implementation shall not
declare any standard library function signature as `constexpr` except
for those where it is explicitly required. Within any header that
provides any non-defining declarations of constexpr functions or
constructors an implementation shall provide corresponding definitions.

#### Requirements for stable algorithms <a id="algorithm.stable">[[algorithm.stable]]</a>

When the requirements for an algorithm state that it is “stable” without
further elaboration, it means:

- For the sort algorithms the relative order of equivalent elements is
  preserved.
- For the remove and copy algorithms the relative order of the elements
  that are not removed is preserved.
- For the merge algorithms, for equivalent elements in the original two
  ranges, the elements from the first range (preserving their original
  order) precede the elements from the second range (preserving their
  original order).

#### Reentrancy <a id="reentrancy">[[reentrancy]]</a>

Except where explicitly specified in this document, it is
*implementation-defined* which functions in the C++ standard library may
be recursively reentered.

#### Data race avoidance <a id="res.on.data.races">[[res.on.data.races]]</a>

This subclause specifies requirements that implementations shall meet to
prevent data races [[intro.multithread]]. Every standard library
function shall meet each requirement unless otherwise specified.
Implementations may prevent data races in cases other than those
specified below.

A C++ standard library function shall not directly or indirectly access
objects [[intro.multithread]] accessible by threads other than the
current thread unless the objects are accessed directly or indirectly
via the function’s arguments, including `this`.

A C++ standard library function shall not directly or indirectly modify
objects [[intro.multithread]] accessible by threads other than the
current thread unless the objects are accessed directly or indirectly
via the function’s non-const arguments, including `this`.

[*Note 1*: This means, for example, that implementations can’t use an
object with static storage duration for internal purposes without
synchronization because doing so can cause a data race even in programs
that do not explicitly share objects between threads. — *end note*]

A C++ standard library function shall not access objects indirectly
accessible via its arguments or via elements of its container arguments
except by invoking functions required by its specification on those
container elements.

Operations on iterators obtained by calling a standard library container
or string member function may access the underlying container, but shall
not modify it.

[*Note 2*: In particular, container operations that invalidate
iterators conflict with operations on iterators associated with that
container. — *end note*]

Implementations may share their own internal objects between threads if
the objects are not visible to users and are protected against data
races.

Unless otherwise specified, C++ standard library functions shall perform
all operations solely within the current thread if those operations have
effects that are visible [[intro.multithread]] to users.

[*Note 3*: This allows implementations to parallelize operations if
there are no visible side effects. — *end note*]

#### Protection within classes <a id="protection.within.classes">[[protection.within.classes]]</a>

It is unspecified whether any function signature or class described in
[[support]] through [[thread]] and [[depr]] is a friend of another class
in the C++ standard library.

#### Derived classes <a id="derivation">[[derivation]]</a>

An implementation may derive any class in the C++ standard library from
a class with a name reserved to the implementation.

Certain classes defined in the C++ standard library are required to be
derived from other classes in the C++ standard library. An
implementation may derive such a class directly from the required base
or indirectly through a hierarchy of base classes with names reserved to
the implementation.

In any case:

- Every base class described as `virtual` shall be virtual;
- Every base class not specified as `virtual` shall not be virtual;
- Unless explicitly stated otherwise, types with distinct names shall be
  distinct types. \[*Note 5*: There is an implicit exception to this
  rule for types that are described as synonyms
  [[dcl.typedef]], [[namespace.udecl]], such as `size_t`
  [[support.types]] and `streamoff` [[stream.types]]. — *end note*]

All types specified in the C++ standard library shall be non-`final`
types unless otherwise specified.

#### Restrictions on exception handling <a id="res.on.exception.handling">[[res.on.exception.handling]]</a>

Any of the functions defined in the C++ standard library can report a
failure by throwing an exception of a type described in its *Throws:*
paragraph, or of a type derived from a type named in the *Throws:*
paragraph that would be caught by an exception handler for the base
type.

Functions from the C standard library shall not throw exceptions [^26]

except when such a function calls a program-supplied function that
throws an exception.[^27]

Destructor operations defined in the C++ standard library shall not
throw exceptions. Every destructor in the C++ standard library shall
behave as if it had a non-throwing exception specification.

Functions defined in the C++ standard library that do not have a
*Throws:* paragraph but do have a potentially-throwing exception
specification may throw *implementation-defined* exceptions.[^28]

Implementations should report errors by throwing exceptions of or
derived from the standard exception classes
[[bad.alloc]], [[support.exception]], [[std.exceptions]].

An implementation may strengthen the exception specification for a
non-virtual function by adding a non-throwing exception specification.

#### Value of error codes <a id="value.error.codes">[[value.error.codes]]</a>

Certain functions in the C++ standard library report errors via a
`std::error_code` [[syserr.errcode.overview]] object. That object’s
`category()` member shall return `std::system_category()` for errors
originating from the operating system, or a reference to an
*implementation-defined* `error_category` object for errors originating
elsewhere. The implementation shall define the possible values of
`value()` for each of these error categories.

[*Example 1*: For operating systems that are based on POSIX,
implementations should define the `std::system_category()` values as
identical to the POSIX `errno` values, with additional values as defined
by the operating system’s documentation. Implementations for operating
systems that are not based on POSIX should define values identical to
the operating system’s values. For errors that do not originate from the
operating system, the implementation may provide enums for the
associated values. — *end example*]

#### Moved-from state of library types <a id="lib.types.movedfrom">[[lib.types.movedfrom]]</a>

Objects of types defined in the C++ standard library may be moved from
[[class.copy.ctor]]. Move operations may be explicitly specified or
implicitly generated. Unless otherwise specified, such moved-from
objects shall be placed in a valid but unspecified state.

An object of a type defined in the C++ standard library may be
move-assigned [[class.copy.assign]] to itself. Unless otherwise
specified, such an assignment places the object in a valid but
unspecified state.

<!-- Link reference definitions -->
[alg.c.library]: algorithms.md#alg.c.library
[alg.sorting]: algorithms.md#alg.sorting
[algorithm.stable]: #algorithm.stable
[algorithms]: algorithms.md#algorithms
[algorithms.requirements]: algorithms.md#algorithms.requirements
[alloc.errors]: support.md#alloc.errors
[allocator.requirements]: #allocator.requirements
[allocator.requirements.completeness]: #allocator.requirements.completeness
[allocator.requirements.general]: #allocator.requirements.general
[allocator.traits]: mem.md#allocator.traits
[alt.headers]: #alt.headers
[array.creation]: containers.md#array.creation
[atomics]: thread.md#atomics
[bad.alloc]: support.md#bad.alloc
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.start]: basic.md#basic.start
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[bit]: utilities.md#bit
[bitmask.types]: #bitmask.types
[byte.strings]: #byte.strings
[c.annex.k.names]: #c.annex.k.names
[cassert.syn]: diagnostics.md#cassert.syn
[cerrno.syn]: diagnostics.md#cerrno.syn
[character.seq]: #character.seq
[character.seq.general]: #character.seq.general
[class.copy.assign]: class.md#class.copy.assign
[class.copy.ctor]: class.md#class.copy.ctor
[class.dtor]: class.md#class.dtor
[class.mem]: class.md#class.mem
[class.virtual]: class.md#class.virtual
[clocale.syn]: localization.md#clocale.syn
[cmp]: support.md#cmp
[compliance]: #compliance
[concept.destructible]: concepts.md#concept.destructible
[concept.invocable]: concepts.md#concept.invocable
[concept.totallyordered]: concepts.md#concept.totallyordered
[concepts]: concepts.md#concepts
[concepts.equality]: concepts.md#concepts.equality
[concepts.object]: concepts.md#concepts.object
[conforming]: #conforming
[conforming.overview]: #conforming.overview
[constexpr.functions]: #constexpr.functions
[constraints]: #constraints
[constraints.overview]: #constraints.overview
[container.requirements]: containers.md#container.requirements
[containers]: containers.md#containers
[contents]: #contents
[conv]: expr.md#conv
[conv.func]: expr.md#conv.func
[conventions]: #conventions
[conventions.general]: #conventions.general
[cpp.include]: cpp.md#cpp.include
[cpp.replace]: cpp.md#cpp.replace
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.destructible]: #cpp17.destructible
[cpp17.hash]: #cpp17.hash
[cpp17.moveassignable]: #cpp17.moveassignable
[cpp17.nullablepointer]: #cpp17.nullablepointer
[cstdarg.syn]: support.md#cstdarg.syn
[cstddef.syn]: support.md#cstddef.syn
[cstdint.syn]: support.md#cstdint.syn
[customization.point.object]: #customization.point.object
[dcl.array]: dcl.md#dcl.array
[dcl.attr]: dcl.md#dcl.attr
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.inline]: dcl.md#dcl.inline
[dcl.link]: dcl.md#dcl.link
[dcl.pre]: dcl.md#dcl.pre
[dcl.typedef]: dcl.md#dcl.typedef
[defns.nonconst.libcall]: intro.md#defns.nonconst.libcall
[depr]: #depr
[derivation]: #derivation
[derived.classes]: #derived.classes
[description]: #description
[description.general]: #description.general
[diagnostics]: diagnostics.md#diagnostics
[enumerated.types]: #enumerated.types
[except]: except.md#except
[expos.only.entity]: #expos.only.entity
[expr.delete]: expr.md#expr.delete
[expr.new]: expr.md#expr.new
[expr.unary.op]: expr.md#expr.unary.op
[extern.names]: #extern.names
[extern.types]: #extern.types
[freestanding.item]: #freestanding.item
[function.objects]: utilities.md#function.objects
[functions.within.classes]: #functions.within.classes
[global.functions]: #global.functions
[handler.functions]: #handler.functions
[hash.requirements]: #hash.requirements
[headers]: #headers
[headers.cpp]: #headers.cpp
[headers.cpp.c]: #headers.cpp.c
[headers.cpp.fs]: #headers.cpp.fs
[hidden.friends]: #hidden.friends
[input.output]: input.md#input.output
[intro.compliance]: intro.md#intro.compliance
[intro.multithread]: basic.md#intro.multithread
[intro.refs]: intro.md#intro.refs
[iterator.requirements]: iterators.md#iterator.requirements
[iterators]: iterators.md#iterators
[lex.charset]: lex.md#lex.charset
[lex.name]: lex.md#lex.name
[lex.name.special]: #lex.name.special
[lex.phases]: lex.md#lex.phases
[lex.separate]: lex.md#lex.separate
[lib.types.movedfrom]: #lib.types.movedfrom
[library]: #library
[library.c]: #library.c
[library.categories]: #library.categories
[library.general]: #library.general
[locales]: localization.md#locales
[localization]: localization.md#localization
[macro.names]: #macro.names
[mem]: mem.md#mem
[member.functions]: #member.functions
[memory]: mem.md#memory
[meta]: meta.md#meta
[module.import]: module.md#module.import
[multibyte.strings]: #multibyte.strings
[namespace.constraints]: #namespace.constraints
[namespace.def]: dcl.md#namespace.def
[namespace.future]: #namespace.future
[namespace.posix]: #namespace.posix
[namespace.std]: #namespace.std
[namespace.udecl]: dcl.md#namespace.udecl
[new.delete]: support.md#new.delete
[new.handler]: support.md#new.handler
[new.syn]: support.md#new.syn
[nullablepointer.requirements]: #nullablepointer.requirements
[numeric.requirements]: numerics.md#numeric.requirements
[numerics]: numerics.md#numerics
[objects.within.classes]: #objects.within.classes
[organization]: #organization
[organization.general]: #organization.general
[ostream.iterator.ops]: iterators.md#ostream.iterator.ops
[over.literal]: over.md#over.literal
[over.match]: over.md#over.match
[over.match.oper]: over.md#over.match.oper
[protection.within.classes]: #protection.within.classes
[random.access.iterators]: iterators.md#random.access.iterators
[ranges]: ranges.md#ranges
[ratio]: meta.md#ratio
[re]: re.md#re
[reentrancy]: #reentrancy
[replacement.functions]: #replacement.functions
[requirements]: #requirements
[requirements.general]: #requirements.general
[res.on.arguments]: #res.on.arguments
[res.on.data.races]: #res.on.data.races
[res.on.exception.handling]: #res.on.exception.handling
[res.on.functions]: #res.on.functions
[res.on.headers]: #res.on.headers
[res.on.macro.definitions]: #res.on.macro.definitions
[res.on.objects]: #res.on.objects
[res.on.requirements]: #res.on.requirements
[reserved.names]: #reserved.names
[reserved.names.general]: #reserved.names.general
[specialized.addressof]: mem.md#specialized.addressof
[std.exceptions]: diagnostics.md#std.exceptions
[std.modules]: #std.modules
[stmt.return]: stmt.md#stmt.return
[stream.types]: input.md#stream.types
[strings]: strings.md#strings
[structure]: #structure
[structure.elements]: #structure.elements
[structure.requirements]: #structure.requirements
[structure.see.also]: #structure.see.also
[structure.specifications]: #structure.specifications
[structure.summary]: #structure.summary
[support]: support.md#support
[support.c.headers]: support.md#support.c.headers
[support.c.headers.other]: support.md#support.c.headers.other
[support.coroutine]: support.md#support.coroutine
[support.dynamic]: support.md#support.dynamic
[support.exception]: support.md#support.exception
[support.initlist]: support.md#support.initlist
[support.limits]: support.md#support.limits
[support.rtti]: support.md#support.rtti
[support.runtime]: support.md#support.runtime
[support.srcloc]: support.md#support.srcloc
[support.start.term]: support.md#support.start.term
[support.types]: support.md#support.types
[swappable.requirements]: #swappable.requirements
[syserr]: diagnostics.md#syserr
[syserr.errcode.overview]: diagnostics.md#syserr.errcode.overview
[tab:cpp17.destructible]: #tab:cpp17.destructible
[tab:cpp17.equalitycomparable]: #tab:cpp17.equalitycomparable
[temp]: temp.md#temp
[temp.concept]: temp.md#temp.concept
[temp.constr.decl]: temp.md#temp.constr.decl
[temp.deduct.call]: temp.md#temp.deduct.call
[template.bitset]: utilities.md#template.bitset
[term.incomplete.type]: basic.md#term.incomplete.type
[term.object.type]: basic.md#term.object.type
[terminate.handler]: support.md#terminate.handler
[thread]: thread.md#thread
[time]: time.md#time
[tuple]: utilities.md#tuple
[type.descriptions]: #type.descriptions
[type.descriptions.general]: #type.descriptions.general
[type.traits]: meta.md#type.traits
[using]: #using
[using.headers]: #using.headers
[using.linkage]: #using.linkage
[using.overview]: #using.overview
[usrlit.suffix]: #usrlit.suffix
[utilities]: utilities.md#utilities
[utility]: utilities.md#utility
[utility.arg.requirements]: #utility.arg.requirements
[utility.requirements]: #utility.requirements
[utility.requirements.general]: #utility.requirements.general
[value.error.codes]: #value.error.codes
[zombie.names]: #zombie.names

[^1]: See also ISO/IEC 9899:2018 section 7.6.

[^2]: To save space, items that do not apply to a Clause are omitted.
    For example, if a Clause does not specify any requirements, there
    will be no “Requirements” subclause.

[^3]: Although in some cases the code given is unambiguously the optimum
    implementation.

[^4]: To save space, items that do not apply to a class are omitted. For
    example, if a class does not specify any comparison operator
    functions, there will be no “Comparison operator functions”
    subclause.

[^5]: To save space, elements that do not apply to a function are
    omitted. For example, if a function specifies no preconditions,
    there will be no *Preconditions:* element.

[^6]: This simplifies the presentation of complexity requirements in
    some cases.

[^7]: Examples from  [[utility.requirements]] include:
    *Cpp17EqualityComparable*, *Cpp17LessThanComparable*,
    *Cpp17CopyConstructible*. Examples from  [[iterator.requirements]]
    include: *Cpp17InputIterator*, *Cpp17ForwardIterator*.

[^8]: Such as an integer type, with constant integer values
    [[basic.fundamental]].

[^9]: Many of the objects manipulated by function signatures declared in
    `<cstring>` are character sequences or NTBSs. The size of some of
    these character sequences is limited by a length value, maintained
    separately from the character sequence.

[^10]: A *string-literal*, such as `"abc"`, is a static NTBS.

[^11]: An NTBS that contains characters only from the basic literal
    character set is also an NTMBS. Each multibyte character then
    consists of a single byte.

[^12]: The C standard library headers [[support.c.headers]] also define
    names within the global namespace, while the C++ headers for C
    library facilities [[headers]] can also define names within the
    global namespace.

[^13]: This gives implementers freedom to use inline namespaces to
    support multiple configurations of the library.

[^14]: A header is not necessarily a source file, nor are the sequences
    delimited by `<` and `>` in header names necessarily valid source
    file names [[cpp.include]].

[^15]: It is intentional that there is no C++ header for any of these C
    headers: , .

[^16]: This disallows the practice, allowed in C, of providing a masking
    macro in addition to the function prototype. The only way to achieve
    equivalent inline behavior in C++ is to provide a definition as an
    extern inline function.

[^17]: In particular, including the standard header `<iso646.h>` has no
    effect.

[^18]: The `".h"` headers dump all their names into the global
    namespace, whereas the newer forms keep their names in namespace
    `std`. Therefore, the newer forms are the preferred forms for all
    uses except for C++ programs which are intended to be strictly
    compatible with C.

[^19]: This is the same as the C standard library.

[^20]: The only reliable way to declare an object or function signature
    from the C standard library is by including the header that declares
    it, notwithstanding the latitude granted in 7.1.4 of the C Standard.

[^21]: Any library code that instantiates other library templates must
    be prepared to work adequately with any user-supplied specialization
    that meets the minimum requirements of this document.

[^22]: The list of such reserved names includes `errno`, declared or
    defined in `<cerrno>`.

[^23]: The list of such reserved function signatures with external
    linkage includes `setjmp(jmp_buf)`, declared or defined in
    `<csetjmp>`, and `va_end(va_list)`, declared or defined in
    `<cstdarg>`.

[^24]: The function signatures declared in `<cuchar>`, `<cwchar>`, and
    `<cwctype>` are always reserved, notwithstanding the restrictions
    imposed in subclause 4.5.1 of Amendment 1 to the C Standard for
    these headers.

[^25]: A valid C++ program always calls the expected library non-member
    function. An implementation can also define additional non-member
    functions that would otherwise not be called by a valid C++ program.

[^26]: That is, the C library functions can all be treated as if they
    are marked `noexcept`. This allows implementations to make
    performance optimizations based on the absence of exceptions at
    runtime.

[^27]: The functions `qsort()` and `bsearch()` [[alg.c.library]] meet
    this condition.

[^28]: In particular, they can report a failure to allocate storage by
    throwing an exception of type `bad_alloc`, or a class derived from
    `bad_alloc` [[bad.alloc]].
