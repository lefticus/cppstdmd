# Time library <a id="time">[[time]]</a>

## General <a id="time.general">[[time.general]]</a>

This Clause describes the chrono library [[time.syn]] and various C
functions [[ctime.syn]] that provide generally useful time utilities, as
summarized in [[time.summary]].

**Table: Time library summary**

| Subclause          |                             | Header     |
| ------------------ | --------------------------- | ---------- |
| [[time.clock.req]] | Cpp17Clock requirements     |            |
| [[time.traits]]    | Time-related traits         | `<chrono>` |
| [[time.duration]]  | Class template `duration`   |            |
| [[time.point]]     | Class template `time_point` |            |
| [[time.clock]]     | Clocks                      |            |
| [[time.cal]]       | Civil calendar              |            |
| [[time.hms]]       | Class template `hh_mm_ss`   |            |
| [[time.12]]        | 12/24 hour functions        |            |
| [[time.zone]]      | Time zones                  |            |
| [[time.format]]    | Formatting                  |            |
| [[time.parse]]     | Parsing                     |            |
| [[ctime.syn]]      | C library time utilities    | `<ctime>`  |


Let *STATICALLY-WIDEN*`<charT>("...")` be `"..."` if `charT` is `char`
and `L"..."` if `charT` is `wchar_t`.

## Header `<chrono>` synopsis <a id="time.syn">[[time.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std::chrono {
  // [time.duration], class template duration
  template<class Rep, class Period = ratio<1>> class duration;

  // [time.point], class template time_point
  template<class Clock, class Duration = typename Clock::duration> class time_point;
}

namespace std {
  // [time.traits.specializations], common_type specializations
  template<class Rep1, class Period1, class Rep2, class Period2>
    struct common_type<chrono::duration<Rep1, Period1>,
                       chrono::duration<Rep2, Period2>>;

  template<class Clock, class Duration1, class Duration2>
    struct common_type<chrono::time_point<Clock, Duration1>,
                       chrono::time_point<Clock, Duration2>>;
}

namespace std::chrono {
  // [time.traits], customization traits
  template<class Rep> struct treat_as_floating_point;
  template<class Rep>
    constexpr bool treat_as_floating_point_v = treat_as_floating_point<Rep>::value;

  template<class Rep> struct duration_values;

  template<class T> struct is_clock;
  template<class T> constexpr bool is_clock_v = is_clock<T>::value;

  // [time.duration.nonmember], duration arithmetic
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
      operator+(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
      operator-(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period, class Rep2>
    constexpr duration<common_type_t<Rep1, Rep2>, Period>
      operator*(const duration<Rep1, Period>& d, const Rep2& s);
  template<class Rep1, class Rep2, class Period>
    constexpr duration<common_type_t<Rep1, Rep2>, Period>
      operator*(const Rep1& s, const duration<Rep2, Period>& d);
  template<class Rep1, class Period, class Rep2>
    constexpr duration<common_type_t<Rep1, Rep2>, Period>
      operator/(const duration<Rep1, Period>& d, const Rep2& s);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr common_type_t<Rep1, Rep2>
      operator/(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period, class Rep2>
    constexpr duration<common_type_t<Rep1, Rep2>, Period>
      operator%(const duration<Rep1, Period>& d, const Rep2& s);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
      operator%(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);

  // [time.duration.comparisons], duration comparisons
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator==(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator< (const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator> (const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator<=(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator>=(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Rep2, class Period2>
    requires see below
    constexpr auto operator<=>(const duration<Rep1, Period1>& lhs,
                               const duration<Rep2, Period2>& rhs);

  // [time.duration.cast], conversions
  template<class ToDuration, class Rep, class Period>
    constexpr ToDuration duration_cast(const duration<Rep, Period>& d);
  template<class ToDuration, class Rep, class Period>
    constexpr ToDuration floor(const duration<Rep, Period>& d);
  template<class ToDuration, class Rep, class Period>
    constexpr ToDuration ceil(const duration<Rep, Period>& d);
  template<class ToDuration, class Rep, class Period>
    constexpr ToDuration round(const duration<Rep, Period>& d);

  // [time.duration.io], duration I/O
  template<class charT, class traits, class Rep, class Period>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os,
                 const duration<Rep, Period>& d);
  template<class charT, class traits, class Rep, class Period, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  duration<Rep, Period>& d,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // convenience typedefs
  using nanoseconds  = duration<signed integer type of at least 64 bits, nano>;
  using microseconds = duration<signed integer type of at least 55 bits, micro>;
  using milliseconds = duration<signed integer type of at least 45 bits, milli>;
  using seconds      = duration<signed integer type of at least 35 bits>;
  using minutes      = duration<signed integer type of at least 29 bits, ratio<  60>>;
  using hours        = duration<signed integer type of at least 23 bits, ratio<3600>>;
  using days         = duration<signed integer type of at least 25 bits,
                                ratio_multiply<ratio<24>, hours::period>>;
  using weeks        = duration<signed integer type of at least 22 bits,
                                ratio_multiply<ratio<7>, days::period>>;
  using years        = duration<signed integer type of at least 17 bits,
                                ratio_multiply<ratio<146097, 400>, days::period>>;
  using months       = duration<signed integer type of at least 20 bits,
                                ratio_divide<years::period, ratio<12>>>;

  // [time.point.nonmember], time_point arithmetic
  template<class Clock, class Duration1, class Rep2, class Period2>
    constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
      operator+(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
  template<class Rep1, class Period1, class Clock, class Duration2>
    constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
      operator+(const duration<Rep1, Period1>& lhs, const time_point<Clock, Duration2>& rhs);
  template<class Clock, class Duration1, class Rep2, class Period2>
    constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
      operator-(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
  template<class Clock, class Duration1, class Duration2>
    constexpr common_type_t<Duration1, Duration2>
      operator-(const time_point<Clock, Duration1>& lhs,
                const time_point<Clock, Duration2>& rhs);

  // [time.point.comparisons], time_point comparisons
  template<class Clock, class Duration1, class Duration2>
     constexpr bool operator==(const time_point<Clock, Duration1>& lhs,
                               const time_point<Clock, Duration2>& rhs);
  template<class Clock, class Duration1, class Duration2>
     constexpr bool operator< (const time_point<Clock, Duration1>& lhs,
                               const time_point<Clock, Duration2>& rhs);
  template<class Clock, class Duration1, class Duration2>
     constexpr bool operator> (const time_point<Clock, Duration1>& lhs,
                               const time_point<Clock, Duration2>& rhs);
  template<class Clock, class Duration1, class Duration2>
     constexpr bool operator<=(const time_point<Clock, Duration1>& lhs,
                               const time_point<Clock, Duration2>& rhs);
  template<class Clock, class Duration1, class Duration2>
     constexpr bool operator>=(const time_point<Clock, Duration1>& lhs,
                               const time_point<Clock, Duration2>& rhs);
  template<class Clock, class Duration1, three_way_comparable_with<Duration1> Duration2>
     constexpr auto operator<=>(const time_point<Clock, Duration1>& lhs,
                                const time_point<Clock, Duration2>& rhs);

  // [time.point.cast], conversions
  template<class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration>
      time_point_cast(const time_point<Clock, Duration>& t);
  template<class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration> floor(const time_point<Clock, Duration>& tp);
  template<class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration> ceil(const time_point<Clock, Duration>& tp);
  template<class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration> round(const time_point<Clock, Duration>& tp);

  // [time.duration.alg], specialized algorithms
  template<class Rep, class Period>
    constexpr duration<Rep, Period> abs(duration<Rep, Period> d);

  // [time.clock.system], class system_clock
  class system_clock;

  template<class Duration>
    using sys_time  = time_point<system_clock, Duration>;
  using sys_seconds = sys_time<seconds>;
  using sys_days    = sys_time<days>;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const sys_time<Duration>& tp);

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const sys_days& dp);

  template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  sys_time<Duration>& tp,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.clock.utc], class utc_clock
  class utc_clock;

  template<class Duration>
    using utc_time  = time_point<utc_clock, Duration>;
  using utc_seconds = utc_time<seconds>;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const utc_time<Duration>& t);
  template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  utc_time<Duration>& tp,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  struct leap_second_info;

  template<class Duration>
    leap_second_info get_leap_second_info(const utc_time<Duration>& ut);

  // [time.clock.tai], class tai_clock
  class tai_clock;

  template<class Duration>
    using tai_time  = time_point<tai_clock, Duration>;
  using tai_seconds = tai_time<seconds>;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const tai_time<Duration>& t);
  template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  tai_time<Duration>& tp,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.clock.gps], class gps_clock
  class gps_clock;

  template<class Duration>
    using gps_time  = time_point<gps_clock, Duration>;
  using gps_seconds = gps_time<seconds>;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const gps_time<Duration>& t);
  template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  gps_time<Duration>& tp,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.clock.file], type file_clock
  using file_clock = see below;

  template<class Duration>
    using file_time = time_point<file_clock, Duration>;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const file_time<Duration>& tp);
  template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  file_time<Duration>& tp,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.clock.steady], class steady_clock
  class steady_clock;

  // [time.clock.hires], class high_resolution_clock
  class high_resolution_clock;

  // [time.clock.local], local time
  struct local_t {};
  template<class Duration>
    using local_time  = time_point<local_t, Duration>;
  using local_seconds = local_time<seconds>;
  using local_days    = local_time<days>;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const local_time<Duration>& tp);
  template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  local_time<Duration>& tp,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.clock.cast], time_point conversions
  template<class DestClock, class SourceClock>
    struct clock_time_conversion;

  template<class DestClock, class SourceClock, class Duration>
    auto clock_cast(const time_point<SourceClock, Duration>& t);

  // [time.cal.last], class last_spec
  struct last_spec;

  // [time.cal.day], class day
  class day;

  constexpr bool operator==(const day& x, const day& y) noexcept;
  constexpr strong_ordering operator<=>(const day& x, const day& y) noexcept;

  constexpr day  operator+(const day&  x, const days& y) noexcept;
  constexpr day  operator+(const days& x, const day&  y) noexcept;
  constexpr day  operator-(const day&  x, const days& y) noexcept;
  constexpr days operator-(const day&  x, const day&  y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const day& d);
  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  day& d, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.month], class month
  class month;

  constexpr bool operator==(const month& x, const month& y) noexcept;
  constexpr strong_ordering operator<=>(const month& x, const month& y) noexcept;

  constexpr month  operator+(const month&  x, const months& y) noexcept;
  constexpr month  operator+(const months& x,  const month& y) noexcept;
  constexpr month  operator-(const month&  x, const months& y) noexcept;
  constexpr months operator-(const month&  x,  const month& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const month& m);
  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  month& m, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.year], class year
  class year;

  constexpr bool operator==(const year& x, const year& y) noexcept;
  constexpr strong_ordering operator<=>(const year& x, const year& y) noexcept;

  constexpr year  operator+(const year&  x, const years& y) noexcept;
  constexpr year  operator+(const years& x, const year&  y) noexcept;
  constexpr year  operator-(const year&  x, const years& y) noexcept;
  constexpr years operator-(const year&  x, const year&  y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const year& y);

  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  year& y, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.wd], class weekday
  class weekday;

  constexpr bool operator==(const weekday& x, const weekday& y) noexcept;

  constexpr weekday operator+(const weekday& x, const days&    y) noexcept;
  constexpr weekday operator+(const days&    x, const weekday& y) noexcept;
  constexpr weekday operator-(const weekday& x, const days&    y) noexcept;
  constexpr days    operator-(const weekday& x, const weekday& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const weekday& wd);

  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  weekday& wd, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.wdidx], class weekday_indexed
  class weekday_indexed;

  constexpr bool operator==(const weekday_indexed& x, const weekday_indexed& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const weekday_indexed& wdi);

  // [time.cal.wdlast], class weekday_last
  class weekday_last;

  constexpr bool operator==(const weekday_last& x, const weekday_last& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const weekday_last& wdl);

  // [time.cal.md], class month_day
  class month_day;

  constexpr bool operator==(const month_day& x, const month_day& y) noexcept;
  constexpr strong_ordering operator<=>(const month_day& x, const month_day& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const month_day& md);

  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  month_day& md, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.mdlast], class month_day_last
  class month_day_last;

  constexpr bool operator==(const month_day_last& x, const month_day_last& y) noexcept;
  constexpr strong_ordering operator<=>(const month_day_last& x,
                                        const month_day_last& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const month_day_last& mdl);

  // [time.cal.mwd], class month_weekday
  class month_weekday;

  constexpr bool operator==(const month_weekday& x, const month_weekday& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const month_weekday& mwd);

  // [time.cal.mwdlast], class month_weekday_last
  class month_weekday_last;

  constexpr bool operator==(const month_weekday_last& x, const month_weekday_last& y) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const month_weekday_last& mwdl);

  // [time.cal.ym], class year_month
  class year_month;

  constexpr bool operator==(const year_month& x, const year_month& y) noexcept;
  constexpr strong_ordering operator<=>(const year_month& x, const year_month& y) noexcept;

  constexpr year_month operator+(const year_month& ym, const months& dm) noexcept;
  constexpr year_month operator+(const months& dm, const year_month& ym) noexcept;
  constexpr year_month operator-(const year_month& ym, const months& dm) noexcept;
  constexpr months operator-(const year_month& x, const year_month& y) noexcept;
  constexpr year_month operator+(const year_month& ym, const years& dy) noexcept;
  constexpr year_month operator+(const years& dy, const year_month& ym) noexcept;
  constexpr year_month operator-(const year_month& ym, const years& dy) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const year_month& ym);

  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  year_month& ym, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.ymd], class year_month_day
  class year_month_day;

  constexpr bool operator==(const year_month_day& x, const year_month_day& y) noexcept;
  constexpr strong_ordering operator<=>(const year_month_day& x,
                                        const year_month_day& y) noexcept;

  constexpr year_month_day operator+(const year_month_day& ymd, const months& dm) noexcept;
  constexpr year_month_day operator+(const months& dm, const year_month_day& ymd) noexcept;
  constexpr year_month_day operator+(const year_month_day& ymd, const years& dy) noexcept;
  constexpr year_month_day operator+(const years& dy, const year_month_day& ymd) noexcept;
  constexpr year_month_day operator-(const year_month_day& ymd, const months& dm) noexcept;
  constexpr year_month_day operator-(const year_month_day& ymd, const years& dy) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const year_month_day& ymd);

  template<class charT, class traits, class Alloc = allocator<charT>>
    basic_istream<charT, traits>&
      from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                  year_month_day& ymd,
                  basic_string<charT, traits, Alloc>* abbrev = nullptr,
                  minutes* offset = nullptr);

  // [time.cal.ymdlast], class year_month_day_last
  class year_month_day_last;

  constexpr bool operator==(const year_month_day_last& x,
                            const year_month_day_last& y) noexcept;
  constexpr strong_ordering operator<=>(const year_month_day_last& x,
                                        const year_month_day_last& y) noexcept;

  constexpr year_month_day_last
    operator+(const year_month_day_last& ymdl, const months& dm) noexcept;
  constexpr year_month_day_last
    operator+(const months& dm, const year_month_day_last& ymdl) noexcept;
  constexpr year_month_day_last
    operator+(const year_month_day_last& ymdl, const years& dy) noexcept;
  constexpr year_month_day_last
    operator+(const years& dy, const year_month_day_last& ymdl) noexcept;
  constexpr year_month_day_last
    operator-(const year_month_day_last& ymdl, const months& dm) noexcept;
  constexpr year_month_day_last
    operator-(const year_month_day_last& ymdl, const years& dy) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const year_month_day_last& ymdl);

  // [time.cal.ymwd], class year_month_weekday
  class year_month_weekday;

  constexpr bool operator==(const year_month_weekday& x,
                            const year_month_weekday& y) noexcept;

  constexpr year_month_weekday
    operator+(const year_month_weekday& ymwd, const months& dm) noexcept;
  constexpr year_month_weekday
    operator+(const months& dm, const year_month_weekday& ymwd) noexcept;
  constexpr year_month_weekday
    operator+(const year_month_weekday& ymwd, const years& dy) noexcept;
  constexpr year_month_weekday
    operator+(const years& dy, const year_month_weekday& ymwd) noexcept;
  constexpr year_month_weekday
    operator-(const year_month_weekday& ymwd, const months& dm) noexcept;
  constexpr year_month_weekday
    operator-(const year_month_weekday& ymwd, const years& dy) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const year_month_weekday& ymwd);

  // [time.cal.ymwdlast], class year_month_weekday_last
  class year_month_weekday_last;

  constexpr bool operator==(const year_month_weekday_last& x,
                            const year_month_weekday_last& y) noexcept;

  constexpr year_month_weekday_last
    operator+(const year_month_weekday_last& ymwdl, const months& dm) noexcept;
  constexpr year_month_weekday_last
    operator+(const months& dm, const year_month_weekday_last& ymwdl) noexcept;
  constexpr year_month_weekday_last
    operator+(const year_month_weekday_last& ymwdl, const years& dy) noexcept;
  constexpr year_month_weekday_last
    operator+(const years& dy, const year_month_weekday_last& ymwdl) noexcept;
  constexpr year_month_weekday_last
    operator-(const year_month_weekday_last& ymwdl, const months& dm) noexcept;
  constexpr year_month_weekday_last
    operator-(const year_month_weekday_last& ymwdl, const years& dy) noexcept;

  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const year_month_weekday_last& ymwdl);

  // [time.cal.operators], civil calendar conventional syntax operators
  constexpr year_month
    operator/(const year& y, const month& m) noexcept;
  constexpr year_month
    operator/(const year& y, int m) noexcept;
  constexpr month_day
    operator/(const month& m, const day& d) noexcept;
  constexpr month_day
    operator/(const month& m, int d) noexcept;
  constexpr month_day
    operator/(int m, const day& d) noexcept;
  constexpr month_day
    operator/(const day& d, const month& m) noexcept;
  constexpr month_day
    operator/(const day& d, int m) noexcept;
  constexpr month_day_last
    operator/(const month& m, last_spec) noexcept;
  constexpr month_day_last
    operator/(int m, last_spec) noexcept;
  constexpr month_day_last
    operator/(last_spec, const month& m) noexcept;
  constexpr month_day_last
    operator/(last_spec, int m) noexcept;
  constexpr month_weekday
    operator/(const month& m, const weekday_indexed& wdi) noexcept;
  constexpr month_weekday
    operator/(int m, const weekday_indexed& wdi) noexcept;
  constexpr month_weekday
    operator/(const weekday_indexed& wdi, const month& m) noexcept;
  constexpr month_weekday
    operator/(const weekday_indexed& wdi, int m) noexcept;
  constexpr month_weekday_last
    operator/(const month& m, const weekday_last& wdl) noexcept;
  constexpr month_weekday_last
    operator/(int m, const weekday_last& wdl) noexcept;
  constexpr month_weekday_last
    operator/(const weekday_last& wdl, const month& m) noexcept;
  constexpr month_weekday_last
    operator/(const weekday_last& wdl, int m) noexcept;
  constexpr year_month_day
    operator/(const year_month& ym, const day& d) noexcept;
  constexpr year_month_day
    operator/(const year_month& ym, int d) noexcept;
  constexpr year_month_day
    operator/(const year& y, const month_day& md) noexcept;
  constexpr year_month_day
    operator/(int y, const month_day& md) noexcept;
  constexpr year_month_day
    operator/(const month_day& md, const year& y) noexcept;
  constexpr year_month_day
    operator/(const month_day& md, int y) noexcept;
  constexpr year_month_day_last
    operator/(const year_month& ym, last_spec) noexcept;
  constexpr year_month_day_last
    operator/(const year& y, const month_day_last& mdl) noexcept;
  constexpr year_month_day_last
    operator/(int y, const month_day_last& mdl) noexcept;
  constexpr year_month_day_last
    operator/(const month_day_last& mdl, const year& y) noexcept;
  constexpr year_month_day_last
    operator/(const month_day_last& mdl, int y) noexcept;
  constexpr year_month_weekday
    operator/(const year_month& ym, const weekday_indexed& wdi) noexcept;
  constexpr year_month_weekday
    operator/(const year& y, const month_weekday& mwd) noexcept;
  constexpr year_month_weekday
    operator/(int y, const month_weekday& mwd) noexcept;
  constexpr year_month_weekday
    operator/(const month_weekday& mwd, const year& y) noexcept;
  constexpr year_month_weekday
    operator/(const month_weekday& mwd, int y) noexcept;
  constexpr year_month_weekday_last
    operator/(const year_month& ym, const weekday_last& wdl) noexcept;
  constexpr year_month_weekday_last
    operator/(const year& y, const month_weekday_last& mwdl) noexcept;
  constexpr year_month_weekday_last
    operator/(int y, const month_weekday_last& mwdl) noexcept;
  constexpr year_month_weekday_last
    operator/(const month_weekday_last& mwdl, const year& y) noexcept;
  constexpr year_month_weekday_last
    operator/(const month_weekday_last& mwdl, int y) noexcept;

  // [time.hms], class template hh_mm_ss
  template<class Duration> class hh_mm_ss;

  template<class charT, class traits, class Duration>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const hh_mm_ss<Duration>& hms);

  // [time.12], 12/24 hour functions
  constexpr bool is_am(const hours& h) noexcept;
  constexpr bool is_pm(const hours& h) noexcept;
  constexpr hours make12(const hours& h) noexcept;
  constexpr hours make24(const hours& h, bool is_pm) noexcept;

  // [time.zone.db], time zone database
  struct tzdb;
  class tzdb_list;

  // [time.zone.db.access], time zone database access
  const tzdb& get_tzdb();
  tzdb_list& get_tzdb_list();
  const time_zone* locate_zone(string_view tz_name);
  const time_zone* current_zone();

  // [time.zone.db.remote], remote time zone database support
  const tzdb& reload_tzdb();
  string remote_version();

  // [time.zone.exception], exception classes
  class nonexistent_local_time;
  class ambiguous_local_time;

  // [time.zone.info], information classes
  struct sys_info;
  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const sys_info& si);

  struct local_info;
  template<class charT, class traits>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const local_info& li);

  // [time.zone.timezone], class time_zone
  enum class choose {earliest, latest};
  class time_zone;

  bool operator==(const time_zone& x, const time_zone& y) noexcept;
  strong_ordering operator<=>(const time_zone& x, const time_zone& y) noexcept;

  // [time.zone.zonedtraits], class template zoned_traits
  template<class T> struct zoned_traits;

  // [time.zone.zonedtime], class template zoned_time
  template<class Duration, class TimeZonePtr = const time_zone*> class zoned_time;

  using zoned_seconds = zoned_time<seconds>;

  template<class Duration1, class Duration2, class TimeZonePtr>
    bool operator==(const zoned_time<Duration1, TimeZonePtr>& x,
                    const zoned_time<Duration2, TimeZonePtr>& y);

  template<class charT, class traits, class Duration, class TimeZonePtr>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os,
                 const zoned_time<Duration, TimeZonePtr>& t);

  // [time.zone.leap], leap second support
  class leap_second;

  constexpr bool operator==(const leap_second& x, const leap_second& y);
  constexpr strong_ordering operator<=>(const leap_second& x, const leap_second& y);

  template<class Duration>
    constexpr bool operator==(const leap_second& x, const sys_time<Duration>& y);
  template<class Duration>
    constexpr bool operator< (const leap_second& x, const sys_time<Duration>& y);
  template<class Duration>
    constexpr bool operator< (const sys_time<Duration>& x, const leap_second& y);
  template<class Duration>
    constexpr bool operator> (const leap_second& x, const sys_time<Duration>& y);
  template<class Duration>
    constexpr bool operator> (const sys_time<Duration>& x, const leap_second& y);
  template<class Duration>
    constexpr bool operator<=(const leap_second& x, const sys_time<Duration>& y);
  template<class Duration>
    constexpr bool operator<=(const sys_time<Duration>& x, const leap_second& y);
  template<class Duration>
    constexpr bool operator>=(const leap_second& x, const sys_time<Duration>& y);
  template<class Duration>
    constexpr bool operator>=(const sys_time<Duration>& x, const leap_second& y);
  template<class Duration>
    requires three_way_comparable_with<sys_seconds, sys_time<Duration>>
    constexpr auto operator<=>(const leap_second& x, const sys_time<Duration>& y);

  // [time.zone.link], class time_zone_link
  class time_zone_link;

  bool operator==(const time_zone_link& x, const time_zone_link& y);
  strong_ordering operator<=>(const time_zone_link& x, const time_zone_link& y);

  // [time.format], formatting
  template<class Duration> struct local-time-format-t;        // exposition only
  template<class Duration>
    local-time-format-t<Duration>
      local_time_format(local_time<Duration> time, const string* abbrev = nullptr,
                        const seconds* offset_sec = nullptr);
}

namespace std {
  template<class Rep, class Period, class charT>
    struct formatter<chrono::duration<Rep, Period>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::sys_time<Duration>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::utc_time<Duration>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::tai_time<Duration>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::gps_time<Duration>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::file_time<Duration>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::local_time<Duration>, charT>;
  template<class Duration, class charT>
    struct formatter<chrono::local-time-format-t<Duration>, charT>;
  template<class charT> struct formatter<chrono::day, charT>;
  template<class charT> struct formatter<chrono::month, charT>;
  template<class charT> struct formatter<chrono::year, charT>;
  template<class charT> struct formatter<chrono::weekday, charT>;
  template<class charT> struct formatter<chrono::weekday_indexed, charT>;
  template<class charT> struct formatter<chrono::weekday_last, charT>;
  template<class charT> struct formatter<chrono::month_day, charT>;
  template<class charT> struct formatter<chrono::month_day_last, charT>;
  template<class charT> struct formatter<chrono::month_weekday, charT>;
  template<class charT> struct formatter<chrono::month_weekday_last, charT>;
  template<class charT> struct formatter<chrono::year_month, charT>;
  template<class charT> struct formatter<chrono::year_month_day, charT>;
  template<class charT> struct formatter<chrono::year_month_day_last, charT>;
  template<class charT> struct formatter<chrono::year_month_weekday, charT>;
  template<class charT> struct formatter<chrono::year_month_weekday_last, charT>;
  template<class Rep, class Period, class charT>
    struct formatter<chrono::hh_mm_ss<duration<Rep, Period>>, charT>;
  template<class charT> struct formatter<chrono::sys_info, charT>;
  template<class charT> struct formatter<chrono::local_info, charT>;
  template<class Duration, class TimeZonePtr, class charT>
    struct formatter<chrono::zoned_time<Duration, TimeZonePtr>, charT>;
}

namespace std::chrono {
  // [time.parse], parsing
  template<class charT, class Parsable>
    unspecified
     parse(const charT* fmt, Parsable& tp);
  template<class charT, class traits, class Alloc, class Parsable>
    unspecified
      parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp);

  template<class charT, class traits, class Alloc, class Parsable>
    unspecified
      parse(const charT* fmt, Parsable& tp,
            basic_string<charT, traits, Alloc>& abbrev);
  template<class charT, class traits, class Alloc, class Parsable>
    unspecified
      parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp,
            basic_string<charT, traits, Alloc>& abbrev);

  template<class charT, class Parsable>
    unspecified
      parse(const charT* fmt, Parsable& tp, minutes& offset);
  template<class charT, class traits, class Alloc, class Parsable>
    unspecified
      parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp,
            minutes& offset);

  template<class charT, class traits, class Alloc, class Parsable>
    unspecified
      parse(const charT* fmt, Parsable& tp,
            basic_string<charT, traits, Alloc>& abbrev, minutes& offset);
  template<class charT, class traits, class Alloc, class Parsable>
    unspecified
      parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp,
            basic_string<charT, traits, Alloc>& abbrev, minutes& offset);

  // calendrical constants
  inline constexpr last_spec last{};

  inline constexpr weekday Sunday{0};
  inline constexpr weekday Monday{1};
  inline constexpr weekday Tuesday{2};
  inline constexpr weekday Wednesday{3};
  inline constexpr weekday Thursday{4};
  inline constexpr weekday Friday{5};
  inline constexpr weekday Saturday{6};

  inline constexpr month January{1};
  inline constexpr month February{2};
  inline constexpr month March{3};
  inline constexpr month April{4};
  inline constexpr month May{5};
  inline constexpr month June{6};
  inline constexpr month July{7};
  inline constexpr month August{8};
  inline constexpr month September{9};
  inline constexpr month October{10};
  inline constexpr month November{11};
  inline constexpr month December{12};
}

namespace std::inline literals::inline chrono_literals {
  // [time.duration.literals], suffixes for duration literals
  constexpr chrono::hours                                 operator""h(unsigned long long);
  constexpr chrono::duration<unspecified, ratio<3600, 1>> operator""h(long double);

  constexpr chrono::minutes                             operator""min(unsigned long long);
  constexpr chrono::duration<unspecified, ratio<60, 1>> operator""min(long double);

  constexpr chrono::seconds               operator""s(unsigned long long);
  constexpr chrono::duration<unspecified>\itcorr[-1] operator""s(long double);

  constexpr chrono::milliseconds                 operator""ms(unsigned long long);
  constexpr chrono::duration<unspecified, milli> operator""ms(long double);

  constexpr chrono::microseconds                 operator""us(unsigned long long);
  constexpr chrono::duration<unspecified, micro> operator""us(long double);

  constexpr chrono::nanoseconds                 operator""ns(unsigned long long);
  constexpr chrono::duration<unspecified, nano> operator""ns(long double);

  // [time.cal.day.nonmembers], non-member functions
  constexpr chrono::day  operator""d(unsigned long long d) noexcept;

  // [time.cal.year.nonmembers], non-member functions
  constexpr chrono::year operator""y(unsigned long long y) noexcept;
}

namespace std::chrono {
  using namespace literals::chrono_literals;
}
```

## *Cpp17Clock* requirements <a id="time.clock.req">[[time.clock.req]]</a>

A clock is a bundle consisting of a `duration`, a `time_point`, and a
function `now()` to get the current `time_point`. The origin of the
clock’s `time_point` is referred to as the clock’s *epoch*. A clock
shall meet the requirements in [[time.clock]].

In [[time.clock]] `C1` and `C2` denote clock types. `t1` and `t2` are
values returned by `C1::now()` where the call returning `t1` happens
before [[intro.multithread]] the call returning `t2` and both of these
calls occur before `C1::time_point::max()`.

[*Note 1*: This means `C1` did not wrap around between `t1` and
`t2`. — *end note*\]

[*Note 2*: The relative difference in durations between those reported
by a given clock and the SI definition is a measure of the quality of
implementation. — *end note*\]

A type `TC` meets the *Cpp17TrivialClock* requirements if:

- `TC` meets the *Cpp17Clock* requirements,
- the types `TC::rep`, `TC::duration`, and `TC::time_point` meet the
  *Cpp17EqualityComparable* ( [[cpp17.equalitycomparable]]) and
  *Cpp17LessThanComparable* ( [[cpp17.lessthancomparable]]) and
  *Cpp17Swappable* [[swappable.requirements]] requirements and the
  requirements of numeric types [[numeric.requirements]],
  \[*Note 1*: This means, in particular, that operations on these types
  will not throw exceptions. — *end note*\]
- the function `TC::now()` does not throw exceptions, and
- the type `TC::time_point::clock` meets the *Cpp17TrivialClock*
  requirements, recursively.

## Time-related traits <a id="time.traits">[[time.traits]]</a>

### `treat_as_floating_point` <a id="time.traits.is.fp">[[time.traits.is.fp]]</a>

``` cpp
template<class Rep> struct treat_as_floating_point : is_floating_point<Rep> { };
```

The `duration` template uses the `treat_as_floating_point` trait to help
determine if a `duration` object can be converted to another `duration`
with a different tick `period`. If `treat_as_floating_point_v<Rep>` is
`true`, then implicit conversions are allowed among `duration`s.
Otherwise, the implicit convertibility depends on the tick `period`s of
the `duration`s.

[*Note 1*: The intention of this trait is to indicate whether a given
class behaves like a floating-point type, and thus allows division of
one value by another with acceptable loss of precision. If
`treat_as_floating_point_v<Rep>` is `false`, `Rep` will be treated as if
it behaved like an integral type for the purpose of these
conversions. — *end note*\]

### `duration_values` <a id="time.traits.duration.values">[[time.traits.duration.values]]</a>

``` cpp
template<class Rep>
  struct duration_values {
  public:
    static constexpr Rep zero() noexcept;
    static constexpr Rep min() noexcept;
    static constexpr Rep max() noexcept;
  };
```

The `duration` template uses the `duration_values` trait to construct
special values of the duration’s representation (`Rep`). This is done
because the representation can be a class type with behavior that
requires some other implementation to return these special values. In
that case, the author of that class type should specialize
`duration_values` to return the indicated values.

``` cpp
static constexpr Rep zero() noexcept;
```

*Returns:* `Rep(0)`.

[*Note 1*: `Rep(0)` is specified instead of `Rep()` because `Rep()` can
have some other meaning, such as an uninitialized value. — *end note*\]

*Remarks:* The value returned shall be the additive identity.

``` cpp
static constexpr Rep min() noexcept;
```

*Returns:* `numeric_limits<Rep>::lowest()`.

*Remarks:* The value returned shall compare less than or equal to
`zero()`.

``` cpp
static constexpr Rep max() noexcept;
```

*Returns:* `numeric_limits<Rep>::max()`.

*Remarks:* The value returned shall compare greater than `zero()`.

### Specializations of `common_type` <a id="time.traits.specializations">[[time.traits.specializations]]</a>

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  struct common_type<chrono::duration<Rep1, Period1>, chrono::duration<Rep2, Period2>> {
    using type = chrono::duration<common_type_t<Rep1, Rep2>, see below>;
  };
```

The `period` of the `duration` indicated by this specialization of
`common_type` is the greatest common divisor of `Period1` and `Period2`.

[*Note 1*: This can be computed by forming a ratio of the greatest
common divisor of `Period1::num` and `Period2::num` and the least common
multiple of `Period1::den` and `Period2::den`. — *end note*\]

[*Note 2*: The `typedef` name `type` is a synonym for the `duration`
with the largest tick `period` possible where both `duration` arguments
will convert to it without requiring a division operation. The
representation of this type is intended to be able to hold any value
resulting from this conversion with no truncation error, although
floating-point durations can have round-off errors. — *end note*\]

``` cpp
template<class Clock, class Duration1, class Duration2>
  struct common_type<chrono::time_point<Clock, Duration1>, chrono::time_point<Clock, Duration2>> {
    using type = chrono::time_point<Clock, common_type_t<Duration1, Duration2>>;
  };
```

The common type of two `time_point` types is a `time_point` with the
same clock as the two types and the common type of their two
`duration`s.

### Class template `is_clock` <a id="time.traits.is.clock">[[time.traits.is.clock]]</a>

``` cpp
template<class T> struct is_clock;
```

`is_clock` is a *Cpp17UnaryTypeTrait* [[meta.rqmts]] with a base
characteristic of `true_type` if `T` meets the *Cpp17Clock* requirements
[[time.clock.req]], otherwise `false_type`. For the purposes of the
specification of this trait, the extent to which an implementation
determines that a type cannot meet the *Cpp17Clock* requirements is
unspecified, except that as a minimum a type `T` shall not qualify as a
*Cpp17Clock* unless it meets all of the following conditions:

- the *qualified-id*s `T::rep`, `T::period`, `T::duration`, and
  `T::time_point` are valid and each denotes a type [[temp.deduct]],
- the expression `T::is_steady` is well-formed when treated as an
  unevaluated operand [[term.unevaluated.operand]],
- the expression `T::now()` is well-formed when treated as an
  unevaluated operand.

The behavior of a program that adds specializations for `is_clock` is
undefined.

## Class template `duration` <a id="time.duration">[[time.duration]]</a>

### General <a id="time.duration.general">[[time.duration.general]]</a>

A `duration` type measures time between two points in time
(`time_point`s). A `duration` has a representation which holds a count
of ticks and a tick period. The tick period is the amount of time which
occurs from one tick to the next, in units of seconds. It is expressed
as a rational constant using the template `ratio`.

``` cpp
namespace std::chrono {
  template<class Rep, class Period = ratio<1>>
  class duration {
  public:
    using rep    = Rep;
    using period = typename Period::type;

  private:
    rep rep_;       // exposition only

  public:
    // [time.duration.cons], construct/copy/destroy
    constexpr duration() = default;
    template<class Rep2>
      constexpr explicit duration(const Rep2& r);
    template<class Rep2, class Period2>
      constexpr duration(const duration<Rep2, Period2>& d);
    ~duration() = default;
    duration(const duration&) = default;
    duration& operator=(const duration&) = default;

    // [time.duration.observer], observer
    constexpr rep count() const;

    // [time.duration.arithmetic], arithmetic
    constexpr common_type_t<duration> operator+() const;
    constexpr common_type_t<duration> operator-() const;
    constexpr duration& operator++();
    constexpr duration  operator++(int);
    constexpr duration& operator--();
    constexpr duration  operator--(int);

    constexpr duration& operator+=(const duration& d);
    constexpr duration& operator-=(const duration& d);

    constexpr duration& operator*=(const rep& rhs);
    constexpr duration& operator/=(const rep& rhs);
    constexpr duration& operator%=(const rep& rhs);
    constexpr duration& operator%=(const duration& rhs);

    // [time.duration.special], special values
    static constexpr duration zero() noexcept;
    static constexpr duration min() noexcept;
    static constexpr duration max() noexcept;
  };
}
```

`Rep` shall be an arithmetic type or a class emulating an arithmetic
type. If `duration` is instantiated with a `duration` type as the
argument for the template parameter `Rep`, the program is ill-formed.

If `Period` is not a specialization of `ratio`, the program is
ill-formed. If `Period::num` is not positive, the program is ill-formed.

Members of `duration` do not throw exceptions other than those thrown by
the indicated operations on their representations.

The defaulted copy constructor of duration shall be a constexpr function
if and only if the required initialization of the member `rep_` for copy
and move, respectively, would be constexpr-suitable [[dcl.constexpr]].

[*Example 1*:

``` cpp
duration<long, ratio<60>> d0;       // holds a count of minutes using a long
duration<long long, milli> d1;      // holds a count of milliseconds using a long long
duration<double, ratio<1, 30>>  d2; // holds a count with a tick period of $\frac{1}{30}$ of a second
                                    // (30 Hz) using a double
```

— *end example*\]

### Constructors <a id="time.duration.cons">[[time.duration.cons]]</a>

``` cpp
template<class Rep2>
  constexpr explicit duration(const Rep2& r);
```

*Constraints:* `is_convertible_v<const Rep2&, rep>` is `true` and

- `treat_as_floating_point_v<rep>` is `true` or
- `treat_as_floating_point_v<Rep2>` is `false`.

[*Example 1*:

``` cpp
duration<int, milli> d(3);          // OK
duration<int, milli> d(3.5);        // error
```

— *end example*\]

*Effects:* Initializes `rep_` with `r`.

``` cpp
template<class Rep2, class Period2>
  constexpr duration(const duration<Rep2, Period2>& d);
```

*Constraints:* No overflow is induced in the conversion and
`treat_as_floating_point_v<rep>` is `true` or both
`ratio_divide<Period2, period>::den` is `1` and
`treat_as_floating_point_v<Rep2>` is `false`.

[*Note 1*: This requirement prevents implicit truncation error when
converting between integral-based `duration` types. Such a construction
could easily lead to confusion about the value of the
`duration`. — *end note*\]

[*Example 2*:

``` cpp
duration<int, milli> ms(3);
duration<int, micro> us = ms;       // OK
duration<int, milli> ms2 = us;      // error
```

— *end example*\]

*Effects:* Initializes `rep_` with `duration_cast<duration>(d).count()`.

### Observer <a id="time.duration.observer">[[time.duration.observer]]</a>

``` cpp
constexpr rep count() const;
```

*Returns:* `rep_`.

### Arithmetic <a id="time.duration.arithmetic">[[time.duration.arithmetic]]</a>

``` cpp
constexpr common_type_t<duration> operator+() const;
```

*Returns:* `common_type_t<duration>(*this)`.

``` cpp
constexpr common_type_t<duration> operator-() const;
```

*Returns:* `common_type_t<duration>(-rep_)`.

``` cpp
constexpr duration& operator++();
```

*Effects:* Equivalent to: `++rep_`.

*Returns:* `*this`.

``` cpp
constexpr duration operator++(int);
```

*Effects:* Equivalent to: `return duration(rep_++);`

``` cpp
constexpr duration& operator--();
```

*Effects:* Equivalent to: `–rep_`.

*Returns:* `*this`.

``` cpp
constexpr duration operator--(int);
```

*Effects:* Equivalent to: `return duration(rep_--);`

``` cpp
constexpr duration& operator+=(const duration& d);
```

*Effects:* Equivalent to: `rep_ += d.count()`.

*Returns:* `*this`.

``` cpp
constexpr duration& operator-=(const duration& d);
```

*Effects:* Equivalent to: `rep_ -= d.count()`.

*Returns:* `*this`.

``` cpp
constexpr duration& operator*=(const rep& rhs);
```

*Effects:* Equivalent to: `rep_ *= rhs`.

*Returns:* `*this`.

``` cpp
constexpr duration& operator/=(const rep& rhs);
```

*Effects:* Equivalent to: `rep_ /= rhs`.

*Returns:* `*this`.

``` cpp
constexpr duration& operator%=(const rep& rhs);
```

*Effects:* Equivalent to: `rep_ %= rhs`.

*Returns:* `*this`.

``` cpp
constexpr duration& operator%=(const duration& rhs);
```

*Effects:* Equivalent to: `rep_ %= rhs.count()`.

*Returns:* `*this`.

### Special values <a id="time.duration.special">[[time.duration.special]]</a>

``` cpp
static constexpr duration zero() noexcept;
```

*Returns:* `duration(duration_values<rep>::zero())`.

``` cpp
static constexpr duration min() noexcept;
```

*Returns:* `duration(duration_values<rep>::min())`.

``` cpp
static constexpr duration max() noexcept;
```

*Returns:* `duration(duration_values<rep>::max())`.

### Non-member arithmetic <a id="time.duration.nonmember">[[time.duration.nonmember]]</a>

In the function descriptions that follow, unless stated otherwise, let
`CD` represent the return type of the function.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
    operator+(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(CD(lhs).count() + CD(rhs).count())`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator-(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(CD(lhs).count() - CD(rhs).count())`.

``` cpp
template<class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
    operator*(const duration<Rep1, Period>& d, const Rep2& s);
```

*Constraints:*
`is_convertible_v<const Rep2&, common_type_t<Rep1, Rep2>>` is `true`.

*Returns:* `CD(CD(d).count() * s)`.

``` cpp
template<class Rep1, class Rep2, class Period>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
    operator*(const Rep1& s, const duration<Rep2, Period>& d);
```

*Constraints:*
`is_convertible_v<const Rep1&, common_type_t<Rep1, Rep2>>` is `true`.

*Returns:* `d * s`.

``` cpp
template<class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
    operator/(const duration<Rep1, Period>& d, const Rep2& s);
```

*Constraints:*
`is_convertible_v<const Rep2&, common_type_t<Rep1, Rep2>>` is `true` and
`Rep2` is not a specialization of `duration`.

*Returns:* `CD(CD(d).count() / s)`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<Rep1, Rep2>
    operator/(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

Let `CD` be
`common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>`.

*Returns:* `CD(lhs).count() / CD(rhs).count()`.

``` cpp
template<class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
    operator%(const duration<Rep1, Period>& d, const Rep2& s);
```

*Constraints:*
`is_convertible_v<const Rep2&, common_type_t<Rep1, Rep2>>` is `true` and
`Rep2` is not a specialization of `duration`.

*Returns:* `CD(CD(d).count() % s)`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
    operator%(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(CD(lhs).count() % CD(rhs).count())`.

### Comparisons <a id="time.duration.comparisons">[[time.duration.comparisons]]</a>

In the function descriptions that follow, `CT` represents
`common_type_t<A, B>`, where `A` and `B` are the types of the two
arguments to the function.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator==(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs).count() == CT(rhs).count()`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<(const duration<Rep1, Period1>& lhs,
                           const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs).count() < CT(rhs).count()`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>(const duration<Rep1, Period1>& lhs,
                           const duration<Rep2, Period2>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template<class Rep1, class Period1, class Rep2, class Period2>
  requires three_way_comparable<typename CT::rep>
  constexpr auto operator<=>(const duration<Rep1, Period1>& lhs,
                             const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs).count() <=> CT(rhs).count()`.

### Conversions <a id="time.duration.cast">[[time.duration.cast]]</a>

``` cpp
template<class ToDuration, class Rep, class Period>
  constexpr ToDuration duration_cast(const duration<Rep, Period>& d);
```

*Constraints:* `ToDuration` is a specialization of `duration`.

*Returns:* Let `CF` be
`ratio_divide<Period, typename ToDuration::period>`, and `CR` be
`common_type<typename ToDuration::rep, Rep, intmax_t>::type`.

- If `CF::num == 1` and `CF::den == 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(d.count()))
  ```
- otherwise, if `CF::num != 1` and `CF::den == 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) * static_cast<CR>(CF::num)))
  ```
- otherwise, if `CF::num == 1` and `CF::den != 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) / static_cast<CR>(CF::den)))
  ```
- otherwise, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) * static_cast<CR>(CF::num) / static_cast<CR>(CF::den)))
  ```

[*Note 1*: This function does not use any implicit conversions; all
conversions are done with `static_cast`. It avoids multiplications and
divisions when it is known at compile time that one or more arguments
is 1. Intermediate computations are carried out in the widest
representation and only converted to the destination representation at
the final step. — *end note*\]

``` cpp
template<class ToDuration, class Rep, class Period>
  constexpr ToDuration floor(const duration<Rep, Period>& d);
```

*Constraints:* `ToDuration` is a specialization of `duration`.

*Returns:* The greatest result `t` representable in `ToDuration` for
which `t <= d`.

``` cpp
template<class ToDuration, class Rep, class Period>
  constexpr ToDuration ceil(const duration<Rep, Period>& d);
```

*Constraints:* `ToDuration` is a specialization of `duration`.

*Returns:* The least result `t` representable in `ToDuration` for which
`t >= d`.

``` cpp
template<class ToDuration, class Rep, class Period>
  constexpr ToDuration round(const duration<Rep, Period>& d);
```

*Constraints:* `ToDuration` is a specialization of `duration` and
`treat_as_floating_point_v<typename ToDuration::rep>` is `false`.

*Returns:* The value of `ToDuration` that is closest to `d`. If there
are two closest values, then return the value `t` for which
`t % 2 == 0`.

### Suffixes for duration literals <a id="time.duration.literals">[[time.duration.literals]]</a>

This subclause describes literal suffixes for constructing duration
literals. The suffixes `h`, `min`, `s`, `ms`, `us`, `ns` denote duration
values of the corresponding types `hours`, `minutes`, `seconds`,
`milliseconds`, `microseconds`, and `nanoseconds` respectively if they
are applied to *integer-literal*s.

If any of these suffixes are applied to a *floating-point-literal* the
result is a `chrono::duration` literal with an unspecified
floating-point representation.

If any of these suffixes are applied to an *integer-literal* and the
resulting `chrono::duration` value cannot be represented in the result
type because of overflow, the program is ill-formed.

[*Example 1*:

The following code shows some duration literals.

``` cpp
using namespace std::chrono_literals;
auto constexpr aday=24h;
auto constexpr lesson=45min;
auto constexpr halfanhour=0.5h;
```

— *end example*\]

``` cpp
constexpr chrono::hours                                 operator""h(unsigned long long hours);
constexpr chrono::duration<unspecified, ratio<3600, 1>> operator""h(long double hours);
```

*Returns:* A `duration` literal representing `hours` hours.

``` cpp
constexpr chrono::minutes                             operator""min(unsigned long long minutes);
constexpr chrono::duration<unspecified, ratio<60, 1>> operator""min(long double minutes);
```

*Returns:* A `duration` literal representing `minutes` minutes.

``` cpp
constexpr chrono::seconds  \itcorr             operator""s(unsigned long long sec);
constexpr chrono::duration<unspecified> operator""s(long double sec);
```

*Returns:* A `duration` literal representing `sec` seconds.

[*Note 1*: The same suffix `s` is used for `basic_string` but there is
no conflict, since duration suffixes apply to numbers and string literal
suffixes apply to character array literals. — *end note*\]

``` cpp
constexpr chrono::milliseconds                 operator""ms(unsigned long long msec);
constexpr chrono::duration<unspecified, milli> operator""ms(long double msec);
```

*Returns:* A `duration` literal representing `msec` milliseconds.

``` cpp
constexpr chrono::microseconds                 operator""us(unsigned long long usec);
constexpr chrono::duration<unspecified, micro> operator""us(long double usec);
```

*Returns:* A `duration` literal representing `usec` microseconds.

``` cpp
constexpr chrono::nanoseconds                 operator""ns(unsigned long long nsec);
constexpr chrono::duration<unspecified, nano> operator""ns(long double nsec);
```

*Returns:* A `duration` literal representing `nsec` nanoseconds.

### Algorithms <a id="time.duration.alg">[[time.duration.alg]]</a>

``` cpp
template<class Rep, class Period>
  constexpr duration<Rep, Period> abs(duration<Rep, Period> d);
```

*Constraints:* `numeric_limits<Rep>::is_signed` is `true`.

*Returns:* If `d >= d.zero()`, return `d`, otherwise return `-d`.

### I/O <a id="time.duration.io">[[time.duration.io]]</a>

``` cpp
template<class charT, class traits, class Rep, class Period>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const duration<Rep, Period>& d);
```

*Effects:* Inserts the duration `d` onto the stream `os` as if it were
implemented as follows:

``` cpp
basic_ostringstream<charT, traits> s;
s.flags(os.flags());
s.imbue(os.getloc());
s.precision(os.precision());
s << d.count() << units-suffix;
return os << s.str();
```

where *`units-suffix`* depends on the type `Period::type` as follows:

- If `Period::type` is `atto`, *`units-suffix`* is `"as"`.
- Otherwise, if `Period::type` is `femto`, *`units-suffix`* is `"fs"`.
- Otherwise, if `Period::type` is `pico`, *`units-suffix`* is `"ps"`.
- Otherwise, if `Period::type` is `nano`, *`units-suffix`* is `"ns"`.
- Otherwise, if `Period::type` is `micro`, it is
  *implementation-defined* whether *`units-suffix`* is `"`\textmu`s"`
  (`"\u00b5\u0073"`) or `"us"`.
- Otherwise, if `Period::type` is `milli`, *`units-suffix`* is `"ms"`.
- Otherwise, if `Period::type` is `centi`, *`units-suffix`* is `"cs"`.
- Otherwise, if `Period::type` is `deci`, *`units-suffix`* is `"ds"`.
- Otherwise, if `Period::type` is `ratio<1>`, *`units-suffix`* is `"s"`.
- Otherwise, if `Period::type` is `deca`, *`units-suffix`* is `"das"`.
- Otherwise, if `Period::type` is `hecto`, *`units-suffix`* is `"hs"`.
- Otherwise, if `Period::type` is `kilo`, *`units-suffix`* is `"ks"`.
- Otherwise, if `Period::type` is `mega`, *`units-suffix`* is `"Ms"`.
- Otherwise, if `Period::type` is `giga`, *`units-suffix`* is `"Gs"`.
- Otherwise, if `Period::type` is `tera`, *`units-suffix`* is `"Ts"`.
- Otherwise, if `Period::type` is `peta`, *`units-suffix`* is `"Ps"`.
- Otherwise, if `Period::type` is `exa`, *`units-suffix`* is `"Es"`.
- Otherwise, if `Period::type` is `ratio<60>`, *`units-suffix`* is
  `"min"`.
- Otherwise, if `Period::type` is `ratio<3600>`, *`units-suffix`* is
  `"h"`.
- Otherwise, if `Period::type` is `ratio<86400>`, *`units-suffix`* is
  `"d"`.
- Otherwise, if `Period::type::den == 1`, *`units-suffix`* is
  `"[`*`num`*`]s"`.
- Otherwise, *`units-suffix`* is `"[`*`num`*`/`*`den`*`]s"`.

In the list above, the use of *`num`* and *`den`* refers to the static
data members of `Period::type`, which are converted to arrays of `charT`
using a decimal conversion with no leading zeroes.

*Returns:* `os`.

``` cpp
template<class charT, class traits, class Rep, class Period, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                duration<Rep, Period>& d,
                basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the duration `d`
using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid duration,
`is.setstate(ios_base::failbit)` is called and `d` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

## Class template `time_point` <a id="time.point">[[time.point]]</a>

### General <a id="time.point.general">[[time.point.general]]</a>

``` cpp
namespace std::chrono {
  template<class Clock, class Duration = typename Clock::duration>
  class time_point {
  public:
    using clock    = Clock;
    using duration = Duration;
    using rep      = typename duration::rep;
    using period   = typename duration::period;

  private:
    duration d_;                                                // exposition only

  public:
    // [time.point.cons], construct
    constexpr time_point();                                     // has value epoch
    constexpr explicit time_point(const duration& d);           // same as time_point() + d
    template<class Duration2>
      constexpr time_point(const time_point<clock, Duration2>& t);

    // [time.point.observer], observer
    constexpr duration time_since_epoch() const;

    // [time.point.arithmetic], arithmetic
    constexpr time_point& operator++();
    constexpr time_point operator++(int);
    constexpr time_point& operator--();
    constexpr time_point operator--(int);
    constexpr time_point& operator+=(const duration& d);
    constexpr time_point& operator-=(const duration& d);

    // [time.point.special], special values
    static constexpr time_point min() noexcept;
    static constexpr time_point max() noexcept;
  };
}
```

If `Duration` is not a specialization of `duration`, the program is
ill-formed.

### Constructors <a id="time.point.cons">[[time.point.cons]]</a>

``` cpp
constexpr time_point();
```

*Effects:* Initializes `d_` with `duration::zero()`. Such a `time_point`
object represents the epoch.

``` cpp
constexpr explicit time_point(const duration& d);
```

*Effects:* Initializes `d_` with `d`. Such a `time_point` object
represents the epoch `+ d`.

``` cpp
template<class Duration2>
  constexpr time_point(const time_point<clock, Duration2>& t);
```

*Constraints:* `is_convertible_v<Duration2, duration>` is `true`.

*Effects:* Initializes `d_` with `t.time_since_epoch()`.

### Observer <a id="time.point.observer">[[time.point.observer]]</a>

``` cpp
constexpr duration time_since_epoch() const;
```

*Returns:* `d_`.

### Arithmetic <a id="time.point.arithmetic">[[time.point.arithmetic]]</a>

``` cpp
constexpr time_point& operator++();
```

*Effects:* Equivalent to: `++d_`.

*Returns:* `*this`.

``` cpp
constexpr time_point operator++(int);
```

*Effects:* Equivalent to: `return time_point{d_++};`

``` cpp
constexpr time_point& operator--();
```

*Effects:* Equivalent to: `–d_`.

*Returns:* `*this`.

``` cpp
constexpr time_point operator--(int);
```

*Effects:* Equivalent to: `return time_point{d_--};`

``` cpp
constexpr time_point& operator+=(const duration& d);
```

*Effects:* Equivalent to: `d_ += d`.

*Returns:* `*this`.

``` cpp
constexpr time_point& operator-=(const duration& d);
```

*Effects:* Equivalent to: `d_ -= d`.

*Returns:* `*this`.

### Special values <a id="time.point.special">[[time.point.special]]</a>

``` cpp
static constexpr time_point min() noexcept;
```

*Returns:* `time_point(duration::min())`.

``` cpp
static constexpr time_point max() noexcept;
```

*Returns:* `time_point(duration::max())`.

### Non-member arithmetic <a id="time.point.nonmember">[[time.point.nonmember]]</a>

``` cpp
template<class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
    operator+(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs.time_since_epoch() + rhs)`, where `CT` is the type of
the return value.

``` cpp
template<class Rep1, class Period1, class Clock, class Duration2>
  constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
    operator+(const duration<Rep1, Period1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `rhs + lhs`.

``` cpp
template<class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
    operator-(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CT(lhs.time_since_epoch() - rhs)`, where `CT` is the type of
the return value.

``` cpp
template<class Clock, class Duration1, class Duration2>
  constexpr common_type_t<Duration1, Duration2>
    operator-(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() - rhs.time_since_epoch()`.

### Comparisons <a id="time.point.comparisons">[[time.point.comparisons]]</a>

``` cpp
template<class Clock, class Duration1, class Duration2>
  constexpr bool operator==(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() == rhs.time_since_epoch()`.

``` cpp
template<class Clock, class Duration1, class Duration2>
  constexpr bool operator<(const time_point<Clock, Duration1>& lhs,
                           const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() < rhs.time_since_epoch()`.

``` cpp
template<class Clock, class Duration1, class Duration2>
  constexpr bool operator>(const time_point<Clock, Duration1>& lhs,
                           const time_point<Clock, Duration2>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template<class Clock, class Duration1, class Duration2>
  constexpr bool operator<=(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template<class Clock, class Duration1, class Duration2>
  constexpr bool operator>=(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(lhs < rhs)`.

``` cpp
template<class Clock, class Duration1,
         three_way_comparable_with<Duration1> Duration2>
  constexpr auto operator<=>(const time_point<Clock, Duration1>& lhs,
                             const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() <=> rhs.time_since_epoch()`.

### Conversions <a id="time.point.cast">[[time.point.cast]]</a>

``` cpp
template<class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration> time_point_cast(const time_point<Clock, Duration>& t);
```

*Constraints:* `ToDuration` is a specialization of `duration`.

*Returns:*

``` cpp
time_point<Clock, ToDuration>(duration_cast<ToDuration>(t.time_since_epoch()))
```

``` cpp
template<class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration> floor(const time_point<Clock, Duration>& tp);
```

*Constraints:* `ToDuration` is a specialization of `duration`.

*Returns:*
`time_point<Clock, ToDuration>(floor<ToDuration>(tp.time_since_epoch()))`.

``` cpp
template<class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration> ceil(const time_point<Clock, Duration>& tp);
```

*Constraints:* `ToDuration` is a specialization of `duration`.

*Returns:*
`time_point<Clock, ToDuration>(ceil<ToDuration>(tp.time_since_epoch()))`.

``` cpp
template<class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration> round(const time_point<Clock, Duration>& tp);
```

*Constraints:* `ToDuration` is a specialization of `duration`, and
`treat_as_floating_point_v<typename ToDuration::rep>` is `false`.

*Returns:*
`time_point<Clock, ToDuration>(round<ToDuration>(tp.time_since_epoch()))`.

## Clocks <a id="time.clock">[[time.clock]]</a>

### General <a id="time.clock.general">[[time.clock.general]]</a>

The types defined in [[time.clock]] meet the *Cpp17TrivialClock*
requirements [[time.clock.req]] unless otherwise specified.

### Class `system_clock` <a id="time.clock.system">[[time.clock.system]]</a>

#### Overview <a id="time.clock.system.overview">[[time.clock.system.overview]]</a>

``` cpp
namespace std::chrono {
  class system_clock {
  public:
    using rep        = see below;
    using period     = ratio<unspecified, unspecified{}>;
    using duration   = chrono::duration<rep, period>;
    using time_point = chrono::time_point<system_clock>;
    static constexpr bool is_steady = unspecified;

    static time_point now() noexcept;

    // mapping to/from C type time_t
    static time_t      to_time_t  (const time_point& t) noexcept;
    static time_point  from_time_t(time_t t) noexcept;
  };
}
```

Objects of type `system_clock` represent wall clock time from the
system-wide realtime clock. Objects of type `sys_time<Duration>` measure
time since 1970-01-01 00:00:00 UTC excluding leap seconds. This measure
is commonly referred to as *Unix time*. This measure facilitates an
efficient mapping between `sys_time` and calendar types [[time.cal]].

[*Example 1*:   
`sys_seconds{sys_days{1970y/January/1}}.time_since_epoch()` is `0s`.  
`sys_seconds{sys_days{2000y/January/1}}.time_since_epoch()` is
`946'684'800s`, which is `10'957 * 86'400s`.  
 — *end example*\]

#### Members <a id="time.clock.system.members">[[time.clock.system.members]]</a>

``` cpp
using system_clock::rep = unspecified;
```

*Constraints:*
`system_clock::duration::min() < system_clock::duration::zero()` is
`true`.

[*Note 1*: This implies that `rep` is a signed type. — *end note*\]

``` cpp
static time_t to_time_t(const time_point& t) noexcept;
```

*Returns:* A `time_t` object that represents the same point in time as
`t` when both values are restricted to the coarser of the precisions of
`time_t` and `time_point`. It is *implementation-defined* whether values
are rounded or truncated to the required precision.

``` cpp
static time_point from_time_t(time_t t) noexcept;
```

*Returns:* A `time_point` object that represents the same point in time
as `t` when both values are restricted to the coarser of the precisions
of `time_t` and `time_point`. It is *implementation-defined* whether
values are rounded or truncated to the required precision.

#### Non-member functions <a id="time.clock.system.nonmembers">[[time.clock.system.nonmembers]]</a>

``` cpp
template<class charT, class traits, class Duration>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const sys_time<Duration>& tp);
```

*Constraints:* `treat_as_floating_point_v<typename Duration::rep>` is
`false`, and `Duration{1} < days{1}` is `true`.

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%F %T}"), tp);
```

[*Example 1*:

``` cpp
cout << sys_seconds{0s} << '\n';                // 1970-01-01 00:00:00
cout << sys_seconds{946'684'800s} << '\n';      // 2000-01-01 00:00:00
cout << sys_seconds{946'688'523s} << '\n';      // 2000-01-01 01:02:03
```

— *end example*\]

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const sys_days& dp);
```

*Effects:* `os << year_month_day{dp}`.

*Returns:* `os`.

``` cpp
template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                sys_time<Duration>& tp, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `sys_time`
`tp` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid date,
`is.setstate(ios_base::failbit)` is called and `tp` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null. Additionally, the parsed offset will be
subtracted from the successfully parsed timestamp prior to assigning
that difference to `tp`.

*Returns:* `is`.

### Class `utc_clock` <a id="time.clock.utc">[[time.clock.utc]]</a>

#### Overview <a id="time.clock.utc.overview">[[time.clock.utc.overview]]</a>

``` cpp
namespace std::chrono {
  class utc_clock {
  public:
    using rep                       = a signed arithmetic type;
    using period                    = ratio<unspecified, unspecified>;
    using duration                  = chrono::duration<rep, period>;
    using time_point                = chrono::time_point<utc_clock>;
    static constexpr bool is_steady = unspecified;

    static time_point now();

    template<class Duration>
      static sys_time<common_type_t<Duration, seconds>>
        to_sys(const utc_time<Duration>& t);
    template<class Duration>
      static utc_time<common_type_t<Duration, seconds>>
        from_sys(const sys_time<Duration>& t);
  };
}
```

In contrast to `sys_time`, which does not take leap seconds into
account, `utc_clock` and its associated `time_point`, `utc_time`, count
time, including leap seconds, since 1970-01-01 00:00:00 UTC.

[*Note 1*: The UTC time standard began on 1972-01-01 00:00:10 TAI. To
measure time since this epoch instead, one can add/subtract the constant
`sys_days{1972y/1/1} - sys_days{1970y/1/1}` (`63'072'000s`) from the
`utc_time`. — *end note*\]

[*Example 1*:   
`clock_cast<utc_clock>(sys_seconds{sys_days{1970y/January/1}}).time_since_epoch()`
is `0s`.  
`clock_cast<utc_clock>(sys_seconds{sys_days{2000y/January/1}}).time_since_epoch()`
is `946'684'822s`,  
which is `10'957 * 86'400s + 22s`.  
 — *end example*\]

`utc_clock` is not a *Cpp17TrivialClock* unless the implementation can
guarantee that `utc_clock::now()` does not propagate an exception.

[*Note 2*: `noexcept(from_sys(system_clock::now()))` is
`false`. — *end note*\]

#### Member functions <a id="time.clock.utc.members">[[time.clock.utc.members]]</a>

``` cpp
static time_point now();
```

*Returns:* `from_sys(system_clock::now())`, or a more accurate value of
`utc_time`.

``` cpp
template<class Duration>
  static sys_time<common_type_t<Duration, seconds>>
    to_sys(const utc_time<Duration>& u);
```

*Returns:* A `sys_time` `t`, such that `from_sys(t) == u` if such a
mapping exists. Otherwise `u` represents a `time_point` during a
positive leap second insertion, the conversion counts that leap second
as not inserted, and the last representable value of `sys_time` prior to
the insertion of the leap second is returned.

``` cpp
template<class Duration>
  static utc_time<common_type_t<Duration, seconds>>
    from_sys(const sys_time<Duration>& t);
```

*Returns:* A `utc_time` `u`, such that
`u.time_since_epoch() - t.time_since_epoch()` is equal to the sum of
leap seconds that were inserted between `t` and 1970-01-01. If `t` is
exactly the date of leap second insertion, then the conversion counts
that leap second as inserted.

[*Example 1*:

``` cpp
auto t = sys_days{July/1/2015} - 2ns;
auto u = utc_clock::from_sys(t);
assert(u.time_since_epoch() - t.time_since_epoch() == 25s);
t += 1ns;
u = utc_clock::from_sys(t);
assert(u.time_since_epoch() - t.time_since_epoch() == 25s);
t += 1ns;
u = utc_clock::from_sys(t);
assert(u.time_since_epoch() - t.time_since_epoch() == 26s);
t += 1ns;
u = utc_clock::from_sys(t);
assert(u.time_since_epoch() - t.time_since_epoch() == 26s);
```

— *end example*\]

#### Non-member functions <a id="time.clock.utc.nonmembers">[[time.clock.utc.nonmembers]]</a>

``` cpp
template<class charT, class traits, class Duration>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const utc_time<Duration>& t);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%F %T}"), t);
```

[*Example 1*:

``` cpp
auto t = sys_days{July/1/2015} - 500ms;
auto u = clock_cast<utc_clock>(t);
for (auto i = 0; i < 8; ++i, u += 250ms)
  cout << u << " UTC\n";
```

Produces this output:

``` text
2015-06-30 23:59:59.500 UTC
2015-06-30 23:59:59.750 UTC
2015-06-30 23:59:60.000 UTC
2015-06-30 23:59:60.250 UTC
2015-06-30 23:59:60.500 UTC
2015-06-30 23:59:60.750 UTC
2015-07-01 00:00:00.000 UTC
2015-07-01 00:00:00.250 UTC
```

— *end example*\]

``` cpp
template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                utc_time<Duration>& tp, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `utc_time`
`tp` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid date,
`is.setstate(ios_base::failbit)` is called and `tp` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null. Additionally, the parsed offset will be
subtracted from the successfully parsed timestamp prior to assigning
that difference to `tp`.

*Returns:* `is`.

``` cpp
struct leap_second_info {
  bool    is_leap_second;
  seconds elapsed;
};
```

The type `leap_second_info` has data members and special members
specified above. It has no base classes or members other than those
specified.

``` cpp
template<class Duration>
  leap_second_info get_leap_second_info(const utc_time<Duration>& ut);
```

*Returns:* A `leap_second_info` `lsi`, where `lsi.is_leap_second` is
`true` if `ut` is during a positive leap second insertion, and otherwise
`false`. `lsi.elapsed` is the sum of leap seconds between 1970-01-01 and
`ut`. If `lsi.is_leap_second` is `true`, the leap second referred to by
`ut` is included in the sum.

### Class `tai_clock` <a id="time.clock.tai">[[time.clock.tai]]</a>

#### Overview <a id="time.clock.tai.overview">[[time.clock.tai.overview]]</a>

``` cpp
namespace std::chrono {
  class tai_clock {
  public:
    using rep                       = a signed arithmetic type;
    using period                    = ratio<unspecified, unspecified>;
    using duration                  = chrono::duration<rep, period>;
    using time_point                = chrono::time_point<tai_clock>;
    static constexpr bool is_steady = unspecified;

    static time_point now();

    template<class Duration>
      static utc_time<common_type_t<Duration, seconds>>
        to_utc(const tai_time<Duration>&) noexcept;
    template<class Duration>
      static tai_time<common_type_t<Duration, seconds>>
        from_utc(const utc_time<Duration>&) noexcept;
  };
}
```

The clock `tai_clock` measures seconds since 1958-01-01 00:00:00 and is
offset 10s ahead of UTC at this date. That is, 1958-01-01 00:00:00 TAI
is equivalent to 1957-12-31 23:59:50 UTC. Leap seconds are not inserted
into TAI. Therefore every time a leap second is inserted into UTC, UTC
shifts another second with respect to TAI. For example by 2000-01-01
there had been 22 positive and 0 negative leap seconds inserted so
2000-01-01 00:00:00 UTC is equivalent to 2000-01-01 00:00:32 TAI (22s
plus the initial 10s offset).

`tai_clock` is not a *Cpp17TrivialClock* unless the implementation can
guarantee that `tai_clock::now()` does not propagate an exception.

[*Note 1*: `noexcept(from_utc(utc_clock::now()))` is
`false`. — *end note*\]

#### Member functions <a id="time.clock.tai.members">[[time.clock.tai.members]]</a>

``` cpp
static time_point now();
```

*Returns:* `from_utc(utc_clock::now())`, or a more accurate value of
`tai_time`.

``` cpp
template<class Duration>
  static utc_time<common_type_t<Duration, seconds>>
    to_utc(const tai_time<Duration>& t) noexcept;
```

*Returns:*

``` cpp
utc_time<common_type_t<Duration, seconds>>{t.time_since_epoch()} - 378691210s
```

[*Note 1*:

``` cpp
378691210s == sys_days{1970y/January/1} - sys_days{1958y/January/1} + 10s
```

— *end note*\]

``` cpp
template<class Duration>
  static tai_time<common_type_t<Duration, seconds>>
    from_utc(const utc_time<Duration>& t) noexcept;
```

*Returns:*

``` cpp
tai_time<common_type_t<Duration, seconds>>{t.time_since_epoch()} + 378691210s
```

[*Note 2*:

``` cpp
378691210s == sys_days{1970y/January/1} - sys_days{1958y/January/1} + 10s
```

— *end note*\]

#### Non-member functions <a id="time.clock.tai.nonmembers">[[time.clock.tai.nonmembers]]</a>

``` cpp
template<class charT, class traits, class Duration>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const tai_time<Duration>& t);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%F %T}"), t);
```

[*Example 1*:

``` cpp
auto st = sys_days{2000y/January/1};
auto tt = clock_cast<tai_clock>(st);
cout << format("{0:%F %T %Z} == {1:%F %T %Z}\n", st, tt);
```

Produces this output:

``` text
2000-01-01 00:00:00 UTC == 2000-01-01 00:00:32 TAI
```

— *end example*\]

``` cpp
template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                tai_time<Duration>& tp, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `tai_time`
`tp` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid date,
`is.setstate(ios_base::failbit)` is called and `tp` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null. Additionally, the parsed offset will be
subtracted from the successfully parsed timestamp prior to assigning
that difference to `tp`.

*Returns:* `is`.

### Class `gps_clock` <a id="time.clock.gps">[[time.clock.gps]]</a>

#### Overview <a id="time.clock.gps.overview">[[time.clock.gps.overview]]</a>

``` cpp
namespace std::chrono {
  class gps_clock {
  public:
    using rep                       = a signed arithmetic type;
    using period                    = ratio<unspecified, unspecified>;
    using duration                  = chrono::duration<rep, period>;
    using time_point                = chrono::time_point<gps_clock>;
    static constexpr bool is_steady = unspecified;

    static time_point now();

    template<class Duration>
      static utc_time<common_type_t<Duration, seconds>>
        to_utc(const gps_time<Duration>&) noexcept;
    template<class Duration>
      static gps_time<common_type_t<Duration, seconds>>
        from_utc(const utc_time<Duration>&) noexcept;
  };
}
```

The clock `gps_clock` measures seconds since the first Sunday of
January, 1980 00:00:00 UTC. Leap seconds are not inserted into GPS.
Therefore every time a leap second is inserted into UTC, UTC shifts
another second with respect to GPS. Aside from the offset from
`1958y/January/1` to `1980y/January/Sunday[1]`, GPS is behind TAI by 19s
due to the 10s offset between 1958 and 1970 and the additional 9 leap
seconds inserted between 1970 and 1980.

`gps_clock` is not a *Cpp17TrivialClock* unless the implementation can
guarantee that `gps_clock::now()` does not propagate an exception.

[*Note 1*: `noexcept(from_utc(utc_clock::now()))` is
`false`. — *end note*\]

#### Member functions <a id="time.clock.gps.members">[[time.clock.gps.members]]</a>

``` cpp
static time_point now();
```

*Returns:* `from_utc(utc_clock::now())`, or a more accurate value of
`gps_time`.

``` cpp
template<class Duration>
  static utc_time<common_type_t<Duration, seconds>>
    to_utc(const gps_time<Duration>& t) noexcept;
```

*Returns:*

``` cpp
utc_time<common_type_t<Duration, seconds>>{t.time_since_epoch()} + 315964809s
```

[*Note 1*:

``` cpp
315964809s == sys_days{1980y/January/Sunday[1]} - sys_days{1970y/January/1} + 9s
```

— *end note*\]

``` cpp
template<class Duration>
  static gps_time<common_type_t<Duration, seconds>>
    from_utc(const utc_time<Duration>& t) noexcept;
```

*Returns:*

``` cpp
gps_time<common_type_t<Duration, seconds>>{t.time_since_epoch()} - 315964809s
```

[*Note 2*:

``` cpp
315964809s == sys_days{1980y/January/Sunday[1]} - sys_days{1970y/January/1} + 9s
```

— *end note*\]

#### Non-member functions <a id="time.clock.gps.nonmembers">[[time.clock.gps.nonmembers]]</a>

``` cpp
template<class charT, class traits, class Duration>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const gps_time<Duration>& t);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%F %T}"), t);
```

[*Example 1*:

``` cpp
auto st = sys_days{2000y/January/1};
auto gt = clock_cast<gps_clock>(st);
cout << format("{0:%F %T %Z} == {1:%F %T %Z}\n", st, gt);
```

Produces this output:

``` text
2000-01-01 00:00:00 UTC == 2000-01-01 00:00:13 GPS
```

— *end example*\]

``` cpp
template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                gps_time<Duration>& tp, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `gps_time`
`tp` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid date,
`is.setstate(ios_base::failbit)` is called and `tp` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null. Additionally, the parsed offset will be
subtracted from the successfully parsed timestamp prior to assigning
that difference to `tp`.

*Returns:* `is`.

### Type `file_clock` <a id="time.clock.file">[[time.clock.file]]</a>

#### Overview <a id="time.clock.file.overview">[[time.clock.file.overview]]</a>

``` cpp
namespace std::chrono {
  using file_clock = see below;
}
```

`file_clock` is an alias for a type meeting the *Cpp17TrivialClock*
requirements [[time.clock.req]], and using a signed arithmetic type for
`file_clock::rep`. `file_clock` is used to create the `time_point`
system used for `file_time_type` [[filesystems]]. Its epoch is
unspecified, and `noexcept(file_clock::now())` is `true`.

[*Note 1*: The type that `file_clock` denotes can be in a different
namespace than `std::chrono`, such as `std::filesystem`. — *end note*\]

#### Member functions <a id="time.clock.file.members">[[time.clock.file.members]]</a>

The type denoted by `file_clock` provides precisely one of the following
two sets of static member functions:

``` cpp
template<class Duration>
  static sys_time<see below>
    to_sys(const file_time<Duration>&);
template<class Duration>
  static file_time<see below>
    from_sys(const sys_time<Duration>&);
```

or:

``` cpp
template<class Duration>
  static utc_time<see below>
    to_utc(const file_time<Duration>&);
template<class Duration>
  static file_time<see below>
    from_utc(const utc_time<Duration>&);
```

These member functions shall provide `time_point` conversions consistent
with those specified by `utc_clock`, `tai_clock`, and `gps_clock`. The
`Duration` of the resultant `time_point` is computed from the `Duration`
of the input `time_point`.

#### Non-member functions <a id="time.clock.file.nonmembers">[[time.clock.file.nonmembers]]</a>

``` cpp
template<class charT, class traits, class Duration>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const file_time<Duration>& t);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%F %T}"), t);
```

``` cpp
template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                file_time<Duration>& tp, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `file_time`
`tp` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid date,
`is.setstate(ios_base::failbit)` is called and `tp` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null. Additionally, the parsed offset will be
subtracted from the successfully parsed timestamp prior to assigning
that difference to `tp`.

*Returns:* `is`.

### Class `steady_clock` <a id="time.clock.steady">[[time.clock.steady]]</a>

``` cpp
namespace std::chrono {
  class steady_clock {
  public:
    using rep        = unspecified;
    using period     = ratio<unspecified, unspecified{}>;
    using duration   = chrono::duration<rep, period>;
    using time_point = chrono::time_point<unspecified, duration>;
    static constexpr bool is_steady = true;

    static time_point now() noexcept;
  };
}
```

Objects of class `steady_clock` represent clocks for which values of
`time_point` never decrease as physical time advances and for which
values of `time_point` advance at a steady rate relative to real time.
That is, the clock may not be adjusted.

### Class `high_resolution_clock` <a id="time.clock.hires">[[time.clock.hires]]</a>

``` cpp
namespace std::chrono {
  class high_resolution_clock {
  public:
    using rep        = unspecified;
    using period     = ratio<unspecified, unspecified{}>;
    using duration   = chrono::duration<rep, period>;
    using time_point = chrono::time_point<unspecified, duration>;
    static constexpr bool is_steady = unspecified;

    static time_point now() noexcept;
  };
}
```

Objects of class `high_resolution_clock` represent clocks with the
shortest tick period. `high_resolution_clock` may be a synonym for
`system_clock` or `steady_clock`.

### Local time <a id="time.clock.local">[[time.clock.local]]</a>

The family of time points denoted by `local_time<Duration>` are based on
the pseudo clock `local_t`. `local_t` has no member `now()` and thus
does not meet the clock requirements. Nevertheless
`local_time<Duration>` serves the vital role of representing local time
with respect to a not-yet-specified time zone. Aside from being able to
get the current time, the complete `time_point` algebra is available for
`local_time<Duration>` (just as for `sys_time<Duration>`).

``` cpp
template<class charT, class traits, class Duration>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const local_time<Duration>& lt);
```

*Effects:*

``` cpp
os << sys_time<Duration>{lt.time_since_epoch()};
```

*Returns:* `os`.

``` cpp
template<class charT, class traits, class Duration, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                local_time<Duration>& tp, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `local_time`
`tp` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid date,
`is.setstate(ios_base::failbit)` is called and `tp` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

### `time_point` conversions <a id="time.clock.cast">[[time.clock.cast]]</a>

#### Class template `clock_time_conversion` <a id="time.clock.conv">[[time.clock.conv]]</a>

``` cpp
namespace std::chrono {
  template<class DestClock, class SourceClock>
  struct clock_time_conversion {};
}
```

`clock_time_conversion` serves as a trait which can be used to specify
how to convert a source `time_point` of type
`time_point<SourceClock, Duration>` to a destination `time_point` of
type `time_point<DestClock, Duration>` via a specialization:
`clock_time_conversion<DestClock, SourceClock>`. A specialization of
`clock_time_conversion<DestClock, SourceClock>` shall provide a
const-qualified `operator()` that takes a parameter of type
`time_point<SourceClock, Duration>` and returns a
`time_point<DestClock, OtherDuration>` representing an equivalent point
in time. `OtherDuration` is a `chrono::duration` whose specialization is
computed from the input `Duration` in a manner which can vary for each
`clock_time_conversion` specialization. A program may specialize
`clock_time_conversion` if at least one of the template parameters is a
user-defined clock type.

Several specializations are provided by the implementation, as described
in [[time.clock.cast.id]], [[time.clock.cast.sys.utc]],
[[time.clock.cast.sys]], and [[time.clock.cast.utc]].

#### Identity conversions <a id="time.clock.cast.id">[[time.clock.cast.id]]</a>

``` cpp
template<class Clock>
struct clock_time_conversion<Clock, Clock> {
  template<class Duration>
    time_point<Clock, Duration>
      operator()(const time_point<Clock, Duration>& t) const;
};
```

``` cpp
template<class Duration>
  time_point<Clock, Duration>
    operator()(const time_point<Clock, Duration>& t) const;
```

*Returns:* `t`.

``` cpp
template<>
struct clock_time_conversion<system_clock, system_clock> {
  template<class Duration>
    sys_time<Duration>
      operator()(const sys_time<Duration>& t) const;
};
```

``` cpp
template<class Duration>
  sys_time<Duration>
    operator()(const sys_time<Duration>& t) const;
```

*Returns:* `t`.

``` cpp
template<>
struct clock_time_conversion<utc_clock, utc_clock> {
  template<class Duration>
    utc_time<Duration>
      operator()(const utc_time<Duration>& t) const;
};
```

``` cpp
template<class Duration>
  utc_time<Duration>
    operator()(const utc_time<Duration>& t) const;
```

*Returns:* `t`.

#### Conversions between `system_clock` and `utc_clock` <a id="time.clock.cast.sys.utc">[[time.clock.cast.sys.utc]]</a>

``` cpp
template<>
struct clock_time_conversion<utc_clock, system_clock> {
  template<class Duration>
    utc_time<common_type_t<Duration, seconds>>
      operator()(const sys_time<Duration>& t) const;
};
```

``` cpp
template<class Duration>
  utc_time<common_type_t<Duration, seconds>>
    operator()(const sys_time<Duration>& t) const;
```

*Returns:* `utc_clock::from_sys(t)`.

``` cpp
template<>
struct clock_time_conversion<system_clock, utc_clock> {
  template<class Duration>
    sys_time<common_type_t<Duration, seconds>>
      operator()(const utc_time<Duration>& t) const;
};
```

``` cpp
template<class Duration>
  sys_time<common_type_t<Duration, seconds>>
    operator()(const utc_time<Duration>& t) const;
```

*Returns:* `utc_clock::to_sys(t)`.

#### Conversions between `system_clock` and other clocks <a id="time.clock.cast.sys">[[time.clock.cast.sys]]</a>

``` cpp
template<class SourceClock>
struct clock_time_conversion<system_clock, SourceClock> {
  template<class Duration>
    auto operator()(const time_point<SourceClock, Duration>& t) const
      -> decltype(SourceClock::to_sys(t));
};
```

``` cpp
template<class Duration>
  auto operator()(const time_point<SourceClock, Duration>& t) const
    -> decltype(SourceClock::to_sys(t));
```

*Constraints:* `SourceClock::to_sys(t)` is well-formed.

*Mandates:* `SourceClock::to_sys(t)` returns a `sys_time<Duration2>` for
some type `Duration2`[[time.point.general]].

*Returns:* `SourceClock::to_sys(t)`.

``` cpp
template<class DestClock>
struct clock_time_conversion<DestClock, system_clock> {
  template<class Duration>
    auto operator()(const sys_time<Duration>& t) const
      -> decltype(DestClock::from_sys(t));
};
```

``` cpp
template<class Duration>
  auto operator()(const sys_time<Duration>& t) const
    -> decltype(DestClock::from_sys(t));
```

*Constraints:* `DestClock::from_sys(t)` is well-formed.

*Mandates:* `DestClock::from_sys(t)` returns a
`time_point<DestClock, Duration2>` for some type
`Duration2`[[time.point.general]].

*Returns:* `DestClock::from_sys(t)`.

#### Conversions between `utc_clock` and other clocks <a id="time.clock.cast.utc">[[time.clock.cast.utc]]</a>

``` cpp
template<class SourceClock>
struct clock_time_conversion<utc_clock, SourceClock> {
  template<class Duration>
    auto operator()(const time_point<SourceClock, Duration>& t) const
      -> decltype(SourceClock::to_utc(t));
};
```

``` cpp
template<class Duration>
  auto operator()(const time_point<SourceClock, Duration>& t) const
    -> decltype(SourceClock::to_utc(t));
```

*Constraints:* `SourceClock::to_utc(t)` is well-formed.

*Mandates:* `SourceClock::to_utc(t)` returns a `utc_time<Duration2>` for
some type `Duration2`[[time.point.general]].

*Returns:* `SourceClock::to_utc(t)`.

``` cpp
template<class DestClock>
struct clock_time_conversion<DestClock, utc_clock> {
  template<class Duration>
    auto operator()(const utc_time<Duration>& t) const
      -> decltype(DestClock::from_utc(t));
};
```

``` cpp
template<class Duration>
  auto operator()(const utc_time<Duration>& t) const
    -> decltype(DestClock::from_utc(t));
```

*Constraints:* `DestClock::from_utc(t)` is well-formed.

*Mandates:* `DestClock::from_utc(t)` returns a
`time_point<DestClock, Duration2>` for some type
`Duration2`[[time.point.general]].

*Returns:* `DestClock::from_utc(t)`.

#### Function template `clock_cast` <a id="time.clock.cast.fn">[[time.clock.cast.fn]]</a>

``` cpp
template<class DestClock, class SourceClock, class Duration>
  auto clock_cast(const time_point<SourceClock, Duration>& t);
```

*Constraints:* At least one of the following clock time conversion
expressions is well-formed:

- ``` cpp
  clock_time_conversion<DestClock, SourceClock>{}(t)
  ```

- ``` cpp
  clock_time_conversion<DestClock, system_clock>{}(
    clock_time_conversion<system_clock, SourceClock>{}(t))
  ```

- ``` cpp
  clock_time_conversion<DestClock, utc_clock>{}(
    clock_time_conversion<utc_clock, SourceClock>{}(t))
  ```

- ``` cpp
  clock_time_conversion<DestClock, utc_clock>{}(
    clock_time_conversion<utc_clock, system_clock>{}(
      clock_time_conversion<system_clock, SourceClock>{}(t)))
  ```

- ``` cpp
  clock_time_conversion<DestClock, system_clock>{}(
    clock_time_conversion<system_clock, utc_clock>{}(
      clock_time_conversion<utc_clock, SourceClock>{}(t)))
  ```

A clock time conversion expression is considered better than another
clock time conversion expression if it involves fewer `operator()` calls
on `clock_time_conversion` specializations.

*Mandates:* Among the well-formed clock time conversion expressions from
the above list, there is a unique best expression.

*Returns:* The best well-formed clock time conversion expression in the
above list.

## The civil calendar <a id="time.cal">[[time.cal]]</a>

### In general <a id="time.cal.general">[[time.cal.general]]</a>

The types in [[time.cal]] describe the civil (Gregorian) calendar and
its relationship to `sys_days` and `local_days`.

### Class `last_spec` <a id="time.cal.last">[[time.cal.last]]</a>

``` cpp
namespace std::chrono {
  struct last_spec {
    explicit last_spec() = default;
  };
}
```

The type `last_spec` is used in conjunction with other calendar types to
specify the last in a sequence. For example, depending on context, it
can represent the last day of a month, or the last day of the week of a
month.

### Class `day` <a id="time.cal.day">[[time.cal.day]]</a>

#### Overview <a id="time.cal.day.overview">[[time.cal.day.overview]]</a>

``` cpp
namespace std::chrono {
  class day {
    unsigned char d_;           // exposition only
  public:
    day() = default;
    constexpr explicit day(unsigned d) noexcept;

    constexpr day& operator++()    noexcept;
    constexpr day  operator++(int) noexcept;
    constexpr day& operator--()    noexcept;
    constexpr day  operator--(int) noexcept;

    constexpr day& operator+=(const days& d) noexcept;
    constexpr day& operator-=(const days& d) noexcept;

    constexpr explicit operator unsigned() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`day` represents a day of a month. It normally holds values in the range
1 to 31, but may hold non-negative values outside this range. It can be
constructed with any `unsigned` value, which will be subsequently
truncated to fit into `day`’s unspecified internal storage. `day` meets
the *Cpp17EqualityComparable* ( [[cpp17.equalitycomparable]]) and
*Cpp17LessThanComparable* ( [[cpp17.lessthancomparable]]) requirements,
and participates in basic arithmetic with `days` objects, which
represent a difference between two `day` objects.

`day` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.day.members">[[time.cal.day.members]]</a>

``` cpp
constexpr explicit day(unsigned d) noexcept;
```

*Effects:* Initializes `d_` with `d`. The value held is unspecified if
`d` is not in the range \[`0`, `255`\].

``` cpp
constexpr day& operator++() noexcept;
```

*Effects:* `++d_`.

*Returns:* `*this`.

``` cpp
constexpr day operator++(int) noexcept;
```

*Effects:* `++(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr day& operator--() noexcept;
```

*Effects:* Equivalent to: `–d_`.

*Returns:* `*this`.

``` cpp
constexpr day operator--(int) noexcept;
```

*Effects:* `–(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr day& operator+=(const days& d) noexcept;
```

*Effects:* `*this = *this + d`.

*Returns:* `*this`.

``` cpp
constexpr day& operator-=(const days& d) noexcept;
```

*Effects:* `*this = *this - d`.

*Returns:* `*this`.

``` cpp
constexpr explicit operator unsigned() const noexcept;
```

*Returns:* `d_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `1 <= d_ && d_ <= 31`.

#### Non-member functions <a id="time.cal.day.nonmembers">[[time.cal.day.nonmembers]]</a>

``` cpp
constexpr bool operator==(const day& x, const day& y) noexcept;
```

*Returns:* `unsigned{x} == unsigned{y}`.

``` cpp
constexpr strong_ordering operator<=>(const day& x, const day& y) noexcept;
```

*Returns:* `unsigned{x} <=> unsigned{y}`.

``` cpp
constexpr day operator+(const day& x, const days& y) noexcept;
```

*Returns:* `day(unsigned{x} + y.count())`.

``` cpp
constexpr day operator+(const days& x, const day& y) noexcept;
```

*Returns:* `y + x`.

``` cpp
constexpr day operator-(const day& x, const days& y) noexcept;
```

*Returns:* `x + -y`.

``` cpp
constexpr days operator-(const day& x, const day& y) noexcept;
```

*Returns:* `days{int(unsigned{x}) - int(unsigned{y})}`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const day& d);
```

*Effects:* Equivalent to:

``` cpp
return os << (d.ok() ?
  format(STATICALLY-WIDEN<charT>("{:%d}"), d) :
  format(STATICALLY-WIDEN<charT>("{:%d} is not a valid day"), d));
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                day& d, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `day` `d`
using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid day,
`is.setstate(ios_base::failbit)` is called and `d` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

``` cpp
constexpr chrono::day operator""d(unsigned long long d) noexcept;
```

*Returns:* `day{static_cast<unsigned>(d)}`.

### Class `month` <a id="time.cal.month">[[time.cal.month]]</a>

#### Overview <a id="time.cal.month.overview">[[time.cal.month.overview]]</a>

``` cpp
namespace std::chrono {
  class month {
    unsigned char m_;           // exposition only
  public:
    month() = default;
    constexpr explicit month(unsigned m) noexcept;

    constexpr month& operator++()    noexcept;
    constexpr month  operator++(int) noexcept;
    constexpr month& operator--()    noexcept;
    constexpr month  operator--(int) noexcept;

    constexpr month& operator+=(const months& m) noexcept;
    constexpr month& operator-=(const months& m) noexcept;

    constexpr explicit operator unsigned() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`month` represents a month of a year. It normally holds values in the
range 1 to 12, but may hold non-negative values outside this range. It
can be constructed with any `unsigned` value, which will be subsequently
truncated to fit into `month`’s unspecified internal storage. `month`
meets the *Cpp17EqualityComparable* ( [[cpp17.equalitycomparable]]) and
*Cpp17LessThanComparable* ( [[cpp17.lessthancomparable]]) requirements,
and participates in basic arithmetic with `months` objects, which
represent a difference between two `month` objects.

`month` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.month.members">[[time.cal.month.members]]</a>

``` cpp
constexpr explicit month(unsigned m) noexcept;
```

*Effects:* Initializes `m_` with `m`. The value held is unspecified if
`m` is not in the range \[`0`, `255`\].

``` cpp
constexpr month& operator++() noexcept;
```

*Effects:* `*this += months{1}`.

*Returns:* `*this`.

``` cpp
constexpr month operator++(int) noexcept;
```

*Effects:* `++(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr month& operator--() noexcept;
```

*Effects:* `*this -= months{1}`.

*Returns:* `*this`.

``` cpp
constexpr month operator--(int) noexcept;
```

*Effects:* `–(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr month& operator+=(const months& m) noexcept;
```

*Effects:* `*this = *this + m`.

*Returns:* `*this`.

``` cpp
constexpr month& operator-=(const months& m) noexcept;
```

*Effects:* `*this = *this - m`.

*Returns:* `*this`.

``` cpp
constexpr explicit operator unsigned() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `1 <= m_ && m_ <= 12`.

#### Non-member functions <a id="time.cal.month.nonmembers">[[time.cal.month.nonmembers]]</a>

``` cpp
constexpr bool operator==(const month& x, const month& y) noexcept;
```

*Returns:* `unsigned{x} == unsigned{y}`.

``` cpp
constexpr strong_ordering operator<=>(const month& x, const month& y) noexcept;
```

*Returns:* `unsigned{x} <=> unsigned{y}`.

``` cpp
constexpr month operator+(const month& x, const months& y) noexcept;
```

*Returns:*

``` cpp
month{modulo(static_cast<long long>(unsigned{x}) + (y.count() - 1), 12) + 1}
```

where `modulo(n, 12)` computes the remainder of `n` divided by 12 using
Euclidean division.

[*Note 1*: Given a divisor of 12, Euclidean division truncates towards
negative infinity and always produces a remainder in the range of \[`0`,
`11`\]. Assuming no overflow in the signed summation, this operation
results in a `month` holding a value in the range \[`1`, `12`\] even if
`!x.ok()`. — *end note*\]

[*Example 1*: `February + months{11} == January`. — *end example*\]

``` cpp
constexpr month operator+(const months& x, const month& y) noexcept;
```

*Returns:* `y + x`.

``` cpp
constexpr month operator-(const month& x, const months& y) noexcept;
```

*Returns:* `x + -y`.

``` cpp
constexpr months operator-(const month& x, const month& y) noexcept;
```

*Returns:* If `x.ok() == true` and `y.ok() == true`, returns a value `m`
in the range \[`months{0}`, `months{11}`\] satisfying `y + m == x`.
Otherwise the value returned is unspecified.

[*Example 2*: `January - February == months{11}`. — *end example*\]

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const month& m);
```

*Effects:* Equivalent to:

``` cpp
return os << (m.ok() ?
  format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%b}"), m) :
  format(os.getloc(), STATICALLY-WIDEN<charT>("{} is not a valid month"),
         static_cast<unsigned>(m)));
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                month& m, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `month` `m`
using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid month,
`is.setstate(ios_base::failbit)` is called and `m` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

### Class `year` <a id="time.cal.year">[[time.cal.year]]</a>

#### Overview <a id="time.cal.year.overview">[[time.cal.year.overview]]</a>

``` cpp
namespace std::chrono {
  class year {
    short y_;                   // exposition only
  public:
    year() = default;
    constexpr explicit year(int y) noexcept;

    constexpr year& operator++()    noexcept;
    constexpr year  operator++(int) noexcept;
    constexpr year& operator--()    noexcept;
    constexpr year  operator--(int) noexcept;

    constexpr year& operator+=(const years& y) noexcept;
    constexpr year& operator-=(const years& y) noexcept;

    constexpr year operator+() const noexcept;
    constexpr year operator-() const noexcept;

    constexpr bool is_leap() const noexcept;

    constexpr explicit operator int() const noexcept;
    constexpr bool ok() const noexcept;

    static constexpr year min() noexcept;
    static constexpr year max() noexcept;
  };
}
```

`year` represents a year in the civil calendar. It can represent values
in the range \[`min()`, `max()`\]. It can be constructed with any `int`
value, which will be subsequently truncated to fit into `year`’s
unspecified internal storage. `year` meets the *Cpp17EqualityComparable*
( [[cpp17.equalitycomparable]]) and *Cpp17LessThanComparable* (
[[cpp17.lessthancomparable]]) requirements, and participates in basic
arithmetic with `years` objects, which represent a difference between
two `year` objects.

`year` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.year.members">[[time.cal.year.members]]</a>

``` cpp
constexpr explicit year(int y) noexcept;
```

*Effects:* Initializes `y_` with `y`. The value held is unspecified if
`y` is not in the range \[`-32767`, `32767`\].

``` cpp
constexpr year& operator++() noexcept;
```

*Effects:* `++y_`.

*Returns:* `*this`.

``` cpp
constexpr year operator++(int) noexcept;
```

*Effects:* `++(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr year& operator--() noexcept;
```

*Effects:* `–y_`.

*Returns:* `*this`.

``` cpp
constexpr year operator--(int) noexcept;
```

*Effects:* `–(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr year& operator+=(const years& y) noexcept;
```

*Effects:* `*this = *this + y`.

*Returns:* `*this`.

``` cpp
constexpr year& operator-=(const years& y) noexcept;
```

*Effects:* `*this = *this - y`.

*Returns:* `*this`.

``` cpp
constexpr year operator+() const noexcept;
```

*Returns:* `*this`.

``` cpp
constexpr year operator-() const noexcept;
```

*Returns:* `year{-y_}`.

``` cpp
constexpr bool is_leap() const noexcept;
```

*Returns:* `y_ % 4 == 0 && (y_ % 100 != 0 || y_ % 400 == 0)`.

``` cpp
constexpr explicit operator int() const noexcept;
```

*Returns:* `y_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `min().y_ <= y_ && y_ <= max().y_`.

``` cpp
static constexpr year min() noexcept;
```

*Returns:* `year{-32767}`.

``` cpp
static constexpr year max() noexcept;
```

*Returns:* `year{32767}`.

#### Non-member functions <a id="time.cal.year.nonmembers">[[time.cal.year.nonmembers]]</a>

``` cpp
constexpr bool operator==(const year& x, const year& y) noexcept;
```

*Returns:* `int{x} == int{y}`.

``` cpp
constexpr strong_ordering operator<=>(const year& x, const year& y) noexcept;
```

*Returns:* `int{x} <=> int{y}`.

``` cpp
constexpr year operator+(const year& x, const years& y) noexcept;
```

*Returns:* `year{int{x} + static_cast<int>(y.count())}`.

``` cpp
constexpr year operator+(const years& x, const year& y) noexcept;
```

*Returns:* `y + x`.

``` cpp
constexpr year operator-(const year& x, const years& y) noexcept;
```

*Returns:* `x + -y`.

``` cpp
constexpr years operator-(const year& x, const year& y) noexcept;
```

*Returns:* `years{int{x} - int{y}}`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const year& y);
```

*Effects:* Equivalent to:

``` cpp
return os << (y.ok() ?
  format(STATICALLY-WIDEN<charT>("{:%Y}"), y) :
  format(STATICALLY-WIDEN<charT>("{:%Y} is not a valid year"), y));
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                year& y, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `year` `y`
using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid year,
`is.setstate(ios_base::failbit)` is called and `y` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

``` cpp
constexpr chrono::year operator""y(unsigned long long y) noexcept;
```

*Returns:* `year{static_cast<int>(y)}`.

### Class `weekday` <a id="time.cal.wd">[[time.cal.wd]]</a>

#### Overview <a id="time.cal.wd.overview">[[time.cal.wd.overview]]</a>

``` cpp
namespace std::chrono {
  class weekday {
    unsigned char wd_;          // exposition only
  public:
    weekday() = default;
    constexpr explicit weekday(unsigned wd) noexcept;
    constexpr weekday(const sys_days& dp) noexcept;
    constexpr explicit weekday(const local_days& dp) noexcept;

    constexpr weekday& operator++()    noexcept;
    constexpr weekday  operator++(int) noexcept;
    constexpr weekday& operator--()    noexcept;
    constexpr weekday  operator--(int) noexcept;

    constexpr weekday& operator+=(const days& d) noexcept;
    constexpr weekday& operator-=(const days& d) noexcept;

    constexpr unsigned c_encoding() const noexcept;
    constexpr unsigned iso_encoding() const noexcept;
    constexpr bool ok() const noexcept;

    constexpr weekday_indexed operator[](unsigned index) const noexcept;
    constexpr weekday_last    operator[](last_spec) const noexcept;
  };
}
```

`weekday` represents a day of the week in the civil calendar. It
normally holds values in the range `0` to `6`, corresponding to Sunday
through Saturday, but it may hold non-negative values outside this
range. It can be constructed with any `unsigned` value, which will be
subsequently truncated to fit into `weekday`’s unspecified internal
storage. `weekday` meets the *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) requirements.

[*Note 1*: `weekday` is not *Cpp17LessThanComparable* because there is
no universal consensus on which day is the first day of the week.
`weekday`’s arithmetic operations treat the days of the week as a
circular range, with no beginning and no end. — *end note*\]

`weekday` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.wd.members">[[time.cal.wd.members]]</a>

``` cpp
constexpr explicit weekday(unsigned wd) noexcept;
```

*Effects:* Initializes `wd_` with `wd == 7 ? 0 : wd`. The value held is
unspecified if `wd` is not in the range \[`0`, `255`\].

``` cpp
constexpr weekday(const sys_days& dp) noexcept;
```

*Effects:* Computes what day of the week corresponds to the `sys_days`
`dp`, and initializes that day of the week in `wd_`.

[*Example 1*: If `dp` represents 1970-01-01, the constructed `weekday`
represents Thursday by storing `4` in `wd_`. — *end example*\]

``` cpp
constexpr explicit weekday(const local_days& dp) noexcept;
```

*Effects:* Computes what day of the week corresponds to the `local_days`
`dp`, and initializes that day of the week in `wd_`.

*Ensures:* The value is identical to that constructed from
`sys_days{dp.time_since_epoch()}`.

``` cpp
constexpr weekday& operator++() noexcept;
```

*Effects:* `*this += days{1}`.

*Returns:* `*this`.

``` cpp
constexpr weekday operator++(int) noexcept;
```

*Effects:* `++(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr weekday& operator--() noexcept;
```

*Effects:* `*this -= days{1}`.

*Returns:* `*this`.

``` cpp
constexpr weekday operator--(int) noexcept;
```

*Effects:* `–(*this)`.

*Returns:* A copy of `*this` as it existed on entry to this member
function.

``` cpp
constexpr weekday& operator+=(const days& d) noexcept;
```

*Effects:* `*this = *this + d`.

*Returns:* `*this`.

``` cpp
constexpr weekday& operator-=(const days& d) noexcept;
```

*Effects:* `*this = *this - d`.

*Returns:* `*this`.

``` cpp
constexpr unsigned c_encoding() const noexcept;
```

*Returns:* `wd_`.

``` cpp
constexpr unsigned iso_encoding() const noexcept;
```

*Returns:* `wd_ == 0u ? 7u : wd_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `wd_ <= 6`.

``` cpp
constexpr weekday_indexed operator[](unsigned index) const noexcept;
```

*Returns:* `{*this, index}`.

``` cpp
constexpr weekday_last operator[](last_spec) const noexcept;
```

*Returns:* `weekday_last{*this}`.

#### Non-member functions <a id="time.cal.wd.nonmembers">[[time.cal.wd.nonmembers]]</a>

``` cpp
constexpr bool operator==(const weekday& x, const weekday& y) noexcept;
```

*Returns:* `x.wd_ == y.wd_`.

``` cpp
constexpr weekday operator+(const weekday& x, const days& y) noexcept;
```

*Returns:*

``` cpp
weekday{modulo(static_cast<long long>(x.wd_) + y.count(), 7)}
```

where `modulo(n, 7)` computes the remainder of `n` divided by 7 using
Euclidean division.

[*Note 1*: Given a divisor of 7, Euclidean division truncates towards
negative infinity and always produces a remainder in the range of \[`0`,
`6`\]. Assuming no overflow in the signed summation, this operation
results in a `weekday` holding a value in the range \[`0`, `6`\] even if
`!x.ok()`. — *end note*\]

[*Example 1*: `Monday + days{6} == Sunday`. — *end example*\]

``` cpp
constexpr weekday operator+(const days& x, const weekday& y) noexcept;
```

*Returns:* `y + x`.

``` cpp
constexpr weekday operator-(const weekday& x, const days& y) noexcept;
```

*Returns:* `x + -y`.

``` cpp
constexpr days operator-(const weekday& x, const weekday& y) noexcept;
```

*Returns:* If `x.ok() == true` and `y.ok() == true`, returns a value `d`
in the range \[`days{0}`, `days{6}`\] satisfying `y + d == x`. Otherwise
the value returned is unspecified.

[*Example 2*: `Sunday - Monday == days{6}`. — *end example*\]

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const weekday& wd);
```

*Effects:* Equivalent to:

``` cpp
return os << (wd.ok() ?
  format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%a}"), wd) :
  format(os.getloc(), STATICALLY-WIDEN<charT>("{} is not a valid weekday"),
         static_cast<unsigned>(wd.wd_)));
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                weekday& wd, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `weekday`
`wd` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid weekday,
`is.setstate(ios_base::failbit)` is called and `wd` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

### Class `weekday_indexed` <a id="time.cal.wdidx">[[time.cal.wdidx]]</a>

#### Overview <a id="time.cal.wdidx.overview">[[time.cal.wdidx.overview]]</a>

``` cpp
namespace std::chrono {
  class weekday_indexed {
    chrono::weekday  wd_;       // exposition only
    unsigned char    index_;    // exposition only

  public:
    weekday_indexed() = default;
    constexpr weekday_indexed(const chrono::weekday& wd, unsigned index) noexcept;

    constexpr chrono::weekday weekday() const noexcept;
    constexpr unsigned        index()   const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`weekday_indexed` represents a `weekday` and a small index in the range
1 to 5. This class is used to represent the first, second, third,
fourth, or fifth weekday of a month.

[*Note 1*: A `weekday_indexed` object can be constructed by indexing a
`weekday` with an `unsigned`. — *end note*\]

[*Example 1*:

``` cpp
constexpr auto wdi = Sunday[2]; // wdi is the second Sunday of an as yet unspecified month
static_assert(wdi.weekday() == Sunday);
static_assert(wdi.index() == 2);
```

— *end example*\]

`weekday_indexed` is a trivially copyable and standard-layout class
type.

#### Member functions <a id="time.cal.wdidx.members">[[time.cal.wdidx.members]]</a>

``` cpp
constexpr weekday_indexed(const chrono::weekday& wd, unsigned index) noexcept;
```

*Effects:* Initializes `wd_` with `wd` and `index_` with `index`. The
values held are unspecified if `!wd.ok()` or `index` is not in the range
\[`0`, `7`\].

``` cpp
constexpr chrono::weekday weekday() const noexcept;
```

*Returns:* `wd_`.

``` cpp
constexpr unsigned index() const noexcept;
```

*Returns:* `index_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `wd_.ok() && 1 <= index_ && index_ <= 5`.

#### Non-member functions <a id="time.cal.wdidx.nonmembers">[[time.cal.wdidx.nonmembers]]</a>

``` cpp
constexpr bool operator==(const weekday_indexed& x, const weekday_indexed& y) noexcept;
```

*Returns:* `x.weekday() == y.weekday() && x.index() == y.index()`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const weekday_indexed& wdi);
```

*Effects:* Equivalent to:

``` cpp
auto i = wdi.index();
return os << (i >= 1 && i <= 5 ?
  format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}[{}]"), wdi.weekday(), i) :
  format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}[{} is not a valid index]"),
         wdi.weekday(), i));
```

### Class `weekday_last` <a id="time.cal.wdlast">[[time.cal.wdlast]]</a>

#### Overview <a id="time.cal.wdlast.overview">[[time.cal.wdlast.overview]]</a>

``` cpp
namespace std::chrono {
  class weekday_last {
    chrono::weekday wd_;                // exposition only

    public:
    constexpr explicit weekday_last(const chrono::weekday& wd) noexcept;

    constexpr chrono::weekday weekday() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`weekday_last` represents the last weekday of a month.

[*Note 1*: A `weekday_last` object can be constructed by indexing a
`weekday` with `last`. — *end note*\]

[*Example 1*:

``` cpp
constexpr auto wdl = Sunday[last];      // wdl is the last Sunday of an as yet unspecified month
static_assert(wdl.weekday() == Sunday);
```

— *end example*\]

`weekday_last` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.wdlast.members">[[time.cal.wdlast.members]]</a>

``` cpp
constexpr explicit weekday_last(const chrono::weekday& wd) noexcept;
```

*Effects:* Initializes `wd_` with `wd`.

``` cpp
constexpr chrono::weekday weekday() const noexcept;
```

*Returns:* `wd_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `wd_.ok()`.

#### Non-member functions <a id="time.cal.wdlast.nonmembers">[[time.cal.wdlast.nonmembers]]</a>

``` cpp
constexpr bool operator==(const weekday_last& x, const weekday_last& y) noexcept;
```

*Returns:* `x.weekday() == y.weekday()`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const weekday_last& wdl);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}[last]"), wdl.weekday());
```

### Class `month_day` <a id="time.cal.md">[[time.cal.md]]</a>

#### Overview <a id="time.cal.md.overview">[[time.cal.md.overview]]</a>

``` cpp
namespace std::chrono {
  class month_day {
    chrono::month m_;           // exposition only
    chrono::day   d_;           // exposition only

  public:
    month_day() = default;
    constexpr month_day(const chrono::month& m, const chrono::day& d) noexcept;

    constexpr chrono::month month() const noexcept;
    constexpr chrono::day   day()   const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`month_day` represents a specific day of a specific month, but with an
unspecified year. `month_day` meets the *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) and *Cpp17LessThanComparable* (
[[cpp17.lessthancomparable]]) requirements.

`month_day` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.md.members">[[time.cal.md.members]]</a>

``` cpp
constexpr month_day(const chrono::month& m, const chrono::day& d) noexcept;
```

*Effects:* Initializes `m_` with `m`, and `d_` with `d`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr chrono::day day() const noexcept;
```

*Returns:* `d_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `true` if `m_.ok()` is `true`, `1d <= d_`, and `d_` is less
than or equal to the number of days in month `m_`; otherwise returns
`false`. When `m_ == February`, the number of days is considered to be
29.

#### Non-member functions <a id="time.cal.md.nonmembers">[[time.cal.md.nonmembers]]</a>

``` cpp
constexpr bool operator==(const month_day& x, const month_day& y) noexcept;
```

*Returns:* `x.month() == y.month() && x.day() == y.day()`.

``` cpp
constexpr strong_ordering operator<=>(const month_day& x, const month_day& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
if (auto c = x.month() <=> y.month(); c != 0) return c;
return x.day() <=> y.day();
```

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const month_day& md);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}/{}"),
                    md.month(), md.day());
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                month_day& md, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `month_day`
`md` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid `month_day`,
`is.setstate(ios_base::failbit)` is called and `md` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

### Class `month_day_last` <a id="time.cal.mdlast">[[time.cal.mdlast]]</a>

``` cpp
namespace std::chrono {
  class month_day_last {
    chrono::month m_;                   // exposition only

  public:
    constexpr explicit month_day_last(const chrono::month& m) noexcept;

    constexpr chrono::month month() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`month_day_last` represents the last day of a month.

[*Note 1*: A `month_day_last` object can be constructed using the
expression `m/last` or `last/m`, where `m` is an expression of type
`month`. — *end note*\]

[*Example 1*:

``` cpp
constexpr auto mdl = February/last;     // mdl is the last day of February of an as yet unspecified year
static_assert(mdl.month() == February);
```

— *end example*\]

`month_day_last` is a trivially copyable and standard-layout class type.

``` cpp
constexpr explicit month_day_last(const chrono::month& m) noexcept;
```

*Effects:* Initializes `m_` with `m`.

``` cpp
constexpr month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `m_.ok()`.

``` cpp
constexpr bool operator==(const month_day_last& x, const month_day_last& y) noexcept;
```

*Returns:* `x.month() == y.month()`.

``` cpp
constexpr strong_ordering operator<=>(const month_day_last& x, const month_day_last& y) noexcept;
```

*Returns:* `x.month() <=> y.month()`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const month_day_last& mdl);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}/last"), mdl.month());
```

### Class `month_weekday` <a id="time.cal.mwd">[[time.cal.mwd]]</a>

#### Overview <a id="time.cal.mwd.overview">[[time.cal.mwd.overview]]</a>

``` cpp
namespace std::chrono {
  class month_weekday {
    chrono::month           m_;         // exposition only
    chrono::weekday_indexed wdi_;       // exposition only
  public:
    constexpr month_weekday(const chrono::month& m, const chrono::weekday_indexed& wdi) noexcept;

    constexpr chrono::month           month()           const noexcept;
    constexpr chrono::weekday_indexed weekday_indexed() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`month_weekday` represents the nᵗʰ weekday of a month, of an as yet
unspecified year. To do this the `month_weekday` stores a `month` and a
`weekday_indexed`.

[*Example 1*:

``` cpp
constexpr auto mwd
    = February/Tuesday[3];              // mwd is the third Tuesday of February of an as yet unspecified year
static_assert(mwd.month() == February);
static_assert(mwd.weekday_indexed() == Tuesday[3]);
```

— *end example*\]

`month_weekday` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.mwd.members">[[time.cal.mwd.members]]</a>

``` cpp
constexpr month_weekday(const chrono::month& m, const chrono::weekday_indexed& wdi) noexcept;
```

*Effects:* Initializes `m_` with `m`, and `wdi_` with `wdi`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr chrono::weekday_indexed weekday_indexed() const noexcept;
```

*Returns:* `wdi_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `m_.ok() && wdi_.ok()`.

#### Non-member functions <a id="time.cal.mwd.nonmembers">[[time.cal.mwd.nonmembers]]</a>

``` cpp
constexpr bool operator==(const month_weekday& x, const month_weekday& y) noexcept;
```

*Returns:*
`x.month() == y.month() && x.weekday_indexed() == y.weekday_indexed()`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const month_weekday& mwd);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}/{:L}"),
                    mwd.month(), mwd.weekday_indexed());
```

### Class `month_weekday_last` <a id="time.cal.mwdlast">[[time.cal.mwdlast]]</a>

#### Overview <a id="time.cal.mwdlast.overview">[[time.cal.mwdlast.overview]]</a>

``` cpp
namespace std::chrono {
  class month_weekday_last {
    chrono::month        m_;    // exposition only
    chrono::weekday_last wdl_;  // exposition only
  public:
    constexpr month_weekday_last(const chrono::month& m,
                                 const chrono::weekday_last& wdl) noexcept;

    constexpr chrono::month        month()        const noexcept;
    constexpr chrono::weekday_last weekday_last() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`month_weekday_last` represents the last weekday of a month, of an as
yet unspecified year. To do this the `month_weekday_last` stores a
`month` and a `weekday_last`.

[*Example 1*:

``` cpp
constexpr auto mwd
    = February/Tuesday[last];   // mwd is the last Tuesday of February of an as yet unspecified year
static_assert(mwd.month() == February);
static_assert(mwd.weekday_last() == Tuesday[last]);
```

— *end example*\]

`month_weekday_last` is a trivially copyable and standard-layout class
type.

#### Member functions <a id="time.cal.mwdlast.members">[[time.cal.mwdlast.members]]</a>

``` cpp
constexpr month_weekday_last(const chrono::month& m,
                             const chrono::weekday_last& wdl) noexcept;
```

*Effects:* Initializes `m_` with `m`, and `wdl_` with `wdl`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr chrono::weekday_last weekday_last() const noexcept;
```

*Returns:* `wdl_`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `m_.ok() && wdl_.ok()`.

#### Non-member functions <a id="time.cal.mwdlast.nonmembers">[[time.cal.mwdlast.nonmembers]]</a>

``` cpp
constexpr bool operator==(const month_weekday_last& x, const month_weekday_last& y) noexcept;
```

*Returns:*
`x.month() == y.month() && x.weekday_last() == y.weekday_last()`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const month_weekday_last& mwdl);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L}/{:L}"),
                    mwdl.month(), mwdl.weekday_last());
```

### Class `year_month` <a id="time.cal.ym">[[time.cal.ym]]</a>

#### Overview <a id="time.cal.ym.overview">[[time.cal.ym.overview]]</a>

``` cpp
namespace std::chrono {
  class year_month {
    chrono::year  y_;           // exposition only
    chrono::month m_;           // exposition only

  public:
    year_month() = default;
    constexpr year_month(const chrono::year& y, const chrono::month& m) noexcept;

    constexpr chrono::year  year()  const noexcept;
    constexpr chrono::month month() const noexcept;

    constexpr year_month& operator+=(const months& dm) noexcept;
    constexpr year_month& operator-=(const months& dm) noexcept;
    constexpr year_month& operator+=(const years& dy)  noexcept;
    constexpr year_month& operator-=(const years& dy)  noexcept;

    constexpr bool ok() const noexcept;
  };
}
```

`year_month` represents a specific month of a specific year, but with an
unspecified day. `year_month` is a field-based time point with a
resolution of `months`. `year_month` meets the *Cpp17EqualityComparable*
( [[cpp17.equalitycomparable]]) and *Cpp17LessThanComparable* (
[[cpp17.lessthancomparable]]) requirements.

`year_month` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.ym.members">[[time.cal.ym.members]]</a>

``` cpp
constexpr year_month(const chrono::year& y, const chrono::month& m) noexcept;
```

*Effects:* Initializes `y_` with `y`, and `m_` with `m`.

``` cpp
constexpr chrono::year year() const noexcept;
```

*Returns:* `y_`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr year_month& operator+=(const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this + dm`.

*Returns:* `*this`.

``` cpp
constexpr year_month& operator-=(const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this - dm`.

*Returns:* `*this`.

``` cpp
constexpr year_month& operator+=(const years& dy) noexcept;
```

*Effects:* `*this = *this + dy`.

*Returns:* `*this`.

``` cpp
constexpr year_month& operator-=(const years& dy) noexcept;
```

*Effects:* `*this = *this - dy`.

*Returns:* `*this`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `y_.ok() && m_.ok()`.

#### Non-member functions <a id="time.cal.ym.nonmembers">[[time.cal.ym.nonmembers]]</a>

``` cpp
constexpr bool operator==(const year_month& x, const year_month& y) noexcept;
```

*Returns:* `x.year() == y.year() && x.month() == y.month()`.

``` cpp
constexpr strong_ordering operator<=>(const year_month& x, const year_month& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
if (auto c = x.year() <=> y.year(); c != 0) return c;
return x.month() <=> y.month();
```

``` cpp
constexpr year_month operator+(const year_month& ym, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* A `year_month` value `z` such that `z.ok() && z - ym == dm`
is `true`.

*Complexity:* 𝑂(1) with respect to the value of `dm`.

``` cpp
constexpr year_month operator+(const months& dm, const year_month& ym) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ym + dm`.

``` cpp
constexpr year_month operator-(const year_month& ym, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ym + -dm`.

``` cpp
constexpr months operator-(const year_month& x, const year_month& y) noexcept;
```

*Returns:*

``` cpp
x.year() - y.year() + months{static_cast<int>(unsigned{x.month()}) -
                             static_cast<int>(unsigned{y.month()})}
```

``` cpp
constexpr year_month operator+(const year_month& ym, const years& dy) noexcept;
```

*Returns:* `(ym.year() + dy) / ym.month()`.

``` cpp
constexpr year_month operator+(const years& dy, const year_month& ym) noexcept;
```

*Returns:* `ym + dy`.

``` cpp
constexpr year_month operator-(const year_month& ym, const years& dy) noexcept;
```

*Returns:* `ym + -dy`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const year_month& ym);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{}/{:L}"),
                    ym.year(), ym.month());
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                year_month& ym, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the `year_month`
`ym` using the format flags given in the NTCTS `fmt` as specified in
[[time.parse]]. If the parse fails to decode a valid `year_month`,
`is.setstate(ios_base::failbit)` is called and `ym` is not modified. If
`%Z` is used and successfully parsed, that value will be assigned to
`*abbrev` if `abbrev` is non-null. If `%z` (or a modified variant) is
used and successfully parsed, that value will be assigned to `*offset`
if `offset` is non-null.

*Returns:* `is`.

### Class `year_month_day` <a id="time.cal.ymd">[[time.cal.ymd]]</a>

#### Overview <a id="time.cal.ymd.overview">[[time.cal.ymd.overview]]</a>

``` cpp
namespace std::chrono {
  class year_month_day {
    chrono::year  y_;           // exposition only
    chrono::month m_;           // exposition only
    chrono::day   d_;           // exposition only

  public:
    year_month_day() = default;
    constexpr year_month_day(const chrono::year& y, const chrono::month& m,
                             const chrono::day& d) noexcept;
    constexpr year_month_day(const year_month_day_last& ymdl) noexcept;
    constexpr year_month_day(const sys_days& dp) noexcept;
    constexpr explicit year_month_day(const local_days& dp) noexcept;

    constexpr year_month_day& operator+=(const months& m) noexcept;
    constexpr year_month_day& operator-=(const months& m) noexcept;
    constexpr year_month_day& operator+=(const years& y)  noexcept;
    constexpr year_month_day& operator-=(const years& y)  noexcept;

    constexpr chrono::year  year()  const noexcept;
    constexpr chrono::month month() const noexcept;
    constexpr chrono::day   day()   const noexcept;

    constexpr          operator sys_days()   const noexcept;
    constexpr explicit operator local_days() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`year_month_day` represents a specific year, month, and day.
`year_month_day` is a field-based time point with a resolution of
`days`.

[*Note 1*: `year_month_day` supports `years`- and `months`-oriented
arithmetic, but not `days`-oriented arithmetic. For the latter, there is
a conversion to `sys_days`, which efficiently supports `days`-oriented
arithmetic. — *end note*\]

`year_month_day` meets the *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) and *Cpp17LessThanComparable* (
[[cpp17.lessthancomparable]]) requirements.

`year_month_day` is a trivially copyable and standard-layout class type.

#### Member functions <a id="time.cal.ymd.members">[[time.cal.ymd.members]]</a>

``` cpp
constexpr year_month_day(const chrono::year& y, const chrono::month& m,
                         const chrono::day& d) noexcept;
```

*Effects:* Initializes `y_` with `y`, `m_` with `m`, and `d_` with `d`.

``` cpp
constexpr year_month_day(const year_month_day_last& ymdl) noexcept;
```

*Effects:* Initializes `y_` with `ymdl.year()`, `m_` with
`ymdl.month()`, and `d_` with `ymdl.day()`.

[*Note 1*: This conversion from `year_month_day_last` to
`year_month_day` can be more efficient than converting a
`year_month_day_last` to a `sys_days`, and then converting that
`sys_days` to a `year_month_day`. — *end note*\]

``` cpp
constexpr year_month_day(const sys_days& dp) noexcept;
```

*Effects:* Constructs an object of type `year_month_day` that
corresponds to the date represented by `dp`.

*Remarks:* For any value `ymd` of type `year_month_day` for which
`ymd.ok()` is `true`, `ymd == year_month_day{sys_days{ymd}}` is `true`.

``` cpp
constexpr explicit year_month_day(const local_days& dp) noexcept;
```

*Effects:* Equivalent to constructing with
`sys_days{dp.time_since_epoch()}`.

``` cpp
constexpr year_month_day& operator+=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this + m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_day& operator-=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this - m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_day& year_month_day::operator+=(const years& y) noexcept;
```

*Effects:* `*this = *this + y`.

*Returns:* `*this`.

``` cpp
constexpr year_month_day& year_month_day::operator-=(const years& y) noexcept;
```

*Effects:* `*this = *this - y`.

*Returns:* `*this`.

``` cpp
constexpr chrono::year year() const noexcept;
```

*Returns:* `y_`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr chrono::day day() const noexcept;
```

*Returns:* `d_`.

``` cpp
constexpr operator sys_days() const noexcept;
```

*Returns:* If `ok()`, returns a `sys_days` holding a count of days from
the `sys_days` epoch to `*this` (a negative value if `*this` represents
a date prior to the `sys_days` epoch). Otherwise, if
`y_.ok() && m_.ok()` is `true`, returns
`sys_days{y_/m_/1d} + (d_ - 1d)`. Otherwise the value returned is
unspecified.

*Remarks:* A `sys_days` in the range \[`days{-12687428}`,
`days{11248737}`\] which is converted to a `year_month_day` has the same
value when converted back to a `sys_days`.

[*Example 1*:

``` cpp
static_assert(year_month_day{sys_days{2017y/January/0}}  == 2016y/December/31);
static_assert(year_month_day{sys_days{2017y/January/31}} == 2017y/January/31);
static_assert(year_month_day{sys_days{2017y/January/32}} == 2017y/February/1);
```

— *end example*\]

``` cpp
constexpr explicit operator local_days() const noexcept;
```

*Returns:* `local_days{sys_days{*this}.time_since_epoch()}`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* If `y_.ok()` is `true`, and `m_.ok()` is `true`, and `d_` is
in the range \[`1d`, `(y_/m_/last).day()`\], then returns `true`;
otherwise returns `false`.

#### Non-member functions <a id="time.cal.ymd.nonmembers">[[time.cal.ymd.nonmembers]]</a>

``` cpp
constexpr bool operator==(const year_month_day& x, const year_month_day& y) noexcept;
```

*Returns:*
`x.year() == y.year() && x.month() == y.month() && x.day() == y.day()`.

``` cpp
constexpr strong_ordering operator<=>(const year_month_day& x, const year_month_day& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
if (auto c = x.year() <=> y.year(); c != 0) return c;
if (auto c = x.month() <=> y.month(); c != 0) return c;
return x.day() <=> y.day();
```

``` cpp
constexpr year_month_day operator+(const year_month_day& ymd, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `(ymd.year() / ymd.month() + dm) / ymd.day()`.

[*Note 1*: If `ymd.day()` is in the range \[`1d`, `28d`\], `ok()` will
return `true` for the resultant `year_month_day`. — *end note*\]

``` cpp
constexpr year_month_day operator+(const months& dm, const year_month_day& ymd) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymd + dm`.

``` cpp
constexpr year_month_day operator-(const year_month_day& ymd, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymd + (-dm)`.

``` cpp
constexpr year_month_day operator+(const year_month_day& ymd, const years& dy) noexcept;
```

*Returns:* `(ymd.year() + dy) / ymd.month() / ymd.day()`.

[*Note 2*: If `ymd.month()` is February and `ymd.day()` is not in the
range \[`1d`, `28d`\], `ok()` can return `false` for the resultant
`year_month_day`. — *end note*\]

``` cpp
constexpr year_month_day operator+(const years& dy, const year_month_day& ymd) noexcept;
```

*Returns:* `ymd + dy`.

``` cpp
constexpr year_month_day operator-(const year_month_day& ymd, const years& dy) noexcept;
```

*Returns:* `ymd + (-dy)`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const year_month_day& ymd);
```

*Effects:* Equivalent to:

``` cpp
return os << (ymd.ok() ?
  format(STATICALLY-WIDEN<charT>("{:%F}"), ymd) :
  format(STATICALLY-WIDEN<charT>("{:%F} is not a valid date"), ymd));
```

``` cpp
template<class charT, class traits, class Alloc = allocator<charT>>
  basic_istream<charT, traits>&
    from_stream(basic_istream<charT, traits>& is, const charT* fmt,
                year_month_day& ymd, basic_string<charT, traits, Alloc>* abbrev = nullptr,
                minutes* offset = nullptr);
```

*Effects:* Attempts to parse the input stream `is` into the
`year_month_day` `ymd` using the format flags given in the NTCTS `fmt`
as specified in [[time.parse]]. If the parse fails to decode a valid
`year_month_day`, `is.setstate(ios_base::failbit)` is called and `ymd`
is not modified. If `%Z` is used and successfully parsed, that value
will be assigned to `*abbrev` if `abbrev` is non-null. If `%z` (or a
modified variant) is used and successfully parsed, that value will be
assigned to `*offset` if `offset` is non-null.

*Returns:* `is`.

### Class `year_month_day_last` <a id="time.cal.ymdlast">[[time.cal.ymdlast]]</a>

#### Overview <a id="time.cal.ymdlast.overview">[[time.cal.ymdlast.overview]]</a>

``` cpp
namespace std::chrono {
  class year_month_day_last {
    chrono::year           y_;          // exposition only
    chrono::month_day_last mdl_;        // exposition only

  public:
    constexpr year_month_day_last(const chrono::year& y,
                                  const chrono::month_day_last& mdl) noexcept;

    constexpr year_month_day_last& operator+=(const months& m) noexcept;
    constexpr year_month_day_last& operator-=(const months& m) noexcept;
    constexpr year_month_day_last& operator+=(const years& y)  noexcept;
    constexpr year_month_day_last& operator-=(const years& y)  noexcept;

    constexpr chrono::year           year()           const noexcept;
    constexpr chrono::month          month()          const noexcept;
    constexpr chrono::month_day_last month_day_last() const noexcept;
    constexpr chrono::day            day()            const noexcept;

    constexpr          operator sys_days()   const noexcept;
    constexpr explicit operator local_days() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`year_month_day_last` represents the last day of a specific year and
month. `year_month_day_last` is a field-based time point with a
resolution of `days`, except that it is restricted to pointing to the
last day of a year and month.

[*Note 1*: `year_month_day_last` supports `years`- and
`months`-oriented arithmetic, but not `days`-oriented arithmetic. For
the latter, there is a conversion to `sys_days`, which efficiently
supports `days`-oriented arithmetic. — *end note*\]

`year_month_day_last` meets the *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) and *Cpp17LessThanComparable* (
[[cpp17.lessthancomparable]]) requirements.

`year_month_day_last` is a trivially copyable and standard-layout class
type.

#### Member functions <a id="time.cal.ymdlast.members">[[time.cal.ymdlast.members]]</a>

``` cpp
constexpr year_month_day_last(const chrono::year& y,
                              const chrono::month_day_last& mdl) noexcept;
```

*Effects:* Initializes `y_` with `y` and `mdl_` with `mdl`.

``` cpp
constexpr year_month_day_last& operator+=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this + m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_day_last& operator-=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this - m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_day_last& operator+=(const years& y) noexcept;
```

*Effects:* `*this = *this + y`.

*Returns:* `*this`.

``` cpp
constexpr year_month_day_last& operator-=(const years& y) noexcept;
```

*Effects:* `*this = *this - y`.

*Returns:* `*this`.

``` cpp
constexpr chrono::year year() const noexcept;
```

*Returns:* `y_`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `mdl_.month()`.

``` cpp
constexpr chrono::month_day_last month_day_last() const noexcept;
```

*Returns:* `mdl_`.

``` cpp
constexpr chrono::day day() const noexcept;
```

*Returns:* If `ok()` is `true`, returns a `day` representing the last
day of the (`year`, `month`) pair represented by `*this`. Otherwise, the
returned value is unspecified.

[*Note 1*: This value might be computed on demand. — *end note*\]

``` cpp
constexpr operator sys_days() const noexcept;
```

*Returns:* `sys_days{year()/month()/day()}`.

``` cpp
constexpr explicit operator local_days() const noexcept;
```

*Returns:* `local_days{sys_days{*this}.time_since_epoch()}`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `y_.ok() && mdl_.ok()`.

#### Non-member functions <a id="time.cal.ymdlast.nonmembers">[[time.cal.ymdlast.nonmembers]]</a>

``` cpp
constexpr bool operator==(const year_month_day_last& x, const year_month_day_last& y) noexcept;
```

*Returns:*
`x.year() == y.year() && x.month_day_last() == y.month_day_last()`.

``` cpp
constexpr strong_ordering operator<=>(const year_month_day_last& x,
                                      const year_month_day_last& y) noexcept;
```

*Effects:* Equivalent to:

``` cpp
if (auto c = x.year() <=> y.year(); c != 0) return c;
return x.month_day_last() <=> y.month_day_last();
```

``` cpp
constexpr year_month_day_last
  operator+(const year_month_day_last& ymdl, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `(ymdl.year() / ymdl.month() + dm) / last`.

``` cpp
constexpr year_month_day_last
  operator+(const months& dm, const year_month_day_last& ymdl) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymdl + dm`.

``` cpp
constexpr year_month_day_last
  operator-(const year_month_day_last& ymdl, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymdl + (-dm)`.

``` cpp
constexpr year_month_day_last
  operator+(const year_month_day_last& ymdl, const years& dy) noexcept;
```

*Returns:* `{ymdl.year()+dy, ymdl.month_day_last()}`.

``` cpp
constexpr year_month_day_last
  operator+(const years& dy, const year_month_day_last& ymdl) noexcept;
```

*Returns:* `ymdl + dy`.

``` cpp
constexpr year_month_day_last
  operator-(const year_month_day_last& ymdl, const years& dy) noexcept;
```

*Returns:* `ymdl + (-dy)`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const year_month_day_last& ymdl);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{}/{:L}"),
                    ymdl.year(), ymdl.month_day_last());
```

### Class `year_month_weekday` <a id="time.cal.ymwd">[[time.cal.ymwd]]</a>

#### Overview <a id="time.cal.ymwd.overview">[[time.cal.ymwd.overview]]</a>

``` cpp
namespace std::chrono {
  class year_month_weekday {
    chrono::year            y_;         // exposition only
    chrono::month           m_;         // exposition only
    chrono::weekday_indexed wdi_;       // exposition only

  public:
    year_month_weekday() = default;
    constexpr year_month_weekday(const chrono::year& y, const chrono::month& m,
                                 const chrono::weekday_indexed& wdi) noexcept;
    constexpr year_month_weekday(const sys_days& dp) noexcept;
    constexpr explicit year_month_weekday(const local_days& dp) noexcept;

    constexpr year_month_weekday& operator+=(const months& m) noexcept;
    constexpr year_month_weekday& operator-=(const months& m) noexcept;
    constexpr year_month_weekday& operator+=(const years& y)  noexcept;
    constexpr year_month_weekday& operator-=(const years& y)  noexcept;

    constexpr chrono::year            year()            const noexcept;
    constexpr chrono::month           month()           const noexcept;
    constexpr chrono::weekday         weekday()         const noexcept;
    constexpr unsigned                index()           const noexcept;
    constexpr chrono::weekday_indexed weekday_indexed() const noexcept;

    constexpr          operator sys_days()   const noexcept;
    constexpr explicit operator local_days() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`year_month_weekday` represents a specific year, month, and nᵗʰ weekday
of the month. `year_month_weekday` is a field-based time point with a
resolution of `days`.

[*Note 1*: `year_month_weekday` supports `years`- and `months`-oriented
arithmetic, but not `days`-oriented arithmetic. For the latter, there is
a conversion to `sys_days`, which efficiently supports `days`-oriented
arithmetic. — *end note*\]

`year_month_weekday` meets the *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) requirements.

`year_month_weekday` is a trivially copyable and standard-layout class
type.

#### Member functions <a id="time.cal.ymwd.members">[[time.cal.ymwd.members]]</a>

``` cpp
constexpr year_month_weekday(const chrono::year& y, const chrono::month& m,
                             const chrono::weekday_indexed& wdi) noexcept;
```

*Effects:* Initializes `y_` with `y`, `m_` with `m`, and `wdi_` with
`wdi`.

``` cpp
constexpr year_month_weekday(const sys_days& dp) noexcept;
```

*Effects:* Constructs an object of type `year_month_weekday` which
corresponds to the date represented by `dp`.

*Remarks:* For any value `ymwd` of type `year_month_weekday` for which
`ymwd.ok()` is `true`, `ymwd == year_month_weekday{sys_days{ymwd}}` is
`true`.

``` cpp
constexpr explicit year_month_weekday(const local_days& dp) noexcept;
```

*Effects:* Equivalent to constructing with
`sys_days{dp.time_since_epoch()}`.

``` cpp
constexpr year_month_weekday& operator+=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this + m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_weekday& operator-=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this - m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_weekday& operator+=(const years& y) noexcept;
```

*Effects:* `*this = *this + y`.

*Returns:* `*this`.

``` cpp
constexpr year_month_weekday& operator-=(const years& y) noexcept;
```

*Effects:* `*this = *this - y`.

*Returns:* `*this`.

``` cpp
constexpr chrono::year year() const noexcept;
```

*Returns:* `y_`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr chrono::weekday weekday() const noexcept;
```

*Returns:* `wdi_.weekday()`.

``` cpp
constexpr unsigned index() const noexcept;
```

*Returns:* `wdi_.index()`.

``` cpp
constexpr chrono::weekday_indexed weekday_indexed() const noexcept;
```

*Returns:* `wdi_`.

``` cpp
constexpr operator sys_days() const noexcept;
```

*Returns:* If `y_.ok() && m_.ok() && wdi_.weekday().ok()`, returns a
`sys_days` that represents the date `(index() - 1) * 7` days after the
first `weekday()` of `year()/month()`. If `index()` is 0 the returned
`sys_days` represents the date 7 days prior to the first `weekday()` of
`year()/month()`. Otherwise the returned value is unspecified.

``` cpp
constexpr explicit operator local_days() const noexcept;
```

*Returns:* `local_days{sys_days{*this}.time_since_epoch()}`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* If any of `y_.ok()`, `m_.ok()`, or `wdi_.ok()` is `false`,
returns `false`. Otherwise, if `*this` represents a valid date, returns
`true`. Otherwise, returns `false`.

#### Non-member functions <a id="time.cal.ymwd.nonmembers">[[time.cal.ymwd.nonmembers]]</a>

``` cpp
constexpr bool operator==(const year_month_weekday& x, const year_month_weekday& y) noexcept;
```

*Returns:*

``` cpp
x.year() == y.year() && x.month() == y.month() && x.weekday_indexed() == y.weekday_indexed()
```

``` cpp
constexpr year_month_weekday operator+(const year_month_weekday& ymwd, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `(ymwd.year() / ymwd.month() + dm) / ymwd.weekday_indexed()`.

``` cpp
constexpr year_month_weekday operator+(const months& dm, const year_month_weekday& ymwd) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymwd + dm`.

``` cpp
constexpr year_month_weekday operator-(const year_month_weekday& ymwd, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymwd + (-dm)`.

``` cpp
constexpr year_month_weekday operator+(const year_month_weekday& ymwd, const years& dy) noexcept;
```

*Returns:* `{ymwd.year()+dy, ymwd.month(), ymwd.weekday_indexed()}`.

``` cpp
constexpr year_month_weekday operator+(const years& dy, const year_month_weekday& ymwd) noexcept;
```

*Returns:* `ymwd + dy`.

``` cpp
constexpr year_month_weekday operator-(const year_month_weekday& ymwd, const years& dy) noexcept;
```

*Returns:* `ymwd + (-dy)`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const year_month_weekday& ymwd);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{}/{:L}/{:L}"),
                    ymwd.year(), ymwd.month(), ymwd.weekday_indexed());
```

### Class `year_month_weekday_last` <a id="time.cal.ymwdlast">[[time.cal.ymwdlast]]</a>

#### Overview <a id="time.cal.ymwdlast.overview">[[time.cal.ymwdlast.overview]]</a>

``` cpp
namespace std::chrono {
  class year_month_weekday_last {
    chrono::year         y_;    // exposition only
    chrono::month        m_;    // exposition only
    chrono::weekday_last wdl_;  // exposition only

  public:
    constexpr year_month_weekday_last(const chrono::year& y, const chrono::month& m,
                                      const chrono::weekday_last& wdl) noexcept;

    constexpr year_month_weekday_last& operator+=(const months& m) noexcept;
    constexpr year_month_weekday_last& operator-=(const months& m) noexcept;
    constexpr year_month_weekday_last& operator+=(const years& y)  noexcept;
    constexpr year_month_weekday_last& operator-=(const years& y)  noexcept;

    constexpr chrono::year         year()         const noexcept;
    constexpr chrono::month        month()        const noexcept;
    constexpr chrono::weekday      weekday()      const noexcept;
    constexpr chrono::weekday_last weekday_last() const noexcept;

    constexpr          operator sys_days()   const noexcept;
    constexpr explicit operator local_days() const noexcept;
    constexpr bool ok() const noexcept;
  };
}
```

`year_month_weekday_last` represents a specific year, month, and last
weekday of the month. `year_month_weekday_last` is a field-based time
point with a resolution of `days`, except that it is restricted to
pointing to the last weekday of a year and month.

[*Note 1*: `year_month_weekday_last` supports `years`- and
`months`-oriented arithmetic, but not `days`-oriented arithmetic. For
the latter, there is a conversion to `sys_days`, which efficiently
supports `days`-oriented arithmetic. — *end note*\]

`year_month_weekday_last` meets the *Cpp17EqualityComparable* (
[[cpp17.equalitycomparable]]) requirements.

`year_month_weekday_last` is a trivially copyable and standard-layout
class type.

#### Member functions <a id="time.cal.ymwdlast.members">[[time.cal.ymwdlast.members]]</a>

``` cpp
constexpr year_month_weekday_last(const chrono::year& y, const chrono::month& m,
                                  const chrono::weekday_last& wdl) noexcept;
```

*Effects:* Initializes `y_` with `y`, `m_` with `m`, and `wdl_` with
`wdl`.

``` cpp
constexpr year_month_weekday_last& operator+=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this + m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_weekday_last& operator-=(const months& m) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Effects:* `*this = *this - m`.

*Returns:* `*this`.

``` cpp
constexpr year_month_weekday_last& operator+=(const years& y) noexcept;
```

*Effects:* `*this = *this + y`.

*Returns:* `*this`.

``` cpp
constexpr year_month_weekday_last& operator-=(const years& y) noexcept;
```

*Effects:* `*this = *this - y`.

*Returns:* `*this`.

``` cpp
constexpr chrono::year year() const noexcept;
```

*Returns:* `y_`.

``` cpp
constexpr chrono::month month() const noexcept;
```

*Returns:* `m_`.

``` cpp
constexpr chrono::weekday weekday() const noexcept;
```

*Returns:* `wdl_.weekday()`.

``` cpp
constexpr chrono::weekday_last weekday_last() const noexcept;
```

*Returns:* `wdl_`.

``` cpp
constexpr operator sys_days() const noexcept;
```

*Returns:* If `ok() == true`, returns a `sys_days` that represents the
last `weekday()` of `year()/month()`. Otherwise the returned value is
unspecified.

``` cpp
constexpr explicit operator local_days() const noexcept;
```

*Returns:* `local_days{sys_days{*this}.time_since_epoch()}`.

``` cpp
constexpr bool ok() const noexcept;
```

*Returns:* `y_.ok() && m_.ok() && wdl_.ok()`.

#### Non-member functions <a id="time.cal.ymwdlast.nonmembers">[[time.cal.ymwdlast.nonmembers]]</a>

``` cpp
constexpr bool operator==(const year_month_weekday_last& x,
                          const year_month_weekday_last& y) noexcept;
```

*Returns:*

``` cpp
x.year() == y.year() && x.month() == y.month() && x.weekday_last() == y.weekday_last()
```

``` cpp
constexpr year_month_weekday_last
  operator+(const year_month_weekday_last& ymwdl, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `(ymwdl.year() / ymwdl.month() + dm) / ymwdl.weekday_last()`.

``` cpp
constexpr year_month_weekday_last
  operator+(const months& dm, const year_month_weekday_last& ymwdl) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymwdl + dm`.

``` cpp
constexpr year_month_weekday_last
  operator-(const year_month_weekday_last& ymwdl, const months& dm) noexcept;
```

*Constraints:* If the argument supplied by the caller for the `months`
parameter is convertible to `years`, its implicit conversion sequence to
`years` is worse than its implicit conversion sequence to
`months`[[over.ics.rank]].

*Returns:* `ymwdl + (-dm)`.

``` cpp
constexpr year_month_weekday_last
  operator+(const year_month_weekday_last& ymwdl, const years& dy) noexcept;
```

*Returns:* `{ymwdl.year()+dy, ymwdl.month(), ymwdl.weekday_last()}`.

``` cpp
constexpr year_month_weekday_last
  operator+(const years& dy, const year_month_weekday_last& ymwdl) noexcept;
```

*Returns:* `ymwdl + dy`.

``` cpp
constexpr year_month_weekday_last
  operator-(const year_month_weekday_last& ymwdl, const years& dy) noexcept;
```

*Returns:* `ymwdl + (-dy)`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const year_month_weekday_last& ymwdl);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{}/{:L}/{:L}"),
                    ymwdl.year(), ymwdl.month(), ymwdl.weekday_last());
```

### Conventional syntax operators <a id="time.cal.operators">[[time.cal.operators]]</a>

A set of overloaded `operator/` functions provides a conventional syntax
for the creation of civil calendar dates.

[*Note 1*:

The year, month, and day are accepted in any of the following 3 orders:

``` cpp
year/month/day
month/day/year
day/month/year
```

Anywhere a `day` is required, any of the following can also be
specified:

``` cpp
last
weekday[i]
weekday[last]
```

— *end note*\]

[*Note 2*:

Partial-date types such as `year_month` and `month_day` can be created
by not applying the second division operator for any of the three
orders. For example:

``` cpp
year_month ym = 2015y/April;
month_day md1 = April/4;
month_day md2 = 4d/April;
```

— *end note*\]

[*Example 1*:

``` cpp
auto a = 2015/4/4;          // a == int(125)
auto b = 2015y/4/4;         // b == year_month_day{year(2015), month(4), day(4)}
auto c = 2015y/4d/April;    // error: no viable operator/ for first /
auto d = 2015/April/4;      // error: no viable operator/ for first /
```

— *end example*\]

``` cpp
constexpr year_month
  operator/(const year& y, const month& m) noexcept;
```

*Returns:* `{y, m}`.

``` cpp
constexpr year_month
  operator/(const year& y, int   m) noexcept;
```

*Returns:* `y / month(m)`.

``` cpp
constexpr month_day
  operator/(const month& m, const day& d) noexcept;
```

*Returns:* `{m, d}`.

``` cpp
constexpr month_day
  operator/(const month& m, int d) noexcept;
```

*Returns:* `m / day(d)`.

``` cpp
constexpr month_day
  operator/(int m, const day& d) noexcept;
```

*Returns:* `month(m) / d`.

``` cpp
constexpr month_day
  operator/(const day& d, const month& m) noexcept;
```

*Returns:* `m / d`.

``` cpp
constexpr month_day
  operator/(const day& d, int m) noexcept;
```

*Returns:* `month(m) / d`.

``` cpp
constexpr month_day_last
  operator/(const month& m, last_spec) noexcept;
```

*Returns:* `month_day_last{m}`.

``` cpp
constexpr month_day_last
  operator/(int m, last_spec) noexcept;
```

*Returns:* `month(m) / last`.

``` cpp
constexpr month_day_last
  operator/(last_spec, const month& m) noexcept;
```

*Returns:* `m / last`.

``` cpp
constexpr month_day_last
  operator/(last_spec, int m) noexcept;
```

*Returns:* `month(m) / last`.

``` cpp
constexpr month_weekday
  operator/(const month& m, const weekday_indexed& wdi) noexcept;
```

*Returns:* `{m, wdi}`.

``` cpp
constexpr month_weekday
  operator/(int m, const weekday_indexed& wdi) noexcept;
```

*Returns:* `month(m) / wdi`.

``` cpp
constexpr month_weekday
  operator/(const weekday_indexed& wdi, const month& m) noexcept;
```

*Returns:* `m / wdi`.

``` cpp
constexpr month_weekday
  operator/(const weekday_indexed& wdi, int m) noexcept;
```

*Returns:* `month(m) / wdi`.

``` cpp
constexpr month_weekday_last
  operator/(const month& m, const weekday_last& wdl) noexcept;
```

*Returns:* `{m, wdl}`.

``` cpp
constexpr month_weekday_last
  operator/(int m, const weekday_last& wdl) noexcept;
```

*Returns:* `month(m) / wdl`.

``` cpp
constexpr month_weekday_last
  operator/(const weekday_last& wdl, const month& m) noexcept;
```

*Returns:* `m / wdl`.

``` cpp
constexpr month_weekday_last
  operator/(const weekday_last& wdl, int m) noexcept;
```

*Returns:* `month(m) / wdl`.

``` cpp
constexpr year_month_day
  operator/(const year_month& ym, const day& d) noexcept;
```

*Returns:* `{ym.year(), ym.month(), d}`.

``` cpp
constexpr year_month_day
  operator/(const year_month& ym, int d) noexcept;
```

*Returns:* `ym / day(d)`.

``` cpp
constexpr year_month_day
  operator/(const year& y, const month_day& md) noexcept;
```

*Returns:* `y / md.month() / md.day()`.

``` cpp
constexpr year_month_day
  operator/(int y, const month_day& md) noexcept;
```

*Returns:* `year(y) / md`.

``` cpp
constexpr year_month_day
  operator/(const month_day& md, const year& y) noexcept;
```

*Returns:* `y / md`.

``` cpp
constexpr year_month_day
  operator/(const month_day& md, int y) noexcept;
```

*Returns:* `year(y) / md`.

``` cpp
constexpr year_month_day_last
  operator/(const year_month& ym, last_spec) noexcept;
```

*Returns:* `{ym.year(), month_day_last{ym.month()}}`.

``` cpp
constexpr year_month_day_last
  operator/(const year& y, const month_day_last& mdl) noexcept;
```

*Returns:* `{y, mdl}`.

``` cpp
constexpr year_month_day_last
  operator/(int y, const month_day_last& mdl) noexcept;
```

*Returns:* `year(y) / mdl`.

``` cpp
constexpr year_month_day_last
  operator/(const month_day_last& mdl, const year& y) noexcept;
```

*Returns:* `y / mdl`.

``` cpp
constexpr year_month_day_last
  operator/(const month_day_last& mdl, int y) noexcept;
```

*Returns:* `year(y) / mdl`.

``` cpp
constexpr year_month_weekday
  operator/(const year_month& ym, const weekday_indexed& wdi) noexcept;
```

*Returns:* `{ym.year(), ym.month(), wdi}`.

``` cpp
constexpr year_month_weekday
  operator/(const year& y, const month_weekday& mwd) noexcept;
```

*Returns:* `{y, mwd.month(), mwd.weekday_indexed()}`.

``` cpp
constexpr year_month_weekday
  operator/(int y, const month_weekday& mwd) noexcept;
```

*Returns:* `year(y) / mwd`.

``` cpp
constexpr year_month_weekday
  operator/(const month_weekday& mwd, const year& y) noexcept;
```

*Returns:* `y / mwd`.

``` cpp
constexpr year_month_weekday
  operator/(const month_weekday& mwd, int y) noexcept;
```

*Returns:* `year(y) / mwd`.

``` cpp
constexpr year_month_weekday_last
  operator/(const year_month& ym, const weekday_last& wdl) noexcept;
```

*Returns:* `{ym.year(), ym.month(), wdl}`.

``` cpp
constexpr year_month_weekday_last
  operator/(const year& y, const month_weekday_last& mwdl) noexcept;
```

*Returns:* `{y, mwdl.month(), mwdl.weekday_last()}`.

``` cpp
constexpr year_month_weekday_last
  operator/(int y, const month_weekday_last& mwdl) noexcept;
```

*Returns:* `year(y) / mwdl`.

``` cpp
constexpr year_month_weekday_last
  operator/(const month_weekday_last& mwdl, const year& y) noexcept;
```

*Returns:* `y / mwdl`.

``` cpp
constexpr year_month_weekday_last
  operator/(const month_weekday_last& mwdl, int y) noexcept;
```

*Returns:* `year(y) / mwdl`.

## Class template `hh_mm_ss` <a id="time.hms">[[time.hms]]</a>

### Overview <a id="time.hms.overview">[[time.hms.overview]]</a>

``` cpp
namespace std::chrono {
  template<class Duration> class hh_mm_ss {
  public:
    static constexpr unsigned fractional_width = see below;
    using precision                            = see below;

    constexpr hh_mm_ss() noexcept : hh_mm_ss{Duration::zero()} {}
    constexpr explicit hh_mm_ss(Duration d);

    constexpr bool is_negative() const noexcept;
    constexpr chrono::hours hours() const noexcept;
    constexpr chrono::minutes minutes() const noexcept;
    constexpr chrono::seconds seconds() const noexcept;
    constexpr precision subseconds() const noexcept;

    constexpr explicit operator precision() const noexcept;
    constexpr precision to_duration() const noexcept;

  private:
    bool            is_neg;     // exposition only
    chrono::hours   h;          // exposition only
    chrono::minutes m;          // exposition only
    chrono::seconds s;          // exposition only
    precision       ss;         // exposition only
  };
}
```

The `hh_mm_ss` class template splits a `duration` into a multi-field
time structure *hours*:*minutes*:*seconds* and possibly *subseconds*,
where *subseconds* will be a duration unit based on a non-positive power
of 10. The `Duration` template parameter dictates the precision to which
the time is split. A `hh_mm_ss` models negative durations with a
distinct `is_negative` getter that returns `true` when the input
duration is negative. The individual duration fields always return
non-negative durations even when `is_negative()` indicates the structure
is representing a negative duration.

If `Duration` is not a specialization of `duration`, the program is
ill-formed.

### Members <a id="time.hms.members">[[time.hms.members]]</a>

``` cpp
static constexpr unsigned fractional_width = see below;
```

`fractional_width` is the number of fractional decimal digits
represented by `precision`. `fractional_width` has the value of the
smallest possible integer in the range \[`0`, `18`\] such that
`precision` will exactly represent all values of `Duration`. If no such
value of `fractional_width` exists, then `fractional_width` is 6.

[*Example 1*:

See  [[time.hms.width]] for some durations, the resulting
`fractional_width`, and the formatted fractional second output of
`Duration{1}`.

**Table: Examples for `fractional_width`**

|                                   |     |               |
| --------------------------------- | --- | ------------- |
| `hours`, `minutes`, and `seconds` | `0` |               |
| `milliseconds`                    | `3` | `0.001`       |
| `microseconds`                    | `6` | `0.000001`    |
| `nanoseconds`                     | `9` | `0.000000001` |
| `duration<int, ratio<1, 2>>`      | `1` | `0.5`         |
| `duration<int, ratio<1, 3>>`      | `6` | `0.333333`    |
| `duration<int, ratio<1, 4>>`      | `2` | `0.25`        |
| `duration<int, ratio<1, 5>>`      | `1` | `0.2`         |
| `duration<int, ratio<1, 6>>`      | `6` | `0.166666`    |
| `duration<int, ratio<1, 7>>`      | `6` | `0.142857`    |
| `duration<int, ratio<1, 8>>`      | `3` | `0.125`       |
| `duration<int, ratio<1, 9>>`      | `6` | `0.111111`    |
| `duration<int, ratio<1, 10>>`     | `1` | `0.1`         |
| `duration<int, ratio<756, 625>>`  | `4` | `0.2096`      |


— *end example*\]

``` cpp
using precision = see below;
```

`precision` is

``` cpp
duration<common_type_t<Duration::rep, seconds::rep>, ratio<1, $10^fractional_width$>>
```

``` cpp
constexpr explicit hh_mm_ss(Duration d);
```

*Effects:* Constructs an object of type `hh_mm_ss` which represents the
`Duration d` with precision `precision`.

- Initializes `is_neg` with `d < Duration::zero()`.
- Initializes `h` with `duration_cast<chrono::hours>(abs(d))`.
- Initializes `m` with
  `duration_cast<chrono::minutes>(abs(d) - hours())`.
- Initializes `s` with
  `duration_cast<chrono::seconds>(abs(d) - hours() - minutes())`.
- If `treat_as_floating_point_v<precision::rep>` is `true`, initializes
  `ss` with `abs(d) - hours() - minutes() - seconds()`. Otherwise,
  initializes `ss` with
  `duration_cast<precision>(abs(d) - hours() - minutes() - seconds())`.

[*Note 1*: When `precision::rep` is integral and `precision::period` is
`ratio<1>`, `subseconds()` always returns a value equal to
`0s`. — *end note*\]

*Ensures:* If `treat_as_floating_point_v<precision::rep>` is `true`,
`to_duration()` returns `d`, otherwise `to_duration()` returns
`duration_cast<precision>(d)`.

``` cpp
constexpr bool is_negative() const noexcept;
```

*Returns:* `is_neg`.

``` cpp
constexpr chrono::hours hours() const noexcept;
```

*Returns:* `h`.

``` cpp
constexpr chrono::minutes minutes() const noexcept;
```

*Returns:* `m`.

``` cpp
constexpr chrono::seconds seconds() const noexcept;
```

*Returns:* `s`.

``` cpp
constexpr precision subseconds() const noexcept;
```

*Returns:* `ss`.

``` cpp
constexpr precision to_duration() const noexcept;
```

*Returns:* If `is_neg`, returns `-(h + m + s + ss)`, otherwise returns
`h + m + s + ss`.

``` cpp
constexpr explicit operator precision() const noexcept;
```

*Returns:* `to_duration()`.

### Non-members <a id="time.hms.nonmembers">[[time.hms.nonmembers]]</a>

``` cpp
template<class charT, class traits, class Duration>
basic_ostream<charT, traits>&
operator<<(basic_ostream<charT, traits>& os, const hh_mm_ss<Duration>& hms);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%T}"), hms);
```

[*Example 1*:

``` cpp
for (auto ms : {-4083007ms, 4083007ms, 65745123ms}) {
  hh_mm_ss hms{ms};
  cout << hms << '\n';
}
cout << hh_mm_ss{65745s} << '\n';
```

Produces the output (assuming the "C" locale):

``` cpp
-01:08:03.007
01:08:03.007
18:15:45.123
18:15:45
```

— *end example*\]

## 12/24 hours functions <a id="time.12">[[time.12]]</a>

These functions aid in translating between a 12h format time of day and
a 24h format time of day.

``` cpp
constexpr bool is_am(const hours& h) noexcept;
```

*Returns:* `0h <= h && h <= 11h`.

``` cpp
constexpr bool is_pm(const hours& h) noexcept;
```

*Returns:* `12h <= h && h <= 23h`.

``` cpp
constexpr hours make12(const hours& h) noexcept;
```

*Returns:* The 12-hour equivalent of `h` in the range \[`1h`, `12h`\].
If `h` is not in the range \[`0h`, `23h`\], the value returned is
unspecified.

``` cpp
constexpr hours make24(const hours& h, bool is_pm) noexcept;
```

*Returns:* If `is_pm` is `false`, returns the 24-hour equivalent of `h`
in the range \[`0h`, `11h`\], assuming `h` represents an ante meridiem
hour. Otherwise, returns the 24-hour equivalent of `h` in the range
\[`12h`, `23h`\], assuming `h` represents a post meridiem hour. If `h`
is not in the range \[`1h`, `12h`\], the value returned is unspecified.

## Time zones <a id="time.zone">[[time.zone]]</a>

### In general <a id="time.zone.general">[[time.zone.general]]</a>

[[time.zone]] describes an interface for accessing the IANA Time Zone
Database that interoperates with `sys_time` and `local_time`. This
interface provides time zone support to both the civil calendar types
[[time.cal]] and to user-defined calendars.

### Time zone database <a id="time.zone.db">[[time.zone.db]]</a>

#### Class `tzdb` <a id="time.zone.db.tzdb">[[time.zone.db.tzdb]]</a>

``` cpp
namespace std::chrono {
  struct tzdb {
    string                 version;
    vector<time_zone>      zones;
    vector<time_zone_link> links;
    vector<leap_second>    leap_seconds;

    const time_zone* locate_zone(string_view tz_name) const;
    const time_zone* current_zone() const;
  };
}
```

Each `vector` in a `tzdb` object is sorted to enable fast lookup.

``` cpp
const time_zone* locate_zone(string_view tz_name) const;
```

*Returns:*

- If `zones` contains an element `tz` for which `tz.name() == tz_name`,
  a pointer to `tz`;
- otherwise, if `links` contains an element `tz_l` for which
  `tz_l.name() == tz_name`, then a pointer to the element `tz` of
  `zones` for which `tz.name() == tz_l.target()`.

[*Note 1*: A `time_zone_link` specifies an alternative name for a
`time_zone`. — *end note*\]

*Throws:* If a `const time_zone*` cannot be found as described in the
*Returns:* element, throws a `runtime_error`.

[*Note 2*: On non-exceptional return, the return value is always a
pointer to a valid `time_zone`. — *end note*\]

``` cpp
const time_zone* current_zone() const;
```

*Returns:* A pointer to the time zone which the computer has set as its
local time zone.

#### Class `tzdb_list` <a id="time.zone.db.list">[[time.zone.db.list]]</a>

``` cpp
namespace std::chrono {
  class tzdb_list {
  public:
    tzdb_list(const tzdb_list&) = delete;
    tzdb_list& operator=(const tzdb_list&) = delete;

    // unspecified additional constructors

    class const_iterator;

    const tzdb& front() const noexcept;

    const_iterator erase_after(const_iterator p);

    const_iterator begin() const noexcept;
    const_iterator end()   const noexcept;

    const_iterator cbegin() const noexcept;
    const_iterator cend()   const noexcept;
  };
}
```

The `tzdb_list` database is a singleton; the unique object of type
`tzdb_list` can be accessed via the `get_tzdb_list()` function.

[*Note 1*: This access is only needed for those applications that need
to have long uptimes and have a need to update the time zone database
while running. Other applications can implicitly access the `front()` of
this list via the read-only namespace scope functions `get_tzdb()`,
`locate_zone()`, and `current_zone()`. — *end note*\]

The `tzdb_list` object contains a list of `tzdb` objects.

`tzdb_list::const_iterator` is a constant iterator which meets the
*Cpp17ForwardIterator* requirements and has a value type of `tzdb`.

``` cpp
const tzdb& front() const noexcept;
```

*Synchronization:* This operation is thread-safe with respect to
`reload_tzdb()`.

[*Note 1*: `reload_tzdb()` pushes a new `tzdb` onto the front of this
container. — *end note*\]

*Returns:* A reference to the first `tzdb` in the container.

``` cpp
const_iterator erase_after(const_iterator p);
```

*Preconditions:* The iterator following `p` is dereferenceable.

*Effects:* Erases the `tzdb` referred to by the iterator following `p`.

*Ensures:* No pointers, references, or iterators are invalidated except
those referring to the erased `tzdb`.

[*Note 2*: It is not possible to erase the `tzdb` referred to by
`begin()`. — *end note*\]

*Returns:* An iterator pointing to the element following the one that
was erased, or `end()` if no such element exists.

*Throws:* Nothing.

``` cpp
const_iterator begin() const noexcept;
```

*Returns:* An iterator referring to the first `tzdb` in the container.

``` cpp
const_iterator end() const noexcept;
```

*Returns:* An iterator referring to the position one past the last
`tzdb` in the container.

``` cpp
const_iterator cbegin() const noexcept;
```

*Returns:* `begin()`.

``` cpp
const_iterator cend() const noexcept;
```

*Returns:* `end()`.

#### Time zone database access <a id="time.zone.db.access">[[time.zone.db.access]]</a>

``` cpp
tzdb_list& get_tzdb_list();
```

*Effects:* If this is the first access to the time zone database,
initializes the database. If this call initializes the database, the
resulting database will be a `tzdb_list` holding a single initialized
`tzdb`.

*Synchronization:* It is safe to call this function from multiple
threads at one time.

*Returns:* A reference to the database.

*Throws:* `runtime_error` if for any reason a reference cannot be
returned to a valid `tzdb_list` containing one or more valid `tzdb`s.

``` cpp
const tzdb& get_tzdb();
```

*Returns:* `get_tzdb_list().front()`.

``` cpp
const time_zone* locate_zone(string_view tz_name);
```

*Returns:* `get_tzdb().locate_zone(tz_name)`.

[*Note 1*: The time zone database will be initialized if this is the
first reference to the database. — *end note*\]

``` cpp
const time_zone* current_zone();
```

*Returns:* `get_tzdb().current_zone()`.

#### Remote time zone database support <a id="time.zone.db.remote">[[time.zone.db.remote]]</a>

The local time zone database is that supplied by the implementation when
the program first accesses the database, for example via
`current_zone()`. While the program is running, the implementation may
choose to update the time zone database. This update shall not impact
the program in any way unless the program calls the functions in this
subclause. This potentially updated time zone database is referred to as
the *remote time zone database*.

``` cpp
const tzdb& reload_tzdb();
```

*Effects:* This function first checks the version of the remote time
zone database. If the versions of the local and remote databases are the
same, there are no effects. Otherwise the remote database is pushed to
the front of the `tzdb_list` accessed by `get_tzdb_list()`.

*Synchronization:* This function is thread-safe with respect to
`get_tzdb_list().front()` and `get_tzdb_list().erase_after()`.

*Ensures:* No pointers, references, or iterators are invalidated.

*Returns:* `get_tzdb_list().front()`.

*Throws:* `runtime_error` if for any reason a reference cannot be
returned to a valid `tzdb`.

``` cpp
string remote_version();
```

*Returns:* The latest remote database version.

[*Note 1*: This can be compared with `get_tzdb().version` to discover
if the local and remote databases are equivalent. — *end note*\]

### Exception classes <a id="time.zone.exception">[[time.zone.exception]]</a>

#### Class `nonexistent_local_time` <a id="time.zone.exception.nonexist">[[time.zone.exception.nonexist]]</a>

``` cpp
namespace std::chrono {
  class nonexistent_local_time : public runtime_error {
  public:
    template<class Duration>
      nonexistent_local_time(const local_time<Duration>& tp, const local_info& i);
  };
}
```

`nonexistent_local_time` is thrown when an attempt is made to convert a
non-existent `local_time` to a `sys_time` without specifying
`choose::earliest` or `choose::latest`.

``` cpp
template<class Duration>
  nonexistent_local_time(const local_time<Duration>& tp, const local_info& i);
```

*Preconditions:* `i.result == local_info::nonexistent` is `true`.

*Effects:* Initializes the base class with a sequence of `char`
equivalent to that produced by `os.str()` initialized as shown below:

``` cpp
ostringstream os;
os << tp << " is in a gap between\n"
   << local_seconds{i.first.end.time_since_epoch()} + i.first.offset << ' '
   << i.first.abbrev << " and\n"
   << local_seconds{i.second.begin.time_since_epoch()} + i.second.offset << ' '
   << i.second.abbrev
   << " which are both equivalent to\n"
   << i.first.end << " UTC";
```

[*Example 1*:

``` cpp
#include <chrono>
#include <iostream>

int main() {
  using namespace std::chrono;
  try {
    auto zt = zoned_time{"America/New_York",
                         local_days{Sunday[2]/March/2016} + 2h + 30min};
  } catch (const nonexistent_local_time& e) {
    std::cout << e.what() << '\n';
  }
}
```

Produces the output:

``` text
2016-03-13 02:30:00 is in a gap between
2016-03-13 02:00:00 EST and
2016-03-13 03:00:00 EDT which are both equivalent to
2016-03-13 07:00:00 UTC
```

— *end example*\]

#### Class `ambiguous_local_time` <a id="time.zone.exception.ambig">[[time.zone.exception.ambig]]</a>

``` cpp
namespace std::chrono {
  class ambiguous_local_time : public runtime_error {
  public:
    template<class Duration>
      ambiguous_local_time(const local_time<Duration>& tp, const local_info& i);
  };
}
```

`ambiguous_local_time` is thrown when an attempt is made to convert an
ambiguous `local_time` to a `sys_time` without specifying
`choose::earliest` or `choose::latest`.

``` cpp
template<class Duration>
  ambiguous_local_time(const local_time<Duration>& tp, const local_info& i);
```

*Preconditions:* `i.result == local_info::ambiguous` is `true`.

*Effects:* Initializes the base class with a sequence of `char`
equivalent to that produced by `os.str()` initialized as shown below:

``` cpp
ostringstream os;
os << tp << " is ambiguous.  It could be\n"
   << tp << ' ' << i.first.abbrev << " == "
   << tp - i.first.offset << " UTC or\n"
   << tp << ' ' << i.second.abbrev  << " == "
   << tp - i.second.offset  << " UTC";
```

[*Example 1*:

``` cpp
#include <chrono>
#include <iostream>

int main() {
  using namespace std::chrono;
  try {
    auto zt = zoned_time{"America/New_York",
                         local_days{Sunday[1]/November/2016} + 1h + 30min};
  } catch (const ambiguous_local_time& e) {
    std::cout << e.what() << '\n';
  }
}
```

Produces the output:

``` text
2016-11-06 01:30:00 is ambiguous.  It could be
2016-11-06 01:30:00 EDT == 2016-11-06 05:30:00 UTC or
2016-11-06 01:30:00 EST == 2016-11-06 06:30:00 UTC
```

— *end example*\]

### Information classes <a id="time.zone.info">[[time.zone.info]]</a>

#### Class `sys_info` <a id="time.zone.info.sys">[[time.zone.info.sys]]</a>

``` cpp
namespace std::chrono {
  struct sys_info {
    sys_seconds   begin;
    sys_seconds   end;
    seconds       offset;
    minutes       save;
    string        abbrev;
  };
}
```

A `sys_info` object can be obtained from the combination of a
`time_zone` and either a `sys_time` or `local_time`. It can also be
obtained from a `zoned_time`, which is effectively a pair of a
`time_zone` and `sys_time`.

[*Note 1*: This type provides a low-level interface to time zone
information. Typical conversions from `sys_time` to `local_time` will
use this class implicitly, not explicitly. — *end note*\]

The `begin` and `end` data members indicate that, for the associated
`time_zone` and `time_point`, the `offset` and `abbrev` are in effect in
the range \[`begin`, `end`). This information can be used to efficiently
iterate the transitions of a `time_zone`.

The `offset` data member indicates the UTC offset in effect for the
associated `time_zone` and `time_point`. The relationship between
`local_time` and `sys_time` is:

``` cpp
offset = local_time - sys_time
```

The `save` data member is extra information not normally needed for
conversion between `local_time` and `sys_time`. If `save != 0min`, this
`sys_info` is said to be on “daylight saving” time, and `offset - save`
suggests what offset this `time_zone` might use if it were off daylight
saving time. However, this information should not be taken as
authoritative. The only sure way to get such information is to query the
`time_zone` with a `time_point` that returns a `sys_info` where
`save == 0min`. There is no guarantee what `time_point` might return
such a `sys_info` except that it is guaranteed not to be in the range
\[`begin`, `end`) (if `save != 0min` for this `sys_info`).

The `abbrev` data member indicates the current abbreviation used for the
associated `time_zone` and `time_point`. Abbreviations are not unique
among the `time_zones`, and so one cannot reliably map abbreviations
back to a `time_zone` and UTC offset.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const sys_info& r);
```

*Effects:* Streams out the `sys_info` object `r` in an unspecified
format.

*Returns:* `os`.

#### Class `local_info` <a id="time.zone.info.local">[[time.zone.info.local]]</a>

``` cpp
namespace std::chrono {
  struct local_info {
    static constexpr int unique      = 0;
    static constexpr int nonexistent = 1;
    static constexpr int ambiguous   = 2;

    int result;
    sys_info first;
    sys_info second;
  };
}
```

[*Note 1*: This type provides a low-level interface to time zone
information. Typical conversions from `local_time` to `sys_time` will
use this class implicitly, not explicitly. — *end note*\]

Describes the result of converting a `local_time` to a `sys_time` as
follows:

- When a `local_time` to `sys_time` conversion is unique,
  `result == unique`, `first` will be filled out with the correct
  `sys_info`, and `second` will be zero-initialized.
- If the conversion stems from a nonexistent `local_time` then
  `result == nonexistent`, `first` will be filled out with the
  `sys_info` that ends just prior to the `local_time`, and `second` will
  be filled out with the `sys_info` that begins just after the
  `local_time`.
- If the conversion stems from an ambiguous `local_time`, then
  `result == ambiguous`, `first` will be filled out with the `sys_info`
  that ends just after the `local_time`, and `second` will be filled out
  with the `sys_info` that starts just before the `local_time`.

``` cpp
template<class charT, class traits>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os, const local_info& r);
```

*Effects:* Streams out the `local_info` object `r` in an unspecified
format.

*Returns:* `os`.

### Class `time_zone` <a id="time.zone.timezone">[[time.zone.timezone]]</a>

#### Overview <a id="time.zone.overview">[[time.zone.overview]]</a>

``` cpp
namespace std::chrono {
  class time_zone {
  public:
    time_zone(time_zone&&) = default;
    time_zone& operator=(time_zone&&) = default;

    // unspecified additional constructors

    string_view name() const noexcept;

    template<class Duration> sys_info   get_info(const sys_time<Duration>& st)   const;
    template<class Duration> local_info get_info(const local_time<Duration>& tp) const;

    template<class Duration>
      sys_time<common_type_t<Duration, seconds>>
        to_sys(const local_time<Duration>& tp) const;

    template<class Duration>
      sys_time<common_type_t<Duration, seconds>>
        to_sys(const local_time<Duration>& tp, choose z) const;

    template<class Duration>
      local_time<common_type_t<Duration, seconds>>
        to_local(const sys_time<Duration>& tp) const;
  };
}
```

A `time_zone` represents all time zone transitions for a specific
geographic area. `time_zone` construction is unspecified, and performed
as part of database initialization.

[*Note 1*: `const time_zone` objects can be accessed via functions such
as `locate_zone`. — *end note*\]

#### Member functions <a id="time.zone.members">[[time.zone.members]]</a>

``` cpp
string_view name() const noexcept;
```

*Returns:* The name of the `time_zone`.

[*Example 1*: `"America/New_York"`. — *end example*\]

``` cpp
template<class Duration>
  sys_info get_info(const sys_time<Duration>& st) const;
```

*Returns:* A `sys_info` `i` for which `st` is in the range \[`i.begin`,
`i.end`).

``` cpp
template<class Duration>
  local_info get_info(const local_time<Duration>& tp) const;
```

*Returns:* A `local_info` for `tp`.

``` cpp
template<class Duration>
  sys_time<common_type_t<Duration, seconds>>
    to_sys(const local_time<Duration>& tp) const;
```

*Returns:* A `sys_time` that is at least as fine as `seconds`, and will
be finer if the argument `tp` has finer precision. This `sys_time` is
the UTC equivalent of `tp` according to the rules of this `time_zone`.

*Throws:* If the conversion from `tp` to a `sys_time` is ambiguous,
throws `ambiguous_local_time`. If the `tp` represents a non-existent
time between two UTC `time_points`, throws `nonexistent_local_time`.

``` cpp
template<class Duration>
  sys_time<common_type_t<Duration, seconds>>
    to_sys(const local_time<Duration>& tp, choose z) const;
```

*Returns:* A `sys_time` that is at least as fine as `seconds`, and will
be finer if the argument `tp` has finer precision. This `sys_time` is
the UTC equivalent of `tp` according to the rules of this `time_zone`.
If the conversion from `tp` to a `sys_time` is ambiguous, returns the
earlier `sys_time` if `z == choose::earliest`, and returns the later
`sys_time` if `z == choose::latest`. If the `tp` represents a
non-existent time between two UTC `time_points`, then the two UTC
`time_points` will be the same, and that UTC `time_point` will be
returned.

``` cpp
template<class Duration>
  local_time<common_type_t<Duration, seconds>>
    to_local(const sys_time<Duration>& tp) const;
```

*Returns:* The `local_time` associated with `tp` and this `time_zone`.

#### Non-member functions <a id="time.zone.nonmembers">[[time.zone.nonmembers]]</a>

``` cpp
bool operator==(const time_zone& x, const time_zone& y) noexcept;
```

*Returns:* `x.name() == y.name()`.

``` cpp
strong_ordering operator<=>(const time_zone& x, const time_zone& y) noexcept;
```

*Returns:* `x.name() <=> y.name()`.

### Class template `zoned_traits` <a id="time.zone.zonedtraits">[[time.zone.zonedtraits]]</a>

``` cpp
namespace std::chrono {
  template<class T> struct zoned_traits {};
}
```

`zoned_traits` provides a means for customizing the behavior of
`zoned_time<Duration, TimeZonePtr>` for the `zoned_time` default
constructor, and constructors taking `string_view`. A specialization for
`const time_zone*` is provided by the implementation:

``` cpp
namespace std::chrono {
  template<> struct zoned_traits<const time_zone*> {
    static const time_zone* default_zone();
    static const time_zone* locate_zone(string_view name);
  };
}
```

``` cpp
static const time_zone* default_zone();
```

*Returns:* `std::chrono::locate_zone("UTC")`.

``` cpp
static const time_zone* locate_zone(string_view name);
```

*Returns:* `std::chrono::locate_zone(name)`.

### Class template `zoned_time` <a id="time.zone.zonedtime">[[time.zone.zonedtime]]</a>

#### Overview <a id="time.zone.zonedtime.overview">[[time.zone.zonedtime.overview]]</a>

``` cpp
namespace std::chrono {
  template<class Duration, class TimeZonePtr = const time_zone*>
  class zoned_time {
  public:
    using duration = common_type_t<Duration, seconds>;

  private:
    TimeZonePtr        zone_;                   // exposition only
    sys_time<duration> tp_;                     // exposition only

    using traits = zoned_traits<TimeZonePtr>;   // exposition only

  public:
    zoned_time();
    zoned_time(const zoned_time&) = default;
    zoned_time& operator=(const zoned_time&) = default;

    zoned_time(const sys_time<Duration>& st);
    explicit zoned_time(TimeZonePtr z);
    explicit zoned_time(string_view name);

    template<class Duration2>
      zoned_time(const zoned_time<Duration2, TimeZonePtr>& y);

    zoned_time(TimeZonePtr z,    const sys_time<Duration>& st);
    zoned_time(string_view name, const sys_time<Duration>& st);

    zoned_time(TimeZonePtr z,    const local_time<Duration>& tp);
    zoned_time(string_view name, const local_time<Duration>& tp);
    zoned_time(TimeZonePtr z,    const local_time<Duration>& tp, choose c);
    zoned_time(string_view name, const local_time<Duration>& tp, choose c);

    template<class Duration2, class TimeZonePtr2>
      zoned_time(TimeZonePtr z, const zoned_time<Duration2, TimeZonePtr2>& y);
    template<class Duration2, class TimeZonePtr2>
      zoned_time(TimeZonePtr z, const zoned_time<Duration2, TimeZonePtr2>& y, choose);

    template<class Duration2, class TimeZonePtr2>
      zoned_time(string_view name, const zoned_time<Duration2, TimeZonePtr2>& y);
    template<class Duration2, class TimeZonePtr2>
      zoned_time(string_view name, const zoned_time<Duration2, TimeZonePtr2>& y, choose c);

    zoned_time& operator=(const sys_time<Duration>& st);
    zoned_time& operator=(const local_time<Duration>& lt);

    operator sys_time<duration>() const;
    explicit operator local_time<duration>() const;

    TimeZonePtr          get_time_zone()  const;
    local_time<duration> get_local_time() const;
    sys_time<duration>   get_sys_time()   const;
    sys_info             get_info()       const;
  };

  zoned_time() -> zoned_time<seconds>;

  template<class Duration>
    zoned_time(sys_time<Duration>)
      -> zoned_time<common_type_t<Duration, seconds>>;

  template<class TimeZonePtrOrName>
    using time-zone-representation =        // exposition only
      conditional_t<is_convertible_v<TimeZonePtrOrName, string_view>,
                    const time_zone*,
                    remove_cvref_t<TimeZonePtrOrName>>;

  template<class TimeZonePtrOrName>
    zoned_time(TimeZonePtrOrName&&)
      -> zoned_time<seconds, time-zone-representation<TimeZonePtrOrName>>;

  template<class TimeZonePtrOrName, class Duration>
    zoned_time(TimeZonePtrOrName&&, sys_time<Duration>)
      -> zoned_time<common_type_t<Duration, seconds>,
                    time-zone-representation<TimeZonePtrOrName>>;

  template<class TimeZonePtrOrName, class Duration>
    zoned_time(TimeZonePtrOrName&&, local_time<Duration>,
               choose = choose::earliest)
      -> zoned_time<common_type_t<Duration, seconds>,
                    time-zone-representation<TimeZonePtrOrName>>;

  template<class Duration, class TimeZonePtrOrName, class TimeZonePtr2>
    zoned_time(TimeZonePtrOrName&&, zoned_time<Duration, TimeZonePtr2>,
               choose = choose::earliest)
      -> zoned_time<common_type_t<Duration, seconds>,
                    time-zone-representation<TimeZonePtrOrName>>;
}
```

`zoned_time` represents a logical pairing of a `time_zone` and a
`time_point` with precision `Duration`. `zoned_time<Duration>` maintains
the invariant that it always refers to a valid time zone and represents
a point in time that exists and is not ambiguous in that time zone.

If `Duration` is not a specialization of `chrono::duration`, the program
is ill-formed.

Every constructor of `zoned_time` that accepts a `string_view` as its
first parameter does not participate in class template argument
deduction [[over.match.class.deduct]].

#### Constructors <a id="time.zone.zonedtime.ctor">[[time.zone.zonedtime.ctor]]</a>

``` cpp
zoned_time();
```

*Constraints:* `traits::default_zone()` is a well-formed expression.

*Effects:* Initializes `zone_` with `traits::default_zone()` and default
constructs `tp_`.

``` cpp
zoned_time(const sys_time<Duration>& st);
```

*Constraints:* `traits::default_zone()` is a well-formed expression.

*Effects:* Initializes `zone_` with `traits::default_zone()` and `tp_`
with `st`.

``` cpp
explicit zoned_time(TimeZonePtr z);
```

*Preconditions:* `z` refers to a time zone.

*Effects:* Initializes `zone_` with `std::move(z)` and default
constructs `tp_`.

``` cpp
explicit zoned_time(string_view name);
```

*Constraints:* `traits::locate_zone(string_view{})` is a well-formed
expression and `zoned_time` is constructible from the return type of
`traits::locate_zone(string_view{})`.

*Effects:* Initializes `zone_` with `traits::locate_zone(name)` and
default constructs `tp_`.

``` cpp
template<class Duration2>
  zoned_time(const zoned_time<Duration2, TimeZonePtr>& y);
```

*Constraints:*
`is_convertible_v<sys_time<Duration2>, sys_time<Duration>>` is `true`.

*Effects:* Initializes `zone_` with `y.zone_` and `tp_` with `y.tp_`.

``` cpp
zoned_time(TimeZonePtr z, const sys_time<Duration>& st);
```

*Preconditions:* `z` refers to a time zone.

*Effects:* Initializes `zone_` with `std::move(z)` and `tp_` with `st`.

``` cpp
zoned_time(string_view name, const sys_time<Duration>& st);
```

*Constraints:* `zoned_time` is constructible from the return type of
`traits::locate_zone(name)` and `st`.

*Effects:* Equivalent to construction with
`{traits::locate_zone(name), st}`.

``` cpp
zoned_time(TimeZonePtr z, const local_time<Duration>& tp);
```

*Constraints:*

``` cpp
is_convertible_v<
  decltype(declval<TimeZonePtr&>()->to_sys(local_time<Duration>{})),
  sys_time<duration>>
```

is `true`.

*Preconditions:* `z` refers to a time zone.

*Effects:* Initializes `zone_` with `std::move(z)` and `tp_` with
`zone_->to_sys(tp)`.

``` cpp
zoned_time(string_view name, const local_time<Duration>& tp);
```

*Constraints:* `zoned_time` is constructible from the return type of
`traits::locate_zone(name)` and `tp`.

*Effects:* Equivalent to construction with
`{traits::locate_zone(name), tp}`.

``` cpp
zoned_time(TimeZonePtr z, const local_time<Duration>& tp, choose c);
```

*Constraints:*

``` cpp
is_convertible_v<
  decltype(declval<TimeZonePtr&>()->to_sys(local_time<Duration>{}, choose::earliest)),
  sys_time<duration>>
```

is `true`.

*Preconditions:* `z` refers to a time zone.

*Effects:* Initializes `zone_` with `std::move(z)` and `tp_` with
`zone_->to_sys(tp, c)`.

``` cpp
zoned_time(string_view name, const local_time<Duration>& tp, choose c);
```

*Constraints:* `zoned_time` is constructible from the return type of
`traits::locate_zone(name)`, `local_time<Duration>`, and `choose`.

*Effects:* Equivalent to construction with
`{traits::locate_zone(name), tp, c}`.

``` cpp
template<class Duration2, class TimeZonePtr2>
  zoned_time(TimeZonePtr z, const zoned_time<Duration2, TimeZonePtr2>& y);
```

*Constraints:*
`is_convertible_v<sys_time<Duration2>, sys_time<Duration>>` is `true`.

*Preconditions:* `z` refers to a valid time zone.

*Effects:* Initializes `zone_` with `std::move(z)` and `tp_` with
`y.tp_`.

``` cpp
template<class Duration2, class TimeZonePtr2>
  zoned_time(TimeZonePtr z, const zoned_time<Duration2, TimeZonePtr2>& y, choose);
```

*Constraints:*
`is_convertible_v<sys_time<Duration2>, sys_time<Duration>>` is `true`.

*Preconditions:* `z` refers to a valid time zone.

*Effects:* Equivalent to construction with `{z, y}`.

[*Note 1*: The `choose` parameter has no effect. — *end note*\]

``` cpp
template<class Duration2, class TimeZonePtr2>
  zoned_time(string_view name, const zoned_time<Duration2, TimeZonePtr2>& y);
```

*Constraints:* `zoned_time` is constructible from the return type of
`traits::locate_zone(name)` and the type
`zoned_time<Duration2, TimeZonePtr2>`.

*Effects:* Equivalent to construction with
`{traits::locate_zone(name), y}`.

``` cpp
template<class Duration2, class TimeZonePtr2>
  zoned_time(string_view name, const zoned_time<Duration2, TimeZonePtr2>& y, choose c);
```

*Constraints:* `zoned_time` is constructible from the return type of
`traits::locate_zone(name)`, the type
`zoned_time<Duration2, TimeZonePtr2>`, and the type `choose`.

*Effects:* Equivalent to construction with
`{traits::locate_zone(name), y, c}`.

[*Note 2*: The `choose` parameter has no effect. — *end note*\]

#### Member functions <a id="time.zone.zonedtime.members">[[time.zone.zonedtime.members]]</a>

``` cpp
zoned_time& operator=(const sys_time<Duration>& st);
```

*Effects:* After assignment, `get_sys_time() == st`. This assignment has
no effect on the return value of `get_time_zone()`.

*Returns:* `*this`.

``` cpp
zoned_time& operator=(const local_time<Duration>& lt);
```

*Effects:* After assignment, `get_local_time() == lt`. This assignment
has no effect on the return value of `get_time_zone()`.

*Returns:* `*this`.

``` cpp
operator sys_time<duration>() const;
```

*Returns:* `get_sys_time()`.

``` cpp
explicit operator local_time<duration>() const;
```

*Returns:* `get_local_time()`.

``` cpp
TimeZonePtr get_time_zone() const;
```

*Returns:* `zone_`.

``` cpp
local_time<duration> get_local_time() const;
```

*Returns:* `zone_->to_local(tp_)`.

``` cpp
sys_time<duration> get_sys_time() const;
```

*Returns:* `tp_`.

``` cpp
sys_info get_info() const;
```

*Returns:* `zone_->get_info(tp_)`.

#### Non-member functions <a id="time.zone.zonedtime.nonmembers">[[time.zone.zonedtime.nonmembers]]</a>

``` cpp
template<class Duration1, class Duration2, class TimeZonePtr>
  bool operator==(const zoned_time<Duration1, TimeZonePtr>& x,
                  const zoned_time<Duration2, TimeZonePtr>& y);
```

*Returns:* `x.zone_ == y.zone_ && x.tp_ == y.tp_`.

``` cpp
template<class charT, class traits, class Duration, class TimeZonePtr>
  basic_ostream<charT, traits>&
    operator<<(basic_ostream<charT, traits>& os,
               const zoned_time<Duration, TimeZonePtr>& t);
```

*Effects:* Equivalent to:

``` cpp
return os << format(os.getloc(), STATICALLY-WIDEN<charT>("{:L%F %T %Z}"), t);
```

### Class `leap_second` <a id="time.zone.leap">[[time.zone.leap]]</a>

#### Overview <a id="time.zone.leap.overview">[[time.zone.leap.overview]]</a>

``` cpp
namespace std::chrono {
  class leap_second {
  public:
    leap_second(const leap_second&)            = default;
    leap_second& operator=(const leap_second&) = default;

    // unspecified additional constructors

    constexpr sys_seconds date() const noexcept;
    constexpr seconds value() const noexcept;
  };
}
```

Objects of type `leap_second` representing the date and value of the
leap second insertions are constructed and stored in the time zone
database when initialized.

[*Example 1*:

``` cpp
for (auto& l : get_tzdb().leap_seconds)
  if (l <= 2018y/March/17d)
    cout << l.date() << ": " << l.value() << '\n';
```

Produces the output:

``` cpp
1972-07-01 00:00:00: 1s
1973-01-01 00:00:00: 1s
1974-01-01 00:00:00: 1s
1975-01-01 00:00:00: 1s
1976-01-01 00:00:00: 1s
1977-01-01 00:00:00: 1s
1978-01-01 00:00:00: 1s
1979-01-01 00:00:00: 1s
1980-01-01 00:00:00: 1s
1981-07-01 00:00:00: 1s
1982-07-01 00:00:00: 1s
1983-07-01 00:00:00: 1s
1985-07-01 00:00:00: 1s
1988-01-01 00:00:00: 1s
1990-01-01 00:00:00: 1s
1991-01-01 00:00:00: 1s
1992-07-01 00:00:00: 1s
1993-07-01 00:00:00: 1s
1994-07-01 00:00:00: 1s
1996-01-01 00:00:00: 1s
1997-07-01 00:00:00: 1s
1999-01-01 00:00:00: 1s
2006-01-01 00:00:00: 1s
2009-01-01 00:00:00: 1s
2012-07-01 00:00:00: 1s
2015-07-01 00:00:00: 1s
2017-01-01 00:00:00: 1s
```

— *end example*\]

#### Member functions <a id="time.zone.leap.members">[[time.zone.leap.members]]</a>

``` cpp
constexpr sys_seconds date() const noexcept;
```

*Returns:* The date and time at which the leap second was inserted.

``` cpp
constexpr seconds value() const noexcept;
```

*Returns:* `+1s` to indicate a positive leap second or `-1s` to indicate
a negative leap second.

[*Note 1*: All leap seconds inserted up through 2022 were positive leap
seconds. — *end note*\]

#### Non-member functions <a id="time.zone.leap.nonmembers">[[time.zone.leap.nonmembers]]</a>

``` cpp
constexpr bool operator==(const leap_second& x, const leap_second& y) noexcept;
```

*Returns:* `x.date() == y.date()`.

``` cpp
constexpr strong_ordering operator<=>(const leap_second& x, const leap_second& y) noexcept;
```

*Returns:* `x.date() <=> y.date()`.

``` cpp
template<class Duration>
  constexpr bool operator==(const leap_second& x, const sys_time<Duration>& y) noexcept;
```

*Returns:* `x.date() == y`.

``` cpp
template<class Duration>
  constexpr bool operator<(const leap_second& x, const sys_time<Duration>& y) noexcept;
```

*Returns:* `x.date() < y`.

``` cpp
template<class Duration>
  constexpr bool operator<(const sys_time<Duration>& x, const leap_second& y) noexcept;
```

*Returns:* `x < y.date()`.

``` cpp
template<class Duration>
  constexpr bool operator>(const leap_second& x, const sys_time<Duration>& y) noexcept;
```

*Returns:* `y < x`.

``` cpp
template<class Duration>
  constexpr bool operator>(const sys_time<Duration>& x, const leap_second& y) noexcept;
```

*Returns:* `y < x`.

``` cpp
template<class Duration>
  constexpr bool operator<=(const leap_second& x, const sys_time<Duration>& y) noexcept;
```

*Returns:* `!(y < x)`.

``` cpp
template<class Duration>
  constexpr bool operator<=(const sys_time<Duration>& x, const leap_second& y) noexcept;
```

*Returns:* `!(y < x)`.

``` cpp
template<class Duration>
  constexpr bool operator>=(const leap_second& x, const sys_time<Duration>& y) noexcept;
```

*Returns:* `!(x < y)`.

``` cpp
template<class Duration>
  constexpr bool operator>=(const sys_time<Duration>& x, const leap_second& y) noexcept;
```

*Returns:* `!(x < y)`.

``` cpp
template<class Duration>
  requires three_way_comparable_with<sys_seconds, sys_time<Duration>>
  constexpr auto operator<=>(const leap_second& x, const sys_time<Duration>& y) noexcept;
```

*Returns:* `x.date() <=> y`.

### Class `time_zone_link` <a id="time.zone.link">[[time.zone.link]]</a>

#### Overview <a id="time.zone.link.overview">[[time.zone.link.overview]]</a>

``` cpp
namespace std::chrono {
  class time_zone_link {
  public:
    time_zone_link(time_zone_link&&)            = default;
    time_zone_link& operator=(time_zone_link&&) = default;

    // unspecified additional constructors

    string_view name()   const noexcept;
    string_view target() const noexcept;
  };
}
```

A `time_zone_link` specifies an alternative name for a `time_zone`.
`time_zone_link`s are constructed when the time zone database is
initialized.

#### Member functions <a id="time.zone.link.members">[[time.zone.link.members]]</a>

``` cpp
string_view name() const noexcept;
```

*Returns:* The alternative name for the time zone.

``` cpp
string_view target() const noexcept;
```

*Returns:* The name of the `time_zone` for which this `time_zone_link`
provides an alternative name.

#### Non-member functions <a id="time.zone.link.nonmembers">[[time.zone.link.nonmembers]]</a>

``` cpp
bool operator==(const time_zone_link& x, const time_zone_link& y) noexcept;
```

*Returns:* `x.name() == y.name()`.

``` cpp
strong_ordering operator<=>(const time_zone_link& x, const time_zone_link& y) noexcept;
```

*Returns:* `x.name() <=> y.name()`.

## Formatting <a id="time.format">[[time.format]]</a>

Each `formatter` [[format.formatter]] specialization in the chrono
library [[time.syn]] meets the requirements [[formatter.requirements]].
The `parse` member functions of these formatters interpret the format
specification as a *chrono-format-spec* according to the following
syntax:

``` bnf
\fmtnontermdef{chrono-format-spec}
    fill-and-alignₒₚₜ widthₒₚₜ precisionₒₚₜ 'L'ₒₚₜ chrono-specsₒₚₜ
```

``` bnf
\fmtnontermdef{chrono-specs}
    conversion-spec
    chrono-specs conversion-spec
    chrono-specs literal-char
```

``` bnf
\fmtnontermdef{literal-char}
    any character other than \{, \}, or \%
```

``` bnf
\fmtnontermdef{conversion-spec}
    '%' modifierₒₚₜ type
```

``` bnf
\fmtnontermdef{modifier} one of
    'E O'
```

``` bnf
\fmtnontermdef{type} one of
    'a A b B c C d D e F g G h H I j m M n'
    'p q Q r R S t T u U V w W x X y Y z Z %'
```

The productions *fill-and-align*, *width*, and *precision* are described
in [[format.string]]. Giving a *precision* specification in the
*chrono-format-spec* is valid only for types that are specializations of
`std::chrono::duration` for which the nested *typedef-name* `rep`
denotes a floating-point type. For all other types, an exception of type
`format_error` is thrown if the *chrono-format-spec* contains a
*precision* specification. All ordinary multibyte characters represented
by *literal-char* are copied unchanged to the output.

A *formatting locale* is an instance of `locale` used by a formatting
function, defined as

- the `"C"` locale if the `L` option is not present in
  *chrono-format-spec*, otherwise
- the locale passed to the formatting function if any, otherwise
- the global locale.

Each conversion specifier *conversion-spec* is replaced by appropriate
characters as described in [[time.format.spec]]; the formats specified
in ISO 8601:2004 shall be used where so described. Some of the
conversion specifiers depend on the formatting locale. If the string
literal encoding is a Unicode encoding form and the locale is among an
*implementation-defined* set of locales, each replacement that depends
on the locale is performed as if the replacement character sequence is
converted to the string literal encoding. If the formatted object does
not contain the information the conversion specifier refers to, an
exception of type `format_error` is thrown.

The result of formatting a `std::chrono::duration` instance holding a
negative value, or an `hh_mm_ss` object `h` for which `h.is_negative()`
is `true`, is equivalent to the output of the corresponding positive
value, with a `STATICALLY-WIDEN<charT>("-")` character sequence placed
before the replacement of the initial conversion specifier.

[*Example 1*:

``` cpp
cout << format("{:%T}", -10'000s);          // prints: -02:46:40
cout << format("{:%H:%M:%S}", -10'000s);    // prints: -02:46:40
cout << format("minutes {:%M, hours %H, seconds %S}", -10'000s);
                                            // prints: minutes -46, hours 02, seconds 40
```

— *end example*\]

Unless explicitly requested, the result of formatting a chrono type does
not contain time zone abbreviation and time zone offset information. If
the information is available, the conversion specifiers `%Z` and `%z`
will format this information (respectively).

[*Note 1*: If the information is not available and a `%Z` or `%z`
conversion specifier appears in the *chrono-format-spec*, an exception
of type `format_error` is thrown, as described above. — *end note*\]

If the type being formatted does not contain the information that the
format flag needs, an exception of type `format_error` is thrown.

[*Example 2*: A `duration` does not contain enough information to
format as a `weekday`. — *end example*\]

However, if a flag refers to a “time of day” (e.g., `%H`, `%I`, `%p`,
etc.), then a specialization of `duration` is interpreted as the time of
day elapsed since midnight.

**Table: Meaning of conversion specifiers**

| Specifier | Replacement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `%a`      | The locale's abbreviated weekday name. If the value does not contain a valid weekday, an exception of type `format_error` is thrown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `%A`      | The locale's full weekday name. If the value does not contain a valid weekday, an exception of type `format_error` is thrown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `%b`      | The locale's abbreviated month name. If the value does not contain a valid month, an exception of type `format_error` is thrown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `%B`      | The locale's full month name. If the value does not contain a valid month, an exception of type `format_error` is thrown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `%c`      | The locale's date and time representation. The modified command `%Ec` produces the locale's alternate date and time representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `%C`      | The year divided by 100 using floored division. If the result is a single decimal digit, it is prefixed with `0`. The modified command `%EC` produces the locale's alternative representation of the century.                                                                                                                                                                                                                                                                                                                                                                                                  |
| `%d`      | The day of month as a decimal number. If the result is a single decimal digit, it is prefixed with `0`. The modified command `%Od` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `%D`      | Equivalent to `%m/%d/%y`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `%e`      | The day of month as a decimal number. If the result is a single decimal digit, it is prefixed with a space. The modified command `%Oe` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `%F`      | Equivalent to `%Y-%m-%d`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `%g`      | The last two decimal digits of the ISO week-based year. If the result is a single digit it is prefixed by `0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `%G`      | The ISO week-based year as a decimal number. If the result is less than four digits it is left-padded with `0` to four digits.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `%h`      | Equivalent to `%b`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `%H`      | The hour (24-hour clock) as a decimal number. If the result is a single digit, it is prefixed with `0`. The modified command `%OH` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `%I`      | The hour (12-hour clock) as a decimal number. If the result is a single digit, it is prefixed with `0`. The modified command `%OI` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `%j`      | If the type being formatted is a specialization of `duration`, the decimal number of `days` without padding. Otherwise, the day of the year as a decimal number. Jan 1 is `001`. If the result is less than three digits, it is left-padded with `0` to three digits.                                                                                                                                                                                                                                                                                                                                          |
| `%m`      | The month as a decimal number. Jan is `01`. If the result is a single digit, it is prefixed with `0`. The modified command `%Om` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `%M`      | The minute as a decimal number. If the result is a single digit, it is prefixed with `0`. The modified command `%OM` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%n`      | A new-line character.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `%p`      | The locale's equivalent of the AM/PM designations associated with a 12-hour clock.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `%q`      | The duration's unit suffix as specified in [[time.duration.io]].                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `%Q`      | The duration's numeric value (as if extracted via `.count()`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `%r`      | The locale's 12-hour clock time.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `%R`      | Equivalent to `%H:%M`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%S`      | Seconds as a decimal number. If the number of seconds is less than `10`, the result is prefixed with `0`. If the precision of the input cannot be exactly represented with seconds, then the format is a decimal floating-point number with a fixed format and a precision matching that of the precision of the input (or to a microseconds precision if the conversion to floating-point decimal seconds cannot be made within 18 fractional digits). The character for the decimal point is localized according to the locale. The modified command `%OS` produces the locale's alternative representation. |
| `%t`      | A horizontal-tab character.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `%T`      | Equivalent to `%H:%M:%S`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `%u`      | The ISO weekday as a decimal number (`1`-`7`), where Monday is `1`. The modified command `%Ou` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `%U`      | The week number of the year as a decimal number. The first Sunday of the year is the first day of week `01`. Days of the same year prior to that are in week `00`. If the result is a single digit, it is prefixed with `0`. The modified command `%OU` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                      |
| `%V`      | The ISO week-based week number as a decimal number. If the result is a single digit, it is prefixed with `0`. The modified command `%OV` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `%w`      | The weekday as a decimal number (`0`-`6`), where Sunday is `0`. The modified command `%Ow` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `%W`      | The week number of the year as a decimal number. The first Monday of the year is the first day of week `01`. Days of the same year prior to that are in week `00`. If the result is a single digit, it is prefixed with `0`. The modified command `%OW` produces the locale's alternative representation.                                                                                                                                                                                                                                                                                                      |
| `%x`      | The locale's date representation. The modified command `%Ex` produces the locale's alternate date representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `%X`      | The locale's time representation. The modified command `%EX` produces the locale's alternate time representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `%y`      | The last two decimal digits of the year. If the result is a single digit it is prefixed by `0`. The modified command `%Oy` produces the locale's alternative representation. The modified command `%Ey` produces the locale's alternative representation of offset from `%EC` (year only).                                                                                                                                                                                                                                                                                                                     |
| `%Y`      | The year as a decimal number. If the result is less than four digits it is left-padded with `0` to four digits. The modified command `%EY` produces the locale's alternative full year representation.                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%z`      | The offset from UTC in the ISO 8601:2004 format. For example `-0430` refers to 4 hours 30 minutes behind UTC. If the offset is zero, `+0000` is used. The modified commands `%Ez` and `%Oz` insert a `:` between the hours and minutes: `-04:30`. If the offset information is not available, an exception of type `format_error` is thrown.                                                                                                                                                                                                                                                                   |
| `%Z`      | The time zone abbreviation. If the time zone abbreviation is not available, an exception of type `format_error` is thrown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `%%`      | A `%` character.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |


If the *chrono-specs* is omitted, the chrono object is formatted as if
by streaming it to `basic_ostringstream<charT> os` with the formatting
locale imbued and copying `os.str()` through the output iterator of the
context with additional padding and adjustments as specified by the
format specifiers.

[*Example 3*:

``` cpp
string s = format("{:=>8}", 42ms);      // value of s is "====42ms"
```

— *end example*\]

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::sys_time<Duration>, charT>;
```

*Remarks:* If `%Z` is used, it is replaced with
*`STATICALLY-WIDEN`*`<charT>("UTC")`. If `%z` (or a modified variant of
`%z`) is used, an offset of `0min` is formatted.

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::utc_time<Duration>, charT>;
```

*Remarks:* If `%Z` is used, it is replaced with
*`STATICALLY-WIDEN`*`<charT>("UTC")`. If `%z` (or a modified variant of
`%z`) is used, an offset of `0min` is formatted. If the argument
represents a time during a positive leap second insertion, and if a
seconds field is formatted, the integral portion of that format is
*`STATICALLY-WIDEN`*`<charT>("60")`.

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::tai_time<Duration>, charT>;
```

*Remarks:* If `%Z` is used, it is replaced with
*`STATICALLY-WIDEN`*`<charT>("TAI")`. If `%z` (or a modified variant of
`%z`) is used, an offset of `0min` is formatted. The date and time
formatted are equivalent to those formatted by a `sys_time` initialized
with

``` cpp
sys_time<Duration>{tp.time_since_epoch()} -
  (sys_days{1970y/January/1} - sys_days{1958y/January/1})
```

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::gps_time<Duration>, charT>;
```

*Remarks:* If `%Z` is used, it is replaced with
*`STATICALLY-WIDEN`*`<charT>("GPS")`. If `%z` (or a modified variant of
`%z`) is used, an offset of `0min` is formatted. The date and time
formatted are equivalent to those formatted by a `sys_time` initialized
with

``` cpp
sys_time<Duration>{tp.time_since_epoch()} +
  (sys_days{1980y/January/Sunday[1]} - sys_days{1970y/January/1})
```

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::file_time<Duration>, charT>;
```

*Remarks:* If `%Z` is used, it is replaced with
*`STATICALLY-WIDEN`*`<charT>("UTC")`. If `%z` (or a modified variant of
`%z`) is used, an offset of `0min` is formatted. The date and time
formatted are equivalent to those formatted by a `sys_time` initialized
with `clock_cast<system_clock>(t)`, or by a `utc_time` initialized with
`clock_cast<utc_clock>(t)`, where `t` is the first argument to `format`.

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::local_time<Duration>, charT>;
```

*Remarks:* If `%Z`, `%z`, or a modified version of `%z` is used, an
exception of type `format_error` is thrown.

``` cpp
template<class Duration> struct local-time-format-t {           // exposition only
  local_time<Duration> time;                                    // exposition only
  const string* abbrev;                                         // exposition only
  const seconds* offset_sec;                                    // exposition only
};
```

``` cpp
template<class Duration>
  local-time-format-t<Duration>
    local_time_format(local_time<Duration> time, const string* abbrev = nullptr,
                      const seconds* offset_sec = nullptr);
```

*Returns:* `{time, abbrev, offset_sec}`.

``` cpp
template<class Duration, class charT>
  struct formatter<chrono::local-time-format-t<Duration>, charT>;
```

Let `f` be a *`local-time-format-t`*`<Duration>` object passed to
`formatter::format`.

*Remarks:* If `%Z` is used, it is replaced with `*f.abbrev` if
`f.abbrev` is not a null pointer value. If `%Z` is used and `f.abbrev`
is a null pointer value, an exception of type `format_error` is thrown.
If `%z` (or a modified variant of `%z`) is used, it is formatted with
the value of `*f.offset_sec` if `f.offset_sec` is not a null pointer
value. If `%z` (or a modified variant of `%z`) is used and
`f.offset_sec` is a null pointer value, then an exception of type
`format_error` is thrown.

``` cpp
template<class Duration, class TimeZonePtr, class charT>
struct formatter<chrono::zoned_time<Duration, TimeZonePtr>, charT>
    : formatter<chrono::local-time-format-t<Duration>, charT> {
  template<class FormatContext>
    typename FormatContext::iterator
      format(const chrono::zoned_time<Duration, TimeZonePtr>& tp, FormatContext& ctx) const;
};
```

``` cpp
template<class FormatContext>
  typename FormatContext::iterator
    format(const chrono::zoned_time<Duration, TimeZonePtr>& tp, FormatContext& ctx) const;
```

*Effects:* Equivalent to:

``` cpp
sys_info info = tp.get_info();
return formatter<chrono::local-time-format-t<Duration>, charT>::
         format({tp.get_local_time(), &info.abbrev, &info.offset}, ctx);
```

## Parsing <a id="time.parse">[[time.parse]]</a>

Each `parse` overload specified in this subclause calls `from_stream`
unqualified, so as to enable argument dependent lookup
[[basic.lookup.argdep]]. In the following paragraphs, let `is` denote an
object of type `basic_istream<charT, traits>` and let `I` be
`basic_istream<charT, traits>&`, where `charT` and `traits` are template
parameters in that context.

*Recommended practice:* Implementations should make it difficult to
accidentally store or use a manipulator that may contain a dangling
reference to a format string, for example by making the manipulators
produced by `parse` immovable and preventing stream extraction into an
lvalue of such a manipulator type.

``` cpp
template<class charT, class Parsable>
  unspecified
    parse(const charT* fmt, Parsable& tp);
template<class charT, class traits, class Alloc, class Parsable>
  unspecified
    parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp);
```

Let F be `fmt` for the first overload and `fmt.c_str()` for the second
overload. Let `traits` be `char_traits<charT>` for the first overload.

*Constraints:* The expression

``` cpp
from_stream(declval<basic_istream<charT, traits>&>(), $F$, tp)
```

is well-formed when treated as an unevaluated
operand [[term.unevaluated.operand]].

*Returns:* A manipulator such that the expression `is >> parse(fmt, tp)`
has type `I`, has value `is`, and calls `from_stream(is, `F`, tp)`.

``` cpp
template<class charT, class traits, class Alloc, class Parsable>
  unspecified
    parse(const charT* fmt, Parsable& tp,
          basic_string<charT, traits, Alloc>& abbrev);
template<class charT, class traits, class Alloc, class Parsable>
  unspecified
    parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp,
          basic_string<charT, traits, Alloc>& abbrev);
```

Let F be `fmt` for the first overload and `fmt.c_str()` for the second
overload.

*Constraints:* The expression

``` cpp
from_stream(declval<basic_istream<charT, traits>&>(), $F$, tp, addressof(abbrev))
```

is well-formed when treated as an unevaluated
operand [[term.unevaluated.operand]].

*Returns:* A manipulator such that the expression
`is >> parse(fmt, tp, abbrev)` has type `I`, has value `is`, and calls
`from_stream(is, `F`, tp, addressof(abbrev))`.

``` cpp
template<class charT, class Parsable>
  unspecified
    parse(const charT* fmt, Parsable& tp, minutes& offset);
template<class charT, class traits, class Alloc, class Parsable>
  unspecified
    parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp,
          minutes& offset);
```

Let F be `fmt` for the first overload and `fmt.c_str()` for the second
overload. Let `traits` be `char_traits<charT>` and `Alloc` be
`allocator<charT>` for the first overload.

*Constraints:* The expression

``` cpp
from_stream(declval<basic_istream<charT, traits>&>(),
            $F$, tp,
            declval<basic_string<charT, traits, Alloc>*>(),
            &offset)
```

is well-formed when treated as an unevaluated
operand [[term.unevaluated.operand]].

*Returns:* A manipulator such that the expression
`is >> parse(fmt, tp, offset)` has type `I`, has value `is`, and calls:

``` cpp
from_stream(is,
            $F$, tp,
            static_cast<basic_string<charT, traits, Alloc>*>(nullptr),
            &offset)
```

``` cpp
template<class charT, class traits, class Alloc, class Parsable>
  unspecified
    parse(const charT* fmt, Parsable& tp,
          basic_string<charT, traits, Alloc>& abbrev, minutes& offset);
template<class charT, class traits, class Alloc, class Parsable>
  unspecified
    parse(const basic_string<charT, traits, Alloc>& fmt, Parsable& tp,
          basic_string<charT, traits, Alloc>& abbrev, minutes& offset);
```

Let F be `fmt` for the first overload and `fmt.c_str()` for the second
overload.

*Constraints:* The expression

``` cpp
from_stream(declval<basic_istream<charT, traits>&>(),
            $F$, tp, addressof(abbrev), &offset)
```

is well-formed when treated as an unevaluated
operand [[term.unevaluated.operand]].

*Returns:* A manipulator such that the expression
`is >> parse(fmt, tp, abbrev, offset)` has type `I`, has value `is`, and
calls `from_stream(is, `F`, tp, addressof(abbrev), &offset)`.

All `from_stream` overloads behave as unformatted input functions,
except that they have an unspecified effect on the value returned by
subsequent calls to `basic_istream<>::gcount()`. Each overload takes a
format string containing ordinary characters and flags which have
special meaning. Each flag begins with a `%`. Some flags can be modified
by `E` or `O`. During parsing each flag interprets characters as parts
of date and time types according to  [[time.parse.spec]]. Some flags can
be modified by a width parameter given as a positive decimal integer
called out as `N` below which governs how many characters are parsed
from the stream in interpreting the flag. All characters in the format
string that are not represented in  [[time.parse.spec]], except for
whitespace, are parsed unchanged from the stream. A whitespace character
matches zero or more whitespace characters in the input stream.

If the type being parsed cannot represent the information that the
format flag refers to, `is.setstate(ios_base::failbit)` is called.

[*Example 1*: A `duration` cannot represent a
`weekday`. — *end example*\]

However, if a flag refers to a “time of day” (e.g., `%H`, `%I`, `%p`,
etc.), then a specialization of `duration` is parsed as the time of day
elapsed since midnight.

If the `from_stream` overload fails to parse everything specified by the
format string, or if insufficient information is parsed to specify a
complete duration, time point, or calendrical data structure,
`setstate(ios_base::failbit)` is called on the `basic_istream`.

**Table: Meaning of `parse` flags**

| Flag | Parsed value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `%a` | The locale's full or abbreviated case-insensitive weekday name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `%A` | Equivalent to `%a`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%b` | The locale's full or abbreviated case-insensitive month name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `%B` | Equivalent to `%b`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%c` | The locale's date and time representation. The modified command `%Ec` interprets the locale's alternate date and time representation.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `%C` | The century as a decimal number. The modified command `%*N*C` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%EC` interprets the locale's alternative representation of the century.                                                                                                                                                                                                                                                                 |
| `%d` | The day of the month as a decimal number. The modified command `%*N*d` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%Od` interprets the locale's alternative representation of the day of the month.                                                                                                                                                                                                                                               |
| `%D` | Equivalent to `%m/%d/%y`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `%e` | Equivalent to `%d` and can be modified like `%d`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `%F` | Equivalent to `%Y-%m-%d`. If modified with a width `*N*`, the width is applied to only `%Y`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `%g` | The last two decimal digits of the ISO week-based year. The modified command `%*N*g` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required.                                                                                                                                                                                                                                                                                                                                        |
| `%G` | The ISO week-based year as a decimal number. The modified command `%*N*G` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 4. Leading zeroes are permitted but not required.                                                                                                                                                                                                                                                                                                                                                   |
| `%h` | Equivalent to `%b`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%H` | The hour (24-hour clock) as a decimal number. The modified command `%*N*H` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%OH` interprets the locale's alternative representation.                                                                                                                                                                                                                                                                   |
| `%I` | The hour (12-hour clock) as a decimal number. The modified command `%*N*I` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%OI` interprets the locale's alternative representation.                                                                                                                                                                                                                                                                   |
| `%j` | If the type being parsed is a specialization of `duration`, a decimal number of `days`. Otherwise, the day of the year as a decimal number. Jan 1 is `1`. In either case, the modified command `%*N*j` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 3. Leading zeroes are permitted but not required.                                                                                                                                                                                                                      |
| `%m` | The month as a decimal number. Jan is `1`. The modified command `%*N*m` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%Om` interprets the locale's alternative representation.                                                                                                                                                                                                                                                                      |
| `%M` | The minutes as a decimal number. The modified command `%*N*M` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%OM` interprets the locale's alternative representation.                                                                                                                                                                                                                                                                                |
| `%n` | Matches one whitespace character. *`%n`, `%t`, and a space can be combined to match a wide range of whitespace patterns. For example, `"%n "` matches one or more whitespace characters, and `"%n%t%t"` matches one to three whitespace characters.*                                                                                                                                                                                                                                                                                                                        |
| `%p` | The locale's equivalent of the AM/PM designations associated with a 12-hour clock.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `%r` | The locale's 12-hour clock time.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `%R` | Equivalent to `%H:%M`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `%S` | The seconds as a decimal number. The modified command `%*N*S` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2 if the input time has a precision convertible to seconds. Otherwise the default width is determined by the decimal precision of the input and the field is interpreted as a `long double` in a fixed format. If encountered, the locale determines the decimal point character. Leading zeroes are permitted but not required. The modified command `%OS` interprets the locale's alternative representation. |
| `%t` | Matches zero or one whitespace characters.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `%T` | Equivalent to `%H:%M:%S`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `%u` | The ISO weekday as a decimal number (`1`-`7`), where Monday is `1`. The modified command `%*N*u` specifies the maximum number of characters to read. If `*N*` is not specified, the default is `1`. Leading zeroes are permitted but not required.                                                                                                                                                                                                                                                                                                                          |
| `%U` | The week number of the year as a decimal number. The first Sunday of the year is the first day of week `01`. Days of the same year prior to that are in week `00`. The modified command `%*N*U` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%OU` interprets the locale's alternative representation.                                                                                                                                              |
| `%V` | The ISO week-based week number as a decimal number. The modified command `%*N*V` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required.                                                                                                                                                                                                                                                                                                                                            |
| `%w` | The weekday as a decimal number (`0`-`6`), where Sunday is `0`. The modified command `%*N*w` specifies the maximum number of characters to read. If `*N*` is not specified, the default is `1`. Leading zeroes are permitted but not required. The modified command `%Ow` interprets the locale's alternative representation.                                                                                                                                                                                                                                               |
| `%W` | The week number of the year as a decimal number. The first Monday of the year is the first day of week `01`. Days of the same year prior to that are in week `00`. The modified command `%*N*W` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified command `%OW` interprets the locale's alternative representation.                                                                                                                                              |
| `%x` | The locale's date representation. The modified command `%Ex` interprets the locale's alternate date representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%X` | The locale's time representation. The modified command `%EX` interprets the locale's alternate time representation.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `%y` | The last two decimal digits of the year. If the century is not otherwise specified (e.g., with `%C`), values in the range {[}`69`, `99`{]} are presumed to refer to the years 1969 to 1999, and values in the range {[}`00`, `68`{]} are presumed to refer to the years 2000 to 2068. The modified command `%*N*y` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 2. Leading zeroes are permitted but not required. The modified commands `%Ey` and `%Oy` interpret the locale's alternative representation.                 |
| `%Y` | The year as a decimal number. The modified command `%*N*Y` specifies the maximum number of characters to read. If `*N*` is not specified, the default is 4. Leading zeroes are permitted but not required. The modified command `%EY` interprets the locale's alternative representation.                                                                                                                                                                                                                                                                                   |
| `%z` | The offset from UTC in the format `[+|-]hh[mm]`. For example `-0430` refers to 4 hours 30 minutes behind UTC, and `04` refers to 4 hours ahead of UTC. The modified commands `%Ez` and `%Oz` parse a `:` between the hours and minutes and render leading zeroes on the hour field optional: `[+|-]h[h][:mm]`. For example `-04:30` refers to 4 hours 30 minutes behind UTC, and `4` refers to 4 hours ahead of UTC.                                                                                                                                                        |
| `%Z` | The time zone abbreviation or name. A single word is parsed. This word can only contain characters from the basic character set [[lex.charset]] that are alphanumeric, or one of `'_'`, `'/'`, `'-'`, or `'+'`.                                                                                                                                                                                                                                                                                                                                                             |
| `%%` | A `%` character is extracted.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |


## Header `<ctime>` synopsis <a id="ctime.syn">[[ctime.syn]]</a>

``` cpp
#define NULL see [support.types.nullptr]
#define CLOCKS_PER_SEC see below
#define TIME_UTC see below

namespace std {
  using size_t = see [support.types.layout];
  using clock_t = see below;
  using time_t = see below;

  struct timespec;
  struct tm;

  clock_t clock();
  double difftime(time_t time1, time_t time0);
  time_t mktime(tm* timeptr);
  time_t time(time_t* timer);
  int timespec_get(timespec* ts, int base);
  char* asctime(const tm* timeptr);
  char* ctime(const time_t* timer);
  tm* gmtime(const time_t* timer);
  tm* localtime(const time_t* timer);
  size_t strftime(char* s, size_t maxsize, const char* format, const tm* timeptr);
}
```

The contents of the header `<ctime>` are the same as the C standard
library header `<time.h>`.[^1]

The functions `asctime`, `ctime`, `gmtime`, and `localtime` are not
required to avoid data races [[res.on.data.races]].

<!-- Section link definitions -->
[ctime.syn]: #ctime.syn
[time]: #time
[time.12]: #time.12
[time.cal]: #time.cal
[time.cal.day]: #time.cal.day
[time.cal.day.members]: #time.cal.day.members
[time.cal.day.nonmembers]: #time.cal.day.nonmembers
[time.cal.day.overview]: #time.cal.day.overview
[time.cal.general]: #time.cal.general
[time.cal.last]: #time.cal.last
[time.cal.md]: #time.cal.md
[time.cal.md.members]: #time.cal.md.members
[time.cal.md.nonmembers]: #time.cal.md.nonmembers
[time.cal.md.overview]: #time.cal.md.overview
[time.cal.mdlast]: #time.cal.mdlast
[time.cal.month]: #time.cal.month
[time.cal.month.members]: #time.cal.month.members
[time.cal.month.nonmembers]: #time.cal.month.nonmembers
[time.cal.month.overview]: #time.cal.month.overview
[time.cal.mwd]: #time.cal.mwd
[time.cal.mwd.members]: #time.cal.mwd.members
[time.cal.mwd.nonmembers]: #time.cal.mwd.nonmembers
[time.cal.mwd.overview]: #time.cal.mwd.overview
[time.cal.mwdlast]: #time.cal.mwdlast
[time.cal.mwdlast.members]: #time.cal.mwdlast.members
[time.cal.mwdlast.nonmembers]: #time.cal.mwdlast.nonmembers
[time.cal.mwdlast.overview]: #time.cal.mwdlast.overview
[time.cal.operators]: #time.cal.operators
[time.cal.wd]: #time.cal.wd
[time.cal.wd.members]: #time.cal.wd.members
[time.cal.wd.nonmembers]: #time.cal.wd.nonmembers
[time.cal.wd.overview]: #time.cal.wd.overview
[time.cal.wdidx]: #time.cal.wdidx
[time.cal.wdidx.members]: #time.cal.wdidx.members
[time.cal.wdidx.nonmembers]: #time.cal.wdidx.nonmembers
[time.cal.wdidx.overview]: #time.cal.wdidx.overview
[time.cal.wdlast]: #time.cal.wdlast
[time.cal.wdlast.members]: #time.cal.wdlast.members
[time.cal.wdlast.nonmembers]: #time.cal.wdlast.nonmembers
[time.cal.wdlast.overview]: #time.cal.wdlast.overview
[time.cal.year]: #time.cal.year
[time.cal.year.members]: #time.cal.year.members
[time.cal.year.nonmembers]: #time.cal.year.nonmembers
[time.cal.year.overview]: #time.cal.year.overview
[time.cal.ym]: #time.cal.ym
[time.cal.ym.members]: #time.cal.ym.members
[time.cal.ym.nonmembers]: #time.cal.ym.nonmembers
[time.cal.ym.overview]: #time.cal.ym.overview
[time.cal.ymd]: #time.cal.ymd
[time.cal.ymd.members]: #time.cal.ymd.members
[time.cal.ymd.nonmembers]: #time.cal.ymd.nonmembers
[time.cal.ymd.overview]: #time.cal.ymd.overview
[time.cal.ymdlast]: #time.cal.ymdlast
[time.cal.ymdlast.members]: #time.cal.ymdlast.members
[time.cal.ymdlast.nonmembers]: #time.cal.ymdlast.nonmembers
[time.cal.ymdlast.overview]: #time.cal.ymdlast.overview
[time.cal.ymwd]: #time.cal.ymwd
[time.cal.ymwd.members]: #time.cal.ymwd.members
[time.cal.ymwd.nonmembers]: #time.cal.ymwd.nonmembers
[time.cal.ymwd.overview]: #time.cal.ymwd.overview
[time.cal.ymwdlast]: #time.cal.ymwdlast
[time.cal.ymwdlast.members]: #time.cal.ymwdlast.members
[time.cal.ymwdlast.nonmembers]: #time.cal.ymwdlast.nonmembers
[time.cal.ymwdlast.overview]: #time.cal.ymwdlast.overview
[time.clock]: #time.clock
[time.clock.cast]: #time.clock.cast
[time.clock.cast.fn]: #time.clock.cast.fn
[time.clock.cast.id]: #time.clock.cast.id
[time.clock.cast.sys]: #time.clock.cast.sys
[time.clock.cast.sys.utc]: #time.clock.cast.sys.utc
[time.clock.cast.utc]: #time.clock.cast.utc
[time.clock.conv]: #time.clock.conv
[time.clock.file]: #time.clock.file
[time.clock.file.members]: #time.clock.file.members
[time.clock.file.nonmembers]: #time.clock.file.nonmembers
[time.clock.file.overview]: #time.clock.file.overview
[time.clock.general]: #time.clock.general
[time.clock.gps]: #time.clock.gps
[time.clock.gps.members]: #time.clock.gps.members
[time.clock.gps.nonmembers]: #time.clock.gps.nonmembers
[time.clock.gps.overview]: #time.clock.gps.overview
[time.clock.hires]: #time.clock.hires
[time.clock.local]: #time.clock.local
[time.clock.req]: #time.clock.req
[time.clock.steady]: #time.clock.steady
[time.clock.system]: #time.clock.system
[time.clock.system.members]: #time.clock.system.members
[time.clock.system.nonmembers]: #time.clock.system.nonmembers
[time.clock.system.overview]: #time.clock.system.overview
[time.clock.tai]: #time.clock.tai
[time.clock.tai.members]: #time.clock.tai.members
[time.clock.tai.nonmembers]: #time.clock.tai.nonmembers
[time.clock.tai.overview]: #time.clock.tai.overview
[time.clock.utc]: #time.clock.utc
[time.clock.utc.members]: #time.clock.utc.members
[time.clock.utc.nonmembers]: #time.clock.utc.nonmembers
[time.clock.utc.overview]: #time.clock.utc.overview
[time.duration]: #time.duration
[time.duration.alg]: #time.duration.alg
[time.duration.arithmetic]: #time.duration.arithmetic
[time.duration.cast]: #time.duration.cast
[time.duration.comparisons]: #time.duration.comparisons
[time.duration.cons]: #time.duration.cons
[time.duration.general]: #time.duration.general
[time.duration.io]: #time.duration.io
[time.duration.literals]: #time.duration.literals
[time.duration.nonmember]: #time.duration.nonmember
[time.duration.observer]: #time.duration.observer
[time.duration.special]: #time.duration.special
[time.format]: #time.format
[time.general]: #time.general
[time.hms]: #time.hms
[time.hms.members]: #time.hms.members
[time.hms.nonmembers]: #time.hms.nonmembers
[time.hms.overview]: #time.hms.overview
[time.parse]: #time.parse
[time.point]: #time.point
[time.point.arithmetic]: #time.point.arithmetic
[time.point.cast]: #time.point.cast
[time.point.comparisons]: #time.point.comparisons
[time.point.cons]: #time.point.cons
[time.point.general]: #time.point.general
[time.point.nonmember]: #time.point.nonmember
[time.point.observer]: #time.point.observer
[time.point.special]: #time.point.special
[time.syn]: #time.syn
[time.traits]: #time.traits
[time.traits.duration.values]: #time.traits.duration.values
[time.traits.is.clock]: #time.traits.is.clock
[time.traits.is.fp]: #time.traits.is.fp
[time.traits.specializations]: #time.traits.specializations
[time.zone]: #time.zone
[time.zone.db]: #time.zone.db
[time.zone.db.access]: #time.zone.db.access
[time.zone.db.list]: #time.zone.db.list
[time.zone.db.remote]: #time.zone.db.remote
[time.zone.db.tzdb]: #time.zone.db.tzdb
[time.zone.exception]: #time.zone.exception
[time.zone.exception.ambig]: #time.zone.exception.ambig
[time.zone.exception.nonexist]: #time.zone.exception.nonexist
[time.zone.general]: #time.zone.general
[time.zone.info]: #time.zone.info
[time.zone.info.local]: #time.zone.info.local
[time.zone.info.sys]: #time.zone.info.sys
[time.zone.leap]: #time.zone.leap
[time.zone.leap.members]: #time.zone.leap.members
[time.zone.leap.nonmembers]: #time.zone.leap.nonmembers
[time.zone.leap.overview]: #time.zone.leap.overview
[time.zone.link]: #time.zone.link
[time.zone.link.members]: #time.zone.link.members
[time.zone.link.nonmembers]: #time.zone.link.nonmembers
[time.zone.link.overview]: #time.zone.link.overview
[time.zone.members]: #time.zone.members
[time.zone.nonmembers]: #time.zone.nonmembers
[time.zone.overview]: #time.zone.overview
[time.zone.timezone]: #time.zone.timezone
[time.zone.zonedtime]: #time.zone.zonedtime
[time.zone.zonedtime.ctor]: #time.zone.zonedtime.ctor
[time.zone.zonedtime.members]: #time.zone.zonedtime.members
[time.zone.zonedtime.nonmembers]: #time.zone.zonedtime.nonmembers
[time.zone.zonedtime.overview]: #time.zone.zonedtime.overview
[time.zone.zonedtraits]: #time.zone.zonedtraits

<!-- Link reference definitions -->
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[cpp17.equalitycomparable]: #cpp17.equalitycomparable
[cpp17.lessthancomparable]: #cpp17.lessthancomparable
[ctime.syn]: #ctime.syn
[dcl.constexpr]: dcl.md#dcl.constexpr
[filesystems]: input.md#filesystems
[format.formatter]: utilities.md#format.formatter
[format.string]: utilities.md#format.string
[formatter.requirements]: utilities.md#formatter.requirements
[intro.multithread]: basic.md#intro.multithread
[lex.charset]: lex.md#lex.charset
[meta.rqmts]: meta.md#meta.rqmts
[numeric.requirements]: numerics.md#numeric.requirements
[over.ics.rank]: over.md#over.ics.rank
[over.match.class.deduct]: over.md#over.match.class.deduct
[res.on.data.races]: library.md#res.on.data.races
[swappable.requirements]: library.md#swappable.requirements
[temp.deduct]: temp.md#temp.deduct
[term.unevaluated.operand]: #term.unevaluated.operand
[time.12]: #time.12
[time.cal]: #time.cal
[time.clock]: #time.clock
[time.clock.cast.id]: #time.clock.cast.id
[time.clock.cast.sys]: #time.clock.cast.sys
[time.clock.cast.sys.utc]: #time.clock.cast.sys.utc
[time.clock.cast.utc]: #time.clock.cast.utc
[time.clock.req]: #time.clock.req
[time.duration]: #time.duration
[time.duration.io]: #time.duration.io
[time.format]: #time.format
[time.format.spec]: #time.format.spec
[time.hms]: #time.hms
[time.hms.width]: #time.hms.width
[time.parse]: #time.parse
[time.parse.spec]: #time.parse.spec
[time.point]: #time.point
[time.point.general]: #time.point.general
[time.summary]: #time.summary
[time.syn]: #time.syn
[time.traits]: #time.traits
[time.zone]: #time.zone

[^1]: `strftime` supports the C conversion specifiers `C`, `D`, `e`,
    `F`, `g`, `G`, `h`, `r`, `R`, `t`, `T`, `u`, `V`, and `z`, and the
    modifiers `E` and `O`.
