# Diagnostics library <a id="diagnostics">[[diagnostics]]</a>

## General <a id="diagnostics.general">[[diagnostics.general]]</a>

This Clause describes components that C++ programs may use to detect and
report error conditions.

The following subclauses describe components for reporting several kinds
of exceptional conditions, documenting program assertions, and a global
variable for error number codes, as summarized in
[[diagnostics.summary]].

**Table: Diagnostics library summary**

| Subclause          |                      | Header           |
| ------------------ | -------------------- | ---------------- |
| [[std.exceptions]] | Exception classes    | `<stdexcept>`    |
| [[assertions]]     | Assertions           | `<cassert>`      |
| [[errno]]          | Error numbers        | `<cerrno>`       |
| [[syserr]]         | System error support | `<system_error>` |


## Exception classes <a id="std.exceptions">[[std.exceptions]]</a>

The C++ standard library provides classes to be used to report certain
errors [[res.on.exception.handling]] in C++ programs. In the error model
reflected in these classes, errors are divided into two broad
categories: *logic* errors and *runtime* errors.

The distinguishing characteristic of logic errors is that they are due
to errors in the internal logic of the program. In theory, they are
preventable.

By contrast, runtime errors are due to events beyond the scope of the
program. They cannot be easily predicted in advance. The header
`<stdexcept>` defines several types of predefined exceptions for
reporting errors in a C++ program. These exceptions are related by
inheritance.

### Header `<stdexcept>` synopsis <a id="stdexcept.syn">[[stdexcept.syn]]</a>

``` cpp
namespace std {
  class logic_error;
    class domain_error;
    class invalid_argument;
    class length_error;
    class out_of_range;
  class runtime_error;
    class range_error;
    class overflow_error;
    class underflow_error;
}
```

### Class `logic_error` <a id="logic.error">[[logic.error]]</a>

``` cpp
namespace std {
  class logic_error : public exception {
  public:
    explicit logic_error(const string& what_arg);
    explicit logic_error(const char* what_arg);
  };
}
```

The class `logic_error` defines the type of objects thrown as exceptions
to report errors presumably detectable before the program executes, such
as violations of logical preconditions or class invariants.

``` cpp
logic_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
logic_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `domain_error` <a id="domain.error">[[domain.error]]</a>

``` cpp
namespace std {
  class domain_error : public logic_error {
  public:
    explicit domain_error(const string& what_arg);
    explicit domain_error(const char* what_arg);
  };
}
```

The class `domain_error` defines the type of objects thrown as
exceptions by the implementation to report domain errors.

``` cpp
domain_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
domain_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `invalid_argument` <a id="invalid.argument">[[invalid.argument]]</a>

``` cpp
namespace std {
  class invalid_argument : public logic_error {
  public:
    explicit invalid_argument(const string& what_arg);
    explicit invalid_argument(const char* what_arg);
  };
}
```

The class `invalid_argument` defines the type of objects thrown as
exceptions to report an invalid argument.

``` cpp
invalid_argument(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
invalid_argument(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `length_error` <a id="length.error">[[length.error]]</a>

``` cpp
namespace std {
  class length_error : public logic_error {
  public:
    explicit length_error(const string& what_arg);
    explicit length_error(const char* what_arg);
  };
}
```

The class `length_error` defines the type of objects thrown as
exceptions to report an attempt to produce an object whose length
exceeds its maximum allowable size.

``` cpp
length_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
length_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `out_of_range` <a id="out.of.range">[[out.of.range]]</a>

``` cpp
namespace std {
  class out_of_range : public logic_error {
  public:
    explicit out_of_range(const string& what_arg);
    explicit out_of_range(const char* what_arg);
  };
}
```

The class `out_of_range` defines the type of objects thrown as
exceptions to report an argument value not in its expected range.

``` cpp
out_of_range(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
out_of_range(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `runtime_error` <a id="runtime.error">[[runtime.error]]</a>

``` cpp
namespace std {
  class runtime_error : public exception {
  public:
    explicit runtime_error(const string& what_arg);
    explicit runtime_error(const char* what_arg);
  };
}
```

The class `runtime_error` defines the type of objects thrown as
exceptions to report errors presumably detectable only when the program
executes.

``` cpp
runtime_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
runtime_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `range_error` <a id="range.error">[[range.error]]</a>

``` cpp
namespace std {
  class range_error : public runtime_error {
  public:
    explicit range_error(const string& what_arg);
    explicit range_error(const char* what_arg);
  };
}
```

The class `range_error` defines the type of objects thrown as exceptions
to report range errors in internal computations.

``` cpp
range_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
range_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `overflow_error` <a id="overflow.error">[[overflow.error]]</a>

``` cpp
namespace std {
  class overflow_error : public runtime_error {
  public:
    explicit overflow_error(const string& what_arg);
    explicit overflow_error(const char* what_arg);
  };
}
```

The class `overflow_error` defines the type of objects thrown as
exceptions to report an arithmetic overflow error.

``` cpp
overflow_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
overflow_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

### Class `underflow_error` <a id="underflow.error">[[underflow.error]]</a>

``` cpp
namespace std {
  class underflow_error : public runtime_error {
  public:
    explicit underflow_error(const string& what_arg);
    explicit underflow_error(const char* what_arg);
  };
}
```

The class `underflow_error` defines the type of objects thrown as
exceptions to report an arithmetic underflow error.

``` cpp
underflow_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
underflow_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

## Assertions <a id="assertions">[[assertions]]</a>

The header `<cassert>` provides a macro for documenting C++ program
assertions and a mechanism for disabling the assertion checks.

### Header `<cassert>` synopsis <a id="cassert.syn">[[cassert.syn]]</a>

``` cpp
#define assert(E) see below
```

The contents are the same as the C standard library header `<assert.h>`,
except that a macro named `static_assert` is not defined.

### The `assert` macro <a id="assertions.assert">[[assertions.assert]]</a>

An expression `assert(E)` is a constant subexpression
[[defns.const.subexpr]], if

- `NDEBUG` is defined at the point where `assert` is last defined or
  redefined, or
- `E` contextually converted to `bool` [[conv]] is a constant
  subexpression that evaluates to the value `true`.

## Error numbers <a id="errno">[[errno]]</a>

The contents of the header `<cerrno>` are the same as the POSIX header
`<errno.h>`, except that `errno` shall be defined as a macro.

[*Note 1*: The intent is to remain in close alignment with the POSIX
standard. — *end note*\]

A separate `errno` value shall be provided for each thread.

### Header `<cerrno>` synopsis <a id="cerrno.syn">[[cerrno.syn]]</a>

``` cpp
#define errno see below

#define E2BIG see below
#define EACCES see below
#define EADDRINUSE see below
#define EADDRNOTAVAIL see below
#define EAFNOSUPPORT see below
#define EAGAIN see below
#define EALREADY see below
#define EBADF see below
#define EBADMSG see below
#define EBUSY see below
#define ECANCELED see below
#define ECHILD see below
#define ECONNABORTED see below
#define ECONNREFUSED see below
#define ECONNRESET see below
#define EDEADLK see below
#define EDESTADDRREQ see below
#define EDOM see below
#define EEXIST see below
#define EFAULT see below
#define EFBIG see below
#define EHOSTUNREACH see below
#define EIDRM see below
#define EILSEQ see below
#define EINPROGRESS see below
#define EINTR see below
#define EINVAL see below
#define EIO see below
#define EISCONN see below
#define EISDIR see below
#define ELOOP see below
#define EMFILE see below
#define EMLINK see below
#define EMSGSIZE see below
#define ENAMETOOLONG see below
#define ENETDOWN see below
#define ENETRESET see below
#define ENETUNREACH see below
#define ENFILE see below
#define ENOBUFS see below
#define ENODATA see below
#define ENODEV see below
#define ENOENT see below
#define ENOEXEC see below
#define ENOLCK see below
#define ENOLINK see below
#define ENOMEM see below
#define ENOMSG see below
#define ENOPROTOOPT see below
#define ENOSPC see below
#define ENOSR see below
#define ENOSTR see below
#define ENOSYS see below
#define ENOTCONN see below
#define ENOTDIR see below
#define ENOTEMPTY see below
#define ENOTRECOVERABLE see below
#define ENOTSOCK see below
#define ENOTSUP see below
#define ENOTTY see below
#define ENXIO see below
#define EOPNOTSUPP see below
#define EOVERFLOW see below
#define EOWNERDEAD see below
#define EPERM see below
#define EPIPE see below
#define EPROTO see below
#define EPROTONOSUPPORT see below
#define EPROTOTYPE see below
#define ERANGE see below
#define EROFS see below
#define ESPIPE see below
#define ESRCH see below
#define ETIME see below
#define ETIMEDOUT see below
#define ETXTBSY see below
#define EWOULDBLOCK see below
#define EXDEV see below
```

The meaning of the macros in this header is defined by the POSIX
standard.

## System error support <a id="syserr">[[syserr]]</a>

This subclause describes components that the standard library and C++
programs may use to report error conditions originating from the
operating system or other low-level application program interfaces.

Components described in this subclause shall not change the value of
`errno` [[errno]]. Implementations should leave the error states
provided by other libraries unchanged.

### Header `<system_error>` synopsis <a id="system.error.syn">[[system.error.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  class error_category;
  const error_category& generic_category() noexcept;
  const error_category& system_category() noexcept;

  class error_code;
  class error_condition;
  class system_error;

  template<class T>
    struct is_error_code_enum : public false_type {};

  template<class T>
    struct is_error_condition_enum : public false_type {};

  enum class errc {
    address_family_not_supported,       // EAFNOSUPPORT
    address_in_use,                     // EADDRINUSE
    address_not_available,              // EADDRNOTAVAIL
    already_connected,                  // EISCONN
    argument_list_too_long,             // E2BIG
    argument_out_of_domain,             // EDOM
    bad_address,                        // EFAULT
    bad_file_descriptor,                // EBADF
    bad_message,                        // EBADMSG
    broken_pipe,                        // EPIPE
    connection_aborted,                 // ECONNABORTED
    connection_already_in_progress,     // EALREADY
    connection_refused,                 // ECONNREFUSED
    connection_reset,                   // ECONNRESET
    cross_device_link,                  // EXDEV
    destination_address_required,       // EDESTADDRREQ
    device_or_resource_busy,            // EBUSY
    directory_not_empty,                // ENOTEMPTY
    executable_format_error,            // ENOEXEC
    file_exists,                        // EEXIST
    file_too_large,                     // EFBIG
    filename_too_long,                  // ENAMETOOLONG
    function_not_supported,             // ENOSYS
    host_unreachable,                   // EHOSTUNREACH
    identifier_removed,                 // EIDRM
    illegal_byte_sequence,              // EILSEQ
    inappropriate_io_control_operation, // ENOTTY
    interrupted,                        // EINTR
    invalid_argument,                   // EINVAL
    invalid_seek,                       // ESPIPE
    io_error,                           // EIO
    is_a_directory,                     // EISDIR
    message_size,                       // EMSGSIZE
    network_down,                       // ENETDOWN
    network_reset,                      // ENETRESET
    network_unreachable,                // ENETUNREACH
    no_buffer_space,                    // ENOBUFS
    no_child_process,                   // ECHILD
    no_link,                            // ENOLINK
    no_lock_available,                  // ENOLCK
    no_message_available,               // ENODATA
    no_message,                         // ENOMSG
    no_protocol_option,                 // ENOPROTOOPT
    no_space_on_device,                 // ENOSPC
    no_stream_resources,                // ENOSR
    no_such_device_or_address,          // ENXIO
    no_such_device,                     // ENODEV
    no_such_file_or_directory,          // ENOENT
    no_such_process,                    // ESRCH
    not_a_directory,                    // ENOTDIR
    not_a_socket,                       // ENOTSOCK
    not_a_stream,                       // ENOSTR
    not_connected,                      // ENOTCONN
    not_enough_memory,                  // ENOMEM
    not_supported,                      // ENOTSUP
    operation_canceled,                 // ECANCELED
    operation_in_progress,              // EINPROGRESS
    operation_not_permitted,            // EPERM
    operation_not_supported,            // EOPNOTSUPP
    operation_would_block,              // EWOULDBLOCK
    owner_dead,                         // EOWNERDEAD
    permission_denied,                  // EACCES
    protocol_error,                     // EPROTO
    protocol_not_supported,             // EPROTONOSUPPORT
    read_only_file_system,              // EROFS
    resource_deadlock_would_occur,      // EDEADLK
    resource_unavailable_try_again,     // EAGAIN
    result_out_of_range,                // ERANGE
    state_not_recoverable,              // ENOTRECOVERABLE
    stream_timeout,                     // ETIME
    text_file_busy,                     // ETXTBSY
    timed_out,                          // ETIMEDOUT
    too_many_files_open_in_system,      // ENFILE
    too_many_files_open,                // EMFILE
    too_many_links,                     // EMLINK
    too_many_symbolic_link_levels,      // ELOOP
    value_too_large,                    // EOVERFLOW
    wrong_protocol_type,                // EPROTOTYPE
  };

  template<> struct is_error_condition_enum<errc> : true_type {};

  // [syserr.errcode.nonmembers], non-member functions
  error_code make_error_code(errc e) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const error_code& ec);

  // [syserr.errcondition.nonmembers], non-member functions
  error_condition make_error_condition(errc e) noexcept;

  // [syserr.compare], comparison functions
  bool operator==(const error_code& lhs, const error_code& rhs) noexcept;
  bool operator==(const error_code& lhs, const error_condition& rhs) noexcept;
  bool operator==(const error_condition& lhs, const error_condition& rhs) noexcept;
  strong_ordering operator<=>(const error_code& lhs, const error_code& rhs) noexcept;
  strong_ordering operator<=>(const error_condition& lhs, const error_condition& rhs) noexcept;

  // [syserr.hash], hash support
  template<class T> struct hash;
  template<> struct hash<error_code>;
  template<> struct hash<error_condition>;

  // [syserr], system error support
  template<class T>
    inline constexpr bool is_error_code_enum_v = is_error_code_enum<T>::value;
  template<class T>
    inline constexpr bool is_error_condition_enum_v = is_error_condition_enum<T>::value;
}
```

The value of each `enum errc` constant shall be the same as the value of
the `<cerrno>` macro shown in the above synopsis. Whether or not the
`<system_error>` implementation exposes the `<cerrno>` macros is
unspecified.

The `is_error_code_enum` and `is_error_condition_enum` may be
specialized for program-defined types to indicate that such types are
eligible for `class error_code` and `class error_condition` automatic
conversions, respectively.

### Class `error_category` <a id="syserr.errcat">[[syserr.errcat]]</a>

#### Overview <a id="syserr.errcat.overview">[[syserr.errcat.overview]]</a>

The class `error_category` serves as a base class for types used to
identify the source and encoding of a particular category of error code.
Classes may be derived from `error_category` to support categories of
errors in addition to those defined in this document. Such classes shall
behave as specified in subclause  [[syserr.errcat]].

[*Note 1*: `error_category` objects are passed by reference, and two
such objects are equal if they have the same address. This means that
applications using custom `error_category` types should create a single
object of each such type. — *end note*\]

``` cpp
namespace std {
  class error_category {
  public:
    constexpr error_category() noexcept;
    virtual ~error_category();
    error_category(const error_category&) = delete;
    error_category& operator=(const error_category&) = delete;
    virtual const char* name() const noexcept = 0;
    virtual error_condition default_error_condition(int ev) const noexcept;
    virtual bool equivalent(int code, const error_condition& condition) const noexcept;
    virtual bool equivalent(const error_code& code, int condition) const noexcept;
    virtual string message(int ev) const = 0;

    bool operator==(const error_category& rhs) const noexcept;
    strong_ordering operator<=>(const error_category& rhs) const noexcept;
  };

  const error_category& generic_category() noexcept;
  const error_category& system_category() noexcept;
}
```

#### Virtual members <a id="syserr.errcat.virtuals">[[syserr.errcat.virtuals]]</a>

``` cpp
virtual const char* name() const noexcept = 0;
```

*Returns:* A string naming the error category.

``` cpp
virtual error_condition default_error_condition(int ev) const noexcept;
```

*Returns:* `error_condition(ev, *this)`.

``` cpp
virtual bool equivalent(int code, const error_condition& condition) const noexcept;
```

*Returns:* `default_error_condition(code) == condition`.

``` cpp
virtual bool equivalent(const error_code& code, int condition) const noexcept;
```

*Returns:* `*this == code.category() && code.value() == condition`.

``` cpp
virtual string message(int ev) const = 0;
```

*Returns:* A string that describes the error condition denoted by `ev`.

#### Non-virtual members <a id="syserr.errcat.nonvirtuals">[[syserr.errcat.nonvirtuals]]</a>

``` cpp
bool operator==(const error_category& rhs) const noexcept;
```

*Returns:* `this == &rhs`.

``` cpp
strong_ordering operator<=>(const error_category& rhs) const noexcept;
```

*Returns:* `compare_three_way()(this, &rhs)`.

[*Note 1*: `compare_three_way`[[comparisons.three.way]] provides a
total ordering for pointers. — *end note*\]

#### Program-defined classes derived from `error_category` <a id="syserr.errcat.derived">[[syserr.errcat.derived]]</a>

``` cpp
virtual const char* name() const noexcept = 0;
```

*Returns:* A string naming the error category.

``` cpp
virtual error_condition default_error_condition(int ev) const noexcept;
```

*Returns:* An object of type `error_condition` that corresponds to `ev`.

``` cpp
virtual bool equivalent(int code, const error_condition& condition) const noexcept;
```

*Returns:* `true` if, for the category of error represented by `*this`,
`code` is considered equivalent to `condition`; otherwise, `false`.

``` cpp
virtual bool equivalent(const error_code& code, int condition) const noexcept;
```

*Returns:* `true` if, for the category of error represented by `*this`,
`code` is considered equivalent to `condition`; otherwise, `false`.

#### Error category objects <a id="syserr.errcat.objects">[[syserr.errcat.objects]]</a>

``` cpp
const error_category& generic_category() noexcept;
```

*Returns:* A reference to an object of a type derived from class
`error_category`. All calls to this function shall return references to
the same object.

*Remarks:* The object’s `default_error_condition` and `equivalent`
virtual functions shall behave as specified for the class
`error_category`. The object’s `name` virtual function shall return a
pointer to the string `"generic"`.

``` cpp
const error_category& system_category() noexcept;
```

*Returns:* A reference to an object of a type derived from class
`error_category`. All calls to this function shall return references to
the same object.

*Remarks:* The object’s `equivalent` virtual functions shall behave as
specified for class `error_category`. The object’s `name` virtual
function shall return a pointer to the string `"system"`. The object’s
`default_error_condition` virtual function shall behave as follows:

If the argument `ev` corresponds to a POSIX `errno` value `posv`, the
function shall return `error_condition(posv, generic_category())`.
Otherwise, the function shall return
`error_condition(ev, system_category())`. What constitutes
correspondence for any given operating system is unspecified.

[*Note 1*: The number of potential system error codes is large and
unbounded, and some may not correspond to any POSIX `errno` value. Thus
implementations are given latitude in determining
correspondence. — *end note*\]

### Class `error_code` <a id="syserr.errcode">[[syserr.errcode]]</a>

#### Overview <a id="syserr.errcode.overview">[[syserr.errcode.overview]]</a>

The class `error_code` describes an object used to hold error code
values, such as those originating from the operating system or other
low-level application program interfaces.

[*Note 1*: Class `error_code` is an adjunct to error reporting by
exception. — *end note*\]

``` cpp
namespace std {
  class error_code {
  public:
    // [syserr.errcode.constructors], constructors
    error_code() noexcept;
    error_code(int val, const error_category& cat) noexcept;
    template<class ErrorCodeEnum>
      error_code(ErrorCodeEnum e) noexcept;

    // [syserr.errcode.modifiers], modifiers
    void assign(int val, const error_category& cat) noexcept;
    template<class ErrorCodeEnum>
      error_code& operator=(ErrorCodeEnum e) noexcept;
    void clear() noexcept;

    // [syserr.errcode.observers], observers
    int value() const noexcept;
    const error_category& category() const noexcept;
    error_condition default_error_condition() const noexcept;
    string message() const;
    explicit operator bool() const noexcept;

  private:
    int val_;                   // exposition only
    const error_category* cat_; // exposition only
  };

  // [syserr.errcode.nonmembers], non-member functions
  error_code make_error_code(errc e) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const error_code& ec);
}
```

#### Constructors <a id="syserr.errcode.constructors">[[syserr.errcode.constructors]]</a>

``` cpp
error_code() noexcept;
```

*Ensures:* `val_ == 0` and `cat_ == &system_category()`.

``` cpp
error_code(int val, const error_category& cat) noexcept;
```

*Ensures:* `val_ == val` and `cat_ == &cat`.

``` cpp
template<class ErrorCodeEnum>
  error_code(ErrorCodeEnum e) noexcept;
```

*Constraints:* `is_error_code_enum_v<ErrorCodeEnum>` is `true`.

*Ensures:* `*this == make_error_code(e)`.

#### Modifiers <a id="syserr.errcode.modifiers">[[syserr.errcode.modifiers]]</a>

``` cpp
void assign(int val, const error_category& cat) noexcept;
```

*Ensures:* `val_ == val` and `cat_ == &cat`.

``` cpp
template<class ErrorCodeEnum>
  error_code& operator=(ErrorCodeEnum e) noexcept;
```

*Constraints:* `is_error_code_enum_v<ErrorCodeEnum>` is `true`.

*Ensures:* `*this == make_error_code(e)`.

*Returns:* `*this`.

``` cpp
void clear() noexcept;
```

*Ensures:* `value() == 0` and `category() == system_category()`.

#### Observers <a id="syserr.errcode.observers">[[syserr.errcode.observers]]</a>

``` cpp
int value() const noexcept;
```

*Returns:* `val_`.

``` cpp
const error_category& category() const noexcept;
```

*Returns:* `*cat_`.

``` cpp
error_condition default_error_condition() const noexcept;
```

*Returns:* `category().default_error_condition(value())`.

``` cpp
string message() const;
```

*Returns:* `category().message(value())`.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `value() != 0`.

#### Non-member functions <a id="syserr.errcode.nonmembers">[[syserr.errcode.nonmembers]]</a>

``` cpp
error_code make_error_code(errc e) noexcept;
```

*Returns:* `error_code(static_cast<int>(e), generic_category())`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>& operator<<(basic_ostream<charT, traits>& os, const error_code& ec);
```

*Effects:* Equivalent to:
`return os << ec.category().name() << ’:’ << ec.value();`

### Class `error_condition` <a id="syserr.errcondition">[[syserr.errcondition]]</a>

#### Overview <a id="syserr.errcondition.overview">[[syserr.errcondition.overview]]</a>

The class `error_condition` describes an object used to hold values
identifying error conditions.

[*Note 1*: `error_condition` values are portable abstractions, while
`error_code` values [[syserr.errcode]] are implementation
specific. — *end note*\]

``` cpp
namespace std {
  class error_condition {
  public:
    // [syserr.errcondition.constructors], constructors
    error_condition() noexcept;
    error_condition(int val, const error_category& cat) noexcept;
    template<class ErrorConditionEnum>
      error_condition(ErrorConditionEnum e) noexcept;

    // [syserr.errcondition.modifiers], modifiers
    void assign(int val, const error_category& cat) noexcept;
    template<class ErrorConditionEnum>
      error_condition& operator=(ErrorConditionEnum e) noexcept;
    void clear() noexcept;

    // [syserr.errcondition.observers], observers
    int value() const noexcept;
    const error_category& category() const noexcept;
    string message() const;
    explicit operator bool() const noexcept;

  private:
    int val_;                   // exposition only
    const error_category* cat_; // exposition only
  };
}
```

#### Constructors <a id="syserr.errcondition.constructors">[[syserr.errcondition.constructors]]</a>

``` cpp
error_condition() noexcept;
```

*Ensures:* `val_ == 0` and `cat_ == &generic_category()`.

``` cpp
error_condition(int val, const error_category& cat) noexcept;
```

*Ensures:* `val_ == val` and `cat_ == &cat`.

``` cpp
template<class ErrorConditionEnum>
  error_condition(ErrorConditionEnum e) noexcept;
```

*Constraints:* `is_error_condition_enum_v<ErrorConditionEnum>` is
`true`.

*Ensures:* `*this == make_error_condition(e)`.

#### Modifiers <a id="syserr.errcondition.modifiers">[[syserr.errcondition.modifiers]]</a>

``` cpp
void assign(int val, const error_category& cat) noexcept;
```

*Ensures:* `val_ == val` and `cat_ == &cat`.

``` cpp
template<class ErrorConditionEnum>
  error_condition& operator=(ErrorConditionEnum e) noexcept;
```

*Constraints:* `is_error_condition_enum_v<ErrorConditionEnum>` is
`true`.

*Ensures:* `*this == make_error_condition(e)`.

*Returns:* `*this`.

``` cpp
void clear() noexcept;
```

*Ensures:* `value() == 0` and `category() == generic_category()`.

#### Observers <a id="syserr.errcondition.observers">[[syserr.errcondition.observers]]</a>

``` cpp
int value() const noexcept;
```

*Returns:* `val_`.

``` cpp
const error_category& category() const noexcept;
```

*Returns:* `*cat_`.

``` cpp
string message() const;
```

*Returns:* `category().message(value())`.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `value() != 0`.

#### Non-member functions <a id="syserr.errcondition.nonmembers">[[syserr.errcondition.nonmembers]]</a>

``` cpp
error_condition make_error_condition(errc e) noexcept;
```

*Returns:* `error_condition(static_cast<int>(e), generic_category())`.

### Comparison functions <a id="syserr.compare">[[syserr.compare]]</a>

``` cpp
bool operator==(const error_code& lhs, const error_code& rhs) noexcept;
```

*Returns:*

``` cpp
lhs.category() == rhs.category() && lhs.value() == rhs.value()
```

``` cpp
bool operator==(const error_code& lhs, const error_condition& rhs) noexcept;
```

*Returns:*

``` cpp
lhs.category().equivalent(lhs.value(), rhs) || rhs.category().equivalent(lhs, rhs.value())
```

``` cpp
bool operator==(const error_condition& lhs, const error_condition& rhs) noexcept;
```

*Returns:*

``` cpp
lhs.category() == rhs.category() && lhs.value() == rhs.value()
```

``` cpp
strong_ordering operator<=>(const error_code& lhs, const error_code& rhs) noexcept;
```

*Effects:* Equivalent to:

``` cpp
if (auto c = lhs.category() <=> rhs.category(); c != 0) return c;
return lhs.value() <=> rhs.value();
```

``` cpp
strong_ordering operator<=>(const error_condition& lhs, const error_condition& rhs) noexcept;
```

*Returns:*

``` cpp
if (auto c = lhs.category() <=> rhs.category(); c != 0) return c;
return lhs.value() <=> rhs.value();
```

### System error hash support <a id="syserr.hash">[[syserr.hash]]</a>

``` cpp
template<> struct hash<error_code>;
template<> struct hash<error_condition>;
```

The specializations are enabled [[unord.hash]].

### Class `system_error` <a id="syserr.syserr">[[syserr.syserr]]</a>

#### Overview <a id="syserr.syserr.overview">[[syserr.syserr.overview]]</a>

The class `system_error` describes an exception object used to report
error conditions that have an associated error code. Such error
conditions typically originate from the operating system or other
low-level application program interfaces.

[*Note 1*: If an error represents an out-of-memory condition,
implementations are encouraged to throw an exception object of type
`bad_alloc` [[bad.alloc]] rather than `system_error`. — *end note*\]

``` cpp
namespace std {
  class system_error : public runtime_error {
  public:
    system_error(error_code ec, const string& what_arg);
    system_error(error_code ec, const char* what_arg);
    system_error(error_code ec);
    system_error(int ev, const error_category& ecat, const string& what_arg);
    system_error(int ev, const error_category& ecat, const char* what_arg);
    system_error(int ev, const error_category& ecat);
    const error_code& code() const noexcept;
    const char* what() const noexcept override;
  };
}
```

#### Members <a id="syserr.syserr.members">[[syserr.syserr.members]]</a>

``` cpp
system_error(error_code ec, const string& what_arg);
```

*Ensures:* `code() == ec` and
`string_view(what()).find(what_arg.c_str()) != string_view::npos`.

``` cpp
system_error(error_code ec, const char* what_arg);
```

*Ensures:* `code() == ec` and
`string_view(what()).find(what_arg) != string_view::npos`.

``` cpp
system_error(error_code ec);
```

*Ensures:* `code() == ec`.

``` cpp
system_error(int ev, const error_category& ecat, const string& what_arg);
```

*Ensures:*

`code() == error_code(ev, ecat)` and
`string_view(what()).find(what_arg.c_str()) != string_view::npos`.

``` cpp
system_error(int ev, const error_category& ecat, const char* what_arg);
```

*Ensures:*

`code() == error_code(ev, ecat)` and
`string_view(what()).find(what_arg) != string_view::npos`.

``` cpp
system_error(int ev, const error_category& ecat);
```

*Ensures:* `code() == error_code(ev, ecat)`.

``` cpp
const error_code& code() const noexcept;
```

*Returns:* `ec` or `error_code(ev, ecat)`, from the constructor, as
appropriate.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An NTBS incorporating the arguments supplied in the
constructor.

[*Note 1*: The returned NTBS might be the contents of
`what_arg + ": " + code.message()`. — *end note*\]

<!-- Section link definitions -->
[assertions]: #assertions
[assertions.assert]: #assertions.assert
[cassert.syn]: #cassert.syn
[cerrno.syn]: #cerrno.syn
[diagnostics]: #diagnostics
[diagnostics.general]: #diagnostics.general
[domain.error]: #domain.error
[errno]: #errno
[invalid.argument]: #invalid.argument
[length.error]: #length.error
[logic.error]: #logic.error
[out.of.range]: #out.of.range
[overflow.error]: #overflow.error
[range.error]: #range.error
[runtime.error]: #runtime.error
[std.exceptions]: #std.exceptions
[stdexcept.syn]: #stdexcept.syn
[syserr]: #syserr
[syserr.compare]: #syserr.compare
[syserr.errcat]: #syserr.errcat
[syserr.errcat.derived]: #syserr.errcat.derived
[syserr.errcat.nonvirtuals]: #syserr.errcat.nonvirtuals
[syserr.errcat.objects]: #syserr.errcat.objects
[syserr.errcat.overview]: #syserr.errcat.overview
[syserr.errcat.virtuals]: #syserr.errcat.virtuals
[syserr.errcode]: #syserr.errcode
[syserr.errcode.constructors]: #syserr.errcode.constructors
[syserr.errcode.modifiers]: #syserr.errcode.modifiers
[syserr.errcode.nonmembers]: #syserr.errcode.nonmembers
[syserr.errcode.observers]: #syserr.errcode.observers
[syserr.errcode.overview]: #syserr.errcode.overview
[syserr.errcondition]: #syserr.errcondition
[syserr.errcondition.constructors]: #syserr.errcondition.constructors
[syserr.errcondition.modifiers]: #syserr.errcondition.modifiers
[syserr.errcondition.nonmembers]: #syserr.errcondition.nonmembers
[syserr.errcondition.observers]: #syserr.errcondition.observers
[syserr.errcondition.overview]: #syserr.errcondition.overview
[syserr.hash]: #syserr.hash
[syserr.syserr]: #syserr.syserr
[syserr.syserr.members]: #syserr.syserr.members
[syserr.syserr.overview]: #syserr.syserr.overview
[system.error.syn]: #system.error.syn
[underflow.error]: #underflow.error

<!-- Link reference definitions -->
[assertions]: #assertions
[bad.alloc]: support.md#bad.alloc
[comparisons.three.way]: utilities.md#comparisons.three.way
[conv]: expr.md#conv
[defns.const.subexpr]: #defns.const.subexpr
[diagnostics.summary]: #diagnostics.summary
[errno]: #errno
[res.on.exception.handling]: library.md#res.on.exception.handling
[std.exceptions]: #std.exceptions
[syserr]: #syserr
[syserr.errcat]: #syserr.errcat
[syserr.errcode]: #syserr.errcode
[unord.hash]: utilities.md#unord.hash
