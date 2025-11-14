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
| [[container.adaptors]]     | Container adaptors               | `<queue>`, `<stack>`                                         |
| [[views]]                  | Views                            | `<span>`                                                     |


## Container requirements <a id="container.requirements">[[container.requirements]]</a>

### General container requirements <a id="container.requirements.general">[[container.requirements.general]]</a>

Containers are objects that store other objects. They control allocation
and deallocation of these objects through constructors, destructors,
insert and erase operations.

All of the complexity requirements in this Clause are stated solely in
terms of the number of operations on the contained objects.

[*Example 1*: The copy constructor of type `vector<vector<int>>` has
linear complexity, even though the complexity of copying each contained
`vector<int>` is itself linear. — *end example*]

For the components affected by this subclause that declare an
`allocator_type`, objects stored in these components shall be
constructed using the function
`allocator_traits<allocator_type>::rebind_traits<U>::{}construct` and
destroyed using the function
`allocator_traits<allocator_type>::rebind_traits<U>::{}destroy`
[[allocator.traits.members]], where `U` is either
`allocator_type::value_type` or an internal type used by the container.
These functions are called only for the container’s element type, not
for internal types used by the container.

[*Note 1*: This means, for example, that a node-based container might
need to construct nodes containing aligned buffers and call `construct`
to place the element into the buffer. — *end note*]

In Tables  [[tab:container.req]], [[tab:container.rev.req]], and
[[tab:container.opt]] `X` denotes a container class containing objects
of type `T`, `a` and `b` denote values of type `X`, `i` and `j` denote
values of type (possibly const) `X::iterator`, `u` denotes an
identifier, `r` denotes a non-const value of type `X`, and `rv` denotes
a non-const rvalue of type `X`.

Those entries marked “(Note A)” or “(Note B)” have linear complexity for
`array` and have constant complexity for all other standard containers.

[*Note 2*: The algorithm `equal()` is defined in
[[algorithms]]. — *end note*]

The member function `size()` returns the number of elements in the
container. The number of elements is defined by the rules of
constructors, inserts, and erases.

`begin()`

returns an iterator referring to the first element in the container.
`end()` returns an iterator which is the past-the-end value for the
container. If the container is empty, then `begin() == end()`.

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

Unless otherwise specified, all containers defined in this clause obtain
memory using an allocator (see  [[allocator.requirements]]).

[*Note 3*: In particular, containers and iterators do not store
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

[*Note 4*: If an invocation of a constructor uses the default value of
an optional allocator argument, then the allocator type must support
value-initialization. — *end note*]

A copy of this allocator is used for any memory allocation and element
construction performed, by these constructors and by all member
functions, during the lifetime of each container object or until the
allocator is replaced. The allocator may be replaced only via assignment
or `swap()`. Allocator replacement is performed by copy assignment, move
assignment, or swapping of the allocator only if
`allocator_traits<allocator_type>::propagate_on_container_copy_assignment::value`,
`allocator_traits<allocator_type>::propagate_on_container_move_assignment::value`,
or
`allocator_traits<allocator_type>::propagate_on_container_swap::value`
is `true` within the implementation of the corresponding container
operation. In all container types defined in this Clause, the member
`get_allocator()` returns a copy of the allocator used to construct the
container or, if that allocator has been replaced, a copy of the most
recent replacement.

The expression `a.swap(b)`, for containers `a` and `b` of a standard
container type other than `array`, shall exchange the values of `a` and
`b` without invoking any move, copy, or swap operations on the
individual container elements. Lvalues of any `Compare`, `Pred`, or
`Hash` types belonging to `a` and `b` shall be swappable and shall be
exchanged by calling `swap` as described in  [[swappable.requirements]].
If
`allocator_traits<allocator_type>::propagate_on_container_swap::value`
is `true`, then lvalues of type `allocator_type` shall be swappable and
the allocators of `a` and `b` shall also be exchanged by calling `swap`
as described in  [[swappable.requirements]]. Otherwise, the allocators
shall not be swapped, and the behavior is undefined unless
`a.get_allocator() == b.get_allocator()`. Every iterator referring to an
element in one container before the swap shall refer to the same element
in the other container after the swap. It is unspecified whether an
iterator with value `a.end()` before the swap will have value `b.end()`
after the swap.

If the iterator type of a container belongs to the bidirectional or
random access iterator categories [[iterator.requirements]], the
container is called *reversible* and meets the additional requirements
in [[container.rev.req]].

Unless otherwise specified (see  [[associative.reqmts.except]],
[[unord.req.except]], [[deque.modifiers]], and [[vector.modifiers]]) all
container types defined in this Clause meet the following additional
requirements:

- if an exception is thrown by an `insert()` or `emplace()` function
  while inserting a single element, that function has no effects.
- if an exception is thrown by a `push_back()`, `push_front()`,
  `emplace_back()`, or `emplace_front()` function, that function has no
  effects.
- no `erase()`, `clear()`, `pop_back()` or `pop_front()` function throws
  an exception.
- no copy constructor or assignment operator of a returned iterator
  throws an exception.
- no `swap()` function throws an exception.
- no `swap()` function invalidates any references, pointers, or
  iterators referring to the elements of the containers being swapped.
  \[*Note 1*: The `end()` iterator does not refer to any element, so it
  may be invalidated. — *end note*]

Unless otherwise specified (either explicitly or by defining a function
in terms of other functions), invoking a container member function or
passing a container as an argument to a library function shall not
invalidate iterators to, or change the values of, objects within that
container.

A *contiguous container* is a container whose member types `iterator`
and `const_iterator` meet the *Cpp17RandomAccessIterator* requirements
[[random.access.iterators]] and model `contiguous_iterator`
[[iterator.concept.contiguous]].

[[container.opt]] lists operations that are provided for some types of
containers but not others. Those containers for which the listed
operations are provided shall implement the semantics described in
[[container.opt]] unless otherwise stated. If the iterators passed to
`lexicographical_compare_three_way` meet the constexpr iterator
requirements [[iterator.requirements.general]] then the operations
described in [[container.opt]] are implemented by constexpr functions.

[*Note 5*: The algorithm `lexicographical_compare_three_way` is defined
in [[algorithms]]. — *end note*]

All of the containers defined in this Clause and in  [[basic.string]]
except `array` meet the additional requirements of an allocator-aware
container, as described in [[container.alloc.req]].

Given an allocator type `A` and given a container type `X` having a
`value_type` identical to `T` and an `allocator_type` identical to
`allocator_traits<A>::rebind_alloc<T>` and given an lvalue `m` of type
`A`, a pointer `p` of type `T*`, an expression `v` of type (possibly
`const`) `T`, and an rvalue `rv` of type `T`, the following terms are
defined. If `X` is not allocator-aware, the terms below are defined as
if `A` were `allocator<T>` — no allocator object needs to be created and
user specializations of `allocator<T>` are not instantiated:

- `T` is *\textit{Cpp17DefaultInsertable} into `X`* into
  X@*Cpp17DefaultInsertable* into `X` means that the following
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
- `T` is *\textit{Cpp17MoveInsertable} into `X`* into
  X@*Cpp17MoveInsertable* into `X` means that the following expression
  is well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, rv)
  ```

  and its evaluation causes the following postcondition to hold: The
  value of `*p` is equivalent to the value of `rv` before the
  evaluation.
  \[*Note 2*: `rv` remains a valid object. Its state is
  unspecified — *end note*]
- `T` is *\textit{Cpp17CopyInsertable} into `X`* into
  X@*Cpp17CopyInsertable* into `X` means that, in addition to `T` being
  *Cpp17MoveInsertable* into `X`, the following expression is
  well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, v)
  ```

  and its evaluation causes the following postcondition to hold: The
  value of `v` is unchanged and is equivalent to `*p`.
- `T` is *\textit{Cpp17EmplaceConstructible} into `X` from `args`* into
  X from args@*Cpp17EmplaceConstructible* into `X` from `args`, for zero
  or more arguments `args`, means that the following expression is
  well-formed:
  ``` cpp
  allocator_traits<A>::construct(m, p, args)
  ```
- `T` is *\textit{Cpp17Erasable} from `X`* from X@*Cpp17Erasable* from
  `X` means that the following expression is well-formed:
  ``` cpp
  allocator_traits<A>::destroy(m, p)
  ```

[*Note 6*: A container calls
`allocator_traits<A>::construct(m, p, args)` to construct an element at
`p` using `args`, with `m == get_allocator()`. The default `construct`
in `allocator` will call `::new((void*)p) T(args)`, but specialized
allocators may choose a different definition. — *end note*]

In [[container.alloc.req]], `X` denotes an allocator-aware container
class with a `value_type` of `T` using allocator of type `A`, `u`
denotes a variable, `a` and `b` denote non-const lvalues of type `X`,
`t` denotes an lvalue or a const rvalue of type `X`, `rv` denotes a
non-const rvalue of type `X`, and `m` is a value of type `A`.

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
may result in a data race. As an exception to the general rule, for a
`vector<bool> y`, `y[0] = true` may race with
`y[1] = true`. — *end note*]

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

[*Note 1*: The sequence containers offer the programmer different
complexity trade-offs and should be used accordingly. `vector` is the
type of sequence container that should be used by default. `array`
should be used when the container has a fixed size known during
translation. `list` or `forward_list` should be used when there are
frequent insertions and deletions from the middle of the sequence.
`deque` is the data structure of choice when most insertions and
deletions take place at the beginning or at the end of the sequence.
When choosing a container, remember `vector` is best; leave a comment to
explain if you choose from the rest! — *end note*]

In Tables  [[tab:container.seq.req]] and [[tab:container.seq.opt]], `X`
denotes a sequence container class, `a` denotes a value of type `X`
containing elements of type `T`, `u` denotes the name of a variable
being declared, `A` denotes `X::allocator_type` if the *qualified-id*
`X::allocator_type` is valid and denotes a type [[temp.deduct]] and
`allocator<T>` if it doesn’t, `i` and `j` denote iterators that meet the
*Cpp17InputIterator* requirements and refer to elements implicitly
convertible to `value_type`, `[i, j)` denotes a valid range, `il`
designates an object of type `initializer_list<value_type>`, `n` denotes
a value of type `X::size_type`, `p` denotes a valid constant iterator to
`a`, `q` denotes a valid dereferenceable constant iterator to `a`,
`[q1, q2)` denotes a valid range of constant iterators in `a`, `t`
denotes an lvalue or a const rvalue of `X::value_type`, and `rv` denotes
a non-const rvalue of `X::value_type`. `Args` denotes a template
parameter pack; `args` denotes a function parameter pack with the
pattern `Args&&`.

The complexities of the expressions are sequence dependent.

[*Note 2*: `args` may directly or indirectly refer to a value in
`a`. — *end note*]

The iterator returned from `a.insert(p, t)` points to the copy of `t`
inserted into `a`.

The iterator returned from `a.insert(p, rv)` points to the copy of `rv`
inserted into `a`.

The iterator returned from `a.insert(p, n, t)` points to the copy of the
first element inserted into `a`, or `p` if `n == 0`.

The iterator returned from `a.insert(p, i, j)` points to the copy of the
first element inserted into `a`, or `p` if `i == j`.

The iterator returned from `a.insert(p, il)` points to the copy of the
first element inserted into `a`, or `p` if `il` is empty.

The iterator returned from `a.emplace(p, args)` points to the new
element constructed from `args` into `a`.

The iterator returned from `a.erase(q)` points to the element
immediately following `q` prior to the element being erased. If no such
element exists, `a.end()` is returned.

The iterator returned by `a.erase(q1, q2)` points to the element pointed
to by `q2` prior to any elements being erased. If no such element
exists, `a.end()` is returned.

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

[[container.seq.opt]] lists operations that are provided for some types
of sequence containers but not others. An implementation shall provide
these operations for all container types shown in the “container”
column, and shall implement them so as to take amortized constant time.

The member function `at()` provides bounds-checked access to container
elements. `at()` throws `out_of_range` if `n >= a.size()`.

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
  // These type declarations are described in Tables [tab:container.assoc.req] and [tab:container.hash.req].
  using value_type     = see belownc{};     // not present for map containers
  using key_type       = see belownc{};     // not present for set containers
  using mapped_type    = see belownc{};     // not present for set containers
  using allocator_type = see belownc{};

private:
  using container_node_type = unspecified;
  using ator_traits = allocator_traits<allocator_type>;

  typename ator_traits::template rebind_traits<container_node_type>::pointer ptr_;
  optional<allocator_type> alloc_;

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

Associative containers provide fast retrieval of data based on keys. The
library provides four basic kinds of associative containers: `set`,
`multiset`, `map` and `multimap`.

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

The associative containers meet all the requirements of Allocator-aware
containers [[container.requirements.general]], except that for `map` and
`multimap`, the requirements placed on `value_type` in
[[container.alloc.req]] apply instead to `key_type` and `mapped_type`.

[*Note 3*: For example, in some cases `key_type` and `mapped_type` are
required to be *Cpp17CopyAssignable* even though the associated
`value_type`, `pair<const key_type, mapped_type>`, is not
*Cpp17CopyAssignable*. — *end note*]

In [[container.assoc.req]], `X` denotes an associative container class,
`a` denotes a value of type `X`, `a2` denotes a value of a type with
nodes compatible with type `X` ([[container.node.compat]]), `b` denotes
a possibly `const` value of type `X`, `u` denotes the name of a variable
being declared, `a_uniq` denotes a value of type `X` when `X` supports
unique keys, `a_eq` denotes a value of type `X` when `X` supports
multiple keys, `a_tran` denotes a possibly `const` value of type `X`
when the *qualified-id* `X::key_compare::is_transparent` is valid and
denotes a type [[temp.deduct]], `i` and `j` meet the
*Cpp17InputIterator* requirements and refer to elements implicitly
convertible to `value_type`, \[`i`, `j`) denotes a valid range, `p`
denotes a valid constant iterator to `a`, `q` denotes a valid
dereferenceable constant iterator to `a`, `r` denotes a valid
dereferenceable iterator to `a`, `[q1, q2)` denotes a valid range of
constant iterators in `a`, `il` designates an object of type
`initializer_list<value_type>`, `t` denotes a value of type
`X::value_type`, `k` denotes a value of type `X::key_type` and `c`
denotes a possibly `const` value of type `X::key_compare`; `kl` is a
value such that `a` is partitioned [[alg.sorting]] with respect to
`c(r, kl)`, with `r` the key value of `e` and `e` in `a`; `ku` is a
value such that `a` is partitioned with respect to `!c(ku, r)`; `ke` is
a value such that `a` is partitioned with respect to `c(r, ke)` and
`!c(ke, r)`, with `c(r, ke)` implying `!c(ke, r)`. `A` denotes the
storage allocator used by `X`, if any, or `allocator<X::value_type>`
otherwise, `m` denotes an allocator of a type convertible to `A`, and
`nh` denotes a non-const rvalue of type `X::node_type`.

The `insert` and `emplace` members shall not affect the validity of
iterators and references to the container, and the `erase` members shall
invalidate only iterators and references to the erased elements.

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
`lower_bound`, `upper_bound`, and `equal_range` shall not participate in
overload resolution unless the *qualified-id* `Compare::is_transparent`
is valid and denotes a type [[temp.deduct]].

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

The unordered associative containers meet all the requirements of
Allocator-aware containers [[container.requirements.general]], except
that for `unordered_map` and `unordered_multimap`, the requirements
placed on `value_type` in [[container.alloc.req]] apply instead to
`key_type` and `mapped_type`.

[*Note 3*: For example, `key_type` and `mapped_type` are sometimes
required to be *Cpp17CopyAssignable* even though the associated
`value_type`, `pair<const key_type, mapped_type>`, is not
*Cpp17CopyAssignable*. — *end note*]

In [[container.hash.req]]:

- `X` denotes an unordered associative container class,
- `a` denotes a value of type `X`,
- `a2` denotes a value of a type with nodes compatible with type `X` (
  [[container.node.compat]]),
- `b` denotes a possibly const value of type `X`,
- `a_uniq` denotes a value of type `X` when `X` supports unique keys,
- `a_eq` denotes a value of type `X` when `X` supports equivalent keys,
- `a_tran` denotes a possibly const value of type `X` when the
  *qualified-id*s `X::key_equal::is_transparent` and
  `X::hasher::is_transparent` are both valid and denote types
  [[temp.deduct]],
- `i` and `j` denote input iterators that refer to `value_type`,
- `[i, j)` denotes a valid range,
- `p` and `q2` denote valid constant iterators to `a`,
- `q` and `q1` denote valid dereferenceable constant iterators to `a`,
- `r` denotes a valid dereferenceable iterator to `a`,
- `[q1, q2)` denotes a valid range in `a`,
- `il` denotes a value of type `initializer_list<value_type>`,
- `t` denotes a value of type `X::value_type`,
- `k` denotes a value of type `key_type`,
- `hf` denotes a possibly const value of type `hasher`,
- `eq` denotes a possibly const value of type `key_equal`,
- `ke` is a value such that
  - `eq(r1, ke) == eq(ke, r1)`
  - `hf(r1) == hf(ke)` if `eq(r1, ke)` is `true`, and
  - `(eq(r1, ke) && eq(r1, r2)) == eq(r2, ke)`

  where `r1` and `r2` are keys of elements in `a_tran`,
- `n` denotes a value of type `size_type`,
- `z` denotes a value of type `float`, and
- `nh` denotes a non-const rvalue of type `X::node_type`.

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
(but worst-case complexity remains , e.g., for a pathologically bad hash
function). The behavior of a program that uses `operator==` or
`operator!=` on unordered containers is undefined unless the `Pred`
function object has the same behavior for both containers and the
equality comparison function for `Key` is a refinement[^1] of the
partition into equivalent-key groups produced by `Pred`.

The iterator types `iterator` and `const_iterator` of an unordered
associative container are of at least the forward iterator category. For
unordered associative containers where the key type and value type are
the same, both `iterator` and `const_iterator` are constant iterators.

The `insert` and `emplace` members shall not affect the validity of
references to container elements, but may invalidate all iterators to
the container. The `erase` members shall invalidate only iterators and
references to the erased elements, and preserve the relative order of
the elements that are not erased.

The `insert` and `emplace` members shall not affect the validity of
iterators if `(N+n) <= z * B`, where `N` is the number of elements in
the container prior to the insert operation, `n` is the number of
elements inserted, `B` is the container’s bucket count, and `z` is the
container’s maximum load factor.

The `extract` members invalidate only iterators to the removed element,
and preserve the relative order of the elements that are not erased;
pointers and references to the removed element remain valid. However,
accessing the element through such pointers and references while the
element is owned by a `node_type` is undefined behavior. References and
pointers to an element obtained while it is owned by a `node_type` are
invalidated if the element is successfully inserted.

The member function templates `find`, `count`, `equal_range`, and
`contains` shall not participate in overload resolution unless the
*qualified-id*s `Pred::is_transparent` and `Hash::is_transparent` are
both valid and denote types [[temp.deduct]].

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
  // [forwardlist], class template forward_list
  template<class T, class Allocator = allocator<T>> class forward_list;

  template<class T, class Allocator>
    bool operator==(const forward_list<T, Allocator>& x, const forward_list<T, Allocator>& y);
  template<class T, class Allocator>
    synth-three-way-result<T> operator<=>(const forward_list<T, Allocator>& x,
    \itcorr                                      const forward_list<T, Allocator>& y);

  template<class T, class Allocator>
    void swap(forward_list<T, Allocator>& x, forward_list<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));

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

  template<class T, class Allocator, class U>
    constexpr typename vector<T, Allocator>::size_type
      erase(vector<T, Allocator>& c, const U& value);
  template<class T, class Allocator, class Predicate>
    constexpr typename vector<T, Allocator>::size_type
      erase_if(vector<T, Allocator>& c, Predicate pred);

  // [vector.bool], class vector<bool>
  template<class Allocator> class vector<bool, Allocator>;

  // hash support
  template<class T> struct hash;
  template<class Allocator> struct hash<vector<bool, Allocator>>;

  namespace pmr {
    template<class T>
      using vector = std::vector<T, polymorphic_allocator<T>>;
  }
}
```

### Class template `array` <a id="array">[[array]]</a>

#### Overview <a id="array.overview">[[array.overview]]</a>

The header `<array>` defines a class template for storing fixed-size
sequences of objects. An `array` is a contiguous container
[[container.requirements.general]]. An instance of `array<T, N>` stores
`N` elements of type `T`, so that `size() == N` is an invariant.

An `array` is an aggregate [[dcl.init.aggr]] that can be
list-initialized with up to `N` elements whose types are convertible to
`T`.

An `array` meets all of the requirements of a container and of a
reversible container [[container.requirements]], except that a default
constructed `array` object is not empty and that `swap` does not have
constant complexity. An `array` meets some of the requirements of a
sequence container [[sequence.reqmts]]. Descriptions are provided here
only for operations on `array` that are not described in one of these
tables and for operations where there is additional semantic
information.

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
`array` relies on the implicitly-declared special member functions (
[[class.default.ctor]], [[class.dtor]], and [[class.copy.ctor]]) to
conform to the container requirements table in 
[[container.requirements]]. In addition to the requirements specified in
the container requirements table, the implicit move constructor and move
assignment operator for `array` require that `T` be
*Cpp17MoveConstructible* or *Cpp17MoveAssignable*, respectively.

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
`array::swap` takes linear time, may exit via an exception, and does not
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

*Returns:* A reference to the `I`^\text{th} element of `a`, where
indexing is zero-based.

### Class template `deque` <a id="deque">[[deque]]</a>

#### Overview <a id="deque.overview">[[deque.overview]]</a>

A `deque` is a sequence container that supports random access iterators
[[random.access.iterators]]. In addition, it supports constant time
insert and erase operations at the beginning or the end; insert and
erase in the middle take linear time. That is, a deque is especially
optimized for pushing and popping elements at the beginning and end.
Storage management is handled automatically.

A `deque` meets all of the requirements of a container, of a reversible
container (given in tables in  [[container.requirements]]), of a
sequence container, including the optional sequence container
requirements [[sequence.reqmts]], and of an allocator-aware container (
[[container.alloc.req]]). Descriptions are provided here only for
operations on `deque` that are not described in one of these tables or
for operations where there is additional semantic information.

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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    deque(const deque& x);
    deque(deque&&);
    deque(const deque&, const Allocator&);
    deque(deque&&, const Allocator&);
    deque(initializer_list<T>, const Allocator& = Allocator());

    ~deque();
    deque& operator=(const deque& x);
    deque& operator=(deque&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    deque& operator=(initializer_list<T>);
    template<class InputIterator>
      void assign(InputIterator first, InputIterator last);
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
    void push_back(const T& x);
    void push_back(T&& x);

    iterator insert(const_iterator position, const T& x);
    iterator insert(const_iterator position, T&& x);
    iterator insert(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      iterator insert(const_iterator position, InputIterator first, InputIterator last);
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

  // swap
  template<class T, class Allocator>
    void swap(deque<T, Allocator>& x, deque<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
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

*Effects:* Constructs a `deque` with `n` default-inserted elements using
the specified allocator.

*Preconditions:* `T` is *Cpp17DefaultInsertable* into `*this`.

*Complexity:* Linear in `n`.

``` cpp
deque(size_type n, const T& value, const Allocator& = Allocator());
```

*Effects:* Constructs a `deque` with `n` copies of `value`, using the
specified allocator.

*Preconditions:* `T` is *Cpp17CopyInsertable* into `*this`.

*Complexity:* Linear in `n`.

``` cpp
template<class InputIterator>
  deque(InputIterator first, InputIterator last, const Allocator& = Allocator());
```

*Effects:* Constructs a `deque` equal to the range \[`first`, `last`),
using the specified allocator.

*Complexity:* Linear in `distance(first, last)`.

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
iterator insert(const_iterator position, initializer_list<T>);

template<class... Args> reference emplace_front(Args&&... args);
template<class... Args> reference emplace_back(Args&&... args);
template<class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_front(const T& x);
void push_front(T&& x);
void push_back(const T& x);
void push_back(T&& x);
```

*Effects:* An insertion in the middle of the deque invalidates all the
iterators and references to elements of the deque. An insertion at
either end of the deque invalidates all the iterators to the deque, but
has no effect on the validity of references to elements of the deque.

*Remarks:* If an exception is thrown other than by the copy constructor,
move constructor, assignment operator, or move assignment operator of
`T` there are no effects. If an exception is thrown while inserting a
single element at either end, there are no effects. Otherwise, if an
exception is thrown by the move constructor of a
non-*Cpp17CopyInsertable* `T`, the effects are unspecified.

*Complexity:* The complexity is linear in the number of elements
inserted plus the lesser of the distances to the beginning and end of
the deque. Inserting a single element at either the beginning or end of
a deque always takes constant time and causes a single call to a
constructor of `T`.

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

*Complexity:* The number of calls to the destructor of `T` is the same
as the number of elements erased, but the number of calls to the
assignment operator of `T` is no more than the lesser of the number of
elements before the erased elements and the number of elements after the
erased elements.

*Throws:* Nothing unless an exception is thrown by the assignment
operator of `T`.

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

### Class template `forward_list` <a id="forwardlist">[[forwardlist]]</a>

#### Overview <a id="forwardlist.overview">[[forwardlist.overview]]</a>

A `forward_list` is a container that supports forward iterators and
allows constant time insert and erase operations anywhere within the
sequence, with storage management handled automatically. Fast random
access to list elements is not supported.

[*Note 1*: It is intended that `forward_list` have zero space or time
overhead relative to a hand-written C-style singly linked list. Features
that would conflict with that goal have been omitted. — *end note*]

A `forward_list` meets all of the requirements of a container (
[[container.req]]), except that the `size()` member function is not
provided and `operator==` has linear complexity. A `forward_list` also
meets all of the requirements for an allocator-aware container (
[[container.alloc.req]]). In addition, a `forward_list` provides the
`assign` member functions ([[container.seq.req]]) and several of the
optional container requirements ([[container.seq.opt]]). Descriptions
are provided here only for operations on `forward_list` that are not
described in that table or for operations where there is additional
semantic information.

[*Note 2*: Modifying any list requires access to the element preceding
the first element of interest, but in a `forward_list` there is no
constant-time way to access a preceding element. For this reason, ranges
that are modified, such as those supplied to `erase` and `splice`, must
be open at the beginning. — *end note*]

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
    using size_type       = implementation-defined; // see [container.requirements]
    using difference_type = implementation-defined; // see [container.requirements]
    using iterator        = implementation-defined  // type of forward_list::iterator; // see [container.requirements]
    using const_iterator  = implementation-defined  // type of forward_list::const_iterator; // see [container.requirements]

    // [forwardlist.cons], construct/copy/destroy
    forward_list() : forward_list(Allocator()) { }
    explicit forward_list(const Allocator&);
    explicit forward_list(size_type n, const Allocator& = Allocator());
    forward_list(size_type n, const T& value, const Allocator& = Allocator());
    template<class InputIterator>
      forward_list(InputIterator first, InputIterator last, const Allocator& = Allocator());
    forward_list(const forward_list& x);
    forward_list(forward_list&& x);
    forward_list(const forward_list& x, const Allocator&);
    forward_list(forward_list&& x, const Allocator&);
    forward_list(initializer_list<T>, const Allocator& = Allocator());
    ~forward_list();
    forward_list& operator=(const forward_list& x);
    forward_list& operator=(forward_list&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    forward_list& operator=(initializer_list<T>);
    template<class InputIterator>
      void assign(InputIterator first, InputIterator last);
    void assign(size_type n, const T& t);
    void assign(initializer_list<T>);
    allocator_type get_allocator() const noexcept;

    // [forwardlist.iter], iterators
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

    // [forwardlist.access], element access
    reference front();
    const_reference front() const;

    // [forwardlist.modifiers], modifiers
    template<class... Args> reference emplace_front(Args&&... args);
    void push_front(const T& x);
    void push_front(T&& x);
    void pop_front();

    template<class... Args> iterator emplace_after(const_iterator position, Args&&... args);
    iterator insert_after(const_iterator position, const T& x);
    iterator insert_after(const_iterator position, T&& x);

    iterator insert_after(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      iterator insert_after(const_iterator position, InputIterator first, InputIterator last);
    iterator insert_after(const_iterator position, initializer_list<T> il);

    iterator erase_after(const_iterator position);
    iterator erase_after(const_iterator position, const_iterator last);
    void swap(forward_list&)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);

    void resize(size_type sz);
    void resize(size_type sz, const value_type& c);
    void clear() noexcept;

    // [forwardlist.ops], forward_list operations
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

  // swap
  template<class T, class Allocator>
    void swap(forward_list<T, Allocator>& x, forward_list<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
}
```

An incomplete type `T` may be used when instantiating `forward_list` if
the allocator meets the allocator completeness requirements
[[allocator.requirements.completeness]]. `T` shall be complete before
any member of the resulting specialization of `forward_list` is
referenced.

#### Constructors, copy, and assignment <a id="forwardlist.cons">[[forwardlist.cons]]</a>

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

#### Iterators <a id="forwardlist.iter">[[forwardlist.iter]]</a>

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

#### Element access <a id="forwardlist.access">[[forwardlist.access]]</a>

``` cpp
reference front();
const_reference front() const;
```

*Returns:* `*begin()`

#### Modifiers <a id="forwardlist.modifiers">[[forwardlist.modifiers]]</a>

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
void pop_front();
```

*Effects:* As if by `erase_after(before_begin())`.

``` cpp
iterator insert_after(const_iterator position, const T& x);
iterator insert_after(const_iterator position, T&& x);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts a copy of `x` after `position`.

*Returns:* An iterator pointing to the copy of `x`.

``` cpp
iterator insert_after(const_iterator position, size_type n, const T& x);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts `n` copies of `x` after `position`.

*Returns:* An iterator pointing to the last inserted copy of `x` or
`position` if `n == 0`.

``` cpp
template<class InputIterator>
  iterator insert_after(const_iterator position, InputIterator first, InputIterator last);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`). Neither `first` nor `last`
are iterators in `*this`.

*Effects:* Inserts copies of elements in \[`first`, `last`) after
`position`.

*Returns:* An iterator pointing to the last inserted element or
`position` if `first == last`.

``` cpp
iterator insert_after(const_iterator position, initializer_list<T> il);
```

*Effects:* `insert_after(p, il.begin(), il.end())`.

*Returns:* An iterator pointing to the last inserted element or
`position` if `il` is empty.

``` cpp
template<class... Args>
  iterator emplace_after(const_iterator position, Args&&... args);
```

*Preconditions:* `position` is `before_begin()` or is a dereferenceable
iterator in the range \[`begin()`, `end()`).

*Effects:* Inserts an object of type `value_type` constructed with
`value_type(std::forward<Args>(args)...)` after `position`.

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

#### Operations <a id="forwardlist.ops">[[forwardlist.ops]]</a>

In this subclause, arguments for a template parameter named `Predicate`
or `BinaryPredicate` shall meet the corresponding requirements in
[[algorithms.requirements]]. For `merge` and `sort`, the definitions and
requirements in [[alg.sorting]] apply.

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

*Remarks:* Stable [[algorithm.stable]].

*Complexity:* Exactly `distance(begin(), end())` applications of the
corresponding predicate.

``` cpp
size_type unique();
template<class BinaryPredicate> size_type unique(BinaryPredicate pred);
```

*Effects:* Erases all but the first element from every consecutive group
of equal elements referred to by the iterator `i` in the range
\[`first + 1`, `last`) for which `*i == *(i-1)` (for the version with no
arguments) or `pred(*i, *(i - 1))` (for the version with a predicate
argument) holds. Invalidates only the iterators and references to the
erased elements.

*Returns:* The number of elements erased.

*Throws:* Nothing unless an exception is thrown by the equality
comparison or the predicate.

*Complexity:* If the range \[`first`, `last`) is not empty, exactly
`(last - first) - 1` applications of the corresponding predicate,
otherwise no applications of the predicate.

``` cpp
void merge(forward_list& x);
void merge(forward_list&& x);
template<class Compare> void merge(forward_list& x, Compare comp);
template<class Compare> void merge(forward_list&& x, Compare comp);
```

*Preconditions:* `*this` and `x` are both sorted with respect to the
comparator `operator<` (for the first two overloads) or `comp` (for the
last two overloads), and `get_allocator() == x.get_allocator()` is
`true`.

*Effects:* Merges the two sorted ranges `[begin(), end())` and
`[x.begin(), x.end())`. `x` is empty after the merge. If an exception is
thrown other than by a comparison there are no effects. Pointers and
references to the moved elements of `x` now refer to those same elements
but as members of `*this`. Iterators referring to the moved elements
will continue to refer to their elements, but they now behave as
iterators into `*this`, not into `x`.

*Remarks:* Stable [[algorithm.stable]].

*Complexity:* At most
`distance(begin(), end()) + distance(x.begin(), x.end()) - 1`
comparisons.

``` cpp
void sort();
template<class Compare> void sort(Compare comp);
```

*Effects:* Sorts the list according to the `operator<` or the `comp`
function object. If an exception is thrown, the order of the elements in
`*this` is unspecified. Does not affect the validity of iterators and
references.

*Remarks:* Stable [[algorithm.stable]].

*Complexity:* Approximately N log N comparisons, where N is
`distance(begin(), end())`.

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

A `list` meets all of the requirements of a container, of a reversible
container (given in two tables in [[container.requirements]]), of a
sequence container, including most of the optional sequence container
requirements [[sequence.reqmts]], and of an allocator-aware container (
[[container.alloc.req]]). The exceptions are the `operator[]` and `at`
member functions, which are not provided.[^2] Descriptions are provided
here only for operations on `list` that are not described in one of
these tables or for operations where there is additional semantic
information.

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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    list(const list& x);
    list(list&& x);
    list(const list&, const Allocator&);
    list(list&&, const Allocator&);
    list(initializer_list<T>, const Allocator& = Allocator());
    ~list();
    list& operator=(const list& x);
    list& operator=(list&& x)
      noexcept(allocator_traits<Allocator>::is_always_equal::value);
    list& operator=(initializer_list<T>);
    template<class InputIterator>
      void assign(InputIterator first, InputIterator last);
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
    void pop_front();
    void push_back(const T& x);
    void push_back(T&& x);
    void pop_back();

    template<class... Args> iterator emplace(const_iterator position, Args&&... args);
    iterator insert(const_iterator position, const T& x);
    iterator insert(const_iterator position, T&& x);
    iterator insert(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      iterator insert(const_iterator position, InputIterator first, InputIterator last);
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

  // swap
  template<class T, class Allocator>
    void swap(list<T, Allocator>& x, list<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
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
iterator insert(const_iterator position, initializer_list<T>);

template<class... Args> reference emplace_front(Args&&... args);
template<class... Args> reference emplace_back(Args&&... args);
template<class... Args> iterator emplace(const_iterator position, Args&&... args);
void push_front(const T& x);
void push_front(T&& x);
void push_back(const T& x);
void push_back(T&& x);
```

*Remarks:* Does not affect the validity of iterators and references. If
an exception is thrown there are no effects.

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

#### Operations <a id="list.ops">[[list.ops]]</a>

Since lists allow fast insertion and erasing from the middle of a list,
certain operations are provided specifically for them.[^3] In this
subclause, arguments for a template parameter named `Predicate` or
`BinaryPredicate` shall meet the corresponding requirements in
[[algorithms.requirements]]. For `merge` and `sort`, the definitions and
requirements in [[alg.sorting]] apply.

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

*Remarks:* Stable [[algorithm.stable]].

*Complexity:* Exactly `size()` applications of the corresponding
predicate.

``` cpp
size_type unique();
template<class BinaryPredicate> size_type unique(BinaryPredicate binary_pred);
```

*Effects:* Erases all but the first element from every consecutive group
of equal elements referred to by the iterator `i` in the range
\[`first + 1`, `last`) for which `*i == *(i-1)` (for the version of
`unique` with no arguments) or `pred(*i, *(i - 1))` (for the version of
`unique` with a predicate argument) holds. Invalidates only the
iterators and references to the erased elements.

*Returns:* The number of elements erased.

*Throws:* Nothing unless an exception is thrown by `*i == *(i-1)` or
`pred(*i, *(i - 1))`

*Complexity:* If the range `[first, last)` is not empty, exactly
`(last - first) - 1` applications of the corresponding predicate,
otherwise no applications of the predicate.

``` cpp
void merge(list& x);
void merge(list&& x);
template<class Compare> void merge(list& x, Compare comp);
template<class Compare> void merge(list&& x, Compare comp);
```

*Preconditions:* Both the list and the argument list shall be sorted
with respect to the comparator `operator<` (for the first two overloads)
or `comp` (for the last two overloads), and
`get_allocator() == x.get_allocator()` is `true`.

*Effects:* If `addressof(x) == this`, does nothing; otherwise, merges
the two sorted ranges `[begin(), end())` and `[x.begin(), x.end())`. The
result is a range in which the elements will be sorted in non-decreasing
order according to the ordering defined by `comp`; that is, for every
iterator `i`, in the range other than the first, the condition
`comp(*i, *(i - 1))` will be `false`. Pointers and references to the
moved elements of `x` now refer to those same elements but as members of
`*this`. Iterators referring to the moved elements will continue to
refer to their elements, but they now behave as iterators into `*this`,
not into `x`.

*Remarks:* Stable [[algorithm.stable]]. If `addressof(x) != this`, the
range `[x.begin(), x.end())` is empty after the merge. No elements are
copied by this operation.

*Complexity:* At most `size() + x.size() - 1` applications of `comp` if
`addressof(x) != this`; otherwise, no applications of `comp` are
performed. If an exception is thrown other than by a comparison there
are no effects.

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

*Remarks:* Stable [[algorithm.stable]].

*Complexity:* Approximately N log N comparisons, where `N == size()`.

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

A `vector` meets all of the requirements of a container and of a
reversible container (given in two tables in 
[[container.requirements]]), of a sequence container, including most of
the optional sequence container requirements [[sequence.reqmts]], of an
allocator-aware container ([[container.alloc.req]]), and, for an
element type other than `bool`, of a contiguous container
[[container.requirements.general]]. The exceptions are the `push_front`,
`pop_front`, and `emplace_front` member functions, which are not
provided. Descriptions are provided here only for operations on `vector`
that are not described in one of these tables or for operations where
there is additional semantic information.

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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    constexpr vector(const vector& x);
    constexpr vector(vector&&) noexcept;
    constexpr vector(const vector&, const Allocator&);
    constexpr vector(vector&&, const Allocator&);
    constexpr vector(initializer_list<T>, const Allocator& = Allocator());
    constexpr ~vector();
    constexpr vector& operator=(const vector& x);
    constexpr vector& operator=(vector&& x)
      noexcept(allocator_traits<Allocator>::propagate_on_container_move_assignment::value ||
               allocator_traits<Allocator>::is_always_equal::value);
    constexpr vector& operator=(initializer_list<T>);
    template<class InputIterator>
      constexpr void assign(InputIterator first, InputIterator last);
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
    constexpr void pop_back();

    template<class... Args> constexpr iterator emplace(const_iterator position, Args&&... args);
    constexpr iterator insert(const_iterator position, const T& x);
    constexpr iterator insert(const_iterator position, T&& x);
    constexpr iterator insert(const_iterator position, size_type n, const T& x);
    template<class InputIterator>
      constexpr iterator insert(const_iterator position,
                                InputIterator first, InputIterator last);
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

  // swap
  template<class T, class Allocator>
    constexpr void swap(vector<T, Allocator>& x, vector<T, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
}
```

An incomplete type `T` may be used when instantiating `vector` if the
allocator meets the allocator completeness requirements
[[allocator.requirements.completeness]]. `T` shall be complete before
any member of the resulting specialization of `vector` is referenced.

#### Constructors, copy, and assignment <a id="vector.cons">[[vector.cons]]</a>

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
access categories. It makes order `N` calls to the copy constructor of
`T` and order log N reallocations if they are just input iterators.

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

*Complexity:* It does not change the size of the sequence and takes at
most linear time in the size of the sequence.

*Throws:* `length_error` if `n > max_size()`.[^4]

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
constexpr iterator insert(const_iterator position, initializer_list<T>);

template<class... Args> constexpr reference emplace_back(Args&&... args);
template<class... Args> constexpr iterator emplace(const_iterator position, Args&&... args);
constexpr void push_back(const T& x);
constexpr void push_back(T&& x);
```

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

*Complexity:* If reallocation happens, linear in the number of elements
of the resulting vector; otherwise, linear in the number of elements
inserted plus the distance to the end of the vector.

``` cpp
constexpr iterator erase(const_iterator position);
constexpr iterator erase(const_iterator first, const_iterator last);
constexpr void pop_back();
```

*Effects:* Invalidates iterators and references at or after the point of
the erase.

*Complexity:* The destructor of `T` is called the number of times equal
to the number of the elements erased, but the assignment operator of `T`
is called the number of times equal to the number of elements in the
vector after the erased elements.

*Throws:* Nothing unless an exception is thrown by the assignment
operator or move assignment operator of `T`.

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

### Class `vector<bool>` <a id="vector.bool">[[vector.bool]]</a>

To optimize space allocation, a specialization of vector for `bool`
elements is provided:

``` cpp
namespace std {
  template<class Allocator>
  class vector<bool, Allocator> {
  public:
    // types
    using value_type             = bool;
    using allocator_type         = Allocator;
    using pointer                = implementation-defined;
    using const_pointer          = implementation-defined;
    using const_reference        = bool;
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
      constexpr reference& operator=(const bool x) noexcept;
      constexpr reference& operator=(const reference& x) noexcept;
      constexpr void flip() noexcept;   // flips the bit
    };

    // construct/copy/destroy
    constexpr vector() : vector(Allocator()) { }
    constexpr explicit vector(const Allocator&);
    constexpr explicit vector(size_type n, const Allocator& = Allocator());
    constexpr vector(size_type n, const bool& value, const Allocator& = Allocator());
    template<class InputIterator>
      constexpr vector(InputIterator first, InputIterator last, const Allocator& = Allocator());
    constexpr vector(const vector& x);
    constexpr vector(vector&& x);
    constexpr vector(const vector&, const Allocator&);
    constexpr vector(vector&&, const Allocator&);
    constexpr vector(initializer_list<bool>, const Allocator& = Allocator()));
    constexpr ~vector();
    constexpr vector& operator=(const vector& x);
    constexpr vector& operator=(vector&& x);
    constexpr vector& operator=(initializer_list<bool>);
    template<class InputIterator>
      constexpr void assign(InputIterator first, InputIterator last);
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
    constexpr void pop_back();
    template<class... Args> constexpr iterator emplace(const_iterator position, Args&&... args);
    constexpr iterator insert(const_iterator position, const bool& x);
    constexpr iterator insert(const_iterator position, size_type n, const bool& x);
    template<class InputIterator>
      constexpr iterator insert(const_iterator position,
                                InputIterator first, InputIterator last);
    constexpr iterator insert(const_iterator position, initializer_list<bool> il);

    constexpr iterator erase(const_iterator position);
    constexpr iterator erase(const_iterator first, const_iterator last);
    constexpr void swap(vector&);
    constexpr static void swap(reference x, reference y) noexcept;
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
set, and `false` otherwise. The assignment operator sets the bit when
the argument is (convertible to) `true` and clears it otherwise. `flip`
reverses the state of the bit.

``` cpp
constexpr void flip() noexcept;
```

*Effects:* Replaces each element in the container with its complement.

``` cpp
constexpr static void swap(reference x, reference y) noexcept;
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
    typename iterator_traits<InputIterator>::value_type::first_type>;   // exposition only
template<class InputIterator>
  using iter-mapped-type =
    typename iterator_traits<InputIterator>::value_type::second_type;   // exposition only
template<class InputIterator>
  using iter-to-alloc-type = pair<
    add_const_t<typename iterator_traits<InputIterator>::value_type::first_type>,
    typename iterator_traits<InputIterator>::value_type::second_type>;  // exposition only
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

A `map` is an associative container that supports unique keys (contains
at most one of each key value) and provides for fast retrieval of values
of another type `T` based on the keys. The `map` class supports
bidirectional iterators.

A `map` meets all of the requirements of a container, of a reversible
container [[container.requirements]], of an associative container
[[associative.reqmts]], and of an allocator-aware container (
[[container.alloc.req]]). A `map` also provides most operations
described in  [[associative.reqmts]] for unique keys. This means that a
`map` supports the `a_uniq` operations in  [[associative.reqmts]] but
not the `a_eq` operations. For a `map<Key,T>` the `key_type` is `Key`
and the `value_type` is `pair<const Key,T>`. Descriptions are provided
here only for operations on `map` that are not described in one of those
tables or for operations where there is additional semantic information.

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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    map(const map& x);
    map(map&& x);
    explicit map(const Allocator&);
    map(const map&, const Allocator&);
    map(map&&, const Allocator&);
    map(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
    template<class InputIterator>
      map(InputIterator first, InputIterator last, const Allocator& a)
        : map(first, last, Compare(), a) { }
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
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

  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
    map(initializer_list<pair<Key, T>>, Compare = Compare(), Allocator = Allocator())
      -> map<Key, T, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    map(InputIterator, InputIterator, Allocator)
      -> map<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
             less<iter-key-type<InputIterator>>, Allocator>;

  template<class Key, class T, class Allocator>
    map(initializer_list<pair<Key, T>>, Allocator) -> map<Key, T, less<Key>, Allocator>;

  // swap
  template<class Key, class T, class Compare, class Allocator>
    void swap(map<Key, T, Compare, Allocator>& x,
              map<Key, T, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
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
sorted using `comp` and otherwise N log N, where N is `last - first`.

#### Element access <a id="map.access">[[map.access]]</a>

``` cpp
mapped_type& operator[](const key_type& x);
```

*Effects:* Equivalent to: `return try_emplace(x).first->second;`

``` cpp
mapped_type& operator[](key_type&& x);
```

*Effects:* Equivalent to: `return try_emplace(move(x)).first->second;`

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
from `k`, `forward<M>(obj)`.

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
from `move(k)`, `forward<M>(obj)`.

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
(possibly containing multiple copies of the same key value) and provides
for fast retrieval of values of another type `T` based on the keys. The
`multimap` class supports bidirectional iterators.

A `multimap` meets all of the requirements of a container and of a
reversible container [[container.requirements]], of an associative
container [[associative.reqmts]], and of an allocator-aware container (
[[container.alloc.req]]). A `multimap` also provides most operations
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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    multimap(const multimap& x);
    multimap(multimap&& x);
    explicit multimap(const Allocator&);
    multimap(const multimap&, const Allocator&);
    multimap(multimap&&, const Allocator&);
    multimap(initializer_list<value_type>,
      const Compare& = Compare(),
      const Allocator& = Allocator());
    template<class InputIterator>
      multimap(InputIterator first, InputIterator last, const Allocator& a)
        : multimap(first, last, Compare(), a) { }
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
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

  template<class Key, class T, class Compare = less<Key>,
           class Allocator = allocator<pair<const Key, T>>>
    multimap(initializer_list<pair<Key, T>>, Compare = Compare(), Allocator = Allocator())
      -> multimap<Key, T, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    multimap(InputIterator, InputIterator, Allocator)
      -> multimap<iter-key-type<InputIterator>, iter-mapped-type<InputIterator>,
                  less<iter-key-type<InputIterator>>, Allocator>;

  template<class Key, class T, class Allocator>
    multimap(initializer_list<pair<Key, T>>, Allocator)
      -> multimap<Key, T, less<Key>, Allocator>;

  // swap
  template<class Key, class T, class Compare, class Allocator>
    void swap(multimap<Key, T, Compare, Allocator>& x,
              multimap<Key, T, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
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
sorted using `comp` and otherwise N log N, where N is `last - first`.

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

A `set` is an associative container that supports unique keys (contains
at most one of each key value) and provides for fast retrieval of the
keys themselves. The `set` class supports bidirectional iterators.

A `set` meets all of the requirements of a container, of a reversible
container [[container.requirements]], of an associative container
[[associative.reqmts]], and of an allocator-aware container (
[[container.alloc.req]]). A `set` also provides most operations
described in  [[associative.reqmts]] for unique keys. This means that a
`set` supports the `a_uniq` operations in  [[associative.reqmts]] but
not the `a_eq` operations. For a `set<Key>` both the `key_type` and
`value_type` are `Key`. Descriptions are provided here only for
operations on `set` that are not described in one of these tables and
for operations where there is additional semantic information.

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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    set(const set& x);
    set(set&& x);
    explicit set(const Allocator&);
    set(const set&, const Allocator&);
    set(set&&, const Allocator&);
    set(initializer_list<value_type>, const Compare& = Compare(),
        const Allocator& = Allocator());
    template<class InputIterator>
      set(InputIterator first, InputIterator last, const Allocator& a)
        : set(first, last, Compare(), a) { }
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    insert_return_type insert(node_type&& nh);
    iterator           insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
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

  template<class Key, class Compare = less<Key>, class Allocator = allocator<Key>>
    set(initializer_list<Key>, Compare = Compare(), Allocator = Allocator())
      -> set<Key, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    set(InputIterator, InputIterator, Allocator)
      -> set<iter-value-type<InputIterator>,
             less<iter-value-type<InputIterator>>, Allocator>;

  template<class Key, class Allocator>
    set(initializer_list<Key>, Allocator) -> set<Key, less<Key>, Allocator>;

  // swap
  template<class Key, class Compare, class Allocator>
    void swap(set<Key, Compare, Allocator>& x,
              set<Key, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
}
```

#### Constructors, copy, and assignment <a id="set.cons">[[set.cons]]</a>

``` cpp
explicit set(const Compare& comp, const Allocator& = Allocator());
```

*Effects:* Constructs an empty `set` using the specified comparison
objects and allocator.

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
sorted using `comp` and otherwise N log N, where N is `last - first`.

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
(possibly contains multiple copies of the same key value) and provides
for fast retrieval of the keys themselves. The `multiset` class supports
bidirectional iterators.

A `multiset` meets all of the requirements of a container, of a
reversible container [[container.requirements]], of an associative
container [[associative.reqmts]], and of an allocator-aware container (
[[container.alloc.req]]). `multiset` also provides most operations
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
    using size_type              = implementation-defined; // see [container.requirements]
    using difference_type        = implementation-defined; // see [container.requirements]
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
    multiset(const multiset& x);
    multiset(multiset&& x);
    explicit multiset(const Allocator&);
    multiset(const multiset&, const Allocator&);
    multiset(multiset&&, const Allocator&);
    multiset(initializer_list<value_type>, const Compare& = Compare(),
             const Allocator& = Allocator());
    template<class InputIterator>
      multiset(InputIterator first, InputIterator last, const Allocator& a)
        : multiset(first, last, Compare(), a) { }
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& x);
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

  template<class Key, class Compare = less<Key>, class Allocator = allocator<Key>>
    multiset(initializer_list<Key>, Compare = Compare(), Allocator = Allocator())
      -> multiset<Key, Compare, Allocator>;

  template<class InputIterator, class Allocator>
    multiset(InputIterator, InputIterator, Allocator)
      -> multiset<iter-value-type<InputIterator>,
                  less<iter-value-type<InputIterator>>, Allocator>;

  template<class Key, class Allocator>
    multiset(initializer_list<Key>, Allocator) -> multiset<Key, less<Key>, Allocator>;

  // swap
  template<class Key, class Compare, class Allocator>
    void swap(multiset<Key, Compare, Allocator>& x,
              multiset<Key, Compare, Allocator>& y)
      noexcept(noexcept(x.swap(y)));
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
sorted using `comp` and otherwise N log N, where N is `last - first`.

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
*iter-mapped-type*, and *iter-to-alloc-type* defined in
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

  template<class K, class T, class H, class P, class A, class Predicate>
    typename unordered_map<K, T, H, P, A>::size_type
      erase_if(unordered_map<K, T, H, P, A>& c, Predicate pred);

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

  template<class K, class H, class P, class A, class Predicate>
    typename unordered_set<K, H, P, A>::size_type
      erase_if(unordered_set<K, H, P, A>& c, Predicate pred);

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

An `unordered_map` meets all of the requirements of a container, of an
unordered associative container, and of an allocator-aware container (
[[container.alloc.req]]). It provides the operations described in the
preceding requirements table for unique keys; that is, an
`unordered_map` supports the `a_uniq` operations in that table, not the
`a_eq` operations. For an `unordered_map<Key, T>` the `key type` is
`Key`, the mapped type is `T`, and the value type is
`pair<const Key, T>`.

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
    using size_type            = implementation-defined; // see [container.requirements]
    using difference_type      = implementation-defined; // see [container.requirements]

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
    unordered_map(const unordered_map&);
    unordered_map(unordered_map&&);
    explicit unordered_map(const Allocator&);
    unordered_map(const unordered_map&, const Allocator&);
    unordered_map(unordered_map&&, const Allocator&);
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
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
    template<class K>
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

  // swap
  template<class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_map<Key, T, Hash, Pred, Alloc>& x,
              unordered_map<Key, T, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));
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
`l`) for the first form, or from the range \[`il.begin()`, `il.end()`)
for the second form. `max_load_factor()` returns `1.0`.

*Complexity:* Average case linear, worst case quadratic.

#### Element access <a id="unord.map.elem">[[unord.map.elem]]</a>

``` cpp
mapped_type& operator[](const key_type& k);
```

*Effects:* Equivalent to: `return try_emplace(k).first->second;`

``` cpp
mapped_type& operator[](key_type&& k);
```

*Effects:* Equivalent to: `return try_emplace(move(k)).first->second;`

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

An `unordered_multimap` meets all of the requirements of a container, of
an unordered associative container, and of an allocator-aware container
([[container.alloc.req]]). It provides the operations described in the
preceding requirements table for equivalent keys; that is, an
`unordered_multimap` supports the `a_eq` operations in that table, not
the `a_uniq` operations. For an `unordered_multimap<Key, T>` the
`key type` is `Key`, the mapped type is `T`, and the value type is
`pair<const Key, T>`.

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
    using size_type            = implementation-defined; // see [container.requirements]
    using difference_type      = implementation-defined; // see [container.requirements]

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
    unordered_multimap(const unordered_multimap&);
    unordered_multimap(unordered_multimap&&);
    explicit unordered_multimap(const Allocator&);
    unordered_multimap(const unordered_multimap&, const Allocator&);
    unordered_multimap(unordered_multimap&&, const Allocator&);
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
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

  // swap
  template<class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_multimap<Key, T, Hash, Pred, Alloc>& x,
              unordered_multimap<Key, T, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));
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
`l`) for the first form, or from the range \[`il.begin()`, `il.end()`)
for the second form. `max_load_factor()` returns `1.0`.

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

An `unordered_set` meets all of the requirements of a container, of an
unordered associative container, and of an allocator-aware container (
[[container.alloc.req]]). It provides the operations described in the
preceding requirements table for unique keys; that is, an
`unordered_set` supports the `a_uniq` operations in that table, not the
`a_eq` operations. For an `unordered_set<Key>` the `key type` and the
value type are both `Key`. The `iterator` and `const_iterator` types are
both constant iterator types. It is unspecified whether they are the
same type.

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
    using size_type            = implementation-defined; // see [container.requirements]
    using difference_type      = implementation-defined; // see [container.requirements]

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
    unordered_set(const unordered_set&);
    unordered_set(unordered_set&&);
    explicit unordered_set(const Allocator&);
    unordered_set(const unordered_set&, const Allocator&);
    unordered_set(unordered_set&&, const Allocator&);
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    insert_return_type insert(node_type&& nh);
    iterator           insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
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

  template<class T, class Allocator>
    unordered_set(initializer_list<T>, typename see below::size_type, Allocator)
      -> unordered_set<T, hash<T>, equal_to<T>, Allocator>;

  template<class T, class Hash, class Allocator>
    unordered_set(initializer_list<T>, typename see below::size_type, Hash, Allocator)
      -> unordered_set<T, Hash, equal_to<T>, Allocator>;

  // swap
  template<class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_set<Key, Hash, Pred, Alloc>& x,
              unordered_set<Key, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));
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
`l`) for the first form, or from the range \[`il.begin()`, `il.end()`)
for the second form. `max_load_factor()` returns `1.0`.

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

An `unordered_multiset` meets all of the requirements of a container, of
an unordered associative container, and of an allocator-aware container
([[container.alloc.req]]). It provides the operations described in the
preceding requirements table for equivalent keys; that is, an
`unordered_multiset` supports the `a_eq` operations in that table, not
the `a_uniq` operations. For an `unordered_multiset<Key>` the `key type`
and the value type are both `Key`. The `iterator` and `const_iterator`
types are both constant iterator types. It is unspecified whether they
are the same type.

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
    using size_type            = implementation-defined; // see [container.requirements]
    using difference_type      = implementation-defined; // see [container.requirements]

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
    unordered_multiset(const unordered_multiset&);
    unordered_multiset(unordered_multiset&&);
    explicit unordered_multiset(const Allocator&);
    unordered_multiset(const unordered_multiset&, const Allocator&);
    unordered_multiset(unordered_multiset&&, const Allocator&);
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
    void insert(initializer_list<value_type>);

    node_type extract(const_iterator position);
    node_type extract(const key_type& x);
    iterator insert(node_type&& nh);
    iterator insert(const_iterator hint, node_type&& nh);

    iterator  erase(iterator position);
    iterator  erase(const_iterator position);
    size_type erase(const key_type& k);
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

  template<class T, class Allocator>
    unordered_multiset(initializer_list<T>, typename see below::size_type, Allocator)
      -> unordered_multiset<T, hash<T>, equal_to<T>, Allocator>;

  template<class T, class Hash, class Allocator>
    unordered_multiset(initializer_list<T>, typename see below::size_type, Hash, Allocator)
      -> unordered_multiset<T, Hash, equal_to<T>, Allocator>;

  // swap
  template<class Key, class Hash, class Pred, class Alloc>
    void swap(unordered_multiset<Key, Hash, Pred, Alloc>& x,
              unordered_multiset<Key, Hash, Pred, Alloc>& y)
      noexcept(noexcept(x.swap(y)));
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
`l`) for the first form, or from the range \[`il.begin()`, `il.end()`)
for the second form. `max_load_factor()` returns `1.0`.

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

The headers `<queue>` and `<stack>` define the container adaptors
`queue`, `priority_queue`, and `stack`.

The container adaptors each take a `Container` template parameter, and
each constructor takes a `Container` reference argument. This container
is copied into the `Container` member of each adaptor. If the container
takes an allocator, then a compatible allocator may be passed in to the
adaptor’s constructor. Otherwise, normal copy or move construction is
used for the container argument. The first template parameter `T` of the
container adaptors shall denote the same type as
`Container::value_type`.

For container adaptors, no `swap` function throws an exception unless
that exception is thrown by the swap of the adaptor’s `Container` or
`Compare` object (if any).

A deduction guide for a container adaptor shall not participate in
overload resolution if any of the following are true:

- It has an `InputIterator` template parameter and a type that does not
  qualify as an input iterator is deduced for that parameter.
- It has a `Compare` template parameter and a type that qualifies as an
  allocator is deduced for that parameter.
- It has a `Container` template parameter and a type that qualifies as
  an allocator is deduced for that parameter.
- It has an `Allocator` template parameter and a type that does not
  qualify as an allocator is deduced for that parameter.
- It has both `Container` and `Allocator` template parameters, and
  `uses_allocator_v<Container, Allocator>` is `false`.

### Header `<queue>` synopsis <a id="queue.syn">[[queue.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
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
    template<class Alloc> explicit queue(const Alloc&);
    template<class Alloc> queue(const Container&, const Alloc&);
    template<class Alloc> queue(Container&&, const Alloc&);
    template<class Alloc> queue(const queue&, const Alloc&);
    template<class Alloc> queue(queue&&, const Alloc&);

    [[nodiscard]] bool empty() const    { return c.empty(); }
    size_type         size()  const     { return c.size(); }
    reference         front()           { return c.front(); }
    const_reference   front() const     { return c.front(); }
    reference         back()            { return c.back(); }
    const_reference   back() const      { return c.back(); }
    void push(const value_type& x)      { c.push_back(x); }
    void push(value_type&& x)           { c.push_back(std::move(x)); }
    template<class... Args>
      decltype(auto) emplace(Args&&... args)
        { return c.emplace_back(std::forward<Args>(args)...); }
    void pop()                          { c.pop_front(); }
    void swap(queue& q) noexcept(is_nothrow_swappable_v<Container>)
      { using std::swap; swap(c, q.c); }
  };

  template<class Container>
    queue(Container) -> queue<typename Container::value_type, Container>;

  template<class Container, class Allocator>
    queue(Container, Allocator) -> queue<typename Container::value_type, Container>;

  template<class T, class Container>
    void swap(queue<T, Container>& x, queue<T, Container>& y) noexcept(noexcept(x.swap(y)));

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
      priority_queue(InputIterator first, InputIterator last, const Compare& x,
                     const Container&);
    template<class InputIterator>
      priority_queue(InputIterator first, InputIterator last,
                     const Compare& x = Compare(), Container&& = Container());
    template<class Alloc> explicit priority_queue(const Alloc&);
    template<class Alloc> priority_queue(const Compare&, const Alloc&);
    template<class Alloc> priority_queue(const Compare&, const Container&, const Alloc&);
    template<class Alloc> priority_queue(const Compare&, Container&&, const Alloc&);
    template<class Alloc> priority_queue(const priority_queue&, const Alloc&);
    template<class Alloc> priority_queue(priority_queue&&, const Alloc&);

    [[nodiscard]] bool empty() const { return c.empty(); }
    size_type size()  const          { return c.size(); }
    const_reference   top() const    { return c.front(); }
    void push(const value_type& x);
    void push(value_type&& x);
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
           class Compare = less<typename iterator_traits<InputIterator>::value_type>,
           class Container = vector<typename iterator_traits<InputIterator>::value_type>>
    priority_queue(InputIterator, InputIterator, Compare = Compare(), Container = Container())
      -> priority_queue<typename iterator_traits<InputIterator>::value_type, Container, Compare>;

  template<class Compare, class Container, class Allocator>
    priority_queue(Compare, Container, Allocator)
      -> priority_queue<typename Container::value_type, Container, Compare>;

  // no equality is provided

  template<class T, class Container, class Compare>
    void swap(priority_queue<T, Container, Compare>& x,
              priority_queue<T, Container, Compare>& y) noexcept(noexcept(x.swap(y)));

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
  priority_queue(InputIterator first, InputIterator last, const Compare& x, const Container& y);
template<class InputIterator>
  priority_queue(InputIterator first, InputIterator last, const Compare& x = Compare(),
                 Container&& y = Container());
```

*Preconditions:* `x` defines a strict weak ordering [[alg.sorting]].

*Effects:* Initializes `comp` with `x` and `c` with `y` (copy
constructing or move constructing as appropriate); calls
`c.insert(c.end(), first, last)`; and finally calls
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
    template<class Alloc> explicit stack(const Alloc&);
    template<class Alloc> stack(const Container&, const Alloc&);
    template<class Alloc> stack(Container&&, const Alloc&);
    template<class Alloc> stack(const stack&, const Alloc&);
    template<class Alloc> stack(stack&&, const Alloc&);

    [[nodiscard]] bool empty() const    { return c.empty(); }
    size_type size()  const             { return c.size(); }
    reference         top()             { return c.back(); }
    const_reference   top() const       { return c.back(); }
    void push(const value_type& x)      { c.push_back(x); }
    void push(value_type&& x)           { c.push_back(std::move(x)); }
    template<class... Args>
      decltype(auto) emplace(Args&&... args)
        { return c.emplace_back(std::forward<Args>(args)...); }
    void pop()                          { c.pop_back(); }
    void swap(stack& s) noexcept(is_nothrow_swappable_v<Container>)
      { using std::swap; swap(c, s.c); }
  };

  template<class Container>
    stack(Container) -> stack<typename Container::value_type, Container>;

  template<class Container, class Allocator>
    stack(Container, Allocator) -> stack<typename Container::value_type, Container>;

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

## Views <a id="views">[[views]]</a>

### General <a id="views.general">[[views.general]]</a>

The header `<span>` defines the view `span`.

### Header `<span>` synopsis <a id="span.syn">[[span.syn]]</a>

``` cpp
namespace std {
  // constants
  inline constexpr size_t dynamic_extent = numeric_limits<size_t>::max();

  // [views.span], class template span
  template<class ElementType, size_t Extent = dynamic_extent>
    class span;

  template<class ElementType, size_t Extent>
    inline constexpr bool ranges::enable_view<span<ElementType, Extent>> =
      Extent == 0 || Extent == dynamic_extent;
  template<class ElementType, size_t Extent>
    inline constexpr bool ranges::enable_borrowed_range<span<ElementType, Extent>> = true;

  // [span.objectrep], views of object representation
  template<class ElementType, size_t Extent>
    span<const byte, Extent == dynamic_extent ? dynamic_extent : sizeof(ElementType) * Extent>
      as_bytes(span<ElementType, Extent> s) noexcept;

  template<class ElementType, size_t Extent>
    span<byte, Extent == dynamic_extent ? dynamic_extent : sizeof(ElementType) * Extent>
      as_writable_bytes(span<ElementType, Extent> s) noexcept;
}
```

### Class template `span` <a id="views.span">[[views.span]]</a>

#### Overview <a id="span.overview">[[span.overview]]</a>

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
    using reverse_iterator = std::reverse_iterator<iterator>;
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
    constexpr reverse_iterator rbegin() const noexcept;
    constexpr reverse_iterator rend() const noexcept;

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

`ElementType` is required to be a complete object type that is not an
abstract class type.

#### Constructors, copy, and assignment <a id="span.cons">[[span.cons]]</a>

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

*Effects:* Initializes `data_` with `to_address(first)` and `size_` with
`count`.

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

*Effects:* Initializes `data_` with `to_address(first)` and `size_` with
`last - first`.

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

*Effects:* Initializes `data_` with `ranges::data(r)` and `size_` with
`ranges::size(r)`.

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

#### Deduction guides <a id="span.deduct">[[span.deduct]]</a>

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

#### Subviews <a id="span.sub">[[span.sub]]</a>

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

#### Observers <a id="span.obs">[[span.obs]]</a>

``` cpp
constexpr size_type size() const noexcept;
```

*Effects:* Equivalent to: `return size_;`

``` cpp
constexpr size_type size_bytes() const noexcept;
```

*Effects:* Equivalent to: `return size() * sizeof(element_type);`

``` cpp
[[nodiscard]] constexpr bool empty() const noexcept;
```

*Effects:* Equivalent to: `return size() == 0;`

#### Element access <a id="span.elem">[[span.elem]]</a>

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

*Effects:* Equivalent to: `return data_;`

#### Iterator support <a id="span.iterators">[[span.iterators]]</a>

``` cpp
using iterator = implementation-defined  // type of span::iterator;
```

The type models `contiguous_iterator`[[iterator.concept.contiguous]],
meets the *Cpp17RandomAccessIterator*
requirements [[random.access.iterators]], and meets the requirements for
constexpr iterators [[iterator.requirements.general]]. All requirements
on container iterators [[container.requirements]] apply to
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

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[algorithm.stable]: library.md#algorithm.stable
[algorithms]: algorithms.md#algorithms
[algorithms.requirements]: algorithms.md#algorithms.requirements
[allocator.requirements]: library.md#allocator.requirements
[allocator.requirements.completeness]: library.md#allocator.requirements.completeness
[allocator.traits.members]: utilities.md#allocator.traits.members
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
[associative.set.syn]: #associative.set.syn
[basic.string]: strings.md#basic.string
[class.copy.ctor]: class.md#class.copy.ctor
[class.default.ctor]: class.md#class.default.ctor
[class.dtor]: class.md#class.dtor
[container.adaptors]: #container.adaptors
[container.adaptors.general]: #container.adaptors.general
[container.alloc.req]: #container.alloc.req
[container.assoc.req]: #container.assoc.req
[container.hash.req]: #container.hash.req
[container.insert.return]: #container.insert.return
[container.node]: #container.node
[container.node.compat]: #container.node.compat
[container.node.cons]: #container.node.cons
[container.node.dtor]: #container.node.dtor
[container.node.modifiers]: #container.node.modifiers
[container.node.observers]: #container.node.observers
[container.node.overview]: #container.node.overview
[container.opt]: #container.opt
[container.req]: #container.req
[container.requirements]: #container.requirements
[container.requirements.dataraces]: #container.requirements.dataraces
[container.requirements.general]: #container.requirements.general
[container.rev.req]: #container.rev.req
[container.seq.opt]: #container.seq.opt
[container.seq.req]: #container.seq.req
[containers]: #containers
[containers.general]: #containers.general
[containers.summary]: #containers.summary
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[deque]: #deque
[deque.capacity]: #deque.capacity
[deque.cons]: #deque.cons
[deque.erasure]: #deque.erasure
[deque.modifiers]: #deque.modifiers
[deque.overview]: #deque.overview
[deque.syn]: #deque.syn
[forward.list.erasure]: #forward.list.erasure
[forward.list.syn]: #forward.list.syn
[forwardlist]: #forwardlist
[forwardlist.access]: #forwardlist.access
[forwardlist.cons]: #forwardlist.cons
[forwardlist.iter]: #forwardlist.iter
[forwardlist.modifiers]: #forwardlist.modifiers
[forwardlist.ops]: #forwardlist.ops
[forwardlist.overview]: #forwardlist.overview
[hash.requirements]: library.md#hash.requirements
[iterator.concept.contiguous]: iterators.md#iterator.concept.contiguous
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
[stack.ops]: #stack.ops
[stack.special]: #stack.special
[stack.syn]: #stack.syn
[strings]: strings.md#strings
[swappable.requirements]: library.md#swappable.requirements
[tab:container.opt]: #tab:container.opt
[tab:container.req]: #tab:container.req
[tab:container.rev.req]: #tab:container.rev.req
[tab:container.seq.opt]: #tab:container.seq.opt
[tab:container.seq.req]: #tab:container.seq.req
[temp.deduct]: temp.md#temp.deduct
[temp.param]: temp.md#temp.param
[temp.type]: temp.md#temp.type
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
[unord.set]: #unord.set
[unord.set.cnstr]: #unord.set.cnstr
[unord.set.erasure]: #unord.set.erasure
[unord.set.overview]: #unord.set.overview
[unord.set.syn]: #unord.set.syn
[vector]: #vector
[vector.bool]: #vector.bool
[vector.capacity]: #vector.capacity
[vector.cons]: #vector.cons
[vector.data]: #vector.data
[vector.erasure]: #vector.erasure
[vector.modifiers]: #vector.modifiers
[vector.overview]: #vector.overview
[vector.syn]: #vector.syn
[views]: #views
[views.general]: #views.general
[views.span]: #views.span

[^1]: Equality comparison is a refinement of partitioning if no two
    objects that compare equal fall into different partitions.

[^2]: These member functions are only provided by containers whose
    iterators are random access iterators.

[^3]: As specified in  [[allocator.requirements]], the requirements in
    this Clause apply only to lists whose allocators compare equal.

[^4]: `reserve()` uses `Allocator::allocate()` which may throw an
    appropriate exception.
