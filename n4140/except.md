# Exception handling <a id="except">[[except]]</a>

Exception handling provides a way of transferring control and
information from a point in the execution of a thread to an exception
handler associated with a point previously passed by the execution. A
handler will be invoked only by throwing an exception in code executed
in the handler’s try block or in functions called from the handler’s try
block.

``` bnf
try-block:
    'try' compound-statement handler-seq
```

``` bnf
function-try-block:
    'try' ctor-initializercₒₚₜompound-statement handler-seq
```

``` bnf
handler-seq:
    handler handler-seq\opt
```

``` bnf
handler:
    'catch (' exception-declaration ')' compound-statement
```

``` bnf
exception-declaration:
    attribute-specifier-seqtₒₚₜype-specifier-seq declarator
    attribute-specifier-seqtₒₚₜype-specifier-seq abstract-declarator
 ₒₚₜ
    '...'
```

``` bnf
throw-expression:
    'throw'  assignment-expression\opt
```

The optional *attribute-specifier-seq* in an *exception-declaration*
appertains to the parameter of the catch clause ( [[except.handle]]).

A *try-block* is a *statement* (Clause  [[stmt.stmt]]). A
*throw-expression* is of type `void`. Within this Clause “try block” is
taken to mean both *try-block* and *function-try-block*.

A `goto` or `switch` statement shall not be used to transfer control
into a try block or into a handler.

``` cpp
void f() {
  goto l1;          // Ill-formed
  goto l2;          // Ill-formed
  try {
    goto l1;        // OK
    goto l2;        // Ill-formed
    l1: ;
  } catch (...) {
    l2: ;
    goto l1;        // Ill-formed
    goto l2;        // OK
  }
}
```

A `goto`, `break`, `return`, or `continue` statement can be used to
transfer control out of a try block or handler. When this happens, each
variable declared in the try block will be destroyed in the context that
directly contains its declaration.

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
the *condition* does not declare a variable. Any exception raised while
destroying `t2` will result in executing *handler 2*; any exception
raised while destroying `t1` will result in executing *handler 1*.

A *function-try-block* associates a *handler-seq* with the
*ctor-initializer*, if present, and the *compound-statement*. An
exception thrown during the execution of the *compound-statement* or,
for constructors and destructors, during the initialization or
destruction, respectively, of the class’s subobjects, transfers control
to a handler in a *function-try-block* in the same way as an exception
thrown during the execution of a *try-block* transfers control to other
handlers.

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
}
catch (...) {
    // handles exceptions thrown from the ctor-initializer
    // and from the constructor statements
}
```

## Throwing an exception <a id="except.throw">[[except.throw]]</a>

Throwing an exception transfers control to a handler. An exception can
be thrown from one of the following contexts: *throw-expression* (see
below), allocation functions ( [[basic.stc.dynamic.allocation]]),
`dynamic_cast` ( [[expr.dynamic.cast]]), `typeid` ( [[expr.typeid]]),
*new-expression* ( [[expr.new]]), and standard library functions (
[[structure.specifications]]). An object is passed and the type of that
object determines which handlers can catch it.

``` cpp
throw "Help!";
```

can be caught by a *handler* of `const` `char*` type:

``` cpp
try {
    // ...
}
catch(const char* p) {
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

can be caught by a handler for exceptions of type `Overflow`

``` cpp
try {
    f(1.2);
} catch(Overflow& oo) {
    // handle exceptions of type Overflow here
}
```

When an exception is thrown, control is transferred to the nearest
handler with a matching type ( [[except.handle]]); “nearest” means the
handler for which the *compound-statement* or *ctor-initializer*
following the `try` keyword was most recently entered by the thread of
control and not yet exited.

Throwing an exception copy-initializes ( [[dcl.init]], [[class.copy]]) a
temporary object, called the *exception object*. The temporary is an
lvalue and is used to initialize the variable declared in the matching
*handler* ( [[except.handle]]). If the type of the exception object
would be an incomplete type or a pointer to an incomplete type other
than (possibly cv-qualified) `void` the program is ill-formed.
Evaluating a *throw-expression* with an operand throws an exception; the
type of the exception object is determined by removing any top-level
*cv-qualifiers* from the static type of the operand and adjusting the
type from “array of `T`” or “function returning `T`” to “pointer to `T`”
or “pointer to function returning `T`,” respectively.

The memory for the exception object is allocated in an unspecified way,
except as noted in  [[basic.stc.dynamic.allocation]]. If a handler exits
by rethrowing, control is passed to another handler for the same
exception. The exception object is destroyed after either the last
remaining active handler for the exception exits by any means other than
rethrowing, or the last object of type `std::exception_ptr` (
[[propagation]]) that refers to the exception object is destroyed,
whichever is later. In the former case, the destruction occurs when the
handler exits, immediately after the destruction of the object declared
in the *exception-declaration* in the handler, if any. In the latter
case, the destruction occurs before the destructor of
`std::exception_ptr` returns. The implementation may then deallocate the
memory for the exception object; any such deallocation is done in an
unspecified way. a thrown exception does not propagate to other threads
unless caught, stored, and rethrown using appropriate library functions;
see  [[propagation]] and  [[futures]].

When the thrown object is a class object, the constructor selected for
the copy-initialization and the destructor shall be accessible, even if
the copy/move operation is elided ( [[class.copy]]).

An exception is considered caught when a handler for that exception
becomes active ( [[except.handle]]). An exception can have active
handlers and still be considered uncaught if it is rethrown.

If the exception handling mechanism, after completing the initialization
of the exception object but before the activation of a handler for the
exception, calls a function that exits via an exception,
`std::terminate` is called ( [[except.terminate]]).

``` cpp
struct C {
  C() { }
  C(const C&) {
    if (std::uncaught_exception()) {
      throw 0;      // throw during copy to handler's exception-declaration object~([except.handle])
    }
  }
};

int main() {
  try {
    throw C();      // calls std::terminate() if construction of the handler's
                    // exception-declaration object is not elided~([class.copy])
  } catch(C) { }
}
```

A *throw-expression* with no operand rethrows the currently handled
exception ( [[except.handle]]). The exception is reactivated with the
existing exception object; no new exception object is created. The
exception is no longer considered to be caught; therefore, the value of
`std::uncaught_exception()` will again be `true`. code that must be
executed because of an exception yet cannot completely handle the
exception can be written like this:

``` cpp
try {
    // ...
} catch (...) {     // catch all exceptions
  // respond (partially) to exception
  throw;            // pass the exception to some
                    // other handler
}
```

If no exception is presently being handled, executing a
*throw-expression* with no operand calls `std::terminate()` (
[[except.terminate]]).

## Constructors and destructors <a id="except.ctor">[[except.ctor]]</a>

As control passes from the point where an exception is thrown to a
handler, destructors are invoked for all automatic objects constructed
since the try block was entered. The automatic objects are destroyed in
the reverse order of the completion of their construction.

An object of any storage duration whose initialization or destruction is
terminated by an exception will have destructors executed for all of its
fully constructed subobjects (excluding the variant members of a
union-like class), that is, for subobjects for which the principal
constructor ( [[class.base.init]]) has completed execution and the
destructor has not yet begun execution. Similarly, if the non-delegating
constructor for an object has completed execution and a delegating
constructor for that object exits with an exception, the object’s
destructor will be invoked. If the object was allocated in a
*new-expression*, the matching deallocation function (
[[basic.stc.dynamic.deallocation]], [[expr.new]], [[class.free]]), if
any, is called to free the storage occupied by the object.

The process of calling destructors for automatic objects constructed on
the path from a try block to the point where an exception is thrown is
called “*stack unwinding*.” If a destructor called during stack
unwinding exits with an exception, `std::terminate` is called (
[[except.terminate]]). So destructors should generally catch exceptions
and not let them propagate out of the destructor.

## Handling an exception <a id="except.handle">[[except.handle]]</a>

The *exception-declaration* in a *handler* describes the type(s) of
exceptions that can cause that *handler* to be entered. The
*exception-declaration* shall not denote an incomplete type, an abstract
class type, or an rvalue reference type. The *exception-declaration*
shall not denote a pointer or reference to an incomplete type, other
than `void*`, `const` `void*`, `volatile` `void*`, or `const` `volatile`
`void*`.

A handler of type “array of `T`” or “function returning `T`” is adjusted
to be of type “pointer to `T`” or “pointer to function returning `T`”,
respectively.

A *handler* is a match for an exception object of type `E` if

- The *handler* is of type *cv* `T` or *cv* `T&` and `E` and `T` are the
  same type (ignoring the top-level *cv-qualifiers*), or
- the *handler* is of type *cv* `T` or *cv* `T&` and `T` is an
  unambiguous public base class of `E`, or
- the *handler* is of type *cv* `T` or `const T&` where `T` is a pointer
  type and `E` is a pointer type that can be converted to `T` by either
  or both of
  - a standard pointer conversion ( [[conv.ptr]]) not involving
    conversions to pointers to private or protected or ambiguous classes
  - a qualification conversion, or
- the *handler* is of type *cv* `T` or `const T&` where `T` is a pointer
  or pointer to member type and `E` is `std::nullptr_t`.

A *throw-expression* whose operand is an integer literal with value zero
does not match a handler of pointer or pointer to member type.

``` cpp
class Matherr { /* ... */ virtual void vf(); };
class Overflow: public Matherr { /* ... */ };
class Underflow: public Matherr { /* ... */ };
class Zerodivide: public Matherr { /* ... */ };

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

The handlers for a try block are tried in order of appearance. That
makes it possible to write handlers that can never be executed, for
example by placing a handler for a derived class after a handler for a
corresponding base class.

A `...` in a handler’s *exception-declaration* functions similarly to
`...` in a function parameter declaration; it specifies a match for any
exception. If present, a `...` handler shall be the last handler for its
try block.

If no match is found among the handlers for a try block, the search for
a matching handler continues in a dynamically surrounding try block of
the same thread.

A handler is considered active when initialization is complete for the
parameter (if any) of the catch clause. The stack will have been unwound
at that point. Also, an implicit handler is considered active when
`std::terminate()` or `std::unexpected()` is entered due to a throw. A
handler is no longer considered active when the catch clause exits or
when `std::unexpected()` exits after being entered due to a throw.

The exception with the most recently activated handler that is still
active is called the *currently handled exception*.

If no matching handler is found, the function `std::terminate()` is
called; whether or not the stack is unwound before this call to
`std::terminate()` is *implementation-defined* ( [[except.terminate]]).

Referring to any non-static member or base class of an object in the
handler for a *function-try-block* of a constructor or destructor for
that object results in undefined behavior.

The fully constructed base classes and members of an object shall be
destroyed before entering the handler of a *function-try-block* of a
constructor for that object. Similarly, if a delegating constructor for
an object exits with an exception after the non-delegating constructor
for that object has completed execution, the object’s destructor shall
be executed before entering the handler of a of a constructor for that
object. The base classes and non-variant members of an object shall be
destroyed before entering the handler of a of a destructor for that
object ( [[class.dtor]]).

The scope and lifetime of the parameters of a function or constructor
extend into the handlers of a *function-try-block*.

Exceptions thrown in destructors of objects with static storage duration
or in constructors of namespace-scope objects with static storage
duration are not caught by a *function-try-block* on `main()`.
Exceptions thrown in destructors of objects with thread storage duration
or in constructors of namespace-scope objects with thread storage
duration are not caught by a *function-try-block* on the initial
function of the thread.

If a return statement appears in a handler of the *function-try-block*
of a constructor, the program is ill-formed.

The currently handled exception is rethrown if control reaches the end
of a handler of the *function-try-block* of a constructor or destructor.
Otherwise, a function returns when control reaches the end of a handler
for the *function-try-block* ( [[stmt.return]]). Flowing off the end of
a *function-try-block* is equivalent to a `return` with no value; this
results in undefined behavior in a value-returning function (
[[stmt.return]]).

The variable declared by the *exception-declaration*, of type cv `T` or
cv `T&`, is initialized from the exception object, of type `E`, as
follows:

- if `T` is a base class of `E`, the variable is copy-initialized (
  [[dcl.init]]) from the corresponding base class subobject of the
  exception object;
- otherwise, the variable is copy-initialized ( [[dcl.init]]) from the
  exception object.

The lifetime of the variable ends when the handler exits, after the
destruction of any automatic objects initialized within the handler.

When the handler declares an object, any changes to that object will not
affect the exception object. When the handler declares a reference to an
object, any changes to the referenced object are changes to the
exception object and will have effect should that object be rethrown.

## Exception specifications <a id="except.spec">[[except.spec]]</a>

A function declaration lists exceptions that its function might directly
or indirectly throw by using an *exception-specification* as a suffix of
its declarator.

``` bnf
exception-specification:
    dynamic-exception-specification
    noexcept-specification
```

``` bnf
dynamic-exception-specification:
    'throw (' type-id-list\terminal ₒₚₜ{)}
```

``` bnf
type-id-list:
    type-id '...'\opt
    type-id-list ',' type-id '...'\opt
```

``` bnf
noexcept-specification:
    'noexcept' '(' constant-expression ')'
    'noexcept'
```

In a *noexcept-specification*, the *constant-expression*, if supplied,
shall be a constant expression ( [[expr.const]]) that is contextually
converted to `bool` (Clause  [[conv]]). A *noexcept-specification*
`noexcept` is equivalent to `noexcept(true)`. A `(` token that follows
`noexcept` is part of the *noexcept-specification* and does not commence
an initializer ( [[dcl.init]]).

An *exception-specification* shall appear only on a function declarator
for a function type, pointer to function type, reference to function
type, or pointer to member function type that is the top-level type of a
declaration or definition, or on such a type appearing as a parameter or
return type in a function declarator. An *exception-specification* shall
not appear in a typedef declaration or *alias-declaration*.

``` cpp
void f() throw(int);                    // OK
void (*fp)() throw (int);               // OK
void g(void pfa() throw(int));          // OK
typedef int (*pf)() throw(int);         // ill-formed
```

A type denoted in an *exception-specification* shall not denote an
incomplete type or an rvalue reference type. A type denoted in an
*exception-specification* shall not denote a pointer or reference to an
incomplete type, other than *cv* `void*`. A type cv `T`, “array of `T`”,
or “function returning `T`” denoted in an *exception-specification* is
adjusted to type `T`, “pointer to `T`”, or “pointer to function
returning `T`”, respectively.

Two *exception-specification*s are *compatible* if:

- both are non-throwing (see below), regardless of their form,
- both have the form `noexcept(`*constant-expression*`)` and the
  *constant-expression*s are equivalent, or
- both are *dynamic-exception-specification*s that have the same set of
  adjusted types.

If any declaration of a function has an *exception-specification* that
is not a *noexcept-specification* allowing all exceptions, all
declarations, including the definition and any explicit specialization,
of that function shall have a compatible *exception-specification*. If
any declaration of a pointer to function, reference to function, or
pointer to member function has an *exception-specification*, all
occurrences of that declaration shall have a compatible
*exception-specification* In an explicit instantiation an
*exception-specification* may be specified, but is not required. If an
*exception-specification* is specified in an explicit instantiation
directive, it shall be compatible with the *exception-specification*s of
other declarations of that function. A diagnostic is required only if
the *exception-specification*s are not compatible within a single
translation unit.

If a virtual function has an *exception-specification*, all
declarations, including the definition, of any function that overrides
that virtual function in any derived class shall only allow exceptions
that are allowed by the *exception-specification* of the base class
virtual function.

``` cpp
struct B {
  virtual void f() throw (int, double);
  virtual void g();
};

struct D: B {
  void f();                     // ill-formed
  void g() throw (int);         // OK
};
```

The declaration of `D::f` is ill-formed because it allows all
exceptions, whereas `B::f` allows only `int` and `double`. A similar
restriction applies to assignment to and initialization of pointers to
functions, pointers to member functions, and references to functions:
the target entity shall allow at least the exceptions allowed by the
source value in the assignment or initialization.

``` cpp
class A { /* ... */ };
void (*pf1)();      // no exception specification
void (*pf2)() throw(A);

void f() {
  pf1 = pf2;        // OK: pf1 is less restrictive
  pf2 = pf1;        // error: pf2 is more restrictive
}
```

In such an assignment or initialization, *exception-specification*s on
return types and parameter types shall be compatible. In other
assignments or initializations, *exception-specification*s shall be
compatible.

An *exception-specification* can include the same type more than once
and can include classes that are related by inheritance, even though
doing so is redundant. An *exception-specification* can also include the
class `std::bad_exception` ( [[bad.exception]]).

A function is said to *allow* an exception of type `E` if the
*constant-expression* in its *noexcept-specification* evaluates to
`false` or its *dynamic-exception-specification* contains a type `T` for
which a handler of type `T` would be a match ( [[except.handle]]) for an
exception of type `E`.

Whenever an exception is thrown and the search for a handler (
[[except.handle]]) encounters the outermost block of a function with an
*exception-specification* that does not allow the exception, then,

- if the *exception-specification* is a
  *dynamic-exception-specification*, the function `std::unexpected()` is
  called ( [[except.unexpected]]),
- otherwise, the function `std::terminate()` is called (
  [[except.terminate]]).

``` cpp
class X { };
class Y { };
class Z: public X { };
class W { };

void f() throw (X, Y) {
  int n = 0;
  if (n) throw X();             // OK
  if (n) throw Z();             // also OK
  throw W();                    // will call std::unexpected()
}
```

A function can have multiple declarations with different non-throwing
*exception-specification*s; for this purpose, the one on the function
definition is used.

The function `unexpected()` may throw an exception that will satisfy the
*exception-specification* for which it was invoked, and in this case the
search for another handler will continue at the call of the function
with this *exception-specification* (see  [[except.unexpected]]), or it
may call `std::terminate()`.

An implementation shall not reject an expression merely because when
executed it throws or might throw an exception that the containing
function does not allow.

``` cpp
extern void f() throw(X, Y);

void g() throw(X) {
  f();                          // OK
}
```

the call to `f` is well-formed even though when called, `f` might throw
exception `Y` that `g` does not allow.

A function with no *exception-specification* or with an
*exception-specification* of the form
`noexcept(`*constant-expression*`)` where the *constant-expression*
yields `false` allows all exceptions. An *exception-specification* is
*non-throwing* if it is of the form `throw()`, `noexcept`, or
`noexcept(`*constant-expression*`)` where the *constant-expression*
yields `true`. A function with a non-throwing *exception-specification*
does not allow any exceptions.

An *exception-specification* is not considered part of a function’s
type.

An inheriting constructor ( [[class.inhctor]]) and an implicitly
declared special member function (Clause  [[special]]) have an
*exception-specification*. If `f` is an inheriting constructor or an
implicitly declared default constructor, copy constructor, move
constructor, destructor, copy assignment operator, or move assignment
operator, its implicit *exception-specification* specifies the *type-id*
`T` if and only if `T` is allowed by the *exception-specification* of a
function directly invoked by `f`’s implicit definition; `f` allows all
exceptions if any function it directly invokes allows all exceptions,
and `f` has the *exception-specification* `noexcept(true)` if every
function it directly invokes allows no exceptions. It follows that `f`
has the *exception-specification* `noexcept(true)` if it invokes no
other functions. An instantiation of an inheriting constructor template
has an implied *exception-specification* as if it were a non-template
inheriting constructor.

``` cpp
struct A {
  A();
  A(const A&) throw();
  A(A&&) throw();
  ~A() throw(X);
};
struct B {
  B() throw();
  B(const B&) = default; // Declaration of B::B(const B&) noexcept(true)
  B(B&&) throw(Y);
  ~B() throw(Y);
};
struct D : public A, public B {
    // Implicit declaration of D::D();
    // Implicit declaration of D::D(const D&) noexcept(true);
    // Implicit declaration of D::D(D&&) throw(Y);
    // Implicit declaration of D::\~D() throw(X, Y);
};
```

Furthermore, if `A::~A()` or `B::~B()` were virtual, `D::~D()` would not
be as restrictive as that of `A::~A`, and the program would be
ill-formed since a function that overrides a virtual function from a
base class shall have an *exception-specification* at least as
restrictive as that in the base class.

A deallocation function ( [[basic.stc.dynamic.deallocation]]) with no
explicit *exception-specification* is treated as if it were specified
with `noexcept(true)`.

An *exception-specification* is considered to be *needed* when:

- in an expression, the function is the unique lookup result or the
  selected member of a set of overloaded functions ( [[basic.lookup]],
  [[over.match]], [[over.over]]);
- the function is odr-used ( [[basic.def.odr]]) or, if it appears in an
  unevaluated operand, would be odr-used if the expression were
  potentially-evaluated;
- the *exception-specification* is compared to that of another
  declaration (e.g., an explicit specialization or an overriding virtual
  function);
- the function is defined; or
- the *exception-specification* is needed for a defaulted special member
  function that calls the function. A defaulted declaration does not
  require the *exception-specification* of a base member function to be
  evaluated until the implicit *exception-specification* of the derived
  function is needed, but an explicit *exception-specification* needs
  the implicit *exception-specification* to compare against.

The *exception-specification* of a defaulted special member function is
evaluated as described above only when needed; similarly, the
*exception-specification* of a specialization of a function template or
member function of a class template is instantiated only when needed.

In a *dynamic-exception-specification*, a *type-id* followed by an
ellipsis is a pack expansion ( [[temp.variadic]]).

The use of *dynamic-exception-specification*s is deprecated (see Annex 
[[depr]]).

## Special functions <a id="except.special">[[except.special]]</a>

The functions `std::terminate()` ( [[except.terminate]]) and
`std::unexpected()` ( [[except.unexpected]]) are used by the exception
handling mechanism for coping with errors related to the exception
handling mechanism itself. The function `std::current_exception()` (
[[propagation]]) and the class `std::nested_exception` (
[[except.nested]]) can be used by a program to capture the currently
handled exception.

### The `std::terminate()` function <a id="except.terminate">[[except.terminate]]</a>

In some situations exception handling must be abandoned for less subtle
error handling techniques. These situations are:

- when the exception handling mechanism, after completing the
  initialization of the exception object but before activation of a
  handler for the exception ( [[except.throw]]), calls a function that
  exits via an exception, or
- when the exception handling mechanism cannot find a handler for a
  thrown exception ( [[except.handle]]), or
- when the search for a handler ( [[except.handle]]) encounters the
  outermost block of a function with a *noexcept-specification* that
  does not allow the exception ( [[except.spec]]), or
- when the destruction of an object during stack unwinding (
  [[except.ctor]]) terminates by throwing an exception, or
- when initialization of a non-local variable with static or thread
  storage duration ( [[basic.start.init]]) exits via an exception, or
- when destruction of an object with static or thread storage duration
  exits via an exception ( [[basic.start.term]]), or
- when execution of a function registered with `std::atexit` or
  `std::at_quick_exit` exits via an exception ( [[support.start.term]]),
  or
- when a *throw-expression* with no operand attempts to rethrow an
  exception and no exception is being handled ( [[except.throw]]), or
- when `std::unexpected` throws an exception which is not allowed by the
  previously violated *dynamic-exception-specification*, and
  `std::bad_exception` is not included in that
  *dynamic-exception-specifica{-}tion* ( [[except.unexpected]]), or
- when the implementation’s default unexpected exception handler is
  called ( [[unexpected.handler]]), or
- when the function `std::nested_exception::rethrow_nested` is called
  for an object that has captured no exception ( [[except.nested]]), or
- when execution of the initial function of a thread exits via an
  exception ( [[thread.thread.constr]]), or
- when the destructor or the copy assignment operator is invoked on an
  object of type `std::thread` that refers to a joinable thread (
  [[thread.thread.destr]],  [[thread.thread.assign]]).

In such cases, `std::terminate()` is called ( [[exception.terminate]]).
In the situation where no matching handler is found, it is
*implementation-defined* whether or not the stack is unwound before
`std::terminate()` is called. In the situation where the search for a
handler ( [[except.handle]]) encounters the outermost block of a
function with a *noexcept-specification* that does not allow the
exception ( [[except.spec]]), it is *implementation-defined* whether the
stack is unwound, unwound partially, or not unwound at all before
`std::terminate()` is called. In all other situations, the stack shall
not be unwound before `std::terminate()` is called. An implementation is
not permitted to finish stack unwinding prematurely based on a
determination that the unwind process will eventually cause a call to
`std::terminate()`.

### The `std::unexpected()` function <a id="except.unexpected">[[except.unexpected]]</a>

If a function with a *dynamic-exception-specification* throws an
exception that is not listed in the * dynamic-exception-specification*,
the function `std::unexpected()` is called ( [[exception.unexpected]])
immediately after completing the stack unwinding for the former
function.

By default, `std::unexpected()` calls `std::terminate()`, but a program
can install its own handler function ( [[set.unexpected]]). In either
case, the constraints in the following paragraph apply.

The `std::unexpected()` function shall not return, but it can throw (or
re-throw) an exception. If it throws a new exception which is allowed by
the exception specification which previously was violated, then the
search for another handler will continue at the call of the function
whose exception specification was violated. If it throws or rethrows an
exception that the * dynamic-exception-specification* does not allow
then the following happens: If the * dynamic-exception-specification*
does not include the class `std::bad_exception` ( [[bad.exception]])
then the function `std::terminate()` is called, otherwise the thrown
exception is replaced by an implementation-defined object of the type
`std::bad_exception` and the search for another handler will continue at
the call of the function whose * dynamic-exception-specification* was
violated.

Thus, a *dynamic-exception-specification* guarantees that only the
listed exceptions will be thrown. If the
* dynamic-exception-specification* includes the type
`std::bad_exception` then any exception not on the list may be replaced
by `std::bad_exception` within the function `std::unexpected()`.

### The `std::uncaught_exception()` function <a id="except.uncaught">[[except.uncaught]]</a>

The function `std::uncaught_exception()` returns `true` after completing
the initialization of the exception object ( [[except.throw]]) until
completing the activation of a handler for the exception (
[[except.handle]],  [[uncaught]]). This includes stack unwinding. If the
exception is rethrown ( [[except.throw]]), `std::uncaught_exception()`
returns `true` from the point of rethrow until the rethrown exception is
caught again.

<!-- Section link definitions -->
[except]: #except
[except.ctor]: #except.ctor
[except.handle]: #except.handle
[except.spec]: #except.spec
[except.special]: #except.special
[except.terminate]: #except.terminate
[except.throw]: #except.throw
[except.uncaught]: #except.uncaught
[except.unexpected]: #except.unexpected

<!-- Link reference definitions -->
[bad.exception]: language.md#bad.exception
[basic.def.odr]: basic.md#basic.def.odr
[basic.lookup]: basic.md#basic.lookup
[basic.start.init]: basic.md#basic.start.init
[basic.start.term]: basic.md#basic.start.term
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[class.base.init]: special.md#class.base.init
[class.copy]: special.md#class.copy
[class.dtor]: special.md#class.dtor
[class.free]: special.md#class.free
[class.inhctor]: special.md#class.inhctor
[conv]: conv.md#conv
[conv.ptr]: conv.md#conv.ptr
[dcl.init]: dcl.md#dcl.init
[depr]: #depr
[except.ctor]: #except.ctor
[except.handle]: #except.handle
[except.nested]: language.md#except.nested
[except.spec]: #except.spec
[except.terminate]: #except.terminate
[except.throw]: #except.throw
[except.unexpected]: #except.unexpected
[exception.terminate]: language.md#exception.terminate
[exception.unexpected]: future.md#exception.unexpected
[expr.const]: expr.md#expr.const
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.new]: expr.md#expr.new
[expr.typeid]: expr.md#expr.typeid
[futures]: thread.md#futures
[over.match]: over.md#over.match
[over.over]: over.md#over.over
[propagation]: language.md#propagation
[set.unexpected]: future.md#set.unexpected
[special]: special.md#special
[stmt.return]: stmt.md#stmt.return
[stmt.stmt]: stmt.md#stmt.stmt
[structure.specifications]: library.md#structure.specifications
[support.start.term]: language.md#support.start.term
[temp.variadic]: temp.md#temp.variadic
[thread.thread.assign]: thread.md#thread.thread.assign
[thread.thread.constr]: thread.md#thread.thread.constr
[thread.thread.destr]: thread.md#thread.thread.destr
[uncaught]: language.md#uncaught
[unexpected.handler]: future.md#unexpected.handler
