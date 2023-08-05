/* *************************************************************

Copyright 2010 Terry Lyons, Stephen Buckley, Djalil Chafai, 
Greg Gyurkó and Arend Janssen. 

Distributed under the terms of the GNU General Public License, 
Version 3. (See accompanying file License.txt)

************************************************************* */




//  libalgebra.h 


// Include once wrapper
#ifndef DJC_COROPA_LIBALGEBRAH_SEEN
#define DJC_COROPA_LIBALGEBRAH_SEEN

#include <iostream>
#include <sstream>
#include <string>
#include <deque>
#include <vector>
#include <map>
#include <utility>
#include <algorithm>
#include <cmath>
#include "implimentation_types.h"
#include <stdlib.h>
#include <cassert>
#include <boost/thread/shared_mutex.hpp>
#include <boost/thread/recursive_mutex.hpp>
#include <boost/thread/locks.hpp>

/// The libalgebra namespace. A set of template classes for Algebras.
/**
   The SCA typename corresponds to a commutative ring with unit containing the
   rationals. Needed operators are * + - and explicit ctor from int type.

   The RAT typename corresponds to rationals built from SCA. Needed
   operators are + - * / and explicit ctor from SCA type and int type.
*/

namespace alg
{

// Some useful macros to avoid similar codes.

#define __DECLARE_BINARY_OPERATOR(T1, NEWOP, OLDOP, T2) \
	T1 operator NEWOP(const T2& rhs) const \
	{ T1 result(*this); return result OLDOP rhs; }

#define __DECLARE_UNARY_OPERATOR(NEWT, NEWOP, OLDOP, OLDT) \
	NEWT operator NEWOP(void) const \
	{ return OLDT::operator OLDOP (); }

//  End of macros.

/// Forward declaration of classes

/// Sparse vectors with default MAP typename from BASIS typename.
template<class BASIS, class MAP = typename BASIS::MAP>
class sparse_vector;
/// Generic Associative Algebra.
template<class BASIS>
class algebra;
/// Generic Associative Algebra basis.
template<typename SCA, DEG n_letters, DEG max_degree = 0>
class tensor_basis;
/// Free Associative Algegra Basis. Concatenation product. Non commutative.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class free_tensor_basis;
/// Free Shuffle Associative Algebra Basis. Shuffle product. Commutative.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class shuffle_tensor_basis;
/// Free Associative Algebra.  Associative and non commutative.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class free_tensor;
/// Free Associative Shuffle Algebra.  Associative and Commutative.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class shuffle_tensor;
/// Philip Hall Lie Basis.
class hall_basis;
/// Free Lie Associative Algebra Basis.  Associative and non commutative.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class lie_basis;
/// Free Lie Associative Algebra.  Associative and non commutative.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class lie;
/// Maps between Free Lie and Free Algebra elements.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree = 0>
class maps;
/// Campbell-Baker-Hausdorff formulas.
template<typename SCA, typename RAT,
		 DEG n_letters, DEG max_degree>
class cbh;
/// Multivariate Polynomial Algebra Basis. Associative and Commutative.
template<typename SCA, typename RAT>
class poly_basis;
/// Multivariate Polynomial Algebra.  Associative and Commutative.
template<typename SCA, typename RAT>
class poly;


/// II. Multivariate Polynomial Algebra pre Basis. Associative and Commutative
template<typename SCA, DEG n_letters, DEG max_degree = 0>
class monomial_basis;
/// II. Multivariate Polynomial Algebra Basis. Associative and Commutative
template<typename SCA, typename RAT, DEG n_letters, DEG max_degree = 0>
class free_monomial_basis;
/// II. Multivariate Polynomial Algebra   Associative and Commutative.
template<typename SCA, typename RAT, DEG n_letters, DEG max_degree = 0>
class multi_polynomial;


///III. Multivariate Polynomial Lie Algebra Basis. Associative and non commutative
template<typename SCA, typename RAT, DEG n_letters, DEG max_degree = 0>
class poly_lie_basis;

///III. Multivariate Polynomial Lie Algebra. Associative and non commutative
template<typename SCA, typename RAT, DEG n_letters, DEG max_degree = 0>
class poly_lie;

#include "sparse_vector.h"
#include "algebra.h"
#include "tensor_basis.h"
#include "tensor.h"
#include "lie_basis.h"
#include "lie.h"
#include "utils.h"
#include "poly_basis.h"
#include "polynomials.h"
#include "monomial_basis.h"
#include "multi_polynomial.h"
#include "poly_lie_basis.h"
#include "poly_lie.h"

// Undeclaring local macros in reverse order of declaration.
#undef __DECLARE_UNARY_OPERATOR
#undef __DECLARE_BINARY_OPERATOR
// End of undeclaration of local macros.

} // namespace alg


// Include once wrapper
#endif // DJC_COROPA_LIBALGEBRAH_SEEN

//EOF.
