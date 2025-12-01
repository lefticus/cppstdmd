# Thread support library <a id="thread">[[thread]]</a>

## General <a id="thread.general">[[thread.general]]</a>

The following subclauses describe components to create and manage
threads ([[intro.multithread]]), perform mutual exclusion, and
communicate conditions and values between threads, as summarized in
Table  [[tab:thread.lib.summary]].

**Table: Thread support library summary** <a id="tab:thread.lib.summary">[tab:thread.lib.summary]</a>

| Subclause            |                     | Header                 |
| -------------------- | ------------------- | ---------------------- |
| [[thread.req]]       | Requirements        |                        |
| [[thread.threads]]   | Threads             | `<thread>`             |
| [[thread.mutex]]     | Mutual exclusion    | `<mutex>`              |
|                      |                     | `<shared_mutex>`       |
| [[thread.condition]] | Condition variables | `<condition_variable>` |
| [[futures]]          | Futures             | `<future>`             |


## Requirements <a id="thread.req">[[thread.req]]</a>

### Template parameter names <a id="thread.req.paramname">[[thread.req.paramname]]</a>

Throughout this Clause, the names of template parameters are used to
express type requirements. If a template parameter is named `Predicate`,
`operator()` applied to the template argument shall return a value that
is convertible to `bool`.

### Exceptions <a id="thread.req.exception">[[thread.req.exception]]</a>

Some functions described in this Clause are specified to throw
exceptions of type `system_error` ([[syserr.syserr]]). Such exceptions
shall be thrown if any of the function’s error conditions is detected or
a call to an operating system or other underlying API results in an
error that prevents the library function from meeting its
specifications. Failure to allocate storage shall be reported as
described in  [[res.on.exception.handling]].

[*Example 1*: Consider a function in this clause that is specified to
throw exceptions of type `system_error` and specifies error conditions
that include `operation_not_permitted` for a thread that does not have
the privilege to perform the operation. Assume that, during the
execution of this function, an `errno` of `EPERM` is reported by a POSIX
API call used by the implementation. Since POSIX specifies an `errno` of
`EPERM` when “the caller does not have the privilege to perform the
operation”, the implementation maps `EPERM` to an `error_condition` of
`operation_not_permitted` ([[syserr]]) and an exception of type
`system_error` is thrown. — *end example*]

The `error_code` reported by such an exception’s `code()` member
function shall compare equal to one of the conditions specified in the
function’s error condition element.

### Native handles <a id="thread.req.native">[[thread.req.native]]</a>

Several classes described in this Clause have members
`native_handle_type` and `native_handle`. The presence of these members
and their semantics is *implementation-defined*.

[*Note 1*: These members allow implementations to provide access to
implementation details. Their names are specified to facilitate portable
compile-time detection. Actual use of these members is inherently
non-portable. — *end note*]

### Timing specifications <a id="thread.req.timing">[[thread.req.timing]]</a>

Several functions described in this Clause take an argument to specify a
timeout. These timeouts are specified as either a `duration` or a
`time_point` type as specified in  [[time]].

Implementations necessarily have some delay in returning from a timeout.
Any overhead in interrupt response, function return, and scheduling
induces a “quality of implementation” delay, expressed as duration Dᵢ.
Ideally, this delay would be zero. Further, any contention for processor
and memory resources induces a “quality of management” delay, expressed
as duration Dₘ. The delay durations may vary from timeout to timeout,
but in all cases shorter is better.

The member functions whose names end in `_for` take an argument that
specifies a duration. These functions produce relative timeouts.
Implementations should use a steady clock to measure time for these
functions.[^1] Given a duration argument Dₜ, the real-time duration of
the timeout is Dₜ + Dᵢ + Dₘ.

The member functions whose names end in `_until` take an argument that
specifies a time point. These functions produce absolute timeouts.
Implementations should use the clock specified in the time point to
measure time for these functions. Given a clock time point argument Cₜ,
the clock time point of the return from timeout should be Cₜ + Dᵢ + Dₘ
when the clock is not adjusted during the timeout. If the clock is
adjusted to the time Cₐ during the timeout, the behavior should be as
follows:

- if Cₐ > Cₜ, the waiting function should wake as soon as possible, i.e.
  Cₐ + Dᵢ + Dₘ, since the timeout is already satisfied. \[*Note 1*: This
  specification may result in the total duration of the wait decreasing
  when measured against a steady clock. — *end note*]
- if Cₐ <= Cₜ, the waiting function should not time out until
  `Clock::now()` returns a time Cₙ >= Cₜ, i.e. waking at Cₜ + Dᵢ + Dₘ.
  \[*Note 2*: When the clock is adjusted backwards, this specification
  may result in the total duration of the wait increasing when measured
  against a steady clock. When the clock is adjusted forwards, this
  specification may result in the total duration of the wait decreasing
  when measured against a steady clock. — *end note*]

An implementation shall return from such a timeout at any point from the
time specified above to the time it would return from a steady-clock
relative timeout on the difference between Cₜ and the time point of the
call to the `_until` function.

[*Note 3*: Implementations should decrease the duration of the wait
when the clock is adjusted forwards. — *end note*]

[*Note 4*: If the clock is not synchronized with a steady clock, e.g.,
a CPU time clock, these timeouts might not provide useful
functionality. — *end note*]

The resolution of timing provided by an implementation depends on both
operating system and hardware. The finest resolution provided by an
implementation is called the *native resolution*.

Implementation-provided clocks that are used for these functions shall
meet the `TrivialClock` requirements ([[time.clock.req]]).

A function that takes an argument which specifies a timeout will throw
if, during its execution, a clock, time point, or time duration throws
an exception. Such exceptions are referred to as *timeout-related
exceptions*.

[*Note 5*: Instantiations of clock, time point and duration types
supplied by the implementation as specified in  [[time.clock]] do not
throw exceptions. — *end note*]

### Requirements for `Lockable` types <a id="thread.req.lockable">[[thread.req.lockable]]</a>

#### In general <a id="thread.req.lockable.general">[[thread.req.lockable.general]]</a>

An *execution agent* is an entity such as a thread that may perform work
in parallel with other execution agents.

[*Note 1*: Implementations or users may introduce other kinds of agents
such as processes or thread-pool tasks. — *end note*]

The calling agent is determined by context, e.g. the calling thread that
contains the call, and so on.

[*Note 2*: Some lockable objects are “agent oblivious” in that they
work for any execution agent model because they do not determine or
store the agent’s ID (e.g., an ordinary spin lock). — *end note*]

The standard library templates `unique_lock` ([[thread.lock.unique]]),
`shared_lock` ([[thread.lock.shared]]), `scoped_lock` (
[[thread.lock.scoped]]), `lock_guard` ([[thread.lock.guard]]), `lock`,
`try_lock` ([[thread.lock.algorithm]]), and `condition_variable_any` (
[[thread.condition.condvarany]]) all operate on user-supplied lockable
objects. The `BasicLockable` requirements, the `Lockable` requirements,
and the `TimedLockable` requirements list the requirements imposed by
these library types in order to acquire or release ownership of a `lock`
by a given execution agent.

[*Note 3*: The nature of any lock ownership and any synchronization it
may entail are not part of these requirements. — *end note*]

#### `BasicLockable` requirements <a id="thread.req.lockable.basic">[[thread.req.lockable.basic]]</a>

A type `L` meets the `BasicLockable` requirements if the following
expressions are well-formed and have the specified semantics (`m`
denotes a value of type `L`).

``` cpp
m.lock()
```

*Effects:* Blocks until a lock can be acquired for the current execution
agent. If an exception is thrown then a lock shall not have been
acquired for the current execution agent.

``` cpp
m.unlock()
```

*Requires:* The current execution agent shall hold a lock on `m`.

*Effects:* Releases a lock on `m` held by the current execution agent.

*Throws:* Nothing.

#### `Lockable` requirements <a id="thread.req.lockable.req">[[thread.req.lockable.req]]</a>

A type `L` meets the `Lockable` requirements if it meets the
`BasicLockable` requirements and the following expressions are
well-formed and have the specified semantics (`m` denotes a value of
type `L`).

``` cpp
m.try_lock()
```

*Effects:* Attempts to acquire a lock for the current execution agent
without blocking. If an exception is thrown then a lock shall not have
been acquired for the current execution agent.

*Return type:* `bool`.

*Returns:* `true` if the lock was acquired, `false` otherwise.

#### `TimedLockable` requirements <a id="thread.req.lockable.timed">[[thread.req.lockable.timed]]</a>

A type `L` meets the `TimedLockable` requirements if it meets the
`Lockable` requirements and the following expressions are well-formed
and have the specified semantics (`m` denotes a value of type `L`,
`rel_time` denotes a value of an instantiation of `duration` (
[[time.duration]]), and `abs_time` denotes a value of an instantiation
of `time_point` ([[time.point]])).

``` cpp
m.try_lock_for(rel_time)
```

*Effects:* Attempts to acquire a lock for the current execution agent
within the relative timeout ([[thread.req.timing]]) specified by
`rel_time`. The function shall not return within the timeout specified
by `rel_time` unless it has obtained a lock on `m` for the current
execution agent. If an exception is thrown then a lock shall not have
been acquired for the current execution agent.

*Return type:* `bool`.

*Returns:* `true` if the lock was acquired, `false` otherwise.

``` cpp
m.try_lock_until(abs_time)
```

*Effects:* Attempts to acquire a lock for the current execution agent
before the absolute timeout ([[thread.req.timing]]) specified by
`abs_time`. The function shall not return before the timeout specified
by `abs_time` unless it has obtained a lock on `m` for the current
execution agent. If an exception is thrown then a lock shall not have
been acquired for the current execution agent.

*Return type:* `bool`.

*Returns:* `true` if the lock was acquired, `false` otherwise.

### `decay_copy` <a id="thread.decaycopy">[[thread.decaycopy]]</a>

In several places in this Clause the operation `DECAY_COPY(x)` is used.
All such uses mean call the function `decay_copy(x)` and use the result,
where `decay_copy` is defined as follows:

``` cpp
template <class T> decay_t<T> decay_copy(T&& v)
  { return std::forward<T>(v); }
```

## Threads <a id="thread.threads">[[thread.threads]]</a>

[[thread.threads]] describes components that can be used to create and
manage threads.

[*Note 1*: These threads are intended to map one-to-one with operating
system threads. — *end note*]

### Header `<thread>` synopsis <a id="thread.syn">[[thread.syn]]</a>

``` cpp
namespace std {
  class thread;

  void swap(thread& x, thread& y) noexcept;

  namespace this_thread {
    thread::id get_id() noexcept;

    void yield() noexcept;
    template <class Clock, class Duration>
      void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
    template <class Rep, class Period>
      void sleep_for(const chrono::duration<Rep, Period>& rel_time);
  }
}
```

### Class `thread` <a id="thread.thread.class">[[thread.thread.class]]</a>

The class `thread` provides a mechanism to create a new thread of
execution, to join with a thread (i.e., wait for a thread to complete),
and to perform other operations that manage and query the state of a
thread. A `thread` object uniquely represents a particular thread of
execution. That representation may be transferred to other `thread`
objects in such a way that no two `thread` objects simultaneously
represent the same thread of execution. A thread of execution is
*detached* when no `thread` object represents that thread. Objects of
class `thread` can be in a state that does not represent a thread of
execution.

[*Note 1*: A `thread` object does not represent a thread of execution
after default construction, after being moved from, or after a
successful call to `detach` or `join`. — *end note*]

``` cpp
namespace std {
  class thread {
  public:
    // types:
    class id;
    using native_handle_type = implementation-defined; // See~[thread.req.native]

    // construct/copy/destroy:
    thread() noexcept;
    template <class F, class... Args> explicit thread(F&& f, Args&&... args);
    ~thread();
    thread(const thread&) = delete;
    thread(thread&&) noexcept;
    thread& operator=(const thread&) = delete;
    thread& operator=(thread&&) noexcept;

    // members:
    void swap(thread&) noexcept;
    bool joinable() const noexcept;
    void join();
    void detach();
    id get_id() const noexcept;
    native_handle_type native_handle(); // See~[thread.req.native]

    // static members:
    static unsigned hardware_concurrency() noexcept;
  };
}
```

#### Class `thread::id` <a id="thread.thread.id">[[thread.thread.id]]</a>

``` cpp
namespace std {
  class thread::id {
  public:
      id() noexcept;
  };

  bool operator==(thread::id x, thread::id y) noexcept;
  bool operator!=(thread::id x, thread::id y) noexcept;
  bool operator<(thread::id x, thread::id y) noexcept;
  bool operator<=(thread::id x, thread::id y) noexcept;
  bool operator>(thread::id x, thread::id y) noexcept;
  bool operator>=(thread::id x, thread::id y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<< (basic_ostream<charT, traits>& out, thread::id id);

  // Hash support
  template <class T> struct hash;
  template <> struct hash<thread::id>;
}
```

An object of type `thread::id` provides a unique identifier for each
thread of execution and a single distinct value for all `thread` objects
that do not represent a thread of execution ([[thread.thread.class]]).
Each thread of execution has an associated `thread::id` object that is
not equal to the `thread::id` object of any other thread of execution
and that is not equal to the `thread::id` object of any `thread` object
that does not represent threads of execution.

`thread::id` shall be a trivially copyable class (Clause  [[class]]).
The library may reuse the value of a `thread::id` of a terminated thread
that can no longer be joined.

[*Note 1*: Relational operators allow `thread::id` objects to be used
as keys in associative containers. — *end note*]

``` cpp
id() noexcept;
```

*Effects:* Constructs an object of type `id`.

*Postconditions:* The constructed object does not represent a thread of
execution.

``` cpp
bool operator==(thread::id x, thread::id y) noexcept;
```

*Returns:* `true` only if `x` and `y` represent the same thread of
execution or neither `x` nor `y` represents a thread of execution.

``` cpp
bool operator!=(thread::id x, thread::id y) noexcept;
```

*Returns:* `!(x == y)`

``` cpp
bool operator<(thread::id x, thread::id y) noexcept;
```

*Returns:* A value such that `operator<` is a total ordering as
described in  [[alg.sorting]].

``` cpp
bool operator<=(thread::id x, thread::id y) noexcept;
```

*Returns:* `!(y < x)`.

``` cpp
bool operator>(thread::id x, thread::id y) noexcept;
```

*Returns:* `y < x`.

``` cpp
bool operator>=(thread::id x, thread::id y) noexcept;
```

*Returns:* `!(x < y)`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<< (basic_ostream<charT, traits>& out, thread::id id);
```

*Effects:* Inserts an unspecified text representation of `id` into
`out`. For two objects of type `thread::id` `x` and `y`, if `x == y` the
`thread::id` objects shall have the same text representation and if
`x != y` the `thread::id` objects shall have distinct text
representations.

*Returns:* `out`.

``` cpp
template <> struct hash<thread::id>;
```

The specialization is enabled ([[unord.hash]]).

#### `thread` constructors <a id="thread.thread.constr">[[thread.thread.constr]]</a>

``` cpp
thread() noexcept;
```

*Effects:* Constructs a `thread` object that does not represent a thread
of execution.

*Postconditions:* `get_id() == id()`.

``` cpp
template <class F, class... Args> explicit thread(F&& f, Args&&... args);
```

*Requires:*  `F` and each `Ti` in `Args` shall satisfy the
`MoveConstructible` requirements.
` `*`INVOKE`*`( `*`DECAY_COPY`*`( std::forward<F>(f)), `*`DECAY_COPY`*`( std::forward<Args>(args))...)` ([[func.require]])
shall be a valid expression.

*Remarks:* This constructor shall not participate in overload resolution
if `decay_t<F>` is the same type as `std::thread`.

*Effects:*  Constructs an object of type `thread`. The new thread of
execution executes
` `*`INVOKE`*`( `*`DECAY_COPY`*`( std::forward<F>(f)), `*`DECAY_COPY`*`( std::forward<Args>(args))...)`
with the calls to *`DECAY_COPY`* being evaluated in the constructing
thread. Any return value from this invocation is ignored.

[*Note 1*: This implies that any exceptions not thrown from the
invocation of the copy of `f` will be thrown in the constructing thread,
not the new thread. — *end note*]

If the invocation of
` `*`INVOKE`*`( `*`DECAY_COPY`*`( std::forward<F>(f)), `*`DECAY_COPY`*`( std::forward<Args>(args))...)`
terminates with an uncaught exception, `terminate` shall be called.

*Synchronization:* The completion of the invocation of the constructor
synchronizes with the beginning of the invocation of the copy of `f`.

*Postconditions:* `get_id() != id()`. `*this` represents the newly
started thread.

*Throws:* `system_error` if unable to start the new thread.

*Error conditions:*

- `resource_unavailable_try_again` — the system lacked the necessary
  resources to create another thread, or the system-imposed limit on the
  number of threads in a process would be exceeded.

``` cpp
thread(thread&& x) noexcept;
```

*Effects:* Constructs an object of type `thread` from `x`, and sets `x`
to a default constructed state.

*Postconditions:* `x.get_id() == id()` and `get_id()` returns the value
of `x.get_id()` prior to the start of construction.

#### `thread` destructor <a id="thread.thread.destr">[[thread.thread.destr]]</a>

``` cpp
~thread();
```

If `joinable()`, calls `terminate()`. Otherwise, has no effects.

[*Note 1*: Either implicitly detaching or joining a `joinable()` thread
in its destructor could result in difficult to debug correctness (for
detach) or performance (for join) bugs encountered only when an
exception is thrown. Thus the programmer must ensure that the destructor
is never executed while the thread is still joinable. — *end note*]

#### `thread` assignment <a id="thread.thread.assign">[[thread.thread.assign]]</a>

``` cpp
thread& operator=(thread&& x) noexcept;
```

*Effects:* If `joinable()`, calls `terminate()`. Otherwise, assigns the
state of `x` to `*this` and sets `x` to a default constructed state.

*Postconditions:* `x.get_id() == id()` and `get_id()` returns the value
of `x.get_id()` prior to the assignment.

*Returns:* `*this`.

#### `thread` members <a id="thread.thread.member">[[thread.thread.member]]</a>

``` cpp
void swap(thread& x) noexcept;
```

*Effects:* Swaps the state of `*this` and `x`.

``` cpp
bool joinable() const noexcept;
```

*Returns:* `get_id() != id()`.

``` cpp
void join();
```

*Effects:*  Blocks until the thread represented by `*this` has
completed.

*Synchronization:* The completion of the thread represented by `*this`
synchronizes with ([[intro.multithread]]) the corresponding successful
`join()` return.

[*Note 1*: Operations on `*this` are not synchronized. — *end note*]

*Postconditions:* The thread represented by `*this` has completed.
`get_id() == id()`.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `resource_deadlock_would_occur` — if deadlock is detected or
  `get_id() == this_thread::get_id()`.
- `no_such_process` — if the thread is not valid.
- `invalid_argument` — if the thread is not joinable.

``` cpp
void detach();
```

*Effects:* The thread represented by `*this` continues execution without
the calling thread blocking. When `detach()` returns, `*this` no longer
represents the possibly continuing thread of execution. When the thread
previously represented by `*this` ends execution, the implementation
shall release any owned resources.

*Postconditions:* `get_id() == id()`.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `no_such_process` — if the thread is not valid.
- `invalid_argument` — if the thread is not joinable.

``` cpp
id get_id() const noexcept;
```

*Returns:* A default constructed `id` object if `*this` does not
represent a thread, otherwise `this_thread::get_id()` for the thread of
execution represented by `*this`.

#### `thread` static members <a id="thread.thread.static">[[thread.thread.static]]</a>

``` cpp
unsigned hardware_concurrency() noexcept;
```

*Returns:* The number of hardware thread contexts.

[*Note 1*: This value should only be considered to be a
hint. — *end note*]

If this value is not computable or well defined an implementation should
return 0.

#### `thread` specialized algorithms <a id="thread.thread.algorithm">[[thread.thread.algorithm]]</a>

``` cpp
void swap(thread& x, thread& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

### Namespace `this_thread` <a id="thread.thread.this">[[thread.thread.this]]</a>

``` cpp
namespace std::this_thread {
  thread::id get_id() noexcept;

  void yield() noexcept;
  template <class Clock, class Duration>
    void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
  template <class Rep, class Period>
    void sleep_for(const chrono::duration<Rep, Period>& rel_time);
}
```

``` cpp
thread::id this_thread::get_id() noexcept;
```

*Returns:* An object of type `thread::id` that uniquely identifies the
current thread of execution. No other thread of execution shall have
this id and this thread of execution shall always have this id. The
object returned shall not compare equal to a default constructed
`thread::id`.

``` cpp
void this_thread::yield() noexcept;
```

*Effects:* Offers the implementation the opportunity to reschedule.

*Synchronization:* None.

``` cpp
template <class Clock, class Duration>
  void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:* Blocks the calling thread for the absolute
timeout ([[thread.req.timing]]) specified by `abs_time`.

*Synchronization:* None.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Rep, class Period>
  void sleep_for(const chrono::duration<Rep, Period>& rel_time);
```

*Effects:* Blocks the calling thread for the relative
timeout ([[thread.req.timing]]) specified by `rel_time`.

*Synchronization:* None.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

## Mutual exclusion <a id="thread.mutex">[[thread.mutex]]</a>

This section provides mechanisms for mutual exclusion: mutexes, locks,
and call once. These mechanisms ease the production of race-free
programs ([[intro.multithread]]).

### Header `<mutex>` synopsis <a id="mutex.syn">[[mutex.syn]]</a>

``` cpp
namespace std {
  class mutex;
  class recursive_mutex;
  class timed_mutex;
  class recursive_timed_mutex;

  struct defer_lock_t { explicit defer_lock_t() = default; };
  struct try_to_lock_t { explicit try_to_lock_t() = default; };
  struct adopt_lock_t { explicit adopt_lock_t() = default; };

  inline constexpr defer_lock_t  defer_lock { };
  inline constexpr try_to_lock_t try_to_lock { };
  inline constexpr adopt_lock_t  adopt_lock { };

  template <class Mutex> class lock_guard;
  template <class... MutexTypes> class scoped_lock;
  template <class Mutex> class unique_lock;

  template <class Mutex>
    void swap(unique_lock<Mutex>& x, unique_lock<Mutex>& y) noexcept;

  template <class L1, class L2, class... L3> int try_lock(L1&, L2&, L3&...);
  template <class L1, class L2, class... L3> void lock(L1&, L2&, L3&...);

  struct once_flag;

  template<class Callable, class... Args>
    void call_once(once_flag& flag, Callable&& func, Args&&... args);
}
```

### Header `<shared_mutex>` synopsis <a id="shared_mutex.syn">[[shared_mutex.syn]]</a>

``` cpp
namespace std {
  class shared_mutex;
  class shared_timed_mutex;
  template <class Mutex> class shared_lock;
  template <class Mutex>
    void swap(shared_lock<Mutex>& x, shared_lock<Mutex>& y) noexcept;
}
```

### Mutex requirements <a id="thread.mutex.requirements">[[thread.mutex.requirements]]</a>

#### In general <a id="thread.mutex.requirements.general">[[thread.mutex.requirements.general]]</a>

A mutex object facilitates protection against data races and allows safe
synchronization of data between execution agents (
[[thread.req.lockable]]). An execution agent *owns* a mutex from the
time it successfully calls one of the lock functions until it calls
unlock. Mutexes can be either recursive or non-recursive, and can grant
simultaneous ownership to one or many execution agents. Both recursive
and non-recursive mutexes are supplied.

#### Mutex types <a id="thread.mutex.requirements.mutex">[[thread.mutex.requirements.mutex]]</a>

The *mutex types* are the standard library types `mutex`,
`recursive_mutex`, `timed_mutex`, `recursive_timed_mutex`,
`shared_mutex`, and `shared_timed_mutex`. They shall meet the
requirements set out in this section. In this description, `m` denotes
an object of a mutex type.

The mutex types shall meet the `Lockable` requirements (
[[thread.req.lockable.req]]).

The mutex types shall be `DefaultConstructible` and `Destructible`. If
initialization of an object of a mutex type fails, an exception of type
`system_error` shall be thrown. The mutex types shall not be copyable or
movable.

The error conditions for error codes, if any, reported by member
functions of the mutex types shall be:

- `resource_unavailable_try_again` — if any native handle type
  manipulated is not available.
- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.
- `invalid_argument` — if any native handle type manipulated as part of
  mutex construction is incorrect.

The implementation shall provide lock and unlock operations, as
described below. For purposes of determining the existence of a data
race, these behave as atomic operations ([[intro.multithread]]). The
lock and unlock operations on a single mutex shall appear to occur in a
single total order.

[*Note 1*: This can be viewed as the modification order (
[[intro.multithread]]) of the mutex. — *end note*]

[*Note 2*: Construction and destruction of an object of a mutex type
need not be thread-safe; other synchronization should be used to ensure
that mutex objects are initialized and visible to other
threads. — *end note*]

The expression `m.lock()` shall be well-formed and have the following
semantics:

*Requires:* If `m` is of type `mutex`, `timed_mutex`, `shared_mutex`, or
`shared_timed_mutex`, the calling thread does not own the mutex.

*Effects:* Blocks the calling thread until ownership of the mutex can be
obtained for the calling thread.

*Postconditions:* The calling thread owns the mutex.

*Return type:* `void`.

*Synchronization:* Prior `unlock()` operations on the same object shall
*synchronize with* ([[intro.multithread]]) this operation.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.
- `resource_deadlock_would_occur` — if the implementation detects that a
  deadlock would occur.

The expression `m.try_lock()` shall be well-formed and have the
following semantics:

*Requires:* If `m` is of type `mutex`, `timed_mutex`, `shared_mutex`, or
`shared_timed_mutex`, the calling thread does not own the mutex.

*Effects:* Attempts to obtain ownership of the mutex for the calling
thread without blocking. If ownership is not obtained, there is no
effect and `try_lock()` immediately returns. An implementation may fail
to obtain the lock even if it is not held by any other thread.

[*Note 1*: This spurious failure is normally uncommon, but allows
interesting implementations based on a simple compare and exchange
(Clause  [[atomics]]). — *end note*]

An implementation should ensure that `try_lock()` does not consistently
return `false` in the absence of contending mutex acquisitions.

*Return type:* `bool`.

*Returns:* `true` if ownership of the mutex was obtained for the calling
thread, otherwise `false`.

*Synchronization:* If `try_lock()` returns `true`, prior `unlock()`
operations on the same object *synchronize
with* ([[intro.multithread]]) this operation.

[*Note 2*: Since `lock()` does not synchronize with a failed subsequent
`try_lock()`, the visibility rules are weak enough that little would be
known about the state after a failure, even in the absence of spurious
failures. — *end note*]

*Throws:* Nothing.

The expression `m.unlock()` shall be well-formed and have the following
semantics:

*Requires:* The calling thread shall own the mutex.

*Effects:* Releases the calling thread’s ownership of the mutex.

*Return type:* `void`.

*Synchronization:* This operation synchronizes
with ([[intro.multithread]]) subsequent lock operations that obtain
ownership on the same object.

*Throws:* Nothing.

##### Class `mutex` <a id="thread.mutex.class">[[thread.mutex.class]]</a>

``` cpp
namespace std {
  class mutex {
  public:
    constexpr mutex() noexcept;
    ~mutex();

    mutex(const mutex&) = delete;
    mutex& operator=(const mutex&) = delete;

    void lock();
    bool try_lock();
    void unlock();

    using native_handle_type = implementation-defined; // See~[thread.req.native]
    native_handle_type native_handle();                // See~[thread.req.native]
  };
}
```

The class `mutex` provides a non-recursive mutex with exclusive
ownership semantics. If one thread owns a mutex object, attempts by
another thread to acquire ownership of that object will fail (for
`try_lock()`) or block (for `lock()`) until the owning thread has
released ownership with a call to `unlock()`.

[*Note 3*: After a thread `A` has called `unlock()`, releasing a mutex,
it is possible for another thread `B` to lock the same mutex, observe
that it is no longer in use, unlock it, and destroy it, before thread
`A` appears to have returned from its unlock call. Implementations are
required to handle such scenarios correctly, as long as thread `A`
doesn’t access the mutex after the unlock call returns. These cases
typically occur when a reference-counted object contains a mutex that is
used to protect the reference count. — *end note*]

The class `mutex` shall satisfy all of the mutex requirements (
[[thread.mutex.requirements]]). It shall be a standard-layout class
(Clause  [[class]]).

[*Note 4*: A program may deadlock if the thread that owns a `mutex`
object calls `lock()` on that object. If the implementation can detect
the deadlock, a `resource_deadlock_would_occur` error condition may be
observed. — *end note*]

The behavior of a program is undefined if it destroys a `mutex` object
owned by any thread or a thread terminates while owning a `mutex`
object.

##### Class `recursive_mutex` <a id="thread.mutex.recursive">[[thread.mutex.recursive]]</a>

``` cpp
namespace std {
  class recursive_mutex {
  public:
    recursive_mutex();
    ~recursive_mutex();

    recursive_mutex(const recursive_mutex&) = delete;
    recursive_mutex& operator=(const recursive_mutex&) = delete;

    void lock();
    bool try_lock() noexcept;
    void unlock();

    using native_handle_type = implementation-defined; // See~[thread.req.native]
    native_handle_type native_handle();                // See~[thread.req.native]
  };
}
```

The class `recursive_mutex` provides a recursive mutex with exclusive
ownership semantics. If one thread owns a `recursive_mutex` object,
attempts by another thread to acquire ownership of that object will fail
(for `try_lock()`) or block (for `lock()`) until the first thread has
completely released ownership.

The class `recursive_mutex` shall satisfy all of the mutex
requirements ([[thread.mutex.requirements]]). It shall be a
standard-layout class (Clause  [[class]]).

A thread that owns a `recursive_mutex` object may acquire additional
levels of ownership by calling `lock()` or `try_lock()` on that object.
It is unspecified how many levels of ownership may be acquired by a
single thread. If a thread has already acquired the maximum level of
ownership for a `recursive_mutex` object, additional calls to
`try_lock()` shall fail, and additional calls to `lock()` shall throw an
exception of type `system_error`. A thread shall call `unlock()` once
for each level of ownership acquired by calls to `lock()` and
`try_lock()`. Only when all levels of ownership have been released may
ownership be acquired by another thread.

The behavior of a program is undefined if:

- it destroys a `recursive_mutex` object owned by any thread or
- a thread terminates while owning a `recursive_mutex` object.

#### Timed mutex types <a id="thread.timedmutex.requirements">[[thread.timedmutex.requirements]]</a>

The *timed mutex types* are the standard library types `timed_mutex`,
`recursive_timed_mutex`, and `shared_timed_mutex`. They shall meet the
requirements set out below. In this description, `m` denotes an object
of a mutex type, `rel_time` denotes an object of an instantiation of
`duration` ([[time.duration]]), and `abs_time` denotes an object of an
instantiation of `time_point` ([[time.point]]).

The timed mutex types shall meet the `TimedLockable` requirements (
[[thread.req.lockable.timed]]).

The expression `m.try_lock_for(rel_time)` shall be well-formed and have
the following semantics:

*Requires:* If `m` is of type `timed_mutex` or `shared_timed_mutex`, the
calling thread does not own the mutex.

*Effects:* The function attempts to obtain ownership of the mutex within
the relative timeout ([[thread.req.timing]]) specified by `rel_time`.
If the time specified by `rel_time` is less than or equal to
`rel_time.zero()`, the function attempts to obtain ownership without
blocking (as if by calling `try_lock()`). The function shall return
within the timeout specified by `rel_time` only if it has obtained
ownership of the mutex object.

[*Note 1*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

*Return type:* `bool`.

*Returns:* `true` if ownership was obtained, otherwise `false`.

*Synchronization:* If `try_lock_for()` returns `true`, prior `unlock()`
operations on the same object *synchronize
with* ([[intro.multithread]]) this operation.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

The expression `m.try_lock_until(abs_time)` shall be well-formed and
have the following semantics:

*Requires:* If `m` is of type `timed_mutex` or `shared_timed_mutex`, the
calling thread does not own the mutex.

*Effects:* The function attempts to obtain ownership of the mutex. If
`abs_time` has already passed, the function attempts to obtain ownership
without blocking (as if by calling `try_lock()`). The function shall
return before the absolute timeout ([[thread.req.timing]]) specified by
`abs_time` only if it has obtained ownership of the mutex object.

[*Note 2*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

*Return type:* `bool`.

*Returns:* `true` if ownership was obtained, otherwise `false`.

*Synchronization:* If `try_lock_until()` returns `true`, prior
`unlock()` operations on the same object *synchronize
with* ([[intro.multithread]]) this operation.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

##### Class `timed_mutex` <a id="thread.timedmutex.class">[[thread.timedmutex.class]]</a>

``` cpp
namespace std {
  class timed_mutex {
  public:
    timed_mutex();
    ~timed_mutex();

    timed_mutex(const timed_mutex&) = delete;
    timed_mutex& operator=(const timed_mutex&) = delete;

    void lock();  // blocking
    bool try_lock();
    template <class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template <class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    using native_handle_type = implementation-defined; // See~[thread.req.native]
    native_handle_type native_handle();                // See~[thread.req.native]
  };
}
```

The class `timed_mutex` provides a non-recursive mutex with exclusive
ownership semantics. If one thread owns a `timed_mutex` object, attempts
by another thread to acquire ownership of that object will fail (for
`try_lock()`) or block (for `lock()`, `try_lock_for()`, and
`try_lock_until()`) until the owning thread has released ownership with
a call to `unlock()` or the call to `try_lock_for()` or
`try_lock_until()` times out (having failed to obtain ownership).

The class `timed_mutex` shall satisfy all of the timed mutex
requirements ([[thread.timedmutex.requirements]]). It shall be a
standard-layout class (Clause  [[class]]).

The behavior of a program is undefined if:

- it destroys a `timed_mutex` object owned by any thread,
- a thread that owns a `timed_mutex` object calls `lock()`,
  `try_lock()`, `try_lock_for()`, or `try_lock_until()` on that object,
  or
- a thread terminates while owning a `timed_mutex` object.

##### Class `recursive_timed_mutex` <a id="thread.timedmutex.recursive">[[thread.timedmutex.recursive]]</a>

``` cpp
namespace std {
  class recursive_timed_mutex {
  public:
    recursive_timed_mutex();
    ~recursive_timed_mutex();

    recursive_timed_mutex(const recursive_timed_mutex&) = delete;
    recursive_timed_mutex& operator=(const recursive_timed_mutex&) = delete;

    void lock();  // blocking
    bool try_lock() noexcept;
    template <class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template <class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    using native_handle_type = implementation-defined; // See~[thread.req.native]
    native_handle_type native_handle();                // See~[thread.req.native]
  };
}
```

The class `recursive_timed_mutex` provides a recursive mutex with
exclusive ownership semantics. If one thread owns a
`recursive_timed_mutex` object, attempts by another thread to acquire
ownership of that object will fail (for `try_lock()`) or block (for
`lock()`, `try_lock_for()`, and `try_lock_until()`) until the owning
thread has completely released ownership or the call to `try_lock_for()`
or `try_lock_until()` times out (having failed to obtain ownership).

The class `recursive_timed_mutex` shall satisfy all of the timed mutex
requirements ([[thread.timedmutex.requirements]]). It shall be a
standard-layout class (Clause  [[class]]).

A thread that owns a `recursive_timed_mutex` object may acquire
additional levels of ownership by calling `lock()`, `try_lock()`,
`try_lock_for()`, or `try_lock_until()` on that object. It is
unspecified how many levels of ownership may be acquired by a single
thread. If a thread has already acquired the maximum level of ownership
for a `recursive_timed_mutex` object, additional calls to `try_lock()`,
`try_lock_for()`, or `try_lock_until()` shall fail, and additional calls
to `lock()` shall throw an exception of type `system_error`. A thread
shall call `unlock()` once for each level of ownership acquired by calls
to `lock()`, `try_lock()`, `try_lock_for()`, and `try_lock_until()`.
Only when all levels of ownership have been released may ownership of
the object be acquired by another thread.

The behavior of a program is undefined if:

- it destroys a `recursive_timed_mutex` object owned by any thread, or
- a thread terminates while owning a `recursive_timed_mutex` object.

#### Shared mutex types <a id="thread.sharedmutex.requirements">[[thread.sharedmutex.requirements]]</a>

The standard library types `shared_mutex` and `shared_timed_mutex` are
*shared mutex types*. Shared mutex types shall meet the requirements of
mutex types ([[thread.mutex.requirements.mutex]]), and additionally
shall meet the requirements set out below. In this description, `m`
denotes an object of a shared mutex type.

In addition to the exclusive lock ownership mode specified in 
[[thread.mutex.requirements.mutex]], shared mutex types provide a
*shared lock* ownership mode. Multiple execution agents can
simultaneously hold a shared lock ownership of a shared mutex type. But
no execution agent shall hold a shared lock while another execution
agent holds an exclusive lock on the same shared mutex type, and
vice-versa. The maximum number of execution agents which can share a
shared lock on a single shared mutex type is unspecified, but shall be
at least 10000. If more than the maximum number of execution agents
attempt to obtain a shared lock, the excess execution agents shall block
until the number of shared locks are reduced below the maximum amount by
other execution agents releasing their shared lock.

The expression `m.lock_shared()` shall be well-formed and have the
following semantics:

*Requires:* The calling thread has no ownership of the mutex.

*Effects:* Blocks the calling thread until shared ownership of the mutex
can be obtained for the calling thread. If an exception is thrown then a
shared lock shall not have been acquired for the current thread.

*Postconditions:* The calling thread has a shared lock on the mutex.

*Return type:* `void`.

*Synchronization:* Prior `unlock()` operations on the same object shall
synchronize with ([[intro.multithread]]) this operation.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.
- `resource_deadlock_would_occur` — if the implementation detects that a
  deadlock would occur.

The expression `m.unlock_shared()` shall be well-formed and have the
following semantics:

*Requires:* The calling thread shall hold a shared lock on the mutex.

*Effects:* Releases a shared lock on the mutex held by the calling
thread.

*Return type:* `void`.

*Synchronization:* This operation synchronizes
with ([[intro.multithread]]) subsequent `lock()` operations that obtain
ownership on the same object.

*Throws:* Nothing.

The expression `m.try_lock_shared()` shall be well-formed and have the
following semantics:

*Requires:* The calling thread has no ownership of the mutex.

*Effects:* Attempts to obtain shared ownership of the mutex for the
calling thread without blocking. If shared ownership is not obtained,
there is no effect and `try_lock_shared()` immediately returns. An
implementation may fail to obtain the lock even if it is not held by any
other thread.

*Return type:* `bool`.

*Returns:* `true` if the shared ownership lock was acquired, `false`
otherwise.

*Synchronization:* If `try_lock_shared()` returns `true`, prior
`unlock()` operations on the same object synchronize
with ([[intro.multithread]]) this operation.

*Throws:* Nothing.

##### Class shared_mutex <a id="thread.sharedmutex.class">[[thread.sharedmutex.class]]</a>

``` cpp
namespace std {
  class shared_mutex {
  public:
    shared_mutex();
    ~shared_mutex();

    shared_mutex(const shared_mutex&) = delete;
    shared_mutex& operator=(const shared_mutex&) = delete;

    // Exclusive ownership
    void lock(); // blocking
    bool try_lock();
    void unlock();

    // Shared ownership
    void lock_shared(); // blocking
    bool try_lock_shared();
    void unlock_shared();

    using native_handle_type = implementation-defined; // See~[thread.req.native]
    native_handle_type native_handle();                // See~[thread.req.native]
  };
}
```

The class `shared_mutex` provides a non-recursive mutex with shared
ownership semantics.

The class `shared_mutex` shall satisfy all of the shared mutex
requirements ([[thread.sharedmutex.requirements]]). It shall be a
standard-layout class (Clause  [[class]]).

The behavior of a program is undefined if:

- it destroys a `shared_mutex` object owned by any thread,
- a thread attempts to recursively gain any ownership of a
  `shared_mutex`, or
- a thread terminates while possessing any ownership of a
  `shared_mutex`.

`shared_mutex` may be a synonym for `shared_timed_mutex`.

#### Shared timed mutex types <a id="thread.sharedtimedmutex.requirements">[[thread.sharedtimedmutex.requirements]]</a>

The standard library type `shared_timed_mutex` is a *shared timed mutex
type*. Shared timed mutex types shall meet the requirements of timed
mutex types ([[thread.timedmutex.requirements]]), shared mutex types (
[[thread.sharedmutex.requirements]]), and additionally shall meet the
requirements set out below. In this description, `m` denotes an object
of a shared timed mutex type, `rel_type` denotes an object of an
instantiation of `duration` ([[time.duration]]), and `abs_time` denotes
an object of an instantiation of `time_point` ([[time.point]]).

The expression `m.try_lock_shared_for(rel_time)` shall be well-formed
and have the following semantics:

*Requires:* The calling thread has no ownership of the mutex.

*Effects:* Attempts to obtain shared lock ownership for the calling
thread within the relative timeout ([[thread.req.timing]]) specified by
`rel_time`. If the time specified by `rel_time` is less than or equal to
`rel_time.zero()`, the function attempts to obtain ownership without
blocking (as if by calling `try_lock_shared()`). The function shall
return within the timeout specified by `rel_time` only if it has
obtained shared ownership of the mutex object.

[*Note 1*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

If an exception is thrown then a shared lock shall not have been
acquired for the current thread.

*Return type:* `bool`.

*Returns:* `true` if the shared lock was acquired, `false` otherwise.

*Synchronization:* If `try_lock_shared_for()` returns `true`, prior
`unlock()` operations on the same object synchronize
with ([[intro.multithread]]) this operation.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

The expression `m.try_lock_shared_until(abs_time)` shall be well-formed
and have the following semantics:

*Requires:* The calling thread has no ownership of the mutex.

*Effects:* The function attempts to obtain shared ownership of the
mutex. If `abs_time` has already passed, the function attempts to obtain
shared ownership without blocking (as if by calling
`try_lock_shared()`). The function shall return before the absolute
timeout ([[thread.req.timing]]) specified by `abs_time` only if it has
obtained shared ownership of the mutex object.

[*Note 2*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

If an exception is thrown then a shared lock shall not have been
acquired for the current thread.

*Return type:* `bool`.

*Returns:* `true` if the shared lock was acquired, `false` otherwise.

*Synchronization:* If `try_lock_shared_until()` returns `true`, prior
`unlock()` operations on the same object synchronize
with ([[intro.multithread]]) this operation.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

##### Class `shared_timed_mutex` <a id="thread.sharedtimedmutex.class">[[thread.sharedtimedmutex.class]]</a>

``` cpp
namespace std {
  class shared_timed_mutex {
  public:
    shared_timed_mutex();
    ~shared_timed_mutex();

    shared_timed_mutex(const shared_timed_mutex&) = delete;
    shared_timed_mutex& operator=(const shared_timed_mutex&) = delete;

    // Exclusive ownership
    void lock();  // blocking
    bool try_lock();
    template <class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template <class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    // Shared ownership
    void lock_shared();  // blocking
    bool try_lock_shared();
    template <class Rep, class Period>
      bool
      try_lock_shared_for(const chrono::duration<Rep, Period>& rel_time);
    template <class Clock, class Duration>
      bool
      try_lock_shared_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock_shared();
  };
}
```

The class `shared_timed_mutex` provides a non-recursive mutex with
shared ownership semantics.

The class `shared_timed_mutex` shall satisfy all of the shared timed
mutex requirements ([[thread.sharedtimedmutex.requirements]]). It shall
be a standard-layout class (Clause  [[class]]).

The behavior of a program is undefined if:

- it destroys a `shared_timed_mutex` object owned by any thread,
- a thread attempts to recursively gain any ownership of a
  `shared_timed_mutex`, or
- a thread terminates while possessing any ownership of a
  `shared_timed_mutex`.

### Locks <a id="thread.lock">[[thread.lock]]</a>

A *lock* is an object that holds a reference to a lockable object and
may unlock the lockable object during the lock’s destruction (such as
when leaving block scope). An execution agent may use a lock to aid in
managing ownership of a lockable object in an exception safe manner. A
lock is said to *own* a lockable object if it is currently managing the
ownership of that lockable object for an execution agent. A lock does
not manage the lifetime of the lockable object it references.

[*Note 1*: Locks are intended to ease the burden of unlocking the
lockable object under both normal and exceptional
circumstances. — *end note*]

Some lock constructors take tag types which describe what should be done
with the lockable object during the lock’s construction.

``` cpp
namespace std {
  struct defer_lock_t  { };     // do not acquire ownership of the mutex
  struct try_to_lock_t { };     // try to acquire ownership of the mutex
                                // without blocking
  struct adopt_lock_t  { };     // assume the calling thread has already
                                // obtained mutex ownership and manage it

  inline constexpr defer_lock_t   defer_lock { };
  inline constexpr try_to_lock_t  try_to_lock { };
  inline constexpr adopt_lock_t   adopt_lock { };
}
```

#### Class template `lock_guard` <a id="thread.lock.guard">[[thread.lock.guard]]</a>

``` cpp
namespace std {
  template <class Mutex>
  class lock_guard {
  public:
    using mutex_type = Mutex;

    explicit lock_guard(mutex_type& m);
    lock_guard(mutex_type& m, adopt_lock_t);
    ~lock_guard();

    lock_guard(const lock_guard&) = delete;
    lock_guard& operator=(const lock_guard&) = delete;

  private:
    mutex_type& pm; // exposition only
  };

  template<class Mutex> lock_guard(lock_guard<Mutex>) -> lock_guard<Mutex>;
}
```

An object of type `lock_guard` controls the ownership of a lockable
object within a scope. A `lock_guard` object maintains ownership of a
lockable object throughout the `lock_guard` object’s lifetime (
[[basic.life]]). The behavior of a program is undefined if the lockable
object referenced by `pm` does not exist for the entire lifetime of the
`lock_guard` object. The supplied `Mutex` type shall meet the
`BasicLockable` requirements ([[thread.req.lockable.basic]]).

``` cpp
explicit lock_guard(mutex_type& m);
```

*Requires:* If `mutex_type` is not a recursive mutex, the calling thread
does not own the mutex `m`.

*Effects:* As if by `m.lock()`.

*Postconditions:* `&pm == &m`

``` cpp
lock_guard(mutex_type& m, adopt_lock_t);
```

*Requires:* The calling thread owns the mutex `m`.

*Postconditions:* `&pm == &m`

*Throws:* Nothing.

``` cpp
~lock_guard();
```

*Effects:* As if by `pm.unlock()`.

#### Class template `scoped_lock` <a id="thread.lock.scoped">[[thread.lock.scoped]]</a>

``` cpp
namespace std {
  template <class... MutexTypes>
  class scoped_lock {
  public:
    using mutex_type = Mutex;  // If MutexTypes... consists of the single type Mutex

    explicit scoped_lock(MutexTypes&... m);
    explicit scoped_lock(MutexTypes&... m, adopt_lock_t);
    ~scoped_lock();

    scoped_lock(const scoped_lock&) = delete;
    scoped_lock& operator=(const scoped_lock&) = delete;

  private:
    tuple<MutexTypes&...> pm; // exposition only
  };

  template<class... MutexTypes>
    scoped_lock(scoped_lock<MutexTypes...>) -> scoped_lock<MutexTypes...>;
}
```

An object of type `scoped_lock` controls the ownership of lockable
objects within a scope. A `scoped_lock` object maintains ownership of
lockable objects throughout the `scoped_lock` object’s lifetime (
[[basic.life]]). The behavior of a program is undefined if the lockable
objects referenced by `pm` do not exist for the entire lifetime of the
`scoped_lock` object. When `sizeof...(MutexTypes)` is `1`, the supplied
`Mutex` type shall meet the `BasicLockable` requirements (
[[thread.req.lockable.basic]]). Otherwise, each of the mutex types shall
meet the `Lockable` requirements ([[thread.req.lockable.req]]).

``` cpp
explicit scoped_lock(MutexTypes&... m);
```

*Requires:* If a `MutexTypes` type is not a recursive mutex, the calling
thread does not own the corresponding mutex element of `m`.

*Effects:* Initializes `pm` with `tie(m...)`. Then if
`sizeof...(MutexTypes)` is `0`, no effects. Otherwise if
`sizeof...(MutexTypes)` is `1`, then `m.lock()`. Otherwise,
`lock(m...)`.

``` cpp
explicit scoped_lock(MutexTypes&... m, adopt_lock_t);
```

*Requires:* The calling thread owns all the mutexes in `m`.

*Effects:* Initializes `pm` with `tie(m...)`.

*Throws:* Nothing.

``` cpp
~scoped_lock();
```

*Effects:* For all `i` in \[`0`, `sizeof...(MutexTypes)`),
`get<i>(pm).unlock()`.

#### Class template `unique_lock` <a id="thread.lock.unique">[[thread.lock.unique]]</a>

``` cpp
namespace std {
  template <class Mutex>
  class unique_lock {
  public:
    using mutex_type = Mutex;

    // [thread.lock.unique.cons], construct/copy/destroy
    unique_lock() noexcept;
    explicit unique_lock(mutex_type& m);
    unique_lock(mutex_type& m, defer_lock_t) noexcept;
    unique_lock(mutex_type& m, try_to_lock_t);
    unique_lock(mutex_type& m, adopt_lock_t);
    template <class Clock, class Duration>
      unique_lock(mutex_type& m, const chrono::time_point<Clock, Duration>& abs_time);
    template <class Rep, class Period>
      unique_lock(mutex_type& m, const chrono::duration<Rep, Period>& rel_time);
    ~unique_lock();

    unique_lock(const unique_lock&) = delete;
    unique_lock& operator=(const unique_lock&) = delete;

    unique_lock(unique_lock&& u) noexcept;
    unique_lock& operator=(unique_lock&& u);

    // [thread.lock.unique.locking], locking
    void lock();
    bool try_lock();

    template <class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template <class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);

    void unlock();

    // [thread.lock.unique.mod], modifiers
    void swap(unique_lock& u) noexcept;
    mutex_type* release() noexcept;

    // [thread.lock.unique.obs], observers
    bool owns_lock() const noexcept;
    explicit operator bool () const noexcept;
    mutex_type* mutex() const noexcept;

  private:
    mutex_type* pm; // exposition only
    bool owns;      // exposition only
  };

  template<class Mutex> unique_lock(unique_lock<Mutex>) -> unique_lock<Mutex>;

  template <class Mutex>
    void swap(unique_lock<Mutex>& x, unique_lock<Mutex>& y) noexcept;
}
```

An object of type `unique_lock` controls the ownership of a lockable
object within a scope. Ownership of the lockable object may be acquired
at construction or after construction, and may be transferred, after
acquisition, to another `unique_lock` object. Objects of type
`unique_lock` are not copyable but are movable. The behavior of a
program is undefined if the contained pointer `pm` is not null and the
lockable object pointed to by `pm` does not exist for the entire
remaining lifetime ([[basic.life]]) of the `unique_lock` object. The
supplied `Mutex` type shall meet the `BasicLockable` requirements (
[[thread.req.lockable.basic]]).

[*Note 1*: `unique_lock<Mutex>` meets the `BasicLockable` requirements.
If `Mutex` meets the `Lockable` requirements (
[[thread.req.lockable.req]]), `unique_lock<Mutex>` also meets the
`Lockable` requirements; if `Mutex` meets the `TimedLockable`
requirements ([[thread.req.lockable.timed]]), `unique_lock<Mutex>` also
meets the `TimedLockable` requirements. — *end note*]

##### `unique_lock` constructors, destructor, and assignment <a id="thread.lock.unique.cons">[[thread.lock.unique.cons]]</a>

``` cpp
unique_lock() noexcept;
```

*Effects:* Constructs an object of type `unique_lock`.

*Postconditions:* `pm == 0` and `owns == false`.

``` cpp
explicit unique_lock(mutex_type& m);
```

*Requires:* If `mutex_type` is not a recursive mutex the calling thread
does not own the mutex.

*Effects:* Constructs an object of type `unique_lock` and calls
`m.lock()`.

*Postconditions:* `pm == addressof(m)` and `owns == true`.

``` cpp
unique_lock(mutex_type& m, defer_lock_t) noexcept;
```

*Effects:* Constructs an object of type `unique_lock`.

*Postconditions:* `pm == addressof(m)` and `owns == false`.

``` cpp
unique_lock(mutex_type& m, try_to_lock_t);
```

*Requires:* The supplied `Mutex` type shall meet the `Lockable`
requirements ([[thread.req.lockable.req]]). If `mutex_type` is not a
recursive mutex the calling thread does not own the mutex.

*Effects:* Constructs an object of type `unique_lock` and calls
`m.try_lock()`.

*Postconditions:* `pm == addressof(m)` and `owns == res`, where `res` is
the value returned by the call to `m.try_lock()`.

``` cpp
unique_lock(mutex_type& m, adopt_lock_t);
```

*Requires:* The calling thread owns the mutex.

*Effects:* Constructs an object of type `unique_lock`.

*Postconditions:* `pm == addressof(m)` and `owns == true`.

*Throws:* Nothing.

``` cpp
template <class Clock, class Duration>
  unique_lock(mutex_type& m, const chrono::time_point<Clock, Duration>& abs_time);
```

*Requires:* If `mutex_type` is not a recursive mutex the calling thread
does not own the mutex. The supplied `Mutex` type shall meet the
`TimedLockable` requirements ([[thread.req.lockable.timed]]).

*Effects:* Constructs an object of type `unique_lock` and calls
`m.try_lock_until(abs_time)`.

*Postconditions:* `pm == addressof(m)` and `owns == res`, where `res` is
the value returned by the call to `m.try_lock_until(abs_time)`.

``` cpp
template <class Rep, class Period>
  unique_lock(mutex_type& m, const chrono::duration<Rep, Period>& rel_time);
```

*Requires:* If `mutex_type` is not a recursive mutex the calling thread
does not own the mutex. The supplied `Mutex` type shall meet the
`TimedLockable` requirements ([[thread.req.lockable.timed]]).

*Effects:* Constructs an object of type `unique_lock` and calls
`m.try_lock_for(rel_time)`.

*Postconditions:* `pm == addressof(m)` and `owns == res`, where `res` is
the value returned by the call to `m.try_lock_for(rel_time)`.

``` cpp
unique_lock(unique_lock&& u) noexcept;
```

*Postconditions:* `pm == u_p.pm` and `owns == u_p.owns` (where `u_p` is
the state of `u` just prior to this construction), `u.pm == 0` and
`u.owns == false`.

``` cpp
unique_lock& operator=(unique_lock&& u);
```

*Effects:* If `owns` calls `pm->unlock()`.

*Postconditions:* `pm == u_p.pm` and `owns == u_p.owns` (where `u_p` is
the state of `u` just prior to this construction), `u.pm == 0` and
`u.owns == false`.

[*Note 1*: With a recursive mutex it is possible for both `*this` and
`u` to own the same mutex before the assignment. In this case, `*this`
will own the mutex after the assignment and `u` will not. — *end note*]

*Throws:* Nothing.

``` cpp
~unique_lock();
```

*Effects:* If `owns` calls `pm->unlock()`.

##### `unique_lock` locking <a id="thread.lock.unique.locking">[[thread.lock.unique.locking]]</a>

``` cpp
void lock();
```

*Effects:* As if by `pm->lock()`.

*Postconditions:* `owns == true`.

*Throws:* Any exception thrown by `pm->lock()`. `system_error` when an
exception is required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
bool try_lock();
```

*Requires:* The supplied `Mutex` shall meet the `Lockable`
requirements ([[thread.req.lockable.req]]).

*Effects:* As if by `pm->try_lock()`.

*Returns:* The value returned by the call to `try_lock()`.

*Postconditions:* `owns == res`, where `res` is the value returned by
the call to `try_lock()`.

*Throws:* Any exception thrown by `pm->try_lock()`. `system_error` when
an exception is required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template <class Clock, class Duration>
  bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Requires:* The supplied `Mutex` type shall meet the `TimedLockable`
requirements ([[thread.req.lockable.timed]]).

*Effects:* As if by `pm->try_lock_until(abs_time)`.

*Returns:* The value returned by the call to `try_lock_until(abs_time)`.

*Postconditions:* `owns == res`, where `res` is the value returned by
the call to `try_lock_until(abs_time)`.

*Throws:* Any exception thrown by `pm->try_lock_until()`. `system_error`
when an exception is required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template <class Rep, class Period>
  bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
```

*Requires:* The supplied `Mutex` type shall meet the `TimedLockable`
requirements ([[thread.req.lockable.timed]]).

*Effects:* As if by `pm->try_lock_for(rel_time)`.

*Returns:* The value returned by the call to `try_lock_until(rel_time)`.

*Postconditions:* `owns == res`, where `res` is the value returned by
the call to `try_lock_for(rel_time)`.

*Throws:* Any exception thrown by `pm->try_lock_for()`. `system_error`
when an exception is required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
void unlock();
```

*Effects:* As if by `pm->unlock()`.

*Postconditions:* `owns == false`.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if on entry `owns` is `false`.

##### `unique_lock` modifiers <a id="thread.lock.unique.mod">[[thread.lock.unique.mod]]</a>

``` cpp
void swap(unique_lock& u) noexcept;
```

*Effects:* Swaps the data members of `*this` and `u`.

``` cpp
mutex_type* release() noexcept;
```

*Returns:* The previous value of `pm`.

*Postconditions:* `pm == 0` and `owns == false`.

``` cpp
template <class Mutex>
  void swap(unique_lock<Mutex>& x, unique_lock<Mutex>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

##### `unique_lock` observers <a id="thread.lock.unique.obs">[[thread.lock.unique.obs]]</a>

``` cpp
bool owns_lock() const noexcept;
```

*Returns:* `owns`.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `owns`.

``` cpp
mutex_type *mutex() const noexcept;
```

*Returns:* `pm`.

#### Class template `shared_lock` <a id="thread.lock.shared">[[thread.lock.shared]]</a>

``` cpp
namespace std {
  template <class Mutex>
  class shared_lock {
  public:
    using mutex_type = Mutex;

    // [thread.lock.shared.cons], construct/copy/destroy
    shared_lock() noexcept;
    explicit shared_lock(mutex_type& m);  // blocking
    shared_lock(mutex_type& m, defer_lock_t) noexcept;
    shared_lock(mutex_type& m, try_to_lock_t);
    shared_lock(mutex_type& m, adopt_lock_t);
    template <class Clock, class Duration>
      shared_lock(mutex_type& m,
                  const chrono::time_point<Clock, Duration>& abs_time);
    template <class Rep, class Period>
      shared_lock(mutex_type& m,
                const chrono::duration<Rep, Period>& rel_time);
    ~shared_lock();

    shared_lock(const shared_lock&) = delete;
    shared_lock& operator=(const shared_lock&) = delete;

    shared_lock(shared_lock&& u) noexcept;
    shared_lock& operator=(shared_lock&& u) noexcept;

    // [thread.lock.shared.locking], locking
    void lock();  // blocking
    bool try_lock();
    template <class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template <class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    // [thread.lock.shared.mod], modifiers
    void swap(shared_lock& u) noexcept;
    mutex_type* release() noexcept;

    // [thread.lock.shared.obs], observers
    bool owns_lock() const noexcept;
    explicit operator bool () const noexcept;
    mutex_type* mutex() const noexcept;

  private:
    mutex_type* pm; // exposition only
    bool owns;      // exposition only
  };

  template<class Mutex> shared_lock(shared_lock<Mutex>) -> shared_lock<Mutex>;

  template <class Mutex>
    void swap(shared_lock<Mutex>& x, shared_lock<Mutex>& y) noexcept;
}
```

An object of type `shared_lock` controls the shared ownership of a
lockable object within a scope. Shared ownership of the lockable object
may be acquired at construction or after construction, and may be
transferred, after acquisition, to another `shared_lock` object. Objects
of type `shared_lock` are not copyable but are movable. The behavior of
a program is undefined if the contained pointer `pm` is not null and the
lockable object pointed to by `pm` does not exist for the entire
remaining lifetime ([[basic.life]]) of the `shared_lock` object. The
supplied `Mutex` type shall meet the shared mutex requirements (
[[thread.sharedtimedmutex.requirements]]).

[*Note 1*: `shared_lock<Mutex>` meets the `TimedLockable`
requirements ([[thread.req.lockable.timed]]). — *end note*]

##### `shared_lock` constructors, destructor, and assignment <a id="thread.lock.shared.cons">[[thread.lock.shared.cons]]</a>

``` cpp
shared_lock() noexcept;
```

*Effects:* Constructs an object of type `shared_lock`.

*Postconditions:* `pm == nullptr` and `owns == false`.

``` cpp
explicit shared_lock(mutex_type& m);
```

*Requires:* The calling thread does not own the mutex for any ownership
mode.

*Effects:* Constructs an object of type `shared_lock` and calls
`m.lock_shared()`.

*Postconditions:* `pm == addressof(m)` and `owns == true`.

``` cpp
shared_lock(mutex_type& m, defer_lock_t) noexcept;
```

*Effects:* Constructs an object of type `shared_lock`.

*Postconditions:* `pm == addressof(m)` and `owns == false`.

``` cpp
shared_lock(mutex_type& m, try_to_lock_t);
```

*Requires:* The calling thread does not own the mutex for any ownership
mode.

*Effects:* Constructs an object of type `shared_lock` and calls
`m.try_lock_shared()`.

*Postconditions:* `pm == addressof(m)` and `owns == res` where `res` is
the value returned by the call to `m.try_lock_shared()`.

``` cpp
shared_lock(mutex_type& m, adopt_lock_t);
```

*Requires:* The calling thread has shared ownership of the mutex.

*Effects:* Constructs an object of type `shared_lock`.

*Postconditions:* `pm == addressof(m)` and `owns == true`.

``` cpp
template <class Clock, class Duration>
  shared_lock(mutex_type& m,
              const chrono::time_point<Clock, Duration>& abs_time);
```

*Requires:* The calling thread does not own the mutex for any ownership
mode.

*Effects:* Constructs an object of type `shared_lock` and calls
`m.try_lock_shared_until(abs_time)`.

*Postconditions:* `pm == addressof(m)` and `owns == res` where `res` is
the value returned by the call to `m.try_lock_shared_until(abs_time)`.

``` cpp
template <class Rep, class Period>
  shared_lock(mutex_type& m,
              const chrono::duration<Rep, Period>& rel_time);
```

*Requires:* The calling thread does not own the mutex for any ownership
mode.

*Effects:* Constructs an object of type `shared_lock` and calls
`m.try_lock_shared_for(rel_time)`.

*Postconditions:* `pm == addressof(m)` and `owns == res` where `res` is
the value returned by the call to `m.try_lock_shared_for(rel_time)`.

``` cpp
~shared_lock();
```

*Effects:* If `owns` calls `pm->unlock_shared()`.

``` cpp
shared_lock(shared_lock&& sl) noexcept;
```

*Postconditions:* `pm == sl_p.pm` and `owns == sl_p.owns` (where `sl_p`
is the state of `sl` just prior to this construction),
`sl.pm == nullptr` and `sl.owns == false`.

``` cpp
shared_lock& operator=(shared_lock&& sl) noexcept;
```

*Effects:* If `owns` calls `pm->unlock_shared()`.

*Postconditions:* `pm == sl_p.pm` and `owns == sl_p.owns` (where `sl_p`
is the state of `sl` just prior to this assignment), `sl.pm == nullptr`
and `sl.owns == false`.

##### `shared_lock` locking <a id="thread.lock.shared.locking">[[thread.lock.shared.locking]]</a>

``` cpp
void lock();
```

*Effects:* As if by `pm->lock_shared()`.

*Postconditions:* `owns == true`.

*Throws:* Any exception thrown by `pm->lock_shared()`. `system_error`
when an exception is required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
bool try_lock();
```

*Effects:* As if by `pm->try_lock_shared()`.

*Returns:* The value returned by the call to `pm->try_lock_shared()`.

*Postconditions:* `owns == res`, where `res` is the value returned by
the call to `pm->try_lock_shared()`.

*Throws:* Any exception thrown by `pm->try_lock_shared()`.
`system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template <class Clock, class Duration>
  bool
  try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:* As if by `pm->try_lock_shared_until(abs_time)`.

*Returns:* The value returned by the call to
`pm->try_lock_shared_until(abs_time)`.

*Postconditions:* `owns == res`, where `res` is the value returned by
the call to `pm->try_lock_shared_until(abs_time)`.

*Throws:* Any exception thrown by `pm->try_lock_shared_until(abs_time)`.
`system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template <class Rep, class Period>
  bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
```

*Effects:* As if by `pm->try_lock_shared_for(rel_time)`.

*Returns:* The value returned by the call to
`pm->try_lock_shared_for(rel_time)`.

*Postconditions:* `owns == res`, where `res` is the value returned by
the call to `pm->try_lock_shared_for(rel_time)`.

*Throws:* Any exception thrown by `pm->try_lock_shared_for(rel_time)`.
`system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
void unlock();
```

*Effects:* As if by `pm->unlock_shared()`.

*Postconditions:* `owns == false`.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `operation_not_permitted` — if on entry `owns` is `false`.

##### `shared_lock` modifiers <a id="thread.lock.shared.mod">[[thread.lock.shared.mod]]</a>

``` cpp
void swap(shared_lock& sl) noexcept;
```

*Effects:* Swaps the data members of `*this` and `sl`.

``` cpp
mutex_type* release() noexcept;
```

*Returns:* The previous value of `pm`.

*Postconditions:* `pm == nullptr` and `owns == false`.

``` cpp
template <class Mutex>
  void swap(shared_lock<Mutex>& x, shared_lock<Mutex>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

##### `shared_lock` observers <a id="thread.lock.shared.obs">[[thread.lock.shared.obs]]</a>

``` cpp
bool owns_lock() const noexcept;
```

*Returns:* `owns`.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `owns`.

``` cpp
mutex_type* mutex() const noexcept;
```

*Returns:* `pm`.

### Generic locking algorithms <a id="thread.lock.algorithm">[[thread.lock.algorithm]]</a>

``` cpp
template <class L1, class L2, class... L3> int try_lock(L1&, L2&, L3&...);
```

*Requires:* Each template parameter type shall meet the `Lockable`
requirements.

[*Note 1*: The `unique_lock` class template meets these requirements
when suitably instantiated. — *end note*]

*Effects:* Calls `try_lock()` for each argument in order beginning with
the first until all arguments have been processed or a call to
`try_lock()` fails, either by returning `false` or by throwing an
exception. If a call to `try_lock()` fails, `unlock()` shall be called
for all prior arguments and there shall be no further calls to
`try_lock()`.

*Returns:* `-1` if all calls to `try_lock()` returned `true`, otherwise
a zero-based index value that indicates the argument for which
`try_lock()` returned `false`.

``` cpp
template <class L1, class L2, class... L3> void lock(L1&, L2&, L3&...);
```

*Requires:* Each template parameter type shall meet the `Lockable`
requirements,

[*Note 2*: The `unique_lock` class template meets these requirements
when suitably instantiated. — *end note*]

*Effects:* All arguments are locked via a sequence of calls to `lock()`,
`try_lock()`, or `unlock()` on each argument. The sequence of calls
shall not result in deadlock, but is otherwise unspecified.

[*Note 3*: A deadlock avoidance algorithm such as try-and-back-off must
be used, but the specific algorithm is not specified to avoid
over-constraining implementations. — *end note*]

If a call to `lock()` or `try_lock()` throws an exception, `unlock()`
shall be called for any argument that had been locked by a call to
`lock()` or `try_lock()`.

### Call once <a id="thread.once">[[thread.once]]</a>

#### Struct `once_flag` <a id="thread.once.onceflag">[[thread.once.onceflag]]</a>

``` cpp
namespace std {
  struct once_flag {
    constexpr once_flag() noexcept;

    once_flag(const once_flag&) = delete;
    once_flag& operator=(const once_flag&) = delete;
  };
}
```

The class `once_flag` is an opaque data structure that `call_once` uses
to initialize data without causing a data race or deadlock.

``` cpp
constexpr once_flag() noexcept;
```

*Effects:* Constructs an object of type `once_flag`.

*Synchronization:* The construction of a `once_flag` object is not
synchronized.

*Postconditions:* The object’s internal state is set to indicate to an
invocation of `call_once` with the object as its initial argument that
no function has been called.

#### Function `call_once` <a id="thread.once.callonce">[[thread.once.callonce]]</a>

``` cpp
template<class Callable, class... Args>
  void call_once(once_flag& flag, Callable&& func, Args&&... args);
```

*Requires:*

``` cpp
INVOKE(std::forward<Callable>(func), std::forward<Args>(args)...)
```

(see [[func.require]]) shall be a valid expression.

*Effects:* An execution of `call_once` that does not call its `func` is
a *passive* execution. An execution of `call_once` that calls its `func`
is an *active* execution. An active execution shall call *INVOKE*(
std::forward\<Callable\>(func), std::forward\<Args\>(args)...). If such
a call to `func` throws an exception the execution is *exceptional*,
otherwise it is *returning*. An exceptional execution shall propagate
the exception to the caller of `call_once`. Among all executions of
`call_once` for any given `once_flag`: at most one shall be a returning
execution; if there is a returning execution, it shall be the last
active execution; and there are passive executions only if there is a
returning execution.

[*Note 1*: Passive executions allow other threads to reliably observe
the results produced by the earlier returning execution. — *end note*]

*Synchronization:* For any given `once_flag`: all active executions
occur in a total order; completion of an active execution synchronizes
with ([[intro.multithread]]) the start of the next one in this total
order; and the returning execution synchronizes with the return from all
passive executions.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]), or any exception thrown by `func`.

[*Example 1*:

``` cpp
// global flag, regular function
void init();
std::once_flag flag;

void f() {
  std::call_once(flag, init);
}

// function static flag, function object
struct initializer {
  void operator()();
};

void g() {
  static std::once_flag flag2;
  std::call_once(flag2, initializer());
}

// object flag, member function
class information {
  std::once_flag verified;
  void verifier();
public:
  void verify() { std::call_once(verified, &information::verifier, *this); }
};
```

— *end example*]

## Condition variables <a id="thread.condition">[[thread.condition]]</a>

Condition variables provide synchronization primitives used to block a
thread until notified by some other thread that some condition is met or
until a system time is reached. Class `condition_variable` provides a
condition variable that can only wait on an object of type
`unique_lock<mutex>`, allowing maximum efficiency on some platforms.
Class `condition_variable_any` provides a general condition variable
that can wait on objects of user-supplied lock types.

Condition variables permit concurrent invocation of the `wait`,
`wait_for`, `wait_until`, `notify_one` and `notify_all` member
functions.

The execution of `notify_one` and `notify_all` shall be atomic. The
execution of `wait`, `wait_for`, and `wait_until` shall be performed in
three atomic parts:

1.  the release of the mutex and entry into the waiting state;
2.  the unblocking of the wait; and
3.  the reacquisition of the lock.

The implementation shall behave as if all executions of `notify_one`,
`notify_all`, and each part of the `wait`, `wait_for`, and `wait_until`
executions are executed in a single unspecified total order consistent
with the "happens before" order.

Condition variable construction and destruction need not be
synchronized.

### Header `<condition_variable>` synopsis <a id="condition_variable.syn">[[condition_variable.syn]]</a>

``` cpp
namespace std {
  class condition_variable;
  class condition_variable_any;

  void notify_all_at_thread_exit(condition_variable& cond, unique_lock<mutex> lk);

  enum class cv_status { no_timeout, timeout };
}
```

### Non-member functions <a id="thread.condition.nonmember">[[thread.condition.nonmember]]</a>

``` cpp
void notify_all_at_thread_exit(condition_variable& cond, unique_lock<mutex> lk);
```

*Requires:* `lk` is locked by the calling thread and either

- no other thread is waiting on `cond`, or
- `lk.mutex()` returns the same value for each of the lock arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Transfers ownership of the lock associated with `lk` into
internal storage and schedules `cond` to be notified when the current
thread exits, after all objects of thread storage duration associated
with the current thread have been destroyed. This notification shall be
as if:

``` cpp
lk.unlock();
cond.notify_all();
```

*Synchronization:* The implied `lk.unlock()` call is sequenced after the
destruction of all objects with thread storage duration associated with
the current thread.

[*Note 1*: The supplied lock will be held until the thread exits, and
care must be taken to ensure that this does not cause deadlock due to
lock ordering issues. After calling `notify_all_at_thread_exit` it is
recommended that the thread should be exited as soon as possible, and
that no blocking or time-consuming tasks are run on that
thread. — *end note*]

[*Note 2*: It is the user’s responsibility to ensure that waiting
threads do not erroneously assume that the thread has finished if they
experience spurious wakeups. This typically requires that the condition
being waited for is satisfied while holding the lock on `lk`, and that
this lock is not released and reacquired prior to calling
`notify_all_at_thread_exit`. — *end note*]

### Class `condition_variable` <a id="thread.condition.condvar">[[thread.condition.condvar]]</a>

``` cpp
namespace std {
  class condition_variable {
  public:

    condition_variable();
    ~condition_variable();

    condition_variable(const condition_variable&) = delete;
    condition_variable& operator=(const condition_variable&) = delete;

    void notify_one() noexcept;
    void notify_all() noexcept;
    void wait(unique_lock<mutex>& lock);
    template <class Predicate>
      void wait(unique_lock<mutex>& lock, Predicate pred);
    template <class Clock, class Duration>
      cv_status wait_until(unique_lock<mutex>& lock,
                           const chrono::time_point<Clock, Duration>& abs_time);
    template <class Clock, class Duration, class Predicate>
      bool wait_until(unique_lock<mutex>& lock,
                      const chrono::time_point<Clock, Duration>& abs_time,
                      Predicate pred);

    template <class Rep, class Period>
      cv_status wait_for(unique_lock<mutex>& lock,
                         const chrono::duration<Rep, Period>& rel_time);
    template <class Rep, class Period, class Predicate>
      bool wait_for(unique_lock<mutex>& lock,
                    const chrono::duration<Rep, Period>& rel_time,
                    Predicate pred);

    using native_handle_type = implementation-defined; // See~[thread.req.native]
    native_handle_type native_handle();                // See~[thread.req.native]
  };
}
```

The class `condition_variable` shall be a standard-layout class (Clause 
[[class]]).

``` cpp
condition_variable();
```

*Effects:* Constructs an object of type `condition_variable`.

*Throws:* `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `resource_unavailable_try_again` — if some non-memory resource
  limitation prevents initialization.

``` cpp
~condition_variable();
```

*Requires:* There shall be no thread blocked on `*this`.

[*Note 1*: That is, all threads shall have been notified; they may
subsequently block on the lock specified in the wait. This relaxes the
usual rules, which would have required all wait calls to happen before
destruction. Only the notification to unblock the wait must happen
before destruction. The user must take care to ensure that no threads
wait on `*this` once the destructor has been started, especially when
the waiting threads are calling the wait functions in a loop or using
the overloads of `wait`, `wait_for`, or `wait_until` that take a
predicate. — *end note*]

*Effects:* Destroys the object.

``` cpp
void notify_one() noexcept;
```

*Effects:* If any threads are blocked waiting for `*this`, unblocks one
of those threads.

``` cpp
void notify_all() noexcept;
```

*Effects:* Unblocks all threads that are blocked waiting for `*this`.

``` cpp
void wait(unique_lock<mutex>& lock);
```

*Requires:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:*

- Atomically calls `lock.unlock()` and blocks on `*this`.
- When unblocked, calls `lock.lock()` (possibly blocking on the lock),
  then returns.
- The function will unblock when signaled by a call to `notify_one()` or
  a call to `notify_all()`, or spuriously.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 2*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread.

*Throws:* Nothing.

``` cpp
template <class Predicate>
  void wait(unique_lock<mutex>& lock, Predicate pred);
```

*Requires:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Equivalent to:

``` cpp
while (!pred())
  wait(lock);
```

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 3*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread.

*Throws:* Any exception thrown by `pred`.

``` cpp
template <class Clock, class Duration>
  cv_status wait_until(unique_lock<mutex>& lock,
                       const chrono::time_point<Clock, Duration>& abs_time);
```

*Requires:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:*

- Atomically calls `lock.unlock()` and blocks on `*this`.
- When unblocked, calls `lock.lock()` (possibly blocking on the lock),
  then returns.
- The function will unblock when signaled by a call to `notify_one()`, a
  call to `notify_all()`, expiration of the absolute
  timeout ([[thread.req.timing]]) specified by `abs_time`, or
  spuriously.
- If the function exits via an exception, `lock.lock()` shall be called
  prior to exiting the function.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 4*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread.

*Returns:* `cv_status::timeout` if the absolute
timeout ([[thread.req.timing]]) specified by `abs_time` expired,
otherwise `cv_status::no_timeout`.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Rep, class Period>
  cv_status wait_for(unique_lock<mutex>& lock,
                     const chrono::duration<Rep, Period>& rel_time);
```

*Requires:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time);
```

*Returns:* `cv_status::timeout` if the relative
timeout ([[thread.req.timing]]) specified by `rel_time` expired,
otherwise `cv_status::no_timeout`.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 5*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Clock, class Duration, class Predicate>
  bool wait_until(unique_lock<mutex>& lock,
                  const chrono::time_point<Clock, Duration>& abs_time,
                  Predicate pred);
```

*Requires:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Equivalent to:

``` cpp
while (!pred())
  if (wait_until(lock, abs_time) == cv_status::timeout)
    return pred();
return true;
```

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 6*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread.

[*Note 7*: The returned value indicates whether the predicate evaluated
to `true` regardless of whether the timeout was
triggered. — *end note*]

*Throws:* Timeout-related exceptions ([[thread.req.timing]]) or any
exception thrown by `pred`.

``` cpp
template <class Rep, class Period, class Predicate>
  bool wait_for(unique_lock<mutex>& lock,
                const chrono::duration<Rep, Period>& rel_time,
                Predicate pred);
```

*Requires:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time, std::move(pred));
```

[*Note 8*: There is no blocking if `pred()` is initially `true`, even
if the timeout has already expired. — *end note*]

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 9*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread.

[*Note 10*: The returned value indicates whether the predicate
evaluates to `true` regardless of whether the timeout was
triggered. — *end note*]

*Throws:* Timeout-related exceptions ([[thread.req.timing]]) or any
exception thrown by `pred`.

### Class `condition_variable_any` <a id="thread.condition.condvarany">[[thread.condition.condvarany]]</a>

A `Lock` type shall meet the `BasicLockable` requirements (
[[thread.req.lockable.basic]]).

[*Note 1*: All of the standard mutex types meet this requirement. If a
`Lock` type other than one of the standard mutex types or a
`unique_lock` wrapper for a standard mutex type is used with
`condition_variable_any`, the user must ensure that any necessary
synchronization is in place with respect to the predicate associated
with the `condition_variable_any` instance. — *end note*]

``` cpp
namespace std {
  class condition_variable_any {
  public:
    condition_variable_any();
    ~condition_variable_any();

    condition_variable_any(const condition_variable_any&) = delete;
    condition_variable_any& operator=(const condition_variable_any&) = delete;

    void notify_one() noexcept;
    void notify_all() noexcept;
    template <class Lock>
      void wait(Lock& lock);
    template <class Lock, class Predicate>
      void wait(Lock& lock, Predicate pred);

    template <class Lock, class Clock, class Duration>
      cv_status wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time);
    template <class Lock, class Clock, class Duration, class Predicate>
      bool wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time,
        Predicate pred);
    template <class Lock, class Rep, class Period>
      cv_status wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time);
    template <class Lock, class Rep, class Period, class Predicate>
      bool wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time,
        Predicate pred);
  };
}
```

``` cpp
condition_variable_any();
```

*Effects:* Constructs an object of type `condition_variable_any`.

*Throws:* `bad_alloc` or `system_error` when an exception is
required ([[thread.req.exception]]).

*Error conditions:*

- `resource_unavailable_try_again` — if some non-memory resource
  limitation prevents initialization.
- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.

``` cpp
~condition_variable_any();
```

*Requires:* There shall be no thread blocked on `*this`.

[*Note 1*: That is, all threads shall have been notified; they may
subsequently block on the lock specified in the wait. This relaxes the
usual rules, which would have required all wait calls to happen before
destruction. Only the notification to unblock the wait must happen
before destruction. The user must take care to ensure that no threads
wait on `*this` once the destructor has been started, especially when
the waiting threads are calling the wait functions in a loop or using
the overloads of `wait`, `wait_for`, or `wait_until` that take a
predicate. — *end note*]

*Effects:* Destroys the object.

``` cpp
void notify_one() noexcept;
```

*Effects:* If any threads are blocked waiting for `*this`, unblocks one
of those threads.

``` cpp
void notify_all() noexcept;
```

*Effects:* Unblocks all threads that are blocked waiting for `*this`.

``` cpp
template <class Lock>
  void wait(Lock& lock);
```

[*Note 2*: If any of the `wait` functions exits via an exception, it is
unspecified whether the `Lock` is held. One can use a `Lock` type that
allows to query that, such as the `unique_lock` wrapper. — *end note*]

*Effects:*

- Atomically calls `lock.unlock()` and blocks on `*this`.
- When unblocked, calls `lock.lock()` (possibly blocking on the lock)
  and returns.
- The function will unblock when signaled by a call to `notify_one()`, a
  call to `notify_all()`, or spuriously.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 3*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock` is locked by the calling thread.

*Throws:* Nothing.

``` cpp
template <class Lock, class Predicate>
  void wait(Lock& lock, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
while (!pred())
  wait(lock);
```

``` cpp
template <class Lock, class Clock, class Duration>
  cv_status wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:*

- Atomically calls `lock.unlock()` and blocks on `*this`.
- When unblocked, calls `lock.lock()` (possibly blocking on the lock)
  and returns.
- The function will unblock when signaled by a call to `notify_one()`, a
  call to `notify_all()`, expiration of the absolute
  timeout ([[thread.req.timing]]) specified by `abs_time`, or
  spuriously.
- If the function exits via an exception, `lock.lock()` shall be called
  prior to exiting the function.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 4*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock` is locked by the calling thread.

*Returns:* `cv_status::timeout` if the absolute
timeout ([[thread.req.timing]]) specified by `abs_time` expired,
otherwise `cv_status::no_timeout`.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Lock, class Rep, class Period>
  cv_status wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time);
```

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time);
```

*Returns:* `cv_status::timeout` if the relative
timeout ([[thread.req.timing]]) specified by `rel_time` expired,
otherwise `cv_status::no_timeout`.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` shall be called ([[except.terminate]]).

[*Note 5*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Postconditions:* `lock` is locked by the calling thread.

*Throws:* Timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Lock, class Clock, class Duration, class Predicate>
  bool wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
while (!pred())
  if (wait_until(lock, abs_time) == cv_status::timeout)
    return pred();
return true;
```

[*Note 6*: There is no blocking if `pred()` is initially `true`, or if
the timeout has already expired. — *end note*]

[*Note 7*: The returned value indicates whether the predicate evaluates
to `true` regardless of whether the timeout was
triggered. — *end note*]

``` cpp
template <class Lock, class Rep, class Period, class Predicate>
  bool wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time, std::move(pred));
```

## Futures <a id="futures">[[futures]]</a>

### Overview <a id="futures.overview">[[futures.overview]]</a>

[[futures]] describes components that a C++program can use to retrieve
in one thread the result (value or exception) from a function that has
run in the same thread or another thread.

[*Note 1*: These components are not restricted to multi-threaded
programs but can be useful in single-threaded programs as
well. — *end note*]

### Header `<future>` synopsis <a id="future.syn">[[future.syn]]</a>

``` cpp
namespace std {
  enum class future_errc {
    broken_promise = implementation-defined,
    future_already_retrieved = implementation-defined,
    promise_already_satisfied = implementation-defined,
    no_state = implementation-defined
  };

  enum class launch : unspecified{} {
    async = unspecified{},
    deferred = unspecified{},
    implementation-defined
  };

  enum class future_status {
    ready,
    timeout,
    deferred
  };

  template <> struct is_error_code_enum<future_errc> : public true_type { };
  error_code make_error_code(future_errc e) noexcept;
  error_condition make_error_condition(future_errc e) noexcept;

  const error_category& future_category() noexcept;

  class future_error;

  template <class R> class promise;
  template <class R> class promise<R&>;
  template <> class promise<void>;

  template <class R>
    void swap(promise<R>& x, promise<R>& y) noexcept;

  template <class R, class Alloc>
    struct uses_allocator<promise<R>, Alloc>;

  template <class R> class future;
  template <class R> class future<R&>;
  template <> class future<void>;

  template <class R> class shared_future;
  template <class R> class shared_future<R&>;
  template <> class shared_future<void>;

  template <class> class packaged_task;   // not defined
  template <class R, class... ArgTypes>
    class packaged_task<R(ArgTypes...)>;

  template <class R, class... ArgTypes>
    void swap(packaged_task<R(ArgTypes...)>&, packaged_task<R(ArgTypes...)>&) noexcept;

  template <class R, class Alloc>
    struct uses_allocator<packaged_task<R>, Alloc>;

  template <class F, class... Args>
    future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
    async(F&& f, Args&&... args);
  template <class F, class... Args>
    future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
    async(launch policy, F&& f, Args&&... args);
}
```

The `enum` type `launch` is a bitmask type ([[bitmask.types]]) with
elements `launch::async` and `launch::deferred`.

[*Note 1*: Implementations can provide bitmasks to specify restrictions
on task interaction by functions launched by `async()` applicable to a
corresponding subset of available launch policies. Implementations can
extend the behavior of the first overload of `async()` by adding their
extensions to the launch policy under the “as if” rule. — *end note*]

The enum values of `future_errc` are distinct and not zero.

### Error handling <a id="futures.errors">[[futures.errors]]</a>

``` cpp
const error_category& future_category() noexcept;
```

*Returns:*  A reference to an object of a type derived from class
`error_category`.

The object’s `default_error_condition` and equivalent virtual functions
shall behave as specified for the class `error_category`. The object’s
`name` virtual function shall return a pointer to the string `"future"`.

``` cpp
error_code make_error_code(future_errc e) noexcept;
```

*Returns:* `error_code(static_cast<int>(e), future_category())`.

``` cpp
error_condition make_error_condition(future_errc e) noexcept;
```

*Returns:* `error_condition(static_cast<int>(e), future_category())`.

### Class `future_error` <a id="futures.future_error">[[futures.future_error]]</a>

``` cpp
namespace std {
  class future_error : public logic_error {
  public:
    explicit future_error(future_errc e);

    const error_code& code() const noexcept;
    const char*       what() const noexcept;
  private:
    error_code ec_;  // exposition only
  };
}
```

``` cpp
explicit future_error(future_errc e);
```

*Effects:* Constructs an object of class `future_error` and initializes
`ec_` with `make_error_code(e)`.

``` cpp
const error_code& code() const noexcept;
```

*Returns:* `ec_`.

``` cpp
const char* what() const noexcept;
```

*Returns:* An NTBSincorporating `code().message()`.

### Shared state <a id="futures.state">[[futures.state]]</a>

Many of the classes introduced in this subclause use some state to
communicate results. This *shared state* consists of some state
information and some (possibly not yet evaluated) *result*, which can be
a (possibly void) value or an exception.

[*Note 1*: Futures, promises, and tasks defined in this clause
reference such shared state. — *end note*]

[*Note 2*: The result can be any kind of object including a function to
compute that result, as used by `async` when `policy` is
`launch::deferred`. — *end note*]

An *asynchronous return object* is an object that reads results from a
shared state. A *waiting function* of an asynchronous return object is
one that potentially blocks to wait for the shared state to be made
ready. If a waiting function can return before the state is made ready
because of a timeout ([[thread.req.lockable]]), then it is a *timed
waiting function*, otherwise it is a *non-timed waiting function*.

An *asynchronous provider* is an object that provides a result to a
shared state. The result of a shared state is set by respective
functions on the asynchronous provider.

[*Note 3*: Such as promises or tasks. — *end note*]

The means of setting the result of a shared state is specified in the
description of those classes and functions that create such a state
object.

When an asynchronous return object or an asynchronous provider is said
to release its shared state, it means:

- if the return object or provider holds the last reference to its
  shared state, the shared state is destroyed; and
- the return object or provider gives up its reference to its shared
  state; and
- these actions will not block for the shared state to become ready,
  except that it may block if all of the following are true: the shared
  state was created by a call to `std::async`, the shared state is not
  yet ready, and this was the last reference to the shared state.

When an asynchronous provider is said to make its shared state ready, it
means:

- first, the provider marks its shared state as ready; and
- second, the provider unblocks any execution agents waiting for its
  shared state to become ready.

When an asynchronous provider is said to abandon its shared state, it
means:

- first, if that state is not ready, the provider
  - stores an exception object of type `future_error` with an error
    condition of `broken_promise` within its shared state; and then
  - makes its shared state ready;
- second, the provider releases its shared state.

A shared state is *ready* only if it holds a value or an exception ready
for retrieval. Waiting for a shared state to become ready may invoke
code to compute the result on the waiting thread if so specified in the
description of the class or function that creates the state object.

Calls to functions that successfully set the stored result of a shared
state synchronize with ([[intro.multithread]]) calls to functions
successfully detecting the ready state resulting from that setting. The
storage of the result (whether normal or exceptional) into the shared
state synchronizes with ([[intro.multithread]]) the successful return
from a call to a waiting function on the shared state.

Some functions (e.g., `promise::set_value_at_thread_exit`) delay making
the shared state ready until the calling thread exits. The destruction
of each of that thread’s objects with thread storage duration (
[[basic.stc.thread]]) is sequenced before making that shared state
ready.

Access to the result of the same shared state may conflict (
[[intro.multithread]]).

[*Note 4*: This explicitly specifies that the result of the shared
state is visible in the objects that reference this state in the sense
of data race avoidance ([[res.on.data.races]]). For example, concurrent
accesses through references returned by `shared_future::get()` (
[[futures.shared_future]]) must either use read-only operations or
provide additional synchronization. — *end note*]

### Class template `promise` <a id="futures.promise">[[futures.promise]]</a>

``` cpp
namespace std {
  template <class R>
  class promise {
  public:
    promise();
    template <class Allocator>
      promise(allocator_arg_t, const Allocator& a);
    promise(promise&& rhs) noexcept;
    promise(const promise& rhs) = delete;
    ~promise();

    // assignment
    promise& operator=(promise&& rhs) noexcept;
    promise& operator=(const promise& rhs) = delete;
    void swap(promise& other) noexcept;

    // retrieving the result
    future<R> get_future();

    // setting the result
    void set_value(see below);
    void set_exception(exception_ptr p);

    // setting the result with deferred notification
    void set_value_at_thread_exit(see below);
    void set_exception_at_thread_exit(exception_ptr p);
  };
  template <class R>
    void swap(promise<R>& x, promise<R>& y) noexcept;
  template <class R, class Alloc>
    struct uses_allocator<promise<R>, Alloc>;
}
```

The implementation shall provide the template `promise` and two
specializations, `promise<R&>` and `promise<{}void>`. These differ only
in the argument type of the member functions `set_value` and
`set_value_at_thread_exit`, as set out in their descriptions, below.

The `set_value`, `set_exception`, `set_value_at_thread_exit`, and
`set_exception_at_thread_exit` member functions behave as though they
acquire a single mutex associated with the promise object while updating
the promise object.

``` cpp
template <class R, class Alloc>
  struct uses_allocator<promise<R>, Alloc>
    : true_type { };
```

*Requires:* `Alloc` shall be an Allocator ([[allocator.requirements]]).

``` cpp
promise();
template <class Allocator>
  promise(allocator_arg_t, const Allocator& a);
```

*Effects:* constructs a `promise` object and a shared state. The second
constructor uses the allocator `a` to allocate memory for the shared
state.

``` cpp
promise(promise&& rhs) noexcept;
```

*Effects:* constructs a new `promise` object and transfers ownership of
the shared state of `rhs` (if any) to the newly-constructed object.

*Postconditions:* `rhs` has no shared state.

``` cpp
~promise();
```

*Effects:* Abandons any shared state ([[futures.state]]).

``` cpp
promise& operator=(promise&& rhs) noexcept;
```

*Effects:* Abandons any shared state ([[futures.state]]) and then as if
`promise(std::move(rhs)).swap(*this)`.

*Returns:* `*this`.

``` cpp
void swap(promise& other) noexcept;
```

*Effects:* Exchanges the shared state of `*this` and `other`.

*Postconditions:* `*this` has the shared state (if any) that `other` had
prior to the call to `swap`. `other` has the shared state (if any) that
`*this` had prior to the call to `swap`.

``` cpp
future<R> get_future();
```

*Returns:* A `future<R>` object with the same shared state as `*this`.

*Throws:* `future_error` if `*this` has no shared state or if
`get_future` has already been called on a `promise` with the same shared
state as `*this`.

*Error conditions:*

- `future_already_retrieved` if `get_future` has already been called on
  a `promise` with the same shared state as `*this`.
- `no_state` if `*this` has no shared state.

``` cpp
void promise::set_value(const R& r);
void promise::set_value(R&& r);
void promise<R&>::set_value(R& r);
void promise<void>::set_value();
```

*Effects:* Atomically stores the value `r` in the shared state and makes
that state ready ([[futures.state]]).

*Throws:*

- `future_error` if its shared state already has a stored value or
  exception, or
- for the first version, any exception thrown by the constructor
  selected to copy an object of `R`, or
- for the second version, any exception thrown by the constructor
  selected to move an object of `R`.

*Error conditions:*

- `promise_already_satisfied` if its shared state already has a stored
  value or exception.
- `no_state` if `*this` has no shared state.

``` cpp
void set_exception(exception_ptr p);
```

*Requires:* `p` is not null.

*Effects:* Atomically stores the exception pointer `p` in the shared
state and makes that state ready ([[futures.state]]).

*Throws:* `future_error` if its shared state already has a stored value
or exception.

*Error conditions:*

- `promise_already_satisfied` if its shared state already has a stored
  value or exception.
- `no_state` if `*this` has no shared state.

``` cpp
void promise::set_value_at_thread_exit(const R& r);
void promise::set_value_at_thread_exit(R&& r);
void promise<R&>::set_value_at_thread_exit(R& r);
void promise<void>::set_value_at_thread_exit();
```

*Effects:* Stores the value `r` in the shared state without making that
state ready immediately. Schedules that state to be made ready when the
current thread exits, after all objects of thread storage duration
associated with the current thread have been destroyed.

*Throws:*

- `future_error` if its shared state already has a stored value or
  exception, or
- for the first version, any exception thrown by the constructor
  selected to copy an object of `R`, or
- for the second version, any exception thrown by the constructor
  selected to move an object of `R`.

*Error conditions:*

- `promise_already_satisfied` if its shared state already has a stored
  value or exception.
- `no_state` if `*this` has no shared state.

``` cpp
void set_exception_at_thread_exit(exception_ptr p);
```

*Requires:* `p` is not null.

*Effects:* Stores the exception pointer `p` in the shared state without
making that state ready immediately. Schedules that state to be made
ready when the current thread exits, after all objects of thread storage
duration associated with the current thread have been destroyed.

*Throws:* `future_error` if an error condition occurs.

*Error conditions:*

- `promise_already_satisfied` if its shared state already has a stored
  value or exception.
- `no_state` if `*this` has no shared state.

``` cpp
template <class R>
  void swap(promise<R>& x, promise<R>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

### Class template `future` <a id="futures.unique_future">[[futures.unique_future]]</a>

The class template `future` defines a type for asynchronous return
objects which do not share their shared state with other asynchronous
return objects. A default-constructed `future` object has no shared
state. A `future` object with shared state can be created by functions
on asynchronous providers ([[futures.state]]) or by the move
constructor and shares its shared state with the original asynchronous
provider. The result (value or exception) of a `future` object can be
set by calling a respective function on an object that shares the same
shared state.

[*Note 1*: Member functions of `future` do not synchronize with
themselves or with member functions of `shared_future`. — *end note*]

The effect of calling any member function other than the destructor, the
move-assignment operator, `share`, or `valid` on a `future` object for
which `valid() == false` is undefined.

[*Note 2*: It is valid to move from a future object for which
`valid() == false`. — *end note*]

[*Note 3*: Implementations are encouraged to detect this case and throw
an object of type `future_error` with an error condition of
`future_errc::no_state`. — *end note*]

``` cpp
namespace std {
  template <class R>
  class future {
  public:
    future() noexcept;
    future(future&&) noexcept;
    future(const future& rhs) = delete;
    ~future();
    future& operator=(const future& rhs) = delete;
    future& operator=(future&&) noexcept;
    shared_future<R> share() noexcept;

    // retrieving the value
    see below get();

    // functions to check state
    bool valid() const noexcept;

    void wait() const;
    template <class Rep, class Period>
      future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
    template <class Clock, class Duration>
      future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
  };
}
```

The implementation shall provide the template `future` and two
specializations, `future<R&>` and `future<{}void>`. These differ only in
the return type and return value of the member function `get`, as set
out in its description, below.

``` cpp
future() noexcept;
```

*Effects:* Constructs an *empty* `future` object that does not refer to
a shared state.

*Postconditions:* `valid() == false`.

``` cpp
future(future&& rhs) noexcept;
```

*Effects:* Move constructs a `future` object that refers to the shared
state that was originally referred to by `rhs` (if any).

*Postconditions:*

- `valid()` returns the same value as `rhs.valid()` prior to the
  constructor invocation.
- `rhs.valid() == false`.

``` cpp
~future();
```

*Effects:*

- Releases any shared state ([[futures.state]]);
- destroys `*this`.

``` cpp
future& operator=(future&& rhs) noexcept;
```

*Effects:*

- Releases any shared state ([[futures.state]]).
- move assigns the contents of `rhs` to `*this`.

*Postconditions:*

- `valid()` returns the same value as `rhs.valid()` prior to the
  assignment.
- `rhs.valid() == false`.

``` cpp
shared_future<R> share() noexcept;
```

*Returns:* `shared_future<R>(std::move(*this))`.

*Postconditions:* `valid() == false`.

``` cpp
R future::get();
R& future<R&>::get();
void future<void>::get();
```

[*Note 1*: As described above, the template and its two required
specializations differ only in the return type and return value of the
member function `get`. — *end note*]

*Effects:*

- `wait()`s until the shared state is ready, then retrieves the value
  stored in the shared state;
- releases any shared state ([[futures.state]]).

*Returns:*

- `future::get()` returns the value `v` stored in the object’s shared
  state as `std::move(v)`.
- `future<R&>::get()` returns the reference stored as value in the
  object’s shared state.
- `future<void>::get()` returns nothing.

*Throws:* the stored exception, if an exception was stored in the shared
state.

*Postconditions:* `valid() == false`.

``` cpp
bool valid() const noexcept;
```

*Returns:* `true` only if `*this` refers to a shared state.

``` cpp
void wait() const;
```

*Effects:* Blocks until the shared state is ready.

``` cpp
template <class Rep, class Period>
  future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
```

*Effects:* None if the shared state contains a deferred
function ([[futures.async]]), otherwise blocks until the shared state
is ready or until the relative timeout ([[thread.req.timing]])
specified by `rel_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  relative timeout ([[thread.req.timing]]) specified by `rel_time` has
  expired.

*Throws:* timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Clock, class Duration>
  future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
```

*Effects:* None if the shared state contains a deferred
function ([[futures.async]]), otherwise blocks until the shared state
is ready or until the absolute timeout ([[thread.req.timing]])
specified by `abs_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  absolute timeout ([[thread.req.timing]]) specified by `abs_time` has
  expired.

*Throws:* timeout-related exceptions ([[thread.req.timing]]).

### Class template `shared_future` <a id="futures.shared_future">[[futures.shared_future]]</a>

The class template `shared_future` defines a type for asynchronous
return objects which may share their shared state with other
asynchronous return objects. A default-constructed `shared_future`
object has no shared state. A `shared_future` object with shared state
can be created by conversion from a `future` object and shares its
shared state with the original asynchronous provider (
[[futures.state]]) of the shared state. The result (value or exception)
of a `shared_future` object can be set by calling a respective function
on an object that shares the same shared state.

[*Note 1*: Member functions of `shared_future` do not synchronize with
themselves, but they synchronize with the shared state. — *end note*]

The effect of calling any member function other than the destructor, the
move-assignment operator, the copy-assignment operator, or `valid()` on
a `shared_future` object for which `valid() == false` is undefined.

[*Note 2*: It is valid to copy or move from a `shared_future` object
for which `valid()` is `false`. — *end note*]

[*Note 3*: Implementations are encouraged to detect this case and throw
an object of type `future_error` with an error condition of
`future_errc::no_state`. — *end note*]

``` cpp
namespace std {
  template <class R>
  class shared_future {
  public:
    shared_future() noexcept;
    shared_future(const shared_future& rhs) noexcept;
    shared_future(future<R>&&) noexcept;
    shared_future(shared_future&& rhs) noexcept;
    ~shared_future();
    shared_future& operator=(const shared_future& rhs) noexcept;
    shared_future& operator=(shared_future&& rhs) noexcept;

    // retrieving the value
    see below get() const;

    // functions to check state
    bool valid() const noexcept;

    void wait() const;
    template <class Rep, class Period>
      future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
    template <class Clock, class Duration>
      future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
  };
}
```

The implementation shall provide the template `shared_future` and two
specializations, `shared_future<R&>` and `shared_future<void>`. These
differ only in the return type and return value of the member function
`get`, as set out in its description, below.

``` cpp
shared_future() noexcept;
```

*Effects:* Constructs an *empty* `shared_future` object that does not
refer to a shared state.

*Postconditions:* `valid() == false`.

``` cpp
shared_future(const shared_future& rhs) noexcept;
```

*Effects:* Constructs a `shared_future` object that refers to the same
shared state as `rhs` (if any).

*Postconditions:* `valid()` returns the same value as `rhs.valid()`.

``` cpp
shared_future(future<R>&& rhs) noexcept;
shared_future(shared_future&& rhs) noexcept;
```

*Effects:* Move constructs a `shared_future` object that refers to the
shared state that was originally referred to by `rhs` (if any).

*Postconditions:*

- `valid()` returns the same value as `rhs.valid()` returned prior to
  the constructor invocation.
- `rhs.valid() == false`.

``` cpp
~shared_future();
```

*Effects:*

- Releases any shared state ([[futures.state]]);
- destroys `*this`.

``` cpp
shared_future& operator=(shared_future&& rhs) noexcept;
```

*Effects:*

- Releases any shared state ([[futures.state]]);
- move assigns the contents of `rhs` to `*this`.

*Postconditions:*

- `valid()` returns the same value as `rhs.valid()` returned prior to
  the assignment.
- `rhs.valid() == false`.

``` cpp
shared_future& operator=(const shared_future& rhs) noexcept;
```

*Effects:*

- Releases any shared state ([[futures.state]]);
- assigns the contents of `rhs` to `*this`. \[*Note 4*: As a result,
  `*this` refers to the same shared state as `rhs` (if
  any). — *end note*]

*Postconditions:* `valid() == rhs.valid()`.

``` cpp
const R& shared_future::get() const;
R& shared_future<R&>::get() const;
void shared_future<void>::get() const;
```

[*Note 1*: As described above, the template and its two required
specializations differ only in the return type and return value of the
member function `get`. — *end note*]

[*Note 2*: Access to a value object stored in the shared state is
unsynchronized, so programmers should apply only those operations on `R`
that do not introduce a data
race ([[intro.multithread]]). — *end note*]

*Effects:* `wait()`s until the shared state is ready, then retrieves the
value stored in the shared state.

*Returns:*

- `shared_future::get()` returns a const reference to the value stored
  in the object’s shared state. \[*Note 5*: Access through that
  reference after the shared state has been destroyed produces undefined
  behavior; this can be avoided by not storing the reference in any
  storage with a greater lifetime than the `shared_future` object that
  returned the reference. — *end note*]
- `shared_future<R&>::get()` returns the reference stored as value in
  the object’s shared state.
- `shared_future<void>::get()` returns nothing.

*Throws:* the stored exception, if an exception was stored in the shared
state.

``` cpp
bool valid() const noexcept;
```

*Returns:* `true` only if `*this` refers to a shared state.

``` cpp
void wait() const;
```

*Effects:* Blocks until the shared state is ready.

``` cpp
template <class Rep, class Period>
  future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
```

*Effects:* None if the shared state contains a deferred
function ([[futures.async]]), otherwise blocks until the shared state
is ready or until the relative timeout ([[thread.req.timing]])
specified by `rel_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  relative timeout ([[thread.req.timing]]) specified by `rel_time` has
  expired.

*Throws:* timeout-related exceptions ([[thread.req.timing]]).

``` cpp
template <class Clock, class Duration>
  future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
```

*Effects:* None if the shared state contains a deferred
function ([[futures.async]]), otherwise blocks until the shared state
is ready or until the absolute timeout ([[thread.req.timing]])
specified by `abs_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  absolute timeout ([[thread.req.timing]]) specified by `abs_time` has
  expired.

*Throws:* timeout-related exceptions ([[thread.req.timing]]).

### Function template `async` <a id="futures.async">[[futures.async]]</a>

The function template `async` provides a mechanism to launch a function
potentially in a new thread and provides the result of the function in a
`future` object with which it shares a shared state.

``` cpp
template <class F, class... Args>
  future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
    async(F&& f, Args&&... args);
template <class F, class... Args>
  future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
    async(launch policy, F&& f, Args&&... args);
```

*Requires:* `F` and each `Ti` in `Args` shall satisfy the
`MoveConstructible` requirements, and

``` cpp
INVOKE(DECAY_COPY(std::forward<F>(f)),
       DECAY_COPY(std::forward<Args>(args))...)     // see REF:func.require, REF:thread.thread.constr
```

shall be a valid expression.

*Effects:* The first function behaves the same as a call to the second
function with a `policy` argument of `launch::async | launch::deferred`
and the same arguments for `F` and `Args`. The second function creates a
shared state that is associated with the returned `future` object. The
further behavior of the second function depends on the `policy` argument
as follows (if more than one of these conditions applies, the
implementation may choose any of the corresponding policies):

- If `launch::async` is set in `policy`, calls
  *INVOKE*(*DECAY_COPY*(std::forward\<F\>(f)),
  *DECAY_COPY*(std::forward\<Args\>(args))...) ([[func.require]],
  [[thread.thread.constr]]) as if in a new thread of execution
  represented by a `thread` object with the calls to *DECAY_COPY*()
  being evaluated in the thread that called `async`. Any return value is
  stored as the result in the shared state. Any exception propagated
  from the execution of *INVOKE*(*DECAY_COPY*(std::forward\<F\>(f)),
  *DECAY_COPY*(std::forward\<Args\>(args))...) is stored as the
  exceptional result in the shared state. The `thread` object is stored
  in the shared state and affects the behavior of any asynchronous
  return objects that reference that state.
- If `launch::deferred` is set in `policy`, stores
  *DECAY_COPY*(std::forward\<F\>(f)) and
  *DECAY_COPY*(std::forward\<Args\>(args))... in the shared state. These
  copies of `f` and `args` constitute a *deferred function*. Invocation
  of the deferred function evaluates *INVOKE*(std::move(g),
  std::move(xyz)) where `g` is the stored value of
  *DECAY_COPY*(std::forward\<F\>(f)) and `xyz` is the stored copy of
  *DECAY_COPY*(std::forward\<Args\>(args)).... Any return value is
  stored as the result in the shared state. Any exception propagated
  from the execution of the deferred function is stored as the
  exceptional result in the shared state. The shared state is not made
  ready until the function has completed. The first call to a non-timed
  waiting function ([[futures.state]]) on an asynchronous return object
  referring to this shared state shall invoke the deferred function in
  the thread that called the waiting function. Once evaluation of
  *INVOKE*(std::move(g), std::move(xyz)) begins, the function is no
  longer considered deferred. \[*Note 1*: If this policy is specified
  together with other policies, such as when using a `policy` value of
  `launch::async | launch::deferred`, implementations should defer
  invocation or the selection of the policy when no more concurrency can
  be effectively exploited. — *end note*]
- If no value is set in the launch policy, or a value is set that is
  neither specified in this International Standard nor by the
  implementation, the behavior is undefined.

*Returns:* An object of type
`future<invoke_result_t<decay_t<F>, decay_t<Args>...>``>` that refers to
the shared state created by this call to `async`.

[*Note 1*: If a future obtained from `async` is moved outside the local
scope, other code that uses the future must be aware that the future’s
destructor may block for the shared state to become
ready. — *end note*]

*Synchronization:* Regardless of the provided `policy` argument,

- the invocation of `async` synchronizes with ([[intro.multithread]])
  the invocation of `f`. \[*Note 2*: This statement applies even when
  the corresponding `future` object is moved to another
  thread. — *end note*] ; and
- the completion of the function `f` is sequenced
  before ([[intro.multithread]]) the shared state is made ready.
  \[*Note 3*: `f` might not be called at all, so its completion might
  never happen. — *end note*]

If the implementation chooses the `launch::async` policy,

- a call to a waiting function on an asynchronous return object that
  shares the shared state created by this `async` call shall block until
  the associated thread has completed, as if joined, or else time
  out ([[thread.thread.member]]);
- the associated thread completion synchronizes
  with ([[intro.multithread]]) the return from the first function that
  successfully detects the ready status of the shared state or with the
  return from the last function that releases the shared state,
  whichever happens first.

*Throws:* `system_error` if `policy == launch::async` and the
implementation is unable to start a new thread, or `std::bad_alloc` if
memory for the internal data structures could not be allocated.

*Error conditions:*

- `resource_unavailable_try_again` — if `policy == launch::async` and
  the system is unable to start a new thread.

[*Note 4*: Line \#1 might not result in concurrency because the `async`
call uses the default policy, which may use `launch::deferred`, in which
case the lambda might not be invoked until the `get()` call; in that
case, `work1` and `work2` are called on the same thread and there is no
concurrency. — *end note*]

### Class template `packaged_task` <a id="futures.task">[[futures.task]]</a>

The class template `packaged_task` defines a type for wrapping a
function or callable object so that the return value of the function or
callable object is stored in a future when it is invoked.

When the `packaged_task` object is invoked, its stored task is invoked
and the result (whether normal or exceptional) stored in the shared
state. Any futures that share the shared state will then be able to
access the stored result.

``` cpp
namespace std {
  template<class> class packaged_task; // not defined

  template<class R, class... ArgTypes>
  class packaged_task<R(ArgTypes...)> {
  public:
    // construction and destruction
    packaged_task() noexcept;
    template <class F>
      explicit packaged_task(F&& f);
    ~packaged_task();

    // no copy
    packaged_task(const packaged_task&) = delete;
    packaged_task& operator=(const packaged_task&) = delete;

    // move support
    packaged_task(packaged_task&& rhs) noexcept;
    packaged_task& operator=(packaged_task&& rhs) noexcept;
    void swap(packaged_task& other) noexcept;

    bool valid() const noexcept;

    // result retrieval
    future<R> get_future();

    // execution
    void operator()(ArgTypes... );
    void make_ready_at_thread_exit(ArgTypes...);

    void reset();
  };
  template <class R, class... ArgTypes>
    void swap(packaged_task<R(ArgTypes...)>& x, packaged_task<R(ArgTypes...)>& y) noexcept;
  template <class R, class Alloc>
    struct uses_allocator<packaged_task<R>, Alloc>;
}
```

#### `packaged_task` member functions <a id="futures.task.members">[[futures.task.members]]</a>

``` cpp
packaged_task() noexcept;
```

*Effects:* Constructs a `packaged_task` object with no shared state and
no stored task.

``` cpp
template <class F>
  packaged_task(F&& f);
```

*Requires:* *INVOKE*\<R\>(f, t1, t2, ..., tN), where `t1, t2, ..., tN`
are values of the corresponding types in `ArgTypes...`, shall be a valid
expression. Invoking a copy of `f` shall behave the same as invoking
`f`.

*Remarks:* This constructor shall not participate in overload resolution
if `decay_t<F>` is the same type as `packaged_task<R(ArgTypes...)>`.

*Effects:* Constructs a new `packaged_task` object with a shared state
and initializes the object’s stored task with `std::forward<F>(f)`.

*Throws:*

- Any exceptions thrown by the copy or move constructor of `f`.
- For the first version, `bad_alloc` if memory for the internal data
  structures could not be allocated.
- For the second version, any exceptions thrown by
  `allocator_traits<Allocator>::template`
  `rebind_traits<`*`unspecified`*`>::allocate`.

``` cpp
packaged_task(packaged_task&& rhs) noexcept;
```

*Effects:* Constructs a new `packaged_task` object and transfers
ownership of `rhs`’s shared state to `*this`, leaving `rhs` with no
shared state. Moves the stored task from `rhs` to `*this`.

*Postconditions:* `rhs` has no shared state.

``` cpp
packaged_task& operator=(packaged_task&& rhs) noexcept;
```

*Effects:*

- Releases any shared state ([[futures.state]]);
- calls `packaged_task(std::move(rhs)).swap(*this)`.

``` cpp
~packaged_task();
```

*Effects:* Abandons any shared state ([[futures.state]]).

``` cpp
void swap(packaged_task& other) noexcept;
```

*Effects:* Exchanges the shared states and stored tasks of `*this` and
`other`.

*Postconditions:* `*this` has the same shared state and stored task (if
any) as `other` prior to the call to `swap`. `other` has the same shared
state and stored task (if any) as `*this` prior to the call to `swap`.

``` cpp
bool valid() const noexcept;
```

*Returns:* `true` only if `*this` has a shared state.

``` cpp
future<R> get_future();
```

*Returns:* A `future` object that shares the same shared state as
`*this`.

*Throws:* a `future_error` object if an error occurs.

*Error conditions:*

- `future_already_retrieved` if `get_future` has already been called on
  a `packaged_task` object with the same shared state as `*this`.
- `no_state` if `*this` has no shared state.

``` cpp
void operator()(ArgTypes... args);
```

*Effects:* As if by *INVOKE*\<R\>(f, t1, t2, ..., tN), where `f` is the
stored task of `*this` and `t1, t2, ..., tN` are the values in
`args...`. If the task returns normally, the return value is stored as
the asynchronous result in the shared state of `*this`, otherwise the
exception thrown by the task is stored. The shared state of `*this` is
made ready, and any threads blocked in a function waiting for the shared
state of `*this` to become ready are unblocked.

*Throws:* a `future_error` exception object if there is no shared state
or the stored task has already been invoked.

*Error conditions:*

- `promise_already_satisfied` if the stored task has already been
  invoked.
- `no_state` if `*this` has no shared state.

``` cpp
void make_ready_at_thread_exit(ArgTypes... args);
```

*Effects:* As if by *INVOKE*\<R\>(f, t1, t2, ..., tN), where `f` is the
stored task and `t1, t2, ..., tN` are the values in `args...`. If the
task returns normally, the return value is stored as the asynchronous
result in the shared state of `*this`, otherwise the exception thrown by
the task is stored. In either case, this shall be done without making
that state ready ([[futures.state]]) immediately. Schedules the shared
state to be made ready when the current thread exits, after all objects
of thread storage duration associated with the current thread have been
destroyed.

*Throws:* `future_error` if an error condition occurs.

*Error conditions:*

- `promise_already_satisfied` if the stored task has already been
  invoked.
- `no_state` if `*this` has no shared state.

``` cpp
void reset();
```

*Effects:* As if `*this = packaged_task(std::move(f))`, where `f` is the
task stored in `*this`.

[*Note 1*: This constructs a new shared state for `*this`. The old
state is abandoned ([[futures.state]]). — *end note*]

*Throws:*

- `bad_alloc` if memory for the new shared state could not be allocated.
- any exception thrown by the move constructor of the task stored in the
  shared state.
- `future_error` with an error condition of `no_state` if `*this` has no
  shared state.

#### `packaged_task` globals <a id="futures.task.nonmembers">[[futures.task.nonmembers]]</a>

``` cpp
template <class R, class... ArgTypes>
  void swap(packaged_task<R(ArgTypes...)>& x, packaged_task<R(ArgTypes...)>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

``` cpp
template <class R, class Alloc>
  struct uses_allocator<packaged_task<R>, Alloc>
    : true_type { };
```

*Requires:* `Alloc` shall be an Allocator ([[allocator.requirements]]).

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[allocator.requirements]: library.md#allocator.requirements
[atomics]: atomics.md#atomics
[basic.life]: basic.md#basic.life
[basic.stc.thread]: basic.md#basic.stc.thread
[bitmask.types]: library.md#bitmask.types
[class]: class.md#class
[condition_variable.syn]: #condition_variable.syn
[except.terminate]: except.md#except.terminate
[func.require]: utilities.md#func.require
[future.syn]: #future.syn
[futures]: #futures
[futures.async]: #futures.async
[futures.errors]: #futures.errors
[futures.future_error]: #futures.future_error
[futures.overview]: #futures.overview
[futures.promise]: #futures.promise
[futures.shared_future]: #futures.shared_future
[futures.state]: #futures.state
[futures.task]: #futures.task
[futures.task.members]: #futures.task.members
[futures.task.nonmembers]: #futures.task.nonmembers
[futures.unique_future]: #futures.unique_future
[intro.multithread]: intro.md#intro.multithread
[mutex.syn]: #mutex.syn
[res.on.data.races]: library.md#res.on.data.races
[res.on.exception.handling]: library.md#res.on.exception.handling
[shared_mutex.syn]: #shared_mutex.syn
[syserr]: diagnostics.md#syserr
[syserr.syserr]: diagnostics.md#syserr.syserr
[tab:thread.lib.summary]: #tab:thread.lib.summary
[thread]: #thread
[thread.condition]: #thread.condition
[thread.condition.condvar]: #thread.condition.condvar
[thread.condition.condvarany]: #thread.condition.condvarany
[thread.condition.nonmember]: #thread.condition.nonmember
[thread.decaycopy]: #thread.decaycopy
[thread.general]: #thread.general
[thread.lock]: #thread.lock
[thread.lock.algorithm]: #thread.lock.algorithm
[thread.lock.guard]: #thread.lock.guard
[thread.lock.scoped]: #thread.lock.scoped
[thread.lock.shared]: #thread.lock.shared
[thread.lock.shared.cons]: #thread.lock.shared.cons
[thread.lock.shared.locking]: #thread.lock.shared.locking
[thread.lock.shared.mod]: #thread.lock.shared.mod
[thread.lock.shared.obs]: #thread.lock.shared.obs
[thread.lock.unique]: #thread.lock.unique
[thread.lock.unique.cons]: #thread.lock.unique.cons
[thread.lock.unique.locking]: #thread.lock.unique.locking
[thread.lock.unique.mod]: #thread.lock.unique.mod
[thread.lock.unique.obs]: #thread.lock.unique.obs
[thread.mutex]: #thread.mutex
[thread.mutex.class]: #thread.mutex.class
[thread.mutex.recursive]: #thread.mutex.recursive
[thread.mutex.requirements]: #thread.mutex.requirements
[thread.mutex.requirements.general]: #thread.mutex.requirements.general
[thread.mutex.requirements.mutex]: #thread.mutex.requirements.mutex
[thread.once]: #thread.once
[thread.once.callonce]: #thread.once.callonce
[thread.once.onceflag]: #thread.once.onceflag
[thread.req]: #thread.req
[thread.req.exception]: #thread.req.exception
[thread.req.lockable]: #thread.req.lockable
[thread.req.lockable.basic]: #thread.req.lockable.basic
[thread.req.lockable.general]: #thread.req.lockable.general
[thread.req.lockable.req]: #thread.req.lockable.req
[thread.req.lockable.timed]: #thread.req.lockable.timed
[thread.req.native]: #thread.req.native
[thread.req.paramname]: #thread.req.paramname
[thread.req.timing]: #thread.req.timing
[thread.sharedmutex.class]: #thread.sharedmutex.class
[thread.sharedmutex.requirements]: #thread.sharedmutex.requirements
[thread.sharedtimedmutex.class]: #thread.sharedtimedmutex.class
[thread.sharedtimedmutex.requirements]: #thread.sharedtimedmutex.requirements
[thread.syn]: #thread.syn
[thread.thread.algorithm]: #thread.thread.algorithm
[thread.thread.assign]: #thread.thread.assign
[thread.thread.class]: #thread.thread.class
[thread.thread.constr]: #thread.thread.constr
[thread.thread.destr]: #thread.thread.destr
[thread.thread.id]: #thread.thread.id
[thread.thread.member]: #thread.thread.member
[thread.thread.static]: #thread.thread.static
[thread.thread.this]: #thread.thread.this
[thread.threads]: #thread.threads
[thread.timedmutex.class]: #thread.timedmutex.class
[thread.timedmutex.recursive]: #thread.timedmutex.recursive
[thread.timedmutex.requirements]: #thread.timedmutex.requirements
[time]: utilities.md#time
[time.clock]: utilities.md#time.clock
[time.clock.req]: utilities.md#time.clock.req
[time.duration]: utilities.md#time.duration
[time.point]: utilities.md#time.point
[unord.hash]: utilities.md#unord.hash

[^1]: All implementations for which standard time units are meaningful
    must necessarily have a steady clock within their hardware
    implementation.
