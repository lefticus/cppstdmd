# Iterators library <a id="iterators">[[iterators]]</a>

## General <a id="iterators.general">[[iterators.general]]</a>

This Clause describes components that C++ programs may use to perform
iterations over containers [[containers]], streams [[iostream.format]],
stream buffers [[stream.buffers]], and other ranges [[ranges]].

The following subclauses describe iterator requirements, and components
for iterator primitives, predefined iterators, and stream iterators, as
summarized in [[iterators.summary]].

**Table: Iterators library summary**

| Subclause                 |                       | Header       |
| ------------------------- | --------------------- | ------------ |
| [[iterator.requirements]] | Iterator requirements | `<iterator>` |
| [[iterator.primitives]]   | Iterator primitives   |              |
| [[predef.iterators]]      | Iterator adaptors     |              |
| [[stream.iterators]]      | Stream iterators      |              |
| [[iterator.range]]        | Range access          |              |


## Header `<iterator>` synopsis <a id="iterator.synopsis">[[iterator.synopsis]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <concepts>             // see [concepts.syn]

namespace std {
  template<class T> using with-reference = T&;  // exposition only
  template<class T> concept can-reference       // exposition only
    = requires { typename with-reference<T>; };
  template<class T> concept dereferenceable     // exposition only
    = requires(T& t) {
      { *t } -> can-reference;  // not required to be equality-preserving
    };

  // [iterator.assoc.types], associated types
  // [incrementable.traits], incrementable traits
  template<class> struct incrementable_traits;
  template<class T>
    using iter_difference_t = see below;

  // [readable.traits], indirectly readable traits
  template<class> struct indirectly_readable_traits;
  template<class T>
    using iter_value_t = see below;

  // [iterator.traits], iterator traits
  template<class I> struct iterator_traits;
  template<class T> requires is_object_v<T> struct iterator_traits<T*>;

  template<dereferenceable T>
    using iter_reference_t = decltype(*declval<T&>());

  namespace ranges {
    // [iterator.cust], customization points
    inline namespace unspecified {
      // [iterator.cust.move], ranges::iter_move
      inline constexpr unspecified iter_move = unspecified;

      // [iterator.cust.swap], ranges::iter_swap
      inline constexpr unspecified iter_swap = unspecified;
    }
  }

  template<dereferenceable T>
    requires requires(T& t) {
      { ranges::iter_move(t) } -> can-reference;
    }
  using iter_rvalue_reference_t
    = decltype(ranges::iter_move(declval<T&>()));

  // [iterator.concepts], iterator concepts
  // [iterator.concept.readable], concept indirectly_readable
  template<class In>
    concept indirectly_readable = see below;

  template<indirectly_readable T>
    using iter_common_reference_t =
      common_reference_t<iter_reference_t<T>, iter_value_t<T>&>;

  // [iterator.concept.writable], concept indirectly_writable
  template<class Out, class T>
    concept indirectly_writable = see below;

  // [iterator.concept.winc], concept weakly_incrementable
  template<class I>
    concept weakly_incrementable = see below;

  // [iterator.concept.inc], concept incrementable
  template<class I>
    concept incrementable = see below;

  // [iterator.concept.iterator], concept input_or_output_iterator
  template<class I>
    concept input_or_output_iterator = see below;

  // [iterator.concept.sentinel], concept sentinel_for
  template<class S, class I>
    concept sentinel_for = see below;

  // [iterator.concept.sizedsentinel], concept sized_sentinel_for
  template<class S, class I>
    inline constexpr bool disable_sized_sentinel_for = false;

  template<class S, class I>
    concept sized_sentinel_for = see below;

  // [iterator.concept.input], concept input_iterator
  template<class I>
    concept input_iterator = see below;

  // [iterator.concept.output], concept output_iterator
  template<class I, class T>
    concept output_iterator = see below;

  // [iterator.concept.forward], concept forward_iterator
  template<class I>
    concept forward_iterator = see below;

  // [iterator.concept.bidir], concept bidirectional_iterator
  template<class I>
    concept bidirectional_iterator = see below;

  // [iterator.concept.random.access], concept random_access_iterator
  template<class I>
    concept random_access_iterator = see below;

  // [iterator.concept.contiguous], concept contiguous_iterator
  template<class I>
    concept contiguous_iterator = see below;

  // [indirectcallable], indirect callable requirements
  // [indirectcallable.indirectinvocable], indirect callables
  template<class F, class I>
    concept indirectly_unary_invocable = see below;

  template<class F, class I>
    concept indirectly_regular_unary_invocable = see below;

  template<class F, class I>
    concept indirect_unary_predicate = see below;

  template<class F, class I1, class I2>
    concept indirect_binary_predicate = see below;

  template<class F, class I1, class I2 = I1>
    concept indirect_equivalence_relation = see below;

  template<class F, class I1, class I2 = I1>
    concept indirect_strict_weak_order = see below;

  template<class F, class... Is>
    requires (indirectly_readable<Is> && ...) && invocable<F, iter_reference_t<Is>...>
      using indirect_result_t = invoke_result_t<F, iter_reference_t<Is>...>;

  // [projected], projected
  template<indirectly_readable I, indirectly_regular_unary_invocable<I> Proj>
    struct projected;

  template<weakly_incrementable I, class Proj>
    struct incrementable_traits<projected<I, Proj>>;

  // [alg.req], common algorithm requirements
  // [alg.req.ind.move], concept indirectly_movable
  template<class In, class Out>
    concept indirectly_movable = see below;

  template<class In, class Out>
    concept indirectly_movable_storable = see below;

  // [alg.req.ind.copy], concept indirectly_copyable
  template<class In, class Out>
    concept indirectly_copyable = see below;

  template<class In, class Out>
    concept indirectly_copyable_storable = see below;

  // [alg.req.ind.swap], concept indirectly_swappable
  template<class I1, class I2 = I1>
    concept indirectly_swappable = see below;

  // [alg.req.ind.cmp], concept indirectly_comparable
  template<class I1, class I2, class R, class P1 = identity, class P2 = identity>
    concept indirectly_comparable = see below;

  // [alg.req.permutable], concept permutable
  template<class I>
    concept permutable = see below;

  // [alg.req.mergeable], concept mergeable
  template<class I1, class I2, class Out,
      class R = ranges::less, class P1 = identity, class P2 = identity>
    concept mergeable = see below;

  // [alg.req.sortable], concept sortable
  template<class I, class R = ranges::less, class P = identity>
    concept sortable = see below;

  // [iterator.primitives], primitives
  // [std.iterator.tags], iterator tags
  struct input_iterator_tag { };
  struct output_iterator_tag { };
  struct forward_iterator_tag: public input_iterator_tag { };
  struct bidirectional_iterator_tag: public forward_iterator_tag { };
  struct random_access_iterator_tag: public bidirectional_iterator_tag { };
  struct contiguous_iterator_tag: public random_access_iterator_tag { };

  // [iterator.operations], iterator operations
  template<class InputIterator, class Distance>
    constexpr void
      advance(InputIterator& i, Distance n);
  template<class InputIterator>
    constexpr typename iterator_traits<InputIterator>::difference_type
      distance(InputIterator first, InputIterator last);
  template<class InputIterator>
    constexpr InputIterator
      next(InputIterator x,
           typename iterator_traits<InputIterator>::difference_type n = 1);
  template<class BidirectionalIterator>
    constexpr BidirectionalIterator
      prev(BidirectionalIterator x,
           typename iterator_traits<BidirectionalIterator>::difference_type n = 1);

  // [range.iter.ops], range iterator operations
  namespace ranges {
    // [range.iter.op.advance], ranges::advance
    template<input_or_output_iterator I>
      constexpr void advance(I& i, iter_difference_t<I> n);
    template<input_or_output_iterator I, sentinel_for<I> S>
      constexpr void advance(I& i, S bound);
    template<input_or_output_iterator I, sentinel_for<I> S>
      constexpr iter_difference_t<I> advance(I& i, iter_difference_t<I> n, S bound);

    // [range.iter.op.distance], ranges::distance
    template<input_or_output_iterator I, sentinel_for<I> S>
      constexpr iter_difference_t<I> distance(I first, S last);
    template<range R>
      constexpr range_difference_t<R> distance(R&& r);

    // [range.iter.op.next], ranges::next
    template<input_or_output_iterator I>
      constexpr I next(I x);
    template<input_or_output_iterator I>
      constexpr I next(I x, iter_difference_t<I> n);
    template<input_or_output_iterator I, sentinel_for<I> S>
      constexpr I next(I x, S bound);
    template<input_or_output_iterator I, sentinel_for<I> S>
      constexpr I next(I x, iter_difference_t<I> n, S bound);

    // [range.iter.op.prev], ranges::prev
    template<bidirectional_iterator I>
      constexpr I prev(I x);
    template<bidirectional_iterator I>
      constexpr I prev(I x, iter_difference_t<I> n);
    template<bidirectional_iterator I>
      constexpr I prev(I x, iter_difference_t<I> n, I bound);
  }

  // [predef.iterators], predefined iterators and sentinels
  // [reverse.iterators], reverse iterators
  template<class Iterator> class reverse_iterator;

  template<class Iterator1, class Iterator2>
    constexpr bool operator==(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator!=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator<(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator>(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator<=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator>=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template<class Iterator1, three_way_comparable_with<Iterator1> Iterator2>
    constexpr compare_three_way_result_t<Iterator1, Iterator2>
      operator<=>(const reverse_iterator<Iterator1>& x,
                  const reverse_iterator<Iterator2>& y);

  template<class Iterator1, class Iterator2>
    constexpr auto operator-(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y) -> decltype(y.base() - x.base());
  template<class Iterator>
    constexpr reverse_iterator<Iterator>
      operator+(
    typename reverse_iterator<Iterator>::difference_type n,
    const reverse_iterator<Iterator>& x);

  template<class Iterator>
    constexpr reverse_iterator<Iterator> make_reverse_iterator(Iterator i);

  template<class Iterator1, class Iterator2>
      requires (!sized_sentinel_for<Iterator1, Iterator2>)
    inline constexpr bool disable_sized_sentinel_for<reverse_iterator<Iterator1>,
                                                     reverse_iterator<Iterator2>> = true;

  // [insert.iterators], insert iterators
  template<class Container> class back_insert_iterator;
  template<class Container>
    constexpr back_insert_iterator<Container> back_inserter(Container& x);

  template<class Container> class front_insert_iterator;
  template<class Container>
    constexpr front_insert_iterator<Container> front_inserter(Container& x);

  template<class Container> class insert_iterator;
  template<class Container>
    constexpr insert_iterator<Container>
      inserter(Container& x, ranges::iterator_t<Container> i);

  // [move.iterators], move iterators and sentinels
  template<class Iterator> class move_iterator;

  template<class Iterator1, class Iterator2>
    constexpr bool operator==(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator<(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator>(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator<=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template<class Iterator1, class Iterator2>
    constexpr bool operator>=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template<class Iterator1, three_way_comparable_with<Iterator1> Iterator2>
    constexpr compare_three_way_result_t<Iterator1, Iterator2>
      operator<=>(const move_iterator<Iterator1>& x,
                  const move_iterator<Iterator2>& y);

  template<class Iterator1, class Iterator2>
    constexpr auto operator-(
    const move_iterator<Iterator1>& x,
    const move_iterator<Iterator2>& y) -> decltype(x.base() - y.base());
  template<class Iterator>
    constexpr move_iterator<Iterator> operator+(
      typename move_iterator<Iterator>::difference_type n, const move_iterator<Iterator>& x);

  template<class Iterator>
    constexpr move_iterator<Iterator> make_move_iterator(Iterator i);

  template<semiregular S> class move_sentinel;

  // [iterators.common], common iterators
  template<input_or_output_iterator I, sentinel_for<I> S>
    requires (!same_as<I, S> && copyable<I>)
      class common_iterator;

  template<class I, class S>
    struct incrementable_traits<common_iterator<I, S>>;

  template<input_iterator I, class S>
    struct iterator_traits<common_iterator<I, S>>;

  // [default.sentinels], default sentinels
  struct default_sentinel_t;
  inline constexpr default_sentinel_t default_sentinel{};

  // [iterators.counted], counted iterators
  template<input_or_output_iterator I> class counted_iterator;

  template<class I>
    struct incrementable_traits<counted_iterator<I>>;

  template<input_iterator I>
    struct iterator_traits<counted_iterator<I>>;

  // [unreachable.sentinels], unreachable sentinels
  struct unreachable_sentinel_t;
  inline constexpr unreachable_sentinel_t unreachable_sentinel{};

  // [stream.iterators], stream iterators
  template<class T, class charT = char, class traits = char_traits<charT>,
           class Distance = ptrdiff_t>
  class istream_iterator;
  template<class T, class charT, class traits, class Distance>
    bool operator==(const istream_iterator<T,charT,traits,Distance>& x,
            const istream_iterator<T,charT,traits,Distance>& y);

  template<class T, class charT = char, class traits = char_traits<charT>>
      class ostream_iterator;

  template<class charT, class traits = char_traits<charT>>
    class istreambuf_iterator;
  template<class charT, class traits>
    bool operator==(const istreambuf_iterator<charT,traits>& a,
            const istreambuf_iterator<charT,traits>& b);

  template<class charT, class traits = char_traits<charT>>
    class ostreambuf_iterator;

  // [iterator.range], range access
  template<class C> constexpr auto begin(C& c) -> decltype(c.begin());
  template<class C> constexpr auto begin(const C& c) -> decltype(c.begin());
  template<class C> constexpr auto end(C& c) -> decltype(c.end());
  template<class C> constexpr auto end(const C& c) -> decltype(c.end());
  template<class T, size_t N> constexpr T* begin(T (&array)[N]) noexcept;
  template<class T, size_t N> constexpr T* end(T (&array)[N]) noexcept;
  template<class C> constexpr auto cbegin(const C& c) noexcept(noexcept(std::begin(c)))
    -> decltype(std::begin(c));
  template<class C> constexpr auto cend(const C& c) noexcept(noexcept(std::end(c)))
    -> decltype(std::end(c));
  template<class C> constexpr auto rbegin(C& c) -> decltype(c.rbegin());
  template<class C> constexpr auto rbegin(const C& c) -> decltype(c.rbegin());
  template<class C> constexpr auto rend(C& c) -> decltype(c.rend());
  template<class C> constexpr auto rend(const C& c) -> decltype(c.rend());
  template<class T, size_t N> constexpr reverse_iterator<T*> rbegin(T (&array)[N]);
  template<class T, size_t N> constexpr reverse_iterator<T*> rend(T (&array)[N]);
  template<class E> constexpr reverse_iterator<const E*> rbegin(initializer_list<E> il);
  template<class E> constexpr reverse_iterator<const E*> rend(initializer_list<E> il);
  template<class C> constexpr auto crbegin(const C& c) -> decltype(std::rbegin(c));
  template<class C> constexpr auto crend(const C& c) -> decltype(std::rend(c));

  template<class C> constexpr auto size(const C& c) -> decltype(c.size());
  template<class T, size_t N> constexpr size_t size(const T (&array)[N]) noexcept;
  template<class C> constexpr auto ssize(const C& c)
    -> common_type_t<ptrdiff_t, make_signed_t<decltype(c.size())>>;
  template<class T, ptrdiff_t N> constexpr ptrdiff_t ssize(const T (&array)[N]) noexcept;
  template<class C> [[nodiscard]] constexpr auto empty(const C& c) -> decltype(c.empty());
  template<class T, size_t N> [[nodiscard]] constexpr bool empty(const T (&array)[N]) noexcept;
  template<class E> [[nodiscard]] constexpr bool empty(initializer_list<E> il) noexcept;
  template<class C> constexpr auto data(C& c) -> decltype(c.data());
  template<class C> constexpr auto data(const C& c) -> decltype(c.data());
  template<class T, size_t N> constexpr T* data(T (&array)[N]) noexcept;
  template<class E> constexpr const E* data(initializer_list<E> il) noexcept;
}
```

## Iterator requirements <a id="iterator.requirements">[[iterator.requirements]]</a>

### In general <a id="iterator.requirements.general">[[iterator.requirements.general]]</a>

Iterators are a generalization of pointers that allow a C++ program to
work with different data structures (for example, containers and ranges)
in a uniform manner. To be able to construct template algorithms that
work correctly and efficiently on different types of data structures,
the library formalizes not just the interfaces but also the semantics
and complexity assumptions of iterators. An input iterator `i` supports
the expression `*i`, resulting in a value of some object type `T`,
called the *value type* of the iterator. An output iterator `i` has a
non-empty set of types that are `indirectly_writable` to the iterator;
for each such type `T`, the expression `*i = o` is valid where `o` is a
value of type `T`. For every iterator type `X`, there is a corresponding
signed integer-like type [[iterator.concept.winc]] called the
*difference type* of the iterator.

Since iterators are an abstraction of pointers, their semantics are a
generalization of most of the semantics of pointers in C++. This ensures
that every function template that takes iterators works as well with
regular pointers. This document defines six categories of iterators,
according to the operations defined on them: *input iterators*, *output
iterators*, *forward iterators*, *bidirectional iterators*, *random
access iterators*, and *contiguous iterators*, as shown in
[[iterators.relations]].

**Table: Relations among iterator categories**

|                |                                 |                                 |                           |                          |
| -------------- | ------------------------------- | ------------------------------- | ------------------------- | ------------------------ |
| **Contiguous** | $\rightarrow$ **Random Access** | $\rightarrow$ **Bidirectional** | $\rightarrow$ **Forward** | $\rightarrow$ **Input**  |
|                |                                 |                                 |                           | $\rightarrow$ **Output** |


The six categories of iterators correspond to the iterator concepts

- `input_iterator` [[iterator.concept.input]],
- `output_iterator` [[iterator.concept.output]],
- `forward_iterator` [[iterator.concept.forward]],
- `bidirectional_iterator` [[iterator.concept.bidir]]
- `random_access_iterator` [[iterator.concept.random.access]], and
- `contiguous_iterator` [[iterator.concept.contiguous]],

respectively. The generic term *iterator* refers to any type that models
the `input_or_output_iterator` concept [[iterator.concept.iterator]].

Forward iterators meet all the requirements of input iterators and can
be used whenever an input iterator is specified; Bidirectional iterators
also meet all the requirements of forward iterators and can be used
whenever a forward iterator is specified; Random access iterators also
meet all the requirements of bidirectional iterators and can be used
whenever a bidirectional iterator is specified; Contiguous iterators
also meet all the requirements of random access iterators and can be
used whenever a random access iterator is specified.

Iterators that further meet the requirements of output iterators are
called *mutable iterators*. Nonmutable iterators are referred to as
*constant iterators*.

In addition to the requirements in this subclause, the nested
*typedef-name*s specified in [[iterator.traits]] shall be provided for
the iterator type.

[*Note 1*: Either the iterator type must provide the *typedef-name*s
directly (in which case `iterator_traits` pick them up automatically),
or an `iterator_traits` specialization must provide them. — *end note*]

Just as a regular pointer to an array guarantees that there is a pointer
value pointing past the last element of the array, so for any iterator
type there is an iterator value that points past the last element of a
corresponding sequence. Such a value is called a *past-the-end value*.
Values of an iterator `i` for which the expression `*i` is defined are
called *dereferenceable*. The library never assumes that past-the-end
values are dereferenceable. Iterators can also have singular values that
are not associated with any sequence.

[*Example 1*: After the declaration of an uninitialized pointer `x` (as
with `int* x;`), `x` must always be assumed to have a singular value of
a pointer. — *end example*]

Results of most expressions are undefined for singular values; the only
exceptions are destroying an iterator that holds a singular value, the
assignment of a non-singular value to an iterator that holds a singular
value, and, for iterators that meet the *Cpp17DefaultConstructible*
requirements, using a value-initialized iterator as the source of a copy
or move operation.

[*Note 2*: This guarantee is not offered for default-initialization,
although the distinction only matters for types with trivial default
constructors such as pointers or aggregates holding
pointers. — *end note*]

In these cases the singular value is overwritten the same way as any
other value. Dereferenceable values are always non-singular.

Most of the library’s algorithmic templates that operate on data
structures have interfaces that use ranges. A *range* is an iterator and
a *sentinel* that designate the beginning and end of the computation, or
an iterator and a count that designate the beginning and the number of
elements to which the computation is to be applied.[^1]

An iterator and a sentinel denoting a range are comparable. A range
\[`i`, `s`) is empty if `i == s`; otherwise, \[`i`, `s`) refers to the
elements in the data structure starting with the element pointed to by
`i` and up to but not including the element, if any, pointed to by the
first iterator `j` such that `j == s`.

A sentinel `s` is called *reachable from* an iterator `i` if and only if
there is a finite sequence of applications of the expression `++i` that
makes `i == s`. If `s` is reachable from `i`, \[`i`, `s`) denotes a
valid range.

A *counted range* `i`+\[0, `n`) is empty if `n == 0`; otherwise,
`i`+\[0, `n`) refers to the `n` elements in the data structure starting
with the element pointed to by `i` and up to but not including the
element, if any, pointed to by the result of `n` applications of `++i`.
A counted range `i`+\[0, `n`) is valid if and only if `n == 0`; or `n`
is positive, `i` is dereferenceable, and `++i`+\[0, `-``-``n`) is valid.

The result of the application of library functions to invalid ranges is
undefined.

All the categories of iterators require only those functions that are
realizable for a given category in constant time (amortized). Therefore,
requirement tables and concept definitions for the iterators do not
specify complexity.

Destruction of a non-forward iterator may invalidate pointers and
references previously obtained from that iterator.

An *invalid iterator* is an iterator that may be singular.[^2]

Iterators are called *constexpr iterators* if all operations provided to
meet iterator category requirements are constexpr functions.

[*Note 3*: For example, the types “pointer to `int`” and
`reverse_iterator<int*>` are constexpr iterators. — *end note*]

### Associated types <a id="iterator.assoc.types">[[iterator.assoc.types]]</a>

#### Incrementable traits <a id="incrementable.traits">[[incrementable.traits]]</a>

To implement algorithms only in terms of incrementable types, it is
often necessary to determine the difference type that corresponds to a
particular incrementable type. Accordingly, it is required that if `WI`
is the name of a type that models the `weakly_incrementable` concept
[[iterator.concept.winc]], the type

``` cpp
iter_difference_t<WI>
```

be defined as the incrementable type’s difference type.

``` cpp
namespace std {
  template<class> struct incrementable_traits { };

  template<class T>
    requires is_object_v<T>
  struct incrementable_traits<T*> {
    using difference_type = ptrdiff_t;
  };

  template<class I>
  struct incrementable_traits<const I>
    : incrementable_traits<I> { };

  template<class T>
    requires requires { typename T::difference_type; }
  struct incrementable_traits<T> {
    using difference_type = typename T::difference_type;
  };

  template<class T>
    requires (!requires { typename T::difference_type; } &&
              requires(const T& a, const T& b) { { a - b } -> integral; })
  struct incrementable_traits<T> {
    using difference_type = make_signed_t<decltype(declval<T>() - declval<T>())>;
  };

  template<class T>
    using iter_difference_t = see below;
}
```

Let R_`I` be `remove_cvref_t<I>`. The type `iter_difference_t<I>`
denotes

- `incrementable_traits<R_\tcode{I}>::difference_type` if
  `iterator_traits<R_\tcode{I}>` names a specialization generated from
  the primary template, and
- `iterator_traits<R_\tcode{I}>::difference_type` otherwise.

Users may specialize `incrementable_traits` on program-defined types.

#### Indirectly readable traits <a id="readable.traits">[[readable.traits]]</a>

To implement algorithms only in terms of indirectly readable types, it
is often necessary to determine the value type that corresponds to a
particular indirectly readable type. Accordingly, it is required that if
`R` is the name of a type that models the `indirectly_readable` concept
[[iterator.concept.readable]], the type

``` cpp
iter_value_t<R>
```

be defined as the indirectly readable type’s value type.

``` cpp
template<class> struct cond-value-type { };     // exposition only
template<class T>
  requires is_object_v<T>
struct cond-value-type<T> {
  using value_type = remove_cv_t<T>;
};

template<class> struct indirectly_readable_traits { };

template<class T>
struct indirectly_readable_traits<T*>
  : cond-value-type<T> { };

template<class I>
  requires is_array_v<I>
struct indirectly_readable_traits<I> {
  using value_type = remove_cv_t<remove_extent_t<I>>;
};

template<class I>
struct indirectly_readable_traits<const I>
  : indirectly_readable_traits<I> { };

template<class T>
  requires requires { typename T::value_type; }
struct indirectly_readable_traits<T>
  : cond-value-type<typename T::value_type> { };

template<class T>
  requires requires { typename T::element_type; }
struct indirectly_readable_traits<T>
  : cond-value-type<typename T::element_type> { };

template<class T> using iter_value_t = see below;
```

Let R_`I` be `remove_cvref_t<I>`. The type `iter_value_t<I>` denotes

- `indirectly_readable_traits<R_\tcode{I}>::value_type` if
  `iterator_traits<R_\tcode{I}>` names a specialization generated from
  the primary template, and
- `iterator_traits<R_\tcode{I}>::value_type` otherwise.

Class template `indirectly_readable_traits` may be specialized on
program-defined types.

[*Note 1*: Some legacy output iterators define a nested type named
`value_type` that is an alias for `void`. These types are not
`indirectly_readable` and have no associated value types. — *end note*]

[*Note 2*: Smart pointers like `shared_ptr<int>` are
`indirectly_readable` and have an associated value type, but a smart
pointer like `shared_ptr<void>` is not `indirectly_readable` and has no
associated value type. — *end note*]

#### Iterator traits <a id="iterator.traits">[[iterator.traits]]</a>

To implement algorithms only in terms of iterators, it is sometimes
necessary to determine the iterator category that corresponds to a
particular iterator type. Accordingly, it is required that if `I` is the
type of an iterator, the type

``` cpp
iterator_traits<I>::iterator_category
```

be defined as the iterator’s iterator category. In addition, the types

``` cpp
iterator_traits<I>::pointer
iterator_traits<I>::reference
```

shall be defined as the iterator’s pointer and reference types; that is,
for an iterator object `a` of class type, the same type as
`decltype(a.operator->())` and `decltype(*a)`, respectively. The type
`iterator_traits<I>::pointer` shall be `void` for an iterator of class
type `I` that does not support `operator->`. Additionally, in the case
of an output iterator, the types

``` cpp
iterator_traits<I>::value_type
iterator_traits<I>::difference_type
iterator_traits<I>::reference
```

may be defined as `void`.

The definitions in this subclause make use of the following
exposition-only concepts:

``` cpp
template<class I>
concept cpp17-iterator =
  copyable<I> && requires(I i) {
    {   *i } -> can-reference;
    {  ++i } -> same_as<I&>;
    { *i++ } -> can-reference;
  };

template<class I>
concept cpp17-input-iterator =
  cpp17-iterator<I> && equality_comparable<I> && requires(I i) {
    typename incrementable_traits<I>::difference_type;
    typename indirectly_readable_traits<I>::value_type;
    typename common_reference_t<iter_reference_t<I>&&,
                                typename indirectly_readable_traits<I>::value_type&>;
    typename common_reference_t<decltype(*i++)&&,
                                typename indirectly_readable_traits<I>::value_type&>;
    requires signed_integral<typename incrementable_traits<I>::difference_type>;
  };

template<class I>
concept cpp17-forward-iterator =
  cpp17-input-iterator<I> && constructible_from<I> &&
  is_lvalue_reference_v<iter_reference_t<I>> &&
  same_as<remove_cvref_t<iter_reference_t<I>>,
          typename indirectly_readable_traits<I>::value_type> &&
  requires(I i) {
    {  i++ } -> convertible_to<const I&>;
    { *i++ } -> same_as<iter_reference_t<I>>;
  };

template<class I>
concept cpp17-bidirectional-iterator =
  cpp17-forward-iterator<I> && requires(I i) {
    {  --i } -> same_as<I&>;
    {  i-- } -> convertible_to<const I&>;
    { *i-- } -> same_as<iter_reference_t<I>>;
  };

template<class I>
concept cpp17-random-access-iterator =
  cpp17-bidirectional-iterator<I> && totally_ordered<I> &&
  requires(I i, typename incrementable_traits<I>::difference_type n) {
    { i += n } -> same_as<I&>;
    { i -= n } -> same_as<I&>;
    { i +  n } -> same_as<I>;
    { n +  i } -> same_as<I>;
    { i -  n } -> same_as<I>;
    { i -  i } -> same_as<decltype(n)>;
    {  i[n]  } -> convertible_to<iter_reference_t<I>>;
  };
```

The members of a specialization `iterator_traits<I>` generated from the
`iterator_traits` primary template are computed as follows:

- If `I` has valid [[temp.deduct]] member types `difference_type`,
  `value_type`, `reference`, and `iterator_category`, then
  `iterator_traits<I>` has the following publicly accessible members:
  ``` cpp
  using iterator_category = typename I::iterator_category;
  using value_type        = typename I::value_type;
  using difference_type   = typename I::difference_type;
  using pointer           = see below;
  using reference         = typename I::reference;
  ```

  If the *qualified-id* `I::pointer` is valid and denotes a type, then
  `iterator_traits<I>::pointer` names that type; otherwise, it names
  `void`.
- Otherwise, if `I` satisfies the exposition-only concept
  `cpp17-input-iterator`, `iterator_traits<I>` has the following
  publicly accessible members:
  ``` cpp
  using iterator_category = see below;
  using value_type        = typename indirectly_readable_traits<I>::value_type;
  using difference_type   = typename incrementable_traits<I>::difference_type;
  using pointer           = see below;
  using reference         = see below;
  ```

  - If the *qualified-id* `I::pointer` is valid and denotes a type,
    `pointer` names that type. Otherwise, if
    `decltype({}declval<I&>().operator->())` is well-formed, then
    `pointer` names that type. Otherwise, `pointer` names `void`.
  - If the *qualified-id* `I::reference` is valid and denotes a type,
    `reference` names that type. Otherwise, `reference` names
    `iter_reference_t<I>`.
  - If the *qualified-id* `I::iterator_category` is valid and denotes a
    type, `iterator_category` names that type. Otherwise,
    `iterator_category` names:
    - `random_access_iterator_tag` if `I` satisfies
      `cpp17-random-access-iterator`, or otherwise
    - `bidirectional_iterator_tag` if `I` satisfies
      `cpp17-bidirectional-iterator`, or otherwise
    - `forward_iterator_tag` if `I` satisfies `cpp17-forward-iterator`,
      or otherwise
    - `input_iterator_tag`.
- Otherwise, if `I` satisfies the exposition-only concept
  `cpp17-iterator`, then `iterator_traits<I>` has the following publicly
  accessible members:
  ``` cpp
  using iterator_category = output_iterator_tag;
  using value_type        = void;
  using difference_type   = see below;
  using pointer           = void;
  using reference         = void;
  ```

  If the *qualified-id* `incrementable_traits<I>::difference_type` is
  valid and denotes a type, then `difference_type` names that type;
  otherwise, it names `void`.
- Otherwise, `iterator_traits<I>` has no members by any of the above
  names.

Explicit or partial specializations of `iterator_traits` may have a
member type `iterator_concept` that is used to indicate conformance to
the iterator concepts [[iterator.concepts]].

`iterator_traits` is specialized for pointers as

``` cpp
namespace std {
  template<class T>
    requires is_object_v<T>
  struct iterator_traits<T*> {
    using iterator_concept  = contiguous_iterator_tag;
    using iterator_category = random_access_iterator_tag;
    using value_type        = remove_cv_t<T>;
    using difference_type   = ptrdiff_t;
    using pointer           = T*;
    using reference         = T&;
  };
}
```

[*Example 1*:

To implement a generic `reverse` function, a C++ program can do the
following:

``` cpp
template<class BI>
void reverse(BI first, BI last) {
  typename iterator_traits<BI>::difference_type n =
    distance(first, last);
  --n;
  while(n > 0) {
    typename iterator_traits<BI>::value_type
     tmp = *first;
    *first++ = *--last;
    *last = tmp;
    n -= 2;
  }
}
```

— *end example*]

### Customization points <a id="iterator.cust">[[iterator.cust]]</a>

#### `ranges::iter_move` <a id="iterator.cust.move">[[iterator.cust.move]]</a>

The name `ranges::iter_move` denotes a customization point object
[[customization.point.object]]. The expression `ranges::iter_move(E)`
for a subexpression `E` is expression-equivalent to:

- `iter_move(E)`, if `E` has class or enumeration type and
  `iter_move(E)` is a well-formed expression when treated as an
  unevaluated operand, with overload resolution performed in a context
  that does not include a declaration of `ranges::iter_move` but does
  include the declaration
  ``` cpp
  void iter_move();
  ```
- Otherwise, if the expression `*E` is well-formed:
  - if `*E` is an lvalue, `std::move(*E)`;
  - otherwise, `*E`.
- Otherwise, `ranges::iter_move(E)` is ill-formed. \[*Note 1*: This case
  can result in substitution failure when `ranges::iter_move(E)` appears
  in the immediate context of a template instantiation. — *end note*]

If `ranges::iter_move(E)` is not equal to `*E`, the program is
ill-formed, no diagnostic required.

#### `ranges::iter_swap` <a id="iterator.cust.swap">[[iterator.cust.swap]]</a>

The name `ranges::iter_swap` denotes a customization point object
[[customization.point.object]] that exchanges the values
[[concept.swappable]] denoted by its arguments.

Let *iter-exchange-move* be the exposition-only function:

``` cpp
template<class X, class Y>
  constexpr iter_value_t<X> iter-exchange-move(X&& x, Y&& y)
    noexcept(noexcept(iter_value_t<X>(iter_move(x))) &&
             noexcept(*x = iter_move(y)));
```

*Effects:* Equivalent to:

``` cpp
iter_value_t<X> old_value(iter_move(x));
*x = iter_move(y);
return old_value;
```

The expression `ranges::iter_swap(E1, E2)` for subexpressions `E1` and
`E2` is expression-equivalent to:

- `(void)iter_swap(E1, E2)`, if either `E1` or `E2` has class or
  enumeration type and `iter_swap(E1, E2)` is a well-formed expression
  with overload resolution performed in a context that includes the
  declaration
  ``` cpp
  template<class I1, class I2>
    void iter_swap(I1, I2) = delete;
  ```

  and does not include a declaration of `ranges::iter_swap`. If the
  function selected by overload resolution does not exchange the values
  denoted by `E1` and `E2`, the program is ill-formed, no diagnostic
  required.
- Otherwise, if the types of `E1` and `E2` each model
  `indirectly_readable`, and if the reference types of `E1` and `E2`
  model `swappable_with` [[concept.swappable]], then
  `ranges::swap(*E1, *E2)`.
- Otherwise, if the types `T1` and `T2` of `E1` and `E2` model
  `indirectly_movable_storable<T1, T2>` and
  `indirectly_movable_storable<T2, T1>`, then
  `(void)(*E1 = iter-exchange-move(E2, E1))`, except that `E1` is
  evaluated only once.
- Otherwise, `ranges::iter_swap(E1, E2)` is ill-formed. \[*Note 2*: This
  case can result in substitution failure when
  `ranges::iter_swap(E1, E2)` appears in the immediate context of a
  template instantiation. — *end note*]

### Iterator concepts <a id="iterator.concepts">[[iterator.concepts]]</a>

#### General <a id="iterator.concepts.general">[[iterator.concepts.general]]</a>

For a type `I`, let `ITER_TRAITS(I)` denote the type `I` if
`iterator_traits<I>` names a specialization generated from the primary
template. Otherwise, `ITER_TRAITS(I)` denotes `iterator_traits<I>`.

- If the *qualified-id* `ITER_TRAITS(I)::iterator_concept` is valid and
  names a type, then `ITER_CONCEPT(I)` denotes that type.
- Otherwise, if the *qualified-id* `ITER_TRAITS(I){}::iterator_category`
  is valid and names a type, then `ITER_CONCEPT(I)` denotes that type.
- Otherwise, if `iterator_traits<I>` names a specialization generated
  from the primary template, then `ITER_CONCEPT(I)` denotes
  `random_access_iterator_tag`.
- Otherwise, `ITER_CONCEPT(I)` does not denote a type.

[*Note 1*: `ITER_TRAITS` enables independent syntactic determination of
an iterator’s category and concept. — *end note*]

[*Example 1*:

``` cpp
struct I {
  using value_type = int;
  using difference_type = int;

  int operator*() const;
  I& operator++();
  I operator++(int);
  I& operator--();
  I operator--(int);

  bool operator==(I) const;
  bool operator!=(I) const;
};
```

`iterator_traits<I>::iterator_category` denotes `input_iterator_tag`,
and `ITER_CONCEPT(I)` denotes `random_access_iterator_tag`.

— *end example*]

#### Concept  <a id="iterator.concept.readable">[[iterator.concept.readable]]</a>

Types that are indirectly readable by applying `operator*` model the
`indirectly_readable` concept, including pointers, smart pointers, and
iterators.

``` cpp
template<class In>
  concept indirectly-readable-impl =
    requires(const In in) {
      typename iter_value_t<In>;
      typename iter_reference_t<In>;
      typename iter_rvalue_reference_t<In>;
      { *in } -> same_as<iter_reference_t<In>>;
      { ranges::iter_move(in) } -> same_as<iter_rvalue_reference_t<In>>;
    } &&
    common_reference_with<iter_reference_t<In>&&, iter_value_t<In>&> &&
    common_reference_with<iter_reference_t<In>&&, iter_rvalue_reference_t<In>&&> &&
    common_reference_with<iter_rvalue_reference_t<In>&&, const iter_value_t<In>&>;
```

``` cpp
template<class In>
  concept indirectly_readable =
    indirectly-readable-impl<remove_cvref_t<In>>;
```

Given a value `i` of type `I`, `I` models `indirectly_readable` only if
the expression `*i` is equality-preserving.

[*Note 1*: The expression `*i` is indirectly required to be valid via
the exposition-only `dereferenceable` concept
[[iterator.synopsis]]. — *end note*]

#### Concept  <a id="iterator.concept.writable">[[iterator.concept.writable]]</a>

The `indirectly_writable` concept specifies the requirements for writing
a value into an iterator’s referenced object.

``` cpp
template<class Out, class T>
  concept indirectly_writable =
    requires(Out&& o, T&& t) {
      *o = std::forward<T>(t);  // not required to be equality-preserving
      *std::forward<Out>(o) = std::forward<T>(t);   // not required to be equality-preserving
      const_cast<const iter_reference_t<Out>&&>(*o) =
        std::forward<T>(t);     // not required to be equality-preserving
      const_cast<const iter_reference_t<Out>&&>(*std::forward<Out>(o)) =
        std::forward<T>(t);     // not required to be equality-preserving
    };
```

Let `E` be an expression such that `decltype((E))` is `T`, and let `o`
be a dereferenceable object of type `Out`. `Out` and `T` model
`indirectly_writable<Out, T>` only if

- If `Out` and `T` model
  `indirectly_readable<Out> && same_as<iter_value_t<Out>, decay_t<T>{>}`,
  then `*o` after any above assignment is equal to the value of `E`
  before the assignment.

After evaluating any above assignment expression, `o` is not required to
be dereferenceable.

If `E` is an xvalue [[basic.lval]], the resulting state of the object it
denotes is valid but unspecified [[lib.types.movedfrom]].

[*Note 1*: The only valid use of an `operator*` is on the left side of
the assignment statement. Assignment through the same value of the
indirectly writable type happens only once. — *end note*]

[*Note 2*: `indirectly_writable` has the awkward `const_cast`
expressions to reject iterators with prvalue non-proxy reference types
that permit rvalue assignment but do not also permit `const` rvalue
assignment. Consequently, an iterator type `I` that returns
`std::string` by value does not model
`indirectly_writable<I, std::string>`. — *end note*]

#### Concept  <a id="iterator.concept.winc">[[iterator.concept.winc]]</a>

The `weakly_incrementable` concept specifies the requirements on types
that can be incremented with the pre- and post-increment operators. The
increment operations are not required to be equality-preserving, nor is
the type required to be `equality_comparable`.

``` cpp
template<class T>
  inline constexpr bool is-integer-like = see below; \itcorr[-2]           // exposition only

template<class T>
  inline constexpr bool is-signed-integer-like = see below; \itcorr[-2]    // exposition only

template<class I>
  concept weakly_incrementable =
    default_initializable<I> && movable<I> &&
    requires(I i) {
      typename iter_difference_t<I>;
      requires is-signed-integer-like<iter_difference_t<I>>;
      { ++i } -> same_as<I&>;   // not required to be equality-preserving
      i++;                      // not required to be equality-preserving
    };
```

A type `I` is an *integer-class type* if it is in a set of
implementation-defined class types that behave as integer types do, as
defined in below.

The range of representable values of an integer-class type is the
continuous set of values over which it is defined. The values 0 and 1
are part of the range of every integer-class type. If any negative
numbers are part of the range, the type is a
*signed-integer-class type*; otherwise, it is an
*unsigned-integer-class type*.

For every integer-class type `I`, let `B(I)` be a hypothetical extended
integer type of the same signedness with the smallest width
[[basic.fundamental]] capable of representing the same range of values.
The width of `I` is equal to the width of `B(I)`.

Let `a` and `b` be objects of integer-class type `I`, let `x` and `y` be
objects of type `B(I)` as described above that represent the same values
as `a` and `b` respectively, and let `c` be an lvalue of any integral
type.

- For every unary operator `@` for which the expression `@x` is
  well-formed, `@a` shall also be well-formed and have the same value,
  effects, and value category as `@x` provided that value is
  representable by `I`. If `@x` has type `bool`, so too does `@a`; if
  `@x` has type `B(I)`, then `@a` has type `I`.
- For every assignment operator `@=` for which `c @= x` is well-formed,
  `c @= a` shall also be well-formed and shall have the same value and
  effects as `c @= x`. The expression `c @= a` shall be an lvalue
  referring to `c`.
- For every binary operator `@` for which `x @ y` is well-formed,
  `a @ b` shall also be well-formed and shall have the same value,
  effects, and value category as `x @ y` provided that value is
  representable by `I`. If `x @ y` has type `bool`, so too does `a @ b`;
  if `x @ y` has type `B(I)`, then `a @ b` has type `I`.

Expressions of integer-class type are explicitly convertible to any
integral type. Expressions of integral type are both implicitly and
explicitly convertible to any integer-class type. Conversions between
integral and integer-class types do not exit via an exception.

An expression `E` of integer-class type `I` is contextually convertible
to `bool` as if by `bool(E != I(0))`.

All integer-class types model `regular` [[concepts.object]] and
`totally_ordered` [[concept.totallyordered]].

A value-initialized object of integer-class type has value 0.

For every (possibly cv-qualified) integer-class type `I`,
`numeric_limits<I>` is specialized such that:

- `numeric_limits<I>::is_specialized` is `true`,
- `numeric_limits<I>::is_signed` is `true` if and only if `I` is a
  signed-integer-class type,
- `numeric_limits<I>::is_integer` is `true`,
- `numeric_limits<I>::is_exact` is `true`,
- `numeric_limits<I>::digits` is equal to the width of the integer-class
  type,
- `numeric_limits<I>::digits10` is equal to
  `static_cast<int>(digits * log10(2))`, and
- `numeric_limits<I>::min()` and `numeric_limits<I>::max()` return the
  lowest and highest representable values of `I`, respectively, and
  `numeric_limits<I>::lowest()` returns `numeric_limits<I>::{}min()`.

A type `I` is *integer-like* if it models `integral<I>` or if it is an
integer-class type. A type `I` is *signed-integer-like* if it models
`signed_integral<I>` or if it is a signed-integer-class type. A type `I`
is *unsigned-integer-like* if it models `unsigned_integral<I>` or if it
is an unsigned-integer-class type.

`is-integer-like<I>` is `true` if and only if `I` is an integer-like
type. `is-signed-integer-like<I>` is `true` if and only if I is a
signed-integer-like type.

Let `i` be an object of type `I`. When `i` is in the domain of both pre-
and post-increment, `i` is said to be *incrementable*. `I` models
`weakly_incrementable<I>` only if

- The expressions `++i` and `i++` have the same domain.
- If `i` is incrementable, then both `++i` and `i++` advance `i` to the
  next element.
- If `i` is incrementable, then `addressof(++i)` is equal to
  `addressof(i)`.

[*Note 1*: For `weakly_incrementable` types, `a` equals `b` does not
imply that `++a` equals `++b`. (Equality does not guarantee the
substitution property or referential transparency.) Algorithms on weakly
incrementable types should never attempt to pass through the same
incrementable value twice. They should be single-pass algorithms. These
algorithms can be used with istreams as the source of the input data
through the `istream_iterator` class template. — *end note*]

#### Concept  <a id="iterator.concept.inc">[[iterator.concept.inc]]</a>

The `incrementable` concept specifies requirements on types that can be
incremented with the pre- and post-increment operators. The increment
operations are required to be equality-preserving, and the type is
required to be `equality_comparable`.

[*Note 1*: This supersedes the annotations on the increment expressions
in the definition of `weakly_incrementable`. — *end note*]

``` cpp
template<class I>
  concept incrementable =
    regular<I> &&
    weakly_incrementable<I> &&
    requires(I i) {
      { i++ } -> same_as<I>;
    };
```

Let `a` and `b` be incrementable objects of type `I`. `I` models
`incrementable` only if

- If `bool(a == b)` then `bool(a++ == b)`.
- If `bool(a == b)` then `bool(((void)a++, a) == ++b)`.

[*Note 2*: The requirement that `a` equals `b` implies `++a` equals
`++b` (which is not true for weakly incrementable types) allows the use
of multi-pass one-directional algorithms with types that model
`incrementable`. — *end note*]

#### Concept  <a id="iterator.concept.iterator">[[iterator.concept.iterator]]</a>

The `input_or_output_iterator` concept forms the basis of the iterator
concept taxonomy; every iterator models `input_or_output_iterator`. This
concept specifies operations for dereferencing and incrementing an
iterator. Most algorithms will require additional operations to compare
iterators with sentinels [[iterator.concept.sentinel]], to read
[[iterator.concept.input]] or write [[iterator.concept.output]] values,
or to provide a richer set of iterator movements (
[[iterator.concept.forward]], [[iterator.concept.bidir]],
[[iterator.concept.random.access]]).

``` cpp
template<class I>
  concept input_or_output_iterator =
    requires(I i) {
      { *i } -> can-reference;
    } &&
    weakly_incrementable<I>;
```

[*Note 1*: Unlike the *Cpp17Iterator* requirements, the
`input_or_output_iterator` concept does not require
copyability. — *end note*]

#### Concept  <a id="iterator.concept.sentinel">[[iterator.concept.sentinel]]</a>

The `sentinel_for` concept specifies the relationship between an
`input_or_output_iterator` type and a `semiregular` type whose values
denote a range.

``` cpp
template<class S, class I>
  concept sentinel_for =
    semiregular<S> &&
    input_or_output_iterator<I> &&
    weakly-equality-comparable-with<S, I>; // See [concept.equalitycomparable]
```

Let `s` and `i` be values of type `S` and `I` such that \[`i`, `s`)
denotes a range. Types `S` and `I` model `sentinel_for<S, I>` only if

- `i == s` is well-defined.
- If `bool(i != s)` then `i` is dereferenceable and \[`++i`, `s`)
  denotes a range.

The domain of `==` is not static. Given an iterator `i` and sentinel `s`
such that \[`i`, `s`) denotes a range and `i != s`, `i` and `s` are not
required to continue to denote a range after incrementing any other
iterator equal to `i`. Consequently, `i == s` is no longer required to
be well-defined.

#### Concept  <a id="iterator.concept.sizedsentinel">[[iterator.concept.sizedsentinel]]</a>

The `sized_sentinel_for` concept specifies requirements on an
`input_or_output_iterator` type `I` and a corresponding
`sentinel_for<I>` that allow the use of the `-` operator to compute the
distance between them in constant time.

``` cpp
template<class S, class I>
  concept sized_sentinel_for =
    sentinel_for<S, I> &&
    !disable_sized_sentinel_for<remove_cv_t<S>, remove_cv_t<I>> &&
    requires(const I& i, const S& s) {
      { s - i } -> same_as<iter_difference_t<I>>;
      { i - s } -> same_as<iter_difference_t<I>>;
    };
```

Let `i` be an iterator of type `I`, and `s` a sentinel of type `S` such
that \[`i`, `s`) denotes a range. Let N be the smallest number of
applications of `++i` necessary to make `bool(i == s)` be `true`. `S`
and `I` model `sized_sentinel_for<S, I>` only if

- If N is representable by `iter_difference_t<I>`, then `s - i` is
  well-defined and equals N.
- If -N is representable by `iter_difference_t<I>`, then `i - s` is
  well-defined and equals -N.

``` cpp
template<class S, class I>
  inline constexpr bool disable_sized_sentinel_for = false;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`disable_sized_sentinel_for` for cv-unqualified non-array object types
`S` and `I` if `S` and/or `I` is a program-defined type. Such
specializations shall be usable in constant expressions [[expr.const]]
and have type `const bool`.

[*Note 1*: `disable_sized_sentinel_for` allows use of sentinels and
iterators with the library that satisfy but do not in fact model
`sized_sentinel_for`. — *end note*]

[*Example 1*: The `sized_sentinel_for` concept is modeled by pairs of
`random_access_iterator`s [[iterator.concept.random.access]] and by
counted iterators and their
sentinels [[counted.iterator]]. — *end example*]

#### Concept  <a id="iterator.concept.input">[[iterator.concept.input]]</a>

The `input_iterator` concept defines requirements for a type whose
referenced values can be read (from the requirement for
`indirectly_readable` [[iterator.concept.readable]]) and which can be
both pre- and post-incremented.

[*Note 1*: Unlike the *Cpp17InputIterator* requirements
[[input.iterators]], the `input_iterator` concept does not need equality
comparison since iterators are typically compared to
sentinels. — *end note*]

``` cpp
template<class I>
  concept input_iterator =
    input_or_output_iterator<I> &&
    indirectly_readable<I> &&
    requires { typename ITER_CONCEPT(I); } &&
    derived_from<ITER_CONCEPT(I), input_iterator_tag>;
```

#### Concept  <a id="iterator.concept.output">[[iterator.concept.output]]</a>

The `output_iterator` concept defines requirements for a type that can
be used to write values (from the requirement for `indirectly_writable`
[[iterator.concept.writable]]) and which can be both pre- and
post-incremented.

[*Note 1*: Output iterators are not required to model
`equality_comparable`. — *end note*]

``` cpp
template<class I, class T>
  concept output_iterator =
    input_or_output_iterator<I> &&
    indirectly_writable<I, T> &&
    requires(I i, T&& t) {
      *i++ = std::forward<T>(t);        // not required to be equality-preserving
    };
```

Let `E` be an expression such that `decltype((E))` is `T`, and let `i`
be a dereferenceable object of type `I`. `I` and `T` model
`output_iterator<I, T>` only if `*i++ = E;` has effects equivalent to:

``` cpp
*i = E;
++i;
```

[*Note 2*: Algorithms on output iterators should never attempt to pass
through the same iterator twice. They should be single-pass
algorithms. — *end note*]

#### Concept  <a id="iterator.concept.forward">[[iterator.concept.forward]]</a>

The `forward_iterator` concept adds copyability, equality comparison,
and the multi-pass guarantee, specified below.

``` cpp
template<class I>
  concept forward_iterator =
    input_iterator<I> &&
    derived_from<ITER_CONCEPT(I), forward_iterator_tag> &&
    incrementable<I> &&
    sentinel_for<I, I>;
```

The domain of `==` for forward iterators is that of iterators over the
same underlying sequence. However, value-initialized iterators of the
same type may be compared and shall compare equal to other
value-initialized iterators of the same type.

[*Note 1*: Value-initialized iterators behave as if they refer past the
end of the same empty sequence. — *end note*]

Pointers and references obtained from a forward iterator into a range
\[`i`, `s`) shall remain valid while \[`i`, `s`) continues to denote a
range.

Two dereferenceable iterators `a` and `b` of type `X` offer the
*multi-pass guarantee* if:

- `a == b` implies `++a == ++b` and
- The expression `((void)[](X x){++x;}(a), *a)` is equivalent to the
  expression `*a`.

[*Note 2*: The requirement that `a == b` implies `++a == ++b` and the
removal of the restrictions on the number of assignments through a
mutable iterator (which applies to output iterators) allow the use of
multi-pass one-directional algorithms with forward
iterators. — *end note*]

#### Concept  <a id="iterator.concept.bidir">[[iterator.concept.bidir]]</a>

The `bidirectional_iterator` concept adds the ability to move an
iterator backward as well as forward.

``` cpp
template<class I>
  concept bidirectional_iterator =
    forward_iterator<I> &&
    derived_from<ITER_CONCEPT(I), bidirectional_iterator_tag> &&
    requires(I i) {
      { --i } -> same_as<I&>;
      { i-- } -> same_as<I>;
    };
```

A bidirectional iterator `r` is decrementable if and only if there
exists some `q` such that `++q == r`. Decrementable iterators `r` shall
be in the domain of the expressions `--r` and `r--`.

Let `a` and `b` be equal objects of type `I`. `I` models
`bidirectional_iterator` only if:

- If `a` and `b` are decrementable, then all of the following are
  `true`:
  - `addressof(--a) == addressof(a)`
  - `bool(a-- == b)`
  - after evaluating both `a--` and `--b`, `bool(a == b)` is still
    `true`
  - `bool(++(--a) == b)`
- If `a` and `b` are incrementable, then `bool(--(++a) == b)`.

#### Concept  <a id="iterator.concept.random.access">[[iterator.concept.random.access]]</a>

The `random_access_iterator` concept adds support for constant-time
advancement with `+=`, `+`, `-=`, and `-`, as well as the computation of
distance in constant time with `-`. Random access iterators also support
array notation via subscripting.

``` cpp
template<class I>
  concept random_access_iterator =
    bidirectional_iterator<I> &&
    derived_from<ITER_CONCEPT(I), random_access_iterator_tag> &&
    totally_ordered<I> &&
    sized_sentinel_for<I, I> &&
    requires(I i, const I j, const iter_difference_t<I> n) {
      { i += n } -> same_as<I&>;
      { j +  n } -> same_as<I>;
      { n +  j } -> same_as<I>;
      { i -= n } -> same_as<I&>;
      { j -  n } -> same_as<I>;
      {  j[n]  } -> same_as<iter_reference_t<I>>;
    };
```

Let `a` and `b` be valid iterators of type `I` such that `b` is
reachable from `a` after `n` applications of `++a`, let `D` be
`iter_difference_t<I>`, and let `n` denote a value of type `D`. `I`
models `random_access_iterator` only if

- `(a += n)` is equal to `b`.
- `addressof(a += n)` is equal to `addressof(a)`.
- `(a + n)` is equal to `(a += n)`.
- For any two positive values `x` and `y` of type `D`, if
  `(a + D(x + y))` is valid, then `(a + D(x + y))` is equal to
  `((a + x) + y)`.
- `(a + D(0))` is equal to `a`.
- If `(a + D(n - 1))` is valid, then `(a + n)` is equal to
  `[](I c){ return ++c; }(a + D(n - 1))`.
- `(b += D(-n))` is equal to `a`.
- `(b -= n)` is equal to `a`.
- `addressof(b -= n)` is equal to `addressof(b)`.
- `(b - n)` is equal to `(b -= n)`.
- If `b` is dereferenceable, then `a[n]` is valid and is equal to `*b`.
- `bool(a <= b)` is `true`.

#### Concept  <a id="iterator.concept.contiguous">[[iterator.concept.contiguous]]</a>

The `contiguous_iterator` concept provides a guarantee that the denoted
elements are stored contiguously in memory.

``` cpp
template<class I>
  concept contiguous_iterator =
    random_access_iterator<I> &&
    derived_from<ITER_CONCEPT(I), contiguous_iterator_tag> &&
    is_lvalue_reference_v<iter_reference_t<I>> &&
    same_as<iter_value_t<I>, remove_cvref_t<iter_reference_t<I>>> &&
    requires(const I& i) {
      { to_address(i) } -> same_as<add_pointer_t<iter_reference_t<I>>>;
    };
```

Let `a` and `b` be dereferenceable iterators and `c` be a
non-dereferenceable iterator of type `I` such that `b` is reachable from
`a` and `c` is reachable from `b`, and let `D` be
`iter_difference_t<I>`. The type `I` models `contiguous_iterator` only
if

- `to_address(a) == addressof(*a)`,
- `to_address(b) == to_address(a) + D(b - a)`, and
- `to_address(c) == to_address(a) + D(c - a)`.

### C++17 iterator requirements <a id="iterator.cpp17">[[iterator.cpp17]]</a>

In the following sections, `a` and `b` denote values of type `X` or
`const X`, `difference_type` and `reference` refer to the types
`iterator_traits<X>::difference_type` and
`iterator_traits<X>::reference`, respectively, `n` denotes a value of
`difference_type`, `u`, `tmp`, and `m` denote identifiers, `r` denotes a
value of `X&`, `t` denotes a value of value type `T`, `o` denotes a
value of some type that is writable to the output iterator.

[*Note 1*: For an iterator type `X` there must be an instantiation of
`iterator_traits<X>` [[iterator.traits]]. — *end note*]

#### *Cpp17Iterator* <a id="iterator.iterators">[[iterator.iterators]]</a>

The *Cpp17Iterator* requirements form the basis of the iterator
taxonomy; every iterator meets the *Cpp17Iterator* requirements. This
set of requirements specifies operations for dereferencing and
incrementing an iterator. Most algorithms will require additional
operations to read [[input.iterators]] or write [[output.iterators]]
values, or to provide a richer set of iterator movements (
[[forward.iterators]], [[bidirectional.iterators]],
[[random.access.iterators]]).

A type `X` meets the *Cpp17Iterator* requirements if:

- `X` meets the *Cpp17CopyConstructible*, *Cpp17CopyAssignable*, and
  *Cpp17Destructible* requirements [[utility.arg.requirements]] and
  lvalues of type `X` are swappable [[swappable.requirements]], and
- `iterator_traits<X>::difference_type` is a signed integer type or
  `void`, and
- the expressions in [[iterator]] are valid and have the indicated
  semantics.

#### Input iterators <a id="input.iterators">[[input.iterators]]</a>

A class or pointer type `X` meets the requirements of an input iterator
for the value type `T` if `X` meets the *Cpp17Iterator*
[[iterator.iterators]] and *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) requirements and the expressions in
[[inputiterator]] are valid and have the indicated semantics.

In [[inputiterator]], the term *the domain of `==`* is used in the
ordinary mathematical sense to denote the set of values over which `==`
is (required to be) defined. This set can change over time. Each
algorithm places additional requirements on the domain of `==` for the
iterator values it uses. These requirements can be inferred from the
uses that algorithm makes of `==` and `!=`.

[*Example 1*: The call `find(a,b,x)` is defined only if the value of
`a` has the property *p* defined as follows: `b` has property *p* and a
value `i` has property *p* if (`*i==x`) or if (`*i!=x` and `++i` has
property *p*). — *end example*]

[*Note 1*: For input iterators, `a == b` does not imply `++a == ++b`.
(Equality does not guarantee the substitution property or referential
transparency.) Algorithms on input iterators should never attempt to
pass through the same iterator twice. They should be *single pass*
algorithms. Value type `T` is not required to be a *Cpp17CopyAssignable*
type ([[cpp17.copyassignable]]). These algorithms can be used with
istreams as the source of the input data through the `istream_iterator`
class template. — *end note*]

#### Output iterators <a id="output.iterators">[[output.iterators]]</a>

A class or pointer type `X` meets the requirements of an output iterator
if `X` meets the *Cpp17Iterator* requirements [[iterator.iterators]] and
the expressions in [[outputiterator]] are valid and have the indicated
semantics.

[*Note 1*: The only valid use of an `operator*` is on the left side of
the assignment statement. Assignment through the same value of the
iterator happens only once. Algorithms on output iterators should never
attempt to pass through the same iterator twice. They should be
single-pass algorithms. Equality and inequality might not be
defined. — *end note*]

#### Forward iterators <a id="forward.iterators">[[forward.iterators]]</a>

A class or pointer type `X` meets the requirements of a forward iterator
if

- `X` meets the *Cpp17InputIterator* requirements [[input.iterators]],
- `X` meets the *Cpp17DefaultConstructible* requirements
  [[utility.arg.requirements]],
- if `X` is a mutable iterator, `reference` is a reference to `T`; if
  `X` is a constant iterator, `reference` is a reference to `const T`,
- the expressions in [[forwarditerator]] are valid and have the
  indicated semantics, and
- objects of type `X` offer the multi-pass guarantee, described below.

The domain of `==` for forward iterators is that of iterators over the
same underlying sequence. However, value-initialized iterators may be
compared and shall compare equal to other value-initialized iterators of
the same type.

[*Note 1*: Value-initialized iterators behave as if they refer past the
end of the same empty sequence. — *end note*]

Two dereferenceable iterators `a` and `b` of type `X` offer the
*multi-pass guarantee* if:

- `a == b` implies `++a == ++b` and
- `X` is a pointer type or the expression `(void)++X(a), *a` is
  equivalent to the expression `*a`.

[*Note 2*: The requirement that `a == b` implies `++a == ++b` (which is
not true for input and output iterators) and the removal of the
restrictions on the number of the assignments through a mutable iterator
(which applies to output iterators) allows the use of multi-pass
one-directional algorithms with forward iterators. — *end note*]

If `a` and `b` are equal, then either `a` and `b` are both
dereferenceable or else neither is dereferenceable.

If `a` and `b` are both dereferenceable, then `a == b` if and only if
`*a` and `*b` are bound to the same object.

#### Bidirectional iterators <a id="bidirectional.iterators">[[bidirectional.iterators]]</a>

A class or pointer type `X` meets the requirements of a bidirectional
iterator if, in addition to meeting the *Cpp17ForwardIterator*
requirements, the following expressions are valid as shown in
[[bidirectionaliterator]].

[*Note 1*: Bidirectional iterators allow algorithms to move iterators
backward as well as forward. — *end note*]

#### Random access iterators <a id="random.access.iterators">[[random.access.iterators]]</a>

A class or pointer type `X` meets the requirements of a random access
iterator if, in addition to meeting the *Cpp17BidirectionalIterator*
requirements, the following expressions are valid as shown in
[[randomaccessiterator]].

### Indirect callable requirements <a id="indirectcallable">[[indirectcallable]]</a>

#### General <a id="indirectcallable.general">[[indirectcallable.general]]</a>

There are several concepts that group requirements of algorithms that
take callable objects ([[func.def]]) as arguments.

#### Indirect callables <a id="indirectcallable.indirectinvocable">[[indirectcallable.indirectinvocable]]</a>

The indirect callable concepts are used to constrain those algorithms
that accept callable objects ([[func.def]]) as arguments.

``` cpp
namespace std {
  template<class F, class I>
    concept indirectly_unary_invocable =
      indirectly_readable<I> &&
      copy_constructible<F> &&
      invocable<F&, iter_value_t<I>&> &&
      invocable<F&, iter_reference_t<I>> &&
      invocable<F&, iter_common_reference_t<I>> &&
      common_reference_with<
        invoke_result_t<F&, iter_value_t<I>&>,
        invoke_result_t<F&, iter_reference_t<I>>>;

  template<class F, class I>
    concept indirectly_regular_unary_invocable =
      indirectly_readable<I> &&
      copy_constructible<F> &&
      regular_invocable<F&, iter_value_t<I>&> &&
      regular_invocable<F&, iter_reference_t<I>> &&
      regular_invocable<F&, iter_common_reference_t<I>> &&
      common_reference_with<
        invoke_result_t<F&, iter_value_t<I>&>,
        invoke_result_t<F&, iter_reference_t<I>>>;

  template<class F, class I>
    concept indirect_unary_predicate =
      indirectly_readable<I> &&
      copy_constructible<F> &&
      predicate<F&, iter_value_t<I>&> &&
      predicate<F&, iter_reference_t<I>> &&
      predicate<F&, iter_common_reference_t<I>>;

  template<class F, class I1, class I2>
    concept indirect_binary_predicate =
      indirectly_readable<I1> && indirectly_readable<I2> &&
      copy_constructible<F> &&
      predicate<F&, iter_value_t<I1>&, iter_value_t<I2>&> &&
      predicate<F&, iter_value_t<I1>&, iter_reference_t<I2>> &&
      predicate<F&, iter_reference_t<I1>, iter_value_t<I2>&> &&
      predicate<F&, iter_reference_t<I1>, iter_reference_t<I2>> &&
      predicate<F&, iter_common_reference_t<I1>, iter_common_reference_t<I2>>;

  template<class F, class I1, class I2 = I1>
    concept indirect_equivalence_relation =
      indirectly_readable<I1> && indirectly_readable<I2> &&
      copy_constructible<F> &&
      equivalence_relation<F&, iter_value_t<I1>&, iter_value_t<I2>&> &&
      equivalence_relation<F&, iter_value_t<I1>&, iter_reference_t<I2>> &&
      equivalence_relation<F&, iter_reference_t<I1>, iter_value_t<I2>&> &&
      equivalence_relation<F&, iter_reference_t<I1>, iter_reference_t<I2>> &&
      equivalence_relation<F&, iter_common_reference_t<I1>, iter_common_reference_t<I2>>;

  template<class F, class I1, class I2 = I1>
    concept indirect_strict_weak_order =
      indirectly_readable<I1> && indirectly_readable<I2> &&
      copy_constructible<F> &&
      strict_weak_order<F&, iter_value_t<I1>&, iter_value_t<I2>&> &&
      strict_weak_order<F&, iter_value_t<I1>&, iter_reference_t<I2>> &&
      strict_weak_order<F&, iter_reference_t<I1>, iter_value_t<I2>&> &&
      strict_weak_order<F&, iter_reference_t<I1>, iter_reference_t<I2>> &&
      strict_weak_order<F&, iter_common_reference_t<I1>, iter_common_reference_t<I2>>;
}
```

#### Class template `projected` <a id="projected">[[projected]]</a>

Class template `projected` is used to constrain algorithms that accept
callable objects and projections [[defns.projection]]. It combines a
`indirectly_readable` type `I` and a callable object type `Proj` into a
new `indirectly_readable` type whose `reference` type is the result of
applying `Proj` to the `iter_reference_t` of `I`.

``` cpp
namespace std {
  template<indirectly_readable I, indirectly_regular_unary_invocable<I> Proj>
  struct projected {
    using value_type = remove_cvref_t<indirect_result_t<Proj&, I>>;
    indirect_result_t<Proj&, I> operator*() const;              // not defined
  };

  template<weakly_incrementable I, class Proj>
  struct incrementable_traits<projected<I, Proj>> {
    using difference_type = iter_difference_t<I>;
  };
}
```

### Common algorithm requirements <a id="alg.req">[[alg.req]]</a>

#### General <a id="alg.req.general">[[alg.req.general]]</a>

There are several additional iterator concepts that are commonly applied
to families of algorithms. These group together iterator requirements of
algorithm families. There are three relational concepts that specify how
element values are transferred between `indirectly_readable` and
`indirectly_writable` types: `indirectly_movable`,
`indirectly_copyable`, and `indirectly_swappable`. There are three
relational concepts for rearrangements: `permutable`, `mergeable`, and
`sortable`. There is one relational concept for comparing values from
different sequences: `indirectly_comparable`.

[*Note 1*: The `ranges::less` function object type used in the concepts
below imposes constraints on the concepts’ arguments in addition to
those that appear in the concepts’ bodies [[range.cmp]]. — *end note*]

#### Concept  <a id="alg.req.ind.move">[[alg.req.ind.move]]</a>

The `indirectly_movable` concept specifies the relationship between a
`indirectly_readable` type and a `indirectly_writable` type between
which values may be moved.

``` cpp
template<class In, class Out>
  concept indirectly_movable =
    indirectly_readable<In> &&
    indirectly_writable<Out, iter_rvalue_reference_t<In>>;
```

The `indirectly_movable_storable` concept augments `indirectly_movable`
with additional requirements enabling the transfer to be performed
through an intermediate object of the `indirectly_readable` type’s value
type.

``` cpp
template<class In, class Out>
  concept indirectly_movable_storable =
    indirectly_movable<In, Out> &&
    indirectly_writable<Out, iter_value_t<In>> &&
    movable<iter_value_t<In>> &&
    constructible_from<iter_value_t<In>, iter_rvalue_reference_t<In>> &&
    assignable_from<iter_value_t<In>&, iter_rvalue_reference_t<In>>;
```

Let `i` be a dereferenceable value of type `In`. `In` and `Out` model
`indirectly_movable_storable<In, Out>` only if after the initialization
of the object `obj` in

``` cpp
iter_value_t<In> obj(ranges::iter_move(i));
```

`obj` is equal to the value previously denoted by `*i`. If
`iter_rvalue_reference_t<In>` is an rvalue reference type, the resulting
state of the value denoted by `*i` is valid but unspecified
[[lib.types.movedfrom]].

#### Concept  <a id="alg.req.ind.copy">[[alg.req.ind.copy]]</a>

The `indirectly_copyable` concept specifies the relationship between a
`indirectly_readable` type and a `indirectly_writable` type between
which values may be copied.

``` cpp
template<class In, class Out>
  concept indirectly_copyable =
    indirectly_readable<In> &&
    indirectly_writable<Out, iter_reference_t<In>>;
```

The `indirectly_copyable_storable` concept augments
`indirectly_copyable` with additional requirements enabling the transfer
to be performed through an intermediate object of the
`indirectly_readable` type’s value type. It also requires the capability
to make copies of values.

``` cpp
template<class In, class Out>
  concept indirectly_copyable_storable =
    indirectly_copyable<In, Out> &&
    indirectly_writable<Out, iter_value_t<In>&> &&
    indirectly_writable<Out, const iter_value_t<In>&> &&
    indirectly_writable<Out, iter_value_t<In>&&> &&
    indirectly_writable<Out, const iter_value_t<In>&&> &&
    copyable<iter_value_t<In>> &&
    constructible_from<iter_value_t<In>, iter_reference_t<In>> &&
    assignable_from<iter_value_t<In>&, iter_reference_t<In>>;
```

Let `i` be a dereferenceable value of type `In`. `In` and `Out` model
`indirectly_copyable_storable<In, Out>` only if after the initialization
of the object `obj` in

``` cpp
iter_value_t<In> obj(*i);
```

`obj` is equal to the value previously denoted by `*i`. If
`iter_reference_t<In>` is an rvalue reference type, the resulting state
of the value denoted by `*i` is valid but unspecified
[[lib.types.movedfrom]].

#### Concept  <a id="alg.req.ind.swap">[[alg.req.ind.swap]]</a>

The `indirectly_swappable` concept specifies a swappable relationship
between the values referenced by two `indirectly_readable` types.

``` cpp
template<class I1, class I2 = I1>
  concept indirectly_swappable =
    indirectly_readable<I1> && indirectly_readable<I2> &&
    requires(const I1 i1, const I2 i2) {
      ranges::iter_swap(i1, i1);
      ranges::iter_swap(i2, i2);
      ranges::iter_swap(i1, i2);
      ranges::iter_swap(i2, i1);
    };
```

#### Concept  <a id="alg.req.ind.cmp">[[alg.req.ind.cmp]]</a>

The `indirectly_comparable` concept specifies the common requirements of
algorithms that compare values from two different sequences.

``` cpp
template<class I1, class I2, class R, class P1 = identity,
         class P2 = identity>
  concept indirectly_comparable =
    indirect_binary_predicate<R, projected<I1, P1>, projected<I2, P2>>;
```

#### Concept  <a id="alg.req.permutable">[[alg.req.permutable]]</a>

The `permutable` concept specifies the common requirements of algorithms
that reorder elements in place by moving or swapping them.

``` cpp
template<class I>
  concept permutable =
    forward_iterator<I> &&
    indirectly_movable_storable<I, I> &&
    indirectly_swappable<I, I>;
```

#### Concept  <a id="alg.req.mergeable">[[alg.req.mergeable]]</a>

The `mergeable` concept specifies the requirements of algorithms that
merge sorted sequences into an output sequence by copying elements.

``` cpp
template<class I1, class I2, class Out, class R = ranges::less,
         class P1 = identity, class P2 = identity>
  concept mergeable =
    input_iterator<I1> &&
    input_iterator<I2> &&
    weakly_incrementable<Out> &&
    indirectly_copyable<I1, Out> &&
    indirectly_copyable<I2, Out> &&
    indirect_strict_weak_order<R, projected<I1, P1>, projected<I2, P2>>;
```

#### Concept  <a id="alg.req.sortable">[[alg.req.sortable]]</a>

The `sortable` concept specifies the common requirements of algorithms
that permute sequences into ordered sequences (e.g., `sort`).

``` cpp
template<class I, class R = ranges::less, class P = identity>
  concept sortable =
    permutable<I> &&
    indirect_strict_weak_order<R, projected<I, P>>;
```

## Iterator primitives <a id="iterator.primitives">[[iterator.primitives]]</a>

To simplify the use of iterators, the library provides several classes
and functions.

### Standard iterator tags <a id="std.iterator.tags">[[std.iterator.tags]]</a>

It is often desirable for a function template specialization to find out
what is the most specific category of its iterator argument, so that the
function can select the most efficient algorithm at compile time. To
facilitate this, the library introduces *category tag* classes which are
used as compile time tags for algorithm selection. They are:
`output_iterator_tag`, `input_iterator_tag`, `forward_iterator_tag`,
`bidirectional_iterator_tag`, `random_access_iterator_tag`, and
`contiguous_iterator_tag`. For every iterator of type `I`,
`iterator_traits<I>::iterator_category` shall be defined to be a
category tag that describes the iterator’s behavior. Additionally,
`iterator_traits<I>::iterator_concept` may be used to indicate
conformance to the iterator concepts [[iterator.concepts]].

``` cpp
namespace std {
  struct output_iterator_tag { };
  struct input_iterator_tag { };
  struct forward_iterator_tag: public input_iterator_tag { };
  struct bidirectional_iterator_tag: public forward_iterator_tag { };
  struct random_access_iterator_tag: public bidirectional_iterator_tag { };
  struct contiguous_iterator_tag: public random_access_iterator_tag { };
}
```

[*Example 1*:

For a program-defined iterator `BinaryTreeIterator`, it could be
included into the bidirectional iterator category by specializing the
`iterator_traits` template:

``` cpp
template<class T> struct iterator_traits<BinaryTreeIterator<T>> {
  using iterator_category = bidirectional_iterator_tag;
  using difference_type   = ptrdiff_t;
  using value_type        = T;
  using pointer           = T*;
  using reference         = T&;
};
```

— *end example*]

[*Example 2*:

If `evolve()` is well-defined for bidirectional iterators, but can be
implemented more efficiently for random access iterators, then the
implementation is as follows:

``` cpp
template<class BidirectionalIterator>
inline void
evolve(BidirectionalIterator first, BidirectionalIterator last) {
  evolve(first, last,
    typename iterator_traits<BidirectionalIterator>::iterator_category());
}

template<class BidirectionalIterator>
void evolve(BidirectionalIterator first, BidirectionalIterator last,
  bidirectional_iterator_tag) {
  // more generic, but less efficient algorithm
}

template<class RandomAccessIterator>
void evolve(RandomAccessIterator first, RandomAccessIterator last,
  random_access_iterator_tag) {
  // more efficient, but less generic algorithm
}
```

— *end example*]

### Iterator operations <a id="iterator.operations">[[iterator.operations]]</a>

Since only random access iterators provide `+` and `-` operators, the
library provides two function templates `advance` and `distance`. These
function templates use `+` and `-` for random access iterators (and are,
therefore, constant time for them); for input, forward and bidirectional
iterators they use `++` to provide linear time implementations.

``` cpp
template<class InputIterator, class Distance>
  constexpr void advance(InputIterator& i, Distance n);
```

*Preconditions:* `n` is negative only for bidirectional iterators.

*Effects:* Increments `i` by `n` if `n` is non-negative, and decrements
`i` by `-n` otherwise.

``` cpp
template<class InputIterator>
  constexpr typename iterator_traits<InputIterator>::difference_type
    distance(InputIterator first, InputIterator last);
```

*Preconditions:* `last` is reachable from `first`, or `InputIterator`
meets the *Cpp17RandomAccessIterator* requirements and `first` is
reachable from `last`.

*Effects:* If `InputIterator` meets the *Cpp17RandomAccessIterator*
requirements, returns `(last - first)`; otherwise, returns the number of
increments needed to get from `first` to `last`.

``` cpp
template<class InputIterator>
  constexpr InputIterator next(InputIterator x,
    typename iterator_traits<InputIterator>::difference_type n = 1);
```

*Effects:* Equivalent to: `advance(x, n); return x;`

``` cpp
template<class BidirectionalIterator>
  constexpr BidirectionalIterator prev(BidirectionalIterator x,
    typename iterator_traits<BidirectionalIterator>::difference_type n = 1);
```

*Effects:* Equivalent to: `advance(x, -n); return x;`

### Range iterator operations <a id="range.iter.ops">[[range.iter.ops]]</a>

The library includes the function templates `ranges::advance`,
`ranges::distance`, `ranges::next`, and `ranges::prev` to manipulate
iterators. These operations adapt to the set of operators provided by
each iterator category to provide the most efficient implementation
possible for a concrete iterator type.

[*Example 1*: `ranges::advance` uses the `+` operator to move a
`random_access_iterator` forward `n` steps in constant time. For an
iterator type that does not model `random_access_iterator`,
`ranges::advance` instead performs `n` individual increments with the
`++` operator. — *end example*]

The function templates defined in this subclause are not found by
argument-dependent name lookup [[basic.lookup.argdep]]. When found by
unqualified [[basic.lookup.unqual]] name lookup for the
*postfix-expression* in a function call [[expr.call]], they inhibit
argument-dependent name lookup.

[*Example 2*:

``` cpp
void foo() {
    using namespace std::ranges;
    std::vector<int> vec{1,2,3};
    distance(begin(vec), end(vec));     // #1
}
```

The function call expression at `#1` invokes `std::ranges::distance`,
not `std::distance`, despite that (a) the iterator type returned from
`begin(vec)` and `end(vec)` may be associated with namespace `std` and
(b) `std::distance` is more specialized ([[temp.func.order]]) than
`std::ranges::distance` since the former requires its first two
parameters to have the same type.

— *end example*]

The number and order of deducible template parameters for the function
templates defined in this subclause is unspecified, except where
explicitly stated otherwise.

#### `ranges::advance` <a id="range.iter.op.advance">[[range.iter.op.advance]]</a>

``` cpp
template<input_or_output_iterator I>
  constexpr void ranges::advance(I& i, iter_difference_t<I> n);
```

*Preconditions:* If `I` does not model `bidirectional_iterator`, `n` is
not negative.

*Effects:*

- If `I` models `random_access_iterator`, equivalent to `i += n`.
- Otherwise, if `n` is non-negative, increments `i` by `n`.
- Otherwise, decrements `i` by `-n`.

``` cpp
template<input_or_output_iterator I, sentinel_for<I> S>
  constexpr void ranges::advance(I& i, S bound);
```

*Preconditions:* \[`i`, `bound`) denotes a range.

*Effects:*

- If `I` and `S` model `assignable_from<I&, S>`, equivalent to
  `i = std::move(bound)`.
- Otherwise, if `S` and `I` model `sized_sentinel_for<S, I>`, equivalent
  to `ranges::advance(i, bound - i)`.
- Otherwise, while `bool(i != bound)` is `true`, increments `i`.

``` cpp
template<input_or_output_iterator I, sentinel_for<I> S>
  constexpr iter_difference_t<I> ranges::advance(I& i, iter_difference_t<I> n, S bound);
```

*Preconditions:* If `n > 0`, \[`i`, `bound`) denotes a range. If
`n == 0`, \[`i`, `bound`) or \[`bound`, `i`) denotes a range. If
`n < 0`, \[`bound`, `i`) denotes a range, `I` models
`bidirectional_iterator`, and `I` and `S` model `same_as<I, S>`.

*Effects:*

- If `S` and `I` model `sized_sentinel_for<S, I>`:
  - If |`n`| \ge |`bound - i`|, equivalent to
    `ranges::advance(i, bound)`.
  - Otherwise, equivalent to `ranges::advance(i, n)`.
- Otherwise,
  - if `n` is non-negative, while `bool(i != bound)` is `true`,
    increments `i` but at most `n` times.
  - Otherwise, while `bool(i != bound)` is `true`, decrements `i` but at
    most `-n` times.

*Returns:* `n - `M, where M is the difference between the ending and
starting positions of `i`.

#### `ranges::distance` <a id="range.iter.op.distance">[[range.iter.op.distance]]</a>

``` cpp
template<input_or_output_iterator I, sentinel_for<I> S>
  constexpr iter_difference_t<I> ranges::distance(I first, S last);
```

*Preconditions:* \[`first`, `last`) denotes a range, or \[`last`,
`first`) denotes a range and `S` and `I` model
`same_as<S, I> && sized_sentinel_for<S, I>`.

*Effects:* If `S` and `I` model `sized_sentinel_for<S, I>`, returns
`(last - first)`; otherwise, returns the number of increments needed to
get from `first` to `last`.

``` cpp
template<range R>
  constexpr range_difference_t<R> ranges::distance(R&& r);
```

*Effects:* If `R` models `sized_range`, equivalent to:

``` cpp
return static_cast<range_difference_t<R>>(ranges::size(r));     // REF:range.prim.size
```

Otherwise, equivalent to:

``` cpp
return ranges::distance(ranges::begin(r), ranges::end(r));      // REF:range.access
```

#### `ranges::next` <a id="range.iter.op.next">[[range.iter.op.next]]</a>

``` cpp
template<input_or_output_iterator I>
  constexpr I ranges::next(I x);
```

*Effects:* Equivalent to: `++x; return x;`

``` cpp
template<input_or_output_iterator I>
  constexpr I ranges::next(I x, iter_difference_t<I> n);
```

*Effects:* Equivalent to: `ranges::advance(x, n); return x;`

``` cpp
template<input_or_output_iterator I, sentinel_for<I> S>
  constexpr I ranges::next(I x, S bound);
```

*Effects:* Equivalent to: `ranges::advance(x, bound); return x;`

``` cpp
template<input_or_output_iterator I, sentinel_for<I> S>
  constexpr I ranges::next(I x, iter_difference_t<I> n, S bound);
```

*Effects:* Equivalent to: `ranges::advance(x, n, bound); return x;`

#### `ranges::prev` <a id="range.iter.op.prev">[[range.iter.op.prev]]</a>

``` cpp
template<bidirectional_iterator I>
  constexpr I ranges::prev(I x);
```

*Effects:* Equivalent to: `-``-``x; return x;`

``` cpp
template<bidirectional_iterator I>
  constexpr I ranges::prev(I x, iter_difference_t<I> n);
```

*Effects:* Equivalent to: `ranges::advance(x, -n); return x;`

``` cpp
template<bidirectional_iterator I>
  constexpr I ranges::prev(I x, iter_difference_t<I> n, I bound);
```

*Effects:* Equivalent to: `ranges::advance(x, -n, bound); return x;`

## Iterator adaptors <a id="predef.iterators">[[predef.iterators]]</a>

### Reverse iterators <a id="reverse.iterators">[[reverse.iterators]]</a>

Class template `reverse_iterator` is an iterator adaptor that iterates
from the end of the sequence defined by its underlying iterator to the
beginning of that sequence.

#### Class template `reverse_iterator` <a id="reverse.iterator">[[reverse.iterator]]</a>

``` cpp
namespace std {
  template<class Iterator>
  class reverse_iterator {
  public:
    using iterator_type     = Iterator;
    using iterator_concept  = see below;
    using iterator_category = see below;
    using value_type        = iter_value_t<Iterator>;
    using difference_type   = iter_difference_t<Iterator>;
    using pointer           = typename iterator_traits<Iterator>::pointer;
    using reference         = iter_reference_t<Iterator>;

    constexpr reverse_iterator();
    constexpr explicit reverse_iterator(Iterator x);
    template<class U> constexpr reverse_iterator(const reverse_iterator<U>& u);
    template<class U> constexpr reverse_iterator& operator=(const reverse_iterator<U>& u);

    constexpr Iterator base() const;
    constexpr reference operator*() const;
    constexpr pointer   operator->() const requires see below;

    constexpr reverse_iterator& operator++();
    constexpr reverse_iterator  operator++(int);
    constexpr reverse_iterator& operator--();
    constexpr reverse_iterator  operator--(int);

    constexpr reverse_iterator  operator+ (difference_type n) const;
    constexpr reverse_iterator& operator+=(difference_type n);
    constexpr reverse_iterator  operator- (difference_type n) const;
    constexpr reverse_iterator& operator-=(difference_type n);
    constexpr unspecified operator[](difference_type n) const;

    friend constexpr iter_rvalue_reference_t<Iterator>
      iter_move(const reverse_iterator& i) noexcept(see below);
    template<indirectly_swappable<Iterator> Iterator2>
      friend constexpr void
        iter_swap(const reverse_iterator& x,
                  const reverse_iterator<Iterator2>& y) noexcept(see below);

  protected:
    Iterator current;
  };
}
```

The member *typedef-name* `iterator_concept` denotes

- `random_access_iterator_tag` if `Iterator` models
  `random_access_iterator`, and
- `bidirectional_iterator_tag` otherwise.

The member *typedef-name* `iterator_category` denotes

- `random_access_iterator_tag` if the type
  `iterator_traits<{}Iterator>::iterator_category` models
  `derived_from<random_access_iterator_tag>`, and
- `iterator_traits<{}Iterator>::iterator_category` otherwise.

#### Requirements <a id="reverse.iter.requirements">[[reverse.iter.requirements]]</a>

The template parameter `Iterator` shall either meet the requirements of
a *Cpp17BidirectionalIterator* [[bidirectional.iterators]] or model
`bidirectional_iterator` [[iterator.concept.bidir]].

Additionally, `Iterator` shall either meet the requirements of a
*Cpp17RandomAccessIterator* [[random.access.iterators]] or model
`random_access_iterator` [[iterator.concept.random.access]] if the
definitions of any of the members

- `operator+`, `operator-`, `operator+=`, `operator-=`
  [[reverse.iter.nav]], or
- `operator[]` [[reverse.iter.elem]],

or the non-member operators [[reverse.iter.cmp]]

- `operator<`, `operator>`, `operator<=`, `operator>=`, `operator-`, or
  `operator+` [[reverse.iter.nonmember]]

are instantiated [[temp.inst]].

#### Construction and assignment <a id="reverse.iter.cons">[[reverse.iter.cons]]</a>

``` cpp
constexpr reverse_iterator();
```

*Effects:* Value-initializes `current`. Iterator operations applied to
the resulting iterator have defined behavior if and only if the
corresponding operations are defined on a value-initialized iterator of
type `Iterator`.

``` cpp
constexpr explicit reverse_iterator(Iterator x);
```

*Effects:* Initializes `current` with `x`.

``` cpp
template<class U> constexpr reverse_iterator(const reverse_iterator<U>& u);
```

*Effects:* Initializes `current` with `u.current`.

``` cpp
template<class U>
  constexpr reverse_iterator&
    operator=(const reverse_iterator<U>& u);
```

*Effects:* Assigns `u.base()` to `current`.

*Returns:* `*this`.

#### Conversion <a id="reverse.iter.conv">[[reverse.iter.conv]]</a>

``` cpp
constexpr Iterator base() const;          // explicit
```

*Returns:* `current`.

#### Element access <a id="reverse.iter.elem">[[reverse.iter.elem]]</a>

``` cpp
constexpr reference operator*() const;
```

*Effects:* As if by:

``` cpp
Iterator tmp = current;
return *--tmp;
```

``` cpp
constexpr pointer operator->() const
  requires (is_pointer_v<Iterator> ||
            requires (const Iterator i) { i.operator->(); });
```

*Effects:*

- If `Iterator` is a pointer type, equivalent to:
  `return prev(current);`
- Otherwise, equivalent to: `return prev(current).operator->();`

``` cpp
constexpr unspecified operator[](difference_type n) const;
```

*Returns:* `current[-n-1]`.

#### Navigation <a id="reverse.iter.nav">[[reverse.iter.nav]]</a>

``` cpp
constexpr reverse_iterator operator+(difference_type n) const;
```

*Returns:* `reverse_iterator(current-n)`.

``` cpp
constexpr reverse_iterator operator-(difference_type n) const;
```

*Returns:* `reverse_iterator(current+n)`.

``` cpp
constexpr reverse_iterator& operator++();
```

*Effects:* As if by: `current;`

*Returns:* `*this`.

``` cpp
constexpr reverse_iterator operator++(int);
```

*Effects:* As if by:

``` cpp
reverse_iterator tmp = *this;
--current;
return tmp;
```

``` cpp
constexpr reverse_iterator& operator--();
```

*Effects:* As if by `++current`.

*Returns:* `*this`.

``` cpp
constexpr reverse_iterator operator--(int);
```

*Effects:* As if by:

``` cpp
reverse_iterator tmp = *this;
++current;
return tmp;
```

``` cpp
constexpr reverse_iterator& operator+=(difference_type n);
```

*Effects:* As if by: `current -= n;`

*Returns:* `*this`.

``` cpp
constexpr reverse_iterator& operator-=(difference_type n);
```

*Effects:* As if by: `current += n;`

*Returns:* `*this`.

#### Comparisons <a id="reverse.iter.cmp">[[reverse.iter.cmp]]</a>

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator==(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Constraints:* `x.base() == y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() == y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator!=(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Constraints:* `x.base() != y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() != y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator<(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Constraints:* `x.base() > y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() > y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator>(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Constraints:* `x.base() < y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() < y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator<=(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Constraints:* `x.base() >= y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() >= y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator>=(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Constraints:* `x.base() <= y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() <= y.base()`.

``` cpp
template<class Iterator1, three_way_comparable_with<Iterator1> Iterator2>
  constexpr compare_three_way_result_t<Iterator1, Iterator2>
    operator<=>(const reverse_iterator<Iterator1>& x,
                const reverse_iterator<Iterator2>& y);
```

*Returns:* `y.base() <=> x.base()`.

[*Note 1*: The argument order in the *Returns:* element is reversed
because this is a reverse iterator. — *end note*]

#### Non-member functions <a id="reverse.iter.nonmember">[[reverse.iter.nonmember]]</a>

``` cpp
template<class Iterator1, class Iterator2>
  constexpr auto operator-(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y) -> decltype(y.base() - x.base());
```

*Returns:* `y.base() - x.base()`.

``` cpp
template<class Iterator>
  constexpr reverse_iterator<Iterator> operator+(
    typename reverse_iterator<Iterator>::difference_type n,
    const reverse_iterator<Iterator>& x);
```

*Returns:* `reverse_iterator<Iterator>(x.base() - n)`.

``` cpp
friend constexpr iter_rvalue_reference_t<Iterator>
  iter_move(const reverse_iterator& i) noexcept(see below);
```

*Effects:* Equivalent to:

``` cpp
auto tmp = i.base();
return ranges::iter_move(--tmp);
```

*Remarks:* The expression in `noexcept` is equivalent to:

``` cpp
is_nothrow_copy_constructible_v<Iterator> &&
noexcept(ranges::iter_move(--declval<Iterator&>()))
```

``` cpp
template<indirectly_swappable<Iterator> Iterator2>
  friend constexpr void
    iter_swap(const reverse_iterator& x,
              const reverse_iterator<Iterator2>& y) noexcept(see below);
```

*Effects:* Equivalent to:

``` cpp
auto xtmp = x.base();
auto ytmp = y.base();
ranges::iter_swap(--xtmp, --ytmp);
```

*Remarks:* The expression in `noexcept` is equivalent to:

``` cpp
is_nothrow_copy_constructible_v<Iterator> &&
is_nothrow_copy_constructible_v<Iterator2> &&
noexcept(ranges::iter_swap(--declval<Iterator&>(), --declval<Iterator2&>()))
```

``` cpp
template<class Iterator>
  constexpr reverse_iterator<Iterator> make_reverse_iterator(Iterator i);
```

*Returns:* `reverse_iterator<Iterator>(i)`.

### Insert iterators <a id="insert.iterators">[[insert.iterators]]</a>

To make it possible to deal with insertion in the same way as writing
into an array, a special kind of iterator adaptors, called *insert
iterators*, are provided in the library. With regular iterator classes,

``` cpp
while (first != last) *result++ = *first++;
```

causes a range \[`first`, `last`) to be copied into a range starting
with result. The same code with `result` being an insert iterator will
insert corresponding elements into the container. This device allows all
of the copying algorithms in the library to work in the *insert mode*
instead of the *regular overwrite* mode.

An insert iterator is constructed from a container and possibly one of
its iterators pointing to where insertion takes place if it is neither
at the beginning nor at the end of the container. Insert iterators meet
the requirements of output iterators. `operator*` returns the insert
iterator itself. The assignment `operator=(const T& x)` is defined on
insert iterators to allow writing into them, it inserts `x` right before
where the insert iterator is pointing. In other words, an insert
iterator is like a cursor pointing into the container where the
insertion takes place. `back_insert_iterator` inserts elements at the
end of a container, `front_insert_iterator` inserts elements at the
beginning of a container, and `insert_iterator` inserts elements where
the iterator points to in a container. `back_inserter`,
`front_inserter`, and `inserter` are three functions making the insert
iterators out of a container.

#### Class template `back_insert_iterator` <a id="back.insert.iterator">[[back.insert.iterator]]</a>

``` cpp
namespace std {
  template<class Container>
  class back_insert_iterator {
  protected:
    Container* container = nullptr;

  public:
    using iterator_category = output_iterator_tag;
    using value_type        = void;
    using difference_type   = ptrdiff_t;
    using pointer           = void;
    using reference         = void;
    using container_type    = Container;

    constexpr back_insert_iterator() noexcept = default;
    constexpr explicit back_insert_iterator(Container& x);
    constexpr back_insert_iterator& operator=(const typename Container::value_type& value);
    constexpr back_insert_iterator& operator=(typename Container::value_type&& value);

    constexpr back_insert_iterator& operator*();
    constexpr back_insert_iterator& operator++();
    constexpr back_insert_iterator  operator++(int);
  };
}
```

##### Operations <a id="back.insert.iter.ops">[[back.insert.iter.ops]]</a>

``` cpp
constexpr explicit back_insert_iterator(Container& x);
```

*Effects:* Initializes `container` with `addressof(x)`.

``` cpp
constexpr back_insert_iterator& operator=(const typename Container::value_type& value);
```

*Effects:* As if by: `container->push_back(value);`

*Returns:* `*this`.

``` cpp
constexpr back_insert_iterator& operator=(typename Container::value_type&& value);
```

*Effects:* As if by: `container->push_back(std::move(value));`

*Returns:* `*this`.

``` cpp
constexpr back_insert_iterator& operator*();
```

*Returns:* `*this`.

``` cpp
constexpr back_insert_iterator& operator++();
constexpr back_insert_iterator  operator++(int);
```

*Returns:* `*this`.

#####  `back_inserter` <a id="back.inserter">[[back.inserter]]</a>

``` cpp
template<class Container>
  constexpr back_insert_iterator<Container> back_inserter(Container& x);
```

*Returns:* `back_insert_iterator<Container>(x)`.

#### Class template `front_insert_iterator` <a id="front.insert.iterator">[[front.insert.iterator]]</a>

``` cpp
namespace std {
  template<class Container>
  class front_insert_iterator {
  protected:
    Container* container = nullptr;

  public:
    using iterator_category = output_iterator_tag;
    using value_type        = void;
    using difference_type   = ptrdiff_t;
    using pointer           = void;
    using reference         = void;
    using container_type    = Container;

    constexpr front_insert_iterator() noexcept = default;
    constexpr explicit front_insert_iterator(Container& x);
    constexpr front_insert_iterator& operator=(const typename Container::value_type& value);
    constexpr front_insert_iterator& operator=(typename Container::value_type&& value);

    constexpr front_insert_iterator& operator*();
    constexpr front_insert_iterator& operator++();
    constexpr front_insert_iterator  operator++(int);
  };
}
```

##### Operations <a id="front.insert.iter.ops">[[front.insert.iter.ops]]</a>

``` cpp
constexpr explicit front_insert_iterator(Container& x);
```

*Effects:* Initializes `container` with `addressof(x)`.

``` cpp
constexpr front_insert_iterator& operator=(const typename Container::value_type& value);
```

*Effects:* As if by: `container->push_front(value);`

*Returns:* `*this`.

``` cpp
constexpr front_insert_iterator& operator=(typename Container::value_type&& value);
```

*Effects:* As if by: `container->push_front(std::move(value));`

*Returns:* `*this`.

``` cpp
constexpr front_insert_iterator& operator*();
```

*Returns:* `*this`.

``` cpp
constexpr front_insert_iterator& operator++();
constexpr front_insert_iterator  operator++(int);
```

*Returns:* `*this`.

##### `front_inserter` <a id="front.inserter">[[front.inserter]]</a>

``` cpp
template<class Container>
  constexpr front_insert_iterator<Container> front_inserter(Container& x);
```

*Returns:* `front_insert_iterator<Container>(x)`.

#### Class template `insert_iterator` <a id="insert.iterator">[[insert.iterator]]</a>

``` cpp
namespace std {
  template<class Container>
  class insert_iterator {
  protected:
    Container* container = nullptr;
    ranges::iterator_t<Container> iter = ranges::iterator_t<Container>();

  public:
    using iterator_category = output_iterator_tag;
    using value_type        = void;
    using difference_type   = ptrdiff_t;
    using pointer           = void;
    using reference         = void;
    using container_type    = Container;

    insert_iterator() = default;
    constexpr insert_iterator(Container& x, ranges::iterator_t<Container> i);
    constexpr insert_iterator& operator=(const typename Container::value_type& value);
    constexpr insert_iterator& operator=(typename Container::value_type&& value);

    constexpr insert_iterator& operator*();
    constexpr insert_iterator& operator++();
    constexpr insert_iterator& operator++(int);
  };
}
```

##### Operations <a id="insert.iter.ops">[[insert.iter.ops]]</a>

``` cpp
constexpr insert_iterator(Container& x, ranges::iterator_t<Container> i);
```

*Effects:* Initializes `container` with `addressof(x)` and `iter` with
`i`.

``` cpp
constexpr insert_iterator& operator=(const typename Container::value_type& value);
```

*Effects:* As if by:

``` cpp
iter = container->insert(iter, value);
++iter;
```

*Returns:* `*this`.

``` cpp
constexpr insert_iterator& operator=(typename Container::value_type&& value);
```

*Effects:* As if by:

``` cpp
iter = container->insert(iter, std::move(value));
++iter;
```

*Returns:* `*this`.

``` cpp
constexpr insert_iterator& operator*();
```

*Returns:* `*this`.

``` cpp
constexpr insert_iterator& operator++();
constexpr insert_iterator& operator++(int);
```

*Returns:* `*this`.

##### `inserter` <a id="inserter">[[inserter]]</a>

``` cpp
template<class Container>
  constexpr insert_iterator<Container>
    inserter(Container& x, ranges::iterator_t<Container> i);
```

*Returns:* `insert_iterator<Container>(x, i)`.

### Move iterators and sentinels <a id="move.iterators">[[move.iterators]]</a>

Class template `move_iterator` is an iterator adaptor with the same
behavior as the underlying iterator except that its indirection operator
implicitly converts the value returned by the underlying iterator’s
indirection operator to an rvalue. Some generic algorithms can be called
with move iterators to replace copying with moving.

[*Example 1*:

``` cpp
list<string> s;
// populate the list s
vector<string> v1(s.begin(), s.end());          // copies strings into v1
vector<string> v2(make_move_iterator(s.begin()),
                  make_move_iterator(s.end())); // moves strings into v2
```

— *end example*]

#### Class template `move_iterator` <a id="move.iterator">[[move.iterator]]</a>

``` cpp
namespace std {
  template<class Iterator>
  class move_iterator {
  public:
    using iterator_type     = Iterator;
    using iterator_concept  = input_iterator_tag;
    using iterator_category = see below;
    using value_type        = iter_value_t<Iterator>;
    using difference_type   = iter_difference_t<Iterator>;
    using pointer           = Iterator;
    using reference         = iter_rvalue_reference_t<Iterator>;

    constexpr move_iterator();
    constexpr explicit move_iterator(Iterator i);
    template<class U> constexpr move_iterator(const move_iterator<U>& u);
    template<class U> constexpr move_iterator& operator=(const move_iterator<U>& u);

    constexpr iterator_type base() const &;
    constexpr iterator_type base() &&;
    constexpr reference operator*() const;

    constexpr move_iterator& operator++();
    constexpr auto operator++(int);
    constexpr move_iterator& operator--();
    constexpr move_iterator operator--(int);

    constexpr move_iterator operator+(difference_type n) const;
    constexpr move_iterator& operator+=(difference_type n);
    constexpr move_iterator operator-(difference_type n) const;
    constexpr move_iterator& operator-=(difference_type n);
    constexpr reference operator[](difference_type n) const;

    template<sentinel_for<Iterator> S>
      friend constexpr bool
        operator==(const move_iterator& x, const move_sentinel<S>& y);
    template<sized_sentinel_for<Iterator> S>
      friend constexpr iter_difference_t<Iterator>
        operator-(const move_sentinel<S>& x, const move_iterator& y);
    template<sized_sentinel_for<Iterator> S>
      friend constexpr iter_difference_t<Iterator>
        operator-(const move_iterator& x, const move_sentinel<S>& y);
    friend constexpr iter_rvalue_reference_t<Iterator>
      iter_move(const move_iterator& i)
        noexcept(noexcept(ranges::iter_move(i.current)));
    template<indirectly_swappable<Iterator> Iterator2>
      friend constexpr void
        iter_swap(const move_iterator& x, const move_iterator<Iterator2>& y)
          noexcept(noexcept(ranges::iter_swap(x.current, y.current)));

  private:
    Iterator current;   // exposition only
  };
}
```

The member *typedef-name* `iterator_category` denotes

- `random_access_iterator_tag` if the type
  `iterator_traits<{}Iterator>::iterator_category` models
  `derived_from<random_access_iterator_tag>`, and
- `iterator_traits<{}Iterator>::iterator_category` otherwise.

#### Requirements <a id="move.iter.requirements">[[move.iter.requirements]]</a>

The template parameter `Iterator` shall either meet the
*Cpp17InputIterator* requirements [[input.iterators]] or model
`input_iterator` [[iterator.concept.input]]. Additionally, if any of the
bidirectional traversal functions are instantiated, the template
parameter shall either meet the *Cpp17BidirectionalIterator*
requirements [[bidirectional.iterators]] or model
`bidirectional_iterator` [[iterator.concept.bidir]]. If any of the
random access traversal functions are instantiated, the template
parameter shall either meet the *Cpp17RandomAccessIterator* requirements
[[random.access.iterators]] or model `random_access_iterator`
[[iterator.concept.random.access]].

#### Construction and assignment <a id="move.iter.cons">[[move.iter.cons]]</a>

``` cpp
constexpr move_iterator();
```

*Effects:* Constructs a `move_iterator`, value-initializing `current`.
Iterator operations applied to the resulting iterator have defined
behavior if and only if the corresponding operations are defined on a
value-initialized iterator of type `Iterator`.

``` cpp
constexpr explicit move_iterator(Iterator i);
```

*Effects:* Constructs a `move_iterator`, initializing `current` with
`std::move(i)`.

``` cpp
template<class U> constexpr move_iterator(const move_iterator<U>& u);
```

*Mandates:* `U` is convertible to `Iterator`.

*Effects:* Constructs a `move_iterator`, initializing `current` with
`u.base()`.

``` cpp
template<class U> constexpr move_iterator& operator=(const move_iterator<U>& u);
```

*Mandates:* `U` is convertible to `Iterator`.

*Effects:* Assigns `u.base()` to `current`.

#### Conversion <a id="move.iter.op.conv">[[move.iter.op.conv]]</a>

``` cpp
constexpr Iterator base() const &;
```

*Constraints:* `Iterator` satisfies `copy_constructible`.

*Preconditions:* `Iterator` models `copy_constructible`.

*Returns:* `current`.

``` cpp
constexpr Iterator base() &&;
```

*Returns:* `std::move(current)`.

#### Element access <a id="move.iter.elem">[[move.iter.elem]]</a>

``` cpp
constexpr reference operator*() const;
```

*Effects:* Equivalent to: `return ranges::iter_move(current);`

``` cpp
constexpr reference operator[](difference_type n) const;
```

*Effects:* Equivalent to: `ranges::iter_move(current + n);`

#### Navigation <a id="move.iter.nav">[[move.iter.nav]]</a>

``` cpp
constexpr move_iterator& operator++();
```

*Effects:* As if by `++current`.

*Returns:* `*this`.

``` cpp
constexpr auto operator++(int);
```

*Effects:* If `Iterator` models `forward_iterator`, equivalent to:

``` cpp
move_iterator tmp = *this;
++current;
return tmp;
```

Otherwise, equivalent to `++current`.

``` cpp
constexpr move_iterator& operator--();
```

*Effects:* As if by `current`.

*Returns:* `*this`.

``` cpp
constexpr move_iterator operator--(int);
```

*Effects:* As if by:

``` cpp
move_iterator tmp = *this;
--current;
return tmp;
```

``` cpp
constexpr move_iterator operator+(difference_type n) const;
```

*Returns:* `move_iterator(current + n)`.

``` cpp
constexpr move_iterator& operator+=(difference_type n);
```

*Effects:* As if by: `current += n;`

*Returns:* `*this`.

``` cpp
constexpr move_iterator operator-(difference_type n) const;
```

*Returns:* `move_iterator(current - n)`.

``` cpp
constexpr move_iterator& operator-=(difference_type n);
```

*Effects:* As if by: `current -= n;`

*Returns:* `*this`.

#### Comparisons <a id="move.iter.op.comp">[[move.iter.op.comp]]</a>

``` cpp
template<class Iterator1, class Iterator2>
  constexpr bool operator==(const move_iterator<Iterator1>& x,
                            const move_iterator<Iterator2>& y);
template<sentinel_for<Iterator> S>
  friend constexpr bool operator==(const move_iterator& x,
                                   const move_sentinel<S>& y);
```

*Constraints:* `x.base() == y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() == y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
constexpr bool operator<(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Constraints:* `x.base() < y.base()` is well-formed and convertible to
`bool`.

*Returns:* `x.base() < y.base()`.

``` cpp
template<class Iterator1, class Iterator2>
constexpr bool operator>(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Constraints:* `y.base() < x.base()` is well-formed and convertible to
`bool`.

*Returns:* `y < x`.

``` cpp
template<class Iterator1, class Iterator2>
constexpr bool operator<=(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Constraints:* `y.base() < x.base()` is well-formed and convertible to
`bool`.

*Returns:* `!(y < x)`.

``` cpp
template<class Iterator1, class Iterator2>
constexpr bool operator>=(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Constraints:* `x.base() < y.base()` is well-formed and convertible to
`bool`.

*Returns:* `!(x < y)`.

``` cpp
template<class Iterator1, three_way_comparable_with<Iterator1> Iterator2>
  constexpr compare_three_way_result_t<Iterator1, Iterator2>
    operator<=>(const move_iterator<Iterator1>& x,
                const move_iterator<Iterator2>& y);
```

*Returns:* `x.base() <=> y.base()`.

#### Non-member functions <a id="move.iter.nonmember">[[move.iter.nonmember]]</a>

``` cpp
template<class Iterator1, class Iterator2>
  constexpr auto operator-(const move_iterator<Iterator1>& x,
                           const move_iterator<Iterator2>& y)
    -> decltype(x.base() - y.base());
template<sized_sentinel_for<Iterator> S>
  friend constexpr iter_difference_t<Iterator>
    operator-(const move_sentinel<S>& x, const move_iterator& y);
template<sized_sentinel_for<Iterator> S>
  friend constexpr iter_difference_t<Iterator>
    operator-(const move_iterator& x, const move_sentinel<S>& y);
```

*Returns:* `x.base() - y.base()`.

``` cpp
template<class Iterator>
  constexpr move_iterator<Iterator>
    operator+(iter_difference_t<Iterator> n, const move_iterator<Iterator>& x);
```

*Constraints:* `x + n` is well-formed and has type `Iterator`.

*Returns:* `x + n`.

``` cpp
friend constexpr iter_rvalue_reference_t<Iterator>
  iter_move(const move_iterator& i)
    noexcept(noexcept(ranges::iter_move(i.current)));
```

*Effects:* Equivalent to: `return ranges::iter_move(i.current);`

``` cpp
template<indirectly_swappable<Iterator> Iterator2>
  friend constexpr void
    iter_swap(const move_iterator& x, const move_iterator<Iterator2>& y)
      noexcept(noexcept(ranges::iter_swap(x.current, y.current)));
```

*Effects:* Equivalent to: `ranges::iter_swap(x.current, y.current)`.

``` cpp
template<class Iterator>
constexpr move_iterator<Iterator> make_move_iterator(Iterator i);
```

*Returns:* `move_iterator<Iterator>(std::move(i))`.

#### Class template `move_sentinel` <a id="move.sentinel">[[move.sentinel]]</a>

Class template `move_sentinel` is a sentinel adaptor useful for denoting
ranges together with `move_iterator`. When an input iterator type `I`
and sentinel type `S` model `sentinel_for<S, I>`, `move_sentinel<S>` and
`move_iterator<I>` model
`sentinel_for<move_sentinel<S>, move_iterator<I>{>}` as well.

[*Example 1*:

A `move_if` algorithm is easily implemented with `copy_if` using
`move_iterator` and `move_sentinel`:

``` cpp
template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
         indirect_unary_predicate<I> Pred>
  requires indirectly_movable<I, O>
void move_if(I first, S last, O out, Pred pred) {
  std::ranges::copy_if(move_iterator<I>{first}, move_sentinel<S>{last}, out, pred);
}
```

— *end example*]

``` cpp
namespace std {
  template<semiregular S>
  class move_sentinel {
  public:
    constexpr move_sentinel();
    constexpr explicit move_sentinel(S s);
    template<class S2>
      requires convertible_to<const S2&, S>
        constexpr move_sentinel(const move_sentinel<S2>& s);
    template<class S2>
      requires assignable_from<S&, const S2&>
        constexpr move_sentinel& operator=(const move_sentinel<S2>& s);

    constexpr S base() const;
  private:
    S last;     // exposition only
  };
}
```

#### Operations <a id="move.sent.ops">[[move.sent.ops]]</a>

``` cpp
constexpr move_sentinel();
```

*Effects:* Value-initializes `last`. If
`is_trivially_default_constructible_v<S>` is `true`, then this
constructor is a `constexpr` constructor.

``` cpp
constexpr explicit move_sentinel(S s);
```

*Effects:* Initializes `last` with `std::move(s)`.

``` cpp
template<class S2>
  requires convertible_to<const S2&, S>
    constexpr move_sentinel(const move_sentinel<S2>& s);
```

*Effects:* Initializes `last` with `s.last`.

``` cpp
template<class S2>
  requires assignable_from<S&, const S2&>
    constexpr move_sentinel& operator=(const move_sentinel<S2>& s);
```

*Effects:* Equivalent to: `last = s.last; return *this;`

``` cpp
constexpr S base() const;
```

*Returns:* `last`.

### Common iterators <a id="iterators.common">[[iterators.common]]</a>

#### Class template `common_iterator` <a id="common.iterator">[[common.iterator]]</a>

Class template `common_iterator` is an iterator/sentinel adaptor that is
capable of representing a non-common range of elements (where the types
of the iterator and sentinel differ) as a common range (where they are
the same). It does this by holding either an iterator or a sentinel, and
implementing the equality comparison operators appropriately.

[*Note 1*: The `common_iterator` type is useful for interfacing with
legacy code that expects the begin and end of a range to have the same
type. — *end note*]

[*Example 1*:

``` cpp
template<class ForwardIterator>
void fun(ForwardIterator begin, ForwardIterator end);

list<int> s;
// populate the list s
using CI = common_iterator<counted_iterator<list<int>::iterator>, default_sentinel_t>;
// call fun on a range of 10 ints
fun(CI(counted_iterator(s.begin(), 10)), CI(default_sentinel));
```

— *end example*]

``` cpp
namespace std {
  template<input_or_output_iterator I, sentinel_for<I> S>
    requires (!same_as<I, S> && copyable<I>)
  class common_iterator {
  public:
    constexpr common_iterator() = default;
    constexpr common_iterator(I i);
    constexpr common_iterator(S s);
    template<class I2, class S2>
      requires convertible_to<const I2&, I> && convertible_to<const S2&, S>
        constexpr common_iterator(const common_iterator<I2, S2>& x);

    template<class I2, class S2>
      requires convertible_to<const I2&, I> && convertible_to<const S2&, S> &&
               assignable_from<I&, const I2&> && assignable_from<S&, const S2&>
        common_iterator& operator=(const common_iterator<I2, S2>& x);

    decltype(auto) operator*();
    decltype(auto) operator*() const
      requires dereferenceable<const I>;
    decltype(auto) operator->() const
      requires see below;

    common_iterator& operator++();
    decltype(auto) operator++(int);

    template<class I2, sentinel_for<I> S2>
      requires sentinel_for<S, I2>
    friend bool operator==(
      const common_iterator& x, const common_iterator<I2, S2>& y);
    template<class I2, sentinel_for<I> S2>
      requires sentinel_for<S, I2> && equality_comparable_with<I, I2>
    friend bool operator==(
      const common_iterator& x, const common_iterator<I2, S2>& y);

    template<sized_sentinel_for<I> I2, sized_sentinel_for<I> S2>
      requires sized_sentinel_for<S, I2>
    friend iter_difference_t<I2> operator-(
      const common_iterator& x, const common_iterator<I2, S2>& y);

    friend iter_rvalue_reference_t<I> iter_move(const common_iterator& i)
      noexcept(noexcept(ranges::iter_move(declval<const I&>())))
        requires input_iterator<I>;
    template<indirectly_swappable<I> I2, class S2>
      friend void iter_swap(const common_iterator& x, const common_iterator<I2, S2>& y)
        noexcept(noexcept(ranges::iter_swap(declval<const I&>(), declval<const I2&>())));

  private:
    variant<I, S> v_;   // exposition only
  };

  template<class I, class S>
  struct incrementable_traits<common_iterator<I, S>> {
    using difference_type = iter_difference_t<I>;
  };

  template<input_iterator I, class S>
  struct iterator_traits<common_iterator<I, S>> {
    using iterator_concept = see below;
    using iterator_category = see below;
    using value_type = iter_value_t<I>;
    using difference_type = iter_difference_t<I>;
    using pointer = see below;
    using reference = iter_reference_t<I>;
  };
}
```

#### Associated types <a id="common.iter.types">[[common.iter.types]]</a>

The nested *typedef-name*s of the specialization of `iterator_traits`
for `common_iterator<I, S>` are defined as follows.

- `iterator_concept` denotes `forward_iterator_tag` if `I` models
  `forward_iterator`; otherwise it denotes `input_iterator_tag`.
- `iterator_category` denotes `forward_iterator_tag` if
  `iterator_traits<I>::iterator_category` models
  `derived_from<forward_iterator_tag>`; otherwise it denotes
  `input_iterator_tag`.
- If the expression `a.operator->()` is well-formed, where `a` is an
  lvalue of type `const common_iterator<I, S>`, then `pointer` denotes
  the type of that expression. Otherwise, `pointer` denotes `void`.

#### Constructors and conversions <a id="common.iter.const">[[common.iter.const]]</a>

``` cpp
constexpr common_iterator(I i);
```

*Effects:* Initializes `v_` as if by
`v_{in_place_type<I>, std::move(i)}`.

``` cpp
constexpr common_iterator(S s);
```

*Effects:* Initializes `v_` as if by
`v_{in_place_type<S>, std::move(s)}`.

``` cpp
template<class I2, class S2>
  requires convertible_to<const I2&, I> && convertible_to<const S2&, S>
    constexpr common_iterator(const common_iterator<I2, S2>& x);
```

*Preconditions:* `x.v_.valueless_by_exception()` is `false`.

*Effects:* Initializes `v_` as if by
`v_{in_place_index<`i`>, get<`i`>(x.v_)}`, where i is `x.v_.index()`.

``` cpp
template<class I2, class S2>
  requires convertible_to<const I2&, I> && convertible_to<const S2&, S> &&
           assignable_from<I&, const I2&> && assignable_from<S&, const S2&>
    common_iterator& operator=(const common_iterator<I2, S2>& x);
```

*Preconditions:* `x.v_.valueless_by_exception()` is `false`.

*Effects:* Equivalent to:

- If `v_.index() == x.v_.index()`, then `get<`i`>(v_) = get<`i`>(x.v_)`.
- Otherwise, `v_.emplace<`i`>(get<`i`>(x.v_))`.

where i is `x.v_.index()`.

*Returns:* `*this`

#### Accessors <a id="common.iter.access">[[common.iter.access]]</a>

``` cpp
decltype(auto) operator*();
decltype(auto) operator*() const
  requires dereferenceable<const I>;
```

*Preconditions:* `holds_alternative<I>(v_)`.

*Effects:* Equivalent to: `return *get<I>(v_);`

``` cpp
decltype(auto) operator->() const
  requires see below;
```

The expression in the requires clause is equivalent to:

``` cpp
indirectly_readable<const I> &&
(requires(const I& i) { i.operator->(); } ||
 is_reference_v<iter_reference_t<I>> ||
 constructible_from<iter_value_t<I>, iter_reference_t<I>>)
```

*Preconditions:* `holds_alternative<I>(v_)`.

*Effects:*

- If `I` is a pointer type or if the expression
  `get<I>(v_).operator->()` is well-formed, equivalent to:
  `return get<I>(v_);`
- Otherwise, if `iter_reference_t<I>` is a reference type, equivalent
  to:
  ``` cpp
  auto&& tmp = *get<I>(v_);
  return addressof(tmp);
  ```
- Otherwise, equivalent to: `return `*`proxy`*`(*get<I>(v_));` where
  *proxy* is the exposition-only class:
  ``` cpp
  class proxy {
    iter_value_t<I> keep_;
    proxy(iter_reference_t<I>&& x)
      : keep_(std::move(x)) {}
  public:
    const iter_value_t<I>* operator->() const {
      return addressof(keep_);
    }
  };
  ```

#### Navigation <a id="common.iter.nav">[[common.iter.nav]]</a>

``` cpp
common_iterator& operator++();
```

*Preconditions:* `holds_alternative<I>(v_)`.

*Effects:* Equivalent to `++get<I>(v_)`.

*Returns:* `*this`.

``` cpp
decltype(auto) operator++(int);
```

*Preconditions:* `holds_alternative<I>(v_)`.

*Effects:* If `I` models `forward_iterator`, equivalent to:

``` cpp
common_iterator tmp = *this;
++*this;
return tmp;
```

Otherwise, equivalent to: `return get<I>(v_)++;`

#### Comparisons <a id="common.iter.cmp">[[common.iter.cmp]]</a>

``` cpp
template<class I2, sentinel_for<I> S2>
  requires sentinel_for<S, I2>
friend bool operator==(
  const common_iterator& x, const common_iterator<I2, S2>& y);
```

*Preconditions:* `x.v_.valueless_by_exception()` and
`y.v_.valueless_by_exception()` are each `false`.

*Returns:* `true` if i` == `j, and otherwise
`get<`i`>(x.v_) == get<`j`>(y.v_)`, where i is `x.v_.index()` and j is
`y.v_.index()`.

``` cpp
template<class I2, sentinel_for<I> S2>
  requires sentinel_for<S, I2> && equality_comparable_with<I, I2>
friend bool operator==(
  const common_iterator& x, const common_iterator<I2, S2>& y);
```

*Preconditions:* `x.v_.valueless_by_exception()` and
`y.v_.valueless_by_exception()` are each `false`.

*Returns:* `true` if i and j are each `1`, and otherwise
`get<`i`>(x.v_) == get<`j`>(y.v_)`, where i is `x.v_.index()` and j is
`y.v_.index()`.

``` cpp
template<sized_sentinel_for<I> I2, sized_sentinel_for<I> S2>
  requires sized_sentinel_for<S, I2>
friend iter_difference_t<I2> operator-(
  const common_iterator& x, const common_iterator<I2, S2>& y);
```

*Preconditions:* `x.v_.valueless_by_exception()` and
`y.v_.valueless_by_exception()` are each `false`.

*Returns:* `0` if i and j are each `1`, and otherwise
`get<`i`>(x.v_) - get<`j`>(y.v_)`, where i is `x.v_.index()` and j is
`y.v_.index()`.

#### Customization <a id="common.iter.cust">[[common.iter.cust]]</a>

``` cpp
friend iter_rvalue_reference_t<I> iter_move(const common_iterator& i)
  noexcept(noexcept(ranges::iter_move(declval<const I&>())))
    requires input_iterator<I>;
```

*Preconditions:* `holds_alternative<I>(v_)`.

*Effects:* Equivalent to: `return ranges::iter_move(get<I>(i.v_));`

``` cpp
template<indirectly_swappable<I> I2, class S2>
  friend void iter_swap(const common_iterator& x, const common_iterator<I2, S2>& y)
    noexcept(noexcept(ranges::iter_swap(declval<const I&>(), declval<const I2&>())));
```

*Preconditions:* `holds_alternative<I>(x.v_)` and
`holds_alternative<I2>(y.v_)` are each `true`.

*Effects:* Equivalent to
`ranges::iter_swap(get<I>(x.v_), get<I2>(y.v_))`.

### Default sentinels <a id="default.sentinels">[[default.sentinels]]</a>

``` cpp
namespace std {
  struct default_sentinel_t { };
}
```

Class `default_sentinel_t` is an empty type used to denote the end of a
range. It can be used together with iterator types that know the bound
of their range (e.g., `counted_iterator` [[counted.iterator]]).

### Counted iterators <a id="iterators.counted">[[iterators.counted]]</a>

#### Class template `counted_iterator` <a id="counted.iterator">[[counted.iterator]]</a>

Class template `counted_iterator` is an iterator adaptor with the same
behavior as the underlying iterator except that it keeps track of the
distance to the end of its range. It can be used together with
`default_sentinel` in calls to generic algorithms to operate on a range
of N elements starting at a given position without needing to know the
end position a priori.

[*Example 1*:

``` cpp
list<string> s;
// populate the list s with at least 10 strings
vector<string> v;
// copies 10 strings into v:
ranges::copy(counted_iterator(s.begin(), 10), default_sentinel, back_inserter(v));
```

— *end example*]

Two values `i1` and `i2` of types `counted_iterator<I1>` and
`counted_iterator<I2>` refer to elements of the same sequence if and
only if `next(i1.base(), i1.count())` and `next(i2.base(), i2.count())`
refer to the same (possibly past-the-end) element.

``` cpp
namespace std {
  template<input_or_output_iterator I>
  class counted_iterator {
  public:
    using iterator_type = I;

    constexpr counted_iterator() = default;
    constexpr counted_iterator(I x, iter_difference_t<I> n);
    template<class I2>
      requires convertible_to<const I2&, I>
        constexpr counted_iterator(const counted_iterator<I2>& x);

    template<class I2>
      requires assignable_from<I&, const I2&>
        constexpr counted_iterator& operator=(const counted_iterator<I2>& x);

    constexpr I base() const & requires copy_constructible<I>;
    constexpr I base() &&;
    constexpr iter_difference_t<I> count() const noexcept;
    constexpr decltype(auto) operator*();
    constexpr decltype(auto) operator*() const
      requires dereferenceable<const I>;

    constexpr counted_iterator& operator++();
    decltype(auto) operator++(int);
    constexpr counted_iterator operator++(int)
      requires forward_iterator<I>;
    constexpr counted_iterator& operator--()
      requires bidirectional_iterator<I>;
    constexpr counted_iterator operator--(int)
      requires bidirectional_iterator<I>;

    constexpr counted_iterator operator+(iter_difference_t<I> n) const
      requires random_access_iterator<I>;
    friend constexpr counted_iterator operator+(
      iter_difference_t<I> n, const counted_iterator& x)
        requires random_access_iterator<I>;
    constexpr counted_iterator& operator+=(iter_difference_t<I> n)
      requires random_access_iterator<I>;

    constexpr counted_iterator operator-(iter_difference_t<I> n) const
      requires random_access_iterator<I>;
    template<common_with<I> I2>
      friend constexpr iter_difference_t<I2> operator-(
        const counted_iterator& x, const counted_iterator<I2>& y);
    friend constexpr iter_difference_t<I> operator-(
      const counted_iterator& x, default_sentinel_t);
    friend constexpr iter_difference_t<I> operator-(
      default_sentinel_t, const counted_iterator& y);
    constexpr counted_iterator& operator-=(iter_difference_t<I> n)
      requires random_access_iterator<I>;

    constexpr decltype(auto) operator[](iter_difference_t<I> n) const
      requires random_access_iterator<I>;

    template<common_with<I> I2>
      friend constexpr bool operator==(
        const counted_iterator& x, const counted_iterator<I2>& y);
    friend constexpr bool operator==(
      const counted_iterator& x, default_sentinel_t);

    template<common_with<I> I2>
      friend constexpr strong_ordering operator<=>(
        const counted_iterator& x, const counted_iterator<I2>& y);

    friend constexpr iter_rvalue_reference_t<I> iter_move(const counted_iterator& i)
      noexcept(noexcept(ranges::iter_move(i.current)))
        requires input_iterator<I>;
    template<indirectly_swappable<I> I2>
      friend constexpr void iter_swap(const counted_iterator& x, const counted_iterator<I2>& y)
        noexcept(noexcept(ranges::iter_swap(x.current, y.current)));

  private:
    I current = I();                    // exposition only
    iter_difference_t<I> length = 0;    // exposition only
  };

  template<class I>
  struct incrementable_traits<counted_iterator<I>> {
    using difference_type = iter_difference_t<I>;
  };

  template<input_iterator I>
  struct iterator_traits<counted_iterator<I>> : iterator_traits<I> {
    using pointer = void;
  };
}
```

#### Constructors and conversions <a id="counted.iter.const">[[counted.iter.const]]</a>

``` cpp
constexpr counted_iterator(I i, iter_difference_t<I> n);
```

*Preconditions:* `n >= 0`.

*Effects:* Initializes `current` with `std::move(i)` and `length` with
`n`.

``` cpp
template<class I2>
  requires convertible_to<const I2&, I>
    constexpr counted_iterator(const counted_iterator<I2>& x);
```

*Effects:* Initializes `current` with `x.current` and `length` with
`x.length`.

``` cpp
template<class I2>
  requires assignable_from<I&, const I2&>
    constexpr counted_iterator& operator=(const counted_iterator<I2>& x);
```

*Effects:* Assigns `x.current` to `current` and `x.length` to `length`.

*Returns:* `*this`.

#### Accessors <a id="counted.iter.access">[[counted.iter.access]]</a>

``` cpp
constexpr I base() const & requires copy_constructible<I>;
```

*Effects:* Equivalent to: `return current;`

``` cpp
constexpr I base() &&;
```

*Returns:* `std::move(current)`.

``` cpp
constexpr iter_difference_t<I> count() const noexcept;
```

*Effects:* Equivalent to: `return length;`

#### Element access <a id="counted.iter.elem">[[counted.iter.elem]]</a>

``` cpp
constexpr decltype(auto) operator*();
constexpr decltype(auto) operator*() const
  requires dereferenceable<const I>;
```

*Effects:* Equivalent to: `return *current;`

``` cpp
constexpr decltype(auto) operator[](iter_difference_t<I> n) const
  requires random_access_iterator<I>;
```

*Preconditions:* `n < length`.

*Effects:* Equivalent to: `return current[n];`

#### Navigation <a id="counted.iter.nav">[[counted.iter.nav]]</a>

``` cpp
constexpr counted_iterator& operator++();
```

*Preconditions:* `length > 0`.

*Effects:* Equivalent to:

``` cpp
++current;
--length;
return *this;
```

``` cpp
decltype(auto) operator++(int);
```

*Preconditions:* `length > 0`.

*Effects:* Equivalent to:

``` cpp
--length;
try { return current++; }
catch(...) { ++length; throw; }
```

``` cpp
constexpr counted_iterator operator++(int)
  requires forward_iterator<I>;
```

*Effects:* Equivalent to:

``` cpp
counted_iterator tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr counted_iterator& operator--()
    requires bidirectional_iterator<I>;
```

*Effects:* Equivalent to:

``` cpp
--current;
++length;
return *this;
```

``` cpp
constexpr counted_iterator operator--(int)
    requires bidirectional_iterator<I>;
```

*Effects:* Equivalent to:

``` cpp
counted_iterator tmp = *this;
--*this;
return tmp;
```

``` cpp
constexpr counted_iterator operator+(iter_difference_t<I> n) const
    requires random_access_iterator<I>;
```

*Effects:* Equivalent to:
`return counted_iterator(current + n, length - n);`

``` cpp
friend constexpr counted_iterator operator+(
  iter_difference_t<I> n, const counted_iterator& x)
    requires random_access_iterator<I>;
```

*Effects:* Equivalent to: `return x + n;`

``` cpp
constexpr counted_iterator& operator+=(iter_difference_t<I> n)
    requires random_access_iterator<I>;
```

*Preconditions:* `n <= length`.

*Effects:* Equivalent to:

``` cpp
current += n;
length -= n;
return *this;
```

``` cpp
constexpr counted_iterator operator-(iter_difference_t<I> n) const
    requires random_access_iterator<I>;
```

*Effects:* Equivalent to:
`return counted_iterator(current - n, length + n);`

``` cpp
template<common_with<I> I2>
  friend constexpr iter_difference_t<I2> operator-(
    const counted_iterator& x, const counted_iterator<I2>& y);
```

*Preconditions:* `x` and `y` refer to elements of the same
sequence [[counted.iterator]].

*Effects:* Equivalent to: `return y.length - x.length;`

``` cpp
friend constexpr iter_difference_t<I> operator-(
  const counted_iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to: `return -x.length;`

``` cpp
friend constexpr iter_difference_t<I> operator-(
  default_sentinel_t, const counted_iterator& y);
```

*Effects:* Equivalent to: `return y.length;`

``` cpp
constexpr counted_iterator& operator-=(iter_difference_t<I> n)
  requires random_access_iterator<I>;
```

*Preconditions:* `-n <= length`.

*Effects:* Equivalent to:

``` cpp
current -= n;
length += n;
return *this;
```

#### Comparisons <a id="counted.iter.cmp">[[counted.iter.cmp]]</a>

``` cpp
template<common_with<I> I2>
  friend constexpr bool operator==(
    const counted_iterator& x, const counted_iterator<I2>& y);
```

*Preconditions:* `x` and `y` refer to elements of the same
sequence [[counted.iterator]].

*Effects:* Equivalent to: `return x.length == y.length;`

``` cpp
friend constexpr bool operator==(
  const counted_iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to: `return x.length == 0;`

``` cpp
template<common_with<I> I2>
  friend constexpr strong_ordering operator<=>(
    const counted_iterator& x, const counted_iterator<I2>& y);
```

*Preconditions:* `x` and `y` refer to elements of the same
sequence [[counted.iterator]].

*Effects:* Equivalent to: `return y.length <=> x.length;`

[*Note 1*: The argument order in the *Effects:* element is reversed
because `length` counts down, not up. — *end note*]

#### Customizations <a id="counted.iter.cust">[[counted.iter.cust]]</a>

``` cpp
friend constexpr iter_rvalue_reference_t<I>
  iter_move(const counted_iterator& i)
    noexcept(noexcept(ranges::iter_move(i.current)))
    requires input_iterator<I>;
```

*Effects:* Equivalent to: `return ranges::iter_move(i.current);`

``` cpp
template<indirectly_swappable<I> I2>
  friend constexpr void
    iter_swap(const counted_iterator& x, const counted_iterator<I2>& y)
      noexcept(noexcept(ranges::iter_swap(x.current, y.current)));
```

*Effects:* Equivalent to `ranges::iter_swap(x.current, y.current)`.

### Unreachable sentinel <a id="unreachable.sentinels">[[unreachable.sentinels]]</a>

#### Class `unreachable_sentinel_t` <a id="unreachable.sentinel">[[unreachable.sentinel]]</a>

Class `unreachable_sentinel_t` can be used with any
`weakly_incrementable` type to denote the “upper bound” of an unbounded
interval.

[*Example 1*:

``` cpp
char* p;
// set p to point to a character buffer containing newlines
char* nl = find(p, unreachable_sentinel, '\n');
```

Provided a newline character really exists in the buffer, the use of
`unreachable_sentinel` above potentially makes the call to `find` more
efficient since the loop test against the sentinel does not require a
conditional branch.

— *end example*]

``` cpp
namespace std {
  struct unreachable_sentinel_t {
    template<weakly_incrementable I>
      friend constexpr bool operator==(unreachable_sentinel_t, const I&) noexcept
      { return false; }
  };
}
```

## Stream iterators <a id="stream.iterators">[[stream.iterators]]</a>

To make it possible for algorithmic templates to work directly with
input/output streams, appropriate iterator-like class templates are
provided.

[*Example 1*:

``` cpp
partial_sum(istream_iterator<double, char>(cin),
  istream_iterator<double, char>(),
  ostream_iterator<double, char>(cout, "\n"));
```

reads a file containing floating-point numbers from `cin`, and prints
the partial sums onto `cout`.

— *end example*]

### Class template `istream_iterator` <a id="istream.iterator">[[istream.iterator]]</a>

The class template `istream_iterator` is an input iterator
[[input.iterators]] that reads successive elements from the input stream
for which it was constructed.

``` cpp
namespace std {
  template<class T, class charT = char, class traits = char_traits<charT>,
           class Distance = ptrdiff_t>
  class istream_iterator {
  public:
    using iterator_category = input_iterator_tag;
    using value_type        = T;
    using difference_type   = Distance;
    using pointer           = const T*;
    using reference         = const T&;
    using char_type         = charT;
    using traits_type       = traits;
    using istream_type      = basic_istream<charT,traits>;

    constexpr istream_iterator();
    constexpr istream_iterator(default_sentinel_t);
    istream_iterator(istream_type& s);
    istream_iterator(const istream_iterator& x) = default;
    ~istream_iterator() = default;
    istream_iterator& operator=(const istream_iterator&) = default;

    const T& operator*() const;
    const T* operator->() const;
    istream_iterator& operator++();
    istream_iterator  operator++(int);

    friend bool operator==(const istream_iterator& i, default_sentinel_t);

  private:
    basic_istream<charT,traits>* in_stream; // exposition only
    T value;                                // exposition only
  };
}
```

The type `T` shall meet the *Cpp17DefaultConstructible*,
*Cpp17CopyConstructible*, and *Cpp17CopyAssignable* requirements.

#### Constructors and destructor <a id="istream.iterator.cons">[[istream.iterator.cons]]</a>

``` cpp
constexpr istream_iterator();
constexpr istream_iterator(default_sentinel_t);
```

*Effects:* Constructs the end-of-stream iterator, value-initializing
`value`.

*Ensures:* `in_stream == nullptr` is `true`.

*Remarks:* If the initializer `T()` in the declaration `auto x = T();`
is a constant initializer [[expr.const]], then these constructors are
`constexpr` constructors.

``` cpp
istream_iterator(istream_type& s);
```

*Effects:* Initializes `in_stream` with `addressof(s)`,
value-initializes `value`, and then calls `operator++()`.

``` cpp
istream_iterator(const istream_iterator& x) = default;
```

*Ensures:* `in_stream == x.in_stream` is `true`.

*Remarks:* If `is_trivially_copy_constructible_v<T>` is `true`, then
this constructor is trivial.

``` cpp
~istream_iterator() = default;
```

*Remarks:* If `is_trivially_destructible_v<T>` is `true`, then this
destructor is trivial.

#### Operations <a id="istream.iterator.ops">[[istream.iterator.ops]]</a>

``` cpp
const T& operator*() const;
```

*Preconditions:* `in_stream != nullptr` is `true`.

*Returns:* `value`.

``` cpp
const T* operator->() const;
```

*Preconditions:* `in_stream != nullptr` is `true`.

*Returns:* `addressof(value)`.

``` cpp
istream_iterator& operator++();
```

*Preconditions:* `in_stream != nullptr` is `true`.

*Effects:* Equivalent to:

``` cpp
if (!(*in_stream >> value))
  in_stream = nullptr;
```

*Returns:* `*this`.

``` cpp
istream_iterator operator++(int);
```

*Preconditions:* `in_stream != nullptr` is `true`.

*Effects:* Equivalent to:

``` cpp
istream_iterator tmp = *this;
++*this;
return tmp;
```

``` cpp
template<class T, class charT, class traits, class Distance>
  bool operator==(const istream_iterator<T,charT,traits,Distance>& x,
                  const istream_iterator<T,charT,traits,Distance>& y);
```

*Returns:* `x.in_stream == y.in_stream`.

``` cpp
friend bool operator==(const istream_iterator& i, default_sentinel_t);
```

*Returns:* `!i.in_stream`.

### Class template `ostream_iterator` <a id="ostream.iterator">[[ostream.iterator]]</a>

`ostream_iterator` writes (using `operator<<`) successive elements onto
the output stream from which it was constructed. If it was constructed
with `charT*` as a constructor argument, this string, called a
*delimiter string*, is written to the stream after every `T` is written.

``` cpp
namespace std {
  template<class T, class charT = char, class traits = char_traits<charT>>
  class ostream_iterator {
  public:
    using iterator_category = output_iterator_tag;
    using value_type        = void;
    using difference_type   = ptrdiff_t;
    using pointer           = void;
    using reference         = void;
    using char_type         = charT;
    using traits_type       = traits;
    using ostream_type      = basic_ostream<charT,traits>;

    constexpr ostream_iterator() noexcept = default;
    ostream_iterator(ostream_type& s);
    ostream_iterator(ostream_type& s, const charT* delimiter);
    ostream_iterator(const ostream_iterator& x);
    ~ostream_iterator();
    ostream_iterator& operator=(const ostream_iterator&) = default;
    ostream_iterator& operator=(const T& value);

    ostream_iterator& operator*();
    ostream_iterator& operator++();
    ostream_iterator& operator++(int);

  private:
    basic_ostream<charT,traits>* out_stream = nullptr;          // exposition only
    const charT* delim = nullptr;                               // exposition only
  };
}
```

#### Constructors and destructor <a id="ostream.iterator.cons.des">[[ostream.iterator.cons.des]]</a>

``` cpp
ostream_iterator(ostream_type& s);
```

*Effects:* Initializes `out_stream` with `addressof(s)` and `delim` with
`nullptr`.

``` cpp
ostream_iterator(ostream_type& s, const charT* delimiter);
```

*Effects:* Initializes `out_stream` with `addressof(s)` and `delim` with
`delimiter`.

#### Operations <a id="ostream.iterator.ops">[[ostream.iterator.ops]]</a>

``` cpp
ostream_iterator& operator=(const T& value);
```

*Effects:* As if by:

``` cpp
*out_stream << value;
if (delim)
  *out_stream << delim;
return *this;
```

``` cpp
ostream_iterator& operator*();
```

*Returns:* `*this`.

``` cpp
ostream_iterator& operator++();
ostream_iterator& operator++(int);
```

*Returns:* `*this`.

### Class template `istreambuf_iterator` <a id="istreambuf.iterator">[[istreambuf.iterator]]</a>

The class template `istreambuf_iterator` defines an input iterator
[[input.iterators]] that reads successive *characters* from the
streambuf for which it was constructed. `operator*` provides access to
the current input character, if any. Each time `operator++` is
evaluated, the iterator advances to the next input character. If the end
of stream is reached (`streambuf_type::sgetc()` returns
`traits::eof()`), the iterator becomes equal to the *end-of-stream*
iterator value. The default constructor `istreambuf_iterator()` and the
constructor `istreambuf_iterator(nullptr)` both construct an
end-of-stream iterator object suitable for use as an end-of-range. All
specializations of `istreambuf_iterator` shall have a trivial copy
constructor, a `constexpr` default constructor, and a trivial
destructor.

The result of `operator*()` on an end-of-stream iterator is undefined.
For any other iterator value a `char_type` value is returned. It is
impossible to assign a character via an input iterator.

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class istreambuf_iterator {
  public:
    using iterator_category = input_iterator_tag;
    using value_type        = charT;
    using difference_type   = typename traits::off_type;
    using pointer           = unspecified;
    using reference         = charT;
    using char_type         = charT;
    using traits_type       = traits;
    using int_type          = typename traits::int_type;
    using streambuf_type    = basic_streambuf<charT,traits>;
    using istream_type      = basic_istream<charT,traits>;

    class proxy;                          // exposition only

    constexpr istreambuf_iterator() noexcept;
    constexpr istreambuf_iterator(default_sentinel_t) noexcept;
    istreambuf_iterator(const istreambuf_iterator&) noexcept = default;
    ~istreambuf_iterator() = default;
    istreambuf_iterator(istream_type& s) noexcept;
    istreambuf_iterator(streambuf_type* s) noexcept;
    istreambuf_iterator(const proxy& p) noexcept;
    istreambuf_iterator& operator=(const istreambuf_iterator&) noexcept = default;
    charT operator*() const;
    istreambuf_iterator& operator++();
    proxy operator++(int);
    bool equal(const istreambuf_iterator& b) const;

    friend bool operator==(const istreambuf_iterator& i, default_sentinel_t s);

  private:
    streambuf_type* sbuf_;              // exposition only
  };
}
```

#### Class `istreambuf_iterator::proxy` <a id="istreambuf.iterator.proxy">[[istreambuf.iterator.proxy]]</a>

Class `istreambuf_iterator<charT,traits>::proxy` is for exposition only.
An implementation is permitted to provide equivalent functionality
without providing a class with this name. Class
`istreambuf_iterator<charT, traits>::proxy` provides a temporary
placeholder as the return value of the post-increment operator
(`operator++`). It keeps the character pointed to by the previous value
of the iterator for some possible future access to get the character.

``` cpp
namespace std {
  template<class charT, class traits>
  class istreambuf_iterator<charT, traits>::proxy { // exposition only
    charT keep_;
    basic_streambuf<charT,traits>* sbuf_;
    proxy(charT c, basic_streambuf<charT,traits>* sbuf)
      : keep_(c), sbuf_(sbuf) { }
  public:
    charT operator*() { return keep_; }
  };
}
```

#### Constructors <a id="istreambuf.iterator.cons">[[istreambuf.iterator.cons]]</a>

For each `istreambuf_iterator` constructor in this subclause, an
end-of-stream iterator is constructed if and only if the exposition-only
member `sbuf_` is initialized with a null pointer value.

``` cpp
constexpr istreambuf_iterator() noexcept;
constexpr istreambuf_iterator(default_sentinel_t) noexcept;
```

*Effects:* Initializes `sbuf_` with `nullptr`.

``` cpp
istreambuf_iterator(istream_type& s) noexcept;
```

*Effects:* Initializes `sbuf_` with `s.rdbuf()`.

``` cpp
istreambuf_iterator(streambuf_type* s) noexcept;
```

*Effects:* Initializes `sbuf_` with `s`.

``` cpp
istreambuf_iterator(const proxy& p) noexcept;
```

*Effects:* Initializes `sbuf_` with `p.sbuf_`.

#### Operations <a id="istreambuf.iterator.ops">[[istreambuf.iterator.ops]]</a>

``` cpp
charT operator*() const;
```

*Returns:* The character obtained via the `streambuf` member
`sbuf_->sgetc()`.

``` cpp
istreambuf_iterator& operator++();
```

*Effects:* As if by `sbuf_->sbumpc()`.

*Returns:* `*this`.

``` cpp
proxy operator++(int);
```

*Returns:* *`proxy`*`(sbuf_->sbumpc(), sbuf_)`.

``` cpp
bool equal(const istreambuf_iterator& b) const;
```

*Returns:* `true` if and only if both iterators are at end-of-stream, or
neither is at end-of-stream, regardless of what `streambuf` object they
use.

``` cpp
template<class charT, class traits>
  bool operator==(const istreambuf_iterator<charT,traits>& a,
                  const istreambuf_iterator<charT,traits>& b);
```

*Returns:* `a.equal(b)`.

``` cpp
friend bool operator==(const istreambuf_iterator& i, default_sentinel_t s);
```

*Returns:* `i.equal(s)`.

### Class template `ostreambuf_iterator` <a id="ostreambuf.iterator">[[ostreambuf.iterator]]</a>

The class template `ostreambuf_iterator` writes successive *characters*
onto the output stream from which it was constructed.

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT>>
  class ostreambuf_iterator {
  public:
    using iterator_category = output_iterator_tag;
    using value_type        = void;
    using difference_type   = ptrdiff_t;
    using pointer           = void;
    using reference         = void;
    using char_type         = charT;
    using traits_type       = traits;
    using streambuf_type    = basic_streambuf<charT,traits>;
    using ostream_type      = basic_ostream<charT,traits>;

    constexpr ostreambuf_iterator() noexcept = default;
    ostreambuf_iterator(ostream_type& s) noexcept;
    ostreambuf_iterator(streambuf_type* s) noexcept;
    ostreambuf_iterator& operator=(charT c);

    ostreambuf_iterator& operator*();
    ostreambuf_iterator& operator++();
    ostreambuf_iterator& operator++(int);
    bool failed() const noexcept;

  private:
    streambuf_type* sbuf_ = nullptr;    // exposition only
  };
}
```

#### Constructors <a id="ostreambuf.iter.cons">[[ostreambuf.iter.cons]]</a>

``` cpp
ostreambuf_iterator(ostream_type& s) noexcept;
```

*Preconditions:* `s.rdbuf()` is not a null pointer.

*Effects:* Initializes `sbuf_` with `s.rdbuf()`.

``` cpp
ostreambuf_iterator(streambuf_type* s) noexcept;
```

*Preconditions:* `s` is not a null pointer.

*Effects:* Initializes `sbuf_` with `s`.

#### Operations <a id="ostreambuf.iter.ops">[[ostreambuf.iter.ops]]</a>

``` cpp
ostreambuf_iterator& operator=(charT c);
```

*Effects:* If `failed()` yields `false`, calls `sbuf_->sputc(c)`;
otherwise has no effect.

*Returns:* `*this`.

``` cpp
ostreambuf_iterator& operator*();
```

*Returns:* `*this`.

``` cpp
ostreambuf_iterator& operator++();
ostreambuf_iterator& operator++(int);
```

*Returns:* `*this`.

``` cpp
bool failed() const noexcept;
```

*Returns:* `true` if in any prior use of member `operator=`, the call to
`sbuf_->sputc()` returned `traits::eof()`; or `false` otherwise.

## Range access <a id="iterator.range">[[iterator.range]]</a>

In addition to being available via inclusion of the `<iterator>` header,
the function templates in [[iterator.range]] are available when any of
the following headers are included: `<array>`, `<deque>`,
`<forward_list>`, `<list>`, `<map>`, `<regex>`, `<set>`, `<span>`,
`<string>`, `<string_view>`, `<unordered_map>`, `<unordered_set>`, and
`<vector>`. Each of these templates is a designated customization point
[[namespace.std]].

``` cpp
template<class C> constexpr auto begin(C& c) -> decltype(c.begin());
template<class C> constexpr auto begin(const C& c) -> decltype(c.begin());
```

*Returns:* `c.begin()`.

``` cpp
template<class C> constexpr auto end(C& c) -> decltype(c.end());
template<class C> constexpr auto end(const C& c) -> decltype(c.end());
```

*Returns:* `c.end()`.

``` cpp
template<class T, size_t N> constexpr T* begin(T (&array)[N]) noexcept;
```

*Returns:* `array`.

``` cpp
template<class T, size_t N> constexpr T* end(T (&array)[N]) noexcept;
```

*Returns:* `array + N`.

``` cpp
template<class C> constexpr auto cbegin(const C& c) noexcept(noexcept(std::begin(c)))
  -> decltype(std::begin(c));
```

*Returns:* `std::begin(c)`.

``` cpp
template<class C> constexpr auto cend(const C& c) noexcept(noexcept(std::end(c)))
  -> decltype(std::end(c));
```

*Returns:* `std::end(c)`.

``` cpp
template<class C> constexpr auto rbegin(C& c) -> decltype(c.rbegin());
template<class C> constexpr auto rbegin(const C& c) -> decltype(c.rbegin());
```

*Returns:* `c.rbegin()`.

``` cpp
template<class C> constexpr auto rend(C& c) -> decltype(c.rend());
template<class C> constexpr auto rend(const C& c) -> decltype(c.rend());
```

*Returns:* `c.rend()`.

``` cpp
template<class T, size_t N> constexpr reverse_iterator<T*> rbegin(T (&array)[N]);
```

*Returns:* `reverse_iterator<T*>(array + N)`.

``` cpp
template<class T, size_t N> constexpr reverse_iterator<T*> rend(T (&array)[N]);
```

*Returns:* `reverse_iterator<T*>(array)`.

``` cpp
template<class E> constexpr reverse_iterator<const E*> rbegin(initializer_list<E> il);
```

*Returns:* `reverse_iterator<const E*>(il.end())`.

``` cpp
template<class E> constexpr reverse_iterator<const E*> rend(initializer_list<E> il);
```

*Returns:* `reverse_iterator<const E*>(il.begin())`.

``` cpp
template<class C> constexpr auto crbegin(const C& c) -> decltype(std::rbegin(c));
```

*Returns:* `std::rbegin(c)`.

``` cpp
template<class C> constexpr auto crend(const C& c) -> decltype(std::rend(c));
```

*Returns:* `std::rend(c)`.

``` cpp
template<class C> constexpr auto size(const C& c) -> decltype(c.size());
```

*Returns:* `c.size()`.

``` cpp
template<class T, size_t N> constexpr size_t size(const T (&array)[N]) noexcept;
```

*Returns:* `N`.

``` cpp
template<class C> constexpr auto ssize(const C& c)
  -> common_type_t<ptrdiff_t, make_signed_t<decltype(c.size())>>;
```

*Effects:* Equivalent to:

``` cpp
return static_cast<common_type_t<ptrdiff_t, make_signed_t<decltype(c.size())>>>(c.size());
```

``` cpp
template<class T, ptrdiff_t N> constexpr ptrdiff_t ssize(const T (&array)[N]) noexcept;
```

*Returns:* `N`.

``` cpp
template<class C> [[nodiscard]] constexpr auto empty(const C& c) -> decltype(c.empty());
```

*Returns:* `c.empty()`.

``` cpp
template<class T, size_t N> [[nodiscard]] constexpr bool empty(const T (&array)[N]) noexcept;
```

*Returns:* `false`.

``` cpp
template<class E> [[nodiscard]] constexpr bool empty(initializer_list<E> il) noexcept;
```

*Returns:* `il.size() == 0`.

``` cpp
template<class C> constexpr auto data(C& c) -> decltype(c.data());
template<class C> constexpr auto data(const C& c) -> decltype(c.data());
```

*Returns:* `c.data()`.

``` cpp
template<class T, size_t N> constexpr T* data(T (&array)[N]) noexcept;
```

*Returns:* `array`.

``` cpp
template<class E> constexpr const E* data(initializer_list<E> il) noexcept;
```

*Returns:* `il.begin()`.

<!-- Section link definitions -->
[alg.req]: #alg.req
[alg.req.general]: #alg.req.general
[alg.req.ind.cmp]: #alg.req.ind.cmp
[alg.req.ind.copy]: #alg.req.ind.copy
[alg.req.ind.move]: #alg.req.ind.move
[alg.req.ind.swap]: #alg.req.ind.swap
[alg.req.mergeable]: #alg.req.mergeable
[alg.req.permutable]: #alg.req.permutable
[alg.req.sortable]: #alg.req.sortable
[back.insert.iter.ops]: #back.insert.iter.ops
[back.insert.iterator]: #back.insert.iterator
[back.inserter]: #back.inserter
[bidirectional.iterators]: #bidirectional.iterators
[common.iter.access]: #common.iter.access
[common.iter.cmp]: #common.iter.cmp
[common.iter.const]: #common.iter.const
[common.iter.cust]: #common.iter.cust
[common.iter.nav]: #common.iter.nav
[common.iter.types]: #common.iter.types
[common.iterator]: #common.iterator
[counted.iter.access]: #counted.iter.access
[counted.iter.cmp]: #counted.iter.cmp
[counted.iter.const]: #counted.iter.const
[counted.iter.cust]: #counted.iter.cust
[counted.iter.elem]: #counted.iter.elem
[counted.iter.nav]: #counted.iter.nav
[counted.iterator]: #counted.iterator
[default.sentinels]: #default.sentinels
[forward.iterators]: #forward.iterators
[front.insert.iter.ops]: #front.insert.iter.ops
[front.insert.iterator]: #front.insert.iterator
[front.inserter]: #front.inserter
[incrementable.traits]: #incrementable.traits
[indirectcallable]: #indirectcallable
[indirectcallable.general]: #indirectcallable.general
[indirectcallable.indirectinvocable]: #indirectcallable.indirectinvocable
[input.iterators]: #input.iterators
[insert.iter.ops]: #insert.iter.ops
[insert.iterator]: #insert.iterator
[insert.iterators]: #insert.iterators
[inserter]: #inserter
[istream.iterator]: #istream.iterator
[istream.iterator.cons]: #istream.iterator.cons
[istream.iterator.ops]: #istream.iterator.ops
[istreambuf.iterator]: #istreambuf.iterator
[istreambuf.iterator.cons]: #istreambuf.iterator.cons
[istreambuf.iterator.ops]: #istreambuf.iterator.ops
[istreambuf.iterator.proxy]: #istreambuf.iterator.proxy
[iterator.assoc.types]: #iterator.assoc.types
[iterator.concept.bidir]: #iterator.concept.bidir
[iterator.concept.contiguous]: #iterator.concept.contiguous
[iterator.concept.forward]: #iterator.concept.forward
[iterator.concept.inc]: #iterator.concept.inc
[iterator.concept.input]: #iterator.concept.input
[iterator.concept.iterator]: #iterator.concept.iterator
[iterator.concept.output]: #iterator.concept.output
[iterator.concept.random.access]: #iterator.concept.random.access
[iterator.concept.readable]: #iterator.concept.readable
[iterator.concept.sentinel]: #iterator.concept.sentinel
[iterator.concept.sizedsentinel]: #iterator.concept.sizedsentinel
[iterator.concept.winc]: #iterator.concept.winc
[iterator.concept.writable]: #iterator.concept.writable
[iterator.concepts]: #iterator.concepts
[iterator.concepts.general]: #iterator.concepts.general
[iterator.cpp17]: #iterator.cpp17
[iterator.cust]: #iterator.cust
[iterator.cust.move]: #iterator.cust.move
[iterator.cust.swap]: #iterator.cust.swap
[iterator.iterators]: #iterator.iterators
[iterator.operations]: #iterator.operations
[iterator.primitives]: #iterator.primitives
[iterator.range]: #iterator.range
[iterator.requirements]: #iterator.requirements
[iterator.requirements.general]: #iterator.requirements.general
[iterator.synopsis]: #iterator.synopsis
[iterator.traits]: #iterator.traits
[iterators]: #iterators
[iterators.common]: #iterators.common
[iterators.counted]: #iterators.counted
[iterators.general]: #iterators.general
[move.iter.cons]: #move.iter.cons
[move.iter.elem]: #move.iter.elem
[move.iter.nav]: #move.iter.nav
[move.iter.nonmember]: #move.iter.nonmember
[move.iter.op.comp]: #move.iter.op.comp
[move.iter.op.conv]: #move.iter.op.conv
[move.iter.requirements]: #move.iter.requirements
[move.iterator]: #move.iterator
[move.iterators]: #move.iterators
[move.sent.ops]: #move.sent.ops
[move.sentinel]: #move.sentinel
[ostream.iterator]: #ostream.iterator
[ostream.iterator.cons.des]: #ostream.iterator.cons.des
[ostream.iterator.ops]: #ostream.iterator.ops
[ostreambuf.iter.cons]: #ostreambuf.iter.cons
[ostreambuf.iter.ops]: #ostreambuf.iter.ops
[ostreambuf.iterator]: #ostreambuf.iterator
[output.iterators]: #output.iterators
[predef.iterators]: #predef.iterators
[projected]: #projected
[random.access.iterators]: #random.access.iterators
[range.iter.op.advance]: #range.iter.op.advance
[range.iter.op.distance]: #range.iter.op.distance
[range.iter.op.next]: #range.iter.op.next
[range.iter.op.prev]: #range.iter.op.prev
[range.iter.ops]: #range.iter.ops
[readable.traits]: #readable.traits
[reverse.iter.cmp]: #reverse.iter.cmp
[reverse.iter.cons]: #reverse.iter.cons
[reverse.iter.conv]: #reverse.iter.conv
[reverse.iter.elem]: #reverse.iter.elem
[reverse.iter.nav]: #reverse.iter.nav
[reverse.iter.nonmember]: #reverse.iter.nonmember
[reverse.iter.requirements]: #reverse.iter.requirements
[reverse.iterator]: #reverse.iterator
[reverse.iterators]: #reverse.iterators
[std.iterator.tags]: #std.iterator.tags
[stream.iterators]: #stream.iterators
[unreachable.sentinel]: #unreachable.sentinel
[unreachable.sentinels]: #unreachable.sentinels

<!-- Link reference definitions -->
[basic.fundamental]: basic.md#basic.fundamental
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.lval]: expr.md#basic.lval
[bidirectional.iterators]: #bidirectional.iterators
[bidirectionaliterator]: #bidirectionaliterator
[concept.swappable]: concepts.md#concept.swappable
[concept.totallyordered]: concepts.md#concept.totallyordered
[concepts.object]: concepts.md#concepts.object
[containers]: containers.md#containers
[counted.iterator]: #counted.iterator
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.equalitycomparable]: #cpp17.equalitycomparable
[customization.point.object]: library.md#customization.point.object
[defns.projection]: #defns.projection
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[forward.iterators]: #forward.iterators
[forwarditerator]: #forwarditerator
[func.def]: utilities.md#func.def
[input.iterators]: #input.iterators
[inputiterator]: #inputiterator
[iostream.format]: input.md#iostream.format
[iterator]: #iterator
[iterator.concept.bidir]: #iterator.concept.bidir
[iterator.concept.contiguous]: #iterator.concept.contiguous
[iterator.concept.forward]: #iterator.concept.forward
[iterator.concept.input]: #iterator.concept.input
[iterator.concept.iterator]: #iterator.concept.iterator
[iterator.concept.output]: #iterator.concept.output
[iterator.concept.random.access]: #iterator.concept.random.access
[iterator.concept.readable]: #iterator.concept.readable
[iterator.concept.sentinel]: #iterator.concept.sentinel
[iterator.concept.winc]: #iterator.concept.winc
[iterator.concept.writable]: #iterator.concept.writable
[iterator.concepts]: #iterator.concepts
[iterator.iterators]: #iterator.iterators
[iterator.primitives]: #iterator.primitives
[iterator.range]: #iterator.range
[iterator.requirements]: #iterator.requirements
[iterator.synopsis]: #iterator.synopsis
[iterator.traits]: #iterator.traits
[iterators.relations]: #iterators.relations
[iterators.summary]: #iterators.summary
[lib.types.movedfrom]: library.md#lib.types.movedfrom
[namespace.std]: library.md#namespace.std
[output.iterators]: #output.iterators
[outputiterator]: #outputiterator
[predef.iterators]: #predef.iterators
[random.access.iterators]: #random.access.iterators
[randomaccessiterator]: #randomaccessiterator
[range.cmp]: utilities.md#range.cmp
[ranges]: ranges.md#ranges
[reverse.iter.cmp]: #reverse.iter.cmp
[reverse.iter.elem]: #reverse.iter.elem
[reverse.iter.nav]: #reverse.iter.nav
[reverse.iter.nonmember]: #reverse.iter.nonmember
[stream.buffers]: input.md#stream.buffers
[stream.iterators]: #stream.iterators
[swappable.requirements]: library.md#swappable.requirements
[temp.deduct]: temp.md#temp.deduct
[temp.func.order]: temp.md#temp.func.order
[temp.inst]: temp.md#temp.inst
[utility.arg.requirements]: library.md#utility.arg.requirements

[^1]: The sentinel denoting the end of a range may have the same type as
    the iterator denoting the beginning of the range, or a different
    type.

[^2]: This definition applies to pointers, since pointers are iterators.
    The effect of dereferencing an iterator that has been invalidated is
    undefined.
