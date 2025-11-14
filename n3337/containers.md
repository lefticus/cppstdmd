# Containers library <a id="containers">[[containers]]</a>

## General <a id="containers.general">[[containers.general]]</a>

This Clause describes components that C++programs may use to organize
collections of information.

The following subclauses describe container requirements, and components
for sequence containers and associative containers, as summarized in
Table  [[tab:containers.lib.summary]].

**Table: Containers library summary**

| Subclause                  |                                  | Header            |
| -------------------------- | -------------------------------- | ----------------- |
| [[container.requirements]] | Requirements                     |                   |
| [[sequences]]              | Sequence containers              | `<array>`         |
|                            |                                  | `<deque>`         |
|                            |                                  | `<forward_list>`  |
|                            |                                  | `<list>`          |
|                            |                                  | `<vector>`        |
| [[associative]]            | Associative containers           | `<map>`           |
|                            |                                  | `<set>`           |
| [[unord]]                  | Unordered associative containers | `<unordered_map>` |
|                            |                                  | `<unordered_set>` |
| [[container.adaptors]]     | Container adaptors               | `<queue>`         |
|                            |                                  | `<stack>`         |


## Container requirements <a id="container.requirements">[[container.requirements]]</a>

### General container requirements <a id="container.requirements.general">[[container.requirements.general]]</a>

Containers are objects that store other objects. They control allocation
and deallocation of these objects through constructors, destructors,
insert and erase operations.

All of the complexity requirements in this Clause are stated solely in
terms of the number of operations on the contained objects. the copy
constructor of type `vector <vector<int> >` has linear complexity, even
though the complexity of copying each contained `vector<int>` is itself
linear.

For the components affected by this subclause that declare an
`allocator_type`, objects stored in these components shall be
constructed using the `allocator_traits<allocator_type>::construct`
function and destroyed using the
`allocator_traits<allocator_type>::destroy` function (
[[allocator.traits.members]]). These functions are called only for the
container’s element type, not for internal types used by the container.
This means, for example, that a node-based container might need to
construct nodes containing aligned buffers and call `construct` to place
the element into the buffer.

In Tables  [[tab:containers.container.requirements]] and
[[tab:containers.reversible.requirements]], `X` denotes a container
class containing objects of type `T`, `a` and `b` denote values of type
`X`, `u` denotes an identifier, `r` denotes a non-const value of type
`X`, and `rv` denotes a non-const rvalue of type `X`.

Notes: the algorithm `equal()` is defined in Clause  [[algorithms]].
Those entries marked “(Note A)” or “(Note B)” have linear complexity for
`array` and have constant complexity for all other standard containers.

The member function `size()` returns the number of elements in the
container. The number of elements is defined by the rules of
constructors, inserts, and erases.

`begin()`

returns an iterator referring to the first element in the container.
`end()` returns an iterator which is the past-the-end value for the
container. If the container is empty, then `begin() == end()`;

Unless otherwise specified, all containers defined in this clause obtain
memory using an allocator (see  [[allocator.requirements]]). Copy
constructors for these container types obtain an allocator by calling
`allocator_traits<allocator_type>::select_on_container_copy_construction`
on their first parameters. Move constructors obtain an allocator by move
construction from the allocator belonging to the container being moved.
Such move construction of the allocator shall not exit via an exception.
All other constructors for these container types take an `Allocator&`
argument ([[allocator.requirements]]), an allocator whose value type is
the same as the container’s value type. If an invocation of a
constructor uses the default value of an optional allocator argument,
then the `Allocator` type must support value initialization. A copy of
this allocator is used for any memory allocation performed, by these
constructors and by all member functions, during the lifetime of each
container object or until the allocator is replaced. The allocator may
be replaced only via assignment or `swap()`. Allocator replacement is
performed by copy assignment, move assignment, or swapping of the
allocator only if
`allocator_traits<allocator_type>::propagate_on_container_copy_assignment::value`,
`allocator_traits<allocator_type>::propagate_on_container_move_assignment::value`,
or
`allocator_traits<allocator_type>::propagate_on_container_swap::value`
is true within the implementation of the corresponding container
operation. The behavior of a call to a container’s `swap` function is
undefined unless the objects being swapped have allocators that compare
equal or
`allocator_traits<allocator_type>::propagate_on_container_swap::value`
is true. In all container types defined in this Clause, the member
`get_allocator()` returns a copy of the allocator used to construct the
container or, if that allocator has been replaced, a copy of the most
recent replacement.

The expression `a.swap(b)`, for containers `a` and `b` of a standard
container type other than `array`, shall exchange the values of `a` and
`b` without invoking any move, copy, or swap operations on the
individual container elements. Any `Compare`, `Pred`, or `Hash` objects
belonging to `a` and `b` shall be swappable and shall be exchanged by
unqualified calls to non-member `swap`. If
`allocator_traits<allocator_type>::propagate_on_container_swap::value`
is `true`, then the allocators of `a` and `b` shall also be exchanged
using an unqualified call to non-member `swap`. Otherwise, they shall
not be swapped, and the behavior is undefined unless
`a.get_allocator() == b.get_allocator()`. Every iterator referring to an
element in one container before the swap shall refer to the same element
in the other container after the swap. It is unspecified whether an
iterator with value `a.end()` before the swap will have value `b.end()`
after the swap.

If the iterator type of a container belongs to the bidirectional or
random access iterator categories ([[iterator.requirements]]), the
container is called *reversible* and satisfies the additional
requirements in Table  [[tab:containers.reversible.requirements]].

Unless otherwise specified (see  [[associative.reqmts.except]],
[[unord.req.except]], [[deque.modifiers]], and [[vector.modifiers]]) all
container types defined in this Clause meet the following additional
requirements:

- if an exception is thrown by an `insert()` or `emplace()` function
  while inserting a single element, that function has no effects.
- if an exception is thrown by a `push_back()` or `push_front()`
  function, that function has no effects.
- no `erase()`, `clear()`, `pop_back()` or `pop_front()` function throws
  an exception.
- no copy constructor or assignment operator of a returned iterator
  throws an exception.
- no `swap()` function throws an exception.
- no `swap()` function invalidates any references, pointers, or
  iterators referring to the elements of the containers being swapped.
  The `end()` iterator does not refer to any element, so it may be
  invalidated.

Unless otherwise specified (either explicitly or by defining a function
in terms of other functions), invoking a container member function or
passing a container as an argument to a library function shall not
invalidate iterators to, or change the values of, objects within that
container.

Table  [[tab:containers.optional.operations]] lists operations that are
provided for some types of containers but not others. Those containers
for which the listed operations are provided shall implement the
semantics described in Table  [[tab:containers.optional.operations]]
unless otherwise stated.

Note: the algorithm `lexicographical_compare()` is defined in Clause 
[[algorithms]].

All of the containers defined in this Clause and in ([[basic.string]])
except `array` meet the additional requirements of an allocator-aware
container, as described in Table  [[tab:containers.allocatoraware]].

Given a container type `X` having an `allocator_type` identical to `A`
and a `value_type` identical to `T` and given an lvalue `m` of type `A`,
a pointer `p` of type `T*`, an expression `v` of type `T`, and an rvalue
`rv` of type `T`, the following terms are defined. (If `X` is not
allocator-aware, the terms below are defined as if `A` were
`std::allocator<T>`.)

- `T` is *`CopyInsertable` into `X`* CopyInsertable into
  X@`CopyInsertable` into `X` means that the following expression is
  well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, v);
  ```
- `T` is *`MoveInsertable` into `X`* MoveInsertable into
  X@`MoveInsertable` into `X` means that the following expression is
  well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, rv);
  ```
- `T` is *`EmplaceConstructible` into `X` from `args`*
  EmplaceConstructible into X from args@`EmplaceConstructible` into `X`
  from `args`, for zero or more arguments `args`, means that the
  following expression is well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, args);
  ```

A container calls `allocator_traits<A>::construct(m, p, args)` to
construct an element at `p` using `args`. The default `construct` in
`std::allocator` will call `::new((void*)p) T(args)`, but specialized
allocators may choose a different definition.

In Table  [[tab:containers.allocatoraware]], `X` denotes an
allocator-aware container class with a `value_type` of `T` using
allocator of type `A`, `u` denotes a variable, `a` and `b` denote
non-const lvalues of type `X`, `t` denotes an lvalue or a const rvalue
of type X``, `rv` denotes a non-const rvalue of type `X`, `m` is a value
of type `A`, and `Q` is an allocator type.

### Container data races <a id="container.requirements.dataraces">[[container.requirements.dataraces]]</a>

For purposes of avoiding data races ([[res.on.data.races]]),
implementations shall consider the following functions to be `const`:
`begin`, `end`, `rbegin`, `rend`, `front`, `back`, `data`, `find`,
`lower_bound`, `upper_bound`, `equal_range`, `at` and, except in
associative or unordered associative containers, `operator[]`.

Notwithstanding ([[res.on.data.races]]), implementations are required
to avoid data races when the contents of the contained object in
different elements in the same sequence, excepting `vector<bool>`, are
modified concurrently.

For a `vector<int> x` with a size greater than one, `x[1] = 5` and
`*x.begin() = 10` can be executed concurrently without a data race, but
`x[0] = 5` and `*x.begin() = 10` executed concurrently may result in a
data race. As an exception to the general rule, for a `vector<bool> y`,
`y[0] = true` may race with `y[1] = true`.

### Sequence containers <a id="sequence.reqmts">[[sequence.reqmts]]</a>

A sequence container organizes a finite set of objects, all of the same
type, into a strictly linear arrangement. The library provides four
basic kinds of sequence containers: `vector`, `forward_list`, `list`,
and `deque`. In addition, `array` is provided as a sequence container
which provides limited sequence operations because it has a fixed number
of elements. The library also provides container adaptors that make it
easy to construct abstract data types, such as `stack`s or `queue`s, out
of the basic sequence container kinds (or out of other kinds of sequence
containers that the user might define).

The sequence containers offer the programmer different complexity
trade-offs and should be used accordingly. `vector` or `array` is the
type of sequence container that should be used by default. `list` or
`forward_list` should be used when there are frequent insertions and
deletions from the middle of the sequence. `deque` is the data structure
of choice when most insertions and deletions take place at the beginning
or at the end of the sequence.

In Tables  [[tab:containers.sequence.requirements]] and
[[tab:containers.sequence.optional]], `X` denotes a sequence container
class, `a` denotes a value of `X` containing elements of type `T`, `A`
denotes `X::allocator_type` if it exists and `std::allocator<T>` if it
doesn’t, `i` and `j` denote iterators satisfying input iterator
requirements and refer to elements implicitly convertible to
`value_type`, `[i, j)` denotes a valid range, `il` designates an object
of type `initializer_list<value_type>`, `n` denotes a value of
`X::size_type`, `p` denotes a valid const iterator to `a`, `q` denotes a
valid dereferenceable const iterator to `a`, `[q1, q2)` denotes a valid
range of const iterators in `a`, `t` denotes an lvalue or a const rvalue
of `X::value_type`, and `rv` denotes a non-const rvalue of
`X::value_type`. `Args` denotes a template parameter pack; `args`
denotes a function parameter pack with the pattern `Args&&`.

The complexities of the expressions are sequence dependent.

`iterator`

and `const_iterator` types for sequence containers shall be at least of
the forward iterator category.

The iterator returned from `a.insert(p, t)` points to the copy of `t`
inserted into `a`.

The iterator returned from `a.insert(p, rv)` points to the copy of `rv`
inserted into `a`.

The iterator returned from `a.insert(p, n, t)` points to the copy of the
first element inserted into `a`, or `p` if `n == 0`.

The iterator returned from `a.insert(p, i, j)` points to the copy of the
first element inserted into `a`, or `p` if `i == j`.

The iterator returned from `a.insert(p, i1)` points to the copy of the
first element inserted into `a`, or `p` if `i1` is empty.

The iterator returned from `a.emplace(p, args)` points to the new
element constructed from `args` into `a`.

The iterator returned from `a.erase(q)` points to the element
immediately following `q` prior to the element being erased. If no such
element exists, `a.end()` is returned.

The iterator returned by `a.erase(q1,q2)` points to the element pointed
to by `q2` prior to any elements being erased. If no such element
exists, `a.end()` is returned.

For every sequence container defined in this Clause and in Clause 
[[strings]]:

- If the constructor
  ``` cpp
  template <class InputIterator>
  X(InputIterator first, InputIterator last,
    const allocator_type& alloc = allocator_type())
  ```

  is called with a type `InputIterator` that does not qualify as an
  input iterator, then the constructor shall not participate in overload
  resolution.
- If the member functions of the forms:
  ``` cpp
  template <class InputIterator>          // such as insert()
  rt fx1(const_iterator p, InputIterator first, InputIterator last);

  template <class InputIterator>          // such as append(), assign()
  rt fx2(InputIterator first, InputIterator last);

  template <class InputIterator>          // such as replace()
  rt fx3(const_iterator i1, const_iterator i2, InputIterator first, InputIterator last);
  ```

  are called with a type `InputIterator` that does not qualify as an
  input iterator, then these functions shall not participate in overload
  resolution.

The extent to which an implementation determines that a type cannot be
an input iterator is unspecified, except that as a minimum integral
types shall not qualify as input iterators.

Table  [[tab:containers.sequence.optional]] lists operations that are
provided for some types of sequence containers but not others. An
implementation shall provide these operations for all container types
shown in the “container” column, and shall implement them so as to take
amortized constant time.

The member function `at()` provides bounds-checked access to container
elements. `at()` throws `out_of_range` if `n >= a.size()`.

### Associative containers <a id="associative.reqmts">[[associative.reqmts]]</a>

Associative containers provide fast retrieval of data based on keys. The
library provides four basic kinds of associative containers: `set`,
`multiset`, `map` and `multimap`.

Each associative container is parameterized on `Key` and an ordering
relation `Compare` that induces a strict weak ordering (
[[alg.sorting]]) on elements of `Key`. In addition, `map` and `multimap`
associate an arbitrary type `T` with the `Key`. The object of type
`Compare` is called the *comparison object* of a container.

The phrase “equivalence of keys” means the equivalence relation imposed
by the comparison and *not* the `operator==` on keys. That is, two keys
`k1` and `k2` are considered to be equivalent if for the comparison
object `comp`, `comp(k1, k2) == false && comp(k2, k1) == false`. For any
two keys `k1` and `k2` in the same container, calling `comp(k1, k2)`
shall always return the same value.

An associative container supports *unique keys* if it may contain at
most one element for each key. Otherwise, it supports *equivalent keys*.
The `set` and `map` classes support unique keys; the `multiset` and
`multimap` classes support equivalent keys. For `multiset` and
`multimap`, `insert`, `emplace`, and `erase` preserve the relative
ordering of equivalent elements.

For `set` and `multiset` the value type is the same as the key type. For
`map` and `multimap` it is equal to `pair<const Key, T>`. Keys in an
associative container are immutable.

`iterator`

of an associative container is of the bidirectional iterator category.
For associative containers where the value type is the same as the key
type, both `iterator` and `const_iterator` are constant iterators. It is
unspecified whether or not `iterator` and `const_iterator` are the same
type. `iterator` and `const_iterator` have identical semantics in this
case, and `iterator` is convertible to `const_iterator`. Users can avoid
violating the One Definition Rule by always using `const_iterator` in
their function parameter lists.

The associative containers meet all the requirements of Allocator-aware
containers ([[container.requirements.general]]), except that for `map`
and `multimap`, the requirements placed on `value_type` in Table 
[[tab:containers.container.requirements]] apply instead to `key_type`
and `mapped_type`. For example, in some cases `key_type` and
`mapped_type` are required to be `CopyAssignable` even though the
associated `value_type`, `pair<const key_type, mapped_type>`, is not
`CopyAssignable`.

In Table  [[tab:containers.associative.requirements]], `X` denotes an
associative container class, `a` denotes a value of `X`, `a_uniq`
denotes a value of `X` when `X` supports unique keys, `a_eq` denotes a
value of `X` when `X` supports multiple keys, `u` denotes an identifier,
`i` and `j` satisfy input iterator requirements and refer to elements
implicitly convertible to `value_type`, \[`i`, `j`) denotes a valid
range, `p` denotes a valid const iterator to `a`, `q` denotes a valid
dereferenceable const iterator to `a`, `[q1, q2)` denotes a valid range
of const iterators in `a`, `il` designates an object of type
`initializer_list<value_type>`, `t` denotes a value of `X::value_type`,
`k` denotes a value of `X::key_type` and `c` denotes a value of type
`X::key_compare`. `A` denotes the storage allocator used by `X`, if any,
or `std::allocator<X::value_type>` otherwise, and `m` denotes an
allocator of a type convertible to `A`.

The `insert` and `emplace` members shall not affect the validity of
iterators and references to the container, and the erase members shall
invalidate only iterators and references to the erased elements.

The fundamental property of iterators of associative containers is that
they iterate through the containers in the non-descending order of keys
where non-descending is defined by the comparison that was used to
construct them. For any two dereferenceable iterators `i` and `j` such
that distance from `i` to `j` is positive,

``` cpp
value_comp(*j, *i) == false
```

For associative containers with unique keys the stronger condition
holds,

``` cpp
value_comp(*i, *j) != false.
```

When an associative container is constructed by passing a comparison
object the container shall not store a pointer or reference to the
passed object, even if that object is passed by reference. When an
associative container is copied, either through a copy constructor or an
assignment operator, the target container shall then use the comparison
object from the container being copied, as if that comparison object had
been passed to the target container in its constructor.

#### Exception safety guarantees <a id="associative.reqmts.except">[[associative.reqmts.except]]</a>

For associative containers, no `clear()` function throws an exception.
`erase(k)` does not throw an exception unless that exception is thrown
by the container’s `Compare` object (if any).

For associative containers, if an exception is thrown by any operation
from within an `insert` or `emplace` function inserting a single
element, the insertion has no effect.

For associative containers, no `swap` function throws an exception
unless that exception is thrown by the swap of the container’s `Compare`
object (if any).

### Unordered associative containers <a id="unord.req">[[unord.req]]</a>

Unordered associative containers provide an ability for fast retrieval
of data based on keys. The worst-case complexity for most operations is
linear, but the average case is much faster. The library provides four
unordered associative containers: `unordered_set`, `unordered_map`,
`unordered_multiset`, and `unordered_multimap`.

Unordered associative containers conform to the requirements for
Containers ([[container.requirements]]), except that the expressions
`a == b` and `a != b` have different semantics than for the other
container types.

Each unordered associative container is parameterized by `Key`, by a
function object type `Hash` that meets the `Hash` requirements (
[[hash.requirements]]) and acts as a hash function for argument values
of type `Key`, and by a binary predicate `Pred` that induces an
equivalence relation on values of type `Key`. Additionally,
`unordered_map` and `unordered_multimap` associate an arbitrary *mapped
type* `T` with the `Key`.

A hash function is a function object that takes a single argument of
type `Key` and returns a value of type `std::size_t`.

Two values `k1` and `k2` of type `Key` are considered equivalent if the
container’s `key_equal` function object returns `true` when passed those
values. If `k1` and `k2` are equivalent, the hash function shall return
the same value for both. Thus, when an unordered associative container
is instantiated with a non-default `Pred` parameter it usually needs a
non-default `Hash` parameter as well.

An unordered associative container supports *unique keys* if it may
contain at most one element for each key. Otherwise, it supports
*equivalent keys*. `unordered_set` and `unordered_map` support unique
keys. `unordered_multiset` and `unordered_multimap` support equivalent
keys. In containers that support equivalent keys, elements with
equivalent keys are adjacent to each other in the iteration order of the
container. Thus, although the absolute order of elements in an unordered
container is not specified, its elements are grouped into
*equivalent-key group*s such that all elements of each group have
equivalent keys. Mutating operations on unordered containers shall
preserve the relative order of elements within each equivalent-key group
unless otherwise specified.

For `unordered_set` and `unordered_multiset` the value type is the same
as the key type. For `unordered_map` and `unordered_multimap` it is
`std::pair<const Key,
T>`.

The elements of an unordered associative container are organized into
*buckets*. Keys with the same hash code appear in the same bucket. The
number of buckets is automatically increased as elements are added to an
unordered associative container, so that the average number of elements
per bucket is kept below a bound. Rehashing invalidates iterators,
changes ordering between elements, and changes which buckets elements
appear in, but does not invalidate pointers or references to elements.
For `unordered_multiset` and `unordered_multimap`, rehashing preserves
the relative ordering of equivalent elements.

The unordered associative containers meet all the requirements of
Allocator-aware containers ([[container.requirements.general]]), except
that for `unordered_map` and `unordered_multimap`, the requirements
placed on `value_type` in Table 
[[tab:containers.container.requirements]] apply instead to `key_type`
and `mapped_type`. For example, `key_type` and `mapped_type` are
sometimes required to be `CopyAssignable` even though the associated
`value_type`, `pair<const key_type, mapped_type>`, is not
`CopyAssignable`.

In table  [[tab:HashRequirements]]: `X` is an unordered associative
container class, `a` is an object of type `X`, `b` is a possibly const
object of type `X`, `a_uniq` is an object of type `X` when `X` supports
unique keys, `a_eq` is an object of type `X` when `X` supports
equivalent keys, `i` and `j` are input iterators that refer to
`value_type`, `[i, j)` is a valid range, `p` and `q2` are valid const
iterators to `a`, `q` and `q1` are valid dereferenceable const iterators
to `a`, `[q1, q2)` is a valid range in `a`, `il` designates an object of
type `initializer_list<value_type>`, `t` is a value of type
`X::value_type`, `k` is a value of type `key_type`, `hf` is a possibly
const value of type `hasher`, `eq` is a possibly const value of type
`key_equal`, `n` is a value of type `size_type`, and `z` is a value of
type `float`.

Two unordered containers `a` and `b` compare equal if
`a.size() == b.size()` and, for every equivalent-key group \[`Ea1`,
`Ea2`) obtained from `a.equal_range(Ea1)`, there exists an
equivalent-key group \[`Eb1`, `Eb2`) obtained from `b.equal_range(Ea1)`,
such that `distance(Ea1, Ea2) == distance(Eb1, Eb2)` and
`is_permutation(Ea1, Ea2, Eb1)` returns `true`. For `unordered_set` and
`unordered_map`, the complexity of `operator==` (i.e., the number of
calls to the `==` operator of the `value_type`, to the predicate
returned by `key_equal()`, and to the hasher returned by
`hash_function()`) is proportional to N in the average case and to N² in
the worst case, where N is a.size(). For `unordered_multiset` and
`unordered_multimap`, the complexity of `operator==` is proportional to
$\sum E_i^2$ in the average case and to N² in the worst case, where N is
`a.size()`, and Eᵢ is the size of the iᵗʰ equivalent-key group in `a`.
However, if the respective elements of each corresponding pair of
equivalent-key groups Eaᵢ and Ebᵢ are arranged in the same order (as is
commonly the case, e.g., if `a` and `b` are unmodified copies of the
same container), then the average-case complexity for
`unordered_multiset` and `unordered_multimap` becomes proportional to N
(but worst-case complexity remains , e.g., for a pathologically bad hash
function). The behavior of a program that uses `operator==` or
`operator!=` on unordered containers is undefined unless the `Hash` and
`Pred` function objects respectively have the same behavior for both
containers and the equality comparison operator for `Key` is a
refinement[^1] of the partition into equivalent-key groups produced by
`Pred`.

The iterator types `iterator` and `const_iterator` of an unordered
associative container are of at least the forward iterator category. For
unordered associative containers where the key type and value type are
the same, both `iterator` and `const_iterator` are const iterators.

The `insert` and `emplace` members shall not affect the validity of
references to container elements, but may invalidate all iterators to
the container. The erase members shall invalidate only iterators and
references to the erased elements.

The `insert` and `emplace` members shall not affect the validity of
iterators if `(N+n) < z * B`, where `N` is the number of elements in the
container prior to the insert operation, `n` is the number of elements
inserted, `B` is the container’s bucket count, and `z` is the
container’s maximum load factor.

#### Exception safety guarantees <a id="unord.req.except">[[unord.req.except]]</a>

For unordered associative containers, no `clear()` function throws an
exception. `erase(k)` does not throw an exception unless that exception
is thrown by the container’s `Hash` or `Pred` object (if any).

For unordered associative containers, if an exception is thrown by any
operation other than the container’s hash function from within an
`insert` or `emplace` function inserting a single element, the insertion
has no effect.

For unordered associative containers, no `swap` function throws an
exception unless that exception is thrown by the swap of the container’s
Hash or Pred object (if any).

For unordered associative containers, if an exception is thrown from
within a `rehash()` function other than by the container’s hash function
or comparison function, the `rehash()` function has no effect.

## Sequence containers <a id="sequences">[[sequences]]</a>

### In general <a id="sequences.general">[[sequences.general]]</a>

The headers `<array>`, `<deque>`, `<forward_list>`, `<list>`, and
`<vector>` define template classes that meet the requirements for
sequence containers.

The headers `<queue>` and `<stack>` define container adaptors (
[[container.adaptors]]) that also meet the requirements for sequence
containers.

\synopsis{Header \texttt{\<array\>} synopsis}

``` cpp
#include <initializer_list>

namespace std {
  template <class T, size_t N > struct array;
  template <class T, size_t N>
    bool operator==(const array<T,N>& x, const array<T,N>& y);
  template <class T, size_t N>
    bool operator!=(const array<T,N>& x, const array<T,N>& y);
  template <class T, size_t N>
    bool operator<(const array<T,N>& x, const array<T,N>& y);
  template <class T, size_t N>
    bool operator>(const array<T,N>& x, const array<T,N>& y);
  template <class T, size_t N>
    bool operator<=(const array<T,N>& x, const array<T,N>& y);
  template <class T, size_t N>
    bool operator>=(const array<T,N>& x, const array<T,N>& y);
  template <class T, size_t N >
    void swap(array<T,N>& x, array<T,N>& y) noexcept(noexcept(x.swap(y)));

  template <class T> class tuple_size;
  template <size_t I, class T> class tuple_element;
  template <class T, size_t N>
    struct tuple_size<array<T, N> >;
  template <size_t I, class T, size_t N>
    struct tuple_element<I, array<T, N> >;
  template <size_t I, class T, size_t N>
    T& get(array<T, N>&) noexcept;
  template <size_t I, class T, size_t N>
    T&& get(array<T, N>&&) noexcept;
  template <size_t I, class T, size_t N>
    const T& get(const array<T, N>&) noexcept;
}
```

\synopsis{Header \texttt{\<deque\>} synopsis}

``` cpp
#include <initializer_list>

namespace std {
  template <class T, class Allocator = allocator<T> > class deque;
  template <class T, class Allocator>
    bool operator==(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    void swap(deque<T,Allocator>& x, deque<T,Allocator>& y);
}
```

\synopsis{Header \texttt{\<forward_list\>} synopsis}

``` cpp
#include <initializer_list>

namespace std {
  template <class T, class Allocator = allocator<T> > class forward_list;
  template <class T, class Allocator>
    bool operator==(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    void swap(forward_list<T,Allocator>& x, forward_list<T,Allocator>& y);
}
```

\synopsis{Header \texttt{\<list\>} synopsis}

``` cpp
#include <initializer_list>

namespace std {
  template <class T, class Allocator = allocator<T> > class list;
  template <class T, class Allocator>
    bool operator==(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    void swap(list<T,Allocator>& x, list<T,Allocator>& y);
}
```

\synopsis{Header \texttt{\<vector\>} synopsis}

``` cpp
#include <initializer_list>

namespace std {
  template <class T, class Allocator = allocator<T> > class vector;
  template <class T, class Allocator>
    bool operator==(const vector<T,Allocator>& x,const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const vector<T,Allocator>& x,const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const vector<T,Allocator>& x,const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const vector<T,Allocator>& x,const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const vector<T,Allocator>& x,const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const vector<T,Allocator>& x,const vector<T,Allocator>& y);
  template <class T, class Allocator>
    void swap(vector<T,Allocator>& x, vector<T,Allocator>& y);

  template <class Allocator> class vector<bool,Allocator>;

  // hash support
  template <class T> struct hash;
  template <class Allocator> struct hash<vector<bool, Allocator> >;
```

### Class template `array` <a id="array">[[array]]</a>

#### Class template `array` overview <a id="array.overview">[[array.overview]]</a>

The header `<array>` defines a class template for storing fixed-size
sequences of objects. An `array` supports random access iterators. An
instance of `array<T, N>` stores `N` elements of type `T`, so that
`size() == N` is an invariant. The elements of an `array` are stored
contiguously, meaning that if `a` is an `array<T, N>` then it obeys the
identity `&a[n] == &a[0] + n` for all `0 <= n < N`.

An `array` is an aggregate ([[dcl.init.aggr]]) that can be initialized
with the syntax

``` cpp
array<T, N> a = { initializer-list };
```

where *initializer-list* is a comma-separated list of up to `N` elements
whose types are convertible to `T`.

An `array` satisfies all of the requirements of a container and of a
reversible container ([[container.requirements]]), except that a
default constructed `array` object is not empty and that `swap` does not
have constant complexity. An `array` satisfies some of the requirements
of a sequence container ([[sequence.reqmts]]). Descriptions are
provided here only for operations on `array` that are not described in
one of these tables and for operations where there is additional
semantic information.

``` cpp
namespace std {
  template <class T, size_t N >
  struct array {
    //  types:
    typedef T&                                    reference;
    typedef const T&                              const_reference;
    typedef implementation-defined  // type of array::iterator                iterator;
    typedef implementation-defined  // type of array::const_iterator                const_iterator;
    typedef size_t                                size_type;
    typedef ptrdiff_t                             difference_type;
    typedef T                                     value_type;
    typedef T*                                    pointer;
    typedef const T*                              const_pointer;
    typedef reverse_iterator<iterator>            reverse_iterator;
    typedef reverse_iterator<const_iterator>      const_reverse_iterator;

    T       elems[N];           // exposition only

    // no explicit construct/copy/destroy for aggregate type

    void fill(const T& u);
    void swap(array&) noexcept(noexcept(swap(declval<T&>(), declval<T&>())));

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;

    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // capacity:
    constexpr size_type size() noexcept;
    constexpr size_type max_size() noexcept;
    constexpr bool      empty() noexcept;

    // element access:
    reference       operator[](size_type n);
    const_reference operator[](size_type n) const;
    const_reference at(size_type n) const;
    reference       at(size_type n);
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    T *       data() noexcept;
    const T * data() const noexcept;
  };
}
```

The member variable `elems` is shown for exposition only, to emphasize
that `array` is a class aggregate. The name `elems` is not part of
`array`’s interface.

#### `array` constructors, copy, and assignment <a id="array.cons">[[array.cons]]</a>

The conditions for an aggregate ([[dcl.init.aggr]]) shall be met. Class
`array` relies on the implicitly-declared special member functions (
[[class.ctor]], [[class.dtor]], and [[class.copy]]) to conform to the
container requirements table in  [[container.requirements]]. In addition
to the requirements specified in the container requirements table, the
implicit move constructor and move assignment operator for `array`
require that `T` be `MoveConstructible` or `MoveAssignable`,
respectively.

#### `array` specialized algorithms <a id="array.special">[[array.special]]</a>

``` cpp
template <class T, size_t N> void swap(array<T,N>& x, array<T,N>& y) noexcept(noexcept(x.swap(y)));
```

*Effects:*

``` cpp
x.swap(y);
```

*Complexity:* linear in `N`.

#### `array::size` <a id="array.size">[[array.size]]</a>

``` cpp
template <class T, size_t N> constexpr size_type array<T,N>::size() noexcept;
```

*Returns:* `N`

#### `array::data` <a id="array.data">[[array.data]]</a>

``` cpp
T *data() noexcept;
const T *data() const noexcept;
```

*Returns:* `elems`.

#### `array::fill` <a id="array.fill">[[array.fill]]</a>

``` cpp
void fill(const T& u);
```

*Effects:* `fill_n(begin(), N, u)`

#### `array::swap` <a id="array.swap">[[array.swap]]</a>

``` cpp
void swap(array& y) noexcept(noexcept(swap(declval<T&>(), declval<T&>())));
```

*Effects:* `swap_ranges(begin(), end(), y.begin())`

*Throws:* Nothing unless one of the element-wise swap calls throws an
exception.

*Note:* Unlike the `swap` function for other containers, array::swap
takes linear time, may exit via an exception, and does not cause
iterators to become associated with the other container.

#### Zero sized arrays <a id="array.zero">[[array.zero]]</a>

`array` shall provide support for the special case `N == 0`.

In the case that `N == 0`, `begin() == end() ==` unique value. The
return value of `data()` is unspecified.

The effect of calling `front()` or `back()` for a zero-sized array is
undefined.

Member function `swap()` shall have a *noexcept-specification* which is
equivalent to `noexcept(true)`.

#### Tuple interface to class template `array` <a id="array.tuple">[[array.tuple]]</a>

``` cpp
tuple_size<array<T, N> >::value
```

*Return type:* integral constant expression.

*Value:* `N`

``` cpp
tuple_element<I, array<T, N> >::type
```

*Requires:* `I < N`. The program is ill-formed if `I` is out of bounds.

*Value:* The type T.

``` cpp
template <size_t I, class T, size_t N> T& get(array<T, N>& a) noexcept;
```

*Requires:* `I < N`. The program is ill-formed if `I` is out of bounds.

*Returns:* A reference to the `I`th element of `a`, where indexing is
zero-based.

``` cpp
template <size_t I, class T, size_t N> T&& get(array<T, N>&& a) noexcept;
```

*Effects:* Equivalent to `return std::move(get<I>(a));`

``` cpp
template <size_t I, class T, size_t N> const T& get(const array<T, N>& a) noexcept;
```

*Requires:* `I < N`. The program is ill-formed if `I` is out of bounds.

*Returns:* A const reference to the `I`th element of `a`, where indexing
is zero-based.

### Class template `deque` <a id="deque">[[deque]]</a>

#### Class template `deque` overview <a id="deque.overview">[[deque.overview]]</a>

A `deque` is a sequence container that, like a `vector` ([[vector]]),
supports random access iterators. In addition, it supports constant time
insert and erase operations at the beginning or the end; insert and
erase in the middle take linear time. That is, a deque is especially
optimized for pushing and popping elements at the beginning and end. As
with vectors, storage management is handled automatically.

A `deque` satisfies all of the requirements of a container, of a
reversible container (given in tables in  [[container.requirements]]),
of a sequence container, including the optional sequence container
requirements ([[sequence.reqmts]]), and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). Descriptions are provided
here only for operations on `deque` that are not described in one of
these tables or for operations where there is additional semantic
information.

``` cpp
namespace std {
  template <class T, class Allocator = allocator<T> >
  class deque {
  public:
    // types:
    typedef value_type&                           reference;
    typedef const value_type&                     const_reference;
    typedef implementation-defined                iterator;       // See [container.requirements]
    typedef implementation-defined                const_iterator; // See [container.requirements]
    typedef implementation-defined                size_type;      // See [container.requirements]
    typedef implementation-defined                difference_type;// See [container.requirements]
    typedef T                                     value_type;
    typedef Allocator                             allocator_type;
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    // [deque.cons], construct/copy/destroy:
    explicit deque(const Allocator& = Allocator());
    explicit deque(size_type n);
    deque(size_type n, const T& value,const Allocator& = Allocator());
    template <class InputIterator>
      deque(InputIterator first, InputIterator last,const Allocator& = Allocator());
    deque(const deque& x);
    deque(deque&&);
    deque(const deque&, const Allocator&);
    deque(deque&&, const Allocator&);
    deque(initializer_list<T>, const Allocator& = Allocator());

    ~deque();
    deque& operator=(const deque& x);
    deque& operator=(deque&& x);
    deque& operator=(initializer_list<T>);
    template <class InputIterator>
      void assign(InputIterator first, InputIterator last);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;
    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // [deque.capacity], capacity:
    size_type size() const noexcept;
    size_type max_size() const noexcept;
    void      resize(size_type sz);
    void      resize(size_type sz, const T& c);
    void      shrink_to_fit();
    bool      empty() const noexcept;

    // element access:
    reference       operator[](size_type n);
    const_reference operator[](size_type n) const;
    reference       at(size_type n);
    const_reference at(size_type n) const;
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    // [deque.modifiers], modifiers:
    template <class... Args> void emplace_front(Args&&... args);
    template <class... Args> void emplace_back(Args&&... args);
    template <class... Args> iterator emplace(const_iterator position, Args&&... args);

    void push_front(const T& x);
    void push_front(T&& x);
    void push_back(const T& x);
    void push_back(T&& x);

    iterator insert(const_iterator position, const T& x);
    iterator insert(const_iterator position, T&& x);
    iterator insert(const_iterator position, size_type n, const T& x);
    template <class InputIterator>
      iterator insert (const_iterator position, InputIterator first, InputIterator last);
    iterator insert(const_iterator position, initializer_list<T>);

    void pop_front();
    void pop_back();

    iterator erase(const_iterator position);
    iterator erase(const_iterator first, const_iterator last);
    void     swap(deque&);
    void     clear() noexcept;
  };

  template <class T, class Allocator>
    bool operator==(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const deque<T,Allocator>& x, const deque<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const deque<T,Allocator>& x, const deque<T,Allocator>& y);

  // specialized algorithms:
  template <class T, class Allocator>
    void swap(deque<T,Allocator>& x, deque<T,Allocator>& y);
}
```

#### `deque` constructors, copy, and assignment <a id="deque.cons">[[deque.cons]]</a>

``` cpp
explicit deque(const Allocator& = Allocator());
```

*Effects:* Constructs an empty `deque`, using the specified allocator.

*Complexity:* Constant.

``` cpp
explicit deque(size_type n);
```

*Effects:* Constructs a `deque` with `n` value-initialized elements.

*Requires:* `T` shall be `DefaultConstructible`.

*Complexity:* Linear in `n`.

``` cpp
deque(size_type n, const T& value,
      const Allocator& = Allocator());
```

*Effects:* Constructs a `deque` with `n` copies of `value`, using the
specified allocator.

*Requires:* `T` shall be `CopyInsertable` into `*this`.

*Complexity:* Linear in `n`.

``` cpp
template <class InputIterator>
  deque(InputIterator first, InputIterator last,
        const Allocator& = Allocator());
```

*Effects:* Constructs a `deque` equal to the range \[`first`, `last`),
using the specified allocator.

*Complexity:* `distance(first, last)`.

``` cpp
template <class InputIterator>
  void assign(InputIterator first, InputIterator last);
```

*Effects:*

``` cpp
erase(begin(), end());
insert(begin(), first, last);
```

``` cpp
void assign(size_type n, const T& t);
```

*Effects:*

``` cpp
erase(begin(), end());
insert(begin(), n, t);
```

#### `deque` capacity <a id="deque.capacity">[[deque.capacity]]</a>

``` cpp
void resize(size_type sz);
```

*Effects:* If `sz <= size()`, equivalent to
`erase(begin() + sz, end());`. If `size() < sz`, appends `sz - size()`
value-initialized elements to the sequence.

*Requires:* `T` shall be `DefaultConstructible`.

``` cpp
void resize(size_type sz, const T& c);
```

*Effects:*

``` cpp
if (sz > size())
  insert(end(), sz-size(), c);
else if (sz < size())
  erase(begin()+sz, end());
else
  ;                 // do nothing
```

*Requires:* `T` shall be `CopyInsertable` into `*this`.

``` cpp
void shrink_to_fit();
```

*Remarks:* `shrink_to_fit` is a non-binding request to reduce memory
use. The request is non-binding to allow latitude for
implementation-specific optimizations.

#### `deque` modifiers <a id="deque.modifiers">[[deque.modifiers]]</a>

``` cpp
iterator insert(const_iterator position, const T& x);
iterator insert(const_iterator position, T&& x);
iterator insert(const_iterator position, size_type n, const T& x);
template <class InputIterator>
  iterator insert(const_iterator position,
                  InputIterator first, InputIterator last);
iterator insert(const_iterator position, initializer_list<T>);

template <class... Args> void emplace_front(Args&&... args);
template <class... Args> void emplace_back(Args&&... args);
template <class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_front(const T& x);
void push_front(T&& x);
void push_back(const T& x);
void push_back(T&& x);
```

*Effects:* An insertion in the middle of the deque invalidates all the
iterators and references to elements of the deque. An insertion at
either end of the deque invalidates all the iterators to the deque, but
has no effect on the validity of references to elements of the deque.

If an exception is thrown other than by the copy constructor, move
constructor, assignment operator, or move assignment operator of `T`
there are no effects. If an exception is thrown by the move constructor
of a non-`CopyInsertable` `T`, the effects are unspecified.

*Complexity:* The complexity is linear in the number of elements
inserted plus the lesser of the distances to the beginning and end of
the deque. Inserting a single element either at the beginning or end of
a deque always takes constant time and causes a single call to a
constructor of `T`.

``` cpp
iterator erase(const_iterator position);
iterator erase(const_iterator first, const_iterator last);
```

*Effects:* An erase operation that erases the last element of a deque
invalidates only the past-the-end iterator and all iterators and
references to the erased elements. An erase operation that erases the
first element of a deque but not the last element invalidates only the
erased elements. An erase operation that erases neither the first
element nor the last element of a deque invalidates the past-the-end
iterator and all iterators and references to all the elements of the
deque.

*Complexity:* The number of calls to the destructor is the same as the
number of elements erased, but the number of calls to the assignment
operator is no more than the lesser of the number of elements before the
erased elements and the number of elements after the erased elements.

*Throws:* Nothing unless an exception is thrown by the copy constructor,
move constructor, assignment operator, or move assignment operator of
`T`.

#### `deque` specialized algorithms <a id="deque.special">[[deque.special]]</a>

``` cpp
template <class T, class Allocator>
  void swap(deque<T,Allocator>& x, deque<T,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

### Class template `forward_list` <a id="forwardlist">[[forwardlist]]</a>

#### Class template `forward_list` overview <a id="forwardlist.overview">[[forwardlist.overview]]</a>

A `forward_list` is a container that supports forward iterators and
allows constant time insert and erase operations anywhere within the
sequence, with storage management handled automatically. Fast random
access to list elements is not supported. It is intended that
`forward_list` have zero space or time overhead relative to a
hand-written C-style singly linked list. Features that would conflict
with that goal have been omitted.

A `forward_list` satisfies all of the requirements of a container
(Table  [[tab:containers.container.requirements]]), except that the
`size()` member function is not provided. A `forward_list` also
satisfies all of the requirements for an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). In addition, a
`forward_list` provides the `assign` member functions (Table 
[[tab:containers.sequence.requirements]]) and several of the optional
container requirements (Table  [[tab:containers.sequence.optional]]).
Descriptions are provided here only for operations on `forward_list`
that are not described in that table or for operations where there is
additional semantic information.

Modifying any list requires access to the element preceding the first
element of interest, but in a `forward_list` there is no constant-time
way to acess a preceding element. For this reason, ranges that are
modified, such as those supplied to `erase` and `splice`, must be open
at the beginning.

``` cpp
namespace std {
  template <class T, class Allocator = allocator<T> >
  class forward_list {
  public:
    // types:
    typedef value_type&                                           reference;
    typedef const value_type&                                     const_reference;
    typedef implementation-defined iterator;       // See [container.requirements]
    typedef implementation-defined const_iterator; // See [container.requirements]
    typedef implementation-defined size_type;      // See [container.requirements]
    typedef implementation-defined difference_type;// See [container.requirements]
    typedef T value_type;
    typedef Allocator allocator_type;
    typedef typename allocator_traits<Allocator>::pointer         pointer;
    typedef typename allocator_traits<Allocator>::const_pointer   const_pointer;

    // [forwardlist.cons], construct/copy/destroy:
    explicit forward_list(const Allocator& = Allocator());
    explicit forward_list(size_type n);
    forward_list(size_type n, const T& value,
                 const Allocator& = Allocator());
    template <class InputIterator>
      forward_list(InputIterator first, InputIterator last,
                   const Allocator& = Allocator());
    forward_list(const forward_list& x);
    forward_list(forward_list&& x);
    forward_list(const forward_list& x, const Allocator&);
    forward_list(forward_list&& x, const Allocator&);
    forward_list(initializer_list<T>, const Allocator& = Allocator());
    ~forward_list();
    forward_list& operator=(const forward_list& x);
    forward_list& operator=(forward_list&& x);
    forward_list& operator=(initializer_list<T>);
    template <class InputIterator>
      void assign(InputIterator first, InputIterator last);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // [forwardlist.iter], iterators:
    iterator before_begin() noexcept;
    const_iterator before_begin() const noexcept;
    iterator begin() noexcept;
    const_iterator begin() const noexcept;
    iterator end() noexcept;
    const_iterator end() const noexcept;

    const_iterator cbegin() const noexcept;
    const_iterator cbefore_begin() const noexcept;
    const_iterator cend() const noexcept;

    // capacity:
    bool empty() const noexcept;
    size_type max_size() const noexcept;

    // [forwardlist.access], element access:
    reference front();
    const_reference front() const;

    // [forwardlist.modifiers], modifiers:
    template <class... Args> void emplace_front(Args&&... args);
    void push_front(const T& x);
    void push_front(T&& x);
    void pop_front();

    template <class... Args> iterator emplace_after(const_iterator position, Args&&... args);
    iterator insert_after(const_iterator position, const T& x);
    iterator insert_after(const_iterator position, T&& x);

    iterator insert_after(const_iterator position, size_type n, const T& x);
    template <class InputIterator>
      iterator insert_after(const_iterator position, InputIterator first, InputIterator last);
    iterator insert_after(const_iterator position, initializer_list<T> il);

    iterator erase_after(const_iterator position);
    iterator erase_after(const_iterator position, const_iterator last);
    void swap(forward_list&);

    void resize(size_type sz);
    void resize(size_type sz, const value_type& c);
    void clear() noexcept;

    // [forwardlist.ops], forward_list operations:
    void splice_after(const_iterator position, forward_list& x);
    void splice_after(const_iterator position, forward_list&& x);
    void splice_after(const_iterator position, forward_list& x,
                      const_iterator i);
    void splice_after(const_iterator position, forward_list&& x,
                      const_iterator i);
    void splice_after(const_iterator position, forward_list& x,
                      const_iterator first, const_iterator last);
    void splice_after(const_iterator position, forward_list&& x,
                      const_iterator first, const_iterator last);

    void remove(const T& value);
    template <class Predicate> void remove_if(Predicate pred);

    void unique();
    template <class BinaryPredicate> void unique(BinaryPredicate binary_pred);

    void merge(forward_list& x);
    void merge(forward_list&& x);
    template <class Compare> void merge(forward_list& x, Compare comp);
    template <class Compare> void merge(forward_list&& x, Compare comp);

    void sort();
    template <class Compare> void sort(Compare comp);

    void reverse() noexcept;
  };

  // Comparison operators
  template <class T, class Allocator>
    bool operator==(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const forward_list<T,Allocator>& x, const forward_list<T,Allocator>& y);

  // [forwardlist.spec], specialized algorithms:
  template <class T, class Allocator>
    void swap(forward_list<T,Allocator>& x, forward_list<T,Allocator>& y);
}
```

#### `forward_list` constructors, copy, assignment <a id="forwardlist.cons">[[forwardlist.cons]]</a>

``` cpp
explicit forward_list(const Allocator& = Allocator());
```

*Effects:* Constructs an empty `forward_list` object using the specified
allocator.

*Complexity:* Constant.

``` cpp
explicit forward_list(size_type n);
```

*Effects:* Constructs a `forward_list` object with `n` value-initialized
elements.

*Requires:* `T` shall be `DefaultConstructible`.

*Complexity:* Linear in `n`.

``` cpp
forward_list(size_type n, const T& value, const Allocator& = Allocator());
```

*Effects:* Constructs a `forward_list` object with `n` copies of `value`
using the specified allocator.

*Requires:* `T` shall be `CopyInsertable` into `*this`.

*Complexity:* Linear in `n`.

``` cpp
template <class InputIterator>
  forward_list(InputIterator first, InputIterator last, const Allocator& = Allocator());
```

*Effects:* Constructs a `forward_list` object equal to the range
\[`first`, `last`).

*Complexity:* Linear in `distance(first, last)`.

``` cpp
template <class InputIterator>
  void assign(InputIterator first, InputIterator last);
```

*Effects:* `clear(); insert_after(before_begin(), first, last);`

``` cpp
void assign(size_type n, const T& t);
```

*Effects:* `clear(); insert_after(before_begin(), n, t);`

#### `forward_list` iterators <a id="forwardlist.iter">[[forwardlist.iter]]</a>

``` cpp
iterator before_begin() noexcept;
const_iterator before_begin() const noexcept;
const_iterator cbefore_begin() const noexcept;
```

*Returns:* A non-dereferenceable iterator that, when incremented, is
equal to the iterator returned by `begin()`.

*Effects:* `cbefore_begin()` is equivalent to
`const_cast<forward_list const&>(*this).before_begin()`.

*Remarks:* `before_begin() == end()` shall equal `false`.

#### `forward_list` element access <a id="forwardlist.access">[[forwardlist.access]]</a>

``` cpp
reference front();
const_reference front() const;
```

*Returns:* `*begin()`

#### `forward_list` modifiers <a id="forwardlist.modifiers">[[forwardlist.modifiers]]</a>

None of the overloads of `insert_after` shall affect the validity of
iterators and references, and `erase_after` shall invalidate only
iterators and references to the erased elements. If an exception is
thrown during `insert_after` there shall be no effect. Inserting `n`
elements into a `forward_list` is linear in `n`, and the number of calls
to the copy or move constructor of `T` is exactly equal to `n`. Erasing
`n` elements from a `forward_list` is linear in `n` and the number of
calls to the destructor of type `T` is exactly equal to `n`.

``` cpp
template <class... Args> void emplace_front(Args&&... args);
```

*Effects:* Inserts an object of type `value_type` constructed with
`value_type(std::forward<Args>(args)...)` at the beginning of the list.

``` cpp
void push_front(const T& x);
void push_front(T&& x);
```

*Effects:* Inserts a copy of `x` at the beginning of the list.

``` cpp
void pop_front();
```

*Effects:* `erase_after(before_begin())`

``` cpp
iterator insert_after(const_iterator position, const T& x);
iterator insert_after(const_iterator position, T&& x);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts a copy of `x` after `position`.

*Returns:* An iterator pointing to the copy of `x`.

``` cpp
iterator insert_after(const_iterator position, size_type n, const T& x);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts `n` copies of `x` after `position`.

*Returns:* An iterator pointing to the last inserted copy of `x` or
`position` if `n == 0`.

``` cpp
template <class InputIterator>
  iterator insert_after(const_iterator position, InputIterator first, InputIterator last);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). `first` and `last` are not
iterators in `*this`.

*Effects:* Inserts copies of elements in \[`first`, `last`) after
`position`.

*Returns:* An iterator pointing to the last inserted element or
`position` if `first == last`.

``` cpp
iterator insert_after(const_iterator position, initializer_list<T> il);
```

*Effects:* `insert_after(p, il.begin(), il.end())`.

*Returns:* An iterator pointing to the last inserted element or
`position` if `i1` is empty.

``` cpp
template <class... Args>
  iterator emplace_after(const_iterator position, Args&&... args);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts an object of type `value_type` constructed with
`value_type(std::forward<Args>(args)...)` after `position`.

*Returns:* An iterator pointing to the new object.

``` cpp
iterator erase_after(const_iterator position);
```

*Requires:* The iterator following `position` is dereferenceable.

*Effects:* Erases the element pointed to by the iterator following
`position`.

*Returns:* An iterator pointing to the element following the one that
was erased, or `end()` if no such element exists.

*Throws:* Nothing.

``` cpp
iterator erase_after(const_iterator position, const_iterator last);
```

*Requires:* All iterators in the range (`position`, `last`) are
dereferenceable.

*Effects:* Erases the elements in the range (`position`, `last`).

*Returns:* `last`.

*Throws:* Nothing.

``` cpp
void resize(size_type sz);
void resize(size_type sz, const value_type& c);
```

*Effects:* If `sz < distance(begin(), end())`, erases the last
`distance(begin(), end()) - sz` elements from the list. Otherwise,
inserts `sz - distance(begin(), end())` elements at the end of the list.
For the first signature the inserted elements are value-initialized, and
for the second signature they are copies of `c`.

*Requires:* `T` shall be `DefaultConstructible` for the first form and
it shall be `CopyInsertable` into `*this` for the second form.

``` cpp
void clear() noexcept;
```

*Effects:* Erases all elements in the range \[`begin()`, `end()`).

*Remarks:* Does not invalidate past-the-end iterators.

#### `forward_list` operations <a id="forwardlist.ops">[[forwardlist.ops]]</a>

``` cpp
void splice_after(const_iterator position, forward_list& x);
void splice_after(const_iterator position, forward_list&& x);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). `&x != this`.

*Effects:* Inserts the contents of `x` after `position`, and `x` becomes
empty. Pointers and references to the moved elements of `x` now refer to
those same elements but as members of `*this`. Iterators referring to
the moved elements will continue to refer to their elements, but they
now behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* 𝑂(distance(x.begin(), x.end()))

``` cpp
void splice_after(const_iterator position, forward_list& x, const_iterator i);
void splice_after(const_iterator position, forward_list&& x, const_iterator i);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). The iterator following `i`
is a dereferenceable iterator in `x`.

*Effects:* Inserts the element following `i` into `*this`, following
`position`, and removes it from `x`. The result is unchanged if
`position == i` or `position == ++i`. Pointers and references to `*i`
continue to refer to the same element but as a member of `*this`.
Iterators to `*i` (including `i` itself) continue to refer to the same
element, but now behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* 𝑂(1)

``` cpp
void splice_after(const_iterator position, forward_list& x,
                  const_iterator first, const_iterator last);
void splice_after(const_iterator position, forward_list&& x,
                  const_iterator first, const_iterator last);
```

*Requires:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). (`first`, `last`) is a
valid range in `x`, and all iterators in the range (`first`, `last`) are
dereferenceable. `position` is not an iterator in the range (`first`,
`last`).

*Effects:* Inserts elements in the range (`first`, `last`) after
`position` and removes the elements from `x`. Pointers and references to
the moved elements of `x` now refer to those same elements but as
members of `*this`. Iterators referring to the moved elements will
continue to refer to their elements, but they now behave as iterators
into `*this`, not into `x`.

*Complexity:* 𝑂(distance(first, last))

``` cpp
void remove(const T& value);
template <class Predicate> void remove_if(Predicate pred);
```

*Effects:* Erases all the elements in the list referred by a list
iterator `i` for which the following conditions hold: `*i == value` (for
`remove()`), `pred(*i)` is true (for `remove_if()`). This operation
shall be stable: the relative order of the elements that are not removed
is the same as their relative order in the original list. Invalidates
only the iterators and references to the erased elements.

*Throws:* Nothing unless an exception is thrown by the equality
comparison or the predicate.

*Complexity:* Exactly `distance(begin(), end())` applications of the
corresponding predicate.

``` cpp
void unique();
template <class BinaryPredicate> void unique(BinaryPredicate pred);
```

*Effects:* Erases all but the first element from every consecutive group
of equal elements referred to by the iterator `i` in the range
\[`first + 1`, `last`) for which `*i == *(i-1)` (for the version with no
arguments) or `pred(*i, *(i - 1))` (for the version with a predicate
argument) holds. Invalidates only the iterators and references to the
erased elements.

*Throws:* Nothing unless an exception is thrown by the equality
comparison or the predicate.

*Complexity:* If the range \[`first`, `last`) is not empty, exactly
`(last - first) - 1` applications of the corresponding predicate,
otherwise no applications of the predicate.

``` cpp
void merge(forward_list& x);
void merge(forward_list&& x);
template <class Compare> void merge(forward_list& x, Compare comp)
template <class Compare> void merge(forward_list&& x, Compare comp)
```

*Requires:* `comp` defines a strict weak ordering ([[alg.sorting]]),
and `*this` and `x` are both sorted according to this ordering.

*Effects:* Merges `x` into `*this`. This operation shall be stable: for
equivalent elements in the two lists, the elements from `*this` shall
always precede the elements from `x`. `x` is empty after the merge. If
an exception is thrown other than by a comparison there are no effects.
Pointers and references to the moved elements of `x` now refer to those
same elements but as members of `*this`. Iterators referring to the
moved elements will continue to refer to their elements, but they now
behave as iterators into `*this`, not into `x`.

*Complexity:* At most distance(begin(), end()) + distance(x.begin(),
x.end()) - 1 comparisons.

``` cpp
void sort();
template <class Compare> void sort(Compare comp);
```

*Requires:* `operator<` (for the version with no arguments) or `comp`
(for the version with a comparison argument) defines a strict weak
ordering ([[alg.sorting]]).

*Effects:* Sorts the list according to the `operator<` or the `comp`
function object. This operation shall be stable: the relative order of
the equivalent elements is preserved. If an exception is thrown the
order of the elements in `*this` is unspecified. Does not affect the
validity of iterators and references.

*Complexity:* Approximately N log N comparisons, where N is
`distance(begin(), end())`.

``` cpp
void reverse() noexcept;
```

*Effects:* Reverses the order of the elements in the list. Does not
affect the validity of iterators and references.

*Complexity:* Linear time.

#### `forward_list` specialized algorithms <a id="forwardlist.spec">[[forwardlist.spec]]</a>

``` cpp
template <class T, class Allocator>
  void swap(forward_list<T,Allocator>& x, forward_list<T,Allocator>& y);
```

*Effects:* `x.swap(y)`

### Class template `list` <a id="list">[[list]]</a>

#### Class template `list` overview <a id="list.overview">[[list.overview]]</a>

A `list` is a sequence container that supports bidirectional iterators
and allows constant time insert and erase operations anywhere within the
sequence, with storage management handled automatically. Unlike
vectors ([[vector]]) and deques ([[deque]]), fast random access to
list elements is not supported, but many algorithms only need sequential
access anyway.

A `list` satisfies all of the requirements of a container, of a
reversible container (given in two tables in
[[container.requirements]]), of a sequence container, including most of
the optional sequence container requirements ([[sequence.reqmts]]), and
of an allocator-aware container (Table 
[[tab:containers.allocatoraware]]). The exceptions are the `operator[]`
and `at` member functions, which are not provided.[^2] Descriptions are
provided here only for operations on `list` that are not described in
one of these tables or for operations where there is additional semantic
information.

``` cpp
namespace std {
  template <class T, class Allocator = allocator<T> >
  class list {
  public:
    // types:
    typedef value_type&                                             reference;
    typedef const value_type&                                       const_reference;
    typedef implementation-defined                iterator;       // see [container.requirements]
    typedef implementation-defined                const_iterator; // see [container.requirements]
    typedef implementation-defined                size_type;      // see [container.requirements]
    typedef implementation-defined                difference_type;// see [container.requirements]
    typedef T                                     value_type;
    typedef Allocator                             allocator_type;
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    // [list.cons], construct/copy/destroy:
    explicit list(const Allocator& = Allocator());
    explicit list(size_type n);
    list(size_type n, const T& value, const Allocator& = Allocator());
    template <class InputIterator>
      list(InputIterator first, InputIterator last, const Allocator& = Allocator());
    list(const list& x);
    list(list&& x);
    list(const list&, const Allocator&);
    list(list&&, const Allocator&);
    list(initializer_list<T>, const Allocator& = Allocator());
   ~list();
    list& operator=(const list& x);
    list& operator=(list&& x);
    list& operator=(initializer_list<T>);
    template <class InputIterator>
      void assign(InputIterator first, InputIterator last);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;
    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // [list.capacity], capacity:
    bool      empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;
    void      resize(size_type sz);
    void      resize(size_type sz, const T& c);

    // element access:
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    // [list.modifiers], modifiers:
    template <class... Args> void emplace_front(Args&&... args);
    void pop_front();
    template <class... Args> void emplace_back(Args&&... args);
    void push_front(const T& x);
    void push_front(T&& x);
    void push_back(const T& x);
    void push_back(T&& x);
    void pop_back();

    template <class... Args> iterator emplace(const_iterator position, Args&&... args);
    iterator insert(const_iterator position, const T& x);
    iterator insert(const_iterator position, T&& x);
    iterator insert(const_iterator position, size_type n, const T& x);
    template <class InputIterator>
      iterator insert(const_iterator position, InputIterator first,
                      InputIterator last);
    iterator insert(const_iterator position, initializer_list<T> il);

    iterator erase(const_iterator position);
    iterator erase(const_iterator position, const_iterator last);
    void     swap(list&);
    void     clear() noexcept;

    // [list.ops], list operations:
    void splice(const_iterator position, list& x);
    void splice(const_iterator position, list&& x);
    void splice(const_iterator position, list& x, const_iterator i);
    void splice(const_iterator position, list&& x, const_iterator i);
    void splice(const_iterator position, list& x,
                const_iterator first, const_iterator last);
    void splice(const_iterator position, list&& x,
                const_iterator first, const_iterator last);

    void remove(const T& value);
    template <class Predicate> void remove_if(Predicate pred);

    void unique();
    template <class BinaryPredicate>
      void unique(BinaryPredicate binary_pred);

    void merge(list& x);
    void merge(list&& x);
    template <class Compare> void merge(list& x, Compare comp);
    template <class Compare> void merge(list&& x, Compare comp);

    void sort();
    template <class Compare> void sort(Compare comp);

    void reverse() noexcept;
  };

  template <class T, class Allocator>
    bool operator==(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const list<T,Allocator>& x, const list<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const list<T,Allocator>& x, const list<T,Allocator>& y);

  // specialized algorithms:
  template <class T, class Allocator>
    void swap(list<T,Allocator>& x, list<T,Allocator>& y);
}
```

#### `list` constructors, copy, and assignment <a id="list.cons">[[list.cons]]</a>

``` cpp
explicit list(const Allocator& = Allocator());
```

*Effects:* Constructs an empty list, using the specified allocator.

*Complexity:* Constant.

``` cpp
explicit list(size_type n);
```

*Effects:* Constructs a `list` with `n` value-initialized elements.

*Requires:* `T` shall be `DefaultConstructible`.

*Complexity:* Linear in `n`.

``` cpp
list(size_type n, const T& value,
     const Allocator& = Allocator());
```

*Effects:* Constructs a `list` with `n` copies of `value`, using the
specified allocator.

*Requires:* `T` shall be `CopyInsertable` into `*this`.

*Complexity:* Linear in `n`.

``` cpp
template <class InputIterator>
list(InputIterator first, InputIterator last,
     const Allocator& = Allocator());
```

*Effects:* Constructs a `list` equal to the range \[`first`, `last`).

*Complexity:* Linear in `distance(first, last)`.

``` cpp
template <class InputIterator>
  void assign(InputIterator first, InputIterator last);
```

*Effects:* Replaces the contents of the list with the range
`[first, last)`.

``` cpp
void assign(size_type n, const T& t);
```

*Effects:* Replaces the contents of the list with `n` copies of `t`.

#### `list` capacity <a id="list.capacity">[[list.capacity]]</a>

``` cpp
void resize(size_type sz);
```

*Effects:* If `size() < sz`, appends `sz - size()` value-initialized
elements to the sequence. If `sz <= size()`, equivalent to

``` cpp
list<T>::iterator it = begin();
advance(it, sz);
erase(it, end());
```

*Requires:* `T` shall be `DefaultConstructible`.

``` cpp
void resize(size_type sz, const T& c);
```

*Effects:*

``` cpp
if (sz > size())
  insert(end(), sz-size(), c);
else if (sz < size()) {
  iterator i = begin();
  advance(i, sz);
  erase(i, end());
}
else
  ;                 // do nothing
```

*Requires:* `T` shall be `CopyInsertable` into `*this`.

#### `list` modifiers <a id="list.modifiers">[[list.modifiers]]</a>

``` cpp
iterator insert(const_iterator position, const T& x);
iterator insert(const_iterator position, T&& x);
iterator insert(const_iterator position, size_type n, const T& x);
template <class InputIterator>
  iterator insert(const_iterator position, InputIterator first,
                  InputIterator last);
iterator insert(const_iterator position, initializer_list<T>);

template <class... Args> void emplace_front(Args&&... args);
template <class... Args> void emplace_back(Args&&... args);
template <class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_front(const T& x);
void push_front(T&& x);
void push_back(const T& x);
void push_back(T&& x);
```

Does not affect the validity of iterators and references. If an
exception is thrown there are no effects.

*Complexity:* Insertion of a single element into a list takes constant
time and exactly one call to a constructor of `T`. Insertion of multiple
elements into a list is linear in the number of elements inserted, and
the number of calls to the copy constructor or move constructor of `T`
is exactly equal to the number of elements inserted.

``` cpp
iterator erase(const_iterator position);
iterator erase(const_iterator first, const_iterator last);

void pop_front();
void pop_back();
void clear() noexcept;
```

*Effects:* Invalidates only the iterators and references to the erased
elements.

*Throws:* Nothing.

*Complexity:* Erasing a single element is a constant time operation with
a single call to the destructor of `T`. Erasing a range in a list is
linear time in the size of the range and the number of calls to the
destructor of type `T` is exactly equal to the size of the range.

#### `list` operations <a id="list.ops">[[list.ops]]</a>

Since lists allow fast insertion and erasing from the middle of a list,
certain operations are provided specifically for them.[^3]

`list` provides three splice operations that destructively move elements
from one list to another. The behavior of splice operations is undefined
if `get_allocator() !=
x.get_allocator()`.

``` cpp
void splice(const_iterator position, list& x);
void splice(const_iterator position, list&& x);
```

*Requires:* `&x != this`.

*Effects:* Inserts the contents of `x` before `position` and `x` becomes
empty. Pointers and references to the moved elements of `x` now refer to
those same elements but as members of `*this`. Iterators referring to
the moved elements will continue to refer to their elements, but they
now behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* Constant time.

``` cpp
void splice(const_iterator position, list& x, const_iterator i);
void splice(const_iterator position, list&& x, const_iterator i);
```

*Effects:* Inserts an element pointed to by `i` from list `x` before
`position` and removes the element from `x`. The result is unchanged if
`position == i` or `position == ++i`. Pointers and references to `*i`
continue to refer to this same element but as a member of `*this`.
Iterators to `*i` (including `i` itself) continue to refer to the same
element, but now behave as iterators into `*this`, not into `x`.

*Requires:* `i` is a valid dereferenceable iterator of `x`.

*Throws:* Nothing.

*Complexity:* Constant time.

``` cpp
void splice(const_iterator position, list& x, const_iterator first,
            const_iterator last);
void splice(const_iterator position, list&& x, const_iterator first,
            const_iterator last);
```

*Effects:* Inserts elements in the range \[`first`, `last`) before
`position` and removes the elements from `x`.

*Requires:* `[first, last)` is a valid range in `x`. The result is
undefined if `position` is an iterator in the range \[`first`, `last`).
Pointers and references to the moved elements of `x` now refer to those
same elements but as members of `*this`. Iterators referring to the
moved elements will continue to refer to their elements, but they now
behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* Constant time if `&x == this`; otherwise, linear time.

``` cpp
void remove(const T& value);
template <class Predicate> void remove_if(Predicate pred);
```

*Effects:* Erases all the elements in the list referred by a list
iterator `i` for which the following conditions hold:
`*i == value, pred(*i) != false`. Invalidates only the iterators and
references to the erased elements.

*Throws:* Nothing unless an exception is thrown by `*i == value` or
`pred(*i) != false`.

Stable.

*Complexity:* Exactly `size()` applications of the corresponding
predicate.

``` cpp
void unique();
template <class BinaryPredicate> void unique(BinaryPredicate binary_pred);
```

*Effects:* Erases all but the first element from every consecutive group
of equal elements referred to by the iterator `i` in the range
\[`first + 1`, `last`) for which `*i == *(i-1)` (for the version of
`unique` with no arguments) or `pred(*i, *(i - 1))` (for the version of
`unique` with a predicate argument) holds. Invalidates only the
iterators and references to the erased elements.

*Throws:* Nothing unless an exception in thrown by `*i == *(i-1)` or
`pred(*i, *(i - 1))`

*Complexity:* If the range `[first, last)` is not empty, exactly
`(last - first) - 1` applications of the corresponding predicate,
otherwise no applications of the predicate.

``` cpp
void                          merge(list& x);
void                          merge(list&& x);
template <class Compare> void merge(list& x, Compare comp);
template <class Compare> void merge(list&& x, Compare comp);
```

*Requires:* `comp` shall define a strict weak
ordering ([[alg.sorting]]), and both the list and the argument list
shall be sorted according to this ordering.

*Effects:* If `(&x == this)` does nothing; otherwise, merges the two
sorted ranges `[begin(), end())` and `[x.begin(), x.end())`. The result
is a range in which the elements will be sorted in non-decreasing order
according to the ordering defined by `comp`; that is, for every iterator
`i`, in the range other than the first, the condition
`comp(*i, *(i - 1))` will be false. Pointers and references to the moved
elements of `x` now refer to those same elements but as members of
`*this`. Iterators referring to the moved elements will continue to
refer to their elements, but they now behave as iterators into `*this`,
not into `x`.

Stable. If `(&x != this)` the range `[x.begin(), x.end())` is empty
after the merge. No elements are copied by this operation. The behavior
is undefined if `this->get_allocator() != x.get_allocator()`.

*Complexity:* At most `size() + x.size() - 1` applications of `comp` if
`(&x != this)`; otherwise, no applications of `comp` are performed. If
an exception is thrown other than by a comparison there are no effects.

``` cpp
void reverse() noexcept;
```

*Effects:* Reverses the order of the elements in the list. Does not
affect the validity of iterators and references.

*Complexity:* Linear time.

``` cpp
void sort();
template <class Compare> void sort(Compare comp);
```

*Requires:* `operator<` (for the first version) or `comp` (for the
second version) shall define a strict weak ordering ([[alg.sorting]]).

*Effects:* Sorts the list according to the `operator<` or a `Compare`
function object. Does not affect the validity of iterators and
references.

Stable.

*Complexity:* Approximately N log(N) comparisons, where `N == size()`.

#### `list` specialized algorithms <a id="list.special">[[list.special]]</a>

``` cpp
template <class T, class Allocator>
  void swap(list<T,Allocator>& x, list<T,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

### Class template `vector` <a id="vector">[[vector]]</a>

#### Class template `vector` overview <a id="vector.overview">[[vector.overview]]</a>

A `vector` is a sequence container that supports random access
iterators. In addition, it supports (amortized) constant time insert and
erase operations at the end; insert and erase in the middle take linear
time. Storage management is handled automatically, though hints can be
given to improve efficiency. The elements of a vector are stored
contiguously, meaning that if `v` is a `vector<T, Allocator>` where `T`
is some type other than `bool`, then it obeys the identity
`&v[n] == &v[0] + n` for all `0 <= n < v.size()`.

A `vector` satisfies all of the requirements of a container and of a
reversible container (given in two tables in 
[[container.requirements]]), of a sequence container, including most of
the optional sequence container requirements ([[sequence.reqmts]]), and
of an allocator-aware container (Table 
[[tab:containers.allocatoraware]]). The exceptions are the `push_front`,
`pop_front`, and `emplace_front` member functions, which are not
provided. Descriptions are provided here only for operations on `vector`
that are not described in one of these tables or for operations where
there is additional semantic information.

``` cpp
namespace std {
  template <class T, class Allocator = allocator<T> >
  class vector {
  public:
    // types:
    typedef value_type&                           reference;
    typedef const value_type&                     const_reference;
    typedef implementation-defined                iterator;       // see [container.requirements]
    typedef implementation-defined                const_iterator; // see [container.requirements]
    typedef implementation-defined                size_type;      // see [container.requirements]
    typedef implementation-defined                difference_type;// see [container.requirements]
    typedef T                                     value_type;
    typedef Allocator                             allocator_type;
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    // [vector.cons], construct/copy/destroy:
    explicit vector(const Allocator& = Allocator());
    explicit vector(size_type n);
    vector(size_type n, const T& value, const Allocator& = Allocator());
    template <class InputIterator>
      vector(InputIterator first, InputIterator last,
             const Allocator& = Allocator());
    vector(const vector& x);
    vector(vector&&);
    vector(const vector&, const Allocator&);
    vector(vector&&, const Allocator&);
    vector(initializer_list<T>, const Allocator& = Allocator());
   ~vector();
    vector& operator=(const vector& x);
    vector& operator=(vector&& x);
    vector& operator=(initializer_list<T>);
    template <class InputIterator>
      void assign(InputIterator first, InputIterator last);
    void assign(size_type n, const T& u);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;
    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // [vector.capacity], capacity:
    size_type size() const noexcept;
    size_type max_size() const noexcept;
    void      resize(size_type sz);
    void      resize(size_type sz, const T& c);
    size_type capacity() const noexcept;
    bool      empty() const noexcept;
    void      reserve(size_type n);
    void      shrink_to_fit();

    // element access:
    reference       operator[](size_type n);
    const_reference operator[](size_type n) const;
    const_reference at(size_type n) const;
    reference       at(size_type n);
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    // [vector.data], data access
    T*         data() noexcept;
    const T*  data() const noexcept;

    // [vector.modifiers], modifiers:
    template <class... Args> void emplace_back(Args&&... args);
    void push_back(const T& x);
    void push_back(T&& x);
    void pop_back();

    template <class... Args> iterator emplace(const_iterator position, Args&&... args);
    iterator insert(const_iterator position, const T& x);
    iterator     insert(const_iterator position, T&& x);
    iterator     insert(const_iterator position, size_type n, const T& x);
    template <class InputIterator>
        iterator insert(const_iterator position,
                        InputIterator first, InputIterator last);
    iterator     insert(const_iterator position, initializer_list<T> il);
    iterator erase(const_iterator position);
    iterator erase(const_iterator first, const_iterator last);
    void     swap(vector&);
    void     clear() noexcept;
  };

  template <class T, class Allocator>
    bool operator==(const vector<T,Allocator>& x, const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator< (const vector<T,Allocator>& x, const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator!=(const vector<T,Allocator>& x, const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator> (const vector<T,Allocator>& x, const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator>=(const vector<T,Allocator>& x, const vector<T,Allocator>& y);
  template <class T, class Allocator>
    bool operator<=(const vector<T,Allocator>& x, const vector<T,Allocator>& y);

  // [vector.special], specialized algorithms:
  template <class T, class Allocator>
    void swap(vector<T,Allocator>& x, vector<T,Allocator>& y);
}
```

#### `vector` constructors, copy, and assignment <a id="vector.cons">[[vector.cons]]</a>

``` cpp
explicit vector(const Allocator& = Allocator());
```

*Effects:* Constructs an empty `vector`, using the specified allocator.

*Complexity:* Constant.

``` cpp
explicit vector(size_type n);
```

*Effects:* Constructs a `vector` with `n` value-initialized elements.

*Requires:* `T` shall be `DefaultConstructible`.

*Complexity:* Linear in `n`.

``` cpp
vector(size_type n, const T& value,
       const Allocator& = Allocator());
```

*Effects:* Constructs a `vector` with `n` copies of `value`, using the
specified allocator.

*Requires:* `T` shall be `CopyInsertable` into `*this`.

*Complexity:* Linear in `n`.

``` cpp
template <class InputIterator>
  vector(InputIterator first, InputIterator last,
         const Allocator& = Allocator());
```

*Effects:* Constructs a `vector` equal to the range \[`first`, `last`),
using the specified allocator.

*Complexity:* Makes only N calls to the copy constructor of `T` (where N
is the distance between `first` and `last`) and no reallocations if
iterators first and last are of forward, bidirectional, or random access
categories. It makes order `N` calls to the copy constructor of `T` and
order log(N) reallocations if they are just input iterators.

``` cpp
template <class InputIterator>
  void assign(InputIterator first, InputIterator last);
```

*Effects:*

``` cpp
erase(begin(), end());
insert(begin(), first, last);
```

``` cpp
void assign(size_type n, const T& t);
```

*Effects:*

``` cpp
erase(begin(), end());
insert(begin(), n, t);
```

#### `vector` capacity <a id="vector.capacity">[[vector.capacity]]</a>

``` cpp
size_type capacity() const noexcept;
```

*Returns:* The total number of elements that the vector can hold without
requiring reallocation.

``` cpp
void reserve(size_type n);
```

*Effects:* A directive that informs a `vector` of a planned change in
size, so that it can manage the storage allocation accordingly. After
`reserve()`, `capacity()` is greater or equal to the argument of
`reserve` if reallocation happens; and equal to the previous value of
`capacity()` otherwise. Reallocation happens at this point if and only
if the current capacity is less than the argument of `reserve()`. If an
exception is thrown other than by the move constructor of a
non-`CopyInsertable` type, there are no effects.

*Complexity:* It does not change the size of the sequence and takes at
most linear time in the size of the sequence.

*Throws:* `length_error` if `n > max_size()`.[^4]

Reallocation invalidates all the references, pointers, and iterators
referring to the elements in the sequence. It is guaranteed that no
reallocation takes place during insertions that happen after a call to
`reserve()` until the time when an insertion would make the size of the
vector greater than the value of `capacity()`.

``` cpp
void shrink_to_fit();
```

`shrink_to_fit` is a non-binding request to reduce `capacity()` to
`size()`. The request is non-binding to allow latitude for
implementation-specific optimizations.

``` cpp
void swap(vector& x);
```

*Effects:* Exchanges the contents and `capacity()` of `*this` with that
of `x`.

*Complexity:* Constant time.

``` cpp
void resize(size_type sz);
```

*Effects:* If `sz <= size()`, equivalent to
`erase(begin() + sz, end());`. If `size() < sz`, appends `sz - size()`
value-initialized elements to the sequence.

*Requires:* `T` shall be `CopyInsertable` into `*this`.

``` cpp
void resize(size_type sz, const T& c);
```

*Effects:*

``` cpp
if (sz > size())
  insert(end(), sz-size(), c);
else if (sz < size())
  erase(begin()+sz, end());
else
  ;                 // do nothing
```

*Requires:* If an exception is thrown other than by the move constructor
of a non-`CopyInsertable` `T` there are no effects.

#### `vector` data <a id="vector.data">[[vector.data]]</a>

``` cpp
T*         data() noexcept;
const T*   data() const noexcept;
```

*Returns:* A pointer such that \[`data()`, `data() + size()`) is a valid
range. For a non-empty vector, `data()` `==` `&front()`.

*Complexity:* Constant time.

#### `vector` modifiers <a id="vector.modifiers">[[vector.modifiers]]</a>

``` cpp
iterator insert(const_iterator position, const T& x);
iterator insert(const_iterator position, T&& x);
iterator insert(const_iterator position, size_type n, const T& x);
template <class InputIterator>
  iterator insert(const_iterator position, InputIterator first, InputIterator last);
iterator insert(const_iterator position, initializer_list<T>);

template <class... Args> void emplace_back(Args&&... args);
template <class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_back(const T& x);
void push_back(T&& x);
```

Causes reallocation if the new size is greater than the old capacity. If
no reallocation happens, all the iterators and references before the
insertion point remain valid. If an exception is thrown other than by
the copy constructor, move constructor, assignment operator, or move
assignment operator of `T` or by any `InputIterator` operation there are
no effects. If an exception is thrown by the move constructor of a
non-`CopyInsertable` `T`, the effects are unspecified.

*Complexity:* The complexity is linear in the number of elements
inserted plus the distance to the end of the vector.

``` cpp
iterator erase(const_iterator position);
iterator erase(const_iterator first, const_iterator last);
```

*Effects:* Invalidates iterators and references at or after the point of
the erase.

*Complexity:* The destructor of `T` is called the number of times equal
to the number of the elements erased, but the move assignment operator
of `T` is called the number of times equal to the number of elements in
the vector after the erased elements.

*Throws:* Nothing unless an exception is thrown by the copy constructor,
move constructor, assignment operator, or move assignment operator of
`T`.

#### `vector` specialized algorithms <a id="vector.special">[[vector.special]]</a>

``` cpp
template <class T, class Allocator>
  void swap(vector<T,Allocator>& x, vector<T,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

### Class `vector<bool>` <a id="vector.bool">[[vector.bool]]</a>

To optimize space allocation, a specialization of vector for `bool`
elements is provided:

``` cpp
namespace std {
  template <class Allocator> class vector<bool, Allocator> {
  public:
    // types:
    typedef bool                                  const_reference;
    typedef implementation-defined                iterator;       // see [container.requirements]
    typedef implementation-defined                const_iterator; // see [container.requirements]
    typedef implementation-defined                size_type;      // see [container.requirements]
    typedef implementation-defined                difference_type;// see [container.requirements]
    typedef bool                                  value_type;
    typedef Allocator                             allocator_type;
    typedef implementation-defined                pointer;
    typedef implementation-defined                const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    // bit reference:
    class reference {
      friend class vector;
      reference() noexcept;
    public:
      ~reference();
      operator bool() const noexcept;
      reference& operator=(const bool x) noexcept;
      reference& operator=(const reference& x) noexcept;
      void flip() noexcept;     // flips the bit
    };

    // construct/copy/destroy:
    explicit vector(const Allocator& = Allocator());
    explicit vector(size_type n, const bool& value = bool(),
                    const Allocator& = Allocator());
    template <class InputIterator>
      vector(InputIterator first, InputIterator last,
             const Allocator& = Allocator());
    vector(const vector<bool,Allocator>& x);
    vector(vector<bool,Allocator>&& x);
    vector(const vector&, const Allocator&);
    vector(vector&&, const Allocator&);
    vector(initializer_list<bool>, const Allocator& = Allocator()));
   ~vector();
    vector<bool,Allocator>& operator=(const vector<bool,Allocator>& x);
    vector<bool,Allocator>& operator=(vector<bool,Allocator>&& x);
    vector operator=(initializer_list<bool>);
    template <class InputIterator>
      void assign(InputIterator first, InputIterator last);
    void assign(size_type n, const bool& t);
    void assign(initializer_list<bool>;
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;
    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // capacity:
    size_type size() const noexcept;
    size_type max_size() const noexcept;
    void      resize(size_type sz, bool c = false);
    size_type capacity() const noexcept;
    bool      empty() const noexcept;
    void      reserve(size_type n);
    void      shrink_to_fit();

    // element access:
    reference       operator[](size_type n);
    const_reference operator[](size_type n) const;
    const_reference at(size_type n) const;
    reference       at(size_type n);
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    // modifiers:
    void push_back(const bool& x);
    void pop_back();
    iterator insert(const_iterator position, const bool& x);
    iterator insert (const_iterator position, size_type n, const bool& x);
    template <class InputIterator>
        iterator insert(const_iterator position,
                        InputIterator first, InputIterator last);
    iterator insert(const_iterator position, initializer_list<bool> il);

    iterator erase(const_iterator position);
    iterator erase(const_iterator first, const_iterator last);
    void swap(vector<bool,Allocator>&);
    static void swap(reference x, reference y) noexcept;
    void flip() noexcept;       // flips all bits
    void clear() noexcept;
  };
}
```

Unless described below, all operations have the same requirements and
semantics as the primary `vector` template, except that operations
dealing with the `bool` value type map to bit values in the container
storage and allocator_traits::construct ([[allocator.traits.members]])
is not used to construct these values.

There is no requirement that the data be stored as a contiguous
allocation of `bool` values. A space-optimized representation of bits is
recommended instead.

`reference`

is a class that simulates the behavior of references of a single bit in
`vector<bool>`. The conversion operator returns `true` when the bit is
set, and `false` otherwise. The assignment operator sets the bit when
the argument is (convertible to) `true` and clears it otherwise. `flip`
reverses the state of the bit.

``` cpp
void flip() noexcept;
```

*Effects:* Replaces each element in the container with its complement.

``` cpp
static void swap(reference x, reference y) noexcept;
```

*Effects:* exchanges the contents of `x` and `y` as if by

``` cpp
bool b = x;
x = y;
y = b;
```

``` cpp
template <class Allocator> struct hash<vector<bool, Allocator> >;
```

*Requires:* the template specialization shall meet the requirements of
class template `hash` ([[unord.hash]]).

## Associative containers <a id="associative">[[associative]]</a>

### In general <a id="associative.general">[[associative.general]]</a>

The header `<map>` defines the class templates `map` and `multimap`; the
header `<set>` defines the class templates `set` and `multiset`.

### Header `<map>` synopsis <a id="associative.map.syn">[[associative.map.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  template <class Key, class T, class Compare = less<Key>,
            class Allocator = allocator<pair<const Key, T> > >
    class map;
  template <class Key, class T, class Compare, class Allocator>
    bool operator==(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator< (const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator!=(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator> (const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator>=(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator<=(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    void swap(map<Key,T,Compare,Allocator>& x,
              map<Key,T,Compare,Allocator>& y);

  template <class Key, class T, class Compare = less<Key>,
            class Allocator = allocator<pair<const Key, T> > >
    class multimap;
  template <class Key, class T, class Compare, class Allocator>
    bool operator==(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator< (const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator!=(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator> (const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator>=(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator<=(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    void swap(multimap<Key,T,Compare,Allocator>& x,
              multimap<Key,T,Compare,Allocator>& y);
}
```

### Header `<set>` synopsis <a id="associative.set.syn">[[associative.set.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  template <class Key, class Compare = less<Key>,
            class Allocator = allocator<Key> >
    class set;
  template <class Key, class Compare, class Allocator>
    bool operator==(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator< (const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator!=(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator> (const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator>=(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator<=(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    void swap(set<Key,Compare,Allocator>& x,
              set<Key,Compare,Allocator>& y);

  template <class Key, class Compare = less<Key>,
            class Allocator = allocator<Key> >
    class multiset;
  template <class Key, class Compare, class Allocator>
    bool operator==(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator< (const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator!=(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator> (const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator>=(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator<=(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    void swap(multiset<Key,Compare,Allocator>& x,
              multiset<Key,Compare,Allocator>& y);
}
```

### Class template `map` <a id="map">[[map]]</a>

#### Class template `map` overview <a id="map.overview">[[map.overview]]</a>

A `map` is an associative container that supports unique keys (contains
at most one of each key value) and provides for fast retrieval of values
of another type `T` based on the keys. The `map` class supports
bidirectional iterators.

A `map` satisfies all of the requirements of a container, of a
reversible container ([[container.requirements]]), of an associative
container ([[associative.reqmts]]), and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). A `map` also provides most
operations described in ([[associative.reqmts]]) for unique keys. This
means that a `map` supports the `a_uniq` operations in (
[[associative.reqmts]]) but not the `a_eq` operations. For a
`map<Key,T>` the `key_type` is `Key` and the `value_type` is
`pair<const Key,T>`. Descriptions are provided here only for operations
on `map` that are not described in one of those tables or for operations
where there is additional semantic information.

``` cpp
namespace std {
  template <class Key, class T, class Compare = less<Key>,
            class Allocator = allocator<pair<const Key, T> > >
  class map {
  public:
    // types:
    typedef Key                                   key_type;
    typedef T                                     mapped_type;
    typedef pair<const Key, T>                    value_type;
    typedef Compare                               key_compare;
    typedef Allocator                             allocator_type;
    typedef value_type&                           reference;
    typedef const value_type&                     const_reference;
    typedef implementation-defined                iterator;       // see [container.requirements]
    typedef implementation-defined                const_iterator; // see [container.requirements]
    typedef implementation-defined                size_type;      // see [container.requirements]
    typedef implementation-defined                difference_type;// see [container.requirements]
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    class value_compare {
    friend class map;
    protected:
      Compare comp;
      value_compare(Compare c) : comp(c) {}
    public:
      typedef bool result_type;
      typedef value_type first_argument_type;
      typedef value_type second_argument_type;
      bool operator()(const value_type& x, const value_type& y) const {
        return comp(x.first, y.first);
      }
    };

    // [map.cons], construct/copy/destroy:
    explicit map(const Compare& comp = Compare(),
                 const Allocator& = Allocator());
    template <class InputIterator>
      map(InputIterator first, InputIterator last,
          const Compare& comp = Compare(), const Allocator& = Allocator());
    map(const map<Key,T,Compare,Allocator>& x);
    map(map<Key,T,Compare,Allocator>&& x);
    explicit map(const Allocator&);
    map(const map&, const Allocator&);
    map(map&&, const Allocator&);
    map(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
   ~map();
    map<Key,T,Compare,Allocator>&
      operator=(const map<Key,T,Compare,Allocator>& x);
    map<Key,T,Compare,Allocator>&
      operator=(map<Key,T,Compare,Allocator>&& x);
    map& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;

    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // capacity:
    bool      empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [map.access], element access:
    T& operator[](const key_type& x);
    T& operator[](key_type&& x);
    T&       at(const key_type& x);
    const T& at(const key_type& x) const;

    // [map.modifiers], modifiers:
    template <class... Args> pair<iterator, bool> emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator, bool> insert(const value_type& x);
    template <class P> pair<iterator, bool> insert(P&& x);
    iterator insert(const_iterator position, const value_type& x);
    template <class P>
      iterator insert(const_iterator position, P&&);
    template <class InputIterator>
      void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    iterator  erase(const_iterator first, const_iterator last);
    void swap(map<Key,T,Compare,Allocator>&);
    void clear() noexcept;

    // observers:
    key_compare   key_comp() const;
    value_compare value_comp() const;

    // [map.ops], map operations:
    iterator       find(const key_type& x);
    const_iterator find(const key_type& x) const;
    size_type      count(const key_type& x) const;

    iterator       lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    iterator       upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;

    pair<iterator,iterator>
      equal_range(const key_type& x);
    pair<const_iterator,const_iterator>
      equal_range(const key_type& x) const;
  };

  template <class Key, class T, class Compare, class Allocator>
    bool operator==(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator< (const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator!=(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator> (const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator>=(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator<=(const map<Key,T,Compare,Allocator>& x,
                    const map<Key,T,Compare,Allocator>& y);

  // specialized algorithms:
  template <class Key, class T, class Compare, class Allocator>
    void swap(map<Key,T,Compare,Allocator>& x,
              map<Key,T,Compare,Allocator>& y);
}
```

#### `map` constructors, copy, and assignment <a id="map.cons">[[map.cons]]</a>

``` cpp
explicit map(const Compare& comp = Compare(),
             const Allocator& = Allocator());
```

*Effects:* Constructs an empty `map` using the specified comparison
object and allocator.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  map(InputIterator first, InputIterator last,
      const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Requires:* If the iterator’s dereference operator returns an lvalue or
a const rvalue `pair<key_type, mapped_type>`, then both `key_type` and
`mapped_type` shall be `CopyConstructible`.

*Effects:* Constructs an empty `map` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted using `comp` and otherwise $N \log{N}$, where N is `last` -
`first`.

#### `map` element access <a id="map.access">[[map.access]]</a>

``` cpp
T& operator[](const key_type& x);
```

*Effects:* If there is no key equivalent to `x` in the map, inserts
`value_type(x, T())` into the map.

*Requires:* `key_type` shall be `CopyConstructible` and `mapped_type`
shall be `DefaultConstructible`.

*Returns:* A reference to the `mapped_type` corresponding to `x` in
`*this`.

*Complexity:* logarithmic.

``` cpp
T& operator[](key_type&& x);
```

*Effects:* If there is no key equivalent to `x` in the map, inserts
`value_type(std::move(x), T())` into the map.

*Requires:* `mapped_type` shall be `DefaultConstructible`.

*Returns:* A reference to the `mapped_type` corresponding to `x` in
`*this`.

*Complexity:* logarithmic.

``` cpp
T&       at(const key_type& x);
const T& at(const key_type& x) const;
```

*Returns:* A reference to the `mapped_type` corresponding to `x` in
`*this`.

*Throws:* An exception object of type `out_of_range` if no such element
is present.

*Complexity:* logarithmic.

#### `map` modifiers <a id="map.modifiers">[[map.modifiers]]</a>

``` cpp
template <class P> pair<iterator, bool> insert(P&& x);
template <class P> pair<iterator, bool> insert(const_iterator position, P&& x);
template <class InputIterator>
  void insert(InputIterator first, InputIterator last);
```

*Requires:* `P` shall be convertible to `value_type`.

If `P` is instantiated as a reference type, then the argument `x` is
copied from. Otherwise `x` is considered to be an rvalue as it is
converted to `value_type` and inserted into the `map`. Specifically, in
such cases `CopyConstructible` is not required of `key_type` or
`mapped_type` unless the conversion from `P` specifically requires it
(e.g., if `P` is a `tuple<const key_type, mapped_type>`, then `key_type`
must be `CopyConstructible`). The signature taking `InputIterator`
parameters does not require `CopyConstructible` of either `key_type` or
`mapped_type` if the dereferenced `InputIterator` returns a non-const
rvalue `pair<key_type,mapped_type>`. Otherwise `CopyConstructible` is
required for both `key_type` and `mapped_type`.

#### `map` operations <a id="map.ops">[[map.ops]]</a>

``` cpp
iterator       find(const key_type& x);
const_iterator find(const key_type& x) const;

iterator       lower_bound(const key_type& x);
const_iterator lower_bound(const key_type& x) const;

iterator       upper_bound(const key_type& x);
const_iterator upper_bound(const key_type &x) const;

pair<iterator, iterator>
  equal_range(const key_type &x);
pair<const_iterator, const_iterator>
  equal_range(const key_type& x) const;
```

The `find`, `lower_bound`, `upper_bound` and `equal_range` member
functions each have two versions, one const and the other non-const. In
each case the behavior of the two functions is identical except that the
const version returns a `const_iterator` and the non-const version an
`iterator` ([[associative.reqmts]]).

#### `map` specialized algorithms <a id="map.special">[[map.special]]</a>

``` cpp
template <class Key, class T, class Compare, class Allocator>
  void swap(map<Key,T,Compare,Allocator>& x,
            map<Key,T,Compare,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

### Class template `multimap` <a id="multimap">[[multimap]]</a>

#### Class template `multimap` overview <a id="multimap.overview">[[multimap.overview]]</a>

A `multimap` is an associative container that supports equivalent keys
(possibly containing multiple copies of the same key value) and provides
for fast retrieval of values of another type `T` based on the keys. The
`multimap` class supports bidirectional iterators.

A `multimap` satisfies all of the requirements of a container and of a
reversible container ([[container.requirements]]), of an associative
container ([[associative.reqmts]]), and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). A `multimap` also provides
most operations described in ([[associative.reqmts]]) for equal keys.
This means that a `multimap` supports the `a_eq` operations in (
[[associative.reqmts]]) but not the `a_uniq` operations. For a
`multimap<Key,T>` the `key_type` is `Key` and the `value_type` is
`pair<const Key,T>`. Descriptions are provided here only for operations
on `multimap` that are not described in one of those tables or for
operations where there is additional semantic information.

``` cpp
namespace std {
  template <class Key, class T, class Compare = less<Key>,
            class Allocator = allocator<pair<const Key, T> > >
  class multimap {
  public:
    // types:
    typedef Key                                   key_type;
    typedef T                                     mapped_type;
    typedef pair<const Key,T>                     value_type;
    typedef Compare                               key_compare;
    typedef Allocator                             allocator_type;
    typedef value_type&                           reference;
    typedef const value_type&                     const_reference;
    typedef implementation-defined                iterator;       // see [container.requirements]
    typedef implementation-defined                const_iterator; // see [container.requirements]
    typedef implementation-defined                size_type;      // see [container.requirements]
    typedef implementation-defined                difference_type;// see [container.requirements]
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    class value_compare {
    friend class multimap;
    protected:
      Compare comp;
      value_compare(Compare c) : comp(c) { }
    public:
      typedef bool result_type;
      typedef value_type first_argument_type;
      typedef value_type second_argument_type;
      bool operator()(const value_type& x, const value_type& y) const {
        return comp(x.first, y.first);
      }
    };

    // construct/copy/destroy:
    explicit multimap(const Compare& comp = Compare(),
                      const Allocator& = Allocator());
    template <class InputIterator>
      multimap(InputIterator first, InputIterator last,
               const Compare& comp = Compare(),
               const Allocator& = Allocator());
    multimap(const multimap<Key,T,Compare,Allocator>& x);
    multimap(multimap<Key,T,Compare,Allocator>&& x);
    explicit multimap(const Allocator&);
    multimap(const multimap&, const Allocator&);
    multimap(multimap&&, const Allocator&);
    multimap(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
   ~multimap();
    multimap<Key,T,Compare,Allocator>&
      operator=(const multimap<Key,T,Compare,Allocator>& x);
    multimap<Key,T,Compare,Allocator>&
      operator=(multimap<Key,T,Compare,Allocator>&& x);
    multimap& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;

    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // capacity:
    bool           empty() const noexcept;
    size_type      size() const noexcept;
    size_type      max_size() const noexcept;

    // modifiers:
    template <class... Args> iterator emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& x);
    template <class P> iterator insert(P&& x);
    iterator insert(const_iterator position, const value_type& x);
    template <class P> iterator insert(const_iterator position, P&& x);
    template <class InputIterator>
      void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    iterator  erase(const_iterator first, const_iterator last);
    void swap(multimap<Key,T,Compare,Allocator>&);
    void clear() noexcept;

    // observers:
    key_compare    key_comp() const;
    value_compare  value_comp() const;

    // map operations:
    iterator       find(const key_type& x);
    const_iterator find(const key_type& x) const;
    size_type      count(const key_type& x) const;

    iterator       lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    iterator       upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;

    pair<iterator,iterator>
      equal_range(const key_type& x);
    pair<const_iterator,const_iterator>
      equal_range(const key_type& x) const;
  };

  template <class Key, class T, class Compare, class Allocator>
    bool operator==(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator< (const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator!=(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator> (const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator>=(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);
  template <class Key, class T, class Compare, class Allocator>
    bool operator<=(const multimap<Key,T,Compare,Allocator>& x,
                    const multimap<Key,T,Compare,Allocator>& y);

  // specialized algorithms:
  template <class Key, class T, class Compare, class Allocator>
    void swap(multimap<Key,T,Compare,Allocator>& x,
              multimap<Key,T,Compare,Allocator>& y);
}
```

#### `multimap` constructors <a id="multimap.cons">[[multimap.cons]]</a>

``` cpp
explicit multimap(const Compare& comp = Compare(),
                  const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multimap` using the specified comparison
object and allocator.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  multimap(InputIterator first, InputIterator last,
           const Compare& comp = Compare(),
           const Allocator& = Allocator());
```

*Requires:* If the iterator’s dereference operator returns an lvalue or
a const rvalue `pair<key_type, mapped_type>`, then both `key_type` and
`mapped_type` shall be `CopyConstructible`.

*Effects:* Constructs an empty `multimap` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted using `comp` and otherwise $N \log{N}$, where N is
`last - first`.

#### `multimap` modifiers <a id="multimap.modifiers">[[multimap.modifiers]]</a>

``` cpp
template <class P> iterator insert(P&& x);
template <class P> iterator insert(const_iterator position, P&& x);
```

*Requires:* `P` shall be convertible to `value_type`.

If `P` is instantiated as a reference type, then the argument `x` is
copied from. Otherwise `x` is considered to be an rvalue as it is
converted to `value_type` and inserted into the `map`. Specifically, in
such cases `CopyConstructible` is not required of `key_type` or
`mapped_type` unless the conversion from `P` specifically requires it
(e.g., if `P` is a `tuple<const key_type, mapped_type>`, then `key_type`
must be `CopyConstructible`). The signature taking `InputIterator`
parameters does not require `CopyConstructible` of either `key_type` or
`mapped_type` if the dereferenced `InputIterator` returns a non-const
rvalue `pair<key_type, mapped_type>`. Otherwise `CopyConstructible` is
required for both `key_type` and `mapped_type`.

#### `multimap` operations <a id="multimap.ops">[[multimap.ops]]</a>

``` cpp
iterator       find(const key_type &x);
const_iterator find(const key_type& x) const;

iterator       lower_bound(const key_type& x);
const_iterator lower_bound(const key_type& x) const;

pair<iterator, iterator>
  equal_range(const key_type& x);
pair<const_iterator, const_iterator>
  equal_range(const key_type& x) const;
```

The `find`, `lower_bound`, `upper_bound`, and `equal_range` member
functions each have two versions, one const and one non-const. In each
case the behavior of the two versions is identical except that the const
version returns a `const_iterator` and the non-const version an
`iterator` ([[associative.reqmts]]).

#### `multimap` specialized algorithms <a id="multimap.special">[[multimap.special]]</a>

``` cpp
template <class Key, class T, class Compare, class Allocator>
  void swap(multimap<Key,T,Compare,Allocator>& x,
            multimap<Key,T,Compare,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

### Class template `set` <a id="set">[[set]]</a>

#### Class template `set` overview <a id="set.overview">[[set.overview]]</a>

A `set` is an associative container that supports unique keys (contains
at most one of each key value) and provides for fast retrieval of the
keys themselves. The `set` class supports bidirectional iterators.

A `set` satisfies all of the requirements of a container, of a
reversible container ([[container.requirements]]), of an associative
container ([[associative.reqmts]]), and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). A `set` also provides most
operations described in ([[associative.reqmts]]) for unique keys. This
means that a `set` supports the `a_uniq` operations in (
[[associative.reqmts]]) but not the `a_eq` operations. For a `set<Key>`
both the `key_type` and `value_type` are `Key`. Descriptions are
provided here only for operations on `set` that are not described in one
of these tables and for operations where there is additional semantic
information.

``` cpp
namespace std {
  template <class Key, class Compare = less<Key>,
            class Allocator = allocator<Key> >
  class set {
  public:
    // types:
    typedef Key                                   key_type;
    typedef Key                                   value_type;
    typedef Compare                               key_compare;
    typedef Compare                               value_compare;
    typedef Allocator                             allocator_type;
    typedef value_type&                           reference;
    typedef const value_type&                     const_reference;
    typedef implementation-defined                iterator;       // See [container.requirements]
    typedef implementation-defined                const_iterator; // See [container.requirements]
    typedef implementation-defined                size_type;      // See [container.requirements]
    typedef implementation-defined                difference_type;// See [container.requirements]
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    // [set.cons], construct/copy/destroy:
    explicit set(const Compare& comp = Compare(),
                 const Allocator& = Allocator());
    template <class InputIterator>
      set(InputIterator first, InputIterator last,
          const Compare& comp = Compare(), const Allocator& = Allocator());
    set(const set<Key,Compare,Allocator>& x);
    set(set<Key,Compare,Allocator>&& x);
    explicit set(const Allocator&);
    set(const set&, const Allocator&);
    set(set&&, const Allocator&);
    set(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
   ~set();
    set<Key,Compare,Allocator>& operator=
      (const set<Key,Compare,Allocator>& x);
    set<Key,Compare,Allocator>& operator=
      (set<Key,Compare,Allocator>&& x);
    set& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;

    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // capacity:
    bool          empty() const noexcept;
    size_type     size() const noexcept;
    size_type     max_size() const noexcept;

    // modifiers:
    template <class... Args> pair<iterator, bool> emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator,bool> insert(const value_type& x);
    pair<iterator,bool> insert(value_type&& x);
    iterator insert(const_iterator position, const value_type& x);
    iterator insert(const_iterator position, value_type&& x);
    template <class InputIterator>
      void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    iterator  erase(const_iterator first, const_iterator last);
    void swap(set<Key,Compare,Allocator>&);
    void clear() noexcept;

    // observers:
    key_compare   key_comp() const;
    value_compare value_comp() const;

    // set operations:
    iterator        find(const key_type& x);
    const_iterator  find(const key_type& x) const;

    size_type count(const key_type& x) const;

    iterator        lower_bound(const key_type& x);
    const_iterator  lower_bound(const key_type& x) const;

    iterator        upper_bound(const key_type& x);
    const_iterator  upper_bound(const key_type& x) const;

    pair<iterator,iterator>             equal_range(const key_type& x);
    pair<const_iterator,const_iterator> equal_range(const key_type& x) const;
  };

  template <class Key, class Compare, class Allocator>
    bool operator==(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator< (const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator!=(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator> (const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator>=(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator<=(const set<Key,Compare,Allocator>& x,
                    const set<Key,Compare,Allocator>& y);

  // specialized algorithms:
  template <class Key, class Compare, class Allocator>
    void swap(set<Key,Compare,Allocator>& x,
              set<Key,Compare,Allocator>& y);
}
```

#### `set` constructors, copy, and assignment <a id="set.cons">[[set.cons]]</a>

``` cpp
explicit set(const Compare& comp = Compare(),
             const Allocator& = Allocator());
```

*Effects:* Constructs an empty set using the specified comparison
objects and allocator.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  set(InputIterator first, InputIterator last,
      const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `set` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Requires:* If the iterator’s dereference operator returns an lvalue or
a non-const rvalue, then `Key` shall be `CopyConstructible`.

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted using `comp` and otherwise $N \log{N}$, where N is
`last - first`.

#### `set` specialized algorithms <a id="set.special">[[set.special]]</a>

``` cpp
template <class Key, class Compare, class Allocator>
  void swap(set<Key,Compare,Allocator>& x,
            set<Key,Compare,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

### Class template `multiset` <a id="multiset">[[multiset]]</a>

#### Class template `multiset` overview <a id="multiset.overview">[[multiset.overview]]</a>

A `multiset` is an associative container that supports equivalent keys
(possibly contains multiple copies of the same key value) and provides
for fast retrieval of the keys themselves. The `multiset` class supports
bidirectional iterators.

A `multiset` satisfies all of the requirements of a container, of a
reversible container ([[container.requirements]]), of an associative
container ([[associative.reqmts]]), and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). `multiset` also provides
most operations described in ([[associative.reqmts]]) for duplicate
keys. This means that a `multiset` supports the `a_eq` operations in (
[[associative.reqmts]]) but not the `a_uniq` operations. For a
`multiset<Key>` both the `key_type` and `value_type` are `Key`.
Descriptions are provided here only for operations on `multiset` that
are not described in one of these tables and for operations where there
is additional semantic information.

``` cpp
namespace std {
  template <class Key, class Compare = less<Key>,
            class Allocator = allocator<Key> >
  class multiset {
  public:
    // types:
    typedef Key                                                     key_type;
    typedef Key                                                     value_type;
    typedef Compare                                                 key_compare;
    typedef Compare                                                 value_compare;
    typedef Allocator                                               allocator_type;
    typedef value_type&                                             reference;
    typedef const value_type&                                       const_reference;
    typedef implementation-defined                iterator;       // see [container.requirements]
    typedef implementation-defined                const_iterator; // see [container.requirements]
    typedef implementation-defined                size_type;      // see [container.requirements]
    typedef implementation-defined                difference_type;// see [container.requirements]
    typedef typename allocator_traits<Allocator>::pointer           pointer;
    typedef typename allocator_traits<Allocator>::const_pointer     const_pointer;
    typedef std::reverse_iterator<iterator>       reverse_iterator;
    typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

    // construct/copy/destroy:
    explicit multiset(const Compare& comp = Compare(),
                      const Allocator& = Allocator());
    template <class InputIterator>
      multiset(InputIterator first, InputIterator last,
               const Compare& comp = Compare(),
               const Allocator& = Allocator());
    multiset(const multiset<Key,Compare,Allocator>& x);
    multiset(multiset<Key,Compare,Allocator>&& x);
    explicit multiset(const Allocator&);
    multiset(const multiset&, const Allocator&);
    multiset(multiset&&, const Allocator&);
    multiset(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
   ~multiset();
    multiset<Key,Compare,Allocator>&
        operator=(const multiset<Key,Compare,Allocator>& x);
    multiset<Key,Compare,Allocator>&
        operator=(multiset<Key,Compare,Allocator>&& x);
    multiset& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators:
    iterator               begin() noexcept;
    const_iterator         begin() const noexcept;
    iterator               end() noexcept;
    const_iterator         end() const noexcept;

    reverse_iterator       rbegin() noexcept;
    const_reverse_iterator rbegin() const noexcept;
    reverse_iterator       rend() noexcept;
    const_reverse_iterator rend() const noexcept;

    const_iterator         cbegin() const noexcept;
    const_iterator         cend() const noexcept;
    const_reverse_iterator crbegin() const noexcept;
    const_reverse_iterator crend() const noexcept;

    // capacity:
    bool          empty() const noexcept;
    size_type     size() const noexcept;
    size_type     max_size() const noexcept;

    // modifiers:
    template <class... Args> iterator emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& x);
    iterator insert(value_type&& x);
    iterator insert(const_iterator position, const value_type& x);
    iterator insert(const_iterator position, value_type&& x);
    template <class InputIterator>
      void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    iterator  erase(const_iterator first, const_iterator last);
    void swap(multiset<Key,Compare,Allocator>&);
    void clear() noexcept;

    // observers:
    key_compare   key_comp() const;
    value_compare value_comp() const;

    // set operations:
    iterator        find(const key_type& x);
    const_iterator  find(const key_type& x) const;

    size_type count(const key_type& x) const;

    iterator        lower_bound(const key_type& x);
    const_iterator  lower_bound(const key_type& x) const;

    iterator        upper_bound(const key_type& x);
    const_iterator  upper_bound(const key_type& x) const;

    pair<iterator,iterator>             equal_range(const key_type& x);
    pair<const_iterator,const_iterator> equal_range(const key_type& x) const;
  };

  template <class Key, class Compare, class Allocator>
    bool operator==(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator< (const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator!=(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator> (const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator>=(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);
  template <class Key, class Compare, class Allocator>
    bool operator<=(const multiset<Key,Compare,Allocator>& x,
                    const multiset<Key,Compare,Allocator>& y);

  // specialized algorithms:
  template <class Key, class Compare, class Allocator>
    void swap(multiset<Key,Compare,Allocator>& x,
              multiset<Key,Compare,Allocator>& y);
}
```

#### `multiset` constructors <a id="multiset.cons">[[multiset.cons]]</a>

``` cpp
explicit multiset(const Compare& comp = Compare(),
                  const Allocator& = Allocator());
```

*Effects:* Constructs an empty set using the specified comparison object
and allocator.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  multiset(InputIterator first, last,
           const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Requires:* If the iterator’s dereference operator returns an lvalue or
a const rvalue, then `Key` shall be `CopyConstructible`.

*Effects:* Constructs an empty `multiset` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted using `comp` and otherwise $N \log{N}$, where N is
`last - first`.

#### `multiset` specialized algorithms <a id="multiset.special">[[multiset.special]]</a>

``` cpp
template <class Key, class Compare, class Allocator>
  void swap(multiset<Key,Compare,Allocator>& x,
            multiset<Key,Compare,Allocator>& y);
```

*Effects:*

``` cpp
x.swap(y);
```

## Unordered associative containers <a id="unord">[[unord]]</a>

### In general <a id="unord.general">[[unord.general]]</a>

The header `<unordered_map>` defines the class templates `unordered_map`
and `unordered_multimap`; the header `<unordered_set>` defines the class
templates `unordered_set` and `unordered_multiset`.

### Header `<unordered_map>` synopsis <a id="unord.map.syn">[[unord.map.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  // [unord.map], class template unordered_map:
  template <class Key,
            class T,
            class Hash = hash<Key>,
            class Pred = std::equal_to<Key>,
            class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_map;

  // [unord.multimap], class template unordered_multimap:
  template <class Key,
            class T,
            class Hash = hash<Key>,
            class Pred = std::equal_to<Key>,
            class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_multimap;

  template <class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_map<Key, T, Hash, Pred, Alloc>& x,
              unordered_map<Key, T, Hash, Pred, Alloc>& y);

  template <class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_multimap<Key, T, Hash, Pred, Alloc>& x,
              unordered_multimap<Key, T, Hash, Pred, Alloc>& y);

  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_map<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_map<Key, T, Hash, Pred, Alloc>& b);
  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_map<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_map<Key, T, Hash, Pred, Alloc>& b);
  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_multimap<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_multimap<Key, T, Hash, Pred, Alloc>& b);
  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_multimap<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_multimap<Key, T, Hash, Pred, Alloc>& b);
} // namespace std
```

### Header `<unordered_set>` synopsis <a id="unord.set.syn">[[unord.set.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  // [unord.set], class template unordered_set:
  template <class Key,
            class Hash = hash<Key>,
            class Pred = std::equal_to<Key>,
            class Alloc = std::allocator<Key> >
    class unordered_set;

  // [unord.multiset], class template unordered_multiset:
  template <class Key,
            class Hash = hash<Key>,
            class Pred = std::equal_to<Key>,
            class Alloc = std::allocator<Key> >
    class unordered_multiset;

  template <class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_set<Key, Hash, Pred, Alloc>& x,
              unordered_set<Key, Hash, Pred, Alloc>& y);

  template <class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_multiset<Key, Hash, Pred, Alloc>& x,
              unordered_multiset<Key, Hash, Pred, Alloc>& y);

  template <class Key, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_set<Key, Hash, Pred, Alloc>& a,
                    const unordered_set<Key, Hash, Pred, Alloc>& b);
  template <class Key, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_set<Key, Hash, Pred, Alloc>& a,
                    const unordered_set<Key, Hash, Pred, Alloc>& b);
  template <class Key, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_multiset<Key, Hash, Pred, Alloc>& a,
                    const unordered_multiset<Key, Hash, Pred, Alloc>& b);
  template <class Key, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_multiset<Key, Hash, Pred, Alloc>& a,
                    const unordered_multiset<Key, Hash, Pred, Alloc>& b);
} // namespace std
```

### Class template `unordered_map` <a id="unord.map">[[unord.map]]</a>

#### Class template `unordered_map` overview <a id="unord.map.overview">[[unord.map.overview]]</a>

An `unordered_map` is an unordered associative container that supports
unique keys (an `unordered_map` contains at most one of each key value)
and that associates values of another type `mapped_type` with the keys.
The `unordered_map` class supports forward iterators.

An `unordered_map` satisfies all of the requirements of a container, of
an unordered associative container, and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). It provides the operations
described in the preceding requirements table for unique keys; that is,
an `unordered_map` supports the `a_uniq` operations in that table, not
the `a_eq` operations. For an `unordered_map<Key, T>` the `key type` is
`Key`, the mapped type is `T`, and the value type is
`std::pair<const Key, T>`.

This section only describes operations on `unordered_map` that are not
described in one of the requirement tables, or for which there is
additional semantic information.

``` cpp
namespace std {
  template <class Key,
            class T,
            class Hash  = hash<Key>,
            class Pred  = std::equal_to<Key>,
            class Allocator = std::allocator<std::pair<const Key, T> > >
  class unordered_map
  {
  public:
    // types
    typedef Key                                      key_type;
    typedef std::pair<const Key, T>                  value_type;
    typedef T                                        mapped_type;
    typedef Hash                                     hasher;
    typedef Pred                                     key_equal;
    typedef Allocator                                allocator_type;
    typedef typename allocator_type::pointer         pointer;
    typedef typename allocator_type::const_pointer   const_pointer;
    typedef typename allocator_type::reference       reference;
    typedef typename allocator_type::const_reference const_reference;
    typedef implementation-defined                   size_type;
    typedef implementation-defined                   difference_type;

    typedef implementation-defined                    iterator;
    typedef implementation-defined                    const_iterator;
    typedef implementation-defined                    local_iterator;
    typedef implementation-defined                    const_local_iterator;

    // construct/destroy/copy
    explicit unordered_map(size_type n = see below,
                           const hasher& hf = hasher(),
                           const key_equal& eql = key_equal(),
                           const allocator_type& a = allocator_type());
    template <class InputIterator>
      unordered_map(InputIterator f, InputIterator l,
                    size_type n = see below,
                    const hasher& hf = hasher(),
                    const key_equal& eql = key_equal(),
                    const allocator_type& a = allocator_type());
    unordered_map(const unordered_map&);
    unordered_map(unordered_map&&);
    explicit unordered_map(const Allocator&);
    unordered_map(const unordered_map&, const Allocator&);
    unordered_map(unordered_map&&, const Allocator&);
    unordered_map(initializer_list<value_type>,
      size_type = see below,
      const hasher& hf = hasher(),
      const key_equal& eql = key_equal(),
      const allocator_type& a = allocator_type());
    ~unordered_map();
    unordered_map& operator=(const unordered_map&);
    unordered_map& operator=(unordered_map&&);
    unordered_map& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // size and capacity
    bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // modifiers
    template <class... Args> pair<iterator, bool> emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator, bool> insert(const value_type& obj);
    template <class P> pair<iterator, bool> insert(P&& obj);
    iterator       insert(const_iterator hint, const value_type& obj);
    template <class P> iterator insert(const_iterator hint, P&& obj);
    template <class InputIterator> void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator erase(const_iterator position);
    size_type erase(const key_type& k);
    iterator erase(const_iterator first, const_iterator last);
    void clear() noexcept;

    void swap(unordered_map&);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // lookup
    iterator       find(const key_type& k);
    const_iterator find(const key_type& k) const;
    size_type count(const key_type& k) const;
    std::pair<iterator, iterator>             equal_range(const key_type& k);
    std::pair<const_iterator, const_iterator> equal_range(const key_type& k) const;

    mapped_type& operator[](const key_type& k);
    mapped_type& operator[](key_type&& k);
    mapped_type& at(const key_type& k);
    const mapped_type& at(const key_type& k) const;

    // bucket interface
    size_type bucket_count() const noexcept;
    size_type max_bucket_count() const noexcept;
    size_type bucket_size(size_type n) const;
    size_type bucket(const key_type& k) const;
    local_iterator begin(size_type n);
    const_local_iterator begin(size_type n) const;
    local_iterator end(size_type n);
    const_local_iterator end(size_type n) const;
    const_local_iterator cbegin(size_type n) const;
    const_local_iterator cend(size_type n) const;

    // hash policy
    float load_factor() const noexcept;
    float max_load_factor() const noexcept;
    void max_load_factor(float z);
    void rehash(size_type n);
    void reserve(size_type n);
  };

  template <class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_map<Key, T, Hash, Pred, Alloc>& x,
              unordered_map<Key, T, Hash, Pred, Alloc>& y);

  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_map<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_map<Key, T, Hash, Pred, Alloc>& b);
  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_map<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_map<Key, T, Hash, Pred, Alloc>& b);
}
```

#### `unordered_map` constructors <a id="unord.map.cnstr">[[unord.map.cnstr]]</a>

``` cpp
explicit unordered_map(size_type n = see below,
                       const hasher& hf = hasher(),
                       const key_equal& eql = key_equal(),
                       const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_map` using the specified hash
function, key equality function, and allocator, and using at least *`n`*
buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. `max_load_factor()` returns 1.0.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  unordered_map(InputIterator f, InputIterator l,
                size_type n = see below,
                const hasher& hf = hasher(),
                const key_equal& eql = key_equal(),
                const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_map` using the specified hash
function, key equality function, and allocator, and using at least *`n`*
buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range
`[`*`f`*`, `*`l`*`)`. `max_load_factor()` returns 1.0.

*Complexity:* Average case linear, worst case quadratic.

#### `unordered_map` element access <a id="unord.map.elem">[[unord.map.elem]]</a>

``` cpp
mapped_type& operator[](const key_type& k);
mapped_type& operator[](key_type&& k);
```

*Requires:* `mapped_type` shall be `DefaultConstructible`. For the first
operator, `key_type` shall be `CopyConstructible`. For the second
operator, `key_type` shall be `MoveConstructible`.

*Effects:* If the `unordered_map` does not already contain an element
whose key is equivalent to *`k`*, the first operator inserts the value
`value_type(k, mapped_type())` and the second operator inserts the value
`value_type(std::move(k), mapped_type())`.

*Returns:* A reference to `x.second`, where `x` is the (unique) element
whose key is equivalent to *`k`*.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`size()`).

``` cpp
mapped_type& at(const key_type& k);
const mapped_type& at(const key_type& k) const;
```

*Returns:* A reference to `x.second`, where `x` is the (unique) element
whose key is equivalent to `k`.

*Throws:* An exception object of type `out_of_range` if no such element
is present.

#### `unordered_map` modifiers <a id="unord.map.modifiers">[[unord.map.modifiers]]</a>

``` cpp
template <class P>
  pair<iterator, bool> insert(P&& obj);
```

*Requires:* `value_type` is constructible from `std::forward<P>(obj)`.

*Effects:* Inserts `obj` converted to `value_type` if and only if there
is no element in the container with key equivalent to the key of
`value_type(obj)`.

*Returns:* The `bool` component of the returned `pair` object indicates
whether the insertion took place and the iterator component points to
the element with key equivalent to the key of `value_type(obj)`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`size()`).

*Remarks:* This signature shall not participate in overload resolution
unless `P` is implicitly convertible to `value_type`.

``` cpp
template <class P>
  iterator insert(const_iterator hint, P&& obj);
```

*Requires:* `value_type` is constructible from `std::forward<P>(obj)`.

*Effects:* Inserts `obj` converted to `value_type` if and only if there
is no element in the container with key equivalent to the key of
`value_type(obj)`. The iterator `hint` is a hint pointing to where the
search should start.

*Returns:* An iterator that points to the element with key equivalent to
the key of `value_type(obj)`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`size()`).

*Remarks:* This signature shall not participate in overload resolution
unless `P` is implicitly convertible to `value_type`.

#### `unordered_map` swap <a id="unord.map.swap">[[unord.map.swap]]</a>

``` cpp
template <class Key, class T, class Hash, class Pred, class Alloc>
  void swap(unordered_map<Key, T, Hash, Pred, Alloc>& x,
            unordered_map<Key, T, Hash, Pred, Alloc>& y);
```

*Effects:* `x.swap(y)`.

### Class template `unordered_multimap` <a id="unord.multimap">[[unord.multimap]]</a>

#### Class template `unordered_multimap` overview <a id="unord.multimap.overview">[[unord.multimap.overview]]</a>

An `unordered_multimap` is an unordered associative container that
supports equivalent keys (an instance of `unordered_multimap` may
contain multiple copies of each key value) and that associates values of
another type `mapped_type` with the keys. The `unordered_multimap` class
supports forward iterators.

An `unordered_multimap` satisfies all of the requirements of a
container, of an unordered associative container, and of an
allocator-aware container (Table  [[tab:containers.allocatoraware]]). It
provides the operations described in the preceding requirements table
for equivalent keys; that is, an `unordered_multimap` supports the
`a_eq` operations in that table, not the `a_uniq` operations. For an
`unordered_multimap<Key, T>` the `key type` is `Key`, the mapped type is
`T`, and the value type is `std::pair<const Key, T>`.

This section only describes operations on `unordered_multimap` that are
not described in one of the requirement tables, or for which there is
additional semantic information.

``` cpp
namespace std {
  template <class Key,
            class T,
            class Hash  = hash<Key>,
            class Pred  = std::equal_to<Key>,
            class Allocator = std::allocator<std::pair<const Key, T> > >
  class unordered_multimap
  {
  public:
    // types
    typedef Key                                      key_type;
    typedef std::pair<const Key, T>                  value_type;
    typedef T                                        mapped_type;
    typedef Hash                                     hasher;
    typedef Pred                                     key_equal;
    typedef Allocator                                allocator_type;
    typedef typename allocator_type::pointer         pointer;
    typedef typename allocator_type::const_pointer   const_pointer;
    typedef typename allocator_type::reference       reference;
    typedef typename allocator_type::const_reference const_reference;
    typedef implementation-defined                   size_type;
    typedef implementation-defined                   difference_type;

    typedef implementation-defined                   iterator;
    typedef implementation-defined                   const_iterator;
    typedef implementation-defined                   local_iterator;
    typedef implementation-defined                   const_local_iterator;

    // construct/destroy/copy
    explicit unordered_multimap(size_type n = see below,
                                const hasher& hf = hasher(),
                                const key_equal& eql = key_equal(),
                                const allocator_type& a = allocator_type());
    template <class InputIterator>
      unordered_multimap(InputIterator f, InputIterator l,
                         size_type n = see below,
                         const hasher& hf = hasher(),
                         const key_equal& eql = key_equal(),
                         const allocator_type& a = allocator_type());
    unordered_multimap(const unordered_multimap&);
    unordered_multimap(unordered_multimap&&);
    explicit unordered_multimap(const Allocator&);
    unordered_multimap(const unordered_multimap&, const Allocator&);
    unordered_multimap(unordered_multimap&&, const Allocator&);
    unordered_multimap(initializer_list<value_type>,
      size_type = see below,
      const hasher& hf = hasher(),
      const key_equal& eql = key_equal(),
      const allocator_type& a = allocator_type());
    ~unordered_multimap();
    unordered_multimap& operator=(const unordered_multimap&);
    unordered_multimap& operator=(unordered_multimap&&);
    unordered_multimap& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // size and capacity
    bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // modifiers
    template <class... Args> iterator emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& obj);
    template <class P> iterator insert(P&& obj);
    iterator insert(const_iterator hint, const value_type& obj);
    template <class P> iterator insert(const_iterator hint, P&& obj);
    template <class InputIterator> void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator erase(const_iterator position);
    size_type erase(const key_type& k);
    iterator erase(const_iterator first, const_iterator last);
    void clear() noexcept;

    void swap(unordered_multimap&);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // lookup
    iterator       find(const key_type& k);
    const_iterator find(const key_type& k) const;
    size_type count(const key_type& k) const;
    std::pair<iterator, iterator>             equal_range(const key_type& k);
    std::pair<const_iterator, const_iterator> equal_range(const key_type& k) const;

    // bucket interface
    size_type bucket_count() const noexcept;
    size_type max_bucket_count() const noexcept;
    size_type bucket_size(size_type n) const;
    size_type bucket(const key_type& k) const;
    local_iterator begin(size_type n);
    const_local_iterator begin(size_type n) const;
    local_iterator end(size_type n);
    const_local_iterator end(size_type n) const;
    const_local_iterator cbegin(size_type n) const;
    const_local_iterator cend(size_type n) const;

    // hash policy
    float load_factor() const noexcept;
    float max_load_factor() const noexcept;
    void max_load_factor(float z);
    void rehash(size_type n);
    void reserve(size_type n);
  };

  template <class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_multimap<Key, T, Hash, Pred, Alloc>& x,
              unordered_multimap<Key, T, Hash, Pred, Alloc>& y);

  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_multimap<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_multimap<Key, T, Hash, Pred, Alloc>& b);
  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_multimap<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_multimap<Key, T, Hash, Pred, Alloc>& b);
}
```

#### `unordered_multimap` constructors <a id="unord.multimap.cnstr">[[unord.multimap.cnstr]]</a>

``` cpp
explicit unordered_multimap(size_type n = see below,
                            const hasher& hf = hasher(),
                            const key_equal& eql = key_equal(),
                            const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multimap` using the specified
hash function, key equality function, and allocator, and using at least
*`n`* buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. `max_load_factor()` returns 1.0.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  unordered_multimap(InputIterator f, InputIterator l,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multimap` using the specified
hash function, key equality function, and allocator, and using at least
*`n`* buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range
`[`*`f`*`, `*`l`*`)`. `max_load_factor()` returns 1.0.

*Complexity:* Average case linear, worst case quadratic.

#### `unordered_multimap` modifiers <a id="unord.multimap.modifiers">[[unord.multimap.modifiers]]</a>

``` cpp
template <class P>
  iterator insert(P&& obj);
```

*Requires:* `value_type` is constructible from `std::forward<P>(obj)`.

*Effects:* Inserts `obj` converted to `value_type`.

*Returns:* An iterator that points to the element with key equivalent to
the key of `value_type(obj)`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`size()`).

*Remarks:* This signature shall not participate in overload resolution
unless `P` is implicitly convertible to `value_type`.

``` cpp
template <class P>
  iterator insert(const_iterator hint, P&& obj);
```

*Requires:* `value_type` is constructible from `std::forward<P>(obj)`.

*Effects:* Inserts `obj` converted to `value_type`. The iterator `hint`
is a hint pointing to where the search should start.

*Returns:* An iterator that points to the element with key equivalent to
the key of `value_type(obj)`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`size()`).

*Remarks:* This signature shall not participate in overload resolution
unless `P` is implicitly convertible to `value_type`.

#### `unordered_multimap` swap <a id="unord.multimap.swap">[[unord.multimap.swap]]</a>

``` cpp
template <class Key, class T, class Hash, class Pred, class Alloc>
  void swap(unordered_multimap<Key, T, Hash, Pred, Alloc>& x,
            unordered_multimap<Key, T, Hash, Pred, Alloc>& y);
```

*Effects:* `x.swap(y)`.

### Class template `unordered_set` <a id="unord.set">[[unord.set]]</a>

#### Class template `unordered_set` overview <a id="unord.set.overview">[[unord.set.overview]]</a>

An `unordered_set` is an unordered associative container that supports
unique keys (an `unordered_set` contains at most one of each key value)
and in which the elements’ keys are the elements themselves. The
`unordered_set` class supports forward iterators.

An `unordered_set` satisfies all of the requirements of a container, of
an unordered associative container, and of an allocator-aware container
(Table  [[tab:containers.allocatoraware]]). It provides the operations
described in the preceding requirements table for unique keys; that is,
an `unordered_set` supports the `a_uniq` operations in that table, not
the `a_eq` operations. For an `unordered_set<Key>` the `key type` and
the value type are both `Key`. The `iterator` and `const_iterator` types
are both const iterator types. It is unspecified whether they are the
same type.

This section only describes operations on `unordered_set` that are not
described in one of the requirement tables, or for which there is
additional semantic information.

``` cpp
namespace std {
  template <class Key,
            class Hash  = hash<Key>,
            class Pred  = std::equal_to<Key>,
            class Allocator = std::allocator<Key> >
  class unordered_set
  {
  public:
    // types
    typedef Key                                      key_type;
    typedef Key                                      value_type;
    typedef Hash                                     hasher;
    typedef Pred                                     key_equal;
    typedef Allocator                                allocator_type;
    typedef typename allocator_type::pointer         pointer;
    typedef typename allocator_type::const_pointer   const_pointer;
    typedef typename allocator_type::reference       reference;
    typedef typename allocator_type::const_reference const_reference;
    typedef implementation-defined                   size_type;
    typedef implementation-defined                   difference_type;

    typedef implementation-defined                   iterator;
    typedef implementation-defined                   const_iterator;
    typedef implementation-defined                   local_iterator;
    typedef implementation-defined                   const_local_iterator;

    // construct/destroy/copy
    explicit unordered_set(size_type n = see below,
                           const hasher& hf = hasher(),
                           const key_equal& eql = key_equal(),
                           const allocator_type& a = allocator_type());
    template <class InputIterator>
      unordered_set(InputIterator f, InputIterator l,
                    size_type n = see below,
                    const hasher& hf = hasher(),
                    const key_equal& eql = key_equal(),
                    const allocator_type& a = allocator_type());
    unordered_set(const unordered_set&);
    unordered_set(unordered_set&&);
    explicit unordered_set(const Allocator&);
    unordered_set(const unordered_set&, const Allocator&);
    unordered_set(unordered_set&&, const Allocator&);
    unordered_set(initializer_list<value_type>,
      size_type = see below,
      const hasher& hf = hasher(),
      const key_equal& eql = key_equal(),
      const allocator_type& a = allocator_type());
    ~unordered_set();
    unordered_set& operator=(const unordered_set&);
    unordered_set& operator=(unordered_set&&);
    unordered_set& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // size and capacity
    bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // modifiers
    template <class... Args> pair<iterator, bool> emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator, bool> insert(const value_type& obj);
    pair<iterator, bool> insert(value_type&& obj);
    iterator insert(const_iterator hint, const value_type& obj);
    iterator insert(const_iterator hint, value_type&& obj);
    template <class InputIterator> void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator erase(const_iterator position);
    size_type erase(const key_type& k);
    iterator erase(const_iterator first, const_iterator last);
    void clear() noexcept;

    void swap(unordered_set&);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // lookup
    iterator       find(const key_type& k);
    const_iterator find(const key_type& k) const;
    size_type count(const key_type& k) const;
    std::pair<iterator, iterator>             equal_range(const key_type& k);
    std::pair<const_iterator, const_iterator> equal_range(const key_type& k) const;

    // bucket interface
    size_type bucket_count() const noexcept;
    size_type max_bucket_count() const noexcept;
    size_type bucket_size(size_type n) const;
    size_type bucket(const key_type& k) const;
    local_iterator begin(size_type n);
    const_local_iterator begin(size_type n) const;
    local_iterator end(size_type n);
    const_local_iterator end(size_type n) const;
    const_local_iterator cbegin(size_type n) const;
    const_local_iterator cend(size_type n) const;

    // hash policy
    float load_factor() const noexcept;
    float max_load_factor() const noexcept;
    void max_load_factor(float z);
    void rehash(size_type n);
    void reserve(size_type n);
  };

  template <class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_set<Key, Hash, Pred, Alloc>& x,
              unordered_set<Key, Hash, Pred, Alloc>& y);

  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_set<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_set<Key, T, Hash, Pred, Alloc>& b);
  template <class Key, class T, class Hash, class Pred, class Alloc>
    bool operator!=(const unordered_set<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_set<Key, T, Hash, Pred, Alloc>& b);
}
```

#### `unordered_set` constructors <a id="unord.set.cnstr">[[unord.set.cnstr]]</a>

``` cpp
explicit unordered_set(size_type n = see below,
                       const hasher& hf = hasher(),
                       const key_equal& eql = key_equal(),
                       const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_set` using the specified hash
function, key equality function, and allocator, and using at least *`n`*
buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. `max_load_factor()` returns 1.0.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  unordered_set(InputIterator f, InputIterator l,
                size_type n = see below,
                const hasher& hf = hasher(),
                const key_equal& eql = key_equal(),
                const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_set` using the specified hash
function, key equality function, and allocator, and using at least *`n`*
buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range
`[`*`f`*`, `*`l`*`)`. `max_load_factor()` returns 1.0.

*Complexity:* Average case linear, worst case quadratic.

#### `unordered_set` swap <a id="unord.set.swap">[[unord.set.swap]]</a>

``` cpp
template <class Key, class Hash, class Pred, class Alloc>
  void swap(unordered_set<Key, Hash, Pred, Alloc>& x,
            unordered_set<Key, Hash, Pred, Alloc>& y);
```

*Effects:* `x.swap(y)`.

### Class template `unordered_multiset` <a id="unord.multiset">[[unord.multiset]]</a>

#### Class template `unordered_multiset` overview <a id="unord.multiset.overview">[[unord.multiset.overview]]</a>

An `unordered_multiset` is an unordered associative container that
supports equivalent keys (an instance of `unordered_multiset` may
contain multiple copies of the same key value) and in which each
element’s key is the element itself. The `unordered_multiset` class
supports forward iterators.

An `unordered_multiset` satisfies all of the requirements of a
container, of an unordered associative container, and of an
allocator-aware container (Table  [[tab:containers.allocatoraware]]). It
provides the operations described in the preceding requirements table
for equivalent keys; that is, an `unordered_multiset` supports the
`a_eq` operations in that table, not the `a_uniq` operations. For an
`unordered_multiset<Key>` the `key type` and the value type are both
`Key`. The `iterator` and `const_iterator` types are both const iterator
types. It is unspecified whether they are the same type.

This section only describes operations on `unordered_multiset` that are
not described in one of the requirement tables, or for which there is
additional semantic information.

``` cpp
namespace std {
  template <class Key,
            class Hash  = hash<Key>,
            class Pred  = std::equal_to<Key>,
            class Allocator = std::allocator<Key> >
  class unordered_multiset
  {
  public:
    // types
    typedef Key                                      key_type;
    typedef Key                                      value_type;
    typedef Hash                                     hasher;
    typedef Pred                                     key_equal;
    typedef Allocator                                allocator_type;
    typedef typename allocator_type::pointer         pointer;
    typedef typename allocator_type::const_pointer   const_pointer;
    typedef typename allocator_type::reference       reference;
    typedef typename allocator_type::const_reference const_reference;
    typedef implementation-defined                   size_type;
    typedef implementation-defined                   difference_type;

    typedef implementation-defined                   iterator;
    typedef implementation-defined                   const_iterator;
    typedef implementation-defined                   local_iterator;
    typedef implementation-defined                   const_local_iterator;

    // construct/destroy/copy
    explicit unordered_multiset(size_type n = see below,
                                const hasher& hf = hasher(),
                                const key_equal& eql = key_equal(),
                                const allocator_type& a = allocator_type());
    template <class InputIterator>
      unordered_multiset(InputIterator f, InputIterator l,
                         size_type n = see below,
                         const hasher& hf = hasher(),
                         const key_equal& eql = key_equal(),
                         const allocator_type& a = allocator_type());
    unordered_multiset(const unordered_multiset&);
    unordered_multiset(unordered_multiset&&);
    explicit unordered_multiset(const Allocator&);
    unordered_multiset(const unordered_multiset&, const Allocator&);
    unordered_multiset(unordered_multiset&&, const Allocator&);
    unordered_multiset(initializer_list<value_type>,
      size_type = see below,
      const hasher& hf = hasher(),
      const key_equal& eql = key_equal(),
      const allocator_type& a = allocator_type());
    ~unordered_multiset();
    unordered_multiset& operator=(const unordered_multiset&);
    unordered_multiset operator=(unordered_multiset&&);
    unordered_multiset& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // size and capacity
    bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // modifiers
    template <class... Args> iterator emplace(Args&&... args);
    template <class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& obj);
    iterator insert(value_type&& obj);
    iterator insert(const_iterator hint, const value_type& obj);
    iterator insert(const_iterator hint, value_type&& obj);
    template <class InputIterator> void insert(InputIterator first, InputIterator last);
    void insert(initializer_list<value_type>);

    iterator erase(const_iterator position);
    size_type erase(const key_type& k);
    iterator erase(const_iterator first, const_iterator last);
    void clear() noexcept;

    void swap(unordered_multiset&);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // lookup
    iterator       find(const key_type& k);
    const_iterator find(const key_type& k) const;
    size_type count(const key_type& k) const;
    std::pair<iterator, iterator>             equal_range(const key_type& k);
    std::pair<const_iterator, const_iterator> equal_range(const key_type& k) const;

    // bucket interface
    size_type bucket_count() const noexcept;
    size_type max_bucket_count() const noexcept;
    size_type bucket_size(size_type n) const;
    size_type bucket(const key_type& k) const;
    local_iterator begin(size_type n);
    const_local_iterator begin(size_type n) const;
    local_iterator end(size_type n);
    const_local_iterator end(size_type n) const;
    const_local_iterator cbegin(size_type n) const;
    const_local_iterator cend(size_type n) const;

    // hash policy
    float load_factor() const noexcept;
    float max_load_factor() const noexcept;
    void max_load_factor(float z);
    void rehash(size_type n);
    void reserve(size_type n);
  };

  template <class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_multiset<Key, Hash, Pred, Alloc>& x,
              unordered_multiset<Key, Hash, Pred, Alloc>& y);
    template <class Key, class T, class Hash, class Pred, class Alloc>
      bool operator==(const unordered_multiset<Key, T, Hash, Pred, Alloc>& a,
                      const unordered_multiset<Key, T, Hash, Pred, Alloc>& b);
    template <class Key, class T, class Hash, class Pred, class Alloc>
      bool operator!=(const unordered_multiset<Key, T, Hash, Pred, Alloc>& a,
                      const unordered_multiset<Key, T, Hash, Pred, Alloc>& b);
}
```

#### `unordered_multiset` constructors <a id="unord.multiset.cnstr">[[unord.multiset.cnstr]]</a>

``` cpp
explicit unordered_multiset(size_type n = see below,
                            const hasher& hf = hasher(),
                            const key_equal& eql = key_equal(),
                            const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multiset` using the specified
hash function, key equality function, and allocator, and using at least
*`n`* buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. `max_load_factor()` returns 1.0.

*Complexity:* Constant.

``` cpp
template <class InputIterator>
  unordered_multiset(InputIterator f, InputIterator l,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multiset` using the specified
hash function, key equality function, and allocator, and using at least
*`n`* buckets. If *`n`* is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range
`[`*`f`*`, `*`l`*`)`. `max_load_factor()` returns 1.0.

*Complexity:* Average case linear, worst case quadratic.

#### `unordered_multiset` swap <a id="unord.multiset.swap">[[unord.multiset.swap]]</a>

``` cpp
template <class Key, class Hash, class Pred, class Alloc>
  void swap(unordered_multiset<Key, Hash, Pred, Alloc>& x,
            unordered_multiset<Key, Hash, Pred, Alloc>& y);
```

*Effects:* `x.swap(y);`

## Container adaptors <a id="container.adaptors">[[container.adaptors]]</a>

### In general <a id="container.adaptors.general">[[container.adaptors.general]]</a>

The headers `<queue>` and `<stack>` define the container adaptors
`queue`, `priority_queue`, and `stack`. These container adaptors meet
the requirements for sequence containers.

The container adaptors each take a `Container` template parameter, and
each constructor takes a `Container` reference argument. This container
is copied into the `Container` member of each adaptor. If the container
takes an allocator, then a compatible allocator may be passed in to the
adaptor’s constructor. Otherwise, normal copy or move construction is
used for the container argument.

For container adaptors, no `swap` function throws an exception unless
that exception is thrown by the swap of the adaptor’s `Container` or
`Compare` object (if any).

### Header `<queue>` synopsis <a id="queue.syn">[[queue.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  template <class T, class Container = deque<T> > class queue;
  template <class T, class Container = vector<T>,
    class Compare = less<typename Container::value_type> >
      class priority_queue;

  template <class T, class Container>
    bool operator==(const queue<T, Container>& x,const queue<T, Container>& y);
  template <class T, class Container>
    bool operator< (const queue<T, Container>& x,const queue<T, Container>& y);
  template <class T, class Container>
    bool operator!=(const queue<T, Container>& x,const queue<T, Container>& y);
  template <class T, class Container>
    bool operator> (const queue<T, Container>& x,const queue<T, Container>& y);
  template <class T, class Container>
    bool operator>=(const queue<T, Container>& x,const queue<T, Container>& y);
  template <class T, class Container>
    bool operator<=(const queue<T, Container>& x,const queue<T, Container>& y);

  template <class T, class Container>
    void swap(queue<T, Container>& x, queue<T, Container>& y) noexcept(noexcept(x.swap(y)));
  template <class T, class Container, class Compare>
    void swap(priority_queue<T, Container, Compare>& x,
              priority_queue<T, Container, Compare>& y) noexcept(noexcept(x.swap(y)));
}
```

### Class template `queue` <a id="queue">[[queue]]</a>

#### `queue` definition <a id="queue.defn">[[queue.defn]]</a>

Any sequence container supporting operations `front()`, `back()`,
`push_back()` and `pop_front()` can be used to instantiate `queue`. In
particular, `list` ([[list]]) and `deque` ([[deque]]) can be used.

``` cpp
namespace std {
  template <class T, class Container = deque<T> >
  class queue {
  public:
    typedef typename Container::value_type            value_type;
    typedef typename Container::reference             reference;
    typedef typename Container::const_reference       const_reference;
    typedef typename Container::size_type             size_type;
    typedef          Container                        container_type;
  protected:
    Container c;

  public:
    explicit queue(const Container&);
    explicit queue(Container&& = Container());
    template <class Alloc> explicit queue(const Alloc&);
    template <class Alloc> queue(const Container&, const Alloc&);
    template <class Alloc> queue(Container&&, const Alloc&);
    template <class Alloc> queue(const queue&, const Alloc&);
    template <class Alloc> queue(queue&&, const Alloc&);

    bool              empty() const     { return c.empty(); }
    size_type         size()  const     { return c.size(); }
    reference         front()           { return c.front(); }
    const_reference   front() const     { return c.front(); }
    reference         back()            { return c.back(); }
    const_reference   back() const      { return c.back(); }
    void push(const value_type& x)      { c.push_back(x); }
    void push(value_type&& x)           { c.push_back(std::move(x)); }
    template <class... Args> void emplace(Args&&... args)
      { c.emplace_back(std::forward<Args>(args)...); }
    void pop()                          { c.pop_front(); }
    void swap(queue& q) noexcept(noexcept(swap(c, q.c)))
      { using std::swap; swap(c, q.c); }
  };

  template <class T, class Container>
    bool operator==(const queue<T, Container>& x, const queue<T, Container>& y);
  template <class T, class Container>
    bool operator< (const queue<T, Container>& x, const queue<T, Container>& y);
  template <class T, class Container>
    bool operator!=(const queue<T, Container>& x, const queue<T, Container>& y);
  template <class T, class Container>
    bool operator> (const queue<T, Container>& x, const queue<T, Container>& y);
  template <class T, class Container>
    bool operator>=(const queue<T, Container>& x, const queue<T, Container>& y);
  template <class T, class Container>
    bool operator<=(const queue<T, Container>& x, const queue<T, Container>& y);

  template <class T, class Container>
    void swap(queue<T, Container>& x, queue<T, Container>& y) noexcept(noexcept(x.swap(y)));

  template <class T, class Container, class Alloc>
    struct uses_allocator<queue<T, Container>, Alloc>
      : uses_allocator<Container, Alloc>::type { };
}
```

#### `queue` constructors <a id="queue.cons">[[queue.cons]]</a>

``` cpp
explicit queue(const Container& cont);
```

*Effects:*  Initializes `c` with `cont`.

``` cpp
explicit queue(Container&& cont = Container());
```

*Effects:*  Initializes `c` with `std::move(cont)`.

#### `queue` constructors with allocators <a id="queue.cons.alloc">[[queue.cons.alloc]]</a>

If `uses_allocator<container_type, Alloc>::value` is `false` the
constructors in this subclause shall not participate in overload
resolution.

``` cpp
template <class Alloc>
  explicit queue(const Alloc& a);
```

*Effects:*  Initializes `c` with `a`.

``` cpp
template <class Alloc>
  queue(const container_type& cont, const Alloc& a);
```

*Effects:*  Initializes `c` with `cont` as the first argument and `a` as
the second argument.

``` cpp
template <class Alloc>
  queue(container_type&& cont, const Alloc& a);
```

*Effects:*  Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument.

``` cpp
template <class Alloc>
  queue(const queue& q, const Alloc& a);
```

*Effects:*  Initializes `c` with `q.c` as the first argument and `a` as
the second argument.

``` cpp
template <class Alloc>
  queue(queue&& q, const Alloc& a);
```

*Effects:*  Initializes `c` with `std::move(q.c)` as the first argument
and `a` as the second argument.

#### `queue` operators <a id="queue.ops">[[queue.ops]]</a>

``` cpp
template <class T, class Container>
    bool operator==(const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c == y.c`.

``` cpp
template <class T, class Container>
    bool operator!=(const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c != y.c`.

``` cpp
template <class T, class Container>
    bool operator< (const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c < y.c`.

``` cpp
template <class T, class Container>
    bool operator<=(const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c <= y.c`.

``` cpp
template <class T, class Container>
    bool operator> (const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c > y.c`.

``` cpp
template <class T, class Container>
    bool operator>=(const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c >= y.c`.

#### `queue` specialized algorithms <a id="queue.special">[[queue.special]]</a>

``` cpp
template <class T, class Container>
  void swap(queue<T, Container>& x, queue<T, Container>& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* `x.swap(y)`.

### Class template `priority_queue` <a id="priority.queue">[[priority.queue]]</a>

Any sequence container with random access iterator and supporting
operations `front()`, `push_back()` and `pop_back()` can be used to
instantiate `priority_queue`. In particular, `vector` ([[vector]]) and
`deque` ([[deque]]) can be used. Instantiating `priority_queue` also
involves supplying a function or function object for making priority
comparisons; the library assumes that the function or function object
defines a strict weak ordering ([[alg.sorting]]).

``` cpp
namespace std {
  template <class T, class Container = vector<T>,
    class Compare = less<typename Container::value_type> >
  class priority_queue {
  public:
    typedef typename Container::value_type            value_type;
    typedef typename Container::reference             reference;
    typedef typename Container::const_reference       const_reference;
    typedef typename Container::size_type             size_type;
    typedef          Container                        container_type;
  protected:
    Container c;
    Compare comp;

  public:
    priority_queue(const Compare& x, const Container&);
    explicit priority_queue(const Compare& x = Compare(), Container&& = Container());
    template <class InputIterator>
      priority_queue(InputIterator first, InputIterator last,
             const Compare& x, const Container&);
    template <class InputIterator>
      priority_queue(InputIterator first, InputIterator last,
             const Compare& x = Compare(), Container&& = Container());
    template <class Alloc> explicit priority_queue(const Alloc&);
    template <class Alloc> priority_queue(const Compare&, const Alloc&);
    template <class Alloc> priority_queue(const Compare&,
      const Container&, const Alloc&);
    template <class Alloc> priority_queue(const Compare&,
      Container&&, const Alloc&);
    template <class Alloc> priority_queue(const priority_queue&, const Alloc&);
    template <class Alloc> priority_queue(priority_queue&&, const Alloc&);

    bool      empty() const       { return c.empty(); }
    size_type size()  const       { return c.size(); }
    const_reference   top() const { return c.front(); }
    void push(const value_type& x);
    void push(value_type&& x);
    template <class... Args> void emplace(Args&&... args);
    void pop();
    void swap(priority_queue& q) noexcept(
        noexcept(swap(c, q.c)) && noexcept(swap(comp, q.comp)))
      { using std::swap; swap(c, q.c); swap(comp, q.comp); }
  };
  // no equality is provided
  template <class T, class Container, class Compare>
    void swap(priority_queue<T, Container, Compare>& x,
              priority_queue<T, Container, Compare>& y) noexcept(noexcept(x.swap(y)));

  template <class T, class Container, class Compare, class Alloc>
    struct uses_allocator<priority_queue<T, Container, Compare>, Alloc>
      : uses_allocator<Container, Alloc>::type { };
}
```

#### `priority_queue` constructors <a id="priqueue.cons">[[priqueue.cons]]</a>

``` cpp
priority_queue(const Compare& x,
               const Container& y);
explicit priority_queue(const Compare& x = Compare(),
               Container&& y = Container());
```

*Requires:* `x` shall define a strict weak ordering ([[alg.sorting]]).

*Effects:* Initializes `comp` with `x` and `c` with `y` (copy
constructing or move constructing as appropriate); calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template <class InputIterator>
  priority_queue(InputIterator first, InputIterator last,
                 const Compare& x,
                 const Container& y);
template <class InputIterator>
  priority_queue(InputIterator first, InputIterator last,
                 const Compare& x = Compare(),
                 Container&& y = Container());
```

*Requires:* `x` shall define a strict weak ordering ([[alg.sorting]]).

*Effects:* Initializes `comp` with `x` and `c` with `y` (copy
constructing or move constructing as appropriate); calls
`c.insert(c.end(), first, last)`; and finally calls
`make_heap(c.begin(), c.end(), comp)`.

#### `priority_queue` constructors with allocators <a id="priqueue.cons.alloc">[[priqueue.cons.alloc]]</a>

If `uses_allocator<container_type, Alloc>::value` is `false` the
constructors in this subclause shall not participate in overload
resolution.

``` cpp
template <class Alloc>
  explicit priority_queue(const Alloc& a);
```

*Effects:*  Initializes `c` with `a` and value-initializes `comp`.

``` cpp
template <class Alloc>
  priority_queue(const Compare& compare, const Alloc& a);
```

*Effects:*  Initializes `c` with `a` and initializes `comp` with
`compare`.

``` cpp
template <class Alloc>
  priority_queue(const Compare& compare, const Container& cont, const Alloc& a);
```

*Effects:*  Initializes `c` with `cont` as the first argument and `a` as
the second argument, and initializes `comp` with `compare`.

``` cpp
template <class Alloc>
  priority_queue(const Compare& compare, Container&& cont, const Alloc& a);
```

*Effects:*  Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument, and initializes `comp` with `compare`.

``` cpp
template <class Alloc>
  priority_queue(const priority_queue& q, const Alloc& a);
```

*Effects:*  Initializes `c` with `q.c` as the first argument and `a` as
the second argument, and initializes `comp` with `q.comp`.

``` cpp
template <class Alloc>
  priority_queue(priority_queue&& q, const Alloc& a);
```

*Effects:*  Initializes `c` with `std::move(q.c)` as the first argument
and `a` as the second argument, and initializes `comp` with
`std::move(q.comp)`.

#### `priority_queue` members <a id="priqueue.members">[[priqueue.members]]</a>

``` cpp
void push(const value_type& x);
```

*Effects:*

``` cpp
c.push_back(x);
push_heap(c.begin(), c.end(), comp);
```

``` cpp
void push(value_type&& x);
```

*Effects:*

``` cpp
c.push_back(std::move(x));
push_heap(c.begin(), c.end(), comp);
```

``` cpp
template <class... Args> void emplace(Args&&... args)
```

*Effects:*

``` cpp
c.emplace_back(std::forward<Args>(args)...);
push_heap(c.begin(), c.end(), comp);
```

``` cpp
void pop();
```

*Effects:*

``` cpp
pop_heap(c.begin(), c.end(), comp);
c.pop_back();
```

#### `priority_queue` specialized algorithms <a id="priqueue.special">[[priqueue.special]]</a>

``` cpp
template <class T, class Container, Compare>
  void swap(priority_queue<T, Container, Compare>& x,
            priority_queue<T, Container, Compare>& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* `x.swap(y)`.

### Class template `stack` <a id="stack">[[stack]]</a>

Any sequence container supporting operations `back()`, `push_back()` and
`pop_back()` can be used to instantiate `stack`. In particular,
`vector` ([[vector]]), `list` ([[list]]) and `deque` ([[deque]]) can
be used.

#### Header `<stack>` synopsis <a id="stack.syn">[[stack.syn]]</a>

``` cpp
#include <initializer_list>

namespace std {

  template <class T, class Container = deque<T> > class stack;
  template <class T, class Container>
    bool operator==(const stack<T, Container>& x,const stack<T, Container>& y);
  template <class T, class Container>
    bool operator< (const stack<T, Container>& x,const stack<T, Container>& y);
  template <class T, class Container>
    bool operator!=(const stack<T, Container>& x,const stack<T, Container>& y);
  template <class T, class Container>
    bool operator> (const stack<T, Container>& x,const stack<T, Container>& y);
  template <class T, class Container>
    bool operator>=(const stack<T, Container>& x,const stack<T, Container>& y);
  template <class T, class Container>
    bool operator<=(const stack<T, Container>& x,const stack<T, Container>& y);
  template <class T, class Container>
    void swap(stack<T, Container>& x, stack<T, Container>& y) noexcept(noexcept(x.swap(y)));
}
```

#### `stack` definition <a id="stack.defn">[[stack.defn]]</a>

``` cpp
namespace std {
  template <class T, class Container = deque<T> >
  class stack {
  public:
    typedef typename Container::value_type            value_type;
    typedef typename Container::reference             reference;
    typedef typename Container::const_reference       const_reference;
    typedef typename Container::size_type             size_type;
    typedef          Container                        container_type;
  protected:
    Container c;

  public:
    explicit stack(const Container&);
    explicit stack(Container&& = Container());
    template <class Alloc> explicit stack(const Alloc&);
    template <class Alloc> stack(const Container&, const Alloc&);
    template <class Alloc> stack(Container&&, const Alloc&);
    template <class Alloc> stack(const stack&, const Alloc&);
    template <class Alloc> stack(stack&&, const Alloc&);

    bool      empty() const             { return c.empty(); }
    size_type size()  const             { return c.size(); }
    reference         top()             { return c.back(); }
    const_reference   top() const       { return c.back(); }
    void push(const value_type& x)      { c.push_back(x); }
    void push(value_type&& x)           { c.push_back(std::move(x)); }
    template <class... Args> void emplace(Args&&... args)
      { c.emplace_back(std::forward<Args>(args)...); }
    void pop()                          { c.pop_back(); }
    void swap(stack& s) noexcept(noexcept(swap(c, s.c)))
      { using std::swap; swap(c, s.c); }
  };

  template <class T, class Container>
    bool operator==(const stack<T, Container>& x, const stack<T, Container>& y);
  template <class T, class Container>
    bool operator< (const stack<T, Container>& x, const stack<T, Container>& y);
  template <class T, class Container>
    bool operator!=(const stack<T, Container>& x, const stack<T, Container>& y);
  template <class T, class Container>
    bool operator> (const stack<T, Container>& x, const stack<T, Container>& y);
  template <class T, class Container>
    bool operator>=(const stack<T, Container>& x, const stack<T, Container>& y);
  template <class T, class Container>
    bool operator<=(const stack<T, Container>& x, const stack<T, Container>& y);
  template <class T, class Allocator>
    void swap(stack<T,Allocator>& x, stack<T,Allocator>& y);

  template <class T, class Container, class Alloc>
    struct uses_allocator<stack<T, Container>, Alloc>
      : uses_allocator<Container, Alloc>::type { };
}
```

#### `stack` constructors <a id="stack.cons">[[stack.cons]]</a>

``` cpp
explicit stack(const Container& cont);
```

*Effects:* Initializes `c` with `cont`.

``` cpp
explicit stack(Container&& const = Container());
```

*Effects:* Initializes `c` with `std::move(cont)`.

#### `stack` constructors with allocators <a id="stack.cons.alloc">[[stack.cons.alloc]]</a>

If `uses_allocator<container_type, Alloc>::value` is `false` the
constructors in this subclause shall not participate in overload
resolution.

``` cpp
template <class Alloc>
  explicit stack(const Alloc& a);
```

*Effects:*  Initializes `c` with `a`.

``` cpp
template <class Alloc>
  stack(const container_type& cont, const Alloc& a);
```

*Effects:*  Initializes `c` with `cont` as the first argument and `a` as
the second argument.

``` cpp
template <class Alloc>
  stack(container_type&& cont, const Alloc& a);
```

*Effects:*  Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument.

``` cpp
template <class Alloc>
  stack(const stack& s, const Alloc& a);
```

*Effects:*  Initializes `c` with `s.c` as the first argument and `a` as
the second argument.

``` cpp
template <class Alloc>
  stack(stack&& s, const Alloc& a);
```

*Effects:*  Initializes `c` with `std::move(s.c)` as the first argument
and `a` as the second argument.

#### `stack` operators <a id="stack.ops">[[stack.ops]]</a>

``` cpp
template <class T, class Container>
    bool operator==(const stack<T, Container>& x,
                    const stack<T, Container>& y);
```

*Returns:* `x.c == y.c`.

``` cpp
template <class T, class Container>
    bool operator!=(const stack<T, Container>& x,
                    const stack<T, Container>& y);
```

*Returns:* `x.c != y.c`.

``` cpp
template <class T, class Container>
    bool operator< (const stack<T, Container>& x,
                    const stack<T, Container>& y);
```

*Returns:* `x.c < y.c`.

``` cpp
template <class T, class Container>
    bool operator<=(const stack<T, Container>& x,
                    const stack<T, Container>& y);
```

*Returns:* `x.c <= y.c`.

``` cpp
template <class T, class Container>
    bool operator> (const stack<T, Container>& x,
                    const stack<T, Container>& y);
```

*Returns:* `x.c > y.c`.

``` cpp
template <class T, class Container>
    bool operator>=(const stack<T, Container>& x,
                    const stack<T, Container>& y);
```

*Returns:* `x.c >= y.c`.

#### `stack` specialized algorithms <a id="stack.special">[[stack.special]]</a>

``` cpp
template <class T, class Container>
  void swap(stack<T, Container>& x, stack<T, Container>& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* `x.swap(y)`.

<!-- Section link definitions -->
[array]: #array
[array.cons]: #array.cons
[array.data]: #array.data
[array.fill]: #array.fill
[array.overview]: #array.overview
[array.size]: #array.size
[array.special]: #array.special
[array.swap]: #array.swap
[array.tuple]: #array.tuple
[array.zero]: #array.zero
[associative]: #associative
[associative.general]: #associative.general
[associative.map.syn]: #associative.map.syn
[associative.reqmts]: #associative.reqmts
[associative.reqmts.except]: #associative.reqmts.except
[associative.set.syn]: #associative.set.syn
[container.adaptors]: #container.adaptors
[container.adaptors.general]: #container.adaptors.general
[container.requirements]: #container.requirements
[container.requirements.dataraces]: #container.requirements.dataraces
[container.requirements.general]: #container.requirements.general
[containers]: #containers
[containers.general]: #containers.general
[deque]: #deque
[deque.capacity]: #deque.capacity
[deque.cons]: #deque.cons
[deque.modifiers]: #deque.modifiers
[deque.overview]: #deque.overview
[deque.special]: #deque.special
[forwardlist]: #forwardlist
[forwardlist.access]: #forwardlist.access
[forwardlist.cons]: #forwardlist.cons
[forwardlist.iter]: #forwardlist.iter
[forwardlist.modifiers]: #forwardlist.modifiers
[forwardlist.ops]: #forwardlist.ops
[forwardlist.overview]: #forwardlist.overview
[forwardlist.spec]: #forwardlist.spec
[list]: #list
[list.capacity]: #list.capacity
[list.cons]: #list.cons
[list.modifiers]: #list.modifiers
[list.ops]: #list.ops
[list.overview]: #list.overview
[list.special]: #list.special
[map]: #map
[map.access]: #map.access
[map.cons]: #map.cons
[map.modifiers]: #map.modifiers
[map.ops]: #map.ops
[map.overview]: #map.overview
[map.special]: #map.special
[multimap]: #multimap
[multimap.cons]: #multimap.cons
[multimap.modifiers]: #multimap.modifiers
[multimap.ops]: #multimap.ops
[multimap.overview]: #multimap.overview
[multimap.special]: #multimap.special
[multiset]: #multiset
[multiset.cons]: #multiset.cons
[multiset.overview]: #multiset.overview
[multiset.special]: #multiset.special
[priority.queue]: #priority.queue
[priqueue.cons]: #priqueue.cons
[priqueue.cons.alloc]: #priqueue.cons.alloc
[priqueue.members]: #priqueue.members
[priqueue.special]: #priqueue.special
[queue]: #queue
[queue.cons]: #queue.cons
[queue.cons.alloc]: #queue.cons.alloc
[queue.defn]: #queue.defn
[queue.ops]: #queue.ops
[queue.special]: #queue.special
[queue.syn]: #queue.syn
[sequence.reqmts]: #sequence.reqmts
[sequences]: #sequences
[sequences.general]: #sequences.general
[set]: #set
[set.cons]: #set.cons
[set.overview]: #set.overview
[set.special]: #set.special
[stack]: #stack
[stack.cons]: #stack.cons
[stack.cons.alloc]: #stack.cons.alloc
[stack.defn]: #stack.defn
[stack.ops]: #stack.ops
[stack.special]: #stack.special
[stack.syn]: #stack.syn
[unord]: #unord
[unord.general]: #unord.general
[unord.map]: #unord.map
[unord.map.cnstr]: #unord.map.cnstr
[unord.map.elem]: #unord.map.elem
[unord.map.modifiers]: #unord.map.modifiers
[unord.map.overview]: #unord.map.overview
[unord.map.swap]: #unord.map.swap
[unord.map.syn]: #unord.map.syn
[unord.multimap]: #unord.multimap
[unord.multimap.cnstr]: #unord.multimap.cnstr
[unord.multimap.modifiers]: #unord.multimap.modifiers
[unord.multimap.overview]: #unord.multimap.overview
[unord.multimap.swap]: #unord.multimap.swap
[unord.multiset]: #unord.multiset
[unord.multiset.cnstr]: #unord.multiset.cnstr
[unord.multiset.overview]: #unord.multiset.overview
[unord.multiset.swap]: #unord.multiset.swap
[unord.req]: #unord.req
[unord.req.except]: #unord.req.except
[unord.set]: #unord.set
[unord.set.cnstr]: #unord.set.cnstr
[unord.set.overview]: #unord.set.overview
[unord.set.swap]: #unord.set.swap
[unord.set.syn]: #unord.set.syn
[vector]: #vector
[vector.bool]: #vector.bool
[vector.capacity]: #vector.capacity
[vector.cons]: #vector.cons
[vector.data]: #vector.data
[vector.modifiers]: #vector.modifiers
[vector.overview]: #vector.overview
[vector.special]: #vector.special

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[algorithms]: algorithms.md#algorithms
[allocator.requirements]: library.md#allocator.requirements
[allocator.traits.members]: utilities.md#allocator.traits.members
[associative]: #associative
[associative.reqmts]: #associative.reqmts
[associative.reqmts.except]: #associative.reqmts.except
[basic.string]: strings.md#basic.string
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.dtor]: special.md#class.dtor
[container.adaptors]: #container.adaptors
[container.requirements]: #container.requirements
[container.requirements.general]: #container.requirements.general
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[deque]: #deque
[deque.modifiers]: #deque.modifiers
[forward.iterators]: iterators.md#forward.iterators
[hash.requirements]: library.md#hash.requirements
[iterator.requirements]: iterators.md#iterator.requirements
[list]: #list
[res.on.data.races]: library.md#res.on.data.races
[sequence.reqmts]: #sequence.reqmts
[sequences]: #sequences
[strings]: strings.md#strings
[tab:HashRequirements]: #tab:HashRequirements
[tab:containers.allocatoraware]: #tab:containers.allocatoraware
[tab:containers.associative.requirements]: #tab:containers.associative.requirements
[tab:containers.container.requirements]: #tab:containers.container.requirements
[tab:containers.lib.summary]: #tab:containers.lib.summary
[tab:containers.optional.operations]: #tab:containers.optional.operations
[tab:containers.reversible.requirements]: #tab:containers.reversible.requirements
[tab:containers.sequence.optional]: #tab:containers.sequence.optional
[tab:containers.sequence.requirements]: #tab:containers.sequence.requirements
[unord]: #unord
[unord.hash]: utilities.md#unord.hash
[unord.req.except]: #unord.req.except
[vector]: #vector
[vector.modifiers]: #vector.modifiers

[^1]: Equality comparison is a refinement of partitioning if no two
    objects that compare equal fall into different partitions.

[^2]: These member functions are only provided by containers whose
    iterators are random access iterators.

[^3]: As specified in  [[allocator.requirements]], the requirements in
    this Clause apply only to lists whose allocators compare equal.

[^4]: `reserve()` uses `Allocator::allocate()` which may throw an
    appropriate exception.
