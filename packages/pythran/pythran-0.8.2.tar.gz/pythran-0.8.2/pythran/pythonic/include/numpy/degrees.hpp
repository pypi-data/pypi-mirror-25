#ifndef PYTHONIC_INCLUDE_NUMPY_DEGREES_HPP
#define PYTHONIC_INCLUDE_NUMPY_DEGREES_HPP

#include "pythonic/include/utils/functor.hpp"
#include "pythonic/include/types/ndarray.hpp"
#include "pythonic/include/utils/numpy_traits.hpp"
#include <boost/simd/function/indeg.hpp>

namespace pythonic
{

  namespace numpy
  {
#define NUMPY_NARY_FUNC_NAME degrees
#define NUMPY_NARY_FUNC_SYM boost::simd::indeg
#include "pythonic/include/types/numpy_nary_expr.hpp"
  }
}

#endif
