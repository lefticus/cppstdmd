# Exception handling <a id="except">[except]</a>

## Preamble <a id="except.pre">[except.pre]</a>

Exception handling provides a way of transferring control and
information from a point in the execution of a thread to an exception
handler associated with a point previously passed by the execution. A
handler will be invoked only by throwing an exception in code executed
in the handler’s try block or in functions called from the handler’s try
block.

``` bnf
try-block:
    \texttt{try} compound-statement handler-seq
```

``` bnf
function-try-block:
    \texttt{try} [ctor-initializer] compound-statement handler-seq
```

``` bnf
handler-seq:
    handler [handler-seq]
```

``` bnf
handler:
    \texttt{catch} '(' exception-declaration ')' compound-statement
```

``` bnf
exception-declaration:
    [attribute-specifier-seq] type-specifier-seq declarator
    [attribute-specifier-seq] type-specifier-seq [abstract-declarator]
    '...'
```

The optional *attribute-specifier-seq* in an *exception-declaration*
appertains to the parameter of the catch clause [except.handle].

A *try-block* is a *statement* [stmt.pre].

\[*Note 1*: Within this Clause “try block” is taken to mean both
*try-block* and *function-try-block*. — *end note*\]

The *compound-statement* of a try block or of a handler is a
control-flow-limited statement [stmt.label].

\[*Example 1*:

``` cpp
void f() {
  goto l1;          // error
  goto l2;          // error
  try {
    goto l1;        // OK
    goto l2;        // error
    l1: ;
  } catch (...) {
    l2: ;
    goto l1;        // error
    goto l2;        // OK
  }
}
```

— *end example*\]

A `goto`, `break`, `return`, or `continue` statement can be used to
transfer control out of a try block or handler. When this happens, each
variable declared in the try block will be destroyed in the context that
directly contains its declaration.

\[*Example 2*:

``` cpp
lab:  try {
  T1 t1;
  try {
    T2 t2;
    if (condition)
      goto lab;
    } catch(...) { /* handler 2 */ }
  } catch(...) { /* handler 1 */ }
```

Here, executing `goto lab;` will destroy first `t2`, then `t1`, assuming
the *condition* does not declare a variable. Any exception thrown while
destroying `t2` will result in executing `handler 2`; any exception
thrown while destroying `t1` will result in executing `handler 1`.

— *end example*\]

A *function-try-block* associates a *handler-seq* with the
*ctor-initializer*, if present, and the *compound-statement*. An
exception thrown during the execution of the *compound-statement* or,
for constructors and destructors, during the initialization or
destruction, respectively, of the class’s subobjects, transfers control
to a handler in a *function-try-block* in the same way as an exception
thrown during the execution of a *try-block* transfers control to other
handlers.

\[*Example 3*:

``` cpp
int f(int);
class C {
  int i;
  double d;
public:
  C(int, double);
};

C::C(int ii, double id)
try : i(f(ii)), d(id) {
    // constructor statements
} catch (...) {
    // handles exceptions thrown from the ctor-initializer and from the constructor statements
}
```

— *end example*\]

In this Clause, “before” and “after” refer to the “sequenced before”
relation [intro.execution].

## Throwing an exception <a id="except.throw">[except.throw]</a>

Throwing an exception transfers control to a handler.

\[*Note 1*: An exception can be thrown from one of the following
contexts: *throw-expression* [expr.throw], allocation functions
[basic.stc.dynamic.allocation], `dynamic_cast` [expr.dynamic.cast],
`typeid` [expr.typeid], *new-expression* [expr.new], and standard
library functions [structure.specifications]. — *end note*\]

An object is passed and the type of that object determines which
handlers can catch it.

\[*Example 1*:

``` cpp
throw "Help!";
```

can be caught by a *handler* of `const` `char*` type:

``` cpp
try {
    // ...
} catch(const char* p) {
    // handle character string exceptions here
}
```

and

``` cpp
class Overflow {
public:
    Overflow(char,double,double);
};

void f(double x) {
    throw Overflow('+',x,3.45e107);
}
```

can be caught by a handler for exceptions of type `Overflow`:

``` cpp
try {
    f(1.2);
} catch(Overflow& oo) {
    // handle exceptions of type Overflow here
}
```

— *end example*\]

When an exception is thrown, control is transferred to the nearest
handler with a matching type [except.handle]; “nearest” means the
handler for which the *compound-statement* or *ctor-initializer*
following the `try` keyword was most recently entered by the thread of
control and not yet exited.

Throwing an exception copy-initializes [dcl.init,class.copy.ctor] a
temporary object, called the *exception object*. If the type of the
exception object would be an incomplete type, an abstract class type
[class.abstract], or a pointer to an incomplete type other than
cv `void` the program is ill-formed.

The memory for the exception object is allocated in an unspecified way,
except as noted in  [basic.stc.dynamic.allocation]. If a handler exits
by rethrowing, control is passed to another handler for the same
exception object. The points of potential destruction for the exception
object are:

- when an active handler for the exception exits by any means other than
  rethrowing, immediately after the destruction of the object (if any)
  declared in the *exception-declaration* in the handler;

- when an object of type `std::exception_ptr` [propagation] that refers
  to the exception object is destroyed, before the destructor of
  `std::exception_ptr` returns.

Among all points of potential destruction for the exception object,
there is an unspecified last one where the exception object is
destroyed. All other points happen before that last one [intro.races].

\[*Note 2*: No other thread synchronization is implied in exception
handling. — *end note*\]

The implementation may then deallocate the memory for the exception
object; any such deallocation is done in an unspecified way.

\[*Note 3*: A thrown exception does not propagate to other threads
unless caught, stored, and rethrown using appropriate library functions;
see  [propagation] and  [futures]. — *end note*\]

When the thrown object is a class object, the constructor selected for
the copy-initialization as well as the constructor selected for a
copy-initialization considering the thrown object as an lvalue shall be
non-deleted and accessible, even if the copy/move operation is elided
[class.copy.elision]. The destructor is potentially invoked
[class.dtor].

An exception is considered caught when a handler for that exception
becomes active [except.handle].

\[*Note 4*: An exception can have active handlers and still be
considered uncaught if it is rethrown. — *end note*\]

If the exception handling mechanism handling an uncaught exception
[except.uncaught] directly invokes a function that exits via an
exception, the function `std::terminate` is invoked [except.terminate].

\[*Example 2*:

``` cpp
struct C {
  C() { }
  C(const C&) {
    if (std::uncaught_exceptions()) {
      throw 0;      // throw during copy to handler's exception-declaration object[except.handle]
    }
  }
};

int main() {
  try {
    throw C();      // calls std::terminate if construction of the handler's
                    // exception-declaration object is not elided[class.copy.elision]
  } catch(C) { }
}
```

— *end example*\]

\[*Note 5*: If a destructor directly invoked by stack unwinding exits
via an exception, `std::terminate` is invoked. — *end note*\]

## Constructors and destructors <a id="except.ctor">[except.ctor]</a>

As control passes from the point where an exception is thrown to a
handler, objects are destroyed by a process, specified in this
subclause, called *stack unwinding*.

Each object with automatic storage duration is destroyed if it has been
constructed, but not yet destroyed, since the try block was entered. If
an exception is thrown during the destruction of temporaries or local
variables for a `return` statement [stmt.return], the destructor for the
returned object (if any) is also invoked. The objects are destroyed in
the reverse order of the completion of their construction.

\[*Example 1*:

``` cpp
struct A { };

struct Y { ~Y() noexcept(false) { throw 0; } };

A f() {
  try {
    A a;
    Y y;
    A b;
    return {};      // \#1
  } catch (...) {
  }
  return {};        // \#2
}
```

At \#1, the returned object of type `A` is constructed. Then, the local
variable `b` is destroyed [stmt.jump]. Next, the local variable `y` is
destroyed, causing stack unwinding, resulting in the destruction of the
returned object, followed by the destruction of the local variable `a`.
Finally, the returned object is constructed again at \#2.

— *end example*\]

If the initialization of an object other than by delegating constructor
is terminated by an exception, the destructor is invoked for each of the
object’s subobjects that were known to be initialized by the object’s
initialization and whose initialization has completed [dcl.init].

\[*Note 1*: If such an object has a reference member that extends the
lifetime of a temporary object, this ends the lifetime of the reference
member, so the lifetime of the temporary object is effectively not
extended. — *end note*\]

A subobject is *known to be initialized* if its initialization is
specified

- in [class.base.init] for initialization by constructor,

- in [class.copy.ctor] for initialization by defaulted copy/move
  constructor,

- in [class.inhctor.init] for initialization by inherited constructor,

- in [dcl.init.aggr] for aggregate initialization,

- in [expr.prim.lambda.capture] for the initialization of the closure
  object when evaluating a *lambda-expression*,

- in [dcl.init.general] for default-initialization,
  value-initialization, or direct-initialization of an array.

\[*Note 2*: This includes virtual base class subobjects if the
initialization is for a complete object, and can include variant members
that were nominated explicitly by a *mem-initializer* or
*designated-initializer-clause* or that have a default member
initializer. — *end note*\]

If the destructor of an object is terminated by an exception, each
destructor invocation that would be performed after executing the body
of the destructor [class.dtor] and that has not yet begun execution is
performed.

\[*Note 3*: This includes virtual base class subobjects if the
destructor was invoked for a complete object. — *end note*\]

The subobjects are destroyed in the reverse order of the completion of
their construction. Such destruction is sequenced before entering a
handler of the *function-try-block* of the constructor or destructor, if
any.

If the *compound-statement* of the *function-body* of a delegating
constructor for an object exits via an exception, the object’s
destructor is invoked. Such destruction is sequenced before entering a
handler of the *function-try-block* of a delegating constructor for that
object, if any.

\[*Note 4*: If the object was allocated by a *new-expression*
[expr.new], the matching deallocation function
[basic.stc.dynamic.deallocation], if any, is called to free the storage
occupied by the object. — *end note*\]

## Handling an exception <a id="except.handle">[except.handle]</a>

The *exception-declaration* in a *handler* describes the type(s) of
exceptions that can cause that *handler* to be entered. The
*exception-declaration* shall not denote an incomplete type, an abstract
class type, or an rvalue reference type. The *exception-declaration*
shall not denote a pointer or reference to an incomplete type, other
than “pointer to cv `void`”.

A handler of type “array of `T`” or function type `T` is adjusted to be
of type “pointer to `T`”.

A *handler* is a match for an exception object of type `E` if

- The *handler* is of type cv `T` or cv `T&` and `E` and `T` are the
  same type (ignoring the top-level *cv-qualifier*), or

- the *handler* is of type cv `T` or cv `T&` and `T` is an unambiguous
  public base class of `E`, or

- the *handler* is of type cv `T` or `const T&` where `T` is a pointer
  or pointer-to-member type and `E` is a pointer or pointer-to-member
  type that can be converted to `T` by one or more of

  - a standard pointer conversion [conv.ptr] not involving conversions
    to pointers to private or protected or ambiguous classes

  - a function pointer conversion [conv.fctptr]

  - a qualification conversion [conv.qual], or

- the *handler* is of type cv `T` or `const T&` where `T` is a pointer
  or pointer-to-member type and `E` is `std::nullptr_t`.

\[*Note 1*: A *throw-expression* whose operand is an integer literal
with value zero does not match a handler of pointer or pointer-to-member
type. A handler of reference to array or function type is never a match
for any exception object [expr.throw]. — *end note*\]

\[*Example 1*:

``` cpp
class Matherr { ... virtual void vf(); };
class Overflow: public Matherr { ... };
class Underflow: public Matherr { ... };
class Zerodivide: public Matherr { ... };

void f() {
  try {
    g();
  } catch (Overflow oo) {
    // ...
  } catch (Matherr mm) {
    // ...
  }
}
```

Here, the `Overflow` handler will catch exceptions of type `Overflow`
and the `Matherr` handler will catch exceptions of type `Matherr` and of
all types publicly derived from `Matherr` including exceptions of type
`Underflow` and `Zerodivide`.

— *end example*\]

The handlers for a try block are tried in order of appearance.

\[*Note 2*: This makes it possible to write handlers that can never be
executed, for example by placing a handler for a final derived class
after a handler for a corresponding unambiguous public base
class. — *end note*\]

A `...` in a handler’s *exception-declaration* functions similarly to
`...` in a function parameter declaration; it specifies a match for any
exception. If present, a `...` handler shall be the last handler for its
try block.

If no match is found among the handlers for a try block, the search for
a matching handler continues in a dynamically surrounding try block of
the same thread.

A handler is considered *active* when initialization is complete for the
parameter (if any) of the catch clause.

\[*Note 3*: The stack will have been unwound at that
point. — *end note*\]

Also, an implicit handler is considered active when the function
`std::terminate` is entered due to a throw. A handler is no longer
considered active when the catch clause exits.

The exception with the most recently activated handler that is still
active is called the *currently handled exception*.

If no matching handler is found, the function `std::terminate` is
invoked; whether or not the stack is unwound before this invocation of
`std::terminate` is *implementation-defined* [except.terminate].

Referring to any non-static member or base class of an object in the
handler for a *function-try-block* of a constructor or destructor for
that object results in undefined behavior.

Exceptions thrown in destructors of objects with static storage duration
or in constructors of objects associated with non-block variables with
static storage duration are not caught by a *function-try-block* on the
`main` function [basic.start.main]. Exceptions thrown in destructors of
objects with thread storage duration or in constructors of objects
associated with non-block variables with thread storage duration are not
caught by a *function-try-block* on the initial function of the thread.

If a `return` statement [stmt.return] appears in a handler of the
*function-try-block* of a constructor, the program is ill-formed.

The currently handled exception is rethrown if control reaches the end
of a handler of the *function-try-block* of a constructor or destructor.
Otherwise, flowing off the end of the *compound-statement* of a
*handler* of a *function-try-block* is equivalent to flowing off the end
of the *compound-statement* of that function (see [stmt.return]).

The variable declared by the *exception-declaration*, of type cv `T` or
cv `T&`, is initialized from the exception object, of type `E`, as
follows:

- if `T` is a base class of `E`, the variable is copy-initialized
  [dcl.init] from an lvalue of type `T` designating the corresponding
  base class subobject of the exception object;

- otherwise, the variable is copy-initialized [dcl.init] from an lvalue
  of type `E` designating the exception object.

The lifetime of the variable ends when the handler exits, after the
destruction of any objects with automatic storage duration initialized
within the handler.

When the handler declares an object, any changes to that object will not
affect the exception object. When the handler declares a reference to an
object, any changes to the referenced object are changes to the
exception object and will have effect should that object be rethrown.

## Exception specifications <a id="except.spec">[except.spec]</a>

The predicate indicating whether a function cannot exit via an exception
is called the *exception specification* of the function. If the
predicate is false, the function has a potentially-throwing!exception
specification, otherwise it has a
*non-throwing exception specification*. The exception specification is
either defined implicitly, or defined explicitly by using a
*noexcept-specifier* as a suffix of a function declarator [dcl.fct].

``` bnf
noexcept-specifier:
    \texttt{noexcept} '(' constant-expression ')'
    \texttt{noexcept}
```

In a *noexcept-specifier*, the *constant-expression*, if supplied, shall
be a contextually converted constant expression of type `bool`
[expr.const]; that constant expression is the exception specification of
the function type in which the *noexcept-specifier* appears. A `(` token
that follows `noexcept` is part of the *noexcept-specifier* and does not
commence an initializer [dcl.init]. The *noexcept-specifier* `noexcept`
without a *constant-expression* is equivalent to the
*noexcept-specifier* `noexcept(true)`.

\[*Example 1*:

``` cpp
void f() noexcept(sizeof(char[2])); // error: narrowing conversion of value 2 to type bool
void g() noexcept(sizeof(char));    // OK, conversion of value 1 to type bool is non-narrowing
```

— *end example*\]

If a declaration of a function does not have a *noexcept-specifier*, the
declaration has a potentially throwing exception specification unless it
is a destructor or a deallocation function or is defaulted on its first
declaration, in which cases the exception specification is as specified
below and no other declaration for that function shall have a
*noexcept-specifier*. In an explicit instantiation [temp.explicit] a
*noexcept-specifier* may be specified, but is not required. If a
*noexcept-specifier* is specified in an explicit instantiation, the
exception specification shall be the same as the exception specification
of all other declarations of that function. A diagnostic is required
only if the exception specifications are not the same within a single
translation unit.

If a virtual function has a non-throwing exception specification, all
declarations, including the definition, of any function that overrides
that virtual function in any derived class shall have a non-throwing
exception specification, unless the overriding function is defined as
deleted.

\[*Example 2*:

``` cpp
struct B {
  virtual void f() noexcept;
  virtual void g();
  virtual void h() noexcept = delete;
};

struct D: B {
  void f();                     // error
  void g() noexcept;            // OK
  void h() = delete;            // OK
};
```

The declaration of `D::f` is ill-formed because it has a
potentially-throwing exception specification, whereas `B::f` has a
non-throwing exception specification.

— *end example*\]

Whenever an exception is thrown and the search for a handler
[except.handle] encounters the outermost block of a function with a
non-throwing exception specification, the function `std::terminate` is
invoked [except.terminate].

\[*Note 1*: An implementation is not permitted to reject an expression
merely because, when executed, it throws or might throw an exception
from a function with a non-throwing exception
specification. — *end note*\]

\[*Example 3*:

``` cpp
extern void f();                // potentially-throwing

void g() noexcept {
  f();                          // valid, even if f throws
  throw 42;                     // valid, effectively a call to std::terminate
}
```

The call to `f` is well-formed despite the possibility for it to throw
an exception.

— *end example*\]

An expression E is *potentially-throwing* if

- E is a function call [expr.call] whose *postfix-expression* has a
  function type, or a pointer-to-function type, with a
  potentially-throwing exception specification, or

- E implicitly invokes a function (such as an overloaded operator, an
  allocation function in a *new-expression*, a constructor for a
  function argument, or a destructor if E is a full-expression
  [intro.execution]) that has a potentially-throwing exception
  specification, or

- E is a *throw-expression* [expr.throw], or

- E is a `dynamic_cast` expression that casts to a reference type and
  requires a runtime check [expr.dynamic.cast], or

- E is a `typeid` expression applied to a (possibly parenthesized)
  built-in unary `*` operator applied to a pointer to a polymorphic
  class type [expr.typeid], or

- any of the immediate subexpressions [intro.execution] of E is
  potentially-throwing.

An implicitly-declared constructor for a class `X`, or a constructor
without a *noexcept-specifier* that is defaulted on its first
declaration, has a potentially-throwing exception specification if and
only if any of the following constructs is potentially-throwing:

- the invocation of a constructor selected by overload resolution in the
  implicit definition of the constructor for class `X` to initialize a
  potentially constructed subobject, or

- a subexpression of such an initialization, such as a default argument
  expression, or,

- for a default constructor, a default member initializer.

\[*Note 2*: Even though destructors for fully-constructed subobjects are
invoked when an exception is thrown during the execution of a
constructor [except.ctor], their exception specifications do not
contribute to the exception specification of the constructor, because an
exception thrown from such a destructor would call the function
`std::terminate` rather than escape the constructor
[except.throw,except.terminate]. — *end note*\]

The exception specification for an implicitly-declared destructor, or a
destructor without a *noexcept-specifier*, is potentially-throwing if
and only if any of the destructors for any of its potentially
constructed subobjects has a potentially-throwing exception
specification or the destructor is virtual and the destructor of any
virtual base class has a potentially-throwing exception specification.

The exception specification for an implicitly-declared assignment
operator, or an assignment-operator without a *noexcept-specifier* that
is defaulted on its first declaration, is potentially-throwing if and
only if the invocation of any assignment operator in the implicit
definition is potentially-throwing.

A deallocation function [basic.stc.dynamic.deallocation] with no
explicit *noexcept-specifier* has a non-throwing exception
specification.

The exception specification for a comparison operator function
[over.binary] without a *noexcept-specifier* that is defaulted on its
first declaration is potentially-throwing if and only if any expression
in the implicit definition is potentially-throwing.

\[*Example 4*:

``` cpp
struct A {
  A(int = (A(5), 0)) noexcept;
  A(const A&) noexcept;
  A(A&&) noexcept;
  ~A();
};
struct B {
  B() noexcept;
  B(const B&) = default;        // implicit exception specification is noexcept(\keyword{true)}
  B(B&&, int = (throw 42, 0)) noexcept;
  ~B() noexcept(false);
};
int n = 7;
struct D : public A, public B {
    int * p = new int[n];
    // D::D() potentially-throwing, as the new operator may throw bad_alloc or bad_array_new_length
    // D::D(const D\&) non-throwing
    // D::D(D\&\&) potentially-throwing, as the default argument for B's constructor may throw
    // D::\~D() potentially-throwing
};
```

Furthermore, if `A::~{}A()` were virtual, the program would be
ill-formed since a function that overrides a virtual function from a
base class shall not have a potentially-throwing exception specification
if the base class function has a non-throwing exception specification.

— *end example*\]

An exception specification is considered to be *needed* when:

- in an expression, the function is selected by overload resolution
  [over.match,over.over];

- the function is odr-used [term.odr.use] or, if it appears in an
  unevaluated operand, would be odr-used if the expression were
  potentially-evaluated;

- the exception specification is compared to that of another declaration
  (e.g., an explicit specialization or an overriding virtual function);

- the function is defined; or

- the exception specification is needed for a defaulted function that
  calls the function.

  \[*Note 1*: A defaulted declaration does not require the exception
  specification of a base member function to be evaluated until the
  implicit exception specification of the derived function is needed,
  but an explicit *noexcept-specifier* needs the implicit exception
  specification to compare against. — *end note*\]

The exception specification of a defaulted function is evaluated as
described above only when needed; similarly, the *noexcept-specifier* of
a specialization of a function template or member function of a class
template is instantiated only when needed.

## Special functions <a id="except.special">[except.special]</a>

### General <a id="except.special.general">[except.special.general]</a>

The function `std::terminate` [except.terminate] is used by the
exception handling mechanism for coping with errors related to the
exception handling mechanism itself. The function
`std::current_exception()` [propagation] and the class
`std::nested_exception` [except.nested] can be used by a program to
capture the currently handled exception.

### The `std::terminate` function <a id="except.terminate">[except.terminate]</a>

In some situations exception handling is abandoned for less subtle error
handling techniques.

\[*Note 1*:

These situations are:

- when the exception handling mechanism, after completing the
  initialization of the exception object but before activation of a
  handler for the exception [except.throw], calls a function that exits
  via an exception, or

- when the exception handling mechanism cannot find a handler for a
  thrown exception [except.handle], or

- when the search for a handler [except.handle] encounters the outermost
  block of a function with a non-throwing exception specification
  [except.spec], or

- when the destruction of an object during stack unwinding [except.ctor]
  terminates by throwing an exception, or

- when initialization of a non-block variable with static or thread
  storage duration [basic.start.dynamic] exits via an exception, or

- when destruction of an object with static or thread storage duration
  exits via an exception [basic.start.term], or

- when execution of a function registered with `std::atexit` or
  `std::at_quick_exit` exits via an exception [support.start.term], or

- when a *throw-expression* [expr.throw] with no operand attempts to
  rethrow an exception and no exception is being handled [except.throw],
  or

- when the function `std::nested_exception::rethrow_nested` is called
  for an object that has captured no exception [except.nested], or

- when execution of the initial function of a thread exits via an
  exception [thread.thread.constr], or

- for a parallel algorithm whose `ExecutionPolicy` specifies such
  behavior [execpol.seq,execpol.par,execpol.parunseq], when execution of
  an element access function [algorithms.parallel.defns] of the parallel
  algorithm exits via an exception [algorithms.parallel.exceptions], or

- when the destructor or the move assignment operator is invoked on an
  object of type `std::thread` that refers to a joinable thread
  [thread.thread.destr,thread.thread.assign], or

- when a call to a `wait()`, `wait_until()`, or `wait_for()` function on
  a condition variable
  [thread.condition.condvar,thread.condition.condvarany] fails to meet a
  postcondition.

— *end note*\]

In such cases, the function `std::terminate` is invoked
[exception.terminate]. In the situation where no matching handler is
found, it is *implementation-defined* whether or not the stack is
unwound before `std::terminate` is invoked. In the situation where the
search for a handler [except.handle] encounters the outermost block of a
function with a non-throwing exception specification [except.spec], it
is *implementation-defined* whether the stack is unwound, unwound
partially, or not unwound at all before the function `std::terminate` is
invoked. In all other situations, the stack shall not be unwound before
the function `std::terminate` is invoked. An implementation is not
permitted to finish stack unwinding prematurely based on a determination
that the unwind process will eventually cause an invocation of the
function `std::terminate`.

### The `std::uncaught_exceptions` function <a id="except.uncaught">[except.uncaught]</a>

An exception is considered uncaught after completing the initialization
of the exception object [except.throw] until completing the activation
of a handler for the exception [except.handle].

\[*Note 2*: As a consequence, an exception is considered uncaught during
any stack unwinding resulting from it being thrown. — *end note*\]

If an exception is rethrown [expr.throw,propagation], it is considered
uncaught from the point of rethrow until the rethrown exception is
caught. The function `std::uncaught_exceptions` [uncaught.exceptions]
returns the number of uncaught exceptions in the current thread.

<!-- Link reference definitions -->
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[class.base.init]: class.md#class.base.init
[class.copy.ctor]: class.md#class.copy.ctor
[class.inhctor.init]: class.md#class.inhctor.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.general]: dcl.md#dcl.init.general
[expr.prim.lambda.capture]: expr.md#expr.prim.lambda.capture
[futures]: thread.md#futures
[propagation]: support.md#propagation
[stmt.return]: stmt.md#stmt.return
