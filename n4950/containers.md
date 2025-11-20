# Containers library <a id="containers">[[containers]]</a>

## General <a id="containers.general">[[containers.general]]</a>

This Clause describes components that C++ programs may use to organize
collections of information.

The following subclauses describe container requirements, and components
for sequence containers and associative containers, as summarized in
[[containers.summary]].

**Table: Containers library summary**

| Subclause                  |                                  | Header                                                       |
| -------------------------- | -------------------------------- | ------------------------------------------------------------ |
| [[container.requirements]] | Requirements                     |                                                              |
| [[sequences]]              | Sequence containers              | `<array>`, `<deque>`, `<forward_list>`, `<list>`, `<vector>` |
| [[associative]]            | Associative containers           | `<map>`, `<set>`                                             |
| [[unord]]                  | Unordered associative containers | `<unordered_map>`, `<unordered_set>`                         |
| [[container.adaptors]]     | Container adaptors               | `<queue>`, `<stack>`, `<flat_map>`, `<flat_set>`             |
| [[views]]                  | Views                            | `<span>`, `<mdspan>`                                         |


## Requirements <a id="container.requirements">[[container.requirements]]</a>

### Preamble <a id="container.requirements.pre">[[container.requirements.pre]]</a>

Containers are objects that store other objects. They control allocation
and deallocation of these objects through constructors, destructors,
insert and erase operations.

All of the complexity requirements in this Clause are stated solely in
terms of the number of operations on the contained objects.

[*Example 1*: The copy constructor of type `vector<vector<int>>` has
linear complexity, even though the complexity of copying each contained
`vector<int>` is itself linear. — *end example*]

Allocator-aware containers [[container.alloc.reqmts]] other than
`basic_string` construct elements using the function
`allocator_traits<allocator_type>::rebind_traits<U>::{}construct` and
destroy elements using the function
`allocator_traits<allocator_type>::rebind_traits<U>::{}destroy`
[[allocator.traits.members]], where `U` is either
`allocator_type::value_type` or an internal type used by the container.
These functions are called only for the container’s element type, not
for internal types used by the container.

[*Note 1*: This means, for example, that a node-based container would
need to construct nodes containing aligned buffers and call `construct`
to place the element into the buffer. — *end note*]

### General containers <a id="container.gen.reqmts">[[container.gen.reqmts]]</a>

#### General <a id="container.requirements.general">[[container.requirements.general]]</a>

In subclause [[container.gen.reqmts]],

- `X` denotes a container class containing objects of type `T`,
- `a` denotes a value of type `X`,
- `b` and `c` denote values of type (possibly const) `X`,
- `i` and `j` denote values of type (possibly const) `X::iterator`,
- `u` denotes an identifier,
- `v` denotes an lvalue of type (possibly const) `X` or an rvalue of
  type `const X`,
- `s` and `t` denote non-const lvalues of type `X`, and
- `rv` denotes a non-const rvalue of type `X`.

The following exposition-only concept is used in the definition of
containers:

``` cpp
template<class R, class T>
concept container-compatible-range =    // exposition only
  ranges::input_range<R> && convertible_to<ranges::range_reference_t<R>, T>;
```

#### Containers <a id="container.reqmts">[[container.reqmts]]</a>

A type `X` meets the *container* requirements if the following types,
statements, and expressions are well-formed and have the specified
semantics.

``` cpp
typename X::value_type
```

*Result:* `T`

*Preconditions:* `T` is *Cpp17Erasable* from `X`
(see  [[container.alloc.reqmts]], below).

``` cpp
typename X::reference
```

*Result:* `T&`

``` cpp
typename X::const_reference
```

*Result:* `const T&`

``` cpp
typename X::iterator
```

*Result:* A type that meets the forward iterator
requirements [[forward.iterators]] with value type `T`. The type
`X::iterator` is convertible to `X::const_iterator`.

``` cpp
typename X::const_iterator
```

*Result:* A type that meets the requirements of a constant iterator and
those of a forward iterator with value type `T`.

``` cpp
typename X::difference_type
```

*Result:* A signed integer type, identical to the difference type of
`X::iterator` and `X::const_iterator`.

``` cpp
typename X::size_type
```

*Result:* An unsigned integer type that can represent any non-negative
value of `X::difference_type`.

``` cpp
X u;
X u = X();
```

*Ensures:* `u.empty()`

*Complexity:* Constant.

``` cpp
X u(v);
X u = v;
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X` (see below).

*Ensures:* `u == v`.

*Complexity:* Linear.

``` cpp
X u(rv);
X u = rv;
```

*Ensures:* `u` is equal to the value that `rv` had before this
construction.

*Complexity:* Linear for `array` and constant for all other standard
containers.

``` cpp
t = v;
```

*Result:* `X&`.

*Ensures:* `t == v`.

*Complexity:* Linear.

``` cpp
t = rv
```

*Result:* `X&`.

*Effects:* All existing elements of `t` are either move assigned to or
destroyed.

*Ensures:* If `t` and `rv` do not refer to the same object, `t` is equal
to the value that `rv` had before this assignment.

*Complexity:* Linear.

``` cpp
a.~X()
```

*Result:* `void`.

*Effects:* Destroys every element of `a`; any memory obtained is
deallocated.

*Complexity:* Linear.

``` cpp
b.begin()
```

*Result:* `iterator`; `const_iterator` for constant `b`.

*Returns:* An iterator referring to the first element in the container.

*Complexity:* Constant.

``` cpp
b.end()
```

*Result:* `iterator`; `const_iterator` for constant `b`.

*Returns:* An iterator which is the past-the-end value for the
container.

*Complexity:* Constant.

``` cpp
b.cbegin()
```

*Result:* `const_iterator`.

*Returns:* `const_cast<X const&>(b).begin()`

*Complexity:* Constant.

``` cpp
b.cend()
```

*Result:* `const_iterator`.

*Returns:* `const_cast<X const&>(b).end()`

*Complexity:* Constant.

``` cpp
i <=> j
```

*Result:* `strong_ordering`.

*Constraints:* `X::iterator` meets the random access iterator
requirements.

*Complexity:* Constant.

``` cpp
c == b
```

*Preconditions:* `T` meets the *Cpp17EqualityComparable* requirements.

*Result:* `bool`.

*Returns:* `equal(c.begin(), c.end(), b.begin(), b.end())`

[*Note 1*: The algorithm `equal` is defined in
[[alg.equal]]. — *end note*]

*Complexity:* Constant if `c.size() != b.size()`, linear otherwise.

*Remarks:* `==` is an equivalence relation.

``` cpp
c != b
```

*Effects:* Equivalent to `!(c == b)`.

``` cpp
t.swap(s)
```

*Result:* `void`.

*Effects:* Exchanges the contents of `t` and `s`.

*Complexity:* Linear for `array` and constant for all other standard
containers.

``` cpp
swap(t, s)
```

*Effects:* Equivalent to `t.swap(s)`.

``` cpp
c.size()
```

*Result:* `size_type`.

*Returns:* `distance(c.begin(), c.end())`, i.e., the number of elements
in the container.

*Complexity:* Constant.

*Remarks:* The number of elements is defined by the rules of
constructors, inserts, and erases.

``` cpp
c.max_size()
```

*Result:* `size_type`.

*Returns:* `distance(begin(), end())` for the largest possible
container.

*Complexity:* Constant.

``` cpp
c.empty()
```

*Result:* `bool`.

*Returns:* `c.begin() == c.end()`

*Complexity:* Constant.

*Remarks:* If the container is empty, then `c.empty()` is `true`.

In the expressions

``` cpp
i == j
i != j
i < j
i <= j
i >= j
i > j
i <=> j
i - j
```

where `i` and `j` denote objects of a container’s `iterator` type,
either or both may be replaced by an object of the container’s
`const_iterator` type referring to the same element with no change in
semantics.

Unless otherwise specified, all containers defined in this Clause obtain
memory using an allocator (see  [[allocator.requirements]]).

[*Note 1*: In particular, containers and iterators do not store
references to allocated elements other than through the allocator’s
pointer type, i.e., as objects of type `P` or
`pointer_traits<P>::template rebind<unspecified>`, where `P` is
`allocator_traits<allocator_type>::pointer`. — *end note*]

Copy constructors for these container types obtain an allocator by
calling
`allocator_traits<allocator_type>::select_on_container_copy_construction`
on the allocator belonging to the container being copied. Move
constructors obtain an allocator by move construction from the allocator
belonging to the container being moved. Such move construction of the
allocator shall not exit via an exception. All other constructors for
these container types take a `const allocator_type&` argument.

[*Note 2*: If an invocation of a constructor uses the default value of
an optional allocator argument, then the allocator type must support
value-initialization. — *end note*]

A copy of this allocator is used for any memory allocation and element
construction performed, by these constructors and by all member
functions, during the lifetime of each container object or until the
allocator is replaced. The allocator may be replaced only via assignment
or `swap()`. Allocator replacement is performed by copy assignment, move
assignment, or swapping of the allocator only if

- `allocator_traits<allocator_type>::propagate_on_container_copy_assignment::value`,
- `allocator_traits<allocator_type>::propagate_on_container_move_assignment::value`,
  or
- `allocator_traits<allocator_type>::propagate_on_container_swap::value`

is `true` within the implementation of the corresponding container
operation. In all container types defined in this Clause, the member
`get_allocator()` returns a copy of the allocator used to construct the
container or, if that allocator has been replaced, a copy of the most
recent replacement.

The expression `a.swap(b)`, for containers `a` and `b` of a standard
container type other than `array`, shall exchange the values of `a` and
`b` without invoking any move, copy, or swap operations on the
individual container elements. Any `Compare`, `Pred`, or `Hash` types
belonging to `a` and `b` shall meet the *Cpp17Swappable* requirements
and shall be exchanged by calling `swap` as described in 
[[swappable.requirements]]. If
`allocator_traits<allocator_type>::propagate_on_container_swap::value`
is `true`, then `allocator_type` shall meet the *Cpp17Swappable*
requirements and the allocators of `a` and `b` shall also be exchanged
by calling `swap` as described in  [[swappable.requirements]].
Otherwise, the allocators shall not be swapped, and the behavior is
undefined unless `a.get_allocator() == b.get_allocator()`. Every
iterator referring to an element in one container before the swap shall
refer to the same element in the other container after the swap. It is
unspecified whether an iterator with value `a.end()` before the swap
will have value `b.end()` after the swap.

Unless otherwise specified (see  [[associative.reqmts.except]],
[[unord.req.except]], [[deque.modifiers]], and [[vector.modifiers]]) all
container types defined in this Clause meet the following additional
requirements:

- If an exception is thrown by an `insert()` or `emplace()` function
  while inserting a single element, that function has no effects.
- If an exception is thrown by a `push_back()`, `push_front()`,
  `emplace_back()`, or `emplace_front()` function, that function has no
  effects.
- No `erase()`, `clear()`, `pop_back()` or `pop_front()` function throws
  an exception.
- No copy constructor or assignment operator of a returned iterator
  throws an exception.
- No `swap()` function throws an exception.
- No `swap()` function invalidates any references, pointers, or
  iterators referring to the elements of the containers being swapped.
  \[*Note 1*: The `end()` iterator does not refer to any element, so it
  can be invalidated. — *end note*]

Unless otherwise specified (either explicitly or by defining a function
in terms of other functions), invoking a container member function or
passing a container as an argument to a library function shall not
invalidate iterators to, or change the values of, objects within that
container.

A *contiguous container* is a container whose member types `iterator`
and `const_iterator` meet the *Cpp17RandomAccessIterator* requirements
[[random.access.iterators]] and model `contiguous_iterator`
[[iterator.concept.contiguous]].

The behavior of certain container member functions and deduction guides
depends on whether types qualify as input iterators or allocators. The
extent to which an implementation determines that a type cannot be an
input iterator is unspecified, except that as a minimum integral types
shall not qualify as input iterators. Likewise, the extent to which an
implementation determines that a type cannot be an allocator is
unspecified, except that as a minimum a type `A` shall not qualify as an
allocator unless it meets both of the following conditions:

- The *qualified-id* `A::value_type` is valid and denotes a type
  [[temp.deduct]].
- The expression `declval<A&>().allocate(size_t{})` is well-formed when
  treated as an unevaluated operand.

#### Reversible container requirements <a id="container.rev.reqmts">[[container.rev.reqmts]]</a>

A type `X` meets the *reversible container* requirements if `X` meets
the container requirements, the iterator type of `X` belongs to the
bidirectional or random access iterator categories
[[iterator.requirements]], and the following types and expressions are
well-formed and have the specified semantics.

``` cpp
typename X::reverse_iterator
```

*Result:* The type `reverse_iterator<X::iterator>`, an iterator type
whose value type is `T`.

``` cpp
typename X::const_reverse_iterator
```

*Result:* The type `reverse_iterator<X::const_iterator>`, a constant
iterator type whose value type is `T`.

``` cpp
a.rbegin()
```

*Result:* `reverse_iterator`; `const_reverse_iterator` for constant `a`.

*Returns:* `reverse_iterator(end())`

*Complexity:* Constant.

``` cpp
a.rend()
```

*Result:* `reverse_iterator`; `const_reverse_iterator` for constant `a`.

*Returns:* `reverse_iterator(begin())`

*Complexity:* Constant.

``` cpp
a.crbegin()
```

*Result:* `const_reverse_iterator`.

*Returns:* `const_cast<X const&>(a).rbegin()`

*Complexity:* Constant.

``` cpp
a.crend()
```

*Result:* `const_reverse_iterator`.

*Returns:* `const_cast<X const&>(a).rend()`

*Complexity:* Constant.

#### Optional container requirements <a id="container.opt.reqmts">[[container.opt.reqmts]]</a>

The following operations are provided for some types of containers but
not others. Those containers for which the listed operations are
provided shall implement the semantics as described unless otherwise
stated. If the iterators passed to `lexicographical_compare_three_way`
meet the constexpr iterator requirements
[[iterator.requirements.general]] then the operations described below
are implemented by constexpr functions.

``` cpp
a <=> b
```

*Result:* *`synth-three-way-result`*`<X::value_type>`.

*Preconditions:* Either `<=>` is defined for values of type (possibly
const) `T`, or `<` is defined for values of type (possibly const) `T`
and `<` is a total ordering relationship.

*Returns:*
`lexicographical_compare_three_way(a.begin(), a.end(), b.begin(), b.end(),`*`synth-three-way`*`)`

[*Note 1*: The algorithm `lexicographical_compare_three_way` is defined
in [[algorithms]]. — *end note*]

*Complexity:* Linear.

#### Allocator-aware containers <a id="container.alloc.reqmts">[[container.alloc.reqmts]]</a>

All of the containers defined in [[containers]] and in  [[basic.string]]
except `array` meet the additional requirements of an
*allocator-aware container*, as described below.

Given an allocator type `A` and given a container type `X` having a
`value_type` identical to `T` and an `allocator_type` identical to
`allocator_traits<A>::rebind_alloc<T>` and given an lvalue `m` of type
`A`, a pointer `p` of type `T*`, an expression `v` of type `T` or
`const T`, and an rvalue `rv` of type `T`, the following terms are
defined. If `X` is not allocator-aware or is a specialization of
`basic_string`, the terms below are defined as if `A` were
`allocator<T>` — no allocator object needs to be created and user
specializations of `allocator<T>` are not instantiated:

- `T` is **Cpp17DefaultInsertable* into `X`* means that the following
  expression is well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p)
  ```
- An element of `X` is *default-inserted* if it is initialized by
  evaluation of the expression
  ``` cpp
  allocator_traits<A>::construct(m, p)
  ```

  where `p` is the address of the uninitialized storage for the element
  allocated within `X`.
- `T` is **Cpp17MoveInsertable* into `X`* means that the following
  expression is well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, rv)
  ```

  and its evaluation causes the following postcondition to hold: The
  value of `*p` is equivalent to the value of `rv` before the
  evaluation.
  \[*Note 2*: `rv` remains a valid object. Its state is
  unspecified — *end note*]
- `T` is **Cpp17CopyInsertable* into `X`* means that, in addition to `T`
  being *Cpp17MoveInsertable* into `X`, the following expression is
  well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, v)
  ```

  and its evaluation causes the following postcondition to hold: The
  value of `v` is unchanged and is equivalent to `*p`.
- `T` is **Cpp17EmplaceConstructible* into `X` from `args`*, for zero or
  more arguments `args`, means that the following expression is
  well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, args)
  ```
- `T` is **Cpp17Erasable* from `X`* means that the following expression
  is well-formed:
  ``` cpp
  allocator_traits<A>::destroy(m, p)
  ```

[*Note 1*: A container calls
`allocator_traits<A>::construct(m, p, args)` to construct an element at
`p` using `args`, with `m == get_allocator()`. The default `construct`
in `allocator` will call `::new((void*)p) T(args)`, but specialized
allocators can choose a different definition. — *end note*]

In this subclause,

- `X` denotes an allocator-aware container class with a `value_type` of
  `T` using an allocator of type `A`,
- `u` denotes a variable,
- `a` and `b` denote non-const lvalues of type `X`,
- `c` denotes an lvalue of type `const X`,
- `t` denotes an lvalue or a const rvalue of type `X`,
- `rv` denotes a non-const rvalue of type `X`, and
- `m` is a value of type `A`.

A type `X` meets the allocator-aware container requirements if `X` meets
the container requirements and the following types, statements, and
expressions are well-formed and have the specified semantics.

``` cpp
typename X::allocator_type
```

*Result:* `A`

*Mandates:* `allocator_type::value_type` is the same as `X::value_type`.

``` cpp
c.get_allocator()
```

*Result:* `A`

*Complexity:* Constant.

``` cpp
X u;
X u = X();
```

*Preconditions:* `A` meets the *Cpp17DefaultConstructible* requirements.

*Ensures:* `u.empty()` returns `true`, `u.get_allocator() == A()`.

*Complexity:* Constant.

``` cpp
X u(m);
```

*Ensures:* `u.empty()` returns `true`, `u.get_allocator() == m`.

*Complexity:* Constant.

``` cpp
X u(t, m);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X`.

*Ensures:* `u == t`, `u.get_allocator() == m`

*Complexity:* Linear.

``` cpp
X u(rv);
```

*Ensures:* `u` has the same elements as `rv` had before this
construction; the value of `u.get_allocator()` is the same as the value
of `rv.get_allocator()` before this construction.

*Complexity:* Constant.

``` cpp
X u(rv, m);
```

*Preconditions:* `T` is *Cpp17MoveInsertable* into `X`.

*Ensures:* `u` has the same elements, or copies of the elements, that
`rv` had before this construction, `u.get_allocator() == m`.

*Complexity:* Constant if `m == rv.get_allocator()`, otherwise linear.

``` cpp
a = t
```

*Result:* `X&`.

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X` and
*Cpp17CopyAssignable*.

*Ensures:* `a == t` is `true`.

*Complexity:* Linear.

``` cpp
a = rv
```

*Result:* `X&`.

*Preconditions:* If
`allocator_traits<allocator_type>::propagate_on_container_move_assignment::value`
is `false`, `T` is *Cpp17MoveInsertable* into `X` and
*Cpp17MoveAssignable*.

*Effects:* All existing elements of `a` are either move assigned to or
destroyed.

*Ensures:* If `a` and `rv` do not refer to the same object, `a` is equal
to the value that `rv` had before this assignment.

*Complexity:* Linear.

``` cpp
a.swap(b)
```

*Result:* `void`

*Effects:* Exchanges the contents of `a` and `b`.

*Complexity:* Constant.

### Container data races <a id="container.requirements.dataraces">[[container.requirements.dataraces]]</a>

For purposes of avoiding data races [[res.on.data.races]],
implementations shall consider the following functions to be `const`:
`begin`, `end`, `rbegin`, `rend`, `front`, `back`, `data`, `find`,
`lower_bound`, `upper_bound`, `equal_range`, `at` and, except in
associative or unordered associative containers, `operator[]`.

Notwithstanding  [[res.on.data.races]], implementations are required to
avoid data races when the contents of the contained object in different
elements in the same container, excepting `vector<bool>`, are modified
concurrently.

[*Note 1*: For a `vector<int> x` with a size greater than one,
`x[1] = 5` and `*x.begin() = 10` can be executed concurrently without a
data race, but `x[0] = 5` and `*x.begin() = 10` executed concurrently
can result in a data race. As an exception to the general rule, for a
`vector<bool> y`, `y[0] = true` can race with
`y[1] = true`. — *end note*]

### Sequence containers <a id="sequence.reqmts">[[sequence.reqmts]]</a>

A sequence container organizes a finite set of objects, all of the same
type, into a strictly linear arrangement. The library provides four
basic kinds of sequence containers: `vector`, `forward_list`, `list`,
and `deque`. In addition, `array` is provided as a sequence container
which provides limited sequence operations because it has a fixed number
of elements. The library also provides container adaptors that make it
easy to construct abstract data types, such as `stack`s, `queue`s,
`flat_map`s, `flat_multimap`s, `flat_set`s, or `flat_multiset`s, out of
the basic sequence container kinds (or out of other program-defined
sequence containers).

[*Note 1*: The sequence containers offer the programmer different
complexity trade-offs. `vector` is appropriate in most circumstances.
`array` has a fixed size known during translation. `list` or
`forward_list` support frequent insertions and deletions from the middle
of the sequence. `deque` supports efficient insertions and deletions
taking place at the beginning or at the end of the sequence. When
choosing a container, remember `vector` is best; leave a comment to
explain if you choose from the rest! — *end note*]

In this subclause,

- `X` denotes a sequence container class,
- `a` denotes a value of type `X` containing elements of type `T`,
- `u` denotes the name of a variable being declared,
- `A` denotes `X::allocator_type` if the *qualified-id*
  `X::allocator_type` is valid and denotes a type [[temp.deduct]] and
  `allocator<T>` if it doesn’t,
- `i` and `j` denote iterators that meet the *Cpp17InputIterator*
  requirements and refer to elements implicitly convertible to
  `value_type`,
- `[i, j)` denotes a valid range,
- `rg` denotes a value of a type `R` that models
  `container-compatible-range<T>`,
- `il` designates an object of type `initializer_list<value_type>`,
- `n` denotes a value of type `X::size_type`,
- `p` denotes a valid constant iterator to `a`,
- `q` denotes a valid dereferenceable constant iterator to `a`,
- `[q1, q2)` denotes a valid range of constant iterators in `a`,
- `t` denotes an lvalue or a const rvalue of `X::value_type`, and
- `rv` denotes a non-const rvalue of `X::value_type`.
- `Args` denotes a template parameter pack;
- `args` denotes a function parameter pack with the pattern `Args&&`.

The complexities of the expressions are sequence dependent.

A type `X` meets the *sequence container* requirements if `X` meets the
container requirements and the following statements and expressions are
well-formed and have the specified semantics.

``` cpp
X u(n, t);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X`.

*Effects:* Constructs a sequence container with `n` copies of `t`.

*Ensures:* `distance(u.begin(), u.end()) == n` is `true`.

``` cpp
X u(i, j);
```

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from `*i`.
For `vector`, if the iterator does not meet the *Cpp17ForwardIterator*
requirements [[forward.iterators]], `T` is also *Cpp17MoveInsertable*
into `X`.

*Effects:* Constructs a sequence container equal to the range `[i, j)`.
Each iterator in the range \[`i`, `j`) is dereferenced exactly once.

*Ensures:* `distance(u.begin(), u.end()) == distance(i, j)` is `true`.

``` cpp
X(from_range, rg)
```

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`. For `vector`, if `R` models neither
`ranges::sized_range` nor `ranges::forward_range`, `T` is also
*Cpp17MoveInsertable* into `X`.

*Effects:* Constructs a sequence container equal to the range `rg`. Each
iterator in the range `rg` is dereferenced exactly once.

*Ensures:* `distance(begin(), end()) == ranges::distance(rg)` is `true`.

``` cpp
X(il)
```

*Effects:* Equivalent to `X(il.begin(), il.end())`.

``` cpp
a = il
```

*Result:* `X&`.

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X` and
*Cpp17CopyAssignable*.

*Effects:* Assigns the range \[`il.begin()`, `il.end()`) into `a`. All
existing elements of `a` are either assigned to or destroyed.

*Returns:* `*this`.

``` cpp
a.emplace(p, args)
```

*Result:* `iterator`.

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`args`. For `vector` and `deque`, `T` is also *Cpp17MoveInsertable* into
`X` and *Cpp17MoveAssignable*.

*Effects:* Inserts an object of type `T` constructed with
`std::forward<Args>(args)...` before `p`.

[*Note 1*: `args` can directly or indirectly refer to a value in
`a`. — *end note*]

*Returns:* An iterator that points to the new element constructed from
`args` into `a`.

``` cpp
a.insert(p, t)
```

*Result:* `iterator`.

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X`. For `vector` and
`deque`, `T` is also *Cpp17CopyAssignable*.

*Effects:* Inserts a copy of `t` before `p`.

*Returns:* An iterator that points to the copy of `t` inserted into `a`.

``` cpp
a.insert(p, rv)
```

*Result:* `iterator`.

*Preconditions:* `T` is *Cpp17MoveInsertable* into `X`. For `vector` and
`deque`, `T` is also *Cpp17MoveAssignable*.

*Effects:* Inserts a copy of `rv` before `p`.

*Returns:* An iterator that points to the copy of `rv` inserted into
`a`.

``` cpp
a.insert(p, n, t)
```

*Result:* `iterator`.

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X` and
*Cpp17CopyAssignable*.

*Effects:* Inserts `n` copies of `t` before `p`.

*Returns:* An iterator that points to the copy of the first element
inserted into `a`, or `p` if `n == 0`.

``` cpp
a.insert(p, i, j)
```

*Result:* `iterator`.

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from `*i`.
For `vector` and `deque`, `T` is also *Cpp17MoveInsertable* into `X`,
and `T` meets the *Cpp17MoveConstructible*, *Cpp17MoveAssignable*, and
*Cpp17Swappable*[[swappable.requirements]] requirements. Neither `i` nor
`j` are iterators into `a`.

*Effects:* Inserts copies of elements in `[i, j)` before `p`. Each
iterator in the range \[`i`, `j`) shall be dereferenced exactly once.

*Returns:* An iterator that points to the copy of the first element
inserted into `a`, or `p` if `i == j`.

``` cpp
a.insert_range(p, rg)
```

*Result:* `iterator`.

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`. For `vector` and `deque`, `T` is also
*Cpp17MoveInsertable* into `X`, and `T` meets the
*Cpp17MoveConstructible*, *Cpp17MoveAssignable*, and
*Cpp17Swappable*[[swappable.requirements]] requirements. `rg` and `a` do
not overlap.

*Effects:* Inserts copies of elements in `rg` before `p`. Each iterator
in the range `rg` is dereferenced exactly once.

*Returns:* An iterator that points to the copy of the first element
inserted into `a`, or `p` if `rg` is empty.

``` cpp
a.insert(p, il)
```

*Effects:* Equivalent to `a.insert(p, il.begin(), il.end())`.

``` cpp
a.erase(q)
```

*Result:* `iterator`.

*Preconditions:* For `vector` and `deque`, `T` is *Cpp17MoveAssignable*.

*Effects:* Erases the element pointed to by `q`.

*Returns:* An iterator that points to the element immediately following
`q` prior to the element being erased. If no such element exists,
`a.end()` is returned.

``` cpp
a.erase(q1, q2)
```

*Result:* `iterator`.

*Preconditions:* For `vector` and `deque`, `T` is *Cpp17MoveAssignable*.

*Effects:* Erases the elements in the range `[q1, q2)`.

*Returns:* An iterator that points to the element pointed to by `q2`
prior to any elements being erased. If no such element exists, `a.end()`
is returned.

``` cpp
a.clear()
```

*Result:* `void`

*Effects:* Destroys all elements in `a`. Invalidates all references,
pointers, and iterators referring to the elements of `a` and may
invalidate the past-the-end iterator.

*Ensures:* `a.empty()` is `true`.

*Complexity:* Linear.

``` cpp
a.assign(i, j)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from `*i`
and assignable from `*i`. For `vector`, if the iterator does not meet
the forward iterator requirements [[forward.iterators]], `T` is also
*Cpp17MoveInsertable* into `X`. Neither `i` nor `j` are iterators into
`a`.

*Effects:* Replaces elements in `a` with a copy of `[i, j)`. Invalidates
all references, pointers and iterators referring to the elements of `a`.
For `vector` and `deque`, also invalidates the past-the-end iterator.
Each iterator in the range \[`i`, `j`) is dereferenced exactly once.

``` cpp
a.assign_range(rg)
```

*Result:* `void`

*Mandates:* `assignable_from<T&, ranges::range_reference_t<R>>` is
modeled.

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`. For `vector`, if `R` models neither
`ranges::sized_range` nor `ranges::forward_range`, `T` is also
*Cpp17MoveInsertable* into `X`. `rg` and `a` do not overlap.

*Effects:* Replaces elements in `a` with a copy of each element in `rg`.
Invalidates all references, pointers, and iterators referring to the
elements of `a`. For `vector` and `deque`, also invalidates the
past-the-end iterator. Each iterator in the range `rg` is dereferenced
exactly once.

``` cpp
a.assign(il)
```

*Effects:* Equivalent to `a.assign(il.begin(), il.end())`.

``` cpp
a.assign(n, t)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X` and
*Cpp17CopyAssignable*. `t` is not a reference into `a`.

*Effects:* Replaces elements in `a` with `n` copies of `t`. Invalidates
all references, pointers and iterators referring to the elements of `a`.
For `vector` and `deque`, also invalidates the past-the-end iterator.

For every sequence container defined in this Clause and in [[strings]]:

- If the constructor
  ``` cpp
  template<class InputIterator>
    X(InputIterator first, InputIterator last,
      const allocator_type& alloc = allocator_type());
  ```

  is called with a type `InputIterator` that does not qualify as an
  input iterator, then the constructor shall not participate in overload
  resolution.
- If the member functions of the forms:
  ``` cpp
  template<class InputIterator>
    return-type F(const_iterator p,
                  InputIterator first, InputIterator last);       // such as insert

  template<class InputIterator>
    return-type F(InputIterator first, InputIterator last);       // such as append, assign

  template<class InputIterator>
    return-type F(const_iterator i1, const_iterator i2,
                  InputIterator first, InputIterator last);       // such as replace
  ```

  are called with a type `InputIterator` that does not qualify as an
  input iterator, then these functions shall not participate in overload
  resolution.
- A deduction guide for a sequence container shall not participate in
  overload resolution if it has an `InputIterator` template parameter
  and a type that does not qualify as an input iterator is deduced for
  that parameter, or if it has an `Allocator` template parameter and a
  type that does not qualify as an allocator is deduced for that
  parameter.

The following operations are provided for some types of sequence
containers but not others. Operations other than `prepend_range` and
`append_range` are implemented so as to take amortized constant time.

``` cpp
a.front()
```

*Result:* `reference; const_reference` for constant `a`.

*Returns:* `*a.begin()`

*Remarks:* Required for `basic_string`, `array`, `deque`,
`forward_list`, `list`, and `vector`.

``` cpp
a.back()
```

*Result:* `reference; const_reference` for constant `a`.

*Effects:* Equivalent to:

``` cpp
auto tmp = a.end();
--tmp;
return *tmp;
```

*Remarks:* Required for `basic_string`, `array`, `deque`, `list`, and
`vector`.

``` cpp
a.emplace_front(args)
```

*Result:* `reference`

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`args`.

*Effects:* Prepends an object of type `T` constructed with
`std::forward<Args>(args)...`.

*Returns:* `a.front()`.

*Remarks:* Required for `deque`, `forward_list`, and `list`.

``` cpp
a.emplace_back(args)
```

*Result:* `reference`

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`args`. For `vector`, `T` is also *Cpp17MoveInsertable* into `X`.

*Effects:* Appends an object of type `T` constructed with
`std::forward<Args>(args)...`.

*Returns:* `a.back()`.

*Remarks:* Required for `deque`, `list`, and `vector`.

``` cpp
a.push_front(t)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X`.

*Effects:* Prepends a copy of `t`.

*Remarks:* Required for `deque`, `forward_list`, and `list`.

``` cpp
a.push_front(rv)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17MoveInsertable* into `X`.

*Effects:* Prepends a copy of `rv`.

*Remarks:* Required for `deque`, `forward_list`, and `list`.

``` cpp
a.prepend_range(rg)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`. For `deque`, `T` is also *Cpp17MoveInsertable*
into `X`, and `T` meets the *Cpp17MoveConstructible*,
*Cpp17MoveAssignable*, and *Cpp17Swappable*[[swappable.requirements]]
requirements.

*Effects:* Inserts copies of elements in `rg` before `begin()`. Each
iterator in the range `rg` is dereferenced exactly once.

[*Note 2*: The order of elements in `rg` is not
reversed. — *end note*]

*Remarks:* Required for `deque`, `forward_list`, and `list`.

``` cpp
a.push_back(t)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17CopyInsertable* into `X`.

*Effects:* Appends a copy of `t`.

*Remarks:* Required for `basic_string`, `deque`, `list`, and `vector`.

``` cpp
a.push_back(rv)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17MoveInsertable* into `X`.

*Effects:* Appends a copy of `rv`.

*Remarks:* Required for `basic_string`, `deque`, `list`, and `vector`.

``` cpp
a.append_range(rg)
```

*Result:* `void`

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`. For `vector`, `T` is also *Cpp17MoveInsertable*
into `X`.

*Effects:* Inserts copies of elements in `rg` before `end()`. Each
iterator in the range `rg` is dereferenced exactly once.

*Remarks:* Required for `deque`, `list`, and `vector`.

``` cpp
a.pop_front()
```

*Result:* `void`

*Preconditions:* `a.empty()` is `false`.

*Effects:* Destroys the first element.

*Remarks:* Required for `deque`, `forward_list`, and `list`.

``` cpp
a.pop_back()
```

*Result:* `void`

*Preconditions:* `a.empty()` is `false`.

*Effects:* Destroys the last element.

*Remarks:* Required for `basic_string`, `deque`, `list`, and `vector`.

``` cpp
a[n]
```

*Result:* `reference; const_reference` for constant `a`

*Returns:* `*(a.begin() + n)`

*Remarks:* Required for `basic_string`, `array`, `deque`, and `vector`.

``` cpp
a.at(n)
```

*Result:* `reference; const_reference` for constant `a`

*Returns:* `*(a.begin() + n)`

*Throws:* `out_of_range` if `n >= a.size()`.

*Remarks:* Required for `basic_string`, `array`, `deque`, and `vector`.

### Node handles <a id="container.node">[[container.node]]</a>

#### Overview <a id="container.node.overview">[[container.node.overview]]</a>

A *node handle* is an object that accepts ownership of a single element
from an associative container [[associative.reqmts]] or an unordered
associative container [[unord.req]]. It may be used to transfer that
ownership to another container with compatible nodes. Containers with
compatible nodes have the same node handle type. Elements may be
transferred in either direction between container types in the same row
of [[container.node.compat]].

**Table: Container types with compatible nodes**

|                                  |                                       |
| -------------------------------- | ------------------------------------- |
| `map<K, T, C1, A>`               | `map<K, T, C2, A>`                    |
| `map<K, T, C1, A>`               | `multimap<K, T, C2, A>`               |
| `set<K, C1, A>`                  | `set<K, C2, A>`                       |
| `set<K, C1, A>`                  | `multiset<K, C2, A>`                  |
| `unordered_map<K, T, H1, E1, A>` | `unordered_map<K, T, H2, E2, A>`      |
| `unordered_map<K, T, H1, E1, A>` | `unordered_multimap<K, T, H2, E2, A>` |
| `unordered_set<K, H1, E1, A>`    | `unordered_set<K, H2, E2, A>`         |
| `unordered_set<K, H1, E1, A>`    | `unordered_multiset<K, H2, E2, A>`    |


If a node handle is not empty, then it contains an allocator that is
equal to the allocator of the container when the element was extracted.
If a node handle is empty, it contains no allocator.

Class *node-handle* is for exposition only.

If a user-defined specialization of `pair` exists for
`pair<const Key, T>` or `pair<Key, T>`, where `Key` is the container’s
`key_type` and `T` is the container’s `mapped_type`, the behavior of
operations involving node handles is undefined.

``` cpp
template<unspecified>
class node-handle {
public:
  // These type declarations are described in [associative.reqmts] and [unord.req].
  using value_type     = see belownc{};     // not present for map containers
  using key_type       = see belownc{};     // not present for set containers
  using mapped_type    = see belownc{};     // not present for set containers
  using allocator_type = see belownc{};

private:
  using container_node_type = unspecified;                  // exposition only
  using ator_traits = allocator_traits<allocator_type>;     // exposition only

  typename ator_traits::template
    rebind_traits<container_node_type>::pointer ptr_;       // exposition only
  optional<allocator_type> alloc_;                          // exposition only

public:
  // [container.node.cons], constructors, copy, and assignment
  constexpr node-handle() noexcept : ptr_(), alloc_() {}
  node-handle(node-handle&&) noexcept;
  node-handle& operator=(node-handle&&);

  // [container.node.dtor], destructor
  ~node-handle();

  // [container.node.observers], observers
  value_type& value() const;            // not present for map containers
  key_type& key() const;                // not present for set containers
  mapped_type& mapped() const;          // not present for set containers

  allocator_type get_allocator() const;
  explicit operator bool() const noexcept;
  [[nodiscard]] bool empty() const noexcept;

  // [container.node.modifiers], modifiers
  void swap(node-handle&)
    noexcept(ator_traits::propagate_on_container_swap::value ||
             ator_traits::is_always_equal::value);

  friend void swap(node-handle& x, node-handle& y) noexcept(noexcept(x.swap(y))) {
    x.swap(y);
  }
};
```

#### Constructors, copy, and assignment <a id="container.node.cons">[[container.node.cons]]</a>

``` cpp
node-handle(node-handle&& nh) noexcept;
```

*Effects:* Constructs a *node-handle* object initializing `ptr_` with
`nh.ptr_`. Move constructs `alloc_` with `nh.alloc_`. Assigns `nullptr`
to `nh.ptr_` and assigns `nullopt` to `nh.alloc_`.

``` cpp
node-handle& operator=(node-handle&& nh);
```

*Preconditions:* Either `!alloc_`, or
`ator_traits::propagate_on_container_move_assignment::value` is `true`,
or `alloc_ == nh.alloc_`.

*Effects:*

- If `ptr_ != nullptr`, destroys the `value_type` subobject in the
  `container_node_type` object pointed to by `ptr_` by calling
  `ator_traits::destroy`, then deallocates `ptr_` by calling
  `ator_traits::template rebind_traits<container_node_type>::deallocate`.
- Assigns `nh.ptr_` to `ptr_`.
- If `!alloc` or
  `ator_traits::propagate_on_container_move_assignment::value` is
  `true`, move assigns `nh.alloc_` to `alloc_`.
- Assigns `nullptr` to `nh.ptr_` and assigns `nullopt` to `nh.alloc_`.

*Returns:* `*this`.

*Throws:* Nothing.

#### Destructor <a id="container.node.dtor">[[container.node.dtor]]</a>

``` cpp
~node-handle();
```

*Effects:* If `ptr_ != nullptr`, destroys the `value_type` subobject in
the `container_node_type` object pointed to by `ptr_` by calling
`ator_traits::destroy`, then deallocates `ptr_` by calling
`ator_traits::template rebind_traits<container_node_type>::deallocate`.

#### Observers <a id="container.node.observers">[[container.node.observers]]</a>

``` cpp
value_type& value() const;
```

*Preconditions:* `empty() == false`.

*Returns:* A reference to the `value_type` subobject in the
`container_node_type` object pointed to by `ptr_`.

*Throws:* Nothing.

``` cpp
key_type& key() const;
```

*Preconditions:* `empty() == false`.

*Returns:* A non-const reference to the `key_type` member of the
`value_type` subobject in the `container_node_type` object pointed to by
`ptr_`.

*Throws:* Nothing.

*Remarks:* Modifying the key through the returned reference is
permitted.

``` cpp
mapped_type& mapped() const;
```

*Preconditions:* `empty() == false`.

*Returns:* A reference to the `mapped_type` member of the `value_type`
subobject in the `container_node_type` object pointed to by `ptr_`.

*Throws:* Nothing.

``` cpp
allocator_type get_allocator() const;
```

*Preconditions:* `empty() == false`.

*Returns:* `*alloc_`.

*Throws:* Nothing.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `ptr_ != nullptr`.

``` cpp
[[nodiscard]] bool empty() const noexcept;
```

*Returns:* `ptr_ == nullptr`.

#### Modifiers <a id="container.node.modifiers">[[container.node.modifiers]]</a>

``` cpp
void swap(node-handle& nh)
  noexcept(ator_traits::propagate_on_container_swap::value ||
           ator_traits::is_always_equal::value);
```

*Preconditions:* `!alloc_`, or `!nh.alloc_`, or
`ator_traits::propagate_on_container_swap::value` is `true`, or
`alloc_ == nh.alloc_`.

*Effects:* Calls `swap(ptr_, nh.ptr_)`. If `!alloc_`, or `!nh.alloc_`,
or `ator_traits::propagate_on_container_swap::value` is `true` calls
`swap(alloc_, nh.alloc_)`.

### Insert return type <a id="container.insert.return">[[container.insert.return]]</a>

The associative containers with unique keys and the unordered containers
with unique keys have a member function `insert` that returns a nested
type `insert_return_type`. That return type is a specialization of the
template specified in this subclause.

``` cpp
template<class Iterator, class NodeType>
struct insert-return-type
{
  Iterator position;
  bool     inserted;
  NodeType node;
};
```

The name *insert-return-type* is exposition only. *insert-return-type*
has the template parameters, data members, and special members specified
above. It has no base classes or members other than those specified.

### Associative containers <a id="associative.reqmts">[[associative.reqmts]]</a>

#### General <a id="associative.reqmts.general">[[associative.reqmts.general]]</a>

Associative containers provide fast retrieval of data based on keys. The
library provides four basic kinds of associative containers: `set`,
`multiset`, `map` and `multimap`. The library also provides container
adaptors that make it easy to construct abstract data types, such as
`flat_map`s, `flat_multimap`s, `flat_set`s, or `flat_multiset`s, out of
the basic sequence container kinds (or out of other program-defined
sequence containers).

Each associative container is parameterized on `Key` and an ordering
relation `Compare` that induces a strict weak ordering [[alg.sorting]]
on elements of `Key`. In addition, `map` and `multimap` associate an
arbitrary *mapped type* `T` with the `Key`. The object of type `Compare`
is called the *comparison object* of a container.

The phrase “equivalence of keys” means the equivalence relation imposed
by the comparison object. That is, two keys `k1` and `k2` are considered
to be equivalent if for the comparison object `comp`,
`comp(k1, k2) == false && comp(k2, k1) == false`.

[*Note 1*: This is not necessarily the same as the result of
`k1 == k2`. — *end note*]

For any two keys `k1` and `k2` in the same container, calling
`comp(k1, k2)` shall always return the same value.

An associative container supports *unique keys* if it may contain at
most one element for each key. Otherwise, it supports *equivalent keys*.
The `set` and `map` classes support unique keys; the `multiset` and
`multimap` classes support equivalent keys. For `multiset` and
`multimap`, `insert`, `emplace`, and `erase` preserve the relative
ordering of equivalent elements.

For `set` and `multiset` the value type is the same as the key type. For
`map` and `multimap` it is equal to `pair<const Key, T>`.

`iterator`

of an associative container is of the bidirectional iterator category.
For associative containers where the value type is the same as the key
type, both `iterator` and `const_iterator` are constant iterators. It is
unspecified whether or not `iterator` and `const_iterator` are the same
type.

[*Note 2*: `iterator` and `const_iterator` have identical semantics in
this case, and `iterator` is convertible to `const_iterator`. Users can
avoid violating the one-definition rule by always using `const_iterator`
in their function parameter lists. — *end note*]

In this subclause,

- `X` denotes an associative container class,
- `a` denotes a value of type `X`,
- `a2` denotes a value of a type with nodes compatible with type `X` (
  [[container.node.compat]]),
- `b` denotes a value or type `X` or `const X`,
- `u` denotes the name of a variable being declared,
- `a_uniq` denotes a value of type `X` when `X` supports unique keys,
- `a_eq` denotes a value of type `X` when `X` supports multiple keys,
- `a_tran` denotes a value of type `X` or `const X` when the
  *qualified-id* `X::key_compare::is_transparent` is valid and denotes a
  type [[temp.deduct]],
- `i` and `j` meet the *Cpp17InputIterator* requirements and refer to
  elements implicitly convertible to `value_type`,
- \[`i`, `j`) denotes a valid range,
- `rg` denotes a value of a type `R` that models
  `container-compatible-range<value_type>`,
- `p` denotes a valid constant iterator to `a`,
- `q` denotes a valid dereferenceable constant iterator to `a`,
- `r` denotes a valid dereferenceable iterator to `a`,
- `[q1, q2)` denotes a valid range of constant iterators in `a`,
- `il` designates an object of type `initializer_list<value_type>`,
- `t` denotes a value of type `X::value_type`,
- `k` denotes a value of type `X::key_type`, and
- `c` denotes a value of type `X::key_compare` or
  `const X::key_compare`;
- `kl` is a value such that `a` is partitioned [[alg.sorting]] with
  respect to `c(x, kl)`, with `x` the key value of `e` and `e` in `a`;
- `ku` is a value such that `a` is partitioned with respect to
  `!c(ku, x)`, with `x` the key value of `e` and `e` in `a`;
- `ke` is a value such that `a` is partitioned with respect to
  `c(x, ke)` and `!c(ke, x)`, with `c(x, ke)` implying `!c(ke, x)` and
  with `x` the key value of `e` and `e` in `a`;
- `kx` is a value such that
  - `a` is partitioned with respect to `c(x, kx)` and `!c(kx, x)`, with
    `c(x, kx)` implying `!c(kx, x)` and with `x` the key value of `e`
    and `e` in `a`, and
  - `kx` is not convertible to either `iterator` or `const_iterator`;
    and
- `A` denotes the storage allocator used by `X`, if any, or
  `allocator<X::value_type>` otherwise,
- `m` denotes an allocator of a type convertible to `A`, and `nh`
  denotes a non-const rvalue of type `X::node_type`.

A type `X` meets the *associative container* requirements if `X` meets
all the requirements of an allocator-aware container
[[container.requirements.general]] and the following types, statements,
and expressions are well-formed and have the specified semantics, except
that for `map` and `multimap`, the requirements placed on `value_type`
in [[container.alloc.reqmts]] apply instead to `key_type` and
`mapped_type`.

[*Note 3*: For example, in some cases `key_type` and `mapped_type` are
required to be *Cpp17CopyAssignable* even though the associated
`value_type`, `pair<const key_type, mapped_type>`, is not
*Cpp17CopyAssignable*. — *end note*]

``` cpp
typename X::key_type
```

*Result:* `Key`.

``` cpp
typename X::mapped_type
```

*Result:* `T`.

*Remarks:* For `map` and `multimap` only.

``` cpp
typename X::value_type
```

*Result:* `Key` for `set` and `multiset` only; `pair<const Key, T>` for
`map` and `multimap` only.

*Preconditions:* `X::value_type` is *Cpp17Erasable* from `X`.

``` cpp
typename X::key_compare
```

*Result:* `Compare`.

*Preconditions:* `key_compare` is *Cpp17CopyConstructible*.

``` cpp
typename X::value_compare
```

*Result:* A binary predicate type. It is the same as `key_compare` for
`set` and `multiset`; is an ordering relation on pairs induced by the
first component (i.e., `Key`) for `map` and `multimap`.

``` cpp
typename X::node_type
```

*Result:* A specialization of the *node-handle* class
template [[container.node]], such that the public nested types are the
same types as the corresponding types in `X`.

``` cpp
X(c)
```

*Effects:* Constructs an empty container. Uses a copy of `c` as a
comparison object.

*Complexity:* Constant.

``` cpp
X u = X();
X u;
```

*Preconditions:* `key_compare` meets the *Cpp17DefaultConstructible*
requirements.

*Effects:* Constructs an empty container. Uses `Compare()` as a
comparison object.

*Complexity:* Constant.

``` cpp
X(i, j, c)
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*i`.

*Effects:* Constructs an empty container and inserts elements from the
range \[`i`, `j`) into it; uses `c` as a comparison object.

*Complexity:* N log N in general, where N has the value
`distance(i, j)`; linear if \[`i`, `j`) is sorted with respect to
`value_comp()`.

``` cpp
X(i, j)
```

*Preconditions:* `key_compare` meets the *Cpp17DefaultConstructible*
requirements. `value_type` is *Cpp17EmplaceConstructible* into `X` from
`*i`.

*Effects:* Constructs an empty container and inserts elements from the
range \[`i`, `j`) into it; uses `Compare()` as a comparison object.

*Complexity:* N log N in general, where N has the value
`distance(i, j)`; linear if \[`i`, `j`) is sorted with respect to
`value_comp()`.

``` cpp
X(from_range, rg, c)
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*ranges::begin(rg)`.

*Effects:* Constructs an empty container and inserts each element from
`rg` into it. Uses `c` as the comparison object.

*Complexity:* N log N in general, where N has the value
`ranges::distance(rg)`; linear if `rg` is sorted with respect to
`value_comp()`.

``` cpp
X(from_range, rg)
```

*Preconditions:* `key_compare` meets the *Cpp17DefaultConstructible*
requirements. `value_type` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`.

*Effects:* Constructs an empty container and inserts each element from
`rg` into it. Uses `Compare()` as the comparison object.

*Complexity:* Same as `X(from_range, rg, c)`.

``` cpp
X(il, c)
```

*Effects:* Equivalent to `X(il.begin(), il.end(), c)`.

``` cpp
X(il)
```

*Effects:* Equivalent to `X(il.begin(), il.end())`.

``` cpp
a = il
```

*Result:* `X&`

*Preconditions:* `value_type` is *Cpp17CopyInsertable* into `X` and
*Cpp17CopyAssignable*.

*Effects:* Assigns the range \[`il.begin()`, `il.end()`) into `a`. All
existing elements of `a` are either assigned to or destroyed.

*Complexity:* N log N in general, where N has the value
`il.size() + a.size()`; linear if \[`il.begin()`, `il.end()`) is sorted
with respect to `value_comp()`.

``` cpp
b.key_comp()
```

*Result:* `X::key_compare`

*Returns:* The comparison object out of which `b` was constructed.

*Complexity:* Constant.

``` cpp
b.value_comp()
```

*Result:* `X::value_compare`

*Returns:* An object of `value_compare` constructed out of the
comparison object.

*Complexity:* Constant.

``` cpp
a_uniq.emplace(args)
```

*Result:* `pair<iterator, bool>`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `args`.

*Effects:* Inserts a `value_type` object `t` constructed with
`std::forward<Args>(args)...` if and only if there is no element in the
container with key equivalent to the key of `t`.

*Returns:* The `bool` component of the returned pair is `true` if and
only if the insertion takes place, and the iterator component of the
pair points to the element with key equivalent to the key of `t`.

*Complexity:* Logarithmic.

``` cpp
a_eq.emplace(args)
```

*Result:* `iterator`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `args`.

*Effects:* Inserts a `value_type` object `t` constructed with
`std::forward<Args>(args)...`. If a range containing elements equivalent
to `t` exists in `a_eq`, `t` is inserted at the end of that range.

*Returns:* An iterator pointing to the newly inserted element.

*Complexity:* Logarithmic.

``` cpp
a.emplace_hint(p, args)
```

*Result:* `iterator`

*Effects:* Equivalent to `a.emplace(std::forward<Args>(args)...)`,
except that the element is inserted as close as possible to the position
just prior to `p`.

*Returns:* An iterator pointing to the element with the key equivalent
to the newly inserted element.

*Complexity:* Logarithmic in general, but amortized constant if the
element is inserted right before `p`.

``` cpp
a_uniq.insert(t)
```

*Result:* `pair<iterator, bool>`

*Preconditions:* If `t` is a non-const rvalue, `value_type` is
*Cpp17MoveInsertable* into `X`; otherwise, `value_type` is
*Cpp17CopyInsertable* into `X`.

*Effects:* Inserts `t` if and only if there is no element in the
container with key equivalent to the key of `t`.

*Returns:* The `bool` component of the returned pair is `true` if and
only if the insertion takes place, and the `iterator` component of the
pair points to the element with key equivalent to the key of `t`.

*Complexity:* Logarithmic.

``` cpp
a_eq.insert(t)
```

*Result:* `iterator`

*Preconditions:* If `t` is a non-const rvalue, `value_type` is
*Cpp17MoveInsertable* into `X`; otherwise, `value_type` is
*Cpp17CopyInsertable* into `X`.

*Effects:* Inserts `t` and returns the iterator pointing to the newly
inserted element. If a range containing elements equivalent to `t`
exists in `a_eq`, `t` is inserted at the end of that range.

*Complexity:* Logarithmic.

``` cpp
a.insert(p, t)
```

*Result:* `iterator`

*Preconditions:* If `t` is a non-const rvalue, `value_type` is
*Cpp17MoveInsertable* into `X`; otherwise, `value_type` is
*Cpp17CopyInsertable* into `X`.

*Effects:* Inserts `t` if and only if there is no element with key
equivalent to the key of `t` in containers with unique keys; always
inserts `t` in containers with equivalent keys. `t` is inserted as close
as possible to the position just prior to `p`.

*Returns:* An iterator pointing to the element with key equivalent to
the key of `t`.

*Complexity:* Logarithmic in general, but amortized constant if `t` is
inserted right before `p`.

``` cpp
a.insert(i, j)
```

*Result:* `void`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*i`. Neither `i` nor `j` are iterators into `a`.

*Effects:* Inserts each element from the range \[`i`, `j`) if and only
if there is no element with key equivalent to the key of that element in
containers with unique keys; always inserts that element in containers
with equivalent keys.

*Complexity:* N log (`a.size()` + N), where N has the value
`distance(i, j)`.

``` cpp
a.insert_range(rg)
```

*Result:* `void`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*ranges::begin(rg)`. `rg` and `a` do not overlap.

*Effects:* Inserts each element from `rg` if and only if there is no
element with key equivalent to the key of that element in containers
with unique keys; always inserts that element in containers with
equivalent keys.

*Complexity:* N log (`a.size()` + N), where N has the value
`ranges::distance(rg)`.

``` cpp
a.insert(il)
```

*Effects:* Equivalent to `a.insert(il.begin(), il.end())`.

``` cpp
a_uniq.insert(nh)
```

*Result:* `insert_return_type`

*Preconditions:* `nh` is empty or
`a_uniq.get_allocator() == nh.get_allocator()` is `true`.

*Effects:* If `nh` is empty, has no effect. Otherwise, inserts the
element owned by `nh` if and only if there is no element in the
container with a key equivalent to `nh.key()`.

*Returns:* If `nh` is empty, `inserted` is `false`, `position` is
`end()`, and `node` is empty. Otherwise if the insertion took place,
`inserted` is `true`, `position` points to the inserted element, and
`node` is empty; if the insertion failed, `inserted` is `false`, `node`
has the previous value of `nh`, and `position` points to an element with
a key equivalent to `nh.key()`.

*Complexity:* Logarithmic.

``` cpp
a_eq.insert(nh)
```

*Result:* `iterator`

*Preconditions:* `nh` is empty or
`a_eq.get_allocator() == nh.get_allocator()` is `true`.

*Effects:* If `nh` is empty, has no effect and returns `a_eq.end()`.
Otherwise, inserts the element owned by `nh` and returns an iterator
pointing to the newly inserted element. If a range containing elements
with keys equivalent to `nh.key()` exists in `a_eq`, the element is
inserted at the end of that range.

*Ensures:* `nh` is empty.

*Complexity:* Logarithmic.

``` cpp
a.insert(p, nh)
```

*Result:* `iterator`

*Preconditions:* `nh` is empty or
`a.get_allocator() == nh.get_allocator()` is `true`.

*Effects:* If `nh` is empty, has no effect and returns `a.end()`.
Otherwise, inserts the element owned by `nh` if and only if there is no
element with key equivalent to `nh.key()` in containers with unique
keys; always inserts the element owned by `nh` in containers with
equivalent keys. The element is inserted as close as possible to the
position just prior to `p`.

*Ensures:* `nh` is empty if insertion succeeds, unchanged if insertion
fails.

*Returns:* An iterator pointing to the element with key equivalent to
`nh.key()`.

*Complexity:* Logarithmic in general, but amortized constant if the
element is inserted right before `p`.

``` cpp
a.extract(k)
```

*Result:* `node_type`

*Effects:* Removes the first element in the container with key
equivalent to `k`.

*Returns:* A `node_type` owning the element if found, otherwise an empty
`node_type`.

*Complexity:* log (`a.size()`)

``` cpp
a_tran.extract(kx)
```

*Result:* `node_type`

*Effects:* Removes the first element in the container with key `r` such
that `!c(r, kx) && !c(kx, r)` is `true`.

*Returns:* A `node_type` owning the element if found, otherwise an empty
`node_type`.

*Complexity:* log(`a_tran.size()`)

``` cpp
a.extract(q)
```

*Result:* `node_type`

*Effects:* Removes the element pointed to by `q`.

*Returns:* A `node_type` owning that element.

*Complexity:* Amortized constant.

``` cpp
a.merge(a2)
```

*Result:* `void`

*Preconditions:* `a.get_allocator() == a2.get_allocator()`.

*Effects:* Attempts to extract each element in `a2` and insert it into
`a` using the comparison object of `a`. In containers with unique keys,
if there is an element in `a` with key equivalent to the key of an
element from `a2`, then that element is not extracted from `a2`.

*Ensures:* Pointers and references to the transferred elements of `a2`
refer to those same elements but as members of `a`. Iterators referring
to the transferred elements will continue to refer to their elements,
but they now behave as iterators into `a`, not into `a2`.

*Throws:* Nothing unless the comparison object throws.

*Complexity:* N log(`a.size()+` N), where N has the value `a2.size()`.

``` cpp
a.erase(k)
```

*Result:* `size_type`

*Effects:* Erases all elements in the container with key equivalent to
`k`.

*Returns:* The number of erased elements.

*Complexity:* log (`a.size()`) + `a.count(k)`

``` cpp
a_tran.erase(kx)
```

*Result:* `size_type`

*Effects:* Erases all elements in the container with key `r` such that
`!c(r, kx) && !c(kx, r)` is `true`.

*Returns:* The number of erased elements.

*Complexity:* log(`a_tran.size())` + `a_tran.count(kx)`

``` cpp
a.erase(q)
```

*Result:* `iterator`

*Effects:* Erases the element pointed to by `q`.

*Returns:* An iterator pointing to the element immediately following `q`
prior to the element being erased. If no such element exists, returns
`a.end()`.

*Complexity:* Amortized constant.

``` cpp
a.erase(r)
```

*Result:* `iterator`

*Effects:* Erases the element pointed to by `r`.

*Returns:* An iterator pointing to the element immediately following `r`
prior to the element being erased. If no such element exists, returns
`a.end()`.

*Complexity:* Amortized constant.

``` cpp
a.erase(q1, q2)
```

*Result:* `iterator`

*Effects:* Erases all the elements in the range \[`q1`, `q2`).

*Returns:* An iterator pointing to the element pointed to by `q2` prior
to any elements being erased. If no such element exists, `a.end()` is
returned.

*Complexity:* log(`a.size()`) + N, where N has the value
`distance(q1, q2)`.

``` cpp
a.clear()
```

*Effects:* Equivalent to `a.erase(a.begin(), a.end())`.

*Ensures:* `a.empty()` is `true`.

*Complexity:* Linear in `a.size()`.

``` cpp
b.find(k)
```

*Result:* `iterator`; `const_iterator` for constant `b`.

*Returns:* An iterator pointing to an element with the key equivalent to
`k`, or `b.end()` if such an element is not found.

*Complexity:* Logarithmic.

``` cpp
a_tran.find(ke)
```

*Result:* `iterator`; `const_iterator` for constant `a_tran`.

*Returns:* An iterator pointing to an element with key `r` such that
`!c(r, ke) && !c(ke, r)` is `true`, or `a_tran.end()` if such an element
is not found.

*Complexity:* Logarithmic.

``` cpp
b.count(k)
```

*Result:* `size_type`

*Returns:* The number of elements with key equivalent to `k`.

*Complexity:* log (`b.size()`) + `b.count(k)`

``` cpp
a_tran.count(ke)
```

*Result:* `size_type`

*Returns:* The number of elements with key `r` such that
`!c(r, ke) && !c(ke, r)`.

*Complexity:* log (`a_tran.size()`) + `a_tran.count(ke)`

``` cpp
b.contains(k)
```

*Result:* `bool`

*Effects:* Equivalent to: `return b.find(k) != b.end();`

``` cpp
a_tran.contains(ke)
```

*Result:* `bool`

*Effects:* Equivalent to: `return a_tran.find(ke) != a_tran.end();`

``` cpp
b.lower_bound(k)
```

*Result:* `iterator`; `const_iterator` for constant `b`.

*Returns:* An iterator pointing to the first element with key not less
than `k`, or `b.end()` if such an element is not found.

*Complexity:* Logarithmic.

``` cpp
a_tran.lower_bound(kl)
```

*Result:* `iterator`; `const_iterator` for constant `a_tran`.

*Returns:* An iterator pointing to the first element with key `r` such
that `!c(r, kl)`, or `a_tran.end()` if such an element is not found.

*Complexity:* Logarithmic.

``` cpp
b.upper_bound(k)
```

*Result:* `iterator`; `const_iterator` for constant `b`.

*Returns:* An iterator pointing to the first element with key greater
than `k`, or `b.end()` if such an element is not found.

*Complexity:* Logarithmic,

``` cpp
a_tran.upper_bound(ku)
```

*Result:* `iterator`; `const_iterator` for constant `a_tran`.

*Returns:* An iterator pointing to the first element with key `r` such
that `c(ku, r)`, or `a_tran.end()` if such an element is not found.

*Complexity:* Logarithmic.

``` cpp
b.equal_range(k)
```

*Result:* `pair<iterator, iterator>`;
`pair<const_iterator, const_iterator>` for constant `b`.

*Effects:* Equivalent to:
`return make_pair(b.lower_bound(k), b.upper_bound(k));`

*Complexity:* Logarithmic.

``` cpp
a_tran.equal_range(ke)
```

*Result:* `pair<iterator, iterator>`;
`pair<const_iterator, const_iterator>` for constant `a_tran`.

*Effects:* Equivalent to:
`return make_pair(a_tran.lower_bound(ke), a_tran.upper_bound(ke));`

*Complexity:* Logarithmic.

The `insert`, `insert_range`, and `emplace` members shall not affect the
validity of iterators and references to the container, and the `erase`
members shall invalidate only iterators and references to the erased
elements.

The `extract` members invalidate only iterators to the removed element;
pointers and references to the removed element remain valid. However,
accessing the element through such pointers and references while the
element is owned by a `node_type` is undefined behavior. References and
pointers to an element obtained while it is owned by a `node_type` are
invalidated if the element is successfully inserted.

The fundamental property of iterators of associative containers is that
they iterate through the containers in the non-descending order of keys
where non-descending is defined by the comparison that was used to
construct them. For any two dereferenceable iterators `i` and `j` such
that distance from `i` to `j` is positive, the following condition
holds:

``` cpp
value_comp(*j, *i) == false
```

For associative containers with unique keys the stronger condition
holds:

``` cpp
value_comp(*i, *j) != false
```

When an associative container is constructed by passing a comparison
object the container shall not store a pointer or reference to the
passed object, even if that object is passed by reference. When an
associative container is copied, through either a copy constructor or an
assignment operator, the target container shall then use the comparison
object from the container being copied, as if that comparison object had
been passed to the target container in its constructor.

The member function templates `find`, `count`, `contains`,
`lower_bound`, `upper_bound`, `equal_range`, `erase`, and `extract`
shall not participate in overload resolution unless the *qualified-id*
`Compare::is_transparent` is valid and denotes a type [[temp.deduct]].
Additionally, the member function templates `extract` and `erase` shall
not participate in overload resolution if
`is_convertible_v<K&&, iterator> || is_convertible_v<K&&, const_iterator>`
is `true`, where `K` is the type substituted as the first template
argument.

A deduction guide for an associative container shall not participate in
overload resolution if any of the following are true:

- It has an `InputIterator` template parameter and a type that does not
  qualify as an input iterator is deduced for that parameter.
- It has an `Allocator` template parameter and a type that does not
  qualify as an allocator is deduced for that parameter.
- It has a `Compare` template parameter and a type that qualifies as an
  allocator is deduced for that parameter.

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

#### General <a id="unord.req.general">[[unord.req.general]]</a>

Unordered associative containers provide an ability for fast retrieval
of data based on keys. The worst-case complexity for most operations is
linear, but the average case is much faster. The library provides four
unordered associative containers: `unordered_set`, `unordered_map`,
`unordered_multiset`, and `unordered_multimap`.

Unordered associative containers conform to the requirements for
Containers [[container.requirements]], except that the expressions
`a == b` and `a != b` have different semantics than for the other
container types.

Each unordered associative container is parameterized by `Key`, by a
function object type `Hash` that meets the *Cpp17Hash* requirements
[[hash.requirements]] and acts as a hash function for argument values of
type `Key`, and by a binary predicate `Pred` that induces an equivalence
relation on values of type `Key`. Additionally, `unordered_map` and
`unordered_multimap` associate an arbitrary *mapped type* `T` with the
`Key`.

The container’s object of type `Hash` — denoted by `hash` — is called
the *hash function* of the container. The container’s object of type
`Pred` — denoted by `pred` — is called the *key equality predicate* of
the container.

Two values `k1` and `k2` are considered equivalent if the container’s
key equality predicate `pred(k1, k2)` is valid and returns `true` when
passed those values. If `k1` and `k2` are equivalent, the container’s
hash function shall return the same value for both.

[*Note 1*: Thus, when an unordered associative container is
instantiated with a non-default `Pred` parameter it usually needs a
non-default `Hash` parameter as well. — *end note*]

For any two keys `k1` and `k2` in the same container, calling
`pred(k1, k2)` shall always return the same value. For any key `k` in a
container, calling `hash(k)` shall always return the same value.

An unordered associative container supports *unique keys* if it may
contain at most one element for each key. Otherwise, it supports
*equivalent keys*. `unordered_set` and `unordered_map` support unique
keys. `unordered_multiset` and `unordered_multimap` support equivalent
keys. In containers that support equivalent keys, elements with
equivalent keys are adjacent to each other in the iteration order of the
container. Thus, although the absolute order of elements in an unordered
container is not specified, its elements are grouped into
*equivalent-key groups* such that all elements of each group have
equivalent keys. Mutating operations on unordered containers shall
preserve the relative order of elements within each equivalent-key group
unless otherwise specified.

For `unordered_set` and `unordered_multiset` the value type is the same
as the key type. For `unordered_map` and `unordered_multimap` it is
`pair<const Key,
T>`.

For unordered containers where the value type is the same as the key
type, both `iterator` and `const_iterator` are constant iterators. It is
unspecified whether or not `iterator` and `const_iterator` are the same
type.

[*Note 2*: `iterator` and `const_iterator` have identical semantics in
this case, and `iterator` is convertible to `const_iterator`. Users can
avoid violating the one-definition rule by always using `const_iterator`
in their function parameter lists. — *end note*]

The elements of an unordered associative container are organized into
*buckets*. Keys with the same hash code appear in the same bucket. The
number of buckets is automatically increased as elements are added to an
unordered associative container, so that the average number of elements
per bucket is kept below a bound. Rehashing invalidates iterators,
changes ordering between elements, and changes which buckets elements
appear in, but does not invalidate pointers or references to elements.
For `unordered_multiset` and `unordered_multimap`, rehashing preserves
the relative ordering of equivalent elements.

In this subclause,

- `X` denotes an unordered associative container class,
- `a` denotes a value of type `X`,
- `a2` denotes a value of a type with nodes compatible with type `X` (
  [[container.node.compat]]),
- `b` denotes a value of type `X` or `const X`,
- `a_uniq` denotes a value of type `X` when `X` supports unique keys,
- `a_eq` denotes a value of type `X` when `X` supports equivalent keys,
- `a_tran` denotes a value of type `X` or `const X` when the
  *qualified-id*s `X::key_equal::is_transparent` and
  `X::hasher::is_transparent` are both valid and denote types
  [[temp.deduct]],
- `i` and `j` denote input iterators that refer to `value_type`,
- `[i, j)` denotes a valid range,
- `rg` denotes a value of a type `R` that models
  `container-compatible-range<value_type>`,
- `p` and `q2` denote valid constant iterators to `a`,
- `q` and `q1` denote valid dereferenceable constant iterators to `a`,
- `r` denotes a valid dereferenceable iterator to `a`,
- `[q1, q2)` denotes a valid range in `a`,
- `il` denotes a value of type `initializer_list<value_type>`,
- `t` denotes a value of type `X::value_type`,
- `k` denotes a value of type `key_type`,
- `hf` denotes a value of type `hasher` or `const hasher`,
- `eq` denotes a value of type `key_equal` or `const key_equal`,
- `ke` is a value such that
  - `eq(r1, ke) == eq(ke, r1)`,
  - `hf(r1) == hf(ke)` if `eq(r1, ke)` is `true`, and
  - if any two of `eq(r1, ke)`, `eq(r2, ke)`, and `eq(r1, r2)` are
    `true`, then all three are `true`,

  where `r1` and `r2` are keys of elements in `a_tran`,
- `kx` is a value such that
  - `eq(r1, kx) == eq(kx, r1)`,
  - `hf(r1) == hf(kx)` if `eq(r1, kx)` is `true`,
  - if any two of `eq(r1, kx)`, `eq(r2, kx)`, and `eq(r1, r2)` are
    `true`, then all three are `true`, and
  - `kx` is not convertible to either `iterator` or `const_iterator`,

  where `r1` and `r2` are keys of elements in `a_tran`,
- `n` denotes a value of type `size_type`,
- `z` denotes a value of type `float`, and
- `nh` denotes an rvalue of type `X::node_type`.

A type `X` meets the *unordered associative container* requirements if
`X` meets all the requirements of an allocator-aware container
[[container.requirements.general]] and the following types, statements,
and expressions are well-formed and have the specified semantics, except
that for `unordered_map` and `unordered_multimap`, the requirements
placed on `value_type` in [[container.alloc.reqmts]] apply instead to
`key_type` and `mapped_type`.

[*Note 3*: For example, `key_type` and `mapped_type` are sometimes
required to be *Cpp17CopyAssignable* even though the associated
`value_type`, `pair<const key_type, mapped_type>`, is not
*Cpp17CopyAssignable*. — *end note*]

``` cpp
typename X::key_type
```

*Result:* `Key`.

``` cpp
typename X::mapped_type
```

*Result:* `T`.

*Remarks:* For `unordered_map` and `unordered_multimap` only.

``` cpp
typename X::value_type
```

*Result:* `Key` for `unordered_set` and `unordered_multiset` only;
`pair<const Key, T>` for `unordered_map` and `unordered_multimap` only.

*Preconditions:* `value_type` is *Cpp17Erasable* from `X`.

``` cpp
typename X::hasher
```

*Result:* `Hash`.

*Preconditions:* `Hash` is a unary function object type such that the
expression `hf(k)` has type `size_t`.

``` cpp
typename X::key_equal
```

*Result:* `Pred`.

*Preconditions:* `Pred` meets the *Cpp17CopyConstructible* requirements.
`Pred` is a binary predicate that takes two arguments of type `Key`.
`Pred` is an equivalence relation.

``` cpp
typename X::local_iterator
```

*Result:* An iterator type whose category, value type, difference type,
and pointer and reference types are the same as `X::iterator`’s.

[*Note 1*: A `local_iterator` object can be used to iterate through a
single bucket, but cannot be used to iterate across
buckets. — *end note*]

``` cpp
typename X::const_local_iterator
```

*Result:* An iterator type whose category, value type, difference type,
and pointer and reference types are the same as `X::const_iterator`’s.

[*Note 2*: A `const_local_iterator` object can be used to iterate
through a single bucket, but cannot be used to iterate across
buckets. — *end note*]

``` cpp
typename X::node_type
```

*Result:* A specialization of a *node-handle* class
template [[container.node]], such that the public nested types are the
same types as the corresponding types in `X`.

``` cpp
X(n, hf, eq)
```

*Effects:* Constructs an empty container with at least `n` buckets,
using `hf` as the hash function and `eq` as the key equality predicate.

*Complexity:* 𝑂(`n`)

``` cpp
X(n, hf)
```

*Preconditions:* `key_equal` meets the *Cpp17DefaultConstructible*
requirements.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hf` as the hash function and `key_equal()` as the key equality
predicate.

*Complexity:* 𝑂(`n`)

``` cpp
X(n)
```

*Preconditions:* `hasher` and `key_equal` meet the
*Cpp17DefaultConstructible* requirements.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hasher()` as the hash function and `key_equal()` as the key
equality predicate.

*Complexity:* 𝑂(`n`)

``` cpp
X a = X();
X a;
```

*Preconditions:* `hasher` and `key_equal` meet the
*Cpp17DefaultConstructible* requirements.

*Effects:* Constructs an empty container with an unspecified number of
buckets, using `hasher()` as the hash function and `key_equal()` as the
key equality predicate.

*Complexity:* Constant.

``` cpp
X(i, j, n, hf, eq)
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*i`.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hf` as the hash function and `eq` as the key equality predicate,
and inserts elements from \[`i`, `j`) into it.

*Complexity:* Average case 𝑂(N) (N is `distance(i, j)`), worst case
𝑂(N^2).

``` cpp
X(i, j, n, hf)
```

*Preconditions:* `key_equal` meets the *Cpp17DefaultConstructible*
requirements. `value_type` is *Cpp17EmplaceConstructible* into `X` from
`*i`.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hf` as the hash function and `key_equal()` as the key equality
predicate, and inserts elements from \[`i`, `j`) into it.

*Complexity:* Average case 𝑂(N) (N is `distance(i, j)`), worst case
𝑂(N^2).

``` cpp
X(i, j, n)
```

*Preconditions:* `hasher` and `key_equal` meet the
*Cpp17DefaultConstructible* requirements. `value_type` is
*Cpp17EmplaceConstructible* into `X` from `*i`.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hasher()` as the hash function and `key_equal()` as the key
equality predicate, and inserts elements from \[`i`, `j`) into it.

*Complexity:* Average case 𝑂(N) (N is `distance(i, j)`), worst case
𝑂(N^2).

``` cpp
X(i, j)
```

*Preconditions:* `hasher` and `key_equal` meet the
*Cpp17DefaultConstructible* requirements. `value_type` is
*Cpp17EmplaceConstructible* into `X` from `*i`.

*Effects:* Constructs an empty container with an unspecified number of
buckets, using `hasher()` as the hash function and `key_equal()` as the
key equality predicate, and inserts elements from \[`i`, `j`) into it.

*Complexity:* Average case 𝑂(N) (N is `distance(i, j)`), worst case
𝑂(N^2).

``` cpp
X(from_range, rg, n, hf, eq)
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*ranges::begin(rg)`.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hf` as the hash function and `eq` as the key equality predicate,
and inserts elements from `rg` into it.

*Complexity:* Average case 𝑂(N) (N is `ranges::distance(rg)`), worst
case 𝑂(N^2).

``` cpp
X(from_range, rg, n, hf)
```

*Preconditions:* `key_equal` meets the *Cpp17DefaultConstructible*
requirements. `value_type` is *Cpp17EmplaceConstructible* into `X` from
`*ranges::begin(rg)`.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hf` as the hash function and `key_equal()` as the key equality
predicate, and inserts elements from `rg` into it.

*Complexity:* Average case 𝑂(N) (N is `ranges::distance(rg)`), worst
case 𝑂(N^2).

``` cpp
X(from_range, rg, n)
```

*Preconditions:* `hasher` and `key_equal` meet the
*Cpp17DefaultConstructible* requirements. `value_type` is
*Cpp17EmplaceConstructible* into `X` from `*ranges::begin(rg)`.

*Effects:* Constructs an empty container with at least `n` buckets,
using `hasher()` as the hash function and `key_equal()` as the key
equality predicate, and inserts elements from `rg` into it.

*Complexity:* Average case 𝑂(N) (N is `ranges::distance(rg)`), worst
case 𝑂(N^2).

``` cpp
X(from_range, rg)
```

*Preconditions:* `hasher` and `key_equal` meet the
*Cpp17DefaultConstructible* requirements. `value_type` is
*Cpp17EmplaceConstructible* into `X` from `*ranges::begin(rg)`.

*Effects:* Constructs an empty container with an unspecified number of
buckets, using `hasher()` as the hash function and `key_equal()` as the
key equality predicate, and inserts elements from `rg` into it.

*Complexity:* Average case 𝑂(N) (N is `ranges::distance(rg)`), worst
case 𝑂(N^2).

``` cpp
X(il)
```

*Effects:* Equivalent to `X(il.begin(), il.end())`.

``` cpp
X(il, n)
```

*Effects:* Equivalent to `X(il.begin(), il.end(), n)`.

``` cpp
X(il, n, hf)
```

*Effects:* Equivalent to `X(il.begin(), il.end(), n, hf)`.

``` cpp
X(il, n, hf, eq)
```

*Effects:* Equivalent to `X(il.begin(), il.end(), n, hf, eq)`.

``` cpp
X(b)
```

*Effects:* In addition to the container
requirements [[container.requirements.general]], copies the hash
function, predicate, and maximum load factor.

*Complexity:* Average case linear in `b.size()`, worst case quadratic.

``` cpp
a = b
```

*Result:* `X&`

*Effects:* In addition to the container requirements, copies the hash
function, predicate, and maximum load factor.

*Complexity:* Average case linear in `b.size()`, worst case quadratic.

``` cpp
a = il
```

*Result:* `X&`

*Preconditions:* `value_type` is *Cpp17CopyInsertable* into `X` and
*Cpp17CopyAssignable*.

*Effects:* Assigns the range \[`il.begin()`, `il.end()`) into `a`. All
existing elements of `a` are either assigned to or destroyed.

*Complexity:* Average case linear in `il.size()`, worst case quadratic.

``` cpp
b.hash_function()
```

*Result:* `hasher`

*Returns:* `b`’s hash function.

*Complexity:* Constant.

``` cpp
b.key_eq()
```

*Result:* `key_equal`

*Returns:* `b`’s key equality predicate.

*Complexity:* Constant.

``` cpp
a_uniq.emplace(args)
```

*Result:* `pair<iterator,` `bool>`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `args`.

*Effects:* Inserts a `value_type` object `t` constructed with
`std::forward<Args>(args)...` if and only if there is no element in the
container with key equivalent to the key of `t`.

*Returns:* The `bool` component of the returned pair is `true` if and
only if the insertion takes place, and the iterator component of the
pair points to the element with key equivalent to the key of `t`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_uniq.size()`).

``` cpp
a_eq.emplace(args)
```

*Result:* `iterator`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `args`.

*Effects:* Inserts a `value_type` object `t` constructed with
`std::forward<Args>(args)...`.

*Returns:* An iterator pointing to the newly inserted element.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_eq.size()`).

``` cpp
a.emplace_hint(p, args)
```

*Result:* `iterator`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `args`.

*Effects:* Equivalent to `a.emplace(std::forward<Args>(args)...)`.

*Returns:* An iterator pointing to the element with the key equivalent
to the newly inserted element. The `const_iterator` `p` is a hint
pointing to where the search should start. Implementations are permitted
to ignore the hint.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a_uniq.insert(t)
```

*Result:* `pair<iterator, bool>`

*Preconditions:* If `t` is a non-const rvalue, `value_type` is
*Cpp17MoveInsertable* into `X`; otherwise, `value_type` is
*Cpp17CopyInsertable* into `X`.

*Effects:* Inserts `t` if and only if there is no element in the
container with key equivalent to the key of `t`.

*Returns:* The `bool` component of the returned pair indicates whether
the insertion takes place, and the `iterator` component points to the
element with key equivalent to the key of `t`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_uniq.size()`).

``` cpp
a_eq.insert(t)
```

*Result:* `iterator`

*Preconditions:* If `t` is a non-const rvalue, `value_type` is
*Cpp17MoveInsertable* into `X`; otherwise, `value_type` is
*Cpp17CopyInsertable* into `X`.

*Effects:* Inserts `t`.

*Returns:* An iterator pointing to the newly inserted element.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_eq.size()`).

``` cpp
a.insert(p, t)
```

*Result:* `iterator`

*Preconditions:* If `t` is a non-const rvalue, `value_type` is
*Cpp17MoveInsertable* into `X`; otherwise, `value_type` is
*Cpp17CopyInsertable* into `X`.

*Effects:* Equivalent to `a.insert(t)`. The iterator `p` is a hint
pointing to where the search should start. Implementations are permitted
to ignore the hint.

*Returns:* An iterator pointing to the element with the key equivalent
to that of `t`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a.insert(i, j)
```

*Result:* `void`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*i`. Neither `i` nor `j` are iterators into `a`.

*Effects:* Equivalent to `a.insert(t)` for each element in `[i,j)`.

*Complexity:* Average case 𝑂(N), where N is `distance(i, j)`, worst case
𝑂(N(`a.size()` + 1)).

``` cpp
a.insert_range(rg)
```

*Result:* `void`

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `X`
from `*ranges::begin(rg)`. `rg` and `a` do not overlap.

*Effects:* Equivalent to `a.insert(t)` for each element `t` in `rg`.

*Complexity:* Average case 𝑂(N), where N is `ranges::distance(rg)`,
worst case 𝑂(N(`a.size()` + 1)).

``` cpp
a.insert(il)
```

*Effects:* Equivalent to `a.insert(il.begin(), il.end())`.

``` cpp
a_uniq.insert(nh)
```

*Result:* `insert_return_type`

*Preconditions:* `nh` is empty or
`a_uniq.get_allocator() == nh.get_allocator()` is `true`.

*Effects:* If `nh` is empty, has no effect. Otherwise, inserts the
element owned by `nh` if and only if there is no element in the
container with a key equivalent to `nh.key()`.

*Ensures:* If `nh` is empty, `inserted` is `false`, `position` is
`end()`, and `node` is empty. Otherwise if the insertion took place,
`inserted` is `true`, `position` points to the inserted element, and
`node` is empty; if the insertion failed, `inserted` is `false`, `node`
has the previous value of `nh`, and `position` points to an element with
a key equivalent to `nh.key()`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_uniq.size()`).

``` cpp
a_eq.insert(nh)
```

*Result:* `iterator`

*Preconditions:* `nh` is empty or
`a_eq.get_allocator() == nh.get_allocator()` is `true`.

*Effects:* If `nh` is empty, has no effect and returns `a_eq.end()`.
Otherwise, inserts the element owned by `nh` and returns an iterator
pointing to the newly inserted element.

*Ensures:* `nh` is empty.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_eq.size()`).

``` cpp
a.insert(q, nh)
```

*Result:* `iterator`

*Preconditions:* `nh` is empty or
`a.get_allocator() == nh.get_allocator()` is `true`.

*Effects:* If `nh` is empty, has no effect and returns `a.end()`.
Otherwise, inserts the element owned by `nh` if and only if there is no
element with key equivalent to `nh.key()` in containers with unique
keys; always inserts the element owned by `nh` in containers with
equivalent keys. The iterator `q` is a hint pointing to where the search
should start. Implementations are permitted to ignore the hint.

*Ensures:* `nh` is empty if insertion succeeds, unchanged if insertion
fails.

*Returns:* An iterator pointing to the element with key equivalent to
`nh.key()`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a.extract(k)
```

*Result:* `node_type`

*Effects:* Removes an element in the container with key equivalent to
`k`.

*Returns:* A `node_type` owning the element if found, otherwise an empty
`node_type`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a_tran.extract(kx)
```

*Result:* `node_type`

*Effects:* Removes an element in the container with key equivalent to
`kx`.

*Returns:* A `node_type` owning the element if found, otherwise an empty
`node_type`.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_tran.size()`).

``` cpp
a.extract(q)
```

*Result:* `node_type`

*Effects:* Removes the element pointed to by `q`.

*Returns:* A `node_type` owning that element.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a.merge(a2)
```

*Result:* `void`

*Preconditions:* `a.get_allocator() == a2.get_allocator()`.

*Effects:* Attempts to extract each element in `a2` and insert it into
`a` using the hash function and key equality predicate of `a`. In
containers with unique keys, if there is an element in `a` with key
equivalent to the key of an element from `a2`, then that element is not
extracted from `a2`.

*Ensures:* Pointers and references to the transferred elements of `a2`
refer to those same elements but as members of `a`. Iterators referring
to the transferred elements and all iterators referring to `a` will be
invalidated, but iterators to elements remaining in `a2` will remain
valid.

*Complexity:* Average case 𝑂(N), where N is `a2.size()`, worst case
𝑂(N`*a.size() + N`).

``` cpp
a.erase(k)
```

*Result:* `size_type`

*Effects:* Erases all elements with key equivalent to `k`.

*Returns:* The number of elements erased.

*Complexity:* Average case 𝑂(`a.count(k)`), worst case 𝑂(`a.size()`).

``` cpp
a_tran.erase(kx)
```

*Result:* `size_type`

*Effects:* Erases all elements with key equivalent to `kx`.

*Returns:* The number of elements erased.

*Complexity:* Average case 𝑂(`a_tran.count(kx)`), worst case
𝑂(`a_tran.size()`).

``` cpp
a.erase(q)
```

*Result:* `iterator`

*Effects:* Erases the element pointed to by `q`.

*Returns:* The iterator immediately following `q` prior to the erasure.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a.erase(r)
```

*Result:* `iterator`

*Effects:* Erases the element pointed to by `r`.

*Returns:* The iterator immediately following `r` prior to the erasure.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a.size()`).

``` cpp
a.erase(q1, q2)
```

*Result:* `iterator`

*Effects:* Erases all elements in the range `[q1, q2)`.

*Returns:* The iterator immediately following the erased elements prior
to the erasure.

*Complexity:* Average case linear in `distance(q1, q2)`, worst case
𝑂(`a.size()`).

``` cpp
a.clear()
```

*Result:* `void`

*Effects:* Erases all elements in the container.

*Ensures:* `a.empty()` is `true`.

*Complexity:* Linear in `a.size()`.

``` cpp
b.find(k)
```

*Result:* `iterator`; `const_iterator` for constant `b`.

*Returns:* An iterator pointing to an element with key equivalent to
`k`, or `b.end()` if no such element exists.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`b.size()`).

``` cpp
a_tran.find(ke)
```

*Result:* `iterator`; `const_iterator` for constant `a_tran`.

*Returns:* An iterator pointing to an element with key equivalent to
`ke`, or `a_tran.end()` if no such element exists.

*Complexity:* Average case 𝑂(1), worst case 𝑂(`a_tran.size()`).

``` cpp
b.count(k)
```

*Result:* `size_type`

*Returns:* The number of elements with key equivalent to `k`.

*Complexity:* Average case 𝑂(`b.count(k)`), worst case 𝑂(`b.size()`).

``` cpp
a_tran.count(ke)
```

*Result:* `size_type`

*Returns:* The number of elements with key equivalent to `ke`.

*Complexity:* Average case 𝑂(`a_tran.count(ke)`), worst case
𝑂(`a_tran.size()`).

``` cpp
b.contains(k)
```

*Effects:* Equivalent to `b.find(k) != b.end()`.

``` cpp
a_tran.contains(ke)
```

*Effects:* Equivalent to `a_tran.find(ke) != a_tran.end()`.

``` cpp
b.equal_range(k)
```

*Result:* `pair<iterator, iterator>`;
`pair<const_iterator, const_iterator>` for constant `b`.

*Returns:* A range containing all elements with keys equivalent to `k`.
Returns `make_pair(b.end(), b.end())` if no such elements exist.

*Complexity:* Average case 𝑂(`b.count(k)`), worst case 𝑂(`b.size()`).

``` cpp
a_tran.equal_range(ke)
```

*Result:* `pair<iterator, iterator>`;
`pair<const_iterator, const_iterator>` for constant `a_tran`.

*Returns:* A range containing all elements with keys equivalent to `ke`.
Returns `make_pair(a_tran.end(), a_tran.end())` if no such elements
exist.

*Complexity:* Average case 𝑂(`a_tran.count(ke)`), worst case
𝑂(`a_tran.size()`).

``` cpp
b.bucket_count()
```

*Result:* `size_type`

*Returns:* The number of buckets that `b` contains.

*Complexity:* Constant.

``` cpp
b.max_bucket_count()
```

*Result:* `size_type`

*Returns:* An upper bound on the number of buckets that `b` can ever
contain.

*Complexity:* Constant.

``` cpp
b.bucket(k)
```

*Result:* `size_type`

*Preconditions:* `b.bucket_count() > 0`.

*Returns:* The index of the bucket in which elements with keys
equivalent to `k` would be found, if any such element existed. The
return value is in the range `[0, b.bucket_count())`.

*Complexity:* Constant.

``` cpp
b.bucket_size(n)
```

*Result:* `size_type`

*Preconditions:* `n` shall be in the range `[0, b.bucket_count())`.

*Returns:* The number of elements in the `n`ᵗʰ bucket.

*Complexity:* 𝑂(`b.bucket_size(n)`)

``` cpp
b.begin(n)
```

*Result:* `local_iterator`; `const_local_iterator` for constant `b`.

*Preconditions:* `n` is in the range `[0, b.bucket_count())`.

*Returns:* An iterator referring to the first element in the bucket. If
the bucket is empty, then `b.begin(n) == b.end(n)`.

*Complexity:* Constant.

``` cpp
b.end(n)
```

*Result:* `local_iterator`; `const_local_iterator` for constant `b`.

*Preconditions:* `n` is in the range `[0, b.bucket_count())`.

*Returns:* An iterator which is the past-the-end value for the bucket.

*Complexity:* Constant.

``` cpp
b.cbegin(n)
```

*Result:* `const_local_iterator`

*Preconditions:* `n` shall be in the range `[0, b.bucket_count())`.

*Returns:* An iterator referring to the first element in the bucket. If
the bucket is empty, then `b.cbegin(n) == b.cend(n)`.

*Complexity:* Constant.

``` cpp
b.cend(n)
```

*Result:* `const_local_iterator`

*Preconditions:* `n` is in the range `[0, b.bucket_count())`.

*Returns:* An iterator which is the past-the-end value for the bucket.

*Complexity:* Constant.

``` cpp
b.load_factor()
```

*Result:* `float`

*Returns:* The average number of elements per bucket.

*Complexity:* Constant.

``` cpp
b.max_load_factor()
```

*Result:* `float`

*Returns:* A positive number that the container attempts to keep the
load factor less than or equal to. The container automatically increases
the number of buckets as necessary to keep the load factor below this
number.

*Complexity:* Constant.

``` cpp
a.max_load_factor(z)
```

*Result:* `void`

*Preconditions:* `z` is positive. May change the container’s maximum
load factor, using `z` as a hint.

*Complexity:* Constant.

``` cpp
a.rehash(n)
```

*Result:* `void`

*Ensures:* `a.bucket_count() >= a.size() / a.max_load_factor()` and
`a.bucket_count() >= n`.

*Complexity:* Average case linear in `a.size()`, worst case quadratic.

``` cpp
a.reserve(n)
```

*Effects:* Equivalent to `a.rehash(ceil(n / a.max_load_factor()))`.

Two unordered containers `a` and `b` compare equal if
`a.size() == b.size()` and, for every equivalent-key group \[`Ea1`,
`Ea2`) obtained from `a.equal_range(Ea1)`, there exists an
equivalent-key group \[`Eb1`, `Eb2`) obtained from `b.equal_range(Ea1)`,
such that `is_permutation(Ea1, Ea2, Eb1, Eb2)` returns `true`. For
`unordered_set` and `unordered_map`, the complexity of `operator==`
(i.e., the number of calls to the `==` operator of the `value_type`, to
the predicate returned by `key_eq()`, and to the hasher returned by
`hash_function()`) is proportional to N in the average case and to N² in
the worst case, where N is `a.size()`. For `unordered_multiset` and
`unordered_multimap`, the complexity of `operator==` is proportional to
$\sum E_i^2$ in the average case and to N² in the worst case, where N is
`a.size()`, and Eᵢ is the size of the iᵗʰ equivalent-key group in `a`.
However, if the respective elements of each corresponding pair of
equivalent-key groups Eaᵢ and Ebᵢ are arranged in the same order (as is
commonly the case, e.g., if `a` and `b` are unmodified copies of the
same container), then the average-case complexity for
`unordered_multiset` and `unordered_multimap` becomes proportional to N
(but worst-case complexity remains 𝑂(N^2), e.g., for a pathologically
bad hash function). The behavior of a program that uses `operator==` or
`operator!=` on unordered containers is undefined unless the `Pred`
function object has the same behavior for both containers and the
equality comparison function for `Key` is a refinement[^1]

of the partition into equivalent-key groups produced by `Pred`.

The iterator types `iterator` and `const_iterator` of an unordered
associative container are of at least the forward iterator category. For
unordered associative containers where the key type and value type are
the same, both `iterator` and `const_iterator` are constant iterators.

The `insert`, `insert_range`, and `emplace` members shall not affect the
validity of references to container elements, but may invalidate all
iterators to the container. The `erase` members shall invalidate only
iterators and references to the erased elements, and preserve the
relative order of the elements that are not erased.

The `insert`, `insert_range`, and `emplace` members shall not affect the
validity of iterators if `(N+n) <= z * B`, where `N` is the number of
elements in the container prior to the insert operation, `n` is the
number of elements inserted, `B` is the container’s bucket count, and
`z` is the container’s maximum load factor.

The `extract` members invalidate only iterators to the removed element,
and preserve the relative order of the elements that are not erased;
pointers and references to the removed element remain valid. However,
accessing the element through such pointers and references while the
element is owned by a `node_type` is undefined behavior. References and
pointers to an element obtained while it is owned by a `node_type` are
invalidated if the element is successfully inserted.

The member function templates `find`, `count`, `equal_range`,
`contains`, `extract`, and `erase` shall not participate in overload
resolution unless the *qualified-id*s `Pred::is_transparent` and
`Hash::is_transparent` are both valid and denote types [[temp.deduct]].
Additionally, the member function templates `extract` and `erase` shall
not participate in overload resolution if
`is_convertible_v<K&&, iterator> || is_convertible_v<K&&, const_iterator>`
is `true`, where `K` is the type substituted as the first template
argument.

A deduction guide for an unordered associative container shall not
participate in overload resolution if any of the following are true:

- It has an `InputIterator` template parameter and a type that does not
  qualify as an input iterator is deduced for that parameter.
- It has an `Allocator` template parameter and a type that does not
  qualify as an allocator is deduced for that parameter.
- It has a `Hash` template parameter and an integral type or a type that
  qualifies as an allocator is deduced for that parameter.
- It has a `Pred` template parameter and a type that qualifies as an
  allocator is deduced for that parameter.

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
`Hash` or `Pred` object (if any).

For unordered associative containers, if an exception is thrown from
within a `rehash()` function other than by the container’s hash function
or comparison function, the `rehash()` function has no effect.

## Sequence containers <a id="sequences">[[sequences]]</a>

### In general <a id="sequences.general">[[sequences.general]]</a>

The headers `<array>`, `<deque>`, `<forward_list>`, `<list>`, and
`<vector>` define class templates that meet the requirements for
sequence containers.

The following exposition-only alias template may appear in deduction
guides for sequence containers:

``` cpp
template<class InputIterator>
  using iter-value-type = typename iterator_traits<InputIterator>::value_type;  // exposition only
```

### Header `<array>` synopsis <a id="array.syn">[[array.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [array], class template array
  template<class T, size_t N> struct array;

  template<class T, size_t N>
    constexpr bool operator==(const array<T, N>& x, const array<T, N>& y);
  template<class T, size_t N>
    constexpr synth-three-way-result<T>
      operator<=>(const array<T, N>& x, const array<T, N>& y);

  // [array.special], specialized algorithms
  template<class T, size_t N>
    constexpr void swap(array<T, N>& x, array<T, N>& y) noexcept(noexcept(x.swap(y)));

  // [array.creation], array creation functions
  template<class T, size_t N>
    constexpr array<remove_cv_t<T>, N> to_array(T (&a)[N]);
  template<class T, size_t N>
    constexpr array<remove_cv_t<T>, N> to_array(T (&&a)[N]);

  // [array.tuple], tuple interface
  template<class T> struct tuple_size;
  template<size_t I, class T> struct tuple_element;
  template<class T, size_t N>
    struct tuple_size<array<T, N>>;
  template<size_t I, class T, size_t N>
    struct tuple_element<I, array<T, N>>;
  template<size_t I, class T, size_t N>
    constexpr T& get(array<T, N>&) noexcept;
  template<size_t I, class T, size_t N>
    constexpr T&& get(array<T, N>&&) noexcept;
  template<size_t I, class T, size_t N>
    constexpr const T& get(const array<T, N>&) noexcept;
  template<size_t I, class T, size_t N>
    constexpr const T&& get(const array<T, N>&&) noexcept;
}
```

### Header `<deque>` synopsis <a id="deque.syn">[[deque.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [deque], class template deque
  template<class T, class Allocator = allocator<T>> class deque;

  template<class T, class Allocator>
    bool operator==(const deque<T, Allocator>& x, const deque<T, Allocator>& y);
  template<class T, class Allocator>
    synth-three-way-result<T> operator<=>(const deque<T, Allocator>& x,
    \itcorr                                      const deque<T, Allocator>& y);

  template<class T, class Allocator>
    void swap(deque<T, Allocator>& x, deque<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [deque.erasure], erasure
  template<class T, class Allocator, class U>
    typename deque<T, Allocator>::size_type
      erase(deque<T, Allocator>& c, const U& value);
  template<class T, class Allocator, class Predicate>
    typename deque<T, Allocator>::size_type
      erase_if(deque<T, Allocator>& c, Predicate pred);

  namespace pmr {
    template<class T>
      using deque = std::deque<T, polymorphic_allocator<T>>;
  }
}
```

### Header `<forward_list>` synopsis <a id="forward.list.syn">[[forward.list.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [forward.list], class template forward_list
  template<class T, class Allocator = allocator<T>> class forward_list;

  template<class T, class Allocator>
    bool operator==(const forward_list<T, Allocator>& x, const forward_list<T, Allocator>& y);
  template<class T, class Allocator>
    synth-three-way-result<T> operator<=>(const forward_list<T, Allocator>& x,
    \itcorr                                      const forward_list<T, Allocator>& y);

  template<class T, class Allocator>
    void swap(forward_list<T, Allocator>& x, forward_list<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [forward.list.erasure], erasure
  template<class T, class Allocator, class U>
    typename forward_list<T, Allocator>::size_type
      erase(forward_list<T, Allocator>& c, const U& value);
  template<class T, class Allocator, class Predicate>
    typename forward_list<T, Allocator>::size_type
      erase_if(forward_list<T, Allocator>& c, Predicate pred);

  namespace pmr {
    template<class T>
      using forward_list = std::forward_list<T, polymorphic_allocator<T>>;
  }
}
```

### Header `<list>` synopsis <a id="list.syn">[[list.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [list], class template list
  template<class T, class Allocator = allocator<T>> class list;

  template<class T, class Allocator>
    bool operator==(const list<T, Allocator>& x, const list<T, Allocator>& y);
  template<class T, class Allocator>
    synth-three-way-result<T> operator<=>(const list<T, Allocator>& x,
    \itcorr                                      const list<T, Allocator>& y);

  template<class T, class Allocator>
    void swap(list<T, Allocator>& x, list<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [list.erasure], erasure
  template<class T, class Allocator, class U>
    typename list<T, Allocator>::size_type
      erase(list<T, Allocator>& c, const U& value);
  template<class T, class Allocator, class Predicate>
    typename list<T, Allocator>::size_type
      erase_if(list<T, Allocator>& c, Predicate pred);

  namespace pmr {
    template<class T>
      using list = std::list<T, polymorphic_allocator<T>>;
  }
}
```

### Header `<vector>` synopsis <a id="vector.syn">[[vector.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [vector], class template vector
  template<class T, class Allocator = allocator<T>> class vector;

  template<class T, class Allocator>
    constexpr bool operator==(const vector<T, Allocator>& x, const vector<T, Allocator>& y);
  template<class T, class Allocator>
    constexpr synth-three-way-result<T> operator<=>(const vector<T, Allocator>& x,
              \itcorr                                      const vector<T, Allocator>& y);

  template<class T, class Allocator>
    constexpr void swap(vector<T, Allocator>& x, vector<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [vector.erasure], erasure
  template<class T, class Allocator, class U>
    constexpr typename vector<T, Allocator>::size_type
      erase(vector<T, Allocator>& c, const U& value);
  template<class T, class Allocator, class Predicate>
    constexpr typename vector<T, Allocator>::size_type
      erase_if(vector<T, Allocator>& c, Predicate pred);

  namespace pmr {
    template<class T>
      using vector = std::vector<T, polymorphic_allocator<T>>;
  }

  // [vector.bool], specialization of vector for bool
  // [vector.bool.pspc], partial class template specialization vector<bool, Allocator>
  template<class Allocator>
    class vector<bool, Allocator>;

  template<class T>
    constexpr bool is-vector-bool-reference = see below;          // exposition only

  // hash support
  template<class T> struct hash;
  template<class Allocator> struct hash<vector<bool, Allocator>>;

  // [vector.bool.fmt], formatter specialization for vector<bool>
  template<class T, class charT> requires is-vector-bool-reference<T>
    struct formatter<T, charT>;
}
```

### Class template `array` <a id="array">[[array]]</a>

#### Overview <a id="array.overview">[[array.overview]]</a>

The header `<array>` defines a class template for storing fixed-size
sequences of objects. An `array` is a contiguous container
[[container.reqmts]]. An instance of `array<T, N>` stores `N` elements
of type `T`, so that `size() == N` is an invariant.

An `array` is an aggregate [[dcl.init.aggr]] that can be
list-initialized with up to `N` elements whose types are convertible to
`T`.

An `array` meets all of the requirements of a container
[[container.reqmts]] and of a reversible container
[[container.rev.reqmts]], except that a default constructed `array`
object is not empty if `N` > 0. An `array` meets some of the
requirements of a sequence container [[sequence.reqmts]]. Descriptions
are provided here only for operations on `array` that are not described
in one of these tables and for operations where there is additional
semantic information.

`array<T, N>` is a structural type [[temp.param]] if `T` is a structural
type. Two values `a1` and `a2` of type `array<T, N>` are
template-argument-equivalent [[temp.type]] if and only if each pair of
corresponding elements in `a1` and `a2` are
template-argument-equivalent.

The types `iterator` and `const_iterator` meet the constexpr iterator
requirements [[iterator.requirements.general]].

``` cpp
namespace std {
  template<class T, size_t N>
  struct array {
    // types
    using value_type             = T;
    using pointer                = T*;
    using const_pointer          = const T*;
    using reference              = T&;
    using const_reference        = const T&;
    using size_type              = size_t;
    using difference_type        = ptrdiff_t;
    using iterator               = implementation-defined  // type of array::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of array::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;

    // no explicit construct/copy/destroy for aggregate type

    constexpr void fill(const T& u);
    constexpr void swap(array&) noexcept(is_nothrow_swappable_v<T>);

    // iterators
    constexpr iterator               begin() noexcept;
    constexpr const_iterator         begin() const noexcept;
    constexpr iterator               end() noexcept;
    constexpr const_iterator         end() const noexcept;

    constexpr reverse_iterator       rbegin() noexcept;
    constexpr const_reverse_iterator rbegin() const noexcept;
    constexpr reverse_iterator       rend() noexcept;
    constexpr const_reverse_iterator rend() const noexcept;

    constexpr const_iterator         cbegin() const noexcept;
    constexpr const_iterator         cend() const noexcept;
    constexpr const_reverse_iterator crbegin() const noexcept;
    constexpr const_reverse_iterator crend() const noexcept;

    // capacity
    [[nodiscard]] constexpr bool empty() const noexcept;
    constexpr size_type size() const noexcept;
    constexpr size_type max_size() const noexcept;

    // element access
    constexpr reference       operator[](size_type n);
    constexpr const_reference operator[](size_type n) const;
    constexpr reference       at(size_type n);
    constexpr const_reference at(size_type n) const;
    constexpr reference       front();
    constexpr const_reference front() const;
    constexpr reference       back();
    constexpr const_reference back() const;

    constexpr T *       data() noexcept;
    constexpr const T * data() const noexcept;
  };

  template<class T, class... U>
    array(T, U...) -> array<T, 1 + sizeof...(U)>;
}
```

#### Constructors, copy, and assignment <a id="array.cons">[[array.cons]]</a>

The conditions for an aggregate [[dcl.init.aggr]] shall be met. Class
`array` relies on the implicitly-declared special member functions
[[class.default.ctor]], [[class.dtor]], [[class.copy.ctor]] to conform
to the container requirements table in  [[container.requirements]]. In
addition to the requirements specified in the container requirements
table, the implicit move constructor and move assignment operator for
`array` require that `T` be *Cpp17MoveConstructible* or
*Cpp17MoveAssignable*, respectively.

``` cpp
template<class T, class... U>
  array(T, U...) -> array<T, 1 + sizeof...(U)>;
```

*Mandates:* `(is_same_v<T, U> && ...)` is `true`.

#### Member functions <a id="array.members">[[array.members]]</a>

``` cpp
constexpr size_type size() const noexcept;
```

*Returns:* `N`.

``` cpp
constexpr T* data() noexcept;
constexpr const T* data() const noexcept;
```

*Returns:* A pointer such that \[`data()`, `data() + size()`) is a valid
range. For a non-empty array, `data()` `==` `addressof(front())`.

``` cpp
constexpr void fill(const T& u);
```

*Effects:* As if by `fill_n(begin(), N, u)`.

``` cpp
constexpr void swap(array& y) noexcept(is_nothrow_swappable_v<T>);
```

*Effects:* Equivalent to `swap_ranges(begin(), end(), y.begin())`.

[*Note 1*: Unlike the `swap` function for other containers,
`array::swap` takes linear time, can exit via an exception, and does not
cause iterators to become associated with the other
container. — *end note*]

#### Specialized algorithms <a id="array.special">[[array.special]]</a>

``` cpp
template<class T, size_t N>
  constexpr void swap(array<T, N>& x, array<T, N>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `N == 0` or `is_swappable_v<T>` is `true`.

*Effects:* As if by `x.swap(y)`.

*Complexity:* Linear in `N`.

#### Zero-sized arrays <a id="array.zero">[[array.zero]]</a>

`array` shall provide support for the special case `N == 0`.

In the case that `N == 0`, `begin() == end() ==` unique value. The
return value of `data()` is unspecified.

The effect of calling `front()` or `back()` for a zero-sized array is
undefined.

Member function `swap()` shall have a non-throwing exception
specification.

#### Array creation functions <a id="array.creation">[[array.creation]]</a>

``` cpp
template<class T, size_t N>
  constexpr array<remove_cv_t<T>, N> to_array(T (&a)[N]);
```

*Mandates:* `is_array_v<T>` is `false` and `is_constructible_v<T, T&>`
is `true`.

*Preconditions:* `T` meets the *Cpp17CopyConstructible* requirements.

*Returns:* `{{ a[0], `…`, a[N - 1] }}`.

``` cpp
template<class T, size_t N>
  constexpr array<remove_cv_t<T>, N> to_array(T (&&a)[N]);
```

*Mandates:* `is_array_v<T>` is `false` and `is_move_constructible_v<T>`
is `true`.

*Preconditions:* `T` meets the *Cpp17MoveConstructible* requirements.

*Returns:* `{{ std::move(a[0]), `…`, std::move(a[N - 1]) }}`.

#### Tuple interface <a id="array.tuple">[[array.tuple]]</a>

``` cpp
template<class T, size_t N>
  struct tuple_size<array<T, N>> : integral_constant<size_t, N> { };
```

``` cpp
template<size_t I, class T, size_t N>
  struct tuple_element<I, array<T, N>> {
    using type = T;
  };
```

*Mandates:* `I < N` is `true`.

``` cpp
template<size_t I, class T, size_t N>
  constexpr T& get(array<T, N>& a) noexcept;
template<size_t I, class T, size_t N>
  constexpr T&& get(array<T, N>&& a) noexcept;
template<size_t I, class T, size_t N>
  constexpr const T& get(const array<T, N>& a) noexcept;
template<size_t I, class T, size_t N>
  constexpr const T&& get(const array<T, N>&& a) noexcept;
```

*Mandates:* `I < N` is `true`.

*Returns:* A reference to the `I`ᵗʰ element of `a`, where indexing is
zero-based.

### Class template `deque` <a id="deque">[[deque]]</a>

#### Overview <a id="deque.overview">[[deque.overview]]</a>

A `deque` is a sequence container that supports random access iterators
[[random.access.iterators]]. In addition, it supports constant time
insert and erase operations at the beginning or the end; insert and
erase in the middle take linear time. That is, a deque is especially
optimized for pushing and popping elements at the beginning and end.
Storage management is handled automatically.

A `deque` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], and of a sequence container, including the
optional sequence container requirements [[sequence.reqmts]].
Descriptions are provided here only for operations on `deque` that are
not described in one of these tables or for operations where there is
additional semantic information.

``` cpp
namespace std {
  template<class T, class Allocator = allocator<T>>
  class deque {
  public:
    // types
    using value_type             = T;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of deque::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of deque::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of deque::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of deque::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;

    // [deque.cons], construct/copy/destroy
    deque() : deque(Allocator()) { }
    explicit deque(const Allocator&);
    explicit deque(size_type n, const Allocator& = Allocator());
    deque(size_type n, const T& value, const Allocator& = Allocator());
    template<class InputIterator>
      deque(InputIterator first, InputIterator last, const Allocator& = Allocator());
    template<container-compatible-range<T> R>
      deque(from_range_t, R&& rg, const Allocator& = Allocator());
    deque(const deque& x);
    deque(deque&&);
    deque(const deque&, const type_identity_t<Allocator>&);
    deque(deque&&, const type_identity_t<Allocator>&);
    deque(initializer_list<T>, const Allocator& = Allocator());

    ~deque();
    deque& operator=(const deque& x);
    deque& operator=(deque&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    deque& operator=(initializer_list<T>);
    template<class InputIterator>
      void assign(InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      void assign_range(R&& rg);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // iterators
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

    // [deque.capacity], capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;
    void      resize(size_type sz);
    void      resize(size_type sz, const T& c);
    void      shrink_to_fit();

    // element access
    reference       operator[](size_type n);
    const_reference operator[](size_type n) const;
    reference       at(size_type n);
    const_reference at(size_type n) const;
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    // [deque.modifiers], modifiers
    template<class... Args> reference emplace_front(Args&&... args);
    template<class... Args> reference emplace_back(Args&&... args);
    template<class... Args> iterator emplace(const_iterator position, Args&&... args);

    void push_front(const T& x);
    void push_front(T&& x);
    template<container-compatible-range<T> R>
      void prepend_range(R&& rg);
    void push_back(const T& x);
    void push_back(T&& x);
    template<container-compatible-range<T> R>
      void append_range(R&& rg);

    iterator insert(const_iterator position, const T& x);
    iterator insert(const_iterator position, T&& x);
    iterator insert(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      iterator insert(const_iterator position, InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      iterator insert_range(const_iterator position, R&& rg);
    iterator insert(const_iterator position, initializer_list<T>);

    void pop_front();
    void pop_back();

    iterator erase(const_iterator position);
    iterator erase(const_iterator first, const_iterator last);
    void     swap(deque&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    void     clear() noexcept;
  };

  template<class InputIterator, class Allocator = allocator<iter-value-type<InputIterator>>>
    deque(InputIterator, InputIterator, Allocator = Allocator())
      -> deque<iter-value-type<InputIterator>, Allocator>;

  template<ranges::input_range R, class Allocator = allocator<ranges::range_value_t<R>>>
    deque(from_range_t, R&&, Allocator = Allocator())
      -> deque<ranges::range_value_t<R>, Allocator>;
}
```

#### Constructors, copy, and assignment <a id="deque.cons">[[deque.cons]]</a>

``` cpp
explicit deque(const Allocator&);
```

*Effects:* Constructs an empty `deque`, using the specified allocator.

*Complexity:* Constant.

``` cpp
explicit deque(size_type n, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Effects:* Constructs a `deque` with `n` default-inserted elements using
the specified allocator.

*Complexity:* Linear in `n`.

``` cpp
deque(size_type n, const T& value, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* Constructs a `deque` with `n` copies of `value`, using the
specified allocator.

*Complexity:* Linear in `n`.

``` cpp
template<class InputIterator>
  deque(InputIterator first, InputIterator last, const Allocator& = Allocator());
```

*Effects:* Constructs a `deque` equal to the range \[`first`, `last`),
using the specified allocator.

*Complexity:* Linear in `distance(first, last)`.

``` cpp
template<container-compatible-range<T> R>
  deque(from_range_t, R&& rg, const Allocator& = Allocator());
```

*Effects:* Constructs a `deque` with the elements of the range `rg`,
using the specified allocator.

*Complexity:* Linear in `ranges::distance(rg)`.

#### Capacity <a id="deque.capacity">[[deque.capacity]]</a>

``` cpp
void resize(size_type sz);
```

*Preconditions:* `T` is *Cpp17MoveInsertable* and
*Cpp17DefaultInsertable* into `*this`.

*Effects:* If `sz < size()`, erases the last `size() - sz` elements from
the sequence. Otherwise, appends `sz - size()` default-inserted elements
to the sequence.

``` cpp
void resize(size_type sz, const T& c);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* If `sz < size()`, erases the last `size() - sz` elements from
the sequence. Otherwise, appends `sz - size()` copies of `c` to the
sequence.

``` cpp
void shrink_to_fit();
```

*Preconditions:* `T` is *Cpp17MoveInsertable* into `*this`.

*Effects:* `shrink_to_fit` is a non-binding request to reduce memory use
but does not change the size of the sequence.

[*Note 1*: The request is non-binding to allow latitude for
implementation-specific optimizations. — *end note*]

If the size is equal to the old capacity, or if an exception is thrown
other than by the move constructor of a non-*Cpp17CopyInsertable* `T`,
then there are no effects.

*Complexity:* If the size is not equal to the old capacity, linear in
the size of the sequence; otherwise constant.

*Remarks:* If the size is not equal to the old capacity, then
invalidates all the references, pointers, and iterators referring to the
elements in the sequence, as well as the past-the-end iterator.

#### Modifiers <a id="deque.modifiers">[[deque.modifiers]]</a>

``` cpp
iterator insert(const_iterator position, const T& x);
iterator insert(const_iterator position, T&& x);
iterator insert(const_iterator position, size_type n, const T& x);
template<class InputIterator>
  iterator insert(const_iterator position,
                  InputIterator first, InputIterator last);
template<container-compatible-range<T> R>
  iterator insert_range(const_iterator position, R&& rg);
iterator insert(const_iterator position, initializer_list<T>);

template<class... Args> reference emplace_front(Args&&... args);
template<class... Args> reference emplace_back(Args&&... args);
template<class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_front(const T& x);
void push_front(T&& x);
template<container-compatible-range<T> R>
  void prepend_range(R&& rg);
void push_back(const T& x);
void push_back(T&& x);
template<container-compatible-range<T> R>
  void append_range(R&& rg);
```

*Effects:* An insertion in the middle of the deque invalidates all the
iterators and references to elements of the deque. An insertion at
either end of the deque invalidates all the iterators to the deque, but
has no effect on the validity of references to elements of the deque.

*Complexity:* The complexity is linear in the number of elements
inserted plus the lesser of the distances to the beginning and end of
the deque. Inserting a single element at either the beginning or end of
a deque always takes constant time and causes a single call to a
constructor of `T`.

*Remarks:* If an exception is thrown other than by the copy constructor,
move constructor, assignment operator, or move assignment operator of
`T` there are no effects. If an exception is thrown while inserting a
single element at either end, there are no effects. Otherwise, if an
exception is thrown by the move constructor of a
non-*Cpp17CopyInsertable* `T`, the effects are unspecified.

``` cpp
iterator erase(const_iterator position);
iterator erase(const_iterator first, const_iterator last);
void pop_front();
void pop_back();
```

*Effects:* An erase operation that erases the last element of a deque
invalidates only the past-the-end iterator and all iterators and
references to the erased elements. An erase operation that erases the
first element of a deque but not the last element invalidates only
iterators and references to the erased elements. An erase operation that
erases neither the first element nor the last element of a deque
invalidates the past-the-end iterator and all iterators and references
to all the elements of the deque.

[*Note 1*: `pop_front` and `pop_back` are erase
operations. — *end note*]

*Throws:* Nothing unless an exception is thrown by the assignment
operator of `T`.

*Complexity:* The number of calls to the destructor of `T` is the same
as the number of elements erased, but the number of calls to the
assignment operator of `T` is no more than the lesser of the number of
elements before the erased elements and the number of elements after the
erased elements.

#### Erasure <a id="deque.erasure">[[deque.erasure]]</a>

``` cpp
template<class T, class Allocator, class U>
  typename deque<T, Allocator>::size_type
    erase(deque<T, Allocator>& c, const U& value);
```

*Effects:* Equivalent to:

``` cpp
auto it = remove(c.begin(), c.end(), value);
auto r = distance(it, c.end());
c.erase(it, c.end());
return r;
```

``` cpp
template<class T, class Allocator, class Predicate>
  typename deque<T, Allocator>::size_type
    erase_if(deque<T, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto it = remove_if(c.begin(), c.end(), pred);
auto r = distance(it, c.end());
c.erase(it, c.end());
return r;
```

### Class template `forward_list` <a id="forward.list">[[forward.list]]</a>

#### Overview <a id="forward.list.overview">[[forward.list.overview]]</a>

A `forward_list` is a container that supports forward iterators and
allows constant time insert and erase operations anywhere within the
sequence, with storage management handled automatically. Fast random
access to list elements is not supported.

[*Note 1*: It is intended that `forward_list` have zero space or time
overhead relative to a hand-written C-style singly linked list. Features
that would conflict with that goal have been omitted. — *end note*]

A `forward_list` meets all of the requirements of a container
[[container.reqmts]], except that the `size()` member function is not
provided and `operator==` has linear complexity, A `forward_list` also
meets all of the requirements for an allocator-aware container
[[container.alloc.reqmts]]. In addition, a `forward_list` provides the
`assign` member functions and several of the optional sequence container
requirements [[sequence.reqmts]]. Descriptions are provided here only
for operations on `forward_list` that are not described in that table or
for operations where there is additional semantic information.

[*Note 2*: Modifying any list requires access to the element preceding
the first element of interest, but in a `forward_list` there is no
constant-time way to access a preceding element. For this reason,
`erase_after` and `splice_after` take fully-open ranges, not semi-open
ranges. — *end note*]

``` cpp
namespace std {
  template<class T, class Allocator = allocator<T>>
  class forward_list {
  public:
    // types
    using value_type      = T;
    using allocator_type  = Allocator;
    using pointer         = typename allocator_traits<Allocator>::pointer;
    using const_pointer   = typename allocator_traits<Allocator>::const_pointer;
    using reference       = value_type&;
    using const_reference = const value_type&;
    using size_type       = implementation-defined  // type of forward_list::size_type; // see [container.requirements]
    using difference_type = implementation-defined  // type of forward_list::difference_type; // see [container.requirements]
    using iterator        = implementation-defined  // type of forward_list::iterator; // see [container.requirements]
    using const_iterator  = implementation-defined  // type of forward_list::const_iterator; // see [container.requirements]

    // [forward.list.cons], construct/copy/destroy
    forward_list() : forward_list(Allocator()) { }
    explicit forward_list(const Allocator&);
    explicit forward_list(size_type n, const Allocator& = Allocator());
    forward_list(size_type n, const T& value, const Allocator& = Allocator());
    template<class InputIterator>
      forward_list(InputIterator first, InputIterator last, const Allocator& = Allocator());
    template<container-compatible-range<T> R>
      forward_list(from_range_t, R&& rg, const Allocator& = Allocator());
    forward_list(const forward_list& x);
    forward_list(forward_list&& x);
    forward_list(const forward_list& x, const type_identity_t<Allocator>&);
    forward_list(forward_list&& x, const type_identity_t<Allocator>&);
    forward_list(initializer_list<T>, const Allocator& = Allocator());
    ~forward_list();
    forward_list& operator=(const forward_list& x);
    forward_list& operator=(forward_list&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    forward_list& operator=(initializer_list<T>);
    template<class InputIterator>
      void assign(InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      void assign_range(R&& rg);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // [forward.list.iter], iterators
    iterator before_begin() noexcept;
    const_iterator before_begin() const noexcept;
    iterator begin() noexcept;
    const_iterator begin() const noexcept;
    iterator end() noexcept;
    const_iterator end() const noexcept;

    const_iterator cbegin() const noexcept;
    const_iterator cbefore_begin() const noexcept;
    const_iterator cend() const noexcept;

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type max_size() const noexcept;

    // [forward.list.access], element access
    reference front();
    const_reference front() const;

    // [forward.list.modifiers], modifiers
    template<class... Args> reference emplace_front(Args&&... args);
    void push_front(const T& x);
    void push_front(T&& x);
    template<container-compatible-range<T> R>
      void prepend_range(R&& rg);
    void pop_front();

    template<class... Args> iterator emplace_after(const_iterator position, Args&&... args);
    iterator insert_after(const_iterator position, const T& x);
    iterator insert_after(const_iterator position, T&& x);

    iterator insert_after(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      iterator insert_after(const_iterator position, InputIterator first, InputIterator last);
    iterator insert_after(const_iterator position, initializer_list<T> il);
    template<container-compatible-range<T> R>
      iterator insert_range_after(const_iterator position, R&& rg);

    iterator erase_after(const_iterator position);
    iterator erase_after(const_iterator position, const_iterator last);
    void swap(forward_list&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);

    void resize(size_type sz);
    void resize(size_type sz, const value_type& c);
    void clear() noexcept;

    // [forward.list.ops], forward_list operations
    void splice_after(const_iterator position, forward_list& x);
    void splice_after(const_iterator position, forward_list&& x);
    void splice_after(const_iterator position, forward_list& x, const_iterator i);
    void splice_after(const_iterator position, forward_list&& x, const_iterator i);
    void splice_after(const_iterator position, forward_list& x,
                      const_iterator first, const_iterator last);
    void splice_after(const_iterator position, forward_list&& x,
                      const_iterator first, const_iterator last);

    size_type remove(const T& value);
    template<class Predicate> size_type remove_if(Predicate pred);

    size_type unique();
    template<class BinaryPredicate> size_type unique(BinaryPredicate binary_pred);

    void merge(forward_list& x);
    void merge(forward_list&& x);
    template<class Compare> void merge(forward_list& x, Compare comp);
    template<class Compare> void merge(forward_list&& x, Compare comp);

    void sort();
    template<class Compare> void sort(Compare comp);

    void reverse() noexcept;
  };

  template<class InputIterator, class Allocator = allocator<iter-value-type<InputIterator>>>
    forward_list(InputIterator, InputIterator, Allocator = Allocator())
      -> forward_list<iter-value-type<InputIterator>, Allocator>;

  template<ranges::input_range R, class Allocator = allocator<ranges::range_value_t<R>>>
    forward_list(from_range_t, R&&, Allocator = Allocator())
      -> forward_list<ranges::range_value_t<R>, Allocator>;
}
```

An incomplete type `T` may be used when instantiating `forward_list` if
the allocator meets the allocator completeness requirements
[[allocator.requirements.completeness]]. `T` shall be complete before
any member of the resulting specialization of `forward_list` is
referenced.

#### Constructors, copy, and assignment <a id="forward.list.cons">[[forward.list.cons]]</a>

``` cpp
explicit forward_list(const Allocator&);
```

*Effects:* Constructs an empty `forward_list` object using the specified
allocator.

*Complexity:* Constant.

``` cpp
explicit forward_list(size_type n, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Effects:* Constructs a `forward_list` object with `n` default-inserted
elements using the specified allocator.

*Complexity:* Linear in `n`.

``` cpp
forward_list(size_type n, const T& value, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* Constructs a `forward_list` object with `n` copies of `value`
using the specified allocator.

*Complexity:* Linear in `n`.

``` cpp
template<class InputIterator>
  forward_list(InputIterator first, InputIterator last, const Allocator& = Allocator());
```

*Effects:* Constructs a `forward_list` object equal to the range
\[`first`, `last`).

*Complexity:* Linear in `distance(first, last)`.

``` cpp
template<container-compatible-range<T> R>
  forward_list(from_range_t, R&& rg, const Allocator& = Allocator());
```

*Effects:* Constructs a `forward_list` object with the elements of the
range `rg`.

*Complexity:* Linear in `ranges::distance(rg)`.

#### Iterators <a id="forward.list.iter">[[forward.list.iter]]</a>

``` cpp
iterator before_begin() noexcept;
const_iterator before_begin() const noexcept;
const_iterator cbefore_begin() const noexcept;
```

*Effects:* `cbefore_begin()` is equivalent to
`const_cast<forward_list const&>(*this).before_begin()`.

*Returns:* A non-dereferenceable iterator that, when incremented, is
equal to the iterator returned by `begin()`.

*Remarks:* `before_begin() == end()` shall equal `false`.

#### Element access <a id="forward.list.access">[[forward.list.access]]</a>

``` cpp
reference front();
const_reference front() const;
```

*Returns:* `*begin()`

#### Modifiers <a id="forward.list.modifiers">[[forward.list.modifiers]]</a>

None of the overloads of `insert_after` shall affect the validity of
iterators and references, and `erase_after` shall invalidate only
iterators and references to the erased elements. If an exception is
thrown during `insert_after` there shall be no effect. Inserting `n`
elements into a `forward_list` is linear in `n`, and the number of calls
to the copy or move constructor of `T` is exactly equal to `n`. Erasing
`n` elements from a `forward_list` is linear in `n` and the number of
calls to the destructor of type `T` is exactly equal to `n`.

``` cpp
template<class... Args> reference emplace_front(Args&&... args);
```

*Effects:* Inserts an object of type `value_type` constructed with
`value_type(std::forward<Args>(args)...)` at the beginning of the list.

``` cpp
void push_front(const T& x);
void push_front(T&& x);
```

*Effects:* Inserts a copy of `x` at the beginning of the list.

``` cpp
template<container-compatible-range<T> R>
  void prepend_range(R&& rg);
```

*Effects:* Inserts a copy of each element of `rg` at the beginning of
the list.

[*Note 1*: The order of elements is not reversed. — *end note*]

``` cpp
void pop_front();
```

*Effects:* As if by `erase_after(before_begin())`.

``` cpp
iterator insert_after(const_iterator position, const T& x);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `forward_list`.
`position` is `before_begin()` or is a dereferenceable iterator in the
range \[`begin()`, `end()`).

*Effects:* Inserts a copy of `x` after `position`.

*Returns:* An iterator pointing to the copy of `x`.

``` cpp
iterator insert_after(const_iterator position, T&& x);
```

*Preconditions:* `T` is *Cpp17MoveInsertable* into `forward_list`.
`position` is `before_begin()` or is a dereferenceable iterator in the
range \[`begin()`, `end()`).

*Effects:* Inserts a copy of `x` after `position`.

*Returns:* An iterator pointing to the copy of `x`.

``` cpp
iterator insert_after(const_iterator position, size_type n, const T& x);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `forward_list`.
`position` is `before_begin()` or is a dereferenceable iterator in the
range \[`begin()`, `end()`).

*Effects:* Inserts `n` copies of `x` after `position`.

*Returns:* An iterator pointing to the last inserted copy of `x`, or
`position` if `n == 0` is `true`.

``` cpp
template<class InputIterator>
  iterator insert_after(const_iterator position, InputIterator first, InputIterator last);
```

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `forward_list`
from `*first`. `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). Neither `first` nor `last`
are iterators in `*this`.

*Effects:* Inserts copies of elements in \[`first`, `last`) after
`position`.

*Returns:* An iterator pointing to the last inserted element, or
`position` if `first == last` is `true`.

``` cpp
template<container-compatible-range<T> R>
  iterator insert_range_after(const_iterator position, R&& rg);
```

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `forward_list`
from `*ranges::begin(rg)`. `position` is `before_begin()` or is a
dereferenceable iterator in the range \[`begin()`, `end()`). `rg` and
`*this` do not overlap.

*Effects:* Inserts copies of elements in the range `rg` after
`position`.

*Returns:* An iterator pointing to the last inserted element, or
`position` if `rg` is empty.

``` cpp
iterator insert_after(const_iterator position, initializer_list<T> il);
```

*Effects:* Equivalent to:
`return insert_after(position, il.begin(), il.end());`

``` cpp
template<class... Args>
  iterator emplace_after(const_iterator position, Args&&... args);
```

*Preconditions:* `T` is *Cpp17EmplaceConstructible* into `forward_list`
from `std::forward<Args>(args)...`. `position` is `before_begin()` or is
a dereferenceable iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts an object of type `value_type`
direct-non-list-initialized with `std::forward<Args>(args)...` after
`position`.

*Returns:* An iterator pointing to the new object.

``` cpp
iterator erase_after(const_iterator position);
```

*Preconditions:* The iterator following `position` is dereferenceable.

*Effects:* Erases the element pointed to by the iterator following
`position`.

*Returns:* An iterator pointing to the element following the one that
was erased, or `end()` if no such element exists.

*Throws:* Nothing.

``` cpp
iterator erase_after(const_iterator position, const_iterator last);
```

*Preconditions:* All iterators in the range (`position`, `last`) are
dereferenceable.

*Effects:* Erases the elements in the range (`position`, `last`).

*Returns:* `last`.

*Throws:* Nothing.

``` cpp
void resize(size_type sz);
```

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Effects:* If `sz < distance(begin(), end())`, erases the last
`distance(begin(), end()) - sz` elements from the list. Otherwise,
inserts `sz - distance(begin(), end())` default-inserted elements at the
end of the list.

``` cpp
void resize(size_type sz, const value_type& c);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* If `sz < distance(begin(), end())`, erases the last
`distance(begin(), end()) - sz` elements from the list. Otherwise,
inserts `sz - distance(begin(), end())` copies of `c` at the end of the
list.

``` cpp
void clear() noexcept;
```

*Effects:* Erases all elements in the range \[`begin()`, `end()`).

*Remarks:* Does not invalidate past-the-end iterators.

#### Operations <a id="forward.list.ops">[[forward.list.ops]]</a>

In this subclause, arguments for a template parameter named `Predicate`
or `BinaryPredicate` shall meet the corresponding requirements in
[[algorithms.requirements]]. The semantics of `i + n`, where `i` is an
iterator into the list and `n` is an integer, are the same as those of
`next(i, n)`. The expression `i - n`, where `i` is an iterator into the
list and `n` is an integer, means an iterator `j` such that `j + n == i`
is `true`. For `merge` and `sort`, the definitions and requirements in
[[alg.sorting]] apply.

``` cpp
void splice_after(const_iterator position, forward_list& x);
void splice_after(const_iterator position, forward_list&& x);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).
`get_allocator() == x.get_allocator()` is `true`. `addressof(x) != this`
is `true`.

*Effects:* Inserts the contents of `x` after `position`, and `x` becomes
empty. Pointers and references to the moved elements of `x` now refer to
those same elements but as members of `*this`. Iterators referring to
the moved elements will continue to refer to their elements, but they
now behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* 𝑂(`distance(x.begin(), x.end())`)

``` cpp
void splice_after(const_iterator position, forward_list& x, const_iterator i);
void splice_after(const_iterator position, forward_list&& x, const_iterator i);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). The iterator following `i`
is a dereferenceable iterator in `x`.
`get_allocator() == x.get_allocator()` is `true`.

*Effects:* Inserts the element following `i` into `*this`, following
`position`, and removes it from `x`. The result is unchanged if
`position == i` or `position == ++i`. Pointers and references to `*++i`
continue to refer to the same element but as a member of `*this`.
Iterators to `*++i` continue to refer to the same element, but now
behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* 𝑂(1)

``` cpp
void splice_after(const_iterator position, forward_list& x,
                  const_iterator first, const_iterator last);
void splice_after(const_iterator position, forward_list&& x,
                  const_iterator first, const_iterator last);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). (`first`, `last`) is a
valid range in `x`, and all iterators in the range (`first`, `last`) are
dereferenceable. `position` is not an iterator in the range (`first`,
`last`). `get_allocator() == x.get_allocator()` is `true`.

*Effects:* Inserts elements in the range (`first`, `last`) after
`position` and removes the elements from `x`. Pointers and references to
the moved elements of `x` now refer to those same elements but as
members of `*this`. Iterators referring to the moved elements will
continue to refer to their elements, but they now behave as iterators
into `*this`, not into `x`.

*Complexity:* 𝑂(`distance(first, last)`)

``` cpp
size_type remove(const T& value);
template<class Predicate> size_type remove_if(Predicate pred);
```

*Effects:* Erases all the elements in the list referred to by a list
iterator `i` for which the following conditions hold: `*i == value` (for
`remove()`), `pred(*i)` is `true` (for `remove_if()`). Invalidates only
the iterators and references to the erased elements.

*Returns:* The number of elements erased.

*Throws:* Nothing unless an exception is thrown by the equality
comparison or the predicate.

*Complexity:* Exactly `distance(begin(), end())` applications of the
corresponding predicate.

*Remarks:* Stable [[algorithm.stable]].

``` cpp
size_type unique();
template<class BinaryPredicate> size_type unique(BinaryPredicate binary_pred);
```

Let `binary_pred` be `equal_to<>{}` for the first overload.

*Preconditions:* `binary_pred` is an equivalence relation.

*Effects:* Erases all but the first element from every consecutive group
of equivalent elements. That is, for a nonempty list, erases all
elements referred to by the iterator `i` in the range \[`begin() + 1`,
`end()`) for which `binary_pred(*i, *(i - 1))` is `true`. Invalidates
only the iterators and references to the erased elements.

*Returns:* The number of elements erased.

*Throws:* Nothing unless an exception is thrown by the predicate.

*Complexity:* If `empty()` is `false`, exactly
`distance(begin(), end()) - 1` applications of the corresponding
predicate, otherwise no applications of the predicate.

``` cpp
void merge(forward_list& x);
void merge(forward_list&& x);
template<class Compare> void merge(forward_list& x, Compare comp);
template<class Compare> void merge(forward_list&& x, Compare comp);
```

Let `comp` be `less<>` for the first two overloads.

*Preconditions:* `*this` and `x` are both sorted with respect to the
comparator `comp`, and `get_allocator() == x.get_allocator()` is `true`.

*Effects:* If `addressof(x) == this`, there are no effects. Otherwise,
merges the two sorted ranges \[`begin()`, `end()`) and \[`x.begin()`,
`x.end()`). The result is a range that is sorted with respect to the
comparator `comp`. Pointers and references to the moved elements of `x`
now refer to those same elements but as members of `*this`. Iterators
referring to the moved elements will continue to refer to their
elements, but they now behave as iterators into `*this`, not into `x`.

*Complexity:* At most
`distance(begin(), end()) + distance(x.begin(), x.end()) - 1`
comparisons if `addressof(x) != this`; otherwise, no comparisons are
performed.

*Remarks:* Stable [[algorithm.stable]]. If `addressof(x) != this`, `x`
is empty after the merge. No elements are copied by this operation. If
an exception is thrown other than by a comparison, there are no effects.

``` cpp
void sort();
template<class Compare> void sort(Compare comp);
```

*Effects:* Sorts the list according to the `operator<` or the `comp`
function object. If an exception is thrown, the order of the elements in
`*this` is unspecified. Does not affect the validity of iterators and
references.

*Complexity:* Approximately N log N comparisons, where N is
`distance(begin(), end())`.

*Remarks:* Stable [[algorithm.stable]].

``` cpp
void reverse() noexcept;
```

*Effects:* Reverses the order of the elements in the list. Does not
affect the validity of iterators and references.

*Complexity:* Linear time.

#### Erasure <a id="forward.list.erasure">[[forward.list.erasure]]</a>

``` cpp
template<class T, class Allocator, class U>
  typename forward_list<T, Allocator>::size_type
    erase(forward_list<T, Allocator>& c, const U& value);
```

*Effects:* Equivalent to:
`return erase_if(c, [&](auto& elem) { return elem == value; });`

``` cpp
template<class T, class Allocator, class Predicate>
  typename forward_list<T, Allocator>::size_type
    erase_if(forward_list<T, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to: `return c.remove_if(pred);`

### Class template `list` <a id="list">[[list]]</a>

#### Overview <a id="list.overview">[[list.overview]]</a>

A `list` is a sequence container that supports bidirectional iterators
and allows constant time insert and erase operations anywhere within the
sequence, with storage management handled automatically. Unlike vectors
[[vector]] and deques [[deque]], fast random access to list elements is
not supported, but many algorithms only need sequential access anyway.

A `list` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], and of a sequence container, including most
of the optional sequence container requirements [[sequence.reqmts]]. The
exceptions are the `operator[]` and `at` member functions, which are not
provided.[^2]

Descriptions are provided here only for operations on `list` that are
not described in one of these tables or for operations where there is
additional semantic information.

``` cpp
namespace std {
  template<class T, class Allocator = allocator<T>>
  class list {
  public:
    // types
    using value_type             = T;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of list::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of list::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of list::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of list::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;

    // [list.cons], construct/copy/destroy
    list() : list(Allocator()) { }
    explicit list(const Allocator&);
    explicit list(size_type n, const Allocator& = Allocator());
    list(size_type n, const T& value, const Allocator& = Allocator());
    template<class InputIterator>
      list(InputIterator first, InputIterator last, const Allocator& = Allocator());
    template<container-compatible-range<T> R>
      list(from_range_t, R&& rg, const Allocator& = Allocator());
    list(const list& x);
    list(list&& x);
    list(const list&, const type_identity_t<Allocator>&);
    list(list&&, const type_identity_t<Allocator>&);
    list(initializer_list<T>, const Allocator& = Allocator());
    ~list();
    list& operator=(const list& x);
    list& operator=(list&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    list& operator=(initializer_list<T>);
    template<class InputIterator>
      void assign(InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      void assign_range(R&& rg);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // iterators
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

    // [list.capacity], capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;
    void      resize(size_type sz);
    void      resize(size_type sz, const T& c);

    // element access
    reference       front();
    const_reference front() const;
    reference       back();
    const_reference back() const;

    // [list.modifiers], modifiers
    template<class... Args> reference emplace_front(Args&&... args);
    template<class... Args> reference emplace_back(Args&&... args);
    void push_front(const T& x);
    void push_front(T&& x);
    template<container-compatible-range<T> R>
      void prepend_range(R&& rg);
    void pop_front();
    void push_back(const T& x);
    void push_back(T&& x);
    template<container-compatible-range<T> R>
      void append_range(R&& rg);
    void pop_back();

    template<class... Args> iterator emplace(const_iterator position, Args&&... args);
    iterator insert(const_iterator position, const T& x);
    iterator insert(const_iterator position, T&& x);
    iterator insert(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      iterator insert(const_iterator position, InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      iterator insert_range(const_iterator position, R&& rg);
    iterator insert(const_iterator position, initializer_list<T> il);

    iterator erase(const_iterator position);
    iterator erase(const_iterator position, const_iterator last);
    void     swap(list&) noexcept(allocator_traits<Allocator>::is_always_equal::value);
    void     clear() noexcept;

    // [list.ops], list operations
    void splice(const_iterator position, list& x);
    void splice(const_iterator position, list&& x);
    void splice(const_iterator position, list& x, const_iterator i);
    void splice(const_iterator position, list&& x, const_iterator i);
    void splice(const_iterator position, list& x, const_iterator first, const_iterator last);
    void splice(const_iterator position, list&& x, const_iterator first, const_iterator last);

    size_type remove(const T& value);
    template<class Predicate> size_type remove_if(Predicate pred);

    size_type unique();
    template<class BinaryPredicate>
      size_type unique(BinaryPredicate binary_pred);

    void merge(list& x);
    void merge(list&& x);
    template<class Compare> void merge(list& x, Compare comp);
    template<class Compare> void merge(list&& x, Compare comp);

    void sort();
    template<class Compare> void sort(Compare comp);

    void reverse() noexcept;
  };

  template<class InputIterator, class Allocator = allocator<iter-value-type<InputIterator>>>
    list(InputIterator, InputIterator, Allocator = Allocator())
      -> list<iter-value-type<InputIterator>, Allocator>;

  template<ranges::input_range R, class Allocator = allocator<ranges::range_value_t<R>>>
    list(from_range_t, R&&, Allocator = Allocator())
      -> list<ranges::range_value_t<R>, Allocator>;
}
```

An incomplete type `T` may be used when instantiating `list` if the
allocator meets the allocator completeness requirements
[[allocator.requirements.completeness]]. `T` shall be complete before
any member of the resulting specialization of `list` is referenced.

#### Constructors, copy, and assignment <a id="list.cons">[[list.cons]]</a>

``` cpp
explicit list(const Allocator&);
```

*Effects:* Constructs an empty list, using the specified allocator.

*Complexity:* Constant.

``` cpp
explicit list(size_type n, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Effects:* Constructs a `list` with `n` default-inserted elements using
the specified allocator.

*Complexity:* Linear in `n`.

``` cpp
list(size_type n, const T& value, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* Constructs a `list` with `n` copies of `value`, using the
specified allocator.

*Complexity:* Linear in `n`.

``` cpp
template<class InputIterator>
  list(InputIterator first, InputIterator last, const Allocator& = Allocator());
```

*Effects:* Constructs a `list` equal to the range \[`first`, `last`).

*Complexity:* Linear in `distance(first, last)`.

``` cpp
template<container-compatible-range<T> R>
  list(from_range_t, R&& rg, const Allocator& = Allocator());
```

*Effects:* Constructs a `list` object with the elements of the range
`rg`.

*Complexity:* Linear in `ranges::distance(rg)`.

#### Capacity <a id="list.capacity">[[list.capacity]]</a>

``` cpp
void resize(size_type sz);
```

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Effects:* If `size() < sz`, appends `sz - size()` default-inserted
elements to the sequence. If `sz <= size()`, equivalent to:

``` cpp
list<T>::iterator it = begin();
advance(it, sz);
erase(it, end());
```

``` cpp
void resize(size_type sz, const T& c);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* As if by:

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

#### Modifiers <a id="list.modifiers">[[list.modifiers]]</a>

``` cpp
iterator insert(const_iterator position, const T& x);
iterator insert(const_iterator position, T&& x);
iterator insert(const_iterator position, size_type n, const T& x);
template<class InputIterator>
  iterator insert(const_iterator position, InputIterator first,
                  InputIterator last);
template<container-compatible-range<T> R>
  iterator insert_range(const_iterator position, R&& rg);
iterator insert(const_iterator position, initializer_list<T>);

template<class... Args> reference emplace_front(Args&&... args);
template<class... Args> reference emplace_back(Args&&... args);
template<class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_front(const T& x);
void push_front(T&& x);
template<container-compatible-range<T> R>
  void prepend_range(R&& rg);
void push_back(const T& x);
void push_back(T&& x);
template<container-compatible-range<T> R>
  void append_range(R&& rg);
```

*Complexity:* Insertion of a single element into a list takes constant
time and exactly one call to a constructor of `T`. Insertion of multiple
elements into a list is linear in the number of elements inserted, and
the number of calls to the copy constructor or move constructor of `T`
is exactly equal to the number of elements inserted.

*Remarks:* Does not affect the validity of iterators and references. If
an exception is thrown there are no effects.

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

#### Operations <a id="list.ops">[[list.ops]]</a>

Since lists allow fast insertion and erasing from the middle of a list,
certain operations are provided specifically for them.[^3]

In this subclause, arguments for a template parameter named `Predicate`
or `BinaryPredicate` shall meet the corresponding requirements in
[[algorithms.requirements]]. The semantics of `i + n` and `i - n`, where
`i` is an iterator into the list and `n` is an integer, are the same as
those of `next(i, n)` and `prev(i, n)`, respectively. For `merge` and
`sort`, the definitions and requirements in [[alg.sorting]] apply.

`list` provides three splice operations that destructively move elements
from one list to another. The behavior of splice operations is undefined
if `get_allocator() !=
x.get_allocator()`.

``` cpp
void splice(const_iterator position, list& x);
void splice(const_iterator position, list&& x);
```

*Preconditions:* `addressof(x) != this` is `true`.

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

*Preconditions:* `i` is a valid dereferenceable iterator of `x`.

*Effects:* Inserts an element pointed to by `i` from list `x` before
`position` and removes the element from `x`. The result is unchanged if
`position == i` or `position == ++i`. Pointers and references to `*i`
continue to refer to this same element but as a member of `*this`.
Iterators to `*i` (including `i` itself) continue to refer to the same
element, but now behave as iterators into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* Constant time.

``` cpp
void splice(const_iterator position, list& x, const_iterator first,
            const_iterator last);
void splice(const_iterator position, list&& x, const_iterator first,
            const_iterator last);
```

*Preconditions:* `[first, last)` is a valid range in `x`. `position` is
not an iterator in the range \[`first`, `last`).

*Effects:* Inserts elements in the range \[`first`, `last`) before
`position` and removes the elements from `x`. Pointers and references to
the moved elements of `x` now refer to those same elements but as
members of `*this`. Iterators referring to the moved elements will
continue to refer to their elements, but they now behave as iterators
into `*this`, not into `x`.

*Throws:* Nothing.

*Complexity:* Constant time if `addressof(x) == this`; otherwise, linear
time.

``` cpp
size_type remove(const T& value);
template<class Predicate> size_type remove_if(Predicate pred);
```

*Effects:* Erases all the elements in the list referred to by a list
iterator `i` for which the following conditions hold: `*i == value`,
`pred(*i) != false`. Invalidates only the iterators and references to
the erased elements.

*Returns:* The number of elements erased.

*Throws:* Nothing unless an exception is thrown by `*i == value` or
`pred(*i) != false`.

*Complexity:* Exactly `size()` applications of the corresponding
predicate.

*Remarks:* Stable [[algorithm.stable]].

``` cpp
size_type unique();
template<class BinaryPredicate> size_type unique(BinaryPredicate binary_pred);
```

Let `binary_pred` be `equal_to<>{}` for the first overload.

*Preconditions:* `binary_pred` is an equivalence relation.

*Effects:* Erases all but the first element from every consecutive group
of equivalent elements. That is, for a nonempty list, erases all
elements referred to by the iterator `i` in the range \[`begin() + 1`,
`end()`) for which `binary_pred(*i, *(i - 1))` is `true`. Invalidates
only the iterators and references to the erased elements.

*Returns:* The number of elements erased.

*Throws:* Nothing unless an exception is thrown by the predicate.

*Complexity:* If `empty()` is `false`, exactly `size() - 1` applications
of the corresponding predicate, otherwise no applications of the
predicate.

``` cpp
void merge(list& x);
void merge(list&& x);
template<class Compare> void merge(list& x, Compare comp);
template<class Compare> void merge(list&& x, Compare comp);
```

Let `comp` be `less<>` for the first two overloads.

*Preconditions:* `*this` and `x` are both sorted with respect to the
comparator `comp`, and `get_allocator() == x.get_allocator()` is `true`.

*Effects:* If `addressof(x) == this`, there are no effects. Otherwise,
merges the two sorted ranges \[`begin()`, `end()`) and \[`x.begin()`,
`x.end()`). The result is a range that is sorted with respect to the
comparator `comp`. Pointers and references to the moved elements of `x`
now refer to those same elements but as members of `*this`. Iterators
referring to the moved elements will continue to refer to their
elements, but they now behave as iterators into `*this`, not into `x`.

*Complexity:* At most `size() + x.size() - 1` comparisons if
`addressof(x) != this`; otherwise, no comparisons are performed.

*Remarks:* Stable [[algorithm.stable]]. If `addressof(x) != this`, `x`
is empty after the merge. No elements are copied by this operation. If
an exception is thrown other than by a comparison there are no effects.

``` cpp
void reverse() noexcept;
```

*Effects:* Reverses the order of the elements in the list. Does not
affect the validity of iterators and references.

*Complexity:* Linear time.

``` cpp
void sort();
template<class Compare> void sort(Compare comp);
```

*Effects:* Sorts the list according to the `operator<` or a `Compare`
function object. If an exception is thrown, the order of the elements in
`*this` is unspecified. Does not affect the validity of iterators and
references.

*Complexity:* Approximately N log N comparisons, where `N == size()`.

*Remarks:* Stable [[algorithm.stable]].

#### Erasure <a id="list.erasure">[[list.erasure]]</a>

``` cpp
template<class T, class Allocator, class U>
  typename list<T, Allocator>::size_type
    erase(list<T, Allocator>& c, const U& value);
```

*Effects:* Equivalent to:
`return erase_if(c, [&](auto& elem) { return elem == value; });`

``` cpp
template<class T, class Allocator, class Predicate>
  typename list<T, Allocator>::size_type
    erase_if(list<T, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to: `return c.remove_if(pred);`

### Class template `vector` <a id="vector">[[vector]]</a>

#### Overview <a id="vector.overview">[[vector.overview]]</a>

A `vector` is a sequence container that supports (amortized) constant
time insert and erase operations at the end; insert and erase in the
middle take linear time. Storage management is handled automatically,
though hints can be given to improve efficiency.

A `vector` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], of a sequence container, including most of
the optional sequence container requirements [[sequence.reqmts]], and,
for an element type other than `bool`, of a contiguous container
[[container.reqmts]]. The exceptions are the `push_front`,
`prepend_range`, `pop_front`, and `emplace_front` member functions,
which are not provided. Descriptions are provided here only for
operations on `vector` that are not described in one of these tables or
for operations where there is additional semantic information.

The types `iterator` and `const_iterator` meet the constexpr iterator
requirements [[iterator.requirements.general]].

``` cpp
namespace std {
  template<class T, class Allocator = allocator<T>>
  class vector {
  public:
    // types
    using value_type             = T;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of vector::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of vector::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of vector::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of vector::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;

    // [vector.cons], construct/copy/destroy
    constexpr vector() noexcept(noexcept(Allocator())) : vector(Allocator()) { }
    constexpr explicit vector(const Allocator&) noexcept;
    constexpr explicit vector(size_type n, const Allocator& = Allocator());
    constexpr vector(size_type n, const T& value, const Allocator& = Allocator());
    template<class InputIterator>
      constexpr vector(InputIterator first, InputIterator last, const Allocator& = Allocator());
    template<container-compatible-range<T> R>
      constexpr vector(from_range_t, R&& rg, const Allocator& = Allocator());
    constexpr vector(const vector& x);
    constexpr vector(vector&&) noexcept;
    constexpr vector(const vector&, const type_identity_t<Allocator>&);
    constexpr vector(vector&&, const type_identity_t<Allocator>&);
    constexpr vector(initializer_list<T>, const Allocator& = Allocator());
    constexpr ~vector();
    constexpr vector& operator=(const vector& x);
    constexpr vector& operator=(vector&& x)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    constexpr vector& operator=(initializer_list<T>);
    template<class InputIterator>
      constexpr void assign(InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      constexpr void assign_range(R&& rg);
    constexpr void assign(size_type n, const T& u);
    constexpr void assign(initializer_list<T>);
    constexpr allocator_type get_allocator() const noexcept;

    // iterators
    constexpr iterator               begin() noexcept;
    constexpr const_iterator         begin() const noexcept;
    constexpr iterator               end() noexcept;
    constexpr const_iterator         end() const noexcept;
    constexpr reverse_iterator       rbegin() noexcept;
    constexpr const_reverse_iterator rbegin() const noexcept;
    constexpr reverse_iterator       rend() noexcept;
    constexpr const_reverse_iterator rend() const noexcept;

    constexpr const_iterator         cbegin() const noexcept;
    constexpr const_iterator         cend() const noexcept;
    constexpr const_reverse_iterator crbegin() const noexcept;
    constexpr const_reverse_iterator crend() const noexcept;

    // [vector.capacity], capacity
    [[nodiscard]] constexpr bool empty() const noexcept;
    constexpr size_type size() const noexcept;
    constexpr size_type max_size() const noexcept;
    constexpr size_type capacity() const noexcept;
    constexpr void      resize(size_type sz);
    constexpr void      resize(size_type sz, const T& c);
    constexpr void      reserve(size_type n);
    constexpr void      shrink_to_fit();

    // element access
    constexpr reference       operator[](size_type n);
    constexpr const_reference operator[](size_type n) const;
    constexpr const_reference at(size_type n) const;
    constexpr reference       at(size_type n);
    constexpr reference       front();
    constexpr const_reference front() const;
    constexpr reference       back();
    constexpr const_reference back() const;

    // [vector.data], data access
    constexpr T*       data() noexcept;
    constexpr const T* data() const noexcept;

    // [vector.modifiers], modifiers
    template<class... Args> constexpr reference emplace_back(Args&&... args);
    constexpr void push_back(const T& x);
    constexpr void push_back(T&& x);
    template<container-compatible-range<T> R>
      constexpr void append_range(R&& rg);
    constexpr void pop_back();

    template<class... Args> constexpr iterator emplace(const_iterator position, Args&&... args);
    constexpr iterator insert(const_iterator position, const T& x);
    constexpr iterator insert(const_iterator position, T&& x);
    constexpr iterator insert(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      constexpr iterator insert(const_iterator position,
                                InputIterator first, InputIterator last);
    template<container-compatible-range<T> R>
      constexpr iterator insert_range(const_iterator position, R&& rg);
    constexpr iterator insert(const_iterator position, initializer_list<T> il);
    constexpr iterator erase(const_iterator position);
    constexpr iterator erase(const_iterator first, const_iterator last);
    constexpr void     swap(vector&)
      noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    constexpr void     clear() noexcept;
  };

  template<class InputIterator, class Allocator = allocator<iter-value-type<InputIterator>>>
    vector(InputIterator, InputIterator, Allocator = Allocator())
      -> vector<iter-value-type<InputIterator>, Allocator>;

  template<ranges::input_range R, class Allocator = allocator<ranges::range_value_t<R>>>
    vector(from_range_t, R&&, Allocator = Allocator())
      -> vector<ranges::range_value_t<R>, Allocator>;
}
```

An incomplete type `T` may be used when instantiating `vector` if the
allocator meets the allocator completeness requirements
[[allocator.requirements.completeness]]. `T` shall be complete before
any member of the resulting specialization of `vector` is referenced.

#### Constructors <a id="vector.cons">[[vector.cons]]</a>

``` cpp
constexpr explicit vector(const Allocator&) noexcept;
```

*Effects:* Constructs an empty `vector`, using the specified allocator.

*Complexity:* Constant.

``` cpp
constexpr explicit vector(size_type n, const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Effects:* Constructs a `vector` with `n` default-inserted elements
using the specified allocator.

*Complexity:* Linear in `n`.

``` cpp
constexpr vector(size_type n, const T& value,
                 const Allocator& = Allocator());
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* Constructs a `vector` with `n` copies of `value`, using the
specified allocator.

*Complexity:* Linear in `n`.

``` cpp
template<class InputIterator>
  constexpr vector(InputIterator first, InputIterator last,
                   const Allocator& = Allocator());
```

*Effects:* Constructs a `vector` equal to the range \[`first`, `last`),
using the specified allocator.

*Complexity:* Makes only N calls to the copy constructor of `T` (where N
is the distance between `first` and `last`) and no reallocations if
iterators `first` and `last` are of forward, bidirectional, or random
access categories. It makes order N calls to the copy constructor of `T`
and order log N reallocations if they are just input iterators.

``` cpp
template<container-compatible-range<T> R>
  constexpr vector(from_range_t, R&& rg, const Allocator& = Allocator());
```

*Effects:* Constructs a `vector` object with the elements of the range
`rg`, using the specified allocator.

*Complexity:* Initializes exactly N elements from the results of
dereferencing successive iterators of `rg`, where N is
`ranges::distance(rg)`. Performs no reallocations if `R` models
`ranges::forward_range` or `ranges::sized_range`; otherwise, performs
order log N reallocations and order N calls to the copy or move
constructor of `T`.

#### Capacity <a id="vector.capacity">[[vector.capacity]]</a>

``` cpp
constexpr size_type capacity() const noexcept;
```

*Returns:* The total number of elements that the vector can hold without
requiring reallocation.

*Complexity:* Constant time.

``` cpp
constexpr void reserve(size_type n);
```

*Preconditions:* `T` is *Cpp17MoveInsertable* into `*this`.

*Effects:* A directive that informs a `vector` of a planned change in
size, so that it can manage the storage allocation accordingly. After
`reserve()`, `capacity()` is greater or equal to the argument of
`reserve` if reallocation happens; and equal to the previous value of
`capacity()` otherwise. Reallocation happens at this point if and only
if the current capacity is less than the argument of `reserve()`. If an
exception is thrown other than by the move constructor of a
non-*Cpp17CopyInsertable* type, there are no effects.

*Throws:* `length_error` if `n > max_size()`.[^4]

*Complexity:* It does not change the size of the sequence and takes at
most linear time in the size of the sequence.

*Remarks:* Reallocation invalidates all the references, pointers, and
iterators referring to the elements in the sequence, as well as the
past-the-end iterator.

[*Note 1*: If no reallocation happens, they remain
valid. — *end note*]

No reallocation shall take place during insertions that happen after a
call to `reserve()` until an insertion would make the size of the vector
greater than the value of `capacity()`.

``` cpp
constexpr void shrink_to_fit();
```

*Preconditions:* `T` is *Cpp17MoveInsertable* into `*this`.

*Effects:* `shrink_to_fit` is a non-binding request to reduce
`capacity()` to `size()`.

[*Note 2*: The request is non-binding to allow latitude for
implementation-specific optimizations. — *end note*]

It does not increase `capacity()`, but may reduce `capacity()` by
causing reallocation. If an exception is thrown other than by the move
constructor of a non-*Cpp17CopyInsertable* `T` there are no effects.

*Complexity:* If reallocation happens, linear in the size of the
sequence.

*Remarks:* Reallocation invalidates all the references, pointers, and
iterators referring to the elements in the sequence as well as the
past-the-end iterator.

[*Note 3*: If no reallocation happens, they remain
valid. — *end note*]

``` cpp
constexpr void swap(vector& x)
  noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
           allocator_traits<Allocator>::is_always_equal::value);
```

*Effects:* Exchanges the contents and `capacity()` of `*this` with that
of `x`.

*Complexity:* Constant time.

``` cpp
constexpr void resize(size_type sz);
```

*Preconditions:* `T` is *Cpp17MoveInsertable* and
*Cpp17DefaultInsertable* into `*this`.

*Effects:* If `sz < size()`, erases the last `size() - sz` elements from
the sequence. Otherwise, appends `sz - size()` default-inserted elements
to the sequence.

*Remarks:* If an exception is thrown other than by the move constructor
of a non-*Cpp17CopyInsertable* `T` there are no effects.

``` cpp
constexpr void resize(size_type sz, const T& c);
```

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Effects:* If `sz < size()`, erases the last `size() - sz` elements from
the sequence. Otherwise, appends `sz - size()` copies of `c` to the
sequence.

*Remarks:* If an exception is thrown there are no effects.

#### Data <a id="vector.data">[[vector.data]]</a>

``` cpp
constexpr T*         data() noexcept;
constexpr const T*   data() const noexcept;
```

*Returns:* A pointer such that \[`data()`, `data() + size()`) is a valid
range. For a non-empty vector, `data()` `==` `addressof(front())`.

*Complexity:* Constant time.

#### Modifiers <a id="vector.modifiers">[[vector.modifiers]]</a>

``` cpp
constexpr iterator insert(const_iterator position, const T& x);
constexpr iterator insert(const_iterator position, T&& x);
constexpr iterator insert(const_iterator position, size_type n, const T& x);
template<class InputIterator>
  constexpr iterator insert(const_iterator position, InputIterator first, InputIterator last);
template<container-compatible-range<T> R>
  constexpr iterator insert_range(const_iterator position, R&& rg);
constexpr iterator insert(const_iterator position, initializer_list<T>);

template<class... Args> constexpr reference emplace_back(Args&&... args);
template<class... Args> constexpr iterator emplace(const_iterator position, Args&&... args);
constexpr void push_back(const T& x);
constexpr void push_back(T&& x);
template<container-compatible-range<T> R>
  constexpr void append_range(R&& rg);
```

*Complexity:* If reallocation happens, linear in the number of elements
of the resulting vector; otherwise, linear in the number of elements
inserted plus the distance to the end of the vector.

*Remarks:* Causes reallocation if the new size is greater than the old
capacity. Reallocation invalidates all the references, pointers, and
iterators referring to the elements in the sequence, as well as the
past-the-end iterator. If no reallocation happens, then references,
pointers, and iterators before the insertion point remain valid but
those at or after the insertion point, including the past-the-end
iterator, are invalidated. If an exception is thrown other than by the
copy constructor, move constructor, assignment operator, or move
assignment operator of `T` or by any `InputIterator` operation there are
no effects. If an exception is thrown while inserting a single element
at the end and `T` is *Cpp17CopyInsertable* or
`is_nothrow_move_constructible_v<T>` is `true`, there are no effects.
Otherwise, if an exception is thrown by the move constructor of a
non-*Cpp17CopyInsertable* `T`, the effects are unspecified.

``` cpp
constexpr iterator erase(const_iterator position);
constexpr iterator erase(const_iterator first, const_iterator last);
constexpr void pop_back();
```

*Effects:* Invalidates iterators and references at or after the point of
the erase.

*Throws:* Nothing unless an exception is thrown by the assignment
operator or move assignment operator of `T`.

*Complexity:* The destructor of `T` is called the number of times equal
to the number of the elements erased, but the assignment operator of `T`
is called the number of times equal to the number of elements in the
vector after the erased elements.

#### Erasure <a id="vector.erasure">[[vector.erasure]]</a>

``` cpp
template<class T, class Allocator, class U>
  constexpr typename vector<T, Allocator>::size_type
    erase(vector<T, Allocator>& c, const U& value);
```

*Effects:* Equivalent to:

``` cpp
auto it = remove(c.begin(), c.end(), value);
auto r = distance(it, c.end());
c.erase(it, c.end());
return r;
```

``` cpp
template<class T, class Allocator, class Predicate>
  constexpr typename vector<T, Allocator>::size_type
    erase_if(vector<T, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto it = remove_if(c.begin(), c.end(), pred);
auto r = distance(it, c.end());
c.erase(it, c.end());
return r;
```

### Specialization of `vector` for `bool` <a id="vector.bool">[[vector.bool]]</a>

#### Partial class template specialization `vector<bool, Allocator>` <a id="vector.bool.pspc">[[vector.bool.pspc]]</a>

To optimize space allocation, a partial specialization of `vector` for
`bool` elements is provided:

``` cpp
namespace std {
  template<class Allocator>
  class vector<bool, Allocator> {
  public:
    // types
    using value_type             = bool;
    using allocator_type         = Allocator;
    using pointer                = implementation-defined  // type of vector<bool>::pointer;
    using const_pointer          = implementation-defined  // type of vector<bool>::const_pointer;
    using const_reference        = bool;
    using size_type              = implementation-defined  // type of vector<bool>::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of vector<bool>::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of vector<bool>::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of vector<bool>::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;

    // bit reference
    class reference {
      friend class vector;
      constexpr reference() noexcept;

    public:
      constexpr reference(const reference&) = default;
      constexpr ~reference();
      constexpr operator bool() const noexcept;
      constexpr reference& operator=(bool x) noexcept;
      constexpr reference& operator=(const reference& x) noexcept;
      constexpr const reference& operator=(bool x) const noexcept;
      constexpr void flip() noexcept;   // flips the bit
    };

    // construct/copy/destroy
    constexpr vector() noexcept(noexcept(Allocator())) : vector(Allocator()) { }
    constexpr explicit vector(const Allocator&) noexcept;
    constexpr explicit vector(size_type n, const Allocator& = Allocator());
    constexpr vector(size_type n, const bool& value, const Allocator& = Allocator());
    template<class InputIterator>
      constexpr vector(InputIterator first, InputIterator last, const Allocator& = Allocator());
    template<container-compatible-range<bool> R>
      constexpr vector(from_range_t, R&& rg, const Allocator& = Allocator());
    constexpr vector(const vector& x);
    constexpr vector(vector&& x) noexcept;
    constexpr vector(const vector&, const type_identity_t<Allocator>&);
    constexpr vector(vector&&, const type_identity_t<Allocator>&);
    constexpr vector(initializer_list<bool>, const Allocator& = Allocator());
    constexpr ~vector();
    constexpr vector& operator=(const vector& x);
    constexpr vector& operator=(vector&& x)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    constexpr vector& operator=(initializer_list<bool>);
    template<class InputIterator>
      constexpr void assign(InputIterator first, InputIterator last);
    template<container-compatible-range<bool> R>
      constexpr void assign_range(R&& rg);
    constexpr void assign(size_type n, const bool& t);
    constexpr void assign(initializer_list<bool>);
    constexpr allocator_type get_allocator() const noexcept;

    // iterators
    constexpr iterator               begin() noexcept;
    constexpr const_iterator         begin() const noexcept;
    constexpr iterator               end() noexcept;
    constexpr const_iterator         end() const noexcept;
    constexpr reverse_iterator       rbegin() noexcept;
    constexpr const_reverse_iterator rbegin() const noexcept;
    constexpr reverse_iterator       rend() noexcept;
    constexpr const_reverse_iterator rend() const noexcept;

    constexpr const_iterator         cbegin() const noexcept;
    constexpr const_iterator         cend() const noexcept;
    constexpr const_reverse_iterator crbegin() const noexcept;
    constexpr const_reverse_iterator crend() const noexcept;

    // capacity
    [[nodiscard]] constexpr bool empty() const noexcept;
    constexpr size_type size() const noexcept;
    constexpr size_type max_size() const noexcept;
    constexpr size_type capacity() const noexcept;
    constexpr void      resize(size_type sz, bool c = false);
    constexpr void      reserve(size_type n);
    constexpr void      shrink_to_fit();

    // element access
    constexpr reference       operator[](size_type n);
    constexpr const_reference operator[](size_type n) const;
    constexpr const_reference at(size_type n) const;
    constexpr reference       at(size_type n);
    constexpr reference       front();
    constexpr const_reference front() const;
    constexpr reference       back();
    constexpr const_reference back() const;

    // modifiers
    template<class... Args> constexpr reference emplace_back(Args&&... args);
    constexpr void push_back(const bool& x);
    template<container-compatible-range<bool> R>
      constexpr void append_range(R&& rg);
    constexpr void pop_back();
    template<class... Args> constexpr iterator emplace(const_iterator position, Args&&... args);
    constexpr iterator insert(const_iterator position, const bool& x);
    constexpr iterator insert(const_iterator position, size_type n, const bool& x);
    template<class InputIterator>
      constexpr iterator insert(const_iterator position,
                                InputIterator first, InputIterator last);
    template<container-compatible-range<bool> R>
      constexpr iterator insert_range(const_iterator position, R&& rg);
    constexpr iterator insert(const_iterator position, initializer_list<bool> il);

    constexpr iterator erase(const_iterator position);
    constexpr iterator erase(const_iterator first, const_iterator last);
    constexpr void swap(vector&)
      noexcept(allocator_traits<Allocator>::propagate_on_container_swap::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    static constexpr void swap(reference x, reference y) noexcept;
    constexpr void flip() noexcept;     // flips all bits
    constexpr void clear() noexcept;
  };
}
```

Unless described below, all operations have the same requirements and
semantics as the primary `vector` template, except that operations
dealing with the `bool` value type map to bit values in the container
storage and `allocator_traits::construct` [[allocator.traits.members]]
is not used to construct these values.

There is no requirement that the data be stored as a contiguous
allocation of `bool` values. A space-optimized representation of bits is
recommended instead.

`reference`

is a class that simulates the behavior of references of a single bit in
`vector<bool>`. The conversion function returns `true` when the bit is
set, and `false` otherwise. The assignment operators set the bit when
the argument is (convertible to) `true` and clear it otherwise. `flip`
reverses the state of the bit.

``` cpp
constexpr void flip() noexcept;
```

*Effects:* Replaces each element in the container with its complement.

``` cpp
static constexpr void swap(reference x, reference y) noexcept;
```

*Effects:* Exchanges the contents of `x` and `y` as if by:

``` cpp
bool b = x;
x = y;
y = b;
```

``` cpp
template<class Allocator> struct hash<vector<bool, Allocator>>;
```

The specialization is enabled [[unord.hash]].

``` cpp
template<class T>
  constexpr bool is-vector-bool-reference = see below;
```

The expression *`is-vector-bool-reference`*`<T>` is `true` if `T`
denotes the type `vector<bool, Alloc>::reference` for some type `Alloc`
and `vector<bool, Alloc>` is not a program-defined specialization.

#### Formatter specialization for `vector<bool>` <a id="vector.bool.fmt">[[vector.bool.fmt]]</a>

``` cpp
namespace std {
  template<class T, class charT>
    requires is-vector-bool-reference<T>
  struct formatter<T, charT> {
  private:
    formatter<bool, charT> underlying_;       // exposition only

  public:
    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(const T& ref, FormatContext& ctx) const;
  };
}
```

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

Equivalent to: `return `*`underlying_`*`.parse(ctx);`

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(const T& ref, FormatContext& ctx) const;
```

Equivalent to: `return `*`underlying_`*`.format(ref, ctx);`

## Associative containers <a id="associative">[[associative]]</a>

### In general <a id="associative.general">[[associative.general]]</a>

The header `<map>` defines the class templates `map` and `multimap`; the
header `<set>` defines the class templates `set` and `multiset`.

The following exposition-only alias templates may appear in deduction
guides for associative containers:

``` cpp
template<class InputIterator>
  using iter-value-type =
    typename iterator_traits<InputIterator>::value_type;                // exposition only
template<class InputIterator>
  using iter-key-type = remove_const_t<
    tuple_element_t<0, iter-value-type<InputIterator>>>;                // exposition only
template<class InputIterator>
  using iter-mapped-type =
    tuple_element_t<1, iter-value-type<InputIterator>>;                 // exposition only
template<class InputIterator>
  using iter-to-alloc-type = pair<
    add_const_t<tuple_element_t<0, iter-value-type<InputIterator>>>,
    tuple_element_t<1, iter-value-type<InputIterator>>>;                // exposition only
template<ranges::input_range Range>
  using range-key-type =
    remove_const_t<typename ranges::range_value_t<Range>::first_type>;  // exposition only
template<ranges::input_range Range>
  using range-mapped-type = typename ranges::range_value_t<Range>::second_type; // exposition only
template<ranges::input_range Range>
  using range-to-alloc-type =
    pair<add_const_t<typename ranges::range_value_t<Range>::first_type>,
         typename ranges::range_value_t<Range>::second_type>;           // exposition only
```

### Header `<map>` synopsis <a id="associative.map.syn">[[associative.map.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [map], class template map
  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
    class map;

  template<class Key, class T, class Compare, class Allocator>
    bool operator==(const map<Key, T, Compare, Allocator>& x,
                    const map<Key, T, Compare, Allocator>& y);
  template<class Key, class T, class Compare, class Allocator>
    synth-three-way-result<pair<const Key, T>>
      operator<=>(const map<Key, T, Compare, Allocator>& x,
                  const map<Key, T, Compare, Allocator>& y);

  template<class Key, class T, class Compare, class Allocator>
    void swap(map<Key, T, Compare, Allocator>& x,
              map<Key, T, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [map.erasure], erasure for map
  template<class Key, class T, class Compare, class Allocator, class Predicate>
    typename map<Key, T, Compare, Allocator>::size_type
      erase_if(map<Key, T, Compare, Allocator>& c, Predicate pred);

  // [multimap], class template multimap
  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
    class multimap;

  template<class Key, class T, class Compare, class Allocator>
    bool operator==(const multimap<Key, T, Compare, Allocator>& x,
                    const multimap<Key, T, Compare, Allocator>& y);
  template<class Key, class T, class Compare, class Allocator>
    synth-three-way-result<pair<const Key, T>>
      operator<=>(const multimap<Key, T, Compare, Allocator>& x,
                  const multimap<Key, T, Compare, Allocator>& y);

  template<class Key, class T, class Compare, class Allocator>
    void swap(multimap<Key, T, Compare, Allocator>& x,
              multimap<Key, T, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [multimap.erasure], erasure for multimap
  template<class Key, class T, class Compare, class Allocator, class Predicate>
    typename multimap<Key, T, Compare, Allocator>::size_type
      erase_if(multimap<Key, T, Compare, Allocator>& c, Predicate pred);

  namespace pmr {
    template<class Key, class T, class Compare = less<Key>>
      using map = std::map<Key, T, Compare,
                           polymorphic_allocator<pair<const Key, T>>>;

    template<class Key, class T, class Compare = less<Key>>
      using multimap = std::multimap<Key, T, Compare,
                                     polymorphic_allocator<pair<const Key, T>>>;
  }
}
```

### Header `<set>` synopsis <a id="associative.set.syn">[[associative.set.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [set], class template set
  template<class Key, class Compare = less<Key>, class Allocator = allocator<Key>>
    class set;

  template<class Key, class Compare, class Allocator>
    bool operator==(const set<Key, Compare, Allocator>& x,
                    const set<Key, Compare, Allocator>& y);
  template<class Key, class Compare, class Allocator>
    synth-three-way-result<Key> operator<=>(const set<Key, Compare, Allocator>& x,
    \itcorr                                        const set<Key, Compare, Allocator>& y);

  template<class Key, class Compare, class Allocator>
    void swap(set<Key, Compare, Allocator>& x,
              set<Key, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [set.erasure], erasure for set
  template<class Key, class Compare, class Allocator, class Predicate>
    typename set<Key, Compare, Allocator>::size_type
      erase_if(set<Key, Compare, Allocator>& c, Predicate pred);

  // [multiset], class template multiset
  template<class Key, class Compare = less<Key>, class Allocator = allocator<Key>>
    class multiset;

  template<class Key, class Compare, class Allocator>
    bool operator==(const multiset<Key, Compare, Allocator>& x,
                    const multiset<Key, Compare, Allocator>& y);
  template<class Key, class Compare, class Allocator>
    synth-three-way-result<Key> operator<=>(const multiset<Key, Compare, Allocator>& x,
    \itcorr                                        const multiset<Key, Compare, Allocator>& y);

  template<class Key, class Compare, class Allocator>
    void swap(multiset<Key, Compare, Allocator>& x,
              multiset<Key, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

  // [multiset.erasure], erasure for multiset
  template<class Key, class Compare, class Allocator, class Predicate>
    typename multiset<Key, Compare, Allocator>::size_type
      erase_if(multiset<Key, Compare, Allocator>& c, Predicate pred);

  namespace pmr {
    template<class Key, class Compare = less<Key>>
      using set = std::set<Key, Compare, polymorphic_allocator<Key>>;

    template<class Key, class Compare = less<Key>>
      using multiset = std::multiset<Key, Compare, polymorphic_allocator<Key>>;
  }
}
```

### Class template `map` <a id="map">[[map]]</a>

#### Overview <a id="map.overview">[[map.overview]]</a>

A `map` is an associative container that supports unique keys (i.e.,
contains at most one of each key value) and provides for fast retrieval
of values of another type `T` based on the keys. The `map` class
supports bidirectional iterators.

A `map` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]]. and of an associative container
[[associative.reqmts]]. A `map` also provides most operations described
in  [[associative.reqmts]] for unique keys. This means that a `map`
supports the `a_uniq` operations in  [[associative.reqmts]] but not the
`a_eq` operations. For a `map<Key,T>` the `key_type` is `Key` and the
`value_type` is `pair<const Key,T>`. Descriptions are provided here only
for operations on `map` that are not described in one of those tables or
for operations where there is additional semantic information.

``` cpp
namespace std {
  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
  class map {
  public:
    // types
    using key_type               = Key;
    using mapped_type            = T;
    using value_type             = pair<const Key, T>;
    using key_compare            = Compare;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of map::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of map::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of map::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of map::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    using node_type              = unspecified;
    using insert_return_type     = insert-return-type<iterator, node_type>;

    class value_compare {
      friend class map;
    protected:
      Compare comp;
      value_compare(Compare c) : comp(c) {}

    public:
      bool operator()(const value_type& x, const value_type& y) const {
        return comp(x.first, y.first);
      }
    };

    // [map.cons], construct/copy/destroy
    map() : map(Compare()) { }
    explicit map(const Compare& comp, const Allocator& = Allocator());
    template<class InputIterator>
      map(InputIterator first, InputIterator last,
          const Compare& comp = Compare(), const Allocator& = Allocator());
    template<container-compatible-range<value_type> R>
      map(from_range_t, R&& rg, const Compare& comp = Compare(), const Allocator& = Allocator());
    map(const map& x);
    map(map&& x);
    explicit map(const Allocator&);
    map(const map&, const type_identity_t<Allocator>&);
    map(map&&, const type_identity_t<Allocator>&);
    map(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
    template<class InputIterator>
      map(InputIterator first, InputIterator last, const Allocator& a)
        : map(first, last, Compare(), a) { }
    template<container-compatible-range<value_type> R>
      map(from_range_t, R&& rg, const Allocator& a))
        : map(from_range, std::forward<R>(rg), Compare(), a) { }
    map(initializer_list<value_type> il, const Allocator& a)
      : map(il, Compare(), a) { }
    ~map();
    map& operator=(const map& x);
    map& operator=(map&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Compare>);
    map& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [map.access], element access
    mapped_type& operator[](const key_type& x);
    mapped_type& operator[](key_type&& x);
    mapped_type&       at(const key_type& x);
    const mapped_type& at(const key_type& x) const;

    // [map.modifiers], modifiers
    template<class... Args> pair<iterator, bool> emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator, bool> insert(const value_type& x);
    pair<iterator, bool> insert(value_type&& x);
    template<class P> pair<iterator, bool> insert(P&& x);
    iterator insert(const_iterator position, const value_type& x);
    iterator insert(const_iterator position, value_type&& x);
    template<class P>
      iterator insert(const_iterator position, P&&);
    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    insert_return_type insert(node_type&& nh);
    iterator           insert(const_iterator hint, node_type&& nh);

    template<class... Args>
      pair<iterator, bool> try_emplace(const key_type& k, Args&&... args);
    template<class... Args>
      pair<iterator, bool> try_emplace(key_type&& k, Args&&... args);
    template<class... Args>
      iterator try_emplace(const_iterator hint, const key_type& k, Args&&... args);
    template<class... Args>
      iterator try_emplace(const_iterator hint, key_type&& k, Args&&... args);
    template<class M>
      pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
    template<class M>
      pair<iterator, bool> insert_or_assign(key_type&& k, M&& obj);
    template<class M>
      iterator insert_or_assign(const_iterator hint, const key_type& k, M&& obj);
    template<class M>
      iterator insert_or_assign(const_iterator hint, key_type&& k, M&& obj);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(map&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Compare>);
    void      clear() noexcept;

    template<class C2>
      void merge(map<Key, T, C2, Allocator>& source);
    template<class C2>
      void merge(map<Key, T, C2, Allocator>&& source);
    template<class C2>
      void merge(multimap<Key, T, C2, Allocator>& source);
    template<class C2>
      void merge(multimap<Key, T, C2, Allocator>&& source);

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    // map operations
    iterator       find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator       find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type      count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool           contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator       lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator       lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator       upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator       upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator>               equal_range(const key_type& x);
    pair<const_iterator, const_iterator>   equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;
  };

  template<class InputIterator, class Compare = less<iter-key-type<InputIterator>>,
           class Allocator = allocator<iter-to-alloc-type<InputIterator>>>
    map(InputIterator, InputIterator, Compare = Compare(), Allocator = Allocator())
      -> map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Compare, Allocator>;

  template<ranges::input_range R, class Compare = less<range-key-type<R>,
           class Allocator = allocator<range-to-alloc-type<R>>>
    map(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> map<range-key-type<R>, range-mapped-type<R>, Compare, Allocator>;

  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
    map(initializer_list<pair<Key, T>>, Compare = Compare(), Allocator = Allocator())
      -> map<Key, T, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    map(InputIterator, InputIterator, Allocator)
      -> map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
             less<iter-key-type<InputIterator>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    map(from_range_t, R&&, Allocator)
      -> map<range-key-type<R>, range-mapped-type<R>, less<range-key-type<R>>, Allocator>;

  template<class Key, class T, class Allocator>
    map(initializer_list<pair<Key, T>>, Allocator) -> map<Key, T, less<Key>, Allocator>;
}
```

#### Constructors, copy, and assignment <a id="map.cons">[[map.cons]]</a>

``` cpp
explicit map(const Compare& comp, const Allocator& = Allocator());
```

*Effects:* Constructs an empty `map` using the specified comparison
object and allocator.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  map(InputIterator first, InputIterator last,
      const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `map` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted with respect to `comp` and otherwise N log N, where N is
`last - first`.

``` cpp
template<container-compatible-range<value_type> R>
  map(from_range_t, R&& rg, const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `map` using the specified comparison
object and allocator, and inserts elements from the range `rg`.

*Complexity:* Linear in N if `rg` is already sorted with respect to
`comp` and otherwise N log N, where N is `ranges::distance(rg)`.

#### Element access <a id="map.access">[[map.access]]</a>

``` cpp
mapped_type& operator[](const key_type& x);
```

*Effects:* Equivalent to: `return try_emplace(x).first->second;`

``` cpp
mapped_type& operator[](key_type&& x);
```

*Effects:* Equivalent to:
`return try_emplace(std::move(x)).first->second;`

``` cpp
mapped_type&       at(const key_type& x);
const mapped_type& at(const key_type& x) const;
```

*Returns:* A reference to the `mapped_type` corresponding to `x` in
`*this`.

*Throws:* An exception object of type `out_of_range` if no such element
is present.

*Complexity:* Logarithmic.

#### Modifiers <a id="map.modifiers">[[map.modifiers]]</a>

``` cpp
template<class P>
  pair<iterator, bool> insert(P&& x);
template<class P>
  iterator insert(const_iterator position, P&& x);
```

*Constraints:* `is_constructible_v<value_type, P&&>` is `true`.

*Effects:* The first form is equivalent to
`return emplace(std::forward<P>(x))`. The second form is equivalent to
`return emplace_hint(position, std::forward<P>(x))`.

``` cpp
template<class... Args>
  pair<iterator, bool> try_emplace(const key_type& k, Args&&... args);
template<class... Args>
  iterator try_emplace(const_iterator hint, const key_type& k, Args&&... args);
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `map`
from `piecewise_construct`, `forward_as_tuple(k)`,
`forward_as_tuple(std::forward<Args>(args)...)`.

*Effects:* If the map already contains an element whose key is
equivalent to `k`, there is no effect. Otherwise inserts an object of
type `value_type` constructed with `piecewise_construct`,
`forward_as_tuple(k)`, `forward_as_tuple(std::forward<Args>(args)...)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class... Args>
  pair<iterator, bool> try_emplace(key_type&& k, Args&&... args);
template<class... Args>
  iterator try_emplace(const_iterator hint, key_type&& k, Args&&... args);
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `map`
from `piecewise_construct`, `forward_as_tuple(std::move(k))`,
`forward_as_tuple(std::forward<Args>(args)...)`.

*Effects:* If the map already contains an element whose key is
equivalent to `k`, there is no effect. Otherwise inserts an object of
type `value_type` constructed with `piecewise_construct`,
`forward_as_tuple(std::move(k))`,
`forward_as_tuple(std::forward<Args>(args)...)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class M>
  pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
template<class M>
  iterator insert_or_assign(const_iterator hint, const key_type& k, M&& obj);
```

*Mandates:* `is_assignable_v<mapped_type&, M&&>` is `true`.

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `map`
from `k`, `std::forward<M>(obj)`.

*Effects:* If the map already contains an element `e` whose key is
equivalent to `k`, assigns `std::forward<M>(obj)` to `e.second`.
Otherwise inserts an object of type `value_type` constructed with `k`,
`std::forward<M>(obj)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class M>
  pair<iterator, bool> insert_or_assign(key_type&& k, M&& obj);
template<class M>
  iterator insert_or_assign(const_iterator hint, key_type&& k, M&& obj);
```

*Mandates:* `is_assignable_v<mapped_type&, M&&>` is `true`.

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into `map`
from `std::move(k)`, `std::forward<M>(obj)`.

*Effects:* If the map already contains an element `e` whose key is
equivalent to `k`, assigns `std::forward<M>(obj)` to `e.second`.
Otherwise inserts an object of type `value_type` constructed with
`std::move(k)`, `std::forward<M>(obj)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

#### Erasure <a id="map.erasure">[[map.erasure]]</a>

``` cpp
template<class Key, class T, class Compare, class Allocator, class Predicate>
  typename map<Key, T, Compare, Allocator>::size_type
    erase_if(map<Key, T, Compare, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

### Class template `multimap` <a id="multimap">[[multimap]]</a>

#### Overview <a id="multimap.overview">[[multimap.overview]]</a>

A `multimap` is an associative container that supports equivalent keys
(i.e., possibly containing multiple copies of the same key value) and
provides for fast retrieval of values of another type `T` based on the
keys. The `multimap` class supports bidirectional iterators.

A `multimap` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], and of an associative container
[[associative.reqmts]]. A `multimap` also provides most operations
described in  [[associative.reqmts]] for equal keys. This means that a
`multimap` supports the `a_eq` operations in  [[associative.reqmts]] but
not the `a_uniq` operations. For a `multimap<Key,T>` the `key_type` is
`Key` and the `value_type` is `pair<const Key,T>`. Descriptions are
provided here only for operations on `multimap` that are not described
in one of those tables or for operations where there is additional
semantic information.

``` cpp
namespace std {
  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
  class multimap {
  public:
    // types
    using key_type               = Key;
    using mapped_type            = T;
    using value_type             = pair<const Key, T>;
    using key_compare            = Compare;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of multimap::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of multimap::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of multimap::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of multimap::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    using node_type              = unspecified;

    class value_compare {
      friend class multimap;
    protected:
      Compare comp;
      value_compare(Compare c) : comp(c) { }

    public:
      bool operator()(const value_type& x, const value_type& y) const {
        return comp(x.first, y.first);
      }
    };

    // [multimap.cons], construct/copy/destroy
    multimap() : multimap(Compare()) { }
    explicit multimap(const Compare& comp, const Allocator& = Allocator());
    template<class InputIterator>
      multimap(InputIterator first, InputIterator last,
               const Compare& comp = Compare(),
               const Allocator& = Allocator());
    template<container-compatible-range<value_type> R>
      multimap(from_range_t, R&& rg,
               const Compare& comp = Compare(), const Allocator& = Allocator());
    multimap(const multimap& x);
    multimap(multimap&& x);
    explicit multimap(const Allocator&);
    multimap(const multimap&, const type_identity_t<Allocator>&);
    multimap(multimap&&, const type_identity_t<Allocator>&);
    multimap(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
    template<class InputIterator>
      multimap(InputIterator first, InputIterator last, const Allocator& a)
        : multimap(first, last, Compare(), a) { }
    template<container-compatible-range<value_type> R>
      multimap(from_range_t, R&& rg, const Allocator& a))
        : multimap(from_range, std::forward<R>(rg), Compare(), a) { }
    multimap(initializer_list<value_type> il, const Allocator& a)
      : multimap(il, Compare(), a) { }
    ~multimap();
    multimap& operator=(const multimap& x);
    multimap& operator=(multimap&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Compare>);
    multimap& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [multimap.modifiers], modifiers
    template<class... Args> iterator emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& x);
    iterator insert(value_type&& x);
    template<class P> iterator insert(P&& x);
    iterator insert(const_iterator position, const value_type& x);
    iterator insert(const_iterator position, value_type&& x);
    template<class P> iterator insert(const_iterator position, P&& x);
    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(multimap&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Compare>);
    void      clear() noexcept;

    template<class C2>
      void merge(multimap<Key, T, C2, Allocator>& source);
    template<class C2>
      void merge(multimap<Key, T, C2, Allocator>&& source);
    template<class C2>
      void merge(map<Key, T, C2, Allocator>& source);
    template<class C2>
      void merge(map<Key, T, C2, Allocator>&& source);

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    // map operations
    iterator       find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator       find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type      count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool           contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator       lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator       lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator       upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator       upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator>               equal_range(const key_type& x);
    pair<const_iterator, const_iterator>   equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;
  };

  template<class InputIterator, class Compare = less<iter-key-type<InputIterator>>,
           class Allocator = allocator<iter-to-alloc-type<InputIterator>>>
    multimap(InputIterator, InputIterator, Compare = Compare(), Allocator = Allocator())
      -> multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                  Compare, Allocator>;

  template<ranges::input_range R, class Compare = less<range-key-type<R>>,
           class Allocator = allocator<range-to-alloc-type<R>>>
    multimap(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> multimap<range-key-type<R>, range-mapped-type<R>, Compare, Allocator>;

  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
    multimap(initializer_list<pair<Key, T>>, Compare = Compare(), Allocator = Allocator())
      -> multimap<Key, T, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    multimap(InputIterator, InputIterator, Allocator)
      -> multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                  less<iter-key-type<InputIterator>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    multimap(from_range_t, R&&, Allocator)
      -> multimap<range-key-type<R>, range-mapped-type<R>, less<range-key-type<R>>, Allocator>;

  template<class Key, class T, class Allocator>
    multimap(initializer_list<pair<Key, T>>, Allocator)
      -> multimap<Key, T, less<Key>, Allocator>;
}
```

#### Constructors <a id="multimap.cons">[[multimap.cons]]</a>

``` cpp
explicit multimap(const Compare& comp, const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multimap` using the specified comparison
object and allocator.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  multimap(InputIterator first, InputIterator last,
           const Compare& comp = Compare(),
           const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multimap` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted with respect to `comp` and otherwise N log N, where N is
`last - first`.

``` cpp
template<container-compatible-range<value_type> R>
  multimap(from_range_t, R&& rg, const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multimap` using the specified comparison
object and allocator, and inserts elements from the range `rg`.

*Complexity:* Linear in N if `rg` is already sorted with respect to
`comp` and otherwise N log N, where N is `ranges::distance(rg)`.

#### Modifiers <a id="multimap.modifiers">[[multimap.modifiers]]</a>

``` cpp
template<class P> iterator insert(P&& x);
template<class P> iterator insert(const_iterator position, P&& x);
```

*Constraints:* `is_constructible_v<value_type, P&&>` is `true`.

*Effects:* The first form is equivalent to
`return emplace(std::forward<P>(x))`. The second form is equivalent to
`return emplace_hint(position, std::forward<P>(x))`.

#### Erasure <a id="multimap.erasure">[[multimap.erasure]]</a>

``` cpp
template<class Key, class T, class Compare, class Allocator, class Predicate>
  typename multimap<Key, T, Compare, Allocator>::size_type
    erase_if(multimap<Key, T, Compare, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

### Class template `set` <a id="set">[[set]]</a>

#### Overview <a id="set.overview">[[set.overview]]</a>

A `set` is an associative container that supports unique keys (i.e.,
contains at most one of each key value) and provides for fast retrieval
of the keys themselves. The `set` class supports bidirectional
iterators.

A `set` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]]. and of an associative container
[[associative.reqmts]]. A `set` also provides most operations described
in  [[associative.reqmts]] for unique keys. This means that a `set`
supports the `a_uniq` operations in  [[associative.reqmts]] but not the
`a_eq` operations. For a `set<Key>` both the `key_type` and `value_type`
are `Key`. Descriptions are provided here only for operations on `set`
that are not described in one of these tables and for operations where
there is additional semantic information.

``` cpp
namespace std {
  template<class Key, class Compare = less<Key>,
           class Allocator = allocator<Key>>
  class set {
  public:
    // types
    using key_type               = Key;
    using key_compare            = Compare;
    using value_type             = Key;
    using value_compare          = Compare;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of set::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of set::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of set::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of set::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    using node_type              = unspecified;
    using insert_return_type     = insert-return-type<iterator, node_type>;

    // [set.cons], construct/copy/destroy
    set() : set(Compare()) { }
    explicit set(const Compare& comp, const Allocator& = Allocator());
    template<class InputIterator>
      set(InputIterator first, InputIterator last,
          const Compare& comp = Compare(), const Allocator& = Allocator());
    template<container-compatible-range<value_type> R>
      set(from_range_t, R&& rg, const Compare& comp = Compare(), const Allocator& = Allocator());
    set(const set& x);
    set(set&& x);
    explicit set(const Allocator&);
    set(const set&, const type_identity_t<Allocator>&);
    set(set&&, const type_identity_t<Allocator>&);
    set(initializer_list<value_type>, const Compare& = Compare(),
        const Allocator& = Allocator());
    template<class InputIterator>
      set(InputIterator first, InputIterator last, const Allocator& a)
        : set(first, last, Compare(), a) { }
    template<container-compatible-range<value_type> R>
      set(from_range_t, R&& rg, const Allocator& a))
        : set(from_range, std::forward<R>(rg), Compare(), a) { }
    set(initializer_list<value_type> il, const Allocator& a)
      : set(il, Compare(), a) { }
    ~set();
    set& operator=(const set& x);
    set& operator=(set&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Compare>);
    set& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // modifiers
    template<class... Args> pair<iterator, bool> emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator,bool> insert(const value_type& x);
    pair<iterator,bool> insert(value_type&& x);
    iterator insert(const_iterator position, const value_type& x);
    iterator insert(const_iterator position, value_type&& x);
    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    insert_return_type insert(node_type&& nh);
    iterator           insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position)
      requires (!same_as<iterator, const_iterator>);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(set&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Compare>);
    void      clear() noexcept;

    template<class C2>
      void merge(set<Key, C2, Allocator>& source);
    template<class C2>
      void merge(set<Key, C2, Allocator>&& source);
    template<class C2>
      void merge(multiset<Key, C2, Allocator>& source);
    template<class C2>
      void merge(multiset<Key, C2, Allocator>&& source);

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    // set operations
    iterator       find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator       find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type      count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool           contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator       lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator       lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator       upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator       upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator>               equal_range(const key_type& x);
    pair<const_iterator, const_iterator>   equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;
  };

  template<class InputIterator,
           class Compare = less<iter-value-type<InputIterator>>,
           class Allocator = allocator<iter-value-type<InputIterator>>>
    set(InputIterator, InputIterator,
        Compare = Compare(), Allocator = Allocator())
      -> set<iter-value-type<InputIterator>, Compare, Allocator>;

  template<ranges::input_range R, class Compare = less<ranges::range_value_t<R>>,
           class Allocator = allocator<ranges::range_value_t<R>>>
    set(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> set<ranges::range_value_t<R>, Compare, Allocator>;

  template<class Key, class Compare = less<Key>, class Allocator = allocator<Key>>
    set(initializer_list<Key>, Compare = Compare(), Allocator = Allocator())
      -> set<Key, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    set(InputIterator, InputIterator, Allocator)
      -> set<iter-value-type<InputIterator>,
             less<iter-value-type<InputIterator>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    set(from_range_t, R&&, Allocator)
      -> set<ranges::range_value_t<R>, less<ranges::range_value_t<R>>, Allocator>;

  template<class Key, class Allocator>
    set(initializer_list<Key>, Allocator) -> set<Key, less<Key>, Allocator>;
}
```

#### Constructors, copy, and assignment <a id="set.cons">[[set.cons]]</a>

``` cpp
explicit set(const Compare& comp, const Allocator& = Allocator());
```

*Effects:* Constructs an empty `set` using the specified comparison
object and allocator.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  set(InputIterator first, InputIterator last,
      const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `set` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted with respect to `comp` and otherwise N log N, where N is
`last - first`.

``` cpp
template<container-compatible-range<value_type> R>
  set(from_range_t, R&& rg, const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `set` using the specified comparison
object and allocator, and inserts elements from the range `rg`.

*Complexity:* Linear in N if `rg` is already sorted with respect to
`comp` and otherwise N log N, where N is `ranges::distance(rg)`.

#### Erasure <a id="set.erasure">[[set.erasure]]</a>

``` cpp
template<class Key, class Compare, class Allocator, class Predicate>
  typename set<Key, Compare, Allocator>::size_type
    erase_if(set<Key, Compare, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

### Class template `multiset` <a id="multiset">[[multiset]]</a>

#### Overview <a id="multiset.overview">[[multiset.overview]]</a>

A `multiset` is an associative container that supports equivalent keys
(i.e., possibly contains multiple copies of the same key value) and
provides for fast retrieval of the keys themselves. The `multiset` class
supports bidirectional iterators.

A `multiset` meets all of the requirements of a container
[[container.reqmts]], of a reversible container
[[container.rev.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], of an associative container
[[associative.reqmts]]. `multiset` also provides most operations
described in  [[associative.reqmts]] for duplicate keys. This means that
a `multiset` supports the `a_eq` operations in  [[associative.reqmts]]
but not the `a_uniq` operations. For a `multiset<Key>` both the
`key_type` and `value_type` are `Key`. Descriptions are provided here
only for operations on `multiset` that are not described in one of these
tables and for operations where there is additional semantic
information.

``` cpp
namespace std {
  template<class Key, class Compare = less<Key>,
           class Allocator = allocator<Key>>
  class multiset {
  public:
    // types
    using key_type               = Key;
    using key_compare            = Compare;
    using value_type             = Key;
    using value_compare          = Compare;
    using allocator_type         = Allocator;
    using pointer                = typename allocator_traits<Allocator>::pointer;
    using const_pointer          = typename allocator_traits<Allocator>::const_pointer;
    using reference              = value_type&;
    using const_reference        = const value_type&;
    using size_type              = implementation-defined  // type of multiset::size_type; // see [container.requirements]
    using difference_type        = implementation-defined  // type of multiset::difference_type; // see [container.requirements]
    using iterator               = implementation-defined  // type of multiset::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of multiset::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    using node_type              = unspecified;

    // [multiset.cons], construct/copy/destroy
    multiset() : multiset(Compare()) { }
    explicit multiset(const Compare& comp, const Allocator& = Allocator());
    template<class InputIterator>
      multiset(InputIterator first, InputIterator last,
               const Compare& comp = Compare(), const Allocator& = Allocator());
    template<container-compatible-range<value_type> R>
      multiset(from_range_t, R&& rg,
               const Compare& comp = Compare(), const Allocator& = Allocator());
    multiset(const multiset& x);
    multiset(multiset&& x);
    explicit multiset(const Allocator&);
    multiset(const multiset&, const type_identity_t<Allocator>&);
    multiset(multiset&&, const type_identity_t<Allocator>&);
    multiset(initializer_list<value_type>, const Compare& = Compare(),
             const Allocator& = Allocator());
    template<class InputIterator>
      multiset(InputIterator first, InputIterator last, const Allocator& a)
        : multiset(first, last, Compare(), a) { }
    template<container-compatible-range<value_type> R>
      multiset(from_range_t, R&& rg, const Allocator& a))
        : multiset(from_range, std::forward<R>(rg), Compare(), a) { }
    multiset(initializer_list<value_type> il, const Allocator& a)
      : multiset(il, Compare(), a) { }
    ~multiset();
    multiset& operator=(const multiset& x);
    multiset& operator=(multiset&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Compare>);
    multiset& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // modifiers
    template<class... Args> iterator emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& x);
    iterator insert(value_type&& x);
    iterator insert(const_iterator position, const value_type& x);
    iterator insert(const_iterator position, value_type&& x);
    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position)
      requires (!same_as<iterator, const_iterator>);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(multiset&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Compare>);
    void      clear() noexcept;

    template<class C2>
      void merge(multiset<Key, C2, Allocator>& source);
    template<class C2>
      void merge(multiset<Key, C2, Allocator>&& source);
    template<class C2>
      void merge(set<Key, C2, Allocator>& source);
    template<class C2>
      void merge(set<Key, C2, Allocator>&& source);

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    // set operations
    iterator       find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator       find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type      count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool           contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator       lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator       lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator       upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator       upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator>               equal_range(const key_type& x);
    pair<const_iterator, const_iterator>   equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;
  };

  template<class InputIterator,
           class Compare = less<iter-value-type<InputIterator>>,
           class Allocator = allocator<iter-value-type<InputIterator>>>
    multiset(InputIterator, InputIterator,
             Compare = Compare(), Allocator = Allocator())
      -> multiset<iter-value-type<InputIterator>, Compare, Allocator>;

  template<ranges::input_range R, class Compare = less<ranges::range_value_t<R>>,
           class Allocator = allocator<ranges::range_value_t<R>>>
    multiset(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> multiset<ranges::range_value_t<R>, Compare, Allocator>;

  template<class Key, class Compare = less<Key>, class Allocator = allocator<Key>>
    multiset(initializer_list<Key>, Compare = Compare(), Allocator = Allocator())
      -> multiset<Key, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    multiset(InputIterator, InputIterator, Allocator)
      -> multiset<iter-value-type<InputIterator>,
                  less<iter-value-type<InputIterator>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    multiset(from_range_t, R&&, Allocator)
      -> multiset<ranges::range_value_t<R>, less<ranges::range_value_t<R>>, Allocator>;

  template<class Key, class Allocator>
    multiset(initializer_list<Key>, Allocator) -> multiset<Key, less<Key>, Allocator>;
}
```

#### Constructors <a id="multiset.cons">[[multiset.cons]]</a>

``` cpp
explicit multiset(const Compare& comp, const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multiset` using the specified comparison
object and allocator.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  multiset(InputIterator first, InputIterator last,
           const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multiset` using the specified comparison
object and allocator, and inserts elements from the range \[`first`,
`last`).

*Complexity:* Linear in N if the range \[`first`, `last`) is already
sorted with respect to `comp` and otherwise N log N, where N is
`last - first`.

``` cpp
template<container-compatible-range<value_type> R>
  multiset(from_range_t, R&& rg, const Compare& comp = Compare(), const Allocator& = Allocator());
```

*Effects:* Constructs an empty `multiset` using the specified comparison
object and allocator, and inserts elements from the range `rg`.

*Complexity:* Linear in N if `rg` is already sorted with respect to
`comp` and otherwise N log N, where N is `ranges::distance(rg)`.

#### Erasure <a id="multiset.erasure">[[multiset.erasure]]</a>

``` cpp
template<class Key, class Compare, class Allocator, class Predicate>
  typename multiset<Key, Compare, Allocator>::size_type
    erase_if(multiset<Key, Compare, Allocator>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

## Unordered associative containers <a id="unord">[[unord]]</a>

### In general <a id="unord.general">[[unord.general]]</a>

The header `<unordered_map>` defines the class templates `unordered_map`
and `unordered_multimap`; the header `<unordered_set>` defines the class
templates `unordered_set` and `unordered_multiset`.

The exposition-only alias templates *iter-value-type*, *iter-key-type*,
*iter-mapped-type*, *iter-to-alloc-type*, *range-key-type*,
*range-mapped-type*, and *range-to-alloc-type* defined in
[[associative.general]] may appear in deduction guides for unordered
containers.

### Header `<unordered_map>` synopsis <a id="unord.map.syn">[[unord.map.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [unord.map], class template unordered_map
  template<class Key,
           class T,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Alloc = allocator<pair<const Key, T>>>
    class unordered_map;

  // [unord.multimap], class template unordered_multimap
  template<class Key,
           class T,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Alloc = allocator<pair<const Key, T>>>
    class unordered_multimap;

  template<class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_map<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_map<Key, T, Hash, Pred, Alloc>& b);

  template<class Key, class T, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_multimap<Key, T, Hash, Pred, Alloc>& a,
                    const unordered_multimap<Key, T, Hash, Pred, Alloc>& b);

  template<class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_map<Key, T, Hash, Pred, Alloc>& x,
              unordered_map<Key, T, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));

  template<class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_multimap<Key, T, Hash, Pred, Alloc>& x,
              unordered_multimap<Key, T, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));

  // [unord.map.erasure], erasure for unordered_map
  template<class K, class T, class H, class P, class A, class Predicate>
    typename unordered_map<K, T, H, P, A>::size_type
      erase_if(unordered_map<K, T, H, P, A>& c, Predicate pred);

  // [unord.multimap.erasure], erasure for unordered_multimap
  template<class K, class T, class H, class P, class A, class Predicate>
    typename unordered_multimap<K, T, H, P, A>::size_type
      erase_if(unordered_multimap<K, T, H, P, A>& c, Predicate pred);

  namespace pmr {
    template<class Key,
             class T,
             class Hash = hash<Key>,
             class Pred = equal_to<Key>>
      using unordered_map =
        std::unordered_map<Key, T, Hash, Pred,
                           polymorphic_allocator<pair<const Key, T>>>;
    template<class Key,
             class T,
             class Hash = hash<Key>,
             class Pred = equal_to<Key>>
      using unordered_multimap =
        std::unordered_multimap<Key, T, Hash, Pred,
                                polymorphic_allocator<pair<const Key, T>>>;

  }
}
```

### Header `<unordered_set>` synopsis <a id="unord.set.syn">[[unord.set.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [unord.set], class template unordered_set
  template<class Key,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Alloc = allocator<Key>>
    class unordered_set;

  // [unord.multiset], class template unordered_multiset
  template<class Key,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Alloc = allocator<Key>>
    class unordered_multiset;

  template<class Key, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_set<Key, Hash, Pred, Alloc>& a,
                    const unordered_set<Key, Hash, Pred, Alloc>& b);

  template<class Key, class Hash, class Pred, class Alloc>
    bool operator==(const unordered_multiset<Key, Hash, Pred, Alloc>& a,
                    const unordered_multiset<Key, Hash, Pred, Alloc>& b);

  template<class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_set<Key, Hash, Pred, Alloc>& x,
              unordered_set<Key, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));

  template<class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_multiset<Key, Hash, Pred, Alloc>& x,
              unordered_multiset<Key, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));

  // [unord.set.erasure], erasure for unordered_set
  template<class K, class H, class P, class A, class Predicate>
    typename unordered_set<K, H, P, A>::size_type
      erase_if(unordered_set<K, H, P, A>& c, Predicate pred);

  // [unord.multiset.erasure], erasure for unordered_multiset
  template<class K, class H, class P, class A, class Predicate>
    typename unordered_multiset<K, H, P, A>::size_type
      erase_if(unordered_multiset<K, H, P, A>& c, Predicate pred);

  namespace pmr {
    template<class Key,
             class Hash = hash<Key>,
             class Pred = equal_to<Key>>
      using unordered_set = std::unordered_set<Key, Hash, Pred,
                                               polymorphic_allocator<Key>>;

    template<class Key,
             class Hash = hash<Key>,
             class Pred = equal_to<Key>>
      using unordered_multiset = std::unordered_multiset<Key, Hash, Pred,
                                                         polymorphic_allocator<Key>>;
  }
}
```

### Class template `unordered_map` <a id="unord.map">[[unord.map]]</a>

#### Overview <a id="unord.map.overview">[[unord.map.overview]]</a>

An `unordered_map` is an unordered associative container that supports
unique keys (an `unordered_map` contains at most one of each key value)
and that associates values of another type `mapped_type` with the keys.
The `unordered_map` class supports forward iterators.

An `unordered_map` meets all of the requirements of a container
[[container.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], and of an unordered associative container
[[unord.req]]. It provides the operations described in the preceding
requirements table for unique keys; that is, an `unordered_map` supports
the `a_uniq` operations in that table, not the `a_eq` operations. For an
`unordered_map<Key, T>` the `key_type` is `Key`, the `mapped_type` is
`T`, and the `value_type` is `pair<const Key, T>`.

Subclause  [[unord.map]] only describes operations on `unordered_map`
that are not described in one of the requirement tables, or for which
there is additional semantic information.

``` cpp
namespace std {
  template<class Key,
           class T,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Allocator = allocator<pair<const Key, T>>>
  class unordered_map {
  public:
    // types
    using key_type             = Key;
    using mapped_type          = T;
    using value_type           = pair<const Key, T>;
    using hasher               = Hash;
    using key_equal            = Pred;
    using allocator_type       = Allocator;
    using pointer              = typename allocator_traits<Allocator>::pointer;
    using const_pointer        = typename allocator_traits<Allocator>::const_pointer;
    using reference            = value_type&;
    using const_reference      = const value_type&;
    using size_type            = implementation-defined  // type of unordered_map::size_type; // see [container.requirements]
    using difference_type      = implementation-defined  // type of unordered_map::difference_type; // see [container.requirements]

    using iterator             = implementation-defined  // type of unordered_map::iterator; // see [container.requirements]
    using const_iterator       = implementation-defined  // type of unordered_map::const_iterator; // see [container.requirements]
    using local_iterator       = implementation-defined  // type of unordered_map::local_iterator; // see [container.requirements]
    using const_local_iterator = implementation-defined  // type of unordered_map::const_local_iterator; // see [container.requirements]
    using node_type            = unspecified;
    using insert_return_type   = insert-return-type<iterator, node_type>;

    // [unord.map.cnstr], construct/copy/destroy
    unordered_map();
    explicit unordered_map(size_type n,
                           const hasher& hf = hasher(),
                           const key_equal& eql = key_equal(),
                           const allocator_type& a = allocator_type());
    template<class InputIterator>
      unordered_map(InputIterator f, InputIterator l,
                    size_type n = see below,
                    const hasher& hf = hasher(),
                    const key_equal& eql = key_equal(),
                    const allocator_type& a = allocator_type());

    template<container-compatible-range<value_type> R>
      unordered_map(from_range_t, R&& rg, size_type n = see below,
        const hasher& hf = hasher(), const key_equal& eql = key_equal(),
        const allocator_type& a = allocator_type());
    unordered_map(const unordered_map&);
    unordered_map(unordered_map&&);
    explicit unordered_map(const Allocator&);
    unordered_map(const unordered_map&, const type_identity_t<Allocator>&);
    unordered_map(unordered_map&&, const type_identity_t<Allocator>&);
    unordered_map(initializer_list<value_type> il,
                  size_type n = see below,
                  const hasher& hf = hasher(),
                  const key_equal& eql = key_equal(),
                  const allocator_type& a = allocator_type());
    unordered_map(size_type n, const allocator_type& a)
      : unordered_map(n, hasher(), key_equal(), a) { }
    unordered_map(size_type n, const hasher& hf, const allocator_type& a)
      : unordered_map(n, hf, key_equal(), a) { }
    template<class InputIterator>
      unordered_map(InputIterator f, InputIterator l, size_type n, const allocator_type& a)
        : unordered_map(f, l, n, hasher(), key_equal(), a) { }
    template<class InputIterator>
      unordered_map(InputIterator f, InputIterator l, size_type n, const hasher& hf,
                    const allocator_type& a)
        : unordered_map(f, l, n, hf, key_equal(), a) { }
    template<container-compatible-range<value_type> R>
      unordered_map(from_range_t, R&& rg, size_type n, const allocator_type& a)
        : unordered_map(from_range, std::forward<R>(rg), n, hasher(), key_equal(), a) { }
    template<container-compatible-range<value_type> R>
      unordered_map(from_range_t, R&& rg, size_type n, const hasher& hf, const allocator_type& a)
        : unordered_map(from_range, std::forward<R>(rg), n, hf, key_equal(), a) { }
    unordered_map(initializer_list<value_type> il, size_type n, const allocator_type& a)
      : unordered_map(il, n, hasher(), key_equal(), a) { }
    unordered_map(initializer_list<value_type> il, size_type n, const hasher& hf,
                  const allocator_type& a)
      : unordered_map(il, n, hf, key_equal(), a) { }
    ~unordered_map();
    unordered_map& operator=(const unordered_map&);
    unordered_map& operator=(unordered_map&&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Hash> &&
               is_nothrow_move_assignable_v<Pred>);
    unordered_map& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [unord.map.modifiers], modifiers
    template<class... Args> pair<iterator, bool> emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator, bool> insert(const value_type& obj);
    pair<iterator, bool> insert(value_type&& obj);
    template<class P> pair<iterator, bool> insert(P&& obj);
    iterator       insert(const_iterator hint, const value_type& obj);
    iterator       insert(const_iterator hint, value_type&& obj);
    template<class P> iterator insert(const_iterator hint, P&& obj);
    template<class InputIterator> void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    insert_return_type insert(node_type&& nh);
    iterator           insert(const_iterator hint, node_type&& nh);

    template<class... Args>
      pair<iterator, bool> try_emplace(const key_type& k, Args&&... args);
    template<class... Args>
      pair<iterator, bool> try_emplace(key_type&& k, Args&&... args);
    template<class... Args>
      iterator try_emplace(const_iterator hint, const key_type& k, Args&&... args);
    template<class... Args>
      iterator try_emplace(const_iterator hint, key_type&& k, Args&&... args);
    template<class M>
      pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
    template<class M>
      pair<iterator, bool> insert_or_assign(key_type&& k, M&& obj);
    template<class M>
      iterator insert_or_assign(const_iterator hint, const key_type& k, M&& obj);
    template<class M>
      iterator insert_or_assign(const_iterator hint, key_type&& k, M&& obj);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(unordered_map&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Hash> &&
               is_nothrow_swappable_v<Pred>);
    void      clear() noexcept;

    template<class H2, class P2>
      void merge(unordered_map<Key, T, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_map<Key, T, H2, P2, Allocator>&& source);
    template<class H2, class P2>
      void merge(unordered_multimap<Key, T, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_multimap<Key, T, H2, P2, Allocator>&& source);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // map operations
    iterator         find(const key_type& k);
    const_iterator   find(const key_type& k) const;
    template<class K>
      iterator       find(const K& k);
    template<class K>
      const_iterator find(const K& k) const;
    size_type        count(const key_type& k) const;
    template<class K>
      size_type      count(const K& k) const;
    bool             contains(const key_type& k) const;
    template<class K>
      bool           contains(const K& k) const;
    pair<iterator, iterator>               equal_range(const key_type& k);
    pair<const_iterator, const_iterator>   equal_range(const key_type& k) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& k);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& k) const;

    // [unord.map.elem], element access
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

  template<class InputIterator,
           class Hash = hash<iter-key-type<InputIterator>>,
           class Pred = equal_to<iter-key-type<InputIterator>>,
           class Allocator = allocator<iter-to-alloc-type<InputIterator>>>
    unordered_map(InputIterator, InputIterator, typename see below::size_type = see below,
                  Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Hash, Pred,
                       Allocator>;

  template<ranges::input_range R, class Hash = hash<range-key-type<R>>,
           class Pred = equal_to<range-key-type<R>>,
           class Allocator = allocator<range-to-alloc-type<R>>>
    unordered_map(from_range_t, R&&, typename see below::size_type = see below,
                  Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_map<range-key-type<R>, range-mapped-type<R>, Hash, Pred, Allocator>;

  template<class Key, class T, class Hash = hash<Key>,
           class Pred = equal_to<Key>, class Allocator = allocator<pair<const Key, T>>>
    unordered_map(initializer_list<pair<Key, T>>,
                  typename see below::size_type = see below, Hash = Hash(),
                  Pred = Pred(), Allocator = Allocator())
      -> unordered_map<Key, T, Hash, Pred, Allocator>;

  template<class InputIterator, class Allocator>
    unordered_map(InputIterator, InputIterator, typename see below::size_type, Allocator)
      -> unordered_map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                       hash<iter-key-type<InputIterator>>,
                       equal_to<iter-key-type<InputIterator>>, Allocator>;

  template<class InputIterator, class Allocator>
    unordered_map(InputIterator, InputIterator, Allocator)
      -> unordered_map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                       hash<iter-key-type<InputIterator>>,
                       equal_to<iter-key-type<InputIterator>>, Allocator>;

  template<class InputIterator, class Hash, class Allocator>
    unordered_map(InputIterator, InputIterator, typename see below::size_type, Hash, Allocator)
      -> unordered_map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Hash,
                       equal_to<iter-key-type<InputIterator>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_map(from_range_t, R&&, typename see below::size_type, Allocator)
      -> unordered_map<range-key-type<R>, range-mapped-type<R>, hash<range-key-type<R>>,
                       equal_to<range-key-type<R>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_map(from_range_t, R&&, Allocator)
      -> unordered_map<range-key-type<R>, range-mapped-type<R>, hash<range-key-type<R>>,
                       equal_to<range-key-type<R>>, Allocator>;

  template<ranges::input_range R, class Hash, class Allocator>
    unordered_map(from_range_t, R&&, typename see below::size_type, Hash, Allocator)
      -> unordered_map<range-key-type<R>, range-mapped-type<R>, Hash,
                       equal_to<range-key-type<R>>, Allocator>;

  template<class Key, class T, class Allocator>
    unordered_map(initializer_list<pair<Key, T>>, typename see below::size_type,
                  Allocator)
      -> unordered_map<Key, T, hash<Key>, equal_to<Key>, Allocator>;

  template<class Key, class T, class Allocator>
    unordered_map(initializer_list<pair<Key, T>>, Allocator)
      -> unordered_map<Key, T, hash<Key>, equal_to<Key>, Allocator>;

  template<class Key, class T, class Hash, class Allocator>
    unordered_map(initializer_list<pair<Key, T>>, typename see below::size_type, Hash,
                  Allocator)
      -> unordered_map<Key, T, Hash, equal_to<Key>, Allocator>;
}
```

A `size_type` parameter type in an `unordered_map` deduction guide
refers to the `size_type` member type of the type deduced by the
deduction guide.

#### Constructors <a id="unord.map.cnstr">[[unord.map.cnstr]]</a>

``` cpp
unordered_map() : unordered_map(size_type(see below)) { }
explicit unordered_map(size_type n,
                       const hasher& hf = hasher(),
                       const key_equal& eql = key_equal(),
                       const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_map` using the specified hash
function, key equality predicate, and allocator, and using at least `n`
buckets. For the default constructor, the number of buckets is
*implementation-defined*. `max_load_factor()` returns `1.0`.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  unordered_map(InputIterator f, InputIterator l,
                size_type n = see below,
                const hasher& hf = hasher(),
                const key_equal& eql = key_equal(),
                const allocator_type& a = allocator_type());
template<container-compatible-range<value_type> R>
  unordered_map(from_range_t, R&& rg,
                size_type n = see below,
                const hasher& hf = hasher(),
                const key_equal& eql = key_equal(),
                const allocator_type& a = allocator_type());
unordered_map(initializer_list<value_type> il,
              size_type n = see below,
              const hasher& hf = hasher(),
              const key_equal& eql = key_equal(),
              const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_map` using the specified hash
function, key equality predicate, and allocator, and using at least `n`
buckets. If `n` is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range \[`f`,
`l`), `rg`, or `il`, respectively. `max_load_factor()` returns `1.0`.

*Complexity:* Average case linear, worst case quadratic.

#### Element access <a id="unord.map.elem">[[unord.map.elem]]</a>

``` cpp
mapped_type& operator[](const key_type& k);
```

*Effects:* Equivalent to: `return try_emplace(k).first->second;`

``` cpp
mapped_type& operator[](key_type&& k);
```

*Effects:* Equivalent to:
`return try_emplace(std::move(k)).first->second;`

``` cpp
mapped_type& at(const key_type& k);
const mapped_type& at(const key_type& k) const;
```

*Returns:* A reference to `x.second`, where `x` is the (unique) element
whose key is equivalent to `k`.

*Throws:* An exception object of type `out_of_range` if no such element
is present.

#### Modifiers <a id="unord.map.modifiers">[[unord.map.modifiers]]</a>

``` cpp
template<class P>
  pair<iterator, bool> insert(P&& obj);
```

*Constraints:* `is_constructible_v<value_type, P&&>` is `true`.

*Effects:* Equivalent to: `return emplace(std::forward<P>(obj));`

``` cpp
template<class P>
  iterator insert(const_iterator hint, P&& obj);
```

*Constraints:* `is_constructible_v<value_type, P&&>` is `true`.

*Effects:* Equivalent to:
`return emplace_hint(hint, std::forward<P>(obj));`

``` cpp
template<class... Args>
  pair<iterator, bool> try_emplace(const key_type& k, Args&&... args);
template<class... Args>
  iterator try_emplace(const_iterator hint, const key_type& k, Args&&... args);
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into
`unordered_map` from `piecewise_construct`, `forward_as_tuple(k)`,
`forward_as_tuple(std::forward<Args>(args)...)`.

*Effects:* If the map already contains an element whose key is
equivalent to `k`, there is no effect. Otherwise inserts an object of
type `value_type` constructed with `piecewise_construct`,
`forward_as_tuple(k)`, `forward_as_tuple(std::forward<Args>(args)...)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class... Args>
  pair<iterator, bool> try_emplace(key_type&& k, Args&&... args);
template<class... Args>
  iterator try_emplace(const_iterator hint, key_type&& k, Args&&... args);
```

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into
`unordered_map` from `piecewise_construct`,
`forward_as_tuple(std::move(k))`,
`forward_as_tuple(std::forward<Args>(args)...)`.

*Effects:* If the map already contains an element whose key is
equivalent to `k`, there is no effect. Otherwise inserts an object of
type `value_type` constructed with `piecewise_construct`,
`forward_as_tuple(std::move(k))`,
`forward_as_tuple(std::forward<Args>(args)...)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class M>
  pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
template<class M>
  iterator insert_or_assign(const_iterator hint, const key_type& k, M&& obj);
```

*Mandates:* `is_assignable_v<mapped_type&, M&&>` is `true`.

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into
`unordered_map` from `k`, `std::forward<M>(obj)`.

*Effects:* If the map already contains an element `e` whose key is
equivalent to `k`, assigns `std::forward<M>(obj)` to `e.second`.
Otherwise inserts an object of type `value_type` constructed with `k`,
`std::forward<M>(obj)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class M>
  pair<iterator, bool> insert_or_assign(key_type&& k, M&& obj);
template<class M>
  iterator insert_or_assign(const_iterator hint, key_type&& k, M&& obj);
```

*Mandates:* `is_assignable_v<mapped_type&, M&&>` is `true`.

*Preconditions:* `value_type` is *Cpp17EmplaceConstructible* into
`unordered_map` from `std::move(k)`, `std::forward<M>(obj)`.

*Effects:* If the map already contains an element `e` whose key is
equivalent to `k`, assigns `std::forward<M>(obj)` to `e.second`.
Otherwise inserts an object of type `value_type` constructed with
`std::move(k)`, `std::forward<M>(obj)`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

#### Erasure <a id="unord.map.erasure">[[unord.map.erasure]]</a>

``` cpp
template<class K, class T, class H, class P, class A, class Predicate>
  typename unordered_map<K, T, H, P, A>::size_type
    erase_if(unordered_map<K, T, H, P, A>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

### Class template `unordered_multimap` <a id="unord.multimap">[[unord.multimap]]</a>

#### Overview <a id="unord.multimap.overview">[[unord.multimap.overview]]</a>

An `unordered_multimap` is an unordered associative container that
supports equivalent keys (an instance of `unordered_multimap` may
contain multiple copies of each key value) and that associates values of
another type `mapped_type` with the keys. The `unordered_multimap` class
supports forward iterators.

An `unordered_multimap` meets all of the requirements of a container
[[container.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], and of an unordered associative container
[[unord.req]]. It provides the operations described in the preceding
requirements table for equivalent keys; that is, an `unordered_multimap`
supports the `a_eq` operations in that table, not the `a_uniq`
operations. For an `unordered_multimap<Key, T>` the `key_type` is `Key`,
the `mapped_type` is `T`, and the `value_type` is `pair<const Key, T>`.

Subclause  [[unord.multimap]] only describes operations on
`unordered_multimap` that are not described in one of the requirement
tables, or for which there is additional semantic information.

``` cpp
namespace std {
  template<class Key,
           class T,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Allocator = allocator<pair<const Key, T>>>
  class unordered_multimap {
  public:
    // types
    using key_type             = Key;
    using mapped_type          = T;
    using value_type           = pair<const Key, T>;
    using hasher               = Hash;
    using key_equal            = Pred;
    using allocator_type       = Allocator;
    using pointer              = typename allocator_traits<Allocator>::pointer;
    using const_pointer        = typename allocator_traits<Allocator>::const_pointer;
    using reference            = value_type&;
    using const_reference      = const value_type&;
    using size_type            = implementation-defined  // type of unordered_multimap::size_type; // see [container.requirements]
    using difference_type      = implementation-defined  // type of unordered_multimap::difference_type; // see [container.requirements]

    using iterator             = implementation-defined  // type of unordered_multimap::iterator; // see [container.requirements]
    using const_iterator       = implementation-defined  // type of unordered_multimap::const_iterator; // see [container.requirements]
    using local_iterator       = implementation-defined  // type of unordered_multimap::local_iterator; // see [container.requirements]
    using const_local_iterator = implementation-defined  // type of unordered_multimap::const_local_iterator; // see [container.requirements]
    using node_type            = unspecified;

    // [unord.multimap.cnstr], construct/copy/destroy
    unordered_multimap();
    explicit unordered_multimap(size_type n,
                                const hasher& hf = hasher(),
                                const key_equal& eql = key_equal(),
                                const allocator_type& a = allocator_type());
    template<class InputIterator>
      unordered_multimap(InputIterator f, InputIterator l,
                         size_type n = see below,
                         const hasher& hf = hasher(),
                         const key_equal& eql = key_equal(),
                         const allocator_type& a = allocator_type());
    template<container-compatible-range<value_type> R>
      unordered_multimap(from_range_t, R&& rg,
                         size_type n = see below,
                         const hasher& hf = hasher(),
                         const key_equal& eql = key_equal(),
                         const allocator_type& a = allocator_type());
    unordered_multimap(const unordered_multimap&);
    unordered_multimap(unordered_multimap&&);
    explicit unordered_multimap(const Allocator&);
    unordered_multimap(const unordered_multimap&, const type_identity_t<Allocator>&);
    unordered_multimap(unordered_multimap&&, const type_identity_t<Allocator>&);
    unordered_multimap(initializer_list<value_type> il,
                       size_type n = see below,
                       const hasher& hf = hasher(),
                       const key_equal& eql = key_equal(),
                       const allocator_type& a = allocator_type());
    unordered_multimap(size_type n, const allocator_type& a)
      : unordered_multimap(n, hasher(), key_equal(), a) { }
    unordered_multimap(size_type n, const hasher& hf, const allocator_type& a)
      : unordered_multimap(n, hf, key_equal(), a) { }
    template<class InputIterator>
      unordered_multimap(InputIterator f, InputIterator l, size_type n, const allocator_type& a)
        : unordered_multimap(f, l, n, hasher(), key_equal(), a) { }
    template<class InputIterator>
      unordered_multimap(InputIterator f, InputIterator l, size_type n, const hasher& hf,
                         const allocator_type& a)
        : unordered_multimap(f, l, n, hf, key_equal(), a) { }
  template<container-compatible-range<value_type> R>
    unordered_multimap(from_range_t, R&& rg, size_type n, const allocator_type& a)
      : unordered_multimap(from_range, std::forward<R>(rg),
                           n, hasher(), key_equal(), a) { }
  template<container-compatible-range<value_type> R>
    unordered_multimap(from_range_t, R&& rg, size_type n, const hasher& hf,
                       const allocator_type& a)
      : unordered_multimap(from_range, std::forward<R>(rg), n, hf, key_equal(), a) { }
    unordered_multimap(initializer_list<value_type> il, size_type n, const allocator_type& a)
      : unordered_multimap(il, n, hasher(), key_equal(), a) { }
    unordered_multimap(initializer_list<value_type> il, size_type n, const hasher& hf,
                       const allocator_type& a)
      : unordered_multimap(il, n, hf, key_equal(), a) { }
    ~unordered_multimap();
    unordered_multimap& operator=(const unordered_multimap&);
    unordered_multimap& operator=(unordered_multimap&&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Hash> &&
               is_nothrow_move_assignable_v<Pred>);
    unordered_multimap& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [unord.multimap.modifiers], modifiers
    template<class... Args> iterator emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& obj);
    iterator insert(value_type&& obj);
    template<class P> iterator insert(P&& obj);
    iterator insert(const_iterator hint, const value_type& obj);
    iterator insert(const_iterator hint, value_type&& obj);
    template<class P> iterator insert(const_iterator hint, P&& obj);
    template<class InputIterator> void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(unordered_multimap&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Hash> &&
               is_nothrow_swappable_v<Pred>);
    void      clear() noexcept;

    template<class H2, class P2>
      void merge(unordered_multimap<Key, T, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_multimap<Key, T, H2, P2, Allocator>&& source);
    template<class H2, class P2>
      void merge(unordered_map<Key, T, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_map<Key, T, H2, P2, Allocator>&& source);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // map operations
    iterator         find(const key_type& k);
    const_iterator   find(const key_type& k) const;
    template<class K>
      iterator       find(const K& k);
    template<class K>
      const_iterator find(const K& k) const;
    size_type        count(const key_type& k) const;
    template<class K>
      size_type      count(const K& k) const;
    bool             contains(const key_type& k) const;
    template<class K>
      bool           contains(const K& k) const;
    pair<iterator, iterator>               equal_range(const key_type& k);
    pair<const_iterator, const_iterator>   equal_range(const key_type& k) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& k);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& k) const;

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

  template<class InputIterator,
           class Hash = hash<iter-key-type<InputIterator>>,
           class Pred = equal_to<iter-key-type<InputIterator>>,
           class Allocator = allocator<iter-to-alloc-type<InputIterator>>>
    unordered_multimap(InputIterator, InputIterator,
                       typename see below::size_type = see below,
                       Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                            Hash, Pred, Allocator>;

  template<ranges::input_range R,
           class Hash = hash<range-key-type<R>>,
           class Pred = equal_to<range-key-type<R>>,
           class Allocator = allocator<range-to-alloc-type<R>>>
    unordered_multimap(from_range_t, R&&, typename see below::size_type = see below,
                       Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_multimap<range-key-type<R>, range-mapped-type<R>, Hash, Pred, Allocator>;

  template<class Key, class T, class Hash = hash<Key>,
           class Pred = equal_to<Key>, class Allocator = allocator<pair<const Key, T>>>
    unordered_multimap(initializer_list<pair<Key, T>>,
                       typename see below::size_type = see below,
                       Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_multimap<Key, T, Hash, Pred, Allocator>;

  template<class InputIterator, class Allocator>
    unordered_multimap(InputIterator, InputIterator, typename see below::size_type, Allocator)
      -> unordered_multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                            hash<iter-key-type<InputIterator>>,
                            equal_to<iter-key-type<InputIterator>>, Allocator>;

  template<class InputIterator, class Allocator>
    unordered_multimap(InputIterator, InputIterator, Allocator)
      -> unordered_multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                            hash<iter-key-type<InputIterator>>,
                            equal_to<iter-key-type<InputIterator>>, Allocator>;

  template<class InputIterator, class Hash, class Allocator>
    unordered_multimap(InputIterator, InputIterator, typename see below::size_type, Hash,
                       Allocator)
      -> unordered_multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Hash,
                            equal_to<iter-key-type<InputIterator>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_multimap(from_range_t, R&&, typename see below::size_type, Allocator)
      -> unordered_multimap<range-key-type<R>, range-mapped-type<R>, hash<range-key-type<R>>,
                            equal_to<range-key-type<R>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_multimap(from_range_t, R&&, Allocator)
      -> unordered_multimap<range-key-type<R>, range-mapped-type<R>, hash<range-key-type<R>>,
                            equal_to<range-key-type<R>>, Allocator>;

  template<ranges::input_range R, class Hash, class Allocator>
    unordered_multimap(from_range_t, R&&, typename see below::size_type, Hash, Allocator)
      -> unordered_multimap<range-key-type<R>, range-mapped-type<R>, Hash,
                            equal_to<range-key-type<R>>, Allocator>;

  template<class Key, class T, class Allocator>
    unordered_multimap(initializer_list<pair<Key, T>>, typename see below::size_type,
                       Allocator)
      -> unordered_multimap<Key, T, hash<Key>, equal_to<Key>, Allocator>;

  template<class Key, class T, class Allocator>
    unordered_multimap(initializer_list<pair<Key, T>>, Allocator)
      -> unordered_multimap<Key, T, hash<Key>, equal_to<Key>, Allocator>;

  template<class Key, class T, class Hash, class Allocator>
    unordered_multimap(initializer_list<pair<Key, T>>, typename see below::size_type,
                       Hash, Allocator)
      -> unordered_multimap<Key, T, Hash, equal_to<Key>, Allocator>;
}
```

A `size_type` parameter type in an `unordered_multimap` deduction guide
refers to the `size_type` member type of the type deduced by the
deduction guide.

#### Constructors <a id="unord.multimap.cnstr">[[unord.multimap.cnstr]]</a>

``` cpp
unordered_multimap() : unordered_multimap(size_type(see below)) { }
explicit unordered_multimap(size_type n,
                            const hasher& hf = hasher(),
                            const key_equal& eql = key_equal(),
                            const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multimap` using the specified
hash function, key equality predicate, and allocator, and using at least
`n` buckets. For the default constructor, the number of buckets is
*implementation-defined*. `max_load_factor()` returns `1.0`.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  unordered_multimap(InputIterator f, InputIterator l,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
template<container-compatible-range<value_type> R>
  unordered_multimap(from_range_t, R&& rg,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
unordered_multimap(initializer_list<value_type> il,
                   size_type n = see below,
                   const hasher& hf = hasher(),
                   const key_equal& eql = key_equal(),
                   const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multimap` using the specified
hash function, key equality predicate, and allocator, and using at least
`n` buckets. If `n` is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range \[`f`,
`l`), `rg`, or `il`, respectively. `max_load_factor()` returns `1.0`.

*Complexity:* Average case linear, worst case quadratic.

#### Modifiers <a id="unord.multimap.modifiers">[[unord.multimap.modifiers]]</a>

``` cpp
template<class P>
  iterator insert(P&& obj);
```

*Constraints:* `is_constructible_v<value_type, P&&>` is `true`.

*Effects:* Equivalent to: `return emplace(std::forward<P>(obj));`

``` cpp
template<class P>
  iterator insert(const_iterator hint, P&& obj);
```

*Constraints:* `is_constructible_v<value_type, P&&>` is `true`.

*Effects:* Equivalent to:
`return emplace_hint(hint, std::forward<P>(obj));`

#### Erasure <a id="unord.multimap.erasure">[[unord.multimap.erasure]]</a>

``` cpp
template<class K, class T, class H, class P, class A, class Predicate>
  typename unordered_multimap<K, T, H, P, A>::size_type
    erase_if(unordered_multimap<K, T, H, P, A>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

### Class template `unordered_set` <a id="unord.set">[[unord.set]]</a>

#### Overview <a id="unord.set.overview">[[unord.set.overview]]</a>

An `unordered_set` is an unordered associative container that supports
unique keys (an `unordered_set` contains at most one of each key value)
and in which the elements’ keys are the elements themselves. The
`unordered_set` class supports forward iterators.

An `unordered_set` meets all of the requirements of a container
[[container.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], of an unordered associative container
[[unord.req]]. It provides the operations described in the preceding
requirements table for unique keys; that is, an `unordered_set` supports
the `a_uniq` operations in that table, not the `a_eq` operations. For an
`unordered_set<Key>` the `key_type` and the `value_type` are both `Key`.
The `iterator` and `const_iterator` types are both constant iterator
types. It is unspecified whether they are the same type.

Subclause  [[unord.set]] only describes operations on `unordered_set`
that are not described in one of the requirement tables, or for which
there is additional semantic information.

``` cpp
namespace std {
  template<class Key,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Allocator = allocator<Key>>
  class unordered_set {
  public:
    // types
    using key_type             = Key;
    using value_type           = Key;
    using hasher               = Hash;
    using key_equal            = Pred;
    using allocator_type       = Allocator;
    using pointer              = typename allocator_traits<Allocator>::pointer;
    using const_pointer        = typename allocator_traits<Allocator>::const_pointer;
    using reference            = value_type&;
    using const_reference      = const value_type&;
    using size_type            = implementation-defined  // type of unordered_set::size_type; // see [container.requirements]
    using difference_type      = implementation-defined  // type of unordered_set::difference_type; // see [container.requirements]

    using iterator             = implementation-defined  // type of unordered_set::iterator; // see [container.requirements]
    using const_iterator       = implementation-defined  // type of unordered_set::const_iterator; // see [container.requirements]
    using local_iterator       = implementation-defined  // type of unordered_set::local_iterator; // see [container.requirements]
    using const_local_iterator = implementation-defined  // type of unordered_set::const_local_iterator; // see [container.requirements]
    using node_type            = unspecified;
    using insert_return_type   = insert-return-type<iterator, node_type>;

    // [unord.set.cnstr], construct/copy/destroy
    unordered_set();
    explicit unordered_set(size_type n,
                           const hasher& hf = hasher(),
                           const key_equal& eql = key_equal(),
                           const allocator_type& a = allocator_type());
    template<class InputIterator>
      unordered_set(InputIterator f, InputIterator l,
                    size_type n = see below,
                    const hasher& hf = hasher(),
                    const key_equal& eql = key_equal(),
                    const allocator_type& a = allocator_type());
    template<container-compatible-range<value_type> R>
      unordered_set(from_range_t, R&& rg,
                    size_type n = see below,
                    const hasher& hf = hasher(),
                    const key_equal& eql = key_equal(),
                    const allocator_type& a = allocator_type());
    unordered_set(const unordered_set&);
    unordered_set(unordered_set&&);
    explicit unordered_set(const Allocator&);
    unordered_set(const unordered_set&, const type_identity_t<Allocator>&);
    unordered_set(unordered_set&&, const type_identity_t<Allocator>&);
    unordered_set(initializer_list<value_type> il,
                  size_type n = see below,
                  const hasher& hf = hasher(),
                  const key_equal& eql = key_equal(),
                  const allocator_type& a = allocator_type());
    unordered_set(size_type n, const allocator_type& a)
      : unordered_set(n, hasher(), key_equal(), a) { }
    unordered_set(size_type n, const hasher& hf, const allocator_type& a)
      : unordered_set(n, hf, key_equal(), a) { }
    template<class InputIterator>
      unordered_set(InputIterator f, InputIterator l, size_type n, const allocator_type& a)
        : unordered_set(f, l, n, hasher(), key_equal(), a) { }
    template<class InputIterator>
      unordered_set(InputIterator f, InputIterator l, size_type n, const hasher& hf,
                    const allocator_type& a)
      : unordered_set(f, l, n, hf, key_equal(), a) { }
    unordered_set(initializer_list<value_type> il, size_type n, const allocator_type& a)
      : unordered_set(il, n, hasher(), key_equal(), a) { }
    template<container-compatible-range<value_type> R>
      unordered_set(from_range_t, R&& rg, size_type n, const allocator_type& a)
        : unordered_set(from_range, std::forward<R>(rg), n, hasher(), key_equal(), a) { }
    template<container-compatible-range<value_type> R>
      unordered_set(from_range_t, R&& rg, size_type n, const hasher& hf, const allocator_type& a)
        : unordered_set(from_range, std::forward<R>(rg), n, hf, key_equal(), a) { }
    unordered_set(initializer_list<value_type> il, size_type n, const hasher& hf,
                  const allocator_type& a)
      : unordered_set(il, n, hf, key_equal(), a) { }
    ~unordered_set();
    unordered_set& operator=(const unordered_set&);
    unordered_set& operator=(unordered_set&&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Hash> &&
               is_nothrow_move_assignable_v<Pred>);
    unordered_set& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // modifiers
    template<class... Args> pair<iterator, bool> emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    pair<iterator, bool> insert(const value_type& obj);
    pair<iterator, bool> insert(value_type&& obj);
    iterator insert(const_iterator hint, const value_type& obj);
    iterator insert(const_iterator hint, value_type&& obj);
    template<class InputIterator> void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    insert_return_type insert(node_type&& nh);
    iterator           insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position)
      requires (!same_as<iterator, const_iterator>);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(unordered_set&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Hash> &&
               is_nothrow_swappable_v<Pred>);
    void      clear() noexcept;

    template<class H2, class P2>
      void merge(unordered_set<Key, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_set<Key, H2, P2, Allocator>&& source);
    template<class H2, class P2>
      void merge(unordered_multiset<Key, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_multiset<Key, H2, P2, Allocator>&& source);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // set operations
    iterator         find(const key_type& k);
    const_iterator   find(const key_type& k) const;
    template<class K>
      iterator       find(const K& k);
    template<class K>
      const_iterator find(const K& k) const;
    size_type        count(const key_type& k) const;
    template<class K>
      size_type      count(const K& k) const;
    bool             contains(const key_type& k) const;
    template<class K>
      bool           contains(const K& k) const;
    pair<iterator, iterator>               equal_range(const key_type& k);
    pair<const_iterator, const_iterator>   equal_range(const key_type& k) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& k);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& k) const;

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

  template<class InputIterator,
           class Hash = hash<iter-value-type<InputIterator>>,
           class Pred = equal_to<iter-value-type<InputIterator>>,
           class Allocator = allocator<iter-value-type<InputIterator>>>
    unordered_set(InputIterator, InputIterator, typename see below::size_type = see below,
                  Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_set<iter-value-type<InputIterator>,
                       Hash, Pred, Allocator>;

  template<ranges::input_range R,
           class Hash = hash<ranges::range_value_t<R>>,
           class Pred = equal_to<ranges::range_value_t<R>>,
           class Allocator = allocator<ranges::range_value_t<R>>>
    unordered_set(from_range_t, R&&, typename see below::size_type = see below,
Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_set<ranges::range_value_t<R>, Hash, Pred, Allocator>;

  template<class T, class Hash = hash<T>,
           class Pred = equal_to<T>, class Allocator = allocator<T>>
    unordered_set(initializer_list<T>, typename see below::size_type = see below,
                  Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_set<T, Hash, Pred, Allocator>;

  template<class InputIterator, class Allocator>
    unordered_set(InputIterator, InputIterator, typename see below::size_type, Allocator)
      -> unordered_set<iter-value-type<InputIterator>,
                       hash<iter-value-type<InputIterator>>,
                       equal_to<iter-value-type<InputIterator>>,
                       Allocator>;

  template<class InputIterator, class Hash, class Allocator>
    unordered_set(InputIterator, InputIterator, typename see below::size_type,
                  Hash, Allocator)
      -> unordered_set<iter-value-type<InputIterator>, Hash,
                       equal_to<iter-value-type<InputIterator>>,
                       Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_set(from_range_t, R&&, typename see below::size_type, Allocator)
      -> unordered_set<ranges::range_value_t<R>, hash<ranges::range_value_t<R>>,
                       equal_to<ranges::range_value_t<R>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_set(from_range_t, R&&, Allocator)
      -> unordered_set<ranges::range_value_t<R>, hash<ranges::range_value_t<R>>,
                       equal_to<ranges::range_value_t<R>>, Allocator>;

  template<ranges::input_range R, class Hash, class Allocator>
    unordered_set(from_range_t, R&&, typename see below::size_type, Hash, Allocator)
      -> unordered_set<ranges::range_value_t<R>, Hash,
                       equal_to<ranges::range_value_t<R>>, Allocator>;

  template<class T, class Allocator>
    unordered_set(initializer_list<T>, typename see below::size_type, Allocator)
      -> unordered_set<T, hash<T>, equal_to<T>, Allocator>;

  template<class T, class Hash, class Allocator>
    unordered_set(initializer_list<T>, typename see below::size_type, Hash, Allocator)
      -> unordered_set<T, Hash, equal_to<T>, Allocator>;
}
```

A `size_type` parameter type in an `unordered_set` deduction guide
refers to the `size_type` member type of the type deduced by the
deduction guide.

#### Constructors <a id="unord.set.cnstr">[[unord.set.cnstr]]</a>

``` cpp
unordered_set() : unordered_set(size_type(see below)) { }
explicit unordered_set(size_type n,
                       const hasher& hf = hasher(),
                       const key_equal& eql = key_equal(),
                       const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_set` using the specified hash
function, key equality predicate, and allocator, and using at least `n`
buckets. For the default constructor, the number of buckets is
*implementation-defined*. `max_load_factor()` returns `1.0`.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  unordered_set(InputIterator f, InputIterator l,
                size_type n = see below,
                const hasher& hf = hasher(),
                const key_equal& eql = key_equal(),
                const allocator_type& a = allocator_type());
template<container-compatible-range<value_type> R>
  unordered_multiset(from_range_t, R&& rg,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
unordered_set(initializer_list<value_type> il,
              size_type n = see below,
              const hasher& hf = hasher(),
              const key_equal& eql = key_equal(),
              const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_set` using the specified hash
function, key equality predicate, and allocator, and using at least `n`
buckets. If `n` is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range \[`f`,
`l`), `rg`, or `il`, respectively. `max_load_factor()` returns `1.0`.

*Complexity:* Average case linear, worst case quadratic.

#### Erasure <a id="unord.set.erasure">[[unord.set.erasure]]</a>

``` cpp
template<class K, class H, class P, class A, class Predicate>
  typename unordered_set<K, H, P, A>::size_type
    erase_if(unordered_set<K, H, P, A>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

### Class template `unordered_multiset` <a id="unord.multiset">[[unord.multiset]]</a>

#### Overview <a id="unord.multiset.overview">[[unord.multiset.overview]]</a>

An `unordered_multiset` is an unordered associative container that
supports equivalent keys (an instance of `unordered_multiset` may
contain multiple copies of the same key value) and in which each
element’s key is the element itself. The `unordered_multiset` class
supports forward iterators.

An `unordered_multiset` meets all of the requirements of a container
[[container.reqmts]], of an allocator-aware container
[[container.alloc.reqmts]], and of an unordered associative container
[[unord.req]]. It provides the operations described in the preceding
requirements table for equivalent keys; that is, an `unordered_multiset`
supports the `a_eq` operations in that table, not the `a_uniq`
operations. For an `unordered_multiset<Key>` the `key_type` and the
`value_type` are both `Key`. The `iterator` and `const_iterator` types
are both constant iterator types. It is unspecified whether they are the
same type.

Subclause  [[unord.multiset]] only describes operations on
`unordered_multiset` that are not described in one of the requirement
tables, or for which there is additional semantic information.

``` cpp
namespace std {
  template<class Key,
           class Hash = hash<Key>,
           class Pred = equal_to<Key>,
           class Allocator = allocator<Key>>
  class unordered_multiset {
  public:
    // types
    using key_type             = Key;
    using value_type           = Key;
    using hasher               = Hash;
    using key_equal            = Pred;
    using allocator_type       = Allocator;
    using pointer              = typename allocator_traits<Allocator>::pointer;
    using const_pointer        = typename allocator_traits<Allocator>::const_pointer;
    using reference            = value_type&;
    using const_reference      = const value_type&;
    using size_type            = implementation-defined  // type of unordered_multiset::size_type; // see [container.requirements]
    using difference_type      = implementation-defined  // type of unordered_multiset::difference_type; // see [container.requirements]

    using iterator             = implementation-defined  // type of unordered_multiset::iterator; // see [container.requirements]
    using const_iterator       = implementation-defined  // type of unordered_multiset::const_iterator; // see [container.requirements]
    using local_iterator       = implementation-defined  // type of unordered_multiset::local_iterator; // see [container.requirements]
    using const_local_iterator = implementation-defined  // type of unordered_multiset::const_local_iterator; // see [container.requirements]
    using node_type            = unspecified;

    // [unord.multiset.cnstr], construct/copy/destroy
    unordered_multiset();
    explicit unordered_multiset(size_type n,
                                const hasher& hf = hasher(),
                                const key_equal& eql = key_equal(),
                                const allocator_type& a = allocator_type());
    template<class InputIterator>
      unordered_multiset(InputIterator f, InputIterator l,
                         size_type n = see below,
                         const hasher& hf = hasher(),
                         const key_equal& eql = key_equal(),
                         const allocator_type& a = allocator_type());
    template<container-compatible-range<value_type> R>
      unordered_multiset(from_range_t, R&& rg,
                         size_type n = see below,
                         const hasher& hf = hasher(),
                         const key_equal& eql = key_equal(),
                         const allocator_type& a = allocator_type());
    unordered_multiset(const unordered_multiset&);
    unordered_multiset(unordered_multiset&&);
    explicit unordered_multiset(const Allocator&);
    unordered_multiset(const unordered_multiset&, const type_identity_t<Allocator>&);
    unordered_multiset(unordered_multiset&&, const type_identity_t<Allocator>&);
    unordered_multiset(initializer_list<value_type> il,
                       size_type n = see below,
                       const hasher& hf = hasher(),
                       const key_equal& eql = key_equal(),
                       const allocator_type& a = allocator_type());
    unordered_multiset(size_type n, const allocator_type& a)
      : unordered_multiset(n, hasher(), key_equal(), a) { }
    unordered_multiset(size_type n, const hasher& hf, const allocator_type& a)
      : unordered_multiset(n, hf, key_equal(), a) { }
    template<class InputIterator>
      unordered_multiset(InputIterator f, InputIterator l, size_type n, const allocator_type& a)
        : unordered_multiset(f, l, n, hasher(), key_equal(), a) { }
    template<class InputIterator>
      unordered_multiset(InputIterator f, InputIterator l, size_type n, const hasher& hf,
                         const allocator_type& a)
      : unordered_multiset(f, l, n, hf, key_equal(), a) { }
    template<container-compatible-range<value_type> R>
      unordered_multiset(from_range_t, R&& rg, size_type n, const allocator_type& a)
        : unordered_multiset(from_range, std::forward<R>(rg),
                             n, hasher(), key_equal(), a) { }
    template<container-compatible-range<value_type> R>
      unordered_multiset(from_range_t, R&& rg, size_type n, const hasher& hf,
                         const allocator_type& a)
        : unordered_multiset(from_range, std::forward<R>(rg), n, hf, key_equal(), a) { }
    unordered_multiset(initializer_list<value_type> il, size_type n, const allocator_type& a)
      : unordered_multiset(il, n, hasher(), key_equal(), a) { }
    unordered_multiset(initializer_list<value_type> il, size_type n, const hasher& hf,
                       const allocator_type& a)
      : unordered_multiset(il, n, hf, key_equal(), a) { }
    ~unordered_multiset();
    unordered_multiset& operator=(const unordered_multiset&);
    unordered_multiset& operator=(unordered_multiset&&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_move_assignable_v<Hash> &&
               is_nothrow_move_assignable_v<Pred>);
    unordered_multiset& operator=(initializer_list<value_type>);
    allocator_type get_allocator() const noexcept;

    // iterators
    iterator       begin() noexcept;
    const_iterator begin() const noexcept;
    iterator       end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cbegin() const noexcept;
    const_iterator cend() const noexcept;

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // modifiers
    template<class... Args> iterator emplace(Args&&... args);
    template<class... Args> iterator emplace_hint(const_iterator position, Args&&... args);
    iterator insert(const value_type& obj);
    iterator insert(value_type&& obj);
    iterator insert(const_iterator hint, const value_type& obj);
    iterator insert(const_iterator hint, value_type&& obj);
    template<class InputIterator> void insert(InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    template<class K> node_type extract(K&& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position)
      requires (!same_as<iterator, const_iterator>);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
    template<class K> size_type erase(K&& x);
    iterator  erase(const_iterator first, const_iterator last);
    void      swap(unordered_multiset&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value &&
               is_nothrow_swappable_v<Hash> &&
               is_nothrow_swappable_v<Pred>);
    void      clear() noexcept;

    template<class H2, class P2>
      void merge(unordered_multiset<Key, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_multiset<Key, H2, P2, Allocator>&& source);
    template<class H2, class P2>
      void merge(unordered_set<Key, H2, P2, Allocator>& source);
    template<class H2, class P2>
      void merge(unordered_set<Key, H2, P2, Allocator>&& source);

    // observers
    hasher hash_function() const;
    key_equal key_eq() const;

    // set operations
    iterator         find(const key_type& k);
    const_iterator   find(const key_type& k) const;
    template<class K>
      iterator       find(const K& k);
    template<class K>
      const_iterator find(const K& k) const;
    size_type        count(const key_type& k) const;
    template<class K>
      size_type      count(const K& k) const;
    bool             contains(const key_type& k) const;
    template<class K>
      bool           contains(const K& k) const;
    pair<iterator, iterator>               equal_range(const key_type& k);
    pair<const_iterator, const_iterator>   equal_range(const key_type& k) const;
    template<class K>
      pair<iterator, iterator>             equal_range(const K& k);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& k) const;

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

  template<class InputIterator,
           class Hash = hash<iter-value-type<InputIterator>>,
           class Pred = equal_to<iter-value-type<InputIterator>>,
           class Allocator = allocator<iter-value-type<InputIterator>>>
    unordered_multiset(InputIterator, InputIterator, see below::size_type = see below,
                       Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_multiset<iter-value-type<InputIterator>,
                            Hash, Pred, Allocator>;

  template<ranges::input_range R,
           class Hash = hash<ranges::range_value_t<R>>,
           class Pred = equal_to<ranges::range_value_t<R>>,
           class Allocator = allocator<ranges::range_value_t<R>>>
    unordered_multiset(from_range_t, R&&, typename see below::size_type = see below,
                       Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_multiset<ranges::range_value_t<R>, Hash, Pred, Allocator>;

  template<class T, class Hash = hash<T>,
           class Pred = equal_to<T>, class Allocator = allocator<T>>
    unordered_multiset(initializer_list<T>, typename see below::size_type = see below,
                       Hash = Hash(), Pred = Pred(), Allocator = Allocator())
      -> unordered_multiset<T, Hash, Pred, Allocator>;

  template<class InputIterator, class Allocator>
    unordered_multiset(InputIterator, InputIterator, typename see below::size_type, Allocator)
      -> unordered_multiset<iter-value-type<InputIterator>,
                            hash<iter-value-type<InputIterator>>,
                            equal_to<iter-value-type<InputIterator>>,
                            Allocator>;

  template<class InputIterator, class Hash, class Allocator>
    unordered_multiset(InputIterator, InputIterator, typename see below::size_type,
                       Hash, Allocator)
      -> unordered_multiset<iter-value-type<InputIterator>, Hash,
                            equal_to<iter-value-type<InputIterator>>,
                            Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_multiset(from_range_t, R&&, typename see below::size_type, Allocator)
      -> unordered_multiset<ranges::range_value_t<R>, hash<ranges::range_value_t<R>>,
                            equal_to<ranges::range_value_t<R>>, Allocator>;

  template<ranges::input_range R, class Allocator>
    unordered_multiset(from_range_t, R&&, Allocator)
      -> unordered_multiset<ranges::range_value_t<R>, hash<ranges::range_value_t<R>>,
                            equal_to<ranges::range_value_t<R>>, Allocator>;

  template<ranges::input_range R, class Hash, class Allocator>
    unordered_multiset(from_range_t, R&&, typename see below::size_type, Hash, Allocator)
      -> unordered_multiset<ranges::range_value_t<R>, Hash, equal_to<ranges::range_value_t<R>>,
                            Allocator>;

  template<class T, class Allocator>
    unordered_multiset(initializer_list<T>, typename see below::size_type, Allocator)
      -> unordered_multiset<T, hash<T>, equal_to<T>, Allocator>;

  template<class T, class Hash, class Allocator>
    unordered_multiset(initializer_list<T>, typename see below::size_type, Hash, Allocator)
      -> unordered_multiset<T, Hash, equal_to<T>, Allocator>;
}
```

A `size_type` parameter type in an `unordered_multiset` deduction guide
refers to the `size_type` member type of the type deduced by the
deduction guide.

#### Constructors <a id="unord.multiset.cnstr">[[unord.multiset.cnstr]]</a>

``` cpp
unordered_multiset() : unordered_multiset(size_type(see below)) { }
explicit unordered_multiset(size_type n,
                            const hasher& hf = hasher(),
                            const key_equal& eql = key_equal(),
                            const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multiset` using the specified
hash function, key equality predicate, and allocator, and using at least
`n` buckets. For the default constructor, the number of buckets is
*implementation-defined*. `max_load_factor()` returns `1.0`.

*Complexity:* Constant.

``` cpp
template<class InputIterator>
  unordered_multiset(InputIterator f, InputIterator l,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
template<container-compatible-range<value_type> R>
  unordered_multiset(from_range_t, R&& rg,
                     size_type n = see below,
                     const hasher& hf = hasher(),
                     const key_equal& eql = key_equal(),
                     const allocator_type& a = allocator_type());
unordered_multiset(initializer_list<value_type> il,
                   size_type n = see below,
                   const hasher& hf = hasher(),
                   const key_equal& eql = key_equal(),
                   const allocator_type& a = allocator_type());
```

*Effects:* Constructs an empty `unordered_multiset` using the specified
hash function, key equality predicate, and allocator, and using at least
`n` buckets. If `n` is not provided, the number of buckets is
*implementation-defined*. Then inserts elements from the range \[`f`,
`l`), `rg`, or `il`, respectively. `max_load_factor()` returns `1.0`.

*Complexity:* Average case linear, worst case quadratic.

#### Erasure <a id="unord.multiset.erasure">[[unord.multiset.erasure]]</a>

``` cpp
template<class K, class H, class P, class A, class Predicate>
  typename unordered_multiset<K, H, P, A>::size_type
    erase_if(unordered_multiset<K, H, P, A>& c, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
auto original_size = c.size();
for (auto i = c.begin(), last = c.end(); i != last; ) {
  if (pred(*i)) {
    i = c.erase(i);
  } else {
    ++i;
  }
}
return original_size - c.size();
```

## Container adaptors <a id="container.adaptors">[[container.adaptors]]</a>

### In general <a id="container.adaptors.general">[[container.adaptors.general]]</a>

The headers `<queue>`, `<stack>`, `<flat_map>`, and `<flat_set>` define
the container adaptors `queue` and `priority_queue`, `stack`, `flat_map`
and `flat_multimap`, and `flat_set` and `flat_multiset`, respectively.

Each container adaptor takes one or more template parameters named
`Container`, `KeyContainer`, or `MappedContainer` that denote the types
of containers that the container adaptor adapts. Each container adaptor
has at least one constructor that takes a reference argument to one or
more such template parameters. For each constructor reference argument
to a container `C`, the constructor copies the container into the
container adaptor. If `C` takes an allocator, then a compatible
allocator may be passed in to the adaptor’s constructor. Otherwise,
normal copy or move construction is used for the container argument. For
the container adaptors that take a single container template parameter
`Container`, the first template parameter `T` of the container adaptor
shall denote the same type as `Container::value_type`.

For container adaptors, no `swap` function throws an exception unless
that exception is thrown by the swap of the adaptor’s `Container`,
`KeyContainer`, `MappedContainer`, or `Compare` object (if any).

A constructor template of a container adaptor shall not participate in
overload resolution if it has an `InputIterator` template parameter and
a type that does not qualify as an input iterator is deduced for that
parameter.

For container adaptors that have them, the `insert`, `emplace`, and
`erase` members affect the validity of iterators, references, and
pointers to the adaptor’s container(s) in the same way that the
containers’ respective `insert`, `emplace`, and `erase` members do.

[*Example 1*: A call to `flat_map<Key, T>::insert` can invalidate all
iterators to the `flat_map`. — *end example*]

A deduction guide for a container adaptor shall not participate in
overload resolution if any of the following are true:

- It has an `InputIterator` template parameter and a type that does not
  qualify as an input iterator is deduced for that parameter.
- It has a `Compare` template parameter and a type that qualifies as an
  allocator is deduced for that parameter.
- It has a `Container`, `KeyContainer`, or `MappedContainer` template
  parameter and a type that qualifies as an allocator is deduced for
  that parameter.
- It has no `Container`, `KeyContainer`, or `MappedContainer` template
  parameter, and it has an `Allocator` template parameter, and a type
  that does not qualify as an allocator is deduced for that parameter.
- It has both `Container` and `Allocator` template parameters, and
  `uses_allocator_v<Container, Allocator>` is `false`.
- It has both `KeyContainer` and `Allocator` template parameters, and
  `uses_allocator_v<KeyContainer, Allocator>` is `false`.
- It has both `KeyContainer` and `Compare` template parameters, and
  ``` cpp
  is_invocable_v<const Compare&,
                const typename KeyContainer::value_type&,
                const typename KeyContainer::value_type&>
  ```

  is not a valid expression or is `false`.
- It has both `MappedContainer` and `Allocator` template parameters, and
  `uses_allocator_v<MappedContainer, Allocator>` is `false`.

The exposition-only alias template *iter-value-type* defined in
[[sequences.general]] and the exposition-only alias templates
*iter-key-type*, *iter-mapped-type*, *range-key-type*, and
*range-mapped-type* defined in [[associative.general]] may appear in
deduction guides for container adaptors.

The following exposition-only alias template may appear in deduction
guides for container adaptors:

``` cpp
template<class Allocator, class T>
  using alloc-rebind =                      // exposition only
    typename allocator_traits<Allocator>::template rebind_alloc<T>;
```

### Header `<queue>` synopsis <a id="queue.syn">[[queue.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [queue], class template queue
  template<class T, class Container = deque<T>> class queue;

  template<class T, class Container>
    bool operator==(const queue<T, Container>& x, const queue<T, Container>& y);
  template<class T, class Container>
    bool operator!=(const queue<T, Container>& x, const queue<T, Container>& y);
  template<class T, class Container>
    bool operator< (const queue<T, Container>& x, const queue<T, Container>& y);
  template<class T, class Container>
    bool operator> (const queue<T, Container>& x, const queue<T, Container>& y);
  template<class T, class Container>
    bool operator<=(const queue<T, Container>& x, const queue<T, Container>& y);
  template<class T, class Container>
    bool operator>=(const queue<T, Container>& x, const queue<T, Container>& y);
  template<class T, three_way_comparable Container>
    compare_three_way_result_t<Container>
      operator<=>(const queue<T, Container>& x, const queue<T, Container>& y);

  template<class T, class Container>
    void swap(queue<T, Container>& x, queue<T, Container>& y) noexcept(noexcept(x.swap(y)));
  template<class T, class Container, class Alloc>
    struct uses_allocator<queue<T, Container>, Alloc>;

  // [priority.queue], class template priority_queue
  template<class T, class Container = vector<T>,
           class Compare = less<typename Container::value_type>>
    class priority_queue;

  template<class T, class Container, class Compare>
    void swap(priority_queue<T, Container, Compare>& x,
              priority_queue<T, Container, Compare>& y) noexcept(noexcept(x.swap(y)));
  template<class T, class Container, class Compare, class Alloc>
    struct uses_allocator<priority_queue<T, Container, Compare>, Alloc>;
}
```

### Header `<stack>` synopsis <a id="stack.syn">[[stack.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [stack], class template stack
  template<class T, class Container = deque<T>> class stack;

  template<class T, class Container>
    bool operator==(const stack<T, Container>& x, const stack<T, Container>& y);
  template<class T, class Container>
    bool operator!=(const stack<T, Container>& x, const stack<T, Container>& y);
  template<class T, class Container>
    bool operator< (const stack<T, Container>& x, const stack<T, Container>& y);
  template<class T, class Container>
    bool operator> (const stack<T, Container>& x, const stack<T, Container>& y);
  template<class T, class Container>
    bool operator<=(const stack<T, Container>& x, const stack<T, Container>& y);
  template<class T, class Container>
    bool operator>=(const stack<T, Container>& x, const stack<T, Container>& y);
  template<class T, three_way_comparable Container>
    compare_three_way_result_t<Container>
      operator<=>(const stack<T, Container>& x, const stack<T, Container>& y);

  template<class T, class Container>
    void swap(stack<T, Container>& x, stack<T, Container>& y) noexcept(noexcept(x.swap(y)));
  template<class T, class Container, class Alloc>
    struct uses_allocator<stack<T, Container>, Alloc>;
}
```

### Header `<flat_map>` synopsis <a id="flat.map.syn">[[flat.map.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [flat.map], class template flat_map
  template<class Key, class T, class Compare = less<Key>,
           class KeyContainer = vector<Key>, class MappedContainer = vector<T>>
    class flat_map;

  struct sorted_unique_t { explicit sorted_unique_t() = default; };
  inline constexpr sorted_unique_t sorted_unique{};

  template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
           class Allocator>
    struct uses_allocator<flat_map<Key, T, Compare, KeyContainer, MappedContainer>,
                          Allocator>;

  // [flat.map.erasure], erasure for flat_map
  template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
           class Predicate>
    typename flat_map<Key, T, Compare, KeyContainer, MappedContainer>::size_type
      erase_if(flat_map<Key, T, Compare, KeyContainer, MappedContainer>& c, Predicate pred);

  // [flat.multimap], class template flat_multimap
  template<class Key, class T, class Compare = less<Key>,
           class KeyContainer = vector<Key>, class MappedContainer = vector<T>>
    class flat_multimap;

  struct sorted_equivalent_t { explicit sorted_equivalent_t() = default; };
  inline constexpr sorted_equivalent_t sorted_equivalent{};

  template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
           class Allocator>
    struct uses_allocator<flat_multimap<Key, T, Compare, KeyContainer, MappedContainer>,
                          Allocator>;

  // [flat.multimap.erasure], erasure for flat_multimap
  template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
           class Predicate>
    typename flat_multimap<Key, T, Compare, KeyContainer, MappedContainer>::size_type
      erase_if(flat_multimap<Key, T, Compare, KeyContainer, MappedContainer>& c, Predicate pred);
}
```

### Header `<flat_set>` synopsis <a id="flat.set.syn">[[flat.set.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [flat.set], class template flat_set
  template<class Key, class Compare = less<Key>, class KeyContainer = vector<Key>>
    class flat_set;

  struct sorted_unique_t { explicit sorted_unique_t() = default; };
  inline constexpr sorted_unique_t sorted_unique{};

  template<class Key, class Compare, class KeyContainer, class Allocator>
    struct uses_allocator<flat_set<Key, Compare, KeyContainer>, Allocator>;

  // [flat.set.erasure], erasure for flat_set
  template<class Key, class Compare, class KeyContainer, class Predicate>
    typename flat_set<Key, Compare, KeyContainer>::size_type
      erase_if(flat_set<Key, Compare, KeyContainer>& c, Predicate pred);

  // [flat.multiset], class template flat_multiset
  template<class Key, class Compare = less<Key>, class KeyContainer = vector<Key>>
    class flat_multiset;

  struct sorted_equivalent_t { explicit sorted_equivalent_t() = default; };
  inline constexpr sorted_equivalent_t sorted_equivalent{};

  template<class Key, class Compare, class KeyContainer, class Allocator>
    struct uses_allocator<flat_multiset<Key, Compare, KeyContainer>, Allocator>;

  // [flat.multiset.erasure], erasure for flat_multiset
  template<class Key, class Compare, class KeyContainer, class Predicate>
    typename flat_multiset<Key, Compare, KeyContainer>::size_type
      erase_if(flat_multiset<Key, Compare, KeyContainer>& c, Predicate pred);
}
```

### Class template `queue` <a id="queue">[[queue]]</a>

#### Definition <a id="queue.defn">[[queue.defn]]</a>

Any sequence container supporting operations `front()`, `back()`,
`push_back()` and `pop_front()` can be used to instantiate `queue`. In
particular, `list` [[list]] and `deque` [[deque]] can be used.

``` cpp
namespace std {
  template<class T, class Container = deque<T>>
  class queue {
  public:
    using value_type      = typename Container::value_type;
    using reference       = typename Container::reference;
    using const_reference = typename Container::const_reference;
    using size_type       = typename Container::size_type;
    using container_type  =          Container;

  protected:
    Container c;

  public:
    queue() : queue(Container()) {}
    explicit queue(const Container&);
    explicit queue(Container&&);
    template<class InputIterator> queue(InputIterator first, InputIterator last);
    template<container-compatible-range<T> R> queue(from_range_t, R&& rg);
    template<class Alloc> explicit queue(const Alloc&);
    template<class Alloc> queue(const Container&, const Alloc&);
    template<class Alloc> queue(Container&&, const Alloc&);
    template<class Alloc> queue(const queue&, const Alloc&);
    template<class Alloc> queue(queue&&, const Alloc&);
    template<class InputIterator, class Alloc>
      queue(InputIterator first, InputIterator last, const Alloc&);
    template<container-compatible-range<T> R, class Alloc>
      queue(from_range_t, R&& rg, const Alloc&);

    [[nodiscard]] bool empty() const    { return c.empty(); }
    size_type         size()  const     { return c.size(); }
    reference         front()           { return c.front(); }
    const_reference   front() const     { return c.front(); }
    reference         back()            { return c.back(); }
    const_reference   back() const      { return c.back(); }
    void push(const value_type& x)      { c.push_back(x); }
    void push(value_type&& x)           { c.push_back(std::move(x)); }
    template<container-compatible-range<T> R> void push_range(R&& rg);
    template<class... Args>
      decltype(auto) emplace(Args&&... args)
        { return c.emplace_back(std::forward<Args>(args)...); }
    void pop()                          { c.pop_front(); }
    void swap(queue& q) noexcept(is_nothrow_swappable_v<Container>)
      { using std::swap; swap(c, q.c); }
  };

  template<class Container>
    queue(Container) -> queue<typename Container::value_type, Container>;

  template<class InputIterator>
    queue(InputIterator, InputIterator) -> queue<iter-value-type<InputIterator>>;

  template<ranges::input_range R>
    queue(from_range_t, R&&) -> queue<ranges::range_value_t<R>>;

  template<class Container, class Allocator>
    queue(Container, Allocator) -> queue<typename Container::value_type, Container>;

  template<class InputIterator, class Allocator>
    queue(InputIterator, InputIterator, Allocator)
      -> queue<iter-value-type<InputIterator>, deque<iter-value-type<InputIterator>,
               Allocator>>;

  template<ranges::input_range R, class Allocator>
    queue(from_range_t, R&&, Allocator)
      -> queue<ranges::range_value_t<R>, deque<ranges::range_value_t<R>, Allocator>>;

  template<class T, class Container, class Alloc>
    struct uses_allocator<queue<T, Container>, Alloc>
      : uses_allocator<Container, Alloc>::type { };
}
```

#### Constructors <a id="queue.cons">[[queue.cons]]</a>

``` cpp
explicit queue(const Container& cont);
```

*Effects:* Initializes `c` with `cont`.

``` cpp
explicit queue(Container&& cont);
```

*Effects:* Initializes `c` with `std::move(cont)`.

``` cpp
template<class InputIterator>
  queue(InputIterator first, InputIterator last);
```

*Effects:* Initializes `c` with `first` as the first argument and `last`
as the second argument.

``` cpp
template<container-compatible-range<T> R>
  queue(from_range_t, R&& rg);
```

*Effects:* Initializes `c` with
`ranges::to<Container>(std::forward<R>(rg))`.

#### Constructors with allocators <a id="queue.cons.alloc">[[queue.cons.alloc]]</a>

If `uses_allocator_v<container_type, Alloc>` is `false` the constructors
in this subclause shall not participate in overload resolution.

``` cpp
template<class Alloc> explicit queue(const Alloc& a);
```

*Effects:* Initializes `c` with `a`.

``` cpp
template<class Alloc> queue(const container_type& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `cont` as the first argument and `a` as
the second argument.

``` cpp
template<class Alloc> queue(container_type&& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument.

``` cpp
template<class Alloc> queue(const queue& q, const Alloc& a);
```

*Effects:* Initializes `c` with `q.c` as the first argument and `a` as
the second argument.

``` cpp
template<class Alloc> queue(queue&& q, const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(q.c)` as the first argument
and `a` as the second argument.

``` cpp
template<class InputIterator, class Alloc>
  queue(InputIterator first, InputIterator last, const Alloc& alloc);
```

*Effects:* Initializes `c` with `first` as the first argument, `last` as
the second argument, and `alloc` as the third argument.

``` cpp
template<container-compatible-range<T> R, class Alloc>
  queue(from_range_t, R&& rg, const Alloc& a);
```

*Effects:* Initializes `c` with
`ranges::to<Container>(std::forward<R>(rg), a)`.

#### Modifiers <a id="queue.mod">[[queue.mod]]</a>

``` cpp
template<container-compatible-range<T> R>
  void push_range(R&& rg);
```

*Effects:* Equivalent to `c.append_range(std::forward<R>(rg))` if that
is a valid expression, otherwise `ranges::copy(rg, back_inserter(c))`.

#### Operators <a id="queue.ops">[[queue.ops]]</a>

``` cpp
template<class T, class Container>
  bool operator==(const queue<T, Container>& x, const queue<T, Container>& y);
```

*Returns:* `x.c == y.c`.

``` cpp
template<class T, class Container>
  bool operator!=(const queue<T, Container>& x,  const queue<T, Container>& y);
```

*Returns:* `x.c != y.c`.

``` cpp
template<class T, class Container>
  bool operator< (const queue<T, Container>& x, const queue<T, Container>& y);
```

*Returns:* `x.c < y.c`.

``` cpp
template<class T, class Container>
  bool operator> (const queue<T, Container>& x, const queue<T, Container>& y);
```

*Returns:* `x.c > y.c`.

``` cpp
template<class T, class Container>
  bool operator<=(const queue<T, Container>& x, const queue<T, Container>& y);
```

*Returns:* `x.c <= y.c`.

``` cpp
template<class T, class Container>
    bool operator>=(const queue<T, Container>& x,
                    const queue<T, Container>& y);
```

*Returns:* `x.c >= y.c`.

``` cpp
template<class T, three_way_comparable Container>
  compare_three_way_result_t<Container>
    operator<=>(const queue<T, Container>& x, const queue<T, Container>& y);
```

*Returns:* `x.c <=> y.c`.

#### Specialized algorithms <a id="queue.special">[[queue.special]]</a>

``` cpp
template<class T, class Container>
  void swap(queue<T, Container>& x, queue<T, Container>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `is_swappable_v<Container>` is `true`.

*Effects:* As if by `x.swap(y)`.

### Class template `priority_queue` <a id="priority.queue">[[priority.queue]]</a>

#### Overview <a id="priqueue.overview">[[priqueue.overview]]</a>

Any sequence container with random access iterator and supporting
operations `front()`, `push_back()` and `pop_back()` can be used to
instantiate `priority_queue`. In particular, `vector` [[vector]] and
`deque` [[deque]] can be used. Instantiating `priority_queue` also
involves supplying a function or function object for making priority
comparisons; the library assumes that the function or function object
defines a strict weak ordering [[alg.sorting]].

``` cpp
namespace std {
  template<class T, class Container = vector<T>,
           class Compare = less<typename Container::value_type>>
  class priority_queue {
  public:
    using value_type      = typename Container::value_type;
    using reference       = typename Container::reference;
    using const_reference = typename Container::const_reference;
    using size_type       = typename Container::size_type;
    using container_type  = Container;
    using value_compare   = Compare;

  protected:
    Container c;
    Compare comp;

  public:
    priority_queue() : priority_queue(Compare()) {}
    explicit priority_queue(const Compare& x) : priority_queue(x, Container()) {}
    priority_queue(const Compare& x, const Container&);
    priority_queue(const Compare& x, Container&&);
    template<class InputIterator>
      priority_queue(InputIterator first, InputIterator last, const Compare& x = Compare());
    template<class InputIterator>
      priority_queue(InputIterator first, InputIterator last, const Compare& x,
                     const Container&);
    template<class InputIterator>
      priority_queue(InputIterator first, InputIterator last, const Compare& x,
                     Container&&);
    template<container-compatible-range<T> R>
      priority_queue(from_range_t, R&& rg, const Compare& x = Compare());
    template<class Alloc> explicit priority_queue(const Alloc&);
    template<class Alloc> priority_queue(const Compare&, const Alloc&);
    template<class Alloc> priority_queue(const Compare&, const Container&, const Alloc&);
    template<class Alloc> priority_queue(const Compare&, Container&&, const Alloc&);
    template<class Alloc> priority_queue(const priority_queue&, const Alloc&);
    template<class Alloc> priority_queue(priority_queue&&, const Alloc&);
    template<class InputIterator, class Alloc>
      priority_queue(InputIterator, InputIterator, const Alloc&);
    template<class InputIterator, class Alloc>
      priority_queue(InputIterator, InputIterator, const Compare&, const Alloc&);
    template<class InputIterator, class Alloc>
      priority_queue(InputIterator, InputIterator, const Compare&, const Container&,
                     const Alloc&);
    template<class InputIterator, class Alloc>
      priority_queue(InputIterator, InputIterator, const Compare&, Container&&, const Alloc&);
    template<container-compatible-range<T> R, class Alloc>
      priority_queue(from_range_t, R&& rg, const Compare&, const Alloc&);
    template<container-compatible-range<T> R, class Alloc>
      priority_queue(from_range_t, R&& rg, const Alloc&);

    [[nodiscard]] bool empty() const { return c.empty(); }
    size_type size()  const          { return c.size(); }
    const_reference   top() const    { return c.front(); }
    void push(const value_type& x);
    void push(value_type&& x);
    template<container-compatible-range<T> R>
      void push_range(R&& rg);
    template<class... Args> void emplace(Args&&... args);
    void pop();
    void swap(priority_queue& q) noexcept(is_nothrow_swappable_v<Container> &&
                                          is_nothrow_swappable_v<Compare>)
      { using std::swap; swap(c, q.c); swap(comp, q.comp); }
  };

  template<class Compare, class Container>
    priority_queue(Compare, Container)
      -> priority_queue<typename Container::value_type, Container, Compare>;

  template<class InputIterator,
           class Compare = less<iter-value-type<InputIterator>>,
           class Container = vector<iter-value-type<InputIterator>>>
    priority_queue(InputIterator, InputIterator, Compare = Compare(), Container = Container())
      -> priority_queue<iter-value-type<InputIterator>, Container, Compare>;

  template<ranges::input_range R, class Compare = less<ranges::range_value_t<R>>>
    priority_queue(from_range_t, R&&, Compare = Compare())
      -> priority_queue<ranges::range_value_t<R>, vector<ranges::range_value_t<R>>, Compare>;

  template<class Compare, class Container, class Allocator>
    priority_queue(Compare, Container, Allocator)
      -> priority_queue<typename Container::value_type, Container, Compare>;

  template<class InputIterator, class Allocator>
    priority_queue(InputIterator, InputIterator, Allocator)
      -> priority_queue<iter-value-type<InputIterator>,
                        vector<iter-value-type<InputIterator>, Allocator>,
                        less<iter-value-type<InputIterator>>>;

  template<class InputIterator, class Compare, class Allocator>
    priority_queue(InputIterator, InputIterator, Compare, Allocator)
      -> priority_queue<iter-value-type<InputIterator>,
                        vector<iter-value-type<InputIterator>, Allocator>, Compare>;

  template<class InputIterator, class Compare, class Container, class Allocator>
    priority_queue(InputIterator, InputIterator, Compare, Container, Allocator)
      -> priority_queue<typename Container::value_type, Container, Compare>;

  template<ranges::input_range R, class Compare, class Allocator>
    priority_queue(from_range_t, R&&, Compare, Allocator)
      -> priority_queue<ranges::range_value_t<R>, vector<ranges::range_value_t<R>, Allocator>,
                        Compare>;

  template<ranges::input_range R, class Allocator>
    priority_queue(from_range_t, R&&, Allocator)
      -> priority_queue<ranges::range_value_t<R>, vector<ranges::range_value_t<R>, Allocator>>;

  // no equality is provided

  template<class T, class Container, class Compare, class Alloc>
    struct uses_allocator<priority_queue<T, Container, Compare>, Alloc>
      : uses_allocator<Container, Alloc>::type { };
}
```

#### Constructors <a id="priqueue.cons">[[priqueue.cons]]</a>

``` cpp
priority_queue(const Compare& x, const Container& y);
priority_queue(const Compare& x, Container&& y);
```

*Preconditions:* `x` defines a strict weak ordering [[alg.sorting]].

*Effects:* Initializes `comp` with `x` and `c` with `y` (copy
constructing or move constructing as appropriate); calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class InputIterator>
  priority_queue(InputIterator first, InputIterator last, const Compare& x = Compare());
```

*Preconditions:* `x` defines a strict weak ordering [[alg.sorting]].

*Effects:* Initializes `c` with `first` as the first argument and `last`
as the second argument, and initializes `comp` with `x`; then calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class InputIterator>
  priority_queue(InputIterator first, InputIterator last, const Compare& x, const Container& y);
template<class InputIterator>
  priority_queue(InputIterator first, InputIterator last, const Compare& x, Container&& y);
```

*Preconditions:* `x` defines a strict weak ordering [[alg.sorting]].

*Effects:* Initializes `comp` with `x` and `c` with `y` (copy
constructing or move constructing as appropriate); calls
`c.insert(c.end(), first, last)`; and finally calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<container-compatible-range<T> R>
  priority_queue(from_range_t, R&& rg, const Compare& x = Compare());
```

*Preconditions:* `x` defines a strict weak ordering [[alg.sorting]].

*Effects:* Initializes `comp` with `x` and `c` with
`ranges::to<Container>(std::forward<R>(rg))` and finally calls
`make_heap(c.begin(), c.end(), comp)`.

#### Constructors with allocators <a id="priqueue.cons.alloc">[[priqueue.cons.alloc]]</a>

If `uses_allocator_v<container_type, Alloc>` is `false` the constructors
in this subclause shall not participate in overload resolution.

``` cpp
template<class Alloc> explicit priority_queue(const Alloc& a);
```

*Effects:* Initializes `c` with `a` and value-initializes `comp`.

``` cpp
template<class Alloc> priority_queue(const Compare& compare, const Alloc& a);
```

*Effects:* Initializes `c` with `a` and initializes `comp` with
`compare`.

``` cpp
template<class Alloc>
  priority_queue(const Compare& compare, const Container& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `cont` as the first argument and `a` as
the second argument, and initializes `comp` with `compare`; calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class Alloc>
  priority_queue(const Compare& compare, Container&& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument, and initializes `comp` with `compare`;
calls `make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class Alloc> priority_queue(const priority_queue& q, const Alloc& a);
```

*Effects:* Initializes `c` with `q.c` as the first argument and `a` as
the second argument, and initializes `comp` with `q.comp`.

``` cpp
template<class Alloc> priority_queue(priority_queue&& q, const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(q.c)` as the first argument
and `a` as the second argument, and initializes `comp` with
`std::move(q.comp)`.

``` cpp
template<class InputIterator, class Alloc>
  priority_queue(InputIterator first, InputIterator last, const Alloc& a);
```

*Effects:* Initializes `c` with `first` as the first argument, `last` as
the second argument, and `a` as the third argument, and
value-initializes `comp`; calls `make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class InputIterator, class Alloc>
  priority_queue(InputIterator first, InputIterator last, const Compare& compare, const Alloc& a);
```

*Effects:* Initializes `c` with `first` as the first argument, `last` as
the second argument, and `a` as the third argument, and initializes
`comp` with `compare`; calls `make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class InputIterator, class Alloc>
  priority_queue(InputIterator first, InputIterator last, const Compare& compare,
                 const Container& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `cont` as the first argument and `a` as
the second argument, and initializes `comp` with `compare`; calls
`c.insert(c.end(), first, last)`; and finally calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<class InputIterator, class Alloc>
  priority_queue(InputIterator first, InputIterator last, const Compare& compare, Container&& cont,
                 const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument, and initializes `comp` with `compare`;
calls `c.insert(c.end(), first, last)`; and finally calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<container-compatible-range<T> R, class Alloc>
  priority_queue(from_range_t, R&& rg, const Compare& compare, const Alloc& a);
```

*Effects:* Initializes `comp` with `compare` and `c` with
`ranges::to<Container>(std::forward<R>(rg), a)`; calls
`make_heap(c.begin(), c.end(), comp)`.

``` cpp
template<container-compatible-range<T> R, class Alloc>
  priority_queue(from_range_t, R&& rg, const Alloc& a);
```

*Effects:* Initializes `c` with
`ranges::to<Container>(std::forward<R>(rg), a)`; calls
`make_heap(c.begin(), c.end(), comp)`.

#### Members <a id="priqueue.members">[[priqueue.members]]</a>

``` cpp
void push(const value_type& x);
```

*Effects:* As if by:

``` cpp
c.push_back(x);
push_heap(c.begin(), c.end(), comp);
```

``` cpp
void push(value_type&& x);
```

*Effects:* As if by:

``` cpp
c.push_back(std::move(x));
push_heap(c.begin(), c.end(), comp);
```

``` cpp
template<container-compatible-range<T> R>
  void push_range(R&& rg);
```

*Effects:* Inserts all elements of `rg` in `c` via
`c.append_range(std::forward<R>(rg))` if that is a valid expression, or
`ranges::copy(rg, back_inserter(c))` otherwise. Then restores the heap
property as if by `make_heap(c.begin(), c.end(), comp)`.

*Ensures:* `is_heap(c.begin(), c.end(), comp)` is `true`.

``` cpp
template<class... Args> void emplace(Args&&... args);
```

*Effects:* As if by:

``` cpp
c.emplace_back(std::forward<Args>(args)...);
push_heap(c.begin(), c.end(), comp);
```

``` cpp
void pop();
```

*Effects:* As if by:

``` cpp
pop_heap(c.begin(), c.end(), comp);
c.pop_back();
```

#### Specialized algorithms <a id="priqueue.special">[[priqueue.special]]</a>

``` cpp
template<class T, class Container, class Compare>
  void swap(priority_queue<T, Container, Compare>& x,
            priority_queue<T, Container, Compare>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `is_swappable_v<Container>` is `true` and
`is_swappable_v<Compare>` is `true`.

*Effects:* As if by `x.swap(y)`.

### Class template `stack` <a id="stack">[[stack]]</a>

#### General <a id="stack.general">[[stack.general]]</a>

Any sequence container supporting operations `back()`, `push_back()` and
`pop_back()` can be used to instantiate `stack`. In particular, `vector`
[[vector]], `list` [[list]] and `deque` [[deque]] can be used.

#### Definition <a id="stack.defn">[[stack.defn]]</a>

``` cpp
namespace std {
  template<class T, class Container = deque<T>>
  class stack {
  public:
    using value_type      = typename Container::value_type;
    using reference       = typename Container::reference;
    using const_reference = typename Container::const_reference;
    using size_type       = typename Container::size_type;
    using container_type  = Container;

  protected:
    Container c;

  public:
    stack() : stack(Container()) {}
    explicit stack(const Container&);
    explicit stack(Container&&);
    template<class InputIterator> stack(InputIterator first, InputIterator last);
    template<container-compatible-range<T> R> stack(from_range_t, R&& rg);
    template<class Alloc> explicit stack(const Alloc&);
    template<class Alloc> stack(const Container&, const Alloc&);
    template<class Alloc> stack(Container&&, const Alloc&);
    template<class Alloc> stack(const stack&, const Alloc&);
    template<class Alloc> stack(stack&&, const Alloc&);
    template<class InputIterator, class Alloc>
      stack(InputIterator first, InputIterator last, const Alloc&);
    template<container-compatible-range<T> R, class Alloc>
      stack(from_range_t, R&& rg, const Alloc&);

    [[nodiscard]] bool empty() const    { return c.empty(); }
    size_type size()  const             { return c.size(); }
    reference         top()             { return c.back(); }
    const_reference   top() const       { return c.back(); }
    void push(const value_type& x)      { c.push_back(x); }
    void push(value_type&& x)           { c.push_back(std::move(x)); }
    template<container-compatible-range<T> R>
      void push_range(R&& rg);
    template<class... Args>
      decltype(auto) emplace(Args&&... args)
        { return c.emplace_back(std::forward<Args>(args)...); }
    void pop()                          { c.pop_back(); }
    void swap(stack& s) noexcept(is_nothrow_swappable_v<Container>)
      { using std::swap; swap(c, s.c); }
  };

  template<class Container>
    stack(Container) -> stack<typename Container::value_type, Container>;

  template<class InputIterator>
    stack(InputIterator, InputIterator) -> stack<iter-value-type<InputIterator>>;

  template<ranges::input_range R>
    stack(from_range_t, R&&) -> stack<ranges::range_value_t<R>>;

  template<class Container, class Allocator>
    stack(Container, Allocator) -> stack<typename Container::value_type, Container>;

  template<class InputIterator, class Allocator>
    stack(InputIterator, InputIterator, Allocator)
      -> stack<iter-value-type<InputIterator>, deque<iter-value-type<InputIterator>,
               Allocator>>;

  template<ranges::input_range R, class Allocator>
    stack(from_range_t, R&&, Allocator)
      -> stack<ranges::range_value_t<R>, deque<ranges::range_value_t<R>, Allocator>>;

  template<class T, class Container, class Alloc>
    struct uses_allocator<stack<T, Container>, Alloc>
      : uses_allocator<Container, Alloc>::type { };
}
```

#### Constructors <a id="stack.cons">[[stack.cons]]</a>

``` cpp
explicit stack(const Container& cont);
```

*Effects:* Initializes `c` with `cont`.

``` cpp
explicit stack(Container&& cont);
```

*Effects:* Initializes `c` with `std::move(cont)`.

``` cpp
template<class InputIterator>
  stack(InputIterator first, InputIterator last);
```

*Effects:* Initializes `c` with `first` as the first argument and `last`
as the second argument.

``` cpp
template<container-compatible-range<T> R>
  stack(from_range_t, R&& rg);
```

*Effects:* Initializes `c` with
`ranges::to<Container>(std::forward<R>(rg))`.

#### Constructors with allocators <a id="stack.cons.alloc">[[stack.cons.alloc]]</a>

If `uses_allocator_v<container_type, Alloc>` is `false` the constructors
in this subclause shall not participate in overload resolution.

``` cpp
template<class Alloc> explicit stack(const Alloc& a);
```

*Effects:* Initializes `c` with `a`.

``` cpp
template<class Alloc> stack(const container_type& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `cont` as the first argument and `a` as
the second argument.

``` cpp
template<class Alloc> stack(container_type&& cont, const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(cont)` as the first argument
and `a` as the second argument.

``` cpp
template<class Alloc> stack(const stack& s, const Alloc& a);
```

*Effects:* Initializes `c` with `s.c` as the first argument and `a` as
the second argument.

``` cpp
template<class Alloc> stack(stack&& s, const Alloc& a);
```

*Effects:* Initializes `c` with `std::move(s.c)` as the first argument
and `a` as the second argument.

``` cpp
template<class InputIterator, class Alloc>
  stack(InputIterator first, InputIterator last, const Alloc& alloc);
```

*Effects:* Initializes `c` with `first` as the first argument, `last` as
the second argument, and `alloc` as the third argument.

``` cpp
template<container-compatible-range<T> R, class Alloc>
  stack(from_range_t, R&& rg, const Alloc& a);
```

*Effects:* Initializes `c` with
`ranges::to<Container>(std::forward<R>(rg), a)`.

#### Modifiers <a id="stack.mod">[[stack.mod]]</a>

``` cpp
template<container-compatible-range<T> R>
  void push_range(R&& rg);
```

*Effects:* Equivalent to `c.append_range(std::forward<R>(rg))` if that
is a valid expression, otherwise `ranges::copy(rg, back_inserter(c))`.

#### Operators <a id="stack.ops">[[stack.ops]]</a>

``` cpp
template<class T, class Container>
  bool operator==(const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c == y.c`.

``` cpp
template<class T, class Container>
  bool operator!=(const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c != y.c`.

``` cpp
template<class T, class Container>
  bool operator< (const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c < y.c`.

``` cpp
template<class T, class Container>
  bool operator> (const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c > y.c`.

``` cpp
template<class T, class Container>
  bool operator<=(const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c <= y.c`.

``` cpp
template<class T, class Container>
  bool operator>=(const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c >= y.c`.

``` cpp
template<class T, three_way_comparable Container>
  compare_three_way_result_t<Container>
    operator<=>(const stack<T, Container>& x, const stack<T, Container>& y);
```

*Returns:* `x.c <=> y.c`.

#### Specialized algorithms <a id="stack.special">[[stack.special]]</a>

``` cpp
template<class T, class Container>
  void swap(stack<T, Container>& x, stack<T, Container>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `is_swappable_v<Container>` is `true`.

*Effects:* As if by `x.swap(y)`.

### Class template `flat_map` <a id="flat.map">[[flat.map]]</a>

#### Overview <a id="flat.map.overview">[[flat.map.overview]]</a>

A `flat_map` is a container adaptor that provides an associative
container interface that supports unique keys (i.e., contains at most
one of each key value) and provides for fast retrieval of values of
another type `T` based on the keys. `flat_map` supports iterators that
meet the *Cpp17InputIterator* requirements and model the
`random_access_iterator` concept [[iterator.concept.random.access]].

A `flat_map` meets all of the requirements of a container
[[container.reqmts]] and of a reversible container
[[container.rev.reqmts]], plus the optional container requirements
[[container.opt.reqmts]]. `flat_map` meets the requirements of an
associative container [[associative.reqmts]], except that:

- it does not meet the requirements related to node handles
  [[container.node]],
- it does not meet the requirements related to iterator invalidation,
  and
- the time complexity of the operations that insert or erase a single
  element from the map is linear, including the ones that take an
  insertion position iterator.

[*Note 1*: A `flat_map` does not meet the additional requirements of an
allocator-aware container [[container.alloc.reqmts]]. — *end note*]

A `flat_map` also provides most operations described in
[[associative.reqmts]] for unique keys. This means that a `flat_map`
supports the `a_uniq` operations in [[associative.reqmts]] but not the
`a_eq` operations. For a `flat_map<Key, T>` the `key_type` is `Key` and
the `value_type` is `pair<Key, T>`.

Descriptions are provided here only for operations on `flat_map` that
are not described in one of those sets of requirements or for operations
where there is additional semantic information.

A `flat_map` maintains the following invariants:

- it contains the same number of keys and values;
- the keys are sorted with respect to the comparison object; and
- the value at offset `off` within the value container is the value
  associated with the key at offset `off` within the key container.

If any member function in [[flat.map.defn]] exits via an exception the
invariants are restored.

[*Note 2*: This can result in the `flat_map` being
emptied. — *end note*]

Any type `C` that meets the sequence container requirements
[[sequence.reqmts]] can be used to instantiate `flat_map`, as long as
`C::iterator` meets the *Cpp17RandomAccessIterator* requirements and
invocations of member functions `C::size` and `C::max_size` do not exit
via an exception. In particular, `vector` [[vector]] and `deque`
[[deque]] can be used.

[*Note 3*: `vector<bool>` is not a sequence container. — *end note*]

The program is ill-formed if `Key` is not the same type as
`KeyContainer::value_type` or `T` is not the same type as
`MappedContainer::value_type`.

The effect of calling a constructor that takes both `key_container_type`
and `mapped_container_type` arguments with containers of different sizes
is undefined.

The effect of calling a constructor or member function that takes a
`sorted_unique_t` argument with a container, containers, or range that
is not sorted with respect to `key_comp()`, or that contains equal
elements, is undefined.

#### Definition <a id="flat.map.defn">[[flat.map.defn]]</a>

``` cpp
namespace std {
  template<class Key, class T, class Compare = less<Key>,
           class KeyContainer = vector<Key>, class MappedContainer = vector<T>>
  class flat_map {
  public:
    // types
    using key_type               = Key;
    using mapped_type            = T;
    using value_type             = pair<key_type, mapped_type>;
    using key_compare            = Compare;
    using reference              = pair<const key_type&, mapped_type&>;
    using const_reference        = pair<const key_type&, const mapped_type&>;
    using size_type              = size_t;
    using difference_type        = ptrdiff_t;
    using iterator               = implementation-defined  // type of flat_map::iterator; // see [container.requirements]
    using const_iterator         = implementation-defined  // type of flat_map::const_iterator; // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    using key_container_type     = KeyContainer;
    using mapped_container_type  = MappedContainer;

    class value_compare {
    private:
      key_compare comp;                                 // exposition only
      value_compare(key_compare c) : comp(c) { }        // exposition only

    public:
      bool operator()(const_reference x, const_reference y) const {
        return comp(x.first, y.first);
      }
    };

    struct containers {
      key_container_type keys;
      mapped_container_type values;
    };

    // [flat.map.cons], construct/copy/destroy
    flat_map() : flat_map(key_compare()) { }

    flat_map(key_container_type key_cont, mapped_container_type mapped_cont,
             const key_compare& comp = key_compare());
    template<class Allocator>
      flat_map(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
               const Allocator& a);
    template<class Allocator>
      flat_map(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
               const key_compare& comp, const Allocator& a);

    flat_map(sorted_unique_t, key_container_type key_cont, mapped_container_type mapped_cont,
             const key_compare& comp = key_compare());
    template<class Allocator>
      flat_map(sorted_unique_t, const key_container_type& key_cont,
               const mapped_container_type& mapped_cont, const Allocator& a);
    template<class Allocator>
      flat_map(sorted_unique_t, const key_container_type& key_cont,
               const mapped_container_type& mapped_cont,
               const key_compare& comp, const Allocator& a);

    explicit flat_map(const key_compare& comp)
      : c(), compare(comp) { }
    template<class Allocator>
      flat_map(const key_compare& comp, const Allocator& a);
    template<class Allocator>
      explicit flat_map(const Allocator& a);

    template<class InputIterator>
      flat_map(InputIterator first, InputIterator last, const key_compare& comp = key_compare())
        : c(), compare(comp) { insert(first, last); }
    template<class InputIterator, class Allocator>
      flat_map(InputIterator first, InputIterator last,
               const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_map(InputIterator first, InputIterator last, const Allocator& a);

    template<container-compatible-range<value_type> R>
      flat_map(from_range_t fr, R&& rg)
        : flat_map(fr, std::forward<R>(rg), key_compare()) { }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_map(from_range_t, R&& rg, const Allocator& a);
    template<container-compatible-range<value_type> R>
      flat_map(from_range_t, R&& rg, const key_compare& comp)
        : flat_map(comp) { insert_range(std::forward<R>(rg)); }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_map(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);

    template<class InputIterator>
      flat_map(sorted_unique_t s, InputIterator first, InputIterator last,
               const key_compare& comp = key_compare())
        : c(), compare(comp) { insert(s, first, last); }
    template<class InputIterator, class Allocator>
      flat_map(sorted_unique_t, InputIterator first, InputIterator last,
               const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_map(sorted_unique_t, InputIterator first, InputIterator last, const Allocator& a);

    flat_map(initializer_list<value_type> il, const key_compare& comp = key_compare())
        : flat_map(il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_map(initializer_list<value_type> il, const key_compare& comp, const Allocator& a);
    template<class Allocator>
      flat_map(initializer_list<value_type> il, const Allocator& a);

    flat_map(sorted_unique_t s, initializer_list<value_type> il,
             const key_compare& comp = key_compare())
        : flat_map(s, il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_map(sorted_unique_t, initializer_list<value_type> il,
               const key_compare& comp, const Allocator& a);
    template<class Allocator>
      flat_map(sorted_unique_t, initializer_list<value_type> il, const Allocator& a);

    flat_map& operator=(initializer_list<value_type> il);

    // iterators
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

    // [flat.map.capacity], capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [flat.map.access], element access
    mapped_type& operator[](const key_type& x);
    mapped_type& operator[](key_type&& x);
    template<class K> mapped_type& operator[](K&& x);
    mapped_type& at(const key_type& x);
    const mapped_type& at(const key_type& x) const;
    template<class K> mapped_type& at(const K& x);
    template<class K> const mapped_type& at(const K& x) const;

    // [flat.map.modifiers], modifiers
    template<class... Args> pair<iterator, bool> emplace(Args&&... args);
    template<class... Args>
      iterator emplace_hint(const_iterator position, Args&&... args);

    pair<iterator, bool> insert(const value_type& x)
      { return emplace(x); }
    pair<iterator, bool> insert(value_type&& x)
      { return emplace(std::move(x)); }
    iterator insert(const_iterator position, const value_type& x)
      { return emplace_hint(position, x); }
    iterator insert(const_iterator position, value_type&& x)
      { return emplace_hint(position, std::move(x)); }

    template<class P> pair<iterator, bool> insert(P&& x);
    template<class P>
      iterator insert(const_iterator position, P&&);
    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<class InputIterator>
      void insert(sorted_unique_t, InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);

    void insert(initializer_list<value_type> il)
      { insert(il.begin(), il.end()); }
    void insert(sorted_unique_t s, initializer_list<value_type> il)
      { insert(s, il.begin(), il.end()); }

    containers extract() &&;
    void replace(key_container_type&& key_cont, mapped_container_type&& mapped_cont);

    template<class... Args>
      pair<iterator, bool> try_emplace(const key_type& k, Args&&... args);
    template<class... Args>
      pair<iterator, bool> try_emplace(key_type&& k, Args&&... args);
    template<class K, class... Args>
      pair<iterator, bool> try_emplace(K&& k, Args&&... args);
    template<class... Args>
      iterator try_emplace(const_iterator hint, const key_type& k, Args&&... args);
    template<class... Args>
      iterator try_emplace(const_iterator hint, key_type&& k, Args&&... args);
    template<class K, class... Args>
      iterator try_emplace(const_iterator hint, K&& k, Args&&... args);
    template<class M>
      pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
    template<class M>
      pair<iterator, bool> insert_or_assign(key_type&& k, M&& obj);
    template<class K, class M>
      pair<iterator, bool> insert_or_assign(K&& k, M&& obj);
    template<class M>
      iterator insert_or_assign(const_iterator hint, const key_type& k, M&& obj);
    template<class M>
      iterator insert_or_assign(const_iterator hint, key_type&& k, M&& obj);
    template<class K, class M>
      iterator insert_or_assign(const_iterator hint, K&& k, M&& obj);

    iterator erase(iterator position);
    iterator erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator erase(const_iterator first, const_iterator last);

    void swap(flat_map& y) noexcept;
    void clear() noexcept;

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    const key_container_type& keys() const noexcept      { return c.keys; }
    const mapped_container_type& values() const noexcept { return c.values; }

    // map operations
    iterator find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator> equal_range(const key_type& x);
    pair<const_iterator, const_iterator> equal_range(const key_type& x) const;
    template<class K> pair<iterator, iterator> equal_range(const K& x);
    template<class K> pair<const_iterator, const_iterator> equal_range(const K& x) const;

    friend bool operator==(const flat_map& x, const flat_map& y);

    friend synth-three-way-result<value_type>
      operator<=>(const flat_map& x, const flat_map& y);

    friend void swap(flat_map& x, flat_map& y) noexcept
      { x.swap(y); }

  private:
    containers c;               // exposition only
    key_compare compare;        // exposition only

    struct key_equiv {  // exposition only
      key_equiv(key_compare c) : comp(c) { }
      bool operator()(const_reference x, const_reference y) const {
        return !comp(x.first, y.first) && !comp(y.first, x.first);
      }
      key_compare comp;
    };
  };

  template<class KeyContainer, class MappedContainer,
           class Compare = less<typename KeyContainer::value_type>>
    flat_map(KeyContainer, MappedContainer, Compare = Compare())
      -> flat_map<typename KeyContainer::value_type, typename MappedContainer::value_type,
                  Compare, KeyContainer, MappedContainer>;

  template<class KeyContainer, class MappedContainer, class Allocator>
    flat_map(KeyContainer, MappedContainer, Allocator)
      -> flat_map<typename KeyContainer::value_type, typename MappedContainer::value_type,
                  less<typename KeyContainer::value_type>, KeyContainer, MappedContainer>;
  template<class KeyContainer, class MappedContainer, class Compare, class Allocator>
    flat_map(KeyContainer, MappedContainer, Compare, Allocator)
      -> flat_map<typename KeyContainer::value_type, typename MappedContainer::value_type,
                  Compare, KeyContainer, MappedContainer>;

  template<class KeyContainer, class MappedContainer,
           class Compare = less<typename KeyContainer::value_type>>
    flat_map(sorted_unique_t, KeyContainer, MappedContainer, Compare = Compare())
      -> flat_map<typename KeyContainer::value_type, typename MappedContainer::value_type,
                  Compare, KeyContainer, MappedContainer>;

  template<class KeyContainer, class MappedContainer, class Allocator>
    flat_map(sorted_unique_t, KeyContainer, MappedContainer, Allocator)
      -> flat_map<typename KeyContainer::value_type, typename MappedContainer::value_type,
                  less<typename KeyContainer::value_type>, KeyContainer, MappedContainer>;
  template<class KeyContainer, class MappedContainer, class Compare, class Allocator>
    flat_map(sorted_unique_t, KeyContainer, MappedContainer, Compare, Allocator)
      -> flat_map<typename KeyContainer::value_type, typename MappedContainer::value_type,
                  Compare, KeyContainer, MappedContainer>;

  template<class InputIterator, class Compare = less<iter-key-type<InputIterator>>>
    flat_map(InputIterator, InputIterator, Compare = Compare())
      -> flat_map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Compare>;

  template<class InputIterator, class Compare = less<iter-key-type<InputIterator>>>
    flat_map(sorted_unique_t, InputIterator, InputIterator, Compare = Compare())
      -> flat_map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Compare>;

  template<ranges::input_range R, class Compare = less<range-key-type<R>>,
           class Allocator = allocator<byte>>
    flat_map(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> flat_map<range-key-type<R>, range-mapped-type<R>, Compare,
                  vector<range-key-type<R>, alloc-rebind<Allocator, range-key-type<R>>>,
                  vector<range-mapped-type<R>, alloc-rebind<Allocator, range-mapped-type<R>>>>;

  template<ranges::input_range R, class Allocator>
    flat_map(from_range_t, R&&, Allocator)
      -> flat_map<range-key-type<R>, range-mapped-type<R>, less<range-key-type<R>>,
                  vector<range-key-type<R>, alloc-rebind<Allocator, range-key-type<R>>>,
                  vector<range-mapped-type<R>, alloc-rebind<Allocator, range-mapped-type<R>>>>;

  template<class Key, class T, class Compare = less<Key>>
    flat_map(initializer_list<pair<Key, T>>, Compare = Compare())
      -> flat_map<Key, T, Compare>;

  template<class Key, class T, class Compare = less<Key>>
    flat_map(sorted_unique_t, initializer_list<pair<Key, T>>, Compare = Compare())
        -> flat_map<Key, T, Compare>;

  template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
            class Allocator>
    struct uses_allocator<flat_map<Key, T, Compare, KeyContainer, MappedContainer>, Allocator>
      : bool_constant<uses_allocator_v<KeyContainer, Allocator> &&
                      uses_allocator_v<MappedContainer, Allocator>> { };
}
```

The member type `containers` has the data members and special members
specified above. It has no base classes or members other than those
specified.

#### Constructors <a id="flat.map.cons">[[flat.map.cons]]</a>

``` cpp
flat_map(key_container_type key_cont, mapped_container_type mapped_cont,
         const key_compare& comp = key_compare());
```

*Effects:* Initializes `c.keys` with `std::move(key_cont)`, `c.values`
with `std::move(mapped_cont)`, and `compare` with `comp`; sorts the
range \[`begin()`, `end()`) with respect to `value_comp()`; and finally
erases the duplicate elements as if by:

``` cpp
auto zv = ranges::zip_view(c.keys, c.values);
auto it = ranges::unique(zv, key_equiv(compare)).begin();
auto dist = distance(zv.begin(), it);
c.keys.erase(c.keys.begin() + dist, c.keys.end());
c.values.erase(c.values.begin() + dist, c.values.end());
```

*Complexity:* Linear in N if the container arguments are already sorted
with respect to `value_comp()` and otherwise N log N, where N is the
value of `key_cont.size()` before this call.

``` cpp
template<class Allocator>
  flat_map(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
           const Allocator& a);
template<class Allocator>
  flat_map(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
           const key_compare& comp, const Allocator& a);
```

*Constraints:* `uses_allocator_v<key_container_type, Allocator>` is
`true` and `uses_allocator_v<mapped_container_type, Allocator>` is
`true`.

*Effects:* Equivalent to `flat_map(key_cont, mapped_cont)` and
`flat_map(key_cont, mapped_cont, comp)`, respectively, except that
`c.keys` and `c.values` are constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Same as `flat_map(key_cont, mapped_cont)` and
`flat_map(key_cont, mapped_cont, comp)`, respectively.

``` cpp
flat_map(sorted_unique_t, key_container_type key_cont, mapped_container_type mapped_cont,
         const key_compare& comp = key_compare());
```

*Effects:* Initializes `c.keys` with `std::move(key_cont)`, `c.values`
with `std::move(mapped_cont)`, and `compare` with `comp`.

*Complexity:* Constant.

``` cpp
template<class Allocator>
  flat_map(sorted_unique_t s, const key_container_type& key_cont,
           const mapped_container_type& mapped_cont, const Allocator& a);
template<class Allocator>
  flat_map(sorted_unique_t s, const key_container_type& key_cont,
           const mapped_container_type& mapped_cont, const key_compare& comp,
           const Allocator& a);
```

*Constraints:* `uses_allocator_v<key_container_type, Allocator>` is
`true` and `uses_allocator_v<mapped_container_type, Allocator>` is
`true`.

*Effects:* Equivalent to `flat_map(s, key_cont, mapped_cont)` and
`flat_map(s, key_cont, mapped_cont, comp)`, respectively, except that
`c.keys` and `c.values` are constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Linear.

``` cpp
template<class Allocator>
  flat_map(const key_compare& comp, const Allocator& a);
template<class Allocator>
  explicit flat_map(const Allocator& a);
template<class InputIterator, class Allocator>
  flat_map(InputIterator first, InputIterator last, const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_map(InputIterator first, InputIterator last, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_map(from_range_t, R&& rg, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_map(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_map(sorted_unique_t, InputIterator first, InputIterator last,
           const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_map(sorted_unique_t, InputIterator first, InputIterator last, const Allocator& a);
template<class Allocator>
  flat_map(initializer_list<value_type> il, const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_map(initializer_list<value_type> il, const Allocator& a);
template<class Allocator>
  flat_map(sorted_unique_t, initializer_list<value_type> il,
           const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_map(sorted_unique_t, initializer_list<value_type> il, const Allocator& a);
```

*Constraints:* `uses_allocator_v<key_container_type, Allocator>` is
`true` and `uses_allocator_v<mapped_container_type, Allocator>` is
`true`.

*Effects:* Equivalent to the corresponding non-allocator constructors
except that `c.keys` and `c.values` are constructed with uses-allocator
construction [[allocator.uses.construction]].

#### Capacity <a id="flat.map.capacity">[[flat.map.capacity]]</a>

``` cpp
size_type size() const noexcept;
```

*Returns:* `c.keys.size()`.

``` cpp
size_type max_size() const noexcept;
```

*Returns:* `min<size_type>(c.keys.max_size(), c.values.max_size())`.

#### Access <a id="flat.map.access">[[flat.map.access]]</a>

``` cpp
mapped_type& operator[](const key_type& x);
```

*Effects:* Equivalent to: `return try_emplace(x).first->second;`

``` cpp
mapped_type& operator[](key_type&& x);
```

*Effects:* Equivalent to:
`return try_emplace(std::move(x)).first->second;`

``` cpp
template<class K> mapped_type& operator[](K&& x);
```

*Constraints:* The *qualified-id* `Compare::is_transparent` is valid and
denotes a type.

*Effects:* Equivalent to:
`return try_emplace(std::forward<K>(x)).first->second;`

``` cpp
mapped_type&       at(const key_type& x);
const mapped_type& at(const key_type& x) const;
```

*Returns:* A reference to the `mapped_type` corresponding to `x` in
`*this`.

*Throws:* An exception object of type `out_of_range` if no such element
is present.

*Complexity:* Logarithmic.

``` cpp
template<class K> mapped_type&       at(const K& x);
template<class K> const mapped_type& at(const K& x) const;
```

*Constraints:* The *qualified-id* `Compare::is_transparent` is valid and
denotes a type.

*Preconditions:* The expression `find(x)` is well-formed and has
well-defined behavior.

*Returns:* A reference to the `mapped_type` corresponding to `x` in
`*this`.

*Throws:* An exception object of type `out_of_range` if no such element
is present.

*Complexity:* Logarithmic.

#### Modifiers <a id="flat.map.modifiers">[[flat.map.modifiers]]</a>

``` cpp
template<class... Args> pair<iterator, bool> emplace(Args&&... args);
```

*Constraints:*
`is_constructible_v<pair<key_type, mapped_type>, Args...>` is `true`.

*Effects:* Initializes an object `t` of type
`pair<key_type, mapped_type>` with `std::forward<Args>(args)...`; if the
map already contains an element whose key is equivalent to `t.first`,
`*this` is unchanged. Otherwise, equivalent to:

``` cpp
auto key_it = ranges::upper_bound(c.keys, t.first, compare);
auto value_it = c.values.begin() + distance(c.keys.begin(), key_it);
c.keys.insert(key_it, std::move(t.first));
c.values.insert(value_it, std::move(t.second));
```

*Returns:* The `bool` component of the returned pair is `true` if and
only if the insertion took place, and the iterator component of the pair
points to the element with key equivalent to `t.first`.

``` cpp
template<class P> pair<iterator, bool> insert(P&& x);
template<class P> iterator insert(const_iterator position, P&& x);
```

*Constraints:* `is_constructible_v<pair<key_type, mapped_type>, P>` is
`true`.

*Effects:* The first form is equivalent to
`return emplace(std::forward<P>(x));`. The second form is equivalent to
`return emplace_hint(position, std::forward<P>(x));`.

``` cpp
template<class InputIterator>
  void insert(InputIterator first, InputIterator last);
```

*Effects:* Adds elements to `c` as if by:

``` cpp
for (; first != last; ++first) {
  value_type value = *first;
  c.keys.insert(c.keys.end(), std::move(value.first));
  c.values.insert(c.values.end(), std::move(value.second));
}
```

Then, sorts the range of newly inserted elements with respect to
`value_comp()`; merges the resulting sorted range and the sorted range
of pre-existing elements into a single sorted range; and finally erases
the duplicate elements as if by:

``` cpp
auto zv = ranges::zip_view(c.keys, c.values);
auto it = ranges::unique(zv, key_equiv(compare)).begin();
auto dist = distance(zv.begin(), it);
c.keys.erase(c.keys.begin() + dist, c.keys.end());
c.values.erase(c.values.begin() + dist, c.values.end());
```

*Complexity:* N + M log M, where N is `size()` before the operation and
M is `distance(first, last)`.

*Remarks:* Since this operation performs an in-place merge, it may
allocate memory.

``` cpp
template<class InputIterator>
  void insert(sorted_unique_t, InputIterator first, InputIterator last);
```

*Effects:* Adds elements to `c` as if by:

``` cpp
for (; first != last; ++first) {
  value_type value = *first;
  c.keys.insert(c.keys.end(), std::move(value.first));
  c.values.insert(c.values.end(), std::move(value.second));
}
```

Then, merges the sorted range of newly added elements and the sorted
range of pre-existing elements into a single sorted range; and finally
erases the duplicate elements as if by:

``` cpp
auto zv = ranges::zip_view(c.keys, c.values);
auto it = ranges::unique(zv, key_equiv(compare)).begin();
auto dist = distance(zv.begin(), it);
c.keys.erase(c.keys.begin() + dist, c.keys.end());
c.values.erase(c.values.begin() + dist, c.values.end());
```

*Complexity:* Linear in N, where N is `size()` after the operation.

*Remarks:* Since this operation performs an in-place merge, it may
allocate memory.

``` cpp
template<container-compatible-range<value_type> R>
  void insert_range(R&& rg);
```

*Effects:* Adds elements to `c` as if by:

``` cpp
for (const auto& e : rg) {
  c.keys.insert(c.keys.end(), e.first);
  c.values.insert(c.values.end(), e.second);
}
```

Then, sorts the range of newly inserted elements with respect to
`value_comp()`; merges the resulting sorted range and the sorted range
of pre-existing elements into a single sorted range; and finally erases
the duplicate elements as if by:

``` cpp
auto zv = ranges::zip_view(c.keys, c.values);
auto it = ranges::unique(zv, key_equiv(compare)).begin();
auto dist = distance(zv.begin(), it);
c.keys.erase(c.keys.begin() + dist, c.keys.end());
c.values.erase(c.values.begin() + dist, c.values.end());
```

*Complexity:* N + M log M, where N is `size()` before the operation and
M is `ranges::distance(rg)`.

*Remarks:* Since this operation performs an in-place merge, it may
allocate memory.

``` cpp
template<class... Args>
  pair<iterator, bool> try_emplace(const key_type& k, Args&&... args);
template<class... Args>
  pair<iterator, bool> try_emplace(key_type&& k, Args&&... args);
template<class... Args>
  iterator try_emplace(const_iterator hint, const key_type& k, Args&&... args);
template<class... Args>
  iterator try_emplace(const_iterator hint, key_type&& k, Args&&... args);
```

*Constraints:* `is_constructible_v<mapped_type, Args...>` is `true`.

*Effects:* If the map already contains an element whose key is
equivalent to `k`, `*this` and `args...` are unchanged. Otherwise
equivalent to:

``` cpp
auto key_it = ranges::upper_bound(c.keys, k, compare);
auto value_it = c.values.begin() + distance(c.keys.begin(), key_it);
c.keys.insert(key_it, std::forward<decltype(k)>(k));
c.values.emplace(value_it, std::forward<Args>(args)...);
```

*Returns:* In the first two overloads, the `bool` component of the
returned pair is `true` if and only if the insertion took place. The
returned iterator points to the map element whose key is equivalent to
`k`.

*Complexity:* The same as `emplace` for the first two overloads, and the
same as `emplace_hint` for the last two overloads.

``` cpp
template<class K, class... Args>
  pair<iterator, bool> try_emplace(K&& k, Args&&... args);
template<class K, class... Args>
  iterator try_emplace(const_iterator hint, K&& k, Args&&... args);
```

*Constraints:*

- The *qualified-id* `Compare::is_transparent` is valid and denotes a
  type.
- `is_constructible_v<key_type, K>` is `true`.
- `is_constructible_v<mapped_type, Args...>` is `true`.
- For the first overload, `is_convertible_v<K&&, const_iterator>` and
  `is_convertible_v<K&&, iterator>` are both `false`.

*Preconditions:* The conversion from `k` into `key_type` constructs an
object `u`, for which `find(k) == find(u)` is `true`.

*Effects:* If the map already contains an element whose key is
equivalent to `k`, `*this` and `args...` are unchanged. Otherwise
equivalent to:

``` cpp
auto key_it = ranges::upper_bound(c.keys, k, compare);
auto value_it = c.values.begin() + distance(c.keys.begin(), key_it);
c.keys.emplace(key_it, std::forward<K>(k));
c.values.emplace(value_it, std::forward<Args>(args)...);
```

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
template<class M>
  pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
template<class M>
  pair<iterator, bool> insert_or_assign(key_type&& k, M&& obj);
template<class M>
  iterator insert_or_assign(const_iterator hint, const key_type& k, M&& obj);
template<class M>
  iterator insert_or_assign(const_iterator hint, key_type&& k, M&& obj);
```

*Constraints:* `is_assignable_v<mapped_type&, M>` is `true` and
`is_constructible_v<mapped_type, M>` is `true`.

*Effects:* If the map already contains an element `e` whose key is
equivalent to `k`, assigns `std::forward<M>(obj)` to `e.second`.
Otherwise, equivalent to

``` cpp
try_emplace(std::forward<decltype(k)>(k), std::forward<M>(obj))
```

for the first two overloads or

``` cpp
try_emplace(hint, std::forward<decltype(k)>(k), std::forward<M>(obj))
```

for the last two overloads.

*Returns:* In the first two overloads, the `bool` component of the
returned pair is `true` if and only if the insertion took place. The
returned iterator points to the map element whose key is equivalent to
`k`.

*Complexity:* The same as `emplace` for the first two overloads and the
same as `emplace_hint` for the last two overloads.

``` cpp
template<class K, class M>
  pair<iterator, bool> insert_or_assign(K&& k, M&& obj);
template<class K, class M>
  iterator insert_or_assign(const_iterator hint, K&& k, M&& obj);
```

*Constraints:*

- The *qualified-id* `Compare::is_transparent` is valid and denotes a
  type.
- `is_constructible_v<key_type, K>` is `true`.
- `is_assignable_v<mapped_type&, M>` is `true`.
- `is_constructible_v<mapped_type, M>` is `true`.

*Preconditions:* The conversion from `k` into `key_type` constructs an
object `u`, for which `find(k) == find(u)` is `true`.

*Effects:* If the map already contains an element `e` whose key is
equivalent to `k`, assigns `std::forward<M>(obj)` to `e.second`.
Otherwise, equivalent to

``` cpp
try_emplace(std::forward<K>(k), std::forward<M>(obj))
```

for the first overload or

``` cpp
try_emplace(hint, std::forward<K>(k), std::forward<M>(obj))
```

for the second overload.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the map element whose key is equivalent to `k`.

*Complexity:* The same as `emplace` and `emplace_hint`, respectively.

``` cpp
void swap(flat_map& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
ranges::swap(compare, y.compare);
ranges::swap(c.keys, y.c.keys);
ranges::swap(c.values, y.c.values);
```

``` cpp
containers extract() &&;
```

*Ensures:* `*this` is emptied, even if the function exits via an
exception.

*Returns:* `std::move(c)`.

``` cpp
void replace(key_container_type&& key_cont, mapped_container_type&& mapped_cont);
```

*Preconditions:* `key_cont.size() == mapped_cont.size()` is `true`, the
elements of `key_cont` are sorted with respect to `compare`, and
`key_cont` contains no equal elements.

*Effects:* Equivalent to:

``` cpp
c.keys = std::move(key_cont);
c.values = std::move(mapped_cont);
```

#### Erasure <a id="flat.map.erasure">[[flat.map.erasure]]</a>

``` cpp
template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
         class Predicate>
  typename flat_map<Key, T, Compare, KeyContainer, MappedContainer>::size_type
    erase_if(flat_map<Key, T, Compare, KeyContainer, MappedContainer>& c, Predicate pred);
```

*Preconditions:* `Key` and `T` meet the *Cpp17MoveAssignable*
requirements.

*Effects:* Let E be `bool(pred(pair<const Key&, const T&>(e)))`. Erases
all elements `e` in `c` for which E holds.

*Returns:* The number of elements erased.

*Complexity:* Exactly `c.size()` applications of the predicate.

*Remarks:* Stable [[algorithm.stable]]. If an invocation of `erase_if`
exits via an exception, `c` is in a valid but unspecified
state [[defns.valid]].

[*Note 1*: `c` still meets its invariants, but can be
empty. — *end note*]

### Class template `flat_multimap` <a id="flat.multimap">[[flat.multimap]]</a>

#### Overview <a id="flat.multimap.overview">[[flat.multimap.overview]]</a>

A `flat_multimap` is a container adaptor that provides an associative
container interface that supports equivalent keys (i.e., possibly
containing multiple copies of the same key value) and provides for fast
retrieval of values of another type `T` based on the keys.
`flat_multimap` supports iterators that meet the *Cpp17InputIterator*
requirements and model the `random_access_iterator` concept
[[iterator.concept.random.access]].

A `flat_multimap` meets all of the requirements for a container
[[container.reqmts]] and for a reversible container
[[container.rev.reqmts]], plus the optional container requirements
[[container.opt.reqmts]]. `flat_multimap` meets the requirements of an
associative container [[associative.reqmts]], except that:

- it does not meet the requirements related to node handles
  [[container.node]],
- it does not meet the requirements related to iterator invalidation,
  and
- the time complexity of the operations that insert or erase a single
  element from the map is linear, including the ones that take an
  insertion position iterator.

[*Note 1*: A `flat_multimap` does not meet the additional requirements
of an allocator-aware container
[[container.alloc.reqmts]]. — *end note*]

A `flat_multimap` also provides most operations described in
[[associative.reqmts]] for equal keys. This means that a `flat_multimap`
supports the `a_eq` operations in [[associative.reqmts]] but not the
`a_uniq` operations. For a `flat_multimap<Key, T>` the `key_type` is
`Key` and the `value_type` is `pair<Key, T>`.

Except as otherwise noted, operations on `flat_multimap` are equivalent
to those of `flat_map`, except that `flat_multimap` operations do not
remove or replace elements with equal keys.

[*Example 1*: `flat_multimap` constructors and emplace do not erase
non-unique elements after sorting them. — *end example*]

A `flat_multimap` maintains the following invariants:

- it contains the same number of keys and values;
- the keys are sorted with respect to the comparison object; and
- the value at offset `off` within the value container is the value
  associated with the key at offset `off` within the key container.

If any member function in [[flat.multimap.defn]] exits via an exception,
the invariants are restored.

[*Note 2*: This can result in the `flat_multimap` being
emptied. — *end note*]

Any type `C` that meets the sequence container requirements
[[sequence.reqmts]] can be used to instantiate `flat_multimap`, as long
as `C::iterator` meets the *Cpp17RandomAccessIterator* requirements and
invocations of member functions `C::size` and `C::max_size` do not exit
via an exception. In particular, `vector` [[vector]] and `deque`
[[deque]] can be used.

[*Note 3*: `vector<bool>` is not a sequence container. — *end note*]

The program is ill-formed if `Key` is not the same type as
`KeyContainer::value_type` or `T` is not the same type as
`MappedContainer::value_type`.

The effect of calling a constructor that takes both `key_container_type`
and `mapped_container_type` arguments with containers of different sizes
is undefined.

The effect of calling a constructor or member function that takes a
`sorted_equivalent_t` argument with a container, containers, or range
that are not sorted with respect to `key_comp()` is undefined.

#### Definition <a id="flat.multimap.defn">[[flat.multimap.defn]]</a>

``` cpp
namespace std {
  template<class Key, class T, class Compare = less<Key>,
           class KeyContainer = vector<Key>, class MappedContainer = vector<T>>
  class flat_multimap {
  public:
    // types
    using key_type               = Key;
    using mapped_type            = T;
    using value_type             = pair<key_type, mapped_type>;
    using key_compare            = Compare;
    using reference              = pair<const key_type&, mapped_type&>;
    using const_reference        = pair<const key_type&, const mapped_type&>;
    using size_type              = size_t;
    using difference_type        = ptrdiff_t;
    using iterator               = implementation-defined  // type of flat_multimap::iterator;     // see [container.requirements]
    using const_iterator         = implementation-defined  // type of flat_multimap::const_iterator;     // see [container.requirements]
    using reverse_iterator       = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;
    using key_container_type     = KeyContainer;
    using mapped_container_type  = MappedContainer;

    class value_compare {
    private:
      key_compare comp;                                 // exposition only
      value_compare(key_compare c) : comp(c) { }        // exposition only

    public:
      bool operator()(const_reference x, const_reference y) const {
        return comp(x.first, y.first);
      }
    };

    struct containers {
      key_container_type keys;
      mapped_container_type values;
    };

    // [flat.multimap.cons], construct/copy/destroy
    flat_multimap() : flat_multimap(key_compare()) { }

    flat_multimap(key_container_type key_cont, mapped_container_type mapped_cont,
                  const key_compare& comp = key_compare());
    template<class Allocator>
      flat_multimap(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
                    const Allocator& a);
    template<class Allocator>
      flat_multimap(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
                    const key_compare& comp, const Allocator& a);

    flat_multimap(sorted_equivalent_t,
                  key_container_type key_cont, mapped_container_type mapped_cont,
                  const key_compare& comp = key_compare());
    template<class Allocator>
      flat_multimap(sorted_equivalent_t, const key_container_type& key_cont,
                    const mapped_container_type& mapped_cont, const Allocator& a);
    template<class Allocator>
      flat_multimap(sorted_equivalent_t, const key_container_type& key_cont,
                    const mapped_container_type& mapped_cont,
                    const key_compare& comp, const Allocator& a);

    explicit flat_multimap(const key_compare& comp)
      : c(), compare(comp) { }
    template<class Allocator>
      flat_multimap(const key_compare& comp, const Allocator& a);
    template<class Allocator>
      explicit flat_multimap(const Allocator& a);

    template<class InputIterator>
      flat_multimap(InputIterator first, InputIterator last,
                    const key_compare& comp = key_compare())
        : c(), compare(comp)
        { insert(first, last); }
    template<class InputIterator, class Allocator>
      flat_multimap(InputIterator first, InputIterator last,
                    const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_multimap(InputIterator first, InputIterator last, const Allocator& a);

    template<container-compatible-range<value_type> R>
      flat_multimap(from_range_t fr, R&& rg)
        : flat_multimap(fr, std::forward<R>(rg), key_compare()) { }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_multimap(from_range_t, R&& rg, const Allocator& a);
    template<container-compatible-range<value_type> R>
      flat_multimap(from_range_t, R&& rg, const key_compare& comp)
        : flat_multimap(comp) { insert_range(std::forward<R>(rg)); }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_multimap(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);

    template<class InputIterator>
      flat_multimap(sorted_equivalent_t s, InputIterator first, InputIterator last,
                    const key_compare& comp = key_compare())
        : c(), compare(comp) { insert(s, first, last); }
    template<class InputIterator, class Allocator>
      flat_multimap(sorted_equivalent_t, InputIterator first, InputIterator last,
                    const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_multimap(sorted_equivalent_t, InputIterator first, InputIterator last,
                    const Allocator& a);

    flat_multimap(initializer_list<value_type> il, const key_compare& comp = key_compare())
        : flat_multimap(il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_multimap(initializer_list<value_type> il, const key_compare& comp,
                    const Allocator& a);
    template<class Allocator>
      flat_multimap(initializer_list<value_type> il, const Allocator& a);

    flat_multimap(sorted_equivalent_t s, initializer_list<value_type> il,
                  const key_compare& comp = key_compare())
        : flat_multimap(s, il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_multimap(sorted_equivalent_t, initializer_list<value_type> il,
                    const key_compare& comp, const Allocator& a);
    template<class Allocator>
      flat_multimap(sorted_equivalent_t, initializer_list<value_type> il, const Allocator& a);

    flat_multimap& operator=(initializer_list<value_type> il);

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // modifiers
    template<class... Args> iterator emplace(Args&&... args);
    template<class... Args>
      iterator emplace_hint(const_iterator position, Args&&... args);

    iterator insert(const value_type& x)
      { return emplace(x); }
    iterator insert(value_type&& x)
      { return emplace(std::move(x)); }
    iterator insert(const_iterator position, const value_type& x)
      { return emplace_hint(position, x); }
    iterator insert(const_iterator position, value_type&& x)
      { return emplace_hint(position, std::move(x)); }

    template<class P> iterator insert(P&& x);
    template<class P>
      iterator insert(const_iterator position, P&&);
    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<class InputIterator>
      void insert(sorted_equivalent_t, InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);

    void insert(initializer_list<value_type> il)
      { insert(il.begin(), il.end()); }
    void insert(sorted_equivalent_t s, initializer_list<value_type> il)
      { insert(s, il.begin(), il.end()); }

    containers extract() &&;
    void replace(key_container_type&& key_cont, mapped_container_type&& mapped_cont);

    iterator erase(iterator position);
    iterator erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator erase(const_iterator first, const_iterator last);

    void swap(flat_multimap&) noexcept;
    void clear() noexcept;

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    const key_container_type& keys() const noexcept { return c.keys; }
    const mapped_container_type& values() const noexcept { return c.values; }

    // map operations
    iterator find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator> equal_range(const key_type& x);
    pair<const_iterator, const_iterator> equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator> equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;

    friend bool operator==(const flat_multimap& x, const flat_multimap& y);

    friend synth-three-way-result<value_type>
      operator<=>(const flat_multimap& x, const flat_multimap& y);

    friend void swap(flat_multimap& x, flat_multimap& y) noexcept
      { x.swap(y); }

  private:
    containers c;               // exposition only
    key_compare compare;        // exposition only
  };

  template<class KeyContainer, class MappedContainer,
           class Compare = less<typename KeyContainer::value_type>>
    flat_multimap(KeyContainer, MappedContainer, Compare = Compare())
      -> flat_multimap<typename KeyContainer::value_type, typename MappedContainer::value_type,
                       Compare, KeyContainer, MappedContainer>;

  template<class KeyContainer, class MappedContainer, class Allocator>
    flat_multimap(KeyContainer, MappedContainer, Allocator)
      -> flat_multimap<typename KeyContainer::value_type, typename MappedContainer::value_type,
                       less<typename KeyContainer::value_type>, KeyContainer, MappedContainer>;
  template<class KeyContainer, class MappedContainer, class Compare, class Allocator>
    flat_multimap(KeyContainer, MappedContainer, Compare, Allocator)
      -> flat_multimap<typename KeyContainer::value_type, typename MappedContainer::value_type,
                       Compare, KeyContainer, MappedContainer>;

  template<class KeyContainer, class MappedContainer,
           class Compare = less<typename KeyContainer::value_type>>
    flat_multimap(sorted_equivalent_t, KeyContainer, MappedContainer, Compare = Compare())
      -> flat_multimap<typename KeyContainer::value_type, typename MappedContainer::value_type,
                       Compare, KeyContainer, MappedContainer>;

  template<class KeyContainer, class MappedContainer, class Allocator>
    flat_multimap(sorted_equivalent_t, KeyContainer, MappedContainer, Allocator)
      -> flat_multimap<typename KeyContainer::value_type, typename MappedContainer::value_type,
                       less<typename KeyContainer::value_type>, KeyContainer, MappedContainer>;
  template<class KeyContainer, class MappedContainer, class Compare, class Allocator>
    flat_multimap(sorted_equivalent_t, KeyContainer, MappedContainer, Compare, Allocator)
      -> flat_multimap<typename KeyContainer::value_type, typename MappedContainer::value_type,
                       Compare, KeyContainer, MappedContainer>;

  template<class InputIterator, class Compare = less<iter-key-type<InputIterator>>>
    flat_multimap(InputIterator, InputIterator, Compare = Compare())
      -> flat_multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Compare>;

  template<class InputIterator, class Compare = less<iter-key-type<InputIterator>>>
    flat_multimap(sorted_equivalent_t, InputIterator, InputIterator, Compare = Compare())
      -> flat_multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>, Compare>;

  template<ranges::input_range R, class Compare = less<range-key-type<R>>,
           class Allocator = allocator<byte>>
    flat_multimap(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> flat_multimap<range-key-type<R>, range-mapped-type<R>, Compare,
                       vector<range-key-type<R>,
                              alloc-rebind<Allocator, range-key-type<R>>>,
                       vector<range-mapped-type<R>,
                              alloc-rebind<Allocator, range-mapped-type<R>>>>;

  template<ranges::input_range R, class Allocator>
    flat_multimap(from_range_t, R&&, Allocator)
      -> flat_multimap<range-key-type<R>, range-mapped-type<R>, less<range-key-type<R>>,
                       vector<range-key-type<R>,
                              alloc-rebind<Allocator, range-key-type<R>>>,
                       vector<range-mapped-type<R>,
                              alloc-rebind<Allocator, range-mapped-type<R>>>>;

  template<class Key, class T, class Compare = less<Key>>
    flat_multimap(initializer_list<pair<Key, T>>, Compare = Compare())
      -> flat_multimap<Key, T, Compare>;

  template<class Key, class T, class Compare = less<Key>>
    flat_multimap(sorted_equivalent_t, initializer_list<pair<Key, T>>, Compare = Compare())
        -> flat_multimap<Key, T, Compare>;

  template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
            class Allocator>
    struct uses_allocator<flat_multimap<Key, T, Compare, KeyContainer, MappedContainer>,
                          Allocator>
      : bool_constant<uses_allocator_v<KeyContainer, Allocator> &&
                      uses_allocator_v<MappedContainer, Allocator>> { };
}
```

The member type `containers` has the data members and special members
specified above. It has no base classes or members other than those
specified.

#### Constructors <a id="flat.multimap.cons">[[flat.multimap.cons]]</a>

``` cpp
flat_multimap(key_container_type key_cont, mapped_container_type mapped_cont,
              const key_compare& comp = key_compare());
```

*Effects:* Initializes `c.keys` with `std::move(key_cont)`, `c.values`
with `std::move(mapped_cont)`, and `compare` with `comp`; sorts the
range \[`begin()`, `end()`) with respect to `value_comp()`.

*Complexity:* Linear in N if the container arguments are already sorted
with respect to `value_comp()` and otherwise N log N, where N is the
value of `key_cont.size()` before this call.

``` cpp
template<class Allocator>
  flat_multimap(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
                const Allocator& a);
template<class Allocator>
  flat_multimap(const key_container_type& key_cont, const mapped_container_type& mapped_cont,
                const key_compare& comp, const Allocator& a);
```

*Constraints:* `uses_allocator_v<key_container_type, Allocator>` is
`true` and `uses_allocator_v<mapped_container_type, Allocator>` is
`true`.

*Effects:* Equivalent to `flat_multimap(key_cont, mapped_cont)` and
`flat_multimap(key_cont, mapped_cont, comp)`, respectively, except that
`c.keys` and `c.values` are constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Same as `flat_multimap(key_cont, mapped_cont)` and
`flat_multimap(key_cont, mapped_cont, comp)`, respectively.

``` cpp
flat_multimap(sorted_equivalent_t, key_container_type key_cont, mapped_container_type mapped_cont,
              const key_compare& comp = key_compare());
```

*Effects:* Initializes `c.keys` with `std::move(key_cont)`, `c.values`
with `std::move(mapped_cont)`, and `compare` with `comp`.

*Complexity:* Constant.

``` cpp
template<class Allocator>
  flat_multimap(sorted_equivalent_t s, const key_container_type& key_cont,
                const mapped_container_type& mapped_cont, const Allocator& a);
template<class Allocator>
  flat_multimap(sorted_equivalent_t s, const key_container_type& key_cont,
                const mapped_container_type& mapped_cont, const key_compare& comp,
                const Allocator& a);
```

*Constraints:* `uses_allocator_v<key_container_type, Allocator>` is
`true` and `uses_allocator_v<mapped_container_type, Allocator>` is
`true`.

*Effects:* Equivalent to `flat_multimap(s, key_cont, mapped_cont)` and
`flat_multimap(s, key_cont, mapped_cont, comp)`, respectively, except
that `c.keys` and `c.values` are constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Linear.

``` cpp
template<class Allocator>
  flat_multimap(const key_compare& comp, const Allocator& a);
template<class Allocator>
  explicit flat_multimap(const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multimap(InputIterator first, InputIterator last, const key_compare& comp,
                const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multimap(InputIterator first, InputIterator last, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_multimap(from_range_t, R&& rg, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_multimap(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multimap(sorted_equivalent_t, InputIterator first, InputIterator last,
                const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multimap(sorted_equivalent_t, InputIterator first, InputIterator last,
                const Allocator& a);
template<class Allocator>
  flat_multimap(initializer_list<value_type> il, const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_multimap(initializer_list<value_type> il, const Allocator& a);
template<class Allocator>
  flat_multimap(sorted_equivalent_t, initializer_list<value_type> il,
                const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_multimap(sorted_equivalent_t, initializer_list<value_type> il, const Allocator& a);
```

*Constraints:* `uses_allocator_v<key_container_type, Allocator>` is
`true` and `uses_allocator_v<mapped_container_type, Allocator>` is
`true`.

*Effects:* Equivalent to the corresponding non-allocator constructors
except that `c.keys` and `c.values` are constructed with uses-allocator
construction [[allocator.uses.construction]].

#### Erasure <a id="flat.multimap.erasure">[[flat.multimap.erasure]]</a>

``` cpp
template<class Key, class T, class Compare, class KeyContainer, class MappedContainer,
         class Predicate>
  typename flat_multimap<Key, T, Compare, KeyContainer, MappedContainer>::size_type
    erase_if(flat_multimap<Key, T, Compare, KeyContainer, MappedContainer>& c, Predicate pred);
```

*Preconditions:* `Key` and `T` meet the *Cpp17MoveAssignable*
requirements.

*Effects:* Let E be `bool(pred(pair<const Key&, const T&>(e)))`. Erases
all elements `e` in `c` for which E holds.

*Returns:* The number of elements erased.

*Complexity:* Exactly `c.size()` applications of the predicate.

*Remarks:* Stable [[algorithm.stable]]. If an invocation of `erase_if`
exits via an exception, `c` is in a valid but unspecified
state [[defns.valid]].

[*Note 1*: `c` still meets its invariants, but can be
empty. — *end note*]

### Class template `flat_set` <a id="flat.set">[[flat.set]]</a>

#### Overview <a id="flat.set.overview">[[flat.set.overview]]</a>

A `flat_set` is a container adaptor that provides an associative
container interface that supports unique keys (i.e., contains at most
one of each key value) and provides for fast retrieval of the keys
themselves. `flat_set` supports iterators that model the
`random_access_iterator` concept [[iterator.concept.random.access]].

A `flat_set` meets all of the requirements for a container
[[container.reqmts]] and for a reversible container
[[container.rev.reqmts]], plus the optional container requirements
[[container.opt.reqmts]]. `flat_set` meets the requirements of an
associative container [[associative.reqmts]], except that:

- it does not meet the requirements related to node handles
  [[container.node.overview]],
- it does not meet the requirements related to iterator invalidation,
  and
- the time complexity of the operations that insert or erase a single
  element from the set is linear, including the ones that take an
  insertion position iterator.

[*Note 1*: A `flat_set` does not meet the additional requirements of an
allocator-aware container, as described in
[[container.alloc.reqmts]]. — *end note*]

A `flat_set` also provides most operations described in
[[associative.reqmts]] for unique keys. This means that a `flat_set`
supports the `a_uniq` operations in [[associative.reqmts]] but not the
`a_eq` operations. For a `flat_set<Key>`, both the `key_type` and
`value_type` are `Key`.

Descriptions are provided here only for operations on `flat_set` that
are not described in one of those sets of requirements or for operations
where there is additional semantic information.

A `flat_set` maintains the invariant that the keys are sorted with
respect to the comparison object.

If any member function in [[flat.set.defn]] exits via an exception, the
invariant is restored.

[*Note 2*: This can result in the `flat_set`’s being
emptied. — *end note*]

Any sequence container [[sequence.reqmts]] supporting
*Cpp17RandomAccessIterator* can be used to instantiate `flat_set`. In
particular, `vector` [[vector]] and `deque` [[deque]] can be used.

[*Note 3*: `vector<bool>` is not a sequence container. — *end note*]

The program is ill-formed if `Key` is not the same type as
`KeyContainer::value_type`.

The effect of calling a constructor or member function that takes a
`sorted_unique_t` argument with a range that is not sorted with respect
to `key_comp()`, or that contains equal elements, is undefined.

#### Definition <a id="flat.set.defn">[[flat.set.defn]]</a>

``` cpp
namespace std {
  template<class Key, class Compare = less<Key>, class KeyContainer = vector<Key>>
  class flat_set {
  public:
    // types
    using key_type                  = Key;
    using value_type                = Key;
    using key_compare               = Compare;
    using value_compare             = Compare;
    using reference                 = value_type&;
    using const_reference           = const value_type&;
    using size_type                 = typename KeyContainer::size_type;
    using difference_type           = typename KeyContainer::difference_type;
    using iterator                  = implementation-defined  // type of flat_set::iterator;  // see [container.requirements]
    using const_iterator            = implementation-defined  // type of flat_set::const_iterator;  // see [container.requirements]
    using reverse_iterator          = std::reverse_iterator<iterator>;
    using const_reverse_iterator    = std::reverse_iterator<const_iterator>;
    using container_type            = KeyContainer;

    // [flat.set.cons], constructors
    flat_set() : flat_set(key_compare()) { }

    explicit flat_set(container_type cont, const key_compare& comp = key_compare());
    template<class Allocator>
      flat_set(const container_type& cont, const Allocator& a);
    template<class Allocator>
      flat_set(const container_type& cont, const key_compare& comp, const Allocator& a);

    flat_set(sorted_unique_t, container_type cont, const key_compare& comp = key_compare())
      : c(std::move(cont)), compare(comp) { }
    template<class Allocator>
      flat_set(sorted_unique_t, const container_type& cont, const Allocator& a);
    template<class Allocator>
      flat_set(sorted_unique_t, const container_type& cont,
               const key_compare& comp, const Allocator& a);

    explicit flat_set(const key_compare& comp)
      : c(), compare(comp) { }
    template<class Allocator>
      flat_set(const key_compare& comp, const Allocator& a);
    template<class Allocator>
      explicit flat_set(const Allocator& a);

    template<class InputIterator>
      flat_set(InputIterator first, InputIterator last, const key_compare& comp = key_compare())
        : c(), compare(comp)
        { insert(first, last); }
    template<class InputIterator, class Allocator>
      flat_set(InputIterator first, InputIterator last,
               const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_set(InputIterator first, InputIterator last, const Allocator& a);

    template<container-compatible-range<value_type> R>
      flat_set(from_range_t fr, R&& rg)
        : flat_set(fr, std::forward<R>(rg), key_compare()) { }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_set(from_range_t, R&& rg, const Allocator& a);
    template<container-compatible-range<value_type> R>
      flat_set(from_range_t, R&& rg, const key_compare& comp)
        : flat_set(comp)
        { insert_range(std::forward<R>(rg)); }
    template<container-compatible-range<value_type> R, class Allocator>
       flat_set(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);

    template<class InputIterator>
      flat_set(sorted_unique_t, InputIterator first, InputIterator last,
               const key_compare& comp = key_compare())
        : c(first, last), compare(comp) { }
    template<class InputIterator, class Allocator>
      flat_set(sorted_unique_t, InputIterator first, InputIterator last,
               const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_set(sorted_unique_t, InputIterator first, InputIterator last, const Allocator& a);

    flat_set(initializer_list<value_type> il, const key_compare& comp = key_compare())
        : flat_set(il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_set(initializer_list<value_type> il, const key_compare& comp, const Allocator& a);
    template<class Allocator>
      flat_set(initializer_list<value_type> il, const Allocator& a);

    flat_set(sorted_unique_t s, initializer_list<value_type> il,
             const key_compare& comp = key_compare())
        : flat_set(s, il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_set(sorted_unique_t, initializer_list<value_type> il,
               const key_compare& comp, const Allocator& a);
    template<class Allocator>
      flat_set(sorted_unique_t, initializer_list<value_type> il, const Allocator& a);

    flat_set& operator=(initializer_list<value_type>);

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [flat.set.modifiers], modifiers
    template<class... Args> pair<iterator, bool> emplace(Args&&... args);
    template<class... Args>
      iterator emplace_hint(const_iterator position, Args&&... args);

    pair<iterator, bool> insert(const value_type& x)
      { return emplace(x); }
    pair<iterator, bool> insert(value_type&& x)
      { return emplace(std::move(x)); }
    template<class K> pair<iterator, bool> insert(K&& x);
    iterator insert(const_iterator position, const value_type& x)
      { return emplace_hint(position, x); }
    iterator insert(const_iterator position, value_type&& x)
      { return emplace_hint(position, std::move(x)); }
    template<class K> iterator insert(const_iterator hint, K&& x);

    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<class InputIterator>
      void insert(sorted_unique_t, InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);

    void insert(initializer_list<value_type> il)
      { insert(il.begin(), il.end()); }
    void insert(sorted_unique_t s, initializer_list<value_type> il)
      { insert(s, il.begin(), il.end()); }

    container_type extract() &&;
    void replace(container_type&&);

    iterator erase(iterator position);
    iterator erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator erase(const_iterator first, const_iterator last);

    void swap(flat_set& y) noexcept;
    void clear() noexcept;

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    // set operations
    iterator find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator> equal_range(const key_type& x);
    pair<const_iterator, const_iterator> equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator> equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;

    friend bool operator==(const flat_set& x, const flat_set& y);

    friend synth-three-way-result<value_type>
      operator<=>(const flat_set& x, const flat_set& y);

    friend void swap(flat_set& x, flat_set& y) noexcept { x.swap(y); }

  private:
    container_type c;           // exposition only
    key_compare compare;        // exposition only
  };

  template<class KeyContainer, class Compare = less<typename KeyContainer::value_type>>
    flat_set(KeyContainer, Compare = Compare())
      -> flat_set<typename KeyContainer::value_type, Compare, KeyContainer>;
  template<class KeyContainer, class Allocator>
    flat_set(KeyContainer, Allocator)
      -> flat_set<typename KeyContainer::value_type,
                  less<typename KeyContainer::value_type>, KeyContainer>;
  template<class KeyContainer, class Compare, class Allocator>
    flat_set(KeyContainer, Compare, Allocator)
      -> flat_set<typename KeyContainer::value_type, Compare, KeyContainer>;

  template<class KeyContainer, class Compare = less<typename KeyContainer::value_type>>
    flat_set(sorted_unique_t, KeyContainer, Compare = Compare())
      -> flat_set<typename KeyContainer::value_type, Compare, KeyContainer>;
  template<class KeyContainer, class Allocator>
    flat_set(sorted_unique_t, KeyContainer, Allocator)
      -> flat_set<typename KeyContainer::value_type,
                  less<typename KeyContainer::value_type>, KeyContainer>;
  template<class KeyContainer, class Compare, class Allocator>
    flat_set(sorted_unique_t, KeyContainer, Compare, Allocator)
      -> flat_set<typename KeyContainer::value_type, Compare, KeyContainer>;

  template<class InputIterator, class Compare = less<iter-value-type<InputIterator>>>
    flat_set(InputIterator, InputIterator, Compare = Compare())
      -> flat_set<iter-value-type<InputIterator>, Compare>;

  template<class InputIterator, class Compare = less<iter-value-type<InputIterator>>>
    flat_set(sorted_unique_t, InputIterator, InputIterator, Compare = Compare())
      -> flat_set<iter-value-type<InputIterator>, Compare>;

  template<ranges::input_range R, class Compare = less<ranges::range_value_t<R>>,
           class Allocator = allocator<ranges::range_value_t<R>>>
    flat_set(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> flat_set<ranges::range_value_t<R>, Compare,
                  vector<ranges::range_value_t<R>,
                         alloc-rebind<Allocator, ranges::range_value_t<R>>>>;

  template<ranges::input_range R, class Allocator>
    flat_set(from_range_t, R&&, Allocator)
      -> flat_set<ranges::range_value_t<R>, less<ranges::range_value_t<R>>,
                  vector<ranges::range_value_t<R>,
                         alloc-rebind<Allocator, ranges::range_value_t<R>>>>;

  template<class Key, class Compare = less<Key>>
    flat_set(initializer_list<Key>, Compare = Compare())
      -> flat_set<Key, Compare>;

  template<class Key, class Compare = less<Key>>
    flat_set(sorted_unique_t, initializer_list<Key>, Compare = Compare())
      -> flat_set<Key, Compare>;

  template<class Key, class Compare, class KeyContainer, class Allocator>
    struct uses_allocator<flat_set<Key, Compare, KeyContainer>, Allocator>
      : bool_constant<uses_allocator_v<KeyContainer, Allocator>> { };
}
```

#### Constructors <a id="flat.set.cons">[[flat.set.cons]]</a>

``` cpp
explicit flat_set(container_type cont, const key_compare& comp = key_compare());
```

*Effects:* Initializes *c* with `std::move(cont)` and *compare* with
`comp`, sorts the range \[`begin()`, `end()`) with respect to *compare*,
and finally erases all but the first element from each group of
consecutive equivalent elements.

*Complexity:* Linear in N if `cont` is sorted with respect to *compare*
and otherwise N log N, where N is the value of `cont.size()` before this
call.

``` cpp
template<class Allocator>
  flat_set(const container_type& cont, const Allocator& a);
template<class Allocator>
  flat_set(const container_type& cont, const key_compare& comp, const Allocator& a);
```

*Constraints:* `uses_allocator_v<container_type, Allocator>` is `true`.

*Effects:* Equivalent to `flat_set(cont)` and `flat_set(cont, comp)`,
respectively, except that *c* is constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Same as `flat_set(cont)` and `flat_set(cont, comp)`,
respectively.

``` cpp
template<class Allocator>
  flat_set(sorted_unique_t s, const container_type& cont, const Allocator& a);
template<class Allocator>
  flat_set(sorted_unique_t s, const container_type& cont,
           const key_compare& comp, const Allocator& a);
```

*Constraints:* `uses_allocator_v<container_type, Allocator>` is `true`.

*Effects:* Equivalent to `flat_set(s, cont)` and
`flat_set(s, cont, comp)`, respectively, except that *c* is constructed
with uses-allocator construction [[allocator.uses.construction]].

*Complexity:* Linear.

``` cpp
template<class Allocator>
  flat_set(const key_compare& comp, const Allocator& a);
template<class Allocator>
  explicit flat_set(const Allocator& a);
template<class InputIterator, class Allocator>
  flat_set(InputIterator first, InputIterator last, const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_set(InputIterator first, InputIterator last, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_set(from_range_t, R&& rg, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_set(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_set(sorted_unique_t, InputIterator first, InputIterator last,
           const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_set(sorted_unique_t, InputIterator first, InputIterator last, const Allocator& a);
template<class Allocator>
  flat_set(initializer_list<value_type> il, const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_set(initializer_list<value_type> il, const Allocator& a);
template<class Allocator>
  flat_set(sorted_unique_t, initializer_list<value_type> il,
           const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_set(sorted_unique_t, initializer_list<value_type> il, const Allocator& a);
```

*Constraints:* `uses_allocator_v<container_type, Allocator>` is `true`.

*Effects:* Equivalent to the corresponding non-allocator constructors
except that *c* is constructed with uses-allocator
construction [[allocator.uses.construction]].

#### Modifiers <a id="flat.set.modifiers">[[flat.set.modifiers]]</a>

``` cpp
template<class K> pair<iterator, bool> insert(K&& x);
template<class K> iterator insert(const_iterator hint, K&& x);
```

*Constraints:* The *qualified-id* `Compare::is_transparent` is valid and
denotes a type. `is_constructible_v<value_type, K>` is `true`.

*Preconditions:* The conversion from `x` into `value_type` constructs an
object `u`, for which `find(x) == find(u)` is true.

*Effects:* If the set already contains an element equivalent to `x`,
`*this` and `x` are unchanged. Otherwise, inserts a new element as if by
`emplace(std::forward<K>(x))`.

*Returns:* In the first overload, the `bool` component of the returned
pair is `true` if and only if the insertion took place. The returned
iterator points to the element whose key is equivalent to `x`.

``` cpp
template<class InputIterator>
  void insert(InputIterator first, InputIterator last);
```

*Effects:* Adds elements to *c* as if by:

``` cpp
c.insert(c.end(), first, last);
```

Then, sorts the range of newly inserted elements with respect to
*compare*; merges the resulting sorted range and the sorted range of
pre-existing elements into a single sorted range; and finally erases all
but the first element from each group of consecutive equivalent
elements.

*Complexity:* N + M log M, where N is `size()` before the operation and
M is `distance(first, last)`.

*Remarks:* Since this operation performs an in-place merge, it may
allocate memory.

``` cpp
template<class InputIterator>
  void insert(sorted_unique_t, InputIterator first, InputIterator last);
```

*Effects:* Equivalent to `insert(first, last)`.

*Complexity:* Linear.

``` cpp
template<container-compatible-range<value_type> R>
  void insert_range(R&& rg);
```

*Effects:* Adds elements to *c* as if by:

``` cpp
for (const auto& e : rg) {
  c.insert(c.end(), e);
}
```

Then, sorts the range of newly inserted elements with respect to
*compare*; merges the resulting sorted range and the sorted range of
pre-existing elements into a single sorted range; and finally erases all
but the first element from each group of consecutive equivalent
elements.

*Complexity:* N + M log M, where N is `size()` before the operation and
M is `ranges::distance(rg)`.

*Remarks:* Since this operation performs an in-place merge, it may
allocate memory.

``` cpp
void swap(flat_set& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
ranges::swap(compare, y.compare);
ranges::swap(c, y.c);
```

``` cpp
container_type extract() &&;
```

*Ensures:* `*this` is emptied, even if the function exits via an
exception.

*Returns:* `std::move(`*`c`*`)`.

``` cpp
void replace(container_type&& cont);
```

*Preconditions:* The elements of `cont` are sorted with respect to
*compare*, and `cont` contains no equal elements.

*Effects:* Equivalent to: *`c`*` = std::move(cont);`

#### Erasure <a id="flat.set.erasure">[[flat.set.erasure]]</a>

``` cpp
template<class Key, class Compare, class KeyContainer, class Predicate>
  typename flat_set<Key, Compare, KeyContainer>::size_type
    erase_if(flat_set<Key, Compare, KeyContainer>& c, Predicate pred);
```

*Preconditions:* `Key` meets the *Cpp17MoveAssignable* requirements.

*Effects:* Let E be `bool(pred(as_const(e)))`. Erases all elements `e`
in `c` for which E holds.

*Returns:* The number of elements erased.

*Complexity:* Exactly `c.size()` applications of the predicate.

*Remarks:* Stable [[algorithm.stable]]. If an invocation of `erase_if`
exits via an exception, `c` is in a valid but unspecified
state [[defns.valid]].

[*Note 1*: `c` still meets its invariants, but can be
empty. — *end note*]

### Class template `flat_multiset` <a id="flat.multiset">[[flat.multiset]]</a>

#### Overview <a id="flat.multiset.overview">[[flat.multiset.overview]]</a>

A `flat_multiset` is a container adaptor that provides an associative
container interface that supports equivalent keys (i.e., possibly
containing multiple copies of the same key value) and provides for fast
retrieval of the keys themselves. `flat_multiset` supports iterators
that model the `random_access_iterator` concept
[[iterator.concept.random.access]].

A `flat_multiset` meets all of the requirements for a container
[[container.reqmts]] and for a reversible container
[[container.rev.reqmts]], plus the optional container requirements
[[container.opt.reqmts]]. `flat_multiset` meets the requirements of an
associative container [[associative.reqmts]], except that:

- it does not meet the requirements related to node handles
  [[container.node.overview]],
- it does not meet the requirements related to iterator invalidation,
  and
- the time complexity of the operations that insert or erase a single
  element from the set is linear, including the ones that take an
  insertion position iterator.

[*Note 1*: A `flat_multiset` does not meet the additional requirements
of an allocator-aware container, as described in
[[container.alloc.reqmts]]. — *end note*]

A `flat_multiset` also provides most operations described in
[[associative.reqmts]] for equal keys. This means that a `flat_multiset`
supports the `a_eq` operations in [[associative.reqmts]] but not the
`a_uniq` operations. For a `flat_multiset<Key>`, both the `key_type` and
`value_type` are `Key`.

Descriptions are provided here only for operations on `flat_multiset`
that are not described in one of the general sections or for operations
where there is additional semantic information.

A `flat_multiset` maintains the invariant that the keys are sorted with
respect to the comparison object.

If any member function in [[flat.multiset.defn]] exits via an exception,
the invariant is restored.

[*Note 2*: This can result in the `flat_multiset`’s being
emptied. — *end note*]

Any sequence container [[sequence.reqmts]] supporting
*Cpp17RandomAccessIterator* can be used to instantiate `flat_multiset`.
In particular, `vector` [[vector]] and `deque` [[deque]] can be used.

[*Note 3*: `vector<bool>` is not a sequence container. — *end note*]

The program is ill-formed if `Key` is not the same type as
`KeyContainer::value_type`.

The effect of calling a constructor or member function that takes a
`sorted_equivalent_t` argument with a range that is not sorted with
respect to `key_comp()` is undefined.

#### Definition <a id="flat.multiset.defn">[[flat.multiset.defn]]</a>

``` cpp
namespace std {
  template<class Key, class Compare = less<Key>, class KeyContainer = vector<Key>>
  class flat_multiset {
  public:
    // types
    using key_type                  = Key;
    using value_type                = Key;
    using key_compare               = Compare;
    using value_compare             = Compare;
    using reference                 = value_type&;
    using const_reference           = const value_type&;
    using size_type                 = typename KeyContainer::size_type;
    using difference_type           = typename KeyContainer::difference_type;
    using iterator                  = implementation-defined  // type of flat_multiset::iterator;  // see [container.requirements]
    using const_iterator            = implementation-defined  // type of flat_multiset::const_iterator;  // see [container.requirements]
    using reverse_iterator          = std::reverse_iterator<iterator>;
    using const_reverse_iterator    = std::reverse_iterator<const_iterator>;
    using container_type            = KeyContainer;

    // [flat.multiset.cons], constructors
    flat_multiset() : flat_multiset(key_compare()) { }

    explicit flat_multiset(container_type cont, const key_compare& comp = key_compare());
    template<class Allocator>
      flat_multiset(const container_type& cont, const Allocator& a);
    template<class Allocator>
      flat_multiset(const container_type& cont, const key_compare& comp, const Allocator& a);

    flat_multiset(sorted_equivalent_t, container_type cont,
                  const key_compare& comp = key_compare())
      : c(std::move(cont)), compare(comp) { }
    template<class Allocator>
      flat_multiset(sorted_equivalent_t, const container_type&, const Allocator& a);
    template<class Allocator>
      flat_multiset(sorted_equivalent_t, const container_type& cont,
                    const key_compare& comp, const Allocator& a);

    explicit flat_multiset(const key_compare& comp)
      : c(), compare(comp) { }
    template<class Allocator>
      flat_multiset(const key_compare& comp, const Allocator& a);
    template<class Allocator>
      explicit flat_multiset(const Allocator& a);

    template<class InputIterator>
      flat_multiset(InputIterator first, InputIterator last,
                    const key_compare& comp = key_compare())
        : c(), compare(comp)
        { insert(first, last); }
    template<class InputIterator, class Allocator>
      flat_multiset(InputIterator first, InputIterator last,
                    const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_multiset(InputIterator first, InputIterator last, const Allocator& a);

    template<container-compatible-range<value_type> R>
      flat_multiset(from_range_t fr, R&& rg)
        : flat_multiset(fr, std::forward<R>(rg), key_compare()) { }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_multiset(from_range_t, R&& rg, const Allocator& a);
    template<container-compatible-range<value_type> R>
      flat_multiset(from_range_t, R&& rg, const key_compare& comp)
        : flat_multiset(comp)
        { insert_range(std::forward<R>(rg)); }
    template<container-compatible-range<value_type> R, class Allocator>
      flat_multiset(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);

    template<class InputIterator>
      flat_multiset(sorted_equivalent_t, InputIterator first, InputIterator last,
                    const key_compare& comp = key_compare())
        : c(first, last), compare(comp) { }
    template<class InputIterator, class Allocator>
      flat_multiset(sorted_equivalent_t, InputIterator first, InputIterator last,
                    const key_compare& comp, const Allocator& a);
    template<class InputIterator, class Allocator>
      flat_multiset(sorted_equivalent_t, InputIterator first, InputIterator last,
                    const Allocator& a);

    flat_multiset(initializer_list<value_type> il, const key_compare& comp = key_compare())
      : flat_multiset(il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_multiset(initializer_list<value_type> il, const key_compare& comp,
                    const Allocator& a);
    template<class Allocator>
      flat_multiset(initializer_list<value_type> il, const Allocator& a);

    flat_multiset(sorted_equivalent_t s, initializer_list<value_type> il,
                  const key_compare& comp = key_compare())
        : flat_multiset(s, il.begin(), il.end(), comp) { }
    template<class Allocator>
      flat_multiset(sorted_equivalent_t, initializer_list<value_type> il,
                    const key_compare& comp, const Allocator& a);
    template<class Allocator>
      flat_multiset(sorted_equivalent_t, initializer_list<value_type> il, const Allocator& a);

    flat_multiset& operator=(initializer_list<value_type>);

    // iterators
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

    // capacity
    [[nodiscard]] bool empty() const noexcept;
    size_type size() const noexcept;
    size_type max_size() const noexcept;

    // [flat.multiset.modifiers], modifiers
    template<class... Args> iterator emplace(Args&&... args);
    template<class... Args>
      iterator emplace_hint(const_iterator position, Args&&... args);

    iterator insert(const value_type& x)
      { return emplace(x); }
    iterator insert(value_type&& x)
      { return emplace(std::move(x)); }
    iterator insert(const_iterator position, const value_type& x)
      { return emplace_hint(position, x); }
    iterator insert(const_iterator position, value_type&& x)
      { return emplace_hint(position, std::move(x)); }

    template<class InputIterator>
      void insert(InputIterator first, InputIterator last);
    template<class InputIterator>
      void insert(sorted_equivalent_t, InputIterator first, InputIterator last);
    template<container-compatible-range<value_type> R>
      void insert_range(R&& rg);

    void insert(initializer_list<value_type> il)
      { insert(il.begin(), il.end()); }
    void insert(sorted_equivalent_t s, initializer_list<value_type> il)
      { insert(s, il.begin(), il.end()); }

    container_type extract() &&;
    void replace(container_type&&);

    iterator erase(iterator position);
    iterator erase(const_iterator position);
    size_type erase(const key_type& x);
    template<class K> size_type erase(K&& x);
    iterator erase(const_iterator first, const_iterator last);

    void swap(flat_multiset& y) noexcept;
    void clear() noexcept;

    // observers
    key_compare key_comp() const;
    value_compare value_comp() const;

    // set operations
    iterator find(const key_type& x);
    const_iterator find(const key_type& x) const;
    template<class K> iterator find(const K& x);
    template<class K> const_iterator find(const K& x) const;

    size_type count(const key_type& x) const;
    template<class K> size_type count(const K& x) const;

    bool contains(const key_type& x) const;
    template<class K> bool contains(const K& x) const;

    iterator lower_bound(const key_type& x);
    const_iterator lower_bound(const key_type& x) const;
    template<class K> iterator lower_bound(const K& x);
    template<class K> const_iterator lower_bound(const K& x) const;

    iterator upper_bound(const key_type& x);
    const_iterator upper_bound(const key_type& x) const;
    template<class K> iterator upper_bound(const K& x);
    template<class K> const_iterator upper_bound(const K& x) const;

    pair<iterator, iterator> equal_range(const key_type& x);
    pair<const_iterator, const_iterator> equal_range(const key_type& x) const;
    template<class K>
      pair<iterator, iterator> equal_range(const K& x);
    template<class K>
      pair<const_iterator, const_iterator> equal_range(const K& x) const;

    friend bool operator==(const flat_multiset& x, const flat_multiset& y);

    friend synth-three-way-result<value_type>
      operator<=>(const flat_multiset& x, const flat_multiset& y);

    friend void swap(flat_multiset& x, flat_multiset& y) noexcept
      { x.swap(y); }

  private:
    container_type c;       // exposition only
    key_compare compare;    // exposition only
  };

  template<class KeyContainer, class Compare = less<typename KeyContainer::value_type>>
    flat_multiset(KeyContainer, Compare = Compare())
      -> flat_multiset<typename KeyContainer::value_type, Compare, KeyContainer>;
  template<class KeyContainer, class Allocator>
    flat_multiset(KeyContainer, Allocator)
      -> flat_multiset<typename KeyContainer::value_type,
                       less<typename KeyContainer::value_type>, KeyContainer>;
  template<class KeyContainer, class Compare, class Allocator>
    flat_multiset(KeyContainer, Compare, Allocator)
      -> flat_multiset<typename KeyContainer::value_type, Compare, KeyContainer>;

  template<class KeyContainer, class Compare = less<typename KeyContainer::value_type>>
    flat_multiset(sorted_equivalent_t, KeyContainer, Compare = Compare())
      -> flat_multiset<typename KeyContainer::value_type, Compare, KeyContainer>;
  template<class KeyContainer, class Allocator>
    flat_multiset(sorted_equivalent_t, KeyContainer, Allocator)
      -> flat_multiset<typename KeyContainer::value_type,
                       less<typename KeyContainer::value_type>, KeyContainer>;
  template<class KeyContainer, class Compare, class Allocator>
    flat_multiset(sorted_equivalent_t, KeyContainer, Compare, Allocator)
      -> flat_multiset<typename KeyContainer::value_type, Compare, KeyContainer>;

  template<class InputIterator, class Compare = less<iter-value-type<InputIterator>>>
    flat_multiset(InputIterator, InputIterator, Compare = Compare())
      -> flat_multiset<iter-value-type<InputIterator>, iter-value-type<InputIterator>, Compare>;

  template<class InputIterator, class Compare = less<iter-value-type<InputIterator>>>
    flat_multiset(sorted_equivalent_t, InputIterator, InputIterator, Compare = Compare())
      -> flat_multiset<iter-value-type<InputIterator>, iter-value-type<InputIterator>, Compare>;

  template<ranges::input_range R, class Compare = less<ranges::range_value_t<R>>,
           class Allocator = allocator<ranges::range_value_t<R>>>
    flat_multiset(from_range_t, R&&, Compare = Compare(), Allocator = Allocator())
      -> flat_multiset<ranges::range_value_t<R>, Compare,
                       vector<ranges::range_value_t<R>,
                              alloc-rebind<Allocator, ranges::range_value_t<R>>>>;

  template<ranges::input_range R, class Allocator>
    flat_multiset(from_range_t, R&&, Allocator)
      -> flat_multiset<ranges::range_value_t<R>, less<ranges::range_value_t<R>>,
                       vector<ranges::range_value_t<R>,
                              alloc-rebind<Allocator, ranges::range_value_t<R>>>>;

  template<class Key, class Compare = less<Key>>
    flat_multiset(initializer_list<Key>, Compare = Compare())
      -> flat_multiset<Key, Compare>;

  template<class Key, class Compare = less<Key>>
  flat_multiset(sorted_equivalent_t, initializer_list<Key>, Compare = Compare())
      -> flat_multiset<Key, Compare>;

  template<class Key, class Compare, class KeyContainer, class Allocator>
    struct uses_allocator<flat_multiset<Key, Compare, KeyContainer>, Allocator>
      : bool_constant<uses_allocator_v<KeyContainer, Allocator>> { };
}
```

#### Constructors <a id="flat.multiset.cons">[[flat.multiset.cons]]</a>

``` cpp
explicit flat_multiset(container_type cont, const key_compare& comp = key_compare());
```

*Effects:* Initializes *c* with `std::move(cont)` and *compare* with
`comp`, and sorts the range \[`begin()`, `end()`) with respect to
*compare*.

*Complexity:* Linear in N if `cont` is sorted with respect to *compare*
and otherwise N log N, where N is the value of `cont.size()` before this
call.

``` cpp
template<class Allocator>
  flat_multiset(const container_type& cont, const Allocator& a);
template<class Allocator>
  flat_multiset(const container_type& cont, const key_compare& comp, const Allocator& a);
```

*Constraints:* `uses_allocator_v<container_type, Allocator>` is `true`.

*Effects:* Equivalent to `flat_multiset(cont)` and
`flat_multiset(cont, comp)`, respectively, except that *c* is
constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Same as `flat_multiset(cont)` and
`flat_multiset(cont, comp)`, respectively.

``` cpp
template<class Allocator>
  flat_multiset(sorted_equivalent_t s, const container_type& cont, const Allocator& a);
template<class Allocator>
  flat_multiset(sorted_equivalent_t s, const container_type& cont,
                const key_compare& comp, const Allocator& a);
```

*Constraints:* `uses_allocator_v<container_type, Allocator>` is `true`.

*Effects:* Equivalent to `flat_multiset(s, cont)` and
`flat_multiset(s, cont, comp)`, respectively, except that *c* is
constructed with uses-allocator
construction [[allocator.uses.construction]].

*Complexity:* Linear.

``` cpp
template<class Allocator>
  flat_multiset(const key_compare& comp, const Allocator& a);
template<class Allocator>
  explicit flat_multiset(const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multiset(InputIterator first, InputIterator last,
                const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multiset(InputIterator first, InputIterator last, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_multiset(from_range_t, R&& rg, const Allocator& a);
template<container-compatible-range<value_type> R, class Allocator>
  flat_multiset(from_range_t, R&& rg, const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multiset(sorted_equivalent_t, InputIterator first, InputIterator last,
                const key_compare& comp, const Allocator& a);
template<class InputIterator, class Allocator>
  flat_multiset(sorted_equivalent_t, InputIterator first, InputIterator last, const Allocator& a);
template<class Allocator>
  flat_multiset(initializer_list<value_type> il, const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_multiset(initializer_list<value_type> il, const Allocator& a);
template<class Allocator>
  flat_multiset(sorted_equivalent_t, initializer_list<value_type> il,
                const key_compare& comp, const Allocator& a);
template<class Allocator>
  flat_multiset(sorted_equivalent_t, initializer_list<value_type> il, const Allocator& a);
```

*Constraints:* `uses_allocator_v<container_type, Allocator>` is `true`.

*Effects:* Equivalent to the corresponding non-allocator constructors
except that *c* is constructed with uses-allocator
construction [[allocator.uses.construction]].

#### Modifiers <a id="flat.multiset.modifiers">[[flat.multiset.modifiers]]</a>

``` cpp
template<class... Args> iterator emplace(Args&&... args);
```

*Constraints:* `is_constructible_v<value_type, Args...>` is `true`.

*Effects:* First, initializes an object `t` of type `value_type` with
`std::forward<Args>(args)...`, then inserts `t` as if by:

``` cpp
auto it = ranges::upper_bound(c, t, compare);
c.insert(it, std::move(t));
```

*Returns:* An iterator that points to the inserted element.

``` cpp
template<class InputIterator>
  void insert(InputIterator first, InputIterator last);
```

*Effects:* Adds elements to *c* as if by:

``` cpp
c.insert(c.end(), first, last);
```

Then, sorts the range of newly inserted elements with respect to
*compare*, and merges the resulting sorted range and the sorted range of
pre-existing elements into a single sorted range.

*Complexity:* N + M log M, where N is `size()` before the operation and
M is `distance(first, last)`.

*Remarks:* Since this operation performs an in-place merge, it may
allocate memory.

``` cpp
template<class InputIterator>
  void insert(sorted_equivalent_t, InputIterator first, InputIterator last);
```

*Effects:* Equivalent to `insert(first, last)`.

*Complexity:* Linear.

``` cpp
void swap(flat_multiset& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
ranges::swap(compare, y.compare);
ranges::swap(c, y.c);
```

``` cpp
container_type extract() &&;
```

*Ensures:* `*this` is emptied, even if the function exits via an
exception.

*Returns:* `std::move(c)`.

``` cpp
void replace(container_type&& cont);
```

*Preconditions:* The elements of `cont` are sorted with respect to
*compare*.

*Effects:* Equivalent to: `c = std::move(cont);`

#### Erasure <a id="flat.multiset.erasure">[[flat.multiset.erasure]]</a>

``` cpp
template<class Key, class Compare, class KeyContainer, class Predicate>
  typename flat_multiset<Key, Compare, KeyContainer>::size_type
    erase_if(flat_multiset<Key, Compare, KeyContainer>& c, Predicate pred);
```

*Preconditions:* `Key` meets the *Cpp17MoveAssignable* requirements.

*Effects:* Let E be `bool(pred(as_const(e)))`. Erases all elements `e`
in `c` for which E holds.

*Returns:* The number of elements erased.

*Complexity:* Exactly `c.size()` applications of the predicate.

*Remarks:* Stable [[algorithm.stable]]. If an invocation of `erase_if`
exits via an exception, `c` is in a valid but unspecified
state [[defns.valid]].

[*Note 1*: `c` still meets its invariants, but can be
empty. — *end note*]

### Container adaptors formatting <a id="container.adaptors.format">[[container.adaptors.format]]</a>

For each of `queue`, `priority_queue`, and `stack`, the library provides
the following formatter specialization where `adaptor-type` is the name
of the template:

``` cpp
namespace std {
  template<class charT, class T, formattable<charT> Container, class... U>
  struct formatter<adaptor-type<T, Container, U...>, charT> {
  private:
    using maybe-const-container =                                             // exposition only
      fmt-maybe-const<Container, charT>;
    using maybe-const-adaptor =                                               // exposition only
      maybe-const<is_const_v<maybe-const-container>,                          // see [ranges.syn]
                  adaptor-type<T, Container, U...>>;
    formatter<ranges::ref_view<maybe-const-container>, charT> underlying_;    // exposition only

  public:
    template<class ParseContext>
      constexpr typename ParseContext::iterator
        parse(ParseContext& ctx);

    template<class FormatContext>
      typename FormatContext::iterator
        format(maybe-const-adaptor& r, FormatContext& ctx) const;
  };
}
```

``` cpp
template<class ParseContext>
  constexpr typename ParseContext::iterator
    parse(ParseContext& ctx);
```

*Effects:* Equivalent to: `return `*`underlying_`*`.parse(ctx);`

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(maybe-const-adaptor& r, FormatContext& ctx) const;
```

*Effects:* Equivalent to: `return `*`underlying_`*`.format(r.c, ctx);`

## Views <a id="views">[[views]]</a>

### General <a id="views.general">[[views.general]]</a>

The header `<span>` defines the view `span`. The header `<mdspan>`
defines the class template `mdspan` and other facilities for interacting
with these multidimensional views.

### Contiguous access <a id="views.contiguous">[[views.contiguous]]</a>

#### Header `<span>` synopsis <a id="span.syn">[[span.syn]]</a>

``` cpp
namespace std {
  // constants
  inline constexpr size_t dynamic_extent = numeric_limits<size_t>::max();

  // [views.span], class template span
  template<class ElementType, size_t Extent = dynamic_extent>
    class span;

  template<class ElementType, size_t Extent>
    constexpr bool ranges::enable_view<span<ElementType, Extent>> = true;
  template<class ElementType, size_t Extent>
    constexpr bool ranges::enable_borrowed_range<span<ElementType, Extent>> = true;

  // [span.objectrep], views of object representation
  template<class ElementType, size_t Extent>
    span<const byte, Extent == dynamic_extent ? dynamic_extent : sizeof(ElementType) * Extent>
      as_bytes(span<ElementType, Extent> s) noexcept;

  template<class ElementType, size_t Extent>
    span<byte, Extent == dynamic_extent ? dynamic_extent : sizeof(ElementType) * Extent>
      as_writable_bytes(span<ElementType, Extent> s) noexcept;
}
```

#### Class template `span` <a id="views.span">[[views.span]]</a>

##### Overview <a id="span.overview">[[span.overview]]</a>

A `span` is a view over a contiguous sequence of objects, the storage of
which is owned by some other object.

All member functions of `span` have constant time complexity.

``` cpp
namespace std {
  template<class ElementType, size_t Extent = dynamic_extent>
  class span {
  public:
    // constants and types
    using element_type = ElementType;
    using value_type = remove_cv_t<ElementType>;
    using size_type = size_t;
    using difference_type = ptrdiff_t;
    using pointer = element_type*;
    using const_pointer = const element_type*;
    using reference = element_type&;
    using const_reference = const element_type&;
    using iterator = implementation-defined  // type of span::iterator;        // see [span.iterators]
    using const_iterator = std::const_iterator<iterator>;
    using reverse_iterator = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::const_iterator<reverse_iterator>;
    static constexpr size_type extent = Extent;

    // [span.cons], constructors, copy, and assignment
    constexpr span() noexcept;
    template<class It>
      constexpr explicit(extent != dynamic_extent) span(It first, size_type count);
    template<class It, class End>
      constexpr explicit(extent != dynamic_extent) span(It first, End last);
    template<size_t N>
      constexpr span(type_identity_t<element_type> (&arr)[N]) noexcept;
    template<class T, size_t N>
      constexpr span(array<T, N>& arr) noexcept;
    template<class T, size_t N>
      constexpr span(const array<T, N>& arr) noexcept;
    template<class R>
      constexpr explicit(extent != dynamic_extent) span(R&& r);
    constexpr span(const span& other) noexcept = default;
    template<class OtherElementType, size_t OtherExtent>
      constexpr explicit(see below) span(const span<OtherElementType, OtherExtent>& s) noexcept;

    ~span() noexcept = default;

    constexpr span& operator=(const span& other) noexcept = default;

    // [span.sub], subviews
    template<size_t Count>
      constexpr span<element_type, Count> first() const;
    template<size_t Count>
      constexpr span<element_type, Count> last() const;
    template<size_t Offset, size_t Count = dynamic_extent>
      constexpr span<element_type, see below> subspan() const;

    constexpr span<element_type, dynamic_extent> first(size_type count) const;
    constexpr span<element_type, dynamic_extent> last(size_type count) const;
    constexpr span<element_type, dynamic_extent> subspan(
      size_type offset, size_type count = dynamic_extent) const;

    // [span.obs], observers
    constexpr size_type size() const noexcept;
    constexpr size_type size_bytes() const noexcept;
    [[nodiscard]] constexpr bool empty() const noexcept;

    // [span.elem], element access
    constexpr reference operator[](size_type idx) const;
    constexpr reference front() const;
    constexpr reference back() const;
    constexpr pointer data() const noexcept;

    // [span.iterators], iterator support
    constexpr iterator begin() const noexcept;
    constexpr iterator end() const noexcept;
    constexpr const_iterator cbegin() const noexcept { return begin(); }
    constexpr const_iterator cend() const noexcept { return end(); }
    constexpr reverse_iterator rbegin() const noexcept;
    constexpr reverse_iterator rend() const noexcept;
    constexpr const_reverse_iterator crbegin() const noexcept { return rbegin(); }
    constexpr const_reverse_iterator crend() const noexcept { return rend(); }

  private:
    pointer data_;              // exposition only
    size_type size_;            // exposition only
  };

  template<class It, class EndOrSize>
    span(It, EndOrSize) -> span<remove_reference_t<iter_reference_t<It>>>;
  template<class T, size_t N>
    span(T (&)[N]) -> span<T, N>;
  template<class T, size_t N>
    span(array<T, N>&) -> span<T, N>;
  template<class T, size_t N>
    span(const array<T, N>&) -> span<const T, N>;
  template<class R>
    span(R&&) -> span<remove_reference_t<ranges::range_reference_t<R>>>;
}
```

`span<ElementType, Extent>` is a trivially copyable type
[[term.trivially.copyable.type]].

`ElementType` is required to be a complete object type that is not an
abstract class type.

##### Constructors, copy, and assignment <a id="span.cons">[[span.cons]]</a>

``` cpp
constexpr span() noexcept;
```

*Constraints:* `Extent == dynamic_extent || Extent == 0` is `true`.

*Ensures:* `size() == 0 && data() == nullptr`.

``` cpp
template<class It>
  constexpr explicit(extent != dynamic_extent) span(It first, size_type count);
```

*Constraints:* Let `U` be `remove_reference_t<iter_reference_t<It>>`.

- `It` satisfies `contiguous_iterator`.
- `is_convertible_v<U(*)[], element_type(*)[]>` is `true`.
  \[*Note 3*: The intent is to allow only qualification conversions of
  the iterator reference type to `element_type`. — *end note*]

*Preconditions:*

- \[`first`, `first + count`) is a valid range.
- `It` models `contiguous_iterator`.
- If `extent` is not equal to `dynamic_extent`, then `count` is equal to
  `extent`.

*Effects:* Initializes *`data_`* with `to_address(first)` and *`size_`*
with `count`.

*Throws:* Nothing.

``` cpp
template<class It, class End>
  constexpr explicit(extent != dynamic_extent) span(It first, End last);
```

*Constraints:* Let `U` be `remove_reference_t<iter_reference_t<It>>`.

- `is_convertible_v<U(*)[], element_type(*)[]>` is `true`.
  \[*Note 4*: The intent is to allow only qualification conversions of
  the iterator reference type to `element_type`. — *end note*]
- `It` satisfies `contiguous_iterator`.
- `End` satisfies `sized_sentinel_for<It>`.
- `is_convertible_v<End, size_t>` is `false`.

*Preconditions:*

- If `extent` is not equal to `dynamic_extent`, then `last - first` is
  equal to `extent`.
- \[`first`, `last`) is a valid range.
- `It` models `contiguous_iterator`.
- `End` models `sized_sentinel_for<It>`.

*Effects:* Initializes *`data_`* with `to_address(first)` and *`size_`*
with `last - first`.

*Throws:* When and what `last - first` throws.

``` cpp
template<size_t N> constexpr span(type_identity_t<element_type> (&arr)[N]) noexcept;
template<class T, size_t N> constexpr span(array<T, N>& arr) noexcept;
template<class T, size_t N> constexpr span(const array<T, N>& arr) noexcept;
```

*Constraints:* Let `U` be `remove_pointer_t<decltype(data(arr))>`.

- `extent == dynamic_extent || N == extent` is `true`, and
- `is_convertible_v<U(*)[], element_type(*)[]>` is `true`.
  \[*Note 5*: The intent is to allow only qualification conversions of
  the array element type to `element_type`. — *end note*]

*Effects:* Constructs a `span` that is a view over the supplied array.

[*Note 1*: `type_identity_t` affects class template argument
deduction. — *end note*]

*Ensures:* `size() == N && data() == data(arr)` is `true`.

``` cpp
template<class R> constexpr explicit(extent != dynamic_extent) span(R&& r);
```

*Constraints:* Let `U` be
`remove_reference_t<ranges::range_reference_t<R>>`.

- `R` satisfies `ranges::contiguous_range` and `ranges::sized_range`.
- Either `R` satisfies `ranges::borrowed_range` or
  `is_const_v<element_type>` is `true`.
- `remove_cvref_t<R>` is not a specialization of `span`.
- `remove_cvref_t<R>` is not a specialization of `array`.
- `is_array_v<remove_cvref_t<R>>` is `false`.
- `is_convertible_v<U(*)[], element_type(*)[]>` is `true`.
  \[*Note 6*: The intent is to allow only qualification conversions of
  the range reference type to `element_type`. — *end note*]

*Preconditions:*

- If `extent` is not equal to `dynamic_extent`, then `ranges::size(r)`
  is equal to `extent`.
- `R` models `ranges::contiguous_range` and `ranges::sized_range`.
- If `is_const_v<element_type>` is `false`, `R` models
  `ranges::borrowed_range`.

*Effects:* Initializes *`data_`* with `ranges::data(r)` and *`size_`*
with `ranges::size(r)`.

*Throws:* What and when `ranges::data(r)` and `ranges::size(r)` throw.

``` cpp
constexpr span(const span& other) noexcept = default;
```

*Ensures:* `other.size() == size() && other.data() == data()`.

``` cpp
template<class OtherElementType, size_t OtherExtent>
  constexpr explicit(see below) span(const span<OtherElementType, OtherExtent>& s) noexcept;
```

*Constraints:*

- `extent == dynamic_extent` `||` `OtherExtent == dynamic_extent` `||`
  `extent == OtherExtent` is `true`, and
- `is_convertible_v<OtherElementType(*)[], element_type(*)[]>` is
  `true`. \[*Note 7*: The intent is to allow only qualification
  conversions of the `OtherElementType` to
  `element_type`. — *end note*]

*Preconditions:* If `extent` is not equal to `dynamic_extent`, then
`s.size()` is equal to `extent`.

*Effects:* Constructs a `span` that is a view over the range
\[`s.data()`, `s.data() + s.size()`).

*Ensures:* `size() == s.size() && data() == s.data()`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
extent != dynamic_extent && OtherExtent == dynamic_extent
```

``` cpp
constexpr span& operator=(const span& other) noexcept = default;
```

*Ensures:* `size() == other.size() && data() == other.data()`.

##### Deduction guides <a id="span.deduct">[[span.deduct]]</a>

``` cpp
template<class It, class EndOrSize>
  span(It, EndOrSize) -> span<remove_reference_t<iter_reference_t<It>>>;
```

*Constraints:* `It` satisfies `contiguous_iterator`.

``` cpp
template<class R>
  span(R&&) -> span<remove_reference_t<ranges::range_reference_t<R>>>;
```

*Constraints:* `R` satisfies `ranges::contiguous_range`.

##### Subviews <a id="span.sub">[[span.sub]]</a>

``` cpp
template<size_t Count> constexpr span<element_type, Count> first() const;
```

*Mandates:* `Count <= Extent` is `true`.

*Preconditions:* `Count <= size()` is `true`.

*Effects:* Equivalent to: `return R{data(), Count};` where `R` is the
return type.

``` cpp
template<size_t Count> constexpr span<element_type, Count> last() const;
```

*Mandates:* `Count <= Extent` is `true`.

*Preconditions:* `Count <= size()` is `true`.

*Effects:* Equivalent to: `return R{data() + (size() - Count), Count};`
where `R` is the return type.

``` cpp
template<size_t Offset, size_t Count = dynamic_extent>
  constexpr span<element_type, see below> subspan() const;
```

*Mandates:*

``` cpp
Offset <= Extent && (Count == dynamic_extent || Count <= Extent - Offset)
```

is `true`.

*Preconditions:*

``` cpp
Offset <= size() && (Count == dynamic_extent || Count <= size() - Offset)
```

is `true`.

*Effects:* Equivalent to:

``` cpp
return span<ElementType, see below>(
  data() + Offset, Count != dynamic_extent ? Count : size() - Offset);
```

*Remarks:* The second template argument of the returned `span` type is:

``` cpp
Count != dynamic_extent ? Count
                        : (Extent != dynamic_extent ? Extent - Offset
                                                    : dynamic_extent)
```

``` cpp
constexpr span<element_type, dynamic_extent> first(size_type count) const;
```

*Preconditions:* `count <= size()` is `true`.

*Effects:* Equivalent to: `return {data(), count};`

``` cpp
constexpr span<element_type, dynamic_extent> last(size_type count) const;
```

*Preconditions:* `count <= size()` is `true`.

*Effects:* Equivalent to: `return {data() + (size() - count), count};`

``` cpp
constexpr span<element_type, dynamic_extent> subspan(
  size_type offset, size_type count = dynamic_extent) const;
```

*Preconditions:*

``` cpp
offset <= size() && (count == dynamic_extent || count <= size() - offset)
```

is `true`.

*Effects:* Equivalent to:

``` cpp
return {data() + offset, count == dynamic_extent ? size() - offset : count};
```

##### Observers <a id="span.obs">[[span.obs]]</a>

``` cpp
constexpr size_type size() const noexcept;
```

*Effects:* Equivalent to: `return `*`size_`*`;`

``` cpp
constexpr size_type size_bytes() const noexcept;
```

*Effects:* Equivalent to: `return size() * sizeof(element_type);`

``` cpp
[[nodiscard]] constexpr bool empty() const noexcept;
```

*Effects:* Equivalent to: `return size() == 0;`

##### Element access <a id="span.elem">[[span.elem]]</a>

``` cpp
constexpr reference operator[](size_type idx) const;
```

*Preconditions:* `idx < size()` is `true`.

*Effects:* Equivalent to: `return *(data() + idx);`

``` cpp
constexpr reference front() const;
```

*Preconditions:* `empty()` is `false`.

*Effects:* Equivalent to: `return *data();`

``` cpp
constexpr reference back() const;
```

*Preconditions:* `empty()` is `false`.

*Effects:* Equivalent to: `return *(data() + (size() - 1));`

``` cpp
constexpr pointer data() const noexcept;
```

*Effects:* Equivalent to: `return `*`data_`*`;`

##### Iterator support <a id="span.iterators">[[span.iterators]]</a>

``` cpp
using iterator = implementation-defined  // type of span::iterator;
```

The type models `contiguous_iterator`[[iterator.concept.contiguous]],
meets the *Cpp17RandomAccessIterator*
requirements [[random.access.iterators]], and meets the requirements for
constexpr iterators [[iterator.requirements.general]], whose value type
is `value_type` and whose reference type is `reference`.

All requirements on container iterators [[container.reqmts]] apply to
`span::iterator` as well.

``` cpp
constexpr iterator begin() const noexcept;
```

*Returns:* An iterator referring to the first element in the span. If
`empty()` is `true`, then it returns the same value as `end()`.

``` cpp
constexpr iterator end() const noexcept;
```

*Returns:* An iterator which is the past-the-end value.

``` cpp
constexpr reverse_iterator rbegin() const noexcept;
```

*Effects:* Equivalent to: `return reverse_iterator(end());`

``` cpp
constexpr reverse_iterator rend() const noexcept;
```

*Effects:* Equivalent to: `return reverse_iterator(begin());`

#### Views of object representation <a id="span.objectrep">[[span.objectrep]]</a>

``` cpp
template<class ElementType, size_t Extent>
  span<const byte, Extent == dynamic_extent ? dynamic_extent : sizeof(ElementType) * Extent>
    as_bytes(span<ElementType, Extent> s) noexcept;
```

*Effects:* Equivalent to:
`return R{reinterpret_cast<const byte*>(s.data()), s.size_bytes()};`
where `R` is the return type.

``` cpp
template<class ElementType, size_t Extent>
  span<byte, Extent == dynamic_extent ? dynamic_extent : sizeof(ElementType) * Extent>
    as_writable_bytes(span<ElementType, Extent> s) noexcept;
```

*Constraints:* `is_const_v<ElementType>` is `false`.

*Effects:* Equivalent to:
`return R{reinterpret_cast<byte*>(s.data()), s.size_bytes()};` where `R`
is the return type.

### Multidimensional access <a id="views.multidim">[[views.multidim]]</a>

#### Overview <a id="mdspan.overview">[[mdspan.overview]]</a>

A *multidimensional index space* is a Cartesian product of integer
intervals. Each interval can be represented by a half-open range
[Lᵢ, Uᵢ), where Lᵢ and Uᵢ are the lower and upper bounds of the iᵗʰ
dimension. The *rank* of a multidimensional index space is the number of
intervals it represents. The *size of a multidimensional index space* is
the product of Uᵢ - Lᵢ for each dimension i if its rank is greater than
0, and 1 otherwise.

An integer r is a *rank index* of an index space S if r is in the range
[0, rank of $S$).

A pack of integers `idx` is a *multidimensional index* in a
multidimensional index space S (or representation thereof) if both of
the following are true:

- `sizeof...(idx)` is equal to the rank of S, and
- for every rank index i of S, the iᵗʰ value of `idx` is an integer in
  the interval [Lᵢ, Uᵢ) of S.

#### Header `<mdspan>` synopsis <a id="mdspan.syn">[[mdspan.syn]]</a>

``` cpp
namespace std {
  // [mdspan.extents], class template extents
  template<class IndexType, size_t... Extents>
    class extents;

  // [mdspan.extents.dextents], alias template dextents
  template<class IndexType, size_t Rank>
    using dextents = see below;

  // [mdspan.layout], layout mapping
  struct layout_left;
  struct layout_right;
  struct layout_stride;

  // [mdspan.accessor.default], class template default_accessor
  template<class ElementType>
    class default_accessor;

  // [mdspan.mdspan], class template mdspan
  template<class ElementType, class Extents, class LayoutPolicy = layout_right,
           class AccessorPolicy = default_accessor<ElementType>>
    class mdspan;
}
```

#### Class template `extents` <a id="mdspan.extents">[[mdspan.extents]]</a>

##### Overview <a id="mdspan.extents.overview">[[mdspan.extents.overview]]</a>

The class template `extents` represents a multidimensional index space
of rank equal to `sizeof...(Extents)`. In subclause [[views]], `extents`
is used synonymously with multidimensional index space.

``` cpp
namespace std {
  template<class IndexType, size_t... Extents>
  class extents {
  public:
    using index_type = IndexType;
    using size_type = make_unsigned_t<index_type>;
    using rank_type = size_t;

    // [mdspan.extents.obs], observers of the multidimensional index space
    static constexpr rank_type rank() noexcept { return sizeof...(Extents); }
    static constexpr rank_type rank_dynamic() noexcept { return dynamic-index(rank()); }
    static constexpr size_t static_extent(rank_type) noexcept;
    constexpr index_type extent(rank_type) const noexcept;

    // [mdspan.extents.cons], constructors
    constexpr extents() noexcept = default;

    template<class OtherIndexType, size_t... OtherExtents>
      constexpr explicit(see below)
        extents(const extents<OtherIndexType, OtherExtents...>&) noexcept;
    template<class... OtherIndexTypes>
      constexpr explicit extents(OtherIndexTypes...) noexcept;
    template<class OtherIndexType, size_t N>
      constexpr explicit(N != rank_dynamic())
        extents(span<OtherIndexType, N>) noexcept;
    template<class OtherIndexType, size_t N>
      constexpr explicit(N != rank_dynamic())
        extents(const array<OtherIndexType, N>&) noexcept;

    // [mdspan.extents.cmp], comparison operators
    template<class OtherIndexType, size_t... OtherExtents>
      friend constexpr bool operator==(const extents&,
                                       const extents<OtherIndexType, OtherExtents...>&) noexcept;

    // [mdspan.extents.expo], exposition-only helpers
    constexpr size_t fwd-prod-of-extents(rank_type) const noexcept;     // exposition only
    constexpr size_t rev-prod-of-extents(rank_type) const noexcept;     // exposition only
    template<class OtherIndexType>
      static constexpr auto index-cast(OtherIndexType&&) noexcept;      // exposition only

  private:
    static constexpr rank_type dynamic-index(rank_type) noexcept;       // exposition only
    static constexpr rank_type dynamic-index-inv(rank_type) noexcept;   // exposition only
    array<index_type, rank_dynamic()> dynamic-extents{};                // exposition only
  };

  template<class... Integrals>
    explicit extents(Integrals...)
      -> see below;
}
```

*Mandates:*

- `IndexType` is a signed or unsigned integer type, and
- each element of `Extents` is either equal to `dynamic_extent`, or is
  representable as a value of type `IndexType`.

Each specialization of `extents` models `regular` and is trivially
copyable.

Let Eᵣ be the rᵗʰ element of `Extents`. Eᵣ is a *dynamic extent* if it
is equal to `dynamic_extent`, otherwise Eᵣ is a *static extent*. Let Dᵣ
be the value of `dynamic-extents[dynamic-index(r)]` if Eᵣ is a dynamic
extent, otherwise Eᵣ.

The rᵗʰ interval of the multidimensional index space represented by an
`extents` object is [0, Dᵣ).

##### Exposition-only helpers <a id="mdspan.extents.expo">[[mdspan.extents.expo]]</a>

``` cpp
static constexpr rank_type dynamic-index(rank_type i) noexcept;
```

*Preconditions:* `i <= rank()` is `true`.

*Returns:* The number of Eᵣ with r < `i` for which Eᵣ is a dynamic
extent.

``` cpp
static constexpr rank_type dynamic-index-inv(rank_type i) noexcept;
```

*Preconditions:* `i < rank_dynamic()` is `true`.

*Returns:* The minimum value of r such that
*`dynamic-index`*`(`r` + 1) == i + 1` is `true`.

``` cpp
constexpr size_t fwd-prod-of-extents(rank_type i) const noexcept;
```

*Preconditions:* `i <= rank()` is `true`.

*Returns:* If `i > 0` is `true`, the product of `extent(`k`)` for all k
in the range [0, `i`), otherwise `1`.

``` cpp
constexpr size_t rev-prod-of-extents(rank_type i) const noexcept;
```

*Preconditions:* `i < rank()` is `true`.

*Returns:* If `i + 1 < rank()` is `true`, the product of `extent(`k`)`
for all k in the range [`i + 1`, `rank()`), otherwise `1`.

``` cpp
template<class OtherIndexType>
  static constexpr auto index-cast(OtherIndexType&& i) noexcept;
```

*Effects:*

- If `OtherIndexType` is an integral type other than `bool`, then
  equivalent to `return i;`,
- otherwise, equivalent to `return static_cast<index_type>(i);`.

[*Note 1*: This function will always return an integral type other than
`bool`. Since this function’s call sites are constrained on
convertibility of `OtherIndexType` to `index_type`, integer-class types
can use the `static_cast` branch without loss of
precision. — *end note*]

##### Constructors <a id="mdspan.extents.cons">[[mdspan.extents.cons]]</a>

``` cpp
template<class OtherIndexType, size_t... OtherExtents>
  constexpr explicit(see below)
    extents(const extents<OtherIndexType, OtherExtents...>& other) noexcept;
```

*Constraints:*

- `sizeof...(OtherExtents) == rank()` is `true`.
- `((OtherExtents == dynamic_extent || Extents == dynamic_extent || OtherExtents ==``Extents) && ...)`
  is `true`.

*Preconditions:*

- `other.extent(`r`)` equals Eᵣ for each r for which Eᵣ is a static
  extent, and
- either
  - `sizeof...(OtherExtents)` is zero, or
  - `other.extent(`r`)` is representable as a value of type `index_type`
    for every rank index r of `other`.

*Ensures:* `*this == other` is `true`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
(((Extents != dynamic_extent) && (OtherExtents == dynamic_extent)) || ... ) ||
(numeric_limits<index_type>::max() < numeric_limits<OtherIndexType>::max())
```

``` cpp
template<class... OtherIndexTypes>
  constexpr explicit extents(OtherIndexTypes... exts) noexcept;
```

Let `N` be `sizeof...(OtherIndexTypes)`, and let `exts_arr` be
`array<index_type, N>{static_cast<`  
`index_type>(std::move(exts))...}`.

*Constraints:*

- `(is_convertible_v<OtherIndexTypes, index_type> && ...)` is `true`,
- `(is_nothrow_constructible_v<index_type, OtherIndexTypes> && ...)` is
  `true`, and
- `N == rank_dynamic() || N == rank()` is `true`. \[*Note 8*: One can
  construct `extents` from just dynamic extents, which are all the
  values getting stored, or from all the extents with a
  precondition. — *end note*]

*Preconditions:*

- If `N != rank_dynamic()` is `true`, `exts_arr[`r`]` equals Eᵣ for each
  r for which Eᵣ is a static extent, and
- either
  - `sizeof...(exts) == 0` is `true`, or
  - each element of `exts` is nonnegative and is representable as a
    value of type `index_type`.

*Ensures:* `*this == extents(exts_arr)` is `true`.

``` cpp
template<class OtherIndexType, size_t N>
  constexpr explicit(N != rank_dynamic())
    extents(span<OtherIndexType, N> exts) noexcept;
template<class OtherIndexType, size_t N>
  constexpr explicit(N != rank_dynamic())
    extents(const array<OtherIndexType, N>& exts) noexcept;
```

*Constraints:*

- `is_convertible_v<const OtherIndexType&, index_type>` is `true`,
- `is_nothrow_constructible_v<index_type, const OtherIndexType&>` is
  `true`, and
- `N == rank_dynamic() || N == rank()` is `true`.

*Preconditions:*

- If `N != rank_dynamic()` is `true`, `exts[`r`]` equals Eᵣ for each r
  for which Eᵣ is a static extent, and
- either
  - `N` is zero, or
  - `exts[`r`]` is nonnegative and is representable as a value of type
    `index_type` for every rank index r.

*Effects:*

- If `N` equals `dynamic_rank()`, for all d in the range
  [0, `rank_dynamic()`), direct-non-list-initializes
  *`dynamic-extents`*`[`d`]` with `as_const(exts[`d`])`.
- Otherwise, for all d in the range [0, `rank_dynamic()`),
  direct-non-list-initializes *dynamic-extents*`[`d`]` with
  `as_const(exts[`*`dynamic-index-inv`*`(`d`)])`.

``` cpp
template<class... Integrals>
  explicit extents(Integrals...) -> see below;
```

*Constraints:* `(is_convertible_v<Integrals, size_t> && ...)` is `true`.

*Remarks:* The deduced type is `dextents<size_t, sizeof...(Integrals)>`.

##### Observers of the multidimensional index space <a id="mdspan.extents.obs">[[mdspan.extents.obs]]</a>

``` cpp
static constexpr size_t static_extent(rank_type i) noexcept;
```

*Preconditions:* `i < rank()` is `true`.

*Returns:* E_`i`.

``` cpp
constexpr index_type extent(rank_type i) const noexcept;
```

*Preconditions:* `i < rank()` is `true`.

*Returns:* D_`i`.

##### Comparison operators <a id="mdspan.extents.cmp">[[mdspan.extents.cmp]]</a>

``` cpp
template<class OtherIndexType, size_t... OtherExtents>
  friend constexpr bool operator==(const extents& lhs,
                                   const extents<OtherIndexType, OtherExtents...>& rhs) noexcept;
```

*Returns:* `true` if `lhs.rank()` equals `rhs.rank()` and if
`lhs.extent(r)` equals `rhs.extent(r)` for every rank index `r` of
`rhs`, otherwise `false`.

##### Alias template `dextents` <a id="mdspan.extents.dextents">[[mdspan.extents.dextents]]</a>

``` cpp
template<class IndexType, size_t Rank>
  using dextents = see below;
```

*Result:* A type `E` that is a specialization of `extents` such that
`E::rank() == Rank && E::rank() == E::rank_dynamic()` is `true`, and
`E::index_type` denotes `IndexType`.

#### Layout mapping <a id="mdspan.layout">[[mdspan.layout]]</a>

##### General <a id="mdspan.layout.general">[[mdspan.layout.general]]</a>

In subclauses [[mdspan.layout.reqmts]] and
[[mdspan.layout.policy.reqmts]]:

- `M` denotes a layout mapping class.
- `m` denotes a (possibly const) value of type `M`.
- `i` and `j` are packs of (possibly const) integers that are
  multidimensional indices in `m.extents()` [[mdspan.overview]].
  \[*Note 9*: The type of each element of the packs can be a different
  integer type. — *end note*]
- `r` is a (possibly const) rank index of `typename M::extents_type`.
- `dᵣ` is a pack of (possibly const) integers for which
  `sizeof...(dᵣ) == M::extents_type::rank()` is `true`, the rᵗʰ element
  is equal to 1, and all other elements are equal to 0.

In subclauses [[mdspan.layout.reqmts]] through [[mdspan.layout.stride]],
let *is-mapping-of* be the exposition-only variable template defined as
follows:

``` cpp
template<class Layout, class Mapping>
constexpr bool is-mapping-of =  // exposition only
  is_same_v<typename Layout::template mapping<typename Mapping::extents_type>, Mapping>;
```

##### Requirements <a id="mdspan.layout.reqmts">[[mdspan.layout.reqmts]]</a>

A type `M` meets the *layout mapping* requirements if

- `M` models `copyable` and `equality_comparable`,
- `is_nothrow_move_constructible_v<M>` is `true`,
- `is_nothrow_move_assignable_v<M>` is `true`,
- `is_nothrow_swappable_v<M>` is `true`, and
- the following types and expressions are well-formed and have the
  specified semantics.

``` cpp
typename M::extents_type
```

*Result:* A type that is a specialization of `extents`.

``` cpp
typename M::index_type
```

*Result:* `typename M::extents_type::index_type`.

``` cpp
typename M::rank_type
```

*Result:* `typename M::extents_type::rank_type`.

``` cpp
typename M::layout_type
```

*Result:* A type `MP` that meets the layout mapping policy
requirements [[mdspan.layout.policy.reqmts]] and for which
*`is-mapping-of`*`<MP, M>` is `true`.

``` cpp
m.extents()
```

*Result:* `const typename M::extents_type&`

``` cpp
m(i...)
```

*Result:* `typename M::index_type`

*Returns:* A nonnegative integer less than
`numeric_limits<typename M::index_type>::max()` and less than or equal
to `numeric_limits<size_t>::max()`.

``` cpp
m(i...) == m(static_cast<typename M::index_type>(i)...)
```

*Result:* `bool`

*Returns:* `true`

``` cpp
m.required_span_size()
```

*Result:* `typename M::index_type`

*Returns:* If the size of the multidimensional index space `m.extents()`
is 0, then `0`, else `1` plus the maximum value of `m(i...)` for all
`i`.

``` cpp
m.is_unique()
```

*Result:* `bool`

*Returns:* `true` only if for every `i` and `j` where `(i != j || ...)`
is `true`, `m(i...) != m(j...)` is `true`.

[*Note 1*: A mapping can return `false` even if the condition is met.
For certain layouts, it is possibly not feasible to determine
efficiently whether the layout is unique. — *end note*]

``` cpp
m.is_exhaustive()
```

*Result:* `bool`

*Returns:* `true` only if for all k in the range
[0, `m.required_span_size()`) there exists an `i` such that `m(i...)`
equals k.

[*Note 2*: A mapping can return `false` even if the condition is met.
For certain layouts, it is possibly not feasible to determine
efficiently whether the layout is exhaustive. — *end note*]

``` cpp
m.is_strided()
```

*Result:* `bool`

*Returns:* `true` only if for every rank index r of `m.extents()` there
exists an integer sᵣ such that, for all `i` where (`i`+dᵣ) is a
multidimensional index in `m.extents()`[[mdspan.overview]],
`m((i + `dᵣ`)...) - m(i...)` equals sᵣ.

[*Note 3*: This implies that for a strided layout
m(i₀, …, iₖ) = m(0, …, 0) + i₀ × s₀ + … + iₖ × sₖ. — *end note*]

[*Note 4*: A mapping can return `false` even if the condition is met.
For certain layouts, it is possibly not feasible to determine
efficiently whether the layout is strided. — *end note*]

``` cpp
m.stride(r)
```

*Preconditions:* `m.is_strided()` is `true`.

*Result:* `typename M::index_type`

*Returns:* sᵣ as defined in `m.is_strided()` above.

``` cpp
M::is_always_unique()
```

*Result:* A constant expression [[expr.const]] of type `bool`.

*Returns:* `true` only if `m.is_unique()` is `true` for all possible
objects `m` of type `M`.

[*Note 5*: A mapping can return `false` even if the above condition is
met. For certain layout mappings, it is possibly not feasible to
determine whether every instance is unique. — *end note*]

``` cpp
M::is_always_exhaustive()
```

*Result:* A constant expression [[expr.const]] of type `bool`.

*Returns:* `true` only if `m.is_exhaustive()` is `true` for all possible
objects `m` of type `M`.

[*Note 6*: A mapping can return `false` even if the above condition is
met. For certain layout mappings, it is possibly not feasible to
determine whether every instance is exhaustive. — *end note*]

``` cpp
M::is_always_strided()
```

*Result:* A constant expression [[expr.const]] of type `bool`.

*Returns:* `true` only if `m.is_strided()` is `true` for all possible
objects `m` of type `M`.

[*Note 7*: A mapping can return `false` even if the above condition is
met. For certain layout mappings, it is possibly not feasible to
determine whether every instance is strided. — *end note*]

##### Layout mapping policy requirements <a id="mdspan.layout.policy.reqmts">[[mdspan.layout.policy.reqmts]]</a>

A type `MP` meets the *layout mapping policy* requirements if for a type
`E` that is a specialization of `extents`, `MP::mapping<E>` is valid and
denotes a type `X` that meets the layout mapping requirements
[[mdspan.layout.reqmts]], and for which the *qualified-id*
`X::layout_type` is valid and denotes the type `MP` and the
*qualified-id* `X::extents_type` denotes `E`.

##### Layout mapping policies <a id="mdspan.layout.policy.overview">[[mdspan.layout.policy.overview]]</a>

``` cpp
namespace std {
  struct layout_left {
    template<class Extents>
      class mapping;
  };
  struct layout_right {
    template<class Extents>
      class mapping;
  };
  struct layout_stride {
    template<class Extents>
      class mapping;
  };
}
```

Each of `layout_left`, `layout_right`, and `layout_stride` meets the
layout mapping policy requirements and is a trivial type.

##### Class template `layout_left::mapping` <a id="mdspan.layout.left">[[mdspan.layout.left]]</a>

###### Overview <a id="mdspan.layout.left.overview">[[mdspan.layout.left.overview]]</a>

`layout_left` provides a layout mapping where the leftmost extent has
stride 1, and strides increase left-to-right as the product of extents.

``` cpp
namespace std {
  template<class Extents>
  class layout_left::mapping {
  public:
    using extents_type = Extents;
    using index_type = typename extents_type::index_type;
    using size_type = typename extents_type::size_type;
    using rank_type = typename extents_type::rank_type;
    using layout_type = layout_left;

    // [mdspan.layout.left.cons], constructors
    constexpr mapping() noexcept = default;
    constexpr mapping(const mapping&) noexcept = default;
    constexpr mapping(const extents_type&) noexcept;
    template<class OtherExtents>
      constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
        mapping(const mapping<OtherExtents>&) noexcept;
    template<class OtherExtents>
      constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
        mapping(const layout_right::mapping<OtherExtents>&) noexcept;
    template<class OtherExtents>
      constexpr explicit(extents_type::rank() > 0)
        mapping(const layout_stride::mapping<OtherExtents>&);

    constexpr mapping& operator=(const mapping&) noexcept = default;

    // [mdspan.layout.left.obs], observers
    constexpr const extents_type& extents() const noexcept { return extents_; }

    constexpr index_type required_span_size() const noexcept;

    template<class... Indices>
      constexpr index_type operator()(Indices...) const noexcept;

    static constexpr bool is_always_unique() noexcept { return true; }
    static constexpr bool is_always_exhaustive() noexcept { return true; }
    static constexpr bool is_always_strided() noexcept { return true; }

    static constexpr bool is_unique() noexcept { return true; }
    static constexpr bool is_exhaustive() noexcept { return true; }
    static constexpr bool is_strided() noexcept { return true; }

    constexpr index_type stride(rank_type) const noexcept;

    template<class OtherExtents>
      friend constexpr bool operator==(const mapping&, const mapping<OtherExtents>&) noexcept;

  private:
    extents_type extents_{};    // exposition only
  };
}
```

If `Extents` is not a specialization of `extents`, then the program is
ill-formed.

`layout_left::mapping<E>` is a trivially copyable type that models
`regular` for each `E`.

*Mandates:* If `Extents::rank_dynamic() == 0` is `true`, then the size
of the multidimensional index space `Extents()` is representable as a
value of type `typename Extents::index_type`.

###### Constructors <a id="mdspan.layout.left.cons">[[mdspan.layout.left.cons]]</a>

``` cpp
constexpr mapping(const extents_type& e) noexcept;
```

*Preconditions:* The size of the multidimensional index space `e` is
representable as a value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with `e`.

``` cpp
template<class OtherExtents>
  constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
    mapping(const mapping<OtherExtents>& other) noexcept;
```

*Constraints:* `is_constructible_v<extents_type, OtherExtents>` is
`true`.

*Preconditions:* `other.required_span_size()` is representable as a
value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

``` cpp
template<class OtherExents>
  constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
    mapping(const layout_right::mapping<OtherExtents>& other) noexcept;
```

*Constraints:*

- `extents_type::rank() <= 1` is `true`, and
- `is_constructible_v<extents_type, OtherExtents>` is `true`.

*Preconditions:* `other.required_span_size()` is representable as a
value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

``` cpp
template<class OtherExtents>
  constexpr explicit(extents_type::rank() > 0)
    mapping(const layout_stride::mapping<OtherExtents>& other);
```

*Constraints:* `is_constructible_v<extents_type, OtherExtents>` is
`true`.

*Preconditions:*

- If `extents_type::rank() > 0` is `true`, then for all r in the range
  [0, `extents_type::rank()`), `other.stride(`r`)` equals
  `other.extents().`*`fwd-prod-of-extents`*`(`r`)`, and
- `other.required_span_size()` is representable as a value of type
  `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

###### Observers <a id="mdspan.layout.left.obs">[[mdspan.layout.left.obs]]</a>

``` cpp
constexpr index_type required_span_size() const noexcept;
```

*Returns:* `extents().`*`fwd-prod-of-extents`*`(extents_type::rank())`.

``` cpp
template<class... Indices>
  constexpr index_type operator()(Indices... i) const noexcept;
```

*Constraints:*

- `sizeof...(Indices) == extents_type::rank()` is `true`,
- `(is_convertible_v<Indices, index_type> && ...)` is `true`, and
- `(is_nothrow_constructible_v<index_type, Indices> && ...)` is `true`.

*Preconditions:* `extents_type::`*`index-cast`*`(i)` is a
multidimensional index in *extents\_*[[mdspan.overview]].

*Effects:* Let `P` be a parameter pack such that

``` cpp
is_same_v<index_sequence_for<Indices...>, index_sequence<P...>>
```

is `true`. Equivalent to:

``` cpp
return ((static_cast<index_type>(i) * stride(P)) + ... + 0);
```

``` cpp
constexpr index_type stride(rank_type i) const;
```

*Constraints:* `extents_type::rank() > 0` is `true`.

*Preconditions:* `i < extents_type::rank()` is `true`.

*Returns:* `extents().`*`fwd-prod-of-extents`*`(i)`.

``` cpp
template<class OtherExtents>
  friend constexpr bool operator==(const mapping& x, const mapping<OtherExtents>& y) noexcept;
```

*Constraints:* `extents_type::rank() == OtherExtents::rank()` is `true`.

*Effects:* Equivalent to: `return x.extents() == y.extents();`

##### Class template `layout_right::mapping` <a id="mdspan.layout.right">[[mdspan.layout.right]]</a>

###### Overview <a id="mdspan.layout.right.overview">[[mdspan.layout.right.overview]]</a>

`layout_right` provides a layout mapping where the rightmost extent is
stride 1, and strides increase right-to-left as the product of extents.

``` cpp
namespace std {
  template<class Extents>
  class layout_right::mapping {
  public:
    using extents_type = Extents;
    using index_type = typename extents_type::index_type;
    using size_type = typename extents_type::size_type;
    using rank_type = typename extents_type::rank_type;
    using layout_type = layout_right;

    // [mdspan.layout.right.cons], constructors
    constexpr mapping() noexcept = default;
    constexpr mapping(const mapping&) noexcept = default;
    constexpr mapping(const extents_type&) noexcept;
    template<class OtherExtents>
      constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
        mapping(const mapping<OtherExtents>&) noexcept;
    template<class OtherExtents>
      constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
        mapping(const layout_left::mapping<OtherExtents>&) noexcept;
    template<class OtherExtents>
      constexpr explicit(extents_type::rank() > 0)
        mapping(const layout_stride::mapping<OtherExtents>&) noexcept;

    constexpr mapping& operator=(const mapping&) noexcept = default;

    // [mdspan.layout.right.obs], observers
    constexpr const extents_type& extents() const noexcept { return extents_; }

    constexpr index_type required_span_size() const noexcept;

    template<class... Indices>
      constexpr index_type operator()(Indices...) const noexcept;

    static constexpr bool is_always_unique() noexcept { return true; }
    static constexpr bool is_always_exhaustive() noexcept { return true; }
    static constexpr bool is_always_strided() noexcept { return true; }

    static constexpr bool is_unique() noexcept { return true; }
    static constexpr bool is_exhaustive() noexcept { return true; }
    static constexpr bool is_strided() noexcept { return true; }

    constexpr index_type stride(rank_type) const noexcept;

    template<class OtherExtents>
      friend constexpr bool operator==(const mapping&, const mapping<OtherExtents>&) noexcept;

  private:
    extents_type extents_{};    // exposition only
  };
}
```

If `Extents` is not a specialization of `extents`, then the program is
ill-formed.

`layout_right::mapping<E>` is a trivially copyable type that models
`regular` for each `E`.

*Mandates:* If `Extents::rank_dynamic() == 0` is `true`, then the size
of the multidimensional index space `Extents()` is representable as a
value of type `typename Extents::index_type`.

###### Constructors <a id="mdspan.layout.right.cons">[[mdspan.layout.right.cons]]</a>

``` cpp
constexpr mapping(const extents_type& e) noexcept;
```

*Preconditions:* The size of the multidimensional index space `e` is
representable as a value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with `e`.

``` cpp
template<class OtherExtents>
  constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
    mapping(const mapping<OtherExtents>& other) noexcept;
```

*Constraints:* `is_constructible_v<extents_type, OtherExtents>` is
`true`.

*Preconditions:* `other.required_span_size()` is representable as a
value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

``` cpp
template<class OtherExtents>
  constexpr explicit(!is_convertible_v<OtherExtents, extents_type>)
    mapping(const layout_left::mapping<OtherExtents>& other) noexcept;
```

*Constraints:*

- `extents_type::rank() <= 1` is `true`, and
- `is_constructible_v<extents_type, OtherExtents>` is `true`.

*Preconditions:* `other.required_span_size()` is representable as a
value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

``` cpp
template<class OtherExtents>
 constexpr explicit(extents_type::rank() > 0)
    mapping(const layout_stride::mapping<OtherExtents>& other) noexcept;
```

*Constraints:* `is_constructible_v<extents_type, OtherExtents>` is
`true`.

*Preconditions:*

- If `extents_type::rank() > 0` is `true`, then for all r in the range
  [0, `extents_type::rank()`), `other.stride(`r`)` equals
  `other.extents().`*`rev-prod-of-extents`*`(`r`)`.
- `other.required_span_size()` is representable as a value of type
  `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`.

###### Observers <a id="mdspan.layout.right.obs">[[mdspan.layout.right.obs]]</a>

``` cpp
index_type required_span_size() const noexcept;
```

*Returns:* `extents().`*`fwd-prod-of-extents`*`(extents_type::rank())`.

``` cpp
template<class... Indices>
  constexpr index_type operator()(Indices... i) const noexcept;
```

*Constraints:*

- `sizeof...(Indices) == extents_type::rank()` is `true`,
- `(is_convertible_v<Indices, index_type> && ...)` is `true`, and
- `(is_nothrow_constructible_v<index_type, Indices> && ...)` is `true`.

*Preconditions:* `extents_type::`*`index-cast`*`(i)` is a
multidimensional index in *extents\_*[[mdspan.overview]].

*Effects:* Let `P` be a parameter pack such that

``` cpp
is_same_v<index_sequence_for<Indices...>, index_sequence<P...>>
```

is `true`. Equivalent to:

``` cpp
return ((static_cast<index_type>(i) * stride(P)) + ... + 0);
```

``` cpp
constexpr index_type stride(rank_type i) const noexcept;
```

*Constraints:* `extents_type::rank() > 0` is `true`.

*Preconditions:* `i < extents_type::rank()` is `true`.

*Returns:* `extents().`*`rev-prod-of-extents`*`(i)`.

``` cpp
template<class OtherExtents>
  friend constexpr bool operator==(const mapping& x, const mapping<OtherExtents>& y) noexcept;
```

*Constraints:* `extents_type::rank() == OtherExtents::rank()` is `true`.

*Effects:* Equivalent to: `return x.extents() == y.extents();`

##### Class template `layout_stride::mapping` <a id="mdspan.layout.stride">[[mdspan.layout.stride]]</a>

###### Overview <a id="mdspan.layout.stride.overview">[[mdspan.layout.stride.overview]]</a>

`layout_stride` provides a layout mapping where the strides are
user-defined.

``` cpp
namespace std {
  template<class Extents>
  class layout_stride::mapping {
  public:
    using extents_type = Extents;
    using index_type = typename extents_type::index_type;
    using size_type = typename extents_type::size_type;
    using rank_type = typename extents_type::rank_type;
    using layout_type = layout_stride;

  private:
    static constexpr rank_type rank_ = extents_type::rank();    // exposition only

  public:
    // [mdspan.layout.stride.cons], constructors
    constexpr mapping() noexcept;
    constexpr mapping(const mapping&) noexcept = default;
    template<class OtherIndexType>
      constexpr mapping(const extents_type&, span<OtherIndexType, rank_>) noexcept;
    template<class OtherIndexType>
      constexpr mapping(const extents_type&, const array<OtherIndexType, rank_>&) noexcept;

    template<class StridedLayoutMapping>
      constexpr explicit(see below) mapping(const StridedLayoutMapping&) noexcept;

    constexpr mapping& operator=(const mapping&) noexcept = default;

    // [mdspan.layout.stride.obs], observers
    constexpr const extents_type& extents() const noexcept { return extents_; }
    constexpr array<index_type, rank_> strides() const noexcept { return strides_; }

    constexpr index_type required_span_size() const noexcept;

    template<class... Indices>
      constexpr index_type operator()(Indices...) const noexcept;

    static constexpr bool is_always_unique() noexcept { return true; }
    static constexpr bool is_always_exhaustive() noexcept { return false; }
    static constexpr bool is_always_strided() noexcept { return true; }

    static constexpr bool is_unique() noexcept { return true; }
    constexpr bool is_exhaustive() const noexcept;
    static constexpr bool is_strided() noexcept { return true; }

    constexpr index_type stride(rank_type i) const noexcept { return strides_[i]; }

    template<class OtherMapping>
      friend constexpr bool operator==(const mapping&, const OtherMapping&) noexcept;

  private:
    extents_type extents_{};                    // exposition only
    array<index_type, rank_> strides_{};        // exposition only
  };
}
```

If `Extents` is not a specialization of `extents`, then the program is
ill-formed.

`layout_stride::mapping<E>` is a trivially copyable type that models
`regular` for each `E`.

*Mandates:* If `Extents::rank_dynamic() == 0` is `true`, then the size
of the multidimensional index space `Extents()` is representable as a
value of type `typename Extents::index_type`.

###### Exposition-only helpers <a id="mdspan.layout.stride.expo">[[mdspan.layout.stride.expo]]</a>

Let `REQUIRED-SPAN-SIZE(e, strides)` be:

- `1`, if `e.rank() == 0` is `true`,
- otherwise `0`, if the size of the multidimensional index space `e` is
  0,
- otherwise `1` plus the sum of products of `(e.extent(r) - 1)` and
  `strides[r]` for all r in the range [0, `e.rank()`).

Let `OFFSET(m)` be:

- `m()`, if `e.rank() == 0` is `true`,
- otherwise `0`, if the size of the multidimensional index space `e` is
  0,
- otherwise `m(z...)` for a pack of integers `z` that is a
  multidimensional index in `m.extents()` and each element of `z` equals
  0.

Let *is-extents* be the exposition-only variable template defined as
follows:

``` cpp
template<class T>
  constexpr bool is-extents = false;                              // exposition only
template<class IndexType, size_t... Args>
  constexpr bool is-extents<extents<IndexType, Args...>> = true;  // exposition only
```

Let `layout-mapping-alike` be the exposition-only concept defined as
follows:

``` cpp
template<class M>
concept layout-mapping-alike = requires {                         // exposition only
  requires is-extents<typename M::extents_type>;
  { M::is_always_strided() } -> same_as<bool>;
  { M::is_always_exhaustive() } -> same_as<bool>;
  { M::is_always_unique() } -> same_as<bool>;
  bool_constant<M::is_always_strided()>::value;
  bool_constant<M::is_always_exhaustive()>::value;
  bool_constant<M::is_always_unique()>::value;
};
```

[*Note 1*: This concept checks that the functions
`M::is_always_strided()`, `M::is_always_exhaustive()`, and
`M::is_always_unique()` exist, are constant expressions, and have a
return type of `bool`. — *end note*]

###### Constructors <a id="mdspan.layout.stride.cons">[[mdspan.layout.stride.cons]]</a>

``` cpp
constexpr mapping() noexcept;
```

*Preconditions:*
`layout_right::mapping<extents_type>().required_span_size()` is
representable as a value of type `index_type`[[basic.fundamental]].

*Effects:* Direct-non-list-initializes *extents\_* with
`extents_type()`, and for all d in the range \[`0`, *`rank_`*),
direct-non-list-initializes *`strides_`*`[`d`]` with
`layout_right::mapping<extents_type>().stride(`d`)`.

``` cpp
template<class OtherIndexType>
  constexpr mapping(const extents_type& e, span<OtherIndexType, rank_> s) noexcept;
template<class OtherIndexType>
  constexpr mapping(const extents_type& e, const array<OtherIndexType, rank_>& s) noexcept;
```

*Constraints:*

- `is_convertible_v<const OtherIndexType&, index_type>` is `true`, and
- `is_nothrow_constructible_v<index_type, const OtherIndexType&>` is
  `true`.

*Preconditions:*

- `s[`i`] > 0` is `true` for all i in the range [0, rank_).
- *`REQUIRED-SPAN-SIZE`*`(e, s)` is representable as a value of type
  `index_type`[[basic.fundamental]].
- If *rank\_* is greater than 0, then there exists a permutation P of
  the integers in the range [0, rank_), such that
  `s[`pᵢ`] >= s[`pᵢ₋₁`] * e.extent(p`$_{i-1}$`)` is `true` for all i in
  the range [1, rank_), where pᵢ is the iᵗʰ element of P.
  \[*Note 10*: For `layout_stride`, this condition is necessary and
  sufficient for `is_unique()` to be `true`. — *end note*]

*Effects:* Direct-non-list-initializes *extents\_* with `e`, and for all
d in the range [0, rank_), direct-non-list-initializes `strides_[`d`]`
with `as_const(s[`d`])`.

``` cpp
template<class StridedLayoutMapping>
  constexpr explicit(see below)
    mapping(const StridedLayoutMapping& other) noexcept;
```

*Constraints:*

- `layout-mapping-alike<StridedLayoutMapping>` is satisfied.
- `is_constructible_v<extents_type, typename StridedLayoutMapping::extents_type>`
  is  
  `true`.
- `StridedLayoutMapping::is_always_unique()` is `true`.
- `StridedLayoutMapping::is_always_strided()` is `true`.

*Preconditions:*

- `StridedLayoutMapping` meets the layout mapping
  requirements [[mdspan.layout.policy.reqmts]],
- `other.stride(`r`) > 0` is `true` for every rank index r of
  `extents()`,
- `other.required_span_size()` is representable as a value of type
  `index_type`[[basic.fundamental]], and
- *`OFFSET`*`(other) == 0` is `true`.

*Effects:* Direct-non-list-initializes *extents\_* with
`other.extents()`, and for all d in the range [0, rank_),
direct-non-list-initializes *`strides_`*`[`d`]` with
`other.stride(`d`)`.

Remarks: The expression inside `explicit` is equivalent to:

``` cpp
!(is_convertible_v<typename StridedLayoutMapping::extents_type, extents_type> &&
  (is-mapping-of<layout_left, LayoutStrideMapping> ||
   is-mapping-of<layout_right, LayoutStrideMapping> ||
   is-mapping-of<layout_stride, LayoutStrideMapping>))
```

###### Observers <a id="mdspan.layout.stride.obs">[[mdspan.layout.stride.obs]]</a>

``` cpp
constexpr index_type required_span_size() const noexcept;
```

*Returns:* *`REQUIRED-SPAN-SIZE`*`(extents(), `*`strides_`*`)`.

``` cpp
template<class... Indices>
  constexpr index_type operator()(Indices... i) const noexcept;
```

*Constraints:*

- `sizeof...(Indices) == `*`rank_`* is `true`,
- `(is_convertible_v<Indices, index_type> && ...)` is `true`, and
- `(is_nothrow_constructible_v<index_type, Indices> && ...)` is `true`.

*Preconditions:* `extents_type::`*`index-cast`*`(i)` is a
multidimensional index in *extents\_*[[mdspan.overview]].

*Effects:* Let `P` be a parameter pack such that

``` cpp
is_same_v<index_sequence_for<Indices...>, index_sequence<P...>>
```

is `true`. Equivalent to:

``` cpp
return ((static_cast<index_type>(i) * stride(P)) + ... + 0);
```

``` cpp
constexpr bool is_exhaustive() const noexcept;
```

*Returns:*

- `true` if *rank\_* is 0.
- Otherwise, `true` if there is a permutation P of the integers in the
  range [0, rank_) such that `stride(`p₀`)` equals 1, and `stride(`pᵢ`)`
  equals `stride(`pᵢ₋₁`) * extents().extent(`pᵢ₋₁`)` for i in the range
  [1, rank_), where pᵢ is the iᵗʰ element of P.
- Otherwise, `false`.

``` cpp
template<class OtherMapping>
  friend constexpr bool operator==(const mapping& x, const OtherMapping& y) noexcept;
```

*Constraints:*

- `layout-mapping-alike<OtherMapping>` is satisfied.
- *`rank_`*` == OtherMapping::extents_type::rank()` is `true`.
- `OtherMapping::is_always_strided()` is `true`.

*Preconditions:* `OtherMapping` meets the layout mapping
requirements [[mdspan.layout.policy.reqmts]].

*Returns:* `true` if `x.extents() == y.extents()` is `true`,
*`OFFSET`*`(y) == 0` is `true`, and each of
`x.stride(`r`) == y.stride(`r`)` is `true` for r in the range
[0, `x.extents().rank()`). Otherwise, `false`.

#### Accessor policy <a id="mdspan.accessor">[[mdspan.accessor]]</a>

##### General <a id="mdspan.accessor.general">[[mdspan.accessor.general]]</a>

An *accessor policy* defines types and operations by which a reference
to a single object is created from an abstract data handle to a number
of such objects and an index.

A range of indices [0, N) is an *accessible range* of a given data
handle and an accessor if, for each i in the range, the accessor
policy’s `access` function produces a valid reference to an object.

In subclause [[mdspan.accessor.reqmts]],

- `A` denotes an accessor policy.
- `a` denotes a value of type `A` or `const A`.
- `p` denotes a value of type `A::data_handle_type` or
  `const A::data_handle_type`. \[*Note 11*: The type
  `A::data_handle_type` need not be dereferenceable. — *end note*]
- `n`, `i`, and `j` each denote values of type `size_t`.

##### Requirements <a id="mdspan.accessor.reqmts">[[mdspan.accessor.reqmts]]</a>

A type `A` meets the accessor policy requirements if

- `A` models `copyable`,
- `is_nothrow_move_constructible_v<A>` is `true`,
- `is_nothrow_move_assignable_v<A>` is `true`,
- `is_nothrow_swappable_v<A>` is `true`, and
- the following types and expressions are well-formed and have the
  specified semantics.

``` cpp
typename A::element_type
```

*Result:* A complete object type that is not an abstract class type.

``` cpp
typename A::data_handle_type
```

*Result:* A type that models `copyable`, and for which
`is_nothrow_move_constructible_v<A::data_handle_type>` is `true`,
`is_nothrow_move_assignable_v<A::data_handle_type>` is `true`, and
`is_nothrow_swappable_v<A::data_handle_type>` is `true`.

[*Note 1*: The type of `data_handle_type` need not be
`element_type*`. — *end note*]

``` cpp
typename A::reference
```

*Result:* A type that models
`common_reference_with<A::reference&&, A::element_type&>`.

[*Note 2*: The type of `reference` need not be
`element_type&`. — *end note*]

``` cpp
typename A::offset_policy
```

*Result:* A type `OP` such that:

- `OP` meets the accessor policy requirements,
- `constructible_from<OP, const A&>` is modeled, and
- `is_same_v<typename OP::element_type, typename A::element_type>` is
  `true`.

``` cpp
a.access(p, i)
```

*Result:* `A::reference`

*Remarks:* The expression is equality preserving.

[*Note 3*: Concrete accessor policies can impose preconditions for
their `access` function. However, they might not. For example, an
accessor where `p` is `span<A::element_type, dynamic_extent>` and
`access(p, i)` returns `p[i % p.size()]` does not need to impose a
precondition on `i`. — *end note*]

``` cpp
a.offset(p, i)
```

*Result:* `A::offset_policy::data_handle_type`

*Returns:* `q` such that for `b` being `A::offset_policy(a)`, and any
integer `n` for which [0, `n`) is an accessible range of `p` and `a`:

- [0, `n` - `i`) is an accessible range of `q` and `b`; and
- `b.access(q, j)` provides access to the same element as
  `a.access(p, i + j)`, for every `j` in the range [0, `n` - `i`).

*Remarks:* The expression is equality-preserving.

##### Class template `default_accessor` <a id="mdspan.accessor.default">[[mdspan.accessor.default]]</a>

###### Overview <a id="mdspan.accessor.default.overview">[[mdspan.accessor.default.overview]]</a>

``` cpp
namespace std {
  template<class ElementType>
  struct default_accessor {
    using offset_policy = default_accessor;
    using element_type = ElementType;
    using reference = ElementType&;
    using data_handle_type = ElementType*;

    constexpr default_accessor() noexcept = default;
    template<class OtherElementType>
      constexpr default_accessor(default_accessor<OtherElementType>) noexcept;
    constexpr reference access(data_handle_type p, size_t i) const noexcept;
    constexpr data_handle_type offset(data_handle_type p, size_t i) const noexcept;
  };
}
```

`default_accessor` meets the accessor policy requirements.

`ElementType` is required to be a complete object type that is neither
an abstract class type nor an array type.

Each specialization of `default_accessor` is a trivially copyable type
that models `semiregular`.

[0, n) is an accessible range for an object `p` of type
`data_handle_type` and an object of type `default_accessor` if and only
if \[`p`, `p + `n) is a valid range.

###### Members <a id="mdspan.accessor.default.members">[[mdspan.accessor.default.members]]</a>

``` cpp
template<class OtherElementType>
  constexpr default_accessor(default_accessor<OtherElementType>) noexcept {}
```

*Constraints:*
`is_convertible_v<OtherElementType(*)[], element_type(*)[]>` is `true`.

``` cpp
constexpr reference access(data_handle_type p, size_t i) const noexcept;
```

*Effects:* Equivalent to: `return p[i];`

``` cpp
constexpr data_handle_type offset(data_handle_type p, size_t i) const noexcept;
```

*Effects:* Equivalent to: `return p + i;`

#### Class template `mdspan` <a id="mdspan.mdspan">[[mdspan.mdspan]]</a>

##### Overview <a id="mdspan.mdspan.overview">[[mdspan.mdspan.overview]]</a>

`mdspan` is a view of a multidimensional array of elements.

``` cpp
namespace std {
  template<class ElementType, class Extents, class LayoutPolicy = layout_right,
           class AccessorPolicy = default_accessor<ElementType>>
  class mdspan {
  public:
    using extents_type = Extents;
    using layout_type = LayoutPolicy;
    using accessor_type = AccessorPolicy;
    using mapping_type = typename layout_type::template mapping<extents_type>;
    using element_type = ElementType;
    using value_type = remove_cv_t<element_type>;
    using index_type = typename extents_type::index_type;
    using size_type = typename extents_type::size_type;
    using rank_type = typename extents_type::rank_type;
    using data_handle_type = typename accessor_type::data_handle_type;
    using reference = typename accessor_type::reference;

    static constexpr rank_type rank() noexcept { return extents_type::rank(); }
    static constexpr rank_type rank_dynamic() noexcept { return extents_type::rank_dynamic(); }
    static constexpr size_t static_extent(rank_type r) noexcept
      { return extents_type::static_extent(r); }
    constexpr index_type extent(rank_type r) const noexcept { return extents().extent(r); }

    // [mdspan.mdspan.cons], constructors
    constexpr mdspan();
    constexpr mdspan(const mdspan& rhs) = default;
    constexpr mdspan(mdspan&& rhs) = default;

    template<class... OtherIndexTypes>
      constexpr explicit mdspan(data_handle_type ptr, OtherIndexTypes... exts);
    template<class OtherIndexType, size_t N>
      constexpr explicit(N != rank_dynamic())
        mdspan(data_handle_type p, span<OtherIndexType, N> exts);
    template<class OtherIndexType, size_t N>
      constexpr explicit(N != rank_dynamic())
        mdspan(data_handle_type p, const array<OtherIndexType, N>& exts);
    constexpr mdspan(data_handle_type p, const extents_type& ext);
    constexpr mdspan(data_handle_type p, const mapping_type& m);
    constexpr mdspan(data_handle_type p, const mapping_type& m, const accessor_type& a);

    template<class OtherElementType, class OtherExtents,
             class OtherLayoutPolicy, class OtherAccessorPolicy>
      constexpr explicit(see below)
        mdspan(const mdspan<OtherElementType, OtherExtents,
                            OtherLayoutPolicy, OtherAccessorPolicy>& other);

    constexpr mdspan& operator=(const mdspan& rhs) = default;
    constexpr mdspan& operator=(mdspan&& rhs) = default;

    // [mdspan.mdspan.members], members
    template<class... OtherIndexTypes>
      constexpr reference operator[](OtherIndexTypes... indices) const;
    template<class OtherIndexType>
      constexpr reference operator[](span<OtherIndexType, rank()> indices) const;
    template<class OtherIndexType>
      constexpr reference operator[](const array<OtherIndexType, rank()>& indices) const;

    constexpr size_type size() const noexcept;
    [[nodiscard]] constexpr bool empty() const noexcept;

    friend constexpr void swap(mdspan& x, mdspan& y) noexcept;

    constexpr const extents_type& extents() const noexcept { return map_.extents(); }
    constexpr const data_handle_type& data_handle() const noexcept { return ptr_; }
    constexpr const mapping_type& mapping() const noexcept { return map_; }
    constexpr const accessor_type& accessor() const noexcept { return acc_; }

    static constexpr bool is_always_unique()
      { return mapping_type::is_always_unique(); }
    static constexpr bool is_always_exhaustive()
      { return mapping_type::is_always_exhaustive(); }
    static constexpr bool is_always_strided()
      { return mapping_type::is_always_strided(); }

    constexpr bool is_unique() const
      { return map_.is_unique(); }
    constexpr bool is_exhaustive() const
      { return map_.is_exhaustive(); }
    constexpr bool is_strided() const
      { return map_.is_strided(); }
    constexpr index_type stride(rank_type r) const
      { return map_.stride(r); }

  private:
    accessor_type acc_;         // exposition only
    mapping_type map_;          // exposition only
    data_handle_type ptr_;      // exposition only
  };

  template<class CArray>
    requires(is_array_v<CArray> && rank_v<CArray> == 1)
    mdspan(CArray&)
      -> mdspan<remove_all_extents_t<CArray>, extents<size_t, extent_v<CArray, 0>>>;

  template<class Pointer>
    requires(is_pointer_v<remove_reference_t<Pointer>>)
    mdspan(Pointer&&)
      -> mdspan<remove_pointer_t<remove_reference_t<Pointer>>, extents<size_t>>;

  template<class ElementType, class... Integrals>
    requires((is_convertible_v<Integrals, size_t> && ...) && sizeof...(Integrals) > 0)
    explicit mdspan(ElementType*, Integrals...)
      -> mdspan<ElementType, dextents<size_t, sizeof...(Integrals)>>;

  template<class ElementType, class OtherIndexType, size_t N>
    mdspan(ElementType*, span<OtherIndexType, N>)
      -> mdspan<ElementType, dextents<size_t, N>>;

  template<class ElementType, class OtherIndexType, size_t N>
    mdspan(ElementType*, const array<OtherIndexType, N>&)
      -> mdspan<ElementType, dextents<size_t, N>>;

  template<class ElementType, class IndexType, size_t... ExtentsPack>
    mdspan(ElementType*, const extents<IndexType, ExtentsPack...>&)
      -> mdspan<ElementType, extents<IndexType, ExtentsPack...>>;

  template<class ElementType, class MappingType>
    mdspan(ElementType*, const MappingType&)
      -> mdspan<ElementType, typename MappingType::extents_type,
                typename MappingType::layout_type>;

  template<class MappingType, class AccessorType>
    mdspan(const typename AccessorType::data_handle_type&, const MappingType&,
           const AccessorType&)
      -> mdspan<typename AccessorType::element_type, typename MappingType::extents_type,
                typename MappingType::layout_type, AccessorType>;
}
```

*Mandates:*

- `ElementType` is a complete object type that is neither an abstract
  class type nor an array type,
- `Extents` is a specialization of `extents`, and
- `is_same_v<ElementType, typename AccessorPolicy::element_type>` is
  `true`.

`LayoutPolicy` shall meet the layout mapping policy requirements
[[mdspan.layout.policy.reqmts]], and `AccessorPolicy` shall meet the
accessor policy requirements [[mdspan.accessor.reqmts]].

Each specialization `MDS` of `mdspan` models `copyable` and

- `is_nothrow_move_constructible_v<MDS>` is `true`,
- `is_nothrow_move_assignable_v<MDS>` is `true`, and
- `is_nothrow_swappable_v<MDS>` is `true`.

A specialization of `mdspan` is a trivially copyable type if its
`accessor_type`, `mapping_type`, and `data_handle_type` are trivially
copyable types.

##### Constructors <a id="mdspan.mdspan.cons">[[mdspan.mdspan.cons]]</a>

``` cpp
constexpr mdspan();
```

*Constraints:*

- `rank_dynamic() > 0` is `true`.
- `is_default_constructible_v<data_handle_type>` is `true`.
- `is_default_constructible_v<mapping_type>` is `true`.
- `is_default_constructible_v<accessor_type>` is `true`.

*Preconditions:* $[0, \texttt{\textit{map_}.required_span_size()})$ is
an accessible range of *ptr\_* and *acc\_* for the values of *map\_* and
*acc\_* after the invocation of this constructor.

*Effects:* Value-initializes *ptr\_*, *map\_*, and *acc\_*.

``` cpp
template<class... OtherIndexTypes>
  constexpr explicit mdspan(data_handle_type p, OtherIndexTypes... exts);
```

Let `N` be `sizeof...(OtherIndexTypes)`.

*Constraints:*

- `(is_convertible_v<OtherIndexTypes, index_type> && ...)` is `true`,
- `(is_nothrow_constructible<index_type, OtherIndexTypes> && ...)` is
  `true`,
- `N == rank() || N == rank_dynamic()` is `true`,
- `is_constructible_v<mapping_type, extents_type>` is `true`, and
- `is_default_constructible_v<accessor_type>` is `true`.

*Preconditions:* $[0, \texttt{\textit{map_}.required_span_size()})$ is
an accessible range of `p` and *acc\_* for the values of *map\_* and
*acc\_* after the invocation of this constructor.

*Effects:*

- Direct-non-list-initializes *ptr\_* with `std::move(p)`,
- direct-non-list-initializes *map\_* with
  `extents_type(static_cast<index_type>(std::move(exts))...)`, and
- value-initializes *acc\_*.

``` cpp
template<class OtherIndexType, size_t N>
  constexpr explicit(N != rank_dynamic())
    mdspan(data_handle_type p, span<OtherIndexType, N> exts);
template<class OtherIndexType, size_t N>
  constexpr explicit(N != rank_dynamic())
    mdspan(data_handle_type p, const array<OtherIndexType, N>& exts);
```

*Constraints:*

- `is_convertible_v<const OtherIndexType&, index_type>` is `true`,
- `(is_nothrow_constructible<index_type, const OtherIndexType&> && ...)`
  is `true`,
- `N == rank() || N == rank_dynamic()` is `true`,
- `is_constructible_v<mapping_type, extents_type>` is `true`, and
- `is_default_constructible_v<accessor_type>` is `true`.

*Preconditions:* $[0, \texttt{\textit{map_}.required_span_size()})$ is
an accessible range of `p` and *acc\_* for the values of *map\_* and
*acc\_* after the invocation of this constructor.

*Effects:*

- Direct-non-list-initializes *ptr\_* with `std::move(p)`,
- direct-non-list-initializes *map\_* with `extents_type(exts)`, and
- value-initializes *acc\_*.

``` cpp
constexpr mdspan(data_handle_type p, const extents_type& ext);
```

*Constraints:*

- `is_constructible_v<mapping_type, const extents_type&>` is `true`, and
- `is_default_constructible_v<accessor_type>` is `true`.

*Preconditions:* $[0, \texttt{\textit{map_}.required_span_size()})$ is
an accessible range of `p` and *acc\_* for the values of *map\_* and
*acc\_* after the invocation of this constructor.

*Effects:*

- Direct-non-list-initializes *ptr\_* with `std::move(p)`,
- direct-non-list-initializes *map\_* with `ext`, and
- value-initializes *acc\_*.

``` cpp
constexpr mdspan(data_handle_type p, const mapping_type& m);
```

*Constraints:* `is_default_constructible_v<accessor_type>` is `true`.

*Preconditions:* [0, `m.required_span_size()`) is an accessible range of
`p` and *acc\_* for the value of *acc\_* after the invocation of this
constructor.

*Effects:*

- Direct-non-list-initializes *ptr\_* with `std::move(p)`,
- direct-non-list-initializes *map\_* with `m`, and
- value-initializes *acc\_*.

``` cpp
constexpr mdspan(data_handle_type p, const mapping_type& m, const accessor_type& a);
```

*Preconditions:* [0, `m.required_span_size()`) is an accessible range of
`p` and `a`.

*Effects:*

- Direct-non-list-initializes *ptr\_* with `std::move(p)`,
- direct-non-list-initializes *map\_* with `m`, and
- direct-non-list-initializes *acc\_* with `a`.

``` cpp
template<class OtherElementType, class OtherExtents,
         class OtherLayoutPolicy, class OtherAccessor>
  constexpr explicit(see below)
    mdspan(const mdspan<OtherElementType, OtherExtents,
                        OtherLayoutPolicy, OtherAccessor>& other);
```

*Constraints:*

- `is_constructible_v<mapping_type, const OtherLayoutPolicy::template mapping<Oth-``erExtents>&>`
  is `true`, and
- `is_constructible_v<accessor_type, const OtherAccessor&>` is `true`.

*Mandates:*

- `is_constructible_v<data_handle_type, const OtherAccessor::data_handle_type&>`
  is`true`, and
- `is_constructible_v<extents_type, OtherExtents>` is `true`.

*Preconditions:*

- For each rank index `r` of `extents_type`,
  `static_extent(r) == dynamic_extent || static_extent(r) == other.extent(r)`
  is `true`.
- $[0, \texttt{\textit{map_}.required_span_size()})$ is an accessible
  range of *ptr\_* and *acc\_* for values of *ptr\_*, *map\_*, and
  *acc\_* after the invocation of this constructor.

*Effects:*

- Direct-non-list-initializes *ptr\_* with `other.`*`ptr_`*,
- direct-non-list-initializes *map\_* with `other.`*`map_`*, and
- direct-non-list-initializes *acc\_* with `other.`*`acc_`*.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<const OtherLayoutPolicy::template mapping<OtherExtents>&, mapping_type>
|| !is_convertible_v<const OtherAccessor&, accessor_type>
```

##### Members <a id="mdspan.mdspan.members">[[mdspan.mdspan.members]]</a>

``` cpp
template<class... OtherIndexTypes>
  constexpr reference operator[](OtherIndexTypes... indices) const;
```

*Constraints:*

- `(is_convertible_v<OtherIndexTypes, index_type> && ...)` is `true`,
- `(is_nothrow_constructible_v<index_type, OtherIndexTypes> && ...)` is
  `true`, and
- `sizeof...(OtherIndexTypes) == rank()` is `true`.

Let `I` be `extents_type::`*`index-cast`*`(std::move(indices))`.

*Preconditions:* `I` is a multidimensional index in `extents()`.

[*Note 1*: This implies that
*`map_`*`(I) < `*`map_`*`.required_span_size()` is
`true`. — *end note*]

*Effects:* Equivalent to:

``` cpp
return acc_.access(ptr_, map_(static_cast<index_type>(std::move(indices))...));
```

``` cpp
template<class OtherIndexType>
  constexpr reference operator[](span<OtherIndexType, rank()> indices) const;
template<class OtherIndexType>
  constexpr reference operator[](const array<OtherIndexType, rank()>& indices) const;
```

*Constraints:*

- `is_convertible_v<const OtherIndexType&, index_type>` is `true`, and
- `is_nothrow_constructible_v<index_type, const OtherIndexType&>` is
  `true`.

*Effects:* Let `P` be a parameter pack such that

``` cpp
is_same_v<make_index_sequence<rank()>, index_sequence<P...>>
```

is `true`. Equivalent to:

``` cpp
return operator[](as_const(indices[P])...);
```

``` cpp
constexpr size_type size() const noexcept;
```

*Preconditions:* The size of the multidimensional index space
`extents()` is representable as a value of type
`size_type`[[basic.fundamental]].

*Returns:* `extents().`*`fwd-prod-of-extents`*`(rank())`.

``` cpp
[[nodiscard]] constexpr bool empty() const noexcept;
```

*Returns:* `true` if the size of the multidimensional index space
`extents()` is 0, otherwise `false`.

``` cpp
friend constexpr void swap(mdspan& x, mdspan& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
swap(x.ptr_, y.ptr_);
swap(x.map_, y.map_);
swap(x.acc_, y.acc_);
```

<!-- Link reference definitions -->
[alg.equal]: algorithms.md#alg.equal
[alg.sorting]: algorithms.md#alg.sorting
[algorithm.stable]: library.md#algorithm.stable
[algorithms]: algorithms.md#algorithms
[algorithms.requirements]: algorithms.md#algorithms.requirements
[allocator.requirements]: library.md#allocator.requirements
[allocator.requirements.completeness]: library.md#allocator.requirements.completeness
[allocator.traits.members]: mem.md#allocator.traits.members
[allocator.uses.construction]: mem.md#allocator.uses.construction
[array]: #array
[array.cons]: #array.cons
[array.creation]: #array.creation
[array.members]: #array.members
[array.overview]: #array.overview
[array.special]: #array.special
[array.syn]: #array.syn
[array.tuple]: #array.tuple
[array.zero]: #array.zero
[associative]: #associative
[associative.general]: #associative.general
[associative.map.syn]: #associative.map.syn
[associative.reqmts]: #associative.reqmts
[associative.reqmts.except]: #associative.reqmts.except
[associative.reqmts.general]: #associative.reqmts.general
[associative.set.syn]: #associative.set.syn
[basic.fundamental]: basic.md#basic.fundamental
[basic.string]: strings.md#basic.string
[class.copy.ctor]: class.md#class.copy.ctor
[class.default.ctor]: class.md#class.default.ctor
[class.dtor]: class.md#class.dtor
[container.adaptors]: #container.adaptors
[container.adaptors.format]: #container.adaptors.format
[container.adaptors.general]: #container.adaptors.general
[container.alloc.reqmts]: #container.alloc.reqmts
[container.gen.reqmts]: #container.gen.reqmts
[container.insert.return]: #container.insert.return
[container.node]: #container.node
[container.node.compat]: #container.node.compat
[container.node.cons]: #container.node.cons
[container.node.dtor]: #container.node.dtor
[container.node.modifiers]: #container.node.modifiers
[container.node.observers]: #container.node.observers
[container.node.overview]: #container.node.overview
[container.opt.reqmts]: #container.opt.reqmts
[container.reqmts]: #container.reqmts
[container.requirements]: #container.requirements
[container.requirements.dataraces]: #container.requirements.dataraces
[container.requirements.general]: #container.requirements.general
[container.requirements.pre]: #container.requirements.pre
[container.rev.reqmts]: #container.rev.reqmts
[containers]: #containers
[containers.general]: #containers.general
[containers.summary]: #containers.summary
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[defns.valid]: intro.md#defns.valid
[deque]: #deque
[deque.capacity]: #deque.capacity
[deque.cons]: #deque.cons
[deque.erasure]: #deque.erasure
[deque.modifiers]: #deque.modifiers
[deque.overview]: #deque.overview
[deque.syn]: #deque.syn
[expr.const]: expr.md#expr.const
[flat.map]: #flat.map
[flat.map.access]: #flat.map.access
[flat.map.capacity]: #flat.map.capacity
[flat.map.cons]: #flat.map.cons
[flat.map.defn]: #flat.map.defn
[flat.map.erasure]: #flat.map.erasure
[flat.map.modifiers]: #flat.map.modifiers
[flat.map.overview]: #flat.map.overview
[flat.map.syn]: #flat.map.syn
[flat.multimap]: #flat.multimap
[flat.multimap.cons]: #flat.multimap.cons
[flat.multimap.defn]: #flat.multimap.defn
[flat.multimap.erasure]: #flat.multimap.erasure
[flat.multimap.overview]: #flat.multimap.overview
[flat.multiset]: #flat.multiset
[flat.multiset.cons]: #flat.multiset.cons
[flat.multiset.defn]: #flat.multiset.defn
[flat.multiset.erasure]: #flat.multiset.erasure
[flat.multiset.modifiers]: #flat.multiset.modifiers
[flat.multiset.overview]: #flat.multiset.overview
[flat.set]: #flat.set
[flat.set.cons]: #flat.set.cons
[flat.set.defn]: #flat.set.defn
[flat.set.erasure]: #flat.set.erasure
[flat.set.modifiers]: #flat.set.modifiers
[flat.set.overview]: #flat.set.overview
[flat.set.syn]: #flat.set.syn
[forward.iterators]: iterators.md#forward.iterators
[forward.list]: #forward.list
[forward.list.access]: #forward.list.access
[forward.list.cons]: #forward.list.cons
[forward.list.erasure]: #forward.list.erasure
[forward.list.iter]: #forward.list.iter
[forward.list.modifiers]: #forward.list.modifiers
[forward.list.ops]: #forward.list.ops
[forward.list.overview]: #forward.list.overview
[forward.list.syn]: #forward.list.syn
[hash.requirements]: library.md#hash.requirements
[iterator.concept.contiguous]: iterators.md#iterator.concept.contiguous
[iterator.concept.random.access]: iterators.md#iterator.concept.random.access
[iterator.requirements]: iterators.md#iterator.requirements
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[list]: #list
[list.capacity]: #list.capacity
[list.cons]: #list.cons
[list.erasure]: #list.erasure
[list.modifiers]: #list.modifiers
[list.ops]: #list.ops
[list.overview]: #list.overview
[list.syn]: #list.syn
[map]: #map
[map.access]: #map.access
[map.cons]: #map.cons
[map.erasure]: #map.erasure
[map.modifiers]: #map.modifiers
[map.overview]: #map.overview
[mdspan.accessor]: #mdspan.accessor
[mdspan.accessor.default]: #mdspan.accessor.default
[mdspan.accessor.default.members]: #mdspan.accessor.default.members
[mdspan.accessor.default.overview]: #mdspan.accessor.default.overview
[mdspan.accessor.general]: #mdspan.accessor.general
[mdspan.accessor.reqmts]: #mdspan.accessor.reqmts
[mdspan.extents]: #mdspan.extents
[mdspan.extents.cmp]: #mdspan.extents.cmp
[mdspan.extents.cons]: #mdspan.extents.cons
[mdspan.extents.dextents]: #mdspan.extents.dextents
[mdspan.extents.expo]: #mdspan.extents.expo
[mdspan.extents.obs]: #mdspan.extents.obs
[mdspan.extents.overview]: #mdspan.extents.overview
[mdspan.layout]: #mdspan.layout
[mdspan.layout.general]: #mdspan.layout.general
[mdspan.layout.left]: #mdspan.layout.left
[mdspan.layout.left.cons]: #mdspan.layout.left.cons
[mdspan.layout.left.obs]: #mdspan.layout.left.obs
[mdspan.layout.left.overview]: #mdspan.layout.left.overview
[mdspan.layout.policy.overview]: #mdspan.layout.policy.overview
[mdspan.layout.policy.reqmts]: #mdspan.layout.policy.reqmts
[mdspan.layout.reqmts]: #mdspan.layout.reqmts
[mdspan.layout.right]: #mdspan.layout.right
[mdspan.layout.right.cons]: #mdspan.layout.right.cons
[mdspan.layout.right.obs]: #mdspan.layout.right.obs
[mdspan.layout.right.overview]: #mdspan.layout.right.overview
[mdspan.layout.stride]: #mdspan.layout.stride
[mdspan.layout.stride.cons]: #mdspan.layout.stride.cons
[mdspan.layout.stride.expo]: #mdspan.layout.stride.expo
[mdspan.layout.stride.obs]: #mdspan.layout.stride.obs
[mdspan.layout.stride.overview]: #mdspan.layout.stride.overview
[mdspan.mdspan]: #mdspan.mdspan
[mdspan.mdspan.cons]: #mdspan.mdspan.cons
[mdspan.mdspan.members]: #mdspan.mdspan.members
[mdspan.mdspan.overview]: #mdspan.mdspan.overview
[mdspan.overview]: #mdspan.overview
[mdspan.syn]: #mdspan.syn
[multimap]: #multimap
[multimap.cons]: #multimap.cons
[multimap.erasure]: #multimap.erasure
[multimap.modifiers]: #multimap.modifiers
[multimap.overview]: #multimap.overview
[multiset]: #multiset
[multiset.cons]: #multiset.cons
[multiset.erasure]: #multiset.erasure
[multiset.overview]: #multiset.overview
[priority.queue]: #priority.queue
[priqueue.cons]: #priqueue.cons
[priqueue.cons.alloc]: #priqueue.cons.alloc
[priqueue.members]: #priqueue.members
[priqueue.overview]: #priqueue.overview
[priqueue.special]: #priqueue.special
[queue]: #queue
[queue.cons]: #queue.cons
[queue.cons.alloc]: #queue.cons.alloc
[queue.defn]: #queue.defn
[queue.mod]: #queue.mod
[queue.ops]: #queue.ops
[queue.special]: #queue.special
[queue.syn]: #queue.syn
[random.access.iterators]: iterators.md#random.access.iterators
[res.on.data.races]: library.md#res.on.data.races
[sequence.reqmts]: #sequence.reqmts
[sequences]: #sequences
[sequences.general]: #sequences.general
[set]: #set
[set.cons]: #set.cons
[set.erasure]: #set.erasure
[set.overview]: #set.overview
[span.cons]: #span.cons
[span.deduct]: #span.deduct
[span.elem]: #span.elem
[span.iterators]: #span.iterators
[span.objectrep]: #span.objectrep
[span.obs]: #span.obs
[span.overview]: #span.overview
[span.sub]: #span.sub
[span.syn]: #span.syn
[stack]: #stack
[stack.cons]: #stack.cons
[stack.cons.alloc]: #stack.cons.alloc
[stack.defn]: #stack.defn
[stack.general]: #stack.general
[stack.mod]: #stack.mod
[stack.ops]: #stack.ops
[stack.special]: #stack.special
[stack.syn]: #stack.syn
[strings]: strings.md#strings
[swappable.requirements]: library.md#swappable.requirements
[temp.deduct]: temp.md#temp.deduct
[temp.param]: temp.md#temp.param
[temp.type]: temp.md#temp.type
[term.trivially.copyable.type]: basic.md#term.trivially.copyable.type
[unord]: #unord
[unord.general]: #unord.general
[unord.hash]: utilities.md#unord.hash
[unord.map]: #unord.map
[unord.map.cnstr]: #unord.map.cnstr
[unord.map.elem]: #unord.map.elem
[unord.map.erasure]: #unord.map.erasure
[unord.map.modifiers]: #unord.map.modifiers
[unord.map.overview]: #unord.map.overview
[unord.map.syn]: #unord.map.syn
[unord.multimap]: #unord.multimap
[unord.multimap.cnstr]: #unord.multimap.cnstr
[unord.multimap.erasure]: #unord.multimap.erasure
[unord.multimap.modifiers]: #unord.multimap.modifiers
[unord.multimap.overview]: #unord.multimap.overview
[unord.multiset]: #unord.multiset
[unord.multiset.cnstr]: #unord.multiset.cnstr
[unord.multiset.erasure]: #unord.multiset.erasure
[unord.multiset.overview]: #unord.multiset.overview
[unord.req]: #unord.req
[unord.req.except]: #unord.req.except
[unord.req.general]: #unord.req.general
[unord.set]: #unord.set
[unord.set.cnstr]: #unord.set.cnstr
[unord.set.erasure]: #unord.set.erasure
[unord.set.overview]: #unord.set.overview
[unord.set.syn]: #unord.set.syn
[vector]: #vector
[vector.bool]: #vector.bool
[vector.bool.fmt]: #vector.bool.fmt
[vector.bool.pspc]: #vector.bool.pspc
[vector.capacity]: #vector.capacity
[vector.cons]: #vector.cons
[vector.data]: #vector.data
[vector.erasure]: #vector.erasure
[vector.modifiers]: #vector.modifiers
[vector.overview]: #vector.overview
[vector.syn]: #vector.syn
[views]: #views
[views.contiguous]: #views.contiguous
[views.general]: #views.general
[views.multidim]: #views.multidim
[views.span]: #views.span

[^1]: Equality comparison is a refinement of partitioning if no two
    objects that compare equal fall into different partitions.

[^2]: These member functions are only provided by containers whose
    iterators are random access iterators.

[^3]: As specified in  [[allocator.requirements]], the requirements in
    this Clause apply only to lists whose allocators compare equal.

[^4]: `reserve()` uses `Allocator::allocate()` which can throw an
    appropriate exception.
