# Execution control library <a id="exec">[[exec]]</a>

## General <a id="exec.general">[[exec.general]]</a>

This Clause describes components supporting execution of function
objects [[function.objects]].

The following subclauses describe the requirements, concepts, and
components for execution control primitives as summarized in
[[exec.summary]].

**Table: Execution control library summary**

| Subclause        |                  | Header        |
| ---------------- | ---------------- | ------------- |
| [[exec.sched]]   | Schedulers       | `<execution>` |
| [[exec.recv]]    | Receivers        |               |
| [[exec.opstate]] | Operation states |               |
| [[exec.snd]]     | Senders          |               |


[[exec.pos]] shows the types of customization point objects
[[customization.point.object]] used in the execution control library.

**Table: Types of customization point objects in the execution control library**

| Customization point | Purpose | Examples | object type |
| ------------------- | ------- | -------- | ----------- |
| core                | provide core execution functionality, and connection between core components | e.g., `connect`, `start` |
| completion functions | called by senders to announce the completion of the work (success, error, or cancellation) | `set_value`, `set_error`, `set_stopped` |
| senders             | allow the specialization of the provided sender algorithms | sender factories (e.g., `schedule`, `just`, `read_env`); sender adaptors (e.g., `continues_on`, `then`, `let_value`); sender consumers (e.g., `sync_wait`) |
| queries             | allow querying different properties of objects | general queries (e.g., `get_allocator`, `get_stop_token`); environment queries (e.g., `get_scheduler`, `get_delegation_scheduler`); scheduler queries (e.g., `get_forward_progress_guarantee`); sender attribute queries (e.g., `get_completion_scheduler`) |


This clause makes use of the following exposition-only entities.

For a subexpression `expr`, let `MANDATE-NOTHROW(expr)` be
expression-equivalent to `expr`.

*Mandates:* `noexcept(expr)` is `true`.

``` cpp
namespace std {
  template<class T>
    concept movable-value =                                     // exposition only
      move_constructible<decay_t<T>> &&
      constructible_from<decay_t<T>, T> &&
      (!is_array_v<remove_reference_t<T>>);
}
```

For function types `F1` and `F2` denoting `R1(Args1...)` and
`R2(Args2...)`, respectively, `MATCHING-SIG(F1, F2)` is `true` if and
only if `same_as<R1(Args1&&...), R2(Args2&&...)>` is `true`.

For a subexpression `err`, let `Err` be `decltype((err))` and let
`AS-EXCEPT-PTR(err)` be:

- `err` if `decay_t<Err>` denotes the type `exception_ptr`.
  *Preconditions:* `!err` is `false`.
- Otherwise, `make_exception_ptr(system_error(err))` if `decay_t<Err>`
  denotes the type `error_code`.
- Otherwise, `make_exception_ptr(err)`.

For a subexpression `expr`, let `AS-CONST(expr)` be
expression-equivalent to

``` cpp
[](const auto& x) noexcept -> const auto& { return x; }(expr)
```

## Queries and queryables <a id="exec.queryable">[[exec.queryable]]</a>

### General <a id="exec.queryable.general">[[exec.queryable.general]]</a>

A *queryable object* is a read-only collection of key/value pair where
each key is a customization point object known as a *query object*. A
*query* is an invocation of a query object with a queryable object as
its first argument and a (possibly empty) set of additional arguments. A
query imposes syntactic and semantic requirements on its invocations.

Let `q` be a query object, let `args` be a (possibly empty) pack of
subexpressions, let `env` be a subexpression that refers to a queryable
object `o` of type `O`, and let `cenv` be a subexpression referring to
`o` such that `decltype((cenv))` is `const O&`. The expression
`q(env, args...)` is equal to [[concepts.equality]] the expression
`q(cenv, args...)`.

The type of a query expression cannot be `void`.

The expression `q(env, args...)` is equality-preserving
[[concepts.equality]] and does not modify the query object or the
arguments.

If the expression `env.query(q, args...)` is well-formed, then it is
expression-equivalent to `q(env, args...)`.

Unless otherwise specified, the result of a query is valid as long as
the queryable object is valid.

### `queryable` concept <a id="exec.queryable.concept">[[exec.queryable.concept]]</a>

``` cpp
namespace std {
  template<class T>
    concept queryable = destructible<T>;   // exposition only
}
```

The exposition-only `queryable` concept specifies the constraints on the
types of queryable objects.

Let `env` be an object of type `Env`. The type `Env` models `queryable`
if for each callable object `q` and a pack of subexpressions `args`, if
`requires { q(env, args...) }` is `true` then `q(env, args...)` meets
any semantic requirements imposed by `q`.

## Asynchronous operations <a id="exec.async.ops">[[exec.async.ops]]</a>

An *execution resource* is a program entity that manages a (possibly
dynamic) set of execution agents [[thread.req.lockable.general]], which
it uses to execute parallel work on behalf of callers.

[*Example 1*: The currently active thread, a system-provided thread
pool, and uses of an API associated with an external hardware
accelerator are all examples of execution resources. — *end example*]

Execution resources execute asynchronous operations. An execution
resource is either valid or invalid.

An *asynchronous operation* is a distinct unit of program execution that

- is explicitly created;
- can be explicitly started once at most;
- once started, eventually completes exactly once with a (possibly
  empty) set of result datums and in exactly one of three
  *dispositions*: success, failure, or cancellation;
  - A successful completion, also known as a *value completion*, can
    have an arbitrary number of result datums.
  - A failure completion, also known as an *error completion*, has a
    single result datum.
  - A cancellation completion, also known as a *stopped completion*, has
    no result datum.

  An asynchronous operation’s *async result* is its disposition and its
  (possibly empty) set of result datums.
- can complete on a different execution resource than the execution
  resource on which it started; and
- can create and start other asynchronous operations called
  *child operations*. A child operation is an asynchronous operation
  that is created by the parent operation and, if started, completes
  before the parent operation completes. A *parent operation* is the
  asynchronous operation that created a particular child operation.

[*Note 1*: An asynchronous operation can execute synchronously; that
is, it can complete during the execution of its start operation on the
thread of execution that started it. — *end note*]

An asynchronous operation has associated state known as its
*operation state*.

An asynchronous operation has an associated environment. An
*environment* is a queryable object [[exec.queryable]] representing the
execution-time properties of the operation’s caller. The caller of an
asynchronous operation is its parent operation or the function that
created it.

An asynchronous operation has an associated receiver. A *receiver* is an
aggregation of three handlers for the three asynchronous completion
dispositions:

- a value completion handler for a value completion,
- an error completion handler for an error completion, and
- a stopped completion handler for a stopped completion.

A receiver has an associated environment. An asynchronous operation’s
operation state owns the operation’s receiver. The environment of an
asynchronous operation is equal to its receiver’s environment.

For each completion disposition, there is a *completion function*. A
completion function is a customization point object
[[customization.point.object]] that accepts an asynchronous operation’s
receiver as the first argument and the result datums of the asynchronous
operation as additional arguments. The value completion function invokes
the receiver’s value completion handler with the value result datums;
likewise for the error completion function and the stopped completion
function. A completion function has an associated type known as its
*completion tag* that is the unqualified type of the completion
function. A valid invocation of a completion function is called a
*completion operation*.

The *lifetime of an asynchronous operation*, also known as the
operation’s *async lifetime*, begins when its start operation begins
executing and ends when its completion operation begins executing. If
the lifetime of an asynchronous operation’s associated operation state
ends before the lifetime of the asynchronous operation, the behavior is
undefined. After an asynchronous operation executes a completion
operation, its associated operation state is invalid. Accessing any part
of an invalid operation state is undefined behavior.

An asynchronous operation shall not execute a completion operation
before its start operation has begun executing. After its start
operation has begun executing, exactly one completion operation shall
execute. The lifetime of an asynchronous operation’s operation state can
end during the execution of the completion operation.

A *sender* is a factory for one or more asynchronous operations.
*Connecting* a sender and a receiver creates an asynchronous operation.
The asynchronous operation’s associated receiver is equal to the
receiver used to create it, and its associated environment is equal to
the environment associated with the receiver used to create it. The
lifetime of an asynchronous operation’s associated operation state does
not depend on the lifetimes of either the sender or the receiver from
which it was created. A sender is started when it is connected to a
receiver and the resulting asynchronous operation is started. A sender’s
async result is the async result of the asynchronous operation created
by connecting it to a receiver. A sender sends its results by way of the
asynchronous operation(s) it produces, and a receiver receives those
results. A sender is either valid or invalid; it becomes invalid when
its parent sender (see below) becomes invalid.

A *scheduler* is an abstraction of an execution resource with a uniform,
generic interface for scheduling work onto that resource. It is a
factory for senders whose asynchronous operations execute value
completion operations on an execution agent belonging to the scheduler’s
associated execution resource. A *schedule-expression* obtains such a
sender from a scheduler. A *schedule sender* is the result of a schedule
expression. On success, an asynchronous operation produced by a schedule
sender executes a value completion operation with an empty set of result
datums. Multiple schedulers can refer to the same execution resource. A
scheduler can be valid or invalid. A scheduler becomes invalid when the
execution resource to which it refers becomes invalid, as do any
schedule senders obtained from the scheduler, and any operation states
obtained from those senders.

An asynchronous operation has one or more associated completion
schedulers for each of its possible dispositions. A *completion
scheduler* is a scheduler whose associated execution resource is used to
execute a completion operation for an asynchronous operation. A value
completion scheduler is a scheduler on which an asynchronous operation’s
value completion operation can execute. Likewise for error completion
schedulers and stopped completion schedulers.

A sender has an associated queryable object [[exec.queryable]] known as
its *attributes* that describes various characteristics of the sender
and of the asynchronous operation(s) it produces. For each disposition,
there is a query object for reading the associated completion scheduler
from a sender’s attributes; i.e., a value completion scheduler query
object for reading a sender’s value completion scheduler, etc. If a
completion scheduler query is well-formed, the returned completion
scheduler is unique for that disposition for any asynchronous operation
the sender creates. A schedule sender is required to have a value
completion scheduler attribute whose value is equal to the scheduler
that produced the schedule sender.

A *completion signature* is a function type that describes a completion
operation. An asynchronous operation has a finite set of possible
completion signatures corresponding to the completion operations that
the asynchronous operation potentially evaluates [[basic.def.odr]]. For
a completion function `set`, receiver `rcvr`, and pack of arguments
`args`, let `c` be the completion operation `set(rcvr, args...)`, and
let `F` be the function type `decltype(auto(set))(decltype((args))...)`.
A completion signature `Sig` is associated with `c` if and only if
`MATCHING-SIG(Sig, F)` is `true` [[exec.general]]. Together, a sender
type and an environment type `Env` determine the set of completion
signatures of an asynchronous operation that results from connecting the
sender with a receiver that has an environment of type `Env`. The type
of the receiver does not affect an asynchronous operation’s completion
signatures, only the type of the receiver’s environment. A
*non-dependent sender* is a sender type whose completion signatures are
knowable independent of an execution environment.

A sender algorithm is a function that takes and/or returns a sender.
There are three categories of sender algorithms:

- A *sender factory* is a function that takes non-senders as arguments
  and that returns a sender.
- A *sender adaptor* is a function that constructs and returns a parent
  sender from a set of one or more child senders and a (possibly empty)
  set of additional arguments. An asynchronous operation created by a
  parent sender is a parent operation to the child operations created by
  the child senders.
- A *sender consumer* is a function that takes one or more senders and a
  (possibly empty) set of additional arguments, and whose return type is
  not the type of a sender.

## Header `<execution>` synopsis <a id="execution.syn">[[execution.syn]]</a>

``` cpp
namespace std {
  // [execpol.type], execution policy type trait
  template<class T> struct is_execution_policy;                 // freestanding
  template<class T> constexpr bool is_execution_policy_v =      // freestanding
      is_execution_policy<T>::value;
}

namespace std::execution {
  // [execpol.seq], sequenced execution policy
  class sequenced_policy;

  // [execpol.par], parallel execution policy
  class parallel_policy;

  // [execpol.parunseq], parallel and unsequenced execution policy
  class parallel_unsequenced_policy;

  // [execpol.unseq], unsequenced execution policy
  class unsequenced_policy;

  // [execpol.objects], execution policy objects
  inline constexpr sequenced_policy            seq{ unspecified };
  inline constexpr parallel_policy             par{ unspecified };
  inline constexpr parallel_unsequenced_policy par_unseq{ unspecified };
  inline constexpr unsequenced_policy          unseq{ unspecified };
}

namespace std {
  // [exec.general], helper concepts
  template<class T>
    concept exposition onlyconceptnc{movable-value} = see belownc;                          // exposition only

  template<class From, class To>
    concept decays-to = same_as<decay_t<From>, To>;             // exposition only

  template<class T>
    concept class-type = exposition onlyconceptnc{decays-to}<T, T> && is_class_v<T>;      // exposition only

  // [exec.queryable], queryable objects
  template<class T>
    concept exposition onlyconceptnc{queryable} = see belownc;                              // exposition only

  // [exec.queries], queries
  struct forwarding_query_t { unspecified };
  struct get_allocator_t { unspecified };
  struct get_stop_token_t { unspecified };

  inline constexpr forwarding_query_t forwarding_query{};
  inline constexpr get_allocator_t get_allocator{};
  inline constexpr get_stop_token_t get_stop_token{};

  template<class T>
    using stop_token_of_t = remove_cvref_t<decltype(get_stop_token(declval<T>()))>;

  template<class T>
    concept forwarding-query = forwarding_query(T{});           // exposition only
}

namespace std::execution {
  // [exec.queries], queries
  struct get_domain_t { unspecified };
  struct get_scheduler_t { unspecified };
  struct get_delegation_scheduler_t { unspecified };
  struct get_forward_progress_guarantee_t { unspecified };
  template<class CPO>
    struct get_completion_scheduler_t { unspecified };
  struct get_await_completion_adaptor_t { unspecified };

  inline constexpr get_domain_t get_domain{};
  inline constexpr get_scheduler_t get_scheduler{};
  inline constexpr get_delegation_scheduler_t get_delegation_scheduler{};
  enum class forward_progress_guarantee;
  inline constexpr get_forward_progress_guarantee_t get_forward_progress_guarantee{};
  template<class CPO>
    constexpr get_completion_scheduler_t<CPO> get_completion_scheduler{};
  inline constexpr get_await_completion_adaptor_t get_await_completion_adaptor{};

  struct get_env_t { unspecified };
  inline constexpr get_env_t get_env{};

  template<class T>
    using env_of_t = decltype(get_env(declval<T>()));

  // [exec.domain.default], execution domains
  struct default_domain;

  // [exec.sched], schedulers
  struct scheduler_t {};

  template<class Sch>
    concept scheduler = see below;

  // [exec.recv], receivers
  struct receiver_t {};

  template<class Rcvr>
    concept receiver = see below;

  template<class Rcvr, class Completions>
    concept receiver_of = see below;

  struct set_value_t { unspecified };
  struct set_error_t { unspecified };
  struct set_stopped_t { unspecified };

  inline constexpr set_value_t set_value{};
  inline constexpr set_error_t set_error{};
  inline constexpr set_stopped_t set_stopped{};

  // [exec.opstate], operation states
  struct operation_state_t {};

  template<class O>
    concept operation_state = see below;

  struct start_t;
  inline constexpr start_t start{};

  // [exec.snd], senders
  struct sender_t {};

  template<class Sndr>
    inline constexpr bool enable_sender = see below;

  template<class Sndr>
    concept sender = see below;

  template<class Sndr, class... Env>
    concept sender_in = see below;

  template<class Sndr>
    concept dependent_sender = see below;

  template<class Sndr, class Rcvr>
    concept sender_to = see below;

  template<class... Ts>
    struct type-list;                                           // exposition only

  template<class... Ts>
    using decayed-tuple = tuple<decay_t<Ts>...>;                // exposition only

  template<class... Ts>
    using variant-or-empty = see belownc;                         // exposition only

  template<class Sndr, class Env = env<>,
           template<class...> class Tuple = decayed-tuple,
           template<class...> class Variant = variant-or-empty>
      requires sender_in<Sndr, Env>
    using value_types_of_t = see below;

  template<class Sndr, class Env = env<>,
           template<class...> class Variant = variant-or-empty>
      requires sender_in<Sndr, Env>
    using error_types_of_t = see below;

  template<class Sndr, class Env = env<>>
      requires sender_in<Sndr, Env>
    constexpr bool sends_stopped = see below;

  template<class Sndr, class... Env>
    using single-sender-value-type = see belownc;                 // exposition only

  template<class Sndr, class... Env>
    concept single-sender = see below; // exposition only

  template<sender Sndr>
    using tag_of_t = see below;

  // [exec.snd.transform], sender transformations
  template<class Domain, sender Sndr, queryable... Env>
      requires (sizeof...(Env) <= 1)
    constexpr sender decltype(auto) transform_sender(
      Domain dom, Sndr&& sndr, const Env&... env) noexcept(see below);

  // [exec.snd.transform.env], environment transformations
  template<class Domain, sender Sndr, queryable Env>
    constexpr queryable decltype(auto) transform_env(
      Domain dom, Sndr&& sndr, Env&& env) noexcept;

  // [exec.snd.apply], sender algorithm application
  template<class Domain, class Tag, sender Sndr, class... Args>
    constexpr decltype(auto) apply_sender(
      Domain dom, Tag, Sndr&& sndr, Args&&... args) noexcept(see below);

  // [exec.getcomplsigs], get completion signatures
  template<class Sndr, class... Env>
    consteval auto get_completion_signatures() -> valid-completion-signatures auto;

  template<class Sndr, class... Env>
      requires sender_in<Sndr, Env...>
    using completion_signatures_of_t = decltype(get_completion_signatures<Sndr, Env...>());

  // [exec.connect], the connect sender algorithm
  struct connect_t;
  inline constexpr connect_t connect{};

  template<class Sndr, class Rcvr>
    using connect_result_t =
      decltype(connect(declval<Sndr>(), declval<Rcvr>()));

  // [exec.factories], sender factories
  struct just_t { unspecified };
  struct just_error_t { unspecified };
  struct just_stopped_t { unspecified };
  struct schedule_t { unspecified };

  inline constexpr just_t just{};
  inline constexpr just_error_t just_error{};
  inline constexpr just_stopped_t just_stopped{};
  inline constexpr schedule_t schedule{};
  inline constexpr unspecified read_env{};

  template<scheduler Sch>
    using schedule_result_t = decltype(schedule(declval<Sch>()));

  // [exec.adapt], sender adaptors
  template<class-type D>
    struct sender_adaptor_closure { };

  struct starts_on_t { unspecified };
  struct continues_on_t { unspecified };
  struct on_t { unspecified };
  struct schedule_from_t { unspecified };
  struct then_t { unspecified };
  struct upon_error_t { unspecified };
  struct upon_stopped_t { unspecified };
  struct let_value_t { unspecified };
  struct let_error_t { unspecified };
  struct let_stopped_t { unspecified };
  struct bulk_t { unspecified };
  struct bulk_chunked_t { unspecified };
  struct bulk_unchunked_t { unspecified };
  struct when_all_t { unspecified };
  struct when_all_with_variant_t { unspecified };
  struct into_variant_t { unspecified };
  struct stopped_as_optional_t { unspecified };
  struct stopped_as_error_t { unspecified };
  struct associate_t { unspecified };
  struct spawn_future_t { unspecified };

  inline constexpr unspecified write_env{};
  inline constexpr unspecified unstoppable{};
  inline constexpr starts_on_t starts_on{};
  inline constexpr continues_on_t continues_on{};
  inline constexpr on_t on{};
  inline constexpr schedule_from_t schedule_from{};
  inline constexpr then_t then{};
  inline constexpr upon_error_t upon_error{};
  inline constexpr upon_stopped_t upon_stopped{};
  inline constexpr let_value_t let_value{};
  inline constexpr let_error_t let_error{};
  inline constexpr let_stopped_t let_stopped{};
  inline constexpr bulk_t bulk{};
  inline constexpr bulk_chunked_t bulk_chunked{};
  inline constexpr bulk_unchunked_t bulk_unchunked{};
  inline constexpr when_all_t when_all{};
  inline constexpr when_all_with_variant_t when_all_with_variant{};
  inline constexpr into_variant_t into_variant{};
  inline constexpr stopped_as_optional_t stopped_as_optional{};
  inline constexpr stopped_as_error_t stopped_as_error{};
  inline constexpr associate_t associate{};
  inline constexpr spawn_future_t spawn_future{};
}

namespace std::this_thread {
  // [exec.consumers], consumers
  struct sync_wait_t { unspecified };
  struct sync_wait_with_variant_t { unspecified };

  inline constexpr sync_wait_t sync_wait{};
  inline constexpr sync_wait_with_variant_t sync_wait_with_variant{};
}

namespace std::execution {
  // [exec.consumers], consumers
  struct spawn_t { unspecified };
  inline constexpr spawn_t spawn{};

  // [exec.cmplsig], completion signatures
  template<class Fn>
    concept exposition onlyconceptnc{completion-signature} = see belownc;                   // exposition only

  template<completion-signature... Fns>
    struct completion_signatures;

  template<class Sigs>
    concept exposition onlyconceptnc{valid-completion-signatures} = see belownc;            // exposition only

  struct dependent_sender_error : exception {};

  // [exec.prop], class template prop
  template<class QueryTag, class ValueType>
    struct prop;

  // [exec.env], class template env
  template<queryable... Envs>
    struct env;

  // [exec.run.loop], run_loop
  class run_loop;

  // [exec.as.awaitable], coroutine utility as_awaitable
  struct as_awaitable_t { unspecified };
  inline constexpr as_awaitable_t as_awaitable{};

  // [exec.with.awaitable.senders], coroutine utility with_awaitable_senders
  template<class-type Promise>
    struct with_awaitable_senders;

  // [exec.affine.on], coroutine utility affine_on
  struct affine_on_t { unspecified };
  inline constexpr affine_on_t affine_on{};

  // [exec.inline.scheduler], inline scheduler
  class inline_scheduler;

  // [exec.task.scheduler], task scheduler
  class task_scheduler;

  template<class E>
  struct with_error {
    using type = remove_cvref_t<E>;
    type error;
  };
  template<class E>
    with_error(E) -> with_error<E>;

  template<scheduler Sch>
  struct change_coroutine_scheduler {
    using type = remove_cvref_t<Sch>;
    type scheduler;
  };
  template<scheduler Sch>
    change_coroutine_scheduler(Sch) -> change_coroutine_scheduler<Sch>;

  // [exec.task], class template task
  template<class T, class Environment>
    class task;

  // [exec.scope.concepts], scope concepts
  template<class Token>
    concept scope_token = see below;

  // [exec.scope.simple.counting], simple counting scope
  class simple_counting_scope;

  // [exec.scope.counting], counting scope
  class counting_scope;

  // [exec.par.scheduler], parallel scheduler
  class parallel_scheduler;
  parallel_scheduler get_parallel_scheduler();

  // [exec.sysctxrepl], namespace system_context_replaceability
  namespace system_context_replaceability@ {
    struct receiver_proxy;
    struct bulk_item_receiver_proxy;
    struct parallel_scheduler_backend;

    shared_ptr<parallel_scheduler_backend> query_parallel_scheduler_backend();
  }
}
```

The exposition-only type `variant-or-empty<Ts...>` is defined as
follows:

- If `sizeof...(Ts)` is greater than zero, `variant-or-empty<Ts...>`
  denotes `variant<Us...>` where `Us...` is the pack `decay_t<Ts>...`
  with duplicate types removed.
- Otherwise, `variant-or-empty<Ts...>` denotes the exposition-only class
  type:
  ``` cpp
  namespace std::execution {
    struct empty-variant {        // exposition only
      empty-variant() = delete;
    };
  }
  ```

For type `Sndr` and pack of types `Env`, let `CS` be
`completion_signatures_of_t<Sndr, Env...>`. Then
`single-sender-value-type<Sndr, Env...>` is ill-formed if `CS` is
ill-formed or if `sizeof...(Env) > 1` is `true`; otherwise, it is an
alias for:

- `gather-signatures<set_value_t, CS, decay_t, type_identity_t>` if that
  type is well-formed,
- Otherwise, `void` if
  `gather-signatures<set_value_t, CS, tuple, variant>` is
  `variant<tuple<>>` or `variant<>`,
- Otherwise,
  `gather-signatures<set_value_t, CS, decayed-tuple, type_identity_t>`
  if that type is well-formed,
- Otherwise, `single-sender-value-type<Sndr, Env...>` is ill-formed.

The exposition-only concept `single-sender` is defined as follows:

``` cpp
namespace std::execution {
  template<class Sndr, class... Env>
    concept single-sender = sender_in<Sndr, Env...> &&
      requires {
        typename single-sender-value-type<Sndr, Env...>;
      };
}
```

A type satisfies and models the exposition-only concept
*valid-completion-signatures* if it is a specialization of the
`completion_signatures` class template.

## Queries <a id="exec.queries">[[exec.queries]]</a>

### `forwarding_query` <a id="exec.fwd.env">[[exec.fwd.env]]</a>

`forwarding_query` asks a query object whether it should be forwarded
through queryable adaptors.

The name `forwarding_query` denotes a query object. For some query
object `q` of type `Q`, `forwarding_query(q)` is expression-equivalent
to:

- `MANDATE-NOTHROW(q.query(forwarding_query))` if that expression is
  well-formed. *Mandates:* The expression above has type `bool` and is a
  core constant expression if `q` is a core constant expression.
- Otherwise, `true` if `derived_from<Q, forwarding_query_t>` is `true`.
- Otherwise, `false`.

### `get_allocator` <a id="exec.get.allocator">[[exec.get.allocator]]</a>

`get_allocator` asks a queryable object for its associated allocator.

The name `get_allocator` denotes a query object. For a subexpression
`env`, `get_allocator(env)` is expression-equivalent to
`MANDATE-NOTHROW(AS-CONST(env).query(get_allocator))`.

*Mandates:* If the expression above is well-formed, its type satisfies
`simple-allocator` [[allocator.requirements.general]].

`forwarding_query(get_allocator)` is a core constant expression and has
value `true`.

### `get_stop_token` <a id="exec.get.stop.token">[[exec.get.stop.token]]</a>

`get_stop_token` asks a queryable object for an associated stop token.

The name `get_stop_token` denotes a query object. For a subexpression
`env`, `get_stop_token(env)` is expression-equivalent to:

- `MANDATE-NOTHROW(AS-CONST(env).query(get_stop_token))` if that
  expression is well-formed. *Mandates:* The type of the expression
  above satisfies `stoppable_token`.
- Otherwise, `never_stop_token{}`.

`forwarding_query(get_stop_token)` is a core constant expression and has
value `true`.

### `execution::get_env` <a id="exec.get.env">[[exec.get.env]]</a>

`execution::get_env` is a customization point object. For a
subexpression `o`, `execution::get_env(o)` is expression-equivalent to:

- `MANDATE-NOTHROW(AS-CONST(o).get_env())` if that expression is
  well-formed. *Mandates:* The type of the expression above satisfies
  `queryable` [[exec.queryable]].
- Otherwise, `env<>{}`.

The value of `get_env(o)` shall be valid while `o` is valid.

[*Note 1*: When passed a sender object, `get_env` returns the sender’s
associated attributes. When passed a receiver, `get_env` returns the
receiver’s associated execution environment. — *end note*]

### `execution::get_domain` <a id="exec.get.domain">[[exec.get.domain]]</a>

`get_domain` asks a queryable object for its associated execution domain
tag.

The name `get_domain` denotes a query object. For a subexpression `env`,
`get_domain(env)` is expression-equivalent to
`MANDATE-NOTHROW(AS-CONST(env).query(get_domain))`.

`forwarding_query(execution::get_domain)` is a core constant expression
and has value `true`.

### `execution::get_scheduler` <a id="exec.get.scheduler">[[exec.get.scheduler]]</a>

`get_scheduler` asks a queryable object for its associated scheduler.

The name `get_scheduler` denotes a query object. For a subexpression
`env`, `get_scheduler(env)` is expression-equivalent to
`MANDATE-NOTHROW(AS-CONST(env).query(get_scheduler))`.

*Mandates:* If the expression above is well-formed, its type satisfies
`scheduler`.

`forwarding_query(execution::get_scheduler)` is a core constant
expression and has value `true`.

### `execution::get_delegation_scheduler` <a id="exec.get.delegation.scheduler">[[exec.get.delegation.scheduler]]</a>

`get_delegation_scheduler` asks a queryable object for a scheduler that
can be used to delegate work to for the purpose of forward progress
delegation [[intro.progress]].

The name `get_delegation_scheduler` denotes a query object. For a
subexpression `env`, `get_delegation_scheduler(env)` is
expression-equivalent to
`MANDATE-NOTHROW(AS-CONST(env).query(get_delegation_scheduler))`.

*Mandates:* If the expression above is well-formed, its type satisfies
`scheduler`.

`forwarding_query(execution::get_delegation_scheduler)` is a core
constant expression and has value `true`.

### `execution::get_forward_progress_guarantee` <a id="exec.get.fwd.progress">[[exec.get.fwd.progress]]</a>

``` cpp
namespace std::execution {
  enum class forward_progress_guarantee {
    concurrent,
    parallel,
    weakly_parallel
  };
}
```

`get_forward_progress_guarantee` asks a scheduler about the forward
progress guarantee of execution agents created by that scheduler’s
associated execution resource [[intro.progress]].

The name `get_forward_progress_guarantee` denotes a query object. For a
subexpression `sch`, let `Sch` be `decltype((sch))`. If `Sch` does not
satisfy `scheduler`, `get_forward_progress_guarantee` is ill-formed.
Otherwise, `get_forward_progress_guarantee(sch)` is
expression-equivalent to:

- `MANDATE-NOTHROW(AS-CONST(sch).query(get_forward_progress_guarantee))`,
  if that expression is well-formed. *Mandates:* The type of the
  expression above is `forward_progress_guarantee`.
- Otherwise, `forward_progress_guarantee::weakly_parallel`.

If `get_forward_progress_guarantee(sch)` for some scheduler `sch`
returns `forward_progress_guarantee::concurrent`, all execution agents
created by that scheduler’s associated execution resource shall provide
the concurrent forward progress guarantee. If it returns
`forward_progress_guarantee::parallel`, all such execution agents shall
provide at least the parallel forward progress guarantee.

### `execution::get_completion_scheduler` <a id="exec.get.compl.sched">[[exec.get.compl.sched]]</a>

`get_completion_scheduler<completion-tag>` obtains the completion
scheduler associated with a completion tag from a sender’s attributes.

The name `get_completion_scheduler` denotes a query object template. For
a subexpression `q`, the expression
`get_completion_scheduler<completion-tag>(q)` is ill-formed if
*`completion-tag`* is not one of `set_value_t`, `set_error_t`, or
`set_stopped_t`. Otherwise,
`get_completion_scheduler<completion-tag>(q)` is expression-equivalent
to

``` cpp
MANDATE-NOTHROW(AS-CONST(q).query(get_completion_scheduler<completion-tag>))
```

*Mandates:* If the expression above is well-formed, its type satisfies
`scheduler`.

Let *`completion-fn`* be a completion function [[exec.async.ops]]; let
*`completion-tag`* be the associated completion tag of
*`completion-fn`*; let `args` be a pack of subexpressions; and let
`sndr` be a subexpression such that `sender<decltype((sndr))>` is `true`
and `get_completion_scheduler<completion-tag>(get_env(sndr))` is
well-formed and denotes a scheduler `sch`. If an asynchronous operation
created by connecting `sndr` with a receiver `rcvr` causes the
evaluation of `completion-fn(rcvr, args...)`, the behavior is undefined
unless the evaluation happens on an execution agent that belongs to
`sch`’s associated execution resource.

The expression
`forwarding_query(get_completion_scheduler<completion-tag>)` is a core
constant expression and has value `true`.

### `execution::get_await_completion_adaptor` <a id="exec.get.await.adapt">[[exec.get.await.adapt]]</a>

`get_await_completion_adaptor` asks a queryable object for its
associated awaitable completion adaptor.

The name `get_await_completion_adaptor` denotes a query object. For a
subexpression `env`,

``` cpp
get_await_completion_adaptor(env)
```

is expression-equivalent to

``` cpp
MANDATE-NOTHROW(AS-CONST(env).query(get_await_completion_adaptor))
```

`forwarding_query(execution::get_await_completion_adaptor)`

is a core constant expression and has value `true`.

## Schedulers <a id="exec.sched">[[exec.sched]]</a>

The `scheduler` concept defines the requirements of a scheduler type
[[exec.async.ops]]. `schedule` is a customization point object that
accepts a scheduler. A valid invocation of `schedule` is a
schedule-expression.

``` cpp
namespace std::execution {
  template<class Sch>
    concept scheduler =
      derived_from<typename remove_cvref_t<Sch>::scheduler_concept, scheduler_t> &&
      queryable<Sch> &&
      requires(Sch&& sch) {
        { schedule(std::forward<Sch>(sch)) } -> sender;
        { auto(get_completion_scheduler<set_value_t>(
            get_env(schedule(std::forward<Sch>(sch))))) }
              -> same_as<remove_cvref_t<Sch>>;
      } &&
      equality_comparable<remove_cvref_t<Sch>> &&
      copyable<remove_cvref_t<Sch>>;
}
```

Let `Sch` be the type of a scheduler and let `Env` be the type of an
execution environment for which `sender_in<schedule_result_t<Sch>, Env>`
is satisfied. Then `sender-in-of<schedule_result_t<Sch>, Env>` shall be
modeled.

No operation required by `copyable<remove_cvref_t<Sch>>` and
`equality_comparable<remove_cvref_t<Sch>>` shall exit via an exception.
None of these operations, nor a scheduler type’s `schedule` function,
shall introduce data races as a result of potentially concurrent
[[intro.races]] invocations of those operations from different threads.

For any two values `sch1` and `sch2` of some scheduler type `Sch`,
`sch1 == sch2` shall return `true` only if both `sch1` and `sch2` share
the same associated execution resource.

For a given scheduler expression `sch`, the expression
`get_completion_scheduler<set_value_t>(get_env(schedule(sch)))` shall
compare equal to `sch`.

For a given scheduler expression `sch`, if the expression
`get_domain(sch)` is well-formed, then the expression
`get_domain(get_env(schedule(sch)))` is also well-formed and has the
same type.

A scheduler type’s destructor shall not block pending completion of any
receivers connected to the sender objects returned from `schedule`.

[*Note 1*: The ability to wait for completion of submitted function
objects can be provided by the associated execution resource of the
scheduler. — *end note*]

## Receivers <a id="exec.recv">[[exec.recv]]</a>

### Receiver concepts <a id="exec.recv.concepts">[[exec.recv.concepts]]</a>

A receiver represents the continuation of an asynchronous operation. The
`receiver` concept defines the requirements for a receiver type
[[exec.async.ops]]. The `receiver_of` concept defines the requirements
for a receiver type that is usable as the first argument of a set of
completion operations corresponding to a set of completion signatures.
The `get_env` customization point object is used to access a receiver’s
associated environment.

``` cpp
namespace std::execution {
  template<class Rcvr>
    concept receiver =
      derived_from<typename remove_cvref_t<Rcvr>::receiver_concept, receiver_t> &&
      requires(const remove_cvref_t<Rcvr>& rcvr) {
        { get_env(rcvr) } -> queryable;
      } &&
      move_constructible<remove_cvref_t<Rcvr>> &&       // rvalues are movable, and
      constructible_from<remove_cvref_t<Rcvr>, Rcvr>;   // lvalues are copyable

  template<class Signature, class Rcvr>
    concept valid-completion-for =                 // exposition only
      requires (Signature* sig) {
        []<class Tag, class... Args>(Tag(*)(Args...))
            requires callable<Tag, remove_cvref_t<Rcvr>, Args...>
        {}(sig);
      };

  template<class Rcvr, class Completions>
    concept has-completions =                      // exposition only
      requires (Completions* completions) {
        []<valid-completion-for<Rcvr>...Sigs>(completion_signatures<Sigs...>*)
        {}(completions);
      };

  template<class Rcvr, class Completions>
    concept receiver_of =
      receiver<Rcvr> && has-completions<Rcvr, Completions>;
}
```

Class types that are marked `final` do not model the `receiver` concept.

Let `rcvr` be a receiver and let `op_state` be an operation state
associated with an asynchronous operation created by connecting `rcvr`
with a sender. Let `token` be a stop token equal to
`get_stop_token(get_env(rcvr))`. `token` shall remain valid for the
duration of the asynchronous operation’s lifetime [[exec.async.ops]].

[*Note 1*: This means that, unless it knows about further guarantees
provided by the type of `rcvr`, the implementation of `op_state` cannot
use `token` after it executes a completion operation. This also implies
that any stop callbacks registered on token must be destroyed before the
invocation of the completion operation. — *end note*]

### `execution::set_value` <a id="exec.set.value">[[exec.set.value]]</a>

`set_value` is a value completion function [[exec.async.ops]]. Its
associated completion tag is `set_value_t`. The expression
`set_value(rcvr, vs...)` for a subexpression `rcvr` and pack of
subexpressions `vs` is ill-formed if `rcvr` is an lvalue or an rvalue of
const type. Otherwise, it is expression-equivalent to
`MANDATE-NOTHROW(rcvr.set_value(vs...))`.

### `execution::set_error` <a id="exec.set.error">[[exec.set.error]]</a>

`set_error` is an error completion function [[exec.async.ops]]. Its
associated completion tag is `set_error_t`. The expression
`set_error(rcvr, err)` for some subexpressions `rcvr` and `err` is
ill-formed if `rcvr` is an lvalue or an rvalue of const type. Otherwise,
it is expression-equivalent to `MANDATE-NOTHROW(rcvr.set_error(err))`.

### `execution::set_stopped` <a id="exec.set.stopped">[[exec.set.stopped]]</a>

`set_stopped` is a stopped completion function [[exec.async.ops]]. Its
associated completion tag is `set_stopped_t`. The expression
`set_stopped(rcvr)` for a subexpression `rcvr` is ill-formed if `rcvr`
is an lvalue or an rvalue of const type. Otherwise, it is
expression-equivalent to `MANDATE-NOTHROW(rcvr.set_stopped())`.

## Operation states <a id="exec.opstate">[[exec.opstate]]</a>

### General <a id="exec.opstate.general">[[exec.opstate.general]]</a>

The `operation_state` concept defines the requirements of an operation
state type [[exec.async.ops]].

``` cpp
namespace std::execution {
  template<class O>
    concept operation_state =
      derived_from<typename O::operation_state_concept, operation_state_t> &&
      requires (O& o) {
        start(o);
      };
}
```

If an `operation_state` object is destroyed during the lifetime of its
asynchronous operation [[exec.async.ops]], the behavior is undefined.

[*Note 1*: The `operation_state` concept does not impose requirements
on any operations other than destruction and `start`, including copy and
move operations. Invoking any such operation on an object whose type
models `operation_state` can lead to undefined behavior. — *end note*]

The program is ill-formed if it performs a copy or move construction or
assignment operation on an operation state object created by connecting
a library-provided sender.

### `execution::start` <a id="exec.opstate.start">[[exec.opstate.start]]</a>

The name `start` denotes a customization point object that starts
[[exec.async.ops]] the asynchronous operation associated with the
operation state object. For a subexpression `op`, the expression
`start(op)` is ill-formed if `op` is an rvalue. Otherwise, it is
expression-equivalent to `MANDATE-NOTHROW(op.start())`.

If `op.start()` does not start [[exec.async.ops]] the asynchronous
operation associated with the operation state `op`, the behavior of
calling `start(op)` is undefined.

## Senders <a id="exec.snd">[[exec.snd]]</a>

### General <a id="exec.snd.general">[[exec.snd.general]]</a>

Subclauses [[exec.factories]] and [[exec.adapt]] define customizable
algorithms that return senders. Each algorithm has a default
implementation. Let `sndr` be the result of an invocation of such an
algorithm or an object equal to the result [[concepts.equality]], and
let `Sndr` be `decltype((sndr))`. Let `rcvr` be a receiver of type
`Rcvr` with associated environment `env` of type `Env` such that
`sender_to<Sndr, Rcvr>` is `true`. For the default implementation of the
algorithm that produced `sndr`, connecting `sndr` to `rcvr` and starting
the resulting operation state [[exec.async.ops]] necessarily results in
the potential evaluation [[basic.def.odr]] of a set of completion
operations whose first argument is a subexpression equal to `rcvr`. Let
`Sigs` be a pack of completion signatures corresponding to this set of
completion operations, and let `CS` be the type of the expression
`get_completion_signatures<Sndr, Env>()`. Then `CS` is a specialization
of the class template `completion_signatures` [[exec.cmplsig]], the set
of whose template arguments is `Sigs`. If none of the types in `Sigs`
are dependent on the type `Env`, then the expression
`get_completion_signatures<Sndr>()` is well-formed and its type is `CS`.
If a user-provided implementation of the algorithm that produced `sndr`
is selected instead of the default:

- Any completion signature that is in the set of types denoted by
  `completion_signatures_of_t<Sndr, Env>` and that is not part of `Sigs`
  shall correspond to error or stopped completion operations, unless
  otherwise specified.
- If none of the types in `Sigs` are dependent on the type `Env`, then
  `completion_signatures_of_t<Sndr>` and
  `completion_signatures_of_t<Sndr, Env>` shall denote the same type.

### Exposition-only entities <a id="exec.snd.expos">[[exec.snd.expos]]</a>

Subclause [[exec.snd]] makes use of the following exposition-only
entities.

For a queryable object `env`, `FWD-ENV(env)` is an expression whose type
satisfies `queryable` such that for a query object `q` and a pack of
subexpressions `as`, the expression `FWD-ENV(env).query(q, as...)` is
ill-formed if `forwarding_query(q)` is `false`; otherwise, it is
expression-equivalent to `env.query(q, as...)`. The type
`FWD-ENV-T(Env)` is `decltype(FWD-ENV(declval<Env>()))`.

For a query object `q` and a subexpression `v`, `MAKE-ENV(q, v)` is an
expression `env` whose type satisfies `queryable` such that the result
of `env.query(q)` has a value equal to `v` [[concepts.equality]]. Unless
otherwise stated, the object to which `env.query(q)` refers remains
valid while `env` remains valid.

For two queryable objects `env1` and `env2`, a query object `q`, and a
pack of subexpressions `as`, `JOIN-ENV(env1, env2)` is an expression
`env3` whose type satisfies `queryable` such that `env3.query(q, as...)`
is expression-equivalent to:

- `env1.query(q, as...)` if that expression is well-formed,
- otherwise, `env2.query(q, as...)` if that expression is well-formed,
- otherwise, `env3.query(q, as...)` is ill-formed.

The results of *`FWD-ENV`*, *`MAKE-ENV`*, and *`JOIN-ENV`* can be
context-dependent; i.e., they can evaluate to expressions with different
types and value categories in different contexts for the same arguments.

For a scheduler `sch`, `SCHED-ATTRS(sch)` is an expression `o1` whose
type satisfies `queryable` such that
`o1.query(get_completion_scheduler<Tag>)` is an expression with the same
type and value as `sch` where `Tag` is one of `set_value_t` or
`set_stopped_t`, and such that `o1.query(get_domain)` is
expression-equivalent to `sch.query(get_domain)`. `SCHED-ENV(sch)` is an
expression `o2` whose type satisfies `queryable` such that
`o2.query(get_scheduler)` is a prvalue with the same type and value as
`sch`, and such that `o2.query(get_domain)` is expression-equivalent to
`sch.query(get_domain)`.

For two subexpressions `rcvr` and `expr`, `SET-VALUE(rcvr, expr)` is
expression-equivalent to `(expr, set_value(std::move(rcvr)))` if the
type of `expr` is `void`; otherwise, `set_value(std::move(rcvr), expr)`.
`TRY-EVAL(rcvr, expr)` is equivalent to:

``` cpp
try {
  expr;
} catch(...) {
  set_error(std::move(rcvr), current_exception());
}
```

if `expr` is potentially-throwing; otherwise, `expr`.
`TRY-SET-VALUE(rcvr, expr)` is

``` cpp
TRY-EVAL(rcvr, SET-VALUE(rcvr, expr))
```

except that `rcvr` is evaluated only once.

``` cpp
template<class Default = default_domain, class Sndr>
  constexpr auto completion-domain(const Sndr& sndr) noexcept;
```

*`COMPL-DOMAIN`*`(T)` is the type of the expression
`get_domain(get_completion_scheduler<T>(get_env(sndr)))`.

*Effects:* If all of the types *`COMPL-DOMAIN`*`(set_value_t)`,
*`COMPL-DOMAIN`*`(set_error_t)`, and *`COMPL-DOMAIN`*`(set_stopped_t)`
are ill-formed, `completion-domain<Default>(sndr)` is a
default-constructed prvalue of type `Default`. Otherwise, if they all
share a common type [[meta.trans.other]] (ignoring those types that are
ill-formed), then *`completion-domain`*`<Default>(sndr)` is a
default-constructed prvalue of that type. Otherwise,
*`completion-domain`*`<Default>(sndr)` is ill-formed.

``` cpp
template<class Tag, class Env, class Default>
  constexpr decltype(auto) query-with-default(
    Tag, const Env& env, Default&& value) noexcept(see below);
```

Let `e` be the expression `Tag()(env)` if that expression is
well-formed; otherwise, it is
`static_cast<Default>(std::forward<Default>(value))`.

*Returns:* `e`.

*Remarks:* The expression in the noexcept clause is `noexcept(e)`.

``` cpp
template<class Sndr>
  constexpr auto get-domain-early(const Sndr& sndr) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return Domain();
```

where `Domain` is the decayed type of the first of the following
expressions that is well-formed:

- `get_domain(get_env(sndr))`
- *`completion-domain`*`(sndr)`
- `default_domain()`

``` cpp
template<class Sndr, class Env>
  constexpr auto get-domain-late(const Sndr& sndr, const Env& env) noexcept;
```

*Effects:* Equivalent to:

- If `sender-for<Sndr, continues_on_t>` is `true`, then
  ``` cpp
  return Domain();
  ```

  where `Domain` is the type of the following expression:
  ``` cpp
  [] {
    auto [_, sch, _] = sndr;
    return query-with-default(get_domain, sch, default_domain());
  }();
  ```

  \[*Note 1*: The `continues_on` algorithm works in tandem with
  `schedule_from`@@REF:exec.schedule.from@@ to give scheduler authors a
  way to customize both how to transition onto (`continues_on`) and off
  of (`schedule_from`) a given execution context. Thus, `continues_on`
  ignores the domain of the predecessor and uses the domain of the
  destination scheduler to select a customization, a property that is
  unique to `continues_on`. That is why it is given special treatment
  here. — *end note*]
- Otherwise,
  ``` cpp
  return Domain();
  ```

  where `Domain` is the first of the following expressions that is
  well-formed and whose type is not `void`:
  - `get_domain(get_env(sndr))`
  - *`completion-domain`*`<void>(sndr)`
  - `get_domain(env)`
  - `get_domain(get_scheduler(env))`
  - `default_domain()`

``` cpp
template<callable Fun>
  requires is_nothrow_move_constructible_v<Fun>
struct emplace-from {
  Fun fun;                                                      // exposition only
  using type = call-result-t<Fun>;

  constexpr operator type() && noexcept(nothrow-callable<Fun>) {
    return std::move(fun)();
  }

  constexpr type operator()() && noexcept(nothrow-callable<Fun>) {
    return std::move(fun)();
  }
};
```

[*Note 1*: *`emplace-from`* is used to emplace non-movable types into
`tuple`, `optional`, `variant`, and similar types. — *end note*]

``` cpp
struct on-stop-request {
  inplace_stop_source& stop-src;       // exposition only
  void operator()() noexcept { stop-src.request_stop(); }
};
```

``` cpp
template<class T_0, class T_1, …, class T_n>
struct product-type {       // exposition only
  T_0 t_0;                // exposition only
  T_1 t_1;                // exposition only
    ⋮
  T_n t_n;                // exposition only

  template<size_t I, class Self>
  constexpr decltype(auto) get(this Self&& self) noexcept;      // exposition only

  template<class Self, class Fn>
  constexpr decltype(auto) apply(this Self&& self, Fn&& fn)     // exposition only
    noexcept(see below);
};
```

[*Note 2*: *`product-type`* is presented here in pseudo-code form for
the sake of exposition. It can be approximated in standard C++ with a
tuple-like implementation that takes care to keep the type an aggregate
that can be used as the initializer of a structured binding
declaration. — *end note*]

[*Note 3*: An expression of type *`product-type`* is usable as the
initializer of a structured binding declaration
[[dcl.struct.bind]]. — *end note*]

``` cpp
template<size_t I, class Self>
constexpr decltype(auto) get(this Self&& self) noexcept;
```

*Effects:* Equivalent to:

``` cpp
auto& [...ts] = self;
return std::forward_like<Self>(ts...[I]);
```

``` cpp
template<class Self, class Fn>
constexpr decltype(auto) apply(this Self&& self, Fn&& fn) noexcept(see below);
```

*Constraints:* The expression in the `return` statement below is
well-formed.

*Effects:* Equivalent to:

``` cpp
auto& [...ts] = self;
return std::forward<Fn>(fn)(std::forward_like<Self>(ts)...);
```

*Remarks:* The expression in the `noexcept` clause is `true` if the
`return` statement above is not potentially throwing; otherwise,
`false`.

Let `valid-specialization` be the following concept:

``` cpp
namespace std::execution {
  template<template<class...> class T, class... Args>
  concept valid-specialization =                                // exposition only
    requires { typename T<Args...>; };
}
```

``` cpp
template<class Tag, class Data = see below, class... Child>
  constexpr auto make-sender(Tag tag, Data&& data, Child&&... child);
```

*Mandates:* The following expressions are `true`:

- `semiregular<Tag>`
- `movable-value<Data>`
- `(sender<Child> && ...)`
- `dependent_sender<Sndr> || sender_in<Sndr>`, where `Sndr` is
  *`basic-sender`*`<Tag, Data,Child...>` as defined below. *Recommended
  practice:* If evaluation of `sender_in<Sndr>` results in an uncaught
  exception from the evaluation of `get_completion_signatures<Sndr>()`,
  the implementation should include information about that exception in
  the resulting diagnostic.

*Returns:* A prvalue of type
*`basic-sender`*`<Tag, decay_t<Data>, decay_t<Child>...>` that has been
direct-list-initialized with the forwarded arguments, where
*basic-sender* is the following exposition-only class template except as
noted below.

*Remarks:* The default template argument for the `Data` template
parameter denotes an unspecified empty trivially copyable class type
that models `semiregular`.

``` cpp
namespace std::execution {
  template<class Tag>
  concept completion-tag =                                      // exposition only
    same_as<Tag, set_value_t> || same_as<Tag, set_error_t> || same_as<Tag, set_stopped_t>;

  struct default-impls {                                        // exposition only
    static constexpr auto get-attrs = see belownc;                // exposition only
    static constexpr auto get-env = see belownc;                  // exposition only
    static constexpr auto get-state = see belownc;                // exposition only
    static constexpr auto start = see belownc;                    // exposition only
    static constexpr auto complete = see belownc;                 // exposition only

    template<class Sndr, class... Env>
      static consteval void check-types();                      // exposition only
  };

  template<class Tag>
  struct impls-for : default-impls {};                          // exposition only

  template<class Sndr, class Rcvr>                              // exposition only
  using state-type = decay_t<call-result-t<
    decltype(impls-for<tag_of_t<Sndr>>::get-state), Sndr, Rcvr&>>;

  template<class Index, class Sndr, class Rcvr>                 // exposition only
  using env-type = call-result-t<
    decltype(impls-for<tag_of_t<Sndr>>::get-env), Index,
    state-type<Sndr, Rcvr>&, const Rcvr&>;

  template<class Sndr>
  using data-type = decltype(declval<Sndr>().template get<1>());                // exposition only

  template<class Sndr, size_t I = 0>
  using child-type = decltype(declval<Sndr>().template get<I+2>());             // exposition only

  template<class Sndr>
  using indices-for = remove_reference_t<Sndr>::indices-for;                    // exposition only

  template<class Sndr, class Rcvr>
  struct basic-state {                                          // exposition only
    basic-state(Sndr&& sndr, Rcvr&& rcvr) noexcept(see below)
      : rcvr(std::move(rcvr))
      , state(impls-for<tag_of_t<Sndr>>::get-state(std::forward<Sndr>(sndr), rcvr)) { }

    Rcvr rcvr;                                                  // exposition only
    state-type<Sndr, Rcvr> state;                               // exposition only
  };

  template<class Sndr, class Rcvr, class Index>
    requires valid-specialization<env-type, Index, Sndr, Rcvr>
  struct basic-receiver {                                       // exposition only
    using receiver_concept = receiver_t;

    using tag-t = tag_of_t<Sndr>;                               // exposition only
    using state-t = state-type<Sndr, Rcvr>;                     // exposition only
    static constexpr const auto& complete = impls-for<tag-t>::complete;         // exposition only

    template<class... Args>
      requires callable<decltype(complete), Index, state-t&, Rcvr&, set_value_t, Args...>
    void set_value(Args&&... args) && noexcept {
      complete(Index(), op->state, op->rcvr, set_value_t(), std::forward<Args>(args)...);
    }

    template<class Error>
      requires callable<decltype(complete), Index, state-t&, Rcvr&, set_error_t, Error>
    void set_error(Error&& err) && noexcept {
      complete(Index(), op->state, op->rcvr, set_error_t(), std::forward<Error>(err));
    }

    void set_stopped() && noexcept
      requires callable<decltype(complete), Index, state-t&, Rcvr&, set_stopped_t> {
      complete(Index(), op->state, op->rcvr, set_stopped_t());
    }

    auto get_env() const noexcept -> env-type<Index, Sndr, Rcvr> {
      return impls-for<tag-t>::get-env(Index(), op->state, op->rcvr);
    }

    basic-state<Sndr, Rcvr>* op;                                // exposition only
  };

  constexpr auto connect-all = see belownc;                       // exposition only

  template<class Sndr, class Rcvr>
  using connect-all-result = call-result-t<                     // exposition only
    decltype(connect-all), basic-state<Sndr, Rcvr>*, Sndr, indices-for<Sndr>>;

  template<class Sndr, class Rcvr>
    requires valid-specialization<state-type, Sndr, Rcvr> &&
             valid-specialization<connect-all-result, Sndr, Rcvr>
  struct basic-operation : basic-state<Sndr, Rcvr> {            // exposition only
    using operation_state_concept = operation_state_t;
    using tag-t = tag_of_t<Sndr>;                               // exposition only

    connect-all-result<Sndr, Rcvr> inner-ops;                   // exposition only

    basic-operation(Sndr&& sndr, Rcvr&& rcvr) noexcept(see belownc)               // exposition only
      : basic-state<Sndr, Rcvr>(std::forward<Sndr>(sndr), std::move(rcvr)),
        inner-ops(connect-all(this, std::forward<Sndr>(sndr), indices-for<Sndr>()))
    {}

    void start() & noexcept {
      auto& [...ops] = inner-ops;
      impls-for<tag-t>::start(this->state, this->rcvr, ops...);
    }
  };

  template<class Tag, class Data, class... Child>
  struct basic-sender : product-type<Tag, Data, Child...> {     // exposition only
    using sender_concept = sender_t;
    using indices-for = index_sequence_for<Child...>;           // exposition only

    decltype(auto) get_env() const noexcept {
      auto& [_, data, ...child] = *this;
      return impls-for<Tag>::get-attrs(data, child...);
    }

    template<decays-to<basic-sender> Self, receiver Rcvr>
    auto connect(this Self&& self, Rcvr rcvr) noexcept(see below)
      -> basic-operation<Self, Rcvr> {
      return {std::forward<Self>(self), std::move(rcvr)};
    }

    template<decays-to<basic-sender> Self, class... Env>
    static constexpr auto get_completion_signatures();
  };
}
```

It is unspecified whether a specialization of *`basic-sender`* is an
aggregate.

An expression of type *`basic-sender`* is usable as the initializer of a
structured binding declaration [[dcl.struct.bind]].

The expression in the `noexcept` clause of the constructor of
*`basic-state`* is

``` cpp
is_nothrow_move_constructible_v<Rcvr> &&
nothrow-callable<decltype(impls-for<tag_of_t<Sndr>>::get-state), Sndr, Rcvr&> &&
(same_as<state-type<Sndr, Rcvr>, get-state-result> ||
 is_nothrow_constructible_v<state-type<Sndr, Rcvr>, get-state-result>)
```

where *`get-state-result`* is

``` cpp
call-result-t<decltype(impls-for<tag_of_t<Sndr>>::get-state), Sndr, Rcvr&>.
```

The object *`connect-all`* is initialized with a callable object
equivalent to the following lambda:

``` cpp
[]<class Sndr, class Rcvr, size_t... Is>(
  basic-state<Sndr, Rcvr>* op, Sndr&& sndr, index_sequence<Is...>) noexcept(see below)
    -> decltype(auto) {
    auto& [_, data, ...child] = sndr;
    return product-type{connect(
      std::forward_like<Sndr>(child),
      basic-receiver<Sndr, Rcvr, integral_constant<size_t, Is>>{op})...};
  }
```

*Constraints:* The expression in the `return` statement is well-formed.

*Remarks:* The expression in the `noexcept` clause is `true` if the
`return` statement is not potentially throwing; otherwise, `false`.

The expression in the `noexcept` clause of the constructor of
*`basic-operation`* is:

``` cpp
is_nothrow_constructible_v<basic-state<Self, Rcvr>, Self, Rcvr> &&
noexcept(connect-all(this, std::forward<Sndr>(sndr), indices-for<Sndr>()))
```

The expression in the `noexcept` clause of the `connect` member function
of *`basic-sender`* is:

``` cpp
is_nothrow_constructible_v<basic-operation<Self, Rcvr>, Self, Rcvr>
```

The member `default-impls::get-attrs` is initialized with a callable
object equivalent to the following lambda:

``` cpp
[](const auto&, const auto&... child) noexcept -> decltype(auto) {
  if constexpr (sizeof...(child) == 1)
    return (FWD-ENV(get_env(child)), ...);
  else
    return env<>();
}
```

The member `default-impls::get-env` is initialized with a callable
object equivalent to the following lambda:

``` cpp
[](auto, auto&, const auto& rcvr) noexcept -> decltype(auto) {
  return FWD-ENV(get_env(rcvr));
}
```

The member `default-impls::get-state` is initialized with a callable
object equivalent to the following lambda:

``` cpp
[]<class Sndr, class Rcvr>(Sndr&& sndr, Rcvr& rcvr) noexcept -> decltype(auto) {
  auto& [_, data, ...child] = sndr;
  return allocator-aware-forward(std::forward_like<Sndr>(data), rcvr);
}
```

The member `default-impls::start` is initialized with a callable object
equivalent to the following lambda:

``` cpp
[](auto&, auto&, auto&... ops) noexcept -> void {
  (execution::start(ops), ...);
}
```

The member `default-impls::complete` is initialized with a callable
object equivalent to the following lambda:

``` cpp
[]<class Index, class Rcvr, class Tag, class... Args>(
  Index, auto& state, Rcvr& rcvr, Tag, Args&&... args) noexcept
    -> void requires callable<Tag, Rcvr, Args...> {
  static_assert(Index::value == 0);
  Tag()(std::move(rcvr), std::forward<Args>(args)...);
}
```

``` cpp
template<class Sndr, class... Env>
  static consteval void default-impls::check-types();
```

Let `Is` be the pack of integral template arguments of the
`integer_sequence` specialization denoted by *`indices-for`*`<Sndr>`.

*Effects:* Equivalent to:

``` cpp
(get_completion_signatures<child-type<Sndr, Is>, FWD-ENV-T(Env)...>(), ...);
```

[*Note 1*:

For any types `T` and `S`, and pack `E`, let `e` be the expression
*`impls-for`*`<T>::`*`check-types`*`<S, E...>()`. Then exactly one of
the following is `true`:

- `e` is ill-formed, or
- the evaluation of `e` exits with an exception, or
- `e` is a core constant expression.

When `e` is a core constant expression, the pack `S, E...` uniquely
determines a set of completion signatures.

— *end note*]

``` cpp
template<class Tag, class Data, class... Child>
  template<class Sndr, class... Env>
    constexpr auto basic-sender<Tag, Data, Child...>::get_completion_signatures();
```

Let `Rcvr` be the type of a receiver whose environment has type `E`,
where `E` is the first type in the list `Env..., env<>`. Let
*`CHECK-TYPES`*`()` be the expression
*`impls-for`*`<Tag>::template `*`check-types`*`<Sndr, E>()`, and let
`CS` be a type determined as follows:

- If *`CHECK-TYPES`*`()` is a core constant expression, let `op` be an
  lvalue subexpression whose type is `connect_result_t<Sndr, Rcvr>`.
  Then `CS` is the specialization of `completion_signatures` the set of
  whose template arguments correspond to the set of completion
  operations that are potentially evaluated [[basic.def.odr]] as a
  result of evaluating `op.start()`.
- Otherwise, `CS` is `completion_signatures<>`.

*Constraints:* *`CHECK-TYPES`*`()` is a well-formed expression.

*Effects:* Equivalent to:

``` cpp
CHECK-TYPES();
return CS();
```

``` cpp
template<class... Fns>
struct overload-set : Fns... {
  using Fns::operator()...;
};
```

``` cpp
struct not-a-sender {
  using sender_concept = sender_t;

  template<class Sndr>
    static consteval auto get_completion_signatures() -> completion_signatures<> {
      throw unspecified-exception();
  }
};
```

where `unspecified-exception` is a type derived from `exception`.

``` cpp
constexpr void decay-copyable-result-datums(auto cs) {
  cs.for-each([]<class Tag, class... Ts>(Tag(*)(Ts...)) {
    if constexpr (!(is_constructible_v<decay_t<Ts>, Ts> &&...))
      throw unspecified-exception();
  });
}
```

where `unspecified-exception` is a type derived from `exception`.

``` cpp
template<class T, class Context>
  decltype(auto) allocator-aware-forward(T&& obj, Context&& context);       // exposition only
```

*allocator-aware-forward* is an exposition-only function template used
to either create a new object of type `remove_cvref_t<T>` from `obj` or
forward `obj` depending on whether an allocator is available. If the
environment associated with `context` provides an allocator (i.e., the
expression `get_allocator(get_env(context))` is valid), let *alloc* be
the result of this expression and let `P` be `remove_cvref_t<T>`.

*Returns:*

- If *alloc* is not defined, returns `std::forward<T>(obj)`,
- otherwise if `P` is a specialization of *product-type*, returns an
  object of type `P` whose elements are initialized using
  ``` cpp
  make_obj_using_allocator<decltype(e)>(std::forward_like<T>(e), alloc)
  ```

  where `e` is the corresponding element of `obj`,
- otherwise, returns
  `make_obj_using_allocator<P>(std::forward<T>(obj), `*`alloc`*`)`.

### Sender concepts <a id="exec.snd.concepts">[[exec.snd.concepts]]</a>

The `sender` concept defines the requirements for a sender type
[[exec.async.ops]]. The `sender_in` concept defines the requirements for
a sender type that can create asynchronous operations given an
associated environment type. The `sender_to` concept defines the
requirements for a sender type that can connect with a specific receiver
type. The `get_env` customization point object is used to access a
sender’s associated attributes. The connect customization point object
is used to connect [[exec.async.ops]] a sender and a receiver to produce
an operation state.

``` cpp
namespace std::execution {
  template<auto>
    concept is-constant = true;                                 // exposition only

  template<class Sndr>
    concept is-sender =                                         // exposition only
      derived_from<typename Sndr::sender_concept, sender_t>;

  template<class Sndr>
    concept enable-sender =                                     // exposition only
      is-sender<Sndr> ||
      is-awaitable<Sndr, env-promise<env<>>>;                 // [exec.awaitable]

  template<class Sndr>
    inline constexpr bool enable_sender = enable-sender<Sndr>;

  template<class Sndr>
    consteval bool is-dependent-sender-helper() try {           // exposition only
      get_completion_signatures<Sndr>();
      return false;
    } catch (dependent_sender_error&) {
      return true;
    }

  template<class Sndr>
    concept sender =
      enable_sender<remove_cvref_t<Sndr>> &&
      requires (const remove_cvref_t<Sndr>& sndr) {
        { get_env(sndr) } -> queryable;
      } &&
      move_constructible<remove_cvref_t<Sndr>> &&
      constructible_from<remove_cvref_t<Sndr>, Sndr>;

  template<class Sndr, class... Env>
    concept sender_in =
      sender<Sndr> &&
      (sizeof...(Env) <= 1) &&
      (queryable<Env> &&...) &&
      is-constant<get_completion_signatures<Sndr, Env...>()>;

  template<class Sndr>
    concept dependent_sender =
      sender<Sndr> && bool_constant<is-dependent-sender-helper<Sndr>()>::value;

  template<class Sndr, class Rcvr>
    concept sender_to =
      sender_in<Sndr, env_of_t<Rcvr>> &&
      receiver_of<Rcvr, completion_signatures_of_t<Sndr, env_of_t<Rcvr>>> &&
      requires (Sndr&& sndr, Rcvr&& rcvr) {
        connect(std::forward<Sndr>(sndr), std::forward<Rcvr>(rcvr));
      };
}
```

For a type `Sndr`, if `sender<Sndr>` is `true` and
`dependent_sender<Sndr>` is `false`, then `Sndr` is a non-dependent
sender [[exec.async.ops]].

Given a subexpression `sndr`, let `Sndr` be `decltype((sndr))` and let
`rcvr` be a receiver with an associated environment whose type is `Env`.
A completion operation is a *permissible completion* for `Sndr` and
`Env` if its completion signature appears in the argument list of the
specialization of `completion_signatures` denoted by
`completion_signatures_of_t<Sndr, Env>`. `Sndr` and `Env` model
`sender_in<Sndr, Env>` if all the completion operations that are
potentially evaluated by connecting `sndr` to `rcvr` and starting the
resulting operation state are permissible completions for `Sndr` and
`Env`.

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`enable_sender` to `true` for cv-unqualified program-defined types that
model `sender`, and `false` for types that do not. Such specializations
shall be usable in constant expressions [[expr.const]] and have type
`const bool`.

The exposition-only concepts `sender-of` and `sender-in-of` define the
requirements for a sender type that completes with a given unique set of
value result types.

``` cpp
namespace std::execution {
  template<class... As>
    using value-signature = set_value_t(As...);             // exposition only

  template<class Sndr, class SetValue, class... Env>
    concept sender-in-of-impl =                             // exposition only
      sender_in<Sndr, Env...> &&
      MATCHING-SIG(SetValue,                                // see [exec.general]
                   gather-signatures<set_value_t,           // see [exec.cmplsig]
                                     completion_signatures_of_t<Sndr, Env...>,
                                     value-signature,
                                     type_identity_t>);

  template<class Sndr, class Env, class... Values>
    concept sender-in-of =                                  // exposition only
      sender-in-of-impl<Sndr, set_value_t(Values...), Env>;

  template<class Sndr, class... Values>
    concept sender-of =                                     // exposition only
      sender-in-of-impl<Sndr, set_value_t(Values...)>;
}
```

Let `sndr` be an expression such that `decltype((sndr))` is `Sndr`. The
type `tag_of_t<Sndr>` is as follows:

- If the declaration
  ``` cpp
  auto&& [tag, data, ...children] = sndr;
  ```

  would be well-formed, `tag_of_t<Sndr>` is an alias for
  `decltype(auto(tag))`.
- Otherwise, `tag_of_t<Sndr>` is ill-formed.

Let `sender-for` be an exposition-only concept defined as follows:

``` cpp
namespace std::execution {
  template<class Sndr, class Tag>
  concept sender-for =
    sender<Sndr> &&
    same_as<tag_of_t<Sndr>, Tag>;
}
```

For a type `T`, `SET-VALUE-SIG(T)` denotes the type `set_value_t()` if
`T` is cv `void`; otherwise, it denotes the type `set_value_t(T)`.

Library-provided sender types

- always expose an overload of a member `connect` that accepts an rvalue
  sender and
- only expose an overload of a member `connect` that accepts an lvalue
  sender if they model `copy_constructible`.

### Awaitable helpers <a id="exec.awaitable">[[exec.awaitable]]</a>

The sender concepts recognize awaitables as senders. For [[exec]], an
*awaitable* is an expression that would be well-formed as the operand of
a `co_await` expression within a given context.

For a subexpression `c`, let `GET-AWAITER(c, p)` be
expression-equivalent to the series of transformations and conversions
applied to `c` as the operand of an *await-expression* in a coroutine,
resulting in lvalue `e` as described by [[expr.await]], where `p` is an
lvalue referring to the coroutine’s promise, which has type `Promise`.

[*Note 1*: This includes the invocation of the promise type’s
`await_transform` member if any, the invocation of the
`operator co_await` picked by overload resolution if any, and any
necessary implicit conversions and materializations. — *end note*]

Let `GET-AWAITER(c)` be expression-equivalent to `GET-AWAITER(c, q)`
where `q` is an lvalue of an unspecified empty class type `none-such`
that lacks an `await_transform` member, and where
`coroutine_handle<none-such>` behaves as `coroutine_handle<void>`.

Let `is-awaitable` be the following exposition-only concept:

``` cpp
namespace std {
  template<class T>
  concept await-suspend-result = see below;                     // exposition only

  template<class A, class... Promise>
  concept is-awaiter =                                          // exposition only
    requires (A& a, coroutine_handle<Promise...> h) {
      a.await_ready() ? 1 : 0;
      { a.await_suspend(h) } -> await-suspend-result;
      a.await_resume();
    };

  template<class C, class... Promise>
  concept is-awaitable =                                        // exposition only
    requires (C (*fc)() noexcept, Promise&... p) {
      { GET-AWAITER(fc(), p...) } -> is-awaiter<Promise...>;
    };
}
```

`\defexposconcept{await-suspend-result}<T>` is `true` if and only if one
of the following is `true`:

- `T` is `void`, or
- `T` is `bool`, or
- `T` is a specialization of `coroutine_handle`.

For a subexpression `c` such that `decltype((c))` is type `C`, and an
lvalue `p` of type `Promise`, `await-result-\newline type<C, Promise>`
denotes the type `decltype(GET-AWAITER(c, p).await_resume())` and
`await-result-type<C>` denotes the type
`decltype(GET-AWAITER(c).await_resume())`.

Let *`with-await-transform`* be the exposition-only class template:

``` cpp
namespace std::execution {
  template<class T, class Promise>
    concept has-as-awaitable =                                  // exposition only
      requires (T&& t, Promise& p) {
        { std::forward<T>(t).as_awaitable(p) } -> is-awaitable<Promise&>;
      };

  template<class Derived>
    struct with-await-transform {                               // exposition only
      template<class T>
        T&& await_transform(T&& value) noexcept {
          return std::forward<T>(value);
        }

      template<has-as-awaitable<Derived> T>
        auto await_transform(T&& value)
          noexcept(noexcept(std::forward<T>(value).as_awaitable(declval<Derived&>())))
          -> decltype(std::forward<T>(value).as_awaitable(declval<Derived&>())) {
          return std::forward<T>(value).as_awaitable(static_cast<Derived&>(*this));
        }
    };
}
```

Let *`env-promise`* be the exposition-only class template:

``` cpp
namespace std::execution {
  template<class Env>
  struct env-promise : with-await-transform<env-promise<Env>> { // exposition only
    unspecified get_return_object() noexcept;
    unspecified initial_suspend() noexcept;
    unspecified final_suspend() noexcept;
    void unhandled_exception() noexcept;
    void return_void() noexcept;
    coroutine_handle<> unhandled_stopped() noexcept;

    const Env& get_env() const noexcept;
  };
}
```

[*Note 2*: Specializations of *`env-promise`* are used only for the
purpose of type computation; its members need not be
defined. — *end note*]

### `execution::default_domain` <a id="exec.domain.default">[[exec.domain.default]]</a>

``` cpp
namespace std::execution {
  struct default_domain {
    template<sender Sndr, queryable... Env>
        requires (sizeof...(Env) <= 1)
      static constexpr sender decltype(auto) transform_sender(Sndr&& sndr, const Env&... env)
        noexcept(see below);

    template<sender Sndr, queryable Env>
      static constexpr queryable decltype(auto) transform_env(Sndr&& sndr, Env&& env) noexcept;

    template<class Tag, sender Sndr, class... Args>
      static constexpr decltype(auto) apply_sender(Tag, Sndr&& sndr, Args&&... args)
        noexcept(see below);
  };
}
```

``` cpp
template<sender Sndr, queryable... Env>
  requires (sizeof...(Env) <= 1)
constexpr sender decltype(auto) transform_sender(Sndr&& sndr, const Env&... env)
  noexcept(see below);
```

Let `e` be the expression

``` cpp
tag_of_t<Sndr>().transform_sender(std::forward<Sndr>(sndr), env...)
```

if that expression is well-formed; otherwise,
`std::forward<Sndr>(sndr)`.

*Returns:* `e`.

*Remarks:* The exception specification is equivalent to `noexcept(e)`.

``` cpp
template<sender Sndr, queryable Env>
  constexpr queryable decltype(auto) transform_env(Sndr&& sndr, Env&& env) noexcept;
```

Let `e` be the expression

``` cpp
tag_of_t<Sndr>().transform_env(std::forward<Sndr>(sndr), std::forward<Env>(env))
```

if that expression is well-formed; otherwise,
*`FWD-ENV`*`(std::forward<Env>(env))`.

*Mandates:* `noexcept(e)` is `true`.

*Returns:* `e`.

``` cpp
template<class Tag, sender Sndr, class... Args>
constexpr decltype(auto) apply_sender(Tag, Sndr&& sndr, Args&&... args)
  noexcept(see below);
```

Let `e` be the expression

``` cpp
Tag().apply_sender(std::forward<Sndr>(sndr), std::forward<Args>(args)...)
```

*Constraints:* `e` is a well-formed expression.

*Returns:* `e`.

*Remarks:* The exception specification is equivalent to `noexcept(e)`.

### `execution::transform_sender` <a id="exec.snd.transform">[[exec.snd.transform]]</a>

``` cpp
namespace std::execution {
  template<class Domain, sender Sndr, queryable... Env>
      requires (sizeof...(Env) <= 1)
    constexpr sender decltype(auto) transform_sender(Domain dom, Sndr&& sndr, const Env&... env)
      noexcept(see below);
}
```

Let *transformed-sndr* be the expression

``` cpp
dom.transform_sender(std::forward<Sndr>(sndr), env...)
```

if that expression is well-formed; otherwise,

``` cpp
default_domain().transform_sender(std::forward<Sndr>(sndr), env...)
```

Let *final-sndr* be the expression *transformed-sndr* if
*transformed-sndr* and *sndr* have the same type ignoring cv-qualifiers;
otherwise, it is the expression
`transform_sender(dom, `*`transformed-sndr`*`, env...)`.

*Returns:* *final-sndr*.

*Remarks:* The exception specification is equivalent to
`noexcept(`*`final-sndr`*`)`.

### `execution::transform_env` <a id="exec.snd.transform.env">[[exec.snd.transform.env]]</a>

``` cpp
namespace std::execution {
  template<class Domain, sender Sndr, queryable Env>
    constexpr queryable decltype(auto) transform_env(Domain dom, Sndr&& sndr, Env&& env) noexcept;
}
```

Let `e` be the expression

``` cpp
dom.transform_env(std::forward<Sndr>(sndr), std::forward<Env>(env))
```

if that expression is well-formed; otherwise,

``` cpp
default_domain().transform_env(std::forward<Sndr>(sndr), std::forward<Env>(env))
```

*Mandates:* `noexcept(e)` is `true`.

*Returns:* `e`.

### `execution::apply_sender` <a id="exec.snd.apply">[[exec.snd.apply]]</a>

``` cpp
namespace std::execution {
  template<class Domain, class Tag, sender Sndr, class... Args>
    constexpr decltype(auto) apply_sender(Domain dom, Tag, Sndr&& sndr, Args&&... args)
      noexcept(see below);
}
```

Let e be the expression

``` cpp
dom.apply_sender(Tag(), std::forward<Sndr>(sndr), std::forward<Args>(args)...)
```

if that expression is well-formed; otherwise,

``` cpp
default_domain().apply_sender(Tag(), std::forward<Sndr>(sndr), std::forward<Args>(args)...)
```

*Constraints:* The expression e is well-formed.

*Returns:* e.

*Remarks:* The exception specification is equivalent to `noexcept(`e`)`.

### `execution::get_completion_signatures` <a id="exec.getcomplsigs">[[exec.getcomplsigs]]</a>

``` cpp
template<class Sndr, class... Env>
  consteval auto get_completion_signatures() -> valid-completion-signatures auto;
```

Let except be an rvalue subexpression of an unspecified class type
Except such that `<`Except`> && derived_from<`Except`, exception>` is
`true`. Let *`CHECKED-COMPLSIGS`*`(`e`)` be e if e is a core constant
expression whose type satisfies `valid-completion-signatures`;
otherwise, it is the following expression:

``` cpp
(e, throw except, completion_signatures())
```

Let *`get-complsigs`*`<Sndr, Env...>()` be expression-equivalent to
`remove_reference_t<Sndr>::template get_completion_signatures<Sndr, Env...>()`.
Let `NewSndr` be `Sndr` if `sizeof...(Env) == 0` is `true`; otherwise,
`decltype(`s`)` where s is the following expression:

``` cpp
transform_sender(
  get-domain-late(declval<Sndr>(), declval<Env>()...),
  declval<Sndr>(),
  declval<Env>()...)
```

*Constraints:* `sizeof...(Env) <= 1` is `true`.

*Effects:* Equivalent to: `return `e`;` where e is expression-equivalent
to the following:

- *`CHECKED-COMPLSIGS`*`(`*`get-complsigs`*`<NewSndr, Env...>())` if
  *`get-complsigs`*`<NewSndr, Env...>()` is a well-formed expression.
- Otherwise, *`CHECKED-COMPLSIGS`*`(`*`get-complsigs`*`<NewSndr>())` if
  *`get-complsigs`*`<NewSndr>()` is a well-formed expression.
- Otherwise,
  ``` cpp
  completion_signatures<
    SET-VALUE-SIG(await-result-type<NewSndr, env-promise<Env>...>),   // REF:exec.snd.concepts
    set_error_t(exception_ptr),
    set_stopped_t()>
  ```

  if `is-awaitable<NewSndr, `*`env-promise`*`<Env>...>` is `true`.
- Otherwise,
  `(throw `*`dependent-sender-error`*`(), completion_signatures())` if
  `sizeof...(Env) == 0` is `true`, where *`dependent-sender-error`* is
  `dependent_sender_error` or an unspecified type derived publicly and
  unambiguously from `dependent_sender_error`.
- Otherwise, `(throw `except`, completion_signatures())`.

Given a type `Env`, if `completion_signatures_of_t<Sndr>` and
`completion_signatures_of_t<Sndr, Env>` are both well-formed, they shall
denote the same type.

Let `rcvr` be an rvalue whose type `Rcvr` models `receiver`, and let
`Sndr` be the type of a sender such that
`sender_in<Sndr, env_of_t<Rcvr>>` is `true`. Let `Sigs...` be the
template arguments of the `completion_signatures` specialization named
by `completion_signatures_of_t<Sndr, env_of_t<Rcvr>>`. Let `CSO` be a
completion function. If sender `Sndr` or its operation state cause the
expression `CSO(rcvr, args...)` to be potentially evaluated
[[basic.def.odr]] then there shall be a signature `Sig` in `Sigs...`
such that

``` cpp
MATCHING-SIG(decayed-typeof<CSO>(decltype(args)...), Sig)
```

is `true` [[exec.general]].

### `execution::connect` <a id="exec.connect">[[exec.connect]]</a>

`connect` connects [[exec.async.ops]] a sender with a receiver.

The name `connect` denotes a customization point object. For
subexpressions `sndr` and `rcvr`, let `Sndr` be `decltype((sndr))` and
`Rcvr` be `decltype((rcvr))`, let `new_sndr` be the expression

``` cpp
transform_sender(decltype(get-domain-late(sndr, get_env(rcvr))){}, sndr, get_env(rcvr))
```

and let `DS` and `DR` be `decay_t<decltype((new_sndr))>` and
`decay_t<Rcvr>`, respectively.

Let *`connect-awaitable-promise`* be the following exposition-only
class:

``` cpp
namespace std::execution {
  struct connect-awaitable-promise : with-await-transform<connect-awaitable-promise> {

    connect-awaitable-promise(DS&, DR& rcvr) noexcept : rcvr(rcvr) {}

    suspend_always initial_suspend() noexcept { return {}; }
    [[noreturn]] suspend_always final_suspend() noexcept { terminate(); }
    [[noreturn]] void unhandled_exception() noexcept { terminate(); }
    [[noreturn]] void return_void() noexcept { terminate(); }

    coroutine_handle<> unhandled_stopped() noexcept {
      set_stopped(std::move(rcvr));
      return noop_coroutine();
    }

    operation-state-task get_return_object() noexcept {
      return operation-state-task{
        coroutine_handle<connect-awaitable-promise>::from_promise(*this)};
    }

    env_of_t<DR> get_env() const noexcept {
      return execution::get_env(rcvr);
    }

  private:
    DR& rcvr;                           // exposition only
  };
}
```

Let *`operation-state-task`* be the following exposition-only class:

``` cpp
namespace std::execution {
  struct operation-state-task {                              // exposition only
    using operation_state_concept = operation_state_t;
    using promise_type = connect-awaitable-promise;

    explicit operation-state-task(coroutine_handle<> h) noexcept : coro(h) {}
    operation-state-task(operation-state-task&&) = delete;
    ~operation-state-task() { coro.destroy(); }

    void start() & noexcept {
      coro.resume();
    }

  private:
    coroutine_handle<> coro;                                    // exposition only
  };
}
```

Let `V` name the type
`await-result-type<DS, connect-awaitable-promise>`, let `Sigs` name the
type

``` cpp
completion_signatures<
  SET-VALUE-SIG(V),         // see~[exec.snd.concepts]
  set_error_t(exception_ptr),
  set_stopped_t()>
```

and let *`connect-awaitable`* be an exposition-only coroutine defined as
follows:

``` cpp
namespace std::execution {
  template<class Fun, class... Ts>
  auto suspend-complete(Fun fun, Ts&&... as) noexcept {    // exposition only
    auto fn = [&, fun]() noexcept { fun(std::forward<Ts>(as)...); };

    struct awaiter {
      decltype(fn) fn;                                     // exposition only

      static constexpr bool await_ready() noexcept { return false; }
      void await_suspend(coroutine_handle<>) noexcept { fn(); }
      [[noreturn]] void await_resume() noexcept { unreachable(); }
    };
    return awaiter{fn};
  }

  operation-state-task connect-awaitable(DS sndr, DR rcvr) requires receiver_of<DR, Sigs> {
    exception_ptr ep;
    try {
      if constexpr (same_as<V, void>) {
        co_await std::move(sndr);
        co_await suspend-complete(set_value, std::move(rcvr));
      } else {
        co_await suspend-complete(set_value, std::move(rcvr), co_await std::move(sndr));
      }
    } catch(...) {
      ep = current_exception();
    }
    co_await suspend-complete(set_error, std::move(rcvr), std::move(ep));
  }
}
```

The expression `connect(sndr, rcvr)` is expression-equivalent to:

- `new_sndr.connect(rcvr)` if that expression is well-formed.
  *Mandates:* The type of the expression above satisfies
  `operation_state`.
- Otherwise, `connect-awaitable(new_sndr, rcvr)`.

Except that `rcvr` is evaluated only once.

*Mandates:* The following are `true`:

- `\texttt{sender_in}<Sndr, env_of_t<Rcvr>>`
- `\texttt{receiver_of}<Rcvr, completion_signatures_of_t<Sndr, env_of_t<Rcvr>>>`

### Sender factories <a id="exec.factories">[[exec.factories]]</a>

#### `execution::schedule` <a id="exec.schedule">[[exec.schedule]]</a>

`schedule` obtains a schedule sender [[exec.async.ops]] from a
scheduler.

The name `schedule` denotes a customization point object. For a
subexpression `sch`, the expression `schedule(sch)` is
expression-equivalent to `sch.schedule()`.

*Mandates:* The type of `sch.schedule()` satisfies `sender`.

If the expression

``` cpp
get_completion_scheduler<set_value_t>(get_env(sch.schedule())) == sch
```

is ill-formed or evaluates to `false`, the behavior of calling
`schedule(sch)` is undefined.

#### `execution::just`, `execution::just_error`, `execution::just_stopped` <a id="exec.just">[[exec.just]]</a>

`just`, `just_error`, and `just_stopped` are sender factories whose
asynchronous operations complete synchronously in their start operation
with a value completion operation, an error completion operation, or a
stopped completion operation, respectively.

The names `just`, `just_error`, and `just_stopped` denote customization
point objects. Let *`just-cpo`* be one of `just`, `just_error`, or
`just_stopped`. For a pack of subexpressions `ts`, let `Ts` be the pack
of types `decltype((ts))`. The expression `just-cpo(ts...)` is
ill-formed if

- `(movable-value<Ts> &&...)` is `false`, or
- *`just-cpo`* is `just_error` and `sizeof...(ts) == 1` is `false`, or
- *`just-cpo`* is `just_stopped` and `sizeof...(ts) == 0` is `false`.

Otherwise, it is expression-equivalent to
`make-sender(just-cpo, product-type{ts...})`.

For `just`, `just_error`, and `just_stopped`, let *`set-cpo`* be
`set_value`, `set_error`, and `set_stopped`, respectively. The
exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for *`just-cpo`* as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<decayed-typeof<just-cpo>> : default-impls {
    static constexpr auto start =
      [](auto& state, auto& rcvr) noexcept -> void {
        auto& [...ts] = state;
        set-cpo(std::move(rcvr), std::move(ts)...);
      };
  };
}
```

#### `execution::read_env` <a id="exec.read.env">[[exec.read.env]]</a>

`read_env` is a sender factory for a sender whose asynchronous operation
completes synchronously in its start operation with a value completion
result equal to a value read from the receiver’s associated environment.

`read_env` is a customization point object. For some query object `q`,
the expression `read_env(q)` is expression-equivalent to
`make-sender(read_env, q)`.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `read_env` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<decayed-typeof<read_env>> : default-impls {
    static constexpr auto start =
      [](auto query, auto& rcvr) noexcept -> void {
        TRY-SET-VALUE(rcvr, query(get_env(rcvr)));
      };
  };

  template<class Sndr, class Env>
    static consteval void check-types();
}
```

``` cpp
template<class Sndr, class Env>
  static consteval void check-types();
```

Let `Q` be `decay_t<`*`data-type`*`<Sndr>>`.

*Throws:* An exception of an unspecified type derived from `exception`
if the expression `Q()(env)` is ill-formed or has type `void`, where
`env` is an lvalue subexpression whose type is `Env`.

### Sender adaptors <a id="exec.adapt">[[exec.adapt]]</a>

#### General <a id="exec.adapt.general">[[exec.adapt.general]]</a>

Subclause [[exec.adapt]] specifies a set of sender adaptors.

The bitwise inclusive operator is overloaded for the purpose of creating
sender chains. The adaptors also support function call syntax with
equivalent semantics.

Unless otherwise specified:

- A sender adaptor is prohibited from causing observable effects, apart
  from moving and copying its arguments, before the returned sender is
  connected with a receiver using `connect`, and `start` is called on
  the resulting operation state.
- A parent sender [[exec.async.ops]] with a single child sender `sndr`
  has an associated attribute object equal to `FWD-ENV(get_env(sndr))`
  [[exec.fwd.env]].
- A parent sender with more than one child sender has an associated
  attributes object equal to `env<>{}`.
- When a parent sender is connected to a receiver `rcvr`, any receiver
  used to connect a child sender has an associated environment equal to
  `FWD-ENV(get_env(rcvr))`.
- An adaptor whose child senders are all non-dependent
  [[exec.async.ops]] is itself non-dependent.
- These requirements apply to any function that is selected by the
  implementation of the sender adaptor.
- *Recommended practice:* Implementations should use the completion
  signatures of the adaptors to communicate type errors to users and to
  propagate any such type errors from child senders.

If a sender returned from a sender adaptor specified in [[exec.adapt]]
is specified to include `set_error_t(Err)` among its set of completion
signatures where `decay_t<Err>` denotes the type `exception_ptr`, but
the implementation does not potentially evaluate an error completion
operation with an `exception_ptr` argument, the implementation is
allowed to omit the `exception_ptr` error completion signature from the
set.

#### Closure objects <a id="exec.adapt.obj">[[exec.adapt.obj]]</a>

A *pipeable sender adaptor closure object* is a function object that
accepts one or more `sender` arguments and returns a `sender`. For a
pipeable sender adaptor closure object `c` and an expression `sndr` such
that `decltype((sndr))` models `sender`, the following expressions are
equivalent and yield a `sender`:

``` cpp
c(sndr)
sndr | c
```

Given an additional pipeable sender adaptor closure object `d`, the
expression `c | d` produces another pipeable sender adaptor closure
object `e`:

`e` is a perfect forwarding call wrapper [[func.require]] with the
following properties:

- Its target object is an object `d2` of type `decltype(auto(d))`
  direct-non-list-initialized with `d`.
- It has one bound argument entity, an object `c2` of type
  `decltype(auto(c))` direct-non-list-initialized with `c`.
- Its call pattern is `d2(c2(arg))`, where arg is the argument used in a
  function call expression of `e`.

The expression `c | d` is well-formed if and only if the initializations
of the state entities [[func.def]] of `e` are all well-formed.

An object `t` of type `T` is a pipeable sender adaptor closure object if
`T` models `derived_from<sender_adaptor_closure<T>>`, `T` has no other
base classes of type `sender_adaptor_closure<U>` for any other type `U`,
and `T` does not satisfy `sender`.

The template parameter `D` for `sender_adaptor_closure` can be an
incomplete type. Before any expression of type cv `D` appears as an
operand to the `|` operator, `D` shall be complete and model
`derived_from<sender_adaptor_closure<D>>`. The behavior of an expression
involving an object of type cv `D` as an operand to the `|` operator is
undefined if overload resolution selects a program-defined `operator|`
function.

A *pipeable sender adaptor object* is a customization point object that
accepts a `sender` as its first argument and returns a `sender`. If a
pipeable sender adaptor object accepts only one argument, then it is a
pipeable sender adaptor closure object.

If a pipeable sender adaptor object adaptor accepts more than one
argument, then let `sndr` be an expression such that `decltype((sndr))`
models `sender`, let `args...` be arguments such that
`adaptor(sndr, args...)` is a well-formed expression as specified below,
and let `BoundArgs` be a pack that denotes `decltype(auto(args))...`.
The expression `adaptor(args...)` produces a pipeable sender adaptor
closure object `f` that is a perfect forwarding call wrapper with the
following properties:

- Its target object is a copy of adaptor.
- Its bound argument entities `bound_args` consist of objects of types
  `BoundArgs...` direct-non-list-initialized with
  `std::forward<decltype((args))>(args)...`, respectively.
- Its call pattern is `adaptor(rcvr, bound_args...)`, where `rcvr` is
  the argument used in a function call expression of `f`.

The expression `adaptor(args...)` is well-formed if and only if the
initializations of the bound argument entities of the result, as
specified above, are all well-formed.

#### `execution::write_env` <a id="exec.write.env">[[exec.write.env]]</a>

`write_env` is a sender adaptor that accepts a sender and a queryable
object, and that returns a sender that, when connected with a receiver
`rcvr`, connects the adapted sender with a receiver whose execution
environment is the result of joining the `queryable` object to the
result of `get_env(rcvr)`.

`write_env` is a customization point object. For some subexpressions
`sndr` and `env`, if `decltype((sndr))` does not satisfy `sender` or if
`decltype((env))` does not satisfy `queryable`, the expression
`write_env(sndr, env)` is ill-formed. Otherwise, it is
expression-equivalent to `make-sender(write_env, env, sndr)`.

Let *`write-env-t`* denote the type `decltype(auto(write_env))`. The
exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for *`write-env-t`* as follows:

``` cpp
template<>
struct impls-for<write-env-t> : default-impls {
  static constexpr auto join-env(const auto& state, const auto& env) noexcept {
    return see below;
  }

  static constexpr auto get-env =
    [](auto, const auto& state, const auto& rcvr) noexcept {
      return join-env(state, FWD-ENV(get_env(rcvr)));
    };

  template<class Sndr, class... Env>
    static consteval void check-types();
};
```

Invocation of `impls-for<write-env-t>::join-env` returns an object `e`
such that

- `decltype(e)` models `queryable` and
- given a query object `q`, the expression `e.query(q)` is
  expression-equivalent to `state.query(q)` if that expression is valid,
  otherwise, `e.query(q)` is expression-equivalent to `env.query(q)`.

For a type `Sndr` and a pack of types `Env`, let `State` be
`data-type<Sndr>` and let `JoinEnv` be the pack
`decltype(join-env(declval<State>(), FWD-ENV(declval<Env>())))`. Then
`impls-for<write-env-{t}>::check-types<Sndr, Env...>()` is
expression-equivalent to
`get_completion_signatures<child-{type}<Sndr>, JoinEnv...>()`.

#### `execution::unstoppable` <a id="exec.unstoppable">[[exec.unstoppable]]</a>

`unstoppable` is a sender adaptor that connects its inner sender with a
receiver that has the execution environment of the outer receiver but
with an object of type `never_stop_token` as the result of the
`get_stop_token query`.

For a subexpression `sndr`, `unstoppable(sndr)` is expression-equivalent
to `write_env(sndr, prop(get_stop_token, never_stop_token{}))`.

#### `execution::starts_on` <a id="exec.starts.on">[[exec.starts.on]]</a>

`starts_on` adapts an input sender into a sender that will start on an
execution agent belonging to a particular scheduler’s associated
execution resource.

The name `starts_on` denotes a customization point object. For
subexpressions `sch` and `sndr`, if `decltype((\newline sch))` does not
satisfy `scheduler`, or `decltype((sndr))` does not satisfy `sender`,
`starts_on(sch, sndr)` is ill-formed.

Otherwise, the expression `starts_on(sch, sndr)` is
expression-equivalent to:

``` cpp
transform_sender(
  query-with-default(get_domain, sch, default_domain()),
  make-sender(starts_on, sch, sndr))
```

except that `sch` is evaluated only once.

Let `out_sndr` and `env` be subexpressions such that `OutSndr` is
`decltype((out_sndr))`. If `sender-for<OutSndr, starts_on_t>` is
`false`, then the expressions `starts_on.transform_env(out_sndr, env)`
and `starts_on.transform_sender(out_sndr, env)` are ill-formed;
otherwise

- `starts_on.transform_env(out_sndr, env)` is equivalent to:
  ``` cpp
  auto&& [_, sch, _] = out_sndr;
  return JOIN-ENV(SCHED-ENV(sch), FWD-ENV(env));
  ```
- `starts_on.transform_sender(out_sndr, env)` is equivalent to:
  ``` cpp
  auto&& [_, sch, sndr] = out_sndr;
  return let_value(
    schedule(sch),
    [sndr = std::forward_like<OutSndr>(sndr)]() mutable
      noexcept(is_nothrow_move_constructible_v<decay_t<OutSndr>>) {
      return std::move(sndr);
    });
  ```

Let `out_sndr` be a subexpression denoting a sender returned from
`starts_on(sch, sndr)` or one equal to such, and let `OutSndr` be the
type `decltype((out_sndr))`. Let `out_rcvr` be a subexpression denoting
a receiver that has an environment of type `Env` such that
`sender_in<OutSndr, Env>` is `true`. Let `op` be an lvalue referring to
the operation state that results from connecting `out_sndr` with
`out_rcvr`. Calling `start(op)` shall start `sndr` on an execution agent
of the associated execution resource of `sch`. If scheduling onto `sch`
fails, an error completion on `out_rcvr` shall be executed on an
unspecified execution agent.

#### `execution::continues_on` <a id="exec.continues.on">[[exec.continues.on]]</a>

`continues_on` adapts a sender into one that completes on the specified
scheduler.

The name `continues_on` denotes a pipeable sender adaptor object. For
subexpressions `sch` and `sndr`, if `decltype((sch))` does not satisfy
`scheduler`, or `decltype((sndr))` does not satisfy `sender`,
`continues_on(sndr, sch)` is ill-formed.

Otherwise, the expression `continues_on(sndr, sch)` is
expression-equivalent to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(continues_on, sch, sndr))
```

except that `sndr` is evaluated only once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `continues_on_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<continues_on_t> : default-impls {
    static constexpr auto get-attrs =
      [](const auto& data, const auto& child) noexcept -> decltype(auto) {
        return JOIN-ENV(SCHED-ATTRS(data), FWD-ENV(get_env(child)));
      };
  };
}
```

Let `sndr` and `env` be subexpressions such that `Sndr` is
`decltype((sndr))`. If `sender-for<Sndr, continues_on_t>` is `false`,
then the expression `continues_on.transform_sender(sndr, env)` is
ill-formed; otherwise, it is equal to:

``` cpp
auto [_, data, child] = sndr;
return schedule_from(std::move(data), std::move(child));
```

[*Note 1*: This causes the `continues_on(sndr, sch)` sender to become
`schedule_from(sch, sndr)` when it is connected with a receiver whose
execution domain does not customize `continues_on`. — *end note*]

Let `out_sndr` be a subexpression denoting a sender returned from
`continues_on(sndr, sch)` or one equal to such, and let `OutSndr` be the
type `decltype((out_sndr))`. Let `out_rcvr` be a subexpression denoting
a receiver that has an environment of type `Env` such that
`sender_in<OutSndr, Env>` is `true`. Let `op` be an lvalue referring to
the operation state that results from connecting `out_sndr` with
`out_rcvr`. Calling `start(op)` shall start `sndr` on the current
execution agent and execute completion operations on `out_rcvr` on an
execution agent of the execution resource associated with `sch`. If
scheduling onto `sch` fails, an error completion on `out_rcvr` shall be
executed on an unspecified execution agent.

#### `execution::schedule_from` <a id="exec.schedule.from">[[exec.schedule.from]]</a>

`schedule_from` schedules work dependent on the completion of a sender
onto a scheduler’s associated execution resource.

[*Note 1*: `schedule_from` is not meant to be used in user code; it is
used in the implementation of `continues_on`. — *end note*]

The name `schedule_from` denotes a customization point object. For some
subexpressions `sch` and `sndr`, let `Sch` be `decltype((sch))` and
`Sndr` be `decltype((sndr))`. If `Sch` does not satisfy `scheduler`, or
`Sndr` does not satisfy `sender`, `schedule_from(sch, sndr)` is
ill-formed.

Otherwise, the expression `schedule_from(sch, sndr)` is
expression-equivalent to:

``` cpp
transform_sender(
  query-with-default(get_domain, sch, default_domain()),
  make-sender(schedule_from, sch, sndr))
```

except that `sch` is evaluated only once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `schedule_from_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<schedule_from_t> : default-impls {
    static constexpr auto get-attrs = see below;
    static constexpr auto get-state = see below;
    static constexpr auto complete = see below;

    template<class Sndr, class... Env>
      static consteval void check-types();
  };
}
```

The member `impls-for<schedule_from_t>::get-attrs` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[](const auto& data, const auto& child) noexcept -> decltype(auto) {
  return JOIN-ENV(SCHED-ATTRS(data), FWD-ENV(get_env(child)));
}
```

The member `impls-for<schedule_from_t>::get-state` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class Sndr, class Rcvr>(Sndr&& sndr, Rcvr& rcvr) noexcept(see below)
    requires sender_in<child-type<Sndr>, FWD-ENV-T(env_of_t<Rcvr>)> {

  auto& [_, sch, child] = sndr;

  using sched_t = decltype(auto(sch));
  using variant_t = see below;
  using receiver_t = see below;
  using operation_t = connect_result_t<schedule_result_t<sched_t>, receiver_t>;
  constexpr bool nothrow = noexcept(connect(schedule(sch), receiver_t{nullptr}));

  struct state-type {
    Rcvr& rcvr;                 // exposition only
    variant_t async-result;     // exposition only
    operation_t op-state;       // exposition only

    explicit state-type(sched_t sch, Rcvr& rcvr) noexcept(nothrow)
      : rcvr(rcvr), op-state(connect(schedule(sch), receiver_t{this})) {}
  };

  return state-type{sch, rcvr};
}
```

``` cpp
template<class Sndr, class... Env>
  static consteval void check-types();
```

*Effects:* Equivalent to:

``` cpp
get_completion_signatures<schedule_result_t<data-type<Sndr>>, FWD-ENV-T(Env)...>();
auto cs = get_completion_signatures<child-type<Sndr>, FWD-ENV-T(Env)...>();
decay-copyable-result-datums(cs);   // see REF:exec.snd.expos
```

Objects of the local class *`state-type`* can be used to initialize a
structured binding.

Let `Sigs` be a pack of the arguments to the `completion_signatures`
specialization named by
`completion_signatures_of_t<child-type<Sndr>, FWD-ENV-T(env_of_t<Rcvr>)>`.
Let *`as-tuple`* be an alias template such that `as-tuple<Tag(Args...)>`
denotes the type `decayed-tuple<Tag, Args...>`, and let
*`is-nothrow-decay-copy-sig`* be a variable template such that
`auto(is-nothrow-decay-copy-sig<Tag(Args...{})>)` is a constant
expression of type `bool` and equal to
`(is_nothrow_constructible_v<decay_t<Args>, Args> && ...)`. Let
*`error-completion`* be a pack consisting of the type
`set_error_t(exception_ptr)` if
`(is-nothrow-decay-copy-sig<Sigs> &&...)` is `false`, and an empty pack
otherwise. Then `variant_t` denotes the type
`variant<monostate, as-tuple<Sigs>..., error-completion...>`, except
with duplicate types removed.

`receiver_t` is an alias for the following exposition-only class:

``` cpp
namespace std::execution {
  struct receiver-type {
    using receiver_concept = receiver_t;
    state-type* state;          // exposition only

    void set_value() && noexcept {
      visit(
        [this]<class Tuple>(Tuple& result) noexcept -> void {
          if constexpr (!same_as<monostate, Tuple>) {
            auto& [tag, ...args] = result;
            tag(std::move(state->rcvr), std::move(args)...);
          }
        },
        state->async-result);
    }

    template<class Error>
    void set_error(Error&& err) && noexcept {
      execution::set_error(std::move(state->rcvr), std::forward<Error>(err));
    }

    void set_stopped() && noexcept {
      execution::set_stopped(std::move(state->rcvr));
    }

    decltype(auto) get_env() const noexcept {
      return FWD-ENV(execution::get_env(state->rcvr));
    }
  };
}
```

The expression in the `noexcept` clause of the lambda is `true` if the
construction of the returned *`state-type`* object is not potentially
throwing; otherwise, `false`.

The member `impls-for<schedule_from_t>::complete` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class Tag, class... Args>(auto, auto& state, auto& rcvr, Tag, Args&&... args) noexcept
    -> void {
  using result_t = decayed-tuple<Tag, Args...>;
  constexpr bool nothrow = (is_nothrow_constructible_v<decay_t<Args>, Args> && ...);

  try {
    state.async-result.template emplace<result_t>(Tag(), std::forward<Args>(args)...);
  } catch (...) {
    if constexpr (!nothrow)
      state.async-result.template emplace<tuple<set_error_t,
                                                exception_ptr>>(set_error, current_exception());
  }
  start(state.op-state);
};
```

Let `out_sndr` be a subexpression denoting a sender returned from
`schedule_from(sch, sndr)` or one equal to such, and let `OutSndr` be
the type `decltype((out_sndr))`. Let `out_rcvr` be a subexpression
denoting a receiver that has an environment of type `Env` such that
`sender_in<OutSndr, Env>` is `true`. Let `op` be an lvalue referring to
the operation state that results from connecting `out_sndr` with
`out_rcvr`. Calling `start(op)` shall start `sndr` on the current
execution agent and execute completion operations on `out_rcvr` on an
execution agent of the execution resource associated with `sch`. If
scheduling onto `sch` fails, an error completion on `out_rcvr` shall be
executed on an unspecified execution agent.

#### `execution::on` <a id="exec.on">[[exec.on]]</a>

The `on` sender adaptor has two forms:

- `on(sch, sndr)`, which starts a sender `sndr` on an execution agent
  belonging to a scheduler `sch`’s associated execution resource and
  that, upon `sndr`’s completion, transfers execution back to the
  execution resource on which the `on` sender was started.
- `on(sndr, sch, closure)`, which upon completion of a sender `sndr`,
  transfers execution to an execution agent belonging to a scheduler
  `sch`’s associated execution resource, then executes a sender adaptor
  closure `closure` with the async results of the sender, and that then
  transfers execution back to the execution resource on which `sndr`
  completed.

The name `on` denotes a pipeable sender adaptor object. For
subexpressions `sch` and `sndr`, `on(sch, sndr)` is ill-formed if any of
the following is `true`:

- `decltype((sch))` does not satisfy `scheduler`, or
- `decltype((sndr))` does not satisfy `sender` and `sndr` is not a
  pipeable sender adaptor closure object [[exec.adapt.obj]], or
- `decltype((sndr))` satisfies `sender` and `sndr `is also a pipeable
  sender adaptor closure object.

Otherwise, if `decltype((sndr))` satisfies `sender`, the expression
`on(sch, sndr)` is expression-equivalent to:

``` cpp
transform_sender(
  query-with-default(get_domain, sch, default_domain()),
  make-sender(on, sch, sndr))
```

except that `sch` is evaluated only once.

For subexpressions `sndr`, `sch`, and `closure`, if

- `decltype((sch))` does not satisfy `scheduler`, or
- `decltype((sndr))` does not satisfy `sender`, or
- `closure` is not a pipeable sender adaptor closure object
  [[exec.adapt.obj]],

the expression `on(sndr, sch, closure)` is ill-formed; otherwise, it is
expression-equivalent to:

``` cpp
transform_sender(
  get-domain-early(sndr),
  make-sender(on, product-type{sch, closure}, sndr))
```

except that `sndr` is evaluated only once.

Let `out_sndr` and `env` be subexpressions, let `OutSndr` be
`decltype((out_sndr))`, and let `Env` be `decltype((env))`. If
`sender-for<OutSndr, on_t>` is `false`, then the expressions
`on.transform_env(out_sndr, env)` and
`on.transform_sender(out_sndr, env)` are ill-formed.

Otherwise: Let *`not-a-scheduler`* be an unspecified empty class type.

The expression `on.transform_env(out_sndr, env)` has effects equivalent
to:

``` cpp
auto&& [_, data, _] = out_sndr;
if constexpr (scheduler<decltype(data)>) {
  return JOIN-ENV(SCHED-ENV(std::forward_like<OutSndr>(data)), FWD-ENV(std::forward<Env>(env)));
} else {
  return std::forward<Env>(env);
}
```

The expression `on.transform_sender(out_sndr, env)` has effects
equivalent to:

``` cpp
auto&& [_, data, child] = out_sndr;
if constexpr (scheduler<decltype(data)>) {
  auto orig_sch =
    query-with-default(get_scheduler, env, not-a-scheduler());

  if constexpr (same_as<decltype(orig_sch), not-a-scheduler>) {
    return not-a-sender{};
  } else {
    return continues_on(
      starts_on(std::forward_like<OutSndr>(data), std::forward_like<OutSndr>(child)),
      std::move(orig_sch));
  }
} else {
  auto& [sch, closure] = data;
  auto orig_sch = query-with-default(
    get_completion_scheduler<set_value_t>,
    get_env(child),
    query-with-default(get_scheduler, env, not-a-scheduler()));

  if constexpr (same_as<decltype(orig_sch), not-a-scheduler>) {
    return not-a-sender{};
  } else {
    return write_env(
      continues_on(
        std::forward_like<OutSndr>(closure)(
          continues_on(
            write_env(std::forward_like<OutSndr>(child), SCHED-ENV(orig_sch)),
            sch)),
        orig_sch),
      SCHED-ENV(sch));
  }
}
```

Let `out_sndr` be a subexpression denoting a sender returned from
`on(sch, sndr)` or one equal to such, and let `OutSndr` be the type
`decltype((out_sndr))`. Let `out_rcvr` be a subexpression denoting a
receiver that has an environment of type `Env` such that
`sender_in<OutSndr, Env>` is `true`. Let `op` be an lvalue referring to
the operation state that results from connecting `out_sndr` with
`out_rcvr`. Calling `start(op)` shall

- remember the current scheduler, `get_scheduler(get_env(rcvr))`;
- start `sndr` on an execution agent belonging to `sch`’s associated
  execution resource;
- upon `sndr`’s completion, transfer execution back to the execution
  resource associated with the scheduler remembered in step 1; and
- forward `sndr`’s async result to `out_rcvr`.

If any scheduling operation fails, an error completion on `out_rcvr`
shall be executed on an unspecified execution agent.

Let `out_sndr` be a subexpression denoting a sender returned from
`on(sndr, sch, closure)` or one equal to such, and let `OutSndr` be the
type `decltype((out_sndr))`. Let `out_rcvr` be a subexpression denoting
a receiver that has an environment of type `Env` such that
`sender_in<OutSndr, Env>` is `true`. Let `op` be an lvalue referring to
the operation state that results from connecting `out_sndr` with
`out_rcvr`. Calling `start(op)` shall

- remember the current scheduler, which is the first of the following
  expressions that is well-formed:
  - `get_completion_scheduler<set_value_t>(get_env(sndr))`
  - `get_scheduler(get_env(rcvr))`;
- start `sndr` on the current execution agent;
- upon `sndr`’s completion, transfer execution to an agent owned by
  `sch`’s associated execution resource;
- forward `sndr`’s async result as if by connecting and starting a
  sender `closure(S)`, where `S` is a sender that completes
  synchronously with `sndr`’s async result; and
- upon completion of the operation started in the previous step,
  transfer execution back to the execution resource associated with the
  scheduler remembered in step 1 and forward the operation’s async
  result to `out_rcvr`.

If any scheduling operation fails, an error completion on `out_rcvr`
shall be executed on an unspecified execution agent.

#### `execution::then`, `execution::upon_error`, `execution::upon_stopped` <a id="exec.then">[[exec.then]]</a>

`then` attaches an invocable as a continuation for an input sender’s
value completion operation. `upon_error` and `upon_stopped` do the same
for the error and stopped completion operations, respectively, sending
the result of the invocable as a value completion.

The names `then`, `upon_error`, and `upon_stopped` denote pipeable
sender adaptor objects. Let the expression *`then-cpo`* be one of
`then`, `upon_error`, or `upon_stopped`. For subexpressions `sndr` and
`f`, if `decltype((sndr))` does not satisfy `sender`, or `decltype((f))`
does not satisfy `movable-value`, `then-cpo(sndr, f) `is ill-formed.

Otherwise, the expression `then-cpo(sndr, f)` is expression-equivalent
to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(then-cpo, f, sndr))
```

except that `sndr` is evaluated only once.

For `then`, `upon_error`, and `upon_stopped`, let *`set-cpo`* be
`set_value`, `set_error`, and `set_stopped`, respectively. The
exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for *`then-cpo`* as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<decayed-typeof<then-cpo>> : default-impls {
    static constexpr auto complete =
      []<class Tag, class... Args>
        (auto, auto& fn, auto& rcvr, Tag, Args&&... args) noexcept -> void {
          if constexpr (same_as<Tag, decayed-typeof<set-cpo>>) {
            TRY-SET-VALUE(rcvr,
                          invoke(std::move(fn), std::forward<Args>(args)...));
          } else {
            Tag()(std::move(rcvr), std::forward<Args>(args)...);
          }
        };

    template<class Sndr, class... Env>
      static consteval void check-types();
  };
}
```

``` cpp
template<class Sndr, class... Env>
  static consteval void check-types();
```

*Effects:* Equivalent to:

``` cpp
auto cs = get_completion_signatures<child-type<Sndr>, FWD-ENV-T(Env)...>();
auto fn = []<class... Ts>(set_value_t(*)(Ts...)) {
  if constexpr (!invocable<remove_cvref_t<data-type<Sndr>>, Ts...>)
    throw unspecified-exception();
};
cs.for-each(overload-set{fn, [](auto){}});
```

where *`unspecified-exception`* is a type derived from `exception`.

The expression `then-cpo(sndr, f)` has undefined behavior unless it
returns a sender `out_sndr` that

- invokes `f` or a copy of such with the value, error, or stopped result
  datums of `sndr` for `then`, `upon_error`, and `upon_stopped`,
  respectively, using the result value of `f` as `out_sndr`’s value
  completion, and
- forwards all other completion operations unchanged.

#### `execution::let_value`, `execution::let_error`, `execution::let_stopped` <a id="exec.let">[[exec.let]]</a>

`let_value`, `let_error`, and `let_stopped` transform a sender’s value,
error, and stopped completions, respectively, into a new child
asynchronous operation by passing the sender’s result datums to a
user-specified callable, which returns a new sender that is connected
and started.

For `let_value`, `let_error`, and `let_stopped`, let *`set-cpo`* be
`set_value`, `set_error`, and `set_stopped`, respectively. Let the
expression *`let-cpo`* be one of `let_value`, `let_error`, or
`let_stopped`. For a subexpression `sndr`, let `let-env(sndr)` be
expression-equivalent to the first well-formed expression below:

- `\exposid{SCHED-ENV}(get_completion_scheduler<\exposid{decayed-typeof}<\exposid{set-cpo}>>(get_env(sndr)))`
- `\exposid{MAKE-ENV}(get_domain, get_domain(get_env(sndr)))`
- `(void(sndr), env<>{})`

The names `let_value`, `let_error`, and `let_stopped` denote pipeable
sender adaptor objects. For subexpressions `sndr` and `f`, let `F` be
the decayed type of `f`. If `decltype((sndr))` does not satisfy `sender`
or if `decltype((f))` does not satisfy `movable-value`, the expression
`let-cpo(sndr, f)` is ill-formed. If `F` does not satisfy `invocable`,
the expression `let_stopped(sndr, f)` is ill-formed.

Otherwise, the expression `let-cpo(sndr, f)` is expression-equivalent
to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(let-cpo, f, sndr))
```

except that `sndr` is evaluated only once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for *`let-cpo`* as follows:

``` cpp
namespace std::execution {
  template<class State, class Rcvr, class... Args>
  void let-bind(State& state, Rcvr& rcvr, Args&&... args);      // exposition only

  template<>
  struct impls-for<decayed-typeof<let-cpo>> : default-impls {
    static constexpr auto get-state = see below;
    static constexpr auto complete = see below;

    template<class Sndr, class... Env>
      static consteval void check-types();
  };
}
```

Let *`receiver2`* denote the following exposition-only class template:

``` cpp
namespace std::execution {
  template<class Rcvr, class Env>
  struct receiver2 {
    using receiver_concept = receiver_t;

    template<class... Args>
    void set_value(Args&&... args) && noexcept {
      execution::set_value(std::move(rcvr), std::forward<Args>(args)...);
    }

    template<class Error>
    void set_error(Error&& err) && noexcept {
      execution::set_error(std::move(rcvr), std::forward<Error>(err));
    }

    void set_stopped() && noexcept {
      execution::set_stopped(std::move(rcvr));
    }

    decltype(auto) get_env() const noexcept {
      return see below;
    }

    Rcvr& rcvr;                 // exposition only
    Env env;                    // exposition only
  };
}
```

Invocation of the function `receiver2::get_env` returns an object `e`
such that

- `decltype(e)` models `queryable` and
- given a query object `q`, the expression `e.query(q)` is
  expression-equivalent to `env.query(q)` if that expression is valid;
  otherwise, if the type of `q` satisfies `forwarding-query`,
  `e.query(q)` is expression-equivalent to `get_env(rcvr).query(q)`;
  otherwise, `e.query(q)` is ill-formed.

``` cpp
template<class Sndr, class... Env>
  static consteval void check-types();
```

*Effects:* Equivalent to:

``` cpp
using LetFn = remove_cvref_t<data-type<Sndr>>;
auto cs = get_completion_signatures<child-type<Sndr>, FWD-ENV-T(Env)...>();
auto fn = []<class... Ts>(decayed-typeof<set-cpo>(*)(Ts...)) {
  if constexpr (!is-valid-let-sender)   // see below
    throw unspecified-exception();
};
cs.for-each(overload-set(fn, [](auto){}));
```

where *`unspecified-exception`* is a type derived from `exception`, and
where *`is-valid-let-sender`* is `true` if and only if all of the
following are `true`:

- `(constructible_from<decay_t<Ts>, Ts> &&...)`
- `invocable<LetFn, decay_t<Ts>&...>`
- `sender<invoke_result_t<LetFn, decay_t<Ts>&...>>`
- `sizeof...(Env) == 0 || sender_in<invoke_result_t<LetFn, decay_t<Ts>&...>, `*`env-t`*`...>`

where *`env-t`* is the pack
`decltype(`*`let-cpo`*`.transform_env(declval<Sndr>(), declval<Env>()))`.

`\exposid{impls-for}<\exposid{decayed-typeof}<\exposid{let-cpo}>>::\exposid{get-state}`

is initialized with a callable object equivalent to the following:

``` cpp
[]<class Sndr, class Rcvr>(Sndr&& sndr, Rcvr& rcvr) requires see below {
  auto& [_, fn, child] = sndr;
  using fn_t = decay_t<decltype(fn)>;
  using env_t = decltype(let-env(child));
  using args_variant_t = see below;
  using ops2_variant_t = see below;

  struct state-type {
    fn_t fn;                    // exposition only
    env_t env;                  // exposition only
    args_variant_t args;        // exposition only
    ops2_variant_t ops2;        // exposition only
  };
  return state-type{allocator-aware-forward(std::forward_like<Sndr>(fn), rcvr),
                    let-env(child), {}, {}};
}
```

Let `Sigs` be a pack of the arguments to the `completion_signatures`
specialization named by
`completion_signatures_of_t<child-type<Sndr>, FWD-ENV-T(env_of_t<Rcvr>)>`.
Let `LetSigs` be a pack of those types in `Sigs` with a return type of
`decayed-typeof<set-cpo>`. Let *`as-tuple`* be an alias template such
that `as-tuple<Tag(Args...)>` denotes the type `decayed-tuple<Args...>`.
Then `args_variant_t` denotes the type
`variant<monostate, as-tuple<LetSigs>...>` except with duplicate types
removed.

Given a type `Tag` and a pack `Args`, let *`as-sndr2`* be an alias
template such that `as-sndr2<Tag(Args...)>` denotes the type
`call-result-t<F, decay_t<Args>&...>`. Then `ops2_variant_t` denotes the
type

``` cpp
variant<monostate, connect_result_t<as-sndr2<LetSigs>, receiver2<Rcvr, env_t>>...>
```

except with duplicate types removed.

The *requires-clause* constraining the above lambda is satisfied if and
only if the types `args_variant_t` and `ops2_variant_t` are well-formed.

The exposition-only function template *`let-bind`* has effects
equivalent to:

``` cpp
using args_t = decayed-tuple<Args...>;
auto mkop2 = [&] {
  return connect(
    apply(std::move(state.fn),
          state.args.template emplace<args_t>(std::forward<Args>(args)...)),
    receiver2{rcvr, std::move(state.env)});
};
start(state.ops2.template emplace<decltype(mkop2())>(emplace-from{mkop2}));
```

`\exposid{impls-for}<\exposid{decayed-typeof}<let-cpo>>::\exposid{complete}`

is initialized with a callable object equivalent to the following:

``` cpp
[]<class Tag, class... Args>
  (auto, auto& state, auto& rcvr, Tag, Args&&... args) noexcept -> void {
    if constexpr (same_as<Tag, decayed-typeof<set-cpo>>) {
      TRY-EVAL(rcvr, let-bind(state, rcvr, std::forward<Args>(args)...));
    } else {
      Tag()(std::move(rcvr), std::forward<Args>(args)...);
    }
  }
```

Let `sndr` and `env` be subexpressions, and let `Sndr` be
`decltype((sndr))`. If `sender-for<Sndr, decayed-typeof<let-cpo>>` is
`false`, then the expression `let-cpo.transform_env(sndr, env)` is
ill-formed. Otherwise, it is equal to:

``` cpp
auto& [_, _, child] = sndr;
return JOIN-ENV(let-env(child), FWD-ENV(env));
```

Let the subexpression `out_sndr` denote the result of the invocation
`let-cpo(sndr, f)` or an object equal to such, and let the subexpression
`rcvr` denote a receiver such that the expression
`connect(out_sndr, rcvr)` is well-formed. The expression
`connect(out_sndr, rcvr)` has undefined behavior unless it creates an
asynchronous operation [[exec.async.ops]] that, when started:

- invokes `f` when *`set-cpo`* is called with `sndr`’s result datums,
- makes its completion dependent on the completion of a sender returned
  by `f`, and
- propagates the other completion operations sent by `sndr`.

#### `execution::bulk`, `execution::bulk_chunked`, and `execution::bulk_unchunked` <a id="exec.bulk">[[exec.bulk]]</a>

`bulk`, `bulk_chunked`, and `bulk_unchunked` run a task repeatedly for
every index in an index space.

The names `bulk`, `bulk_chunked`, and `bulk_unchunked` denote pipeable
sender adaptor objects. Let `bulk-algo` be either `bulk`,
`bulk_chunked`, or `bulk_unchunked`. For subexpressions `sndr`,
`policy`, `shape`, and `f`, let `Policy` be
`remove_cvref_t<decltype(policy)>`, `Shape` be `decltype(auto(shape))`,
and `Func` be `decay_t<decltype((f))>`. If

- `decltype((sndr))` does not satisfy `sender`, or
- `is_execution_policy_v<Policy>` is `false`, or
- `Shape` does not satisfy `integral`, or
- `Func` does not model `copy_constructible`,

`bulk-algo(sndr, policy, shape, f)` is ill-formed.

Otherwise, the expression `bulk-algo(sndr, policy, shape, f)` is
expression-equivalent to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(
    bulk-algo, product-type<see below, Shape, Func>{policy, shape, f}, sndr))
```

except that `sndr` is evaluated only once. The first template argument
of *`product-type`* is `Policy` if `Policy` models `copy_constructible`,
and `const Policy&` otherwise.

Let `sndr` and `env` be subexpressions such that `Sndr` is
`decltype((sndr))`. If `sender-for<Sndr, bulk_t>` is `false`, then the
expression `bulk.transform_sender(sndr, env)` is ill-formed; otherwise,
it is equivalent to:

``` cpp
auto [_, data, child] = sndr;
auto& [policy, shape, f] = data;
auto new_f = [func = std::move(f)](Shape begin, Shape end, auto&&... vs)
    noexcept(noexcept(f(begin, vs...))) {
  while (begin != end) func(begin++, vs...);
}
return bulk_chunked(std::move(child), policy, shape, std::move(new_f));
```

[*Note 1*: This causes the `bulk(sndr, policy, shape, f)` sender to be
expressed in terms of `bulk_chunked(sndr, policy, shape, f)` when it is
connected to a receiver whose execution domain does not customize
`bulk`. — *end note*]

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `bulk_chunked_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<bulk_chunked_t> : default-impls {
    static constexpr auto complete = see below;

    template<class Sndr, class... Env>
      static consteval void check-types();
  };
}
```

The member `impls-for<bulk_chunked_t>::complete` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class Index, class State, class Rcvr, class Tag, class... Args>
  (Index, State& state, Rcvr& rcvr, Tag, Args&&... args) noexcept
  -> void requires see below {
    if constexpr (same_as<Tag, set_value_t>) {
      auto& [policy, shape, f] = state;
      constexpr bool nothrow = noexcept(f(auto(shape), auto(shape), args...));
      TRY-EVAL(rcvr, [&]() noexcept(nothrow) {
        f(static_cast<decltype(auto(shape))>(0), auto(shape), args...);
        Tag()(std::move(rcvr), std::forward<Args>(args)...);
      }());
    } else {
      Tag()(std::move(rcvr), std::forward<Args>(args)...);
    }
  }
```

The expression in the *requires-clause* of the lambda above is `true` if
and only if `Tag` denotes a type other than `set_value_t` or if the
expression `f(auto(shape), auto(shape), args...)` is well-formed.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `bulk_unchunked_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<bulk_unchunked_t> : default-impls {
    static constexpr auto complete = see below;
  };
}
```

The member `impls-for<bulk_unchunked_t>::complete` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class Index, class State, class Rcvr, class Tag, class... Args>
  (Index, State& state, Rcvr& rcvr, Tag, Args&&... args) noexcept
  -> void requires see below {
    if constexpr (same_as<Tag, set_value_t>) {
      auto& [policy, shape, f] = state;
      constexpr bool nothrow = noexcept(f(auto(shape), args...));
      TRY-EVAL(rcvr, [&]() noexcept(nothrow) {
        for (decltype(auto(shape)) i = 0; i < shape; ++i) {
          f(auto(i), args...);
        }
        Tag()(std::move(rcvr), std::forward<Args>(args)...);
      }());
    } else {
      Tag()(std::move(rcvr), std::forward<Args>(args)...);
    }
  }
```

The expression in the *requires-clause* of the lambda above is `true` if
and only if `Tag` denotes a type other than `set_value_t` or if the
expression `f(auto(shape), args...)` is well-formed.

``` cpp
template<class Sndr, class... Env>
  static consteval void check-types();
```

*Effects:* Equivalent to:

``` cpp
auto cs = get_completion_signatures<child-type<Sndr>, FWD-ENV-T(Env)...>();
auto fn = []<class... Ts>(set_value_t(*)(Ts...)) {
  if constexpr (!invocable<remove_cvref_t<data-type<Sndr>>, Ts&...>)
    throw unspecified-exception();
};
cs.for-each(overload-set(fn, [](auto){}));
```

where *`unspecified-exception`* is a type derived from `exception`.

Let the subexpression `out_sndr` denote the result of the invocation
`bulk-algo(sndr, policy, shape, f)` or an object equal to such, and let
the subexpression `rcvr` denote a receiver such that the expression
`connect(out_sndr, rcvr)` is well-formed. The expression
`connect(out_sndr, rcvr)` has undefined behavior unless it creates an
asynchronous operation [[exec.async.ops]] that, when started:

- If `sndr` has a successful completion, where `args` is a pack of
  lvalue subexpressions referring to the value completion result datums
  of `sndr`, or decayed copies of those values if they model
  `copy_constructible`, then:
  - If `out_sndr` also completes successfully, then:
    - for `bulk`, invokes `f(i, args...)` for every i of type `Shape`
      from `0` to `shape`;
    - for `bulk_unchunked`, invokes `f(i, args...)` for every i of type
      `Shape` from `0` to `shape`; *Recommended practice:* The
      underlying scheduler should execute each iteration on a distinct
      execution agent.
    - for `bulk_chunked`, invokes `f(b, e, args...)` zero or more times
      with pairs of b and e of type `Shape` in range \[`0`, `shape`\],
      such that b < e and for every i of type `Shape` from `0` to
      `shape`, there is exactly one invocation with a pair b and e, such
      that i is in the range \[b, e).
  - If `out_sndr` completes with `set_error(rcvr, eptr)`, then the
    asynchronous operation may invoke a subset of the invocations of `f`
    before the error completion handler is called, and `eptr` is an
    `exception_ptr` containing either:
    - an exception thrown by an invocation of `f`, or
    - a `bad_alloc` exception if the implementation fails to allocate
      required resources, or
    - an exception derived from `runtime_error`.
  - If `out_sndr` completes with `set_stopped(rcvr)`, then the
    asynchronous operation may invoke a subset of the invocations of `f`
    before the stopped completion handler.
- If `sndr` does not complete with `set_value`, then the completion is
  forwarded to `recv`.
- For `bulk-algo`, the parameter `policy` describes the manner in which
  the execution of the asynchronous operations corresponding to these
  algorithms may be parallelized and the manner in which they apply `f`.
  Permissions and requirements on parallel algorithm element access
  functions [[algorithms.parallel.exec]] apply to `f`.

[*Note 2*: The asynchronous operation corresponding to
`bulk-algo(sndr, policy, shape, f)` can complete with `set_stopped` if
cancellation is requested or ignore cancellation
requests. — *end note*]

#### `execution::when_all` <a id="exec.when.all">[[exec.when.all]]</a>

`when_all` and `when_all_with_variant` both adapt multiple input senders
into a sender that completes when all input senders have completed.
`when_all` only accepts senders with a single value completion signature
and on success concatenates all the input senders’ value result datums
into its own value completion operation.
`when_all_with_variant(sndrs...)` is semantically equivalent to
w`hen_all(into_variant(sndrs)...)`, where `sndrs` is a pack of
subexpressions whose types model `sender`.

The names `when_all` and `when_all_with_variant` denote customization
point objects. Let `sndrs` be a pack of subexpressions, let `Sndrs` be a
pack of the types `decltype((sndrs))...`, and let `CD` be the type
`common_type_t<decltype(get-domain-early(sndrs))...>`. Let `CD2` be `CD`
if `CD` is well-formed, and `default_domain` otherwise. The expressions
`when_all(sndrs...)` and `when_all_with_variant(sndrs...)` are
ill-formed if any of the following is `true`:

- `sizeof...(sndrs)` is `0`, or
- `(sender<Sndrs> && ...)` is `false`.

The expression `when_all(sndrs...)` is expression-equivalent to:

``` cpp
transform_sender(CD2(), make-sender(when_all, {}, sndrs...))
```

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `when_all_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<when_all_t> : default-impls {
    static constexpr auto get-attrs = see below;
    static constexpr auto get-env = see below;
    static constexpr auto get-state = see below;
    static constexpr auto start = see below;
    static constexpr auto complete = see below;

    template<class Sndr, class... Env>
      static consteval void check-types();
  };
}
```

Let *`make-when-all-env`* be the following exposition-only function
template:

``` cpp
template<class Env>
  constexpr auto make-when-all-env(inplace_stop_source& stop_src,               // exposition only
                                   Env&& env) noexcept {
  return see below;
}
```

Returns an object `e` such that

- `decltype(e)` models `queryable`, and
- `e.query(get_stop_token)` is expression-equivalent to
  `state.stop-src.get_token()`, and
- given a query object `q` with type other than cv `get_stop_token_t`
  and whose type satisfies *`forwarding-query`*, `e.query(q)` is
  expression-equivalent to `get_env(rcvr).query(q)`.

Let `when-all-env` be an alias template such that `when-all-env<Env>`
denotes the type
`decltype(make-{when-all-env}(declval<inplace_stop_source&>(), declval<Env>()))`.

``` cpp
template<class Sndr, class... Env>
  static consteval void check-types();
```

Let `Is` be the pack of integral template arguments of the
`integer_sequence` specialization denoted by *`indices-for`*`<Sndr>`.

*Effects:* Equivalent to:

``` cpp
auto fn = []<class Child>() {
  auto cs = get_completion_signatures<Child, when-all-env<Env>...>();
  if constexpr (cs.count-of(set_value) >= 2)
    throw unspecified-exception();
  decay-copyable-result-datums(cs); // see REF:exec.snd.expos
};
(fn.template operator()<child-type<Sndr, Is>>(), ...);
```

where *`unspecified-exception`* is a type derived from `exception`.

*Throws:* Any exception thrown as a result of evaluating the *Effects*,
or an exception of an unspecified type derived from `exception` when
`CD` is ill-formed.

The member `impls-for<when_all_t>::get-attrs` is initialized with a
callable object equivalent to the following lambda expression:

``` cpp
[](auto&&, auto&&... child) noexcept {
  if constexpr (same_as<CD, default_domain>) {
    return env<>();
  } else {
    return MAKE-ENV(get_domain, CD());
  }
}
```

The member `impls-for<when_all_t>::get-env` is initialized with a
callable object equivalent to the following lambda expression:

``` cpp
[]<class State, class Rcvr>(auto&&, State& state, const Receiver& rcvr) noexcept {
  return make-when-all-env(state.stop-src, get_env(rcvr));
}
```

The member `impls-for<when_all_t>::get-state` is initialized with a
callable object equivalent to the following lambda expression:

``` cpp
[]<class Sndr, class Rcvr>(Sndr&& sndr, Rcvr& rcvr) noexcept(noexcept(e)) -> decltype(e) {
  return e;
}
```

where e is the expression

``` cpp
std::forward<Sndr>(sndr).apply(make-state<Rcvr>())
```

and where *`make-state`* is the following exposition-only class
template:

``` cpp
enum class disposition { started, error, stopped };             // exposition only

template<class Rcvr>
struct make-state {
  template<class... Sndrs>
  auto operator()(auto, auto, Sndrs&&... sndrs) const {
    using values_tuple = see below;
    using errors_variant = see below;
    using stop_callback = stop_callback_for_t<stop_token_of_t<env_of_t<Rcvr>>, on-stop-request>;

    struct state-type {
      void arrive(Rcvr& rcvr) noexcept {                        // exposition only
        if (0 == --count) {
          complete(rcvr);
        }
      }

      void complete(Rcvr& rcvr) noexcept;                       // exposition only

      atomic<size_t> count{sizeof...(sndrs)};                   // exposition only
      inplace_stop_source stop_src{};                           // exposition only
      atomic<disposition> disp{disposition::started};           // exposition only
      errors_variant errors{};                                  // exposition only
      values_tuple values{};                                    // exposition only
      optional<stop_callback> on_stop{nullopt};                 // exposition only
    };

    return state-type{};
  }
};
```

Let *`copy-fail`* be `exception_ptr` if decay-copying any of the child
senders’ result datums can potentially throw; otherwise, `none-such`,
where `none-such` is an unspecified empty class type.

The alias `values_tuple` denotes the type

``` cpp
tuple<value_types_of_t<Sndrs, FWD-ENV-T(env_of_t<Rcvr>), decayed-tuple, optional>...>
```

if that type is well-formed; otherwise, `tuple<>`.

The alias `errors_variant` denotes the type
`variant<none-such, copy-fail, Es...>` with duplicate types removed,
where `Es` is the pack of the decayed types of all the child senders’
possible error result datums.

The member `void state-type::complete(Rcvr& rcvr) noexcept` behaves as
follows:

- If `disp` is equal to `disposition::started`, evaluates:
  ``` cpp
  auto tie = []<class... T>(tuple<T...>& t) noexcept { return tuple<T&...>(t); };
  auto set = [&](auto&... t) noexcept { set_value(std::move(rcvr), std::move(t)...); };

  on_stop.reset();
  apply(
    [&](auto&... opts) noexcept {
      apply(set, tuple_cat(tie(*opts)...));
    },
    values);
  ```
- Otherwise, if `disp` is equal to `disposition::error`, evaluates:
  ``` cpp
  on_stop.reset();
  visit(
    [&]<class Error>(Error& error) noexcept {
      if constexpr (!same_as<Error, none-such>) {
        set_error(std::move(rcvr), std::move(error));
      }
    },
    errors);
  ```
- Otherwise, evaluates:
  ``` cpp
  on_stop.reset();
  set_stopped(std::move(rcvr));
  ```

The member `impls-for<when_all_t>::start` is initialized with a callable
object equivalent to the following lambda expression:

``` cpp
[]<class State, class Rcvr, class... Ops>(
    State& state, Rcvr& rcvr, Ops&... ops) noexcept -> void {
  state.on_stop.emplace(
    get_stop_token(get_env(rcvr)),
    on-stop-request{state.stop_src});
  if (state.stop_src.stop_requested()) {
    state.on_stop.reset();
    set_stopped(std::move(rcvr));
  } else {
    (start(ops), ...);
  }
}
```

The member `impls-for<when_all_t>::complete` is initialized with a
callable object equivalent to the following lambda expression:

``` cpp
[]<class Index, class State, class Rcvr, class Set, class... Args>(
    this auto& complete, Index, State& state, Rcvr& rcvr, Set, Args&&... args) noexcept -> void {
  if constexpr (same_as<Set, set_error_t>) {
    if (disposition::error != state.disp.exchange(disposition::error)) {
      state.stop_src.request_stop();
      TRY-EMPLACE-ERROR(state.errors, std::forward<Args>(args)...);
    }
  } else if constexpr (same_as<Set, set_stopped_t>) {
    auto expected = disposition::started;
    if (state.disp.compare_exchange_strong(expected, disposition::stopped)) {
      state.stop_src.request_stop();
    }
  } else if constexpr (!same_as<decltype(State::values), tuple<>>) {
    if (state.disp == disposition::started) {
      auto& opt = get<Index::value>(state.values);
      TRY-EMPLACE-VALUE(complete, opt, std::forward<Args>(args)...);
    }
  }
  state.arrive(rcvr);
}
```

where `TRY-EMPLACE-ERROR(v, e)`, for subexpressions `v` and `e`, is
equivalent to:

``` cpp
try {
  v.template emplace<decltype(auto(e))>(e);
} catch (...) {
  v.template emplace<exception_ptr>(current_exception());
}
```

if the expression `decltype(auto(e))(e)` is potentially throwing;
otherwise, `v.template emplace<decltype(auto(e))>(e)`; and where
`TRY-EMPLACE-VALUE(c, o, as...)`, for subexpressions `c`, `o`, and pack
of subexpressions `as`, is equivalent to:

``` cpp
try {
  o.emplace(as...);
} catch (...) {
  c(Index(), state, rcvr, set_error, current_exception());
  return;
}
```

if the expression `decayed-tuple<decltype(as)...>{as...}` is potentially
throwing; otherwise, `o.emplace(as...)`.

The expression `when_all_with_variant(sndrs...)` is
expression-equivalent to:

``` cpp
transform_sender(CD2(), make-sender(when_all_with_variant, {}, sndrs...));
```

Given subexpressions `sndr` and `env`, if
`sender-for<decltype((sndr)), when_all_with_variant_t>` is `false`, then
the expression `when_all_with_variant.transform_sender(sndr, env)` is
ill-formed; otherwise, it is equivalent to:

``` cpp
auto&& [_, _, ...child] = sndr;
return when_all(into_variant(std::forward_like<decltype((sndr))>(child))...);
```

[*Note 1*: This causes the `when_all_with_variant(sndrs...)` sender to
become `when_all(into_variant(sndrs)...)` when it is connected with a
receiver whose execution domain does not customize
`when_all_with_variant`. — *end note*]

#### `execution::into_variant` <a id="exec.into.variant">[[exec.into.variant]]</a>

`into_variant` adapts a sender with multiple value completion signatures
into a sender with just one value completion signature consisting of a
`variant` of `tuple`s.

The name `into_variant` denotes a pipeable sender adaptor object. For a
subexpression `sndr`, let `Sndr` be `decltype((sndr))`. If `Sndr` does
not satisfy `sender`, `into_variant(sndr)` is ill-formed.

Otherwise, the expression `into_variant(sndr)` is expression-equivalent
to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(into_variant, {}, sndr))
```

except that `sndr` is only evaluated once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `into_variant` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<into_variant_t> : default-impls {
    static constexpr auto get-state = see below;
    static constexpr auto complete = see below;

    template<class Sndr, class... Env>
      static consteval void check-types() {
        auto cs = get_completion_signatures<child-type<Sndr>, FWD-ENV-T(Env)...>();
        decay-copyable-result-datums(cs);   // see [exec.snd.expos]
      }
  };
}
```

The member `impls-for<into_variant_t>::get-state` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class Sndr, class Rcvr>(Sndr&& sndr, Rcvr& rcvr) noexcept
  -> type_identity<value_types_of_t<child-type<Sndr>, FWD-ENV-T(env_of_t<Rcvr>)>> {
  return {};
}
```

The member `impls-for<into_variant_t>::complete` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class State, class Rcvr, class Tag, class... Args>(
    auto, State, Rcvr& rcvr, Tag, Args&&... args) noexcept -> void {
  if constexpr (same_as<Tag, set_value_t>) {
    using variant_type = State::type;
    TRY-SET-VALUE(rcvr, variant_type(decayed-tuple<Args...>{std::forward<Args>(args)...}));
  } else {
    Tag()(std::move(rcvr), std::forward<Args>(args)...);
  }
}
```

#### `execution::stopped_as_optional` <a id="exec.stopped.opt">[[exec.stopped.opt]]</a>

`stopped_as_optional` maps a sender’s stopped completion operation into
a value completion operation as a disengaged `optional`. The sender’s
value completion operation is also converted into an `optional`. The
result is a sender that never completes with stopped, reporting
cancellation by completing with a disengaged `optional`.

The name `stopped_as_optional` denotes a pipeable sender adaptor object.
For a subexpression `sndr`, let `Sndr` be `decltype((sndr))`. The
expression `stopped_as_optional(sndr)` is expression-equivalent to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(stopped_as_optional, {}, sndr))
```

except that `sndr` is only evaluated once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `stopped_as_optional_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<stopped_as_optional_t> : default-impls {
    template<class Sndr, class... Env>
      static consteval void check-types() {
        default-impls::check-types<Sndr, Env...>();
        if constexpr (!requires {
          requires (!same_as<void, single-sender-value-type<child-type<Sndr>,
                                                            FWD-ENV-T(Env)...>>); })
          throw unspecified-exception();
      }
  };
}
```

where `unspecified-exception` is a type derived from `exception`.

Let `sndr` and `env` be subexpressions such that `Sndr` is
`decltype((sndr))` and `Env` is `decltype((env))`. If
`sender-for<Sndr, stopped_as_optional_t>` is `false` then the expression
`stopped_as_optional.transform_sender(sndr, env)` is ill-formed;
otherwise, if `sender_in<child-type<Sndr>, FWD-ENV-T(Env)>` is `false`,
the expression `stopped_as_optional.transform_sender(sndr, env)` is
equivalent to `not-a-sender()`; otherwise, it is equivalent to:

``` cpp
auto&& [_, _, child] = sndr;
using V = single-sender-value-type<child-type<Sndr>, FWD-ENV-T(Env)>;
return let_stopped(
  then(std::forward_like<Sndr>(child),
       []<class... Ts>(Ts&&... ts) noexcept(is_nothrow_constructible_v<V, Ts...>) {
         return optional<V>(in_place, std::forward<Ts>(ts)...);
       }),
  []() noexcept { return just(optional<V>()); });
```

#### `execution::stopped_as_error` <a id="exec.stopped.err">[[exec.stopped.err]]</a>

`stopped_as_error` maps an input sender’s stopped completion operation
into an error completion operation as a custom error type. The result is
a sender that never completes with stopped, reporting cancellation by
completing with an error.

The name `stopped_as_error` denotes a pipeable sender adaptor object.
For some subexpressions `sndr` and `err`, let `Sndr` be
`decltype((sndr))` and let `Err` be `decltype((err))`. If the type
`Sndr` does not satisfy `sender` or if the type `Err` does not satisfy
`movable-value`, `stopped_as_error(sndr, err)` is ill-formed. Otherwise,
the expression `stopped_as_error(sndr, err)` is expression-equivalent
to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(stopped_as_error, err, sndr))
```

except that `sndr` is only evaluated once.

Let `sndr` and `env` be subexpressions such that `Sndr` is
`decltype((sndr))` and `Env` is `decltype((env))`. If
`sender-for<Sndr, stopped_as_error_t>` is `false`, then the expression
`stopped_as_error.transform_sender(sndr, env)` is ill-formed; otherwise,
it is equivalent to:

``` cpp
auto&& [_, err, child] = sndr;
using E = decltype(auto(err));
return let_stopped(
  std::forward_like<Sndr>(child),
  [err = std::forward_like<Sndr>(err)]() mutable noexcept(is_nothrow_move_constructible_v<E>) {
    return just_error(std::move(err));
  });
```

#### `execution::associate` <a id="exec.associate">[[exec.associate]]</a>

`associate` tries to associate a sender with an async scope such that
the scope can track the lifetime of any asynchronous operations created
with the sender.

Let *`associate-data`* be the following exposition-only class template:

``` cpp
namespace std::execution {
  template<scope_token Token, sender Sender>
  struct associate-data {                                       // exposition only
    using wrap-sender =                                         // exposition only
      remove_cvref_t<decltype(declval<Token&>().wrap(declval<Sender>()))>;

    explicit associate-data(Token t, Sender&& s)
      : sndr(t.wrap(std::forward<Sender>(s))),
        token(t) {
      if (!token.try_associate())
        sndr.reset();
    }

    associate-data(const associate-data& other)
      noexcept(is_nothrow_copy_constructible_v<wrap-sender> &&
               noexcept(other.token.try_associate()));

    associate-data(associate-data&& other)
      noexcept(is_nothrow_move_constructible_v<wrap-sender>);

    ~associate-data();

    optional<pair<Token, wrap-sender>>
      release() && noexcept(is_nothrow_move_constructible_v<wrap-sender>);

  private:
    optional<wrap-sender> sndr;  // exposition only
    Token token;                 // exposition only
  };

  template<scope_token Token, sender Sender>
    associate-data(Token, Sender&&) -> associate-data<Token, Sender>;
}
```

For an *`associate-data`* object `a`, `a.sndr.has_value()` is `true` if
and only if an association was successfully made and is owned by `a`.

``` cpp
associate-data(const associate-data& other)
  noexcept(is_nothrow_copy_constructible_v<wrap-sender> &&
           noexcept(other.token.try_associate()));
```

*Constraints:* `copy_constructible<`*`wrap-sender`*`>` is `true`.

*Effects:* Value-initializes *sndr* and initializes *token* with
`other.`*`token`*. If `other.`*`sndr`*`.has_value()` is `false`, no
further effects; otherwise, calls *`token`*`.try_associate()` and, if
that returns `true`, calls *`sndr`*`.emplace(*other.`*`sndr`*`)` and, if
that exits with an exception, calls *`token`*`.disassociate()` before
propagating the exception.

``` cpp
associate-data(associate-data&& other)
  noexcept(is_nothrow_move_constructible_v<wrap-sender>);
```

*Effects:* Initializes *sndr* with `std::move(other.`*`sndr`*`)` and
initializes *token* with `std::move(other.`*`token`*`)` and then calls
`other.`*`sndr`*`.reset()`.

``` cpp
~associate-data();
```

*Effects:* If *`sndr`*`.has_value()` returns `false` then no effect;
otherwise, invokes *`sndr`*`.reset()` before invoking
*`token`*`.disassociate()`.

``` cpp
optional<pair<Token, wrap-sender>>
  release() && noexcept(is_nothrow_move_constructible_v<wrap-sender>);
```

*Effects:* If *`sndr`*`.has_value()` returns `false` then returns an
`optional` that does not contain a value; otherwise returns an
`optional` containing a value of type `pair<Token, `*`wrap-sender`*`>`
as if by:

``` cpp
return optional(pair(token, std::move(*sndr)));
```

*Ensures:* *sndr* does not contain a value.

The name `associate` denotes a pipeable sender adaptor object. For
subexpressions `sndr` and `token`:

- If `decltype((sndr))` does not satisfy `sender`, or
  `remove_cvref_t<decltype((token))>` does not satisfy `scope_token`,
  then `associate(sndr, token)` is ill-formed.
- Otherwise, the expression `associate(sndr, token)` is
  expression-equivalent to:
  ``` cpp
  transform_sender(get-domain-early(sndr),
                   make-sender(associate, associate-data(token, sndr)))
  ```

  except that `sndr` is evaluated only once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `associate_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<associate_t> : default-impls {
    static constexpr auto get-state = see below;                // exposition only
    static constexpr auto start = see below;                    // exposition only

    template<class Sndr, class... Env>
      static consteval void check-types() {                     // exposition only
        using associate_data_t = remove_cvref_t<data-type<Sndr>>;
        using child_type_t = associate_data_t::wrap-sender;
        (void)get_completion_signatures<child_type_t, FWD-ENV-T(Env)...>();
    }
  };
}
```

The member `impls-for<associate_t>::get-state` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[]<class Sndr, class Rcvr>(Sndr&& sndr, Rcvr& rcvr) noexcept(see below) {
  auto [_, data] = std::forward<Sndr>(sndr);
  auto dataParts = std::move(data).release();

  using scope_tkn = decltype(dataParts->first);
  using wrap_sender = decltype(dataParts->second);
  using op_t = connect_result_t<wrap_sender, Rcvr>;

  struct op_state {
    bool associated = false;    // exposition only
    union {
      Rcvr* rcvr;               // exposition only
      struct {
        scope_tkn token;        // exposition only
        op_t op;                // exposition only
      } assoc;                  // exposition only
    };

    explicit op_state(Rcvr& r) noexcept
      : rcvr(addressof(r)) {}

    explicit op_state(scope_tkn tkn, wrap_sender&& sndr, Rcvr& r) try
      : associated(true),
        assoc(tkn, connect(std::move(sndr), std::move(r))) {
    }
    catch (...) {
      tkn.disassociate();
      throw;
    }

    op_state(op_state&&) = delete;

    ~op_state() {
      if (associated) {
        assoc.op.~op_t();
        assoc.token.disassociate();
        assoc.token.~scope_tkn();
      }
    }

    void run() noexcept {       // exposition only
      if (associated)
        start(assoc.op);
      else
        set_stopped(std::move(*rcvr));
    }
  };

  if (dataParts)
    return op_state{std::move(dataParts->first), std::move(dataParts->second), rcvr};
  else
    return op_state{rcvr};
}
```

The expression in the `noexcept` clause of
`impls-for<associate_t>::get-state` is

``` cpp
is_nothrow_constructible_v<remove_cvref_t<Sndr>, Sndr> &&
is_nothrow_move_constructible_v<wrap-sender> &&
nothrow-callable<connect_t, wrap-sender, Rcvr>
```

where *`wrap-sender`* is the type
`remove_cvref_t<data-type<Sndr>>::wrap-sender`.

The member `impls-for<associate_t>::start` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[](auto& state, auto&) noexcept -> void {
  state.run();
}
```

The evaluation of `associate(sndr, token)` may cause side effects
observable via `token`'s associated async scope object.

#### Exposition-only `execution::stop-when` <a id="exec.stop.when">[[exec.stop.when]]</a>

*`stop-when`* fuses an additional stop token `t` into a sender so that,
upon connecting to a receiver `r`, the resulting operation state
receives stop requests from both `t` and the token returned from
`get_stop_token(get_env(r))`.

The name *`stop-when`* denotes an exposition-only sender adaptor. For
subexpressions `sndr` and `token`:

- If `decltype((sndr))` does not satisfy `sender`, or
  `remove_cvref_t<decltype((token))>` does not satisfy
  `stoppable_token`, then `stop-when(sndr, token)` is ill-formed.
- Otherwise, if `remove_cvref_t<decltype((token))>` models
  `unstoppable_token` then `stop-when({}sndr, token)` is
  expression-equivalent to `sndr`.
- Otherwise, `stop-when(sndr, token)` returns a sender `osndr`. If
  `osndr` is connected to a receiver `r`, let `rtoken` be the result of
  `get_stop_token(get_env(r))`.
  - If the type of `rtoken` models `unstoppable_token` then the effects
    of connecting `osndr` to `r` are equivalent to
    `connect(write_env(sndr, prop(get_stop_token, token)), r)`.
  - Otherwise, the effects of connecting `osndr` to `r` are equivalent
    to `connect(write_env(sndr, prop(get_stop_token, stoken)), r)` where
    `stoken` is an object of an exposition-only type *`stoken-t`* such
    that:
    - *`stoken-t`* models `stoppable_token`;
    - `stoken.stop_requested()` returns
      `token.stop_requested() || rtoken.stop_reques-{}ted()`;
    - `stoken.stop_possible()` returns
      `token.stop_possible() || rtoken.stop_possible()`; and
    - for types `Fn` and `Init` such that both `invocable<Fn>` and
      `constructible_from<Fn, Init>` are modeled,
      `stoken-t::callback_type<Fn>` models
      `stoppable-callback-for<Fn, stoken-t, Init>`.*`stoken-t`*

#### `execution::spawn_future` <a id="exec.spawn.future">[[exec.spawn.future]]</a>

`spawn_future` attempts to associate the given input sender with the
given token’s async scope and, on success, eagerly starts the input
sender; the return value is a sender that, when connected and started,
completes with either the result of the eagerly-started input sender or
with `set_stopped` if the input sender was not started.

The name `spawn_future` denotes a customization point object. For
subexpressions `sndr`, `token`, and `env`,

- let `Sndr` be `decltype((sndr))`,
- let `Token` be `remove_cvref_t<decltype((token))>`, and
- let `Env` be `remove_cvref_t<decltype((env))>`.

If any of `sender<Sndr>`, `scope_token<Token>`, or `queryable<Env>` are
not satisfied, the expression `spawn_future(sndr, token, env)` is
ill-formed.

Let *`spawn-future-state-base`* be the exposition-only class template:

``` cpp
namespace std::execution {
  template<class Completions>
  struct spawn-future-state-base;                                   // exposition only

  template<class... Sigs>
  struct spawn-future-state-base<completion_signatures<Sigs...>> {  // exposition only
    using variant-t = see below;                                    // exposition only
    variant-t result;                                               // exposition only
    virtual void complete() noexcept = 0;                           // exposition only
  };
}
```

Let `Sigs` be the pack of arguments to the `completion_signatures`
specialization provided as a parameter to the
*`spawn-future-state-base`* class template. Let *`as-tuple`* be an alias
template that transforms a completion signature `Tag(Args...)` into the
tuple specialization `decayed-tuple<Tag, Args...>`.

- If `is_nothrow_constructible_v<decay_t<Arg>, Arg>` is `true` for every
  type `Arg` in every parameter pack `Args` in every completion
  signature `Tag(Args...)` in `Sigs` then *`variant-t`* denotes the type
  `variant<monostate, tuple<set_stopped_t>, as-tuple<Sigs>...>`, except
  with duplicate types removed.
- Otherwise *`variant-t`* denotes the type
  `variant<monostate, tuple<set_stopped_t>, tuple<set_error_t, exception_ptr>, as-tuple<Sigs>...>`,
  except with duplicate types removed.

Let *`spawn-future-receiver`* be the exposition-only class template:

``` cpp
namespace std::execution {
  template<class Completions>
  struct spawn-future-receiver {                                // exposition only
    using receiver_concept = receiver_t;

    spawn-future-state-base<Completions>* state;                // exposition only

    template<class... T>
      void set_value(T&&... t) && noexcept {
        set-complete<set_value_t>(std::forward<T>(t)...);
      }

    template<class E>
      void set_error(E&& e) && noexcept {
        set-complete<set_error_t>(std::forward<E>(e));
      }

    void set_stopped() && noexcept {
      set-complete<set_stopped_t>();
    }

  private:
    template<class CPO, class... T>
      void set-complete(T&&... t) noexcept {                    // exposition only
        constexpr bool nothrow = (is_nothrow_constructible_v<decay_t<T>, T> && ...);
        try {
          state->result.template emplace<decayed-tuple<CPO, T...>>(CPO{},
                                                                   std::forward<T>(t)...);
        }
        catch (...) {
          if constexpr (!nothrow) {
            using tuple_t = decayed-tuple<set_error_t, exception_ptr>;
            state->result.template emplace<tuple_t>(set_error_t{}, current_exception());
          }
        }
        state->complete();
      }
  };
}
```

Let `ssource-t` be an unspecified type that models `stoppable-source`
and let `ssource` be an lvalue of type `ssource-t`. Let `stoken-t` be
`decltype(ssource.get_token())`. Let *`future-spawned-sender`* be the
alias template:

``` cpp
template<sender Sender, class Env>
using future-spawned-sender =                                   // exposition only
  decltype(write_env(stop-when(declval<Sender>(), declval<stoken-t>()), declval<Env>()));
```

Let *`spawn-future-state`* be the exposition-only class template:

``` cpp
namespace std::execution {
  template<class Alloc, scope_token Token, sender Sender, class Env>
  struct spawn-future-state                                                 // exposition only
    : spawn-future-state-base<completion_signatures_of_t<future-spawned-sender<Sender, Env>>> {
    using sigs-t =                                                          // exposition only
      completion_signatures_of_t<future-spawned-sender<Sender, Env>>;
    using receiver-t =                                                      // exposition only
      spawn-future-receiver<sigs-t>;
    using op-t =                                                            // exposition only
      connect_result_t<future-spawned-sender<Sender, Env>, receiver-t>;

    spawn-future-state(Alloc alloc, Sender&& sndr, Token token, Env env)    // exposition only
      : alloc(std::move(alloc)),
        op(connect(
          write_env(stop-when(std::forward<Sender>(sndr), ssource.get_token()), std::move(env)),
          receiver-t(this))),
        token(std::move(token)),
        associated(token.try_associate()) {
          if (associated)
            start(op);
          else
            set_stopped(receiver-t(this));
        }

    void complete() noexcept override;                                      // exposition only
    void consume(receiver auto& rcvr) noexcept;                             // exposition only
    void abandon() noexcept;                                                // exposition only

  private:
    using alloc-t =                                                         // exposition only
      allocator_traits<Alloc>::template rebind_alloc<spawn-future-state>;

    alloc-t alloc;                                                          // exposition only
    ssource-t ssource;                                                      // exposition only
    op-t op;                                                                // exposition only
    Token token;                                                            // exposition only
    bool associated;                                                        // exposition only

    void destroy() noexcept;                                                // exposition only
  };
}
```

For purposes of determining the existence of a data race, *`complete`*,
*`consume`*, and *`abandon`* behave as atomic operations
[[intro.multithread]]. These operations on a single object of a type
that is a specialization of *`spawn-future-state`* appear to occur in a
single total order.

``` cpp
void complete() noexcept;
```

*Effects:*

- No effects if this invocation of *complete* happens before an
  invocation of *consume* or *abandon* on `*this`;
- otherwise, if an invocation of *consume* on `*this` happens before
  this invocation of *complete* then there is a receiver, `rcvr`,
  registered and that receiver is completed as if by
  *`consume`*`(rcvr)`;
- otherwise, *destroy* is invoked.

``` cpp
void consume(receiver auto& rcvr) noexcept;
```

*Effects:*

- If this invocation of *consume* happens before an invocation of
  *complete* on `*this` then `rcvr` is registered to be completed when
  *complete* is subsequently invoked on `*this`;
- otherwise, `rcvr` is completed as if by:
  ``` cpp
  std::move(this->result).visit(
    [&rcvr](auto&& tuple) noexcept {
      if constexpr (!same_as<remove_reference_t<decltype(tuple)>, monostate>) {
        apply([&rcvr](auto cpo, auto&&... vals) {
          cpo(std::move(rcvr), std::move(vals)...);
        }, std::move(tuple));
      }
    });
  ```

``` cpp
void abandon() noexcept;
```

*Effects:*

- If this invocation of *abandon* happens before an invocation of
  *complete* on `*this` then equivalent to:
  ``` cpp
  ssource.request_stop();
  ```
- otherwise, *destroy* is invoked.

``` cpp
void destroy() noexcept;
```

*Effects:* Equivalent to:

``` cpp
auto token = std::move(this->token);
bool associated = this->associated;

{
  auto alloc = std::move(this->alloc);

  allocator_traits<alloc-t>::destroy(alloc, this);
  allocator_traits<alloc-t>::deallocate(alloc, this, 1);
}

if (associated)
  token.disassociate();
```

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `spawn_future_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<spawn_future_t> : default-impls {
    static constexpr auto start = see below;                    // exposition only
  };
}
```

The member `impls-for<spawn_future_t>::start` is initialized with a
callable object equivalent to the following lambda:

``` cpp
[](auto& state, auto& rcvr) noexcept -> void {
  state->consume(rcvr);
}
```

For the expression `spawn_future(sndr, token, env)` let `new_sender` be
the expression `token.wrap(sndr)` and let `alloc` and `senv` be defined
as follows:

- if the expression `get_allocator(env)` is well-formed, then `alloc` is
  the result of `get_allocator(env)` and `senv` is the expression `env`;
- otherwise, if the expression `get_allocator(get_env(new_sender))` is
  well-formed, then `alloc` is the result of
  `get_allocator(get_env(new_sender))` and `senv` is the expression
  `JOIN-ENV(prop(get_allocator, alloc), env)`;
- otherwise, `alloc` is `allocator<void>()` and `senv` is the expression
  `env`.

The expression `spawn_future(sndr, token, env)` has the following
effects:

- Uses `alloc` to allocate and construct an object `s` of a type that is
  a specialization of *`spawn-future-{`* from `alloc`,
  `token.wrap(sndr)`, `token`, and `senv`. If an exception is thrown
  then any constructed objects are destroyed and any allocated memory is
  deallocated.
- Constructs an object `u` of a type that is a specialization of
  `unique_ptr` such that:
  - `u.get()` is equal to the address of `s`, and
  - `u.get_deleter()(u.release())` is equivalent to
    `u.release()->abandon()`.
- Returns `make-sender(spawn_future, std::move(u))`.

The expression `spawn_future(sndr, token)` is expression-equivalent to
`spawn_future(sndr, token, execution::env<>())`.

### Sender consumers <a id="exec.consumers">[[exec.consumers]]</a>

#### `this_thread::sync_wait` <a id="exec.sync.wait">[[exec.sync.wait]]</a>

`this_thread::sync_wait` and `this_thread::sync_wait_with_variant` are
used to block the current thread of execution until the specified sender
completes and to return its async result. `sync_wait` mandates that the
input sender has exactly one value completion signature.

Let *`sync-wait-env`* be the following exposition-only class type:

``` cpp
namespace std::this_thread {
  struct sync-wait-env {
    execution::run_loop* loop;                                  // exposition only

    auto query(execution::get_scheduler_t) const noexcept {
      return loop->get_scheduler();
    }

    auto query(execution::get_delegation_scheduler_t) const noexcept {
      return loop->get_scheduler();
    }
  };
}
```

Let *`sync-wait-result-type`* and *`sync-wait-with-variant-result-type`*
be exposition-only alias templates defined as follows:

``` cpp
namespace std::this_thread {
  template<execution::sender_in<sync-wait-env> Sndr>
    using sync-wait-result-type =
      optional<execution::value_types_of_t<Sndr, sync-wait-env, decayed-tuple,
               type_identity_t>>;

  template<execution::sender_in<sync-wait-env> Sndr>
    using sync-wait-with-variant-result-type =
      optional<execution::value_types_of_t<Sndr, sync-wait-env>>;
}
```

The name `this_thread::sync_wait` denotes a customization point object.
For a subexpression `sndr`, let `Sndr` be `decltype((sndr))`. The
expression `this_thread::sync_wait(sndr)` is expression-equivalent to
the following, except that `sndr` is evaluated only once:

``` cpp
apply_sender(get-domain-early(sndr), sync_wait, sndr)
```

*Mandates:*

- `sender_in<Sndr, sync-wait-env>` is `true`.
- The type `sync-wait-result-type<Sndr>` is well-formed.
- `same_as<decltype(e), sync-wait-result-type<Sndr>>` is `true`, where e
  is the `apply_sender` expression above.

Let *`sync-wait-state`* and *`sync-wait-receiver`* be the following
exposition-only class templates:

``` cpp
namespace std::this_thread {
  template<class Sndr>
  struct sync-wait-state {                                      // exposition only
    execution::run_loop loop;                                   // exposition only
    exception_ptr error;                                        // exposition only
    sync-wait-result-type<Sndr> result;                         // exposition only
  };

  template<class Sndr>
  struct sync-wait-receiver {                                   // exposition only
    using receiver_concept = execution::receiver_t;
    sync-wait-state<Sndr>* state;                               // exposition only

    template<class... Args>
    void set_value(Args&&... args) && noexcept;

    template<class Error>
    void set_error(Error&& err) && noexcept;

    void set_stopped() && noexcept;

    sync-wait-env get_env() const noexcept { return {&state->loop}; }
  };
}
```

``` cpp
template<class... Args>
void set_value(Args&&... args) && noexcept;
```

*Effects:* Equivalent to:

``` cpp
try {
  state->result.emplace(std::forward<Args>(args)...);
} catch (...) {
  state->error = current_exception();
}
state->loop.finish();
```

``` cpp
template<class Error>
void set_error(Error&& err) && noexcept;
```

*Effects:* Equivalent to:

``` cpp
state->error = AS-EXCEPT-PTR(std::forward<Error>(err));    // see REF:exec.general
state->loop.finish();
```

``` cpp
void set_stopped() && noexcept;
```

*Effects:* Equivalent to *`state`*`->`*`loop`*`.finish()`.

For a subexpression `sndr`, let `Sndr` be `decltype((sndr))`. If
`sender_to<Sndr, sync-wait-receiver<Sndr>>` is `false`, the expression
`sync_wait.apply_sender(sndr)` is ill-formed; otherwise, it is
equivalent to:

``` cpp
sync-wait-state<Sndr> state;
auto op = connect(sndr, sync-wait-receiver<Sndr>{&state});
start(op);

state.loop.run();
if (state.error) {
  rethrow_exception(std::move(state.error));
}
return std::move(state.result);
```

The behavior of `this_thread::sync_wait(sndr)` is undefined unless:

- It blocks the current thread of execution [[defns.block]] with forward
  progress guarantee delegation [[intro.progress]] until the specified
  sender completes. \[*Note 2*: The default implementation of
  `sync_wait` achieves forward progress guarantee delegation by
  providing a `run_loop` scheduler via the `get_delegation_scheduler`
  query on the *`sync-wait-receiver`*’s environment. The `run_loop` is
  driven by the current thread of execution. — *end note*]
- It returns the specified sender’s async results as follows:
  - For a value completion, the result datums are returned in a `tuple`
    in an engaged `optional` object.
  - For an error completion, an exception is thrown.
  - For a stopped completion, a disengaged `optional` object is
    returned.

#### `this_thread::sync_wait_with_variant` <a id="exec.sync.wait.var">[[exec.sync.wait.var]]</a>

The name `this_thread::sync_wait_with_variant` denotes a customization
point object. For a subexpression `sndr`, let `Sndr` be
`decltype(into_variant(sndr))`. The expression
`this_thread::sync_wait_with_variant(sndr)` is expression-equivalent to
the following, except `sndr` is evaluated only once:

``` cpp
apply_sender(get-domain-early(sndr), sync_wait_with_variant, sndr)
```

*Mandates:*

- `sender_in<Sndr, sync-wait-env>` is `true`.
- The type `sync-wait-with-variant-result-type<Sndr>` is well-formed.
- `same_as<decltype(e), sync-wait-with-variant-result-type<Sndr>>` is
  `true`, where e is the `apply_sender` expression above.

The expression `sync_wait_with_variant.apply_sender(sndr)` is equivalent
to:

``` cpp
using result_type = sync-wait-with-variant-result-type<Sndr>;
if (auto opt_value = sync_wait(into_variant(sndr))) {
  return result_type(std::move(get<0>(*opt_value)));
}
return result_type(nullopt);
```

The behavior of `this_thread::sync_wait_with_variant(sndr)` is undefined
unless:

- It blocks the current thread of execution [[defns.block]] with forward
  progress guarantee delegation [[intro.progress]] until the specified
  sender completes. \[*Note 3*: The default implementation of
  `sync_wait_with_variant` achieves forward progress guarantee
  delegation by relying on the forward progress guarantee delegation
  provided by `sync_wait`. — *end note*]
- It returns the specified sender’s async results as follows:
  - For a value completion, the result datums are returned in an engaged
    `optional` object that contains a `variant` of `tuple`s.
  - For an error completion, an exception is thrown.
  - For a stopped completion, a disengaged `optional` object is
    returned.

#### `execution::spawn` <a id="exec.spawn">[[exec.spawn]]</a>

`spawn` attempts to associate the given input sender with the given
token’s async scope and, on success, eagerly starts the input sender.

The name `spawn` denotes a customization point object. For
subexpressions `sndr`, `token`, and `env`,

- let `Sndr` be `decltype((sndr))`,
- let `Token` be `remove_cvref_t<decltype((token))>`, and
- let `Env` be `remove_cvref_t<decltype((env))>`.

If any of `sender<Sndr>`, `scope_token<Token>`, or `queryable<Env>` are
not satisfied, the expression `spawn({}sndr, token, env)` is ill-formed.

Let *`spawn-state-base`* be the exposition-only class:

``` cpp
namespace std::execution {
  struct spawn-state-base {                                 // exposition only
    virtual void complete() noexcept = 0;                   // exposition only
  };
}
```

Let *`spawn-receiver`* be the exposition-only class:

``` cpp
namespace std::execution {
  struct spawn-receiver {                                   // exposition only
    using receiver_concept = receiver_t;

    spawn-state-base* state;                                // exposition only
    void set_value() && noexcept { state->complete(); }
    void set_stopped() && noexcept { state->complete(); }
  };
}
```

Let *`spawn-state`* be the exposition-only class template:

``` cpp
namespace std::execution {
  template<class Alloc, scope_token Token, sender Sender>
  struct spawn-state : spawn-state-base {                   // exposition only
    using op-t = connect_result_t<Sender, spawn-receiver>;  // exposition only

    spawn-state(Alloc alloc, Sender&& sndr, Token token);   // exposition only
    void complete() noexcept override;                      // exposition only
    void run();                                             // exposition only

  private:
    using alloc-t =                                         // exposition only
      allocator_traits<Alloc>::template rebind_alloc<spawn-state>;

    alloc-t alloc;                                          // exposition only
    op-t op;                                                // exposition only
    Token token;                                            // exposition only

    void destroy() noexcept;                                // exposition only
  };
}
```

``` cpp
spawn-state(Alloc alloc, Sender&& sndr, Token token);
```

*Effects:* Initializes *alloc* with `alloc`, *token* with `token`, and
*op* with:

``` cpp
connect(std::move(sndr), spawn-receiver(this))
```

``` cpp
void run();
```

*Effects:* Equivalent to:

``` cpp
if (token.try_associate())
  start(op);
else
  destroy();
```

``` cpp
void complete() noexcept override;
```

*Effects:* Equivalent to:

``` cpp
auto token = std::move(this->token);

destroy();
token.disassociate();
```

``` cpp
void destroy() noexcept;
```

*Effects:* Equivalent to:

``` cpp
auto alloc = std::move(this->alloc);

allocator_traits<alloc-t>::destroy(alloc, this);
allocator_traits<alloc-t>::deallocate(alloc, this, 1);
```

For the expression `spawn(sndr, token, env)` let `new_sender` be the
expression `token.wrap(sndr)` and let `alloc` and `senv` be defined as
follows:

- if the expression `get_allocator(env)` is well-formed, then `alloc` is
  the result of `get_allocator(env)` and `senv` is the expression `env`,
- otherwise if the expression `get_allocator(get_env(new_sender))` is
  well-formed, then `alloc` is the result of
  `get_allocator(get_env(new_sender))` and `senv` is the expression
  `JOIN-ENV(prop(get_allocator, alloc), env)`,
- otherwise `alloc` is `allocator<void>()` and `senv` is the expression
  `env`.

The expression `spawn(sndr, token, env)` is of type `void` and has the
following effects:

- Uses `alloc` to allocate and construct an object `o` of type that is a
  specialization of `spawn-state` from `alloc`,
  `write_env(token.wrap(sndr), senv)`, and `token` and then invokes
  `o.run()`. If an exception is thrown then any constructed objects are
  destroyed and any allocated memory is deallocated.

The expression `spawn(sndr, token)` is expression-equivalent to
`spawn(sndr, token, execution::env<>({}))`.

## Completion signatures <a id="exec.cmplsig">[[exec.cmplsig]]</a>

`completion_signatures` is a type that encodes a set of completion
signatures [[exec.async.ops]].

[*Example 1*:

``` cpp
struct my_sender {
  using sender_concept = sender_t;
  using completion_signatures =
    execution::completion_signatures<
      set_value_t(),
      set_value_t(int, float),
      set_error_t(exception_ptr),
      set_error_t(error_code),
      set_stopped_t()>;
};
```

Declares `my_sender` to be a sender that can complete by calling one of
the following for a receiver expression `rcvr`:

- `set_value(rcvr)`
- `set_value(rcvr, int{...}, float{...})`
- `set_error(rcvr, exception_ptr{...})`
- `set_error(rcvr, error_code{...})`
- `set_stopped(rcvr)`

— *end example*]

This subclause makes use of the following exposition-only entities:

``` cpp
template<class Fn>
  concept completion-signature = see below;
```

A type `Fn` satisfies `completion-signature` if and only if it is a
function type with one of the following forms:

- `set_value_t(Vs...)`, where `Vs` is a pack of object or reference
  types.
- `set_error_t(Err)`, where `Err` is an object or reference type.
- `set_stopped_t()`

``` cpp
template<bool>
  struct indirect-meta-apply {
    template<template<class...> class T, class... As>
      using meta-apply = T<As...>;                              // exposition only
  };

template<class...>
  concept always-true = true;                                   // exposition only

template<class Tag,
         valid-completion-signatures Completions,
         template<class...> class Tuple,
         template<class...> class Variant>
  using gather-signatures = see below;
```

Let `Fns` be a pack of the arguments of the `completion_signatures`
specialization named by `Completions`, let `TagFns` be a pack of the
function types in `Fns` whose return types are `Tag`, and let `Tsₙ` be a
pack of the function argument types in the n-th type in `TagFns`. Then,
given two variadic templates `Tuple` and `Variant`, the type
`gather-signatures<Tag, Completions, Tuple, Variant>` names the type

``` cpp
META-APPLY(Variant, META-APPLY(Tuple, Ts_0...),
                    META-APPLY(Tuple, Ts_1...),
                    …,
                    META-APPLY(Tuple, Ts_{m-1}...))
```

where m is the size of the pack `TagFns` and `META-APPLY(T, As...)` is
equivalent to:

``` cpp
typename indirect-meta-apply<always-true<As...>>::template meta-apply<T, As...>
```

[*Note 1*: The purpose of *`META-APPLY`* is to make it valid to use
non-variadic templates as `Variant` and `Tuple` arguments to
*`gather-signatures`*. — *end note*]

``` cpp
namespace std::execution {
  template<completion-signature... Fns>
    struct completion_signatures {
      template<class Tag>
        static constexpr size_t count-of(Tag) { return see below; }

      template<class Fn>
        static constexpr void for-each(Fn&& fn) {               // exposition only
          (std::forward<Fn>(fn)(static_cast<Fns*>(nullptr)), ...);
        }
    };

  template<class Sndr, class Env = env<>,
           template<class...> class Tuple = decayed-tuple,
           template<class...> class Variant = variant-or-empty>
      requires sender_in<Sndr, Env>
    using value_types_of_t =
      gather-signatures<set_value_t, completion_signatures_of_t<Sndr, Env>, Tuple, Variant>;

  template<class Sndr, class Env = env<>,
           template<class...> class Variant = variant-or-empty>
      requires sender_in<Sndr, Env>
    using error_types_of_t =
      gather-signatures<set_error_t, completion_signatures_of_t<Sndr, Env>,
                        type_identity_t, Variant>;

  template<class Sndr, class Env = env<>>
      requires sender_in<Sndr, Env>
    constexpr bool sends_stopped =
      !same_as<type-list<>,
               gather-signatures<set_stopped_t, completion_signatures_of_t<Sndr, Env>,
                                 type-list, type-list>>;
}
```

For a subexpression `tag`, let `Tag` be the decayed type of `tag`.
`completion_signatures<Fns...>::count-of({}tag)` returns the count of
function types in `Fns...` that are of the form `Tag(Ts...)` where `Ts`
is a pack of types.

## Queryable utilities <a id="exec.envs">[[exec.envs]]</a>

### Class template `prop` <a id="exec.prop">[[exec.prop]]</a>

``` cpp
namespace std::execution {
  template<class QueryTag, class ValueType>
  struct prop {
    QueryTag query_;            // exposition only
    ValueType value_;           // exposition only

    constexpr const ValueType& query(QueryTag) const noexcept {
      return value_;
    }
  };

  template<class QueryTag, class ValueType>
    prop(QueryTag, ValueType) -> prop<QueryTag, unwrap_reference_t<ValueType>>;
}
```

Class template `prop` is for building a queryable object from a query
object and a value.

*Mandates:* `callable<QueryTag, prop-like<ValueType>>` is modeled, where
*`prop-like`* is the following exposition-only class template:

``` cpp
template<class ValueType>
struct prop-like {              // exposition only
  const ValueType& query(auto) const noexcept;
};
```

[*Example 1*:

``` cpp
template<sender Sndr>
sender auto parameterize_work(Sndr sndr) {
  // Make an environment such that get_allocator(env) returns a reference to a copy of my_alloc{}.
  auto e = prop(get_allocator, my_alloc{});

  // Parameterize the input sender so that it will use our custom execution environment.
  return write_env(sndr, e);
}
```

— *end example*]

Specializations of `prop` are not assignable.

### Class template `env` <a id="exec.env">[[exec.env]]</a>

``` cpp
namespace std::execution {
  template<queryable... Envs>
  struct env {
    Envs_0 envs_0;               // exposition only
    Envs_1 envs_1;               // exposition only
      ⋮
    Envs_{n-1} envs_{n-1};           // exposition only

    template<class QueryTag>
      constexpr decltype(auto) query(QueryTag q) const noexcept(see below);
  };

  template<class... Envs>
    env(Envs...) -> env<unwrap_reference_t<Envs>...>;
}
```

The class template `env` is used to construct a queryable object from
several queryable objects. Query invocations on the resulting object are
resolved by attempting to query each subobject in lexical order.

Specializations of `env` are not assignable.

It is unspecified whether `env` supports initialization using a
parenthesized *expression-list* [[dcl.init]], unless the
*expression-list* consist of a single element of type (possibly const)
`env`.

[*Example 1*:

``` cpp
template<sender Sndr>
sender auto parameterize_work(Sndr sndr) {
  // Make an environment such that:
  //   get_allocator(env) returns a reference to a copy of my_alloc{}
  //   get_scheduler(env) returns a reference to a copy of my_sched{}
  auto e = env{prop(get_allocator, my_alloc{}),
               prop(get_scheduler, my_sched{})};

  // Parameterize the input sender so that it will use our custom execution environment.
  return write_env(sndr, e);
}
```

— *end example*]

``` cpp
template<class QueryTag>
constexpr decltype(auto) query(QueryTag q) const noexcept(see below);
```

Let `has-query` be the following exposition-only concept:

``` cpp
template<class Env, class QueryTag>
  concept has-query =                   // exposition only
    requires (const Env& env) {
      env.query(QueryTag());
    };
```

Let *fe* be the first element of envs₀, envs₁, …, envsₙ₋₁ such that the
expression *`fe`*`.query(q)` is well-formed.

*Constraints:* `(has-query<Envs, QueryTag> || ...)` is `true`.

*Effects:* Equivalent to: `return `*`fe`*`.query(q);`

*Remarks:* The expression in the `noexcept` clause is equivalent to
`noexcept(`*`fe`*`.query(q))`.

## Execution contexts <a id="exec.ctx">[[exec.ctx]]</a>

### `execution::run_loop` <a id="exec.run.loop">[[exec.run.loop]]</a>

#### General <a id="exec.run.loop.general">[[exec.run.loop.general]]</a>

A `run_loop` is an execution resource on which work can be scheduled. It
maintains a thread-safe first-in-first-out queue of work. Its `run`
member function removes elements from the queue and executes them in a
loop on the thread of execution that calls `run`.

A `run_loop` instance has an associated *count* that corresponds to the
number of work items that are in its queue. Additionally, a `run_loop`
instance has an associated state that can be one of *starting*,
*running*, *finishing*, or *finished*.

Concurrent invocations of the member functions of `run_loop` other than
`run` and its destructor do not introduce data races. The member
functions *`pop-front`*, *`push-back`*, and `finish` execute atomically.

*Recommended practice:* Implementations should use an intrusive queue of
operation states to hold the work units to make scheduling
allocation-free.

``` cpp
namespace std::execution {
  class run_loop {
    // [exec.run.loop.types], associated types
    class run-loop-scheduler;                                   // exposition only
    class run-loop-sender;                                      // exposition only
    struct run-loop-opstate-base {                              // exposition only
      virtual void execute() = 0;                               // exposition only
      run_loop* loop;                                           // exposition only
      run-loop-opstate-base* next;                              // exposition only
    };
    template<class Rcvr>
      using run-loop-opstate = unspecified;                     // exposition only

    // [exec.run.loop.members], member functions
    run-loop-opstate-base* pop-front();                         // exposition only
    void push-back(run-loop-opstate-base*);                     // exposition only

  public:
    // [exec.run.loop.ctor], constructor and destructor
    run_loop() noexcept;
    run_loop(run_loop&&) = delete;
    ~run_loop();

    // [exec.run.loop.members], member functions
    run-loop-scheduler get_scheduler();
    void run();
    void finish();
  };
}
```

#### Associated types <a id="exec.run.loop.types">[[exec.run.loop.types]]</a>

``` cpp
class run-loop-scheduler;
```

*`run-loop-scheduler`* is an unspecified type that models `scheduler`.

Instances of *`run-loop-scheduler`* remain valid until the end of the
lifetime of the `run_loop` instance from which they were obtained.

Two instances of *`run-loop-scheduler`* compare equal if and only if
they were obtained from the same `run_loop` instance.

Let *`sch`* be an expression of type *`run-loop-scheduler`*. The
expression `schedule(sch)` has type *`run-loop-\newline sender`* and is
not potentially-throwing if *`sch`* is not potentially-throwing.

``` cpp
class run-loop-sender;
```

*`run-loop-sender`* is an exposition-only type that satisfies `sender`.
`completion_signatures_of_t<run-{loop-sender}>` is

``` cpp
completion_signatures<set_value_t(), set_error_t(exception_ptr), set_stopped_t()>
```

An instance of *`run-loop-sender`* remains valid until the end of the
lifetime of its associated `run_loop` instance.

Let *`sndr`* be an expression of type *`run-loop-sender`*, let *`rcvr`*
be an expression such that `receiver_of<decltype((rcvr)), CS>` is `true`
where `CS` is the `completion_signatures` specialization above. Let `C`
be either `set_value_t` or `set_stopped_t`. Then:

- The expression `connect(sndr, rcvr)` has type
  `run-loop-opstate<decay_t<decltype((rcvr))>>` and is
  potentially-throwing if and only if `(void(sndr), auto(rcvr))` is
  potentially-throwing.
- The expression `get_completion_scheduler<C>(get_env(sndr))` is
  potentially-throwing if and only if *`sndr`* is potentially-throwing,
  has type *`run-loop-scheduler`*, and compares equal to the
  *`run-loop-\newline scheduler`* instance from which *`sndr`* was
  obtained.

``` cpp
template<class Rcvr>
  struct run-loop-opstate;
```

`\exposid{run-loop-opstate}<Rcvr>`

inherits privately and unambiguously from *`run-loop-opstate-base`*.

Let o be a non-const lvalue of type `run-loop-opstate<Rcvr>`, and let
`REC(o)` be a non-const lvalue reference to an instance of type `Rcvr`
that was initialized with the expression *`rcvr`* passed to the
invocation of connect that returned o. Then:

- The object to which `REC(o)` refers remains valid for the lifetime of
  the object to which o refers.
- The type `run-loop-opstate<Rcvr>` overrides
  `run-loop-opstate-base::execute()` such that `o.execute()` is
  equivalent to:
  ``` cpp
  if (get_stop_token(REC(o)).stop_requested()) {
    set_stopped(std::move(REC(o)));
  } else {
    set_value(std::move(REC(o)));
  }
  ```
- The expression `start(o)` is equivalent to:
  ``` cpp
  try {
    o.loop->push-back(addressof(o));
  } catch(...) {
    set_error(std::move(REC(o)), current_exception());
  }
  ```

#### Constructor and destructor <a id="exec.run.loop.ctor">[[exec.run.loop.ctor]]</a>

``` cpp
run_loop() noexcept;
```

*Ensures:* The `run_loop` instance’s count is 0 and its state is
starting.

``` cpp
~run_loop();
```

*Effects:* If the `run_loop` instance’s count is not 0 or if its state
is running, invokes `terminate`[[except.terminate]]. Otherwise, has no
effects.

#### Member functions <a id="exec.run.loop.members">[[exec.run.loop.members]]</a>

``` cpp
run-loop-opstate-base* pop-front();
```

*Effects:* Blocks [[defns.block]] until one of the following conditions
is `true`:

- The `run_loop` instance’s count is 0 and its state is finishing, in
  which case *pop-front* sets the state to finished and returns
  `nullptr`; or
- the `run_loop` instance’s count is greater than 0, in which case an
  item is removed from the front of the queue, the count is decremented
  by `1`, and the removed item is returned.

``` cpp
void push-back(run-loop-opstate-base* item);
```

*Effects:* Adds `item` to the back of the queue and increments the
`run_loop` instance’s count by 1.

*Synchronization:* This operation synchronizes with the *pop-front*
operation that obtains `item`.

``` cpp
run-loop-scheduler get_scheduler();
```

*Returns:* An instance of *run-loop-scheduler* that can be used to
schedule work onto this `run_loop` instance.

``` cpp
void run();
```

*Preconditions:* The `run_loop` instance’s state is either starting or
finishing.

*Effects:* If the `run_loop` instance’s state is starting, sets the
state to running, otherwise leaves the state unchanged. Then, equivalent
to:

``` cpp
while (auto* op = pop-front()) {
  op->execute();
}
```

*Remarks:* When the `run_loop` instance’s state changes, it does so
without introducing data races.

``` cpp
void finish();
```

*Preconditions:* The `run_loop` instance’s state is either starting or
running.

*Effects:* Changes the `run_loop` instance’s state to finishing.

*Synchronization:* `finish` synchronizes with the *pop-front* operation
that returns `nullptr`.

## Coroutine utilities <a id="exec.coro.util">[[exec.coro.util]]</a>

### `execution::as_awaitable` <a id="exec.as.awaitable">[[exec.as.awaitable]]</a>

`as_awaitable` transforms an object into one that is awaitable within a
particular coroutine. Subclause [[exec.coro.util]] makes use of the
following exposition-only entities:

``` cpp
namespace std::execution {
  template<class Sndr, class Promise>
    concept awaitable-sender =
      single-sender<Sndr, env_of_t<Promise>> &&
      sender_to<Sndr, awaitable-receiver> &&    // see below
      requires (Promise& p) {
        { p.unhandled_stopped() } -> convertible_to<coroutine_handle<>>;
      };

  template<class Sndr>
    concept has-queryable-await-completion-adaptor =            // exposition only
      sender<Sndr> &&
      requires(Sndr&& sender) {
        get_await_completion_adaptor(get_env(sender));
      };

  template<class Sndr, class Promise>
    class sender-awaitable;                                     // exposition only
}
```

The type `sender-awaitable<Sndr, Promise>` is equivalent to:

``` cpp
namespace std::execution {
  template<class Sndr, class Promise>
  class sender-awaitable {
    struct unit {};                                             // exposition only
    using value-type =                                          // exposition only
      single-sender-value-type<Sndr, env_of_t<Promise>>;
    using result-type =                                         // exposition only
      conditional_t<is_void_v<value-type>, unit, value-type>;
    struct awaitable-receiver;                                  // exposition only

    variant<monostate, result-type, exception_ptr> result{};    // exposition only
    connect_result_t<Sndr, awaitable-receiver> state;           // exposition only

  public:
    sender-awaitable(Sndr&& sndr, Promise& p);
    static constexpr bool await_ready() noexcept { return false; }
    void await_suspend(coroutine_handle<Promise>) noexcept { start(state); }
    value-type await_resume();
  };
}
```

*`awaitable-receiver`* is equivalent to:

``` cpp
struct awaitable-receiver {
  using receiver_concept = receiver_t;
  variant<monostate, result-type, exception_ptr>* result-ptr;   // exposition only
  coroutine_handle<Promise> continuation;                       // exposition only
  // see below
};
```

Let `rcvr` be an rvalue expression of type *`awaitable-receiver`*, let
`crcvr` be a const lvalue that refers to `rcvr`, let `vs` be a pack of
subexpressions, and let `err` be an expression of type `Err`. Then:

- If `constructible_from<result-type, decltype((vs))...>` is satisfied,
  the expression `set_value(\newline rcvr, vs...)` is equivalent to:
  ``` cpp
  try {
    rcvr.result-ptr->template emplace<1>(vs...);
  } catch(...) {
    rcvr.result-ptr->template emplace<2>(current_exception());
  }
  rcvr.continuation.resume();
  ```

  Otherwise, `set_value(rcvr, vs...)` is ill-formed.
- The expression `set_error(rcvr, err)` is equivalent to:
  ``` cpp
  rcvr.result-ptr->template emplace<2>(AS-EXCEPT-PTR(err));    // see [exec.general]
  rcvr.continuation.resume();
  ```
- The expression `set_stopped(rcvr)` is equivalent to:
  ``` cpp
  static_cast<coroutine_handle<>>(rcvr.continuation.promise().unhandled_stopped()).resume();
  ```
- For any expression `tag` whose type satisfies `forwarding-query` and
  for any pack of subexpressions `as`,
  `get_env(crcvr).query(tag, as...)` is expression-equivalent to:
  ``` cpp
  tag(get_env(as_const(crcvr.continuation.promise())), as...)
  ```

``` cpp
sender-awaitable(Sndr&& sndr, Promise& p);
```

*Effects:* Initializes *state* with

``` cpp
connect(std::forward<Sndr>(sndr),
        awaitable-receiver{addressof(result), coroutine_handle<Promise>::from_promise(p)})
```

``` cpp
value-type await_resume();
```

*Effects:* Equivalent to:

``` cpp
if (result.index() == 2)
  rethrow_exception(get<2>(result));
if constexpr (!is_void_v<value-type>)
  return std::forward<value-type>(get<1>(result));
```

`as_awaitable` is a customization point object. For subexpressions
`expr` and `p` where `p` is an lvalue, `Expr` names the type
`decltype((expr))` and `Promise` names the type
`decay_t<decltype((p))>`, `as_awaitable(expr, p)` is
expression-equivalent to, except that the evaluations of `expr` and `p`
are indeterminately sequenced:

- `expr.as_awaitable(p)` if that expression is well-formed. *Mandates:*
  `is-awaitable<A, Promise>` is `true`, where `A` is the type of the
  expression above.
- Otherwise, `(void(p), expr)` if `is-awaitable<Expr, U>` is `true`,
  where `U` is an unspecified class type that is not `Promise` and that
  lacks a member named `await_transform`. *Preconditions:*
  `is-awaitable<Expr, Promise>` is `true` and the expression
  `co_await expr` in a coroutine with promise type `U` is
  expression-equivalent to the same expression in a coroutine with
  promise type `Promise`.
- Otherwise, `sender-awaitable{adapted-expr, p}` if
  ``` cpp
  has-queryable-await-completion-adaptor<Expr>
  ```

  and
  ``` cpp
  awaitable-sender<decltype((adapted-expr)), Promise>
  ```

  are both satisfied, where *`adapted-expr`* is
  `get_await_completion_adaptor(get_env(expr))(expr)`, except that
  `expr` is evaluated only once.
- Otherwise, `sender-awaitable{expr, p}` if
  `awaitable-sender<Expr, Promise>` is `true`.
- Otherwise, `(void(p), expr)`.

### `execution::with_awaitable_senders` <a id="exec.with.awaitable.senders">[[exec.with.awaitable.senders]]</a>

`with_awaitable_senders`, when used as the base class of a coroutine
promise type, makes senders awaitable in that coroutine type.

In addition, it provides a default implementation of `unhandled_stopped`
such that if a sender completes by calling `set_stopped`, it is treated
as if an uncatchable "stopped" exception were thrown from the
*await-expression*.

[*Note 1*: The coroutine is never resumed, and the `unhandled_stopped`
of the coroutine caller’s promise type is called. — *end note*]

``` cpp
namespace std::execution {
  template<class-type Promise>
    struct with_awaitable_senders {
      template<class OtherPromise>
        requires (!same_as<OtherPromise, void>)
      void set_continuation(coroutine_handle<OtherPromise> h) noexcept;

      coroutine_handle<> continuation() const noexcept { return continuation; }

      coroutine_handle<> unhandled_stopped() noexcept {
        return stopped-handler(continuation.address());
      }

      template<class Value>
      see below await_transform(Value&& value);

    private:
      [[noreturn]] static coroutine_handle<>
        default-unhandled-stopped(void*) noexcept {             // exposition only
        terminate();
      }
      coroutine_handle<> continuation{};                        // exposition only
      coroutine_handle<> (*stopped-handler)(void*) noexcept =   // exposition only
        &default-unhandled-stopped;
    };
}
```

``` cpp
template<class OtherPromise>
  requires (!same_as<OtherPromise, void>)
void set_continuation(coroutine_handle<OtherPromise> h) noexcept;
```

*Effects:* Equivalent to:

``` cpp
continuation = h;
if constexpr ( requires(OtherPromise& other) { other.unhandled_stopped(); } ) {
  stopped-handler = [](void* p) noexcept -> coroutine_handle<> {
    return coroutine_handle<OtherPromise>::from_address(p)
      .promise().unhandled_stopped();
  };
} else {
  stopped-handler = &default-unhandled-stopped;
}
```

``` cpp
template<class Value>
call-result-t<as_awaitable_t, Value, Promise&> await_transform(Value&& value);
```

*Effects:* Equivalent to:

``` cpp
return as_awaitable(std::forward<Value>(value), static_cast<Promise&>(*this));
```

### `execution::affine_on` <a id="exec.affine.on">[[exec.affine.on]]</a>

`affine_on` adapts a sender into one that completes on the specified
scheduler. If the algorithm determines that the adapted sender already
completes on the correct scheduler it can avoid any scheduling
operation.

The name `affine_on` denotes a pipeable sender adaptor object. For
subexpressions `sch` and `sndr`, if `decltype((sch))` does not satisfy
`scheduler`, or `decltype((sndr))` does not satisfy `sender`,
`affine_on(sndr, sch)` is ill-formed.

Otherwise, the expression `affine_on(sndr, sch)` is
expression-equivalent to:

``` cpp
transform_sender(get-domain-early(sndr), make-sender(affine_on, sch, sndr))
```

except that `sndr` is evaluated only once.

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for `affine_on_t` as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<affine_on_t> : default-impls {
    static constexpr auto get-attrs =
      [](const auto& data, const auto& child) noexcept -> decltype(auto) {
        return JOIN-ENV(SCHED-ATTRS(data), FWD-ENV(get_env(child)));
      };
  };
}
```

Let `out_sndr` be a subexpression denoting a sender returned from
`affine_on(sndr, sch)` or one equal to such, and let `OutSndr` be the
type `decltype((out_sndr))`. Let `out_rcvr` be a subexpression denoting
a receiver that has an environment of type `Env` such that
`sender_in<OutSndr, Env>` is `true`. Let `op` be an lvalue referring to
the operation state that results from connecting `out_sndr` to
`out_rcvr`. Calling `start(op)` will start `sndr` on the current
execution agent and execute completion operations on `out_rcvr` on an
execution agent of the execution resource associated with `sch`. If the
current execution resource is the same as the execution resource
associated with `sch`, the completion operation on `out_rcvr` may be
called before `start(op)` completes. If scheduling onto `sch` fails, an
error completion on `out_rcvr` shall be executed on an unspecified
execution agent.

### `execution::inline_scheduler` <a id="exec.inline.scheduler">[[exec.inline.scheduler]]</a>

``` cpp
namespace std::execution {
  class inline_scheduler {
    class inline-sender;                // exposition only

    template<receiver R>
      class inline-state;               // exposition only

  public:
    using scheduler_concept = scheduler_t;

    constexpr inline-sender schedule() noexcept { return {}; }
    constexpr bool operator==(const inline_scheduler&) const noexcept = default;
  };
}
```

`inline_scheduler` is a class that models `scheduler` [[exec.sched]].
All objects of type `inline_scheduler` are equal.

*`inline-sender`* is an exposition-only type that satisfies `sender`.
The type `completion_signatures_of_t<inline-sender>` is
`completion_signatures<set_value_t()>`.

Let `sndr` be an expression of type *`inline-sender`*, let `rcvr` be an
expression such that `receiver_of<decltype((rcvr)), CS>` is `true` where
`CS` is `completion_signatures<set_value_t()>`, then:

- the expression `connect(sndr, rcvr)` has type
  `inline-state<remove_cvref_t<decltype((rcvr))>>` and is
  potentially-throwing if and only if `((void)sndr, auto(rcvr))` is
  potentially-throwing, and
- the expression `get_completion_scheduler<set_value_t>(get_env(sndr))`
  has type `inline_scheduler` and is potentially-throwing if and only if
  `get_env(sndr)` is potentially-throwing.

Let `o` be a non-`const` lvalue of type `inline-state<Rcvr>`, and let
`REC(o)` be a non-`const` lvalue reference to an object of type `Rcvr`
that was initialized with the expression `rcvr` passed to an invocation
of `connect` that returned `o`, then:

- the object to which `REC(o)` refers remains valid for the lifetime of
  the object to which `o` refers, and
- the expression `start(o)` is equivalent to
  `set_value(std::move(REC(o)))`.

### `execution::task_scheduler` <a id="exec.task.scheduler">[[exec.task.scheduler]]</a>

``` cpp
namespace std::execution {
  class task_scheduler {
    class ts-sender;                    // exposition only

    template<receiver R>
      class state;                      // exposition only

  public:
    using scheduler_concept = scheduler_t;

    template<class Sch, class Allocator = allocator<void>>
      requires (!same_as<task_scheduler, remove_cvref_t<Sch>>)
        && scheduler<Sch>
    explicit task_scheduler(Sch&& sch, Allocator alloc = {});

    ts-sender schedule();

    friend bool operator==(const task_scheduler& lhs, const task_scheduler& rhs)
        noexcept;
    template<class Sch>
      requires (!same_as<task_scheduler, Sch>)
      && scheduler<Sch>
    friend bool operator==(const task_scheduler& lhs, const Sch& rhs) noexcept;

  private:
    shared_ptr<void> sch_; // exposition only
  };
}
```

`task_scheduler` is a class that models `scheduler` [[exec.sched]].
Given an object `s` of type `task_scheduler`, let `SCHED(s)` be the
object owned by `s.sch_`.

``` cpp
template<class Sch, class Allocator = allocator<void>>
  requires(!same_as<task_scheduler, remove_cvref_t<Sch>>) && scheduler<Sch>
explicit task_scheduler(Sch&& sch, Allocator alloc = {});
```

*Effects:* Initialize *sch\_* with
`allocate_shared<remove_cvref_t<Sch>>(alloc, std::forward<Sch>(sch))`.

*Recommended practice:* Implementations should avoid the use of
dynamically allocated memory for small scheduler objects.

*Remarks:* Any allocations performed by construction of *ts-sender* or
*state* objects resulting from calls on `*this` are performed using a
copy of `alloc`.

``` cpp
ts-sender schedule();
```

*Effects:* Returns an object of type *ts-sender* containing a sender
initialized with `schedule(`*`SCHED`*`(*this))`.

``` cpp
bool operator==(const task_scheduler& lhs, const task_scheduler& rhs) noexcept;
```

*Effects:* Equivalent to: `return lhs == `*`SCHED`*`(rhs);`

``` cpp
template<class Sch>
  requires (!same_as<task_scheduler, Sch>)
        && scheduler<Sch>
bool operator==(const task_scheduler& lhs, const Sch& rhs) noexcept;
```

*Returns:* `false` if the type of *`SCHED`*`(lhs)` is not `Sch`,
otherwise *`SCHED`*`(lhs) == rhs`.

``` cpp
namespace std::execution {
  class task_scheduler::ts-sender {     // exposition only
  public:
    using sender_concept = sender_t;

    template<receiver Rcvr>
      state<Rcvr> connect(Rcvr&& rcvr);
  };
}
```

*`ts-sender`* is an exposition-only class that models `sender`
[[exec.snd]] and for which `completion_signatures_of_t<ts-sender>`
denotes:

``` cpp
completion_signatures<
  set_value_t(),
  set_error_t(error_code),
  set_error_t(exception_ptr),
  set_stopped_t()>
```

Let `sch` be an object of type `task_scheduler` and let `sndr` be an
object of type *`ts-sender`* obtained from `schedule(sch)`. Then
`get_completion_scheduler<set_value_t>(get_env(sndr)) == sch` is `true`.
The object `SENDER(sndr)` is the sender object contained by `sndr` or an
object move constructed from it.

``` cpp
template<receiver Rcvr>
  state<Rcvr> connect(Rcvr&& rcvr);
```

*Effects:* Let *`r`* be an object of a type that models `receiver` and
whose completion handlers result in invoking the corresponding
completion handlers of `rcvr` or copy thereof. Returns an object of type
*`state`*`<Rcvr>` containing an operation state object initialized with
`connect(`*`SENDER`*`(*this), std::move(`*`r`*`))`.

``` cpp
namespace std::execution {
  template<receiver R>
  class task_scheduler::state {         // exposition only
  public:
    using operation_state_concept = operation_state_t;

    void start() & noexcept;
  };
}
```

*`state`* is an exposition-only class template whose specializations
model `operation_state` [[exec.opstate]].

``` cpp
void start() & noexcept;
```

*Effects:* Equivalent to `start(st)` where `st` is the operation state
object contained by `*this`.

### `execution::task` <a id="exec.task">[[exec.task]]</a>

#### `task` overview <a id="task.overview">[[task.overview]]</a>

The `task` class template represents a sender that can be used as the
return type of coroutines. The first template parameter `T` defines the
type of the value completion datum [[exec.async.ops]] if `T` is not
`void`. Otherwise, there are no value completion datums. Inside
coroutines returning `task<T, E>` the operand of `co_return` (if any)
becomes the argument of `set_value`. The second template parameter
`Environment` is used to customize the behavior of `task`.

#### Class template `task` <a id="task.class">[[task.class]]</a>

``` cpp
namespace std::execution {
  template<class T, class Environment>
  class task {
    // [task.state]
    template<receiver Rcvr>
      class state;                              // exposition only

  public:
    using sender_concept = sender_t;
    using completion_signatures = see below;
    using allocator_type = see below;
    using scheduler_type = see below;
    using stop_source_type = see below;
    using stop_token_type = decltype(declval<stop_source_type>().get_token());
    using error_types = see below;

    // [task.promise]
    class promise_type;

    task(task&&) noexcept;
    ~task();

    template<receiver Rcvr>
      state<Rcvr> connect(Rcvr&& rcvr);

  private:
    coroutine_handle<promise_type> handle;      // exposition only
  };
}
```

`task<T, E>` models `sender` [[exec.snd]] if `T` is `void`, a reference
type, or a cv-unqualified non-array object type and `E` is a class type.
Otherwise a program that instantiates the definition of `task<T, E>` is
ill-formed.

The nested types of `task` template specializations are determined based
on the `Environment` parameter:

- `allocator_type` is `Environment::allocator_type` if that
  *qualified-id* is valid and denotes a type, `allocator<byte>`
  otherwise.
- `scheduler_type` is `Environment::scheduler_type` if that
  *qualified-id* is valid and denotes a type, `task_scheduler`
  otherwise.
- `stop_source_type` is `Environment::stop_source_type` if that
  *qualified-id* is valid and denotes a type, `inplace_stop_source`
  otherwise.
- `error_types` is `Environment::error_types` if that *qualified-id* is
  valid and denotes a type,
  `completion_signatures<set_error_t(exception_ptr)>` otherwise.

A program is ill-formed if `error_types` is not a specialization of
`execution::completion_signatures` or if the template arguments of that
specialization contain an element which is not of the form
`set_error_t(E)` for some type `E`.

The type alias `completion_signatures` is a specialization of
`execution::completion_signatures` with the template arguments (in
unspecified order):

- `set_value_t()` if `T` is `void`, and `set_value_t(T)` otherwise;
- template arguments of the specialization of
  `execution::completion_signatures` denoted by `error_types`; and
- `set_stopped_t()`.

`allocator_type` shall meet the *Cpp17Allocator* requirements.

#### `task` members <a id="task.members">[[task.members]]</a>

``` cpp
task(task&& other) noexcept;
```

*Effects:* Initializes *handle* with `exchange(other.`*`handle`*`, {})`.

``` cpp
~task();
```

*Effects:* Equivalent to:

``` cpp
if (handle)
  handle.destroy();
```

``` cpp
template<receiver Rcvr>
  state<Rcvr> connect(Rcvr&& recv);
```

*Preconditions:* `bool(`*`handle`*`)` is `true`.

*Effects:* Equivalent to:

``` cpp
return state<Rcvr>(exchange(handle, {}), std::forward<Rcvr>(recv));
```

#### Class template `task::state` <a id="task.state">[[task.state]]</a>

``` cpp
namespace std::execution {
  template<class T, class Environment>
  template<receiver Rcvr>
  class task<T, Environment>::state {           // exposition only
  public:
    using operation_state_concept = operation_state_t;

    template<class R>
      state(coroutine_handle<promise_type> h, R&& rr);

    ~state();

    void start() & noexcept;

  private:
    using own-env-t = see belownc;                // exposition only
    coroutine_handle<promise_type> handle;      // exposition only
    remove_cvref_t<Rcvr>           rcvr;        // exposition only
    own-env-t                      own-env;     // exposition only
    Environment                    environment; // exposition only
  };
}
```

The type *`own-env-t`* is `Environment::template
env_type<decltype(get_env({}declval{}<Rcvr>({}))){}>` if that
*qualified-id* is valid and denotes a type, `env<>` otherwise.

``` cpp
template<class R>
  state(coroutine_handle<promise_type> h, R&& rr);
```

*Effects:* Initializes

- *handle* with `std::move(h)`;
- *rcvr* with `std::forward<R>(rr)`;
- *own-env* with *`own-env-t`*`(get_env(`*`rcvr`*`))` if that expression
  is valid and *`own-env-t`*`()` otherwise. If neither of these
  expressions is valid, the program is ill-formed.
- *environment* with `Environment(`*`own-env`*`)` if that expression is
  valid, otherwise `Environment(get_env(`*`rcvr`*`))` if this expression
  is valid, otherwise `Environment()`. If neither of these expressions
  is valid, the program is ill-formed.

``` cpp
~state();
```

*Effects:* Equivalent to:

``` cpp
if (handle)
  handle.destroy();
```

``` cpp
void start() & noexcept;
```

*Effects:* Let *`prom`* be the object *`handle`*`.promise()`. Associates
*`STATE`*`(`*`prom`*`)`, *`RCVR`*`(`*`prom`*`)`, and
*`SCHED`*`(`*`prom`*`)` with `*this` as follows:

- *`STATE`*`(`*`prom`*`)` is `*this`.
- *`RCVR`*`(`*`prom`*`)` is *rcvr*.
- *`SCHED`*`(`*`prom`*`)` is the object initialized with
  `scheduler_type(get_scheduler(get_env(`*`rcvr`*`)))` if that
  expression is valid and `scheduler_type()` otherwise. If neither of
  these expressions is valid, the program is ill-formed.

Let *`st`* be `get_stop_token(get_env(`*`rcvr`*`))`. Initializes
*`prom`*`.`*`token`* and *`prom`*`.`*`source`* such that

- *`prom`*`.`*`token`*`.stop_requested()` returns
  *`st`*`.stop_requested()`;
- *`prom`*`.`*`token`*`.stop_possible()` returns
  *`st`*`.stop_possible()`; and
- for types `Fn` and `Init` such that both `invocable<Fn>` and
  `constructible_from<Fn, Init>` are modeled,
  `stop_token_type::callback_type<Fn>` models
  `stoppable-callback-for<Fn, stop_token_type, Init>`.

After that invokes *`handle`*`.resume()`.

#### Class `task::promise_type` <a id="task.promise">[[task.promise]]</a>

``` cpp
namespace std::execution {
  template<class T, class Environment>
  class task<T, Environment>::promise_type {
  public:
    template<class... Args>
      promise_type(const Args&... args);

    task get_return_object() noexcept;

    auto initial_suspend() noexcept;
    auto final_suspend() noexcept;

    void uncaught_exception();
    coroutine_handle<> unhandled_stopped();

    void return_void();                 // present only if is_void_v<T> is true
    template<class V>
      void return_value(V&& value);     // present only if is_void_v<T> is false

    template<class E>
      unspecified yield_value(with_error<E> error);

    template<class A>
      auto await_transform(A&& a);
    template<class Sch>
      auto await_transform(change_coroutine_scheduler<Sch> sch);

    unspecified get_env() const noexcept;

    template<class... Args>
      void* operator new(size_t size, Args&&... args);

    void operator delete(void* pointer, size_t size) noexcept;

  private:
    using error-variant = see belownc;    // exposition only

    allocator_type    alloc;            // exposition only
    stop_source_type  source;           // exposition only
    stop_token_type   token;            // exposition only
    optional<T>       result;           // exposition only; present only if is_void_v<T> is false
    error-variant     errors;           // exposition only
  };
}
```

Let `prom` be an object of `promise_type` and let `tsk` be the `task`
object created by `prom.get_return_object()`. The description below
refers to objects `STATE(prom)`, `RCVR(prom)`, and `SCHED(prom)`
associated with `tsk` during evaluation of `task::state<Rcvr>::start`
for some receiver `Rcvr`.

*`error-variant`* is a `variant<monostate,
remove_cvref_t<E>...>`, with duplicate types removed, where `E...` are
the parameter types of the template arguments of the specialization of
`execution::completion_signatures` denoted by `error_types`.

``` cpp
template<class... Args>
  promise_type(const Args&... args);
```

*Mandates:* The first parameter of type `allocator_arg_t` (if any) is
not the last parameter.

*Effects:* If `Args` contains an element of type `allocator_arg_t` then
*alloc* is initialized with the corresponding next element of `args`.
Otherwise, *alloc* is initialized with `allocator_type()`.

``` cpp
task get_return_object() noexcept;
```

*Returns:* A `task` object whose member *handle* is
`coroutine_handle<promise_type>::from_promise(*this)`.

``` cpp
auto initial_suspend() noexcept;
```

*Returns:* An awaitable object of unspecified type [[expr.await]] whose
member functions arrange for

- the calling coroutine to be suspended,
- the coroutine to be resumed on an execution agent of the execution
  resource associated with *`SCHED`*`(*this)`.

``` cpp
auto final_suspend() noexcept;
```

*Returns:* An awaitable object of unspecified type [[expr.await]] whose
member functions arrange for the completion of the asynchronous
operation associated with *`STATE`*`(*this)` by invoking:

- `set_error(std::move(`*`RCVR`*`(*this)), std::move(e))` if
  *`errors`*`.index()` is greater than zero and `e` is the value held by
  *errors*, otherwise
- `set_value(std::move(`*`RCVR`*`(*this)))` if `is_void<T>` is `true`,
  and otherwise
- `set_value(std::move(`*`RCVR`*`(*this)), *`*`result`*`)`.

``` cpp
template<class Err>
  auto yield_value(with_error<Err> err);
```

*Mandates:* `std::move(err.error)` is convertible to exactly one of the
`set_error_t` argument types of `error_types`. Let *`Cerr`* be that
type.

*Returns:* An awaitable object of unspecified type [[expr.await]] whose
member functions arrange for the calling coroutine to be suspended and
then completes the asynchronous operation associated with
*`STATE`*`(*this)` by invoking
`set_error(std::move(`*`RCVR`*`(*this)), `*`Cerr`*`(std::move(err.error)))`.

``` cpp
template<sender Sender>
  auto await_transform(Sender&& sndr) noexcept;
```

*Returns:* If `same_as<inline_scheduler, scheduler_type>` is `true`
returns `as_awaitable(std::forward<Sender>(sndr), *this)`; otherwise
returns
`as_awaitable(affine_on(std::forward<Sender>(sndr), `*`SCHED`*`(*this)), *this)`.

``` cpp
template<class Sch>
  auto await_transform(change_coroutine_scheduler<Sch> sch) noexcept;
```

*Effects:* Equivalent to:

``` cpp
return await_transform(just(exchange(SCHED(*this), scheduler_type(sch.scheduler))), *this);
```

``` cpp
void uncaught_exception();
```

*Effects:* If the signature `set_error_t(exception_ptr)` is not an
element of `error_types`, calls `terminate()`[[except.terminate]].
Otherwise, stores `current_exception()` into *errors*.

``` cpp
coroutine_handle<> unhandled_stopped();
```

*Effects:* Completes the asynchronous operation associated with
*`STATE`*`(*this)` by invoking
`set_stopped(std::move(`*`RCVR`*`(*this)))`.

*Returns:* `noop_coroutine()`.

``` cpp
unspecified get_env() const noexcept;
```

*Returns:* An object `env` such that queries are forwarded as follows:

- `env.query(get_scheduler)` returns
  `scheduler_type(`*`SCHED`*`(*this))`.
- `env.query(get_allocator)` returns *alloc*.
- `env.query(get_stop_token)` returns *token*.
- For any other query `q` and arguments `a...` a call to
  `env.query(q, a...)` returns *`STATE`*`(*this)`.
  `environment.query(q, a...)` if this expression is well-formed and
  `forwarding_query(q)` is well-formed and is `true`. Otherwise
  `env.query(q, a...)` is ill-formed.

``` cpp
template<class... Args>
  void* operator new(size_t size, const Args&... args);
```

If there is no parameter with type `allocator_arg_t` then let `alloc` be
`allocator_type()`. Otherwise, let `arg_next` be the parameter following
the first `allocator_arg_t` parameter, and let `alloc` be
`allocator_type(arg_next)`. Let `PAlloc` be
`allocator_traits<allocator_type>::template rebind_alloc<U>`, where `U`
is an unspecified type whose size and alignment are both
\_\_STDCPP_DEFAULT_NEW_ALIGNMENT\_\_.

*Mandates:*

- The first parameter of type `allocator_arg_t` (if any) is not the last
  parameter.
- `allocator_type(arg_next)` is a valid expression if there is a
  parameter of type `allocator_arg_t`.
- `allocator_traits<PAlloc>::pointer` is a pointer type.

*Effects:* Initializes an allocator `palloc` of type `PAlloc` with
`alloc`. Uses `palloc` to allocate storage for the smallest array of `U`
sufficient to provide storage for a coroutine state of size `size`, and
unspecified additional state necessary to ensure that `operator delete`
can later deallocate this memory block with an allocator equal to
`palloc`.

*Returns:* A pointer to the allocated storage.

``` cpp
void operator delete(void* pointer, size_t size) noexcept;
```

*Preconditions:* `pointer` was returned from an invocation of the above
overload of `operator new` with a size argument equal to `size`.

*Effects:* Deallocates the storage pointed to by `pointer` using an
allocator equal to that used to allocate it.

## Execution scope utilities <a id="exec.scope">[[exec.scope]]</a>

### Execution scope concepts <a id="exec.scope.concepts">[[exec.scope.concepts]]</a>

The `scope_token` concept defines the requirements on a type `Token`
that can be used to create associations between senders and an async
scope.

Let *test-sender* and *test-env* be unspecified types such that
`sender_in<test-sender, test-env>` is modeled.

``` cpp
namespace std::execution {
  template<class Token>
    concept scope_token =
      copyable<Token> &&
      requires(const Token token) {
        { token.try_associate() } -> same_as<bool>;
        { token.disassociate() } noexcept -> same_as<void>;
        { token.wrap(declval<test-sender>()) } -> sender_in<test-env>;
      };
}
```

A type `Token` models `scope_token` only if:

- no exceptions are thrown from copy construction, move construction,
  copy assignment, or move assignment of objects of type `Token`; and
- given an lvalue `token` of type (possibly const) `Token`, for all
  expressions `sndr` such that `decltype(({}sndr))` models `sender`:
  - `token.wrap(sndr)` is a valid expression,
  - `decltype(token.wrap(sndr))` models `sender`, and
  - `completion_signatures_of_t<decltype(token.wrap(sndr)), E>` contains
    the same completion signatures as
    `completion_signatures_of_t<decltype((sndr)), E>` for all types `E`
    such that `sender_in<decltype((sndr)), E>` is modeled.

### Counting Scopes <a id="exec.counting.scopes">[[exec.counting.scopes]]</a>

#### General <a id="exec.counting.scopes.general">[[exec.counting.scopes.general]]</a>

Scopes of type `simple_counting_scope` and `counting_scope` maintain
counts of associations. Let:

- `Scope` be either `simple_counting_scope` or `counting_scope`,
- `scope` be an object of type `Scope`,
- `tkn` be an object of type `Scope::token` obtained from
  `scope.get_token()`,
- `jsndr` be a sender obtained from `scope.join()`, and
- `op` be an operation state obtained from connecting `jsndr` to a
  receiver.

During its lifetime `scope` goes through different states which govern
what operations are allowed and the result of these operations:

- *`unused`*: a newly constructed object starts in the *`unused`* state.
- *`open`*: when `tkn.try_associate()` is called while `scope` is in the
  *`unused`* state, `scope` moves to the *`open`* state.
- *`open-and-joining`*: when the operation state `op` is started while
  `scope` is in the *`unused`* or *`open`* state, `scope` moves to the
  *`open-and-joining`* state.
- *`closed`*: when `scope.close()` is called while `scope` is in the
  *`open`* state, `scope` moves to the *`closed`* state.
- *`unused-and-closed`*: when `scope.close()` is called while `scope` is
  in the *`unused`* state, `scope` moves to the *`unused-and-closed`*
  state.
- *`closed-and-joining`*: when `scope.close()` is called while `scope`
  is in the *`open-and-joining`* state or the operation state `op` is
  started while `scope` is in the *`closed`* or *`unused-and-closed`*
  state, `scope` moves to the *`closed-and-joining`* state.
- *`joined`*: when the count of associations drops to zero while `scope`
  is in the *`open-and-joining`* or *`closed-and-joining`* state,
  `scope` moves to the *`joined`* state.

*Recommended practice:* For `simple_counting_scope` and
`counting_scope`, implementations should store the state and the count
of associations in a single member of type `size_t`.

Subclause [[exec.counting.scopes]] makes use of the following
exposition-only entities:

``` cpp
struct scope-join-t {};     // exposition only

enum scope-state-type {     // exposition only
  unused,                   // exposition only
  open,                     // exposition only
  closed,                   // exposition only
  open-and-joining,         // exposition only
  closed-and-joining,       // exposition only
  unused-and-closed,        // exposition only
  joined,                   // exposition only
};
```

The exposition-only class template *`impls-for`* [[exec.snd.expos]] is
specialized for *`scope-join-t`* as follows:

``` cpp
namespace std::execution {
  template<>
  struct impls-for<scope-join-t> : default-impls {
    template<class Scope, class Rcvr>
    struct state {                          // exposition only
      struct rcvr-t {                       // exposition only
        using receiver_concept = receiver_t;

        Rcvr& rcvr;                         // exposition only

        void set_value() && noexcept {
          execution::set_value(std::move(rcvr));
        }

        template<class E>
          void set_error(E&& e) && noexcept {
            execution::set_error(std::move(rcvr), std::forward<E>(e));
          }

        void set_stopped() && noexcept {
          execution::set_stopped(std::move(rcvr));
        }

        decltype(auto) get_env() const noexcept {
          return execution::get_env(rcvr);
        }
      };

      using sched-sender =                  // exposition only
        decltype(schedule(get_scheduler(get_env(declval<Rcvr&>()))));
      using op-t =                          // exposition only
        connect_result_t<sched-sender, rcvr-t>;

      Scope* scope;                         // exposition only
      Rcvr& receiver;                       // exposition only
      op-t op;                              // exposition only

      state(Scope* scope, Rcvr& rcvr)       // exposition only
        noexcept(nothrow-callable<connect_t, sched-sender, rcvr-t>)
        : scope(scope),
          receiver(rcvr),
          op(connect(schedule(get_scheduler(get_env(rcvr))), rcvr-t(rcvr))) {}

      void complete() noexcept {            // exposition only
        start(op);
      }

      void complete-inline() noexcept {     // exposition only
        set_value(std::move(receiver));
      }
    };

    static constexpr auto get-state =       // exposition only
      []<class Rcvr>(auto&& sender, Rcvr& receiver)
        noexcept(is_nothrow_constructible_v<state<Rcvr>, data-type<decltype(sender)>, Rcvr&>) {
        auto[_, self] = sender;
        return state(self, receiver);
      };

    static constexpr auto start =           // exposition only
      [](auto& s, auto&) noexcept {
        if (s.scope->start-join-sender(s))
          s.complete-inline();
      };
  };
}
```

#### Simple Counting Scope <a id="exec.scope.simple.counting">[[exec.scope.simple.counting]]</a>

##### General <a id="exec.scope.simple.counting.general">[[exec.scope.simple.counting.general]]</a>

``` cpp
namespace std::execution {
  class simple_counting_scope {
  public:
    // [exec.simple.counting.token], token
    struct token;

    static constexpr size_t max_associations = implementation-defined;

    // [exec.simple.counting.ctor], constructor and destructor
    simple_counting_scope() noexcept;
    simple_counting_scope(simple_counting_scope&&) = delete;
    ~simple_counting_scope();

    // [exec.simple.counting.mem], members
    token get_token() noexcept;
    void close() noexcept;
    sender auto join() noexcept;

  private:
    size_t count;                                       // exposition only
    scope-state-type state;                             // exposition only

    bool try-associate() noexcept;                      // exposition only
    void disassociate() noexcept;                       // exposition only
    template<class State>
      bool start-join-sender(State& state) noexcept;    // exposition only
  };
}
```

For purposes of determining the existence of a data race, `get_token`,
`close`, `join`, *`try-associate`*, *`disassociate`*, and
*`start-join-sender`* behave as atomic operations [[intro.multithread]].
These operations on a single object of type `simple_counting_scope`
appear to occur in a single total order.

##### Constructor and Destructor <a id="exec.simple.counting.ctor">[[exec.simple.counting.ctor]]</a>

``` cpp
simple_counting_scope() noexcept;
```

*Ensures:* *count* is `0` and *state* is *unused*.

``` cpp
~simple_counting_scope();
```

*Effects:* If *state* is not one of *joined*, *unused*, or
*unused-and-closed*, invokes `terminate`[[except.terminate]]. Otherwise,
has no effects.

##### Members <a id="exec.simple.counting.mem">[[exec.simple.counting.mem]]</a>

``` cpp
token get_token() noexcept;
```

*Returns:* An object `t` of type `simple_counting_scope::token` such
that `t.`*`scope`*` == this` is `true`.

``` cpp
void close() noexcept;
```

*Effects:* If *state* is

- *unused*, then changes *state* to *unused-and-closed*;
- *open*, then changes *state* to *closed*;
- *open-and-joining*, then changes *state* to *closed-and-joining*;
- otherwise, no effects.

*Ensures:* Any subsequent call to *`try-associate`*`()` on `*this`
returns `false`.

``` cpp
sender auto join() noexcept;
```

*Returns:* *`make-sender`*`(`*`scope-join-t`*`(), this)`.

``` cpp
bool try-associate() noexcept;
```

*Effects:* If *count* is equal to `max_associations`, then no effects.
Otherwise, if *state* is

- *unused*, then increments *count* and changes *state* to *open*;
- *open* or *open-and-joining*, then increments *count*;
- otherwise, no effects.

*Returns:* `true` if *count* was incremented, `false` otherwise.

``` cpp
void disassociate() noexcept;
```

*Preconditions:* *count* is greater than zero.

*Effects:* Decrements *count*. If *count* is zero after decrementing and
*state* is *open-and-joining* or *closed-and-joining*, changes *state*
to *joined* and calls *`complete`*`()` on all objects registered with
`*this`.

[*Note 1*: Calling *`complete`*`()` on any registered object can cause
`*this` to be destroyed. — *end note*]

``` cpp
template<class State>
  bool start-join-sender(State& st) noexcept;
```

*Effects:* If *state* is

- *unused*, *unused-and-closed*, or *joined*, then changes *state* to
  *joined* and returns `true`;
- *open* or *open-and-joining*, then changes *state* to
  *open-and-joining*, registers `st` with `*this` and returns `false`;
- *closed* or *closed-and-joining*, then changes *state* to
  *closed-and-joining*, registers `st` with `*this` and returns `false`.

##### Token <a id="exec.simple.counting.token">[[exec.simple.counting.token]]</a>

``` cpp
namespace std::execution {
  struct simple_counting_scope::token {
    template<sender Sender>
      Sender&& wrap(Sender&& snd) const noexcept;
    bool try_associate() const noexcept;
    void disassociate() const noexcept;

  private:
    simple_counting_scope* scope;   // exposition only
  };
}
```

``` cpp
template<sender Sender>
  Sender&& wrap(Sender&& snd) const noexcept;
```

*Returns:* `std::forward<Sender>(snd)`.

``` cpp
bool try_associate() const noexcept;
```

*Effects:* Equivalent to: `return `*`scope`*`->`*`try-associate`*`();`

``` cpp
void disassociate() const noexcept;
```

*Effects:* Equivalent to *`scope`*`->`*`disassociate`*`()`.

#### Counting Scope <a id="exec.scope.counting">[[exec.scope.counting]]</a>

``` cpp
namespace std::execution {
  class counting_scope {
  public:
    struct token {
      template<sender Sender>
        sender auto wrap(Sender&& snd) const noexcept(see below);
      bool try_associate() const noexcept;
      void disassociate() const noexcept;

    private:
      counting_scope* scope;                            // exposition only
    };

    static constexpr size_t max_associations = implementation-defined;

    counting_scope() noexcept;
    counting_scope(counting_scope&&) = delete;
    ~counting_scope();

    token get_token() noexcept;
    void close() noexcept;
    sender auto join() noexcept;
    void request_stop() noexcept;

  private:
    size_t count;                                       // exposition only
    scope-state-type state;                             // exposition only
    inplace_stop_source s_source;                       // exposition only

    bool try-associate() noexcept;                      // exposition only
    void disassociate() noexcept;                       // exposition only

    template<class State>
      bool start-join-sender(State& state) noexcept;    // exposition only
  };
}
```

`counting_scope` differs from `simple_counting_scope` by adding support
for cancellation. Unless specified below, the semantics of members of
`counting_scope` are the same as the corresponding members of
`simple_counting_scope`.

``` cpp
token get_token() noexcept;
```

*Returns:* An object `t` of type `counting_scope::token` such that
`t.`*`scope`*` == this` is `true`.

``` cpp
void request_stop() noexcept;
```

*Effects:* Equivalent to *`s_source`*`.request_stop()`.

*Remarks:* Calls to `request_stop` do not introduce data races.

``` cpp
template<sender Sender>
  sender auto counting_scope::token::wrap(Sender&& snd) const
    noexcept(is_nothrow_constructible_v<remove_cvref_t<Sender>, Sender>);
```

*Effects:* Equivalent to:

``` cpp
return stop-when(std::forward<Sender>(snd), scope->s_source.get_token());
```

## Parallel scheduler <a id="exec.par.scheduler">[[exec.par.scheduler]]</a>

``` cpp
namespace std::execution {
  class parallel_scheduler {
    unspecified
  };
}
```

`parallel_scheduler` models `scheduler`.

Let `sch` be an object of type `parallel_scheduler`, and let
`BACKEND-OF(sch)` be `*ptr`, where `sch` is associated with `ptr`.

The expression `get_forward_progress_guarantee(sch)` has the value
`forward_progress_guarantee::{}parallel`.

Let `sch2` be an object of type `parallel_scheduler`. Two objects `sch`
and `sch2` compare equal if and only if `BACKEND-OF(sch)` and
`BACKEND-OF(sch2)` refer to the same object.

Let `rcvr` be a receiver. A *proxy for `rcvr` with base `B`* is an
lvalue `r` of type `B` such that:

- `r.set_value()` has effects equivalent to
  `set_value(std::move(rcvr))`.
- `r.set_error(e)`, where `e` is an `exception_ptr` object, has effects
  equivalent to `set_error(std::move({}rcvr), std::move(e))`.
- `r.set_stopped()` has effects equivalent to
  `set_stopped(std::move(rcvr))`.

A *preallocated backend storage for a proxy* `r` is an object `s` of
type `span<byte>` such that the range `s` remains valid and may be
overwritten until one of `set_value`, `set_error`, or `set_stopped` is
called on `r`.

[*Note 1*: The storage referenced by `s` can be used as temporary
storage for operations launched via calls to
`parallel_scheduler_backend`. — *end note*]

A *bulk chunked proxy for `rcvr` with callable `f` and arguments `args`*
is a proxy `r` for `rcvr` with base
`system_context_replaceability::bulk_item_receiver_proxy` such that
`r.execute(i, j)` for indices `i` and `j` has effects equivalent to
`f(i, j, args...)`.

A *bulk unchunked proxy for `rcvr` with callable `f` and arguments
`args`* is a proxy `r` for `rcvr` with base
`system_context_replaceability::bulk_item_receiver_proxy` such that
`r.execute(i, i + 1)` for index `i` has effects equivalent to
`f(i, args...)`.

Let `b` be `BACKEND-OF(sch)`, let `sndr` be the object returned by
`schedule(sch)`, and let `rcvr` be a receiver. If `rcvr` is connected to
`sndr` and the resulting operation state is started, then:

- If `sndr` completes successfully, then `b.schedule(r, s)` is called,
  where
  - `r` is a proxy for `rcvr` with base
    `system_context_replaceability::receiver_proxy` and
  - `s` is a preallocated backend storage for `r`.
- All other completion operations are forwarded unchanged.

`parallel_scheduler` provides a customized implementation of the
`bulk_chunked` algorithm [[exec.bulk]]. If a receiver `rcvr` is
connected to the sender returned by `bulk_chunked(sndr, pol, shape, f)`
and the resulting operation state is started, then:

- If `sndr` completes with values `vals`, let `args` be a pack of lvalue
  subexpressions designating `vals`, then
  `b.schedule_bulk_chunked(shape, r, s)` is called, where
  - `r` is a bulk chunked proxy for `rcvr` with callable `f` and
    arguments `args` and
  - `s` is a preallocated backend storage for `r`.
- All other completion operations are forwarded unchanged.

[*Note 2*: Customizing the behavior of `bulk_chunked` affects the
default implementation of `bulk`. — *end note*]

`parallel_scheduler` provides a customized implementation of the
`bulk_unchunked` algorithm [[exec.bulk]]. If a receiver `rcvr` is
connected to the sender returned by
`bulk_unchunked(sndr, pol, shape, f)` and the resulting operation state
is started, then:

- If `sndr` completes with values `vals`, let `args` be a pack of lvalue
  subexpressions designating `vals`, then
  `b.schedule_bulk_unchunked(shape, r, s)` is called, where
  - `r` is a bulk unchunked proxy for `rcvr` with callable `f` and
    arguments `args` and
  - `s` is a preallocated backend storage for `r`.
- All other completion operations are forwarded unchanged.

``` cpp
parallel_scheduler get_parallel_scheduler();
```

*Effects:* Let `eb` be the result of
`system_context_replaceability::query_parallel_scheduler_backend()`. If
`eb == nullptr` is `true`, calls `terminate`[[except.terminate]].
Otherwise, returns a `parallel_scheduler` object associated with `eb`.

## Namespace `system_context_replaceability` <a id="exec.sysctxrepl">[[exec.sysctxrepl]]</a>

### General <a id="exec.sysctxrepl.general">[[exec.sysctxrepl.general]]</a>

Facilities in the `system_context_replaceability` namespace allow users
to replace the default implementation of `parallel_scheduler`.

### Receiver proxies <a id="exec.sysctxrepl.recvproxy">[[exec.sysctxrepl.recvproxy]]</a>

``` cpp
namespace std::execution::system_context_replaceability {
  struct receiver_proxy {
    virtual ~receiver_proxy() = default;

  protected:
    virtual bool query-env(unspecified) noexcept = 0;   // exposition only

  public:
    virtual void set_value() noexcept = 0;
    virtual void set_error(exception_ptr) noexcept = 0;
    virtual void set_stopped() noexcept = 0;

    template<class P, class-type Query>
      optional<P> try_query(Query q) noexcept;
  };

  struct bulk_item_receiver_proxy : receiver_proxy {
    virtual void execute(size_t, size_t) noexcept = 0;
  };
}
```

`receiver_proxy` represents a receiver that will be notified by the
implementations of `parallel_scheduler_backend` to trigger the
completion operations. `bulk_item_receiver_proxy` is derived from
`receiver_proxy` and is used for `bulk_chunked` and `bulk_unchunked`
customizations that will also receive notifications from implementations
of `parallel_scheduler_backend` corresponding to different iterations.

``` cpp
template<class P, class-type Query>
  optional<P> try_query(Query q) noexcept;
```

*Mandates:* `P` is a cv-unqualified non-array object type.

*Returns:* Let `env` be the environment of the receiver represented by
`*this`. If

- `Query` is not a member of an implementation-defined set of supported
  queries; or
- `P` is not a member of an implementation-defined set of supported
  result types for `Query`; or
- the expression `q(env)` is not well-formed or does not have type cv
  `P`,

then returns `nullopt`. Otherwise, returns `q(env)`.

*Remarks:* `get_stop_token_t` is in the implementation-defined set of
supported queries, and `inplace_stop_token` is a member of the
implementation-defined set of supported result types for
`get_stop_token_t`.

### `query_parallel_scheduler_backend` <a id="exec.sysctxrepl.query">[[exec.sysctxrepl.query]]</a>

``` cpp
shared_ptr<parallel_scheduler_backend> query_parallel_scheduler_backend();
```

`query_parallel_scheduler_backend()` returns the implementation object
for a parallel scheduler.

*Returns:* A non-null shared pointer to an object that implements the
`parallel_scheduler_backend` interface.

*Remarks:* This function is replaceable [[term.replaceable.function]].

### Class `parallel_scheduler_backend` <a id="exec.sysctxrepl.psb">[[exec.sysctxrepl.psb]]</a>

``` cpp
namespace std::execution::system_context_replaceability {
  struct parallel_scheduler_backend {
    virtual ~parallel_scheduler_backend() = default;

    virtual void schedule(receiver_proxy&, span<byte>) noexcept = 0;
    virtual void schedule_bulk_chunked(size_t, bulk_item_receiver_proxy&,
                                       span<byte>) noexcept = 0;
    virtual void schedule_bulk_unchunked(size_t, bulk_item_receiver_proxy&,
                                         span<byte>) noexcept = 0;
  };
}
```

``` cpp
virtual void schedule(receiver_proxy& r, span<byte> s) noexcept = 0;
```

*Preconditions:* The ends of the lifetimes of `*this`, the object
referred to by `r`, and any storage referenced by `s` all happen after
the beginning of the evaluation of the call to `set_value`, `set_error`,
or `set_done` on `r` (see below).

*Effects:* A derived class shall implement this function such that:

- One of the following expressions is evaluated:
  - `r.set_value()`, if no error occurs, and the work is successful;
  - `r.set_error(eptr)`, if an error occurs, where `eptr` is an object
    of type `exception_ptr`;
  - `r.set_stopped()`, if the work is canceled.
- Any call to `r.set_value()` happens on an execution agent of the
  execution context represented by `*this`.

*Remarks:* The storage referenced by `s` may be used by `*this` as
temporary storage for the duration of the operation launched by this
call.

``` cpp
virtual void schedule_bulk_chunked(size_t n, bulk_item_receiver_proxy& r,
                                   span<byte> s) noexcept = 0;
```

*Preconditions:* The ends of the lifetimes of `*this`, the object
referred to by `r`, and any storage referenced by `s` all happen after
the beginning of the evaluation of one of the expressions below.

*Effects:* A derived class shall implement this function such that:

- Eventually, one of the following expressions is evaluated:
  - `r.set_value()`, if no error occurs, and the work is successful;
  - `r.set_error(eptr)`, if an error occurs, where `eptr` is an object
    of type `exception_ptr`;
  - `r.set_stopped()`, if the work is canceled.
- If `r.execute(b, e)` is called, then `b` and `e` are in the range
  \[`0`, `n`\] and `b` < `e`.
- For each i in \[`0`, `n`), there is at most one call to
  `r.execute(b, e)` such that i is in the range \[`b`, `e`).
- If `r.set_value()` is called, then for each i in \[`0`, `n`), there is
  exactly one call to `r.execute(b, e)` such that i is in the range
  \[`b`, `e`).
- All calls to `execute` on `r` happen before the call to either
  `set_value`, `set_error`, or `set_stopped` on `r`.
- All calls to `execute` and `set_value` on `r` are made on execution
  agents of the execution context represented by `*this`.

*Remarks:* The storage referenced by `s` may be used by `*this` as
temporary storage for the duration of the operation launched by this
call.

``` cpp
virtual void schedule_bulk_unchunked(size_t n, bulk_item_receiver_proxy& r,
                                     span<byte> s) noexcept = 0;
```

*Preconditions:* The ends of the lifetimes of `*this`, the object
referred to by `r`, and any storage referenced by `s` all happen after
the beginning of the evaluation of one of the expressions below.

*Effects:* A derived class shall implement this function such that:

- Eventually, one of the following expressions is evaluated:
  - `r.set_value()`, if no error occurs, and the work is successful;
  - `r.set_error(eptr)`, if an error occurs, where `eptr` is an object
    of type `exception_ptr`;
  - `r.set_stopped()`, if the work is canceled.
- If `r.execute(b, e)` is called, then `b` is in the range \[`0`, `n`)
  and `e` is equal to `b + 1`. For each i in \[`0`, `n`), there is at
  most one call to `r.execute(`i`, `i` + 1)`.
- If `r.set_value()` is called, then for each i in \[`0`, `n`), there is
  exactly one call to `r.execute(`i`, `i` + 1)`.
- All calls to `execute` on `r` happen before the call to either
  `set_value`, `set_error`, or `set_stopped` on `r`.
- All calls to `execute` and `set_value` on `r` are made on execution
  agents of the execution context represented by `*this`.

*Remarks:* The storage referenced by `s` may be used by `*this` as
temporary storage for the duration of the operation launched by this
call.

<!-- Link reference definitions -->
[algorithms.parallel.exec]: algorithms.md#algorithms.parallel.exec
[allocator.requirements.general]: library.md#allocator.requirements.general
[basic.def.odr]: basic.md#basic.def.odr
[concepts.equality]: concepts.md#concepts.equality
[customization.point.object]: library.md#customization.point.object
[dcl.init]: dcl.md#dcl.init
[dcl.struct.bind]: dcl.md#dcl.struct.bind
[defns.block]: intro.md#defns.block
[except.terminate]: except.md#except.terminate
[exec]: #exec
[exec.adapt]: #exec.adapt
[exec.adapt.general]: #exec.adapt.general
[exec.adapt.obj]: #exec.adapt.obj
[exec.affine.on]: #exec.affine.on
[exec.as.awaitable]: #exec.as.awaitable
[exec.associate]: #exec.associate
[exec.async.ops]: #exec.async.ops
[exec.awaitable]: #exec.awaitable
[exec.bulk]: #exec.bulk
[exec.cmplsig]: #exec.cmplsig
[exec.connect]: #exec.connect
[exec.consumers]: #exec.consumers
[exec.continues.on]: #exec.continues.on
[exec.coro.util]: #exec.coro.util
[exec.counting.scopes]: #exec.counting.scopes
[exec.counting.scopes.general]: #exec.counting.scopes.general
[exec.ctx]: #exec.ctx
[exec.domain.default]: #exec.domain.default
[exec.env]: #exec.env
[exec.envs]: #exec.envs
[exec.factories]: #exec.factories
[exec.fwd.env]: #exec.fwd.env
[exec.general]: #exec.general
[exec.get.allocator]: #exec.get.allocator
[exec.get.await.adapt]: #exec.get.await.adapt
[exec.get.compl.sched]: #exec.get.compl.sched
[exec.get.delegation.scheduler]: #exec.get.delegation.scheduler
[exec.get.domain]: #exec.get.domain
[exec.get.env]: #exec.get.env
[exec.get.fwd.progress]: #exec.get.fwd.progress
[exec.get.scheduler]: #exec.get.scheduler
[exec.get.stop.token]: #exec.get.stop.token
[exec.getcomplsigs]: #exec.getcomplsigs
[exec.inline.scheduler]: #exec.inline.scheduler
[exec.into.variant]: #exec.into.variant
[exec.just]: #exec.just
[exec.let]: #exec.let
[exec.on]: #exec.on
[exec.opstate]: #exec.opstate
[exec.opstate.general]: #exec.opstate.general
[exec.opstate.start]: #exec.opstate.start
[exec.par.scheduler]: #exec.par.scheduler
[exec.pos]: #exec.pos
[exec.prop]: #exec.prop
[exec.queries]: #exec.queries
[exec.queryable]: #exec.queryable
[exec.queryable.concept]: #exec.queryable.concept
[exec.queryable.general]: #exec.queryable.general
[exec.read.env]: #exec.read.env
[exec.recv]: #exec.recv
[exec.recv.concepts]: #exec.recv.concepts
[exec.run.loop]: #exec.run.loop
[exec.run.loop.ctor]: #exec.run.loop.ctor
[exec.run.loop.general]: #exec.run.loop.general
[exec.run.loop.members]: #exec.run.loop.members
[exec.run.loop.types]: #exec.run.loop.types
[exec.sched]: #exec.sched
[exec.schedule]: #exec.schedule
[exec.schedule.from]: #exec.schedule.from
[exec.scope]: #exec.scope
[exec.scope.concepts]: #exec.scope.concepts
[exec.scope.counting]: #exec.scope.counting
[exec.scope.simple.counting]: #exec.scope.simple.counting
[exec.scope.simple.counting.general]: #exec.scope.simple.counting.general
[exec.set.error]: #exec.set.error
[exec.set.stopped]: #exec.set.stopped
[exec.set.value]: #exec.set.value
[exec.simple.counting.ctor]: #exec.simple.counting.ctor
[exec.simple.counting.mem]: #exec.simple.counting.mem
[exec.simple.counting.token]: #exec.simple.counting.token
[exec.snd]: #exec.snd
[exec.snd.apply]: #exec.snd.apply
[exec.snd.concepts]: #exec.snd.concepts
[exec.snd.expos]: #exec.snd.expos
[exec.snd.general]: #exec.snd.general
[exec.snd.transform]: #exec.snd.transform
[exec.snd.transform.env]: #exec.snd.transform.env
[exec.spawn]: #exec.spawn
[exec.spawn.future]: #exec.spawn.future
[exec.starts.on]: #exec.starts.on
[exec.stop.when]: #exec.stop.when
[exec.stopped.err]: #exec.stopped.err
[exec.stopped.opt]: #exec.stopped.opt
[exec.summary]: #exec.summary
[exec.sync.wait]: #exec.sync.wait
[exec.sync.wait.var]: #exec.sync.wait.var
[exec.sysctxrepl]: #exec.sysctxrepl
[exec.sysctxrepl.general]: #exec.sysctxrepl.general
[exec.sysctxrepl.psb]: #exec.sysctxrepl.psb
[exec.sysctxrepl.query]: #exec.sysctxrepl.query
[exec.sysctxrepl.recvproxy]: #exec.sysctxrepl.recvproxy
[exec.task]: #exec.task
[exec.task.scheduler]: #exec.task.scheduler
[exec.then]: #exec.then
[exec.unstoppable]: #exec.unstoppable
[exec.when.all]: #exec.when.all
[exec.with.awaitable.senders]: #exec.with.awaitable.senders
[exec.write.env]: #exec.write.env
[execution.syn]: #execution.syn
[expr.await]: expr.md#expr.await
[expr.const]: expr.md#expr.const
[func.def]: utilities.md#func.def
[func.require]: utilities.md#func.require
[function.objects]: utilities.md#function.objects
[intro.multithread]: basic.md#intro.multithread
[intro.progress]: basic.md#intro.progress
[intro.races]: basic.md#intro.races
[meta.trans.other]: meta.md#meta.trans.other
[namespace.std]: library.md#namespace.std
[task.class]: #task.class
[task.members]: #task.members
[task.overview]: #task.overview
[task.promise]: #task.promise
[task.state]: #task.state
[term.replaceable.function]: dcl.md#term.replaceable.function
[thread.req.lockable.general]: thread.md#thread.req.lockable.general
