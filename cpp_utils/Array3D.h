#ifndef _ARRAY3D_H_
#define _ARRAY3D_H_
#include <iostream>
#include<assert.h>
#include<typeinfo>

//template<typename T> 
//T ***AllocateMemory(size_t ni, size_t nj, size_t nk);

//template<typename T> 
//T ***DeallocateMemory(T ***array, size_t ni, size_t nj, size_t nk);
    
template<typename T>
class Array3D {

// friend function in template class need special treatment !

template<typename U> friend void print3Darray(const Array3D<U> &array3d);

// overloading 1 arg operator- as global function, ex: B = -A 
template<typename U> friend Array3D<U> operator-(const Array3D<U> &rhs);    
    
// overloading 2 arg operator+ as global function (element wise)
template<typename U> friend Array3D<U> operator+(const Array3D<U> &lhs,const Array3D<U> &rhs);    
    
// overloading 2 arg operator- as global function (element wise)
template<typename U> friend Array3D<U> operator-(const Array3D<U> &lhs,const Array3D<U> &rhs);

// overloading 2 arg operator* as global function (element wise)
template<typename U> friend Array3D<U> operator*(const Array3D<U> &lhs,const Array3D<U> &rhs);

// overloading 2 arg operator/ as global function (element wise)
template<typename U> friend Array3D<U> operator/(const Array3D<U> &lhs,const Array3D<U> &rhs);

// overloading 2 arg operator== as global function (element wise)
template<typename U> friend bool operator==(const Array3D<U> &lhs,const Array3D<U> &rhs);

// overloading 2 arg operator+ by scaler as global function
template<typename U> friend Array3D<U> operator+(double val, const Array3D<U> &rhs);
template<typename U> friend Array3D<U> operator+(const Array3D<U> &lhs, double val);

// overloading 2 arg operator* by scaler as global function
template<typename U> friend Array3D<U> operator*(double val, const Array3D<U> &rhs);
template<typename U> friend Array3D<U> operator*(const Array3D<U> &lhs, double val);

// overloading 2 arg operator/ by scaler as global function
template<typename U> friend Array3D<U> operator/(const Array3D<U> &lhs, double val);

// overloading 2 arg operator- by scaler as global function
template<typename U> friend Array3D<U> operator-(const Array3D<U> &lhs, double val);

// overloading string insertation operator as global function
template<typename U> friend std::ostream &operator<<(std::ostream &os, const Array3D<U> &obj); 

private:
    static size_t NumVectors; // cannot initialize value here 
    static bool IsVerbose;
    size_t ni {1}; // number of nodes in x direction 
    size_t nj {1}; //                    y
    size_t nk {1}; //                    z 
    T ***data {nullptr};

public:
    /* dont need to do Array3D<T> because inside class definitions, 
       C++ assumes that any reference to that class is templated, so adding the 
       <T> is redundant
    */
    
    // constructor
    // Array3D() = default; // don't use it because I need to NumVectors++
    Array3D();
    Array3D(size_t ni_val,size_t nj_val,size_t nk_val,T init_val = 0);
    
    // copy constructor ("deep")
    Array3D(const Array3D &source);
    
    // move constructor
    Array3D(Array3D &&source);
    
    // overloading assignment operator
    Array3D &operator=(double val);
    
    // overloading copy assignment operator 
    Array3D &operator=(const Array3D &rhs);   
    
    // overloading move assignment operator
    Array3D &operator=(Array3D &&rhs);   

    //overloading operator+= by scaler
    Array3D &operator+=(double val); 
    
    //overloading operator-= by scaler
    Array3D &operator-=(double val); 
    
    //overloading operator*= by scaler
    Array3D &operator*=(double val); 
    
    //overloading operator/= by scaler
    Array3D &operator/=(double val); 

    // overload array access operator 
    // so you can vec[1][2][0] = 7, instead of vec.data[1][2][0] = 7 */
    T **operator[](size_t i) {return data[i];}
    
    // getters
    size_t get_ni() const {return ni;}
    size_t get_nj() const {return nj;}
    size_t get_nk() const {return nk;}
    static size_t GetNumVectors() {return NumVectors;};
    
    // setter
    static void SetIsVerbose(bool IsV) {IsVerbose=IsV;}
    
    // destructor
    ~Array3D(); 
};

// Definition ==================================================================

// print array =================================================================
/*
When moving definition from .cpp to .h, inline is needed to avoid error:
/tmp/ccdACIyA.o: In function `print3Darray(Array3D const&)':
Array3D.cpp:(.text+0x0): multiple definition of `print3Darray(Array3D const&)'
/tmp/cckpaLg0.o:main.cpp:(.text+0x0): first defined here
collect2: error: ld returned 1 exit status

but if it is a template class, inline is not needed !
*/
template<typename T>
void print3Darray(const Array3D<T> &array) {
    for (size_t i{0}; i<array.ni; i++) {
        std::cout << "i = " << i << ": " << std::endl;
        for (size_t j{0}; j<array.nj; j++) {
            std::cout << "[ ";
            for (size_t k{0}; k<array.nk; k++) {
                std::cout << array.data[i][j][k] << ' ';
            }
            std::cout << ']' << std::endl;
        }
    }
}

// allocate memory for 3d array ================================================
template<typename T> 
T ***AllocateMemory(size_t ni, size_t nj, size_t nk) {
    assert(ni > 0);
    assert(nj > 0);
    assert(nk > 0);
    T ***array = new T**[ni];
    for (size_t i {0}; i<ni; i++) {
        array[i] = new T*[nj];
        for (size_t j {0}; j<nj; j++) {
            array[i][j] = new T[nk];
        }
    }    
    return array;
}

// deallocate memory for 3d array ==============================================
template<typename T> 
T ***DeallocateMemory(T ***array, size_t ni, size_t nj, size_t nk) {
    assert(ni > 0);
    assert(nj > 0);
    assert(nk > 0);
    if (array==nullptr) return array;
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            delete array[i][j];
        }
        delete array[i];
    }        
    delete [] array;
    // ref: 
    // set it to nullptr after you delete them, a null pointed exception is 
    // sometimes easier to spot, and it's also safe to call delete on 
    // nullptr. 
    array = nullptr;
    return array;
}

// constructor =================================================================
template<typename T>
Array3D<T>::Array3D() {
    NumVectors++;
    data = AllocateMemory<T>(ni,nj,nk);
    if (IsVerbose) { // Array3D<T>::IsVerbose works too 
        std::cout << "In No-Arg Constructor, "
                  << "Type=" << typeid(T).name() 
                  << ", NumVectors=" << NumVectors << std::endl;
    }
}

// constructor =================================================================
template<typename T>
Array3D<T>::Array3D(size_t ni_val, size_t nj_val, size_t nk_val, 
                    T init_val/* = 0*/) 
    :ni {ni_val}, nj {nj_val}, nk {nk_val} {
    NumVectors++;
    data = AllocateMemory<T>(ni,nj,nk);
    (*this) = init_val; // use assignment operator to assign initial value
    if (IsVerbose) { // Array3D<T>::IsVerbose works too 
        std::cout << "In 4-Arg Constructor, "
                  << "Type=" << typeid(T).name() 
                  << ", NumVectors=" << NumVectors << std::endl;
    }
}

// copy constructor ("deep") ===================================================
template<typename T>
Array3D<T>::Array3D(const Array3D<T> &source)
    :ni {source.ni}, nj {source.nj}, nk {source.nk} {
    NumVectors++;
    data = AllocateMemory<T>(ni,nj,nk);
    (*this) = source; // use copy assignment operator 
    if (IsVerbose) { // Array3D<T>::IsVerbose works too 
        std::cout << "In Copy Constructor, "
                  << "Type=" << typeid(T).name() 
                  << ", NumVectors=" << NumVectors << std::endl;
    }
} 

// move constructor ============================================================
template<typename T>
Array3D<T>::Array3D(Array3D<T> &&source)
    :ni {source.ni}, nj {source.nj}, nk {source.nk} {
    NumVectors++;
    data = source.data;
    source.data = nullptr;
    if (IsVerbose) { // Array3D<T>::IsVerbose works too 
        std::cout << "In Move Constructor" << std::endl;
    }  
}

// overloading assignment operator =============================================
template<typename T>
Array3D<T> &Array3D<T>::operator=(double val) {
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++){
                data[i][j][k] = val;
            }
        }
    }
    if (IsVerbose) // Array3D<T>::IsVerbose works too 
        {std::cout << "In Assignment Operator" << std::endl;}
    return *this;
}

// overloading copy assignment operator ========================================
template<typename T>
Array3D<T> &Array3D<T>::operator=(const Array3D<T> &rhs) {
    if (this == &rhs) {return *this;}
    data = DeallocateMemory<T>(data,ni,nj,nk);
    ni = rhs.ni;
    nj = rhs.nj;
    nk = rhs.nk;
    data = AllocateMemory<T>(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] = rhs.data[i][j][k];
            }
        }
    }
    if (IsVerbose) // Array3D<T>::IsVerbose works too 
        {std::cout << "In Copy Assignment Operator" << std::endl;}
    return *this;
}

// overloading move assignment operator ========================================
template<typename T>
Array3D<T> &Array3D<T>::operator=(Array3D<T> &&rhs) {
    if (this == &rhs) {return *this;}
    data = DeallocateMemory<T>(data,ni,nj,nk);
    ni = rhs.ni;
    nj = rhs.nj;
    nk = rhs.nk;
    data = rhs.data;
    rhs.data = nullptr;
    if (IsVerbose) { // Array3D<T>::IsVerbose works too 
        std::cout << "In Move Assignment Operator, "
                  << "Type=" << typeid(T).name() 
                  << " is moved to target." << std::endl;   } 
    return *this;
}

// overloading 1 arg operator- as global function ==============================
template<typename T>
Array3D<T> operator-(const Array3D<T> &rhs) {
    size_t ni = rhs.ni;
    size_t nj = rhs.nj;
    size_t nk = rhs.nk;
    Array3D<T> minus(ni,nj,nk); 
    //minus = -1*rhs;
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                minus.data[i][j][k] = -rhs.data[i][j][k];
            }
        }
    } 
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 1 Args Operator-" << std::endl;}
    return minus;
}

// overloading 2 arg operator+ as global function (element wise) ===============
template<typename T>
Array3D<T> operator+(const Array3D<T> &lhs,const Array3D<T> &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D<T> plus(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                plus.data[i][j][k] = lhs.data[i][j][k]+rhs.data[i][j][k];
            }
        }
    } 
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 Args Operator+" << std::endl;}
    return plus;
}

// overloading 2 arg operator- as global function (element wise) ===============
template<typename T>
Array3D<T> operator-(const Array3D<T> &lhs,const Array3D<T> &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D<T> minus(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                minus.data[i][j][k] = lhs.data[i][j][k]-rhs.data[i][j][k];
            }
        }
    } 
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 Args Operator-" << std::endl;}
    return minus;
}

// overloading 2 arg operator* as global function (element wise) ===============
template<typename T>
Array3D<T> operator*(const Array3D<T> &lhs,const Array3D<T> &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D<T> multiply(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                multiply.data[i][j][k] = lhs.data[i][j][k]*rhs.data[i][j][k];
            }
        }
    } 
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 Args Operator*" << std::endl;}
    return multiply;
}

// overloading 2 arg operator/ as global function (element wise) ===============
template<typename T>
Array3D<T> operator/(const Array3D<T> &lhs,const Array3D<T> &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D<T> divide(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                divide.data[i][j][k] = lhs.data[i][j][k]/rhs.data[i][j][k];
            }
        }
    } 
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 Args Operator/" << std::endl;}
    return divide;
}

// overloading 2 arg operator== as global function (element wise) ==============
template<typename T>
bool operator==(const Array3D<T> &lhs,const Array3D<T> &rhs) {
    if ( (lhs.ni!=rhs.ni) || 
         (lhs.nj!=rhs.nj) ||
         (lhs.nk!=rhs.nk) ) {
        return false;         
    }
    size_t ni = rhs.ni;
    size_t nj = rhs.nj;
    size_t nk = rhs.nk;
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                if (lhs.data[i][j][k] == rhs.data[i][j][k]) {
                    continue;
                } else {
                    return false;
                }
            }
        }
    }    
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 Args Operator==" << std::endl;}
    return true;
}

// overloading operator+= by scaler ============================================
template<typename T>
Array3D<T> &Array3D<T>::operator+=(double val) {
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] += val;
            }
        }
    }   
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In Operator+= By Scaler" << std::endl;}
    return *this;
}

// overloading operator-= by scaler ============================================
template<typename T>
Array3D<T> &Array3D<T>::operator-=(double val) {
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] -= val;
            }
        }
    }  
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In Operator-= By Scaler" << std::endl;}
    return *this;
}

// overloading operator*= by scaler ============================================
template<typename T>
Array3D<T> &Array3D<T>::operator*=(double val) {
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] *= val;
            }
        }
    }   
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In Operator*= By Scaler" << std::endl;}
    return *this;
}

// overloading operator/= by scaler ============================================
template<typename T>
Array3D<T> &Array3D<T>::operator/=(double val) {
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] /= val;
            }
        }
    }   
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In Operator/= By Scaler" << std::endl;}
    return *this;
}

// overloading 2 arg operator+ by scaler as global function ====================
template<typename T>
Array3D<T> operator+(double val, const Array3D<T> &rhs) {
    Array3D<T> plus {rhs};
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 arg Operator+ By Scaler" << std::endl;}
    return std::move(plus += val);
}

template<typename T>
Array3D<T> operator+(const Array3D<T> &lhs, double val) 
    {return operator+(val,lhs);}

// overloading 2 arg operator* by scaler as global function ====================
template<typename T>
Array3D<T> operator*(double val, const Array3D<T> &rhs) {
    Array3D<T> multiply {rhs};
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 arg Operator* By Scaler" << std::endl;}
    return std::move(multiply *= val);
}

template<typename T>
Array3D<T> operator*(const Array3D<T> &lhs, double val) 
    {return operator*(val,lhs);}

// overloading 2 arg operator/ by scaler as global function ====================
template<typename T>
Array3D<T> operator/(const Array3D<T> &lhs, double val) {
    Array3D<T> divide {lhs};
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 arg Operator/ By Scaler" << std::endl;}
    return std::move(divide /= val);
}

// overloading 2 arg operator- by scaler as global function ====================
template<typename T>
Array3D<T> operator-(const Array3D<T> &lhs, double val) {
    Array3D<T> sub {lhs};
    if (Array3D<T>::IsVerbose) // cannot just use IsVerbose
        {std::cout << "In 2 arg Operator- By Scaler" << std::endl;}
    return std::move(sub -= val);
}

// overloading string insertation operator as global function ==================
template<typename T>
std::ostream &operator<<(std::ostream &os, const Array3D<T> &obj) {
    os << "Array3D object into: (ni=" << obj.ni 
       << ", nj=" << obj.nj 
       << ", nk=" << obj.nk << ")" << std::endl;
    os << "print3Darray:" << std::endl;   
    print3Darray(obj);
    //os << "Total Number of vectors: " << Array3D<T>::GetNumVectors() << std::endl;
    return os;
}

// static variables ============================================================
/* 
ref: https://stackoverflow.com/q/19366615
When you have a (non-templated) class that contains a static member,
it must be defined in .cpp file.
If the class is a class template, the static member can be defined in the header

ref:https://www.geeksforgeeks.org/templates-and-static-variables-in-c/
Each instantiation of class template has its own copy of member static 
variables. In other words, Array3D<int> and Array3D<douyble> have it's own 
NumVectors and IsVerbose.
*/
template<typename T>
size_t Array3D<T>::NumVectors {0};

template<typename T>
bool Array3D<T>::IsVerbose {false};

// destructor ==================================================================
template<typename T>
Array3D<T>::~Array3D() {
    NumVectors--;
    if (data==nullptr) {
        
    } else {
        data = DeallocateMemory<T>(data,ni,nj,nk);
    }
    if (IsVerbose) { // Array3D<T>::IsVerbose works too 
        std::cout << "In Destructor, "
                  << "Type=" << typeid(T).name() 
                  << ", NumVectors =" << NumVectors << std::endl;
    }
}

#endif