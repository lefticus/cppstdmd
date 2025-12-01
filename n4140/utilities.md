# General utilities library <a id="utilities">[[utilities]]</a>

## General <a id="utilities.general">[[utilities.general]]</a>

This Clause describes utilities that are generally useful in
C++programs; some of these utilities are used by other elements of the
C++standard library. These utilities are summarized in Table 
[[tab:util.lib.summary]].

**Table: General utilities library summary** <a id="tab:util.lib.summary">[tab:util.lib.summary]</a>

| Subclause             |                                  | Header               |
| --------------------- | -------------------------------- | -------------------- |
| [[utility]]           | Utility components               | `<utility>`          |
| [[pairs]]             | Pairs                            | `<utility>`          |
| [[tuple]]             | Tuples                           | `<tuple>`            |
| [[intseq]]            | Compile-time integer sequences   | `<utility>`          |
| [[template.bitset]]   | Fixed-size sequences of bits     | `<bitset>`           |
|                       |                                  | `<memory>`           |
| [[memory]]            | Memory                           | `<cstdlib>`          |
|                       |                                  | `<cstring>`          |
| [[smartptr]]          | Smart pointers                   | `<memory>`           |
| [[function.objects]]  | Function objects                 | `<functional>`       |
| [[meta]]              | Type traits                      | `<type_traits>`      |
| [[ratio]]             | Compile-time rational arithmetic | `<ratio>`            |
| [[time]]              | Time utilities                   | `<chrono>`           |
|                       |                                  | `<ctime>`            |
| [[allocator.adaptor]] | Scoped allocators                | `<scoped_allocator>` |
| [[type.index]]        | Type indexes                     | `<typeindex>`        |


## Utility components <a id="utility">[[utility]]</a>

This subclause contains some basic function and class templates that are
used throughout the rest of the library.

\synopsis{Header \texttt{\<utility\>} synopsis}

The header `<utility>` defines several types and function templates that
are described in this Clause. It also defines the template `pair` and
various function templates that operate on `pair` objects.

``` cpp
#include <initializer_list>

namespace std {
  // [operators], operators:
  namespace rel_ops {
    template<class T> bool operator!=(const T&, const T&);
    template<class T> bool operator> (const T&, const T&);
    template<class T> bool operator<=(const T&, const T&);
    template<class T> bool operator>=(const T&, const T&);
  }

  // [utility.swap], swap:
  template<class T> void swap(T& a, T& b) noexcept(see below);
  template <class T, size_t N> void swap(T (&a)[N], T (&b)[N]) noexcept(noexcept(swap(*a, *b)));

  // [utility.exchange], exchange:
  template <class T, class U=T> T exchange(T& obj, U&& new_val);

  // [forward], forward/move:
  template <class T>
    constexpr T&& forward(remove_reference_t<T>& t) noexcept;
  template <class T>
    constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
  template <class T>
    constexpr remove_reference_t<T>&& move(T&&) noexcept;
  template <class T>
    constexpr conditional_t<
    !is_nothrow_move_constructible<T>::value && is_copy_constructible<T>::value,
    const T&, T&&> move_if_noexcept(T& x) noexcept;

  // [declval], declval:
  template <class T>
    add_rvalue_reference_t<T> declval() noexcept;  // as unevaluated operand

  // [pairs], pairs:
  template <class T1, class T2> struct pair;

  // [pairs.spec], pair specialized algorithms:
  template <class T1, class T2>
    constexpr bool operator==(const pair<T1,T2>&, const pair<T1,T2>&);
  template <class T1, class T2>
    constexpr bool operator< (const pair<T1,T2>&, const pair<T1,T2>&);
  template <class T1, class T2>
    constexpr bool operator!=(const pair<T1,T2>&, const pair<T1,T2>&);
  template <class T1, class T2>
    constexpr bool operator> (const pair<T1,T2>&, const pair<T1,T2>&);
  template <class T1, class T2>
    constexpr bool operator>=(const pair<T1,T2>&, const pair<T1,T2>&);
  template <class T1, class T2>
    constexpr bool operator<=(const pair<T1,T2>&, const pair<T1,T2>&);
  template <class T1, class T2>
    void swap(pair<T1,T2>& x, pair<T1,T2>& y) noexcept(noexcept(x.swap(y)));
  template <class T1, class T2>
    constexpr see below make_pair(T1&&, T2&&);

  // [pair.astuple], tuple-like access to pair:
  template <class T> class tuple_size;
  template <size_t I, class T> class tuple_element;

  template <class T1, class T2> struct tuple_size<pair<T1, T2> >;
  template <class T1, class T2> struct tuple_element<0, pair<T1, T2> >;
  template <class T1, class T2> struct tuple_element<1, pair<T1, T2> >;

  template<size_t I, class T1, class T2>
    constexpr tuple_element_t<I, pair<T1, T2>>&
      get(pair<T1, T2>&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr tuple_element_t<I, pair<T1, T2>>&&
      get(pair<T1, T2>&&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr const tuple_element_t<I, pair<T1, T2>>&
      get(const pair<T1, T2>&) noexcept;
  template <class T, class U>
    constexpr T& get(pair<T, U>& p) noexcept;
  template <class T, class U>
    constexpr const T& get(const pair<T, U>& p) noexcept;
  template <class T, class U>
    constexpr T&& get(pair<T, U>&& p) noexcept;
  template <class T, class U>
    constexpr T& get(pair<U, T>& p) noexcept;
  template <class T, class U>
    constexpr const T& get(const pair<U, T>& p) noexcept;
  template <class T, class U>
    constexpr T&& get(pair<U, T>&& p) noexcept;

  // [pair.piecewise], pair piecewise construction
  struct piecewise_construct_t { };
  constexpr piecewise_construct_t piecewise_construct{};
  template <class... Types> class tuple;  // defined in <tuple>


  // [intseq], Compile-time integer sequences
  template<class T, T...> struct integer_sequence;
  template<size_t... I>
    using index_sequence = integer_sequence<size_t, I...>;

  template<class T, T N>
    using make_integer_sequence = integer_sequence<T, see below{}>;
  template<size_t N>
    using make_index_sequence = make_integer_sequence<size_t, N>;

  template<class... T>
    using index_sequence_for = make_index_sequence<sizeof...(T)>;
}
```

### Operators <a id="operators">[[operators]]</a>

To avoid redundant definitions of `operator!=` out of `operator==` and
operators `>`, `<=`, and `>=` out of `operator<`, the library provides
the following:

``` cpp
template <class T> bool operator!=(const T& x, const T& y);
```

*Requires:* Type `T` is `EqualityComparable`
(Table  [[equalitycomparable]]).

*Returns:* `!(x == y)`.

``` cpp
template <class T> bool operator>(const T& x, const T& y);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[lessthancomparable]]).

*Returns:* `y < x`.

``` cpp
template <class T> bool operator<=(const T& x, const T& y);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[lessthancomparable]]).

*Returns:* `!(y < x)`.

``` cpp
template <class T> bool operator>=(const T& x, const T& y);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[lessthancomparable]]).

*Returns:* `!(x < y)`.

In this library, whenever a declaration is provided for an `operator!=`,
`operator>`, `operator>=`, or `operator<=`, and requirements and
semantics are not explicitly provided, the requirements and semantics
are as specified in this Clause.

### swap <a id="utility.swap">[[utility.swap]]</a>

``` cpp
template<class T> void swap(T& a, T& b) noexcept(see below);
```

The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_move_constructible<T>::value &&
is_nothrow_move_assignable<T>::value
```

*Requires:* Type `T` shall be `MoveConstructible`
(Table  [[moveconstructible]]) and `MoveAssignable`
(Table  [[moveassignable]]).

*Effects:* Exchanges values stored in two locations.

``` cpp
template<class T, size_t N>
  void swap(T (&a)[N], T (&b)[N]) noexcept(noexcept(swap(*a, *b)));
```

*Requires:* `a[i]` shall be swappable with ([[swappable.requirements]])
`b[i]` for all `i` in the range \[`0`, `N`).

*Effects:* `swap_ranges(a, a + N, b)`

### exchange <a id="utility.exchange">[[utility.exchange]]</a>

``` cpp
template <class T, class U=T> T exchange(T& obj, U&& new_val);
```

*Effects:* Equivalent to:

``` cpp
T old_val = std::move(obj);
obj = std::forward<U>(new_val);
return old_val;
```

### forward/move helpers <a id="forward">[[forward]]</a>

The library provides templated helper functions to simplify applying
move semantics to an lvalue and to simplify the implementation of
forwarding functions.

``` cpp
template <class T> constexpr T&& forward(remove_reference_t<T>& t) noexcept;
template <class T> constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
```

*Returns:* `static_cast<T&&>(t)`.

If the second form is instantiated with an lvalue reference type, the
program is ill-formed.

``` cpp
template <class T, class A1, class A2>
shared_ptr<T> factory(A1&& a1, A2&& a2) {
  return shared_ptr<T>(new T(std::forward<A1>(a1), std::forward<A2>(a2)));
}

struct A {
  A(int&, const double&);
};

void g() {
  shared_ptr<A> sp1 = factory<A>(2, 1.414); // error: 2 will not bind to int&
  int i = 2;
  shared_ptr<A> sp2 = factory<A>(i, 1.414); // OK
}
```

In the first call to `factory`, `A1` is deduced as `int`, so 2 is
forwarded to `A`’s constructor as an rvalue. In the second call to
`factory`, `A1` is deduced as `int&`, so `i` is forwarded to `A`’s
constructor as an lvalue. In both cases, `A2` is deduced as `double`, so
1.414 is forwarded to `A`’s constructor as an rvalue.

``` cpp
template <class T> constexpr remove_reference_t<T>&& move(T&& t) noexcept;
```

*Returns:* `static_cast<remove_reference_t<T>&&>(t)`.

``` cpp
template <class T, class A1>
shared_ptr<T> factory(A1&& a1) {
  return shared_ptr<T>(new T(std::forward<A1>(a1)));
}

struct A {
  A();
  A(const A&);  // copies from lvalues
  A(A&&);       // moves from rvalues
};

void g() {
  A a;
  shared_ptr<A> sp1 = factory<A>(a);              // ``a'' binds to A(const A&)
  shared_ptr<A> sp1 = factory<A>(std::move(a));   // ``a'' binds to A(A&&)
}
```

In the first call to `factory`, `A1` is deduced as `A&`, so `a` is
forwarded as a non-const lvalue. This binds to the constructor
`A(const A&)`, which copies the value from `a`. In the second call to
`factory`, because of the call `std::move(a)`, `A1` is deduced as `A`,
so `a` is forwarded as an rvalue. This binds to the constructor
`A(A&&)`, which moves the value from `a`.

``` cpp
template <class T> constexpr conditional_t<
  !is_nothrow_move_constructible<T>::value && is_copy_constructible<T>::value,
  const T&, T&&> move_if_noexcept(T& x) noexcept;
```

*Returns:* `std::move(x)`

### Function template `declval` <a id="declval">[[declval]]</a>

The library provides the function template `declval` to simplify the
definition of expressions which occur as unevaluated operands (Clause 
[[expr]]).

``` cpp
template <class T>
  add_rvalue_reference_t<T> declval() noexcept;  // as unevaluated operand
```

*Remarks:* If this function is odr-used ([[basic.def.odr]]), the
program is ill-formed.

*Remarks:* The template parameter `T` of `declval` may be an incomplete
type.

``` cpp
template <class To, class From>
  decltype(static_cast<To>(declval<From>())) convert(From&&);
```

declares a function template `convert` which only participates in
overloading if the type `From` can be explicitly converted to type `To`.
For another example see class template
`common_type` ([[meta.trans.other]]).

## Pairs <a id="pairs">[[pairs]]</a>

### In general <a id="pairs.general">[[pairs.general]]</a>

The library provides a template for heterogeneous pairs of values. The
library also provides a matching function template to simplify their
construction and several templates that provide access to `pair` objects
as if they were `tuple` objects (see  [[tuple.helper]] and 
[[tuple.elem]]).

### Class template `pair` <a id="pairs.pair">[[pairs.pair]]</a>

``` cpp
// defined in header <utility>

namespace std {
  template <class T1, class T2>
  struct pair {
    typedef T1 first_type;
    typedef T2 second_type;

    T1 first;
    T2 second;
    pair(const pair&) = default;
    pair(pair&&) = default;
    constexpr pair();
    constexpr pair(const T1& x, const T2& y);
    template<class U, class V> constexpr pair(U&& x, V&& y);
    template<class U, class V> constexpr pair(const pair<U, V>& p);
    template<class U, class V> constexpr pair(pair<U, V>&& p);
    template <class... Args1, class... Args2>
      pair(piecewise_construct_t,
           tuple<Args1...> first_args, tuple<Args2...> second_args);

    pair& operator=(const pair& p);
    template<class U, class V> pair& operator=(const pair<U, V>& p);
    pair& operator=(pair&& p) noexcept(see below);
    template<class U, class V> pair& operator=(pair<U, V>&& p);

    void swap(pair& p) noexcept(see below);
  };
}
```

Constructors and member functions of `pair` shall not throw exceptions
unless one of the element-wise operations specified to be called for
that operation throws an exception.

The defaulted move and copy constructor, respectively, of pair shall be
a `constexpr` function if and only if all required element-wise
initializations for copy and move, respectively, would satisfy the
requirements for a `constexpr` function.

``` cpp
constexpr pair();
```

*Requires:* `is_default_constructible<first_type>::value` is `true` and
`is_default_construct-`  
`ible<second_type>::value` is `true`.

*Effects:* Value-initializes `first` and `second`.

``` cpp
constexpr pair(const T1& x, const T2& y);
```

*Requires:* `is_copy_constructible<first_type>::value` is `true` and
`is_copy_constructible<second_type>::value` is `true`.

*Effects:* The constructor initializes `first` with `x` and `second`
with `y`.

``` cpp
template<class U, class V> constexpr pair(U&& x, V&& y);
```

*Requires:* `is_constructible<first_type, U&&>::value` is `true` and
`is_constructible<second_type, V&&>::value` is `true`.

*Effects:* The constructor initializes `first` with `std::forward<U>(x)`
and `second` with `std::forward<V>(y)`.

*Remarks:* If `U` is not implicitly convertible to `first_type` or `V`
is not implicitly convertible to `second_type` this constructor shall
not participate in overload resolution.

``` cpp
template<class U, class V> constexpr pair(const pair<U, V>& p);
```

*Requires:* `is_constructible<first_type, const U&>::value` is `true`
and `is_constructible<second_type, const V&>::value` is `true`.

*Effects:* Initializes members from the corresponding members of the
argument.

This constructor shall not participate in overload resolution unless
`const U&` is implicitly convertible to `first_type` and `const V&` is
implicitly convertible to `second_type`.

``` cpp
template<class U, class V> constexpr pair(pair<U, V>&& p);
```

*Requires:* `is_constructible<first_type, U&&>::value` is `true` and
`is_constructible<second_type, V&&>::value` is `true`.

*Effects:* The constructor initializes `first` with
`std::forward<U>(p.first)` and `second` with
`std::forward<V>(p.second)`.

This constructor shall not participate in overload resolution unless `U`
is implicitly convertible to `first_type` and `V` is implicitly
convertible to `second_type`.

``` cpp
template<class... Args1, class... Args2>
  pair(piecewise_construct_t,
       tuple<Args1...> first_args, tuple<Args2...> second_args);
```

*Requires:* `is_constructible<first_type, Args1&&...>::value` is `true`
and `is_constructible<second_type, Args2&&...>::value` is `true`.

*Effects:* The constructor initializes `first` with arguments of types
`Args1...` obtained by forwarding the elements of `first_args` and
initializes `second` with arguments of types `Args2...` obtained by
forwarding the elements of `second_args`. (Here, forwarding an element
`x` of type `U` within a `tuple` object means calling
`std::forward<U>(x)`.) This form of construction, whereby constructor
arguments for `first` and `second` are each provided in a separate
`tuple` object, is called *piecewise construction*.

``` cpp
pair& operator=(const pair& p);
```

*Requires:* `is_copy_assignable<first_type>::value` is `true` and
`is_copy_assignable<second_type>::value` is `true`.

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

``` cpp
template<class U, class V> pair& operator=(const pair<U, V>& p);
```

*Requires:* `is_assignable<first_type&, const U&>::value` is `true` and
`is_assignable<second_type&, const V&>::value` is `true`.

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

``` cpp
pair& operator=(pair&& p) noexcept(see below);
```

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_move_assignable<T1>::value &&
is_nothrow_move_assignable<T2>::value
```

*Requires:* `is_move_assignable<first_type>::value` is `true` and
`is_move_assignable<second_type>::value` is `true`.

*Effects:* Assigns to `first` with `std::forward<first_type>(p.first)`
and to `second` with  
`std::forward<second_type>(p.second)`.

*Returns:* `*this`.

``` cpp
template<class U, class V> pair& operator=(pair<U, V>&& p);
```

*Requires:* `is_assignable<first_type&, U&&>::value` is `true` and
`is_assignable<second_type&, V&&>::value` is `true`.

*Effects:* Assigns to `first` with `std::forward<U>(p.first)` and to
`second` with  
`std::forward<V>(p.second)`.

*Returns:* `*this`.

``` cpp
void swap(pair& p) noexcept(see below);
```

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
noexcept(swap(first, p.first)) &&
noexcept(swap(second, p.second))
```

*Requires:* `first` shall be swappable
with ([[swappable.requirements]]) `p.first` and `second` shall be
swappable with `p.second`.

*Effects:* Swaps `first` with `p.first` and `second` with `p.second`.

### Specialized algorithms <a id="pairs.spec">[[pairs.spec]]</a>

``` cpp
template <class T1, class T2>
  constexpr bool operator==(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `x.first == y.first && x.second == y.second`.

``` cpp
template <class T1, class T2>
  constexpr bool operator<(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:*
`x.first < y.first || (!(y.first < x.first) && x.second < y.second)`.

``` cpp
template <class T1, class T2>
  constexpr bool operator!=(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `!(x == y)`

``` cpp
template <class T1, class T2>
  constexpr bool operator>(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `y < x`

``` cpp
template <class T1, class T2>
  constexpr bool operator>=(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `!(x < y)`

``` cpp
template <class T1, class T2>
  constexpr bool operator<=(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `!(y < x)`

``` cpp
template<class T1, class T2> void swap(pair<T1, T2>& x, pair<T1, T2>& y)
  noexcept(noexcept(x.swap(y)));
```

*Effects:* `x.swap(y)`

``` cpp
template <class T1, class T2>
  constexpr pair<V1, V2> make_pair(T1&& x, T2&& y);
```

*Returns:* `pair<V1, V2>(std::forward<T1>(x), std::forward<T2>(y))`;

where `V1` and `V2` are determined as follows: Let `Ui` be `decay_t<Ti>`
for each `Ti`. Then each `Vi` is `X&` if `Ui` equals
`reference_wrapper<X>`, otherwise `Vi` is `Ui`.

In place of:

``` cpp
return pair<int, double>(5, 3.1415926);   // explicit types
```

a C++program may contain:

``` cpp
return make_pair(5, 3.1415926);           // types are deduced
```

### Tuple-like access to pair <a id="pair.astuple">[[pair.astuple]]</a>

``` cpp
template <class T1, class T2>
struct tuple_size<pair<T1, T2>>
  : integral_constant<size_t, 2> { };
```

``` cpp
tuple_element<0, pair<T1, T2> >::type
```

*Value:* the type `T1`.

``` cpp
tuple_element<1, pair<T1, T2> >::type
```

*Value:* the type T2.

``` cpp
template<size_t I, class T1, class T2>
  constexpr tuple_element_t<I, pair<T1, T2>>&
    get(pair<T1, T2>& p) noexcept;
template<size_t I, class T1, class T2>
  constexpr const tuple_element_t<I, pair<T1, T2>>&
    get(const pair<T1, T2>& p) noexcept;
```

*Returns:* If `I == 0` returns `p.first`; if `I == 1` returns
`p.second`; otherwise the program is ill-formed.

``` cpp
template<size_t I, class T1, class T2>
  constexpr tuple_element_t<I, pair<T1, T2>>&&
    get(pair<T1, T2>&& p) noexcept;
```

*Returns:* If `I == 0` returns `std::forward<T1&&>(p.first)`; if
`I == 1` returns `std::forward<T2&&>(p.second)`; otherwise the program
is ill-formed.

``` cpp
template <class T, class U>
  constexpr T& get(pair<T, U>& p) noexcept;
template <class T, class U>
  constexpr const T& get(const pair<T, U>& p) noexcept;
```

*Requires:* `T` and `U` are distinct types. Otherwise, the program is
ill-formed.

*Returns:* `get<0>(p);`

``` cpp
template <class T, class U>
  constexpr T&& get(pair<T, U>&& p) noexcept;
```

*Requires:* `T` and `U` are distinct types. Otherwise, the program is
ill-formed.

*Returns:* `get<0>(std::move(p));`

``` cpp
template <class T, class U>
  constexpr T& get(pair<U, T>& p) noexcept;
template <class T, class U>
  constexpr const T& get(const pair<U, T>& p) noexcept;
```

*Requires:* `T` and `U` are distinct types. Otherwise, the program is
ill-formed.

*Returns:* `get<1>(p);`

``` cpp
template <class T, class U>
  constexpr T&& get(pair<U, T>&& p) noexcept;
```

*Requires:* `T` and `U` are distinct types. Otherwise, the program is
ill-formed.

*Returns:* `get<1>(std::move(p));`

### Piecewise construction <a id="pair.piecewise">[[pair.piecewise]]</a>

``` cpp
struct piecewise_construct_t { };
constexpr piecewise_construct_t piecewise_construct{};
```

The `struct` `piecewise_construct_t` is an empty structure type used as
a unique type to disambiguate constructor and function overloading.
Specifically, `pair` has a constructor with `piecewise_construct_t` as
the first argument, immediately followed by two `tuple` ([[tuple]])
arguments used for piecewise construction of the elements of the `pair`
object.

## Tuples <a id="tuple">[[tuple]]</a>

### In general <a id="tuple.general">[[tuple.general]]</a>

This subclause describes the tuple library that provides a tuple type as
the class template `tuple` that can be instantiated with any number of
arguments. Each template argument specifies the type of an element in
the `tuple`. Consequently, tuples are heterogeneous, fixed-size
collections of values. An instantiation of `tuple` with two arguments is
similar to an instantiation of `pair` with the same two arguments. See 
[[pairs]].

``` cpp
namespace std {
  // [tuple.tuple], class template tuple:
  template <class... Types> class tuple;

  // [tuple.creation], tuple creation functions:
  const unspecified ignore;

  template <class... Types>
    constexpr tuple<VTypes...> make_tuple(Types&&...);
  template <class... Types>
    constexpr tuple<Types&&...> forward_as_tuple(Types&&...) noexcept;

  template<class... Types>
    constexpr tuple<Types&...> tie(Types&...) noexcept;

  template <class... Tuples>
    constexpr tuple<Ctypes...> tuple_cat(Tuples&&...);

  // [tuple.helper], tuple helper classes:
  template <class T> class tuple_size;  // undefined
  template <class T> class tuple_size<const T>;
  template <class T> class tuple_size<volatile T>;
  template <class T> class tuple_size<const volatile T>;

  template <class... Types> class tuple_size<tuple<Types...> >;

  template <size_t I, class T> class tuple_element;    // undefined
  template <size_t I, class T> class tuple_element<I, const T>;
  template <size_t I, class T> class tuple_element<I, volatile T>;
  template <size_t I, class T> class tuple_element<I, const volatile T>;

  template <size_t I, class... Types> class tuple_element<I, tuple<Types...> >;

  template <size_t I, class T>
    using tuple_element_t = typename tuple_element<I, T>::type;

  // [tuple.elem], element access:
  template <size_t I, class... Types>
    constexpr tuple_element_t<I, tuple<Types...>>&
      get(tuple<Types...>&) noexcept;
  template <size_t I, class... Types>
    constexpr tuple_element_t<I, tuple<Types...>>&&
      get(tuple<Types...>&&) noexcept;
  template <size_t I, class... Types>
    constexpr const tuple_element_t<I, tuple<Types...>>&
      get(const tuple<Types...>&) noexcept;
  template <class T, class... Types>
    constexpr T& get(tuple<Types...>& t) noexcept;
  template <class T, class... Types>
    constexpr T&& get(tuple<Types...>&& t) noexcept;
  template <class T, class... Types>
    constexpr const T& get(const tuple<Types...>& t) noexcept;

  // [tuple.rel], relational operators:
  template<class... TTypes, class... UTypes>
    constexpr bool operator==(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator<(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator!=(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator>(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator<=(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator>=(const tuple<TTypes...>&, const tuple<UTypes...>&);

  // [tuple.traits], allocator-related traits
  template <class... Types, class Alloc>
    struct uses_allocator<tuple<Types...>, Alloc>;

  // [tuple.special], specialized algorithms:
  template <class... Types>
    void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);
}
```

### Class template `tuple` <a id="tuple.tuple">[[tuple.tuple]]</a>

``` cpp
namespace std {
  template <class... Types>
  class tuple  {
  public:

    // [tuple.cnstr], tuple construction
    constexpr tuple();
    constexpr explicit tuple(const Types&...);
    template <class... UTypes>
      constexpr explicit tuple(UTypes&&...);

    tuple(const tuple&) = default;
    tuple(tuple&&) = default;

    template <class... UTypes>
      constexpr tuple(const tuple<UTypes...>&);
    template <class... UTypes>
      constexpr tuple(tuple<UTypes...>&&);

    template <class U1, class U2>
      constexpr tuple(const pair<U1, U2>&);       // only if sizeof...(Types) == 2
    template <class U1, class U2>
      constexpr tuple(pair<U1, U2>&&);            // only if sizeof...(Types) == 2

    // allocator-extended constructors
    template <class Alloc>
      tuple(allocator_arg_t, const Alloc& a);
    template <class Alloc>
      tuple(allocator_arg_t, const Alloc& a, const Types&...);
    template <class Alloc, class... UTypes>
      tuple(allocator_arg_t, const Alloc& a, UTypes&&...);
    template <class Alloc>
      tuple(allocator_arg_t, const Alloc& a, const tuple&);
    template <class Alloc>
      tuple(allocator_arg_t, const Alloc& a, tuple&&);
    template <class Alloc, class... UTypes>
      tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
    template <class Alloc, class... UTypes>
      tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
    template <class Alloc, class U1, class U2>
      tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
    template <class Alloc, class U1, class U2>
      tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);

    // [tuple.assign], tuple assignment
    tuple& operator=(const tuple&);
    tuple& operator=(tuple&&) noexcept(see below);

    template <class... UTypes>
      tuple& operator=(const tuple<UTypes...>&);
    template <class... UTypes>
      tuple& operator=(tuple<UTypes...>&&);

    template <class U1, class U2>
      tuple& operator=(const pair<U1, U2>&);    // only if sizeof...(Types) == 2
    template <class U1, class U2>
      tuple& operator=(pair<U1, U2>&&);         // only if sizeof...(Types) == 2

    // [tuple.swap], tuple swap
    void swap(tuple&) noexcept(see below);
  };
}
```

#### Construction <a id="tuple.cnstr">[[tuple.cnstr]]</a>

For each `tuple` constructor, an exception is thrown only if the
construction of one of the types in `Types` throws an exception.

The defaulted move and copy constructor, respectively, of `tuple` shall
be a `constexpr` function if and only if all required element-wise
initializations for copy and move, respectively, would satisfy the
requirements for a `constexpr` function. The defaulted move and copy
constructor of `tuple<>` shall be `constexpr` functions.

In the constructor descriptions that follow, let i be in the range
\[`0`, `sizeof...(Types)`) in order, Tᵢ be the iᵗʰ type in `Types`, and
Uᵢ be the iᵗʰ type in a template parameter pack named `UTypes`, where
indexing is zero-based.

``` cpp
constexpr tuple();
```

*Requires:* `is_default_constructible<`Tᵢ`>::value` is true for all i.

*Effects:* Value initializes each element.

``` cpp
constexpr explicit tuple(const Types&...);
```

*Requires:* `is_copy_constructible<`Tᵢ`>::value` is true for all i.

*Effects:* Initializes each element with the value of the corresponding
parameter.

``` cpp
template <class... UTypes>
  constexpr explicit tuple(UTypes&&... u);
```

*Requires:* `sizeof...(Types)` `==` `sizeof...(UTypes)`.
`is_constructible<`Tᵢ`, `Uᵢ`&&>::value` is `true` for all i.

*Effects:* Initializes the elements in the tuple with the corresponding
value in `std::forward<UTypes>(u)`.

This constructor shall not participate in overload resolution unless
each type in `UTypes` is implicitly convertible to its corresponding
type in `Types`.

``` cpp
tuple(const tuple& u) = default;
```

*Requires:* `is_copy_constructible<`Tᵢ`>::value` is `true` for all i.

*Effects:* Initializes each element of `*this` with the corresponding
element of `u`.

``` cpp
tuple(tuple&& u) = default;
```

*Requires:* `is_move_constructible<`Tᵢ`>::value` is `true` for all i.

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`std::forward<`Tᵢ`>(get<`i`>(u))`.

``` cpp
template <class... UTypes> constexpr tuple(const tuple<UTypes...>& u);
```

*Requires:* `sizeof...(Types)` `==` `sizeof...(UTypes)`.
`is_constructible<`Tᵢ`, const `Uᵢ`&>::value` is `true` for all i.

*Effects:* Constructs each element of `*this` with the corresponding
element of `u`.

This constructor shall not participate in overload resolution unless
`const `Uᵢ`&` is implicitly convertible to Tᵢ for all i.

``` cpp
template <class... UTypes> constexpr tuple(tuple<UTypes...>&& u);
```

*Requires:* `sizeof...(Types)` `==` `sizeof...(UTypes)`.
`is_constructible<`Tᵢ`, `Uᵢ`&&>::value` is `true` for all i.

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`std::forward<`Uᵢ`>(get<`i`>(u))`.

This constructor shall not participate in overload resolution unless
each type in `UTypes` is implicitly convertible to its corresponding
type in `Types`.

``` cpp
template <class U1, class U2> constexpr tuple(const pair<U1, U2>& u);
```

*Requires:* `sizeof...(Types) == 2`.
`is_constructible<`T₀`, const U1&>::value` is `true` for the first type
T₀ in `Types` and `is_constructible<`T₁`, const U2&>::value` is `true`
for the second type T₁ in `Types`.

*Effects:* Constructs the first element with `u.first` and the second
element with `u.second`.

This constructor shall not participate in overload resolution unless
`const U1&` is implicitly convertible to T₀ and `const U2&` is
implicitly convertible to T₁.

``` cpp
template <class U1, class U2> constexpr tuple(pair<U1, U2>&& u);
```

*Requires:* `sizeof...(Types) == 2`.
`is_constructible<`T₀`, U1&&>::value` is `true` for the first type T₀ in
`Types` and `is_constructible<`T₁`, U2&&>::value` is `true` for the
second type T₁ in `Types`.

*Effects:* Initializes the first element with
`std::forward<U1>(u.first)` and the second element with
`std::forward<U2>(u.second)`.

This constructor shall not participate in overload resolution unless
`U1` is implicitly convertible to T₀ and `U2` is implicitly convertible
to T₁.

``` cpp
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a);
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a, const Types&...);
template <class Alloc, class... UTypes>
  tuple(allocator_arg_t, const Alloc& a, UTypes&&...);
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a, const tuple&);
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a, tuple&&);
template <class Alloc, class... UTypes>
  tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
template <class Alloc, class... UTypes>
  tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
template <class Alloc, class U1, class U2>
  tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
template <class Alloc, class U1, class U2>
  tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);
```

*Requires:* `Alloc` shall meet the requirements for an
`Allocator` ([[allocator.requirements]]).

*Effects:* Equivalent to the preceding constructors except that each
element is constructed with uses-allocator
construction ([[allocator.uses.construction]]).

#### Assignment <a id="tuple.assign">[[tuple.assign]]</a>

For each `tuple` assignment operator, an exception is thrown only if the
assignment of one of the types in `Types` throws an exception. In the
function descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`) in order, Tᵢ be the iᵗʰ type in `Types`, and Uᵢ be
the iᵗʰ type in a template parameter pack named `UTypes`, where indexing
is zero-based.

``` cpp
tuple& operator=(const tuple& u);
```

*Requires:* `is_copy_assignable<`Tᵢ`>::value` is `true` for all i.

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Returns:* `*this`

``` cpp
tuple& operator=(tuple&& u) noexcept(see below);
```

The expression inside `noexcept` is equivalent to the logical
<span class="smallcaps">and</span> of the following expressions:

``` cpp
is_nothrow_move_assignable<Tᵢ>::value
```

where Tᵢ is the iᵗʰ type in `Types`.

*Requires:* `is_move_assignable<`Tᵢ`>::value` is `true` for all i.

*Effects:* For all i, assigns `std::forward<`Tᵢ`>(get<`i`>(u))` to
`get<`i`>(*this)`.

*Returns:* `*this`.

``` cpp
template <class... UTypes>
  tuple& operator=(const tuple<UTypes...>& u);
```

*Requires:* `sizeof...(Types) == sizeof...(UTypes)` and
`is_assignable<`Tᵢ`&, const `Uᵢ`&>::value` is `true` for all i.

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Returns:* `*this`

``` cpp
template <class... UTypes>
  tuple& operator=(tuple<UTypes...>&& u);
```

*Requires:* `is_assignable<Ti&, Ui&&>::value == true` for all `i`.
`sizeof...(Types)` `==`  
`sizeof...(UTypes)`.

*Effects:* For all i, assigns `std::forward<`Uᵢ`>(get<`i`)>(u))` to
`get<`i`>(*this)`.

*Returns:* `*this`.

``` cpp
template <class U1, class U2> tuple& operator=(const pair<U1, U2>& u);
```

*Requires:* `sizeof...(Types) == 2`.
`is_assignable<`T₀`&, const U1&>::value` is `true` for the first type T₀
in `Types` and `is_assignable<`T₁`&, const U2&>::value` is `true` for
the second type T₁ in `Types`.

*Effects:* Assigns `u.first` to the first element of `*this` and
`u.second` to the second element of `*this`.

*Returns:* `*this`

``` cpp
template <class U1, class U2> tuple& operator=(pair<U1, U2>&& u);
```

*Requires:* `sizeof...(Types) == 2`. `is_assignable<`T₀`&, U1&&>::value`
is `true` for the first type T₀ in `Types` and
`is_assignable<`T₁`&, U2&&>::value` is `true` for the second type T₁ in
`Types`.

*Effects:* Assigns `std::forward<U1>(u.first)` to the first element of
`*this` and  
`std::forward<U2>(u.second)` to the second element of `*this`.

*Returns:* `*this`.

#### `swap` <a id="tuple.swap">[[tuple.swap]]</a>

``` cpp
void swap(tuple& rhs) noexcept(see below);
```

The expression inside `noexcept` is equivalent to the logical
<span class="smallcaps">and</span> of the following expressions:

``` cpp
noexcept(swap(declval<Tᵢ&>>(), declval<Tᵢ&>()))
```

where Tᵢ is the iᵗʰ type in `Types`.

*Requires:* Each element in `*this` shall be swappable
with ([[swappable.requirements]]) the corresponding element in `rhs`.

*Effects:* Calls `swap` for each element in `*this` and its
corresponding element in `rhs`.

*Throws:* Nothing unless one of the element-wise `swap` calls throws an
exception.

#### Tuple creation functions <a id="tuple.creation">[[tuple.creation]]</a>

In the function descriptions that follow, let i be in the range \[`0`,
`sizeof...(TTypes)`) in order and let Tᵢ be the iᵗʰ type in a template
parameter pack named `TTypes`; let j be in the range \[`0`,
`sizeof...(UTypes)`) in order and Uⱼ be the jᵗʰ type in a template
parameter pack named `UTypes`, where indexing is zero-based.

``` cpp
template<class... Types>
  constexpr tuple<VTypes...> make_tuple(Types&&... t);
```

Let Uᵢ be `decay_t<`Tᵢ`>` for each Tᵢ in `Types`. Then each Vᵢ in
`VTypes` is `X&` if Uᵢ equals `reference_wrapper<X>`, otherwise Vᵢ is
Uᵢ.

*Returns:* `tuple<VTypes...>(std::forward<Types>(t)...)`.

``` cpp
int i; float j;
make_tuple(1, ref(i), cref(j))
```

creates a tuple of type

``` cpp
tuple<int, int&, const float&>
```

``` cpp
template<class... Types>
  constexpr tuple<Types&&...> forward_as_tuple(Types&&... t) noexcept;
```

*Effects:* Constructs a tuple of references to the arguments in `t`
suitable for forwarding as arguments to a function. Because the result
may contain references to temporary variables, a program shall ensure
that the return value of this function does not outlive any of its
arguments. (e.g., the program should typically not store the result in a
named variable).

*Returns:* `tuple<Types&&...>(std::forward<Types>(t)...)`

``` cpp
template<class... Types>
  constexpr tuple<Types&...> tie(Types&... t) noexcept;
```

*Returns:* `tuple<Types&...>(t...)`. When an argument in `t` is
`ignore`, assigning any value to the corresponding tuple element has no
effect.

`tie` functions allow one to create tuples that unpack tuples into
variables. `ignore` can be used for elements that are not needed:

``` cpp
int i; std::string s;
tie(i, ignore, s) = make_tuple(42, 3.14, "C++");
// i == 42, s == "C++"
```

``` cpp
template <class... Tuples>
  constexpr tuple<CTypes...> tuple_cat(Tuples&&... tpls);
```

In the following paragraphs, let Tᵢ be the iᵗʰ type in `Tuples`, Uᵢ be
`remove_reference_t<Ti>`, and tpᵢ be the iᵗʰ parameter in the function
parameter pack `tpls`, where all indexing is zero-based.

*Requires:* For all i, Uᵢ shall be the type cvᵢ `tuple<`Argsᵢ...`>`,
where cvᵢ is the (possibly empty) iᵗʰ cv-qualifier-seq and Argsᵢ is the
parameter pack representing the element types in Uᵢ. Let {Aᵢₖ} be the
kᵢᵗʰ type in Argsᵢ. For all Aᵢₖ the following requirements shall be
satisfied: If Tᵢ is deduced as an lvalue reference type, then
`is_constructible<`Aᵢₖ`, `cvᵢ` `Aᵢₖ`&>::value == true`, otherwise
`is_constructible<`Aᵢₖ`, `cvᵢ Aᵢₖ`&&>::value == true`.

*Remarks:* The types in *`Ctypes`* shall be equal to the ordered
sequence of the extended types Args₀`..., `Args₁`...,` ... Argsₙ₋₁`...`,
where n is equal to `sizeof...(Tuples)`. Let eᵢ`...` be the iᵗʰ ordered
sequence of tuple elements of the resulting `tuple` object corresponding
to the type sequence Argsᵢ.

*Returns:* A `tuple` object constructed by initializing the kᵢᵗʰ type
element eᵢₖ in eᵢ`...` with  
`get<`kᵢ`>(std::forward<`Tᵢ`>(`tpᵢ`))` for each valid kᵢ and each group
eᵢ in order.

*Note:* An implementation may support additional types in the parameter
pack `Tuples` that support the `tuple`-like protocol, such as `pair` and
`array`.

#### Tuple helper classes <a id="tuple.helper">[[tuple.helper]]</a>

``` cpp
template <class T> struct tuple_size;
```

*Remarks:* All specializations of `tuple_size<T>` shall meet the
`UnaryTypeTrait` requirements ([[meta.rqmts]]) with a
`BaseCharacteristic` of `integral_constant<size_t, N>` for some `N`.

``` cpp
template <class... Types>
class tuple_size<tuple<Types...> >
  : public integral_constant<size_t, sizeof...(Types)> { };
```

``` cpp
template <size_t I, class... Types>
class tuple_element<I, tuple<Types...> > {
public:
  typedef TI type;
};
```

*Requires:* `I < sizeof...(Types)`. The program is ill-formed if `I` is
out of bounds.

*Type:* `TI` is the type of the `I`th element of `Types`, where indexing
is zero-based.

``` cpp
template <class T> class tuple_size<const T>;
template <class T> class tuple_size<volatile T>;
template <class T> class tuple_size<const volatile T>;
```

Let *TS* denote `tuple_size<T>` of the cv-unqualified type `T`. Then
each of the three templates shall meet the `UnaryTypeTrait`
requirements ([[meta.rqmts]]) with a `BaseCharacteristic` of

``` cpp
integral_constant<size_t, TS::value>
```

``` cpp
template <size_t I, class T> class tuple_element<I, const T>;
template <size_t I, class T> class tuple_element<I, volatile T>;
template <size_t I, class T> class tuple_element<I, const volatile T>;
```

Let *TE* denote `tuple_element<I, T>` of the cv-unqualified type `T`.
Then each of the three templates shall meet the `TransformationTrait`
requirements ([[meta.rqmts]]) with a member typedef `type` that names
the following type:

- for the first specialization, `add_const_t<`*`TE`*`::type>`,
- for the second specialization, `add_volatile_t<`*`TE`*`::type>`, and
- for the third specialization, `add_cv_t<`*`TE`*`::type>`.

#### Element access <a id="tuple.elem">[[tuple.elem]]</a>

``` cpp
template <size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...> >& get(tuple<Types...>& t) noexcept;
```

*Requires:* `I < sizeof...(Types)`. The program is ill-formed if `I` is
out of bounds.

*Returns:* A reference to the `I`th element of `t`, where indexing is
zero-based.

``` cpp
template <size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...> >&& get(tuple<Types...>&& t) noexcept;
```

*Effects:* Equivalent to
`return std::forward<typename tuple_element<I, tuple<Types...> >`  
`::type&&>(get<I>(t));`

*Note:* if a `T` in `Types` is some reference type `X&`, the return type
is `X&`, not `X&&`. However, if the element type is a non-reference type
`T`, the return type is `T&&`.

``` cpp
template <size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...> > const& get(const tuple<Types...>& t) noexcept;
```

*Requires:* `I < sizeof...(Types)`. The program is ill-formed if `I` is
out of bounds.

*Returns:* A const reference to the `I`th element of `t`, where indexing
is zero-based.

Constness is shallow. If a `T` in `Types` is some reference type `X&`,
the return type is `X&`, not `const X&`. However, if the element type is
non-reference type `T`, the return type is `const T&`. This is
consistent with how constness is defined to work for member variables of
reference type.

``` cpp
template <class T, class... Types>
  constexpr T& get(tuple<Types...>& t) noexcept;
template <class T, class... Types>
  constexpr T&& get(tuple<Types...>&& t) noexcept;
template <class T, class... Types>
  constexpr const T& get(const tuple<Types...>& t) noexcept;
```

*Requires:* The type `T` occurs exactly once in `Types...`. Otherwise,
the program is ill-formed.

*Returns:* A reference to the element of `t` corresponding to the type
`T` in `Types...`.

``` cpp
const tuple<int, const int, double, double> t(1, 2, 3.4, 5.6);
  const int &i1 = get<int>(t);        // OK. Not ambiguous. i1 == 1
  const int &i2 = get<const int>(t);  // OK. Not ambiguous. i2 == 2
  const double &d = get<double>(t);   // ERROR. ill-formed
```

The reason `get` is a nonmember function is that if this functionality
had been provided as a member function, code where the type depended on
a template parameter would have required using the `template` keyword.

#### Relational operators <a id="tuple.rel">[[tuple.rel]]</a>

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator==(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Requires:* For all `i`, where `0 <= i` and `i < sizeof...(TTypes)`,
`get<i>(t) == get<i>(u)` is a valid expression returning a type that is
convertible to `bool`. `sizeof...(TTypes)` `==` `sizeof...(UTypes)`.

*Returns:* `true` if `get<i>(t) == get<i>(u)` for all `i`, otherwise
`false`. For any two zero-length tuples `e` and `f`, `e == f` returns
`true`.

*Effects:* The elementary comparisons are performed in order from the
zeroth index upwards. No comparisons or element accesses are performed
after the first equality comparison that evaluates to `false`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator<(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Requires:* For all `i`, where `0 <= i` and `i < sizeof...(TTypes)`,
`get<i>(t) < get<i>(u)` and `get<i>(u) < get<i>(t)` are valid
expressions returning types that are convertible to `bool`.
`sizeof...(TTypes)` `==` `sizeof...(UTypes)`.

*Returns:* The result of a lexicographical comparison between `t` and
`u`. The result is defined as:
`(bool)(get<0>(t) < get<0>(u)) || (!(bool)(get<0>(u) < get<0>(t)) && t`ₜₐᵢₗ` < u`ₜₐᵢₗ`)`,
where `r`ₜₐᵢₗ for some tuple `r` is a tuple containing all but the first
element of `r`. For any two zero-length tuples `e` and `f`, `e < f`
returns `false`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator!=(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `!(t == u)`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator>(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `u < t`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator<=(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `!(u < t)`

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator>=(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `!(t < u)`

The above definitions for comparison operators do not require `tₜₐᵢₗ`
(or `uₜₐᵢₗ`) to be constructed. It may not even be possible, as `t` and
`u` are not required to be copy constructible. Also, all comparison
operators are short circuited; they do not perform element accesses
beyond what is required to determine the result of the comparison.

#### Tuple traits <a id="tuple.traits">[[tuple.traits]]</a>

``` cpp
template <class... Types, class Alloc>
  struct uses_allocator<tuple<Types...>, Alloc> : true_type { };
```

*Requires:* `Alloc` shall be an
`Allocator` ([[allocator.requirements]]).

Specialization of this trait informs other library components that
`tuple` can be constructed with an allocator, even though it does not
have a nested `allocator_type`.

#### Tuple specialized algorithms <a id="tuple.special">[[tuple.special]]</a>

``` cpp
template <class... Types>
  void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);
```

The expression inside `noexcept` is equivalent to:

``` cpp
noexcept(x.swap(y))
```

*Effects:* `x.swap(y)`

## Compile-time integer sequences <a id="intseq">[[intseq]]</a>

### In general <a id="intseq.general">[[intseq.general]]</a>

The library provides a class template that can represent an integer
sequence. When used as an argument to a function template the parameter
pack defining the sequence can be deduced and used in a pack expansion.

``` cpp
template<class F, class Tuple, std::size_t... I>
  decltype(auto) apply_impl(F&& f, Tuple&& t, index_sequence<I...>) {
    return std::forward<F>(f)(std::get<I>(std::forward<Tuple>(t))...);
  }

template<class F, class Tuple>
  decltype(auto) apply(F&& f, Tuple&& t) {
    using Indices = make_index_sequence<std::tuple_size<std::decay_t<Tuple>>::value>;
    return apply_impl(std::forward<F>(f), std::forward<Tuple>(t), Indices());
  }
```

The `index_sequence` alias template is provided for the common case of
an integer sequence of type `size_t`.

### Class template `integer_sequence` <a id="intseq.intseq">[[intseq.intseq]]</a>

``` cpp
namespace std {
  template<class T, T... I>
  struct integer_sequence {
    typedef T value_type;
    static constexpr size_t size() noexcept { return sizeof...(I); }
  };
}
```

`T` shall be an integer type.

### Alias template `make_integer_sequence` <a id="intseq.make">[[intseq.make]]</a>

``` cpp
template<class T, T N>
  using make_integer_sequence = integer_sequence<T, see below{}>;
```

If `N` is negative the program is ill-formed. The alias template
`make_integer_sequence` denotes a specialization of `integer_sequence`
with `N` template non-type arguments. The type
`make_integer_sequence<T, N>` denotes the type
`integer_sequence<T, 0, 1, ..., N-1>`. `make_integer_sequence<int, 0>`
denotes the type `integer_sequence<int>`

## Class template `bitset` <a id="template.bitset">[[template.bitset]]</a>

\synopsis{Header \texttt{\<bitset\>} synopsis}

``` cpp
#include <string>
#include <iosfwd>               // for istream, ostream
namespace std {
  template <size_t N> class bitset;

  // [bitset.operators] bitset operators:
  template <size_t N>
    bitset<N> operator&(const bitset<N>&, const bitset<N>&) noexcept;
  template <size_t N>
    bitset<N> operator|(const bitset<N>&, const bitset<N>&) noexcept;
  template <size_t N>
    bitset<N> operator^(const bitset<N>&, const bitset<N>&) noexcept;
  template <class charT, class traits, size_t N>
    basic_istream<charT, traits>&
    operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
  template <class charT, class traits, size_t N>
    basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const bitset<N>& x);
}
```

The header `<bitset>` defines a class template and several related
functions for representing and manipulating fixed-size sequences of
bits.

``` cpp
namespace std {
  template<size_t N> class bitset {
  public:
    // bit reference:
    class reference {
      friend class bitset;
      reference() noexcept;
    public:
     ~reference() noexcept;
      reference& operator=(bool x) noexcept;             // for b[i] = x;
      reference& operator=(const reference&) noexcept;   // for b[i] = b[j];
      bool operator~() const noexcept;                   // flips the bit
      operator bool() const noexcept;                    // for x = b[i];
      reference& flip() noexcept;                        // for b[i].flip();
    };

    // [bitset.cons] constructors:
    constexpr bitset() noexcept;
    constexpr bitset(unsigned long long val) noexcept;
    template<class charT, class traits, class Allocator>
      explicit bitset(
        const basic_string<charT,traits,Allocator>& str,
        typename basic_string<charT,traits,Allocator>::size_type pos = 0,
        typename basic_string<charT,traits,Allocator>::size_type n =
          basic_string<charT,traits,Allocator>::npos,
          charT zero = charT('0'), charT one = charT('1'));
    template <class charT>
      explicit bitset(
        const charT* str,
        typename basic_string<charT>::size_type n = basic_string<charT>::npos,
        charT zero = charT('0'), charT one = charT('1'));

    // [bitset.members] bitset operations:
    bitset<N>& operator&=(const bitset<N>& rhs) noexcept;
    bitset<N>& operator|=(const bitset<N>& rhs) noexcept;
    bitset<N>& operator^=(const bitset<N>& rhs) noexcept;
    bitset<N>& operator<<=(size_t pos) noexcept;
    bitset<N>& operator>>=(size_t pos) noexcept;
    bitset<N>& set() noexcept;
    bitset<N>& set(size_t pos, bool val = true);
    bitset<N>& reset() noexcept;
    bitset<N>& reset(size_t pos);
    bitset<N>  operator~() const noexcept;
    bitset<N>& flip() noexcept;
    bitset<N>& flip(size_t pos);

    // element access:
    constexpr bool operator[](size_t pos) const;       // for b[i];
    reference operator[](size_t pos);                  // for b[i];

    unsigned long to_ulong() const;
    unsigned long long to_ullong() const;
    template <class charT = char,
        class traits = char_traits<charT>,
        class Allocator = allocator<charT> >
      basic_string<charT, traits, Allocator>
      to_string(charT zero = charT('0'), charT one = charT('1')) const;
    size_t count() const noexcept;
    constexpr size_t size() const noexcept;
    bool operator==(const bitset<N>& rhs) const noexcept;
    bool operator!=(const bitset<N>& rhs) const noexcept;
    bool test(size_t pos) const;
    bool all() const noexcept;
    bool any() const noexcept;
    bool none() const noexcept;
    bitset<N> operator<<(size_t pos) const noexcept;
    bitset<N> operator>>(size_t pos) const noexcept;
  };

  // [bitset.hash] hash support
  template <class T> struct hash;
  template <size_t N> struct hash<bitset<N> >;
}
```

The class template `bitset<N>` describes an object that can store a
sequence consisting of a fixed number of bits, `N`.

Each bit represents either the value zero (reset) or one (set). To
*toggle* a bit is to change the value zero to one, or the value one to
zero. Each bit has a non-negative position `pos`. When converting
between an object of class `bitset<N>` and a value of some integral
type, bit position `pos` corresponds to the *bit value* `1 \shl pos`.
The integral value corresponding to two or more bits is the sum of their
bit values.

The functions described in this subclause can report three kinds of
errors, each associated with a distinct exception:

- an *invalid-argument* error is associated with exceptions of type
  `invalid_argument` ([[invalid.argument]]);
- an *out-of-range* error is associated with exceptions of type
  `out_of_range` ([[out.of.range]]);
- an *overflow* error is associated with exceptions of type
  `overflow_error` ([[overflow.error]]).

### `bitset` constructors <a id="bitset.cons">[[bitset.cons]]</a>

``` cpp
constexpr bitset() noexcept;
```

*Effects:* Constructs an object of class `bitset<N>`, initializing all
bits to zero.

``` cpp
constexpr bitset(unsigned long long val) noexcept;
```

*Effects:* Constructs an object of class `bitset<N>`, initializing the
first `M` bit positions to the corresponding bit values in `val`. `M` is
the smaller of `N` and the number of bits in the value
representation ([[basic.types]]) of `unsigned long long`. If `M < N`,
the remaining bit positions are initialized to zero.

``` cpp
template <class charT, class traits, class Allocator>
explicit
bitset(const basic_string<charT, traits, Allocator>& str,
       typename basic_string<charT, traits, Allocator>::size_type pos = 0,
       typename basic_string<charT, traits, Allocator>::size_type n =
         basic_string<charT, traits, Allocator>::npos,
         charT zero = charT('0'), charT one = charT('1'));
```

*Requires:* `pos <= str.size()`.

*Throws:* `out_of_range` if `pos > str.size()`.

*Effects:* Determines the effective length `rlen` of the initializing
string as the smaller of `n` and `str.size() - pos`.

The function then throws

`invalid_argument` if any of the `rlen` characters in `str` beginning at
position `pos` is other than `zero` or `one`. The function uses
`traits::eq()` to compare the character values.

Otherwise, the function constructs an object of class `bitset<N>`,
initializing the first `M` bit positions to values determined from the
corresponding characters in the string `str`. `M` is the smaller of `N`
and `rlen`.

An element of the constructed object has value zero if the corresponding
character in `str`, beginning at position `pos`, is `zero`. Otherwise,
the element has the value one. Character position `pos + M - 1`
corresponds to bit position zero. Subsequent decreasing character
positions correspond to increasing bit positions.

If `M < N`, remaining bit positions are initialized to zero.

``` cpp
template <class charT>
  explicit bitset(
    const charT* str,
    typename basic_string<charT>::size_type n = basic_string<charT>::npos,
    charT zero = charT('0'), charT one = charT('1'));
```

*Effects:* Constructs an object of class `bitset<N>` as if by

``` cpp
bitset(
  n == basic_string<charT>::npos
    ? basic_string<charT>(str)
    : basic_string<charT>(str, n),
  0, n, zero, one)
```

### `bitset` members <a id="bitset.members">[[bitset.members]]</a>

``` cpp
bitset<N>& operator&=(const bitset<N>& rhs) noexcept;
```

*Effects:* Clears each bit in `*this` for which the corresponding bit in
`rhs` is clear, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
bitset<N>& operator|=(const bitset<N>& rhs) noexcept;
```

*Effects:* Sets each bit in `*this` for which the corresponding bit in
`rhs` is set, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
bitset<N>& operator^=(const bitset<N>& rhs) noexcept;
```

*Effects:* Toggles each bit in `*this` for which the corresponding bit
in `rhs` is set, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
bitset<N>& operator<<=(size_t pos) noexcept;
```

*Effects:* Replaces each bit at position `I` in `*this` with a value
determined as follows:

- If `I < pos`, the new value is zero;
- If `I >= pos`, the new value is the previous value of the bit at
  position `I - pos`.

*Returns:* `*this`.

``` cpp
bitset<N>& operator>>=(size_t pos) noexcept;
```

*Effects:* Replaces each bit at position `I` in `*this` with a value
determined as follows:

- If `pos >= N - I`, the new value is zero;
- If `pos < N - I`, the new value is the previous value of the bit at
  position `I + pos`.

*Returns:* `*this`.

``` cpp
bitset<N>& set() noexcept;
```

*Effects:* Sets all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& set(size_t pos, bool val = true);
```

*Requires:* `pos` is valid

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Effects:* Stores a new value in the bit at position `pos` in `*this`.
If `val` is nonzero, the stored value is one, otherwise it is zero.

*Returns:* `*this`.

``` cpp
bitset<N>& reset() noexcept;
```

*Effects:* Resets all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& reset(size_t pos);
```

*Requires:* `pos` is valid

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Effects:* Resets the bit at position `pos` in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N> operator~() const noexcept;
```

*Effects:* Constructs an object `x` of class `bitset<N>` and initializes
it with `*this`.

*Returns:* `x.flip()`.

``` cpp
bitset<N>& flip() noexcept;
```

*Effects:* Toggles all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& flip(size_t pos);
```

*Requires:* `pos` is valid

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Effects:* Toggles the bit at position `pos` in `*this`.

*Returns:* `*this`.

``` cpp
unsigned long to_ulong() const;
```

*Throws:* `overflow_error`

if the integral value `x` corresponding to the bits in `*this` cannot be
represented as type `unsigned long`.

*Returns:* `x`.

``` cpp
unsigned long long to_ullong() const;
```

*Throws:* `overflow_error` if the integral value `x` corresponding to
the bits in `*this` cannot be represented as type `unsigned long long`.

*Returns:* `x`.

``` cpp
template <class charT = char,
    class traits = char_traits<charT>,
    class Allocator = allocator<charT> >
  basic_string<charT, traits, Allocator>
  to_string(charT zero = charT('0'), charT one = charT('1')) const;
```

*Effects:* Constructs a string object of the appropriate type and
initializes it to a string of length `N` characters. Each character is
determined by the value of its corresponding bit position in `*this`.
Character position `N - 1` corresponds to bit position zero. Subsequent
decreasing character positions correspond to increasing bit positions.
Bit value zero becomes the character `zero`, bit value one becomes the
character `one`.

*Returns:* The created object.

``` cpp
size_t count() const noexcept;
```

*Returns:* A count of the number of bits set in `*this`.

``` cpp
constexpr size_t size() const noexcept;
```

*Returns:* `N`.

``` cpp
bool operator==(const bitset<N>& rhs) const noexcept;
```

*Returns:* `true` if the value of each bit in `*this` equals the value
of the corresponding bit in `rhs`.

``` cpp
bool operator!=(const bitset<N>& rhs) const noexcept;
```

*Returns:* `true` if `!(*this == rhs)`.

``` cpp
bool test(size_t pos) const;
```

*Requires:* `pos` is valid

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one.

``` cpp
bool all() const noexcept;
```

*Returns:* `count() == size()`

``` cpp
bool any() const noexcept;
```

*Returns:* `count() != 0`

``` cpp
bool none() const noexcept;
```

*Returns:* `count() == 0`

``` cpp
bitset<N> operator<<(size_t pos) const noexcept;
```

*Returns:* `bitset<N>(*this) ``= pos`.

``` cpp
bitset<N> operator>>(size_t pos) const noexcept;
```

*Returns:* `bitset<N>(*this) ``= pos`.

``` cpp
constexpr bool operator[](size_t pos) const;
```

*Requires:* `pos` shall be valid.

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one, otherwise `false`.

*Throws:* Nothing.

``` cpp
bitset<N>::reference operator[](size_t pos);
```

*Requires:* `pos` shall be valid.

*Returns:* An object of type `bitset<N>::reference` such that
`(*this)[pos] == this->test(pos)`, and such that `(*this)[pos] = val` is
equivalent to `this->set(pos, val)`.

*Throws:* Nothing.

For the purpose of determining the presence of a data
race ([[intro.multithread]]), any access or update through the
resulting reference potentially accesses or modifies, respectively, the
entire underlying bitset.

### `bitset` hash support <a id="bitset.hash">[[bitset.hash]]</a>

``` cpp
template <size_t N> struct hash<bitset<N> >;
```

The template specialization shall meet the requirements of class
template `hash` ([[unord.hash]]).

### `bitset` operators <a id="bitset.operators">[[bitset.operators]]</a>

``` cpp
bitset<N> operator&(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) &= rhs`.

``` cpp
bitset<N> operator|(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) |= rhs`.

``` cpp
bitset<N> operator^(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) ^= rhs`.

``` cpp
template <class charT, class traits, size_t N>
  basic_istream<charT, traits>&
  operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
```

A formatted input function ([[istream.formatted]]).

*Effects:* Extracts up to `N` characters from `is`. Stores these
characters in a temporary object `str` of type
`basic_string<charT, traits>`, then evaluates the expression
`x = bitset<N>(str)`. Characters are extracted and stored until any of
the following occurs:

- `N` characters have been extracted and stored;
- end-of-file occurs on the input sequence;
- the next input character is neither `is.widen(’0’)` nor
  `is.widen(’1’)` (in which case the input character is not extracted).

If no characters are stored in `str`, calls
`is.setstate(ios_base::failbit)` (which may throw
`ios_base::failure` ([[iostate.flags]])).

*Returns:* `is`.

``` cpp
template <class charT, class traits, size_t N>
  basic_ostream<charT, traits>&
  operator<<(basic_ostream<charT, traits>& os, const bitset<N>& x);
```

*Returns:*

``` cpp
os \shl x.template to_string<charT,traits,allocator<charT> >(
  use_facet<ctype<charT> >(os.getloc()).widen('0'),
  use_facet<ctype<charT> >(os.getloc()).widen('1'))
```

(see  [[ostream.formatted]]).

## Memory <a id="memory">[[memory]]</a>

### In general <a id="memory.general">[[memory.general]]</a>

This subclause describes the contents of the header `<memory>` (
[[memory.syn]]) and some of the contents of the C headers `<cstdlib>`
and `<cstring>` ([[c.malloc]]).

### Header `<memory>` synopsis <a id="memory.syn">[[memory.syn]]</a>

The header `<memory>` defines several types and function templates that
describe properties of pointers and pointer-like types, manage memory
for containers and other template types, and construct multiple objects
in uninitialized memory buffers ([[pointer.traits]]–
[[specialized.algorithms]]). The header also defines the templates
`unique_ptr`, `shared_ptr`, `weak_ptr`, and various function templates
that operate on objects of these types ([[smartptr]]).

``` cpp
namespace std {
  // [pointer.traits], pointer traits
  template <class Ptr> struct pointer_traits;
  template <class T> struct pointer_traits<T*>;

  // [util.dynamic.safety], pointer safety
  enum class pointer_safety { relaxed, preferred, strict };
  void declare_reachable(void* p);
  template <class T> T* undeclare_reachable(T* p);
  void declare_no_pointers(char* p, size_t n);
  void undeclare_no_pointers(char* p, size_t n);
  pointer_safety get_pointer_safety() noexcept;

  // [ptr.align], pointer alignment function
  void* align(std::size_t alignment, std::size_t size,
    void*& ptr, std::size_t& space);

  // [allocator.tag], allocator argument tag
  struct allocator_arg_t { };
  constexpr allocator_arg_t allocator_arg{};

  // [allocator.uses], uses_allocator
  template <class T, class Alloc> struct uses_allocator;

  // [allocator.traits], allocator traits
  template <class Alloc> struct allocator_traits;

  // [default.allocator], the default allocator:
  template <class T> class allocator;
  template <> class allocator<void>;
  template <class T, class U>
    bool operator==(const allocator<T>&, const allocator<U>&) noexcept;
  template <class T, class U>
    bool operator!=(const allocator<T>&, const allocator<U>&) noexcept;

  // [storage.iterator], raw storage iterator:
  template <class OutputIterator, class T> class raw_storage_iterator;

  // [temporary.buffer], temporary buffers:
  template <class T>
    pair<T*,ptrdiff_t> get_temporary_buffer(ptrdiff_t n) noexcept;
  template <class T>
    void return_temporary_buffer(T* p);

  // [specialized.algorithms], specialized algorithms:
  template <class T> T* addressof(T& r) noexcept;
  template <class InputIterator, class ForwardIterator>
    ForwardIterator uninitialized_copy(InputIterator first, InputIterator last,
                                       ForwardIterator result);
  template <class InputIterator, class Size, class ForwardIterator>
    ForwardIterator uninitialized_copy_n(InputIterator first, Size n,
                                         ForwardIterator result);
  template <class ForwardIterator, class T>
    void uninitialized_fill(ForwardIterator first, ForwardIterator last,
                            const T& x);
  template <class ForwardIterator, class Size, class T>
    ForwardIterator uninitialized_fill_n(ForwardIterator first, Size n, const T& x);

  // [unique.ptr] class template unique_ptr:
  template <class T> struct default_delete;
  template <class T> struct default_delete<T[]>;
  template <class T, class D = default_delete<T>> class unique_ptr;
  template <class T, class D> class unique_ptr<T[], D>;

  template <class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
  template <class T> unique_ptr<T> make_unique(size_t n);
  template <class T, class... Args> unspecified make_unique(Args&&...) = delete;

  template <class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;

  template <class T1, class D1, class T2, class D2>
    bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator!=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);

  template <class T, class D>
    bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator==(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator!=(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator!=(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator<(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<=(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>=(nullptr_t, const unique_ptr<T, D>& y);

  // [util.smartptr.weakptr], class bad_weak_ptr:
  class bad_weak_ptr;

  // [util.smartptr.shared], class template shared_ptr:
  template<class T> class shared_ptr;

  // [util.smartptr.shared.create], shared_ptr creation
  template<class T, class... Args> shared_ptr<T> make_shared(Args&&... args);
  template<class T, class A, class... Args>
    shared_ptr<T> allocate_shared(const A& a, Args&&... args);

  // [util.smartptr.shared.cmp], shared_ptr comparisons:
  template<class T, class U>
    bool operator==(shared_ptr<T> const& a, shared_ptr<U> const& b) noexcept;
  template<class T, class U>
    bool operator!=(shared_ptr<T> const& a, shared_ptr<U> const& b) noexcept;
  template<class T, class U>
    bool operator<(shared_ptr<T> const& a, shared_ptr<U> const& b) noexcept;
  template<class T, class U>
    bool operator>(shared_ptr<T> const& a, shared_ptr<U> const& b) noexcept;
  template<class T, class U>
    bool operator<=(shared_ptr<T> const& a, shared_ptr<U> const& b) noexcept;
  template<class T, class U>
    bool operator>=(shared_ptr<T> const& a, shared_ptr<U> const& b) noexcept;

  template <class T>
    bool operator==(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator==(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator!=(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator!=(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator<(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator<(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator<=(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator<=(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator>(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator>(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator>=(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator>=(nullptr_t, const shared_ptr<T>& y) noexcept;

  // [util.smartptr.shared.spec], shared_ptr specialized algorithms:
  template<class T> void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.cast], shared_ptr casts:
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(shared_ptr<U> const& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(shared_ptr<U> const& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(shared_ptr<U> const& r) noexcept;

  // [util.smartptr.getdeleter], shared_ptr get_deleter:
  template<class D, class T> D* get_deleter(shared_ptr<T> const& p) noexcept;

  // [util.smartptr.shared.io], shared_ptr I/O:
  template<class E, class T, class Y>
    basic_ostream<E, T>& operator<< (basic_ostream<E, T>& os, shared_ptr<Y> const& p);

  // [util.smartptr.weak], class template weak_ptr:
  template<class T> class weak_ptr;

  // [util.smartptr.weak.spec], weak_ptr specialized algorithms:
  template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;

  // [util.smartptr.ownerless], class template owner_less:
  template<class T> class owner_less;

  // [util.smartptr.enab], class template enable_shared_from_this:
  template<class T> class enable_shared_from_this;

  // [util.smartptr.shared.atomic], shared_ptr atomic access:
  template<class T>
    bool atomic_is_lock_free(const shared_ptr<T>* p);

  template<class T>
    shared_ptr<T> atomic_load(const shared_ptr<T>* p);
  template<class T>
    shared_ptr<T> atomic_load_explicit(const shared_ptr<T>* p, memory_order mo);

  template<class T>
    void atomic_store(shared_ptr<T>* p, shared_ptr<T> r);
  template<class T>
    void atomic_store_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);

  template<class T>
    shared_ptr<T> atomic_exchange(shared_ptr<T>* p, shared_ptr<T> r);
  template<class T>
    shared_ptr<T> atomic_exchange_explicit(shared_ptr<T>* p, shared_ptr<T> r,
                                           memory_order mo);

  template<class T>
    bool atomic_compare_exchange_weak(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
  template<class T>
    bool atomic_compare_exchange_strong(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
  template<class T>
    bool atomic_compare_exchange_weak_explicit(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
      memory_order success, memory_order failure);
  template<class T>
    bool atomic_compare_exchange_strong_explicit(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
      memory_order success, memory_order failure);

  // [util.smartptr.hash] hash support
  template <class T> struct hash;
  template <class T, class D> struct hash<unique_ptr<T, D> >;
  template <class T> struct hash<shared_ptr<T> >;

  // [depr.auto.ptr], auto_ptr (deprecated)
  template <class X> class auto_ptr;
}
```

### Pointer traits <a id="pointer.traits">[[pointer.traits]]</a>

The class template `pointer_traits` supplies a uniform interface to
certain attributes of pointer-like types.

``` cpp
namespace std {
  template <class Ptr> struct pointer_traits {
    typedef Ptr       pointer;
    typedef see below element_type;
    typedef see below difference_type;

    template <class U> using rebind = see below;

    static pointer pointer_to(see below r);
  };

  template <class T> struct pointer_traits<T*> {
    typedef T*        pointer;
    typedef T         element_type;
    typedef ptrdiff_t difference_type;

    template <class U> using rebind = U*;

    static pointer pointer_to(see below r) noexcept;
  };
}
```

#### Pointer traits member types <a id="pointer.traits.types">[[pointer.traits.types]]</a>

``` cpp
typedef see below element_type;
```

*Type:* `Ptr::element_type` if such a type exists; otherwise, `T` if
`Ptr` is a class template instantiation of the form
`SomePointer<T, Args>`, where `Args` is zero or more type arguments;
otherwise, the specialization is ill-formed.

``` cpp
typedef see below difference_type;
```

*Type:* `Ptr::difference_type` if such a type exists; otherwise,
`std::ptrdiff_t`.

``` cpp
template <class U> using rebind = see below;
```

*Alias template:* `Ptr::rebind<U>` if such a type exists; otherwise,
`SomePointer<U, Args>` if `Ptr` is a class template instantiation of the
form `SomePointer<T, Args>`, where `Args` is zero or more type
arguments; otherwise, the instantiation of `rebind` is ill-formed.

#### Pointer traits member functions <a id="pointer.traits.functions">[[pointer.traits.functions]]</a>

``` cpp
static pointer pointer_traits::pointer_to(see below r);
static pointer pointer_traits<T*>::pointer_to(see below r) noexcept;
```

If `element_type` is (possibly cv-qualified) `void`, the type of `r` is
unspecified; otherwise, it is `element_type&`.

*Returns:* The first member function returns a pointer to `r` obtained
by calling `Ptr::pointer_to(r)` through which indirection is valid; an
instantiation of this function is ill-formed if `Ptr` does not have a
matching `pointer_to` static member function. The second member function
returns `std::addressof(r)`.

### Pointer safety <a id="util.dynamic.safety">[[util.dynamic.safety]]</a>

A complete object is *declared reachable* while the number of calls to
`declare_reachable` with an argument referencing the object exceeds the
number of calls to `undeclare_reachable` with an argument referencing
the object.

``` cpp
void declare_reachable(void* p);
```

*Requires:* `p` shall be a safely-derived
pointer ([[basic.stc.dynamic.safety]]) or a null pointer value.

*Effects:* If `p` is not null, the complete object referenced by `p` is
subsequently declared reachable ([[basic.stc.dynamic.safety]]).

*Throws:* May throw `std::bad_alloc` if the system cannot allocate
additional memory that may be required to track objects declared
reachable.

``` cpp
template <class T> T* undeclare_reachable(T* p);
```

*Requires:* If `p` is not null, the complete object referenced by `p`
shall have been previously declared reachable, and shall be
live ([[basic.life]]) from the time of the call until the last
`undeclare_reachable(p)` call on the object.

*Returns:* A safely derived copy of `p` which shall compare equal to
`p`.

*Throws:* Nothing.

It is expected that calls to `declare_reachable(p)` will consume a small
amount of memory in addition to that occupied by the referenced object
until the matching call to `undeclare_reachable(p)` is encountered. Long
running programs should arrange that calls are matched.

``` cpp
void declare_no_pointers(char* p, size_t n);
```

*Requires:* No bytes in the specified range are currently registered
with `declare_no_pointers()`. If the specified range is in an allocated
object, then it must be entirely within a single allocated object. The
object must be live until the corresponding `undeclare_no_pointers()`
call. In a garbage-collecting implementation, the fact that a region in
an object is registered with `declare_no_pointers()` should not prevent
the object from being collected.

*Effects:* The `n` bytes starting at `p` no longer contain traceable
pointer locations, independent of their type. Hence indirection through
a pointer located there is undefined if the object it points to was
created by global `operator new` and not previously declared reachable.
This may be used to inform a garbage collector or leak detector that
this region of memory need not be traced.

*Throws:* Nothing.

Under some conditions implementations may need to allocate memory.
However, the request can be ignored if memory allocation fails.

``` cpp
void undeclare_no_pointers(char* p, size_t n);
```

*Requires:* The same range must previously have been passed to
`declare_no_pointers()`.

*Effects:* Unregisters a range registered with `declare_no_pointers()`
for destruction. It must be called before the lifetime of the object
ends.

*Throws:* Nothing.

``` cpp
pointer_safety get_pointer_safety() noexcept;
```

*Returns:* `pointer_safety::strict` if the implementation has strict
pointer safety ([[basic.stc.dynamic.safety]]). It is implementation
defined whether `get_pointer_safety` returns `pointer_safety::relaxed`
or `pointer_safety::preferred` if the implementation has relaxed pointer
safety.[^1]

### Align <a id="ptr.align">[[ptr.align]]</a>

``` cpp
void* align(std::size_t alignment, std::size_t size,
    void*& ptr, std::size_t& space);
```

*Effects:* If it is possible to fit `size` bytes of storage aligned by
`alignment` into the buffer pointed to by `ptr` with length `space`, the
function updates `ptr` to point to the first possible address of such
storage and decreases `space` by the number of bytes used for alignment.
Otherwise, the function does nothing.

*Requires:*

- `alignment` shall be a fundamental alignment value or an extended
  alignment value supported by the implementation in this context
- `ptr` shall point to contiguous storage of at least `space` bytes

*Returns:* A null pointer if the requested aligned buffer would not fit
into the available space, otherwise the adjusted value of `ptr`.

The function updates its `ptr` and `space` arguments so that it can be
called repeatedly with possibly different `alignment` and `size`
arguments for the same buffer.

### Allocator argument tag <a id="allocator.tag">[[allocator.tag]]</a>

``` cpp
namespace std {
  struct allocator_arg_t { };
  constexpr allocator_arg_t allocator_arg{};
}
```

The `allocator_arg_t` struct is an empty structure type used as a unique
type to disambiguate constructor and function overloading. Specifically,
several types (see `tuple`  [[tuple]]) have constructors with
`allocator_arg_t` as the first argument, immediately followed by an
argument of a type that satisfies the `Allocator` requirements (
[[allocator.requirements]]).

### `uses_allocator` <a id="allocator.uses">[[allocator.uses]]</a>

#### `uses_allocator` trait <a id="allocator.uses.trait">[[allocator.uses.trait]]</a>

``` cpp
template <class T, class Alloc> struct uses_allocator;
```

automatically detects whether `T` has a nested `allocator_type` that is
convertible from `Alloc`. Meets the BinaryTypeTrait
requirements ([[meta.rqmts]]). The implementation shall provide a
definition that is derived from `true_type` if a type
`T::allocator_type` exists and
`is_convertible<Alloc, T::allocator_type>::value != false`, otherwise it
shall be derived from `false_type`. A program may specialize this
template to derive from `true_type` for a user-defined type `T` that
does not have a nested `allocator_type` but nonetheless can be
constructed with an allocator where either:

- the first argument of a constructor has type `allocator_arg_t` and the
  second argument has type `Alloc` or
- the last argument of a constructor has type `Alloc`.

#### uses-allocator construction <a id="allocator.uses.construction">[[allocator.uses.construction]]</a>

*Uses-allocator construction* with allocator `Alloc` refers to the
construction of an object `obj` of type `T`, using constructor arguments
`v1, v2, ..., vN` of types `V1, V2, ..., VN`, respectively, and an
allocator `alloc` of type `Alloc`, according to the following rules:

- if `uses_allocator<T, Alloc>::value` is `false` and
  `is_constructible<T, V1, V2, ..., VN>::value` is `true`, then `obj` is
  initialized as `obj(v1, v2, ..., vN)`;
- otherwise, if `uses_allocator<T, Alloc>::value` is `true` and
  `is_constructible<T, allocator_arg_t, Alloc,`
  `V1, V2, ..., VN>::value` is `true`, then `obj` is initialized as
  `obj(allocator_arg, alloc, v1,
  v2, ..., vN)`;
- otherwise, if `uses_allocator<T, Alloc>::value` is `true` and
  `is_constructible<T, V1, V2, ..., VN, Alloc>::value` is `true`, then
  `obj` is initialized as `obj(v1, v2, ..., vN, alloc)`;
- otherwise, the request for uses-allocator construction is ill-formed.
  An error will result if `uses_allocator<T, Alloc>::value` is `true`
  but the specific constructor does not take an allocator. This
  definition prevents a silent failure to pass the allocator to an
  element.

### Allocator traits <a id="allocator.traits">[[allocator.traits]]</a>

The class template `allocator_traits` supplies a uniform interface to
all allocator types. An allocator cannot be a non-class type, however,
even if `allocator_traits` supplies the entire required interface. Thus,
it is always possible to create a derived class from an allocator.

``` cpp
namespace std {
  template <class Alloc> struct allocator_traits {
    typedef Alloc allocator_type;

    typedef typename Alloc::value_type value_type;

    typedef see below pointer;
    typedef see below const_pointer;
    typedef see below void_pointer;
    typedef see below const_void_pointer;

    typedef see below difference_type;
    typedef see below size_type;

    typedef see below propagate_on_container_copy_assignment;
    typedef see below propagate_on_container_move_assignment;
    typedef see below propagate_on_container_swap;

    template <class T> using rebind_alloc = see below;
    template <class T> using rebind_traits = allocator_traits<rebind_alloc<T> >;

    static pointer allocate(Alloc& a, size_type n);
    static pointer allocate(Alloc& a, size_type n, const_void_pointer hint);

    static void deallocate(Alloc& a, pointer p, size_type n);

    template <class T, class... Args>
      static void construct(Alloc& a, T* p, Args&&... args);

    template <class T>
      static void destroy(Alloc& a, T* p);

    static size_type max_size(const Alloc& a) noexcept;

    static Alloc select_on_container_copy_construction(const Alloc& rhs);
  };
}
```

#### Allocator traits member types <a id="allocator.traits.types">[[allocator.traits.types]]</a>

``` cpp
typedef see below pointer;
```

*Type:* `Alloc::pointer` if such a type exists; otherwise,
`value_type*`.

``` cpp
typedef see below const_pointer;
```

*Type:* `Alloc::const_pointer` if such a type exists; otherwise,
`pointer_traits<pointer>::rebind<const value_type>`.

``` cpp
typedef see below void_pointer;
```

*Type:* `Alloc::void_pointer` if such a type exists; otherwise,
`pointer_traits<pointer>::rebind<void>`.

``` cpp
typedef see below const_void_pointer;
```

*Type:* `Alloc::const_void_pointer` if such a type exists; otherwise,
`pointer_traits<pointer>::rebind<const void>`.

``` cpp
typedef see below difference_type;
```

*Type:* `Alloc::difference_type` if such a type exists; otherwise,
`pointer_traits<pointer>::difference_type`.

``` cpp
typedef see below size_type;
```

*Type:* `Alloc::size_type` if such a type exists; otherwise,
`make_unsigned_t<difference_type>`.

``` cpp
typedef see below propagate_on_container_copy_assignment;
```

*Type:* `Alloc::propagate_on_container_copy_assignment` if such a type
exists, otherwise `false_type`.

``` cpp
typedef see below propagate_on_container_move_assignment;
```

*Type:* `Alloc::propagate_on_container_move_assignment` if such a type
exists, otherwise `false_type`.

``` cpp
typedef see below propagate_on_container_swap;
```

*Type:* `Alloc::propagate_on_container_swap` if such a type exists,
otherwise `false_type`.

``` cpp
template <class T> using rebind_alloc = see below;
```

*Alias template:* `Alloc::rebind<T>::other` if such a type exists;
otherwise, `Alloc<T, Args>` if `Alloc` is a class template instantiation
of the form `Alloc<U, Args>`, where `Args` is zero or more type
arguments; otherwise, the instantiation of `rebind_alloc` is ill-formed.

#### Allocator traits static member functions <a id="allocator.traits.members">[[allocator.traits.members]]</a>

``` cpp
static pointer allocate(Alloc& a, size_type n);
```

*Returns:* `a.allocate(n)`.

``` cpp
static pointer allocate(Alloc& a, size_type n, const_void_pointer hint);
```

*Returns:* `a.allocate(n, hint)` if that expression is well-formed;
otherwise, `a.allocate(n)`.

``` cpp
static void deallocate(Alloc& a, pointer p, size_type n);
```

*Effects:* calls `a.deallocate(p, n)`.

*Throws:* Nothing.

``` cpp
template <class T, class... Args>
  static void construct(Alloc& a, T* p, Args&&... args);
```

*Effects:* calls `a.construct(p, std::forward<Args>(args)...)` if that
call is well-formed; otherwise, invokes
`::new (static_cast<void*>(p)) T(std::forward<Args>(args)...)`.

``` cpp
template <class T>
  static void destroy(Alloc& a, T* p);
```

*Effects:* calls `a.destroy(p)` if that call is well-formed; otherwise,
invokes `p->~T()`.

``` cpp
static size_type max_size(const Alloc& a) noexcept;
```

*Returns:* `a.max_size()` if that expression is well-formed; otherwise,
`numeric_limits<size_type>::max()`.

``` cpp
static Alloc select_on_container_copy_construction(const Alloc& rhs);
```

*Returns:* `rhs.select_on_container_copy_construction()` if that
expression is well-formed; otherwise, `rhs`.

### The default allocator <a id="default.allocator">[[default.allocator]]</a>

``` cpp
namespace std {
  template <class T> class allocator;

  // specialize for void:
  template <> class allocator<void> {
  public:
    typedef void*   pointer;
    typedef const void* const_pointer;
    // reference-to-void members are impossible.
    typedef void  value_type;
    template <class U> struct rebind { typedef allocator<U> other; };
  };

  template <class T> class allocator {
   public:
    typedef size_t    size_type;
    typedef ptrdiff_t difference_type;
    typedef T*        pointer;
    typedef const T*  const_pointer;
    typedef T&        reference;
    typedef const T&  const_reference;
    typedef T         value_type;
    template <class U> struct rebind { typedef allocator<U> other; };
    typedef true_type propagate_on_container_move_assignment;

    allocator() noexcept;
    allocator(const allocator&) noexcept;
    template <class U> allocator(const allocator<U>&) noexcept;
   ~allocator();

    pointer address(reference x) const noexcept;
    const_pointer address(const_reference x) const noexcept;

    pointer allocate(
      size_type, allocator<void>::const_pointer hint = 0);
    void deallocate(pointer p, size_type n);
    size_type max_size() const noexcept;

    template<class U, class... Args>
      void construct(U* p, Args&&... args);
    template <class U>
      void destroy(U* p);
  };
}
```

#### `allocator` members <a id="allocator.members">[[allocator.members]]</a>

Except for the destructor, member functions of the default allocator
shall not introduce data races ([[intro.multithread]]) as a result of
concurrent calls to those member functions from different threads. Calls
to these functions that allocate or deallocate a particular unit of
storage shall occur in a single total order, and each such deallocation
call shall happen before the next allocation (if any) in this order.

``` cpp
pointer address(reference x) const noexcept;
```

*Returns:* The actual address of the object referenced by `x`, even in
the presence of an overloaded operator&.

``` cpp
const_pointer address(const_reference x) const noexcept;
```

*Returns:* The actual address of the object referenced by `x`, even in
the presence of an overloaded operator&.

``` cpp
pointer allocate(size_type n, allocator<void>::const_pointer hint = 0);
```

In a container member function, the address of an adjacent element is
often a good choice to pass for the `hint` argument.

*Returns:* A pointer to the initial element of an array of storage of
size `n` `* sizeof(T)`, aligned appropriately for objects of type `T`.
It is *implementation-defined* whether over-aligned types are
supported ([[basic.align]]).

the storage is obtained by calling
`::operator new(std::size_t)` ([[new.delete]]), but it is unspecified
when or how often this function is called. The use of `hint` is
unspecified, but intended as an aid to locality if an implementation so
desires.

*Throws:* `bad_alloc` if the storage cannot be obtained.

``` cpp
void deallocate(pointer p, size_type n);
```

*Requires:* `p` shall be a pointer value obtained from `allocate()`. `n`
shall equal the value passed as the first argument to the invocation of
allocate which returned `p`.

*Effects:* Deallocates the storage referenced by `p` .

*Remarks:* Uses
`::operator delete(void*, std::size_t)` ([[new.delete]]), but it is
unspecified when this function is called.

``` cpp
size_type max_size() const noexcept;
```

*Returns:* The largest value *N* for which the call `allocate(N,0)`
might succeed.

``` cpp
template <class U, class... Args>
  void construct(U* p, Args&&... args);
```

*Effects:* `::new((void *)p) U(std::forward<Args>(args)...)`

``` cpp
template <class U>
  void destroy(U* p);
```

*Effects:* `p->~U()`

#### `allocator` globals <a id="allocator.globals">[[allocator.globals]]</a>

``` cpp
template <class T1, class T2>
  bool operator==(const allocator<T1>&, const allocator<T2>&) noexcept;
```

*Returns:* `true`.

``` cpp
template <class T1, class T2>
  bool operator!=(const allocator<T1>&, const allocator<T2>&) noexcept;
```

*Returns:* `false`.

### Raw storage iterator <a id="storage.iterator">[[storage.iterator]]</a>

`raw_storage_iterator` is provided to enable algorithms to store their
results into uninitialized memory. The template parameter
`OutputIterator` is required to have its `operator*` return an object
for which `operator&` is defined and returns a pointer to `T`, and is
also required to satisfy the requirements of an output iterator (
[[output.iterators]]).

``` cpp
namespace std {
  template <class OutputIterator, class T>
  class raw_storage_iterator
    : public iterator<output_iterator_tag,void,void,void,void> {
  public:
    explicit raw_storage_iterator(OutputIterator x);

    raw_storage_iterator& operator*();
    raw_storage_iterator& operator=(const T& element);
    raw_storage_iterator& operator++();
    raw_storage_iterator  operator++(int);
  };
}
```

``` cpp
explicit raw_storage_iterator(OutputIterator x);
```

*Effects:* Initializes the iterator to point to the same value to which
`x` points.

``` cpp
raw_storage_iterator& operator*();
```

*Returns:* `*this`

``` cpp
raw_storage_iterator& operator=(const T& element);
```

*Effects:* Constructs a value from `element` at the location to which
the iterator points.

*Returns:* A reference to the iterator.

``` cpp
raw_storage_iterator& operator++();
```

*Effects:* Pre-increment: advances the iterator and returns a reference
to the updated iterator.

``` cpp
raw_storage_iterator operator++(int);
```

*Effects:* Post-increment: advances the iterator and returns the old
value of the iterator.

### Temporary buffers <a id="temporary.buffer">[[temporary.buffer]]</a>

``` cpp
template <class T>
  pair<T*, ptrdiff_t> get_temporary_buffer(ptrdiff_t n) noexcept;
```

*Effects:* Obtains a pointer to storage sufficient to store up to `n`
adjacent `T` objects. It is *implementation-defined* whether
over-aligned types are supported ([[basic.align]]).

*Returns:* A `pair` containing the buffer’s address and capacity (in the
units of `sizeof(T)`), or a pair of 0 values if no storage can be
obtained or if `n <= 0`.

``` cpp
template <class T> void return_temporary_buffer(T* p);
```

*Effects:* Deallocates the buffer to which `p` points.

*Requires:* The buffer shall have been previously allocated by
`get_temporary_buffer`.

### Specialized algorithms <a id="specialized.algorithms">[[specialized.algorithms]]</a>

All the iterators that are used as template parameters in the following
algorithms are required to have their `operator*` return an object for
which `operator&` is defined and returns a pointer to `T`. In the
algorithm `uninitialized_copy`, the template parameter `InputIterator`
is required to satisfy the requirements of an input iterator (
[[input.iterators]]). In all of the following algorithms, the template
parameter `ForwardIterator` is required to satisfy the requirements of a
forward iterator ([[forward.iterators]]), and is required to have the
property that no exceptions are thrown from increment, assignment,
comparison, or indirection through valid iterators. In the following
algorithms, if an exception is thrown there are no effects.

#### `addressof` <a id="specialized.addressof">[[specialized.addressof]]</a>

``` cpp
template <class T> T* addressof(T& r) noexcept;
```

*Returns:* The actual address of the object or function referenced by
`r`, even in the presence of an overloaded `operator&`.

#### `uninitialized_copy` <a id="uninitialized.copy">[[uninitialized.copy]]</a>

``` cpp
template <class InputIterator, class ForwardIterator>
  ForwardIterator uninitialized_copy(InputIterator first, InputIterator last,
                                     ForwardIterator result);
```

*Effects:*

``` cpp
for (; first != last; ++result, ++first)
  ::new (static_cast<void*>(&*result))
    typename iterator_traits<ForwardIterator>::value_type(*first);
```

*Returns:* `result`

``` cpp
template <class InputIterator, class Size, class ForwardIterator>
  ForwardIterator uninitialized_copy_n(InputIterator first, Size n,
                                       ForwardIterator result);
```

*Effects:*

``` cpp
for ( ; n > 0; ++result, ++first, --n) {
  ::new (static_cast<void*>(&*result))
    typename iterator_traits<ForwardIterator>::value_type(*first);
}
```

*Returns:* `result`

#### `uninitialized_fill` <a id="uninitialized.fill">[[uninitialized.fill]]</a>

``` cpp
template <class ForwardIterator, class T>
  void uninitialized_fill(ForwardIterator first, ForwardIterator last,
                          const T& x);
```

*Effects:*

``` cpp
for (; first != last; ++first)
  ::new (static_cast<void*>(&*first))
    typename iterator_traits<ForwardIterator>::value_type(x);
```

#### `uninitialized_fill_n` <a id="uninitialized.fill.n">[[uninitialized.fill.n]]</a>

``` cpp
template <class ForwardIterator, class Size, class T>
  ForwardIterator uninitialized_fill_n(ForwardIterator first, Size n, const T& x);
```

*Effects:*

``` cpp
for (; n--; ++first)
  ::new (static_cast<void*>(&*first))
    typename iterator_traits<ForwardIterator>::value_type(x);
return first;
```

### C library <a id="c.malloc">[[c.malloc]]</a>

Table  [[tab:util.hdr.cstdlib]] describes the header `<cstdlib>`.

The contents are the same as the Standard C library header `<stdlib.h>,`
with the following changes:

The functions `calloc()`, `malloc()`, and `realloc()` do not attempt to
allocate storage by calling `::operator new()` ([[support.dynamic]]).

The function `free()` does not attempt to deallocate storage by calling
`::operator delete()`.

ISO C Clause 7.11.2.

Storage allocated directly with `malloc()`, `calloc()`, or `realloc()`
is implicitly declared reachable (see  [[basic.stc.dynamic.safety]]) on
allocation, ceases to be declared reachable on deallocation, and need
not cease to be declared reachable as the result of an
`undeclare_reachable()` call. This allows existing C libraries to remain
unaffected by restrictions on pointers that are not safely derived, at
the expense of providing far fewer garbage collection and leak detection
options for `malloc()`-allocated objects. It also allows `malloc()` to
be implemented with a separate allocation arena, bypassing the normal
`declare_reachable()` implementation. The above functions should never
intentionally be used as a replacement for `declare_reachable()`, and
newly written code is strongly encouraged to treat memory allocated with
these functions as though it were allocated with `operator new`.

Table  [[tab:util.hdr.cstring]] describes the header `<cstring>`.

The contents are the same as the Standard C library header `<string.h>`,
with the change to `memchr()` specified in  [[c.strings]].

ISO C Clause 7.11.2.

## Smart pointers <a id="smartptr">[[smartptr]]</a>

### Class template `unique_ptr` <a id="unique.ptr">[[unique.ptr]]</a>

A *unique pointer* is an object that owns another object and manages
that other object through a pointer. More precisely, a unique pointer is
an object *u* that stores a pointer to a second object *p* and will
dispose of *p* when *u* is itself destroyed (e.g., when leaving block
scope ([[stmt.dcl]])). In this context, *u* is said to *own* `p`.

The mechanism by which *u* disposes of *p* is known as *p*’s associated
*deleter*, a function object whose correct invocation results in *p*’s
appropriate disposition (typically its deletion).

Let the notation *u.p* denote the pointer stored by *u*, and let *u.d*
denote the associated deleter. Upon request, *u* can *reset* (replace)
*u.p* and *u.d* with another pointer and deleter, but must properly
dispose of its owned object via the associated deleter before such
replacement is considered completed.

Additionally, *u* can, upon request, *transfer ownership* to another
unique pointer *u2*. Upon completion of such a transfer, the following
postconditions hold:

- *u2.p* is equal to the pre-transfer *u.p*,
- *u.p* is equal to `nullptr`, and
- if the pre-transfer *u.d* maintained state, such state has been
  transferred to *u2.d*.

As in the case of a reset, *u2* must properly dispose of its
pre-transfer owned object via the pre-transfer associated deleter before
the ownership transfer is considered complete. A deleter’s state need
never be copied, only moved or swapped as ownership is transferred.

Each object of a type `U` instantiated from the `unique_ptr` template
specified in this subclause has the strict ownership semantics,
specified above, of a unique pointer. In partial satisfaction of these
semantics, each such `U` is `MoveConstructible` and `MoveAssignable`,
but is not `CopyConstructible` nor `CopyAssignable`. The template
parameter `T` of `unique_ptr` may be an incomplete type.

The uses of `unique_ptr` include providing exception safety for
dynamically allocated memory, passing ownership of dynamically allocated
memory to a function, and returning dynamically allocated memory from a
function.

``` cpp
namespace std {
  template<class T> struct default_delete;
  template<class T> struct default_delete<T[]>;

  template<class T, class D = default_delete<T>> class unique_ptr;
  template<class T, class D> class unique_ptr<T[], D>;

  template<class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
  template<class T> unique_ptr<T> make_unique(size_t n);
  template<class T, class... Args> unspecified make_unique(Args&&...) = delete;

  template<class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;

  template<class T1, class D1, class T2, class D2>
    bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator!=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);

  template <class T, class D>
    bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator==(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator!=(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator!=(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator<(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<=(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>=(nullptr_t, const unique_ptr<T, D>& y);

}
```

#### Default deleters <a id="unique.ptr.dltr">[[unique.ptr.dltr]]</a>

##### In general <a id="unique.ptr.dltr.general">[[unique.ptr.dltr.general]]</a>

The class template `default_delete` serves as the default deleter
(destruction policy) for the class template `unique_ptr`.

The template parameter `T` of `default_delete` may be an incomplete
type.

##### `default_delete` <a id="unique.ptr.dltr.dflt">[[unique.ptr.dltr.dflt]]</a>

``` cpp
namespace std {
  template <class T> struct default_delete {
    constexpr default_delete() noexcept = default;
    template <class U> default_delete(const default_delete<U>&) noexcept;
    void operator()(T*) const;
  };
}
```

``` cpp
template <class U> default_delete(const default_delete<U>& other) noexcept;
```

*Effects:* Constructs a `default_delete` object from another
`default_delete<U>` object.

*Remarks:* This constructor shall not participate in overload resolution
unless `U*` is implicitly convertible to `T*`.

``` cpp
void operator()(T* ptr) const;
```

*Effects:* calls `delete` on `ptr`.

*Remarks:* If `T` is an incomplete type, the program is ill-formed.

##### `default_delete<T[]>` <a id="unique.ptr.dltr.dflt1">[[unique.ptr.dltr.dflt1]]</a>

``` cpp
namespace std {
  template <class T> struct default_delete<T[]> {
    constexpr default_delete() noexcept = default;
    void operator()(T*) const;
    template <class U> void operator()(U*) const = delete;
  };
}
```

``` cpp
void operator()(T* ptr) const;
```

*Effects:* calls `delete[]` on `ptr`.

*Remarks:* If T is an incomplete type, the program is ill-formed.

#### `unique_ptr` for single objects <a id="unique.ptr.single">[[unique.ptr.single]]</a>

``` cpp
namespace std {
  template <class T, class D = default_delete<T>> class unique_ptr {
  public:
    typedef see below pointer;
    typedef T element_type;
    typedef D deleter_type;

    // [unique.ptr.single.ctor], constructors
    constexpr unique_ptr() noexcept;
    explicit unique_ptr(pointer p) noexcept;
    unique_ptr(pointer p, see below d1) noexcept;
    unique_ptr(pointer p, see below d2) noexcept;
    unique_ptr(unique_ptr&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept
      : unique_ptr() { }
    template <class U, class E>
      unique_ptr(unique_ptr<U, E>&& u) noexcept;
    template <class U>
      unique_ptr(auto_ptr<U>&& u) noexcept;

    // [unique.ptr.single.dtor], destructor
    ~unique_ptr();

    // [unique.ptr.single.asgn], assignment
    unique_ptr& operator=(unique_ptr&& u) noexcept;
    template <class U, class E> unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
    unique_ptr& operator=(nullptr_t) noexcept;

    // [unique.ptr.single.observers], observers
    add_lvalue_reference_t<T> operator*() const;
    pointer operator->() const noexcept;
    pointer get() const noexcept;
    deleter_type& get_deleter() noexcept;
    const deleter_type& get_deleter() const noexcept;
    explicit operator bool() const noexcept;

    // [unique.ptr.single.modifiers] modifiers
    pointer release() noexcept;
    void reset(pointer p = pointer()) noexcept;
    void swap(unique_ptr& u) noexcept;

    // disable copy from lvalue
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
  };
}
```

The default type for the template parameter `D` is `default_delete`. A
client-supplied template argument `D` shall be a function object type (
[[function.objects]]), lvalue-reference to function, or lvalue-reference
to function object type for which, given a value `d` of type `D` and a
value `ptr` of type `unique_ptr<T, D>::pointer`, the expression `d(ptr)`
is valid and has the effect of disposing of the pointer as appropriate
for that deleter.

If the deleter’s type `D` is not a reference type, `D` shall satisfy the
requirements of `Destructible` (Table  [[destructible]]).

If the type `remove_reference_t<D>::pointer` exists, then `unique_ptr<T,
D>::pointer` shall be a synonym for `remove_reference_t<D>::pointer`.
Otherwise `unique_ptr<T, D>::pointer` shall be a synonym for `T*`. The
type `unique_ptr<T,
D>::pointer` shall satisfy the requirements of `NullablePointer` (
[[nullablepointer.requirements]]).

Given an allocator type `X` ([[allocator.requirements]]) and letting
`A` be a synonym for `allocator_traits<X>`, the types `A::pointer`,
`A::const_pointer`, `A::void_pointer`, and `A::const_void_pointer` may
be used as `unique_ptr<T, D>::pointer`.

##### `unique_ptr` constructors <a id="unique.ptr.single.ctor">[[unique.ptr.single.ctor]]</a>

``` cpp
constexpr unique_ptr() noexcept;
```

*Requires:* `D` shall satisfy the requirements of `DefaultConstructible`
(Table  [[defaultconstructible]]), and that construction shall not throw
an exception.

*Effects:* Constructs a `unique_ptr` object that owns nothing,
value-initializing the stored pointer and the stored deleter.

*Postconditions:* `get() == nullptr`. `get_deleter()` returns a
reference to the stored deleter.

*Remarks:* If this constructor is instantiated with a pointer type or
reference type for the template argument `D`, the program is ill-formed.

``` cpp
explicit unique_ptr(pointer p) noexcept;
```

*Requires:* `D` shall satisfy the requirements of `DefaultConstructible`
(Table  [[defaultconstructible]]), and that construction shall not throw
an exception.

*Effects:* Constructs a `unique_ptr` which owns `p`, initializing the
stored pointer with `p` and value-initializing the stored deleter.

*Postconditions:* `get() == p`. `get_deleter()` returns a reference to
the stored deleter.

*Remarks:* If this constructor is instantiated with a pointer type or
reference type for the template argument `D`, the program is ill-formed.

``` cpp
unique_ptr(pointer p, see below d1) noexcept;
unique_ptr(pointer p, see below d2) noexcept;
```

The signature of these constructors depends upon whether `D` is a
reference type. If `D` is non-reference type `A`, then the signatures
are:

``` cpp
unique_ptr(pointer p, const A& d);
unique_ptr(pointer p, A&& d);
```

If `D` is an lvalue-reference type `A&`, then the signatures are:

``` cpp
unique_ptr(pointer p, A& d);
unique_ptr(pointer p, A&& d);
```

If `D` is an lvalue-reference type `const A&`, then the signatures are:

``` cpp
unique_ptr(pointer p, const A& d);
unique_ptr(pointer p, const A&& d);
```

*Requires:*

- If `D` is not an lvalue-reference type then
  - If `d` is an lvalue or `const` rvalue then the first constructor of
    this pair will be selected. `D` shall satisfy the requirements of
    `CopyConstructible` (Table  [[copyconstructible]]), and the copy
    constructor of `D` shall not throw an exception. This `unique_ptr`
    will hold a copy of `d`.
  - Otherwise, `d` is a non-const rvalue and the second constructor of
    this pair will be selected. `D` shall satisfy the requirements of
    `MoveConstructible` (Table  [[moveconstructible]]), and the move
    constructor of `D` shall not throw an exception. This `unique_ptr`
    will hold a value move constructed from `d`.
- Otherwise `D` is an lvalue-reference type. `d` shall be
  reference-compatible with one of the constructors. If `d` is an
  rvalue, it will bind to the second constructor of this pair and the
  program is ill-formed. The diagnostic could be implemented using a
  `static_assert` which assures that `D` is not a reference type. Else
  `d` is an lvalue and will bind to the first constructor of this pair.
  The type which `D` references need not be `CopyConstructible` nor
  `MoveConstructible`. This `unique_ptr` will hold a `D` which refers to
  the lvalue `d`. `D` may not be an rvalue-reference type.

*Effects:* Constructs a `unique_ptr` object which owns `p`, initializing
the stored pointer with `p` and initializing the deleter as described
above.

*Postconditions:* `get() == p`. `get_deleter()` returns a reference to
the stored deleter. If `D` is a reference type then `get_deleter()`
returns a reference to the lvalue `d`.

``` cpp
D d;
unique_ptr<int, D> p1(new int, D());        // D must be MoveConstructible
unique_ptr<int, D> p2(new int, d);          // D must be CopyConstructible
unique_ptr<int, D&> p3(new int, d);         // p3 holds a reference to d
unique_ptr<int, const D&> p4(new int, D()); // error: rvalue deleter object combined
                                            // with reference deleter type
```

``` cpp
unique_ptr(unique_ptr&& u) noexcept;
```

*Requires:* If `D` is not a reference type, `D` shall satisfy the
requirements of `MoveConstructible` (Table  [[moveconstructible]]).
Construction of the deleter from an rvalue of type `D` shall not throw
an exception.

*Effects:* Constructs a `unique_ptr` by transferring ownership from `u`
to `*this`. If `D` is a reference type, this deleter is copy constructed
from `u`’s deleter; otherwise, this deleter is move constructed from
`u`’s deleter. The deleter constructor can be implemented with
`std::forward<D>`.

*Postconditions:* `get()` yields the value `u.get()` yielded before the
construction. `get_deleter()` returns a reference to the stored deleter
that was constructed from `u.get_deleter()`. If `D` is a reference type
then `get_deleter()` and `u.get_deleter()` both reference the same
lvalue deleter.

``` cpp
template <class U, class E> unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

*Requires:* If `E` is not a reference type, construction of the deleter
from an rvalue of type `E` shall be well formed and shall not throw an
exception. Otherwise, `E` is a reference type and construction of the
deleter from an lvalue of type `E` shall be well formed and shall not
throw an exception.

*Remarks:* This constructor shall not participate in overload resolution
unless:

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
- `U` is not an array type, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

*Effects:* Constructs a `unique_ptr` by transferring ownership from `u`
to `*this`. If `E` is a reference type, this deleter is copy constructed
from `u`’s deleter; otherwise, this deleter is move constructed from
`u`’s deleter. The deleter constructor can be implemented with
`std::forward<E>`.

*Postconditions:* `get()` yields the value `u.get()` yielded before the
construction. `get_deleter()` returns a reference to the stored deleter
that was constructed from `u.get_deleter()`.

``` cpp
template <class U>
  unique_ptr(auto_ptr<U>&& u) noexcept;
```

*Effects:* Constructs a `unique_ptr` object, initializing the stored
pointer with `u.release()` and value-initializing the stored deleter.

*Postconditions:* `get()` yields the value `u.get()` yielded before the
construction. `u.get() == nullptr`. `get_deleter()` returns a reference
to the stored deleter.

*Remarks:* This constructor shall not participate in overload resolution
unless `U*` is implicitly convertible to `T*` and `D` is the same type
as `default_delete<T>`.

##### `unique_ptr` destructor <a id="unique.ptr.single.dtor">[[unique.ptr.single.dtor]]</a>

``` cpp
~unique_ptr();
```

*Requires:* The expression `get_deleter()(get())` shall be well formed,
shall have well-defined behavior, and shall not throw exceptions. The
use of `default_delete` requires `T` to be a complete type.

*Effects:* If `get() == nullptr` there are no effects. Otherwise
`get_deleter()(get())`.

##### `unique_ptr` assignment <a id="unique.ptr.single.asgn">[[unique.ptr.single.asgn]]</a>

``` cpp
unique_ptr& operator=(unique_ptr&& u) noexcept;
```

*Requires:* If `D` is not a reference type, `D` shall satisfy the
requirements of `MoveAssignable` (Table  [[moveassignable]]) and
assignment of the deleter from an rvalue of type `D` shall not throw an
exception. Otherwise, `D` is a reference type; `remove_reference_t<D>`
shall satisfy the `CopyAssignable` requirements and assignment of the
deleter from an lvalue of type `D` shall not throw an exception.

*Effects:* Transfers ownership from `u` to `*this` as if by calling
`reset(u.release())` followed by
`get_deleter() = std::forward<D>(u.get_deleter())`.

*Returns:* `*this`.

``` cpp
template <class U, class E> unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
```

*Requires:* If `E` is not a reference type, assignment of the deleter
from an rvalue of type `E` shall be well-formed and shall not throw an
exception. Otherwise, `E` is a reference type and assignment of the
deleter from an lvalue of type `E` shall be well-formed and shall not
throw an exception.

*Remarks:* This operator shall not participate in overload resolution
unless:

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer` and
- `U` is not an array type.

*Effects:* Transfers ownership from `u` to `*this` as if by calling
`reset(u.release())` followed by
`get_deleter() = std::forward<E>(u.get_deleter())`.

*Returns:* `*this`.

``` cpp
unique_ptr& operator=(nullptr_t) noexcept;
```

*Effects:* `reset()`.

`get() == nullptr`

*Returns:* `*this`.

##### `unique_ptr` observers <a id="unique.ptr.single.observers">[[unique.ptr.single.observers]]</a>

``` cpp
add_lvalue_reference_t<T> operator*() const;
```

*Requires:* `get() != nullptr`.

*Returns:* `*get()`.

``` cpp
pointer operator->() const noexcept;
```

*Requires:* `get() != nullptr`.

*Returns:* `get()`.

*Note:* use typically requires that `T` be a complete type.

``` cpp
pointer get() const noexcept;
```

*Returns:* The stored pointer.

``` cpp
deleter_type& get_deleter() noexcept;
const deleter_type& get_deleter() const noexcept;
```

*Returns:* A reference to the stored deleter.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `get() != nullptr`.

##### `unique_ptr` modifiers <a id="unique.ptr.single.modifiers">[[unique.ptr.single.modifiers]]</a>

``` cpp
pointer release() noexcept;
```

`get() == nullptr`.

*Returns:* The value `get()` had at the start of the call to `release`.

``` cpp
void reset(pointer p = pointer()) noexcept;
```

*Requires:* The expression `get_deleter()(get())` shall be well formed,
shall have well-defined behavior, and shall not throw exceptions.

*Effects:* assigns `p` to the stored pointer, and then if the old value
of the stored pointer, `old_p`, was not equal to `nullptr`, calls
`get_deleter()(old_p)`. The order of these operations is significant
because the call to `get_deleter()` may destroy `*this`.

*Postconditions:* `get() == p`. The postcondition does not hold if the
call to `get_deleter()` destroys `*this` since `this->get()` is no
longer a valid expression.

``` cpp
void swap(unique_ptr& u) noexcept;
```

*Requires:* `get_deleter()` shall be
swappable ([[swappable.requirements]]) and shall not throw an exception
under `swap`.

*Effects:* Invokes `swap` on the stored pointers and on the stored
deleters of `*this` and `u`.

#### `unique_ptr` for array objects with a runtime length <a id="unique.ptr.runtime">[[unique.ptr.runtime]]</a>

``` cpp
namespace std {
  template <class T, class D> class unique_ptr<T[], D> {
  public:
    typedef see below pointer;
    typedef T element_type;
    typedef D deleter_type;

    // [unique.ptr.runtime.ctor], constructors
    constexpr unique_ptr() noexcept;
    explicit unique_ptr(pointer p) noexcept;
    unique_ptr(pointer p, see below d) noexcept;
    unique_ptr(pointer p, see below d) noexcept;
    unique_ptr(unique_ptr&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept : unique_ptr() { }

    // destructor
    ~unique_ptr();

    // assignment
    unique_ptr& operator=(unique_ptr&& u) noexcept;
    unique_ptr& operator=(nullptr_t) noexcept;

    // [unique.ptr.runtime.observers], observers
    T& operator[](size_t i) const;
    pointer get() const noexcept;
    deleter_type& get_deleter() noexcept;
    const deleter_type& get_deleter() const noexcept;
    explicit operator bool() const noexcept;

    // [unique.ptr.runtime.modifiers] modifiers
    pointer release() noexcept;
    void reset(pointer p = pointer()) noexcept;
    void reset(nullptr_t) noexcept;
    template <class U> void reset(U) = delete;
    void swap(unique_ptr& u) noexcept;

    // disable copy from lvalue
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
  };
}
```

A specialization for array types is provided with a slightly altered
interface.

- Conversions between different types of `unique_ptr<T[], D>` or to or
  from the non-array forms of `unique_ptr` produce an ill-formed
  program.
- Pointers to types derived from `T` are rejected by the constructors,
  and by `reset`.
- The observers `operator*` and `operator->` are not provided.
- The indexing observer `operator[]` is provided.
- The default deleter will call `delete[]`.

Descriptions are provided below only for member functions that have
behavior different from the primary template.

The template argument `T` shall be a complete type.

##### `unique_ptr` constructors <a id="unique.ptr.runtime.ctor">[[unique.ptr.runtime.ctor]]</a>

``` cpp
explicit unique_ptr(pointer p) noexcept;
unique_ptr(pointer p, see below d) noexcept;
unique_ptr(pointer p, see below d) noexcept;
```

These constructors behave the same as in the primary template except
that they do not accept pointer types which are convertible to
`pointer`. One implementation technique is to create private templated
overloads of these members.

##### `unique_ptr` observers <a id="unique.ptr.runtime.observers">[[unique.ptr.runtime.observers]]</a>

``` cpp
T& operator[](size_t i) const;
```

*Requires:* `i <` the number of elements in the array to which the
stored pointer points.

*Returns:* `get()[i]`.

##### `unique_ptr` modifiers <a id="unique.ptr.runtime.modifiers">[[unique.ptr.runtime.modifiers]]</a>

``` cpp
void reset(nullptr_t p) noexcept;
```

*Effects:* Equivalent to `reset(pointer())`.

#### `unique_ptr` creation <a id="unique.ptr.create">[[unique.ptr.create]]</a>

``` cpp
template <class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
```

*Remarks:* This function shall not participate in overload resolution
unless `T` is not an array.

*Returns:* `unique_ptr<T>(new T(std::forward<Args>(args)...))`.

``` cpp
template <class T> unique_ptr<T> make_unique(size_t n);
```

*Remarks:* This function shall not participate in overload resolution
unless `T` is an array of unknown bound.

*Returns:* `unique_ptr<T>(new remove_extent_t<T>[n]())`.

``` cpp
template <class T, class... Args> unspecified make_unique(Args&&...) = delete;
```

*Remarks:* This function shall not participate in overload resolution
unless `T` is an array of known bound.

#### `unique_ptr` specialized algorithms <a id="unique.ptr.special">[[unique.ptr.special]]</a>

``` cpp
template <class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;
```

*Effects:* Calls `x.swap(y)`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `x.get() == y.get()`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator!=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `x.get() != y.get()`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Requires:* Let `CT` be `common_type<unique_ptr<T1, D1>::pointer,`
`unique_ptr<T2, D2>::pointer>::type`. Then the specialization `less<CT>`
shall be a function object type ([[function.objects]]) that induces a
strict weak ordering ([[alg.sorting]]) on the pointer values.

*Returns:* `less<CT>()(x.get(), y.get()).`

*Remarks:* If `unique_ptr<T1, D1>::pointer` is not implicitly
convertible to `CT` or `unique_ptr<T2, D2>::pointer` is not implicitly
convertible to `CT`, the program is ill-formed.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(y < x)`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `y < x`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(x < y)`.

``` cpp
template <class T, class D>
  bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
template <class T, class D>
  bool operator==(nullptr_t, const unique_ptr<T, D>& x) noexcept;
```

*Returns:* `!x`.

``` cpp
template <class T, class D>
  bool operator!=(const unique_ptr<T, D>& x, nullptr_t) noexcept;
template <class T, class D>
  bool operator!=(nullptr_t, const unique_ptr<T, D>& x) noexcept;
```

*Returns:* `(bool)x`.

``` cpp
template <class T, class D>
  bool operator<(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator<(nullptr_t, const unique_ptr<T, D>& x);
```

*Requires:* The specialization `less<unique_ptr<T, D>::pointer>` shall
be a function object type ([[function.objects]]) that induces a strict
weak ordering ([[alg.sorting]]) on the pointer values.

*Returns:* The first function template returns
`less<unique_ptr<T, D>::pointer>()(x.get(),`  
`nullptr)`. The second function template returns
`less<unique_ptr<T, D>::pointer>()(nullptr, x.get())`.

``` cpp
template <class T, class D>
  bool operator>(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator>(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `nullptr < x`. The second
function template returns `x < nullptr`.

``` cpp
template <class T, class D>
  bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator<=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(nullptr < x)`. The
second function template returns `!(x < nullptr)`.

``` cpp
template <class T, class D>
  bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator>=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(x < nullptr)`. The
second function template returns `!(nullptr < x)`.

### Shared-ownership pointers <a id="util.smartptr">[[util.smartptr]]</a>

#### Class `bad_weak_ptr` <a id="util.smartptr.weakptr">[[util.smartptr.weakptr]]</a>

``` cpp
namespace std {
  class bad_weak_ptr: public std::exception {
  public:
    bad_weak_ptr() noexcept;
  };
} // namespace std
```

An exception of type `bad_weak_ptr` is thrown by the `shared_ptr`
constructor taking a `weak_ptr`.

``` cpp
bad_weak_ptr() noexcept;
```

*Postconditions:* `what()` returns `"bad_weak_ptr"`.

#### Class template `shared_ptr` <a id="util.smartptr.shared">[[util.smartptr.shared]]</a>

The `shared_ptr` class template stores a pointer, usually obtained via
`new`. `shared_ptr` implements semantics of shared ownership; the last
remaining owner of the pointer is responsible for destroying the object,
or otherwise releasing the resources associated with the stored pointer.
A `shared_ptr` object is *empty* if it does not own a pointer.

``` cpp
namespace std {
  template<class T> class shared_ptr {
  public:
    typedef T element_type;

    // [util.smartptr.shared.const], constructors:
    constexpr shared_ptr() noexcept;
    template<class Y> explicit shared_ptr(Y* p);
    template<class Y, class D> shared_ptr(Y* p, D d);
    template<class Y, class D, class A> shared_ptr(Y* p, D d, A a);
    template <class D> shared_ptr(nullptr_t p, D d);
    template <class D, class A> shared_ptr(nullptr_t p, D d, A a);
    template<class Y> shared_ptr(const shared_ptr<Y>& r, T* p) noexcept;
    shared_ptr(const shared_ptr& r) noexcept;
    template<class Y> shared_ptr(const shared_ptr<Y>& r) noexcept;
    shared_ptr(shared_ptr&& r) noexcept;
    template<class Y> shared_ptr(shared_ptr<Y>&& r) noexcept;
    template<class Y> explicit shared_ptr(const weak_ptr<Y>& r);
    template<class Y> shared_ptr(auto_ptr<Y>&& r);
    template <class Y, class D> shared_ptr(unique_ptr<Y, D>&& r);
    constexpr shared_ptr(nullptr_t) : shared_ptr() { }

    // [util.smartptr.shared.dest], destructor:
    ~shared_ptr();

    // [util.smartptr.shared.assign], assignment:
    shared_ptr& operator=(const shared_ptr& r) noexcept;
    template<class Y> shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    shared_ptr& operator=(shared_ptr&& r) noexcept;
    template<class Y> shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
    template<class Y> shared_ptr& operator=(auto_ptr<Y>&& r);
    template <class Y, class D> shared_ptr& operator=(unique_ptr<Y, D>&& r);

    // [util.smartptr.shared.mod], modifiers:
    void swap(shared_ptr& r) noexcept;
    void reset() noexcept;
    template<class Y> void reset(Y* p);
    template<class Y, class D> void reset(Y* p, D d);
    template<class Y, class D, class A> void reset(Y* p, D d, A a);

    // [util.smartptr.shared.obs], observers:
    T* get() const noexcept;
    T& operator*() const noexcept;
    T* operator->() const noexcept;
    long use_count() const noexcept;
    bool unique() const noexcept;
    explicit operator bool() const noexcept;
    template<class U> bool owner_before(shared_ptr<U> const& b) const;
    template<class U> bool owner_before(weak_ptr<U> const& b) const;
  };

  // [util.smartptr.shared.create], shared_ptr creation
  template<class T, class... Args> shared_ptr<T> make_shared(Args&&... args);
  template<class T, class A, class... Args>
    shared_ptr<T> allocate_shared(const A& a, Args&&... args);

  // [util.smartptr.shared.cmp], shared_ptr comparisons:
  template<class T, class U>
    bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator!=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator<(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator<=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator>=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;

  template <class T>
    bool operator==(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator==(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator!=(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator!=(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator<(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator<(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator<=(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator<=(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator>(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator>(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator>=(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator>=(nullptr_t, const shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.spec], shared_ptr specialized algorithms:
  template<class T> void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.cast], shared_ptr casts:
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;

  // [util.smartptr.getdeleter], shared_ptr get_deleter:
  template<class D, class T> D* get_deleter(const shared_ptr<T>& p) noexcept;

  // [util.smartptr.shared.io], shared_ptr I/O:
  template<class E, class T, class Y>
    basic_ostream<E, T>& operator<< (basic_ostream<E, T>& os, const shared_ptr<Y>& p);
} // namespace std
```

Specializations of `shared_ptr` shall be `CopyConstructible`,
`CopyAssignable`, and `LessThanComparable`, allowing their use in
standard containers. Specializations of `shared_ptr` shall be
convertible to `bool`, allowing their use in boolean expressions and
declarations in conditions. The template parameter `T` of `shared_ptr`
may be an incomplete type.

``` cpp
if(shared_ptr<X> px = dynamic_pointer_cast<X>(py)) {
  // do something with px
}
```

For purposes of determining the presence of a data race, member
functions shall access and modify only the `shared_ptr` and `weak_ptr`
objects themselves and not objects they refer to. Changes in
`use_count()` do not reflect modifications that can introduce data
races.

##### `shared_ptr` constructors <a id="util.smartptr.shared.const">[[util.smartptr.shared.const]]</a>

``` cpp
constexpr shared_ptr() noexcept;
```

*Effects:* Constructs an *empty* `shared_ptr` object.

*Postconditions:* `use_count() == 0 && get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(Y* p);
```

*Requires:* `p` shall be convertible to `T*`. `Y` shall be a complete
type. The expression `delete p` shall be well formed, shall have well
defined behavior, and shall not throw exceptions.

*Effects:* Constructs a `shared_ptr` object that *owns* the pointer `p`.

*Postconditions:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

If an exception is thrown, `delete p` is called.

``` cpp
template<class Y, class D> shared_ptr(Y* p, D d);
template<class Y, class D, class A> shared_ptr(Y* p, D d, A a);
template <class D> shared_ptr(nullptr_t p, D d);
template <class D, class A> shared_ptr(nullptr_t p, D d, A a);
```

*Requires:* `p` shall be convertible to `T*`. `D` shall be
`CopyConstructible`. The copy constructor and destructor of ` D` shall
not throw exceptions. The expression `d(p)` shall be well formed, shall
have well defined behavior, and shall not throw exceptions. `A` shall be
an allocator ([[allocator.requirements]]). The copy constructor and
destructor of `A` shall not throw exceptions.

*Effects:* Constructs a `shared_ptr` object that *owns* the object `p`
and the deleter `d`. The second and fourth constructors shall use a copy
of `a` to allocate memory for internal use.

*Postconditions:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

If an exception is thrown, `d(p)` is called.

``` cpp
template<class Y> shared_ptr(const shared_ptr<Y>& r, T* p) noexcept;
```

*Effects:* Constructs a `shared_ptr` instance that stores `p` and
*shares ownership* with `r`.

*Postconditions:* `get() == p && use_count() == r.use_count()`

To avoid the possibility of a dangling pointer, the user of this
constructor must ensure that `p` remains valid at least until the
ownership group of `r` is destroyed.

This constructor allows creation of an *empty* `shared_ptr` instance
with a non-null stored pointer.

``` cpp
shared_ptr(const shared_ptr& r) noexcept;
template<class Y> shared_ptr(const shared_ptr<Y>& r) noexcept;
```

The second constructor shall not participate in overload resolution
unless `Y*` is implicitly convertible to `T*`.

*Effects:* If `r` is *empty*, constructs an *empty* `shared_ptr` object;
otherwise, constructs a `shared_ptr` object that *shares ownership* with
`r`.

*Postconditions:* `get() == r.get() && use_count() == r.use_count()`.

``` cpp
shared_ptr(shared_ptr&& r) noexcept;
template<class Y> shared_ptr(shared_ptr<Y>&& r) noexcept;
```

The second constructor shall not participate in overload resolution
unless `Y*` is convertible to `T*`.

*Effects:* Move-constructs a `shared_ptr` instance from `r`.

*Postconditions:* `*this` shall contain the old value of `r`. `r` shall
be *empty*. `r.get() == nullptr.`

``` cpp
template<class Y> explicit shared_ptr(const weak_ptr<Y>& r);
```

*Requires:* `Y*` shall be convertible to `T*`.

*Effects:* Constructs a `shared_ptr` object that *shares ownership* with
`r` and stores a copy of the pointer stored in `r`.

*Postconditions:* `use_count() == r.use_count()`.

*Throws:* `bad_weak_ptr` when `r.expired()`.

If an exception is thrown, the constructor has no effect.

``` cpp
template<class Y> shared_ptr(auto_ptr<Y>&& r);
```

*Requires:* `r.release()` shall be convertible to `T*`. `Y` shall be a
complete type. The expression `delete r.release()` shall be well formed,
shall have well defined behavior, and shall not throw exceptions.

*Effects:* Constructs a `shared_ptr` object that stores and *owns*
`r.release()`.

*Postconditions:* `use_count() == 1` `&&` `r.get() == nullptr`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

If an exception is thrown, the constructor has no effect.

``` cpp
template <class Y, class D> shared_ptr(unique_ptr<Y, D>&& r);
```

*Effects:* Equivalent to `shared_ptr(r.release(), r.get_deleter())` when
`D` is not a reference type, otherwise
`shared_ptr(r.release(), ref(r.get_deleter()))`.

If an exception is thrown, the constructor has no effect.

##### `shared_ptr` destructor <a id="util.smartptr.shared.dest">[[util.smartptr.shared.dest]]</a>

``` cpp
~shared_ptr();
```

*Effects:*

- If `*this` is *empty* or shares ownership with another `shared_ptr`
  instance (`use_count() > 1`), there are no side effects.
- Otherwise, if `*this` *owns* an object `p` and a deleter `d`, `d(p)`
  is called.
- Otherwise, `*this` *owns* a pointer `p`, and `delete p` is called.

Since the destruction of `*this` decreases the number of instances that
share ownership with `*this` by one, after `*this` has been destroyed
all `shared_ptr` instances that shared ownership with `*this` will
report a `use_count()` that is one less than its previous value.

##### `shared_ptr` assignment <a id="util.smartptr.shared.assign">[[util.smartptr.shared.assign]]</a>

``` cpp
shared_ptr& operator=(const shared_ptr& r) noexcept;
template<class Y> shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
template<class Y> shared_ptr& operator=(auto_ptr<Y>&& r);
```

*Effects:* Equivalent to `shared_ptr(r).swap(*this)`.

*Returns:* `*this`.

The use count updates caused by the temporary object construction and
destruction are not observable side effects, so the implementation may
meet the effects (and the implied guarantees) via different means,
without creating a temporary. In particular, in the example:

``` cpp
shared_ptr<int> p(new int);
shared_ptr<void> q(p);
p = p;
q = p;
```

both assignments may be no-ops.

``` cpp
shared_ptr& operator=(shared_ptr&& r) noexcept;
template<class Y> shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

``` cpp
template <class Y, class D> shared_ptr& operator=(unique_ptr<Y, D>&& r);
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`

##### `shared_ptr` modifiers <a id="util.smartptr.shared.mod">[[util.smartptr.shared.mod]]</a>

``` cpp
void swap(shared_ptr& r) noexcept;
```

*Effects:* Exchanges the contents of `*this` and `r`.

``` cpp
void reset() noexcept;
```

*Effects:* Equivalent to `shared_ptr().swap(*this)`.

``` cpp
template<class Y> void reset(Y* p);
```

*Effects:* Equivalent to `shared_ptr(p).swap(*this)`.

``` cpp
template<class Y, class D> void reset(Y* p, D d);
```

*Effects:* Equivalent to `shared_ptr(p, d).swap(*this)`.

``` cpp
template<class Y, class D, class A> void reset(Y* p, D d, A a);
```

*Effects:* Equivalent to `shared_ptr(p, d, a).swap(*this)`.

##### `shared_ptr` observers <a id="util.smartptr.shared.obs">[[util.smartptr.shared.obs]]</a>

``` cpp
T* get() const noexcept;
```

*Returns:* the stored pointer.

``` cpp
T& operator*() const noexcept;
```

*Requires:* `get() != 0`.

*Returns:* `*get()`.

*Remarks:* When `T` is `void`, it is unspecified whether this member
function is declared. If it is declared, it is unspecified what its
return type is, except that the declaration (although not necessarily
the definition) of the function shall be well formed.

``` cpp
T* operator->() const noexcept;
```

*Requires:* `get() != 0`.

*Returns:* `get()`.

``` cpp
long use_count() const noexcept;
```

*Returns:* the number of `shared_ptr` objects, `*this` included, that
*share ownership* with `*this`, or `0` when `*this` is *empty*.

`use_count()` is not necessarily efficient.

``` cpp
bool unique() const noexcept;
```

*Returns:* `use_count() == 1`.

`unique()` may be faster than `use_count()`. If you are using `unique()`
to implement copy on write, do not rely on a specific value when
`get() == nullptr`.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `get() != 0`.

``` cpp
template<class U> bool owner_before(shared_ptr<U> const& b) const;
template<class U> bool owner_before(weak_ptr<U> const& b) const;
```

*Returns:* An unspecified value such that

- `x.owner_before(y)` defines a strict weak ordering as defined
  in  [[alg.sorting]];
- under the equivalence relation defined by `owner_before`,
  `!a.owner_before(b) && !b.owner_before(a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

##### `shared_ptr` creation <a id="util.smartptr.shared.create">[[util.smartptr.shared.create]]</a>

``` cpp
template<class T, class... Args> shared_ptr<T> make_shared(Args&&... args);
template<class T, class A, class... Args>
  shared_ptr<T> allocate_shared(const A& a, Args&&... args);
```

*Requires:* The expression `::new (pv) T(std::forward<Args>(args)...)`,
where `pv` has type `void*` and points to storage suitable to hold an
object of type `T`, shall be well formed. `A` shall be an
*allocator* ([[allocator.requirements]]). The copy constructor and
destructor of `A` shall not throw exceptions.

*Effects:* Allocates memory suitable for an object of type `T` and
constructs an object in that memory via the placement new expression
`::new (pv) T(std::forward<Args>(args)...)`. The template
`allocate_shared` uses a copy of `a` to allocate memory. If an exception
is thrown, the functions have no effect.

*Returns:* A `shared_ptr` instance that stores and owns the address of
the newly constructed object of type `T`.

*Postconditions:* `get() != 0 && use_count() == 1`

*Throws:* `bad_alloc`, or an exception thrown from `A::allocate` or from
the constructor of `T`.

*Remarks:* Implementations should perform no more than one memory
allocation. This provides efficiency equivalent to an intrusive smart
pointer.

These functions will typically allocate more memory than `sizeof(T)` to
allow for internal bookkeeping structures such as the reference counts.

##### `shared_ptr` comparison <a id="util.smartptr.shared.cmp">[[util.smartptr.shared.cmp]]</a>

``` cpp
template<class T, class U> bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `a.get() == b.get()`.

``` cpp
template<class T, class U> bool operator<(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `less<V>()(a.get(), b.get())`, where `V` is the composite
pointer type (Clause  [[expr]]) of `T*` and `U*`.

Defining a comparison operator allows `shared_ptr` objects to be used as
keys in associative containers.

``` cpp
template <class T>
  bool operator==(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator==(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* `!a`.

``` cpp
template <class T>
  bool operator!=(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator!=(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* `(bool)a`.

``` cpp
template <class T>
  bool operator<(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator<(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns
`less<T*>()(a.get(), nullptr)`. The second function template returns
`less<T*>()(nullptr, a.get())`.

``` cpp
template <class T>
  bool operator>(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator>(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns `nullptr < a`. The second
function template returns `a < nullptr`.

``` cpp
template <class T>
  bool operator<=(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator<=(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns `!(nullptr < a)`. The
second function template returns `!(a < nullptr)`.

``` cpp
template <class T>
  bool operator>=(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator>=(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns `!(a < nullptr)`. The
second function template returns `!(nullptr < a)`.

##### `shared_ptr` specialized algorithms <a id="util.smartptr.shared.spec">[[util.smartptr.shared.spec]]</a>

``` cpp
template<class T> void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

##### `shared_ptr` casts <a id="util.smartptr.shared.cast">[[util.smartptr.shared.cast]]</a>

``` cpp
template<class T, class U> shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `static_cast<T*>(r.get())` shall be well
formed.

*Returns:* If `r` is *empty*, an *empty* `shared_ptr<T>`; otherwise, a
`shared_ptr<T>` object that stores `static_cast<T*>(r.get())` and
*shares ownership* with `r`.

*Postconditions:* `w.get() == static_cast<T*>(r.get())` and
`w.use_count() == r.use_count()`, where `w` is the return value.

The seemingly equivalent expression
`shared_ptr<T>(static_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object twice.

``` cpp
template<class T, class U> shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `dynamic_cast<T*>(r.get())` shall be well
formed and shall have well defined behavior.

*Returns:*

- When `dynamic_cast<T*>(r.get())` returns a nonzero value, a
  `shared_ptr<T>` object that stores a copy of it and *shares ownership*
  with `r`;
- Otherwise, an *empty* `shared_ptr<T>` object.

`w.get() == dynamic_cast<T*>(r.get())`, where `w` is the return value.

The seemingly equivalent expression
`shared_ptr<T>(dynamic_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object twice.

``` cpp
template<class T, class U> shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `const_cast<T*>(r.get())` shall be well
formed.

*Returns:* If `r` is empty, an empty `shared_ptr<T>`; otherwise, a
`shared_ptr<T>` object that stores `const_cast<T*>(r.get())` and shares
ownership with `r`.

*Postconditions:* `w.get() == const_cast<T*>(r.get())` and
`w.use_count() == r.use_count()`, where `w` is the return value.

The seemingly equivalent expression
`shared_ptr<T>(const_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object twice.

##### get_deleter <a id="util.smartptr.getdeleter">[[util.smartptr.getdeleter]]</a>

``` cpp
template<class D, class T> D* get_deleter(const shared_ptr<T>& p) noexcept;
```

*Returns:* If `p` *owns* a deleter `d` of type cv-unqualified `D`,
returns `&d`; otherwise returns `nullptr`. The returned pointer remains
valid as long as there exists a `shared_ptr` instance that owns `d`. It
is unspecified whether the pointer remains valid longer than that. This
can happen if the implementation doesn’t destroy the deleter until all
`weak_ptr` instances that share ownership with `p` have been destroyed.

##### `shared_ptr` I/O <a id="util.smartptr.shared.io">[[util.smartptr.shared.io]]</a>

``` cpp
template<class E, class T, class Y>
  basic_ostream<E, T>& operator<< (basic_ostream<E, T>& os, shared_ptr<Y> const& p);
```

*Effects:* `os << p.get();`.

*Returns:* `os`.

#### Class template `weak_ptr` <a id="util.smartptr.weak">[[util.smartptr.weak]]</a>

The `weak_ptr` class template stores a weak reference to an object that
is already managed by a `shared_ptr`. To access the object, a `weak_ptr`
can be converted to a `shared_ptr` using the member function `lock`.

``` cpp
namespace std {
  template<class T> class weak_ptr {
  public:
    typedef T element_type;

    // [util.smartptr.weak.const], constructors
    constexpr weak_ptr() noexcept;
    template<class Y> weak_ptr(shared_ptr<Y> const& r) noexcept;
    weak_ptr(weak_ptr const& r) noexcept;
    template<class Y> weak_ptr(weak_ptr<Y> const& r) noexcept;
    weak_ptr(weak_ptr&& r) noexcept;
    template<class Y> weak_ptr(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.dest], destructor
    ~weak_ptr();

    // [util.smartptr.weak.assign], assignment
    weak_ptr& operator=(weak_ptr const& r) noexcept;
    template<class Y> weak_ptr& operator=(weak_ptr<Y> const& r) noexcept;
    template<class Y> weak_ptr& operator=(shared_ptr<Y> const& r) noexcept;
    weak_ptr& operator=(weak_ptr&& r) noexcept;
    template<class Y> weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.mod], modifiers
    void swap(weak_ptr& r) noexcept;
    void reset() noexcept;

    // [util.smartptr.weak.obs], observers
    long use_count() const noexcept;
    bool expired() const noexcept;
    shared_ptr<T> lock() const noexcept;
    template<class U> bool owner_before(shared_ptr<U> const& b) const;
    template<class U> bool owner_before(weak_ptr<U> const& b) const;
  };

  // [util.smartptr.weak.spec], specialized algorithms
  template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
} // namespace std
```

Specializations of `weak_ptr` shall be `CopyConstructible` and
`CopyAssignable`, allowing their use in standard containers. The
template parameter `T` of `weak_ptr` may be an incomplete type.

##### `weak_ptr` constructors <a id="util.smartptr.weak.const">[[util.smartptr.weak.const]]</a>

``` cpp
constexpr weak_ptr() noexcept;
```

*Effects:* Constructs an *empty* `weak_ptr` object.

*Postconditions:* `use_count() == 0`.

``` cpp
weak_ptr(const weak_ptr& r) noexcept;
template<class Y> weak_ptr(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr(const shared_ptr<Y>& r) noexcept;
```

The second and third constructors shall not participate in overload
resolution unless `Y*` is implicitly convertible to `T*`.

*Effects:* If `r` is *empty*, constructs an *empty* `weak_ptr` object;
otherwise, constructs a `weak_ptr` object that *shares ownership* with
`r` and stores a copy of the pointer stored in `r`.

*Postconditions:* `use_count() == r.use_count()`.

``` cpp
weak_ptr(weak_ptr&& r) noexcept;
template<class Y> weak_ptr(weak_ptr<Y>&& r) noexcept;
```

The second constructor shall not participate in overload resolution
unless `Y*` is implicitly convertible to `T*`.

*Effects:* Move-constructs a `weak_ptr` instance from `r`.

*Postconditions:* `*this` shall contain the old value of `r`. `r` shall
be *empty*. `r.use_count() == 0`.

##### `weak_ptr` destructor <a id="util.smartptr.weak.dest">[[util.smartptr.weak.dest]]</a>

``` cpp
~weak_ptr();
```

*Effects:* Destroys this `weak_ptr` object but has no effect on the
object its stored pointer points to.

##### `weak_ptr` assignment <a id="util.smartptr.weak.assign">[[util.smartptr.weak.assign]]</a>

``` cpp
weak_ptr& operator=(const weak_ptr& r) noexcept;
template<class Y> weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(r).swap(*this)`.

*Remarks:* The implementation may meet the effects (and the implied
guarantees) via different means, without creating a temporary.

*Returns:* `*this`.

``` cpp
weak_ptr& operator=(weak_ptr&& r) noexcept;
template<class Y> weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

##### `weak_ptr` modifiers <a id="util.smartptr.weak.mod">[[util.smartptr.weak.mod]]</a>

``` cpp
void swap(weak_ptr& r) noexcept;
```

*Effects:* Exchanges the contents of `*this` and `r`.

``` cpp
void reset() noexcept;
```

*Effects:* Equivalent to `weak_ptr().swap(*this)`.

##### `weak_ptr` observers <a id="util.smartptr.weak.obs">[[util.smartptr.weak.obs]]</a>

``` cpp
long use_count() const noexcept;
```

*Returns:* `0` if `*this` is *empty*; otherwise, the number of
`shared_ptr` instances that *share ownership* with `*this`.

`use_count()` is not necessarily efficient.

``` cpp
bool expired() const noexcept;
```

*Returns:* `use_count() == 0`.

`expired()` may be faster than `use_count()`.

``` cpp
shared_ptr<T> lock() const noexcept;
```

*Returns:* `expired() ? shared_ptr<T>() : shared_ptr<T>(*this)`,
executed atomically.

``` cpp
template<class U> bool owner_before(shared_ptr<U> const& b) const;
template<class U> bool owner_before(weak_ptr<U> const& b) const;
```

*Returns:* An unspecified value such that

- `x.owner_before(y)` defines a strict weak ordering as defined
  in  [[alg.sorting]];
- under the equivalence relation defined by `owner_before`,
  `!a.owner_before(b) && !b.owner_before(a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

##### `weak_ptr` specialized algorithms <a id="util.smartptr.weak.spec">[[util.smartptr.weak.spec]]</a>

``` cpp
template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

#### Class template `owner_less` <a id="util.smartptr.ownerless">[[util.smartptr.ownerless]]</a>

The class template `owner_less` allows ownership-based mixed comparisons
of shared and weak pointers.

``` cpp
namespace std {
  template<class T> struct owner_less;

  template<class T> struct owner_less<shared_ptr<T> > {
    typedef bool result_type;
    typedef shared_ptr<T> first_argument_type;
    typedef shared_ptr<T> second_argument_type;
    bool operator()(shared_ptr<T> const&, shared_ptr<T> const&) const;
    bool operator()(shared_ptr<T> const&, weak_ptr<T> const&) const;
    bool operator()(weak_ptr<T> const&, shared_ptr<T> const&) const;
  };

  template<class T> struct owner_less<weak_ptr<T> > {
    typedef bool result_type;
    typedef weak_ptr<T> first_argument_type;
    typedef weak_ptr<T> second_argument_type;
    bool operator()(weak_ptr<T> const&, weak_ptr<T> const&) const;
    bool operator()(shared_ptr<T> const&, weak_ptr<T> const&) const;
    bool operator()(weak_ptr<T> const&, shared_ptr<T> const&) const;
  };
}
```

`operator()(x,y)` shall return `x.owner_before(y)`. Note that

- `operator()` defines a strict weak ordering as defined in 
  [[alg.sorting]];
- under the equivalence relation defined by `operator()`,
  `!operator()(a, b) && !operator()(b, a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

#### Class template `enable_shared_from_this` <a id="util.smartptr.enab">[[util.smartptr.enab]]</a>

A class `T` can inherit from `enable_shared_from_this<T>` to inherit the
`shared_from_this` member functions that obtain a *shared_ptr* instance
pointing to `*this`.

``` cpp
struct X: public enable_shared_from_this<X> {
};

int main() {
  shared_ptr<X> p(new X);
  shared_ptr<X> q = p->shared_from_this();
  assert(p == q);
  assert(!(p < q ) && !(q < p)); // p and q share ownership
}
```

``` cpp
namespace std {
  template<class T> class enable_shared_from_this {
  protected:
    constexpr enable_shared_from_this() noexcept;
    enable_shared_from_this(enable_shared_from_this const&) noexcept;
    enable_shared_from_this& operator=(enable_shared_from_this const&) noexcept;
    ~enable_shared_from_this();
  public:
    shared_ptr<T> shared_from_this();
    shared_ptr<T const> shared_from_this() const;
  };
} // namespace std
```

The template parameter `T` of `enable_shared_from_this` may be an
incomplete type.

``` cpp
constexpr enable_shared_from_this() noexcept;
enable_shared_from_this(const enable_shared_from_this<T>&) noexcept;
```

*Effects:* Constructs an `enable_shared_from_this<T>` object.

``` cpp
enable_shared_from_this<T>& operator=(const enable_shared_from_this<T>&) noexcept;
```

*Returns:* `*this`.

``` cpp
~enable_shared_from_this();
```

*Effects:* Destroys `*this`.

``` cpp
shared_ptr<T>       shared_from_this();
shared_ptr<T const> shared_from_this() const;
```

*Requires:* `enable_shared_from_this<T>` shall be an accessible base
class of `T`. `*this` shall be a subobject of an object `t` of type `T`.
There shall be at least one `shared_ptr` instance `p` that *owns* `&t`.

*Returns:* A `shared_ptr<T>` object `r` that *shares ownership with*
`p`.

*Postconditions:* `r.get() == this`.

A possible implementation is shown below:

``` cpp
template<class T> class enable_shared_from_this {
private:
  weak_ptr<T> __weak_this;
protected:
  constexpr enable_shared_from_this() : __weak_this() { }
  enable_shared_from_this(enable_shared_from_this const &) { }
  enable_shared_from_this& operator=(enable_shared_from_this const &) { return *this; }
  ~enable_shared_from_this() { }
public:
  shared_ptr<T> shared_from_this() { return shared_ptr<T>(__weak_this); }
  shared_ptr<T const> shared_from_this() const { return shared_ptr<T const>(__weak_this); }
};
```

The `shared_ptr` constructors that create unique pointers can detect the
presence of an `enable_shared_from_this` base and assign the newly
created `shared_ptr` to its `__weak_this` member.

#### `shared_ptr` atomic access <a id="util.smartptr.shared.atomic">[[util.smartptr.shared.atomic]]</a>

Concurrent access to a `shared_ptr` object from multiple threads does
not introduce a data race if the access is done exclusively via the
functions in this section and the instance is passed as their first
argument.

The meaning of the arguments of type `memory_order` is explained in 
[[atomics.order]].

``` cpp
template<class T>
  bool atomic_is_lock_free(const shared_ptr<T>* p);
```

*Requires:* `p` shall not be null.

*Returns:* `true` if atomic access to `*p` is lock-free, `false`
otherwise.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_load(const shared_ptr<T>* p);
```

*Requires:* `p` shall not be null.

*Returns:* `atomic_load_explicit(p, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_load_explicit(const shared_ptr<T>* p, memory_order mo);
```

*Requires:* `p` shall not be null.

*Requires:* `mo` shall not be `memory_order_release` or
`memory_order_acq_rel`.

*Returns:* `*p`.

*Throws:* Nothing.

``` cpp
template<class T>
  void atomic_store(shared_ptr<T>* p, shared_ptr<T> r);
```

*Requires:* `p` shall not be null.

*Effects:* `atomic_store_explicit(p, r, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  void atomic_store_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);
```

*Requires:* `p` shall not be null.

*Requires:* `mo` shall not be `memory_order_acquire` or
`memory_order_acq_rel`.

*Effects:* `p->swap(r)`.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_exchange(shared_ptr<T>* p, shared_ptr<T> r);
```

*Requires:* `p` shall not be null.

*Returns:* `atomic_exchange_explicit(p, r, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_exchange_explicit(shared_ptr<T>* p, shared_ptr<T> r,
                                         memory_order mo);
```

*Requires:* `p` shall not be null.

*Effects:* `p->swap(r)`.

*Returns:* The previous value of `*p`.

*Throws:* Nothing.

``` cpp
template<class T>
  bool atomic_compare_exchange_weak(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
```

*Requires:* `p` shall not be null and `v` shall not be null.

*Returns:*
`atomic_compare_exchange_weak_explicit(p, v, w, memory_order_seq_cst, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  bool atomic_compare_exchange_strong(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
```

*Returns:* `atomic_compare_exchange_strong_explicit(p, v, w,`
`memory_order_seq_cst, memory_order_seq_cst)`.

``` cpp
template<class T>
  bool atomic_compare_exchange_weak_explicit(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
    memory_order success, memory_order failure);
template<class T>
  bool atomic_compare_exchange_strong_explicit(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
    memory_order success, memory_order failure);
```

*Requires:* `p` shall not be null and `v` shall not be null.

*Requires:* `failure` shall not be `memory_order_release`,
`memory_order_acq_rel`, or stronger than `success`.

*Effects:* If `*p` is equivalent to `*v`, assigns `w` to `*p` and has
synchronization semantics corresponding to the value of `success`,
otherwise assigns `*p` to `*v` and has synchronization semantics
corresponding to the value of `failure`.

*Returns:* `true` if `*p` was equivalent to `*v`, `false` otherwise.

*Throws:* Nothing.

*Remarks:* two `shared_ptr` objects are equivalent if they store the
same pointer value and share ownership.

*Remarks:* the weak forms may fail spuriously.
See  [[atomics.types.operations]].

#### Smart pointer hash support <a id="util.smartptr.hash">[[util.smartptr.hash]]</a>

``` cpp
template <class T, class D> struct hash<unique_ptr<T, D> >;
```

The template specialization shall meet the requirements of class
template `hash` ([[unord.hash]]). For an object `p` of type `UP`, where
`UP` is `unique_ptr<T, D>`, `hash<UP>()(p)` shall evaluate to the same
value as `hash<typename UP::pointer>()(p.get())`.

*Requires:* The specialization `hash<typename UP::pointer>` shall be
well-formed and well-defined, and shall meet the requirements of class
template `hash` ([[unord.hash]]).

``` cpp
template <class T> struct hash<shared_ptr<T> >;
```

The template specialization shall meet the requirements of class
template `hash` ([[unord.hash]]). For an object `p` of type
`shared_ptr<T>`, `hash<shared_ptr<T> >()(p)` shall evaluate to the same
value as `hash<T*>()(p.get())`.

## Function objects <a id="function.objects">[[function.objects]]</a>

A *function object type* is an object type ([[basic.types]]) that can
be the type of the *postfix-expression* in a function call (
[[expr.call]],  [[over.match.call]]).[^2] A *function object* is an
object of a function object type. In the places where one would expect
to pass a pointer to a function to an algorithmic template (Clause 
[[algorithms]]), the interface is specified to accept a function object.
This not only makes algorithmic templates work with pointers to
functions, but also enables them to work with arbitrary function
objects.

``` cpp
namespace std {
  // [depr.base], base (deprecated):
  template <class Arg, class Result> struct unary_function;
  template <class Arg1, class Arg2, class Result> struct binary_function;

  // [refwrap], reference_wrapper:
  template <class T> class reference_wrapper;

  template <class T> reference_wrapper<T> ref(T&) noexcept;
  template <class T> reference_wrapper<const T> cref(const T&) noexcept;
  template <class T> void ref(const T&&) = delete;
  template <class T> void cref(const T&&) = delete;

  template <class T> reference_wrapper<T> ref(reference_wrapper<T>) noexcept;
  template <class T> reference_wrapper<const T> cref(reference_wrapper<T>) noexcept;

  // [arithmetic.operations], arithmetic operations:
  template <class T = void> struct plus;
  template <class T = void> struct minus;
  template <class T = void> struct multiplies;
  template <class T = void> struct divides;
  template <class T = void> struct modulus;
  template <class T = void> struct negate;
  template <> struct plus<void>;
  template <> struct minus<void>;
  template <> struct multiplies<void>;
  template <> struct divides<void>;
  template <> struct modulus<void>;
  template <> struct negate<void>;

  // [comparisons], comparisons:
  template <class T = void> struct equal_to;
  template <class T = void> struct not_equal_to;
  template <class T = void> struct greater;
  template <class T = void> struct less;
  template <class T = void> struct greater_equal;
  template <class T = void> struct less_equal;
  template <> struct equal_to<void>;
  template <> struct not_equal_to<void>;
  template <> struct greater<void>;
  template <> struct less<void>;
  template <> struct greater_equal<void>;
  template <> struct less_equal<void>;

  // [logical.operations], logical operations:
  template <class T = void> struct logical_and;
  template <class T = void> struct logical_or;
  template <class T = void> struct logical_not;
  template <> struct logical_and<void>;
  template <> struct logical_or<void>;
  template <> struct logical_not<void>;

  // [bitwise.operations], bitwise operations:
  template <class T = void> struct bit_and;
  template <class T = void> struct bit_or;
  template <class T = void> struct bit_xor;
  template <class T = void> struct bit_not;
  template <> struct bit_and<void>;
  template <> struct bit_or<void>;
  template <> struct bit_xor<void>;
  template <> struct bit_not<void>;

  // [negators], negators:
  template <class Predicate> class unary_negate;
  template <class Predicate>
    constexpr unary_negate<Predicate> not1(const Predicate&);
  template <class Predicate> class binary_negate;
  template <class Predicate>
    constexpr binary_negate<Predicate> not2(const Predicate&);

  // [func.bind], bind:
  template<class T> struct is_bind_expression;
  template<class T> struct is_placeholder;

  template<class F, class... BoundArgs>
    unspecified bind(F&&, BoundArgs&&...);
  template<class R, class F, class... BoundArgs>
    unspecified bind(F&&, BoundArgs&&...);

  namespace placeholders {
    // M is the implementation-defined number of placeholders
    extern unspecified _1;
    extern unspecified _2;
                .
                .
                .
    extern unspecified _M;
  }

  // [depr.lib.binders], binders (deprecated):
  template <class Fn> class binder1st;
  template <class Fn, class T>
    binder1st<Fn> bind1st(const Fn&, const T&);
  template <class Fn> class binder2nd;
  template <class Fn, class T>
    binder2nd<Fn> bind2nd(const Fn&, const T&);

  // [depr.function.pointer.adaptors], adaptors (deprecated):
  template <class Arg, class Result> class pointer_to_unary_function;
  template <class Arg, class Result>
    pointer_to_unary_function<Arg,Result> ptr_fun(Result (*)(Arg));
  template <class Arg1, class Arg2, class Result>
    class pointer_to_binary_function;
  template <class Arg1, class Arg2, class Result>
    pointer_to_binary_function<Arg1,Arg2,Result>
      ptr_fun(Result (*)(Arg1,Arg2));

  // [depr.member.pointer.adaptors], adaptors (deprecated):
  template<class S, class T> class mem_fun_t;
  template<class S, class T, class A> class mem_fun1_t;
  template<class S, class T>
      mem_fun_t<S,T> mem_fun(S (T::*f)());
  template<class S, class T, class A>
      mem_fun1_t<S,T,A> mem_fun(S (T::*f)(A));
  template<class S, class T> class mem_fun_ref_t;
  template<class S, class T, class A> class mem_fun1_ref_t;
  template<class S, class T>
      mem_fun_ref_t<S,T> mem_fun_ref(S (T::*f)());
  template<class S, class T, class A>
      mem_fun1_ref_t<S,T,A> mem_fun_ref(S (T::*f)(A));

  template <class S, class T> class const_mem_fun_t;
  template <class S, class T, class A> class const_mem_fun1_t;
  template <class S, class T>
    const_mem_fun_t<S,T> mem_fun(S (T::*f)() const);
  template <class S, class T, class A>
    const_mem_fun1_t<S,T,A> mem_fun(S (T::*f)(A) const);
  template <class S, class T> class const_mem_fun_ref_t;
  template <class S, class T, class A> class const_mem_fun1_ref_t;
  template <class S, class T>
    const_mem_fun_ref_t<S,T> mem_fun_ref(S (T::*f)() const);
  template <class S, class T, class A>
    const_mem_fun1_ref_t<S,T,A> mem_fun_ref(S (T::*f)(A) const);

  // [func.memfn], member function adaptors:
  template<class R, class T> unspecified mem_fn(R T::*);

  // [func.wrap] polymorphic function wrappers:
  class bad_function_call;

  template<class> class function; // undefined
  template<class R, class... ArgTypes> class function<R(ArgTypes...)>;

  template<class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&);

  template<class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t);
  template<class R, class... ArgTypes>
    bool operator==(nullptr_t, const function<R(ArgTypes...)>&);
  template<class R, class... ArgTypes>
    bool operator!=(const function<R(ArgTypes...)>&, nullptr_t);
  template<class R, class... ArgTypes>
    bool operator!=(nullptr_t, const function<R(ArgTypes...)>&);

  // [unord.hash], hash function primary template:
  template <class T> struct hash;

  // Hash function specializations
  template <> struct hash<bool>;
  template <> struct hash<char>;
  template <> struct hash<signed char>;
  template <> struct hash<unsigned char>;
  template <> struct hash<char16_t>;
  template <> struct hash<char32_t>;
  template <> struct hash<wchar_t>;
  template <> struct hash<short>;
  template <> struct hash<unsigned short>;
  template <> struct hash<int>;
  template <> struct hash<unsigned int>;
  template <> struct hash<long>;
  template <> struct hash<long long>;
  template <> struct hash<unsigned long>;
  template <> struct hash<unsigned long long>;

  template <> struct hash<float>;
  template <> struct hash<double>;
  template <> struct hash<long double>;

  template<class T> struct hash<T*>;
}
```

If a C++program wants to have a by-element addition of two vectors `a`
and `b` containing `double` and put the result into `a`, it can do:

``` cpp
transform(a.begin(), a.end(), b.begin(), a.begin(), plus<double>());
```

To negate every element of `a`:

``` cpp
transform(a.begin(), a.end(), a.begin(), negate<double>());
```

To enable adaptors and other components to manipulate function objects
that take one or two arguments many of the function objects in this
clause correspondingly provide typedefs `argument_type` and
`result_type` for function objects that take one argument and
`first_argument_type`, `second_argument_type`, and `result_type` for
function objects that take two arguments.

### Definitions <a id="func.def">[[func.def]]</a>

The following definitions apply to this Clause:

A *call signature* is the name of a return type followed by a
parenthesized comma-separated list of zero or more argument types.

A *callable type* is a function object type ([[function.objects]]) or a
pointer to member.

A *callable object* is an object of a callable type.

A *call wrapper type* is a type that holds a callable object and
supports a call operation that forwards to that object.

A *call wrapper* is an object of a call wrapper type.

A *target object* is the callable object held by a call wrapper.

### Requirements <a id="func.require">[[func.require]]</a>

Define `INVOKE(f, t1, t2, ..., tN)` as follows:

- `(t1.*f)(t2, ..., tN)` when `f` is a pointer to a member function of a
  class `T` and `t1` is an object of type `T` or a reference to an
  object of type `T` or a reference to an object of a type derived from
  `T`;
- `((*t1).*f)(t2, ..., tN)` when `f` is a pointer to a member function
  of a class `T` and `t1` is not one of the types described in the
  previous item;
- `t1.*f` when `N == 1` and `f` is a pointer to member data of a class
  `T` and `t1` is an object of type `T` or a reference to an object of
  type `T` or a reference to an object of a type derived from `T`;
- `(*t1).*f` when `N == 1` and `f` is a pointer to member data of a
  class `T` and `t1` is not one of the types described in the previous
  item;
- `f(t1, t2, ..., tN)` in all other cases.

Define `INVOKE(f, t1, t2, ..., tN, R)` as `INVOKE(f, t1, t2, ..., tN)`
implicitly converted to `R`.

If a call wrapper ([[func.def]]) has a *weak result type* the type of
its member type `result_type` is based on the type `T` of the wrapper’s
target object ([[func.def]]):

- if `T` is a pointer to function type, `result_type` shall be a synonym
  for the return type of `T`;
- if `T` is a pointer to member function, `result_type` shall be a
  synonym for the return type of `T`;
- if `T` is a class type with a member type `result_type`, then
  `result_type` shall be a synonym for `T::result_type`;
- otherwise `result_type` shall not be defined.

Every call wrapper ([[func.def]]) shall be `MoveConstructible`. A
*simple call wrapper* is a call wrapper that is `CopyConstructible` and
`CopyAssignable` and whose copy constructor, move constructor, and
assignment operator do not throw exceptions. A *forwarding call wrapper*
is a call wrapper that can be called with an arbitrary argument list and
delivers the arguments to the wrapped callable object as references.
This forwarding step shall ensure that rvalue arguments are delivered as
rvalue-references and lvalue arguments are delivered as
lvalue-references. In a typical implementation forwarding call wrappers
have an overloaded function call operator of the form

``` cpp
template<class... UnBoundArgs>
R operator()(UnBoundArgs&&... unbound_args) cv-qual;
```

### Class template `reference_wrapper` <a id="refwrap">[[refwrap]]</a>

``` cpp
namespace std {
  template <class T> class reference_wrapper {
  public :
    // types
    typedef T type;
    typedef see below result_type;               // not always defined
    typedef see below argument_type;             // not always defined
    typedef see below first_argument_type;       // not always defined
    typedef see below second_argument_type;      // not always defined

    // construct/copy/destroy
    reference_wrapper(T&) noexcept;
    reference_wrapper(T&&) = delete;     // do not bind to temporary objects
    reference_wrapper(const reference_wrapper& x) noexcept;

    // assignment
    reference_wrapper& operator=(const reference_wrapper& x) noexcept;

    // access
    operator T& () const noexcept;
    T& get() const noexcept;

    // invocation
    template <class... ArgTypes>
    result_of_t<T&(ArgTypes&&...)>
    operator() (ArgTypes&&...) const;
  };
}
```

`reference_wrapper<T>` is a `CopyConstructible` and `CopyAssignable`
wrapper around a reference to an object or function of type `T`.

`reference_wrapper<T>` has a weak result type ([[func.require]]). If
`T` is a function type, `result_type` shall be a synonym for the return
type of `T`.

The template specialization `reference_wrapper<T>` shall define a nested
type named `argument_type` as a synonym for `T1` only if the type `T` is
any of the following:

- a function type or a pointer to function type taking one argument of
  type `T1`
- a pointer to member function `R T0::f` *cv* (where *cv* represents the
  member function’s cv-qualifiers); the type `T1` is *cv* `T0*`
- a class type with a member type `argument_type`; the type `T1` is
  `T::argument_type`.

The template instantiation `reference_wrapper<T>` shall define two
nested types named `first_argument_type` and `second_argument_type` as
synonyms for `T1` and `T2`, respectively, only if the type `T` is any of
the following:

- a function type or a pointer to function type taking two arguments of
  types `T1` and `T2`
- a pointer to member function `R T0::f(T2)` *cv* (where *cv* represents
  the member function’s cv-qualifiers); the type `T1` is *cv* `T0*`
- a class type with member types `first_argument_type` and
  `second_argument_type`; the type `T1` is `T::first_argument_type` and
  the type `T2` is `T::second_argument_type`.

#### `reference_wrapper` construct/copy/destroy <a id="refwrap.const">[[refwrap.const]]</a>

``` cpp
reference_wrapper(T& t) noexcept;
```

*Effects:* Constructs a `reference_wrapper` object that stores a
reference to `t`.

``` cpp
reference_wrapper(const reference_wrapper& x) noexcept;
```

*Effects:* Constructs a `reference_wrapper` object that stores a
reference to `x.get()`.

#### `reference_wrapper` assignment <a id="refwrap.assign">[[refwrap.assign]]</a>

``` cpp
reference_wrapper& operator=(const reference_wrapper& x) noexcept;
```

*Postconditions:* `*this` stores a reference to `x.get()`.

#### `reference_wrapper` access <a id="refwrap.access">[[refwrap.access]]</a>

``` cpp
operator T& () const noexcept;
```

*Returns:* The stored reference.

``` cpp
T& get() const noexcept;
```

*Returns:* The stored reference.

#### reference_wrapper invocation <a id="refwrap.invoke">[[refwrap.invoke]]</a>

``` cpp
template <class... ArgTypes>
  result_of_t<T&(ArgTypes&&... )>
    operator()(ArgTypes&&... args) const;
```

*Returns:*
*`INVOKE`*`(get(), std::forward<ArgTypes>(args)...)`. ([[func.require]])

`operator()` is described for exposition only. Implementations are not
required to provide an actual `reference_wrapper::operator()`.
Implementations are permitted to support `reference_wrapper` function
invocation through multiple overloaded operators or through other means.

#### reference_wrapper helper functions <a id="refwrap.helpers">[[refwrap.helpers]]</a>

``` cpp
template <class T> reference_wrapper<T> ref(T& t) noexcept;
```

*Returns:* `reference_wrapper<T>(t)`

``` cpp
template <class T> reference_wrapper<T> ref(reference_wrapper<T> t) noexcept;
```

*Returns:* `ref(t.get())`

``` cpp
template <class T> reference_wrapper<const T> cref(const T& t) noexcept;
```

*Returns:* `reference_wrapper <const T>(t)`

``` cpp
template <class T> reference_wrapper<const T> cref(reference_wrapper<T> t) noexcept;
```

*Returns:* `cref(t.get());`

### Arithmetic operations <a id="arithmetic.operations">[[arithmetic.operations]]</a>

The library provides basic function object classes for all of the
arithmetic operators in the language ([[expr.mul]], [[expr.add]]).

``` cpp
template <class T = void> struct plus {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x + y`.

``` cpp
template <class T = void> struct minus {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x - y`.

``` cpp
template <class T = void> struct multiplies {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x * y`.

``` cpp
template <class T = void> struct divides {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x / y`.

``` cpp
template <class T = void> struct modulus {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x % y`.

``` cpp
template <class T = void> struct negate {
  constexpr T operator()(const T& x) const;
  typedef T argument_type;
  typedef T result_type;
};
```

`operator()` returns `-x`.

``` cpp
template <> struct plus<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) + std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) + std::forward<U>(u)`.

``` cpp
template <> struct minus<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) - std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) - std::forward<U>(u)`.

``` cpp
template <> struct multiplies<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) * std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) * std::forward<U>(u)`.

``` cpp
template <> struct divides<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) / std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) / std::forward<U>(u)`.

``` cpp
template <> struct modulus<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) % std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) % std::forward<U>(u)`.

``` cpp
template <> struct negate<void> {
  template <class T> constexpr auto operator()(T&& t) const
    -> decltype(-std::forward<T>(t));

  typedef unspecified is_transparent;
};
```

`operator()` returns `-std::forward<T>(t)`.

### Comparisons <a id="comparisons">[[comparisons]]</a>

The library provides basic function object classes for all of the
comparison operators in the language ([[expr.rel]], [[expr.eq]]).

``` cpp
template <class T = void> struct equal_to {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x == y`.

``` cpp
template <class T = void> struct not_equal_to {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x != y`.

``` cpp
template <class T = void> struct greater {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x > y`.

``` cpp
template <class T = void> struct less {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x < y`.

``` cpp
template <class T = void> struct greater_equal {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x >= y`.

``` cpp
template <class T = void> struct less_equal {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x <= y`.

``` cpp
template <> struct equal_to<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) == std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) == std::forward<U>(u)`.

``` cpp
template <> struct not_equal_to<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) != std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) != std::forward<U>(u)`.

``` cpp
template <> struct greater<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) > std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) > std::forward<U>(u)`.

``` cpp
template <> struct less<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) < std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) < std::forward<U>(u)`.

``` cpp
template <> struct greater_equal<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) >= std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) >= std::forward<U>(u)`.

``` cpp
template <> struct less_equal<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) <= std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) <= std::forward<U>(u)`.

For templates `greater`, `less`, `greater_equal`, and `less_equal`, the
specializations for any pointer type yield a total order, even if the
built-in operators `<`, `>`, `<=`, `>=` do not.

### Logical operations <a id="logical.operations">[[logical.operations]]</a>

The library provides basic function object classes for all of the
logical operators in the language ([[expr.log.and]], [[expr.log.or]],
[[expr.unary.op]]).

``` cpp
template <class T = void> struct logical_and {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x && y`.

``` cpp
template <class T = void> struct logical_or {
  constexpr bool operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef bool result_type;
};
```

`operator()` returns `x || y`.

``` cpp
template <class T = void> struct logical_not {
  constexpr bool operator()(const T& x) const;
  typedef T argument_type;
  typedef bool result_type;
};
```

`operator()` returns `!x`.

``` cpp
template <> struct logical_and<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) && std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) && std::forward<U>(u)`.

``` cpp
template <> struct logical_or<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) || std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) || std::forward<U>(u)`.

``` cpp
template <> struct logical_not<void> {
  template <class T> constexpr auto operator()(T&& t) const
    -> decltype(!std::forward<T>(t));

  typedef unspecified is_transparent;
};
```

`operator()` returns `!std::forward<T>(t)`.

### Bitwise operations <a id="bitwise.operations">[[bitwise.operations]]</a>

The library provides basic function object classes for all of the
bitwise operators in the language ([[expr.bit.and]], [[expr.or]],
[[expr.xor]], [[expr.unary.op]]).

``` cpp
template <class T = void> struct bit_and {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x & y`.

``` cpp
template <class T = void> struct bit_or {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x | y`.

``` cpp
template <class T = void> struct bit_xor {
  constexpr T operator()(const T& x, const T& y) const;
  typedef T first_argument_type;
  typedef T second_argument_type;
  typedef T result_type;
};
```

`operator()` returns `x ^ y`.

``` cpp
template <class T = void> struct bit_not {
  constexpr T operator()(const T& x) const;
  typedef T argument_type;
  typedef T result_type;
};
```

`operator()` returns `~x`.

``` cpp
template <> struct bit_and<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) & std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) & std::forward<U>(u)`.

``` cpp
template <> struct bit_or<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) | std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) | std::forward<U>(u)`.

``` cpp
template <> struct bit_xor<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) ^ std::forward<U>(u));

  typedef unspecified is_transparent;
};
```

`operator()` returns `std::forward<T>(t) ^ std::forward<U>(u)`.

``` cpp
template <> struct bit_not<void> {
  template <class T> constexpr auto operator()(T&& t) const
    -> decltype(~std::forward<T>(t));

  typedef unspecified is_transparent;
};
```

`operator()` returns `~std::forward<T>(t)`.

### Negators <a id="negators">[[negators]]</a>

Negators `not1` and `not2` take a unary and a binary predicate,
respectively, and return their complements ([[expr.unary.op]]).

``` cpp
template <class Predicate>
  class unary_negate {
public:
  constexpr explicit unary_negate(const Predicate& pred);
  constexpr bool operator()(const typename Predicate::argument_type& x) const;
  typedef typename Predicate::argument_type argument_type;
  typedef bool result_type;
};
```

`operator()` returns `!pred(x)`.

``` cpp
template <class Predicate>
  constexpr unary_negate<Predicate> not1(const Predicate& pred);
```

*Returns:* `unary_negate<Predicate>(pred)`.

``` cpp
template <class Predicate>
  class binary_negate {
  public:
    constexpr explicit binary_negate(const Predicate& pred);
    constexpr bool operator()(const typename Predicate::first_argument_type& x,
        const typename Predicate::second_argument_type& y) const;
  typedef typename Predicate::first_argument_type first_argument_type;
  typedef typename Predicate::second_argument_type second_argument_type;
  typedef bool result_type;
  };
```

`operator()` returns `!pred(x,y)`.

``` cpp
template <class Predicate>
  constexpr binary_negate<Predicate> not2(const Predicate& pred);
```

*Returns:* `binary_negate<Predicate>(pred)`.

### Function object binders <a id="func.bind">[[func.bind]]</a>

This subclause describes a uniform mechanism for binding arguments of
callable objects.

#### Class template `is_bind_expression` <a id="func.bind.isbind">[[func.bind.isbind]]</a>

``` cpp
namespace std {
  template<class T> struct is_bind_expression; // see below
}
```

`is_bind_expression` can be used to detect function objects generated by
`bind`. `bind` uses `is_bind_expression` to detect subexpressions.

Instantiations of the `is_bind_expression` template shall meet the
UnaryTypeTrait requirements ([[meta.rqmts]]). The implementation shall
provide a definition that has a BaseCharacteristic of `true_type` if `T`
is a type returned from `bind`, otherwise it shall have a
BaseCharacteristic of `false_type`. A program may specialize this
template for a user-defined type `T` to have a BaseCharacteristic of
`true_type` to indicate that `T` should be treated as a subexpression in
a `bind` call.

#### Class template `is_placeholder` <a id="func.bind.isplace">[[func.bind.isplace]]</a>

``` cpp
namespace std {
  template<class T> struct is_placeholder; // see below
}
```

`is_placeholder` can be used to detect the standard placeholders `_1`,
`_2`, and so on. `bind` uses `is_placeholder` to detect placeholders.

Instantiations of the `is_placeholder` template shall meet the
UnaryTypeTrait requirements ([[meta.rqmts]]). The implementation shall
provide a definition that has the BaseCharacteristic of
`integral_constant<int, J>` if `T` is the type of
`std::placeholders::_J`, otherwise it shall have a BaseCharacteristic of
`integral_constant<int, 0>`. A program may specialize this template for
a user-defined type `T` to have a BaseCharacteristic of
`integral_constant<int, N>` with `N > 0` to indicate that `T` should be
treated as a placeholder type.

#### Function template `bind` <a id="func.bind.bind">[[func.bind.bind]]</a>

In the text that follows, the following names have the following
meanings:

- `FD` is the type `decay_t<F>`,
- `fd` is an lvalue of type `FD` constructed from `std::forward<F>(f)`,
- `Ti` is the iᵗʰ type in the template parameter pack `BoundArgs`,
- `TiD` is the type `decay_t<Ti>`,
- `ti` is the iᵗʰ argument in the function parameter pack `bound_args`,
- `tid` is an lvalue of type `TiD` constructed from
  `std::forward<Ti>(ti)`,
- `Uj` is the jᵗʰ deduced type of the `UnBoundArgs&&...` parameter of
  the forwarding call wrapper, and
- `uj` is the jᵗʰ argument associated with `Uj`.

``` cpp
template<class F, class... BoundArgs>
  unspecified bind(F&& f, BoundArgs&&... bound_args);
```

*Requires:* `is_constructible<FD, F>::value` shall be `true`. For each
`Ti` in `BoundArgs`, `is_constructible<TiD, Ti>::value` shall be `true`.
*`INVOKE`*` (fd, w1, w2, ..., wN)` ([[func.require]]) shall be a valid
expression for some values *w1, w2, ..., wN*, where
`N == sizeof...(bound_args)`.

*Returns:* A forwarding call wrapper `g` with a weak result
type ([[func.require]]). The effect of `g(u1, u2, ..., uM)` shall be
*`INVOKE`*`(fd, std::forward<V1>(v1), std::forward<V2>(v2), ..., std::forward<VN>(vN), result_of_t<FD `*`cv`*` & (V1, V2, ..., VN)>)`,
where *`cv`* represents the *cv*-qualifiers of `g` and the values and
types of the bound arguments `v1, v2, ..., vN` are determined as
specified below. The copy constructor and move constructor of the
forwarding call wrapper shall throw an exception if and only if the
corresponding constructor of `FD` or of any of the types `TiD` throws an
exception.

*Throws:* Nothing unless the construction of `fd` or of one of the
values `tid` throws an exception.

*Remarks:* The return type shall satisfy the requirements of
`MoveConstructible`. If all of `FD` and `TiD` satisfy the requirements
of `CopyConstructible`, then the return type shall satisfy the
requirements of `CopyConstructible`. This implies that all of `FD` and
`TiD` are `MoveConstructible`.

``` cpp
template<class R, class F, class... BoundArgs>
  unspecified bind(F&& f, BoundArgs&&... bound_args);
```

*Requires:* `is_constructible<FD, F>::value` shall be `true`. For each
`Ti` in `BoundArgs`, `is_constructible<TiD, Ti>::value` shall be `true`.
*`INVOKE`*`(fd, w1, w2, ..., wN)` shall be a valid expression for some
values *w1, w2, ..., wN*, where `N == sizeof...(bound_args)`.

*Returns:* A forwarding call wrapper `g` with a nested type
`result_type` defined as a synonym for `R`. The effect of
`g(u1, u2, ..., uM)` shall be
*`INVOKE`*`(fd, std::forward<V1>(v1), std::forward<V2>(v2), ..., std::forward<VN>(vN), R)`,
where the values and types of the bound arguments `v1, v2, ..., vN` are
determined as specified below. The copy constructor and move constructor
of the forwarding call wrapper shall throw an exception if and only if
the corresponding constructor of `FD` or of any of the types `TiD`
throws an exception.

*Throws:* Nothing unless the construction of `fd` or of one of the
values `tid` throws an exception.

*Remarks:* The return type shall satisfy the requirements of
`MoveConstructible`. If all of `FD` and `TiD` satisfy the requirements
of `CopyConstructible`, then the return type shall satisfy the
requirements of `CopyConstructible`. This implies that all of `FD` and
`TiD` are `MoveConstructible`.

The values of the *bound arguments* `v1, v2, ..., vN` and their
corresponding types `V1, V2, ..., VN` depend on the types `TiD` derived
from the call to `bind` and the *cv*-qualifiers *cv* of the call wrapper
`g` as follows:

- if `TiD` is `reference_wrapper<T>`, the argument is `tid.get()` and
  its type `Vi` is `T&`;
- if the value of `is_bind_expression<TiD>::value` is `true`, the
  argument is `tid(std::forward<Uj>({}uj)...)` and its type `Vi` is
  `result_of_t<TiD cv & (Uj&&...)>&&`;
- if the value `j` of `is_placeholder<TiD>::value` is not zero, the
  argument is `std::forward<Uj>(uj)` and its type `Vi` is `Uj&&`;
- otherwise, the value is `tid` and its type `Vi` is `TiD cv &`.

#### Placeholders <a id="func.bind.place">[[func.bind.place]]</a>

``` cpp
namespace std {
  namespace placeholders {
    // M is the implementation-defined number of placeholders
    extern unspecified _1;
    extern unspecified _2;
                .
                .
                .
    extern unspecified _M;
  }
}
```

All placeholder types shall be `DefaultConstructible` and
`CopyConstructible`, and their default constructors and copy/move
constructors shall not throw exceptions. It is *implementation-defined*
whether placeholder types are `CopyAssignable`. `CopyAssignable`
placeholders’ copy assignment operators shall not throw exceptions.

### Function template `mem_fn` <a id="func.memfn">[[func.memfn]]</a>

``` cpp
template<class R, class T> unspecified mem_fn(R T::* pm);
```

*Returns:* A simple call wrapper ([[func.def]]) `fn` such that the
expression `fn(t, a2, ..., aN)` is equivalent to
*`INVOKE`*`(pm, t, a2, ..., aN)` ([[func.require]]). `fn` shall have a
nested type `result_type` that is a synonym for the return type of `pm`
when `pm` is a pointer to member function.

The simple call wrapper shall define two nested types named
`argument_type` and `result_type` as synonyms for `cv T*` and `Ret`,
respectively, when `pm` is a pointer to member function with
cv-qualifier *cv* and taking no arguments, where *Ret* is `pm`’s return
type.

The simple call wrapper shall define three nested types named
`first_argument_type`, `second_argument_type`, and `result_type` as
synonyms for `cv T*`, `T1`, and `Ret`, respectively, when `pm` is a
pointer to member function with cv-qualifier *cv* and taking one
argument of type `T1`, where *Ret* is `pm`’s return type.

*Throws:* Nothing.

### Polymorphic function wrappers <a id="func.wrap">[[func.wrap]]</a>

This subclause describes a polymorphic wrapper class that encapsulates
arbitrary callable objects.

#### Class `bad_function_call` <a id="func.wrap.badcall">[[func.wrap.badcall]]</a>

An exception of type `bad_function_call` is thrown by
`function::operator()` ([[func.wrap.func.inv]]) when the function
wrapper object has no target.

``` cpp
namespace std {
  class bad_function_call : public std::exception {
  public:
    // [func.wrap.badcall.const], constructor:
    bad_function_call() noexcept;
  };
} // namespace std
```

##### `bad_function_call` constructor <a id="func.wrap.badcall.const">[[func.wrap.badcall.const]]</a>

``` cpp
bad_function_call() noexcept;
```

*Effects:* constructs a `bad_function_call` object.

#### Class template `function` <a id="func.wrap.func">[[func.wrap.func]]</a>

``` cpp
namespace std {
  template<class> class function; // undefined

  template<class R, class... ArgTypes>
  class function<R(ArgTypes...)> {
  public:
    typedef R result_type;
    typedef T1 argument_type;           // only if sizeof...(ArgTypes) == 1 and
                                        // the type in ArgTypes is T1
    typedef T1 first_argument_type;     // only if sizeof...(ArgTypes) == 2 and
                                        // ArgTypes contains T1 and T2
    typedef T2 second_argument_type;    // only if sizeof...(ArgTypes) == 2 and
                                        // ArgTypes contains T1 and T2

    // [func.wrap.func.con], construct/copy/destroy:
    function() noexcept;
    function(nullptr_t) noexcept;
    function(const function&);
    function(function&&);
    template<class F> function(F);
    template<class A> function(allocator_arg_t, const A&) noexcept;
    template<class A> function(allocator_arg_t, const A&,
      nullptr_t) noexcept;
    template<class A> function(allocator_arg_t, const A&,
      const function&);
    template<class A> function(allocator_arg_t, const A&,
      function&&);
    template<class F, class A> function(allocator_arg_t, const A&, F);

    function& operator=(const function&);
    function& operator=(function&&);
    function& operator=(nullptr_t);
    template<class F> function& operator=(F&&);
    template<class F> function& operator=(reference_wrapper<F>) noexcept;

    ~function();

    // [func.wrap.func.mod], function modifiers:
    void swap(function&) noexcept;
    template<class F, class A> void assign(F&&, const A&);

    // [func.wrap.func.cap], function capacity:
    explicit operator bool() const noexcept;

    // [func.wrap.func.inv], function invocation:
    R operator()(ArgTypes...) const;

    // [func.wrap.func.targ], function target access:
    const std::type_info& target_type() const noexcept;
    template<class T>       T* target() noexcept;
    template<class T> const T* target() const noexcept;

  };

  // [func.wrap.func.nullptr], Null pointer comparisons:
  template <class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

  template <class R, class... ArgTypes>
    bool operator==(nullptr_t, const function<R(ArgTypes...)>&) noexcept;

  template <class R, class... ArgTypes>
    bool operator!=(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

  template <class R, class... ArgTypes>
    bool operator!=(nullptr_t, const function<R(ArgTypes...)>&) noexcept;

  // [func.wrap.func.alg], specialized algorithms:
  template <class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&);

  template<class R, class... ArgTypes, class Alloc>
    struct uses_allocator<function<R(ArgTypes...)>, Alloc>
      : true_type { };
}
```

The `function` class template provides polymorphic wrappers that
generalize the notion of a function pointer. Wrappers can store, copy,
and call arbitrary callable objects ([[func.def]]), given a call
signature ([[func.def]]), allowing functions to be first-class objects.

A callable object `f` of type `F` is *Callable* for argument types
`ArgTypes` and return type `R` if the expression
`INVOKE(f, declval<ArgTypes>()..., R)`, considered as an unevaluated
operand (Clause  [[expr]]), is well formed ([[func.require]]).

The `function` class template is a call wrapper ([[func.def]]) whose
call signature ([[func.def]]) is `R(ArgTypes...)`.

##### `function` construct/copy/destroy <a id="func.wrap.func.con">[[func.wrap.func.con]]</a>

When any `function` constructor that takes a first argument of type
`allocator_arg_t` is invoked, the second argument shall have a type that
conforms to the requirements for Allocator (Table 
[[allocator.requirements]]). A copy of the allocator argument is used to
allocate memory, if necessary, for the internal data structures of the
constructed `function` object.

``` cpp
function() noexcept;
template <class A> function(allocator_arg_t, const A& a) noexcept;
```

*Postconditions:* `!*this`.

``` cpp
function(nullptr_t) noexcept;
template <class A> function(allocator_arg_t, const A& a, nullptr_t) noexcept;
```

*Postconditions:* `!*this`.

``` cpp
function(const function& f);
template <class A> function(allocator_arg_t, const A& a, const function& f);
```

*Postconditions:* `!*this` if `!f`; otherwise, `*this` targets a copy of
`f.target()`.

*Throws:* shall not throw exceptions if `f`’s target is a callable
object passed via `reference_wrapper` or a function pointer. Otherwise,
may throw `bad_alloc` or any exception thrown by the copy constructor of
the stored callable object. Implementations are encouraged to avoid the
use of dynamically allocated memory for small callable objects, for
example, where `f`’s target is an object holding only a pointer or
reference to an object and a member function pointer.

``` cpp
function(function&& f);
template <class A> function(allocator_arg_t, const A& a, function&& f);
```

*Effects:* If `!f`, `*this` has no target; otherwise, move-constructs
the target of `f` into the target of `*this`, leaving `f` in a valid
state with an unspecified value.

``` cpp
template<class F> function(F f);
template <class F, class A> function(allocator_arg_t, const A& a, F f);
```

*Requires:* `F` shall be `CopyConstructible`.

*Remarks:* These constructors shall not participate in overload
resolution unless `f` is Callable ([[func.wrap.func]]) for argument
types `ArgTypes...` and return type `R`.

*Postconditions:* `!*this` if any of the following hold:

- `f` is a null function pointer value.
- `f` is a null member pointer value.
- `F` is an instance of the `function` class template, and `!f`.

Otherwise, `*this` targets a copy of `f` initialized with
`std::move(f)`. Implementations are encouraged to avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f`’s target is an object holding only a pointer or reference to
an object and a member function pointer.

*Throws:* shall not throw exceptions when `f` is a function pointer or a
`reference_wrapper<T>` for some `T`. Otherwise, may throw `bad_alloc` or
any exception thrown by `F`’s copy or move constructor.

``` cpp
function& operator=(const function& f);
```

*Effects:* `function(f).swap(*this);`

*Returns:* `*this`

``` cpp
function& operator=(function&& f);
```

*Effects:* Replaces the target of `*this` with the target of `f`.

*Returns:* `*this`

``` cpp
function& operator=(nullptr_t);
```

*Effects:* If `*this != nullptr`, destroys the target of `this`.

*Postconditions:* `!(*this)`.

*Returns:* `*this`

``` cpp
template<class F> function& operator=(F&& f);
```

*Effects:* `function(std::forward<F>(f)).swap(*this);`

*Returns:* `*this`

*Remarks:* This assignment operator shall not participate in overload
resolution unless `declval<typename decay<F>::type&>()` is
Callable ([[func.wrap.func]]) for argument types `ArgTypes...` and
return type `R`.

``` cpp
template<class F> function& operator=(reference_wrapper<F> f) noexcept;
```

*Effects:* `function(f).swap(*this);`

*Returns:* `*this`

``` cpp
~function();
```

*Effects:* If `*this != nullptr`, destroys the target of `this`.

##### `function` modifiers <a id="func.wrap.func.mod">[[func.wrap.func.mod]]</a>

``` cpp
void swap(function& other) noexcept;
```

*Effects:* interchanges the targets of `*this` and `other`.

``` cpp
template<class F, class A>
  void assign(F&& f, const A& a);
```

*Effects:* `function(allocator_arg, a, std::forward<F>(f)).swap(*this)`

##### `function` capacity <a id="func.wrap.func.cap">[[func.wrap.func.cap]]</a>

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `true` if `*this` has a target, otherwise `false`.

##### `function` invocation <a id="func.wrap.func.inv">[[func.wrap.func.inv]]</a>

``` cpp
R operator()(ArgTypes... args) const
```

*Effects:*
*`INVOKE`*`(f, std::forward<ArgTypes>(args)..., R)` ([[func.require]]),
where `f` is the target object ([[func.def]]) of `*this`.

*Returns:* Nothing if `R` is `void`, otherwise the return value of
*`INVOKE`*`(f, std::forward<ArgTypes>(args)..., R)`.

*Throws:* `bad_function_call` if `!*this`; otherwise, any exception
thrown by the wrapped callable object.

##### function target access <a id="func.wrap.func.targ">[[func.wrap.func.targ]]</a>

``` cpp
const std::type_info& target_type() const noexcept;
```

*Returns:* If `*this` has a target of type `T`, `typeid(T)`; otherwise,
`typeid(void)`.

``` cpp
template<class T>       T* target() noexcept;
template<class T> const T* target() const noexcept;
```

*Requires:* `T` shall be a type that is Callable ([[func.wrap.func]])
for parameter types `ArgTypes` and return type `R`.

*Returns:* If `target_type() == typeid(T)` a pointer to the stored
function target; otherwise a null pointer.

##### null pointer comparison operators <a id="func.wrap.func.nullptr">[[func.wrap.func.nullptr]]</a>

``` cpp
template <class R, class... ArgTypes>
  bool operator==(const function<R(ArgTypes...)>& f, nullptr_t) noexcept;
template <class R, class... ArgTypes>
  bool operator==(nullptr_t, const function<R(ArgTypes...)>& f) noexcept;
```

*Returns:* `!f`.

``` cpp
template <class R, class... ArgTypes>
  bool operator!=(const function<R(ArgTypes...)>& f, nullptr_t) noexcept;
template <class R, class... ArgTypes>
  bool operator!=(nullptr_t, const function<R(ArgTypes...)>& f) noexcept;
```

*Returns:* ` (bool) f`.

##### specialized algorithms <a id="func.wrap.func.alg">[[func.wrap.func.alg]]</a>

``` cpp
template<class R, class... ArgTypes>
  void swap(function<R(ArgTypes...)>& f1, function<R(ArgTypes...)>& f2);
```

*Effects:* `f1.swap(f2);`

### Class template `hash` <a id="unord.hash">[[unord.hash]]</a>

The unordered associative containers defined in [[unord]] use
specializations of the class template `hash` as the default hash
function. For all object types `Key` for which there exists a
specialization `hash<Key>`, and for all enumeration types (
[[dcl.enum]]) `Key`, the instantiation `hash<Key>` shall:

- satisfy the `Hash` requirements ([[hash.requirements]]), with `Key`
  as the function call argument type, the `DefaultConstructible`
  requirements (Table  [[defaultconstructible]]), the `CopyAssignable`
  requirements (Table  [[copyassignable]]),
- be swappable ([[swappable.requirements]]) for lvalues,
- provide two nested types `result_type` and `argument_type` which shall
  be synonyms for `size_t` and `Key`, respectively,
- satisfy the requirement that if `k1 == k2` is true, `h(k1) == h(k2)`
  is also true, where `h` is an object of type `hash<Key>` and `k1` and
  `k2` are objects of type `Key`;
- satisfy the requirement that the expression `h(k)`, where `h` is an
  object of type `hash<Key>` and `k` is an object of type `Key`, shall
  not throw an exception unless `hash<Key>` is a user-defined
  specialization that depends on at least one user-defined type.

``` cpp
template <> struct hash<bool>;
template <> struct hash<char>;
template <> struct hash<signed char>;
template <> struct hash<unsigned char>;
template <> struct hash<char16_t>;
template <> struct hash<char32_t>;
template <> struct hash<wchar_t>;
template <> struct hash<short>;
template <> struct hash<unsigned short>;
template <> struct hash<int>;
template <> struct hash<unsigned int>;
template <> struct hash<long>;
template <> struct hash<unsigned long>;
template <> struct hash<long long>;
template <> struct hash<unsigned long long>;
template <> struct hash<float>;
template <> struct hash<double>;
template <> struct hash<long double>;
template <class T> struct hash<T*>;
```

The template specializations shall meet the requirements of class
template `hash` ([[unord.hash]]).

## Metaprogramming and type traits <a id="meta">[[meta]]</a>

This subclause describes components used by C++programs, particularly in
templates, to support the widest possible range of types, optimise
template code usage, detect type related user errors, and perform type
inference and transformation at compile time. It includes type
classification traits, type property inspection traits, and type
transformations. The type classification traits describe a complete
taxonomy of all possible C++types, and state where in that taxonomy a
given type belongs. The type property inspection traits allow important
characteristics of types or of combinations of types to be inspected.
The type transformations allow certain properties of types to be
manipulated.

### Requirements <a id="meta.rqmts">[[meta.rqmts]]</a>

A *UnaryTypeTrait* describes a property of a type. It shall be a class
template that takes one template type argument and, optionally,
additional arguments that help define the property being described. It
shall be `DefaultConstructible`, `CopyConstructible`, and publicly and
unambiguously derived, directly or indirectly, from its
*BaseCharacteristic*, which is a specialization of the template
`integral_constant` ([[meta.help]]), with the arguments to the template
`integral_constant` determined by the requirements for the particular
property being described. The member names of the BaseCharacteristic
shall not be hidden and shall be unambiguously available in the
UnaryTypeTrait.

A *BinaryTypeTrait* describes a relationship between two types. It shall
be a class template that takes two template type arguments and,
optionally, additional arguments that help define the relationship being
described. It shall be `DefaultConstructible`, `CopyConstructible`, and
publicly and unambiguously derived, directly or indirectly, from its
*BaseCharacteristic*, which is a specialization of the template
`integral_constant` ([[meta.help]]), with the arguments to the template
`integral_constant` determined by the requirements for the particular
relationship being described. The member names of the BaseCharacteristic
shall not be hidden and shall be unambiguously available in the
BinaryTypeTrait.

A *TransformationTrait* modifies a property of a type. It shall be a
class template that takes one template type argument and, optionally,
additional arguments that help define the modification. It shall define
a publicly accessible nested type named `type`, which shall be a synonym
for the modified type.

### Header `<type_traits>` synopsis <a id="meta.type.synop">[[meta.type.synop]]</a>

``` cpp
namespace std {
  // [meta.help], helper class:
  template <class T, T v> struct integral_constant;
  typedef integral_constant<bool, true>  true_type;
  typedef integral_constant<bool, false> false_type;

  // [meta.unary.cat], primary type categories:
  template <class T> struct is_void;
  template <class T> struct is_null_pointer;
  template <class T> struct is_integral;
  template <class T> struct is_floating_point;
  template <class T> struct is_array;
  template <class T> struct is_pointer;
  template <class T> struct is_lvalue_reference;
  template <class T> struct is_rvalue_reference;
  template <class T> struct is_member_object_pointer;
  template <class T> struct is_member_function_pointer;
  template <class T> struct is_enum;
  template <class T> struct is_union;
  template <class T> struct is_class;
  template <class T> struct is_function;

  // [meta.unary.comp], composite type categories:
  template <class T> struct is_reference;
  template <class T> struct is_arithmetic;
  template <class T> struct is_fundamental;
  template <class T> struct is_object;
  template <class T> struct is_scalar;
  template <class T> struct is_compound;
  template <class T> struct is_member_pointer;

  // [meta.unary.prop], type properties:
  template <class T> struct is_const;
  template <class T> struct is_volatile;
  template <class T> struct is_trivial;
  template <class T> struct is_trivially_copyable;
  template <class T> struct is_standard_layout;
  template <class T> struct is_pod;
  template <class T> struct is_literal_type;
  template <class T> struct is_empty;
  template <class T> struct is_polymorphic;
  template <class T> struct is_abstract;
  template <class T> struct is_final;

  template <class T> struct is_signed;
  template <class T> struct is_unsigned;

  template <class T, class... Args> struct is_constructible;
  template <class T> struct is_default_constructible;
  template <class T> struct is_copy_constructible;
  template <class T> struct is_move_constructible;

  template <class T, class U> struct is_assignable;
  template <class T> struct is_copy_assignable;
  template <class T> struct is_move_assignable;

  template <class T> struct is_destructible;

  template <class T, class... Args> struct is_trivially_constructible;
  template <class T> struct is_trivially_default_constructible;
  template <class T> struct is_trivially_copy_constructible;
  template <class T> struct is_trivially_move_constructible;

  template <class T, class U> struct is_trivially_assignable;
  template <class T> struct is_trivially_copy_assignable;
  template <class T> struct is_trivially_move_assignable;
  template <class T> struct is_trivially_destructible;

  template <class T, class... Args> struct is_nothrow_constructible;
  template <class T> struct is_nothrow_default_constructible;
  template <class T> struct is_nothrow_copy_constructible;
  template <class T> struct is_nothrow_move_constructible;

  template <class T, class U> struct is_nothrow_assignable;
  template <class T> struct  is_nothrow_copy_assignable;
  template <class T> struct is_nothrow_move_assignable;

  template <class T> struct is_nothrow_destructible;
  template <class T> struct has_virtual_destructor;

  // [meta.unary.prop.query], type property queries:
  template <class T> struct alignment_of;
  template <class T> struct rank;
  template <class T, unsigned I = 0> struct extent;

  // [meta.rel], type relations:
  template <class T, class U> struct is_same;
  template <class Base, class Derived> struct is_base_of;
  template <class From, class To> struct is_convertible;

  // [meta.trans.cv], const-volatile modifications:
  template <class T> struct remove_const;
  template <class T> struct remove_volatile;
  template <class T> struct remove_cv;
  template <class T> struct add_const;
  template <class T> struct add_volatile;
  template <class T> struct add_cv;

  template <class T>
    using remove_const_t    = typename remove_const<T>::type;
  template <class T>
    using remove_volatile_t = typename remove_volatile<T>::type;
  template <class T>
    using remove_cv_t       = typename remove_cv<T>::type;
  template <class T>
    using add_const_t       = typename add_const<T>::type;
  template <class T>
    using add_volatile_t    = typename add_volatile<T>::type;
  template <class T>
    using add_cv_t          = typename add_cv<T>::type;

  // [meta.trans.ref], reference modifications:
  template <class T> struct remove_reference;
  template <class T> struct add_lvalue_reference;
  template <class T> struct add_rvalue_reference;

  template <class T>
    using remove_reference_t     = typename remove_reference<T>::type;
  template <class T>
    using add_lvalue_reference_t = typename add_lvalue_reference<T>::type;
  template <class T>
    using add_rvalue_reference_t = typename add_rvalue_reference<T>::type;

  // [meta.trans.sign], sign modifications:
  template <class T> struct make_signed;
  template <class T> struct make_unsigned;

  template <class T>
    using make_signed_t   = typename make_signed<T>::type;
  template <class T>
    using make_unsigned_t = typename make_unsigned<T>::type;

  // [meta.trans.arr], array modifications:
  template <class T> struct remove_extent;
  template <class T> struct remove_all_extents;

  template <class T>
    using remove_extent_t      = typename remove_extent<T>::type;
  template <class T>
    using remove_all_extents_t = typename remove_all_extents<T>::type;

  // [meta.trans.ptr], pointer modifications:
  template <class T> struct remove_pointer;
  template <class T> struct add_pointer;

  template <class T>
    using remove_pointer_t = typename remove_pointer<T>::type;
  template <class T>
    using add_pointer_t    = typename add_pointer<T>::type;

  // [meta.trans.other], other transformations:
  template <std::size_t Len,
            std::size_t Align = default-alignment>   // see [meta.trans.other]
    struct aligned_storage;
  template <std::size_t Len, class... Types> struct aligned_union;
  template <class T> struct decay;
  template <bool, class T = void> struct enable_if;
  template <bool, class T, class F> struct conditional;
  template <class... T> struct common_type;
  template <class T> struct underlying_type;
  template <class> class result_of;   // not defined
  template <class F, class... ArgTypes> class result_of<F(ArgTypes...)>;

  template <std::size_t Len,
            std::size_t Align = default-alignment > // see [meta.trans.other]
    using aligned_storage_t = typename aligned_storage<Len,Align>::type;
  template <std::size_t Len, class... Types>
    using aligned_union_t   = typename aligned_union<Len,Types...>::type;
  template <class T>
    using decay_t           = typename decay<T>::type;
  template <bool b, class T = void>
    using enable_if_t       = typename enable_if<b,T>::type;
  template <bool b, class T, class F>
    using conditional_t     = typename conditional<b,T,F>::type;
  template <class... T>
    using common_type_t     = typename common_type<T...>::type;
  template <class T>
    using underlying_type_t = typename underlying_type<T>::type;
  template <class T>
    using result_of_t       = typename result_of<T>::type;
} // namespace std
```

The behavior of a program that adds specializations for any of the class
templates defined in this subclause is undefined unless otherwise
specified.

### Helper classes <a id="meta.help">[[meta.help]]</a>

``` cpp
namespace std {
  template <class T, T v>
  struct integral_constant {
    static constexpr T value = v;
    typedef T value_type;
    typedef integral_constant<T,v> type;
    constexpr operator value_type() const noexcept { return value; }
    constexpr value_type operator()() const noexcept { return value; }
  };
  typedef integral_constant<bool, true> true_type;
  typedef integral_constant<bool, false> false_type;
}
```

The class template `integral_constant` and its associated typedefs
`true_type` and `false_type` are used as base classes to define the
interface for various type traits.

### Unary type traits <a id="meta.unary">[[meta.unary]]</a>

This sub-clause contains templates that may be used to query the
properties of a type at compile time.

Each of these templates shall be a UnaryTypeTrait ([[meta.rqmts]]) with
a BaseCharacteristic of `true_type` if the corresponding condition is
true, otherwise `false_type`.

#### Primary type categories <a id="meta.unary.cat">[[meta.unary.cat]]</a>

The primary type categories correspond to the descriptions given in
section  [[basic.types]] of the C++standard.

For any given type `T`, the result of applying one of these templates to
`T` and to *cv-qualified* `T` shall yield the same result.

For any given type `T`, exactly one of the primary type categories has a
`value` member that evaluates to `true`.

#### Composite type traits <a id="meta.unary.comp">[[meta.unary.comp]]</a>

These templates provide convenient compositions of the primary type
categories, corresponding to the descriptions given in section 
[[basic.types]].

For any given type `T`, the result of applying one of these templates to
`T`, and to *cv-qualified* `T` shall yield the same result.

#### Type properties <a id="meta.unary.prop">[[meta.unary.prop]]</a>

These templates provide access to some of the more important properties
of types.

It is unspecified whether the library defines any full or partial
specializations of any of these templates.

For all of the class templates `X` declared in this Clause,
instantiating that template with a template-argument that is a class
template specialization may result in the implicit instantiation of the
template argument if and only if the semantics of `X` require that the
argument must be a complete type.

``` cpp
is_const<const volatile int>::value     // true
is_const<const int*>::value             // false
is_const<const int&>::value             // false
is_const<int[3]>::value                 // false
is_const<const int[3]>::value           // true
```

``` cpp
remove_const_t<const volatile int>  // volatile int
remove_const_t<const int* const>    // const int*
remove_const_t<const int&>          // const int&
remove_const_t<const int[3]>        // int[3]
```

``` cpp
// Given:
struct P final { };
union U1 { };
union U2 final { };

// the following assertions hold:
static_assert(!is_final<int>::value, "Error!");
static_assert( is_final<P>::value, "Error!");
static_assert(!is_final<U1>::value, "Error!");
static_assert( is_final<U2>::value, "Error!");
```

Given the following function prototype:

``` cpp
template <class T>
  add_rvalue_reference_t<T> create() noexcept;
```

the predicate condition for a template specialization
`is_constructible<T, Args...>` shall be satisfied if and only if the
following variable definition would be well-formed for some invented
variable `t`:

``` cpp
T t(create<Args>()...);
```

These tokens are never interpreted as a function declaration. Access
checking is performed as if in a context unrelated to `T` and any of the
`Args`. Only the validity of the immediate context of the variable
initialization is considered. The evaluation of the initialization can
result in side effects such as the instantiation of class template
specializations and function template specializations, the generation of
implicitly-defined functions, and so on. Such side effects are not in
the “immediate context” and can result in the program being ill-formed.

### Type property queries <a id="meta.unary.prop.query">[[meta.unary.prop.query]]</a>

This sub-clause contains templates that may be used to query properties
of types at compile time.

Each of these templates shall be a `UnaryTypeTrait` ([[meta.rqmts]])
with a `BaseCharacteristic` of `integral_constant<size_t, Value>`.

``` cpp
// the following assertions hold:
assert(rank<int>::value == 0);
assert(rank<int[2]>::value == 1);
assert(rank<int[][4]>::value == 2);
```

``` cpp
// the following assertions hold:
assert(extent<int>::value == 0);
assert(extent<int[2]>::value == 2);
assert(extent<int[2][4]>::value == 2);
assert(extent<int[][4]>::value == 0);
assert((extent<int, 1>::value) == 0);
assert((extent<int[2], 1>::value) == 0);
assert((extent<int[2][4], 1>::value) == 4);
assert((extent<int[][4], 1>::value) == 4);
```

### Relationships between types <a id="meta.rel">[[meta.rel]]</a>

This sub-clause contains templates that may be used to query
relationships between types at compile time.

Each of these templates shall be a BinaryTypeTrait ([[meta.rqmts]])
with a BaseCharacteristic of `true_type` if the corresponding condition
is true, otherwise `false_type`.

``` cpp
struct B {};
struct B1 : B {};
struct B2 : B {};
struct D : private B1, private B2 {};

is_base_of<B, D>::value         // true
is_base_of<const B, D>::value   // true
is_base_of<B, const D>::value   // true
is_base_of<B, const B>::value   // true
is_base_of<D, B>::value         // false
is_base_of<B&, D&>::value       // false
is_base_of<B[3], D[3]>::value   // false
is_base_of<int, int>::value     // false
```

Given the following function prototype:

``` cpp
template <class T>
  add_rvalue_reference_t<T> create() noexcept;
```

the predicate condition for a template specialization
`is_convertible<From, To>` shall be satisfied if and only if the return
expression in the following code would be well-formed, including any
implicit conversions to the return type of the function:

``` cpp
To test() {
  return create<From>();
}
```

This requirement gives well defined results for reference types, void
types, array types, and function types.Access checking is performed as
if in a context unrelated to `To` and `From`. Only the validity of the
immediate context of the expression of the *return-statement* (including
conversions to the return type) is considered. The evaluation of the
conversion can result in side effects such as the instantiation of class
template specializations and function template specializations, the
generation of implicitly-defined functions, and so on. Such side effects
are not in the “immediate context” and can result in the program being
ill-formed.

### Transformations between types <a id="meta.trans">[[meta.trans]]</a>

Each of the templates in this subclause shall be a
*TransformationTrait* ([[meta.rqmts]]).

#### Const-volatile modifications <a id="meta.trans.cv">[[meta.trans.cv]]</a>

#### Reference modifications <a id="meta.trans.ref">[[meta.trans.ref]]</a>

#### Sign modifications <a id="meta.trans.sign">[[meta.trans.sign]]</a>

#### Array modifications <a id="meta.trans.arr">[[meta.trans.arr]]</a>

``` cpp
// the following assertions hold:
assert((is_same<remove_extent_t<int>, int>::value));
assert((is_same<remove_extent_t<int[2]>, int>::value));
assert((is_same<remove_extent_t<int[2][3]>, int[3]>::value));
assert((is_same<remove_extent_t<int[][3]>, int[3]>::value));
```

``` cpp
// the following assertions hold:
assert((is_same<remove_all_extents_t<int>, int>::value));
assert((is_same<remove_all_extents_t<int[2]>, int>::value));
assert((is_same<remove_all_extents_t<int[2][3]>, int>::value));
assert((is_same<remove_all_extents_t<int[][3]>, int>::value));
```

#### Pointer modifications <a id="meta.trans.ptr">[[meta.trans.ptr]]</a>

#### Other transformations <a id="meta.trans.other">[[meta.trans.other]]</a>

A typical implementation would define `aligned_storage` as:

``` cpp
template <std::size_t Len, std::size_t Alignment>
struct aligned_storage {
  typedef struct {
    alignas(Alignment) unsigned char __data[Len];
  } type;
};
```

It is *implementation-defined* whether any extended alignment is
supported ([[basic.align]]).

The nested typedef `common_type::type` shall be defined as follows:

``` cpp
template <class ...T> struct common_type;

template <class T>
struct common_type<T> {
  typedef decay_t<T> type;
};

template <class T, class U>
struct common_type<T, U> {
  typedef decay_t<decltype(true ? declval<T>() : declval<U>())> type;
};

template <class T, class U, class... V>
struct common_type<T, U, V...> {
  typedef common_type_t<common_type_t<T, U>, V...> type;
};
```

Given these definitions:

``` cpp
typedef bool (&PF1)();
typedef short (*PF2)(long);

struct S {
  operator PF2() const;
  double operator()(char, int&);
  void fn(long) const;
  char data;
};

typedef void (S::*PMF)(long) const;
typedef char S::*PMD;
```

the following assertions will hold:

``` cpp
static_assert(is_same<result_of_t<S(int)>, short>::value, "Error!");
static_assert(is_same<result_of_t<S&(unsigned char, int&)>, double>::value, "Error!");
static_assert(is_same<result_of_t<PF1()>, bool>::value, "Error!");
static_assert(is_same<result_of_t<PMF(unique_ptr<S>, int)>, void>::value, "Error!");
static_assert(is_same<result_of_t<PMD(S)>, char&&>::value, "Error!");
static_assert(is_same<result_of_t<PMD(const S*)>, const char&>::value, "Error!");
```

## Compile-time rational arithmetic <a id="ratio">[[ratio]]</a>

### In general <a id="ratio.general">[[ratio.general]]</a>

This subclause describes the ratio library. It provides a class template
`ratio` which exactly represents any finite rational number with a
numerator and denominator representable by compile-time constants of
type `intmax_t`.

Throughout this subclause, the names of template parameters are used to
express type requirements. If a template parameter is named `R1` or
`R2`, and the template argument is not a specialization of the `ratio`
template, the program is ill-formed.

### Header `<ratio>` synopsis <a id="ratio.syn">[[ratio.syn]]</a>

``` cpp
namespace std {
  // [ratio.ratio], class template ratio
  template <intmax_t N, intmax_t D = 1> class ratio;

  // [ratio.arithmetic], ratio arithmetic
  template <class R1, class R2> using ratio_add = see below;
  template <class R1, class R2> using ratio_subtract = see below;
  template <class R1, class R2> using ratio_multiply = see below;
  template <class R1, class R2> using ratio_divide = see below;

  // [ratio.comparison], ratio comparison
  template <class R1, class R2> struct ratio_equal;
  template <class R1, class R2> struct ratio_not_equal;
  template <class R1, class R2> struct ratio_less;
  template <class R1, class R2> struct ratio_less_equal;
  template <class R1, class R2> struct ratio_greater;
  template <class R1, class R2> struct ratio_greater_equal;

  // [ratio.si], convenience SI typedefs
  typedef ratio<1, 1'000'000'000'000'000'000'000'000> yocto;  // see below
  typedef ratio<1,     1'000'000'000'000'000'000'000> zepto;  // see below
  typedef ratio<1,         1'000'000'000'000'000'000> atto;
  typedef ratio<1,             1'000'000'000'000'000> femto;
  typedef ratio<1,                 1'000'000'000'000> pico;
  typedef ratio<1,                     1'000'000'000> nano;
  typedef ratio<1,                         1'000'000> micro;
  typedef ratio<1,                             1'000> milli;
  typedef ratio<1,                               100> centi;
  typedef ratio<1,                                10> deci;
  typedef ratio<                               10, 1> deca;
  typedef ratio<                              100, 1> hecto;
  typedef ratio<                            1'000, 1> kilo;
  typedef ratio<                        1'000'000, 1> mega;
  typedef ratio<                    1'000'000'000, 1> giga;
  typedef ratio<                1'000'000'000'000, 1> tera;
  typedef ratio<            1'000'000'000'000'000, 1> peta;
  typedef ratio<        1'000'000'000'000'000'000, 1> exa;
  typedef ratio<    1'000'000'000'000'000'000'000, 1> zetta;  // see below
  typedef ratio<1'000'000'000'000'000'000'000'000, 1> yotta;  // see below
}
```

### Class template `ratio` <a id="ratio.ratio">[[ratio.ratio]]</a>

``` cpp
namespace std {
  template <intmax_t N, intmax_t D = 1>
  class ratio {
  public:
    static constexpr intmax_t num;
    static constexpr intmax_t den;
    typedef ratio<num, den> type;
  };
}
```

If the template argument `D` is zero or the absolute values of either of
the template arguments `N` and `D` is not representable by type
`intmax_t`, the program is ill-formed. These rules ensure that infinite
ratios are avoided and that for any negative input, there exists a
representable value of its absolute value which is positive. In a two’s
complement representation, this excludes the most negative value.

The static data members `num` and `den` shall have the following values,
where `gcd` represents the greatest common divisor of the absolute
values of `N` and `D`:

- `num` shall have the value `sign(N) * sign(D) * abs(N) / gcd`.
- `den` shall have the value `abs(D) / gcd`.

### Arithmetic on `ratio`s <a id="ratio.arithmetic">[[ratio.arithmetic]]</a>

Each of the alias templates `ratio_add`, `ratio_subtract`,
`ratio_multiply`, and `ratio_divide` denotes the result of an arithmetic
computation on two `ratio`s `R1` and `R2`. With `X` and `Y` computed (in
the absence of arithmetic overflow) as specified by Table 
[[tab:ratio.arithmetic]], each alias denotes a `ratio<U, V>` such that
`U` is the same as `ratio<X, Y>::num` and `V` is the same as
`ratio<X, Y>::den`.

If it is not possible to represent `U` or `V` with `intmax_t`, the
program is ill-formed. Otherwise, an implementation should yield correct
values of `U` and `V`. If it is not possible to represent `X` or `Y`
with `intmax_t`, the program is ill-formed unless the implementation
yields correct values of `U` and `V`.

**Table: Expressions used to perform ratio arithmetic** <a id="tab:ratio.arithmetic">[tab:ratio.arithmetic]</a>

|                          |                       |                     |
| ------------------------ | --------------------- | ------------------- |
| `ratio_add<R1, R2>`      | `R1::num * R2::den +` | `R1::den * R2::den` |
|                          | `R2::num * R1::den`   |                     |
| `ratio_subtract<R1, R2>` | `R1::num * R2::den -` | `R1::den * R2::den` |
|                          | `R2::num * R1::den`   |                     |
| `ratio_multiply<R1, R2>` | `R1::num * R2::num`   | `R1::den * R2::den` |
| `ratio_divide<R1, R2>`   | `R1::num * R2::den`   | `R1::den * R2::num` |


``` cpp
static_assert(ratio_add<ratio<1,3>, ratio<1,6>>::num == 1, "1/3+1/6 == 1/2");
static_assert(ratio_add<ratio<1,3>, ratio<1,6>>::den == 2, "1/3+1/6 == 1/2");
static_assert(ratio_multiply<ratio<1,3>, ratio<3,2>>::num == 1, "1/3*3/2 == 1/2");
static_assert(ratio_multiply<ratio<1,3>, ratio<3,2>>::den == 2, "1/3*3/2 == 1/2");

  // The following cases may cause the program to be ill-formed under some implementations
static_assert(ratio_add<ratio<1,INT_MAX>, ratio<1,INT_MAX>>::num == 2,
  "1/MAX+1/MAX == 2/MAX");
static_assert(ratio_add<ratio<1,INT_MAX>, ratio<1,INT_MAX>>::den == INT_MAX,
  "1/MAX+1/MAX == 2/MAX");
static_assert(ratio_multiply<ratio<1,INT_MAX>, ratio<INT_MAX,2>>::num == 1,
  "1/MAX * MAX/2 == 1/2");
static_assert(ratio_multiply<ratio<1,INT_MAX>, ratio<INT_MAX,2>>::den == 2,
  "1/MAX * MAX/2 == 1/2");
```

### Comparison of `ratio`s <a id="ratio.comparison">[[ratio.comparison]]</a>

``` cpp
template <class R1, class R2> struct ratio_equal
  : integral_constant<bool, see below> { };
```

If `R1::num == R2::num` and `R1::den == R2::den`, `ratio_equal<R1, R2>`
shall be derived from  
`integral_constant<bool, true>`; otherwise it shall be derived from
`integral_constant<bool, false>`.

``` cpp
template <class R1, class R2> struct ratio_not_equal
  : integral_constant<bool, !ratio_equal<R1, R2>::value> { };
```

``` cpp
template <class R1, class R2> struct ratio_less
  : integral_constant<bool, see below> { };
```

If `R1::num * R2::den < R2::num * R1::den`, `ratio_less<R1, R2>` shall
be derived from `integral_constant<bool, true>`; otherwise it shall be
derived from `integral_constant<bool, false>`. Implementations may use
other algorithms to compute this relationship to avoid overflow. If
overflow occurs, the program is ill-formed.

``` cpp
template <class R1, class R2> struct ratio_less_equal
  : integral_constant<bool, !ratio_less<R2, R1>::value> { };
```

``` cpp
template <class R1, class R2> struct ratio_greater
  : integral_constant<bool, ratio_less<R2, R1>::value> { };
```

``` cpp
template <class R1, class R2> struct ratio_greater_equal
  : integral_constant<bool, !ratio_less<R1, R2>::value> { };
```

### SI types for `ratio` <a id="ratio.si">[[ratio.si]]</a>

For each of the typedefs `yocto`, `zepto`, `zetta`, and `yotta`, if both
of the constants used in its specification are representable by
`intmax_t`, the typedef shall be defined; if either of the constants is
not representable by `intmax_t`, the typedef shall not be defined.

## Time utilities <a id="time">[[time]]</a>

### In general <a id="time.general">[[time.general]]</a>

This subclause describes the chrono library ([[time.syn]]) and various
C functions ([[date.time]]) that provide generally useful time
utilities.

### Header `<chrono>` synopsis <a id="time.syn">[[time.syn]]</a>

``` cpp
namespace std {
namespace chrono {

// [time.duration], class template duration
template <class Rep, class Period = ratio<1> > class duration;

// [time.point], class template time_point
template <class Clock, class Duration = typename Clock::duration> class time_point;

}  // namespace chrono

// [time.traits.specializations] common_type specializations
template <class Rep1, class Period1, class Rep2, class Period2>
  struct common_type<chrono::duration<Rep1, Period1>, chrono::duration<Rep2, Period2>>;

template <class Clock, class Duration1, class Duration2>
  struct common_type<chrono::time_point<Clock, Duration1>, chrono::time_point<Clock, Duration2>>;

namespace chrono {

// [time.traits], customization traits
template <class Rep> struct treat_as_floating_point;
template <class Rep> struct duration_values;

// [time.duration.nonmember], duration arithmetic
template <class Rep1, class Period1, class Rep2, class Period2>
  common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  constexpr operator+(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Rep2, class Period2>
  common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  constexpr operator-(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period, class Rep2>
  duration<common_type_t<Rep1, Rep2>, Period>
  constexpr operator*(const duration<Rep1, Period>& d, const Rep2& s);
template <class Rep1, class Rep2, class Period>
  duration<common_type_t<Rep1, Rep2>, Period>
  constexpr operator*(const Rep1& s, const duration<Rep2, Period>& d);
template <class Rep1, class Period, class Rep2>
  duration<common_type_t<Rep1, Rep2>, Period>
  constexpr operator/(const duration<Rep1, Period>& d, const Rep2& s);
template <class Rep1, class Period1, class Rep2, class Period2>
  common_type_t<Rep1, Rep2>
  constexpr operator/(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period, class Rep2>
  duration<common_type_t<Rep1, Rep2>, Period>
  constexpr operator%(const duration<Rep1, Period>& d, const Rep2& s);
template <class Rep1, class Period1, class Rep2, class Period2>
  common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  constexpr operator%(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);

// [time.duration.comparisons], duration comparisons
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator==(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator!=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator< (const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator> (const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);

// [time.duration.cast], duration_cast
template <class ToDuration, class Rep, class Period>
  constexpr ToDuration duration_cast(const duration<Rep, Period>& d);

// convenience typedefs
typedef duration<signed integer type of at least 64 bits,        nano> nanoseconds;
typedef duration<signed integer type of at least 55 bits,       micro> microseconds;
typedef duration<signed integer type of at least 45 bits,       milli> milliseconds;
typedef duration<signed integer type of at least 35 bits             > seconds;
typedef duration<signed integer type of at least 29 bits, ratio<  60>> minutes;
typedef duration<signed integer type of at least 23 bits, ratio<3600>> hours;

// [time.point.nonmember], time_point arithmetic
template <class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
  operator+(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
template <class Rep1, class Period1, class Clock, class Duration2>
  constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
  operator+(const duration<Rep1, Period1>& lhs, const time_point<Clock, Duration2>& rhs);
template <class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
  operator-(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
template <class Clock, class Duration1, class Duration2>
  constexpr common_type_t<Duration1, Duration2>
  operator-(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);

// [time.point.comparisons] time_point comparisons
template <class Clock, class Duration1, class Duration2>
   constexpr bool operator==(const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);
template <class Clock, class Duration1, class Duration2>
   constexpr bool operator!=(const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);
template <class Clock, class Duration1, class Duration2>
   constexpr bool operator< (const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);
template <class Clock, class Duration1, class Duration2>
   constexpr bool operator<=(const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);
template <class Clock, class Duration1, class Duration2>
   constexpr bool operator> (const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);
template <class Clock, class Duration1, class Duration2>
   constexpr bool operator>=(const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);

// [time.point.cast], time_point_cast
template <class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration>
  time_point_cast(const time_point<Clock, Duration>& t);

// [time.clock], clocks
class system_clock;
class steady_clock;
class high_resolution_clock;

}  // namespace chrono

inline namespace literals {
inline namespace chrono_literals {

// ~[time.duration.literals], suffixes for duration literals
constexpr chrono::hours                                 operator "" h(unsigned long long);
constexpr chrono::duration<unspecified, ratio<3600,1>> operator "" h(long double);
constexpr chrono::minutes                               operator "" min(unsigned long long);
constexpr chrono::duration<unspecified, ratio<60,1>>   operator "" min(long double);
constexpr chrono::seconds                               operator "" s(unsigned long long);
constexpr chrono::duration<unspecified>                operator "" s(long double);
constexpr chrono::milliseconds                          operator "" ms(unsigned long long);
constexpr chrono::duration<unspecified, milli>         operator "" ms(long double);
constexpr chrono::microseconds                          operator "" us(unsigned long long);
constexpr chrono::duration<unspecified, micro>         operator "" us(long double);
constexpr chrono::nanoseconds                           operator "" ns(unsigned long long);
constexpr chrono::duration<unspecified, nano>          operator "" ns(long double);

}  // namespace chrono_literals
}  // namespace literals

namespace chrono {

using namespace literals::chrono_literals;

} // namespace chrono

}  // namespace std
```

### Clock requirements <a id="time.clock.req">[[time.clock.req]]</a>

A clock is a bundle consisting of a `duration`, a `time_point`, and a
function `now()` to get the current `time_point`. The origin of the
clock’s `time_point` is referred to as the clock’s *epoch*. A clock
shall meet the requirements in Table  [[tab:time.clock]].

In Table  [[tab:time.clock]] `C1` and `C2` denote clock types. `t1` and
`t2` are values returned by `C1::now()` where the call returning `t1`
happens before ([[intro.multithread]]) the call returning `t2` and both
of these calls occur before `C1::time_point::max()`. this means `C1` did
not wrap around between `t1` and `t2`.

The relative difference in durations between those reported by a given
clock and the SI definition is a measure of the quality of
implementation.

A type `TC` meets the `TrivialClock` requirements if:

- `TC` satisfies the `Clock` requirements ([[time.clock.req]]),
- the types `TC::rep`, `TC::duration`, and `TC::time_point` satisfy the
  requirements of `EqualityComparable` (Table [[equalitycomparable]]),
  `LessThanComparable` (Table [[lessthancomparable]]),
  `DefaultConstructible` (Table [[defaultconstructible]]),
  `CopyConstructible` (Table [[copyconstructible]]), `CopyAssignable`
  (Table [[copyassignable]]), `Destructible` (Table [[destructible]]),
  and the requirements of numeric types ([[numeric.requirements]]).
  this means, in particular, that operations on these types will not
  throw exceptions.
- lvalues of the types `TC::rep`, `TC::duration`, and `TC::time_point`
  are swappable ([[swappable.requirements]]),
- the function `TC::now()` does not throw exceptions, and
- the type `TC::time_point::clock` meets the `TrivialClock`
  requirements, recursively.

### Time-related traits <a id="time.traits">[[time.traits]]</a>

#### `treat_as_floating_point` <a id="time.traits.is_fp">[[time.traits.is_fp]]</a>

``` cpp
template <class Rep> struct treat_as_floating_point
  : is_floating_point<Rep> { };
```

The `duration` template uses the `treat_as_floating_point` trait to help
determine if a `duration` object can be converted to another `duration`
with a different tick `period`. If `treat_as_floating_point<Rep>::value`
is true, then implicit conversions are allowed among `duration`s.
Otherwise, the implicit convertibility depends on the tick `period`s of
the `duration`s. The intention of this trait is to indicate whether a
given class behaves like a floating-point type, and thus allows division
of one value by another with acceptable loss of precision. If
`treat_as_floating_point<Rep>::value` is `false`, `Rep` will be treated
as if it behaved like an integral type for the purpose of these
conversions.

#### `duration_values` <a id="time.traits.duration_values">[[time.traits.duration_values]]</a>

``` cpp
template <class Rep>
struct duration_values {
public:
  static constexpr Rep zero();
  static constexpr Rep min();
  static constexpr Rep max();
};
```

The `duration` template uses the `duration_values` trait to construct
special values of the durations representation (`Rep`). This is done
because the representation might be a class type with behavior which
requires some other implementation to return these special values. In
that case, the author of that class type should specialize
`duration_values` to return the indicated values.

``` cpp
static constexpr Rep zero();
```

*Returns:* `Rep(0)`. `Rep(0)` is specified instead of `Rep()` because
`Rep()` may have some other meaning, such as an uninitialized value.

The value returned shall be the additive identity.

``` cpp
static constexpr Rep min();
```

*Returns:* `numeric_limits<Rep>::lowest()`.

The value returned shall compare less than or equal to `zero()`.

``` cpp
static constexpr Rep max();
```

*Returns:* `numeric_limits<Rep>::max()`.

The value returned shall compare greater than `zero()`.

#### Specializations of `common_type` <a id="time.traits.specializations">[[time.traits.specializations]]</a>

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
struct common_type<chrono::duration<Rep1, Period1>, chrono::duration<Rep2, Period2>> {
  typedef chrono::duration<common_type_t<Rep1, Rep2>, see below> type;
};
```

The `period` of the `duration` indicated by this specialization of
`common_type` shall be the greatest common divisor of `Period1` and
`Period2`. This can be computed by forming a ratio of the greatest
common divisor of `Period1::num` and `Period2::num` and the least common
multiple of `Period1::den` and `Period2::den`.

The `typedef` name `type` is a synonym for the `duration` with the
largest tick `period` possible where both `duration` arguments will
convert to it without requiring a division operation. The representation
of this type is intended to be able to hold any value resulting from
this conversion with no truncation error, although floating-point
durations may have round-off errors.

``` cpp
template <class Clock, class Duration1, class Duration2>
struct common_type<chrono::time_point<Clock, Duration1>, chrono::time_point<Clock, Duration2>> {
  typedef chrono::time_point<Clock, common_type_t<Duration1, Duration2>> type;
};
```

The common type of two `time_point` types is a `time_point` with the
same clock as the two types and the common type of their two
`duration`s.

### Class template `duration` <a id="time.duration">[[time.duration]]</a>

A `duration` type measures time between two points in time
(`time_point`s). A `duration` has a representation which holds a count
of ticks and a tick period. The tick period is the amount of time which
occurs from one tick to the next, in units of seconds. It is expressed
as a rational constant using the template `ratio`.

``` cpp
template <class Rep, class Period = ratio<1>>
class duration {
public:
  typedef Rep    rep;
  typedef Period period;
private:
  rep rep_;  // exposition only
public:
  // [time.duration.cons], construct/copy/destroy:
  constexpr duration() = default;
  template <class Rep2>
      constexpr explicit duration(const Rep2& r);
  template <class Rep2, class Period2>
     constexpr duration(const duration<Rep2, Period2>& d);
  ~duration() = default;
  duration(const duration&) = default;
  duration& operator=(const duration&) = default;

  // [time.duration.observer], observer:
  constexpr rep count() const;

  // [time.duration.arithmetic], arithmetic:
  constexpr duration  operator+() const;
  constexpr duration  operator-() const;
  duration& operator++();
  duration  operator++(int);
  duration& operator--();
  duration  operator--(int);

  duration& operator+=(const duration& d);
  duration& operator-=(const duration& d);

  duration& operator*=(const rep& rhs);
  duration& operator/=(const rep& rhs);
  duration& operator%=(const rep& rhs);
  duration& operator%=(const duration& rhs);

  // [time.duration.special], special values:
  static constexpr duration zero();
  static constexpr duration min();
  static constexpr duration max();
};
```

*Requires:* `Rep` shall be an arithmetic type or a class emulating an
arithmetic type.

*Remarks:* If `duration` is instantiated with a `duration` type for the
template argument `Rep`, the program is ill-formed.

*Remarks:* If `Period` is not a specialization of `ratio`, the program
is ill-formed.

*Remarks:* If `Period::num` is not positive, the program is ill-formed.

*Requires:* Members of `duration` shall not throw exceptions other than
those thrown by the indicated operations on their representations.

*Remarks:* The defaulted copy constructor of duration shall be a
`constexpr` function if and only if the required initialization of the
member `rep_` for copy and move, respectively, would satisfy the
requirements for a `constexpr` function.

``` cpp
duration<long, ratio<60>> d0;       // holds a count of minutes using a long
duration<long long, milli> d1;      // holds a count of milliseconds using a long long
duration<double, ratio<1, 30>>  d2; // holds a count with a tick period of $\frac{1}{30}$ of a second
                                    // (30 Hz) using a double
```

#### `duration` constructors <a id="time.duration.cons">[[time.duration.cons]]</a>

``` cpp
template <class Rep2>
  constexpr explicit duration(const Rep2& r);
```

*Remarks:* This constructor shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `rep` and

- `treat_as_floating_point<rep>::value` is `true` or
- `treat_as_floating_point<Rep2>::value` is `false`.

``` cpp
duration<int, milli> d(3);          // OK
duration<int, milli> d(3.5);        // error
```

*Effects:* Constructs an object of type `duration`.

`count() == static_cast<rep>(r)`.

``` cpp
template <class Rep2, class Period2>
  constexpr duration(const duration<Rep2, Period2>& d);
```

*Remarks:* This constructor shall not participate in overload resolution
unless no overflow is induced in the conversion and
`treat_as_floating_point<rep>::value` is `true` or both
`ratio_divide<Period2, period>::den` is `1` and
`treat_as_floating_point<Rep2>::value` is `false`. This requirement
prevents implicit truncation error when converting between
integral-based `duration` types. Such a construction could easily lead
to confusion about the value of the `duration`.

``` cpp
duration<int, milli> ms(3);
duration<int, micro> us = ms;       // OK
duration<int, milli> ms2 = us;      // error
```

*Effects:* Constructs an object of type `duration`, constructing `rep_`
from  
`duration_cast<duration>(d).count()`.

#### `duration` observer <a id="time.duration.observer">[[time.duration.observer]]</a>

``` cpp
constexpr rep count() const;
```

*Returns:* `rep_`.

#### `duration` arithmetic <a id="time.duration.arithmetic">[[time.duration.arithmetic]]</a>

``` cpp
constexpr duration operator+() const;
```

*Returns:* `*this`.

``` cpp
constexpr duration operator-() const;
```

*Returns:* `duration(-rep_);`.

``` cpp
duration& operator++();
```

*Effects:* `++rep_`.

*Returns:* `*this`.

``` cpp
duration operator++(int);
```

*Returns:* `duration(rep_++);`.

``` cpp
duration& operator--();
```

*Effects:* `-``-``rep_`.

*Returns:* `*this`.

``` cpp
duration operator--(int);
```

*Returns:* `duration(rep_--);`.

``` cpp
duration& operator+=(const duration& d);
```

*Effects:* `rep_ += d.count()`.

*Returns:* `*this`.

``` cpp
duration& operator-=(const duration& d);
```

*Effects:* `rep_ -= d.count()`.

*Returns:* `*this`.

``` cpp
duration& operator*=(const rep& rhs);
```

*Effects:* `rep_ *= rhs`.

*Returns:* `*this`.

``` cpp
duration& operator/=(const rep& rhs);
```

*Effects:* `rep_ /= rhs`.

*Returns:* `*this`.

``` cpp
duration& operator%=(const rep& rhs);
```

*Effects:* `rep_ %= rhs`.

*Returns:* `*this`.

``` cpp
duration& operator%=(const duration& rhs);
```

*Effects:* `rep_ %= rhs.count()`.

*Returns:* `*this`.

#### `duration` special values <a id="time.duration.special">[[time.duration.special]]</a>

``` cpp
static constexpr duration zero();
```

*Returns:* `duration(duration_values<rep>::zero())`.

``` cpp
static constexpr duration min();
```

*Returns:* `duration(duration_values<rep>::min())`.

``` cpp
static constexpr duration max();
```

*Returns:* `duration(duration_values<rep>::max())`.

#### `duration` non-member arithmetic <a id="time.duration.nonmember">[[time.duration.nonmember]]</a>

In the function descriptions that follow, `CD` represents the return
type of the function. `CR(A,B)` represents `common_type_t<A, B>`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator+(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* CD(CD(lhs).count() + CD(rhs).count()).

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator-(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* CD(CD(lhs).count() - CD(rhs).count()).

``` cpp
template <class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator*(const duration<Rep1, Period>& d, const Rep2& s);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `CR(Rep1, Rep2)`.

*Returns:* CD(CD(d).count() \* s).

``` cpp
template <class Rep1, class Rep2, class Period>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator*(const Rep1& s, const duration<Rep2, Period>& d);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep1` is implicitly convertible to `CR(Rep1, Rep2)`.

*Returns:* `d * s`.

``` cpp
template <class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator/(const duration<Rep1, Period>& d, const Rep2& s);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `CR(Rep1, Rep2)` and `Rep2`
is not an instantiation of `duration`.

*Returns:* CD(CD(d).count() / s).

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<Rep1, Rep2>
  operator/(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(lhs).count() / CD(rhs).count()`.

``` cpp
template <class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator%(const duration<Rep1, Period>& d, const Rep2& s);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `CR(Rep1, Rep2)` and `Rep2`
is not an instantiation of `duration`.

*Returns:* CD(CD(d).count() % s).

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator%(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* CD(CD(lhs).count() % CD(rhs).count()).

#### `duration` comparisons <a id="time.duration.comparisons">[[time.duration.comparisons]]</a>

In the function descriptions that follow, `CT` represents
`common_type_t<A, B>`, where `A` and `B` are the types of the two
arguments to the function.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator==(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs).count() == CT(rhs).count()`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator!=(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs).count() < CT(rhs).count()`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<=(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>=(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(lhs < rhs)`.

#### `duration_cast` <a id="time.duration.cast">[[time.duration.cast]]</a>

``` cpp
template <class ToDuration, class Rep, class Period>
  constexpr ToDuration duration_cast(const duration<Rep, Period>& d);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is an instantiation of `duration`.

*Returns:* Let `CF` be
`ratio_divide<Period, typename ToDuration::period>`, and `CR` be
`common_type<` `typename ToDuration::rep, Rep, intmax_t>::type.`

- If `CF::num == 1` and `CF::den == 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(d.count()))
  ```
- otherwise, if `CF::num != 1` and `CF::den == 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) * static_cast<CR>(CF::num)))
  ```
- otherwise, if `CF::num == 1` and `CF::den != 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) / static_cast<CR>(CF::den)))
  ```
- otherwise, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) * static_cast<CR>(CF::num) / static_cast<CR>(CF::den)))
  ```

*Notes:* This function does not use any implicit conversions; all
conversions are done with `static_cast`. It avoids multiplications and
divisions when it is known at compile time that one or more arguments
is 1. Intermediate computations are carried out in the widest
representation and only converted to the destination representation at
the final step.

#### Suffixes for duration literals <a id="time.duration.literals">[[time.duration.literals]]</a>

This section describes literal suffixes for constructing duration
literals. The suffixes `h`, `min`, `s`, `ms`, `us`, `ns` denote duration
values of the corresponding types `hours`, `minutes`, `seconds`,
`milliseconds`, `microseconds`, and `nanoseconds` respectively if they
are applied to integral literals.

If any of these suffixes are applied to a floating point literal the
result is a `chrono::duration` literal with an unspecified floating
point representation.

If any of these suffixes are applied to an integer literal and the
resulting `chrono::duration` value cannot be represented in the result
type because of overflow, the program is ill-formed.

The following code shows some duration literals.

``` cpp
using namespace std::chrono_literals;
auto constexpr aday=24h;
auto constexpr lesson=45min;
auto constexpr halfanhour=0.5h;
```

``` cpp
constexpr chrono::hours                                 operator "" h(unsigned long long hours);
constexpr chrono::duration<unspecified, ratio<3600,1>> operator "" h(long double hours);
```

*Returns:* A `duration` literal representing `hours` hours.

``` cpp
constexpr chrono::minutes                             operator "" min(unsigned long long minutes);
constexpr chrono::duration<unspecified, ratio<60,1>> operator "" min(long double minutes);
```

*Returns:* A `duration` literal representing `minutes` minutes.

``` cpp
constexpr chrono::seconds                operator "" s(unsigned long long sec);
constexpr chrono::duration<unspecified> operator "" s(long double sec);
```

*Returns:* A `duration` literal representing `sec` seconds.

The same suffix `s` is used for `basic_string` but there is no conflict,
since duration suffixes apply to numbers and string literal suffixes
apply to character array literals.

``` cpp
constexpr chrono::milliseconds                  operator "" ms(unsigned long long msec);
constexpr chrono::duration<unspecified, milli> operator "" ms(long double msec);
```

*Returns:* A `duration` literal representing `msec` milliseconds.

``` cpp
constexpr chrono::microseconds                  operator "" us(unsigned long long usec);
constexpr chrono::duration<unspecified, micro> operator "" us(long double usec);
```

*Returns:* A `duration` literal representing `usec` microseconds.

``` cpp
constexpr chrono::nanoseconds                  operator "" ns(unsigned long long nsec);
constexpr chrono::duration<unspecified, nano> operator "" ns(long double nsec);
```

*Returns:* A `duration` literal representing `nsec` nanoseconds.

### Class template `time_point` <a id="time.point">[[time.point]]</a>

``` cpp
template <class Clock, class Duration = typename Clock::duration>
class time_point {
public:
  typedef Clock                     clock;
  typedef Duration                  duration;
  typedef typename duration::rep    rep;
  typedef typename duration::period period;
private:
  duration d_;  // exposition only

public:
  // [time.point.cons], construct:
  constexpr time_point();  // has value epoch
  constexpr explicit time_point(const duration& d);  // same as time_point() + d
  template <class Duration2>
    constexpr time_point(const time_point<clock, Duration2>& t);

  // [time.point.observer], observer:
  constexpr duration time_since_epoch() const;

  // [time.point.arithmetic], arithmetic:
  time_point& operator+=(const duration& d);
  time_point& operator-=(const duration& d);

  // [time.point.special], special values:
  static constexpr time_point min();
  static constexpr time_point max();
};
```

`Clock` shall meet the Clock requirements ([[time.clock]]).

If `Duration` is not an instance of `duration`, the program is
ill-formed.

#### `time_point` constructors <a id="time.point.cons">[[time.point.cons]]</a>

``` cpp
constexpr time_point();
```

*Effects:* Constructs an object of type `time_point`, initializing `d_`
with `duration::zero()`. Such a `time_point` object represents the
epoch.

``` cpp
constexpr explicit time_point(const duration& d);
```

*Effects:* Constructs an object of type `time_point`, initializing `d_`
with `d`. Such a `time_point` object represents the epoch `+ d`.

``` cpp
template <class Duration2>
  constexpr time_point(const time_point<clock, Duration2>& t);
```

*Remarks:* This constructor shall not participate in overload resolution
unless `Duration2` is implicitly convertible to `duration`.

*Effects:* Constructs an object of type `time_point`, initializing `d_`
with `t.time_since_epoch()`.

#### `time_point` observer <a id="time.point.observer">[[time.point.observer]]</a>

``` cpp
constexpr duration time_since_epoch() const;
```

*Returns:* `d_`.

#### `time_point` arithmetic <a id="time.point.arithmetic">[[time.point.arithmetic]]</a>

``` cpp
time_point& operator+=(const duration& d);
```

*Effects:* `d_ += d`.

*Returns:* `*this`.

``` cpp
time_point& operator-=(const duration& d);
```

*Effects:* `d_ -= d`.

*Returns:* `*this`.

#### `time_point` special values <a id="time.point.special">[[time.point.special]]</a>

``` cpp
static constexpr time_point min();
```

*Returns:* `time_point(duration::min())`.

``` cpp
static constexpr time_point max();
```

*Returns:* `time_point(duration::max())`.

#### `time_point` non-member arithmetic <a id="time.point.nonmember">[[time.point.nonmember]]</a>

``` cpp
template <class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
  operator+(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs.time_since_epoch() + rhs)`, where `CT` is the type of
the return value.

``` cpp
template <class Rep1, class Period1, class Clock, class Duration2>
  constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
  operator+(const duration<Rep1, Period1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `rhs + lhs`.

``` cpp
template <class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
  operator-(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `lhs + (-rhs)`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr common_type_t<Duration1, Duration2>
  operator-(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() - rhs.time_since_epoch()`.

#### `time_point` comparisons <a id="time.point.comparisons">[[time.point.comparisons]]</a>

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator==(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() == rhs.time_since_epoch()`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator!=(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator<(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() < rhs.time_since_epoch()`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator<=(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator>(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator>=(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(lhs < rhs)`.

#### `time_point_cast` <a id="time.point.cast">[[time.point.cast]]</a>

``` cpp
template <class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration>
  time_point_cast(const time_point<Clock, Duration>& t);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is an instantiation of `duration`.

*Returns:*
`time_point<Clock, ToDuration>(duration_cast<ToDuration>(t.time_since_epoch()))`.

### Clocks <a id="time.clock">[[time.clock]]</a>

The types defined in this subclause shall satisfy the `TrivialClock`
requirements ([[time.clock.req]]).

#### Class `system_clock` <a id="time.clock.system">[[time.clock.system]]</a>

Objects of class `system_clock` represent wall clock time from the
system-wide realtime clock.

``` cpp
class system_clock {
public:
  typedef see below                           rep;
  typedef ratio<unspecified, unspecified>   period;
  typedef chrono::duration<rep, period>       duration;
  typedef chrono::time_point<system_clock>    time_point;
  static constexpr bool is_steady =        unspecified;

  static time_point now() noexcept;

  // Map to C API
  static time_t      to_time_t  (const time_point& t) noexcept;
  static time_point  from_time_t(time_t t) noexcept;
};
```

``` cpp
typedef unspecified system_clock::rep;
```

*Requires:*
`system_clock::duration::min() < system_clock::duration::zero()` shall
be `true`. This implies that `rep` is a signed type.

``` cpp
static time_t to_time_t(const time_point& t) noexcept;
```

*Returns:* A `time_t` object that represents the same point in time as
`t` when both values are restricted to the coarser of the precisions of
`time_t` and `time_point`. It is implementation defined whether values
are rounded or truncated to the required precision.

``` cpp
static time_point from_time_t(time_t t) noexcept;
```

*Returns:* A `time_point` object that represents the same point in time
as `t` when both values are restricted to the coarser of the precisions
of `time_t` and `time_point`. It is implementation defined whether
values are rounded or truncated to the required precision.

#### Class `steady_clock` <a id="time.clock.steady">[[time.clock.steady]]</a>

Objects of class `steady_clock` represent clocks for which values of
`time_point` never decrease as physical time advances and for which
values of `time_point` advance at a steady rate relative to real time.
That is, the clock may not be adjusted.

``` cpp
class steady_clock {
public:
  typedef unspecified                               rep;
  typedef ratio<unspecified, unspecified>          period;
  typedef chrono::duration<rep, period>              duration;
  typedef chrono::time_point<unspecified, duration>  time_point;
  static constexpr bool is_steady =               true;

  static time_point now() noexcept;
};
```

#### Class `high_resolution_clock` <a id="time.clock.hires">[[time.clock.hires]]</a>

Objects of class `high_resolution_clock` represent clocks with the
shortest tick period. `high_resolution_clock` may be a synonym for
`system_clock` or `steady_clock`.

``` cpp
class high_resolution_clock {
public:
  typedef unspecified                               rep;
  typedef ratio<unspecified, unspecified>          period;
  typedef chrono::duration<rep, period>              duration;
  typedef chrono::time_point<unspecified, duration> time_point;
  static constexpr bool is_steady =               unspecified;

  static time_point now() noexcept;
};
```

### Date and time functions <a id="date.time">[[date.time]]</a>

Table  [[tab:util.hdr.ctime]] describes the header `<ctime>`.

The contents are the same as the Standard C library header
`<time.h>.`[^3] The functions `asctime`, `ctime`, `gmtime`, and
`localtime` are not required to avoid data races (
[[res.on.data.races]]).

ISO C Clause 7.12, Amendment 1 Clause 4.6.4.

## Class template `scoped_allocator_adaptor` <a id="allocator.adaptor">[[allocator.adaptor]]</a>

### Header `<scoped_allocator>` synopsis <a id="allocator.adaptor.syn">[[allocator.adaptor.syn]]</a>

``` cpp
// scoped allocator adaptor
  template <class OuterAlloc, class... InnerAlloc>
    class scoped_allocator_adaptor;
  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator!=(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

The class template `scoped_allocator_adaptor` is an allocator template
that specifies the memory resource (the outer allocator) to be used by a
container (as any other allocator does) and also specifies an inner
allocator resource to be passed to the constructor of every element
within the container. This adaptor is instantiated with one outer and
zero or more inner allocator types. If instantiated with only one
allocator type, the inner allocator becomes the
`scoped_allocator_adaptor` itself, thus using the same allocator
resource for the container and every element within the container and,
if the elements themselves are containers, each of their elements
recursively. If instantiated with more than one allocator, the first
allocator is the outer allocator for use by the container, the second
allocator is passed to the constructors of the container’s elements,
and, if the elements themselves are containers, the third allocator is
passed to the elements’ elements, and so on. If containers are nested to
a depth greater than the number of allocators, the last allocator is
used repeatedly, as in the single-allocator case, for any remaining
recursions. The `scoped_allocator_adaptor` is derived from the outer
allocator type so it can be substituted for the outer allocator type in
most expressions.

``` cpp
namespace std {
  template <class OuterAlloc, class... InnerAllocs>
    class scoped_allocator_adaptor : public OuterAlloc {
  private:
    typedef allocator_traits<OuterAlloc> OuterTraits; // exposition only
    scoped_allocator_adaptor<InnerAllocs...> inner;   // exposition only
  public:
    typedef OuterAlloc outer_allocator_type;
    typedef see below inner_allocator_type;

    typedef typename OuterTraits::value_type value_type;
    typedef typename OuterTraits::size_type size_type;
    typedef typename OuterTraits::difference_type difference_type;
    typedef typename OuterTraits::pointer pointer;
    typedef typename OuterTraits::const_pointer const_pointer;
    typedef typename OuterTraits::void_pointer void_pointer;
    typedef typename OuterTraits::const_void_pointer const_void_pointer;

    typedef see below propagate_on_container_copy_assignment;
    typedef see below propagate_on_container_move_assignment;
    typedef see below propagate_on_container_swap;

    template <class Tp>
      struct rebind {
        typedef scoped_allocator_adaptor<
          OuterTraits::template rebind_alloc<Tp>, InnerAllocs...> other;
      };

    scoped_allocator_adaptor();
    template <class OuterA2>
      scoped_allocator_adaptor(OuterA2&& outerAlloc,
                               const InnerAllocs&... innerAllocs) noexcept;

    scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
    scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;

    template <class OuterA2>
      scoped_allocator_adaptor(
        const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& other) noexcept;
    template <class OuterA2>
      scoped_allocator_adaptor(
        scoped_allocator_adaptor<OuterA2, InnerAllocs...>&& other) noexcept;

    ~scoped_allocator_adaptor();

    inner_allocator_type& inner_allocator() noexcept;
    const inner_allocator_type& inner_allocator() const noexcept;
    outer_allocator_type& outer_allocator() noexcept;
    const outer_allocator_type& outer_allocator() const noexcept;

    pointer allocate(size_type n);
    pointer allocate(size_type n, const_void_pointer hint);
    void deallocate(pointer p, size_type n);
    size_type max_size() const;

    template <class T, class... Args>
      void construct(T* p, Args&&... args);
    template <class T1, class T2, class... Args1, class... Args2>
      void construct(pair<T1, T2>* p, piecewise_construct_t,
                     tuple<Args1...> x, tuple<Args2...> y);
    template <class T1, class T2>
      void construct(pair<T1, T2>* p);
    template <class T1, class T2, class U, class V>
      void construct(pair<T1, T2>* p, U&& x, V&& y);
    template <class T1, class T2, class U, class V>
      void construct(pair<T1, T2>* p, const pair<U, V>& x);
    template <class T1, class T2, class U, class V>
      void construct(pair<T1, T2>* p, pair<U, V>&& x);

    template <class T>
      void destroy(T* p);

    scoped_allocator_adaptor select_on_container_copy_construction() const;
  };

  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator!=(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
}
```

### Scoped allocator adaptor member types <a id="allocator.adaptor.types">[[allocator.adaptor.types]]</a>

``` cpp
typedef see below inner_allocator_type;
```

*Type:* `scoped_allocator_adaptor<OuterAlloc>` if
`sizeof...(InnerAllocs)` is zero; otherwise,  
`scoped_allocator_adaptor<InnerAllocs...>`.

``` cpp
typedef see below propagate_on_container_copy_assignment;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_copy_assignment::value` is
`true` for any `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

``` cpp
typedef see below propagate_on_container_move_assignment;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_move_assignment::value` is
`true` for any `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

``` cpp
typedef see below propagate_on_container_swap;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_swap::value` is `true` for
any `A` in the set of `OuterAlloc` and `InnerAllocs...`; otherwise,
`false_type`.

### Scoped allocator adaptor constructors <a id="allocator.adaptor.cnstr">[[allocator.adaptor.cnstr]]</a>

``` cpp
scoped_allocator_adaptor();
```

*Effects:* value-initializes the `OuterAlloc` base class and the `inner`
allocator object.

``` cpp
template <class OuterA2>
  scoped_allocator_adaptor(OuterA2&& outerAlloc,
                           const InnerAllocs&... innerAllocs) noexcept;
```

*Requires:* `OuterAlloc` shall be constructible from `OuterA2`.

*Effects:* initializes the `OuterAlloc` base class with
`std::forward<OuterA2>(outerAlloc)` and `inner` with `innerAllocs...`
(hence recursively initializing each allocator within the adaptor with
the corresponding allocator from the argument list).

``` cpp
scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
```

*Effects:* initializes each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;
```

*Effects:* move constructs each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
template <class OuterA2>
  scoped_allocator_adaptor(const scoped_allocator_adaptor<OuterA2,
                                                          InnerAllocs...>& other) noexcept;
```

*Requires:* `OuterAlloc` shall be constructible from `OuterA2`.

*Effects:* initializes each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
template <class OuterA2>
  scoped_allocator_adaptor(scoped_allocator_adaptor<OuterA2,
                                                    InnerAllocs...>&& other) noexcept;
```

*Requires:* `OuterAlloc` shall be constructible from `OuterA2`.

*Effects:* initializes each allocator within the adaptor with the
corresponding allocator rvalue from `other`.

### Scoped allocator adaptor members <a id="allocator.adaptor.members">[[allocator.adaptor.members]]</a>

In the `construct` member functions, *OUTERMOST(x)* is `x` if `x` does
not have an `outer_allocator()` member function and  
*OUTERMOST(x.outer_allocator())* otherwise; *OUTERMOST_ALLOC_TRAITS(x)*
is  
`allocator_traits<decltype(OUTERMOST(x))>`. *OUTERMOST*(x) and  
*OUTERMOST_ALLOC_TRAITS*(x) are recursive operations. It is incumbent
upon the definition of `outer_allocator()` to ensure that the recursion
terminates. It will terminate for all instantiations of  
`scoped_allocator_adaptor`.

``` cpp
inner_allocator_type& inner_allocator() noexcept;
const inner_allocator_type& inner_allocator() const noexcept;
```

*Returns:* `*this` if `sizeof...(InnerAllocs)` is zero; otherwise,
`inner`.

``` cpp
outer_allocator_type& outer_allocator() noexcept;
```

*Returns:* `static_cast<OuterAlloc&>(*this)`.

``` cpp
const outer_allocator_type& outer_allocator() const noexcept;
```

*Returns:* `static_cast<const OuterAlloc&>(*this)`.

``` cpp
pointer allocate(size_type n);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n)`.

``` cpp
pointer allocate(size_type n, const_void_pointer hint);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n, hint)`.

``` cpp
void deallocate(pointer p, size_type n) noexcept;
```

*Effects:*
`allocator_traits<OuterAlloc>::deallocate(outer_allocator(), p, n)`;

``` cpp
size_type max_size() const;
```

*Returns:* `allocator_traits<OuterAlloc>::max_size(outer_allocator())`.

``` cpp
template <class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Effects:*

- If `uses_allocator<T, inner_allocator_type>::value` is `false` and
  `is_constructible<T, Args...>::value` is `true`, calls
  *OUTERMOST_ALLOC_TRAITS*(`*this`)`::construct(`  
  *`OUTERMOST`*`(*this), p, std::forward<Args>(args)...)`.
- Otherwise, if `uses_allocator<T, inner_allocator_type>::value` is
  `true` and
  `is_constructible<T, allocator_arg_t, inner_allocator_type, Args...>::value`
  is `true`, calls
  *OUTERMOST_ALLOC_TRAITS*(`*this`)`::construct(`*`OUTERMOST`*`(*this), p, allocator_arg,`  
  `inner_allocator(), std::forward<Args>(args)...)`.
- Otherwise, if `uses_allocator<T, inner_allocator_type>::value` is
  `true` and `is_constructible<T, Args..., inner_allocator_type>::value`
  is `true`, calls *OUTERMOST_ALLOC_TRAITS*(\*this)::
  `construct(`*`OUTERMOST`*`(*this), p, std::forward<Args>(args)...,`  
  `inner_allocator())`.
- Otherwise, the program is ill-formed. An error will result if
  `uses_allocator` evaluates to true but the specific constructor does
  not take an allocator. This definition prevents a silent failure to
  pass an inner allocator to a contained element.

``` cpp
template <class T1, class T2, class... Args1, class... Args2>
  void construct(pair<T1, T2>* p,piecewise_construct_t,
                 tuple<Args1...> x, tuple<Args2...> y);
```

*Requires:* all of the types in `Args1` and `Args2` shall be
`CopyConstructible` (Table  [[copyconstructible]]).

*Effects:* Constructs a `tuple` object `xprime` from `x` by the
following rules:

- If `uses_allocator<T1, inner_allocator_type>::value` is `false` and
  `is_constructible<T1, Args1...>::value` is `true`, then `xprime` is
  `x`.
- Otherwise, if `uses_allocator<T1, inner_allocator_type>::value` is
  `true` and
  `is_constructible<T1, allocator_arg_t, inner_allocator_type, Args1...>::value`
  is `true`, then `xprime` is
  `tuple_cat(tuple<allocator_arg_t, inner_allocator_type&>( allocator_arg, inner_allocator()), std::move(x))`.
- Otherwise, if `uses_allocator<T1, inner_allocator_type>::value` is
  `true` and
  `is_constructible<T1, Args1..., inner_allocator_type>::value` is
  `true`, then `xprime` is
  `tuple_cat(std::move(x), tuple<inner_allocator_type&>(inner_allocator()))`.
- Otherwise, the program is ill-formed.

and constructs a `tuple` object `yprime` from `y` by the following
rules:

- If `uses_allocator<T2, inner_allocator_type>::value` is `false` and
  `is_constructible<T2, Args2...>::value` is `true`, then `yprime` is
  `y`.
- Otherwise, if `uses_allocator<T2, inner_allocator_type>::value` is
  `true` and
  `is_constructible<T2, allocator_arg_t, inner_allocator_type, Args2...>::value`
  is `true`, then `yprime` is
  `tuple_cat(tuple<allocator_arg_t, inner_allocator_type&>( allocator_arg, inner_allocator()), std::move(y))`.
- Otherwise, if `uses_allocator<T2, inner_allocator_type>::value` is
  `true` and
  `is_constructible<T2, Args2..., inner_allocator_type>::value` is
  `true`, then `yprime` is
  `tuple_cat(std::move(y), tuple<inner_allocator_type&>(inner_allocator()))`.
- Otherwise, the program is ill-formed.

then calls
*`OUTERMOST_ALLOC_TRAITS`*`(*this)::construct(`*`OUTERMOST`*`(*this), p,`  
`piecewise_construct, std::move(xprime), std::move(yprime))`.

``` cpp
template <class T1, class T2>
  void construct(pair<T1, T2>* p);
```

*Effects:* Equivalent to
`this->construct(p, piecewise_construct, tuple<>(), tuple<>())`.

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1, T2>* p, U&& x, V&& y);
```

*Effects:* Equivalent to
`this->construct(p, piecewise_construct, forward_as_tuple(std::forward<U>(x)), forward_as_tuple(std::forward<V>(y)))`.

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1, T2>* p, const pair<U, V>& x);
```

*Effects:* Equivalent to
`this->construct(p, piecewise_construct, forward_as_tuple(x.first), forward_as_tuple(x.second))`.

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1, T2>* p, pair<U, V>&& x);
```

*Effects:* Equivalent to
`this->construct(p, piecewise_construct, forward_as_tuple(std::forward<U>(x.first)), forward_as_tuple(std::forward<V>(x.second)))`.

``` cpp
template <class T>
  void destroy(T* p);
```

*Effects:* calls
*`OUTERMOST_ALLOC_TRAITS`*`(*this)::destroy(`*`OUTERMOST`*`(*this), p)`.

``` cpp
scoped_allocator_adaptor select_on_container_copy_construction() const;
```

*Returns:* A new scoped_allocator_adaptor object where each allocator
`A` in the adaptor is initialized from the result of calling
`allocator_traits<A>::select_on_container_copy_construction()` on the
corresponding allocator in `*this`.

### Scoped allocator operators <a id="scoped.adaptor.operators">[[scoped.adaptor.operators]]</a>

``` cpp
template <class OuterA1, class OuterA2, class... InnerAllocs>
  bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                  const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

*Returns:* `a.outer_allocator() == b.outer_allocator()` if
`sizeof...(InnerAllocs)` is zero; otherwise,
`a.outer_allocator() == b.outer_allocator()` `&&`
`a.inner_allocator() == b.inner_allocator()`.

``` cpp
template <class OuterA1, class OuterA2, class... InnerAllocs>
  bool operator!=(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                  const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

*Returns:* `!(a == b)`.

## Class `type_index` <a id="type.index">[[type.index]]</a>

### Header `<typeindex>` synopsis <a id="type.index.synopsis">[[type.index.synopsis]]</a>

``` cpp
namespace std {
  class type_index;
  template <class T> struct hash;
  template<> struct hash<type_index>;
}
```

### `type_index` overview <a id="type.index.overview">[[type.index.overview]]</a>

``` cpp
namespace std {
  class type_index {
  public:
    type_index(const type_info& rhs) noexcept;
    bool operator==(const type_index& rhs) const noexcept;
    bool operator!=(const type_index& rhs) const noexcept;
    bool operator< (const type_index& rhs) const noexcept;
    bool operator<= (const type_index& rhs) const noexcept;
    bool operator> (const type_index& rhs) const noexcept;
    bool operator>= (const type_index& rhs) const noexcept;
    size_t hash_code() const noexcept;
    const char* name() const noexcept;
  private:
    const type_info* target;    // exposition only
    // Note that the use of a pointer here, rather than a reference,
    // means that the default copy/move constructor and assignment
    // operators will be provided and work as expected.
  };
}
```

The class `type_index` provides a simple wrapper for `type_info` which
can be used as an index type in associative containers (
[[associative]]) and in unordered associative containers ([[unord]]).

### `type_index` members <a id="type.index.members">[[type.index.members]]</a>

``` cpp
type_index(const type_info& rhs) noexcept;
```

*Effects:* constructs a `type_index` object, the equivalent of
`target = &rhs`.

``` cpp
bool operator==(const type_index& rhs) const noexcept;
```

*Returns:* `*target == *rhs.target`

``` cpp
bool operator!=(const type_index& rhs) const noexcept;
```

*Returns:* `*target != *rhs.target`

``` cpp
bool operator<(const type_index& rhs) const noexcept;
```

*Returns:* `target->before(*rhs.target)`

``` cpp
bool operator<=(const type_index& rhs) const noexcept;
```

*Returns:* `!rhs.target->before(*target)`

``` cpp
bool operator>(const type_index& rhs) const noexcept;
```

*Returns:* `rhs.target->before(*target)`

``` cpp
bool operator>=(const type_index& rhs) const noexcept;
```

*Returns:* `!target->before(*rhs.target)`

``` cpp
size_t hash_code() const noexcept;
```

*Returns:* `target->hash_code()`

``` cpp
const char* name() const noexcept;
```

*Returns:* `target->name()`

### Hash support <a id="type.index.hash">[[type.index.hash]]</a>

``` cpp
template <> struct hash<type_index>;
```

The template specialization shall meet the requirements of class
template `hash` ([[unord.hash]]). For an object `index` of type
`type_index`, `hash<type_index>()(index)` shall evaluate to the same
result as `index.hash_code()`.

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[algorithms]: algorithms.md#algorithms
[allocator.adaptor]: #allocator.adaptor
[allocator.adaptor.cnstr]: #allocator.adaptor.cnstr
[allocator.adaptor.members]: #allocator.adaptor.members
[allocator.adaptor.syn]: #allocator.adaptor.syn
[allocator.adaptor.types]: #allocator.adaptor.types
[allocator.globals]: #allocator.globals
[allocator.members]: #allocator.members
[allocator.requirements]: library.md#allocator.requirements
[allocator.tag]: #allocator.tag
[allocator.traits]: #allocator.traits
[allocator.traits.members]: #allocator.traits.members
[allocator.traits.types]: #allocator.traits.types
[allocator.uses]: #allocator.uses
[allocator.uses.construction]: #allocator.uses.construction
[allocator.uses.trait]: #allocator.uses.trait
[arithmetic.operations]: #arithmetic.operations
[array]: containers.md#array
[associative]: containers.md#associative
[atomics.order]: atomics.md#atomics.order
[atomics.types.operations]: atomics.md#atomics.types.operations
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[bitset.cons]: #bitset.cons
[bitset.hash]: #bitset.hash
[bitset.members]: #bitset.members
[bitset.operators]: #bitset.operators
[bitwise.operations]: #bitwise.operations
[c.malloc]: #c.malloc
[c.strings]: strings.md#c.strings
[class]: class.md#class
[class.abstract]: class.md#class.abstract
[class.derived]: class.md#class.derived
[class.dtor]: special.md#class.dtor
[class.virtual]: class.md#class.virtual
[comparisons]: #comparisons
[conv.array]: conv.md#conv.array
[conv.func]: conv.md#conv.func
[conv.lval]: conv.md#conv.lval
[conv.rank]: conv.md#conv.rank
[copyassignable]: #copyassignable
[copyconstructible]: #copyconstructible
[date.time]: #date.time
[dcl.array]: dcl.md#dcl.array
[dcl.enum]: dcl.md#dcl.enum
[dcl.ref]: dcl.md#dcl.ref
[declval]: #declval
[default.allocator]: #default.allocator
[defaultconstructible]: #defaultconstructible
[destructible]: #destructible
[equalitycomparable]: #equalitycomparable
[expr]: expr.md#expr
[expr.add]: expr.md#expr.add
[expr.alignof]: expr.md#expr.alignof
[expr.bit.and]: expr.md#expr.bit.and
[expr.call]: expr.md#expr.call
[expr.eq]: expr.md#expr.eq
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.mul]: expr.md#expr.mul
[expr.or]: expr.md#expr.or
[expr.rel]: expr.md#expr.rel
[expr.unary.noexcept]: expr.md#expr.unary.noexcept
[expr.unary.op]: expr.md#expr.unary.op
[expr.xor]: expr.md#expr.xor
[forward]: #forward
[forward.iterators]: iterators.md#forward.iterators
[func.bind]: #func.bind
[func.bind.bind]: #func.bind.bind
[func.bind.isbind]: #func.bind.isbind
[func.bind.isplace]: #func.bind.isplace
[func.bind.place]: #func.bind.place
[func.def]: #func.def
[func.memfn]: #func.memfn
[func.require]: #func.require
[func.wrap]: #func.wrap
[func.wrap.badcall]: #func.wrap.badcall
[func.wrap.badcall.const]: #func.wrap.badcall.const
[func.wrap.func]: #func.wrap.func
[func.wrap.func.alg]: #func.wrap.func.alg
[func.wrap.func.cap]: #func.wrap.func.cap
[func.wrap.func.con]: #func.wrap.func.con
[func.wrap.func.inv]: #func.wrap.func.inv
[func.wrap.func.mod]: #func.wrap.func.mod
[func.wrap.func.nullptr]: #func.wrap.func.nullptr
[func.wrap.func.targ]: #func.wrap.func.targ
[function.objects]: #function.objects
[hash.requirements]: library.md#hash.requirements
[input.iterators]: iterators.md#input.iterators
[intro.multithread]: intro.md#intro.multithread
[intseq]: #intseq
[intseq.general]: #intseq.general
[intseq.intseq]: #intseq.intseq
[intseq.make]: #intseq.make
[invalid.argument]: diagnostics.md#invalid.argument
[iostate.flags]: input.md#iostate.flags
[istream.formatted]: input.md#istream.formatted
[lessthancomparable]: #lessthancomparable
[logical.operations]: #logical.operations
[memory]: #memory
[memory.general]: #memory.general
[memory.syn]: #memory.syn
[meta]: #meta
[meta.help]: #meta.help
[meta.rel]: #meta.rel
[meta.rqmts]: #meta.rqmts
[meta.trans]: #meta.trans
[meta.trans.arr]: #meta.trans.arr
[meta.trans.cv]: #meta.trans.cv
[meta.trans.other]: #meta.trans.other
[meta.trans.ptr]: #meta.trans.ptr
[meta.trans.ref]: #meta.trans.ref
[meta.trans.sign]: #meta.trans.sign
[meta.type.synop]: #meta.type.synop
[meta.unary]: #meta.unary
[meta.unary.cat]: #meta.unary.cat
[meta.unary.comp]: #meta.unary.comp
[meta.unary.prop]: #meta.unary.prop
[meta.unary.prop.query]: #meta.unary.prop.query
[moveassignable]: #moveassignable
[moveconstructible]: #moveconstructible
[negators]: #negators
[new.delete]: language.md#new.delete
[nullablepointer.requirements]: library.md#nullablepointer.requirements
[numeric.requirements]: numerics.md#numeric.requirements
[operators]: #operators
[ostream.formatted]: input.md#ostream.formatted
[out.of.range]: diagnostics.md#out.of.range
[output.iterators]: iterators.md#output.iterators
[over.match.call]: over.md#over.match.call
[overflow.error]: diagnostics.md#overflow.error
[pair.astuple]: #pair.astuple
[pair.piecewise]: #pair.piecewise
[pairs]: #pairs
[pairs.general]: #pairs.general
[pairs.pair]: #pairs.pair
[pairs.spec]: #pairs.spec
[pointer.traits]: #pointer.traits
[pointer.traits.functions]: #pointer.traits.functions
[pointer.traits.types]: #pointer.traits.types
[ptr.align]: #ptr.align
[ratio]: #ratio
[ratio.arithmetic]: #ratio.arithmetic
[ratio.comparison]: #ratio.comparison
[ratio.general]: #ratio.general
[ratio.ratio]: #ratio.ratio
[ratio.si]: #ratio.si
[ratio.syn]: #ratio.syn
[refwrap]: #refwrap
[refwrap.access]: #refwrap.access
[refwrap.assign]: #refwrap.assign
[refwrap.const]: #refwrap.const
[refwrap.helpers]: #refwrap.helpers
[refwrap.invoke]: #refwrap.invoke
[res.on.data.races]: library.md#res.on.data.races
[scoped.adaptor.operators]: #scoped.adaptor.operators
[smartptr]: #smartptr
[special]: special.md#special
[specialized.addressof]: #specialized.addressof
[specialized.algorithms]: #specialized.algorithms
[stmt.dcl]: stmt.md#stmt.dcl
[storage.iterator]: #storage.iterator
[support.dynamic]: language.md#support.dynamic
[swappable.requirements]: library.md#swappable.requirements
[tab:ratio.arithmetic]: #tab:ratio.arithmetic
[tab:time.clock]: #tab:time.clock
[tab:util.hdr.cstdlib]: #tab:util.hdr.cstdlib
[tab:util.hdr.cstring]: #tab:util.hdr.cstring
[tab:util.hdr.ctime]: #tab:util.hdr.ctime
[tab:util.lib.summary]: #tab:util.lib.summary
[template.bitset]: #template.bitset
[temporary.buffer]: #temporary.buffer
[time]: #time
[time.clock]: #time.clock
[time.clock.hires]: #time.clock.hires
[time.clock.req]: #time.clock.req
[time.clock.steady]: #time.clock.steady
[time.clock.system]: #time.clock.system
[time.duration]: #time.duration
[time.duration.arithmetic]: #time.duration.arithmetic
[time.duration.cast]: #time.duration.cast
[time.duration.comparisons]: #time.duration.comparisons
[time.duration.cons]: #time.duration.cons
[time.duration.literals]: #time.duration.literals
[time.duration.nonmember]: #time.duration.nonmember
[time.duration.observer]: #time.duration.observer
[time.duration.special]: #time.duration.special
[time.general]: #time.general
[time.point]: #time.point
[time.point.arithmetic]: #time.point.arithmetic
[time.point.cast]: #time.point.cast
[time.point.comparisons]: #time.point.comparisons
[time.point.cons]: #time.point.cons
[time.point.nonmember]: #time.point.nonmember
[time.point.observer]: #time.point.observer
[time.point.special]: #time.point.special
[time.syn]: #time.syn
[time.traits]: #time.traits
[time.traits.duration_values]: #time.traits.duration_values
[time.traits.is_fp]: #time.traits.is_fp
[time.traits.specializations]: #time.traits.specializations
[tuple]: #tuple
[tuple.assign]: #tuple.assign
[tuple.cnstr]: #tuple.cnstr
[tuple.creation]: #tuple.creation
[tuple.elem]: #tuple.elem
[tuple.general]: #tuple.general
[tuple.helper]: #tuple.helper
[tuple.rel]: #tuple.rel
[tuple.special]: #tuple.special
[tuple.swap]: #tuple.swap
[tuple.traits]: #tuple.traits
[tuple.tuple]: #tuple.tuple
[type.index]: #type.index
[type.index.hash]: #type.index.hash
[type.index.members]: #type.index.members
[type.index.overview]: #type.index.overview
[type.index.synopsis]: #type.index.synopsis
[uninitialized.copy]: #uninitialized.copy
[uninitialized.fill]: #uninitialized.fill
[uninitialized.fill.n]: #uninitialized.fill.n
[unique.ptr]: #unique.ptr
[unique.ptr.create]: #unique.ptr.create
[unique.ptr.dltr]: #unique.ptr.dltr
[unique.ptr.dltr.dflt]: #unique.ptr.dltr.dflt
[unique.ptr.dltr.dflt1]: #unique.ptr.dltr.dflt1
[unique.ptr.dltr.general]: #unique.ptr.dltr.general
[unique.ptr.runtime]: #unique.ptr.runtime
[unique.ptr.runtime.ctor]: #unique.ptr.runtime.ctor
[unique.ptr.runtime.modifiers]: #unique.ptr.runtime.modifiers
[unique.ptr.runtime.observers]: #unique.ptr.runtime.observers
[unique.ptr.single]: #unique.ptr.single
[unique.ptr.single.asgn]: #unique.ptr.single.asgn
[unique.ptr.single.ctor]: #unique.ptr.single.ctor
[unique.ptr.single.dtor]: #unique.ptr.single.dtor
[unique.ptr.single.modifiers]: #unique.ptr.single.modifiers
[unique.ptr.single.observers]: #unique.ptr.single.observers
[unique.ptr.special]: #unique.ptr.special
[unord]: containers.md#unord
[unord.hash]: #unord.hash
[util.dynamic.safety]: #util.dynamic.safety
[util.smartptr]: #util.smartptr
[util.smartptr.enab]: #util.smartptr.enab
[util.smartptr.getdeleter]: #util.smartptr.getdeleter
[util.smartptr.hash]: #util.smartptr.hash
[util.smartptr.ownerless]: #util.smartptr.ownerless
[util.smartptr.shared]: #util.smartptr.shared
[util.smartptr.shared.assign]: #util.smartptr.shared.assign
[util.smartptr.shared.atomic]: #util.smartptr.shared.atomic
[util.smartptr.shared.cast]: #util.smartptr.shared.cast
[util.smartptr.shared.cmp]: #util.smartptr.shared.cmp
[util.smartptr.shared.const]: #util.smartptr.shared.const
[util.smartptr.shared.create]: #util.smartptr.shared.create
[util.smartptr.shared.dest]: #util.smartptr.shared.dest
[util.smartptr.shared.io]: #util.smartptr.shared.io
[util.smartptr.shared.mod]: #util.smartptr.shared.mod
[util.smartptr.shared.obs]: #util.smartptr.shared.obs
[util.smartptr.shared.spec]: #util.smartptr.shared.spec
[util.smartptr.weak]: #util.smartptr.weak
[util.smartptr.weak.assign]: #util.smartptr.weak.assign
[util.smartptr.weak.const]: #util.smartptr.weak.const
[util.smartptr.weak.dest]: #util.smartptr.weak.dest
[util.smartptr.weak.mod]: #util.smartptr.weak.mod
[util.smartptr.weak.obs]: #util.smartptr.weak.obs
[util.smartptr.weak.spec]: #util.smartptr.weak.spec
[util.smartptr.weakptr]: #util.smartptr.weakptr
[utilities]: #utilities
[utilities.general]: #utilities.general
[utility]: #utility
[utility.exchange]: #utility.exchange
[utility.swap]: #utility.swap

[^1]: `pointer_safety::preferred` might be returned to indicate that a
    leak detector is running so that the program can avoid spurious leak
    reports.

[^2]: Such a type is a function pointer or a class type which has a
    member `operator()` or a class type which has a conversion to a
    pointer to function.

[^3]: `strftime` supports the C conversion specifiers `C`, `D`, `e`,
    `F`, `g`, `G`, `h`, `r`, `R`, `t`, `T`, `u`, `V`, and `z`, and the
    modifiers `E` and `O`.
