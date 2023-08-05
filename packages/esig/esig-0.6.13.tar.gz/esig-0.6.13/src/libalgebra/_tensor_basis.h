/* *************************************************************

Copyright 2010 Terry Lyons, Stephen Buckley, Djalil Chafai, 
Greg Gyurkó and Arend Janssen. 

Distributed under the terms of the GNU General Public License, 
Version 3. (See accompanying file License.txt)

************************************************************* */



#pragma once
#include "implimentation_types.h"
#include "constlog2.h"

/// Base class for tensor_basis
template <unsigned No_Letters, unsigned DEPTH>
class
_tensor_basis
{

private:

	/// A private constructor from doubles
	_tensor_basis(const double base)
		: _word(base)
	{
	}

	/// A double that contains a word
	double _word;

	///The number of Bits in a letter
	static const unsigned uBitsInLetter = ConstLog2 < No_Letters -
		1 > ::ans + 1;
	static const unsigned uMaxSizeAlphabet = (1 << uBitsInLetter);
	static const unsigned uMaxWordLength = 52 / uBitsInLetter;


public:

	///Letter
	typedef alg::LET LET;

	///Constructor

	///Checks that the DEPTH does not exceed the Maximum word length.
	_tensor_basis(void)
		: _word(1.)
	{
		assert(DEPTH <= uMaxWordLength);
	}

	///Destructor
	~_tensor_basis(void)
	{
	}

	/// Concatenates two words
	inline _tensor_basis& push_back(const _tensor_basis& rhs)
	{
		assert(size() + rhs.size() <= uMaxWordLength);
		int iExponent;
		frexp(rhs._word, &iExponent);
		double dPowerOfTwo = ldexp(.5, iExponent);
		_word = (_word - 1) * dPowerOfTwo + rhs._word;
		return *this;
	}

	/// Concatenates two words
	inline _tensor_basis operator* (const _tensor_basis& rhs) const
	{
		int iExponent;
		frexp(rhs._word, &iExponent);
		double dPowerOfTwo = ldexp(.5, iExponent);
		return (_word * dPowerOfTwo + rhs._word) - dPowerOfTwo;
	}


	/// Compares two words
	inline bool operator < (const _tensor_basis & rhs) const
	{
		assert(size() <= DEPTH  || size() == end().size());
		return _word < rhs._word;
	}

	_tensor_basis(const LET uLetter)
		: _word (uMaxSizeAlphabet + (uLetter - 1)%uMaxSizeAlphabet)
	{
		assert(0 < uLetter && uLetter <= No_Letters);
	}

	/// gives the number of letters in _word
	inline unsigned size () const
	{
		int iExponent;
		frexp(_word, &iExponent);
		assert((iExponent - 1) % uBitsInLetter == 0);
		return (iExponent - 1) / uBitsInLetter;
	}

	/// Returns the first letter of a _tensor_basis as a letter.
	inline LET FirstLetter() const
	{
		static const double dShiftPlus1(uMaxSizeAlphabet * 2);
		static const double dShift(uMaxSizeAlphabet);
		//static const double dMinusShift = 1 / dShift;

		assert(size() > 0);
		int iExponent;
		double dMantissa = frexp(_word, &iExponent);
		double ans;
		modf(dMantissa * dShiftPlus1, &ans);
		return LET(ans - dShift) + 1;
	}

	/// Checks validity of a finite instance of _tensor_basis
	bool valid() const
	{
		if (DEPTH > uMaxWordLength) abort();
		if (this->_word == _tensor_basis()._word)
			return true;
		else
			return size() <= DEPTH && (FirstLetter() - 1 < No_Letters) &&
				rparent().valid();
	}


	//TJL 21/08/2012
	friend class _LET;
	struct _LET {
		_tensor_basis& m_parent;
		size_t m_index;
		_LET(const size_t index, _tensor_basis& parent)
			:m_parent(parent), m_index(index)
		{
		}

		operator LET()
		{
			double dBottom, dMiddle, dTop;
			int iExponent;
			double dTemp, dMantissa;
			dMantissa = frexp(m_parent._word, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent - (m_index + 1) *
				uBitsInLetter));
			dMiddle = modf(dTemp, &dTop);
			dTemp = dMiddle + 1.;
			dMantissa = frexp(dTemp, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent + uBitsInLetter));
			dBottom = modf(dTemp, &dMiddle);
			_tensor_basis middle(dMiddle);
			return  middle.FirstLetter(); //adds a one implicitly
		}

		bool operator <(DEG arg) const
		{
			return operator LET() < arg;
		}

		_LET& operator +=(const size_t i)
		{
			double dBottom, dMiddle, dTop;
			int iExponent;
			double dTemp, dMantissa;
			dMantissa = frexp(m_parent._word, &iExponent);
			dTemp = ldexp(dMantissa, int(
				iExponent - (m_index+1) *
								uBitsInLetter)
				);
			dMiddle = modf(dTemp, &dTop);
			dTemp = 1. + dMiddle;
			dMantissa = frexp(dTemp, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent + 1 * uBitsInLetter));
			dBottom = modf(dTemp, &dMiddle);
			dTemp = 1. + dBottom;
			dMantissa = frexp(dTemp, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent + m_index * uBitsInLetter));
			modf(dTemp, &dBottom);
			_tensor_basis top(dTop), middle(dMiddle), bottom(dBottom),
				ans_tb;
			_tensor_basis newmiddle(LET(middle.FirstLetter() + i));
			ans_tb =(top * newmiddle * bottom);
			m_parent = ans_tb;
			return *this;
		}

		_LET& operator =(LET i)
		{
			double dBottom, dMiddle, dTop;

			int iExponent;
			double dTemp, dMantissa;
			dMantissa = frexp(m_parent._word, &iExponent);
			dTemp = ldexp(dMantissa, int(
				iExponent - (m_index + 1) *
								uBitsInLetter)
				);
			dMiddle = modf(dTemp, &dTop);
			dTemp = 1. + dMiddle;
			dMantissa = frexp(dTemp, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent + uBitsInLetter));
			dBottom= modf(dTemp, &dMiddle);
			dTemp = 1. + dBottom;
			dMantissa = frexp(dTemp, &iExponent);
			dBottom = ldexp(dMantissa, int(iExponent + m_index * uBitsInLetter));

			_tensor_basis top(dTop), middle(dMiddle), bottom(dBottom);
			_tensor_basis newmiddle(i);
			m_parent._word = (top*newmiddle*bottom)._word;
			return *this;
		}

		bool tt() const
		{
			double dBottom, dMiddle, dTop;
			int iExponent;
			double dTemp, dMantissa;
			dMantissa = frexp(m_parent._word, &iExponent);
			dTemp = ldexp(dMantissa, int(
				iExponent - (m_index+1) *
								uBitsInLetter)
				);
			dMiddle = modf(dTemp, &dTop);
			dTemp = 1. + dMiddle;
			dMantissa = frexp(dTemp, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent + 1 * uBitsInLetter));
			dBottom = modf(dTemp, &dMiddle);
			dTemp = 1. + dBottom;
			dMantissa = frexp(dTemp, &iExponent);
			dTemp = ldexp(dMantissa, int(iExponent + m_index * uBitsInLetter));
			modf(dTemp, &dBottom);
			_tensor_basis top(dTop), middle(dMiddle), bottom(dBottom),
				ans_tb;
			ans_tb = (top*middle*bottom);
			return m_parent._word == ans_tb._word;

			/*
			//push_back
			frexp(rhs._word, &iExponent);
			double dPowerOfTwo = ldexp(.5, iExponent);
			_word = (_word - 1) * dPowerOfTwo + rhs._word;
			*/
		}
	};

	//TJL 21/08/2012
	/// Treats the basis word as an array and returns a "letter" starting at the highest end of the used part of _word.
	inline _LET operator[](const size_t arg)
	{
		assert(arg < size());
		size_t rarg = size() -1 - arg;
		return _LET(rarg, *this);
	}

	inline LET operator[](const size_t arg) const
	{
		assert(arg < size());
		size_t rarg = size() -1 - arg;
		_tensor_basis temp(*this);
		return _LET(rarg, temp);
	}

	/// Returns the first letter of a _tensor_basis in a _tensor_basis.
	inline _tensor_basis lparent() const
	{
		static const double dShiftPlus1(uMaxSizeAlphabet * 2);
		//static const double dShift(uMaxSizeAlphabet);
		//static const double dMinusShift = 1 / dShift;

		assert(size() > 0);
		int iExponent;
		double dMantissa = frexp(_word, &iExponent);
		double ans;
		modf(dMantissa * dShiftPlus1, &ans);
		return ans;
	}

	/// Returns the _tensor_basis which corresponds to the sub-word after the first letter.
	inline _tensor_basis rparent() const
	{
		static const double dShiftPlus1(uMaxSizeAlphabet * 2);
		//static const double dShift(uMaxSizeAlphabet);
		//static const double dMinusShift = 1 / dShift;

		assert(size() > 0);
		int iExponent;
		double dMantissa = frexp(_word, &iExponent);
		double ans;
		double dPowerOfTwo = ldexp(.5, int(iExponent - uBitsInLetter));
		return (modf(dMantissa * dShiftPlus1, &ans) + 1.) * dPowerOfTwo;
	}

	static _tensor_basis end()
	{
		return std::numeric_limits<double>::infinity();
	}

	friend std::ostream & operator << (std::ostream & os, const _tensor_basis < No_Letters, DEPTH > & word)
	{
		int iExponent;
		unsigned count = word.size();
		double dNormalised = frexp(word._word, &iExponent) * 2. - 1.;
		os << "(";
		while (count > 0) {
			double letter;
			dNormalised = modf(dNormalised * uMaxSizeAlphabet, &letter);
			os << letter + 1.;
			--count;
			if (count != 0)
				os << ",";
		}
		return os << ")";
	}
};

