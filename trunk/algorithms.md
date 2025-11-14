# Algorithms library <a id="algorithms">[[algorithms]]</a>

## General <a id="algorithms.general">[[algorithms.general]]</a>

This Clause describes components that C++ programs may use to perform
algorithmic operations on containers [[containers]] and other sequences.

The following subclauses describe components for non-modifying sequence
operations, mutating sequence operations, sorting and related
operations, and algorithms from the C library, as summarized in
[[algorithms.summary]].

**Table: Algorithms library summary**

| Subclause                    |                                   | Header        |
| ---------------------------- | --------------------------------- | ------------- |
| [[algorithms.requirements]]  | Algorithms requirements           |               |
| [[algorithms.parallel]]      | Parallel algorithms               | `<execution>` |
| [[algorithms.results]]       | Algorithm result types            | `<algorithm>` |
| [[alg.nonmodifying]]         | Non-modifying sequence operations |               |
| [[alg.modifying.operations]] | Mutating sequence operations      |               |
| [[alg.sorting]]              | Sorting and related operations    |               |
| [[numeric.ops]]              | Generalized numeric operations    | `<numeric>`   |
| [[specialized.algorithms]]   | Specialized `<memory>` algorithms | `<memory>`    |
| [[alg.rand]]                 | Specialized `<random>` algorithms | `<random>`    |
| [[alg.c.library]]            | C library algorithms              | `<cstdlib>`   |


## Algorithms requirements <a id="algorithms.requirements">[[algorithms.requirements]]</a>

The entities defined in the `std::ranges` namespace in this Clause and
specified as function templates are algorithm function objects
[[alg.func.obj]].

For purposes of determining the existence of data races, algorithms
shall not modify objects referenced through an iterator argument unless
the specification requires such modification.

Throughout this Clause, where the template parameters are not
constrained, the names of template parameters are used to express type
requirements.

- If an algorithm’s *Effects* element specifies that a value pointed to
  by any iterator passed as an argument is modified, then the type of
  that argument shall meet the requirements of a mutable iterator
  [[iterator.requirements]].
- If an algorithm’s template parameter is named `InputIterator`,
  `InputIterator1`, or `InputIterator2`, the template argument shall
  meet the *Cpp17InputIterator* requirements [[input.iterators]].
- If an algorithm’s template parameter is named `OutputIterator`,
  `OutputIterator1`, or `OutputIterator2`, the template argument shall
  meet the *Cpp17OutputIterator* requirements [[output.iterators]].
- If an algorithm’s template parameter is named `ForwardIterator`,
  `ForwardIterator1`, `ForwardIterator2`, or `NoThrowForwardIterator`,
  the template argument shall meet the *Cpp17ForwardIterator*
  requirements [[forward.iterators]] if it is required to be a mutable
  iterator, or model `forward_iterator` [[iterator.concept.forward]]
  otherwise.
- If an algorithm’s template parameter is named
  `NoThrowForwardIterator`, the template argument is also required to
  have the property that no exceptions are thrown from increment,
  assignment, or comparison of, or indirection through, valid iterators.
- If an algorithm’s template parameter is named `BidirectionalIterator`,
  `BidirectionalIterator1`, or `BidirectionalIterator2`, the template
  argument shall meet the *Cpp17BidirectionalIterator* requirements
  [[bidirectional.iterators]] if it is required to be a mutable
  iterator, or model `bidirectional_iterator` [[iterator.concept.bidir]]
  otherwise.
- If an algorithm’s template parameter is named `RandomAccessIterator`,
  `RandomAccessIterator1`, or `RandomAccessIterator2`, the template
  argument shall meet the *Cpp17RandomAccessIterator* requirements
  [[random.access.iterators]] if it is required to be a mutable
  iterator, or model `random_access_iterator`
  [[iterator.concept.random.access]] otherwise.

[*Note 1*: These requirements do not affect iterator arguments that are
constrained, for which iterator category and mutability requirements are
expressed explicitly. — *end note*]

Both in-place and copying versions are provided for certain
algorithms.[^1]

When such a version is provided for *algorithm* it is called
*algorithm`_copy`*. Algorithms that take predicates end with the suffix
`_if` (which follows the suffix `_copy`).

When not otherwise constrained, the `Predicate` parameter is used
whenever an algorithm expects a function object [[function.objects]]
that, when applied to the result of dereferencing the corresponding
iterator, returns a value testable as `true`. If an algorithm takes
`Predicate pred` as its argument and `first` as its iterator argument
with value type `T`, the expression `pred(*first)` shall be well-formed
and the type `decltype(pred(*first))` shall model `boolean-testable`
[[concept.booleantestable]]. The function object `pred` shall not apply
any non-constant function through its argument. Given a glvalue `u` of
type (possibly const) `T` that designates the same object as `*first`,
`pred(u)` shall be a valid expression that is equal to `pred(*first)`.

When not otherwise constrained, the `BinaryPredicate` parameter is used
whenever an algorithm expects a function object that, when applied to
the result of dereferencing two corresponding iterators or to
dereferencing an iterator and type `T` when `T` is part of the
signature, returns a value testable as `true`. If an algorithm takes
`BinaryPredicate binary_pred` as its argument and `first1` and `first2`
as its iterator arguments with respective value types `T1` and `T2`, the
expression `binary_pred(*first1, *first2)` shall be well-formed and the
type `decltype(binary_pred(*first1, *first2))` shall model
`boolean-testable`. Unless otherwise specified, `BinaryPredicate` always
takes the first iterator’s `value_type` as its first argument, that is,
in those cases when `T value` is part of the signature, the expression
`binary_pred(*first1, value)` shall be well-formed and the type
`decltype(binary_pred(*first1, value))` shall model `boolean-testable`.
`binary_pred` shall not apply any non-constant function through any of
its arguments. Given a glvalue `u` of type (possibly const) `T1` that
designates the same object as `*first1`, and a glvalue `v` of type
(possibly const) `T2` that designates the same object as `*first2`,
`binary_pred(u, *first2)`, `binary_pred(*first1, v)`, and
`binary_pred(u, v)` shall each be a valid expression that is equal to
`binary_pred(*first1, *first2)`, and `binary_pred(u, value)` shall be a
valid expression that is equal to `binary_pred(*first1, value)`.

The parameters `UnaryOperation`, `BinaryOperation`, `BinaryOperation1`,
and `BinaryOperation2` are used whenever an algorithm expects a function
object [[function.objects]].

[*Note 2*: Unless otherwise specified, algorithms that take function
objects as arguments can copy those function objects freely. If object
identity is important, a wrapper class that points to a non-copied
implementation object such as `reference_wrapper<T>` [[refwrap]], or
some equivalent solution, can be used. — *end note*]

When the description of an algorithm gives an expression such as
`*first == value` for a condition, the expression shall evaluate to
either `true` or `false` in boolean contexts.

In the description of the algorithms, operator `+` is used for some of
the iterator categories for which it does not have to be defined. In
these cases the semantics of `a + n` are the same as those of

``` cpp
auto tmp = a;
for (; n < 0; ++n) --tmp;
for (; n > 0; --n) ++tmp;
return tmp;
```

Similarly, operator `-` is used for some combinations of iterators and
sentinel types for which it does not have to be defined. If \[`a`, `b`)
denotes a range, the semantics of `b - a` in these cases are the same as
those of

``` cpp
iter_difference_t<decltype(a)> n = 0;
for (auto tmp = a; tmp != b; ++tmp) ++n;
return n;
```

and if \[`b`, `a`) denotes a range, the same as those of

``` cpp
iter_difference_t<decltype(b)> n = 0;
for (auto tmp = b; tmp != a; ++tmp) --n;
return n;
```

For each iterator `i` and sentinel `s` produced from a range `r`, the
semantics of `s - i` has the same type, value, and value category as
`ranges::distance(i, s)`.

[*Note 3*: The implementation can use `ranges::distance(r)` when that
produces the same value as `ranges::distance(i, s)`. This can be more
efficient for sized ranges. — *end note*]

In the description of the algorithms, given an iterator `a` whose
difference type is `D`, and an expression `n` of integer-like type other
than cv `D`, the semantics of `a + n` and `a - n` are, respectively,
those of `a + D(n)` and `a - D(n)`.

In the description of algorithm return values, a sentinel value `s`
denoting the end of a range \[`i`, `s`) is sometimes returned where an
iterator is expected. In these cases, the semantics are as if the
sentinel is converted into an iterator using `ranges::next(i, s)`.

Overloads of algorithms that take `range` arguments [[range.range]]
behave as if they are implemented by dispatching to the overload in
namespace `ranges` that takes separate iterator and sentinel arguments,
where for each range argument `r`

- a corresponding iterator argument is initialized with
  `ranges::begin(r)` and
- a corresponding sentinel argument is initialized with
  `ranges::end(r)`, or
  `ranges::next(ranges::{}begin(r), ranges::end(r))` if the type of `r`
  models `forward_range` and computing `ranges::next` meets the
  specified complexity requirements.

The well-formedness and behavior of a call to an algorithm with an
explicitly-specified template argument list is unspecified, except where
explicitly stated otherwise.

[*Note 4*: Consequently, an implementation can declare an algorithm
with different template parameters than those presented. — *end note*]

## Parallel algorithms <a id="algorithms.parallel">[[algorithms.parallel]]</a>

### Preamble <a id="algorithms.parallel.defns">[[algorithms.parallel.defns]]</a>

A *parallel algorithm* is a function template listed in this document
with a template parameter named `ExecutionPolicy` or constrained by the
following exposition-only concept:

``` cpp
template<class Ep>
  concept execution-policy = is_execution_policy_v<remove_cvref_t<Ep>>;     // exposition only
```

Such a template parameter is termed an
*execution policy template parameter*.

A parallel algorithm accesses objects indirectly accessible via its
arguments by invoking the following functions:

- All operations of the categories of the iterators, sentinels, or
  `mdspan` types that the algorithm is instantiated with.
- Operations on those sequence elements that are required by its
  specification.
- User-provided invocable objects to be applied during the execution of
  the algorithm, if required by the specification.
- Operations on those invocable objects required by the specification.
  \[*Note 1*: See  [[algorithms.requirements]]. — *end note*]

These functions are herein called *element access functions*.

[*Example 1*:

The `sort` function may invoke the following element access functions:

- Operations of the random-access iterator of the actual template
  argument (as per [[random.access.iterators]]), as implied by the name
  of the template parameter `RandomAccessIterator`.
- The `swap` function on the elements of the sequence (as per the
  preconditions specified in [[sort]]).
- The user-provided `Compare` function object.

— *end example*]

A standard library function is *vectorization-unsafe* if it is specified
to synchronize with another function invocation, or another function
invocation is specified to synchronize with it, and if it is not a
memory allocation or deallocation function or lock-free atomic
modify-write operation [[atomics.order]].

[*Note 1*: Implementations must ensure that internal synchronization
inside standard library functions does not prevent forward progress when
those functions are executed by threads of execution with weakly
parallel forward progress guarantees. — *end note*]

[*Example 2*:

``` cpp
int x = 0;
std::mutex m;
void f() {
  int a[] = {1,2};
  std::for_each(std::execution::par_unseq, std::begin(a), std::end(a), [&](int) {
    std::lock_guard<mutex> guard(m);            // incorrect: lock_guard constructor calls m.lock()
    ++x;
  });
}
```

The above program may result in two consecutive calls to `m.lock()` on
the same thread of execution (which may deadlock), because the
applications of the function object are not guaranteed to run on
different threads of execution.

— *end example*]

### Requirements on user-provided function objects <a id="algorithms.parallel.user">[[algorithms.parallel.user]]</a>

Unless otherwise specified, invocable objects passed into parallel
algorithms as objects of a type denoted by a template parameter named
`Predicate`, `BinaryPredicate`, `Compare`, `UnaryOperation`,
`BinaryOperation`, `BinaryOperation1`, `BinaryOperation2`,
`BinaryDivideOp`, or constrained by a concept that subsumes
`regular_invocable` and the operators used by the analogous overloads to
these parallel algorithms that are formed by an invocation with the
specified default predicate or operation (where applicable) shall not
directly or indirectly modify objects via their arguments, nor shall
they rely on the identity of the provided objects.

### Effect of execution policies on algorithm execution <a id="algorithms.parallel.exec">[[algorithms.parallel.exec]]</a>

An execution policy template parameter describes the manner in which the
execution of a parallel algorithm may be parallelized and the manner in
which it applies the element access functions.

If an object is modified by an element access function, the algorithm
will perform no other unsynchronized accesses to that object. The
modifying element access functions are those which are specified as
modifying the object.

[*Note 1*: For example, `swap`, `++`, `--`, `@=`, and assignments
modify the object. For the assignment and `@=` operators, only the left
argument is modified. — *end note*]

Unless otherwise stated, implementations may make arbitrary copies of
elements (with type `T`) from sequences where
`is_trivially_copy_constructible_v<T>` and
`is_trivially_destructible_v<T>` are `true`.

[*Note 2*: This implies that user-supplied function objects cannot rely
on object identity of arguments for such input sequences. If object
identity of the arguments to these function objects is important, a
wrapping iterator that returns a non-copied implementation object such
as `reference_wrapper<T>` [[refwrap]], or some equivalent solution, can
be used. — *end note*]

The invocations of element access functions in parallel algorithms
invoked with an execution policy object of type
`execution::sequenced_policy` all occur in the calling thread of
execution.

[*Note 3*: The invocations are not interleaved; see 
[[intro.execution]]. — *end note*]

The invocations of element access functions in parallel algorithms
invoked with an execution policy object of type
`execution::unsequenced_policy` are permitted to execute in an unordered
fashion in the calling thread of execution, unsequenced with respect to
one another in the calling thread of execution.

[*Note 4*: This means that multiple function object invocations can be
interleaved on a single thread of execution, which overrides the usual
guarantee from [[intro.execution]] that function executions do not
overlap with one another. — *end note*]

The behavior of a program is undefined if it invokes a
vectorization-unsafe standard library function from user code called
from an `execution::unsequenced_policy` algorithm.

[*Note 5*: Because `execution::unsequenced_policy` allows the execution
of element access functions to be interleaved on a single thread of
execution, blocking synchronization, including the use of mutexes, risks
deadlock. — *end note*]

The invocations of element access functions in parallel algorithms
invoked with an execution policy object of type
`execution::parallel_policy` are permitted to execute either in the
invoking thread of execution or in a thread of execution implicitly
created by the library to support parallel algorithm execution. If the
threads of execution created by `thread` [[thread.thread.class]] or
`jthread` [[thread.jthread.class]] provide concurrent forward progress
guarantees [[intro.progress]], then a thread of execution implicitly
created by the library will provide parallel forward progress
guarantees; otherwise, the provided forward progress guarantee is
*implementation-defined*. Any such invocations executing in the same
thread of execution are indeterminately sequenced with respect to each
other.

[*Note 6*: It is the caller’s responsibility to ensure that the
invocation does not introduce data races or deadlocks. — *end note*]

[*Example 1*:

``` cpp
int a[] = {0,1};
std::vector<int> v;
std::for_each(std::execution::par, std::begin(a), std::end(a), [&](int i) {
  v.push_back(i*2+1);                   // incorrect: data race
});
```

The program above has a data race because of the unsynchronized access
to the container `v`.

— *end example*]

[*Example 2*:

``` cpp
std::atomic<int> x{0};
int a[] = {1,2};
std::for_each(std::execution::par, std::begin(a), std::end(a), [&](int) {
  x.fetch_add(1, std::memory_order::relaxed);
  // spin wait for another iteration to change the value of x
  while (x.load(std::memory_order::relaxed) == 1) { }           // incorrect: assumes execution order
});
```

The above example depends on the order of execution of the iterations,
and will not terminate if both iterations are executed sequentially on
the same thread of execution.

— *end example*]

[*Example 3*:

``` cpp
int x = 0;
std::mutex m;
int a[] = {1,2};
std::for_each(std::execution::par, std::begin(a), std::end(a), [&](int) {
  std::lock_guard<mutex> guard(m);
  ++x;
});
```

The above example synchronizes access to object `x` ensuring that it is
incremented correctly.

— *end example*]

The invocations of element access functions in parallel algorithms
invoked with an execution policy object of type
`execution::parallel_unsequenced_policy` are permitted to execute in an
unordered fashion in unspecified threads of execution, and unsequenced
with respect to one another within each thread of execution. These
threads of execution are either the invoking thread of execution or
threads of execution implicitly created by the library; the latter will
provide weakly parallel forward progress guarantees.

[*Note 7*: This means that multiple function object invocations can be
interleaved on a single thread of execution, which overrides the usual
guarantee from [[intro.execution]] that function executions do not
overlap with one another. — *end note*]

The behavior of a program is undefined if it invokes a
vectorization-unsafe standard library function from user code called
from an `execution::parallel_unsequenced_policy` algorithm.

[*Note 8*: Because `execution::parallel_unsequenced_policy` allows the
execution of element access functions to be interleaved on a single
thread of execution, blocking synchronization, including the use of
mutexes, risks deadlock. — *end note*]

[*Note 9*: The semantics of invocation with
`execution::unsequenced_policy`, `execution::parallel_policy`, or
`execution::parallel_unsequenced_policy` allow the implementation to
fall back to sequential execution if the system cannot parallelize an
algorithm invocation, e.g., due to lack of resources. — *end note*]

If an invocation of a parallel algorithm uses threads of execution
implicitly created by the library, then the invoking thread of execution
will either

- temporarily block with forward progress guarantee delegation
  [[intro.progress]] on the completion of these library-managed threads
  of execution, or
- eventually execute an element access function;

the thread of execution will continue to do so until the algorithm is
finished.

[*Note 10*: In blocking with forward progress guarantee delegation in
this context, a thread of execution created by the library is considered
to have finished execution as soon as it has finished the execution of
the particular element access function that the invoking thread of
execution logically depends on. — *end note*]

The semantics of parallel algorithms invoked with an execution policy
object of *implementation-defined* type are *implementation-defined*.

### Parallel algorithm exceptions <a id="algorithms.parallel.exceptions">[[algorithms.parallel.exceptions]]</a>

During the execution of a parallel algorithm, if temporary memory
resources are required for parallelization and none are available, the
algorithm throws a `bad_alloc` exception.

During the execution of a parallel algorithm, if the invocation of an
element access function exits via an uncaught exception, the behavior is
determined by the execution policy.

### Parallel algorithm overloads <a id="algorithms.parallel.overloads">[[algorithms.parallel.overloads]]</a>

Parallel algorithms are algorithm overloads. Each parallel algorithm
overload has an additional function parameter P of type `T&&` as the
first function parameter, where `T` is the execution policy template
parameter.

[*Note 1*: Not all algorithms have parallel algorithm
overloads. — *end note*]

Unless otherwise specified, the semantics of calling a parallel
algorithm overload are identical to calling the corresponding algorithm
overload without the parameter P, using all but the first argument.

Unless otherwise specified, the complexity requirements of a parallel
algorithm overload are relaxed from the complexity requirements of the
corresponding overload without the parameter P as follows: when the
guarantee says “at most *expr*” or “exactly *expr*” and does not specify
the number of assignments or swaps, and *expr* is not already expressed
with \bigoh notation, the complexity of the algorithm shall be *expr*.

A parallel algorithm with a template parameter named `ExecutionPolicy`
shall not participate in overload resolution unless that template
parameter satisfies `execution-policy`.

### Execution policies <a id="execpol">[[execpol]]</a>

#### General <a id="execpol.general">[[execpol.general]]</a>

Subclause  [[execpol]] describes classes that are *execution policy*
types. An object of an execution policy type indicates the kinds of
parallelism allowed in the execution of an algorithm and expresses the
consequent requirements on the element access functions. Execution
policy types are declared in header `<execution>`.

[*Example 1*:

``` cpp
using namespace std;
vector<int> v = ...;

// standard sequential sort
sort(v.begin(), v.end());

// explicitly sequential sort
sort(execution::seq, v.begin(), v.end());

// permitting parallel execution
sort(execution::par, v.begin(), v.end());

// permitting vectorization as well
sort(execution::par_unseq, v.begin(), v.end());
```

— *end example*]

[*Note 1*: Implementations can provide additional execution policies to
those described in this document as extensions to address parallel
architectures that require idiosyncratic parameters for efficient
execution. — *end note*]

#### Execution policy type trait <a id="execpol.type">[[execpol.type]]</a>

``` cpp
template<class T> struct is_execution_policy;
```

`is_execution_policy` can be used to detect execution policies for the
purpose of excluding function signatures from otherwise ambiguous
overload resolution participation.

`is_execution_policy<T>` is a *Cpp17UnaryTypeTrait* with a base
characteristic of `true_type` if `T` is the type of a standard or
*implementation-defined* execution policy, otherwise `false_type`.

[*Note 1*: This provision reserves the privilege of creating
non-standard execution policies to the library
implementation. — *end note*]

The behavior of a program that adds specializations for
`is_execution_policy` is undefined.

#### Sequenced execution policy <a id="execpol.seq">[[execpol.seq]]</a>

``` cpp
class execution::sequenced_policy { unspecified };
```

The class `execution::sequenced_policy` is an execution policy type used
as a unique type to disambiguate parallel algorithm overloading and
require that a parallel algorithm’s execution may not be parallelized.

During the execution of a parallel algorithm with the
`execution::sequenced_policy` policy, if the invocation of an element
access function exits via an exception, `terminate` is
invoked [[except.terminate]].

#### Parallel execution policy <a id="execpol.par">[[execpol.par]]</a>

``` cpp
class execution::parallel_policy { unspecified };
```

The class `execution::parallel_policy` is an execution policy type used
as a unique type to disambiguate parallel algorithm overloading and
indicate that a parallel algorithm’s execution may be parallelized.

During the execution of a parallel algorithm with the
`execution::parallel_policy` policy, if the invocation of an element
access function exits via an exception, `terminate` is
invoked [[except.terminate]].

#### Parallel and unsequenced execution policy <a id="execpol.parunseq">[[execpol.parunseq]]</a>

``` cpp
class execution::parallel_unsequenced_policy { unspecified };
```

The class `execution::parallel_unsequenced_policy` is an execution
policy type used as a unique type to disambiguate parallel algorithm
overloading and indicate that a parallel algorithm’s execution may be
parallelized and vectorized.

During the execution of a parallel algorithm with the
`execution::parallel_unsequenced_policy` policy, if the invocation of an
element access function exits via an exception, `terminate` is
invoked [[except.terminate]].

#### Unsequenced execution policy <a id="execpol.unseq">[[execpol.unseq]]</a>

``` cpp
class execution::unsequenced_policy { unspecified };
```

The class `unsequenced_policy` is an execution policy type used as a
unique type to disambiguate parallel algorithm overloading and indicate
that a parallel algorithm’s execution may be vectorized, e.g., executed
on a single thread using instructions that operate on multiple data
items.

During the execution of a parallel algorithm with the
`execution::unsequenced_policy` policy, if the invocation of an element
access function exits via an exception, `terminate` is
invoked [[except.terminate]].

#### Execution policy objects <a id="execpol.objects">[[execpol.objects]]</a>

``` cpp
inline constexpr execution::sequenced_policy            execution::seq{ unspecified };
inline constexpr execution::parallel_policy             execution::par{ unspecified };
inline constexpr execution::parallel_unsequenced_policy execution::par_unseq{ unspecified };
inline constexpr execution::unsequenced_policy          execution::unseq{ unspecified };
```

The header `<execution>` declares global objects associated with each
type of execution policy.

## Header `<algorithm>` synopsis <a id="algorithm.syn">[[algorithm.syn]]</a>

``` cpp
// mostly freestanding
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  namespace ranges {
    // [algorithms.results], algorithm result types
    template<class I, class F>
      struct in_fun_result;

    template<class I1, class I2>
      struct in_in_result;

    template<class I, class O>
      struct in_out_result;

    template<class I1, class I2, class O>
      struct in_in_out_result;

    template<class I, class O1, class O2>
      struct in_out_out_result;

    template<class T>
      struct min_max_result;

    template<class I>
      struct in_found_result;

    template<class I, class T>
      struct in_value_result;

    template<class O, class T>
      struct out_value_result;
  }

  // [alg.nonmodifying], non-modifying sequence operations
  // [alg.all.of], all of
  template<class InputIterator, class Predicate>
    constexpr bool all_of(InputIterator first, InputIterator last, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    bool all_of(ExecutionPolicy&& exec,                         // freestanding-deleted, see [algorithms.parallel.overloads]
                ForwardIterator first, ForwardIterator last, Predicate pred);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr bool all_of(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr bool all_of(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      bool all_of(Ep&& exec, I first, S last, Pred pred, Proj proj = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      bool all_of(Ep&& exec, R&& r, Pred pred, Proj proj = {});             // freestanding-deleted
  }

  // [alg.any.of], any of
  template<class InputIterator, class Predicate>
    constexpr bool any_of(InputIterator first, InputIterator last, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    bool any_of(ExecutionPolicy&& exec,                         // freestanding-deleted, see [algorithms.parallel.overloads]
                ForwardIterator first, ForwardIterator last, Predicate pred);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr bool any_of(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr bool any_of(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      bool any_of(Ep&& exec, I first, S last, Pred pred, Proj proj = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      bool any_of(Ep&& exec, R&& r, Pred pred, Proj proj = {});             // freestanding-deleted
  }

  // [alg.none.of], none of
  template<class InputIterator, class Predicate>
    constexpr bool none_of(InputIterator first, InputIterator last, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    bool none_of(ExecutionPolicy&& exec,                        // freestanding-deleted, see [algorithms.parallel.overloads]
                 ForwardIterator first, ForwardIterator last, Predicate pred);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr bool none_of(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr bool none_of(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      bool none_of(Ep&& exec, I first, S last, Pred pred, Proj proj = {});  // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      bool none_of(Ep&& exec, R&& r, Pred pred, Proj proj = {});            // freestanding-deleted
  }

  // [alg.contains], contains
  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      constexpr bool contains(I first, S last, const T& value, Proj proj = {});
    template<input_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires
        indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
      constexpr bool contains(R&& r, const T& value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      bool contains(Ep&& exec, I first, S last, const T& value,
                    Proj proj = {});                                        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires
        indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
      bool contains(Ep&& exec, R&& r, const T& value, Proj proj = {});      // freestanding-deleted

    template<forward_iterator I1, sentinel_for<I1> S1,
             forward_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr bool contains_subrange(I1 first1, S1 last1, I2 first2, S2 last2,
                                       Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<forward_range R1, forward_range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr bool contains_subrange(R1&& r1, R2&& r2,
                                       Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      bool contains_subrange(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                             Proj1 proj1 = {}, Proj2 proj2 = {});           // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      bool contains_subrange(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {}, Proj1 proj1 = {},
                             Proj2 proj2 = {});                             // freestanding-deleted
  }

  // [alg.foreach], for each
  template<class InputIterator, class Function>
    constexpr Function for_each(InputIterator first, InputIterator last, Function f);
  template<class ExecutionPolicy, class ForwardIterator, class Function>
    void for_each(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator first, ForwardIterator last, Function f);

  namespace ranges {
    template<class I, class F>
      using for_each_result = in_fun_result<I, F>;

    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirectly_unary_invocable<projected<I, Proj>> Fun>
      constexpr for_each_result<I, Fun>
        for_each(I first, S last, Fun f, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirectly_unary_invocable<projected<iterator_t<R>, Proj>> Fun>
      constexpr for_each_result<borrowed_iterator_t<R>, Fun>
        for_each(R&& r, Fun f, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirectly_unary_invocable<projected<I, Proj>> Fun>
      I for_each(Ep&& exec, I first, S last, Fun f, Proj proj = {});        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirectly_unary_invocable<projected<iterator_t<R>, Proj>> Fun>
      borrowed_iterator_t<R>
        for_each(Ep&& exec, R&& r, Fun f, Proj proj = {});                  // freestanding-deleted
  }

  template<class InputIterator, class Size, class Function>
    constexpr InputIterator for_each_n(InputIterator first, Size n, Function f);
  template<class ExecutionPolicy, class ForwardIterator, class Size, class Function>
    ForwardIterator for_each_n(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator first, Size n, Function f);

  namespace ranges {
    template<class I, class F>
      using for_each_n_result = in_fun_result<I, F>;

    template<input_iterator I, class Proj = identity,
             indirectly_unary_invocable<projected<I, Proj>> Fun>
      constexpr for_each_n_result<I, Fun>
        for_each_n(I first, iter_difference_t<I> n, Fun f, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, class Proj = identity,
             indirectly_unary_invocable<projected<I, Proj>> Fun>
      I for_each_n(Ep&& exec, I first, iter_difference_t<I> n, Fun f,
                   Proj proj = {});                             // freestanding-deleted
  }

  // [alg.find], find
  template<class InputIterator, class T = iterator_traits<InputIterator>::value_type>
    constexpr InputIterator find(InputIterator first, InputIterator last,
                                 const T& value);
  template<class ExecutionPolicy, class ForwardIterator,
           class T = iterator_traits<ForwardIterator>::value_type>
    ForwardIterator find(ExecutionPolicy&& exec,                // freestanding-deleted, see [algorithms.parallel.overloads]
                         ForwardIterator first, ForwardIterator last,
                         const T& value);
  template<class InputIterator, class Predicate>
    constexpr InputIterator find_if(InputIterator first, InputIterator last,
                                    Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    ForwardIterator find_if(ExecutionPolicy&& exec,             // freestanding-deleted, see [algorithms.parallel.overloads]
                            ForwardIterator first, ForwardIterator last,
                            Predicate pred);
  template<class InputIterator, class Predicate>
    constexpr InputIterator find_if_not(InputIterator first, InputIterator last,
                                        Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    ForwardIterator find_if_not(ExecutionPolicy&& exec,         // freestanding-deleted, see [algorithms.parallel.overloads]
                                ForwardIterator first, ForwardIterator last,
                                Predicate pred);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      constexpr I find(I first, S last, const T& value, Proj proj = {});
    template<input_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      constexpr borrowed_iterator_t<R>
        find(R&& r, const T& value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      I find(Ep&& exec, I first, S last, const T& value, Proj proj = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      borrowed_iterator_t<R>
        find(Ep&& exec, R&& r, const T& value, Proj proj = {});             // freestanding-deleted

    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr I find_if(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr borrowed_iterator_t<R>
        find_if(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      I find_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      borrowed_iterator_t<R>
        find_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});               // freestanding-deleted

    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr I find_if_not(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr borrowed_iterator_t<R>
        find_if_not(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      I find_if_not(Ep&& exec, I first, S last, Pred pred, Proj proj = {}); // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      borrowed_iterator_t<R>
        find_if_not(Ep&& exec, R&& r, Pred pred, Proj proj = {});           // freestanding-deleted
  }

  // [alg.find.last], find last
  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      constexpr subrange<I> find_last(I first, S last, const T& value, Proj proj = {});
    template<forward_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires
        indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
      constexpr borrowed_subrange_t<R> find_last(R&& r, const T& value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      subrange<I>
        find_last(Ep&& exec, I first, S last, const T& value,
                  Proj proj = {});                                          // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires
        indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
      borrowed_subrange_t<R>
        find_last(Ep&& exec, R&& r, const T& value, Proj proj = {});        // freestanding-deleted

    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr subrange<I> find_last_if(I first, S last, Pred pred, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr borrowed_subrange_t<R> find_last_if(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      subrange<I>
        find_last_if(Ep&& exec, I first, S last, Pred pred,
                     Proj proj = {});                                       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R,
             class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      borrowed_subrange_t<R>
        find_last_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});          // freestanding-deleted

    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr subrange<I> find_last_if_not(I first, S last, Pred pred, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr borrowed_subrange_t<R> find_last_if_not(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      subrange<I>
        find_last_if_not(Ep&& exec, I first, S last, Pred pred,
                         Proj proj = {});                                   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      borrowed_subrange_t<R>
        find_last_if_not(Ep&& exec, R&& r, Pred pred, Proj proj = {});      // freestanding-deleted
  }

  // [alg.find.end], find end
  template<class ForwardIterator1, class ForwardIterator2>
    constexpr ForwardIterator1
      find_end(ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ForwardIterator1, class ForwardIterator2, class BinaryPredicate>
    constexpr ForwardIterator1
      find_end(ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2,
               BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator1
      find_end(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1,
           class ForwardIterator2, class BinaryPredicate>
    ForwardIterator1
      find_end(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2,
               BinaryPredicate pred);

  namespace ranges {
    template<forward_iterator I1, sentinel_for<I1> S1, forward_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr subrange<I1>
        find_end(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});
    template<forward_range R1, forward_range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr borrowed_subrange_t<R1>
        find_end(R1&& r1, R2&& r2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      subrange<I1>
        find_end(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});           // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      borrowed_subrange_t<R1>
        find_end(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});           // freestanding-deleted
  }

  // [alg.find.first.of], find first of
  template<class InputIterator, class ForwardIterator>
    constexpr InputIterator
      find_first_of(InputIterator first1, InputIterator last1,
                    ForwardIterator first2, ForwardIterator last2);
  template<class InputIterator, class ForwardIterator, class BinaryPredicate>
    constexpr InputIterator
      find_first_of(InputIterator first1, InputIterator last1,
                    ForwardIterator first2, ForwardIterator last2,
                    BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator1
      find_first_of(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    ForwardIterator1 first1, ForwardIterator1 last1,
                    ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1,
           class ForwardIterator2, class BinaryPredicate>
    ForwardIterator1
      find_first_of(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    ForwardIterator1 first1, ForwardIterator1 last1,
                    ForwardIterator2 first2, ForwardIterator2 last2,
                    BinaryPredicate pred);

  namespace ranges {
    template<input_iterator I1, sentinel_for<I1> S1, forward_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr I1 find_first_of(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, forward_range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr borrowed_iterator_t<R1>
        find_first_of(R1&& r1, R2&& r2, Pred pred = {},
                      Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      I1 find_first_of(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                       Proj1 proj1 = {}, Proj2 proj2 = {});     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      borrowed_iterator_t<R1>
        find_first_of(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                      Proj1 proj1 = {}, Proj2 proj2 = {});      // freestanding-deleted
  }

  // [alg.adjacent.find], adjacent find
  template<class ForwardIterator>
    constexpr ForwardIterator
      adjacent_find(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class BinaryPredicate>
    constexpr ForwardIterator
      adjacent_find(ForwardIterator first, ForwardIterator last,
                    BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator
      adjacent_find(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class BinaryPredicate>
    ForwardIterator
      adjacent_find(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    ForwardIterator first, ForwardIterator last,
                    BinaryPredicate pred);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_binary_predicate<projected<I, Proj>,
                                       projected<I, Proj>> Pred = ranges::equal_to>
      constexpr I adjacent_find(I first, S last, Pred pred = {},
                                Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_binary_predicate<projected<iterator_t<R>, Proj>,
                                       projected<iterator_t<R>, Proj>> Pred = ranges::equal_to>
      constexpr borrowed_iterator_t<R>
        adjacent_find(R&& r, Pred pred = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_binary_predicate<projected<I, Proj>,
                                       projected<I, Proj>> Pred = ranges::equal_to>
      I adjacent_find(Ep&& exec, I first, S last, Pred pred = {},
                      Proj proj = {});                                      // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_binary_predicate<projected<iterator_t<R>, Proj>,
                                       projected<iterator_t<R>, Proj>> Pred = ranges::equal_to>
      borrowed_iterator_t<R>
        adjacent_find(Ep&& exec, R&& r, Pred pred = {}, Proj proj = {});    // freestanding-deleted
  }

  // [alg.count], count
  template<class InputIterator, class T = iterator_traits<InputIterator>::value_type>
    constexpr typename iterator_traits<InputIterator>::difference_type
      count(InputIterator first, InputIterator last, const T& value);
  template<class ExecutionPolicy, class ForwardIterator,
           class T = iterator_traits<InputIterator>::value_type>
    typename iterator_traits<ForwardIterator>::difference_type
      count(ExecutionPolicy&& exec,                             // freestanding-deleted, see [algorithms.parallel.overloads]
            ForwardIterator first, ForwardIterator last, const T& value);
  template<class InputIterator, class Predicate>
    constexpr typename iterator_traits<InputIterator>::difference_type
      count_if(InputIterator first, InputIterator last, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    typename iterator_traits<ForwardIterator>::difference_type
      count_if(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator first, ForwardIterator last, Predicate pred);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      constexpr iter_difference_t<I>
        count(I first, S last, const T& value, Proj proj = {});
    template<input_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      constexpr range_difference_t<R>
        count(R&& r, const T& value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      iter_difference_t<I>
        count(Ep&& exec, I first, S last, const T& value, Proj proj = {});  // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      range_difference_t<R>
        count(Ep&& exec, R&& r, const T& value, Proj proj = {});            // freestanding-deleted

    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr iter_difference_t<I>
        count_if(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr range_difference_t<R>
        count_if(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      iter_difference_t<I>
        count_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      range_difference_t<R>
        count_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});              // freestanding-deleted
  }

  // [alg.mismatch], mismatch
  template<class InputIterator1, class InputIterator2>
    constexpr pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2);
  template<class InputIterator1, class InputIterator2, class BinaryPredicate>
    constexpr pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, BinaryPredicate pred);
  template<class InputIterator1, class InputIterator2>
    constexpr pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, InputIterator2 last2);
  template<class InputIterator1, class InputIterator2, class BinaryPredicate>
    constexpr pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, InputIterator2 last2,
               BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    pair<ForwardIterator1, ForwardIterator2>
      mismatch(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryPredicate>
    pair<ForwardIterator1, ForwardIterator2>
      mismatch(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    pair<ForwardIterator1, ForwardIterator2>
      mismatch(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryPredicate>
    pair<ForwardIterator1, ForwardIterator2>
      mismatch(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2,
               BinaryPredicate pred);

  namespace ranges {
    template<class I1, class I2>
      using mismatch_result = in_in_result<I1, I2>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr mismatch_result<I1, I2>
        mismatch(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr mismatch_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
        mismatch(R1&& r1, R2&& r2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      mismatch_result<I1, I2>
        mismatch(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});           // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      mismatch_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
        mismatch(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                 Proj1 proj1 = {}, Proj2 proj2 = {});           // freestanding-deleted
  }

  // [alg.equal], equal
  template<class InputIterator1, class InputIterator2>
    constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2);
  template<class InputIterator1, class InputIterator2, class BinaryPredicate>
    constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, BinaryPredicate pred);
  template<class InputIterator1, class InputIterator2>
    constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2);
  template<class InputIterator1, class InputIterator2, class BinaryPredicate>
    constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    bool equal(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryPredicate>
    bool equal(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    bool equal(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryPredicate>
    bool equal(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2,
               BinaryPredicate pred);

  namespace ranges {
    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr bool equal(I1 first1, S1 last1, I2 first2, S2 last2,
                           Pred pred = {},
                           Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr bool equal(R1&& r1, R2&& r2, Pred pred = {},
                           Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      bool equal(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                 Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      bool equal(Ep&& exec, R1&& r1, R2&& r2,
                 Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});       // freestanding-deleted
  }

  // [alg.is.permutation], is permutation
  template<class ForwardIterator1, class ForwardIterator2>
    constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                  ForwardIterator2 first2);
  template<class ForwardIterator1, class ForwardIterator2, class BinaryPredicate>
    constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                  ForwardIterator2 first2, BinaryPredicate pred);
  template<class ForwardIterator1, class ForwardIterator2>
    constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                  ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ForwardIterator1, class ForwardIterator2, class BinaryPredicate>
    constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                  ForwardIterator2 first2, ForwardIterator2 last2,
                                  BinaryPredicate pred);

  namespace ranges {
    template<forward_iterator I1, sentinel_for<I1> S1, forward_iterator I2,
             sentinel_for<I2> S2, class Proj1 = identity, class Proj2 = identity,
             indirect_equivalence_relation<projected<I1, Proj1>,
                                           projected<I2, Proj2>> Pred = ranges::equal_to>
      constexpr bool is_permutation(I1 first1, S1 last1, I2 first2, S2 last2,
                                    Pred pred = {},
                                    Proj1 proj1 = {}, Proj2 proj2 = {});
    template<forward_range R1, forward_range R2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_equivalence_relation<projected<iterator_t<R1>, Proj1>,
                                           projected<iterator_t<R2>, Proj2>>
                                           Pred = ranges::equal_to>
      constexpr bool is_permutation(R1&& r1, R2&& r2, Pred pred = {},
                                    Proj1 proj1 = {}, Proj2 proj2 = {});
  }

  // [alg.search], search
  template<class ForwardIterator1, class ForwardIterator2>
    constexpr ForwardIterator1
      search(ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ForwardIterator1, class ForwardIterator2, class BinaryPredicate>
    constexpr ForwardIterator1
      search(ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator1
      search(ExecutionPolicy&& exec,                            // freestanding-deleted, see [algorithms.parallel.overloads]
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryPredicate>
    ForwardIterator1
      search(ExecutionPolicy&& exec,                            // freestanding-deleted, see [algorithms.parallel.overloads]
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);

  namespace ranges {
    template<forward_iterator I1, sentinel_for<I1> S1, forward_iterator I2,
             sentinel_for<I2> S2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr subrange<I1>
        search(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
               Proj1 proj1 = {}, Proj2 proj2 = {});
    template<forward_range R1, forward_range R2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr borrowed_subrange_t<R1>
        search(R1&& r1, R2&& r2, Pred pred = {},
               Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      subrange<I1>
        search(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
               Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      borrowed_subrange_t<R1>
        search(Ep&& exec, R1&& r1, R2&& r2,
               Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});         // freestanding-deleted
  }

  template<class ForwardIterator, class Size,
           class T = iterator_traits<ForwardIterator>::value_type>
    constexpr ForwardIterator
      search_n(ForwardIterator first, ForwardIterator last,
               Size count, const T& value);
  template<class ForwardIterator, class Size,
           class T = iterator_traits<ForwardIterator>::value_type, class BinaryPredicate>
    constexpr ForwardIterator
      search_n(ForwardIterator first, ForwardIterator last,
               Size count, const T& value, BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Size,
           class T = iterator_traits<ForwardIterator>::value_type>
    ForwardIterator
      search_n(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator first, ForwardIterator last,
               Size count, const T& value);
  template<class ExecutionPolicy, class ForwardIterator, class Size,
           class T = iterator_traits<ForwardIterator>::value_type, class BinaryPredicate>
    ForwardIterator
      search_n(ExecutionPolicy&& exec,                          // freestanding-deleted, see [algorithms.parallel.overloads]
               ForwardIterator first, ForwardIterator last,
               Size count, const T& value,
               BinaryPredicate pred);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S,
             class Pred = ranges::equal_to, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirectly_comparable<I, const T*, Pred, Proj>
      constexpr subrange<I>
        search_n(I first, S last, iter_difference_t<I> count,
                 const T& value, Pred pred = {}, Proj proj = {});
    template<forward_range R, class Pred = ranges::equal_to,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirectly_comparable<iterator_t<R>, const T*, Pred, Proj>
      constexpr borrowed_subrange_t<R>
        search_n(R&& r, range_difference_t<R> count,
                 const T& value, Pred pred = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Pred = ranges::equal_to, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirectly_comparable<I, const T*, Pred, Proj>
      subrange<I>
        search_n(Ep&& exec, I first, S last, iter_difference_t<I> count,
                 const T& value, Pred pred = {}, Proj proj = {});           // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Pred = ranges::equal_to,
             class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirectly_comparable<iterator_t<R>, const T*, Pred, Proj>
      borrowed_subrange_t<R>
        search_n(Ep&& exec, R&& r, range_difference_t<R> count,
                 const T& value, Pred pred = {}, Proj proj = {});           // freestanding-deleted
  }

  template<class ForwardIterator, class Searcher>
    constexpr ForwardIterator
      search(ForwardIterator first, ForwardIterator last, const Searcher& searcher);

  namespace ranges {
    // [alg.starts.with], starts with
    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr bool starts_with(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr bool starts_with(R1&& r1, R2&& r2, Pred pred = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      bool starts_with(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                       Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {}); // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1,
             sized-random-access-range R2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      bool starts_with(Ep&& exec, R1&& r1, R2&& r2,
                       Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {}); // freestanding-deleted

    // [alg.ends.with], ends with
    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires (forward_iterator<I1> || sized_sentinel_for<S1, I1>) &&
               (forward_iterator<I2> || sized_sentinel_for<S2, I2>) &&
               indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      constexpr bool ends_with(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                               Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires (forward_range<R1> || sized_range<R1>) &&
               (forward_range<R2> || sized_range<R2>) &&
               indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      constexpr bool ends_with(R1&& r1, R2&& r2, Pred pred = {},
                               Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
      bool ends_with(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                     Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1,
             sized-random-access-range R2, class Pred = ranges::equal_to,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
      bool ends_with(Ep&& exec, R1&& r1, R2&& r2,
                     Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});   // freestanding-deleted

    // [alg.fold], fold
    template<class F>
    class flipped {     // exposition only
      F f;              // exposition only

    public:
      template<class T, class U> requires invocable<F&, U, T>
      invoke_result_t<F&, U, T> operator()(T&&, U&&);
    };

    template<class F, class T, class I, class U>
      concept indirectly-binary-left-foldable-impl =  // exposition only
        movable<T> && movable<U> &&
        convertible_to<T, U> && invocable<F&, U, iter_reference_t<I>> &&
        assignable_from<U&, invoke_result_t<F&, U, iter_reference_t<I>>>;

    template<class F, class T, class I>
      concept indirectly-binary-left-foldable =      // exposition only
        copy_constructible<F> && indirectly_readable<I> &&
        invocable<F&, T, iter_reference_t<I>> &&
        convertible_to<invoke_result_t<F&, T, iter_reference_t<I>>,
               decay_t<invoke_result_t<F&, T, iter_reference_t<I>>>> &&
        indirectly-binary-left-foldable-impl<F, T, I,
                        decay_t<invoke_result_t<F&, T, iter_reference_t<I>>>>;

    template<class F, class T, class I>
      concept indirectly-binary-right-foldable =    // exposition only
        indirectly-binary-left-foldable<flipped<F>, T, I>;

    template<input_iterator I, sentinel_for<I> S, class T = iter_value_t<I>,
             indirectly-binary-left-foldable<T, I> F>
      constexpr auto fold_left(I first, S last, T init, F f);

    template<input_range R, class T = range_value_t<R>,
             indirectly-binary-left-foldable<T, iterator_t<R>> F>
      constexpr auto fold_left(R&& r, T init, F f);

    template<input_iterator I, sentinel_for<I> S,
             indirectly-binary-left-foldable<iter_value_t<I>, I> F>
      requires constructible_from<iter_value_t<I>, iter_reference_t<I>>
      constexpr auto fold_left_first(I first, S last, F f);

    template<input_range R, indirectly-binary-left-foldable<range_value_t<R>, iterator_t<R>> F>
      requires constructible_from<range_value_t<R>, range_reference_t<R>>
      constexpr auto fold_left_first(R&& r, F f);

    template<bidirectional_iterator I, sentinel_for<I> S, class T = iter_value_t<I>,
             indirectly-binary-right-foldable<T, I> F>
      constexpr auto fold_right(I first, S last, T init, F f);

    template<bidirectional_range R, class T = range_value_t<R>,
             indirectly-binary-right-foldable<T, iterator_t<R>> F>
      constexpr auto fold_right(R&& r, T init, F f);

    template<bidirectional_iterator I, sentinel_for<I> S,
             indirectly-binary-right-foldable<iter_value_t<I>, I> F>
      requires constructible_from<iter_value_t<I>, iter_reference_t<I>>
      constexpr auto fold_right_last(I first, S last, F f);

    template<bidirectional_range R,
             indirectly-binary-right-foldable<range_value_t<R>, iterator_t<R>> F>
      requires constructible_from<range_value_t<R>, range_reference_t<R>>
      constexpr auto fold_right_last(R&& r, F f);

    template<class I, class T>
      using fold_left_with_iter_result = in_value_result<I, T>;
    template<class I, class T>
      using fold_left_first_with_iter_result = in_value_result<I, T>;

    template<input_iterator I, sentinel_for<I> S, class T = iter_value_t<I>,
             indirectly-binary-left-foldable<T, I> F>
      constexpr see below fold_left_with_iter(I first, S last, T init, F f);

    template<input_range R, class T = range_value_t<R>,
             indirectly-binary-left-foldable<T, iterator_t<R>> F>
      constexpr see below fold_left_with_iter(R&& r, T init, F f);

    template<input_iterator I, sentinel_for<I> S,
             indirectly-binary-left-foldable<iter_value_t<I>, I> F>
      requires constructible_from<iter_value_t<I>, iter_reference_t<I>>
      constexpr see below fold_left_first_with_iter(I first, S last, F f);

    template<input_range R,
             indirectly-binary-left-foldable<range_value_t<R>, iterator_t<R>> F>
      requires constructible_from<range_value_t<R>, range_reference_t<R>>
      constexpr see below fold_left_first_with_iter(R&& r, F f);
  }

  // [alg.modifying.operations], mutating sequence operations
  // [alg.copy], copy
  template<class InputIterator, class OutputIterator>
    constexpr OutputIterator copy(InputIterator first, InputIterator last,
                                  OutputIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2 copy(ExecutionPolicy&& exec,               // freestanding-deleted, see [algorithms.parallel.overloads]
                          ForwardIterator1 first, ForwardIterator1 last,
                          ForwardIterator2 result);

  namespace ranges {
    template<class I, class O>
      using copy_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O>
      requires indirectly_copyable<I, O>
      constexpr copy_result<I, O>
        copy(I first, S last, O result);
    template<input_range R, weakly_incrementable O>
      requires indirectly_copyable<iterator_t<R>, O>
      constexpr copy_result<borrowed_iterator_t<R>, O>
        copy(R&& r, O result);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS>
      requires indirectly_copyable<I, O>
      copy_result<I, O>
        copy(Ep&& exec, I first, S last, O result, OutS result_last);       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
      copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        copy(Ep&& exec, R&& r, OutR&& result_r);                            // freestanding-deleted
  }

  template<class InputIterator, class Size, class OutputIterator>
    constexpr OutputIterator copy_n(InputIterator first, Size n,
                                    OutputIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class Size,
           class ForwardIterator2>
    ForwardIterator2 copy_n(ExecutionPolicy&& exec,             // freestanding-deleted, see [algorithms.parallel.overloads]
                            ForwardIterator1 first, Size n,
                            ForwardIterator2 result);

  namespace ranges {
    template<class I, class O>
      using copy_n_result = in_out_result<I, O>;

    template<input_iterator I, weakly_incrementable O>
      requires indirectly_copyable<I, O>
      constexpr copy_n_result<I, O>
        copy_n(I first, iter_difference_t<I> n, O result);

    template<execution-policy Ep, random_access_iterator I, random_access_iterator O,
             sized_sentinel_for<O> OutS>
      requires indirectly_copyable<I, O>
      copy_n_result<I, O>
        copy_n(Ep&& exec, I first, iter_difference_t<I> n, O result,
               OutS result_last);                               // freestanding-deleted
  }

  template<class InputIterator, class OutputIterator, class Predicate>
    constexpr OutputIterator copy_if(InputIterator first, InputIterator last,
                                     OutputIterator result, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class Predicate>
    ForwardIterator2 copy_if(ExecutionPolicy&& exec,            // freestanding-deleted, see [algorithms.parallel.overloads]
                             ForwardIterator1 first, ForwardIterator1 last,
                             ForwardIterator2 result, Predicate pred);

  namespace ranges {
    template<class I, class O>
      using copy_if_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O>
      constexpr copy_if_result<I, O>
        copy_if(I first, S last, O result, Pred pred, Proj proj = {});
    template<input_range R, weakly_incrementable O, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, O>
      constexpr copy_if_result<borrowed_iterator_t<R>, O>
        copy_if(R&& r, O result, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O>
      copy_if_result<I, O>
        copy_if(Ep&& exec, I first, S last, O result, OutS result_last,
                Pred pred, Proj proj = {});                     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
      copy_if_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        copy_if(Ep&& exec, R&& r, OutR&& result_r, Pred pred,
                Proj proj = {});                                // freestanding-deleted
  }

  template<class BidirectionalIterator1, class BidirectionalIterator2>
    constexpr BidirectionalIterator2
      copy_backward(BidirectionalIterator1 first, BidirectionalIterator1 last,
                    BidirectionalIterator2 result);

  namespace ranges {
    template<class I1, class I2>
      using copy_backward_result = in_out_result<I1, I2>;

    template<bidirectional_iterator I1, sentinel_for<I1> S1, bidirectional_iterator I2>
      requires indirectly_copyable<I1, I2>
      constexpr copy_backward_result<I1, I2>
        copy_backward(I1 first, S1 last, I2 result);
    template<bidirectional_range R, bidirectional_iterator I>
      requires indirectly_copyable<iterator_t<R>, I>
      constexpr copy_backward_result<borrowed_iterator_t<R>, I>
        copy_backward(R&& r, I result);
  }

  // [alg.move], move
  template<class InputIterator, class OutputIterator>
    constexpr OutputIterator move(InputIterator first, InputIterator last,
                                  OutputIterator result);
  template<class ExecutionPolicy, class ForwardIterator1,
           class ForwardIterator2>
    ForwardIterator2 move(ExecutionPolicy&& exec,               // freestanding-deleted, see [algorithms.parallel.overloads]
                          ForwardIterator1 first, ForwardIterator1 last,
                          ForwardIterator2 result);

  namespace ranges {
    template<class I, class O>
      using move_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O>
      requires indirectly_movable<I, O>
      constexpr move_result<I, O>
        move(I first, S last, O result);
    template<input_range R, weakly_incrementable O>
      requires indirectly_movable<iterator_t<R>, O>
      constexpr move_result<borrowed_iterator_t<R>, O>
        move(R&& r, O result);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS>
      requires indirectly_movable<I, O>
      move_result<I, O>
        move(Ep&& exec, I first, S last, O result, OutS result_last);       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
      requires indirectly_movable<iterator_t<R>, iterator_t<OutR>>
      move_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        move(Ep&& exec, R&& r, OutR&& result_r);                            // freestanding-deleted
  }

  template<class BidirectionalIterator1, class BidirectionalIterator2>
    constexpr BidirectionalIterator2
      move_backward(BidirectionalIterator1 first, BidirectionalIterator1 last,
                    BidirectionalIterator2 result);

  namespace ranges {
    template<class I1, class I2>
      using move_backward_result = in_out_result<I1, I2>;

    template<bidirectional_iterator I1, sentinel_for<I1> S1, bidirectional_iterator I2>
      requires indirectly_movable<I1, I2>
      constexpr move_backward_result<I1, I2>
        move_backward(I1 first, S1 last, I2 result);
    template<bidirectional_range R, bidirectional_iterator I>
      requires indirectly_movable<iterator_t<R>, I>
      constexpr move_backward_result<borrowed_iterator_t<R>, I>
        move_backward(R&& r, I result);
  }

  // [alg.swap], swap
  template<class ForwardIterator1, class ForwardIterator2>
    constexpr ForwardIterator2 swap_ranges(ForwardIterator1 first1, ForwardIterator1 last1,
                                           ForwardIterator2 first2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2 swap_ranges(ExecutionPolicy&& exec,        // freestanding-deleted, see [algorithms.parallel.overloads]
                                 ForwardIterator1 first1, ForwardIterator1 last1,
                                 ForwardIterator2 first2);

  namespace ranges {
    template<class I1, class I2>
      using swap_ranges_result = in_in_result<I1, I2>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2>
      requires indirectly_swappable<I1, I2>
      constexpr swap_ranges_result<I1, I2>
        swap_ranges(I1 first1, S1 last1, I2 first2, S2 last2);
    template<input_range R1, input_range R2>
      requires indirectly_swappable<iterator_t<R1>, iterator_t<R2>>
      constexpr swap_ranges_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
        swap_ranges(R1&& r1, R2&& r2);

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2>
      requires indirectly_swappable<I1, I2>
      swap_ranges_result<I1, I2>
        swap_ranges(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2);   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2>
      requires indirectly_swappable<iterator_t<R1>, iterator_t<R2>>
      swap_ranges_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
        swap_ranges(Ep&& exec, R1&& r1, R2&& r2);                           // freestanding-deleted
  }

  template<class ForwardIterator1, class ForwardIterator2>
    constexpr void iter_swap(ForwardIterator1 a, ForwardIterator2 b);

  // [alg.transform], transform
  template<class InputIterator, class OutputIterator, class UnaryOperation>
    constexpr OutputIterator
      transform(InputIterator first1, InputIterator last1,
                OutputIterator result, UnaryOperation op);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
           class BinaryOperation>
    constexpr OutputIterator
      transform(InputIterator1 first1, InputIterator1 last1,
                InputIterator2 first2, OutputIterator result,
                BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class UnaryOperation>
    ForwardIterator2
      transform(ExecutionPolicy&& exec,                         // freestanding-deleted, see [algorithms.parallel.overloads]
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 result, UnaryOperation op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator, class BinaryOperation>
    ForwardIterator
      transform(ExecutionPolicy&& exec,                         // freestanding-deleted, see [algorithms.parallel.overloads]
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2, ForwardIterator result,
                BinaryOperation binary_op);

  namespace ranges {
    template<class I, class O>
      using unary_transform_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
             copy_constructible F, class Proj = identity>
      requires indirectly_writable<O, indirect_result_t<F&, projected<I, Proj>>>
      constexpr unary_transform_result<I, O>
        transform(I first1, S last1, O result, F op, Proj proj = {});
    template<input_range R, weakly_incrementable O, copy_constructible F,
             class Proj = identity>
      requires indirectly_writable<O, indirect_result_t<F&, projected<iterator_t<R>, Proj>>>
      constexpr unary_transform_result<borrowed_iterator_t<R>, O>
        transform(R&& r, O result, F op, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS,
             copy_constructible F, class Proj = identity>
      requires indirectly_writable<O, indirect_result_t<F&, projected<I, Proj>>>
      unary_transform_result<I, O>
        transform(Ep&& exec, I first1, S last1, O result, OutS result_last,
                  F op, Proj proj = {});                                    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             copy_constructible F, class Proj = identity>
      requires indirectly_writable<iterator_t<OutR>,
                                   indirect_result_t<F&, projected<iterator_t<R>, Proj>>>
      unary_transform_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        transform(Ep&& exec, R&& r, OutR&& result_r, F op, Proj proj = {}); // freestanding-deleted

    template<class I1, class I2, class O>
      using binary_transform_result = in_in_out_result<I1, I2, O>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             weakly_incrementable O, copy_constructible F, class Proj1 = identity,
             class Proj2 = identity>
      requires indirectly_writable<O, indirect_result_t<F&, projected<I1, Proj1>,
                                   projected<I2, Proj2>>>
      constexpr binary_transform_result<I1, I2, O>
        transform(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                  F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, weakly_incrementable O,
             copy_constructible F, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_writable<O, indirect_result_t<F&, projected<iterator_t<R1>, Proj1>,
                                   projected<iterator_t<R2>, Proj2>>>
      constexpr binary_transform_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
        transform(R1&& r1, R2&& r2, O result,
                  F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             random_access_iterator O, sized_sentinel_for<O> OutS,
             copy_constructible F, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_writable<O, indirect_result_t<F&, projected<I1, Proj1>,
                                   projected<I2, Proj2>>>
      binary_transform_result<I1, I2, O>
        transform(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                  O result, OutS result_last,
                  F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             sized-random-access-range OutR, copy_constructible F,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_writable<iterator_t<OutR>,
                                   indirect_result_t<F&, projected<iterator_t<R1>, Proj1>,
                                   projected<iterator_t<R2>, Proj2>>>
      binary_transform_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                              borrowed_iterator_t<OutR>>
        transform(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r,
                  F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});         // freestanding-deleted
  }

  // [alg.replace], replace
  template<class ForwardIterator, class T>
    constexpr void replace(ForwardIterator first, ForwardIterator last,
                           const T& old_value, const T& new_value);
  template<class ExecutionPolicy, class ForwardIterator,
           class T = iterator_traits<ForwardIterator>::value_type>
    void replace(ExecutionPolicy&& exec,                        // freestanding-deleted, see [algorithms.parallel.overloads]
                 ForwardIterator first, ForwardIterator last,
                 const T& old_value, const T& new_value);
  template<class ForwardIterator, class Predicate,
           class T = iterator_traits<ForwardIterator>::value_type>
    constexpr void replace_if(ForwardIterator first, ForwardIterator last,
                              Predicate pred, const T& new_value);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate,
           class T = iterator_traits<ForwardIterator>::value_type>
    void replace_if(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    ForwardIterator first, ForwardIterator last,
                    Predicate pred, const T& new_value);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             class T1 = projected_value_t<I, Proj>, class T2 = T1>
      requires indirectly_writable<I, const T2&> &&
               indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*>
      constexpr I
        replace(I first, S last, const T1& old_value, const T2& new_value, Proj proj = {});
    template<input_range R, class Proj = identity,
             class T1 = projected_value_t<iterator_t<R>, Proj>, class T2 = T1>
      requires indirectly_writable<iterator_t<R>, const T2&> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T1*>
      constexpr borrowed_iterator_t<R>
        replace(R&& r, const T1& old_value, const T2& new_value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T1 = projected_value_t<I, Proj>, class T2 = T1>
      requires indirectly_writable<I, const T2&> &&
               indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*>
      I replace(Ep&& exec, I first, S last,
                const T1& old_value, const T2& new_value, Proj proj = {});  // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T1 = projected_value_t<iterator_t<R>, Proj>, class T2 = T1>
      requires indirectly_writable<iterator_t<R>, const T2&> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T1*>
      borrowed_iterator_t<R>
        replace(Ep&& exec, R&& r, const T1& old_value, const T2& new_value,
                Proj proj = {});                                            // freestanding-deleted

    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_writable<I, const T&>
      constexpr I replace_if(I first, S last, Pred pred, const T& new_value, Proj proj = {});
    template<input_range R, class Proj = identity, class T = projected_value_t<I, Proj>,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_writable<iterator_t<R>, const T&>
      constexpr borrowed_iterator_t<R>
        replace_if(R&& r, Pred pred, const T& new_value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T = projected_value_t<I, Proj>,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_writable<I, const T&>
      I replace_if(Ep&& exec, I first, S last, Pred pred,
                   const T& new_value, Proj proj = {});         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_writable<iterator_t<R>, const T&>
      borrowed_iterator_t<R>
        replace_if(Ep&& exec, R&& r, Pred pred, const T& new_value,
                   Proj proj = {});                             // freestanding-deleted
  }

  template<class InputIterator, class OutputIterator, class T>
    constexpr OutputIterator replace_copy(InputIterator first, InputIterator last,
                                          OutputIterator result,
                                          const T& old_value, const T& new_value);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T>
    ForwardIterator2 replace_copy(ExecutionPolicy&& exec,       // freestanding-deleted, see [algorithms.parallel.overloads]
                                  ForwardIterator1 first, ForwardIterator1 last,
                                  ForwardIterator2 result,
                                  const T& old_value, const T& new_value);
  template<class InputIterator, class OutputIterator, class Predicate,
           class T = iterator_traits<OutputIterator>::value_type>
    constexpr OutputIterator replace_copy_if(InputIterator first, InputIterator last,
                                             OutputIterator result,
                                             Predicate pred, const T& new_value);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class Predicate, class T = iterator_traits<ForwardIterator2>::value_type>
    ForwardIterator2 replace_copy_if(ExecutionPolicy&& exec,    // freestanding-deleted, see [algorithms.parallel.overloads]
                                     ForwardIterator1 first, ForwardIterator1 last,
                                     ForwardIterator2 result,
                                     Predicate pred, const T& new_value);

  namespace ranges {
    template<class I, class O>
      using replace_copy_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, class O,
             class Proj = identity,
             class T1 = projected_value_t<I, Proj>, class T2 = iter_value_t<O>>
      requires indirectly_copyable<I, O> &&
               indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*> &&
               output_iterator<O, const T2&>
      constexpr replace_copy_result<I, O>
        replace_copy(I first, S last, O result, const T1& old_value, const T2& new_value,
                     Proj proj = {});
    template<input_range R, class O, class Proj = identity,
             class T1 = projected_value_t<iterator_t<R>, Proj>, class T2 = iter_value_t<O>>
      requires indirectly_copyable<iterator_t<R>, O> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T1*> &&
               output_iterator<O, const T2&>
      constexpr replace_copy_result<borrowed_iterator_t<R>, O>
        replace_copy(R&& r, O result, const T1& old_value, const T2& new_value,
                     Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS,
             class Proj = identity,
             class T1 = projected_value_t<I, Proj>, class T2 = iter_value_t<O>>
      requires indirectly_copyable<I, O> &&
               indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*> &&
               indirectly_writable<O, const T2&>
      replace_copy_result<I, O>
        replace_copy(Ep&& exec, I first, S last, O result, OutS result_last, const T1& old_value,
                     const T2& new_value, Proj proj = {});      // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             class Proj = identity, class T1 = projected_value_t<iterator_t<R>, Proj>,
             class T2 = range_value_t<OutR>>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T1*> &&
               indirectly_writable<iterator_t<OutR>, const T2&>
      replace_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        replace_copy(Ep&& exec, R&& r, OutR&& result_r, const T1& old_value, const T2& new_value,
                     Proj proj = {});                           // freestanding-deleted

    template<class I, class O>
      using replace_copy_if_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, class O, class T = iter_value_t<O>
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O> && output_iterator<O, const T&>
      constexpr replace_copy_if_result<I, O>
        replace_copy_if(I first, S last, O result, Pred pred, const T& new_value,
                        Proj proj = {});
    template<input_range R, class O, class T = iter_value_t<O>, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, O> && output_iterator<O, const T&>
      constexpr replace_copy_if_result<borrowed_iterator_t<R>, O>
        replace_copy_if(R&& r, O result, Pred pred, const T& new_value,
                        Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS, class T = iter_value_t<O>,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O> && indirectly_writable<O, const T&>
      replace_copy_if_result<I, O>
        replace_copy_if(Ep&& exec, I first, S last, O result, OutS result_last,
                        Pred pred, const T& new_value, Proj proj = {});     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             class T = range_value_t<OutR>, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>> &&
               indirectly_writable<iterator_t<OutR>, const T&>
      replace_copy_if_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        replace_copy_if(Ep&& exec, R&& r, OutR&& result_r, Pred pred, const T& new_value,
                        Proj proj = {});                                    // freestanding-deleted
  }

  // [alg.fill], fill
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
    constexpr void fill(ForwardIterator first, ForwardIterator last, const T& value);
  template<class ExecutionPolicy, class ForwardIterator,
           class T = iterator_traits<ForwardIterator>::value_type>
    void fill(ExecutionPolicy&& exec,                           // freestanding-deleted, see [algorithms.parallel.overloads]
              ForwardIterator first, ForwardIterator last, const T& value);
  template<class OutputIterator, class Size,
           class T = iterator_traits<OutputIterator>::value_type>
    constexpr OutputIterator fill_n(OutputIterator first, Size n, const T& value)
  template<class ExecutionPolicy, class ForwardIterator,
           class Size, class T = iterator_traits<ForwardIterator>::value_type>
    ForwardIterator fill_n(ExecutionPolicy&& exec,              // freestanding-deleted, see [algorithms.parallel.overloads]
                           ForwardIterator first, Size n, const T& value);

  namespace ranges {
    template<class O, sentinel_for<O> S, class T = iter_value_t<O>>
      requires output_iterator<O, const T&>
      constexpr O fill(O first, S last, const T& value);
    template<class R, class T = range_value_t<R>>
      requires output_range<R, const T&>
      constexpr borrowed_iterator_t<R> fill(R&& r, const T& value);
    template<class O, class T = iter_value_t<O>>
      requires output_iterator<O, const T&>
      constexpr O fill_n(O first, iter_difference_t<O> n, const T& value);

    template<execution-policy Ep, random_access_iterator O, sized_sentinel_for<O> S,
             class T = iter_value_t<O>>
      requires indirectly_writable<O, const T&>
      O fill(Ep&& exec, O first, S last, const T& value);                   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class T = range_value_t<R>>
      requires indirectly_writable<iterator_t<R>, const T&>
      borrowed_iterator_t<R> fill(Ep&& exec, R&& r, const T& value);        // freestanding-deleted
    template<execution-policy Ep, random_access_iterator O, class T = iter_value_t<O>>
      requires indirectly_writable<O, const T&>
      O fill_n(Ep&& exec, O first, iter_difference_t<O> n, const T& value); // freestanding-deleted
  }

  // [alg.generate], generate
  template<class ForwardIterator, class Generator>
    constexpr void generate(ForwardIterator first, ForwardIterator last,
                            Generator gen);
  template<class ExecutionPolicy, class ForwardIterator, class Generator>
    void generate(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator first, ForwardIterator last,
                  Generator gen);
  template<class OutputIterator, class Size, class Generator>
    constexpr OutputIterator generate_n(OutputIterator first, Size n, Generator gen);
  template<class ExecutionPolicy, class ForwardIterator, class Size, class Generator>
    ForwardIterator generate_n(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator first, Size n, Generator gen);

  namespace ranges {
    template<input_or_output_iterator O, sentinel_for<O> S, copy_constructible F>
      requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
      constexpr O generate(O first, S last, F gen);
    template<class R, copy_constructible F>
      requires invocable<F&> && output_range<R, invoke_result_t<F&>>
      constexpr borrowed_iterator_t<R> generate(R&& r, F gen);
    template<input_or_output_iterator O, copy_constructible F>
      requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
      constexpr O generate_n(O first, iter_difference_t<O> n, F gen);
    template<execution-policy Ep, random_access_iterator O, sized_sentinel_for<O> S,
             copy_constructible F>
      requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
      O generate(Ep&& exec, O first, S last, F gen);                        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, copy_constructible F>
      requires invocable<F&> && indirectly_writable<iterator_t<R>, invoke_result_t<F&>>
      borrowed_iterator_t<R> generate(Ep&& exec, R&& r, F gen);             // freestanding-deleted
    template<execution-policy Ep, random_access_iterator O, copy_constructible F>
      requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
      O generate_n(Ep&& exec, O first, iter_difference_t<O> n, F gen);      // freestanding-deleted
  }

  // [alg.remove], remove
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
    constexpr ForwardIterator remove(ForwardIterator first, ForwardIterator last,
                                     const T& value);
  template<class ExecutionPolicy, class ForwardIterator,
           class T = iterator_traits<ForwardIterator>::value_type>
    ForwardIterator remove(ExecutionPolicy&& exec,              // freestanding-deleted, see [algorithms.parallel.overloads]
                           ForwardIterator first, ForwardIterator last,
                           const T& value);
  template<class ForwardIterator, class Predicate>
    constexpr ForwardIterator remove_if(ForwardIterator first, ForwardIterator last,
                                        Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    ForwardIterator remove_if(ExecutionPolicy&& exec,           // freestanding-deleted, see [algorithms.parallel.overloads]
                              ForwardIterator first, ForwardIterator last,
                              Predicate pred);

  namespace ranges {
    template<permutable I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      constexpr subrange<I> remove(I first, S last, const T& value, Proj proj = {});
    template<forward_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires permutable<iterator_t<R>> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      constexpr borrowed_subrange_t<R>
        remove(R&& r, const T& value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      subrange<I> remove(Ep&& exec, I first, S last, const T& value,
                         Proj proj = {});                                   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires permutable<iterator_t<R>> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      borrowed_subrange_t<R>
        remove(Ep&& exec, R&& r, const T& value, Proj proj = {});           // freestanding-deleted

    template<permutable I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr subrange<I> remove_if(I first, S last, Pred pred, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R>
        remove_if(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      subrange<I>
        remove_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        remove_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});             // freestanding-deleted
  }

  template<class InputIterator, class OutputIterator,
           class T = iterator_traits<InputIterator>::value_type>
    constexpr OutputIterator
      remove_copy(InputIterator first, InputIterator last,
                  OutputIterator result, const T& value);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class T = iterator_traits<ForwardIterator1>::value_type>
    ForwardIterator2
      remove_copy(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator1 first, ForwardIterator1 last,
                  ForwardIterator2 result, const T& value);
  template<class InputIterator, class OutputIterator, class Predicate>
    constexpr OutputIterator
      remove_copy_if(InputIterator first, InputIterator last,
                     OutputIterator result, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class Predicate>
    ForwardIterator2
      remove_copy_if(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first, ForwardIterator1 last,
                     ForwardIterator2 result, Predicate pred);

  namespace ranges {
    template<class I, class O>
      using remove_copy_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirectly_copyable<I, O> &&
               indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      constexpr remove_copy_result<I, O>
        remove_copy(I first, S last, O result, const T& value, Proj proj = {});
    template<input_range R, weakly_incrementable O, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirectly_copyable<iterator_t<R>, O> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      constexpr remove_copy_result<borrowed_iterator_t<R>, O>
        remove_copy(R&& r, O result, const T& value, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS,
             class Proj = identity, class T = projected_value_t<I, Proj>>
      requires indirectly_copyable<I, O> &&
               indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
      remove_copy_result<I, O>
        remove_copy(Ep&& exec, I first, S last, O result, OutS result_last, const T& value,
                    Proj proj = {});                                        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>> &&
               indirect_binary_predicate<ranges::equal_to,
                                         projected<iterator_t<R>, Proj>, const T*>
      remove_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        remove_copy(Ep&& exec, R&& r, OutR&& result_r, const T& value,
                    Proj proj = {});                                        // freestanding-deleted

    template<class I, class O>
      using remove_copy_if_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O>
      constexpr remove_copy_if_result<I, O>
        remove_copy_if(I first, S last, O result, Pred pred, Proj proj = {});
    template<input_range R, weakly_incrementable O, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, O>
      constexpr remove_copy_if_result<borrowed_iterator_t<R>, O>
        remove_copy_if(R&& r, O result, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O>
      remove_copy_if_result<I, O>
        remove_copy_if(Ep&& exec, I first, S last, O result, OutS result_last, Pred pred,
                       Proj proj = {});                         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
      remove_copy_if_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        remove_copy_if(Ep&& exec, R&& r, OutR&& result_r, Pred pred,
                       Proj proj = {});                         // freestanding-deleted
  }

  // [alg.unique], unique
  template<class ForwardIterator>
    constexpr ForwardIterator unique(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class BinaryPredicate>
    constexpr ForwardIterator unique(ForwardIterator first, ForwardIterator last,
                                     BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator unique(ExecutionPolicy&& exec,              // freestanding-deleted, see [algorithms.parallel.overloads]
                           ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class BinaryPredicate>
    ForwardIterator unique(ExecutionPolicy&& exec,              // freestanding-deleted, see [algorithms.parallel.overloads]
                           ForwardIterator first, ForwardIterator last,
                           BinaryPredicate pred);

  namespace ranges {
    template<permutable I, sentinel_for<I> S, class Proj = identity,
             indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
      constexpr subrange<I> unique(I first, S last, C comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R>
        unique(R&& r, C comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
      requires permutable<I>
      subrange<I> unique(Ep&& exec, I first, S last, C comp = {},
                         Proj proj = {});                       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        unique(Ep&& exec, R&& r, C comp = {}, Proj proj = {});  // freestanding-deleted
  }

  template<class InputIterator, class OutputIterator>
    constexpr OutputIterator
      unique_copy(InputIterator first, InputIterator last,
                  OutputIterator result);
  template<class InputIterator, class OutputIterator, class BinaryPredicate>
    constexpr OutputIterator
      unique_copy(InputIterator first, InputIterator last,
                  OutputIterator result, BinaryPredicate pred);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2
      unique_copy(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator1 first, ForwardIterator1 last,
                  ForwardIterator2 result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryPredicate>
    ForwardIterator2
      unique_copy(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator1 first, ForwardIterator1 last,
                  ForwardIterator2 result, BinaryPredicate pred);

  namespace ranges {
    template<class I, class O>
      using unique_copy_result = in_out_result<I, O>;

    template<input_iterator I, sentinel_for<I> S, weakly_incrementable O, class Proj = identity,
             indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
      requires indirectly_copyable<I, O> &&
               (forward_iterator<I> ||
                (input_iterator<O> && same_as<iter_value_t<I>, iter_value_t<O>>) ||
                indirectly_copyable_storable<I, O>)
      constexpr unique_copy_result<I, O>
        unique_copy(I first, S last, O result, C comp = {}, Proj proj = {});
    template<input_range R, weakly_incrementable O, class Proj = identity,
             indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
      requires indirectly_copyable<iterator_t<R>, O> &&
               (forward_iterator<iterator_t<R>> ||
                (input_iterator<O> && same_as<range_value_t<R>, iter_value_t<O>>) ||
                indirectly_copyable_storable<iterator_t<R>, O>)
      constexpr unique_copy_result<borrowed_iterator_t<R>, O>
        unique_copy(R&& r, O result, C comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS, class Proj = identity,
             indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
      requires indirectly_copyable<I, O>
      unique_copy_result<I, O>
        unique_copy(Ep&& exec, I first, S last, O result, OutS result_last, C comp = {},
                    Proj proj = {});                            // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
             class Proj = identity,
             indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
      unique_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        unique_copy(Ep&& exec, R&& r, OutR&& result_r, C comp = {},
                    Proj proj = {});                            // freestanding-deleted
  }

  // [alg.reverse], reverse
  template<class BidirectionalIterator>
    constexpr void reverse(BidirectionalIterator first, BidirectionalIterator last);
  template<class ExecutionPolicy, class BidirectionalIterator>
    void reverse(ExecutionPolicy&& exec,                        // freestanding-deleted, see [algorithms.parallel.overloads]
                 BidirectionalIterator first, BidirectionalIterator last);

  namespace ranges {
    template<bidirectional_iterator I, sentinel_for<I> S>
      requires permutable<I>
      constexpr I reverse(I first, S last);
    template<bidirectional_range R>
      requires permutable<iterator_t<R>>
      constexpr borrowed_iterator_t<R> reverse(R&& r);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
      requires permutable<I>
      I reverse(Ep&& exec, I first, S last);                    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R>
      requires permutable<iterator_t<R>>
      borrowed_iterator_t<R> reverse(Ep&& exec, R&& r);         // freestanding-deleted
  }

  template<class BidirectionalIterator, class OutputIterator>
    constexpr OutputIterator
      reverse_copy(BidirectionalIterator first, BidirectionalIterator last,
                   OutputIterator result);
  template<class ExecutionPolicy, class BidirectionalIterator, class ForwardIterator>
    ForwardIterator
      reverse_copy(ExecutionPolicy&& exec,                      // freestanding-deleted, see [algorithms.parallel.overloads]
                   BidirectionalIterator first, BidirectionalIterator last,
                   ForwardIterator result);

  namespace ranges {
    template<class I, class O>
      using reverse_copy_result = in_out_result<I, O>;
    template<class I, class O>
      using reverse_copy_truncated_result = in_in_out_result<I, I, O>;

    template<bidirectional_iterator I, sentinel_for<I> S, weakly_incrementable O>
      requires indirectly_copyable<I, O>
      constexpr reverse_copy_result<I, O>
        reverse_copy(I first, S last, O result);
    template<bidirectional_range R, weakly_incrementable O>
      requires indirectly_copyable<iterator_t<R>, O>
      constexpr reverse_copy_result<borrowed_iterator_t<R>, O>
        reverse_copy(R&& r, O result);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS>
      requires indirectly_copyable<I, O>
      reverse_copy_truncated_result<I, O>
        reverse_copy(Ep&& exec, I first, S last, O result,
                     OutS result_last);                         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
      reverse_copy_truncated_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        reverse_copy(Ep&& exec, R&& r, OutR&& result_r);        // freestanding-deleted
  }

  // [alg.rotate], rotate
  template<class ForwardIterator>
    constexpr ForwardIterator rotate(ForwardIterator first,
                                     ForwardIterator middle,
                                     ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator rotate(ExecutionPolicy&& exec,              // freestanding-deleted, see [algorithms.parallel.overloads]
                           ForwardIterator first,
                           ForwardIterator middle,
                           ForwardIterator last);

  namespace ranges {
    template<permutable I, sentinel_for<I> S>
      constexpr subrange<I> rotate(I first, I middle, S last);
    template<forward_range R>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R> rotate(R&& r, iterator_t<R> middle);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
      requires permutable<I>
      subrange<I>
        rotate(Ep&& exec, I first, I middle, S last);           // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        rotate(Ep&& exec, R&& r, iterator_t<R> middle);         // freestanding-deleted
  }

  template<class ForwardIterator, class OutputIterator>
    constexpr OutputIterator
      rotate_copy(ForwardIterator first, ForwardIterator middle,
                  ForwardIterator last, OutputIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2
      rotate_copy(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator1 first, ForwardIterator1 middle,
                  ForwardIterator1 last, ForwardIterator2 result);

  namespace ranges {
    template<class I, class O>
      using rotate_copy_result = in_out_result<I, O>;
    template<class I, class O>
      using rotate_copy_truncated_result = in_in_out_result<I, I, O>;

    template<forward_iterator I, sentinel_for<I> S, weakly_incrementable O>
      requires indirectly_copyable<I, O>
      constexpr rotate_copy_result<I, O>
        rotate_copy(I first, I middle, S last, O result);
    template<forward_range R, weakly_incrementable O>
      requires indirectly_copyable<iterator_t<R>, O>
      constexpr rotate_copy_result<borrowed_iterator_t<R>, O>
        rotate_copy(R&& r, iterator_t<R> middle, O result);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O, sized_sentinel_for<O> OutS>
      requires indirectly_copyable<I, O>
      rotate_copy_truncated_result<I, O>
        rotate_copy(Ep&& exec, I first, I middle, S last, O result,     // freestanding-deleted
                    OutS result_last);
    template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
      rotate_copy_truncated_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
        rotate_copy(Ep&& exec, R&& r, iterator_t<R> middle,             // freestanding-deleted
                    OutR&& result_r);
  }

  // [alg.random.sample], sample
  template<class PopulationIterator, class SampleIterator,
           class Distance, class UniformRandomBitGenerator>
    SampleIterator sample(PopulationIterator first, PopulationIterator last,
                          SampleIterator out, Distance n,
                          UniformRandomBitGenerator&& g);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S,
             weakly_incrementable O, class Gen>
      requires (forward_iterator<I> || random_access_iterator<O>) &&
               indirectly_copyable<I, O> &&
               uniform_random_bit_generator<remove_reference_t<Gen>>
      O sample(I first, S last, O out, iter_difference_t<I> n, Gen&& g);
    template<input_range R, weakly_incrementable O, class Gen>
      requires (forward_range<R> || random_access_iterator<O>) &&
               indirectly_copyable<iterator_t<R>, O> &&
               uniform_random_bit_generator<remove_reference_t<Gen>>
      O sample(R&& r, O out, range_difference_t<R> n, Gen&& g);
  }

  // [alg.random.shuffle], shuffle
  template<class RandomAccessIterator, class UniformRandomBitGenerator>
    void shuffle(RandomAccessIterator first,
                 RandomAccessIterator last,
                 UniformRandomBitGenerator&& g);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Gen>
      requires permutable<I> &&
               uniform_random_bit_generator<remove_reference_t<Gen>>
      I shuffle(I first, S last, Gen&& g);
    template<random_access_range R, class Gen>
      requires permutable<iterator_t<R>> &&
               uniform_random_bit_generator<remove_reference_t<Gen>>
      borrowed_iterator_t<R> shuffle(R&& r, Gen&& g);
  }

  // [alg.shift], shift
  template<class ForwardIterator>
    constexpr ForwardIterator
      shift_left(ForwardIterator first, ForwardIterator last,
                 typename iterator_traits<ForwardIterator>::difference_type n);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator
      shift_left(ExecutionPolicy&& exec,                        // freestanding-deleted, see [algorithms.parallel.overloads]
                 ForwardIterator first, ForwardIterator last,
                 typename iterator_traits<ForwardIterator>::difference_type n);

  namespace ranges {
    template<permutable I, sentinel_for<I> S>
      constexpr subrange<I> shift_left(I first, S last, iter_difference_t<I> n);
    template<forward_range R>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R> shift_left(R&& r, range_difference_t<R> n);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
      requires permutable<I>
      subrange<I>
        shift_left(Ep&& exec, I first, S last, iter_difference_t<I> n);     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        shift_left(Ep&& exec, R&& r, range_difference_t<R> n);              // freestanding-deleted
  }

  template<class ForwardIterator>
    constexpr ForwardIterator
      shift_right(ForwardIterator first, ForwardIterator last,
                  typename iterator_traits<ForwardIterator>::difference_type n);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator
      shift_right(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator first, ForwardIterator last,
                  typename iterator_traits<ForwardIterator>::difference_type n);

  namespace ranges {
    template<permutable I, sentinel_for<I> S>
      constexpr subrange<I> shift_right(I first, S last, iter_difference_t<I> n);
    template<forward_range R>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R> shift_right(R&& r, range_difference_t<R> n);

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
      requires permutable<I>
      subrange<I>
        shift_right(Ep&& exec, I first, S last, iter_difference_t<I> n);    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        shift_right(Ep&& exec, R&& r, range_difference_t<R> n);             // freestanding-deleted
  }

  // [alg.sorting], sorting and related operations
  // [alg.sort], sorting
  template<class RandomAccessIterator>
    constexpr void sort(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void sort(RandomAccessIterator first, RandomAccessIterator last,
                        Compare comp);
  template<class ExecutionPolicy, class RandomAccessIterator>
    void sort(ExecutionPolicy&& exec,                           // freestanding-deleted, see [algorithms.parallel.overloads]
              RandomAccessIterator first, RandomAccessIterator last);
  template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
    void sort(ExecutionPolicy&& exec,                           // freestanding-deleted, see [algorithms.parallel.overloads]
              RandomAccessIterator first, RandomAccessIterator last,
              Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        sort(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        sort(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Comp = ranges::less, class Proj = identity>
      requires sortable<I, Comp, Proj>
      I sort(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      borrowed_iterator_t<R>
        sort(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});             // freestanding-deleted
  }

  template<class RandomAccessIterator>
    constexpr void stable_sort(RandomAccessIterator first, RandomAccessIterator last);  // hosted
  template<class RandomAccessIterator, class Compare>
    constexpr void stable_sort(RandomAccessIterator first, RandomAccessIterator last,   // hosted
                               Compare comp);
  template<class ExecutionPolicy, class RandomAccessIterator>
    void stable_sort(ExecutionPolicy&& exec,                    // hosted, see [algorithms.parallel.overloads]
                     RandomAccessIterator first, RandomAccessIterator last);
  template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
    void stable_sort(ExecutionPolicy&& exec,                    // hosted, see [algorithms.parallel.overloads]
                     RandomAccessIterator first, RandomAccessIterator last,
                     Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I stable_sort(I first, S last, Comp comp = {}, Proj proj = {});         // hosted
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        stable_sort(R&& r, Comp comp = {}, Proj proj = {});                             // hosted

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Comp = ranges::less, class Proj = identity>
      requires sortable<I, Comp, Proj>
      I stable_sort(Ep&& exec, I first, S last, Comp comp = {},
                    Proj proj = {});                                        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      borrowed_iterator_t<R>
        stable_sort(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});      // freestanding-deleted
  }

  template<class RandomAccessIterator>
    constexpr void partial_sort(RandomAccessIterator first, RandomAccessIterator middle,
                                RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void partial_sort(RandomAccessIterator first, RandomAccessIterator middle,
                                RandomAccessIterator last, Compare comp);
  template<class ExecutionPolicy, class RandomAccessIterator>
    void partial_sort(ExecutionPolicy&& exec,                   // freestanding-deleted, see [algorithms.parallel.overloads]
                      RandomAccessIterator first, RandomAccessIterator middle,
                      RandomAccessIterator last);
  template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
    void partial_sort(ExecutionPolicy&& exec,                   // freestanding-deleted, see [algorithms.parallel.overloads]
                      RandomAccessIterator first, RandomAccessIterator middle,
                      RandomAccessIterator last, Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        partial_sort(I first, I middle, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        partial_sort(R&& r, iterator_t<R> middle, Comp comp = {},
                     Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Comp = ranges::less, class Proj = identity>
      requires sortable<I, Comp, Proj>
      I partial_sort(Ep&& exec, I first, I middle, S last, Comp comp = {},
                     Proj proj = {});                           // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R,
             class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      borrowed_iterator_t<R>
        partial_sort(Ep&& exec, R&& r, iterator_t<R> middle, Comp comp = {},
                     Proj proj = {});                           // freestanding-deleted
  }

  template<class InputIterator, class RandomAccessIterator>
    constexpr RandomAccessIterator
      partial_sort_copy(InputIterator first, InputIterator last,
                        RandomAccessIterator result_first,
                        RandomAccessIterator result_last);
  template<class InputIterator, class RandomAccessIterator, class Compare>
    constexpr RandomAccessIterator
      partial_sort_copy(InputIterator first, InputIterator last,
                        RandomAccessIterator result_first,
                        RandomAccessIterator result_last,
                        Compare comp);
  template<class ExecutionPolicy, class ForwardIterator, class RandomAccessIterator>
    RandomAccessIterator
      partial_sort_copy(ExecutionPolicy&& exec,                 // freestanding-deleted, see [algorithms.parallel.overloads]
                        ForwardIterator first, ForwardIterator last,
                        RandomAccessIterator result_first,
                        RandomAccessIterator result_last);
  template<class ExecutionPolicy, class ForwardIterator, class RandomAccessIterator,
           class Compare>
    RandomAccessIterator
      partial_sort_copy(ExecutionPolicy&& exec,                 // freestanding-deleted, see [algorithms.parallel.overloads]
                        ForwardIterator first, ForwardIterator last,
                        RandomAccessIterator result_first,
                        RandomAccessIterator result_last,
                        Compare comp);

  namespace ranges {
    template<class I, class O>
      using partial_sort_copy_result = in_out_result<I, O>;

    template<input_iterator I1, sentinel_for<I1> S1,
             random_access_iterator I2, sentinel_for<I2> S2,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_copyable<I1, I2> && sortable<I2, Comp, Proj2> &&
               indirect_strict_weak_order<Comp, projected<I1, Proj1>, projected<I2, Proj2>>
      constexpr partial_sort_copy_result<I1, I2>
        partial_sort_copy(I1 first, S1 last, I2 result_first, S2 result_last,
                          Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, random_access_range R2, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires indirectly_copyable<iterator_t<R1>, iterator_t<R2>> &&
               sortable<iterator_t<R2>, Comp, Proj2> &&
               indirect_strict_weak_order<Comp, projected<iterator_t<R1>, Proj1>,
                                          projected<iterator_t<R2>, Proj2>>
      constexpr partial_sort_copy_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
        partial_sort_copy(R1&& r, R2&& result_r, Comp comp = {},
                          Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_copyable<I1, I2> && sortable<I2, Comp, Proj2> &&
               indirect_strict_weak_order<Comp, projected<I1, Proj1>, projected<I2, Proj2>>
      partial_sort_copy_result<I1, I2>
        partial_sort_copy(Ep&& exec, I1 first, S1 last, I2 result_first, S2 result_last,
                          Comp comp = {}, Proj1 proj1 = {},
                          Proj2 proj2 = {});                    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires indirectly_copyable<iterator_t<R1>, iterator_t<R2>> &&
               sortable<iterator_t<R2>, Comp, Proj2> &&
               indirect_strict_weak_order<Comp, projected<iterator_t<R1>, Proj1>,
                                          projected<iterator_t<R2>, Proj2>>
      partial_sort_copy_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
        partial_sort_copy(Ep&& exec, R1&& r, R2&& result_r, Comp comp = {},
                          Proj1 proj1 = {}, Proj2 proj2 = {});  // freestanding-deleted
  }

  template<class ForwardIterator>
    constexpr bool is_sorted(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    constexpr bool is_sorted(ForwardIterator first, ForwardIterator last,
                             Compare comp);
  template<class ExecutionPolicy, class ForwardIterator>
    bool is_sorted(ExecutionPolicy&& exec,                      // freestanding-deleted, see [algorithms.parallel.overloads]
                   ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class Compare>
    bool is_sorted(ExecutionPolicy&& exec,                      // freestanding-deleted, see [algorithms.parallel.overloads]
                   ForwardIterator first, ForwardIterator last,
                   Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr bool is_sorted(I first, S last, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr bool is_sorted(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      bool is_sorted(Ep&& exec, I first, S last, Comp comp = {},
                     Proj proj = {});                                       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      bool is_sorted(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});     // freestanding-deleted
  }

  template<class ForwardIterator>
    constexpr ForwardIterator
      is_sorted_until(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    constexpr ForwardIterator
      is_sorted_until(ForwardIterator first, ForwardIterator last,
                      Compare comp);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator
      is_sorted_until(ExecutionPolicy&& exec,                   // freestanding-deleted, see [algorithms.parallel.overloads]
                      ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class Compare>
    ForwardIterator
      is_sorted_until(ExecutionPolicy&& exec,                   // freestanding-deleted, see [algorithms.parallel.overloads]
                      ForwardIterator first, ForwardIterator last,
                      Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr I is_sorted_until(I first, S last, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr borrowed_iterator_t<R>
        is_sorted_until(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      I is_sorted_until(Ep&& exec, I first, S last, Comp comp = {},
                        Proj proj = {});                                    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      borrowed_iterator_t<R>
        is_sorted_until(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});  // freestanding-deleted
  }

  // [alg.nth.element], Nth element
  template<class RandomAccessIterator>
    constexpr void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                               RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                               RandomAccessIterator last, Compare comp);
  template<class ExecutionPolicy, class RandomAccessIterator>
    void nth_element(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     RandomAccessIterator first, RandomAccessIterator nth,
                     RandomAccessIterator last);
  template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
    void nth_element(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     RandomAccessIterator first, RandomAccessIterator nth,
                     RandomAccessIterator last, Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        nth_element(I first, I nth, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        nth_element(R&& r, iterator_t<R> nth, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Comp = ranges::less, class Proj = identity>
      requires sortable<I, Comp, Proj>
      I nth_element(Ep&& exec, I first, I nth, S last, Comp comp = {},
                    Proj proj = {});                            // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      borrowed_iterator_t<R>
        nth_element(Ep&& exec, R&& r, iterator_t<R> nth, Comp comp = {},
                    Proj proj = {});                            // freestanding-deleted
  }

  // [alg.binary.search], binary search
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
    constexpr ForwardIterator
      lower_bound(ForwardIterator first, ForwardIterator last,
                  const T& value);
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
           class Compare>
    constexpr ForwardIterator
      lower_bound(ForwardIterator first, ForwardIterator last,
                  const T& value, Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>,
             indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
      constexpr I lower_bound(I first, S last, const T& value, Comp comp = {},
                              Proj proj = {});
    template<forward_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>,
             indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
               ranges::less>
      constexpr borrowed_iterator_t<R>
        lower_bound(R&& r, const T& value, Comp comp = {}, Proj proj = {});
  }

  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
    constexpr ForwardIterator
      upper_bound(ForwardIterator first, ForwardIterator last,
                  const T& value);
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
           class Compare>
    constexpr ForwardIterator
      upper_bound(ForwardIterator first, ForwardIterator last,
                  const T& value, Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>
             indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
      constexpr I upper_bound(I first, S last, const T& value, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>,
             indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
               ranges::less>
      constexpr borrowed_iterator_t<R>
        upper_bound(R&& r, const T& value, Comp comp = {}, Proj proj = {});
  }

  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
    constexpr pair<ForwardIterator, ForwardIterator>
      equal_range(ForwardIterator first, ForwardIterator last,
                  const T& value);
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
           class Compare>
    constexpr pair<ForwardIterator, ForwardIterator>
      equal_range(ForwardIterator first, ForwardIterator last,
                  const T& value, Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj,
             indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
      constexpr subrange<I>
        equal_range(I first, S last, const T& value, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>,
             indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
               ranges::less>
      constexpr borrowed_subrange_t<R>
        equal_range(R&& r, const T& value, Comp comp = {}, Proj proj = {});
  }

  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
    constexpr bool
      binary_search(ForwardIterator first, ForwardIterator last,
                    const T& value);
  template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
           class Compare>
    constexpr bool
      binary_search(ForwardIterator first, ForwardIterator last,
                    const T& value, Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             class T = projected_value_t<I, Proj>,
             indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
      constexpr bool binary_search(I first, S last, const T& value, Comp comp = {},
                                   Proj proj = {});
    template<forward_range R, class Proj = identity,
             class T = projected_value_t<iterator_t<R>, Proj>,
             indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
               ranges::less>
      constexpr bool binary_search(R&& r, const T& value, Comp comp = {},
                                   Proj proj = {});
  }

  // [alg.partitions], partitions
  template<class InputIterator, class Predicate>
    constexpr bool is_partitioned(InputIterator first, InputIterator last, Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    bool is_partitioned(ExecutionPolicy&& exec,                 // freestanding-deleted, see [algorithms.parallel.overloads]
                        ForwardIterator first, ForwardIterator last, Predicate pred);

  namespace ranges {
    template<input_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr bool is_partitioned(I first, S last, Pred pred, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr bool is_partitioned(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      bool is_partitioned(Ep&& exec, I first, S last, Pred pred,
                          Proj proj = {});                                  // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      bool is_partitioned(Ep&& exec, R&& r, Pred pred, Proj proj = {});     // freestanding-deleted
  }

  template<class ForwardIterator, class Predicate>
    constexpr ForwardIterator partition(ForwardIterator first,
                                        ForwardIterator last,
                                        Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class Predicate>
    ForwardIterator partition(ExecutionPolicy&& exec,           // freestanding-deleted, see [algorithms.parallel.overloads]
                              ForwardIterator first,
                              ForwardIterator last,
                              Predicate pred);

  namespace ranges {
    template<permutable I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr subrange<I>
        partition(I first, S last, Pred pred, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R>
        partition(R&& r, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      subrange<I>
        partition(Ep&& exec, I first, S last, Pred pred, Proj proj = {});   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        partition(Ep&& exec, R&& r, Pred pred, Proj proj = {});             // freestanding-deleted
  }

  template<class BidirectionalIterator, class Predicate>
    constexpr BidirectionalIterator stable_partition(BidirectionalIterator first,   // hosted
                                                     BidirectionalIterator last,
                                                     Predicate pred);
  template<class ExecutionPolicy, class BidirectionalIterator, class Predicate>
    BidirectionalIterator stable_partition(ExecutionPolicy&& exec,                  // hosted,
                                           BidirectionalIterator first,             // see [algorithms.parallel.overloads]
                                           BidirectionalIterator last,
                                           Predicate pred);

  namespace ranges {
    template<bidirectional_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      requires permutable<I>
      constexpr subrange<I> stable_partition(I first, S last, Pred pred,            // hosted
                                             Proj proj = {});
    template<bidirectional_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires permutable<iterator_t<R>>
      constexpr borrowed_subrange_t<R> stable_partition(R&& r, Pred pred,           // hosted
                                                        Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires permutable<I>
      subrange<I>
        stable_partition(Ep&& exec, I first, S last, Pred pred,
                         Proj proj = {});                                   // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires permutable<iterator_t<R>>
      borrowed_subrange_t<R>
        stable_partition(Ep&& exec, R&& r, Pred pred, Proj proj = {});      // freestanding-deleted
  }

  template<class InputIterator, class OutputIterator1,
           class OutputIterator2, class Predicate>
    constexpr pair<OutputIterator1, OutputIterator2>
      partition_copy(InputIterator first, InputIterator last,
                     OutputIterator1 out_true, OutputIterator2 out_false,
                     Predicate pred);
  template<class ExecutionPolicy, class ForwardIterator, class ForwardIterator1,
           class ForwardIterator2, class Predicate>
    pair<ForwardIterator1, ForwardIterator2>
      partition_copy(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator first, ForwardIterator last,
                     ForwardIterator1 out_true, ForwardIterator2 out_false,
                     Predicate pred);

  namespace ranges {
    template<class I, class O1, class O2>
      using partition_copy_result = in_out_out_result<I, O1, O2>;

    template<input_iterator I, sentinel_for<I> S,
             weakly_incrementable O1, weakly_incrementable O2,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O1> && indirectly_copyable<I, O2>
      constexpr partition_copy_result<I, O1, O2>
        partition_copy(I first, S last, O1 out_true, O2 out_false, Pred pred,
                       Proj proj = {});
    template<input_range R, weakly_incrementable O1, weakly_incrementable O2,
             class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, O1> &&
               indirectly_copyable<iterator_t<R>, O2>
      constexpr partition_copy_result<borrowed_iterator_t<R>, O1, O2>
        partition_copy(R&& r, O1 out_true, O2 out_false, Pred pred, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             random_access_iterator O1, sized_sentinel_for<O1> OutS1,
             random_access_iterator O2, sized_sentinel_for<O2> OutS2,
             class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
      requires indirectly_copyable<I, O1> && indirectly_copyable<I, O2>
      partition_copy_result<I, O1, O2>
        partition_copy(Ep&& exec, I first, S last, O1 out_true, OutS1 last_true,
                       O2 out_false, OutS2 last_false, Pred pred,
                       Proj proj = {});                         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R,
             sized-random-access-range OutR1, sized-random-access-range OutR2,
             class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      requires indirectly_copyable<iterator_t<R>, iterator_t<OutR1>> &&
               indirectly_copyable<iterator_t<R>, iterator_t<OutR2>>
      partition_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR1>,
                            borrowed_iterator_t<OutR2>>
        partition_copy(Ep&& exec, R&& r, OutR1&& out_true_r, OutR2&& out_false_r, Pred pred,
                       Proj proj = {});                         // freestanding-deleted
  }

  template<class ForwardIterator, class Predicate>
    constexpr ForwardIterator
      partition_point(ForwardIterator first, ForwardIterator last,
                      Predicate pred);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_unary_predicate<projected<I, Proj>> Pred>
      constexpr I partition_point(I first, S last, Pred pred, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
      constexpr borrowed_iterator_t<R>
        partition_point(R&& r, Pred pred, Proj proj = {});
  }

  // [alg.merge], merge
  template<class InputIterator1, class InputIterator2, class OutputIterator>
    constexpr OutputIterator
      merge(InputIterator1 first1, InputIterator1 last1,
            InputIterator2 first2, InputIterator2 last2,
            OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
           class Compare>
    constexpr OutputIterator
      merge(InputIterator1 first1, InputIterator1 last1,
            InputIterator2 first2, InputIterator2 last2,
            OutputIterator result, Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator>
    ForwardIterator
      merge(ExecutionPolicy&& exec,                             // freestanding-deleted, see [algorithms.parallel.overloads]
            ForwardIterator1 first1, ForwardIterator1 last1,
            ForwardIterator2 first2, ForwardIterator2 last2,
            ForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator, class Compare>
    ForwardIterator
      merge(ExecutionPolicy&& exec,                             // freestanding-deleted, see [algorithms.parallel.overloads]
            ForwardIterator1 first1, ForwardIterator1 last1,
            ForwardIterator2 first2, ForwardIterator2 last2,
            ForwardIterator result, Compare comp);

  namespace ranges {
    template<class I1, class I2, class O>
      using merge_result = in_in_out_result<I1, I2, O>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             weakly_incrementable O, class Comp = ranges::less, class Proj1 = identity,
             class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      constexpr merge_result<I1, I2, O>
        merge(I1 first1, S1 last1, I2 first2, S2 last2, O result,
              Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, weakly_incrementable O, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
      constexpr merge_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
        merge(R1&& r1, R2&& r2, O result,
              Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      merge_result<I1, I2, O>
        merge(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, O result, OutS result_last,
              Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});          // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             sized-random-access-range OutR, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
      merge_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, borrowed_iterator_t<OutR>>
        merge(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r,
              Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});          // freestanding-deleted
  }

  template<class BidirectionalIterator>
    constexpr void inplace_merge(BidirectionalIterator first,   // hosted
                                 BidirectionalIterator middle,
                                 BidirectionalIterator last);
  template<class BidirectionalIterator, class Compare>
    constexpr void inplace_merge(BidirectionalIterator first,   // hosted
                                 BidirectionalIterator middle,
                                 BidirectionalIterator last, Compare comp);
  template<class ExecutionPolicy, class BidirectionalIterator>
    void inplace_merge(ExecutionPolicy&& exec,                  // hosted, see [algorithms.parallel.overloads]
                       BidirectionalIterator first,
                       BidirectionalIterator middle,
                       BidirectionalIterator last);
  template<class ExecutionPolicy, class BidirectionalIterator, class Compare>
    void inplace_merge(ExecutionPolicy&& exec,                  // hosted, see [algorithms.parallel.overloads]
                       BidirectionalIterator first,
                       BidirectionalIterator middle,
                       BidirectionalIterator last, Compare comp);

  namespace ranges {
    template<bidirectional_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        inplace_merge(I first, I middle, S last, Comp comp = {}, Proj proj = {});       // hosted
    template<bidirectional_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        inplace_merge(R&& r, iterator_t<R> middle, Comp comp = {}, Proj proj = {});     // hosted

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Comp = ranges::less, class Proj = identity>
      requires sortable<I, Comp, Proj>
      I inplace_merge(Ep&& exec, I first, I middle, S last, Comp comp = {},
                      Proj proj = {});                          // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      borrowed_iterator_t<R>
        inplace_merge(Ep&& exec, R&& r, iterator_t<R> middle, Comp comp = {},
                      Proj proj = {});                          // freestanding-deleted
  }

  // [alg.set.operations], set operations
  template<class InputIterator1, class InputIterator2>
    constexpr bool includes(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, InputIterator2 last2);
  template<class InputIterator1, class InputIterator2, class Compare>
    constexpr bool includes(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, InputIterator2 last2,
                            Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    bool includes(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator1 first1, ForwardIterator1 last1,
                  ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class Compare>
    bool includes(ExecutionPolicy&& exec,                       // freestanding-deleted, see [algorithms.parallel.overloads]
                  ForwardIterator1 first1, ForwardIterator1 last1,
                  ForwardIterator2 first2, ForwardIterator2 last2,
                  Compare comp);

  namespace ranges {
    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_strict_weak_order<projected<I1, Proj1>, projected<I2, Proj2>> Comp =
               ranges::less>
      constexpr bool includes(I1 first1, S1 last1, I2 first2, S2 last2, Comp comp = {},
                              Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, class Proj1 = identity,
             class Proj2 = identity,
             indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                        projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
      constexpr bool includes(R1&& r1, R2&& r2, Comp comp = {},
                              Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_strict_weak_order<projected<I1, Proj1>, projected<I2, Proj2>> Comp =
               ranges::less>
      bool includes(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                    Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});    // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                        projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
      bool includes(Ep&& exec, R1&& r1, R2&& r2,
                    Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});    // freestanding-deleted
  }

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    constexpr OutputIterator
      set_union(InputIterator1 first1, InputIterator1 last1,
                InputIterator2 first2, InputIterator2 last2,
                OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    constexpr OutputIterator
      set_union(InputIterator1 first1, InputIterator1 last1,
                InputIterator2 first2, InputIterator2 last2,
                OutputIterator result, Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator>
    ForwardIterator
      set_union(ExecutionPolicy&& exec,                         // freestanding-deleted, see [algorithms.parallel.overloads]
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2, ForwardIterator2 last2,
                ForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator, class Compare>
    ForwardIterator
      set_union(ExecutionPolicy&& exec,                         // freestanding-deleted, see [algorithms.parallel.overloads]
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2, ForwardIterator2 last2,
                ForwardIterator result, Compare comp);

  namespace ranges {
    template<class I1, class I2, class O>
      using set_union_result = in_in_out_result<I1, I2, O>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             weakly_incrementable O, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      constexpr set_union_result<I1, I2, O>
        set_union(I1 first1, S1 last1, I2 first2, S2 last2, O result, Comp comp = {},
                  Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, weakly_incrementable O,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
      constexpr set_union_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
        set_union(R1&& r1, R2&& r2, O result, Comp comp = {},
                  Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      set_union_result<I1, I2, O>
        set_union(Ep&& exec, I1 first1, S1 last1,
                  I2 first2, S2 last2, O result, OutS result_last,
                  Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});      // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             sized-random-access-range OutR, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
      set_union_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                       borrowed_iterator_t<OutR>>
        set_union(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                  Proj1 proj1 = {}, Proj2 proj2 = {});                      // freestanding-deleted
  }

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    constexpr OutputIterator
      set_intersection(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2, InputIterator2 last2,
                       OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    constexpr OutputIterator
      set_intersection(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2, InputIterator2 last2,
                       OutputIterator result, Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator>
    ForwardIterator
      set_intersection(ExecutionPolicy&& exec,                  // freestanding-deleted, see [algorithms.parallel.overloads]
                       ForwardIterator1 first1, ForwardIterator1 last1,
                       ForwardIterator2 first2, ForwardIterator2 last2,
                       ForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator, class Compare>
    ForwardIterator
      set_intersection(ExecutionPolicy&& exec,                  // freestanding-deleted, see [algorithms.parallel.overloads]
                       ForwardIterator1 first1, ForwardIterator1 last1,
                       ForwardIterator2 first2, ForwardIterator2 last2,
                       ForwardIterator result, Compare comp);

  namespace ranges {
    template<class I1, class I2, class O>
      using set_intersection_result = in_in_out_result<I1, I2, O>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             weakly_incrementable O, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      constexpr set_intersection_result<I1, I2, O>
        set_intersection(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                         Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, weakly_incrementable O,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
      constexpr set_intersection_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
        set_intersection(R1&& r1, R2&& r2, O result,
                         Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      set_intersection_result<I1, I2, O>
        set_intersection(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                         O result, OutS result_last, Comp comp = {}, Proj1 proj1 = {},
                         Proj2 proj2 = {});                     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             sized-random-access-range OutR, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
      set_intersection_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                              borrowed_iterator_t<OutR>>
        set_intersection(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                         Proj1 proj1 = {}, Proj2 proj2 = {});   // freestanding-deleted
  }

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    constexpr OutputIterator
      set_difference(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2, InputIterator2 last2,
                     OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    constexpr OutputIterator
      set_difference(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2, InputIterator2 last2,
                     OutputIterator result, Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator>
    ForwardIterator
      set_difference(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2, ForwardIterator2 last2,
                     ForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator, class Compare>
    ForwardIterator
      set_difference(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2, ForwardIterator2 last2,
                     ForwardIterator result, Compare comp);

  namespace ranges {
    template<class I, class O>
      using set_difference_result = in_out_result<I, O>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             weakly_incrementable O, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      constexpr set_difference_result<I1, O>
        set_difference(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                       Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, weakly_incrementable O,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
      constexpr set_difference_result<borrowed_iterator_t<R1>, O>
        set_difference(R1&& r1, R2&& r2, O result,
                       Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      set_difference_result<I1, O>
        set_difference(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                       O result, OutS result_last, Comp comp = {}, Proj1 proj1 = {},
                       Proj2 proj2 = {});                       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             sized-random-access-range OutR, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
      set_difference_result<borrowed_iterator_t<R1>, borrowed_iterator_t<OutR>>
        set_difference(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                       Proj1 proj1 = {}, Proj2 proj2 = {});     // freestanding-deleted
  }

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    constexpr OutputIterator
      set_symmetric_difference(InputIterator1 first1, InputIterator1 last1,
                               InputIterator2 first2, InputIterator2 last2,
                               OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    constexpr OutputIterator
      set_symmetric_difference(InputIterator1 first1, InputIterator1 last1,
                               InputIterator2 first2, InputIterator2 last2,
                               OutputIterator result, Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator>
    ForwardIterator
      set_symmetric_difference(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator1 first1, ForwardIterator1 last1,
                               ForwardIterator2 first2, ForwardIterator2 last2,
                               ForwardIterator result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class ForwardIterator, class Compare>
    ForwardIterator
      set_symmetric_difference(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator1 first1, ForwardIterator1 last1,
                               ForwardIterator2 first2, ForwardIterator2 last2,
                               ForwardIterator result, Compare comp);

  namespace ranges {
    template<class I1, class I2, class O>
      using set_symmetric_difference_result = in_in_out_result<I1, I2, O>;

    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             weakly_incrementable O, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      constexpr set_symmetric_difference_result<I1, I2, O>
        set_symmetric_difference(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                                 Comp comp = {}, Proj1 proj1 = {},
                                 Proj2 proj2 = {});
    template<input_range R1, input_range R2, weakly_incrementable O,
             class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
      constexpr set_symmetric_difference_result<borrowed_iterator_t<R1>,
                                                borrowed_iterator_t<R2>, O>
        set_symmetric_difference(R1&& r1, R2&& r2, O result, Comp comp = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
      set_symmetric_difference_result<I1, I2, O>
        set_symmetric_difference(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                                 O result, OutS result_last, Comp comp = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             sized-random-access-range OutR, class Comp = ranges::less,
             class Proj1 = identity, class Proj2 = identity>
      requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
      set_symmetric_difference_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                                      borrowed_iterator_t<OutR>>
        set_symmetric_difference(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});       // freestanding-deleted
  }

  // [alg.heap.operations], heap operations
  template<class RandomAccessIterator>
    constexpr void push_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void push_heap(RandomAccessIterator first, RandomAccessIterator last,
                             Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        push_heap(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        push_heap(R&& r, Comp comp = {}, Proj proj = {});
  }

  template<class RandomAccessIterator>
    constexpr void pop_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void pop_heap(RandomAccessIterator first, RandomAccessIterator last,
                            Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        pop_heap(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        pop_heap(R&& r, Comp comp = {}, Proj proj = {});
  }

  template<class RandomAccessIterator>
    constexpr void make_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void make_heap(RandomAccessIterator first, RandomAccessIterator last,
                             Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        make_heap(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        make_heap(R&& r, Comp comp = {}, Proj proj = {});
  }

  template<class RandomAccessIterator>
    constexpr void sort_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr void sort_heap(RandomAccessIterator first, RandomAccessIterator last,
                             Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr I
        sort_heap(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Comp = ranges::less, class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr borrowed_iterator_t<R>
        sort_heap(R&& r, Comp comp = {}, Proj proj = {});
  }

  template<class RandomAccessIterator>
    constexpr bool is_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr bool is_heap(RandomAccessIterator first, RandomAccessIterator last,
                           Compare comp);
  template<class ExecutionPolicy, class RandomAccessIterator>
    bool is_heap(ExecutionPolicy&& exec,                        // freestanding-deleted, see [algorithms.parallel.overloads]
                 RandomAccessIterator first, RandomAccessIterator last);
  template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
    bool is_heap(ExecutionPolicy&& exec,                        // freestanding-deleted, see [algorithms.parallel.overloads]
                 RandomAccessIterator first, RandomAccessIterator last,
                 Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr bool is_heap(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr bool is_heap(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      bool is_heap(Ep&& exec, I first, S last, Comp comp = {},
                   Proj proj = {});                                         // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      bool is_heap(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});       // freestanding-deleted
  }

  template<class RandomAccessIterator>
    constexpr RandomAccessIterator
      is_heap_until(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    constexpr RandomAccessIterator
      is_heap_until(RandomAccessIterator first, RandomAccessIterator last,
                    Compare comp);
  template<class ExecutionPolicy, class RandomAccessIterator>
    RandomAccessIterator
      is_heap_until(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    RandomAccessIterator first, RandomAccessIterator last);
  template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
    RandomAccessIterator
      is_heap_until(ExecutionPolicy&& exec,                     // freestanding-deleted, see [algorithms.parallel.overloads]
                    RandomAccessIterator first, RandomAccessIterator last,
                    Compare comp);

  namespace ranges {
    template<random_access_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr I is_heap_until(I first, S last, Comp comp = {}, Proj proj = {});
    template<random_access_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr borrowed_iterator_t<R>
        is_heap_until(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      I is_heap_until(Ep&& exec, I first, S last, Comp comp = {},
                      Proj proj = {});                                      // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      borrowed_iterator_t<R>
        is_heap_until(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});    // freestanding-deleted
  }

  // [alg.min.max], minimum and maximum
  template<class T> constexpr const T& min(const T& a, const T& b);
  template<class T, class Compare>
    constexpr const T& min(const T& a, const T& b, Compare comp);
  template<class T>
    constexpr T min(initializer_list<T> t);
  template<class T, class Compare>
    constexpr T min(initializer_list<T> t, Compare comp);

  namespace ranges {
    template<class T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr const T& min(const T& a, const T& b, Comp comp = {}, Proj proj = {});
    template<copyable T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr T min(initializer_list<T> r, Comp comp = {}, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
      constexpr range_value_t<R>
        min(R&& r, Comp comp = {}, Proj proj = {});
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
      range_value_t<R>
        min(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});              // freestanding-deleted
  }

  template<class T> constexpr const T& max(const T& a, const T& b);
  template<class T, class Compare>
    constexpr const T& max(const T& a, const T& b, Compare comp);
  template<class T>
    constexpr T max(initializer_list<T> t);
  template<class T, class Compare>
    constexpr T max(initializer_list<T> t, Compare comp);

  namespace ranges {
    template<class T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr const T& max(const T& a, const T& b, Comp comp = {}, Proj proj = {});
    template<copyable T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr T max(initializer_list<T> r, Comp comp = {}, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
      constexpr range_value_t<R>
        max(R&& r, Comp comp = {}, Proj proj = {});
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
      range_value_t<R>
        max(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});              // freestanding-deleted
  }

  template<class T> constexpr pair<const T&, const T&> minmax(const T& a, const T& b);
  template<class T, class Compare>
    constexpr pair<const T&, const T&> minmax(const T& a, const T& b, Compare comp);
  template<class T>
    constexpr pair<T, T> minmax(initializer_list<T> t);
  template<class T, class Compare>
    constexpr pair<T, T> minmax(initializer_list<T> t, Compare comp);

  namespace ranges {
    template<class T>
      using minmax_result = min_max_result<T>;

    template<class T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr minmax_result<const T&>
        minmax(const T& a, const T& b, Comp comp = {}, Proj proj = {});
    template<copyable T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr minmax_result<T>
        minmax(initializer_list<T> r, Comp comp = {}, Proj proj = {});
    template<input_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
      constexpr minmax_result<range_value_t<R>>
        minmax(R&& r, Comp comp = {}, Proj proj = {});
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
      minmax_result<range_value_t<R>>
        minmax(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});           // freestanding-deleted
  }

  template<class ForwardIterator>
    constexpr ForwardIterator min_element(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    constexpr ForwardIterator min_element(ForwardIterator first, ForwardIterator last,
                                          Compare comp);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator min_element(ExecutionPolicy&& exec,         // freestanding-deleted, see [algorithms.parallel.overloads]
                                ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class Compare>
    ForwardIterator min_element(ExecutionPolicy&& exec,         // freestanding-deleted, see [algorithms.parallel.overloads]
                                ForwardIterator first, ForwardIterator last,
                                Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr I min_element(I first, S last, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr borrowed_iterator_t<R>
        min_element(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      I min_element(Ep&& exec, I first, S last, Comp comp = {},
                    Proj proj = {});                                        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R,
             class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      borrowed_iterator_t<R>
        min_element(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});      // freestanding-deleted
  }

  template<class ForwardIterator>
    constexpr ForwardIterator max_element(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    constexpr ForwardIterator max_element(ForwardIterator first, ForwardIterator last,
                                          Compare comp);
  template<class ExecutionPolicy, class ForwardIterator>
    ForwardIterator max_element(ExecutionPolicy&& exec,         // freestanding-deleted, see [algorithms.parallel.overloads]
                                ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class Compare>
    ForwardIterator max_element(ExecutionPolicy&& exec,         // freestanding-deleted, see [algorithms.parallel.overloads]
                                ForwardIterator first, ForwardIterator last,
                                Compare comp);

  namespace ranges {
    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr I max_element(I first, S last, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr borrowed_iterator_t<R>
        max_element(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      I max_element(Ep&& exec, I first, S last, Comp comp = {},
                    Proj proj = {});                                        // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R,
             class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      borrowed_iterator_t<R>
        max_element(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});      // freestanding-deleted
  }

  template<class ForwardIterator>
    constexpr pair<ForwardIterator, ForwardIterator>
      minmax_element(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    constexpr pair<ForwardIterator, ForwardIterator>
      minmax_element(ForwardIterator first, ForwardIterator last, Compare comp);
  template<class ExecutionPolicy, class ForwardIterator>
    pair<ForwardIterator, ForwardIterator>
      minmax_element(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class Compare>
    pair<ForwardIterator, ForwardIterator>
      minmax_element(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator first, ForwardIterator last, Compare comp);

  namespace ranges {
    template<class I>
      using minmax_element_result = min_max_result<I>;

    template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      constexpr minmax_element_result<I>
        minmax_element(I first, S last, Comp comp = {}, Proj proj = {});
    template<forward_range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      constexpr minmax_element_result<borrowed_iterator_t<R>>
        minmax_element(R&& r, Comp comp = {}, Proj proj = {});

    template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
             class Proj = identity,
             indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
      minmax_element_result<I>
        minmax_element(Ep&& exec, I first, S last, Comp comp = {},
                       Proj proj = {});                                     // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
             indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
      minmax_element_result<borrowed_iterator_t<R>>
        minmax_element(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});   // freestanding-deleted
  }

  // [alg.clamp], bounded value
  template<class T>
    constexpr const T& clamp(const T& v, const T& lo, const T& hi);
  template<class T, class Compare>
    constexpr const T& clamp(const T& v, const T& lo, const T& hi, Compare comp);

  namespace ranges {
    template<class T, class Proj = identity,
             indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
      constexpr const T&
        clamp(const T& v, const T& lo, const T& hi, Comp comp = {}, Proj proj = {});
  }

  // [alg.lex.comparison], lexicographical comparison
  template<class InputIterator1, class InputIterator2>
    constexpr bool
      lexicographical_compare(InputIterator1 first1, InputIterator1 last1,
                              InputIterator2 first2, InputIterator2 last2);
  template<class InputIterator1, class InputIterator2, class Compare>
    constexpr bool
      lexicographical_compare(InputIterator1 first1, InputIterator1 last1,
                              InputIterator2 first2, InputIterator2 last2,
                              Compare comp);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    bool
      lexicographical_compare(ExecutionPolicy&& exec,           // freestanding-deleted, see [algorithms.parallel.overloads]
                              ForwardIterator1 first1, ForwardIterator1 last1,
                              ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class Compare>
    bool
      lexicographical_compare(ExecutionPolicy&& exec,           // freestanding-deleted, see [algorithms.parallel.overloads]
                              ForwardIterator1 first1, ForwardIterator1 last1,
                              ForwardIterator2 first2, ForwardIterator2 last2,
                              Compare comp);

  namespace ranges {
    template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_strict_weak_order<projected<I1, Proj1>, projected<I2, Proj2>> Comp =
               ranges::less>
      constexpr bool
        lexicographical_compare(I1 first1, S1 last1, I2 first2, S2 last2,
                                Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
    template<input_range R1, input_range R2, class Proj1 = identity,
             class Proj2 = identity,
             indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                        projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
      constexpr bool
        lexicographical_compare(R1&& r1, R2&& r2, Comp comp = {},
                                Proj1 proj1 = {}, Proj2 proj2 = {});

    template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
             random_access_iterator I2, sized_sentinel_for<I2> S2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_strict_weak_order<projected<I1, Proj1>,
                                        projected<I2, Proj2>> Comp = ranges::less>
      bool lexicographical_compare(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                                   Comp comp = {}, Proj1 proj1 = {},
                                   Proj2 proj2 = {});                       // freestanding-deleted
    template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
             class Proj1 = identity, class Proj2 = identity,
             indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                        projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
      bool lexicographical_compare(Ep&& exec, R1&& r1, R2&& r2, Comp comp = {},
                                   Proj1 proj1 = {}, Proj2 proj2 = {});     // freestanding-deleted
  }

  // [alg.three.way], three-way comparison algorithms
  template<class InputIterator1, class InputIterator2, class Cmp>
    constexpr auto
      lexicographical_compare_three_way(InputIterator1 b1, InputIterator1 e1,
                                        InputIterator2 b2, InputIterator2 e2,
                                        Cmp comp)
        -> decltype(comp(*b1, *b2));
  template<class InputIterator1, class InputIterator2>
    constexpr auto
      lexicographical_compare_three_way(InputIterator1 b1, InputIterator1 e1,
                                        InputIterator2 b2, InputIterator2 e2);

  // [alg.permutation.generators], permutations
  template<class BidirectionalIterator>
    constexpr bool next_permutation(BidirectionalIterator first,
                                    BidirectionalIterator last);
  template<class BidirectionalIterator, class Compare>
    constexpr bool next_permutation(BidirectionalIterator first,
                                    BidirectionalIterator last, Compare comp);

  namespace ranges {
    template<class I>
      using next_permutation_result = in_found_result<I>;

    template<bidirectional_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr next_permutation_result<I>
        next_permutation(I first, S last, Comp comp = {}, Proj proj = {});
    template<bidirectional_range R, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr next_permutation_result<borrowed_iterator_t<R>>
        next_permutation(R&& r, Comp comp = {}, Proj proj = {});
  }

  template<class BidirectionalIterator>
    constexpr bool prev_permutation(BidirectionalIterator first,
                                    BidirectionalIterator last);
  template<class BidirectionalIterator, class Compare>
    constexpr bool prev_permutation(BidirectionalIterator first,
                                    BidirectionalIterator last, Compare comp);

  namespace ranges {
    template<class I>
      using prev_permutation_result = in_found_result<I>;

    template<bidirectional_iterator I, sentinel_for<I> S, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<I, Comp, Proj>
      constexpr prev_permutation_result<I>
        prev_permutation(I first, S last, Comp comp = {}, Proj proj = {});
    template<bidirectional_range R, class Comp = ranges::less,
             class Proj = identity>
      requires sortable<iterator_t<R>, Comp, Proj>
      constexpr prev_permutation_result<borrowed_iterator_t<R>>
        prev_permutation(R&& r, Comp comp = {}, Proj proj = {});
  }
}
```

## Algorithm result types <a id="algorithms.results">[[algorithms.results]]</a>

Each of the class templates specified in this subclause has the template
parameters, data members, and special members specified below, and has
no base classes or members other than those specified.

``` cpp
namespace std::ranges {
  template<class I, class F>
  struct in_fun_result {
    [[no_unique_address]] I in;
    [[no_unique_address]] F fun;

    template<class I2, class F2>
      requires convertible_to<const I&, I2> && convertible_to<const F&, F2>
    constexpr operator in_fun_result<I2, F2>() const & {
      return {in, fun};
    }

    template<class I2, class F2>
      requires convertible_to<I, I2> && convertible_to<F, F2>
    constexpr operator in_fun_result<I2, F2>() && {
      return {std::move(in), std::move(fun)};
    }
  };

  template<class I1, class I2>
  struct in_in_result {
    [[no_unique_address]] I1 in1;
    [[no_unique_address]] I2 in2;

    template<class II1, class II2>
      requires convertible_to<const I1&, II1> && convertible_to<const I2&, II2>
    constexpr operator in_in_result<II1, II2>() const & {
      return {in1, in2};
    }

    template<class II1, class II2>
      requires convertible_to<I1, II1> && convertible_to<I2, II2>
    constexpr operator in_in_result<II1, II2>() && {
      return {std::move(in1), std::move(in2)};
    }
  };

  template<class I, class O>
  struct in_out_result {
    [[no_unique_address]] I in;
    [[no_unique_address]] O out;

    template<class I2, class O2>
      requires convertible_to<const I&, I2> && convertible_to<const O&, O2>
    constexpr operator in_out_result<I2, O2>() const & {
      return {in, out};
    }

    template<class I2, class O2>
      requires convertible_to<I, I2> && convertible_to<O, O2>
    constexpr operator in_out_result<I2, O2>() && {
      return {std::move(in), std::move(out)};
    }
  };

  template<class I1, class I2, class O>
  struct in_in_out_result {
    [[no_unique_address]] I1 in1;
    [[no_unique_address]] I2 in2;
    [[no_unique_address]] O  out;

    template<class II1, class II2, class OO>
      requires convertible_to<const I1&, II1> &&
               convertible_to<const I2&, II2> &&
               convertible_to<const O&, OO>
    constexpr operator in_in_out_result<II1, II2, OO>() const & {
      return {in1, in2, out};
    }

    template<class II1, class II2, class OO>
      requires convertible_to<I1, II1> &&
               convertible_to<I2, II2> &&
               convertible_to<O, OO>
    constexpr operator in_in_out_result<II1, II2, OO>() && {
      return {std::move(in1), std::move(in2), std::move(out)};
    }
  };

  template<class I, class O1, class O2>
  struct in_out_out_result {
    [[no_unique_address]] I  in;
    [[no_unique_address]] O1 out1;
    [[no_unique_address]] O2 out2;

    template<class II, class OO1, class OO2>
      requires convertible_to<const I&, II> &&
               convertible_to<const O1&, OO1> &&
               convertible_to<const O2&, OO2>
    constexpr operator in_out_out_result<II, OO1, OO2>() const & {
      return {in, out1, out2};
    }

    template<class II, class OO1, class OO2>
      requires convertible_to<I, II> &&
               convertible_to<O1, OO1> &&
               convertible_to<O2, OO2>
    constexpr operator in_out_out_result<II, OO1, OO2>() && {
      return {std::move(in), std::move(out1), std::move(out2)};
    }
  };

  template<class T>
  struct min_max_result {
    [[no_unique_address]] T min;
    [[no_unique_address]] T max;

    template<class T2>
      requires convertible_to<const T&, T2>
    constexpr operator min_max_result<T2>() const & {
      return {min, max};
    }

    template<class T2>
      requires convertible_to<T, T2>
    constexpr operator min_max_result<T2>() && {
      return {std::move(min), std::move(max)};
    }
  };

  template<class I>
  struct in_found_result {
    [[no_unique_address]] I in;
    bool found;

    template<class I2>
      requires convertible_to<const I&, I2>
    constexpr operator in_found_result<I2>() const & {
      return {in, found};
    }
    template<class I2>
      requires convertible_to<I, I2>
    constexpr operator in_found_result<I2>() && {
      return {std::move(in), found};
    }
  };

  template<class I, class T>
  struct in_value_result {
    [[no_unique_address]] I in;
    [[no_unique_address]] T value;

    template<class I2, class T2>
      requires convertible_to<const I&, I2> && convertible_to<const T&, T2>
    constexpr operator in_value_result<I2, T2>() const & {
      return {in, value};
    }

    template<class I2, class T2>
      requires convertible_to<I, I2> && convertible_to<T, T2>
    constexpr operator in_value_result<I2, T2>() && {
      return {std::move(in), std::move(value)};
    }
  };

  template<class O, class T>
  struct out_value_result {
    [[no_unique_address]] O out;
    [[no_unique_address]] T value;

    template<class O2, class T2>
      requires convertible_to<const O&, O2> && convertible_to<const T&, T2>
    constexpr operator out_value_result<O2, T2>() const & {
      return {out, value};
    }

    template<class O2, class T2>
      requires convertible_to<O, O2> && convertible_to<T, T2>
    constexpr operator out_value_result<O2, T2>() && {
      return {std::move(out), std::move(value)};
    }
  };
}
```

## Non-modifying sequence operations <a id="alg.nonmodifying">[[alg.nonmodifying]]</a>

### All of <a id="alg.all.of">[[alg.all.of]]</a>

``` cpp
template<class InputIterator, class Predicate>
  constexpr bool all_of(InputIterator first, InputIterator last, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  bool all_of(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
              Predicate pred);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr bool ranges::all_of(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr bool ranges::all_of(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  bool ranges::all_of(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  bool ranges::all_of(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be:

- `pred(*i)` for the overloads in namespace `std`;
- `invoke(pred, invoke(proj, *i))` for the overloads in namespace
  `ranges`.

*Returns:* `false` if E is `false` for some iterator `i` in the range
\[`first`, `last`), and `true` otherwise.

*Complexity:* At most `last - first` applications of the predicate and
any projection.

### Any of <a id="alg.any.of">[[alg.any.of]]</a>

``` cpp
template<class InputIterator, class Predicate>
  constexpr bool any_of(InputIterator first, InputIterator last, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  bool any_of(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
              Predicate pred);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr bool ranges::any_of(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr bool ranges::any_of(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  bool ranges::any_of(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  bool ranges::any_of(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be:

- `pred(*i)` for the overloads in namespace `std`;
- `invoke(pred, invoke(proj, *i))` for the overloads in namespace
  `ranges`.

*Returns:* `true` if E is `true` for some iterator `i` in the range
\[`first`, `last`), and `false` otherwise.

*Complexity:* At most `last - first` applications of the predicate and
any projection.

### None of <a id="alg.none.of">[[alg.none.of]]</a>

``` cpp
template<class InputIterator, class Predicate>
  constexpr bool none_of(InputIterator first, InputIterator last, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  bool none_of(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
               Predicate pred);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr bool ranges::none_of(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr bool ranges::none_of(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  bool ranges::none_of(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  bool ranges::none_of(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be:

- `pred(*i)` for the overloads in namespace `std`;
- `invoke(pred, invoke(proj, *i))` for the overloads in namespace
  `ranges`.

*Returns:* `false` if E is `true` for some iterator `i` in the range
\[`first`, `last`), and `true` otherwise.

*Complexity:* At most `last - first` applications of the predicate and
any projection.

### Contains <a id="alg.contains">[[alg.contains]]</a>

``` cpp
template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  constexpr bool ranges::contains(I first, S last, const T& value, Proj proj = {});
template<input_range R, class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  constexpr bool ranges::contains(R&& r, const T& value, Proj proj = {});
```

*Returns:* `ranges::find(std::move(first), last, value, proj) != last`.

``` cpp
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  bool ranges::contains(Ep&& exec, I first, S last, const T& value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires
    indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  bool ranges::contains(Ep&& exec, R&& r, const T& value, Proj proj = {});
```

*Returns:*
`ranges::find(std::forward<Ep>(exec), first, last, value, proj) != last`.

``` cpp
template<forward_iterator I1, sentinel_for<I1> S1,
         forward_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr bool ranges::contains_subrange(I1 first1, S1 last1, I2 first2, S2 last2,
                                           Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<forward_range R1, forward_range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr bool ranges::contains_subrange(R1&& r1, R2&& r2, Pred pred = {},
                                           Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:*

``` cpp
first2 == last2 || !ranges::search(first1, last1, first2, last2,
                                   pred, proj1, proj2).empty()
```

``` cpp
template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  bool ranges::contains_subrange(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                                 Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  bool ranges::contains_subrange(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                                 Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:*

``` cpp
first2 == last2 || !ranges::search(std::forward<Ep>(exec), first1, last1,
                                   first2, last2, pred, proj1, proj2).empty()
```

### For each <a id="alg.foreach">[[alg.foreach]]</a>

``` cpp
template<class InputIterator, class Function>
  constexpr Function for_each(InputIterator first, InputIterator last, Function f);
```

*Preconditions:* `Function` meets the *Cpp17MoveConstructible*
requirements ([[cpp17.moveconstructible]]).

[*Note 1*: `Function` need not meet the requirements of
*Cpp17CopyConstructible* ([[cpp17.copyconstructible]]). — *end note*]

*Effects:* Applies `f` to the result of dereferencing every iterator in
the range \[`first`, `last`), starting from `first` and proceeding to
`last - 1`.

[*Note 2*: If the type of `first` meets the requirements of a mutable
iterator, `f` can apply non-constant functions through the dereferenced
iterator. — *end note*]

*Returns:* `f`.

*Complexity:* Applies `f` exactly `last - first` times.

*Remarks:* If `f` returns a result, the result is ignored.

``` cpp
template<class ExecutionPolicy, class ForwardIterator, class Function>
  void for_each(ExecutionPolicy&& exec,
                ForwardIterator first, ForwardIterator last,
                Function f);
```

*Preconditions:* `Function` meets the *Cpp17CopyConstructible*
requirements.

*Effects:* Applies `f` to the result of dereferencing every iterator in
the range \[`first`, `last`).

[*Note 3*: If the type of `first` meets the requirements of a mutable
iterator, `f` can apply non-constant functions through the dereferenced
iterator. — *end note*]

*Complexity:* Applies `f` exactly `last - first` times.

*Remarks:* If `f` returns a result, the result is ignored.
Implementations do not have the freedom granted under
[[algorithms.parallel.exec]] to make arbitrary copies of elements from
the input sequence.

[*Note 4*: Does not return a copy of its `Function` parameter, since
parallelization often does not permit efficient state
accumulation. — *end note*]

``` cpp
template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirectly_unary_invocable<projected<I, Proj>> Fun>
  constexpr ranges::for_each_result<I, Fun>
    ranges::for_each(I first, S last, Fun f, Proj proj = {});
template<input_range R, class Proj = identity,
         indirectly_unary_invocable<projected<iterator_t<R>, Proj>> Fun>
  constexpr ranges::for_each_result<borrowed_iterator_t<R>, Fun>
    ranges::for_each(R&& r, Fun f, Proj proj = {});
```

*Effects:* Calls `invoke(f, invoke(proj, *i))` for every iterator `i` in
the range \[`first`, `last`), starting from `first` and proceeding to
`last - 1`.

[*Note 5*: If the result of `invoke(proj, *i)` is a mutable reference,
`f` can apply non-constant functions. — *end note*]

*Returns:* `{last, std::move(f)}`.

*Complexity:* Applies `f` and `proj` exactly `last - first` times.

*Remarks:* If `f` returns a result, the result is ignored.

[*Note 6*: The overloads in namespace `ranges` require `Fun` to model
`copy_constructible`. — *end note*]

``` cpp
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirectly_unary_invocable<projected<I, Proj>> Fun>
  I ranges::for_each(Ep&& exec, I first, S last, Fun f, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirectly_unary_invocable<projected<iterator_t<R>, Proj>> Fun>
  borrowed_iterator_t<R>
    ranges::for_each(Ep&& exec, R&& r, Fun f, Proj proj = {});
```

*Effects:* Calls `invoke(f, invoke(proj, *i))` for every iterator `i` in
the range \[`first`, `last`).

[*Note 7*: If the result of `invoke(proj, *i)` is a mutable reference,
`f` can apply non-constant functions. — *end note*]

*Returns:* `last`.

*Complexity:* Applies `f` and `proj` exactly `last - first` times.

*Remarks:*

- If `f` returns a result, the result is ignored.
- Implementations do not have the freedom granted under
  [[algorithms.parallel.exec]] to make arbitrary copies of elements from
  the input sequence.
- `f` may modify objects via its arguments [[algorithms.parallel.user]].

[*Note 8*: Does not return a copy of its `Fun` parameter, since
parallelization often does not permit efficient state
accumulation. — *end note*]

``` cpp
template<class InputIterator, class Size, class Function>
  constexpr InputIterator for_each_n(InputIterator first, Size n, Function f);
```

*Mandates:* The type `Size` is convertible to an integral
type [[conv.integral,class.conv]].

*Preconditions:* `n >= 0` is `true`. `Function` meets the
*Cpp17MoveConstructible* requirements.

[*Note 9*: `Function` need not meet the requirements of
*Cpp17CopyConstructible*. — *end note*]

*Effects:* Applies `f` to the result of dereferencing every iterator in
the range \[`first`, `first + n`) in order.

[*Note 10*: If the type of `first` meets the requirements of a mutable
iterator, `f` can apply non-constant functions through the dereferenced
iterator. — *end note*]

*Returns:* `first + n`.

*Remarks:* If `f` returns a result, the result is ignored.

``` cpp
template<class ExecutionPolicy, class ForwardIterator, class Size, class Function>
  ForwardIterator for_each_n(ExecutionPolicy&& exec, ForwardIterator first, Size n,
                             Function f);
```

*Mandates:* The type `Size` is convertible to an integral
type [[conv.integral,class.conv]].

*Preconditions:* `n >= 0` is `true`. `Function` meets the
*Cpp17CopyConstructible* requirements.

*Effects:* Applies `f` to the result of dereferencing every iterator in
the range \[`first`, `first + n`).

[*Note 11*: If the type of `first` meets the requirements of a mutable
iterator, `f` can apply non-constant functions through the dereferenced
iterator. — *end note*]

*Returns:* `first + n`.

*Remarks:* If `f` returns a result, the result is ignored.
Implementations do not have the freedom granted under
[[algorithms.parallel.exec]] to make arbitrary copies of elements from
the input sequence.

``` cpp
template<input_iterator I, class Proj = identity,
         indirectly_unary_invocable<projected<I, Proj>> Fun>
  constexpr ranges::for_each_n_result<I, Fun>
    ranges::for_each_n(I first, iter_difference_t<I> n, Fun f, Proj proj = {});
```

*Preconditions:* `n >= 0` is `true`.

*Effects:* Calls `invoke(f, invoke(proj, *i))` for every iterator `i` in
the range \[`first`, `first + n`) in order.

[*Note 12*: If the result of `invoke(proj, *i)` is a mutable reference,
`f` can apply non-constant functions. — *end note*]

*Returns:* `{first + n, std::move(f)}`.

*Remarks:* If `f` returns a result, the result is ignored.

[*Note 13*: The overload in namespace `ranges` requires `Fun` to model
`copy_constructible`. — *end note*]

``` cpp
template<execution-policy Ep, random_access_iterator I, class Proj = identity,
         indirectly_unary_invocable<projected<I, Proj>> Fun>
  I ranges::for_each_n(Ep&& exec, I first, iter_difference_t<I> n, Fun f, Proj proj = {});
```

*Preconditions:* `n >= 0` is `true`.

*Effects:* Calls `invoke(f, invoke(proj, *i))` for every iterator `i` in
the range \[`first`, `first + n`).

[*Note 14*: If the result of `invoke(proj, *i)` is a mutable reference,
`f` can apply non-constant functions. — *end note*]

*Returns:* `first + n`.

*Remarks:*

- If `f` returns a result, the result is ignored.
- Implementations do not have the freedom granted under
  [[algorithms.parallel.exec]] to make arbitrary copies of elements from
  the input sequence.
- `f` may modify objects via its arguments [[algorithms.parallel.user]].

[*Note 15*: Does not return a copy of its `Fun` parameter, since
parallelization often does not permit efficient state
accumulation. — *end note*]

### Find <a id="alg.find">[[alg.find]]</a>

``` cpp
template<class InputIterator, class T = iterator_traits<InputIterator>::value_type>
  constexpr InputIterator find(InputIterator first, InputIterator last,
                               const T& value);
template<class ExecutionPolicy, class ForwardIterator,
         class T = iterator_traits<ForwardIterator>::value_type>
  ForwardIterator find(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
                       const T& value);

template<class InputIterator, class Predicate>
  constexpr InputIterator find_if(InputIterator first, InputIterator last,
                                  Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  ForwardIterator find_if(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
                          Predicate pred);

template<class InputIterator, class Predicate>
  constexpr InputIterator find_if_not(InputIterator first, InputIterator last,
                                      Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  ForwardIterator find_if_not(ExecutionPolicy&& exec,
                              ForwardIterator first, ForwardIterator last,
                              Predicate pred);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  constexpr I ranges::find(I first, S last, const T& value, Proj proj = {});
template<input_range R, class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  constexpr borrowed_iterator_t<R>
    ranges::find(R&& r, const T& value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  I ranges::find(Ep&& exec, I first, S last, const T& value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirect_binary_predicate<ranges::equal_to,
                                     projected<iterator_t<R>, Proj>, const T*>
  borrowed_iterator_t<R> ranges::find(Ep&& exec, R&& r, const T& value, Proj proj = {});

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr I ranges::find_if(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr borrowed_iterator_t<R>
    ranges::find_if(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  I ranges::find_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  borrowed_iterator_t<R> ranges::find_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr I ranges::find_if_not(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr borrowed_iterator_t<R>
    ranges::find_if_not(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  I ranges::find_if_not(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  borrowed_iterator_t<R> ranges::find_if_not(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be:

- `*i == value` for `find`;
- `pred(*i) != false` for `find_if`;
- `pred(*i) == false` for `find_if_not`;
- `bool(invoke(proj, *i) == value)` for `ranges::find`;
- `bool(invoke(pred, invoke(proj, *i)))` for `ranges::find_if`;
- `bool(!invoke(pred, invoke(proj, *i)))` for `ranges::find_if_not`.

*Returns:* The first iterator `i` in the range \[`first`, `last`) for
which E is `true`. Returns `last` if no such iterator is found.

*Complexity:* At most `last - first` applications of the corresponding
predicate and any projection.

### Find last <a id="alg.find.last">[[alg.find.last]]</a>

``` cpp
template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  constexpr subrange<I> ranges::find_last(I first, S last, const T& value, Proj proj = {});
template<forward_range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  constexpr borrowed_subrange_t<R> ranges::find_last(R&& r, const T& value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  subrange<I> ranges::find_last(Ep&& exec, I first, S last, const T& value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
          class T = projected_value_t<iterator_t<R>, Proj>>
  requires
    indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  borrowed_subrange_t<R> ranges::find_last(Ep&& exec, R&& r, const T& value, Proj proj = {});

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr subrange<I> ranges::find_last_if(I first, S last, Pred pred, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr borrowed_subrange_t<R> ranges::find_last_if(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  subrange<I> ranges::find_last_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R,
          class Proj = identity,
          indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  borrowed_subrange_t<R> ranges::find_last_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr subrange<I> ranges::find_last_if_not(I first, S last, Pred pred, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr borrowed_subrange_t<R> ranges::find_last_if_not(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  subrange<I> ranges::find_last_if_not(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  borrowed_subrange_t<R> ranges::find_last_if_not(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be:

- `bool(invoke(proj, *i) == value)` for `ranges::find_last`;
- `bool(invoke(pred, invoke(proj, *i)))` for `ranges::find_last_if`;
- `bool(!invoke(pred, invoke(proj, *i)))` for
  `ranges::find_last_if_not`.

*Returns:* Let `i` be the last iterator in the range \[`first`, `last`)
for which E is `true`. Returns `{i, last}`, or `{last, last}` if no such
iterator is found.

*Complexity:* At most `last - first` applications of the corresponding
predicate and projection.

### Find end <a id="alg.find.end">[[alg.find.end]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  constexpr ForwardIterator1
    find_end(ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator1
    find_end(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);

template<class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  constexpr ForwardIterator1
    find_end(ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  ForwardIterator1
    find_end(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);

template<forward_iterator I1, sentinel_for<I1> S1, forward_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr subrange<I1>
    ranges::find_end(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});
template<forward_range R1, forward_range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr borrowed_subrange_t<R1>
    ranges::find_end(R1&& r1, R2&& r2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  subrange<I1>
    ranges::find_end(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  borrowed_subrange_t<R1>
    ranges::find_end(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `pred` be `equal_to{}` for the overloads with no parameter `pred`;
- E be:
  - `pred(*(i + n), *(first2 + n))` for the overloads in namespace
    `std`;
  - `invoke(pred, invoke(proj1, *(i + n)), invoke(proj2, *(first2 + n)))`
    for the overloads in namespace `ranges`;
- `i` be `last1` if \[`first2`, `last2`) is empty, or if
  `(last2 - first2) > (last1 - first1)` is `true`, or if there is no
  iterator in the range \[`first1`, `last1 - (last2 - first2)`) such
  that for every non-negative integer `n < (last2 - first2)`, E is
  `true`. Otherwise `i` is the last such iterator in \[`first1`,
  `last1 - (last2 - first2)`).

*Returns:*

- `i` for the overloads in namespace `std`.
- `{i, i + (i == last1 ? 0 : last2 - first2)}` for the overloads in
  namespace `ranges`.

*Complexity:* At most
`(last2 - first2) * (last1 - first1 - (last2 - first2) + 1)`
applications of the corresponding predicate and any projections.

### Find first of <a id="alg.find.first.of">[[alg.find.first.of]]</a>

``` cpp
template<class InputIterator, class ForwardIterator>
  constexpr InputIterator
    find_first_of(InputIterator first1, InputIterator last1,
                  ForwardIterator first2, ForwardIterator last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator1
    find_first_of(ExecutionPolicy&& exec,
                  ForwardIterator1 first1, ForwardIterator1 last1,
                  ForwardIterator2 first2, ForwardIterator2 last2);

template<class InputIterator, class ForwardIterator,
         class BinaryPredicate>
  constexpr InputIterator
    find_first_of(InputIterator first1, InputIterator last1,
                  ForwardIterator first2, ForwardIterator last2,
                  BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  ForwardIterator1
    find_first_of(ExecutionPolicy&& exec,
                  ForwardIterator1 first1, ForwardIterator1 last1,
                  ForwardIterator2 first2, ForwardIterator2 last2,
                  BinaryPredicate pred);

template<input_iterator I1, sentinel_for<I1> S1, forward_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr I1 ranges::find_first_of(I1 first1, S1 last1, I2 first2, S2 last2,
                                     Pred pred = {},
                                     Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, forward_range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr borrowed_iterator_t<R1>
    ranges::find_first_of(R1&& r1, R2&& r2,
                          Pred pred = {},
                          Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  I1 ranges::find_first_of(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                           Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  borrowed_iterator_t<R1>
    ranges::find_first_of(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                          Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let E be:

- `*i == *j` for the overloads with no parameter `pred`;
- `pred(*i, *j) != false` for the overloads with a parameter `pred` and
  no parameter `proj1`;
- `bool(invoke(pred, invoke(proj1, *i), invoke(proj2, *j)))` for the
  overloads with parameters `pred` and `proj1`.

*Effects:* Finds an element that matches one of a set of values.

*Returns:* The first iterator `i` in the range \[`first1`, `last1`) such
that for some iterator `j` in the range \[`first2`, `last2`) E holds.
Returns `last1` if \[`first2`, `last2`) is empty or if no such iterator
is found.

*Complexity:* At most `(last1 - first1) * (last2 - first2)` applications
of the corresponding predicate and any projections.

### Adjacent find <a id="alg.adjacent.find">[[alg.adjacent.find]]</a>

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator
    adjacent_find(ForwardIterator first, ForwardIterator last);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator
    adjacent_find(ExecutionPolicy&& exec,
                  ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class BinaryPredicate>
  constexpr ForwardIterator
    adjacent_find(ForwardIterator first, ForwardIterator last,
                  BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator, class BinaryPredicate>
  ForwardIterator
    adjacent_find(ExecutionPolicy&& exec,
                  ForwardIterator first, ForwardIterator last,
                  BinaryPredicate pred);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_binary_predicate<projected<I, Proj>,
                                   projected<I, Proj>> Pred = ranges::equal_to>
  constexpr I ranges::adjacent_find(I first, S last, Pred pred = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_binary_predicate<projected<iterator_t<R>, Proj>,
                                   projected<iterator_t<R>, Proj>> Pred = ranges::equal_to>
  constexpr borrowed_iterator_t<R> ranges::adjacent_find(R&& r, Pred pred = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_binary_predicate<projected<I, Proj>,
                                    projected<I, Proj>> Pred = ranges::equal_to>
  I ranges::adjacent_find(Ep&& exec, I first, S last, Pred pred = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_binary_predicate<projected<iterator_t<R>, Proj>,
                                    projected<iterator_t<R>, Proj>> Pred = ranges::equal_to>
  borrowed_iterator_t<R>
    ranges::adjacent_find(Ep&& exec, R&& r, Pred pred = {}, Proj proj = {});
```

Let E be:

- `*i == *(i + 1)` for the overloads with no parameter `pred`;
- `pred(*i, *(i + 1)) != false` for the overloads with a parameter
  `pred` and no parameter `proj`;
- `bool(invoke(pred, invoke(proj, *i), invoke(proj, *(i + 1))))` for the
  overloads with both parameters `pred` and `proj`.

*Returns:* The first iterator `i` such that both `i` and `i + 1` are in
the range \[`first`, `last`) for which E holds. Returns `last` if no
such iterator is found.

*Complexity:* For the non-parallel algorithm overloads, exactly
$$\min(\texttt{(i - first) + 1}, \ \texttt{(last - first) - 1})$$
applications of the corresponding predicate, where `i` is
`adjacent_find`’s return value. For the parallel algorithm overloads,
𝑂(`last - first`) applications of the corresponding predicate. No more
than twice as many applications of any projection.

### Count <a id="alg.count">[[alg.count]]</a>

``` cpp
template<class InputIterator, class T = iterator_traits<InputIterator>::value_type>
  constexpr typename iterator_traits<InputIterator>::difference_type
    count(InputIterator first, InputIterator last, const T& value);
template<class ExecutionPolicy, class ForwardIterator,
         class T = iterator_traits<ForwardIterator>::value_type>
  typename iterator_traits<ForwardIterator>::difference_type
    count(ExecutionPolicy&& exec,
          ForwardIterator first, ForwardIterator last, const T& value);

template<class InputIterator, class Predicate>
  constexpr typename iterator_traits<InputIterator>::difference_type
    count_if(InputIterator first, InputIterator last, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  typename iterator_traits<ForwardIterator>::difference_type
    count_if(ExecutionPolicy&& exec,
             ForwardIterator first, ForwardIterator last, Predicate pred);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  constexpr iter_difference_t<I>
    ranges::count(I first, S last, const T& value, Proj proj = {});
template<input_range R, class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  constexpr range_difference_t<R>
    ranges::count(R&& r, const T& value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  iter_difference_t<I>
    ranges::count(Ep&& exec, I first, S last, const T& value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirect_binary_predicate<ranges::equal_to,
                                      projected<iterator_t<R>, Proj>, const T*>
  range_difference_t<R> ranges::count(Ep&& exec, R&& r, const T& value, Proj proj = {});

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr iter_difference_t<I>
    ranges::count_if(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr range_difference_t<R>
    ranges::count_if(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  iter_difference_t<I>
    ranges::count_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  range_difference_t<R>
    ranges::count_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be:

- `*i == value` for the overloads with no parameter `pred` or `proj`;
- `pred(*i) != false` for the overloads with a parameter `pred` but no
  parameter `proj`;
- `invoke(proj, *i) == value` for the overloads with a parameter `proj`
  but no parameter `pred`;
- `bool(invoke(pred, invoke(proj, *i)))` for the overloads with both
  parameters `proj` and `pred`.

*Effects:* Returns the number of iterators `i` in the range \[`first`,
`last`) for which E holds.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate and any projection.

### Mismatch <a id="alg.mismatch">[[alg.mismatch]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  constexpr pair<InputIterator1, InputIterator2>
    mismatch(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  pair<ForwardIterator1, ForwardIterator2>
    mismatch(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2);

template<class InputIterator1, class InputIterator2,
         class BinaryPredicate>
  constexpr pair<InputIterator1, InputIterator2>
    mismatch(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  pair<ForwardIterator1, ForwardIterator2>
    mismatch(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, BinaryPredicate pred);

template<class InputIterator1, class InputIterator2>
  constexpr pair<InputIterator1, InputIterator2>
    mismatch(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, InputIterator2 last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  pair<ForwardIterator1, ForwardIterator2>
    mismatch(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);

template<class InputIterator1, class InputIterator2,
         class BinaryPredicate>
  constexpr pair<InputIterator1, InputIterator2>
    mismatch(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, InputIterator2 last2,
             BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  pair<ForwardIterator1, ForwardIterator2>
    mismatch(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr ranges::mismatch_result<I1, I2>
    ranges::mismatch(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr ranges::mismatch_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
    ranges::mismatch(R1&& r1, R2&& r2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  ranges::mismatch_result<I1, I2>
    ranges::mismatch(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  ranges::mismatch_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
    ranges::mismatch(Ep&& exec, R1&& r1, R2&& r2, Pred pred = {},
                     Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let `last2` be `first2 + (last1 - first1)` for the overloads in
namespace `std` with no parameter `last2`.

Let E be:

- `!(*(first1 + n) == *(first2 + n))` for the overloads with no
  parameter `pred`;
- `pred(*(first1 + n), *(first2 + n)) == false` for the overloads with a
  parameter `pred` and no parameter `proj1`;
- `!invoke(pred, invoke(proj1, *(first1 + n)), invoke(proj2, *(first2 + n)))`
  for the overloads with both parameters `pred` and `proj1`.

Let N be \min(`last1 - first1`, \ `last2 - first2`).

*Returns:* `{ first1 + n, first2 + n }`, where `n` is the smallest
integer in \[`0`, N) such that E holds, or N if no such integer exists.

*Complexity:* At most N applications of the corresponding predicate and
any projections.

### Equal <a id="alg.equal">[[alg.equal]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  bool equal(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2);

template<class InputIterator1, class InputIterator2,
         class BinaryPredicate>
  constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2, BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  bool equal(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, BinaryPredicate pred);

template<class InputIterator1, class InputIterator2>
  constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2, InputIterator2 last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  bool equal(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);

template<class InputIterator1, class InputIterator2,
         class BinaryPredicate>
  constexpr bool equal(InputIterator1 first1, InputIterator1 last1,
                       InputIterator2 first2, InputIterator2 last2,
                       BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  bool equal(ExecutionPolicy&& exec,
             ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr bool ranges::equal(I1 first1, S1 last1, I2 first2, S2 last2,
                               Pred pred = {},
                               Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, class Pred = ranges::equal_to,
         class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr bool ranges::equal(R1&& r1, R2&& r2, Pred pred = {},
                               Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  bool ranges::equal(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                     Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  bool ranges::equal(Ep&& exec, R1&& r1, R2&& r2,
                     Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `last2` be `first2 + (last1 - first1)` for the overloads in namespace
  `std` with no parameter `last2`;
- `pred` be `equal_to{}` for the overloads with no parameter `pred`;
- E be:
  - `pred(*i, *(first2 + (i - first1)))` for the overloads with no
    parameter `proj1`;
  - `invoke(pred, invoke(proj1, *i), invoke(proj2, *(first2 + (i - first1))))`
    for the overloads with parameter `proj1`.

*Returns:* If `last1 - first1 != last2 - first2`, return `false`.
Otherwise return `true` if E holds for every iterator `i` in the range
\[`first1`, `last1`). Otherwise, returns `false`.

*Complexity:* If

- the types of `first1`, `last1`, `first2`, and `last2` meet the
  *Cpp17RandomAccessIterator* requirements [[random.access.iterators]]
  and `last1 - first1 != last2 - first2` for the overloads in namespace
  `std`;
- the types of `first1`, `last1`, `first2`, and `last2` pairwise model
  `sized_sentinel_for`[[iterator.concept.sizedsentinel]] and
  `last1 - first1 != last2 - first2` for the first and third overloads
  in namespace `ranges`, or
- `R1` and `R2` each model `sized_range` and
  `ranges::distance(r1) != ranges::distance(r2)` for the second and
  fourth overloads in namespace `ranges`,

then no applications of the corresponding predicate and each projection;
otherwise, at most
$$\min(\texttt{last1 - first1}, \ \texttt{last2 - first2})$$
applications of the corresponding predicate and any projections.

### Is permutation <a id="alg.is.permutation">[[alg.is.permutation]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                ForwardIterator2 first2);
template<class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                ForwardIterator2 first2, BinaryPredicate pred);
template<class ForwardIterator1, class ForwardIterator2>
  constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                ForwardIterator2 first2, ForwardIterator2 last2);
template<class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  constexpr bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                                ForwardIterator2 first2, ForwardIterator2 last2,
                                BinaryPredicate pred);
```

Let `last2` be `first2 + (last1 - first1)` for the overloads with no
parameter named `last2`, and let `pred` be `equal_to{}` for the
overloads with no parameter `pred`.

*Mandates:* `ForwardIterator1` and `ForwardIterator2` have the same
value type.

*Preconditions:* The comparison function is an equivalence relation.

*Returns:* If `last1 - first1 != last2 - first2`, return `false`.
Otherwise return `true` if there exists a permutation of the elements in
the range \[`first2`, `last2`), beginning with `ForwardIterator2 begin`,
such that `equal(first1, last1, begin, pred)` returns `true`; otherwise,
returns `false`.

*Complexity:* No applications of the corresponding predicate if
`ForwardIterator1` and `ForwardIterator2` meet the requirements of
random access iterators and `last1 - first1 != last2 - first2`.
Otherwise, exactly `last1 - first1` applications of the corresponding
predicate if `equal(first1, last1, first2, last2, pred)` would return
`true`; otherwise, at worst 𝑂(N^2), where N has the value
`last1 - first1`.

``` cpp
template<forward_iterator I1, sentinel_for<I1> S1, forward_iterator I2,
         sentinel_for<I2> S2, class Proj1 = identity, class Proj2 = identity,
         indirect_equivalence_relation<projected<I1, Proj1>,
                                       projected<I2, Proj2>> Pred = ranges::equal_to>
  constexpr bool ranges::is_permutation(I1 first1, S1 last1, I2 first2, S2 last2,
                                        Pred pred = {},
                                        Proj1 proj1 = {}, Proj2 proj2 = {});
template<forward_range R1, forward_range R2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_equivalence_relation<projected<iterator_t<R1>, Proj1>,
                                       projected<iterator_t<R2>, Proj2>> Pred = ranges::equal_to>
  constexpr bool ranges::is_permutation(R1&& r1, R2&& r2, Pred pred = {},
                                        Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:* If `last1 - first1 != last2 - first2`, return `false`.
Otherwise return `true` if there exists a permutation of the elements in
the range \[`first2`, `last2`), bounded by \[`pfirst`, `plast`), such
that `ranges::equal(first1, last1, pfirst, plast, pred, proj1, proj2)`
returns `true`; otherwise, returns `false`.

*Complexity:* No applications of the corresponding predicate and
projections if

- for the first overload,
  - `S1` and `I1` model `sized_sentinel_for<S1, I1>`,
  - `S2` and `I2` model `sized_sentinel_for<S2, I2>`, and
  - `last1 - first1 != last2 - first2`;
- for the second overload, `R1` and `R2` each model `sized_range`, and
  `ranges::distance(r1) != ranges::distance(r2)`.

Otherwise, exactly `last1 - first1` applications of the corresponding
predicate and projections if
`ranges::equal(first1, last1, first2, last2, pred, proj1, proj2)` would
return `true`; otherwise, at worst 𝑂(N^2), where N has the value
`last1 - first1`.

### Search <a id="alg.search">[[alg.search]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  constexpr ForwardIterator1
    search(ForwardIterator1 first1, ForwardIterator1 last1,
           ForwardIterator2 first2, ForwardIterator2 last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator1
    search(ExecutionPolicy&& exec,
           ForwardIterator1 first1, ForwardIterator1 last1,
           ForwardIterator2 first2, ForwardIterator2 last2);

template<class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  constexpr ForwardIterator1
    search(ForwardIterator1 first1, ForwardIterator1 last1,
           ForwardIterator2 first2, ForwardIterator2 last2,
           BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  ForwardIterator1
    search(ExecutionPolicy&& exec,
           ForwardIterator1 first1, ForwardIterator1 last1,
           ForwardIterator2 first2, ForwardIterator2 last2,
           BinaryPredicate pred);
```

*Returns:* The first iterator `i` in the range \[`first1`,
`last1 - (last2 - first2)`\] such that for every non-negative integer
`n` less than `last2 - first2` the following corresponding conditions
hold:
`*(i + n) == *(first2 + n), pred(*(i + n), *(first2 + n)) != false`.
Returns `first1` if \[`first2`, `last2`) is empty, otherwise returns
`last1` if no such iterator is found.

*Complexity:* At most `(last1 - first1) * (last2 - first2)` applications
of the corresponding predicate.

``` cpp
template<forward_iterator I1, sentinel_for<I1> S1, forward_iterator I2,
         sentinel_for<I2> S2, class Pred = ranges::equal_to,
         class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr subrange<I1>
    ranges::search(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                   Proj1 proj1 = {}, Proj2 proj2 = {});
template<forward_range R1, forward_range R2, class Pred = ranges::equal_to,
         class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr borrowed_subrange_t<R1>
    ranges::search(R1&& r1, R2&& r2, Pred pred = {},
                   Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  subrange<I1>
    ranges::search(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                   Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  borrowed_subrange_t<R1>
    ranges::search(Ep&& exec, R1&& r1, R2&& r2,
                   Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:*

- `{i, i + (last2 - first2)}`, where `i` is the first iterator in the
  range \[`first1`, `last1 - (last2 - first2)`\] such that for every
  non-negative integer `n` less than `last2 - first2` the condition
  ``` cpp
  bool(invoke(pred, invoke(proj1, *(i + n)), invoke(proj2, *(first2 + n))))
  ```

  is `true`.
- Returns `{last1, last1}` if no such iterator exists.

*Complexity:* At most `(last1 - first1) * (last2 - first2)` applications
of the corresponding predicate and projections.

``` cpp
template<class ForwardIterator, class Size, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr ForwardIterator
    search_n(ForwardIterator first, ForwardIterator last,
             Size count, const T& value);
template<class ExecutionPolicy, class ForwardIterator, class Size,
         class T = iterator_traits<ForwardIterator>::value_type>
  ForwardIterator
    search_n(ExecutionPolicy&& exec,
             ForwardIterator first, ForwardIterator last,
             Size count, const T& value);

template<class ForwardIterator, class Size, class T = iterator_traits<ForwardIterator>::value_type,
         class BinaryPredicate>
  constexpr ForwardIterator
    search_n(ForwardIterator first, ForwardIterator last,
             Size count, const T& value,
             BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Size,
         class T = iterator_traits<ForwardIterator>::value_type,
         class BinaryPredicate>
  ForwardIterator
    search_n(ExecutionPolicy&& exec,
             ForwardIterator first, ForwardIterator last,
             Size count, const T& value,
             BinaryPredicate pred);
```

*Mandates:* The type `Size` is convertible to an integral
type [[conv.integral,class.conv]].

Let E be `pred(*(i + n), value) != false` for the overloads with a
parameter `pred`, and `*(i + n) == value` otherwise.

*Returns:* The first iterator `i` in the range \[`first`,
`last - count`\] such that for every non-negative integer `n` less than
`count` the condition E is `true`. Returns `last` if no such iterator is
found.

*Complexity:* At most `last - first` applications of the corresponding
predicate.

``` cpp
template<forward_iterator I, sentinel_for<I> S,
         class Pred = ranges::equal_to, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirectly_comparable<I, const T*, Pred, Proj>
  constexpr subrange<I>
    ranges::search_n(I first, S last, iter_difference_t<I> count,
                     const T& value, Pred pred = {}, Proj proj = {});
template<forward_range R, class Pred = ranges::equal_to,
         class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirectly_comparable<iterator_t<R>, const T*, Pred, Proj>
  constexpr borrowed_subrange_t<R>
    ranges::search_n(R&& r, range_difference_t<R> count,
                     const T& value, Pred pred = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Pred = ranges::equal_to, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirectly_comparable<I, const T*, Pred, Proj>
  subrange<I>
    ranges::search_n(Ep&& exec, I first, S last, iter_difference_t<I> count,
                     const T& value, Pred pred = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Pred = ranges::equal_to,
         class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirectly_comparable<iterator_t<R>, const T*, Pred, Proj>
  borrowed_subrange_t<R>
    ranges::search_n(Ep&& exec, R&& r, range_difference_t<R> count,
                     const T& value, Pred pred = {}, Proj proj = {});
```

*Returns:* `{i, i + count}` where `i` is the first iterator in the range
\[`first`, `last - count`\] such that for every non-negative integer `n`
less than `count`, the following condition holds:
`invoke(pred, invoke(proj, *(i + n)), value)`. Returns `{last, last}` if
no such iterator is found.

*Complexity:* At most `last - first` applications of the corresponding
predicate and projection.

``` cpp
template<class ForwardIterator, class Searcher>
  constexpr ForwardIterator
    search(ForwardIterator first, ForwardIterator last, const Searcher& searcher);
```

*Effects:* Equivalent to: `return searcher(first, last).first;`

*Remarks:* `Searcher` need not meet the *Cpp17CopyConstructible*
requirements.

### Starts with <a id="alg.starts.with">[[alg.starts.with]]</a>

``` cpp
template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr bool ranges::starts_with(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                                     Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, class Pred = ranges::equal_to, class Proj1 = identity,
         class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr bool ranges::starts_with(R1&& r1, R2&& r2, Pred pred = {},
                                     Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:*

``` cpp
ranges::mismatch(std::move(first1), last1, std::move(first2), last2,
                 pred, proj1, proj2).in2 == last2
```

``` cpp
template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  bool ranges::starts_with(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                           Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1,
         sized-random-access-range R2, class Pred = ranges::equal_to,
         class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  bool ranges::starts_with(Ep&& exec, R1&& r1, R2&& r2,
                           Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:*

``` cpp
ranges::mismatch(std::forward<Ep>(exec), std::move(first1), last1, std::move(first2),
                 last2, pred, proj1, proj2).in2 == last2
```

### Ends with <a id="alg.ends.with">[[alg.ends.with]]</a>

``` cpp
template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires (forward_iterator<I1> || sized_sentinel_for<S1, I1>) &&
           (forward_iterator<I2> || sized_sentinel_for<S2, I2>) &&
           indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  constexpr bool ranges::ends_with(I1 first1, S1 last1, I2 first2, S2 last2, Pred pred = {},
                                   Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let `N1` be `last1 - first1` and `N2` be `last2 - first2`.

*Returns:* `false` if `N1` < `N2`, otherwise:

``` cpp
ranges::equal(std::move(first1) + (N1 - N2), last1, std::move(first2), last2,
              pred, proj1, proj2)
```

``` cpp
template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Pred = ranges::equal_to, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<I1, I2, Pred, Proj1, Proj2>
  bool ranges::ends_with(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                         Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let `N1` be `last1 - first1` and `N2` be `last2 - first2`.

*Returns:* `false` if `N1` < `N2`, otherwise:

``` cpp
ranges::equal(std::forward<Ep>(exec), std::move(first1) + (N1 - N2), last1,
              std::move(first2), last2, pred, proj1, proj2)
```

``` cpp
template<input_range R1, input_range R2, class Pred = ranges::equal_to, class Proj1 = identity,
         class Proj2 = identity>
  requires (forward_range<R1> || sized_range<R1>) &&
           (forward_range<R2> || sized_range<R2>) &&
           indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  constexpr bool ranges::ends_with(R1&& r1, R2&& r2, Pred pred = {},
                                   Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let `N1` be `ranges::distance(r1)` and `N2` be `ranges::distance(r2)`.

*Returns:* `false` if `N1` < `N2`, otherwise:

``` cpp
ranges::equal(views::drop(ranges::ref_view(r1), N1 - static_cast<decltype(N1)>(N2)),
              r2, pred, proj1, proj2)
```

``` cpp
template<execution-policy Ep, sized-random-access-range R1,
         sized-random-access-range R2, class Pred = ranges::equal_to,
         class Proj1 = identity, class Proj2 = identity>
  requires indirectly_comparable<iterator_t<R1>, iterator_t<R2>, Pred, Proj1, Proj2>
  bool ranges::ends_with(Ep&& exec, R1&& r1, R2&& r2,
                         Pred pred = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let `N1` be `ranges::distance(r1)` and `N2` be `ranges::distance(r2)`.

*Returns:* `false` if `N1` < `N2`, otherwise:

``` cpp
ranges::equal(std::forward<Ep>(exec),
              views::drop(ranges::ref_view(r1), N1 - static_cast<decltype(N1)>(N2)),
              r2, pred, proj1, proj2)
```

### Fold <a id="alg.fold">[[alg.fold]]</a>

``` cpp
template<input_iterator I, sentinel_for<I> S, class T = iter_value_t<I>,
         indirectly-binary-left-foldable<T, I> F>
  constexpr auto ranges::fold_left(I first, S last, T init, F f);
template<input_range R, class T = range_value_t<R>,
         indirectly-binary-left-foldable<T, iterator_t<R>> F>
  constexpr auto ranges::fold_left(R&& r, T init, F f);
```

*Returns:*

``` cpp
ranges::fold_left_with_iter(std::move(first), last, std::move(init), f).value
```

``` cpp
template<input_iterator I, sentinel_for<I> S,
         indirectly-binary-left-foldable<iter_value_t<I>, I> F>
  requires constructible_from<iter_value_t<I>, iter_reference_t<I>>
  constexpr auto ranges::fold_left_first(I first, S last, F f);
template<input_range R, indirectly-binary-left-foldable<range_value_t<R>, iterator_t<R>> F>
  requires constructible_from<range_value_t<R>, range_reference_t<R>>
  constexpr auto ranges::fold_left_first(R&& r, F f);
```

*Returns:*

``` cpp
ranges::fold_left_first_with_iter(std::move(first), last, f).value
```

``` cpp
template<bidirectional_iterator I, sentinel_for<I> S, class T = iter_value_t<I>,
         indirectly-binary-right-foldable<T, I> F>
  constexpr auto ranges::fold_right(I first, S last, T init, F f);
template<bidirectional_range R, class T = range_value_t<R>,
         indirectly-binary-right-foldable<T, iterator_t<R>> F>
  constexpr auto ranges::fold_right(R&& r, T init, F f);
```

*Effects:* Equivalent to:

``` cpp
using U = decay_t<invoke_result_t<F&, iter_reference_t<I>, T>>;
if (first == last)
  return U(std::move(init));
I tail = ranges::next(first, last);
U accum = invoke(f, *--tail, std::move(init));
while (first != tail)
  accum = invoke(f, *--tail, std::move(accum));
return accum;
```

``` cpp
template<bidirectional_iterator I, sentinel_for<I> S,
         indirectly-binary-right-foldable<iter_value_t<I>, I> F>
  requires constructible_from<iter_value_t<I>, iter_reference_t<I>>
  constexpr auto ranges::fold_right_last(I first, S last, F f);
template<bidirectional_range R,
         indirectly-binary-right-foldable<range_value_t<R>, iterator_t<R>> F>
  requires constructible_from<range_value_t<R>, range_reference_t<R>>
  constexpr auto ranges::fold_right_last(R&& r, F f);
```

Let `U` be
`decltype(ranges::fold_right(first, last, iter_value_t<I>(*first), f))`.

*Effects:* Equivalent to:

``` cpp
if (first == last)
  return optional<U>();
I tail = ranges::prev(ranges::next(first, std::move(last)));
return optional<U>(in_place,
  ranges::fold_right(std::move(first), tail, iter_value_t<I>(*tail), std::move(f)));
```

``` cpp
template<input_iterator I, sentinel_for<I> S, class T = iter_value_t<I>,
         indirectly-binary-left-foldable<T, I> F>
  constexpr see below ranges::fold_left_with_iter(I first, S last, T init, F f);
template<input_range R, class T = range_value_t<R>,
         indirectly-binary-left-foldable<T, iterator_t<R>> F>
  constexpr see below ranges::fold_left_with_iter(R&& r, T init, F f);
```

Let `U` be `decay_t<invoke_result_t<F&, T, iter_reference_t<I>>>`.

*Effects:* Equivalent to:

``` cpp
if (first == last)
  return {std::move(first), U(std::move(init))};
U accum = invoke(f, std::move(init), *first);
for (++first; first != last; ++first)
  accum = invoke(f, std::move(accum), *first);
return {std::move(first), std::move(accum)};
```

*Remarks:* The return type is `fold_left_with_iter_result<I, U>` for the
first overload and
`fold_left_with_iter_result<borrowed_iterator_t<R>, U>` for the second
overload.

``` cpp
template<input_iterator I, sentinel_for<I> S,
         indirectly-binary-left-foldable<iter_value_t<I>, I> F>
  requires constructible_from<iter_value_t<I>, iter_reference_t<I>>
  constexpr see below ranges::fold_left_first_with_iter(I first, S last, F f);
template<input_range R, indirectly-binary-left-foldable<range_value_t<R>, iterator_t<R>> F>
  requires constructible_from<range_value_t<R>, range_reference_t<R>>
  constexpr see below ranges::fold_left_first_with_iter(R&& r, F f);
```

Let `U` be

``` cpp
decltype(ranges::fold_left(std::move(first), last, iter_value_t<I>(*first), f))
```

*Effects:* Equivalent to:

``` cpp
if (first == last)
  return {std::move(first), optional<U>()};
optional<U> init(in_place, *first);
for (++first; first != last; ++first)
  *init = invoke(f, std::move(*init), *first);
return {std::move(first), std::move(init)};
```

*Remarks:* The return type is
`fold_left_first_with_iter_result<I, optional<U>>` for the first
overload and
`fold_left_first_with_iter_result<borrowed_iterator_t<R>, optional<U>>`
for the second overload.

## Mutating sequence operations <a id="alg.modifying.operations">[[alg.modifying.operations]]</a>

### Copy <a id="alg.copy">[[alg.copy]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  constexpr OutputIterator copy(InputIterator first, InputIterator last,
                                OutputIterator result);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O>
  requires indirectly_copyable<I, O>
  constexpr ranges::copy_result<I, O> ranges::copy(I first, S last, O result);
template<input_range R, weakly_incrementable O>
  requires indirectly_copyable<iterator_t<R>, O>
  constexpr ranges::copy_result<borrowed_iterator_t<R>, O> ranges::copy(R&& r, O result);
```

Let N be `last - first`.

*Preconditions:* `result` is not in the range \[`first`, `last`).

*Effects:* Copies elements in the range \[`first`, `last`) into the
range \[`result`, `result + `N) starting from `first` and proceeding to
`last`. For each non-negative integer n < N, performs
`*(result + `n`) = *(first + `n`)`.

*Returns:*

- `result + `N for the overload in namespace `std`.
- `{last, result + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2 copy(ExecutionPolicy&& exec,
                        ForwardIterator1 first, ForwardIterator1 last,
                        ForwardIterator2 result);

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS>
  requires indirectly_copyable<I, O>
  ranges::copy_result<I, O>
    ranges::copy(Ep&& exec, I first, S last, O result, OutS result_last);
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
  ranges::copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::copy(Ep&& exec, R&& r, OutR&& result_r);
```

Let `result_last` be `result + (last - first)` for the overload in
namespace `std`.

Let N be \min(`last - first`, \ `result_last - result`).

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

*Effects:* Copies elements in the range \[`first`, `first + `N) into the
range \[`result`, `result + `N). For each non-negative integer n < N,
performs `*(result + `n`) = *(first + `n`)`.

*Returns:*

- `result + `N for the overload in namespace `std`.
- `{first + `N`, result + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<class InputIterator, class Size, class OutputIterator>
  constexpr OutputIterator copy_n(InputIterator first, Size n,
                                  OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class Size, class ForwardIterator2>
  ForwardIterator2 copy_n(ExecutionPolicy&& exec,
                          ForwardIterator1 first, Size n,
                          ForwardIterator2 result);

template<input_iterator I, weakly_incrementable O>
  requires indirectly_copyable<I, O>
  constexpr ranges::copy_n_result<I, O>
    ranges::copy_n(I first, iter_difference_t<I> n, O result);

template<execution-policy Ep, random_access_iterator I, random_access_iterator O,
         sized_sentinel_for<O> OutS>
  requires indirectly_copyable<I, O>
  ranges::copy_n_result<I, O>
    ranges::copy_n(Ep&& exec, I first, iter_difference_t<I> n, O result, OutS result_last);
```

Let M be \max(0, \ `n`).

Let `result_last` be `result + `M for the overloads with no parameter
`result_last`.

Let N be \min(`result_last - result`, M).

*Mandates:* The type `Size` is convertible to an integral
type [[conv.integral,class.conv]].

*Effects:* For each non-negative integer i < N, performs
`*(result + `i`) = *(first + `i`)`.

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{first + `N`, result + `N`}` for the overload in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<class InputIterator, class OutputIterator, class Predicate>
  constexpr OutputIterator copy_if(InputIterator first, InputIterator last,
                                   OutputIterator result, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class Predicate>
  ForwardIterator2 copy_if(ExecutionPolicy&& exec,
                           ForwardIterator1 first, ForwardIterator1 last,
                           ForwardIterator2 result, Predicate pred);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O>
  constexpr ranges::copy_if_result<I, O>
    ranges::copy_if(I first, S last, O result, Pred pred, Proj proj = {});
template<input_range R, weakly_incrementable O, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, O>
  constexpr ranges::copy_if_result<borrowed_iterator_t<R>, O>
    ranges::copy_if(R&& r, O result, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
          random_access_iterator O, sized_sentinel_for<O> OutS,
          class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O>
  ranges::copy_if_result<I, O>
    ranges::copy_if(Ep&& exec, I first, S last, O result, OutS result_last,
                    Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
          class Proj = identity,
          indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
  ranges::copy_if_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::copy_if(Ep&& exec, R&& r, OutR&& result_r, Pred pred, Proj proj = {});
```

Let E(`i`) be:

- `bool(pred(*i))` for the overloads in namespace `std`;
- `bool(invoke(pred, invoke(proj, *i)))` for the overloads in namespace
  `ranges`.

Let:

- M be the number of iterators `i` in the range \[`first`, `last`) for
  which the condition E(`i`) holds;
- `result_last` be `result + `M for the overloads with no parameter
  `result_last` or `result_r`;
- N be \min(M, \ `result_last - result`).

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

[*Note 1*: For the parallel algorithm overload in namespace `std`,
there can be a performance cost if
`iterator_traits<ForwardIterator1>::value_type` does not meet the
*Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) requirements.
For the parallel algorithm overloads in namespace `ranges`, there can be
a performance cost if `iter_value_t<I>` does not model
`move_constructible`. — *end note*]

*Effects:* Copies the first N elements referred to by the iterator `i`
in the range \[`first`, `last`) for which E(`i`) is `true` into the
range \[`result`, `result + `N).

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{last, result + `N`}` for the overloads in namespace `ranges`, if N
  is equal to M.
- Otherwise, `{j, result_last}` for the overloads in namespace `ranges`,
  where `j` is the iterator in \[`first`, `last`) for which E(`j`) holds
  and there are exactly N iterators `i` in \[`first`, `j`) for which
  E(`i`) holds.

*Complexity:* At most `last - first` applications of the corresponding
predicate and any projection.

*Remarks:* Stable [[algorithm.stable]].

``` cpp
template<class BidirectionalIterator1, class BidirectionalIterator2>
  constexpr BidirectionalIterator2
    copy_backward(BidirectionalIterator1 first,
                  BidirectionalIterator1 last,
                  BidirectionalIterator2 result);

template<bidirectional_iterator I1, sentinel_for<I1> S1, bidirectional_iterator I2>
  requires indirectly_copyable<I1, I2>
  constexpr ranges::copy_backward_result<I1, I2>
    ranges::copy_backward(I1 first, S1 last, I2 result);
template<bidirectional_range R, bidirectional_iterator I>
  requires indirectly_copyable<iterator_t<R>, I>
  constexpr ranges::copy_backward_result<borrowed_iterator_t<R>, I>
    ranges::copy_backward(R&& r, I result);
```

Let N be `last - first`.

*Preconditions:* `result` is not in the range (`first`, `last`).

*Effects:* Copies elements in the range \[`first`, `last`) into the
range \[`result - `N, `result`) starting from `last - 1` and proceeding
to `first`.[^2]

For each positive integer n ≤ N, performs
`*(result - `n`) = *(last - `n`)`.

*Returns:*

- `result - `N for the overload in namespace `std`.
- `{last, result - `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

### Move <a id="alg.move">[[alg.move]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  constexpr OutputIterator move(InputIterator first, InputIterator last,
                                OutputIterator result);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O>
  requires indirectly_movable<I, O>
  constexpr ranges::move_result<I, O>
    ranges::move(I first, S last, O result);
template<input_range R, weakly_incrementable O>
  requires indirectly_movable<iterator_t<R>, O>
  constexpr ranges::move_result<borrowed_iterator_t<R>, O>
    ranges::move(R&& r, O result);
```

Let E(n) be

- `std::move(*(first + `n`))` for the overload in namespace `std`;
- `ranges::iter_move(first + `n`)` for the overloads in namespace
  `ranges`.

Let N be `last - first`.

*Preconditions:* `result` is not in the range \[`first`, `last`).

*Effects:* Moves elements in the range \[`first`, `last`) into the range
\[`result`, `result + `N) starting from `first` and proceeding to
`last`. For each non-negative integer n < N, performs
`*(result + `n`) = `E(n).

*Returns:*

- `result + `N for the overload in namespace `std`.
- `{last, result + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2 move(ExecutionPolicy&& exec,
                        ForwardIterator1 first, ForwardIterator1 last,
                        ForwardIterator2 result);

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS>
  requires indirectly_movable<I, O>
  ranges::move_result<I, O>
    ranges::move(Ep&& exec, I first, S last, O result, OutS result_last);
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
  requires indirectly_movable<iterator_t<R>, iterator_t<OutR>>
  ranges::move_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::move(Ep&& exec, R&& r, OutR&& result_r);
```

Let E(n) be:

- `std::move(*(first + `n`))` for the overload in namespace `std`;
- `ranges::iter_move(first + `n`)` for the overloads in namespace
  `ranges`.

Let `result_last` be `result + (last - first)` for the overloads in
namespace `std`.

Let N be \min(`last - first`, \ `result_last - result`).

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

*Effects:* Moves elements in the range \[`first`, `first + `N) into the
range \[`result`, `result + `N). For each non-negative integer n < N,
performs `*(result + `n`) = `E(n).

*Returns:*

- `result + `N for the overload in namespace `std`.
- `{first + `N`, result + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<class BidirectionalIterator1, class BidirectionalIterator2>
  constexpr BidirectionalIterator2
    move_backward(BidirectionalIterator1 first, BidirectionalIterator1 last,
                  BidirectionalIterator2 result);

template<bidirectional_iterator I1, sentinel_for<I1> S1, bidirectional_iterator I2>
  requires indirectly_movable<I1, I2>
  constexpr ranges::move_backward_result<I1, I2>
    ranges::move_backward(I1 first, S1 last, I2 result);
template<bidirectional_range R, bidirectional_iterator I>
  requires indirectly_movable<iterator_t<R>, I>
  constexpr ranges::move_backward_result<borrowed_iterator_t<R>, I>
    ranges::move_backward(R&& r, I result);
```

Let E(n) be

- `std::move(*(last - `n`))` for the overload in namespace `std`;
- `ranges::iter_move(last - `n`)` for the overloads in namespace
  `ranges`.

Let N be `last - first`.

*Preconditions:* `result` is not in the range (`first`, `last`).

*Effects:* Moves elements in the range \[`first`, `last`) into the range
\[`result - `N, `result`) starting from `last - 1` and proceeding to
`first`.[^3]

For each positive integer n ≤ N, performs `*(result - `n`) = `E(n).

*Returns:*

- `result - `N for the overload in namespace `std`.
- `{last, result - `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

### Swap <a id="alg.swap">[[alg.swap]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  constexpr ForwardIterator2
    swap_ranges(ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    swap_ranges(ExecutionPolicy&& exec,
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2>
  requires indirectly_swappable<I1, I2>
  constexpr ranges::swap_ranges_result<I1, I2>
    ranges::swap_ranges(I1 first1, S1 last1, I2 first2, S2 last2);
template<input_range R1, input_range R2>
  requires indirectly_swappable<iterator_t<R1>, iterator_t<R2>>
  constexpr ranges::swap_ranges_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
    ranges::swap_ranges(R1&& r1, R2&& r2);

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2>
  requires indirectly_swappable<I1, I2>
  ranges::swap_ranges_result<I1, I2>
    ranges::swap_ranges(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2);
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2>
  requires indirectly_swappable<iterator_t<R1>, iterator_t<R2>>
  ranges::swap_ranges_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
    ranges::swap_ranges(Ep&& exec, R1&& r1, R2&& r2);
```

Let:

- `last2` be `first2 + (last1 - first1)` for the overloads in namespace
  `std` with no parameter named `last2`;
- M be \min(`last1 - first1`, \ `last2 - first2`).

*Preconditions:* The two ranges \[`first1`, `last1`) and \[`first2`,
`last2`) do not overlap. For the overloads in namespace `std`,
`*(first1 + `n`)` is swappable with [[swappable.requirements]]
`*(first2 + `n`)`.

*Effects:* For each non-negative integer n < M performs:

- `swap(*(first1 + `n`), *(first2 + `n`))` for the overloads in
  namespace `std`;
- `ranges::iter_swap(first1 + `n`, first2 + `n`)` for the overloads in
  namespace `ranges`.

*Returns:*

- `last2` for the overloads in namespace `std`.
- `{first1 + `M`, first2 + `M`}` for the overloads in namespace
  `ranges`.

*Complexity:* Exactly M swaps.

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  constexpr void iter_swap(ForwardIterator1 a, ForwardIterator2 b);
```

*Preconditions:* `a` and `b` are dereferenceable. `*a` is swappable
with [[swappable.requirements]] `*b`.

*Effects:* As if by `swap(*a, *b)`.

### Transform <a id="alg.transform">[[alg.transform]]</a>

``` cpp
template<class InputIterator, class OutputIterator,
         class UnaryOperation>
  constexpr OutputIterator
    transform(InputIterator first1, InputIterator last1,
              OutputIterator result, UnaryOperation op);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class UnaryOperation>
  ForwardIterator2
    transform(ExecutionPolicy&& exec,
              ForwardIterator1 first1, ForwardIterator1 last1,
              ForwardIterator2 result, UnaryOperation op);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class BinaryOperation>
  constexpr OutputIterator
    transform(InputIterator1 first1, InputIterator1 last1,
              InputIterator2 first2, OutputIterator result,
              BinaryOperation binary_op);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator, class BinaryOperation>
  ForwardIterator
    transform(ExecutionPolicy&& exec,
              ForwardIterator1 first1, ForwardIterator1 last1,
              ForwardIterator2 first2, ForwardIterator result,
              BinaryOperation binary_op);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
         copy_constructible F, class Proj = identity>
  requires indirectly_writable<O, indirect_result_t<F&, projected<I, Proj>>>
  constexpr ranges::unary_transform_result<I, O>
    ranges::transform(I first1, S last1, O result, F op, Proj proj = {});
template<input_range R, weakly_incrementable O, copy_constructible F,
         class Proj = identity>
  requires indirectly_writable<O, indirect_result_t<F&, projected<iterator_t<R>, Proj>>>
  constexpr ranges::unary_transform_result<borrowed_iterator_t<R>, O>
    ranges::transform(R&& r, O result, F op, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS,
         copy_constructible F, class Proj = identity>
  requires indirectly_writable<O, indirect_result_t<F&, projected<I, Proj>>>
  ranges::unary_transform_result<I, O>
    ranges::transform(Ep&& exec, I first1, S last1, O result, OutS result_last,
                      F op, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
          copy_constructible F, class Proj = identity>
  requires indirectly_writable<iterator_t<OutR>,
                                indirect_result_t<F&, projected<iterator_t<R>, Proj>>>
  ranges::unary_transform_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::transform(Ep&& exec, R&& r, OutR&& result_r, F op, Proj proj = {});

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         weakly_incrementable O, copy_constructible F, class Proj1 = identity,
         class Proj2 = identity>
  requires indirectly_writable<O, indirect_result_t<F&, projected<I1, Proj1>,
                               projected<I2, Proj2>>>
  constexpr ranges::binary_transform_result<I1, I2, O>
    ranges::transform(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                      F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, weakly_incrementable O,
         copy_constructible F, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_writable<O, indirect_result_t<F&, projected<iterator_t<R1>, Proj1>,
                               projected<iterator_t<R2>, Proj2>>>
  constexpr ranges::binary_transform_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
    ranges::transform(R1&& r1, R2&& r2, O result,
                      F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         random_access_iterator O, sized_sentinel_for<O> OutS,
         copy_constructible F, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_writable<O, indirect_result_t<F&, projected<I1, Proj1>,
                                projected<I2, Proj2>>>
  ranges::binary_transform_result<I1, I2, O>
    ranges::transform(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                      O result, OutS result_last,
                      F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         sized-random-access-range OutR, copy_constructible F,
          class Proj1 = identity, class Proj2 = identity>
  requires indirectly_writable<iterator_t<OutR>,
                                indirect_result_t<F&, projected<iterator_t<R1>, Proj1>,
                                projected<iterator_t<R2>, Proj2>>>
  ranges::binary_transform_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                                  borrowed_iterator_t<OutR>>
    ranges::transform(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r,
                      F binary_op, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `last2` be `first2 + (last1 - first1)` for the overloads in namespace
  `std` with parameter `first2` but no parameter `last2`;
- M be `last1 - first1` for unary transforms, or
  \min(`last1 - first1`, \ `last2 - first2`) for binary transforms;
- `result_last` be `result + `M for the overloads with no parameter
  `result_last` or `result_r`;
- N be \min(M, \ `result_last - result`);
- E(`i`) be
  - `op(*(first1 + (i - result)))` for unary transforms defined in
    namespace `std`;
  - `binary_op(*(first1 + (i - result)), *(first2 + (i - result)))` for
    binary transforms defined in namespace `std`;
  - `invoke(op, invoke(proj, *(first1 + (i - result))))` for unary
    transforms defined in namespace `ranges`;
  - `invoke(binary_op, invoke(proj1, *(first1 + (i - result))), invoke(proj2,*(first2 + (i - result))))`
    for binary transforms defined in namespace `ranges`.

*Preconditions:* For parallel algorithm overloads `op` and `binary_op`
satisfy the requirements specified in [[algorithms.parallel.user]]. `op`
and `binary_op` do not invalidate iterators or subranges, nor modify
elements in the ranges

- \[`first1`, `first1 + `N\],
- \[`first2`, `first2 + `N\], and
- \[`result`, `result + `N\].[^4]

*Effects:* Assigns through every iterator `i` in the range \[`result`,
`result + `N) a new corresponding value equal to E(`i`).

*Returns:*

- `result + `N for the overloads defined in namespace `std`.
- `{first1 + `N`, result + `N`}` for unary transforms defined in
  namespace `ranges`.
- `{first1 + `N`, first2 + `N`, result + `N`}` for binary transforms
  defined in namespace `ranges`.

*Complexity:* Exactly N applications of `op` or `binary_op`, and any
projections. This requirement also applies to the parallel algorithm
overloads.

*Remarks:* `result` may be equal to `first1` or `first2`.

### Replace <a id="alg.replace">[[alg.replace]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr void replace(ForwardIterator first, ForwardIterator last,
                         const T& old_value, const T& new_value);
template<class ExecutionPolicy, class ForwardIterator,
         class T = iterator_traits<ForwardIterator>::value_type>
  void replace(ExecutionPolicy&& exec,
               ForwardIterator first, ForwardIterator last,
               const T& old_value, const T& new_value);

template<class ForwardIterator, class Predicate,
         class T = iterator_traits<ForwardIterator>::value_type>
  constexpr void replace_if(ForwardIterator first, ForwardIterator last,
                            Predicate pred, const T& new_value);
template<class ExecutionPolicy, class ForwardIterator, class Predicate,
         class T = iterator_traits<ForwardIterator>::value_type>
  void replace_if(ExecutionPolicy&& exec,
                  ForwardIterator first, ForwardIterator last,
                  Predicate pred, const T& new_value);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         class T1 = projected_value_t<I, Proj>, class T2 = T1>
  requires indirectly_writable<I, const T2&> &&
           indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*>
  constexpr I
    ranges::replace(I first, S last, const T1& old_value, const T2& new_value, Proj proj = {});
template<input_range R, class Proj = identity,
         class T1 = projected_value_t<iterator_t<R>, Proj>, class T2 = T1>
  requires indirectly_writable<iterator_t<R>, const T2&> &&
           indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T1*>
  constexpr borrowed_iterator_t<R>
    ranges::replace(R&& r, const T1& old_value, const T2& new_value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T1 = projected_value_t<I, Proj>, class T2 = T1>
  requires indirectly_writable<I, const T2&> &&
           indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*>
  I ranges::replace(Ep&& exec, I first, S last,
                    const T1& old_value, const T2& new_value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         class T1 = projected_value_t<iterator_t<R>, Proj>, class T2 = T1>
  requires indirectly_writable<iterator_t<R>, const T2&> &&
            indirect_binary_predicate<ranges::equal_to,
                                      projected<iterator_t<R>, Proj>, const T1*>
  borrowed_iterator_t<R>
    ranges::replace(Ep&& exec, R&& r, const T1& old_value, const T2& new_value,
                    Proj proj = {});

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_writable<I, const T&>
  constexpr I ranges::replace_if(I first, S last, Pred pred, const T& new_value, Proj proj = {});
template<input_range R, class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_writable<iterator_t<R>, const T&>
  constexpr borrowed_iterator_t<R>
    ranges::replace_if(R&& r, Pred pred, const T& new_value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T = projected_value_t<I, Proj>,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_writable<I, const T&>
  I ranges::replace_if(Ep&& exec, I first, S last, Pred pred,
                       const T& new_value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_writable<iterator_t<R>, const T&>
  borrowed_iterator_t<R>
    ranges::replace_if(Ep&& exec, R&& r, Pred pred, const T& new_value, Proj proj = {});
```

Let E(`i`) be

- `bool(*i == old_value)` for `replace`;
- `bool(pred(*i))` for `replace_if`;
- `bool(invoke(proj, *i) == old_value)` for `ranges::replace`;
- `bool(invoke(pred, invoke(proj, *i)))` for `ranges::replace_if`.

*Mandates:* `new_value` is writable [[iterator.requirements.general]] to
`first`.

*Effects:* Substitutes elements referred by the iterator `i` in the
range \[`first`, `last`) with `new_value`, when E(`i`) is `true`.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate and any projection.

``` cpp
template<class InputIterator, class OutputIterator, class T>
  constexpr OutputIterator
    replace_copy(InputIterator first, InputIterator last,
                 OutputIterator result,
                 const T& old_value, const T& new_value);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T>
  ForwardIterator2
    replace_copy(ExecutionPolicy&& exec,
                 ForwardIterator1 first, ForwardIterator1 last,
                 ForwardIterator2 result,
                 const T& old_value, const T& new_value);

template<class InputIterator, class OutputIterator, class Predicate, class T>
  constexpr OutputIterator
    replace_copy_if(InputIterator first, InputIterator last,
                    OutputIterator result,
                    Predicate pred, const T& new_value);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class Predicate, class T>
  ForwardIterator2
    replace_copy_if(ExecutionPolicy&& exec,
                    ForwardIterator1 first, ForwardIterator1 last,
                    ForwardIterator2 result,
                    Predicate pred, const T& new_value);

template<input_iterator I, sentinel_for<I> S, class O,
         class Proj = identity, class T1 = projected_value_t<I, Proj>, class T2 = iter_value_t<O>>
  requires indirectly_copyable<I, O> &&
           indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*> &&
           output_iterator<O, const T2&>
  constexpr ranges::replace_copy_result<I, O>
    ranges::replace_copy(I first, S last, O result, const T1& old_value, const T2& new_value,
                         Proj proj = {});
template<input_range R, class O, class Proj = identity,
         class T1 = projected_value_t<iterator_t<R>, Proj>, class T2 = iter_value_t<O>>
  requires indirectly_copyable<iterator_t<R>, O> &&
           indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T1*>
           && output_iterator<O, const T2&>
  constexpr ranges::replace_copy_result<borrowed_iterator_t<R>, O>
    ranges::replace_copy(R&& r, O result, const T1& old_value, const T2& new_value,
                         Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS,
         class Proj = identity,
         class T1 = projected_value_t<I, Proj>, class T2 = iter_value_t<O>>
  requires indirectly_copyable<I, O> &&
           indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T1*> &&
           indirectly_writable<O, const T2&>
  ranges::replace_copy_result<I, O>
    ranges::replace_copy(Ep&& exec, I first, S last, O result, OutS result_last,
                         const T1& old_value, const T2& new_value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
         class Proj = identity, class T1 = projected_value_t<iterator_t<R>, Proj>,
         class T2 = range_value_t<OutR>>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>> &&
           indirect_binary_predicate<ranges::equal_to,
                                      projected<iterator_t<R>, Proj>, const T1*> &&
           indirectly_writable<iterator_t<OutR>, const T2&>
  ranges::replace_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::replace_copy(Ep&& exec, R&& r, OutR&& result_r, const T1& old_value,
                         const T2& new_value, Proj proj = {});

template<input_iterator I, sentinel_for<I> S,class O, class T = iter_value_t<O>,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O> && output_iterator<O, const T&>
  constexpr ranges::replace_copy_if_result<I, O>
    ranges::replace_copy_if(I first, S last, O result, Pred pred, const T& new_value,
                            Proj proj = {});
template<input_range R, class O, class T = iter_value_t<O>, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, O> && output_iterator<O, const T&>
  constexpr ranges::replace_copy_if_result<borrowed_iterator_t<R>, O>
    ranges::replace_copy_if(R&& r, O result, Pred pred, const T& new_value,
                            Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS, class T = iter_value_t<O>,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O> && indirectly_writable<O, const T&>
  ranges::replace_copy_if_result<I, O>
    ranges::replace_copy_if(Ep&& exec, I first, S last, O result, OutS result_last,
                            Pred pred, const T& new_value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
         class T = range_value_t<OutR>, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>> &&
           indirectly_writable<OutR, const T&>
  ranges::replace_copy_if_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::replace_copy_if(Ep&& exec, R&& r, OutR&& result_r, Pred pred, const T& new_value,
                            Proj proj = {});
```

Let E(`i`) be

- `bool(*(first + (i - result)) == old_value)` for `replace_copy`;
- `bool(pred(*(first + (i - result))))` for `replace_copy_if`;
- `bool(invoke(proj, *(first + (i - result))) == old_value)` for
  `ranges::replace_copy`;
- `bool(invoke(pred, invoke(proj, *(first + (i - result)))))` for
  `ranges::replace_copy_if`.

Let:

- `result_last` be `result + (last - first)` for the overloads with no
  parameter `result_last` or `result_r`;
- N be \min(`last - first`, \ `result_last - result`).

*Mandates:* The results of the expressions `*first` and `new_value` are
writable [[iterator.requirements.general]] to `result`.

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

*Effects:* Assigns through every iterator `i` in the range \[`result`,
`result + `N) a new corresponding value

- `new_value` if E(`i`) is `true` or
- `*(first + (i - result))` otherwise.

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{first + `N`, result + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N applications of the corresponding predicate and
any projection.

### Fill <a id="alg.fill">[[alg.fill]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr void fill(ForwardIterator first, ForwardIterator last, const T& value);
template<class ExecutionPolicy, class ForwardIterator,
         class T = iterator_traits<ForwardIterator>::value_type>
  void fill(ExecutionPolicy&& exec,
            ForwardIterator first, ForwardIterator last, const T& value);

template<class OutputIterator, class Size, class T = iterator_traits<OutputIterator>::value_type>
  constexpr OutputIterator fill_n(OutputIterator first, Size n, const T& value);
template<class ExecutionPolicy, class ForwardIterator, class Size,
         class T = iterator_traits<ForwardIterator>::value_type>
  ForwardIterator fill_n(ExecutionPolicy&& exec,
                         ForwardIterator first, Size n, const T& value);

template<class O, sentinel_for<O> S, class T = iter_value_t<O>>
  requires output_iterator<O, const T&>
  constexpr O ranges::fill(O first, S last, const T& value);
template<class R, class T = range_value_t<R>>
  requires output_range<R, const T&>
  constexpr borrowed_iterator_t<R> ranges::fill(R&& r, const T& value);
template<class O, class T = iter_value_t<O>>
  requires output_iterator<O, const T&>
  constexpr O ranges::fill_n(O first, iter_difference_t<O> n, const T& value);

template<execution-policy Ep, random_access_iterator O, sized_sentinel_for<O> S,
         class T = iter_value_t<O>>
  requires indirectly_writable<O, const T&>
  O ranges::fill(Ep&& exec, O first, S last, const T& value);
template<execution-policy Ep, sized-random-access-range R, class T = range_value_t<R>>
  requires indirectly_writable<iterator_t<R>, const T&>
  borrowed_iterator_t<R> fill(Ep&& exec, R&& r, const T& value);
template<execution-policy Ep, random_access_iterator O, class T = iter_value_t<O>>
  requires indirectly_writable<O, const T&>
  O ranges::fill_n(Ep&& exec, O first, iter_difference_t<O> n, const T& value);
```

Let N be \max(0, `n`) for the `fill_n` algorithms, and `last - first`
for the `fill` algorithms.

*Mandates:* The expression `value` is
writable [[iterator.requirements.general]] to the output iterator. The
type `Size` is convertible to an integral
type [[conv.integral,class.conv]].

*Effects:* Assigns `value` through all the iterators in the range
\[`first`, `first + `N).

*Returns:* `first + `N.

*Complexity:* Exactly N assignments.

### Generate <a id="alg.generate">[[alg.generate]]</a>

``` cpp
template<class ForwardIterator, class Generator>
  constexpr void generate(ForwardIterator first, ForwardIterator last,
                          Generator gen);
template<class ExecutionPolicy, class ForwardIterator, class Generator>
  void generate(ExecutionPolicy&& exec,
                ForwardIterator first, ForwardIterator last,
                Generator gen);

template<class OutputIterator, class Size, class Generator>
  constexpr OutputIterator generate_n(OutputIterator first, Size n, Generator gen);
template<class ExecutionPolicy, class ForwardIterator, class Size, class Generator>
  ForwardIterator generate_n(ExecutionPolicy&& exec,
                             ForwardIterator first, Size n, Generator gen);

template<input_or_output_iterator O, sentinel_for<O> S, copy_constructible F>
  requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
  constexpr O ranges::generate(O first, S last, F gen);
template<class R, copy_constructible F>
  requires invocable<F&> && output_range<R, invoke_result_t<F&>>
  constexpr borrowed_iterator_t<R> ranges::generate(R&& r, F gen);
template<input_or_output_iterator O, copy_constructible F>
  requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
  constexpr O ranges::generate_n(O first, iter_difference_t<O> n, F gen);

template<execution-policy Ep, random_access_iterator O, sized_sentinel_for<O> S,
         copy_constructible F>
  requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
  O ranges::generate(Ep&& exec, O first, S last, F gen);
template<execution-policy Ep, sized-random-access-range R, copy_constructible F>
  requires invocable<F&> && indirectly_writable<iterator_t<R>, invoke_result_t<F&>>
  borrowed_iterator_t<R> ranges::generate(Ep&& exec, R&& r, F gen);
template<execution-policy Ep, random_access_iterator O, copy_constructible F>
  requires invocable<F&> && indirectly_writable<O, invoke_result_t<F&>>
  O ranges::generate_n(Ep&& exec, O first, iter_difference_t<O> n, F gen);
```

Let N be \max(0, `n`) for the `generate_n` algorithms, and
`last - first` for the `generate` algorithms.

*Mandates:* `Size` is convertible to an integral
type [[conv.integral,class.conv]].

*Effects:* Assigns the result of successive evaluations of `gen()`
through each iterator in the range \[`first`, `first + `N).

*Returns:* `first + `N.

*Complexity:* Exactly N evaluations of `gen()` and assignments.

*Remarks:* `gen` may modify objects via its arguments for parallel
algorithm overloads [[algorithms.parallel.user]].

### Remove <a id="alg.remove">[[alg.remove]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr ForwardIterator remove(ForwardIterator first, ForwardIterator last,
                                   const T& value);
template<class ExecutionPolicy, class ForwardIterator,
         class T = iterator_traits<ForwardIterator>::value_type>
  ForwardIterator remove(ExecutionPolicy&& exec,
                         ForwardIterator first, ForwardIterator last,
                         const T& value);

template<class ForwardIterator, class Predicate>
  constexpr ForwardIterator remove_if(ForwardIterator first, ForwardIterator last,
                                      Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  ForwardIterator remove_if(ExecutionPolicy&& exec,
                            ForwardIterator first, ForwardIterator last,
                            Predicate pred);

template<permutable I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  constexpr subrange<I> ranges::remove(I first, S last, const T& value, Proj proj = {});
template<forward_range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires permutable<iterator_t<R>> &&
           indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  constexpr borrowed_subrange_t<R>
    ranges::remove(R&& r, const T& value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  subrange<I>
    ranges::remove(Ep&& exec, I first, S last, const T& value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires permutable<iterator_t<R>> &&
           indirect_binary_predicate<ranges::equal_to,
                                      projected<iterator_t<R>, Proj>, const T*>
  borrowed_subrange_t<R>
    ranges::remove(Ep&& exec, R&& r, const T& value, Proj proj = {});

template<permutable I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr subrange<I> ranges::remove_if(I first, S last, Pred pred, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R>
    ranges::remove_if(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  subrange<I>
    ranges::remove_if(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R>
    ranges::remove_if(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let E be

- `bool(*i == value)` for `remove`;
- `bool(pred(*i))` for `remove_if`;
- `bool(invoke(proj, *i) == value)` for `ranges::remove`;
- `bool(invoke(pred, invoke(proj, *i)))` for `ranges::remove_if`.

*Preconditions:* For the algorithms in namespace `std`, the type of
`*first` meets the *Cpp17MoveAssignable* requirements
([[cpp17.moveassignable]]).

*Effects:* Eliminates all the elements referred to by iterator `i` in
the range \[`first`, `last`) for which E holds.

*Returns:* Let j be the end of the resulting range. Returns:

- j for the overloads in namespace `std`.
- `{`j`, last}` for the overloads in namespace `ranges`.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate and any projection.

*Remarks:* Stable [[algorithm.stable]].

[*Note 1*: Each element in the range \[`ret`, `last`), where `ret` is
the returned value, has a valid but unspecified state, because the
algorithms can eliminate elements by moving from elements that were
originally in that range. — *end note*]

``` cpp
template<class InputIterator, class OutputIterator,
         class T = iterator_traits<InputIterator>::value_type>
  constexpr OutputIterator
    remove_copy(InputIterator first, InputIterator last,
                OutputIterator result, const T& value);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class T = iterator_traits<ForwardIterator1>::value_type>
  ForwardIterator2
    remove_copy(ExecutionPolicy&& exec,
                ForwardIterator1 first, ForwardIterator1 last,
                ForwardIterator2 result, const T& value);

template<class InputIterator, class OutputIterator, class Predicate>
  constexpr OutputIterator
    remove_copy_if(InputIterator first, InputIterator last,
                   OutputIterator result, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class Predicate>
  ForwardIterator2
    remove_copy_if(ExecutionPolicy&& exec,
                   ForwardIterator1 first, ForwardIterator1 last,
                   ForwardIterator2 result, Predicate pred);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirectly_copyable<I, O> &&
           indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  constexpr ranges::remove_copy_result<I, O>
    ranges::remove_copy(I first, S last, O result, const T& value, Proj proj = {});
template<input_range R, weakly_incrementable O, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirectly_copyable<iterator_t<R>, O> &&
           indirect_binary_predicate<ranges::equal_to, projected<iterator_t<R>, Proj>, const T*>
  constexpr ranges::remove_copy_result<borrowed_iterator_t<R>, O>
    ranges::remove_copy(R&& r, O result, const T& value, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS,
         class Proj = identity, class T = projected_value_t<I, Proj>>
  requires indirectly_copyable<I, O> &&
           indirect_binary_predicate<ranges::equal_to, projected<I, Proj>, const T*>
  ranges::remove_copy_result<I, O>
    ranges::remove_copy(Ep&& exec, I first, S last, O result, OutS result_last,
                        const T& value, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
         class Proj = identity, class T = projected_value_t<iterator_t<R>, Proj>>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>> &&
           indirect_binary_predicate<ranges::equal_to,
                                      projected<iterator_t<R>, Proj>, const T*>
  ranges::remove_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::remove_copy(Ep&& exec, R&& r, OutR&& result_r, const T& value, Proj proj = {});

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O>
  constexpr ranges::remove_copy_if_result<I, O>
    ranges::remove_copy_if(I first, S last, O result, Pred pred, Proj proj = {});
template<input_range R, weakly_incrementable O, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, O>
  constexpr ranges::remove_copy_if_result<borrowed_iterator_t<R>, O>
    ranges::remove_copy_if(R&& r, O result, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O>
  ranges::remove_copy_if_result<I, O>
    ranges::remove_copy_if(Ep&& exec, I first, S last, O result, OutS result_last,
                           Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
         class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
  ranges::remove_copy_if_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::remove_copy_if(Ep&& exec, R&& r, OutR&& result_r, Pred pred, Proj proj = {});
```

Let E(`i`) be

- `bool(*i == value)` for `remove_copy`;
- `bool(pred(*i))` for `remove_copy_if`;
- `bool(invoke(proj, *i) == value)` for `ranges::remove_copy`;
- `bool(invoke(pred, invoke(proj, *i)))` for `ranges::remove_copy_if`.

Let:

- M be the number of iterators `i` in \[`first`, `last`) for which
  E(`i`) is `false`;
- `result_last` be `result + `M for the overloads with no parameter
  `result_last` or `result_r`;
- N be \min(M, \ `result_last - result`).

*Mandates:* `*first` is writable [[iterator.requirements.general]] to
`result`.

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

[*Note 2*: For the parallel algorithm overloads in namespace `std`,
there can be a performance cost if
`iterator_traits<ForwardIterator1>::value_type` does not meet the
*Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) requirements.
For the parallel algorithm overloads in namespace `ranges`, there can be
a performance cost if `iter_value_t<I>` does not model
`move_constructible`. — *end note*]

*Effects:* Copies the first N elements referred to by the iterator `i`
in the range \[`first`, `last`) for which E(`i`) is `false` into the
range \[`result`, `result + `N).

*Returns:*

- `result + `N, for the algorithms in namespace `std`.
- `{last, result + `N`}`, for the algorithms in namespace `ranges`, if N
  is equal to M.
- Otherwise, `{j, result_last}`, for the algorithms in namespace
  `ranges`, where `j` is the iterator in \[`first`, `last`) for which
  E(`j`) is `false` and there are exactly N iterators `i` in \[`first`,
  `j`) for which E(`i`) is `false`.

*Complexity:* At most `last - first` applications of the corresponding
predicate and any projection.

*Remarks:* Stable [[algorithm.stable]].

### Unique <a id="alg.unique">[[alg.unique]]</a>

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator unique(ForwardIterator first, ForwardIterator last);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator unique(ExecutionPolicy&& exec,
                         ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class BinaryPredicate>
  constexpr ForwardIterator unique(ForwardIterator first, ForwardIterator last,
                                   BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator, class BinaryPredicate>
  ForwardIterator unique(ExecutionPolicy&& exec,
                         ForwardIterator first, ForwardIterator last,
                         BinaryPredicate pred);

template<permutable I, sentinel_for<I> S, class Proj = identity,
         indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
  constexpr subrange<I> ranges::unique(I first, S last, C comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R>
    ranges::unique(R&& r, C comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
  requires permutable<I>
  subrange<I> ranges::unique(Ep&& exec, I first, S last, C comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R> ranges::unique(Ep&& exec, R&& r, C comp = {}, Proj proj = {});
```

Let `pred` be `equal_to{}` for the overloads with no parameter `pred`,
and let E be

- `bool(pred(*(i - 1), *i))` for the overloads in namespace `std`;
- `bool(invoke(comp, invoke(proj, *(i - 1)), invoke(proj, *i)))` for the
  overloads in namespace `ranges`.

*Preconditions:* For the overloads in namespace `std`, `pred` is an
equivalence relation and the type of `*first` meets the
*Cpp17MoveAssignable* requirements ([[cpp17.moveassignable]]).

*Effects:* For a nonempty range, eliminates all but the first element
from every consecutive group of equivalent elements referred to by the
iterator `i` in the range \[`first + 1`, `last`) for which E is `true`.

*Returns:* Let j be the end of the resulting range. Returns:

- j for the overloads in namespace `std`.
- `{`j`, last}` for the overloads in namespace `ranges`.

*Complexity:* For nonempty ranges, exactly `(last - first) - 1`
applications of the corresponding predicate and no more than twice as
many applications of any projection.

``` cpp
template<class InputIterator, class OutputIterator>
  constexpr OutputIterator
    unique_copy(InputIterator first, InputIterator last,
                OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    unique_copy(ExecutionPolicy&& exec,
                ForwardIterator1 first, ForwardIterator1 last,
                ForwardIterator2 result);

template<class InputIterator, class OutputIterator,
         class BinaryPredicate>
  constexpr OutputIterator
    unique_copy(InputIterator first, InputIterator last,
                OutputIterator result, BinaryPredicate pred);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  ForwardIterator2
    unique_copy(ExecutionPolicy&& exec,
                ForwardIterator1 first, ForwardIterator1 last,
                ForwardIterator2 result, BinaryPredicate pred);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O, class Proj = identity,
         indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
  requires indirectly_copyable<I, O> &&
           (forward_iterator<I> ||
            (input_iterator<O> && same_as<iter_value_t<I>, iter_value_t<O>>) ||
            indirectly_copyable_storable<I, O>)
  constexpr ranges::unique_copy_result<I, O>
    ranges::unique_copy(I first, S last, O result, C comp = {}, Proj proj = {});
template<input_range R, weakly_incrementable O, class Proj = identity,
         indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
  requires indirectly_copyable<iterator_t<R>, O> &&
           (forward_iterator<iterator_t<R>> ||
            (input_iterator<O> && same_as<range_value_t<R>, iter_value_t<O>>) ||
            indirectly_copyable_storable<iterator_t<R>, O>)
  constexpr ranges::unique_copy_result<borrowed_iterator_t<R>, O>
    ranges::unique_copy(R&& r, O result, C comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS, class Proj = identity,
         indirect_equivalence_relation<projected<I, Proj>> C = ranges::equal_to>
  requires indirectly_copyable<I, O>
  ranges::unique_copy_result<I, O>
    ranges::unique_copy(Ep&& exec, I first, S last, O result, OutS result_last,
                        C comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR,
         class Proj = identity,
         indirect_equivalence_relation<projected<iterator_t<R>, Proj>> C = ranges::equal_to>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
  ranges::unique_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::unique_copy(Ep&& exec, R&& r, OutR&& result_r, C comp = {}, Proj proj = {});
```

Let `pred` be `equal_to{}` for the overloads in namespace `std` with no
parameter `pred`, and let E(`i`) be

- `bool(pred(*i, *(i - 1)))` for the overloads in namespace `std`;
- `bool(invoke(comp, invoke(proj, *i), invoke(proj, *(i - 1))))` for the
  overloads in namespace `ranges`.

Let:

- M be the number of iterators `i` in the range \[`first + 1`, `last`)
  for which E(`i`) is `false`;
- `result_last` be `result + `M` + 1` for the overloads with no
  parameter `result_last` or `result_r`;
- N be \min(M + 1, \ `result_last - result`).

*Mandates:* `*first` is writable [[iterator.requirements.general]] to
`result`.

*Preconditions:*

- The ranges \[`first`, `last`) and \[`result`, `result + `N) do not
  overlap.
- For the overloads in namespace `std`:
  - The comparison function is an equivalence relation.
  - For the overloads with no `ExecutionPolicy`, let `T` be the value
    type of `InputIterator`. If `InputIterator` models
    `forward_iterator`[[iterator.concept.forward]], then there are no
    additional requirements for `T`. Otherwise, if `OutputIterator`
    meets the *Cpp17ForwardIterator* requirements and its value type is
    the same as `T`, then `T` meets the *Cpp17CopyAssignable*
    ([[cpp17.copyassignable]]) requirements. Otherwise, `T` meets both
    the *Cpp17CopyConstructible* ([[cpp17.copyconstructible]]) and
    *Cpp17CopyAssignable* requirements.

[*Note 1*: For the parallel algorithm overloads in namespace `std`,
there can be a performance cost if the value type of `ForwardIterator1`
does not meet both the *Cpp17CopyConstructible* and
*Cpp17CopyAssignable* requirements. For the parallel algorithm overloads
in namespace `ranges`, there can be a performance cost if
`iter_value_t<I>` does not model `copyable`. — *end note*]

*Effects:* Copies only the first element from N consecutive groups of
equivalent elements referred to by the iterator `i` in the range
\[`first + 1`, `last`) for which E(`i`) holds into the range \[`result`,
`result + `N).

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{last, result + `N`}` for the overloads in namespace `ranges`, if N
  is equal to M + 1.
- Otherwise, `{j, result_last}` for the overloads in namespace `ranges`,
  where `j` is the iterator in \[`first + 1`, `last`) for which E(`j`)
  is `false` and there are exactly N - 1 iterators `i` in \[`first + 1`,
  `j`) for which E(`i`) is `false`.

*Complexity:* At most `last - first - 1` applications of the
corresponding predicate and no more than twice as many applications of
any projection.

### Reverse <a id="alg.reverse">[[alg.reverse]]</a>

``` cpp
template<class BidirectionalIterator>
  constexpr void reverse(BidirectionalIterator first, BidirectionalIterator last);
template<class ExecutionPolicy, class BidirectionalIterator>
  void reverse(ExecutionPolicy&& exec,
               BidirectionalIterator first, BidirectionalIterator last);

template<bidirectional_iterator I, sentinel_for<I> S>
  requires permutable<I>
  constexpr I ranges::reverse(I first, S last);
template<bidirectional_range R>
  requires permutable<iterator_t<R>>
  constexpr borrowed_iterator_t<R> ranges::reverse(R&& r);

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
  requires permutable<I>
  I ranges::reverse(Ep&& exec, I first, S last);
template<execution-policy Ep, sized-random-access-range R>
  requires permutable<iterator_t<R>>
  borrowed_iterator_t<R> ranges::reverse(Ep&& exec, R&& r);
```

*Preconditions:* For the overloads in namespace `std`,
`BidirectionalIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]].

*Effects:* For each non-negative integer `i < (last - first) / 2`,
applies `std::iter_swap`, or `ranges::iter_swap` for the overloads in
namespace `ranges`, to all pairs of iterators
`first + i, (last - i) - 1`.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* Exactly `(last - first)/2` swaps.

``` cpp
template<class BidirectionalIterator, class OutputIterator>
  constexpr OutputIterator
    reverse_copy(BidirectionalIterator first, BidirectionalIterator last,
                 OutputIterator result);
template<class ExecutionPolicy, class BidirectionalIterator, class ForwardIterator>
  ForwardIterator
    reverse_copy(ExecutionPolicy&& exec,
                 BidirectionalIterator first, BidirectionalIterator last,
                 ForwardIterator result);

template<bidirectional_iterator I, sentinel_for<I> S, weakly_incrementable O>
  requires indirectly_copyable<I, O>
  constexpr ranges::reverse_copy_result<I, O>
    ranges::reverse_copy(I first, S last, O result);
template<bidirectional_range R, weakly_incrementable O>
  requires indirectly_copyable<iterator_t<R>, O>
  constexpr ranges::reverse_copy_result<borrowed_iterator_t<R>, O>
    ranges::reverse_copy(R&& r, O result);
```

Let N be `last - first`.

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

*Effects:* Copies the range \[`first`, `last`) to the range \[`result`,
`result + `N) such that for every non-negative integer `i < `N the
following assignment takes place:
`*(result + `N` - 1 - i) = *(first + i)`.

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{last, result + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS>
  requires indirectly_copyable<I, O>
  ranges::reverse_copy_truncated_result<I, O>
    ranges::reverse_copy(Ep&& exec, I first, S last, O result,
                         OutS result_last);
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
  ranges::reverse_copy_truncated_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::reverse_copy(Ep&& exec, R&& r, OutR&& result_r);
```

Let N be \min(`last - first`, \ `result_last - result`), and let
*NEW_FIRST* be `first + (last - first) - `N.

*Preconditions:* The ranges \[`first`, `last`) and \[`result`,
`result + `N) do not overlap.

*Effects:* Copies the range \[*`NEW_FIRST`*, `last`) to the range
\[`result`, `result + `N) such that for every non-negative integer i < N
the following assignment takes place:
`*(result + `N` - 1 - `i`) = *(`*`NEW_FIRST`*` + `i`)`.

*Returns:* `{last, `*`NEW_FIRST`*`, result + `N`}`.

*Complexity:* Exactly N assignments.

### Rotate <a id="alg.rotate">[[alg.rotate]]</a>

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator
    rotate(ForwardIterator first, ForwardIterator middle, ForwardIterator last);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator
    rotate(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator middle, ForwardIterator last);

template<permutable I, sentinel_for<I> S>
  constexpr subrange<I> ranges::rotate(I first, I middle, S last);
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
  requires permutable<I>
  subrange<I> ranges::rotate(Ep&& exec, I first, I middle, S last);
```

*Preconditions:* \[`first`, `middle`) and \[`middle`, `last`) are valid
ranges. For the overloads in namespace `std`, `ForwardIterator` meets
the *Cpp17ValueSwappable* requirements [[swappable.requirements]], and
the type of `*first` meets the *Cpp17MoveConstructible*
([[cpp17.moveconstructible]]) and *Cpp17MoveAssignable*
([[cpp17.moveassignable]]) requirements.

*Effects:* For each non-negative integer `i < (last - first)`, places
the element from the position `first + i` into position
`first + (i + (last - middle)) % (last - first)`.

[*Note 1*: This is a left rotate. — *end note*]

*Returns:*

- `first + (last - middle)` for the overloads in namespace `std`.
- `{first + (last - middle), last}` for the overload in namespace
  `ranges`.

*Complexity:* At most `last - first` swaps.

``` cpp
template<forward_range R>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R> ranges::rotate(R&& r, iterator_t<R> middle);
```

*Effects:* Equivalent to:
`return ranges::rotate(ranges::begin(r), middle, ranges::end(r));`

``` cpp
template<execution-policy Ep, sized-random-access-range R>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R> ranges::rotate(Ep&& exec, R&& r, iterator_t<R> middle);
```

*Effects:* Equivalent to:

``` cpp
return ranges::rotate(std::forward<Ep>(exec), ranges::begin(r), middle, ranges::end(r));
```

``` cpp
template<class ForwardIterator, class OutputIterator>
  constexpr OutputIterator
    rotate_copy(ForwardIterator first, ForwardIterator middle, ForwardIterator last,
                OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    rotate_copy(ExecutionPolicy&& exec,
                ForwardIterator1 first, ForwardIterator1 middle, ForwardIterator1 last,
                ForwardIterator2 result);

  template<forward_iterator I, sentinel_for<I> S, weakly_incrementable O>
    requires indirectly_copyable<I, O>
    constexpr ranges::rotate_copy_result<I, O>
      ranges::rotate_copy(I first, I middle, S last, O result);
```

Let N be `last - first`.

*Preconditions:* \[`first`, `middle`) and \[`middle`, `last`) are valid
ranges. The ranges \[`first`, `last`) and \[`result`, `result + `N) do
not overlap.

*Effects:* Copies the range \[`first`, `last`) to the range \[`result`,
`result + `N) such that for each non-negative integer i < N the
following assignment takes place:
`*(result + `i`) = *(first + (`i` + (middle - first)) % `N`)`.

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{last, result + `N`}` for the overload in namespace `ranges`.

*Complexity:* Exactly N assignments.

``` cpp
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O, sized_sentinel_for<O> OutS>
  requires indirectly_copyable<I, O>
  ranges::rotate_copy_truncated_result<I, O>
    ranges::rotate_copy(Ep&& exec, I first, I middle, S last, O result, OutS result_last);
```

Let M be `last - first` and N be \min(M, \ `result_last - result`).

*Preconditions:* \[`first`, `middle`) and \[`middle`, `last`) are valid
ranges. The ranges \[`first`, `last`) and \[`result`, `result + `N) do
not overlap.

*Effects:* Copies the range \[`first`, `last`) to the range \[`result`,
`result + `N) such that for each non-negative integer i < N the
following assignment takes place:
`*(result + `i`) = *(first + (`i` + (middle - first)) % `M`)`.

*Returns:*

- `{middle + `N`, first, result + `N`}` if N is less than
  `last - middle`.
- Otherwise,
  `{last, first + (`N` + (middle - first)) % `M`, result + `N`}`.

*Complexity:* Exactly N assignments.

``` cpp
template<forward_range R, weakly_incrementable O>
  requires indirectly_copyable<iterator_t<R>, O>
  constexpr ranges::rotate_copy_result<borrowed_iterator_t<R>, O>
    ranges::rotate_copy(R&& r, iterator_t<R> middle, O result);
```

*Effects:* Equivalent to:

``` cpp
return ranges::rotate_copy(ranges::begin(r), middle, ranges::end(r), std::move(result));
```

``` cpp
template<execution-policy Ep, sized-random-access-range R, sized-random-access-range OutR>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR>>
  ranges::rotate_copy_truncated_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR>>
    ranges::rotate_copy(Ep&& exec, R&& r, iterator_t<R> middle, OutR&& result_r);
```

*Effects:* Equivalent to:

``` cpp
return ranges::rotate_copy(std::forward<Ep>(exec), ranges::begin(r), middle, ranges::end(r),
                           ranges::begin(result_r), ranges::end(result_r));
```

### Sample <a id="alg.random.sample">[[alg.random.sample]]</a>

``` cpp
template<class PopulationIterator, class SampleIterator,
         class Distance, class UniformRandomBitGenerator>
  SampleIterator sample(PopulationIterator first, PopulationIterator last,
                        SampleIterator out, Distance n,
                        UniformRandomBitGenerator&& g);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O, class Gen>
  requires (forward_iterator<I> || random_access_iterator<O>) &&
           indirectly_copyable<I, O> &&
           uniform_random_bit_generator<remove_reference_t<Gen>>
  O ranges::sample(I first, S last, O out, iter_difference_t<I> n, Gen&& g);
template<input_range R, weakly_incrementable O, class Gen>
  requires (forward_range<R> || random_access_iterator<O>) &&
           indirectly_copyable<iterator_t<R>, O> &&
           uniform_random_bit_generator<remove_reference_t<Gen>>
  O ranges::sample(R&& r, O out, range_difference_t<R> n, Gen&& g);
```

*Mandates:* For the overload in namespace `std`, `Distance` is an
integer type and `*first` is writable [[iterator.requirements.general]]
to `out`.

*Preconditions:* `out` is not in the range \[`first`, `last`). For the
overload in namespace `std`:

- `PopulationIterator` meets the *Cpp17InputIterator*
  requirements [[input.iterators]].
- `SampleIterator` meets the *Cpp17OutputIterator*
  requirements [[output.iterators]].
- `SampleIterator` meets the *Cpp17RandomAccessIterator*
  requirements [[random.access.iterators]] unless `PopulationIterator`
  models `forward_iterator`[[iterator.concept.forward]].
- `remove_reference_t<UniformRandomBitGenerator>` meets the requirements
  of a uniform random bit generator type [[rand.req.urng]].

*Effects:* Copies \min(`last - first`, \ `n`) elements (the *sample*)
from \[`first`, `last`) (the *population*) to `out` such that each
possible sample has equal probability of appearance.

[*Note 1*: Algorithms that obtain such effects include *selection
sampling* and *reservoir sampling*. — *end note*]

*Returns:* The end of the resulting sample range.

*Complexity:* 𝑂(`last - first`).

*Remarks:*

- For the overload in namespace `std`, stable if and only if
  `PopulationIterator` models `forward_iterator`. For the first overload
  in namespace `ranges`, stable if and only if `I` models
  `forward_iterator`.
- To the extent that the implementation of this function makes use of
  random numbers, the object `g` serves as the implementation’s source
  of randomness.

### Shuffle <a id="alg.random.shuffle">[[alg.random.shuffle]]</a>

``` cpp
template<class RandomAccessIterator, class UniformRandomBitGenerator>
  void shuffle(RandomAccessIterator first,
               RandomAccessIterator last,
               UniformRandomBitGenerator&& g);

template<random_access_iterator I, sentinel_for<I> S, class Gen>
  requires permutable<I> &&
           uniform_random_bit_generator<remove_reference_t<Gen>>
  I ranges::shuffle(I first, S last, Gen&& g);
template<random_access_range R, class Gen>
  requires permutable<iterator_t<R>> &&
           uniform_random_bit_generator<remove_reference_t<Gen>>
  borrowed_iterator_t<R> ranges::shuffle(R&& r, Gen&& g);
```

*Preconditions:* For the overload in namespace `std`:

- `RandomAccessIterator` meets the *Cpp17ValueSwappable*
  requirements [[swappable.requirements]].
- The type `remove_reference_t<UniformRandomBitGenerator>` meets the
  uniform random bit generator [[rand.req.urng]] requirements.

*Effects:* Permutes the elements in the range \[`first`, `last`) such
that each possible permutation of those elements has equal probability
of appearance.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* Exactly `(last - first) - 1` swaps.

*Remarks:* To the extent that the implementation of this function makes
use of random numbers, the object referenced by `g` shall serve as the
implementation’s source of randomness.

### Shift <a id="alg.shift">[[alg.shift]]</a>

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator
    shift_left(ForwardIterator first, ForwardIterator last,
               typename iterator_traits<ForwardIterator>::difference_type n);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator
    shift_left(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
               typename iterator_traits<ForwardIterator>::difference_type n);

template<permutable I, sentinel_for<I> S>
  constexpr subrange<I> ranges::shift_left(I first, S last, iter_difference_t<I> n);
template<forward_range R>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R> ranges::shift_left(R&& r, range_difference_t<R> n);

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
  requires permutable<I>
  subrange<I>
    ranges::shift_left(Ep&& exec, I first, S last, iter_difference_t<I> n);
template<execution-policy Ep, sized-random-access-range R>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R>
    ranges::shift_left(Ep&& exec, R&& r, range_difference_t<R> n);
```

*Preconditions:* `n >= 0` is `true`. For the overloads in namespace
`std`, the type of `*first` meets the *Cpp17MoveAssignable*
requirements.

*Effects:* If `n == 0` or `n >= last - first`, does nothing. Otherwise,
moves the element from position `first + n + i` into position
`first + i` for each non-negative integer `i < (last - first) - n`. For
the non-parallel algorithm overloads, does so in order starting from
`i = 0` and proceeding to `i = (last - first) - n - 1`.

*Returns:* Let *NEW_LAST* be `first + (last - first - n)` if
`n < last - first`, otherwise `first`. Returns:

- *NEW_LAST* for the overloads in namespace `std`.
- `{first, `*`NEW_LAST`*`}` for the overloads in namespace `ranges`.

*Complexity:* At most `(last - first) - n` assignments.

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator
    shift_right(ForwardIterator first, ForwardIterator last,
                typename iterator_traits<ForwardIterator>::difference_type n);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator
    shift_right(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last,
                typename iterator_traits<ForwardIterator>::difference_type n);

template<permutable I, sentinel_for<I> S>
  constexpr subrange<I> ranges::shift_right(I first, S last, iter_difference_t<I> n);
template<forward_range R>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R> ranges::shift_right(R&& r, range_difference_t<R> n);

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S>
  requires permutable<I>
  subrange<I>
    ranges::shift_right(Ep&& exec, I first, S last, iter_difference_t<I> n);
template<execution-policy Ep, sized-random-access-range R>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R>
    ranges::shift_right(Ep&& exec, R&& r, range_difference_t<R> n);
```

*Preconditions:* `n >= 0` is `true`. For the overloads in namespace
`std`, the type of `*first` meets the *Cpp17MoveAssignable*
requirements, and `ForwardIterator` meets the
*Cpp17BidirectionalIterator* requirements [[bidirectional.iterators]] or
the *Cpp17ValueSwappable* requirements.

*Effects:* If `n == 0` or `n >= last - first`, does nothing. Otherwise,
moves the element from position `first + i` into position
`first + n + i` for each non-negative integer `i < (last - first) - n`.
Does so in order starting from `i = (last - first) - n - 1` and
proceeding to `i = 0` if

- for the non-parallel algorithm overload in namespace `std`,
  `ForwardIterator` meets the *Cpp17BidirectionalIterator* requirements,
- for the non-parallel algorithm overloads in namespace `ranges`, `I`
  models `bidirectional_iterator`.

*Returns:* Let *NEW_FIRST* be `first + n` if `n < last - first`,
otherwise `last`. Returns:

- *NEW_FIRST* for the overloads in namespace `std`.
- `{`*`NEW_FIRST`*`, last}` for the overloads in namespace `ranges`.

*Complexity:* At most `(last - first) - n` assignments or swaps.

## Sorting and related operations <a id="alg.sorting">[[alg.sorting]]</a>

### General <a id="alg.sorting.general">[[alg.sorting.general]]</a>

The operations in  [[alg.sorting]] defined directly in namespace `std`
have two versions: one that takes a function object of type `Compare`
and one that uses an `operator<`.

`Compare` is a function object type [[function.objects]] that meets the
requirements for a template parameter named `BinaryPredicate` 
[[algorithms.requirements]]. The return value of the function call
operation applied to an object of type `Compare`, when converted to
`bool`, yields `true` if the first argument of the call is less than the
second, and `false` otherwise. `Compare comp` is used throughout for
algorithms assuming an ordering relation.

For all algorithms that take `Compare`, there is a version that uses
`operator<` instead. That is, `comp(*i, *j) != false` defaults to
`*i < *j != false`. For algorithms other than those described in 
[[alg.binary.search]], `comp` shall induce a strict weak ordering on the
values.

The term *strict* refers to the requirement of an irreflexive relation
(`!comp(x, x)` for all `x`), and the term *weak* to requirements that
are not as strong as those for a total ordering, but stronger than those
for a partial ordering. If we define `equiv(a, b)` as
`!comp(a, b) && !comp(b, a)`, then the requirements are that `comp` and
`equiv` both be transitive relations:

- `comp(a, b) && comp(b, c)` implies `comp(a, c)`
- `equiv(a, b) && equiv(b, c)` implies `equiv(a, c)`

[*Note 1*:

Under these conditions, it can be shown that

- `equiv` is an equivalence relation,
- `comp` induces a well-defined relation on the equivalence classes
  determined by `equiv`, and
- the induced relation is a strict total ordering.

— *end note*]

A sequence is *sorted with respect to a `comp` and `proj`* for a
comparator and projection `comp` and `proj` if for every iterator `i`
pointing to the sequence and every non-negative integer `n` such that
`i + n` is a valid iterator pointing to an element of the sequence,

``` cpp
bool(invoke(comp, invoke(proj, *(i + n)), invoke(proj, *i)))
```

is `false`.

A sequence is *sorted with respect to a comparator `comp`* for a
comparator `comp` if it is sorted with respect to `comp` and
`identity{}` (the identity projection).

A sequence \[`start`, `finish`) is *partitioned with respect to an
expression* `f(e)` if there exists an integer `n` such that for all
`0 <= i < (finish - start)`, `f(*(start + i))` is `true` if and only if
`i < n`.

In the descriptions of the functions that deal with ordering
relationships we frequently use a notion of equivalence to describe
concepts such as stability. The equivalence to which we refer is not
necessarily an `operator==`, but an equivalence relation induced by the
strict weak ordering. That is, two elements `a` and `b` are considered
equivalent if and only if `!(a < b) && !(b < a)`.

### Sorting <a id="alg.sort">[[alg.sort]]</a>

#### `sort` <a id="sort">[[sort]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void sort(RandomAccessIterator first, RandomAccessIterator last);
template<class ExecutionPolicy, class RandomAccessIterator>
  void sort(ExecutionPolicy&& exec,
            RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void sort(RandomAccessIterator first, RandomAccessIterator last,
                      Compare comp);
template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
  void sort(ExecutionPolicy&& exec,
            RandomAccessIterator first, RandomAccessIterator last,
            Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::sort(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::sort(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Comp = ranges::less, class Proj = identity>
  requires sortable<I, Comp, Proj>
  I ranges::sort(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  borrowed_iterator_t<R> ranges::sort(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Sorts the elements in the range \[`first`, `last`) with
respect to `comp` and `proj`.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* Let N be `last - first`. 𝑂(N log N) comparisons and
projections.

#### `stable_sort` <a id="stable.sort">[[stable.sort]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void stable_sort(RandomAccessIterator first, RandomAccessIterator last);
template<class ExecutionPolicy, class RandomAccessIterator>
  void stable_sort(ExecutionPolicy&& exec,
                   RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void stable_sort(RandomAccessIterator first, RandomAccessIterator last,
                             Compare comp);
template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
  void stable_sort(ExecutionPolicy&& exec,
                   RandomAccessIterator first, RandomAccessIterator last,
                   Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I ranges::stable_sort(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::stable_sort(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Comp = ranges::less, class Proj = identity>
  requires sortable<I, Comp, Proj>
  I ranges::stable_sort(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  borrowed_iterator_t<R>
    ranges::stable_sort(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Sorts the elements in the range \[`first`, `last`) with
respect to `comp` and `proj`.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* Let N be `last - first`. If enough extra memory is
available, N log(N) comparisons. Otherwise, at most N log²(N)
comparisons. In either case, twice as many projections as the number of
comparisons.

*Remarks:* Stable [[algorithm.stable]].

#### `partial_sort` <a id="partial.sort">[[partial.sort]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void partial_sort(RandomAccessIterator first,
                              RandomAccessIterator middle,
                              RandomAccessIterator last);
template<class ExecutionPolicy, class RandomAccessIterator>
  void partial_sort(ExecutionPolicy&& exec,
                    RandomAccessIterator first,
                    RandomAccessIterator middle,
                    RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void partial_sort(RandomAccessIterator first,
                              RandomAccessIterator middle,
                              RandomAccessIterator last,
                              Compare comp);
template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
  void partial_sort(ExecutionPolicy&& exec,
                    RandomAccessIterator first,
                    RandomAccessIterator middle,
                    RandomAccessIterator last,
                    Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::partial_sort(I first, I middle, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Comp = ranges::less, class Proj = identity>
  requires sortable<I, Comp, Proj>
  I ranges::partial_sort(Ep&& exec, I first, I middle, S last, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* \[`first`, `middle`) and \[`middle`, `last`) are valid
ranges. For the overloads in namespace `std`, `RandomAccessIterator`
meets the *Cpp17ValueSwappable* requirements [[swappable.requirements]]
and the type of `*first` meets the *Cpp17MoveConstructible*
([[cpp17.moveconstructible]]) and *Cpp17MoveAssignable*
([[cpp17.moveassignable]]) requirements.

*Effects:* Places the first `middle - first` elements from the range
\[`first`, `last`) as sorted with respect to `comp` and `proj` into the
range \[`first`, `middle`). The rest of the elements in the range
\[`middle`, `last`) are placed in an unspecified order.

*Returns:* `last` for the overload in namespace `ranges`.

*Complexity:* Approximately `(last - first) * log(middle - first)`
comparisons, and twice as many projections.

``` cpp
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::partial_sort(R&& r, iterator_t<R> middle, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::partial_sort(ranges::begin(r), middle, ranges::end(r), comp, proj);
```

``` cpp
template<execution-policy Ep, sized-random-access-range R,
         class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  borrowed_iterator_t<R>
    ranges::partial_sort(Ep&& exec, R&& r, iterator_t<R> middle, Comp comp = {},
                         Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::partial_sort(std::forward<Ep>(exec), ranges::begin(r), middle,
                            ranges::end(r), comp, proj);
```

#### `partial_sort_copy` <a id="partial.sort.copy">[[partial.sort.copy]]</a>

``` cpp
template<class InputIterator, class RandomAccessIterator>
  constexpr RandomAccessIterator
    partial_sort_copy(InputIterator first, InputIterator last,
                      RandomAccessIterator result_first,
                      RandomAccessIterator result_last);
template<class ExecutionPolicy, class ForwardIterator, class RandomAccessIterator>
  RandomAccessIterator
    partial_sort_copy(ExecutionPolicy&& exec,
                      ForwardIterator first, ForwardIterator last,
                      RandomAccessIterator result_first,
                      RandomAccessIterator result_last);

template<class InputIterator, class RandomAccessIterator,
         class Compare>
  constexpr RandomAccessIterator
    partial_sort_copy(InputIterator first, InputIterator last,
                      RandomAccessIterator result_first,
                      RandomAccessIterator result_last,
                      Compare comp);
template<class ExecutionPolicy, class ForwardIterator, class RandomAccessIterator,
         class Compare>
  RandomAccessIterator
    partial_sort_copy(ExecutionPolicy&& exec,
                      ForwardIterator first, ForwardIterator last,
                      RandomAccessIterator result_first,
                      RandomAccessIterator result_last,
                      Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, random_access_iterator I2, sentinel_for<I2> S2,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_copyable<I1, I2> && sortable<I2, Comp, Proj2> &&
           indirect_strict_weak_order<Comp, projected<I1, Proj1>, projected<I2, Proj2>>
  constexpr ranges::partial_sort_copy_result<I1, I2>
    ranges::partial_sort_copy(I1 first, S1 last, I2 result_first, S2 result_last,
                              Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, random_access_range R2, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires indirectly_copyable<iterator_t<R1>, iterator_t<R2>> &&
           sortable<iterator_t<R2>, Comp, Proj2> &&
           indirect_strict_weak_order<Comp, projected<iterator_t<R1>, Proj1>,
                                      projected<iterator_t<R2>, Proj2>>
  constexpr ranges::partial_sort_copy_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
    ranges::partial_sort_copy(R1&& r, R2&& result_r, Comp comp = {},
                              Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_copyable<I1, I2> && sortable<I2, Comp, Proj2> &&
            indirect_strict_weak_order<Comp, projected<I1, Proj1>, projected<I2, Proj2>>
  ranges::partial_sort_copy_result<I1, I2>
    ranges::partial_sort_copy(Ep&& exec, I1 first, S1 last, I2 result_first, S2 result_last,
                              Comp comp = {}, Proj1 proj1 = {},
                              Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires indirectly_copyable<iterator_t<R1>, iterator_t<R2>> &&
           sortable<iterator_t<R2>, Comp, Proj2> &&
           indirect_strict_weak_order<Comp, projected<iterator_t<R1>, Proj1>,
                                      projected<iterator_t<R2>, Proj2>>
  ranges::partial_sort_copy_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>>
    ranges::partial_sort_copy(Ep&& exec, R1&& r, R2&& result_r, Comp comp = {},
                              Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let N be \min(`last - first`, \ `result_last - result_first`). Let
`comp` be `less{}`, and `proj1` and `proj2` be `identity{}` for the
overloads with no parameters by those names.

*Mandates:* For the overloads in namespace `std`, the expression
`*first` is writable [[iterator.requirements.general]] to
`result_first`.

*Preconditions:* For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]], the type of `*result_first`
meets the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

For iterators `a1` and `b1` in \[`first`, `last`), and iterators `x2`
and `y2` in \[`result_first`, `result_last`), after evaluating the
assignment `*y2 = *b1`, let E be the value of

``` cpp
bool(invoke(comp, invoke(proj1, *a1), invoke(proj2, *y2))).
```

Then, after evaluating the assignment `*x2 = *a1`, E is equal to

``` cpp
bool(invoke(comp, invoke(proj2, *x2), invoke(proj2, *y2))).
```

[*Note 1*: Writing a value from the input range into the output range
does not affect how it is ordered by `comp` and `proj1` or
`proj2`. — *end note*]

*Effects:* Places the first N elements as sorted with respect to `comp`
and `proj2` into the range \[`result_first`, `result_first + `N).

*Returns:*

- `result_first + `N for the overloads in namespace `std`.
- `{last, result_first + `N`}` for the overloads in namespace `ranges`.

*Complexity:* Approximately `(last - first) * log `N comparisons, and
twice as many projections.

#### `is_sorted` <a id="is.sorted">[[is.sorted]]</a>

``` cpp
template<class ForwardIterator>
  constexpr bool is_sorted(ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to: `return is_sorted_until(first, last) == last;`

``` cpp
template<class ExecutionPolicy, class ForwardIterator>
  bool is_sorted(ExecutionPolicy&& exec,
                 ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
return is_sorted_until(std::forward<ExecutionPolicy>(exec), first, last) == last;
```

``` cpp
template<class ForwardIterator, class Compare>
  constexpr bool is_sorted(ForwardIterator first, ForwardIterator last,
                           Compare comp);
```

*Effects:* Equivalent to:
`return is_sorted_until(first, last, comp) == last;`

``` cpp
template<class ExecutionPolicy, class ForwardIterator, class Compare>
  bool is_sorted(ExecutionPolicy&& exec,
                 ForwardIterator first, ForwardIterator last,
                 Compare comp);
```

*Effects:* Equivalent to:

``` cpp
return is_sorted_until(std::forward<ExecutionPolicy>(exec), first, last, comp) == last;
```

``` cpp
template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr bool ranges::is_sorted(I first, S last, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr bool ranges::is_sorted(R&& r, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:
`return ranges::is_sorted_until(first, last, comp, proj) == last;`

``` cpp
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  bool ranges::is_sorted(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  bool ranges::is_sorted(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::is_sorted_until(std::forward<Ep>(exec), first, last, comp, proj) == last;
```

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator
    is_sorted_until(ForwardIterator first, ForwardIterator last);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator
    is_sorted_until(ExecutionPolicy&& exec,
                    ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class Compare>
  constexpr ForwardIterator
    is_sorted_until(ForwardIterator first, ForwardIterator last,
                    Compare comp);
template<class ExecutionPolicy, class ForwardIterator, class Compare>
  ForwardIterator
    is_sorted_until(ExecutionPolicy&& exec,
                    ForwardIterator first, ForwardIterator last,
                    Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr I ranges::is_sorted_until(I first, S last, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr borrowed_iterator_t<R>
    ranges::is_sorted_until(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  I ranges::is_sorted_until(Ep&& exec, I first, S last, Comp comp = {},
                    Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  borrowed_iterator_t<R>
    ranges::is_sorted_until(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Returns:* The last iterator `i` in \[`first`, `last`\] for which the
range \[`first`, `i`) is sorted with respect to `comp` and `proj`.

*Complexity:* Linear.

### Nth element <a id="alg.nth.element">[[alg.nth.element]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                             RandomAccessIterator last);
template<class ExecutionPolicy, class RandomAccessIterator>
  void nth_element(ExecutionPolicy&& exec,
                   RandomAccessIterator first, RandomAccessIterator nth,
                   RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                             RandomAccessIterator last,  Compare comp);
template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
  void nth_element(ExecutionPolicy&& exec,
                   RandomAccessIterator first, RandomAccessIterator nth,
                   RandomAccessIterator last, Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::nth_element(I first, I nth, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Comp = ranges::less, class Proj = identity>
  requires sortable<I, Comp, Proj>
  I ranges::nth_element(Ep&& exec, I first, I nth, S last, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* \[`first`, `nth`) and \[`nth`, `last`) are valid
ranges. For the overloads in namespace `std`, `RandomAccessIterator`
meets the *Cpp17ValueSwappable* requirements [[swappable.requirements]],
and the type of `*first` meets the *Cpp17MoveConstructible*
([[cpp17.moveconstructible]]) and *Cpp17MoveAssignable*
([[cpp17.moveassignable]]) requirements.

*Effects:* After `nth_element` the element in the position pointed to by
`nth` is the element that would be in that position if the whole range
were sorted with respect to `comp` and `proj`, unless `nth == last`.
Also for every iterator `i` in the range \[`first`, `nth`) and every
iterator `j` in the range \[`nth`, `last`) it holds that:
`bool(invoke(comp, invoke(proj, *j), invoke(proj, *i)))` is `false`.

*Returns:* `last` for the overload in namespace `ranges`.

*Complexity:* For the non-parallel algorithm overloads, linear on
average. For the parallel algorithm overloads, 𝑂(N) applications of the
predicate, and 𝑂(N log N) swaps, where N = `last - first`.

``` cpp
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::nth_element(R&& r, iterator_t<R> nth, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::nth_element(ranges::begin(r), nth, ranges::end(r), comp, proj);
```

``` cpp
template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  borrowed_iterator_t<R>
    ranges::nth_element(Ep&& exec, R&& r, iterator_t<R> nth, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::nth_element(std::forward<Ep>(exec), ranges::begin(r), nth, ranges::end(r),
                           comp, proj);
```

### Binary search <a id="alg.binary.search">[[alg.binary.search]]</a>

#### General <a id="alg.binary.search.general">[[alg.binary.search.general]]</a>

All of the algorithms in [[alg.binary.search]] are versions of binary
search and assume that the sequence being searched is partitioned with
respect to an expression formed by binding the search key to an argument
of the comparison function. They work on non-random access iterators
minimizing the number of comparisons, which will be logarithmic for all
types of iterators. They are especially appropriate for random access
iterators, because these algorithms do a logarithmic number of steps
through the data structure. For non-random access iterators they execute
a linear number of steps.

#### `lower_bound` <a id="lower.bound">[[lower.bound]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr ForwardIterator
    lower_bound(ForwardIterator first, ForwardIterator last,
                const T& value);

template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
         class Compare>
  constexpr ForwardIterator
    lower_bound(ForwardIterator first, ForwardIterator last,
                const T& value, Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>,
         indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
  constexpr I ranges::lower_bound(I first, S last, const T& value, Comp comp = {},
                                  Proj proj = {});
template<forward_range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>,
         indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
           ranges::less>
  constexpr borrowed_iterator_t<R>
    ranges::lower_bound(R&& r, const T& value, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for overloads with no
parameters by those names.

*Preconditions:* The elements `e` of \[`first`, `last`) are partitioned
with respect to the expression  
`bool(invoke(comp, invoke(proj, e), value))`.

*Returns:* The furthermost iterator `i` in the range \[`first`, `last`\]
such that for every iterator `j` in the range \[`first`, `i`),
`bool(invoke(comp, invoke(proj, *j), value))` is `true`.

*Complexity:* At most \log_2(`last - first`) + 𝑂(1) comparisons and
projections.

#### `upper_bound` <a id="upper.bound">[[upper.bound]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr ForwardIterator
    upper_bound(ForwardIterator first, ForwardIterator last,
                const T& value);

template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
         class Compare>
  constexpr ForwardIterator
    upper_bound(ForwardIterator first, ForwardIterator last,
                const T& value, Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>,
         indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
  constexpr I ranges::upper_bound(I first, S last, const T& value, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>,
         indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
           ranges::less>
  constexpr borrowed_iterator_t<R>
    ranges::upper_bound(R&& r, const T& value, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for overloads with no
parameters by those names.

*Preconditions:* The elements `e` of \[`first`, `last`) are partitioned
with respect to the expression  
`!bool(invoke(comp, value, invoke(proj, e)))`.

*Returns:* The furthermost iterator `i` in the range \[`first`, `last`\]
such that for every iterator `j` in the range \[`first`, `i`),
`!bool(invoke(comp, value, invoke(proj, *j)))` is `true`.

*Complexity:* At most \log_2(`last - first`) + 𝑂(1) comparisons and
projections.

#### `equal_range` <a id="equal.range">[[equal.range]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first,
                ForwardIterator last, const T& value);

template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
         class Compare>
  constexpr pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first,
                ForwardIterator last, const T& value,
                Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>,
         indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
  constexpr subrange<I>
    ranges::equal_range(I first, S last, const T& value, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>,
         indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
           ranges::less>
  constexpr borrowed_subrange_t<R>
    ranges::equal_range(R&& r, const T& value, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for overloads with no
parameters by those names.

*Preconditions:* The elements `e` of \[`first`, `last`) are partitioned
with respect to the expressions
`bool(invoke(comp, invoke(proj, e), value))` and
`!bool(invoke(comp, value, invoke(proj, e)))`. Also, for all elements
`e` of \[`first`, `last`), `bool(comp(e, value))` implies
`!bool(comp(value, e))` for the overloads in namespace `std`.

*Returns:*

- For the overloads in namespace `std`:
  ``` cpp
  {lower_bound(first, last, value, comp),
   upper_bound(first, last, value, comp)}
  ```
- For the overloads in namespace `ranges`:
  ``` cpp
  {ranges::lower_bound(first, last, value, comp, proj),
   ranges::upper_bound(first, last, value, comp, proj)}
  ```

*Complexity:* At most 2 * \log_2(`last - first`) + 𝑂(1) comparisons and
projections.

#### `binary_search` <a id="binary.search">[[binary.search]]</a>

``` cpp
template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type>
  constexpr bool
    binary_search(ForwardIterator first, ForwardIterator last,
                  const T& value);

template<class ForwardIterator, class T = iterator_traits<ForwardIterator>::value_type,
         class Compare>
  constexpr bool
    binary_search(ForwardIterator first, ForwardIterator last,
                  const T& value, Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         class T = projected_value_t<I, Proj>,
         indirect_strict_weak_order<const T*, projected<I, Proj>> Comp = ranges::less>
  constexpr bool ranges::binary_search(I first, S last, const T& value, Comp comp = {},
                                       Proj proj = {});
template<forward_range R, class Proj = identity,
         class T = projected_value_t<iterator_t<R>, Proj>,
         indirect_strict_weak_order<const T*, projected<iterator_t<R>, Proj>> Comp =
           ranges::less>
  constexpr bool ranges::binary_search(R&& r, const T& value, Comp comp = {},
                                       Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for overloads with no
parameters by those names.

*Preconditions:* The elements `e` of \[`first`, `last`) are partitioned
with respect to the expressions
`bool(invoke(comp, invoke(proj, e), value))` and
`!bool(invoke(comp, value, invoke(proj, e)))`. Also, for all elements
`e` of \[`first`, `last`), `bool(comp(e, value))` implies
`!bool(comp(value, e))` for the overloads in namespace `std`.

*Returns:* `true` if and only if for some iterator `i` in the range
\[`first`, `last`),
`!bool(invoke(comp, invoke(proj, *i), value)) && !bool(invoke(comp, value, invoke(proj, *i)))`
is `true`.

*Complexity:* At most \log_2(`last - first`) + 𝑂(1) comparisons and
projections.

### Partitions <a id="alg.partitions">[[alg.partitions]]</a>

``` cpp
template<class InputIterator, class Predicate>
  constexpr bool is_partitioned(InputIterator first, InputIterator last, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  bool is_partitioned(ExecutionPolicy&& exec,
                      ForwardIterator first, ForwardIterator last, Predicate pred);

template<input_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr bool ranges::is_partitioned(I first, S last, Pred pred, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr bool ranges::is_partitioned(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  bool ranges::is_partitioned(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  bool ranges::is_partitioned(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let `proj` be `identity{}` for the overloads with no parameter named
`proj`.

*Returns:* `true` if and only if the elements `e` of \[`first`, `last`)
are partitioned with respect to the expression
`bool(invoke(pred, invoke(proj, e)))`.

*Complexity:* Linear. At most `last - first` applications of `pred` and
`proj`.

``` cpp
template<class ForwardIterator, class Predicate>
  constexpr ForwardIterator
    partition(ForwardIterator first, ForwardIterator last, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class Predicate>
  ForwardIterator
    partition(ExecutionPolicy&& exec, ForwardIterator first, ForwardIterator last, Predicate pred);

template<permutable I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr subrange<I>
    ranges::partition(I first, S last, Pred pred, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R>
    ranges::partition(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  subrange<I> ranges::partition(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R> ranges::partition(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let `proj` be `identity{}` for the overloads with no parameter named
`proj` and let E(x) be `bool(invoke(pred, invoke(proj, `x`)))`.

*Preconditions:* For the overloads in namespace `std`, `ForwardIterator`
meets the *Cpp17ValueSwappable* requirements [[swappable.requirements]].

*Effects:* Places all the elements `e` in \[`first`, `last`) that
satisfy E(`e`) before all the elements that do not.

*Returns:* Let `i` be an iterator such that E(`*j`) is `true` for every
iterator `j` in \[`first`, `i`) and `false` for every iterator `j` in
\[`i`, `last`). Returns:

- `i` for the overloads in namespace `std`.
- `{i, last}` for the overloads in namespace `ranges`.

*Complexity:* Let N = `last - first`:

- For the non-parallel algorithm overloads, exactly N applications of
  the predicate and projection. At most N / 2 swaps if the type of
  `first` meets the *Cpp17BidirectionalIterator* requirements for the
  overloads in namespace `std` or models `bidirectional_iterator` for
  the overloads in namespace `ranges`, and at most N swaps otherwise.
- For the parallel algorithm overloads, 𝑂(N log N) swaps and 𝑂(N)
  applications of the predicate.

``` cpp
template<class BidirectionalIterator, class Predicate>
  BidirectionalIterator
    constexpr stable_partition(BidirectionalIterator first, BidirectionalIterator last,
                               Predicate pred);
template<class ExecutionPolicy, class BidirectionalIterator, class Predicate>
  BidirectionalIterator
    stable_partition(ExecutionPolicy&& exec,
                     BidirectionalIterator first, BidirectionalIterator last, Predicate pred);

template<bidirectional_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  requires permutable<I>
  constexpr subrange<I> ranges::stable_partition(I first, S last, Pred pred, Proj proj = {});
template<bidirectional_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires permutable<iterator_t<R>>
  constexpr borrowed_subrange_t<R> ranges::stable_partition(R&& r, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires permutable<I>
  subrange<I>
    ranges::stable_partition(Ep&& exec, I first, S last, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires permutable<iterator_t<R>>
  borrowed_subrange_t<R>
    ranges::stable_partition(Ep&& exec, R&& r, Pred pred, Proj proj = {});
```

Let `proj` be `identity{}` for the overloads with no parameter named
`proj` and let E(x) be `bool(invoke(pred, invoke(proj, `x`)))`.

*Preconditions:* For the overloads in namespace `std`,
`BidirectionalIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Places all the elements `e` in \[`first`, `last`) that
satisfy E(`e`) before all the elements that do not. The relative order
of the elements in both groups is preserved.

*Returns:* Let `i` be an iterator such that for every iterator `j` in
\[`first`, `i`), E(`*j`) is `true`, and for every iterator `j` in the
range \[`i`, `last`), E(`*j`) is `false`. Returns:

- `i` for the overloads in namespace `std`.
- `{i, last}` for the overloads in namespace `ranges`.

*Complexity:* Let N = `last - first`:

- For the non-parallel algorithm overloads, at most N log₂ N swaps, but
  only 𝑂(N) swaps if there is enough extra memory. Exactly N
  applications of the predicate and projection.
- For the parallel algorithm overloads, 𝑂(N log N) swaps and 𝑂(N)
  applications of the predicate.

``` cpp
template<class InputIterator, class OutputIterator1, class OutputIterator2, class Predicate>
  constexpr pair<OutputIterator1, OutputIterator2>
    partition_copy(InputIterator first, InputIterator last,
                   OutputIterator1 out_true, OutputIterator2 out_false, Predicate pred);
template<class ExecutionPolicy, class ForwardIterator, class ForwardIterator1,
         class ForwardIterator2, class Predicate>
  pair<ForwardIterator1, ForwardIterator2>
    partition_copy(ExecutionPolicy&& exec,
                   ForwardIterator first, ForwardIterator last,
                   ForwardIterator1 out_true, ForwardIterator2 out_false, Predicate pred);

template<input_iterator I, sentinel_for<I> S, weakly_incrementable O1, weakly_incrementable O2,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O1> && indirectly_copyable<I, O2>
  constexpr ranges::partition_copy_result<I, O1, O2>
    ranges::partition_copy(I first, S last, O1 out_true, O2 out_false, Pred pred,
                           Proj proj = {});
template<input_range R, weakly_incrementable O1, weakly_incrementable O2,
         class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, O1> &&
           indirectly_copyable<iterator_t<R>, O2>
  constexpr ranges::partition_copy_result<borrowed_iterator_t<R>, O1, O2>
    ranges::partition_copy(R&& r, O1 out_true, O2 out_false, Pred pred, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         random_access_iterator O1, sized_sentinel_for<O1> OutS1,
         random_access_iterator O2, sized_sentinel_for<O2> OutS2,
         class Proj = identity, indirect_unary_predicate<projected<I, Proj>> Pred>
  requires indirectly_copyable<I, O1> && indirectly_copyable<I, O2>
  ranges::partition_copy_result<I, O1, O2>
    ranges::partition_copy(Ep&& exec, I first, S last, O1 out_true, OutS1 last_true,
                           O2 out_false, OutS2 last_false, Pred pred, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R,
         sized-random-access-range OutR1, sized-random-access-range OutR2,
         class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  requires indirectly_copyable<iterator_t<R>, iterator_t<OutR1>> &&
            indirectly_copyable<iterator_t<R>, iterator_t<OutR2>>
  ranges::partition_copy_result<borrowed_iterator_t<R>, borrowed_iterator_t<OutR1>,
                                borrowed_iterator_t<OutR2>>
    ranges::partition_copy(Ep&& exec, R&& r, OutR1&& out_true_r, OutR2&& out_false_r,
                           Pred pred, Proj proj = {});
```

Let `proj` be `identity{}` for the overloads with no parameter named
`proj` and let E(x) be `bool(invoke(pred, invoke(proj, `x`)))`.

For the overloads with no parameters `last_true`, `last_false`,
`out_true_r`, or `out_false_r`, let

- M be the number of iterators `i` in \[`first`, `last`) for which
  E(`*i`) is `true`, and K be `last - first - `M;
- `last_true` be `out_true + `M, and `last_false` be `out_false + `K.

For the overloads with parameters `last_true`, `last_false`,
`out_true_r`, or `out_false_r`, let M be `last_true - out_true` and K be
`last_false - out_false`.

Let:

- `i1` be the iterator in \[`first`, `last`) for which E(`*i1`) is
  `true` and there are exactly M iterators `j` in \[`first`, `i1`) for
  which E(`*j`) is `true`, or `last` if no such iterator exists;
- `i2` be the iterator in \[`first`, `last`) for which E(`*i2`) is
  `false` and there are exactly K iterators `j` in \[`first`, `i2`) for
  which E(`*j`) is `false`, or `last` if no such iterator exists;
- N be \min(`i1 - first`, \ `i2 - first`).

*Mandates:* For the overloads in namespace `std`, the expression
`*first` is writable [[iterator.requirements.general]] to `out_true` and
`out_false`.

*Preconditions:* The input range and output ranges do not overlap.

[*Note 1*: For the parallel algorithm overload in namespace `std`,
there can be a performance cost if `first`’s value type does not meet
the *Cpp17CopyConstructible* requirements. For the parallel algorithm
overloads in namespace `ranges`, there can be a performance cost if
`first`’s value type does not model `copy_constructible`. — *end note*]

*Effects:* For each iterator `i` in \[`first`, `first + `N), copies `*i`
to the output range \[`out_true`, `last_true`) if E(`*i`) is `true`, or
to the output range \[`out_false`, `last_false`) otherwise.

*Returns:* Let `o1` be the iterator past the last copied element in the
output range \[`out_true`, `last_true`), and `o2` be the iterator past
the last copied element in the output range \[`out_false`,
`last_false`). Returns:

- `{o1, o2}` for the overloads in namespace `std`.
- `{first + `N`, o1, o2}` for the overloads in namespace `ranges`.

*Complexity:* At most `last - first` applications of `pred` and `proj`.

``` cpp
template<class ForwardIterator, class Predicate>
  constexpr ForwardIterator
    partition_point(ForwardIterator first, ForwardIterator last, Predicate pred);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_unary_predicate<projected<I, Proj>> Pred>
  constexpr I ranges::partition_point(I first, S last, Pred pred, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_unary_predicate<projected<iterator_t<R>, Proj>> Pred>
  constexpr borrowed_iterator_t<R>
    ranges::partition_point(R&& r, Pred pred, Proj proj = {});
```

Let `proj` be `identity{}` for the overloads with no parameter named
`proj` and let E(x) be `bool(invoke(pred, invoke(proj, `x`)))`.

*Preconditions:* The elements `e` of \[`first`, `last`) are partitioned
with respect to E(`e`).

*Returns:* An iterator `mid` such that E(`*i`) is `true` for all
iterators `i` in \[`first`, `mid`), and `false` for all iterators `i` in
\[`mid`, `last`).

*Complexity:* 𝑂(log(`last - first`)) applications of `pred` and `proj`.

### Merge <a id="alg.merge">[[alg.merge]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  constexpr OutputIterator
    merge(InputIterator1 first1, InputIterator1 last1,
          InputIterator2 first2, InputIterator2 last2,
          OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator>
  ForwardIterator
    merge(ExecutionPolicy&& exec,
          ForwardIterator1 first1, ForwardIterator1 last1,
          ForwardIterator2 first2, ForwardIterator2 last2,
          ForwardIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  constexpr OutputIterator
    merge(InputIterator1 first1, InputIterator1 last1,
          InputIterator2 first2, InputIterator2 last2,
          OutputIterator result, Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator, class Compare>
  ForwardIterator
    merge(ExecutionPolicy&& exec,
          ForwardIterator1 first1, ForwardIterator1 last1,
          ForwardIterator2 first2, ForwardIterator2 last2,
          ForwardIterator result, Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         weakly_incrementable O, class Comp = ranges::less, class Proj1 = identity,
         class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  constexpr ranges::merge_result<I1, I2, O>
    ranges::merge(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                  Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, weakly_incrementable O, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
  constexpr ranges::merge_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
    ranges::merge(R1&& r1, R2&& r2, O result,
                  Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  ranges::merge_result<I1, I2, O>
    ranges::merge(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2, O result, OutS result_last,
                  Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         sized-random-access-range OutR, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
  ranges::merge_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, borrowed_iterator_t<OutR>>
    ranges::merge(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r,
                  Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- N be:
  - `(last1 - first1) + (last2 - first2)` for the overloads with no
    parameter `result_last` or `result_r`;
  - \min(`(last1 - first1) + (last2 - first2)`, \ `result_last - result`)
    for the overloads with parameters `result_last` or `result_r`;
- `comp` be `less{}`, `proj1` be `identity{}`, and `proj2` be
  `identity{}`, for the overloads with no parameters by those names;
- E(`e1`, `e1`) be
  `bool(invoke(comp, invoke(proj2, e2), invoke(proj1, e1)))`;
- K be the smallest integer in \[`0`, `last1 - first1`) such that for
  the element `e1` in the position `first1 + `K there are at least N - K
  elements `e2` in \[`first2`, `last2`) for which E(`e1`, `e1`) holds,
  and be equal to `last1 - first1` if no such integer exists.
  \[*Note 2*: `first1 + `K points to the position past the last element
  to be copied. — *end note*]

*Preconditions:* The ranges \[`first1`, `last1`) and \[`first2`,
`last2`) are sorted with respect to `comp` and `proj1` or `proj2`,
respectively. The resulting range does not overlap with either of the
original ranges.

*Effects:* Copies the first K elements of the range \[`first1`, `last1`)
and the first N - K elements of the range \[`first2`, `last2`) into the
range \[`result`, `result + `N). If an element `a` precedes `b` in an
input range, `a` is copied into the output range before `b`. If `e1` is
an element of \[`first1`, `last1`) and `e2` of \[`first2`, `last2`),
`e2` is copied into the output range before `e1` if and only if
E(`e1`, `e1`) is `true`.

*Returns:*

- `result + `N for the overloads in namespace `std`.
- `{first1 + `K`, first2 + `N` - `K`, result + `N`}` for the overloads
  in namespace `ranges`.

*Complexity:*

- For the non-parallel algorithm overloads, at most N - 1 comparisons
  and applications of each projection.
- For the parallel algorithm overloads, 𝑂(N) comparisons and
  applications of each projection.

*Remarks:* Stable [[algorithm.stable]].

``` cpp
template<class BidirectionalIterator>
  constexpr void inplace_merge(BidirectionalIterator first,
                               BidirectionalIterator middle,
                               BidirectionalIterator last);
template<class ExecutionPolicy, class BidirectionalIterator>
  void inplace_merge(ExecutionPolicy&& exec,
                     BidirectionalIterator first,
                     BidirectionalIterator middle,
                     BidirectionalIterator last);

template<class BidirectionalIterator, class Compare>
  constexpr void inplace_merge(BidirectionalIterator first,
                               BidirectionalIterator middle,
                               BidirectionalIterator last, Compare comp);
template<class ExecutionPolicy, class BidirectionalIterator, class Compare>
  void inplace_merge(ExecutionPolicy&& exec,
                     BidirectionalIterator first,
                     BidirectionalIterator middle,
                     BidirectionalIterator last, Compare comp);

template<bidirectional_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I ranges::inplace_merge(I first, I middle, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Comp = ranges::less, class Proj = identity>
  requires sortable<I, Comp, Proj>
  I ranges::inplace_merge(Ep&& exec, I first, I middle, S last, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* \[`first`, `middle`) and \[`middle`, `last`) are valid
ranges sorted with respect to `comp` and `proj`. For the overloads in
namespace `std`, `BidirectionalIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Merges two sorted consecutive ranges \[`first`, `middle`) and
\[`middle`, `last`), putting the result of the merge into the range
\[`first`, `last`). The resulting range is sorted with respect to `comp`
and `proj`.

*Returns:* `last` for the overload in namespace `ranges`.

*Complexity:* Let N = `last - first`:

- For the non-parallel algorithm overloads, and if enough additional
  memory is available, at most N - 1 comparisons.
- Otherwise, 𝑂(N log N) comparisons.

In either case, twice as many projections as comparisons.

*Remarks:* Stable [[algorithm.stable]].

``` cpp
template<bidirectional_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::inplace_merge(R&& r, iterator_t<R> middle, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::inplace_merge(ranges::begin(r), middle, ranges::end(r), comp, proj);
```

``` cpp
template<execution-policy Ep, sized-random-access-range R, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  borrowed_iterator_t<R>
    ranges::inplace_merge(Ep&& exec, R&& r, iterator_t<R> middle, Comp comp = {},
                          Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::inplace_merge(std::forward<Ep>(exec), ranges::begin(r), middle,
                             ranges::end(r), comp, proj);
```

### Set operations on sorted structures <a id="alg.set.operations">[[alg.set.operations]]</a>

#### General <a id="alg.set.operations.general">[[alg.set.operations.general]]</a>

Subclause [[alg.set.operations]] defines all the basic set operations on
sorted structures. They also work with `multiset`s [[multiset]]
containing multiple copies of equivalent elements. The semantics of the
set operations are generalized to `multiset`s in a standard way by
defining `set_union` to contain the maximum number of occurrences of
every element, `set_intersection` to contain the minimum, and so on.

#### `includes` <a id="includes">[[includes]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  constexpr bool includes(InputIterator1 first1, InputIterator1 last1,
                          InputIterator2 first2, InputIterator2 last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  bool includes(ExecutionPolicy&& exec,
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2, ForwardIterator2 last2);

template<class InputIterator1, class InputIterator2, class Compare>
  constexpr bool includes(InputIterator1 first1, InputIterator1 last1,
                          InputIterator2 first2, InputIterator2 last2,
                          Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class Compare>
  bool includes(ExecutionPolicy&& exec,
                ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2, ForwardIterator2 last2,
                Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_strict_weak_order<projected<I1, Proj1>,
                                    projected<I2, Proj2>> Comp = ranges::less>
  constexpr bool ranges::includes(I1 first1, S1 last1, I2 first2, S2 last2, Comp comp = {},
                                  Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, class Proj1 = identity,
         class Proj2 = identity,
         indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                    projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
  constexpr bool ranges::includes(R1&& r1, R2&& r2, Comp comp = {},
                                  Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_strict_weak_order<projected<I1, Proj1>, projected<I2, Proj2>> Comp =
           ranges::less>
  bool ranges::includes(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                        Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                     projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
  bool ranges::includes(Ep&& exec, R1&& r1, R2&& r2,
                        Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let `comp` be `less{}`, `proj1` be `identity{}`, and `proj2` be
`identity{}`, for the overloads with no parameters by those names.

*Preconditions:* The ranges \[`first1`, `last1`) and \[`first2`,
`last2`) are sorted with respect to `comp` and `proj1` or `proj2`,
respectively.

*Returns:* `true` if and only if \[`first2`, `last2`) is a subsequence
of \[`first1`, `last1`).

[*Note 1*: A sequence S is a subsequence of another sequence T if S can
be obtained from T by removing some, all, or none of T’s elements and
keeping the remaining elements in the same order. — *end note*]

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons and applications of each projection.

#### `set_union` <a id="set.union">[[set.union]]</a>

``` cpp
template<class InputIterator1, class InputIterator2, class OutputIterator>
  constexpr OutputIterator
    set_union(InputIterator1 first1, InputIterator1 last1,
              InputIterator2 first2, InputIterator2 last2,
              OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator>
  ForwardIterator
    set_union(ExecutionPolicy&& exec,
              ForwardIterator1 first1, ForwardIterator1 last1,
              ForwardIterator2 first2, ForwardIterator2 last2,
              ForwardIterator result);

template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
  constexpr OutputIterator
    set_union(InputIterator1 first1, InputIterator1 last1,
              InputIterator2 first2, InputIterator2 last2,
              OutputIterator result, Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator, class Compare>
  ForwardIterator
    set_union(ExecutionPolicy&& exec,
              ForwardIterator1 first1, ForwardIterator1 last1,
              ForwardIterator2 first2, ForwardIterator2 last2,
              ForwardIterator result, Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         weakly_incrementable O, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  constexpr ranges::set_union_result<I1, I2, O>
    ranges::set_union(I1 first1, S1 last1, I2 first2, S2 last2, O result, Comp comp = {},
                      Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, weakly_incrementable O,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
  constexpr ranges::set_union_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
    ranges::set_union(R1&& r1, R2&& r2, O result, Comp comp = {},
                      Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  ranges::set_union_result<I1, I2, O>
    ranges::set_union(Ep&& exec, I1 first1, S1 last1,
                      I2 first2, S2 last2, O result, OutS result_last,
                      Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         sized-random-access-range OutR, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
  ranges::set_union_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                           borrowed_iterator_t<OutR>>
    ranges::set_union(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                      Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `comp` be `less{}`, and `proj1` and `proj2` be `identity{}` for the
  overloads with no parameters by those names;
- M be `last1 - first1` plus the number of elements in \[`first2`,
  `last2`) that are not present in \[`first1`, `last1`);
- `result_last` be `result + `M for the overloads with no parameter
  `result_last` or `result_r`;
- N be \min(M, \ `result_last - result`).

*Preconditions:* The ranges \[`first1`, `last1`) and \[`first2`,
`last2`) are sorted with respect to `comp` and `proj1` or `proj2`,
respectively. The resulting range does not overlap with either of the
original ranges.

*Effects:* Constructs a sorted union of N elements from the two ranges;
that is, the set of elements that are present in one or both of the
ranges.

*Returns:*

- `result_last` for the overloads in namespace `std`.
- `{last1, last2, result + `N`}` for the overloads in namespace
  `ranges`, if N is equal to M.
- Otherwise, `{j1, j2, result_last}` for the overloads in namespace
  `ranges`, where the iterators `j1` and `j2` point to positions past
  the last copied or skipped elements in \[`first1`, `last1`) and
  \[`first2`, `last2`), respectively.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons and applications of each projection.

*Remarks:* Stable [[algorithm.stable]]. If \[`first1`, `last1`) contains
m elements that are equivalent to each other and \[`first2`, `last2`)
contains n elements that are equivalent to them, then all m elements
from the first range are copied to the output range, in order, and then
the final max(n - m, 0) elements from the second range are copied to the
output range, in order.

#### `set_intersection` <a id="set.intersection">[[set.intersection]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  constexpr OutputIterator
    set_intersection(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2, InputIterator2 last2,
                     OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator>
  ForwardIterator
    set_intersection(ExecutionPolicy&& exec,
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2, ForwardIterator2 last2,
                     ForwardIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  constexpr OutputIterator
    set_intersection(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2, InputIterator2 last2,
                     OutputIterator result, Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator, class Compare>
  ForwardIterator
    set_intersection(ExecutionPolicy&& exec,
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2, ForwardIterator2 last2,
                     ForwardIterator result, Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         weakly_incrementable O, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  constexpr ranges::set_intersection_result<I1, I2, O>
    ranges::set_intersection(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                             Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, weakly_incrementable O,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
  constexpr ranges::set_intersection_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>, O>
    ranges::set_intersection(R1&& r1, R2&& r2, O result,
                             Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  ranges::set_intersection_result<I1, I2, O>
    ranges::set_intersection(Ep&& exec, I1 first1, S1 last1,
                      I2 first2, S2 last2, O result, OutS result_last,
                      Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         sized-random-access-range OutR, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
  ranges::set_intersection_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                                  borrowed_iterator_t<OutR>>
    ranges::set_intersection(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                             Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `comp` be `less{}`, and `proj1` and `proj2` be `identity{}` for the
  overloads with no parameters by those names;
- M be the number of elements in \[`first1`, `last1`) that are present
  in \[`first2`, `last2`);
- `result_last` be `result + `M for the overloads with no parameter
  `result_last` or `result_r`;
- N be \min(M, \ `result_last - result`).

*Preconditions:* The ranges \[`first1`, `last1`) and \[`first2`,
`last2`) are sorted with respect to `comp` and `proj1` or `proj2`,
respectively. The resulting range does not overlap with either of the
original ranges.

*Effects:* Constructs a sorted intersection of N elements from the two
ranges; that is, the set of elements that are present in both of the
ranges.

*Returns:*

- `result_last` for the overloads in namespace `std`.
- `{last1, last2, result + `N`}` for the overloads in namespace
  `ranges`, if N is equal to M.
- Otherwise, `{j1, j2, result_last}` for the overloads in namespace
  `ranges`, where the iterators `j1` and `j2` point to positions past
  the last copied or skipped elements in \[`first1`, `last1`) and
  \[`first2`, `last2`), respectively.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons and applications of each projection.

*Remarks:* Stable [[algorithm.stable]]. If \[`first1`, `last1`) contains
m elements that are equivalent to each other and \[`first2`, `last2`)
contains n elements that are equivalent to them, the first min(m, n)
elements are copied from the first range to the output range, in order.

#### `set_difference` <a id="set.difference">[[set.difference]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  constexpr OutputIterator
    set_difference(InputIterator1 first1, InputIterator1 last1,
                   InputIterator2 first2, InputIterator2 last2,
                   OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator>
  ForwardIterator
    set_difference(ExecutionPolicy&& exec,
                   ForwardIterator1 first1, ForwardIterator1 last1,
                   ForwardIterator2 first2, ForwardIterator2 last2,
                   ForwardIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  constexpr OutputIterator
    set_difference(InputIterator1 first1, InputIterator1 last1,
                   InputIterator2 first2, InputIterator2 last2,
                   OutputIterator result, Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator, class Compare>
  ForwardIterator
    set_difference(ExecutionPolicy&& exec,
                   ForwardIterator1 first1, ForwardIterator1 last1,
                   ForwardIterator2 first2, ForwardIterator2 last2,
                   ForwardIterator result, Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         weakly_incrementable O, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  constexpr ranges::set_difference_result<I1, O>
    ranges::set_difference(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                           Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, weakly_incrementable O,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
  constexpr ranges::set_difference_result<borrowed_iterator_t<R1>, O>
    ranges::set_difference(R1&& r1, R2&& r2, O result,
                           Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  ranges::set_difference_result<I1, O>
    ranges::set_difference(Ep&& exec, I1 first1, S1 last1,
                           I2 first2, S2 last2, O result, OutS result_last,
                           Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         sized-random-access-range OutR, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
  ranges::set_difference_result<borrowed_iterator_t<R1>, borrowed_iterator_t<OutR>>
    ranges::set_difference(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r, Comp comp = {},
                           Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `comp` be `less{}`, and `proj1` and `proj2` be `identity{}` for the
  overloads with no parameters by those names;
- M be the number of elements in \[`first1`, `last1`) that are not
  present in \[`first2`, `last2`);
- `result_last` be `result + `M for the overloads with no parameter
  `result_last` or `result_r`;
- N be \min(M, \ `result_last - result`).

*Preconditions:* The ranges \[`first1`, `last1`) and \[`first2`,
`last2`) are sorted with respect to `comp` and `proj1` or `proj2`,
respectively. The resulting range does not overlap with either of the
original ranges.

*Effects:* Copies N elements of the range \[`first1`, `last1`) which are
not present in the range \[`first2`, `last2`) to the range \[`result`,
`result + `N). The elements in the constructed range are sorted.

*Returns:*

- `result_last` for the overloads in namespace `std`.
- `{last1, result + `N`}` for the overloads in namespace `ranges`, if N
  is equal to M.
- Otherwise, `{j1, result_last}` for the overloads in namespace
  `ranges`, where the iterator `j1` points to the position past the last
  copied or skipped element in \[`first1`, `last1`).

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons and applications of each projection.

*Remarks:* If \[`first1`, `last1`) contains m elements that are
equivalent to each other and \[`first2`, `last2`) contains n elements
that are equivalent to them, the last max(m - n, 0) elements from
\[`first1`, `last1`) are copied to the output range, in order.

#### `set_symmetric_difference` <a id="set.symmetric.difference">[[set.symmetric.difference]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  constexpr OutputIterator
    set_symmetric_difference(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, InputIterator2 last2,
                             OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator>
  ForwardIterator
    set_symmetric_difference(ExecutionPolicy&& exec,
                             ForwardIterator1 first1, ForwardIterator1 last1,
                             ForwardIterator2 first2, ForwardIterator2 last2,
                             ForwardIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  constexpr OutputIterator
    set_symmetric_difference(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, InputIterator2 last2,
                             OutputIterator result, Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class ForwardIterator, class Compare>
  ForwardIterator
    set_symmetric_difference(ExecutionPolicy&& exec,
                             ForwardIterator1 first1, ForwardIterator1 last1,
                             ForwardIterator2 first2, ForwardIterator2 last2,
                             ForwardIterator result, Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         weakly_incrementable O, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  constexpr ranges::set_symmetric_difference_result<I1, I2, O>
    ranges::set_symmetric_difference(I1 first1, S1 last1, I2 first2, S2 last2, O result,
                                     Comp comp = {}, Proj1 proj1 = {},
                                     Proj2 proj2 = {});
template<input_range R1, input_range R2, weakly_incrementable O,
         class Comp = ranges::less, class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, O, Comp, Proj1, Proj2>
  constexpr ranges::set_symmetric_difference_result<borrowed_iterator_t<R1>,
                                                    borrowed_iterator_t<R2>, O>
    ranges::set_symmetric_difference(R1&& r1, R2&& r2, O result, Comp comp = {},
                                     Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         random_access_iterator O, sized_sentinel_for<O> OutS, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<I1, I2, O, Comp, Proj1, Proj2>
  ranges::set_symmetric_difference_result<I1, I2, O>
    ranges::set_symmetric_difference(Ep&& exec, I1 first1, S1 last1,
                                     I2 first2, S2 last2, O result, OutS result_last,
                                     Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         sized-random-access-range OutR, class Comp = ranges::less,
         class Proj1 = identity, class Proj2 = identity>
  requires mergeable<iterator_t<R1>, iterator_t<R2>, iterator_t<OutR>, Comp, Proj1, Proj2>
  ranges::set_symmetric_difference_result<borrowed_iterator_t<R1>, borrowed_iterator_t<R2>,
                                  borrowed_iterator_t<OutR>>
    ranges::set_symmetric_difference(Ep&& exec, R1&& r1, R2&& r2, OutR&& result_r,
                                     Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
```

Let:

- `comp` be `less{}`, and `proj1` and `proj2` be `identity{}` for the
  overloads with no parameters by those names;
- K be the number of elements in \[`first1`, `last1`) that are not
  present in \[`first2`, `last2`).
- M be the number of elements in \[`first2`, `last2`) that are not
  present in \[`first1`, `last1`).
- `result_last` be `result + `M` + `K for the overloads with no
  parameter `result_last` or `result_r`;
- N be \min(K + M, \ `result_last - result`).

*Preconditions:* The ranges \[`first1`, `last1`) and \[`first2`,
`last2`) are sorted with respect to `comp` and `proj1` or `proj2`,
respectively. The resulting range does not overlap with either of the
original ranges.

*Effects:* Copies the elements of the range \[`first1`, `last1`) that
are not present in the range \[`first2`, `last2`), and the elements of
the range \[`first2`, `last2`) that are not present in the range
\[`first1`, `last1`) to the range \[`result`, `result + `N). The
elements in the constructed range are sorted.

*Returns:*

- `result_last` for the overloads in namespace `std`.
- `{last1, last2, result + `N`}` for the overloads in namespace
  `ranges`, if N is equal to M + K.
- Otherwise, `{j1, j2, result_last}` for the overloads in namespace
  `ranges`, where the iterators `j1` and `j2` point to positions past
  the last copied or skipped elements in \[`first1`, `last1`) and
  \[`first2`, `last2`), respectively.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons and applications of each projection.

*Remarks:* Stable [[algorithm.stable]]. If \[`first1`, `last1`) contains
m elements that are equivalent to each other and \[`first2`, `last2`)
contains n elements that are equivalent to them, then |m - n| of those
elements shall be copied to the output range: the last m - n of these
elements from \[`first1`, `last1`) if m > n, and the last n - m of these
elements from \[`first2`, `last2`) if m < n. In either case, the
elements are copied in order.

### Heap operations <a id="alg.heap.operations">[[alg.heap.operations]]</a>

#### General <a id="alg.heap.operations.general">[[alg.heap.operations.general]]</a>

A random access range \[`a`, `b`) is a
*heap with respect to `comp` and `proj`* heap with respect to comp and
proj@heap with respect to `comp` and `proj` for a comparator and
projection `comp` and `proj` if its elements are organized such that:

- With `N = b - a`, for all i, 0 < i < N,
  `bool(invoke(comp, invoke(proj, a[\left \lfloor{\frac{i - 1}{2}}\right \rfloor]), invoke({}proj, a[i])))`
  is `false`.
- `*a` may be removed by `pop_heap`, or a new element added by
  `push_heap`, in time.

These properties make heaps useful as priority queues.

`make_heap` converts a range into a heap and `sort_heap` turns a heap
into a sorted sequence.

#### `push_heap` <a id="push.heap">[[push.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void push_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void push_heap(RandomAccessIterator first, RandomAccessIterator last,
                           Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::push_heap(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::push_heap(R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* The range \[`first`, `last - 1`) is a valid heap with
respect to `comp` and `proj`. For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* requirements ([[cpp17.moveconstructible]])
and the *Cpp17MoveAssignable* requirements ([[cpp17.moveassignable]]).

*Effects:* Places the value in the location `last - 1` into the
resulting heap \[`first`, `last`).

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* At most \log(`last - first`) comparisons and twice as many
projections.

#### `pop_heap` <a id="pop.heap">[[pop.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void pop_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void pop_heap(RandomAccessIterator first, RandomAccessIterator last,
                          Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::pop_heap(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::pop_heap(R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* The range \[`first`, `last`) is a valid non-empty heap
with respect to `comp` and `proj`. For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Swaps the value in the location `first` with the value in the
location `last - 1` and makes \[`first`, `last - 1`) into a heap with
respect to `comp` and `proj`.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* At most 2 \log(`last - first`) comparisons and twice as
many projections.

#### `make_heap` <a id="make.heap">[[make.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void make_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void make_heap(RandomAccessIterator first, RandomAccessIterator last,
                           Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::make_heap(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::make_heap(R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Constructs a heap with respect to `comp` and `proj` out of
the range \[`first`, `last`).

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* At most 3(`last - first`) comparisons and twice as many
projections.

#### `sort_heap` <a id="sort.heap">[[sort.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr void sort_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr void sort_heap(RandomAccessIterator first, RandomAccessIterator last,
                           Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr I
    ranges::sort_heap(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Comp = ranges::less, class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr borrowed_iterator_t<R>
    ranges::sort_heap(R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Preconditions:* The range \[`first`, `last`) is a valid heap with
respect to `comp` and `proj`. For the overloads in namespace `std`,
`RandomAccessIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]] and the type of `*first` meets
the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]]) and
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.

*Effects:* Sorts elements in the heap \[`first`, `last`) with respect to
`comp` and `proj`.

*Returns:* `last` for the overloads in namespace `ranges`.

*Complexity:* At most 2N log N comparisons, where N = `last - first`,
and twice as many projections.

#### `is_heap` <a id="is.heap">[[is.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  constexpr bool is_heap(RandomAccessIterator first, RandomAccessIterator last);
```

*Effects:* Equivalent to: `return is_heap_until(first, last) == last;`

``` cpp
template<class ExecutionPolicy, class RandomAccessIterator>
  bool is_heap(ExecutionPolicy&& exec,
               RandomAccessIterator first, RandomAccessIterator last);
```

*Effects:* Equivalent to:

``` cpp
return is_heap_until(std::forward<ExecutionPolicy>(exec), first, last) == last;
```

``` cpp
template<class RandomAccessIterator, class Compare>
  constexpr bool is_heap(RandomAccessIterator first, RandomAccessIterator last,
                         Compare comp);
```

*Effects:* Equivalent to:
`return is_heap_until(first, last, comp) == last;`

``` cpp
template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
  bool is_heap(ExecutionPolicy&& exec,
               RandomAccessIterator first, RandomAccessIterator last,
               Compare comp);
```

*Effects:* Equivalent to:

``` cpp
return is_heap_until(std::forward<ExecutionPolicy>(exec), first, last, comp) == last;
```

``` cpp
template<random_access_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr bool ranges::is_heap(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr bool ranges::is_heap(R&& r, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:
`return ranges::is_heap_until(first, last, comp, proj) == last;`

``` cpp
template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  bool ranges::is_heap(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  bool ranges::is_heap(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

*Effects:* Equivalent to:

``` cpp
return ranges::is_heap_until(std::forward<Ep>(exec), first, last, comp, proj) == last;
```

``` cpp
template<class RandomAccessIterator>
  constexpr RandomAccessIterator
    is_heap_until(RandomAccessIterator first, RandomAccessIterator last);
template<class ExecutionPolicy, class RandomAccessIterator>
  RandomAccessIterator
    is_heap_until(ExecutionPolicy&& exec,
                  RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  constexpr RandomAccessIterator
    is_heap_until(RandomAccessIterator first, RandomAccessIterator last,
                  Compare comp);
template<class ExecutionPolicy, class RandomAccessIterator, class Compare>
  RandomAccessIterator
    is_heap_until(ExecutionPolicy&& exec,
                  RandomAccessIterator first, RandomAccessIterator last,
                  Compare comp);

template<random_access_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr I ranges::is_heap_until(I first, S last, Comp comp = {}, Proj proj = {});
template<random_access_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr borrowed_iterator_t<R>
    ranges::is_heap_until(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  I ranges::is_heap_until(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  borrowed_iterator_t<R>
    ranges::is_heap_until(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Returns:* The last iterator `i` in \[`first`, `last`\] for which the
range \[`first`, `i`) is a heap with respect to `comp` and `proj`.

*Complexity:* Linear.

### Minimum and maximum <a id="alg.min.max">[[alg.min.max]]</a>

``` cpp
template<class T>
  constexpr const T& min(const T& a, const T& b);
template<class T, class Compare>
  constexpr const T& min(const T& a, const T& b, Compare comp);

template<class T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr const T& ranges::min(const T& a, const T& b, Comp comp = {}, Proj proj = {});
```

*Preconditions:* For the first form, `T` meets the
*Cpp17LessThanComparable* requirements ([[cpp17.lessthancomparable]]).

*Returns:* The smaller value. Returns the first argument when the
arguments are equivalent.

*Complexity:* Exactly one comparison and two applications of the
projection, if any.

*Remarks:* An invocation may explicitly specify an argument for the
template parameter `T` of the overloads in namespace `std`.

``` cpp
template<class T>
  constexpr T min(initializer_list<T> r);
template<class T, class Compare>
  constexpr T min(initializer_list<T> r, Compare comp);

template<copyable T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr T ranges::min(initializer_list<T> r, Comp comp = {}, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
  constexpr range_value_t<R>
    ranges::min(R&& r, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
  range_value_t<R>
    ranges::min(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

*Preconditions:* `ranges::distance(r) > 0`. For the overloads in
namespace `std`, `T` meets the *Cpp17CopyConstructible* requirements.
For the first form, `T` meets the *Cpp17LessThanComparable* requirements
([[cpp17.lessthancomparable]]).

*Returns:* The smallest value in the input range. Returns a copy of the
leftmost element when several elements are equivalent to the smallest.

*Complexity:* Exactly `ranges::distance(r) - 1` comparisons and twice as
many applications of the projection, if any.

*Remarks:* An invocation may explicitly specify an argument for the
template parameter `T` of the overloads in namespace `std`.

``` cpp
template<class T>
  constexpr const T& max(const T& a, const T& b);
template<class T, class Compare>
  constexpr const T& max(const T& a, const T& b, Compare comp);

template<class T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr const T& ranges::max(const T& a, const T& b, Comp comp = {}, Proj proj = {});
```

*Preconditions:* For the first form, `T` meets the
*Cpp17LessThanComparable* requirements ([[cpp17.lessthancomparable]]).

*Returns:* The larger value. Returns the first argument when the
arguments are equivalent.

*Complexity:* Exactly one comparison and two applications of the
projection, if any.

*Remarks:* An invocation may explicitly specify an argument for the
template parameter `T` of the overloads in namespace `std`.

``` cpp
template<class T>
  constexpr T max(initializer_list<T> r);
template<class T, class Compare>
  constexpr T max(initializer_list<T> r, Compare comp);

template<copyable T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr T ranges::max(initializer_list<T> r, Comp comp = {}, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
  constexpr range_value_t<R>
    ranges::max(R&& r, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
  range_value_t<R>
    ranges::max(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

*Preconditions:* `ranges::distance(r) > 0`. For the overloads in
namespace `std`, `T` meets the *Cpp17CopyConstructible* requirements.
For the first form, `T` meets the *Cpp17LessThanComparable* requirements
([[cpp17.lessthancomparable]]).

*Returns:* The largest value in the input range. Returns a copy of the
leftmost element when several elements are equivalent to the largest.

*Complexity:* Exactly `ranges::distance(r) - 1` comparisons and twice as
many applications of the projection, if any.

*Remarks:* An invocation may explicitly specify an argument for the
template parameter `T` of the overloads in namespace `std`.

``` cpp
template<class T>
  constexpr pair<const T&, const T&> minmax(const T& a, const T& b);
template<class T, class Compare>
  constexpr pair<const T&, const T&> minmax(const T& a, const T& b, Compare comp);

template<class T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr ranges::minmax_result<const T&>
    ranges::minmax(const T& a, const T& b, Comp comp = {}, Proj proj = {});
```

*Preconditions:* For the first form, `T` meets the
*Cpp17LessThanComparable* requirements ([[cpp17.lessthancomparable]]).

*Returns:* `{b, a}` if `b` is smaller than `a`, and `{a, b}` otherwise.

*Complexity:* Exactly one comparison and two applications of the
projection, if any.

*Remarks:* An invocation may explicitly specify an argument for the
template parameter `T` of the overloads in namespace `std`.

``` cpp
template<class T>
  constexpr pair<T, T> minmax(initializer_list<T> t);
template<class T, class Compare>
  constexpr pair<T, T> minmax(initializer_list<T> t, Compare comp);

template<copyable T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr ranges::minmax_result<T>
    ranges::minmax(initializer_list<T> r, Comp comp = {}, Proj proj = {});
template<input_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
  constexpr ranges::minmax_result<range_value_t<R>>
    ranges::minmax(R&& r, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  requires indirectly_copyable_storable<iterator_t<R>, range_value_t<R>*>
  ranges::minmax_result<range_value_t<R>>
    ranges::minmax(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

*Preconditions:* `ranges::distance(r) > 0`. For the overloads in
namespace `std`, `T` meets the *Cpp17CopyConstructible* requirements.
For the first form, type `T` meets the *Cpp17LessThanComparable*
requirements ([[cpp17.lessthancomparable]]).

*Returns:* Let `X` be the return type. Returns `X{x, y}`, where `x` is a
copy of the leftmost element with the smallest value and `y` a copy of
the rightmost element with the largest value in the input range.

*Complexity:* At most (3/2)`ranges::distance(r)` applications of the
corresponding predicate and twice as many applications of the
projection, if any.

*Remarks:* An invocation may explicitly specify an argument for the
template parameter `T` of the overloads in namespace `std`.

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator min_element(ForwardIterator first, ForwardIterator last);

template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator min_element(ExecutionPolicy&& exec,
                              ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class Compare>
  constexpr ForwardIterator min_element(ForwardIterator first, ForwardIterator last,
                                        Compare comp);
template<class ExecutionPolicy, class ForwardIterator, class Compare>
  ForwardIterator min_element(ExecutionPolicy&& exec,
                              ForwardIterator first, ForwardIterator last, Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr I ranges::min_element(I first, S last, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr borrowed_iterator_t<R>
    ranges::min_element(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  I ranges::min_element(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R,
         class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  borrowed_iterator_t<R>
    ranges::min_element(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Returns:* The first iterator `i` in the range \[`first`, `last`) such
that for every iterator `j` in the range \[`first`, `last`),

``` cpp
bool(invoke(comp, invoke(proj, *j), invoke(proj, *i)))
```

is `false`. Returns `last` if `first == last`.

*Complexity:* Exactly \max(`last - first - 1`, 0) comparisons and twice
as many projections.

``` cpp
template<class ForwardIterator>
  constexpr ForwardIterator max_element(ForwardIterator first, ForwardIterator last);
template<class ExecutionPolicy, class ForwardIterator>
  ForwardIterator max_element(ExecutionPolicy&& exec,
                              ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class Compare>
  constexpr ForwardIterator max_element(ForwardIterator first, ForwardIterator last,
                                        Compare comp);
template<class ExecutionPolicy, class ForwardIterator, class Compare>
  ForwardIterator max_element(ExecutionPolicy&& exec,
                              ForwardIterator first, ForwardIterator last,
                              Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr I ranges::max_element(I first, S last, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr borrowed_iterator_t<R>
    ranges::max_element(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  I ranges::max_element(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R,
         class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  borrowed_iterator_t<R>
    ranges::max_element(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for the overloads with
no parameters by those names.

*Returns:* The first iterator `i` in the range \[`first`, `last`) such
that for every iterator `j` in the range \[`first`, `last`),

``` cpp
bool(invoke(comp, invoke(proj, *i), invoke(proj, *j)))
```

is `false`. Returns `last` if `first == last`.

*Complexity:* Exactly \max(`last - first - 1`, 0) comparisons and twice
as many projections.

``` cpp
template<class ForwardIterator>
  constexpr pair<ForwardIterator, ForwardIterator>
    minmax_element(ForwardIterator first, ForwardIterator last);
template<class ExecutionPolicy, class ForwardIterator>
  pair<ForwardIterator, ForwardIterator>
    minmax_element(ExecutionPolicy&& exec,
                   ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class Compare>
  constexpr pair<ForwardIterator, ForwardIterator>
    minmax_element(ForwardIterator first, ForwardIterator last, Compare comp);
template<class ExecutionPolicy, class ForwardIterator, class Compare>
  pair<ForwardIterator, ForwardIterator>
    minmax_element(ExecutionPolicy&& exec,
                   ForwardIterator first, ForwardIterator last, Compare comp);

template<forward_iterator I, sentinel_for<I> S, class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  constexpr ranges::minmax_element_result<I>
    ranges::minmax_element(I first, S last, Comp comp = {}, Proj proj = {});
template<forward_range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  constexpr ranges::minmax_element_result<borrowed_iterator_t<R>>
    ranges::minmax_element(R&& r, Comp comp = {}, Proj proj = {});

template<execution-policy Ep, random_access_iterator I, sized_sentinel_for<I> S,
         class Proj = identity,
         indirect_strict_weak_order<projected<I, Proj>> Comp = ranges::less>
  ranges::minmax_element_result<I>
    ranges::minmax_element(Ep&& exec, I first, S last, Comp comp = {}, Proj proj = {});
template<execution-policy Ep, sized-random-access-range R, class Proj = identity,
         indirect_strict_weak_order<projected<iterator_t<R>, Proj>> Comp = ranges::less>
  ranges::minmax_element_result<borrowed_iterator_t<R>>
    ranges::minmax_element(Ep&& exec, R&& r, Comp comp = {}, Proj proj = {});
```

*Returns:* `{first, first}` if \[`first`, `last`) is empty, otherwise
`{m, M}`, where `m` is the first iterator in \[`first`, `last`) such
that no iterator in the range refers to a smaller element, and where `M`
is the last iterator[^5]

in \[`first`, `last`) such that no iterator in the range refers to a
larger element.

*Complexity:* Let N be `last - first`. At most
$\max(\bigl\lfloor{\frac{3}{2}} (N-1)\bigr\rfloor, 0)$ comparisons and
twice as many applications of the projection, if any.

### Bounded value <a id="alg.clamp">[[alg.clamp]]</a>

``` cpp
template<class T>
  constexpr const T& clamp(const T& v, const T& lo, const T& hi);
template<class T, class Compare>
  constexpr const T& clamp(const T& v, const T& lo, const T& hi, Compare comp);
template<class T, class Proj = identity,
         indirect_strict_weak_order<projected<const T*, Proj>> Comp = ranges::less>
  constexpr const T&
    ranges::clamp(const T& v, const T& lo, const T& hi, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` for the overloads with no parameter `comp`, and
let `proj` be `identity{}` for the overloads with no parameter `proj`.

*Preconditions:*
`bool(invoke(comp, invoke(proj, hi), invoke(proj, lo)))` is `false`. For
the first form, type `T` meets the *Cpp17LessThanComparable*
requirements ([[cpp17.lessthancomparable]]).

*Returns:* `lo` if
`bool(invoke(comp, invoke(proj, v), invoke(proj, lo)))` is `true`, `hi`
if `bool(invoke(comp, invoke(proj, hi), invoke(proj, v)))` is `true`,
otherwise `v`.

[*Note 1*: If NaN is avoided, `T` can be a floating-point
type. — *end note*]

*Complexity:* At most two comparisons and three applications of the
projection.

### Lexicographical comparison <a id="alg.lex.comparison">[[alg.lex.comparison]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  constexpr bool
    lexicographical_compare(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, InputIterator2 last2);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  bool
    lexicographical_compare(ExecutionPolicy&& exec,
                            ForwardIterator1 first1, ForwardIterator1 last1,
                            ForwardIterator2 first2, ForwardIterator2 last2);

template<class InputIterator1, class InputIterator2, class Compare>
  constexpr bool
    lexicographical_compare(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, InputIterator2 last2,
                            Compare comp);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class Compare>
  bool
    lexicographical_compare(ExecutionPolicy&& exec,
                            ForwardIterator1 first1, ForwardIterator1 last1,
                            ForwardIterator2 first2, ForwardIterator2 last2,
                            Compare comp);

template<input_iterator I1, sentinel_for<I1> S1, input_iterator I2, sentinel_for<I2> S2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_strict_weak_order<projected<I1, Proj1>,
                                    projected<I2, Proj2>> Comp = ranges::less>
  constexpr bool
    ranges::lexicographical_compare(I1 first1, S1 last1, I2 first2, S2 last2,
                                    Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<input_range R1, input_range R2, class Proj1 = identity,
         class Proj2 = identity,
         indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                    projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
  constexpr bool
    ranges::lexicographical_compare(R1&& r1, R2&& r2, Comp comp = {},
                                    Proj1 proj1 = {}, Proj2 proj2 = {});

template<execution-policy Ep, random_access_iterator I1, sized_sentinel_for<I1> S1,
         random_access_iterator I2, sized_sentinel_for<I2> S2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_strict_weak_order<projected<I1, Proj1>,
                                    projected<I2, Proj2>> Comp = ranges::less>
  bool ranges::lexicographical_compare(Ep&& exec, I1 first1, S1 last1, I2 first2, S2 last2,
                                       Comp comp = {}, Proj1 proj1 = {}, Proj2 proj2 = {});
template<execution-policy Ep, sized-random-access-range R1, sized-random-access-range R2,
         class Proj1 = identity, class Proj2 = identity,
         indirect_strict_weak_order<projected<iterator_t<R1>, Proj1>,
                                    projected<iterator_t<R2>, Proj2>> Comp = ranges::less>
  bool ranges::lexicographical_compare(Ep&& exec, R1&& r1, R2&& r2, Comp comp = {},
                                       Proj1 proj1 = {}, Proj2 proj2 = {});
```

*Returns:* `true` if and only if the sequence of elements defined by the
range \[`first1`, `last1`) is lexicographically less than the sequence
of elements defined by the range \[`first2`, `last2`).

*Complexity:* At most 2 \min(`last1 - first1`, \ `last2 - first2`)
applications of the corresponding comparison and each projection, if
any.

*Remarks:* If two sequences have the same number of elements and their
corresponding elements (if any) are equivalent, then neither sequence is
lexicographically less than the other. If one sequence is a proper
prefix of the other, then the shorter sequence is lexicographically less
than the longer sequence. Otherwise, the lexicographical comparison of
the sequences yields the same result as the comparison of the first
corresponding pair of elements that are not equivalent.

[*Example 1*:

`ranges::lexicographical_compare(I1, S1, I2, S2, Comp, Proj1, Proj2)`
can be implemented as:

``` cpp
for (; first1 != last1 && first2 != last2; ++first1, (void)++first2) {
  if (invoke(comp, invoke(proj1, *first1), invoke(proj2, *first2))) return true;
  if (invoke(comp, invoke(proj2, *first2), invoke(proj1, *first1))) return false;
}
return first1 == last1 && first2 != last2;
```

— *end example*]

[*Note 1*: An empty sequence is lexicographically less than any
non-empty sequence, but not less than any empty sequence. — *end note*]

### Three-way comparison algorithms <a id="alg.three.way">[[alg.three.way]]</a>

``` cpp
template<class InputIterator1, class InputIterator2, class Cmp>
  constexpr auto
    lexicographical_compare_three_way(InputIterator1 b1, InputIterator1 e1,
                                      InputIterator2 b2, InputIterator2 e2,
                                      Cmp comp)
      -> decltype(comp(*b1, *b2));
```

Let N be \min(`e1 - b1`, `e2 - b2`). Let E(n) be
`comp(*(b1 + `n`), *(b2 + `n`))`.

*Mandates:* `decltype(comp(*b1, *b2))` is a comparison category type.

*Returns:* E(i), where i is the smallest integer in \[`0`, N) such that
E(i)` != 0` is `true`, or `(e1 - b1) <=> (e2 - b2)` if no such integer
exists.

*Complexity:* At most N applications of `comp`.

``` cpp
template<class InputIterator1, class InputIterator2>
  constexpr auto
    lexicographical_compare_three_way(InputIterator1 b1, InputIterator1 e1,
                                      InputIterator2 b2, InputIterator2 e2);
```

*Effects:* Equivalent to:

``` cpp
return lexicographical_compare_three_way(b1, e1, b2, e2, compare_three_way());
```

### Permutation generators <a id="alg.permutation.generators">[[alg.permutation.generators]]</a>

``` cpp
template<class BidirectionalIterator>
  constexpr bool next_permutation(BidirectionalIterator first,
                                  BidirectionalIterator last);

template<class BidirectionalIterator, class Compare>
  constexpr bool next_permutation(BidirectionalIterator first,
                                  BidirectionalIterator last, Compare comp);

template<bidirectional_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr ranges::next_permutation_result<I>
    ranges::next_permutation(I first, S last, Comp comp = {}, Proj proj = {});
template<bidirectional_range R, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr ranges::next_permutation_result<borrowed_iterator_t<R>>
    ranges::next_permutation(R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for overloads with no
parameters by those names.

*Preconditions:* For the overloads in namespace `std`,
`BidirectionalIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]].

*Effects:* Takes a sequence defined by the range \[`first`, `last`) and
transforms it into the next permutation. The next permutation is found
by assuming that the set of all permutations is lexicographically sorted
with respect to `comp` and `proj`. If no such permutation exists,
transforms the sequence into the first permutation; that is, the
ascendingly-sorted one.

*Returns:* Let `B` be `true` if a next permutation was found and
otherwise `false`. Returns:

- `B` for the overloads in namespace `std`.
- `{ last, B }` for the overloads in namespace `ranges`.

*Complexity:* At most `(last - first) / 2` swaps.

``` cpp
template<class BidirectionalIterator>
  constexpr bool prev_permutation(BidirectionalIterator first,
                                  BidirectionalIterator last);

template<class BidirectionalIterator, class Compare>
  constexpr bool prev_permutation(BidirectionalIterator first,
                                  BidirectionalIterator last, Compare comp);

template<bidirectional_iterator I, sentinel_for<I> S, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<I, Comp, Proj>
  constexpr ranges::prev_permutation_result<I>
    ranges::prev_permutation(I first, S last, Comp comp = {}, Proj proj = {});
template<bidirectional_range R, class Comp = ranges::less,
         class Proj = identity>
  requires sortable<iterator_t<R>, Comp, Proj>
  constexpr ranges::prev_permutation_result<borrowed_iterator_t<R>>
    ranges::prev_permutation(R&& r, Comp comp = {}, Proj proj = {});
```

Let `comp` be `less{}` and `proj` be `identity{}` for overloads with no
parameters by those names.

*Preconditions:* For the overloads in namespace `std`,
`BidirectionalIterator` meets the *Cpp17ValueSwappable*
requirements [[swappable.requirements]].

*Effects:* Takes a sequence defined by the range \[`first`, `last`) and
transforms it into the previous permutation. The previous permutation is
found by assuming that the set of all permutations is lexicographically
sorted with respect to `comp` and `proj`. If no such permutation exists,
transforms the sequence into the last permutation; that is, the
descendingly-sorted one.

*Returns:* Let `B` be `true` if a previous permutation was found and
otherwise `false`. Returns:

- `B` for the overloads in namespace `std`.
- `{ last, B }` for the overloads in namespace `ranges`.

*Complexity:* At most `(last - first) / 2` swaps.

## Header `<numeric>` synopsis <a id="numeric.ops.overview">[[numeric.ops.overview]]</a>

``` cpp
// mostly freestanding
namespace std {
  // [accumulate], accumulate
  template<class InputIterator, class T>
    constexpr T accumulate(InputIterator first, InputIterator last, T init);
  template<class InputIterator, class T, class BinaryOperation>
    constexpr T accumulate(InputIterator first, InputIterator last, T init,
                           BinaryOperation binary_op);

  // [reduce], reduce
  template<class InputIterator>
    constexpr typename iterator_traits<InputIterator>::value_type
      reduce(InputIterator first, InputIterator last);
  template<class InputIterator, class T>
    constexpr T reduce(InputIterator first, InputIterator last, T init);
  template<class InputIterator, class T, class BinaryOperation>
    constexpr T reduce(InputIterator first, InputIterator last, T init,
                       BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator>
    typename iterator_traits<ForwardIterator>::value_type
      reduce(ExecutionPolicy&& exec,                            // freestanding-deleted, see [algorithms.parallel.overloads]
             ForwardIterator first, ForwardIterator last);
  template<class ExecutionPolicy, class ForwardIterator, class T>
    T reduce(ExecutionPolicy&& exec,                            // freestanding-deleted, see [algorithms.parallel.overloads]
             ForwardIterator first, ForwardIterator last, T init);
  template<class ExecutionPolicy, class ForwardIterator, class T, class BinaryOperation>
    T reduce(ExecutionPolicy&& exec,                            // freestanding-deleted, see [algorithms.parallel.overloads]
             ForwardIterator first, ForwardIterator last, T init, BinaryOperation binary_op);

  // [inner.product], inner product
  template<class InputIterator1, class InputIterator2, class T>
    constexpr T inner_product(InputIterator1 first1, InputIterator1 last1,
                              InputIterator2 first2, T init);
  template<class InputIterator1, class InputIterator2, class T,
           class BinaryOperation1, class BinaryOperation2>
    constexpr T inner_product(InputIterator1 first1, InputIterator1 last1,
                              InputIterator2 first2, T init,
                              BinaryOperation1 binary_op1, BinaryOperation2 binary_op2);

  // [transform.reduce], transform reduce
  template<class InputIterator1, class InputIterator2, class T>
    constexpr T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                                 InputIterator2 first2, T init);
  template<class InputIterator1, class InputIterator2, class T,
           class BinaryOperation1, class BinaryOperation2>
    constexpr T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                                 InputIterator2 first2, T init,
                                 BinaryOperation1 binary_op1, BinaryOperation2 binary_op2);
  template<class InputIterator, class T,
           class BinaryOperation, class UnaryOperation>
    constexpr T transform_reduce(InputIterator first, InputIterator last, T init,
                                 BinaryOperation binary_op, UnaryOperation unary_op);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2, class T>
    T transform_reduce(ExecutionPolicy&& exec,                  // freestanding-deleted, see [algorithms.parallel.overloads]
                       ForwardIterator1 first1, ForwardIterator1 last1,
                       ForwardIterator2 first2, T init);
  template<class ExecutionPolicy,
           class ForwardIterator1, class ForwardIterator2, class T,
           class BinaryOperation1, class BinaryOperation2>
    T transform_reduce(ExecutionPolicy&& exec,                  // freestanding-deleted, see [algorithms.parallel.overloads]
                       ForwardIterator1 first1, ForwardIterator1 last1,
                       ForwardIterator2 first2, T init,
                       BinaryOperation1 binary_op1, BinaryOperation2 binary_op2);
  template<class ExecutionPolicy, class ForwardIterator, class T,
           class BinaryOperation, class UnaryOperation>
    T transform_reduce(ExecutionPolicy&& exec,                  // freestanding-deleted, see [algorithms.parallel.overloads]
                       ForwardIterator first, ForwardIterator last, T init,
                       BinaryOperation binary_op, UnaryOperation unary_op);

  // [partial.sum], partial sum
  template<class InputIterator, class OutputIterator>
    constexpr OutputIterator
      partial_sum(InputIterator first, InputIterator last,
                  OutputIterator result);
  template<class InputIterator, class OutputIterator, class BinaryOperation>
    constexpr OutputIterator
      partial_sum(InputIterator first, InputIterator last,
                  OutputIterator result, BinaryOperation binary_op);

  // [exclusive.scan], exclusive scan
  template<class InputIterator, class OutputIterator, class T>
    constexpr OutputIterator
      exclusive_scan(InputIterator first, InputIterator last,
                     OutputIterator result, T init);
  template<class InputIterator, class OutputIterator, class T, class BinaryOperation>
    constexpr OutputIterator
      exclusive_scan(InputIterator first, InputIterator last,
                     OutputIterator result, T init, BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T>
    ForwardIterator2
      exclusive_scan(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first, ForwardIterator1 last,
                     ForwardIterator2 result, T init);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T,
           class BinaryOperation>
    ForwardIterator2
      exclusive_scan(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first, ForwardIterator1 last,
                     ForwardIterator2 result, T init, BinaryOperation binary_op);

  // [inclusive.scan], inclusive scan
  template<class InputIterator, class OutputIterator>
    constexpr OutputIterator
      inclusive_scan(InputIterator first, InputIterator last,
                     OutputIterator result);
  template<class InputIterator, class OutputIterator, class BinaryOperation>
    constexpr OutputIterator
      inclusive_scan(InputIterator first, InputIterator last,
                     OutputIterator result, BinaryOperation binary_op);
  template<class InputIterator, class OutputIterator, class BinaryOperation, class T>
    constexpr OutputIterator
      inclusive_scan(InputIterator first, InputIterator last,
                     OutputIterator result, BinaryOperation binary_op, T init);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2
      inclusive_scan(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first, ForwardIterator1 last,
                     ForwardIterator2 result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation>
    ForwardIterator2
      inclusive_scan(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first, ForwardIterator1 last,
                     ForwardIterator2 result, BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation, class T>
    ForwardIterator2
      inclusive_scan(ExecutionPolicy&& exec,                    // freestanding-deleted, see [algorithms.parallel.overloads]
                     ForwardIterator1 first, ForwardIterator1 last,
                     ForwardIterator2 result, BinaryOperation binary_op, T init);

  // [transform.exclusive.scan], transform exclusive scan
  template<class InputIterator, class OutputIterator, class T,
           class BinaryOperation, class UnaryOperation>
    constexpr OutputIterator
      transform_exclusive_scan(InputIterator first, InputIterator last,
                               OutputIterator result, T init,
                               BinaryOperation binary_op, UnaryOperation unary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T,
           class BinaryOperation, class UnaryOperation>
    ForwardIterator2
      transform_exclusive_scan(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator1 first, ForwardIterator1 last,
                               ForwardIterator2 result, T init,
                               BinaryOperation binary_op, UnaryOperation unary_op);

  // [transform.inclusive.scan], transform inclusive scan
  template<class InputIterator, class OutputIterator,
           class BinaryOperation, class UnaryOperation>
    constexpr OutputIterator
      transform_inclusive_scan(InputIterator first, InputIterator last,
                               OutputIterator result,
                               BinaryOperation binary_op, UnaryOperation unary_op);
  template<class InputIterator, class OutputIterator,
           class BinaryOperation, class UnaryOperation, class T>
    constexpr OutputIterator
      transform_inclusive_scan(InputIterator first, InputIterator last,
                               OutputIterator result,
                               BinaryOperation binary_op, UnaryOperation unary_op, T init);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation, class UnaryOperation>
    ForwardIterator2
      transform_inclusive_scan(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator1 first, ForwardIterator1 last,
                               ForwardIterator2 result, BinaryOperation binary_op,
                               UnaryOperation unary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation, class UnaryOperation, class T>
    ForwardIterator2
      transform_inclusive_scan(ExecutionPolicy&& exec,          // freestanding-deleted, see [algorithms.parallel.overloads]
                               ForwardIterator1 first, ForwardIterator1 last,
                               ForwardIterator2 result,
                               BinaryOperation binary_op, UnaryOperation unary_op, T init);

  // [adjacent.difference], adjacent difference
  template<class InputIterator, class OutputIterator>
    constexpr OutputIterator
      adjacent_difference(InputIterator first, InputIterator last,
                          OutputIterator result);
  template<class InputIterator, class OutputIterator, class BinaryOperation>
    constexpr OutputIterator
      adjacent_difference(InputIterator first, InputIterator last,
                          OutputIterator result, BinaryOperation binary_op);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2
      adjacent_difference(ExecutionPolicy&& exec,               // freestanding-deleted, see [algorithms.parallel.overloads]
                          ForwardIterator1 first, ForwardIterator1 last,
                          ForwardIterator2 result);
  template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
           class BinaryOperation>
    ForwardIterator2
      adjacent_difference(ExecutionPolicy&& exec,               // freestanding-deleted, see [algorithms.parallel.overloads]
                          ForwardIterator1 first, ForwardIterator1 last,
                          ForwardIterator2 result, BinaryOperation binary_op);

  // [numeric.iota], iota
  template<class ForwardIterator, class T>
    constexpr void iota(ForwardIterator first, ForwardIterator last, T value);

  namespace ranges {
    template<class O, class T>
      using iota_result = out_value_result<O, T>;

    template<input_or_output_iterator O, sentinel_for<O> S, weakly_incrementable T>
      requires indirectly_writable<O, const T&>
      constexpr iota_result<O, T> iota(O first, S last, T value);

    template<weakly_incrementable T, output_range<const T&> R>
      constexpr iota_result<borrowed_iterator_t<R>, T> iota(R&& r, T value);
  }

  // [numeric.ops.gcd], greatest common divisor
  template<class M, class N>
    constexpr common_type_t<M, N> gcd(M m, N n);

  // [numeric.ops.lcm], least common multiple
  template<class M, class N>
    constexpr common_type_t<M, N> lcm(M m, N n);

  // [numeric.ops.midpoint], midpoint
  template<class T>
    constexpr T midpoint(T a, T b) noexcept;
  template<class T>
    constexpr T* midpoint(T* a, T* b);

  // [numeric.sat], saturation arithmetic
  template<class T>
    constexpr T add_sat(T x, T y) noexcept;
  template<class T>
    constexpr T sub_sat(T x, T y) noexcept;
  template<class T>
    constexpr T mul_sat(T x, T y) noexcept;
  template<class T>
    constexpr T div_sat(T x, T y) noexcept;
  template<class T, class U>
    constexpr T saturate_cast(U x) noexcept;
}
```

## Generalized numeric operations <a id="numeric.ops">[[numeric.ops]]</a>

### General <a id="numeric.ops.general">[[numeric.ops.general]]</a>

[*Note 1*: The use of closed ranges as well as semi-open ranges to
specify requirements throughout [[numeric.ops]] is
intentional. — *end note*]

### Definitions <a id="numerics.defns">[[numerics.defns]]</a>

Define `GENERALIZED_NONCOMMUTATIVE_SUM(op, a1, \dotsc, aN)` as follows:

- `a1` when `N` is `1`, otherwise
- `op(GENERALIZED_NONCOMMUTATIVE_SUM(op, a1, \dotsc, aK),`  
  `\phantom{op(}GENERALIZED_NONCOMMUTATIVE_SUM(op, aM, \dotsc, aN))` for
  any `K` where 1 < K+1 = M ≤ N.

Define `GENERALIZED_SUM(op, a1, \dotsc, aN)` as
`GENERALIZED_NONCOMMUTATIVE_SUM(op, b1, \dotsc, bN)`, where
`b1, \dotsc, bN` may be any permutation of `a1, \dotsc, aN`.

### Accumulate <a id="accumulate">[[accumulate]]</a>

``` cpp
template<class InputIterator, class T>
  constexpr T accumulate(InputIterator first, InputIterator last, T init);
template<class InputIterator, class T, class BinaryOperation>
  constexpr T accumulate(InputIterator first, InputIterator last, T init,
                         BinaryOperation binary_op);
```

*Preconditions:* `T` meets the *Cpp17CopyConstructible*
([[cpp17.copyconstructible]]) and *Cpp17CopyAssignable*
([[cpp17.copyassignable]]) requirements. In the range \[`first`,
`last`\], `binary_op` neither modifies elements nor invalidates
iterators or subranges.[^6]

*Effects:* Computes its result by initializing the accumulator `acc`
with the initial value `init` and then modifies it with
`acc = std::move(acc) + *i` or `acc = binary_op(std::move(acc), *i)` for
every iterator `i` in the range \[`first`, `last`) in order.[^7]

### Reduce <a id="reduce">[[reduce]]</a>

``` cpp
template<class InputIterator>
  constexpr typename iterator_traits<InputIterator>::value_type
    reduce(InputIterator first, InputIterator last);
```

*Effects:* Equivalent to:

``` cpp
return reduce(first, last,
              typename iterator_traits<InputIterator>::value_type{});
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator>
  typename iterator_traits<ForwardIterator>::value_type
    reduce(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
return reduce(std::forward<ExecutionPolicy>(exec), first, last,
              typename iterator_traits<ForwardIterator>::value_type{});
```

``` cpp
template<class InputIterator, class T>
  constexpr T reduce(InputIterator first, InputIterator last, T init);
```

*Effects:* Equivalent to:

``` cpp
return reduce(first, last, init, plus<>());
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator, class T>
  T reduce(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator last, T init);
```

*Effects:* Equivalent to:

``` cpp
return reduce(std::forward<ExecutionPolicy>(exec), first, last, init, plus<>());
```

``` cpp
template<class InputIterator, class T, class BinaryOperation>
  constexpr T reduce(InputIterator first, InputIterator last, T init,
                     BinaryOperation binary_op);
template<class ExecutionPolicy, class ForwardIterator, class T, class BinaryOperation>
  T reduce(ExecutionPolicy&& exec,
           ForwardIterator first, ForwardIterator last, T init,
           BinaryOperation binary_op);
```

*Mandates:* All of

- `binary_op(init, *first)`,
- `binary_op(*first, init)`,
- `binary_op(init, init)`, and
- `binary_op(*first, *first)`

are convertible to `T`.

*Preconditions:*

- `T` meets the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]])
  requirements.
- `binary_op` neither invalidates iterators or subranges, nor modifies
  elements in the range \[`first`, `last`\].

*Returns:* *GENERALIZED_SUM*(binary_op, init, \*i, …) for every `i` in
\[`first`, `last`).

*Complexity:* 𝑂(`last - first`) applications of `binary_op`.

[*Note 1*: The difference between `reduce` and `accumulate` is that
`reduce` applies `binary_op` in an unspecified order, which yields a
nondeterministic result for non-associative or non-commutative
`binary_op` such as floating-point addition. — *end note*]

### Inner product <a id="inner.product">[[inner.product]]</a>

``` cpp
template<class InputIterator1, class InputIterator2, class T>
  constexpr T inner_product(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, T init);
template<class InputIterator1, class InputIterator2, class T,
         class BinaryOperation1, class BinaryOperation2>
  constexpr T inner_product(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, T init,
                            BinaryOperation1 binary_op1,
                            BinaryOperation2 binary_op2);
```

*Preconditions:* `T` meets the *Cpp17CopyConstructible*
([[cpp17.copyconstructible]]) and *Cpp17CopyAssignable*
([[cpp17.copyassignable]]) requirements. In the ranges \[`first1`,
`last1`\] and \[`first2`, `first2 + (last1 - first1)`\] `binary_op1` and
`binary_op2` neither modifies elements nor invalidates iterators or
subranges.[^8]

*Effects:* Computes its result by initializing the accumulator `acc`
with the initial value `init` and then modifying it with
`acc = std::move(acc) + (*i1) * (*i2)` or
`acc = binary_op1(std::move(acc), binary_op2(*i1, *i2))` for every
iterator `i1` in the range \[`first1`, `last1`) and iterator `i2` in the
range \[`first2`, `first2 + (last1 - first1)`) in order.

### Transform reduce <a id="transform.reduce">[[transform.reduce]]</a>

``` cpp
template<class InputIterator1, class InputIterator2, class T>
  constexpr T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                               InputIterator2 first2,
                               T init);
```

*Effects:* Equivalent to:

``` cpp
return transform_reduce(first1, last1, first2, init, plus<>(), multiplies<>());
```

``` cpp
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class T>
  T transform_reduce(ExecutionPolicy&& exec,
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2,
                     T init);
```

*Effects:* Equivalent to:

``` cpp
return transform_reduce(std::forward<ExecutionPolicy>(exec),
                        first1, last1, first2, init, plus<>(), multiplies<>());
```

``` cpp
template<class InputIterator1, class InputIterator2, class T,
         class BinaryOperation1, class BinaryOperation2>
  constexpr T transform_reduce(InputIterator1 first1, InputIterator1 last1,
                               InputIterator2 first2,
                               T init,
                               BinaryOperation1 binary_op1,
                               BinaryOperation2 binary_op2);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class T,
         class BinaryOperation1, class BinaryOperation2>
  T transform_reduce(ExecutionPolicy&& exec,
                     ForwardIterator1 first1, ForwardIterator1 last1,
                     ForwardIterator2 first2,
                     T init,
                     BinaryOperation1 binary_op1,
                     BinaryOperation2 binary_op2);
```

*Mandates:* All of

- `binary_op1(init, init)`,
- `binary_op1(init, binary_op2(*first1, *first2))`,
- `binary_op1(binary_op2(*first1, *first2), init)`, and
- `binary_op1(binary_op2(*first1, *first2), binary_op2(*first1, *first2))`

are convertible to `T`.

*Preconditions:*

- `T` meets the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]])
  requirements.
- Neither `binary_op1` nor `binary_op2` invalidates subranges, nor
  modifies elements in the ranges \[`first1`, `last1`\] and \[`first2`,
  `first2 + (last1 - first1)`\].

*Returns:*

``` cpp
GENERALIZED_SUM(binary_op1, init, binary_op2(*i, *(first2 + (i - first1))), $\dotsc$)
```

for every iterator `i` in \[`first1`, `last1`).

*Complexity:* 𝑂(`last1 - first1`) applications each of `binary_op1` and
`binary_op2`.

``` cpp
template<class InputIterator, class T,
         class BinaryOperation, class UnaryOperation>
  constexpr T transform_reduce(InputIterator first, InputIterator last, T init,
                               BinaryOperation binary_op, UnaryOperation unary_op);
template<class ExecutionPolicy,
         class ForwardIterator, class T,
         class BinaryOperation, class UnaryOperation>
  T transform_reduce(ExecutionPolicy&& exec,
                     ForwardIterator first, ForwardIterator last,
                     T init, BinaryOperation binary_op, UnaryOperation unary_op);
```

*Mandates:* All of

- `binary_op(init, init)`,
- `binary_op(init, unary_op(*first))`,
- `binary_op(unary_op(*first), init)`, and
- `binary_op(unary_op(*first), unary_op(*first))`

are convertible to `T`.

*Preconditions:*

- `T` meets the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]])
  requirements.
- Neither `unary_op` nor `binary_op` invalidates subranges, nor modifies
  elements in the range \[`first`, `last`\].

*Returns:*

``` cpp
GENERALIZED_SUM(binary_op, init, unary_op(*i), $\dotsc$)
```

for every iterator `i` in \[`first`, `last`).

*Complexity:* 𝑂(`last - first`) applications each of `unary_op` and
`binary_op`.

[*Note 1*: `transform_reduce` does not apply `unary_op` to
`init`. — *end note*]

### Partial sum <a id="partial.sum">[[partial.sum]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  constexpr OutputIterator
    partial_sum(InputIterator first, InputIterator last,
                OutputIterator result);
template<class InputIterator, class OutputIterator, class BinaryOperation>
  constexpr OutputIterator
    partial_sum(InputIterator first, InputIterator last,
                OutputIterator result, BinaryOperation binary_op);
```

*Mandates:* `InputIterator`’s value type is constructible from `*first`.
The result of the expression `std::move(acc) + *i` or
`binary_op(std::move(acc), *i)` is implicitly convertible to
`InputIterator`’s value type. `acc` is
writable [[iterator.requirements.general]] to `result`.

*Preconditions:* In the ranges \[`first`, `last`\] and \[`result`,
`result + (last - first)`\] `binary_op` neither modifies elements nor
invalidates iterators or subranges.[^9]

*Effects:* For a non-empty range, the function creates an accumulator
`acc` whose type is `InputIterator`’s value type, initializes it with
`*first`, and assigns the result to `*result`. For every iterator `i` in
\[`first + 1`, `last`) in order, `acc` is then modified by
`acc = std::move(acc) + *i` or `acc = binary_op(std::move(acc), *i)` and
the result is assigned to `*(result + (i - first))`.

*Returns:* `result + (last - first)`.

*Complexity:* Exactly `(last - first) - 1` applications of the binary
operation.

*Remarks:* `result` may be equal to `first`.

### Exclusive scan <a id="exclusive.scan">[[exclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator, class T>
  constexpr OutputIterator
    exclusive_scan(InputIterator first, InputIterator last,
                   OutputIterator result, T init);
```

*Effects:* Equivalent to:

``` cpp
return exclusive_scan(first, last, result, init, plus<>());
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2, class T>
  ForwardIterator2
    exclusive_scan(ExecutionPolicy&& exec,
                   ForwardIterator1 first, ForwardIterator1 last,
                   ForwardIterator2 result, T init);
```

*Effects:* Equivalent to:

``` cpp
return exclusive_scan(std::forward<ExecutionPolicy>(exec),
                      first, last, result, init, plus<>());
```

``` cpp
template<class InputIterator, class OutputIterator, class T, class BinaryOperation>
  constexpr OutputIterator
    exclusive_scan(InputIterator first, InputIterator last,
                   OutputIterator result, T init, BinaryOperation binary_op);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class T, class BinaryOperation>
  ForwardIterator2
    exclusive_scan(ExecutionPolicy&& exec,
                   ForwardIterator1 first, ForwardIterator1 last,
                   ForwardIterator2 result, T init, BinaryOperation binary_op);
```

*Mandates:* All of

- `binary_op(init, init)`,
- `binary_op(init, *first)`, and
- `binary_op(*first, *first)`

are convertible to `T`.

*Preconditions:*

- `T` meets the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]])
  requirements.
- `binary_op` neither invalidates iterators or subranges, nor modifies
  elements in the ranges \[`first`, `last`\] or \[`result`,
  `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of:

``` cpp
GENERALIZED_NONCOMMUTATIVE_SUM(
    binary_op, init, *(first + 0), *(first + 1), $\dotsc$, *(first + K - 1))
```

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications of `binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `exclusive_scan` and `inclusive_scan`
is that `exclusive_scan` excludes the iᵗʰ input element from the iᵗʰ
sum. If `binary_op` is not mathematically associative, the behavior of
`exclusive_scan` can be nondeterministic. — *end note*]

### Inclusive scan <a id="inclusive.scan">[[inclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  constexpr OutputIterator
    inclusive_scan(InputIterator first, InputIterator last,
                   OutputIterator result);
```

*Effects:* Equivalent to:

``` cpp
return inclusive_scan(first, last, result, plus<>());
```

``` cpp
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    inclusive_scan(ExecutionPolicy&& exec,
                   ForwardIterator1 first, ForwardIterator1 last,
                   ForwardIterator2 result);
```

*Effects:* Equivalent to:

``` cpp
return inclusive_scan(std::forward<ExecutionPolicy>(exec), first, last, result, plus<>());
```

``` cpp
template<class InputIterator, class OutputIterator, class BinaryOperation>
  constexpr OutputIterator
    inclusive_scan(InputIterator first, InputIterator last,
                   OutputIterator result, BinaryOperation binary_op);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation>
  ForwardIterator2
    inclusive_scan(ExecutionPolicy&& exec,
                   ForwardIterator1 first, ForwardIterator1 last,
                   ForwardIterator2 result, BinaryOperation binary_op);

template<class InputIterator, class OutputIterator, class BinaryOperation, class T>
  constexpr OutputIterator
    inclusive_scan(InputIterator first, InputIterator last,
                   OutputIterator result, BinaryOperation binary_op, T init);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class BinaryOperation, class T>
  ForwardIterator2
    inclusive_scan(ExecutionPolicy&& exec,
                   ForwardIterator1 first, ForwardIterator1 last,
                   ForwardIterator2 result, BinaryOperation binary_op, T init);
```

Let `U` be the value type of `decltype(first)`.

*Mandates:* If `init` is provided, all of

- `binary_op(init, init)`,
- `binary_op(init, *first)`, and
- `binary_op(*first, *first)`

are convertible to `T`; otherwise, `binary_op(*first, *first)` is
convertible to `U`.

*Preconditions:*

- If `init` is provided, `T` meets the *Cpp17MoveConstructible*
  ([[cpp17.moveconstructible]]) requirements; otherwise, `U` meets the
  *Cpp17MoveConstructible* requirements.
- `binary_op` neither invalidates iterators or subranges, nor modifies
  elements in the ranges \[`first`, `last`\] or \[`result`,
  `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of

- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op, init, \*(first + 0), \*(first + 1), …, \*(first + K))  
  if `init` is provided, or
- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op, \*(first + 0), \*(first + 1), …, \*(first + K))  
  otherwise.

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications of `binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `exclusive_scan` and `inclusive_scan`
is that `inclusive_scan` includes the iᵗʰ input element in the iᵗʰ sum.
If `binary_op` is not mathematically associative, the behavior of
`inclusive_scan` can be nondeterministic. — *end note*]

### Transform exclusive scan <a id="transform.exclusive.scan">[[transform.exclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator, class T,
         class BinaryOperation, class UnaryOperation>
  constexpr OutputIterator
    transform_exclusive_scan(InputIterator first, InputIterator last,
                             OutputIterator result, T init,
                             BinaryOperation binary_op, UnaryOperation unary_op);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2, class T,
         class BinaryOperation, class UnaryOperation>
  ForwardIterator2
    transform_exclusive_scan(ExecutionPolicy&& exec,
                             ForwardIterator1 first, ForwardIterator1 last,
                             ForwardIterator2 result, T init,
                             BinaryOperation binary_op, UnaryOperation unary_op);
```

*Mandates:* All of

- `binary_op(init, init)`,
- `binary_op(init, unary_op(*first))`, and
- `binary_op(unary_op(*first), unary_op(*first))`

are convertible to `T`.

*Preconditions:*

- `T` meets the *Cpp17MoveConstructible* ([[cpp17.moveconstructible]])
  requirements.
- Neither `unary_op` nor `binary_op` invalidates iterators or subranges,
  nor modifies elements in the ranges \[`first`, `last`\] or \[`result`,
  `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of:

``` cpp
GENERALIZED_NONCOMMUTATIVE_SUM(
    binary_op, init,
    unary_op(*(first + 0)), unary_op(*(first + 1)), $\dotsc$, unary_op(*(first + K - 1)))
```

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications each of `unary_op` and
`binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `transform_exclusive_scan` and
`transform_inclusive_scan` is that `transform_exclusive_scan` excludes
the iᵗʰ input element from the iᵗʰ sum. If `binary_op` is not
mathematically associative, the behavior of `transform_exclusive_scan`
can be nondeterministic. `transform_exclusive_scan` does not apply
`unary_op` to `init`. — *end note*]

### Transform inclusive scan <a id="transform.inclusive.scan">[[transform.inclusive.scan]]</a>

``` cpp
template<class InputIterator, class OutputIterator,
         class BinaryOperation, class UnaryOperation>
  constexpr OutputIterator
    transform_inclusive_scan(InputIterator first, InputIterator last,
                             OutputIterator result,
                             BinaryOperation binary_op, UnaryOperation unary_op);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation, class UnaryOperation>
  ForwardIterator2
    transform_inclusive_scan(ExecutionPolicy&& exec,
                             ForwardIterator1 first, ForwardIterator1 last,
                             ForwardIterator2 result,
                             BinaryOperation binary_op, UnaryOperation unary_op);
template<class InputIterator, class OutputIterator,
         class BinaryOperation, class UnaryOperation, class T>
  constexpr OutputIterator
    transform_inclusive_scan(InputIterator first, InputIterator last,
                             OutputIterator result,
                             BinaryOperation binary_op, UnaryOperation unary_op,
                             T init);
template<class ExecutionPolicy,
         class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation, class UnaryOperation, class T>
  ForwardIterator2
    transform_inclusive_scan(ExecutionPolicy&& exec,
                             ForwardIterator1 first, ForwardIterator1 last,
                             ForwardIterator2 result,
                             BinaryOperation binary_op, UnaryOperation unary_op,
                             T init);
```

Let `U` be the value type of `decltype(first)`.

*Mandates:* If `init` is provided, all of

- `binary_op(init, init)`,
- `binary_op(init, unary_op(*first))`, and
- `binary_op(unary_op(*first), unary_op(*first))`

are convertible to `T`; otherwise,
`binary_op(unary_op(*first), unary_op(*first))` is convertible to `U`.

*Preconditions:*

- If `init` is provided, `T` meets the *Cpp17MoveConstructible*
  ([[cpp17.moveconstructible]]) requirements; otherwise, `U` meets the
  *Cpp17MoveConstructible* requirements.
- Neither `unary_op` nor `binary_op` invalidates iterators or subranges,
  nor modifies elements in the ranges \[`first`, `last`\] or \[`result`,
  `result + (last - first)`\].

*Effects:* For each integer `K` in \[`0`, `last - first`) assigns
through `result + K` the value of

- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op, init,  
      unary_op(\*(first + 0)), unary_op(\*(first + 1)), …,
  unary_op(\*(first + K)))  
  if `init` is provided, or
- *GENERALIZED_NONCOMMUTATIVE_SUM*(  
      binary_op,  
      unary_op(\*(first + 0)), unary_op(\*(first + 1)), …,
  unary_op(\*(first + K)))  
  otherwise.

*Returns:* The end of the resulting range beginning at `result`.

*Complexity:* 𝑂(`last - first`) applications each of `unary_op` and
`binary_op`.

*Remarks:* `result` may be equal to `first`.

[*Note 1*: The difference between `transform_exclusive_scan` and
`transform_inclusive_scan` is that `transform_inclusive_scan` includes
the iᵗʰ input element in the iᵗʰ sum. If `binary_op` is not
mathematically associative, the behavior of `transform_inclusive_scan`
can be nondeterministic. `transform_inclusive_scan` does not apply
`unary_op` to `init`. — *end note*]

### Adjacent difference <a id="adjacent.difference">[[adjacent.difference]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  constexpr OutputIterator
    adjacent_difference(InputIterator first, InputIterator last,
                        OutputIterator result);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    adjacent_difference(ExecutionPolicy&& exec,
                        ForwardIterator1 first, ForwardIterator1 last, ForwardIterator2 result);

template<class InputIterator, class OutputIterator, class BinaryOperation>
  constexpr OutputIterator
    adjacent_difference(InputIterator first, InputIterator last,
                        OutputIterator result, BinaryOperation binary_op);
template<class ExecutionPolicy, class ForwardIterator1, class ForwardIterator2,
         class BinaryOperation>
  ForwardIterator2
    adjacent_difference(ExecutionPolicy&& exec,
                        ForwardIterator1 first, ForwardIterator1 last,
                        ForwardIterator2 result, BinaryOperation binary_op);
```

Let `T` be the value type of `decltype(first)`. For the overloads that
do not take an argument `binary_op`, let `binary_op` be an lvalue that
denotes an object of type `minus<>`.

*Mandates:*

- For the overloads with no `ExecutionPolicy`, `T` is constructible from
  `*first`. `acc` (defined below) is
  writable [[iterator.requirements.general]] to the `result` output
  iterator. The result of the expression
  `binary_op(val, std::move(acc))` is writable to `result`.
- For the overloads with an `ExecutionPolicy`, the result of the
  expressions `binary_op(*first, *first)` and `*first` are writable to
  `result`.

*Preconditions:*

- For the overloads with no `ExecutionPolicy`, `T` meets the
  *Cpp17MoveAssignable* ([[cpp17.moveassignable]]) requirements.
- For all overloads, in the ranges \[`first`, `last`\] and \[`result`,
  `result + (last - first)`\], `binary_op` neither modifies elements nor
  invalidates iterators or subranges.[^10]

*Effects:* For the overloads with no `ExecutionPolicy` and a non-empty
range, the function creates an accumulator `acc` of type `T`,
initializes it with `*first`, and assigns the result to `*result`. For
every iterator `i` in \[`first + 1`, `last`) in order, creates an object
`val` whose type is `T`, initializes it with `*i`, computes
`binary_op(val, std::move(acc))`, assigns the result to
`*(result + (i - first))`, and move assigns from `val` to `acc`.

For the overloads with an `ExecutionPolicy` and a non-empty range,
performs `*result = *first`. Then, for every `d` in \[`1`,
`last - first - 1`\], performs
`*(result + d) = binary_op(*(first + d), *(first + (d - 1)))`.

*Returns:* `result + (last - first)`.

*Complexity:* Exactly `(last - first) - 1` applications of the binary
operation.

*Remarks:* For the overloads with no `ExecutionPolicy`, `result` may be
equal to `first`. For the overloads with an `ExecutionPolicy`, the
ranges \[`first`, `last`) and \[`result`, `result + (last - first)`)
shall not overlap.

### Iota <a id="numeric.iota">[[numeric.iota]]</a>

``` cpp
template<class ForwardIterator, class T>
  constexpr void iota(ForwardIterator first, ForwardIterator last, T value);
```

*Mandates:* `T` is convertible to `ForwardIterator`’s value type. The
expression `++val`, where `val` has type `T`, is well-formed.

*Effects:* For each element referred to by the iterator `i` in the range
\[`first`, `last`), assigns `*i = value` and increments `value` as if by
`++value`.

*Complexity:* Exactly `last - first` increments and assignments.

``` cpp
template<input_or_output_iterator O, sentinel_for<O> S, weakly_incrementable T>
  requires indirectly_writable<O, const T&>
  constexpr ranges::iota_result<O, T> ranges::iota(O first, S last, T value);
template<weakly_incrementable T, output_range<const T&> R>
  constexpr ranges::iota_result<borrowed_iterator_t<R>, T> ranges::iota(R&& r, T value);
```

*Effects:* Equivalent to:

``` cpp
while (first != last) {
  *first = as_const(value);
  ++first;
  ++value;
}
return {std::move(first), std::move(value)};
```

### Greatest common divisor <a id="numeric.ops.gcd">[[numeric.ops.gcd]]</a>

``` cpp
template<class M, class N>
  constexpr common_type_t<M, N> gcd(M m, N n);
```

*Mandates:* `M` and `N` both are integer types other than cv `bool`.

*Preconditions:* |`m`| and |`n`| are representable as a value of
`common_type_t<M, N>`.

[*Note 1*: These requirements ensure, for example, that
`gcd(m, m)` = |`m`| is representable as a value of type
`M`. — *end note*]

*Returns:* Zero when `m` and `n` are both zero. Otherwise, returns the
greatest common divisor of |`m`| and |`n`|.

*Throws:* Nothing.

### Least common multiple <a id="numeric.ops.lcm">[[numeric.ops.lcm]]</a>

``` cpp
template<class M, class N>
  constexpr common_type_t<M, N> lcm(M m, N n);
```

*Mandates:* `M` and `N` both are integer types other than cv `bool`.

*Preconditions:* |`m`| and |`n`| are representable as a value of
`common_type_t<M, N>`. The least common multiple of |`m`| and |`n`| is
representable as a value of type `common_type_t<M, N>`.

*Returns:* Zero when either `m` or `n` is zero. Otherwise, returns the
least common multiple of |`m`| and |`n`|.

*Throws:* Nothing.

### Midpoint <a id="numeric.ops.midpoint">[[numeric.ops.midpoint]]</a>

``` cpp
template<class T>
  constexpr T midpoint(T a, T b) noexcept;
```

*Constraints:* `T` is an arithmetic type other than `bool`.

*Returns:* Half the sum of `a` and `b`. If `T` is an integer type and
the sum is odd, the result is rounded towards `a`.

*Remarks:* No overflow occurs. If `T` is a floating-point type, at most
one inexact operation occurs.

``` cpp
template<class T>
  constexpr T* midpoint(T* a, T* b);
```

*Constraints:* `T` is an object type.

*Mandates:* `T` is a complete type.

*Preconditions:* `a` and `b` point to, respectively, elements i and j of
the same array object `x`.

[*Note 1*: As specified in [[basic.compound]], an object that is not an
array element is considered to belong to a single-element array for this
purpose and a pointer past the last element of an array of n elements is
considered to be equivalent to a pointer to a hypothetical array element
n for this purpose. — *end note*]

*Returns:* A pointer to array element $i+\frac{j-i}{2}$ of `x`, where
the result of the division is truncated towards zero.

### Saturation arithmetic <a id="numeric.sat">[[numeric.sat]]</a>

#### Arithmetic functions <a id="numeric.sat.func">[[numeric.sat.func]]</a>

In the following descriptions, an arithmetic operation is performed as a
mathematical operation with infinite range and then it is determined
whether the mathematical result fits into the result type.

``` cpp
template<class T>
  constexpr T add_sat(T x, T y) noexcept;
```

*Constraints:* `T` is a signed or unsigned integer
type [[basic.fundamental]].

*Returns:* If `x` + `y` is representable as a value of type `T`,
`x` + `y`; otherwise, either the largest or smallest representable value
of type `T`, whichever is closer to the value of `x` + `y`.

``` cpp
template<class T>
  constexpr T sub_sat(T x, T y) noexcept;
```

*Constraints:* `T` is a signed or unsigned integer
type [[basic.fundamental]].

*Returns:* If `x` - `y` is representable as a value of type `T`,
`x` - `y`; otherwise, either the largest or smallest representable value
of type `T`, whichever is closer to the value of `x` - `y`.

``` cpp
template<class T>
  constexpr T mul_sat(T x, T y) noexcept;
```

*Constraints:* `T` is a signed or unsigned integer
type [[basic.fundamental]].

*Returns:* If `x` \times `y` is representable as a value of type `T`,
`x` \times `y`; otherwise, either the largest or smallest representable
value of type `T`, whichever is closer to the value of `x` \times `y`.

``` cpp
template<class T>
  constexpr T div_sat(T x, T y) noexcept;
```

*Constraints:* `T` is a signed or unsigned integer
type [[basic.fundamental]].

*Preconditions:* `y != 0` is `true`.

*Returns:* If `T` is a signed integer type and
`x == numeric_limits<T>::min() && y == -1` is `true`,
`numeric_limits<T>::max()`, otherwise, `x / y`.

*Remarks:* A function call expression that violates the precondition in
the *Preconditions* element is not a core constant
expression [[expr.const]].

#### Casting <a id="numeric.sat.cast">[[numeric.sat.cast]]</a>

``` cpp
template<class R, class T>
  constexpr R saturate_cast(T x) noexcept;
```

*Constraints:* `R` and `T` are signed or unsigned integer
types [[basic.fundamental]].

*Returns:* If `x` is representable as a value of type `R`, `x`;
otherwise, either the largest or smallest representable value of type
`R`, whichever is closer to the value of `x`.

## Specialized `<memory>` algorithms <a id="specialized.algorithms">[[specialized.algorithms]]</a>

### General <a id="specialized.algorithms.general">[[specialized.algorithms.general]]</a>

The contents specified in [[specialized.algorithms]] are declared in the
header `<memory>`.

Unless otherwise specified, if an exception is thrown in the following
algorithms, objects constructed by a placement *new-expression*
[[expr.new]] are destroyed in an unspecified order before allowing the
exception to propagate.

[*Note 1*: When new objects are created by the algorithms specified in
[[specialized.algorithms]], the lifetime ends for any existing objects
(including potentially-overlapping subobjects [[intro.object]]) in
storage that is reused [[basic.life]]. — *end note*]

Some algorithms specified in [[specialized.algorithms]] make use of the
following exposition-only function templates:

``` cpp
template<class T>
  constexpr void* voidify(T& obj) noexcept {
    return addressof(obj);
  }

template<class I>
  decltype(auto) deref-move(I& it) {
    if constexpr (is_lvalue_reference_v<decltype(*it)>)
      return std::move(*it);
    else
      return *it;
  }
```

### Special memory concepts <a id="special.mem.concepts">[[special.mem.concepts]]</a>

Some algorithms in this subclause are constrained with the following
exposition-only concepts:

``` cpp
template<class I>
concept nothrow-input-iterator = // exposition only
  input_iterator<I> &&
  is_lvalue_reference_v<iter_reference_t<I>> &&
  same_as<remove_cvref_t<iter_reference_t<I>>, iter_value_t<I>>;
```

A type `I` models `nothrow-input-iterator` only if no exceptions are
thrown from increment, copy construction, move construction, copy
assignment, move assignment, or indirection through valid iterators.

[*Note 1*: This concept allows some
`input_iterator`[[iterator.concept.input]] operations to throw
exceptions. — *end note*]

``` cpp
template<class S, class I>
concept nothrow-sentinel-for = sentinel_for<S, I>; // exposition only
```

Types `S` and `I` model `nothrow-sentinel-for` only if no exceptions are
thrown from copy construction, move construction, copy assignment, move
assignment, or comparisons between valid values of type `I` and `S`.

[*Note 2*: This concept allows some
`sentinel_for`[[iterator.concept.sentinel]] operations to throw
exceptions. — *end note*]

``` cpp
template<class S, class I>
concept nothrow-sized-sentinel-for = // exposition only
  nothrow-sentinel-for<S, I> &&
  sized_sentinel_for<S, I>;
```

Types `S` and `I` model `nothrow-sized-sentinel-for` only if no
exceptions are thrown from the `-` operator for valid values of type `I`
and `S`.

[*Note 3*: This concept allows some
`sized_sentinel_for`[[iterator.concept.sizedsentinel]] operations to
throw exceptions. — *end note*]

``` cpp
template<class R>
concept nothrow-input-range = // exposition only
  range<R> &&
  nothrow-input-iterator<iterator_t<R>> &&
  nothrow-sentinel-for<sentinel_t<R>, iterator_t<R>>;
```

A type `R` models `nothrow-input-range` only if no exceptions are thrown
from calls to `ranges::begin` and `ranges::end` on an object of type
`R`.

``` cpp
template<class I>
concept nothrow-forward-iterator = // exposition only
  nothrow-input-iterator<I> &&
  forward_iterator<I> &&
  nothrow-sentinel-for<I, I>;
```

[*Note 4*: This concept allows some
`forward_iterator`[[iterator.concept.forward]] operations to throw
exceptions. — *end note*]

``` cpp
template<class R>
concept nothrow-forward-range = // exposition only
  nothrow-input-range<R> &&
  nothrow-forward-iterator<iterator_t<R>>;
```

``` cpp
template<class I>
concept nothrow-bidirectional-iterator = // exposition only
  nothrow-forward-iterator<I> &&
  bidirectional_iterator<I>;
```

A type `I` models `nothrow-bidirectional-iterator` only if no exceptions
are thrown from decrementing valid iterators.

[*Note 5*: This concept allows some
`bidirectional_iterator`[[iterator.concept.bidir]] operations to throw
exceptions. — *end note*]

``` cpp
template<class R>
concept nothrow-bidirectional-range = // exposition only
  nothrow-forward-range<R> &&
  nothrow-bidirectional-iterator<iterator_t<R>>;
```

``` cpp
template<class I>
concept nothrow-random-access-iterator = // exposition only
  nothrow-bidirectional-iterator<I> &&
  random_access_iterator<I> &&
  nothrow-sized-sentinel-for<I, I>;
```

A type `I` models `nothrow-random-access-iterator` only if no exceptions
are thrown from comparisons of valid iterators, or the `-`, `+`, `-=`,
`+=`, `[]` operators on valid values of type `I` and
`iter_difference_t<I>`.

[*Note 6*: This concept allows some
`random_access_iterator`[[iterator.concept.random.access]] operations to
throw exceptions. — *end note*]

``` cpp
template<class R>
concept nothrow-random-access-range = // exposition only
  nothrow-bidirectional-range<R> &&
  nothrow-random-access-iterator<iterator_t<R>>;

template<class R>
concept nothrow-sized-random-access-range = // exposition only
  nothrow-random-access-range<R> && sized_range<R>;
```

A type `R` models `nothrow-sized-random-access-range` only if no
exceptions are thrown from the call to `ranges::size` on an object of
type `R`.

### `uninitialized_default_construct` <a id="uninitialized.construct.default">[[uninitialized.construct.default]]</a>

``` cpp
template<class NoThrowForwardIterator>
  constexpr void uninitialized_default_construct(NoThrowForwardIterator first,
                                                 NoThrowForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (voidify(*first))
    typename iterator_traits<NoThrowForwardIterator>::value_type;
```

``` cpp
namespace ranges {
  template<nothrow-forward-iterator I, nothrow-sentinel-for<I> S>
    requires default_initializable<iter_value_t<I>>
    constexpr I uninitialized_default_construct(I first, S last);
  template<nothrow-forward-range R>
    requires default_initializable<range_value_t<R>>
    constexpr borrowed_iterator_t<R> uninitialized_default_construct(R&& r);
}
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (voidify(*first)) remove_reference_t<iter_reference_t<I>>;
return first;
```

``` cpp
template<class NoThrowForwardIterator, class Size>
  constexpr NoThrowForwardIterator
    uninitialized_default_construct_n(NoThrowForwardIterator first, Size n);
```

*Effects:* Equivalent to:

``` cpp
for (; n > 0; (void)++first, --n)
  ::new (voidify(*first))
    typename iterator_traits<NoThrowForwardIterator>::value_type;
return first;
```

``` cpp
namespace ranges {
  template<nothrow-forward-iterator I>
    requires default_initializable<iter_value_t<I>>
    constexpr I uninitialized_default_construct_n(I first, iter_difference_t<I> n);
}
```

*Effects:* Equivalent to:

``` cpp
return uninitialized_default_construct(counted_iterator(first, n),
                                       default_sentinel).base();
```

### `uninitialized_value_construct` <a id="uninitialized.construct.value">[[uninitialized.construct.value]]</a>

``` cpp
template<class NoThrowForwardIterator>
  constexpr void uninitialized_value_construct(NoThrowForwardIterator first,
                                               NoThrowForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (voidify(*first))
    typename iterator_traits<NoThrowForwardIterator>::value_type();
```

``` cpp
namespace ranges {
  template<nothrow-forward-iterator I, nothrow-sentinel-for<I> S>
    requires default_initializable<iter_value_t<I>>
    constexpr I uninitialized_value_construct(I first, S last);
  template<nothrow-forward-range R>
    requires default_initializable<range_value_t<R>>
    constexpr borrowed_iterator_t<R> uninitialized_value_construct(R&& r);
}
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (voidify(*first)) remove_reference_t<iter_reference_t<I>>();
return first;
```

``` cpp
template<class NoThrowForwardIterator, class Size>
  constexpr NoThrowForwardIterator
    uninitialized_value_construct_n(NoThrowForwardIterator first, Size n);
```

*Effects:* Equivalent to:

``` cpp
for (; n > 0; (void)++first, --n)
  ::new (voidify(*first))
    typename iterator_traits<NoThrowForwardIterator>::value_type();
return first;
```

``` cpp
namespace ranges {
  template<nothrow-forward-iterator I>
    requires default_initializable<iter_value_t<I>>
    constexpr I uninitialized_value_construct_n(I first, iter_difference_t<I> n);
}
```

*Effects:* Equivalent to:

``` cpp
return uninitialized_value_construct(counted_iterator(first, n),
                                     default_sentinel).base();
```

### `uninitialized_copy` <a id="uninitialized.copy">[[uninitialized.copy]]</a>

``` cpp
template<class InputIterator, class NoThrowForwardIterator>
  constexpr NoThrowForwardIterator uninitialized_copy(InputIterator first, InputIterator last,
                                                      NoThrowForwardIterator result);
```

*Preconditions:* `result`+\[0, `(last - first)`) does not overlap with
\[`first`, `last`).

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++result, (void)++first)
  ::new (voidify(*result))
    typename iterator_traits<NoThrowForwardIterator>::value_type(*first);
```

*Returns:* `result`.

``` cpp
namespace ranges {
  template<input_iterator I, sentinel_for<I> S1,
           nothrow-forward-iterator O, nothrow-sentinel-for<O> S2>
    requires constructible_from<iter_value_t<O>, iter_reference_t<I>>
    constexpr uninitialized_copy_result<I, O>
      uninitialized_copy(I ifirst, S1 ilast, O ofirst, S2 olast);
  template<input_range IR, nothrow-forward-range OR>
    requires constructible_from<range_value_t<OR>, range_reference_t<IR>>
    constexpr uninitialized_copy_result<borrowed_iterator_t<IR>, borrowed_iterator_t<OR>>
      uninitialized_copy(IR&& in_range, OR&& out_range);
}
```

*Preconditions:* \[`ofirst`, `olast`) does not overlap with \[`ifirst`,
`ilast`).

*Effects:* Equivalent to:

``` cpp
for (; ifirst != ilast && ofirst != olast; ++ofirst, (void)++ifirst)
  ::new (voidify(*ofirst)) remove_reference_t<iter_reference_t<O>>(*ifirst);
return {std::move(ifirst), ofirst};
```

``` cpp
template<class InputIterator, class Size, class NoThrowForwardIterator>
  constexpr NoThrowForwardIterator uninitialized_copy_n(InputIterator first, Size n,
                                                        NoThrowForwardIterator result);
```

*Preconditions:* `result`+\[0, `n`) does not overlap with `first`+\[0,
`n`).

*Effects:* Equivalent to:

``` cpp
for (; n > 0; ++result, (void)++first, --n)
  ::new (voidify(*result))
    typename iterator_traits<NoThrowForwardIterator>::value_type(*first);
```

*Returns:* `result`.

``` cpp
namespace ranges {
  template<input_iterator I, nothrow-forward-iterator O, nothrow-sentinel-for<O> S>
    requires constructible_from<iter_value_t<O>, iter_reference_t<I>>
    constexpr uninitialized_copy_n_result<I, O>
      uninitialized_copy_n(I ifirst, iter_difference_t<I> n, O ofirst, S olast);
}
```

*Preconditions:* \[`ofirst`, `olast`) does not overlap with
`ifirst`+\[0, `n`).

*Effects:* Equivalent to:

``` cpp
auto t = uninitialized_copy(counted_iterator(std::move(ifirst), n),
                            default_sentinel, ofirst, olast);
return {std::move(t.in).base(), t.out};
```

### `uninitialized_move` <a id="uninitialized.move">[[uninitialized.move]]</a>

``` cpp
template<class InputIterator, class NoThrowForwardIterator>
  constexpr NoThrowForwardIterator uninitialized_move(InputIterator first, InputIterator last,
                                                      NoThrowForwardIterator result);
```

*Preconditions:* `result`+\[0, `(last - first)`) does not overlap with
\[`first`, `last`).

*Effects:* Equivalent to:

``` cpp
for (; first != last; (void)++result, ++first)
  ::new (voidify(*result))
    typename iterator_traits<NoThrowForwardIterator>::value_type(deref-move(first));
return result;
```

``` cpp
namespace ranges {
  template<input_iterator I, sentinel_for<I> S1,
           nothrow-forward-iterator O, nothrow-sentinel-for<O> S2>
    requires constructible_from<iter_value_t<O>, iter_rvalue_reference_t<I>>
    constexpr uninitialized_move_result<I, O>
      uninitialized_move(I ifirst, S1 ilast, O ofirst, S2 olast);
  template<input_range IR, nothrow-forward-range OR>
    requires constructible_from<range_value_t<OR>, range_rvalue_reference_t<IR>>
    constexpr uninitialized_move_result<borrowed_iterator_t<IR>, borrowed_iterator_t<OR>>
      uninitialized_move(IR&& in_range, OR&& out_range);
}
```

*Preconditions:* \[`ofirst`, `olast`) does not overlap with \[`ifirst`,
`ilast`).

*Effects:* Equivalent to:

``` cpp
for (; ifirst != ilast && ofirst != olast; ++ofirst, (void)++ifirst)
  ::new (voidify(*ofirst))
    remove_reference_t<iter_reference_t<O>>(ranges::iter_move(ifirst));
return {std::move(ifirst), ofirst};
```

[*Note 1*: If an exception is thrown, some objects in the range
\[`ifirst`, `ilast`) are left in a valid, but unspecified
state. — *end note*]

``` cpp
template<class InputIterator, class Size, class NoThrowForwardIterator>
  constexpr pair<InputIterator, NoThrowForwardIterator>
    uninitialized_move_n(InputIterator first, Size n, NoThrowForwardIterator result);
```

*Preconditions:* `result`+\[0, `n`) does not overlap with `first`+\[0,
`n`).

*Effects:* Equivalent to:

``` cpp
for (; n > 0; ++result, (void)++first, --n)
  ::new (voidify(*result))
    typename iterator_traits<NoThrowForwardIterator>::value_type(deref-move(first));
return {first, result};
```

``` cpp
namespace ranges {
  template<input_iterator I, nothrow-forward-iterator O, nothrow-sentinel-for<O> S>
    requires constructible_from<iter_value_t<O>, iter_rvalue_reference_t<I>>
    constexpr uninitialized_move_n_result<I, O>
      uninitialized_move_n(I ifirst, iter_difference_t<I> n, O ofirst, S olast);
}
```

*Preconditions:* \[`ofirst`, `olast`) does not overlap with
`ifirst`+\[0, `n`).

*Effects:* Equivalent to:

``` cpp
auto t = uninitialized_move(counted_iterator(std::move(ifirst), n),
                            default_sentinel, ofirst, olast);
return {std::move(t.in).base(), t.out};
```

[*Note 2*: If an exception is thrown, some objects in the range
`ifirst`+\[0, `n`) are left in a valid but unspecified
state. — *end note*]

### `uninitialized_fill` <a id="uninitialized.fill">[[uninitialized.fill]]</a>

``` cpp
template<class NoThrowForwardIterator, class T>
  constexpr void uninitialized_fill(NoThrowForwardIterator first,
                                    NoThrowForwardIterator last, const T& x);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (voidify(*first))
    typename iterator_traits<NoThrowForwardIterator>::value_type(x);
```

``` cpp
namespace ranges {
  template<nothrow-forward-iterator I, nothrow-sentinel-for<I> S, class T>
    requires constructible_from<iter_value_t<I>, const T&>
    constexpr I uninitialized_fill(I first, S last, const T& x);
  template<nothrow-forward-range R, class T>
    requires constructible_from<range_value_t<R>, const T&>
    constexpr borrowed_iterator_t<R> uninitialized_fill(R&& r, const T& x);
}
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (voidify(*first)) remove_reference_t<iter_reference_t<I>>(x);
return first;
```

``` cpp
template<class NoThrowForwardIterator, class Size, class T>
  constexpr NoThrowForwardIterator
    uninitialized_fill_n(NoThrowForwardIterator first, Size n, const T& x);
```

*Effects:* Equivalent to:

``` cpp
for (; n--; ++first)
  ::new (voidify(*first))
    typename iterator_traits<NoThrowForwardIterator>::value_type(x);
return first;
```

``` cpp
namespace ranges {
  template<nothrow-forward-iterator I, class T>
    requires constructible_from<iter_value_t<I>, const T&>
    constexpr I uninitialized_fill_n(I first, iter_difference_t<I> n, const T& x);
}
```

*Effects:* Equivalent to:

``` cpp
return uninitialized_fill(counted_iterator(first, n), default_sentinel, x).base();
```

### `construct_at` <a id="specialized.construct">[[specialized.construct]]</a>

``` cpp
template<class T, class... Args>
  constexpr T* construct_at(T* location, Args&&... args);

namespace ranges {
  template<class T, class... Args>
    constexpr T* construct_at(T* location, Args&&... args);
}
```

*Constraints:* `is_unbounded_array_v<T>` is `false`. The expression
`::new (declval<void*>()) T(declval<Args>()...)` is well-formed when
treated as an unevaluated operand [[term.unevaluated.operand]].

*Mandates:* If `is_array_v<T>` is `true`, `sizeof...(Args)` is zero.

*Effects:* Equivalent to:

``` cpp
if constexpr (is_array_v<T>)
  return ::new (voidify(*location)) T[1]();
else
  return ::new (voidify(*location)) T(std::forward<Args>(args)...);
```

### `destroy` <a id="specialized.destroy">[[specialized.destroy]]</a>

``` cpp
template<class T>
  constexpr void destroy_at(T* location);
namespace ranges {
  template<destructible T>
    constexpr void destroy_at(T* location) noexcept;
}
```

*Effects:*

- If `T` is an array type, equivalent to
  `destroy(begin(*location), end(*location))`.
- Otherwise, equivalent to `location->T̃()`.

``` cpp
template<class NoThrowForwardIterator>
  constexpr void destroy(NoThrowForwardIterator first, NoThrowForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  destroy_at(addressof(*first));
```

``` cpp
namespace ranges {
  template<nothrow-input-iterator I, nothrow-sentinel-for<I> S>
    requires destructible<iter_value_t<I>>
    constexpr I destroy(I first, S last) noexcept;
  template<nothrow-input-range R>
    requires destructible<range_value_t<R>>
    constexpr borrowed_iterator_t<R> destroy(R&& r) noexcept;
}
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  destroy_at(addressof(*first));
return first;
```

``` cpp
template<class NoThrowForwardIterator, class Size>
  constexpr NoThrowForwardIterator destroy_n(NoThrowForwardIterator first, Size n);
```

*Effects:* Equivalent to:

``` cpp
for (; n > 0; (void)++first, --n)
  destroy_at(addressof(*first));
return first;
```

``` cpp
namespace ranges {
  template<nothrow-input-iterator I>
    requires destructible<iter_value_t<I>>
    constexpr I destroy_n(I first, iter_difference_t<I> n) noexcept;
}
```

*Effects:* Equivalent to:

``` cpp
return destroy(counted_iterator(std::move(first), n), default_sentinel).base();
```

## Specialized `<random>` algorithms <a id="alg.rand">[[alg.rand]]</a>

### General <a id="alg.rand.general">[[alg.rand.general]]</a>

The contents specified in [[alg.rand]] are declared in the header
`<random>`.

### `generate_random` <a id="alg.rand.generate">[[alg.rand.generate]]</a>

``` cpp
template<class R, class G>
  requires output_range<R, invoke_result_t<G&>> && uniform_random_bit_generator<remove_cvref_t<G>>
constexpr borrowed_iterator_t<R> ranges::generate_random(R&& r, G&& g);
```

*Effects:*

- Calls `g.generate_random(std::forward<R>(r))` if this expression is
  well-formed.
- Otherwise, if `R` models `sized_range`, fills `r` with
  `ranges::size(r)` values of type `invoke_result_t<G&>` by performing
  an unspecified number of invocations of the form `g()` or
  `g.generate_random(s)`, if such an expression is well-formed for a
  value `N` and an object `s` of type `span<invoke_result_t<G&>, N>`.
  \[*Note 3*: Values of `N` can differ between
  invocations. — *end note*]
- Otherwise, calls `ranges::generate(std::forward<R>(r), ref(g))`.

*Returns:* `ranges::end(r)`.

*Remarks:* The effects of `generate_random(r, g)` shall be equivalent to
`ranges::generate(std::forward<R>(r), ref(g))`.

[*Note 1*: This implies that `g.generate_random(a)` fills `a` with the
same values as produced by invocation of `g()`. — *end note*]

``` cpp
template<class G, output_iterator<invoke_result_t<G&>> O, sentinel_for<O> S>
  requires uniform_random_bit_generator<remove_cvref_t<G>>
constexpr O ranges::generate_random(O first, S last, G&& g);
```

*Effects:* Equivalent to:

``` cpp
return generate_random(subrange<O, S>(std::move(first), last), g);
```

``` cpp
template<class R, class G, class D>
  requires output_range<R, invoke_result_t<D&, G&>> && invocable<D&, G&> &&
           uniform_random_bit_generator<remove_cvref_t<G>> &&
           is_arithmetic_v<invoke_result_t<D&, G&>>
constexpr borrowed_iterator_t<R> ranges::generate_random(R&& r, G&& g, D&& d);
```

*Effects:*

- Calls `d.generate_random(std::forward<R>(r), g)` if this expression is
  well-formed.
- Otherwise, if `R` models `sized_range`, fills `r` with
  `ranges::size(r)` values of type `invoke_result_t<D&, G&>` by
  performing an unspecified number of invocations of the form
  `invoke(d, g)` or `d.generate_random(s, g)`, if such an expression is
  well-formed for a value `N` and an object `s` of type
  `span<invoke_result_t<D&, G&>, N>`. \[*Note 4*: Values of N can differ
  between invocations. — *end note*]
- Otherwise, calls
  ``` cpp
  ranges::generate(std::forward<R>(r), [&d, &g] { return invoke(d, g); });
  ```

*Returns:* `ranges::end(r)`.

*Remarks:* The effects of `generate_random(r, g, d)` shall be equivalent
to

``` cpp
ranges::generate(std::forward<R>(r), [&d, &g] { return invoke(d, g); })
```

[*Note 2*: This implies that `d.generate_random(a, g)` fills `a` with
the values with the same random distribution as produced by invocation
of `invoke(d, g)`. — *end note*]

``` cpp
template<class G, class D, output_iterator<invoke_result_t<D&, G&>> O, sentinel_for<O> S>
  requires invocable<D&, G&> && uniform_random_bit_generator<remove_cvref_t<G>> &&
           is_arithmetic_v<invoke_result_t<D&, G&>>
constexpr O ranges::generate_random(O first, S last, G&& g, D&& d);
```

*Effects:* Equivalent to:

``` cpp
return generate_random(subrange<O, S>(std::move(first), last), g, d);
```

## C library algorithms <a id="alg.c.library">[[alg.c.library]]</a>

[*Note 1*: The header `<cstdlib>` declares the functions described in
this subclause. — *end note*]

``` cpp
void* bsearch(const void* key, void* base, size_t nmemb, size_t size,
              c-compare-pred* compar);
void* bsearch(const void* key, void* base, size_t nmemb, size_t size,
              compare-pred* compar);
const void* bsearch(const void* key, const void* base, size_t nmemb, size_t size,
                    c-compare-pred* compar);
const void* bsearch(const void* key, const void* base, size_t nmemb, size_t size,
                    compare-pred* compar);
void qsort(void* base, size_t nmemb, size_t size, c-compare-pred* compar);
void qsort(void* base, size_t nmemb, size_t size, compare-pred* compar);
```

*Preconditions:* For `qsort`, the objects in the array pointed to by
`base` are of trivially copyable type.

*Effects:* These functions have the semantics specified in the C
standard library.

*Throws:* Any exception thrown by `compar`[[res.on.exception.handling]].

<!-- Link reference definitions -->
[accumulate]: #accumulate
[adjacent.difference]: #adjacent.difference
[alg.adjacent.find]: #alg.adjacent.find
[alg.all.of]: #alg.all.of
[alg.any.of]: #alg.any.of
[alg.binary.search]: #alg.binary.search
[alg.binary.search.general]: #alg.binary.search.general
[alg.c.library]: #alg.c.library
[alg.clamp]: #alg.clamp
[alg.contains]: #alg.contains
[alg.copy]: #alg.copy
[alg.count]: #alg.count
[alg.ends.with]: #alg.ends.with
[alg.equal]: #alg.equal
[alg.fill]: #alg.fill
[alg.find]: #alg.find
[alg.find.end]: #alg.find.end
[alg.find.first.of]: #alg.find.first.of
[alg.find.last]: #alg.find.last
[alg.fold]: #alg.fold
[alg.foreach]: #alg.foreach
[alg.func.obj]: library.md#alg.func.obj
[alg.generate]: #alg.generate
[alg.heap.operations]: #alg.heap.operations
[alg.heap.operations.general]: #alg.heap.operations.general
[alg.is.permutation]: #alg.is.permutation
[alg.lex.comparison]: #alg.lex.comparison
[alg.merge]: #alg.merge
[alg.min.max]: #alg.min.max
[alg.mismatch]: #alg.mismatch
[alg.modifying.operations]: #alg.modifying.operations
[alg.move]: #alg.move
[alg.none.of]: #alg.none.of
[alg.nonmodifying]: #alg.nonmodifying
[alg.nth.element]: #alg.nth.element
[alg.partitions]: #alg.partitions
[alg.permutation.generators]: #alg.permutation.generators
[alg.rand]: #alg.rand
[alg.rand.general]: #alg.rand.general
[alg.rand.generate]: #alg.rand.generate
[alg.random.sample]: #alg.random.sample
[alg.random.shuffle]: #alg.random.shuffle
[alg.remove]: #alg.remove
[alg.replace]: #alg.replace
[alg.reverse]: #alg.reverse
[alg.rotate]: #alg.rotate
[alg.search]: #alg.search
[alg.set.operations]: #alg.set.operations
[alg.set.operations.general]: #alg.set.operations.general
[alg.shift]: #alg.shift
[alg.sort]: #alg.sort
[alg.sorting]: #alg.sorting
[alg.sorting.general]: #alg.sorting.general
[alg.starts.with]: #alg.starts.with
[alg.swap]: #alg.swap
[alg.three.way]: #alg.three.way
[alg.transform]: #alg.transform
[alg.unique]: #alg.unique
[algorithm.stable]: library.md#algorithm.stable
[algorithm.syn]: #algorithm.syn
[algorithms]: #algorithms
[algorithms.general]: #algorithms.general
[algorithms.parallel]: #algorithms.parallel
[algorithms.parallel.defns]: #algorithms.parallel.defns
[algorithms.parallel.exceptions]: #algorithms.parallel.exceptions
[algorithms.parallel.exec]: #algorithms.parallel.exec
[algorithms.parallel.overloads]: #algorithms.parallel.overloads
[algorithms.parallel.user]: #algorithms.parallel.user
[algorithms.requirements]: #algorithms.requirements
[algorithms.results]: #algorithms.results
[algorithms.summary]: #algorithms.summary
[atomics.order]: thread.md#atomics.order
[basic.compound]: basic.md#basic.compound
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[bidirectional.iterators]: iterators.md#bidirectional.iterators
[binary.search]: #binary.search
[concept.booleantestable]: concepts.md#concept.booleantestable
[containers]: containers.md#containers
[conv.integral,class.conv]: #conv.integral,class.conv
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.lessthancomparable]: #cpp17.lessthancomparable
[cpp17.moveassignable]: #cpp17.moveassignable
[cpp17.moveconstructible]: #cpp17.moveconstructible
[equal.range]: #equal.range
[except.terminate]: except.md#except.terminate
[exclusive.scan]: #exclusive.scan
[execpol]: #execpol
[execpol.general]: #execpol.general
[execpol.objects]: #execpol.objects
[execpol.par]: #execpol.par
[execpol.parunseq]: #execpol.parunseq
[execpol.seq]: #execpol.seq
[execpol.type]: #execpol.type
[execpol.unseq]: #execpol.unseq
[expr.const]: expr.md#expr.const
[expr.new]: expr.md#expr.new
[forward.iterators]: iterators.md#forward.iterators
[function.objects]: utilities.md#function.objects
[includes]: #includes
[inclusive.scan]: #inclusive.scan
[inner.product]: #inner.product
[input.iterators]: iterators.md#input.iterators
[intro.execution]: basic.md#intro.execution
[intro.object]: basic.md#intro.object
[intro.progress]: basic.md#intro.progress
[is.heap]: #is.heap
[is.sorted]: #is.sorted
[iterator.concept.bidir]: iterators.md#iterator.concept.bidir
[iterator.concept.forward]: iterators.md#iterator.concept.forward
[iterator.concept.input]: iterators.md#iterator.concept.input
[iterator.concept.random.access]: iterators.md#iterator.concept.random.access
[iterator.concept.sentinel]: iterators.md#iterator.concept.sentinel
[iterator.concept.sizedsentinel]: iterators.md#iterator.concept.sizedsentinel
[iterator.requirements]: iterators.md#iterator.requirements
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[lower.bound]: #lower.bound
[make.heap]: #make.heap
[multiset]: containers.md#multiset
[numeric.iota]: #numeric.iota
[numeric.ops]: #numeric.ops
[numeric.ops.gcd]: #numeric.ops.gcd
[numeric.ops.general]: #numeric.ops.general
[numeric.ops.lcm]: #numeric.ops.lcm
[numeric.ops.midpoint]: #numeric.ops.midpoint
[numeric.ops.overview]: #numeric.ops.overview
[numeric.sat]: #numeric.sat
[numeric.sat.cast]: #numeric.sat.cast
[numeric.sat.func]: #numeric.sat.func
[numerics.defns]: #numerics.defns
[output.iterators]: iterators.md#output.iterators
[partial.sort]: #partial.sort
[partial.sort.copy]: #partial.sort.copy
[partial.sum]: #partial.sum
[pop.heap]: #pop.heap
[push.heap]: #push.heap
[rand.req.urng]: numerics.md#rand.req.urng
[random.access.iterators]: iterators.md#random.access.iterators
[range.range]: ranges.md#range.range
[reduce]: #reduce
[refwrap]: utilities.md#refwrap
[res.on.exception.handling]: library.md#res.on.exception.handling
[set.difference]: #set.difference
[set.intersection]: #set.intersection
[set.symmetric.difference]: #set.symmetric.difference
[set.union]: #set.union
[sort]: #sort
[sort.heap]: #sort.heap
[special.mem.concepts]: #special.mem.concepts
[specialized.algorithms]: #specialized.algorithms
[specialized.algorithms.general]: #specialized.algorithms.general
[specialized.construct]: #specialized.construct
[specialized.destroy]: #specialized.destroy
[stable.sort]: #stable.sort
[swappable.requirements]: library.md#swappable.requirements
[term.unevaluated.operand]: expr.md#term.unevaluated.operand
[thread.jthread.class]: thread.md#thread.jthread.class
[thread.thread.class]: thread.md#thread.thread.class
[transform.exclusive.scan]: #transform.exclusive.scan
[transform.inclusive.scan]: #transform.inclusive.scan
[transform.reduce]: #transform.reduce
[uninitialized.construct.default]: #uninitialized.construct.default
[uninitialized.construct.value]: #uninitialized.construct.value
[uninitialized.copy]: #uninitialized.copy
[uninitialized.fill]: #uninitialized.fill
[uninitialized.move]: #uninitialized.move
[upper.bound]: #upper.bound

[^1]: The decision whether to include a copying version was usually
    based on complexity considerations. When the cost of doing the
    operation dominates the cost of copy, the copying version is not
    included. For example, `sort_copy` is not included because the cost
    of sorting is much more significant, and users can invoke `copy`
    followed by `sort`.

[^2]: `copy_backward` can be used instead of `copy` when `last` is in
    the range \[`result - `N, `result`).

[^3]: `move_backward` can be used instead of `move` when `last` is in
    the range \[`result - `N, `result`).

[^4]: The use of fully closed ranges is intentional.

[^5]: This behavior intentionally differs from `max_element`.

[^6]: The use of fully closed ranges is intentional.

[^7]: `accumulate` is similar to the APL reduction operator and Common
    Lisp reduce function, but it avoids the difficulty of defining the
    result of reduction on an empty sequence by always requiring an
    initial value.

[^8]: The use of fully closed ranges is intentional.

[^9]: The use of fully closed ranges is intentional.

[^10]: The use of fully closed ranges is intentional.
