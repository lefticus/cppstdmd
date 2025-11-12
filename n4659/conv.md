# Standard conversions <a id="conv">[[conv]]</a>

Standard conversions are implicit conversions with built-in meaning.
Clause  [[conv]] enumerates the full set of such conversions. A
*standard conversion sequence* is a sequence of standard conversions in
the following order:

- Zero or one conversion from the following set: lvalue-to-rvalue
  conversion, array-to-pointer conversion, and function-to-pointer
  conversion.
- Zero or one conversion from the following set: integral promotions,
  floating-point promotion, integral conversions, floating-point
  conversions, floating-integral conversions, pointer conversions,
  pointer to member conversions, and boolean conversions.
- Zero or one function pointer conversion.
- Zero or one qualification conversion.

[*Note 1*: A standard conversion sequence can be empty, i.e., it can
consist of no conversions. — *end note*\]

A standard conversion sequence will be applied to an expression if
necessary to convert it to a required destination type.

[*Note 2*:

Expressions with a given type will be implicitly converted to other
types in several contexts:

- When used as operands of operators. The operator’s requirements for
  its operands dictate the destination type (Clause  [[expr]]).
- When used in the condition of an `if` statement or iteration
  statement ( [[stmt.select]], [[stmt.iter]]). The destination type is
  `bool`.
- When used in the expression of a `switch` statement. The destination
  type is integral ( [[stmt.select]]).
- When used as the source expression for an initialization (which
  includes use as an argument in a function call and use as the
  expression in a `return` statement). The type of the entity being
  initialized is (generally) the destination type. See  [[dcl.init]], 
  [[dcl.init.ref]].

— *end note*\]

An expression `e` can be *implicitly converted* to a type `T` if and
only if the declaration `T t=e;` is well-formed, for some invented
temporary variable `t` ( [[dcl.init]]).

Certain language constructs require that an expression be converted to a
Boolean value. An expression `e` appearing in such a context is said to
be *contextually converted to `bool`* and is well-formed if and only if
the declaration `bool t(e);` is well-formed, for some invented temporary
variable `t` ( [[dcl.init]]).

Certain language constructs require conversion to a value having one of
a specified set of types appropriate to the construct. An expression `e`
of class type `E` appearing in such a context is said to be
*contextually implicitly converted* to a specified type `T` and is
well-formed if and only if `e` can be implicitly converted to a type `T`
that is determined as follows: `E` is searched for non-explicit
conversion functions whose return type is cv-qualifiercv `T` or
reference to cv-qualifiercv `T` such that `T` is allowed by the context.
There shall be exactly one such `T`.

The effect of any implicit conversion is the same as performing the
corresponding declaration and initialization and then using the
temporary variable as the result of the conversion. The result is an
lvalue if `T` is an lvalue reference type or an rvalue reference to
function type ( [[dcl.ref]]), an xvalue if `T` is an rvalue reference to
object type, and a prvalue otherwise. The expression `e` is used as a
glvalue if and only if the initialization uses it as a glvalue.

[*Note 3*: For class types, user-defined conversions are considered as
well; see  [[class.conv]]. In general, an implicit conversion sequence (
[[over.best.ics]]) consists of a standard conversion sequence followed
by a user-defined conversion followed by another standard conversion
sequence. — *end note*\]

[*Note 4*: There are some contexts where certain conversions are
suppressed. For example, the lvalue-to-rvalue conversion is not done on
the operand of the unary `&` operator. Specific exceptions are given in
the descriptions of those operators and contexts. — *end note*\]

## Lvalue-to-rvalue conversion <a id="conv.lval">[[conv.lval]]</a>

A glvalue ( [[basic.lval]]) of a non-function, non-array type `T` can be
converted to a prvalue.[^1] If `T` is an incomplete type, a program that
necessitates this conversion is ill-formed. If `T` is a non-class type,
the type of the prvalue is the cv-unqualified version of `T`. Otherwise,
the type of the prvalue is `T`. [^2]

When an lvalue-to-rvalue conversion is applied to an expression `e`, and
either

- `e` is not potentially evaluated, or
- the evaluation of `e` results in the evaluation of a member `ex` of
  the set of potential results of `e`, and `ex` names a variable `x`
  that is not odr-used by `ex` ( [[basic.def.odr]]),

the value contained in the referenced object is not accessed.

[*Example 1*:

``` cpp
struct S { int n; };
auto f() {
  S x { 1 };
  constexpr S y { 2 };
  return [&](bool b) { return (b ? y : x).n; };
}
auto g = f();
int m = g(false);   // undefined behavior due to access of x.n outside its lifetime
int n = g(true);    // OK, does not access y.n
```

— *end example*\]

The result of the conversion is determined according to the following
rules:

- If `T` is cv `std::nullptr_t`, the result is a null pointer constant (
  [[conv.ptr]]). \[*Note 1*: Since no value is fetched from memory,
  there is no side effect for a volatile access ( [[intro.execution]]),
  and an inactive member of a union ( [[class.union]]) may be
  accessed. — *end note*\]
- Otherwise, if `T` has a class type, the conversion copy-initializes
  the result object from the glvalue.
- Otherwise, if the object to which the glvalue refers contains an
  invalid pointer value ( [[basic.stc.dynamic.deallocation]],
  [[basic.stc.dynamic.safety]]), the behavior is
  *implementation-defined*.
- Otherwise, the value contained in the object indicated by the glvalue
  is the prvalue result.

[*Note 1*: See also  [[basic.lval]]. — *end note*\]

## Array-to-pointer conversion <a id="conv.array">[[conv.array]]</a>

An lvalue or rvalue of type “array of `N` `T`” or “array of unknown
bound of `T`” can be converted to a prvalue of type “pointer to `T`”.
The temporary materialization conversion ( [[conv.rval]]) is applied.
The result is a pointer to the first element of the array.

## Function-to-pointer conversion <a id="conv.func">[[conv.func]]</a>

An lvalue of function type `T` can be converted to a prvalue of type
“pointer to `T`”. The result is a pointer to the function.[^3]

[*Note 1*: See  [[over.over]] for additional rules for the case where
the function is overloaded. — *end note*\]

## Temporary materialization conversion <a id="conv.rval">[[conv.rval]]</a>

A prvalue of type `T` can be converted to an xvalue of type `T`. This
conversion initializes a temporary object ( [[class.temporary]]) of type
`T` from the prvalue by evaluating the prvalue with the temporary object
as its result object, and produces an xvalue denoting the temporary
object. `T` shall be a complete type.

[*Note 1*: If `T` is a class type (or array thereof), it must have an
accessible and non-deleted destructor; see 
[[class.dtor]]. — *end note*\]

[*Example 1*:

``` cpp
struct X { int n; };
int k = X().n;      // OK, X() prvalue is converted to xvalue
```

— *end example*\]

## Qualification conversions <a id="conv.qual">[[conv.qual]]</a>

A *cv-decomposition* of a type `T` is a sequence of cvᵢ and Pᵢ such that
`T` is

where each cvᵢ is a set of cv-qualifiers ( [[basic.type.qualifier]]),
and each Pᵢ is “pointer to” ( [[dcl.ptr]]), “pointer to member of class
Cᵢ of type” ( [[dcl.mptr]]), “array of Nᵢ”, or “array of unknown bound
of” ( [[dcl.array]]). If Pᵢ designates an array, the cv-qualifiers cvᵢ₊₁
on the element type are also taken as the cv-qualifiers cvᵢ of the
array.

[*Example 1*: The type denoted by the *type-id* `const int **` has two
cv-decompositions, taking `U` as “`int`” and as “pointer to
`const int`”. — *end example*\]

The n-tuple of cv-qualifiers after the first one in the longest
cv-decomposition of `T`, that is, cv₁, cv₂, …, cvₙ, is called the
*cv-qualification signature* of `T`.

Two types `T₁` and `T₂` are *similar* if they have cv-decompositions
with the same n such that corresponding Pᵢ components are the same and
the types denoted by `U` are the same.

A prvalue expression of type `T₁` can be converted to type `T₂` if the
following conditions are satisfied, where cvᵢʲ denotes the cv-qualifiers
in the cv-qualification signature of `Tⱼ`: [^4]

- `T₁` and `T₂` are similar.
- For every i > 0, if `const` is in cvᵢ¹ then `const` is in cvᵢ², and
  similarly for `volatile`.
- If the cvᵢ¹ and cvᵢ² are different, then `const` is in every cvₖ² for
  0 < k < i.

[*Note 1*:

If a program could assign a pointer of type `T**` to a pointer of type
`const` `T**` (that is, if line \#1 below were allowed), a program could
inadvertently modify a `const` object (as it is done on line \#2). For
example,

``` cpp
int main() {
  const char c = 'c';
  char* pc;
  const char** pcc = &pc;       // #1: not allowed
  *pcc = &c;
  *pc = 'C';                    // #2: modifies a const object
}
```

— *end note*\]

[*Note 2*: A prvalue of type “pointer to cv-qualifiercv1 `T`” can be
converted to a prvalue of type “pointer to cv-qualifiercv2 `T`” if
“cv-qualifiercv2 `T`” is more cv-qualified than “cv-qualifiercv1 `T`”. A
prvalue of type “pointer to member of `X` of type cv-qualifiercv1 `T`”
can be converted to a prvalue of type “pointer to member of `X` of type
cv-qualifiercv2 `T`” if “cv-qualifiercv2 `T`” is more cv-qualified than
“cv-qualifiercv1 `T`”. — *end note*\]

[*Note 3*: Function types (including those used in pointer to member
function types) are never cv-qualified ( [[dcl.fct]]). — *end note*\]

## Integral promotions <a id="conv.prom">[[conv.prom]]</a>

A prvalue of an integer type other than `bool`, `char16_t`, `char32_t`,
or `wchar_t` whose integer conversion rank ( [[conv.rank]]) is less than
the rank of `int` can be converted to a prvalue of type `int` if `int`
can represent all the values of the source type; otherwise, the source
prvalue can be converted to a prvalue of type `unsigned int`.

A prvalue of type `char16_t`, `char32_t`, or `wchar_t` (
[[basic.fundamental]]) can be converted to a prvalue of the first of the
following types that can represent all the values of its underlying
type: `int`, `unsigned int`, `long int`, `unsigned long int`,
`long long int`, or `unsigned long long int`. If none of the types in
that list can represent all the values of its underlying type, a prvalue
of type `char16_t`, `char32_t`, or `wchar_t` can be converted to a
prvalue of its underlying type.

A prvalue of an unscoped enumeration type whose underlying type is not
fixed ( [[dcl.enum]]) can be converted to a prvalue of the first of the
following types that can represent all the values of the enumeration
(i.e., the values in the range bₘin to bₘax as described in 
[[dcl.enum]]): `int`, `unsigned int`, `long int`, `unsigned long int`,
`long long int`, or `unsigned long long int`. If none of the types in
that list can represent all the values of the enumeration, a prvalue of
an unscoped enumeration type can be converted to a prvalue of the
extended integer type with lowest integer conversion rank (
[[conv.rank]]) greater than the rank of `long long` in which all the
values of the enumeration can be represented. If there are two such
extended types, the signed one is chosen.

A prvalue of an unscoped enumeration type whose underlying type is
fixed ( [[dcl.enum]]) can be converted to a prvalue of its underlying
type. Moreover, if integral promotion can be applied to its underlying
type, a prvalue of an unscoped enumeration type whose underlying type is
fixed can also be converted to a prvalue of the promoted underlying
type.

A prvalue for an integral bit-field ( [[class.bit]]) can be converted to
a prvalue of type `int` if `int` can represent all the values of the
bit-field; otherwise, it can be converted to `unsigned int` if
`unsigned int` can represent all the values of the bit-field. If the
bit-field is larger yet, no integral promotion applies to it. If the
bit-field has an enumerated type, it is treated as any other value of
that type for promotion purposes.

A prvalue of type `bool` can be converted to a prvalue of type `int`,
with `false` becoming zero and `true` becoming one.

These conversions are called *integral promotions*.

## Floating-point promotion <a id="conv.fpprom">[[conv.fpprom]]</a>

A prvalue of type `float` can be converted to a prvalue of type
`double`. The value is unchanged.

This conversion is called *floating-point promotion*.

## Integral conversions <a id="conv.integral">[[conv.integral]]</a>

A prvalue of an integer type can be converted to a prvalue of another
integer type. A prvalue of an unscoped enumeration type can be converted
to a prvalue of an integer type.

If the destination type is unsigned, the resulting value is the least
unsigned integer congruent to the source integer (modulo 2ⁿ where n is
the number of bits used to represent the unsigned type).

[*Note 1*: In a two’s complement representation, this conversion is
conceptual and there is no change in the bit pattern (if there is no
truncation). — *end note*\]

If the destination type is signed, the value is unchanged if it can be
represented in the destination type; otherwise, the value is
*implementation-defined*.

If the destination type is `bool`, see  [[conv.bool]]. If the source
type is `bool`, the value `false` is converted to zero and the value
`true` is converted to one.

The conversions allowed as integral promotions are excluded from the set
of integral conversions.

## Floating-point conversions <a id="conv.double">[[conv.double]]</a>

A prvalue of floating-point type can be converted to a prvalue of
another floating-point type. If the source value can be exactly
represented in the destination type, the result of the conversion is
that exact representation. If the source value is between two adjacent
destination values, the result of the conversion is an
*implementation-defined* choice of either of those values. Otherwise,
the behavior is undefined.

The conversions allowed as floating-point promotions are excluded from
the set of floating-point conversions.

## Floating-integral conversions <a id="conv.fpint">[[conv.fpint]]</a>

A prvalue of a floating-point type can be converted to a prvalue of an
integer type. The conversion truncates; that is, the fractional part is
discarded. The behavior is undefined if the truncated value cannot be
represented in the destination type.

[*Note 1*: If the destination type is `bool`, see 
[[conv.bool]]. — *end note*\]

A prvalue of an integer type or of an unscoped enumeration type can be
converted to a prvalue of a floating-point type. The result is exact if
possible. If the value being converted is in the range of values that
can be represented but the value cannot be represented exactly, it is an
*implementation-defined* choice of either the next lower or higher
representable value.

[*Note 2*: Loss of precision occurs if the integral value cannot be
represented exactly as a value of the floating type. — *end note*\]

If the value being converted is outside the range of values that can be
represented, the behavior is undefined. If the source type is `bool`,
the value `false` is converted to zero and the value `true` is converted
to one.

## Pointer conversions <a id="conv.ptr">[[conv.ptr]]</a>

A *null pointer constant* is an integer literal ( [[lex.icon]]) with
value zero or a prvalue of type `std::nullptr_t`. A null pointer
constant can be converted to a pointer type; the result is the *null
pointer value* of that type and is distinguishable from every other
value of object pointer or function pointer type. Such a conversion is
called a *null pointer conversion*. Two null pointer values of the same
type shall compare equal. The conversion of a null pointer constant to a
pointer to cv-qualified type is a single conversion, and not the
sequence of a pointer conversion followed by a qualification
conversion ( [[conv.qual]]). A null pointer constant of integral type
can be converted to a prvalue of type `std::nullptr_t`.

[*Note 1*: The resulting prvalue is not a null pointer
value. — *end note*\]

A prvalue of type “pointer to cv-qualifiercv `T`”, where `T` is an
object type, can be converted to a prvalue of type “pointer to
cv-qualifiercv `void`”. The pointer value ( [[basic.compound]]) is
unchanged by this conversion.

A prvalue of type “pointer to cv-qualifiercv `D`”, where `D` is a class
type, can be converted to a prvalue of type “pointer to cv-qualifiercv
`B`”, where `B` is a base class (Clause  [[class.derived]]) of `D`. If
`B` is an inaccessible (Clause  [[class.access]]) or ambiguous (
[[class.member.lookup]]) base class of `D`, a program that necessitates
this conversion is ill-formed. The result of the conversion is a pointer
to the base class subobject of the derived class object. The null
pointer value is converted to the null pointer value of the destination
type.

## Pointer to member conversions <a id="conv.mem">[[conv.mem]]</a>

A null pointer constant ( [[conv.ptr]]) can be converted to a pointer to
member type; the result is the *null member pointer value* of that type
and is distinguishable from any pointer to member not created from a
null pointer constant. Such a conversion is called a *null member
pointer conversion*. Two null member pointer values of the same type
shall compare equal. The conversion of a null pointer constant to a
pointer to member of cv-qualified type is a single conversion, and not
the sequence of a pointer to member conversion followed by a
qualification conversion ( [[conv.qual]]).

A prvalue of type “pointer to member of `B` of type cv-qualifiercv `T`”,
where `B` is a class type, can be converted to a prvalue of type
“pointer to member of `D` of type cv-qualifiercv `T`”, where `D` is a
derived class (Clause  [[class.derived]]) of `B`. If `B` is an
inaccessible (Clause  [[class.access]]), ambiguous (
[[class.member.lookup]]), or virtual ( [[class.mi]]) base class of `D`,
or a base class of a virtual base class of `D`, a program that
necessitates this conversion is ill-formed. The result of the conversion
refers to the same member as the pointer to member before the conversion
took place, but it refers to the base class member as if it were a
member of the derived class. The result refers to the member in `D`’s
instance of `B`. Since the result has type “pointer to member of `D` of
type cv-qualifiercv `T`”, indirection through it with a `D` object is
valid. The result is the same as if indirecting through the pointer to
member of `B` with the `B` subobject of `D`. The null member pointer
value is converted to the null member pointer value of the destination
type.[^5]

## Function pointer conversions <a id="conv.fctptr">[[conv.fctptr]]</a>

A prvalue of type “pointer to `noexcept` function” can be converted to a
prvalue of type “pointer to function”. The result is a pointer to the
function. A prvalue of type “pointer to member of type `noexcept`
function” can be converted to a prvalue of type “pointer to member of
type function”. The result points to the member function.

[*Example 1*:

``` cpp
  void (*p)();
  void (**pp)() noexcept = &p;  // error: cannot convert to pointer to noexcept function

  struct S { typedef void (*p)(); operator p(); };
  void (*q)() noexcept = S();   // error: cannot convert to pointer to noexcept function
```

— *end example*\]

## Boolean conversions <a id="conv.bool">[[conv.bool]]</a>

A prvalue of arithmetic, unscoped enumeration, pointer, or pointer to
member type can be converted to a prvalue of type `bool`. A zero value,
null pointer value, or null member pointer value is converted to
`false`; any other value is converted to `true`. For
direct-initialization ( [[dcl.init]]), a prvalue of type
`std::nullptr_t` can be converted to a prvalue of type `bool`; the
resulting value is `false`.

## Integer conversion rank <a id="conv.rank">[[conv.rank]]</a>

Every integer type has an *integer conversion rank* defined as follows:

- No two signed integer types other than `char` and `signed
  char` (if `char` is signed) shall have the same rank, even if they
  have the same representation.
- The rank of a signed integer type shall be greater than the rank of
  any signed integer type with a smaller size.
- The rank of `long long int` shall be greater than the rank of
  `long int`, which shall be greater than the rank of `int`, which shall
  be greater than the rank of `short int`, which shall be greater than
  the rank of `signed char`.
- The rank of any unsigned integer type shall equal the rank of the
  corresponding signed integer type.
- The rank of any standard integer type shall be greater than the rank
  of any extended integer type with the same size.
- The rank of `char` shall equal the rank of `signed char` and
  `unsigned char`.
- The rank of `bool` shall be less than the rank of all other standard
  integer types.
- The ranks of `char16_t`, `char32_t`, and `wchar_t` shall equal the
  ranks of their underlying types ( [[basic.fundamental]]).
- The rank of any extended signed integer type relative to another
  extended signed integer type with the same size is
  *implementation-defined*, but still subject to the other rules for
  determining the integer conversion rank.
- For all integer types `T1`, `T2`, and `T3`, if `T1` has greater rank
  than `T2` and `T2` has greater rank than `T3`, then `T1` shall have
  greater rank than `T3`.

[*Note 1*: The integer conversion rank is used in the definition of the
integral promotions ( [[conv.prom]]) and the usual arithmetic
conversions (Clause  [[expr]]). — *end note*\]

<!-- Section link definitions -->
[conv]: #conv
[conv.array]: #conv.array
[conv.bool]: #conv.bool
[conv.double]: #conv.double
[conv.fctptr]: #conv.fctptr
[conv.fpint]: #conv.fpint
[conv.fpprom]: #conv.fpprom
[conv.func]: #conv.func
[conv.integral]: #conv.integral
[conv.lval]: #conv.lval
[conv.mem]: #conv.mem
[conv.prom]: #conv.prom
[conv.ptr]: #conv.ptr
[conv.qual]: #conv.qual
[conv.rank]: #conv.rank
[conv.rval]: #conv.rval

<!-- Link reference definitions -->
[basic.compound]: basic.md#basic.compound
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.lval]: basic.md#basic.lval
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[basic.type.qualifier]: basic.md#basic.type.qualifier
[class.access]: class.md#class.access
[class.bit]: class.md#class.bit
[class.conv]: special.md#class.conv
[class.derived]: class.md#class.derived
[class.dtor]: special.md#class.dtor
[class.member.lookup]: class.md#class.member.lookup
[class.mi]: class.md#class.mi
[class.temporary]: special.md#class.temporary
[class.union]: class.md#class.union
[conv]: #conv
[conv.bool]: #conv.bool
[conv.prom]: #conv.prom
[conv.ptr]: #conv.ptr
[conv.qual]: #conv.qual
[conv.rank]: #conv.rank
[conv.rval]: #conv.rval
[dcl.array]: dcl.md#dcl.array
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.init]: dcl.md#dcl.init
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.mptr]: dcl.md#dcl.mptr
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[expr]: expr.md#expr
[intro.execution]: intro.md#intro.execution
[lex.icon]: lex.md#lex.icon
[over.best.ics]: over.md#over.best.ics
[over.over]: over.md#over.over
[stmt.iter]: stmt.md#stmt.iter
[stmt.select]: stmt.md#stmt.select

[^1]: For historical reasons, this conversion is called the
    “lvalue-to-rvalue” conversion, even though that name does not
    accurately reflect the taxonomy of expressions described in 
    [[basic.lval]].

[^2]: In C++class and array prvalues can have cv-qualified types. This
    differs from ISO C, in which non-lvalues never have cv-qualified
    types.

[^3]: This conversion never applies to non-static member functions
    because an lvalue that refers to a non-static member function cannot
    be obtained.

[^4]: These rules ensure that const-safety is preserved by the
    conversion.

[^5]: The rule for conversion of pointers to members (from pointer to
    member of base to pointer to member of derived) appears inverted
    compared to the rule for pointers to objects (from pointer to
    derived to pointer to base) ( [[conv.ptr]], Clause 
    [[class.derived]]). This inversion is necessary to ensure type
    safety. Note that a pointer to member is not an object pointer or a
    function pointer and the rules for conversions of such pointers do
    not apply to pointers to members. In particular, a pointer to member
    cannot be converted to a `void*`.
