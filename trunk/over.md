# Overloading <a id="over">[[over]]</a>

## Preamble <a id="over.pre">[[over.pre]]</a>

[*Note 1*: Each of two or more entities with the same name in the same
scope, which must be functions or function templates, is commonly called
an “overload”. — *end note*]

When a function is designated in a call, which function declaration is
being referenced and the validity of the call are determined by
comparing the types of the arguments at the point of use with the types
of the parameters in the declarations in the overload set. This function
selection process is called *overload resolution* and is defined in 
[[over.match]].

[*Note 2*: Overload sets are formed by *id-expression*s naming
functions and function templates and by *splice-expression*s designating
entities of the same kinds. — *end note*]

[*Example 1*:

``` cpp
double abs(double);
int abs(int);

abs(1);             // calls abs(int);
abs(1.0);           // calls abs(double);
```

— *end example*]

## Overload resolution <a id="over.match">[[over.match]]</a>

### General <a id="over.match.general">[[over.match.general]]</a>

Overload resolution is a mechanism for selecting the best function to
call given a list of expressions that are to be the arguments of the
call and a set of *candidate functions* that can be called based on the
context of the call. The selection criteria for the best function are
the number of arguments, how well the arguments match the
parameter-type-list of the candidate function, how well (for non-static
member functions) the object matches the object parameter, and certain
other properties of the candidate function.

[*Note 1*: The function selected by overload resolution is not
guaranteed to be appropriate for the context. Other restrictions, such
as the accessibility of the function, can make its use in the calling
context ill-formed. — *end note*]

Overload resolution selects the function to call in seven distinct
contexts within the language:

- invocation of a function named in the function call syntax
  [[over.call.func]];
- invocation of a function call operator, a pointer-to-function
  conversion function, a reference-to-pointer-to-function conversion
  function, or a reference-to-function conversion function on a class
  object named in the function call syntax [[over.call.object]];
- invocation of the operator referenced in an expression
  [[over.match.oper]];
- invocation of a constructor for default- or direct-initialization
  [[dcl.init]] of a class object [[over.match.ctor]];
- invocation of a user-defined conversion for copy-initialization
  [[dcl.init]] of a class object [[over.match.copy]];
- invocation of a conversion function for initialization of an object of
  a non-class type from an expression of class type [[over.match.conv]];
  and
- invocation of a conversion function for conversion in which a
  reference [[dcl.init.ref]] will be directly bound [[over.match.ref]].

Each of these contexts defines the set of candidate functions and the
list of arguments in its own unique way. But, once the candidate
functions and argument lists have been identified, the selection of the
best function is the same in all cases:

- First, a subset of the candidate functions (those that have the proper
  number of arguments and meet certain other conditions) is selected to
  form a set of viable functions [[over.match.viable]].
- Then the best viable function is selected based on the implicit
  conversion sequences [[over.best.ics]] needed to match each argument
  to the corresponding parameter of each viable function.

If a best viable function exists and is unique, overload resolution
succeeds and produces it as the result. Otherwise overload resolution
fails and the invocation is ill-formed. When overload resolution
succeeds, and the best viable function is not accessible
[[class.access]] in the context in which it is used, the program is
ill-formed.

Overload resolution results in a *usable candidate* if overload
resolution succeeds and the selected candidate is either not a function
[[over.built]], or is a function that is not deleted and is accessible
from the context in which overload resolution was performed.

### Candidate functions and argument lists <a id="over.match.funcs">[[over.match.funcs]]</a>

#### General <a id="over.match.funcs.general">[[over.match.funcs.general]]</a>

The subclauses of  [[over.match.funcs]] describe the set of candidate
functions and the argument list submitted to overload resolution in each
context in which overload resolution is used. The source transformations
and constructions defined in these subclauses are only for the purpose
of describing the overload resolution process. An implementation is not
required to use such transformations and constructions.

The set of candidate functions can contain both member and non-member
functions to be resolved against the same argument list. If a member
function is

- an implicit object member function that is not a constructor, or
- a static member function and the argument list includes an implied
  object argument,

it is considered to have an extra first parameter, called the
*implicit object parameter*, which represents the object for which the
member function has been called.

Similarly, when appropriate, the context can construct an argument list
that contains an *implied object argument* as the first argument in the
list to denote the object to be operated on.

For implicit object member functions, the type of the implicit object
parameter is

- “lvalue reference to cv `X`” for functions declared without a
  *ref-qualifier* or with the `&` *ref-qualifier*
- “rvalue reference to cv `X`” for functions declared with the `&&`
  *ref-qualifier*

where `X` is the class of which the function is a direct member and cv
is the cv-qualification on the member function declaration.

[*Example 1*: For a `const` member function of class `X`, the extra
parameter is assumed to have type “lvalue reference to
`const X`”. — *end example*]

For conversion functions that are implicit object member functions, the
function is considered to be a member of the class of the implied object
argument for the purpose of defining the type of the implicit object
parameter. For non-conversion functions that are implicit object member
functions nominated by a *using-declaration* in a derived class, the
function is considered to be a member of the derived class for the
purpose of defining the type of the implicit object parameter. For
static member functions, the implicit object parameter is considered to
match any object (since if the function is selected, the object is
discarded).

[*Note 1*: No actual type is established for the implicit object
parameter of a static member function, and no attempt will be made to
determine a conversion sequence for that parameter
[[over.match.best]]. — *end note*]

During overload resolution, the implied object argument is
indistinguishable from other arguments. The implicit object parameter,
however, retains its identity since no user-defined conversions can be
applied to achieve a type match with it. For implicit object member
functions declared without a *ref-qualifier*, even if the implicit
object parameter is not const-qualified, an rvalue can be bound to the
parameter as long as in all other respects the argument can be converted
to the type of the implicit object parameter.

[*Note 2*: The fact that such an argument is an rvalue does not affect
the ranking of implicit conversion sequences
[[over.ics.rank]]. — *end note*]

Because other than in list-initialization only one user-defined
conversion is allowed in an implicit conversion sequence, special rules
apply when selecting the best user-defined conversion
[[over.match.best]], [[over.best.ics]].

[*Example 2*:

``` cpp
class T {
public:
  T();
};

class C : T {
public:
  C(int);
};
T a = 1;            // error: no viable conversion (T(C(1)) not considered)
```

— *end example*]

In each case where conversion functions of a class `S` are considered
for initializing an object or reference of type `T`, the candidate
functions include the result of a search for the
*conversion-function-id* `operator T` in `S`.

[*Note 3*: This search can find a specialization of a conversion
function template [[basic.lookup]]. — *end note*]

Each such case also defines sets of *permissible types* for explicit and
non-explicit conversion functions; each (non-template) conversion
function that

- is a non-hidden member of `S`,
- yields a permissible type, and,
- for the former set, is non-explicit

is also a candidate function. If initializing an object, for any
permissible type cv `U`, any cv-qualifiercv2 `U`, cv-qualifiercv2 `U&`,
or cv-qualifiercv2 `U&&` is also a permissible type. If the set of
permissible types for explicit conversion functions is empty, any
candidates that are explicit are discarded.

In each case where a candidate is a function template, candidate
function template specializations are generated using template argument
deduction [[temp.over]], [[temp.deduct]]. If a constructor template or
conversion function template has an *explicit-specifier* whose
*constant-expression* is value-dependent [[temp.dep]], template argument
deduction is performed first and then, if the context admits only
candidates that are not explicit and the generated specialization is
explicit [[dcl.fct.spec]], it will be removed from the candidate set.
Those candidates are then handled as candidate functions in the usual
way.[^1]

A given name can refer to, or a conversion can consider, one or more
function templates as well as a set of non-template functions. In such a
case, the candidate functions generated from each function template are
combined with the set of non-template candidate functions.

A defaulted move special member function
[[class.copy.ctor]], [[class.copy.assign]] that is defined as deleted is
excluded from the set of candidate functions in all contexts. A
constructor inherited from class type `C` [[class.inhctor.init]] that
has a first parameter of type “reference to cv-qualifiercv1 `P`”
(including such a constructor instantiated from a template) is excluded
from the set of candidate functions when constructing an object of type
cv-qualifiercv2 `D` if the argument list has exactly one argument and
`C` is reference-related to `P` and `P` is reference-related to `D`.

[*Example 3*:

``` cpp
struct A {
  A();                                  // #1
  A(A &&);                              // #2
  template<typename T> A(T &&);         // #3
};
struct B : A {
  using A::A;
  B(const B &);                         // #4
  B(B &&) = default;                    // #5, implicitly deleted

  struct X { X(X &&) = delete; } x;
};
extern B b1;
B b2 = static_cast<B&&>(b1);            // calls #4: #1 is not viable, #2, #3, and #5 are not candidates
struct C { operator B&&(); };
B b3 = C();                             // calls #4
```

— *end example*]

#### Function call syntax <a id="over.match.call">[[over.match.call]]</a>

##### General <a id="over.match.call.general">[[over.match.call.general]]</a>

In a function call [[expr.call]]

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

if the *postfix-expression* names at least one function or function
template, overload resolution is applied as specified in
[[over.call.func]]. If the *postfix-expression* denotes an object of
class type, overload resolution is applied as specified in
[[over.call.object]].

If the *postfix-expression* is the address of an overload set, overload
resolution is applied using that set as described above.

[*Note 1*: No implied object argument is added in this
case. — *end note*]

If the function selected by overload resolution is an implicit object
member function, the program is ill-formed.

[*Note 2*: The resolution of the address of an overload set in other
contexts is described in [[over.over]]. — *end note*]

##### Call to designated function <a id="over.call.func">[[over.call.func]]</a>

Of interest in  [[over.call.func]] are only those function calls in
which the *postfix-expression* ultimately contains an *id-expression* or
*splice-expression* that designates one or more functions. Such a
*postfix-expression*, perhaps nested arbitrarily deep in parentheses,
has one of the following forms:

``` bnf
postfix-expression:
    postfix-expression '.' id-expression
    postfix-expression '.' splice-expression
    postfix-expression '->' id-expression
    postfix-expression '->' splice-expression
    id-expression
    splice-expression
```

These represent two syntactic subcategories of function calls: qualified
function calls and unqualified function calls.

In qualified function calls, the function is designated by an
*id-expression* or *splice-expression* E preceded by an `->` or `.`
operator. Since the construct `A->B` is generally equivalent to
`(*A).B`, the rest of [[over]] assumes, without loss of generality, that
all member function calls have been normalized to the form that uses an
object and the `.` operator. Furthermore, [[over]] assumes that the
*postfix-expression* that is the left operand of the `.` operator has
type “cv `T`” where `T` denotes a class.[^2]

The set of candidate functions either is the set found by name lookup
[[class.member.lookup]] if E is an *id-expression* or is the set
determined as specified in  [[expr.prim.splice]] if E is a
*splice-expression*. The argument list is the *expression-list* in the
call augmented by the addition of the left operand of the `.` operator
in the normalized member function call as the implied object argument
[[over.match.funcs]].

In unqualified function calls, the function is designated by an
*id-expression* or a *splice-expression* E. The set of candidate
functions either is the set found by name lookup [[basic.lookup]] if E
is an *id-expression* or is the set determined as specified in 
[[expr.prim.splice]] if E is a *splice-expression*. The set of candidate
functions consists either entirely of non-member functions or entirely
of member functions of some class `T`. In the former case or if E is
either a *splice-expression* or the address of an overload set, the
argument list is the same as the *expression-list* in the call.
Otherwise, the argument list is the *expression-list* in the call
augmented by the addition of an implied object argument as in a
qualified function call. If the current class is, or is derived from,
`T`, and the keyword `this` [[expr.prim.this]] refers to it,

- if the unqualified function call appears in a precondition assertion
  of a constructor or a postcondition assertion of a destructor and
  overload resolution selects a non-static member function, the call is
  ill-formed;
- otherwise, the implied object argument is `(*this)`.

Otherwise,

- if overload resolution selects a non-static member function, the call
  is ill-formed;
- otherwise, a contrived object of type `T` becomes the implied object
  argument.[^3]

[*Example 1*:

``` cpp
struct C {
  bool a();
  void b() {
    a();                // OK, (*this).a()
  }

  void c(this const C&);    // #1
  void c() &;               // #2
  static void c(int = 0);   // #3

  void d() {
    c();                // error: ambiguous between #2 and #3
    (C::c)();           // error: as above
    (&(C::c))();        // error: cannot resolve address of overloaded this->C::c[over.over]
    (&C::c)(C{});       // selects #1
    (&C::c)(*this);     // error: selects #2, and is ill-formed[over.match.call.general]
    (&C::c)();          // selects #3
  }

  void f(this const C&);
  void g() const {
    f();                // OK, (*this).f()
    f(*this);           // error: no viable candidate for (*this).f(*this)
    this->f();          // OK
  }

  static void h() {
    f();                // error: contrived object argument, but overload resolution
                        // picked a non-static member function
    f(C{});             // error: no viable candidate
    C{}.f();            // OK
  }

  void k(this int);
  operator int() const;
  void m(this const C& c) {
    c.k();              // OK
  }

  C()
    pre(a())            // error: implied this in constructor precondition
    pre(this->a())      // OK
    post(a());          // OK
  ~C()
    pre(a())            // OK
    post(a())           // error: implied this in destructor postcondition
    post(this->a());    // OK
};
```

— *end example*]

##### Call to object of class type <a id="over.call.object">[[over.call.object]]</a>

If the *postfix-expression* `E` in the function call syntax evaluates to
a class object of type “cv `T`”, then the set of candidate functions
includes at least the function call operators of `T`. The function call
operators of `T` are the results of a search for the name `operator()`
in the scope of `T`.

In addition, for each non-explicit conversion function declared in `T`
of the form

``` bnf
operator conversion-type-id '( )' cv-qualifier-seqₒₚₜ ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ ';'
```

where the optional *cv-qualifier-seq* is the same cv-qualification as,
or a greater cv-qualification than, cv, and where *conversion-type-id*
denotes the type “pointer to function of (`P₁`, …, `Pₙ`) returning `R`”,
or the type “reference to pointer to function of (`P₁`, …, `Pₙ`)
returning `R`”, or the type “reference to function of (`P₁`, …, `Pₙ`)
returning `R`”, a *surrogate call function* with the unique name
*call-function* and having the form

``` bnf
'R' *call-function* '(' conversion-type-id \ %
'F, P₁ a₁, …, Pₙ aₙ)' \terminal{\ return \terminal{F (a₁, …, aₙ); \}}
```

is also considered as a candidate function. Similarly, surrogate call
functions are added to the set of candidate functions for each
non-explicit conversion function declared in a base class of `T`
provided the function is not hidden within `T` by another intervening
declaration.[^4]

The argument list submitted to overload resolution consists of the
argument expressions present in the function call syntax preceded by the
implied object argument `(E)`.

[*Note 3*: When comparing the call against the function call operators,
the implied object argument is compared against the object parameter of
the function call operator. When comparing the call against a surrogate
call function, the implied object argument is compared against the first
parameter of the surrogate call function. — *end note*]

[*Example 2*:

``` cpp
int f1(int);
int f2(float);
typedef int (*fp1)(int);
typedef int (*fp2)(float);
struct A {
  operator fp1() { return f1; }
  operator fp2() { return f2; }
} a;
int i = a(1);                   // calls f1 via pointer returned from conversion function
```

— *end example*]

#### Operators in expressions <a id="over.match.oper">[[over.match.oper]]</a>

If no operand of an operator in an expression has a type that is a class
or an enumeration, the operator is assumed to be a built-in operator and
interpreted according to [[expr.compound]].

[*Note 1*: Because `.`, `.*`, and `::` cannot be overloaded, these
operators are always built-in operators interpreted according to
[[expr.compound]]. `?:` cannot be overloaded, but the rules in this
subclause are used to determine the conversions to be applied to the
second and third operands when they have class or enumeration type
[[expr.cond]]. — *end note*]

[*Example 1*:

``` cpp
struct String {
  String (const String&);
  String (const char*);
  operator const char* ();
};
String operator + (const String&, const String&);

void f() {
  const char* p= "one" + "two"; // error: cannot add two pointers; overloaded operator+ not considered
                                // because neither operand has class or enumeration type
  int I = 1 + 1;                // always evaluates to 2 even if class or enumeration types exist
                                // that would perform the operation.
}
```

— *end example*]

If either operand has a type that is a class or an enumeration, a
user-defined operator function can be declared that implements this
operator or a user-defined conversion can be necessary to convert the
operand to a type that is appropriate for a built-in operator. In this
case, overload resolution is used to determine which operator function
or built-in operator is to be invoked to implement the operator.
Therefore, the operator notation is first transformed to the equivalent
function-call notation as summarized in [[over.match.oper]] (where `@`
denotes one of the operators covered in the specified subclause).
However, the operands are sequenced in the order prescribed for the
built-in operator [[expr.compound]].

**Table: Relationship between operator and function call notation**

| Subclause       | Expression | As member function  | As non-member function |
| --------------- | ---------- | ------------------- | ---------------------- |
| (a)}            |
| (a, b)}         |
| [[over.assign]] | `a=b`      | `(a).operator= (b)` |                        |
| [[over.sub]]    | `a[b]`     | `(a).operator[](b)` |                        |
| [[over.ref]]    | `a->`      | `(a).operator->( )` |                        |
| (a, 0)}         |


For a unary operator `@` with an operand of type cv-qualifiercv1 `T1`,
and for a binary operator `@` with a left operand of type
cv-qualifiercv1 `T1` and a right operand of type cv-qualifiercv2 `T2`,
four sets of candidate functions, designated *member candidates*,
*non-member candidates*, *built-in candidates*, and
*rewritten candidates*, are constructed as follows:

- If `T1` is a complete class type or a class currently being defined,
  the set of member candidates is the result of a search for `operator@`
  in the scope of `T1`; otherwise, the set of member candidates is
  empty.
- For the operators `=`, `[]`, or `->`, the set of non-member candidates
  is empty; otherwise, it includes the result of unqualified lookup for
  `operator@` in the rewritten function call
  [[basic.lookup.unqual]], [[basic.lookup.argdep]], ignoring all member
  functions. However, if no operand has a class type, only those
  non-member functions in the lookup set that have a first parameter of
  type `T1` or “reference to cv `T1`”, when `T1` is an enumeration type,
  or (if there is a right operand) a second parameter of type `T2` or
  “reference to cv `T2`”, when `T2` is an enumeration type, are
  candidate functions.
- For the operator `,`, the unary operator `&`, or the operator `->`,
  the built-in candidates set is empty. For all other operators, the
  built-in candidates include all of the candidate operator functions
  defined in  [[over.built]] that, compared to the given operator,
  - have the same operator name, and
  - accept the same number of operands, and
  - accept operand types to which the given operand or operands can be
    converted according to [[over.best.ics]], and
  - do not have the same parameter-type-list as any non-member candidate
    or rewritten non-member candidate that is not a function template
    specialization.
- The rewritten candidate set is determined as follows:
  - For the relational [[expr.rel]] operators, the rewritten candidates
    include all non-rewritten candidates for the expression `x <=> y`.
  - For the relational [[expr.rel]] and three-way comparison
    [[expr.spaceship]] operators, the rewritten candidates also include
    a synthesized candidate, with the order of the two parameters
    reversed, for each non-rewritten candidate for the expression
    `y <=> x`.
  - For the `!=` operator [[expr.eq]], the rewritten candidates include
    all non-rewritten candidates for the expression `x == y` that are
    rewrite targets with first operand `x` (see below).
  - For the equality operators, the rewritten candidates also include a
    synthesized candidate, with the order of the two parameters
    reversed, for each non-rewritten candidate for the expression
    `y == x` that is a rewrite target with first operand `y`.
  - For all other operators, the rewritten candidate set is empty.

  \[*Note 1*: A candidate synthesized from a member candidate has its
  object parameter as the second parameter, thus implicit conversions
  are considered for the first, but not for the second,
  parameter. — *end note*]

A non-template function or function template `F` named `operator==` is a
rewrite target with first operand `o` unless a search for the name
`operator!=` in the scope S from the instantiation context of the
operator expression finds a function or function template that would
correspond [[basic.scope.scope]] to `F` if its name were `operator==`,
where S is the scope of the class type of `o` if `F` is a class member,
and the namespace scope of which `F` is a member otherwise. A function
template specialization named `operator==` is a rewrite target if its
function template is a rewrite target.

[*Example 2*:

``` cpp
struct A {};
template<typename T> bool operator==(A, T);     // #1
bool a1 = 0 == A();                             // OK, calls reversed #1
template<typename T> bool operator!=(A, T);
bool a2 = 0 == A();                             // error, #1 is not a rewrite target

struct B {
  bool operator==(const B&);    // #2
};
struct C : B {
  C();
  C(B);
  bool operator!=(const B&);    // #3
};
bool c1 = B() == C();           // OK, calls #2; reversed #2 is not a candidate
                                // because search for operator!= in C finds #3
bool c2 = C() == B();           // error: ambiguous between #2 found when searching C and
                                // reversed #2 found when searching B

struct D {};
template<typename T> bool operator==(D, T);     // #4
inline namespace N {
  template<typename T> bool operator!=(D, T);   // #5
}
bool d1 = 0 == D();             // OK, calls reversed #4; #5 does not forbid #4 as a rewrite target
```

— *end example*]

For the first parameter of the built-in assignment operators, only
standard conversion sequences [[over.ics.scs]] are considered.

For all other operators, no such restrictions apply.

The set of candidate functions for overload resolution for some operator
`@` is the union of the member candidates, the non-member candidates,
the built-in candidates, and the rewritten candidates for that operator
`@`.

The argument list contains all of the operands of the operator. The best
function from the set of candidate functions is selected according to 
[[over.match.viable]] and  [[over.match.best]].[^5]

[*Example 3*:

``` cpp
struct A {
  operator int();
};
A operator+(const A&, const A&);
void m() {
  A a, b;
  a + b;                        // operator+(a, b) chosen over int(a) + int(b)
}
```

— *end example*]

If a rewritten `operator<=>` candidate is selected by overload
resolution for an operator `@`, `x @ y` is interpreted as
`0 @ (y <=> x)` if the selected candidate is a synthesized candidate
with reversed order of parameters, or `(x <=> y) @ 0` otherwise, using
the selected rewritten `operator<=>` candidate. Rewritten candidates for
the operator `@` are not considered in the context of the resulting
expression.

If a rewritten `operator==` candidate is selected by overload resolution
for an operator `@`, its return type shall be cv `bool`, and `x @ y` is
interpreted as:

- if `@` is `!=` and the selected candidate is a synthesized candidate
  with reversed order of parameters, `!(y == x)`,
- otherwise, if `@` is `!=`, `!(x == y)`,
- otherwise (when `@` is `==`), `y == x`,

in each case using the selected rewritten `operator==` candidate.

If a built-in candidate is selected by overload resolution, the operands
of class type are converted to the types of the corresponding parameters
of the selected operation function, except that the second standard
conversion sequence of a user-defined conversion sequence
[[over.ics.user]] is not applied. Then the operator is treated as the
corresponding built-in operator and interpreted according to
[[expr.compound]].

[*Example 4*:

``` cpp
struct X {
  operator double();
};

struct Y {
  operator int*();
};

int *a = Y() + 100.0;           // error: pointer arithmetic requires integral operand
int *b = Y() + X();             // error: pointer arithmetic requires integral operand
```

— *end example*]

The second operand of operator `->` is ignored in selecting an
`operator->` function, and is not an argument when the `operator->`
function is called. When `operator->` returns, the operator `->` is
applied to the value returned, with the original second operand.[^6]

If the operator is the operator `,`, the unary operator `&`, or the
operator `->`, and there are no viable functions, then the operator is
assumed to be the built-in operator and interpreted according to
[[expr.compound]].

[*Note 2*:

The lookup rules for operators in expressions are different than the
lookup rules for operator function names in a function call, as shown in
the following example:

``` cpp
struct A { };
void operator + (A, A);

struct B {
  void operator + (B);
  void f ();
};

A a;

void B::f() {
  operator+ (a,a);              // error: global operator hidden by member
  a + a;                        // OK, calls global operator+
}
```

— *end note*]

#### Initialization by constructor <a id="over.match.ctor">[[over.match.ctor]]</a>

When objects of class type are direct-initialized [[dcl.init]],
copy-initialized from an expression of the same or a derived class type
[[dcl.init]], or default-initialized [[dcl.init]], overload resolution
selects the constructor. For direct-initialization or
default-initialization (including default-initialization in the context
of copy-list-initialization), the candidate functions are all the
constructors of the class of the object being initialized. Otherwise,
the candidate functions are all the non-explicit constructors
[[class.conv.ctor]] of that class. The argument list is the
*expression-list* or *assignment-expression* of the *initializer*. For
default-initialization in the context of copy-list-initialization, if an
explicit constructor is chosen, the initialization is ill-formed.

#### Copy-initialization of class by user-defined conversion <a id="over.match.copy">[[over.match.copy]]</a>

Under the conditions specified in  [[dcl.init]], as part of a
copy-initialization of an object of class type, a user-defined
conversion can be invoked to convert an initializer expression to the
type of the object being initialized. Overload resolution is used to
select the user-defined conversion to be invoked.

[*Note 1*: The conversion performed for indirect binding to a reference
to a possibly cv-qualified class type is determined in terms of a
corresponding non-reference copy-initialization. — *end note*]

Assuming that “cv-qualifiercv1 `T`” is the type of the object being
initialized, with `T` a class type, the candidate functions are selected
as follows:

- The non-explicit constructors [[class.conv.ctor]] of `T` are candidate
  functions.
- When the type of the initializer expression is a class type “cv `S`”,
  conversion functions are considered. The permissible types for
  non-explicit conversion functions are `T` and any class derived from
  `T`. When initializing a temporary object [[class.mem]] to be bound to
  the first parameter of a constructor where the parameter is of type
  “reference to cv-qualifiercv2 `T`” and the constructor is called with
  a single argument in the context of direct-initialization of an object
  of type “cv-qualifiercv3 `T`”, the permissible types for explicit
  conversion functions are the same; otherwise there are none.

In both cases, the argument list has one argument, which is the
initializer expression.

[*Note 2*: This argument will be compared against the first parameter
of the constructors and against the object parameter of the conversion
functions. — *end note*]

#### Initialization by conversion function <a id="over.match.conv">[[over.match.conv]]</a>

Under the conditions specified in  [[dcl.init]], as part of an
initialization of an object of non-class type, a conversion function can
be invoked to convert an initializer expression of class type to the
type of the object being initialized. Overload resolution is used to
select the conversion function to be invoked. Assuming that “cv `T`” is
the type of the object being initialized, the candidate functions are
selected as follows:

- The permissible types for non-explicit conversion functions are those
  that can be converted to type `T` via a standard conversion sequence
  [[over.ics.scs]]. For direct-initialization, the permissible types for
  explicit conversion functions are those that can be converted to type
  `T` with a (possibly trivial) qualification conversion [[conv.qual]];
  otherwise there are none.

The argument list has one argument, which is the initializer expression.

[*Note 1*: This argument will be compared against the object parameter
of the conversion functions. — *end note*]

#### Initialization by conversion function for direct reference binding <a id="over.match.ref">[[over.match.ref]]</a>

Under the conditions specified in  [[dcl.init.ref]], a reference can be
bound directly to the result of applying a conversion function to an
initializer expression. Overload resolution is used to select the
conversion function to be invoked. Assuming that “reference to
cv-qualifiercv1 `T`” is the type of the reference being initialized, the
candidate functions are selected as follows:

- Let R be a set of types including
  - “lvalue reference to cv-qualifiercv2 `T2`” (when converting to an
    lvalue) and
  - “cv-qualifiercv2 `T2`” and “rvalue reference to cv-qualifiercv2
    `T2`” (when converting to an rvalue or an lvalue of function type)

  for any `T2`. The permissible types for non-explicit conversion
  functions are the members of R where “cv-qualifiercv1 `T`” is
  reference-compatible [[dcl.init.ref]] with “cv-qualifiercv2 `T2`”. For
  direct-initialization, the permissible types for explicit conversion
  functions are the members of R where `T2` can be converted to type `T`
  with a (possibly trivial) qualification conversion [[conv.qual]];
  otherwise there are none.

The argument list has one argument, which is the initializer expression.

[*Note 1*: This argument will be compared against the object parameter
of the conversion functions. — *end note*]

#### Initialization by list-initialization <a id="over.match.list">[[over.match.list]]</a>

When objects of non-aggregate class type `T` are list-initialized such
that [[dcl.init.list]] specifies that overload resolution is performed
according to the rules in this subclause or when forming a
list-initialization sequence according to [[over.ics.list]], overload
resolution selects the constructor in two phases:

- If the initializer list is not empty or `T` has no default
  constructor, overload resolution is first performed where the
  candidate functions are the initializer-list constructors
  [[dcl.init.list]] of the class `T` and the argument list consists of
  the initializer list as a single argument.
- Otherwise, or if no viable initializer-list constructor is found,
  overload resolution is performed again, where the candidate functions
  are all the constructors of the class `T` and the argument list
  consists of the elements of the initializer list.

In copy-list-initialization, if an explicit constructor is chosen, the
initialization is ill-formed.

[*Note 1*: This differs from other situations
[[over.match.ctor]], [[over.match.copy]], where only non-explicit
constructors are considered for copy-initialization. This restriction
only applies if this initialization is part of the final result of
overload resolution. — *end note*]

#### Class template argument deduction <a id="over.match.class.deduct">[[over.match.class.deduct]]</a>

When resolving a placeholder for a deduced class type
[[dcl.type.class.deduct]] where the *template-name* or
*splice-type-specifier* designates a primary class template `C`, a set
of functions and function templates, called the guides of `C`, is formed
comprising:

- If `C` is defined, for each constructor of `C`, a function template
  with the following properties:
  - The template parameters are the template parameters of `C` followed
    by the template parameters (including default template arguments) of
    the constructor, if any.
  - The associated constraints [[temp.constr.decl]] are the conjunction
    of the associated constraints of `C` and the associated constraints
    of the constructor, if any. \[*Note 2*: A *constraint-expression* in
    the *template-head* of `C` is checked for satisfaction before any
    constraints from the *template-head* or trailing *requires-clause*
    of the constructor. — *end note*]
  - The *parameter-declaration-clause* is that of the constructor.
  - The return type is the class template specialization designated by
    `C` and template arguments corresponding to the template parameters
    of `C`.
- If `C` is not defined or does not declare any constructors, an
  additional function template derived as above from a hypothetical
  constructor `C()`.
- An additional function template derived as above from a hypothetical
  constructor `C(C)`, called the *copy deduction candidate*.
- For each *deduction-guide*, a function or function template with the
  following properties:
  - The *template-head*, if any, and *parameter-declaration-clause* are
    those of the *deduction-guide*.
  - The return type is the *simple-template-id* of the
    *deduction-guide*.

In addition, if `C` is defined and its definition satisfies the
conditions for an aggregate class [[dcl.init.aggr]] with the assumption
that any dependent base class has no virtual functions and no virtual
base classes, and the initializer is a non-empty *braced-init-list* or
parenthesized *expression-list*, and there are no *deduction-guide*s for
`C`, the set contains an additional function template, called the
*aggregate deduction candidate*, defined as follows. Let x₁, …, xₙ be
the elements of the *initializer-list* or *designated-initializer-list*
of the *braced-init-list*, or of the *expression-list*. For each xᵢ, let
eᵢ be the corresponding aggregate element of `C` or of one of its
(possibly recursive) subaggregates that would be initialized by xᵢ
[[dcl.init.aggr]] if

- brace elision is not considered for any aggregate element that has
  - a dependent non-array type,
  - an array type with a value-dependent bound, or
  - an array type with a dependent array element type and xᵢ is a string
    literal; and
- each non-trailing aggregate element that is a pack expansion is
  assumed to correspond to no elements of the initializer list, and
- a trailing aggregate element that is a pack expansion is assumed to
  correspond to all remaining elements of the initializer list (if any).

If there is no such aggregate element eᵢ for any xᵢ, the aggregate
deduction candidate is not added to the set. The aggregate deduction
candidate is derived as above from a hypothetical constructor
`C`(`T₁`, …, `Tₙ`), where

- if eᵢ is of array type and xᵢ is a *braced-init-list*, `Tᵢ` is an
  rvalue reference to the declared type of eᵢ, and
- if eᵢ is of array type and xᵢ is a *string-literal*, `Tᵢ` is an lvalue
  reference to the const-qualified declared type of eᵢ, and
- otherwise, `Tᵢ` is the declared type of eᵢ,

except that additional parameter packs of the form `Pⱼ` `...` are
inserted into the parameter list in their original aggregate element
position corresponding to each non-trailing aggregate element of type
`Pⱼ` that was skipped because it was a parameter pack, and the trailing
sequence of parameters corresponding to a trailing aggregate element
that is a pack expansion (if any) is replaced by a single parameter of
the form `Tₙ` `...`. In addition, if `C` is defined and inherits
constructors [[namespace.udecl]] from a direct base class denoted in the
*base-specifier-list* by a *class-or-decltype* `B`, let `A` be an alias
template whose template parameter list is that of `C` and whose
*defining-type-id* is `B`. If `A` is a deducible template
[[dcl.type.simple]], the set contains the guides of `A` with the return
type `R` of each guide replaced with `typename CC<R>::type` given a
class template

``` cpp
template <typename> class CC;
```

whose primary template is not defined and with a single partial
specialization whose template parameter list is that of `A` and whose
template argument list is a specialization of `A` with the template
argument list of `A` [[temp.dep.type]] having a member typedef `type`
designating a template specialization with the template argument list of
`A` but with `C` as the template.

[*Note 1*: Equivalently, the template parameter list of the
specialization is that of `C`, the template argument list of the
specialization is `B`, and the member typedef names `C` with the
template argument list of `C`. — *end note*]

[*Example 1*:

``` cpp
template <typename T> struct B {
  B(T);
};
template <typename T> struct C : public B<T> {
  using B<T>::B;
};
template <typename T> struct D : public B<T> {};

C c(42);            // OK, deduces C<int>
D d(42);            // error: deduction failed, no inherited deduction guides
B(int) -> B<char>;
C c2(42);           // OK, deduces C<char>

template <typename T> struct E : public B<int> {
  using B<int>::B;
};

E e(42);            // error: deduction failed, arguments of E cannot be deduced from introduced guides

template <typename T, typename U, typename V> struct F {
  F(T, U, V);
};
template <typename T, typename U> struct G : F<U, T, int> {
  using G::F::F;
}

G g(true, 'a', 1);  // OK, deduces G<char, bool>

template<class T, std::size_t N>
struct H {
  T array[N];
};
template<class T, std::size_t N>
struct I {
  volatile T array[N];
};
template<std::size_t N>
struct J {
  unsigned char array[N];
};

H h = { "abc" };    // OK, deduces H<char, 4> (not T = const char)
I i = { "def" };    // OK, deduces I<char, 4>
J j = { "ghi" };    // error: cannot bind reference to array of unsigned char to array of char in deduction
```

— *end example*]

When resolving a placeholder for a deduced class type
[[dcl.type.simple]] where the *template-name* or *splice-type-specifier*
designates an alias template `A`, the *defining-type-id* of `A` must be
of the form

``` bnf
typenameₒₚₜ nested-name-specifierₒₚₜ templateₒₚₜ simple-template-id
```

as specified in [[dcl.type.simple]]. The guides of `A` are the set of
functions or function templates formed as follows. For each function or
function template `f` in the guides of the template named by the
*simple-template-id* of the *defining-type-id*, the template arguments
of the return type of `f` are deduced from the *defining-type-id* of `A`
according to the process in [[temp.deduct.type]] with the exception that
deduction does not fail if not all template arguments are deduced. If
deduction fails for another reason, proceed with an empty set of deduced
template arguments. Let `g` denote the result of substituting these
deductions into `f`. If substitution succeeds, form a function or
function template `f'` with the following properties and add it to the
set of guides of `A`:

- The function type of `f'` is the function type of `g`.
- If `f` is a function template, `f'` is a function template whose
  template parameter list consists of all the template parameters of `A`
  (including their default template arguments) that appear in the above
  deductions or (recursively) in their default template arguments,
  followed by the template parameters of `f` that were not deduced
  (including their default template arguments), otherwise `f'` is not a
  function template.
- The associated constraints [[temp.constr.decl]] are the conjunction of
  the associated constraints of `g` and a constraint that is satisfied
  if and only if the arguments of `A` are deducible (see below) from the
  return type.
- If `f` is a copy deduction candidate, then `f'` is considered to be so
  as well.
- If `f` was generated from a *deduction-guide* [[temp.deduct.guide]],
  then `f'` is considered to be so as well.
- The *explicit-specifier* of `f'` is the *explicit-specifier* of `g`
  (if any).

The arguments of a template `A` are said to be deducible from a type `T`
if, given a class template

``` cpp
template <typename> class AA;
```

with a single partial specialization whose template parameter list is
that of `A` and whose template argument list is a specialization of `A`
with the template argument list of `A` [[temp.dep.type]], `AA<T>`
matches the partial specialization.

Initialization and overload resolution are performed as described in
[[dcl.init]] and [[over.match.ctor]], [[over.match.copy]], or
[[over.match.list]] (as appropriate for the type of initialization
performed) for an object of a hypothetical class type, where the guides
of the template named by the placeholder are considered to be the
constructors of that class type for the purpose of forming an overload
set, and the initializer is provided by the context in which class
template argument deduction was performed. The following exceptions
apply:

- The first phase in [[over.match.list]] (considering initializer-list
  constructors) is omitted if the initializer list consists of a single
  expression of type cv `U`, where `U` is, or is derived from, a
  specialization of the class template directly or indirectly named by
  the placeholder.
- During template argument deduction for the aggregate deduction
  candidate, the number of elements in a trailing parameter pack is only
  deduced from the number of remaining function arguments if it is not
  otherwise deduced.

If the function or function template was generated from a constructor or
*deduction-guide* that had an *explicit-specifier*, each such notional
constructor is considered to have that same *explicit-specifier*. All
such notional constructors are considered to be public members of the
hypothetical class type.

[*Example 2*:

``` cpp
template <class T> struct A {
  explicit A(const T&, ...) noexcept;               // #1
  A(T&&, ...);                                      // #2
};

int i;
A a1 = { i, i };    // error: explicit constructor #1 selected in copy-list-initialization during deduction,
                    // cannot deduce from non-forwarding rvalue reference in #2

A a2{i, i};         // OK, #1 deduces to A<int> and also initializes
A a3{0, i};         // OK, #2 deduces to A<int> and also initializes
A a4 = {0, i};      // OK, #2 deduces to A<int> and also initializes

template <class T> A(const T&, const T&) -> A<T&>;  // #3
template <class T> explicit A(T&&, T&&) -> A<T>;    // #4

A a5 = {0, 1};      // error: explicit deduction guide #4 selected in copy-list-initialization during deduction
A a6{0,1};          // OK, #4 deduces to A<int> and #2 initializes
A a7 = {0, i};      // error: #3 deduces to A<int&>, #1 and #2 declare same constructor
A a8{0,i};          // error: #3 deduces to A<int&>, #1 and #2 declare same constructor

template <class T> struct B {
  template <class U> using TA = T;
  template <class U> B(U, TA<U>);
};

B b{(int*)0, (char*)0};         // OK, deduces B<char*>

template <typename T>
struct S {
  T x;
  T y;
};

template <typename T>
struct C {
  S<T> s;
  T t;
};

template <typename T>
struct D {
  S<int> s;
  T t;
};

C c1 = {1, 2};                  // error: deduction failed
C c2 = {1, 2, 3};               // error: deduction failed
C c3 = {{1u, 2u}, 3};           // OK, deduces C<int>

D d1 = {1, 2};                  // error: deduction failed
D d2 = {1, 2, 3};               // OK, braces elided, deduces D<int>

template <typename T>
struct E {
  T t;
  decltype(t) t2;
};

E e1 = {1, 2};                  // OK, deduces E<int>

template <typename... T>
struct Types {};

template <typename... T>
struct F : Types<T...>, T... {};

struct X {};
struct Y {};
struct Z {};
struct W { operator Y(); };

F f1 = {Types<X, Y, Z>{}, {}, {}};      // OK, F<X, Y, Z> deduced
F f2 = {Types<X, Y, Z>{}, X{}, Y{}};    // OK, F<X, Y, Z> deduced
F f3 = {Types<X, Y, Z>{}, X{}, W{}};    // error: conflicting types deduced; operator Y not considered
```

— *end example*]

[*Example 3*:

``` cpp
template <class T, class U> struct C {
  C(T, U);                                      // #1
};
template<class T, class U>
  C(T, U) -> C<T, std::type_identity_t<U>>;     // #2

template<class V> using A = C<V *, V *>;
template<std::integral W> using B = A<W>;

int i{};
double d{};
A a1(&i, &i);   // deduces A<int>
A a2(i, i);     // error: cannot deduce V * from i
A a3(&i, &d);   // error: #1: cannot deduce (V*, V*) from (int *, double *)
                // #2: cannot deduce A<V> from C<int *, double *>
B b1(&i, &i);   // deduces B<int>
B b2(&d, &d);   // error: cannot deduce B<W> from C<double *, double *>
```

Possible exposition-only implementation of the above procedure:

``` cpp
// The following concept ensures a specialization of A is deduced.
template <class> class AA;
template <class V> class AA<A<V>> { };
template <class T> concept deduces_A = requires { sizeof(AA<T>); };

// f1 is formed from the constructor #1 of C, generating the following function template
template<class T, class U>
  auto f1(T, U) -> C<T, U>;

// Deducing arguments for C<T, U> from C<V *, V*> deduces T as V * and U as V *;
// f1' is obtained by transforming f1 as described by the above procedure.
template<class V> requires deduces_A<C<V *, V *>>
  auto f1_prime(V *, V*) -> C<V *, V *>;

// f2 is formed from the deduction-guide #2 of C
template<class T, class U> auto f2(T, U) -> C<T, std::type_identity_t<U>>;

// Deducing arguments for C<T, std::type_identity_t<U>> from C<V *, V*> deduces T as V *;
// f2' is obtained by transforming f2 as described by the above procedure.
template<class V, class U>
  requires deduces_A<C<V *, std::type_identity_t<U>>>
  auto f2_prime(V *, U) -> C<V *, std::type_identity_t<U>>;

// The following concept ensures a specialization of B is deduced.
template <class> class BB;
template <class V> class BB<B<V>> { };
template <class T> concept deduces_B = requires { sizeof(BB<T>); };

// The guides for B derived from the above f1' and f2' for A are as follows:
template<std::integral W>
  requires deduces_A<C<W *, W *>> && deduces_B<C<W *, W *>>
  auto f1_prime_for_B(W *, W *) -> C<W *, W *>;

template<std::integral W, class U>
  requires deduces_A<C<W *, std::type_identity_t<U>>> &&
    deduces_B<C<W *, std::type_identity_t<U>>>
  auto f2_prime_for_B(W *, U) -> C<W *, std::type_identity_t<U>>;
```

— *end example*]

### Viable functions <a id="over.match.viable">[[over.match.viable]]</a>

From the set of candidate functions constructed for a given context
[[over.match.funcs]], a set of viable functions is chosen, from which
the best function will be selected by comparing argument conversion
sequences and associated constraints [[temp.constr.decl]] for the best
fit [[over.match.best]]. The selection of viable functions considers
associated constraints, if any, and relationships between arguments and
function parameters other than the ranking of conversion sequences.

First, to be a viable function, a candidate function shall have enough
parameters to agree in number with the arguments in the list.

- If there are m arguments in the list, all candidate functions having
  exactly m parameters are viable.
- A candidate function having fewer than m parameters is viable only if
  it has an ellipsis in its parameter list [[dcl.fct]]. For the purposes
  of overload resolution, any argument for which there is no
  corresponding parameter is considered to “match the ellipsis”
  [[over.ics.ellipsis]].
- A candidate function `C` having more than m parameters is viable only
  if the set of scopes G, as defined below, is not empty. G consists of
  every scope X that satisfies all of the following:
  - There is a declaration of `C`, whose host scope is X, considered by
    the overload resolution.
  - For every $k^\textrm{th}$ parameter P where k \> m, there is a
    reachable declaration, whose host scope is X, that specifies a
    default argument [[dcl.fct.default]] for P.

  If `C` is selected as the best viable function [[over.match.best]]:
  - G shall contain exactly one scope (call it S).
  - If the candidates are denoted by a *splice-expression*, then S shall
    not be a block scope.
  - The default arguments used in the call to `C` are the default
    arguments specified by the reachable declarations whose host scope
    is S.

  For the purposes of overload resolution, the parameter list is
  truncated on the right, so that there are exactly m parameters.

[*Example 1*:

``` cpp
namespace A {
  extern "C" void f(int, int = 5);
  extern "C" void f(int = 6, int);
}
namespace B {
  extern "C" void f(int, int = 7);
}

void use() {
  [:^^A::f:](3, 4);     // OK, default argument was not used for viability
  [:^^A::f:](3);        // error: default argument provided by declarations from two scopes
  [:^^A::f:]();         // OK, default arguments provided by declarations in the scope of A

  using A::f;
  using B::f;
  f(3, 4);              // OK, default argument was not used for viability
  f(3);                 // error: default argument provided by declaration from two scopes
  f();                  // OK, default arguments provided by declarations in the scope of A

  void g(int = 8);
  g();                  // OK
  [:^^g:]();            // error: host scope is block scope
}

void h(int = 7);
constexpr std::meta::info r = ^^h;
void poison() {
  void h(int = 8);
  h();                  // OK, calls h(8)
  [:^^h:]();            // error: default argument provided by declarations from two scopes
}
void call_h() {
  [:^^h:]();            // error: default argument provided by declarations from two scopes
  [:r:]();              // error: default argument provided by declarations from two scopes
}

template<typename... Ts>
int k(int = 3, Ts...);
int i = k<int>();       // error: no default argument for the second parameter
int j = k<>();          // OK
```

— *end example*]

Second, for a function to be viable, if it has associated constraints
[[temp.constr.decl]], those constraints shall be satisfied
[[temp.constr.constr]].

Third, for `F` to be a viable function, there shall exist for each
argument an implicit conversion sequence [[over.best.ics]] that converts
that argument to the corresponding parameter of `F`. If the parameter
has reference type, the implicit conversion sequence includes the
operation of binding the reference, and the fact that an lvalue
reference to non-`const` cannot bind to an rvalue and that an rvalue
reference cannot bind to an lvalue can affect the viability of the
function (see  [[over.ics.ref]]).

### Best viable function <a id="over.match.best">[[over.match.best]]</a>

#### General <a id="over.match.best.general">[[over.match.best.general]]</a>

Define \text{ICS}^i(`F`) as the implicit conversion sequence that
converts the iᵗʰ argument in the list to the type of the iᵗʰ parameter
of viable function `F`. [[over.best.ics]] defines the implicit
conversion sequences and [[over.ics.rank]] defines what it means for one
implicit conversion sequence to be a better conversion sequence or worse
conversion sequence than another.

Given these definitions, a viable function `F₁` is defined to be a
*better* function than another viable function `F₂` if for all arguments
i, \text{ICS}^i(`F₁`) is not a worse conversion sequence than
\text{ICS}^i(`F₂`), and then

- for some argument j, \text{ICS}^j(`F₁`) is a better conversion
  sequence than \text{ICS}^j(`F₂`), or, if not that,
- the context is an initialization by user-defined conversion (see 
  [[dcl.init]], [[over.match.conv]], and  [[over.match.ref]]) and the
  standard conversion sequence from the result of `F₁` to the
  destination type (i.e., the type of the entity being initialized) is a
  better conversion sequence than the standard conversion sequence from
  the result of `F₂` to the destination type
  \[*Example 1*:
  ``` cpp
  struct A {
    A();
    operator int();
    operator double();
  } a;
  int i = a;          // a.operator int() followed by no conversion is better than
                      // a.operator double() followed by a conversion to int
  float x = a;        // ambiguous: both possibilities require conversions,
                      // and neither is better than the other
  ```

  — *end example*]
  or, if not that,
- the context is an initialization by conversion function for direct
  reference binding [[over.match.ref]] of a reference to function type,
  the return type of `F₁` is the same kind of reference (lvalue or
  rvalue) as the reference being initialized, and the return type of
  `F₂` is not
  \[*Example 2*:
  ``` cpp
  template <class T> struct A {
    operator T&();    // #1
    operator T&&();   // #2
  };
  typedef int Fn();
  A<Fn> a;
  Fn& lf = a;         // calls #1
  Fn&& rf = a;        // calls #2
  ```

  — *end example*]
  or, if not that,
- `F₁` is not a function template specialization and `F₂` is a function
  template specialization, or, if not that,
- `F₁` and `F₂` are function template specializations, and the function
  template for `F₁` is more specialized than the template for `F₂`
  according to the partial ordering rules described in 
  [[temp.func.order]], or, if not that,
- `F₁` and `F₂` are non-template functions and `F₁` is more
  partial-ordering-constrained than `F₂` [[temp.constr.order]]
  \[*Example 3*:
  ``` cpp
  template <typename T = int>
  struct S {
    constexpr void f();                       // #1
    constexpr void f(this S&) requires true;  // #2
  };

  void test() {
    S<> s;
    s.f();                // calls #2
  }
  ```

  — *end example*]
  or, if not that,
- `F₁` is a constructor for a class `D`, `F₂` is a constructor for a
  base class `B` of `D`, and for all arguments the corresponding
  parameters of `F₁` and `F₂` have the same type
  \[*Example 4*:
  ``` cpp
  struct A {
    A(int = 0);
  };

  struct B: A {
    using A::A;
    B();
  };

  int main() {
    B b;              // OK, B::B()
  }
  ```

  — *end example*]
  or, if not that,
- `F₂` is a rewritten candidate [[over.match.oper]] and `F₁` is not
  \[*Example 5*:
  ``` cpp
  struct S {
    friend auto operator<=>(const S&, const S&) = default;        // #1
    friend bool operator<(const S&, const S&);                    // #2
  };
  bool b = S() < S();                                             // calls #2
  ```

  — *end example*]
  or, if not that,
- `F₁` and `F₂` are rewritten candidates, and `F₂` is a synthesized
  candidate with reversed order of parameters and `F₁` is not
  \[*Example 6*:
  ``` cpp
  struct S {
    friend std::weak_ordering operator<=>(const S&, int);         // #1
    friend std::weak_ordering operator<=>(int, const S&);         // #2
  };
  bool b = 1 < S();                                               // calls #2
  ```

  — *end example*]
  or, if not that,
- `F₁` and `F₂` are generated from class template argument deduction
  [[over.match.class.deduct]] for a class `D`, and `F₂` is generated
  from inheriting constructors from a base class of `D` while `F₁` is
  not, and for each explicit function argument, the corresponding
  parameters of `F₁` and `F₂` are either both ellipses or have the same
  type, or, if not that,
- `F₁` is generated from a *deduction-guide* [[over.match.class.deduct]]
  and `F₂` is not, or, if not that,
- `F₁` is the copy deduction candidate [[over.match.class.deduct]] and
  `F₂` is not, or, if not that,
- `F₁` is generated from a non-template constructor and `F₂` is
  generated from a constructor template.
  \[*Example 7*:
  ``` cpp
  template <class T> struct A {
    using value_type = T;
    A(value_type);    // #1
    A(const A&);      // #2
    A(T, T, int);     // #3
    template<class U>
      A(int, T, U);   // #4
    // #5 is the copy deduction candidate, A(A)
  };

  A x(1, 2, 3);       // uses #3, generated from a non-template constructor

  template <class T>
  A(T) -> A<T>;       // #6, less specialized than #5

  A a(42);            // uses #6 to deduce A<int> and #1 to initialize
  A b = a;            // uses #5 to deduce A<int> and #2 to initialize

  template <class T>
  A(A<T>) -> A<A<T>>; // #7, as specialized as #5

  A b2 = a;           // uses #7 to deduce A<A<int>> and #1 to initialize
  ```

  — *end example*]

If there is exactly one viable function that is a better function than
all other viable functions, then it is the one selected by overload
resolution; otherwise the call is ill-formed.[^7]

[*Example 1*:

``` cpp
void Fcn(const int*,  short);
void Fcn(int*, int);

int i;
short s = 0;

void f() {
  Fcn(&i, s);       // is ambiguous because &i → int* is better than &i → const int*
                    // but s → short is also better than s → int

  Fcn(&i, 1L);      // calls Fcn(int*, int), because &i → int* is better than &i → const int*
                    // and 1L → short and 1L → int are indistinguishable

  Fcn(&i, 'c');     // calls Fcn(int*, int), because &i → int* is better than &i → const int*
                    // and 'c' → int is better than 'c' → short
}
```

— *end example*]

[*Note 1*: If the best viable function was made viable by one or more
default arguments, additional requirements apply
[[over.match.viable]]. — *end note*]

#### Implicit conversion sequences <a id="over.best.ics">[[over.best.ics]]</a>

##### General <a id="over.best.ics.general">[[over.best.ics.general]]</a>

An *implicit conversion sequence* is a sequence of conversions used to
convert an argument in a function call to the type of the corresponding
parameter of the function being called. The sequence of conversions is
an implicit conversion as defined in [[conv]], which means it is
governed by the rules for initialization of an object or reference by a
single expression [[dcl.init]], [[dcl.init.ref]].

Implicit conversion sequences are concerned only with the type,
cv-qualification, and value category of the argument and how these are
converted to match the corresponding properties of the parameter.

[*Note 1*: Other properties, such as the lifetime, storage duration,
linkage, alignment, accessibility of the argument, whether the argument
is a bit-field, and whether a function is deleted
[[dcl.fct.def.delete]], are ignored. So, although an implicit conversion
sequence can be defined for a given argument-parameter pair, the
conversion from the argument to the parameter might still be ill-formed
in the final analysis. — *end note*]

A well-formed implicit conversion sequence is one of the following
forms:

- a standard conversion sequence [[over.ics.scs]],
- a user-defined conversion sequence [[over.ics.user]], or
- an ellipsis conversion sequence [[over.ics.ellipsis]].

However, if the target is

- the first parameter of a constructor or
- the object parameter of a user-defined conversion function

and the constructor or user-defined conversion function is a candidate
by

-  [[over.match.ctor]], when the argument is the temporary in the second
  step of a class copy-initialization,
-  [[over.match.copy]], [[over.match.conv]], or [[over.match.ref]] (in
  all cases), or
- the second phase of [[over.match.list]] when the initializer list has
  exactly one element that is itself an initializer list, and the target
  is the first parameter of a constructor of class `X`, and the
  conversion is to `X` or reference to cv `X`,

user-defined conversion sequences are not considered.

[*Note 2*: These rules prevent more than one user-defined conversion
from being applied during overload resolution, thereby avoiding infinite
recursion. — *end note*]

[*Example 1*:

``` cpp
struct Y { Y(int); };
struct A { operator int(); };
Y y1 = A();         // error: A::operator int() is not a candidate

struct X { X(); };
struct B { operator X(); };
B b;
X x{{b}};           // error: B::operator X() is not a candidate
```

— *end example*]

For the case where the parameter type is a reference, see 
[[over.ics.ref]].

When the parameter type is not a reference, the implicit conversion
sequence models a copy-initialization of the parameter from the argument
expression. The implicit conversion sequence is the one required to
convert the argument expression to a prvalue of the type of the
parameter.

[*Note 3*: When the parameter has a class type, this is a conceptual
conversion defined for the purposes of [[over]]; the actual
initialization is defined in terms of constructors and is not a
conversion. — *end note*]

When the cv-unqualified version of the type of the argument expression
is the same as the parameter type, the implicit conversion sequence is
an identity conversion. When the parameter has a class type and the
argument expression has a (possibly cv-qualified) derived class type,
the implicit conversion sequence is a derived-to-base conversion from
the derived class to the base class. A derived-to-base conversion has
Conversion rank [[over.ics.scs]].

[*Note 4*: There is no such standard conversion; this derived-to-base
conversion exists only in the description of implicit conversion
sequences. — *end note*]

[*Example 2*: An implicit conversion sequence from an argument of type
`const A` to a parameter of type `A` can be formed, even if overload
resolution for copy-initialization of `A` from the argument would not
find a viable function [[over.match.ctor]], [[over.match.viable]]. The
implicit conversion sequence for that case is the identity sequence; it
contains no “conversion” from `const A` to `A`. — *end example*]

When the parameter is the implicit object parameter of a static member
function, the implicit conversion sequence is a standard conversion
sequence that is neither better nor worse than any other standard
conversion sequence.

In all contexts, when converting to the implicit object parameter or
when converting to the left operand of an assignment operation only
standard conversion sequences are allowed.

[*Note 5*: When a conversion to the explicit object parameter occurs,
it can include user-defined conversion sequences. — *end note*]

If no conversions are required to match an argument to a parameter type,
the implicit conversion sequence is the standard conversion sequence
consisting of the identity conversion [[over.ics.scs]].

If no sequence of conversions can be found to convert an argument to a
parameter type, an implicit conversion sequence cannot be formed.

If there are multiple well-formed implicit conversion sequences
converting the argument to the parameter type, the implicit conversion
sequence associated with the parameter is defined to be the unique
conversion sequence designated the *ambiguous conversion sequence*. For
the purpose of ranking implicit conversion sequences as described in 
[[over.ics.rank]], the ambiguous conversion sequence is treated as a
user-defined conversion sequence that is indistinguishable from any
other user-defined conversion sequence.

[*Note 6*:

This rule prevents a function from becoming non-viable because of an
ambiguous conversion sequence for one of its parameters.

[*Example 3*:

``` cpp
class B;
class A { A (B&);};
class B { operator A (); };
class C { C (B&); };
void f(A) { }
void f(C) { }
B b;
f(b);               // error: ambiguous because there is a conversion b → C (via constructor)
                    // and an (ambiguous) conversion b → A (via constructor or conversion function)
void f(B) { }
f(b);               // OK, unambiguous
```

— *end example*]

— *end note*]

If a function that uses the ambiguous conversion sequence is selected as
the best viable function, the call will be ill-formed because the
conversion of one of the arguments in the call is ambiguous.

The three forms of implicit conversion sequences mentioned above are
defined in the following subclauses.

##### Standard conversion sequences <a id="over.ics.scs">[[over.ics.scs]]</a>

summarizes the conversions defined in [[conv]] and partitions them into
four disjoint categories: Lvalue Transformation, Qualification
Adjustment, Promotion, and Conversion.

[*Note 7*: These categories are orthogonal with respect to value
category, cv-qualification, and data representation: the Lvalue
Transformations do not change the cv-qualification or data
representation of the type; the Qualification Adjustments do not change
the value category or data representation of the type; and the
Promotions and Conversions do not change the value category or
cv-qualification of the type. — *end note*]

[*Note 8*: As described in [[conv]], a standard conversion sequence
either is the Identity conversion by itself (that is, no conversion) or
consists of one to three conversions from the other four categories. If
there are two or more conversions in the sequence, the conversions are
applied in the canonical order: **Lvalue Transformation**, **Promotion**
or **Conversion**, **Qualification Adjustment**. — *end note*]

Each conversion in [[over.ics.scs]] also has an associated rank (Exact
Match, Promotion, or Conversion). These are used to rank standard
conversion sequences [[over.ics.rank]]. The rank of a conversion
sequence is determined by considering the rank of each conversion in the
sequence and the rank of any reference binding [[over.ics.ref]]. If any
of those has Conversion rank, the sequence has Conversion rank;
otherwise, if any of those has Promotion rank, the sequence has
Promotion rank; otherwise, the sequence has Exact Match rank.

**Table: Conversions**

| Conversion              | Category | Rank | Subclause         |
| ----------------------- | -------- | ---- | ----------------- |
| No conversions required | Identity |      |                   |
| Integral promotions     |          |      | [[conv.prom]]     |
| Integral conversions    |          |      | [[conv.integral]] |


##### User-defined conversion sequences <a id="over.ics.user">[[over.ics.user]]</a>

A *user-defined conversion sequence* consists of an initial standard
conversion sequence followed by a user-defined conversion [[class.conv]]
followed by a second standard conversion sequence. If the user-defined
conversion is specified by a constructor [[class.conv.ctor]], the
initial standard conversion sequence converts the source type to the
type of the first parameter of that constructor. If the user-defined
conversion is specified by a conversion function [[class.conv.fct]], the
initial standard conversion sequence converts the source type to the
type of the object parameter of that conversion function.

The second standard conversion sequence converts the result of the
user-defined conversion to the target type for the sequence; any
reference binding is included in the second standard conversion
sequence. Since an implicit conversion sequence is an initialization,
the special rules for initialization by user-defined conversion apply
when selecting the best user-defined conversion for a user-defined
conversion sequence (see  [[over.match.best]] and  [[over.best.ics]]).

If the user-defined conversion is specified by a specialization of a
conversion function template, the second standard conversion sequence
shall have Exact Match rank.

A conversion of an expression of class type to the same class type is
given Exact Match rank, and a conversion of an expression of class type
to a base class of that type is given Conversion rank, in spite of the
fact that a constructor (i.e., a user-defined conversion function) is
called for those cases.

##### Ellipsis conversion sequences <a id="over.ics.ellipsis">[[over.ics.ellipsis]]</a>

An ellipsis conversion sequence occurs when an argument in a function
call is matched with the ellipsis parameter specification of the
function called (see  [[expr.call]]).

##### Reference binding <a id="over.ics.ref">[[over.ics.ref]]</a>

When a parameter of type “reference to cv `T`” binds directly
[[dcl.init.ref]] to an argument expression:

- If the argument expression has a type that is a derived class of the
  parameter type, the implicit conversion sequence is a derived-to-base
  conversion [[over.best.ics]].
- Otherwise, if the type of the argument is possibly cv-qualified `T`,
  or if `T` is an array type of unknown bound with element type `U` and
  the argument has an array type of known bound whose element type is
  possibly cv-qualified `U`, the implicit conversion sequence is the
  identity conversion.
- Otherwise, if `T` is a function type, the implicit conversion sequence
  is a function pointer conversion.
- Otherwise, the implicit conversion sequence is a qualification
  conversion.

[*Example 4*:

``` cpp
struct A {};
struct B : public A {} b;
int f(A&);
int f(B&);
int i = f(b);       // calls f(B&), an exact match, rather than f(A&), a conversion

void g() noexcept;
int h(void (&)() noexcept); // #1
int h(void (&)());          // #2
int j = h(g);               // calls #1, an exact match, rather than #2, a function pointer conversion
```

— *end example*]

If the parameter binds directly to the result of applying a conversion
function to the argument expression, the implicit conversion sequence is
a user-defined conversion sequence [[over.ics.user]] whose second
standard conversion sequence is determined by the above rules.

When a parameter of reference type is not bound directly to an argument
expression, the conversion sequence is the one required to convert the
argument expression to the referenced type according to 
[[over.best.ics]]. Conceptually, this conversion sequence corresponds to
copy-initializing a temporary of the referenced type with the argument
expression. Any difference in top-level cv-qualification is subsumed by
the initialization itself and does not constitute a conversion.

Except for an implicit object parameter, for which see 
[[over.match.funcs]], an implicit conversion sequence cannot be formed
if it requires binding an lvalue reference other than a reference to a
non-volatile `const` type to an rvalue or binding an rvalue reference to
an lvalue of object type.

[*Note 9*: This means, for example, that a candidate function cannot be
a viable function if it has a non-`const` lvalue reference parameter
(other than the implicit object parameter) and the corresponding
argument would require a temporary to be created to initialize the
lvalue reference (see  [[dcl.init.ref]]). — *end note*]

Other restrictions on binding a reference to a particular argument that
are not based on the types of the reference and the argument do not
affect the formation of an implicit conversion sequence, however.

[*Example 5*: A function with an “lvalue reference to `int`” parameter
can be a viable candidate even if the corresponding argument is an `int`
bit-field. The formation of implicit conversion sequences treats the
`int` bit-field as an `int` lvalue and finds an exact match with the
parameter. If the function is selected by overload resolution, the call
will nonetheless be ill-formed because of the prohibition on binding a
non-`const` lvalue reference to a bit-field
[[dcl.init.ref]]. — *end example*]

##### List-initialization sequence <a id="over.ics.list">[[over.ics.list]]</a>

When an argument is an initializer list [[dcl.init.list]], it is not an
expression and special rules apply for converting it to a parameter
type.

If the initializer list is a *designated-initializer-list* and the
parameter is not a reference, a conversion is only possible if the
parameter has an aggregate type that can be initialized from the
initializer list according to the rules for aggregate initialization
[[dcl.init.aggr]], in which case the implicit conversion sequence is a
user-defined conversion sequence whose second standard conversion
sequence is an identity conversion.

[*Note 10*:

Aggregate initialization does not require that the members are declared
in designation order. If, after overload resolution, the order does not
match for the selected overload, the initialization of the parameter
will be ill-formed [[dcl.init.list]].

[*Example 6*:

``` cpp
struct A { int x, y; };
struct B { int y, x; };
void f(A a, int);               // #1
void f(B b, ...);               // #2
void g(A a);                    // #3
void g(B b);                    // #4
void h() {
  f({.x = 1, .y = 2}, 0);       // OK; calls #1
  f({.y = 2, .x = 1}, 0);       // error: selects #1, initialization of a fails
                                // due to non-matching member order[dcl.init.list]
  g({.x = 1, .y = 2});          // error: ambiguous between #3 and #4
}
```

— *end example*]

— *end note*]

Otherwise, if the parameter type is an aggregate class `X` and the
initializer list has a single element of type cv `U`, where `U` is `X`
or a class derived from `X`, the implicit conversion sequence is the one
required to convert the element to the parameter type.

Otherwise, if the parameter type is a character array[^8]

and the initializer list has a single element that is an
appropriately-typed *string-literal* [[dcl.init.string]], the implicit
conversion sequence is the identity conversion.

Otherwise, if the parameter type is `std::initializer_list<X>` and all
the elements of the initializer list can be implicitly converted to `X`,
the implicit conversion sequence is the worst conversion necessary to
convert an element of the list to `X`, or if the initializer list has no
elements, the identity conversion. This conversion can be a user-defined
conversion even in the context of a call to an initializer-list
constructor.

[*Example 7*:

``` cpp
void f(std::initializer_list<int>);
f( {} );                        // OK, f(initializer_list<int>) identity conversion
f( {1,2,3} );                   // OK, f(initializer_list<int>) identity conversion
f( {'a','b'} );                 // OK, f(initializer_list<int>) integral promotion
f( {1.0} );                     // error: narrowing

struct A {
  A(std::initializer_list<double>);                     // #1
  A(std::initializer_list<std::complex<double>>);       // #2
  A(std::initializer_list<std::string>);                // #3
};
A a{ 1.0,2.0 };                 // OK, uses #1

void g(A);
g({ "foo", "bar" });            // OK, uses #3

typedef int IA[3];
void h(const IA&);
h({ 1, 2, 3 });                 // OK, identity conversion
```

— *end example*]

Otherwise, if the parameter type is “array of `N` `X`” or “array of
unknown bound of `X`”, if there exists an implicit conversion sequence
from each element of the initializer list (and from `{}` in the former
case if `N` exceeds the number of elements in the initializer list) to
`X`, the implicit conversion sequence is the worst such implicit
conversion sequence.

Otherwise, if the parameter is a non-aggregate class `X` and overload
resolution per  [[over.match.list]] chooses a single best constructor
`C` of `X` to perform the initialization of an object of type `X` from
the argument initializer list:

- If `C` is not an initializer-list constructor and the initializer list
  has a single element of type cv `U`, where `U` is `X` or a class
  derived from `X`, the implicit conversion sequence has Exact Match
  rank if `U` is `X`, or Conversion rank if `U` is derived from `X`.
- Otherwise, the implicit conversion sequence is a user-defined
  conversion sequence whose second standard conversion sequence is an
  identity conversion.

If multiple constructors are viable but none is better than the others,
the implicit conversion sequence is the ambiguous conversion sequence.
User-defined conversions are allowed for conversion of the initializer
list elements to the constructor parameter types except as noted in 
[[over.best.ics]].

[*Example 8*:

``` cpp
struct A {
  A(std::initializer_list<int>);
};
void f(A);
f( {'a', 'b'} );        // OK, f(A(std::initializer_list<int>)) user-defined conversion

struct B {
  B(int, double);
};
void g(B);
g( {'a', 'b'} );        // OK, g(B(int, double)) user-defined conversion
g( {1.0, 1.0} );        // error: narrowing

void f(B);
f( {'a', 'b'} );        // error: ambiguous f(A) or f(B)

struct C {
  C(std::string);
};
void h(C);
h({"foo"});             // OK, h(C(std::string("foo")))

struct D {
  D(A, C);
};
void i(D);
i({ {1,2}, {"bar"} });  // OK, i(D(A(std::initializer_list<int>{1,2\), C(std::string("bar"))))}
```

— *end example*]

Otherwise, if the parameter has an aggregate type which can be
initialized from the initializer list according to the rules for
aggregate initialization [[dcl.init.aggr]], the implicit conversion
sequence is a user-defined conversion sequence whose second standard
conversion sequence is an identity conversion.

[*Example 9*:

``` cpp
struct A {
  int m1;
  double m2;
};

void f(A);
f( {'a', 'b'} );        // OK, f(A(int,double)) user-defined conversion
f( {1.0} );             // error: narrowing
```

— *end example*]

Otherwise, if the parameter is a reference, see  [[over.ics.ref]].

[*Note 11*: The rules in this subclause will apply for initializing the
underlying temporary for the reference. — *end note*]

[*Example 10*:

``` cpp
struct A {
  int m1;
  double m2;
};

void f(const A&);
f( {'a', 'b'} );        // OK, f(A(int,double)) user-defined conversion
f( {1.0} );             // error: narrowing

void g(const double &);
g({1});                 // same conversion as int to double
```

— *end example*]

Otherwise, if the parameter type is not a class:

- if the initializer list has one element that is not itself an
  initializer list, the implicit conversion sequence is the one required
  to convert the element to the parameter type;
  \[*Example 8*:
  ``` cpp
  void f(int);
  f( {'a'} );             // OK, same conversion as char to int
  f( {1.0} );             // error: narrowing
  ```

  — *end example*]
- if the initializer list has no elements, the implicit conversion
  sequence is the identity conversion.
  \[*Example 9*:
  ``` cpp
  void f(int);
  f( { } );               // OK, identity conversion
  ```

  — *end example*]

In all cases other than those enumerated above, no conversion is
possible.

#### Ranking implicit conversion sequences <a id="over.ics.rank">[[over.ics.rank]]</a>

This subclause defines a partial ordering of implicit conversion
sequences based on the relationships *better conversion sequence* and
*better conversion*. If an implicit conversion sequence S1 is defined by
these rules to be a better conversion sequence than S2, then it is also
the case that S2 is a *worse conversion sequence* than S1. If conversion
sequence S1 is neither better than nor worse than conversion sequence
S2, S1 and S2 are said to be *indistinguishable conversion sequences*.

When comparing the basic forms of implicit conversion sequences (as
defined in  [[over.best.ics]])

- a standard conversion sequence [[over.ics.scs]] is a better conversion
  sequence than a user-defined conversion sequence or an ellipsis
  conversion sequence, and
- a user-defined conversion sequence [[over.ics.user]] is a better
  conversion sequence than an ellipsis conversion sequence
  [[over.ics.ellipsis]].

Two implicit conversion sequences of the same form are indistinguishable
conversion sequences unless one of the following rules applies:

- List-initialization sequence `L1` is a better conversion sequence than
  list-initialization sequence `L2` if
  - `L1` converts to `std::initializer_list<X>` for some `X` and `L2`
    does not, or, if not that,
  - `L1` and `L2` convert to arrays of the same element type, and either
    the number of elements n₁ initialized by `L1` is less than the
    number of elements n₂ initialized by `L2`, or n₁ = n₂ and `L2`
    converts to an array of unknown bound and `L1` does not,

  even if one of the other rules in this paragraph would otherwise
  apply.
  \[*Example 10*:
  ``` cpp
  void f1(int);                                   // #1
  void f1(std::initializer_list<long>);           // #2
  void g1() { f1({42}); }                         // chooses #2

  void f2(std::pair<const char*, const char*>);   // #3
  void f2(std::initializer_list<std::string>);    // #4
  void g2() { f2({"foo","bar"}); }                // chooses #4
  ```

  — *end example*]
  \[*Example 11*:
  ``` cpp
  void f(int    (&&)[] );         // #1
  void f(double (&&)[] );         // #2
  void f(int    (&&)[2]);         // #3

  f( {1} );           // Calls #1: Better than #2 due to conversion, better than #3 due to bounds
  f( {1.0} );         // Calls #2: Identity conversion is better than floating-integral conversion
  f( {1.0, 2.0} );    // Calls #2: Identity conversion is better than floating-integral conversion
  f( {1, 2} );        // Calls #3: Converting to array of known bound is better than to unknown bound,
                      // and an identity conversion is better than floating-integral conversion
  ```

  — *end example*]
- Standard conversion sequence `S1` is a better conversion sequence than
  standard conversion sequence `S2` if
  - `S1` is a proper subsequence of `S2` (comparing the conversion
    sequences in the canonical form defined by  [[over.ics.scs]],
    excluding any Lvalue Transformation; the identity conversion
    sequence is considered to be a subsequence of any non-identity
    conversion sequence) or, if not that,
  - the rank of `S1` is better than the rank of `S2`, or `S1` and `S2`
    have the same rank and are distinguishable by the rules in the
    paragraph below, or, if not that,
  - `S1` and `S2` include reference bindings [[dcl.init.ref]] and
    neither refers to an implicit object parameter of a non-static
    member function declared without a *ref-qualifier*, and `S1` binds
    an rvalue reference to an rvalue and `S2` binds an lvalue reference
    \[*Example 12*:
    ``` cpp
    int i;
    int f1();
    int&& f2();
    int g(const int&);
    int g(const int&&);
    int j = g(i);                   // calls g(const int&)
    int k = g(f1());                // calls g(const int&&)
    int l = g(f2());                // calls g(const int&&)

    struct A {
      A& operator<<(int);
      void p() &;
      void p() &&;
    };
    A& operator<<(A&&, char);
    A() << 1;                       // calls A::operator<<(int)
    A() << 'c';                     // calls operator<<(A&&, char)
    A a;
    a << 1;                         // calls A::operator<<(int)
    a << 'c';                       // calls A::operator<<(int)
    A().p();                        // calls A::p()&&
    a.p();                          // calls A::p()&
    ```

    — *end example*]
    or, if not that,
  - `S1` and `S2` include reference bindings [[dcl.init.ref]] and `S1`
    binds an lvalue reference to an lvalue of function type and `S2`
    binds an rvalue reference to an lvalue of function type
    \[*Example 13*:
    ``` cpp
    int f(void(&)());               // #1
    int f(void(&&)());              // #2
    void g();
    int i1 = f(g);                  // calls #1
    ```

    — *end example*]
    or, if not that,
  - `S1` and `S2` differ only in their qualification conversion
    [[conv.qual]] and yield similar types `T1` and `T2`, respectively
    (where a standard conversion sequence that is a reference binding is
    considered to yield the cv-unqualified referenced type), where `T1`
    and `T2` are not the same type, and `const T2` is
    reference-compatible with `T1` [[dcl.init.ref]]
    \[*Example 14*:
    ``` cpp
    int f(const volatile int *);
    int f(const int *);
    int i;
    int j = f(&i);                  // calls f(const int*)
    int g(const int*);
    int g(const volatile int* const&);
    int* p;
    int k = g(p);                   // calls g(const int*)
    ```

    — *end example*]
    or, if not that,
  - `S1`
    and `S2` bind “reference to `T1`” and “reference to `T2`”,
    respectively [[dcl.init.ref]], where `T1` and `T2` are not the same
    type, and `T2` is reference-compatible with `T1`
    \[*Example 15*:
    ``` cpp
    int f(const int &);
    int f(int &);
    int g(const int &);
    int g(int);

    int i;
    int j = f(i);                   // calls f(int &)
    int k = g(i);                   // ambiguous

    struct X {
      void f() const;
      void f();
    };
    void g(const X& a, X b) {
      a.f();                        // calls X::f() const
      b.f();                        // calls X::f()
    }

    int h(int (&)[]);
    int h(int (&)[1]);
    void g2() {
      int a[1];
      h(a);                         // calls h(int (&)[1])
    }
    ```

    — *end example*]
    or, if not that,
  - `S1` and `S2` bind the same reference type “reference to `T`” and
    have source types `V1` and `V2`, respectively, where the standard
    conversion sequence from `V1*` to `T*` is better than the standard
    conversion sequence from `V2*` to `T*`.
    \[*Example 16*:
    ``` cpp
    struct Z {};

    struct A {
      operator Z&();
      operator const Z&();          // #1
    };

    struct B {
      operator Z();
      operator const Z&&();         // #2
    };

    const Z& r1 = A();              // OK, uses #1
    const Z&& r2 = B();             // OK, uses #2
    ```

    — *end example*]
- User-defined conversion sequence `U1` is a better conversion sequence
  than another user-defined conversion sequence `U2` if they contain the
  same user-defined conversion function or constructor or they
  initialize the same class in an aggregate initialization and in either
  case the second standard conversion sequence of `U1` is better than
  the second standard conversion sequence of `U2`.
  \[*Example 17*:
  ``` cpp
  struct A {
    operator short();
  } a;
  int f(int);
  int f(float);
  int i = f(a);                   // calls f(int), because short → int is
                                  // better than short → float.
  ```

  — *end example*]

Standard conversion sequences are ordered by their ranks: an Exact Match
is a better conversion than a Promotion, which is a better conversion
than a Conversion. Two conversion sequences with the same rank are
indistinguishable unless one of the following rules applies:

- A conversion that does not convert a pointer or a pointer to member to
  `bool` is better than one that does.
- A conversion that promotes an enumeration whose underlying type is
  fixed to its underlying type is better than one that promotes to the
  promoted underlying type, if the two are different.
- A conversion in either direction between floating-point type `FP1` and
  floating-point type `FP2` is better than a conversion in the same
  direction between `FP1` and arithmetic type `T3` if
  - the floating-point conversion rank [[conv.rank]] of `FP1` is equal
    to the rank of `FP2`, and
  - `T3` is not a floating-point type, or `T3` is a floating-point type
    whose rank is not equal to the rank of `FP1`, or the floating-point
    conversion subrank [[conv.rank]] of `FP2` is greater than the
    subrank of `T3`.
    \[*Example 18*:
    ``` cpp
    int f(std::float32_t);
    int f(std::float64_t);
    int f(long long);
    float x;
    std::float16_t y;
    int i = f(x);           // calls f(std::float32_t) on implementations where
                            // float and std::float32_t have equal conversion ranks
    int j = f(y);           // error: ambiguous, no equal conversion rank
    ```

    — *end example*]
- If class `B` is derived directly or indirectly from class `A`,
  conversion of `B*` to `A*` is better than conversion of `B*` to
  `void*`, and conversion of `A*` to `void*` is better than conversion
  of `B*` to `void*`.
- If class `B` is derived directly or indirectly from class `A` and
  class `C` is derived directly or indirectly from `B`,
  - conversion of `C*` to `B*` is better than conversion of `C*` to
    `A*`,
    \[*Example 19*:
    ``` cpp
    struct A {};
    struct B : public A {};
    struct C : public B {};
    C* pc;
    int f(A*);
    int f(B*);
    int i = f(pc);                  // calls f(B*)
    ```

    — *end example*]
  - binding of an expression of type `C` to a reference to type `B` is
    better than binding an expression of type `C` to a reference to type
    `A`,
  - conversion of `A::*` to `B::*` is better than conversion of `A::*`
    to `C::*`,
  - conversion of `C` to `B` is better than conversion of `C` to `A`,
  - conversion of `B*` to `A*` is better than conversion of `C*` to
    `A*`,
  - binding of an expression of type `B` to a reference to type `A` is
    better than binding an expression of type `C` to a reference to type
    `A`,
  - conversion of `B::*` to `C::*` is better than conversion of `A::*`
    to `C::*`, and
  - conversion of `B` to `A` is better than conversion of `C` to `A`.

  \[*Note 3*: Compared conversion sequences will have different source
  types only in the context of comparing the second standard conversion
  sequence of an initialization by user-defined conversion (see 
  [[over.match.best]]); in all other contexts, the source types will be
  the same and the target types will be different. — *end note*]

## Address of an overload set <a id="over.over">[[over.over]]</a>

An expression that designates an overload set S and that appears without
arguments is resolved to a function, a pointer to function, or a pointer
to member function for a specific function that is chosen from a set of
functions selected from S determined based on the target type required
in the context (if any), as described below. The target can be

- an object or reference being initialized
  [[dcl.init]], [[dcl.init.ref]], [[dcl.init.list]],
- the left side of an assignment [[expr.assign]],
- a parameter of a function [[expr.call]],
- a parameter of a user-defined operator [[over.oper]],
- the return value of a function, operator function, or conversion
  [[stmt.return]],
- an explicit type conversion
  [[expr.type.conv]], [[expr.static.cast]], [[expr.cast]], or
- a constant template parameter [[temp.arg.nontype]].

If the target type contains a placeholder type, placeholder type
deduction is performed [[dcl.type.auto.deduct]], and the remainder of
this subclause uses the target type so deduced. The expression can be
preceded by the `&` operator.

[*Note 1*: Any redundant set of parentheses surrounding the function
name is ignored [[expr.prim.paren]]. — *end note*]

If there is no target, all non-template functions named are selected.
Otherwise, a non-template function with type `F` is selected for the
function type `FT` of the target type if `F` (after possibly applying
the function pointer conversion [[conv.fctptr]]) is identical to `FT`.

[*Note 2*: That is, the class of which the function is a member is
ignored when matching a pointer-to-member-function type. — *end note*]

The specialization, if any, generated by template argument deduction
[[temp.over]], [[temp.deduct.funcaddr]], [[temp.arg.explicit]] for each
function template named is added to the set of selected functions
considered.

Non-member functions, static member functions, and explicit object
member functions match targets of function pointer type or reference to
function type. Implicit object member functions match targets of
pointer-to-member-function type.

[*Note 3*: If an implicit object member function is chosen, the result
can be used only to form a pointer to member
[[expr.unary.op]]. — *end note*]

All functions with associated constraints that are not satisfied
[[temp.constr.decl]] are eliminated from the set of selected functions.
If more than one function in the set remains, all function template
specializations in the set are eliminated if the set also contains a
function that is not a function template specialization. Any given
non-template function `F0` is eliminated if the set contains a second
non-template function that is more partial-ordering-constrained than
`F0` [[temp.constr.order]]. Any given function template specialization
`F1` is eliminated if the set contains a second function template
specialization whose function template is more specialized than the
function template of `F1` according to the partial ordering rules of 
[[temp.func.order]]. After such eliminations, if any, there shall remain
exactly one selected function.

[*Example 1*:

``` cpp
int f(double);
int f(int);
int (*pfd)(double) = &f;        // selects f(double)
int (*pfi)(int) = &f;           // selects f(int)
int (*pfe)(...) = &f;           // error: type mismatch
int (&rfi)(int) = f;            // selects f(int)
int (&rfd)(double) = f;         // selects f(double)
void g() {
  (int (*)(int))&f;             // cast expression as selector
}
```

The initialization of `pfe` is ill-formed because no `f()` with type
`int(...)` has been declared, and not because of any ambiguity.

— *end example*]

[*Example 2*:

``` cpp
struct X {
  int f(int);
  static int f(long);
};

int (X::*p1)(int)  = &X::f;     // OK
int    (*p2)(int)  = &X::f;     // error: mismatch
int    (*p3)(long) = &X::f;     // OK
int (X::*p4)(long) = &X::f;     // error: mismatch
int (X::*p5)(int)  = &(X::f);   // error: wrong syntax for
                                // pointer to member
int    (*p6)(long) = &(X::f);   // OK
```

— *end example*]

[*Example 3*:

``` cpp
template<bool B> struct X {
  void f(short) requires B;
  void f(long);
  template<typename> void g(short) requires B;
  template<typename> void g(long);
};
void test() {
  &X<true>::f;                  // error: ambiguous; constraints are not considered
  &X<true>::g<int>;             // error: ambiguous; constraints are not considered
}
```

— *end example*]

[*Note 4*: If `f` and `g` are both overload sets, the Cartesian product
of possibilities is considered to resolve `f(&g)`, or the equivalent
expression `f(g)`. — *end note*]

[*Note 5*:

Even if `B` is a public base of `D`, we have

``` cpp
D* f();
B* (*p1)() = &f;                // error

void g(D*);
void (*p2)(B*) = &g;            // error
```

— *end note*]

## Overloaded operators <a id="over.oper">[[over.oper]]</a>

### General <a id="over.oper.general">[[over.oper.general]]</a>

A declaration whose *declarator-id* is an *operator-function-id* shall
declare a function or function template or an explicit instantiation or
specialization of a function template. A function so declared is an
*operator function*. A function template so declared is an
*operator function template*. A specialization of an operator function
template is also an operator function. An operator function is said to
*implement* the operator named in its *operator-function-id*.

``` bnf
operator-function-id:
    operator operator
```

``` bnf
%% Ed. note: character protrusion would misalign various operators.

operator: one of
    'new \ \ \ \ \ delete \ \ new[] \ \ \ delete[] co_await (\rlap{ )} \ \ \ \ \ \ \ [\rlap{ ]} \ \ \ \ \ \ \ -> \ \ \ \ \ \ ->*'
    '~\ \ \ \ \ \ \ ! \ \ \ \ \ \ \ + \ \ \ \ \ \ \ - \ \ \ \ \ \ \ * \ \ \ \ \ \ \ / \ \ \ \ \ \ \ % \ \ \ \ \ \ \ ^ \ \ \ \ \ \ \ &'
    '| \ \ \ \ \ \ \ = \ \ \ \ \ \ \ += \ \ \ \ \ \ -= \ \ \ \ \ \ *= \ \ \ \ \ \ /= \ \ \ \ \ \ %= \ \ \ \ \ \ ^= \ \ \ \ \ \ &='
    '|= \ \ \ \ \ \ == \ \ \ \ \ \ != \ \ \ \ \ \ < \ \ \ \ \ \ \ > \ \ \ \ \ \ \ <= \ \ \ \ \ \ >= \ \ \ \ \ \ <=> \ \ \ \ \ &&'
    '|| \ \ \ \ \ \ << \ \ \ \ \ \ >> \ \ \ \ \ \ <<= \ \ \ \ \ >>= \ \ \ \ \ ++ \ \ \ \ \ \ -- \ \ \ \ \ \ ,'
```

[*Note 1*: The operators `new[]`, `delete[]`, `()`, and `[]` are formed
from more than one token. The latter two operators are function call
[[expr.call]] and subscripting [[expr.sub]]. — *end note*]

Both the unary and binary forms of

``` bnf
'+ \ \ \ \ \ - \ \ \ \ \ * \ \ \ \ \ &'
```

can be overloaded.

[*Note 2*:

The following operators cannot be overloaded:

``` bnf
'. \ \ \ \ \ .* \ \ \ \ :: \ \ \ \ ?:'
```

nor can the preprocessing symbols `#` [[cpp.stringize]] and `##`
[[cpp.concat]].

— *end note*]

Operator functions are usually not called directly; instead they are
invoked to evaluate the operators they implement ([[over.unary]] –
[[over.inc]]). They can be explicitly called, however, using the
*operator-function-id* as the name of the function in the function call
syntax [[expr.call]].

[*Example 1*:

``` cpp
complex z = a.operator+(b);     // complex z = a+b;
void* p = operator new(sizeof(int)*n);
```

— *end example*]

The allocation and deallocation functions, `operator` `new`, `operator`
`new[]`, `operator` `delete`, and `operator` `delete[]`, are described
completely in  [[basic.stc.dynamic]]. The attributes and restrictions
found in the rest of [[over.oper]] do not apply to them unless
explicitly stated in  [[basic.stc.dynamic]].

The `co_await` operator is described completely in  [[expr.await]]. The
attributes and restrictions found in the rest of [[over.oper]] do not
apply to it unless explicitly stated in  [[expr.await]].

An operator function shall have at least one function parameter or
implicit object parameter whose type is a class, a reference to a class,
an enumeration, or a reference to an enumeration. It is not possible to
change the precedence, grouping, or number of operands of operators. The
meaning of the operators `=`, (unary) `&`, and `,` (comma), predefined
for each type, can be changed for specific class types by defining
operator functions that implement these operators. Likewise, the meaning
of the operators (unary) `&` and `,` (comma) can be changed for specific
enumeration types. Operator functions are inherited in the same manner
as other base class functions.

An operator function shall be a prefix unary, binary, function call,
subscripting, class member access, increment, or decrement operator
function.

[*Note 3*: The identities among certain predefined operators applied to
fundamental types (for example, `++a` ≡ `a+=1`) need not hold for
operator functions. Some predefined operators, such as `+=`, require an
operand to be an lvalue when applied to fundamental types; this is not
required by operator functions. — *end note*]

An operator function cannot have default arguments [[dcl.fct.default]],
except where explicitly stated below. Operator functions cannot have
more or fewer parameters than the number required for the corresponding
operator, as described in the rest of [[over.oper]].

Operators not mentioned explicitly in subclauses  [[over.assign]]
through  [[over.inc]] act as ordinary unary and binary operators obeying
the rules of  [[over.unary]] or  [[over.binary]].

### Unary operators <a id="over.unary">[[over.unary]]</a>

A *prefix unary operator function* is a function named `operator@` for a
prefix *unary-operator* `@` [[expr.unary.op]] that is either a
non-static member function [[class.mfct]] with no non-object parameters
or a non-member function with one parameter. For a *unary-expression* of
the form `@ cast-expression`, the operator function is selected by
overload resolution [[over.match.oper]]. If a member function is
selected, the expression is interpreted as

``` bnf
cast-expression '.' operator '@' '('')'
```

Otherwise, if a non-member function is selected, the expression is
interpreted as

``` bnf
operator '@' '(' cast-expression ')'
```

[*Note 1*: The operators `++` and `--` [[expr.pre.incr]] are described
in  [[over.inc]]. — *end note*]

[*Note 2*: The unary and binary forms of the same operator have the
same name. Consequently, a unary operator can hide a binary operator
from an enclosing scope, and vice versa. — *end note*]

### Binary operators <a id="over.binary">[[over.binary]]</a>

#### General <a id="over.binary.general">[[over.binary.general]]</a>

A *binary operator function* is a function named `operator@` for a
binary operator `@` that is either a non-static member function
[[class.mfct]] with one non-object parameter or a non-member function
with two parameters. For an expression `x @ y` with subexpressions x and
y, the operator function is selected by overload resolution
[[over.match.oper]]. If a member function is selected, the expression is
interpreted as

``` bnf
x '.' operator '@' '(' y ')'
```

Otherwise, if a non-member function is selected, the expression is
interpreted as

``` bnf
operator '@' '(' x ',' y ')'
```

An *equality operator function* is an operator function for an equality
operator [[expr.eq]]. A *relational operator function* is an operator
function for a relational operator [[expr.rel]]. A
*three-way comparison operator function* is an operator function for the
three-way comparison operator [[expr.spaceship]]. A
*comparison operator function* is an equality operator function, a
relational operator function, or a three-way comparison operator
function.

#### Simple assignment <a id="over.assign">[[over.assign]]</a>

A *simple assignment operator function* is a binary operator function
named `operator=`. A simple assignment operator function shall be a
non-static member function.

[*Note 1*: Because only standard conversion sequences are considered
when converting to the left operand of an assignment operation
[[over.best.ics]], an expression `x = y` with a subexpression x of class
type is always interpreted as `x.operator=(y)`. — *end note*]

[*Note 2*: Since a copy assignment operator is implicitly declared for
a class if not declared by the user [[class.copy.assign]], a base class
assignment operator function is always hidden by the copy assignment
operator function of the derived class. — *end note*]

[*Note 3*:

Any assignment operator function, even the copy and move assignment
operators, can be virtual. For a derived class `D` with a base class `B`
for which a virtual copy/move assignment has been declared, the
copy/move assignment operator in `D` does not override `B`’s virtual
copy/move assignment operator.

[*Example 1*:

``` cpp
struct B {
  virtual int operator= (int);
  virtual B& operator= (const B&);
};
struct D : B {
  virtual int operator= (int);
  virtual D& operator= (const B&);
};

D dobj1;
D dobj2;
B* bptr = &dobj1;
void f() {
  bptr->operator=(99);          // calls D::operator=(int)
  *bptr = 99;                   // ditto
  bptr->operator=(dobj2);       // calls D::operator=(const B&)
  *bptr = dobj2;                // ditto
  dobj1 = dobj2;                // calls implicitly-declared D::operator=(const D&)
}
```

— *end example*]

— *end note*]

### Function call <a id="over.call">[[over.call]]</a>

A *function call operator function* is a function named `operator()`
that is a member function with an arbitrary number of parameters. It may
have default arguments. For an expression of the form

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

where the *postfix-expression* is of class type, the operator function
is selected by overload resolution [[over.call.object]]. If a surrogate
call function is selected, let e be the result of invoking the
corresponding conversion operator function on the *postfix-expression*;

the expression is interpreted as

``` bnf
e '(' expression-listₒₚₜ ')'
```

Otherwise, the expression is interpreted as

``` bnf
postfix-expression '.' operator '('')' '(' expression-listₒₚₜ ')'
```

### Subscripting <a id="over.sub">[[over.sub]]</a>

A *subscripting operator function* is a member function named
`operator[]` with an arbitrary number of parameters. It may have default
arguments. For an expression of the form

``` bnf
postfix-expression '[' expression-listₒₚₜ ']'
```

the operator function is selected by overload resolution
[[over.match.oper]]. If a member function is selected, the expression is
interpreted as

``` bnf
postfix-expression . operator '['']' '(' expression-listₒₚₜ ')'
```

[*Example 1*:

``` cpp
struct X {
  Z operator[](std::initializer_list<int>);
  Z operator[](auto...);
};
X x;
x[{1,2,3}] = 7;                 // OK, meaning x.operator[]({1,2,3\)}
x[1,2,3] = 7;                   // OK, meaning x.operator[](1,2,3)
int a[10];
a[{1,2,3}] = 7;                 // error: built-in subscript operator
a[1,2,3] = 7;                   // error: built-in subscript operator
```

— *end example*]

### Class member access <a id="over.ref">[[over.ref]]</a>

A *class member access operator function* is a function named
`operator->` that is a non-static member function taking no non-object
parameters. For an expression of the form

``` bnf
postfix-expression '->' templateₒₚₜ id-expression
```

the operator function is selected by overload resolution
[[over.match.oper]], and the expression is interpreted as

``` bnf
'(' postfix-expression . operator '->' '('')' ')' '->' templateₒₚₜ id-expression
```

### Increment and decrement <a id="over.inc">[[over.inc]]</a>

An *increment operator function* is a function named `operator++`. If
this function is a non-static member function with no non-object
parameters, or a non-member function with one parameter, it defines the
prefix increment operator `++` for objects of that type. If the function
is a non-static member function with one non-object parameter (which
shall be of type `int`) or a non-member function with two parameters
(the second of which shall be of type `int`), it defines the postfix
increment operator `++` for objects of that type. When the postfix
increment is called as a result of using the `++` operator, the `int`
argument will have value zero.[^9]

[*Example 1*:

``` cpp
struct X {
  X&   operator++();            // prefix ++a
  X    operator++(int);         // postfix a++
};

struct Y { };
Y&   operator++(Y&);            // prefix ++b
Y    operator++(Y&, int);       // postfix b++

void f(X a, Y b) {
  ++a;                          // a.operator++();
  a++;                          // a.operator++(0);
  ++b;                          // operator++(b);
  b++;                          // operator++(b, 0);

  a.operator++();               // explicit call: like ++a;
  a.operator++(0);              // explicit call: like a++;
  operator++(b);                // explicit call: like ++b;
  operator++(b, 0);             // explicit call: like b++;
}
```

— *end example*]

A *decrement operator function* is a function named `operator--` and is
handled analogously to an increment operator function.

## Built-in operators <a id="over.built">[[over.built]]</a>

The candidate operator functions that represent the built-in operators
defined in [[expr.compound]] are specified in this subclause. These
candidate functions participate in the operator overload resolution
process as described in  [[over.match.oper]] and are used for no other
purpose.

[*Note 1*: Because built-in operators take only operands with non-class
type, and operator overload resolution occurs only when an operand
expression originally has class or enumeration type, operator overload
resolution can resolve to a built-in operator only when an operand has a
class type that has a user-defined conversion to a non-class type
appropriate for the operator, or when an operand has an enumeration type
that can be converted to a type appropriate for the operator. Also note
that some of the candidate operator functions given in this subclause
are more permissive than the built-in operators themselves. As described
in  [[over.match.oper]], after a built-in operator is selected by
overload resolution the expression is subject to the requirements for
the built-in operator given in [[expr.compound]], and therefore to any
additional semantic constraints given there. In some cases, user-written
candidates with the same name and parameter types as a built-in
candidate operator function cause the built-in operator function to not
be included in the set of candidate functions. — *end note*]

In this subclause, the term *promoted integral type* is used to refer to
those cv-unqualified integral types which are preserved by integral
promotion [[conv.prom]] (including e.g. `int` and `long` but excluding
e.g. `char`).

[*Note 2*: In all cases where a promoted integral type is required, an
operand of unscoped enumeration type will be acceptable by way of the
integral promotions. — *end note*]

In the remainder of this subclause, cv-qualifiervq represents either
`volatile` or no cv-qualifier.

For every pair (`T`, cv-qualifiervq), where `T` is a cv-unqualified
arithmetic type other than `bool` or a cv-unqualified pointer to
(possibly cv-qualified) object type, there exist candidate operator
functions of the form

``` cpp
cv-qualifier{vq} T& operator++(cv-qualifier{vq} T&);
T operator++(cv-qualifier{vq} T&, int);
cv-qualifier{vq} T& operator--(cv-qualifier{vq} T&);
T operator--(cv-qualifier{vq} T&, int);
```

For every (possibly cv-qualified) object type `T` and for every function
type `T` that has neither *cv-qualifier*s nor a *ref-qualifier*, there
exist candidate operator functions of the form

``` cpp
T&    operator*(T*);
```

For every type `T` there exist candidate operator functions of the form

``` cpp
T*    operator+(T*);
```

For every cv-unqualified floating-point or promoted integral type `T`,
there exist candidate operator functions of the form

``` cpp
T operator+(T);
T operator-(T);
```

For every promoted integral type `T`, there exist candidate operator
functions of the form

``` cpp
T operator~(T);
```

For every quintuple (`C1`, `C2`, `T`, cv-qualifiercv1, cv-qualifiercv2),
where `C2` is a class type, `C1` is the same type as `C2` or is a
derived class of `C2`, and `T` is an object type or a function type,
there exist candidate operator functions of the form

``` cpp
cv-qualifier{cv12} T& operator->*(cv-qualifier{cv1} C1*, cv-qualifier{cv2} T C2::*);
```

where cv-qualifiercv12 is the union of cv-qualifiercv1 and
cv-qualifiercv2. The return type is shown for exposition only; see 
[[expr.mptr.oper]] for the determination of the operator’s result type.

For every pair of types `L` and `R`, where each of `L` and `R` is a
floating-point or promoted integral type, there exist candidate operator
functions of the form

``` cpp
LR      operator*(L, R);
LR      operator/(L, R);
LR      operator+(L, R);
LR      operator-(L, R);
bool    operator==(L, R);
bool    operator!=(L, R);
bool    operator<(L, R);
bool    operator>(L, R);
bool    operator<=(L, R);
bool    operator>=(L, R);
```

where `LR` is the result of the usual arithmetic conversions
[[expr.arith.conv]] between types `L` and `R`.

For every integral type `T` there exists a candidate operator function
of the form

``` cpp
std::strong_ordering operator<=>(T, T);
```

For every pair of floating-point types `L` and `R`, there exists a
candidate operator function of the form

``` cpp
std::partial_ordering operator<=>(L, R);
```

For every cv-qualified or cv-unqualified object type `T` there exist
candidate operator functions of the form

``` cpp
T*      operator+(T*, std::ptrdiff_t);
T&      operator[](T*, std::ptrdiff_t);
T*      operator-(T*, std::ptrdiff_t);
T*      operator+(std::ptrdiff_t, T*);
T&      operator[](std::ptrdiff_t, T*);
```

For every `T`, where `T` is a pointer to object type, there exist
candidate operator functions of the form

``` cpp
std::ptrdiff_t   operator-(T, T);
```

For every `T`, where `T` is an enumeration type or a pointer type, there
exist candidate operator functions of the form

``` cpp
bool    operator==(T, T);
bool    operator!=(T, T);
bool    operator<(T, T);
bool    operator>(T, T);
bool    operator<=(T, T);
bool    operator>=(T, T);
R       operator<=>(T, T);
```

where `R` is the result type specified in [[expr.spaceship]].

For every `T`, where `T` is a pointer-to-member type, `std::meta::info`,
or `std::nullptr_t`, there exist candidate operator functions of the
form

``` cpp
bool operator==(T, T);
bool operator!=(T, T);
```

For every pair of promoted integral types `L` and `R`, there exist
candidate operator functions of the form

``` cpp
LR      operator%(L, R);
LR      operator&(L, R);
LR      operator^(L, R);
LR      operator|(L, R);
L       operator<<(L, R);
L       operator>>(L, R);
```

where `LR` is the result of the usual arithmetic conversions
[[expr.arith.conv]] between types `L` and `R`.

For every triple (`L`, cv-qualifiervq, `R`), where `L` is an arithmetic
type, and `R` is a floating-point or promoted integral type, there exist
candidate operator functions of the form

``` cpp
cv-qualifier{vq} L&   operator=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator*=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator/=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator+=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator-=(cv-qualifier{vq} L&, R);
```

For every pair (`T`, cv-qualifiervq), where `T` is any type, there exist
candidate operator functions of the form

``` cpp
T*cv-qualifier{vq}&   operator=(T*cv-qualifier{vq}&, T*);
```

For every pair (`T`, cv-qualifiervq), where `T` is an enumeration or
pointer-to-member type, there exist candidate operator functions of the
form

``` cpp
cv-qualifier{vq} T&   operator=(cv-qualifier{vq} T&, T);
```

For every pair (`T`, cv-qualifiervq), where `T` is a cv-qualified or
cv-unqualified object type, there exist candidate operator functions of
the form

``` cpp
T*cv-qualifier{vq}&   operator+=(T*cv-qualifier{vq}&, std::ptrdiff_t);
T*cv-qualifier{vq}&   operator-=(T*cv-qualifier{vq}&, std::ptrdiff_t);
```

For every triple (`L`, cv-qualifiervq, `R`), where `L` is an integral
type, and `R` is a promoted integral type, there exist candidate
operator functions of the form

``` cpp
cv-qualifier{vq} L&   operator%=(\cvqual{vq} L&, R);
cv-qualifier{vq} L&   operator<<=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator>>=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator&=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator^=(cv-qualifier{vq} L&, R);
cv-qualifier{vq} L&   operator|=(cv-qualifier{vq} L&, R);
```

There also exist candidate operator functions of the form

``` cpp
bool    operator!(bool);
bool    operator&&(bool, bool);
bool    operator||(bool, bool);
```

For every pair of types `L` and `R`, where each of `L` and `R` is a
floating-point or promoted integral type, there exist candidate operator
functions of the form

``` cpp
LR      operator?:(bool, L, R);
```

where `LR` is the result of the usual arithmetic conversions
[[expr.arith.conv]] between types `L` and `R`.

[*Note 3*: As with all these descriptions of candidate functions, this
declaration serves only to describe the built-in operator for purposes
of overload resolution. The operator “`?:`” cannot be
overloaded. — *end note*]

For every type `T`, where `T` is a pointer, pointer-to-member, or scoped
enumeration type, there exist candidate operator functions of the form

``` cpp
T       operator?:(bool, T, T);
```

## User-defined literals <a id="over.literal">[[over.literal]]</a>

``` bnf
literal-operator-id:
    operator unevaluated-string identifier
    operator user-defined-string-literal
```

The *user-defined-string-literal* in a *literal-operator-id* shall have
no *encoding-prefix*. The *unevaluated-string* or
*user-defined-string-literal* shall be empty. The *ud-suffix* of the
*user-defined-string-literal* or the *identifier* in a
*literal-operator-id* is called a *literal suffix identifier*. The first
form of *literal-operator-id* is deprecated [[depr.lit]]. Some literal
suffix identifiers are reserved for future standardization; see 
[[usrlit.suffix]]. A declaration whose *literal-operator-id* uses such a
literal suffix identifier is ill-formed, no diagnostic required.

A declaration whose *declarator-id* is a *literal-operator-id* shall
declare a function or function template that belongs to a namespace (it
could be a friend function [[class.friend]]) or an explicit
instantiation or specialization of a function template. A function
declared with a *literal-operator-id* is a *literal
operator*. A function template declared with a *literal-operator-id* is
a *literal operator template*.

The declaration of a literal operator shall have a
*parameter-declaration-clause* equivalent to one of the following:

``` cpp
const char*
unsigned long long int
long double
char
wchar_t
char8_t
char16_t
char32_t
const char*, std::size_t
const wchar_t*, std::size_t
const char8_t*, std::size_t
const char16_t*, std::size_t
const char32_t*, std::size_t
```

If a parameter has a default argument [[dcl.fct.default]], the program
is ill-formed.

A *raw literal operator* is a literal operator with a single parameter
whose type is `const char*`.

A *numeric literal operator template* is a literal operator template
whose *template-parameter-list* has a single *template-parameter* that
is a constant template parameter pack [[temp.variadic]] with element
type `char`. A *string literal operator template* is a literal operator
template whose *template-parameter-list* comprises a single
*parameter-declaration* that declares a constant template parameter of
class type. The declaration of a literal operator template shall have an
empty *parameter-declaration-clause* and shall declare either a numeric
literal operator template or a string literal operator template.

Literal operators and literal operator templates shall not have C
language linkage.

[*Note 1*: Literal operators and literal operator templates are usually
invoked implicitly through user-defined literals [[lex.ext]]. However,
except for the constraints described above, they are ordinary
namespace-scope functions and function templates. In particular, they
are looked up like ordinary functions and function templates and they
follow the same overload resolution rules. Also, they can be declared
`inline` or `constexpr`, they can have internal, module, or external
linkage, they can be called explicitly, their addresses can be taken,
etc. — *end note*]

[*Example 1*:

``` cpp
void operator ""_km(long double);                   // OK
string operator "" _i18n(const char*, std::size_t); // OK, deprecated
template <char...> double operator ""_\u03C0();     // OK, UCN for lowercase pi
float operator ""_e(const char*);                   // OK
float operator ""E(const char*);                    // ill-formed, no diagnostic required:
                                                    // reserved literal suffix[usrlit.suffix,lex.ext]
double operator""_Bq(long double);                  // OK, does not use the reserved identifier _Bq[lex.name]
double operator"" _Bq(long double);                 // ill-formed, no diagnostic required:
                                                    // uses the reserved identifier _Bq[lex.name]
float operator " "B(const char*);                   // error: non-empty string-literal
string operator ""5X(const char*, std::size_t);     // error: invalid literal suffix identifier
double operator ""_miles(double);                   // error: invalid parameter-declaration-clause
template <char...> int operator ""_j(const char*);  // error: invalid parameter-declaration-clause
extern "C" void operator ""_m(long double);         // error: C language linkage
```

— *end example*]

<!-- Link reference definitions -->
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope.scope]: basic.md#basic.scope.scope
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[class.access]: class.md#class.access
[class.conv]: class.md#class.conv
[class.conv.ctor]: class.md#class.conv.ctor
[class.conv.fct]: class.md#class.conv.fct
[class.copy.assign]: class.md#class.copy.assign
[class.copy.ctor]: class.md#class.copy.ctor
[class.friend]: class.md#class.friend
[class.inhctor.init]: class.md#class.inhctor.init
[class.mem]: class.md#class.mem
[class.member.lookup]: basic.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[conv]: expr.md#conv
[conv.array]: expr.md#conv.array
[conv.bool]: expr.md#conv.bool
[conv.double]: expr.md#conv.double
[conv.fctptr]: expr.md#conv.fctptr
[conv.fpint]: expr.md#conv.fpint
[conv.fpprom]: expr.md#conv.fpprom
[conv.func]: expr.md#conv.func
[conv.integral]: expr.md#conv.integral
[conv.lval]: expr.md#conv.lval
[conv.mem]: expr.md#conv.mem
[conv.prom]: expr.md#conv.prom
[conv.ptr]: expr.md#conv.ptr
[conv.qual]: expr.md#conv.qual
[conv.rank]: basic.md#conv.rank
[cpp.concat]: cpp.md#cpp.concat
[cpp.stringize]: cpp.md#cpp.stringize
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.fct.spec]: dcl.md#dcl.fct.spec
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.init.string]: dcl.md#dcl.init.string
[dcl.type.auto.deduct]: dcl.md#dcl.type.auto.deduct
[dcl.type.class.deduct]: dcl.md#dcl.type.class.deduct
[dcl.type.simple]: dcl.md#dcl.type.simple
[depr.lit]: future.md#depr.lit
[expr.arith.conv]: expr.md#expr.arith.conv
[expr.assign]: expr.md#expr.assign
[expr.await]: expr.md#expr.await
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.compound]: expr.md#expr.compound
[expr.cond]: expr.md#expr.cond
[expr.eq]: expr.md#expr.eq
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.pre.incr]: expr.md#expr.pre.incr
[expr.prim.paren]: expr.md#expr.prim.paren
[expr.prim.splice]: expr.md#expr.prim.splice
[expr.prim.this]: expr.md#expr.prim.this
[expr.rel]: expr.md#expr.rel
[expr.spaceship]: expr.md#expr.spaceship
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.type.conv]: expr.md#expr.type.conv
[expr.unary.op]: expr.md#expr.unary.op
[lex.ext]: lex.md#lex.ext
[namespace.udecl]: dcl.md#namespace.udecl
[over]: #over
[over.assign]: #over.assign
[over.best.ics]: #over.best.ics
[over.best.ics.general]: #over.best.ics.general
[over.binary]: #over.binary
[over.binary.general]: #over.binary.general
[over.built]: #over.built
[over.call]: #over.call
[over.call.func]: #over.call.func
[over.call.object]: #over.call.object
[over.ics.ellipsis]: #over.ics.ellipsis
[over.ics.list]: #over.ics.list
[over.ics.rank]: #over.ics.rank
[over.ics.ref]: #over.ics.ref
[over.ics.scs]: #over.ics.scs
[over.ics.user]: #over.ics.user
[over.inc]: #over.inc
[over.literal]: #over.literal
[over.match]: #over.match
[over.match.best]: #over.match.best
[over.match.best.general]: #over.match.best.general
[over.match.call]: #over.match.call
[over.match.call.general]: #over.match.call.general
[over.match.class.deduct]: #over.match.class.deduct
[over.match.conv]: #over.match.conv
[over.match.copy]: #over.match.copy
[over.match.ctor]: #over.match.ctor
[over.match.funcs]: #over.match.funcs
[over.match.funcs.general]: #over.match.funcs.general
[over.match.general]: #over.match.general
[over.match.list]: #over.match.list
[over.match.oper]: #over.match.oper
[over.match.ref]: #over.match.ref
[over.match.viable]: #over.match.viable
[over.oper]: #over.oper
[over.oper.general]: #over.oper.general
[over.over]: #over.over
[over.pre]: #over.pre
[over.ref]: #over.ref
[over.sub]: #over.sub
[over.unary]: #over.unary
[stmt.return]: stmt.md#stmt.return
[temp.arg.explicit]: temp.md#temp.arg.explicit
[temp.arg.nontype]: temp.md#temp.arg.nontype
[temp.constr.constr]: temp.md#temp.constr.constr
[temp.constr.decl]: temp.md#temp.constr.decl
[temp.constr.order]: temp.md#temp.constr.order
[temp.deduct]: temp.md#temp.deduct
[temp.deduct.funcaddr]: temp.md#temp.deduct.funcaddr
[temp.deduct.guide]: temp.md#temp.deduct.guide
[temp.deduct.type]: temp.md#temp.deduct.type
[temp.dep]: temp.md#temp.dep
[temp.dep.type]: temp.md#temp.dep.type
[temp.func.order]: temp.md#temp.func.order
[temp.over]: temp.md#temp.over
[temp.variadic]: temp.md#temp.variadic
[usrlit.suffix]: library.md#usrlit.suffix

[^1]: The process of argument deduction fully determines the parameter
    types of the function template specializations, i.e., the parameters
    of function template specializations contain no template parameter
    types. Therefore, except where specified otherwise, function
    template specializations and non-template functions [[dcl.fct]] are
    treated equivalently for the remainder of overload resolution.

[^2]: Note that cv-qualifiers on the type of objects are significant in
    overload resolution for both glvalue and class prvalue objects.

[^3]: An implied object argument is contrived to correspond to the
    implicit object parameter attributed to member functions during
    overload resolution. It is not used in the call to the selected
    function. Since the member functions all have the same implicit
    object parameter, the contrived object will not be the cause to
    select or reject a function.

[^4]: Note that this construction can yield candidate call functions
    that cannot be differentiated one from the other by overload
    resolution because they have identical declarations or differ only
    in their return type. The call will be ambiguous if overload
    resolution cannot select a match to the call that is uniquely better
    than such undifferentiable functions.

[^5]: If the set of candidate functions is empty, overload resolution is
    unsuccessful.

[^6]: If the value returned by the `operator->` function has class type,
    this can result in selecting and calling another `operator->`
    function. The process repeats until an `operator->` function returns
    a value of non-class type.

[^7]: The algorithm for selecting the best viable function is linear in
    the number of viable functions. Run a simple tournament to find a
    function `W` that is not worse than any opponent it faced. Although
    it is possible that another function `F` that `W` did not face is at
    least as good as `W`, `F` cannot be the best function because at
    some point in the tournament `F` encountered another function `G`
    such that `F` was not better than `G`. Hence, either `W` is the best
    function or there is no best function. So, make a second pass over
    the viable functions to verify that `W` is better than all other
    functions.

[^8]: Since there are no parameters of array type, this will only occur
    as the referenced type of a reference parameter.

[^9]: Calling `operator++` explicitly, as in expressions like
    `a.operator++(2)`, has no special properties: The argument to
    `operator++` is `2`.
