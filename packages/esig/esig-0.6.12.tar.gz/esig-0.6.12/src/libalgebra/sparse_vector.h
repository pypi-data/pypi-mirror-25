/* *************************************************************

Copyright 2010 Terry Lyons, Stephen Buckley, Djalil Chafai, 
Greg Gyurkó and Arend Janssen. 

Distributed under the terms of the GNU General Public License, 
Version 3. (See accompanying file License.txt)

************************************************************* */




//  sparse_vector.h


// Include once wrapper
#ifndef DJC_COROPA_LIBALGEBRA_SPARSEVECTORH_SEEN
#define DJC_COROPA_LIBALGEBRA_SPARSEVECTORH_SEEN

/// A class to store and manipulate sparse vectors.
/**
An instance of the sparse_vector class is just a MAP between KEY and
SCALAR, with vector space operators. It is a vector of basis elements
of type KEY, stored in a MAP class, associated to coefficients given by
SCALAR instances. Each basis element refers to the static instance of type
BASIS.

The MAP class must comes with a std::map<KEY, SCALAR> interface.
The scalar type SCALAR correponds to MAP::mapped_type.
By default, the MAP class is taken from the BASIS via the BASIS::MAP 
type, cf. forward declaration of the sparse_vector class in libalgebra.h.

The SCALAR type must comes with operators making it an associative 
algebra (non necessarily commutative) containing the integers (via a 
suitable constructor). Thus, operators *,+,- must be implemented.

There is a compatibility condition between the BASIS and MAP classes
since the MAP::key_type type and the BASIS::KEY must be the same.
*/
template<class BASIS, class MAP>
class sparse_vector :
	/*private*/ MAP
	{
public:
		/// Import of Const_Iterator to beginning of the sparse vector
		using MAP::begin;
		/// Import of Const_Iterator to end of the sparse vector
		using MAP::end;
		/// Import of find a KEY in the sparse vector
		using MAP::find;
		/// Import of erase a KEY from the sparse vector
		using MAP::erase;
		/// Import of set a KEY with a given SCALAR 
		using MAP::operator [];
		/// Import of set this instance to the zero instance
		using MAP::clear;
		/// Import empty()
		using MAP::empty;
		/// Import size()
		using MAP::size;
	
		/// Swap the vector instance controlled by *this with the one in the RHS
	void swap (sparse_vector & rhs) {
			MAP::swap(rhs);
		}
		/// Import of the rational type from the BASIS class.
		typedef typename BASIS::RATIONAL RATIONAL;
		/// Import of the KEY type from the MAP class.
		typedef typename MAP::key_type KEY;
		/// Import of the SCALAR type from the MAP class.
		typedef typename MAP::mapped_type SCALAR;
		/// Import of the iterator type from the MAP type.
		typedef typename MAP::iterator iterator;
		/// Import of the KEY constant iterator type from the MAP type.
		typedef typename MAP::const_iterator const_iterator;
public:
		/// The zero scalar value.
		const static SCALAR zero; //0
		/// The +1 scalar value.
		const static SCALAR one;  //+1
		/// The -1 scalar value.
		const static SCALAR mone; //-1
	
		/// The static basis. 
		/// Can be dynamically updated by some internal mechanism.
		static BASIS basis;

public:
		/// Default constructor.
		/**
		* Create an instance of an empty vector.
		* Such a vector is a neutral element for operator+= and operator-=.
		*/
	sparse_vector(void) {}
		/// Copy constructor. 
	sparse_vector(const sparse_vector& v) : MAP(v) {}
		/// Unidimensional constructor.
		/**
		* Constructs a sparse_vector correponding the unique basis
		* element k with coefficient s (+1 by default).
		*/
	explicit sparse_vector(const KEY& k, const SCALAR& s = one)
		{
			if (s != zero)
				(*this)[k] = s;
		}
public:
		/// Returns an instance of the additive inverse of the instance.
	inline sparse_vector operator-(void) const
		{	
			if (empty())
				return *this;
			const_iterator in;
			sparse_vector result;
			for (in = begin(); in != end(); ++in)
				result[in->first] = -(in->second);
			return result;
		}
		/// Multiplies the instance with scalar s.
	inline sparse_vector& operator*=(const SCALAR& s)
		{
			if (s != zero)
			{
				iterator it;
				if (!empty())
					for (it = begin(); it != end(); ++it)
						it->second *= s;
			}
			else
				clear();
			return *this;
		}
		/// Binary version of operator*=()
	inline __DECLARE_BINARY_OPERATOR(sparse_vector,*,*=,SCALAR)
		/// Divides the instance by scalar s.
	inline sparse_vector& operator/=(const RATIONAL& s)
		{
			iterator it;
			if (!empty())
				for (it = begin(); it != end(); ++it)
				{
					RATIONAL temp(1);
					it->second *= (temp / s);
				}
			return *this;
		}
		/// Binary instance of  operator/=()
	inline __DECLARE_BINARY_OPERATOR(sparse_vector,/,/=,RATIONAL)
		/// Adds a sparse_vector to the instance.
	inline sparse_vector& operator+=(const sparse_vector& rhs)
		{
			iterator it;
			const_iterator cit;
			if (rhs.empty())
				return *this;
			if (empty())
				return *this = rhs;
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{ // Instead of a bare (*this)[cit->first] += cit->second;
				it = find(cit->first);
				if (it == end())
					(*this)[cit->first] = cit->second;
				else if ((it->second += cit->second) == zero)
					erase(it->first);
			}	
			return *this;
		}
		/// Binary version of  operator+=()
	inline __DECLARE_BINARY_OPERATOR(sparse_vector,+,+=,sparse_vector)
		/// Substracts a sparse_vector to the instance.
	inline sparse_vector& operator-=(const sparse_vector& rhs)
		{
			iterator it;
			const_iterator cit;
			if (rhs.empty())
				return *this;
			if (empty())
				return *this = -rhs;
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{ // Instead of a bare (*this)[cit->first] -= cit->second;
				it = find(cit->first);
				if (it == end())
					(*this)[cit->first] = -(cit->second);
				else if ((it->second -= cit->second) == zero)
					erase(it->first);
			}	
			return *this;
		}
		/// Binary version of  operator-=()
	inline __DECLARE_BINARY_OPERATOR(sparse_vector,-,-=,sparse_vector)

		/// A fast version of operator+=(rhs.scal_prod(s))
	inline sparse_vector& add_scal_prod(const sparse_vector& rhs,
		const SCALAR& s)
		{
			iterator it;
			const_iterator cit;
			if ((s == zero) || rhs.empty())
				return *this;
			if (empty())
			{
				*this = rhs;
				return operator *= (s);
			}
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{ // Instead of a bare (*this)[cit->first] += cit->second * s;
				it = find(cit->first);
				if (it == end())
					(*this)[cit->first] = cit->second * s;
				else if ((it->second += cit->second * s) == zero)
					erase(it->first);
			}	
			return *this;
		}
		/// A fast version of operator-=(rhs.scal_prod(s))
	inline sparse_vector& sub_scal_prod(const sparse_vector& rhs,
		const SCALAR& s)
		{
			iterator it;
			const_iterator cit;
			if ((s == zero) || rhs.empty())
				return *this;
			if (empty())
			{
				*this = rhs;
				return operator *= (-s);
			}
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{ // Instead of a bare (*this)[cit->first] -= cit->second * s;
				it = find(cit->first);
				if (it == end())
					(*this)[cit->first] = cit->second * -s;
				else if ((it->second -= cit->second * s) == zero)
					erase(it->first);
			}	
			return *this;
		}
		/// A fast version of operator+=(rhs.scal_div(s))
	inline sparse_vector& add_scal_div(const sparse_vector& rhs,
		const RATIONAL& s)
		{
			iterator it;
			const_iterator cit;
			if (rhs.empty())
				return *this;
			if (empty())
			{
				*this = rhs;
				return operator /= (s);
			}
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{ // Instead of a bare (*this)[cit->first] += cit->second / s;
				it = find(cit->first);
				if (it == end())
					(*this)[cit->first] = cit->second / s;
				else if ((it->second += (cit->second / s)) == zero)
					erase(it->first);
			}	
			return *this;
		}
		/// A fast version of operator-=(rhs.scal_div(s))
	inline sparse_vector& sub_scal_div(const sparse_vector& rhs,
		const RATIONAL& s)
		{
			iterator it;
			const_iterator cit;
			if (rhs.empty())
				return *this;
			if (empty())
			{
				*this = rhs;
				return operator /= (-s);
			}
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{ // Instead of a bare (*this)[cit->first] -= cit->second / s;
				it = find(cit->first);
				if (it == end())
					(*this)[cit->first] = - cit->second / s;
				else if ((it->second -= (cit->second / s)) == zero)
					erase(it->first);
			}	
			return *this;
		}
		/// Compares the instance to a sparse_vector.
	bool operator==(const sparse_vector& rhs) const
		{
			if (size() != rhs.size())
				return false;
			const_iterator i, j;
			for (i = begin(); i != end(); ++i)
			{
				j = rhs.find(i->first);
				if ((j == rhs.end()) || (j->second != i->second))
					return false;
			}
			return true;
		}
		/// Lexicographically compares the instance to a sparse_vector.
	bool operator < (const sparse_vector& rhs) const
		{
			return std::lexicographical_compare(begin(), end(), rhs.begin(), rhs.end());
		}
		/// Boolean negation of operator==()
	bool operator!=(const sparse_vector& rhs) const
		{
			return !operator == (rhs);
		}
		/// Computes the l1 norm of sparse vector with respect to this basis
	inline SCALAR NormL1() const
		{
			const_iterator i;
			SCALAR ans(zero);
			for (i = begin(); i != end(); ++i)
			{
				ans += abs(i->second);
			}
			return ans;
		}
		/// Computes the l1 norm of degree d component of a sparse vector with respect to this basis
	inline SCALAR NormL1(const DEG & d) const
		{
			const_iterator i;
			SCALAR ans(zero);
			for (i = begin(); i != end(); ++i)
			{
				if (d == basis.degree(i->first))
					ans += abs(i->second);
			}
			return ans;
		}
		/// Outputs a sparse_vector to an std::ostream.
		/** 
		It is assumed that there is std::ostream support to
		output std::pair<BASIS*, KEY> and SCALAR types. 
		*/
	inline friend std::ostream& operator<<(std::ostream& os,
		const sparse_vector& rhs)
		{	
			const_iterator cit;			
			std::pair<BASIS*, KEY> token;
			token.first = &sparse_vector::basis;
			os << '{';
			for (cit = rhs.begin(); cit != rhs.end(); ++cit)
			{
				token.second = cit->first;
				os << ' ' << cit->second << '(' << token << ')';
			}
			os << " }";
			return os;
		}
	};

// Initialisation of static members of sparse_vector<>

/// Static initialisation of the sparse_vector basis.
template<class BASIS, class MAP>
BASIS sparse_vector<BASIS, MAP>::basis;

/// Static initialisation of the scalar constant +1.
template<class BASIS, class MAP>
const typename MAP::mapped_type sparse_vector<BASIS, MAP>::one(+1);

/// Static initialisation of the scalar constant 0.
template<class BASIS, class MAP>
const typename MAP::mapped_type sparse_vector<BASIS, MAP>::zero(0);

/// Static initialisation of the scalar constant -1.
template<class BASIS, class MAP>
const typename MAP::mapped_type sparse_vector<BASIS, MAP>::mone(-1);

// Include once wrapper
// DJC_COROPA_LIBALGEBRA_SPARSEVECTORH_SEEN
#endif
//EOF.


