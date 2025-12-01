# Atomic operations library <a id="atomics">[[atomics]]</a>

## General <a id="atomics.general">[[atomics.general]]</a>

This Clause describes components for fine-grained atomic access. This
access is provided via operations on atomic objects.

The following subclauses describe atomics requirements and components
for types and operations, as summarized in [[atomics.summary]].

**Table: Atomics library summary** <a id="atomics.summary">[atomics.summary]</a>

| Subclause                 |                             | Header     |
| ------------------------- | --------------------------- | ---------- |
| [[atomics.alias]]         | Type aliases                | `<atomic>` |
| [[atomics.order]]         | Order and consistency       |            |
| [[atomics.lockfree]]      | Lock-free property          |            |
| [[atomics.wait]]          | Waiting and notifying       |            |
| [[atomics.ref.generic]]   | Class template `atomic_ref` |            |
| [[atomics.types.generic]] | Class template `atomic`     |            |
| [[atomics.nonmembers]]    | Non-member functions        |            |
| [[atomics.flag]]          | Flag type and operations    |            |
| [[atomics.fences]]        | Fences                      |            |


## Header `<atomic>` synopsis <a id="atomics.syn">[[atomics.syn]]</a>

``` cpp
namespace std {
  // [atomics.order], order and consistency
  enum class memory_order : unspecified;
  template<class T>
    T kill_dependency(T y) noexcept;

  // [atomics.lockfree], lock-free property
  #define ATOMIC_BOOL_LOCK_FREE unspecified
  #define ATOMIC_CHAR_LOCK_FREE unspecified
  #define ATOMIC_CHAR8_T_LOCK_FREE unspecified
  #define ATOMIC_CHAR16_T_LOCK_FREE unspecified
  #define ATOMIC_CHAR32_T_LOCK_FREE unspecified
  #define ATOMIC_WCHAR_T_LOCK_FREE unspecified
  #define ATOMIC_SHORT_LOCK_FREE unspecified
  #define ATOMIC_INT_LOCK_FREE unspecified
  #define ATOMIC_LONG_LOCK_FREE unspecified
  #define ATOMIC_LLONG_LOCK_FREE unspecified
  #define ATOMIC_POINTER_LOCK_FREE unspecified

  // [atomics.ref.generic], class template atomic_ref
  template<class T> struct atomic_ref;
  // [atomics.ref.pointer], partial specialization for pointers
  template<class T> struct atomic_ref<T*>;

  // [atomics.types.generic], class template atomic
  template<class T> struct atomic;
  // [atomics.types.pointer], partial specialization for pointers
  template<class T> struct atomic<T*>;

  // [atomics.nonmembers], non-member functions
  template<class T>
    bool atomic_is_lock_free(const volatile atomic<T>*) noexcept;
  template<class T>
    bool atomic_is_lock_free(const atomic<T>*) noexcept;
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
    T atomic_exchange(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
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

  template<class T>
    T atomic_fetch_add(volatile atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template<class T>
    T atomic_fetch_add(atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template<class T>
    T atomic_fetch_add_explicit(volatile atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_add_explicit(atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_sub(volatile atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template<class T>
    T atomic_fetch_sub(atomic<T>*, typename atomic<T>::difference_type) noexcept;
  template<class T>
    T atomic_fetch_sub_explicit(volatile atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_sub_explicit(atomic<T>*, typename atomic<T>::difference_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_and(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_fetch_and(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_fetch_and_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_and_explicit(atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_or(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_fetch_or(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_fetch_or_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template<class T>
    T atomic_fetch_or_explicit(atomic<T>*, typename atomic<T>::value_type,
                               memory_order) noexcept;
  template<class T>
    T atomic_fetch_xor(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_fetch_xor(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    T atomic_fetch_xor_explicit(volatile atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;
  template<class T>
    T atomic_fetch_xor_explicit(atomic<T>*, typename atomic<T>::value_type,
                                memory_order) noexcept;

  template<class T>
    void atomic_wait(const volatile atomic<T>*, typename atomic<T>::value_type);
  template<class T>
    void atomic_wait(const atomic<T>*, typename atomic<T>::value_type);
  template<class T>
    void atomic_wait_explicit(const volatile atomic<T>*, typename atomic<T>::value_type,
                              memory_order);
  template<class T>
    void atomic_wait_explicit(const atomic<T>*, typename atomic<T>::value_type,
                              memory_order);
  template<class T>
    void atomic_notify_one(volatile atomic<T>*);
  template<class T>
    void atomic_notify_one(atomic<T>*);
  template<class T>
    void atomic_notify_all(volatile atomic<T>*);
  template<class T>
    void atomic_notify_all(atomic<T>*);

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
  using atomic_char8_t        = atomic<char8_t>;
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

  using atomic_signed_lock_free   = see below;
  using atomic_unsigned_lock_free = see below;

  // [atomics.flag], flag type and operations
  struct atomic_flag;

  bool atomic_flag_test(const volatile atomic_flag*) noexcept;
  bool atomic_flag_test(const atomic_flag*) noexcept;
  bool atomic_flag_test_explicit(const volatile atomic_flag*, memory_order) noexcept;
  bool atomic_flag_test_explicit(const atomic_flag*, memory_order) noexcept;
  bool atomic_flag_test_and_set(volatile atomic_flag*) noexcept;
  bool atomic_flag_test_and_set(atomic_flag*) noexcept;
  bool atomic_flag_test_and_set_explicit(volatile atomic_flag*, memory_order) noexcept;
  bool atomic_flag_test_and_set_explicit(atomic_flag*, memory_order) noexcept;
  void atomic_flag_clear(volatile atomic_flag*) noexcept;
  void atomic_flag_clear(atomic_flag*) noexcept;
  void atomic_flag_clear_explicit(volatile atomic_flag*, memory_order) noexcept;
  void atomic_flag_clear_explicit(atomic_flag*, memory_order) noexcept;

  void atomic_flag_wait(const volatile atomic_flag*, bool) noexcept;
  void atomic_flag_wait(const atomic_flag*, bool) noexcept;
  void atomic_flag_wait_explicit(const volatile atomic_flag*,
                                 bool, memory_order) noexcept;
  void atomic_flag_wait_explicit(const atomic_flag*,
                                 bool, memory_order) noexcept;
  void atomic_flag_notify_one(volatile atomic_flag*) noexcept;
  void atomic_flag_notify_one(atomic_flag*) noexcept;
  void atomic_flag_notify_all(volatile atomic_flag*) noexcept;
  void atomic_flag_notify_all(atomic_flag*) noexcept;

  // [atomics.fences], fences
  extern "C" void atomic_thread_fence(memory_order) noexcept;
  extern "C" void atomic_signal_fence(memory_order) noexcept;
}
```

## Type aliases <a id="atomics.alias">[[atomics.alias]]</a>

The type aliases `atomic_signed_lock_free` and
`atomic_unsigned_lock_free` name specializations of `atomic` whose
template arguments are integral types, respectively signed and unsigned,
and whose `is_always_lock_free` property is `true`.

[*Note 1*: These aliases are optional in freestanding implementations
[[compliance]]. — *end note*]

Implementations should choose for these aliases the integral
specializations of `atomic` for which the atomic waiting and notifying
operations [[atomics.wait]] are most efficient.

## Order and consistency <a id="atomics.order">[[atomics.order]]</a>

``` cpp
namespace std {
  enum class memory_order : unspecified {
    relaxed, consume, acquire, release, acq_rel, seq_cst
  };
  inline constexpr memory_order memory_order_relaxed = memory_order::relaxed;
  inline constexpr memory_order memory_order_consume = memory_order::consume;
  inline constexpr memory_order memory_order_acquire = memory_order::acquire;
  inline constexpr memory_order memory_order_release = memory_order::release;
  inline constexpr memory_order memory_order_acq_rel = memory_order::acq_rel;
  inline constexpr memory_order memory_order_seq_cst = memory_order::seq_cst;
}
```

The enumeration `memory_order` specifies the detailed regular
(non-atomic) memory synchronization order as defined in
[[intro.multithread]] and may provide for operation ordering. Its
enumerated values and their meanings are as follows:

- `memory_order::relaxed`: no operation orders memory.
- `memory_order::release`, `memory_order::acq_rel`, and
  `memory_order::seq_cst`: a store operation performs a release
  operation on the affected memory location.
- `memory_order::consume`: a load operation performs a consume operation
  on the affected memory location. \[*Note 1*: Prefer
  `memory_order::acquire`, which provides stronger guarantees than
  `memory_order::consume`. Implementations have found it infeasible to
  provide performance better than that of `memory_order::acquire`.
  Specification revisions are under consideration. — *end note*]
- `memory_order::acquire`, `memory_order::acq_rel`, and
  `memory_order::seq_cst`: a load operation performs an acquire
  operation on the affected memory location.

[*Note 2*: Atomic operations specifying `memory_order::relaxed` are
relaxed with respect to memory ordering. Implementations must still
guarantee that any given atomic access to a particular atomic object be
indivisible with respect to all other atomic accesses to that
object. — *end note*]

An atomic operation A that performs a release operation on an atomic
object M synchronizes with an atomic operation B that performs an
acquire operation on M and takes its value from any side effect in the
release sequence headed by A.

An atomic operation A on some atomic object M is *coherence-ordered
before* another atomic operation B on M if

- A is a modification, and B reads the value stored by A, or
- A precedes B in the modification order of M, or
- A and B are not the same atomic read-modify-write operation, and there
  exists an atomic modification X of M such that A reads the value
  stored by X and X precedes B in the modification order of M, or
- there exists an atomic modification X of M such that A is
  coherence-ordered before X and X is coherence-ordered before B.

There is a single total order S on all `memory_order::seq_cst`
operations, including fences, that satisfies the following constraints.
First, if A and B are `memory_order::seq_cst` operations and A strongly
happens before B, then A precedes B in S. Second, for every pair of
atomic operations A and B on an object M, where A is coherence-ordered
before B, the following four conditions are required to be satisfied by
S:

- if A and B are both `memory_order::seq_cst` operations, then A
  precedes B in S; and
- if A is a `memory_order::seq_cst` operation and B happens before a
  `memory_order::seq_cst` fence Y, then A precedes Y in S; and
- if a `memory_order::seq_cst` fence X happens before A and B is a
  `memory_order::seq_cst` operation, then X precedes B in S; and
- if a `memory_order::seq_cst` fence X happens before A and B happens
  before a `memory_order::seq_cst` fence Y, then X precedes Y in S.

[*Note 3*: This definition ensures that S is consistent with the
modification order of any atomic object M. It also ensures that a
`memory_order::seq_cst` load A of M gets its value either from the last
modification of M that precedes A in S or from some
non-`memory_order::seq_cst` modification of M that does not happen
before any modification of M that precedes A in S. — *end note*]

[*Note 4*: We do not require that S be consistent with “happens before”
[[intro.races]]. This allows more efficient implementation of
`memory_order::acquire` and `memory_order::release` on some machine
architectures. It can produce surprising results when these are mixed
with `memory_order::seq_cst` accesses. — *end note*]

[*Note 5*: `memory_order::seq_cst` ensures sequential consistency only
for a program that is free of data races and uses exclusively
`memory_order::seq_cst` atomic operations. Any use of weaker ordering
will invalidate this guarantee unless extreme care is used. In many
cases, `memory_order::seq_cst` atomic operations are reorderable with
respect to other atomic operations performed by the same
thread. — *end note*]

Implementations should ensure that no “out-of-thin-air” values are
computed that circularly depend on their own computation.

[*Note 6*:

For example, with `x` and `y` initially zero,

``` cpp
// Thread 1:
r1 = y.load(memory_order::relaxed);
x.store(r1, memory_order::relaxed);
```

``` cpp
// Thread 2:
r2 = x.load(memory_order::relaxed);
y.store(r2, memory_order::relaxed);
```

should not produce `r1 == r2 == 42`, since the store of 42 to `y` is
only possible if the store to `x` stores `42`, which circularly depends
on the store to `y` storing `42`. Note that without this restriction,
such an execution is possible.

— *end note*]

[*Note 7*:

The recommendation similarly disallows `r1 == r2 == 42` in the following
example, with `x` and `y` again initially zero:

``` cpp
// Thread 1:
r1 = x.load(memory_order::relaxed);
if (r1 == 42) y.store(42, memory_order::relaxed);
```

``` cpp
// Thread 2:
r2 = y.load(memory_order::relaxed);
if (r2 == 42) x.store(42, memory_order::relaxed);
```

— *end note*]

Atomic read-modify-write operations shall always read the last value (in
the modification order) written before the write associated with the
read-modify-write operation.

Implementations should make atomic stores visible to atomic loads within
a reasonable amount of time.

``` cpp
template<class T>
  T kill_dependency(T y) noexcept;
```

*Effects:* The argument does not carry a dependency to the return
value [[intro.multithread]].

*Returns:* `y`.

## Lock-free property <a id="atomics.lockfree">[[atomics.lockfree]]</a>

``` cpp
#define ATOMIC_BOOL_LOCK_FREE unspecified
#define ATOMIC_CHAR_LOCK_FREE unspecified
#define ATOMIC_CHAR8_T_LOCK_FREE unspecified
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

At least one signed integral specialization of the `atomic` template,
along with the specialization for the corresponding unsigned type
[[basic.fundamental]], is always lock-free.

[*Note 1*: This requirement is optional in freestanding implementations
[[compliance]]. — *end note*]

The function `atomic_is_lock_free` [[atomics.types.operations]]
indicates whether the object is lock-free. In any given program
execution, the result of the lock-free query shall be consistent for all
pointers of the same type.

Atomic operations that are not lock-free are considered to potentially
block [[intro.progress]].

[*Note 2*: Operations that are lock-free should also be address-free.
That is, atomic operations on the same memory location via two different
addresses will communicate atomically. The implementation should not
depend on any per-process state. This restriction enables communication
by memory that is mapped into a process more than once and by memory
that is shared between two processes. — *end note*]

## Waiting and notifying <a id="atomics.wait">[[atomics.wait]]</a>

*Atomic waiting operations* and *atomic notifying operations* provide a
mechanism to wait for the value of an atomic object to change more
efficiently than can be achieved with polling. An atomic waiting
operation may block until it is unblocked by an atomic notifying
operation, according to each function’s effects.

[*Note 1*: Programs are not guaranteed to observe transient atomic
values, an issue known as the A-B-A problem, resulting in continued
blocking if a condition is only temporarily met. — *end note*]

[*Note 2*:

The following functions are atomic waiting operations:

- `atomic<T>::wait`,
- `atomic_flag::wait`,
- `atomic_wait` and `atomic_wait_explicit`,
- `atomic_flag_wait` and `atomic_flag_wait_explicit`, and
- `atomic_ref<T>::wait`.

— *end note*]

[*Note 3*:

The following functions are atomic notifying operations:

- `atomic<T>::notify_one` and `atomic<T>::notify_all`,
- `atomic_flag::notify_one` and `atomic_flag::notify_all`,
- `atomic_notify_one` and `atomic_notify_all`,
- `atomic_flag_notify_one` and `atomic_flag_notify_all`, and
- `atomic_ref<T>::notify_one` and `atomic_ref<T>::notify_all`.

— *end note*]

A call to an atomic waiting operation on an atomic object `M` is
*eligible to be unblocked* by a call to an atomic notifying operation on
`M` if there exist side effects `X` and `Y` on `M` such that:

- the atomic waiting operation has blocked after observing the result of
  `X`,
- `X` precedes `Y` in the modification order of `M`, and
- `Y` happens before the call to the atomic notifying operation.

## Class template `atomic_ref` <a id="atomics.ref.generic">[[atomics.ref.generic]]</a>

``` cpp
namespace std {
  template<class T> struct atomic_ref {
  private:
    T* ptr;             // exposition only
  public:
    using value_type = T;
    static constexpr size_t required_alignment = implementation-defined  // required alignment for atomic_ref type's operations;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic_ref type's operations are always lock free;
    bool is_lock_free() const noexcept;

    explicit atomic_ref(T&);
    atomic_ref(const atomic_ref&) noexcept;
    atomic_ref& operator=(const atomic_ref&) = delete;

    void store(T, memory_order = memory_order::seq_cst) const noexcept;
    T operator=(T) const noexcept;
    T load(memory_order = memory_order::seq_cst) const noexcept;
    operator T() const noexcept;

    T exchange(T, memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_weak(T&, T,
                               memory_order, memory_order) const noexcept;
    bool compare_exchange_strong(T&, T,
                                 memory_order, memory_order) const noexcept;
    bool compare_exchange_weak(T&, T,
                               memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_strong(T&, T,
                                 memory_order = memory_order::seq_cst) const noexcept;

    void wait(T, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() const noexcept;
    void notify_all() const noexcept;
  };
}
```

An `atomic_ref` object applies atomic operations [[atomics.general]] to
the object referenced by `*ptr` such that, for the lifetime
[[basic.life]] of the `atomic_ref` object, the object referenced by
`*ptr` is an atomic object [[intro.races]].

The program is ill-formed if `is_trivially_copyable_v<T>` is `false`.

The lifetime [[basic.life]] of an object referenced by `*ptr` shall
exceed the lifetime of all `atomic_ref`s that reference the object.
While any `atomic_ref` instances exist that reference the `*ptr` object,
all accesses to that object shall exclusively occur through those
`atomic_ref` instances. No subobject of the object referenced by
`atomic_ref` shall be concurrently referenced by any other `atomic_ref`
object.

Atomic operations applied to an object through a referencing
`atomic_ref` are atomic with respect to atomic operations applied
through any other `atomic_ref` referencing the same object.

[*Note 1*: Atomic operations or the `atomic_ref` constructor could
acquire a shared resource, such as a lock associated with the referenced
object, to enable atomic operations to be applied to the referenced
object. — *end note*]

### Operations <a id="atomics.ref.ops">[[atomics.ref.ops]]</a>

``` cpp
static constexpr size_t required_alignment;
```

The alignment required for an object to be referenced by an atomic
reference, which is at least `alignof(T)`.

[*Note 1*: Hardware could require an object referenced by an
`atomic_ref` to have stricter alignment [[basic.align]] than other
objects of type `T`. Further, whether operations on an `atomic_ref` are
lock-free could depend on the alignment of the referenced object. For
example, lock-free operations on `std::complex<double>` could be
supported only if aligned to `2*alignof(double)`. — *end note*]

``` cpp
static constexpr bool is_always_lock_free;
```

The static data member `is_always_lock_free` is `true` if the
`atomic_ref` type’s operations are always lock-free, and `false`
otherwise.

``` cpp
bool is_lock_free() const noexcept;
```

*Returns:* `true` if operations on all objects of the type
`atomic_ref<T>` are lock-free, `false` otherwise.

``` cpp
atomic_ref(T& obj);
```

*Preconditions:* The referenced object is aligned to
`required_alignment`.

*Ensures:* `*this` references `obj`.

*Throws:* Nothing.

``` cpp
atomic_ref(const atomic_ref& ref) noexcept;
```

*Ensures:* `*this` references the object referenced by `ref`.

``` cpp
void store(T desired, memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* The `order` argument is neither
`memory_order::consume`, `memory_order::acquire`, nor
`memory_order::acq_rel`.

*Effects:* Atomically replaces the value referenced by `*ptr` with the
value of `desired`. Memory is affected according to the value of
`order`.

``` cpp
T operator=(T desired) const noexcept;
```

*Effects:* Equivalent to:

``` cpp
store(desired);
return desired;
```

``` cpp
T load(memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* The `order` argument is neither `memory_order::release`
nor `memory_order::acq_rel`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns the value referenced by `*ptr`.

``` cpp
operator T() const noexcept;
```

*Effects:* Equivalent to: `return load();`

``` cpp
T exchange(T desired, memory_order order = memory_order::seq_cst) const noexcept;
```

*Effects:* Atomically replaces the value referenced by `*ptr` with
`desired`. Memory is affected according to the value of `order`. This
operation is an atomic read-modify-write
operation [[intro.multithread]].

*Returns:* Atomically returns the value referenced by `*ptr` immediately
before the effects.

``` cpp
bool compare_exchange_weak(T& expected, T desired,
                           memory_order success, memory_order failure) const noexcept;

bool compare_exchange_strong(T& expected, T desired,
                             memory_order success, memory_order failure) const noexcept;

bool compare_exchange_weak(T& expected, T desired,
                           memory_order order = memory_order::seq_cst) const noexcept;

bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* The `failure` argument is neither
`memory_order::release` nor `memory_order::acq_rel`.

*Effects:* Retrieves the value in `expected`. It then atomically
compares the value representation of the value referenced by `*ptr` for
equality with that previously retrieved from `expected`, and if `true`,
replaces the value referenced by `*ptr` with that in `desired`. If and
only if the comparison is `true`, memory is affected according to the
value of `success`, and if the comparison is `false`, memory is affected
according to the value of `failure`. When only one `memory_order`
argument is supplied, the value of `success` is `order`, and the value
of `failure` is `order` except that a value of `memory_order::acq_rel`
shall be replaced by the value `memory_order::acquire` and a value of
`memory_order::release` shall be replaced by the value
`memory_order::relaxed`. If and only if the comparison is `false` then,
after the atomic operation, the value in `expected` is replaced by the
value read from the value referenced by `*ptr` during the atomic
comparison. If the operation returns `true`, these operations are atomic
read-modify-write operations [[intro.races]] on the value referenced by
`*ptr`. Otherwise, these operations are atomic load operations on that
memory.

*Returns:* The result of the comparison.

*Remarks:* A weak compare-and-exchange operation may fail spuriously.
That is, even when the contents of memory referred to by `expected` and
`ptr` are equal, it may return `false` and store back to `expected` the
same memory contents that were originally there.

[*Note 2*: This spurious failure enables implementation of
compare-and-exchange on a broader class of machines, e.g., load-locked
store-conditional machines. A consequence of spurious failure is that
nearly all uses of weak compare-and-exchange will be in a loop. When a
compare-and-exchange is in a loop, the weak version will yield better
performance on some platforms. When a weak compare-and-exchange would
require a loop and a strong one would not, the strong one is
preferable. — *end note*]

``` cpp
void wait(T old, memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `load(order)` and compares its value representation for
  equality against that of `old`.
- If they compare unequal, returns.
- Blocks until it is unblocked by an atomic notifying operation or is
  unblocked spuriously.

*Remarks:* This function is an atomic waiting operation [[atomics.wait]]
on atomic object `*ptr`.

``` cpp
void notify_one() const noexcept;
```

*Effects:* Unblocks the execution of at least one atomic waiting
operation on `*ptr` that is eligible to be unblocked [[atomics.wait]] by
this call, if any such atomic waiting operations exist.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]] on atomic object `*ptr`.

``` cpp
void notify_all() const noexcept;
```

*Effects:* Unblocks the execution of all atomic waiting operations on
`*ptr` that are eligible to be unblocked [[atomics.wait]] by this call.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]] on atomic object `*ptr`.

### Specializations for integral types <a id="atomics.ref.int">[[atomics.ref.int]]</a>

There are specializations of the `atomic_ref` class template for the
integral types `char`, `signed char`, `unsigned char`, `short`,
`unsigned short`, `int`, `unsigned int`, `long`, `unsigned long`,
`long long`, `unsigned long long`, `char8_t`, `char16_t`, `char32_t`,
`wchar_t`, and any other types needed by the typedefs in the header
`<cstdint>`. For each such type `integral`, the specialization
`atomic_ref<integral>` provides additional atomic operations appropriate
to integral types.

[*Note 1*: The specialization `atomic_ref<bool>` uses the primary
template [[atomics.ref.generic]]. — *end note*]

``` cpp
namespace std {
  template<> struct atomic_ref<integral> {
  private:
    integral* ptr;        // exposition only
  public:
    using value_type = integral;
    using difference_type = value_type;
    static constexpr size_t required_alignment = implementation-defined  // required alignment for atomic_ref type's operations;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic_ref type's operations are always lock free;
    bool is_lock_free() const noexcept;

    explicit atomic_ref(integral&);
    atomic_ref(const atomic_ref&) noexcept;
    atomic_ref& operator=(const atomic_ref&) = delete;

    void store(integral, memory_order = memory_order::seq_cst) const noexcept;
    integral operator=(integral) const noexcept;
    integral load(memory_order = memory_order::seq_cst) const noexcept;
    operator integral() const noexcept;

    integral exchange(integral,
                      memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order, memory_order) const noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order, memory_order) const noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order = memory_order::seq_cst) const noexcept;

    integral fetch_add(integral,
                       memory_order = memory_order::seq_cst) const noexcept;
    integral fetch_sub(integral,
                       memory_order = memory_order::seq_cst) const noexcept;
    integral fetch_and(integral,
                       memory_order = memory_order::seq_cst) const noexcept;
    integral fetch_or(integral,
                      memory_order = memory_order::seq_cst) const noexcept;
    integral fetch_xor(integral,
                       memory_order = memory_order::seq_cst) const noexcept;

    integral operator++(int) const noexcept;
    integral operator--(int) const noexcept;
    integral operator++() const noexcept;
    integral operator--() const noexcept;
    integral operator+=(integral) const noexcept;
    integral operator-=(integral) const noexcept;
    integral operator&=(integral) const noexcept;
    integral operator|=(integral) const noexcept;
    integral operator^=(integral) const noexcept;

    void wait(integral, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() const noexcept;
    void notify_all() const noexcept;
  };
}
```

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform arithmetic computations. The key,
operator, and computation correspondence is identified in
[[atomic.types.int.comp]].

``` cpp
integral fetch_key(integral operand, memory_order order = memory_order::seq_cst) const noexcept;
```

*Effects:* Atomically replaces the value referenced by `*ptr` with the
result of the computation applied to the value referenced by `*ptr` and
the given operand. Memory is affected according to the value of `order`.
These operations are atomic read-modify-write
operations [[intro.races]].

*Returns:* Atomically, the value referenced by `*ptr` immediately before
the effects.

*Remarks:* For signed integer types, the result is as if the object
value and parameters were converted to their corresponding unsigned
types, the computation performed on those types, and the result
converted back to the signed type.

[*Note 1*: There are no undefined results arising from the
computation. — *end note*]

``` cpp
integral operator op=(integral operand) const noexcept;
```

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Specializations for floating-point types <a id="atomics.ref.float">[[atomics.ref.float]]</a>

There are specializations of the `atomic_ref` class template for the
floating-point types `float`, `double`, and `long double`. For each such
type `floating-point`, the specialization `atomic_ref<floating-point>`
provides additional atomic operations appropriate to floating-point
types.

``` cpp
namespace std {
  template<> struct atomic_ref<floating-point> {
  private:
    floating-point* ptr;  // exposition only
  public:
    using value_type = floating-point;
    using difference_type = value_type;
    static constexpr size_t required_alignment = implementation-defined  // required alignment for atomic_ref type's operations;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic_ref type's operations are always lock free;
    bool is_lock_free() const noexcept;

    explicit atomic_ref(floating-point&);
    atomic_ref(const atomic_ref&) noexcept;
    atomic_ref& operator=(const atomic_ref&) = delete;

    void store(floating-point, memory_order = memory_order::seq_cst) const noexcept;
    floating-point operator=(floating-point) const noexcept;
    floating-point load(memory_order = memory_order::seq_cst) const noexcept;
    operator floating-point() const noexcept;

    floating-point exchange(floating-point,
                            memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_weak(floating-point&, floating-point,
                               memory_order, memory_order) const noexcept;
    bool compare_exchange_strong(floating-point&, floating-point,
                                 memory_order, memory_order) const noexcept;
    bool compare_exchange_weak(floating-point&, floating-point,
                               memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_strong(floating-point&, floating-point,
                                 memory_order = memory_order::seq_cst) const noexcept;

    floating-point fetch_add(floating-point,
                             memory_order = memory_order::seq_cst) const noexcept;
    floating-point fetch_sub(floating-point,
                             memory_order = memory_order::seq_cst) const noexcept;

    floating-point operator+=(floating-point) const noexcept;
    floating-point operator-=(floating-point) const noexcept;

    void wait(floating-point, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() const noexcept;
    void notify_all() const noexcept;
  };
}
```

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform arithmetic computations. The key,
operator, and computation correspondence are identified in
[[atomic.types.int.comp]].

``` cpp
floating-point fetch_key(floating-point operand,
                          memory_order order = memory_order::seq_cst) const noexcept;
```

*Effects:* Atomically replaces the value referenced by `*ptr` with the
result of the computation applied to the value referenced by `*ptr` and
the given operand. Memory is affected according to the value of `order`.
These operations are atomic read-modify-write
operations [[intro.races]].

*Returns:* Atomically, the value referenced by `*ptr` immediately before
the effects.

*Remarks:* If the result is not a representable value for its
type [[expr.pre]], the result is unspecified, but the operations
otherwise have no undefined behavior. Atomic arithmetic operations on
*`floating-point`* should conform to the
`std::numeric_limits<`*`floating-point`*`>` traits associated with the
floating-point type [[limits.syn]]. The floating-point
environment [[cfenv]] for atomic arithmetic operations on
*`floating-point`* may be different than the calling thread’s
floating-point environment.

``` cpp
floating-point operator op=(floating-point operand) const noexcept;
```

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Partial specialization for pointers <a id="atomics.ref.pointer">[[atomics.ref.pointer]]</a>

``` cpp
namespace std {
  template<class T> struct atomic_ref<T*> {
  private:
    T** ptr;        // exposition only
  public:
    using value_type = T*;
    using difference_type = ptrdiff_t;
    static constexpr size_t required_alignment = implementation-defined  // required alignment for atomic_ref type's operations;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic_ref type's operations are always lock free;
    bool is_lock_free() const noexcept;

    explicit atomic_ref(T*&);
    atomic_ref(const atomic_ref&) noexcept;
    atomic_ref& operator=(const atomic_ref&) = delete;

    void store(T*, memory_order = memory_order::seq_cst) const noexcept;
    T* operator=(T*) const noexcept;
    T* load(memory_order = memory_order::seq_cst) const noexcept;
    operator T*() const noexcept;

    T* exchange(T*, memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_weak(T*&, T*,
                               memory_order, memory_order) const noexcept;
    bool compare_exchange_strong(T*&, T*,
                                 memory_order, memory_order) const noexcept;
    bool compare_exchange_weak(T*&, T*,
                               memory_order = memory_order::seq_cst) const noexcept;
    bool compare_exchange_strong(T*&, T*,
                                 memory_order = memory_order::seq_cst) const noexcept;

    T* fetch_add(difference_type, memory_order = memory_order::seq_cst) const noexcept;
    T* fetch_sub(difference_type, memory_order = memory_order::seq_cst) const noexcept;

    T* operator++(int) const noexcept;
    T* operator--(int) const noexcept;
    T* operator++() const noexcept;
    T* operator--() const noexcept;
    T* operator+=(difference_type) const noexcept;
    T* operator-=(difference_type) const noexcept;

    void wait(T*, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() const noexcept;
    void notify_all() const noexcept;
  };
}
```

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform arithmetic computations. The key,
operator, and computation correspondence is identified in
[[atomic.types.pointer.comp]].

``` cpp
T* fetch_key(difference_type operand, memory_order order = memory_order::seq_cst) const noexcept;
```

*Mandates:* `T` is a complete object type.

*Effects:* Atomically replaces the value referenced by `*ptr` with the
result of the computation applied to the value referenced by `*ptr` and
the given operand. Memory is affected according to the value of `order`.
These operations are atomic read-modify-write
operations [[intro.races]].

*Returns:* Atomically, the value referenced by `*ptr` immediately before
the effects.

*Remarks:* The result may be an undefined address, but the operations
otherwise have no undefined behavior.

``` cpp
T* operator op=(difference_type operand) const noexcept;
```

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Member operators common to integers and pointers to objects <a id="atomics.ref.memop">[[atomics.ref.memop]]</a>

``` cpp
value_type operator++(int) const noexcept;
```

*Effects:* Equivalent to: `return fetch_add(1);`

``` cpp
value_type operator--(int) const noexcept;
```

*Effects:* Equivalent to: `return fetch_sub(1);`

``` cpp
value_type operator++() const noexcept;
```

*Effects:* Equivalent to: `return fetch_add(1) + 1;`

``` cpp
value_type operator--() const noexcept;
```

*Effects:* Equivalent to: `return fetch_sub(1) - 1;`

## Class template `atomic` <a id="atomics.types.generic">[[atomics.types.generic]]</a>

``` cpp
namespace std {
  template<class T> struct atomic {
    using value_type = T;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;

    // [atomics.types.operations], operations on atomic types
    constexpr atomic() noexcept(is_nothrow_default_constructible_v<T>);
    constexpr atomic(T) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;

    T load(memory_order = memory_order::seq_cst) const volatile noexcept;
    T load(memory_order = memory_order::seq_cst) const noexcept;
    operator T() const volatile noexcept;
    operator T() const noexcept;
    void store(T, memory_order = memory_order::seq_cst) volatile noexcept;
    void store(T, memory_order = memory_order::seq_cst) noexcept;
    T operator=(T) volatile noexcept;
    T operator=(T) noexcept;

    T exchange(T, memory_order = memory_order::seq_cst) volatile noexcept;
    T exchange(T, memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_weak(T&, T, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(T&, T, memory_order, memory_order) noexcept;
    bool compare_exchange_strong(T&, T, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(T&, T, memory_order, memory_order) noexcept;
    bool compare_exchange_weak(T&, T, memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_weak(T&, T, memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_strong(T&, T, memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_strong(T&, T, memory_order = memory_order::seq_cst) noexcept;

    void wait(T, memory_order = memory_order::seq_cst) const volatile noexcept;
    void wait(T, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() volatile noexcept;
    void notify_one() noexcept;
    void notify_all() volatile noexcept;
    void notify_all() noexcept;
  };
}
```

The template argument for `T` shall meet the *Cpp17CopyConstructible*
and *Cpp17CopyAssignable* requirements. The program is ill-formed if any
of

- `is_trivially_copyable_v<T>`,
- `is_copy_constructible_v<T>`,
- `is_move_constructible_v<T>`,
- `is_copy_assignable_v<T>`, or
- `is_move_assignable_v<T>`

is `false`.

[*Note 1*: Type arguments that are not also statically initializable
may be difficult to use. — *end note*]

The specialization `atomic<bool>` is a standard-layout struct.

[*Note 2*: The representation of an atomic specialization need not have
the same size and alignment requirement as its corresponding argument
type. — *end note*]

### Operations on atomic types <a id="atomics.types.operations">[[atomics.types.operations]]</a>

``` cpp
constexpr atomic() noexcept(is_nothrow_default_constructible_v<T>);
```

*Mandates:* `is_default_constructible_v<T>` is `true`.

*Effects:* Initializes the atomic object with the value of `T()`.
Initialization is not an atomic operation [[intro.multithread]].

``` cpp
constexpr atomic(T desired) noexcept;
```

*Effects:* Initializes the object with the value `desired`.
Initialization is not an atomic operation [[intro.multithread]].

[*Note 1*: It is possible to have an access to an atomic object `A`
race with its construction, for example by communicating the address of
the just-constructed object `A` to another thread via
`memory_order::relaxed` operations on a suitable atomic pointer
variable, and then immediately accessing `A` in the receiving thread.
This results in undefined behavior. — *end note*]

``` cpp
static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
```

The `static` data member `is_always_lock_free` is `true` if the atomic
type’s operations are always lock-free, and `false` otherwise.

[*Note 2*: The value of `is_always_lock_free` is consistent with the
value of the corresponding `ATOMIC_..._LOCK_FREE` macro, if
defined. — *end note*]

``` cpp
bool is_lock_free() const volatile noexcept;
bool is_lock_free() const noexcept;
```

*Returns:* `true` if the object’s operations are lock-free, `false`
otherwise.

[*Note 3*: The return value of the `is_lock_free` member function is
consistent with the value of `is_always_lock_free` for the same
type. — *end note*]

``` cpp
void store(T desired, memory_order order = memory_order::seq_cst) volatile noexcept;
void store(T desired, memory_order order = memory_order::seq_cst) noexcept;
```

*Preconditions:* The `order` argument is neither
`memory_order::consume`, `memory_order::acquire`, nor
`memory_order::acq_rel`.

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Atomically replaces the value pointed to by `this` with the
value of `desired`. Memory is affected according to the value of
`order`.

``` cpp
T operator=(T desired) volatile noexcept;
T operator=(T desired) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to `store(desired)`.

*Returns:* `desired`.

``` cpp
T load(memory_order order = memory_order::seq_cst) const volatile noexcept;
T load(memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* The `order` argument is neither `memory_order::release`
nor `memory_order::acq_rel`.

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns the value pointed to by `this`.

``` cpp
operator T() const volatile noexcept;
operator T() const noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to: `return load();`

``` cpp
T exchange(T desired, memory_order order = memory_order::seq_cst) volatile noexcept;
T exchange(T desired, memory_order order = memory_order::seq_cst) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Atomically replaces the value pointed to by `this` with
`desired`. Memory is affected according to the value of `order`. These
operations are atomic read-modify-write
operations [[intro.multithread]].

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
                           memory_order order = memory_order::seq_cst) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order order = memory_order::seq_cst) noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order::seq_cst) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order::seq_cst) noexcept;
```

*Preconditions:* The `failure` argument is neither
`memory_order::release` nor `memory_order::acq_rel`.

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Retrieves the value in `expected`. It then atomically
compares the value representation of the value pointed to by `this` for
equality with that previously retrieved from `expected`, and if true,
replaces the value pointed to by `this` with that in `desired`. If and
only if the comparison is `true`, memory is affected according to the
value of `success`, and if the comparison is false, memory is affected
according to the value of `failure`. When only one `memory_order`
argument is supplied, the value of `success` is `order`, and the value
of `failure` is `order` except that a value of `memory_order::acq_rel`
shall be replaced by the value `memory_order::acquire` and a value of
`memory_order::release` shall be replaced by the value
`memory_order::relaxed`. If and only if the comparison is false then,
after the atomic operation, the value in `expected` is replaced by the
value pointed to by `this` during the atomic comparison. If the
operation returns `true`, these operations are atomic read-modify-write
operations [[intro.multithread]] on the memory pointed to by `this`.
Otherwise, these operations are atomic load operations on that memory.

*Returns:* The result of the comparison.

[*Note 4*:

For example, the effect of `compare_exchange_strong` on objects without
padding bits [[basic.types]] is

``` cpp
if (memcmp(this, &expected, sizeof(*this)) == 0)
  memcpy(this, &desired, sizeof(*this));
else
  memcpy(expected, this, sizeof(*this));
```

— *end note*]

[*Example 1*:

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

[*Example 2*:

Because the expected value is updated only on failure, code releasing
the memory containing the `expected` value on success will work. For
example, list head insertion will act atomically and would not introduce
a data race in the following code:

``` cpp
do {
  p->next = head;                                   // make new list node point to the current head
} while (!head.compare_exchange_weak(p->next, p));  // try to insert
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

[*Note 5*: This spurious failure enables implementation of
compare-and-exchange on a broader class of machines, e.g., load-locked
store-conditional machines. A consequence of spurious failure is that
nearly all uses of weak compare-and-exchange will be in a loop. When a
compare-and-exchange is in a loop, the weak version will yield better
performance on some platforms. When a weak compare-and-exchange would
require a loop and a strong one would not, the strong one is
preferable. — *end note*]

[*Note 6*: Under cases where the `memcpy` and `memcmp` semantics of the
compare-and-exchange operations apply, the outcome might be failed
comparisons for values that compare equal with `operator==` if the value
representation has trap bits or alternate representations of the same
value. Notably, on implementations conforming to ISO/IEC/IEEE 60559,
floating-point `-0.0` and `+0.0` will not compare equal with `memcmp`
but will compare equal with `operator==`, and NaNs with the same payload
will compare equal with `memcmp` but will not compare equal with
`operator==`. — *end note*]

[*Note 7*:

Because compare-and-exchange acts on an object’s value representation,
padding bits that never participate in the object’s value representation
are ignored. As a consequence, the following code is guaranteed to avoid
spurious failure:

``` cpp
struct padded {
  char clank = 0x42;
  // Padding here.
  unsigned biff = 0xC0DEFEFE;
};
atomic<padded> pad = {};

bool zap() {
  padded expected, desired{0, 0};
  return pad.compare_exchange_strong(expected, desired);
}
```

— *end note*]

[*Note 8*:

For a union with bits that participate in the value representation of
some members but not others, compare-and-exchange might always fail.
This is because such padding bits have an indeterminate value when they
do not participate in the value representation of the active member. As
a consequence, the following code is not guaranteed to ever succeed:

``` cpp
union pony {
  double celestia = 0.;
  short luna;       // padded
};
atomic<pony> princesses = {};

bool party(pony desired) {
  pony expected;
  return princesses.compare_exchange_strong(expected, desired);
}
```

— *end note*]

``` cpp
void wait(T old, memory_order order = memory_order::seq_cst) const volatile noexcept;
void wait(T old, memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `load(order)` and compares its value representation for
  equality against that of `old`.
- If they compare unequal, returns.
- Blocks until it is unblocked by an atomic notifying operation or is
  unblocked spuriously.

*Remarks:* This function is an atomic waiting
operation [[atomics.wait]].

``` cpp
void notify_one() volatile noexcept;
void notify_one() noexcept;
```

*Effects:* Unblocks the execution of at least one atomic waiting
operation that is eligible to be unblocked [[atomics.wait]] by this
call, if any such atomic waiting operations exist.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

``` cpp
void notify_all() volatile noexcept;
void notify_all() noexcept;
```

*Effects:* Unblocks the execution of all atomic waiting operations that
are eligible to be unblocked [[atomics.wait]] by this call.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

### Specializations for integers <a id="atomics.types.int">[[atomics.types.int]]</a>

There are specializations of the `atomic` class template for the
integral types `char`, `signed char`, `unsigned char`, `short`,
`unsigned short`, `int`, `unsigned int`, `long`, `unsigned long`,
`long long`, `unsigned long long`, `char8_t`, `char16_t`, `char32_t`,
`wchar_t`, and any other types needed by the typedefs in the header
`<cstdint>`. For each such type `integral`, the specialization
`atomic<integral>` provides additional atomic operations appropriate to
integral types.

[*Note 1*: The specialization `atomic<bool>` uses the primary template
[[atomics.types.generic]]. — *end note*]

``` cpp
namespace std {
  template<> struct atomic<integral> {
    using value_type = integral;
    using difference_type = value_type;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;

    constexpr atomic() noexcept;
    constexpr atomic(integral) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;

    void store(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    void store(integral, memory_order = memory_order::seq_cst) noexcept;
    integral operator=(integral) volatile noexcept;
    integral operator=(integral) noexcept;
    integral load(memory_order = memory_order::seq_cst) const volatile noexcept;
    integral load(memory_order = memory_order::seq_cst) const noexcept;
    operator integral() const volatile noexcept;
    operator integral() const noexcept;

    integral exchange(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    integral exchange(integral, memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order, memory_order) noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order, memory_order) noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_weak(integral&, integral,
                               memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_strong(integral&, integral,
                                 memory_order = memory_order::seq_cst) noexcept;

    integral fetch_add(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    integral fetch_add(integral, memory_order = memory_order::seq_cst) noexcept;
    integral fetch_sub(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    integral fetch_sub(integral, memory_order = memory_order::seq_cst) noexcept;
    integral fetch_and(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    integral fetch_and(integral, memory_order = memory_order::seq_cst) noexcept;
    integral fetch_or(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    integral fetch_or(integral, memory_order = memory_order::seq_cst) noexcept;
    integral fetch_xor(integral, memory_order = memory_order::seq_cst) volatile noexcept;
    integral fetch_xor(integral, memory_order = memory_order::seq_cst) noexcept;

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

    void wait(integral, memory_order = memory_order::seq_cst) const volatile noexcept;
    void wait(integral, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() volatile noexcept;
    void notify_one() noexcept;
    void notify_all() volatile noexcept;
    void notify_all() noexcept;
  };
}
```

The atomic integral specializations are standard-layout structs. They
each have a trivial destructor.

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform arithmetic computations. The key,
operator, and computation correspondence is:

**Table: Atomic arithmetic computations** <a id="atomic.types.int.comp">[atomic.types.int.comp]</a>

| Op  | Computation |
| --- | ----------- |
| `add` | `+`         | addition | `sub` | `-` | subtraction |
| `or` | `|`         | bitwise inclusive or | `xor` | `^` | bitwise exclusive or |
| `and` | `&`         | bitwise and |     |     |     |

``` cpp
T fetch_key(T operand, memory_order order = memory_order::seq_cst) volatile noexcept;
T fetch_key(T operand, memory_order order = memory_order::seq_cst) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Atomically replaces the value pointed to by `this` with the
result of the computation applied to the value pointed to by `this` and
the given `operand`. Memory is affected according to the value of
`order`. These operations are atomic read-modify-write
operations [[intro.multithread]].

*Returns:* Atomically, the value pointed to by `this` immediately before
the effects.

*Remarks:* For signed integer types, the result is as if the object
value and parameters were converted to their corresponding unsigned
types, the computation performed on those types, and the result
converted back to the signed type.

[*Note 1*: There are no undefined results arising from the
computation. — *end note*]

``` cpp
T operator op=(T operand) volatile noexcept;
T operator op=(T operand) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Specializations for floating-point types <a id="atomics.types.float">[[atomics.types.float]]</a>

There are specializations of the `atomic` class template for the
floating-point types `float`, `double`, and `long double`. For each such
type `floating-point`, the specialization `atomic<floating-point>`
provides additional atomic operations appropriate to floating-point
types.

``` cpp
namespace std {
  template<> struct atomic<floating-point> {
    using value_type = floating-point;
    using difference_type = value_type;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;

    constexpr atomic() noexcept;
    constexpr atomic(floating-point) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;

    void store(floating-point, memory_order = memory_order::seq_cst) volatile noexcept;
    void store(floating-point, memory_order = memory_order::seq_cst) noexcept;
    floating-point operator=(floating-point) volatile noexcept;
    floating-point operator=(floating-point) noexcept;
    floating-point load(memory_order = memory_order::seq_cst) volatile noexcept;
    floating-point load(memory_order = memory_order::seq_cst) noexcept;
    operator floating-point() volatile noexcept;
    operator floating-point() noexcept;

    floating-point exchange(floating-point,
                            memory_order = memory_order::seq_cst) volatile noexcept;
    floating-point exchange(floating-point,
                            memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_weak(floating-point&, floating-point,
                               memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(floating-point&, floating-point,
                               memory_order, memory_order) noexcept;
    bool compare_exchange_strong(floating-point&, floating-point,
                                 memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(floating-point&, floating-point,
                                 memory_order, memory_order) noexcept;
    bool compare_exchange_weak(floating-point&, floating-point,
                               memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_weak(floating-point&, floating-point,
                               memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_strong(floating-point&, floating-point,
                                 memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_strong(floating-point&, floating-point,
                                 memory_order = memory_order::seq_cst) noexcept;

    floating-point fetch_add(floating-point,
                             memory_order = memory_order::seq_cst) volatile noexcept;
    floating-point fetch_add(floating-point,
                             memory_order = memory_order::seq_cst) noexcept;
    floating-point fetch_sub(floating-point,
                             memory_order = memory_order::seq_cst) volatile noexcept;
    floating-point fetch_sub(floating-point,
                             memory_order = memory_order::seq_cst) noexcept;

    floating-point operator+=(floating-point) volatile noexcept;
    floating-point operator+=(floating-point) noexcept;
    floating-point operator-=(floating-point) volatile noexcept;
    floating-point operator-=(floating-point) noexcept;

    void wait(floating-point, memory_order = memory_order::seq_cst) const volatile noexcept;
    void wait(floating-point, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() volatile noexcept;
    void notify_one() noexcept;
    void notify_all() volatile noexcept;
    void notify_all() noexcept;
  };
}
```

The atomic floating-point specializations are standard-layout structs.
They each have a trivial destructor.

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform arithmetic addition and subtraction
computations. The key, operator, and computation correspondence are
identified in [[atomic.types.int.comp]].

``` cpp
T fetch_key(T operand, memory_order order = memory_order::seq_cst) volatile noexcept;
T fetch_key(T operand, memory_order order = memory_order::seq_cst) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Atomically replaces the value pointed to by `this` with the
result of the computation applied to the value pointed to by `this` and
the given `operand`. Memory is affected according to the value of
`order`. These operations are atomic read-modify-write
operations [[intro.multithread]].

*Returns:* Atomically, the value pointed to by `this` immediately before
the effects.

*Remarks:* If the result is not a representable value for its
type [[expr.pre]] the result is unspecified, but the operations
otherwise have no undefined behavior. Atomic arithmetic operations on
*`floating-point`* should conform to the
`std::numeric_limits<`*`floating-point`*`>` traits associated with the
floating-point type [[limits.syn]]. The floating-point
environment [[cfenv]] for atomic arithmetic operations on
*`floating-point`* may be different than the calling thread’s
floating-point environment.

``` cpp
T operator op=(T operand) volatile noexcept;
T operator op=(T operand) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

*Remarks:* If the result is not a representable value for its
type [[expr.pre]] the result is unspecified, but the operations
otherwise have no undefined behavior. Atomic arithmetic operations on
*`floating-point`* should conform to the
`std::numeric_limits<`*`floating-point`*`>` traits associated with the
floating-point type [[limits.syn]]. The floating-point
environment [[cfenv]] for atomic arithmetic operations on
*`floating-point`* may be different than the calling thread’s
floating-point environment.

### Partial specialization for pointers <a id="atomics.types.pointer">[[atomics.types.pointer]]</a>

``` cpp
namespace std {
  template<class T> struct atomic<T*> {
    using value_type = T*;
    using difference_type = ptrdiff_t;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const volatile noexcept;
    bool is_lock_free() const noexcept;

    constexpr atomic() noexcept;
    constexpr atomic(T*) noexcept;
    atomic(const atomic&) = delete;
    atomic& operator=(const atomic&) = delete;
    atomic& operator=(const atomic&) volatile = delete;

    void store(T*, memory_order = memory_order::seq_cst) volatile noexcept;
    void store(T*, memory_order = memory_order::seq_cst) noexcept;
    T* operator=(T*) volatile noexcept;
    T* operator=(T*) noexcept;
    T* load(memory_order = memory_order::seq_cst) const volatile noexcept;
    T* load(memory_order = memory_order::seq_cst) const noexcept;
    operator T*() const volatile noexcept;
    operator T*() const noexcept;

    T* exchange(T*, memory_order = memory_order::seq_cst) volatile noexcept;
    T* exchange(T*, memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_weak(T*&, T*, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(T*&, T*, memory_order, memory_order) noexcept;
    bool compare_exchange_strong(T*&, T*, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(T*&, T*, memory_order, memory_order) noexcept;
    bool compare_exchange_weak(T*&, T*,
                               memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_weak(T*&, T*,
                               memory_order = memory_order::seq_cst) noexcept;
    bool compare_exchange_strong(T*&, T*,
                                 memory_order = memory_order::seq_cst) volatile noexcept;
    bool compare_exchange_strong(T*&, T*,
                                 memory_order = memory_order::seq_cst) noexcept;

    T* fetch_add(ptrdiff_t, memory_order = memory_order::seq_cst) volatile noexcept;
    T* fetch_add(ptrdiff_t, memory_order = memory_order::seq_cst) noexcept;
    T* fetch_sub(ptrdiff_t, memory_order = memory_order::seq_cst) volatile noexcept;
    T* fetch_sub(ptrdiff_t, memory_order = memory_order::seq_cst) noexcept;

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

    void wait(T*, memory_order = memory_order::seq_cst) const volatile noexcept;
    void wait(T*, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() volatile noexcept;
    void notify_one() noexcept;
    void notify_all() volatile noexcept;
    void notify_all() noexcept;
  };
}
```

There is a partial specialization of the `atomic` class template for
pointers. Specializations of this partial specialization are
standard-layout structs. They each have a trivial destructor.

Descriptions are provided below only for members that differ from the
primary template.

The following operations perform pointer arithmetic. The key, operator,
and computation correspondence is:

**Table: Atomic pointer computations** <a id="atomic.types.pointer.comp">[atomic.types.pointer.comp]</a>

|       |     |          |       |     |             |
| ----- | --- | -------- | ----- | --- | ----------- |
| `add` | `+` | addition | `sub` | `-` | subtraction |

``` cpp
T* fetch_key(ptrdiff_t operand, memory_order order = memory_order::seq_cst) volatile noexcept;
T* fetch_key(ptrdiff_t operand, memory_order order = memory_order::seq_cst) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Mandates:* `T` is a complete object type.

[*Note 1*: Pointer arithmetic on `void*` or function pointers is
ill-formed. — *end note*]

*Effects:* Atomically replaces the value pointed to by `this` with the
result of the computation applied to the value pointed to by `this` and
the given `operand`. Memory is affected according to the value of
`order`. These operations are atomic read-modify-write
operations [[intro.multithread]].

*Returns:* Atomically, the value pointed to by `this` immediately before
the effects.

*Remarks:* The result may be an undefined address, but the operations
otherwise have no undefined behavior.

``` cpp
T* operator op=(ptrdiff_t operand) volatile noexcept;
T* operator op=(ptrdiff_t operand) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to:
`return fetch_`*`key`*`(operand) `*`op`*` operand;`

### Member operators common to integers and pointers to objects <a id="atomics.types.memop">[[atomics.types.memop]]</a>

``` cpp
value_type operator++(int) volatile noexcept;
value_type operator++(int) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to: `return fetch_add(1);`

``` cpp
value_type operator--(int) volatile noexcept;
value_type operator--(int) noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to: `return fetch_sub(1);`

``` cpp
value_type operator++() volatile noexcept;
value_type operator++() noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to: `return fetch_add(1) + 1;`

``` cpp
value_type operator--() volatile noexcept;
value_type operator--() noexcept;
```

*Constraints:* For the `volatile` overload of this function,
`is_always_lock_free` is `true`.

*Effects:* Equivalent to: `return fetch_sub(1) - 1;`

### Partial specializations for smart pointers <a id="util.smartptr.atomic">[[util.smartptr.atomic]]</a>

The library provides partial specializations of the `atomic` template
for shared-ownership smart pointers [[smartptr]]. The behavior of all
operations is as specified in [[atomics.types.generic]], unless
specified otherwise. The template parameter `T` of these partial
specializations may be an incomplete type.

All changes to an atomic smart pointer in this subclause, and all
associated `use_count` increments, are guaranteed to be performed
atomically. Associated `use_count` decrements are sequenced after the
atomic operation, but are not required to be part of it. Any associated
deletion and deallocation are sequenced after the atomic update step and
are not part of the atomic operation.

[*Note 1*: If the atomic operation uses locks, locks acquired by the
implementation will be held when any `use_count` adjustments are
performed, and will not be held when any destruction or deallocation
resulting from this is performed. — *end note*]

[*Example 1*:

``` cpp
template<typename T> class atomic_list {
  struct node {
    T t;
    shared_ptr<node> next;
  };
  atomic<shared_ptr<node>> head;

public:
  auto find(T t) const {
    auto p = head.load();
    while (p && p->t != t)
      p = p->next;

    return shared_ptr<node>(move(p));
  }

  void push_front(T t) {
    auto p = make_shared<node>();
    p->t = t;
    p->next = head;
    while (!head.compare_exchange_weak(p->next, p)) {}
  }
};
```

— *end example*]

#### Partial specialization for `shared_ptr` <a id="util.smartptr.atomic.shared">[[util.smartptr.atomic.shared]]</a>

``` cpp
namespace std {
  template<class T> struct atomic<shared_ptr<T>> {
    using value_type = shared_ptr<T>;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const noexcept;

    constexpr atomic() noexcept;
    atomic(shared_ptr<T> desired) noexcept;
    atomic(const atomic&) = delete;
    void operator=(const atomic&) = delete;

    shared_ptr<T> load(memory_order order = memory_order::seq_cst) const noexcept;
    operator shared_ptr<T>() const noexcept;
    void store(shared_ptr<T> desired, memory_order order = memory_order::seq_cst) noexcept;
    void operator=(shared_ptr<T> desired) noexcept;

    shared_ptr<T> exchange(shared_ptr<T> desired,
                           memory_order order = memory_order::seq_cst) noexcept;
    bool compare_exchange_weak(shared_ptr<T>& expected, shared_ptr<T> desired,
                               memory_order success, memory_order failure) noexcept;
    bool compare_exchange_strong(shared_ptr<T>& expected, shared_ptr<T> desired,
                                 memory_order success, memory_order failure) noexcept;
    bool compare_exchange_weak(shared_ptr<T>& expected, shared_ptr<T> desired,
                               memory_order order = memory_order::seq_cst) noexcept;
    bool compare_exchange_strong(shared_ptr<T>& expected, shared_ptr<T> desired,
                                 memory_order order = memory_order::seq_cst) noexcept;

    void wait(shared_ptr<T> old, memory_order order = memory_order::seq_cst) const noexcept;
    void notify_one() noexcept;
    void notify_all() noexcept;

  private:
    shared_ptr<T> p;            // exposition only
  };
}
```

``` cpp
constexpr atomic() noexcept;
```

*Effects:* Initializes `p{}`.

``` cpp
atomic(shared_ptr<T> desired) noexcept;
```

*Effects:* Initializes the object with the value `desired`.
Initialization is not an atomic operation [[intro.multithread]].

[*Note 1*: It is possible to have an access to an atomic object `A`
race with its construction, for example, by communicating the address of
the just-constructed object `A` to another thread via
`memory_order::relaxed` operations on a suitable atomic pointer
variable, and then immediately accessing `A` in the receiving thread.
This results in undefined behavior. — *end note*]

``` cpp
void store(shared_ptr<T> desired, memory_order order = memory_order::seq_cst) noexcept;
```

*Preconditions:* `order` is neither `memory_order::consume`,
`memory_order::acquire`, nor `memory_order::acq_rel`.

*Effects:* Atomically replaces the value pointed to by `this` with the
value of `desired` as if by `p.swap(desired)`. Memory is affected
according to the value of `order`.

``` cpp
void operator=(shared_ptr<T> desired) noexcept;
```

*Effects:* Equivalent to `store(desired)`.

``` cpp
shared_ptr<T> load(memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns `p`.

``` cpp
operator shared_ptr<T>() const noexcept;
```

*Effects:* Equivalent to: `return load();`

``` cpp
shared_ptr<T> exchange(shared_ptr<T> desired, memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Atomically replaces `p` with `desired` as if by
`p.swap(desired)`. Memory is affected according to the value of `order`.
This is an atomic read-modify-write operation [[intro.races]].

*Returns:* Atomically returns the value of `p` immediately before the
effects.

``` cpp
bool compare_exchange_weak(shared_ptr<T>& expected, shared_ptr<T> desired,
                           memory_order success, memory_order failure) noexcept;
bool compare_exchange_strong(shared_ptr<T>& expected, shared_ptr<T> desired,
                             memory_order success, memory_order failure) noexcept;
```

*Preconditions:* `failure` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* If `p` is equivalent to `expected`, assigns `desired` to `p`
and has synchronization semantics corresponding to the value of
`success`, otherwise assigns `p` to `expected` and has synchronization
semantics corresponding to the value of `failure`.

*Returns:* `true` if `p` was equivalent to `expected`, `false`
otherwise.

*Remarks:* Two `shared_ptr` objects are equivalent if they store the
same pointer value and either share ownership or are both empty. The
weak form may fail spuriously. See [[atomics.types.operations]].

If the operation returns `true`, `expected` is not accessed after the
atomic update and the operation is an atomic read-modify-write
operation [[intro.multithread]] on the memory pointed to by `this`.
Otherwise, the operation is an atomic load operation on that memory, and
`expected` is updated with the existing value read from the atomic
object in the attempted atomic update. The `use_count` update
corresponding to the write to `expected` is part of the atomic
operation. The write to `expected` itself is not required to be part of
the atomic operation.

``` cpp
bool compare_exchange_weak(shared_ptr<T>& expected, shared_ptr<T> desired,
                           memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return compare_exchange_weak(expected, desired, order, fail_order);
```

where `fail_order` is the same as `order` except that a value of
`memory_order::acq_rel` shall be replaced by the value
`memory_order::acquire` and a value of `memory_order::release` shall be
replaced by the value `memory_order::relaxed`.

``` cpp
bool compare_exchange_strong(shared_ptr<T>& expected, shared_ptr<T> desired,
                             memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return compare_exchange_strong(expected, desired, order, fail_order);
```

where `fail_order` is the same as `order` except that a value of
`memory_order::acq_rel` shall be replaced by the value
`memory_order::acquire` and a value of `memory_order::release` shall be
replaced by the value `memory_order::relaxed`.

``` cpp
void wait(shared_ptr<T> old, memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `load(order)` and compares it to `old`.
- If the two are not equivalent, returns.
- Blocks until it is unblocked by an atomic notifying operation or is
  unblocked spuriously.

*Remarks:* Two `shared_ptr` objects are equivalent if they store the
same pointer and either share ownership or are both empty. This function
is an atomic waiting operation [[atomics.wait]].

``` cpp
void notify_one() noexcept;
```

*Effects:* Unblocks the execution of at least one atomic waiting
operation that is eligible to be unblocked [[atomics.wait]] by this
call, if any such atomic waiting operations exist.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

``` cpp
void notify_all() noexcept;
```

*Effects:* Unblocks the execution of all atomic waiting operations that
are eligible to be unblocked [[atomics.wait]] by this call.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

#### Partial specialization for `weak_ptr` <a id="util.smartptr.atomic.weak">[[util.smartptr.atomic.weak]]</a>

``` cpp
namespace std {
  template<class T> struct atomic<weak_ptr<T>> {
    using value_type = weak_ptr<T>;

    static constexpr bool is_always_lock_free = implementation-defined  // whether a given atomic type's operations are always lock free;
    bool is_lock_free() const noexcept;

    constexpr atomic() noexcept;
    atomic(weak_ptr<T> desired) noexcept;
    atomic(const atomic&) = delete;
    void operator=(const atomic&) = delete;

    weak_ptr<T> load(memory_order order = memory_order::seq_cst) const noexcept;
    operator weak_ptr<T>() const noexcept;
    void store(weak_ptr<T> desired, memory_order order = memory_order::seq_cst) noexcept;
    void operator=(weak_ptr<T> desired) noexcept;

    weak_ptr<T> exchange(weak_ptr<T> desired,
                         memory_order order = memory_order::seq_cst) noexcept;
    bool compare_exchange_weak(weak_ptr<T>& expected, weak_ptr<T> desired,
                               memory_order success, memory_order failure) noexcept;
    bool compare_exchange_strong(weak_ptr<T>& expected, weak_ptr<T> desired,
                                 memory_order success, memory_order failure) noexcept;
    bool compare_exchange_weak(weak_ptr<T>& expected, weak_ptr<T> desired,
                               memory_order order = memory_order::seq_cst) noexcept;
    bool compare_exchange_strong(weak_ptr<T>& expected, weak_ptr<T> desired,
                                 memory_order order = memory_order::seq_cst) noexcept;

    void wait(weak_ptr<T> old, memory_order order = memory_order::seq_cst) const noexcept;
    void notify_one() noexcept;
    void notify_all() noexcept;

  private:
    weak_ptr<T> p;              // exposition only
  };
}
```

``` cpp
constexpr atomic() noexcept;
```

*Effects:* Initializes `p{}`.

``` cpp
atomic(weak_ptr<T> desired) noexcept;
```

*Effects:* Initializes the object with the value `desired`.
Initialization is not an atomic operation [[intro.multithread]].

[*Note 1*: It is possible to have an access to an atomic object `A`
race with its construction, for example, by communicating the address of
the just-constructed object `A` to another thread via
`memory_order::relaxed` operations on a suitable atomic pointer
variable, and then immediately accessing `A` in the receiving thread.
This results in undefined behavior. — *end note*]

``` cpp
void store(weak_ptr<T> desired, memory_order order = memory_order::seq_cst) noexcept;
```

*Preconditions:* `order` is neither `memory_order::consume`,
`memory_order::acquire`, nor `memory_order::acq_rel`.

*Effects:* Atomically replaces the value pointed to by `this` with the
value of `desired` as if by `p.swap(desired)`. Memory is affected
according to the value of `order`.

``` cpp
void operator=(weak_ptr<T> desired) noexcept;
```

*Effects:* Equivalent to `store(desired)`.

``` cpp
weak_ptr<T> load(memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns `p`.

``` cpp
operator weak_ptr<T>() const noexcept;
```

*Effects:* Equivalent to: `return load();`

``` cpp
weak_ptr<T> exchange(weak_ptr<T> desired, memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Atomically replaces `p` with `desired` as if by
`p.swap(desired)`. Memory is affected according to the value of `order`.
This is an atomic read-modify-write operation [[intro.races]].

*Returns:* Atomically returns the value of `p` immediately before the
effects.

``` cpp
bool compare_exchange_weak(weak_ptr<T>& expected, weak_ptr<T> desired,
                           memory_order success, memory_order failure) noexcept;
bool compare_exchange_strong(weak_ptr<T>& expected, weak_ptr<T> desired,
                             memory_order success, memory_order failure) noexcept;
```

*Preconditions:* `failure` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* If `p` is equivalent to `expected`, assigns `desired` to `p`
and has synchronization semantics corresponding to the value of
`success`, otherwise assigns `p` to `expected` and has synchronization
semantics corresponding to the value of `failure`.

*Returns:* `true` if `p` was equivalent to `expected`, `false`
otherwise.

*Remarks:* Two `weak_ptr` objects are equivalent if they store the same
pointer value and either share ownership or are both empty. The weak
form may fail spuriously. See [[atomics.types.operations]].

If the operation returns `true`, `expected` is not accessed after the
atomic update and the operation is an atomic read-modify-write
operation [[intro.multithread]] on the memory pointed to by `this`.
Otherwise, the operation is an atomic load operation on that memory, and
`expected` is updated with the existing value read from the atomic
object in the attempted atomic update. The `use_count` update
corresponding to the write to `expected` is part of the atomic
operation. The write to `expected` itself is not required to be part of
the atomic operation.

``` cpp
bool compare_exchange_weak(weak_ptr<T>& expected, weak_ptr<T> desired,
                           memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return compare_exchange_weak(expected, desired, order, fail_order);
```

where `fail_order` is the same as `order` except that a value of
`memory_order::acq_rel` shall be replaced by the value
`memory_order::acquire` and a value of `memory_order::release` shall be
replaced by the value `memory_order::relaxed`.

``` cpp
bool compare_exchange_strong(weak_ptr<T>& expected, weak_ptr<T> desired,
                             memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return compare_exchange_strong(expected, desired, order, fail_order);
```

where `fail_order` is the same as `order` except that a value of
`memory_order::acq_rel` shall be replaced by the value
`memory_order::acquire` and a value of `memory_order::release` shall be
replaced by the value `memory_order::relaxed`.

``` cpp
void wait(weak_ptr<T> old, memory_order order = memory_order::seq_cst) const noexcept;
```

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `load(order)` and compares it to `old`.
- If the two are not equivalent, returns.
- Blocks until it is unblocked by an atomic notifying operation or is
  unblocked spuriously.

*Remarks:* Two `weak_ptr` objects are equivalent if they store the same
pointer and either share ownership or are both empty. This function is
an atomic waiting operation [[atomics.wait]].

``` cpp
void notify_one() noexcept;
```

*Effects:* Unblocks the execution of at least one atomic waiting
operation that is eligible to be unblocked [[atomics.wait]] by this
call, if any such atomic waiting operations exist.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

``` cpp
void notify_all() noexcept;
```

*Effects:* Unblocks the execution of all atomic waiting operations that
are eligible to be unblocked [[atomics.wait]] by this call.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

## Non-member functions <a id="atomics.nonmembers">[[atomics.nonmembers]]</a>

A non-member function template whose name matches the pattern `atomic_f`
or the pattern `atomic_f_explicit` invokes the member function `f`, with
the value of the first parameter as the object expression and the values
of the remaining parameters (if any) as the arguments of the member
function call, in order. An argument for a parameter of type
`atomic<T>::value_type*` is dereferenced when passed to the member
function call. If no such member function exists, the program is
ill-formed.

[*Note 1*: The non-member functions enable programmers to write code
that can be compiled as either C or C++, for example in a shared header
file. — *end note*]

## Flag type and operations <a id="atomics.flag">[[atomics.flag]]</a>

``` cpp
namespace std {
  struct atomic_flag {
    constexpr atomic_flag() noexcept;
    atomic_flag(const atomic_flag&) = delete;
    atomic_flag& operator=(const atomic_flag&) = delete;
    atomic_flag& operator=(const atomic_flag&) volatile = delete;

    bool test(memory_order = memory_order::seq_cst) const volatile noexcept;
    bool test(memory_order = memory_order::seq_cst) const noexcept;
    bool test_and_set(memory_order = memory_order::seq_cst) volatile noexcept;
    bool test_and_set(memory_order = memory_order::seq_cst) noexcept;
    void clear(memory_order = memory_order::seq_cst) volatile noexcept;
    void clear(memory_order = memory_order::seq_cst) noexcept;

    void wait(bool, memory_order = memory_order::seq_cst) const volatile noexcept;
    void wait(bool, memory_order = memory_order::seq_cst) const noexcept;
    void notify_one() volatile noexcept;
    void notify_one() noexcept;
    void notify_all() volatile noexcept;
    void notify_all() noexcept;
  };
}
```

The `atomic_flag` type provides the classic test-and-set functionality.
It has two states, set and clear.

Operations on an object of type `atomic_flag` shall be lock-free.

[*Note 1*: Hence the operations should also be
address-free. — *end note*]

The `atomic_flag` type is a standard-layout struct. It has a trivial
destructor.

``` cpp
constexpr atomic_flag::atomic_flag() noexcept;
```

*Effects:* Initializes `*this` to the clear state.

``` cpp
bool atomic_flag_test(const volatile atomic_flag* object) noexcept;
bool atomic_flag_test(const atomic_flag* object) noexcept;
bool atomic_flag_test_explicit(const volatile atomic_flag* object,
                               memory_order order) noexcept;
bool atomic_flag_test_explicit(const atomic_flag* object,
                               memory_order order) noexcept;
bool atomic_flag::test(memory_order order = memory_order::seq_cst) const volatile noexcept;
bool atomic_flag::test(memory_order order = memory_order::seq_cst) const noexcept;
```

For `atomic_flag_test`, let `order` be `memory_order::seq_cst`.

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns the value pointed to by `object` or
`this`.

``` cpp
bool atomic_flag_test_and_set(volatile atomic_flag* object) noexcept;
bool atomic_flag_test_and_set(atomic_flag* object) noexcept;
bool atomic_flag_test_and_set_explicit(volatile atomic_flag* object, memory_order order) noexcept;
bool atomic_flag_test_and_set_explicit(atomic_flag* object, memory_order order) noexcept;
bool atomic_flag::test_and_set(memory_order order = memory_order::seq_cst) volatile noexcept;
bool atomic_flag::test_and_set(memory_order order = memory_order::seq_cst) noexcept;
```

*Effects:* Atomically sets the value pointed to by `object` or by `this`
to `true`. Memory is affected according to the value of `order`. These
operations are atomic read-modify-write
operations [[intro.multithread]].

*Returns:* Atomically, the value of the object immediately before the
effects.

``` cpp
void atomic_flag_clear(volatile atomic_flag* object) noexcept;
void atomic_flag_clear(atomic_flag* object) noexcept;
void atomic_flag_clear_explicit(volatile atomic_flag* object, memory_order order) noexcept;
void atomic_flag_clear_explicit(atomic_flag* object, memory_order order) noexcept;
void atomic_flag::clear(memory_order order = memory_order::seq_cst) volatile noexcept;
void atomic_flag::clear(memory_order order = memory_order::seq_cst) noexcept;
```

*Preconditions:* The `order` argument is neither
`memory_order::consume`, `memory_order::acquire`, nor
`memory_order::acq_rel`.

*Effects:* Atomically sets the value pointed to by `object` or by `this`
to `false`. Memory is affected according to the value of `order`.

``` cpp
void atomic_flag_wait(const volatile atomic_flag* object, bool old) noexcept;
void atomic_flag_wait(const atomic_flag* object, bool old) noexcept;
void atomic_flag_wait_explicit(const volatile atomic_flag* object,
                               bool old, memory_order order) noexcept;
void atomic_flag_wait_explicit(const atomic_flag* object,
                               bool old, memory_order order) noexcept;
void atomic_flag::wait(bool old, memory_order order =
                                   memory_order::seq_cst) const volatile noexcept;
void atomic_flag::wait(bool old, memory_order order =
                                   memory_order::seq_cst) const noexcept;
```

For `atomic_flag_wait`, let `order` be `memory_order::seq_cst`. Let
`flag` be `object` for the non-member functions and `this` for the
member functions.

*Preconditions:* `order` is neither `memory_order::release` nor
`memory_order::acq_rel`.

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `flag->test(order) != old`.
- If the result of that evaluation is `true`, returns.
- Blocks until it is unblocked by an atomic notifying operation or is
  unblocked spuriously.

*Remarks:* This function is an atomic waiting
operation [[atomics.wait]].

``` cpp
void atomic_flag_notify_one(volatile atomic_flag* object) noexcept;
void atomic_flag_notify_one(atomic_flag* object) noexcept;
void atomic_flag::notify_one() volatile noexcept;
void atomic_flag::notify_one() noexcept;
```

*Effects:* Unblocks the execution of at least one atomic waiting
operation that is eligible to be unblocked [[atomics.wait]] by this
call, if any such atomic waiting operations exist.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

``` cpp
void atomic_flag_notify_all(volatile atomic_flag* object) noexcept;
void atomic_flag_notify_all(atomic_flag* object) noexcept;
void atomic_flag::notify_all() volatile noexcept;
void atomic_flag::notify_all() noexcept;
```

*Effects:* Unblocks the execution of all atomic waiting operations that
are eligible to be unblocked [[atomics.wait]] by this call.

*Remarks:* This function is an atomic notifying
operation [[atomics.wait]].

## Fences <a id="atomics.fences">[[atomics.fences]]</a>

This subclause introduces synchronization primitives called *fences*.
Fences can have acquire semantics, release semantics, or both. A fence
with acquire semantics is called an *acquire fence*. A fence with
release semantics is called a *release fence*.

A release fence A synchronizes with an acquire fence B if there exist
atomic operations X and Y, both operating on some atomic object M, such
that A is sequenced before X, X modifies M, Y is sequenced before B, and
Y reads the value written by X or a value written by any side effect in
the hypothetical release sequence X would head if it were a release
operation.

A release fence A synchronizes with an atomic operation B that performs
an acquire operation on an atomic object M if there exists an atomic
operation X such that A is sequenced before X, X modifies M, and B reads
the value written by X or a value written by any side effect in the
hypothetical release sequence X would head if it were a release
operation.

An atomic operation A that is a release operation on an atomic object M
synchronizes with an acquire fence B if there exists some atomic
operation X on M such that X is sequenced before B and reads the value
written by A or a value written by any side effect in the release
sequence headed by A.

``` cpp
extern "C" void atomic_thread_fence(memory_order order) noexcept;
```

*Effects:* Depending on the value of `order`, this operation:

- has no effects, if `order == memory_order::relaxed`;
- is an acquire fence, if `order == memory_order::acquire` or
  `order == memory_order::consume`;
- is a release fence, if `order == memory_order::release`;
- is both an acquire fence and a release fence, if
  `order == memory_order::acq_rel`;
- is a sequentially consistent acquire and release fence, if
  `order == memory_order::seq_cst`.

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
[atomic.types.int.comp]: #atomic.types.int.comp
[atomic.types.pointer.comp]: #atomic.types.pointer.comp
[atomics]: #atomics
[atomics.alias]: #atomics.alias
[atomics.fences]: #atomics.fences
[atomics.flag]: #atomics.flag
[atomics.general]: #atomics.general
[atomics.lockfree]: #atomics.lockfree
[atomics.nonmembers]: #atomics.nonmembers
[atomics.order]: #atomics.order
[atomics.ref.float]: #atomics.ref.float
[atomics.ref.generic]: #atomics.ref.generic
[atomics.ref.int]: #atomics.ref.int
[atomics.ref.memop]: #atomics.ref.memop
[atomics.ref.ops]: #atomics.ref.ops
[atomics.ref.pointer]: #atomics.ref.pointer
[atomics.summary]: #atomics.summary
[atomics.syn]: #atomics.syn
[atomics.types.float]: #atomics.types.float
[atomics.types.generic]: #atomics.types.generic
[atomics.types.int]: #atomics.types.int
[atomics.types.memop]: #atomics.types.memop
[atomics.types.operations]: #atomics.types.operations
[atomics.types.pointer]: #atomics.types.pointer
[atomics.wait]: #atomics.wait
[basic.align]: basic.md#basic.align
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.types]: basic.md#basic.types
[cfenv]: numerics.md#cfenv
[compliance]: library.md#compliance
[expr.pre]: expr.md#expr.pre
[intro.multithread]: basic.md#intro.multithread
[intro.progress]: basic.md#intro.progress
[intro.races]: basic.md#intro.races
[limits.syn]: support.md#limits.syn
[smartptr]: utilities.md#smartptr
[util.smartptr.atomic]: #util.smartptr.atomic
[util.smartptr.atomic.shared]: #util.smartptr.atomic.shared
[util.smartptr.atomic.weak]: #util.smartptr.atomic.weak
