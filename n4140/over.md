# Overloading <a id="over">[[over]]</a>

When two or more different declarations are specified for a single name
in the same scope, that name is said to be *overloaded*. By extension,
two declarations in the same scope that declare the same name but with
different types are called *overloaded declarations*. Only function and
function template declarations can be overloaded; variable and type
declarations cannot be overloaded.

When an overloaded function name is used in a call, which overloaded
function declaration is being referenced is determined by comparing the
types of the arguments at the point of use with the types of the
parameters in the overloaded declarations that are visible at the point
of use. This function selection process is called *overload resolution*
and is defined in  [[over.match]].

``` cpp
double abs(double);
int abs(int);

abs(1);             // calls abs(int);
abs(1.0);           // calls abs(double);
```

## Overloadable declarations <a id="over.load">[[over.load]]</a>

Not all function declarations can be overloaded. Those that cannot be
overloaded are specified here. A program is ill-formed if it contains
two such non-overloadable declarations in the same scope. This
restriction applies to explicit declarations in a scope, and between
such declarations and declarations made through a *using-declaration* (
[[namespace.udecl]]). It does not apply to sets of functions fabricated
as a result of name lookup (e.g., because of *using-directive*s) or
overload resolution (e.g., for operator functions).

Certain function declarations cannot be overloaded:

- Function declarations that differ only in the return type cannot be
  overloaded.
- Member function declarations with the same name and the same
  *parameter-type-list* cannot be overloaded if any of them is a
  `static` member function declaration ([[class.static]]). Likewise,
  member function template declarations with the same name, the same
  *parameter-type-list*, and the same template parameter lists cannot be
  overloaded if any of them is a `static` member function template
  declaration. The types of the implicit object parameters constructed
  for the member functions for the purpose of overload resolution (
  [[over.match.funcs]]) are not considered when comparing
  parameter-type-lists for enforcement of this rule. In contrast, if
  there is no `static` member function declaration among a set of member
  function declarations with the same name and the same
  parameter-type-list, then these member function declarations can be
  overloaded if they differ in the type of their implicit object
  parameter. the following illustrates this distinction:
  ``` cpp
  class X {
    static void f();
    void f();                     // ill-formed
    void f() const;               // ill-formed
    void f() const volatile;      // ill-formed
    void g();
    void g() const;               // OK: no static g
    void g() const volatile;      // OK: no static g
  };
  ```
- Member function declarations with the same name and the same
  *parameter-type-list* as well as member function template declarations
  with the same name, the same *parameter-type-list*, and the same
  template parameter lists cannot be overloaded if any of them, but not
  all, have a *ref-qualifier* ([[dcl.fct]]).
  ``` cpp
  class Y {
    void h() &;
    void h() const &;             // OK
    void h() &&;                  // OK, all declarations have a ref-qualifier
    void i() &;
    void i() const;               // ill-formed, prior declaration of i
                                  // has a ref-qualifier
  };
  ```

As specified in  [[dcl.fct]], function declarations that have equivalent
parameter declarations declare the same function and therefore cannot be
overloaded:

- Parameter declarations that differ only in the use of equivalent
  typedef “types” are equivalent. A `typedef` is not a separate type,
  but only a synonym for another type ([[dcl.typedef]]).
  ``` cpp
  typedef int Int;

  void f(int i);
  void f(Int i);                  // OK: redeclaration of f(int)
  void f(int i) { /* ... */ }
  void f(Int i) { /* ... */ }    // error: redefinition of f(int)
  ```

  Enumerations, on the other hand, are distinct types and can be used to
  distinguish overloaded function declarations.
  ``` cpp
  enum E { a };

  void f(int i) { /* ... */ }
  void f(E i)   { /* ... */ }
  ```
- Parameter declarations that differ only in a pointer `*` versus an
  array `[]` are equivalent. That is, the array declaration is adjusted
  to become a pointer declaration ([[dcl.fct]]). Only the second and
  subsequent array dimensions are significant in parameter types (
  [[dcl.array]]).
  ``` cpp
  int f(char*);
  int f(char[]);                  // same as f(char*);
  int f(char[7]);                 // same as f(char*);
  int f(char[9]);                 // same as f(char*);

  int g(char(*)[10]);
  int g(char[5][10]);             // same as g(char(*)[10]);
  int g(char[7][10]);             // same as g(char(*)[10]);
  int g(char(*)[20]);             // different from g(char(*)[10]);
  ```
- Parameter declarations that differ only in that one is a function type
  and the other is a pointer to the same function type are equivalent.
  That is, the function type is adjusted to become a pointer to function
  type ([[dcl.fct]]).
  ``` cpp
  void h(int());
  void h(int (*)());              // redeclaration of h(int())
  void h(int x()) { }             // definition of h(int())
  void h(int (*x)()) { }          // ill-formed: redefinition of h(int())
  ```
- Parameter declarations that differ only in the presence or absence of
  `const` and/or `volatile` are equivalent. That is, the `const` and
  `volatile` type-specifiers for each parameter type are ignored when
  determining which function is being declared, defined, or called.
  ``` cpp
  typedef const int cInt;

  int f (int);
  int f (const int);              // redeclaration of f(int)
  int f (int) { /* ... */ }      // definition of f(int)
  int f (cInt) { /* ... */ }     // error: redefinition of f(int)
  ```

  Only the `const` and `volatile` type-specifiers at the outermost level
  of the parameter type specification are ignored in this fashion;
  `const` and `volatile` type-specifiers buried within a parameter type
  specification are significant and can be used to distinguish
  overloaded function declarations.[^1] In particular, for any type `T`,
  “pointer to `T`,” “pointer to `const` `T`,” and “pointer to `volatile`
  `T`” are considered distinct parameter types, as are “reference to
  `T`,” “reference to `const` `T`,” and “reference to `volatile` `T`.”
- Two parameter declarations that differ only in their default arguments
  are equivalent. consider the following:
  ``` cpp
  void f (int i, int j);
  void f (int i, int j = 99);     // OK: redeclaration of f(int, int)
  void f (int i = 88, int j);     // OK: redeclaration of f(int, int)
  void f ();                      // OK: overloaded declaration of f

  void prog () {
      f (1, 2);                   // OK: call f(int, int)
      f (1);                      // OK: call f(int, int)
      f ();                       // Error: f(int, int) or f()?
  }
  ```

## Declaration matching <a id="over.dcl">[[over.dcl]]</a>

Two function declarations of the same name refer to the same function if
they are in the same scope and have equivalent parameter declarations (
[[over.load]]). A function member of a derived class is *not* in the
same scope as a function member of the same name in a base class.

``` cpp
struct B {
  int f(int);
};

struct D : B {
  int f(const char*);
};
```

Here `D::f(const char*)` hides `B::f(int)` rather than overloading it.

``` cpp
void h(D* pd) {
  pd->f(1);                     // error:
                                // D::f(const char*) hides B::f(int)
  pd->B::f(1);                  // OK
  pd->f("Ben");                 // OK, calls D::f
}
```

A locally declared function is not in the same scope as a function in a
containing scope.

``` cpp
void f(const char*);
void g() {
  extern void f(int);
  f("asdf");                    // error: f(int) hides f(const char*)
                                // so there is no f(const char*) in this scope
}

void caller () {
  extern void callee(int, int);
  {
    extern void callee(int);    // hides callee(int, int)
    callee(88, 99);             // error: only callee(int) in scope
  }
}
```

Different versions of an overloaded member function can be given
different access rules.

``` cpp
class buffer {
private:
    char* p;
    int size;
protected:
    buffer(int s, char* store) { size = s; p = store; }
public:
    buffer(int s) { p = new char[size = s]; }
};
```

## Overload resolution <a id="over.match">[[over.match]]</a>

Overload resolution is a mechanism for selecting the best function to
call given a list of expressions that are to be the arguments of the
call and a set of *candidate functions* that can be called based on the
context of the call. The selection criteria for the best function are
the number of arguments, how well the arguments match the
parameter-type-list of the candidate function, how well (for non-static
member functions) the object matches the implicit object parameter, and
certain other properties of the candidate function. The function
selected by overload resolution is not guaranteed to be appropriate for
the context. Other restrictions, such as the accessibility of the
function, can make its use in the calling context ill-formed.

Overload resolution selects the function to call in seven distinct
contexts within the language:

- invocation of a function named in the function call syntax (
  [[over.call.func]]);
- invocation of a function call operator, a pointer-to-function
  conversion function, a reference-to-pointer-to-function conversion
  function, or a reference-to-function conversion function on a class
  object named in the function call syntax ([[over.call.object]]);
- invocation of the operator referenced in an expression (
  [[over.match.oper]]);
- invocation of a constructor for direct-initialization ([[dcl.init]])
  of a class object ([[over.match.ctor]]);
- invocation of a user-defined conversion for copy-initialization (
  [[dcl.init]]) of a class object ([[over.match.copy]]);
- invocation of a conversion function for initialization of an object of
  a nonclass type from an expression of class type (
  [[over.match.conv]]); and
- invocation of a conversion function for conversion to a glvalue or
  class prvalue to which a reference ([[dcl.init.ref]]) will be
  directly bound ([[over.match.ref]]).

Each of these contexts defines the set of candidate functions and the
list of arguments in its own unique way. But, once the candidate
functions and argument lists have been identified, the selection of the
best function is the same in all cases:

- First, a subset of the candidate functions (those that have the proper
  number of arguments and meet certain other conditions) is selected to
  form a set of viable functions ([[over.match.viable]]).
- Then the best viable function is selected based on the implicit
  conversion sequences ([[over.best.ics]]) needed to match each
  argument to the corresponding parameter of each viable function.

If a best viable function exists and is unique, overload resolution
succeeds and produces it as the result. Otherwise overload resolution
fails and the invocation is ill-formed. When overload resolution
succeeds, and the best viable function is not accessible (Clause 
[[class.access]]) in the context in which it is used, the program is
ill-formed.

### Candidate functions and argument lists <a id="over.match.funcs">[[over.match.funcs]]</a>

The subclauses of  [[over.match.funcs]] describe the set of candidate
functions and the argument list submitted to overload resolution in each
of the seven contexts in which overload resolution is used. The source
transformations and constructions defined in these subclauses are only
for the purpose of describing the overload resolution process. An
implementation is not required to use such transformations and
constructions.

The set of candidate functions can contain both member and non-member
functions to be resolved against the same argument list. So that
argument and parameter lists are comparable within this heterogeneous
set, a member function is considered to have an extra parameter, called
the *implicit object parameter*, which represents the object for which
the member function has been called. For the purposes of overload
resolution, both static and non-static member functions have an implicit
object parameter, but constructors do not.

Similarly, when appropriate, the context can construct an argument list
that contains an *implied object argument* to denote the object to be
operated on. Since arguments and parameters are associated by position
within their respective lists, the convention is that the implicit
object parameter, if present, is always the first parameter and the
implied object argument, if present, is always the first argument.

For non-static member functions, the type of the implicit object
parameter is

- “lvalue reference to *cv* `X`” for functions declared without a
  *ref-qualifier* or with the `&` *ref-qualifier*
- “rvalue reference to *cv* `X`” for functions declared with the `&&`
  *ref-qualifier*

where `X` is the class of which the function is a member and *cv* is the
cv-qualification on the member function declaration. for a `const`
member function of class `X`, the extra parameter is assumed to have
type “reference to `const X`”. For conversion functions, the function is
considered to be a member of the class of the implied object argument
for the purpose of defining the type of the implicit object parameter.
For non-conversion functions introduced by a *using-declaration* into a
derived class, the function is considered to be a member of the derived
class for the purpose of defining the type of the implicit object
parameter. For static member functions, the implicit object parameter is
considered to match any object (since if the function is selected, the
object is discarded). No actual type is established for the implicit
object parameter of a static member function, and no attempt will be
made to determine a conversion sequence for that parameter (
[[over.match.best]]).

During overload resolution, the implied object argument is
indistinguishable from other arguments. The implicit object parameter,
however, retains its identity since conversions on the corresponding
argument shall obey these additional rules:

- no temporary object can be introduced to hold the argument for the
  implicit object parameter; and
- no user-defined conversions can be applied to achieve a type match
  with it.

For non-static member functions declared without a *ref-qualifier*, an
additional rule applies:

- even if the implicit object parameter is not `const`-qualified, an
  rvalue can be bound to the parameter as long as in all other respects
  the argument can be converted to the type of the implicit object
  parameter. The fact that such an argument is an rvalue does not affect
  the ranking of implicit conversion sequences ([[over.ics.rank]]).

Because other than in list-initialization only one user-defined
conversion is allowed in an implicit conversion sequence, special rules
apply when selecting the best user-defined conversion (
[[over.match.best]], [[over.best.ics]]).

``` cpp
class T {
public:
  T();
};

class C : T {
public:
  C(int);
};
T a = 1;            // ill-formed: T(C(1)) not tried
```

In each case where a candidate is a function template, candidate
function template specializations are generated using template argument
deduction ([[temp.over]], [[temp.deduct]]). Those candidates are then
handled as candidate functions in the usual way.[^2] A given name can
refer to one or more function templates and also to a set of overloaded
non-template functions. In such a case, the candidate functions
generated from each function template are combined with the set of
non-template candidate functions.

A defaulted move constructor or assignment operator ([[class.copy]])
that is defined as deleted is excluded from the set of candidate
functions in all contexts.

#### Function call syntax <a id="over.match.call">[[over.match.call]]</a>

In a function call ([[expr.call]])

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

if the *postfix-expression* denotes a set of overloaded functions and/or
function templates, overload resolution is applied as specified in
[[over.call.func]]. If the *postfix-expression* denotes an object of
class type, overload resolution is applied as specified in
[[over.call.object]].

If the *postfix-expression* denotes the address of a set of overloaded
functions and/or function templates, overload resolution is applied
using that set as described above. If the function selected by overload
resolution is a non-static member function, the program is ill-formed.
The resolution of the address of an overload set in other contexts is
described in [[over.over]].

##### Call to named function <a id="over.call.func">[[over.call.func]]</a>

Of interest in  [[over.call.func]] are only those function calls in
which the *postfix-expression* ultimately contains a name that denotes
one or more functions that might be called. Such a *postfix-expression*,
perhaps nested arbitrarily deep in parentheses, has one of the following
forms:

``` bnf
postfix-expression:
    postfix-expression '.' id-expression
    postfix-expression '->' id-expression
    primary-expression
```

These represent two syntactic subcategories of function calls: qualified
function calls and unqualified function calls.

In qualified function calls, the name to be resolved is an
*id-expression* and is preceded by an `->` or `.` operator. Since the
construct `A->B` is generally equivalent to `(*A).B`, the rest of
Clause  [[over]] assumes, without loss of generality, that all member
function calls have been normalized to the form that uses an object and
the `.` operator. Furthermore, Clause  [[over]] assumes that the
*postfix-expression* that is the left operand of the `.` operator has
type “*cv* `T`” where `T` denotes a class[^3]. Under this assumption,
the *id-expression* in the call is looked up as a member function of `T`
following the rules for looking up names in classes (
[[class.member.lookup]]). The function declarations found by that lookup
constitute the set of candidate functions. The argument list is the
*expression-list* in the call augmented by the addition of the left
operand of the `.` operator in the normalized member function call as
the implied object argument ([[over.match.funcs]]).

In unqualified function calls, the name is not qualified by an `->` or
`.` operator and has the more general form of a *primary-expression*.
The name is looked up in the context of the function call following the
normal rules for name lookup in function calls ([[basic.lookup]]). The
function declarations found by that lookup constitute the set of
candidate functions. Because of the rules for name lookup, the set of
candidate functions consists (1) entirely of non-member functions or (2)
entirely of member functions of some class `T`. In case (1), the
argument list is the same as the *expression-list* in the call. In case
(2), the argument list is the *expression-list* in the call augmented by
the addition of an implied object argument as in a qualified function
call. If the keyword `this` ([[class.this]]) is in scope and refers to
class `T`, or a derived class of `T`, then the implied object argument
is `(*this)`. If the keyword `this` is not in scope or refers to another
class, then a contrived object of type `T` becomes the implied object
argument[^4]. If the argument list is augmented by a contrived object
and overload resolution selects one of the non-static member functions
of `T`, the call is ill-formed.

##### Call to object of class type <a id="over.call.object">[[over.call.object]]</a>

If the *primary-expression* `E` in the function call syntax evaluates to
a class object of type “*cv* `T`”, then the set of candidate functions
includes at least the function call operators of `T`. The function call
operators of `T` are obtained by ordinary lookup of the name
`operator()` in the context of `(E).operator()`.

In addition, for each non-explicit conversion function declared in `T`
of the form

``` bnf
'operator' conversion-type-id '( )' cv-qualifier ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ ';'
```

where *cv-qualifier* is the same cv-qualification as, or a greater
cv-qualification than, *cv*, and where *conversion-type-id* denotes the
type “pointer to function of (`P1`,...,`Pn)` returning `R`”, or the type
“reference to pointer to function of (`P1`,...,`Pn)` returning `R`”, or
the type “reference to function of (`P1`,...,`Pn)` returning `R`”, a
*surrogate call function* with the unique name *call-function* and
having the form

``` bnf
'R' call-function '(' conversion-type-id 'F, P1 a1, ... ,Pn an)' '{ return F (a1,... ,an); }'
```

is also considered as a candidate function. Similarly, surrogate call
functions are added to the set of candidate functions for each
non-explicit conversion function declared in a base class of `T`
provided the function is not hidden within `T` by another intervening
declaration[^5].

If such a surrogate call function is selected by overload resolution,
the corresponding conversion function will be called to convert `E` to
the appropriate function pointer or reference, and the function will
then be invoked with the arguments of the call. If the conversion
function cannot be called (e.g., because of an ambiguity), the program
is ill-formed.

The argument list submitted to overload resolution consists of the
argument expressions present in the function call syntax preceded by the
implied object argument `(E)`. When comparing the call against the
function call operators, the implied object argument is compared against
the implicit object parameter of the function call operator. When
comparing the call against a surrogate call function, the implied object
argument is compared against the first parameter of the surrogate call
function. The conversion function from which the surrogate call function
was derived will be used in the conversion sequence for that parameter
since it converts the implied object argument to the appropriate
function pointer or reference required by that first parameter.

``` cpp
int f1(int);
int f2(float);
typedef int (*fp1)(int);
typedef int (*fp2)(float);
struct A {
  operator fp1() { return f1; }
  operator fp2() { return f2; }
} a;
int i = a(1);       // calls f1 via pointer returned from
                    // conversion function
```

#### Operators in expressions <a id="over.match.oper">[[over.match.oper]]</a>

If no operand of an operator in an expression has a type that is a class
or an enumeration, the operator is assumed to be a built-in operator and
interpreted according to Clause  [[expr]]. Because `.`, `.*`, and `::`
cannot be overloaded, these operators are always built-in operators
interpreted according to Clause  [[expr]]. `?:` cannot be overloaded,
but the rules in this subclause are used to determine the conversions to
be applied to the second and third operands when they have class or
enumeration type ([[expr.cond]]).

``` cpp
struct String {
  String (const String&);
  String (const char*);
  operator const char* ();
};
String operator + (const String&, const String&);

void f(void) {
 const char* p= "one" + "two";  // ill-formed because neither
                                // operand has class or enumeration type
 int I = 1 + 1;                 // Always evaluates to 2 even if
                                // class or enumeration types exist that
                                // would perform the operation.
}
```

If either operand has a type that is a class or an enumeration, a
user-defined operator function might be declared that implements this
operator or a user-defined conversion can be necessary to convert the
operand to a type that is appropriate for a built-in operator. In this
case, overload resolution is used to determine which operator function
or built-in operator is to be invoked to implement the operator.
Therefore, the operator notation is first transformed to the equivalent
function-call notation as summarized in Table  [[tab:over.rel.op.func]]
(where `@` denotes one of the operators covered in the specified
subclause).

**Table: Relationship between operator and function call notation** <a id="tab:over.rel.op.func">[tab:over.rel.op.func]</a>

| Subclause    | Expression | As member function | As non-member function |
| ------------ | ---------- | ------------------ | ---------------------- |
| (a)          |
| (a, b)       |
| [[over.ass]] | a=b        | (a).operator= (b)  |                        |
| [[over.sub]] | a[b]       | (a).operator[](b)  |                        |
| [[over.ref]] | a->        | (a).operator-> ( ) |                        |
| (a, 0)       |


For a unary operator `@` with an operand of a type whose cv-unqualified
version is `T1`, and for a binary operator `@` with a left operand of a
type whose cv-unqualified version is `T1` and a right operand of a type
whose cv-unqualified version is `T2`, three sets of candidate functions,
designated *member candidates*, *non-member candidates* and *built-in
candidates*, are constructed as follows:

- If `T1` is a complete class type or a class currently being defined,
  the set of member candidates is the result of the qualified lookup of
  `T1::operator@` ([[over.call.func]]); otherwise, the set of member
  candidates is empty.
- The set of non-member candidates is the result of the unqualified
  lookup of `operator@` in the context of the expression according to
  the usual rules for name lookup in unqualified function calls (
  [[basic.lookup.argdep]]) except that all member functions are ignored.
  However, if no operand has a class type, only those non-member
  functions in the lookup set that have a first parameter of type `T1`
  or “reference to (possibly cv-qualified) `T1`”, when `T1` is an
  enumeration type, or (if there is a right operand) a second parameter
  of type `T2` or “reference to (possibly cv-qualified) `T2`”, when `T2`
  is an enumeration type, are candidate functions.
- For the operator `,`, the unary operator `&`, or the operator `->`,
  the built-in candidates set is empty. For all other operators, the
  built-in candidates include all of the candidate operator functions
  defined in  [[over.built]] that, compared to the given operator,
  - have the same operator name, and
  - accept the same number of operands, and
  - accept operand types to which the given operand or operands can be
    converted according to [[over.best.ics]], and
  - do not have the same parameter-type-list as any non-member candidate
    that is not a function template specialization.

For the built-in assignment operators, conversions of the left operand
are restricted as follows:

- no temporaries are introduced to hold the left operand, and
- no user-defined conversions are applied to the left operand to achieve
  a type match with the left-most parameter of a built-in candidate.

For all other operators, no such restrictions apply.

The set of candidate functions for overload resolution is the union of
the member candidates, the non-member candidates, and the built-in
candidates. The argument list contains all of the operands of the
operator. The best function from the set of candidate functions is
selected according to  [[over.match.viable]] and 
[[over.match.best]].[^6]

``` cpp
struct A {
  operator int();
};
A operator+(const A&, const A&);
void m() {
  A a, b;
  a + b;            // operator+(a,b) chosen over int(a) + int(b)
}
```

If a built-in candidate is selected by overload resolution, the operands
of class type are converted to the types of the corresponding parameters
of the selected operation function, except that the second standard
conversion sequence of a user-defined conversion sequence (
[[over.ics.user]]) is not applied. Then the operator is treated as the
corresponding built-in operator and interpreted according to Clause 
[[expr]].

``` cpp
struct X {
  operator double();
};

struct Y {
  operator int*();
};

int *a = Y() + 100.0;      // error: pointer arithmetic requires integral operand
int *b = Y() + X();        // error: pointer arithmetic requires integral operand
```

The second operand of operator `->` is ignored in selecting an
`operator->` function, and is not an argument when the `operator->`
function is called. When `operator->` returns, the operator `->` is
applied to the value returned, with the original second operand.[^7]

If the operator is the operator `,`, the unary operator `&`, or the
operator `->`, and there are no viable functions, then the operator is
assumed to be the built-in operator and interpreted according to Clause 
[[expr]].

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
  a + a;                        // OK: calls global operator+
}
```

#### Initialization by constructor <a id="over.match.ctor">[[over.match.ctor]]</a>

When objects of class type are direct-initialized ([[dcl.init]]), or
copy-initialized from an expression of the same or a derived class
type ([[dcl.init]]), overload resolution selects the constructor. For
direct-initialization, the candidate functions are all the constructors
of the class of the object being initialized. For copy-initialization,
the candidate functions are all the converting constructors (
[[class.conv.ctor]]) of that class. The argument list is the
*expression-list* or *assignment-expression* of the *initializer*.

#### Copy-initialization of class by user-defined conversion <a id="over.match.copy">[[over.match.copy]]</a>

Under the conditions specified in  [[dcl.init]], as part of a
copy-initialization of an object of class type, a user-defined
conversion can be invoked to convert an initializer expression to the
type of the object being initialized. Overload resolution is used to
select the user-defined conversion to be invoked. The conversion
performed for indirect binding to a reference to a possibly cv-qualified
class type is determined in terms of a corresponding non-reference
copy-initialization. Assuming that “*cv1* `T`” is the type of the object
being initialized, with `T` a class type, the candidate functions are
selected as follows:

- The converting constructors ([[class.conv.ctor]]) of `T` are
  candidate functions.
- When the type of the initializer expression is a class type “*cv*
  `S`”, the non-explicit conversion functions of `S` and its base
  classes are considered. When initializing a temporary to be bound to
  the first parameter of a constructor that takes a reference to
  possibly cv-qualified `T` as its first argument, called with a single
  argument in the context of direct-initialization of an object of type
  “*cv2* `T`”, explicit conversion functions are also considered. Those
  that are not hidden within `S` and yield a type whose cv-unqualified
  version is the same type as `T` or is a derived class thereof are
  candidate functions. Conversion functions that return “reference to
  `X`” return lvalues or xvalues, depending on the type of reference, of
  type `X` and are therefore considered to yield `X` for this process of
  selecting candidate functions.

In both cases, the argument list has one argument, which is the
initializer expression. This argument will be compared against the first
parameter of the constructors and against the implicit object parameter
of the conversion functions.

#### Initialization by conversion function <a id="over.match.conv">[[over.match.conv]]</a>

Under the conditions specified in  [[dcl.init]], as part of an
initialization of an object of nonclass type, a conversion function can
be invoked to convert an initializer expression of class type to the
type of the object being initialized. Overload resolution is used to
select the conversion function to be invoked. Assuming that “*cv1* `T`”
is the type of the object being initialized, and “*cv* `S`” is the type
of the initializer expression, with `S` a class type, the candidate
functions are selected as follows:

- The conversion functions of `S` and its base classes are considered.
  Those non-explicit conversion functions that are not hidden within `S`
  and yield type `T` or a type that can be converted to type `T` via a
  standard conversion sequence ([[over.ics.scs]]) are candidate
  functions. For direct-initialization, those explicit conversion
  functions that are not hidden within `S` and yield type `T` or a type
  that can be converted to type `T` with a qualification conversion (
  [[conv.qual]]) are also candidate functions. Conversion functions that
  return a cv-qualified type are considered to yield the cv-unqualified
  version of that type for this process of selecting candidate
  functions. Conversion functions that return “reference to *cv2* `X`”
  return lvalues or xvalues, depending on the type of reference, of type
  “*cv2* `X`” and are therefore considered to yield `X` for this process
  of selecting candidate functions.

The argument list has one argument, which is the initializer expression.
This argument will be compared against the implicit object parameter of
the conversion functions.

#### Initialization by conversion function for direct reference binding <a id="over.match.ref">[[over.match.ref]]</a>

Under the conditions specified in  [[dcl.init.ref]], a reference can be
bound directly to a glvalue or class prvalue that is the result of
applying a conversion function to an initializer expression. Overload
resolution is used to select the conversion function to be invoked.
Assuming that “*cv1* `T`” is the underlying type of the reference being
initialized, and “*cv* `S`” is the type of the initializer expression,
with `S` a class type, the candidate functions are selected as follows:

- The conversion functions of `S` and its base classes are considered.
  Those non-explicit conversion functions that are not hidden within `S`
  and yield type “lvalue reference to *cv2* `T2`” (when initializing an
  lvalue reference or an rvalue reference to function) or “ `T2`” or
  “rvalue reference to `T2`” (when initializing an rvalue reference or
  an lvalue reference to function), where “*cv1* `T`” is
  reference-compatible ([[dcl.init.ref]]) with “*cv2* `T2`”, are
  candidate functions. For direct-initialization, those explicit
  conversion functions that are not hidden within `S` and yield type
  “lvalue reference to *cv2* `T2`” or “*cv2* `T2`” or “rvalue reference
  to *cv2* `T2`,” respectively, where `T2` is the same type as `T` or
  can be converted to type `T` with a qualification conversion (
  [[conv.qual]]), are also candidate functions.

The argument list has one argument, which is the initializer expression.
This argument will be compared against the implicit object parameter of
the conversion functions.

#### Initialization by list-initialization <a id="over.match.list">[[over.match.list]]</a>

When objects of non-aggregate class type `T` are list-initialized (
[[dcl.init.list]]), overload resolution selects the constructor in two
phases:

- Initially, the candidate functions are the initializer-list
  constructors ([[dcl.init.list]]) of the class `T` and the argument
  list consists of the initializer list as a single argument.
- If no viable initializer-list constructor is found, overload
  resolution is performed again, where the candidate functions are all
  the constructors of the class `T` and the argument list consists of
  the elements of the initializer list.

If the initializer list has no elements and `T` has a default
constructor, the first phase is omitted. In copy-list-initialization, if
an `explicit` constructor is chosen, the initialization is ill-formed.
This differs from other situations ([[over.match.ctor]], 
[[over.match.copy]]), where only converting constructors are considered
for copy-initialization. This restriction only applies if this
initialization is part of the final result of overload resolution.

### Viable functions <a id="over.match.viable">[[over.match.viable]]</a>

From the set of candidate functions constructed for a given context (
[[over.match.funcs]]), a set of viable functions is chosen, from which
the best function will be selected by comparing argument conversion
sequences for the best fit ([[over.match.best]]). The selection of
viable functions considers relationships between arguments and function
parameters other than the ranking of conversion sequences.

First, to be a viable function, a candidate function shall have enough
parameters to agree in number with the arguments in the list.

- If there are *m* arguments in the list, all candidate functions having
  exactly *m* parameters are viable.
- A candidate function having fewer than *m* parameters is viable only
  if it has an ellipsis in its parameter list ([[dcl.fct]]). For the
  purposes of overload resolution, any argument for which there is no
  corresponding parameter is considered to “match the ellipsis” (
  [[over.ics.ellipsis]]) .
- A candidate function having more than *m* parameters is viable only if
  the *(m+1)*-st parameter has a default argument (
  [[dcl.fct.default]]).[^8] For the purposes of overload resolution, the
  parameter list is truncated on the right, so that there are exactly
  *m* parameters.

Second, for `F` to be a viable function, there shall exist for each
argument an *implicit conversion sequence* ([[over.best.ics]]) that
converts that argument to the corresponding parameter of `F`. If the
parameter has reference type, the implicit conversion sequence includes
the operation of binding the reference, and the fact that an lvalue
reference to non-`const` cannot be bound to an rvalue and that an rvalue
reference cannot be bound to an lvalue can affect the viability of the
function (see  [[over.ics.ref]]).

### Best viable function <a id="over.match.best">[[over.match.best]]</a>

Define ICS*i*(`F`) as follows:

- if `F` is a static member function, ICS*1*(`F`) is defined such that
  ICS*1*(`F`) is neither better nor worse than ICS*1*(`G`) for any
  function `G`, and, symmetrically, ICS*1*(`G`) is neither better nor
  worse than ICS*1*(`F`)[^9]; otherwise,
- let ICS*i*(`F`) denote the implicit conversion sequence that converts
  the *i*-th argument in the list to the type of the *i*-th parameter of
  viable function `F`. [[over.best.ics]] defines the implicit conversion
  sequences and [[over.ics.rank]] defines what it means for one implicit
  conversion sequence to be a better conversion sequence or worse
  conversion sequence than another.

Given these definitions, a viable function `F1` is defined to be a
*better* function than another viable function `F2` if for all arguments
*i*, ICS*i*(`F1`) is not a worse conversion sequence than ICS*i*(`F2`),
and then

- for some argument *j*, ICS*j*(`F1`) is a better conversion sequence
  than ICS*j*(`F2`), or, if not that,
- the context is an initialization by user-defined conversion (see 
  [[dcl.init]], [[over.match.conv]], and  [[over.match.ref]]) and the
  standard conversion sequence from the return type of `F1` to the
  destination type (i.e., the type of the entity being initialized) is a
  better conversion sequence than the standard conversion sequence from
  the return type of `F2` to the destination type.
  ``` cpp
  struct A {
    A();
    operator int();
    operator double();
  } a;
  int i = a;                      // a.operator int() followed by no conversion
                                  // is better than a.operator double() followed by
                                  // a conversion to int
  float x = a;                    // ambiguous: both possibilities require conversions,
                                  // and neither is better than the other
  ```

  or, if not that,
- the context is an initialization by conversion function for direct
  reference binding ([[over.match.ref]]) of a reference to function
  type, the return type of `F1` is the same kind of reference (i.e.
  lvalue or rvalue) as the reference being initialized, and the return
  type of `F2` is not
  ``` cpp
  template <class T> struct A {
    operator T&();        // #1
    operator T&&();       // #2
  };
  typedef int Fn();
  A<Fn> a;
  Fn& lf = a;             // calls #1
  Fn&& rf = a;            // calls #2
  ```

  or, if not that,
- `F1` is not a function template specialization and `F2` is a function
  template specialization, or, if not that,
- `F1` and `F2` are function template specializations, and the function
  template for `F1` is more specialized than the template for `F2`
  according to the partial ordering rules described in 
  [[temp.func.order]].

If there is exactly one viable function that is a better function than
all other viable functions, then it is the one selected by overload
resolution; otherwise the call is ill-formed[^10].

``` cpp
void Fcn(const int*,  short);
void Fcn(int*, int);

int i;
short s = 0;

void f() {
  Fcn(&i, s);                   // is ambiguous because
                                // &i → int* is better than &i → const int*
                                // but s → short is also better than s → int

  Fcn(&i, 1L);                  // calls Fcn(int*, int), because
                                // &i → int* is better than &i → const int*
                                // and 1L → short and 1L → int are indistinguishable

  Fcn(&i,'c');                  // calls Fcn(int*, int), because
                                // &i → int* is better than &i → const int*
                                // and c → int is better than c → short
}
```

If the best viable function resolves to a function for which multiple
declarations were found, and if at least two of these declarations — or
the declarations they refer to in the case of *using-declaration*s —
specify a default argument that made the function viable, the program is
ill-formed.

``` cpp
namespace A {
  extern "C" void f(int = 5);
}
namespace B {
  extern "C" void f(int = 5);
}

using A::f;
using B::f;

void use() {
  f(3);                         // OK, default argument was not used for viability
  f();                          // Error: found default argument twice
}
```

#### Implicit conversion sequences <a id="over.best.ics">[[over.best.ics]]</a>

An *implicit conversion sequence* is a sequence of conversions used to
convert an argument in a function call to the type of the corresponding
parameter of the function being called. The sequence of conversions is
an implicit conversion as defined in Clause  [[conv]], which means it is
governed by the rules for initialization of an object or reference by a
single expression ([[dcl.init]], [[dcl.init.ref]]).

Implicit conversion sequences are concerned only with the type,
cv-qualification, and value category of the argument and how these are
converted to match the corresponding properties of the parameter. Other
properties, such as the lifetime, storage class, alignment, or
accessibility of the argument and whether or not the argument is a
bit-field are ignored. So, although an implicit conversion sequence can
be defined for a given argument-parameter pair, the conversion from the
argument to the parameter might still be ill-formed in the final
analysis.

A well-formed implicit conversion sequence is one of the following
forms:

- a *standard conversion sequence* ([[over.ics.scs]]),
- a *user-defined conversion sequence* ([[over.ics.user]]), or
- an *ellipsis conversion sequence* ([[over.ics.ellipsis]]).

However, if the target is

- the first parameter of a constructor or
- the implicit object parameter of a user-defined conversion function

and the constructor or user-defined conversion function is a candidate
by

-  [[over.match.ctor]], when the argument is the temporary in the second
  step of a class copy-initialization,
-  [[over.match.copy]], [[over.match.conv]], or [[over.match.ref]] (in
  all cases), or
- the second phase of [[over.match.list]] when the initializer list has
  exactly one element, and the target is the first parameter of a
  constructor of class `X`, and the conversion is to `X` or reference to
  (possibly cv-qualified) `X`,

user-defined conversion sequences are not considered. These rules
prevent more than one user-defined conversion from being applied during
overload resolution, thereby avoiding infinite recursion.

``` cpp
struct Y { Y(int); };
  struct A { operator int(); };
  Y y1 = A();  // error: A::operator int() is not a candidate

  struct X { };
  struct B { operator X(); };
  B b;
  X x({b});    // error: B::operator X() is not a candidate
```

For the case where the parameter type is a reference, see 
[[over.ics.ref]].

When the parameter type is not a reference, the implicit conversion
sequence models a copy-initialization of the parameter from the argument
expression. The implicit conversion sequence is the one required to
convert the argument expression to a prvalue of the type of the
parameter. When the parameter has a class type, this is a conceptual
conversion defined for the purposes of Clause  [[over]]; the actual
initialization is defined in terms of constructors and is not a
conversion. Any difference in top-level cv-qualification is subsumed by
the initialization itself and does not constitute a conversion. a
parameter of type `A` can be initialized from an argument of type
`const A`. The implicit conversion sequence for that case is the
identity sequence; it contains no “conversion” from `const A` to `A`.
When the parameter has a class type and the argument expression has the
same type, the implicit conversion sequence is an identity conversion.
When the parameter has a class type and the argument expression has a
derived class type, the implicit conversion sequence is a
derived-to-base Conversion from the derived class to the base class.
There is no such standard conversion; this derived-to-base Conversion
exists only in the description of implicit conversion sequences. A
derived-to-base Conversion has Conversion rank ([[over.ics.scs]]).

In all contexts, when converting to the implicit object parameter or
when converting to the left operand of an assignment operation only
standard conversion sequences that create no temporary object for the
result are allowed.

If no conversions are required to match an argument to a parameter type,
the implicit conversion sequence is the standard conversion sequence
consisting of the identity conversion ([[over.ics.scs]]).

If no sequence of conversions can be found to convert an argument to a
parameter type or the conversion is otherwise ill-formed, an implicit
conversion sequence cannot be formed.

If several different sequences of conversions exist that each convert
the argument to the parameter type, the implicit conversion sequence
associated with the parameter is defined to be the unique conversion
sequence designated the *ambiguous conversion sequence*. For the purpose
of ranking implicit conversion sequences as described in 
[[over.ics.rank]], the ambiguous conversion sequence is treated as a
user-defined sequence that is indistinguishable from any other
user-defined conversion sequence[^11]. If a function that uses the
ambiguous conversion sequence is selected as the best viable function,
the call will be ill-formed because the conversion of one of the
arguments in the call is ambiguous.

The three forms of implicit conversion sequences mentioned above are
defined in the following subclauses.

##### Standard conversion sequences <a id="over.ics.scs">[[over.ics.scs]]</a>

Table  [[tab:over.conversions]] summarizes the conversions defined in
Clause  [[conv]] and partitions them into four disjoint categories:
Lvalue Transformation, Qualification Adjustment, Promotion, and
Conversion. These categories are orthogonal with respect to value
category, cv-qualification, and data representation: the Lvalue
Transformations do not change the cv-qualification or data
representation of the type; the Qualification Adjustments do not change
the value category or data representation of the type; and the
Promotions and Conversions do not change the value category or
cv-qualification of the type.

As described in Clause  [[conv]], a standard conversion sequence is
either the Identity conversion by itself (that is, no conversion) or
consists of one to three conversions from the other four categories. At
most one conversion from each category is allowed in a single standard
conversion sequence. If there are two or more conversions in the
sequence, the conversions are applied in the canonical order: **Lvalue
Transformation**, **Promotion** or **Conversion**, **Qualification
Adjustment**.

Each conversion in Table  [[tab:over.conversions]] also has an
associated rank (Exact Match, Promotion, or Conversion). These are used
to rank standard conversion sequences ([[over.ics.rank]]). The rank of
a conversion sequence is determined by considering the rank of each
conversion in the sequence and the rank of any reference binding (
[[over.ics.ref]]). If any of those has Conversion rank, the sequence has
Conversion rank; otherwise, if any of those has Promotion rank, the
sequence has Promotion rank; otherwise, the sequence has Exact Match
rank.

**Table: Conversions** <a id="tab:over.conversions">[tab:over.conversions]</a>

| Conversion              | Category | Rank | Subclause         |
| ----------------------- | -------- | ---- | ----------------- |
| No conversions required | Identity |      |                   |
| Integral promotions     |          |      | [[conv.prom]]     |
| Integral conversions    |          |      | [[conv.integral]] |


##### User-defined conversion sequences <a id="over.ics.user">[[over.ics.user]]</a>

A user-defined conversion sequence consists of an initial standard
conversion sequence followed by a user-defined conversion (
[[class.conv]]) followed by a second standard conversion sequence. If
the user-defined conversion is specified by a constructor (
[[class.conv.ctor]]), the initial standard conversion sequence converts
the source type to the type required by the argument of the constructor.
If the user-defined conversion is specified by a conversion function (
[[class.conv.fct]]), the initial standard conversion sequence converts
the source type to the implicit object parameter of the conversion
function.

The second standard conversion sequence converts the result of the
user-defined conversion to the target type for the sequence. Since an
implicit conversion sequence is an initialization, the special rules for
initialization by user-defined conversion apply when selecting the best
user-defined conversion for a user-defined conversion sequence (see 
[[over.match.best]] and  [[over.best.ics]]).

If the user-defined conversion is specified by a specialization of a
conversion function template, the second standard conversion sequence
shall have exact match rank.

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

When a parameter of reference type binds directly ([[dcl.init.ref]]) to
an argument expression, the implicit conversion sequence is the identity
conversion, unless the argument expression has a type that is a derived
class of the parameter type, in which case the implicit conversion
sequence is a derived-to-base Conversion ([[over.best.ics]]).

``` cpp
struct A {};
struct B : public A {} b;
int f(A&);
int f(B&);
int i = f(b);                   // calls f(B&), an exact match, rather than
                                // f(A&), a conversion
```

If the parameter binds directly to the result of applying a conversion
function to the argument expression, the implicit conversion sequence is
a user-defined conversion sequence ([[over.ics.user]]), with the second
standard conversion sequence either an identity conversion or, if the
conversion function returns an entity of a type that is a derived class
of the parameter type, a derived-to-base Conversion.

When a parameter of reference type is not bound directly to an argument
expression, the conversion sequence is the one required to convert the
argument expression to the underlying type of the reference according
to  [[over.best.ics]]. Conceptually, this conversion sequence
corresponds to copy-initializing a temporary of the underlying type with
the argument expression. Any difference in top-level cv-qualification is
subsumed by the initialization itself and does not constitute a
conversion.

Except for an implicit object parameter, for which see 
[[over.match.funcs]], a standard conversion sequence cannot be formed if
it requires binding an lvalue reference other than a reference to a
non-volatile `const` type to an rvalue or binding an rvalue reference to
an lvalue other than a function lvalue. This means, for example, that a
candidate function cannot be a viable function if it has a non-`const`
lvalue reference parameter (other than the implicit object parameter)
and the corresponding argument is a temporary or would require one to be
created to initialize the lvalue reference (see  [[dcl.init.ref]]).

Other restrictions on binding a reference to a particular argument that
are not based on the types of the reference and the argument do not
affect the formation of a standard conversion sequence, however. a
function with an “lvalue reference to `int`” parameter can be a viable
candidate even if the corresponding argument is an `int` bit-field. The
formation of implicit conversion sequences treats the `int` bit-field as
an `int` lvalue and finds an exact match with the parameter. If the
function is selected by overload resolution, the call will nonetheless
be ill-formed because of the prohibition on binding a non-`const` lvalue
reference to a bit-field ([[dcl.init.ref]]).

##### List-initialization sequence <a id="over.ics.list">[[over.ics.list]]</a>

When an argument is an initializer list ([[dcl.init.list]]), it is not
an expression and special rules apply for converting it to a parameter
type.

If the parameter type is `std::initializer_list<X>` and all the elements
of the initializer list can be implicitly converted to `X`, the implicit
conversion sequence is the worst conversion necessary to convert an
element of the list to `X`, or if the initializer list has no elements,
the identity conversion. This conversion can be a user-defined
conversion even in the context of a call to an initializer-list
constructor.

``` cpp
void f(std::initializer_list<int>);
f( {} );                    // OK: f(initializer_list<int>) identity conversion
f( {1,2,3} );               // OK: f(initializer_list<int>) identity conversion
f( {'a','b'} );             // OK: f(initializer_list<int>) integral promotion
f( {1.0} );                 // error: narrowing

struct A {
  A(std::initializer_list<double>);           // #1
  A(std::initializer_list<complex<double>>);  // #2
  A(std::initializer_list<std::string>);      // #3
};
A a{ 1.0,2.0 };             // OK, uses #1

void g(A);
g({ "foo", "bar" });        // OK, uses #3

typedef int IA[3];
void h(const IA&);
h({ 1, 2, 3 });             // OK: identity conversion
```

Otherwise, if the parameter type is “array of `N` `X`”[^12], if the
initializer list has exactly `N` elements or if it has fewer than `N`
elements and `X` is default-constructible, and if all the elements of
the initializer list can be implicitly converted to `X`, the implicit
conversion sequence is the worst conversion necessary to convert an
element of the list to `X`.

Otherwise, if the parameter is a non-aggregate class `X` and overload
resolution per  [[over.match.list]] chooses a single best constructor of
`X` to perform the initialization of an object of type `X` from the
argument initializer list, the implicit conversion sequence is a
user-defined conversion sequence with the second standard conversion
sequence an identity conversion. If multiple constructors are viable but
none is better than the others, the implicit conversion sequence is the
ambiguous conversion sequence. User-defined conversions are allowed for
conversion of the initializer list elements to the constructor parameter
types except as noted in  [[over.best.ics]].

``` cpp
struct A {
  A(std::initializer_list<int>);
};
void f(A);
f( {'a', 'b'} );            // OK: f(A(std::initializer_list<int>)) user-defined conversion

struct B {
  B(int, double);
};
void g(B);
g( {'a', 'b'} );            // OK: g(B(int,double)) user-defined conversion
g( {1.0, 1.0} );            // error: narrowing

void f(B);
f( {'a', 'b'} );            // error: ambiguous f(A) or f(B)

struct C {
  C(std::string);
};
void h(C);
h({"foo"});                 // OK: h(C(std::string("foo")))

struct D {
  D(A, C);
};
void i(D);
i({ {1,2}, {"bar"} });      // OK: i(D(A(std::initializer_list<int>{1,2\),C(std::string("bar"))))}
```

Otherwise, if the parameter has an aggregate type which can be
initialized from the initializer list according to the rules for
aggregate initialization ([[dcl.init.aggr]]), the implicit conversion
sequence is a user-defined conversion sequence with the second standard
conversion sequence an identity conversion.

``` cpp
struct A {
  int m1;
  double m2;
};

void f(A);
f( {'a', 'b'} );            // OK: f(A(int,double)) user-defined conversion
f( {1.0} );                 // error: narrowing
```

Otherwise, if the parameter is a reference, see  [[over.ics.ref]]. The
rules in this section will apply for initializing the underlying
temporary for the reference.

``` cpp
struct A {
  int m1;
  double m2;
};

void f(const A&);
f( {'a', 'b'} );            // OK: f(A(int,double)) user-defined conversion
f( {1.0} );                 // error: narrowing

void g(const double &);
g({1});                     // same conversion as int to double
```

Otherwise, if the parameter type is not a class:

- if the initializer list has one element, the implicit conversion
  sequence is the one required to convert the element to the parameter
  type;
  ``` cpp
  void f(int);
  f( {'a'} );                 // OK: same conversion as char to int
  f( {1.0} );                 // error: narrowing
  ```
- if the initializer list has no elements, the implicit conversion
  sequence is the identity conversion.
  ``` cpp
  void f(int);
  f( { } );                   // OK: identity conversion
  ```

In all cases other than those enumerated above, no conversion is
possible.

#### Ranking implicit conversion sequences <a id="over.ics.rank">[[over.ics.rank]]</a>

[[over.ics.rank]] defines a partial ordering of implicit conversion
sequences based on the relationships *better conversion sequence* and
*better conversion*. If an implicit conversion sequence S1 is defined by
these rules to be a better conversion sequence than S2, then it is also
the case that S2 is a *worse conversion sequence* than S1. If conversion
sequence S1 is neither better than nor worse than conversion sequence
S2, S1 and S2 are said to be *indistinguishable conversion sequences*.

When comparing the basic forms of implicit conversion sequences (as
defined in  [[over.best.ics]])

- a standard conversion sequence ([[over.ics.scs]]) is a better
  conversion sequence than a user-defined conversion sequence or an
  ellipsis conversion sequence, and
- a user-defined conversion sequence ([[over.ics.user]]) is a better
  conversion sequence than an ellipsis conversion sequence (
  [[over.ics.ellipsis]]).

Two implicit conversion sequences of the same form are indistinguishable
conversion sequences unless one of the following rules applies:

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
  - `S1` and `S2` are reference bindings ([[dcl.init.ref]]) and neither
    refers to an implicit object parameter of a non-static member
    function declared without a *ref-qualifier*, and `S1` binds an
    rvalue reference to an rvalue and `S2` binds an lvalue reference.
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
    A() << 1;                       // calls A::operator\shl(int)
    A() << 'c';                     // calls operator\shl(A&&, char)
    A a;
    a << 1;                         // calls A::operator\shl(int)
    a << 'c';                       // calls A::operator\shl(int)
    A().p();                        // calls A::p()&&
    a.p();                          // calls A::p()&
    ```

    or, if not that,
  - `S1` and `S2` are reference bindings ([[dcl.init.ref]]) and `S1`
    binds an lvalue reference to a function lvalue and `S2` binds an
    rvalue reference to a function lvalue.
    ``` cpp
    int f(void(&)());               // #1
    int f(void(&&)());              // #2
    void g();
    int i1 = f(g);                  // calls #1
    ```

    or, if not that,
  - `S1`
    and `S2` differ only in their qualification conversion and yield
    similar types `T1` and `T2` ([[conv.qual]]), respectively, and the
    cv-qualification signature of type `T1` is a proper subset of the
    cv-qualification signature of type `T2`.
    ``` cpp
    int f(const volatile int *);
    int f(const int *);
    int i;
    int j = f(&i);                  // calls f(const int*)
    ```

    or, if not that,
  - `S1`
    and `S2` are reference bindings ([[dcl.init.ref]]), and the types
    to which the references refer are the same type except for top-level
    cv-qualifiers, and the type to which the reference initialized by
    `S2` refers is more cv-qualified than the type to which the
    reference initialized by `S1` refers.
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
    ```
- User-defined conversion sequence `U1` is a better conversion sequence
  than another user-defined conversion sequence `U2` if they contain the
  same user-defined conversion function or constructor or they
  initialize the same class in an aggregate initialization and in either
  case the second standard conversion sequence of `U1` is better than
  the second standard conversion sequence of `U2`.
  ``` cpp
  struct A {
    operator short();
  } a;
  int f(int);
  int f(float);
  int i = f(a);                   // calls f(int), because short → int is
                                  // better than short → float.
  ```
- List-initialization sequence `L1` is a better conversion sequence than
  list-initialization sequence `L2` if
  - `L1` converts to `std::initializer_list<X>` for some `X` and `L2`
    does not, or, if not that,
  - `L1` converts to type “array of `N1` `T`”, `L2` converts to type
    “array of `N2` `T`”, and `N1` is smaller than `N2`.

Standard conversion sequences are ordered by their ranks: an Exact Match
is a better conversion than a Promotion, which is a better conversion
than a Conversion. Two conversion sequences with the same rank are
indistinguishable unless one of the following rules applies:

- A conversion that does not convert a pointer, a pointer to member, or
  `std::nullptr_t` to `bool` is better than one that does.
- A conversion that promotes an enumeration whose underlying type is
  fixed to its underlying type is better than one that promotes to the
  promoted underlying type, if the two are different.
- If class `B` is derived directly or indirectly from class `A`,
  conversion of `B*` to `A*` is better than conversion of `B*` to
  `void*`, and conversion of `A*` to `void*` is better than conversion
  of `B*` to `void*`.
- If class `B` is derived directly or indirectly from class `A` and
  class `C` is derived directly or indirectly from `B`,
  - conversion of `C*` to `B*` is better than conversion of `C*` to
    `A*`,
    ``` cpp
    struct A {};
    struct B : public A {};
    struct C : public B {};
    C* pc;
    int f(A*);
    int f(B*);
    int i = f(pc);                  // calls f(B*)
    ```
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

  Compared conversion sequences will have different source types only in
  the context of comparing the second standard conversion sequence of an
  initialization by user-defined conversion (see  [[over.match.best]]);
  in all other contexts, the source types will be the same and the
  target types will be different.

## Address of overloaded function <a id="over.over">[[over.over]]</a>

A use of an overloaded function name without arguments is resolved in
certain contexts to a function, a pointer to function or a pointer to
member function for a specific function from the overload set. A
function template name is considered to name a set of overloaded
functions in such contexts. The function selected is the one whose type
is identical to the function type of the target type required in the
context. That is, the class of which the function is a member is ignored
when matching a pointer-to-member-function type. The target can be

- an object or reference being initialized ([[dcl.init]],
  [[dcl.init.ref]], [[dcl.init.list]]),
- the left side of an assignment ([[expr.ass]]),
- a parameter of a function ([[expr.call]]),
- a parameter of a user-defined operator ([[over.oper]]),
- the return value of a function, operator function, or conversion (
  [[stmt.return]]),
- an explicit type conversion ([[expr.type.conv]],
  [[expr.static.cast]], [[expr.cast]]), or
- a non-type *template-parameter* ([[temp.arg.nontype]]).

The overloaded function name can be preceded by the `&` operator. An
overloaded function name shall not be used without arguments in contexts
other than those listed. Any redundant set of parentheses surrounding
the overloaded function name is ignored ([[expr.prim]]).

If the name is a function template, template argument deduction is
done ([[temp.deduct.funcaddr]]), and if the argument deduction
succeeds, the resulting template argument list is used to generate a
single function template specialization, which is added to the set of
overloaded functions considered. As described in  [[temp.arg.explicit]],
if deduction fails and the function template name is followed by an
explicit template argument list, the *template-id* is then examined to
see whether it identifies a single function template specialization. If
it does, the *template-id* is considered to be an lvalue for that
function template specialization. The target type is not used in that
determination.

Non-member functions and static member functions match targets of type
“pointer-to-function” or “reference-to-function.” Nonstatic member
functions match targets of type “pointer-to-member-function”. If a
non-static member function is selected, the reference to the overloaded
function name is required to have the form of a pointer to member as
described in  [[expr.unary.op]].

If more than one function is selected, any function template
specializations in the set are eliminated if the set also contains a
function that is not a function template specialization, and any given
function template specialization `F1` is eliminated if the set contains
a second function template specialization whose function template is
more specialized than the function template of `F1` according to the
partial ordering rules of  [[temp.func.order]]. After such eliminations,
if any, there shall remain exactly one selected function.

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
`int(...)` has been declared, and not because of any ambiguity. For
another example,

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

If `f()` and `g()` are both overloaded functions, the cross product of
possibilities must be considered to resolve `f(&g)`, or the equivalent
expression `f(g)`.

There are no standard conversions (Clause  [[conv]]) of one
pointer-to-function type into another. In particular, even if `B` is a
public base of `D`, we have

``` cpp
D* f();
B* (*p1)() = &f;                // error

void g(D*);
void (*p2)(B*) = &g;            // error
```

## Overloaded operators <a id="over.oper">[[over.oper]]</a>

A function declaration having one of the following
*operator-function-id*s as its name declares an *operator function*. A
function template declaration having one of the following
*operator-function-id*s as its name declares an *operator function
template*. A specialization of an operator function template is also an
operator function. An operator function is said to *implement* the
operator named in its *operator-function-id*.

``` bnf
operator-function-id:
    'operator' operator
```

The last two operators are function call ([[expr.call]]) and
subscripting ([[expr.sub]]). The operators `new[]`, `delete[]`, `()`,
and `[]` are formed from more than one token.

Both the unary and binary forms of

``` cpp
+    -    *     &
```

can be overloaded.

The following operators cannot be overloaded:

``` cpp
.    .*   ::    ?:
```

nor can the preprocessing symbols `#` and `##` (Clause  [[cpp]]).

Operator functions are usually not called directly; instead they are
invoked to evaluate the operators they implement ([[over.unary]] –
[[over.inc]]). They can be explicitly called, however, using the
*operator-function-id* as the name of the function in the function call
syntax ([[expr.call]]).

``` cpp
complex z = a.operator+(b);     // complex z = a+b;
void* p = operator new(sizeof(int)*n);
```

The allocation and deallocation functions, `operator` `new`, `operator`
`new[]`, `operator` `delete` and `operator` `delete[]`, are described
completely in  [[basic.stc.dynamic]]. The attributes and restrictions
found in the rest of this subclause do not apply to them unless
explicitly stated in  [[basic.stc.dynamic]].

An operator function shall either be a non-static member function or be
a non-member function that has at least one parameter whose type is a
class, a reference to a class, an enumeration, or a reference to an
enumeration. It is not possible to change the precedence, grouping, or
number of operands of operators. The meaning of the operators `=`,
(unary) `&`, and `,` (comma), predefined for each type, can be changed
for specific class and enumeration types by defining operator functions
that implement these operators. Operator functions are inherited in the
same manner as other base class functions.

The identities among certain predefined operators applied to basic types
(for example, `++a` ≡ `a+=1`) need not hold for operator functions. Some
predefined operators, such as `+=`, require an operand to be an lvalue
when applied to basic types; this is not required by operator functions.

An operator function cannot have default arguments (
[[dcl.fct.default]]), except where explicitly stated below. Operator
functions cannot have more or fewer parameters than the number required
for the corresponding operator, as described in the rest of this
subclause.

Operators not mentioned explicitly in subclauses  [[over.ass]] through 
[[over.inc]] act as ordinary unary and binary operators obeying the
rules of   [[over.unary]] or  [[over.binary]].

### Unary operators <a id="over.unary">[[over.unary]]</a>

A prefix unary operator shall be implemented by a non-static member
function ([[class.mfct]]) with no parameters or a non-member function
with one parameter. Thus, for any prefix unary operator `@`, `@x` can be
interpreted as either `x.operator@()` or `operator@(x)`. If both forms
of the operator function have been declared, the rules in 
[[over.match.oper]] determine which, if any, interpretation is used.
See  [[over.inc]] for an explanation of the postfix unary operators `++`
and `\dcr`.

The unary and binary forms of the same operator are considered to have
the same name. Consequently, a unary operator can hide a binary operator
from an enclosing scope, and vice versa.

### Binary operators <a id="over.binary">[[over.binary]]</a>

A binary operator shall be implemented either by a non-static member
function ([[class.mfct]]) with one parameter or by a non-member
function with two parameters. Thus, for any binary operator `@`, `x@y`
can be interpreted as either `x.operator@(y)` or `operator@(x,y)`. If
both forms of the operator function have been declared, the rules in 
[[over.match.oper]] determine which, if any, interpretation is used.

### Assignment <a id="over.ass">[[over.ass]]</a>

An assignment operator shall be implemented by a non-static member
function with exactly one parameter. Because a copy assignment operator
`operator=` is implicitly declared for a class if not declared by the
user ([[class.copy]]), a base class assignment operator is always
hidden by the copy assignment operator of the derived class.

Any assignment operator, even the copy and move assignment operators,
can be virtual. For a derived class `D` with a base class `B` for which
a virtual copy/move assignment has been declared, the copy/move
assignment operator in `D` does not override `B`’s virtual copy/move
assignment operator.

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
  dobj1 = dobj2;                // calls implicitly-declared
                                // D::operator=(const D&)
}
```

### Function call <a id="over.call">[[over.call]]</a>

`operator()`

shall be a non-static member function with an arbitrary number of
parameters. It can have default arguments. It implements the function
call syntax

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

where the *postfix-expression* evaluates to a class object and the
possibly empty *expression-list* matches the parameter list of an
`operator()` member function of the class. Thus, a call `x(arg1,...)` is
interpreted as `x.operator()(arg1, ...)` for a class object `x` of type
`T` if `T::operator()(T1,` `T2,` `T3)` exists and if the operator is
selected as the best match function by the overload resolution
mechanism ([[over.match.best]]).

### Subscripting <a id="over.sub">[[over.sub]]</a>

`operator[]`

shall be a non-static member function with exactly one parameter. It
implements the subscripting syntax

``` bnf
postfix-expression '[' expression ']'
```

or

``` bnf
postfix-expression '[' braced-init-list ']'
```

Thus, a subscripting expression `x[y]` is interpreted as
`x.operator[](y)` for a class object `x` of type `T` if
`T::operator[](T1)` exists and if the operator is selected as the best
match function by the overload resolution mechanism (
[[over.match.best]]).

``` cpp
struct X {
  Z operator[](std::initializer_list<int>);
};
X x;
x[{1,2,3}] = 7;           // OK: meaning x.operator[]({1,2,3\)}
int a[10];
a[{1,2,3}] = 7;           // error: built-in subscript operator
```

### Class member access <a id="over.ref">[[over.ref]]</a>

`operator->`

shall be a non-static member function taking no parameters. It
implements the class member access syntax that uses `->`.

``` bnf
postfix-expression '->' 'templateₒₚₜ ' id-expression\\
postfix-expression '->' pseudo-destructor-name
```

An expression `x->m` is interpreted as `(x.operator->())->m` for a class
object `x` of type `T` if `T::operator->()` exists and if the operator
is selected as the best match function by the overload resolution
mechanism ([[over.match]]).

### Increment and decrement <a id="over.inc">[[over.inc]]</a>

The user-defined function called `operator++` implements the prefix and
postfix `++` operator. If this function is a non-static member function
with no parameters, or a non-member function with one parameter, it
defines the prefix increment operator `++` for objects of that type. If
the function is a non-static member function with one parameter (which
shall be of type `int`) or a non-member function with two parameters
(the second of which shall be of type `int`), it defines the postfix
increment operator `++` for objects of that type. When the postfix
increment is called as a result of using the `++` operator, the `int`
argument will have value zero.[^13]

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

The prefix and postfix decrement operators `-{-}` are handled
analogously.

### User-defined literals <a id="over.literal">[[over.literal]]</a>

``` bnf
literal-operator-id:
    'operator' string-literal identifier
    'operator' user-defined-string-literal
```

The *string-literal* or *user-defined-string-literal* in a
*literal-operator-id* shall have no *encoding-prefix* and shall contain
no characters other than the implicit terminating `'\0'`. The
*ud-suffix* of the *user-defined-string-literal* or the *identifier* in
a *literal-operator-id* is called a *literal suffix identifier*. some
literal suffix identifiers are reserved for future standardization; see 
[[usrlit.suffix]].

A declaration whose *declarator-id* is a *literal-operator-id* shall be
a declaration of a namespace-scope function or function template (it
could be a friend function ([[class.friend]])), an explicit
instantiation or specialization of a function template, or a
*using-declaration* ([[namespace.udecl]]). A function declared with a
*literal-operator-id* is a *literal operator*. A function template
declared with a *literal-operator-id* is a *literal operator template*.

The declaration of a literal operator shall have a
*parameter-declaration-clause* equivalent to one of the following:

``` cpp
const char*
unsigned long long int
long double
char
wchar_t
char16_t
char32_t
const char*, std::size_t
const wchar_t*, std::size_t
const char16_t*, std::size_t
const char32_t*, std::size_t
```

If a parameter has a default argument ([[dcl.fct.default]]), the
program is ill-formed.

A *raw literal operator* is a literal operator with a single parameter
whose type is `const char*`.

The declaration of a literal operator template shall have an empty
*parameter-declaration-clause* and its *template-parameter-list* shall
have a single *template-parameter* that is a non-type template parameter
pack ([[temp.variadic]]) with element type `char`.

Literal operators and literal operator templates shall not have C
language linkage.

Literal operators and literal operator templates are usually invoked
implicitly through user-defined literals ([[lex.ext]]). However, except
for the constraints described above, they are ordinary namespace-scope
functions and function templates. In particular, they are looked up like
ordinary functions and function templates and they follow the same
overload resolution rules. Also, they can be declared `inline` or
`constexpr`, they may have internal or external linkage, they can be
called explicitly, their addresses can be taken, etc.

``` cpp
void operator "" _km(long double);                  // OK
string operator "" _i18n(const char*, std::size_t); // OK
template <char...> double operator "" _\u03C0();    // OK: UCN for lowercase pi
float operator ""_e(const char*);                   // OK
float operator ""E(const char*);                    // error: reserved literal suffix~([usrlit.suffix], [lex.ext])
double operator""_Bq(long double);                  // OK: does not use the reserved name _Bq~([global.names])
double operator"" _Bq(long double);                 // uses the reserved name _Bq~([global.names])
float operator " " B(const char*);                  // error: non-empty string-literal
string operator "" 5X(const char*, std::size_t);    // error: invalid literal suffix identifier
double operator "" _miles(double);                  // error: invalid parameter-declaration-clause
template <char...> int operator "" _j(const char*); // error: invalid parameter-declaration-clause
extern "C" void operator "" _m(long double);        // error: C language linkage
```

## Built-in operators <a id="over.built">[[over.built]]</a>

The candidate operator functions that represent the built-in operators
defined in Clause  [[expr]] are specified in this subclause. These
candidate functions participate in the operator overload resolution
process as described in  [[over.match.oper]] and are used for no other
purpose. Because built-in operators take only operands with non-class
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
the built-in operator given in Clause  [[expr]], and therefore to any
additional semantic constraints given there. If there is a user-written
candidate with the same name and parameter types as a built-in candidate
operator function, the built-in operator function is hidden and is not
included in the set of candidate functions.

In this subclause, the term *promoted integral type* is used to refer to
those integral types which are preserved by integral promotion
(including e.g. `int` and `long` but excluding e.g. `char`). Similarly,
the term *promoted arithmetic type* refers to floating types plus
promoted integral types. In all cases where a promoted integral type or
promoted arithmetic type is required, an operand of enumeration type
will be acceptable by way of the integral promotions.

For every pair (*T*, *VQ*), where *T* is an arithmetic type, and *VQ* is
either `volatile` or empty, there exist candidate operator functions of
the form

``` cpp
VQ T& operator++(VQ T&);
T operator++(VQ T&, int);
```

For every pair (*T*, *VQ*), where *T* is an arithmetic type other than
*bool*, and *VQ* is either `volatile` or empty, there exist candidate
operator functions of the form

``` cpp
VQ T& operator--(VQ T&);
T operator--(VQ T&, int);
```

For every pair (*T*, *VQ*), where *T* is a cv-qualified or
cv-unqualified object type, and *VQ* is either `volatile` or empty,
there exist candidate operator functions of the form

``` cpp
T*VQ& operator++(T*VQ&);
T*VQ& operator--(T*VQ&);
T*    operator++(T*VQ&, int);
T*    operator--(T*VQ&, int);
```

For every cv-qualified or cv-unqualified object type *T*, there exist
candidate operator functions of the form

``` cpp
T&    operator*(T*);
```

For every function type *T* that does not have cv-qualifiers or a
*ref-qualifier*, there exist candidate operator functions of the form

``` cpp
T&    operator*(T*);
```

For every type *T* there exist candidate operator functions of the form

``` cpp
T*    operator+(T*);
```

For every promoted arithmetic type *T*, there exist candidate operator
functions of the form

``` cpp
T operator+(T);
T operator-(T);
```

For every promoted integral type *T*, there exist candidate operator
functions of the form

``` cpp
T operator~(T);
```

For every quintuple (*C1*, *C2*, *T*, *CV1*, *CV2*), where *C2* is a
class type, *C1* is the same type as C2 or is a derived class of C2, *T*
is an object type or a function type, and *CV1* and *CV2* are
*cv-qualifier-seq*s, there exist candidate operator functions of the
form

``` cpp
CV12 T& operator->*(CV1 C1*, CV2 T C2::*);
```

where *CV12* is the union of *CV1* and *CV2*. The return type is shown
for exposition only; see  [[expr.mptr.oper]] for the determination of
the operator’s result type.

For every pair of promoted arithmetic types *L* and *R*, there exist
candidate operator functions of the form

``` cpp
LR      operator*(L, R);
LR      operator/(L, R);
LR      operator+(L, R);
LR      operator-(L, R);
bool    operator<(L, R);
bool    operator>(L, R);
bool    operator<=(L, R);
bool    operator>=(L, R);
bool    operator==(L, R);
bool    operator!=(L, R);
```

where *LR* is the result of the usual arithmetic conversions between
types *L* and *R*.

For every cv-qualified or cv-unqualified object type *T* there exist
candidate operator functions of the form

``` cpp
T*      operator+(T*, std::ptrdiff_t);
T&      operator[](T*, std::ptrdiff_t);
T*      operator-(T*, std::ptrdiff_t);
T*      operator+(std::ptrdiff_t, T*);
T&      operator[](std::ptrdiff_t, T*);
```

For every *T*, where *T* is a pointer to object type, there exist
candidate operator functions of the form

``` cpp
std::ptrdiff_t   operator-(T, T);
```

For every *T*, where *T* is an enumeration type or a pointer type, there
exist candidate operator functions of the form

``` cpp
bool    operator<(T, T);
bool    operator>(T, T);
bool    operator<=(T, T);
bool    operator>=(T, T);
bool    operator==(T, T);
bool    operator!=(T, T);
```

For every pointer to member type *T* or type `std::nullptr_t` there
exist candidate operator functions of the form

``` cpp
bool    operator==(T, T);
bool    operator!=(T, T);
```

For every pair of promoted integral types *L* and *R*, there exist
candidate operator functions of the form

``` cpp
LR      operator%(L, R);
LR      operator&(L, R);
LR      operator^(L, R);
LR      operator|(L, R);
L       operator<<(L, R);
L       operator>>(L, R);
```

where *LR* is the result of the usual arithmetic conversions between
types *L* and *R*.

For every triple (*L*, *VQ*, *R*), where *L* is an arithmetic type, *VQ*
is either `volatile` or empty, and *R* is a promoted arithmetic type,
there exist candidate operator functions of the form

``` cpp
VQ L&   operator=(VQ L&, R);
VQ L&   operator*=(VQ L&, R);
VQ L&   operator/=(VQ L&, R);
VQ L&   operator+=(VQ L&, R);
VQ L&   operator-=(VQ L&, R);
```

For every pair (*T*, *VQ*), where *T* is any type and *VQ* is either
`volatile` or empty, there exist candidate operator functions of the
form

``` cpp
T*VQ&   operator=(T*VQ&, T*);
```

For every pair (*T*, *VQ*), where *T* is an enumeration or pointer to
member type and *VQ* is either `volatile` or empty, there exist
candidate operator functions of the form

``` cpp
VQ T&   operator=(VQ T&, T);
```

For every pair (*T*, *VQ*), where *T* is a cv-qualified or
cv-unqualified object type and *VQ* is either `volatile` or empty, there
exist candidate operator functions of the form

``` cpp
T*VQ&   operator+=(T*VQ&, std::ptrdiff_t);
T*VQ&   operator-=(T*VQ&, std::ptrdiff_t);
```

For every triple (*L*, *VQ*, *R*), where *L* is an integral type, *VQ*
is either `volatile` or empty, and *R* is a promoted integral type,
there exist candidate operator functions of the form

``` cpp
VQ L&   operator%=(VQ L&, R);
VQ L&   operator<<=(VQ L&, R);
VQ L&   operator>>=(VQ L&, R);
VQ L&   operator&=(VQ L&, R);
VQ L&   operator^=(VQ L&, R);
VQ L&   operator|=(VQ L&, R);
```

There also exist candidate operator functions of the form

``` cpp
bool    operator!(bool);
bool    operator&&(bool, bool);
bool    operator||(bool, bool);
```

For every pair of promoted arithmetic types *L* and *R*, there exist
candidate operator functions of the form

``` cpp
LR      operator?:(bool, L, R);
```

where *LR* is the result of the usual arithmetic conversions between
types *L* and *R*. As with all these descriptions of candidate
functions, this declaration serves only to describe the built-in
operator for purposes of overload resolution. The operator “`?:`” cannot
be overloaded.

For every type *T*, where *T* is a pointer, pointer-to-member, or scoped
enumeration type, there exist candidate operator functions of the form

``` cpp
T       operator?:(bool, T, T);
```

<!-- Link reference definitions -->
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[class.access]: class.md#class.access
[class.conv]: special.md#class.conv
[class.conv.ctor]: special.md#class.conv.ctor
[class.conv.fct]: special.md#class.conv.fct
[class.copy]: special.md#class.copy
[class.friend]: class.md#class.friend
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.static]: class.md#class.static
[class.this]: class.md#class.this
[conv]: conv.md#conv
[conv.array]: conv.md#conv.array
[conv.bool]: conv.md#conv.bool
[conv.double]: conv.md#conv.double
[conv.fpint]: conv.md#conv.fpint
[conv.fpprom]: conv.md#conv.fpprom
[conv.func]: conv.md#conv.func
[conv.integral]: conv.md#conv.integral
[conv.lval]: conv.md#conv.lval
[conv.mem]: conv.md#conv.mem
[conv.prom]: conv.md#conv.prom
[conv.ptr]: conv.md#conv.ptr
[conv.qual]: conv.md#conv.qual
[cpp]: cpp.md#cpp
[dcl.array]: dcl.md#dcl.array
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.typedef]: dcl.md#dcl.typedef
[expr]: expr.md#expr
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.cond]: expr.md#expr.cond
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.prim]: expr.md#expr.prim
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.type.conv]: expr.md#expr.type.conv
[expr.unary.op]: expr.md#expr.unary.op
[lex.ext]: lex.md#lex.ext
[namespace.udecl]: dcl.md#namespace.udecl
[over]: #over
[over.ass]: #over.ass
[over.best.ics]: #over.best.ics
[over.binary]: #over.binary
[over.built]: #over.built
[over.call]: #over.call
[over.call.func]: #over.call.func
[over.call.object]: #over.call.object
[over.dcl]: #over.dcl
[over.ics.ellipsis]: #over.ics.ellipsis
[over.ics.list]: #over.ics.list
[over.ics.rank]: #over.ics.rank
[over.ics.ref]: #over.ics.ref
[over.ics.scs]: #over.ics.scs
[over.ics.user]: #over.ics.user
[over.inc]: #over.inc
[over.literal]: #over.literal
[over.load]: #over.load
[over.match]: #over.match
[over.match.best]: #over.match.best
[over.match.call]: #over.match.call
[over.match.conv]: #over.match.conv
[over.match.copy]: #over.match.copy
[over.match.ctor]: #over.match.ctor
[over.match.funcs]: #over.match.funcs
[over.match.list]: #over.match.list
[over.match.oper]: #over.match.oper
[over.match.ref]: #over.match.ref
[over.match.viable]: #over.match.viable
[over.oper]: #over.oper
[over.over]: #over.over
[over.ref]: #over.ref
[over.sub]: #over.sub
[over.unary]: #over.unary
[stmt.return]: stmt.md#stmt.return
[tab:over.conversions]: #tab:over.conversions
[tab:over.rel.op.func]: #tab:over.rel.op.func
[temp.arg.explicit]: temp.md#temp.arg.explicit
[temp.arg.nontype]: temp.md#temp.arg.nontype
[temp.deduct]: temp.md#temp.deduct
[temp.deduct.funcaddr]: temp.md#temp.deduct.funcaddr
[temp.func.order]: temp.md#temp.func.order
[temp.over]: temp.md#temp.over
[temp.variadic]: temp.md#temp.variadic
[usrlit.suffix]: library.md#usrlit.suffix

[^1]: When a parameter type includes a function type, such as in the
    case of a parameter type that is a pointer to function, the `const`
    and `volatile` type-specifiers at the outermost level of the
    parameter type specifications for the inner function type are also
    ignored.

[^2]: The process of argument deduction fully determines the parameter
    types of the function template specializations, i.e., the parameters
    of function template specializations contain no template parameter
    types. Therefore, except where specified otherwise, function
    template specializations and non-template functions ([[dcl.fct]])
    are treated equivalently for the remainder of overload resolution.

[^3]: Note that cv-qualifiers on the type of objects are significant in
    overload resolution for both glvalue and class prvalue objects.

[^4]: An implied object argument must be contrived to correspond to the
    implicit object parameter attributed to member functions during
    overload resolution. It is not used in the call to the selected
    function. Since the member functions all have the same implicit
    object parameter, the contrived object will not be the cause to
    select or reject a function.

[^5]: Note that this construction can yield candidate call functions
    that cannot be differentiated one from the other by overload
    resolution because they have identical declarations or differ only
    in their return type. The call will be ambiguous if overload
    resolution cannot select a match to the call that is uniquely better
    than such undifferentiable functions.

[^6]: If the set of candidate functions is empty, overload resolution is
    unsuccessful.

[^7]: If the value returned by the `operator->` function has class type,
    this may result in selecting and calling another `operator->`
    function. The process repeats until an `operator->` function returns
    a value of non-class type.

[^8]: According to  [[dcl.fct.default]], parameters following the
    *(m+1)*-st parameter must also have default arguments.

[^9]: If a function is a static member function, this definition means
    that the first argument, the implied object argument, has no effect
    in the determination of whether the function is better or worse than
    any other function.

[^10]: The algorithm for selecting the best viable function is linear in
    the number of viable functions. Run a simple tournament to find a
    function `W` that is not worse than any opponent it faced. Although
    another function `F` that `W` did not face might be at least as good
    as `W`, `F` cannot be the best function because at some point in the
    tournament `F` encountered another function `G` such that `F` was
    not better than `G`. Hence, `W` is either the best function or there
    is no best function. So, make a second pass over the viable
    functions to verify that `W` is better than all other functions.

[^11]: The ambiguous conversion sequence is ranked with user-defined
    conversion sequences because multiple conversion sequences for an
    argument can exist only if they involve different user-defined
    conversions. The ambiguous conversion sequence is indistinguishable
    from any other user-defined conversion sequence because it
    represents at least two user-defined conversion sequences, each with
    a different user-defined conversion, and any other user-defined
    conversion sequence must be indistinguishable from at least one of
    them.

    This rule prevents a function from becoming non-viable because of an
    ambiguous conversion sequence for one of its parameters. Consider
    this example,

    If it were not for this rule, `f(A)` would be eliminated as a viable
    function for the call `f(b)` causing overload resolution to select
    `f(C)` as the function to call even though it is not clearly the
    best choice. On the other hand, if an `f(B)` were to be declared
    then `f(b)` would resolve to that `f(B)` because the exact match
    with `f(B)` is better than any of the sequences required to match
    `f(A)`.

[^12]: Since there are no parameters of array type, this will only occur
    as the underlying type of a reference parameter.

[^13]: Calling `operator++` explicitly, as in expressions like
    `a.operator++(2)`, has no special properties: The argument to
    `operator++` is `2`.
