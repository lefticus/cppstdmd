# Algorithms library <a id="algorithms">[[algorithms]]</a>

## General <a id="algorithms.general">[[algorithms.general]]</a>

This Clause describes components that C++programs may use to perform
algorithmic operations on containers (Clause  [[containers]]) and other
sequences.

The following subclauses describe components for non-modifying sequence
operation, modifying sequence operations, sorting and related
operations, and algorithms from the ISO C library, as summarized in
Table  [[tab:algorithms.summary]].

**Table: Algorithms library summary**

| Subclause                    |                                   | Header        |
| ---------------------------- | --------------------------------- | ------------- |
| [[alg.nonmodifying]]         | Non-modifying sequence operations |               |
| [[alg.modifying.operations]] | Mutating sequence operations      | `<algorithm>` |
| [[alg.sorting]]              | Sorting and related operations    |               |
| [[alg.c.library]]            | C library algorithms              | `<cstdlib>`   |

``` cpp
#include <initializer_list>

namespace std {

  // [alg.nonmodifying], non-modifying sequence operations:
  template <class InputIterator, class Predicate>
    bool all_of(InputIterator first, InputIterator last, Predicate pred);
  template <class InputIterator, class Predicate>
    bool any_of(InputIterator first, InputIterator last, Predicate pred);
  template <class InputIterator, class Predicate>
    bool none_of(InputIterator first, InputIterator last, Predicate pred);

  template<class InputIterator, class Function>
    Function for_each(InputIterator first, InputIterator last, Function f);
  template<class InputIterator, class T>
    InputIterator find(InputIterator first, InputIterator last,
                       const T& value);
  template<class InputIterator, class Predicate>
    InputIterator find_if(InputIterator first, InputIterator last,
                          Predicate pred);
  template<class InputIterator, class Predicate>
    InputIterator find_if_not(InputIterator first, InputIterator last,
                              Predicate pred);
  template<class ForwardIterator1, class ForwardIterator2>
    ForwardIterator1
      find_end(ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ForwardIterator1, class ForwardIterator2,
     class BinaryPredicate>
    ForwardIterator1
      find_end(ForwardIterator1 first1, ForwardIterator1 last1,
               ForwardIterator2 first2, ForwardIterator2 last2,
               BinaryPredicate pred);

  template<class InputIterator, class ForwardIterator>
    InputIterator
      find_first_of(InputIterator first1, InputIterator last1,
                    ForwardIterator first2, ForwardIterator last2);
  template<class InputIterator, class ForwardIterator,
     class BinaryPredicate>
    InputIterator
      find_first_of(InputIterator first1, InputIterator last1,
                    ForwardIterator first2, ForwardIterator last2,
                    BinaryPredicate pred);

  template<class ForwardIterator>
    ForwardIterator adjacent_find(ForwardIterator first,
                                  ForwardIterator last);
  template<class ForwardIterator, class BinaryPredicate>
    ForwardIterator adjacent_find(ForwardIterator first,
                                  ForwardIterator last,
                                  BinaryPredicate pred);

  template<class InputIterator, class T>
    typename iterator_traits<InputIterator>::difference_type
      count(InputIterator first, InputIterator last, const T& value);
  template<class InputIterator, class Predicate>
    typename iterator_traits<InputIterator>::difference_type
      count_if(InputIterator first, InputIterator last, Predicate pred);

  template<class InputIterator1, class InputIterator2>
    pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2);
  template
   <class InputIterator1, class InputIterator2, class BinaryPredicate>
    pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, BinaryPredicate pred);

  template<class InputIterator1, class InputIterator2>
    pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, InputIterator2 last2);

  template
   <class InputIterator1, class InputIterator2, class BinaryPredicate>
    pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, InputIterator2 last2,
               BinaryPredicate pred);

  template<class InputIterator1, class InputIterator2>
    bool equal(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2);
  template
   <class InputIterator1, class InputIterator2, class BinaryPredicate>
    bool equal(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, BinaryPredicate pred);

  template<class InputIterator1, class InputIterator2>
    bool equal(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, InputIterator2 last2);

  template
   <class InputIterator1, class InputIterator2, class BinaryPredicate>
    bool equal(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, InputIterator2 last2,
               BinaryPredicate pred);

  template<class ForwardIterator1, class ForwardIterator2>
    bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                        ForwardIterator2 first2);
  template<class ForwardIterator1, class ForwardIterator2,
                   class BinaryPredicate>
    bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                        ForwardIterator2 first2, BinaryPredicate pred);

  template<class ForwardIterator1, class ForwardIterator2>
    bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                        ForwardIterator2 first2, ForwardIterator2 last2);

  template<class ForwardIterator1, class ForwardIterator2,
                      class BinaryPredicate>
    bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                        ForwardIterator2 first2, ForwardIterator2 last2,
                        BinaryPredicate pred);

  template<class ForwardIterator1, class ForwardIterator2>
    ForwardIterator1 search(
      ForwardIterator1 first1, ForwardIterator1 last1,
      ForwardIterator2 first2, ForwardIterator2 last2);
  template<class ForwardIterator1, class ForwardIterator2,
     class BinaryPredicate>
    ForwardIterator1 search(
      ForwardIterator1 first1, ForwardIterator1 last1,
      ForwardIterator2 first2, ForwardIterator2 last2,
      BinaryPredicate pred);
  template<class ForwardIterator, class Size, class T>
    ForwardIterator search_n(ForwardIterator first, ForwardIterator last,
                             Size count, const T& value);
  template
   <class ForwardIterator, class Size, class T, class BinaryPredicate>
    ForwardIterator search_n(ForwardIterator first, ForwardIterator last,
                             Size count, const T& value,
                             BinaryPredicate pred);

  // [alg.modifying.operations], modifying sequence operations:
  // [alg.copy], copy:
  template<class InputIterator, class OutputIterator>
    OutputIterator copy(InputIterator first, InputIterator last,
                        OutputIterator result);
  template<class InputIterator, class Size, class OutputIterator>
    OutputIterator copy_n(InputIterator first, Size n,
                          OutputIterator result);
  template<class InputIterator, class OutputIterator, class Predicate>
    OutputIterator copy_if(InputIterator first, InputIterator last,
                          OutputIterator result, Predicate pred);
  template<class BidirectionalIterator1, class BidirectionalIterator2>
    BidirectionalIterator2 copy_backward(
      BidirectionalIterator1 first, BidirectionalIterator1 last,
      BidirectionalIterator2 result);

  // [alg.move], move:
  template<class InputIterator, class OutputIterator>
    OutputIterator move(InputIterator first, InputIterator last,
                        OutputIterator result);
  template<class BidirectionalIterator1, class BidirectionalIterator2>
    BidirectionalIterator2 move_backward(
      BidirectionalIterator1 first, BidirectionalIterator1 last,
      BidirectionalIterator2 result);

  // [alg.swap], swap:
  template<class ForwardIterator1, class ForwardIterator2>
    ForwardIterator2 swap_ranges(ForwardIterator1 first1,
    ForwardIterator1 last1, ForwardIterator2 first2);
  template<class ForwardIterator1, class ForwardIterator2>
    void iter_swap(ForwardIterator1 a, ForwardIterator2 b);

  template<class InputIterator, class OutputIterator, class UnaryOperation>
    OutputIterator transform(InputIterator first, InputIterator last,
                             OutputIterator result, UnaryOperation op);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
     class BinaryOperation>
    OutputIterator transform(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, OutputIterator result,
                             BinaryOperation binary_op);

  template<class ForwardIterator, class T>
    void replace(ForwardIterator first, ForwardIterator last,
                 const T& old_value, const T& new_value);
  template<class ForwardIterator, class Predicate, class T>
    void replace_if(ForwardIterator first, ForwardIterator last,
                    Predicate pred, const T& new_value);
  template<class InputIterator, class OutputIterator, class T>
    OutputIterator replace_copy(InputIterator first, InputIterator last,
                                OutputIterator result,
                                const T& old_value, const T& new_value);
  template<class InputIterator, class OutputIterator, class Predicate, class T>
    OutputIterator replace_copy_if(InputIterator first, InputIterator last,
                                   OutputIterator result,
                                   Predicate pred, const T& new_value);

  template<class ForwardIterator, class T>
    void fill(ForwardIterator first, ForwardIterator last, const T& value);
  template<class OutputIterator, class Size, class T>
    OutputIterator fill_n(OutputIterator first, Size n, const T& value);

  template<class ForwardIterator, class Generator>
    void generate(ForwardIterator first, ForwardIterator last,
                  Generator gen);
  template<class OutputIterator, class Size, class Generator>
    OutputIterator generate_n(OutputIterator first, Size n, Generator gen);

  template<class ForwardIterator, class T>
    ForwardIterator remove(ForwardIterator first, ForwardIterator last,
                           const T& value);
  template<class ForwardIterator, class Predicate>
    ForwardIterator remove_if(ForwardIterator first, ForwardIterator last,
                              Predicate pred);
  template<class InputIterator, class OutputIterator, class T>
    OutputIterator remove_copy(InputIterator first, InputIterator last,
                               OutputIterator result, const T& value);
  template<class InputIterator, class OutputIterator, class Predicate>
    OutputIterator remove_copy_if(InputIterator first, InputIterator last,
                                  OutputIterator result, Predicate pred);

  template<class ForwardIterator>
    ForwardIterator unique(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class BinaryPredicate>
    ForwardIterator unique(ForwardIterator first, ForwardIterator last,
                           BinaryPredicate pred);
  template<class InputIterator, class OutputIterator>
    OutputIterator unique_copy(InputIterator first, InputIterator last,
                               OutputIterator result);
  template<class InputIterator, class OutputIterator, class BinaryPredicate>
    OutputIterator unique_copy(InputIterator first, InputIterator last,
                               OutputIterator result, BinaryPredicate pred);

  template<class BidirectionalIterator>
    void reverse(BidirectionalIterator first, BidirectionalIterator last);
  template<class BidirectionalIterator, class OutputIterator>
    OutputIterator reverse_copy(BidirectionalIterator first,
                                BidirectionalIterator last,
                                OutputIterator result);

  template<class ForwardIterator>
    ForwardIterator rotate(ForwardIterator first, ForwardIterator middle,
                           ForwardIterator last);
  template<class ForwardIterator, class OutputIterator>
    OutputIterator rotate_copy(
      ForwardIterator first, ForwardIterator middle,
      ForwardIterator last, OutputIterator result);

  // [depr.alg.random.shuffle], random_shuffle (deprecated):
  template<class RandomAccessIterator>
    void random_shuffle(RandomAccessIterator first,
                        RandomAccessIterator last);
  template<class RandomAccessIterator, class RandomNumberGenerator>
    void random_shuffle(RandomAccessIterator first,
                        RandomAccessIterator last,
                        RandomNumberGenerator&& rng);

  // [alg.random.shuffle], shuffle:
  template<class RandomAccessIterator, class UniformRandomNumberGenerator>
    void shuffle(RandomAccessIterator first,
                        RandomAccessIterator last,
                        UniformRandomNumberGenerator&& g);

  // [alg.partitions], partitions:
  template <class InputIterator, class Predicate>
    bool is_partitioned(InputIterator first, InputIterator last, Predicate pred);

  template<class ForwardIterator, class Predicate>
    ForwardIterator partition(ForwardIterator first,
                              ForwardIterator last,
                              Predicate pred);
  template<class BidirectionalIterator, class Predicate>
    BidirectionalIterator stable_partition(BidirectionalIterator first,
                                           BidirectionalIterator last,
                                           Predicate pred);
  template <class InputIterator, class OutputIterator1,
            class OutputIterator2, class Predicate>
    pair<OutputIterator1, OutputIterator2>
    partition_copy(InputIterator first, InputIterator last,
                   OutputIterator1 out_true, OutputIterator2 out_false,
                   Predicate pred);
  template<class ForwardIterator, class Predicate>
    ForwardIterator partition_point(ForwardIterator first,
                                    ForwardIterator last,
                                    Predicate pred);

  // [alg.sorting], sorting and related operations:
  // [alg.sort], sorting:
  template<class RandomAccessIterator>
    void sort(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void sort(RandomAccessIterator first, RandomAccessIterator last,
              Compare comp);

  template<class RandomAccessIterator>
    void stable_sort(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void stable_sort(RandomAccessIterator first, RandomAccessIterator last,
                     Compare comp);

  template<class RandomAccessIterator>
    void partial_sort(RandomAccessIterator first,
                      RandomAccessIterator middle,
                      RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void partial_sort(RandomAccessIterator first,
                      RandomAccessIterator middle,
                      RandomAccessIterator last, Compare comp);
  template<class InputIterator, class RandomAccessIterator>
    RandomAccessIterator partial_sort_copy(
      InputIterator first, InputIterator last,
      RandomAccessIterator result_first,
      RandomAccessIterator result_last);
  template<class InputIterator, class RandomAccessIterator, class Compare>
    RandomAccessIterator partial_sort_copy(
      InputIterator first, InputIterator last,
      RandomAccessIterator result_first,
      RandomAccessIterator result_last,
      Compare comp);
  template<class ForwardIterator>
    bool is_sorted(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    bool is_sorted(ForwardIterator first, ForwardIterator last,
                   Compare comp);
  template<class ForwardIterator>
    ForwardIterator is_sorted_until(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    ForwardIterator is_sorted_until(ForwardIterator first, ForwardIterator last,
                                    Compare comp);

  template<class RandomAccessIterator>
    void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                     RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                     RandomAccessIterator last, Compare comp);

  // [alg.binary.search], binary search:
  template<class ForwardIterator, class T>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last,
                                const T& value);
  template<class ForwardIterator, class T, class Compare>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last,
                                const T& value, Compare comp);

  template<class ForwardIterator, class T>
    ForwardIterator upper_bound(ForwardIterator first, ForwardIterator last,
                                const T& value);
  template<class ForwardIterator, class T, class Compare>
    ForwardIterator upper_bound(ForwardIterator first, ForwardIterator last,
                                const T& value, Compare comp);

  template<class ForwardIterator, class T>
    pair<ForwardIterator, ForwardIterator>
      equal_range(ForwardIterator first, ForwardIterator last,
                  const T& value);
  template<class ForwardIterator, class T, class Compare>
    pair<ForwardIterator, ForwardIterator>
      equal_range(ForwardIterator first, ForwardIterator last,
                  const T& value, Compare comp);

  template<class ForwardIterator, class T>
    bool binary_search(ForwardIterator first, ForwardIterator last,
                       const T& value);
  template<class ForwardIterator, class T, class Compare>
    bool binary_search(ForwardIterator first, ForwardIterator last,
                       const T& value, Compare comp);

  // [alg.merge], merge:
  template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
     class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

  template<class BidirectionalIterator>
    void inplace_merge(BidirectionalIterator first,
                       BidirectionalIterator middle,
                       BidirectionalIterator last);
  template<class BidirectionalIterator, class Compare>
    void inplace_merge(BidirectionalIterator first,
                       BidirectionalIterator middle,
                       BidirectionalIterator last, Compare comp);

  // [alg.set.operations], set operations:
  template<class InputIterator1, class InputIterator2>
    bool includes(InputIterator1 first1, InputIterator1 last1,
                  InputIterator2 first2, InputIterator2 last2);
  template<class InputIterator1, class InputIterator2, class Compare>
    bool includes(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2, Compare comp);

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator set_union(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, InputIterator2 last2,
                             OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
     class Compare>
    OutputIterator set_union(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, InputIterator2 last2,
                             OutputIterator result, Compare comp);

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator set_intersection(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
     class Compare>
    OutputIterator set_intersection(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      OutputIterator result, Compare comp);

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator set_difference(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
     class Compare>
    OutputIterator set_difference(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      OutputIterator result, Compare comp);

  template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator set_symmetric_difference(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      OutputIterator result);
  template<class InputIterator1, class InputIterator2, class OutputIterator,
      class Compare>
    OutputIterator set_symmetric_difference(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      OutputIterator result, Compare comp);

  // [alg.heap.operations], heap operations:
  template<class RandomAccessIterator>
    void push_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void push_heap(RandomAccessIterator first, RandomAccessIterator last,
                   Compare comp);

  template<class RandomAccessIterator>
    void pop_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void pop_heap(RandomAccessIterator first, RandomAccessIterator last,
                  Compare comp);

  template<class RandomAccessIterator>
    void make_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void make_heap(RandomAccessIterator first, RandomAccessIterator last,
                   Compare comp);

  template<class RandomAccessIterator>
    void sort_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    void sort_heap(RandomAccessIterator first, RandomAccessIterator last,
                   Compare comp);

  template<class RandomAccessIterator>
    bool is_heap(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    bool is_heap(RandomAccessIterator first, RandomAccessIterator last, Compare comp);
  template<class RandomAccessIterator>
    RandomAccessIterator is_heap_until(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    RandomAccessIterator is_heap_until(RandomAccessIterator first, RandomAccessIterator last,
                                       Compare comp);

  // [alg.min.max], minimum and maximum:
  template<class T> constexpr const T& min(const T& a, const T& b);
  template<class T, class Compare>
    constexpr const T& min(const T& a, const T& b, Compare comp);
  template<class T>
    constexpr T min(initializer_list<T> t);
  template<class T, class Compare>
    constexpr T min(initializer_list<T> t, Compare comp);

  template<class T> constexpr const T& max(const T& a, const T& b);
  template<class T, class Compare>
    constexpr const T& max(const T& a, const T& b, Compare comp);
  template<class T>
    constexpr T max(initializer_list<T> t);
  template<class T, class Compare>
    constexpr T max(initializer_list<T> t, Compare comp);

  template<class T> constexpr pair<const T&, const T&> minmax(const T& a, const T& b);
  template<class T, class Compare>
    constexpr pair<const T&, const T&> minmax(const T& a, const T& b, Compare comp);
  template<class T>
    constexpr pair<T, T> minmax(initializer_list<T> t);
  template<class T, class Compare>
    constexpr pair<T, T> minmax(initializer_list<T> t, Compare comp);

  template<class ForwardIterator>
    ForwardIterator min_element(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    ForwardIterator min_element(ForwardIterator first, ForwardIterator last,
                                Compare comp);
  template<class ForwardIterator>
    ForwardIterator max_element(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    ForwardIterator max_element(ForwardIterator first, ForwardIterator last,
                                Compare comp);
  template<class ForwardIterator>
    pair<ForwardIterator, ForwardIterator>
      minmax_element(ForwardIterator first, ForwardIterator last);
  template<class ForwardIterator, class Compare>
    pair<ForwardIterator, ForwardIterator>
      minmax_element(ForwardIterator first, ForwardIterator last, Compare comp);

  template<class InputIterator1, class InputIterator2>
    bool lexicographical_compare(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2);
  template<class InputIterator1, class InputIterator2, class Compare>
    bool lexicographical_compare(
      InputIterator1 first1, InputIterator1 last1,
      InputIterator2 first2, InputIterator2 last2,
      Compare comp);

  // [alg.permutation.generators], permutations:
  template<class BidirectionalIterator>
    bool next_permutation(BidirectionalIterator first,
                          BidirectionalIterator last);
  template<class BidirectionalIterator, class Compare>
    bool next_permutation(BidirectionalIterator first,
                          BidirectionalIterator last, Compare comp);
  template<class BidirectionalIterator>
    bool prev_permutation(BidirectionalIterator first,
                          BidirectionalIterator last);
  template<class BidirectionalIterator, class Compare>
    bool prev_permutation(BidirectionalIterator first,
                          BidirectionalIterator last, Compare comp);
}
```

All of the algorithms are separated from the particular implementations
of data structures and are parameterized by iterator types. Because of
this, they can work with program-defined data structures, as long as
these data structures have iterator types satisfying the assumptions on
the algorithms.

For purposes of determining the existence of data races, algorithms
shall not modify objects referenced through an iterator argument unless
the specification requires such modification.

Throughout this Clause, the names of template parameters are used to
express type requirements.

- If an algorithm’s template parameter is named `InputIterator`,
  `InputIterator1`, or `InputIterator2`, the template argument shall
  satisfy the requirements of an input iterator ([[input.iterators]]).
- If an algorithm’s template parameter is named `OutputIterator`,
  `OutputIterator1`, or `OutputIterator2`, the template argument shall
  satisfy the requirements of an output iterator (
  [[output.iterators]]).
- If an algorithm’s template parameter is named `ForwardIterator`,
  `ForwardIterator1`, or `ForwardIterator2`, the template argument shall
  satisfy the requirements of a forward iterator (
  [[forward.iterators]]).
- If an algorithm’s template parameter is named `BidirectionalIterator`,
  `BidirectionalIterator1`, or `BidirectionalIterator2`, the template
  argument shall satisfy the requirements of a bidirectional iterator (
  [[bidirectional.iterators]]).
- If an algorithm’s template parameter is named `RandomAccessIterator`,
  `RandomAccessIterator1`, or `RandomAccessIterator2`, the template
  argument shall satisfy the requirements of a random-access iterator (
  [[random.access.iterators]]).

If an algorithm’s section says that a value pointed to by any iterator
passed as an argument is modified, then that algorithm has an additional
type requirement: The type of that argument shall satisfy the
requirements of a mutable iterator ([[iterator.requirements]]). This
requirement does not affect arguments that are named `OutputIterator`,
`OutputIterator1`, or `OutputIterator2`, because output iterators must
always be mutable.

Both in-place and copying versions are provided for certain
algorithms.[^1] When such a version is provided for *algorithm* it is
called *algorithm`_copy`*. Algorithms that take predicates end with the
suffix `_if` (which follows the suffix `_copy`).

The `Predicate` parameter is used whenever an algorithm expects a
function object ([[function.objects]]) that, when applied to the result
of dereferencing the corresponding iterator, returns a value testable as
`true`. In other words, if an algorithm takes `Predicate pred` as its
argument and `first` as its iterator argument, it should work correctly
in the construct `pred(*first)` contextually converted to `bool`
(Clause  [[conv]]). The function object `pred` shall not apply any
non-constant function through the dereferenced iterator.

The `BinaryPredicate` parameter is used whenever an algorithm expects a
function object that when applied to the result of dereferencing two
corresponding iterators or to dereferencing an iterator and type `T`
when `T` is part of the signature returns a value testable as `true`. In
other words, if an algorithm takes `BinaryPredicate binary_pred` as its
argument and `first1` and `first2` as its iterator arguments, it should
work correctly in the construct `binary_pred(*first1, *first2)`
contextually converted to `bool` (Clause  [[conv]]). `BinaryPredicate`
always takes the first iterator’s `value_type` as its first argument,
that is, in those cases when `T value` is part of the signature, it
should work correctly in the construct `binary_pred(*first1, value)`
contextually converted to `bool` (Clause  [[conv]]). `binary_pred` shall
not apply any non-constant function through the dereferenced iterators.

Unless otherwise specified, algorithms that take function objects as
arguments are permitted to copy those function objects freely.
Programmers for whom object identity is important should consider using
a wrapper class that points to a noncopied implementation object such as
`reference_wrapper<T>` ([[refwrap]]), or some equivalent solution.

When the description of an algorithm gives an expression such as
`*first == value` for a condition, the expression shall evaluate to
either true or false in boolean contexts.

In the description of the algorithms operators `+` and `-` are used for
some of the iterator categories for which they do not have to be
defined. In these cases the semantics of `a+n` is the same as that of

``` cpp
X tmp = a;
advance(tmp, n);
return tmp;
```

and that of `b-a` is the same as of

``` cpp
return distance(a, b);
```

## Non-modifying sequence operations <a id="alg.nonmodifying">[[alg.nonmodifying]]</a>

### All of <a id="alg.all_of">[[alg.all_of]]</a>

``` cpp
template <class InputIterator, class Predicate>
  bool all_of(InputIterator first, InputIterator last, Predicate pred);
```

*Returns:* `true` if \[`first`, `last`) is empty or if `pred(*i)` is
`true` for every iterator `i` in the range \[`first`, `last`), and
`false` otherwise.

*Complexity:* At most `last - first` applications of the predicate.

### Any of <a id="alg.any_of">[[alg.any_of]]</a>

``` cpp
template <class InputIterator, class Predicate>
  bool any_of(InputIterator first, InputIterator last, Predicate pred);
```

*Returns:* `false` if \[`first`, `last`) is empty or if there is no
iterator `i` in the range \[`first`, `last`) such that `pred(*i)` is
`true`, and `true` otherwise.

*Complexity:* At most `last - first` applications of the predicate.

### None of <a id="alg.none_of">[[alg.none_of]]</a>

``` cpp
template <class InputIterator, class Predicate>
  bool none_of(InputIterator first, InputIterator last, Predicate pred);
```

*Returns:* `true` if \[`first`, `last`) is empty or if `pred(*i)` is
`false` for every iterator `i` in the range \[`first`, `last`), and
`false` otherwise.

*Complexity:* At most `last - first` applications of the predicate.

### For each <a id="alg.foreach">[[alg.foreach]]</a>

``` cpp
template<class InputIterator, class Function>
  Function for_each(InputIterator first, InputIterator last, Function f);
```

*Requires:* `Function` shall meet the requirements of
`MoveConstructible` (Table  [[moveconstructible]]). `Function` need not
meet the requirements of `CopyConstructible`
(Table  [[copyconstructible]]).

*Effects:* Applies `f` to the result of dereferencing every iterator in
the range \[`first`, `last`), starting from `first` and proceeding to
`last - 1`. If the type of `first` satisfies the requirements of a
mutable iterator, `f` may apply nonconstant functions through the
dereferenced iterator.

*Returns:* `std::move(f)`.

*Complexity:* Applies `f` exactly `last - first` times.

*Remarks:* If `f` returns a result, the result is ignored.

### Find <a id="alg.find">[[alg.find]]</a>

``` cpp
template<class InputIterator, class T>
  InputIterator find(InputIterator first, InputIterator last,
                     const T& value);

template<class InputIterator, class Predicate>
  InputIterator find_if(InputIterator first, InputIterator last,
                        Predicate pred);
template<class InputIterator, class Predicate>
  InputIterator find_if_not(InputIterator first, InputIterator last,
                            Predicate pred);
```

*Returns:* The first iterator `i` in the range \[`first`, `last`) for
which the following corresponding conditions hold: `*i == value`,
`pred(*i) != false`, `pred(*i) == false`. Returns `last` if no such
iterator is found.

*Complexity:* At most `last - first` applications of the corresponding
predicate.

### Find end <a id="alg.find.end">[[alg.find.end]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  ForwardIterator1
    find_end(ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2);

template<class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  ForwardIterator1
    find_end(ForwardIterator1 first1, ForwardIterator1 last1,
             ForwardIterator2 first2, ForwardIterator2 last2,
             BinaryPredicate pred);
```

*Effects:* Finds a subsequence of equal values in a sequence.

*Returns:* The last iterator `i` in the range \[`first1`,
`last1 - (last2 - first2)`) such that for every non-negative integer
`n < (last2 - first2)`, the following corresponding conditions hold:
`*(i + n) == *(first2 + n), pred(*(i + n), *(first2 + n)) != false`.
Returns `last1` if \[`first2`, `last2`) is empty or if no such iterator
is found.

*Complexity:* At most
`(last2 - first2) * (last1 - first1 - (last2 - first2) + 1)`
applications of the corresponding predicate.

### Find first <a id="alg.find.first.of">[[alg.find.first.of]]</a>

``` cpp
template<class InputIterator, class ForwardIterator>
  InputIterator
    find_first_of(InputIterator first1, InputIterator last1,
                  ForwardIterator first2, ForwardIterator last2);

template<class InputIterator, class ForwardIterator,
          class BinaryPredicate>
  InputIterator
    find_first_of(InputIterator first1, InputIterator last1,
                  ForwardIterator first2, ForwardIterator last2,
                  BinaryPredicate pred);
```

*Effects:* Finds an element that matches one of a set of values.

*Returns:* The first iterator `i` in the range \[`first1`, `last1`) such
that for some iterator `j` in the range \[`first2`, `last2`) the
following conditions hold: `*i == *j, pred(*i,*j) != false`. Returns
`last1` if \[`first2`, `last2`) is empty or if no such iterator is
found.

*Complexity:* At most `(last1-first1) * (last2-first2)` applications of
the corresponding predicate.

### Adjacent find <a id="alg.adjacent.find">[[alg.adjacent.find]]</a>

``` cpp
template<class ForwardIterator>
  ForwardIterator adjacent_find(ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class BinaryPredicate>
  ForwardIterator adjacent_find(ForwardIterator first, ForwardIterator last,
                              BinaryPredicate pred);
```

*Returns:* The first iterator `i` such that both `i` and `i + 1` are in
the range \[`first`, `last`) for which the following corresponding
conditions hold: `*i == *(i + 1), pred(*i, *(i + 1)) != false`. Returns
`last` if no such iterator is found.

*Complexity:* For a nonempty range, exactly
`min((i - first) + 1, (last - first) - 1)` applications of the
corresponding predicate, where `i` is `adjacent_find`’s return value.

### Count <a id="alg.count">[[alg.count]]</a>

``` cpp
template<class InputIterator, class T>
    typename iterator_traits<InputIterator>::difference_type
       count(InputIterator first, InputIterator last, const T& value);

template<class InputIterator, class Predicate>
    typename iterator_traits<InputIterator>::difference_type
      count_if(InputIterator first, InputIterator last, Predicate pred);
```

*Effects:* Returns the number of iterators `i` in the range \[`first`,
`last`) for which the following corresponding conditions hold:
`*i == value, pred(*i) != false`.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate.

### Mismatch <a id="mismatch">[[mismatch]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2);

template<class InputIterator1, class InputIterator2,
          class BinaryPredicate>
  pair<InputIterator1, InputIterator2>
      mismatch(InputIterator1 first1, InputIterator1 last1,
               InputIterator2 first2, BinaryPredicate pred);

template<class InputIterator1, class InputIterator2>
  pair<InputIterator1, InputIterator2>
    mismatch(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, InputIterator2 last2);

template <class InputIterator1, class InputIterator2,
           class BinaryPredicate>
  pair<InputIterator1, InputIterator2>
    mismatch(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, InputIterator2 last2,
             BinaryPredicate pred);
```

*Remarks:* If `last2` was not given in the argument list, it denotes
`first2 + (last1 - first1)` below.

*Returns:* A pair of iterators `i` and `j` such that
`j == first2 + (i - first1)` and `i` is the first iterator in the range
\[`first1`, `last1`) for which the following corresponding conditions
hold:

- `j` is in the range `[first2, last2)`.
- `!(*i == *(first2 + (i - first1)))`
- `pred(*i, *(first2 + (i - first1))) == false`

Returns the pair `first1 + min(last1 - first1, last2 - first2)` and
`first2 + min(last1 - first1, last2 - first2)` if such an iterator `i`
is not found.

*Complexity:* At most `last1 - first1` applications of the corresponding
predicate.

### Equal <a id="alg.equal">[[alg.equal]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  bool equal(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2);

template<class InputIterator1, class InputIterator2,
          class BinaryPredicate>
  bool equal(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, BinaryPredicate pred);

template<class InputIterator1, class InputIterator2>
  bool equal(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, InputIterator2 last2);

template<class InputIterator1, class InputIterator2,
           class BinaryPredicate>
  bool equal(InputIterator1 first1, InputIterator1 last1,
             InputIterator2 first2, InputIterator2 last2,
             BinaryPredicate pred);
```

*Remarks:* If `last2` was not given in the argument list, it denotes
`first2 + (last1 - first1)` below.

*Returns:* If `last1 - first1 != last2 - first2`, return `false`.
Otherwise return `true` if for every iterator `i` in the range
\[`first1`, `last1`) the following corresponding conditions hold:
`*i == *(first2 + (i - first1)), pred(*i, *(first2 + (i - first1))) != false`.
Otherwise, returns `false`.

*Complexity:* No applications of the corresponding predicate if
`InputIterator1` and `InputIterator2` meet the requirements of random
access iterators and `last1 - first1 != last2 - first2`. Otherwise, at
most `min(last1 - first1, last2 - first2)` applications of the
corresponding predicate.

### Is permutation <a id="alg.is_permutation">[[alg.is_permutation]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                      ForwardIterator2 first2);
template<class ForwardIterator1, class ForwardIterator2,
                 class BinaryPredicate>
  bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                      ForwardIterator2 first2, BinaryPredicate pred);
template<class ForwardIterator1, class ForwardIterator2>
  bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                      ForwardIterator2 first2, ForwardIterator2 last2);
template<class ForwardIterator1, class ForwardIterator2,
                 class BinaryPredicate>
  bool is_permutation(ForwardIterator1 first1, ForwardIterator1 last1,
                      ForwardIterator2 first2, ForwardIterator2 last2,
                      BinaryPredicate pred);
```

*Requires:* `ForwardIterator1` and `ForwardIterator2` shall have the
same value type. The comparison function shall be an equivalence
relation.

*Remarks:* If `last2` was not given in the argument list, it denotes
`first2 + (last1 - first1)` below.

*Returns:* If `last1 - first1 != last2 - first2`, return `false`.
Otherwise return `true` if there exists a permutation of the elements in
the range \[`first2`, `first2 + (last1 - first1)`), beginning with
`ForwardIterator2 begin`, such that `equal(first1, last1, begin)`
returns `true` or `equal(first1, last1, begin, pred)` returns `true`;
otherwise, returns `false`.

*Complexity:* No applications of the corresponding predicate if
`ForwardIterator1` and `ForwardIterator2` meet the requirements of
random access iterators and `last1 - first1 != last2 - first2`.
Otherwise, exactly `distance(first1, last1)` applications of the
corresponding predicate if `equal(first1, last1, first2, last2)` would
return `true` if `pred` was not given in the argument list or
`equal(first1, last1, first2, last2, pred)` would return `true` if pred
was given in the argument list; otherwise, at worst 𝑂(N^2), where N has
the value `distance(first1, last1)`.

### Search <a id="alg.search">[[alg.search]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  ForwardIterator1
    search(ForwardIterator1 first1, ForwardIterator1 last1,
           ForwardIterator2 first2, ForwardIterator2 last2);

template<class ForwardIterator1, class ForwardIterator2,
         class BinaryPredicate>
  ForwardIterator1
    search(ForwardIterator1 first1, ForwardIterator1 last1,
           ForwardIterator2 first2, ForwardIterator2 last2,
           BinaryPredicate pred);
```

*Effects:* Finds a subsequence of equal values in a sequence.

*Returns:* The first iterator `i` in the range \[`first1`,
`last1 - (last2-first2)`) such that for every non-negative integer `n`
less than `last2 - first2` the following corresponding conditions hold:
`*(i + n) == *(first2 + n), pred(*(i + n), *(first2 + n)) != false`.
Returns `first1` if \[`first2`, `last2`) is empty, otherwise returns
`last1` if no such iterator is found.

*Complexity:* At most `(last1 - first1) * (last2 - first2)` applications
of the corresponding predicate.

``` cpp
template<class ForwardIterator, class Size, class T>
  ForwardIterator
    search_n(ForwardIterator first, ForwardIterator last, Size count,
           const T& value);

template<class ForwardIterator, class Size, class T,
         class BinaryPredicate>
  ForwardIterator
    search_n(ForwardIterator first, ForwardIterator last, Size count,
           const T& value, BinaryPredicate pred);
```

*Requires:* The type `Size` shall be convertible to integral
type ([[conv.integral]], [[class.conv]]).

*Effects:* Finds a subsequence of equal values in a sequence.

*Returns:* The first iterator `i` in the range \[`first`, `last-count`)
such that for every non-negative integer `n` less than `count` the
following corresponding conditions hold:
`*(i + n) == value, pred(*(i + n),value) != false`. Returns `last` if no
such iterator is found.

*Complexity:* At most `last - first` applications of the corresponding
predicate.

## Mutating sequence operations <a id="alg.modifying.operations">[[alg.modifying.operations]]</a>

### Copy <a id="alg.copy">[[alg.copy]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  OutputIterator copy(InputIterator first, InputIterator last,
                      OutputIterator result);
```

*Effects:* Copies elements in the range \[`first`, `last`) into the
range \[`result`, `result + (last - first)`) starting from `first` and
proceeding to `last`. For each non-negative integer
`n < (last - first)`, performs `*(result + n) = *(first + n)`.

*Returns:* `result + (last - first)`.

*Requires:* `result` shall not be in the range \[`first`, `last`).

*Complexity:* Exactly `last - first` assignments.

``` cpp
template<class InputIterator, class Size, class OutputIterator>
  OutputIterator copy_n(InputIterator first, Size n,
                        OutputIterator result);
```

*Effects:* For each non-negative integer i < n, performs
`*(result + i) = *(first + i)`.

*Returns:* `result + n`.

*Complexity:* Exactly `n` assignments.

``` cpp
template<class InputIterator, class OutputIterator, class Predicate>
  OutputIterator copy_if(InputIterator first, InputIterator last,
                         OutputIterator result, Predicate pred);
```

*Requires:* The ranges \[`first`, `last`) and \[`result`,
`result + (last - first)`) shall not overlap.

*Effects:* Copies all of the elements referred to by the iterator `i` in
the range \[`first`, `last`) for which `pred(*i)` is `true`.

*Returns:* The end of the resulting range.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate.

*Remarks:* Stable ([[algorithm.stable]]).

``` cpp
template<class BidirectionalIterator1, class BidirectionalIterator2>
  BidirectionalIterator2
    copy_backward(BidirectionalIterator1 first,
                  BidirectionalIterator1 last,
                  BidirectionalIterator2 result);
```

*Effects:* Copies elements in the range \[`first`, `last`) into the
range \[`result - (last-first)`, `result`) starting from `last - 1` and
proceeding to `first`.[^2] For each positive integer
`n <= (last - first)`, performs `*(result - n) = *(last - n)`.

*Requires:* `result` shall not be in the range (`first`, `last`).

*Returns:* `result - (last - first)`.

*Complexity:* Exactly `last - first` assignments.

### Move <a id="alg.move">[[alg.move]]</a>

``` cpp
template<class InputIterator, class OutputIterator>
  OutputIterator move(InputIterator first, InputIterator last,
                      OutputIterator result);
```

*Effects:* Moves elements in the range \[`first`, `last`) into the range
\[`result`, `result + (last - first)`) starting from first and
proceeding to last. For each non-negative integer `n < (last-first)`,
performs `*(result + n)` `= std::move(*(first + n))`.

*Returns:* `result + (last - first)`.

*Requires:* `result` shall not be in the range \[`first`, `last`).

*Complexity:* Exactly `last - first` move assignments.

``` cpp
template<class BidirectionalIterator1, class BidirectionalIterator2>
  BidirectionalIterator2
    move_backward(BidirectionalIterator1 first,
                  BidirectionalIterator1 last,
                  BidirectionalIterator2 result);
```

*Effects:* Moves elements in the range \[`first`, `last`) into the range
\[`result - (last-first)`, `result`) starting from `last - 1` and
proceeding to first.[^3] For each positive integer
`n <= (last - first)`, performs
`*(result - n) = std::move(*(last - n))`.

*Requires:* `result` shall not be in the range (`first`, `last`).

*Returns:* `result - (last - first)`.

*Complexity:* Exactly `last - first` assignments.

### swap <a id="alg.swap">[[alg.swap]]</a>

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  ForwardIterator2
    swap_ranges(ForwardIterator1 first1, ForwardIterator1 last1,
                ForwardIterator2 first2);
```

*Effects:* For each non-negative integer `n < (last1 - first1)`
performs: `swap(*(first1 + n), *(first2 + n))`.

*Requires:* The two ranges \[`first1`, `last1`) and \[`first2`,
`first2 + (last1 - first1)`) shall not overlap. `*(first1 + n)` shall be
swappable with ([[swappable.requirements]]) `*(first2 + n)`.

*Returns:* `first2 + (last1 - first1)`.

*Complexity:* Exactly `last1 - first1` swaps.

``` cpp
template<class ForwardIterator1, class ForwardIterator2>
  void iter_swap(ForwardIterator1 a, ForwardIterator2 b);
```

*Effects:* `swap(*a, *b)`.

*Requires:* `a` and `b` shall be dereferenceable. `*a` shall be
swappable with ([[swappable.requirements]]) `*b`.

### Transform <a id="alg.transform">[[alg.transform]]</a>

``` cpp
template<class InputIterator, class OutputIterator,
         class UnaryOperation>
  OutputIterator
    transform(InputIterator first, InputIterator last,
              OutputIterator result, UnaryOperation op);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class BinaryOperation>
  OutputIterator
    transform(InputIterator1 first1, InputIterator1 last1,
              InputIterator2 first2, OutputIterator result,
              BinaryOperation binary_op);
```

*Effects:* Assigns through every iterator `i` in the range \[`result`,
`result + (last1 - first1)`) a new corresponding value equal to
`op(*(first1 + (i - result))` or
`binary_op(*(first1 + (i - result)), *(first2 + (i - result)))`.

*Requires:* `op` and `binary_op` shall not invalidate iterators or
subranges, or modify elements in the ranges \[`first1`, `last1`\],
\[`first2`, `first2 + (last1 - first1)`\], and \[`result`,
`result + (last1 - first1)`\].[^4]

*Returns:* `result + (last1 - first1)`.

*Complexity:* Exactly `last1 - first1` applications of `op` or
`binary_op`.

*Remarks:* `result` may be equal to `first` in case of unary transform,
or to `first1` or `first2` in case of binary transform.

### Replace <a id="alg.replace">[[alg.replace]]</a>

``` cpp
template<class ForwardIterator, class T>
  void replace(ForwardIterator first, ForwardIterator last,
               const T& old_value, const T& new_value);

template<class ForwardIterator, class Predicate, class T>
  void replace_if(ForwardIterator first, ForwardIterator last,
                  Predicate pred, const T& new_value);
```

*Requires:* The expression `*first = new_value` shall be valid.

*Effects:* Substitutes elements referred by the iterator `i` in the
range \[`first`, `last`) with `new_value`, when the following
corresponding conditions hold: `*i == old_value`, `pred(*i) != false`.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate.

``` cpp
template<class InputIterator, class OutputIterator, class T>
  OutputIterator
    replace_copy(InputIterator first, InputIterator last,
                 OutputIterator result,
                 const T& old_value, const T& new_value);

template<class InputIterator, class OutputIterator, class Predicate, class T>
  OutputIterator
    replace_copy_if(InputIterator first, InputIterator last,
                    OutputIterator result,
                    Predicate pred, const T& new_value);
```

*Requires:* The results of the expressions `*first` and `new_value`
shall be writable to the `result` output iterator. The ranges \[`first`,
`last`) and \[`result`, `result + (last - first)`) shall not overlap.

*Effects:* Assigns to every iterator `i` in the range \[`result`,
`result + (last - first)`) either `new_value` or
`*(first + (i - result))` depending on whether the following
corresponding conditions hold:

``` cpp
*(first + (i - result)) == old_value
pred(*(first + (i - result))) != false
```

*Returns:* `result + (last - first)`.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate.

### Fill <a id="alg.fill">[[alg.fill]]</a>

``` cpp
template<class ForwardIterator, class T>
  void fill(ForwardIterator first, ForwardIterator last, const T& value);

template<class OutputIterator, class Size, class T>
  OutputIterator fill_n(OutputIterator first, Size n, const T& value);
```

*Requires:* The expression `value` shall be writable to the output
iterator. The type `Size` shall be convertible to an integral
type ([[conv.integral]], [[class.conv]]).

*Effects:* The first algorithm assigns `value` through all the iterators
in the range \[`first`, `last`). The second algorithm assigns `value`
through all the iterators in the range \[`first`, `first + n`) if `n` is
positive, otherwise it does nothing.

*Returns:* `fill_n` returns `first + n` for non-negative values of `n`
and `first` for negative values.

*Complexity:* Exactly `last - first`, `n`, or 0 assignments,
respectively.

### Generate <a id="alg.generate">[[alg.generate]]</a>

``` cpp
template<class ForwardIterator, class Generator>
  void generate(ForwardIterator first, ForwardIterator last,
                Generator gen);

template<class OutputIterator, class Size, class Generator>
  OutputIterator generate_n(OutputIterator first, Size n, Generator gen);
```

*Effects:* The first algorithm invokes the function object `gen` and
assigns the return value of `gen` through all the iterators in the range
\[`first`, `last`). The second algorithm invokes the function object
`gen` and assigns the return value of `gen` through all the iterators in
the range \[`first`, `first + n`) if `n` is positive, otherwise it does
nothing.

*Requires:* `gen` takes no arguments, `Size` shall be convertible to an
integral type ([[conv.integral]], [[class.conv]]).

*Returns:* `generate_n` returns `first + n` for non-negative values of
`n` and `first` for negative values.

*Complexity:* Exactly `last - first`, `n`, or 0 invocations of `gen` and
assignments, respectively.

### Remove <a id="alg.remove">[[alg.remove]]</a>

``` cpp
template<class ForwardIterator, class T>
  ForwardIterator remove(ForwardIterator first, ForwardIterator last,
                         const T& value);

template<class ForwardIterator, class Predicate>
  ForwardIterator remove_if(ForwardIterator first, ForwardIterator last,
                            Predicate pred);
```

*Requires:* The type of `*first` shall satisfy the `MoveAssignable`
requirements (Table  [[moveassignable]]).

*Effects:* Eliminates all the elements referred to by iterator `i` in
the range \[`first`, `last`) for which the following corresponding
conditions hold: `*i == value, pred(*i) != false`.

*Returns:* The end of the resulting range.

*Remarks:* Stable ([[algorithm.stable]]).

*Complexity:* Exactly `last - first` applications of the corresponding
predicate.

*Note:* each element in the range \[`ret`, `last`), where `ret` is the
returned value, has a valid but unspecified state, because the
algorithms can eliminate elements by moving from elements that were
originally in that range.

``` cpp
template<class InputIterator, class OutputIterator, class T>
  OutputIterator
    remove_copy(InputIterator first, InputIterator last,
                OutputIterator result, const T& value);

template<class InputIterator, class OutputIterator, class Predicate>
  OutputIterator
    remove_copy_if(InputIterator first, InputIterator last,
                   OutputIterator result, Predicate pred);
```

*Requires:* The ranges \[`first`, `last`) and \[`result`,
`result + (last - first)`) shall not overlap. The expression
`*result = *first` shall be valid.

*Effects:* Copies all the elements referred to by the iterator `i` in
the range \[`first`, `last`) for which the following corresponding
conditions do not hold: `*i == value, pred(*i) != false`.

*Returns:* The end of the resulting range.

*Complexity:* Exactly `last - first` applications of the corresponding
predicate.

*Remarks:* Stable ([[algorithm.stable]]).

### Unique <a id="alg.unique">[[alg.unique]]</a>

``` cpp
template<class ForwardIterator>
  ForwardIterator unique(ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class BinaryPredicate>
  ForwardIterator unique(ForwardIterator first, ForwardIterator last,
                         BinaryPredicate pred);
```

*Effects:* For a nonempty range, eliminates all but the first element
from every consecutive group of equivalent elements referred to by the
iterator `i` in the range \[`first + 1`, `last`) for which the following
conditions hold: `*(i - 1) == *i` or `pred(*(i - 1), *i) != false`.

*Requires:* The comparison function shall be an equivalence relation.
The type of `*first` shall satisfy the `MoveAssignable` requirements
(Table  [[moveassignable]]).

*Returns:* The end of the resulting range.

*Complexity:* For nonempty ranges, exactly `(last - first) - 1`
applications of the corresponding predicate.

``` cpp
template<class InputIterator, class OutputIterator>
  OutputIterator
    unique_copy(InputIterator first, InputIterator last,
                OutputIterator result);

template<class InputIterator, class OutputIterator,
         class BinaryPredicate>
  OutputIterator
    unique_copy(InputIterator first, InputIterator last,
                OutputIterator result, BinaryPredicate pred);
```

*Requires:* The comparison function shall be an equivalence relation.
The ranges \[`first`, `last`) and \[`result`, `result+(last-first)`)
shall not overlap. The expression `*result = *first` shall be valid. If
neither `InputIterator` nor `OutputIterator` meets the requirements of
forward iterator then the value type of `InputIterator` shall be
`CopyConstructible` (Table  [[copyconstructible]]) and `CopyAssignable`
(Table  [[copyassignable]]). Otherwise `CopyConstructible` is not
required.

*Effects:* Copies only the first element from every consecutive group of
equal elements referred to by the iterator `i` in the range \[`first`,
`last`) for which the following corresponding conditions hold:
`*i == *(i - 1)` or `pred(*i, *(i - 1)) != false`.

*Returns:* The end of the resulting range.

*Complexity:* For nonempty ranges, exactly `last - first - 1`
applications of the corresponding predicate.

### Reverse <a id="alg.reverse">[[alg.reverse]]</a>

``` cpp
template<class BidirectionalIterator>
  void reverse(BidirectionalIterator first, BidirectionalIterator last);
```

*Effects:* For each non-negative integer `i < (last - first)/2`, applies
`iter_swap` to all pairs of iterators `first + i, (last - i) - 1`.

*Requires:* `*first` shall be swappable ([[swappable.requirements]]).

*Complexity:* Exactly `(last - first)/2` swaps.

``` cpp
template<class BidirectionalIterator, class OutputIterator>
  OutputIterator
    reverse_copy(BidirectionalIterator first,
                 BidirectionalIterator last, OutputIterator result);
```

*Effects:* Copies the range \[`first`, `last`) to the range \[`result`,
`result+(last-first)`) such that for every non-negative integer
`i < (last - first)` the following assignment takes place:
`*(result + (last - first) - 1 - i) = *(first + i)`.

*Requires:* The ranges \[`first`, `last`) and \[`result`,
`result+(last-first)`) shall not overlap.

*Returns:* `result + (last - first)`.

*Complexity:* Exactly `last - first` assignments.

### Rotate <a id="alg.rotate">[[alg.rotate]]</a>

``` cpp
template<class ForwardIterator>
  ForwardIterator rotate(ForwardIterator first, ForwardIterator middle,
              ForwardIterator last);
```

*Effects:* For each non-negative integer `i < (last - first)`, places
the element from the position `first + i` into position
`first + (i + (last - middle)) % (last - first)`.

*Returns:* `first + (last - middle)`.

*Remarks:* This is a left rotate.

*Requires:* \[`first`, `middle`) and \[`middle`, `last`) shall be valid
ranges. `ForwardIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and the requirements of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* At most `last - first` swaps.

``` cpp
template<class ForwardIterator, class OutputIterator>
  OutputIterator
    rotate_copy(ForwardIterator first, ForwardIterator middle,
                ForwardIterator last, OutputIterator result);
```

*Effects:* Copies the range \[`first`, `last`) to the range \[`result`,
`result + (last - first)`) such that for each non-negative integer
`i < (last - first)` the following assignment takes place:
`*(result + i) = *(first + (i + (middle - first)) % (last - first))`.

*Returns:* `result + (last - first)`.

*Requires:* The ranges \[`first`, `last`) and \[`result`,
`result + (last - first)`) shall not overlap.

*Complexity:* Exactly `last - first` assignments.

### Shuffle <a id="alg.random.shuffle">[[alg.random.shuffle]]</a>

``` cpp
template<class RandomAccessIterator, class UniformRandomNumberGenerator>
  void shuffle(RandomAccessIterator first,
                      RandomAccessIterator last,
                      UniformRandomNumberGenerator&& g);
```

*Effects:* Permutes the elements in the range \[`first`, `last`) such
that each possible permutation of those elements has equal probability
of appearance.

*Requires:* `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type
`UniformRandomNumberGenerator` shall meet the requirements of a uniform
random number generator ([[rand.req.urng]]) type whose return type is
convertible to `iterator_traits<RandomAccessIterator>::difference_type`.

*Complexity:* Exactly `(last - first) - 1` swaps.

*Remarks:* To the extent that the implementation of this function makes
use of random numbers, the object `g` shall serve as the
implementation’s source of randomness.

### Partitions <a id="alg.partitions">[[alg.partitions]]</a>

``` cpp
template <class InputIterator, class Predicate>
  bool is_partitioned(InputIterator first, InputIterator last, Predicate pred);
```

*Requires:* `InputIterator`’s value type shall be convertible to
`Predicate`’s argument type.

*Returns:* `true` if \[`first`, `last`) is empty or if \[`first`,
`last`) is partitioned by `pred`, i.e. if all elements that satisfy
`pred` appear before those that do not.

*Complexity:* Linear. At most `last - first` applications of `pred`.

``` cpp
template<class ForwardIterator, class Predicate>
  ForwardIterator
    partition(ForwardIterator first,
              ForwardIterator last, Predicate pred);
```

*Effects:* Places all the elements in the range \[`first`, `last`) that
satisfy `pred` before all the elements that do not satisfy it.

*Returns:* An iterator `i` such that for every iterator `j` in the range
\[`first`, `i`) `pred(*j) != false`, and for every iterator `k` in the
range \[`i`, `last`), `pred(*k) == false`.

*Requires:* `ForwardIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]).

*Complexity:* If ForwardIterator meets the requirements for a
BidirectionalIterator, at most `(last - first) / 2` swaps are done;
otherwise at most `last - first` swaps are done. Exactly `last - first`
applications of the predicate are done.

``` cpp
template<class BidirectionalIterator, class Predicate>
  BidirectionalIterator
    stable_partition(BidirectionalIterator first,
                     BidirectionalIterator last, Predicate pred);
```

*Effects:* Places all the elements in the range \[`first`, `last`) that
satisfy `pred` before all the elements that do not satisfy it.

*Returns:* An iterator `i` such that for every iterator `j` in the range
\[`first`, `i`), `pred(*j) != false`, and for every iterator `k` in the
range \[`i`, `last`), `pred(*k) == false`. The relative order of the
elements in both groups is preserved.

*Requires:* `BidirectionalIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* At most `(last - first) * log(last - first)` swaps, but
only linear number of swaps if there is enough extra memory. Exactly
`last - first` applications of the predicate.

``` cpp
template <class InputIterator, class OutputIterator1,
          class OutputIterator2, class Predicate>
  pair<OutputIterator1, OutputIterator2>
  partition_copy(InputIterator first, InputIterator last,
                 OutputIterator1 out_true, OutputIterator2 out_false,
                 Predicate pred);
```

*Requires:* `InputIterator`’s value type shall be `CopyAssignable`, and
shall be writable to the `out_true` and `out_false` `OutputIterator`s,
and shall be convertible to `Predicate`’s argument type. The input range
shall not overlap with either of the output ranges.

*Effects:* For each iterator `i` in \[`first`, `last`), copies `*i` to
the output range beginning with `out_true` if `pred(*i)` is `true`, or
to the output range beginning with `out_false` otherwise.

*Returns:* A pair `p` such that `p.first` is the end of the output range
beginning at `out_true` and `p.second` is the end of the output range
beginning at `out_false`.

*Complexity:* Exactly `last - first` applications of `pred`.

``` cpp
template<class ForwardIterator, class Predicate>
  ForwardIterator partition_point(ForwardIterator first,
                                  ForwardIterator last,
                                  Predicate pred);
```

*Requires:* `ForwardIterator`’s value type shall be convertible to
`Predicate`’s argument type. \[`first`, `last`) shall be partitioned by
`pred`, i.e. all elements that satisfy `pred` shall appear before those
that do not.

*Returns:* An iterator `mid` such that `all_of(first, mid, pred)` and
`none_of(mid, last, pred)` are both true.

*Complexity:* 𝑂(log(last - first)) applications of `pred`.

## Sorting and related operations <a id="alg.sorting">[[alg.sorting]]</a>

All the operations in  [[alg.sorting]] have two versions: one that takes
a function object of type `Compare` and one that uses an `operator<`.

`Compare`

is a function object type ([[function.objects]]). The return value of
the function call operation applied to an object of type `Compare`, when
contextually converted to `bool` (Clause  [[conv]]), yields `true` if
the first argument of the call is less than the second, and `false`
otherwise. `Compare comp` is used throughout for algorithms assuming an
ordering relation. It is assumed that `comp` will not apply any
non-constant function through the dereferenced iterator.

For all algorithms that take `Compare`, there is a version that uses
`operator<` instead. That is, `comp(*i, *j) != false` defaults to
`*i < *j != false`. For algorithms other than those described in 
[[alg.binary.search]] to work correctly, `comp` has to induce a strict
weak ordering on the values.

The term *strict* refers to the requirement of an irreflexive relation
(`!comp(x, x)` for all `x`), and the term *weak* to requirements that
are not as strong as those for a total ordering, but stronger than those
for a partial ordering. If we define `equiv(a, b)` as
`!comp(a, b) && !comp(b, a)`, then the requirements are that `comp` and
`equiv` both be transitive relations:

- `comp(a, b) && comp(b, c)` implies `comp(a, c)`
- `equiv(a, b) && equiv(b, c)`
  implies `equiv(a, c)` Under these conditions, it can be shown that
  - `equiv` is an equivalence relation
  - `comp` induces a well-defined relation on the equivalence classes
    determined by `equiv`
  - The induced relation is a strict total ordering.

A sequence is *sorted with respect to a comparator* `comp` if for every
iterator `i` pointing to the sequence and every non-negative integer `n`
such that `i + n` is a valid iterator pointing to an element of the
sequence, `comp(*(i + n), *i) == false`.

A sequence \[`start`, `finish`) is *partitioned with respect to an
expression* `f(e)` if there exists an integer `n` such that for all
`0 <= i < distance(start, finish)`, `f(*(start + i))` is true if and
only if `i < n`.

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
  void sort(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void sort(RandomAccessIterator first, RandomAccessIterator last,
            Compare comp);
```

*Effects:* Sorts the elements in the range \[`first`, `last`).

*Requires:* `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* 𝑂(Nlog(N)) (where N` == last - first`) comparisons.

#### `stable_sort` <a id="stable.sort">[[stable.sort]]</a>

``` cpp
template<class RandomAccessIterator>
  void stable_sort(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void stable_sort(RandomAccessIterator first, RandomAccessIterator last,
                   Compare comp);
```

*Effects:* Sorts the elements in the range \[`first`, `last`).

*Requires:* `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* It does at most N log²(N) (where N` == last - first`)
comparisons; if enough extra memory is available, it is N log(N).

*Remarks:* Stable ([[algorithm.stable]]).

#### `partial_sort` <a id="partial.sort">[[partial.sort]]</a>

``` cpp
template<class RandomAccessIterator>
  void partial_sort(RandomAccessIterator first,
                    RandomAccessIterator middle,
                    RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void partial_sort(RandomAccessIterator first,
                    RandomAccessIterator middle,
                    RandomAccessIterator last,
                    Compare comp);
```

*Effects:* Places the first `middle - first` sorted elements from the
range \[`first`, `last`) into the range \[`first`, `middle`). The rest
of the elements in the range \[`middle`, `last`) are placed in an
unspecified order.

*Requires:* `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* It takes approximately
`(last - first) * log(middle - first)` comparisons.

#### `partial_sort_copy` <a id="partial.sort.copy">[[partial.sort.copy]]</a>

``` cpp
template<class InputIterator, class RandomAccessIterator>
  RandomAccessIterator
    partial_sort_copy(InputIterator first, InputIterator last,
                      RandomAccessIterator result_first,
                      RandomAccessIterator result_last);

template<class InputIterator, class RandomAccessIterator,
         class Compare>
  RandomAccessIterator
    partial_sort_copy(InputIterator first, InputIterator last,
                      RandomAccessIterator result_first,
                      RandomAccessIterator result_last,
                      Compare comp);
```

*Effects:* Places the first
`min(last - first, result_last - result_first)` sorted elements into the
range \[`result_first`,
`result_first + min(last - first, result_last - result_first)`).

*Returns:* The smaller of: `result_last` or
`result_first + (last - first)`.

*Requires:* `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of
`*result_first` shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* Approximately
`(last - first) * log(min(last - first, result_last - result_first))`
comparisons.

#### `is_sorted` <a id="is.sorted">[[is.sorted]]</a>

``` cpp
template<class ForwardIterator>
  bool is_sorted(ForwardIterator first, ForwardIterator last);
```

*Returns:* `is_sorted_until(first, last) == last`

``` cpp
template<class ForwardIterator, class Compare>
  bool is_sorted(ForwardIterator first, ForwardIterator last,
    Compare comp);
```

*Returns:* `is_sorted_until(first, last, comp) == last`

``` cpp
template<class ForwardIterator>
  ForwardIterator is_sorted_until(ForwardIterator first, ForwardIterator last);
template<class ForwardIterator, class Compare>
  ForwardIterator is_sorted_until(ForwardIterator first, ForwardIterator last,
    Compare comp);
```

*Returns:* If `distance(first, last) < 2`, returns `last`. Otherwise,
returns the last iterator `i` in \[`first`, `last`\] for which the range
\[`first`, `i`) is sorted.

*Complexity:* Linear.

### Nth element <a id="alg.nth.element">[[alg.nth.element]]</a>

``` cpp
template<class RandomAccessIterator>
  void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                   RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void nth_element(RandomAccessIterator first, RandomAccessIterator nth,
                   RandomAccessIterator last,  Compare comp);
```

After `nth_element` the element in the position pointed to by `nth` is
the element that would be in that position if the whole range were
sorted, unless `nth == last`. Also for every iterator `i` in the range
\[`first`, `nth`) and every iterator `j` in the range \[`nth`, `last`)
it holds that: `!(*j < *i)` or `comp(*j, *i) == false`.

*Requires:* `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* Linear on average.

### Binary search <a id="alg.binary.search">[[alg.binary.search]]</a>

All of the algorithms in this section are versions of binary search and
assume that the sequence being searched is partitioned with respect to
an expression formed by binding the search key to an argument of the
implied or explicit comparison function. They work on non-random access
iterators minimizing the number of comparisons, which will be
logarithmic for all types of iterators. They are especially appropriate
for random access iterators, because these algorithms do a logarithmic
number of steps through the data structure. For non-random access
iterators they execute a linear number of steps.

#### `lower_bound` <a id="lower.bound">[[lower.bound]]</a>

``` cpp
template<class ForwardIterator, class T>
  ForwardIterator
    lower_bound(ForwardIterator first, ForwardIterator last,
                const T& value);

template<class ForwardIterator, class T, class Compare>
  ForwardIterator
    lower_bound(ForwardIterator first, ForwardIterator last,
                const T& value, Compare comp);
```

*Requires:* The elements `e` of \[`first`, `last`) shall be partitioned
with respect to the expression `e < value` or `comp(e, value)`.

*Returns:* The furthermost iterator `i` in the range \[`first`, `last`\]
such that for every iterator `j` in the range \[`first`, `i`) the
following corresponding conditions hold: `*j < value` or
`comp(*j, value) != false`.

*Complexity:* At most log₂(`last - first`) + 𝑂(1) comparisons.

#### `upper_bound` <a id="upper.bound">[[upper.bound]]</a>

``` cpp
template<class ForwardIterator, class T>
  ForwardIterator
    upper_bound(ForwardIterator first, ForwardIterator last,
                const T& value);

template<class ForwardIterator, class T, class Compare>
  ForwardIterator
    upper_bound(ForwardIterator first, ForwardIterator last,
                const T& value, Compare comp);
```

*Requires:* The elements `e` of \[`first`, `last`) shall be partitioned
with respect to the expression `!(value < e)` or `!comp(value, e)`.

*Returns:* The furthermost iterator `i` in the range \[`first`, `last`\]
such that for every iterator `j` in the range \[`first`, `i`) the
following corresponding conditions hold: `!(value < *j)` or
`comp(value, *j) == false`.

*Complexity:* At most log₂(`last - first`) + 𝑂(1) comparisons.

#### `equal_range` <a id="equal.range">[[equal.range]]</a>

``` cpp
template<class ForwardIterator, class T>
  pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first,
                ForwardIterator last, const T& value);

template<class ForwardIterator, class T, class Compare>
  pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first,
                ForwardIterator last, const T& value,
                Compare comp);
```

*Requires:* The elements `e` of \[`first`, `last`) shall be partitioned
with respect to the expressions `e < value` and `!(value < e)` or
`comp(e, value)` and `!comp(value, e)`. Also, for all elements `e` of
`[first, last)`, `e < value` shall imply `!(value < e)` or
`comp(e, value)` shall imply `!comp(value, e)`.

*Returns:*

``` cpp
make_pair(lower_bound(first, last, value),
          upper_bound(first, last, value))
```

or

``` cpp
make_pair(lower_bound(first, last, value, comp),
          upper_bound(first, last, value, comp))
```

*Complexity:* At most 2 * log₂(`last - first`) + 𝑂(1) comparisons.

#### `binary_search` <a id="binary.search">[[binary.search]]</a>

``` cpp
template<class ForwardIterator, class T>
  bool binary_search(ForwardIterator first, ForwardIterator last,
                     const T& value);

template<class ForwardIterator, class T, class Compare>
  bool binary_search(ForwardIterator first, ForwardIterator last,
                     const T& value, Compare comp);
```

*Requires:* The elements `e` of \[`first`, `last`) are partitioned with
respect to the expressions `e < value` and `!(value < e)` or
`comp(e, value)` and `!comp(value, e)`. Also, for all elements `e` of
`[first, last)`, `e < value` implies `!(value < e)` or `comp(e, value)`
implies `!comp(value, e)`.

*Returns:* `true` if there is an iterator `i` in the range \[`first`,
`last`) that satisfies the corresponding conditions:
`!(*i < value) && !(value < *i)` or
`comp(*i, value) == false && comp(value, *i) == false`.

*Complexity:* At most log₂(`last - first`) + 𝑂(1) comparisons.

### Merge <a id="alg.merge">[[alg.merge]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  OutputIterator
    merge(InputIterator1 first1, InputIterator1 last1,
          InputIterator2 first2, InputIterator2 last2,
          OutputIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  OutputIterator
    merge(InputIterator1 first1, InputIterator1 last1,
          InputIterator2 first2, InputIterator2 last2,
          OutputIterator result, Compare comp);
```

*Effects:*  Copies all the elements of the two ranges \[`first1`,
`last1`) and \[`first2`, `last2`) into the range \[`result`,
`result_last`), where `result_last` is
`result + (last1 - first1) + (last2 - first2)`, such that the resulting
range satisfies `is_sorted(result, result_last)` or
`is_sorted(result, result_last, comp)`, respectively.

*Requires:* The ranges \[`first1`, `last1`) and \[`first2`, `last2`)
shall be sorted with respect to `operator<` or `comp`. The resulting
range shall not overlap with either of the original ranges.

*Returns:* `result + (last1 - first1) + (last2 - first2)`.

*Complexity:* At most `(last1 - first1) + (last2 - first2) - 1`
comparisons.

*Remarks:* Stable ([[algorithm.stable]]).

``` cpp
template<class BidirectionalIterator>
  void inplace_merge(BidirectionalIterator first,
                     BidirectionalIterator middle,
                     BidirectionalIterator last);

template<class BidirectionalIterator, class Compare>
  void inplace_merge(BidirectionalIterator first,
                     BidirectionalIterator middle,
                     BidirectionalIterator last, Compare comp);
```

*Effects:* Merges two sorted consecutive ranges \[`first`, `middle`) and
\[`middle`, `last`), putting the result of the merge into the range
\[`first`, `last`). The resulting range will be in non-decreasing order;
that is, for every iterator `i` in \[`first`, `last`) other than
`first`, the condition `*i < *(i - 1)` or, respectively,
`comp(*i, *(i - 1))` will be false.

*Requires:* The ranges \[`first`, `middle`) and \[`middle`, `last`)
shall be sorted with respect to `operator<` or `comp`.
`BidirectionalIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* When enough additional memory is available,
`(last - first) - 1` comparisons. If no additional memory is available,
an algorithm with complexity N log(N) (where `N` is equal to
`last - first`) may be used.

*Remarks:* Stable ([[algorithm.stable]]).

### Set operations on sorted structures <a id="alg.set.operations">[[alg.set.operations]]</a>

This section defines all the basic set operations on sorted structures.
They also work with `multiset`s ([[multiset]]) containing multiple
copies of equivalent elements. The semantics of the set operations are
generalized to `multiset`s in a standard way by defining `set_union()`
to contain the maximum number of occurrences of every element,
`set_intersection()` to contain the minimum, and so on.

#### `includes` <a id="includes">[[includes]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  bool includes(InputIterator1 first1, InputIterator1 last1,
                InputIterator2 first2, InputIterator2 last2);

template<class InputIterator1, class InputIterator2, class Compare>
  bool includes(InputIterator1 first1, InputIterator1 last1,
                InputIterator2 first2, InputIterator2 last2,
                Compare comp);
```

*Returns:* `true` if \[`first2`, `last2`) is empty or if every element
in the range \[`first2`, `last2`) is contained in the range \[`first1`,
`last1`). Returns `false` otherwise.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons.

#### `set_union` <a id="set.union">[[set.union]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  OutputIterator
    set_union(InputIterator1 first1, InputIterator1 last1,
              InputIterator2 first2, InputIterator2 last2,
              OutputIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  OutputIterator
    set_union(InputIterator1 first1, InputIterator1 last1,
              InputIterator2 first2, InputIterator2 last2,
              OutputIterator result, Compare comp);
```

*Effects:* Constructs a sorted union of the elements from the two
ranges; that is, the set of elements that are present in one or both of
the ranges.

*Requires:* The resulting range shall not overlap with either of the
original ranges.

*Returns:* The end of the constructed range.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons.

*Remarks:* If \[`first1`, `last1`) contains m elements that are
equivalent to each other and \[`first2`, `last2`) contains n elements
that are equivalent to them, then all m elements from the first range
shall be copied to the output range, in order, and then max(n - m, 0)
elements from the second range shall be copied to the output range, in
order.

#### `set_intersection` <a id="set.intersection">[[set.intersection]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  OutputIterator
    set_intersection(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2, InputIterator2 last2,
                     OutputIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  OutputIterator
    set_intersection(InputIterator1 first1, InputIterator1 last1,
                     InputIterator2 first2, InputIterator2 last2,
                     OutputIterator result, Compare comp);
```

*Effects:* Constructs a sorted intersection of the elements from the two
ranges; that is, the set of elements that are present in both of the
ranges.

*Requires:* The resulting range shall not overlap with either of the
original ranges.

*Returns:* The end of the constructed range.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons.

*Remarks:* If \[`first1`, `last1`) contains m elements that are
equivalent to each other and \[`first2`, `last2`) contains n elements
that are equivalent to them, the first min(m, n) elements shall be
copied from the first range to the output range, in order.

#### `set_difference` <a id="set.difference">[[set.difference]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  OutputIterator
    set_difference(InputIterator1 first1, InputIterator1 last1,
                   InputIterator2 first2, InputIterator2 last2,
                   OutputIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  OutputIterator
    set_difference(InputIterator1 first1, InputIterator1 last1,
                   InputIterator2 first2, InputIterator2 last2,
                   OutputIterator result, Compare comp);
```

*Effects:* Copies the elements of the range \[`first1`, `last1`) which
are not present in the range \[`first2`, `last2`) to the range beginning
at `result`. The elements in the constructed range are sorted.

*Requires:* The resulting range shall not overlap with either of the
original ranges.

*Returns:* The end of the constructed range.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons.

*Remarks:* If \[`first1`, `last1`) contains m elements that are
equivalent to each other and \[`first2`, `last2`) contains n elements
that are equivalent to them, the last max(m - n, 0) elements from
\[`first1`, `last1`) shall be copied to the output range.

#### `set_symmetric_difference` <a id="set.symmetric.difference">[[set.symmetric.difference]]</a>

``` cpp
template<class InputIterator1, class InputIterator2,
         class OutputIterator>
  OutputIterator
    set_symmetric_difference(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, InputIterator2 last2,
                             OutputIterator result);

template<class InputIterator1, class InputIterator2,
         class OutputIterator, class Compare>
  OutputIterator
    set_symmetric_difference(InputIterator1 first1, InputIterator1 last1,
                             InputIterator2 first2, InputIterator2 last2,
                             OutputIterator result, Compare comp);
```

*Effects:* Copies the elements of the range \[`first1`, `last1`) that
are not present in the range \[`first2`, `last2`), and the elements of
the range \[`first2`, `last2`) that are not present in the range
\[`first1`, `last1`) to the range beginning at `result`. The elements in
the constructed range are sorted.

*Requires:* The resulting range shall not overlap with either of the
original ranges.

*Returns:* The end of the constructed range.

*Complexity:* At most `2 * ((last1 - first1) + (last2 - first2)) - 1`
comparisons.

*Remarks:* If \[`first1`, `last1`) contains m elements that are
equivalent to each other and \[`first2`, `last2`) contains n elements
that are equivalent to them, then |m - n| of those elements shall be
copied to the output range: the last m - n of these elements from
\[`first1`, `last1`) if m > n, and the last n - m of these elements from
\[`first2`, `last2`) if m < n.

### Heap operations <a id="alg.heap.operations">[[alg.heap.operations]]</a>

A *heap* is a particular organization of elements in a range between two
random access iterators \[`a`, `b`). Its two key properties are:

- **(1)} There is no element greater than
\texttt{\*a}
in the range and**

- **`(2)} \texttt{*a}
may be removed by
\texttt{pop_heap()},
or a new element added by
\texttt{push_heap()},
in
$\mathcal{O}(\log(N))$
time.`**

These properties make heaps useful as priority queues.

`make_heap()`

converts a range into a heap and `sort_heap()` turns a heap into a
sorted sequence.

#### `push_heap` <a id="push.heap">[[push.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  void push_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void push_heap(RandomAccessIterator first, RandomAccessIterator last,
                 Compare comp);
```

*Effects:* Places the value in the location `last - 1` into the
resulting heap \[`first`, `last`).

*Requires:* The range \[`first`, `last - 1`) shall be a valid heap. The
type of `*first` shall satisfy the `MoveConstructible` requirements
(Table  [[moveconstructible]]) and the `MoveAssignable` requirements
(Table  [[moveassignable]]).

*Complexity:* At most `log(last - first)` comparisons.

#### `pop_heap` <a id="pop.heap">[[pop.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  void pop_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void pop_heap(RandomAccessIterator first, RandomAccessIterator last,
                Compare comp);
```

*Requires:* The range \[`first`, `last`) shall be a valid non-empty
heap. `RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Effects:* Swaps the value in the location `first` with the value in the
location `last - 1` and makes \[`first`, `last - 1`) into a heap.

*Complexity:* At most `2 * log(last - first)` comparisons.

#### `make_heap` <a id="make.heap">[[make.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  void make_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void make_heap(RandomAccessIterator first, RandomAccessIterator last,
                 Compare comp);
```

*Effects:* Constructs a heap out of the range \[`first`, `last`).

*Requires:* The type of `*first` shall satisfy the `MoveConstructible`
requirements (Table  [[moveconstructible]]) and the `MoveAssignable`
requirements (Table  [[moveassignable]]).

*Complexity:* At most `3 * (last - first)` comparisons.

#### `sort_heap` <a id="sort.heap">[[sort.heap]]</a>

``` cpp
template<class RandomAccessIterator>
  void sort_heap(RandomAccessIterator first, RandomAccessIterator last);

template<class RandomAccessIterator, class Compare>
  void sort_heap(RandomAccessIterator first, RandomAccessIterator last,
                 Compare comp);
```

*Effects:* Sorts elements in the heap \[`first`, `last`).

*Requires:* The range \[`first`, `last`) shall be a valid heap.
`RandomAccessIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]). The type of `*first`
shall satisfy the requirements of `MoveConstructible`
(Table  [[moveconstructible]]) and of `MoveAssignable`
(Table  [[moveassignable]]).

*Complexity:* At most N log(N) comparisons (where `N == last - first`).

#### `is_heap` <a id="is.heap">[[is.heap]]</a>

``` cpp
template<class RandomAccessIterator>
    bool is_heap(RandomAccessIterator first, RandomAccessIterator last);
```

*Returns:* `is_heap_until(first, last) == last`

``` cpp
template<class RandomAccessIterator, class Compare>
    bool is_heap(RandomAccessIterator first, RandomAccessIterator last, Compare comp);
```

*Returns:* `is_heap_until(first, last, comp) == last`

``` cpp
template<class RandomAccessIterator>
    RandomAccessIterator is_heap_until(RandomAccessIterator first, RandomAccessIterator last);
  template<class RandomAccessIterator, class Compare>
    RandomAccessIterator is_heap_until(RandomAccessIterator first, RandomAccessIterator last,
      Compare comp);
```

*Returns:* If `distance(first, last) < 2`, returns `last`. Otherwise,
returns the last iterator `i` in \[`first`, `last`\] for which the range
\[`first`, `i`) is a heap.

*Complexity:* Linear.

### Minimum and maximum <a id="alg.min.max">[[alg.min.max]]</a>

``` cpp
template<class T> constexpr const T& min(const T& a, const T& b);
template<class T, class Compare>
  constexpr const T& min(const T& a, const T& b, Compare comp);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[lessthancomparable]]).

*Returns:* The smaller value.

*Remarks:* Returns the first argument when the arguments are equivalent.

``` cpp
template<class T>
  constexpr T min(initializer_list<T> t);
template<class T, class Compare>
  constexpr T min(initializer_list<T> t, Compare comp);
```

*Requires:* `T` is `LessThanComparable` and `CopyConstructible` and
`t.size() > 0`.

*Returns:* The smallest value in the initializer_list.

*Remarks:* Returns a copy of the leftmost argument when several
arguments are equivalent to the smallest. 

``` cpp
template<class T> constexpr const T& max(const T& a, const T& b);
template<class T, class Compare>
  constexpr const T& max(const T& a, const T& b, Compare comp);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[lessthancomparable]]).

*Returns:* The larger value.

*Remarks:* Returns the first argument when the arguments are equivalent.

``` cpp
template<class T>
  constexpr T max(initializer_list<T> t);
template<class T, class Compare>
  constexpr T max(initializer_list<T> t, Compare comp);
```

*Requires:* `T` is `LessThanComparable` and `CopyConstructible` and
`t.size() > 0`.

*Returns:* The largest value in the initializer_list.

*Remarks:* Returns a copy of the leftmost argument when several
arguments are equivalent to the largest.

``` cpp
template<class T> constexpr pair<const T&, const T&> minmax(const T& a, const T& b);
template<class T, class Compare>
  constexpr pair<const T&, const T&> minmax(const T& a, const T& b, Compare comp);
```

*Requires:* Type `T` shall be `LessThanComparable`
(Table  [[lessthancomparable]]).

*Returns:* `pair<const T&, const T&>(b, a)` if `b` is smaller than `a`,
and `pair<const T&, const T&>(a, b)` otherwise.

*Remarks:* Returns `pair<const T&, const T&>(a, b)` when the arguments
are equivalent.

*Complexity:* Exactly one comparison.

``` cpp
template<class T>
  constexpr pair<T, T> minmax(initializer_list<T> t);
template<class T, class Compare>
  constexpr pair<T, T> minmax(initializer_list<T> t, Compare comp);
```

*Requires:* `T` is `LessThanComparable` and `CopyConstructible` and
`t.size() > 0`.

*Returns:* `pair<T, T>(x, y)`, where `x` has the smallest and `y` has
the largest value in the initializer list.

*Remarks:* `x` is a copy of the leftmost argument when several arguments
are equivalent to the smallest. `y` is a copy of the rightmost argument
when several arguments are equivalent to the largest.

*Complexity:* At most `(3/2) * t.size()` applications of the
corresponding predicate.

``` cpp
template<class ForwardIterator>
  ForwardIterator min_element(ForwardIterator first, ForwardIterator last);

template<class ForwardIterator, class Compare>
  ForwardIterator min_element(ForwardIterator first, ForwardIterator last,
                            Compare comp);
```

*Returns:* The first iterator `i` in the range \[`first`, `last`) such
that for every iterator `j` in the range \[`first`, `last`) the
following corresponding conditions hold: `!(*j < *i)` or
`comp(*j, *i) == false`. Returns `last` if `first == last`.

*Complexity:* Exactly `max((last - first) - 1, 0)` applications of the
corresponding comparisons.

``` cpp
template<class ForwardIterator>
  ForwardIterator max_element(ForwardIterator first, ForwardIterator last);
template<class ForwardIterator, class Compare>
  ForwardIterator max_element(ForwardIterator first, ForwardIterator last,
                            Compare comp);
```

*Returns:* The first iterator `i` in the range \[`first`, `last`) such
that for every iterator `j` in the range \[`first`, `last`) the
following corresponding conditions hold: `!(*i < *j)` or
`comp(*i, *j) == false`. Returns `last` if `first == last`.

*Complexity:* Exactly `max((last - first) - 1, 0)` applications of the
corresponding comparisons.

``` cpp
template<class ForwardIterator>
  pair<ForwardIterator, ForwardIterator>
    minmax_element(ForwardIterator first, ForwardIterator last);
template<class ForwardIterator, class Compare>
  pair<ForwardIterator, ForwardIterator>
    minmax_element(ForwardIterator first, ForwardIterator last, Compare comp);
```

*Returns:* `make_pair(first, first)` if \[`first`, `last`) is empty,
otherwise `make_pair(m, M)`, where `m` is the first iterator in
\[`first`, `last`) such that no iterator in the range refers to a
smaller element, and where `M` is the last iterator in \[`first`,
`last`) such that no iterator in the range refers to a larger element.

*Complexity:* At most $max(\lfloor{\frac{3}{2}} (N-1)\rfloor, 0)$
applications of the corresponding predicate, where N is
`distance(first, last)`.

### Lexicographical comparison <a id="alg.lex.comparison">[[alg.lex.comparison]]</a>

``` cpp
template<class InputIterator1, class InputIterator2>
  bool
    lexicographical_compare(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, InputIterator2 last2);

template<class InputIterator1, class InputIterator2, class Compare>
  bool
    lexicographical_compare(InputIterator1 first1, InputIterator1 last1,
                            InputIterator2 first2, InputIterator2 last2,
                            Compare comp);
```

*Returns:* `true` if the sequence of elements defined by the range
\[`first1`, `last1`) is lexicographically less than the sequence of
elements defined by the range \[`first2`, `last2`) and `false`
otherwise.

*Complexity:* At most `2*min((last1 - first1), (last2 - first2))`
applications of the corresponding comparison.

*Remarks:* If two sequences have the same number of elements and their
corresponding elements are equivalent, then neither sequence is
lexicographically less than the other. If one sequence is a prefix of
the other, then the shorter sequence is lexicographically less than the
longer sequence. Otherwise, the lexicographical comparison of the
sequences yields the same result as the comparison of the first
corresponding pair of elements that are not equivalent.

``` cpp
for ( ; first1 != last1 && first2 != last2 ; ++first1, ++first2) {
  if (*first1 < *first2) return true;
  if (*first2 < *first1) return false;
}
return first1 == last1 && first2 != last2;
```

*Remarks:*  An empty sequence is lexicographically less than any
non-empty sequence, but not less than any empty sequence.

### Permutation generators <a id="alg.permutation.generators">[[alg.permutation.generators]]</a>

``` cpp
template<class BidirectionalIterator>
  bool next_permutation(BidirectionalIterator first,
                        BidirectionalIterator last);

template<class BidirectionalIterator, class Compare>
  bool next_permutation(BidirectionalIterator first,
                        BidirectionalIterator last, Compare comp);
```

*Effects:* Takes a sequence defined by the range \[`first`, `last`) and
transforms it into the next permutation. The next permutation is found
by assuming that the set of all permutations is lexicographically sorted
with respect to `operator<` or `comp`. If such a permutation exists, it
returns `true`. Otherwise, it transforms the sequence into the smallest
permutation, that is, the ascendingly sorted one, and returns `false`.

*Requires:* `BidirectionalIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]).

*Complexity:* At most `(last - first)/2` swaps.

``` cpp
template<class BidirectionalIterator>
  bool prev_permutation(BidirectionalIterator first,
                        BidirectionalIterator last);

template<class BidirectionalIterator, class Compare>
  bool prev_permutation(BidirectionalIterator first,
                        BidirectionalIterator last, Compare comp);
```

*Effects:* Takes a sequence defined by the range \[`first`, `last`) and
transforms it into the previous permutation. The previous permutation is
found by assuming that the set of all permutations is lexicographically
sorted with respect to `operator<` or `comp`.

*Returns:* `true` if such a permutation exists. Otherwise, it transforms
the sequence into the largest permutation, that is, the descendingly
sorted one, and returns `false`.

*Requires:* `BidirectionalIterator` shall satisfy the requirements of
`ValueSwappable` ([[swappable.requirements]]).

*Complexity:* At most `(last - first)/2` swaps.

## C library algorithms <a id="alg.c.library">[[alg.c.library]]</a>

Table  [[tab:algorithms.hdr.cstdlib]] describes some of the contents of
the header `<cstdlib>`.

The contents are the same as the Standard C library header `<stdlib.h>`
with the following exceptions:

The function signature:

``` cpp
bsearch(const void *, const void *, size_t, size_t,
  int (*)(const void *, const void *));
```

is replaced by the two declarations:

``` cpp
extern "C" void* bsearch(const void* key, const void* base,
                         size_t nmemb, size_t size,
                         int (*compar)(const void*, const void*));
extern "C++" void* bsearch(const void* key, const void* base,
                           size_t nmemb, size_t size,
                           int (*compar)(const void*, const void*));
```

both of which have the same behavior as the original declaration.

The function signature:

``` cpp
qsort(void *, size_t, size_t,
  int (*)(const void *, const void *));
```

is replaced by the two declarations:

``` cpp
extern "C" void qsort(void* base, size_t nmemb, size_t size,
                      int (*compar)(const void*, const void*));
extern "C++" void qsort(void* base, size_t nmemb, size_t size,
                        int (*compar)(const void*, const void*));
```

both of which have the same behavior as the original declaration. The
behavior is undefined unless the objects in the array pointed to by
`base` are of trivial type.

Because the function argument `compar()` may throw an exception,
`bsearch()` and `qsort()` are allowed to propagate the exception (
[[res.on.exception.handling]]).

ISO C 7.10.5.

<!-- Link reference definitions -->
[alg.adjacent.find]: #alg.adjacent.find
[alg.all_of]: #alg.all_of
[alg.any_of]: #alg.any_of
[alg.binary.search]: #alg.binary.search
[alg.c.library]: #alg.c.library
[alg.copy]: #alg.copy
[alg.count]: #alg.count
[alg.equal]: #alg.equal
[alg.fill]: #alg.fill
[alg.find]: #alg.find
[alg.find.end]: #alg.find.end
[alg.find.first.of]: #alg.find.first.of
[alg.foreach]: #alg.foreach
[alg.generate]: #alg.generate
[alg.heap.operations]: #alg.heap.operations
[alg.is_permutation]: #alg.is_permutation
[alg.lex.comparison]: #alg.lex.comparison
[alg.merge]: #alg.merge
[alg.min.max]: #alg.min.max
[alg.modifying.operations]: #alg.modifying.operations
[alg.move]: #alg.move
[alg.none_of]: #alg.none_of
[alg.nonmodifying]: #alg.nonmodifying
[alg.nth.element]: #alg.nth.element
[alg.partitions]: #alg.partitions
[alg.permutation.generators]: #alg.permutation.generators
[alg.random.shuffle]: #alg.random.shuffle
[alg.remove]: #alg.remove
[alg.replace]: #alg.replace
[alg.reverse]: #alg.reverse
[alg.rotate]: #alg.rotate
[alg.search]: #alg.search
[alg.set.operations]: #alg.set.operations
[alg.sort]: #alg.sort
[alg.sorting]: #alg.sorting
[alg.swap]: #alg.swap
[alg.transform]: #alg.transform
[alg.unique]: #alg.unique
[algorithm.stable]: library.md#algorithm.stable
[algorithms]: #algorithms
[algorithms.general]: #algorithms.general
[bidirectional.iterators]: iterators.md#bidirectional.iterators
[binary.search]: #binary.search
[class.conv]: special.md#class.conv
[containers]: containers.md#containers
[conv]: conv.md#conv
[conv.integral]: conv.md#conv.integral
[copyassignable]: #copyassignable
[copyconstructible]: #copyconstructible
[equal.range]: #equal.range
[forward.iterators]: iterators.md#forward.iterators
[function.objects]: utilities.md#function.objects
[includes]: #includes
[input.iterators]: iterators.md#input.iterators
[is.heap]: #is.heap
[is.sorted]: #is.sorted
[iterator.requirements]: iterators.md#iterator.requirements
[lessthancomparable]: #lessthancomparable
[lower.bound]: #lower.bound
[make.heap]: #make.heap
[mismatch]: #mismatch
[moveassignable]: #moveassignable
[moveconstructible]: #moveconstructible
[multiset]: containers.md#multiset
[output.iterators]: iterators.md#output.iterators
[partial.sort]: #partial.sort
[partial.sort.copy]: #partial.sort.copy
[pop.heap]: #pop.heap
[push.heap]: #push.heap
[rand.req.urng]: numerics.md#rand.req.urng
[random.access.iterators]: iterators.md#random.access.iterators
[refwrap]: utilities.md#refwrap
[res.on.exception.handling]: library.md#res.on.exception.handling
[set.difference]: #set.difference
[set.intersection]: #set.intersection
[set.symmetric.difference]: #set.symmetric.difference
[set.union]: #set.union
[sort]: #sort
[sort.heap]: #sort.heap
[stable.sort]: #stable.sort
[swappable.requirements]: library.md#swappable.requirements
[tab:algorithms.hdr.cstdlib]: #tab:algorithms.hdr.cstdlib
[tab:algorithms.summary]: #tab:algorithms.summary
[upper.bound]: #upper.bound

[^1]: The decision whether to include a copying version was usually
    based on complexity considerations. When the cost of doing the
    operation dominates the cost of copy, the copying version is not
    included. For example, `sort_copy` is not included because the cost
    of sorting is much more significant, and users might as well do
    `copy` followed by `sort`.

[^2]: `copy_backward` should be used instead of copy when `last` is in
    the range \[`result - (last - first)`, `result`).

[^3]: `move_backward` should be used instead of move when last is in the
    range \[`result - (last - first)`, `result`).

[^4]: The use of fully closed ranges is intentional.
