# Language support library <a id="support">[[support]]</a>

## General <a id="support.general">[[support.general]]</a>

This Clause describes the function signatures that are called
implicitly, and the types of objects generated implicitly, during the
execution of some C++ programs. It also describes the headers that
declare these function signatures and define any related types.

The following subclauses describe common type definitions used
throughout the library, characteristics of the predefined types,
functions supporting start and termination of a C++ program, support for
dynamic memory management, support for dynamic type identification,
support for exception processing, support for initializer lists, and
other runtime support, as summarized in [[support.summary]].

**Table: Language support library summary**

| Subclause               |                           | Header                                             |
| ----------------------- | ------------------------- | -------------------------------------------------- |
| [[support.types]]       | Common definitions        | `<cstddef>`, `<cstdlib>`                           |
| [[support.limits]]      | Implementation properties | `<cfloat>`, `<climits>`, `<limits>`, `<version>`   |
| [[support.arith.types]] | Arithmetic types          | `<cstdint>`, `<stdfloat>`                          |
| [[support.start.term]]  | Start and termination     | `<cstdlib>`                                        |
| [[support.dynamic]]     | Dynamic memory management | `<new>`                                            |
| [[support.rtti]]        | Type identification       | `<typeinfo>`                                       |
| [[support.srcloc]]      | Source location           | `<source_location>`                                |
| [[support.exception]]   | Exception handling        | `<exception>`                                      |
| [[support.initlist]]    | Initializer lists         | `<initializer_list>`                               |
| [[cmp]]                 | Comparisons               | `<compare>`                                        |
| [[support.coroutine]]   | Coroutines                | `<coroutine>`                                      |
| [[support.runtime]]     | Other runtime support     | `<csetjmp>`, `<csignal>`, `<cstdarg>`, `<cstdlib>` |


## Common definitions <a id="support.types">[[support.types]]</a>

### Header `<cstddef>` synopsis <a id="cstddef.syn">[[cstddef.syn]]</a>

``` cpp
// all freestanding
namespace std {
  using ptrdiff_t = see below;
  using size_t = see below;
  using max_align_t = see below;
  using nullptr_t = decltype(nullptr);

  enum class byte : unsigned char {};

  // [support.types.byteops], byte type operations
  template<class IntType>
    constexpr byte& operator<<=(byte& b, IntType shift) noexcept;
  template<class IntType>
    constexpr byte operator<<(byte b, IntType shift) noexcept;
  template<class IntType>
    constexpr byte& operator>>=(byte& b, IntType shift) noexcept;
  template<class IntType>
    constexpr byte operator>>(byte b, IntType shift) noexcept;
  constexpr byte& operator|=(byte& l, byte r) noexcept;
  constexpr byte operator|(byte l, byte r) noexcept;
  constexpr byte& operator&=(byte& l, byte r) noexcept;
  constexpr byte operator&(byte l, byte r) noexcept;
  constexpr byte& operator^=(byte& l, byte r) noexcept;
  constexpr byte operator^(byte l, byte r) noexcept;
  constexpr byte operator~(byte b) noexcept;
  template<class IntType>
    constexpr IntType to_integer(byte b) noexcept;
}

#define NULL see below
#define offsetof(P, D) see below
```

The contents and meaning of the header `<cstddef>` are the same as the C
standard library header `<stddef.h>`, except that it does not declare
the type `wchar_t`, that it also declares the type `byte` and its
associated operations [[support.types.byteops]], and as noted in
[[support.types.nullptr]] and [[support.types.layout]].

### Header `<cstdlib>` synopsis <a id="cstdlib.syn">[[cstdlib.syn]]</a>

``` cpp
namespace std {
  using size_t = see below;                                             // freestanding
  using div_t = see below;
  using ldiv_t = see below;
  using lldiv_t = see below;
}

#define NULL see below                                                  // freestanding
#define EXIT_FAILURE see below
#define EXIT_SUCCESS see below
#define RAND_MAX see below
#define MB_CUR_MAX see below

namespace std {
  // Exposition-only function type aliases
  extern "C" using c-atexit-handler = void();                           // exposition only
  extern "C++" using atexit-handler = void();                           // exposition only
  extern "C" using c-compare-pred = int(const void*, const void*);      // exposition only
  extern "C++" using compare-pred = int(const void*, const void*);      // exposition only

  // [support.start.term], start and termination
  [[noreturn]] void abort() noexcept;                                   // freestanding
  int atexit(c-atexit-handler* func) noexcept;                          // freestanding
  int atexit(atexit-handler* func) noexcept;                            // freestanding
  int at_quick_exit(c-atexit-handler* func) noexcept;                   // freestanding
  int at_quick_exit(atexit-handler* func) noexcept;                     // freestanding
  [[noreturn]] void exit(int status);                                   // freestanding
  [[noreturn]] void _Exit(int status) noexcept;                         // freestanding
  [[noreturn]] void quick_exit(int status) noexcept;                    // freestanding

  char* getenv(const char* name);
  int system(const char* string);

  // [c.malloc], C library memory allocation
  void* aligned_alloc(size_t alignment, size_t size);
  void* calloc(size_t nmemb, size_t size);
  void free(void* ptr);
  void* malloc(size_t size);
  void* realloc(void* ptr, size_t size);

  double atof(const char* nptr);
  int atoi(const char* nptr);
  long int atol(const char* nptr);
  long long int atoll(const char* nptr);
  double strtod(const char* nptr, char** endptr);
  float strtof(const char* nptr, char** endptr);
  long double strtold(const char* nptr, char** endptr);
  long int strtol(const char* nptr, char** endptr, int base);
  long long int strtoll(const char* nptr, char** endptr, int base);
  unsigned long int strtoul(const char* nptr, char** endptr, int base);
  unsigned long long int strtoull(const char* nptr, char** endptr, int base);

  // [c.mb.wcs], multibyte / wide string and character conversion functions
  int mblen(const char* s, size_t n);
  int mbtowc(wchar_t* pwc, const char* s, size_t n);
  int wctomb(char* s, wchar_t wchar);
  size_t mbstowcs(wchar_t* pwcs, const char* s, size_t n);
  size_t wcstombs(char* s, const wchar_t* pwcs, size_t n);

  // [alg.c.library], C standard library algorithms
  void* bsearch(const void* key, const void* base, size_t nmemb, size_t size,
                c-compare-pred*\itcorr[-1] compar);
  void* bsearch(const void* key, const void* base, size_t nmemb, size_t size,
                compare-pred*\itcorr[-1] compar);
  void qsort(void* base, size_t nmemb, size_t size, c-compare-pred*\itcorr[-1] compar);
  void qsort(void* base, size_t nmemb, size_t size, compare-pred*\itcorr[-1] compar);

  // [c.math.rand], low-quality random number generation
  int rand();
  void srand(unsigned int seed);

  // [c.math.abs], absolute values
  constexpr int abs(int j);
  constexpr long int abs(long int j);
  constexpr long long int abs(long long int j);
  constexpr floating-point-type abs(floating-point-type j);

  constexpr long int labs(long int j);
  constexpr long long int llabs(long long int j);

  constexpr div_t div(int numer, int denom);
  constexpr ldiv_t div(long int numer, long int denom);                 // see [library.c]
  constexpr lldiv_t div(long long int numer, long long int denom);      // see [library.c]
  constexpr ldiv_t ldiv(long int numer, long int denom);
  constexpr lldiv_t lldiv(long long int numer, long long int denom);
}
```

The contents and meaning of the header `<cstdlib>` are the same as the C
standard library header `<stdlib.h>`, except that it does not declare
the type `wchar_t`, and except as noted in [[support.types.nullptr]],
[[support.types.layout]], [[support.start.term]], [[c.malloc]],
[[c.mb.wcs]], [[alg.c.library]], [[c.math.rand]], and [[c.math.abs]].

\[*Note 1*: Several functions have additional overloads in this
document, but they have the same behavior as in the C standard library
[[library.c]]. — *end note*\]

### Null pointers <a id="support.types.nullptr">[[support.types.nullptr]]</a>

The type `nullptr_t` is a synonym for the type of a `nullptr`
expression, and it has the characteristics described in 
[[basic.fundamental]] and  [[conv.ptr]].

\[*Note 1*: Although `nullptr`’s address cannot be taken, the address of
another `nullptr_t` object that is an lvalue can be
taken. — *end note*\]

The macro `NULL` is an *implementation-defined* null pointer
constant.[^1]

### Sizes, alignments, and offsets <a id="support.types.layout">[[support.types.layout]]</a>

The macro `offsetof(type, member-designator)` has the same semantics as
the corresponding macro in the C standard library header `<stddef.h>`,
but accepts a restricted set of `type` arguments in this document. Use
of the `offsetof` macro with a `type` other than a standard-layout class
[[class.prop]] is conditionally-supported.[^2]

The expression `offsetof(type, member-designator)` is never
type-dependent [[temp.dep.expr]] and it is value-dependent
[[temp.dep.constexpr]] if and only if `type` is dependent. The result of
applying the `offsetof` macro to a static data member or a function
member is undefined. No operation invoked by the `offsetof` macro shall
throw an exception and `noexcept(offsetof(type, member-designator))`
shall be `true`.

The type `ptrdiff_t` is an *implementation-defined* signed integer type
that can hold the difference of two subscripts in an array object, as
described in  [[expr.add]].

The type `size_t` is an *implementation-defined* unsigned integer type
that is large enough to contain the size in bytes of any object
[[expr.sizeof]].

*Recommended practice:* An implementation should choose types for
`ptrdiff_t` and `size_t` whose integer conversion ranks [[conv.rank]]
are no greater than that of `signed long int` unless a larger size is
necessary to contain all the possible values.

The type `max_align_t` is a trivial standard-layout type whose alignment
requirement is at least as great as that of every scalar type, and whose
alignment requirement is supported in every context [[basic.align]].

### `byte` type operations <a id="support.types.byteops">[[support.types.byteops]]</a>

``` cpp
template<class IntType>
  constexpr byte& operator<<=(byte& b, IntType shift) noexcept;
```

*Constraints:* `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to: `return b = b << shift;`

``` cpp
template<class IntType>
  constexpr byte operator<<(byte b, IntType shift) noexcept;
```

*Constraints:* `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to:

``` cpp
return static_cast<byte>(static_cast<unsigned int>(b) << shift);
```

``` cpp
template<class IntType>
  constexpr byte& operator>>=(byte& b, IntType shift) noexcept;
```

*Constraints:* `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to: `return b = b >> shift;`

``` cpp
template<class IntType>
  constexpr byte operator>>(byte b, IntType shift) noexcept;
```

*Constraints:* `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to:

``` cpp
return static_cast<byte>(static_cast<unsigned int>(b) >> shift);
```

``` cpp
constexpr byte& operator|=(byte& l, byte r) noexcept;
```

*Effects:* Equivalent to: `return l = l | r;`

``` cpp
constexpr byte operator|(byte l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return static_cast<byte>(static_cast<unsigned int>(l) | static_cast<unsigned int>(r));
```

``` cpp
constexpr byte& operator&=(byte& l, byte r) noexcept;
```

*Effects:* Equivalent to: `return l = l & r;`

``` cpp
constexpr byte operator&(byte l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return static_cast<byte>(static_cast<unsigned int>(l) & static_cast<unsigned int>(r));
```

\indexlibrarymember{operator^=}{byte}

``` cpp
constexpr byte& operator^=(byte& l, byte r) noexcept;
```

*Effects:* Equivalent to: `return l = l `^` r;`

\indexlibrarymember{operator^}{byte}

``` cpp
constexpr byte operator^(byte l, byte r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return static_cast<byte>(static_cast<unsigned int>(l) ^ static_cast<unsigned int>(r));
```

``` cpp
constexpr byte operator~(byte b) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return static_cast<byte>(~static_cast<unsigned int>(b));
```

``` cpp
template<class IntType>
  constexpr IntType to_integer(byte b) noexcept;
```

*Constraints:* `is_integral_v<IntType>` is `true`.

*Effects:* Equivalent to: `return static_cast<IntType>(b);`

## Implementation properties <a id="support.limits">[[support.limits]]</a>

### General <a id="support.limits.general">[[support.limits.general]]</a>

The headers `<limits>`, `<climits>`, and `<cfloat>` supply
characteristics of implementation-dependent arithmetic types
[[basic.fundamental]].

### Header `<version>` synopsis <a id="version.syn">[[version.syn]]</a>

The header `<version>` supplies implementation-dependent information
about the C++ standard library (e.g., version number and release date).

Each of the macros defined in `<version>` is also defined after
inclusion of any member of the set of library headers indicated in the
corresponding comment in this synopsis.

\[*Note 1*: Future revisions of C++ might replace the values of these
macros with greater values. — *end note*\]

``` cpp
#define __cpp_lib_addressof_constexpr               201603L // also in <memory>
#define __cpp_lib_algorithm_iterator_requirements   202207L
  // also in <algorithm>, <numeric>, <memory>
#define __cpp_lib_allocate_at_least                 202302L // also in <memory>
#define __cpp_lib_allocator_traits_is_always_equal  201411L
  // also in <memory>, <scoped_allocator>, <string>, <deque>, <forward_list>, <list>, <vector>,
  // <map>, <set>, <unordered_map>, <unordered_set>
#define __cpp_lib_adaptor_iterator_pair_constructor 202106L // also in <stack>, <queue>
#define __cpp_lib_any                               201606L // also in <any>
#define __cpp_lib_apply                             201603L // also in <tuple>
#define __cpp_lib_array_constexpr                   201811L // also in <iterator>, <array>
#define __cpp_lib_as_const                          201510L // also in <utility>
#define __cpp_lib_associative_heterogeneous_erasure 202110L
  // also in <map>, <set>, <unordered_map>, <unordered_set>
#define __cpp_lib_assume_aligned                    201811L // also in <memory>
#define __cpp_lib_atomic_flag_test                  201907L // also in <atomic>
#define __cpp_lib_atomic_float                      201711L // also in <atomic>
#define __cpp_lib_atomic_is_always_lock_free        201603L // also in <atomic>
#define __cpp_lib_atomic_lock_free_type_aliases     201907L // also in <atomic>
#define __cpp_lib_atomic_ref                        201806L // also in <atomic>
#define __cpp_lib_atomic_shared_ptr                 201711L // also in <memory>
#define __cpp_lib_atomic_value_initialization       201911L // also in <atomic>, <memory>
#define __cpp_lib_atomic_wait                       201907L // also in <atomic>
#define __cpp_lib_barrier                           202302L // also in <barrier>
#define __cpp_lib_bind_back                         202202L // also in <functional>
#define __cpp_lib_bind_front                        201907L // also in <functional>
#define __cpp_lib_bit_cast                          201806L // also in <bit>
#define __cpp_lib_bitops                            201907L // also in <bit>
#define __cpp_lib_bool_constant                     201505L // also in <type_traits>
#define __cpp_lib_bounded_array_traits              201902L // also in <type_traits>
#define __cpp_lib_boyer_moore_searcher              201603L // also in <functional>
#define __cpp_lib_byte                              201603L // also in <cstddef>
#define __cpp_lib_byteswap                          202110L // also in <bit>
#define __cpp_lib_char8_t                           201907L
  // also in <atomic>, <filesystem>, <istream>, <limits>, <locale>, <ostream>, <string>, <string_view>
#define __cpp_lib_chrono                            201907L // also in <chrono>
#define __cpp_lib_chrono_udls                       201304L // also in <chrono>
#define __cpp_lib_clamp                             201603L // also in <algorithm>
#define __cpp_lib_common_reference                  202302L // also in <type_traits>
#define __cpp_lib_common_reference_wrapper          202302L // also in <functional>
#define __cpp_lib_complex_udls                      201309L // also in <complex>
#define __cpp_lib_concepts                          202207L // also in <concepts>, <compare>
#define __cpp_lib_constexpr_algorithms              201806L // also in <algorithm>, <utility>
#define __cpp_lib_constexpr_bitset                  202207L // also in <bitset>
#define __cpp_lib_constexpr_charconv                202207L // also in <charconv>
#define __cpp_lib_constexpr_cmath                   202202L // also in <cmath>, <cstdlib>
#define __cpp_lib_constexpr_complex                 201711L // also in <complex>
#define __cpp_lib_constexpr_dynamic_alloc           201907L // also in <memory>
#define __cpp_lib_constexpr_functional              201907L // also in <functional>
#define __cpp_lib_constexpr_iterator                201811L // also in <iterator>
#define __cpp_lib_constexpr_memory                  202202L // also in <memory>
#define __cpp_lib_constexpr_numeric                 201911L // also in <numeric>
#define __cpp_lib_constexpr_string                  201907L // also in <string>
#define __cpp_lib_constexpr_string_view             201811L // also in <string_view>
#define __cpp_lib_constexpr_tuple                   201811L // also in <tuple>
#define __cpp_lib_constexpr_typeinfo                202106L // also in <typeinfo>
#define __cpp_lib_constexpr_utility                 201811L // also in <utility>
#define __cpp_lib_constexpr_vector                  201907L // also in <vector>
#define __cpp_lib_containers_ranges                 202202L
  // also in <vector>, <list>, <forward_list>, <map>, <set>, <unordered_map>, <unordered_set>,
  // <deque>, <queue>, <stack>, <string>
#define __cpp_lib_coroutine                         201902L // also in <coroutine>
#define __cpp_lib_destroying_delete                 201806L // also in <new>
#define __cpp_lib_enable_shared_from_this           201603L // also in <memory>
#define __cpp_lib_endian                            201907L // also in <bit>
#define __cpp_lib_erase_if                          202002L
  // also in <string>, <deque>, <forward_list>, <list>, <vector>, <map>, <set>, <unordered_map>,
  // <unordered_set>
#define __cpp_lib_exchange_function                 201304L // also in <utility>
#define __cpp_lib_execution                         201902L // also in <execution>
#define __cpp_lib_expected                          202211L // also in <expected>
#define __cpp_lib_filesystem                        201703L // also in <filesystem>
#define __cpp_lib_flat_map                          202207L // also in <flat_map>
#define __cpp_lib_flat_set                          202207L // also in <flat_set>
#define __cpp_lib_format                            202207L // also in <format>
#define __cpp_lib_format_ranges                     202207L // also in <format>
#define __cpp_lib_formatters                        202302L // also in <stacktrace>, <thread>
#define __cpp_lib_forward_like                      202207L // also in <utility>
#define __cpp_lib_gcd_lcm                           201606L // also in <numeric>
#define __cpp_lib_generator                         202207L // also in <generator>
#define __cpp_lib_generic_associative_lookup        201304L // also in <map>, <set>
#define __cpp_lib_generic_unordered_lookup          201811L
  // also in <unordered_map>, <unordered_set>
#define __cpp_lib_hardware_interference_size        201703L // also in <new>
#define __cpp_lib_has_unique_object_representations 201606L // also in <type_traits>
#define __cpp_lib_hypot                             201603L // also in <cmath>
#define __cpp_lib_incomplete_container_elements     201505L
  // also in <forward_list>, <list>, <vector>
#define __cpp_lib_int_pow2                          202002L // also in <bit>
#define __cpp_lib_integer_comparison_functions      202002L // also in <utility>
#define __cpp_lib_integer_sequence                  201304L // also in <utility>
#define __cpp_lib_integral_constant_callable        201304L // also in <type_traits>
#define __cpp_lib_interpolate                       201902L // also in <cmath>, <numeric>
#define __cpp_lib_invoke                            201411L // also in <functional>
#define __cpp_lib_invoke_r                          202106L // also in <functional>
#define __cpp_lib_ios_noreplace                     202207L // also in <ios>
#define __cpp_lib_is_aggregate                      201703L // also in <type_traits>
#define __cpp_lib_is_constant_evaluated             201811L // also in <type_traits>
#define __cpp_lib_is_final                          201402L // also in <type_traits>
#define __cpp_lib_is_implicit_lifetime              202302L // also in <type_traits>
#define __cpp_lib_is_invocable                      201703L // also in <type_traits>
#define __cpp_lib_is_layout_compatible              201907L // also in <type_traits>
#define __cpp_lib_is_nothrow_convertible            201806L // also in <type_traits>
#define __cpp_lib_is_null_pointer                   201309L // also in <type_traits>
#define __cpp_lib_is_pointer_interconvertible       201907L // also in <type_traits>
#define __cpp_lib_is_scoped_enum                    202011L // also in <type_traits>
#define __cpp_lib_is_swappable                      201603L // also in <type_traits>
#define __cpp_lib_jthread                           201911L // also in <stop_token>, <thread>
#define __cpp_lib_latch                             201907L // also in <latch>
#define __cpp_lib_launder                           201606L // also in <new>
#define __cpp_lib_list_remove_return_type           201806L // also in <forward_list>, <list>
#define __cpp_lib_logical_traits                    201510L // also in <type_traits>
#define __cpp_lib_make_from_tuple                   201606L // also in <tuple>
#define __cpp_lib_make_reverse_iterator             201402L // also in <iterator>
#define __cpp_lib_make_unique                       201304L // also in <memory>
#define __cpp_lib_map_try_emplace                   201411L // also in <map>
#define __cpp_lib_math_constants                    201907L // also in <numbers>
#define __cpp_lib_math_special_functions            201603L // also in <cmath>
#define __cpp_lib_mdspan                            202207L // also in <mdspan>
#define __cpp_lib_memory_resource                   201603L // also in <memory_resource>
#define __cpp_lib_modules                           202207L
#define __cpp_lib_move_iterator_concept             202207L // also in <iterator>
#define __cpp_lib_move_only_function                202110L // also in <functional>
#define __cpp_lib_node_extract                      201606L
  // also in <map>, <set>, <unordered_map>, <unordered_set>
#define __cpp_lib_nonmember_container_access        201411L
  // also in <array>, <deque>, <forward_list>, <iterator>, <list>, <map>, <regex>, <set>, <string>,
  // <unordered_map>, <unordered_set>, <vector>
#define __cpp_lib_not_fn                            201603L // also in <functional>
#define __cpp_lib_null_iterators                    201304L // also in <iterator>
#define __cpp_lib_optional                          202110L // also in <optional>
#define __cpp_lib_out_ptr                           202106L // also in <memory>
#define __cpp_lib_parallel_algorithm                201603L // also in <algorithm>, <numeric>
#define __cpp_lib_polymorphic_allocator             201902L // also in <memory_resource>
#define __cpp_lib_print                             202207L // also in <print>, <ostream>
#define __cpp_lib_quoted_string_io                  201304L // also in <iomanip>
#define __cpp_lib_ranges                            202302L
  // also in <algorithm>, <functional>, <iterator>, <memory>, <ranges>
#define __cpp_lib_ranges_as_const                   202207L // also in <ranges>
#define __cpp_lib_ranges_as_rvalue                  202207L // also in <ranges>
#define __cpp_lib_ranges_cartesian_product          202207L // also in <ranges>
#define __cpp_lib_ranges_chunk                      202202L // also in <ranges>
#define __cpp_lib_ranges_chunk_by                   202202L // also in <ranges>
#define __cpp_lib_ranges_contains                   202207L // also in <algorithm>
#define __cpp_lib_ranges_enumerate                  202302L // also in <ranges>, <version>
#define __cpp_lib_ranges_find_last                  202207L // also in <algorithm>
#define __cpp_lib_ranges_fold                       202207L // also in <algorithm>
#define __cpp_lib_ranges_iota                       202202L // also in <numeric>
#define __cpp_lib_ranges_join_with                  202202L // also in <ranges>
#define __cpp_lib_ranges_repeat                     202207L // also in <ranges>
#define __cpp_lib_ranges_slide                      202202L // also in <ranges>
#define __cpp_lib_ranges_starts_ends_with           202106L // also in <algorithm>
#define __cpp_lib_ranges_stride                     202207L // also in <ranges>
#define __cpp_lib_ranges_to_container               202202L // also in <ranges>
#define __cpp_lib_ranges_zip                        202110L // also in <ranges>, <tuple>, <utility>
#define __cpp_lib_raw_memory_algorithms             201606L // also in <memory>
#define __cpp_lib_reference_from_temporary          202202L // also in <type_traits>
#define __cpp_lib_remove_cvref                      201711L // also in <type_traits>
#define __cpp_lib_result_of_sfinae                  201210L // also in <functional>, <type_traits>
#define __cpp_lib_robust_nonmodifying_seq_ops       201304L // also in <algorithm>
#define __cpp_lib_sample                            201603L // also in <algorithm>
#define __cpp_lib_scoped_lock                       201703L // also in <mutex>
#define __cpp_lib_semaphore                         201907L // also in <semaphore>
#define __cpp_lib_shared_mutex                      201505L // also in <shared_mutex>
#define __cpp_lib_shared_ptr_arrays                 201707L // also in <memory>
#define __cpp_lib_shared_ptr_weak_type              201606L // also in <memory>
#define __cpp_lib_shared_timed_mutex                201402L // also in <shared_mutex>
#define __cpp_lib_shift                             202202L // also in <algorithm>
#define __cpp_lib_smart_ptr_for_overwrite           202002L // also in <memory>
#define __cpp_lib_source_location                   201907L // also in <source_location>
#define __cpp_lib_span                              202002L // also in <span>
#define __cpp_lib_spanstream                        202106L // also in <spanstream>
#define __cpp_lib_ssize                             201902L // also in <iterator>
#define __cpp_lib_stacktrace                        202011L // also in <stacktrace>
#define __cpp_lib_start_lifetime_as                 202207L // also in <memory>
#define __cpp_lib_starts_ends_with                  201711L // also in <string>, <string_view>
#define __cpp_lib_stdatomic_h                       202011L // also in <stdatomic.h>
#define __cpp_lib_string_contains                   202011L // also in <string>, <string_view>
#define __cpp_lib_string_resize_and_overwrite       202110L // also in <string>
#define __cpp_lib_string_udls                       201304L // also in <string>
#define __cpp_lib_string_view                       201803L // also in <string>, <string_view>
#define __cpp_lib_syncbuf                           201803L // also in <syncstream>
#define __cpp_lib_three_way_comparison              201907L // also in <compare>
#define __cpp_lib_to_address                        201711L // also in <memory>
#define __cpp_lib_to_array                          201907L // also in <array>
#define __cpp_lib_to_chars                          201611L // also in <charconv>
#define __cpp_lib_to_underlying                     202102L // also in <utility>
#define __cpp_lib_transformation_trait_aliases      201304L // also in <type_traits>
#define __cpp_lib_transparent_operators             201510L // also in <memory>, <functional>
#define __cpp_lib_tuple_like                        202207L
  // also in <utility>, <tuple>, <map>, <unordered_map>
#define __cpp_lib_tuple_element_t                   201402L // also in <tuple>
#define __cpp_lib_tuples_by_type                    201304L // also in <utility>, <tuple>
#define __cpp_lib_type_identity                     201806L // also in <type_traits>
#define __cpp_lib_type_trait_variable_templates     201510L // also in <type_traits>
#define __cpp_lib_uncaught_exceptions               201411L // also in <exception>
#define __cpp_lib_unordered_map_try_emplace         201411L // also in <unordered_map>
#define __cpp_lib_unreachable                       202202L // also in <utility>
#define __cpp_lib_unwrap_ref                        201811L // also in <type_traits>
#define __cpp_lib_variant                           202106L // also in <variant>
#define __cpp_lib_void_t                            201411L // also in <type_traits>
```

### Header `<limits>` synopsis <a id="limits.syn">[[limits.syn]]</a>

``` cpp
// all freestanding
namespace std {
  // [round.style], enumeration float_round_style
  enum float_round_style;

  // [numeric.limits], class template numeric_limits
  template<class T> class numeric_limits;

  template<class T> class numeric_limits<const T>;
  template<class T> class numeric_limits<volatile T>;
  template<class T> class numeric_limits<const volatile T>;

  template<> class numeric_limits<bool>;

  template<> class numeric_limits<char>;
  template<> class numeric_limits<signed char>;
  template<> class numeric_limits<unsigned char>;
  template<> class numeric_limits<char8_t>;
  template<> class numeric_limits<char16_t>;
  template<> class numeric_limits<char32_t>;
  template<> class numeric_limits<wchar_t>;

  template<> class numeric_limits<short>;
  template<> class numeric_limits<int>;
  template<> class numeric_limits<long>;
  template<> class numeric_limits<long long>;
  template<> class numeric_limits<unsigned short>;
  template<> class numeric_limits<unsigned int>;
  template<> class numeric_limits<unsigned long>;
  template<> class numeric_limits<unsigned long long>;

  template<> class numeric_limits<float>;
  template<> class numeric_limits<double>;
  template<> class numeric_limits<long double>;
}
```

### Enum `float_round_style` <a id="round.style">[[round.style]]</a>

``` cpp
namespace std {
  enum float_round_style {
    round_indeterminate       = -1,
    round_toward_zero         =  0,
    round_to_nearest          =  1,
    round_toward_infinity     =  2,
    round_toward_neg_infinity =  3
  };
}
```

The rounding mode for floating-point arithmetic is characterized by the
values:

- `round_indeterminate` if the rounding style is indeterminable
- `round_toward_zero` if the rounding style is toward zero
- `round_to_nearest` if the rounding style is to the nearest
  representable value
- `round_toward_infinity` if the rounding style is toward infinity
- `round_toward_neg_infinity` if the rounding style is toward negative
  infinity

### Class template `numeric_limits` <a id="numeric.limits">[[numeric.limits]]</a>

#### General <a id="numeric.limits.general">[[numeric.limits.general]]</a>

The `numeric_limits` class template provides a C++ program with
information about various properties of the implementation’s
representation of the arithmetic types.

``` cpp
namespace std {
  template<class T> class numeric_limits {
  public:
    static constexpr bool is_specialized = false;
    static constexpr T min() noexcept { return T(); }
    static constexpr T max() noexcept { return T(); }
    static constexpr T lowest() noexcept { return T(); }

    static constexpr int  digits = 0;
    static constexpr int  digits10 = 0;
    static constexpr int  max_digits10 = 0;
    static constexpr bool is_signed = false;
    static constexpr bool is_integer = false;
    static constexpr bool is_exact = false;
    static constexpr int  radix = 0;
    static constexpr T epsilon() noexcept { return T(); }
    static constexpr T round_error() noexcept { return T(); }

    static constexpr int  min_exponent = 0;
    static constexpr int  min_exponent10 = 0;
    static constexpr int  max_exponent = 0;
    static constexpr int  max_exponent10 = 0;

    static constexpr bool has_infinity = false;
    static constexpr bool has_quiet_NaN = false;
    static constexpr bool has_signaling_NaN = false;
    static constexpr T infinity() noexcept { return T(); }
    static constexpr T quiet_NaN() noexcept { return T(); }
    static constexpr T signaling_NaN() noexcept { return T(); }
    static constexpr T denorm_min() noexcept { return T(); }

    static constexpr bool is_iec559 = false;
    static constexpr bool is_bounded = false;
    static constexpr bool is_modulo = false;

    static constexpr bool traps = false;
    static constexpr bool tinyness_before = false;
    static constexpr float_round_style round_style = round_toward_zero;
  };
}
```

For all members declared `static` `constexpr` in the `numeric_limits`
template, specializations shall define these values in such a way that
they are usable as constant expressions.

For the `numeric_limits` primary template, all data members are
value-initialized and all member functions return a value-initialized
object.

\[*Note 1*: This means all members have zero or `false` values unless
`numeric_limits` is specialized for a type. — *end note*\]

Specializations shall be provided for each arithmetic type, both
floating-point and integer, including `bool`. The member
`is_specialized` shall be `true` for all such specializations of
`numeric_limits`.

The value of each member of a specialization of `numeric_limits` on a
cv-qualified type `cv T` shall be equal to the value of the
corresponding member of the specialization on the unqualified type `T`.

Non-arithmetic standard types, such as `complex<T>` [[complex]], shall
not have specializations.

#### `numeric_limits` members <a id="numeric.limits.members">[[numeric.limits.members]]</a>

Each member function defined in this subclause is signal-safe
[[support.signal]].

``` cpp
static constexpr T min() noexcept;
```

Minimum finite value.[^3]

For floating-point types with subnormal numbers, returns the minimum
positive normalized value.

Meaningful for all specializations in which `is_bounded != false`, or
`is_bounded == false && is_signed == false`.

``` cpp
static constexpr T max() noexcept;
```

Maximum finite value.[^4]

Meaningful for all specializations in which `is_bounded != false`.

``` cpp
static constexpr T lowest() noexcept;
```

A finite value `x` such that there is no other finite value `y` where
`y < x`.[^5]

Meaningful for all specializations in which `is_bounded != false`.

``` cpp
static constexpr int digits;
```

Number of `radix` digits that can be represented without change.

For integer types, the number of non-sign bits in the representation.

For floating-point types, the number of `radix` digits in the
mantissa.[^6]

``` cpp
static constexpr int digits10;
```

Number of base 10 digits that can be represented without change.[^7]

Meaningful for all specializations in which `is_bounded != false`.

``` cpp
static constexpr int max_digits10;
```

Number of base 10 digits required to ensure that values which differ are
always differentiated.

Meaningful for all floating-point types.

``` cpp
static constexpr bool is_signed;
```

`true` if the type is signed.

Meaningful for all specializations.

``` cpp
static constexpr bool is_integer;
```

`true` if the type is integer.

Meaningful for all specializations.

``` cpp
static constexpr bool is_exact;
```

`true` if the type uses an exact representation. All integer types are
exact, but not all exact types are integer. For example, rational and
fixed-exponent representations are exact but not integer.

Meaningful for all specializations.

``` cpp
static constexpr int radix;
```

For floating-point types, specifies the base or radix of the exponent
representation (often 2).[^8]

For integer types, specifies the base of the representation.[^9]

Meaningful for all specializations.

``` cpp
static constexpr T epsilon() noexcept;
```

Machine epsilon: the difference between 1 and the least value greater
than 1 that is representable.[^10]

Meaningful for all floating-point types.

``` cpp
static constexpr T round_error() noexcept;
```

Measure of the maximum rounding error.[^11]

``` cpp
static constexpr int  min_exponent;
```

Minimum negative integer such that `radix` raised to the power of one
less than that integer is a normalized floating-point number.[^12]

Meaningful for all floating-point types.

``` cpp
static constexpr int  min_exponent10;
```

Minimum negative integer such that 10 raised to that power is in the
range of normalized floating-point numbers.[^13]

Meaningful for all floating-point types.

``` cpp
static constexpr int  max_exponent;
```

Maximum positive integer such that `radix` raised to the power one less
than that integer is a representable finite floating-point number.[^14]

Meaningful for all floating-point types.

``` cpp
static constexpr int  max_exponent10;
```

Maximum positive integer such that 10 raised to that power is in the
range of representable finite floating-point numbers.[^15]

Meaningful for all floating-point types.

``` cpp
static constexpr bool has_infinity;
```

`true` if the type has a representation for positive infinity.

Meaningful for all floating-point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr bool has_quiet_NaN;
```

`true` if the type has a representation for a quiet (non-signaling) “Not
a Number”.[^16]

Meaningful for all floating-point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr bool has_signaling_NaN;
```

`true` if the type has a representation for a signaling “Not a
Number”.[^17]

Meaningful for all floating-point types.

Shall be `true` for all specializations in which `is_iec559 != false`.

``` cpp
static constexpr T infinity() noexcept;
```

Representation of positive infinity, if available.[^18]

Meaningful for all specializations for which `has_infinity != false`.
Required in specializations for which `is_iec559 != false`.

``` cpp
static constexpr T quiet_NaN() noexcept;
```

Representation of a quiet “Not a Number”, if available.[^19]

Meaningful for all specializations for which `has_quiet_NaN != false`.
Required in specializations for which `is_iec559 != false`.

``` cpp
static constexpr T signaling_NaN() noexcept;
```

Representation of a signaling “Not a Number”, if available.[^20]

Meaningful for all specializations for which
`has_signaling_NaN != false`. Required in specializations for which
`is_iec559 != false`.

``` cpp
static constexpr T denorm_min() noexcept;
```

Minimum positive subnormal value, if available.[^21]

Otherwise, minimum positive normalized value.

Meaningful for all floating-point types.

``` cpp
static constexpr bool is_iec559;
```

`true` if and only if the type adheres to ISO/IEC/IEEE 60559.[^22]

\[*Note 1*: The value is `true` for any of the types `float16_t`,
`float32_t`, `float64_t`, or `float128_t`, if
present [[basic.extended.fp]]. — *end note*\]

Meaningful for all floating-point types.

``` cpp
static constexpr bool is_bounded;
```

`true` if the set of values representable by the type is finite.[^23]

\[*Note 2*: All fundamental types [[basic.fundamental]] are bounded.
This member would be `false` for arbitrary precision
types. — *end note*\]

Meaningful for all specializations.

``` cpp
static constexpr bool is_modulo;
```

`true` if the type is modulo.[^24]

A type is modulo if, for any operation involving `+`, `-`, or `*` on
values of that type whose result would fall outside the range \[`min()`,
`max()`\], the value returned differs from the true value by an integer
multiple of `max() - min() + 1`.

\[*Example 1*: `is_modulo` is `false` for signed integer
types [[basic.fundamental]] unless an implementation, as an extension to
this document, defines signed integer overflow to
wrap. — *end example*\]

Meaningful for all specializations.

``` cpp
static constexpr bool traps;
```

`true` if, at the start of the program, there exists a value of the type
that would cause an arithmetic operation using that value to trap.[^25]

Meaningful for all specializations.

``` cpp
static constexpr bool tinyness_before;
```

`true` if tinyness is detected before rounding.[^26]

Meaningful for all floating-point types.

``` cpp
static constexpr float_round_style round_style;
```

The rounding style for the type.[^27]

Meaningful for all floating-point types. Specializations for integer
types shall return `round_toward_zero`.

#### `numeric_limits` specializations <a id="numeric.special">[[numeric.special]]</a>

All members shall be provided for all specializations. However, many
values are only required to be meaningful under certain conditions (for
example, `epsilon()` is only meaningful if `is_integer` is `false`). Any
value that is not “meaningful” shall be set to 0 or `false`.

\[*Example 1*:

``` cpp
namespace std {
  template<> class numeric_limits<float> {
  public:
    static constexpr bool is_specialized = true;

    static constexpr float min() noexcept { return 1.17549435E-38F; }
    static constexpr float max() noexcept { return 3.40282347E+38F; }
    static constexpr float lowest() noexcept { return -3.40282347E+38F; }

    static constexpr int digits   = 24;
    static constexpr int digits10 =  6;
    static constexpr int max_digits10 =  9;

    static constexpr bool is_signed  = true;
    static constexpr bool is_integer = false;
    static constexpr bool is_exact   = false;

    static constexpr int radix = 2;
    static constexpr float epsilon() noexcept     { return 1.19209290E-07F; }
    static constexpr float round_error() noexcept { return 0.5F; }

    static constexpr int min_exponent   = -125;
    static constexpr int min_exponent10 = - 37;
    static constexpr int max_exponent   = +128;
    static constexpr int max_exponent10 = + 38;

    static constexpr bool has_infinity             = true;
    static constexpr bool has_quiet_NaN            = true;
    static constexpr bool has_signaling_NaN        = true;

    static constexpr float infinity()      noexcept { return value; }
    static constexpr float quiet_NaN()     noexcept { return value; }
    static constexpr float signaling_NaN() noexcept { return value; }
    static constexpr float denorm_min()    noexcept { return min(); }

    static constexpr bool is_iec559  = true;
    static constexpr bool is_bounded = true;
    static constexpr bool is_modulo  = false;
    static constexpr bool traps      = true;
    static constexpr bool tinyness_before = true;

    static constexpr float_round_style round_style = round_to_nearest;
  };
}
```

— *end example*\]

The specialization for `bool` shall be provided as follows:

``` cpp
namespace std {
   template<> class numeric_limits<bool> {
   public:
     static constexpr bool is_specialized = true;
     static constexpr bool min() noexcept { return false; }
     static constexpr bool max() noexcept { return true; }
     static constexpr bool lowest() noexcept { return false; }

     static constexpr int  digits = 1;
     static constexpr int  digits10 = 0;
     static constexpr int  max_digits10 = 0;

     static constexpr bool is_signed = false;
     static constexpr bool is_integer = true;
     static constexpr bool is_exact = true;
     static constexpr int  radix = 2;
     static constexpr bool epsilon() noexcept { return 0; }
     static constexpr bool round_error() noexcept { return 0; }

     static constexpr int  min_exponent = 0;
     static constexpr int  min_exponent10 = 0;
     static constexpr int  max_exponent = 0;
     static constexpr int  max_exponent10 = 0;

     static constexpr bool has_infinity = false;
     static constexpr bool has_quiet_NaN = false;
     static constexpr bool has_signaling_NaN = false;
     static constexpr bool infinity() noexcept { return 0; }
     static constexpr bool quiet_NaN() noexcept { return 0; }
     static constexpr bool signaling_NaN() noexcept { return 0; }
     static constexpr bool denorm_min() noexcept { return 0; }

     static constexpr bool is_iec559 = false;
     static constexpr bool is_bounded = true;
     static constexpr bool is_modulo = false;

     static constexpr bool traps = false;
     static constexpr bool tinyness_before = false;
     static constexpr float_round_style round_style = round_toward_zero;
   };
}
```

### Header `<climits>` synopsis <a id="climits.syn">[[climits.syn]]</a>

``` cpp
// all freestanding
#define CHAR_BIT see below
#define SCHAR_MIN see below
#define SCHAR_MAX see below
#define UCHAR_MAX see below
#define CHAR_MIN see below
#define CHAR_MAX see below
#define MB_LEN_MAX see below
#define SHRT_MIN see below
#define SHRT_MAX see below
#define USHRT_MAX see below
#define INT_MIN see below
#define INT_MAX see below
#define UINT_MAX see below
#define LONG_MIN see below
#define LONG_MAX see below
#define ULONG_MAX see below
#define LLONG_MIN see below
#define LLONG_MAX see below
#define ULLONG_MAX see below
```

The header `<climits>` defines all macros the same as the C standard
library header `<limits.h>`.

\[*Note 1*: Except for `CHAR_BIT` and `MB_LEN_MAX`, a macro referring to
an integer type `T` defines a constant whose type is the promoted type
of `T` [[conv.prom]]. — *end note*\]

### Header `<cfloat>` synopsis <a id="cfloat.syn">[[cfloat.syn]]</a>

``` cpp
// all freestanding
#define FLT_ROUNDS see below
#define FLT_EVAL_METHOD see below
#define FLT_HAS_SUBNORM see below
#define DBL_HAS_SUBNORM see below
#define LDBL_HAS_SUBNORM see below
#define FLT_RADIX see below
#define FLT_MANT_DIG see below
#define DBL_MANT_DIG see below
#define LDBL_MANT_DIG see below
#define FLT_DECIMAL_DIG see below
#define DBL_DECIMAL_DIG see below
#define LDBL_DECIMAL_DIG see below
#define DECIMAL_DIG see below
#define FLT_DIG see below
#define DBL_DIG see below
#define LDBL_DIG see below
#define FLT_MIN_EXP see below
#define DBL_MIN_EXP see below
#define LDBL_MIN_EXP see below
#define FLT_MIN_10_EXP see below
#define DBL_MIN_10_EXP see below
#define LDBL_MIN_10_EXP see below
#define FLT_MAX_EXP see below
#define DBL_MAX_EXP see below
#define LDBL_MAX_EXP see below
#define FLT_MAX_10_EXP see below
#define DBL_MAX_10_EXP see below
#define LDBL_MAX_10_EXP see below
#define FLT_MAX see below
#define DBL_MAX see below
#define LDBL_MAX see below
#define FLT_EPSILON see below
#define DBL_EPSILON see below
#define LDBL_EPSILON see below
#define FLT_MIN see below
#define DBL_MIN see below
#define LDBL_MIN see below
#define FLT_TRUE_MIN see below
#define DBL_TRUE_MIN see below
#define LDBL_TRUE_MIN see below
```

The header `<cfloat>` defines all macros the same as the C standard
library header `<float.h>`.

## Arithmetic types <a id="support.arith.types">[[support.arith.types]]</a>

### Header `<cstdint>` synopsis <a id="cstdint.syn">[[cstdint.syn]]</a>

The header `<cstdint>` supplies integer types having specified widths,
and macros that specify limits of integer types.

``` cpp
// all freestanding
namespace std {
  using int8_t         = signed integer type;   // optional
  using int16_t        = signed integer type;   // optional
  using int32_t        = signed integer type;   // optional
  using int64_t        = signed integer type;   // optional
  using intN_t         = see below;             // optional

  using int_fast8_t    = signed integer type;
  using int_fast16_t   = signed integer type;
  using int_fast32_t   = signed integer type;
  using int_fast64_t   = signed integer type;
  using int_fastN_t    = see below;             // optional

  using int_least8_t   = signed integer type;
  using int_least16_t  = signed integer type;
  using int_least32_t  = signed integer type;
  using int_least64_t  = signed integer type;
  using int_leastN_t   = see below;             // optional

  using intmax_t       = signed integer type;
  using intptr_t       = signed integer type;   // optional

  using uint8_t        = unsigned integer type; // optional
  using uint16_t       = unsigned integer type; // optional
  using uint32_t       = unsigned integer type; // optional
  using uint64_t       = unsigned integer type; // optional
  using uintN_t        = see below;             // optional

  using uint_fast8_t   = unsigned integer type;
  using uint_fast16_t  = unsigned integer type;
  using uint_fast32_t  = unsigned integer type;
  using uint_fast64_t  = unsigned integer type;
  using uint_fastN_t   = see below;             // optional

  using uint_least8_t  = unsigned integer type;
  using uint_least16_t = unsigned integer type;
  using uint_least32_t = unsigned integer type;
  using uint_least64_t = unsigned integer type;
  using uint_leastN_t  = see below;             // optional

  using uintmax_t      = unsigned integer type;
  using uintptr_t      = unsigned integer type; // optional
}

#define INTN_MIN         see below
#define INTN_MAX         see below
#define UINTN_MAX        see below

#define INT_FASTN_MIN    see below
#define INT_FASTN_MAX    see below
#define UINT_FASTN_MAX   see below

#define INT_LEASTN_MIN   see below
#define INT_LEASTN_MAX   see below
#define UINT_LEASTN_MAX  see below

#define INTMAX_MIN       see below
#define INTMAX_MAX       see below
#define UINTMAX_MAX      see below

#define INTPTR_MIN       see below              // optional
#define INTPTR_MAX       see below              // optional
#define UINTPTR_MAX      see below              // optional

#define PTRDIFF_MIN      see below
#define PTRDIFF_MAX      see below
#define SIZE_MAX         see below

#define SIG_ATOMIC_MIN   see below
#define SIG_ATOMIC_MAX   see below

#define WCHAR_MIN        see below
#define WCHAR_MAX        see below

#define WINT_MIN         see below
#define WINT_MAX         see below

#define INTN_C(value)    see below
#define UINTN_C(value)   see below
#define INTMAX_C(value)  see below
#define UINTMAX_C(value) see below
```

The header defines all types and macros the same as the C standard
library header `<stdint.h>`.

All types that use the placeholder *N* are optional when *N* is not `8`,
`16`, `32`, or `64`. The exact-width types `intN_t` and `uintN_t` for
*N* = `8`, `16`, `32`, and `64` are also optional; however, if an
implementation defines integer types with the corresponding width and no
padding bits, it defines the corresponding *typedef-name*s. Each of the
macros listed in this subclause is defined if and only if the
implementation defines the corresponding *typedef-name*.

\[*Note 1*: The macros `INTN_C` and `UINTN_C` correspond to the
*typedef-name*s `int_leastN_t` and `uint_leastN_t`,
respectively. — *end note*\]

### Header `<stdfloat>` synopsis <a id="stdfloat.syn">[[stdfloat.syn]]</a>

The header `<stdfloat>` defines type aliases for the optional extended
floating-point types that are specified in [[basic.extended.fp]].

``` cpp
namespace std {
  #if defined(__STDCPP_FLOAT16_T__)
    using float16_t  = implementation-defined;  // see [basic.extended.fp]
  #endif
  #if defined(__STDCPP_FLOAT32_T__)
    using float32_t  = implementation-defined;  // see [basic.extended.fp]
  #endif
  #if defined(__STDCPP_FLOAT64_T__)
    using float64_t  = implementation-defined;  // see [basic.extended.fp]
  #endif
  #if defined(__STDCPP_FLOAT128_T__)
    using float128_t = implementation-defined; // see [basic.extended.fp]
  #endif
  #if defined(__STDCPP_BFLOAT16_T__)
    using bfloat16_t = implementation-defined; // see [basic.extended.fp]
  #endif
}
```

## Startup and termination <a id="support.start.term">[[support.start.term]]</a>

\[*Note 1*: The header `<cstdlib>` declares the functions described in
this subclause. — *end note*\]

``` cpp
[[noreturn]] void _Exit(int status) noexcept;
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* The program is terminated without executing destructors for
objects of automatic, thread, or static storage duration and without
calling functions passed to `atexit()`[[basic.start.term]]. The function
`_Exit` is signal-safe [[support.signal]].

``` cpp
[[noreturn]] void abort() noexcept;
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* The program is terminated without executing destructors for
objects of automatic, thread, or static storage duration and without
calling functions passed to `atexit()`[[basic.start.term]]. The function
`abort` is signal-safe [[support.signal]].

``` cpp
int atexit(c-atexit-handler* f) noexcept;
int atexit(atexit-handler* f) noexcept;
```

*Effects:* The `atexit()` functions register the function pointed to by
`f` to be called without arguments at normal program termination. It is
unspecified whether a call to `atexit()` that does not happen
before [[intro.multithread]] a call to `exit()` will succeed.

\[*Note 1*: The `atexit()` functions do not introduce a data
race [[res.on.data.races]]. — *end note*\]

*Implementation limits:* The implementation shall support the
registration of at least 32 functions.

*Returns:* The `atexit()` function returns zero if the registration
succeeds, nonzero if it fails.

``` cpp
[[noreturn]] void exit(int status);
```

*Effects:*

- First, objects with thread storage duration and associated with the
  current thread are destroyed. Next, objects with static storage
  duration are destroyed and functions registered by calling `atexit`
  are called.[^28] See  [[basic.start.term]] for the order of
  destructions and calls. (Objects with automatic storage duration are
  not destroyed as a result of calling `exit()`.)[^29] If a registered
  function invoked by `exit` exits via an exception, the function
  `std::terminate` is invoked [[except.terminate]].
- Next, all open C streams (as mediated by the function signatures
  declared in `<cstdio>`) with unwritten buffered data are flushed, all
  open C streams are closed, and all files created by calling
  `tmpfile()` are removed.
- Finally, control is returned to the host environment. If `status` is
  zero or `EXIT_SUCCESS`, an *implementation-defined* form of the status
  *successful termination* is returned. If `status` is `EXIT_FAILURE`,
  an *implementation-defined* form of the status *unsuccessful
  termination* is returned. Otherwise the status returned is
  *implementation-defined*.[^30]

``` cpp
int at_quick_exit(c-atexit-handler* f) noexcept;
int at_quick_exit(atexit-handler* f) noexcept;
```

*Effects:* The `at_quick_exit()` functions register the function pointed
to by `f` to be called without arguments when `quick_exit` is called. It
is unspecified whether a call to `at_quick_exit()` that does not happen
before [[intro.multithread]] all calls to `quick_exit` will succeed.

\[*Note 2*: The `at_quick_exit()` functions do not introduce a data
race [[res.on.data.races]]. — *end note*\]

\[*Note 3*: The order of registration could be indeterminate if
`at_quick_exit` was called from more than one thread. — *end note*\]

\[*Note 4*: The `at_quick_exit` registrations are distinct from the
`atexit` registrations, and applications might need to call both
registration functions with the same argument. — *end note*\]

*Implementation limits:* The implementation shall support the
registration of at least 32 functions.

*Returns:* Zero if the registration succeeds, nonzero if it fails.

``` cpp
[[noreturn]] void quick_exit(int status) noexcept;
```

*Effects:* Functions registered by calls to `at_quick_exit` are called
in the reverse order of their registration, except that a function shall
be called after any previously registered functions that had already
been called at the time it was registered. Objects shall not be
destroyed as a result of calling `quick_exit`. If a registered function
invoked by `quick_exit` exits via an exception, the function
`std::terminate` is invoked [[except.terminate]].

\[*Note 5*: A function registered via `at_quick_exit` is invoked by the
thread that calls `quick_exit`, which can be a different thread than the
one that registered it, so registered functions cannot rely on the
identity of objects with thread storage duration. — *end note*\]

After calling registered functions, `quick_exit` shall call
`_Exit(status)`.

*Remarks:* The function `quick_exit` is signal-safe [[support.signal]]
when the functions registered with `at_quick_exit` are.

## Dynamic memory management <a id="support.dynamic">[[support.dynamic]]</a>

### General <a id="support.dynamic.general">[[support.dynamic.general]]</a>

The header `<new>` defines several functions that manage the allocation
of dynamic storage in a program. It also defines components for
reporting storage management errors.

### Header `<new>` synopsis <a id="new.syn">[[new.syn]]</a>

``` cpp
// all freestanding
namespace std {
  // [alloc.errors], storage allocation errors
  class bad_alloc;
  class bad_array_new_length;

  struct destroying_delete_t {
    explicit destroying_delete_t() = default;
  };
  inline constexpr destroying_delete_t destroying_delete{};

  // global operator new control%
  \indexlibraryglobal{align_val_t  \indexlibraryglobal{destroying_delete_t  \indexlibraryglobal{destroying_delete  \indexlibraryglobal{nothrow_t  \indexlibraryglobal{nothrow}
  enum class align_val_t : size_t {};

  struct nothrow_t { explicit nothrow_t() = default; };
  extern const nothrow_t nothrow;

  using new_handler = void (*)();
  new_handler get_new_handler() noexcept;
  new_handler set_new_handler(new_handler new_p) noexcept;

  // [ptr.launder], pointer optimization barrier
  template<class T> [[nodiscard]] constexpr T* launder(T* p) noexcept;

  // [hardware.interference], hardware interference size
  inline constexpr size_t hardware_destructive_interference_size = implementation-defined{};
  inline constexpr size_t hardware_constructive_interference_size = implementation-defined{};
}

// [new.delete], storage allocation and deallocation
[[nodiscard]] void* operator new(std::size_t size);
[[nodiscard]] void* operator new(std::size_t size, std::align_val_t alignment);
[[nodiscard]] void* operator new(std::size_t size, const std::nothrow_t&) noexcept;
[[nodiscard]] void* operator new(std::size_t size, std::align_val_t alignment,
                                 const std::nothrow_t&) noexcept;

void operator delete(void* ptr) noexcept;
void operator delete(void* ptr, std::size_t size) noexcept;
void operator delete(void* ptr, std::align_val_t alignment) noexcept;
void operator delete(void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
void operator delete(void* ptr, const std::nothrow_t&) noexcept;
void operator delete(void* ptr, std::align_val_t alignment, const std::nothrow_t&) noexcept;

[[nodiscard]] void* operator new[](std::size_t size);
[[nodiscard]] void* operator new[](std::size_t size, std::align_val_t alignment);
[[nodiscard]] void* operator new[](std::size_t size, const std::nothrow_t&) noexcept;
[[nodiscard]] void* operator new[](std::size_t size, std::align_val_t alignment,
                                   const std::nothrow_t&) noexcept;

void operator delete[](void* ptr) noexcept;
void operator delete[](void* ptr, std::size_t size) noexcept;
void operator delete[](void* ptr, std::align_val_t alignment) noexcept;
void operator delete[](void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
void operator delete[](void* ptr, const std::nothrow_t&) noexcept;
void operator delete[](void* ptr, std::align_val_t alignment, const std::nothrow_t&) noexcept;

[[nodiscard]] void* operator new  (std::size_t size, void* ptr) noexcept;
[[nodiscard]] void* operator new[](std::size_t size, void* ptr) noexcept;
void operator delete  (void* ptr, void*) noexcept;
void operator delete[](void* ptr, void*) noexcept;
```

### Storage allocation and deallocation <a id="new.delete">[[new.delete]]</a>

#### General <a id="new.delete.general">[[new.delete.general]]</a>

Except where otherwise specified, the provisions of 
[[basic.stc.dynamic]] apply to the library versions of `operator new`
and `operator
delete`. If the value of an alignment argument passed to any of these
functions is not a valid alignment value, the behavior is undefined.

#### Single-object forms <a id="new.delete.single">[[new.delete.single]]</a>

``` cpp
[[nodiscard]] void* operator new(std::size_t size);
[[nodiscard]] void* operator new(std::size_t size, std::align_val_t alignment);
```

*Effects:* The allocation functions [[basic.stc.dynamic.allocation]]
called by a *new-expression*[[expr.new]] to allocate `size` bytes of
storage. The second form is called for a type with new-extended
alignment, and the first form is called otherwise.

*Replaceable:* A C++ program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage [[basic.stc.dynamic]], or else throw a `bad_alloc` exception.
This requirement is binding on any replacement versions of these
functions.

*Default behavior:*

- Executes a loop: Within the loop, the function first attempts to
  allocate the requested storage. Whether the attempt involves a call to
  the C standard library functions `malloc` or `aligned_alloc` is
  unspecified.
- Returns a pointer to the allocated storage if the attempt is
  successful. Otherwise, if the current `new_handler`[[get.new.handler]]
  is a null pointer value, throws `bad_alloc`.
- Otherwise, the function calls the current `new_handler`
  function [[new.handler]]. If the called function returns, the loop
  repeats.
- The loop terminates when an attempt to allocate the requested storage
  is successful or when a called `new_handler` function does not return.

``` cpp
[[nodiscard]] void* operator new(std::size_t size, const std::nothrow_t&) noexcept;
[[nodiscard]] void* operator new(std::size_t size, std::align_val_t alignment,
                                 const std::nothrow_t&) noexcept;
```

*Effects:* Same as above, except that these are called by a placement
version of a *new-expression* when a C++ program prefers a null pointer
result as an error indication, instead of a `bad_alloc` exception.

*Replaceable:* A C++ program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage [[basic.stc.dynamic]], or else return a null pointer. Each of
these nothrow versions of `operator new` returns a pointer obtained as
if acquired from the (possibly replaced) corresponding non-placement
function. This requirement is binding on any replacement versions of
these functions.

*Default behavior:* Calls `operator new(size)`, or
`operator new(size, alignment)`, respectively. If the call returns
normally, returns the result of that call. Otherwise, returns a null
pointer.

\[*Example 1*:

``` cpp
T* p1 = new T;                  // throws bad_alloc if it fails
T* p2 = new(nothrow) T;         // returns nullptr if it fails
```

— *end example*\]

``` cpp
void operator delete(void* ptr) noexcept;
void operator delete(void* ptr, std::size_t size) noexcept;
void operator delete(void* ptr, std::align_val_t alignment) noexcept;
void operator delete(void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
```

*Preconditions:* `ptr` is a null pointer or its value represents the
address of a block of memory allocated by an earlier call to a (possibly
replaced) `operator new(std::size_t)` or
`operator new(std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete`.

If the `alignment` parameter is not present, `ptr` was returned by an
allocation function without an `alignment` parameter. If present, the
`alignment` argument is equal to the `alignment` argument passed to the
allocation function that returned `ptr`. If present, the `size` argument
is equal to the `size` argument passed to the allocation function that
returned `ptr`.

*Effects:* The deallocation functions [[basic.stc.dynamic.deallocation]]
called by a *delete-expression*[[expr.delete]] to render the value of
`ptr` invalid.

*Replaceable:* A C++ program may define functions with any of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

If a function without a `size` parameter is defined, the program should
also define the corresponding function with a `size` parameter. If a
function with a `size` parameter is defined, the program shall also
define the corresponding version without the `size` parameter.

\[*Note 1*: The default behavior below might change in the future, which
will require replacing both deallocation functions when replacing the
allocation function. — *end note*\]

*Required behavior:* A call to an `operator delete` with a `size`
parameter may be changed to a call to the corresponding
`operator delete` without a `size` parameter, without affecting memory
allocation.

\[*Note 2*: A conforming implementation is for
`operator delete(void* ptr, std::size_t size)` to simply call
`operator delete(ptr)`. — *end note*\]

*Default behavior:* The functions that have a `size` parameter forward
their other parameters to the corresponding function without a `size`
parameter.

\[*Note 3*: See the note in the above *Replaceable:*
paragraph. — *end note*\]

*Default behavior:* If `ptr` is null, does nothing. Otherwise, reclaims
the storage allocated by the earlier call to `operator new`.

*Remarks:* It is unspecified under what conditions part or all of such
reclaimed storage will be allocated by subsequent calls to
`operator new` or any of `aligned_alloc`, `calloc`, `malloc`, or
`realloc`, declared in `<cstdlib>`.

``` cpp
void operator delete(void* ptr, const std::nothrow_t&) noexcept;
void operator delete(void* ptr, std::align_val_t alignment, const std::nothrow_t&) noexcept;
```

*Preconditions:* `ptr` is a null pointer or its value represents the
address of a block of memory allocated by an earlier call to a (possibly
replaced) `operator new(std::size_t)` or
`operator new(std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete`.

If the `alignment` parameter is not present, `ptr` was returned by an
allocation function without an `alignment` parameter. If present, the
`alignment` argument is equal to the `alignment` argument passed to the
allocation function that returned `ptr`.

*Effects:* The deallocation functions [[basic.stc.dynamic.deallocation]]
called by the implementation to render the value of `ptr` invalid when
the constructor invoked from a nothrow placement version of the
*new-expression* throws an exception.

*Replaceable:* A C++ program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

*Default behavior:* Calls `operator delete(ptr)`, or
`operator delete(ptr, alignment)`, respectively.

#### Array forms <a id="new.delete.array">[[new.delete.array]]</a>

``` cpp
[[nodiscard]] void* operator new[](std::size_t size);
[[nodiscard]] void* operator new[](std::size_t size, std::align_val_t alignment);
```

*Effects:* The allocation functions [[basic.stc.dynamic.allocation]]
called by the array form of a *new-expression*[[expr.new]] to allocate
`size` bytes of storage. The second form is called for a type with
new-extended alignment, and the first form is called otherwise.[^31]

*Replaceable:* A C++ program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

*Required behavior:* Same as for the corresponding single-object forms.
This requirement is binding on any replacement versions of these
functions.

*Default behavior:* Returns `operator new(size)`, or
`operator new(size, alignment)`, respectively.

``` cpp
[[nodiscard]] void* operator new[](std::size_t size, const std::nothrow_t&) noexcept;
[[nodiscard]] void* operator new[](std::size_t size, std::align_val_t alignment,
                                   const std::nothrow_t&) noexcept;
```

*Effects:* Same as above, except that these are called by a placement
version of a *new-expression* when a C++ program prefers a null pointer
result as an error indication, instead of a `bad_alloc` exception.

*Replaceable:* A C++ program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

*Required behavior:* Return a non-null pointer to suitably aligned
storage [[basic.stc.dynamic]], or else return a null pointer. Each of
these nothrow versions of `operator new[]` returns a pointer obtained as
if acquired from the (possibly replaced) corresponding non-placement
function. This requirement is binding on any replacement versions of
these functions.

*Default behavior:* Calls `operator new[](size)`, or
`operator new[](size, alignment)`, respectively. If the call returns
normally, returns the result of that call. Otherwise, returns a null
pointer.

``` cpp
void operator delete[](void* ptr) noexcept;
void operator delete[](void* ptr, std::size_t size) noexcept;
void operator delete[](void* ptr, std::align_val_t alignment) noexcept;
void operator delete[](void* ptr, std::size_t size, std::align_val_t alignment) noexcept;
```

*Preconditions:* `ptr` is a null pointer or its value represents the
address of a block of memory allocated by an earlier call to a (possibly
replaced) `operator new[](std::size_t)` or
`operator new[](std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete[]`.

If the `alignment` parameter is not present, `ptr` was returned by an
allocation function without an `alignment` parameter. If present, the
`alignment` argument is equal to the `alignment` argument passed to the
allocation function that returned `ptr`. If present, the `size` argument
is equal to the `size` argument passed to the allocation function that
returned `ptr`.

*Effects:* The deallocation functions [[basic.stc.dynamic.deallocation]]
called by the array form of a *delete-expression* to render the value of
`ptr` invalid.

*Replaceable:* A C++ program may define functions with any of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

If a function without a `size` parameter is defined, the program should
also define the corresponding function with a `size` parameter. If a
function with a `size` parameter is defined, the program shall also
define the corresponding version without the `size` parameter.

\[*Note 1*: The default behavior below might change in the future, which
will require replacing both deallocation functions when replacing the
allocation function. — *end note*\]

*Required behavior:* A call to an `operator delete[]` with a `size`
parameter may be changed to a call to the corresponding
`operator delete[]` without a `size` parameter, without affecting memory
allocation.

\[*Note 2*: A conforming implementation is for
`operator delete[](void* ptr, std::size_t size)` to simply call
`operator delete[](ptr)`. — *end note*\]

*Default behavior:* The functions that have a `size` parameter forward
their other parameters to the corresponding function without a `size`
parameter. The functions that do not have a `size` parameter forward
their parameters to the corresponding `operator delete` (single-object)
function.

``` cpp
void operator delete[](void* ptr, const std::nothrow_t&) noexcept;
void operator delete[](void* ptr, std::align_val_t alignment, const std::nothrow_t&) noexcept;
```

*Preconditions:* `ptr` is a null pointer or its value represents the
address of a block of memory allocated by an earlier call to a (possibly
replaced) `operator new[](std::size_t)` or
`operator new[](std::size_t, std::align_val_t)` which has not been
invalidated by an intervening call to `operator delete[]`.

If the `alignment` parameter is not present, `ptr` was returned by an
allocation function without an `alignment` parameter. If present, the
`alignment` argument is equal to the `alignment` argument passed to the
allocation function that returned `ptr`.

*Effects:* The deallocation functions [[basic.stc.dynamic.deallocation]]
called by the implementation to render the value of `ptr` invalid when
the constructor invoked from a nothrow placement version of the array
*new-expression* throws an exception.

*Replaceable:* A C++ program may define functions with either of these
function signatures, and thereby displace the default versions defined
by the C++ standard library.

*Default behavior:* Calls `operator delete[](ptr)`, or
`operator delete[](ptr, alignment)`, respectively.

#### Non-allocating forms <a id="new.delete.placement">[[new.delete.placement]]</a>

These functions are reserved; a C++ program may not define functions
that displace the versions in the C++ standard library [[constraints]].
The provisions of  [[basic.stc.dynamic]] do not apply to these reserved
placement forms of `operator new` and `operator delete`.

``` cpp
[[nodiscard]] void* operator new(std::size_t size, void* ptr) noexcept;
```

*Returns:* `ptr`.

*Remarks:* Intentionally performs no other action.

\[*Example 1*:

This can be useful for constructing an object at a known address:

``` cpp
void* place = operator new(sizeof(Something));
Something* p = new (place) Something();
```

— *end example*\]

``` cpp
[[nodiscard]] void* operator new[](std::size_t size, void* ptr) noexcept;
```

*Returns:* `ptr`.

*Remarks:* Intentionally performs no other action.

``` cpp
void operator delete(void* ptr, void*) noexcept;
```

*Effects:* Intentionally performs no action.

*Remarks:* Default function called when any part of the initialization
in a placement *new-expression* that invokes the library’s non-array
placement operator new terminates by throwing an exception [[expr.new]].

``` cpp
void operator delete[](void* ptr, void*) noexcept;
```

*Effects:* Intentionally performs no action.

*Remarks:* Default function called when any part of the initialization
in a placement *new-expression* that invokes the library’s array
placement operator new terminates by throwing an exception [[expr.new]].

#### Data races <a id="new.delete.dataraces">[[new.delete.dataraces]]</a>

For purposes of determining the existence of data races, the library
versions of `operator new`, user replacement versions of global
`operator new`, the C standard library functions `aligned_alloc`,
`calloc`, and `malloc`, the library versions of `operator delete`, user
replacement versions of `operator delete`, the C standard library
function `free`, and the C standard library function `realloc` shall not
introduce a data race [[res.on.data.races]]. Calls to these functions
that allocate or deallocate a particular unit of storage shall occur in
a single total order, and each such deallocation call shall happen
before [[intro.multithread]] the next allocation (if any) in this order.

### Storage allocation errors <a id="alloc.errors">[[alloc.errors]]</a>

#### Class `bad_alloc` <a id="bad.alloc">[[bad.alloc]]</a>

``` cpp
namespace std {
  class bad_alloc : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

The class `bad_alloc` defines the type of objects thrown as exceptions
by the implementation to report a failure to allocate storage.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

#### Class `bad_array_new_length` <a id="new.badlength">[[new.badlength]]</a>

``` cpp
namespace std {
  class bad_array_new_length : public bad_alloc {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

The class `bad_array_new_length` defines the type of objects thrown as
exceptions by the implementation to report an attempt to allocate an
array of size less than zero or greater than an *implementation-defined*
limit [[expr.new]].

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

#### Type `new_handler` <a id="new.handler">[[new.handler]]</a>

``` cpp
using new_handler = void (*)();
```

The type of a *handler function* to be called by `operator new()` or
`operator new[]()`[[new.delete]] when they cannot satisfy a request for
additional storage.

*Required behavior:* A `new_handler` shall perform one of the following:

- make more storage available for allocation and then return;
- throw an exception of type `bad_alloc` or a class derived from
  `bad_alloc`;
- terminate execution of the program without returning to the caller.

#### `set_new_handler` <a id="set.new.handler">[[set.new.handler]]</a>

``` cpp
new_handler set_new_handler(new_handler new_p) noexcept;
```

*Effects:* Establishes the function designated by `new_p` as the current
`new_handler`.

*Returns:* The previous `new_handler`.

*Remarks:* The initial `new_handler` is a null pointer.

#### `get_new_handler` <a id="get.new.handler">[[get.new.handler]]</a>

``` cpp
new_handler get_new_handler() noexcept;
```

*Returns:* The current `new_handler`.

\[*Note 1*: This can be a null pointer value. — *end note*\]

### Pointer optimization barrier <a id="ptr.launder">[[ptr.launder]]</a>

``` cpp
template<class T> [[nodiscard]] constexpr T* launder(T* p) noexcept;
```

*Mandates:* `!is_function_v<T> && !is_void_v<T>` is `true`.

*Preconditions:* `p` represents the address *A* of a byte in memory. An
object *X* that is within its lifetime [[basic.life]] and whose type is
similar [[conv.qual]] to `T` is located at the address *A*. All bytes of
storage that would be reachable through [[basic.compound]] the result
are reachable through `p`.

*Returns:* A value of type `T*` that points to *X*.

*Remarks:* An invocation of this function may be used in a core constant
expression if and only if the (converted) value of its argument may be
used in place of the function invocation.

\[*Note 1*: If a new object is created in storage occupied by an
existing object of the same type, a pointer to the original object can
be used to refer to the new object unless its complete object is a const
object or it is a base class subobject; in the latter cases, this
function can be used to obtain a usable pointer to the new object.
See  [[basic.life]]. — *end note*\]

\[*Example 1*:

``` cpp
struct X { int n; };
const X *p = new const X{3};
const int a = p->n;
new (const_cast<X*>(p)) const X{5}; // p does not point to new objectREF:basic.life because its type is const
const int b = p->n;                 // undefined behavior
const int c = std::launder(p)->n;   // OK
```

— *end example*\]

### Hardware interference size <a id="hardware.interference">[[hardware.interference]]</a>

``` cpp
inline constexpr size_t hardware_destructive_interference_size = implementation-defined{};
```

This number is the minimum recommended offset between two
concurrently-accessed objects to avoid additional performance
degradation due to contention introduced by the implementation. It shall
be at least `alignof(max_align_t)`.

\[*Example 1*:

``` cpp
struct keep_apart {
  alignas(hardware_destructive_interference_size) atomic<int> cat;
  alignas(hardware_destructive_interference_size) atomic<int> dog;
};
```

— *end example*\]

``` cpp
inline constexpr size_t hardware_constructive_interference_size = implementation-defined{};
```

This number is the maximum recommended size of contiguous memory
occupied by two objects accessed with temporal locality by concurrent
threads. It shall be at least `alignof(max_align_t)`.

\[*Example 2*:

``` cpp
struct together {
  atomic<int> dog;
  int puppy;
};
struct kennel {
  // Other data members...
  alignas(sizeof(together)) together pack;
  // Other data members...
};
static_assert(sizeof(together) <= hardware_constructive_interference_size);
```

— *end example*\]

## Type identification <a id="support.rtti">[[support.rtti]]</a>

### General <a id="support.rtti.general">[[support.rtti.general]]</a>

The header `<typeinfo>` defines a type associated with type information
generated by the implementation. It also defines two types for reporting
dynamic type identification errors.

### Header `<typeinfo>` synopsis <a id="typeinfo.syn">[[typeinfo.syn]]</a>

``` cpp
// all freestanding
namespace std {
  class type_info;
  class bad_cast;
  class bad_typeid;
}
```

### Class `type_info` <a id="type.info">[[type.info]]</a>

``` cpp
namespace std {
  class type_info {
  public:
    virtual ~type_info();
    constexpr bool operator==(const type_info& rhs) const noexcept;
    bool before(const type_info& rhs) const noexcept;
    size_t hash_code() const noexcept;
    const char* name() const noexcept;

    type_info(const type_info&) = delete;                   // cannot be copied
    type_info& operator=(const type_info&) = delete;        // cannot be copied
  };
}
```

The class `type_info` describes type information generated by the
implementation [[expr.typeid]]. Objects of this class effectively store
a pointer to a name for the type, and an encoded value suitable for
comparing two types for equality or collating order. The names, encoding
rule, and collating sequence for types are all unspecified and may
differ between programs.

``` cpp
constexpr bool operator==(const type_info& rhs) const noexcept;
```

*Effects:* Compares the current object with `rhs`.

*Returns:* `true` if the two values describe the same type.

``` cpp
bool before(const type_info& rhs) const noexcept;
```

*Effects:* Compares the current object with `rhs`.

*Returns:* `true` if `*this` precedes `rhs` in the implementation’s
collation order.

``` cpp
size_t hash_code() const noexcept;
```

*Returns:* An unspecified value, except that within a single execution
of the program, it shall return the same value for any two `type_info`
objects which compare equal.

*Remarks:* An implementation should return different values for two
`type_info` objects which do not compare equal.

``` cpp
const char* name() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string [[multibyte.strings]], suitable for conversion and display as a
`wstring`[[string.classes,locale.codecvt]].

### Class `bad_cast` <a id="bad.cast">[[bad.cast]]</a>

``` cpp
namespace std {
  class bad_cast : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

The class `bad_cast` defines the type of objects thrown as exceptions by
the implementation to report the execution of an invalid `dynamic_cast`
expression [[expr.dynamic.cast]].

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Class `bad_typeid` <a id="bad.typeid">[[bad.typeid]]</a>

``` cpp
namespace std {
  class bad_typeid : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

The class `bad_typeid` defines the type of objects thrown as exceptions
by the implementation to report a null pointer in a `typeid` expression
[[expr.typeid]].

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

## Source location <a id="support.srcloc">[[support.srcloc]]</a>

### Header `<source_location>` synopsis <a id="source.location.syn">[[source.location.syn]]</a>

The header `<source_location>` defines the class `source_location` that
provides a means to obtain source location information.

``` cpp
// all freestanding
namespace std {
  struct source_location;
}
```

### Class `source_location` <a id="support.srcloc.class">[[support.srcloc.class]]</a>

#### General <a id="support.srcloc.class.general">[[support.srcloc.class.general]]</a>

``` cpp
namespace std {
  struct source_location {
    // source location construction
    static consteval source_location current() noexcept;
    constexpr source_location() noexcept;

    // source location field access
    constexpr uint_least32_t line() const noexcept;
    constexpr uint_least32_t column() const noexcept;
    constexpr const char* file_name() const noexcept;
    constexpr const char* function_name() const noexcept;

  private:
    uint_least32_t line_;               // exposition only
    uint_least32_t column_;             // exposition only
    const char* file_name_;             // exposition only
    const char* function_name_;         // exposition only
  };
}
```

The type `source_location` meets the *Cpp17DefaultConstructible*,
*Cpp17CopyConstructible*, *Cpp17CopyAssignable*, *Cpp17Swappable*, and
*Cpp17Destructible* requirements
[[utility.arg.requirements]], [[swappable.requirements]]. All of the
following conditions are `true`:

- `is_nothrow_move_constructible_v<source_location>`
- `is_nothrow_move_assignable_v<source_location>`
- `is_nothrow_swappable_v<source_location>`

\[*Note 1*: The intent of `source_location` is to have a small size and
efficient copying. It is unspecified whether the copy/move constructors
and the copy/move assignment operators are trivial and/or
constexpr. — *end note*\]

The data members `file_name_` and `function_name_` always each refer to
an NTBS.

The copy/move constructors and the copy/move assignment operators of
`source_location` meet the following postconditions: Given two objects
`lhs` and `rhs` of type `source_location`, where `lhs` is a copy/move
result of `rhs`, and where `rhs_p` is a value denoting the state of
`rhs` before the corresponding copy/move operation, then each of the
following conditions is `true`:

- `strcmp(lhs.file_name(), rhs_p.file_name()) == 0`
- `strcmp(lhs.function_name(), rhs_p.function_name()) == 0`
- `lhs.line() == rhs_p.line()`
- `lhs.column() == rhs_p.column()`

#### Creation <a id="support.srcloc.cons">[[support.srcloc.cons]]</a>

``` cpp
static consteval source_location current() noexcept;
```

*Returns:*

- When invoked by a function call whose *postfix-expression* is a
  (possibly parenthesized) *id-expression* naming `current`, returns a
  `source_location` with an *implementation-defined* value. The value
  should be affected by `#line`[[cpp.line]] in the same manner as for
  \_\_LINE\_\_ and \_\_FILE\_\_. The values of the exposition-only data
  members of the returned `source_location` object are indicated in
  [[support.srcloc.current]].
- Otherwise, when invoked in some other way, returns a `source_location`
  whose data members are initialized with valid but unspecified values.

*Remarks:* Any call to `current` that appears as a default member
initializer [[class.mem]], or as a subexpression thereof, should
correspond to the location of the constructor definition or aggregate
initialization that uses the default member initializer. Any call to
`current` that appears as a default argument [[dcl.fct.default]], or as
a subexpression thereof, should correspond to the location of the
invocation of the function that uses the default argument [[expr.call]].

\[*Example 1*:

``` cpp
struct s {
  source_location member = source_location::current();
  int other_member;
  s(source_location loc = source_location::current())
    : member(loc)               // values of member refer to the location of the calling function[dcl.fct.default]
  {}
  s(int blather) :              // values of member refer to this location
    other_member(blather)
  {}
  s(double)                     // values of member refer to this location
  {}
};
void f(source_location a = source_location::current()) {
  source_location b = source_location::current();       // values in b refer to this line
}

void g() {
  f();                          // f's first argument corresponds to this line of code

  source_location c = source_location::current();
  f(c);                         // f's first argument gets the same values as c, above
}
```

— *end example*\]

``` cpp
constexpr source_location() noexcept;
```

*Effects:* The data members are initialized with valid but unspecified
values.

#### Observers <a id="support.srcloc.obs">[[support.srcloc.obs]]</a>

``` cpp
constexpr uint_least32_t line() const noexcept;
```

*Returns:* `line_`.

``` cpp
constexpr uint_least32_t column() const noexcept;
```

*Returns:* `column_`.

``` cpp
constexpr const char* file_name() const noexcept;
```

*Returns:* `file_name_`.

``` cpp
constexpr const char* function_name() const noexcept;
```

*Returns:* `function_name_`.

## Exception handling <a id="support.exception">[[support.exception]]</a>

### General <a id="support.exception.general">[[support.exception.general]]</a>

The header `<exception>` defines several types and functions related to
the handling of exceptions in a C++ program.

### Header `<exception>` synopsis <a id="exception.syn">[[exception.syn]]</a>

``` cpp
// all freestanding
namespace std {
  class exception;
  class bad_exception;
  class nested_exception;

  using terminate_handler = void (*)();
  terminate_handler get_terminate() noexcept;
  terminate_handler set_terminate(terminate_handler f) noexcept;
  [[noreturn]] void terminate() noexcept;

  int uncaught_exceptions() noexcept;

  using exception_ptr = unspecified;

  exception_ptr current_exception() noexcept;
  [[noreturn]] void rethrow_exception(exception_ptr p);
  template<class E> exception_ptr make_exception_ptr(E e) noexcept;

  template<class T> [[noreturn]] void throw_with_nested(T&& t);
  template<class E> void rethrow_if_nested(const E& e);
}
```

### Class `exception` <a id="exception">[[exception]]</a>

``` cpp
namespace std {
  class exception {
  public:
    exception() noexcept;
    exception(const exception&) noexcept;
    exception& operator=(const exception&) noexcept;
    virtual ~exception();
    virtual const char* what() const noexcept;
  };
}
```

The class `exception` defines the base class for the types of objects
thrown as exceptions by C++ standard library components, and certain
expressions, to report errors detected during program execution.

Each standard library class `T` that derives from class `exception` has
the following publicly accessible member functions, each of them having
a non-throwing exception specification [[except.spec]]:

- default constructor (unless the class synopsis shows other
  constructors)
- copy constructor
- copy assignment operator

The copy constructor and the copy assignment operator meet the following
postcondition: If two objects `lhs` and `rhs` both have dynamic type `T`
and `lhs` is a copy of `rhs`, then `strcmp(lhs.what(), rhs.what())` is
equal to `0`. The `what()` member function of each such `T` satisfies
the constraints specified for `exception::what()` (see below).

``` cpp
exception(const exception& rhs) noexcept;
exception& operator=(const exception& rhs) noexcept;
```

*Ensures:* If `*this` and `rhs` both have dynamic type `exception` then
the value of the expression `strcmp(what(), rhs.what())` shall equal 0.

``` cpp
virtual ~exception();
```

*Effects:* Destroys an object of class `exception`.

``` cpp
virtual const char* what() const noexcept;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string [[multibyte.strings]], suitable for conversion and display as a
`wstring`[[string.classes,locale.codecvt]]. The return value remains
valid until the exception object from which it is obtained is destroyed
or a non-`const` member function of the exception object is called.

### Class `bad_exception` <a id="bad.exception">[[bad.exception]]</a>

``` cpp
namespace std {
  class bad_exception : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

The class `bad_exception` defines the type of the object referenced by
the `exception_ptr` returned from a call to `current_exception`
[[propagation]] when the currently active exception object fails to
copy.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Abnormal termination <a id="exception.terminate">[[exception.terminate]]</a>

#### Type `terminate_handler` <a id="terminate.handler">[[terminate.handler]]</a>

``` cpp
using terminate_handler = void (*)();
```

The type of a *handler function* to be invoked by `terminate` when
terminating exception processing.

*Required behavior:* A `terminate_handler` shall terminate execution of
the program without returning to the caller.

*Default behavior:* The implementation’s default `terminate_handler`
calls `abort()`.

#### `set_terminate` <a id="set.terminate">[[set.terminate]]</a>

``` cpp
terminate_handler set_terminate(terminate_handler f) noexcept;
```

*Effects:* Establishes the function designated by `f` as the current
handler function for terminating exception processing.

*Returns:* The previous `terminate_handler`.

*Remarks:* It is unspecified whether a null pointer value designates the
default `terminate_handler`.

#### `get_terminate` <a id="get.terminate">[[get.terminate]]</a>

``` cpp
terminate_handler get_terminate() noexcept;
```

*Returns:* The current `terminate_handler`.

\[*Note 1*: This can be a null pointer value. — *end note*\]

#### `terminate` <a id="terminate">[[terminate]]</a>

``` cpp
[[noreturn]] void terminate() noexcept;
```

*Effects:* Calls a `terminate_handler` function. It is unspecified which
`terminate_handler` function will be called if an exception is active
during a call to `set_terminate`. Otherwise calls the current
`terminate_handler` function.

\[*Note 1*: A default `terminate_handler` is always considered a
callable handler in this context. — *end note*\]

*Remarks:* Called by the implementation when exception handling must be
abandoned for any of several reasons [[except.terminate]]. May also be
called directly by the program.

### `uncaught_exceptions` <a id="uncaught.exceptions">[[uncaught.exceptions]]</a>

``` cpp
int uncaught_exceptions() noexcept;
```

*Returns:* The number of uncaught exceptions [[except.uncaught]].

*Remarks:* When `uncaught_exceptions() > 0`, throwing an exception can
result in a call of the function `std::terminate`[[except.terminate]].

### Exception propagation <a id="propagation">[[propagation]]</a>

``` cpp
using exception_ptr = unspecified;
```

The type `exception_ptr` can be used to refer to an exception object.

`exception_ptr` meets the requirements of *Cpp17NullablePointer*
( [[cpp17.nullablepointer]]).

Two non-null values of type `exception_ptr` are equivalent and compare
equal if and only if they refer to the same exception.

The default constructor of `exception_ptr` produces the null value of
the type.

`exception_ptr` shall not be implicitly convertible to any arithmetic,
enumeration, or pointer type.

\[*Note 1*: An implementation can use a reference-counted smart pointer
as `exception_ptr`. — *end note*\]

For purposes of determining the presence of a data race, operations on
`exception_ptr` objects shall access and modify only the `exception_ptr`
objects themselves and not the exceptions they refer to. Use of
`rethrow_exception` on `exception_ptr` objects that refer to the same
exception object shall not introduce a data race.

\[*Note 2*: If `rethrow_exception` rethrows the same exception object
(rather than a copy), concurrent access to that rethrown exception
object can introduce a data race. Changes in the number of
`exception_ptr` objects that refer to a particular exception do not
introduce a data race. — *end note*\]

``` cpp
exception_ptr current_exception() noexcept;
```

*Returns:* An `exception_ptr` object that refers to the currently
handled exception [[except.handle]] or a copy of the currently handled
exception, or a null `exception_ptr` object if no exception is being
handled. The referenced object shall remain valid at least as long as
there is an `exception_ptr` object that refers to it. If the function
needs to allocate memory and the attempt fails, it returns an
`exception_ptr` object that refers to an instance of `bad_alloc`. It is
unspecified whether the return values of two successive calls to
`current_exception` refer to the same exception object.

\[*Note 3*: That is, it is unspecified whether `current_exception`
creates a new copy each time it is called. — *end note*\]

If the attempt to copy the current exception object throws an exception,
the function returns an `exception_ptr` object that refers to the thrown
exception or, if this is not possible, to an instance of
`bad_exception`.

\[*Note 4*: The copy constructor of the thrown exception can also fail,
so the implementation is allowed to substitute a `bad_exception` object
to avoid infinite recursion. — *end note*\]

``` cpp
[[noreturn]] void rethrow_exception(exception_ptr p);
```

*Preconditions:* `p` is not a null pointer.

*Effects:* Let u be the exception object to which `p` refers, or a copy
of that exception object. It is unspecified whether a copy is made, and
memory for the copy is allocated in an unspecified way.

- If allocating memory to form u fails, throws an instance of
  `bad_alloc`;
- otherwise, if copying the exception to which `p` refers to form u
  throws an exception, throws that exception;
- otherwise, throws u.

``` cpp
template<class E> exception_ptr make_exception_ptr(E e) noexcept;
```

*Effects:* Creates an `exception_ptr` object that refers to a copy of
`e`, as if:

``` cpp
try {
  throw e;
} catch(...) {
  return current_exception();
}
```

\[*Note 5*: This function is provided for convenience and efficiency
reasons. — *end note*\]

### `nested_exception` <a id="except.nested">[[except.nested]]</a>

``` cpp
namespace std {
  class nested_exception {
  public:
    nested_exception() noexcept;
    nested_exception(const nested_exception&) noexcept = default;
    nested_exception& operator=(const nested_exception&) noexcept = default;
    virtual ~nested_exception() = default;

    // access functions
    [[noreturn]] void rethrow_nested() const;
    exception_ptr nested_ptr() const noexcept;
  };

  template<class T> [[noreturn]] void throw_with_nested(T&& t);
  template<class E> void rethrow_if_nested(const E& e);
}
```

The class `nested_exception` is designed for use as a mixin through
multiple inheritance. It captures the currently handled exception and
stores it for later use.

\[*Note 1*: `nested_exception` has a virtual destructor to make it a
polymorphic class. Its presence can be tested for with
`dynamic_cast`. — *end note*\]

``` cpp
nested_exception() noexcept;
```

*Effects:* The constructor calls `current_exception()` and stores the
returned value.

``` cpp
[[noreturn]] void rethrow_nested() const;
```

*Effects:* If `nested_ptr()` returns a null pointer, the function calls
the function `std::terminate`. Otherwise, it throws the stored exception
captured by `*this`.

``` cpp
exception_ptr nested_ptr() const noexcept;
```

*Returns:* The stored exception captured by this `nested_exception`
object.

``` cpp
template<class T> [[noreturn]] void throw_with_nested(T&& t);
```

Let `U` be `decay_t<T>`.

*Preconditions:* `U` meets the *Cpp17CopyConstructible* requirements.

*Throws:* If
`is_class_v<U> && !is_final_v<U> && !is_base_of_v<nested_exception, U>`
is `true`, an exception of unspecified type that is publicly derived
from both `U` and `nested_exception` and constructed from
`std::forward<T>(t)`, otherwise `std::forward<T>(t)`.

``` cpp
template<class E> void rethrow_if_nested(const E& e);
```

*Effects:* If `E` is not a polymorphic class type, or if
`nested_exception` is an inaccessible or ambiguous base class of `E`,
there is no effect. Otherwise, performs:

``` cpp
if (auto p = dynamic_cast<const nested_exception*>(addressof(e)))
  p->rethrow_nested();
```

## Initializer lists <a id="support.initlist">[[support.initlist]]</a>

### General <a id="support.initlist.general">[[support.initlist.general]]</a>

The header `<initializer_list>` defines a class template and several
support functions related to list-initialization (see
[[dcl.init.list]]). All functions specified in [[support.initlist]] are
signal-safe [[support.signal]].

### Header `<initializer_list>` synopsis <a id="initializer.list.syn">[[initializer.list.syn]]</a>

``` cpp
// all freestanding
namespace std {
  template<class E> class initializer_list {
  public:
    using value_type      = E;
    using reference       = const E&;
    using const_reference = const E&;
    using size_type       = size_t;

    using iterator        = const E*;
    using const_iterator  = const E*;

    constexpr initializer_list() noexcept;

    constexpr size_t size() const noexcept;     // number of elements
    constexpr const E* begin() const noexcept;  // first element
    constexpr const E* end() const noexcept;    // one past the last element
  };

  // [support.initlist.range], initializer list range access
  template<class E> constexpr const E* begin(initializer_list<E> il) noexcept;
  template<class E> constexpr const E* end(initializer_list<E> il) noexcept;
}
```

An object of type `initializer_list<E>` provides access to an array of
objects of type `const E`.

\[*Note 1*: A pair of pointers or a pointer plus a length would be
obvious representations for `initializer_list`. `initializer_list` is
used to implement initializer lists as specified in  [[dcl.init.list]].
Copying an initializer list does not copy the underlying
elements. — *end note*\]

If an explicit specialization or partial specialization of
`initializer_list` is declared, the program is ill-formed.

### Initializer list constructors <a id="support.initlist.cons">[[support.initlist.cons]]</a>

``` cpp
constexpr initializer_list() noexcept;
```

*Ensures:* `size() == 0`.

### Initializer list access <a id="support.initlist.access">[[support.initlist.access]]</a>

``` cpp
constexpr const E* begin() const noexcept;
```

*Returns:* A pointer to the beginning of the array. If `size() == 0` the
values of `begin()` and `end()` are unspecified but they shall be
identical.

``` cpp
constexpr const E* end() const noexcept;
```

*Returns:* `begin() + size()`.

``` cpp
constexpr size_t size() const noexcept;
```

*Returns:* The number of elements in the array.

*Complexity:* Constant time.

### Initializer list range access <a id="support.initlist.range">[[support.initlist.range]]</a>

``` cpp
template<class E> constexpr const E* begin(initializer_list<E> il) noexcept;
```

*Returns:* `il.begin()`.

``` cpp
template<class E> constexpr const E* end(initializer_list<E> il) noexcept;
```

*Returns:* `il.end()`.

## Comparisons <a id="cmp">[[cmp]]</a>

### Header `<compare>` synopsis <a id="compare.syn">[[compare.syn]]</a>

The header `<compare>` specifies types, objects, and functions for use
primarily in connection with the three-way comparison operator
[[expr.spaceship]].

``` cpp
// all freestanding
namespace std {
  // [cmp.categories], comparison category types
  class partial_ordering;
  class weak_ordering;
  class strong_ordering;

  // named comparison functions
  constexpr bool is_eq  (partial_ordering cmp) noexcept { return cmp == 0; }
  constexpr bool is_neq (partial_ordering cmp) noexcept { return cmp != 0; }
  constexpr bool is_lt  (partial_ordering cmp) noexcept { return cmp < 0; }
  constexpr bool is_lteq(partial_ordering cmp) noexcept { return cmp <= 0; }
  constexpr bool is_gt  (partial_ordering cmp) noexcept { return cmp > 0; }
  constexpr bool is_gteq(partial_ordering cmp) noexcept { return cmp >= 0; }

  // [cmp.common], common comparison category type
  template<class... Ts>
  struct common_comparison_category {
    using type = see below;
  };
  template<class... Ts>
    using common_comparison_category_t = typename common_comparison_category<Ts...>::type;

  // [cmp.concept], concept three_way_comparable
  template<class T, class Cat = partial_ordering>
    concept three_way_comparable = see below;
  template<class T, class U, class Cat = partial_ordering>
    concept three_way_comparable_with = see below;

  // [cmp.result], result of three-way comparison
  template<class T, class U = T> struct compare_three_way_result;

  template<class T, class U = T>
    using compare_three_way_result_t = typename compare_three_way_result<T, U>::type;

  // [comparisons.three.way], class compare_three_way
  struct compare_three_way;

  // [cmp.alg], comparison algorithms
  inline namespace unspecified {
    inline constexpr unspecified strong_order = unspecified;
    inline constexpr unspecified weak_order = unspecified;
    inline constexpr unspecified partial_order = unspecified;
    inline constexpr unspecified compare_strong_order_fallback = unspecified;
    inline constexpr unspecified compare_weak_order_fallback = unspecified;
    inline constexpr unspecified compare_partial_order_fallback = unspecified;
  }
}
```

### Comparison category types <a id="cmp.categories">[[cmp.categories]]</a>

#### Preamble <a id="cmp.categories.pre">[[cmp.categories.pre]]</a>

The types `partial_ordering`, `weak_ordering`, and `strong_ordering` are
collectively termed the *comparison category types*. Each is specified
in terms of an exposition-only data member named `value` whose value
typically corresponds to that of an enumerator from one of the following
exposition-only enumerations:

``` cpp
enum class ord { equal = 0, equivalent = equal, less = -1, greater = 1 }; // exposition only
enum class ncmp { unordered = -127 };                                     // exposition only
```

\[*Note 1*: The type `strong_ordering` corresponds to the term total
ordering in mathematics. — *end note*\]

The relational and equality operators for the comparison category types
are specified with an anonymous parameter of unspecified type. This type
shall be selected by the implementation such that these parameters can
accept literal `0` as a corresponding argument.

\[*Example 1*:

`nullptr_t`

meets this requirement.

— *end example*\]

In this context, the behavior of a program that supplies an argument
other than a literal `0` is undefined.

For the purposes of subclause [[cmp.categories]], *substitutability* is
the property that `f(a) == f(b)` is `true` whenever `a == b` is `true`,
where `f` denotes a function that reads only comparison-salient state
that is accessible via the argument’s public const members.

#### Class `partial_ordering` <a id="cmp.partialord">[[cmp.partialord]]</a>

The `partial_ordering` type is typically used as the result type of a
three-way comparison operator [[expr.spaceship]] for a type that admits
all of the six two-way comparison operators [[expr.rel]], [[expr.eq]],
for which equality need not imply substitutability, and that permits two
values to be incomparable.[^32]

``` cpp
namespace std {
  class partial_ordering {
    int value;          // exposition only
    bool is_ordered;    // exposition only

    // exposition-only constructors
    constexpr explicit
      partial_ordering(ord v) noexcept : value(int(v)), is_ordered(true) {}     // exposition only
    constexpr explicit
      partial_ordering(ncmp v) noexcept : value(int(v)), is_ordered(false) {}   // exposition only

  public:
    // valid values
    static const partial_ordering less;
    static const partial_ordering equivalent;
    static const partial_ordering greater;
    static const partial_ordering unordered;

    // comparisons
    friend constexpr bool operator==(partial_ordering v, unspecified) noexcept;
    friend constexpr bool operator==(partial_ordering v, partial_ordering w) noexcept = default;
    friend constexpr bool operator< (partial_ordering v, unspecified) noexcept;
    friend constexpr bool operator> (partial_ordering v, unspecified) noexcept;
    friend constexpr bool operator<=(partial_ordering v, unspecified) noexcept;
    friend constexpr bool operator>=(partial_ordering v, unspecified) noexcept;
    friend constexpr bool operator< (unspecified, partial_ordering v) noexcept;
    friend constexpr bool operator> (unspecified, partial_ordering v) noexcept;
    friend constexpr bool operator<=(unspecified, partial_ordering v) noexcept;
    friend constexpr bool operator>=(unspecified, partial_ordering v) noexcept;
    friend constexpr partial_ordering operator<=>(partial_ordering v, unspecified) noexcept;
    friend constexpr partial_ordering operator<=>(unspecified, partial_ordering v) noexcept;
  };

  // valid values' definitions
  inline constexpr partial_ordering partial_ordering::less(ord::less);
  inline constexpr partial_ordering partial_ordering::equivalent(ord::equivalent);
  inline constexpr partial_ordering partial_ordering::greater(ord::greater);
  inline constexpr partial_ordering partial_ordering::unordered(ncmp::unordered);
}
```

``` cpp
constexpr bool operator==(partial_ordering v, unspecified) noexcept;
constexpr bool operator< (partial_ordering v, unspecified) noexcept;
constexpr bool operator> (partial_ordering v, unspecified) noexcept;
constexpr bool operator<=(partial_ordering v, unspecified) noexcept;
constexpr bool operator>=(partial_ordering v, unspecified) noexcept;
```

*Returns:* For `operator`, `v.is_ordered && v.value 0`.

``` cpp
constexpr bool operator< (unspecified, partial_ordering v) noexcept;
constexpr bool operator> (unspecified, partial_ordering v) noexcept;
constexpr bool operator<=(unspecified, partial_ordering v) noexcept;
constexpr bool operator>=(unspecified, partial_ordering v) noexcept;
```

*Returns:* For `operator`, `v.is_ordered && 0 v.value`.

``` cpp
constexpr partial_ordering operator<=>(partial_ordering v, unspecified) noexcept;
```

*Returns:* `v`.

``` cpp
constexpr partial_ordering operator<=>(unspecified, partial_ordering v) noexcept;
```

*Returns:*
`v < 0 ? partial_ordering::greater : v > 0 ? partial_ordering::less : v`.

#### Class `weak_ordering` <a id="cmp.weakord">[[cmp.weakord]]</a>

The `weak_ordering` type is typically used as the result type of a
three-way comparison operator [[expr.spaceship]] for a type that admits
all of the six two-way comparison operators [[expr.rel]], [[expr.eq]]
and for which equality need not imply substitutability.

``` cpp
namespace std {
  class weak_ordering {
    int value;  // exposition only

    // exposition-only constructors
    constexpr explicit weak_ordering(ord v) noexcept : value(int(v)) {} // exposition only

  public:
    // valid values
    static const weak_ordering less;
    static const weak_ordering equivalent;
    static const weak_ordering greater;

    // conversions
    constexpr operator partial_ordering() const noexcept;

    // comparisons
    friend constexpr bool operator==(weak_ordering v, unspecified) noexcept;
    friend constexpr bool operator==(weak_ordering v, weak_ordering w) noexcept = default;
    friend constexpr bool operator< (weak_ordering v, unspecified) noexcept;
    friend constexpr bool operator> (weak_ordering v, unspecified) noexcept;
    friend constexpr bool operator<=(weak_ordering v, unspecified) noexcept;
    friend constexpr bool operator>=(weak_ordering v, unspecified) noexcept;
    friend constexpr bool operator< (unspecified, weak_ordering v) noexcept;
    friend constexpr bool operator> (unspecified, weak_ordering v) noexcept;
    friend constexpr bool operator<=(unspecified, weak_ordering v) noexcept;
    friend constexpr bool operator>=(unspecified, weak_ordering v) noexcept;
    friend constexpr weak_ordering operator<=>(weak_ordering v, unspecified) noexcept;
    friend constexpr weak_ordering operator<=>(unspecified, weak_ordering v) noexcept;
  };

  // valid values' definitions
  inline constexpr weak_ordering weak_ordering::less(ord::less);
  inline constexpr weak_ordering weak_ordering::equivalent(ord::equivalent);
  inline constexpr weak_ordering weak_ordering::greater(ord::greater);
}
```

``` cpp
constexpr operator partial_ordering() const noexcept;
```

*Returns:*

``` cpp
value == 0 ? partial_ordering::equivalent :
value < 0  ? partial_ordering::less :
             partial_ordering::greater
```

``` cpp
constexpr bool operator==(weak_ordering v, unspecified) noexcept;
constexpr bool operator< (weak_ordering v, unspecified) noexcept;
constexpr bool operator> (weak_ordering v, unspecified) noexcept;
constexpr bool operator<=(weak_ordering v, unspecified) noexcept;
constexpr bool operator>=(weak_ordering v, unspecified) noexcept;
```

*Returns:* `v.value 0` for `operator`.

``` cpp
constexpr bool operator< (unspecified, weak_ordering v) noexcept;
constexpr bool operator> (unspecified, weak_ordering v) noexcept;
constexpr bool operator<=(unspecified, weak_ordering v) noexcept;
constexpr bool operator>=(unspecified, weak_ordering v) noexcept;
```

*Returns:* `0 v.value` for `operator`.

``` cpp
constexpr weak_ordering operator<=>(weak_ordering v, unspecified) noexcept;
```

*Returns:* `v`.

``` cpp
constexpr weak_ordering operator<=>(unspecified, weak_ordering v) noexcept;
```

*Returns:*
`v < 0 ? weak_ordering::greater : v > 0 ? weak_ordering::less : v`.

#### Class `strong_ordering` <a id="cmp.strongord">[[cmp.strongord]]</a>

The `strong_ordering` type is typically used as the result type of a
three-way comparison operator [[expr.spaceship]] for a type that admits
all of the six two-way comparison operators [[expr.rel]], [[expr.eq]]
and for which equality does imply substitutability.

``` cpp
namespace std {
  class strong_ordering {
    int value;  // exposition only

    // exposition-only constructors
    constexpr explicit strong_ordering(ord v) noexcept : value(int(v)) {}   // exposition only

  public:
    // valid values
    static const strong_ordering less;
    static const strong_ordering equal;
    static const strong_ordering equivalent;
    static const strong_ordering greater;

    // conversions
    constexpr operator partial_ordering() const noexcept;
    constexpr operator weak_ordering() const noexcept;

    // comparisons
    friend constexpr bool operator==(strong_ordering v, unspecified) noexcept;
    friend constexpr bool operator==(strong_ordering v, strong_ordering w) noexcept = default;
    friend constexpr bool operator< (strong_ordering v, unspecified) noexcept;
    friend constexpr bool operator> (strong_ordering v, unspecified) noexcept;
    friend constexpr bool operator<=(strong_ordering v, unspecified) noexcept;
    friend constexpr bool operator>=(strong_ordering v, unspecified) noexcept;
    friend constexpr bool operator< (unspecified, strong_ordering v) noexcept;
    friend constexpr bool operator> (unspecified, strong_ordering v) noexcept;
    friend constexpr bool operator<=(unspecified, strong_ordering v) noexcept;
    friend constexpr bool operator>=(unspecified, strong_ordering v) noexcept;
    friend constexpr strong_ordering operator<=>(strong_ordering v, unspecified) noexcept;
    friend constexpr strong_ordering operator<=>(unspecified, strong_ordering v) noexcept;
  };

  // valid values' definitions
  inline constexpr strong_ordering strong_ordering::less(ord::less);
  inline constexpr strong_ordering strong_ordering::equal(ord::equal);
  inline constexpr strong_ordering strong_ordering::equivalent(ord::equivalent);
  inline constexpr strong_ordering strong_ordering::greater(ord::greater);
}
```

``` cpp
constexpr operator partial_ordering() const noexcept;
```

*Returns:*

``` cpp
value == 0 ? partial_ordering::equivalent :
value < 0  ? partial_ordering::less :
             partial_ordering::greater
```

``` cpp
constexpr operator weak_ordering() const noexcept;
```

*Returns:*

``` cpp
value == 0 ? weak_ordering::equivalent :
value < 0  ? weak_ordering::less :
             weak_ordering::greater
```

``` cpp
constexpr bool operator==(strong_ordering v, unspecified) noexcept;
constexpr bool operator< (strong_ordering v, unspecified) noexcept;
constexpr bool operator> (strong_ordering v, unspecified) noexcept;
constexpr bool operator<=(strong_ordering v, unspecified) noexcept;
constexpr bool operator>=(strong_ordering v, unspecified) noexcept;
```

*Returns:* `v.value 0` for `operator`.

``` cpp
constexpr bool operator< (unspecified, strong_ordering v) noexcept;
constexpr bool operator> (unspecified, strong_ordering v) noexcept;
constexpr bool operator<=(unspecified, strong_ordering v) noexcept;
constexpr bool operator>=(unspecified, strong_ordering v) noexcept;
```

*Returns:* `0 v.value` for `operator`.

``` cpp
constexpr strong_ordering operator<=>(strong_ordering v, unspecified) noexcept;
```

*Returns:* `v`.

``` cpp
constexpr strong_ordering operator<=>(unspecified, strong_ordering v) noexcept;
```

*Returns:*
`v < 0 ? strong_ordering::greater : v > 0 ? strong_ordering::less : v`.

### Class template `common_comparison_category` <a id="cmp.common">[[cmp.common]]</a>

The type `common_comparison_category` provides an alias for the
strongest comparison category to which all of the template arguments can
be converted.

\[*Note 1*: A comparison category type is stronger than another if they
are distinct types and an instance of the former can be converted to an
instance of the latter. — *end note*\]

``` cpp
template<class... Ts>
struct common_comparison_category {
  using type = see below;
};
```

*Remarks:* The member *typedef-name* `type` denotes the common
comparison type [[class.spaceship]] of `Ts...`, the expanded parameter
pack, or `void` if any element of `Ts` is not a comparison category
type.

\[*Note 1*: This is `std::strong_ordering` if the expansion is
empty. — *end note*\]

### Concept  <a id="cmp.concept">[[cmp.concept]]</a>

``` cpp
template<class T, class Cat>
  concept compares-as =                 // exposition only
    same_as<common_comparison_category_t<T, Cat>, Cat>;

template<class T, class U>
  concept partially-ordered-with =      // exposition only
    requires(const remove_reference_t<T>& t, const remove_reference_t<U>& u) {
      { t <  u } -> boolean-testable;
      { t >  u } -> boolean-testable;
      { t <= u } -> boolean-testable;
      { t >= u } -> boolean-testable;
      { u <  t } -> boolean-testable;
      { u >  t } -> boolean-testable;
      { u <= t } -> boolean-testable;
      { u >= t } -> boolean-testable;
    };
```

Let `t` and `u` be lvalues of types `const remove_reference_t<T>` and
`const remove_reference_t<U>`, respectively. `T` and `U` model
`partially-ordered-with<T, U>` only if:

- `t < u`, `t <= u`, `t > u`, `t >= u`, `u < t`, `u <= t`, `u > t`, and
  `u >= t` have the same domain.
- `bool(t < u) == bool(u > t)` is `true`,
- `bool(u < t) == bool(t > u)` is `true`,
- `bool(t <= u) == bool(u >= t)` is `true`, and
- `bool(u <= t) == bool(t >= u)` is `true`.

``` cpp
template<class T, class Cat = partial_ordering>
  concept three_way_comparable =
    weakly-equality-comparable-with<T, T> &&
    partially-ordered-with<T, T> &&
    requires(const remove_reference_t<T>& a, const remove_reference_t<T>& b) {
      { a <=> b } -> compares-as<Cat>;
    };
```

Let `a` and `b` be lvalues of type `const remove_reference_t<T>`. `T`
and `Cat` model `three_way_comparable<T, Cat>` only if:

- `(a <=> b == 0) == bool(a == b)` is `true`,
- `(a <=> b != 0) == bool(a != b)` is `true`,
- `((a <=> b) <=> 0)` and `(0 <=> (b <=> a))` are equal,
- `(a <=> b < 0) == bool(a < b)` is `true`,
- `(a <=> b > 0) == bool(a > b)` is `true`,
- `(a <=> b <= 0) == bool(a <= b)` is `true`,
- `(a <=> b >= 0) == bool(a >= b)` is `true`, and
- if `Cat` is convertible to `strong_ordering`, `T` models
  `totally_ordered` [[concept.totallyordered]].

``` cpp
template<class T, class U, class Cat = partial_ordering>
  concept three_way_comparable_with =
    three_way_comparable<T, Cat> &&
    three_way_comparable<U, Cat> &&
    comparison-common-type-with<T, U> &&
    three_way_comparable<
      common_reference_t<const remove_reference_t<T>&, const remove_reference_t<U>&>, Cat> &&
    weakly-equality-comparable-with<T, U> &&
    partially-ordered-with<T, U> &&
    requires(const remove_reference_t<T>& t, const remove_reference_t<U>& u) {
      { t <=> u } -> compares-as<Cat>;
      { u <=> t } -> compares-as<Cat>;
    };
```

Let `t` and `t2` be lvalues denoting distinct equal objects of types
`const remove_reference_t<T>` and `remove_cvref_t<T>`, respectively, and
let `u` and `u2` be lvalues denoting distinct equal objects of types
`const remove_reference_t<U>` and `remove_cvref_t<U>`, respectively. Let
`C` be
`common_reference_t<const remove_reference_t<T>&, const remove_reference_t<U>&>`.
Let `CONVERT_TO_LVALUE<C>(E)` be defined as in
[[concepts.compare.general]]. `T`, `U`, and `Cat` model
`three_way_comparable_with<T, U, Cat>` only if:

- `t <=> u` and `u <=> t` have the same domain,
- `((t <=> u) <=> 0)` and `(0 <=> (u <=> t))` are equal,
- `(t <=> u == 0) == bool(t == u)` is `true`,
- `(t <=> u != 0) == bool(t != u)` is `true`,
- `Cat(t <=> u) == Cat(CONVERT_TO_LVALUE<C>(t2) <=>
  CONVERT_TO_LVALUE<C>(u2))` is `true`,
- `(t <=> u < 0) == bool(t < u)` is `true`,
- `(t <=> u > 0) == bool(t > u)` is `true`,
- `(t <=> u <= 0) == bool(t <= u)` is `true`,
- `(t <=> u >= 0) == bool(t >= u)` is `true`, and
- if `Cat` is convertible to `strong_ordering`, `T` and `U` model
  `totally_ordered_with<T, U>` [[concept.totallyordered]].

### Result of three-way comparison <a id="cmp.result">[[cmp.result]]</a>

The behavior of a program that adds specializations for the
`compare_three_way_result` template defined in this subclause is
undefined.

For the `compare_three_way_result` type trait applied to the types `T`
and `U`, let `t` and `u` denote lvalues of types
`const remove_reference_t<T>` and `const remove_reference_t<U>`,
respectively. If the expression `t <=> u` is well-formed when treated as
an unevaluated operand [[expr.context]], the member *typedef-name*
`type` denotes the type `decltype(t <=> u)`. Otherwise, there is no
member `type`.

### Comparison algorithms <a id="cmp.alg">[[cmp.alg]]</a>

The name `strong_order` denotes a customization point object
[[customization.point.object]]. Given subexpressions `E` and `F`, the
expression `strong_order(E, F)` is expression-equivalent
[[defns.expression.equivalent]] to the following:

- If the decayed types of `E` and `F` differ, `strong_order(E, F)` is
  ill-formed.
- Otherwise, `strong_ordering(strong_order(E, F))` if it is a
  well-formed expression where the meaning of `strong_order` is
  established as-if by performing argument-dependent lookup only
  [[basic.lookup.argdep]].
- Otherwise, if the decayed type `T` of `E` is a floating-point type,
  yields a value of type `strong_ordering` that is consistent with the
  ordering observed by `T`’s comparison operators, and if
  `numeric_limits<T>::is_iec559` is `true`, is additionally consistent
  with the `totalOrder` operation as specified in ISO/IEC/IEEE 60559.
- Otherwise, `strong_ordering(compare_three_way()(E, F))` if it is a
  well-formed expression.
- Otherwise, `strong_order(E, F)` is ill-formed.

\[*Note 1*: Ill-formed cases above result in substitution failure when
`strong_order(E, F)` appears in the immediate context of a template
instantiation. — *end note*\]

The name `weak_order` denotes a customization point object
[[customization.point.object]]. Given subexpressions `E` and `F`, the
expression `weak_order(E, F)` is expression-equivalent
[[defns.expression.equivalent]] to the following:

- If the decayed types of `E` and `F` differ, `weak_order(E, F)` is
  ill-formed.
- Otherwise, `weak_ordering(weak_order(E, F))` if it is a well-formed
  expression where the meaning of `weak_order` is established as-if by
  performing argument-dependent lookup only [[basic.lookup.argdep]].
- Otherwise, if the decayed type `T` of `E` is a floating-point type,
  yields a value of type `weak_ordering` that is consistent with the
  ordering observed by `T`’s comparison operators and `strong_order`,
  and if `numeric_limits<T>::is_iec559` is `true`, is additionally
  consistent with the following equivalence classes, ordered from lesser
  to greater:
  - together, all negative NaN values;
  - negative infinity;
  - each normal negative value;
  - each subnormal negative value;
  - together, both zero values;
  - each subnormal positive value;
  - each normal positive value;
  - positive infinity;
  - together, all positive NaN values.
- Otherwise, `weak_ordering(compare_three_way()(E, F))` if it is a
  well-formed expression.
- Otherwise, `weak_ordering(strong_order(E, F))` if it is a well-formed
  expression.
- Otherwise, `weak_order(E, F)` is ill-formed.

\[*Note 2*: Ill-formed cases above result in substitution failure when
`weak_order(E, F)` appears in the immediate context of a template
instantiation. — *end note*\]

The name `partial_order` denotes a customization point object
[[customization.point.object]]. Given subexpressions `E` and `F`, the
expression `partial_order(E, F)` is expression-equivalent
[[defns.expression.equivalent]] to the following:

- If the decayed types of `E` and `F` differ, `partial_order(E, F)` is
  ill-formed.
- Otherwise, `partial_ordering(partial_order(E, F))` if it is a
  well-formed expression where the meaning of `partial_order` is
  established as-if by performing argument-dependent lookup only
  [[basic.lookup.argdep]].
- Otherwise, `partial_ordering(compare_three_way()(E, F))` if it is a
  well-formed expression.
- Otherwise, `partial_ordering(weak_order(E, F))` if it is a well-formed
  expression.
- Otherwise, `partial_order(E, F)` is ill-formed.

\[*Note 3*: Ill-formed cases above result in substitution failure when
`partial_order(E, F)` appears in the immediate context of a template
instantiation. — *end note*\]

The name `compare_strong_order_fallback` denotes a customization point
object [[customization.point.object]]. Given subexpressions `E` and `F`,
the expression `compare_strong_order_fallback(E, F)` is
expression-equivalent [[defns.expression.equivalent]] to:

- If the decayed types of `E` and `F` differ,
  `compare_strong_order_fallback(E, F)` is ill-formed.
- Otherwise, `strong_order(E, F)` if it is a well-formed expression.
- Otherwise, if the expressions `E == F` and `E < F` are both
  well-formed and each of `decltype(E == F)` and `decltype(E < F)`
  models `boolean-testable`,
  ``` cpp
  E == F ? strong_ordering::equal :
  E < F  ? strong_ordering::less :
           strong_ordering::greater
  ```

  except that `E` and `F` are evaluated only once.
- Otherwise, `compare_strong_order_fallback(E, F)` is ill-formed.

\[*Note 4*: Ill-formed cases above result in substitution failure when
`compare_strong_order_fallback(E, F)` appears in the immediate context
of a template instantiation. — *end note*\]

The name `compare_weak_order_fallback` denotes a customization point
object [[customization.point.object]]. Given subexpressions `E` and `F`,
the expression `compare_weak_order_fallback(E, F)` is
expression-equivalent [[defns.expression.equivalent]] to:

- If the decayed types of `E` and `F` differ,
  `compare_weak_order_fallback(E, F)` is ill-formed.
- Otherwise, `weak_order(E, F)` if it is a well-formed expression.
- Otherwise, if the expressions `E == F` and `E < F` are both
  well-formed and each of `decltype(E == F)` and `decltype(E < F)`
  models `boolean-testable`,
  ``` cpp
  E == F ? weak_ordering::equivalent :
  E < F  ? weak_ordering::less :
           weak_ordering::greater
  ```

  except that `E` and `F` are evaluated only once.
- Otherwise, `compare_weak_order_fallback(E, F)` is ill-formed.

\[*Note 5*: Ill-formed cases above result in substitution failure when
`compare_weak_order_fallback(E, F)` appears in the immediate context of
a template instantiation. — *end note*\]

The name `compare_partial_order_fallback` denotes a customization point
object [[customization.point.object]]. Given subexpressions `E` and `F`,
the expression `compare_partial_order_fallback(E, F)` is
expression-equivalent [[defns.expression.equivalent]] to:

- If the decayed types of `E` and `F` differ,
  `compare_partial_order_fallback(E, F)` is ill-formed.
- Otherwise, `partial_order(E, F)` if it is a well-formed expression.
- Otherwise, if the expressions `E == F`, `E < F`, and `F < E` are all
  well-formed and each of `decltype(E == F)` and `decltype(E < F)`
  models `boolean-testable`,
  ``` cpp
  E == F ? partial_ordering::equivalent :
  E < F  ? partial_ordering::less :
  F < E  ? partial_ordering::greater :
           partial_ordering::unordered
  ```

  except that `E` and `F` are evaluated only once.
- Otherwise, `compare_partial_order_fallback(E, F)` is ill-formed.

\[*Note 6*: Ill-formed cases above result in substitution failure when
`compare_partial_order_fallback(E, F)` appears in the immediate context
of a template instantiation. — *end note*\]

## Coroutines <a id="support.coroutine">[[support.coroutine]]</a>

### General <a id="support.coroutine.general">[[support.coroutine.general]]</a>

The header `<coroutine>` defines several types providing compile and
run-time support for coroutines in a C++ program.

### Header `<coroutine>` synopsis <a id="coroutine.syn">[[coroutine.syn]]</a>

``` cpp
// all freestanding
#include <compare>              // see [compare.syn]

namespace std {
  // [coroutine.traits], coroutine traits
  template<class R, class... ArgTypes>
    struct coroutine_traits;

  // [coroutine.handle], coroutine handle
  template<class Promise = void>
    struct coroutine_handle;

  // [coroutine.handle.compare], comparison operators
  constexpr bool operator==(coroutine_handle<> x, coroutine_handle<> y) noexcept;
  constexpr strong_ordering operator<=>(coroutine_handle<> x, coroutine_handle<> y) noexcept;

  // [coroutine.handle.hash], hash support
  template<class T> struct hash;
  template<class P> struct hash<coroutine_handle<P>>;

  // [coroutine.noop], no-op coroutines
  struct noop_coroutine_promise;

  template<> struct coroutine_handle<noop_coroutine_promise>;
  using noop_coroutine_handle = coroutine_handle<noop_coroutine_promise>;

  noop_coroutine_handle noop_coroutine() noexcept;

  // [coroutine.trivial.awaitables], trivial awaitables
  struct suspend_never;
  struct suspend_always;
}
```

### Coroutine traits <a id="coroutine.traits">[[coroutine.traits]]</a>

#### General <a id="coroutine.traits.general">[[coroutine.traits.general]]</a>

Subclause [[coroutine.traits]] defines requirements on classes
representing *coroutine traits*, and defines the class template
`coroutine_traits` that meets those requirements.

#### Class template `coroutine_traits` <a id="coroutine.traits.primary">[[coroutine.traits.primary]]</a>

The header `<coroutine>` defines the primary template `coroutine_traits`
such that if `ArgTypes` is a parameter pack of types and if the
*qualified-id* `R::promise_type` is valid and denotes a type
[[temp.deduct]], then `coroutine_traits<R, ArgTypes...>` has the
following publicly accessible member:

``` cpp
using promise_type = typename R::promise_type;
```

Otherwise, `coroutine_traits<R, ArgTypes...>` has no members.

Program-defined specializations of this template shall define a publicly
accessible nested type named `promise_type`.

### Class template `coroutine_handle` <a id="coroutine.handle">[[coroutine.handle]]</a>

#### General <a id="coroutine.handle.general">[[coroutine.handle.general]]</a>

``` cpp
namespace std {
  template<>
  struct coroutine_handle<void>
  {
    // [coroutine.handle.con], construct/reset
    constexpr coroutine_handle() noexcept;
    constexpr coroutine_handle(nullptr_t) noexcept;
    coroutine_handle& operator=(nullptr_t) noexcept;

    // [coroutine.handle.export.import], export/import
    constexpr void* address() const noexcept;
    static constexpr coroutine_handle from_address(void* addr);

    // [coroutine.handle.observers], observers
    constexpr explicit operator bool() const noexcept;
    bool done() const;

    // [coroutine.handle.resumption], resumption
    void operator()() const;
    void resume() const;
    void destroy() const;

  private:
    void* ptr;  // exposition only
  };

  template<class Promise>
  struct coroutine_handle
  {
    // [coroutine.handle.con], construct/reset
    constexpr coroutine_handle() noexcept;
    constexpr coroutine_handle(nullptr_t) noexcept;
    static coroutine_handle from_promise(Promise&);
    coroutine_handle& operator=(nullptr_t) noexcept;

    // [coroutine.handle.export.import], export/import
    constexpr void* address() const noexcept;
    static constexpr coroutine_handle from_address(void* addr);

    // [coroutine.handle.conv], conversion
    constexpr operator coroutine_handle<>() const noexcept;

    // [coroutine.handle.observers], observers
    constexpr explicit operator bool() const noexcept;
    bool done() const;

    // [coroutine.handle.resumption], resumption
    void operator()() const;
    void resume() const;
    void destroy() const;

    // [coroutine.handle.promise], promise access
    Promise& promise() const;

  private:
    void* ptr;  // exposition only
  };
}
```

An object of type `coroutine_handle<T>` is called a *coroutine handle*
and can be used to refer to a suspended or executing coroutine. A
`coroutine_handle` object whose member `address()` returns a null
pointer value does not refer to any coroutine. Two `coroutine_handle`
objects refer to the same coroutine if and only if their member
`address()` returns the same non-null value.

If a program declares an explicit or partial specialization of
`coroutine_handle`, the behavior is undefined.

#### Construct/reset <a id="coroutine.handle.con">[[coroutine.handle.con]]</a>

``` cpp
constexpr coroutine_handle() noexcept;
constexpr coroutine_handle(nullptr_t) noexcept;
```

*Ensures:* `address() == nullptr`.

``` cpp
static coroutine_handle from_promise(Promise& p);
```

*Preconditions:* `p` is a reference to a promise object of a coroutine.

*Ensures:* `addressof(h.promise()) == addressof(p)`.

*Returns:* A coroutine handle `h` referring to the coroutine.

``` cpp
coroutine_handle& operator=(nullptr_t) noexcept;
```

*Ensures:* `address() == nullptr`.

*Returns:* `*this`.

#### Conversion <a id="coroutine.handle.conv">[[coroutine.handle.conv]]</a>

``` cpp
constexpr operator coroutine_handle<>() const noexcept;
```

*Effects:* Equivalent to:
`return coroutine_handle<>::from_address(address());`

#### Export/import <a id="coroutine.handle.export.import">[[coroutine.handle.export.import]]</a>

``` cpp
constexpr void* address() const noexcept;
```

*Returns:* `ptr`.

``` cpp
static constexpr coroutine_handle<> coroutine_handle<>::from_address(void* addr);
```

*Preconditions:* `addr` was obtained via a prior call to `address` on an
object whose type is a specialization of `coroutine_handle`.

*Ensures:* `from_address(address()) == *this`.

``` cpp
static constexpr coroutine_handle<Promise> coroutine_handle<Promise>::from_address(void* addr);
```

*Preconditions:* `addr` was obtained via a prior call to `address` on an
object of type cv `coroutine_handle<Promise>`.

*Ensures:* `from_address(address()) == *this`.

#### Observers <a id="coroutine.handle.observers">[[coroutine.handle.observers]]</a>

``` cpp
constexpr explicit operator bool() const noexcept;
```

*Returns:* `address() != nullptr`.

``` cpp
bool done() const;
```

*Preconditions:* `*this` refers to a suspended coroutine.

*Returns:* `true` if the coroutine is suspended at its final suspend
point, otherwise `false`.

#### Resumption <a id="coroutine.handle.resumption">[[coroutine.handle.resumption]]</a>

Resuming a coroutine via `resume`, `operator()`, or `destroy` on an
execution agent other than the one on which it was suspended has
*implementation-defined* behavior unless each execution agent either is
an instance of `std::thread` or `std::jthread`, or is the thread that
executes `main`.

\[*Note 1*: A coroutine that is resumed on a different execution agent
should avoid relying on consistent thread identity throughout, such as
holding a mutex object across a suspend point. — *end note*\]

\[*Note 2*: A concurrent resumption of the coroutine can result in a
data race. — *end note*\]

``` cpp
void operator()() const;
void resume() const;
```

*Preconditions:* `*this` refers to a suspended coroutine. The coroutine
is not suspended at its final suspend point.

*Effects:* Resumes the execution of the coroutine.

``` cpp
void destroy() const;
```

*Preconditions:* `*this` refers to a suspended coroutine.

*Effects:* Destroys the coroutine [[dcl.fct.def.coroutine]].

#### Promise access <a id="coroutine.handle.promise">[[coroutine.handle.promise]]</a>

``` cpp
Promise& promise() const;
```

*Preconditions:* `*this` refers to a coroutine.

*Returns:* A reference to the promise of the coroutine.

#### Comparison operators <a id="coroutine.handle.compare">[[coroutine.handle.compare]]</a>

``` cpp
constexpr bool operator==(coroutine_handle<> x, coroutine_handle<> y) noexcept;
```

*Returns:* `x.address() == y.address()`.

``` cpp
constexpr strong_ordering operator<=>(coroutine_handle<> x, coroutine_handle<> y) noexcept;
```

*Returns:* `compare_three_way()(x.address(), y.address())`.

#### Hash support <a id="coroutine.handle.hash">[[coroutine.handle.hash]]</a>

``` cpp
template<class P> struct hash<coroutine_handle<P>>;
```

The specialization is enabled [[unord.hash]].

### No-op coroutines <a id="coroutine.noop">[[coroutine.noop]]</a>

#### Class `noop_coroutine_promise` <a id="coroutine.promise.noop">[[coroutine.promise.noop]]</a>

``` cpp
struct noop_coroutine_promise {};
```

The class `noop_coroutine_promise` defines the promise type for the
coroutine referred to by `noop_coroutine_handle`[[coroutine.syn]].

#### Class `coroutine_handle<noop_coroutine_promise>` <a id="coroutine.handle.noop">[[coroutine.handle.noop]]</a>

``` cpp
namespace std {
  template<>
  struct coroutine_handle<noop_coroutine_promise>
  {
    // [coroutine.handle.noop.conv], conversion
    constexpr operator coroutine_handle<>() const noexcept;

    // [coroutine.handle.noop.observers], observers
    constexpr explicit operator bool() const noexcept;
    constexpr bool done() const noexcept;

    // [coroutine.handle.noop.resumption], resumption
    constexpr void operator()() const noexcept;
    constexpr void resume() const noexcept;
    constexpr void destroy() const noexcept;

    // [coroutine.handle.noop.promise], promise access
    noop_coroutine_promise& promise() const noexcept;

    // [coroutine.handle.noop.address], address
    constexpr void* address() const noexcept;
  private:
    coroutine_handle(unspecified);
    void* ptr;  // exposition only
  };
}
```

##### Conversion <a id="coroutine.handle.noop.conv">[[coroutine.handle.noop.conv]]</a>

``` cpp
constexpr operator coroutine_handle<>() const noexcept;
```

*Effects:* Equivalent to:
`return coroutine_handle<>::from_address(address());`

##### Observers <a id="coroutine.handle.noop.observers">[[coroutine.handle.noop.observers]]</a>

``` cpp
constexpr explicit operator bool() const noexcept;
```

*Returns:* `true`.

``` cpp
constexpr bool done() const noexcept;
```

*Returns:* `false`.

##### Resumption <a id="coroutine.handle.noop.resumption">[[coroutine.handle.noop.resumption]]</a>

``` cpp
constexpr void operator()() const noexcept;
constexpr void resume() const noexcept;
constexpr void destroy() const noexcept;
```

*Effects:* None.

*Remarks:* If `noop_coroutine_handle` is converted to
`coroutine_handle<>`, calls to `operator()`, `resume` and `destroy` on
that handle will also have no observable effects.

##### Promise access <a id="coroutine.handle.noop.promise">[[coroutine.handle.noop.promise]]</a>

``` cpp
noop_coroutine_promise& promise() const noexcept;
```

*Returns:* A reference to the promise object associated with this
coroutine handle.

##### Address <a id="coroutine.handle.noop.address">[[coroutine.handle.noop.address]]</a>

``` cpp
constexpr void* address() const noexcept;
```

*Returns:* `ptr`.

*Remarks:* A `noop_coroutine_handle`’s `ptr` is always a non-null
pointer value.

#### Function `noop_coroutine` <a id="coroutine.noop.coroutine">[[coroutine.noop.coroutine]]</a>

``` cpp
noop_coroutine_handle noop_coroutine() noexcept;
```

*Returns:* A handle to a coroutine that has no observable effects when
resumed or destroyed.

*Remarks:* A handle returned from `noop_coroutine` may or may not
compare equal to a handle returned from another invocation of
`noop_coroutine`.

### Trivial awaitables <a id="coroutine.trivial.awaitables">[[coroutine.trivial.awaitables]]</a>

``` cpp
namespace std {
  struct suspend_never {
    constexpr bool await_ready() const noexcept { return true; }
    constexpr void await_suspend(coroutine_handle<>) const noexcept {}
    constexpr void await_resume() const noexcept {}
  };
  struct suspend_always {
    constexpr bool await_ready() const noexcept { return false; }
    constexpr void await_suspend(coroutine_handle<>) const noexcept {}
    constexpr void await_resume() const noexcept {}
  };
}
```

\[*Note 1*: The types `suspend_never` and `suspend_always` can be used
to indicate that an *await-expression* either never suspends or always
suspends, and in either case does not produce a value. — *end note*\]

## Other runtime support <a id="support.runtime">[[support.runtime]]</a>

### General <a id="support.runtime.general">[[support.runtime.general]]</a>

Headers `<csetjmp>` (nonlocal jumps), `<csignal>` (signal handling),
`<cstdarg>` (variable arguments), and `<cstdlib>` (runtime environment
`getenv`, `system`), provide further compatibility with C code.

Calls to the function `getenv` [[cstdlib.syn]] shall not introduce a
data race [[res.on.data.races]] provided that nothing modifies the
environment.

\[*Note 1*: Calls to the POSIX functions `setenv` and `putenv` modify
the environment. — *end note*\]

A call to the `setlocale` function [[c.locales]] may introduce a data
race with other calls to the `setlocale` function or with calls to
functions that are affected by the current C locale. The implementation
shall behave as if no library function other than `locale::global` calls
the `setlocale` function.

### Header `<cstdarg>` synopsis <a id="cstdarg.syn">[[cstdarg.syn]]</a>

``` cpp
// all freestanding
namespace std {
  using va_list = see below;
}

#define va_arg(V, P) see below
#define va_copy(VDST, VSRC) see below
#define va_end(V) see below
#define va_start(V, P) see below
```

The contents of the header `<cstdarg>` are the same as the C standard
library header `<stdarg.h>`, with the following changes:

- In lieu of the default argument promotions specified in ISO C 6.5.2.2,
  the definition in  [[expr.call]] applies.
- The restrictions that ISO C places on the second parameter to the
  `va_start` macro in header `<stdarg.h>` are different in this
  document. The parameter `parmN` is the rightmost parameter in the
  variable parameter list of the function definition (the one just
  before the `...`).[^33] If the parameter `parmN` is a pack expansion
  [[temp.variadic]] or an entity resulting from a lambda capture
  [[expr.prim.lambda]], the program is ill-formed, no diagnostic
  required. If the parameter `parmN` is of a reference type, or of a
  type that is not compatible with the type that results when passing an
  argument for which there is no parameter, the behavior is undefined.

### Header `<csetjmp>` synopsis <a id="csetjmp.syn">[[csetjmp.syn]]</a>

``` cpp
namespace std {
  using jmp_buf = see below;
  [[noreturn]] void longjmp(jmp_buf env, int val);
}

#define setjmp(env) see below
```

The contents of the header `<csetjmp>` are the same as the C standard
library header `<setjmp.h>`.

The function signature `longjmp(jmp_buf jbuf, int val)` has more
restricted behavior in this document. A `setjmp`/`longjmp` call pair has
undefined behavior if replacing the `setjmp` and `longjmp` by `catch`
and `throw` would invoke any non-trivial destructors for any objects
with automatic storage duration. A call to `setjmp` or `longjmp` has
undefined behavior if invoked in a suspension context of a coroutine
[[expr.await]].

### Header `<csignal>` synopsis <a id="csignal.syn">[[csignal.syn]]</a>

``` cpp
namespace std {
  using sig_atomic_t = see below;

  // [support.signal], signal handlers
  extern "C" using signal-handler = void(int);  // exposition only
  signal-handler* signal(int sig, signal-handler* func);

  int raise(int sig);
}

#define SIG_DFL see below
#define SIG_ERR see below
#define SIG_IGN see below
#define SIGABRT see below
#define SIGFPE see below
#define SIGILL see below
#define SIGINT see below
#define SIGSEGV see below
#define SIGTERM see below
```

The contents of the header `<csignal>` are the same as the C standard
library header `<signal.h>`.

### Signal handlers <a id="support.signal">[[support.signal]]</a>

A call to the function `signal` synchronizes with any resulting
invocation of the signal handler so installed.

A *plain lock-free atomic operation* is an invocation of a function `f`
from [[atomics]], such that:

- `f` is the function `atomic_is_lock_free()`, or
- `f` is the member function `is_lock_free()`, or
- `f` is a non-static member function of class `atomic_flag`, or
- `f` is a non-member function, and the first parameter of `f` has type
  cv `atomic_flag*`, or
- `f` is a non-static member function invoked on an object `A`, such
  that `A.is_lock_free()` yields `true`, or
- `f` is a non-member function, and for every pointer-to-atomic argument
  `A` passed to `f`, `atomic_is_lock_free(A)` yields `true`.

An evaluation is *signal-safe* unless it includes one of the following:

- a call to any standard library function, except for plain lock-free
  atomic operations and functions explicitly identified as signal-safe;
  \[*Note 1*: This implicitly excludes the use of `new` and `delete`
  expressions that rely on a library-provided memory
  allocator. — *end note*\]
- an access to an object with thread storage duration;
- a `dynamic_cast` expression;
- throwing of an exception;
- control entering a *try-block* or *function-try-block*;
- initialization of a variable with static storage duration requiring
  dynamic initialization [[basic.start.dynamic]], [[stmt.dcl]][^34] ; or
- waiting for the completion of the initialization of a variable with
  static storage duration [[stmt.dcl]].

A signal handler invocation has undefined behavior if it includes an
evaluation that is not signal-safe.

The function `signal` is signal-safe if it is invoked with the first
argument equal to the signal number corresponding to the signal that
caused the invocation of the handler.

## C headers <a id="support.c.headers">[[support.c.headers]]</a>

### General <a id="support.c.headers.general">[[support.c.headers.general]]</a>

For compatibility with the C standard library, the C++ standard library
provides the *C headers* shown in [[c.headers]]. The intended use of
these headers is for interoperability only. It is possible that C++
source files need to include one of these headers in order to be valid
ISO C. Source files that are not intended to also be valid ISO C should
not use any of the C headers.

\[*Note 1*: The C headers either have no effect, such as `<stdbool.h>`
and `<stdalign.h>`, or otherwise the corresponding header of the form
`<cname>` provides the same facilities and assuredly defines them in
namespace `std`. — *end note*\]

\[*Example 1*:

The following source file is both valid C++ and valid ISO C. Viewed as
C++, it declares a function with C language linkage; viewed as C it
simply declares a function (and provides a prototype).

``` cpp
#include <stdbool.h>    // for bool in C, no effect in C++{}
#include <stddef.h>     // for size_t

#ifdef __cplusplus      // see [cpp.predefined]
extern "C"              // see [dcl.link]
#endif
void f(bool b[], size_t n);
```

— *end example*\]

### Header `<complex.h>` synopsis <a id="complex.h.syn">[[complex.h.syn]]</a>

``` cpp
#include <complex>
```

The header `<complex.h>` behaves as if it simply includes the header
`<complex>`.

\[*Note 1*: Names introduced by `<complex>` in namespace `std` are not
placed into the global namespace scope by `<complex.h>`. — *end note*\]

### Header `<iso646.h>` synopsis <a id="iso646.h.syn">[[iso646.h.syn]]</a>

The C++ header `<iso646.h>` is empty.

\[*Note 1*: `and`, `and_eq`, `bitand`, `bitor`, `compl`, `not_eq`,
`not`, `or`, `or_eq`, `xor`, and `xor_eq` are keywords in C++
[[lex.key]]. — *end note*\]

### Header `<stdalign.h>` synopsis <a id="stdalign.h.syn">[[stdalign.h.syn]]</a>

The contents of the C++ header `<stdalign.h>` are the same as the C
standard library header `<stdalign.h>`, with the following changes: The
header `<stdalign.h>` does not define a macro named `alignas`.

### Header `<stdbool.h>` synopsis <a id="stdbool.h.syn">[[stdbool.h.syn]]</a>

The contents of the C++ header `<stdbool.h>` are the same as the C
standard library header `<stdbool.h>`, with the following changes: The
header `<stdbool.h>` does not define macros named `bool`, `true`, or
`false`.

### Header `<tgmath.h>` synopsis <a id="tgmath.h.syn">[[tgmath.h.syn]]</a>

``` cpp
#include <cmath>
#include <complex>
```

The header `<tgmath.h>` behaves as if it simply includes the headers
`<cmath>` and `<complex>`.

\[*Note 1*: The overloads provided in C by type-generic macros are
already provided in `<complex>` and `<cmath>` by “sufficient” additional
overloads. — *end note*\]

\[*Note 2*: Names introduced by `<cmath>` or `<complex>` in namespace
`std` are not placed into the global namespace scope by
`<tgmath.h>`. — *end note*\]

### Other C headers <a id="support.c.headers.other">[[support.c.headers.other]]</a>

Every C header other than `<complex.h>`, `<iso646.h>`, `<stdalign.h>`,
`<stdatomic.h>`, `<stdbool.h>`, and `<tgmath.h>`, each of which has a
name of the form `<name.h>`, behaves as if each name placed in the
standard library namespace by the corresponding `<cname>` header is
placed within the global namespace scope, except for the functions
described in [[sf.cmath]], the `std::lerp` function overloads
[[c.math.lerp]], the declaration of `std::byte` [[cstddef.syn]], and the
functions and function templates described in [[support.types.byteops]].
It is unspecified whether these names are first declared or defined
within namespace scope [[basic.scope.namespace]] of the namespace `std`
and are then injected into the global namespace scope by explicit
*using-declaration*s [[namespace.udecl]].

\[*Example 1*: The header `<cstdlib>` assuredly provides its
declarations and definitions within the namespace `std`. It may also
provide these names within the global namespace. The header `<stdlib.h>`
assuredly provides the same declarations and definitions within the
global namespace, much as in the C Standard. It may also provide these
names within the namespace `std`. — *end example*\]

<!-- Section link definitions -->
[alloc.errors]: #alloc.errors
[bad.alloc]: #bad.alloc
[bad.cast]: #bad.cast
[bad.exception]: #bad.exception
[bad.typeid]: #bad.typeid
[cfloat.syn]: #cfloat.syn
[climits.syn]: #climits.syn
[cmp]: #cmp
[cmp.alg]: #cmp.alg
[cmp.categories]: #cmp.categories
[cmp.categories.pre]: #cmp.categories.pre
[cmp.common]: #cmp.common
[cmp.concept]: #cmp.concept
[cmp.partialord]: #cmp.partialord
[cmp.result]: #cmp.result
[cmp.strongord]: #cmp.strongord
[cmp.weakord]: #cmp.weakord
[compare.syn]: #compare.syn
[complex.h.syn]: #complex.h.syn
[coroutine.handle]: #coroutine.handle
[coroutine.handle.compare]: #coroutine.handle.compare
[coroutine.handle.con]: #coroutine.handle.con
[coroutine.handle.conv]: #coroutine.handle.conv
[coroutine.handle.export.import]: #coroutine.handle.export.import
[coroutine.handle.general]: #coroutine.handle.general
[coroutine.handle.hash]: #coroutine.handle.hash
[coroutine.handle.noop]: #coroutine.handle.noop
[coroutine.handle.noop.address]: #coroutine.handle.noop.address
[coroutine.handle.noop.conv]: #coroutine.handle.noop.conv
[coroutine.handle.noop.observers]: #coroutine.handle.noop.observers
[coroutine.handle.noop.promise]: #coroutine.handle.noop.promise
[coroutine.handle.noop.resumption]: #coroutine.handle.noop.resumption
[coroutine.handle.observers]: #coroutine.handle.observers
[coroutine.handle.promise]: #coroutine.handle.promise
[coroutine.handle.resumption]: #coroutine.handle.resumption
[coroutine.noop]: #coroutine.noop
[coroutine.noop.coroutine]: #coroutine.noop.coroutine
[coroutine.promise.noop]: #coroutine.promise.noop
[coroutine.syn]: #coroutine.syn
[coroutine.traits]: #coroutine.traits
[coroutine.traits.general]: #coroutine.traits.general
[coroutine.traits.primary]: #coroutine.traits.primary
[coroutine.trivial.awaitables]: #coroutine.trivial.awaitables
[csetjmp.syn]: #csetjmp.syn
[csignal.syn]: #csignal.syn
[cstdarg.syn]: #cstdarg.syn
[cstddef.syn]: #cstddef.syn
[cstdint.syn]: #cstdint.syn
[cstdlib.syn]: #cstdlib.syn
[except.nested]: #except.nested
[exception]: #exception
[exception.syn]: #exception.syn
[exception.terminate]: #exception.terminate
[get.new.handler]: #get.new.handler
[get.terminate]: #get.terminate
[hardware.interference]: #hardware.interference
[initializer.list.syn]: #initializer.list.syn
[iso646.h.syn]: #iso646.h.syn
[limits.syn]: #limits.syn
[new.badlength]: #new.badlength
[new.delete]: #new.delete
[new.delete.array]: #new.delete.array
[new.delete.dataraces]: #new.delete.dataraces
[new.delete.general]: #new.delete.general
[new.delete.placement]: #new.delete.placement
[new.delete.single]: #new.delete.single
[new.handler]: #new.handler
[new.syn]: #new.syn
[numeric.limits]: #numeric.limits
[numeric.limits.general]: #numeric.limits.general
[numeric.limits.members]: #numeric.limits.members
[numeric.special]: #numeric.special
[propagation]: #propagation
[ptr.launder]: #ptr.launder
[round.style]: #round.style
[set.new.handler]: #set.new.handler
[set.terminate]: #set.terminate
[source.location.syn]: #source.location.syn
[stdalign.h.syn]: #stdalign.h.syn
[stdbool.h.syn]: #stdbool.h.syn
[stdfloat.syn]: #stdfloat.syn
[support]: #support
[support.arith.types]: #support.arith.types
[support.c.headers]: #support.c.headers
[support.c.headers.general]: #support.c.headers.general
[support.c.headers.other]: #support.c.headers.other
[support.coroutine]: #support.coroutine
[support.coroutine.general]: #support.coroutine.general
[support.dynamic]: #support.dynamic
[support.dynamic.general]: #support.dynamic.general
[support.exception]: #support.exception
[support.exception.general]: #support.exception.general
[support.general]: #support.general
[support.initlist]: #support.initlist
[support.initlist.access]: #support.initlist.access
[support.initlist.cons]: #support.initlist.cons
[support.initlist.general]: #support.initlist.general
[support.initlist.range]: #support.initlist.range
[support.limits]: #support.limits
[support.limits.general]: #support.limits.general
[support.rtti]: #support.rtti
[support.rtti.general]: #support.rtti.general
[support.runtime]: #support.runtime
[support.runtime.general]: #support.runtime.general
[support.signal]: #support.signal
[support.srcloc]: #support.srcloc
[support.srcloc.class]: #support.srcloc.class
[support.srcloc.class.general]: #support.srcloc.class.general
[support.srcloc.cons]: #support.srcloc.cons
[support.srcloc.obs]: #support.srcloc.obs
[support.start.term]: #support.start.term
[support.types]: #support.types
[support.types.byteops]: #support.types.byteops
[support.types.layout]: #support.types.layout
[support.types.nullptr]: #support.types.nullptr
[terminate]: #terminate
[terminate.handler]: #terminate.handler
[tgmath.h.syn]: #tgmath.h.syn
[type.info]: #type.info
[typeinfo.syn]: #typeinfo.syn
[uncaught.exceptions]: #uncaught.exceptions
[version.syn]: #version.syn

<!-- Link reference definitions -->
[alg.c.library]: algorithms.md#alg.c.library
[atomics]: thread.md#atomics
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.extended.fp]: basic.md#basic.extended.fp
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.term]: basic.md#basic.start.term
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[c.headers]: #c.headers
[c.locales]: localization.md#c.locales
[c.malloc]: mem.md#c.malloc
[c.math.abs]: numerics.md#c.math.abs
[c.math.lerp]: numerics.md#c.math.lerp
[c.math.rand]: numerics.md#c.math.rand
[c.mb.wcs]: strings.md#c.mb.wcs
[class.mem]: class.md#class.mem
[class.prop]: class.md#class.prop
[class.spaceship]: class.md#class.spaceship
[cmp.categories]: #cmp.categories
[complex]: numerics.md#complex
[concept.totallyordered]: concepts.md#concept.totallyordered
[concepts.compare.general]: concepts.md#concepts.compare.general
[constraints]: library.md#constraints
[conv.prom]: expr.md#conv.prom
[conv.ptr]: expr.md#conv.ptr
[conv.qual]: expr.md#conv.qual
[conv.rank]: basic.md#conv.rank
[coroutine.syn]: #coroutine.syn
[coroutine.traits]: #coroutine.traits
[cpp.line]: cpp.md#cpp.line
[cpp17.nullablepointer]: #cpp17.nullablepointer
[cstddef.syn]: #cstddef.syn
[cstdlib.syn]: #cstdlib.syn
[customization.point.object]: library.md#customization.point.object
[dcl.fct.def.coroutine]: dcl.md#dcl.fct.def.coroutine
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init.list]: dcl.md#dcl.init.list
[defns.expression.equivalent]: #defns.expression.equivalent
[except.handle]: except.md#except.handle
[except.spec]: except.md#except.spec
[except.terminate]: except.md#except.terminate
[except.uncaught]: except.md#except.uncaught
[expr.add]: expr.md#expr.add
[expr.await]: expr.md#expr.await
[expr.call]: expr.md#expr.call
[expr.context]: expr.md#expr.context
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.eq]: expr.md#expr.eq
[expr.new]: expr.md#expr.new
[expr.prim.lambda]: expr.md#expr.prim.lambda
[expr.rel]: expr.md#expr.rel
[expr.sizeof]: expr.md#expr.sizeof
[expr.spaceship]: expr.md#expr.spaceship
[expr.typeid]: expr.md#expr.typeid
[get.new.handler]: #get.new.handler
[intro.multithread]: basic.md#intro.multithread
[lex.key]: lex.md#lex.key
[library.c]: library.md#library.c
[multibyte.strings]: library.md#multibyte.strings
[namespace.udecl]: dcl.md#namespace.udecl
[new.delete]: #new.delete
[new.handler]: #new.handler
[propagation]: #propagation
[res.on.data.races]: library.md#res.on.data.races
[sf.cmath]: numerics.md#sf.cmath
[stmt.dcl]: stmt.md#stmt.dcl
[string.classes,locale.codecvt]: #string.classes,locale.codecvt
[support.initlist]: #support.initlist
[support.signal]: #support.signal
[support.srcloc.current]: #support.srcloc.current
[support.start.term]: #support.start.term
[support.summary]: #support.summary
[support.types.byteops]: #support.types.byteops
[support.types.layout]: #support.types.layout
[support.types.nullptr]: #support.types.nullptr
[swappable.requirements]: library.md#swappable.requirements
[temp.deduct]: temp.md#temp.deduct
[temp.dep.constexpr]: temp.md#temp.dep.constexpr
[temp.dep.expr]: temp.md#temp.dep.expr
[temp.variadic]: temp.md#temp.variadic
[term.odr.use]: #term.odr.use
[unord.hash]: utilities.md#unord.hash
[utility.arg.requirements]: library.md#utility.arg.requirements

<!-- Link reference definitions -->
[cmp]: #cmp
[support.arith.types]: #support.arith.types
[support.coroutine]: #support.coroutine
[support.dynamic]: #support.dynamic
[support.exception]: #support.exception
[support.initlist]: #support.initlist
[support.limits]: #support.limits
[support.rtti]: #support.rtti
[support.runtime]: #support.runtime
[support.srcloc]: #support.srcloc
[support.start.term]: #support.start.term
[support.types]: #support.types

[^1]: Possible definitions include `0` and `0L`, but not `(void*)0`.

[^2]: Note that `offsetof` is required to work as specified even if
    unary `operator&` is overloaded for any of the types involved.

[^3]: Equivalent to `CHAR_MIN`, `SHRT_MIN`, `FLT_MIN`, `DBL_MIN`, etc.

[^4]: Equivalent to `CHAR_MAX`, `SHRT_MAX`, `FLT_MAX`, `DBL_MAX`, etc.

[^5]: `lowest()` is necessary because not all floating-point
    representations have a smallest (most negative) value that is the
    negative of the largest (most positive) finite value.

[^6]: Equivalent to `FLT_MANT_DIG`, `DBL_MANT_DIG`, `LDBL_MANT_DIG`.

[^7]: Equivalent to `FLT_DIG`, `DBL_DIG`, `LDBL_DIG`.

[^8]: Equivalent to `FLT_RADIX`.

[^9]: Distinguishes types with bases other than 2 (e.g., BCD).

[^10]: Equivalent to `FLT_EPSILON`, `DBL_EPSILON`, `LDBL_EPSILON`.

[^11]: Rounding error is described in LIA-1 Section 5.2.4 and Annex C
    Rationale Section C.5.2.4 — Rounding and rounding constants.

[^12]: Equivalent to `FLT_MIN_EXP`, `DBL_MIN_EXP`, `LDBL_MIN_EXP`.

[^13]: Equivalent to `FLT_MIN_10_EXP`, `DBL_MIN_10_EXP`,
    `LDBL_MIN_10_EXP`.

[^14]: Equivalent to `FLT_MAX_EXP`, `DBL_MAX_EXP`, `LDBL_MAX_EXP`.

[^15]: Equivalent to `FLT_MAX_10_EXP`, `DBL_MAX_10_EXP`,
    `LDBL_MAX_10_EXP`.

[^16]: Required by LIA-1.

[^17]: Required by LIA-1.

[^18]: Required by LIA-1.

[^19]: Required by LIA-1.

[^20]: Required by LIA-1.

[^21]: Required by LIA-1.

[^22]: ISO/IEC/IEEE 60559:2020 is the same as IEEE 754-2019.

[^23]: Required by LIA-1.

[^24]: Required by LIA-1.

[^25]: Required by LIA-1.

[^26]: Refer to ISO/IEC/IEEE 60559. Required by LIA-1.

[^27]: Equivalent to `FLT_ROUNDS`. Required by LIA-1.

[^28]: A function is called for every time it is registered.

[^29]: Objects with automatic storage duration are all destroyed in a
    program whose `main` function@@REF:basic.start.main@@ contains no
    objects with automatic storage duration and executes the call to
    `exit()`. Control can be transferred directly to such a `main`
    function by throwing an exception that is caught in `main`.

[^30]: The macros `EXIT_FAILURE` and `EXIT_SUCCESS` are defined in
    `<cstdlib>`.

[^31]: It is not the direct responsibility of `operator new[]` or
    `operator delete[]` to note the repetition count or element size of
    the array. Those operations are performed elsewhere in the array
    `new` and `delete` expressions. The array `new` expression, can,
    however, increase the `size` argument to `operator new[]` to obtain
    space to store supplemental information.

[^32]: That is, `a < b`, `a == b`, and `a > b` might all be `false`.

[^33]: Note that `va_start` is required to work as specified even if
    unary `operator&` is overloaded for the type of `parmN`.

[^34]: Such initialization can occur because it is the first odr-use
    [[term.odr.use]] of that variable.
