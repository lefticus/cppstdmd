# Expressions <a id="expr">[expr]</a>

## Preamble <a id="expr.pre">[expr.pre]</a>

\[*Note 1*:

[expr] defines the syntax, order of evaluation, and meaning of
expressions.

An expression is a sequence of operators and operands that specifies a
computation. An expression can result in a value and can cause side
effects.

— *end note*\]

\[*Note 2*: Operators can be overloaded, that is, given meaning when
applied to expressions of class type [class] or enumeration type
[dcl.enum]. Uses of overloaded operators are transformed into function
calls as described in  [over.oper]. Overloaded operators obey the rules
for syntax and evaluation order specified in [expr.compound], but the
requirements of operand type and value category are replaced by the
rules for function call. Relations between operators, such as `++a`
meaning `a+=1`, are not guaranteed for overloaded operators
[over.oper]. — *end note*\]

Subclause [expr.compound] defines the effects of operators when applied
to types for which they have not been overloaded. Operator overloading
shall not modify the rules for the *built-in operators*, that is, for
operators applied to types for which they are defined by this Standard.
However, these built-in operators participate in overload resolution,
and as part of that process user-defined conversions will be considered
where necessary to convert the operands to types appropriate for the
built-in operator. If a built-in operator is selected, such conversions
will be applied to the operands before the operation is considered
further according to the rules in subclause [expr.compound]; see 
[over.match.oper], [over.built].

If during the evaluation of an expression, the result is not
mathematically defined or not in the range of representable values for
its type, the behavior is undefined.

\[*Note 3*:  Treatment of division by zero, forming a remainder using a
zero divisor, and all floating-point exceptions varies among machines,
and is sometimes adjustable by a library function. — *end note*\]

\[*Note 4*:

The implementation can regroup operators according to the usual
mathematical rules only where the operators really are associative or
commutative.

For example, in the following fragment

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
representable by an `int` is , the implementation cannot rewrite this
expression as

``` cpp
a = ((a + b) + 32765);
```

since if the values for `a` and `b` were, respectively, -32754 and -15,
the sum `a + b` would produce an exception while the original expression
would not; nor can the expression be rewritten as either

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

— *end note*\]

The values of the floating-point operands and the results of
floating-point expressions may be represented in greater precision and
range than that required by the type; the types are not changed thereby.

## Properties of expressions <a id="expr.prop">[expr.prop]</a>

### Value category <a id="basic.lval">[basic.lval]</a>

- A *glvalue* is an expression whose evaluation determines the identity
  of an object or function.

- A *prvalue* is an expression whose evaluation initializes an object or
  computes the value of an operand of an operator, as specified by the
  context in which it appears, or an expression that has type cv `void`.

- An *xvalue* is a glvalue that denotes an object whose resources can be
  reused (usually because it is near the end of its lifetime).

- An *lvalue* is a glvalue that is not an xvalue.

- An *rvalue* is a prvalue or an xvalue.

Every expression belongs to exactly one of the fundamental
classifications in this taxonomy: lvalue, xvalue, or prvalue. This
property of an expression is called its *value category*.

\[*Note 1*: The discussion of each built-in operator in [expr.compound]
indicates the category of the value it yields and the value categories
of the operands it expects. For example, the built-in assignment
operators expect that the left operand is an lvalue and that the right
operand is a prvalue and yield an lvalue as the result. User-defined
operators are functions, and the categories of values they expect and
yield are determined by their parameter and return types. — *end note*\]

\[*Note 2*: Historically, lvalues and rvalues were so-called because
they could appear on the left- and right-hand side of an assignment
(although this is no longer generally true); glvalues are “generalized”
lvalues, prvalues are “pure” rvalues, and xvalues are “eXpiring”
lvalues. Despite their names, these terms classify expressions, not
values. — *end note*\]

\[*Note 3*:

An expression is an xvalue if it is:

- a move-eligible *id-expression* [expr.prim.id.unqual],

- the result of calling a function, whether implicitly or explicitly,
  whose return type is an rvalue reference to object type [expr.call],

- a cast to an rvalue reference to object type
  [expr.type.conv,expr.dynamic.cast,expr.static.cast,
  expr.reinterpret.cast,expr.const.cast,expr.cast],

- a subscripting operation with an xvalue array operand [expr.sub],

- a class member access expression designating a non-static data member
  of non-reference type in which the object expression is an xvalue
  [expr.ref], or

- a `.*` pointer-to-member expression in which the first operand is an
  xvalue and the second operand is a pointer to data member
  [expr.mptr.oper].

In general, the effect of this rule is that named rvalue references are
treated as lvalues and unnamed rvalue references to objects are treated
as xvalues; rvalue references to functions are treated as lvalues
whether named or not.

— *end note*\]

\[*Example 1*:

``` cpp
struct A {
  int m;
};
A&& operator+(A, A);
A&& f();

A a;
A&& ar = static_cast<A&&>(a);
```

The expressions `f()`, `f().m`, `static_cast<A&&>(a)`, and `a + a` are
xvalues. The expression `ar` is an lvalue.

— *end example*\]

The *result* of a glvalue is the entity denoted by the expression. The
*result* of a prvalue is the value that the expression stores into its
context; a prvalue that has type cv `void` has no result. A prvalue
whose result is the value *V* is sometimes said to have or name the
value *V*. The *result object* of a prvalue is the object initialized by
the prvalue; a non-discarded prvalue that is used to compute the value
of an operand of a built-in operator or a prvalue that has type
cv `void` has no result object.

\[*Note 4*: Except when the prvalue is the operand of a
*decltype-specifier*, a prvalue of class or array type always has a
result object. For a discarded prvalue that has type other than
cv `void`, a temporary object is materialized; see
[expr.context]. — *end note*\]

Whenever a glvalue appears as an operand of an operator that expects a
prvalue for that operand, the lvalue-to-rvalue [conv.lval],
array-to-pointer [conv.array], or function-to-pointer [conv.func]
standard conversions are applied to convert the expression to a prvalue.

\[*Note 5*: An attempt to bind an rvalue reference to an lvalue is not
such a context; see  [dcl.init.ref]. — *end note*\]

\[*Note 6*: Because cv-qualifiers are removed from the type of an
expression of non-class type when the expression is converted to a
prvalue, an lvalue of type `const int` can, for example, be used where a
prvalue of type `int` is required. — *end note*\]

\[*Note 7*: There are no prvalue bit-fields; if a bit-field is converted
to a prvalue [conv.lval], a prvalue of the type of the bit-field is
created, which might then be promoted [conv.prom]. — *end note*\]

Whenever a prvalue appears as an operand of an operator that expects a
glvalue for that operand, the temporary materialization conversion
[conv.rval] is applied to convert the expression to an xvalue.

The discussion of reference initialization in  [dcl.init.ref] and of
temporaries in  [class.temporary] indicates the behavior of lvalues and
rvalues in other significant contexts.

Unless otherwise indicated [dcl.type.decltype], a prvalue shall always
have complete type or the `void` type; if it has a class type or
(possibly multidimensional) array of class type, that class shall not be
an abstract class [class.abstract]. A glvalue shall not have type
cv `void`.

\[*Note 8*: A glvalue can have complete or incomplete non-`void` type.
Class and array prvalues can have cv-qualified types; other prvalues
always have cv-unqualified types. See [expr.type]. — *end note*\]

An lvalue is *modifiable* unless its type is const-qualified or is a
function type.

\[*Note 9*: A program that attempts to modify an object through a
nonmodifiable lvalue or through an rvalue is ill-formed
[expr.ass,expr.post.incr,expr.pre.incr]. — *end note*\]

If a program attempts to access [defns.access] the stored value of an
object through a glvalue whose type is not similar [conv.qual] to one of
the following types the behavior is undefined:

- the dynamic type of the object,

- a type that is the signed or unsigned type corresponding to the
  dynamic type of the object, or

- a `char`, `unsigned char`, or `std::byte` type.

If a program invokes a defaulted copy/move constructor or copy/move
assignment operator for a union of type `U` with a glvalue argument that
does not denote an object of type cv `U` within its lifetime, the
behavior is undefined.

\[*Note 10*: In C, an entire object of structure type can be accessed,
e.g., using assignment. By contrast, C++ has no notion of accessing an
object of class type through an lvalue of class type. — *end note*\]

### Type <a id="expr.type">[expr.type]</a>

If an expression initially has the type “reference to `T`”
[dcl.ref,dcl.init.ref], the type is adjusted to `T` prior to any further
analysis. The expression designates the object or function denoted by
the reference, and the expression is an lvalue or an xvalue, depending
on the expression.

\[*Note 11*: Before the lifetime of the reference has started or after
it has ended, the behavior is undefined (see 
[basic.life]). — *end note*\]

If a prvalue initially has the type “cv `T`”, where `T` is a
cv-unqualified non-class, non-array type, the type of the expression is
adjusted to `T` prior to any further analysis.

The *composite pointer type* of two operands `p1` and `p2` having types
`T1` and `T2`, respectively, where at least one is a pointer or
pointer-to-member type or `std::nullptr_t`, is:

- if both `p1` and `p2` are null pointer constants, `std::nullptr_t`;

- if either `p1` or `p2` is a null pointer constant, `T2` or `T1`,
  respectively;

- if `T1` or `T2` is “pointer to `void`” and the other type is “pointer
  to `T`”, where `T` is an object type or `void`, “pointer to `void`”,
  where is the union of and ;

- if `T1` or `T2` is “pointer to `noexcept` function” and the other type
  is “pointer to function”, where the function types are otherwise the
  same, “pointer to function”;

- if `T1` is “pointer to `C1`” and `T2` is “pointer to `C2`”, where `C1`
  is reference-related to `C2` or `C2` is reference-related to `C1`
  [dcl.init.ref], the qualification-combined type [conv.qual] of `T1`
  and `T2` or the qualification-combined type of `T2` and `T1`,
  respectively;

- if `T1` or `T2` is “pointer to member of `C1` of type function”, the
  other type is “pointer to member of `C2` of type `noexcept` function”,
  and `C1` is reference-related to `C2` or `C2` is reference-related to
  `C1` [dcl.init.ref], where the function types are otherwise the same,
  “pointer to member of `C2` of type function” or “pointer to member of
  `C1` of type function”, respectively;

- if `T1` is “pointer to member of `C1` of type `U`” and `T2` is
  “pointer to member of `C2` of type `U`”, for some non-function type
  `U`, where `C1` is reference-related to `C2` or `C2` is
  reference-related to `C1` [dcl.init.ref], the qualification-combined
  type of `T2` and `T1` or the qualification-combined type of `T1` and
  `T2`, respectively;

- if `T1` and `T2` are similar types [conv.qual], the
  qualification-combined type of `T1` and `T2`;

- otherwise, a program that necessitates the determination of a
  composite pointer type is ill-formed.

\[*Example 2*:

``` cpp
typedef void *p;
typedef const int *q;
typedef int **pi;
typedef const int **pci;
```

The composite pointer type of `p` and `q` is “pointer to `const void`”;
the composite pointer type of `pi` and `pci` is “pointer to `const`
pointer to `const int`”.

— *end example*\]

### Context dependence <a id="expr.context">[expr.context]</a>

In some contexts, *unevaluated operands* appear [expr.prim.req,
expr.typeid,
expr.sizeof,
expr.unary.noexcept,
dcl.type.decltype,
temp.pre,
temp.concept]. An unevaluated operand is not evaluated.

\[*Note 12*: In an unevaluated operand, a non-static class member can be
named [expr.prim.id] and naming of objects or functions does not, by
itself, require that a definition be provided [basic.def.odr]. An
unevaluated operand is considered a full-expression
[intro.execution]. — *end note*\]

In some contexts, an expression only appears for its side effects. Such
an expression is called a *discarded-value expression*. The
array-to-pointer [conv.array] and function-to-pointer [conv.func]
standard conversions are not applied. The lvalue-to-rvalue conversion
[conv.lval] is applied if and only if the expression is a glvalue of
volatile-qualified type and it is one of the following:

- `(` *expression* `)`, where *expression* is one of these expressions,

- *id-expression* [expr.prim.id],

- subscripting [expr.sub],

- class member access [expr.ref],

- indirection [expr.unary.op],

- pointer-to-member operation [expr.mptr.oper],

- conditional expression [expr.cond] where both the second and the third
  operands are one of these expressions, or

- comma expression [expr.comma] where the right operand is one of these
  expressions.

\[*Note 13*: Using an overloaded operator causes a function call; the
above covers only operators with built-in meaning. — *end note*\]

The temporary materialization conversion [conv.rval] is applied if the
(possibly converted) expression is a prvalue of object type.

\[*Note 14*: If the original expression is an lvalue of class type, it
must have a volatile copy constructor to initialize the temporary object
that is the result object of the temporary materialization
conversion. — *end note*\]

The expression is evaluated and its result (if any) is discarded.

## Standard conversions <a id="conv">[conv]</a>

### General <a id="conv.general">[conv.general]</a>

Standard conversions are implicit conversions with built-in meaning.
[conv] enumerates the full set of such conversions. A
*standard conversion sequence* is a sequence of standard conversions in
the following order:

- Zero or one conversion from the following set: lvalue-to-rvalue
  conversion, array-to-pointer conversion, and function-to-pointer
  conversion.

- Zero or one conversion from the following set: integral promotions,
  floating-point promotion, integral conversions, floating-point
  conversions, floating-integral conversions, pointer conversions,
  pointer-to-member conversions, and boolean conversions.

- Zero or one function pointer conversion.

- Zero or one qualification conversion.

\[*Note 1*: A standard conversion sequence can be empty, i.e., it can
consist of no conversions. — *end note*\]

A standard conversion sequence will be applied to an expression if
necessary to convert it to a required destination type.

\[*Note 2*:

Expressions with a given type will be implicitly converted to other
types in several contexts:

- When used as operands of operators. The operator’s requirements for
  its operands dictate the destination type [expr.compound].

- When used in the condition of an `if` statement [stmt.if] or iteration
  statement [stmt.iter]. The destination type is `bool`.

- When used in the expression of a `switch` statement [stmt.switch]. The
  destination type is integral.

- When used as the source expression for an initialization (which
  includes use as an argument in a function call and use as the
  expression in a `return` statement). The type of the entity being
  initialized is (generally) the destination type. See  [dcl.init],
  [dcl.init.ref].

— *end note*\]

An expression E can be *implicitly converted* to a type `T` if and only
if the declaration `T t=$E$;` is well-formed, for some invented
temporary variable `t` [dcl.init].

Certain language constructs require that an expression be converted to a
Boolean value. An expression E appearing in such a context is said to be
`bool}}{conversion!contextual to \tcode{bool}` and is well-formed if and
only if the declaration `bool t($E$);` is well-formed, for some invented
temporary variable `t` [dcl.init].

Certain language constructs require conversion to a value having one of
a specified set of types appropriate to the construct. An expression E
of class type `C` appearing in such a context is said to be
*contextually implicitly converted* to a specified type `T` and is
well-formed if and only if E can be implicitly converted to a type `T`
that is determined as follows: `C` is searched for non-explicit
conversion functions whose return type is cv `T` or reference to cv `T`
such that `T` is allowed by the context. There shall be exactly one such
`T`.

The effect of any implicit conversion is the same as performing the
corresponding declaration and initialization and then using the
temporary variable as the result of the conversion. The result is an
lvalue if `T` is an lvalue reference type or an rvalue reference to
function type [dcl.ref], an xvalue if `T` is an rvalue reference to
object type, and a prvalue otherwise. The expression E is used as a
glvalue if and only if the initialization uses it as a glvalue.

\[*Note 3*: For class types, user-defined conversions are considered as
well; see  [class.conv]. In general, an implicit conversion sequence
[over.best.ics] consists of a standard conversion sequence followed by a
user-defined conversion followed by another standard conversion
sequence. — *end note*\]

\[*Note 4*: There are some contexts where certain conversions are
suppressed. For example, the lvalue-to-rvalue conversion is not done on
the operand of the unary `&` operator. Specific exceptions are given in
the descriptions of those operators and contexts. — *end note*\]

### Lvalue-to-rvalue conversion <a id="conv.lval">[conv.lval]</a>

A glvalue [basic.lval] of a non-function, non-array type `T` can be
converted to a prvalue.

If `T` is an incomplete type, a program that necessitates this
conversion is ill-formed. If `T` is a non-class type, the type of the
prvalue is the cv-unqualified version of `T`. Otherwise, the type of the
prvalue is `T`.

When an lvalue-to-rvalue conversion is applied to an expression E, and
either

- E is not potentially evaluated, or

- the evaluation of E results in the evaluation of a member
  $E_\tcode{x}$ of the set of potential results of E, and $E_\tcode{x}$
  names a variable `x` that is not odr-used by $E_\tcode{x}$
  [basic.def.odr],

the value contained in the referenced object is not accessed.

\[*Example 1*:

``` cpp
struct S { int n; };
auto f() {
  S x { 1 };
  constexpr S y { 2 };
  return [&](bool b) { return (b ? y : x).n; };
}
auto g = f();
int m = g(false);   // undefined behavior: access of x.n outside its lifetime
int n = g(true);    // OK, does not access y.n
```

— *end example*\]

The result of the conversion is determined according to the following
rules:

- If `T` is cv `std::nullptr_t`, the result is a null pointer constant
  [conv.ptr].

  \[*Note 1*: Since the conversion does not access the object to which
  the glvalue refers, there is no side effect even if `T` is
  volatile-qualified [intro.execution], and the glvalue can refer to an
  inactive member of a union [class.union]. — *end note*\]

- Otherwise, if `T` has a class type, the conversion copy-initializes
  the result object from the glvalue.

- Otherwise, if the object to which the glvalue refers contains an
  invalid pointer value [basic.stc.dynamic.deallocation], the behavior
  is *implementation-defined*.

- Otherwise, the object indicated by the glvalue is read [defns.access],
  and the value contained in the object is the prvalue result.

\[*Note 5*: See also  [basic.lval]. — *end note*\]

### Array-to-pointer conversion <a id="conv.array">[conv.array]</a>

An lvalue or rvalue of type “array of `N` `T`” or “array of unknown
bound of `T`” can be converted to a prvalue of type “pointer to `T`”.
The temporary materialization conversion [conv.rval] is applied. The
result is a pointer to the first element of the array.

### Function-to-pointer conversion <a id="conv.func">[conv.func]</a>

An lvalue of function type `T` can be converted to a prvalue of type
“pointer to `T`”. The result is a pointer to the function.

### Temporary materialization conversion <a id="conv.rval">[conv.rval]</a>

A prvalue of type `T` can be converted to an xvalue of type `T`. This
conversion initializes a temporary object [class.temporary] of type `T`
from the prvalue by evaluating the prvalue with the temporary object as
its result object, and produces an xvalue denoting the temporary object.
`T` shall be a complete type.

\[*Note 6*: If `T` is a class type (or array thereof), it must have an
accessible and non-deleted destructor; see  [class.dtor]. — *end note*\]

\[*Example 2*:

``` cpp
struct X { int n; };
int k = X().n;      // OK, X() prvalue is converted to xvalue
```

— *end example*\]

### Qualification conversions <a id="conv.qual">[conv.qual]</a>

A *qualification-decomposition* of a type `T` is a sequence of $\cv{}_i$
and Pᵢ such that `T` is

where each $\cv{}_i$ is a set of cv-qualifiers [basic.type.qualifier],
and each Pᵢ is “pointer to” [dcl.ptr], “pointer to member of class Cᵢ of
type” [dcl.mptr], “array of Nᵢ”, or “array of unknown bound of”
[dcl.array]. If Pᵢ designates an array, the cv-qualifiers $\cv{}_{i+1}$
on the element type are also taken as the cv-qualifiers $\cv{}_i$ of the
array.

\[*Example 3*: The type denoted by the *type-id* `const int **` has
three qualification-decompositions, taking `U` as “`int`”, as “pointer
to `const int`”, and as “pointer to pointer to
`const int`”. — *end example*\]

The n-tuple of cv-qualifiers after the first one in the longest
qualification-decomposition of `T`, that is,
$\cv{}_1, \cv{}_2, \dotsc, \cv{}_n$, is called the
*cv-qualification signature* of `T`.

Two types `T1` and `T2` are *similar* if they have
qualification-decompositions with the same n such that corresponding Pᵢ
components are either the same or one is “array of Nᵢ” and the other is
“array of unknown bound of”, and the types denoted by `U` are the same.

The *qualification-combined type* of two types `T1` and `T2` is the type
`T3` similar to `T1` whose qualification-decomposition is such that:

- for every i > 0, $\cv{}^3_i$ is the union of $\cv{}^1_i$ and
  $\cv{}^2_i$,

- if either P¹_i or P²_i is “array of unknown bound of”, P³_i is “array
  of unknown bound of”, otherwise it is P¹_i, and

- if the resulting $\cv{}^3_i$ is different from $\cv{}^1_i$ or
  $\cv{}^2_i$, or the resulting P³_i is different from P¹_i or P²_i,
  then `const` is added to every $\cv{}^3_k$ for 0 < k < i,

where $\cv{}^j_i$ and $P^j_i$ are the components of the
qualification-decomposition of $\tcode{T}j$. A prvalue of type `T1` can
be converted to type `T2` if the qualification-combined type of `T1` and
`T2` is `T2`.

\[*Note 7*:

If a program could assign a pointer of type `T**` to a pointer of type
`const` `T**` (that is, if line \#1 below were allowed), a program could
inadvertently modify a const object (as it is done on line \#2). For
example,

``` cpp
int main() {
  const char c = 'c';
  char* pc;
  const char** pcc = &pc;       // \#1: not allowed
  *pcc = &c;
  *pc = 'C';                    // \#2: modifies a const object
}
```

— *end note*\]

\[*Note 8*: Given similar types `T1` and `T2`, this construction ensures
that both can be converted to the qualification-combined type of `T1`
and `T2`. — *end note*\]

\[*Note 9*: A prvalue of type “pointer to `T`” can be converted to a
prvalue of type “pointer to `T`” if “ `T`” is more cv-qualified than “
`T`”. A prvalue of type “pointer to member of `X` of type `T`” can be
converted to a prvalue of type “pointer to member of `X` of type `T`” if
“ `T`” is more cv-qualified than “ `T`”. — *end note*\]

\[*Note 10*: Function types (including those used in
pointer-to-member-function types) are never cv-qualified
[dcl.fct]. — *end note*\]

### Integral promotions <a id="conv.prom">[conv.prom]</a>

A prvalue of an integer type other than `bool`, `char8_t`, `char16_t`,
`char32_t`, or `wchar_t` whose integer conversion rank [conv.rank] is
less than the rank of `int` can be converted to a prvalue of type `int`
if `int` can represent all the values of the source type; otherwise, the
source prvalue can be converted to a prvalue of type `unsigned int`.

A prvalue of type `char8_t`, `char16_t`, `char32_t`, or `wchar_t`
[basic.fundamental] can be converted to a prvalue of the first of the
following types that can represent all the values of its underlying
type: `int`, `unsigned int`, `long int`, `unsigned long int`,
`long long int`, or `unsigned long long int`. If none of the types in
that list can represent all the values of its underlying type, a prvalue
of type `char8_t`, `char16_t`, `char32_t`, or `wchar_t` can be converted
to a prvalue of its underlying type.

A prvalue of an unscoped enumeration type whose underlying type is not
fixed can be converted to a prvalue of the first of the following types
that can represent all the values of the enumeration [dcl.enum]: `int`,
`unsigned int`, `long int`, `unsigned long int`, `long long int`, or
`unsigned long long int`. If none of the types in that list can
represent all the values of the enumeration, a prvalue of an unscoped
enumeration type can be converted to a prvalue of the extended integer
type with lowest integer conversion rank [conv.rank] greater than the
rank of `long long` in which all the values of the enumeration can be
represented. If there are two such extended types, the signed one is
chosen.

A prvalue of an unscoped enumeration type whose underlying type is fixed
[dcl.enum] can be converted to a prvalue of its underlying type.
Moreover, if integral promotion can be applied to its underlying type, a
prvalue of an unscoped enumeration type whose underlying type is fixed
can also be converted to a prvalue of the promoted underlying type.

A prvalue for an integral bit-field [class.bit] can be converted to a
prvalue of type `int` if `int` can represent all the values of the
bit-field; otherwise, it can be converted to `unsigned int` if
`unsigned int` can represent all the values of the bit-field. If the
bit-field is larger yet, no integral promotion applies to it. If the
bit-field has enumeration type, it is treated as any other value of that
type for promotion purposes.

A prvalue of type `bool` can be converted to a prvalue of type `int`,
with `false` becoming zero and `true` becoming one.

These conversions are called *integral promotions*.

### Floating-point promotion <a id="conv.fpprom">[conv.fpprom]</a>

A prvalue of type `float` can be converted to a prvalue of type
`double`. The value is unchanged.

This conversion is called *floating-point promotion*.

### Integral conversions <a id="conv.integral">[conv.integral]</a>

A prvalue of an integer type can be converted to a prvalue of another
integer type. A prvalue of an unscoped enumeration type can be converted
to a prvalue of an integer type.

If the destination type is `bool`, see  [conv.bool]. If the source type
is `bool`, the value `false` is converted to zero and the value `true`
is converted to one.

Otherwise, the result is the unique value of the destination type that
is congruent to the source integer modulo $2^N$, where N is the width of
the destination type.

The conversions allowed as integral promotions are excluded from the set
of integral conversions.

### Floating-point conversions <a id="conv.double">[conv.double]</a>

A prvalue of floating-point type can be converted to a prvalue of
another floating-point type with a greater or equal conversion rank
[conv.rank]. A prvalue of standard floating-point type can be converted
to a prvalue of another standard floating-point type.

If the source value can be exactly represented in the destination type,
the result of the conversion is that exact representation. If the source
value is between two adjacent destination values, the result of the
conversion is an *implementation-defined* choice of either of those
values. Otherwise, the behavior is undefined.

The conversions allowed as floating-point promotions are excluded from
the set of floating-point conversions.

### Floating-integral conversions <a id="conv.fpint">[conv.fpint]</a>

A prvalue of a floating-point type can be converted to a prvalue of an
integer type. The conversion truncates; that is, the fractional part is
discarded. The behavior is undefined if the truncated value cannot be
represented in the destination type.

\[*Note 11*: If the destination type is `bool`, see 
[conv.bool]. — *end note*\]

A prvalue of an integer type or of an unscoped enumeration type can be
converted to a prvalue of a floating-point type. The result is exact if
possible. If the value being converted is in the range of values that
can be represented but the value cannot be represented exactly, it is an
*implementation-defined* choice of either the next lower or higher
representable value.

\[*Note 12*: Loss of precision occurs if the integral value cannot be
represented exactly as a value of the floating-point
type. — *end note*\]

If the value being converted is outside the range of values that can be
represented, the behavior is undefined. If the source type is `bool`,
the value `false` is converted to zero and the value `true` is converted
to one.

### Pointer conversions <a id="conv.ptr">[conv.ptr]</a>

A *null pointer constant* is an integer literal [lex.icon] with value
zero or a prvalue of type `std::nullptr_t`. A null pointer constant can
be converted to a pointer type; the result is the null pointer value of
that type [basic.compound] and is distinguishable from every other value
of object pointer or function pointer type. Such a conversion is called
a *null pointer conversion*. Two null pointer values of the same type
shall compare equal. The conversion of a null pointer constant to a
pointer to cv-qualified type is a single conversion, and not the
sequence of a pointer conversion followed by a qualification conversion
[conv.qual]. A null pointer constant of integral type can be converted
to a prvalue of type `std::nullptr_t`.

\[*Note 13*: The resulting prvalue is not a null pointer
value. — *end note*\]

A prvalue of type “pointer to cv `T`”, where `T` is an object type, can
be converted to a prvalue of type “pointer to cv `void`”. The pointer
value [basic.compound] is unchanged by this conversion.

A prvalue of type “pointer to cv `D`”, where `D` is a complete class
type, can be converted to a prvalue of type “pointer to cv `B`”, where
`B` is a base class [class.derived] of `D`. If `B` is an inaccessible
[class.access] or ambiguous [class.member.lookup] base class of `D`, a
program that necessitates this conversion is ill-formed. The result of
the conversion is a pointer to the base class subobject of the derived
class object. The null pointer value is converted to the null pointer
value of the destination type.

### Pointer-to-member conversions <a id="conv.mem">[conv.mem]</a>

A null pointer constant [conv.ptr] can be converted to a
pointer-to-member type; the result is the *null member pointer value* of
that type and is distinguishable from any pointer to member not created
from a null pointer constant. Such a conversion is called a
*null member pointer conversion*. Two null member pointer values of the
same type shall compare equal. The conversion of a null pointer constant
to a pointer to member of cv-qualified type is a single conversion, and
not the sequence of a pointer-to-member conversion followed by a
qualification conversion [conv.qual].

A prvalue of type “pointer to member of `B` of type cv `T`”, where `B`
is a class type, can be converted to a prvalue of type “pointer to
member of `D` of type cv `T`”, where `D` is a complete class derived
[class.derived] from `B`. If `B` is an inaccessible [class.access],
ambiguous [class.member.lookup], or virtual [class.mi] base class of
`D`, or a base class of a virtual base class of `D`, a program that
necessitates this conversion is ill-formed. The result of the conversion
refers to the same member as the pointer to member before the conversion
took place, but it refers to the base class member as if it were a
member of the derived class. The result refers to the member in `D`’s
instance of `B`. Since the result has type “pointer to member of `D` of
type cv `T`”, indirection through it with a `D` object is valid. The
result is the same as if indirecting through the pointer to member of
`B` with the `B` subobject of `D`. The null member pointer value is
converted to the null member pointer value of the destination type.

### Function pointer conversions <a id="conv.fctptr">[conv.fctptr]</a>

A prvalue of type “pointer to `noexcept` function” can be converted to a
prvalue of type “pointer to function”. The result is a pointer to the
function. A prvalue of type “pointer to member of type `noexcept`
function” can be converted to a prvalue of type “pointer to member of
type function”. The result designates the member function.

\[*Example 4*:

``` cpp
void (*p)();
void (**pp)() noexcept = &p;    // error: cannot convert to pointer to noexcept function

struct S { typedef void (*p)(); operator p(); };
void (*q)() noexcept = S();     // error: cannot convert to pointer to noexcept function
```

— *end example*\]

### Boolean conversions <a id="conv.bool">[conv.bool]</a>

A prvalue of arithmetic, unscoped enumeration, pointer, or
pointer-to-member type can be converted to a prvalue of type `bool`. A
zero value, null pointer value, or null member pointer value is
converted to `false`; any other value is converted to `true`.

## Usual arithmetic conversions <a id="expr.arith.conv">[expr.arith.conv]</a>

Many binary operators that expect operands of arithmetic or enumeration
type cause conversions and yield result types in a similar way. The
purpose is to yield a common type, which is also the type of the result.
This pattern is called the *usual arithmetic conversions*, which are
defined as follows:

- If either operand is of scoped enumeration type [dcl.enum], no
  conversions are performed; if the other operand does not have the same
  type, the expression is ill-formed.

- Otherwise, if either operand is of floating-point type, the following
  rules are applied:

  - If both operands have the same type, no further conversion is
    needed.

  - Otherwise, if one of the operands is of a non-floating-point type,
    that operand is converted to the type of the operand with the
    floating-point type.

  - Otherwise, if the floating-point conversion ranks [conv.rank] of the
    types of the operands are ordered but not equal, then the operand of
    the type with the lesser floating-point conversion rank is converted
    to the type of the other operand.

  - Otherwise, if the floating-point conversion ranks of the types of
    the operands are equal, then the operand with the lesser
    floating-point conversion subrank [conv.rank] is converted to the
    type of the other operand.

  - Otherwise, the expression is ill-formed.

- Otherwise, each operand is converted to a common type `C`. The
  integral promotion rules [conv.prom] are used to determine a type `T1`
  and type `T2` for each operand.

  Then the following rules are applied to determine `C`:

  - If `T1` and `T2` are the same type, `C` is that type.

  - Otherwise, if `T1` and `T2` are both signed integer types or are
    both unsigned integer types, `C` is the type with greater rank.

  - Otherwise, let `U` be the unsigned integer type and `S` be the
    signed integer type.

    - If `U` has rank greater than or equal to the rank of `S`, `C` is
      `U`.

    - Otherwise, if `S` can represent all of the values of `U`, `C` is
      `S`.

    - Otherwise, `C` is the unsigned integer type corresponding to `S`.

If one operand is of enumeration type and the other operand is of a
different enumeration type or a floating-point type, this behavior is
deprecated [depr.arith.conv.enum].

## Primary expressions <a id="expr.prim">[expr.prim]</a>

``` bnf
primary-expression:
    literal
    \texttt{this}
    '(' expression ')'
    id-expression
    lambda-expression
    fold-expression
    requires-expression
```

### Literals <a id="expr.prim.literal">[expr.prim.literal]</a>

The type of a *literal* is determined based on its form as specified in
[lex.literal]. A *string-literal* is an lvalue designating a
corresponding string literal object [lex.string], a
*user-defined-literal* has the same value category as the corresponding
operator call expression described in [lex.ext], and any other *literal*
is a prvalue.

### This <a id="expr.prim.this">[expr.prim.this]</a>

The keyword `this` names a pointer to the object for which an implicit
object member function [class.mfct.non.static] is invoked or a
non-static data member’s initializer [class.mem] is evaluated.

The *current class* at a program point is the class associated with the
innermost class scope containing that point.

\[*Note 1*: A *lambda-expression* does not introduce a class
scope. — *end note*\]

If a declaration declares a member function or member function template
of a class `X`, the expression `this` is a prvalue of type “pointer to
*cv-qualifier-seq* `X`” wherever `X` is the current class between the
optional *cv-qualifier-seq* and the end of the *function-definition*,
*member-declarator*, or *declarator*. It shall not appear within the
declaration of either a static member function or an explicit object
member function of the current class (although its type and value
category are defined within such member functions as they are within an
implicit object member function).

\[*Note 2*: This is because declaration matching does not occur until
the complete declarator is known. — *end note*\]

\[*Note 3*:

In a *trailing-return-type*, the class being defined is not required to
be complete for purposes of class member access [expr.ref]. Class
members declared later are not visible.

— *end note*\]

Otherwise, if a *member-declarator* declares a non-static data member
[class.mem] of a class `X`, the expression `this` is a prvalue of type
“pointer to `X`” wherever `X` is the current class within the optional
default member initializer [class.mem].

The expression `this` shall not appear in any other context.

\[*Example 1*:

``` cpp
class Outer {
  int a[sizeof(*this)];                 // error: not inside a member function
  unsigned int sz = sizeof(*this);      // OK, in default member initializer

  void f() {
    int b[sizeof(*this)];               // OK

    struct Inner {
      int c[sizeof(*this)];             // error: not inside a member function of Inner
    };
  }
};
```

— *end example*\]

### Parentheses <a id="expr.prim.paren">[expr.prim.paren]</a>

A parenthesized expression `($E$)` is a primary expression whose type,
result, and value category are identical to those of E. The
parenthesized expression can be used in exactly the same contexts as
those where E can be used, and with the same meaning, except as
otherwise indicated.

### Names <a id="expr.prim.id">[expr.prim.id]</a>

#### General <a id="expr.prim.id.general">[expr.prim.id.general]</a>

``` bnf
id-expression:
    unqualified-id
    qualified-id
```

An *id-expression* is a restricted form of a *primary-expression*.

\[*Note 4*: An *id-expression* can appear after `.` and `->` operators
[expr.ref]. — *end note*\]

If an *id-expression* E denotes a member M of an anonymous union
[class.union.anon] U:

- If U is a non-static data member, E refers to M as a member of the
  lookup context of the terminal name of E (after any transformation to
  a class member access expression [class.mfct.non.static]).

  \[*Example 1*: `o.x` is interpreted as `o.$u$.x`, where u names the
  anonymous union member. — *end example*\]

- Otherwise, E is interpreted as a class member access [expr.ref] that
  designates the member subobject M of the anonymous union variable for
  U.

  \[*Note 2*: Under this interpretation, E no longer denotes a
  non-static data member. — *end note*\]

  \[*Example 2*: `N::x` is interpreted as `N::$u$.x`, where u names the
  anonymous union variable. — *end example*\]

An *id-expression* that denotes a non-static data member or implicit
object member function of a class can only be used:

- as part of a class member access [expr.ref] in which the object
  expression refers to the member’s class

  or a class derived from that class, or

- to form a pointer to member [expr.unary.op], or

- if that *id-expression* denotes a non-static data member and it
  appears in an unevaluated operand.

  \[*Example 3*:

  ``` cpp
  struct S {
    int m;
  };
  int i = sizeof(S::m);           // OK
  int j = sizeof(S::m + 42);      // OK
  ```

  — *end example*\]

For an *id-expression* that denotes an overload set, overload resolution
is performed to select a unique function [over.match,over.over].

\[*Note 5*:

A program cannot refer to a function with a trailing *requires-clause*
whose *constraint-expression* is not satisfied, because such functions
are never selected by overload resolution.

— *end note*\]

#### Unqualified names <a id="expr.prim.id.unqual">[expr.prim.id.unqual]</a>

``` bnf
unqualified-id:
    identifier
    operator-function-id
    conversion-function-id
    literal-operator-id
    '\~' type-name
    '\~' decltype-specifier
    template-id
```

An *identifier* is only an *id-expression* if it has been suitably
declared [dcl.dcl] or if it appears as part of a *declarator-id*
[dcl.decl]. An *identifier* that names a coroutine parameter refers to
the copy of the parameter [dcl.fct.def.coroutine].

\[*Note 6*: For *operator-function-id*, see  [over.oper]; for
*conversion-function-id*, see  [class.conv.fct]; for
*literal-operator-id*, see  [over.literal]; for *template-id*, see 
[temp.names]. A *type-name* or *decltype-specifier* prefixed by `~`
denotes the destructor of the type so named; see  [expr.prim.id.dtor].
Within the definition of a non-static member function, an *identifier*
that names a non-static member is transformed to a class member access
expression [class.mfct.non.static]. — *end note*\]

A *component name* of an *unqualified-id* U is

- U if it is a name or

- the component name of the *template-id* or *type-name* of U, if any.

\[*Note 7*: Other constructs that contain names to look up can have
several component names
[expr.prim.id.qual,dcl.type.simple,dcl.type.elab,
dcl.mptr,namespace.udecl,temp.param,temp.names,temp.res]. — *end note*\]

The *terminal name* of a construct is the component name of that
construct that appears lexically last.

The result is the entity denoted by the *unqualified-id*
[basic.lookup.unqual]. If the *unqualified-id* appears in a
*lambda-expression* at program point P and the entity is a local entity
[basic.pre] or a variable declared by an *init-capture*
[expr.prim.lambda.capture], then let S be the *compound-statement* of
the innermost enclosing *lambda-expression* of P. If naming the entity
from outside of an unevaluated operand within S would refer to an entity
captured by copy in some intervening *lambda-expression*, then let E be
the innermost such *lambda-expression*.

- If there is such a *lambda-expression* and if P is in E’s function
  parameter scope but not its *parameter-declaration-clause*, then the
  type of the expression is the type of a class member access expression
  [expr.ref] naming the non-static data member that would be declared
  for such a capture in the object parameter [dcl.fct] of the function
  call operator of E.

  \[*Note 3*: If E is not declared `mutable`, the type of such an
  identifier will typically be `const` qualified. — *end note*\]

- Otherwise (if there is no such *lambda-expression* or if P either
  precedes E’s function parameter scope or is in E’s
  *parameter-declaration-clause*), the type of the expression is the
  type of the result.

\[*Note 8*: If the entity is a template parameter object for a template
parameter of type `T` [temp.param], the type of the expression is
`const T`. — *end note*\]

\[*Note 9*: The type will be adjusted as described in [expr.type] if it
is cv-qualified or is a reference type. — *end note*\]

The expression is an xvalue if it is move-eligible (see below); an
lvalue if the entity is a function, variable, structured binding
[dcl.struct.bind], data member, or template parameter object; and a
prvalue otherwise [basic.lval]; it is a bit-field if the identifier
designates a bit-field.

\[*Example 2*:

``` cpp
void f() {
  float x, &r = x;

  [=]() -> decltype((x)) {      // lambda returns float const\& because this lambda is not mutable and
                                // x is an lvalue
    decltype(x) y1;             // y1 has type float
    decltype((x)) y2 = y1;      // y2 has type float const\&
    decltype(r) r1 = y1;        // r1 has type float\&
    decltype((r)) r2 = y2;      // r2 has type float const\&
    return y2;
  };

  [=](decltype((x)) y) {
    decltype((x)) z = x;        // OK, y has type float\&, z has type float const\&
  };

  [=] {
    [](decltype((x)) y) {};     // OK, lambda takes a parameter of type float const\&

    [x=1](decltype((x)) y) {
      decltype((x)) z = x;      // OK, y has type int\&, z has type int const\&
    };
  };
}
```

— *end example*\]

An *implicitly movable entity* is a variable of automatic storage
duration that is either a non-volatile object or an rvalue reference to
a non-volatile object type. In the following contexts, an
*id-expression* is *move-eligible*:

- If the *id-expression* (possibly parenthesized) is the operand of a
  `return` [stmt.return] or `co_return` [stmt.return.coroutine]
  statement, and names an implicitly movable entity declared in the body
  or *parameter-declaration-clause* of the innermost enclosing function
  or *lambda-expression*, or

- if the *id-expression* (possibly parenthesized) is the operand of a
  *throw-expression* [expr.throw], and names an implicitly movable
  entity that belongs to a scope that does not contain the
  *compound-statement* of the innermost *lambda-expression*,
  *try-block*, or *function-try-block* (if any) whose
  *compound-statement* or *ctor-initializer* contains the
  *throw-expression*.

#### Qualified names <a id="expr.prim.id.qual">[expr.prim.id.qual]</a>

``` bnf
qualified-id:
    nested-name-specifier [\texttt{template]} unqualified-id
```

``` bnf
nested-name-specifier:
    '::'
    type-name '::'
    namespace-name '::'
    decltype-specifier '::'
    nested-name-specifier identifier '::'
    nested-name-specifier [\texttt{template]} simple-template-id '::'
```

The component names of a *qualified-id* are those of its
*nested-name-specifier* and *unqualified-id*. The component names of a
*nested-name-specifier* are its *identifier* (if any) and those of its
*type-name*, *namespace-name*, *simple-template-id*, and/or
*nested-name-specifier*.

A *nested-name-specifier* is *declarative* if it is part of

- a *class-head-name*,

- an *enum-head-name*,

- a *qualified-id* that is the *id-expression* of a *declarator-id*, or

- a declarative *nested-name-specifier*.

A declarative *nested-name-specifier* shall not have a
*decltype-specifier*. A declaration that uses a declarative
*nested-name-specifier* shall be a friend declaration or inhabit a scope
that contains the entity being redeclared or specialized.

The *nested-name-specifier* `::` nominates the global namespace. A
*nested-name-specifier* with a *decltype-specifier* nominates the type
denoted by the *decltype-specifier*, which shall be a class or
enumeration type. If a *nested-name-specifier* N is declarative and has
a *simple-template-id* with a template argument list A that involves a
template parameter, let T be the template nominated by N without A. T
shall be a class template.

- If A is the template argument list [temp.arg] of the corresponding
  *template-head* H [temp.mem], N nominates the primary template of T; H
  shall be equivalent to the *template-head* of T [temp.over.link].

- Otherwise, N nominates the partial specialization [temp.spec.partial]
  of T whose template argument list is equivalent to A [temp.over.link];
  the program is ill-formed if no such partial specialization exists.

Any other *nested-name-specifier* nominates the entity denoted by its
*type-name*, *namespace-name*, *identifier*, or *simple-template-id*. If
the *nested-name-specifier* is not declarative, the entity shall not be
a template.

A *qualified-id* shall not be of the form *nested-name-specifier*
`template` `~` *decltype-specifier* nor of the form *decltype-specifier*
`::` `~` *type-name*.

The result of a *qualified-id* Q is the entity it denotes
[basic.lookup.qual]. The type of the expression is the type of the
result. The result is an lvalue if the member is

- a function other than a non-static member function,

- a non-static member function if Q is the operand of a unary `&`
  operator,

- a variable,

- a structured binding [dcl.struct.bind], or

- a data member,

and a prvalue otherwise.

#### Destruction <a id="expr.prim.id.dtor">[expr.prim.id.dtor]</a>

An *id-expression* that denotes the destructor of a type `T` names the
destructor of `T` if `T` is a class type [class.dtor], otherwise the
*id-expression* is said to name a *pseudo-destructor*.

If the *id-expression* names a pseudo-destructor, `T` shall be a scalar
type and the *id-expression* shall appear as the right operand of a
class member access [expr.ref] that forms the *postfix-expression* of a
function call [expr.call].

\[*Note 10*: Such a call ends the lifetime of the object
[expr.call,basic.life]. — *end note*\]

\[*Example 3*:

``` cpp
struct C { };
void f() {
  C * pc = new C;
  using C2 = C;
  pc->C::~C2();     // OK, destroys *pc
  C().C::~C();      // undefined behavior: temporary of type C destroyed twice
  using T = int;
  0 .T::~T();       // OK, no effect
  0.T::~T();        // error: 0.T is a user-defined-floating-point-literal[lex.ext]
}
```

— *end example*\]

### Lambda expressions <a id="expr.prim.lambda">[expr.prim.lambda]</a>

#### General <a id="expr.prim.lambda.general">[expr.prim.lambda.general]</a>

``` bnf
lambda-expression:
    lambda-introducer [attribute-specifier-seq] lambda-declarator compound-statement
    lambda-introducer '<' template-parameter-list '>' [requires-clause] [attribute-specifier-seq]
       lambda-declarator compound-statement
```

``` bnf
lambda-introducer:
    '[' [lambda-capture] ']'
```

``` bnf
lambda-declarator:
    lambda-specifier-seq [noexcept-specifier] [attribute-specifier-seq] [trailing-return-type]
    noexcept-specifier [attribute-specifier-seq] [trailing-return-type]
    [trailing-return-type]
    '(' parameter-declaration-clause ')' [lambda-specifier-seq] [noexcept-specifier] [attribute-specifier-seq]
       [trailing-return-type] [requires-clause]
```

``` bnf
lambda-specifier:
    \texttt{consteval}
    \texttt{constexpr}
    \texttt{mutable}
    \texttt{static}
```

``` bnf
lambda-specifier-seq:
    lambda-specifier
    lambda-specifier lambda-specifier-seq
```

A *lambda-expression* provides a concise way to create a simple function
object.

\[*Example 4*:

``` cpp
#include <algorithm>
#include <cmath>
void abssort(float* x, unsigned N) {
  std::sort(x, x + N, [](float a, float b) { return std::abs(a) < std::abs(b); });
}
```

— *end example*\]

A *lambda-expression* is a prvalue whose result object is called the
*closure object*.

\[*Note 11*: A closure object behaves like a function object
[function.objects]. — *end note*\]

An ambiguity can arise because a *requires-clause* can end in an
*attribute-specifier-seq*, which collides with the
*attribute-specifier-seq* in *lambda-expression*. In such cases, any
attributes are treated as *attribute-specifier-seq* in
*lambda-expression*.

\[*Note 12*: Such ambiguous cases cannot have valid semantics because
the constraint expression would not have type `bool`. — *end note*\]

A *lambda-specifier-seq* shall contain at most one of each
*lambda-specifier* and shall not contain both `constexpr` and
`consteval`. If the *lambda-declarator* contains an explicit object
parameter [dcl.fct], then no *lambda-specifier* in the
*lambda-specifier-seq* shall be `mutable` or `static`. The
*lambda-specifier-seq* shall not contain both `mutable` and `static`. If
the *lambda-specifier-seq* contains `static`, there shall be no
*lambda-capture*.

\[*Note 13*: The trailing *requires-clause* is described in
[dcl.decl]. — *end note*\]

If a *lambda-declarator* does not include a
*parameter-declaration-clause*, it is as if `()` were inserted at the
start of the *lambda-declarator*. If the *lambda-declarator* does not
include a *trailing-return-type*, it is considered to be `-> auto`.

\[*Note 14*: In that case, the return type is deduced from `return`
statements as described in [dcl.spec.auto]. — *end note*\]

\[*Example 5*:

``` cpp
auto x1 = [](int i) { return i; };      // OK, return type is int
auto x2 = []{ return { 1, 2 }; };       // error: deducing return type from braced-init-list
int j;
auto x3 = [&]()->auto&& { return j; };  // OK, return type is int\&
```

— *end example*\]

A lambda is a *generic lambda* if the *lambda-expression* has any
generic parameter type placeholders [dcl.spec.auto], or if the lambda
has a *template-parameter-list*.

\[*Example 6*:

``` cpp
int i = [](int i, auto a) { return i; }(3, 4);                  // OK, a generic lambda
int j = []<class T>(T t, int i) { return i; }(3, 4);            // OK, a generic lambda
```

— *end example*\]

#### Closure types <a id="expr.prim.lambda.closure">[expr.prim.lambda.closure]</a>

The type of a *lambda-expression* (which is also the type of the closure
object) is a unique, unnamed non-union class type, called the
*closure type*, whose properties are described below.

The closure type is declared in the smallest block scope, class scope,
or namespace scope that contains the corresponding *lambda-expression*.

\[*Note 15*: This determines the set of namespaces and classes
associated with the closure type [basic.lookup.argdep]. The parameter
types of a *lambda-declarator* do not affect these associated namespaces
and classes. — *end note*\]

The closure type is not an aggregate type [dcl.init.aggr]. An
implementation may define the closure type differently from what is
described below provided this does not alter the observable behavior of
the program other than by changing:

- the size and/or alignment of the closure type,

- whether the closure type is trivially copyable [class.prop], or

- whether the closure type is a standard-layout class [class.prop].

An implementation shall not add members of rvalue reference type to the
closure type.

The closure type for a *lambda-expression* has a public inline function
call operator (for a non-generic lambda) or function call operator
template (for a generic lambda) [over.call] whose parameters and return
type are described by the *lambda-expression*’s
*parameter-declaration-clause* and *trailing-return-type* respectively,
and whose *template-parameter-list* consists of the specified
*template-parameter-list*, if any. The *requires-clause* of the function
call operator template is the *requires-clause* immediately following
`<` *template-parameter-list* `>`, if any. The trailing
*requires-clause* of the function call operator or operator template is
the *requires-clause* of the *lambda-declarator*, if any.

\[*Note 16*: The function call operator template for a generic lambda
can be an abbreviated function template [dcl.fct]. — *end note*\]

\[*Example 7*:

``` cpp
auto glambda = [](auto a, auto&& b) { return a < b; };
bool b = glambda(3, 3.14);                                      // OK

auto vglambda = [](auto printer) {
  return [=](auto&& ... ts) {                                   // OK, ts is a function parameter pack
    printer(std::forward<decltype(ts)>(ts)...);

    return [=]() {
      printer(ts ...);
    };
  };
};
auto p = vglambda( [](auto v1, auto v2, auto v3)
                   { std::cout << v1 << v2 << v3; } );
auto q = p(1, 'a', 3.14);                                       // OK, outputs 1a3.14
q();                                                            // OK, outputs 1a3.14

auto fact = [](this auto self, int n) -> int {                  // OK, explicit object parameter
  return (n <= 1) ? 1 : n * self(n-1);
};
std::cout << fact(5);                                           // OK, outputs 120
```

— *end example*\]

Given a lambda with a *lambda-capture*, the type of the explicit object
parameter, if any, of the lambda’s function call operator (possibly
instantiated from a function call operator template) shall be either:

- the closure type,

- a class type derived from the closure type, or

- a reference to a possibly cv-qualified such type.

\[*Example 8*:

``` cpp
struct C {
  template <typename T>
  C(T);
};

void func(int i) {
  int x = [=](this auto&&) { return i; }();     // OK
  int y = [=](this C) { return i; }();          // error
  int z = [](this C) { return 42; }();          // OK
}
```

— *end example*\]

The function call operator or operator template is a static member
function or static member function template [class.static.mfct] if the
*lambda-expression*’s *parameter-declaration-clause* is followed by
`static`. Otherwise, it is a non-static member function or member
function template [class.mfct.non.static] that is declared `const`
[class.mfct.non.static] if and only if the *lambda-expression*’s
*parameter-declaration-clause* is not followed by `mutable` and the
*lambda-declarator* does not contain an explicit object parameter. It is
neither virtual nor declared `volatile`. Any *noexcept-specifier*
specified on a *lambda-expression* applies to the corresponding function
call operator or operator template. An *attribute-specifier-seq* in a
*lambda-declarator* appertains to the type of the corresponding function
call operator or operator template. An *attribute-specifier-seq* in a
*lambda-expression* preceding a *lambda-declarator* appertains to the
corresponding function call operator or operator template. The function
call operator or any given operator template specialization is a
constexpr function if either the corresponding *lambda-expression*
*parameter-declaration-clause* is followed by `constexpr` or
`consteval`, or it is constexpr-suitable [dcl.constexpr]. It is an
immediate function [dcl.constexpr] if the corresponding
*lambda-expression* *parameter-declaration-clause* is followed by
`consteval`.

\[*Example 9*:

``` cpp
auto ID = [](auto a) { return a; };
static_assert(ID(3) == 3);                      // OK

struct NonLiteral {
  NonLiteral(int n) : n(n) { }
  int n;
};
static_assert(ID(NonLiteral{3}).n == 3);        // error
```

— *end example*\]

\[*Example 10*:

``` cpp
auto monoid = [](auto v) { return [=] { return v; }; };
auto add = [](auto m1) constexpr {
  auto ret = m1();
  return [=](auto m2) mutable {
    auto m1val = m1();
    auto plus = [=](auto m2val) mutable constexpr
                   { return m1val += m2val; };
    ret = plus(m2());
    return monoid(ret);
  };
};
constexpr auto zero = monoid(0);
constexpr auto one = monoid(1);
static_assert(add(one)(zero)() == one());       // OK

// Since two below is not declared constexpr, an evaluation of its constexpr member function call operator
// cannot perform an lvalue-to-rvalue conversion on one of its subobjects (that represents its capture)
// in a constant expression.
auto two = monoid(2);
assert(two() == 2); // OK, not a constant expression.
static_assert(add(one)(one)() == two());        // error: two() is not a constant expression
static_assert(add(one)(one)() == monoid(2)());  // OK
```

— *end example*\]

\[*Note 17*:

The function call operator or operator template can be constrained
[temp.constr.decl] by a *type-constraint* [temp.param], a
*requires-clause* [temp.pre], or a trailing *requires-clause*
[dcl.decl].

— *end note*\]

The closure type for a non-generic *lambda-expression* with no
*lambda-capture* whose constraints (if any) are satisfied has a
conversion function to pointer to function with C++ language linkage
[dcl.link] having the same parameter and return types as the closure
type’s function call operator. The conversion is to “pointer to
`noexcept` function” if the function call operator has a non-throwing
exception specification. If the function call operator is a static
member function, then the value returned by this conversion function is
the address of the function call operator. Otherwise, the value returned
by this conversion function is the address of a function `F` that, when
invoked, has the same effect as invoking the closure type’s function
call operator on a default-constructed instance of the closure type. `F`
is a constexpr function if the function call operator is a constexpr
function and is an immediate function if the function call operator is
an immediate function.

For a generic lambda with no *lambda-capture*, the closure type has a
conversion function template to pointer to function. The conversion
function template has the same invented template parameter list, and the
pointer to function has the same parameter types, as the function call
operator template. The return type of the pointer to function shall
behave as if it were a *decltype-specifier* denoting the return type of
the corresponding function call operator template specialization.

\[*Note 18*:

If the generic lambda has no *trailing-return-type* or the
*trailing-return-type* contains a placeholder type, return type
deduction of the corresponding function call operator template
specialization has to be done. The corresponding specialization is that
instantiation of the function call operator template with the same
template arguments as those deduced for the conversion function
template. Consider the following:

``` cpp
auto glambda = [](auto a) { return a; };
int (*fp)(int) = glambda;
```

The behavior of the conversion function of `glambda` above is like that
of the following conversion function:

``` cpp
struct Closure {
  template<class T> auto operator()(T t) const { ... }
  template<class T> static auto lambda_call_operator_invoker(T a) {
    // forwards execution to operator()(a) and therefore has
    // the same return type deduced
    ...
  }
  template<class T> using fptr_t =
     decltype(lambda_call_operator_invoker(declval<T>())) (*)(T);

  template<class T> operator fptr_t<T>() const
    { return &lambda_call_operator_invoker; }
};
```

— *end note*\]

\[*Example 11*:

``` cpp
void f1(int (*)(int))   { }
void f2(char (*)(int))  { }

void g(int (*)(int))    { }     // \#1
void g(char (*)(char))  { }     // \#2

void h(int (*)(int))    { }     // \#3
void h(char (*)(int))   { }     // \#4

auto glambda = [](auto a) { return a; };
f1(glambda);                    // OK
f2(glambda);                    // error: ID is not convertible
g(glambda);                     // error: ambiguous
h(glambda);                     // OK, calls \#3 since it is convertible from ID
int& (*fpi)(int*) = [](auto* a) -> auto& { return *a; };        // OK
```

— *end example*\]

If the function call operator template is a static member function
template, then the value returned by any given specialization of this
conversion function template is the address of the corresponding
function call operator template specialization. Otherwise, the value
returned by any given specialization of this conversion function
template is the address of a function `F` that, when invoked, has the
same effect as invoking the generic lambda’s corresponding function call
operator template specialization on a default-constructed instance of
the closure type. `F` is a constexpr function if the corresponding
specialization is a constexpr function and `F` is an immediate function
if the function call operator template specialization is an immediate
function.

\[*Note 19*: This will result in the implicit instantiation of the
generic lambda’s body. The instantiated generic lambda’s return type and
parameter types are required to match the return type and parameter
types of the pointer to function. — *end note*\]

\[*Example 12*:

``` cpp
auto GL = [](auto a) { std::cout << a; return a; };
int (*GL_int)(int) = GL;        // OK, through conversion function template
GL_int(3);                      // OK, same as GL(3)
```

— *end example*\]

The conversion function or conversion function template is public,
constexpr, non-virtual, non-explicit, const, and has a non-throwing
exception specification [except.spec].

\[*Example 13*:

``` cpp
auto Fwd = [](int (*fp)(int), auto a) { return fp(a); };
auto C = [](auto a) { return a; };

static_assert(Fwd(C,3) == 3);   // OK

// No specialization of the function call operator template can be constexpr (due to the local static).
auto NC = [](auto a) { static int s; return a; };
static_assert(Fwd(NC,3) == 3);  // error
```

— *end example*\]

The *lambda-expression*’s *compound-statement* yields the
*function-body* [dcl.fct.def] of the function call operator, but it is
not within the scope of the closure type.

\[*Example 14*:

``` cpp
struct S1 {
  int x, y;
  int operator()(int);
  void f() {
    [=]()->int {
      return operator()(this->x + y);   // equivalent to S1::operator()(this->x + (*this).y)
                                        // this has type S1*
    };
  }
};
```

— *end example*\]

Further, a variable \_\_func\_\_ is implicitly defined at the beginning
of the *compound-statement* of the *lambda-expression*, with semantics
as described in  [dcl.fct.def.general].

The closure type associated with a *lambda-expression* has no default
constructor if the *lambda-expression* has a *lambda-capture* and a
defaulted default constructor otherwise. It has a defaulted copy
constructor and a defaulted move constructor [class.copy.ctor]. It has a
deleted copy assignment operator if the *lambda-expression* has a
*lambda-capture* and defaulted copy and move assignment operators
otherwise [class.copy.assign].

\[*Note 20*: These special member functions are implicitly defined as
usual, which can result in them being defined as deleted. — *end note*\]

The closure type associated with a *lambda-expression* has an
implicitly-declared destructor [class.dtor].

A member of a closure type shall not be explicitly instantiated
[temp.explicit], explicitly specialized [temp.expl.spec], or named in a
friend declaration [class.friend].

#### Captures <a id="expr.prim.lambda.capture">[expr.prim.lambda.capture]</a>

``` bnf
lambda-capture:
    capture-default
    capture-list
    capture-default ',' capture-list
```

``` bnf
capture-default:
    '&'
    '='
```

``` bnf
capture-list:
    capture
    capture-list ',' capture
```

``` bnf
capture:
    simple-capture
    init-capture
```

``` bnf
simple-capture:
    identifier ['...']
    '&' identifier ['...']
    \texttt{this}
    '*' 'this'
```

``` bnf
init-capture:
    ['...'] identifier initializer
    '&' ['...'] identifier initializer
```

The body of a *lambda-expression* may refer to local entities of
enclosing block scopes by capturing those entities, as described below.

If a *lambda-capture* includes a *capture-default* that is `&`, no
identifier in a *simple-capture* of that *lambda-capture* shall be
preceded by `&`. If a *lambda-capture* includes a *capture-default* that
is `=`, each *simple-capture* of that *lambda-capture* shall be of the
form “`&` *identifier* `...}`”, “`this`”, or “`* this`”.

\[*Note 21*: The form `[&,this]` is redundant but accepted for
compatibility with ISO C++14. — *end note*\]

Ignoring appearances in *initializer* of *init-capture*, an identifier
or `this` shall not appear more than once in a *lambda-capture*.

\[*Example 15*:

``` cpp
struct S2 { void f(int i); };
void S2::f(int i) {
  [&, i]{ };        // OK
  [&, this, i]{ };  // OK, equivalent to [\&, i]
  [&, &i]{ };       // error: i preceded by \& when \& is the default
  [=, *this]{ };    // OK
  [=, this]{ };     // OK, equivalent to [=]
  [i, i]{ };        // error: i repeated
  [this, *this]{ }; // error: this appears twice
}
```

— *end example*\]

A *lambda-expression* shall not have a *capture-default* or
*simple-capture* in its *lambda-introducer* unless its innermost
enclosing scope is a block scope [basic.scope.block] or it appears
within a default member initializer and its innermost enclosing scope is
the corresponding class scope [basic.scope.class].

The *identifier* in a *simple-capture* shall denote a local entity
[basic.lookup.unqual,basic.pre]. The *simple-capture* `this` and
`* this` denote the local entity `*this`. An entity that is designated
by a *simple-capture* is said to be *explicitly captured*.

If an *identifier* in a *capture* appears as the *declarator-id* of a
parameter of the *lambda-declarator*’s *parameter-declaration-clause* or
as the name of a template parameter of the *lambda-expression*’s
*template-parameter-list*, the program is ill-formed.

\[*Example 16*:

``` cpp
void f() {
  int x = 0;
  auto g = [x](int x) { return 0; };    // error: parameter and capture have the same name
  auto h = [y = 0]<typename y>(y) { return 0; };    // error: template parameter and capture
                                                    // have the same name
}
```

— *end example*\]

An *init-capture* inhabits the lambda scope [basic.scope.lambda] of the
*lambda-expression*. An *init-capture* without ellipsis behaves as if it
declares and explicitly captures a variable of the form “`auto`
*init-capture* `;`”, except that:

- if the capture is by copy (see below), the non-static data member
  declared for the capture and the variable are treated as two different
  ways of referring to the same object, which has the lifetime of the
  non-static data member, and no additional copy and destruction is
  performed, and

- if the capture is by reference, the variable’s lifetime ends when the
  closure object’s lifetime ends.

\[*Note 22*: This enables an *init-capture* like “`x = std::move(x)`”;
the second “`x`” must bind to a declaration in the surrounding
context. — *end note*\]

\[*Example 17*:

``` cpp
int x = 4;
auto y = [&r = x, x = x+1]()->int {
            r += 2;
            return x+2;
         }();                               // Updates ::x to 6, and initializes y to 7.

auto z = [a = 42](int a) { return 1; };     // error: parameter and conceptual local variable have the same name
auto counter = [i=0]() mutable -> decltype(i) {     // OK, returns int
  return i++;
};
```

— *end example*\]

For the purposes of lambda capture, an expression potentially references
local entities as follows:

- An *id-expression* that names a local entity potentially references
  that entity; an *id-expression* that names one or more non-static
  class members and does not form a pointer to member [expr.unary.op]
  potentially references `*this`.

  \[*Note 4*: This occurs even if overload resolution selects a static
  member function for the *id-expression*. — *end note*\]

- A `this` expression potentially references `*this`.

- A *lambda-expression* potentially references the local entities named
  by its *simple-capture*.

If an expression potentially references a local entity within a scope in
which it is odr-usable [basic.def.odr], and the expression would be
potentially evaluated if the effect of any enclosing `typeid`
expressions [expr.typeid] were ignored, the entity is said to be
*implicitly captured* by each intervening *lambda-expression* with an
associated *capture-default* that does not explicitly capture it. The
implicit capture of `*this` is deprecated when the *capture-default* is
`=`; see [depr.capture.this].

\[*Example 18*:

``` cpp
void f(int, const int (&)[2] = {});         // \#1
void f(const int&, const int (&)[1]);       // \#2
void test() {
  const int x = 17;
  auto g = [](auto a) {
    f(x);                       // OK, calls \#1, does not capture x
  };

  auto g1 = [=](auto a) {
    f(x);                       // OK, calls \#1, captures x
  };

  auto g2 = [=](auto a) {
    int selector[sizeof(a) == 1 ? 1 : 2]{};
    f(x, selector);             // OK, captures x, can call \#1 or \#2
  };

  auto g3 = [=](auto a) {
    typeid(a + x);              // captures x regardless of whether a + x is an unevaluated operand
  };
}
```

Within `g1`, an implementation can optimize away the capture of `x` as
it is not odr-used.

— *end example*\]

\[*Note 23*:

The set of captured entities is determined syntactically, and entities
are implicitly captured even if the expression denoting a local entity
is within a discarded statement [stmt.if].

— *end note*\]

An entity is *captured* if it is captured explicitly or implicitly. An
entity captured by a *lambda-expression* is odr-used [term.odr.use] by
the *lambda-expression*.

\[*Note 24*: As a consequence, if a *lambda-expression* explicitly
captures an entity that is not odr-usable, the program is ill-formed
[basic.def.odr]. — *end note*\]

\[*Example 19*:

``` cpp
void f1(int i) {
  int const N = 20;
  auto m1 = [=]{
    int const M = 30;
    auto m2 = [i]{
      int x[N][M];              // OK, N and M are not odr-used
      x[0][0] = i;              // OK, i is explicitly captured by m2 and implicitly captured by m1
    };
  };
  struct s1 {
    int f;
    void work(int n) {
      int m = n*n;
      int j = 40;
      auto m3 = [this,m] {
        auto m4 = [&,j] {       // error: j not odr-usable due to intervening lambda m3
          int x = n;            // error: n is odr-used but not odr-usable due to intervening lambda m3
          x += m;               // OK, m implicitly captured by m4 and explicitly captured by m3
          x += i;               // error: i is odr-used but not odr-usable
                                // due to intervening function and class scopes
          x += f;               // OK, this captured implicitly by m4 and explicitly by m3
        };
      };
    }
  };
}

struct s2 {
  double ohseven = .007;
  auto f() {
    return [this] {
      return [*this] {
          return ohseven;       // OK
      };
    }();
  }
  auto g() {
    return [] {
      return [*this] { };       // error: *this not captured by outer lambda-expression
    }();
  }
};
```

— *end example*\]

\[*Note 25*: Because local entities are not odr-usable within a default
argument [basic.def.odr], a *lambda-expression* appearing in a default
argument cannot implicitly or explicitly capture any local entity. Such
a *lambda-expression* can still have an *init-capture* if any
full-expression in its *initializer* satisfies the constraints of an
expression appearing in a default argument
[dcl.fct.default]. — *end note*\]

\[*Example 20*:

``` cpp
void f2() {
  int i = 1;
  void g1(int = ([i]{ return i; })());          // error
  void g2(int = ([i]{ return 0; })());          // error
  void g3(int = ([=]{ return i; })());          // error
  void g4(int = ([=]{ return 0; })());          // OK
  void g5(int = ([]{ return sizeof i; })());    // OK
  void g6(int = ([x=1]{ return x; })());        // OK
  void g7(int = ([x=i]{ return x; })());        // error
}
```

— *end example*\]

An entity is *captured by copy* if

- it is implicitly captured, the *capture-default* is `=`, and the
  captured entity is not `*this`, or

- it is explicitly captured with a capture that is not of the form
  `this`, `&` *identifier*, or `&` *identifier* *initializer*.

For each entity captured by copy, an unnamed non-static data member is
declared in the closure type. The declaration order of these members is
unspecified. The type of such a data member is the referenced type if
the entity is a reference to an object, an lvalue reference to the
referenced function type if the entity is a reference to a function, or
the type of the corresponding captured entity otherwise. A member of an
anonymous union shall not be captured by copy.

Every *id-expression* within the *compound-statement* of a
*lambda-expression* that is an odr-use [term.odr.use] of an entity
captured by copy is transformed into an access to the corresponding
unnamed data member of the closure type.

\[*Note 26*: An *id-expression* that is not an odr-use refers to the
original entity, never to a member of the closure type. However, such an
*id-expression* can still cause the implicit capture of the
entity. — *end note*\]

If `*this` is captured by copy, each expression that odr-uses `*this` is
transformed to instead refer to the corresponding unnamed data member of
the closure type.

\[*Example 21*:

``` cpp
void f(const int*);
void g() {
  const int N = 10;
  [=] {
    int arr[N];     // OK, not an odr-use, refers to automatic variable
    f(&N);          // OK, causes N to be captured; \&N points to
                    // the corresponding member of the closure type
  };
}
```

— *end example*\]

An entity is *captured by reference* if it is implicitly or explicitly
captured but not captured by copy. It is unspecified whether additional
unnamed non-static data members are declared in the closure type for
entities captured by reference. If declared, such non-static data
members shall be of literal type.

\[*Example 22*:

``` cpp
// The inner closure type must be a literal type regardless of how reference captures are represented.
static_assert([](int n) { return [&n] { return ++n; }(); }(3) == 4);
```

— *end example*\]

A bit-field or a member of an anonymous union shall not be captured by
reference.

An *id-expression* within the *compound-statement* of a
*lambda-expression* that is an odr-use of a reference captured by
reference refers to the entity to which the captured reference is bound
and not to the captured reference.

\[*Note 27*: The validity of such captures is determined by the lifetime
of the object to which the reference refers, not by the lifetime of the
reference itself. — *end note*\]

\[*Example 23*:

``` cpp
auto h(int &r) {
  return [&] {
    ++r;            // Valid after h returns if the lifetime of the
                    // object to which r is bound has not ended
  };
}
```

— *end example*\]

If a *lambda-expression* `m2` captures an entity and that entity is
captured by an immediately enclosing *lambda-expression* `m1`, then
`m2`’s capture is transformed as follows:

- If `m1` captures the entity by copy, `m2` captures the corresponding
  non-static data member of `m1`’s closure type; if `m1` is not
  `mutable`, the non-static data member is considered to be
  const-qualified.

- If `m1` captures the entity by reference, `m2` captures the same
  entity captured by `m1`.

\[*Example 24*:

The nested *lambda-expression*s and invocations below will output
`123234`.

``` cpp
int a = 1, b = 1, c = 1;
auto m1 = [a, &b, &c]() mutable {
  auto m2 = [a, b, &c]() mutable {
    std::cout << a << b << c;
    a = 4; b = 4; c = 4;
  };
  a = 3; b = 3; c = 3;
  m2();
};
a = 2; b = 2; c = 2;
m1();
std::cout << a << b << c;
```

— *end example*\]

When the *lambda-expression* is evaluated, the entities that are
captured by copy are used to direct-initialize each corresponding
non-static data member of the resulting closure object, and the
non-static data members corresponding to the *init-capture* are
initialized as indicated by the corresponding *initializer* (which may
be copy- or direct-initialization). (For array members, the array
elements are direct-initialized in increasing subscript order.) These
initializations are performed in the (unspecified) order in which the
non-static data members are declared.

\[*Note 28*: This ensures that the destructions will occur in the
reverse order of the constructions. — *end note*\]

\[*Note 29*: If a non-reference entity is implicitly or explicitly
captured by reference, invoking the function call operator of the
corresponding *lambda-expression* after the lifetime of the entity has
ended is likely to result in undefined behavior. — *end note*\]

A *simple-capture* containing an ellipsis is a pack expansion
[temp.variadic]. An *init-capture* containing an ellipsis is a pack
expansion that declares an *init-capture* pack [temp.variadic].

\[*Example 25*:

``` cpp
template<class... Args>
void f(Args... args) {
  auto lm = [&, args...] { return g(args...); };
  lm();

  auto lm2 = [...xs=std::move(args)] { return g(xs...); };
  lm2();
}
```

— *end example*\]

### Fold expressions <a id="expr.prim.fold">[expr.prim.fold]</a>

A fold expression performs a fold of a pack [temp.variadic] over a
binary operator.

``` bnf
fold-expression:
    '(' cast-expression fold-operator '...' ')'
    '(' '...' fold-operator cast-expression ')'
    '(' cast-expression fold-operator '...' fold-operator cast-expression ')'
```

``` bnf
%% Ed. note: character protrusion would misalign operators with leading `-`.

fold-operator: one of
    '+ '\quad'- '\quad'* '\quad'/ '\quad'% '\quad'\caret{' }\quad'& '\quad'| '\quad'<< '\quad'>> '
    '+='\quad'-='\quad'*='\quad'/='\quad'%='\quad'\caret='\quad'&='\quad'|='\quad'<<='\quad'>>='\quad'='
    '=='\quad'!='\quad'< '\quad'> '\quad'<='\quad'>='\quad'&&'\quad'||'\quad',  '\quad'.* '\quad'->*'
```

An expression of the form `(...` *op* `e)` where *op* is a
*fold-operator* is called a *unary left fold*. An expression of the form
`(e` *op* `...)` where *op* is a *fold-operator* is called a
*unary right fold*. Unary left folds and unary right folds are
collectively called *unary folds*. In a unary fold, the
*cast-expression* shall contain an unexpanded pack [temp.variadic].

An expression of the form `(e1` *op1* `...` *op2* `e2)` where *op1* and
*op2* are *fold-operator* is called a *binary fold*. In a binary fold,
*op1* and *op2* shall be the same *fold-operator*, and either `e1` shall
contain an unexpanded pack or `e2` shall contain an unexpanded pack, but
not both. If `e2` contains an unexpanded pack, the expression is called
a *binary left fold*. If `e1` contains an unexpanded pack, the
expression is called a *binary right fold*.

\[*Example 26*:

``` cpp
template<typename ...Args>
bool f(Args ...args) {
  return (true && ... && args); // OK
}

template<typename ...Args>
bool f(Args ...args) {
  return (args + ... + args);   // error: both operands contain unexpanded packs
}
```

— *end example*\]

### Requires expressions <a id="expr.prim.req">[expr.prim.req]</a>

#### General <a id="expr.prim.req.general">[expr.prim.req.general]</a>

A *requires-expression* provides a concise way to express requirements
on template arguments that can be checked by name lookup [basic.lookup]
or by checking properties of types and expressions.

``` bnf
requires-expression:
    \texttt{requires} [requirement-parameter-list] requirement-body
```

``` bnf
requirement-parameter-list:
    '(' parameter-declaration-clause ')'
```

``` bnf
requirement-body:
    '{' requirement-seq '$'}
```

``` bnf
requirement-seq:
    requirement
    requirement requirement-seq
```

``` bnf
requirement:
    simple-requirement
    type-requirement
    compound-requirement
    nested-requirement
```

A *requires-expression* is a prvalue of type `bool` whose value is
described below. Expressions appearing within a *requirement-body* are
unevaluated operands [term.unevaluated.operand].

\[*Example 27*:

A common use of *requires-expression*s is to define requirements in
concepts such as the one below:

``` cpp
template<typename T>
  concept R = requires (T i) {
    typename T::type;
    {*i} -> std::convertible_to<const typename T::type&>;
  };
```

A *requires-expression* can also be used in a *requires-clause*
[temp.pre] as a way of writing ad hoc constraints on template arguments
such as the one below:

``` cpp
template<typename T>
  requires requires (T x) { x + x; }
    T add(T a, T b) { return a + b; }
```

The first `requires` introduces the *requires-clause*, and the second
introduces the *requires-expression*.

— *end example*\]

A *requires-expression* may introduce local parameters using a
*parameter-declaration-clause* [dcl.fct]. A local parameter of a
*requires-expression* shall not have a default argument. These
parameters have no linkage, storage, or lifetime; they are only used as
notation for the purpose of defining *requirement*s. The
*parameter-declaration-clause* of a *requirement-parameter-list* shall
not terminate with an ellipsis.

\[*Example 28*:

``` cpp
template<typename T>
concept C = requires(T t, ...) {    // error: terminates with an ellipsis
  t;
};
```

— *end example*\]

The substitution of template arguments into a *requires-expression* may
result in the formation of invalid types or expressions in its
*requirement*s or the violation of the semantic constraints of those
*requirement*s. In such cases, the *requires-expression* evaluates to
`false`; it does not cause the program to be ill-formed. The
substitution and semantic constraint checking proceeds in lexical order
and stops when a condition that determines the result of the
*requires-expression* is encountered. If substitution (if any) and
semantic constraint checking succeed, the *requires-expression*
evaluates to `true`.

\[*Note 30*: If a *requires-expression* contains invalid types or
expressions in its *requirement*s, and it does not appear within the
declaration of a templated entity, then the program is
ill-formed. — *end note*\]

If the substitution of template arguments into a *requirement* would
always result in a substitution failure, the program is ill-formed; no
diagnostic required.

\[*Example 29*:

``` cpp
template<typename T> concept C =
requires {
  new int[-(int)sizeof(T)];     // ill-formed, no diagnostic required
};
```

— *end example*\]

#### Simple requirements <a id="expr.prim.req.simple">[expr.prim.req.simple]</a>

``` bnf
simple-requirement:
    expression ';'
```

A *simple-requirement* asserts the validity of an *expression*.

\[*Note 31*: The enclosing *requires-expression* will evaluate to
`false` if substitution of template arguments into the *expression*
fails. The *expression* is an unevaluated operand
[term.unevaluated.operand]. — *end note*\]

\[*Example 30*:

``` cpp
template<typename T> concept C =
  requires (T a, T b) {
    a + b;          // C<T> is true if a + b is a valid expression
  };
```

— *end example*\]

A *requirement* that starts with a `requires` token is never interpreted
as a *simple-requirement*.

\[*Note 32*: This simplifies distinguishing between a
*simple-requirement* and a *nested-requirement*. — *end note*\]

#### Type requirements <a id="expr.prim.req.type">[expr.prim.req.type]</a>

``` bnf
type-requirement:
    \texttt{typename} [nested-name-specifier] type-name ';'
```

A *type-requirement* asserts the validity of a type.

\[*Note 33*: The enclosing *requires-expression* will evaluate to
`false` if substitution of template arguments fails. — *end note*\]

\[*Example 31*:

``` cpp
template<typename T, typename T::type = 0> struct S;
template<typename T> using Ref = T&;

template<typename T> concept C = requires {
  typename T::inner;    // required nested member name
  typename S<T>;        // required valid[temp.names] template-id;
                        // fails if T::type does not exist as a type to which 0 can be implicitly converted
  typename Ref<T>;      // required alias template substitution, fails if T is void
};
```

— *end example*\]

A *type-requirement* that names a class template specialization does not
require that type to be complete [term.incomplete.type].

#### Compound requirements <a id="expr.prim.req.compound">[expr.prim.req.compound]</a>

``` bnf
compound-requirement:
    '{' expression '$'} [\texttt{noexcept]} [return-type-requirement] ';'
```

``` bnf
return-type-requirement:
    '->' type-constraint
```

A *compound-requirement* asserts properties of the *expression* E.
Substitution of template arguments (if any) and verification of semantic
properties proceed in the following order:

- Substitution of template arguments (if any) into the *expression* is
  performed.

- If the `noexcept` specifier is present, E shall not be a
  potentially-throwing expression [except.spec].

- If the *return-type-requirement* is present, then:

  - Substitution of template arguments (if any) into the
    *return-type-requirement* is performed.

  - The immediately-declared constraint [temp.param] of the
    *type-constraint* for `decltype((E))` shall be satisfied.

  \[*Example 4*:

  Given concepts `C` and `D`,

  ``` cpp
  requires {
    { E1 } -> C;
    { E2 } -> D<A$_1$, $\cdots$, A$_n$>;
  };
  ```

  is equivalent to

  ``` cpp
  requires {
    E1; requires C<decltype((E1))>;
    E2; requires D<decltype((E2)), A$_1$, $\cdots$, A$_n$>;
  };
  ```

  (including in the case where n is zero).

  — *end example*\]

\[*Example 32*:

``` cpp
template<typename T> concept C1 = requires(T x) {
  {x++};
};
```

The *compound-requirement* in `C1` requires that `x++` is a valid
expression. It is equivalent to the *simple-requirement* `x++;`.

``` cpp
template<typename T> concept C2 = requires(T x) {
  {*x} -> std::same_as<typename T::inner>;
};
```

The *compound-requirement* in `C2` requires that `*x` is a valid
expression, that `typename T::inner` is a valid type, and that
`std::same_as<decltype((*x)), typename T::inner>` is satisfied.

``` cpp
template<typename T> concept C3 =
  requires(T x) {
    {g(x)} noexcept;
  };
```

The *compound-requirement* in `C3` requires that `g(x)` is a valid
expression and that `g(x)` is non-throwing.

— *end example*\]

#### Nested requirements <a id="expr.prim.req.nested">[expr.prim.req.nested]</a>

``` bnf
nested-requirement:
    \texttt{requires} constraint-expression ';'
```

A *nested-requirement* can be used to specify additional constraints in
terms of local parameters. The *constraint-expression* shall be
satisfied [temp.constr.decl] by the substituted template arguments, if
any. Substitution of template arguments into a *nested-requirement* does
not result in substitution into the *constraint-expression* other than
as specified in [temp.constr.constr].

\[*Example 33*:

``` cpp
template<typename U> concept C = sizeof(U) == 1;

template<typename T> concept D = requires (T t) {
  requires C<decltype (+t)>;
};
```

`D<T>` is satisfied if `sizeof(decltype (+t)) == 1`
[temp.constr.atomic].

— *end example*\]

## Compound expressions <a id="expr.compound">[expr.compound]</a>

### Postfix expressions <a id="expr.post">[expr.post]</a>

#### General <a id="expr.post.general">[expr.post.general]</a>

Postfix expressions group left-to-right.

``` bnf
postfix-expression:
    primary-expression
    postfix-expression '[' [expression-list] ']'
    postfix-expression '(' [expression-list] ')'
    simple-type-specifier '(' [expression-list] ')'
    typename-specifier '(' [expression-list] ')'
    simple-type-specifier braced-init-list
    typename-specifier braced-init-list
    postfix-expression '.' ['template'] id-expression
    postfix-expression '->' ['template'] id-expression
    postfix-expression '++'
    postfix-expression '--'
    \texttt{dynamic_cast} '<' type-id '>' '(' expression ')'
    \texttt{static_cast} '<' type-id '>' '(' expression ')'
    \texttt{reinterpret_cast} '<' type-id '>' '(' expression ')'
    \texttt{const_cast} '<' type-id '>' '(' expression ')'
    \texttt{typeid} '(' expression ')'
    \texttt{typeid} '(' type-id ')'
```

``` bnf
expression-list:
    initializer-list
```

\[*Note 1*: The `>` token following the *type-id* in a `dynamic_cast`,
`static_cast`, `reinterpret_cast`, or `const_cast` can be the product of
replacing a `>>` token by two consecutive `>` tokens
[temp.names]. — *end note*\]

#### Subscripting <a id="expr.sub">[expr.sub]</a>

A *subscript expression* is a postfix expression followed by square
brackets containing a possibly empty, comma-separated list of
*initializer-clause*s that constitute the arguments to the subscript
operator. The *postfix-expression* and the initialization of the object
parameter of any applicable subscript operator function is sequenced
before each expression in the *expression-list* and also before any
default argument. The initialization of a non-object parameter of a
subscript operator function `S` [over.sub], including every associated
value computation and side effect, is indeterminately sequenced with
respect to that of any other non-object parameter of `S`.

With the built-in subscript operator, an *expression-list* shall be
present, consisting of a single *assignment-expression*. One of the
expressions shall be a glvalue of type “array of `T`” or a prvalue of
type “pointer to `T`” and the other shall be a prvalue of unscoped
enumeration or integral type. The result is of type “`T`”. The type
“`T`” shall be a completely-defined object type.

The expression `E1[E2]` is identical (by definition) to `*((E1)+(E2))`,
except that in the case of an array operand, the result is an lvalue if
that operand is an lvalue and an xvalue otherwise.

\[*Note 2*: Despite its asymmetric appearance, subscripting is a
commutative operation except for sequencing. See  [expr.unary] and 
[expr.add] for details of `*` and `+` and  [dcl.array] for details of
array types. — *end note*\]

#### Function call <a id="expr.call">[expr.call]</a>

A function call is a postfix expression followed by parentheses
containing a possibly empty, comma-separated list of
*initializer-clause* which constitute the arguments to the function.

\[*Note 3*: If the postfix expression is a function or member function
name, the appropriate function and the validity of the call are
determined according to the rules in  [over.match]. — *end note*\]

The postfix expression shall have function type or function pointer
type. For a call to a non-member function or to a static member
function, the postfix expression shall either be an lvalue that refers
to a function (in which case the function-to-pointer standard conversion
[conv.func] is suppressed on the postfix expression), or have function
pointer type.

If the selected function is non-virtual, or if the *id-expression* in
the class member access expression is a *qualified-id*, that function is
called. Otherwise, its final overrider [class.virtual] in the dynamic
type of the object expression is called; such a call is referred to as a
*virtual function call*.

\[*Note 4*: The dynamic type is the type of the object referred to by
the current value of the object expression. [class.cdtor] describes the
behavior of virtual function calls when the object expression refers to
an object under construction or destruction. — *end note*\]

\[*Note 5*: If a function or member function name is used, and name
lookup [basic.lookup] does not find a declaration of that name, the
program is ill-formed. No function is implicitly declared by such a
call. — *end note*\]

If the *postfix-expression* names a destructor or pseudo-destructor
[expr.prim.id.dtor], the type of the function call expression is `void`;
otherwise, the type of the function call expression is the return type
of the statically chosen function (i.e., ignoring the `virtual`
keyword), even if the type of the function actually called is different.
If the *postfix-expression* names a pseudo-destructor (in which case the
*postfix-expression* is a possibly-parenthesized class member access),
the function call destroys the object of scalar type denoted by the
object expression of the class member access [expr.ref,basic.life].

Calling a function through an expression whose function type `E` is
different from the function type `F` of the called function’s definition
results in undefined behavior unless the type “pointer to `F`” can be
converted to the type “pointer to `E`” via a function pointer conversion
[conv.fctptr].

\[*Note 6*: The exception applies when the expression has the type of a
potentially-throwing function, but the called function has a
non-throwing exception specification, and the function types are
otherwise the same. — *end note*\]

When a function is called, each parameter [dcl.fct] is initialized
[dcl.init,class.copy.ctor] with its corresponding argument. If the
function is an explicit object member function and there is an implied
object argument [over.call.func], the list of provided arguments is
preceded by the implied object argument for the purposes of this
correspondence. If there is no corresponding argument, the default
argument for the parameter is used.

\[*Example 1*:

``` cpp
template<typename ...T> int f(int n = 0, T ...t);
int x = f<int>();               // error: no argument for second function parameter
```

— *end example*\]

If the function is an implicit object member function, the `this`
parameter of the function [expr.prim.this] is initialized with a pointer
to the object of the call, converted as if by an explicit type
conversion [expr.cast].

\[*Note 7*: There is no access or ambiguity checking on this conversion;
the access checking and disambiguation are done as part of the (possibly
implicit) class member access operator. See  [class.member.lookup],
[class.access.base], and  [expr.ref]. — *end note*\]

When a function is called, the type of any parameter shall not be a
class type that is either incomplete or abstract.

\[*Note 8*: This still allows a parameter to be a pointer or reference
to such a type. However, it prevents a passed-by-value parameter to have
an incomplete or abstract class type. — *end note*\]

It is *implementation-defined* whether the lifetime of a parameter ends
when the function in which it is defined returns or at the end of the
enclosing full-expression. The initialization and destruction of each
parameter occurs within the context of the calling function.

\[*Example 2*: The access of the constructor, conversion functions or
destructor is checked at the point of call in the calling function. If a
constructor or destructor for a function parameter throws an exception,
the search for a handler starts in the calling function; in particular,
if the function called has a *function-try-block* [except.pre] with a
handler that can handle the exception, this handler is not
considered. — *end example*\]

The *postfix-expression* is sequenced before each *expression* in the
*expression-list* and any default argument. The initialization of a
parameter, including every associated value computation and side effect,
is indeterminately sequenced with respect to that of any other
parameter.

\[*Note 9*: All side effects of argument evaluations are sequenced
before the function is entered (see  [intro.execution]). — *end note*\]

\[*Example 3*:

``` cpp
void f() {
  std::string s = "but I have heard it works even if you don't believe in it";
  s.replace(0, 4, "").replace(s.find("even"), 4, "only").replace(s.find(" don't"), 6, "");
  assert(s == "I have heard it works only if you believe in it");       // OK
}
```

— *end example*\]

\[*Note 10*: If an operator function is invoked using operator notation,
argument evaluation is sequenced as specified for the built-in operator;
see  [over.match.oper]. — *end note*\]

\[*Example 4*:

``` cpp
struct S {
  S(int);
};
int operator<<(S, int);
int i, j;
int x = S(i=1) << (i=2);
int y = operator<<(S(j=1), j=2);
```

After performing the initializations, the value of `i` is 2 (see 
[expr.shift]), but it is unspecified whether the value of `j` is 1 or 2.

— *end example*\]

The result of a function call is the result of the possibly-converted
operand of the `return` statement [stmt.return] that transferred control
out of the called function (if any), except in a virtual function call
if the return type of the final overrider is different from the return
type of the statically chosen function, the value returned from the
final overrider is converted to the return type of the statically chosen
function.

\[*Note 11*:  A function can change the values of its non-const
parameters, but these changes cannot affect the values of the arguments
except where a parameter is of a reference type [dcl.ref]; if the
reference is to a const-qualified type, `const_cast` is required to be
used to cast away the constness in order to modify the argument’s value.
Where a parameter is of `const` reference type a temporary object is
introduced if needed
[dcl.type,lex.literal,lex.string,dcl.array,class.temporary]. In
addition, it is possible to modify the values of non-constant objects
through pointer parameters. — *end note*\]

A function can be declared to accept fewer arguments (by declaring
default arguments [dcl.fct.default]) or more arguments (by using the
ellipsis, `...`, or a function parameter pack [dcl.fct]) than the number
of parameters in the function definition [dcl.fct.def].

\[*Note 12*: This implies that, except where the ellipsis (`...`) or a
function parameter pack is used, a parameter is available for each
argument. — *end note*\]

When there is no parameter for a given argument, the argument is passed
in such a way that the receiving function can obtain the value of the
argument by invoking `va_arg` [support.runtime].

\[*Note 13*: This paragraph does not apply to arguments passed to a
function parameter pack. Function parameter packs are expanded during
template instantiation [temp.variadic], thus each such argument has a
corresponding parameter when a function template specialization is
actually called. — *end note*\]

The lvalue-to-rvalue [conv.lval], array-to-pointer [conv.array], and
function-to-pointer [conv.func] standard conversions are performed on
the argument expression. An argument that has type cv `std::nullptr_t`
is converted to type `void*` [conv.ptr]. After these conversions, if the
argument does not have arithmetic, enumeration, pointer,
pointer-to-member, or class type, the program is ill-formed. Passing a
potentially-evaluated argument of a scoped enumeration type or of a
class type [class] having an eligible non-trivial copy constructor, an
eligible non-trivial move constructor, or a non-trivial destructor
[special], with no corresponding parameter, is conditionally-supported
with *implementation-defined* semantics. If the argument has integral or
enumeration type that is subject to the integral promotions [conv.prom],
or a floating-point type that is subject to the floating-point promotion
[conv.fpprom], the value of the argument is converted to the promoted
type before the call. These promotions are referred to as the
*default argument promotions*.

Recursive calls are permitted, except to the `main` function
[basic.start.main].

A function call is an lvalue if the result type is an lvalue reference
type or an rvalue reference to function type, an xvalue if the result
type is an rvalue reference to object type, and a prvalue otherwise.

#### Explicit type conversion (functional notation) <a id="expr.type.conv">[expr.type.conv]</a>

A *simple-type-specifier* [dcl.type.simple] or *typename-specifier*
[temp.res] followed by a parenthesized optional *expression-list* or by
a *braced-init-list* (the initializer) constructs a value of the
specified type given the initializer. If the type is a placeholder for a
deduced class type, it is replaced by the return type of the function
selected by overload resolution for class template deduction
[over.match.class.deduct] for the remainder of this subclause.
Otherwise, if the type contains a placeholder type, it is replaced by
the type determined by placeholder type deduction
[dcl.type.auto.deduct].

\[*Example 5*:

``` cpp
struct A {};
void f(A&);             // \#1
void f(A&&);            // \#2
A& g();
void h() {
  f(g());               // calls \#1
  f(A(g()));            // calls \#2 with a temporary object
  f(auto(g()));         // calls \#2 with a temporary object
}
```

— *end example*\]

If the initializer is a parenthesized single expression, the type
conversion expression is equivalent to the corresponding cast expression
[expr.cast]. Otherwise, if the type is cv `void` and the initializer is
`()` or `\{\}` (after pack expansion, if any), the expression is a
prvalue of type `void` that performs no initialization. Otherwise, the
expression is a prvalue of the specified type whose result object is
direct-initialized [dcl.init] with the initializer. If the initializer
is a parenthesized optional *expression-list*, the specified type shall
not be an array type.

#### Class member access <a id="expr.ref">[expr.ref]</a>

A postfix expression followed by a dot `.` or an arrow `->`, optionally
followed by the keyword `template`, and then followed by an
*id-expression*, is a postfix expression. The postfix expression before
the dot or arrow is evaluated;

the result of that evaluation, together with the *id-expression*,
determines the result of the entire postfix expression.

\[*Note 14*: If the keyword `template` is used, the following
unqualified name is considered to refer to a template [temp.names]. If a
*simple-template-id* results and is followed by a `::`, the
*id-expression* is a *qualified-id*. — *end note*\]

For the first option (dot) the first expression shall be a glvalue. For
the second option (arrow) the first expression shall be a prvalue having
pointer type. The expression `E1->E2` is converted to the equivalent
form `(*(E1)).E2`; the remainder of [expr.ref] will address only the
first option (dot).

Abbreviating *postfix-expression*`.`*id-expression* as `E1.E2`, `E1` is
called the *object expression*. If the object expression is of scalar
type, `E2` shall name the pseudo-destructor of that same type (ignoring
cv-qualifications) and `E1.E2` is a prvalue of type “function of ()
returning `void`”.

\[*Note 15*: This value can only be used for a notional function call
[expr.prim.id.dtor]. — *end note*\]

Otherwise, the object expression shall be of class type. The class type
shall be complete unless the class member access appears in the
definition of that class.

\[*Note 16*: The program is ill-formed if the result differs from that
when the class is complete [class.member.lookup]. — *end note*\]

\[*Note 17*:  [basic.lookup.qual] describes how names are looked up
after the `.` and `->` operators. — *end note*\]

If `E2` is a bit-field, `E1.E2` is a bit-field. The type and value
category of `E1.E2` are determined as follows. In the remainder of 
[expr.ref], represents either `const` or the absence of `const` and
represents either `volatile` or the absence of `volatile`. represents an
arbitrary set of cv-qualifiers, as defined in  [basic.type.qualifier].

If `E2` is declared to have type “reference to `T`”, then `E1.E2` is an
lvalue of type `T`. If `E2` is a static data member, `E1.E2` designates
the object or function to which the reference is bound, otherwise
`E1.E2` designates the object or function to which the corresponding
reference member of `E1` is bound. Otherwise, one of the following rules
applies.

- If `E2` is a static data member and the type of `E2` is `T`, then
  `E1.E2` is an lvalue; the expression designates the named member of
  the class. The type of `E1.E2` is `T`.

- If `E2` is a non-static data member and the type of `E1` is “ `X`”,
  and the type of `E2` is “ `T`”, the expression designates the
  corresponding member subobject of the object designated by the first
  expression. If `E1` is an lvalue, then `E1.E2` is an lvalue; otherwise
  `E1.E2` is an xvalue. Let the notation stand for the “union” of and ;
  that is, if or is `volatile`, then is `volatile`. Similarly, let the
  notation stand for the “union” of and ; that is, if or is `const`,
  then is `const`. If `E2` is declared to be a `mutable` member, then
  the type of `E1.E2` is “ `T`”. If `E2` is not declared to be a
  `mutable` member, then the type of `E1.E2` is “ `T`”.

- If `E2` is an overload set, function overload resolution [over.match]
  is used to select the function to which `E2` refers. The type of
  `E1.E2` is the type of `E2` and `E1.E2` refers to the function
  referred to by `E2`.

  - If `E2` refers to a static member function, `E1.E2` is an lvalue.

  - Otherwise (when `E2` refers to a non-static member function),
    `E1.E2` is a prvalue. The expression can be used only as the
    left-hand operand of a member function call [class.mfct].

    \[*Note 5*: Any redundant set of parentheses surrounding the
    expression is ignored [expr.prim.paren]. — *end note*\]

- If `E2` is a nested type, the expression `E1.E2` is ill-formed.

- If `E2` is a member enumerator and the type of `E2` is `T`, the
  expression `E1.E2` is a prvalue of type `T` whose value is the value
  of the enumerator.

If `E2` is a non-static member, the program is ill-formed if the class
of which `E2` is directly a member is an ambiguous base
[class.member.lookup] of the naming class [class.access.base] of `E2`.

\[*Note 18*: The program is also ill-formed if the naming class is an
ambiguous base of the class type of the object expression; see 
[class.access.base]. — *end note*\]

If `E2` is a non-static member and the result of `E1` is an object whose
type is not similar [conv.qual] to the type of `E1`, the behavior is
undefined.

\[*Example 6*:

``` cpp
struct A { int i; };
struct B { int j; };
struct D : A, B {};
void f() {
  D d;
  static_cast<B&>(d).j;             // OK, object expression designates the B subobject of d
  reinterpret_cast<B&>(d).j;        // undefined behavior
}
```

— *end example*\]

#### Increment and decrement <a id="expr.post.incr">[expr.post.incr]</a>

The value of a postfix `++` expression is the value of its operand.

\[*Note 19*: The value obtained is a copy of the original
value. — *end note*\]

The operand shall be a modifiable lvalue. The type of the operand shall
be an arithmetic type other than cv `bool`, or a pointer to a complete
object type. An operand with volatile-qualified type is deprecated; see 
[depr.volatile.type]. The value of the operand object is modified
[defns.access] by adding `1` to it. The value computation of the `++`
expression is sequenced before the modification of the operand object.
With respect to an indeterminately-sequenced function call, the
operation of postfix `++` is a single evaluation.

\[*Note 20*: Therefore, a function call cannot intervene between the
lvalue-to-rvalue conversion and the side effect associated with any
single postfix `++` operator. — *end note*\]

The result is a prvalue. The type of the result is the cv-unqualified
version of the type of the operand. If the operand is a bit-field that
cannot represent the incremented value, the resulting value of the
bit-field is . See also  [expr.add] and  [expr.ass].

The operand of postfix `--` is decremented analogously to the postfix
`++` operator.

\[*Note 21*: For prefix increment and decrement, see 
[expr.pre.incr]. — *end note*\]

#### Dynamic cast <a id="expr.dynamic.cast">[expr.dynamic.cast]</a>

The result of the expression `dynamic_cast<T>(v)` is the result of
converting the expression `v` to type `T`. `T` shall be a pointer or
reference to a complete class type, or “pointer to cv `void`”. The
`dynamic_cast` operator shall not cast away constness [expr.const.cast].

If `T` is a pointer type, `v` shall be a prvalue of a pointer to
complete class type, and the result is a prvalue of type `T`. If `T` is
an lvalue reference type, `v` shall be an lvalue of a complete class
type, and the result is an lvalue of the type referred to by `T`. If `T`
is an rvalue reference type, `v` shall be a glvalue having a complete
class type, and the result is an xvalue of the type referred to by `T`.

If the type of `v` is the same as `T` (ignoring cv-qualifications), the
result is `v` (converted if necessary).

If `T` is “pointer to `B`” and `v` has type “pointer to `D`” such that
`B` is a base class of `D`, the result is a pointer to the unique `B`
subobject of the `D` object pointed to by `v`, or a null pointer value
if `v` is a null pointer value. Similarly, if `T` is “reference to `B`”
and `v` has type `D` such that `B` is a base class of `D`, the result is
the unique `B` subobject of the `D` object referred to by `v`.

In both the pointer and reference cases, the program is ill-formed if
`B` is an inaccessible or ambiguous base class of `D`.

\[*Example 7*:

``` cpp
struct B { };
struct D : B { };
void foo(D* dp) {
  B*  bp = dynamic_cast<B*>(dp);    // equivalent to B* bp = dp;
}
```

— *end example*\]

Otherwise, `v` shall be a pointer to or a glvalue of a polymorphic type
[class.virtual].

If `v` is a null pointer value, the result is a null pointer value.

If `T` is “pointer to cv `void`”, then the result is a pointer to the
most derived object pointed to by `v`. Otherwise, a runtime check is
applied to see if the object pointed or referred to by `v` can be
converted to the type pointed or referred to by `T`.

Let `C` be the class type to which `T` points or refers. The runtime
check logically executes as follows:

- If, in the most derived object pointed (referred) to by `v`, `v`
  points (refers) to a public base class subobject of a `C` object, and
  if only one object of type `C` is derived from the subobject pointed
  (referred) to by `v` the result points (refers) to that `C` object.

- Otherwise, if `v` points (refers) to a public base class subobject of
  the most derived object, and the type of the most derived object has a
  base class, of type `C`, that is unambiguous and public, the result
  points (refers) to the `C` subobject of the most derived object.

- Otherwise, the runtime check *fails*.

The value of a failed cast to pointer type is the null pointer value of
the required result type. A failed cast to reference type throws an
exception [except.throw] of a type that would match a handler
[except.handle] of type `std::bad_cast` [bad.cast].

\[*Example 8*:

``` cpp
class A { virtual void f(); };
class B { virtual void g(); };
class D : public virtual A, private B { };
void g() {
  D   d;
  B*  bp = (B*)&d;                  // cast needed to break protection
  A*  ap = &d;                      // public derivation, no cast needed
  D&  dr = dynamic_cast<D&>(*bp);   // fails
  ap = dynamic_cast<A*>(bp);        // fails
  bp = dynamic_cast<B*>(ap);        // fails
  ap = dynamic_cast<A*>(&d);        // succeeds
  bp = dynamic_cast<B*>(&d);        // ill-formed (not a runtime check)
}

class E : public D, public B { };
class F : public E, public D { };
void h() {
  F   f;
  A*  ap  = &f;                     // succeeds: finds unique A
  D*  dp  = dynamic_cast<D*>(ap);   // fails: yields null; f has two D subobjects
  E*  ep  = (E*)ap;                 // error: cast from virtual base
  E*  ep1 = dynamic_cast<E*>(ap);   // succeeds
}
```

— *end example*\]

\[*Note 22*: Subclause [class.cdtor] describes the behavior of a
`dynamic_cast` applied to an object under construction or
destruction. — *end note*\]

#### Type identification <a id="expr.typeid">[expr.typeid]</a>

The result of a `typeid` expression is an lvalue of static type `const`
`std::type_info` [type.info] and dynamic type `const` `std::type_info`
or `const` *name* where *name* is an *implementation-defined* class
publicly derived from `std::type_info` which preserves the behavior
described in  [type.info].

The lifetime of the object referred to by the lvalue extends to the end
of the program. Whether or not the destructor is called for the
`std::type_info` object at the end of the program is unspecified.

If the type of the *expression* or *type-id* operand is a (possibly
cv-qualified) class type or a reference to (possibly cv-qualified) class
type, that class shall be completely defined.

When `typeid` is applied to a glvalue whose type is a polymorphic class
type [class.virtual], the result refers to a `std::type_info` object
representing the type of the most derived object [intro.object] (that
is, the dynamic type) to which the glvalue refers. If the glvalue is
obtained by applying the unary `*` operator to a pointer

and the pointer is a null pointer value [basic.compound], the `typeid`
expression throws an exception [except.throw] of a type that would match
a handler of type `std::bad_typeid` exception [bad.typeid].

When `typeid` is applied to an expression other than a glvalue of a
polymorphic class type, the result refers to a `std::type_info` object
representing the static type of the expression. Lvalue-to-rvalue
[conv.lval], array-to-pointer [conv.array], and function-to-pointer
[conv.func] conversions are not applied to the expression. If the
expression is a prvalue, the temporary materialization conversion
[conv.rval] is applied. The expression is an unevaluated operand
[term.unevaluated.operand].

When `typeid` is applied to a *type-id*, the result refers to a
`std::type_info` object representing the type of the *type-id*. If the
type of the *type-id* is a reference to a possibly cv-qualified type,
the result of the `typeid` expression refers to a `std::type_info`
object representing the cv-unqualified referenced type.

\[*Note 23*: The *type-id* cannot denote a function type with a
*cv-qualifier-seq* or a *ref-qualifier* [dcl.fct]. — *end note*\]

If the type of the expression or *type-id* is a cv-qualified type, the
result of the `typeid` expression refers to a `std::type_info` object
representing the cv-unqualified type.

\[*Example 9*:

``` cpp
class D { ... };
D d1;
const D d2;

typeid(d1) == typeid(d2);       // yields true
typeid(D)  == typeid(const D);  // yields true
typeid(D)  == typeid(d2);       // yields true
typeid(D)  == typeid(const D&); // yields true
```

— *end example*\]

The type `std::type_info` [type.info] is not predefined; if a standard
library declaration [typeinfo.syn,std.modules] of `std::type_info` does
not precede [basic.lookup.general] a `typeid` expression, the program is
ill-formed.

\[*Note 24*: Subclause [class.cdtor] describes the behavior of `typeid`
applied to an object under construction or destruction. — *end note*\]

#### Static cast <a id="expr.static.cast">[expr.static.cast]</a>

The result of the expression `static_cast<T>(v)` is the result of
converting the expression `v` to type `T`. If `T` is an lvalue reference
type or an rvalue reference to function type, the result is an lvalue;
if `T` is an rvalue reference to object type, the result is an xvalue;
otherwise, the result is a prvalue. The `static_cast` operator shall not
cast away constness [expr.const.cast].

An lvalue of type “ `B`”, where `B` is a class type, can be cast to type
“reference to `D`”, where `D` is a class derived [class.derived] from
`B`, if is the same cv-qualification as, or greater cv-qualification
than, . If `B` is a virtual base class of `D` or a base class of a
virtual base class of `D`, or if no valid standard conversion from
“pointer to `D`” to “pointer to `B`” exists [conv.ptr], the program is
ill-formed. An xvalue of type “ `B`” can be cast to type “rvalue
reference to `D`” with the same constraints as for an lvalue of type “
`B`”. If the object of type “ `B`” is actually a base class subobject of
an object of type `D`, the result refers to the enclosing object of type
`D`. Otherwise, the behavior is undefined.

\[*Example 10*:

``` cpp
struct B { };
struct D : public B { };
D d;
B &br = d;

static_cast<D&>(br);            // produces lvalue denoting the original d object
```

— *end example*\]

An lvalue of type `T1` can be cast to type “rvalue reference to `T2`” if
`T2` is reference-compatible with `T1` [dcl.init.ref]. If the value is
not a bit-field, the result refers to the object or the specified base
class subobject thereof; otherwise, the lvalue-to-rvalue conversion
[conv.lval] is applied to the bit-field and the resulting prvalue is
used as the operand of the `static_cast` for the remainder of this
subclause. If `T2` is an inaccessible [class.access] or ambiguous
[class.member.lookup] base class of `T1`, a program that necessitates
such a cast is ill-formed.

An expression E can be explicitly converted to a type `T` if there is an
implicit conversion sequence [over.best.ics] from E to `T`, if overload
resolution for a direct-initialization [dcl.init] of an object or
reference of type `T` from E would find at least one viable function
[over.match.viable], or if `T` is an aggregate type [dcl.init.aggr]
having a first element `x` and there is an implicit conversion sequence
from E to the type of `x`. If `T` is a reference type, the effect is the
same as performing the declaration and initialization

``` cpp
T t($E$);
```

for some invented temporary variable `t` [dcl.init] and then using the
temporary variable as the result of the conversion. Otherwise, the
result object is direct-initialized from E.

\[*Note 25*: The conversion is ill-formed when attempting to convert an
expression of class type to an inaccessible or ambiguous base
class. — *end note*\]

\[*Note 26*: If `T` is “array of unknown bound of `U`”, this
direct-initialization defines the type of the expression as
`U[1]`. — *end note*\]

Otherwise, the `static_cast` shall perform one of the conversions listed
below. No other conversion shall be performed explicitly using a
`static_cast`.

Any expression can be explicitly converted to type cv `void`, in which
case the operand is a discarded-value expression [expr.prop].

\[*Note 27*: Such a `static_cast` has no result as it is a prvalue of
type `void`; see  [basic.lval]. — *end note*\]

\[*Note 28*: However, if the value is in a temporary object
[class.temporary], the destructor for that object is not executed until
the usual time, and the value of the object is preserved for the purpose
of executing the destructor. — *end note*\]

The inverse of any standard conversion sequence [conv] not containing an
lvalue-to-rvalue [conv.lval], array-to-pointer [conv.array],
function-to-pointer [conv.func], null pointer [conv.ptr], null member
pointer [conv.mem], boolean [conv.bool], or function pointer
[conv.fctptr] conversion, can be performed explicitly using
`static_cast`. A program is ill-formed if it uses `static_cast` to
perform the inverse of an ill-formed standard conversion sequence.

\[*Example 11*:

``` cpp
struct B { };
struct D : private B { };
void f() {
  static_cast<D*>((B*)0);               // error: B is a private base of D
  static_cast<int B::*>((int D::*)0);   // error: B is a private base of D
}
```

— *end example*\]

The lvalue-to-rvalue [conv.lval], array-to-pointer [conv.array], and
function-to-pointer [conv.func] conversions are applied to the operand.
Such a `static_cast` is subject to the restriction that the explicit
conversion does not cast away constness [expr.const.cast], and the
following additional rules for specific cases:

A value of a scoped enumeration type [dcl.enum] can be explicitly
converted to an integral type; the result is the same as that of
converting to the enumeration’s underlying type and then to the
destination type. A value of a scoped enumeration type can also be
explicitly converted to a floating-point type; the result is the same as
that of converting from the original value to the floating-point type.

A value of integral or enumeration type can be explicitly converted to a
complete enumeration type. If the enumeration type has a fixed
underlying type, the value is first converted to that type by integral
promotion [conv.prom] or integral conversion [conv.integral], if
necessary, and then to the enumeration type. If the enumeration type
does not have a fixed underlying type, the value is unchanged if the
original value is within the range of the enumeration values [dcl.enum],
and otherwise, the behavior is undefined. A value of floating-point type
can also be explicitly converted to an enumeration type. The resulting
value is the same as converting the original value to the underlying
type of the enumeration [conv.fpint], and subsequently to the
enumeration type.

A prvalue of floating-point type can be explicitly converted to any
other floating-point type. If the source value can be exactly
represented in the destination type, the result of the conversion has
that exact representation. If the source value is between two adjacent
destination values, the result of the conversion is an
*implementation-defined* choice of either of those values. Otherwise,
the behavior is undefined.

A prvalue of type “pointer to `B`”, where `B` is a class type, can be
converted to a prvalue of type “pointer to `D`”, where `D` is a complete
class derived [class.derived] from `B`, if is the same cv-qualification
as, or greater cv-qualification than, . If `B` is a virtual base class
of `D` or a base class of a virtual base class of `D`, or if no valid
standard conversion from “pointer to `D`” to “pointer to `B`” exists
[conv.ptr], the program is ill-formed. The null pointer value
[basic.compound] is converted to the null pointer value of the
destination type. If the prvalue of type “pointer to `B`” points to a
`B` that is actually a base class subobject of an object of type `D`,
the resulting pointer points to the enclosing object of type `D`.
Otherwise, the behavior is undefined.

A prvalue of type “pointer to member of `D` of type `T`” can be
converted to a prvalue of type “pointer to member of `B` of type `T`”,
where `D` is a complete class type and `B` is a base class
[class.derived] of `D`, if is the same cv-qualification as, or greater
cv-qualification than, .

\[*Note 29*: Function types (including those used in
pointer-to-member-function types) are never cv-qualified
[dcl.fct]. — *end note*\]

If no valid standard conversion from “pointer to member of `B` of type
`T`” to “pointer to member of `D` of type `T`” exists [conv.mem], the
program is ill-formed. The null member pointer value [conv.mem] is
converted to the null member pointer value of the destination type. If
class `B` contains the original member, or is a base or derived class of
the class containing the original member, the resulting pointer to
member points to the original member. Otherwise, the behavior is
undefined.

\[*Note 30*: Although class `B` need not contain the original member,
the dynamic type of the object with which indirection through the
pointer to member is performed must contain the original member; see 
[expr.mptr.oper]. — *end note*\]

A prvalue of type “pointer to `void`” can be converted to a prvalue of
type “pointer to `T`”, where `T` is an object type and is the same
cv-qualification as, or greater cv-qualification than, . If the original
pointer value represents the address `A` of a byte in memory and `A`
does not satisfy the alignment requirement of `T`, then the resulting
pointer value is unspecified. Otherwise, if the original pointer value
points to an object *a*, and there is an object *b* of type similar to
`T` that is pointer-interconvertible [basic.compound] with *a*, the
result is a pointer to *b*. Otherwise, the pointer value is unchanged by
the conversion.

\[*Example 12*:

``` cpp
T* p1 = new T;
const T* p2 = static_cast<const T*>(static_cast<void*>(p1));
bool b = p1 == p2;  // b will have the value true.
```

— *end example*\]

#### Reinterpret cast <a id="expr.reinterpret.cast">[expr.reinterpret.cast]</a>

The result of the expression `reinterpret_cast<T>(v)` is the result of
converting the expression `v` to type `T`. If `T` is an lvalue reference
type or an rvalue reference to function type, the result is an lvalue;
if `T` is an rvalue reference to object type, the result is an xvalue;
otherwise, the result is a prvalue and the lvalue-to-rvalue [conv.lval],
array-to-pointer [conv.array], and function-to-pointer [conv.func]
standard conversions are performed on the expression `v`. Conversions
that can be performed explicitly using `reinterpret_cast` are listed
below. No other conversion can be performed explicitly using
`reinterpret_cast`.

The `reinterpret_cast` operator shall not cast away constness
[expr.const.cast]. An expression of integral, enumeration, pointer, or
pointer-to-member type can be explicitly converted to its own type; such
a cast yields the value of its operand.

\[*Note 31*: The mapping performed by `reinterpret_cast` might, or might
not, produce a representation different from the original
value. — *end note*\]

A pointer can be explicitly converted to any integral type large enough
to hold all values of its type. The mapping function is
*implementation-defined*.

\[*Note 32*: It is intended to be unsurprising to those who know the
addressing structure of the underlying machine. — *end note*\]

A value of type `std::nullptr_t` can be converted to an integral type;
the conversion has the same meaning and validity as a conversion of
`(void*)0` to the integral type.

\[*Note 33*: A `reinterpret_cast` cannot be used to convert a value of
any type to the type `std::nullptr_t`. — *end note*\]

A value of integral type or enumeration type can be explicitly converted
to a pointer. A pointer converted to an integer of sufficient size (if
any such exists on the implementation) and back to the same pointer type
will have its original value; mappings between pointers and integers are
otherwise *implementation-defined*.

A function pointer can be explicitly converted to a function pointer of
a different type.

\[*Note 34*: The effect of calling a function through a pointer to a
function type [dcl.fct] that is not the same as the type used in the
definition of the function is undefined [expr.call]. — *end note*\]

Except that converting a prvalue of type “pointer to `T1`” to the type
“pointer to `T2`” (where `T1` and `T2` are function types) and back to
its original type yields the original pointer value, the result of such
a pointer conversion is unspecified.

\[*Note 35*: See also  [conv.ptr] for more details of pointer
conversions. — *end note*\]

An object pointer can be explicitly converted to an object pointer of a
different type.

When a prvalue `v` of object pointer type is converted to the object
pointer type “pointer to cv `T`”, the result is
`static_cast<\cv{} T*>(static_cast<\cv{}~void*>(v))`.

\[*Note 36*: Converting a pointer of type “pointer to `T1`” that points
to an object of type `T1` to the type “pointer to `T2`” (where `T2` is
an object type and the alignment requirements of `T2` are no stricter
than those of `T1`) and back to its original type yields the original
pointer value. — *end note*\]

Converting a function pointer to an object pointer type or vice versa is
conditionally-supported. The meaning of such a conversion is
*implementation-defined*, except that if an implementation supports
conversions in both directions, converting a prvalue of one type to the
other type and back, possibly with different cv-qualification, shall
yield the original pointer value.

The null pointer value [basic.compound] is converted to the null pointer
value of the destination type.

\[*Note 37*: A null pointer constant of type `std::nullptr_t` cannot be
converted to a pointer type, and a null pointer constant of integral
type is not necessarily converted to a null pointer
value. — *end note*\]

A prvalue of type “pointer to member of `X` of type `T1`” can be
explicitly converted to a prvalue of a different type “pointer to member
of `Y` of type `T2`” if `T1` and `T2` are both function types or both
object types.

The null member pointer value [conv.mem] is converted to the null member
pointer value of the destination type. The result of this conversion is
unspecified, except in the following cases:

- Converting a prvalue of type “pointer to member function” to a
  different pointer-to-member-function type and back to its original
  type yields the original pointer-to-member value.

- Converting a prvalue of type “pointer to data member of `X` of type
  `T1`” to the type “pointer to data member of `Y` of type `T2`” (where
  the alignment requirements of `T2` are no stricter than those of `T1`)
  and back to its original type yields the original pointer-to-member
  value.

A glvalue of type `T1`, designating an object *x*, can be cast to the
type “reference to `T2`” if an expression of type “pointer to `T1`” can
be explicitly converted to the type “pointer to `T2`” using a
`reinterpret_cast`. The result is that of `*reinterpret_cast<T2 *>(p)`
where `p` is a pointer to *x* of type “pointer to `T1`”. No temporary is
created, no copy is made, and no constructors [class.ctor] or conversion
functions [class.conv] are called.

#### Const cast <a id="expr.const.cast">[expr.const.cast]</a>

The result of the expression `const_cast<T>(v)` is of type `T`. If `T`
is an lvalue reference to object type, the result is an lvalue; if `T`
is an rvalue reference to object type, the result is an xvalue;
otherwise, the result is a prvalue and the lvalue-to-rvalue [conv.lval],
array-to-pointer [conv.array], and function-to-pointer [conv.func]
standard conversions are performed on the expression `v`. Conversions
that can be performed explicitly using `const_cast` are listed below. No
other conversion shall be performed explicitly using `const_cast`.

\[*Note 38*: Subject to the restrictions in this subclause, an
expression can be cast to its own type using a `const_cast`
operator. — *end note*\]

For two similar types `T1` and `T2` [conv.qual], a prvalue of type `T1`
may be explicitly converted to the type `T2` using a `const_cast` if,
considering the qualification-decompositions of both types, each P¹_i is
the same as P²_i for all i. The result of a `const_cast` refers to the
original entity.

\[*Example 13*:

``` cpp
typedef int *A[3];                  // array of 3 pointer to int
typedef const int *const CA[3];     // array of 3 const pointer to const int

CA &&r = A{};                       // OK, reference binds to temporary array object
                                    // after qualification conversion to type CA
A &&r1 = const_cast<A>(CA{});       // error: temporary array decayed to pointer
A &&r2 = const_cast<A&&>(CA{});     // OK
```

— *end example*\]

For two object types `T1` and `T2`, if a pointer to `T1` can be
explicitly converted to the type “pointer to `T2`” using a `const_cast`,
then the following conversions can also be made:

- an lvalue of type `T1` can be explicitly converted to an lvalue of
  type `T2` using the cast `const_cast<T2&>`;

- a glvalue of type `T1` can be explicitly converted to an xvalue of
  type `T2` using the cast `const_cast<T2&&>`; and

- if `T1` is a class type, a prvalue of type `T1` can be explicitly
  converted to an xvalue of type `T2` using the cast `const_cast<T2&&>`.

The result of a reference `const_cast` refers to the original object if
the operand is a glvalue and to the result of applying the temporary
materialization conversion [conv.rval] otherwise.

A null pointer value [basic.compound] is converted to the null pointer
value of the destination type. The null member pointer value [conv.mem]
is converted to the null member pointer value of the destination type.

\[*Note 39*:

Depending on the type of the object, a write operation through the
pointer, lvalue or pointer to data member resulting from a `const_cast`
that casts away a const-qualifier

can produce undefined behavior [dcl.type.cv].

— *end note*\]

A conversion from a type `T1` to a type `T2` *casts away constness* if
`T1` and `T2` are different, there is a qualification-decomposition
[conv.qual] of `T1` yielding *n* such that `T2` has a
qualification-decomposition of the form

and there is no qualification conversion that converts `T1` to

Casting from an lvalue of type `T1` to an lvalue of type `T2` using an
lvalue reference cast or casting from an expression of type `T1` to an
xvalue of type `T2` using an rvalue reference cast casts away constness
if a cast from a prvalue of type “pointer to `T1`” to the type “pointer
to `T2`” casts away constness.

\[*Note 40*: Some conversions which involve only changes in
cv-qualification cannot be done using `const_cast`. For instance,
conversions between pointers to functions are not covered because such
conversions lead to values whose use causes undefined behavior. For the
same reasons, conversions between pointers to member functions, and in
particular, the conversion from a pointer to a const member function to
a pointer to a non-const member function, are not
covered. — *end note*\]

### Unary expressions <a id="expr.unary">[expr.unary]</a>

#### General <a id="expr.unary.general">[expr.unary.general]</a>

Expressions with unary operators group right-to-left.

``` bnf
%% Ed. note: character protrusion would misalign operators.

unary-expression:
    postfix-expression
    unary-operator cast-expression
    '++' cast-expression
    '--' cast-expression
    await-expression
    \texttt{sizeof} unary-expression
    \texttt{sizeof} '(' type-id ')'
    \texttt{sizeof} '...' '(' identifier ')'
    \texttt{alignof} '(' type-id ')'
    noexcept-expression
    new-expression
    delete-expression
```

``` bnf
%% Ed. note: character protrusion would misalign operators.

unary-operator: one of
    '*  &  +  -  !  \~'
```

#### Unary operators <a id="expr.unary.op">[expr.unary.op]</a>

The unary `*` operator performs *indirection*. Its operand shall be a
prvalue of type “pointer to `T`”, where `T` is an object or function
type. The operator yields an lvalue of type `T` denoting the object or
function to which the operand points.

\[*Note 41*:  Indirection through a pointer to an incomplete type (other
than cv `void`) is valid. The lvalue thus obtained can be used in
limited ways (to initialize a reference, for example); this lvalue must
not be converted to a prvalue, see  [conv.lval]. — *end note*\]

Each of the following unary operators yields a prvalue.

The operand of the unary `&` operator shall be an lvalue of some type
`T`. The result is a prvalue.

- If the operand is a *qualified-id* naming a non-static or variant
  member `m` of some class `C`, other than an explicit object member
  function, the result has type “pointer to member of class `C` of type
  `T`” and designates `C::m`.

- Otherwise, the result has type “pointer to `T`” and points to the
  designated object [intro.memory] or function [basic.compound]. If the
  operand names an explicit object member function [dcl.fct], the
  operand shall be a *qualified-id*.

  \[*Note 6*: In particular, taking the address of a variable of type
  “cv `T`” yields a pointer of type “pointer to cv `T`”. — *end note*\]

\[*Example 14*:

``` cpp
struct A { int i; };
struct B : A { };
... &B::i ...       // has type int A::*
int a;
int* p1 = &a;
int* p2 = p1 + 1;   // defined behavior
bool b = p2 > p1;   // defined behavior, with value true
```

— *end example*\]

\[*Note 42*: A pointer to member formed from a `mutable` non-static data
member [dcl.stc] does not reflect the `mutable` specifier associated
with the non-static data member. — *end note*\]

A pointer to member is only formed when an explicit `&` is used and its
operand is a *qualified-id* not enclosed in parentheses.

\[*Note 43*: That is, the expression `&(qualified-id)`, where the
*qualified-id* is enclosed in parentheses, does not form an expression
of type “pointer to member”. Neither does `qualified-id`, because there
is no implicit conversion from a *qualified-id* for a non-static member
function to the type “pointer to member function” as there is from an
lvalue of function type to the type “pointer to function” [conv.func].
Nor is `&unqualified-id` a pointer to member, even within the scope of
the *unqualified-id*’s class. — *end note*\]

If `&` is applied to an lvalue of incomplete class type and the complete
type declares `operator&()`, it is unspecified whether the operator has
the built-in meaning or the operator function is called. The operand of
`&` shall not be a bit-field.

\[*Note 44*: The address of an overload set [over] can be taken only in
a context that uniquely determines which function is referred to (see 
[over.over]). Since the context can affect whether the operand is a
static or non-static member function, the context can also affect
whether the expression has type “pointer to function” or “pointer to
member function”. — *end note*\]

The operand of the unary `+` operator shall have arithmetic, unscoped
enumeration, or pointer type and the result is the value of the
argument. Integral promotion is performed on integral or enumeration
operands. The type of the result is the type of the promoted operand.

The operand of the unary `-` operator shall have arithmetic or unscoped
enumeration type and the result is the negative of its operand. Integral
promotion is performed on integral or enumeration operands. The negative
of an unsigned quantity is computed by subtracting its value from 2ⁿ,
where n is the number of bits in the promoted operand. The type of the
result is the type of the promoted operand.

\[*Note 45*: The result is the two’s complement of the operand (where
operand and result are considered as unsigned). — *end note*\]

The operand of the logical negation operator `!` is contextually
converted to `bool` [conv]; its value is `true` if the converted operand
is `false` and `false` otherwise. The type of the result is `bool`.

The operand of the `~{}` operator shall have integral or unscoped
enumeration type. Integral promotions are performed. The type of the
result is the type of the promoted operand. Given the coefficients
$\tcode{x}_i$ of the base-2 representation [basic.fundamental] of the
promoted operand `x`, the coefficient $\tcode{r}_i$ of the base-2
representation of the result `r` is 1 if $\tcode{x}_i$ is 0, and 0
otherwise.

\[*Note 46*: The result is the ones’ complement of the operand (where
operand and result are considered as unsigned). — *end note*\]

There is an ambiguity in the grammar when `~{}` is followed by a
*type-name* or *decltype-specifier*. The ambiguity is resolved by
treating `~{}` as the operator rather than as the start of an
*unqualified-id* naming a destructor.

\[*Note 47*: Because the grammar does not permit an operator to follow
the `.`, `->`, or `::` tokens, a `~{}` followed by a *type-name* or
*decltype-specifier* in a member access expression or *qualified-id* is
unambiguously parsed as a destructor name. — *end note*\]

#### Increment and decrement <a id="expr.pre.incr">[expr.pre.incr]</a>

The operand of prefix `++` is modified [defns.access] by adding `1`. The
operand shall be a modifiable lvalue. The type of the operand shall be
an arithmetic type other than cv `bool`, or a pointer to a
completely-defined object type. An operand with volatile-qualified type
is deprecated; see  [depr.volatile.type]. The result is the updated
operand; it is an lvalue, and it is a bit-field if the operand is a
bit-field. The expression `++x` is equivalent to `x+=1`.

\[*Note 48*: See the discussions of addition [expr.add] and assignment
operators [expr.ass] for information on conversions. — *end note*\]

The operand of prefix `--` is modified [defns.access] by subtracting
`1`. The requirements on the operand of prefix `--` and the properties
of its result are otherwise the same as those of prefix `++`.

\[*Note 49*: For postfix increment and decrement, see 
[expr.post.incr]. — *end note*\]

#### Await <a id="expr.await">[expr.await]</a>

The `co_await` expression is used to suspend evaluation of a coroutine
[dcl.fct.def.coroutine] while awaiting completion of the computation
represented by the operand expression.

``` bnf
await-expression:
    'co_await' cast-expression
```

An *await-expression* shall appear only in a potentially-evaluated
expression within the *compound-statement* of a *function-body* outside
of a *handler* [except.pre]. In a *declaration-statement* or in the
*simple-declaration* (if any) of an *init-statement*, an
*await-expression* shall appear only in an *initializer* of that
*declaration-statement* or *simple-declaration*. An *await-expression*
shall not appear in a default argument [dcl.fct.default]. An
*await-expression* shall not appear in the initializer of a block
variable with static or thread storage duration. A context within a
function where an *await-expression* can appear is called a
*suspension context* of the function.

Evaluation of an *await-expression* involves the following auxiliary
types, expressions, and objects:

- *p* is an lvalue naming the promise object [dcl.fct.def.coroutine] of
  the enclosing coroutine and `P` is the type of that object.

- Unless the *await-expression* was implicitly produced by a
  *yield-expression* [expr.yield], an initial await expression, or a
  final await expression [dcl.fct.def.coroutine], a search is performed
  for the name `await_transform` in the scope of `P`
  [class.member.lookup]. If this search is performed and finds at least
  one declaration, then *a* is
  `.await_transform(}cast-expression\tcode{)}`; otherwise, *a* is the
  *cast-expression*.

- *o* is determined by enumerating the applicable `operator co_await`
  functions for an argument *a* [over.match.oper], and choosing the best
  one through overload resolution [over.match]. If overload resolution
  is ambiguous, the program is ill-formed. If no viable functions are
  found, *o* is *a*. Otherwise, *o* is a call to the selected function
  with the argument *a*. If *o* would be a prvalue, the temporary
  materialization conversion [conv.rval] is applied.

- *e* is an lvalue referring to the result of evaluating the
  (possibly-converted) *o*.

- *h* is an object of type `std::coroutine_handle<P>` referring to the
  enclosing coroutine.

- *await-ready* is the expression *e*`.await_ready()`, contextually
  converted to `bool`.

- *await-suspend* is the expression *e*`.await_suspend(`*h*`)`, which
  shall be a prvalue of type `void`, `bool`, or
  `std::coroutine_handle<Z>` for some type `Z`.

- *await-resume* is the expression *e*`.await_resume()`.

The *await-expression* has the same type and value category as the
*await-resume* expression.

The *await-expression* evaluates the (possibly-converted) *o* expression
and the *await-ready* expression, then:

- If the result of *await-ready* is `false`, the coroutine is considered
  suspended. Then:

  - If the type of *await-suspend* is `std::coroutine_handle<Z>`,
    *await-suspend*`.resume()` is evaluated.

    \[*Note 7*: This resumes the coroutine referred to by the result of
    *await-suspend*. Any number of coroutines can be successively
    resumed in this fashion, eventually returning control flow to the
    current coroutine caller or resumer
    [dcl.fct.def.coroutine]. — *end note*\]

  - Otherwise, if the type of *await-suspend* is `bool`, *await-suspend*
    is evaluated, and the coroutine is resumed if the result is `false`.

  - Otherwise, *await-suspend* is evaluated.

  If the evaluation of *await-suspend* exits via an exception, the
  exception is caught, the coroutine is resumed, and the exception is
  immediately rethrown [except.throw]. Otherwise, control flow returns
  to the current coroutine caller or resumer [dcl.fct.def.coroutine]
  without exiting any scopes [stmt.jump]. The point in the coroutine
  immediately prior to control returning to its caller or resumer is a
  coroutine *suspend point*.

- If the result of *await-ready* is `true`, or when the coroutine is
  resumed other than by rethrowing an exception from *await-suspend*,
  the *await-resume* expression is evaluated, and its result is the
  result of the *await-expression*.

\[*Note 50*: With respect to sequencing, an *await-expression* is
indivisible [intro.execution]. — *end note*\]

\[*Example 15*:

``` cpp
template <typename T>
struct my_future {
  ...
  bool await_ready();
  void await_suspend(std::coroutine_handle<>);
  T await_resume();
};

template <class Rep, class Period>
auto operator co_await(std::chrono::duration<Rep, Period> d) {
  struct awaiter {
    std::chrono::system_clock::duration duration;
    ...
    awaiter(std::chrono::system_clock::duration d) : duration(d) {}
    bool await_ready() const { return duration.count() <= 0; }
    void await_resume() {}
    void await_suspend(std::coroutine_handle<> h) { ... }
  };
  return awaiter{d};
}

using namespace std::chrono;

my_future<int> h();

my_future<void> g() {
  std::cout << "just about to go to sleep...\n";
  co_await 10ms;
  std::cout << "resumed\n";
  co_await h();
}

auto f(int x = co_await h());   // error: await-expression outside of function suspension context
int a[] = { co_await h() };     // error: await-expression outside of function suspension context
```

— *end example*\]

#### Sizeof <a id="expr.sizeof">[expr.sizeof]</a>

The `sizeof` operator yields the number of bytes occupied by a
non-potentially-overlapping object of the type of its operand. The
operand is either an expression, which is an unevaluated operand
[term.unevaluated.operand], or a parenthesized *type-id*. The `sizeof`
operator shall not be applied to an expression that has function or
incomplete type, to the parenthesized name of such types, or to a
glvalue that designates a bit-field. The result of `sizeof` applied to
any of the narrow character types is `1`. The result of `sizeof` applied
to any other fundamental type [basic.fundamental] is
*implementation-defined*.

\[*Note 51*:

In particular, the values of `sizeof(bool)`, `sizeof(char16_t)`,
`sizeof(char32_t)`, and `sizeof(wchar_t)` are implementation-defined.

— *end note*\]

\[*Note 52*: See  [intro.memory] for the definition of byte and 
[term.object.representation] for the definition of object
representation. — *end note*\]

When applied to a reference type, the result is the size of the
referenced type. When applied to a class, the result is the number of
bytes in an object of that class including any padding required for
placing objects of that type in an array. The result of applying
`sizeof` to a potentially-overlapping subobject is the size of the type,
not the size of the subobject.

When applied to an array, the result is the total number of bytes in the
array. This implies that the size of an array of n elements is n times
the size of an element.

The lvalue-to-rvalue [conv.lval], array-to-pointer [conv.array], and
function-to-pointer [conv.func] standard conversions are not applied to
the operand of `sizeof`. If the operand is a prvalue, the temporary
materialization conversion [conv.rval] is applied.

The identifier in a `sizeof...` expression shall name a pack. The
`sizeof...` operator yields the number of elements in the pack
[temp.variadic]. A `sizeof...` expression is a pack expansion
[temp.variadic].

\[*Example 16*:

``` cpp
template<class... Types>
struct count {
  static const std::size_t value = sizeof...(Types);
};
```

— *end example*\]

The result of `sizeof` and `sizeof...` is a prvalue of type
`std::size_t`.

\[*Note 53*: A `sizeof` expression is an integral constant expression
[expr.const]. The type `std::size_t` is defined in the standard header
`<cstddef>` [cstddef.syn,support.types.layout]. — *end note*\]

#### Alignof <a id="expr.alignof">[expr.alignof]</a>

An `alignof` expression yields the alignment requirement of its operand
type. The operand shall be a *type-id* representing a complete object
type, or an array thereof, or a reference to one of those types.

The result is a prvalue of type `std::size_t`.

\[*Note 54*: An `alignof` expression is an integral constant expression
[expr.const]. The type `std::size_t` is defined in the standard header
`<cstddef>` [cstddef.syn,support.types.layout]. — *end note*\]

When `alignof` is applied to a reference type, the result is the
alignment of the referenced type. When `alignof` is applied to an array
type, the result is the alignment of the element type.

#### `noexcept` operator <a id="expr.unary.noexcept">[expr.unary.noexcept]</a>

The `noexcept` operator determines whether the evaluation of its
operand, which is an unevaluated operand [term.unevaluated.operand], can
throw an exception [except.throw].

``` bnf
noexcept-expression:
  \texttt{noexcept} '(' expression ')'
```

The result of the `noexcept` operator is a prvalue of type `bool`.

\[*Note 55*: A *noexcept-expression* is an integral constant expression
[expr.const]. — *end note*\]

The result of the `noexcept` operator is `true` unless the *expression*
is potentially-throwing [except.spec].

#### New <a id="expr.new">[expr.new]</a>

The *new-expression* attempts to create an object of the *type-id*
[dcl.name] or *new-type-id* to which it is applied. The type of that
object is the *allocated type*. This type shall be a complete object
type [term.incomplete.type], but not an abstract class type
[class.abstract] or array thereof [intro.object].

\[*Note 56*: Because references are not objects, references cannot be
created by *new-expression*. — *end note*\]

\[*Note 57*: The *type-id* can be a cv-qualified type, in which case the
object created by the *new-expression* has a cv-qualified
type. — *end note*\]

``` bnf
new-expression:
    ['::'] \texttt{new} [new-placement] new-type-id [new-initializer] 
    ['::'] \texttt{new} [new-placement] '(' type-id ')' [new-initializer]
```

``` bnf
new-placement:
    '(' expression-list ')'
```

``` bnf
new-type-id:
    type-specifier-seq [new-declarator]
```

``` bnf
new-declarator:
    ptr-operator [new-declarator] 
    noptr-new-declarator
```

``` bnf
noptr-new-declarator:
    '[' [expression] ']' [attribute-specifier-seq]
    noptr-new-declarator '[' constant-expression ']' [attribute-specifier-seq]
```

``` bnf
new-initializer:
    '(' [expression-list] ')'
    braced-init-list
```

If a placeholder type [dcl.spec.auto] appears in the
*type-specifier-seq* of a *new-type-id* or *type-id* of a
*new-expression*, the allocated type is deduced as follows: Let *init*
be the *new-initializer*, if any, and `T` be the *new-type-id* or
*type-id* of the *new-expression*, then the allocated type is the type
deduced for the variable `x` in the invented declaration
[dcl.spec.auto]:

``` cpp
T x init ;
```

\[*Example 17*:

``` cpp
new auto(1);                    // allocated type is int
auto x = new auto('a');         // allocated type is char, x is of type char*

template<class T> struct A { A(T, T); };
auto y = new A{1, 2};           // allocated type is A<int>
```

— *end example*\]

The *new-type-id* in a *new-expression* is the longest possible sequence
of *new-declarator*.

\[*Note 58*: This prevents ambiguities between the declarator operators
`&`, `&&`, `*`, and `[]` and their expression
counterparts. — *end note*\]

\[*Example 18*:

``` cpp
new int * i;                    // syntax error: parsed as (new int*) i, not as (new int)*i
```

The `*` is the pointer declarator and not the multiplication operator.

— *end example*\]

\[*Note 59*:

Parentheses in a *new-type-id* of a *new-expression* can have surprising
effects.

— *end note*\]

The *attribute-specifier-seq* in a *noptr-new-declarator* appertains to
the associated array type.

Every *constant-expression* in a *noptr-new-declarator* shall be a
converted constant expression [expr.const] of type `std::size_t` and its
value shall be greater than zero.

\[*Example 19*: Given the definition `int n = 42`, `new float[n][5]` is
well-formed (because `n` is the *expression* of a
*noptr-new-declarator*), but `new float[5][n]` is ill-formed (because
`n` is not a constant expression). — *end example*\]

If the *type-id* or *new-type-id* denotes an array type of unknown bound
[dcl.array], the *new-initializer* shall not be omitted; the allocated
object is an array with `n` elements, where `n` is determined from the
number of initial elements supplied in the *new-initializer*
[dcl.init.aggr,dcl.init.string].

If the *expression* in a *noptr-new-declarator* is present, it is
implicitly converted to `std::size_t`. The *expression* is erroneous if:

- the expression is of non-class type and its value before converting to
  `std::size_t` is less than zero;

- the expression is of class type and its value before application of
  the second standard conversion [over.ics.user]

  is less than zero;

- its value is such that the size of the allocated object would exceed
  the *implementation-defined* limit [implimits]; or

- the *new-initializer* is a *braced-init-list* and the number of array
  elements for which initializers are provided (including the
  terminating `'\ 0'` in a *string-literal* [lex.string]) exceeds the
  number of elements to initialize.

If the *expression* is erroneous after converting to `std::size_t`:

- if the *expression* is a potentially-evaluated core constant
  expression, the program is ill-formed;

- otherwise, an allocation function is not called; instead

  - if the allocation function that would have been called has a
    non-throwing exception specification [except.spec], the value of the
    *new-expression* is the null pointer value of the required result
    type;

  - otherwise, the *new-expression* terminates by throwing an exception
    of a type that would match a handler [except.handle] of type
    `std::bad_array_new_length` [new.badlength].

When the value of the *expression* is zero, the allocation function is
called to allocate an array with no elements.

Objects created by a *new-expression* have dynamic storage duration
[basic.stc.dynamic].

\[*Note 60*:  The lifetime of such an object is not necessarily
restricted to the scope in which it is created. — *end note*\]

When the allocated type is “array of `N` `T`” (that is, the
*noptr-new-declarator* syntax is used or the *new-type-id* or *type-id*
denotes an array type), the *new-expression* yields a prvalue of type
“pointer to `T`” that points to the initial element (if any) of the
array. Otherwise, let `T` be the allocated type; the *new-expression* is
a prvalue of type “pointer to T” that points to the object created.

\[*Note 61*: Both `new int` and `new int[10]` have type `int*` and the
type of `new int[i][10]` is `int (*)[10]`. — *end note*\]

A *new-expression* may obtain storage for the object by calling an
allocation function [basic.stc.dynamic.allocation]. If the
*new-expression* terminates by throwing an exception, it may release
storage by calling a deallocation function
[basic.stc.dynamic.deallocation]. If the allocated type is a non-array
type, the allocation function’s name is `operator new` and the
deallocation function’s name is `operator delete`. If the allocated type
is an array type, the allocation function’s name is `operator new[]` and
the deallocation function’s name is `operator delete[]`.

\[*Note 62*: An implementation is required to provide default
definitions for the global allocation functions
[basic.stc.dynamic,new.delete.single,new.delete.array]. A C++ program
can provide alternative definitions of these functions
[replacement.functions] and/or class-specific versions [class.free]. The
set of allocation and deallocation functions that can be called by a
*new-expression* can include functions that do not perform allocation or
deallocation; for example, see [new.delete.placement]. — *end note*\]

If the *new-expression* does not begin with a unary `::` operator and
the allocated type is a class type `T` or array thereof, a search is
performed for the allocation function’s name in the scope of `T`
[class.member.lookup]. Otherwise, or if nothing is found, the allocation
function’s name is looked up by searching for it in the global scope.

An implementation is allowed to omit a call to a replaceable global
allocation function [new.delete.single,new.delete.array]. When it does
so, the storage is instead provided by the implementation or provided by
extending the allocation of another *new-expression*.

During an evaluation of a constant expression, a call to an allocation
function is always omitted.

\[*Note 63*: Only *new-expression* that would otherwise result in a call
to a replaceable global allocation function can be evaluated in constant
expressions [expr.const]. — *end note*\]

The implementation may extend the allocation of a *new-expression* `e1`
to provide storage for a *new-expression* `e2` if the following would be
true were the allocation not extended:

- the evaluation of `e1` is sequenced before the evaluation of `e2`, and

- `e2` is evaluated whenever `e1` obtains storage, and

- both `e1` and `e2` invoke the same replaceable global allocation
  function, and

- if the allocation function invoked by `e1` and `e2` is throwing, any
  exceptions thrown in the evaluation of either `e1` or `e2` would be
  first caught in the same handler, and

- the pointer values produced by `e1` and `e2` are operands to evaluated
  *delete-expression*, and

- the evaluation of `e2` is sequenced before the evaluation of the
  *delete-expression* whose operand is the pointer value produced by
  `e1`.

\[*Example 20*:

``` cpp
void can_merge(int x) {
  // These allocations are safe for merging:
  std::unique_ptr<char[]> a{new (std::nothrow) char[8]};
  std::unique_ptr<char[]> b{new (std::nothrow) char[8]};
  std::unique_ptr<char[]> c{new (std::nothrow) char[x]};

  g(a.get(), b.get(), c.get());
}

void cannot_merge(int x) {
  std::unique_ptr<char[]> a{new char[8]};
  try {
    // Merging this allocation would change its catch handler.
    std::unique_ptr<char[]> b{new char[x]};
  } catch (const std::bad_alloc& e) {
    std::cerr << "Allocation failed: " << e.what() << std::endl;
    throw;
  }
}
```

— *end example*\]

When a *new-expression* calls an allocation function and that allocation
has not been extended, the *new-expression* passes the amount of space
requested to the allocation function as the first argument of type
`std::size_t`. That argument shall be no less than the size of the
object being created; it may be greater than the size of the object
being created only if the object is an array and the allocation function
is not a non-allocating form [new.delete.placement]. For arrays of
`char`, `unsigned char`, and `std::byte`, the difference between the
result of the *new-expression* and the address returned by the
allocation function shall be an integral multiple of the strictest
fundamental alignment requirement [basic.align] of any object type whose
size is no greater than the size of the array being created.

\[*Note 64*:  Because allocation functions are assumed to return
pointers to storage that is appropriately aligned for objects of any
type with fundamental alignment, this constraint on array allocation
overhead permits the common idiom of allocating character arrays into
which objects of other types will later be placed. — *end note*\]

When a *new-expression* calls an allocation function and that allocation
has been extended, the size argument to the allocation call shall be no
greater than the sum of the sizes for the omitted calls as specified
above, plus the size for the extended call had it not been extended,
plus any padding necessary to align the allocated objects within the
allocated memory.

The *new-placement* syntax is used to supply additional arguments to an
allocation function; such an expression is called a *new-expression*.

Overload resolution is performed on a function call created by
assembling an argument list. The first argument is the amount of space
requested, and has type `std::size_t`. If the type of the allocated
object has new-extended alignment, the next argument is the type’s
alignment, and has type `std::align_val_t`. If the *new-placement*
syntax is used, the *initializer-clause* in its *expression-list* are
the succeeding arguments. If no matching function is found then

- if the allocated object type has new-extended alignment, the alignment
  argument is removed from the argument list;

- otherwise, an argument that is the type’s alignment and has type
  `std::align_val_t` is added into the argument list immediately after
  the first argument;

and then overload resolution is performed again.

\[*Example 21*:

- `new T` results in one of the following calls:

  \_\_CODEBLOCK_1\_\_

- `new(2,f) T` results in one of the following calls:

  \_\_CODEBLOCK_2\_\_

- `new T[5]` results in one of the following calls:

  \_\_CODEBLOCK_3\_\_

- `new(2,f) T[5]` results in one of the following calls:

  \_\_CODEBLOCK_4\_\_

Here, each instance of `x` is a non-negative unspecified value
representing array allocation overhead; the result of the
*new-expression* will be offset by this amount from the value returned
by `operator new[]`. This overhead may be applied in all array
*new-expression*, including those referencing a placement allocation
function, except when referencing the library function
`operator new[](std::size_t, void*)`. The amount of overhead may vary
from one invocation of `new` to another.

— *end example*\]

\[*Note 65*: Unless an allocation function has a non-throwing exception
specification [except.spec], it indicates failure to allocate storage by
throwing a `std::bad_alloc` exception
[basic.stc.dynamic.allocation,except,bad.alloc]; it returns a non-null
pointer otherwise. If the allocation function has a non-throwing
exception specification, it returns null to indicate failure to allocate
storage and a non-null pointer otherwise. — *end note*\]

If the allocation function is a non-allocating form
[new.delete.placement] that returns null, the behavior is undefined.
Otherwise, if the allocation function returns null, initialization shall
not be done, the deallocation function shall not be called, and the
value of the *new-expression* shall be null.

\[*Note 66*: When the allocation function returns a value other than
null, it must be a pointer to a block of storage in which space for the
object has been reserved. The block of storage is assumed to be
appropriately aligned and of the requested size. The address of the
created object will not necessarily be the same as that of the block if
the object is an array. — *end note*\]

A *new-expression* that creates an object of type `T` initializes that
object as follows:

- If the *new-initializer* is omitted, the object is default-initialized
  [dcl.init].

  \[*Note 8*: If no initialization is performed, the object has an
  indeterminate value. — *end note*\]

- Otherwise, the *new-initializer* is interpreted according to the
  initialization rules of  [dcl.init] for direct-initialization.

The invocation of the allocation function is sequenced before the
evaluations of expressions in the *new-initializer*. Initialization of
the allocated object is sequenced before the value computation of the
*new-expression*.

If the *new-expression* creates an object or an array of objects of
class type, access and ambiguity control are done for the allocation
function, the deallocation function [basic.stc.dynamic.deallocation],
and the constructor [class.ctor] selected for the initialization (if
any). If the *new-expression* creates an array of objects of class type,
the destructor is potentially invoked [class.dtor].

If any part of the object initialization described above

terminates by throwing an exception and a suitable deallocation function
can be found, the deallocation function is called to free the memory in
which the object was being constructed, after which the exception
continues to propagate in the context of the *new-expression*. If no
unambiguous matching deallocation function can be found, propagating the
exception does not cause the object’s memory to be freed.

\[*Note 67*: This is appropriate when the called allocation function
does not allocate memory; otherwise, it is likely to result in a memory
leak. — *end note*\]

If the *new-expression* does not begin with a unary `::` operator and
the allocated type is a class type `T` or an array thereof, a search is
performed for the deallocation function’s name in the scope of `T`.
Otherwise, or if nothing is found, the deallocation function’s name is
looked up by searching for it in the global scope.

A declaration of a placement deallocation function matches the
declaration of a placement allocation function if it has the same number
of parameters and, after parameter transformations [dcl.fct], all
parameter types except the first are identical. If the lookup finds a
single matching deallocation function, that function will be called;
otherwise, no deallocation function will be called. If the lookup finds
a usual deallocation function and that function, considered as a
placement deallocation function, would have been selected as a match for
the allocation function, the program is ill-formed. For a non-placement
allocation function, the normal deallocation function lookup is used to
find the matching deallocation function [expr.delete].

\[*Example 22*:

``` cpp
struct S {
  // Placement allocation function:
  static void* operator new(std::size_t, std::size_t);

  // Usual (non-placement) deallocation function:
  static void operator delete(void*, std::size_t);
};

S* p = new (0) S;   // error: non-placement deallocation function matches
                    // placement allocation function
```

— *end example*\]

If a *new-expression* calls a deallocation function, it passes the value
returned from the allocation function call as the first argument of type
`void*`. If a placement deallocation function is called, it is passed
the same additional arguments as were passed to the placement allocation
function, that is, the same arguments as those specified with the
*new-placement* syntax. If the implementation is allowed to introduce a
temporary object or make a copy of any argument as part of the call to
the allocation function, it is unspecified whether the same object is
used in the call to both the allocation and deallocation functions.

#### Delete <a id="expr.delete">[expr.delete]</a>

The *delete-expression* operator destroys a most derived object
[intro.object] or array created by a *new-expression*.

``` bnf
delete-expression:
    ['::'] \texttt{delete} cast-expression
    ['::'] \texttt{delete} '[' ']' cast-expression
```

The first alternative is a *single-object delete expression*, and the
second is an *array delete expression*. Whenever the `delete` keyword is
immediately followed by empty square brackets, it shall be interpreted
as the second alternative.

The operand shall be of pointer to object type or of class type. If of
class type, the operand is contextually implicitly converted [conv] to a
pointer to object type.

The *delete-expression* has type `void`.

If the operand has a class type, the operand is converted to a pointer
type by calling the above-mentioned conversion function, and the
converted operand is used in place of the original operand for the
remainder of this subclause. In a single-object delete expression, the
value of the operand of `delete` may be a null pointer value, a pointer
value that resulted from a previous non-array *new-expression*, or a
pointer to a base class subobject of an object created by such a
*new-expression*. If not, the behavior is undefined. In an array delete
expression, the value of the operand of `delete` may be a null pointer
value or a pointer value that resulted from a previous array
*new-expression* whose allocation function was not a non-allocating form
[new.delete.placement].

If not, the behavior is undefined.

\[*Note 68*: This means that the syntax of the *delete-expression* must
match the type of the object allocated by `new`, not the syntax of the
*new-expression*. — *end note*\]

\[*Note 69*: A pointer to a `const` type can be the operand of a
*delete-expression*; it is not necessary to cast away the constness
[expr.const.cast] of the pointer expression before it is used as the
operand of the *delete-expression*. — *end note*\]

In a single-object delete expression, if the static type of the object
to be deleted is not similar [conv.qual] to its dynamic type and the
selected deallocation function (see below) is not a destroying operator
delete, the static type shall be a base class of the dynamic type of the
object to be deleted and the static type shall have a virtual destructor
or the behavior is undefined. In an array delete expression, if the
dynamic type of the object to be deleted is not similar to its static
type, the behavior is undefined.

The *cast-expression* in a *delete-expression* shall be evaluated
exactly once.

If the object being deleted has incomplete class type at the point of
deletion and the complete class has a non-trivial destructor or a
deallocation function, the behavior is undefined.

If the value of the operand of the *delete-expression* is not a null
pointer value and the selected deallocation function (see below) is not
a destroying operator delete, the *delete-expression* will invoke the
destructor (if any) for the object or the elements of the array being
deleted. In the case of an array, the elements will be destroyed in
order of decreasing address (that is, in reverse order of the completion
of their constructor; see  [class.base.init]).

If the value of the operand of the *delete-expression* is not a null
pointer value, then:

- If the allocation call for the *new-expression* for the object to be
  deleted was not omitted and the allocation was not extended
  [expr.new], the *delete-expression* shall call a deallocation function
  [basic.stc.dynamic.deallocation]. The value returned from the
  allocation call of the *new-expression* shall be passed as the first
  argument to the deallocation function.

- Otherwise, if the allocation was extended or was provided by extending
  the allocation of another *new-expression*, and the
  *delete-expression* for every other pointer value produced by a
  *new-expression* that had storage provided by the extended
  *new-expression* has been evaluated, the *delete-expression* shall
  call a deallocation function. The value returned from the allocation
  call of the extended *new-expression* shall be passed as the first
  argument to the deallocation function.

- Otherwise, the *delete-expression* will not call a deallocation
  function.

\[*Note 70*: The deallocation function is called regardless of whether
the destructor for the object or some element of the array throws an
exception. — *end note*\]

If the value of the operand of the *delete-expression* is a null pointer
value, it is unspecified whether a deallocation function will be called
as described above.

If a deallocation function is called, it is `operator delete` for a
single-object delete expression or `operator delete[]` for an array
delete expression.

\[*Note 71*:  An implementation provides default definitions of the
global deallocation functions [new.delete.single,new.delete.array]. A
C++ program can provide alternative definitions of these functions
[replacement.functions], and/or class-specific versions
[class.free]. — *end note*\]

If the keyword `delete` in a *delete-expression* is not preceded by the
unary `::` operator and the type of the operand is a pointer to a
(possibly cv-qualified) class type `T` or (possibly multidimensional)
array thereof:

- For a single-object delete expression, if the operand is a pointer to
  cv `T` and `T` has a virtual destructor, the deallocation function is
  the one selected at the point of definition of the dynamic type’s
  virtual destructor [class.dtor].

- Otherwise, a search is performed for the deallocation function’s name
  in the scope of `T`.

Otherwise, or if nothing is found, the deallocation function’s name is
looked up by searching for it in the global scope. In any case, any
declarations other than of usual deallocation functions
[basic.stc.dynamic.deallocation] are discarded.

\[*Note 72*: If only a placement deallocation function is found in a
class, the program is ill-formed because the lookup set is empty
[basic.lookup]. — *end note*\]

If more than one deallocation function is found, the function to be
called is selected as follows:

- If any of the deallocation functions is a destroying operator delete,
  all deallocation functions that are not destroying operator deletes
  are eliminated from further consideration.

- If the type has new-extended alignment, a function with a parameter of
  type `std::align_val_t` is preferred; otherwise a function without
  such a parameter is preferred. If any preferred functions are found,
  all non-preferred functions are eliminated from further consideration.

- If exactly one function remains, that function is selected and the
  selection process terminates.

- If the deallocation functions belong to a class scope, the one without
  a parameter of type `std::size_t` is selected.

- If the type is complete and if, for an array delete expression only,
  the operand is a pointer to a class type with a non-trivial destructor
  or a (possibly multidimensional) array thereof, the function with a
  parameter of type `std::size_t` is selected.

- Otherwise, it is unspecified whether a deallocation function with a
  parameter of type `std::size_t` is selected.

For a single-object delete expression, the deleted object is the object
A pointed to by the operand if the static type of A does not have a
virtual destructor, and the most-derived object of A otherwise.

\[*Note 73*: If the deallocation function is not a destroying operator
delete and the deleted object is not the most derived object in the
former case, the behavior is undefined, as stated above. — *end note*\]

For an array delete expression, the deleted object is the array object.
When a *delete-expression* is executed, the selected deallocation
function shall be called with the address of the deleted object in a
single-object delete expression, or the address of the deleted object
suitably adjusted for the array allocation overhead [expr.new] in an
array delete expression, as its first argument.

\[*Note 74*: Any cv-qualifiers in the type of the deleted object are
ignored when forming this argument. — *end note*\]

If a destroying operator delete is used, an unspecified value is passed
as the argument corresponding to the parameter of type
`std::destroying_delete_t`. If a deallocation function with a parameter
of type `std::align_val_t` is used, the alignment of the type of the
deleted object is passed as the corresponding argument. If a
deallocation function with a parameter of type `std::size_t` is used,
the size of the deleted object in a single-object delete expression, or
of the array plus allocation overhead in an array delete expression, is
passed as the corresponding argument.

\[*Note 75*: If this results in a call to a replaceable deallocation
function, and either the first argument was not the result of a prior
call to a replaceable allocation function or the second or third
argument was not the corresponding argument in said call, the behavior
is undefined [new.delete.single,new.delete.array]. — *end note*\]

Access and ambiguity control are done for both the deallocation function
and the destructor [class.dtor,class.free].

### Explicit type conversion (cast notation) <a id="expr.cast">[expr.cast]</a>

The result of the expression `(T)` *cast-expression* is of type `T`. The
result is an lvalue if `T` is an lvalue reference type or an rvalue
reference to function type and an xvalue if `T` is an rvalue reference
to object type; otherwise the result is a prvalue.

\[*Note 76*: If `T` is a non-class type that is cv-qualified, the
*cv-qualifier* are discarded when determining the type of the resulting
prvalue; see [expr.prop]. — *end note*\]

An explicit type conversion can be expressed using functional notation
[expr.type.conv], a type conversion operator (`dynamic_cast`,
`static_cast`, `reinterpret_cast`, `const_cast`), or the *cast*
notation.

``` bnf
cast-expression:
    unary-expression
    '(' type-id ')' cast-expression
```

Any type conversion not mentioned below and not explicitly defined by
the user [class.conv] is ill-formed.

The conversions performed by

- a `const_cast` [expr.const.cast],

- a `static_cast` [expr.static.cast],

- a `static_cast` followed by a `const_cast`,

- a `reinterpret_cast` [expr.reinterpret.cast], or

- a `reinterpret_cast` followed by a `const_cast`,

can be performed using the cast notation of explicit type conversion.
The same semantic restrictions and behaviors apply, with the exception
that in performing a `static_cast` in the following situations the
conversion is valid even if the base class is inaccessible:

- a pointer to an object of derived class type or an lvalue or rvalue of
  derived class type may be explicitly converted to a pointer or
  reference to an unambiguous base class type, respectively;

- a pointer to member of derived class type may be explicitly converted
  to a pointer to member of an unambiguous non-virtual base class type;

- a pointer to an object of an unambiguous non-virtual base class type,
  a glvalue of an unambiguous non-virtual base class type, or a pointer
  to member of an unambiguous non-virtual base class type may be
  explicitly converted to a pointer, a reference, or a pointer to member
  of a derived class type, respectively.

If a conversion can be interpreted in more than one of the ways listed
above, the interpretation that appears first in the list is used, even
if a cast resulting from that interpretation is ill-formed. If a
conversion can be interpreted in more than one way as a `static_cast`
followed by a `const_cast`, the conversion is ill-formed.

\[*Example 23*:

``` cpp
struct A { };
struct I1 : A { };
struct I2 : A { };
struct D : I1, I2 { };
A* foo( D* p ) {
  return (A*)( p );             // ill-formed static_cast interpretation
}
```

— *end example*\]

The operand of a cast using the cast notation can be a prvalue of type
“pointer to incomplete class type”. The destination type of a cast using
the cast notation can be “pointer to incomplete class type”. If both the
operand and destination types are class types and one or both are
incomplete, it is unspecified whether the `static_cast` or the
`reinterpret_cast` interpretation is used, even if there is an
inheritance relationship between the two classes.

\[*Note 77*: For example, if the classes were defined later in the
translation unit, a multi-pass compiler would be permitted to interpret
a cast between pointers to the classes as if the class types were
complete at the point of the cast. — *end note*\]

### Pointer-to-member operators <a id="expr.mptr.oper">[expr.mptr.oper]</a>

The pointer-to-member operators `->*` and `.*` group left-to-right.

``` bnf
pm-expression:
    cast-expression
    pm-expression '.*' cast-expression
    pm-expression '->*' cast-expression
```

The binary operator `.*` binds its second operand, which shall be of
type “pointer to member of `T`” to its first operand, which shall be a
glvalue of class `T` or of a class of which `T` is an unambiguous and
accessible base class. The result is an object or a function of the type
specified by the second operand.

The binary operator `->*` binds its second operand, which shall be of
type “pointer to member of `T`” to its first operand, which shall be of
type “pointer to `U`” where `U` is either `T` or a class of which `T` is
an unambiguous and accessible base class. The expression `E1->*E2` is
converted into the equivalent form `(*(E1)).*E2`.

Abbreviating *pm-expression*`.*`*cast-expression* as `E1.*E2`, `E1` is
called the *object expression*. If the result of `E1` is an object whose
type is not similar to the type of `E1`, or whose most derived object
does not contain the member to which `E2` refers, the behavior is
undefined. The expression `E1` is sequenced before the expression `E2`.

The restrictions on cv-qualification, and the manner in which the
cv-qualifiers of the operands are combined to produce the cv-qualifiers
of the result, are the same as the rules for `E1.E2` given in 
[expr.ref].

\[*Note 78*:

It is not possible to use a pointer to member that refers to a `mutable`
member to modify a const class object. For example,

``` cpp
struct S {
  S() : i(0) { }
  mutable int i;
};
void f()
{
  const S cs;
  int S::* pm = &S::i;          // pm refers to mutable member S::i
  cs.*pm = 88;                  // error: cs is a const object
}
```

— *end note*\]

If the result of `.*` or `->*` is a function, then that result can be
used only as the operand for the function call operator `()`.

\[*Example 24*:

``` cpp
(ptr_to_obj->*ptr_to_mfct)(10);
```

calls the member function denoted by `ptr_to_mfct` for the object
pointed to by `ptr_to_obj`.

— *end example*\]

In a `.*` expression whose object expression is an rvalue, the program
is ill-formed if the second operand is a pointer to member function
whose *ref-qualifier* is `&`, unless its *cv-qualifier-seq* is `const`.
In a `.*` expression whose object expression is an lvalue, the program
is ill-formed if the second operand is a pointer to member function
whose *ref-qualifier* is `&&`. The result of a `.*` expression whose
second operand is a pointer to a data member is an lvalue if the first
operand is an lvalue and an xvalue otherwise. The result of a `.*`
expression whose second operand is a pointer to a member function is a
prvalue. If the second operand is the null member pointer value
[conv.mem], the behavior is undefined.

### Multiplicative operators <a id="expr.mul">[expr.mul]</a>

The multiplicative operators `*`, `/`, and `%` group left-to-right.

``` bnf
multiplicative-expression:
    pm-expression
    multiplicative-expression '*' pm-expression
    multiplicative-expression '/' pm-expression
    multiplicative-expression '%' pm-expression
```

The operands of `*` and `/` shall have arithmetic or unscoped
enumeration type; the operands of `%` shall have integral or unscoped
enumeration type. The usual arithmetic conversions [expr.arith.conv] are
performed on the operands and determine the type of the result.

The binary `*` operator indicates multiplication.

The binary `/` operator yields the quotient, and the binary `%` operator
yields the remainder from the division of the first expression by the
second. If the second operand of `/` or `%` is zero the behavior is
undefined. For integral operands the `/` operator yields the algebraic
quotient with any fractional part discarded;

if the quotient `a/b` is representable in the type of the result,
`(a/b)*b + a%b` is equal to `a`; otherwise, the behavior of both `a/b`
and `a%b` is undefined.

### Additive operators <a id="expr.add">[expr.add]</a>

The additive operators `+` and `-` group left-to-right. The usual
arithmetic conversions [expr.arith.conv] are performed for operands of
arithmetic or enumeration type.

``` bnf
additive-expression:
    multiplicative-expression
    additive-expression '+' multiplicative-expression
    additive-expression '-' multiplicative-expression
```

For addition, either both operands shall have arithmetic or unscoped
enumeration type, or one operand shall be a pointer to a
completely-defined object type and the other shall have integral or
unscoped enumeration type.

For subtraction, one of the following shall hold:

- both operands have arithmetic or unscoped enumeration type; or

-  both operands are pointers to cv-qualified or cv-unqualified versions
  of the same completely-defined object type; or

- the left operand is a pointer to a completely-defined object type and
  the right operand has integral or unscoped enumeration type.

The result of the binary `+` operator is the sum of the operands. The
result of the binary `-` operator is the difference resulting from the
subtraction of the second operand from the first.

When an expression `J` that has integral type is added to or subtracted
from an expression `P` of pointer type, the result has the type of `P`.

- If `P` evaluates to a null pointer value and `J` evaluates to 0, the
  result is a null pointer value.

- Otherwise, if `P` points to an array element i of an array object `x`
  with n elements [dcl.array],

  the expressions `P + J` and `J + P` (where `J` has the value j) point
  to the (possibly-hypothetical) array element i + j of `x` if
  $0 \le i + j \le n$ and the expression `P - J` points to the
  (possibly-hypothetical) array element i - j of `x` if
  $0 \le i - j \le n$.

- Otherwise, the behavior is undefined.

\[*Note 79*: Adding a value other than 0 or 1 to a pointer to a base
class subobject, a member subobject, or a complete object results in
undefined behavior. — *end note*\]

When two pointer expressions `P` and `Q` are subtracted, the type of the
result is an *implementation-defined* signed integral type; this type
shall be the same type that is defined as `std::ptrdiff_t` in the
`<cstddef>` header [support.types.layout].

- If `P` and `Q` both evaluate to null pointer values, the result is 0.

- Otherwise, if `P` and `Q` point to, respectively, array elements i and
  j of the same array object `x`, the expression `P - Q` has the value
  i - j.

- Otherwise, the behavior is undefined.

  \[*Note 9*: If the value i - j is not in the range of representable
  values of type `std::ptrdiff_t`, the behavior is
  undefined. — *end note*\]

For addition or subtraction, if the expressions `P` or `Q` have type
“pointer to cv `T`”, where `T` and the array element type are not
similar [conv.qual], the behavior is undefined.

\[*Example 25*:

``` cpp
int arr[5] = {1, 2, 3, 4, 5};
unsigned int *p = reinterpret_cast<unsigned int*>(arr + 1);
unsigned int k = *p;            // OK, value of k is $2$[conv.lval]
unsigned int *q = p + 1;        // undefined behavior: p points to an int, not an unsigned int object
```

— *end example*\]

### Shift operators <a id="expr.shift">[expr.shift]</a>

The shift operators `<<` and `>>` group left-to-right.

``` bnf
shift-expression:
    additive-expression
    shift-expression '<<' additive-expression
    shift-expression '>>' additive-expression
```

The operands shall be of integral or unscoped enumeration type and
integral promotions are performed. The type of the result is that of the
promoted left operand. The behavior is undefined if the right operand is
negative, or greater than or equal to the width of the promoted left
operand.

The value of `E1 << E2` is the unique value congruent to
$\tcode{E1} \times 2^\tcode{E2}$ modulo $2^N$, where N is the width of
the type of the result.

\[*Note 80*: `E1` is left-shifted `E2` bit positions; vacated bits are
zero-filled. — *end note*\]

The value of `E1 >> E2` is $\tcode{E1} / 2^\tcode{E2}$, rounded down.

\[*Note 81*: `E1` is right-shifted `E2` bit positions. Right-shift on
signed integral types is an arithmetic right shift, which performs
sign-extension. — *end note*\]

The expression `E1` is sequenced before the expression `E2`.

### Three-way comparison operator <a id="expr.spaceship">[expr.spaceship]</a>

The three-way comparison operator groups left-to-right.

``` bnf
compare-expression:
    shift-expression
    compare-expression '<=>' shift-expression
```

The expression `p <=> q` is a prvalue indicating whether `p` is less
than, equal to, greater than, or incomparable with `q`.

If one of the operands is of type `bool` and the other is not, the
program is ill-formed.

If both operands have arithmetic types, or one operand has integral type
and the other operand has unscoped enumeration type, the usual
arithmetic conversions [expr.arith.conv] are applied to the operands.
Then:

- If a narrowing conversion [dcl.init.list] is required, other than from
  an integral type to a floating-point type, the program is ill-formed.

- Otherwise, if the operands have integral type, the result is of type
  `std::strong_ordering`. The result is `std::strong_ordering::equal` if
  both operands are arithmetically equal, `std::strong_ordering::less`
  if the first operand is arithmetically less than the second operand,
  and `std::strong_ordering::greater` otherwise.

- Otherwise, the operands have floating-point type, and the result is of
  type `std::partial_ordering`. The expression `a <=> b` yields
  `std::partial_ordering::less` if `a` is less than `b`,
  `std::partial_ordering::greater` if `a` is greater than `b`,
  `std::partial_ordering::equivalent` if `a` is equivalent to `b`, and
  `std::partial_ordering::unordered` otherwise.

If both operands have the same enumeration type `E`, the operator yields
the result of converting the operands to the underlying type of `E` and
applying `<=>` to the converted operands.

If at least one of the operands is of object pointer type and the other
operand is of object pointer or array type, array-to-pointer conversions
[conv.array], pointer conversions [conv.ptr], and qualification
conversions [conv.qual] are performed on both operands to bring them to
their composite pointer type [expr.type]. After the conversions, the
operands shall have the same type.

\[*Note 82*: If both of the operands are arrays, array-to-pointer
conversions [conv.array] are not applied. — *end note*\]

In this case, `p <=> q` is of type `std::strong_ordering` and the result
is defined by the following rules:

- If two pointer operands `p` and `q` compare equal [expr.eq], `p <=> q`
  yields `std::strong_ordering::equal`;

- otherwise, if `p` and `q` compare unequal, `p <=> q` yields
  `std::strong_ordering::less` if `q` compares greater than `p` and
  `std::strong_ordering::greater` if `p` compares greater than `q`
  [expr.rel];

- otherwise, the result is unspecified.

Otherwise, the program is ill-formed.

The three comparison category types [cmp.categories] (the types
`std::strong_ordering`, `std::weak_ordering`, and
`std::partial_ordering`) are not predefined; if a standard library
declaration [compare.syn,std.modules] of such a class type does not
precede [basic.lookup.general] a use of that type — even an implicit use
in which the type is not named (e.g., via the `auto` specifier
[dcl.spec.auto] in a defaulted three-way comparison [class.spaceship] or
use of the built-in operator) — the program is ill-formed.

### Relational operators <a id="expr.rel">[expr.rel]</a>

The relational operators group left-to-right.

\[*Example 26*: `a<b<c` means `(a<b)<c` and *not*
`(a<b)&&(b<c)`. — *end example*\]

``` bnf
relational-expression:
    compare-expression
    relational-expression '<' compare-expression
    relational-expression '>' compare-expression
    relational-expression '<=' compare-expression
    relational-expression '>=' compare-expression
```

The lvalue-to-rvalue [conv.lval], array-to-pointer [conv.array], and
function-to-pointer [conv.func] standard conversions are performed on
the operands. The comparison is deprecated if both operands were of
array type prior to these conversions [depr.array.comp].

The converted operands shall have arithmetic, enumeration, or pointer
type. The operators `<` (less than), `>` (greater than), `<=` (less than
or equal to), and `>=` (greater than or equal to) all yield `false` or
`true`. The type of the result is `bool`.

The usual arithmetic conversions [expr.arith.conv] are performed on
operands of arithmetic or enumeration type. If both operands are
pointers, pointer conversions [conv.ptr] and qualification conversions
[conv.qual] are performed to bring them to their composite pointer type
[expr.type]. After conversions, the operands shall have the same type.

The result of comparing unequal pointers to objects

is defined in terms of a partial order consistent with the following
rules:

- If two pointers point to different elements of the same array, or to
  subobjects thereof, the pointer to the element with the higher
  subscript is required to compare greater.

- If two pointers point to different non-static data members of the same
  object, or to subobjects of such members, recursively, the pointer to
  the later declared member is required to compare greater provided
  neither member is a subobject of zero size and their class is not a
  union.

- Otherwise, neither pointer is required to compare greater than the
  other.

If two operands `p` and `q` compare equal [expr.eq], `p<=q` and `p>=q`
both yield `true` and `p<q` and `p>q` both yield `false`. Otherwise, if
a pointer to object `p` compares greater than a pointer `q`, `p>=q`,
`p>q`, `q<=p`, and `q<p` all yield `true` and `p<=q`, `p<q`, `q>=p`, and
`q>p` all yield `false`. Otherwise, the result of each of the operators
is unspecified.

\[*Note 83*: A relational operator applied to unequal function pointers
or to unequal pointers to `void` yields an unspecified
result. — *end note*\]

If both operands (after conversions) are of arithmetic or enumeration
type, each of the operators shall yield `true` if the specified
relationship is true and `false` if it is false.

### Equality operators <a id="expr.eq">[expr.eq]</a>

``` bnf
equality-expression:
    relational-expression
    equality-expression '==' relational-expression
    equality-expression '!=' relational-expression
```

The `==` (equal to) and the `!=` (not equal to) operators group
left-to-right. The lvalue-to-rvalue [conv.lval], array-to-pointer
[conv.array], and function-to-pointer [conv.func] standard conversions
are performed on the operands. The comparison is deprecated if both
operands were of array type prior to these conversions
[depr.array.comp].

The converted operands shall have arithmetic, enumeration, pointer, or
pointer-to-member type, or type `std::nullptr_t`. The operators `==` and
`!=` both yield `true` or `false`, i.e., a result of type `bool`. In
each case below, the operands shall have the same type after the
specified conversions have been applied.

If at least one of the operands is a pointer, pointer conversions
[conv.ptr], function pointer conversions [conv.fctptr], and
qualification conversions [conv.qual] are performed on both operands to
bring them to their composite pointer type [expr.type]. Comparing
pointers is defined as follows:

- If one pointer represents the address of a complete object, and
  another pointer represents the address one past the last element of a
  different complete object,

  the result of the comparison is unspecified.

- Otherwise, if the pointers are both null, both point to the same
  function, or both represent the same address [basic.compound], they
  compare equal.

- Otherwise, the pointers compare unequal.

If at least one of the operands is a pointer to member,
pointer-to-member conversions [conv.mem], function pointer conversions
[conv.fctptr], and qualification conversions [conv.qual] are performed
on both operands to bring them to their composite pointer type
[expr.type]. Comparing pointers to members is defined as follows:

- If two pointers to members are both the null member pointer value,
  they compare equal.

- If only one of two pointers to members is the null member pointer
  value, they compare unequal.

- If either is a pointer to a virtual member function, the result is
  unspecified.

- If one refers to a member of class `C1` and the other refers to a
  member of a different class `C2`, where neither is a base class of the
  other, the result is unspecified.

  \[*Example 5*:

  ``` cpp
  struct A {};
  struct B : A { int x; };
  struct C : A { int x; };

  int A::*bx = (int(A::*))&B::x;
  int A::*cx = (int(A::*))&C::x;

  bool b1 = (bx == cx);   // unspecified
  ```

  — *end example*\]

- If both refer to (possibly different) members of the same union
  [class.union], they compare equal.

- Otherwise, two pointers to members compare equal if they would refer
  to the same member of the same most derived object [intro.object] or
  the same subobject if indirection with a hypothetical object of the
  associated class type were performed, otherwise they compare unequal.

  \[*Example 6*:

  ``` cpp
  struct B {
    int f();
  };
  struct L : B { };
  struct R : B { };
  struct D : L, R { };

  int (B::*pb)() = &B::f;
  int (L::*pl)() = pb;
  int (R::*pr)() = pb;
  int (D::*pdl)() = pl;
  int (D::*pdr)() = pr;
  bool x = (pdl == pdr);          // false
  bool y = (pb == pl);            // true
  ```

  — *end example*\]

Two operands of type `std::nullptr_t` or one operand of type
`std::nullptr_t` and the other a null pointer constant compare equal.

If two operands compare equal, the result is `true` for the `==`
operator and `false` for the `!=` operator. If two operands compare
unequal, the result is `false` for the `==` operator and `true` for the
`!=` operator. Otherwise, the result of each of the operators is
unspecified.

If both operands are of arithmetic or enumeration type, the usual
arithmetic conversions [expr.arith.conv] are performed on both operands;
each of the operators shall yield `true` if the specified relationship
is true and `false` if it is false.

### Bitwise AND operator <a id="expr.bit.and">[expr.bit.and]</a>

``` bnf
and-expression:
    equality-expression
    and-expression '&' equality-expression
```

The `&` operator groups left-to-right. The operands shall be of integral
or unscoped enumeration type. The usual arithmetic conversions
[expr.arith.conv] are performed. Given the coefficients $\tcode{x}_i$
and $\tcode{y}_i$ of the base-2 representation [basic.fundamental] of
the converted operands `x` and `y`, the coefficient $\tcode{r}_i$ of the
base-2 representation of the result `r` is 1 if both $\tcode{x}_i$ and
$\tcode{y}_i$ are 1, and 0 otherwise.

\[*Note 84*: The result is the bitwise function of the
operands. — *end note*\]

### Bitwise exclusive OR operator <a id="expr.xor">[expr.xor]</a>

``` bnf
exclusive-or-expression:
    and-expression
    exclusive-or-expression '\caret' and-expression
```

The `\caret` operator groups left-to-right. The operands shall be of
integral or unscoped enumeration type. The usual arithmetic conversions
[expr.arith.conv] are performed. Given the coefficients $\tcode{x}_i$
and $\tcode{y}_i$ of the base-2 representation [basic.fundamental] of
the converted operands `x` and `y`, the coefficient $\tcode{r}_i$ of the
base-2 representation of the result `r` is 1 if either (but not both) of
$\tcode{x}_i$ and $\tcode{y}_i$ is 1, and 0 otherwise.

\[*Note 85*: The result is the bitwise exclusive function of the
operands. — *end note*\]

### Bitwise inclusive OR operator <a id="expr.or">[expr.or]</a>

``` bnf
inclusive-or-expression:
    exclusive-or-expression
    inclusive-or-expression '|' exclusive-or-expression
```

The `|` operator groups left-to-right. The operands shall be of integral
or unscoped enumeration type. The usual arithmetic conversions
[expr.arith.conv] are performed. Given the coefficients $\tcode{x}_i$
and $\tcode{y}_i$ of the base-2 representation [basic.fundamental] of
the converted operands `x` and `y`, the coefficient $\tcode{r}_i$ of the
base-2 representation of the result `r` is 1 if at least one of
$\tcode{x}_i$ and $\tcode{y}_i$ is 1, and 0 otherwise.

\[*Note 86*: The result is the bitwise inclusive function of the
operands. — *end note*\]

### Logical AND operator <a id="expr.log.and">[expr.log.and]</a>

``` bnf
logical-and-expression:
    inclusive-or-expression
    logical-and-expression '&&' inclusive-or-expression
```

The `&&` operator groups left-to-right. The operands are both
contextually converted to `bool` [conv]. The result is `true` if both
operands are `true` and `false` otherwise. Unlike `&`, `&&` guarantees
left-to-right evaluation: the second operand is not evaluated if the
first operand is `false`.

The result is a `bool`. If the second expression is evaluated, the first
expression is sequenced before the second expression [intro.execution].

### Logical OR operator <a id="expr.log.or">[expr.log.or]</a>

``` bnf
logical-or-expression:
    logical-and-expression
    logical-or-expression '||' logical-and-expression
```

The `||` operator groups left-to-right. The operands are both
contextually converted to `bool` [conv]. The result is `true` if either
of its operands is `true`, and `false` otherwise. Unlike `|`, `||`
guarantees left-to-right evaluation; moreover, the second operand is not
evaluated if the first operand evaluates to `true`.

The result is a `bool`. If the second expression is evaluated, the first
expression is sequenced before the second expression [intro.execution].

### Conditional operator <a id="expr.cond">[expr.cond]</a>

``` bnf
conditional-expression:
    logical-or-expression
    logical-or-expression '?' expression ':' assignment-expression
```

Conditional expressions group right-to-left. The first expression is
contextually converted to `bool` [conv]. It is evaluated and if it is
`true`, the result of the conditional expression is the value of the
second expression, otherwise that of the third expression. Only one of
the second and third expressions is evaluated. The first expression is
sequenced before the second or third expression [intro.execution].

If either the second or the third operand has type `void`, one of the
following shall hold:

-  The second or the third operand (but not both) is a (possibly
  parenthesized) *throw-expression* [expr.throw]; the result is of the
  type and value category of the other. The *conditional-expression* is
  a bit-field if that operand is a bit-field.

- Both the second and the third operands have type `void`; the result is
  of type `void` and is a prvalue.

  \[*Note 10*: This includes the case where both operands are
  *throw-expression*. — *end note*\]

Otherwise, if the second and third operand are glvalue bit-fields of the
same value category and of types `T` and `T`, respectively, the operands
are considered to be of type cv `T` for the remainder of this subclause,
where cv is the union of and .

Otherwise, if the second and third operand have different types and
either has (possibly cv-qualified) class type, or if both are glvalues
of the same value category and the same type except for
cv-qualification, an attempt is made to form an implicit conversion
sequence [over.best.ics] from each of those operands to the type of the
other.

\[*Note 87*: Properties such as access, whether an operand is a
bit-field, or whether a conversion function is deleted are ignored for
that determination. — *end note*\]

Attempts are made to form an implicit conversion sequence from an
operand expression `E1` of type `T1` to a target type related to the
type `T2` of the operand expression `E2` as follows:

- If `E2` is an lvalue, the target type is “lvalue reference to `T2`”,
  but an implicit conversion sequence can only be formed if the
  reference would bind directly [dcl.init.ref] to a glvalue.

- If `E2` is an xvalue, the target type is “rvalue reference to `T2`”,
  but an implicit conversion sequence can only be formed if the
  reference would bind directly.

- If `E2` is a prvalue or if neither of the conversion sequences above
  can be formed and at least one of the operands has (possibly
  cv-qualified) class type:

  - if `T1` and `T2` are the same class type (ignoring cv-qualification)
    and `T2` is at least as cv-qualified as `T1`, the target type is
    `T2`,

  - otherwise, if `T2` is a base class of `T1`, the target type is `T2`,
    where denotes the cv-qualifiers of `T1`,

  - otherwise, the target type is the type that `E2` would have after
    applying the lvalue-to-rvalue [conv.lval], array-to-pointer
    [conv.array], and function-to-pointer [conv.func] standard
    conversions.

Using this process, it is determined whether an implicit conversion
sequence can be formed from the second operand to the target type
determined for the third operand, and vice versa. If both sequences can
be formed, or one can be formed but it is the ambiguous conversion
sequence, the program is ill-formed. If no conversion sequence can be
formed, the operands are left unchanged and further checking is
performed as described below. Otherwise, if exactly one conversion
sequence can be formed, that conversion is applied to the chosen operand
and the converted operand is used in place of the original operand for
the remainder of this subclause.

\[*Note 88*: The conversion might be ill-formed even if an implicit
conversion sequence could be formed. — *end note*\]

If the second and third operands are glvalues of the same value category
and have the same type, the result is of that type and value category
and it is a bit-field if the second or the third operand is a bit-field,
or if both are bit-fields.

Otherwise, the result is a prvalue. If the second and third operands do
not have the same type, and either has (possibly cv-qualified) class
type, overload resolution is used to determine the conversions (if any)
to be applied to the operands [over.match.oper,over.built]. If the
overload resolution fails, the program is ill-formed. Otherwise, the
conversions thus determined are applied, and the converted operands are
used in place of the original operands for the remainder of this
subclause.

Lvalue-to-rvalue [conv.lval], array-to-pointer [conv.array], and
function-to-pointer [conv.func] standard conversions are performed on
the second and third operands. After those conversions, one of the
following shall hold:

- The second and third operands have the same type; the result is of
  that type and the result object is initialized using the selected
  operand.

- The second and third operands have arithmetic or enumeration type; the
  usual arithmetic conversions [expr.arith.conv] are performed to bring
  them to a common type, and the result is of that type.

- One or both of the second and third operands have pointer type;
  pointer conversions [conv.ptr], function pointer conversions
  [conv.fctptr], and qualification conversions [conv.qual] are performed
  to bring them to their composite pointer type [expr.type]. The result
  is of the composite pointer type.

- One or both of the second and third operands have pointer-to-member
  type; pointer to member conversions [conv.mem], function pointer
  conversions [conv.fctptr], and qualification conversions [conv.qual]
  are performed to bring them to their composite pointer type
  [expr.type]. The result is of the composite pointer type.

- Both the second and third operands have type `std::nullptr_t` or one
  has that type and the other is a null pointer constant. The result is
  of type `std::nullptr_t`.

### Yielding a value <a id="expr.yield">[expr.yield]</a>

``` bnf
yield-expression:
  'co_yield' assignment-expression
  'co_yield' braced-init-list
```

A *yield-expression* shall appear only within a suspension context of a
function [expr.await]. Let *e* be the operand of the *yield-expression*
and *p* be an lvalue naming the promise object of the enclosing
coroutine [dcl.fct.def.coroutine], then the *yield-expression* is
equivalent to the expression `co_await p.yield_value(e)`.

\[*Example 27*:

``` cpp
template <typename T>
struct my_generator {
  struct promise_type {
    T current_value;
    ...
    auto yield_value(T v) {
      current_value = std::move(v);
      return std::suspend_always{};
    }
  };
  struct iterator { ... };
  iterator begin();
  iterator end();
};

my_generator<pair<int,int>> g1() {
  for (int i = 0; i < 10; ++i) co_yield {i,i};
}
my_generator<pair<int,int>> g2() {
  for (int i = 0; i < 10; ++i) co_yield make_pair(i,i);
}

auto f(int x = co_yield 5);     // error: yield-expression outside of function suspension context
int a[] = { co_yield 1 };       // error: yield-expression outside of function suspension context

int main() {
  auto r1 = g1();
  auto r2 = g2();
  assert(std::equal(r1.begin(), r1.end(), r2.begin(), r2.end()));
}
```

— *end example*\]

### Throwing an exception <a id="expr.throw">[expr.throw]</a>

``` bnf
throw-expression:
    \texttt{throw}  [assignment-expression]
```

A *throw-expression* is of type `void`.

Evaluating a *throw-expression* with an operand throws an exception
[except.throw]; the type of the exception object is determined by
removing any top-level *cv-qualifier* from the static type of the
operand and adjusting the type from “array of `T`” or function type `T`
to “pointer to `T`”.

A *throw-expression* with no operand rethrows the currently handled
exception [except.handle]. The exception is reactivated with the
existing exception object; no new exception object is created. The
exception is no longer considered to be caught.

\[*Example 28*:

An exception handler that cannot completely handle the exception itself
can be written like this:

``` cpp
try {
  // ...
} catch (...) {     // catch all exceptions
  // respond (partially) to exception
  throw;            // pass the exception to some other handler
}
```

— *end example*\]

If no exception is presently being handled, evaluating a
*throw-expression* with no operand calls `std::terminate()`
[except.terminate].

### Assignment and compound assignment operators <a id="expr.ass">[expr.ass]</a>

The assignment operator (`=`) and the compound assignment operators all
group right-to-left. All require a modifiable lvalue as their left
operand; their result is an lvalue of the type of the left operand,
referring to the left operand. The result in all cases is a bit-field if
the left operand is a bit-field. In all cases, the assignment is
sequenced after the value computation of the right and left operands,
and before the value computation of the assignment expression. The right
operand is sequenced before the left operand. With respect to an
indeterminately-sequenced function call, the operation of a compound
assignment is a single evaluation.

\[*Note 89*: Therefore, a function call cannot intervene between the
lvalue-to-rvalue conversion and the side effect associated with any
single compound assignment operator. — *end note*\]

``` bnf
assignment-expression:
    conditional-expression
    yield-expression
    throw-expression
    logical-or-expression assignment-operator initializer-clause
```

``` bnf
assignment-operator: one of
    '=  *=  /=  %=   +=  -=  >>=  <<=  &=  \caret=  |='
```

In simple assignment (`=`), the object referred to by the left operand
is modified [defns.access] by replacing its value with the result of the
right operand.

If the right operand is an expression, it is implicitly converted [conv]
to the cv-unqualified type of the left operand.

When the left operand of an assignment operator is a bit-field that
cannot represent the value of the expression, the resulting value of the
bit-field is .

An assignment whose left operand is of a volatile-qualified type is
deprecated [depr.volatile.type] unless the (possibly parenthesized)
assignment is a discarded-value expression or an unevaluated operand
[term.unevaluated.operand].

The behavior of an expression of the form `E1 op= E2` is equivalent to
`E1 = E1 op E2` except that `E1` is evaluated only once.

\[*Note 90*: The object designated by `E1` is accessed
twice. — *end note*\]

For `+=` and `-=`, `E1` shall either have arithmetic type or be a
pointer to a possibly cv-qualified completely-defined object type. In
all other cases, `E1` shall have arithmetic type.

If the value being stored in an object is read via another object that
overlaps in any way the storage of the first object, then the overlap
shall be exact and the two objects shall have the same type, otherwise
the behavior is undefined.

\[*Note 91*: This restriction applies to the relationship between the
left and right sides of the assignment operation; it is not a statement
about how the target of the assignment can be aliased in general. See 
[basic.lval]. — *end note*\]

A *braced-init-list* may appear on the right-hand side of

- an assignment to a scalar, in which case the initializer list shall
  have at most a single element. The meaning of `x = \{v\}`, where `T`
  is the scalar type of the expression `x`, is that of `x = T\{v\}`. The
  meaning of `x = \{\}` is `x = T\{\}`.

- an assignment to an object of class type, in which case the
  initializer list is passed as the argument to the assignment operator
  function selected by overload resolution [over.ass,over.match].

\[*Example 29*:

``` cpp
complex<double> z;
z = { 1,2 };        // meaning z.operator=(\{1,2\)}
z += { 1, 2 };      // meaning z.operator+=(\{1,2\)}
int a, b;
a = b = { 1 };      // meaning a=b=1;
a = { 1 } = b;      // syntax error
```

— *end example*\]

### Comma operator <a id="expr.comma">[expr.comma]</a>

The comma operator groups left-to-right.

``` bnf
expression:
    assignment-expression
    expression ',' assignment-expression
```

A pair of expressions separated by a comma is evaluated left-to-right;
the left expression is a discarded-value expression [expr.prop]. The
left expression is sequenced before the right expression
[intro.execution]. The type and value of the result are the type and
value of the right operand; the result is of the same value category as
its right operand, and is a bit-field if its right operand is a
bit-field.

\[*Note 92*:

In contexts where the comma token is given special meaning (e.g.,
function calls [expr.call], subscript expressions [expr.sub], lists of
initializers [dcl.init], or *template-argument-list* [temp.names]), the
comma operator as described in this subclause can appear only in
parentheses.

— *end note*\]

## Constant expressions <a id="expr.const">[expr.const]</a>

Certain contexts require expressions that satisfy additional
requirements as detailed in this subclause; other contexts have
different semantics depending on whether or not an expression satisfies
these requirements. Expressions that satisfy these requirements,
assuming that copy elision [class.copy.elision] is not performed, are
called *constant expressions*.

\[*Note 1*: Constant expressions can be evaluated during
translation. — *end note*\]

``` bnf
constant-expression:
    conditional-expression
```

A variable or temporary object `o` is *constant-initialized* if

- either it has an initializer or its default-initialization results in
  some initialization being performed, and

- the full-expression of its initialization is a constant expression
  when interpreted as a *constant-expression*, except that if `o` is an
  object, that full-expression may also invoke constexpr constructors
  for `o` and its subobjects even if those objects are of non-literal
  class types.

  \[*Note 11*: Such a class can have a non-trivial destructor. Within
  this evaluation, `std::is_constant_evaluated()` [meta.const.eval]
  returns `true`. — *end note*\]

A variable is *potentially-constant* if it is constexpr or it has
reference or non-volatile const-qualified integral or enumeration type.

A constant-initialized potentially-constant variable V is
*usable in constant expressions* at a point P if V’s initializing
declaration D is reachable from P and

- V is constexpr,

- V is not initialized to a TU-local value, or

- P is in the same translation unit as D.

An object or reference is *usable in constant expressions* if it is

- a variable that is usable in constant expressions, or

- a template parameter object [temp.param], or

- a string literal object [lex.string], or

- a temporary object of non-volatile const-qualified literal type whose
  lifetime is extended [class.temporary] to that of a variable that is
  usable in constant expressions, or

- a non-mutable subobject or reference member of any of the above.

An expression E is a *core constant expression* unless the evaluation of
E, following the rules of the abstract machine [intro.execution], would
evaluate one of the following:

- `this` [expr.prim.this], except

  - in a constexpr function [dcl.constexpr] that is being evaluated as
    part of E or

  - when appearing as the *postfix-expression* of an implicit or
    explicit class member access expression [expr.ref];

- a control flow that passes through a declaration of a variable with
  static [basic.stc.static] or thread [basic.stc.thread] storage
  duration, unless that variable is usable in constant expressions;

  \[*Example 7*:

  ``` cpp
  constexpr char test() {
    static const int x = 5;
    static constexpr char c[] = "Hello World";
    return *(c + x);
  }
  static_assert(' ' == test());
  ```

  — *end example*\]

- an invocation of a non-constexpr function;

- an invocation of an undefined constexpr function;

- an invocation of an instantiated constexpr function that is not
  constexpr-suitable;

- an invocation of a virtual function [class.virtual] for an object
  whose dynamic type is constexpr-unknown;

- an expression that would exceed the implementation-defined limits (see
  [implimits]);

- an operation that would have undefined behavior as specified in
  [intro] through [cpp], excluding [dcl.attr.assume];

- an lvalue-to-rvalue conversion [conv.lval] unless it is applied to

  - a non-volatile glvalue that refers to an object that is usable in
    constant expressions, or

  - a non-volatile glvalue of literal type that refers to a non-volatile
    object whose lifetime began within the evaluation of E;

- an lvalue-to-rvalue conversion that is applied to a glvalue that
  refers to a non-active member of a union or a subobject thereof;

- an lvalue-to-rvalue conversion that is applied to an object with an
  indeterminate value [basic.indet];

- an invocation of an implicitly-defined copy/move constructor or
  copy/move assignment operator for a union whose active member (if any)
  is mutable, unless the lifetime of the union object began within the
  evaluation of E;

- in a *lambda-expression*, a reference to `this` or to a variable with
  automatic storage duration defined outside that *lambda-expression*,
  where the reference would be an odr-use
  [term.odr.use,expr.prim.lambda];

  \[*Example 8*:

  ``` cpp
  void g() {
    const int n = 0;
    [=] {
      constexpr int i = n;        // OK, n is not odr-used here
      constexpr int j = *&n;      // error: \&n would be an odr-use of n
    };
  }
  ```

  — *end example*\]

  \[*Note 12*:

  If the odr-use occurs in an invocation of a function call operator of
  a closure type, it no longer refers to `this` or to an enclosing
  automatic variable due to the transformation
  [expr.prim.lambda.capture] of the *id-expression* into an access of
  the corresponding data member.

  — *end note*\]

- a conversion from type cv `void*` to a pointer-to-object type;

- a `reinterpret_cast` [expr.reinterpret.cast];

- a modification of an object [expr.ass,expr.post.incr,expr.pre.incr]
  unless it is applied to a non-volatile lvalue of literal type that
  refers to a non-volatile object whose lifetime began within the
  evaluation of E;

- an invocation of a destructor [class.dtor] or a function call whose
  *postfix-expression* names a pseudo-destructor [expr.call], in either
  case for an object whose lifetime did not begin within the evaluation
  of E;

- a *new-expression* [expr.new], unless the selected allocation function
  is a replaceable global allocation function
  [new.delete.single,new.delete.array] and the allocated storage is
  deallocated within the evaluation of E;

- a *delete-expression* [expr.delete], unless it deallocates a region of
  storage allocated within the evaluation of E;

- a call to an instance of `std::allocator<T>::allocate`
  [allocator.members], unless the allocated storage is deallocated
  within the evaluation of E;

- a call to an instance of `std::allocator<T>::deallocate`
  [allocator.members], unless it deallocates a region of storage
  allocated within the evaluation of E;

- an *await-expression* [expr.await];

- a *yield-expression* [expr.yield];

- a three-way comparison [expr.spaceship], relational [expr.rel], or
  equality [expr.eq] operator where the result is unspecified;

- a *throw-expression* [expr.throw];

- a `dynamic_cast` [expr.dynamic.cast] or `typeid` [expr.typeid]
  expression on a glvalue that refers to an object whose dynamic type is
  constexpr-unknown or that would throw an exception;

- an *asm-declaration* [dcl.asm];

- an invocation of the `va_arg` macro [cstdarg.syn];

- a non-constant library call [defns.nonconst.libcall]; or

- a `goto` statement [stmt.goto].

It is unspecified whether E is a core constant expression if E satisfies
the constraints of a core constant expression, but evaluation of E would
evaluate

- an operation that has undefined behavior as specified in [library]
  through [\lastlibchapter],

- an invocation of the `va_start` macro [cstdarg.syn], or

- a statement with an assumption [dcl.attr.assume] whose converted
  *conditional-expression*, if evaluated where the assumption appears,
  would not disqualify E from being a core constant expression and would
  not evaluate to `true`.

  \[*Note 13*: E is not disqualified from being a core constant
  expression if the hypothetical evaluation of the converted
  *conditional-expression* would disqualify E from being a core constant
  expression. — *end note*\]

\[*Example 1*:

``` cpp
int x;                              // not constant
struct A {
  constexpr A(bool b) : m(b?42:x) { }
  int m;
};
constexpr int v = A(true).m;        // OK, constructor call initializes m with the value 42

constexpr int w = A(false).m;       // error: initializer for m is x, which is non-constant

constexpr int f1(int k) {
  constexpr int x = k;              // error: x is not initialized by a constant expression
                                    // because lifetime of k began outside the initializer of x
  return x;
}
constexpr int f2(int k) {
  int x = k;                        // OK, not required to be a constant expression
                                    // because x is not constexpr
  return x;
}

constexpr int incr(int &n) {
  return ++n;
}
constexpr int g(int k) {
  constexpr int x = incr(k);        // error: incr(k) is not a core constant expression
                                    // because lifetime of k began outside the expression incr(k)
  return x;
}
constexpr int h(int k) {
  int x = incr(k);                  // OK, incr(k) is not required to be a core constant expression
  return x;
}
constexpr int y = h(1);             // OK, initializes y with the value 2
                                    // h(1) is a core constant expression because
                                    // the lifetime of k begins inside h(1)
```

— *end example*\]

For the purposes of determining whether an expression E is a core
constant expression, the evaluation of the body of a member function of
`std::allocator<T>` as defined in [allocator.members], where `T` is a
literal type, is ignored. Similarly, the evaluation of the body of
`std::construct_at` or `std::ranges::construct_at` is considered to
include only the underlying constructor call if the first argument (of
type `T*`) points to storage allocated with `std::allocator<T>` or to an
object whose lifetime began within the evaluation of E.

For the purposes of determining whether E is a core constant expression,
the evaluation of a call to a trivial copy/move constructor or copy/move
assignment operator of a union is considered to copy/move the active
member of the union, if any.

\[*Note 2*: The copy/move of the active member is
trivial. — *end note*\]

During the evaluation of an expression E as a core constant expression,
all *id-expression*s and uses of `*this` that refer to an object or
reference whose lifetime did not begin with the evaluation of E are
treated as referring to a specific instance of that object or reference
whose lifetime and that of all subobjects (including all union members)
includes the entire constant evaluation. For such an object that is not
usable in constant expressions, the dynamic type of the object is
*constexpr-unknown*. For such a reference that is not usable in constant
expressions, the reference is treated as binding to an unspecified
object of the referenced type whose lifetime and that of all subobjects
includes the entire constant evaluation and whose dynamic type is
constexpr-unknown.

\[*Example 2*:

``` cpp
template <typename T, size_t N>
constexpr size_t array_size(T (&)[N]) {
  return N;
}

void use_array(int const (&gold_medal_mel)[2]) {
  constexpr auto gold = array_size(gold_medal_mel);     // OK
}

constexpr auto olympic_mile() {
  const int ledecky = 1500;
  return []{ return ledecky; };
}
static_assert(olympic_mile()() == 1500);                // OK

struct Swim {
  constexpr int phelps() { return 28; }
  virtual constexpr int lochte() { return 12; }
  int coughlin = 12;
};

constexpr int how_many(Swim& swam) {
  Swim* p = &swam;
  return (p + 1 - 1)->phelps();
}

void splash(Swim& swam) {
  static_assert(swam.phelps() == 28);           // OK
  static_assert((&swam)->phelps() == 28);       // OK

  Swim* pswam = &swam;
  static_assert(pswam->phelps() == 28);         // error: lvalue-to-rvalue conversion on a pointer
                                                // not usable in constant expressions

  static_assert(how_many(swam) == 28);          // OK
  static_assert(Swim().lochte() == 12);         // OK

  static_assert(swam.lochte() == 12);           // error: invoking virtual function on reference
                                                // with constexpr-unknown dynamic type

  static_assert(swam.coughlin == 12);           // error: lvalue-to-rvalue conversion on an object
                                                // not usable in constant expressions
}

extern Swim dc;
extern Swim& trident;

constexpr auto& sandeno   = typeid(dc);         // OK, can only be typeid(Swim)
constexpr auto& gallagher = typeid(trident);    // error: constexpr-unknown dynamic type
```

— *end example*\]

An object `a` is said to have *constant destruction* if:

- it is not of class type nor (possibly multidimensional) array thereof,
  or

- it is of class type or (possibly multidimensional) array thereof, that
  class type has a constexpr destructor, and for a hypothetical
  expression E whose only effect is to destroy `a`, E would be a core
  constant expression if the lifetime of `a` and its non-mutable
  subobjects (but not its mutable subobjects) were considered to start
  within E.

An *integral constant expression* is an expression of integral or
unscoped enumeration type, implicitly converted to a prvalue, where the
converted expression is a core constant expression.

\[*Note 3*: Such expressions can be used as bit-field lengths
[class.bit], as enumerator initializers if the underlying type is not
fixed [dcl.enum], and as alignments [dcl.align]. — *end note*\]

If an expression of literal class type is used in a context where an
integral constant expression is required, then that expression is
contextually implicitly converted [conv] to an integral or unscoped
enumeration type and the selected conversion function shall be
`constexpr`.

\[*Example 3*:

``` cpp
struct A {
  constexpr A(int i) : val(i) { }
  constexpr operator int() const { return val; }
  constexpr operator long() const { return 42; }
private:
  int val;
};
constexpr A a = alignof(int);
alignas(a) int n;               // error: ambiguous conversion
struct B { int n : a; };        // error: ambiguous conversion
```

— *end example*\]

A *converted constant expression* of type `T` is an expression,
implicitly converted to type `T`, where the converted expression is a
constant expression and the implicit conversion sequence contains only

- user-defined conversions,

- lvalue-to-rvalue conversions [conv.lval],

- array-to-pointer conversions [conv.array],

- function-to-pointer conversions [conv.func],

- qualification conversions [conv.qual],

- integral promotions [conv.prom],

- integral conversions [conv.integral] other than narrowing conversions
  [dcl.init.list],

- null pointer conversions [conv.ptr] from `std::nullptr_t`,

- null member pointer conversions [conv.mem] from `std::nullptr_t`, and

- function pointer conversions [conv.fctptr],

and where the reference binding (if any) binds directly.

\[*Note 4*: Such expressions can be used in `new` expressions
[expr.new], as case expressions [stmt.switch], as enumerator
initializers if the underlying type is fixed [dcl.enum], as array bounds
[dcl.array], and as non-type template arguments
[temp.arg]. — *end note*\]

A `bool}` is an expression, contextually converted to `bool` [conv],
where the converted expression is a constant expression and the
conversion sequence contains only the conversions above.

A *constant expression* is either a glvalue core constant expression
that refers to an entity that is a permitted result of a constant
expression (as defined below), or a prvalue core constant expression
whose value satisfies the following constraints:

- if the value is an object of class type, each non-static data member
  of reference type refers to an entity that is a permitted result of a
  constant expression,

- if the value is an object of scalar type, it does not have an
  indeterminate value [basic.indet],

- if the value is of pointer type, it contains the address of an object
  with static storage duration, the address past the end of such an
  object [expr.add], the address of a non-immediate function, or a null
  pointer value,

- if the value is of pointer-to-member-function type, it does not
  designate an immediate function, and

- if the value is an object of class or array type, each subobject
  satisfies these constraints for the value.

An entity is a *permitted result of a constant expression* if it is an
object with static storage duration that either is not a temporary
object or is a temporary object whose value satisfies the above
constraints, or if it is a non-immediate function.

\[*Note 5*: A glvalue core constant expression that either refers to or
points to an unspecified object is not a constant
expression. — *end note*\]

\[*Example 4*:

``` cpp
consteval int f() { return 42; }
consteval auto g() { return f; }
consteval int h(int (*p)() = g()) { return p(); }
constexpr int r = h();                          // OK
constexpr auto e = g();                         // error: a pointer to an immediate function is
                                                // not a permitted result of a constant expression
```

— *end example*\]

Implementations should provide consistent results of floating-point
evaluations, irrespective of whether the evaluation is performed during
translation or during program execution.

\[*Note 6*:

Since this document imposes no restrictions on the accuracy of
floating-point operations, it is unspecified whether the evaluation of a
floating-point expression during translation yields the same result as
the evaluation of the same expression (or the same operations on the
same values) during program execution.

— *end note*\]

An expression or conversion is in an *immediate function context* if it
is potentially evaluated and either:

- its innermost enclosing non-block scope is a function parameter scope
  of an immediate function,

- it is a subexpression of a manifestly constant-evaluated expression or
  conversion, or

- its enclosing statement is enclosed [stmt.pre] by the
  *compound-statement* of a consteval if statement [stmt.if].

An invocation is an *immediate invocation* if it is a
potentially-evaluated explicit or implicit invocation of an immediate
function and is not in an immediate function context. An aggregate
initialization is an immediate invocation if it evaluates a default
member initializer that has a subexpression that is an
immediate-escalating expression.

An expression or conversion is *immediate-escalating* if it is not
initially in an immediate function context and it is either

- a potentially-evaluated *id-expression* that denotes an immediate
  function that is not a subexpression of an immediate invocation, or

- an immediate invocation that is not a constant expression and is not a
  subexpression of an immediate invocation.

An *immediate-escalating* function is

- the call operator of a lambda that is not declared with the
  `consteval` specifier,

- a defaulted special member function that is not declared with the
  `consteval` specifier, or

- a function that results from the instantiation of a templated entity
  defined with the `constexpr` specifier.

An immediate-escalating expression shall appear only in an
immediate-escalating function.

An *immediate function* is a function or constructor that is

- declared with the `consteval` specifier, or

- an immediate-escalating function `F` whose function body contains an
  immediate-escalating expression `E` such that `E`’s innermost
  enclosing non-block scope is `F`’s function parameter scope.

\[*Example 5*:

``` cpp
consteval int id(int i) { return i; }
constexpr char id(char c) { return c; }

template<class T>
constexpr int f(T t) {
  return t + id(t);
}

auto a = &f<char>;              // OK, f<char> is not an immediate function
auto b = &f<int>;               // error: f<int> is an immediate function

static_assert(f(3) == 6);       // OK

template<class T>
constexpr int g(T t) {          // g<int> is not an immediate function
  return t + id(42);            // because id(42) is already a constant
}

template<class T, class F>
constexpr bool is_not(T t, F f) {
  return not f(t);
}

consteval bool is_even(int i) { return i % 2 == 0; }

static_assert(is_not(5, is_even));      // OK

int x = 0;

template<class T>
constexpr T h(T t = id(x)) {    // h<int> is not an immediate function
    return t;
}

template<class T>
constexpr T hh() {              // hh<int> is an immediate function
  return h<T>();
}

int i = hh<int>();              // error: hh<int>() is an immediate-escalating expression
                                // outside of an immediate-escalating function

struct A {
  int x;
  int y = id(x);
};

template<class T>
constexpr int k(int) {          // k<int> is not an immediate function because A(42) is a
  return A(42).y;               // constant expression and thus not immediate-escalating
}
```

— *end example*\]

An expression or conversion is *manifestly constant-evaluated* if it is:

- a *constant-expression*, or

- the condition of a constexpr if statement [stmt.if], or

- an immediate invocation, or

- the result of substitution into an atomic constraint expression to
  determine whether it is satisfied [temp.constr.atomic], or

- the initializer of a variable that is usable in constant expressions
  or has constant initialization [basic.start.static].

  \[*Example 9*:

  ``` cpp
  template<bool> struct X {};
  X<std::is_constant_evaluated()> x;                      // type X<true>
  int y;
  const int a = std::is_constant_evaluated() ? y : 1;     // dynamic initialization to 1
  double z[a];                                            // error: a is not usable
                                                          // in constant expressions
  const int b = std::is_constant_evaluated() ? 2 : y;     // static initialization to 2
  int c = y + (std::is_constant_evaluated() ? 2 : y);     // dynamic initialization to y+y

  constexpr int f() {
    const int n = std::is_constant_evaluated() ? 13 : 17; // n is 13
    int m = std::is_constant_evaluated() ? 13 : 17;       // m can be 13 or 17 (see below)
    char arr[n] = {}; // char[13]
    return m + sizeof(arr);
  }
  int p = f();                                            // m is 13; initialized to 26
  int q = p + f();                                        // m is 17 for this call; initialized to 56
  ```

  — *end example*\]

\[*Note 7*: A manifestly constant-evaluated expression is evaluated even
in an unevaluated operand [term.unevaluated.operand]. — *end note*\]

An expression or conversion is *potentially constant evaluated* if it
is:

- a manifestly constant-evaluated expression,

- a potentially-evaluated expression [basic.def.odr],

- an immediate subexpression of a *braced-init-list*,

- an expression of the form `&` *cast-expression* that occurs within a
  templated entity,

  or

- a potentially-evaluated subexpression [intro.execution] of one of the
  above.

A function or variable is *needed for constant evaluation* if it is:

- a constexpr function that is named by an expression [basic.def.odr]
  that is potentially constant evaluated, or

- a potentially-constant variable named by a potentially constant
  evaluated expression.

<!-- Link reference definitions -->
[\lastlibchapter]: #\lastlibchapter
[allocator.members]: mem.md#allocator.members
[basic.life]: basic.md#basic.life
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lval]: #basic.lval
[basic.type.qualifier]: basic.md#basic.type.qualifier
[class.access.base]: class.md#class.access.base
[class.base.init]: class.md#class.base.init
[class.cdtor]: class.md#class.cdtor
[class.conv]: class.md#class.conv
[class.conv.fct]: class.md#class.conv.fct
[class.dtor]: class.md#class.dtor
[class.member.lookup]: basic.md#class.member.lookup
[class.temporary]: basic.md#class.temporary
[conv]: #conv
[conv.bool]: #conv.bool
[conv.lval]: #conv.lval
[conv.ptr]: #conv.ptr
[cpp]: cpp.md#cpp
[dcl.array]: dcl.md#dcl.array
[dcl.attr.assume]: dcl.md#dcl.attr.assume
[dcl.decl]: dcl.md#dcl.decl
[dcl.fct.def.general]: dcl.md#dcl.fct.def.general
[dcl.init]: dcl.md#dcl.init
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[depr.capture.this]: future.md#depr.capture.this
[depr.volatile.type]: future.md#depr.volatile.type
[expr]: #expr
[expr.add]: #expr.add
[expr.ass]: #expr.ass
[expr.compound]: #expr.compound
[expr.context]: #expr.context
[expr.mptr.oper]: #expr.mptr.oper
[expr.post.incr]: #expr.post.incr
[expr.pre.incr]: #expr.pre.incr
[expr.prim.id.dtor]: #expr.prim.id.dtor
[expr.prop]: #expr.prop
[expr.ref]: #expr.ref
[expr.shift]: #expr.shift
[expr.type]: #expr.type
[expr.type.conv]: #expr.type.conv
[expr.unary]: #expr.unary
[implimits]: #implimits
[intro]: intro.md#intro
[intro.execution]: basic.md#intro.execution
[intro.memory]: basic.md#intro.memory
[lex.ext]: lex.md#lex.ext
[lex.literal]: lex.md#lex.literal
[library]: library.md#library
[new.delete.placement]: support.md#new.delete.placement
[over.built]: over.md#over.built
[over.literal]: over.md#over.literal
[over.match]: over.md#over.match
[over.match.oper]: over.md#over.match.oper
[over.oper]: over.md#over.oper
[over.over]: over.md#over.over
[temp.constr.constr]: temp.md#temp.constr.constr
[temp.names]: temp.md#temp.names
[term.object.representation]: #term.object.representation
[type.info]: support.md#type.info
