#ifndef _ARRAY3D_H_
#define _ARRAY3D_H_
#include <iostream>
#include<assert.h>

class Array3D {
    
friend void print3Darray(const Array3D &array3d);

// overloading 1 arg operator- as global function
// ex: B = -A 
friend Array3D operator-(const Array3D &rhs);    
    
// overloading 2 arg operator+ as global function (element wise)
friend Array3D operator+(const Array3D &lhs,const Array3D &rhs);    
    
// overloading 2 arg operator- as global function (element wise)
friend Array3D operator-(const Array3D &lhs,const Array3D &rhs);

// overloading 2 arg operator* as global function (element wise)
friend Array3D operator*(const Array3D &lhs,const Array3D &rhs);

// overloading 2 arg operator/ as global function (element wise)
friend Array3D operator/(const Array3D &lhs,const Array3D &rhs);

// overloading 2 arg operator== as global function (element wise)
friend bool operator==(const Array3D &lhs,const Array3D &rhs);

// overloading 2 arg operator+ by scaler as global function
friend Array3D operator+(double val, const Array3D &rhs);
friend Array3D operator+(const Array3D &lhs, double val);

// overloading 2 arg operator* by scaler as global function
friend Array3D operator*(double val, const Array3D &rhs);
friend Array3D operator*(const Array3D &lhs, double val);

// overloading 2 arg operator/ by scaler as global function
friend Array3D operator/(const Array3D &lhs, double val);

// overloading 2 arg operator- by scaler as global function
friend Array3D operator-(const Array3D &lhs, double val);

// overloading string insertation operator as global function
friend std::ostream &operator<<(std::ostream &os, const Array3D &obj); 

private:
    static size_t NumVectors; // cannot assign value here 
    static bool IsVerbose;
    size_t ni {1}; // number of nodes in x direction 
    size_t nj {1}; //                    y
    size_t nk {1}; //                    z 
    double ***data {nullptr};

public:

    // constructor
    // Array3D() = default; // don't use it because I need to NumVectors++
    Array3D();
    Array3D(size_t ni_val,size_t nj_val,size_t nk_val,double init_val = 0);
    
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
    double **operator[](size_t i) {return data[i];}
    
    // getters
    size_t get_ni() const {return ni;}
    size_t get_nj() const {return nj;}
    size_t get_nk() const {return nk;}
    static size_t GetNumVectors();
    
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
*/
inline void print3Darray(const Array3D &array) {
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
inline double ***AllocateMemory(size_t ni, size_t nj, size_t nk) {
    assert(ni > 0);
    assert(nj > 0);
    assert(nk > 0);
    double ***array = new double**[ni];
    for (size_t i {0}; i<ni; i++) {
        array[i] = new double*[nj];
        for (size_t j {0}; j<nj; j++) {
            array[i][j] = new double[nk];
        }
    }    
    return array;
}

// deallocate memory for 3d array ==============================================
inline double ***DeallocateMemory(double ***array, 
                                  size_t ni, size_t nj, size_t nk) {
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
    array = nullptr;
    return array;
}

// constructor =================================================================
inline Array3D::Array3D() {
    if (IsVerbose) {std::cout << "In No-Arg Constructor" << std::endl;}
    NumVectors++;
}

// constructor =================================================================
inline Array3D::Array3D(size_t ni_val, 
                        size_t nj_val, 
                        size_t nk_val, 
                        double init_val/* = 0*/) 
    :ni {ni_val}, nj {nj_val}, nk {nk_val} {
    if (IsVerbose) {std::cout << "In 4-Arg Constructor" << std::endl;}
    NumVectors++;
    data = AllocateMemory(ni,nj,nk);
    (*this) = init_val; // use assignment operator to assign initial value
}

// copy constructor ("deep") ===================================================
inline Array3D::Array3D(const Array3D &source)
    :ni {source.ni}, nj {source.nj}, nk {source.nk} {
    if (IsVerbose) {std::cout << "In Copy Constructor" << std::endl;}
    NumVectors++;
    data = AllocateMemory(ni,nj,nk);
    (*this) = source; // use copy assignment operator 
    
    /*
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] = source.data[i][j][k];
            }
        }
    } 
    */
} 

// move constructor ============================================================
inline Array3D::Array3D(Array3D &&source)
    :ni {source.ni}, nj {source.nj}, nk {source.nk} {
    if (IsVerbose) {std::cout << "In Move Constructor" << std::endl;}
    NumVectors++;
    data = source.data;
    source.data = nullptr;
}

// overloading assignment operator =============================================
inline Array3D &Array3D::operator=(double val) {
    if (IsVerbose) {std::cout << "In Assignment Operator" << std::endl;}
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++){
                data[i][j][k] = val;
            }
        }
    }
    return *this;
}

// overloading copy assignment operator ========================================
inline Array3D &Array3D::operator=(const Array3D &rhs) {
    if (IsVerbose) {std::cout << "In Copy Assignment Operator" << std::endl;}
    if (this == &rhs) {return *this;}
    data = DeallocateMemory(data,ni,nj,nk);
    ni = rhs.ni;
    nj = rhs.nj;
    nk = rhs.nk;
    data = AllocateMemory(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] = rhs.data[i][j][k];
            }
        }
    }
    return *this;
}

// overloading move assignment operator ========================================
inline Array3D &Array3D::operator=(Array3D &&rhs) {
    if (IsVerbose) {std::cout << "In Move Assignment Operator" << std::endl;}
    if (this == &rhs) {return *this;}
    data = DeallocateMemory(data,ni,nj,nk);
    ni = rhs.ni;
    nj = rhs.nj;
    nk = rhs.nk;
    data = rhs.data;
    rhs.data = nullptr;
    return *this;
}

// overloading 1 arg operator- as global function ==============================
inline Array3D operator-(const Array3D &rhs) {
    if (Array3D::IsVerbose) {std::cout << "In 1 Args Operator-" << std::endl;}
    size_t ni = rhs.ni;
    size_t nj = rhs.nj;
    size_t nk = rhs.nk;
    Array3D minus(ni,nj,nk); 
    //minus = -1*rhs;
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                minus.data[i][j][k] = -rhs.data[i][j][k];
            }
        }
    } 
    return minus;
}

// overloading 2 arg operator+ as global function (element wise) ==============
inline Array3D operator+(const Array3D &lhs,const Array3D &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    if (Array3D::IsVerbose) {std::cout << "In 2 Args Operator+" << std::endl;}
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D plus(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                plus.data[i][j][k] = lhs.data[i][j][k]+rhs.data[i][j][k];
            }
        }
    } 
    return plus;
}

// overloading 2 arg operator- as global function (element wise) ===============
inline Array3D operator-(const Array3D &lhs,const Array3D &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    if (Array3D::IsVerbose)  {std::cout << "In 2 Args Operator-" << std::endl;}
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D minus(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                minus.data[i][j][k] = lhs.data[i][j][k]-rhs.data[i][j][k];
            }
        }
    } 
    return minus;
}

// overloading 2 arg operator* as global function (element wise) ===============
inline Array3D operator*(const Array3D &lhs,const Array3D &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    if (Array3D::IsVerbose) {std::cout << "In 2 Args Operator*" << std::endl;}
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D multiply(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                multiply.data[i][j][k] = lhs.data[i][j][k]*rhs.data[i][j][k];
            }
        }
    } 
    return multiply;
}

// overloading 2 arg operator/ as global function (element wise) ===============
inline Array3D operator/(const Array3D &lhs,const Array3D &rhs){
    assert(lhs.ni == rhs.ni);
    assert(lhs.nj == rhs.nj);
    assert(lhs.nk == rhs.nk);
    if (Array3D::IsVerbose) {std::cout << "In 2 Args Operator/" << std::endl;}
    size_t ni = lhs.ni;
    size_t nj = lhs.nj;
    size_t nk = lhs.nk;
    Array3D divide(ni,nj,nk);
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                divide.data[i][j][k] = lhs.data[i][j][k]/rhs.data[i][j][k];
            }
        }
    } 
    return divide;
}

// overloading 2 arg operator== as global function (element wise) ==============
inline bool operator==(const Array3D &lhs,const Array3D &rhs) {
    if (Array3D::IsVerbose) {std::cout << "In 2 Args Operator==" << std::endl;}
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
    return true;
}

// overloading operator+= by scaler ============================================
inline Array3D &Array3D::operator+=(double val) {
    if (IsVerbose) {std::cout << "In Operator+= By Scaler" << std::endl;}
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] += val;
            }
        }
    }   
    return *this;
}

// overloading operator-= by scaler ============================================
inline Array3D &Array3D::operator-=(double val) {
    if (IsVerbose) {std::cout << "In Operator-= By Scaler" << std::endl;}
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] -= val;
            }
        }
    }   
    return *this;
}

// overloading operator*= by scaler ============================================
inline Array3D &Array3D::operator*=(double val) {
    if (IsVerbose) {std::cout << "In Operator*= By Scaler" << std::endl;}
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] *= val;
            }
        }
    }   
    return *this;
}

// overloading operator/= by scaler ============================================
inline Array3D &Array3D::operator/=(double val) {
    if (IsVerbose) {std::cout << "In Operator/= By Scaler" << std::endl;}
    for (size_t i {0}; i<ni; i++) {
        for (size_t j {0}; j<nj; j++) {
            for (size_t k {0}; k<nk; k++) {
                data[i][j][k] /= val;
            }
        }
    }   
    return *this;
}

// overloading 2 arg operator+ by scaler as global function ====================
inline Array3D operator+(double val, const Array3D &rhs) {
    if (Array3D::IsVerbose) 
        {std::cout << "In 2 arg Operator+ By Scaler" << std::endl;}
    Array3D plus {rhs};
    return std::move(plus += val);
}
inline Array3D operator+(const Array3D &lhs, double val) 
    {return operator+(val,lhs);}

// overloading 2 arg operator* by scaler as global function ====================
inline Array3D operator*(double val, const Array3D &rhs) {
    if (Array3D::IsVerbose) 
        {std::cout << "In 2 arg Operator* By Scaler" << std::endl;}
    Array3D multiply {rhs};
    return std::move(multiply *= val);
}

inline Array3D operator*(const Array3D &lhs, double val) 
    {return operator*(val,lhs);}

// overloading 2 arg operator/ by scaler as global function ====================
inline Array3D operator/(const Array3D &lhs, double val) {
    if (Array3D::IsVerbose)  
        {std::cout << "In 2 arg Operator/ By Scaler" << std::endl;}
    Array3D divide {lhs};
    return std::move(divide /= val);
}

// overloading 2 arg operator- by scaler as global function ====================
inline Array3D operator-(const Array3D &lhs, double val) {
    if (Array3D::IsVerbose) 
        {std::cout << "In 2 arg Operator- By Scaler" << std::endl;}
    Array3D sub {lhs};
    return std::move(sub -= val);
}

// overloading string insertation operator as global function ==================
inline std::ostream &operator<<(std::ostream &os, const Array3D &obj) {
    os << "Array3D object (ni=" << obj.ni 
       << ", nj=" << obj.nj 
       << ", nk=" << obj.nk << ")" << std::endl;
    os << "print3Darray:" << std::endl;   
    print3Darray(obj);
    os << "Total Number of vectors: " << Array3D::GetNumVectors() << std::endl;
    return os;
}

// destructor ==================================================================
inline Array3D::~Array3D() {
    if (IsVerbose) {std::cout << "In Destructor" << std::endl;}
    NumVectors--;
    if (data==nullptr) return;
    data = DeallocateMemory(data,ni,nj,nk);
}

#endif