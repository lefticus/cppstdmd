# Atomic operations library <a id="atomics">[[atomics]]</a>

## General <a id="atomics.general">[[atomics.general]]</a>

This Clause describes components for fine-grained atomic access. This
access is provided via operations on atomic objects.

The following subclauses describe atomics requirements and components
for types and operations, as summarized below.

**Table: Atomics library summary**

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

  // [atomics.types.generic], generic types
  template<class T> struct atomic;
  template<> struct atomic<integral>;
  template<class T> struct atomic<T*>;

  // [atomics.types.operations.general], general operations on atomic types
  //  In the following declarations, atomic-type is either
  //  atomic<T> or a named base class for T from
  //  Table~[tab:atomics.integral] or inferred from Table~[tab:atomics.typedefs] or from bool.
  // If it is atomic<T>, then the declaration is a template
  // declaration prefixed with template <class T>.
  bool atomic_is_lock_free(const volatile atomic-type*) noexcept;
  bool atomic_is_lock_free(const atomic-type*) noexcept;
  void atomic_init(volatile atomic-type*, T) noexcept;
  void atomic_init(atomic-type*, T) noexcept;
  void atomic_store(volatile atomic-type*, T) noexcept;
  void atomic_store(atomic-type*, T) noexcept;
  void atomic_store_explicit(volatile atomic-type*, T, memory_order) noexcept;
  void atomic_store_explicit(atomic-type*, T, memory_order) noexcept;
  T atomic_load(const volatile atomic-type*) noexcept;
  T atomic_load(const atomic-type*) noexcept;
  T atomic_load_explicit(const volatile atomic-type*, memory_order) noexcept;
  T atomic_load_explicit(const atomic-type*, memory_order) noexcept;
  T atomic_exchange(volatile atomic-type*, T) noexcept;
  T atomic_exchange(atomic-type*, T) noexcept;
  T atomic_exchange_explicit(volatile atomic-type*, T, memory_order) noexcept;
  T atomic_exchange_explicit(atomic-type*, T, memory_order) noexcept;
  bool atomic_compare_exchange_weak(volatile atomic-type*, T*, T) noexcept;
  bool atomic_compare_exchange_weak(atomic-type*, T*, T) noexcept;
  bool atomic_compare_exchange_strong(volatile atomic-type*, T*, T) noexcept;
  bool atomic_compare_exchange_strong(atomic-type*, T*, T) noexcept;
  bool atomic_compare_exchange_weak_explicit(volatile atomic-type*, T*, T,
    memory_order, memory_order) noexcept;
  bool atomic_compare_exchange_weak_explicit(atomic-type*, T*, T.
    memory_order, memory_order) noexcept;
  bool atomic_compare)exchange_strong_explicit(volatile atomic-type*, T*, T,
    memory_order, memory_order) noexcept;
  bool atomic_compare_exchange_strong_explicit(atomic-type*, T*, T,
    memory_order, memory_order) noexcept;

  // [atomics.types.operations.templ], templated operations on atomic types
  template <class T>
    T atomic_fetch_add(volatile atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_add(atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_add_explicit(volatile atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_add_explicit(atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_sub(volatile atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_sub(atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_sub_explicit(volatile atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_sub_explicit(atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_and(volatile atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_and(atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_and_explicit(volatile atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_and_explicit(atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_or(volatile atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_or(atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_or_explicit(volatile atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_or_explicit(atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_xor(volatile atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_xor(atomic<T>*, T) noexcept;
  template <class T>
    T atomic_fetch_xor_explicit(volatile atomic<T>*, T, memory_order) noexcept;
  template <class T>
    T atomic_fetch_xor_explicit(atomic<T>*, T, memory_order) noexcept;

  // [atomics.types.operations.arith], arithmetic operations on atomic types
  // In the following declarations, atomic-integral is either
  // atomic<T> or a named base class for T from
  // Table~[tab:atomics.integral] or inferred from Table~[tab:atomics.typedefs].
  // If it is atomic<T>, then the declaration is a template
  // specialization declaration prefixed with template <>.

  integral atomic_fetch_add(volatile atomic-integral*, integral) noexcept;
  integral atomic_fetch_add(atomic-integral*, integral) noexcept;
  integral atomic_fetch_add_explicit(volatile atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_add_explicit(atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_sub(volatile atomic-integral*, integral) noexcept;
  integral atomic_fetch_sub(atomic-integral*, integral) noexcept;
  integral atomic_fetch_sub_explicit(volatile atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_sub_explicit(atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_and(volatile atomic-integral*, integral) noexcept;
  integral atomic_fetch_and(atomic-integral*, integral) noexcept;
  integral atomic_fetch_and_explicit(volatile atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_and_explicit(atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_or(volatile atomic-integral*, integral) noexcept;
  integral atomic_fetch_or(atomic-integral*, integral) noexcept;
  integral atomic_fetch_or_explicit(volatile atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_or_explicit(atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_xor(volatile atomic-integral*, integral) noexcept;
  integral atomic_fetch_xor(atomic-integral*, integral) noexcept;
  integral atomic_fetch_xor_explicit(volatile atomic-integral*, integral, memory_order) noexcept;
  integral atomic_fetch_xor_explicit(atomic-integral*, integral, memory_order) noexcept;

  // [atomics.types.operations.pointer], partial specializations for pointers

  template <class T>
    T* atomic_fetch_add(volatile atomic<T*>*, ptrdiff_t) noexcept;
  template <class T>
    T* atomic_fetch_add(atomic<T*>*, ptrdiff_t) noexcept;
  template <class T>
    T* atomic_fetch_add_explicit(volatile atomic<T*>*, ptrdiff_t, memory_order) noexcept;
  template <class T>
    T* atomic_fetch_add_explicit(atomic<T*>*, ptrdiff_t, memory_order) noexcept;
  template <class T>
    T* atomic_fetch_sub(volatile atomic<T*>*, ptrdiff_t) noexcept;
  template <class T>
    T* atomic_fetch_sub(atomic<T*>*, ptrdiff_t) noexcept;
  template <class T>
    T* atomic_fetch_sub_explicit(volatile atomic<T*>*, ptrdiff_t, memory_order) noexcept;
  template <class T>
    T* atomic_fetch_sub_explicit(atomic<T*>*, ptrdiff_t, memory_order) noexcept;

  // [atomics.types.operations.req], initialization
  #define ATOMIC_VAR_INIT(value) see below

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

## Order and consistency <a id="atomics.order">[[atomics.order]]</a>

``` cpp
namespace std {
  typedef enum memory_order {
    memory_order_relaxed, memory_order_consume, memory_order_acquire,
    memory_order_release, memory_order_acq_rel, memory_order_seq_cst
  } memory_order;
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
  on the affected memory location.
- `memory_order_acquire`, `memory_order_acq_rel`, and
  `memory_order_seq_cst`: a load operation performs an acquire operation
  on the affected memory location.

Atomic operations specifying `memory_order_relaxed` are relaxed with
respect to memory ordering. Implementations must still guarantee that
any given atomic access to a particular atomic object be indivisible
with respect to all other atomic accesses to that object.

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
- if *A* exists, the result of some modification of *M* in the visible
  sequence of side effects with respect to *B* that is not
  `memory_order_seq_cst` and that does not happen before *A*, or
- if *A* does not exist, the result of some modification of *M* in the
  visible sequence of side effects with respect to *B* that is not
  `memory_order_seq_cst`.

Although it is not explicitly required that *S* include locks, it can
always be extended to an order that does include lock and unlock
operations, since the ordering between those is already included in the
“happens before” ordering.

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

For atomic operations *A* and *B* on an atomic object *M*, if there are
`memory_order_seq_cst` fences `X` and `Y` such that *A* is sequenced
before *X*, *Y* is sequenced before *B*, and *X* precedes *Y* in *S*,
then *B* occurs later than *A* in the modification order of *M*.

`memory_order_seq_cst` ensures sequential consistency only for a program
that is free of data races and uses exclusively `memory_order_seq_cst`
operations. Any use of weaker ordering will invalidate this guarantee
unless extreme care is used. In particular, `memory_order_seq_cst`
fences ensure a total order only for the fences themselves. Fences
cannot, in general, be used to restore sequential consistency for atomic
operations with weaker ordering specifications.

An atomic store shall only store a value that has been computed from
constants and program input values by a finite sequence of program
evaluations, such that each evaluation observes the values of variables
as computed by the last prior assignment in the sequence. The ordering
of evaluations in this sequence shall be such that:

- if an evaluation *B* observes a value computed by *A* in a different
  thread, then *B* does not happen before *A*, and
- if an evaluation *A* is included in the sequence, then every
  evaluation that assigns to the same variable and happens before *A* is
  included.

The second requirement disallows “out-of-thin-air” or “speculative”
stores of atomics when relaxed atomics are used. Since unordered
operations are involved, evaluations may appear in this sequence out of
thread order. For example, with `x` and `y` initially zero,

``` cpp
// Thread 1:
r1 = y.load(memory_order_relaxed);
x.store(r1, memory_order_relaxed);
```

``` cpp
// Thread 2:
r2 = x.load(memory_order_relaxed);
y.store(42, memory_order_relaxed);
```

is allowed to produce `r1 = r2 = 42`. The sequence of evaluations
justifying this consists of:

``` cpp
y.store(42, memory_order_relaxed);
r1 = y.load(memory_order_relaxed);
x.store(r1, memory_order_relaxed);
r2 = x.load(memory_order_relaxed);
```

On the other hand,

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

may not produce `r1 = r2 = 42`, since there is no sequence of
evaluations that results in the computation of 42. In the absence of
“relaxed” operations and read-modify-write operations with weaker than
`memory_order_acq_rel` ordering, the second requirement has no impact.

The requirements do allow `r1 == r2 == 42` in the following example,
with `x` and `y` initially zero:

``` cpp
// Thread 1:
r1 = x.load(memory_order_relaxed);
if (r1 == 42) y.store(r1, memory_order_relaxed);
```

``` cpp
// Thread 2:
r2 = y.load(memory_order_relaxed);
if (r2 == 42) x.store(42, memory_order_relaxed);
```

However, implementations should not allow such behavior.

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
value ( [[intro.multithread]]).

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

The function `atomic_is_lock_free` ( [[atomics.types.operations]])
indicates whether the object is lock-free. In any given program
execution, the result of the lock-free query shall be consistent for all
pointers of the same type.

Operations that are lock-free should also be address-free. That is,
atomic operations on the same memory location via two different
addresses will communicate atomically. The implementation should not
depend on any per-process state. This restriction enables communication
by memory that is mapped into a process more than once and by memory
that is shared between two processes.

## Atomic types <a id="atomics.types.generic">[[atomics.types.generic]]</a>

``` cpp
namespace std {
  template <class T> struct atomic {
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

  template <> struct atomic<integral> {
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
    bool compare_exchange_weak(integral&, integral, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_weak(integral&, integral, memory_order, memory_order) noexcept;
    bool compare_exchange_strong(integral&, integral, memory_order, memory_order) volatile noexcept;
    bool compare_exchange_strong(integral&, integral, memory_order, memory_order) noexcept;
    bool compare_exchange_weak(integral&, integral, memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_weak(integral&, integral, memory_order = memory_order_seq_cst) noexcept;
    bool compare_exchange_strong(integral&, integral, memory_order = memory_order_seq_cst) volatile noexcept;
    bool compare_exchange_strong(integral&, integral, memory_order = memory_order_seq_cst) noexcept;
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

  template <class T> struct atomic<T*> {
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

There is a generic class template `atomic<T>`. The type of the template
argument `T` shall be trivially copyable ( [[basic.types]]). Type
arguments that are not also statically initializable may be difficult to
use.

The semantics of the operations on specializations of `atomic` are
defined in  [[atomics.types.operations]].

Specializations and instantiations of the `atomic` template shall have a
deleted copy constructor, a deleted copy assignment operator, and a
constexpr value constructor.

There shall be full specializations of the `atomic` template for the
integral types `char`, `signed char`, `unsigned char`, `short`,
`unsigned short`, `int`, `unsigned int`, `long`, `unsigned long`,
`long long`, `unsigned long long`, `char16_t`, `char32_t`, `wchar_t`,
and any other types needed by the typedefs in the header `<cstdint>`.
For each integral type *integral*, the specialization `atomic<integral>`
provides additional atomic operations appropriate to integral types.
There shall be a specialization `atomic<bool>` which provides the
general atomic operations as specified in
[[atomics.types.operations.general]].

The atomic integral specializations and the specialization
`atomic<bool>` shall have standard layout. They shall each have a
trivial default constructor and a trivial destructor. They shall each
support aggregate initialization syntax.

There shall be pointer partial specializations of the `atomic` class
template. These specializations shall have standard layout, trivial
default constructors, and trivial destructors. They shall each support
aggregate initialization syntax.

There shall be named types corresponding to the integral specializations
of `atomic`, as specified in Table  [[tab:atomics.integral]], and a
named type `atomic_bool` corresponding to the specified `atomic<bool>`.
Each named type is a either typedef to the corresponding specialization
or a base class of the corresponding specialization. If it is a base
class, it shall support the same member functions as the corresponding
specialization.

There shall be atomic typedefs corresponding to the typedefs in the
header `<inttypes.h>` as specified in Table  [[tab:atomics.typedefs]].

The representation of an atomic specialization need not have the same
size as its corresponding argument type. Specializations should have the
same size whenever possible, as this reduces the effort required to port
existing code.

## Operations on atomic types <a id="atomics.types.operations">[[atomics.types.operations]]</a>

### General operations on atomic types <a id="atomics.types.operations.general">[[atomics.types.operations.general]]</a>

The implementation shall provide the functions and function templates
identified as “general operations on atomic types” in  [[atomics.syn]].

In the declarations of these functions and function templates, the name
*atomic-type* refers to either `atomic<T>` or to a named base class for
`T` from Table  [[tab:atomics.integral]] or inferred from Table 
[[tab:atomics.typedefs]].

### Templated operations on atomic types <a id="atomics.types.operations.templ">[[atomics.types.operations.templ]]</a>

The implementation shall declare but not define the function templates
identified as “templated operations on atomic types” in 
[[atomics.syn]].

### Arithmetic operations on atomic types <a id="atomics.types.operations.arith">[[atomics.types.operations.arith]]</a>

The implementation shall provide the functions and function template
specializations identified as “arithmetic operations on atomic types”
in  [[atomics.syn]].

In the declarations of these functions and function template
specializations, the name *integral* refers to an integral type and the
name *atomic-integral* refers to either `atomic<integral>` or to a named
base class for `integral` from Table  [[tab:atomics.integral]] or
inferred from Table  [[tab:atomics.typedefs]].

### Operations on atomic pointer types <a id="atomics.types.operations.pointer">[[atomics.types.operations.pointer]]</a>

The implementation shall provide the function template specializations
identified as “partial specializations for pointers” in 
[[atomics.syn]].

### Requirements for operations on atomic types <a id="atomics.types.operations.req">[[atomics.types.operations.req]]</a>

There are only a few kinds of operations on atomic types, though there
are many instances on those kinds. This section specifies each general
kind. The specific instances are defined in [[atomics.types.generic]],
[[atomics.types.operations.general]],
[[atomics.types.operations.arith]], and
[[atomics.types.operations.pointer]].

In the following operation definitions:

- an *A* refers to one of the atomic types.
- a *C* refers to its corresponding non-atomic type. The
  `atomic_address` atomic type corresponds to the `void*` non-atomic
  type.
- an *M* refers to type of the other argument for arithmetic operations.
  For integral atomic types, *M* is *C*. For atomic address types, *M*
  is `std::ptrdiff_t`.
- the free functions not ending in `_explicit` have the semantics of
  their corresponding `_explicit` with `memory_order` arguments of
  `memory_order_seq_cst`.

Many operations are volatile-qualified. The “volatile as device
register” semantics have not changed in the standard. This qualification
means that volatility is preserved when applying these operations to
volatile objects. It does not mean that operations on non-volatile
objects become volatile. Thus, volatile qualified operations on
non-volatile objects may be merged under some conditions.

``` cpp
A::A() noexcept = default;
```

*Effects:* leaves the atomic object in an uninitialized state. These
semantics ensure compatibility with C.

``` cpp
constexpr A::A(C desired) noexcept;
```

*Effects:* Initializes the object with the value `desired`.
Initialization is not an atomic operation ( [[intro.multithread]]). it
is possible to have an access to an atomic object `A` race with its
construction, for example by communicating the address of the
just-constructed object `A` to another thread via `memory_order_relaxed`
operations on a suitable atomic pointer variable, and then immediately
accessing `A` in the receiving thread. This results in undefined
behavior.

``` cpp
#define ATOMIC_VAR_INIT(value) see below
```

The macro expands to a token sequence suitable for constant
initialization of an atomic variable of static storage duration of a
type that is initialization-compatible with *value*. This operation may
need to initialize locks. Concurrent access to the variable being
initialized, even via an atomic operation, constitutes a data race.

``` cpp
atomic<int> v = ATOMIC_VAR_INIT(5);
```

``` cpp
bool atomic_is_lock_free(const volatile A *object) noexcept;
bool atomic_is_lock_free(const A *object) noexcept;
bool A::is_lock_free() const volatile noexcept;
bool A::is_lock_free() const noexcept;
```

*Returns:* True if the object’s operations are lock-free, false
otherwise.

``` cpp
void atomic_init(volatile A *object, C desired) noexcept;
void atomic_init(A *object, C desired) noexcept;
```

*Effects:* Non-atomically initializes `*object` with value `desired`.
This function shall only be applied to objects that have been default
constructed, and then only once. These semantics ensure compatibility
with C. Concurrent access from another thread, even via an atomic
operation, constitutes a data race.

``` cpp
void atomic_store(volatile A* object, C desired) noexcept;
void atomic_store(A* object, C desired) noexcept;
void atomic_store_explicit(volatile A *object, C desired, memory_order order) noexcept;
void atomic_store_explicit(A* object, C desired, memory_order order) noexcept;
void A::store(C desired, memory_order order = memory_order_seq_cst) volatile noexcept;
void A::store(C desired, memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* The `order` argument shall not be `memory_order_consume`,
`memory_order_acquire`, nor `memory_order_acq_rel`.

*Effects:* Atomically replaces the value pointed to by `object` or by
`this` with the value of `desired`. Memory is affected according to the
value of `order`.

``` cpp
C A::operator=(C desired) volatile noexcept;
C A::operator=(C desired) noexcept;
```

*Effects:* `store(desired)`

*Returns:* `desired`

``` cpp
C atomic_load(const volatile A* object) noexcept;
C atomic_load(const A* object) noexcept;
C atomic_load_explicit(const volatile A* object, memory_order) noexcept;
C atomic_load_explicit(const A* object, memory_order) noexcept;
C A::load(memory_order order = memory_order_seq_cst) const volatile noexcept;
C A::load(memory_order order = memory_order_seq_cst) const noexcept;
```

*Requires:* The `order` argument shall not be `memory_order_release` nor
`memory_order_acq_rel`.

*Effects:* Memory is affected according to the value of `order`.

*Returns:* Atomically returns the value pointed to by `object` or by
`this`.

``` cpp
A::operator C() const volatile noexcept;
A::operator C() const noexcept;
```

*Effects:* `load()`

*Returns:* The result of `load()`.

``` cpp
C atomic_exchange(volatile A* object, C desired) noexcept;
C atomic_exchange(A* object, C desired) noexcept;
C atomic_exchange_explicit(volatile A* object, C desired, memory_order) noexcept;
C atomic_exchange_explicit(A* object, C desired, memory_order) noexcept;
C A::exchange(C desired, memory_order order = memory_order_seq_cst) volatile noexcept;
C A::exchange(C desired, memory_order order = memory_order_seq_cst) noexcept;
```

*Effects:* Atomically replaces the value pointed to by `object` or by
`this` with `desired`. Memory is affected according to the value of
`order`. These operations are atomic read-modify-write
operations ( [[intro.multithread]]).

*Returns:* Atomically returns the value pointed to by `object` or by
`this` immediately before the effects.

``` cpp
bool atomic_compare_exchange_weak(volatile A* object, C* expected, C desired) noexcept;
bool atomic_compare_exchange_weak(A* object, C* expected, C desired) noexcept;
bool atomic_compare_exchange_strong(volatile A* object, C* expected, C desired) noexcept;
bool atomic_compare_exchange_strong(A* object, C* expected, C desired) noexcept;
bool atomic_compare_exchange_weak_explicit(volatile A* object, C* expected, C desired,
    memory_order success, memory_order failure) noexcept;
bool atomic_compare_exchange_weak_explicit(A* object, C* expected, C desired,
    memory_order success, memory_order failure) noexcept;
bool atomic_compare_exchange_strong_explicit(volatile A* object, C* expected, C desired,
    memory_order success, memory_order failure) noexcept;
bool atomic_compare_exchange_strong_explicit(A* object, C* expected, C desired,
    memory_order success, memory_order failure) noexcept;
bool A::compare_exchange_weak(C& expected, C desired,
    memory_order success, memory_order failure) volatile noexcept;
bool A::compare_exchange_weak(C& expected, C desired,
    memory_order success, memory_order failure) noexcept;
bool A::compare_exchange_strong(C& expected, C desired,
    memory_order success, memory_order failure) volatile noexcept;
bool A::compare_exchange_strong(C& expected, C desired,
    memory_order success, memory_order failure) noexcept;
bool A::compare_exchange_weak(C& expected, C desired,
    memory_order order = memory_order_seq_cst) volatile noexcept;
bool A::compare_exchange_weak(C& expected, C desired,
    memory_order order = memory_order_seq_cst) noexcept;
bool A::compare_exchange_strong(C& expected, C desired,
    memory_order order = memory_order_seq_cst) volatile noexcept;
bool A::compare_exchange_strong(C& expected, C desired,
    memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* The `failure` argument shall not be `memory_order_release`
nor `memory_order_acq_rel`. The `failure` argument shall be no stronger
than the `success` argument.

*Effects:* Atomically, compares the contents of the memory pointed to by
`object` or by `this` for equality with that in `expected`, and if true,
replaces the contents of the memory pointed to by `object` or by `this`
with that in `desired`, and if false, updates the contents of the memory
in `expected` with the contents of the memory pointed to by `object` or
by `this`. Further, if the comparison is true, memory is affected
according to the value of `success`, and if the comparison is false,
memory is affected according to the value of `failure`. When only one
`memory_order` argument is supplied, the value of `success` is `order`,
and the value of `failure` is `order` except that a value of
`memory_order_acq_rel` shall be replaced by the value
`memory_order_acquire` and a value of `memory_order_release` shall be
replaced by the value `memory_order_relaxed`. If the operation returns
`true`, these operations are atomic read-modify-write
operations ( [[intro.multithread]]). Otherwise, these operations are
atomic load operations.

*Returns:* The result of the comparison.

For example, the effect of `atomic_compare_exchange_strong` is

``` cpp
if (memcmp(object, expected, sizeof(*object)) == 0)
  memcpy(object, &desired, sizeof(*object));
else
  memcpy(expected, object, sizeof(*object));
```

the expected use of the compare-and-exchange operations is as follows.
The compare-and-exchange operations will update `expected` when another
iteration of the loop is needed.

``` cpp
expected = current.load();
do {
  desired = function(expected);
} while (!current.compare_exchange_weak(expected, desired));
```

Implementations should ensure that weak compare-and-exchange operations
do not consistently return `false` unless either the atomic object has
value different from `expected` or there are concurrent modifications to
the atomic object.

A weak compare-and-exchange operation may fail spuriously. That is, even
when the contents of memory referred to by `expected` and `object` are
equal, it may return false and store back to `expected` the same memory
contents that were originally there. This spurious failure enables
implementation of compare-and-exchange on a broader class of machines,
e.g., load-locked store-conditional machines. A consequence of spurious
failure is that nearly all uses of weak compare-and-exchange will be in
a loop.

When a compare-and-exchange is in a loop, the weak version will yield
better performance on some platforms. When a weak compare-and-exchange
would require a loop and a strong one would not, the strong one is
preferable.

The `memcpy` and `memcmp` semantics of the compare-and-exchange
operations may result in failed comparisons for values that compare
equal with `operator==` if the underlying type has padding bits, trap
bits, or alternate representations of the same value. Thus,
`compare_exchange_strong` should be used with extreme care. On the other
hand, `compare_exchange_weak` should converge rapidly.

The following operations perform arithmetic computations. The key,
operator, and computation correspondence is:

**Table: Atomic arithmetic computations**

|       |     |                      |       |        |                      |
| ----- | --- | -------------------- | ----- | ------ | -------------------- |
| `add` | `+` | addition             | `sub` | `-`    | subtraction          |
| `or`  | `|` | bitwise inclusive or | `xor` | `\^{}` | bitwise exclusive or |
| `and` | `&` | bitwise and          |       |        |                      |

``` cpp
C atomic_fetch_key(volatile A *object, M operand) noexcept;
C atomic_fetch_key(A* object, M operand) noexcept;
C atomic_fetch_key_explicit(volatile A *object, M operand, memory_order order) noexcept;
C atomic_fetch_key_explicit(A* object, M operand, memory_order order) noexcept;
C A::fetch_key(M operand, memory_order order = memory_order_seq_cst) volatile noexcept;
C A::fetch_key(M operand, memory_order order = memory_order_seq_cst) noexcept;
```

*Effects:* Atomically replaces the value pointed to by `object` or by
`this` with the result of the *computation* applied to the value pointed
to by `object` or by `this` and the given `operand`. Memory is affected
according to the value of `order`. These operations are atomic
read-modify-write operations ( [[intro.multithread]]).

*Returns:* Atomically, the value pointed to by `object` or by `this`
immediately before the effects.

For signed integer types, arithmetic is defined to use two’s complement
representation. There are no undefined results. For address types, the
result may be an undefined address, but the operations otherwise have no
undefined behavior.

``` cpp
C A::operator op=(M operand) volatile noexcept;
C A::operator op=(M operand) noexcept;
```

*Effects:* `fetch_`*`key`*`(operand)`

*Returns:* `fetch_`*`key`*`(operand) op operand`

``` cpp
C A::operator++(int) volatile noexcept;
C A::operator++(int) noexcept;
```

*Returns:* `fetch_add(1)`

``` cpp
C A::operator--(int) volatile noexcept;
C A::operator--(int) noexcept;
```

*Returns:* `fetch_sub(1)`

``` cpp
C A::operator++() volatile noexcept;
C A::operator++() noexcept;
```

*Effects:* `fetch_add(1)`

*Returns:* `fetch_add(1) + 1`

``` cpp
C A::operator--() volatile noexcept;
C A::operator--() noexcept;
```

*Effects:* `fetch_sub(1)`

*Returns:* `fetch_sub(1) - 1`

## Flag type and operations <a id="atomics.flag">[[atomics.flag]]</a>

``` cpp
namespace std {
  typedef struct atomic_flag {
    bool test_and_set(memory_order = memory_order_seq_cst) volatile noexcept;
    bool test_and_set(memory_order = memory_order_seq_cst) noexcept;
    void clear(memory_order = memory_order_seq_cst) volatile noexcept;
    void clear(memory_order = memory_order_seq_cst) noexcept;

    atomic_flag() noexcept = default;
    atomic_flag(const atomic_flag&) = delete;
    atomic_flag& operator=(const atomic_flag&) = delete;
    atomic_flag& operator=(const atomic_flag&) volatile = delete;
  } atomic_flag;

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

Operations on an object of type `atomic_flag` shall be lock-free. Hence
the operations should also be address-free. No other type requires
lock-free operations, so the `atomic_flag` type is the minimum
hardware-implemented type needed to conform to this International
standard. The remaining types can be emulated with `atomic_flag`, though
with less than ideal properties.

The `atomic_flag` type shall have standard layout. It shall have a
trivial default constructor, a deleted copy constructor, a deleted copy
assignment operator, and a trivial destructor.

The macro `ATOMIC_FLAG_INIT` shall be defined in such a way that it can
be used to initialize an object of type `atomic_flag` to the clear
state. For a static-duration object, that initialization shall be
static. It is unspecified whether an uninitialized `atomic_flag` object
has an initial state of set or clear.

``` cpp
atomic_flag guard = ATOMIC_FLAG_INIT;
```

``` cpp
bool atomic_flag_test_and_set(volatile atomic_flag *object) noexcept;
bool atomic_flag_test_and_set(atomic_flag *object) noexcept;
bool atomic_flag_test_and_set_explicit(volatile atomic_flag *object, memory_order order) noexcept;
bool atomic_flag_test_and_set_explicit(atomic_flag *object, memory_order order) noexcept;
bool atomic_flag::test_and_set(memory_order order = memory_order_seq_cst) volatile noexcept;
bool atomic_flag::test_and_set(memory_order order = memory_order_seq_cst) noexcept;
```

*Effects:* Atomically sets the value pointed to by `object` or by `this`
to true. Memory is affected according to the value of `order`. These
operations are atomic read-modify-write
operations ( [[intro.multithread]]).

*Returns:* Atomically, the value of the object immediately before the
effects.

``` cpp
void atomic_flag_clear(volatile atomic_flag *object) noexcept;
void atomic_flag_clear(atomic_flag *object) noexcept;
void atomic_flag_clear_explicit(volatile atomic_flag *object, memory_order order) noexcept;
void atomic_flag_clear_explicit(atomic_flag *object, memory_order order) noexcept;
void atomic_flag::clear(memory_order order = memory_order_seq_cst) volatile noexcept;
void atomic_flag::clear(memory_order order = memory_order_seq_cst) noexcept;
```

*Requires:* The `order` argument shall not be `memory_order_acquire` or
`memory_order_acq_rel`.

*Effects:* Atomically sets the value pointed to by `object` or by `this`
to false. Memory is affected according to the value of `order`.

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

*Effects:* depending on the value of `order`, this operation:

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

*Effects:* equivalent to `atomic_thread_fence(order)`, except that the
resulting ordering constraints are established only between a thread and
a signal handler executed in the same thread.

*Note:* `atomic_signal_fence` can be used to specify the order in which
actions performed by the thread become visible to the signal handler.

*Note:* compiler optimizations and reorderings of loads and stores are
inhibited in the same way as with `atomic_thread_fence`, but the
hardware fence instructions that `atomic_thread_fence` would have
inserted are not emitted.

<!-- Section link definitions -->
[atomics]: #atomics
[atomics.fences]: #atomics.fences
[atomics.flag]: #atomics.flag
[atomics.general]: #atomics.general
[atomics.lockfree]: #atomics.lockfree
[atomics.order]: #atomics.order
[atomics.syn]: #atomics.syn
[atomics.types.generic]: #atomics.types.generic
[atomics.types.operations]: #atomics.types.operations
[atomics.types.operations.arith]: #atomics.types.operations.arith
[atomics.types.operations.general]: #atomics.types.operations.general
[atomics.types.operations.pointer]: #atomics.types.operations.pointer
[atomics.types.operations.req]: #atomics.types.operations.req
[atomics.types.operations.templ]: #atomics.types.operations.templ

<!-- Link reference definitions -->
[atomics.fences]: #atomics.fences
[atomics.flag]: #atomics.flag
[atomics.lockfree]: #atomics.lockfree
[atomics.order]: #atomics.order
[atomics.syn]: #atomics.syn
[atomics.types.generic]: #atomics.types.generic
[atomics.types.operations]: #atomics.types.operations
[atomics.types.operations.arith]: #atomics.types.operations.arith
[atomics.types.operations.general]: #atomics.types.operations.general
[atomics.types.operations.pointer]: #atomics.types.operations.pointer
[basic.types]: basic.md#basic.types
[intro.multithread]: intro.md#intro.multithread
[tab:atomics.integral]: #tab:atomics.integral
[tab:atomics.typedefs]: #tab:atomics.typedefs
