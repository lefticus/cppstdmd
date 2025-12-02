# Iterators library <a id="iterators">[[iterators]]</a>

## General <a id="iterators.general">[[iterators.general]]</a>

This Clause describes components that C++programs may use to perform
iterations over containers (Clause [[containers]]), streams (
[[iostream.format]]), and stream buffers ([[stream.buffers]]).

The following subclauses describe iterator requirements, and components
for iterator primitives, predefined iterators, and stream iterators, as
summarized in Table  [[tab:iterators.lib.summary]].

**Table: Iterators library summary** <a id="tab:iterators.lib.summary">[tab:iterators.lib.summary]</a>

| Subclause                 |                      | Header       |
| ------------------------- | -------------------- | ------------ |
| [[iterator.requirements]] | Requirements         |              |
| [[iterator.primitives]]   | Iterator primitives  | `<iterator>` |
| [[predef.iterators]]      | Predefined iterators |              |
| [[stream.iterators]]      | Stream iterators     |              |


## Iterator requirements <a id="iterator.requirements">[[iterator.requirements]]</a>

### In general <a id="iterator.requirements.general">[[iterator.requirements.general]]</a>

Iterators are a generalization of pointers that allow a C++program to
work with different data structures (containers) in a uniform manner. To
be able to construct template algorithms that work correctly and
efficiently on different types of data structures, the library
formalizes not just the interfaces but also the semantics and complexity
assumptions of iterators. All input iterators `i` support the expression
`*i`, resulting in a value of some object type `T`, called the *value
type* of the iterator. All output iterators support the expression
`*i = o` where `o` is a value of some type that is in the set of types
that are *writable* to the particular iterator type of `i`. All
iterators `i` for which the expression `(*i).m` is well-defined, support
the expression `i->m` with the same semantics as `(*i).m`. For every
iterator type `X` for which equality is defined, there is a
corresponding signed integer type called the *difference type* of the
iterator.

Since iterators are an abstraction of pointers, their semantics is a
generalization of most of the semantics of pointers in C++. This ensures
that every function template that takes iterators works as well with
regular pointers. This International Standard defines five categories of
iterators, according to the operations defined on them: *input
iterators*, *output iterators*, *forward iterators*, *bidirectional
iterators* and *random access iterators*, as shown in Table 
[[tab:iterators.relations]].

**Table: Relations among iterator categories** <a id="tab:iterators.relations">[tab:iterators.relations]</a>

|                   |                                 |                           |                          |
| ----------------- | ------------------------------- | ------------------------- | ------------------------ |
| **Random Access** | $\rightarrow$ **Bidirectional** | $\rightarrow$ **Forward** | $\rightarrow$ **Input**  |
|                   |                                 |                           | $\rightarrow$ **Output** |


Forward iterators satisfy all the requirements of input iterators and
can be used whenever an input iterator is specified; Bidirectional
iterators also satisfy all the requirements of forward iterators and can
be used whenever a forward iterator is specified; Random access
iterators also satisfy all the requirements of bidirectional iterators
and can be used whenever a bidirectional iterator is specified.

Iterators that further satisfy the requirements of output iterators are
called *mutable iterator*s. Nonmutable iterators are referred to as
*constant iterator*s.

Just as a regular pointer to an array guarantees that there is a pointer
value pointing past the last element of the array, so for any iterator
type there is an iterator value that points past the last element of a
corresponding sequence. These values are called *past-the-end* values.
Values of an iterator `i` for which the expression `*i` is defined are
called *dereferenceable*. The library never assumes that past-the-end
values are dereferenceable. Iterators can also have singular values that
are not associated with any sequence. After the declaration of an
uninitialized pointer `x` (as with `int* x;`), `x` must always be
assumed to have a singular value of a pointer. Results of most
expressions are undefined for singular values; the only exceptions are
destroying an iterator that holds a singular value, the assignment of a
non-singular value to an iterator that holds a singular value, and, for
iterators that satisfy the `DefaultConstructible` requirements, using a
value-initialized iterator as the source of a copy or move operation.
This guarantee is not offered for default initialization, although the
distinction only matters for types with trivial default constructors
such as pointers or aggregates holding pointers. In these cases the
singular value is overwritten the same way as any other value.
Dereferenceable values are always non-singular.

An iterator `j` is called *reachable* from an iterator `i` if and only
if there is a finite sequence of applications of the expression `++i`
that makes `i == j`. If `j` is reachable from `i`, they refer to
elements of the same sequence.

Most of the library’s algorithmic templates that operate on data
structures have interfaces that use ranges. A *range* is a pair of
iterators that designate the beginning and end of the computation. A
range \[`i`, `i`) is an empty range; in general, a range \[`i`, `j`)
refers to the elements in the data structure starting with the element
pointed to by `i` and up to but not including the element pointed to by
`j`. Range \[`i`, `j`) is valid if and only if `j` is reachable from
`i`. The result of the application of functions in the library to
invalid ranges is undefined.

All the categories of iterators require only those functions that are
realizable for a given category in constant time (amortized). Therefore,
requirement tables for the iterators do not have a complexity column.

Destruction of an iterator may invalidate pointers and references
previously obtained from that iterator.

An *invalid* iterator is an iterator that may be singular.[^1]

In the following sections, `a` and `b` denote values of type `X` or
`const X`, `difference_type` and `reference` refer to the types
`iterator_traits<X>::difference_type` and
`iterator_traits<X>::reference`, respectively, `n` denotes a value of
`difference_type`, `u`, `tmp`, and `m` denote identifiers, `r` denotes a
value of `X&`, `t` denotes a value of value type `T`, `o` denotes a
value of some type that is writable to the output iterator. For an
iterator type `X` there must be an instantiation of
`iterator_traits<X>` ([[iterator.traits]]).

### Iterator <a id="iterator.iterators">[[iterator.iterators]]</a>

The `Iterator` requirements form the basis of the iterator concept
taxonomy; every iterator satisfies the `Iterator` requirements. This set
of requirements specifies operations for dereferencing and incrementing
an iterator. Most algorithms will require additional operations to
read ([[input.iterators]]) or write ([[output.iterators]]) values, or
to provide a richer set of iterator movements ([[forward.iterators]],
[[bidirectional.iterators]], [[random.access.iterators]]).)

A type `X` satisfies the `Iterator` requirements if:

- `X` satisfies the `CopyConstructible`, `CopyAssignable`, and
  `Destructible` requirements ([[utility.arg.requirements]]) and
  lvalues of type `X` are swappable ([[swappable.requirements]]), and
- the expressions in Table  [[tab:iterator.requirements]] are valid and
  have the indicated semantics.

### Input iterators <a id="input.iterators">[[input.iterators]]</a>

A class or pointer type `X` satisfies the requirements of an input
iterator for the value type `T` if X satisfies the `Iterator` (
[[iterator.iterators]]) and `EqualityComparable` (Table 
[[equalitycomparable]]) requirements and the expressions in Table 
[[tab:iterator.input.requirements]] are valid and have the indicated
semantics.

In Table  [[tab:iterator.input.requirements]], the term *the domain of
`==`* is used in the ordinary mathematical sense to denote the set of
values over which `==` is (required to be) defined. This set can change
over time. Each algorithm places additional requirements on the domain
of `==` for the iterator values it uses. These requirements can be
inferred from the uses that algorithm makes of `==` and `!=`. the call
`find(a,b,x)` is defined only if the value of `a` has the property *p*
defined as follows: `b` has property *p* and a value `i` has property
*p* if `(*i==x)` or if `(*i!=x` and `++i` has property `p`).

For input iterators, `a == b` does not imply `++a == ++b`. (Equality
does not guarantee the substitution property or referential
transparency.) Algorithms on input iterators should never attempt to
pass through the same iterator twice. They should be *single pass*
algorithms. Value type T is not required to be a `CopyAssignable` type
(Table  [[copyassignable]]). These algorithms can be used with istreams
as the source of the input data through the `istream_iterator` class
template.

### Output iterators <a id="output.iterators">[[output.iterators]]</a>

A class or pointer type `X` satisfies the requirements of an output
iterator if `X` satisfies the `Iterator` requirements (
[[iterator.iterators]]) and the expressions in Table 
[[tab:iterator.output.requirements]] are valid and have the indicated
semantics.

The only valid use of an `operator*` is on the left side of the
assignment statement. *Assignment through the same value of the iterator
happens only once.* Algorithms on output iterators should never attempt
to pass through the same iterator twice. They should be *single pass*
algorithms. Equality and inequality might not be defined. Algorithms
that take output iterators can be used with ostreams as the destination
for placing data through the `ostream_iterator` class as well as with
insert iterators and insert pointers.

### Forward iterators <a id="forward.iterators">[[forward.iterators]]</a>

A class or pointer type `X` satisfies the requirements of a forward
iterator if

- `X` satisfies the requirements of an input iterator (
  [[input.iterators]]),
- X satisfies the `DefaultConstructible` requirements (
  [[utility.arg.requirements]]),
- if `X` is a mutable iterator, `reference` is a reference to `T`; if
  `X` is a const iterator, `reference` is a reference to `const T`,
- the expressions in Table  [[tab:iterator.forward.requirements]] are
  valid and have the indicated semantics, and
- objects of type `X` offer the multi-pass guarantee, described below.

The domain of == for forward iterators is that of iterators over the
same underlying sequence.

Two dereferenceable iterators `a` and `b` of type `X` offer the
*multi-pass guarantee* if:

- `a == b` implies `++a == ++b` and
- `X` is a pointer type or the expression `(void)++X(a), *a` is
  equivalent to the expression `*a`.

The requirement that `a == b` implies `++a == ++b` (which is not true
for input and output iterators) and the removal of the restrictions on
the number of the assignments through a mutable iterator (which applies
to output iterators) allows the use of multi-pass one-directional
algorithms with forward iterators.

If `a` and `b` are equal, then either `a` and `b` are both
dereferenceable or else neither is dereferenceable.

If `a` and `b` are both dereferenceable, then `a == b` if and only if
`*a` and `*b` are bound to the same object.

### Bidirectional iterators <a id="bidirectional.iterators">[[bidirectional.iterators]]</a>

A class or pointer type `X` satisfies the requirements of a
bidirectional iterator if, in addition to satisfying the requirements
for forward iterators, the following expressions are valid as shown in
Table  [[tab:iterator.bidirectional.requirements]].

Bidirectional iterators allow algorithms to move iterators backward as
well as forward.

### Random access iterators <a id="random.access.iterators">[[random.access.iterators]]</a>

A class or pointer type `X` satisfies the requirements of a random
access iterator if, in addition to satisfying the requirements for
bidirectional iterators, the following expressions are valid as shown in
Table  [[tab:iterator.random.access.requirements]].

## Header `<iterator>` synopsis <a id="iterator.synopsis">[[iterator.synopsis]]</a>

``` cpp
namespace std {
  // [iterator.primitives], primitives:
  template<class Iterator> struct iterator_traits;
  template<class T> struct iterator_traits<T*>;

  template<class Category, class T, class Distance = ptrdiff_t,
       class Pointer = T*, class Reference = T&> struct iterator;

  struct input_iterator_tag { };
  struct output_iterator_tag { };
  struct forward_iterator_tag: public input_iterator_tag { };
  struct bidirectional_iterator_tag: public forward_iterator_tag { };
  struct random_access_iterator_tag: public bidirectional_iterator_tag { };

  // [iterator.operations], iterator operations:
  template <class InputIterator, class Distance>
    void advance(InputIterator& i, Distance n);
  template <class InputIterator>
    typename iterator_traits<InputIterator>::difference_type
    distance(InputIterator first, InputIterator last);
  template <class ForwardIterator>
    ForwardIterator next(ForwardIterator x,
      typename std::iterator_traits<ForwardIterator>::difference_type n = 1);
  template <class BidirectionalIterator>
    BidirectionalIterator prev(BidirectionalIterator x,
      typename std::iterator_traits<BidirectionalIterator>::difference_type n = 1);

  // [predef.iterators], predefined iterators:
  template <class Iterator> class reverse_iterator;

  template <class Iterator1, class Iterator2>
    bool operator==(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator!=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);

  template <class Iterator1, class Iterator2>
    auto operator-(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y) ->decltype(y.base() - x.base());
  template <class Iterator>
    reverse_iterator<Iterator>
      operator+(
    typename reverse_iterator<Iterator>::difference_type n,
    const reverse_iterator<Iterator>& x);

  template <class Container> class back_insert_iterator;
  template <class Container>
    back_insert_iterator<Container> back_inserter(Container& x);

  template <class Container> class front_insert_iterator;
  template <class Container>
    front_insert_iterator<Container> front_inserter(Container& x);

  template <class Container> class insert_iterator;
  template <class Container>
    insert_iterator<Container> inserter(Container& x, typename Container::iterator i);

  template <class Iterator> class move_iterator;
  template <class Iterator1, class Iterator2>
    bool operator==(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator!=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);

  template <class Iterator1, class Iterator2>
    auto operator-(
    const move_iterator<Iterator1>& x,
    const move_iterator<Iterator2>& y) -> decltype(x.base() - y.base());
  template <class Iterator>
    move_iterator<Iterator> operator+(
      typename move_iterator<Iterator>::difference_type n, const move_iterator<Iterator>& x);
  template <class Iterator>
    move_iterator<Iterator> make_move_iterator(const Iterator& i);

  // [stream.iterators], stream iterators:
  template <class T, class charT = char, class traits = char_traits<charT>,
      class Distance = ptrdiff_t>
  class istream_iterator;
  template <class T, class charT, class traits, class Distance>
    bool operator==(const istream_iterator<T,charT,traits,Distance>& x,
            const istream_iterator<T,charT,traits,Distance>& y);
  template <class T, class charT, class traits, class Distance>
    bool operator!=(const istream_iterator<T,charT,traits,Distance>& x,
            const istream_iterator<T,charT,traits,Distance>& y);

  template <class T, class charT = char, class traits = char_traits<charT> >
      class ostream_iterator;

  template<class charT, class traits = char_traits<charT> >
    class istreambuf_iterator;
  template <class charT, class traits>
    bool operator==(const istreambuf_iterator<charT,traits>& a,
            const istreambuf_iterator<charT,traits>& b);
  template <class charT, class traits>
    bool operator!=(const istreambuf_iterator<charT,traits>& a,
            const istreambuf_iterator<charT,traits>& b);

  template <class charT, class traits = char_traits<charT> >
    class ostreambuf_iterator;

  // [iterator.range], range access:
  template <class C> auto begin(C& c) -> decltype(c.begin());
  template <class C> auto begin(const C& c) -> decltype(c.begin());
  template <class C> auto end(C& c) -> decltype(c.end());
  template <class C> auto end(const C& c) -> decltype(c.end());
  template <class T, size_t N> T* begin(T (&array)[N]);
  template <class T, size_t N> T* end(T (&array)[N]);
}
```

## Iterator primitives <a id="iterator.primitives">[[iterator.primitives]]</a>

To simplify the task of defining iterators, the library provides several
classes and functions:

### Iterator traits <a id="iterator.traits">[[iterator.traits]]</a>

To implement algorithms only in terms of iterators, it is often
necessary to determine the value and difference types that correspond to
a particular iterator type. Accordingly, it is required that if
`Iterator` is the type of an iterator, the types

``` cpp
iterator_traits<Iterator>::difference_type
iterator_traits<Iterator>::value_type
iterator_traits<Iterator>::iterator_category
```

be defined as the iterator’s difference type, value type and iterator
category, respectively. In addition, the types

``` cpp
iterator_traits<Iterator>::reference
iterator_traits<Iterator>::pointer
```

shall be defined as the iterator’s reference and pointer types, that is,
for an iterator object `a`, the same type as the type of `*a` and `a->`,
respectively. In the case of an output iterator, the types

``` cpp
iterator_traits<Iterator>::difference_type
iterator_traits<Iterator>::value_type
iterator_traits<Iterator>::reference
iterator_traits<Iterator>::pointer
```

may be defined as `void`.

The template `iterator_traits<Iterator>` is defined as

``` cpp
namespace std {
  template<class Iterator> struct iterator_traits {
    typedef typename Iterator::difference_type difference_type;
    typedef typename Iterator::value_type value_type;
    typedef typename Iterator::pointer pointer;
    typedef typename Iterator::reference reference;
    typedef typename Iterator::iterator_category iterator_category;
  };
}
```

It is specialized for pointers as

``` cpp
namespace std {
  template<class T> struct iterator_traits<T*> {
    typedef ptrdiff_t difference_type;
    typedef T value_type;
    typedef T* pointer;
    typedef T& reference;
    typedef random_access_iterator_tag iterator_category;
  };
}
```

and for pointers to const as

``` cpp
namespace std {
  template<class T> struct iterator_traits<const T*> {
    typedef ptrdiff_t difference_type;
    typedef T value_type;
    typedef const T* pointer;
    typedef const T& reference;
    typedef random_access_iterator_tag iterator_category;
  };
}
```

If there is an additional pointer type ` \xname{far}` such that the
difference of two ` \xname{far}` is of type `long`, an implementation
may define

``` cpp
template<class T> struct iterator_traits<T __far*> {
    typedef long difference_type;
    typedef T value_type;
    typedef T __far* pointer;
    typedef T __far& reference;
    typedef random_access_iterator_tag iterator_category;
  };
```

To implement a generic `reverse` function, a C++program can do the
following:

``` cpp
template <class BidirectionalIterator>
void reverse(BidirectionalIterator first, BidirectionalIterator last) {
  typename iterator_traits<BidirectionalIterator>::difference_type n =
    distance(first, last);
  --n;
  while(n > 0) {
    typename iterator_traits<BidirectionalIterator>::value_type
     tmp = *first;
    *first++ = *--last;
    *last = tmp;
    n -= 2;
  }
}
```

### Basic iterator <a id="iterator.basic">[[iterator.basic]]</a>

The `iterator` template may be used as a base class to ease the
definition of required types for new iterators.

``` cpp
namespace std {
  template<class Category, class T, class Distance = ptrdiff_t,
    class Pointer = T*, class Reference = T&>
  struct iterator {
    typedef T         value_type;
    typedef Distance  difference_type;
    typedef Pointer   pointer;
    typedef Reference reference;
    typedef Category  iterator_category;
  };
}
```

### Standard iterator tags <a id="std.iterator.tags">[[std.iterator.tags]]</a>

It is often desirable for a function template specialization to find out
what is the most specific category of its iterator argument, so that the
function can select the most efficient algorithm at compile time. To
facilitate this, the library introduces *category tag* classes which are
used as compile time tags for algorithm selection. They are:
`input_iterator_tag`, `output_iterator_tag`, `forward_iterator_tag`,
`bidirectional_iterator_tag` and `random_access_iterator_tag`. For every
iterator of type `Iterator`,
`iterator_traits<Iterator>::iterator_category` shall be defined to be
the most specific category tag that describes the iterator’s behavior.

``` cpp
namespace std {
  struct input_iterator_tag { };
  struct output_iterator_tag { };
  struct forward_iterator_tag: public input_iterator_tag { };
  struct bidirectional_iterator_tag: public forward_iterator_tag { };
  struct random_access_iterator_tag: public bidirectional_iterator_tag { };
}
```

For a program-defined iterator `BinaryTreeIterator`, it could be
included into the bidirectional iterator category by specializing the
`iterator_traits` template:

``` cpp
template<class T> struct iterator_traits<BinaryTreeIterator<T> > {
  typedef std::ptrdiff_t difference_type;
  typedef T value_type;
  typedef T* pointer;
  typedef T& reference;
  typedef bidirectional_iterator_tag iterator_category;
};
```

Typically, however, it would be easier to derive `BinaryTreeIterator<T>`
from `iterator<bidirectional_iterator_tag,T,ptrdiff_t,T*,T&>`.

If `evolve()` is well defined for bidirectional iterators, but can be
implemented more efficiently for random access iterators, then the
implementation is as follows:

``` cpp
template <class BidirectionalIterator>
inline void
evolve(BidirectionalIterator first, BidirectionalIterator last) {
  evolve(first, last,
    typename iterator_traits<BidirectionalIterator>::iterator_category());
}

template <class BidirectionalIterator>
void evolve(BidirectionalIterator first, BidirectionalIterator last,
  bidirectional_iterator_tag) {
  // more generic, but less efficient algorithm
}

template <class RandomAccessIterator>
void evolve(RandomAccessIterator first, RandomAccessIterator last,
  random_access_iterator_tag) {
  // more efficient, but less generic algorithm
}
```

If a C++program wants to define a bidirectional iterator for some data
structure containing `double` and such that it works on a large memory
model of the implementation, it can do so with:

``` cpp
class MyIterator :
  public iterator<bidirectional_iterator_tag, double, long, T*, T&> {
  // code implementing ++, etc.
};
```

Then there is no need to specialize the `iterator_traits` template.

### Iterator operations <a id="iterator.operations">[[iterator.operations]]</a>

Since only random access iterators provide `+` and `-` operators, the
library provides two function templates `advance` and `distance`. These
function templates use `+` and `-` for random access iterators (and are,
therefore, constant time for them); for input, forward and bidirectional
iterators they use `++` to provide linear time implementations.

``` cpp
template <class InputIterator, class Distance>
  void advance(InputIterator& i, Distance n);
```

*Requires:* `n` shall be negative only for bidirectional and random
access iterators.

*Effects:* Increments (or decrements for negative `n`) iterator
reference `i` by `n`.

``` cpp
template<class InputIterator>
      typename iterator_traits<InputIterator>::difference_type
         distance(InputIterator first, InputIterator last);
```

*Effects:* If `InputIterator` meets the requirements of random access
iterator, returns `(last - first)`; otherwise, returns the number of
increments needed to get from `first` to `last`.

*Requires:* If `InputIterator` meets the requirements of random access
iterator, `last` shall be reachable from `first` or `first` shall be
reachable from `last`; otherwise, `last` shall be reachable from
`first`.

``` cpp
template <class ForwardIterator>
  ForwardIterator next(ForwardIterator x,
    typename std::iterator_traits<ForwardIterator>::difference_type n = 1);
```

*Effects:* Equivalent to `advance(x, n); return x;`

``` cpp
template <class BidirectionalIterator>
  BidirectionalIterator prev(BidirectionalIterator x,
    typename std::iterator_traits<BidirectionalIterator>::difference_type n = 1);
```

*Effects:* Equivalent to `advance(x, -n); return x;`

## Iterator adaptors <a id="predef.iterators">[[predef.iterators]]</a>

### Reverse iterators <a id="reverse.iterators">[[reverse.iterators]]</a>

Class template `reverse_iterator` is an iterator adaptor that iterates
from the end of the sequence defined by its underlying iterator to the
beginning of that sequence. The fundamental relation between a reverse
iterator and its corresponding iterator `i` is established by the
identity: `&*(reverse_iterator(i)) == &*(i - 1)`.

#### Class template `reverse_iterator` <a id="reverse.iterator">[[reverse.iterator]]</a>

``` cpp
namespace std {
  template <class Iterator>
  class reverse_iterator : public
        iterator<typename iterator_traits<Iterator>::iterator_category,
        typename iterator_traits<Iterator>::value_type,
        typename iterator_traits<Iterator>::difference_type,
        typename iterator_traits<Iterator>::pointer,
        typename iterator_traits<Iterator>::reference> {
  public:
    typedef Iterator                                            iterator_type;
    typedef typename iterator_traits<Iterator>::difference_type difference_type;
    typedef typename iterator_traits<Iterator>::reference       reference;
    typedef typename iterator_traits<Iterator>::pointer         pointer;

    reverse_iterator();
    explicit reverse_iterator(Iterator x);
    template <class U> reverse_iterator(const reverse_iterator<U>& u);
    template <class U> reverse_iterator& operator=(const reverse_iterator<U>& u);

    Iterator base() const;      // explicit
    reference operator*() const;
    pointer   operator->() const;

    reverse_iterator& operator++();
    reverse_iterator  operator++(int);
    reverse_iterator& operator--();
    reverse_iterator  operator--(int);

    reverse_iterator  operator+ (difference_type n) const;
    reverse_iterator& operator+=(difference_type n);
    reverse_iterator  operator- (difference_type n) const;
    reverse_iterator& operator-=(difference_type n);
    unspecified operator[](difference_type n) const;
  protected:
    Iterator current;
  private:
    Iterator deref_tmp;         // exposition only
  };

  template <class Iterator1, class Iterator2>
    bool operator==(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator!=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<=(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    auto operator-(
      const reverse_iterator<Iterator1>& x,
      const reverse_iterator<Iterator2>& y) -> decltype(y.current - x.current);
  template <class Iterator>
    reverse_iterator<Iterator> operator+(
      typename reverse_iterator<Iterator>::difference_type n,
      const reverse_iterator<Iterator>& x);
}
```

#### `reverse_iterator` requirements <a id="reverse.iter.requirements">[[reverse.iter.requirements]]</a>

The template parameter `Iterator` shall meet all the requirements of a
Bidirectional Iterator ([[bidirectional.iterators]]).

Additionally, `Iterator` shall meet the requirements of a Random Access
Iterator ([[random.access.iterators]]) if any of the members
`operator+` ([[reverse.iter.op+]]), `operator-` (
[[reverse.iter.op-]]), `operator+=` ([[reverse.iter.op+=]]),
`operator-=` ([[reverse.iter.op-=]]), `operator []` (
[[reverse.iter.opindex]]), or the global operators `operator<` (
[[reverse.iter.op<]]), `operator>` ([[reverse.iter.op>]]),  
`operator <=` ([[reverse.iter.op<=]]), `operator>=` (
[[reverse.iter.op>=]]), `operator-` ([[reverse.iter.opdiff]]) or
`operator+` ([[reverse.iter.opsum]]) are referenced in a way that
requires instantiation ([[temp.inst]]).

#### `reverse_iterator` operations <a id="reverse.iter.ops">[[reverse.iter.ops]]</a>

##### `reverse_iterator` constructor <a id="reverse.iter.cons">[[reverse.iter.cons]]</a>

``` cpp
reverse_iterator();
```

*Effects:* Value initializes `current`. Iterator operations applied to
the resulting iterator have defined behavior if and only if the
corresponding operations are defined on a value-initialized iterator of
type `Iterator`.

``` cpp
explicit reverse_iterator(Iterator x);
```

*Effects:* Initializes `current` with `x`.

``` cpp
template <class U> reverse_iterator(const reverse_iterator<U> &u);
```

*Effects:* Initializes `current` with `u.current`.

##### `reverse_iterator::operator=` <a id="reverse.iter.op=">[[reverse.iter.op=]]</a>

``` cpp
template <class U>
reverse_iterator&
  operator=(const reverse_iterator<U>& u);
```

*Effects:* Assigns `u.base()` to current.

*Returns:* `*this`.

##### Conversion <a id="reverse.iter.conv">[[reverse.iter.conv]]</a>

``` cpp
Iterator base() const;          // explicit
```

*Returns:* `current`.

##### `operator*` <a id="reverse.iter.op.star">[[reverse.iter.op.star]]</a>

``` cpp
reference operator*() const;
```

*Effects:*

``` cpp
deref_tmp = current;
--deref_tmp;
return *deref_tmp;
```

This operation must use an auxiliary member variable rather than a
temporary variable to avoid returning a reference that persists beyond
the lifetime of its associated iterator.
(See  [[iterator.requirements]].)

##### `operator->` <a id="reverse.iter.opref">[[reverse.iter.opref]]</a>

``` cpp
pointer operator->() const;
```

*Returns:* `&(operator*())`.

##### `operator++` <a id="reverse.iter.op++">[[reverse.iter.op++]]</a>

``` cpp
reverse_iterator& operator++();
```

*Effects:* `current;`

*Returns:* `*this`.

``` cpp
reverse_iterator operator++(int);
```

*Effects:*

``` cpp
reverse_iterator tmp = *this;
--current;
return tmp;
```

\[reverse.iter.op\]`operator\dcr`

``` cpp
reverse_iterator& operator--();
```

*Effects:* `++current`

*Returns:* `*this`.

``` cpp
reverse_iterator operator--(int);
```

*Effects:*

``` cpp
reverse_iterator tmp = *this;
++current;
return tmp;
```

##### `operator+` <a id="reverse.iter.op+">[[reverse.iter.op+]]</a>

``` cpp
reverse_iterator
operator+(typename reverse_iterator<Iterator>::difference_type n) const;
```

*Returns:* `reverse_iterator(current-n)`.

##### `operator+=` <a id="reverse.iter.op+=">[[reverse.iter.op+=]]</a>

``` cpp
reverse_iterator&
operator+=(typename reverse_iterator<Iterator>::difference_type n);
```

*Effects:* `current -= n;`

*Returns:* `*this`.

##### `operator-` <a id="reverse.iter.op-">[[reverse.iter.op-]]</a>

``` cpp
reverse_iterator
operator-(typename reverse_iterator<Iterator>::difference_type n) const;
```

*Returns:* `reverse_iterator(current+n)`.

##### `operator-=` <a id="reverse.iter.op-=">[[reverse.iter.op-=]]</a>

``` cpp
reverse_iterator&
operator-=(typename reverse_iterator<Iterator>::difference_type n);
```

*Effects:* `current += n;`

*Returns:* `*this`.

##### `operator[]` <a id="reverse.iter.opindex">[[reverse.iter.opindex]]</a>

``` cpp
unspecified operator[](
    typename reverse_iterator<Iterator>::difference_type n) const;
```

*Returns:* `current[-n-1]`.

##### `operator==` <a id="reverse.iter.op==">[[reverse.iter.op==]]</a>

``` cpp
template <class Iterator1, class Iterator2>
  bool operator==(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Returns:* `x.current == y.current`.

##### `operator<` <a id="reverse.iter.op<">[[reverse.iter.op<]]</a>

``` cpp
template <class Iterator1, class Iterator2>
  bool operator<(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Returns:* `x.current > y.current`.

##### `operator!=` <a id="reverse.iter.op!=">[[reverse.iter.op!=]]</a>

``` cpp
template <class Iterator1, class Iterator2>
  bool operator!=(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Returns:* `x.current != y.current`.

##### `operator>` <a id="reverse.iter.op>">[[reverse.iter.op>]]</a>

``` cpp
template <class Iterator1, class Iterator2>
  bool operator>(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Returns:* `x.current < y.current`.

##### `operator>=` <a id="reverse.iter.op>=">[[reverse.iter.op>=]]</a>

``` cpp
template <class Iterator1, class Iterator2>
  bool operator>=(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Returns:* `x.current <= y.current`.

##### `operator<=` <a id="reverse.iter.op<=">[[reverse.iter.op<=]]</a>

``` cpp
template <class Iterator1, class Iterator2>
  bool operator<=(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y);
```

*Returns:* `x.current >= y.current`.

##### `operator-` <a id="reverse.iter.opdiff">[[reverse.iter.opdiff]]</a>

``` cpp
template <class Iterator1, class Iterator2>
    auto operator-(
    const reverse_iterator<Iterator1>& x,
    const reverse_iterator<Iterator2>& y) -> decltype(y.current - x.current);
```

*Returns:* `y.current - x.current`.

##### `operator+` <a id="reverse.iter.opsum">[[reverse.iter.opsum]]</a>

``` cpp
template <class Iterator>
  reverse_iterator<Iterator> operator+(
    typename reverse_iterator<Iterator>::difference_type n,
    const reverse_iterator<Iterator>& x);
```

*Returns:* `reverse_iterator<Iterator> (x.current - n)`.

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
at the beginning nor at the end of the container. Insert iterators
satisfy the requirements of output iterators. `operator*` returns the
insert iterator itself. The assignment `operator=(const T& x)` is
defined on insert iterators to allow writing into them, it inserts `x`
right before where the insert iterator is pointing. In other words, an
insert iterator is like a cursor pointing into the container where the
insertion takes place. `back_insert_iterator` inserts elements at the
end of a container, `front_insert_iterator` inserts elements at the
beginning of a container, and `insert_iterator` inserts elements where
the iterator points to in a container. `back_inserter`,
`front_inserter`, and `inserter` are three functions making the insert
iterators out of a container.

#### Class template `back_insert_iterator` <a id="back.insert.iterator">[[back.insert.iterator]]</a>

``` cpp
namespace std {
  template <class Container>
  class back_insert_iterator :
    public iterator<output_iterator_tag,void,void,void,void> {
  protected:
    Container* container;

  public:
    typedef Container container_type;
    explicit back_insert_iterator(Container& x);
    back_insert_iterator<Container>&
      operator=(const typename Container::value_type& value);
    back_insert_iterator<Container>&
      operator=(typename Container::value_type&& value);

    back_insert_iterator<Container>& operator*();
    back_insert_iterator<Container>& operator++();
    back_insert_iterator<Container>  operator++(int);
  };

  template <class Container>
    back_insert_iterator<Container> back_inserter(Container& x);
}
```

#### `back_insert_iterator` operations <a id="back.insert.iter.ops">[[back.insert.iter.ops]]</a>

##### `back_insert_iterator` constructor <a id="back.insert.iter.cons">[[back.insert.iter.cons]]</a>

``` cpp
explicit back_insert_iterator(Container& x);
```

*Effects:* Initializes `container` with `&x`.

##### `back_insert_iterator::operator=` <a id="back.insert.iter.op=">[[back.insert.iter.op=]]</a>

``` cpp
back_insert_iterator<Container>&
  operator=(const typename Container::value_type& value);
```

*Effects:* `container->push_back(value);`

*Returns:* `*this`.

``` cpp
back_insert_iterator<Container>&
  operator=(typename Container::value_type&& value);
```

*Effects:* `container->push_back(std::move(value));`

*Returns:* `*this`.

##### `back_insert_iterator::operator*` <a id="back.insert.iter.op*">[[back.insert.iter.op*]]</a>

``` cpp
back_insert_iterator<Container>& operator*();
```

*Returns:* `*this`.

##### `back_insert_iterator::operator++` <a id="back.insert.iter.op++">[[back.insert.iter.op++]]</a>

``` cpp
back_insert_iterator<Container>& operator++();
back_insert_iterator<Container>  operator++(int);
```

*Returns:* `*this`.

#####  `back_inserter` <a id="back.inserter">[[back.inserter]]</a>

``` cpp
template <class Container>
  back_insert_iterator<Container> back_inserter(Container& x);
```

*Returns:* `back_insert_iterator<Container>(x)`.

#### Class template `front_insert_iterator` <a id="front.insert.iterator">[[front.insert.iterator]]</a>

``` cpp
namespace std {
  template <class Container>
  class front_insert_iterator :
    public iterator<output_iterator_tag,void,void,void,void> {
  protected:
    Container* container;

  public:
    typedef Container container_type;
    explicit front_insert_iterator(Container& x);
    front_insert_iterator<Container>&
      operator=(const typename Container::value_type& value);
    front_insert_iterator<Container>&
      operator=(typename Container::value_type&& value);

    front_insert_iterator<Container>& operator*();
    front_insert_iterator<Container>& operator++();
    front_insert_iterator<Container>  operator++(int);
  };

  template <class Container>
    front_insert_iterator<Container> front_inserter(Container& x);
}
```

#### `front_insert_iterator` operations <a id="front.insert.iter.ops">[[front.insert.iter.ops]]</a>

##### `front_insert_iterator` constructor <a id="front.insert.iter.cons">[[front.insert.iter.cons]]</a>

``` cpp
explicit front_insert_iterator(Container& x);
```

*Effects:* Initializes `container` with `&x`.

##### `front_insert_iterator::operator=` <a id="front.insert.iter.op=">[[front.insert.iter.op=]]</a>

``` cpp
front_insert_iterator<Container>&
  operator=(const typename Container::value_type& value);
```

*Effects:* `container->push_front(value);`

*Returns:* `*this`.

``` cpp
front_insert_iterator<Container>&
  operator=(typename Container::value_type&& value);
```

*Effects:* `container->push_front(std::move(value));`

*Returns:* `*this`.

##### `front_insert_iterator::operator*` <a id="front.insert.iter.op*">[[front.insert.iter.op*]]</a>

``` cpp
front_insert_iterator<Container>& operator*();
```

*Returns:* `*this`.

##### `front_insert_iterator::operator++` <a id="front.insert.iter.op++">[[front.insert.iter.op++]]</a>

``` cpp
front_insert_iterator<Container>& operator++();
front_insert_iterator<Container>  operator++(int);
```

*Returns:* `*this`.

##### `front_inserter` <a id="front.inserter">[[front.inserter]]</a>

``` cpp
template <class Container>
  front_insert_iterator<Container> front_inserter(Container& x);
```

*Returns:* `front_insert_iterator<Container>(x)`.

#### Class template `insert_iterator` <a id="insert.iterator">[[insert.iterator]]</a>

``` cpp
namespace std {
  template <class Container>
  class insert_iterator :
    public iterator<output_iterator_tag,void,void,void,void> {
  protected:
    Container* container;
    typename Container::iterator iter;

  public:
    typedef Container container_type;
    insert_iterator(Container& x, typename Container::iterator i);
    insert_iterator<Container>&
      operator=(const typename Container::value_type& value);
    insert_iterator<Container>&
      operator=(typename Container::value_type&& value);

    insert_iterator<Container>& operator*();
    insert_iterator<Container>& operator++();
    insert_iterator<Container>& operator++(int);
  };

  template <class Container>
    insert_iterator<Container> inserter(Container& x, typename Container::iterator i);
}
```

#### `insert_iterator` operations <a id="insert.iter.ops">[[insert.iter.ops]]</a>

##### `insert_iterator` constructor <a id="insert.iter.cons">[[insert.iter.cons]]</a>

``` cpp
insert_iterator(Container& x, typename Container::iterator i);
```

*Effects:* Initializes `container` with `&x` and `iter` with `i`.

##### `insert_iterator::operator=` <a id="insert.iter.op=">[[insert.iter.op=]]</a>

``` cpp
insert_iterator<Container>&
  operator=(const typename Container::value_type& value);
```

*Effects:*

``` cpp
iter = container->insert(iter, value);
++iter;
```

*Returns:* `*this`.

``` cpp
insert_iterator<Container>&
  operator=(typename Container::value_type&& value);
```

*Effects:*

``` cpp
iter = container->insert(iter, std::move(value));
++iter;
```

*Returns:* `*this`.

##### `insert_iterator::operator*` <a id="insert.iter.op*">[[insert.iter.op*]]</a>

``` cpp
insert_iterator<Container>& operator*();
```

*Returns:* `*this`.

##### `insert_iterator::operator++` <a id="insert.iter.op++">[[insert.iter.op++]]</a>

``` cpp
insert_iterator<Container>& operator++();
insert_iterator<Container>& operator++(int);
```

*Returns:* `*this`.

##### `inserter` <a id="inserter">[[inserter]]</a>

``` cpp
template <class Container>
  insert_iterator<Container> inserter(Container& x, typename Container::iterator i);
```

*Returns:* `insert_iterator<Container>(x, i)`.

### Move iterators <a id="move.iterators">[[move.iterators]]</a>

Class template `move_iterator` is an iterator adaptor with the same
behavior as the underlying iterator except that its dereference operator
implicitly converts the value returned by the underlying iterator’s
dereference operator to an rvalue reference. Some generic algorithms can
be called with move iterators to replace copying with moving.

``` cpp
list<string> s;
// populate the list s
vector<string> v1(s.begin(), s.end());          // copies strings into v1
vector<string> v2(make_move_iterator(s.begin()),
                  make_move_iterator(s.end())); // moves strings into v2
```

#### Class template `move_iterator` <a id="move.iterator">[[move.iterator]]</a>

``` cpp
namespace std {
  template <class Iterator>
  class move_iterator {
  public:
    typedef Iterator                                              iterator_type;
    typedef typename iterator_traits<Iterator>::difference_type   difference_type;
    typedef Iterator                                              pointer;
    typedef typename iterator_traits<Iterator>::value_type        value_type;
    typedef typename iterator_traits<Iterator>::iterator_category iterator_category;
    typedef value_type&&                                          reference;

    move_iterator();
    explicit move_iterator(Iterator i);
    template <class U> move_iterator(const move_iterator<U>& u);
    template <class U> move_iterator& operator=(const move_iterator<U>& u);

    iterator_type base() const;
    reference operator*() const;
    pointer operator->() const;

    move_iterator& operator++();
    move_iterator operator++(int);
    move_iterator& operator--();
    move_iterator operator--(int);

    move_iterator operator+(difference_type n) const;
    move_iterator& operator+=(difference_type n);
    move_iterator operator-(difference_type n) const;
    move_iterator& operator-=(difference_type n);
    unspecified operator[](difference_type n) const;

  private:
    Iterator current;   // exposition only
  };

  template <class Iterator1, class Iterator2>
    bool operator==(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator!=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator<=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
  template <class Iterator1, class Iterator2>
    bool operator>=(
      const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);

  template <class Iterator1, class Iterator2>
    auto operator-(
      const move_iterator<Iterator1>& x,
      const move_iterator<Iterator2>& y) -> decltype(x.base() - y.base());
  template <class Iterator>
    move_iterator<Iterator> operator+(
      typename move_iterator<Iterator>::difference_type n, const move_iterator<Iterator>& x);
  template <class Iterator>
    move_iterator<Iterator> make_move_iterator(const Iterator& i);
}
```

#### `move_iterator` requirements <a id="move.iter.requirements">[[move.iter.requirements]]</a>

The template parameter `Iterator` shall meet the requirements for an
Input Iterator ([[input.iterators]]). Additionally, if any of the
bidirectional or random access traversal functions are instantiated, the
template parameter shall meet the requirements for a Bidirectional
Iterator ([[bidirectional.iterators]]) or a Random Access Iterator (
[[random.access.iterators]]), respectively.

#### `move_iterator` operations <a id="move.iter.ops">[[move.iter.ops]]</a>

##### `move_iterator` constructors <a id="move.iter.op.const">[[move.iter.op.const]]</a>

``` cpp
move_iterator();
```

*Effects:* Constructs a `move_iterator`, value initializing `current`.
Iterator operations applied to the resulting iterator have defined
behavior if and only if the corresponding operations are defined on a
value-initialized iterator of type `Iterator`.

``` cpp
explicit move_iterator(Iterator i);
```

*Effects:* Constructs a `move_iterator`, initializing `current` with
`i`.

``` cpp
template <class U> move_iterator(const move_iterator<U>& u);
```

*Effects:* Constructs a `move_iterator`, initializing `current` with
`u.base()`.

*Requires:* `U` shall be convertible to `Iterator`.

##### `move_iterator::operator=` <a id="move.iter.op=">[[move.iter.op=]]</a>

``` cpp
template <class U> move_iterator& operator=(const move_iterator<U>& u);
```

*Effects:* Assigns `u.base()` to `current`.

*Requires:* `U` shall be convertible to `Iterator`.

##### `move_iterator` conversion <a id="move.iter.op.conv">[[move.iter.op.conv]]</a>

``` cpp
Iterator base() const;
```

*Returns:* `current`.

##### `move_iterator::operator*` <a id="move.iter.op.star">[[move.iter.op.star]]</a>

``` cpp
reference operator*() const;
```

*Returns:* `std::move(`\*current).

##### `move_iterator::operator->` <a id="move.iter.op.ref">[[move.iter.op.ref]]</a>

``` cpp
pointer operator->() const;
```

*Returns:* `current`.

##### `move_iterator::operator++` <a id="move.iter.op.incr">[[move.iter.op.incr]]</a>

``` cpp
move_iterator& operator++();
```

*Effects:* `++current`.

*Returns:* `*this`.

``` cpp
move_iterator operator++(int);
```

*Effects:*

``` cpp
move_iterator tmp = *this;
++current;
return tmp;
```

##### `move_iterator::operator-{-}` <a id="move.iter.op.decr">[[move.iter.op.decr]]</a>

``` cpp
move_iterator& operator--();
```

*Effects:* \dcr`current`.

*Returns:* `*this`.

``` cpp
move_iterator operator--(int);
```

*Effects:*

``` cpp
move_iterator tmp = *this;
--current;
return tmp;
```

##### `move_iterator::operator+` <a id="move.iter.op.+">[[move.iter.op.+]]</a>

``` cpp
move_iterator operator+(difference_type n) const;
```

*Returns:* `move_iterator(current + n)`.

##### `move_iterator::operator+=` <a id="move.iter.op.+=">[[move.iter.op.+=]]</a>

``` cpp
move_iterator& operator+=(difference_type n);
```

*Effects:* `current += n`.

*Returns:* `*this`.

##### `move_iterator::operator-` <a id="move.iter.op.-">[[move.iter.op.-]]</a>

``` cpp
move_iterator operator-(difference_type n) const;
```

*Returns:* `move_iterator(current - n)`.

##### `move_iterator::operator-=` <a id="move.iter.op.-=">[[move.iter.op.-=]]</a>

``` cpp
move_iterator& operator-=(difference_type n);
```

*Effects:* `current -= n`.

*Returns:* `*this`.

##### `move_iterator::operator[]` <a id="move.iter.op.index">[[move.iter.op.index]]</a>

``` cpp
unspecified operator[](difference_type n) const;
```

*Returns:* `std::move(`current\[n\]).

##### `move_iterator` comparisons <a id="move.iter.op.comp">[[move.iter.op.comp]]</a>

``` cpp
template <class Iterator1, class Iterator2>
bool operator==(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Returns:* `x.base() == y.base()`.

``` cpp
template <class Iterator1, class Iterator2>
bool operator!=(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Returns:* `!(x == y)`.

``` cpp
template <class Iterator1, class Iterator2>
bool operator<(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Returns:* `x.base() < y.base()`.

``` cpp
template <class Iterator1, class Iterator2>
bool operator<=(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Returns:* `!(y < x)`.

``` cpp
template <class Iterator1, class Iterator2>
bool operator>(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Returns:* `y < x`.

``` cpp
template <class Iterator1, class Iterator2>
bool operator>=(const move_iterator<Iterator1>& x, const move_iterator<Iterator2>& y);
```

*Returns:* `!(x < y)`.

##### `move_iterator` non-member functions <a id="move.iter.nonmember">[[move.iter.nonmember]]</a>

``` cpp
template <class Iterator1, class Iterator2>
    auto operator-(
    const move_iterator<Iterator1>& x,
    const move_iterator<Iterator2>& y) -> decltype(x.base() - y.base());
```

*Returns:* `x.base() - y.base()`.

``` cpp
template <class Iterator>
  move_iterator<Iterator> operator+(
    typename move_iterator<Iterator>::difference_type n, const move_iterator<Iterator>& x);
```

*Returns:* `x + n`.

``` cpp
template <class Iterator>
move_iterator<Iterator> make_move_iterator(const Iterator& i);
```

*Returns:* `move_iterator<Iterator>(i)`.

## Stream iterators <a id="stream.iterators">[[stream.iterators]]</a>

To make it possible for algorithmic templates to work directly with
input/output streams, appropriate iterator-like class templates are
provided.

``` cpp
partial_sum_copy(istream_iterator<double, char>(cin),
  istream_iterator<double, char>(),
  ostream_iterator<double, char>(cout, "\n"));
```

reads a file containing floating point numbers from `cin`, and prints
the partial sums onto `cout`.

### Class template `istream_iterator` <a id="istream.iterator">[[istream.iterator]]</a>

The class template `istream_iterator` is an input iterator (
[[input.iterators]]) that reads (using `operator>>`) successive elements
from the input stream for which it was constructed. After it is
constructed, and every time `++` is used, the iterator reads and stores
a value of `T`. If the iterator fails to read and store a value of `T`
(`fail()` on the stream returns `true`), the iterator becomes equal to
the *end-of-stream* iterator value. The constructor with no arguments
`istream_iterator()` always constructs an end-of-stream input iterator
object, which is the only legitimate iterator to be used for the end
condition. The result of `operator*` on an end-of-stream iterator is not
defined. For any other iterator value a `const T&` is returned. The
result of `operator->` on an end-of-stream iterator is not defined. For
any other iterator value a `const T*` is returned. The behavior of a
program that applies `operator++()` to an end-of-stream iterator is
undefined. It is impossible to store things into istream iterators.

Two end-of-stream iterators are always equal. An end-of-stream iterator
is not equal to a non-end-of-stream iterator. Two non-end-of-stream
iterators are equal when they are constructed from the same stream.

``` cpp
namespace std {
  template <class T, class charT = char, class traits = char_traits<charT>,
      class Distance = ptrdiff_t>
  class istream_iterator:
    public iterator<input_iterator_tag, T, Distance, const T*, const T&> {
  public:
    typedef charT char_type;
    typedef traits traits_type;
    typedef basic_istream<charT,traits> istream_type;
    see below istream_iterator();
    istream_iterator(istream_type& s);
    istream_iterator(const istream_iterator& x) = default;
   ~istream_iterator() = default;

    const T& operator*() const;
    const T* operator->() const;
    istream_iterator<T,charT,traits,Distance>& operator++();
    istream_iterator<T,charT,traits,Distance>  operator++(int);
  private:
    basic_istream<charT,traits>* in_stream; // exposition only
    T value;                                // exposition only
  };

  template <class T, class charT, class traits, class Distance>
    bool operator==(const istream_iterator<T,charT,traits,Distance>& x,
            const istream_iterator<T,charT,traits,Distance>& y);
  template <class T, class charT, class traits, class Distance>
    bool operator!=(const istream_iterator<T,charT,traits,Distance>& x,
            const istream_iterator<T,charT,traits,Distance>& y);
}
```

#### `istream_iterator` constructors and destructor <a id="istream.iterator.cons">[[istream.iterator.cons]]</a>

``` cpp
see below istream_iterator();
```

*Effects:* Constructs the end-of-stream iterator. If `T` is a literal
type, then this constructor shall be a `constexpr` constructor.

`in_stream == 0`.

``` cpp
istream_iterator(istream_type& s);
```

*Effects:* Initializes *in_stream* with `&s`. *value* may be initialized
during construction or the first time it is referenced.

`in_stream == &s`.

``` cpp
istream_iterator(const istream_iterator& x) = default;
```

*Effects:* Constructs a copy of `x`. If `T` is a literal type, then this
constructor shall be a trivial copy constructor.

`in_stream == x.in_stream`.

``` cpp
~istream_iterator() = default;
```

*Effects:* The iterator is destroyed. If `T` is a literal type, then
this destructor shall be a trivial destructor.

#### `istream_iterator` operations <a id="istream.iterator.ops">[[istream.iterator.ops]]</a>

``` cpp
const T& operator*() const;
```

*Returns:* *value*.

``` cpp
const T* operator->() const;
```

*Returns:* `&(operator*())`.

``` cpp
istream_iterator<T,charT,traits,Distance>& operator++();
```

*Requires:* `in_stream != 0`.

*Effects:* `*in_stream >> value`.

*Returns:* `*this`.

``` cpp
istream_iterator<T,charT,traits,Distance> operator++(int);
```

*Requires:* `in_stream != 0`.

*Effects:*

``` cpp
istream_iterator<T,charT,traits,Distance> tmp = *this;
*in_stream >> value;
return (tmp);
```

``` cpp
template <class T, class charT, class traits, class Distance>
  bool operator==(const istream_iterator<T,charT,traits,Distance> &x,
                  const istream_iterator<T,charT,traits,Distance> &y);
```

*Returns:* `x.in_stream == y.in_stream`.

``` cpp
template <class T, class charT, class traits, class Distance>
  bool operator!=(const istream_iterator<T,charT,traits,Distance> &x,
                  const istream_iterator<T,charT,traits,Distance> &y);
```

*Returns:* `!(x == y)`

### Class template `ostream_iterator` <a id="ostream.iterator">[[ostream.iterator]]</a>

`ostream_iterator` writes (using `operator<<`) successive elements onto
the output stream from which it was constructed. If it was constructed
with `charT*` as a constructor argument, this string, called a
*delimiter string*, is written to the stream after every `T` is written.
It is not possible to get a value out of the output iterator. Its only
use is as an output iterator in situations like

``` cpp
while (first != last)
  *result++ = *first++;
```

`ostream_iterator`

is defined as:

``` cpp
namespace std {
  template <class T, class charT = char, class traits = char_traits<charT> >
  class ostream_iterator:
    public iterator<output_iterator_tag, void, void, void, void> {
  public:
    typedef charT char_type;
    typedef traits traits_type;
    typedef basic_ostream<charT,traits> ostream_type;
    ostream_iterator(ostream_type& s);
    ostream_iterator(ostream_type& s, const charT* delimiter);
    ostream_iterator(const ostream_iterator<T,charT,traits>& x);
   ~ostream_iterator();
    ostream_iterator<T,charT,traits>& operator=(const T& value);

    ostream_iterator<T,charT,traits>& operator*();
    ostream_iterator<T,charT,traits>& operator++();
    ostream_iterator<T,charT,traits>& operator++(int);
  private:
    basic_ostream<charT,traits>* out_stream;  // exposition only
    const charT* delim;                       // exposition onlyr
  };
}
```

#### `ostream_iterator` constructors and destructor <a id="ostream.iterator.cons.des">[[ostream.iterator.cons.des]]</a>

``` cpp
ostream_iterator(ostream_type& s);
```

*Effects:* Initializes *out_stream* with `&s` and *delim* with null.

``` cpp
ostream_iterator(ostream_type& s, const charT* delimiter);
```

*Effects:* Initializes *out_stream* with `&s` and *delim* with
`delimiter`.

``` cpp
ostream_iterator(const ostream_iterator& x);
```

*Effects:* Constructs a copy of `x`.

``` cpp
~ostream_iterator();
```

*Effects:* The iterator is destroyed.

#### `ostream_iterator` operations <a id="ostream.iterator.ops">[[ostream.iterator.ops]]</a>

``` cpp
ostream_iterator& operator=(const T& value);
```

*Effects:*

``` cpp
*out_stream << value;
if(delim != 0)
  *out_stream << delim;
return (*this);
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

The class template `istreambuf_iterator` defines an input iterator (
[[input.iterators]]) that reads successive *characters* from the
streambuf for which it was constructed. `operator*` provides access to
the current input character, if any. `operator->` may return a proxy.
Each time `operator++` is evaluated, the iterator advances to the next
input character. If the end of stream is reached
(streambuf_type::sgetc() returns `traits::eof()`), the iterator becomes
equal to the *end-of-stream* iterator value. The default constructor
`istreambuf_iterator()` and the constructor `istreambuf_iterator(0)`
both construct an end-of-stream iterator object suitable for use as an
end-of-range. All specializations of `istreambuf_iterator` shall have a
trivial copy constructor, a `constexpr` default constructor, and a
trivial destructor.

The result of `operator*()` on an end-of-stream iterator is undefined.
For any other iterator value a `char_type` value is returned. It is
impossible to assign a character via an input iterator.

``` cpp
namespace std {
  template<class charT, class traits = char_traits<charT> >
  class istreambuf_iterator
     : public iterator<input_iterator_tag, charT,
                       typename traits::off_type, unspecified, charT> {
  public:
    typedef charT                         char_type;
    typedef traits                        traits_type;
    typedef typename traits::int_type     int_type;
    typedef basic_streambuf<charT,traits> streambuf_type;
    typedef basic_istream<charT,traits>   istream_type;

    class proxy;                          // exposition only

    constexpr istreambuf_iterator() noexcept;
    istreambuf_iterator(const istreambuf_iterator&) noexcept = default;
    ~istreambuf_iterator() = default;
    istreambuf_iterator(istream_type& s) noexcept;
    istreambuf_iterator(streambuf_type* s) noexcept;
    istreambuf_iterator(const proxy& p) noexcept;
    charT operator*() const;
    pointer operator->() const;
    istreambuf_iterator<charT,traits>& operator++();
    proxy operator++(int);
    bool equal(const istreambuf_iterator& b) const;
  private:
    streambuf_type* sbuf_;                // exposition only
  };

  template <class charT, class traits>
    bool operator==(const istreambuf_iterator<charT,traits>& a,
            const istreambuf_iterator<charT,traits>& b);
  template <class charT, class traits>
    bool operator!=(const istreambuf_iterator<charT,traits>& a,
            const istreambuf_iterator<charT,traits>& b);
}
```

#### Class template `istreambuf_iterator::proxy` <a id="istreambuf.iterator::proxy">[[istreambuf.iterator::proxy]]</a>

``` cpp
namespace std {
  template <class charT, class traits = char_traits<charT> >
  class istreambuf_iterator<charT, traits>::proxy {
    charT keep_;
    basic_streambuf<charT,traits>* sbuf_;
    proxy(charT c,
      basic_streambuf<charT,traits>* sbuf)
      : keep_(c), sbuf_(sbuf) { }
  public:
    charT operator*() { return keep_; }
  };
}
```

Class `istreambuf_iterator<charT,traits>::proxy` is for exposition only.
An implementation is permitted to provide equivalent functionality
without providing a class with this name. Class
`istreambuf_iterator<charT, traits>::proxy` provides a temporary
placeholder as the return value of the post-increment operator
(`operator++`). It keeps the character pointed to by the previous value
of the iterator for some possible future access to get the character.

#### `istreambuf_iterator` constructors <a id="istreambuf.iterator.cons">[[istreambuf.iterator.cons]]</a>

``` cpp
constexpr istreambuf_iterator() noexcept;
```

*Effects:* Constructs the end-of-stream iterator.

``` cpp
istreambuf_iterator(basic_istream<charT,traits>& s) noexcept;
istreambuf_iterator(basic_streambuf<charT,traits>* s) noexcept;
```

*Effects:* Constructs an `istreambuf_iterator<>` that uses the
`basic_streambuf<>` object `*(s.rdbuf())`, or `*s`, respectively.
Constructs an end-of-stream iterator if `s.rdbuf()` is null.

``` cpp
istreambuf_iterator(const proxy& p) noexcept;
```

*Effects:* Constructs a `istreambuf_iterator<>` that uses the
`basic_streambuf<>` object pointed to by the `proxy` object’s
constructor argument `p`.

#### `istreambuf_iterator::operator*` <a id="istreambuf.iterator::op*">[[istreambuf.iterator::op*]]</a>

``` cpp
charT operator*() const
```

*Returns:* The character obtained via the `streambuf` member
*`sbuf_`*`->sgetc()`.

#### `istreambuf_iterator::operator++` <a id="istreambuf.iterator::op++">[[istreambuf.iterator::op++]]</a>

``` cpp
istreambuf_iterator<charT,traits>&
    istreambuf_iterator<charT,traits>::operator++();
```

*Effects:* *`sbuf_`*`->sbumpc()`.

*Returns:* `*this`.

``` cpp
proxy istreambuf_iterator<charT,traits>::operator++(int);
```

*Returns:* `proxy(`*`sbuf_`*`->sbumpc(), `*`sbuf_`*`)`.

#### `istreambuf_iterator::equal` <a id="istreambuf.iterator::equal">[[istreambuf.iterator::equal]]</a>

``` cpp
bool equal(const istreambuf_iterator<charT,traits>& b) const;
```

*Returns:* `true` if and only if both iterators are at end-of-stream, or
neither is at end-of-stream, regardless of what `streambuf` object they
use.

#### `operator==` <a id="istreambuf.iterator::op==">[[istreambuf.iterator::op==]]</a>

``` cpp
template <class charT, class traits>
  bool operator==(const istreambuf_iterator<charT,traits>& a,
                  const istreambuf_iterator<charT,traits>& b);
```

*Returns:* `a.equal(b)`.

#### `operator!=` <a id="istreambuf.iterator::op!=">[[istreambuf.iterator::op!=]]</a>

``` cpp
template <class charT, class traits>
  bool operator!=(const istreambuf_iterator<charT,traits>& a,
                  const istreambuf_iterator<charT,traits>& b);
```

*Returns:* `!a.equal(b)`.

### Class template `ostreambuf_iterator` <a id="ostreambuf.iterator">[[ostreambuf.iterator]]</a>

``` cpp
namespace std {
  template <class charT, class traits = char_traits<charT> >
  class ostreambuf_iterator :
    public iterator<output_iterator_tag, void, void, void, void> {
  public:
    typedef charT                         char_type;
    typedef traits                        traits_type;
    typedef basic_streambuf<charT,traits> streambuf_type;
    typedef basic_ostream<charT,traits>   ostream_type;

  public:
    ostreambuf_iterator(ostream_type& s) noexcept;
    ostreambuf_iterator(streambuf_type* s) noexcept;
    ostreambuf_iterator& operator=(charT c);

    ostreambuf_iterator& operator*();
    ostreambuf_iterator& operator++();
    ostreambuf_iterator& operator++(int);
    bool failed() const noexcept;

  private:
    streambuf_type* sbuf_;                // exposition only
  };
}
```

The class template `ostreambuf_iterator` writes successive *characters*
onto the output stream from which it was constructed. It is not possible
to get a character value out of the output iterator.

#### `ostreambuf_iterator` constructors <a id="ostreambuf.iter.cons">[[ostreambuf.iter.cons]]</a>

``` cpp
ostreambuf_iterator(ostream_type& s) noexcept;
```

*Requires:* `s.rdbuf()` shall not null pointer.

*Effects:* `:sbuf_(s.rdbuf()) {}`.

``` cpp
ostreambuf_iterator(streambuf_type* s) noexcept;
```

*Requires:* `s` shall not be a null pointer.

*Effects:* `: `*`sbuf_`*`(s) {}`.

#### `ostreambuf_iterator` operations <a id="ostreambuf.iter.ops">[[ostreambuf.iter.ops]]</a>

``` cpp
ostreambuf_iterator<charT,traits>&
  operator=(charT c);
```

*Effects:* If `failed()` yields `false`, calls *`sbuf_`*`->sputc(c)`;
otherwise has no effect.

*Returns:* `*this`.

``` cpp
ostreambuf_iterator<charT,traits>& operator*();
```

*Returns:* `*this`.

``` cpp
ostreambuf_iterator<charT,traits>& operator++();
ostreambuf_iterator<charT,traits>& operator++(int);
```

*Returns:* `*this`.

``` cpp
bool failed() const noexcept;
```

*Returns:* `true` if in any prior use of member `operator=`, the call to
*`sbuf_`*`->sputc()` returned `traits::eof()`; or `false` otherwise.

### range access <a id="iterator.range">[[iterator.range]]</a>

In addition to being available via inclusion of the `<iterator>` header,
the function templates in [[iterator.range]] are available when any of
the following headers are included: `<array>`, `<deque>`,
`<forward_list>`, `<list>`, `<map>`, `<regex>`, `<set>`, `<string>`,
`<unordered_map>`, `<unordered_set>`, and `<vector>`.

``` cpp
template <class C> auto begin(C& c) -> decltype(c.begin());
template <class C> auto begin(const C& c) -> decltype(c.begin());
```

*Returns:* `c.begin()`.

``` cpp
template <class C> auto end(C& c) -> decltype(c.end());
template <class C> auto end(const C& c) -> decltype(c.end());
```

*Returns:* `c.end()`.

``` cpp
template <class T, size_t N> T* begin(T (&array)[N]);
```

*Returns:* `array`.

``` cpp
template <class T, size_t N> T* end(T (&array)[N]);
```

*Returns:* `array + N`.

<!-- Link reference definitions -->
[back.insert.iter.cons]: #back.insert.iter.cons
[back.insert.iter.op*]: #back.insert.iter.op*
[back.insert.iter.op++]: #back.insert.iter.op++
[back.insert.iter.op=]: #back.insert.iter.op=
[back.insert.iter.ops]: #back.insert.iter.ops
[back.insert.iterator]: #back.insert.iterator
[back.inserter]: #back.inserter
[bidirectional.iterators]: #bidirectional.iterators
[containers]: containers.md#containers
[copyassignable]: #copyassignable
[equalitycomparable]: #equalitycomparable
[forward.iterators]: #forward.iterators
[front.insert.iter.cons]: #front.insert.iter.cons
[front.insert.iter.op*]: #front.insert.iter.op*
[front.insert.iter.op++]: #front.insert.iter.op++
[front.insert.iter.op=]: #front.insert.iter.op=
[front.insert.iter.ops]: #front.insert.iter.ops
[front.insert.iterator]: #front.insert.iterator
[front.inserter]: #front.inserter
[input.iterators]: #input.iterators
[insert.iter.cons]: #insert.iter.cons
[insert.iter.op*]: #insert.iter.op*
[insert.iter.op++]: #insert.iter.op++
[insert.iter.op=]: #insert.iter.op=
[insert.iter.ops]: #insert.iter.ops
[insert.iterator]: #insert.iterator
[insert.iterators]: #insert.iterators
[inserter]: #inserter
[iostream.format]: input.md#iostream.format
[istream.iterator]: #istream.iterator
[istream.iterator.cons]: #istream.iterator.cons
[istream.iterator.ops]: #istream.iterator.ops
[istreambuf.iterator]: #istreambuf.iterator
[istreambuf.iterator.cons]: #istreambuf.iterator.cons
[istreambuf.iterator::equal]: #istreambuf.iterator::equal
[istreambuf.iterator::op!=]: #istreambuf.iterator::op!=
[istreambuf.iterator::op*]: #istreambuf.iterator::op*
[istreambuf.iterator::op++]: #istreambuf.iterator::op++
[istreambuf.iterator::op==]: #istreambuf.iterator::op==
[istreambuf.iterator::proxy]: #istreambuf.iterator::proxy
[iterator.basic]: #iterator.basic
[iterator.iterators]: #iterator.iterators
[iterator.operations]: #iterator.operations
[iterator.primitives]: #iterator.primitives
[iterator.range]: #iterator.range
[iterator.requirements]: #iterator.requirements
[iterator.requirements.general]: #iterator.requirements.general
[iterator.synopsis]: #iterator.synopsis
[iterator.traits]: #iterator.traits
[iterators]: #iterators
[iterators.general]: #iterators.general
[move.iter.nonmember]: #move.iter.nonmember
[move.iter.op.+]: #move.iter.op.+
[move.iter.op.+=]: #move.iter.op.+=
[move.iter.op.-]: #move.iter.op.-
[move.iter.op.-=]: #move.iter.op.-=
[move.iter.op.comp]: #move.iter.op.comp
[move.iter.op.const]: #move.iter.op.const
[move.iter.op.conv]: #move.iter.op.conv
[move.iter.op.decr]: #move.iter.op.decr
[move.iter.op.incr]: #move.iter.op.incr
[move.iter.op.index]: #move.iter.op.index
[move.iter.op.ref]: #move.iter.op.ref
[move.iter.op.star]: #move.iter.op.star
[move.iter.op=]: #move.iter.op=
[move.iter.ops]: #move.iter.ops
[move.iter.requirements]: #move.iter.requirements
[move.iterator]: #move.iterator
[move.iterators]: #move.iterators
[ostream.iterator]: #ostream.iterator
[ostream.iterator.cons.des]: #ostream.iterator.cons.des
[ostream.iterator.ops]: #ostream.iterator.ops
[ostreambuf.iter.cons]: #ostreambuf.iter.cons
[ostreambuf.iter.ops]: #ostreambuf.iter.ops
[ostreambuf.iterator]: #ostreambuf.iterator
[output.iterators]: #output.iterators
[predef.iterators]: #predef.iterators
[random.access.iterators]: #random.access.iterators
[reverse.iter.cons]: #reverse.iter.cons
[reverse.iter.conv]: #reverse.iter.conv
[reverse.iter.op!=]: #reverse.iter.op!=
[reverse.iter.op+]: #reverse.iter.op+
[reverse.iter.op++]: #reverse.iter.op++
[reverse.iter.op+=]: #reverse.iter.op+=
[reverse.iter.op-]: #reverse.iter.op-
[reverse.iter.op-=]: #reverse.iter.op-=
[reverse.iter.op.star]: #reverse.iter.op.star
[reverse.iter.op<]: #reverse.iter.op<
[reverse.iter.op<=]: #reverse.iter.op<=
[reverse.iter.op=]: #reverse.iter.op=
[reverse.iter.op==]: #reverse.iter.op==
[reverse.iter.op>]: #reverse.iter.op>
[reverse.iter.op>=]: #reverse.iter.op>=
[reverse.iter.opdiff]: #reverse.iter.opdiff
[reverse.iter.opindex]: #reverse.iter.opindex
[reverse.iter.opref]: #reverse.iter.opref
[reverse.iter.ops]: #reverse.iter.ops
[reverse.iter.opsum]: #reverse.iter.opsum
[reverse.iter.requirements]: #reverse.iter.requirements
[reverse.iterator]: #reverse.iterator
[reverse.iterators]: #reverse.iterators
[std.iterator.tags]: #std.iterator.tags
[stream.buffers]: input.md#stream.buffers
[stream.iterators]: #stream.iterators
[swappable.requirements]: library.md#swappable.requirements
[tab:iterator.bidirectional.requirements]: #tab:iterator.bidirectional.requirements
[tab:iterator.forward.requirements]: #tab:iterator.forward.requirements
[tab:iterator.input.requirements]: #tab:iterator.input.requirements
[tab:iterator.output.requirements]: #tab:iterator.output.requirements
[tab:iterator.random.access.requirements]: #tab:iterator.random.access.requirements
[tab:iterator.requirements]: #tab:iterator.requirements
[tab:iterators.lib.summary]: #tab:iterators.lib.summary
[tab:iterators.relations]: #tab:iterators.relations
[temp.inst]: temp.md#temp.inst
[utility.arg.requirements]: library.md#utility.arg.requirements

[^1]: This definition applies to pointers, since pointers are iterators.
    The effect of dereferencing an iterator that has been invalidated is
    undefined.
