# Thread support library <a id="thread">[[thread]]</a>

## General <a id="thread.general">[[thread.general]]</a>

The following subclauses describe components to create and manage
threads [[intro.multithread]], perform mutual exclusion, and communicate
conditions and values between threads, as summarized in
[[thread.summary]].

**Table: Thread support library summary** <a id="thread.summary">[thread.summary]</a>

| Subclause            |                     | Header                      |
| -------------------- | ------------------- | --------------------------- |
| [[thread.req]]       | Requirements        |                             |
| [[thread.stoptoken]] | Stop tokens         | `<stop_token>`              |
| [[thread.threads]]   | Threads             | `<thread>`                  |
| [[thread.mutex]]     | Mutual exclusion    | `<mutex>`, `<shared_mutex>` |
| [[thread.condition]] | Condition variables | `<condition_variable>`      |
| [[thread.sema]]      | Semaphores          | `<semaphore>`               |
| [[thread.coord]]     | Coordination types  | `<latch>` `<barrier>`       |
| [[futures]]          | Futures             | `<future>`                  |


## Requirements <a id="thread.req">[[thread.req]]</a>

### Template parameter names <a id="thread.req.paramname">[[thread.req.paramname]]</a>

Throughout this Clause, the names of template parameters are used to
express type requirements. If a template parameter is named `Predicate`,
`operator()` applied to the template argument shall return a value that
is convertible to `bool`. If a template parameter is named `Clock`, the
corresponding template argument shall be a type `C` for which
`is_clock_v<C>` is `true`; otherwise the program is ill-formed.

### Exceptions <a id="thread.req.exception">[[thread.req.exception]]</a>

Some functions described in this Clause are specified to throw
exceptions of type `system_error` [[syserr.syserr]]. Such exceptions are
thrown if any of the function’s error conditions is detected or a call
to an operating system or other underlying API results in an error that
prevents the library function from meeting its specifications. Failure
to allocate storage is reported as described in 
[[res.on.exception.handling]].

[*Example 1*: Consider a function in this clause that is specified to
throw exceptions of type `system_error` and specifies error conditions
that include `operation_not_permitted` for a thread that does not have
the privilege to perform the operation. Assume that, during the
execution of this function, an `errno` of `EPERM` is reported by a POSIX
API call used by the implementation. Since POSIX specifies an `errno` of
`EPERM` when “the caller does not have the privilege to perform the
operation”, the implementation maps `EPERM` to an `error_condition` of
`operation_not_permitted` [[syserr]] and an exception of type
`system_error` is thrown. — *end example*]

The `error_code` reported by such an exception’s `code()` member
function compares equal to one of the conditions specified in the
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

The functions whose names end in `_for` take an argument that specifies
a duration. These functions produce relative timeouts. Implementations
should use a steady clock to measure time for these functions.[^1] Given
a duration argument Dₜ, the real-time duration of the timeout is
Dₜ + Dᵢ + Dₘ.

The functions whose names end in `_until` take an argument that
specifies a time point. These functions produce absolute timeouts.
Implementations should use the clock specified in the time point to
measure time for these functions. Given a clock time point argument Cₜ,
the clock time point of the return from timeout should be Cₜ + Dᵢ + Dₘ
when the clock is not adjusted during the timeout. If the clock is
adjusted to the time Cₐ during the timeout, the behavior should be as
follows:

- if Cₐ > Cₜ, the waiting function should wake as soon as possible,
  i.e., Cₐ + Dᵢ + Dₘ, since the timeout is already satisfied. This
  specification may result in the total duration of the wait decreasing
  when measured against a steady clock.
- if Cₐ ≤ Cₜ, the waiting function should not time out until
  `Clock::now()` returns a time Cₙ ≥ Cₜ, i.e., waking at Cₜ + Dᵢ + Dₘ.
  \[*Note 1*: When the clock is adjusted backwards, this specification
  can result in the total duration of the wait increasing when measured
  against a steady clock. When the clock is adjusted forwards, this
  specification can result in the total duration of the wait decreasing
  when measured against a steady clock. — *end note*]

An implementation returns from such a timeout at any point from the time
specified above to the time it would return from a steady-clock relative
timeout on the difference between Cₜ and the time point of the call to
the `_until` function.

[*Note 2*: Implementations should decrease the duration of the wait
when the clock is adjusted forwards. — *end note*]

[*Note 3*: If the clock is not synchronized with a steady clock, e.g.,
a CPU time clock, these timeouts might not provide useful
functionality. — *end note*]

The resolution of timing provided by an implementation depends on both
operating system and hardware. The finest resolution provided by an
implementation is called the *native resolution*.

Implementation-provided clocks that are used for these functions meet
the *Cpp17TrivialClock* requirements [[time.clock.req]].

A function that takes an argument which specifies a timeout will throw
if, during its execution, a clock, time point, or time duration throws
an exception. Such exceptions are referred to as *timeout-related
exceptions*.

[*Note 4*: Instantiations of clock, time point and duration types
supplied by the implementation as specified in  [[time.clock]] do not
throw exceptions. — *end note*]

### Requirements for *Cpp17Lockable* types <a id="thread.req.lockable">[[thread.req.lockable]]</a>

#### In general <a id="thread.req.lockable.general">[[thread.req.lockable.general]]</a>

An *execution agent* is an entity such as a thread that may perform work
in parallel with other execution agents.

[*Note 1*: Implementations or users can introduce other kinds of agents
such as processes or thread-pool tasks. — *end note*]

The calling agent is determined by context, e.g., the calling thread
that contains the call, and so on.

[*Note 2*: Some lockable objects are “agent oblivious” in that they
work for any execution agent model because they do not determine or
store the agent’s ID (e.g., an ordinary spin lock). — *end note*]

The standard library templates `unique_lock` [[thread.lock.unique]],
`shared_lock` [[thread.lock.shared]], `scoped_lock`
[[thread.lock.scoped]], `lock_guard` [[thread.lock.guard]], `lock`,
`try_lock` [[thread.lock.algorithm]], and `condition_variable_any`
[[thread.condition.condvarany]] all operate on user-supplied lockable
objects. The *Cpp17BasicLockable* requirements, the *Cpp17Lockable*
requirements, and the *Cpp17TimedLockable* requirements list the
requirements imposed by these library types in order to acquire or
release ownership of a `lock` by a given execution agent.

[*Note 3*: The nature of any lock ownership and any synchronization it
entails are not part of these requirements. — *end note*]

#### *Cpp17BasicLockable* requirements <a id="thread.req.lockable.basic">[[thread.req.lockable.basic]]</a>

A type `L` meets the *Cpp17BasicLockable* requirements if the following
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

*Preconditions:* The current execution agent holds a lock on `m`.

*Effects:* Releases a lock on `m` held by the current execution agent.

*Throws:* Nothing.

#### *Cpp17Lockable* requirements <a id="thread.req.lockable.req">[[thread.req.lockable.req]]</a>

A type `L` meets the *Cpp17Lockable* requirements if it meets the
*Cpp17BasicLockable* requirements and the following expressions are
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

#### *Cpp17TimedLockable* requirements <a id="thread.req.lockable.timed">[[thread.req.lockable.timed]]</a>

A type `L` meets the *Cpp17TimedLockable* requirements if it meets the
*Cpp17Lockable* requirements and the following expressions are
well-formed and have the specified semantics (`m` denotes a value of
type `L`, `rel_time` denotes a value of an instantiation of `duration`
[[time.duration]], and `abs_time` denotes a value of an instantiation of
`time_point` [[time.point]]).

``` cpp
m.try_lock_for(rel_time)
```

*Effects:* Attempts to acquire a lock for the current execution agent
within the relative timeout [[thread.req.timing]] specified by
`rel_time`. The function will not return within the timeout specified by
`rel_time` unless it has obtained a lock on `m` for the current
execution agent. If an exception is thrown then a lock has not been
acquired for the current execution agent.

*Return type:* `bool`.

*Returns:* `true` if the lock was acquired, `false` otherwise.

``` cpp
m.try_lock_until(abs_time)
```

*Effects:* Attempts to acquire a lock for the current execution agent
before the absolute timeout [[thread.req.timing]] specified by
`abs_time`. The function will not return before the timeout specified by
`abs_time` unless it has obtained a lock on `m` for the current
execution agent. If an exception is thrown then a lock has not been
acquired for the current execution agent.

*Return type:* `bool`.

*Returns:* `true` if the lock was acquired, `false` otherwise.

## Stop tokens <a id="thread.stoptoken">[[thread.stoptoken]]</a>

### Introduction <a id="thread.stoptoken.intro">[[thread.stoptoken.intro]]</a>

This clause describes components that can be used to asynchonously
request that an operation stops execution in a timely manner, typically
because the result is no longer required. Such a request is called a
*stop request*.

`stop_source`, `stop_token`, and `stop_callback` implement semantics of
shared ownership of a *stop state*. Any `stop_source`, `stop_token`, or
`stop_callback` that shares ownership of the same stop state is an
*associated* `stop_source`, `stop_token`, or `stop_callback`,
respectively. The last remaining owner of the stop state automatically
releases the resources associated with the stop state.

A `stop_token` can be passed to an operation which can either

- actively poll the token to check if there has been a stop request, or
- register a callback using the `stop_callback` class template which
  will be called in the event that a stop request is made.

A stop request made via a `stop_source` will be visible to all
associated `stop_token` and `stop_source` objects. Once a stop request
has been made it cannot be withdrawn (a subsequent stop request has no
effect).

Callbacks registered via a `stop_callback` object are called when a stop
request is first made by any associated `stop_source` object.

Calls to the functions `request_stop`, `stop_requested`, and
`stop_possible` do not introduce data races. A call to `request_stop`
that returns `true` synchronizes with a call to `stop_requested` on an
associated `stop_token` or `stop_source` object that returns `true`.
Registration of a callback synchronizes with the invocation of that
callback.

### Header `<stop_token>` synopsis <a id="thread.stoptoken.syn">[[thread.stoptoken.syn]]</a>

``` cpp
namespace std {
  // [stoptoken], class stop_token
  class stop_token;

  // [stopsource], class stop_source
  class stop_source;

  // no-shared-stop-state indicator
  struct nostopstate_t {
    explicit nostopstate_t() = default;
  };
  inline constexpr nostopstate_t nostopstate{};

  // [stopcallback], class stop_callback
  template<class Callback>
  class stop_callback;
}
```

### Class `stop_token` <a id="stoptoken">[[stoptoken]]</a>

The class `stop_token` provides an interface for querying whether a stop
request has been made (`stop_requested`) or can ever be made
(`stop_possible`) using an associated `stop_source` object (
[[stopsource]]). A `stop_token` can also be passed to a `stop_callback`
[[stopcallback]] constructor to register a callback to be called when a
stop request has been made from an associated `stop_source`.

``` cpp
namespace std {
  class stop_token {
  public:
    // [stoptoken.cons], constructors, copy, and assignment
    stop_token() noexcept;

    stop_token(const stop_token&) noexcept;
    stop_token(stop_token&&) noexcept;
    stop_token& operator=(const stop_token&) noexcept;
    stop_token& operator=(stop_token&&) noexcept;
    ~stop_token();
    void swap(stop_token&) noexcept;

    // [stoptoken.mem], stop handling
    [[nodiscard]] bool stop_requested() const noexcept;
    [[nodiscard]] bool stop_possible() const noexcept;

    [[nodiscard]] friend bool operator==(const stop_token& lhs, const stop_token& rhs) noexcept;
    friend void swap(stop_token& lhs, stop_token& rhs) noexcept;
  };
}
```

#### Constructors, copy, and assignment <a id="stoptoken.cons">[[stoptoken.cons]]</a>

``` cpp
stop_token() noexcept;
```

*Ensures:* `stop_possible()` is `false` and `stop_requested()` is
`false`.

[*Note 1*: Because the created `stop_token` object can never receive a
stop request, no resources are allocated for a stop
state. — *end note*]

``` cpp
stop_token(const stop_token& rhs) noexcept;
```

*Ensures:* `*this == rhs` is `true`.

[*Note 2*: `*this` and `rhs` share the ownership of the same stop
state, if any. — *end note*]

``` cpp
stop_token(stop_token&& rhs) noexcept;
```

*Ensures:* `*this` contains the value of `rhs` prior to the start of
construction and `rhs.stop_possible()` is `false`.

``` cpp
~stop_token();
```

*Effects:* Releases ownership of the stop state, if any.

``` cpp
stop_token& operator=(const stop_token& rhs) noexcept;
```

*Effects:* Equivalent to: `stop_token(rhs).swap(*this)`.

*Returns:* `*this`.

``` cpp
stop_token& operator=(stop_token&& rhs) noexcept;
```

*Effects:* Equivalent to: `stop_token(std::move(rhs)).swap(*this)`.

*Returns:* `*this`.

``` cpp
void swap(stop_token& rhs) noexcept;
```

*Effects:* Exchanges the values of `*this` and `rhs`.

#### Members <a id="stoptoken.mem">[[stoptoken.mem]]</a>

``` cpp
[[nodiscard]] bool stop_requested() const noexcept;
```

*Returns:* `true` if `*this` has ownership of a stop state that has
received a stop request; otherwise, `false`.

``` cpp
[[nodiscard]] bool stop_possible() const noexcept;
```

*Returns:* `false` if:

- `*this` does not have ownership of a stop state, or
- a stop request was not made and there are no associated `stop_source`
  objects;

otherwise, `true`.

#### Non-member functions <a id="stoptoken.nonmembers">[[stoptoken.nonmembers]]</a>

``` cpp
[[nodiscard]] bool operator==(const stop_token& lhs, const stop_token& rhs) noexcept;
```

*Returns:* `true` if `lhs` and `rhs` have ownership of the same stop
state or if both `lhs` and `rhs` do not have ownership of a stop state;
otherwise `false`.

``` cpp
friend void swap(stop_token& x, stop_token& y) noexcept;
```

*Effects:* Equivalent to: `x.swap(y)`.

### Class `stop_source` <a id="stopsource">[[stopsource]]</a>

The class `stop_source` implements the semantics of making a stop
request. A stop request made on a `stop_source` object is visible to all
associated `stop_source` and `stop_token` ([[stoptoken]]) objects. Once
a stop request has been made it cannot be withdrawn (a subsequent stop
request has no effect).

``` cpp
namespace std {
  // no-shared-stop-state indicator
  struct nostopstate_t {
    explicit nostopstate_t() = default;
  };
  inline constexpr nostopstate_t nostopstate{};

  class stop_source {
  public:
    // [stopsource.cons], constructors, copy, and assignment
    stop_source();
    explicit stop_source(nostopstate_t) noexcept;

    stop_source(const stop_source&) noexcept;
    stop_source(stop_source&&) noexcept;
    stop_source& operator=(const stop_source&) noexcept;
    stop_source& operator=(stop_source&&) noexcept;
    ~stop_source();
    void swap(stop_source&) noexcept;

    // [stopsource.mem], stop handling
    [[nodiscard]] stop_token get_token() const noexcept;
    [[nodiscard]] bool stop_possible() const noexcept;
    [[nodiscard]] bool stop_requested() const noexcept;
    bool request_stop() noexcept;

    [[nodiscard]] friend bool
      operator==(const stop_source& lhs, const stop_source& rhs) noexcept;
    friend void swap(stop_source& lhs, stop_source& rhs) noexcept;
  };
}
```

#### Constructors, copy, and assignment <a id="stopsource.cons">[[stopsource.cons]]</a>

``` cpp
stop_source();
```

*Effects:* Initialises `*this` to have ownership of a new stop state.

*Ensures:* `stop_possible()` is `true` and `stop_requested()` is
`false`.

*Throws:* `bad_alloc` if memory could not be allocated for the stop
state.

``` cpp
explicit stop_source(nostopstate_t) noexcept;
```

*Ensures:* `stop_possible()` is `false` and `stop_requested()` is
`false`.

[*Note 1*: No resources are allocated for the state. — *end note*]

``` cpp
stop_source(const stop_source& rhs) noexcept;
```

*Ensures:* `*this == rhs` is `true`.

[*Note 2*: `*this` and `rhs` share the ownership of the same stop
state, if any. — *end note*]

``` cpp
stop_source(stop_source&& rhs) noexcept;
```

*Ensures:* `*this` contains the value of `rhs` prior to the start of
construction and `rhs.stop_possible()` is `false`.

``` cpp
~stop_source();
```

*Effects:* Releases ownership of the stop state, if any.

``` cpp
stop_source& operator=(const stop_source& rhs) noexcept;
```

*Effects:* Equivalent to: `stop_source(rhs).swap(*this)`.

*Returns:* `*this`.

``` cpp
stop_source& operator=(stop_source&& rhs) noexcept;
```

*Effects:* Equivalent to: `stop_source(std::move(rhs)).swap(*this)`.

*Returns:* `*this`.

``` cpp
void swap(stop_source& rhs) noexcept;
```

*Effects:* Exchanges the values of `*this` and `rhs`.

#### Members <a id="stopsource.mem">[[stopsource.mem]]</a>

``` cpp
[[nodiscard]] stop_token get_token() const noexcept;
```

*Returns:* `stop_token()` if `stop_possible()` is `false`; otherwise a
new associated `stop_token` object.

``` cpp
[[nodiscard]] bool stop_possible() const noexcept;
```

*Returns:* `true` if `*this` has ownership of a stop state; otherwise,
`false`.

``` cpp
[[nodiscard]] bool stop_requested() const noexcept;
```

*Returns:* `true` if `*this` has ownership of a stop state that has
received a stop request; otherwise, `false`.

``` cpp
bool request_stop() noexcept;
```

*Effects:* If `*this` does not have ownership of a stop state, returns
`false`. Otherwise, atomically determines whether the owned stop state
has received a stop request, and if not, makes a stop request. The
determination and making of the stop request are an atomic
read-modify-write operation [[intro.races]]. If the request was made,
the callbacks registered by associated `stop_callback` objects are
synchronously called. If an invocation of a callback exits via an
exception then `terminate` is called [[except.terminate]].

[*Note 1*: A stop request includes notifying all condition variables of
type `condition_variable_any` temporarily registered during an
interruptible wait [[thread.condvarany.intwait]]. — *end note*]

*Ensures:* `stop_possible()` is `false` or `stop_requested()` is `true`.

*Returns:* `true` if this call made a stop request; otherwise `false`.

#### Non-member functions <a id="stopsource.nonmembers">[[stopsource.nonmembers]]</a>

``` cpp
[[nodiscard]] friend bool
  operator==(const stop_source& lhs, const stop_source& rhs) noexcept;
```

*Returns:* `true` if `lhs` and `rhs` have ownership of the same stop
state or if both `lhs` and `rhs` do not have ownership of a stop state;
otherwise `false`.

``` cpp
friend void swap(stop_source& x, stop_source& y) noexcept;
```

*Effects:* Equivalent to: `x.swap(y)`.

### Class template `stop_callback` <a id="stopcallback">[[stopcallback]]</a>

``` cpp
namespace std {
  template<class Callback>
  class stop_callback {
  public:
    using callback_type = Callback;

    // [stopcallback.cons], constructors and destructor
    template<class C>
    explicit stop_callback(const stop_token& st, C&& cb)
        noexcept(is_nothrow_constructible_v<Callback, C>);
    template<class C>
    explicit stop_callback(stop_token&& st, C&& cb)
        noexcept(is_nothrow_constructible_v<Callback, C>);
    ~stop_callback();

    stop_callback(const stop_callback&) = delete;
    stop_callback(stop_callback&&) = delete;
    stop_callback& operator=(const stop_callback&) = delete;
    stop_callback& operator=(stop_callback&&) = delete;

  private:
    Callback callback;      // exposition only
  };

  template<class Callback>
  stop_callback(stop_token, Callback) -> stop_callback<Callback>;
}
```

*Mandates:* `stop_callback` is instantiated with an argument for the
template parameter `Callback` that satisfies both `invocable` and
`destructible`.

*Preconditions:* `stop_callback` is instantiated with an argument for
the template parameter `Callback` that models both `invocable` and
`destructible`.

#### Constructors and destructor <a id="stopcallback.cons">[[stopcallback.cons]]</a>

``` cpp
template<class C>
explicit stop_callback(const stop_token& st, C&& cb)
  noexcept(is_nothrow_constructible_v<Callback, C>);
template<class C>
explicit stop_callback(stop_token&& st, C&& cb)
  noexcept(is_nothrow_constructible_v<Callback, C>);
```

*Constraints:* `Callback` and `C` satisfy
`constructible_from<Callback, C>`.

*Preconditions:* `Callback` and `C` model
`constructible_from<Callback, C>`.

*Effects:* Initializes `callback` with `std::forward<C>(cb)`. If
`st.stop_requested()` is `true`, then
`std::forward<Callback>(callback)()` is evaluated in the current thread
before the constructor returns. Otherwise, if `st` has ownership of a
stop state, acquires shared ownership of that stop state and registers
the callback with that stop state such that
`std::forward<Callback>(callback)()` is evaluated by the first call to
`request_stop()` on an associated `stop_source`.

*Remarks:* If evaluating `std::forward<Callback>(callback)()` exits via
an exception, then `terminate` is called [[except.terminate]].

*Throws:* Any exception thrown by the initialization of `callback`.

``` cpp
~stop_callback();
```

*Effects:* Unregisters the callback from the owned stop state, if any.
The destructor does not block waiting for the execution of another
callback registered by an associated `stop_callback`. If `callback` is
concurrently executing on another thread, then the return from the
invocation of `callback` strongly happens before [[intro.races]]
`callback` is destroyed. If `callback` is executing on the current
thread, then the destructor does not block [[defns.block]] waiting for
the return from the invocation of `callback`. Releases ownership of the
stop state, if any.

## Threads <a id="thread.threads">[[thread.threads]]</a>

[[thread.threads]] describes components that can be used to create and
manage threads.

[*Note 1*: These threads are intended to map one-to-one with operating
system threads. — *end note*]

### Header `<thread>` synopsis <a id="thread.syn">[[thread.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  class thread;

  void swap(thread& x, thread& y) noexcept;

  // [thread.jthread.class] class jthread
  class jthread;

  namespace this_thread {
    thread::id get_id() noexcept;

    void yield() noexcept;
    template<class Clock, class Duration>
      void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
    template<class Rep, class Period>
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
    // types
    class id;
    using native_handle_type = implementation-defined;         // see~[thread.req.native]

    // construct/copy/destroy
    thread() noexcept;
    template<class F, class... Args> explicit thread(F&& f, Args&&... args);
    ~thread();
    thread(const thread&) = delete;
    thread(thread&&) noexcept;
    thread& operator=(const thread&) = delete;
    thread& operator=(thread&&) noexcept;

    // members
    void swap(thread&) noexcept;
    bool joinable() const noexcept;
    void join();
    void detach();
    id get_id() const noexcept;
    native_handle_type native_handle();                         // see~[thread.req.native]

    // static members
    static unsigned int hardware_concurrency() noexcept;
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
  strong_ordering operator<=>(thread::id x, thread::id y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& out, thread::id id);

  // hash support
  template<class T> struct hash;
  template<> struct hash<thread::id>;
}
```

An object of type `thread::id` provides a unique identifier for each
thread of execution and a single distinct value for all `thread` objects
that do not represent a thread of execution [[thread.thread.class]].
Each thread of execution has an associated `thread::id` object that is
not equal to the `thread::id` object of any other thread of execution
and that is not equal to the `thread::id` object of any `thread` object
that does not represent threads of execution.

`thread::id` is a trivially copyable class [[class.prop]]. The library
may reuse the value of a `thread::id` of a terminated thread that can no
longer be joined.

[*Note 1*: Relational operators allow `thread::id` objects to be used
as keys in associative containers. — *end note*]

``` cpp
id() noexcept;
```

*Ensures:* The constructed object does not represent a thread of
execution.

``` cpp
bool operator==(thread::id x, thread::id y) noexcept;
```

*Returns:* `true` only if `x` and `y` represent the same thread of
execution or neither `x` nor `y` represents a thread of execution.

``` cpp
strong_ordering operator<=>(thread::id x, thread::id y) noexcept;
```

Let P(`x`, `y`) be an unspecified total ordering over `thread::id` as
described in [[alg.sorting]].

*Returns:* `strong_ordering::less` if P(`x`, `y`) is `true`. Otherwise,
`strong_ordering::greater` if P(`y`, `x`) is `true`. Otherwise,
`strong_ordering::equal`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<< (basic_ostream<charT, traits>& out, thread::id id);
```

*Effects:* Inserts an unspecified text representation of `id` into
`out`. For two objects of type `thread::id` `x` and `y`, if `x == y` the
`thread::id` objects have the same text representation and if `x != y`
the `thread::id` objects have distinct text representations.

*Returns:* `out`.

``` cpp
template<> struct hash<thread::id>;
```

The specialization is enabled [[unord.hash]].

#### Constructors <a id="thread.thread.constr">[[thread.thread.constr]]</a>

``` cpp
thread() noexcept;
```

*Effects:* The object does not represent a thread of execution.

*Ensures:* `get_id() == id()`.

``` cpp
template<class F, class... Args> explicit thread(F&& f, Args&&... args);
```

*Constraints:* `remove_cvref_t<F>` is not the same type as `thread`.

*Mandates:* The following are all `true`:

- `is_constructible_v<decay_t<F>, F>`,
- `(is_constructible_v<decay_t<Args>, Args> && ...)`,
- `is_move_constructible_v<decay_t<F>>`,
- `(is_move_constructible_v<decay_t<Args>> && ...)`, and
- `is_invocable_v<decay_t<F>, decay_t<Args>...>`.

*Preconditions:* `decay_t<F>` and each type in `decay_t<Args>` meet the
*Cpp17MoveConstructible* requirements.

*Effects:* The new thread of execution executes

``` cpp
invoke(decay-copy(std::forward<F>(f)), decay-copy(std::forward<Args>(args))...)
```

with the calls to *`decay-copy`* being evaluated in the constructing
thread. Any return value from this invocation is ignored.

[*Note 1*: This implies that any exceptions not thrown from the
invocation of the copy of `f` will be thrown in the constructing thread,
not the new thread. — *end note*]

If the invocation of `invoke` terminates with an uncaught exception,
`terminate` is called.

*Synchronization:* The completion of the invocation of the constructor
synchronizes with the beginning of the invocation of the copy of `f`.

*Ensures:* `get_id() != id()`. `*this` represents the newly started
thread.

*Throws:* `system_error` if unable to start the new thread.

*Error conditions:*

- `resource_unavailable_try_again` — the system lacked the necessary
  resources to create another thread, or the system-imposed limit on the
  number of threads in a process would be exceeded.

``` cpp
thread(thread&& x) noexcept;
```

*Ensures:* `x.get_id() == id()` and `get_id()` returns the value of
`x.get_id()` prior to the start of construction.

#### Destructor <a id="thread.thread.destr">[[thread.thread.destr]]</a>

``` cpp
~thread();
```

*Effects:* If `joinable()`, calls `terminate()`. Otherwise, has no
effects.

[*Note 1*: Either implicitly detaching or joining a `joinable()` thread
in its destructor could result in difficult to debug correctness (for
detach) or performance (for join) bugs encountered only when an
exception is thrown. Thus the programmer must ensure that the destructor
is never executed while the thread is still joinable. — *end note*]

#### Assignment <a id="thread.thread.assign">[[thread.thread.assign]]</a>

``` cpp
thread& operator=(thread&& x) noexcept;
```

*Effects:* If `joinable()`, calls `terminate()`. Otherwise, assigns the
state of `x` to `*this` and sets `x` to a default constructed state.

*Ensures:* `x.get_id() == id()` and `get_id()` returns the value of
`x.get_id()` prior to the assignment.

*Returns:* `*this`.

#### Members <a id="thread.thread.member">[[thread.thread.member]]</a>

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

*Effects:* Blocks until the thread represented by `*this` has completed.

*Synchronization:* The completion of the thread represented by `*this`
synchronizes with [[intro.multithread]] the corresponding successful
`join()` return.

[*Note 1*: Operations on `*this` are not synchronized. — *end note*]

*Ensures:* The thread represented by `*this` has completed.
`get_id() == id()`.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

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
releases any owned resources.

*Ensures:* `get_id() == id()`.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `no_such_process` — if the thread is not valid.
- `invalid_argument` — if the thread is not joinable.

``` cpp
id get_id() const noexcept;
```

*Returns:* A default constructed `id` object if `*this` does not
represent a thread, otherwise `this_thread::get_id()` for the thread of
execution represented by `*this`.

#### Static members <a id="thread.thread.static">[[thread.thread.static]]</a>

``` cpp
unsigned hardware_concurrency() noexcept;
```

*Returns:* The number of hardware thread contexts.

[*Note 1*: This value should only be considered to be a
hint. — *end note*]

If this value is not computable or well-defined, an implementation
should return 0.

#### Specialized algorithms <a id="thread.thread.algorithm">[[thread.thread.algorithm]]</a>

``` cpp
void swap(thread& x, thread& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

### Class `jthread` <a id="thread.jthread.class">[[thread.jthread.class]]</a>

The class `jthread` provides a mechanism to create a new thread of
execution. The functionality is the same as for class `thread`
[[thread.thread.class]] with the additional abilities to provide a
`stop_token` [[thread.stoptoken]] to the new thread of execution, make
stop requests, and automatically join.

``` cpp
namespace std {
  class jthread {
  public:
    // types
    using id = thread::id;
    using native_handle_type = thread::native_handle_type;

    // [thread.jthread.cons], constructors, move, and assignment
    jthread() noexcept;
    template<class F, class... Args> explicit jthread(F&& f, Args&&... args);
    ~jthread();
    jthread(const jthread&) = delete;
    jthread(jthread&&) noexcept;
    jthread& operator=(const jthread&) = delete;
    jthread& operator=(jthread&&) noexcept;

    // [thread.jthread.mem], members
    void swap(jthread&) noexcept;
    [[nodiscard]] bool joinable() const noexcept;
    void join();
    void detach();
    [[nodiscard]] id get_id() const noexcept;
    [[nodiscard]] native_handle_type native_handle();   // see~[thread.req.native]

    // [thread.jthread.stop], stop token handling
    [[nodiscard]] stop_source get_stop_source() noexcept;
    [[nodiscard]] stop_token get_stop_token() const noexcept;
    bool request_stop() noexcept;

    // [thread.jthread.special], specialized algorithms
    friend void swap(jthread& lhs, jthread& rhs) noexcept;

    // [thread.jthread.static], static members
    [[nodiscard]] static unsigned int hardware_concurrency() noexcept;

  private:
    stop_source ssource;        // exposition only
  };
}
```

#### Constructors, move, and assignment <a id="thread.jthread.cons">[[thread.jthread.cons]]</a>

``` cpp
jthread() noexcept;
```

*Effects:* Constructs a `jthread` object that does not represent a
thread of execution.

*Ensures:* `get_id() == id()` is `true` and `ssource.stop_possible()` is
`false`.

``` cpp
template<class F, class... Args> explicit jthread(F&& f, Args&&... args);
```

*Constraints:* `remove_cvref_t<F>` is not the same type as `jthread`.

*Mandates:* The following are all `true`:

- `is_constructible_v<decay_t<F>, F>`,
- `(is_constructible_v<decay_t<Args>, Args> && ...)`,
- `is_move_constructible_v<decay_t<F>>`,
- `(is_move_constructible_v<decay_t<Args>> && ...)`, and
- `is_invocable_v<decay_t<F>, decay_t<Args>...> ||`  
  `is_invocable_v<decay_t<F>, stop_token, decay_t<Args>...>`.

*Preconditions:* `decay_t<F>` and each type in `decay_t<Args>` meet the
*Cpp17MoveConstructible* requirements.

*Effects:* Initializes `ssource`. The new thread of execution executes

``` cpp
invoke(decay-copy(std::forward<F>(f)), get_stop_token(),
       decay-copy(std::forward<Args>(args))...)
```

if that expression is well-formed, otherwise

``` cpp
invoke(decay-copy(std::forward<F>(f)), decay-copy(std::forward<Args>(args))...)
```

with the calls to *`decay-copy`* being evaluated in the constructing
thread. Any return value from this invocation is ignored.

[*Note 1*: This implies that any exceptions not thrown from the
invocation of the copy of `f` will be thrown in the constructing thread,
not the new thread. — *end note*]

If the `invoke` expression exits via an exception, `terminate` is
called.

*Synchronization:* The completion of the invocation of the constructor
synchronizes with the beginning of the invocation of the copy of `f`.

*Ensures:* `get_id() != id()` is `true` and `ssource.stop_possible()` is
`true` and `*this` represents the newly started thread.

[*Note 2*: The calling thread can make a stop request only once,
because it cannot replace this stop token. — *end note*]

*Throws:* `system_error` if unable to start the new thread.

*Error conditions:*

- `resource_unavailable_try_again` — the system lacked the necessary
  resources to create another thread, or the system-imposed limit on the
  number of threads in a process would be exceeded.

``` cpp
jthread(jthread&& x) noexcept;
```

*Ensures:* `x.get_id() == id()` and `get_id()` returns the value of
`x.get_id()` prior to the start of construction. `ssource` has the value
of `x.ssource` prior to the start of construction and
`x.ssource.stop_possible()` is `false`.

``` cpp
~jthread();
```

*Effects:* If `joinable()` is `true`, calls `request_stop()` and then
`join()`.

[*Note 3*: Operations on `*this` are not synchronized. — *end note*]

``` cpp
jthread& operator=(jthread&& x) noexcept;
```

*Effects:* If `joinable()` is `true`, calls `request_stop()` and then
`join()`. Assigns the state of `x` to `*this` and sets `x` to a default
constructed state.

*Ensures:* `x.get_id() == id()` and `get_id()` returns the value of
`x.get_id()` prior to the assignment. `ssource` has the value of
`x.ssource` prior to the assignment and `x.ssource.stop_possible()` is
`false`.

*Returns:* `*this`.

#### Members <a id="thread.jthread.mem">[[thread.jthread.mem]]</a>

``` cpp
void swap(jthread& x) noexcept;
```

*Effects:* Exchanges the values of `*this` and `x`.

``` cpp
[[nodiscard]] bool joinable() const noexcept;
```

*Returns:* `get_id() != id()`.

``` cpp
void join();
```

*Effects:* Blocks until the thread represented by `*this` has completed.

*Synchronization:* The completion of the thread represented by `*this`
synchronizes with [[intro.multithread]] the corresponding successful
`join()` return.

[*Note 1*: Operations on `*this` are not synchronized. — *end note*]

*Ensures:* The thread represented by `*this` has completed.
`get_id() == id()`.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

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
releases any owned resources.

*Ensures:* `get_id() == id()`.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `no_such_process` — if the thread is not valid.
- `invalid_argument` — if the thread is not joinable.

``` cpp
id get_id() const noexcept;
```

*Returns:* A default constructed `id` object if `*this` does not
represent a thread, otherwise `this_thread::get_id()` for the thread of
execution represented by `*this`.

#### Stop token handling <a id="thread.jthread.stop">[[thread.jthread.stop]]</a>

``` cpp
[[nodiscard]] stop_source get_stop_source() noexcept;
```

*Effects:* Equivalent to: `return ssource;`

``` cpp
[[nodiscard]] stop_token get_stop_token() const noexcept;
```

*Effects:* Equivalent to: `return ssource.get_token();`

``` cpp
bool request_stop() noexcept;
```

*Effects:* Equivalent to: `return ssource.request_stop();`

#### Specialized algorithms <a id="thread.jthread.special">[[thread.jthread.special]]</a>

``` cpp
friend void swap(jthread& x, jthread& y) noexcept;
```

*Effects:* Equivalent to: `x.swap(y)`.

#### Static members <a id="thread.jthread.static">[[thread.jthread.static]]</a>

``` cpp
[[nodiscard]] static unsigned int hardware_concurrency() noexcept;
```

*Returns:* `thread::hardware_concurrency()`.

### Namespace `this_thread` <a id="thread.thread.this">[[thread.thread.this]]</a>

``` cpp
namespace std::this_thread {
  thread::id get_id() noexcept;

  void yield() noexcept;
  template<class Clock, class Duration>
    void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
  template<class Rep, class Period>
    void sleep_for(const chrono::duration<Rep, Period>& rel_time);
}
```

``` cpp
thread::id this_thread::get_id() noexcept;
```

*Returns:* An object of type `thread::id` that uniquely identifies the
current thread of execution. No other thread of execution has this id
and this thread of execution always has this id. The object returned
does not compare equal to a default constructed `thread::id`.

``` cpp
void this_thread::yield() noexcept;
```

*Effects:* Offers the implementation the opportunity to reschedule.

*Synchronization:* None.

``` cpp
template<class Clock, class Duration>
  void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:* Blocks the calling thread for the absolute
timeout [[thread.req.timing]] specified by `abs_time`.

*Synchronization:* None.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Rep, class Period>
  void sleep_for(const chrono::duration<Rep, Period>& rel_time);
```

*Effects:* Blocks the calling thread for the relative
timeout [[thread.req.timing]] specified by `rel_time`.

*Synchronization:* None.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

## Mutual exclusion <a id="thread.mutex">[[thread.mutex]]</a>

This subclause provides mechanisms for mutual exclusion: mutexes, locks,
and call once. These mechanisms ease the production of race-free
programs [[intro.multithread]].

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

  template<class Mutex> class lock_guard;
  template<class... MutexTypes> class scoped_lock;
  template<class Mutex> class unique_lock;

  template<class Mutex>
    void swap(unique_lock<Mutex>& x, unique_lock<Mutex>& y) noexcept;

  template<class L1, class L2, class... L3> int try_lock(L1&, L2&, L3&...);
  template<class L1, class L2, class... L3> void lock(L1&, L2&, L3&...);

  struct once_flag;

  template<class Callable, class... Args>
    void call_once(once_flag& flag, Callable&& func, Args&&... args);
}
```

### Header `<shared_mutex>` synopsis <a id="shared.mutex.syn">[[shared.mutex.syn]]</a>

``` cpp
namespace std {
  class shared_mutex;
  class shared_timed_mutex;
  template<class Mutex> class shared_lock;
  template<class Mutex>
    void swap(shared_lock<Mutex>& x, shared_lock<Mutex>& y) noexcept;
}
```

### Mutex requirements <a id="thread.mutex.requirements">[[thread.mutex.requirements]]</a>

#### In general <a id="thread.mutex.requirements.general">[[thread.mutex.requirements.general]]</a>

A mutex object facilitates protection against data races and allows safe
synchronization of data between execution agents
[[thread.req.lockable]]. An execution agent *owns* a mutex from the time
it successfully calls one of the lock functions until it calls unlock.
Mutexes can be either recursive or non-recursive, and can grant
simultaneous ownership to one or many execution agents. Both recursive
and non-recursive mutexes are supplied.

#### Mutex types <a id="thread.mutex.requirements.mutex">[[thread.mutex.requirements.mutex]]</a>

The *mutex types* are the standard library types `mutex`,
`recursive_mutex`, `timed_mutex`, `recursive_timed_mutex`,
`shared_mutex`, and `shared_timed_mutex`. They meet the requirements set
out in this subclause. In this description, `m` denotes an object of a
mutex type.

The mutex types meet the *Cpp17Lockable* requirements
[[thread.req.lockable.req]].

The mutex types meet *Cpp17DefaultConstructible* and
*Cpp17Destructible*. If initialization of an object of a mutex type
fails, an exception of type `system_error` is thrown. The mutex types
are neither copyable nor movable.

The error conditions for error codes, if any, reported by member
functions of the mutex types are as follows:

- `resource_unavailable_try_again` — if any native handle type
  manipulated is not available.
- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.
- `invalid_argument` — if any native handle type manipulated as part of
  mutex construction is incorrect.

The implementation provides lock and unlock operations, as described
below. For purposes of determining the existence of a data race, these
behave as atomic operations [[intro.multithread]]. The lock and unlock
operations on a single mutex appears to occur in a single total order.

[*Note 1*: This can be viewed as the modification order
[[intro.multithread]] of the mutex. — *end note*]

[*Note 2*: Construction and destruction of an object of a mutex type
need not be thread-safe; other synchronization should be used to ensure
that mutex objects are initialized and visible to other
threads. — *end note*]

The expression `m.lock()` is well-formed and has the following
semantics:

*Preconditions:* If `m` is of type `mutex`, `timed_mutex`,
`shared_mutex`, or `shared_timed_mutex`, the calling thread does not own
the mutex.

*Effects:* Blocks the calling thread until ownership of the mutex can be
obtained for the calling thread.

*Ensures:* The calling thread owns the mutex.

*Return type:* `void`.

*Synchronization:* Prior `unlock()` operations on the same object
*synchronize with*[[intro.multithread]] this operation.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.
- `resource_deadlock_would_occur` — if the implementation detects that a
  deadlock would occur.

The expression `m.try_lock()` is well-formed and has the following
semantics:

*Preconditions:* If `m` is of type `mutex`, `timed_mutex`,
`shared_mutex`, or `shared_timed_mutex`, the calling thread does not own
the mutex.

*Effects:* Attempts to obtain ownership of the mutex for the calling
thread without blocking. If ownership is not obtained, there is no
effect and `try_lock()` immediately returns. An implementation may fail
to obtain the lock even if it is not held by any other thread.

[*Note 1*: This spurious failure is normally uncommon, but allows
interesting implementations based on a simple compare and
exchange [[atomics]]. — *end note*]

An implementation should ensure that `try_lock()` does not consistently
return `false` in the absence of contending mutex acquisitions.

*Return type:* `bool`.

*Returns:* `true` if ownership of the mutex was obtained for the calling
thread, otherwise `false`.

*Synchronization:* If `try_lock()` returns `true`, prior `unlock()`
operations on the same object *synchronize with*[[intro.multithread]]
this operation.

[*Note 2*: Since `lock()` does not synchronize with a failed subsequent
`try_lock()`, the visibility rules are weak enough that little would be
known about the state after a failure, even in the absence of spurious
failures. — *end note*]

*Throws:* Nothing.

The expression `m.unlock()` is well-formed and has the following
semantics:

*Preconditions:* The calling thread owns the mutex.

*Effects:* Releases the calling thread’s ownership of the mutex.

*Return type:* `void`.

*Synchronization:* This operation synchronizes
with [[intro.multithread]] subsequent lock operations that obtain
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

    using native_handle_type = implementation-defined;          // see~[thread.req.native]
    native_handle_type native_handle();                         // see~[thread.req.native]
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

The class `mutex` meets all of the mutex requirements
[[thread.mutex.requirements]]. It is a standard-layout class
[[class.prop]].

[*Note 4*: A program can deadlock if the thread that owns a `mutex`
object calls `lock()` on that object. If the implementation can detect
the deadlock, a `resource_deadlock_would_occur` error condition might be
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

    using native_handle_type = implementation-defined;          // see~[thread.req.native]
    native_handle_type native_handle();                         // see~[thread.req.native]
  };
}
```

The class `recursive_mutex` provides a recursive mutex with exclusive
ownership semantics. If one thread owns a `recursive_mutex` object,
attempts by another thread to acquire ownership of that object will fail
(for `try_lock()`) or block (for `lock()`) until the first thread has
completely released ownership.

The class `recursive_mutex` meets all of the mutex requirements
[[thread.mutex.requirements]]. It is a standard-layout class
[[class.prop]].

A thread that owns a `recursive_mutex` object may acquire additional
levels of ownership by calling `lock()` or `try_lock()` on that object.
It is unspecified how many levels of ownership may be acquired by a
single thread. If a thread has already acquired the maximum level of
ownership for a `recursive_mutex` object, additional calls to
`try_lock()` fail, and additional calls to `lock()` throw an exception
of type `system_error`. A thread shall call `unlock()` once for each
level of ownership acquired by calls to `lock()` and `try_lock()`. Only
when all levels of ownership have been released may ownership be
acquired by another thread.

The behavior of a program is undefined if:

- it destroys a `recursive_mutex` object owned by any thread or
- a thread terminates while owning a `recursive_mutex` object.

#### Timed mutex types <a id="thread.timedmutex.requirements">[[thread.timedmutex.requirements]]</a>

The *timed mutex types* are the standard library types `timed_mutex`,
`recursive_timed_mutex`, and `shared_timed_mutex`. They meet the
requirements set out below. In this description, `m` denotes an object
of a mutex type, `rel_time` denotes an object of an instantiation of
`duration` [[time.duration]], and `abs_time` denotes an object of an
instantiation of `time_point` [[time.point]].

The timed mutex types meet the *Cpp17TimedLockable* requirements
[[thread.req.lockable.timed]].

The expression `m.try_lock_for(rel_time)` is well-formed and has the
following semantics:

*Preconditions:* If `m` is of type `timed_mutex` or
`shared_timed_mutex`, the calling thread does not own the mutex.

*Effects:* The function attempts to obtain ownership of the mutex within
the relative timeout [[thread.req.timing]] specified by `rel_time`. If
the time specified by `rel_time` is less than or equal to
`rel_time.zero()`, the function attempts to obtain ownership without
blocking (as if by calling `try_lock()`). The function returns within
the timeout specified by `rel_time` only if it has obtained ownership of
the mutex object.

[*Note 1*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

*Return type:* `bool`.

*Returns:* `true` if ownership was obtained, otherwise `false`.

*Synchronization:* If `try_lock_for()` returns `true`, prior `unlock()`
operations on the same object *synchronize with*[[intro.multithread]]
this operation.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

The expression `m.try_lock_until(abs_time)` is well-formed and has the
following semantics:

*Preconditions:* If `m` is of type `timed_mutex` or
`shared_timed_mutex`, the calling thread does not own the mutex.

*Effects:* The function attempts to obtain ownership of the mutex. If
`abs_time` has already passed, the function attempts to obtain ownership
without blocking (as if by calling `try_lock()`). The function returns
before the absolute timeout [[thread.req.timing]] specified by
`abs_time` only if it has obtained ownership of the mutex object.

[*Note 2*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

*Return type:* `bool`.

*Returns:* `true` if ownership was obtained, otherwise `false`.

*Synchronization:* If `try_lock_until()` returns `true`, prior
`unlock()` operations on the same object *synchronize
with*[[intro.multithread]] this operation.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

##### Class `timed_mutex` <a id="thread.timedmutex.class">[[thread.timedmutex.class]]</a>

``` cpp
namespace std {
  class timed_mutex {
  public:
    timed_mutex();
    ~timed_mutex();

    timed_mutex(const timed_mutex&) = delete;
    timed_mutex& operator=(const timed_mutex&) = delete;

    void lock();    // blocking
    bool try_lock();
    template<class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    using native_handle_type = implementation-defined;          // see~[thread.req.native]
    native_handle_type native_handle();                         // see~[thread.req.native]
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

The class `timed_mutex` meets all of the timed mutex requirements
[[thread.timedmutex.requirements]]. It is a standard-layout class
[[class.prop]].

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

    void lock();    // blocking
    bool try_lock() noexcept;
    template<class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    using native_handle_type = implementation-defined;          // see~[thread.req.native]
    native_handle_type native_handle();                         // see~[thread.req.native]
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

The class `recursive_timed_mutex` meets all of the timed mutex
requirements [[thread.timedmutex.requirements]]. It is a standard-layout
class [[class.prop]].

A thread that owns a `recursive_timed_mutex` object may acquire
additional levels of ownership by calling `lock()`, `try_lock()`,
`try_lock_for()`, or `try_lock_until()` on that object. It is
unspecified how many levels of ownership may be acquired by a single
thread. If a thread has already acquired the maximum level of ownership
for a `recursive_timed_mutex` object, additional calls to `try_lock()`,
`try_lock_for()`, or `try_lock_until()` fail, and additional calls to
`lock()` throw an exception of type `system_error`. A thread shall call
`unlock()` once for each level of ownership acquired by calls to
`lock()`, `try_lock()`, `try_lock_for()`, and `try_lock_until()`. Only
when all levels of ownership have been released may ownership of the
object be acquired by another thread.

The behavior of a program is undefined if:

- it destroys a `recursive_timed_mutex` object owned by any thread, or
- a thread terminates while owning a `recursive_timed_mutex` object.

#### Shared mutex types <a id="thread.sharedmutex.requirements">[[thread.sharedmutex.requirements]]</a>

The standard library types `shared_mutex` and `shared_timed_mutex` are
*shared mutex types*. Shared mutex types meet the requirements of mutex
types [[thread.mutex.requirements.mutex]] and additionally meet the
requirements set out below. In this description, `m` denotes an object
of a shared mutex type.

In addition to the exclusive lock ownership mode specified in 
[[thread.mutex.requirements.mutex]], shared mutex types provide a
*shared lock* ownership mode. Multiple execution agents can
simultaneously hold a shared lock ownership of a shared mutex type. But
no execution agent holds a shared lock while another execution agent
holds an exclusive lock on the same shared mutex type, and vice-versa.
The maximum number of execution agents which can share a shared lock on
a single shared mutex type is unspecified, but is at least 10000. If
more than the maximum number of execution agents attempt to obtain a
shared lock, the excess execution agents block until the number of
shared locks are reduced below the maximum amount by other execution
agents releasing their shared lock.

The expression `m.lock_shared()` is well-formed and has the following
semantics:

*Preconditions:* The calling thread has no ownership of the mutex.

*Effects:* Blocks the calling thread until shared ownership of the mutex
can be obtained for the calling thread. If an exception is thrown then a
shared lock has not been acquired for the current thread.

*Ensures:* The calling thread has a shared lock on the mutex.

*Return type:* `void`.

*Synchronization:* Prior `unlock()` operations on the same object
synchronize with [[intro.multithread]] this operation.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.
- `resource_deadlock_would_occur` — if the implementation detects that a
  deadlock would occur.

The expression `m.unlock_shared()` is well-formed and has the following
semantics:

*Preconditions:* The calling thread holds a shared lock on the mutex.

*Effects:* Releases a shared lock on the mutex held by the calling
thread.

*Return type:* `void`.

*Synchronization:* This operation synchronizes
with [[intro.multithread]] subsequent `lock()` operations that obtain
ownership on the same object.

*Throws:* Nothing.

The expression `m.try_lock_shared()` is well-formed and has the
following semantics:

*Preconditions:* The calling thread has no ownership of the mutex.

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
with [[intro.multithread]] this operation.

*Throws:* Nothing.

##### Class `shared_mutex` <a id="thread.sharedmutex.class">[[thread.sharedmutex.class]]</a>

``` cpp
namespace std {
  class shared_mutex {
  public:
    shared_mutex();
    ~shared_mutex();

    shared_mutex(const shared_mutex&) = delete;
    shared_mutex& operator=(const shared_mutex&) = delete;

    // exclusive ownership
    void lock();                // blocking
    bool try_lock();
    void unlock();

    // shared ownership
    void lock_shared();         // blocking
    bool try_lock_shared();
    void unlock_shared();

    using native_handle_type = implementation-defined;          // see~[thread.req.native]
    native_handle_type native_handle();                         // see~[thread.req.native]
  };
}
```

The class `shared_mutex` provides a non-recursive mutex with shared
ownership semantics.

The class `shared_mutex` meets all of the shared mutex requirements
[[thread.sharedmutex.requirements]]. It is a standard-layout class
[[class.prop]].

The behavior of a program is undefined if:

- it destroys a `shared_mutex` object owned by any thread,
- a thread attempts to recursively gain any ownership of a
  `shared_mutex`, or
- a thread terminates while possessing any ownership of a
  `shared_mutex`.

`shared_mutex` may be a synonym for `shared_timed_mutex`.

#### Shared timed mutex types <a id="thread.sharedtimedmutex.requirements">[[thread.sharedtimedmutex.requirements]]</a>

The standard library type `shared_timed_mutex` is a *shared timed mutex
type*. Shared timed mutex types meet the requirements of timed mutex
types [[thread.timedmutex.requirements]], shared mutex types
[[thread.sharedmutex.requirements]], and additionally meet the
requirements set out below. In this description, `m` denotes an object
of a shared timed mutex type, `rel_type` denotes an object of an
instantiation of `duration` [[time.duration]], and `abs_time` denotes an
object of an instantiation of `time_point` [[time.point]].

The expression `m.try_lock_shared_for(rel_time)` is well-formed and has
the following semantics:

*Preconditions:* The calling thread has no ownership of the mutex.

*Effects:* Attempts to obtain shared lock ownership for the calling
thread within the relative timeout [[thread.req.timing]] specified by
`rel_time`. If the time specified by `rel_time` is less than or equal to
`rel_time.zero()`, the function attempts to obtain ownership without
blocking (as if by calling `try_lock_shared()`). The function returns
within the timeout specified by `rel_time` only if it has obtained
shared ownership of the mutex object.

[*Note 1*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

If an exception is thrown then a shared lock has not been acquired for
the current thread.

*Return type:* `bool`.

*Returns:* `true` if the shared lock was acquired, `false` otherwise.

*Synchronization:* If `try_lock_shared_for()` returns `true`, prior
`unlock()` operations on the same object synchronize
with [[intro.multithread]] this operation.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

The expression `m.try_lock_shared_until(abs_time)` is well-formed and
has the following semantics:

*Preconditions:* The calling thread has no ownership of the mutex.

*Effects:* The function attempts to obtain shared ownership of the
mutex. If `abs_time` has already passed, the function attempts to obtain
shared ownership without blocking (as if by calling
`try_lock_shared()`). The function returns before the absolute
timeout [[thread.req.timing]] specified by `abs_time` only if it has
obtained shared ownership of the mutex object.

[*Note 2*: As with `try_lock()`, there is no guarantee that ownership
will be obtained if the lock is available, but implementations are
expected to make a strong effort to do so. — *end note*]

If an exception is thrown then a shared lock has not been acquired for
the current thread.

*Return type:* `bool`.

*Returns:* `true` if the shared lock was acquired, `false` otherwise.

*Synchronization:* If `try_lock_shared_until()` returns `true`, prior
`unlock()` operations on the same object synchronize
with [[intro.multithread]] this operation.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

##### Class `shared_timed_mutex` <a id="thread.sharedtimedmutex.class">[[thread.sharedtimedmutex.class]]</a>

``` cpp
namespace std {
  class shared_timed_mutex {
  public:
    shared_timed_mutex();
    ~shared_timed_mutex();

    shared_timed_mutex(const shared_timed_mutex&) = delete;
    shared_timed_mutex& operator=(const shared_timed_mutex&) = delete;

    // exclusive ownership
    void lock();                // blocking
    bool try_lock();
    template<class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
      bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock();

    // shared ownership
    void lock_shared();         // blocking
    bool try_lock_shared();
    template<class Rep, class Period>
      bool try_lock_shared_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
      bool try_lock_shared_until(const chrono::time_point<Clock, Duration>& abs_time);
    void unlock_shared();
  };
}
```

The class `shared_timed_mutex` provides a non-recursive mutex with
shared ownership semantics.

The class `shared_timed_mutex` meets all of the shared timed mutex
requirements [[thread.sharedtimedmutex.requirements]]. It is a
standard-layout class [[class.prop]].

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
  template<class Mutex>
  class lock_guard {
  public:
    using mutex_type = Mutex;

    explicit lock_guard(mutex_type& m);
    lock_guard(mutex_type& m, adopt_lock_t);
    ~lock_guard();

    lock_guard(const lock_guard&) = delete;
    lock_guard& operator=(const lock_guard&) = delete;

  private:
    mutex_type& pm;             // exposition only
  };
}
```

An object of type `lock_guard` controls the ownership of a lockable
object within a scope. A `lock_guard` object maintains ownership of a
lockable object throughout the `lock_guard` object’s lifetime
[[basic.life]]. The behavior of a program is undefined if the lockable
object referenced by `pm` does not exist for the entire lifetime of the
`lock_guard` object. The supplied `Mutex` type shall meet the
*Cpp17BasicLockable* requirements [[thread.req.lockable.basic]].

``` cpp
explicit lock_guard(mutex_type& m);
```

*Preconditions:* If `mutex_type` is not a recursive mutex, the calling
thread does not own the mutex `m`.

*Effects:* Initializes `pm` with `m`. Calls `m.lock()`.

``` cpp
lock_guard(mutex_type& m, adopt_lock_t);
```

*Preconditions:* The calling thread owns the mutex `m`.

*Effects:* Initializes `pm` with `m`.

*Throws:* Nothing.

``` cpp
~lock_guard();
```

*Effects:* As if by `pm.unlock()`.

#### Class template `scoped_lock` <a id="thread.lock.scoped">[[thread.lock.scoped]]</a>

``` cpp
namespace std {
  template<class... MutexTypes>
  class scoped_lock {
  public:
    using mutex_type = Mutex;   // If MutexTypes... consists of the single type Mutex

    explicit scoped_lock(MutexTypes&... m);
    explicit scoped_lock(adopt_lock_t, MutexTypes&... m);
    ~scoped_lock();

    scoped_lock(const scoped_lock&) = delete;
    scoped_lock& operator=(const scoped_lock&) = delete;

  private:
    tuple<MutexTypes&...> pm;   // exposition only
  };
}
```

An object of type `scoped_lock` controls the ownership of lockable
objects within a scope. A `scoped_lock` object maintains ownership of
lockable objects throughout the `scoped_lock` object’s lifetime
[[basic.life]]. The behavior of a program is undefined if the lockable
objects referenced by `pm` do not exist for the entire lifetime of the
`scoped_lock` object. When `sizeof...(MutexTypes)` is `1`, the supplied
`Mutex` type shall meet the *Cpp17BasicLockable* requirements
[[thread.req.lockable.basic]]. Otherwise, each of the mutex types shall
meet the *Cpp17Lockable* requirements [[thread.req.lockable.req]].

``` cpp
explicit scoped_lock(MutexTypes&... m);
```

*Preconditions:* If a `MutexTypes` type is not a recursive mutex, the
calling thread does not own the corresponding mutex element of `m`.

*Effects:* Initializes `pm` with `tie(m...)`. Then if
`sizeof...(MutexTypes)` is `0`, no effects. Otherwise if
`sizeof...(MutexTypes)` is `1`, then `m.lock()`. Otherwise,
`lock(m...)`.

``` cpp
explicit scoped_lock(adopt_lock_t, MutexTypes&... m);
```

*Preconditions:* The calling thread owns all the mutexes in `m`.

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
  template<class Mutex>
  class unique_lock {
  public:
    using mutex_type = Mutex;

    // [thread.lock.unique.cons], construct/copy/destroy
    unique_lock() noexcept;
    explicit unique_lock(mutex_type& m);
    unique_lock(mutex_type& m, defer_lock_t) noexcept;
    unique_lock(mutex_type& m, try_to_lock_t);
    unique_lock(mutex_type& m, adopt_lock_t);
    template<class Clock, class Duration>
      unique_lock(mutex_type& m, const chrono::time_point<Clock, Duration>& abs_time);
    template<class Rep, class Period>
      unique_lock(mutex_type& m, const chrono::duration<Rep, Period>& rel_time);
    ~unique_lock();

    unique_lock(const unique_lock&) = delete;
    unique_lock& operator=(const unique_lock&) = delete;

    unique_lock(unique_lock&& u) noexcept;
    unique_lock& operator=(unique_lock&& u);

    // [thread.lock.unique.locking], locking
    void lock();
    bool try_lock();

    template<class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
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
    mutex_type* pm;             // exposition only
    bool owns;                  // exposition only
  };

  template<class Mutex>
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
remaining lifetime [[basic.life]] of the `unique_lock` object. The
supplied `Mutex` type shall meet the *Cpp17BasicLockable* requirements
[[thread.req.lockable.basic]].

[*Note 1*: `unique_lock<Mutex>` meets the *Cpp17BasicLockable*
requirements. If `Mutex` meets the *Cpp17Lockable* requirements
[[thread.req.lockable.req]], `unique_lock<Mutex>` also meets the
*Cpp17Lockable* requirements; if `Mutex` meets the *Cpp17TimedLockable*
requirements [[thread.req.lockable.timed]], `unique_lock<Mutex>` also
meets the *Cpp17TimedLockable* requirements. — *end note*]

##### Constructors, destructor, and assignment <a id="thread.lock.unique.cons">[[thread.lock.unique.cons]]</a>

``` cpp
unique_lock() noexcept;
```

*Ensures:* `pm == 0` and `owns == false`.

``` cpp
explicit unique_lock(mutex_type& m);
```

*Preconditions:* If `mutex_type` is not a recursive mutex the calling
thread does not own the mutex.

*Effects:* Calls `m.lock()`.

*Ensures:* `pm == addressof(m)` and `owns == true`.

``` cpp
unique_lock(mutex_type& m, defer_lock_t) noexcept;
```

*Ensures:* `pm == addressof(m)` and `owns == false`.

``` cpp
unique_lock(mutex_type& m, try_to_lock_t);
```

*Preconditions:* The supplied `Mutex` type meets the *Cpp17Lockable*
requirements [[thread.req.lockable.req]]. If `mutex_type` is not a
recursive mutex the calling thread does not own the mutex.

*Effects:* Calls `m.try_lock()`.

*Ensures:* `pm == addressof(m)` and `owns == res`, where `res` is the
value returned by the call to `m.try_lock()`.

``` cpp
unique_lock(mutex_type& m, adopt_lock_t);
```

*Preconditions:* The calling thread owns the mutex.

*Ensures:* `pm == addressof(m)` and `owns == true`.

*Throws:* Nothing.

``` cpp
template<class Clock, class Duration>
  unique_lock(mutex_type& m, const chrono::time_point<Clock, Duration>& abs_time);
```

*Preconditions:* If `mutex_type` is not a recursive mutex the calling
thread does not own the mutex. The supplied `Mutex` type meets the
*Cpp17TimedLockable* requirements [[thread.req.lockable.timed]].

*Effects:* Calls `m.try_lock_until(abs_time)`.

*Ensures:* `pm == addressof(m)` and `owns == res`, where `res` is the
value returned by the call to `m.try_lock_until(abs_time)`.

``` cpp
template<class Rep, class Period>
  unique_lock(mutex_type& m, const chrono::duration<Rep, Period>& rel_time);
```

*Preconditions:* If `mutex_type` is not a recursive mutex the calling
thread does not own the mutex. The supplied `Mutex` type meets the
*Cpp17TimedLockable* requirements [[thread.req.lockable.timed]].

*Effects:* Calls `m.try_lock_for(rel_time)`.

*Ensures:* `pm == addressof(m)` and `owns == res`, where `res` is the
value returned by the call to `m.try_lock_for(rel_time)`.

``` cpp
unique_lock(unique_lock&& u) noexcept;
```

*Ensures:* `pm == u_p.pm` and `owns == u_p.owns` (where `u_p` is the
state of `u` just prior to this construction), `u.pm == 0` and
`u.owns == false`.

``` cpp
unique_lock& operator=(unique_lock&& u);
```

*Effects:* If `owns` calls `pm->unlock()`.

*Ensures:* `pm == u_p.pm` and `owns == u_p.owns` (where `u_p` is the
state of `u` just prior to this construction), `u.pm == 0` and
`u.owns == false`.

[*Note 1*: With a recursive mutex it is possible for both `*this` and
`u` to own the same mutex before the assignment. In this case, `*this`
will own the mutex after the assignment and `u` will not. — *end note*]

*Throws:* Nothing.

``` cpp
~unique_lock();
```

*Effects:* If `owns` calls `pm->unlock()`.

##### Locking <a id="thread.lock.unique.locking">[[thread.lock.unique.locking]]</a>

``` cpp
void lock();
```

*Effects:* As if by `pm->lock()`.

*Ensures:* `owns == true`.

*Throws:* Any exception thrown by `pm->lock()`. `system_error` when an
exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
bool try_lock();
```

*Preconditions:* The supplied `Mutex` meets the *Cpp17Lockable*
requirements [[thread.req.lockable.req]].

*Effects:* As if by `pm->try_lock()`.

*Returns:* The value returned by the call to `try_lock()`.

*Ensures:* `owns == res`, where `res` is the value returned by the call
to `try_lock()`.

*Throws:* Any exception thrown by `pm->try_lock()`. `system_error` when
an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template<class Clock, class Duration>
  bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Preconditions:* The supplied `Mutex` type meets the
*Cpp17TimedLockable* requirements [[thread.req.lockable.timed]].

*Effects:* As if by `pm->try_lock_until(abs_time)`.

*Returns:* The value returned by the call to `try_lock_until(abs_time)`.

*Ensures:* `owns == res`, where `res` is the value returned by the call
to `try_lock_until(abs_time)`.

*Throws:* Any exception thrown by `pm->try_lock_until()`. `system_error`
when an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template<class Rep, class Period>
  bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
```

*Preconditions:* The supplied `Mutex` type meets the
*Cpp17TimedLockable* requirements [[thread.req.lockable.timed]].

*Effects:* As if by `pm->try_lock_for(rel_time)`.

*Returns:* The value returned by the call to `try_lock_for(rel_time)`.

*Ensures:* `owns == res`, where `res` is the value returned by the call
to `try_lock_for(rel_time)`.

*Throws:* Any exception thrown by `pm->try_lock_for()`. `system_error`
when an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
void unlock();
```

*Effects:* As if by `pm->unlock()`.

*Ensures:* `owns == false`.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if on entry `owns` is `false`.

##### Modifiers <a id="thread.lock.unique.mod">[[thread.lock.unique.mod]]</a>

``` cpp
void swap(unique_lock& u) noexcept;
```

*Effects:* Swaps the data members of `*this` and `u`.

``` cpp
mutex_type* release() noexcept;
```

*Returns:* The previous value of `pm`.

*Ensures:* `pm == 0` and `owns == false`.

``` cpp
template<class Mutex>
  void swap(unique_lock<Mutex>& x, unique_lock<Mutex>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

##### Observers <a id="thread.lock.unique.obs">[[thread.lock.unique.obs]]</a>

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
  template<class Mutex>
  class shared_lock {
  public:
    using mutex_type = Mutex;

    // [thread.lock.shared.cons], construct/copy/destroy
    shared_lock() noexcept;
    explicit shared_lock(mutex_type& m);        // blocking
    shared_lock(mutex_type& m, defer_lock_t) noexcept;
    shared_lock(mutex_type& m, try_to_lock_t);
    shared_lock(mutex_type& m, adopt_lock_t);
    template<class Clock, class Duration>
      shared_lock(mutex_type& m, const chrono::time_point<Clock, Duration>& abs_time);
    template<class Rep, class Period>
      shared_lock(mutex_type& m, const chrono::duration<Rep, Period>& rel_time);
    ~shared_lock();

    shared_lock(const shared_lock&) = delete;
    shared_lock& operator=(const shared_lock&) = delete;

    shared_lock(shared_lock&& u) noexcept;
    shared_lock& operator=(shared_lock&& u) noexcept;

    // [thread.lock.shared.locking], locking
    void lock();                                // blocking
    bool try_lock();
    template<class Rep, class Period>
      bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
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
    mutex_type* pm;                             // exposition only
    bool owns;                                  // exposition only
  };

  template<class Mutex>
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
remaining lifetime [[basic.life]] of the `shared_lock` object. The
supplied `Mutex` type shall meet the shared mutex requirements
[[thread.sharedtimedmutex.requirements]].

[*Note 1*: `shared_lock<Mutex>` meets the *Cpp17TimedLockable*
requirements [[thread.req.lockable.timed]]. — *end note*]

##### Constructors, destructor, and assignment <a id="thread.lock.shared.cons">[[thread.lock.shared.cons]]</a>

``` cpp
shared_lock() noexcept;
```

*Ensures:* `pm == nullptr` and `owns == false`.

``` cpp
explicit shared_lock(mutex_type& m);
```

*Preconditions:* The calling thread does not own the mutex for any
ownership mode.

*Effects:* Calls `m.lock_shared()`.

*Ensures:* `pm == addressof(m)` and `owns == true`.

``` cpp
shared_lock(mutex_type& m, defer_lock_t) noexcept;
```

*Ensures:* `pm == addressof(m)` and `owns == false`.

``` cpp
shared_lock(mutex_type& m, try_to_lock_t);
```

*Preconditions:* The calling thread does not own the mutex for any
ownership mode.

*Effects:* Calls `m.try_lock_shared()`.

*Ensures:* `pm == addressof(m)` and `owns == res` where `res` is the
value returned by the call to `m.try_lock_shared()`.

``` cpp
shared_lock(mutex_type& m, adopt_lock_t);
```

*Preconditions:* The calling thread has shared ownership of the mutex.

*Ensures:* `pm == addressof(m)` and `owns == true`.

``` cpp
template<class Clock, class Duration>
  shared_lock(mutex_type& m,
              const chrono::time_point<Clock, Duration>& abs_time);
```

*Preconditions:* The calling thread does not own the mutex for any
ownership mode.

*Effects:* Calls `m.try_lock_shared_until(abs_time)`.

*Ensures:* `pm == addressof(m)` and `owns == res` where `res` is the
value returned by the call to `m.try_lock_shared_until(abs_time)`.

``` cpp
template<class Rep, class Period>
  shared_lock(mutex_type& m,
              const chrono::duration<Rep, Period>& rel_time);
```

*Preconditions:* The calling thread does not own the mutex for any
ownership mode.

*Effects:* Calls `m.try_lock_shared_for(rel_time)`.

*Ensures:* `pm == addressof(m)` and `owns == res` where `res` is the
value returned by the call to `m.try_lock_shared_for(rel_time)`.

``` cpp
~shared_lock();
```

*Effects:* If `owns` calls `pm->unlock_shared()`.

``` cpp
shared_lock(shared_lock&& sl) noexcept;
```

*Ensures:* `pm == sl_p.pm` and `owns == sl_p.owns` (where `sl_p` is the
state of `sl` just prior to this construction), `sl.pm == nullptr` and
`sl.owns == false`.

``` cpp
shared_lock& operator=(shared_lock&& sl) noexcept;
```

*Effects:* If `owns` calls `pm->unlock_shared()`.

*Ensures:* `pm == sl_p.pm` and `owns == sl_p.owns` (where `sl_p` is the
state of `sl` just prior to this assignment), `sl.pm == nullptr` and
`sl.owns == false`.

##### Locking <a id="thread.lock.shared.locking">[[thread.lock.shared.locking]]</a>

``` cpp
void lock();
```

*Effects:* As if by `pm->lock_shared()`.

*Ensures:* `owns == true`.

*Throws:* Any exception thrown by `pm->lock_shared()`. `system_error`
when an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
bool try_lock();
```

*Effects:* As if by `pm->try_lock_shared()`.

*Returns:* The value returned by the call to `pm->try_lock_shared()`.

*Ensures:* `owns == res`, where `res` is the value returned by the call
to `pm->try_lock_shared()`.

*Throws:* Any exception thrown by `pm->try_lock_shared()`.
`system_error` when an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template<class Clock, class Duration>
  bool try_lock_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:* As if by `pm->try_lock_shared_until(abs_time)`.

*Returns:* The value returned by the call to
`pm->try_lock_shared_until(abs_time)`.

*Ensures:* `owns == res`, where `res` is the value returned by the call
to `pm->try_lock_shared_until(abs_time)`.

*Throws:* Any exception thrown by `pm->try_lock_shared_until(abs_time)`.
`system_error` when an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
template<class Rep, class Period>
  bool try_lock_for(const chrono::duration<Rep, Period>& rel_time);
```

*Effects:* As if by `pm->try_lock_shared_for(rel_time)`.

*Returns:* The value returned by the call to
`pm->try_lock_shared_for(rel_time)`.

*Ensures:* `owns == res`, where `res` is the value returned by the call
to `pm->try_lock_shared_for(rel_time)`.

*Throws:* Any exception thrown by `pm->try_lock_shared_for(rel_time)`.
`system_error` when an exception is required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if `pm` is `nullptr`.
- `resource_deadlock_would_occur` — if on entry `owns` is `true`.

``` cpp
void unlock();
```

*Effects:* As if by `pm->unlock_shared()`.

*Ensures:* `owns == false`.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `operation_not_permitted` — if on entry `owns` is `false`.

##### Modifiers <a id="thread.lock.shared.mod">[[thread.lock.shared.mod]]</a>

``` cpp
void swap(shared_lock& sl) noexcept;
```

*Effects:* Swaps the data members of `*this` and `sl`.

``` cpp
mutex_type* release() noexcept;
```

*Returns:* The previous value of `pm`.

*Ensures:* `pm == nullptr` and `owns == false`.

``` cpp
template<class Mutex>
  void swap(shared_lock<Mutex>& x, shared_lock<Mutex>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

##### Observers <a id="thread.lock.shared.obs">[[thread.lock.shared.obs]]</a>

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
template<class L1, class L2, class... L3> int try_lock(L1&, L2&, L3&...);
```

*Preconditions:* Each template parameter type meets the *Cpp17Lockable*
requirements.

[*Note 1*: The `unique_lock` class template meets these requirements
when suitably instantiated. — *end note*]

*Effects:* Calls `try_lock()` for each argument in order beginning with
the first until all arguments have been processed or a call to
`try_lock()` fails, either by returning `false` or by throwing an
exception. If a call to `try_lock()` fails, `unlock()` is called for all
prior arguments with no further calls to `try_lock()`.

*Returns:* `-1` if all calls to `try_lock()` returned `true`, otherwise
a zero-based index value that indicates the argument for which
`try_lock()` returned `false`.

``` cpp
template<class L1, class L2, class... L3> void lock(L1&, L2&, L3&...);
```

*Preconditions:* Each template parameter type meets the *Cpp17Lockable*
requirements.

[*Note 2*: The `unique_lock` class template meets these requirements
when suitably instantiated. — *end note*]

*Effects:* All arguments are locked via a sequence of calls to `lock()`,
`try_lock()`, or `unlock()` on each argument. The sequence of calls does
not result in deadlock, but is otherwise unspecified.

[*Note 3*: A deadlock avoidance algorithm such as try-and-back-off must
be used, but the specific algorithm is not specified to avoid
over-constraining implementations. — *end note*]

If a call to `lock()` or `try_lock()` throws an exception, `unlock()` is
called for any argument that had been locked by a call to `lock()` or
`try_lock()`.

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

*Synchronization:* The construction of a `once_flag` object is not
synchronized.

*Ensures:* The object’s internal state is set to indicate to an
invocation of `call_once` with the object as its initial argument that
no function has been called.

#### Function `call_once` <a id="thread.once.callonce">[[thread.once.callonce]]</a>

``` cpp
template<class Callable, class... Args>
  void call_once(once_flag& flag, Callable&& func, Args&&... args);
```

*Mandates:* `is_invocable_v<Callable, Args...>` is `true`.

*Effects:* An execution of `call_once` that does not call its `func` is
a *passive* execution. An execution of `call_once` that calls its `func`
is an *active* execution. An active execution calls *INVOKE*(
std::forward\<Callable\>(func), std::forward\<Args\>(args)...). If such
a call to `func` throws an exception the execution is *exceptional*,
otherwise it is *returning*. An exceptional execution propagates the
exception to the caller of `call_once`. Among all executions of
`call_once` for any given `once_flag`: at most one is a returning
execution; if there is a returning execution, it is the last active
execution; and there are passive executions only if there is a returning
execution.

[*Note 1*: Passive executions allow other threads to reliably observe
the results produced by the earlier returning execution. — *end note*]

*Synchronization:* For any given `once_flag`: all active executions
occur in a total order; completion of an active execution synchronizes
with [[intro.multithread]] the start of the next one in this total
order; and the returning execution synchronizes with the return from all
passive executions.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]], or any exception thrown by `func`.

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
`unique_lock<mutex>`, allowing the implementation to be more efficient.
Class `condition_variable_any` provides a general condition variable
that can wait on objects of user-supplied lock types.

Condition variables permit concurrent invocation of the `wait`,
`wait_for`, `wait_until`, `notify_one` and `notify_all` member
functions.

The executions of `notify_one` and `notify_all` are atomic. The
executions of `wait`, `wait_for`, and `wait_until` are performed in
three atomic parts:

1.  the release of the mutex and entry into the waiting state;
2.  the unblocking of the wait; and
3.  the reacquisition of the lock.

The implementation behaves as if all executions of `notify_one`,
`notify_all`, and each part of the `wait`, `wait_for`, and `wait_until`
executions are executed in a single unspecified total order consistent
with the "happens before" order.

Condition variable construction and destruction need not be
synchronized.

### Header `<condition_variable>` synopsis <a id="condition.variable.syn">[[condition.variable.syn]]</a>

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

*Preconditions:* `lk` is locked by the calling thread and either

- no other thread is waiting on `cond`, or
- `lk.mutex()` returns the same value for each of the lock arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Transfers ownership of the lock associated with `lk` into
internal storage and schedules `cond` to be notified when the current
thread exits, after all objects of thread storage duration associated
with the current thread have been destroyed. This notification is
equivalent to:

``` cpp
lk.unlock();
cond.notify_all();
```

*Synchronization:* The implied `lk.unlock()` call is sequenced after the
destruction of all objects with thread storage duration associated with
the current thread.

[*Note 1*: The supplied lock will be held until the thread exits, and
care should be taken to ensure that this does not cause deadlock due to
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
    template<class Predicate>
      void wait(unique_lock<mutex>& lock, Predicate pred);
    template<class Clock, class Duration>
      cv_status wait_until(unique_lock<mutex>& lock,
                           const chrono::time_point<Clock, Duration>& abs_time);
    template<class Clock, class Duration, class Predicate>
      bool wait_until(unique_lock<mutex>& lock,
                      const chrono::time_point<Clock, Duration>& abs_time,
                      Predicate pred);
    template<class Rep, class Period>
      cv_status wait_for(unique_lock<mutex>& lock,
                         const chrono::duration<Rep, Period>& rel_time);
    template<class Rep, class Period, class Predicate>
      bool wait_for(unique_lock<mutex>& lock,
                    const chrono::duration<Rep, Period>& rel_time,
                    Predicate pred);

    using native_handle_type = implementation-defined;          // see~[thread.req.native]
    native_handle_type native_handle();                         // see~[thread.req.native]
  };
}
```

The class `condition_variable` is a standard-layout class
[[class.prop]].

``` cpp
condition_variable();
```

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `resource_unavailable_try_again` — if some non-memory resource
  limitation prevents initialization.

``` cpp
~condition_variable();
```

*Preconditions:* There is no thread blocked on `*this`.

[*Note 1*: That is, all threads have been notified; they could
subsequently block on the lock specified in the wait. This relaxes the
usual rules, which would have required all wait calls to happen before
destruction. Only the notification to unblock the wait needs to happen
before destruction. The user should take care to ensure that no threads
wait on `*this` once the destructor has been started, especially when
the waiting threads are calling the wait functions in a loop or using
the overloads of `wait`, `wait_for`, or `wait_until` that take a
predicate. — *end note*]

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

*Preconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread, and either

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
`terminate()` is called [[except.terminate]].

[*Note 2*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread.

*Throws:* Nothing.

``` cpp
template<class Predicate>
  void wait(unique_lock<mutex>& lock, Predicate pred);
```

*Preconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread, and either

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
`terminate()` is called [[except.terminate]].

[*Note 3*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread.

*Throws:* Any exception thrown by `pred`.

``` cpp
template<class Clock, class Duration>
  cv_status wait_until(unique_lock<mutex>& lock,
                       const chrono::time_point<Clock, Duration>& abs_time);
```

*Preconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread, and either

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
  timeout [[thread.req.timing]] specified by `abs_time`, or spuriously.
- If the function exits via an exception, `lock.lock()` is called prior
  to exiting the function.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` is called [[except.terminate]].

[*Note 4*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread.

*Returns:* `cv_status::timeout` if the absolute
timeout [[thread.req.timing]] specified by `abs_time` expired, otherwise
`cv_status::no_timeout`.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Rep, class Period>
  cv_status wait_for(unique_lock<mutex>& lock,
                     const chrono::duration<Rep, Period>& rel_time);
```

*Preconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread, and either

- no other thread is waiting on this `condition_variable` object or
- `lock.mutex()` returns the same value for each of the `lock` arguments
  supplied by all concurrently waiting (via `wait`, `wait_for`, or
  `wait_until`) threads.

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time);
```

*Returns:* `cv_status::timeout` if the relative
timeout [[thread.req.timing]] specified by `rel_time` expired, otherwise
`cv_status::no_timeout`.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` is called [[except.terminate]].

[*Note 5*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Clock, class Duration, class Predicate>
  bool wait_until(unique_lock<mutex>& lock,
                  const chrono::time_point<Clock, Duration>& abs_time,
                  Predicate pred);
```

*Preconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread, and either

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
`terminate()` is called [[except.terminate]].

[*Note 6*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread.

[*Note 7*: The returned value indicates whether the predicate evaluated
to `true` regardless of whether the timeout was
triggered. — *end note*]

*Throws:* Timeout-related exceptions [[thread.req.timing]] or any
exception thrown by `pred`.

``` cpp
template<class Rep, class Period, class Predicate>
  bool wait_for(unique_lock<mutex>& lock,
                const chrono::duration<Rep, Period>& rel_time,
                Predicate pred);
```

*Preconditions:* `lock.owns_lock()` is `true` and `lock.mutex()` is
locked by the calling thread, and either

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
`terminate()` is called [[except.terminate]].

[*Note 9*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock.owns_lock()` is `true` and `lock.mutex()` is locked by
the calling thread.

[*Note 10*: The returned value indicates whether the predicate
evaluates to `true` regardless of whether the timeout was
triggered. — *end note*]

*Throws:* Timeout-related exceptions [[thread.req.timing]] or any
exception thrown by `pred`.

### Class `condition_variable_any` <a id="thread.condition.condvarany">[[thread.condition.condvarany]]</a>

A `Lock` type shall meet the *Cpp17BasicLockable* requirements
[[thread.req.lockable.basic]].

[*Note 1*: All of the standard mutex types meet this requirement. If a
`Lock` type other than one of the standard mutex types or a
`unique_lock` wrapper for a standard mutex type is used with
`condition_variable_any`, the user should ensure that any necessary
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

    // [thread.condvarany.wait], noninterruptible waits
    template<class Lock>
      void wait(Lock& lock);
    template<class Lock, class Predicate>
      void wait(Lock& lock, Predicate pred);

    template<class Lock, class Clock, class Duration>
      cv_status wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time);
    template<class Lock, class Clock, class Duration, class Predicate>
      bool wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time,
                      Predicate pred);
    template<class Lock, class Rep, class Period>
      cv_status wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time);
    template<class Lock, class Rep, class Period, class Predicate>
      bool wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time, Predicate pred);

    // [thread.condvarany.intwait], interruptible waits
    template<class Lock, class Predicate>
      bool wait(Lock& lock, stop_token stoken, Predicate pred);
    template<class Lock, class Clock, class Duration, class Predicate>
      bool wait_until(Lock& lock, stop_token stoken,
                      const chrono::time_point<Clock, Duration>& abs_time, Predicate pred);
    template<class Lock, class Rep, class Period, class Predicate>
      bool wait_for(Lock& lock, stop_token stoken,
                    const chrono::duration<Rep, Period>& rel_time, Predicate pred);
  };
}
```

``` cpp
condition_variable_any();
```

*Throws:* `bad_alloc` or `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:*

- `resource_unavailable_try_again` — if some non-memory resource
  limitation prevents initialization.
- `operation_not_permitted` — if the thread does not have the privilege
  to perform the operation.

``` cpp
~condition_variable_any();
```

*Preconditions:* There is no thread blocked on `*this`.

[*Note 1*: That is, all threads have been notified; they could
subsequently block on the lock specified in the wait. This relaxes the
usual rules, which would have required all wait calls to happen before
destruction. Only the notification to unblock the wait needs to happen
before destruction. The user should take care to ensure that no threads
wait on `*this` once the destructor has been started, especially when
the waiting threads are calling the wait functions in a loop or using
the overloads of `wait`, `wait_for`, or `wait_until` that take a
predicate. — *end note*]

``` cpp
void notify_one() noexcept;
```

*Effects:* If any threads are blocked waiting for `*this`, unblocks one
of those threads.

``` cpp
void notify_all() noexcept;
```

*Effects:* Unblocks all threads that are blocked waiting for `*this`.

#### Noninterruptible waits <a id="thread.condvarany.wait">[[thread.condvarany.wait]]</a>

``` cpp
template<class Lock>
  void wait(Lock& lock);
```

*Effects:*

- Atomically calls `lock.unlock()` and blocks on `*this`.
- When unblocked, calls `lock.lock()` (possibly blocking on the lock)
  and returns.
- The function will unblock when signaled by a call to `notify_one()`, a
  call to `notify_all()`, or spuriously.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` is called [[except.terminate]].

[*Note 1*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock` is locked by the calling thread.

*Throws:* Nothing.

``` cpp
template<class Lock, class Predicate>
  void wait(Lock& lock, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
while (!pred())
  wait(lock);
```

``` cpp
template<class Lock, class Clock, class Duration>
  cv_status wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:*

- Atomically calls `lock.unlock()` and blocks on `*this`.
- When unblocked, calls `lock.lock()` (possibly blocking on the lock)
  and returns.
- The function will unblock when signaled by a call to `notify_one()`, a
  call to `notify_all()`, expiration of the absolute
  timeout [[thread.req.timing]] specified by `abs_time`, or spuriously.
- If the function exits via an exception, `lock.lock()` is called prior
  to exiting the function.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` is called [[except.terminate]].

[*Note 2*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock` is locked by the calling thread.

*Returns:* `cv_status::timeout` if the absolute
timeout [[thread.req.timing]] specified by `abs_time` expired, otherwise
`cv_status::no_timeout`.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Lock, class Rep, class Period>
  cv_status wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time);
```

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time);
```

*Returns:* `cv_status::timeout` if the relative
timeout [[thread.req.timing]] specified by `rel_time` expired, otherwise
`cv_status::no_timeout`.

*Remarks:* If the function fails to meet the postcondition,
`terminate()` is called [[except.terminate]].

[*Note 3*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Ensures:* `lock` is locked by the calling thread.

*Throws:* Timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Lock, class Clock, class Duration, class Predicate>
  bool wait_until(Lock& lock, const chrono::time_point<Clock, Duration>& abs_time, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
while (!pred())
  if (wait_until(lock, abs_time) == cv_status::timeout)
    return pred();
return true;
```

[*Note 4*: There is no blocking if `pred()` is initially `true`, or if
the timeout has already expired. — *end note*]

[*Note 5*: The returned value indicates whether the predicate evaluates
to `true` regardless of whether the timeout was
triggered. — *end note*]

``` cpp
template<class Lock, class Rep, class Period, class Predicate>
  bool wait_for(Lock& lock, const chrono::duration<Rep, Period>& rel_time, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, chrono::steady_clock::now() + rel_time, std::move(pred));
```

#### Interruptible waits <a id="thread.condvarany.intwait">[[thread.condvarany.intwait]]</a>

The following wait functions will be notified when there is a stop
request on the passed `stop_token`. In that case the functions return
immediately, returning `false` if the predicate evaluates to `false`.

``` cpp
template<class Lock, class Predicate>
  bool wait(Lock& lock, stop_token stoken, Predicate pred);
```

*Effects:* Registers for the duration of this call `*this` to get
notified on a stop request on `stoken` during this call and then
equivalent to:

``` cpp
while (!stoken.stop_requested()) {
  if (pred())
    return true;
  wait(lock);
}
return pred();
```

[*Note 1*: The returned value indicates whether the predicate evaluated
to `true` regardless of whether there was a stop request. — *end note*]

*Ensures:* `lock` is locked by the calling thread.

*Remarks:* If the function fails to meet the postcondition, `terminate`
is called [[except.terminate]].

[*Note 2*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Throws:* Any exception thrown by `pred`.

``` cpp
template<class Lock, class Clock, class Duration, class Predicate>
  bool wait_until(Lock& lock, stop_token stoken,
                  const chrono::time_point<Clock, Duration>& abs_time, Predicate pred);
```

*Effects:* Registers for the duration of this call `*this` to get
notified on a stop request on `stoken` during this call and then
equivalent to:

``` cpp
while (!stoken.stop_requested()) {
  if (pred())
    return true;
  if (cv.wait_until(lock, abs_time) == cv_status::timeout)
    return pred();
}
return pred();
```

[*Note 3*: There is no blocking if `pred()` is initially `true`,
`stoken.stop_requested()` was already `true` or the timeout has already
expired. — *end note*]

[*Note 4*: The returned value indicates whether the predicate evaluated
to `true` regardless of whether the timeout was triggered or a stop
request was made. — *end note*]

*Ensures:* `lock` is locked by the calling thread.

*Remarks:* If the function fails to meet the postcondition, `terminate`
is called [[except.terminate]].

[*Note 5*: This can happen if the re-locking of the mutex throws an
exception. — *end note*]

*Throws:* Timeout-related exceptions [[thread.req.timing]], or any
exception thrown by `pred`.

``` cpp
template<class Lock, class Rep, class Period, class Predicate>
  bool wait_for(Lock& lock, stop_token stoken,
                const chrono::duration<Rep, Period>& rel_time, Predicate pred);
```

*Effects:* Equivalent to:

``` cpp
return wait_until(lock, std::move(stoken), chrono::steady_clock::now() + rel_time,
                  std::move(pred));
```

## Semaphore <a id="thread.sema">[[thread.sema]]</a>

Semaphores are lightweight synchronization primitives used to constrain
concurrent access to a shared resource. They are widely used to
implement other synchronization primitives and, whenever both are
applicable, can be more efficient than condition variables.

A counting semaphore is a semaphore object that models a non-negative
resource count. A binary semaphore is a semaphore object that has only
two states. A binary semaphore should be more efficient than the default
implementation of a counting semaphore with a unit resource count.

### Header `<semaphore>` synopsis <a id="semaphore.syn">[[semaphore.syn]]</a>

``` cpp
namespace std {
  template<ptrdiff_t least_max_value = implementation-defined>
    class counting_semaphore;

  using binary_semaphore = counting_semaphore<1>;
}
```

### Class template `counting_semaphore` <a id="thread.sema.cnt">[[thread.sema.cnt]]</a>

``` cpp
namespace std {
  template<ptrdiff_t least_max_value = implementation-defined>
  class counting_semaphore {
  public:
    static constexpr ptrdiff_t max() noexcept;

    constexpr explicit counting_semaphore(ptrdiff_t desired);
    ~counting_semaphore();

    counting_semaphore(const counting_semaphore&) = delete;
    counting_semaphore& operator=(const counting_semaphore&) = delete;

    void release(ptrdiff_t update = 1);
    void acquire();
    bool try_acquire() noexcept;
    template<class Rep, class Period>
      bool try_acquire_for(const chrono::duration<Rep, Period>& rel_time);
    template<class Clock, class Duration>
      bool try_acquire_until(const chrono::time_point<Clock, Duration>& abs_time);

  private:
    ptrdiff_t counter;          // exposition only
  };
}
```

Class template `counting_semaphore` maintains an internal counter that
is initialized when the semaphore is created. The counter is decremented
when a thread acquires the semaphore, and is incremented when a thread
releases the semaphore. If a thread tries to acquire the semaphore when
the counter is zero, the thread will block until another thread
increments the counter by releasing the semaphore.

`least_max_value` shall be non-negative; otherwise the program is
ill-formed.

Concurrent invocations of the member functions of `counting_semaphore`,
other than its destructor, do not introduce data races.

``` cpp
static constexpr ptrdiff_t max() noexcept;
```

*Returns:* The maximum value of `counter`. This value is greater than or
equal to `least_max_value`.

``` cpp
constexpr explicit counting_semaphore(ptrdiff_t desired);
```

*Preconditions:* `desired >= 0` is `true`, and `desired <= max()` is
`true`.

*Effects:* Initializes `counter` with `desired`.

*Throws:* Nothing.

``` cpp
void release(ptrdiff_t update = 1);
```

*Preconditions:* `update >= 0` is `true`, and
`update <= max() - counter` is `true`.

*Effects:* Atomically execute `counter += update`. Then, unblocks any
threads that are waiting for `counter` to be greater than zero.

*Synchronization:* Strongly happens before invocations of `try_acquire`
that observe the result of the effects.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

``` cpp
bool try_acquire() noexcept;
```

*Effects:* Attempts to atomically decrement `counter` if it is positive,
without blocking. If `counter` is not decremented, there is no effect
and `try_acquire` immediately returns. An implementation may fail to
decrement `counter` even if it is positive.

[*Note 1*: This spurious failure is normally uncommon, but allows
interesting implementations based on a simple compare and
exchange [[atomics]]. — *end note*]

An implementation should ensure that `try_acquire` does not consistently
return `false` in the absence of contending semaphore operations.

*Returns:* `true` if `counter` was decremented, otherwise `false`.

``` cpp
void acquire();
```

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `try_acquire`. If the result is `true`, returns.
- Blocks on `*this` until `counter` is greater than zero.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

``` cpp
template<class Rep, class Period>
  bool try_acquire_for(const chrono::duration<Rep, Period>& rel_time);
template<class Clock, class Duration>
  bool try_acquire_until(const chrono::time_point<Clock, Duration>& abs_time);
```

*Effects:* Repeatedly performs the following steps, in order:

- Evaluates `try_acquire()`. If the result is `true`, returns `true`.
- Blocks on `*this` until `counter` is greater than zero or until the
  timeout expires. If it is unblocked by the timeout expiring, returns
  `false`.

The timeout expires [[thread.req.timing]] when the current time is after
`abs_time` (for `try_acquire_until`) or when at least `rel_time` has
passed from the start of the function (for `try_acquire_for`).

*Throws:* Timeout-related exceptions [[thread.req.timing]], or
`system_error` when a non-timeout-related exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

## Coordination types <a id="thread.coord">[[thread.coord]]</a>

This subclause describes various concepts related to thread
coordination, and defines the coordination types `latch` and `barrier`.
These types facilitate concurrent computation performed by a number of
threads.

### Latches <a id="thread.latch">[[thread.latch]]</a>

A latch is a thread coordination mechanism that allows any number of
threads to block until an expected number of threads arrive at the latch
(via the `count_down` function). The expected count is set when the
latch is created. An individual latch is a single-use object; once the
expected count has been reached, the latch cannot be reused.

#### Header `<latch>` synopsis <a id="latch.syn">[[latch.syn]]</a>

``` cpp
namespace std {
  class latch;
}
```

#### Class `latch` <a id="thread.latch.class">[[thread.latch.class]]</a>

``` cpp
namespace std {
  class latch {
  public:
    static constexpr ptrdiff_t max() noexcept;

    constexpr explicit latch(ptrdiff_t expected);
    ~latch();

    latch(const latch&) = delete;
    latch& operator=(const latch&) = delete;

    void count_down(ptrdiff_t update = 1);
    bool try_wait() const noexcept;
    void wait() const;
    void arrive_and_wait(ptrdiff_t update = 1);

  private:
    ptrdiff_t counter;  // exposition only
  };
}
```

A `latch` maintains an internal counter that is initialized when the
latch is created. Threads can block on the latch object, waiting for
counter to be decremented to zero.

Concurrent invocations of the member functions of `latch`, other than
its destructor, do not introduce data races.

``` cpp
static constexpr ptrdiff_t max() noexcept;
```

*Returns:* The maximum value of `counter` that the implementation
supports.

``` cpp
constexpr explicit latch(ptrdiff_t expected);
```

*Preconditions:* `expected >= 0` is `true` and `expected <= max()` is
`true`.

*Effects:* Initializes `counter` with `expected`.

*Throws:* Nothing.

``` cpp
void count_down(ptrdiff_t update = 1);
```

*Preconditions:* `update >= 0` is `true`, and `update <= counter` is
`true`.

*Effects:* Atomically decrements `counter` by `update`. If `counter` is
equal to zero, unblocks all threads blocked on `*this`.

*Synchronization:* Strongly happens before the returns from all calls
that are unblocked.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

``` cpp
bool try_wait() const noexcept;
```

*Returns:* With very low probability `false`. Otherwise `counter == 0`.

``` cpp
void wait() const;
```

*Effects:* If `counter` equals zero, returns immediately. Otherwise,
blocks on `*this` until a call to `count_down` that decrements `counter`
to zero.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

``` cpp
void arrive_and_wait(ptrdiff_t update = 1);
```

*Effects:* Equivalent to:

``` cpp
count_down(update);
wait();
```

### Barriers <a id="thread.barrier">[[thread.barrier]]</a>

A barrier is a thread coordination mechanism whose lifetime consists of
a sequence of barrier phases, where each phase allows at most an
expected number of threads to block until the expected number of threads
arrive at the barrier.

[*Note 1*: A barrier is useful for managing repeated tasks that are
handled by multiple threads. — *end note*]

#### Header `<barrier>` synopsis <a id="barrier.syn">[[barrier.syn]]</a>

``` cpp
namespace std {
  template<class CompletionFunction = see below>
    class barrier;
}
```

#### Class template `barrier` <a id="thread.barrier.class">[[thread.barrier.class]]</a>

``` cpp
namespace std {
  template<class CompletionFunction = see below>
  class barrier {
  public:
    using arrival_token = see below;

    static constexpr ptrdiff_t max() noexcept;

    constexpr explicit barrier(ptrdiff_t expected,
                               CompletionFunction f = CompletionFunction());
    ~barrier();

    barrier(const barrier&) = delete;
    barrier& operator=(const barrier&) = delete;

    [[nodiscard]] arrival_token arrive(ptrdiff_t update = 1);
    void wait(arrival_token&& arrival) const;

    void arrive_and_wait();
    void arrive_and_drop();

  private:
    CompletionFunction completion;      // exposition only
  };
}
```

Each *barrier phase* consists of the following steps:

- The expected count is decremented by each call to `arrive` or
  `arrive_and_drop`.
- When the expected count reaches zero, the phase completion step is
  run. For the specialization with the default value of the
  `CompletionFunction` template parameter, the completion step is run as
  part of the call to `arrive` or `arrive_and_drop` that caused the
  expected count to reach zero. For other specializations, the
  completion step is run on one of the threads that arrived at the
  barrier during the phase.
- When the completion step finishes, the expected count is reset to what
  was specified by the `expected` argument to the constructor, possibly
  adjusted by calls to `arrive_and_drop`, and the next phase starts.

Each phase defines a *phase synchronization point*. Threads that arrive
at the barrier during the phase can block on the phase synchronization
point by calling `wait`, and will remain blocked until the phase
completion step is run.

The *phase completion step* that is executed at the end of each phase
has the following effects:

- Invokes the completion function, equivalent to `completion()`.
- Unblocks all threads that are blocked on the phase synchronization
  point.

The end of the completion step strongly happens before the returns from
all calls that were unblocked by the completion step. For
specializations that do not have the default value of the
`CompletionFunction` template parameter, the behavior is undefined if
any of the barrier object’s member functions other than `wait` are
called while the completion step is in progress.

Concurrent invocations of the member functions of `barrier`, other than
its destructor, do not introduce data races. The member functions
`arrive` and `arrive_and_drop` execute atomically.

`CompletionFunction` shall meet the *Cpp17MoveConstructible* (
[[cpp17.moveconstructible]]) and *Cpp17Destructible* (
[[cpp17.destructible]]) requirements.
`is_nothrow_invocable_v<CompletionFunction&>` shall be `true`.

The default value of the `CompletionFunction` template parameter is an
unspecified type, such that, in addition to satisfying the requirements
of `CompletionFunction`, it meets the *Cpp17DefaultConstructible*
requirements ([[cpp17.defaultconstructible]]) and `completion()` has no
effects.

`barrier::arrival_token` is an unspecified type, such that it meets the
*Cpp17MoveConstructible* ([[cpp17.moveconstructible]]),
*Cpp17MoveAssignable* ([[cpp17.moveassignable]]), and
*Cpp17Destructible* ([[cpp17.destructible]]) requirements.

``` cpp
static constexpr ptrdiff_t max() noexcept;
```

*Returns:* The maximum expected count that the implementation supports.

``` cpp
constexpr explicit barrier(ptrdiff_t expected,
                           CompletionFunction f = CompletionFunction());
```

*Preconditions:* `expected >= 0` is `true` and `expected <= max()` is
`true`.

*Effects:* Sets both the initial expected count for each barrier phase
and the current expected count for the first phase to `expected`.
Initializes `completion` with `std::move(f)`. Starts the first phase.

[*Note 1*: If `expected` is 0 this object can only be
destroyed. — *end note*]

*Throws:* Any exception thrown by `CompletionFunction`’s move
constructor.

``` cpp
[[nodiscard]] arrival_token arrive(ptrdiff_t update = 1);
```

*Preconditions:* `update > 0` is `true`, and `update` is less than or
equal to the expected count for the current barrier phase.

*Effects:* Constructs an object of type `arrival_token` that is
associated with the phase synchronization point for the current phase.
Then, decrements the expected count by `update`.

*Synchronization:* The call to `arrive` strongly happens before the
start of the phase completion step for the current phase.

*Returns:* The constructed `arrival_token` object.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

[*Note 2*: This call can cause the completion step for the current
phase to start. — *end note*]

``` cpp
void wait(arrival_token&& arrival) const;
```

*Preconditions:* `arrival` is associated with the phase synchronization
point for the current phase or the immediately preceding phase of the
same barrier object.

*Effects:* Blocks at the synchronization point associated with
`std::move(arrival)` until the phase completion step of the
synchronization point’s phase is run.

[*Note 3*: If `arrival` is associated with the synchronization point
for a previous phase, the call returns immediately. — *end note*]

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

``` cpp
void arrive_and_wait();
```

*Effects:* Equivalent to: `wait(arrive())`.

``` cpp
void arrive_and_drop();
```

*Preconditions:* The expected count for the current barrier phase is
greater than zero.

*Effects:* Decrements the initial expected count for all subsequent
phases by one. Then decrements the expected count for the current phase
by one.

*Synchronization:* The call to `arrive_and_drop` strongly happens before
the start of the phase completion step for the current phase.

*Throws:* `system_error` when an exception is
required [[thread.req.exception]].

*Error conditions:* Any of the error conditions allowed for mutex
types [[thread.mutex.requirements.mutex]].

[*Note 4*: This call can cause the completion step for the current
phase to start. — *end note*]

## Futures <a id="futures">[[futures]]</a>

### Overview <a id="futures.overview">[[futures.overview]]</a>

[[futures]] describes components that a C++ program can use to retrieve
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

  template<> struct is_error_code_enum<future_errc> : public true_type { };
  error_code make_error_code(future_errc e) noexcept;
  error_condition make_error_condition(future_errc e) noexcept;

  const error_category& future_category() noexcept;

  class future_error;

  template<class R> class promise;
  template<class R> class promise<R&>;
  template<> class promise<void>;

  template<class R>
    void swap(promise<R>& x, promise<R>& y) noexcept;

  template<class R, class Alloc>
    struct uses_allocator<promise<R>, Alloc>;

  template<class R> class future;
  template<class R> class future<R&>;
  template<> class future<void>;

  template<class R> class shared_future;
  template<class R> class shared_future<R&>;
  template<> class shared_future<void>;

  template<class> class packaged_task;  // not defined
  template<class R, class... ArgTypes>
    class packaged_task<R(ArgTypes...)>;

  template<class R, class... ArgTypes>
    void swap(packaged_task<R(ArgTypes...)>&, packaged_task<R(ArgTypes...)>&) noexcept;

  template<class F, class... Args>
    [[nodiscard]] future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
      async(F&& f, Args&&... args);
  template<class F, class... Args>
    [[nodiscard]] future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
      async(launch policy, F&& f, Args&&... args);
}
```

The `enum` type `launch` is a bitmask type [[bitmask.types]] with
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

*Returns:* A reference to an object of a type derived from class
`error_category`.

The object’s `default_error_condition` and equivalent virtual functions
shall behave as specified for the class `error_category`. The object’s
`name` virtual function returns a pointer to the string `"future"`.

``` cpp
error_code make_error_code(future_errc e) noexcept;
```

*Returns:* `error_code(static_cast<int>(e), future_category())`.

``` cpp
error_condition make_error_condition(future_errc e) noexcept;
```

*Returns:* `error_condition(static_cast<int>(e), future_category())`.

### Class `future_error` <a id="futures.future.error">[[futures.future.error]]</a>

``` cpp
namespace std {
  class future_error : public logic_error {
  public:
    explicit future_error(future_errc e);

    const error_code& code() const noexcept;
    const char*       what() const noexcept;

  private:
    error_code ec_;             // exposition only
  };
}
```

``` cpp
explicit future_error(future_errc e);
```

*Effects:* Initializes `ec_` with `make_error_code(e)`.

``` cpp
const error_code& code() const noexcept;
```

*Returns:* `ec_`.

``` cpp
const char* what() const noexcept;
```

*Returns:* An NTBS incorporating `code().message()`.

### Shared state <a id="futures.state">[[futures.state]]</a>

Many of the classes introduced in subclause  [[futures]] use some state
to communicate results. This *shared state* consists of some state
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
because of a timeout [[thread.req.lockable]], then it is a *timed
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
state synchronize with [[intro.multithread]] calls to functions
successfully detecting the ready state resulting from that setting. The
storage of the result (whether normal or exceptional) into the shared
state synchronizes with [[intro.multithread]] the successful return from
a call to a waiting function on the shared state.

Some functions (e.g., `promise::set_value_at_thread_exit`) delay making
the shared state ready until the calling thread exits. The destruction
of each of that thread’s objects with thread storage duration
[[basic.stc.thread]] is sequenced before making that shared state ready.

Access to the result of the same shared state may conflict
[[intro.multithread]].

[*Note 4*: This explicitly specifies that the result of the shared
state is visible in the objects that reference this state in the sense
of data race avoidance [[res.on.data.races]]. For example, concurrent
accesses through references returned by `shared_future::get()`
[[futures.shared.future]] must either use read-only operations or
provide additional synchronization. — *end note*]

### Class template `promise` <a id="futures.promise">[[futures.promise]]</a>

``` cpp
namespace std {
  template<class R>
  class promise {
  public:
    promise();
    template<class Allocator>
      promise(allocator_arg_t, const Allocator& a);
    promise(promise&& rhs) noexcept;
    promise(const promise&) = delete;
    ~promise();

    // assignment
    promise& operator=(promise&& rhs) noexcept;
    promise& operator=(const promise&) = delete;
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

  template<class R>
    void swap(promise<R>& x, promise<R>& y) noexcept;

  template<class R, class Alloc>
    struct uses_allocator<promise<R>, Alloc>;
}
```

The implementation provides the template `promise` and two
specializations, `promise<R&>` and `promise<{}void>`. These differ only
in the argument type of the member functions `set_value` and
`set_value_at_thread_exit`, as set out in their descriptions, below.

The `set_value`, `set_exception`, `set_value_at_thread_exit`, and
`set_exception_at_thread_exit` member functions behave as though they
acquire a single mutex associated with the promise object while updating
the promise object.

``` cpp
template<class R, class Alloc>
  struct uses_allocator<promise<R>, Alloc>
    : true_type { };
```

*Preconditions:* `Alloc` meets the *Cpp17Allocator* requirements
([[cpp17.allocator]]).

``` cpp
promise();
template<class Allocator>
  promise(allocator_arg_t, const Allocator& a);
```

*Effects:* Creates a shared state. The second constructor uses the
allocator `a` to allocate memory for the shared state.

``` cpp
promise(promise&& rhs) noexcept;
```

*Effects:* Transfers ownership of the shared state of `rhs` (if any) to
the newly-constructed object.

*Ensures:* `rhs` has no shared state.

``` cpp
~promise();
```

*Effects:* Abandons any shared state [[futures.state]].

``` cpp
promise& operator=(promise&& rhs) noexcept;
```

*Effects:* Abandons any shared state [[futures.state]] and then as if
`promise(std::move(rhs)).swap(*this)`.

*Returns:* `*this`.

``` cpp
void swap(promise& other) noexcept;
```

*Effects:* Exchanges the shared state of `*this` and `other`.

*Ensures:* `*this` has the shared state (if any) that `other` had prior
to the call to `swap`. `other` has the shared state (if any) that
`*this` had prior to the call to `swap`.

``` cpp
future<R> get_future();
```

*Returns:* A `future<R>` object with the same shared state as `*this`.

*Synchronization:* Calls to this function do not introduce data
races  [[intro.multithread]] with calls to `set_value`, `set_exception`,
`set_value_at_thread_exit`, or `set_exception_at_thread_exit`.

[*Note 1*: Such calls need not synchronize with each
other. — *end note*]

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
that state ready [[futures.state]].

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

*Preconditions:* `p` is not null.

*Effects:* Atomically stores the exception pointer `p` in the shared
state and makes that state ready [[futures.state]].

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

*Preconditions:* `p` is not null.

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
template<class R>
  void swap(promise<R>& x, promise<R>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

### Class template `future` <a id="futures.unique.future">[[futures.unique.future]]</a>

The class template `future` defines a type for asynchronous return
objects which do not share their shared state with other asynchronous
return objects. A default-constructed `future` object has no shared
state. A `future` object with shared state can be created by functions
on asynchronous providers [[futures.state]] or by the move constructor
and shares its shared state with the original asynchronous provider. The
result (value or exception) of a `future` object can be set by calling a
respective function on an object that shares the same shared state.

[*Note 1*: Member functions of `future` do not synchronize with
themselves or with member functions of `shared_future`. — *end note*]

The effect of calling any member function other than the destructor, the
move-assignment operator, `share`, or `valid` on a `future` object for
which `valid() == false` is undefined.

[*Note 2*: It is valid to move from a future object for which
`valid() == false`. — *end note*]

[*Note 3*: Implementations should detect this case and throw an object
of type `future_error` with an error condition of
`future_errc::no_state`. — *end note*]

``` cpp
namespace std {
  template<class R>
  class future {
  public:
    future() noexcept;
    future(future&&) noexcept;
    future(const future&) = delete;
    ~future();
    future& operator=(const future&) = delete;
    future& operator=(future&&) noexcept;
    shared_future<R> share() noexcept;

    // retrieving the value
    see below get();

    // functions to check state
    bool valid() const noexcept;

    void wait() const;
    template<class Rep, class Period>
      future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
    template<class Clock, class Duration>
      future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
  };
}
```

The implementation provides the template `future` and two
specializations, `future<R&>` and `future<{}void>`. These differ only in
the return type and return value of the member function `get`, as set
out in its description, below.

``` cpp
future() noexcept;
```

*Effects:* The object does not refer to a shared state.

*Ensures:* `valid() == false`.

``` cpp
future(future&& rhs) noexcept;
```

*Effects:* Move constructs a `future` object that refers to the shared
state that was originally referred to by `rhs` (if any).

*Ensures:*

- `valid()` returns the same value as `rhs.valid()` prior to the
  constructor invocation.
- `rhs.valid() == false`.

``` cpp
~future();
```

*Effects:*

- Releases any shared state [[futures.state]];
- destroys `*this`.

``` cpp
future& operator=(future&& rhs) noexcept;
```

*Effects:*

- Releases any shared state [[futures.state]].
- move assigns the contents of `rhs` to `*this`.

*Ensures:*

- `valid()` returns the same value as `rhs.valid()` prior to the
  assignment.
- `rhs.valid() == false`.

``` cpp
shared_future<R> share() noexcept;
```

*Returns:* `shared_future<R>(std::move(*this))`.

*Ensures:* `valid() == false`.

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
- releases any shared state [[futures.state]].

*Returns:*

- `future::get()` returns the value `v` stored in the object’s shared
  state as `std::move(v)`.
- `future<R&>::get()` returns the reference stored as value in the
  object’s shared state.
- `future<void>::get()` returns nothing.

*Throws:* The stored exception, if an exception was stored in the shared
state.

*Ensures:* `valid() == false`.

``` cpp
bool valid() const noexcept;
```

*Returns:* `true` only if `*this` refers to a shared state.

``` cpp
void wait() const;
```

*Effects:* Blocks until the shared state is ready.

``` cpp
template<class Rep, class Period>
  future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
```

*Effects:* None if the shared state contains a deferred
function [[futures.async]], otherwise blocks until the shared state is
ready or until the relative timeout [[thread.req.timing]] specified by
`rel_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  relative timeout [[thread.req.timing]] specified by `rel_time` has
  expired.

*Throws:* timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Clock, class Duration>
  future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
```

*Effects:* None if the shared state contains a deferred
function [[futures.async]], otherwise blocks until the shared state is
ready or until the absolute timeout [[thread.req.timing]] specified by
`abs_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  absolute timeout [[thread.req.timing]] specified by `abs_time` has
  expired.

*Throws:* timeout-related exceptions [[thread.req.timing]].

### Class template `shared_future` <a id="futures.shared.future">[[futures.shared.future]]</a>

The class template `shared_future` defines a type for asynchronous
return objects which may share their shared state with other
asynchronous return objects. A default-constructed `shared_future`
object has no shared state. A `shared_future` object with shared state
can be created by conversion from a `future` object and shares its
shared state with the original asynchronous provider [[futures.state]]
of the shared state. The result (value or exception) of a
`shared_future` object can be set by calling a respective function on an
object that shares the same shared state.

[*Note 1*: Member functions of `shared_future` do not synchronize with
themselves, but they synchronize with the shared state. — *end note*]

The effect of calling any member function other than the destructor, the
move-assignment operator, the copy-assignment operator, or `valid()` on
a `shared_future` object for which `valid() == false` is undefined.

[*Note 2*: It is valid to copy or move from a `shared_future` object
for which `valid()` is `false`. — *end note*]

[*Note 3*: Implementations should detect this case and throw an object
of type `future_error` with an error condition of
`future_errc::no_state`. — *end note*]

``` cpp
namespace std {
  template<class R>
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
    template<class Rep, class Period>
      future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
    template<class Clock, class Duration>
      future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
  };
}
```

The implementation provides the template `shared_future` and two
specializations, `shared_future<R&>` and `shared_future<void>`. These
differ only in the return type and return value of the member function
`get`, as set out in its description, below.

``` cpp
shared_future() noexcept;
```

*Effects:* The object does not refer to a shared state.

*Ensures:* `valid() == false`.

``` cpp
shared_future(const shared_future& rhs) noexcept;
```

*Effects:* The object refers to the same shared state as `rhs` (if any).

*Ensures:* `valid()` returns the same value as `rhs.valid()`.

``` cpp
shared_future(future<R>&& rhs) noexcept;
shared_future(shared_future&& rhs) noexcept;
```

*Effects:* Move constructs a `shared_future` object that refers to the
shared state that was originally referred to by `rhs` (if any).

*Ensures:*

- `valid()` returns the same value as `rhs.valid()` returned prior to
  the constructor invocation.
- `rhs.valid() == false`.

``` cpp
~shared_future();
```

*Effects:*

- Releases any shared state [[futures.state]];
- destroys `*this`.

``` cpp
shared_future& operator=(shared_future&& rhs) noexcept;
```

*Effects:*

- Releases any shared state [[futures.state]];
- move assigns the contents of `rhs` to `*this`.

*Ensures:*

- `valid()` returns the same value as `rhs.valid()` returned prior to
  the assignment.
- `rhs.valid() == false`.

``` cpp
shared_future& operator=(const shared_future& rhs) noexcept;
```

*Effects:*

- Releases any shared state [[futures.state]];
- assigns the contents of `rhs` to `*this`. \[*Note 4*: As a result,
  `*this` refers to the same shared state as `rhs` (if
  any). — *end note*]

*Ensures:* `valid() == rhs.valid()`.

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
that do not introduce a data race [[intro.multithread]]. — *end note*]

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

*Throws:* The stored exception, if an exception was stored in the shared
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
template<class Rep, class Period>
  future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
```

*Effects:* None if the shared state contains a deferred
function [[futures.async]], otherwise blocks until the shared state is
ready or until the relative timeout [[thread.req.timing]] specified by
`rel_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  relative timeout [[thread.req.timing]] specified by `rel_time` has
  expired.

*Throws:* timeout-related exceptions [[thread.req.timing]].

``` cpp
template<class Clock, class Duration>
  future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
```

*Effects:* None if the shared state contains a deferred
function [[futures.async]], otherwise blocks until the shared state is
ready or until the absolute timeout [[thread.req.timing]] specified by
`abs_time` has expired.

*Returns:*

- `future_status::deferred` if the shared state contains a deferred
  function.
- `future_status::ready` if the shared state is ready.
- `future_status::timeout` if the function is returning because the
  absolute timeout [[thread.req.timing]] specified by `abs_time` has
  expired.

*Throws:* timeout-related exceptions [[thread.req.timing]].

### Function template `async` <a id="futures.async">[[futures.async]]</a>

The function template `async` provides a mechanism to launch a function
potentially in a new thread and provides the result of the function in a
`future` object with which it shares a shared state.

``` cpp
template<class F, class... Args>
  [[nodiscard]] future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
    async(F&& f, Args&&... args);
template<class F, class... Args>
  [[nodiscard]] future<invoke_result_t<decay_t<F>, decay_t<Args>...>>
    async(launch policy, F&& f, Args&&... args);
```

*Mandates:* The following are all `true`:

- `is_constructible_v<decay_t<F>, F>`,
- `(is_constructible_v<decay_t<Args>, Args> &&...)`,
- `is_move_constructible_v<decay_t<F>>`,
- `(is_move_constructible_v<decay_t<Args>> &&...)`, and
- `is_invocable_v<decay_t<F>, decay_t<Args>...>`.

*Preconditions:* `decay_t<F>` and each type in `decay_t<Args>` meet the
*Cpp17MoveConstructible* requirements.

*Effects:* The first function behaves the same as a call to the second
function with a `policy` argument of `launch::async | launch::deferred`
and the same arguments for `F` and `Args`. The second function creates a
shared state that is associated with the returned `future` object. The
further behavior of the second function depends on the `policy` argument
as follows (if more than one of these conditions applies, the
implementation may choose any of the corresponding policies):

- If `launch::async` is set in `policy`, calls
  `invoke(`*`decay-copy`*`(std::forward<F>(f)),`
  *decay-copy*(std::forward\<Args\>(args))...) ([[func.require]],
  [[thread.thread.constr]]) as if in a new thread of execution
  represented by a `thread` object with the calls to *`decay-copy`*
  being evaluated in the thread that called `async`. Any return value is
  stored as the result in the shared state. Any exception propagated
  from the execution of
  `invoke(`*`decay-copy`*`(std::forward<F>(f)), `*`decay-copy`*`(std::forward<Args>(args))...)`
  is stored as the exceptional result in the shared state. The `thread`
  object is stored in the shared state and affects the behavior of any
  asynchronous return objects that reference that state.
- If `launch::deferred` is set in `policy`, stores
  *decay-copy*(std::forward\<F\>(f)) and
  *decay-copy*(std::forward\<Args\>(args))... in the shared state. These
  copies of `f` and `args` constitute a *deferred function*. Invocation
  of the deferred function evaluates
  `invoke(std::move(g), std::move(xyz))` where `g` is the stored value
  of *decay-copy*(std::forward\<F\>(f)) and `xyz` is the stored copy of
  *decay-copy*(std::forward\<Args\>(args)).... Any return value is
  stored as the result in the shared state. Any exception propagated
  from the execution of the deferred function is stored as the
  exceptional result in the shared state. The shared state is not made
  ready until the function has completed. The first call to a non-timed
  waiting function [[futures.state]] on an asynchronous return object
  referring to this shared state invokes the deferred function in the
  thread that called the waiting function. Once evaluation of
  `invoke(std::move(g), std::move(xyz))` begins, the function is no
  longer considered deferred. \[*Note 1*: If this policy is specified
  together with other policies, such as when using a `policy` value of
  `launch::async | launch::deferred`, implementations should defer
  invocation or the selection of the policy when no more concurrency can
  be effectively exploited. — *end note*]
- If no value is set in the launch policy, or a value is set that is
  neither specified in this document nor by the implementation, the
  behavior is undefined.

*Returns:* An object of type
`future<invoke_result_t<decay_t<F>, decay_t<Args>...>``>` that refers to
the shared state created by this call to `async`.

[*Note 1*: If a future obtained from `async` is moved outside the local
scope, other code that uses the future should be aware that the future’s
destructor can block for the shared state to become
ready. — *end note*]

*Synchronization:* Regardless of the provided `policy` argument,

- the invocation of `async` synchronizes with [[intro.multithread]] the
  invocation of `f`. \[*Note 2*: This statement applies even when the
  corresponding `future` object is moved to another
  thread. — *end note*] ; and
- the completion of the function `f` is sequenced
  before [[intro.multithread]] the shared state is made ready.
  \[*Note 3*: `f` might not be called at all, so its completion might
  never happen. — *end note*]

If the implementation chooses the `launch::async` policy,

- a call to a waiting function on an asynchronous return object that
  shares the shared state created by this `async` call shall block until
  the associated thread has completed, as if joined, or else time
  out [[thread.thread.member]];
- the associated thread completion synchronizes
  with [[intro.multithread]] the return from the first function that
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
  template<class> class packaged_task;  // not defined

  template<class R, class... ArgTypes>
  class packaged_task<R(ArgTypes...)> {
  public:
    // construction and destruction
    packaged_task() noexcept;
    template<class F>
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

  template<class R, class... ArgTypes>
    void swap(packaged_task<R(ArgTypes...)>& x, packaged_task<R(ArgTypes...)>& y) noexcept;
}
```

#### Member functions <a id="futures.task.members">[[futures.task.members]]</a>

``` cpp
packaged_task() noexcept;
```

*Effects:* The object has no shared state and no stored task.

``` cpp
template<class F>
  packaged_task(F&& f);
```

*Constraints:* `remove_cvref_t<F>` is not the same type as
`packaged_task<R(ArgTypes...)>`.

*Mandates:* `is_invocable_r_v<R, F&, ArgTypes...>` is `true`.

*Preconditions:* Invoking a copy of `f` behaves the same as invoking
`f`.

*Effects:* Constructs a new `packaged_task` object with a shared state
and initializes the object’s stored task with `std::forward<F>(f)`.

*Throws:* Any exceptions thrown by the copy or move constructor of `f`,
or `bad_alloc` if memory for the internal data structures could not be
allocated.

``` cpp
packaged_task(packaged_task&& rhs) noexcept;
```

*Effects:* Transfers ownership of `rhs`’s shared state to `*this`,
leaving `rhs` with no shared state. Moves the stored task from `rhs` to
`*this`.

*Ensures:* `rhs` has no shared state.

``` cpp
packaged_task& operator=(packaged_task&& rhs) noexcept;
```

*Effects:*

- Releases any shared state [[futures.state]];
- calls `packaged_task(std::move(rhs)).swap(*this)`.

``` cpp
~packaged_task();
```

*Effects:* Abandons any shared state [[futures.state]].

``` cpp
void swap(packaged_task& other) noexcept;
```

*Effects:* Exchanges the shared states and stored tasks of `*this` and
`other`.

*Ensures:* `*this` has the same shared state and stored task (if any) as
`other` prior to the call to `swap`. `other` has the same shared state
and stored task (if any) as `*this` prior to the call to `swap`.

``` cpp
bool valid() const noexcept;
```

*Returns:* `true` only if `*this` has a shared state.

``` cpp
future<R> get_future();
```

*Returns:* A `future` object that shares the same shared state as
`*this`.

*Synchronization:* Calls to this function do not introduce data
races  [[intro.multithread]] with calls to `operator()` or
`make_ready_at_thread_exit`.

[*Note 1*: Such calls need not synchronize with each
other. — *end note*]

*Throws:* A `future_error` object if an error occurs.

*Error conditions:*

- `future_already_retrieved` if `get_future` has already been called on
  a `packaged_task` object with the same shared state as `*this`.
- `no_state` if `*this` has no shared state.

``` cpp
void operator()(ArgTypes... args);
```

*Effects:* As if by *INVOKE*\<R\>(f, t₁, t₂, …, t$_N$) [[func.require]],
where `f` is the stored task of `*this` and `t`₁`, t`₂`, `…`, t`$_N$ are
the values in `args...`. If the task returns normally, the return value
is stored as the asynchronous result in the shared state of `*this`,
otherwise the exception thrown by the task is stored. The shared state
of `*this` is made ready, and any threads blocked in a function waiting
for the shared state of `*this` to become ready are unblocked.

*Throws:* A `future_error` exception object if there is no shared state
or the stored task has already been invoked.

*Error conditions:*

- `promise_already_satisfied` if the stored task has already been
  invoked.
- `no_state` if `*this` has no shared state.

``` cpp
void make_ready_at_thread_exit(ArgTypes... args);
```

*Effects:* As if by *INVOKE*\<R\>(f, t₁, t₂, …, t$_N$) [[func.require]],
where `f` is the stored task and `t`₁`, t`₂`, `…`, t`$_N$ are the values
in `args...`. If the task returns normally, the return value is stored
as the asynchronous result in the shared state of `*this`, otherwise the
exception thrown by the task is stored. In either case, this is done
without making that state ready [[futures.state]] immediately. Schedules
the shared state to be made ready when the current thread exits, after
all objects of thread storage duration associated with the current
thread have been destroyed.

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

[*Note 2*: This constructs a new shared state for `*this`. The old
state is abandoned [[futures.state]]. — *end note*]

*Throws:*

- `bad_alloc` if memory for the new shared state could not be allocated.
- any exception thrown by the move constructor of the task stored in the
  shared state.
- `future_error` with an error condition of `no_state` if `*this` has no
  shared state.

#### Globals <a id="futures.task.nonmembers">[[futures.task.nonmembers]]</a>

``` cpp
template<class R, class... ArgTypes>
  void swap(packaged_task<R(ArgTypes...)>& x, packaged_task<R(ArgTypes...)>& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[atomics]: atomics.md#atomics
[barrier.syn]: #barrier.syn
[basic.life]: basic.md#basic.life
[basic.stc.thread]: basic.md#basic.stc.thread
[bitmask.types]: library.md#bitmask.types
[class.prop]: class.md#class.prop
[condition.variable.syn]: #condition.variable.syn
[cpp17.allocator]: #cpp17.allocator
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[cpp17.moveassignable]: #cpp17.moveassignable
[cpp17.moveconstructible]: #cpp17.moveconstructible
[defns.block]: intro.md#defns.block
[except.terminate]: except.md#except.terminate
[func.require]: utilities.md#func.require
[future.syn]: #future.syn
[futures]: #futures
[futures.async]: #futures.async
[futures.errors]: #futures.errors
[futures.future.error]: #futures.future.error
[futures.overview]: #futures.overview
[futures.promise]: #futures.promise
[futures.shared.future]: #futures.shared.future
[futures.state]: #futures.state
[futures.task]: #futures.task
[futures.task.members]: #futures.task.members
[futures.task.nonmembers]: #futures.task.nonmembers
[futures.unique.future]: #futures.unique.future
[intro.multithread]: basic.md#intro.multithread
[intro.races]: basic.md#intro.races
[latch.syn]: #latch.syn
[mutex.syn]: #mutex.syn
[res.on.data.races]: library.md#res.on.data.races
[res.on.exception.handling]: library.md#res.on.exception.handling
[semaphore.syn]: #semaphore.syn
[shared.mutex.syn]: #shared.mutex.syn
[stopcallback]: #stopcallback
[stopcallback.cons]: #stopcallback.cons
[stopsource]: #stopsource
[stopsource.cons]: #stopsource.cons
[stopsource.mem]: #stopsource.mem
[stopsource.nonmembers]: #stopsource.nonmembers
[stoptoken]: #stoptoken
[stoptoken.cons]: #stoptoken.cons
[stoptoken.mem]: #stoptoken.mem
[stoptoken.nonmembers]: #stoptoken.nonmembers
[syserr]: diagnostics.md#syserr
[syserr.syserr]: diagnostics.md#syserr.syserr
[thread]: #thread
[thread.barrier]: #thread.barrier
[thread.barrier.class]: #thread.barrier.class
[thread.condition]: #thread.condition
[thread.condition.condvar]: #thread.condition.condvar
[thread.condition.condvarany]: #thread.condition.condvarany
[thread.condition.nonmember]: #thread.condition.nonmember
[thread.condvarany.intwait]: #thread.condvarany.intwait
[thread.condvarany.wait]: #thread.condvarany.wait
[thread.coord]: #thread.coord
[thread.general]: #thread.general
[thread.jthread.class]: #thread.jthread.class
[thread.jthread.cons]: #thread.jthread.cons
[thread.jthread.mem]: #thread.jthread.mem
[thread.jthread.special]: #thread.jthread.special
[thread.jthread.static]: #thread.jthread.static
[thread.jthread.stop]: #thread.jthread.stop
[thread.latch]: #thread.latch
[thread.latch.class]: #thread.latch.class
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
[thread.sema]: #thread.sema
[thread.sema.cnt]: #thread.sema.cnt
[thread.sharedmutex.class]: #thread.sharedmutex.class
[thread.sharedmutex.requirements]: #thread.sharedmutex.requirements
[thread.sharedtimedmutex.class]: #thread.sharedtimedmutex.class
[thread.sharedtimedmutex.requirements]: #thread.sharedtimedmutex.requirements
[thread.stoptoken]: #thread.stoptoken
[thread.stoptoken.intro]: #thread.stoptoken.intro
[thread.stoptoken.syn]: #thread.stoptoken.syn
[thread.summary]: #thread.summary
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
[time]: time.md#time
[time.clock]: time.md#time.clock
[time.clock.req]: time.md#time.clock.req
[time.duration]: time.md#time.duration
[time.point]: time.md#time.point
[unord.hash]: utilities.md#unord.hash

[^1]: All implementations for which standard time units are meaningful
    must necessarily have a steady clock within their hardware
    implementation.
