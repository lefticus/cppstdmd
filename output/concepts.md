---
current_file: concepts
label_index_file: converted/cppstdmd/output/cpp_std_labels.lua
---

# Concepts library <a id="concepts">[[concepts]]</a>

## General <a id="concepts.general">[[concepts.general]]</a>

This Clause describes library components that C++ programs may use to
perform compile-time validation of template arguments and perform
function dispatch based on properties of types. The purpose of these
concepts is to establish a foundation for equational reasoning in
programs.

The following subclauses describe language-related concepts, comparison
concepts, object concepts, and callable concepts as summarized in
[[concepts.summary]].

**Table: Fundamental concepts library summary**

| Subclause |  | Header |
| --- | --- | --- |
| [[concepts.equality]] | Equality preservation |
| [[concepts.lang]] | Language-related concepts | `<concepts>` |
| [[concepts.compare]] | Comparison concepts |
| [[concepts.object]] | Object concepts |
| [[concepts.callable]] | Callable concepts |

## Equality preservation <a id="concepts.equality">[[concepts.equality]]</a>

An expression is *equality-preserving* if, given equal inputs, the
expression results in equal outputs. The inputs to an expression are the
set of the expression’s operands. The output of an expression is the
expression’s result and all operands modified by the expression. For the
purposes of this subclause, the operands of an expression are the
largest subexpressions that include only:

- an *id-expression* [[expr.prim.id]], and

- invocations of the library function templates `std::move`,
  `std::forward`, and `std::declval` [[forward]], [[declval]].

\[*Example 1*: The operands of the expression `a = std::move(b)` are `a`
and `std::move(b)`. — *end example*\]

Not all input values need be valid for a given expression.

\[*Example 2*: For integers `a` and `b`, the expression `a / b` is not
well-defined when `b` is `0`. This does not preclude the expression
`a / b` being equality-preserving. — *end example*\]

The *domain* of an expression is the set of input values for which the
expression is required to be well-defined.

Expressions required to be equality-preserving are further required to
be stable: two evaluations of such an expression with the same input
objects are required to have equal outputs absent any explicit
intervening modification of those input objects.

\[*Note 1*: This requirement allows generic code to reason about the
current values of objects based on knowledge of the prior values as
observed via equality-preserving expressions. It effectively forbids
spontaneous changes to an object, changes to an object from another
thread of execution, changes to an object as side effects of
non-modifying expressions, and changes to an object as side effects of
modifying a distinct object if those changes could be observable to a
library function via an equality-preserving expression that is required
to be valid for that object. — *end note*\]

Expressions declared in a *requires-expression* in the library clauses
are required to be equality-preserving, except for those annotated with
the comment “not required to be equality-preserving.” An expression so
annotated may be equality-preserving, but is not required to be so.

An expression that may alter the value of one or more of its inputs in a
manner observable to equality-preserving expressions is said to modify
those inputs. The library clauses use a notational convention to specify
which expressions declared in a *requires-expression* modify which
inputs: except where otherwise specified, an expression operand that is
a non-constant lvalue or rvalue may be modified. Operands that are
constant lvalues or rvalues are required to not be modified. For the
purposes of this subclause, the cv-qualification and value category of
each operand are determined by assuming that each template type
parameter denotes a cv-unqualified complete non-array object type.

Where a *requires-expression* declares an expression that is
non-modifying for some constant lvalue operand, additional variations of
that expression that accept a non-constant lvalue or (possibly constant)
rvalue for the given operand are also required except where such an
expression variation is explicitly required with differing semantics.
These *implicit expression variations* are required to meet the semantic
requirements of the declared expression. The extent to which an
implementation validates the syntax of the variations is unspecified.

\[*Example 3*:

``` cpp
template<class T> concept C = requires(T a, T b, const T c, const T d) {
  c == d;           // \#1
  a = std::move(b); // \#2
  a = c;            // \#3
};
```

For the above example:

- Expression \#1 does not modify either of its operands, \#2 modifies
  both of its operands, and \#3 modifies only its first operand `a`.

- Expression \#1 implicitly requires additional expression variations
  that meet the requirements for `c == d` (including non-modification),
  as if the expressions

  \_\_CODEBLOCK_2\_\_

  had been declared as well.

- Expression \#3 implicitly requires additional expression variations
  that meet the requirements for `a = c` (including non-modification of
  the second operand), as if the expressions `a = b` and
  `a = std::move(c)` had been declared. Expression \#3 does not
  implicitly require an expression variation with a non-constant rvalue
  second operand, since expression \#2 already specifies exactly such an
  expression explicitly.

— *end example*\]

\[*Example 4*:

The following type `T` meets the explicitly stated syntactic
requirements of concept `C` above but does not meet the additional
implicit requirements:

``` cpp
struct T {
  bool operator==(const T&) const { return true; }
  bool operator==(T&) = delete;
};
```

`T` fails to meet the implicit requirements of `C`, so `T` satisfies but
does not model `C`. Since implementations are not required to validate
the syntax of implicit requirements, it is unspecified whether an
implementation diagnoses as ill-formed a program that requires `C<T>`.

— *end example*\]

## Header `<concepts>` synopsis <a id="concepts.syn">[[concepts.syn]]</a>

``` cpp
// all freestanding
namespace std {
  // [concepts.lang], language-related concepts
  // [concept.same], concept same_as
  template<class T, class U>
    concept same_as = see below;

  // [concept.derived], concept derived_from
  template<class Derived, class Base>
    concept derived_from = see below;

  // [concept.convertible], concept convertible_to
  template<class From, class To>
    concept convertible_to = see below;

  // [concept.commonref], concept common_reference_with
  template<class T, class U>
    concept common_reference_with = see below;

  // [concept.common], concept common_with
  template<class T, class U>
    concept common_with = see below;

  // [concepts.arithmetic], arithmetic concepts
  template<class T>
    concept integral = see below;
  template<class T>
    concept signed_integral = see below;
  template<class T>
    concept unsigned_integral = see below;
  template<class T>
    concept floating_point = see below;

  // [concept.assignable], concept assignable_from
  template<class LHS, class RHS>
    concept assignable_from = see below;

  // [concept.swappable], concept swappable
  namespace ranges {
    inline namespace unspecified {
      inline constexpr unspecified swap = unspecified;
    }
  }
  template<class T>
    concept swappable = see below;
  template<class T, class U>
    concept swappable_with = see below;

  // [concept.destructible], concept destructible
  template<class T>
    concept destructible = see below;

  // [concept.constructible], concept constructible_from
  template<class T, class... Args>
    concept constructible_from = see below;

  // [concept.default.init], concept default_initializable
  template<class T>
    concept default_initializable = see below;

  // [concept.moveconstructible], concept move_constructible
  template<class T>
    concept move_constructible = see below;

  // [concept.copyconstructible], concept copy_constructible
  template<class T>
    concept copy_constructible = see below;

  // [concepts.compare], comparison concepts
  // [concept.equalitycomparable], concept equality_comparable
  template<class T>
    concept equality_comparable = see below;
  template<class T, class U>
    concept equality_comparable_with = see below;

  // [concept.totallyordered], concept totally_ordered
  template<class T>
    concept totally_ordered = see below;
  template<class T, class U>
    concept totally_ordered_with = see below;

  // [concepts.object], object concepts
  template<class T>
    concept movable = see below;
  template<class T>
    concept copyable = see below;
  template<class T>
    concept semiregular = see below;
  template<class T>
    concept regular = see below;

  // [concepts.callable], callable concepts
  // [concept.invocable], concept invocable
  template<class F, class... Args>
    concept invocable = see below;

  // [concept.regularinvocable], concept regular_invocable
  template<class F, class... Args>
    concept regular_invocable = see below;

  // [concept.predicate], concept predicate
  template<class F, class... Args>
    concept predicate = see below;

  // [concept.relation], concept relation
  template<class R, class T, class U>
    concept relation = see below;

  // [concept.equiv], concept equivalence_relation
  template<class R, class T, class U>
    concept equivalence_relation = see below;

  // [concept.strictweakorder], concept strict_weak_order
  template<class R, class T, class U>
    concept strict_weak_order = see below;
}
```

## Language-related concepts <a id="concepts.lang">[[concepts.lang]]</a>

### General <a id="concepts.lang.general">[[concepts.lang.general]]</a>

Subclause [[concepts.lang]] contains the definition of concepts
corresponding to language features. These concepts express relationships
between types, type classifications, and fundamental type properties.

### Concept  <a id="concept.same">[[concept.same]]</a>

``` cpp
template<class T, class U>
  concept same-as-impl = is_same_v<T, U>;       // exposition only

template<class T, class U>
  concept same_as = same-as-impl<T, U> && same-as-impl<U, T>;
```

> \[*Note 1*: `same_as``<T, U>` subsumes `same_as``<U, T>` and vice
> versa. — *end note*\]

### Concept  <a id="concept.derived">[[concept.derived]]</a>

``` cpp
template<class Derived, class Base>
  concept derived_from =
    is_base_of_v<Base, Derived> &&
    is_convertible_v<const volatile Derived*, const volatile Base*>;
```

> \[*Note 2*: `derived_from``<Derived, Base>` is satisfied if and only
> if `Derived` is publicly and unambiguously derived from `Base`, or
> `Derived` and `Base` are the same class type ignoring
> cv-qualifiers. — *end note*\]

### Concept  <a id="concept.convertible">[[concept.convertible]]</a>

Given types `From` and `To` and an expression `E` whose type and value
category are the same as those of `declval<From>()`,
`convertible_to<From, To>` requires `E` to be both implicitly and
explicitly convertible to type `To`. The implicit and explicit
conversions are required to produce equal results.

``` cpp
template<class From, class To>
  concept convertible_to =
    is_convertible_v<From, To> &&
    requires {
      static_cast<To>(declval<From>());
    };
```

> Let `FromR` be `add_rvalue_reference_t<From>` and `test` be the
> invented function:
>
> ``` cpp
> To test(FromR (&f)()) {
>   return f();
> }
> ```
>
> and let `f` be a function with no arguments and return type `FromR`
> such that `f()` is equality-preserving. Types `From` and `To` model
> `convertible_to``<From, To>` only if:
>
> - `To` is not an object or reference-to-object type, or
>   `static_cast<To>(f())` is equal to `test(f)`.
>
> - `FromR` is not a reference-to-object type, or
>
>   - If `FromR` is an rvalue reference to a non const-qualified type,
>     the resulting state of the object referenced by `f()` after either
>     above expression is valid but unspecified\[lib.types.movedfrom\].
>
>   - Otherwise, the object referred to by `f()` is not modified by
>     either above expression.

### Concept  <a id="concept.commonref">[[concept.commonref]]</a>

For two types `T` and `U`, if `common_reference_t<T, U>` is well-formed
and denotes a type `C` such that both `convertible_to<T, C>` and
`convertible_to<U, C>` are modeled, then `T` and `U` share a
*common reference type*, `C`.

\[*Note 1*: `C` can be the same as `T` or `U`, or can be a different
type. `C` can be a reference type. — *end note*\]

``` cpp
template<class T, class U>
  concept common_reference_with =
    same_as<common_reference_t<T, U>, common_reference_t<U, T>> &&
    convertible_to<T, common_reference_t<T, U>> &&
    convertible_to<U, common_reference_t<T, U>>;
```

> Let `C` be `common_reference_t<T, U>`. Let `t1` and `t2` be
> equality-preserving expressions\[concepts.equality\] such that
> `decltype((t1))` and `decltype((t2))` are each `T`, and let `u1` and
> `u2` be equality-preserving expressions such that `decltype((u1))` and
> `decltype((u2))` are each `U`. `T` and `U` model
> `common_reference_with``<T, U>` only if:
>
> - `C(t1)` equals `C(t2)` if and only if `t1` equals `t2`, and
>
> - `C(u1)` equals `C(u2)` if and only if `u1` equals `u2`.
>
> \[*Note 3*: Users can customize the behavior of
> `common_reference_with` by specializing the `basic_common_reference`
> class template\[meta.trans.other\]. — *end note*\]

### Concept  <a id="concept.common">[[concept.common]]</a>

If `T` and `U` can both be explicitly converted to some third type, `C`,
then `T` and `U` share a *common type*, `C`.

\[*Note 2*: `C` can be the same as `T` or `U`, or can be a different
type. `C` is not necessarily unique. — *end note*\]

``` cpp
template<class T, class U>
  concept common_with =
    same_as<common_type_t<T, U>, common_type_t<U, T>> &&
    requires {
      static_cast<common_type_t<T, U>>(declval<T>());
      static_cast<common_type_t<T, U>>(declval<U>());
    } &&
    common_reference_with<
      add_lvalue_reference_t<const T>,
      add_lvalue_reference_t<const U>> &&
    common_reference_with<
      add_lvalue_reference_t<common_type_t<T, U>>,
      common_reference_t<
        add_lvalue_reference_t<const T>,
        add_lvalue_reference_t<const U>>>;
```

> Let `C` be `common_type_t<T, U>`. Let `t1` and `t2` be
> equality-preserving expressions\[concepts.equality\] such that
> `decltype((t1))` and `decltype((t2))` are each `T`, and let `u1` and
> `u2` be equality-preserving expressions such that `decltype((u1))` and
> `decltype((u2))` are each `U`. `T` and `U` model `common_with``<T, U>`
> only if:
>
> - `C(t1)` equals `C(t2)` if and only if `t1` equals `t2`, and
>
> - `C(u1)` equals `C(u2)` if and only if `u1` equals `u2`.
>
> \[*Note 4*: Users can customize the behavior of `common_with` by
> specializing the `common_type` class
> template\[meta.trans.other\]. — *end note*\]

### Arithmetic concepts <a id="concepts.arithmetic">[[concepts.arithmetic]]</a>

``` cpp
template<class T>
  concept integral = is_integral_v<T>;
template<class T>
  concept signed_integral = integral<T> && is_signed_v<T>;
template<class T>
  concept unsigned_integral = integral<T> && !signed_integral<T>;
template<class T>
  concept floating_point = is_floating_point_v<T>;
```

> \[*Note 5*: `signed_integral` can be modeled even by types that are
> not signed integer types\[basic.fundamental\]; for example,
> `char`. — *end note*\]
>
> \[*Note 6*: `unsigned_integral` can be modeled even by types that are
> not unsigned integer types\[basic.fundamental\]; for example,
> `bool`. — *end note*\]

### Concept  <a id="concept.assignable">[[concept.assignable]]</a>

``` cpp
template<class LHS, class RHS>
  concept assignable_from =
    is_lvalue_reference_v<LHS> &&
    common_reference_with<const remove_reference_t<LHS>&, const remove_reference_t<RHS>&> &&
    requires(LHS lhs, RHS&& rhs) {
      { lhs = std::forward<RHS>(rhs) } -> same_as<LHS>;
    };
```

> Let:
>
> - `lhs` be an lvalue that refers to an object `lcopy` such that
>   `decltype((lhs))` is `LHS`,
>
> - `rhs` be an expression such that `decltype((rhs))` is `RHS`, and
>
> - `rcopy` be a distinct object that is equal to `rhs`.
>
> `LHS` and `RHS` model `assignable_from``<LHS, RHS>` only if
>
> - `addressof(lhs = rhs) == addressof(lcopy)`.
>
> - After evaluating `lhs = rhs`:
>
>   - `lhs` is equal to `rcopy`, unless `rhs` is a non-const xvalue that
>     refers to `lcopy`.
>
>   - If `rhs` is a non- xvalue, the resulting state of the object to
>     which it refers is valid but unspecified\[lib.types.movedfrom\].
>
>   - Otherwise, if `rhs` is a glvalue, the object to which it refers is
>     not modified.
>
> \[*Note 7*: Assignment need not be a total
> function\[structure.requirements\]; in particular, if assignment to an
> object `x` can result in a modification of some other object `y`, then
> `x = y` is likely not in the domain of `=`. — *end note*\]

### Concept  <a id="concept.swappable">[[concept.swappable]]</a>

Let `t1` and `t2` be equality-preserving expressions that denote
distinct equal objects of type `T`, and let `u1` and `u2` similarly
denote distinct equal objects of type `U`.

\[*Note 3*: `t1` and `u1` can denote distinct objects, or the same
object. — *end note*\]

An operation *exchanges the values* denoted by `t1` and `u1` if and only
if the operation modifies neither `t2` nor `u2` and:

- If `T` and `U` are the same type, the result of the operation is that
  `t1` equals `u2` and `u1` equals `t2`.

- If `T` and `U` are different types and
  `common_reference_with<decltype((t1)), decltype((u1))>` is modeled,
  the result of the operation is that `C(t1)` equals `C(u2)` and `C(u1)`
  equals `C(t2)` where `C` is
  `common_reference_t<decltype((t1)), decltype((u1))>`.

The name `ranges::swap` denotes a customization point object
[[customization.point.object]]. The expression `ranges::swap(E1, E2)`
for subexpressions `E1` and `E2` is expression-equivalent to an
expression `S` determined as follows:

- `S` is `(void)swap(E1, E2)`

  if `E1` or `E2` has class or enumeration type [[basic.compound]] and
  that expression is valid, with overload resolution performed in a
  context that includes the declaration

  ``` cpp
  template<class T>
    void swap(T&, T&) = delete;
  ```

  and does not include a declaration of `ranges::swap`. If the function
  selected by overload resolution does not exchange the values denoted
  by `E1` and `E2`, the program is ill-formed, no diagnostic required.

  \[*Note 8*: This precludes calling unconstrained program-defined
  overloads of `swap`. When the deleted overload is viable,
  program-defined overloads need to be more specialized
  [[temp.func.order]] to be selected. — *end note*\]

- Otherwise, if `E1` and `E2` are lvalues of array types
  [[basic.compound]] with equal extent and `ranges::swap(*E1, *E2)` is a
  valid expression, `S` is `(void)ranges::swap_ranges(E1, E2)`, except
  that `noexcept(S)` is equal to `noexcept(ranges::swap(*E1, *E2))`.

- Otherwise, if `E1` and `E2` are lvalues of the same type `T` that
  models `move_constructible<T>` and `assignable_from<T&, T>`, `S` is an
  expression that exchanges the denoted values. `S` is a constant
  expression if

  - `T` is a literal type [[term.literal.type]],

  - both `E1 = std::move(E2)` and `E2 = std::move(E1)` are constant
    subexpressions [[defns.const.subexpr]], and

  - the full-expressions of the initializers in the declarations

    ``` cpp
    T t1(std::move(E1));
    T t2(std::move(E2));
    ```

    are constant subexpressions.

  `noexcept(S)` is equal to
  `is_nothrow_move_constructible_v<T> && is_nothrow_move_assignable_v<T>`.

- Otherwise, `ranges::swap(E1, E2)` is ill-formed.

  \[*Note 9*: This case can result in substitution failure when
  `ranges::swap(E1, E2)` appears in the immediate context of a template
  instantiation. — *end note*\]

\[*Note 4*: Whenever `ranges::swap(E1, E2)` is a valid expression, it
exchanges the values denoted by `E1` and `E2` and has type
`void`. — *end note*\]

``` cpp
template<class T>
  concept swappable = requires(T& a, T& b) { ranges::swap(a, b); };
```

``` cpp
template<class T, class U>
  concept swappable_with =
    common_reference_with<T, U> &&
    requires(T&& t, U&& u) {
      ranges::swap(std::forward<T>(t), std::forward<T>(t));
      ranges::swap(std::forward<U>(u), std::forward<U>(u));
      ranges::swap(std::forward<T>(t), std::forward<U>(u));
      ranges::swap(std::forward<U>(u), std::forward<T>(t));
    };
```

\[*Note 5*: The semantics of the `swappable` and `swappable_with`
concepts are fully defined by the `ranges::swap` customization point
object. — *end note*\]

\[*Example 1*:

User code can ensure that the evaluation of `swap` calls is performed in
an appropriate context under the various conditions as follows:

``` cpp
#include <cassert>
#include <concepts>
#include <utility>

namespace ranges = std::ranges;

template<class T, std::swappable_with<T> U>
void value_swap(T&& t, U&& u) {
  ranges::swap(std::forward<T>(t), std::forward<U>(u));
}

template<std::swappable T>
void lv_swap(T& t1, T& t2) {
  ranges::swap(t1, t2);
}

namespace N {
  struct A { int m; };
  struct Proxy {
    A* a;
    Proxy(A& a) : a{&a} {}
    friend void swap(Proxy x, Proxy y) {
      ranges::swap(*x.a, *y.a);
    }
  };
  Proxy proxy(A& a) { return Proxy{ a }; }
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

— *end example*\]

### Concept  <a id="concept.destructible">[[concept.destructible]]</a>

The `destructible` concept specifies properties of all types, instances
of which can be destroyed at the end of their lifetime, or reference
types.

``` cpp
template<class T>
  concept destructible = is_nothrow_destructible_v<T>;
```

> \[*Note 10*: Unlike the *Cpp17Destructible*
> requirements (\[cpp17.destructible\]), this concept forbids
> destructors that are potentially throwing, even if a particular
> invocation of the destructor does not actually throw. — *end note*\]

### Concept  <a id="concept.constructible">[[concept.constructible]]</a>

The `constructible_from` concept constrains the initialization of a
variable of a given type with a particular set of argument types.

``` cpp
template<class T, class... Args>
  concept constructible_from = destructible<T> && is_constructible_v<T, Args...>;
```

### Concept  <a id="concept.default.init">[[concept.default.init]]</a>

``` cpp
template<class T>
  constexpr bool is-default-initializable = see below;         // exposition only

template<class T>
  concept default_initializable = constructible_from<T> &&
                                  requires { T{}; } &&
                                  is-default-initializable<T>;
```

> For a type `T`, *`is-default-initializable`*`<T>` is `true` if and
> only if the variable definition
>
> ``` cpp
> T t;
> ```
>
> is well-formed for some invented variable `t`; otherwise it is
> `false`. Access checking is performed as if in a context unrelated to
> `T`. Only the validity of the immediate context of the variable
> initialization is considered.

### Concept  <a id="concept.moveconstructible">[[concept.moveconstructible]]</a>

``` cpp
template<class T>
  concept move_constructible = constructible_from<T, T> && convertible_to<T, T>;
```

> If `T` is an object type, then let `rv` be an rvalue of type `T` and
> `u2` a distinct object of type `T` equal to `rv`. `T` models
> `move_constructible` only if
>
> - After the definition `T u = rv;`, `u` is equal to `u2`.
>
> - `T(rv)` is equal to `u2`.
>
> - If `T` is not , `rv`’s resulting state is valid but
>   unspecified\[lib.types.movedfrom\]; otherwise, it is unchanged.

### Concept  <a id="concept.copyconstructible">[[concept.copyconstructible]]</a>

``` cpp
template<class T>
  concept copy_constructible =
    move_constructible<T> &&
    constructible_from<T, T&> && convertible_to<T&, T> &&
    constructible_from<T, const T&> && convertible_to<const T&, T> &&
    constructible_from<T, const T> && convertible_to<const T, T>;
```

> If `T` is an object type, then let `v` be an lvalue of type `T` or
> ` T` or an rvalue of type ` T`. `T` models `copy_constructible` only
> if
>
> - After the definition `T u = v;`, `u` is equal to
>   `v`\[concepts.equality\] and `v` is not modified.
>
> - `T(v)` is equal to `v` and does not modify `v`.

## Comparison concepts <a id="concepts.compare">[[concepts.compare]]</a>

### General <a id="concepts.compare.general">[[concepts.compare.general]]</a>

Subclause [[concepts.compare]] describes concepts that establish
relationships and orderings on values of possibly differing object
types.

Given an expression `E` and a type `C`, let `CONVERT_TO_LVALUE<C>(E)`
be:

- `static_cast<const C&>(as_const(E))` if that is a valid expression,
  and

- `static_cast<const C&>(std::move(E))` otherwise.

### Boolean testability <a id="concept.booleantestable">[[concept.booleantestable]]</a>

The exposition-only `boolean-testable` concept specifies the
requirements on expressions that are convertible to `bool` and for which
the logical operators
[[expr.log.and]], [[expr.log.or]], [[expr.unary.op]] have the
conventional semantics.

``` cpp
template<class T>
  concept boolean-testable-impl = convertible_to<T, bool>;  // exposition only
```

Let `e` be an expression such that `decltype((e))` is `T`. `T` models
`boolean-testable-impl` only if:

- either `remove_cvref_t<T>` is not a class type, or a search for the
  names `operator&&` and `operator||` in the scope of
  `remove_cvref_t<T>` finds nothing; and

- argument-dependent lookup [[basic.lookup.argdep]] for the names
  `operator&&` and `operator||` with `T` as the only argument type finds
  no disqualifying declaration (defined below).

A *disqualifying parameter* is a function parameter whose declared type
`P`

- is not dependent on a template parameter, and there exists an implicit
  conversion sequence [[over.best.ics]] from `e` to `P`; or

- is dependent on one or more template parameters, and either

  - `P` contains no template parameter that participates in template
    argument deduction [[temp.deduct.type]], or

  - template argument deduction using the rules for deducing template
    arguments in a function call [[temp.deduct.call]] and `e` as the
    argument succeeds.

A *key parameter* of a function template `D` is a function parameter of
type cv `X` or reference thereto, where `X` names a specialization of a
class template that has the same innermost enclosing non-inline
namespace as `D`, and `X` contains at least one template parameter that
participates in template argument deduction.

\[*Example 1*:

In

``` cpp
namespace Z {
  template<class> struct C {};
  template<class T>
    void operator&&(C<T> x, T y);
  template<class T>
    void operator||(C<type_identity_t<T>> x, T y);
}
```

the declaration of `Z::operator&&` contains one key parameter, `C<T> x`,
and the declaration of `Z::operator||` contains no key parameters.

— *end example*\]

A *disqualifying declaration* is

- a (non-template) function declaration that contains at least one
  disqualifying parameter; or

- a function template declaration that contains at least one
  disqualifying parameter, where

  - at least one disqualifying parameter is a key parameter; or

  - the declaration contains no key parameters; or

  - the declaration declares a function template to which no name is
    bound [[dcl.meaning]].

\[*Note 1*: The intention is to ensure that given two types `T1` and
`T2` that each model `boolean-testable-impl`, the `&&` and `||`
operators within the expressions `declval<T1>() && declval<T2>()` and
`declval<T1>() || declval<T2>()` resolve to the corresponding built-in
operators. — *end note*\]

``` cpp
template<class T>
  concept boolean-testable =                // exposition only
    boolean-testable-impl<T> && requires(T&& t) {
      { !std::forward<T>(t) } -> boolean-testable-impl;
    };
```

Let `e` be an expression such that `decltype((e))` is `T`. `T` models
`boolean-testable` only if `bool(e) == !bool(!e)`.

\[*Example 2*: The types `bool`, `true_type` [[meta.type.synop]],
`int*`, and `bitset<N>::reference` [[template.bitset]] model
`boolean-testable`. — *end example*\]

### Comparison common types <a id="concept.comparisoncommontype">[[concept.comparisoncommontype]]</a>

``` cpp
template<class T, class U, class C = common_reference_t<const T&, const U&>>
  concept comparison-common-type-with-impl =   // exposition only
    same_as<common_reference_t<const T&, const U&>,
            common_reference_t<const U&, const T&>> &&
    requires {
      requires convertible_to<const T&, const C&> || convertible_to<T, const C&>;
      requires convertible_to<const U&, const C&> || convertible_to<U, const C&>;
    };

template<class T, class U>
  concept comparison-common-type-with =   // exposition only
    comparison-common-type-with-impl<remove_cvref_t<T>, remove_cvref_t<U>>;
```

Let `C` be `common_reference_t<const T&, const U&>`. Let `t1` and `t2`
be equality-preserving expressions that are lvalues of type
`remove_cvref_t<T>`, and let `u1` and `u2` be equality-preserving
expressions that are lvalues of type `remove_cvref_t<U>`. `T` and `U`
model `comparison-common-type-with<T, U>` only if:

- `CONVERT_TO_LVALUE<C>(t1)` equals `CONVERT_TO_LVALUE<C>(t2)` if and
  only if `t1` equals `t2`, and

- `CONVERT_TO_LVALUE<C>(u1)` equals `CONVERT_TO_LVALUE<C>(u2)` if and
  only if `u1` equals `u2`

### Concept  <a id="concept.equalitycomparable">[[concept.equalitycomparable]]</a>

``` cpp
template<class T, class U>
  concept weakly-equality-comparable-with = // exposition only
    requires(const remove_reference_t<T>& t,
             const remove_reference_t<U>& u) {
      { t == u } -> boolean-testable;
      { t != u } -> boolean-testable;
      { u == t } -> boolean-testable;
      { u != t } -> boolean-testable;
    };
```

> Given types `T` and `U`, let `t` and `u` be lvalues of types
> `const remove_reference_t<T>` and `const remove_reference_t<U>`
> respectively. `T` and `U` model
> `weakly-equality-comparable-with``<T, U>` only if
>
> - `t == u`, `u == t`, `t != u`, and `u != t` have the same domain.
>
> - `bool(u == t) == bool(t == u)`.
>
> - `bool(t != u) == !bool(t == u)`.
>
> - `bool(u != t) == bool(t != u)`.

``` cpp
template<class T>
  concept equality_comparable = weakly-equality-comparable-with<T, T>;
```

> Let `a` and `b` be objects of type `T`. `T` models
> `equality_comparable` only if `bool(a == b)` is `true` when `a` is
> equal to `b`\[concepts.equality\], and `false` otherwise.
>
> \[*Note 11*: The requirement that the expression `a == b` is
> equality-preserving implies that `==` is transitive and
> symmetric. — *end note*\]

``` cpp
template<class T, class U>
  concept equality_comparable_with =
    equality_comparable<T> && equality_comparable<U> &&
    comparison-common-type-with<T, U> &&
    equality_comparable<
      common_reference_t<
        const remove_reference_t<T>&,
        const remove_reference_t<U>&>> &&
    weakly-equality-comparable-with<T, U>;
```

> Given types `T` and `U`, let `t` and `t2` be lvalues denoting distinct
> equal objects of types `const remove_reference_t<T>` and
> `remove_cvref_t<T>`, respectively, let `u` and `u2` be lvalues
> denoting distinct equal objects of types `const remove_reference_t<U>`
> and `remove_cvref_t<U>`, respectively, and let `C` be:
>
> ``` cpp
> common_reference_t<const remove_reference_t<T>&, const remove_reference_t<U>&>
> ```
>
> `T` and `U` model `equality_comparable_with``<T, U>` only if
>
> ``` cpp
> bool(t == u) == bool(CONVERT_TO_LVALUE<C>(t2) == CONVERT_TO_LVALUE<C>(u2))
> ```

### Concept  <a id="concept.totallyordered">[[concept.totallyordered]]</a>

``` cpp
template<class T>
  concept totally_ordered =
    equality_comparable<T> && partially-ordered-with<T, T>;
```

> Given a type `T`, let `a`, `b`, and `c` be lvalues of type
> `const remove_reference_t<T>`. `T` models `totally_ordered` only if
>
> - Exactly one of `bool(a < b)`, `bool(a > b)`, or `bool(a == b)` is
>   `true`.
>
> - If `bool(a < b)` and `bool(b < c)`, then `bool(a < c)`.
>
> - `bool(a <= b) == !bool(b < a)`.
>
> - `bool(a >= b) == !bool(a < b)`.

``` cpp
template<class T, class U>
  concept totally_ordered_with =
    totally_ordered<T> && totally_ordered<U> &&
    equality_comparable_with<T, U> &&
    totally_ordered<
      common_reference_t<
        const remove_reference_t<T>&,
        const remove_reference_t<U>&>> &&
    partially-ordered-with<T, U>;
```

> Given types `T` and `U`, let `t` and `t2` be lvalues denoting distinct
> equal objects of types `const remove_reference_t<T>` and
> `remove_cvref_t<T>`, respectively, let `u` and `u2` be lvalues
> denoting distinct equal objects of types `const remove_reference_t<U>`
> and `remove_cvref_t<U>`, respectively, and let `C` be:
>
> ``` cpp
> common_reference_t<const remove_reference_t<T>&, const remove_reference_t<U>&>
> ```
>
> `T` and `U` model `totally_ordered_with``<T, U>` only if
>
> - `bool(t < u) == bool(`*`CONVERT_TO_LVALUE`*`<C>(t2) < `*`CONVERT_TO_LVALUE`*`<C>(u2))`.
>
> - `bool(t > u) == bool(`*`CONVERT_TO_LVALUE`*`<C>(t2) > `*`CONVERT_TO_LVALUE`*`<C>(u2))`.
>
> - `bool(t <= u) == bool(`*`CONVERT_TO_LVALUE`*`<C>(t2) <= `*`CONVERT_TO_LVALUE`*`<C>(u2))`.
>
> - `bool(t >= u) == bool(`*`CONVERT_TO_LVALUE`*`<C>(t2) >= `*`CONVERT_TO_LVALUE`*`<C>(u2))`.
>
> - `bool(u < t) == bool(`*`CONVERT_TO_LVALUE`*`<C>(u2) < `*`CONVERT_TO_LVALUE`*`<C>(t2))`.
>
> - `bool(u > t) == bool(`*`CONVERT_TO_LVALUE`*`<C>(u2) > `*`CONVERT_TO_LVALUE`*`<C>(t2))`.
>
> - `bool(u <= t) == bool(`*`CONVERT_TO_LVALUE`*`<C>(u2) <= `*`CONVERT_TO_LVALUE`*`<C>(t2))`.
>
> - `bool(u >= t) == bool(`*`CONVERT_TO_LVALUE`*`<C>(u2) >= `*`CONVERT_TO_LVALUE`*`<C>(t2))`.

## Object concepts <a id="concepts.object">[[concepts.object]]</a>

This subclause describes concepts that specify the basis of the
value-oriented programming style on which the library is based.

``` cpp
template<class T>
  concept movable = is_object_v<T> && move_constructible<T> &&
                    assignable_from<T&, T> && swappable<T>;
template<class T>
  concept copyable = copy_constructible<T> && movable<T> && assignable_from<T&, T&> &&
                     assignable_from<T&, const T&> && assignable_from<T&, const T>;
template<class T>
  concept semiregular = copyable<T> && default_initializable<T>;
template<class T>
  concept regular = semiregular<T> && equality_comparable<T>;
```

> \[*Note 12*: The `semiregular` concept is modeled by types that behave
> similarly to fundamental types like `int`, except that they need not
> be comparable with `==`. — *end note*\]
>
> \[*Note 13*: The `regular` concept is modeled by types that behave
> similarly to fundamental types like `int` and that are comparable with
> `==`. — *end note*\]

## Callable concepts <a id="concepts.callable">[[concepts.callable]]</a>

### General <a id="concepts.callable.general">[[concepts.callable.general]]</a>

The concepts in subclause [[concepts.callable]] describe the
requirements on function objects [[function.objects]] and their
arguments.

### Concept  <a id="concept.invocable">[[concept.invocable]]</a>

The `invocable` concept specifies a relationship between a callable type
[[func.def]] `F` and a set of argument types `Args...` which can be
evaluated by the library function `invoke` [[func.invoke]].

``` cpp
template<class F, class... Args>
  concept invocable = requires(F&& f, Args&&... args) {
    invoke(std::forward<F>(f), std::forward<Args>(args)...); // not required to be equality-preserving
  };
```

> \[*Example 1*: A function that generates random numbers can model
> `invocable`, since the `invoke` function call expression is not
> required to be
> equality-preserving\[concepts.equality\]. — *end example*\]

### Concept  <a id="concept.regularinvocable">[[concept.regularinvocable]]</a>

``` cpp
template<class F, class... Args>
  concept regular_invocable = invocable<F, Args...>;
```

> The `invoke` function call expression shall be
> equality-preserving\[concepts.equality\] and shall not modify the
> function object or the arguments.
>
> \[*Note 14*: This requirement supersedes the annotation in the
> definition of `invocable`. — *end note*\]
>
> \[*Example 2*: A random number generator does not model
> `regular_invocable`. — *end example*\]
>
> \[*Note 15*: The distinction between `invocable` and
> `regular_invocable` is purely semantic. — *end note*\]

### Concept  <a id="concept.predicate">[[concept.predicate]]</a>

``` cpp
template<class F, class... Args>
  concept predicate =
    regular_invocable<F, Args...> && boolean-testable<invoke_result_t<F, Args...>>;
```

### Concept  <a id="concept.relation">[[concept.relation]]</a>

``` cpp
template<class R, class T, class U>
  concept relation =
    predicate<R, T, T> && predicate<R, U, U> &&
    predicate<R, T, U> && predicate<R, U, T>;
```

### Concept  <a id="concept.equiv">[[concept.equiv]]</a>

``` cpp
template<class R, class T, class U>
  concept equivalence_relation = relation<R, T, U>;
```

> A `relation` models `equivalence_relation` only if it imposes an
> equivalence relation on its arguments.

### Concept  <a id="concept.strictweakorder">[[concept.strictweakorder]]</a>

``` cpp
template<class R, class T, class U>
  concept strict_weak_order = relation<R, T, U>;
```

> A `relation` models `strict_weak_order` only if it imposes a on its
> arguments.
>
> The term refers to the requirement of an irreflexive relation
> (`!comp(x, x)` for all `x`), and the term to requirements that are not
> as strong as those for a total ordering, but stronger than those for a
> partial ordering. If we define `equiv(a, b)` as
> `!comp(a, b) && !comp(b, a)`, then the requirements are that `comp`
> and `equiv` both be transitive relations:
>
> - `comp(a, b) && comp(b, c)` implies `comp(a, c)`
>
> - `equiv(a, b) && equiv(b, c)` implies `equiv(a, c)`
>
> \[*Note 16*:
>
> Under these conditions, it can be shown that
>
> - `equiv` is an equivalence relation,
>
> - `comp` induces a well-defined relation on the equivalence classes
>   determined by `equiv`, and
>
> - the induced relation is a strict total ordering.
>
> — *end note*\]

<!-- Link reference definitions -->
[basic.compound]: basic.md#basic.compound
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[concepts.callable]: #concepts.callable
[concepts.compare]: #concepts.compare
[concepts.lang]: #concepts.lang
[concepts.summary]: #concepts.summary
[customization.point.object]: library.md#customization.point.object
[dcl.meaning]: dcl.md#dcl.meaning
[declval]: utilities.md#declval
[defns.const.subexpr]: #defns.const.subexpr
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.prim.id]: expr.md#expr.prim.id
[expr.unary.op]: expr.md#expr.unary.op
[forward]: utilities.md#forward
[func.def]: utilities.md#func.def
[func.invoke]: utilities.md#func.invoke
[function.objects]: utilities.md#function.objects
[meta.type.synop]: meta.md#meta.type.synop
[over.best.ics]: over.md#over.best.ics
[temp.deduct.call]: temp.md#temp.deduct.call
[temp.deduct.type]: temp.md#temp.deduct.type
[temp.func.order]: temp.md#temp.func.order
[template.bitset]: utilities.md#template.bitset
[term.literal.type]: #term.literal.type

<!-- Link reference definitions -->
[concepts.callable]: #concepts.callable
[concepts.compare]: #concepts.compare
[concepts.equality]: #concepts.equality
[concepts.lang]: #concepts.lang
[concepts.object]: #concepts.object
