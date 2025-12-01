# Atomic operations library <a id="atomics">[[atomics]]</a>

## General <a id="atomics.general">[[atomics.general]]</a>

This Clause describes components for fine-grained atomic access. This
access is provided via operations on atomic objects.

The following subclauses describe atomics requirements and components
for types and operations, as summarized below.

**Table: Atomics library summary** <a id="tab:atomics.lib.summary">[tab:atomics.lib.summary]</a>

| Subclause                    |                            | Header     |
| ---------------------------- | -------------------------- | ---------- |
| [[atomics.order]]            | Order and Consistency      |            |
| [[atomics.lockfree]]         | Lock-free Property         |            |
| [[atomics.types.generic]]    | Atomic Types               | `<atomic>` |
| [[atomics.types.operations]] | Operations on Atomic Types |            |
| [[atomics.flag]]             | Flag Type and Operations   |            |
| [[atomics.fences]]           | Fences                     |            |


## Header `<atomic>` synopsis <a id="atomics.syn">[[atomics.syn]]</a>

``` cpp
namespace std {
  // [atomics.order], order and consistency
  enum memory_order;
  template <class T>
    T kill_dependency(T y) noexcept;

  // [atomics.lockfree], lock-free property
  #define ATOMIC_BOOL_LOCK_FREE unspecified
  #define ATOMIC_CHAR_LOCK_FREE unspecified
  #define ATOMIC_CHAR16_T_LOCK_FREE unspecified
  #define ATOMIC_CHAR32_T_LOCK_FREE unspecified
  #define ATOMIC_WCHAR_T_LOCK_FREE unspecified
  #define ATOMIC_SHORT_LOCK_FREE unspecified
  #define ATOMIC_INT_LOCK_FREE unspecified
  #define ATOMIC_LONG_LOCK_FREE unspecified
  #define ATOMIC_LLONG_LOCK_FREE unspecified
  #define ATOMIC_POINTER_LOCK_FREE unspecified

  // [atomics.types.generic], atomic
  template<class T> struct atomic;
  // [atomics.types.pointer], partial specialization for pointers
  template<class T> struct atomic<T*>;

  // [atomics.nonmembers], non-member functions
  template<class T>
    bool atomic_is_lock_free(const volatile atomic<T>*) noexcept;
  template<class T>
    bool atomic_is_lock_free(const atomic<T>*) noexcept;
  template<class T>
    void atomic_init(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    void atomic_init(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    void atomic_store(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    void atomic_store(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    void atomic_store_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template<class T>
    void atomic_store_explicit(atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template<class T>
    T atomic_load(const volatile atomic<T>*) noexcept;
  template<class T>
    T atomic_load(const atomic<T>*) noexcept;
  template<class T>
    T atomic_load_explicit(const volatile atomic<T>*, memory_order) noexcept;
  template<class T>
    T atomic_load_explicit(const atomic<T>*, memory_order) noexcept;
  template<class T>
    T atomic_exchange(volatile atomic<T>*, T) noexcept;
  template<class T>
    T atomic_exchange(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_exchange_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template<class T>
    T atomic_exchange_explicit(atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template<class T>
    bool atomic_compare_exchange_weak(volatile atomic<T>*,
                                      typename atomic<T>::value_type*,
                                      typename atomic<T>::value_type) noexcept;
  template<class T>
    bool atomic_compare_exchange_weak(atomic<T>*,
                                      typename atomic<T>::value_type*,
                                      typename atomic<T>::value_type) noexcept;
  template<class T>
    bool atomic_compare_exchange_strong(volatile atomic<T>*,
                                        typename atomic<T>::value_type*,
                                        typename atomic<T>::value_type) noexcept;
  template<class T>
    bool atomic_compare_exchange_strong(atomic<T>*,
                                        typename atomic<T>::value_type*,
                                        typename atomic<T>::value_type) noexcept;
  template<class T>
    bool atomic_compare_exchange_weak_explicit(volatile atomic<T>*,
                                               typename atomic<T>::value_type*,
                                               typename atomic<T>::value_type,
                                               memory_order, memory_order) noexcept;
  template<class T>
    bool atomic_compare_exchange_weak_explicit(atomic<T>*,
                                               typename atomic<T>::value_type*,
                                               typename atomic<T>::value_type,
                                               memory_order, memory_order) noexcept;
  template<class T>
    bool atomic_compare_exchange_strong_explicit(volatile atomic<T>*,
                                                 typename atomic<T>::value_type*,
                                                 typename atomic<T>::value_type,
                                                 memory_order, memory_order) noexcept;
  template<class T>
    bool atomic_compare_exchange_strong_explicit(atomic<T>*,
                                                 typename atomic<T>::value_type*,
                                                 typename atomic<T>::value_type,
                                                 memory_order, memory_order) noexcept;

  template <class T>
    T atomic_fetch_add(volatile atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template <class T>
    T atomic_fetch_add(atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template <class T>
    T atomic_fetch_add_explicit(volatile atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_add_explicit(atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_sub(volatile atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template <class T>
    T atomic_fetch_sub(atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template <class T>
    T atomic_fetch_sub_explicit(volatile atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_sub_explicit(atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_and(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template <class T>
    T atomic_fetch_and(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template <class T>
    T atomic_fetch_and_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_and_explicit(atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_or(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template <class T>
    T atomic_fetch_or(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template <class T>
    T atomic_fetch_or_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template <class T>
    T atomic_fetch_or_explicit(atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template <class T>
    T atomic_fetch_xor(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template <class T>
    T atomic_fetch_xor(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template <class T>
    T atomic_fetch_xor_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;
  template <class T>
    T atomic_fetch_xor_explicit(atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;

  // [atomics.types.operations], initialization
  #define ATOMIC_VAR_INIT(value) see below

  // [atomics.alias], type aliases
  using atomic_bool           = atomic<bool>;
  using atomic_char           = atomic<char>;
  using atomic_schar          = atomic<signed char>;
  using atomic_uchar          = atomic<unsigned char>;
  using atomic_short          = atomic<short>;
  using atomic_ushort         = atomic<unsigned short>;
  using atomic_int            = atomic<int>;
  using atomic_uint           = atomic<unsigned int>;
  using atomic_long           = atomic<long>;
  using atomic_ulong          = atomic<unsigned long>;
  using atomic_llong          = atomic<long long>;
  using atomic_ullong         = atomic<unsigned long long>;
  using atomic_char16_t       = atomic<char16_t>;
  using atomic_char32_t       = atomic<char32_t>;
  using atomic_wchar_t        = atomic<wchar_t>;

  using atomic_int8_t         = atomic<int8_t>;
  using atomic_uint8_t        = atomic<uint8_t>;
  using atomic_int16_t        = atomic<int16_t>;
  using atomic_uint16_t       = atomic<uint16_t>;
  using atomic_int32_t        = atomic<int32_t>;
  using atomic_uint32_t       = atomic<uint32_t>;
  using atomic_int64_t        = atomic<int64_t>;
  using atomic_uint64_t       = atomic<uint64_t>;

  using atomic_int_least8_t   = atomic<int_least8_t>;
  using atomic_uint_least8_t  = atomic<uint_least8_t>;
  using atomic_int_least16_t  = atomic<int_least16_t>;
  using atomic_uint_least16_t = atomic<uint_least16_t>;
  using atomic_int_least32_t  = atomic<int_least32_t>;
  using atomic_uint_least32_t = atomic<uint_least32_t>;
  using atomic_int_least64_t  = atomic<int_least64_t>;
  using atomic_uint_least64_t = atomic<uint_least64_t>;

  using atomic_int_fast8_t    = atomic<int_fast8_t>;
  using atomic_uint_fast8_t   = atomic<uint_fast8_t>;
  using atomic_int_fast16_t   = atomic<int_fast16_t>;
  using atomic_uint_fast16_t  = atomic<uint_fast16_t>;
  using atomic_int_fast32_t   = atomic<int_fast32_t>;
  using atomic_uint_fast32_t  = atomic<uint_fast32_t>;
  using atomic_int_fast64_t   = atomic<int_fast64_t>;
  using atomic_uint_fast64_t  = atomic<uint_fast64_t>;

  using atomic_intptr_t       = atomic<intptr_t>;
  using atomic_uintptr_t      = atomic<uintptr_t>;
  using atomic_size_t         = atomic<size_t>;
  using atomic_ptrdiff_t      = atomic<ptrdiff_t>;
  using atomic_intmax_t       = atomic<intmax_t>;
  using atomic_uintmax_t      = atomic<uintmax_t>;

  // [atomics.flag], flag type and operations
  struct atomic_flag;
  bool atomic_flag_test_and_set(volatile atomic_flag*) noexcept;
  bool atomic_flag_test_and_set(atomic_flag*) noexcept;
  bool atomic_flag_test_and_set_explicit(volatile atomic_flag*, memory_order) noexcept;
  bool atomic_flag_test_and_set_explicit(atomic_flag*, memory_order) noexcept;
  void atomic_flag_clear(volatile atomic_flag*) noexcept;
  void atomic_flag_clear(atomic_flag*) noexcept;
  void atomic_flag_clear_explicit(volatile atomic_flag*, memory_order) noexcept;
  void atomic_flag_clear_explicit(atomic_flag*, memory_order) noexcept;
  #define ATOMIC_FLAG_INIT see below

  // [atomics.fences], fences
  extern "C" void atomic_thread_fence(memory_order) noexcept;
  extern "C" void atomic_signal_fence(memory_order) noexcept;
}
```

## Type aliases <a id="atomics.alias">[[atomics.alias]]</a>

## Order and consistency <a id="atomics.order">[[atomics.order]]</a>

``` cpp
namespace std {
  enum memory_order {
    memory_order_relaxed, memory_order_consume, memory_order_acquire,
    memory_order_release, memory_order_acq_rel, memory_order_seq_cst
  };
}
```

The enumeration `memory_order` specifies the detailed regular
(non-atomic) memory synchronization order as defined in
[[intro.multithread]] and may provide for operation ordering. Its
enumerated values and their meanings are as follows:

- `memory_order_relaxed`: no operation orders memory.
- `memory_order_release`, `memory_order_acq_rel`, and
  `memory_order_seq_cst`: a store operation performs a release operation
  on the affected memory location.
- `memory_order_consume`: a load operation performs a consume operation
  on the affected memory location. \[*Note 1*: Prefer
  `memory_order_acquire`, which provides stronger guarantees than
  `memory_order_consume`. Implementations have found it infeasible to
  provide performance better than that of `memory_order_acquire`.
  Specification revisions are under consideration. — *end note*]
- `memory_order_acquire`, `memory_order_acq_rel`, and
  `memory_order_seq_cst`: a load operation performs an acquire operation
  on the affected memory location.

[*Note 2*: Atomic operations specifying `memory_order_relaxed` are
relaxed with respect to memory ordering. Implementations must still
guarantee that any given atomic access to a particular atomic object be
indivisible with respect to all other atomic accesses to that
object. — *end note*]

An atomic operation *A* that performs a release operation on an atomic
object *M* synchronizes with an atomic operation *B* that performs an
acquire operation on *M* and takes its value from any side effect in the
release sequence headed by *A*.

There shall be a single total order *S* on all `memory_order_seq_cst`
operations, consistent with the “happens before” order and modification
orders for all affected locations, such that each `memory_order_seq_cst`
operation *B* that loads a value from an atomic object *M* observes one
of the following values:

- the result of the last modification *A* of *M* that precedes *B* in
  *S*, if it exists, or
- if *A* exists, the result of some modification of *M* that is not
  `memory_order_seq_cst` and that does not happen before *A*, or
- if *A* does not exist, the result of some modification of *M* that is
  not `memory_order_seq_cst`.

[*Note 3*: Although it is not explicitly required that *S* include
locks, it can always be extended to an order that does include lock and
unlock operations, since the ordering between those is already included
in the “happens before” ordering. — *end note*]

For an atomic operation *B* that reads the value of an atomic object
*M*, if there is a `memory_order_seq_cst` fence *X* sequenced before
*B*, then *B* observes either the last `memory_order_seq_cst`
modification of *M* preceding *X* in the total order *S* or a later
modification of *M* in its modification order.

For atomic operations *A* and *B* on an atomic object *M*, where *A*
modifies *M* and *B* takes its value, if there is a
`memory_order_seq_cst` fence *X* such that *A* is sequenced before *X*
and *B* follows *X* in *S*, then *B* observes either the effects of *A*
or a later modification of *M* in its modification order.

For atomic operations *A* and *B* on an atomic object *M*, where *A*
modifies *M* and *B* takes its value, if there are
`memory_order_seq_cst` fences *X* and *Y* such that *A* is sequenced
before *X*, *Y* is sequenced before *B*, and *X* precedes *Y* in *S*,
then *B* observes either the effects of *A* or a later modification of
*M* in its modification order.

For atomic modifications *A* and *B* of an atomic object *M*, *B* occurs
later than *A* in the modification order of *M* if:

- there is a `memory_order_seq_cst` fence *X* such that *A* is sequenced
  before *X*, and *X* precedes *B* in *S*, or
- there is a `memory_order_seq_cst` fence *Y* such that *Y* is sequenced
  before *B*, and *A* precedes *Y* in *S*, or
- there are `memory_order_seq_cst` fences *X* and *Y* such that *A* is
  sequenced before *X*, *Y* is sequenced before *B*, and *X* precedes
  *Y* in *S*.

[*Note 4*: `memory_order_seq_cst` ensures sequential consistency only
for a program that is free of data races and uses exclusively
`memory_order_seq_cst` operations. Any use of weaker ordering will
invalidate this guarantee unless extreme care is used. In particular,
`memory_order_seq_cst` fences ensure a total order only for the fences
themselves. Fences cannot, in general, be used to restore sequential
consistency for atomic operations with weaker ordering
specifications. — *end note*]

Implementations should ensure that no “out-of-thin-air” values are
computed that circularly depend on their own computation.

[*Note 5*:

For example, with `x` and `y` initially zero,

``` cpp
// Thread 1:
r1 = y.load(memory_order_relaxed);
x.store(r1, memory_order_relaxed);
```

``` cpp
// Thread 2:
r2 = x.load(memory_order_relaxed);
y.store(r2, memory_order_relaxed);
```

should not produce `r1 == r2 == 42`, since the store of 42 to `y` is
only possible if the store to `x` stores `42`, which circularly depends
on the store to `y` storing `42`. Note that without this restriction,
such an execution is possible.

— *end note*]

[*Note 6*:

The recommendation similarly disallows `r1 == r2 == 42` in the following
example, with `x` and `y` again initially zero:

``` cpp
// Thread 1:
r1 = x.load(memory_order_relaxed);
if (r1 == 42) y.store(42, memory_order_relaxed);
```

``` cpp
// Thread 2:
r2 = y.load(memory_order_relaxed);
if (r2 == 42) x.store(42, memory_order_relaxed);
```

— *end note*]

Atomic read-modify-write operations shall always read the last value (in
the modification order) written before the write associated with the
read-modify-write operation.

Implementations should make atomic stores visible to atomic loads within
a reasonable amount of time.

``` cpp
template <class T>
  T kill_dependency(T y) noexcept;
```

*Effects:* The argument does not carry a dependency to the return
value ([[intro.multithread]]).

*Returns:* `y`.

## Lock-free property <a id="atomics.lockfree">[[atomics.lockfree]]</a>

``` cpp
#define ATOMIC_BOOL_LOCK_FREE unspecified
#define ATOMIC_CHAR_LOCK_FREE unspecified
#define ATOMIC_CHAR16_T_LOCK_FREE unspecified
#define ATOMIC_CHAR32_T_LOCK_FREE unspecified
#define ATOMIC_WCHAR_T_LOCK_FREE unspecified
#define ATOMIC_SHORT_LOCK_FREE unspecified
#define ATOMIC_INT_LOCK_FREE unspecified
#define ATOMIC_LONG_LOCK_FREE unspecified
#define ATOMIC_LLONG_LOCK_FREE unspecified
#define ATOMIC_POINTER_LOCK_FREE unspecified
```

The `ATOMIC_..._LOCK_FREE` macros indicate the lock-free property of the
corresponding atomic types, with the signed and unsigned variants
grouped together. The properties also apply to the corresponding
(partial) specializations of the `atomic` template. A value of 0
indicates that the types are never lock-free. A value of 1 indicates
that the types are sometimes lock-free. A value of 2 indicates that the
types are always lock-free.

The function `atomic_is_lock_free` ([[atomics.types.operations]])
indicates whether the object is lock-free. In any given program
execution, the result of the lock-free query shall be consistent for all
pointers of the same type.

Atomic operations that are not lock-free are considered to potentially
block ([[intro.progress]]).

[*Note 1*: Operations that are lock-free should also be address-free.
That is, atomic operations on the same memory location via two different
addresses will communicate atomically. The implementation should not
depend on any per-process state. This restriction enables communication
by memory that is mapped into a process more than once and by memory
that is shared between two processes. — *end note*]

## Class template `atomic` <a id="atomics.types.generic">[[atomics.types.generic]]</a>

``` cpp
namespace std {
  template <class T> struct atomic {
    using value_type = T;
    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;
    void store(T, memory_order = memory_order_seq_cst) volatile noexcept;
    void store(T, memory_order = memory_order_seq_cst) noexcept;
    T load(memory_order = memory_order_seq_cst) const volatile noexcept;
    T load(memory_order = memory_order_seq_cst) const noexcept;
    operator T() const volatile noexcept;
    operator T() const noexcept;
    T exchange(T, memory_order = memory_order_seq_cst) volatile noexcept;
    T exchange(T, memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_weak(T&, T, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(T&, T, memory_order, memory_order) noexcept;
    bool compare_exchange_strong(T&, T, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(T&, T, memory_order, memory_order) noexcept;
    bool compare_exchange_weak(T&, T, memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_weak(T&, T, memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_strong(T&, T, memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_strong(T&, T, memory_order = memory_order_seq_cst) noexcept;

    atomic() noexcept = default;
    constexpr atomic(T) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;
    T operator=(T) volatile noexcept;
    T operator=(T) noexcept;
  };
}
```

The template argument for `T` shall be trivially copyable (
[[basic.types]]).

[*Note 1*: Type arguments that are not also statically initializable
may be difficult to use. — *end note*]

The specialization `atomic<bool>` is a standard-layout struct.

[*Note 2*: The representation of an atomic specialization need not have
the same size as its corresponding argument type. Specializations should
have the same size whenever possible, as this reduces the effort
required to port existing code. — *end note*]

### Operations on atomic types <a id="atomics.types.operations">[[atomics.types.operations]]</a>

[*Note 1*: Many operations are volatile-qualified. The “volatile as
device register” semantics have not changed in the standard. This
qualification means that volatility is preserved when applying these
operations to volatile objects. It does not mean that operations on
non-volatile objects become volatile. — *end note*]

``` cpp
atomic() noexcept = default;
```

*Effects:* Leaves the atomic object in an uninitialized state.

[*Note 1*: These semantics ensure compatibility with C. — *end note*]

``` cpp
constexpr atomic(T desired) noexcept;
```

*Effects:* Initializes the object with the value `desired`.
Initialization is not an atomic operation ([[intro.multithread]]).

[*Note 2*: It is possible to have an access to an atomic object `A`
race with its construction, for example by communicating the address of
the just-constructed object `A` to another thread via
`memory_order_relaxed` operations on a suitable atomic pointer variable,
and then immediately accessing `A` in the receiving thread. This results
in undefined behavior. — *end note*]

``` cpp
#define ATOMIC_VAR_INIT(value) see below
```

The macro expands to a token sequence suitable for constant
initialization of an atomic variable of static storage duration of a
type that is initialization-compatible with `value`.

[*Note 3*: This operation may need to initialize locks. — *end note*]

Concurrent access to the variable being initialized, even via an atomic
operation, constitutes a data race.

[*Example 1*:

``` cpp
atomic<int> v = ATOMIC_VAR_INIT(5);
```

— *end example*]

``` cpp
static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
```

The `static` data member `is_always_lock_free` is `true` if the atomic
type’s operations are always lock-free, and `false` otherwise.

[*Note 4*: The value of `is_always_lock_free` is consistent with the
value of the corresponding `ATOMIC_..._LOCK_FREE` macro, if
defined. — *end note*]

``` cpp
bool is_lock_free() const volatile noexcept;
bool is_lock_free() const noexcept;
```

*Returns:* `true` if the object’s operations are lock-free, `false`
otherwise.

[*Note 5*: The return value of the `is_lock_free` member function is
consistent with the value of `is_always_lock_free` for the same
type. — *end note*]

``` cpp
void store(T desired, memory_order order = memory_order_seq_cst) volatile noexcept;
void store(T desired, memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* The `order` argument shall not be `memory_order_consume`,
`memory_order_acquire`, nor `memory_order_acq_rel`.

*Effects:* Atomically replaces the value pointed to by `this` with the
value of `desired`. Memory is affected according to the value of
`order`.

``` cpp
T operator=(T desired) volatile noexcept;
T operator=(T desired) noexcept;
```

*Effects:* Equivalent to: `store(desired)`.

*Returns:* `desired`.

``` cpp
T load(memory_order order = memory_order_seq_cst) const volatile noexcept;
T load(memory_order order = memory_order_seq_cst) const noexcept;
```

*Requires:* The `order` argument shall not be `memory_order_release` nor
`memory_order_acq_rel`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns the value pointed to by `this`.

``` cpp
operator T() const volatile noexcept;
operator T() const noexcept;
```

*Effects:* Equivalent to: `return load();`

``` cpp
T exchange(T desired, memory_order order = memory_order_seq_cst) volatile noexcept;
T exchange(T desired, memory_order order = memory_order_seq_cst) noexcept;
```

*Effects:* Atomically replaces the value pointed to by `this` with
`desired`. Memory is affected according to the value of `order`. These
operations are atomic read-modify-write
operations ([[intro.multithread]]).

*Returns:* Atomically returns the value pointed to by `this` immediately
before the effects.

``` cpp
bool compare_exchange_weak(T& expected, T desired,
                           memory_order success, memory_order failure) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order success, memory_order failure) noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order success, memory_order failure) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order success, memory_order failure) noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order order = memory_order_seq_cst) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order order = memory_order_seq_cst) noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order_seq_cst) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* The `failure` argument shall not be `memory_order_release`
nor `memory_order_acq_rel`.

*Effects:* Retrieves the value in `expected`. It then atomically
compares the contents of the memory pointed to by `this` for equality
with that previously retrieved from `expected`, and if true, replaces
the contents of the memory pointed to by `this` with that in `desired`.
If and only if the comparison is true, memory is affected according to
the value of `success`, and if the comparison is false, memory is
affected according to the value of `failure`. When only one
`memory_order` argument is supplied, the value of `success` is `order`,
and the value of `failure` is `order` except that a value of
`memory_order_acq_rel` shall be replaced by the value
`memory_order_acquire` and a value of `memory_order_release` shall be
replaced by the value `memory_order_relaxed`. If and only if the
comparison is false then, after the atomic operation, the contents of
the memory in `expected` are replaced by the value read from the memory
pointed to by `this` during the atomic comparison. If the operation
returns `true`, these operations are atomic read-modify-write
operations ([[intro.multithread]]) on the memory pointed to by `this`.
Otherwise, these operations are atomic load operations on that memory.

*Returns:* The result of the comparison.

[*Note 6*:

For example, the effect of `compare_exchange_strong` is

``` cpp
if (memcmp(this, &expected, sizeof(*this)) == 0)
  memcpy(this, &desired, sizeof(*this));
else
  memcpy(expected, this, sizeof(*this));
```

— *end note*]

[*Example 2*:

The expected use of the compare-and-exchange operations is as follows.
The compare-and-exchange operations will update `expected` when another
iteration of the loop is needed.

``` cpp
expected = current.load();
do {
  desired = function(expected);
} while (!current.compare_exchange_weak(expected, desired));
```

— *end example*]

[*Example 3*:

Because the expected value is updated only on failure, code releasing
the memory containing the `expected` value on success will work. E.g.
list head insertion will act atomically and would not introduce a data
race in the following code:

``` cpp
do {
  p->next = head; // make new list node point to the current head
} while (!head.compare_exchange_weak(p->next, p)); // try to insert
```

— *end example*]

Implementations should ensure that weak compare-and-exchange operations
do not consistently return `false` unless either the atomic object has
value different from `expected` or there are concurrent modifications to
the atomic object.

*Remarks:* A weak compare-and-exchange operation may fail spuriously.
That is, even when the contents of memory referred to by `expected` and
`this` are equal, it may return `false` and store back to `expected` the
same memory contents that were originally there.

[*Note 7*: This spurious failure enables implementation of
compare-and-exchange on a broader class of machines, e.g., load-locked
store-conditional machines. A consequence of spurious failure is that
nearly all uses of weak compare-and-exchange will be in a loop. When a
compare-and-exchange is in a loop, the weak version will yield better
performance on some platforms. When a weak compare-and-exchange would
require a loop and a strong one would not, the strong one is
preferable. — *end note*]

[*Note 8*: The `memcpy` and `memcmp` semantics of the
compare-and-exchange operations may result in failed comparisons for
values that compare equal with `operator==` if the underlying type has
padding bits, trap bits, or alternate representations of the same value.
Thus, `compare_exchange_strong` should be used with extreme care. On the
other hand, `compare_exchange_weak` should converge
rapidly. — *end note*]

### Specializations for integers <a id="atomics.types.int">[[atomics.types.int]]</a>

There are specializations of the `atomic` template for the integral
types `char`, `signed char`, `unsigned char`, `short`, `unsigned short`,
`int`, `unsigned int`, `long`, `unsigned long`, `long long`,
`unsigned long long`, `char16_t`, `char32_t`, `wchar_t`, and any other
types needed by the typedefs in the header `<cstdint>`. For each such
integral type `integral`, the specialization `atomic<integral>` provides
additional atomic operations appropriate to integral types.

[*Note 1*: For the specialization `atomic<bool>`, see
[[atomics.types.generic]]. — *end note*]

``` cpp
namespace std {
  template <> struct atomic<integral> {
    using value_type = integral;
    using difference_type = value_type;
    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;
    void store(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    void store(integral, memory_order = memory_order_seq_cst) noexcept;
    integral load(memory_order = memory_order_seq_cst) const volatile noexcept;
    integral load(memory_order = memory_order_seq_cst) const noexcept;
    operator integral() const volatile noexcept;
    operator integral() const noexcept;
    integral exchange(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    integral exchange(integral, memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order, memory_order) noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order, memory_order) noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_strong(integral&, integral,
                               memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_strong(integral&, integral,
                               memory_order = memory_order_seq_cst) noexcept;
    integral fetch_add(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    integral fetch_add(integral, memory_order = memory_order_seq_cst) noexcept;
    integral fetch_sub(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    integral fetch_sub(integral, memory_order = memory_order_seq_cst) noexcept;
    integral fetch_and(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    integral fetch_and(integral, memory_order = memory_order_seq_cst) noexcept;
    integral fetch_or(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    integral fetch_or(integral, memory_order = memory_order_seq_cst) noexcept;
    integral fetch_xor(integral, memory_order = memory_order_seq_cst) volatile noexcept;
    integral fetch_xor(integral, memory_order = memory_order_seq_cst) noexcept;

    atomic() noexcept = default;
    constexpr atomic(integral) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;
    integral operator=(integral) volatile noexcept;
    integral operator=(integral) noexcept;

    integral operator++(int) volatile noexcept;
    integral operator++(int) noexcept;
    integral operator--(int) volatile noexcept;
    integral operator--(int) noexcept;
    integral operator++() volatile noexcept;
    integral operator++() noexcept;
    integral operator--() volatile noexcept;
    integral operator--() noexcept;
    integral operator+=(integral) volatile noexcept;
    integral operator+=(integral) noexcept;
    integral operator-=(integral) volatile noexcept;
    integral operator-=(integral) noexcept;
    integral operator&=(integral) volatile noexcept;
    integral operator&=(integral) noexcept;
    integral operator|=(integral) volatile noexcept;
    integral operator|=(integral) noexcept;
    integral operator^=(integral) volatile noexcept;
    integral operator^=(integral) noexcept;
  };
}
```

The atomic integral specializations are standard-layout structs. They
each have a trivial default constructor and a trivial destructor.

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform arithmetic computations. The key,
operator, and computation correspondence is:

**Table: Atomic arithmetic computations** <a id="tab:atomic.arithmetic.computations">[tab:atomic.arithmetic.computations]</a>

| Op  | Computation |
| --- | ----------- |
| `add` | `+`         | addition | `sub` | `-` | subtraction |
| `or` | `|`         | bitwise inclusive or | `xor` | `^` | bitwise exclusive or |
| `and` | `&`         | bitwise and |     |     |     |

``` cpp
T fetch_key(T operand, memory_order order = memory_order_seq_cst) volatile noexcept;
T fetch_key(T operand, memory_order order = memory_order_seq_cst) noexcept;
```

*Effects:* Atomically replaces the value pointed to by `this` with the
result of the computation applied to the value pointed to by `this` and
the given `operand`. Memory is affected according to the value of
`order`. These operations are atomic read-modify-write
operations ([[intro.multithread]]).

*Returns:* Atomically, the value pointed to by `this` immediately before
the effects.

*Remarks:* For signed integer types, arithmetic is defined to use two’s
complement representation. There are no undefined results.

``` cpp
T operator op=(T operand) volatile noexcept;
T operator op=(T operand) noexcept;
```

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Partial specialization for pointers <a id="atomics.types.pointer">[[atomics.types.pointer]]</a>

``` cpp
namespace std {
  template <class T> struct atomic<T*> {
    using value_type = T*;
    using difference_type = ptrdiff_t;
    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;
    void store(T*, memory_order = memory_order_seq_cst) volatile noexcept;
    void store(T*, memory_order = memory_order_seq_cst) noexcept;
    T* load(memory_order = memory_order_seq_cst) const volatile noexcept;
    T* load(memory_order = memory_order_seq_cst) const noexcept;
    operator T*() const volatile noexcept;
    operator T*() const noexcept;
    T* exchange(T*, memory_order = memory_order_seq_cst) volatile noexcept;
    T* exchange(T*, memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_weak(T*&, T*, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(T*&, T*, memory_order, memory_order) noexcept;
    bool compare_exchange_strong(T*&, T*, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(T*&, T*, memory_order, memory_order) noexcept;
    bool compare_exchange_weak(T*&, T*, memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_weak(T*&, T*, memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_strong(T*&, T*, memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_strong(T*&, T*, memory_order = memory_order_seq_cst) noexcept;
    T* fetch_add(ptrdiff_t, memory_order = memory_order_seq_cst) volatile noexcept;
    T* fetch_add(ptrdiff_t, memory_order = memory_order_seq_cst) noexcept;
    T* fetch_sub(ptrdiff_t, memory_order = memory_order_seq_cst) volatile noexcept;
    T* fetch_sub(ptrdiff_t, memory_order = memory_order_seq_cst) noexcept;

    atomic() noexcept = default;
    constexpr atomic(T*) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;
    T* operator=(T*) volatile noexcept;
    T* operator=(T*) noexcept;

    T* operator++(int) volatile noexcept;
    T* operator++(int) noexcept;
    T* operator--(int) volatile noexcept;
    T* operator--(int) noexcept;
    T* operator++() volatile noexcept;
    T* operator++() noexcept;
    T* operator--() volatile noexcept;
    T* operator--() noexcept;
    T* operator+=(ptrdiff_t) volatile noexcept;
    T* operator+=(ptrdiff_t) noexcept;
    T* operator-=(ptrdiff_t) volatile noexcept;
    T* operator-=(ptrdiff_t) noexcept;
  };
}
```

There is a partial specialization of the `atomic` class template for
pointers. Specializations of this partial specialization are
standard-layout structs. They each have a trivial default constructor
and a trivial destructor.

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform pointer arithmetic. The key, operator,
and computation correspondence is:

**Table: Atomic pointer computations** <a id="tab:atomic.pointer.computations">[tab:atomic.pointer.computations]</a>

|       |     |          |       |     |             |
| ----- | --- | -------- | ----- | --- | ----------- |
| `add` | `+` | addition | `sub` | `-` | subtraction |

``` cpp
T* fetch_key(ptrdiff_t operand, memory_order order = memory_order_seq_cst) volatile noexcept;
T* fetch_key(ptrdiff_t operand, memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* T shall be an object type, otherwise the program is
ill-formed.

[*Note 1*: Pointer arithmetic on `void*` or function pointers is
ill-formed. — *end note*]

*Effects:* Atomically replaces the value pointed to by `this` with the
result of the computation applied to the value pointed to by `this` and
the given `operand`. Memory is affected according to the value of
`order`. These operations are atomic read-modify-write
operations ([[intro.multithread]]).

*Returns:* Atomically, the value pointed to by `this` immediately before
the effects.

*Remarks:* The result may be an undefined address, but the operations
otherwise have no undefined behavior.

``` cpp
T* operator op=(ptrdiff_t operand) volatile noexcept;
T* operator op=(ptrdiff_t operand) noexcept;
```

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Member operators common to integers and pointers to objects <a id="atomics.types.memop">[[atomics.types.memop]]</a>

``` cpp
T operator++(int) volatile noexcept;
T operator++(int) noexcept;
```

*Effects:* Equivalent to: `return fetch_add(1);`

``` cpp
T operator--(int) volatile noexcept;
T operator--(int) noexcept;
```

*Effects:* Equivalent to: `return fetch_sub(1);`

``` cpp
T operator++() volatile noexcept;
T operator++() noexcept;
```

*Effects:* Equivalent to: `return fetch_add(1) + 1;`

``` cpp
T operator--() volatile noexcept;
T operator--() noexcept;
```

*Effects:* Equivalent to: `return fetch_sub(1) - 1;`

## Non-member functions <a id="atomics.nonmembers">[[atomics.nonmembers]]</a>

A non-member function template whose name matches the pattern `atomic_f`
or the pattern `atomic_f_explicit` invokes the member function `f`, with
the value of the first parameter as the object expression and the values
of the remaining parameters (if any) as the arguments of the member
function call, in order. An argument for a parameter of type
`atomic<T>::value_type*` is dereferenced when passed to the member
function call. If no such member function exists, the program is
ill-formed.

``` cpp
template<class T>
  void atomic_init(volatile atomic<T>* object, typename atomic<T>::value_type desired) noexcept;
template<class T>
  void atomic_init(atomic<T>* object, typename atomic<T>::value_type desired) noexcept;
```

*Effects:* Non-atomically initializes `*object` with value `desired`.
This function shall only be applied to objects that have been default
constructed, and then only once.

[*Note 1*: These semantics ensure compatibility with C. — *end note*]

[*Note 2*: Concurrent access from another thread, even via an atomic
operation, constitutes a data race. — *end note*]

[*Note 1*: The non-member functions enable programmers to write code
that can be compiled as either C or C++, for example in a shared header
file. — *end note*]

## Flag type and operations <a id="atomics.flag">[[atomics.flag]]</a>

``` cpp
namespace std {
  struct atomic_flag {
    bool test_and_set(memory_order = memory_order_seq_cst) volatile noexcept;
    bool test_and_set(memory_order = memory_order_seq_cst) noexcept;
    void clear(memory_order = memory_order_seq_cst) volatile noexcept;
    void clear(memory_order = memory_order_seq_cst) noexcept;

    atomic_flag() noexcept = default;
    atomic_flag(const atomic_flag&) = delete;
    atomic_flag& operator=(const atomic_flag&) = delete;
    atomic_flag& operator=(const atomic_flag&) volatile = delete;
  };

  bool atomic_flag_test_and_set(volatile atomic_flag*) noexcept;
  bool atomic_flag_test_and_set(atomic_flag*) noexcept;
  bool atomic_flag_test_and_set_explicit(volatile atomic_flag*, memory_order) noexcept;
  bool atomic_flag_test_and_set_explicit(atomic_flag*, memory_order) noexcept;
  void atomic_flag_clear(volatile atomic_flag*) noexcept;
  void atomic_flag_clear(atomic_flag*) noexcept;
  void atomic_flag_clear_explicit(volatile atomic_flag*, memory_order) noexcept;
  void atomic_flag_clear_explicit(atomic_flag*, memory_order) noexcept;

  #define ATOMIC_FLAG_INIT see below
}
```

The `atomic_flag` type provides the classic test-and-set functionality.
It has two states, set and clear.

Operations on an object of type `atomic_flag` shall be lock-free.

[*Note 1*: Hence the operations should also be
address-free. — *end note*]

The `atomic_flag` type is a standard-layout struct. It has a trivial
default constructor and a trivial destructor.

The macro `ATOMIC_FLAG_INIT` shall be defined in such a way that it can
be used to initialize an object of type `atomic_flag` to the clear
state. The macro can be used in the form:

``` cpp
atomic_flag guard = ATOMIC_FLAG_INIT;
```

It is unspecified whether the macro can be used in other initialization
contexts. For a complete static-duration object, that initialization
shall be static. Unless initialized with `ATOMIC_FLAG_INIT`, it is
unspecified whether an `atomic_flag` object has an initial state of set
or clear.

``` cpp
bool atomic_flag_test_and_set(volatile atomic_flag* object) noexcept;
bool atomic_flag_test_and_set(atomic_flag* object) noexcept;
bool atomic_flag_test_and_set_explicit(volatile atomic_flag* object, memory_order order) noexcept;
bool atomic_flag_test_and_set_explicit(atomic_flag* object, memory_order order) noexcept;
bool atomic_flag::test_and_set(memory_order order = memory_order_seq_cst) volatile noexcept;
bool atomic_flag::test_and_set(memory_order order = memory_order_seq_cst) noexcept;
```

*Effects:* Atomically sets the value pointed to by `object` or by `this`
to `true`. Memory is affected according to the value of `order`. These
operations are atomic read-modify-write
operations ([[intro.multithread]]).

*Returns:* Atomically, the value of the object immediately before the
effects.

``` cpp
void atomic_flag_clear(volatile atomic_flag* object) noexcept;
void atomic_flag_clear(atomic_flag* object) noexcept;
void atomic_flag_clear_explicit(volatile atomic_flag* object, memory_order order) noexcept;
void atomic_flag_clear_explicit(atomic_flag* object, memory_order order) noexcept;
void atomic_flag::clear(memory_order order = memory_order_seq_cst) volatile noexcept;
void atomic_flag::clear(memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* The `order` argument shall not be `memory_order_consume`,
`memory_order_acquire`, nor `memory_order_acq_rel`.

*Effects:* Atomically sets the value pointed to by `object` or by `this`
to `false`. Memory is affected according to the value of `order`.

## Fences <a id="atomics.fences">[[atomics.fences]]</a>

This section introduces synchronization primitives called *fences*.
Fences can have acquire semantics, release semantics, or both. A fence
with acquire semantics is called an *acquire fence*. A fence with
release semantics is called a *release fence*.

A release fence *A* synchronizes with an acquire fence *B* if there
exist atomic operations *X* and *Y*, both operating on some atomic
object *M*, such that *A* is sequenced before *X*, *X* modifies *M*, *Y*
is sequenced before *B*, and *Y* reads the value written by *X* or a
value written by any side effect in the hypothetical release sequence
*X* would head if it were a release operation.

A release fence *A* synchronizes with an atomic operation *B* that
performs an acquire operation on an atomic object *M* if there exists an
atomic operation *X* such that *A* is sequenced before *X*, *X* modifies
*M*, and *B* reads the value written by *X* or a value written by any
side effect in the hypothetical release sequence *X* would head if it
were a release operation.

An atomic operation *A* that is a release operation on an atomic object
*M* synchronizes with an acquire fence *B* if there exists some atomic
operation *X* on *M* such that *X* is sequenced before *B* and reads the
value written by *A* or a value written by any side effect in the
release sequence headed by *A*.

``` cpp
extern "C" void atomic_thread_fence(memory_order order) noexcept;
```

*Effects:* Depending on the value of `order`, this operation:

- has no effects, if `order == memory_order_relaxed`;
- is an acquire fence, if
  `order == memory_order_acquire || order == memory_order_consume`;
- is a release fence, if `order == memory_order_release`;
- is both an acquire fence and a release fence, if
  `order == memory_order_acq_rel`;
- is a sequentially consistent acquire and release fence, if
  `order == memory_order_seq_cst`.

``` cpp
extern "C" void atomic_signal_fence(memory_order order) noexcept;
```

*Effects:* Equivalent to `atomic_thread_fence(order)`, except that the
resulting ordering constraints are established only between a thread and
a signal handler executed in the same thread.

[*Note 1*: `atomic_signal_fence` can be used to specify the order in
which actions performed by the thread become visible to the signal
handler. Compiler optimizations and reorderings of loads and stores are
inhibited in the same way as with `atomic_thread_fence`, but the
hardware fence instructions that `atomic_thread_fence` would have
inserted are not emitted. — *end note*]

<!-- Link reference definitions -->
[atomics]: #atomics
[atomics.alias]: #atomics.alias
[atomics.fences]: #atomics.fences
[atomics.flag]: #atomics.flag
[atomics.general]: #atomics.general
[atomics.lockfree]: #atomics.lockfree
[atomics.nonmembers]: #atomics.nonmembers
[atomics.order]: #atomics.order
[atomics.syn]: #atomics.syn
[atomics.types.generic]: #atomics.types.generic
[atomics.types.int]: #atomics.types.int
[atomics.types.memop]: #atomics.types.memop
[atomics.types.operations]: #atomics.types.operations
[atomics.types.pointer]: #atomics.types.pointer
[basic.types]: basic.md#basic.types
[intro.multithread]: intro.md#intro.multithread
[intro.progress]: intro.md#intro.progress
