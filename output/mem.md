---
current_file: mem
label_index_file: converted/cppstdmd/output/cpp_std_labels.lua
source_dir: ../../cplusplus-draft/source
---

# Memory management library <a id="mem">[[mem]]</a>

## General <a id="mem.general">[[mem.general]]</a>

This Clause describes components for memory management.

The following subclauses describe general memory management facilities,
smart pointers, memory resources, and scoped allocators, as summarized
in [[mem.summary]].

**Table: Memory management library summary**

| Subclause |  | Header |
| --- | --- | --- |
| [[memory]] | Memory | `<cstdlib>`, `<memory>` |
| [[smartptr]] | Smart pointers | `<memory>` |
| [[mem.res]] | Memory resources | `<memory_resource>` |
| [[allocator.adaptor]] | Scoped allocators | `<scoped_allocator>` |


## Memory <a id="memory">[[memory]]</a>

### In general <a id="memory.general">[[memory.general]]</a>

Subclause  [[memory]] describes the contents of the header `<memory>`
and some of the contents of the header `<cstdlib>`.

### Header `<memory>` synopsis <a id="memory.syn">[[memory.syn]]</a>

The header `<memory>` defines several types and function templates that
describe properties of pointers and pointer-like types, manage memory
for containers and other template types, destroy objects, and construct
objects in uninitialized memory buffers ( [[pointer.traits]]–
[[specialized.addressof]] and [[specialized.algorithms]]). The header
also defines the templates `unique_ptr`, `shared_ptr`, `weak_ptr`,
`out_ptr_t`, `inout_ptr_t`, and various function templates that operate
on objects of these types [[smartptr]].

Let `POINTER_OF(T)` denote a type that is

- `T::pointer` if the *qualified-id* `T::pointer` is valid and denotes a
  type,
- otherwise, `T::element_type*` if the *qualified-id* `T::element_type`
  is valid and denotes a type,
- otherwise, `pointer_traits<T>::element_type*`.

Let `POINTER_OF_OR(T, U)` denote a type that is:

- `\exposid{POINTER_OF}(T)`
  if `POINTER_OF(T)` is valid and denotes a type,
- otherwise, `U`.

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  // [pointer.traits], pointer traits
  template<class Ptr> struct pointer_traits;                                        // freestanding
  template<class T> struct pointer_traits<T*>;                                      // freestanding

  // [pointer.conversion], pointer conversion
  template<class T>
    constexpr T* to_address(T* p) noexcept;                                         // freestanding
  template<class Ptr>
    constexpr auto to_address(const Ptr& p) noexcept;                               // freestanding

  // [ptr.align], pointer alignment
  void* align(size_t alignment, size_t size, void*& ptr, size_t& space);            // freestanding
  template<size_t N, class T>
    [[nodiscard]] constexpr T* assume_aligned(T* ptr);                              // freestanding

  // [obj.lifetime], explicit lifetime management
  template<class T>
    T* start_lifetime_as(void* p) noexcept;                                         // freestanding
  template<class T>
    const T* start_lifetime_as(const void* p) noexcept;                             // freestanding
  template<class T>
    volatile T* start_lifetime_as(volatile void* p) noexcept;                       // freestanding
  template<class T>
    const volatile T* start_lifetime_as(const volatile void* p) noexcept;           // freestanding
  template<class T>
    T* start_lifetime_as_array(void* p, size_t n) noexcept;                         // freestanding
  template<class T>
    const T* start_lifetime_as_array(const void* p, size_t n) noexcept;             // freestanding
  template<class T>
    volatile T* start_lifetime_as_array(volatile void* p, size_t n) noexcept;       // freestanding
  template<class T>
    const volatile T* start_lifetime_as_array(const volatile void* p,               // freestanding
                                          size_t n) noexcept;

  // [allocator.tag], allocator argument tag
  struct allocator_arg_t {                                                          // freestanding
      explicit allocator_arg_t() = default;                                         // freestanding
  };
  inline constexpr allocator_arg_t allocator_arg{};                                 // freestanding

  // [allocator.uses], uses_allocator
  template<class T, class Alloc> struct uses_allocator;                             // freestanding

  // [allocator.uses.trait], uses_allocator
  template<class T, class Alloc>
    constexpr bool \libglobal{uses_allocator_v} = uses_allocator<T, Alloc>::value;              // freestanding

  // [allocator.uses.construction], uses-allocator construction
  template<class T, class Alloc, class... Args>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    Args&&... args) noexcept;
  template<class T, class Alloc, class Tuple1, class Tuple2>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    piecewise_construct_t,
                                                    Tuple1&& x, Tuple2&& y) noexcept;
  template<class T, class Alloc>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc) noexcept;   // freestanding
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    U&& u, V&& v) noexcept;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    pair<U, V>& pr) noexcept;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    const pair<U, V>& pr) noexcept;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    pair<U, V>&& pr) noexcept;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    const pair<U, V>&& pr) noexcept;
  template<class T, class Alloc, pair-like P>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    P&& p) noexcept;
  template<class T, class Alloc, class U>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,             // freestanding
                                                    U&& u) noexcept;
  template<class T, class Alloc, class... Args>
    constexpr T make_obj_using_allocator(const Alloc& alloc, Args&&... args);       // freestanding
  template<class T, class Alloc, class... Args>
    constexpr T* uninitialized_construct_using_allocator(T* p,                      // freestanding
                                                         const Alloc& alloc, Args&&... args);

  // [allocator.traits], allocator traits
  template<class Alloc> struct allocator_traits;                                    // freestanding

  template<class Pointer, class SizeType = size_t>
  struct allocation_result {                                                        // freestanding
    Pointer ptr;
    SizeType count;
  };

  // [default.allocator], the default allocator
  template<class T> class allocator;
  template<class T, class U>
    constexpr bool operator==(const allocator<T>&, const allocator<U>&) noexcept;

  // [specialized.addressof], addressof
  template<class T>
    constexpr T* addressof(T& r) noexcept;                                          // freestanding
  template<class T>
    const T* addressof(const T&&) = delete;                                         // freestanding

  // [specialized.algorithms], specialized algorithms
  // [special.mem.concepts], special memory concepts
  template<class I>
    concept nothrow-input-iterator = see below;    // exposition only
  template<class I>
    concept nothrow-forward-iterator = see below;  // exposition only
  template<class S, class I>
    concept nothrow-sentinel-for = see below;      // exposition only
  template<class R>
    concept nothrow-input-range = see below;       // exposition only
  template<class R>
    concept nothrow-forward-range = see below;     // exposition only

  template<class NoThrowForwardIterator>
    void uninitialized_default_construct(NoThrowForwardIterator first,              // freestanding
                                         NoThrowForwardIterator last);
  template<class ExecutionPolicy, class NoThrowForwardIterator>
    void uninitialized_default_construct(ExecutionPolicy&& exec,                    // see [algorithms.parallel.overloads]
                                         NoThrowForwardIterator first,
                                         NoThrowForwardIterator last);
  template<class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_default_construct_n(NoThrowForwardIterator first, Size n);      // freestanding
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_default_construct_n(ExecutionPolicy&& exec,                     // see [algorithms.parallel.overloads]
                                        NoThrowForwardIterator first, Size n);

  namespace ranges {
    template<nothrow-forward-iterator I, nothrow-sentinel-for<I> S>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_default_construct(I first, S last);                         // freestanding
    template<nothrow-forward-range R>
      requires default_initializable<range_value_t<R>>
        borrowed_iterator_t<R> uninitialized_default_construct(R&& r);              // freestanding

    template<nothrow-forward-iterator I>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_default_construct_n(I first, iter_difference_t<I> n);       // freestanding
  }

  template<class NoThrowForwardIterator>
    void uninitialized_value_construct(NoThrowForwardIterator first,                // freestanding
                                       NoThrowForwardIterator last);
  template<class ExecutionPolicy, class NoThrowForwardIterator>
    void uninitialized_value_construct(ExecutionPolicy&& exec,                      // see [algorithms.parallel.overloads]
                                       NoThrowForwardIterator first,
                                       NoThrowForwardIterator last);
  template<class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_value_construct_n(NoThrowForwardIterator first, Size n);        // freestanding
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_value_construct_n(ExecutionPolicy&& exec,                       // see [algorithms.parallel.overloads]
                                      NoThrowForwardIterator first, Size n);

  namespace ranges {
    template<nothrow-forward-iterator I, nothrow-sentinel-for<I> S>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_value_construct(I first, S last);                           // freestanding
    template<nothrow-forward-range R>
      requires default_initializable<range_value_t<R>>
        borrowed_iterator_t<R> uninitialized_value_construct(R&& r);                // freestanding

    template<nothrow-forward-iterator I>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_value_construct_n(I first, iter_difference_t<I> n);         // freestanding
  }

  template<class InputIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy(InputIterator first,                  // freestanding
                                              InputIterator last,
                                              NoThrowForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy(ExecutionPolicy&& exec,               // see [algorithms.parallel.overloads]
                                              ForwardIterator first, ForwardIterator last,
                                              NoThrowForwardIterator result);
  template<class InputIterator, class Size, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy_n(InputIterator first, Size n,        // freestanding
                                                NoThrowForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator, class Size,
           class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy_n(ExecutionPolicy&& exec,             // see [algorithms.parallel.overloads]
                                                ForwardIterator first, Size n,
                                                NoThrowForwardIterator result);

  namespace ranges {
    template<class I, class O>
      using uninitialized_copy_result = in_out_result<I, O>;                        // freestanding
    template<input_iterator I, sentinel_for<I> S1,
             nothrow-forward-iterator O, nothrow-sentinel-for<O> S2>
      requires constructible_from<iter_value_t<O>, iter_reference_t<I>>
        uninitialized_copy_result<I, O>
          uninitialized_copy(I ifirst, S1 ilast, O ofirst, S2 olast);               // freestanding
    template<input_range IR, nothrow-forward-range OR>
      requires constructible_from<range_value_t<OR>, range_reference_t<IR>>
        uninitialized_copy_result<borrowed_iterator_t<IR>, borrowed_iterator_t<OR>>
          uninitialized_copy(IR&& in_range, OR&& out_range);                        // freestanding

    template<class I, class O>
      using uninitialized_copy_n_result = in_out_result<I, O>;                      // freestanding
    template<input_iterator I, nothrow-forward-iterator O, nothrow-sentinel-for<O> S>
      requires constructible_from<iter_value_t<O>, iter_reference_t<I>>
        uninitialized_copy_n_result<I, O>
          uninitialized_copy_n(I ifirst, iter_difference_t<I> n,                    // freestanding
                               O ofirst, S olast);
  }

  template<class InputIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_move(InputIterator first,                  // freestanding
                                              InputIterator last,
                                              NoThrowForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_move(ExecutionPolicy&& exec,               // see [algorithms.parallel.overloads]
                                              ForwardIterator first, ForwardIterator last,
                                              NoThrowForwardIterator result);
  template<class InputIterator, class Size, class NoThrowForwardIterator>
    pair<InputIterator, NoThrowForwardIterator>
      uninitialized_move_n(InputIterator first, Size n,                             // freestanding
                           NoThrowForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator, class Size,
           class NoThrowForwardIterator>
    pair<ForwardIterator, NoThrowForwardIterator>
      uninitialized_move_n(ExecutionPolicy&& exec,                                  // see [algorithms.parallel.overloads]
                           ForwardIterator first, Size n, NoThrowForwardIterator result);

  namespace ranges {
    template<class I, class O>
      using uninitialized_move_result = in_out_result<I, O>;                        // freestanding
    template<input_iterator I, sentinel_for<I> S1,
             nothrow-forward-iterator O, nothrow-sentinel-for<O> S2>
      requires constructible_from<iter_value_t<O>, iter_rvalue_reference_t<I>>
        uninitialized_move_result<I, O>
          uninitialized_move(I ifirst, S1 ilast, O ofirst, S2 olast);               // freestanding
    template<input_range IR, nothrow-forward-range OR>
      requires constructible_from<range_value_t<OR>, range_rvalue_reference_t<IR>>
        uninitialized_move_result<borrowed_iterator_t<IR>, borrowed_iterator_t<OR>>
          uninitialized_move(IR&& in_range, OR&& out_range);                        // freestanding

    template<class I, class O>
      using uninitialized_move_n_result = in_out_result<I, O>;                      // freestanding
    template<input_iterator I,
             nothrow-forward-iterator O, nothrow-sentinel-for<O> S>
      requires constructible_from<iter_value_t<O>, iter_rvalue_reference_t<I>>
        uninitialized_move_n_result<I, O>
          uninitialized_move_n(I ifirst, iter_difference_t<I> n,                    // freestanding
                               O ofirst, S olast);
  }

  template<class NoThrowForwardIterator, class T>
    void uninitialized_fill(NoThrowForwardIterator first,                           // freestanding
                            NoThrowForwardIterator last, const T& x);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class T>
    void uninitialized_fill(ExecutionPolicy&& exec,                                 // see [algorithms.parallel.overloads]
                            NoThrowForwardIterator first, NoThrowForwardIterator last,
                            const T& x);
  template<class NoThrowForwardIterator, class Size, class T>
    NoThrowForwardIterator
      uninitialized_fill_n(NoThrowForwardIterator first, Size n, const T& x);       // freestanding
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size, class T>
    NoThrowForwardIterator
      uninitialized_fill_n(ExecutionPolicy&& exec,                                  // see [algorithms.parallel.overloads]
                           NoThrowForwardIterator first, Size n, const T& x);

  namespace ranges {
    template<nothrow-forward-iterator I, nothrow-sentinel-for<I> S, class T>
      requires constructible_from<iter_value_t<I>, const T&>
        I uninitialized_fill(I first, S last, const T& x);                          // freestanding
    template<nothrow-forward-range R, class T>
      requires constructible_from<range_value_t<R>, const T&>
        borrowed_iterator_t<R> uninitialized_fill(R&& r, const T& x);               // freestanding

    template<nothrow-forward-iterator I, class T>
      requires constructible_from<iter_value_t<I>, const T&>
        I uninitialized_fill_n(I first, iter_difference_t<I> n, const T& x);        // freestanding
  }

  // [specialized.construct], construct_at
  template<class T, class... Args>
    constexpr T* construct_at(T* location, Args&&... args);                         // freestanding

  namespace ranges {
    template<class T, class... Args>
      constexpr T* construct_at(T* location, Args&&... args);                       // freestanding
  }

  // [specialized.destroy], destroy
  template<class T>
    constexpr void destroy_at(T* location);                                         // freestanding
  template<class NoThrowForwardIterator>
    constexpr void destroy(NoThrowForwardIterator first,                            // freestanding
                           NoThrowForwardIterator last);
  template<class ExecutionPolicy, class NoThrowForwardIterator>
    void destroy(ExecutionPolicy&& exec,                                            // see [algorithms.parallel.overloads]
                 NoThrowForwardIterator first, NoThrowForwardIterator last);
  template<class NoThrowForwardIterator, class Size>
    constexpr NoThrowForwardIterator destroy_n(NoThrowForwardIterator first,        // freestanding
                                               Size n);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator destroy_n(ExecutionPolicy&& exec,                        // see [algorithms.parallel.overloads]
                                     NoThrowForwardIterator first, Size n);

  namespace ranges {
    template<destructible T>
      constexpr void destroy_at(T* location) noexcept;                              // freestanding

    template<nothrow-input-iterator I, nothrow-sentinel-for<I> S>
      requires destructible<iter_value_t<I>>
        constexpr I destroy(I first, S last) noexcept;                              // freestanding
    template<nothrow-input-range R>
      requires destructible<range_value_t<R>>
        constexpr borrowed_iterator_t<R> destroy(R&& r) noexcept;                   // freestanding

    template<nothrow-input-iterator I>
      requires destructible<iter_value_t<I>>
        constexpr I destroy_n(I first, iter_difference_t<I> n) noexcept;            // freestanding
  }

  // [unique.ptr], class template unique_ptr
  template<class T> struct default_delete;                                          // freestanding
  template<class T> struct default_delete<T[]>;                                     // freestanding
  template<class T, class D = default_delete<T>> class unique_ptr;                  // freestanding
  template<class T, class D> class unique_ptr<T[], D>;                              // freestanding

  template<class T, class... Args>
    constexpr unique_ptr<T> make_unique(Args&&... args);                        // T is not array
  template<class T>
    constexpr unique_ptr<T> make_unique(size_t n);                              // T is U[]
  template<class T, class... Args>
    unspecifiednc make_unique(Args&&...) = delete;                                // T is U[N]

  template<class T>
    constexpr unique_ptr<T> make_unique_for_overwrite();                        // T is not array
  template<class T>
    constexpr unique_ptr<T> make_unique_for_overwrite(size_t n);                // T is U[]
  template<class T, class... Args>
    unspecifiednc make_unique_for_overwrite(Args&&...) = delete;                  // T is U[N]

  template<class T, class D>
    constexpr void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;         // freestanding

  template<class T1, class D1, class T2, class D2>
    constexpr bool operator==(const unique_ptr<T1, D1>& x,                          // freestanding
                              const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);       // freestanding
  template<class T1, class D1, class T2, class D2>
    bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);       // freestanding
  template<class T1, class D1, class T2, class D2>
    bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);      // freestanding
  template<class T1, class D1, class T2, class D2>
    bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);      // freestanding
  template<class T1, class D1, class T2, class D2>
    requires three_way_comparable_with<typename unique_ptr<T1, D1>::pointer,
                                       typename unique_ptr<T2, D2>::pointer>
    compare_three_way_result_t<typename unique_ptr<T1, D1>::pointer,
                               typename unique_ptr<T2, D2>::pointer>
      operator<=>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);        // freestanding

  template<class T, class D>
    constexpr bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;       // freestanding
  template<class T, class D>
    constexpr bool operator<(const unique_ptr<T, D>& x, nullptr_t);                 // freestanding
  template<class T, class D>
    constexpr bool operator<(nullptr_t, const unique_ptr<T, D>& y);                 // freestanding
  template<class T, class D>
    constexpr bool operator>(const unique_ptr<T, D>& x, nullptr_t);                 // freestanding
  template<class T, class D>
    constexpr bool operator>(nullptr_t, const unique_ptr<T, D>& y);                 // freestanding
  template<class T, class D>
    constexpr bool operator<=(const unique_ptr<T, D>& x, nullptr_t);                // freestanding
  template<class T, class D>
    constexpr bool operator<=(nullptr_t, const unique_ptr<T, D>& y);                // freestanding
  template<class T, class D>
    constexpr bool operator>=(const unique_ptr<T, D>& x, nullptr_t);                // freestanding
  template<class T, class D>
    constexpr bool operator>=(nullptr_t, const unique_ptr<T, D>& y);                // freestanding
  template<class T, class D>
    requires three_way_comparable<typename unique_ptr<T, D>::pointer>
    constexpr compare_three_way_result_t<typename unique_ptr<T, D>::pointer>
      operator<=>(const unique_ptr<T, D>& x, nullptr_t);                            // freestanding

  template<class E, class T, class Y, class D>
    basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const unique_ptr<Y, D>& p);

  // [util.smartptr.weak.bad], class bad_weak_ptr
  class bad_weak_ptr;

  // [util.smartptr.shared], class template shared_ptr
  template<class T> class shared_ptr;

  // [util.smartptr.shared.create], shared_ptr creation
  template<class T, class... Args>
    shared_ptr<T> make_shared(Args&&... args);                                  // T is not array
  template<class T, class A, class... Args>
    shared_ptr<T> allocate_shared(const A& a, Args&&... args);                  // T is not array

  template<class T>
    shared_ptr<T> make_shared(size_t N);                                        // T is U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a, size_t N);                        // T is U[]

  template<class T>
    shared_ptr<T> make_shared();                                                // T is U[N]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a);                                  // T is U[N]

  template<class T>
    shared_ptr<T> make_shared(size_t N, const remove_extent_t<T>& u);           // T is U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a, size_t N,
                                  const remove_extent_t<T>& u);                 // T is U[]

  template<class T>
    shared_ptr<T> make_shared(const remove_extent_t<T>& u);                     // T is U[N]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a, const remove_extent_t<T>& u);     // T is U[N]

  template<class T>
    shared_ptr<T> make_shared_for_overwrite();                                  // T is not U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared_for_overwrite(const A& a);                    // T is not U[]

  template<class T>
    shared_ptr<T> make_shared_for_overwrite(size_t N);                          // T is U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared_for_overwrite(const A& a, size_t N);          // T is U[]

  // [util.smartptr.shared.cmp], shared_ptr comparisons
  template<class T, class U>
    bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    strong_ordering operator<=>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;

  template<class T>
    bool operator==(const shared_ptr<T>& x, nullptr_t) noexcept;
  template<class T>
    strong_ordering operator<=>(const shared_ptr<T>& x, nullptr_t) noexcept;

  // [util.smartptr.shared.spec], shared_ptr specialized algorithms
  template<class T>
    void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.cast], shared_ptr casts
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(shared_ptr<U>&& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(shared_ptr<U>&& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(shared_ptr<U>&& r) noexcept;
  template<class T, class U>
    shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> reinterpret_pointer_cast(shared_ptr<U>&& r) noexcept;

  // [util.smartptr.getdeleter], shared_ptr get_deleter
  template<class D, class T>
    D* get_deleter(const shared_ptr<T>& p) noexcept;

  // [util.smartptr.shared.io], shared_ptr I/O
  template<class E, class T, class Y>
    basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const shared_ptr<Y>& p);

  // [util.smartptr.weak], class template weak_ptr
  template<class T> class weak_ptr;

  // [util.smartptr.weak.spec], weak_ptr specialized algorithms
  template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;

  // [util.smartptr.ownerless], class template owner_less
  template<class T = void> struct owner_less;

  // [util.smartptr.enab], class template enable_shared_from_this
  template<class T> class enable_shared_from_this;

  // [util.smartptr.hash], hash support
  template<class T> struct hash;                                                    // freestanding
  template<class T, class D> struct hash<unique_ptr<T, D>>;                         // freestanding
  template<class T> struct hash<shared_ptr<T>>;

  // [util.smartptr.atomic], atomic smart pointers
  template<class T> struct atomic;                                                  // freestanding
  template<class T> struct atomic<shared_ptr<T>>;
  template<class T> struct atomic<weak_ptr<T>>;

  // [out.ptr.t], class template out_ptr_t
  template<class Smart, class Pointer, class... Args>
    class out_ptr_t;

  // [out.ptr], function template out_ptr
  template<class Pointer = void, class Smart, class... Args>
    auto out_ptr(Smart& s, Args&&... args);

  // [inout.ptr.t], class template inout_ptr_t
  template<class Smart, class Pointer, class... Args>
    class inout_ptr_t;

  // [inout.ptr], function template inout_ptr
  template<class Pointer = void, class Smart, class... Args>
    auto inout_ptr(Smart& s, Args&&... args);
}
```

### Pointer traits <a id="pointer.traits">[[pointer.traits]]</a>

#### General <a id="pointer.traits.general">[[pointer.traits.general]]</a>

The class template `pointer_traits` supplies a uniform interface to
certain attributes of pointer-like types.

``` cpp
namespace std {
  template<class Ptr> struct pointer_traits {
    see below;
  };

  template<class T> struct pointer_traits<T*> {
    using pointer         = T*;
    using element_type    = T;
    using difference_type = ptrdiff_t;

    template<class U> using rebind = U*;

    static constexpr pointer pointer_to(see below r) noexcept;
  };
}
```

#### Member types <a id="pointer.traits.types">[[pointer.traits.types]]</a>

The definitions in this subclause make use of the following
exposition-only class template and concept:

``` cpp
template<class T>
struct ptr-traits-elem          // exposition only
{ };

template<class T> requires requires { typename T::element_type; }
struct ptr-traits-elem<T>
{ using type = typename T::element_type; };

template<template<class...> class SomePointer, class T, class... Args>
  requires (!requires { typename SomePointer<T, Args...>::element_type; })
struct ptr-traits-elem<SomePointer<T, Args...>>
{ using type = T; };

template<class Ptr>
  concept has-elem-type =       // exposition only
    requires { typename ptr-traits-elem<Ptr>::type; }
```

If `Ptr` satisfies `has-elem-type`, a specialization
`pointer_traits<Ptr>` generated from the `pointer_traits` primary
template has the following members as well as those described in 
[[pointer.traits.functions]]; otherwise, such a specialization has no
members by any of those names.

``` cpp
using pointer = see below;
```

*Type:* `Ptr`.

``` cpp
using element_type = see below;
```

*Type:* `typename `*`ptr-traits-elem`*`<Ptr>::type`.

``` cpp
using difference_type = see below;
```

*Type:* `Ptr::difference_type` if the *qualified-id*
`Ptr::difference_type` is valid and denotes a type [[temp.deduct]];
otherwise, `ptrdiff_t`.

``` cpp
template<class U> using rebind = see below;
```

*Alias template:* `Ptr::rebind<U>` if the *qualified-id*
`Ptr::rebind<U>` is valid and denotes a type [[temp.deduct]]; otherwise,
`SomePointer<U, Args>` if `Ptr` is a class template instantiation of the
form `SomePointer<T, Args>`, where `Args` is zero or more type
arguments; otherwise, the instantiation of `rebind` is ill-formed.

#### Member functions <a id="pointer.traits.functions">[[pointer.traits.functions]]</a>

``` cpp
static pointer pointer_traits::pointer_to(see below r);
static constexpr pointer pointer_traits<T*>::pointer_to(see below r) noexcept;
```

*Mandates:* For the first member function, `Ptr::pointer_to(r)` is
well-formed.

*Preconditions:* For the first member function, `Ptr::pointer_to(r)`
returns a pointer to `r` through which indirection is valid.

*Returns:* The first member function returns `Ptr::pointer_to(r)`. The
second member function returns `addressof(r)`.

*Remarks:* If `element_type` is  , the type of `r` is unspecified;
otherwise, it is `element_type&`.

#### Optional members <a id="pointer.traits.optmem">[[pointer.traits.optmem]]</a>

Specializations of `pointer_traits` may define the member declared in
this subclause to customize the behavior of the standard library. A
specialization generated from the `pointer_traits` primary template has
no member by this name.

``` cpp
static element_type* to_address(pointer p) noexcept;
```

*Returns:* A pointer of type `element_type*` that references the same
location as the argument `p`.

\[*Note 1*: This function is intended to be the inverse of `pointer_to`.
If defined, it customizes the behavior of the non-member function
`to_address`[[pointer.conversion]]. — *end note*\]

### Pointer conversion <a id="pointer.conversion">[[pointer.conversion]]</a>

``` cpp
template<class T> constexpr T* to_address(T* p) noexcept;
```

*Mandates:* `T` is not a function type.

*Returns:* `p`.

``` cpp
template<class Ptr> constexpr auto to_address(const Ptr& p) noexcept;
```

*Returns:* `pointer_traits<Ptr>::to_address(p)` if that expression is
well-formed (see [[pointer.traits.optmem]]), otherwise
`to_address(p.operator->())`.

### Pointer alignment <a id="ptr.align">[[ptr.align]]</a>

``` cpp
void* align(size_t alignment, size_t size, void*& ptr, size_t& space);
```

*Preconditions:*

- `alignment` is a power of two
- `ptr` represents the address of contiguous storage of at least `space`
  bytes

*Effects:* If it is possible to fit `size` bytes of storage aligned by
`alignment` into the buffer pointed to by `ptr` with length `space`, the
function updates `ptr` to represent the first possible address of such
storage and decreases `space` by the number of bytes used for alignment.
Otherwise, the function does nothing.

*Returns:* A null pointer if the requested aligned buffer would not fit
into the available space, otherwise the adjusted value of `ptr`.

\[*Note 1*: The function updates its `ptr` and `space` arguments so that
it can be called repeatedly with possibly different `alignment` and
`size` arguments for the same buffer. — *end note*\]

``` cpp
template<size_t N, class T>
  [[nodiscard]] constexpr T* assume_aligned(T* ptr);
```

*Mandates:* `N` is a power of two.

*Preconditions:* `ptr` points to an object `X` of a type
similar [[conv.qual]] to `T`, where `X` has alignment
`N`[[basic.align]].

*Returns:* `ptr`.

*Throws:* Nothing.

\[*Note 2*: The alignment assumption on an object `X` expressed by a
call to `assume_aligned` might result in generation of more efficient
code. It is up to the program to ensure that the assumption actually
holds. The call does not cause the implementation to verify or enforce
this. An implementation might only make the assumption for those
operations on `X` that access `X` through the pointer returned by
`assume_aligned`. — *end note*\]

### Explicit lifetime management <a id="obj.lifetime">[[obj.lifetime]]</a>

``` cpp
template<class T>
  T* start_lifetime_as(void* p) noexcept;
template<class T>
  const T* start_lifetime_as(const void* p) noexcept;
template<class T>
  volatile T* start_lifetime_as(volatile void* p) noexcept;
template<class T>
  const volatile T* start_lifetime_as(const volatile void* p) noexcept;
```

*Mandates:* `T` is an implicit-lifetime type [[basic.types.general]] and
not an incomplete type [[term.incomplete.type]].

*Preconditions:* \[`p`, `(char*)p + sizeof(T)`) denotes a region of
allocated storage that is a subset of the region of storage reachable
through [[basic.compound]] `p` and suitably aligned for the type `T`.

*Effects:* Implicitly creates objects [[intro.object]] within the
denoted region consisting of an object *a* of type `T` whose address is
`p`, and objects nested within *a*, as follows: The object
representation of *a* is the contents of the storage prior to the call
to `start_lifetime_as`. The value of each created object *o* of
trivially-copyable type `U` is determined in the same manner as for a
call to `bit_cast<U>(E)`[[bit.cast]], where `E` is an lvalue of type `U`
denoting *o*, except that the storage is not accessed. The value of any
other created object is unspecified.

\[*Note 1*: The unspecified value can be indeterminate. — *end note*\]

*Returns:* A pointer to the *a* defined in the paragraph.

``` cpp
template<class T>
  T* start_lifetime_as_array(void* p, size_t n) noexcept;
template<class T>
  const T* start_lifetime_as_array(const void* p, size_t n) noexcept;
template<class T>
  volatile T* start_lifetime_as_array(volatile void* p, size_t n) noexcept;
template<class T>
  const volatile T* start_lifetime_as_array(const volatile void* p, size_t n) noexcept;
```

*Mandates:* `T` is a complete type.

*Preconditions:* `p` is suitably aligned for an array of `T` or is null.
`n <= size_t(-1) / sizeof(T)` is `true`. If `n > 0` is `true`,
\[`(char*)p`, `(char*)p + (n * sizeof(T))`) denotes a region of
allocated storage that is a subset of the region of storage reachable
through [[basic.compound]] `p`.

*Effects:* If `n > 0` is `true`, equivalent to `start_lifetime_as<U>(p)`
where `U` is the type “array of `n` `T`”. Otherwise, there are no
effects.

*Returns:* A pointer to the first element of the created array, if any;
otherwise, a pointer that compares equal to `p`[[expr.eq]].

### Allocator argument tag <a id="allocator.tag">[[allocator.tag]]</a>

``` cpp
namespace std {
  struct allocator_arg_t { explicit allocator_arg_t() = default; };
  inline constexpr allocator_arg_t allocator_arg{};
}
```

The `allocator_arg_t` struct is an empty class type used as a unique
type to disambiguate constructor and function overloading. Specifically,
several types (see `tuple`  [[tuple]]) have constructors with
`allocator_arg_t` as the first argument, immediately followed by an
argument of a type that meets the *Cpp17Allocator* requirements
[[allocator.requirements.general]].

### `uses_allocator` <a id="allocator.uses">[[allocator.uses]]</a>

#### `uses_allocator` trait <a id="allocator.uses.trait">[[allocator.uses.trait]]</a>

``` cpp
template<class T, class Alloc> struct uses_allocator;
```

*Remarks:* Automatically detects whether `T` has a nested
`allocator_type` that is convertible from `Alloc`. Meets the
*Cpp17BinaryTypeTrait* requirements [[meta.rqmts]]. The implementation
shall provide a definition that is derived from `true_type` if the
*qualified-id* `T::allocator_type` is valid and denotes a
type [[temp.deduct]] and
`is_convertible_v<Alloc, T::allocator_type> != false`, otherwise it
shall be derived from `false_type`. A program may specialize this
template to derive from `true_type` for a program-defined type `T` that
does not have a nested `allocator_type` but nonetheless can be
constructed with an allocator where either:

- the first argument of a constructor has type `allocator_arg_t` and the
  second argument has type `Alloc` or
- the last argument of a constructor has type `Alloc`.

#### Uses-allocator construction <a id="allocator.uses.construction">[[allocator.uses.construction]]</a>

*Uses-allocator construction*

with allocator `alloc` and constructor arguments `args...` refers to the
construction of an object of type `T` such that `alloc` is passed to the
constructor of `T` if `T` uses an allocator type compatible with
`alloc`. When applied to the construction of an object of type `T`, it
is equivalent to initializing it with the value of the expression
`make_obj_using_allocator<T>(alloc, args...)`, described below.

The following utility functions support three conventions for passing
`alloc` to a constructor:

- If `T` does not use an allocator compatible with `alloc`, then `alloc`
  is ignored.
- Otherwise, if `T` has a constructor invocable as
  `T(allocator_arg, alloc, args...)` (leading-allocator convention),
  then uses-allocator construction chooses this constructor form.
- Otherwise, if `T` has a constructor invocable as `T(args..., alloc)`
  (trailing-allocator convention), then uses-allocator construction
  chooses this constructor form.

The `uses_allocator_construction_args` function template takes an
allocator and argument list and produces (as a tuple) a new argument
list matching one of the above conventions. Additionally, overloads are
provided that treat specializations of `pair` such that uses-allocator
construction is applied individually to the `first` and `second` data
members. The `make_obj_using_allocator` and
`uninitialized_construct_using_allocator` function templates apply the
modified constructor arguments to construct an object of type `T` as a
return value or in-place, respectively.

\[*Note 1*: For `uses_allocator_construction_args` and
`make_obj_using_allocator`, type `T` is not deduced and must therefore
be specified explicitly by the caller. — *end note*\]

``` cpp
template<class T, class Alloc, class... Args>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  Args&&... args) noexcept;
```

*Constraints:* `remove_cv_t<T>` is not a specialization of `pair`.

*Returns:* A `tuple` value determined as follows:

- If `uses_allocator_v<remove_cv_t<T>, Alloc>` is `false` and
  `is_constructible_v<T,Args...>` is `true`, return
  `forward_as_tuple(std::forward<Args>(args)...)`.
- Otherwise, if `uses_allocator_v<remove_cv_t<T>, Alloc>` is `true` and
  `is_constructible_v<T, allocator_arg_t, const Alloc&, Args...>` is
  `true`, return
      tuple<allocator_arg_t, const Alloc&, Args&&...>(
        allocator_arg, alloc, std::forward<Args>(args)...)
- Otherwise, if `uses_allocator_v<remove_cv_t<T>, Alloc>` is `true` and
  `is_constructible_v<T, Args..., const Alloc&>` is `true`, return
  `forward_as_tuple(std::forward<Args>(args)..., alloc)`.
- Otherwise, the program is ill-formed.

\[*Note 2*: This definition prevents a silent failure to pass the
allocator to a constructor of a type for which
`uses_allocator_v<T, Alloc>` is `true`. — *end note*\]

``` cpp
template<class T, class Alloc, class Tuple1, class Tuple2>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc, piecewise_construct_t,
                                                  Tuple1&& x, Tuple2&& y) noexcept;
```

Let `T1` be `T::first_type`. Let `T2` be `T::second_type`.

*Constraints:* `remove_cv_t<T>` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return make_tuple(
  piecewise_construct,
  apply([&alloc](auto&&... args1) {
          return uses_allocator_construction_args<T1>(
            alloc, std::forward<decltype(args1)>(args1)...);
        }, std::forward<Tuple1>(x)),
  apply([&alloc](auto&&... args2) {
          return uses_allocator_construction_args<T2>(
            alloc, std::forward<decltype(args2)>(args2)...);
        }, std::forward<Tuple2>(y)));
```

``` cpp
template<class T, class Alloc>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc) noexcept;
```

*Constraints:* `remove_cv_t<T>` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           tuple<>{}, tuple<>{});
```

``` cpp
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  U&& u, V&& v) noexcept;
```

*Constraints:* `remove_cv_t<T>` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(std::forward<U>(u)),
                                           forward_as_tuple(std::forward<V>(v)));
```

``` cpp
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  pair<U, V>& pr) noexcept;
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  const pair<U, V>& pr) noexcept;
```

*Constraints:* `remove_cv_t<T>` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(pr.first),
                                           forward_as_tuple(pr.second));
```

``` cpp
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  pair<U, V>&& pr) noexcept;
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  const pair<U, V>&& pr) noexcept;
```

*Constraints:* `remove_cv_t<T>` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(get<0>(std::move(pr))),
                                           forward_as_tuple(get<1>(std::move(pr))));
```

``` cpp
template<class T, class Alloc, pair-like P>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc, P&& p) noexcept;
```

*Constraints:* `remove_cv_t<T>` is a specialization of `pair` and
`remove_cvref_t<P>` is not a specialization of `ranges::subrange`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(get<0>(std::forward<P>(p))),
                                           forward_as_tuple(get<1>(std::forward<P>(p))));
```

``` cpp
template<class T, class Alloc, class U>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc, U&& u) noexcept;
```

Let *FUN* be the function template:

``` cpp
template<class A, class B>
  void FUN(const pair<A, B>&);
```

*Constraints:* `remove_cv_t<T>` is a specialization of `pair`, and
either:

- `remove_cvref_t<U>` is a specialization of `ranges::subrange`, or
- `U` does not satisfy `pair-like` and the expression *`FUN`*`(u)` is
  not well-formed when considered as an unevaluated operand.

Let *pair-constructor* be an exposition-only class defined as follows:

``` cpp
class pair-constructor {
  using pair-type = remove_cv_t<T>;                             // exposition only

  constexpr auto do-construct(const pair-type& p) const {       // exposition only
    return make_obj_using_allocator<pair-type>(alloc_, p);
  }
  constexpr auto do-construct(pair-type&& p) const {            // exposition only
    return make_obj_using_allocator<pair-type>(alloc_, std::move(p));
  }

  const Alloc& alloc_;  // exposition only
  U& u_;                // exposition only

public:
  constexpr operator pair-type() const {
    return do-construct(std::forward<U>(u_));
  }
};
```

*Returns:* `make_tuple(pc)`, where `pc` is a *pair-constructor* object
whose *alloc\_* member is initialized with `alloc` and whose *u\_*
member is initialized with `u`.

``` cpp
template<class T, class Alloc, class... Args>
  constexpr T make_obj_using_allocator(const Alloc& alloc, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return make_from_tuple<T>(uses_allocator_construction_args<T>(
                            alloc, std::forward<Args>(args)...));
```

``` cpp
template<class T, class Alloc, class... Args>
  constexpr T* uninitialized_construct_using_allocator(T* p, const Alloc& alloc, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return apply([&]<class... U>(U&&... xs) {
       return construct_at(p, std::forward<U>(xs)...);
     }, uses_allocator_construction_args<T>(alloc, std::forward<Args>(args)...));
```

### Allocator traits <a id="allocator.traits">[[allocator.traits]]</a>

#### General <a id="allocator.traits.general">[[allocator.traits.general]]</a>

The class template `allocator_traits` supplies a uniform interface to
all allocator types. An allocator cannot be a non-class type, however,
even if `allocator_traits` supplies the entire required interface.

\[*Note 1*: Thus, it is always possible to create a derived class from
an allocator. — *end note*\]

If a program declares an explicit or partial specialization of
`allocator_traits`, the program is ill-formed, no diagnostic required.

``` cpp
namespace std {
  template<class Alloc> struct allocator_traits {
    using allocator_type     = Alloc;

    using value_type         = typename Alloc::value_type;

    using pointer            = see below;
    using const_pointer      = see below;
    using void_pointer       = see below;
    using const_void_pointer = see below;

    using difference_type    = see below;
    using size_type          = see below;

    using propagate_on_container_copy_assignment = see below;
    using propagate_on_container_move_assignment = see below;
    using propagate_on_container_swap            = see below;
    using is_always_equal                        = see below;

    template<class T> using rebind_alloc = see below;
    template<class T> using rebind_traits = allocator_traits<rebind_alloc<T>>;

    [[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n);
    [[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n,
                                                    const_void_pointer hint);
    [[nodiscard]] static constexpr allocation_result<pointer, size_type>
      allocate_at_least(Alloc& a, size_type n);

    static constexpr void deallocate(Alloc& a, pointer p, size_type n);

    template<class T, class... Args>
      static constexpr void construct(Alloc& a, T* p, Args&&... args);

    template<class T>
      static constexpr void destroy(Alloc& a, T* p);

    static constexpr size_type max_size(const Alloc& a) noexcept;

    static constexpr Alloc select_on_container_copy_construction(const Alloc& rhs);
  };
}
```

#### Member types <a id="allocator.traits.types">[[allocator.traits.types]]</a>

``` cpp
using pointer = see below;
```

*Type:* `Alloc::pointer` if the *qualified-id* `Alloc::pointer` is valid
and denotes a type [[temp.deduct]]; otherwise, `value_type*`.

``` cpp
using const_pointer = see below;
```

*Type:* `Alloc::const_pointer` if the *qualified-id*
`Alloc::const_pointer` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::rebind<const value_type>`.

``` cpp
using void_pointer = see below;
```

*Type:* `Alloc::void_pointer` if the *qualified-id*
`Alloc::void_pointer` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::rebind<void>`.

``` cpp
using const_void_pointer = see below;
```

*Type:* `Alloc::const_void_pointer` if the *qualified-id*
`Alloc::const_void_pointer` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::rebind<const void>`.

``` cpp
using difference_type = see below;
```

*Type:* `Alloc::difference_type` if the *qualified-id*
`Alloc::difference_type` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::difference_type`.

``` cpp
using size_type = see below;
```

*Type:* `Alloc::size_type` if the *qualified-id* `Alloc::size_type` is
valid and denotes a type [[temp.deduct]]; otherwise,
`make_unsigned_t<difference_type>`.

``` cpp
using propagate_on_container_copy_assignment = see below;
```

*Type:* `Alloc::propagate_on_container_copy_assignment` if the
*qualified-id* `Alloc::propagate_on_container_copy_assignment` is valid
and denotes a type [[temp.deduct]]; otherwise `false_type`.

``` cpp
using propagate_on_container_move_assignment = see below;
```

*Type:* `Alloc::propagate_on_container_move_assignment` if the
*qualified-id* `Alloc::propagate_on_container_move_assignment` is valid
and denotes a type [[temp.deduct]]; otherwise `false_type`.

``` cpp
using propagate_on_container_swap = see below;
```

*Type:* `Alloc::propagate_on_container_swap` if the *qualified-id*
`Alloc::propagate_on_container_swap` is valid and denotes a
type [[temp.deduct]]; otherwise `false_type`.

``` cpp
using is_always_equal = see below;
```

*Type:* `Alloc::is_always_equal` if the *qualified-id*
`Alloc::is_always_equal` is valid and denotes a type [[temp.deduct]];
otherwise `is_empty<Alloc>::type`.

``` cpp
template<class T> using rebind_alloc = see below;
```

*Alias template:* `Alloc::rebind<T>::other` if the *qualified-id*
`Alloc::rebind<T>::other` is valid and denotes a type [[temp.deduct]];
otherwise, `Alloc<T, Args>` if `Alloc` is a class template instantiation
of the form `Alloc<U, Args>`, where `Args` is zero or more type
arguments; otherwise, the instantiation of `rebind_alloc` is ill-formed.

#### Static member functions <a id="allocator.traits.members">[[allocator.traits.members]]</a>

``` cpp
[[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n);
```

*Returns:* `a.allocate(n)`.

``` cpp
[[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n, const_void_pointer hint);
```

*Returns:* `a.allocate(n, hint)` if that expression is well-formed;
otherwise, `a.allocate(n)`.

``` cpp
[[nodiscard]] static constexpr allocation_result<pointer, size_type>
  allocate_at_least(Alloc& a, size_type n);
```

*Returns:* `a.allocate_at_least(n)` if that expression is well-formed;
otherwise, `{a.allocate(n), n}`.

``` cpp
static constexpr void deallocate(Alloc& a, pointer p, size_type n);
```

*Effects:* Calls `a.deallocate(p, n)`.

*Throws:* Nothing.

``` cpp
template<class T, class... Args>
  static constexpr void construct(Alloc& a, T* p, Args&&... args);
```

*Effects:* Calls `a.construct(p, std::forward<Args>(args)...)` if that
call is well-formed; otherwise, invokes
`construct_at(p, std::forward<Args>(args)...)`.

``` cpp
template<class T>
  static constexpr void destroy(Alloc& a, T* p);
```

*Effects:* Calls `a.destroy(p)` if that call is well-formed; otherwise,
invokes `destroy_at(p)`.

``` cpp
static constexpr size_type max_size(const Alloc& a) noexcept;
```

*Returns:* `a.max_size()` if that expression is well-formed; otherwise,
`numeric_limits<size_type>::max()/sizeof(value_type)`.

``` cpp
static constexpr Alloc select_on_container_copy_construction(const Alloc& rhs);
```

*Returns:* `rhs.select_on_container_copy_construction()` if that
expression is well-formed; otherwise, `rhs`.

#### Other <a id="allocator.traits.other">[[allocator.traits.other]]</a>

The class template `allocation_result` has the template parameters, data
members, and special members specified above. It has no base classes or
members other than those specified.

### The default allocator <a id="default.allocator">[[default.allocator]]</a>

#### General <a id="default.allocator.general">[[default.allocator.general]]</a>

All specializations of the default allocator meet the allocator
completeness requirements [[allocator.requirements.completeness]].

``` cpp
namespace std {
  template<class T> class allocator {
   public:
    using value_type                             = T;
    using size_type                              = size_t;
    using difference_type                        = ptrdiff_t;
    using propagate_on_container_move_assignment = true_type;

    constexpr allocator() noexcept;
    constexpr allocator(const allocator&) noexcept;
    template<class U> constexpr allocator(const allocator<U>&) noexcept;
    constexpr ~allocator();
    constexpr allocator& operator=(const allocator&) = default;

    [[nodiscard]] constexpr T* allocate(size_t n);
    [[nodiscard]] constexpr allocation_result<T*> allocate_at_least(size_t n);
    constexpr void deallocate(T* p, size_t n);
  };
}
```

`allocator_traits<allocator<T>>::is_always_equal::value`

is `true` for any `T`.

#### Members <a id="allocator.members">[[allocator.members]]</a>

Except for the destructor, member functions of the default allocator
shall not introduce data races [[intro.multithread]] as a result of
concurrent calls to those member functions from different threads. Calls
to these functions that allocate or deallocate a particular unit of
storage shall occur in a single total order, and each such deallocation
call shall happen before the next allocation (if any) in this order.

``` cpp
[[nodiscard]] constexpr T* allocate(size_t n);
```

*Mandates:* `T` is not an incomplete type [[term.incomplete.type]].

*Returns:* A pointer to the initial element of an array of `n` `T`.

*Throws:* `bad_array_new_length` if
`numeric_limits<size_t>::max() / sizeof(T) < n`, or `bad_alloc` if the
storage cannot be obtained.

*Remarks:* The storage for the array is obtained by calling
`::operator new`[[new.delete]], but it is unspecified when or how often
this function is called. This function starts the lifetime of the array
object, but not that of any of the array elements.

``` cpp
[[nodiscard]] constexpr allocation_result<T*> allocate_at_least(size_t n);
```

*Mandates:* `T` is not an incomplete type [[term.incomplete.type]].

*Returns:* `allocation_result<T*>{ptr, count}`, where `ptr` is a pointer
to the initial element of an array of `count` `T` and
$\texttt{count} \geq \texttt{n}$.

*Throws:* `bad_array_new_length` if
$\texttt{numeric_limits<size_t>::max() / sizeof(T)} < \texttt{n}$, or
`bad_alloc` if the storage cannot be obtained.

*Remarks:* The storage for the array is obtained by calling
`::operator new`, but it is unspecified when or how often this function
is called. This function starts the lifetime of the array object, but
not that of any of the array elements.

``` cpp
constexpr void deallocate(T* p, size_t n);
```

*Preconditions:*

- If `p` is memory that was obtained by a call to `allocate_at_least`,
  let `ret` be the value returned and `req` be the value passed as the
  first argument to that call. `p` is equal to `ret.ptr` and `n` is a
  value such that
  $\texttt{req} \leq \texttt{n} \leq \texttt{ret.count}$.
- Otherwise, `p` is a pointer value obtained from `allocate`. `n` equals
  the value passed as the first argument to the invocation of `allocate`
  which returned `p`.

*Effects:* Deallocates the storage referenced by `p`.

*Remarks:* Uses `::operator delete`[[new.delete]], but it is unspecified
when this function is called.

#### Operators <a id="allocator.globals">[[allocator.globals]]</a>

``` cpp
template<class T, class U>
  constexpr bool operator==(const allocator<T>&, const allocator<U>&) noexcept;
```

*Returns:* `true`.

### `addressof` <a id="specialized.addressof">[[specialized.addressof]]</a>

``` cpp
template<class T> constexpr T* addressof(T& r) noexcept;
```

*Returns:* The actual address of the object or function referenced by
`r`, even in the presence of an overloaded `operator&`.

*Remarks:* An expression `addressof(E)` is a constant
subexpression [[defns.const.subexpr]] if `E` is an lvalue constant
subexpression.

### C library memory allocation <a id="c.malloc">[[c.malloc]]</a>

\[*Note 1*: The header `<cstdlib>` declares the functions described in
this subclause. — *end note*\]

``` cpp
void* aligned_alloc(size_t alignment, size_t size);
void* calloc(size_t nmemb, size_t size);
void* malloc(size_t size);
void* realloc(void* ptr, size_t size);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* These functions do not attempt to allocate storage by calling
`::operator new()`[[new.delete]].

These functions implicitly create objects [[intro.object]] in the
returned region of storage and return a pointer to a suitable created
object. In the case of `calloc` and `realloc`, the objects are created
before the storage is zeroed or copied, respectively.

``` cpp
void free(void* ptr);
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* This function does not attempt to deallocate storage by
calling `::operator delete()`.

## Smart pointers <a id="smartptr">[[smartptr]]</a>

### Unique-ownership pointers <a id="unique.ptr">[[unique.ptr]]</a>

#### General <a id="unique.ptr.general">[[unique.ptr.general]]</a>

A *unique pointer* is an object that owns another object and manages
that other object through a pointer. More precisely, a unique pointer is
an object *u* that stores a pointer to a second object *p* and will
dispose of *p* when *u* is itself destroyed (e.g., when leaving block
scope [[stmt.dcl]]). In this context, *u* is said to *own* `p`.

The mechanism by which *u* disposes of *p* is known as *p*’s associated
*deleter*, a function object whose correct invocation results in *p*’s
appropriate disposition (typically its deletion).

Let the notation *u.p* denote the pointer stored by *u*, and let *u.d*
denote the associated deleter. Upon request, *u* can *reset* (replace)
*u.p* and *u.d* with another pointer and deleter, but properly disposes
of its owned object via the associated deleter before such replacement
is considered completed.

Each object of a type `U` instantiated from the `unique_ptr` template
specified in [[unique.ptr]] has the strict ownership semantics,
specified above, of a unique pointer. In partial satisfaction of these
semantics, each such `U` is *Cpp17MoveConstructible* and
*Cpp17MoveAssignable*, but is not *Cpp17CopyConstructible* nor
*Cpp17CopyAssignable*. The template parameter `T` of `unique_ptr` may be
an incomplete type.

\[*Note 1*: The uses of `unique_ptr` include providing exception safety
for dynamically allocated memory, passing ownership of dynamically
allocated memory to a function, and returning dynamically allocated
memory from a function. — *end note*\]

#### Default deleters <a id="unique.ptr.dltr">[[unique.ptr.dltr]]</a>

##### In general <a id="unique.ptr.dltr.general">[[unique.ptr.dltr.general]]</a>

The class template `default_delete` serves as the default deleter
(destruction policy) for the class template `unique_ptr`.

The template parameter `T` of `default_delete` may be an incomplete
type.

##### `default_delete` <a id="unique.ptr.dltr.dflt">[[unique.ptr.dltr.dflt]]</a>

``` cpp
namespace std {
  template<class T> struct default_delete {
    constexpr default_delete() noexcept = default;
    template<class U> constexpr default_delete(const default_delete<U>&) noexcept;
    constexpr void operator()(T*) const;
  };
}
```

``` cpp
template<class U> constexpr default_delete(const default_delete<U>& other) noexcept;
```

*Constraints:* `U*` is implicitly convertible to `T*`.

*Effects:* Constructs a `default_delete` object from another
`default_delete<U>` object.

``` cpp
constexpr void operator()(T* ptr) const;
```

*Mandates:* `T` is a complete type.

*Effects:* Calls on `ptr`.

##### `default_delete<T[]>` <a id="unique.ptr.dltr.dflt1">[[unique.ptr.dltr.dflt1]]</a>

``` cpp
namespace std {
  template<class T> struct default_delete<T[]> {
    constexpr default_delete() noexcept = default;
    template<class U> constexpr default_delete(const default_delete<U[]>&) noexcept;
    template<class U> constexpr void operator()(U* ptr) const;
  };
}
```

``` cpp
template<class U> constexpr default_delete(const default_delete<U[]>& other) noexcept;
```

*Constraints:* `U(*)[]` is convertible to `T(*)[]`.

*Effects:* Constructs a `default_delete` object from another
`default_delete<U[]>` object.

``` cpp
template<class U> constexpr void operator()(U* ptr) const;
```

*Constraints:* `U(*)[]` is convertible to `T(*)[]`.

*Mandates:* `U` is a complete type.

*Effects:* Calls `delete[]` on `ptr`.

#### `unique_ptr` for single objects <a id="unique.ptr.single">[[unique.ptr.single]]</a>

##### General <a id="unique.ptr.single.general">[[unique.ptr.single.general]]</a>

``` cpp
namespace std {
  template<class T, class D = default_delete<T>> class unique_ptr {
  public:
    using pointer      = see below;
    using element_type = T;
    using deleter_type = D;

    // [unique.ptr.single.ctor], constructors
    constexpr unique_ptr() noexcept;
    constexpr explicit unique_ptr(type_identity_t<pointer> p) noexcept;
    constexpr unique_ptr(type_identity_t<pointer> p, see below d1) noexcept;
    constexpr unique_ptr(type_identity_t<pointer> p, see below d2) noexcept;
    constexpr unique_ptr(unique_ptr&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept;
    template<class U, class E>
      constexpr unique_ptr(unique_ptr<U, E>&& u) noexcept;

    // [unique.ptr.single.dtor], destructor
    constexpr ~unique_ptr();

    // [unique.ptr.single.asgn], assignment
    constexpr unique_ptr& operator=(unique_ptr&& u) noexcept;
    template<class U, class E>
      constexpr unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
    constexpr unique_ptr& operator=(nullptr_t) noexcept;

    // [unique.ptr.single.observers], observers
    constexpr add_lvalue_reference_t<T> operator*() const noexcept(see below);
    constexpr pointer operator->() const noexcept;
    constexpr pointer get() const noexcept;
    constexpr deleter_type& get_deleter() noexcept;
    constexpr const deleter_type& get_deleter() const noexcept;
    constexpr explicit operator bool() const noexcept;

    // [unique.ptr.single.modifiers], modifiers
    constexpr pointer release() noexcept;
    constexpr void reset(pointer p = pointer()) noexcept;
    constexpr void swap(unique_ptr& u) noexcept;

    // disable copy from lvalue
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
  };
}
```

The default type for the template parameter `D` is `default_delete`. A
client-supplied template argument `D` shall be a function object type
[[function.objects]], lvalue reference to function, or lvalue reference
to function object type for which, given a value `d` of type `D` and a
value `ptr` of type `unique_ptr<T, D>::pointer`, the expression `d(ptr)`
is valid and has the effect of disposing of the pointer as appropriate
for that deleter.

If the deleter’s type `D` is not a reference type, `D` shall meet the
*Cpp17Destructible* requirements ( [[cpp17.destructible]]).

If the *qualified-id* `remove_reference_t<D>::pointer` is valid and
denotes a type [[temp.deduct]], then `unique_ptr<T,
D>::pointer` shall be a synonym for `remove_reference_t<D>::pointer`.
Otherwise `unique_ptr<T, D>::pointer` shall be a synonym for
`element_type*`. The type `unique_ptr<T,
D>::pointer` shall meet the *Cpp17NullablePointer* requirements (
[[cpp17.nullablepointer]]).

\[*Example 1*: Given an allocator type `X`
[[allocator.requirements.general]] and letting `A` be a synonym for
`allocator_traits<X>`, the types `A::pointer`, `A::const_pointer`,
`A::void_pointer`, and `A::const_void_pointer` may be used as
`unique_ptr<T, D>::pointer`. — *end example*\]

##### Constructors <a id="unique.ptr.single.ctor">[[unique.ptr.single.ctor]]</a>

``` cpp
constexpr unique_ptr() noexcept;
constexpr unique_ptr(nullptr_t) noexcept;
```

*Constraints:* `is_pointer_v<deleter_type>` is `false` and
`is_default_constructible_v<deleter_type>` is `true`.

*Preconditions:* `D` meets the *Cpp17DefaultConstructible* requirements
( [[cpp17.defaultconstructible]]), and that construction does not throw
an exception.

*Effects:* Constructs a `unique_ptr` object that owns nothing,
value-initializing the stored pointer and the stored deleter.

*Ensures:* `get() == nullptr`. `get_deleter()` returns a reference to
the stored deleter.

``` cpp
constexpr explicit unique_ptr(type_identity_t<pointer> p) noexcept;
```

*Constraints:* `is_pointer_v<deleter_type>` is `false` and
`is_default_constructible_v<deleter_type>` is `true`.

*Preconditions:* `D` meets the *Cpp17DefaultConstructible* requirements
( [[cpp17.defaultconstructible]]), and that construction does not throw
an exception.

*Effects:* Constructs a `unique_ptr` which owns `p`, initializing the
stored pointer with `p` and value-initializing the stored deleter.

*Ensures:* `get() == p`. `get_deleter()` returns a reference to the
stored deleter.

``` cpp
constexpr unique_ptr(type_identity_t<pointer> p, const D& d) noexcept;
constexpr unique_ptr(type_identity_t<pointer> p, remove_reference_t<D>&& d) noexcept;
```

*Constraints:* `is_constructible_v<D, decltype(d)>` is `true`.

*Preconditions:* For the first constructor, if `D` is not a reference
type, `D` meets the *Cpp17CopyConstructible* requirements and such
construction does not exit via an exception. For the second constructor,
if `D` is not a reference type, `D` meets the *Cpp17MoveConstructible*
requirements and such construction does not exit via an exception.

*Effects:* Constructs a `unique_ptr` object which owns `p`, initializing
the stored pointer with `p` and initializing the deleter from
`std::forward<decltype(d)>(d)`.

*Ensures:* `get() == p`. `get_deleter()` returns a reference to the
stored deleter. If `D` is a reference type then `get_deleter()` returns
a reference to the lvalue `d`.

*Remarks:* If `D` is a reference type, the second constructor is defined
as deleted.

\[*Example 2*:

    D d;
    unique_ptr<int, D> p1(new int, D());        // \texttt{D} must be \textit{Cpp17MoveConstructible}
    unique_ptr<int, D> p2(new int, d);          // \texttt{D} must be \textit{Cpp17CopyConstructible}
    unique_ptr<int, D&> p3(new int, d);         // \texttt{p3} holds a reference to \texttt{d}
    unique_ptr<int, const D&> p4(new int, D()); // error: rvalue deleter object combined
                                                // with reference deleter type

— *end example*\]

``` cpp
constexpr unique_ptr(unique_ptr&& u) noexcept;
```

*Constraints:* `is_move_constructible_v<D>` is `true`.

*Preconditions:* If `D` is not a reference type, `D` meets the
*Cpp17MoveConstructible* requirements ( [[cpp17.moveconstructible]]).
Construction of the deleter from an rvalue of type `D` does not throw an
exception.

*Effects:* Constructs a `unique_ptr` from `u`. If `D` is a reference
type, this deleter is copy constructed from `u`’s deleter; otherwise,
this deleter is move constructed from `u`’s deleter.

\[*Note 1*: The construction of the deleter can be implemented with
`std::forward<D>`. — *end note*\]

*Ensures:* `get()` yields the value `u.get()` yielded before the
construction. `u.get() == nullptr`. `get_deleter()` returns a reference
to the stored deleter that was constructed from `u.get_deleter()`. If
`D` is a reference type then `get_deleter()` and `u.get_deleter()` both
reference the same lvalue deleter.

``` cpp
template<class U, class E> constexpr unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

*Constraints:*

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
- `U` is not an array type, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

*Preconditions:* If `E` is not a reference type, construction of the
deleter from an rvalue of type `E` is well-formed and does not throw an
exception. Otherwise, `E` is a reference type and construction of the
deleter from an lvalue of type `E` is well-formed and does not throw an
exception.

*Effects:* Constructs a `unique_ptr` from `u`. If `E` is a reference
type, this deleter is copy constructed from `u`’s deleter; otherwise,
this deleter is move constructed from `u`’s deleter.

\[*Note 2*: The deleter constructor can be implemented with
`std::forward<E>`. — *end note*\]

*Ensures:* `get()` yields the value `u.get()` yielded before the
construction. `u.get() == nullptr`. `get_deleter()` returns a reference
to the stored deleter that was constructed from `u.get_deleter()`.

##### Destructor <a id="unique.ptr.single.dtor">[[unique.ptr.single.dtor]]</a>

``` cpp
constexpr ~unique_ptr();
```

*Effects:* Equivalent to: `if (get()) get_deleter()(get());`

\[*Note 3*: The use of `default_delete` requires `T` to be a complete
type. — *end note*\]

*Remarks:* The behavior is undefined if the evaluation of
`get_deleter()(get())` throws an exception.

##### Assignment <a id="unique.ptr.single.asgn">[[unique.ptr.single.asgn]]</a>

``` cpp
constexpr unique_ptr& operator=(unique_ptr&& u) noexcept;
```

*Constraints:* `is_move_assignable_v<D>` is `true`.

*Preconditions:* If `D` is not a reference type, `D` meets the
*Cpp17MoveAssignable* requirements ( [[cpp17.moveassignable]]) and
assignment of the deleter from an rvalue of type `D` does not throw an
exception. Otherwise, `D` is a reference type; `remove_reference_t<D>`
meets the *Cpp17CopyAssignable* requirements and assignment of the
deleter from an lvalue of type `D` does not throw an exception.

*Effects:* Calls `reset(u.release())` followed by
`get_deleter() = std::forward<D>(u.get_deleter())`.

*Ensures:* If `this != addressof(u)`, `u.get() == nullptr`, otherwise
`u.get()` is unchanged.

*Returns:* `*this`.

``` cpp
template<class U, class E> constexpr unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
```

*Constraints:*

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
  and
- `U` is not an array type, and
- `is_assignable_v<D&, E&&>` is `true`.

*Preconditions:* If `E` is not a reference type, assignment of the
deleter from an rvalue of type `E` is well-formed and does not throw an
exception. Otherwise, `E` is a reference type and assignment of the
deleter from an lvalue of type `E` is well-formed and does not throw an
exception.

*Effects:* Calls `reset(u.release())` followed by
`get_deleter() = std::forward<E>(u.get_deleter())`.

*Ensures:* `u.get() == nullptr`.

*Returns:* `*this`.

``` cpp
constexpr unique_ptr& operator=(nullptr_t) noexcept;
```

*Effects:* As if by `reset()`.

*Ensures:* `get() == nullptr`.

*Returns:* `*this`.

##### Observers <a id="unique.ptr.single.observers">[[unique.ptr.single.observers]]</a>

``` cpp
constexpr add_lvalue_reference_t<T> operator*() const noexcept(noexcept(*declval<pointer>()));
```

*Preconditions:* `get() != nullptr`.

*Returns:* `*get()`.

``` cpp
constexpr pointer operator->() const noexcept;
```

*Preconditions:* `get() != nullptr`.

*Returns:* `get()`.

\[*Note 4*: The use of this function typically requires that `T` be a
complete type. — *end note*\]

``` cpp
constexpr pointer get() const noexcept;
```

*Returns:* The stored pointer.

``` cpp
constexpr deleter_type& get_deleter() noexcept;
constexpr const deleter_type& get_deleter() const noexcept;
```

*Returns:* A reference to the stored deleter.

``` cpp
constexpr explicit operator bool() const noexcept;
```

*Returns:* `get() != nullptr`.

##### Modifiers <a id="unique.ptr.single.modifiers">[[unique.ptr.single.modifiers]]</a>

``` cpp
constexpr pointer release() noexcept;
```

*Ensures:* `get() == nullptr`.

*Returns:* The value `get()` had at the start of the call to `release`.

``` cpp
constexpr void reset(pointer p = pointer()) noexcept;
```

*Effects:* Assigns `p` to the stored pointer, and then, with the old
value of the stored pointer, `old_p`, evaluates
`if (old_p) get_deleter()(old_p);`

\[*Note 5*: The order of these operations is significant because the
call to `get_deleter()` might destroy `*this`. — *end note*\]

*Ensures:* `get() == p`.

\[*Note 6*: The postcondition does not hold if the call to
`get_deleter()` destroys `*this` since `this->get()` is no longer a
valid expression. — *end note*\]

*Remarks:* The behavior is undefined if the evaluation of
`get_deleter()(old_p)` throws an exception.

``` cpp
constexpr void swap(unique_ptr& u) noexcept;
```

*Preconditions:* `get_deleter()` is swappable [[swappable.requirements]]
and does not throw an exception under `swap`.

*Effects:* Invokes `swap` on the stored pointers and on the stored
deleters of `*this` and `u`.

#### `unique_ptr` for array objects with a runtime length <a id="unique.ptr.runtime">[[unique.ptr.runtime]]</a>

##### General <a id="unique.ptr.runtime.general">[[unique.ptr.runtime.general]]</a>

``` cpp
namespace std {
  template<class T, class D> class unique_ptr<T[], D> {
  public:
    using pointer      = see below;
    using element_type = T;
    using deleter_type = D;

    // [unique.ptr.runtime.ctor], constructors
    constexpr unique_ptr() noexcept;
    template<class U> constexpr explicit unique_ptr(U p) noexcept;
    template<class U> constexpr unique_ptr(U p, see below d) noexcept;
    template<class U> constexpr unique_ptr(U p, see below d) noexcept;
    constexpr unique_ptr(unique_ptr&& u) noexcept;
    template<class U, class E>
      constexpr unique_ptr(unique_ptr<U, E>&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept;

    // destructor
    constexpr ~unique_ptr();

    // assignment
    constexpr unique_ptr& operator=(unique_ptr&& u) noexcept;
    template<class U, class E>
      constexpr unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
    constexpr unique_ptr& operator=(nullptr_t) noexcept;

    // [unique.ptr.runtime.observers], observers
    constexpr T& operator[](size_t i) const;
    constexpr pointer get() const noexcept;
    constexpr deleter_type& get_deleter() noexcept;
    constexpr const deleter_type& get_deleter() const noexcept;
    constexpr explicit operator bool() const noexcept;

    // [unique.ptr.runtime.modifiers], modifiers
    constexpr pointer release() noexcept;
    template<class U> constexpr void reset(U p) noexcept;
    constexpr void reset(nullptr_t = nullptr) noexcept;
    constexpr void swap(unique_ptr& u) noexcept;

    // disable copy from lvalue
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
  };
}
```

A specialization for array types is provided with a slightly altered
interface.

- Conversions between different types of `unique_ptr<T[], D>` that would
  be disallowed for the corresponding pointer-to-array types, and
  conversions to or from the non-array forms of `unique_ptr`, produce an
  ill-formed program.
- Pointers to types derived from `T` are rejected by the constructors,
  and by `reset`.
- The observers `operator*` and `operator->` are not provided.
- The indexing observer `operator[]` is provided.
- The default deleter will call `delete[]`.

Descriptions are provided below only for members that differ from the
primary template.

The template argument `T` shall be a complete type.

##### Constructors <a id="unique.ptr.runtime.ctor">[[unique.ptr.runtime.ctor]]</a>

``` cpp
template<class U> constexpr explicit unique_ptr(U p) noexcept;
```

This constructor behaves the same as the constructor in the primary
template that takes a single parameter of type `pointer`.

*Constraints:*

- `U` is the same type as `pointer`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

``` cpp
template<class U> constexpr unique_ptr(U p, see below d) noexcept;
template<class U> constexpr unique_ptr(U p, see below d) noexcept;
```

These constructors behave the same as the constructors in the primary
template that take a parameter of type `pointer` and a second parameter.

*Constraints:*

- `U` is the same type as `pointer`,
- `U` is `nullptr_t`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

``` cpp
template<class U, class E> constexpr unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

This constructor behaves the same as in the primary template.

*Constraints:* Where `UP` is `unique_ptr<U, E>`:

- `U` is an array type, and
- `pointer` is the same type as `element_type*`, and
- `UP::pointer` is the same type as `UP::element_type*`, and
- `UP::element_type(*)[]` is convertible to `element_type(*)[]`, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

\[*Note 1*: This replaces the *Constraints:* specification of the
primary template. — *end note*\]

##### Assignment <a id="unique.ptr.runtime.asgn">[[unique.ptr.runtime.asgn]]</a>

``` cpp
template<class U, class E> constexpr unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
```

This operator behaves the same as in the primary template.

*Constraints:* Where `UP` is `unique_ptr<U, E>`:

- `U` is an array type, and
- `pointer` is the same type as `element_type*`, and
- `UP::pointer` is the same type as `UP::element_type*`, and
- `UP::element_type(*)[]` is convertible to `element_type(*)[]`, and
- `is_assignable_v<D&, E&&>` is `true`.

\[*Note 2*: This replaces the *Constraints:* specification of the
primary template. — *end note*\]

##### Observers <a id="unique.ptr.runtime.observers">[[unique.ptr.runtime.observers]]</a>

``` cpp
constexpr T& operator[](size_t i) const;
```

*Preconditions:* $\texttt{i} <$ the number of elements in the array to
which the stored pointer points.

*Returns:* `get()[i]`.

##### Modifiers <a id="unique.ptr.runtime.modifiers">[[unique.ptr.runtime.modifiers]]</a>

``` cpp
constexpr void reset(nullptr_t p = nullptr) noexcept;
```

*Effects:* Equivalent to `reset(pointer())`.

``` cpp
constexpr template<class U> void reset(U p) noexcept;
```

This function behaves the same as the `reset` member of the primary
template.

*Constraints:*

- `U` is the same type as `pointer`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

#### Creation <a id="unique.ptr.create">[[unique.ptr.create]]</a>

``` cpp
template<class T, class... Args> constexpr unique_ptr<T> make_unique(Args&&... args);
```

*Constraints:* `T` is not an array type.

*Returns:* `unique_ptr<T>(new T(std::forward<Args>(args)...))`.

``` cpp
template<class T> constexpr unique_ptr<T> make_unique(size_t n);
```

*Constraints:* `T` is an array of unknown bound.

*Returns:* `unique_ptr<T>(new remove_extent_t<T>[n]())`.

``` cpp
template<class T, class... Args> unspecified make_unique(Args&&...) = delete;
```

*Constraints:* `T` is an array of known bound.

``` cpp
template<class T> constexpr unique_ptr<T> make_unique_for_overwrite();
```

*Constraints:* `T` is not an array type.

*Returns:* `unique_ptr<T>(new T)`.

``` cpp
template<class T> constexpr unique_ptr<T> make_unique_for_overwrite(size_t n);
```

*Constraints:* `T` is an array of unknown bound.

*Returns:* `unique_ptr<T>(new remove_extent_t<T>[n])`.

``` cpp
template<class T, class... Args> unspecified make_unique_for_overwrite(Args&&...) = delete;
```

*Constraints:* `T` is an array of known bound.

#### Specialized algorithms <a id="unique.ptr.special">[[unique.ptr.special]]</a>

``` cpp
template<class T, class D> constexpr void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;
```

*Constraints:* `is_swappable_v<D>` is `true`.

*Effects:* Calls `x.swap(y)`.

``` cpp
template<class T1, class D1, class T2, class D2>
  constexpr bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `x.get() == y.get()`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

Let `CT` denote

``` cpp
common_type_t<typename unique_ptr<T1, D1>::pointer,
              typename unique_ptr<T2, D2>::pointer>
```

*Mandates:*

- `unique_ptr<T1, D1>::pointer` is implicitly convertible to `CT` and
- `unique_ptr<T2, D2>::pointer` is implicitly convertible to `CT`.

*Preconditions:* The specialization `less<CT>` is a function object
type [[function.objects]] that induces a strict weak
ordering [[alg.sorting]] on the pointer values.

*Returns:* `less<CT>()(x.get(), y.get())`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `y < x`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(y < x)`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(x < y)`.

``` cpp
template<class T1, class D1, class T2, class D2>
  requires three_way_comparable_with<typename unique_ptr<T1, D1>::pointer,
                                     typename unique_ptr<T2, D2>::pointer>
  compare_three_way_result_t<typename unique_ptr<T1, D1>::pointer,
                             typename unique_ptr<T2, D2>::pointer>
    operator<=>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `compare_three_way()(x.get(), y.get())`.

``` cpp
template<class T, class D>
  constexpr bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
```

*Returns:* `!x`.

``` cpp
template<class T, class D>
  constexpr bool operator<(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  constexpr bool operator<(nullptr_t, const unique_ptr<T, D>& x);
```

*Preconditions:* The specialization `less<unique_ptr<T, D>::pointer>` is
a function object type [[function.objects]] that induces a strict weak
ordering [[alg.sorting]] on the pointer values.

*Returns:* The first function template returns

``` cpp
less<unique_ptr<T, D>::pointer>()(x.get(), nullptr)
```

The second function template returns

``` cpp
less<unique_ptr<T, D>::pointer>()(nullptr, x.get())
```

``` cpp
template<class T, class D>
  constexpr bool operator>(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  constexpr bool operator>(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `nullptr < x`. The second
function template returns `x < nullptr`.

``` cpp
template<class T, class D>
  constexpr bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  constexpr bool operator<=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(nullptr < x)`. The
second function template returns `!(x < nullptr)`.

``` cpp
template<class T, class D>
  constexpr bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  constexpr bool operator>=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(x < nullptr)`. The
second function template returns `!(nullptr < x)`.

``` cpp
template<class T, class D>
  requires three_way_comparable<typename unique_ptr<T, D>::pointer>
  constexpr compare_three_way_result_t<typename unique_ptr<T, D>::pointer>
    operator<=>(const unique_ptr<T, D>& x, nullptr_t);
```

*Returns:*

``` cpp
compare_three_way()(x.get(), static_cast<typename unique_ptr<T, D>::pointer>(nullptr)).
```

#### I/O <a id="unique.ptr.io">[[unique.ptr.io]]</a>

``` cpp
template<class E, class T, class Y, class D>
  basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const unique_ptr<Y, D>& p);
```

*Constraints:* `os << p.get()` is a valid expression.

*Effects:* Equivalent to: `os << p.get();`

*Returns:* `os`.

### Shared-ownership pointers <a id="util.sharedptr">[[util.sharedptr]]</a>

#### Class `bad_weak_ptr` <a id="util.smartptr.weak.bad">[[util.smartptr.weak.bad]]</a>

``` cpp
namespace std {
  class bad_weak_ptr : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

An exception of type `bad_weak_ptr` is thrown by the `shared_ptr`
constructor taking a `weak_ptr`.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

#### Class template `shared_ptr` <a id="util.smartptr.shared">[[util.smartptr.shared]]</a>

##### General <a id="util.smartptr.shared.general">[[util.smartptr.shared.general]]</a>

The `shared_ptr` class template stores a pointer, usually obtained via
`new`. `shared_ptr` implements semantics of shared ownership; the last
remaining owner of the pointer is responsible for destroying the object,
or otherwise releasing the resources associated with the stored pointer.
A `shared_ptr` is said to be empty if it does not own a pointer.

``` cpp
namespace std {
  template<class T> class shared_ptr {
  public:
    using element_type = remove_extent_t<T>;
    using weak_type    = weak_ptr<T>;

    // [util.smartptr.shared.const], constructors
    constexpr shared_ptr() noexcept;
    constexpr shared_ptr(nullptr_t) noexcept : shared_ptr() { }
    template<class Y>
      explicit shared_ptr(Y* p);
    template<class Y, class D>
      shared_ptr(Y* p, D d);
    template<class Y, class D, class A>
      shared_ptr(Y* p, D d, A a);
    template<class D>
      shared_ptr(nullptr_t p, D d);
    template<class D, class A>
      shared_ptr(nullptr_t p, D d, A a);
    template<class Y>
      shared_ptr(const shared_ptr<Y>& r, element_type* p) noexcept;
    template<class Y>
      shared_ptr(shared_ptr<Y>&& r, element_type* p) noexcept;
    shared_ptr(const shared_ptr& r) noexcept;
    template<class Y>
      shared_ptr(const shared_ptr<Y>& r) noexcept;
    shared_ptr(shared_ptr&& r) noexcept;
    template<class Y>
      shared_ptr(shared_ptr<Y>&& r) noexcept;
    template<class Y>
      explicit shared_ptr(const weak_ptr<Y>& r);
    template<class Y, class D>
      shared_ptr(unique_ptr<Y, D>&& r);

    // [util.smartptr.shared.dest], destructor
    ~shared_ptr();

    // [util.smartptr.shared.assign], assignment
    shared_ptr& operator=(const shared_ptr& r) noexcept;
    template<class Y>
      shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    shared_ptr& operator=(shared_ptr&& r) noexcept;
    template<class Y>
      shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
    template<class Y, class D>
      shared_ptr& operator=(unique_ptr<Y, D>&& r);

    // [util.smartptr.shared.mod], modifiers
    void swap(shared_ptr& r) noexcept;
    void reset() noexcept;
    template<class Y>
      void reset(Y* p);
    template<class Y, class D>
      void reset(Y* p, D d);
    template<class Y, class D, class A>
      void reset(Y* p, D d, A a);

    // [util.smartptr.shared.obs], observers
    element_type* get() const noexcept;
    T& operator*() const noexcept;
    T* operator->() const noexcept;
    element_type& operator[](ptrdiff_t i) const;
    long use_count() const noexcept;
    explicit operator bool() const noexcept;
    template<class U>
      bool owner_before(const shared_ptr<U>& b) const noexcept;
    template<class U>
      bool owner_before(const weak_ptr<U>& b) const noexcept;
  };

  template<class T>
    shared_ptr(weak_ptr<T>) -> shared_ptr<T>;
  template<class T, class D>
    shared_ptr(unique_ptr<T, D>) -> shared_ptr<T>;
}
```

Specializations of `shared_ptr` shall be *Cpp17CopyConstructible*,
*Cpp17CopyAssignable*, and *Cpp17\\Less\\Than\\Comparable*, allowing
their use in standard containers. Specializations of `shared_ptr` shall
be contextually convertible to `bool`, allowing their use in boolean
expressions and declarations in conditions.

The template parameter `T` of `shared_ptr` may be an incomplete type.

\[*Note 1*: `T` can be a function type. — *end note*\]

\[*Example 1*:

``` cpp
if (shared_ptr<X> px = dynamic_pointer_cast<X>(py)) {
  // do something with px
}
```

— *end example*\]

For purposes of determining the presence of a data race, member
functions shall access and modify only the `shared_ptr` and `weak_ptr`
objects themselves and not objects they refer to. Changes in
`use_count()` do not reflect modifications that can introduce data
races.

For the purposes of subclause [[smartptr]], a pointer type `Y*` is said
to be *compatible with* a pointer type `T*` when either `Y*` is
convertible to `T*` or `Y` is `U[N]` and `T` is cv `U[]`.

##### Constructors <a id="util.smartptr.shared.const">[[util.smartptr.shared.const]]</a>

In the constructor definitions below, enables `shared_from_this` with
`p`, for a pointer `p` of type `Y*`, means that if `Y` has an
unambiguous and accessible base class that is a specialization of
`enable_shared_from_this` [[util.smartptr.enab]], then `remove_cv_t<Y>*`
shall be implicitly convertible to `T*` and the constructor evaluates
the statement:

``` cpp
if (p != nullptr && p->weak_this.expired())
  p->weak_this = shared_ptr<remove_cv_t<Y>>(*this, const_cast<remove_cv_t<Y>*>(p));
```

The assignment to the `weak_this` member is not atomic and conflicts
with any potentially concurrent access to the same object
[[intro.multithread]].

``` cpp
constexpr shared_ptr() noexcept;
```

*Ensures:* `use_count() == 0 && get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(Y* p);
```

*Constraints:* When `T` is an array type, the expression `delete[] p` is
well-formed and either `T` is `U[N]` and `Y(*)[N]` is convertible to
`T*`, or `T` is `U[]` and `Y(*)[]` is convertible to `T*`. When `T` is
not an array type, the expression `delete p` is well-formed and `Y*` is
convertible to `T*`.

*Mandates:* `Y` is a complete type.

*Preconditions:* The expression `delete[] p`, when `T` is an array type,
or `delete p`, when `T` is not an array type, has well-defined behavior,
and does not throw exceptions.

*Effects:* When `T` is not an array type, constructs a `shared_ptr`
object that owns the pointer `p`. Otherwise, constructs a `shared_ptr`
that owns `p` and a deleter of an unspecified type that calls
`delete[] p`. When `T` is not an array type, enables `shared_from_this`
with `p`. If an exception is thrown, `delete p` is called when `T` is
not an array type, `delete[] p` otherwise.

*Ensures:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory cannot be obtained.

``` cpp
template<class Y, class D> shared_ptr(Y* p, D d);
template<class Y, class D, class A> shared_ptr(Y* p, D d, A a);
template<class D> shared_ptr(nullptr_t p, D d);
template<class D, class A> shared_ptr(nullptr_t p, D d, A a);
```

*Constraints:* `is_move_constructible_v<D>` is `true`, and `d(p)` is a
well-formed expression. For the first two overloads:

- If `T` is an array type, then either `T` is `U[N]` and `Y(*)[N]` is
  convertible to `T*`, or `T` is `U[]` and `Y(*)[]` is convertible to
  `T*`.
- If `T` is not an array type, then `Y*` is convertible to `T*`.

*Preconditions:* Construction of `d` and a deleter of type `D`
initialized with `std::move(d)` do not throw exceptions. The expression
`d(p)` has well-defined behavior and does not throw exceptions. `A`
meets the *Cpp17Allocator*
requirements [[allocator.requirements.general]].

*Effects:* Constructs a `shared_ptr` object that owns the object `p` and
the deleter `d`. When `T` is not an array type, the first and second
constructors enable `shared_from_this` with `p`. The second and fourth
constructors shall use a copy of `a` to allocate memory for internal
use. If an exception is thrown, `d(p)` is called.

*Ensures:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory cannot be obtained.

``` cpp
template<class Y> shared_ptr(const shared_ptr<Y>& r, element_type* p) noexcept;
template<class Y> shared_ptr(shared_ptr<Y>&& r, element_type* p) noexcept;
```

*Effects:* Constructs a `shared_ptr` instance that stores `p` and shares
ownership with the initial value of `r`.

*Ensures:* `get() == p`. For the second overload, `r` is empty and
`r.get() == nullptr`.

\[*Note 2*: Use of this constructor leads to a dangling pointer unless
`p` remains valid at least until the ownership group of `r` is
destroyed. — *end note*\]

\[*Note 3*: This constructor allows creation of an empty `shared_ptr`
instance with a non-null stored pointer. — *end note*\]

``` cpp
shared_ptr(const shared_ptr& r) noexcept;
template<class Y> shared_ptr(const shared_ptr<Y>& r) noexcept;
```

*Constraints:* For the second constructor, `Y*` is compatible with `T*`.

*Effects:* If `r` is empty, constructs an empty `shared_ptr` object;
otherwise, constructs a `shared_ptr` object that shares ownership with
`r`.

*Ensures:* `get() == r.get() && use_count() == r.use_count()`.

``` cpp
shared_ptr(shared_ptr&& r) noexcept;
template<class Y> shared_ptr(shared_ptr<Y>&& r) noexcept;
```

*Constraints:* For the second constructor, `Y*` is compatible with `T*`.

*Effects:* Move constructs a `shared_ptr` instance from `r`.

*Ensures:* `*this` contains the old value of `r`. `r` is empty, and
`r.get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(const weak_ptr<Y>& r);
```

*Constraints:* `Y*` is compatible with `T*`.

*Effects:* Constructs a `shared_ptr` object that shares ownership with
`r` and stores a copy of the pointer stored in `r`. If an exception is
thrown, the constructor has no effect.

*Ensures:* `use_count() == r.use_count()`.

*Throws:* `bad_weak_ptr` when `r.expired()`.

``` cpp
template<class Y, class D> shared_ptr(unique_ptr<Y, D>&& r);
```

*Constraints:* `Y*` is compatible with `T*` and
`unique_ptr<Y, D>::pointer` is convertible to `element_type*`.

*Effects:* If `r.get() == nullptr`, equivalent to `shared_ptr()`.
Otherwise, if `D` is not a reference type, equivalent to
`shared_ptr(r.release(), std::move(r.get_deleter()))`. Otherwise,
equivalent to `shared_ptr(r.release(), ref(r.get_deleter()))`. If an
exception is thrown, the constructor has no effect.

##### Destructor <a id="util.smartptr.shared.dest">[[util.smartptr.shared.dest]]</a>

``` cpp
~shared_ptr();
```

*Effects:*

- If `*this` is empty or shares ownership with another `shared_ptr`
  instance (`use_count() > 1`), there are no side effects.
- Otherwise, if `*this` owns an object `p` and a deleter `d`, `d(p)` is
  called.
- Otherwise, `*this` owns a pointer `p`, and `delete p` is called.

\[*Note 4*: Since the destruction of `*this` decreases the number of
instances that share ownership with `*this` by one, after `*this` has
been destroyed all `shared_ptr` instances that shared ownership with
`*this` will report a `use_count()` that is one less than its previous
value. — *end note*\]

##### Assignment <a id="util.smartptr.shared.assign">[[util.smartptr.shared.assign]]</a>

``` cpp
shared_ptr& operator=(const shared_ptr& r) noexcept;
template<class Y> shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `shared_ptr(r).swap(*this)`.

*Returns:* `*this`.

\[*Note 5*:

The use count updates caused by the temporary object construction and
destruction are not observable side effects, so the implementation can
meet the effects (and the implied guarantees) via different means,
without creating a temporary. In particular, in the example:

    shared_ptr<int> p(new int);
    shared_ptr<void> q(p);
    p = p;
    q = p;

both assignments can be no-ops.

— *end note*\]

``` cpp
shared_ptr& operator=(shared_ptr&& r) noexcept;
template<class Y> shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

``` cpp
template<class Y, class D> shared_ptr& operator=(unique_ptr<Y, D>&& r);
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

##### Modifiers <a id="util.smartptr.shared.mod">[[util.smartptr.shared.mod]]</a>

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

##### Observers <a id="util.smartptr.shared.obs">[[util.smartptr.shared.obs]]</a>

``` cpp
element_type* get() const noexcept;
```

*Returns:* The stored pointer.

``` cpp
T& operator*() const noexcept;
```

*Preconditions:* `get() != nullptr`.

*Returns:* `*get()`.

*Remarks:* When `T` is an array type or  , it is unspecified whether
this member function is declared. If it is declared, it is unspecified
what its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well-formed.

``` cpp
T* operator->() const noexcept;
```

*Preconditions:* `get() != nullptr`.

*Returns:* `get()`.

*Remarks:* When `T` is an array type, it is unspecified whether this
member function is declared. If it is declared, it is unspecified what
its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well-formed.

``` cpp
element_type& operator[](ptrdiff_t i) const;
```

*Preconditions:* `get() != nullptr && i >= 0`. If `T` is `U[N]`,
`i < N`.

*Returns:* `get()[i]`.

*Throws:* Nothing.

*Remarks:* When `T` is not an array type, it is unspecified whether this
member function is declared. If it is declared, it is unspecified what
its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well-formed.

``` cpp
long use_count() const noexcept;
```

*Synchronization:* None.

*Returns:* The number of `shared_ptr` objects, `*this` included, that
share ownership with `*this`, or `0` when `*this` is empty.

\[*Note 6*: `get() == nullptr` does not imply a specific return value of
`use_count()`. — *end note*\]

\[*Note 7*: `weak_ptr<T>::lock()` can affect the return value of
`use_count()`. — *end note*\]

\[*Note 8*: When multiple threads might affect the return value of
`use_count()`, the result is approximate. In particular,
`use_count() == 1` does not imply that accesses through a previously
destroyed `shared_ptr` have in any sense completed. — *end note*\]

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `get() != nullptr`.

``` cpp
template<class U> bool owner_before(const shared_ptr<U>& b) const noexcept;
template<class U> bool owner_before(const weak_ptr<U>& b) const noexcept;
```

*Returns:* An unspecified value such that

- `x.owner_before(y)` defines a strict weak ordering as defined
  in  [[alg.sorting]];
- under the equivalence relation defined by `owner_before`,
  `!a.owner_before(b) && !b.owner_before(a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

##### Creation <a id="util.smartptr.shared.create">[[util.smartptr.shared.create]]</a>

The common requirements that apply to all `make_shared`,
`allocate_shared`, `make_shared_for_overwrite`, and
`allocate_shared_for_overwrite` overloads, unless specified otherwise,
are described below.

``` cpp
template<class T, ...>
  shared_ptr<T> make_shared(args);
template<class T, class A, ...>
  shared_ptr<T> allocate_shared(const A& a, args);
template<class T, ...>
  shared_ptr<T> make_shared_for_overwrite(args);
template<class T, class A, ...>
  shared_ptr<T> allocate_shared_for_overwrite(const A& a, args);
```

*Preconditions:* `A` meets the *Cpp17Allocator*
requirements [[allocator.requirements.general]].

*Effects:* Allocates memory for an object of type `T` (or `U[N]` when
`T` is `U[]`, where `N` is determined from *args* as specified by the
concrete overload). The object is initialized from *args* as specified
by the concrete overload. The `allocate_shared` and
`allocate_shared_for_overwrite` templates use a copy of `a` (rebound for
an unspecified `value_type`) to allocate memory. If an exception is
thrown, the functions have no effect.

*Ensures:* `r.get() != nullptr && r.use_count() == 1`, where `r` is the
return value.

*Returns:* A `shared_ptr` instance that stores and owns the address of
the newly constructed object.

*Throws:* `bad_alloc`, or an exception thrown from `allocate` or from
the initialization of the object.

*Remarks:*

- Implementations should perform no more than one memory allocation.
  \[*Note 1*: This provides efficiency equivalent to an intrusive smart
  pointer. — *end note*\]
- When an object of an array type `U` is specified to have an initial
  value of `u` (of the same type), this shall be interpreted to mean
  that each array element of the object has as its initial value the
  corresponding element from `u`.
- When an object of an array type is specified to have a default initial
  value, this shall be interpreted to mean that each array element of
  the object has a default initial value.
- When a (sub)object of a non-array type `U` is specified to have an
  initial value of `v`, or `U(l...)`, where `l...` is a list of
  constructor arguments, `make_shared` shall initialize this (sub)object
  via the expression `::new(pv) U(v)` or `::new(pv) U(l...)`
  respectively, where `pv` has type `void*` and points to storage
  suitable to hold an object of type `U`.
- When a (sub)object of a non-array type `U` is specified to have an
  initial value of `v`, or `U(l...)`, where `l...` is a list of
  constructor arguments, `allocate_shared` shall initialize this
  (sub)object via the expression
  - `allocator_traits<A2>::construct(a2, pv, v)` or
  - `allocator_traits<A2>::construct(a2, pv, l...)`

  respectively, where `pv` points to storage suitable to hold an object
  of type `U` and `a2` of type `A2` is a rebound copy of the allocator
  `a` passed to `allocate_shared` such that its `value_type` is
  `remove_cv_t<U>`.
- When a (sub)object of non-array type `U` is specified to have a
  default initial value, `make_shared` shall initialize this (sub)object
  via the expression `::new(pv) U()`, where `pv` has type `void*` and
  points to storage suitable to hold an object of type `U`.
- When a (sub)object of non-array type `U` is specified to have a
  default initial value, `allocate_shared` shall initialize this
  (sub)object via the expression
  `allocator_traits<A2>::construct(a2, pv)`, where `pv` points to
  storage suitable to hold an object of type `U` and `a2` of type `A2`
  is a rebound copy of the allocator `a` passed to `allocate_shared`
  such that its `value_type` is `remove_cv_t<U>`.
- When a (sub)object of non-array type `U` is initialized by
  `make_shared_for_overwrite` or `allocate_shared_for_overwrite`, it is
  initialized via the expression `::new(pv) U`, where `pv` has type
  `void*` and points to storage suitable to hold an object of type `U`.
- Array elements are initialized in ascending order of their addresses.
- When the lifetime of the object managed by the return value ends, or
  when the initialization of an array element throws an exception, the
  initialized elements are destroyed in the reverse order of their
  original construction.
- When a (sub)object of non-array type `U` that was initialized by
  `make_shared` is to be destroyed, it is destroyed via the expression
  `pv->~U()` where `pv` points to that object of type `U`.
- When a (sub)object of non-array type `U` that was initialized by
  `allocate_shared` is to be destroyed, it is destroyed via the
  expression `allocator_traits<A2>::destroy(a2, pv)` where `pv` points
  to that object of type `remove_cv_t<U>` and `a2` of type `A2` is a
  rebound copy of the allocator `a` passed to `allocate_shared` such
  that its `value_type` is `remove_cv_t<U>`.

\[*Note 9*: These functions will typically allocate more memory than
`sizeof(T)` to allow for internal bookkeeping structures such as
reference counts. — *end note*\]

``` cpp
template<class T, class... Args>
  shared_ptr<T> make_shared(Args&&... args);                    // T is not array
template<class T, class A, class... Args>
  shared_ptr<T> allocate_shared(const A& a, Args&&... args);    // T is not array
```

*Constraints:* `T` is not an array type.

*Returns:* A `shared_ptr` to an object of type `T` with an initial value
`T(std::forward<Args>(args)...)`.

*Remarks:* The `shared_ptr` constructors called by these functions
enable `shared_from_this` with the address of the newly constructed
object of type `T`.

\[*Example 2*:

    shared_ptr<int> p = make_shared<int>(); // \texttt{shared_ptr} to \texttt{int()}
    shared_ptr<vector<int>> q = make_shared<vector<int>>(16, 1);
      // \texttt{shared_ptr} to vector of \texttt{16} elements with value \texttt{1}

— *end example*\]

``` cpp
template<class T> shared_ptr<T>
  make_shared(size_t N);                                        // T is U[]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a, size_t N);          // T is U[]
```

*Constraints:* `T` is of the form `U[]`.

*Returns:* A `shared_ptr` to an object of type `U[N]` with a default
initial value, where `U` is `remove_extent_t<T>`.

\[*Example 3*:

    shared_ptr<double[]> p = make_shared<double[]>(1024);
      // \texttt{shared_ptr} to a value-initialized \texttt{double[1024]}
    shared_ptr<double[][2][2]> q = make_shared<double[][2][2]>(6);
      // \texttt{shared_ptr} to a value-initialized \texttt{double[6][2][2]}

— *end example*\]

``` cpp
template<class T>
  shared_ptr<T> make_shared();                                  // T is U[N]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a);                    // T is U[N]
```

*Constraints:* `T` is of the form `U[N]`.

*Returns:* A `shared_ptr` to an object of type `T` with a default
initial value.

\[*Example 4*:

    shared_ptr<double[1024]> p = make_shared<double[1024]>();
      // \texttt{shared_ptr} to a value-initialized \texttt{double[1024]}
    shared_ptr<double[6][2][2]> q = make_shared<double[6][2][2]>();
      // \texttt{shared_ptr} to a value-initialized \texttt{double[6][2][2]}

— *end example*\]

``` cpp
template<class T>
  shared_ptr<T> make_shared(size_t N,
                            const remove_extent_t<T>& u);       // T is U[]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a, size_t N,
                                const remove_extent_t<T>& u);   // T is U[]
```

*Constraints:* `T` is of the form `U[]`.

*Returns:* A `shared_ptr` to an object of type `U[N]`, where `U` is
`remove_extent_t<T>` and each array element has an initial value of `u`.

\[*Example 5*:

    shared_ptr<double[]> p = make_shared<double[]>(1024, 1.0);
      // \texttt{shared_ptr} to a \texttt{double[1024]}, where each element is \texttt{1.0}
    shared_ptr<double[][2]> q = make_shared<double[][2]>(6, {1.0, 0.0});
      // \texttt{shared_ptr} to a \texttt{double[6][2]}, where each \texttt{double[2]} element is \texttt{{1.0, 0.0}}
    shared_ptr<vector<int>[]> r = make_shared<vector<int>[]>(4, {1, 2});
      // \texttt{shared_ptr} to a \texttt{vector<int>[4]}, where each vector has contents \texttt{{1, 2}}

— *end example*\]

``` cpp
template<class T>
  shared_ptr<T> make_shared(const remove_extent_t<T>& u);       // T is U[N]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a,
                                const remove_extent_t<T>& u);   // T is U[N]
```

*Constraints:* `T` is of the form `U[N]`.

*Returns:* A `shared_ptr` to an object of type `T`, where each array
element of type `remove_extent_t<T>` has an initial value of `u`.

\[*Example 6*:

    shared_ptr<double[1024]> p = make_shared<double[1024]>(1.0);
      // \texttt{shared_ptr} to a \texttt{double[1024]}, where each element is \texttt{1.0}
    shared_ptr<double[6][2]> q = make_shared<double[6][2]>({1.0, 0.0});
      // \texttt{shared_ptr} to a \texttt{double[6][2]}, where each double[2] element is \texttt{{1.0, 0.0}}
    shared_ptr<vector<int>[4]> r = make_shared<vector<int>[4]>({1, 2});
      // \texttt{shared_ptr} to a \texttt{vector<int>[4]}, where each vector has contents \texttt{{1, 2}}

— *end example*\]

``` cpp
template<class T>
  shared_ptr<T> make_shared_for_overwrite();
template<class T, class A>
  shared_ptr<T> allocate_shared_for_overwrite(const A& a);
```

*Constraints:* `T` is not an array of unknown bound.

*Returns:* A `shared_ptr` to an object of type `T`.

\[*Example 7*:

    struct X { double data[1024]; };
    shared_ptr<X> p = make_shared_for_overwrite<X>();
      // \texttt{shared_ptr} to a default-initialized \texttt{X}, where each element in \texttt{X::data} has an indeterminate value

    shared_ptr<double[1024]> q = make_shared_for_overwrite<double[1024]>();
      // \texttt{shared_ptr} to a default-initialized \texttt{double[1024]}, where each element has an indeterminate value

— *end example*\]

``` cpp
template<class T>
  shared_ptr<T> make_shared_for_overwrite(size_t N);
template<class T, class A>
  shared_ptr<T> allocate_shared_for_overwrite(const A& a, size_t N);
```

*Constraints:* `T` is an array of unknown bound.

*Returns:* A `shared_ptr` to an object of type `U[N]`, where `U` is
`remove_extent_t<T>`.

\[*Example 8*:

    shared_ptr<double[]> p = make_shared_for_overwrite<double[]>(1024);
      // \texttt{shared_ptr} to a default-initialized \texttt{double[1024]}, where each element has an indeterminate value

— *end example*\]

##### Comparison <a id="util.smartptr.shared.cmp">[[util.smartptr.shared.cmp]]</a>

``` cpp
template<class T, class U>
  bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `a.get() == b.get()`.

``` cpp
template<class T>
  bool operator==(const shared_ptr<T>& a, nullptr_t) noexcept;
```

*Returns:* `!a`.

``` cpp
template<class T, class U>
  strong_ordering operator<=>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `compare_three_way()(a.get(), b.get())`.

\[*Note 10*: Defining a comparison operator function allows `shared_ptr`
objects to be used as keys in associative containers. — *end note*\]

``` cpp
template<class T>
  strong_ordering operator<=>(const shared_ptr<T>& a, nullptr_t) noexcept;
```

*Returns:*

``` cpp
compare_three_way()(a.get(), static_cast<typename shared_ptr<T>::element_type*>(nullptr).
```

##### Specialized algorithms <a id="util.smartptr.shared.spec">[[util.smartptr.shared.spec]]</a>

``` cpp
template<class T>
  void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

##### Casts <a id="util.smartptr.shared.cast">[[util.smartptr.shared.cast]]</a>

``` cpp
template<class T, class U>
  shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> static_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `static_cast<T*>((U*)nullptr)` is
well-formed.

*Returns:*

``` cpp
shared_ptr<T>(R, static_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

where *`R`* is `r` for the first overload, and `std::move(r)` for the
second.

\[*Note 11*: The seemingly equivalent expression
`shared_ptr<T>(static_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*\]

``` cpp
template<class T, class U>
  shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> dynamic_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `dynamic_cast<T*>((U*)nullptr)` is
well-formed. The expression
`dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())` is
well-formed.

*Preconditions:* The expression
`dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())` has
well-defined behavior.

*Returns:*

- When `dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())`
  returns a non-null value `p`, `shared_ptr<T>(`*`R`*`, p)`, where *`R`*
  is `r` for the first overload, and `std::move(r)` for the second.
- Otherwise, `shared_ptr<T>()`.

\[*Note 12*: The seemingly equivalent expression
`shared_ptr<T>(dynamic_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*\]

``` cpp
template<class T, class U>
  shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> const_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `const_cast<T*>((U*)nullptr)` is well-formed.

*Returns:*

``` cpp
shared_ptr<T>(R, const_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

where *`R`* is `r` for the first overload, and `std::move(r)` for the
second.

\[*Note 13*: The seemingly equivalent expression
`shared_ptr<T>(const_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*\]

``` cpp
template<class T, class U>
  shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> reinterpret_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `reinterpret_cast<T*>((U*)nullptr)` is
well-formed.

*Returns:*

``` cpp
shared_ptr<T>(R, reinterpret_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

where *`R`* is `r` for the first overload, and `std::move(r)` for the
second.

\[*Note 14*: The seemingly equivalent expression
`shared_ptr<T>(reinterpret_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*\]

##### `get_deleter` <a id="util.smartptr.getdeleter">[[util.smartptr.getdeleter]]</a>

``` cpp
template<class D, class T>
  D* get_deleter(const shared_ptr<T>& p) noexcept;
```

*Returns:* If `p` owns a deleter `d` of type cv-unqualified `D`, returns
`addressof(d)`; otherwise returns . The returned pointer remains valid
as long as there exists a `shared_ptr` instance that owns `d`.

\[*Note 15*: It is unspecified whether the pointer remains valid longer
than that. This can happen if the implementation doesn’t destroy the
deleter until all `weak_ptr` instances that share ownership with `p`
have been destroyed. — *end note*\]

##### I/O <a id="util.smartptr.shared.io">[[util.smartptr.shared.io]]</a>

``` cpp
template<class E, class T, class Y>
  basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const shared_ptr<Y>& p);
```

*Effects:* As if by: `os << p.get();`

*Returns:* `os`.

#### Class template `weak_ptr` <a id="util.smartptr.weak">[[util.smartptr.weak]]</a>

##### General <a id="util.smartptr.weak.general">[[util.smartptr.weak.general]]</a>

The `weak_ptr` class template stores a weak reference to an object that
is already managed by a `shared_ptr`. To access the object, a `weak_ptr`
can be converted to a `shared_ptr` using the member function `lock`.

``` cpp
namespace std {
  template<class T> class weak_ptr {
  public:
    using element_type = remove_extent_t<T>;

    // [util.smartptr.weak.const], constructors
    constexpr weak_ptr() noexcept;
    template<class Y>
      weak_ptr(const shared_ptr<Y>& r) noexcept;
    weak_ptr(const weak_ptr& r) noexcept;
    template<class Y>
      weak_ptr(const weak_ptr<Y>& r) noexcept;
    weak_ptr(weak_ptr&& r) noexcept;
    template<class Y>
      weak_ptr(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.dest], destructor
    ~weak_ptr();

    // [util.smartptr.weak.assign], assignment
    weak_ptr& operator=(const weak_ptr& r) noexcept;
    template<class Y>
      weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
    template<class Y>
      weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    weak_ptr& operator=(weak_ptr&& r) noexcept;
    template<class Y>
      weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.mod], modifiers
    void swap(weak_ptr& r) noexcept;
    void reset() noexcept;

    // [util.smartptr.weak.obs], observers
    long use_count() const noexcept;
    bool expired() const noexcept;
    shared_ptr<T> lock() const noexcept;
    template<class U>
      bool owner_before(const shared_ptr<U>& b) const noexcept;
    template<class U>
      bool owner_before(const weak_ptr<U>& b) const noexcept;
  };

  template<class T>
    weak_ptr(shared_ptr<T>) -> weak_ptr<T>;
}
```

Specializations of `weak_ptr` shall be *Cpp17CopyConstructible* and
*Cpp17CopyAssignable*, allowing their use in standard containers. The
template parameter `T` of `weak_ptr` may be an incomplete type.

##### Constructors <a id="util.smartptr.weak.const">[[util.smartptr.weak.const]]</a>

``` cpp
constexpr weak_ptr() noexcept;
```

*Effects:* Constructs an empty `weak_ptr` object that stores a null
pointer value.

*Ensures:* `use_count() == 0`.

``` cpp
weak_ptr(const weak_ptr& r) noexcept;
template<class Y> weak_ptr(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr(const shared_ptr<Y>& r) noexcept;
```

*Constraints:* For the second and third constructors, `Y*` is compatible
with `T*`.

*Effects:* If `r` is empty, constructs an empty `weak_ptr` object that
stores a null pointer value; otherwise, constructs a `weak_ptr` object
that shares ownership with `r` and stores a copy of the pointer stored
in `r`.

*Ensures:* `use_count() == r.use_count()`.

``` cpp
weak_ptr(weak_ptr&& r) noexcept;
template<class Y> weak_ptr(weak_ptr<Y>&& r) noexcept;
```

*Constraints:* For the second constructor, `Y*` is compatible with `T*`.

*Effects:* Move constructs a `weak_ptr` instance from `r`.

*Ensures:* `*this` contains the old value of `r`. `r` is empty, stores a
null pointer value, and `r.use_count() == 0`.

##### Destructor <a id="util.smartptr.weak.dest">[[util.smartptr.weak.dest]]</a>

``` cpp
~weak_ptr();
```

*Effects:* Destroys this `weak_ptr` object but has no effect on the
object its stored pointer points to.

##### Assignment <a id="util.smartptr.weak.assign">[[util.smartptr.weak.assign]]</a>

``` cpp
weak_ptr& operator=(const weak_ptr& r) noexcept;
template<class Y> weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(r).swap(*this)`.

*Returns:* `*this`.

*Remarks:* The implementation may meet the effects (and the implied
guarantees) via different means, without creating a temporary object.

``` cpp
weak_ptr& operator=(weak_ptr&& r) noexcept;
template<class Y> weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

##### Modifiers <a id="util.smartptr.weak.mod">[[util.smartptr.weak.mod]]</a>

``` cpp
void swap(weak_ptr& r) noexcept;
```

*Effects:* Exchanges the contents of `*this` and `r`.

``` cpp
void reset() noexcept;
```

*Effects:* Equivalent to `weak_ptr().swap(*this)`.

##### Observers <a id="util.smartptr.weak.obs">[[util.smartptr.weak.obs]]</a>

``` cpp
long use_count() const noexcept;
```

*Returns:* `0` if `*this` is empty; otherwise, the number of
`shared_ptr` instances that share ownership with `*this`.

``` cpp
bool expired() const noexcept;
```

*Returns:* `use_count() == 0`.

``` cpp
shared_ptr<T> lock() const noexcept;
```

*Returns:* `expired() ? shared_ptr<T>() : shared_ptr<T>(*this)`,
executed atomically.

``` cpp
template<class U> bool owner_before(const shared_ptr<U>& b) const noexcept;
template<class U> bool owner_before(const weak_ptr<U>& b) const noexcept;
```

*Returns:* An unspecified value such that

- `x.owner_before(y)` defines a strict weak ordering as defined
  in  [[alg.sorting]];
- under the equivalence relation defined by `owner_before`,
  `!a.owner_before(b) && !b.owner_before(a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

##### Specialized algorithms <a id="util.smartptr.weak.spec">[[util.smartptr.weak.spec]]</a>

``` cpp
template<class T>
  void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

#### Class template `owner_less` <a id="util.smartptr.ownerless">[[util.smartptr.ownerless]]</a>

The class template `owner_less` allows ownership-based mixed comparisons
of shared and weak pointers.

``` cpp
namespace std {
  template<class T = void> struct owner_less;

  template<class T> struct owner_less<shared_ptr<T>> {
    bool operator()(const shared_ptr<T>&, const shared_ptr<T>&) const noexcept;
    bool operator()(const shared_ptr<T>&, const weak_ptr<T>&) const noexcept;
    bool operator()(const weak_ptr<T>&, const shared_ptr<T>&) const noexcept;
  };

  template<class T> struct owner_less<weak_ptr<T>> {
    bool operator()(const weak_ptr<T>&, const weak_ptr<T>&) const noexcept;
    bool operator()(const shared_ptr<T>&, const weak_ptr<T>&) const noexcept;
    bool operator()(const weak_ptr<T>&, const shared_ptr<T>&) const noexcept;
  };

  template<> struct owner_less<void> {
    template<class T, class U>
      bool operator()(const shared_ptr<T>&, const shared_ptr<U>&) const noexcept;
    template<class T, class U>
      bool operator()(const shared_ptr<T>&, const weak_ptr<U>&) const noexcept;
    template<class T, class U>
      bool operator()(const weak_ptr<T>&, const shared_ptr<U>&) const noexcept;
    template<class T, class U>
      bool operator()(const weak_ptr<T>&, const weak_ptr<U>&) const noexcept;

    using is_transparent = unspecified;
  };
}
```

`operator()(x, y)` returns `x.owner_before(y)`.

\[*Note 1*:

Note that

- `operator()` defines a strict weak ordering as defined in 
  [[alg.sorting]];
- two `shared_ptr` or `weak_ptr` instances are equivalent under the
  equivalence relation defined by `operator()`,
  `!operator()(a, b) && !operator()(b, a)`, if and only if they share
  ownership or are both empty.

— *end note*\]

#### Class template `enable_shared_from_this` <a id="util.smartptr.enab">[[util.smartptr.enab]]</a>

A class `T` can inherit from `enable_shared_from_this<T>` to inherit the
`shared_from_this` member functions that obtain a `shared_ptr` instance
pointing to `*this`.

\[*Example 1*:

``` cpp
struct X: public enable_shared_from_this<X> { };

int main() {
  shared_ptr<X> p(new X);
  shared_ptr<X> q = p->shared_from_this();
  assert(p == q);
  assert(!p.owner_before(q) && !q.owner_before(p)); // p and q share ownership
}
```

— *end example*\]

``` cpp
namespace std {
  template<class T> class enable_shared_from_this {
  protected:
    constexpr enable_shared_from_this() noexcept;
    enable_shared_from_this(const enable_shared_from_this&) noexcept;
    enable_shared_from_this& operator=(const enable_shared_from_this&) noexcept;
    ~enable_shared_from_this();

  public:
    shared_ptr<T> shared_from_this();
    shared_ptr<T const> shared_from_this() const;
    weak_ptr<T> weak_from_this() noexcept;
    weak_ptr<T const> weak_from_this() const noexcept;

  private:
    mutable weak_ptr<T> weak_this;  // exposition only
  };
}
```

The template parameter `T` of `enable_shared_from_this` may be an
incomplete type.

``` cpp
constexpr enable_shared_from_this() noexcept;
enable_shared_from_this(const enable_shared_from_this<T>&) noexcept;
```

*Effects:* Value-initializes `weak_this`.

``` cpp
enable_shared_from_this<T>& operator=(const enable_shared_from_this<T>&) noexcept;
```

*Returns:* `*this`.

\[*Note 1*: `weak_this` is not changed. — *end note*\]

``` cpp
shared_ptr<T>       shared_from_this();
shared_ptr<T const> shared_from_this() const;
```

*Returns:* `shared_ptr<T>(weak_this)`.

``` cpp
weak_ptr<T>       weak_from_this() noexcept;
weak_ptr<T const> weak_from_this() const noexcept;
```

*Returns:* `weak_this`.

### Smart pointer hash support <a id="util.smartptr.hash">[[util.smartptr.hash]]</a>

``` cpp
template<class T, class D> struct hash<unique_ptr<T, D>>;
```

Letting `UP` be `unique_ptr<T, D>`, the specialization `hash<UP>` is
enabled [[unord.hash]] if and only if `hash<typename UP::pointer>` is
enabled. When enabled, for an object `p` of type `UP`, `hash<UP>()(p)`
evaluates to the same value as `hash<typename UP::pointer>()(p.get())`.
The member functions are not guaranteed to be .

``` cpp
template<class T> struct hash<shared_ptr<T>>;
```

For an object `p` of type `shared_ptr<T>`, `hash<shared_ptr<T>>()(p)`
evaluates to the same value as
`hash<typename shared_ptr<T>::element_type*>()(p.get())`.

### Smart pointer adaptors <a id="smartptr.adapt">[[smartptr.adapt]]</a>

#### Class template `out_ptr_t` <a id="out.ptr.t">[[out.ptr.t]]</a>

`out_ptr_t` is a class template used to adapt types such as smart
pointers [[smartptr]] for functions that use output pointer parameters.

\[*Example 1*:

``` cpp
#include <memory>
#include <cstdio>

int fopen_s(std::FILE** f, const char* name, const char* mode);

struct fclose_deleter {
  void operator()(std::FILE* f) const noexcept {
    std::fclose(f);
  }
};

int main(int, char*[]) {
  constexpr const char* file_name = "ow.o";
  std::unique_ptr<std::FILE, fclose_deleter> file_ptr;
  int err = fopen_s(std::out_ptr<std::FILE*>(file_ptr), file_name, "r+b");
  if (err != 0)
    return 1;
  // *file_ptr is valid
  return 0;
}
```

`unique_ptr` can be used with `out_ptr` to be passed into an output
pointer-style function, without needing to hold onto an intermediate
pointer value and manually delete it on error or failure.

— *end example*\]

``` cpp
namespace std {
  template<class Smart, class Pointer, class... Args>
  class out_ptr_t {
  public:
    explicit out_ptr_t(Smart&, Args...);
    out_ptr_t(const out_ptr_t&) = delete;

    ~out_ptr_t();

    operator Pointer*() const noexcept;
    operator void**() const noexcept;

  private:
    Smart& s;                   // exposition only
    tuple<Args...> a;           // exposition only
    Pointer p;                  // exposition only
  };
}
```

`Pointer` shall meet the *Cpp17NullablePointer* requirements. If `Smart`
is a specialization of `shared_ptr` and `sizeof...(Args) == 0`, the
program is ill-formed.

\[*Note 1*: It is typically a user error to reset a `shared_ptr` without
specifying a deleter, as `shared_ptr` will replace a custom deleter upon
usage of `reset`, as specified in
[[util.smartptr.shared.mod]]. — *end note*\]

Program-defined specializations of `out_ptr_t` that depend on at least
one program-defined type need not meet the requirements for the primary
template.

Evaluations of the conversion functions on the same object may conflict
[[intro.races]].

``` cpp
explicit out_ptr_t(Smart& smart, Args... args);
```

*Effects:* Initializes `s` with `smart`, `a` with
`std::forward<Args>(args)...`, and value-initializes `p`. Then,
equivalent to:

- s.reset();

  if the expression `s.reset()` is well-formed;

- otherwise,
      s = Smart();

  if `is_constructible_v<Smart>` is `true`;

- otherwise, the program is ill-formed.

\[*Note 2*: The constructor is not `noexcept` to allow for a variety of
non-terminating and safe implementation strategies. For example, an
implementation can allocate a `shared_ptr`’s internal node in the
constructor and let implementation-defined exceptions escape safely. The
destructor can then move the allocated control block in directly and
avoid any other exceptions. — *end note*\]

``` cpp
~out_ptr_t();
```

Let `SP` be *`POINTER_OF_OR`*`(Smart, Pointer)`[[memory.general]].

*Effects:* Equivalent to:

- if (p) {
        apply([&](auto&&... args) {
          s.reset(static_cast<SP>(p), std::forward<Args>(args)...); }, std::move(a));
      }

  if the expression
  `s.reset(static_cast<SP>(p), std::forward<Args>(args)...)` is
  well-formed;

- otherwise,
      if (p) {
        apply([&](auto&&... args) {
          s = Smart(static_cast<SP>(p), std::forward<Args>(args)...); }, std::move(a));
      }

  if `is_constructible_v<Smart, SP, Args...>` is `true`;

- otherwise, the program is ill-formed.

``` cpp
operator Pointer*() const noexcept;
```

*Preconditions:* `operator void**()` has not been called on `*this`.

*Returns:* `addressof(const_cast<Pointer&>(p))`.

``` cpp
operator void**() const noexcept;
```

*Constraints:* `is_same_v<Pointer, void*>` is `false`.

*Mandates:* `is_pointer_v<Pointer>` is `true`.

*Preconditions:* `operator Pointer*()` has not been called on `*this`.

*Returns:* A pointer value `v` such that:

- the initial value `*v` is equivalent to `static_cast<void*>(p)` and
- any modification of `*v` that is not followed by a subsequent
  modification of `*this` affects the value of `p` during the
  destruction of `*this`, such that `static_cast<void*>(p) == *v`.

*Remarks:* Accessing `*v` outside the lifetime of `*this` has undefined
behavior.

\[*Note 3*: `reinterpret_cast<void**>(static_cast<Pointer*>(*this))` can
be a viable implementation strategy for some
implementations. — *end note*\]

#### Function template `out_ptr` <a id="out.ptr">[[out.ptr]]</a>

``` cpp
template<class Pointer = void, class Smart, class... Args>
  auto out_ptr(Smart& s, Args&&... args);
```

Let `P` be `Pointer` if `is_void_v<Pointer>` is `false`, otherwise
*`POINTER_OF`*`(Smart)`.

*Returns:*
`out_ptr_t<Smart, P, Args&&...>(s, std::forward<Args>(args)...)`

#### Class template `inout_ptr_t` <a id="inout.ptr.t">[[inout.ptr.t]]</a>

`inout_ptr_t` is a class template used to adapt types such as smart
pointers [[smartptr]] for functions that use output pointer parameters
whose dereferenced values may first be deleted before being set to
another allocated value.

\[*Example 1*:

``` cpp
#include <memory>

struct star_fish* star_fish_alloc();
int star_fish_populate(struct star_fish** ps, const char* description);

struct star_fish_deleter {
  void operator() (struct star_fish* c) const noexcept;
};

using star_fish_ptr = std::unique_ptr<star_fish, star_fish_deleter>;

int main(int, char*[]) {
  star_fish_ptr peach(star_fish_alloc());
  // ...
  // used, need to re-make
  int err = star_fish_populate(std::inout_ptr(peach), "caring clown-fish liker");
  return err;
}
```

A `unique_ptr` can be used with `inout_ptr` to be passed into an output
pointer-style function. The original value will be properly deleted
according to the function it is used with and a new value reset in its
place.

— *end example*\]

``` cpp
namespace std {
  template<class Smart, class Pointer, class... Args>
  class inout_ptr_t {
  public:
    explicit inout_ptr_t(Smart&, Args...);
    inout_ptr_t(const inout_ptr_t&) = delete;

    ~inout_ptr_t();

    operator Pointer*() const noexcept;
    operator void**() const noexcept;

  private:
    Smart& s;                   // exposition only
    tuple<Args...> a;           // exposition only
    Pointer p;                  // exposition only
  };
}
```

`Pointer` shall meet the *Cpp17NullablePointer* requirements. If `Smart`
is a specialization of `shared_ptr`, the program is ill-formed.

\[*Note 1*: It is impossible to properly acquire unique ownership of the
managed resource from a `shared_ptr` given its shared ownership
model. — *end note*\]

Program-defined specializations of `inout_ptr_t` that depend on at least
one program-defined type need not meet the requirements for the primary
template.

Evaluations of the conversion functions on the same object may conflict
[[intro.races]].

``` cpp
explicit inout_ptr_t(Smart& smart, Args... args);
```

*Effects:* Initializes `s` with `smart`, `a` with
`std::forward<Args>(args)...`, and `p` to either

- `smart` if `is_pointer_v<Smart>` is `true`,
- otherwise, `smart.get()`.

*Remarks:* An implementation can call `s.release()`.

\[*Note 2*: The constructor is not `noexcept` to allow for a variety of
non-terminating and safe implementation strategies. For example, an
intrusive pointer implementation with a control block can allocate in
the constructor and safely fail with an exception. — *end note*\]

``` cpp
~inout_ptr_t();
```

Let `SP` be *`POINTER_OF_OR`*`(Smart, Pointer)`[[memory.general]].

Let *release-statement* be `s.release();` if an implementation does not
call `s.release()` in the constructor. Otherwise, it is empty.

*Effects:* Equivalent to:

- if (p) {
        apply([&](auto&&... args) {
          s = Smart( static_cast<SP>(p), std::forward<Args>(args)...); }, std::move(a));
      }

  if `is_pointer_v<Smart>` is `true`;

- otherwise,
      release-statement;
      if (p) {
        apply([&](auto&&... args) {
          s.reset(static_cast<SP>(p), std::forward<Args>(args)...); }, std::move(a));
      }

  if the expression
  `s.reset(static_cast<SP>(p), std::forward<Args>(args)...)` is
  well-formed;

- otherwise,
      release-statement;
      if (p) {
        apply([&](auto&&... args) {
          s = Smart(static_cast<SP>(p), std::forward<Args>(args)...); }, std::move(a));
      }

  if `is_constructible_v<Smart, SP, Args...>` is `true`;

- otherwise, the program is ill-formed.

``` cpp
operator Pointer*() const noexcept;
```

*Preconditions:* `operator void**()` has not been called on `*this`.

*Returns:* `addressof(const_cast<Pointer&>(p))`.

``` cpp
operator void**() const noexcept;
```

*Constraints:* `is_same_v<Pointer, void*>` is `false`.

*Mandates:* `is_pointer_v<Pointer>` is `true`.

*Preconditions:* `operator Pointer*()` has not been called on `*this`.

*Returns:* A pointer value `v` such that:

- the initial value `*v` is equivalent to `static_cast<void*>(p)` and
- any modification of `*v` that is not followed by subsequent
  modification of `*this` affects the value of `p` during the
  destruction of `*this`, such that `static_cast<void*>(p) == *v`.

*Remarks:* Accessing `*v` outside the lifetime of `*this` has undefined
behavior.

\[*Note 3*: `reinterpret_cast<void**>(static_cast<Pointer*>(*this))` can
be a viable implementation strategy for some
implementations. — *end note*\]

#### Function template `inout_ptr` <a id="inout.ptr">[[inout.ptr]]</a>

``` cpp
template<class Pointer = void, class Smart, class... Args>
  auto inout_ptr(Smart& s, Args&&... args);
```

Let `P` be `Pointer` if `is_void_v<Pointer>` is `false`, otherwise
*`POINTER_OF`*`(Smart)`.

*Returns:*
`inout_ptr_t<Smart, P, Args&&...>(s, std::forward<Args>(args)...)`.

## Memory resources <a id="mem.res">[[mem.res]]</a>

### Header `<memory_resource>` synopsis <a id="mem.res.syn">[[mem.res.syn]]</a>

``` cpp
namespace std::pmr {
  // [mem.res.class], class memory_resource
  class memory_resource;

  bool operator==(const memory_resource& a, const memory_resource& b) noexcept;

  // [mem.poly.allocator.class], class template polymorphic_allocator
  template<class Tp = byte> class polymorphic_allocator;

  template<class T1, class T2>
    bool operator==(const polymorphic_allocator<T1>& a,
                    const polymorphic_allocator<T2>& b) noexcept;

  // [mem.res.global], global memory resources
  memory_resource* new_delete_resource() noexcept;
  memory_resource* null_memory_resource() noexcept;
  memory_resource* set_default_resource(memory_resource* r) noexcept;
  memory_resource* get_default_resource() noexcept;

  // [mem.res.pool], pool resource classes
  struct pool_options;
  class synchronized_pool_resource;
  class unsynchronized_pool_resource;
  class monotonic_buffer_resource;
}
```

### Class `memory_resource` <a id="mem.res.class">[[mem.res.class]]</a>

#### General <a id="mem.res.class.general">[[mem.res.class.general]]</a>

The `memory_resource` class is an abstract interface to an unbounded set
of classes encapsulating memory resources.

``` cpp
namespace std::pmr {
  class memory_resource {
    static constexpr size_t max_align = alignof(max_align_t);   // exposition only

  public:
    memory_resource() = default;
    memory_resource(const memory_resource&) = default;
    virtual ~memory_resource();

    memory_resource& operator=(const memory_resource&) = default;

    [[nodiscard]] void* allocate(size_t bytes, size_t alignment = max_align);
    void deallocate(void* p, size_t bytes, size_t alignment = max_align);

    bool is_equal(const memory_resource& other) const noexcept;

  private:
    virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
    virtual void do_deallocate(void* p, size_t bytes, size_t alignment) = 0;

    virtual bool do_is_equal(const memory_resource& other) const noexcept = 0;
  };
}
```

#### Public member functions <a id="mem.res.public">[[mem.res.public]]</a>

``` cpp
~memory_resource();
```

*Effects:* Destroys this `memory_resource`.

``` cpp
[[nodiscard]] void* allocate(size_t bytes, size_t alignment = max_align);
```

*Effects:* Allocates storage by calling `do_allocate(bytes, alignment)`
and implicitly creates objects within the allocated region of storage.

*Returns:* A pointer to a suitable created object [[intro.object]] in
the allocated region of storage.

*Throws:* What and when the call to `do_allocate` throws.

``` cpp
void deallocate(void* p, size_t bytes, size_t alignment = max_align);
```

*Effects:* Equivalent to `do_deallocate(p, bytes, alignment)`.

``` cpp
bool is_equal(const memory_resource& other) const noexcept;
```

*Effects:* Equivalent to: `return do_is_equal(other);`

#### Private virtual member functions <a id="mem.res.private">[[mem.res.private]]</a>

``` cpp
virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
```

*Preconditions:* `alignment` is a power of two.

*Returns:* A derived class shall implement this function to return a
pointer to allocated storage [[basic.stc.dynamic.allocation]] with a
size of at least `bytes`, aligned to the specified `alignment`.

*Throws:* A derived class implementation shall throw an appropriate
exception if it is unable to allocate memory with the requested size and
alignment.

``` cpp
virtual void do_deallocate(void* p, size_t bytes, size_t alignment) = 0;
```

*Preconditions:* `p` was returned from a prior call to
`allocate(bytes, alignment)` on a memory resource equal to `*this`, and
the storage at `p` has not yet been deallocated.

*Effects:* A derived class shall implement this function to dispose of
allocated storage.

*Throws:* Nothing.

``` cpp
virtual bool do_is_equal(const memory_resource& other) const noexcept = 0;
```

*Returns:* A derived class shall implement this function to return
`true` if memory allocated from can be deallocated from `other` and
vice-versa, otherwise `false`.

\[*Note 1*: It is possible that the most-derived type of `other` does
not match the type of . For a derived class `D`, an implementation of
this function can immediately return `false` if
`dynamic_cast<const D*>(&other) == nullptr`. — *end note*\]

#### Equality <a id="mem.res.eq">[[mem.res.eq]]</a>

``` cpp
bool operator==(const memory_resource& a, const memory_resource& b) noexcept;
```

*Returns:* `&a == &b || a.is_equal(b)`.

### Class template `polymorphic_allocator` <a id="mem.poly.allocator.class">[[mem.poly.allocator.class]]</a>

#### General <a id="mem.poly.allocator.class.general">[[mem.poly.allocator.class.general]]</a>

A specialization of class template `pmr::polymorphic_allocator` meets
the *Cpp17Allocator* requirements [[allocator.requirements.general]] if
its template argument is a cv-unqualified object type. Constructed with
different memory resources, different instances of the same
specialization of `pmr::polymorphic_allocator` can exhibit entirely
different allocation behavior. This runtime polymorphism allows objects
that use `polymorphic_allocator` to behave as if they used different
allocator types at run time even though they use the same static
allocator type.

A specialization of class template `pmr::polymorphic_allocator` meets
the allocator completeness requirements
[[allocator.requirements.completeness]] if its template argument is a
cv-unqualified object type.

``` cpp
namespace std::pmr {
  template<class Tp = byte> class polymorphic_allocator {
    memory_resource* memory_rsrc;       // exposition only

  public:
    using value_type = Tp;

    // [mem.poly.allocator.ctor], constructors
    polymorphic_allocator() noexcept;
    polymorphic_allocator(memory_resource* r);

    polymorphic_allocator(const polymorphic_allocator& other) = default;

    template<class U>
      polymorphic_allocator(const polymorphic_allocator<U>& other) noexcept;

    polymorphic_allocator& operator=(const polymorphic_allocator&) = delete;

    // [mem.poly.allocator.mem], member functions
    [[nodiscard]] Tp* allocate(size_t n);
    void deallocate(Tp* p, size_t n);

    [[nodiscard]] void* allocate_bytes(size_t nbytes, size_t alignment = alignof(max_align_t));
    void deallocate_bytes(void* p, size_t nbytes, size_t alignment = alignof(max_align_t));
    template<class T> [[nodiscard]] T* allocate_object(size_t n = 1);
    template<class T> void deallocate_object(T* p, size_t n = 1);
    template<class T, class... CtorArgs> [[nodiscard]] T* new_object(CtorArgs&&... ctor_args);
    template<class T> void delete_object(T* p);

    template<class T, class... Args>
      void construct(T* p, Args&&... args);

    polymorphic_allocator select_on_container_copy_construction() const;

    memory_resource* resource() const;

    // friends
    friend bool operator==(const polymorphic_allocator& a,
                           const polymorphic_allocator& b) noexcept {
      return *a.resource() == *b.resource();
    }
  };
}
```

#### Constructors <a id="mem.poly.allocator.ctor">[[mem.poly.allocator.ctor]]</a>

``` cpp
polymorphic_allocator() noexcept;
```

*Effects:* Sets `memory_rsrc` to `get_default_resource()`.

``` cpp
polymorphic_allocator(memory_resource* r);
```

*Preconditions:* `r` is non-null.

*Effects:* Sets `memory_rsrc` to `r`.

*Throws:* Nothing.

\[*Note 1*: This constructor provides an implicit conversion from
`memory_resource*`. — *end note*\]

``` cpp
template<class U> polymorphic_allocator(const polymorphic_allocator<U>& other) noexcept;
```

*Effects:* Sets `memory_rsrc` to `other.resource()`.

#### Member functions <a id="mem.poly.allocator.mem">[[mem.poly.allocator.mem]]</a>

``` cpp
[[nodiscard]] Tp* allocate(size_t n);
```

*Effects:* If `numeric_limits<size_t>::max() / sizeof(Tp) < n`, throws
`bad_array_new_length`. Otherwise equivalent to:

``` cpp
return static_cast<Tp*>(memory_rsrc->allocate(n * sizeof(Tp), alignof(Tp)));
```

``` cpp
void deallocate(Tp* p, size_t n);
```

*Preconditions:* `p` was allocated from a memory resource `x`, equal to
`*memory_rsrc`, using `x.allocate(n * sizeof(Tp), alignof(Tp))`.

*Effects:* Equivalent to
`memory_rsrc->deallocate(p, n * sizeof(Tp), alignof(Tp))`.

*Throws:* Nothing.

``` cpp
[[nodiscard]] void* allocate_bytes(size_t nbytes, size_t alignment = alignof(max_align_t));
```

*Effects:* Equivalent to:
`return memory_rsrc->allocate(nbytes, alignment);`

\[*Note 1*: The return type is `void*` (rather than, e.g., `byte*`) to
support conversion to an arbitrary pointer type `U*` by
`static_cast<U*>`, thus facilitating construction of a `U` object in the
allocated memory. — *end note*\]

``` cpp
void deallocate_bytes(void* p, size_t nbytes, size_t alignment = alignof(max_align_t));
```

*Effects:* Equivalent to
`memory_rsrc->deallocate(p, nbytes, alignment)`.

``` cpp
template<class T>
  [[nodiscard]] T* allocate_object(size_t n = 1);
```

*Effects:* Allocates memory suitable for holding an array of `n` objects
of type `T`, as follows:

- if `numeric_limits<size_t>::max() / sizeof(T) < n`, throws
  `bad_array_new_length`,
- otherwise equivalent to:
      return static_cast<T*>(allocate_bytes(n*sizeof(T), alignof(T)));

\[*Note 2*: `T` is not deduced and must therefore be provided as a
template argument. — *end note*\]

``` cpp
template<class T>
  void deallocate_object(T* p, size_t n = 1);
```

*Effects:* Equivalent to `deallocate_bytes(p, n*sizeof(T), alignof(T))`.

``` cpp
template<class T, class... CtorArgs>
  [[nodiscard]] T* new_object(CtorArgs&&... ctor_args);
```

*Effects:* Allocates and constructs an object of type `T`, as follows.
Equivalent to:

``` cpp
T* p = allocate_object<T>();
try {
  construct(p, std::forward<CtorArgs>(ctor_args)...);
} catch (...) {
  deallocate_object(p);
  throw;
}
return p;
```

\[*Note 3*: `T` is not deduced and must therefore be provided as a
template argument. — *end note*\]

``` cpp
template<class T>
  void delete_object(T* p);
```

*Effects:* Equivalent to:

``` cpp
allocator_traits<polymorphic_allocator>::destroy(*this, p);
deallocate_object(p);
```

``` cpp
template<class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Mandates:* Uses-allocator construction of `T` with allocator `*this`
(see  [[allocator.uses.construction]]) and constructor arguments
`std::forward<Args>(args)...` is well-formed.

*Effects:* Construct a `T` object in the storage whose address is
represented by `p` by uses-allocator construction with allocator `*this`
and constructor arguments `std::forward<Args>(args)...`.

*Throws:* Nothing unless the constructor for `T` throws.

``` cpp
polymorphic_allocator select_on_container_copy_construction() const;
```

*Returns:* `polymorphic_allocator()`.

\[*Note 4*: The memory resource is not propagated. — *end note*\]

``` cpp
memory_resource* resource() const;
```

*Returns:* `memory_rsrc`.

#### Equality <a id="mem.poly.allocator.eq">[[mem.poly.allocator.eq]]</a>

``` cpp
template<class T1, class T2>
  bool operator==(const polymorphic_allocator<T1>& a,
                  const polymorphic_allocator<T2>& b) noexcept;
```

*Returns:* `*a.resource() == *b.resource()`.

### Access to program-wide `memory_resource` objects <a id="mem.res.global">[[mem.res.global]]</a>

``` cpp
memory_resource* new_delete_resource() noexcept;
```

*Returns:* A pointer to a static-duration object of a type derived from
`memory_resource` that can serve as a resource for allocating memory
using `::operator new` and `::operator delete`. The same value is
returned every time this function is called. For a return value `p` and
a memory resource `r`, `p->is_equal(r)` returns `&r == p`.

``` cpp
memory_resource* null_memory_resource() noexcept;
```

*Returns:* A pointer to a static-duration object of a type derived from
`memory_resource` for which `allocate()` always throws `bad_alloc` and
for which `deallocate()` has no effect. The same value is returned every
time this function is called. For a return value `p` and a memory
resource `r`, `p->is_equal(r)` returns `&r == p`.

The *default memory resource pointer* is a pointer to a memory resource
that is used by certain facilities when an explicit memory resource is
not supplied through the interface. Its initial value is the return
value of `new_delete_resource()`.

``` cpp
memory_resource* set_default_resource(memory_resource* r) noexcept;
```

*Effects:* If `r` is non-null, sets the value of the default memory
resource pointer to `r`, otherwise sets the default memory resource
pointer to `new_delete_resource()`.

*Returns:* The previous value of the default memory resource pointer.

*Remarks:* Calling the `set_default_resource` and `get_default_resource`
functions shall not incur a data race. A call to the
`set_default_resource` function shall synchronize with subsequent calls
to the `set_default_resource` and `get_default_resource` functions.

``` cpp
memory_resource* get_default_resource() noexcept;
```

*Returns:* The current value of the default memory resource pointer.

### Pool resource classes <a id="mem.res.pool">[[mem.res.pool]]</a>

#### Classes `synchronized_pool_resource` and `unsynchronized_pool_resource` <a id="mem.res.pool.overview">[[mem.res.pool.overview]]</a>

The `synchronized_pool_resource` and `unsynchronized_pool_resource`
classes (collectively called *pool resource classes*) are
general-purpose memory resources having the following qualities:

- Each resource frees its allocated memory on destruction, even if
  `deallocate` has not been called for some of the allocated blocks.
- A pool resource consists of a collection of *pools*, serving requests
  for different block sizes. Each individual pool manages a collection
  of *chunks* that are in turn divided into blocks of uniform size,
  returned via calls to `do_allocate`. Each call to
  `do_allocate(size, alignment)` is dispatched to the pool serving the
  smallest blocks accommodating at least `size` bytes.
- When a particular pool is exhausted, allocating a block from that pool
  results in the allocation of an additional chunk of memory from the
  *upstream allocator* (supplied at construction), thus replenishing the
  pool. With each successive replenishment, the chunk size obtained
  increases geometrically.
  \[*Note 2*: By allocating memory in chunks, the pooling strategy
  increases the chance that consecutive allocations will be close
  together in memory. — *end note*\]
- Allocation requests that exceed the largest block size of any pool are
  fulfilled directly from the upstream allocator.
- A `pool_options` struct may be passed to the pool resource
  constructors to tune the largest block size and the maximum chunk
  size.

A `synchronized_pool_resource` may be accessed from multiple threads
without external synchronization and may have thread-specific pools to
reduce synchronization costs. An `unsynchronized_pool_resource` class
may not be accessed from multiple threads simultaneously and thus avoids
the cost of synchronization entirely in single-threaded applications.

``` cpp
namespace std::pmr {
  struct pool_options {
    size_t max_blocks_per_chunk = 0;
    size_t largest_required_pool_block = 0;
  };

  class synchronized_pool_resource : public memory_resource {
  public:
    synchronized_pool_resource(const pool_options& opts, memory_resource* upstream);

    synchronized_pool_resource()
        : synchronized_pool_resource(pool_options(), get_default_resource()) {}
    explicit synchronized_pool_resource(memory_resource* upstream)
        : synchronized_pool_resource(pool_options(), upstream) {}
    explicit synchronized_pool_resource(const pool_options& opts)
        : synchronized_pool_resource(opts, get_default_resource()) {}

    synchronized_pool_resource(const synchronized_pool_resource&) = delete;
    virtual ~synchronized_pool_resource();

    synchronized_pool_resource& operator=(const synchronized_pool_resource&) = delete;

    void release();
    memory_resource* upstream_resource() const;
    pool_options options() const;

  protected:
    void* do_allocate(size_t bytes, size_t alignment) override;
    void do_deallocate(void* p, size_t bytes, size_t alignment) override;

    bool do_is_equal(const memory_resource& other) const noexcept override;
  };

  class unsynchronized_pool_resource : public memory_resource {
  public:
    unsynchronized_pool_resource(const pool_options& opts, memory_resource* upstream);

    unsynchronized_pool_resource()
        : unsynchronized_pool_resource(pool_options(), get_default_resource()) {}
    explicit unsynchronized_pool_resource(memory_resource* upstream)
        : unsynchronized_pool_resource(pool_options(), upstream) {}
    explicit unsynchronized_pool_resource(const pool_options& opts)
        : unsynchronized_pool_resource(opts, get_default_resource()) {}

    unsynchronized_pool_resource(const unsynchronized_pool_resource&) = delete;
    virtual ~unsynchronized_pool_resource();

    unsynchronized_pool_resource& operator=(const unsynchronized_pool_resource&) = delete;

    void release();
    memory_resource* upstream_resource() const;
    pool_options options() const;

  protected:
    void* do_allocate(size_t bytes, size_t alignment) override;
    void do_deallocate(void* p, size_t bytes, size_t alignment) override;

    bool do_is_equal(const memory_resource& other) const noexcept override;
  };
}
```

#### `pool_options` data members <a id="mem.res.pool.options">[[mem.res.pool.options]]</a>

The members of `pool_options` comprise a set of constructor options for
pool resources. The effect of each option on the pool resource behavior
is described below:

``` cpp
size_t max_blocks_per_chunk;
```

The maximum number of blocks that will be allocated at once from the
upstream memory resource [[mem.res.monotonic.buffer]] to replenish a
pool. If the value of `max_blocks_per_chunk` is zero or is greater than
an *implementation-defined* limit, that limit is used instead. The
implementation may choose to use a smaller value than is specified in
this field and may use different values for different pools.

``` cpp
size_t largest_required_pool_block;
```

The largest allocation size that is required to be fulfilled using the
pooling mechanism. Attempts to allocate a single block larger than this
threshold will be allocated directly from the upstream memory resource.
If `largest_required_pool_block` is zero or is greater than an
*implementation-defined* limit, that limit is used instead. The
implementation may choose a pass-through threshold larger than specified
in this field.

#### Constructors and destructors <a id="mem.res.pool.ctor">[[mem.res.pool.ctor]]</a>

``` cpp
synchronized_pool_resource(const pool_options& opts, memory_resource* upstream);
unsynchronized_pool_resource(const pool_options& opts, memory_resource* upstream);
```

*Preconditions:* `upstream` is the address of a valid memory resource.

*Effects:* Constructs a pool resource object that will obtain memory
from `upstream` whenever the pool resource is unable to satisfy a memory
request from its own internal data structures. The resulting object will
hold a copy of `upstream`, but will not own the resource to which
`upstream` points.

\[*Note 1*: The intention is that calls to `upstream->allocate()` will
be substantially fewer than calls to `this->allocate()` in most
cases. — *end note*\]

The behavior of the pooling mechanism is tuned according to the value of
the `opts` argument.

*Throws:* Nothing unless `upstream->allocate()` throws. It is
unspecified if, or under what conditions, this constructor calls
`upstream->allocate()`.

``` cpp
virtual ~synchronized_pool_resource();
virtual ~unsynchronized_pool_resource();
```

*Effects:* Calls `release()`.

#### Members <a id="mem.res.pool.mem">[[mem.res.pool.mem]]</a>

``` cpp
void release();
```

*Effects:* Calls `upstream_resource()->deallocate()` as necessary to
release all allocated memory.

\[*Note 1*: The memory is released back to `upstream_resource()` even if
`deallocate` has not been called for some of the allocated
blocks. — *end note*\]

``` cpp
memory_resource* upstream_resource() const;
```

*Returns:* The value of the `upstream` argument provided to the
constructor of this object.

``` cpp
pool_options options() const;
```

*Returns:* The options that control the pooling behavior of this
resource. The values in the returned struct may differ from those
supplied to the pool resource constructor in that values of zero will be
replaced with *implementation-defined* defaults, and sizes may be
rounded to unspecified granularity.

``` cpp
void* do_allocate(size_t bytes, size_t alignment) override;
```

*Effects:* If the pool selected for a block of size `bytes` is unable to
satisfy the memory request from its own internal data structures, it
will call `upstream_resource()->allocate()` to obtain more memory. If
`bytes` is larger than that which the largest pool can handle, then
memory will be allocated using `upstream_resource()->allocate()`.

*Returns:* A pointer to allocated
storage [[basic.stc.dynamic.allocation]] with a size of at least
`bytes`. The size and alignment of the allocated memory shall meet the
requirements for a class derived from
`memory_resource`[[mem.res.class]].

*Throws:* Nothing unless `upstream_resource()->allocate()` throws.

``` cpp
void do_deallocate(void* p, size_t bytes, size_t alignment) override;
```

*Effects:* Returns the memory at `p` to the pool. It is unspecified if,
or under what circumstances, this operation will result in a call to
`upstream_resource()->deallocate()`.

*Throws:* Nothing.

``` cpp
bool do_is_equal(const memory_resource& other) const noexcept override;
```

*Returns:* `this == &other`.

### Class `monotonic_buffer_resource` <a id="mem.res.monotonic.buffer">[[mem.res.monotonic.buffer]]</a>

#### General <a id="mem.res.monotonic.buffer.general">[[mem.res.monotonic.buffer.general]]</a>

A `monotonic_buffer_resource` is a special-purpose memory resource
intended for very fast memory allocations in situations where memory is
used to build up a few objects and then is released all at once when the
memory resource object is destroyed.

``` cpp
namespace std::pmr {
  class monotonic_buffer_resource : public memory_resource {
    memory_resource* upstream_rsrc;     // exposition only
    void* current_buffer;               // exposition only
    size_t next_buffer_size;            // exposition only

  public:
    explicit monotonic_buffer_resource(memory_resource* upstream);
    monotonic_buffer_resource(size_t initial_size, memory_resource* upstream);
    monotonic_buffer_resource(void* buffer, size_t buffer_size, memory_resource* upstream);

    monotonic_buffer_resource()
      : monotonic_buffer_resource(get_default_resource()) {}
    explicit monotonic_buffer_resource(size_t initial_size)
      : monotonic_buffer_resource(initial_size, get_default_resource()) {}
    monotonic_buffer_resource(void* buffer, size_t buffer_size)
      : monotonic_buffer_resource(buffer, buffer_size, get_default_resource()) {}

    monotonic_buffer_resource(const monotonic_buffer_resource&) = delete;

    virtual ~monotonic_buffer_resource();

    monotonic_buffer_resource& operator=(const monotonic_buffer_resource&) = delete;

    void release();
    memory_resource* upstream_resource() const;

  protected:
    void* do_allocate(size_t bytes, size_t alignment) override;
    void do_deallocate(void* p, size_t bytes, size_t alignment) override;

    bool do_is_equal(const memory_resource& other) const noexcept override;
  };
}
```

#### Constructors and destructor <a id="mem.res.monotonic.buffer.ctor">[[mem.res.monotonic.buffer.ctor]]</a>

``` cpp
explicit monotonic_buffer_resource(memory_resource* upstream);
monotonic_buffer_resource(size_t initial_size, memory_resource* upstream);
```

*Preconditions:* `upstream` is the address of a valid memory resource.
`initial_size`, if specified, is greater than zero.

*Effects:* Sets `upstream_rsrc` to `upstream` and `current_buffer` to .
If `initial_size` is specified, sets `next_buffer_size` to at least
`initial_size`; otherwise sets `next_buffer_size` to an
*implementation-defined* size.

``` cpp
monotonic_buffer_resource(void* buffer, size_t buffer_size, memory_resource* upstream);
```

*Preconditions:* `upstream` is the address of a valid memory resource.
`buffer_size` is no larger than the number of bytes in `buffer`.

*Effects:* Sets `upstream_rsrc` to `upstream`, `current_buffer` to
`buffer`, and `next_buffer_size` to `buffer_size` (but not less than 1),
then increases `next_buffer_size` by an *implementation-defined* growth
factor (which need not be integral).

``` cpp
~monotonic_buffer_resource();
```

*Effects:* Calls `release()`.

#### Members <a id="mem.res.monotonic.buffer.mem">[[mem.res.monotonic.buffer.mem]]</a>

``` cpp
void release();
```

*Effects:* Calls `upstream_rsrc->deallocate()` as necessary to release
all allocated memory. Resets `current_buffer` and `next_buffer_size` to
their initial values at construction.

\[*Note 1*: The memory is released back to `upstream_rsrc` even if some
blocks that were allocated from have not been deallocated from
. — *end note*\]

``` cpp
memory_resource* upstream_resource() const;
```

*Returns:* The value of `upstream_rsrc`.

``` cpp
void* do_allocate(size_t bytes, size_t alignment) override;
```

*Effects:* If the unused space in `current_buffer` can fit a block with
the specified `bytes` and `alignment`, then allocate the return block
from `current_buffer`; otherwise set `current_buffer` to
`upstream_rsrc->allocate(n, m)`, where `n` is not less than
`max(bytes, next_buffer_size)` and `m` is not less than `alignment`, and
increase `next_buffer_size` by an *implementation-defined* growth factor
(which need not be integral), then allocate the return block from the
newly-allocated `current_buffer`.

*Returns:* A pointer to allocated
storage [[basic.stc.dynamic.allocation]] with a size of at least
`bytes`. The size and alignment of the allocated memory shall meet the
requirements for a class derived from
`memory_resource`[[mem.res.class]].

*Throws:* Nothing unless `upstream_rsrc->allocate()` throws.

``` cpp
void do_deallocate(void* p, size_t bytes, size_t alignment) override;
```

*Effects:* None.

*Throws:* Nothing.

*Remarks:* Memory used by this resource increases monotonically until
its destruction.

``` cpp
bool do_is_equal(const memory_resource& other) const noexcept override;
```

*Returns:* `this == &other`.

## Class template `scoped_allocator_adaptor` <a id="allocator.adaptor">[[allocator.adaptor]]</a>

### Header `<scoped_allocator>` synopsis <a id="allocator.adaptor.syn">[[allocator.adaptor.syn]]</a>

``` cpp
namespace std {
  // class template scoped_allocator_adaptor
  template<class OuterAlloc, class... InnerAlloc>
    class scoped_allocator_adaptor;

  // [scoped.adaptor.operators], scoped allocator operators
  template<class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
}
```

The class template `scoped_allocator_adaptor` is an allocator template
that specifies an allocator resource (the outer allocator) to be used by
a container (as any other allocator does) and also specifies an inner
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
recursions.

\[*Note 1*: The `scoped_allocator_adaptor` is derived from the outer
allocator type so it can be substituted for the outer allocator type in
most expressions. — *end note*\]

``` cpp
namespace std {
  template<class OuterAlloc, class... InnerAllocs>
  class scoped_allocator_adaptor : public OuterAlloc {
  private:
    using OuterTraits = allocator_traits<OuterAlloc>;   // exposition only
    scoped_allocator_adaptor<InnerAllocs...> inner;     // exposition only

  public:
    using outer_allocator_type = OuterAlloc;
    using inner_allocator_type = see below;

    using value_type           = typename OuterTraits::value_type;
    using size_type            = typename OuterTraits::size_type;
    using difference_type      = typename OuterTraits::difference_type;
    using pointer              = typename OuterTraits::pointer;
    using const_pointer        = typename OuterTraits::const_pointer;
    using void_pointer         = typename OuterTraits::void_pointer;
    using const_void_pointer   = typename OuterTraits::const_void_pointer;

    using propagate_on_container_copy_assignment = see below;
    using propagate_on_container_move_assignment = see below;
    using propagate_on_container_swap            = see below;
    using is_always_equal                        = see below;

    template<class Tp> struct rebind {
      using other = scoped_allocator_adaptor<
        OuterTraits::template rebind_alloc<Tp>, InnerAllocs...>;
    };

    scoped_allocator_adaptor();
    template<class OuterA2>
      scoped_allocator_adaptor(OuterA2&& outerAlloc,
                               const InnerAllocs&... innerAllocs) noexcept;

    scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
    scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;

    template<class OuterA2>
      scoped_allocator_adaptor(
        const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& other) noexcept;
    template<class OuterA2>
      scoped_allocator_adaptor(
        scoped_allocator_adaptor<OuterA2, InnerAllocs...>&& other) noexcept;

    scoped_allocator_adaptor& operator=(const scoped_allocator_adaptor&) = default;
    scoped_allocator_adaptor& operator=(scoped_allocator_adaptor&&) = default;

    ~scoped_allocator_adaptor();

    inner_allocator_type& inner_allocator() noexcept;
    const inner_allocator_type& inner_allocator() const noexcept;
    outer_allocator_type& outer_allocator() noexcept;
    const outer_allocator_type& outer_allocator() const noexcept;

    [[nodiscard]] pointer allocate(size_type n);
    [[nodiscard]] pointer allocate(size_type n, const_void_pointer hint);
    void deallocate(pointer p, size_type n);
    size_type max_size() const;

    template<class T, class... Args>
      void construct(T* p, Args&&... args);

    template<class T>
      void destroy(T* p);

    scoped_allocator_adaptor select_on_container_copy_construction() const;
  };

  template<class OuterAlloc, class... InnerAllocs>
    scoped_allocator_adaptor(OuterAlloc, InnerAllocs...)
      -> scoped_allocator_adaptor<OuterAlloc, InnerAllocs...>;
}
```

### Member types <a id="allocator.adaptor.types">[[allocator.adaptor.types]]</a>

``` cpp
using inner_allocator_type = see below;
```

*Type:* `scoped_allocator_adaptor<OuterAlloc>` if
`sizeof...(InnerAllocs)` is zero; otherwise,  
`scoped_allocator_adaptor<InnerAllocs...>`.

``` cpp
using propagate_on_container_copy_assignment = see below;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_copy_assignment::value` is
`true` for any `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

``` cpp
using propagate_on_container_move_assignment = see below;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_move_assignment::value` is
`true` for any `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

``` cpp
using propagate_on_container_swap = see below;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_swap::value` is `true` for
any `A` in the set of `OuterAlloc` and `InnerAllocs...`; otherwise,
`false_type`.

``` cpp
using is_always_equal = see below;
```

*Type:* `true_type` if `allocator_traits<A>::is_always_equal::value` is
`true` for every `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

### Constructors <a id="allocator.adaptor.cnstr">[[allocator.adaptor.cnstr]]</a>

``` cpp
scoped_allocator_adaptor();
```

*Effects:* Value-initializes the `OuterAlloc` base class and the `inner`
allocator object.

``` cpp
template<class OuterA2>
  scoped_allocator_adaptor(OuterA2&& outerAlloc, const InnerAllocs&... innerAllocs) noexcept;
```

*Constraints:* `is_constructible_v<OuterAlloc, OuterA2>` is `true`.

*Effects:* Initializes the `OuterAlloc` base class with
`std::forward<OuterA2>(outerAlloc)` and `inner` with `innerAllocs...`
(hence recursively initializing each allocator within the adaptor with
the corresponding allocator from the argument list).

``` cpp
scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
```

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;
```

*Effects:* Move constructs each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
template<class OuterA2>
  scoped_allocator_adaptor(
    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& other) noexcept;
```

*Constraints:* `is_constructible_v<OuterAlloc, const OuterA2&>` is
`true`.

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
template<class OuterA2>
  scoped_allocator_adaptor(scoped_allocator_adaptor<OuterA2, InnerAllocs...>&& other) noexcept;
```

*Constraints:* `is_constructible_v<OuterAlloc, OuterA2>` is `true`.

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator rvalue from `other`.

### Members <a id="allocator.adaptor.members">[[allocator.adaptor.members]]</a>

In the `construct` member functions, `OUTERMOST(x)` is
`OUTERMOST(x.outer_allocator())` if the expression `x.outer_allocator()`
is valid  [[temp.deduct]] and `x` otherwise; `OUTERMOST_ALLOC_TRAITS(x)`
is `allocator_traits<remove_reference_t<decltype(OUTERMOST(x))>>`.

\[*Note 1*: `OUTERMOST(x)` and `OUTERMOST_ALLOC_TRAITS(x)` are recursive
operations. It is incumbent upon the definition of `outer_allocator()`
to ensure that the recursion terminates. It will terminate for all
instantiations of `scoped_allocator_adaptor`. — *end note*\]

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
[[nodiscard]] pointer allocate(size_type n);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n)`.

``` cpp
[[nodiscard]] pointer allocate(size_type n, const_void_pointer hint);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n, hint)`.

``` cpp
void deallocate(pointer p, size_type n) noexcept;
```

*Effects:* As if by:
`allocator_traits<OuterAlloc>::deallocate(outer_allocator(), p, n);`

``` cpp
size_type max_size() const;
```

*Returns:* `allocator_traits<OuterAlloc>::max_size(outer_allocator())`.

``` cpp
template<class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
apply([p, this](auto&&... newargs) {
        OUTERMOST_ALLOC_TRAITS(*this)::construct(
          OUTERMOST(*this), p,
          std::forward<decltype(newargs)>(newargs)...);
      },
      uses_allocator_construction_args<T>(inner_allocator(),
                                          std::forward<Args>(args)...));
```

``` cpp
template<class T>
  void destroy(T* p);
```

*Effects:* Calls
*OUTERMOST_ALLOC_TRAITS*(\*this)::destroy(*OUTERMOST*(\*this), p).

``` cpp
scoped_allocator_adaptor select_on_container_copy_construction() const;
```

*Returns:* A new `scoped_allocator_adaptor` object where each allocator
`a1` within the adaptor is initialized with
`allocator_traits<A1>::select_on_container_copy_construction(a2)`, where
`A1` is the type of `a1` and `a2` is the corresponding allocator in
`*this`.

### Operators <a id="scoped.adaptor.operators">[[scoped.adaptor.operators]]</a>

``` cpp
template<class OuterA1, class OuterA2, class... InnerAllocs>
  bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                  const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

*Returns:* If `sizeof...(InnerAllocs)` is zero,

``` cpp
a.outer_allocator() == b.outer_allocator()
```

otherwise

``` cpp
a.outer_allocator() == b.outer_allocator() && a.inner_allocator() == b.inner_allocator()
```

<!-- Section link definitions -->
[allocator.adaptor]: #allocator.adaptor
[allocator.adaptor.cnstr]: #allocator.adaptor.cnstr
[allocator.adaptor.members]: #allocator.adaptor.members
[allocator.adaptor.syn]: #allocator.adaptor.syn
[allocator.adaptor.types]: #allocator.adaptor.types
[allocator.globals]: #allocator.globals
[allocator.members]: #allocator.members
[allocator.tag]: #allocator.tag
[allocator.traits]: #allocator.traits
[allocator.traits.general]: #allocator.traits.general
[allocator.traits.members]: #allocator.traits.members
[allocator.traits.other]: #allocator.traits.other
[allocator.traits.types]: #allocator.traits.types
[allocator.uses]: #allocator.uses
[allocator.uses.construction]: #allocator.uses.construction
[allocator.uses.trait]: #allocator.uses.trait
[c.malloc]: #c.malloc
[default.allocator]: #default.allocator
[default.allocator.general]: #default.allocator.general
[inout.ptr]: #inout.ptr
[inout.ptr.t]: #inout.ptr.t
[mem]: #mem
[mem.general]: #mem.general
[mem.poly.allocator.class]: #mem.poly.allocator.class
[mem.poly.allocator.class.general]: #mem.poly.allocator.class.general
[mem.poly.allocator.ctor]: #mem.poly.allocator.ctor
[mem.poly.allocator.eq]: #mem.poly.allocator.eq
[mem.poly.allocator.mem]: #mem.poly.allocator.mem
[mem.res]: #mem.res
[mem.res.class]: #mem.res.class
[mem.res.class.general]: #mem.res.class.general
[mem.res.eq]: #mem.res.eq
[mem.res.global]: #mem.res.global
[mem.res.monotonic.buffer]: #mem.res.monotonic.buffer
[mem.res.monotonic.buffer.ctor]: #mem.res.monotonic.buffer.ctor
[mem.res.monotonic.buffer.general]: #mem.res.monotonic.buffer.general
[mem.res.monotonic.buffer.mem]: #mem.res.monotonic.buffer.mem
[mem.res.pool]: #mem.res.pool
[mem.res.pool.ctor]: #mem.res.pool.ctor
[mem.res.pool.mem]: #mem.res.pool.mem
[mem.res.pool.options]: #mem.res.pool.options
[mem.res.pool.overview]: #mem.res.pool.overview
[mem.res.private]: #mem.res.private
[mem.res.public]: #mem.res.public
[mem.res.syn]: #mem.res.syn
[memory]: #memory
[memory.general]: #memory.general
[memory.syn]: #memory.syn
[obj.lifetime]: #obj.lifetime
[out.ptr]: #out.ptr
[out.ptr.t]: #out.ptr.t
[pointer.conversion]: #pointer.conversion
[pointer.traits]: #pointer.traits
[pointer.traits.functions]: #pointer.traits.functions
[pointer.traits.general]: #pointer.traits.general
[pointer.traits.optmem]: #pointer.traits.optmem
[pointer.traits.types]: #pointer.traits.types
[ptr.align]: #ptr.align
[scoped.adaptor.operators]: #scoped.adaptor.operators
[smartptr]: #smartptr
[smartptr.adapt]: #smartptr.adapt
[specialized.addressof]: #specialized.addressof
[unique.ptr]: #unique.ptr
[unique.ptr.create]: #unique.ptr.create
[unique.ptr.dltr]: #unique.ptr.dltr
[unique.ptr.dltr.dflt]: #unique.ptr.dltr.dflt
[unique.ptr.dltr.dflt1]: #unique.ptr.dltr.dflt1
[unique.ptr.dltr.general]: #unique.ptr.dltr.general
[unique.ptr.general]: #unique.ptr.general
[unique.ptr.io]: #unique.ptr.io
[unique.ptr.runtime]: #unique.ptr.runtime
[unique.ptr.runtime.asgn]: #unique.ptr.runtime.asgn
[unique.ptr.runtime.ctor]: #unique.ptr.runtime.ctor
[unique.ptr.runtime.general]: #unique.ptr.runtime.general
[unique.ptr.runtime.modifiers]: #unique.ptr.runtime.modifiers
[unique.ptr.runtime.observers]: #unique.ptr.runtime.observers
[unique.ptr.single]: #unique.ptr.single
[unique.ptr.single.asgn]: #unique.ptr.single.asgn
[unique.ptr.single.ctor]: #unique.ptr.single.ctor
[unique.ptr.single.dtor]: #unique.ptr.single.dtor
[unique.ptr.single.general]: #unique.ptr.single.general
[unique.ptr.single.modifiers]: #unique.ptr.single.modifiers
[unique.ptr.single.observers]: #unique.ptr.single.observers
[unique.ptr.special]: #unique.ptr.special
[util.sharedptr]: #util.sharedptr
[util.smartptr.enab]: #util.smartptr.enab
[util.smartptr.getdeleter]: #util.smartptr.getdeleter
[util.smartptr.hash]: #util.smartptr.hash
[util.smartptr.ownerless]: #util.smartptr.ownerless
[util.smartptr.shared]: #util.smartptr.shared
[util.smartptr.shared.assign]: #util.smartptr.shared.assign
[util.smartptr.shared.cast]: #util.smartptr.shared.cast
[util.smartptr.shared.cmp]: #util.smartptr.shared.cmp
[util.smartptr.shared.const]: #util.smartptr.shared.const
[util.smartptr.shared.create]: #util.smartptr.shared.create
[util.smartptr.shared.dest]: #util.smartptr.shared.dest
[util.smartptr.shared.general]: #util.smartptr.shared.general
[util.smartptr.shared.io]: #util.smartptr.shared.io
[util.smartptr.shared.mod]: #util.smartptr.shared.mod
[util.smartptr.shared.obs]: #util.smartptr.shared.obs
[util.smartptr.shared.spec]: #util.smartptr.shared.spec
[util.smartptr.weak]: #util.smartptr.weak
[util.smartptr.weak.assign]: #util.smartptr.weak.assign
[util.smartptr.weak.bad]: #util.smartptr.weak.bad
[util.smartptr.weak.const]: #util.smartptr.weak.const
[util.smartptr.weak.dest]: #util.smartptr.weak.dest
[util.smartptr.weak.general]: #util.smartptr.weak.general
[util.smartptr.weak.mod]: #util.smartptr.weak.mod
[util.smartptr.weak.obs]: #util.smartptr.weak.obs
[util.smartptr.weak.spec]: #util.smartptr.weak.spec

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[allocator.requirements.completeness]: library.md#allocator.requirements.completeness
[allocator.requirements.general]: library.md#allocator.requirements.general
[allocator.uses.construction]: #allocator.uses.construction
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.types.general]: basic.md#basic.types.general
[bit.cast]: utilities.md#bit.cast
[conv.qual]: expr.md#conv.qual
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[cpp17.moveassignable]: #cpp17.moveassignable
[cpp17.moveconstructible]: #cpp17.moveconstructible
[cpp17.nullablepointer]: #cpp17.nullablepointer
[defns.const.subexpr]: #defns.const.subexpr
[expr.eq]: expr.md#expr.eq
[function.objects]: utilities.md#function.objects
[intro.multithread]: basic.md#intro.multithread
[intro.object]: basic.md#intro.object
[intro.races]: basic.md#intro.races
[mem.res.class]: #mem.res.class
[mem.res.monotonic.buffer]: #mem.res.monotonic.buffer
[mem.summary]: #mem.summary
[memory]: #memory
[memory.general]: #memory.general
[meta.rqmts]: meta.md#meta.rqmts
[new.delete]: support.md#new.delete
[pointer.conversion]: #pointer.conversion
[pointer.traits]: #pointer.traits
[pointer.traits.functions]: #pointer.traits.functions
[pointer.traits.optmem]: #pointer.traits.optmem
[smartptr]: #smartptr
[specialized.addressof]: #specialized.addressof
[specialized.algorithms]: algorithms.md#specialized.algorithms
[stmt.dcl]: stmt.md#stmt.dcl
[swappable.requirements]: library.md#swappable.requirements
[temp.deduct]: temp.md#temp.deduct
[term.incomplete.type]: #term.incomplete.type
[tuple]: utilities.md#tuple
[unique.ptr]: #unique.ptr
[unord.hash]: utilities.md#unord.hash
[util.smartptr.enab]: #util.smartptr.enab
[util.smartptr.shared.mod]: #util.smartptr.shared.mod

<!-- Link reference definitions -->
[allocator.adaptor]: #allocator.adaptor
[mem.res]: #mem.res
[memory]: #memory
[smartptr]: #smartptr
