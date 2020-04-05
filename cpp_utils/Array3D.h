#ifndef _ARRAY3D_H_
#define _ARRAY3D_H_
#include <iostream>

class Array3D {
    
friend void print3Darray(const Array3D &array3d);

// overloading 1 arg operator- as global function
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
friend Array3D operator+(const Array3D &rhs, double val);

// overloading 2 arg operator* by scaler as global function
friend Array3D operator*(double val, const Array3D &rhs);
friend Array3D operator*(const Array3D &lhs, double val);

// overloading 2 arg operator/ by scaler as global function
friend Array3D operator/(const Array3D &lhs, double val);

// overloading 2 arg operator- by scaler as global function
friend Array3D operator-(const Array3D &lhs, double val);

private:
    static size_t NumVectors; // cannot assign value here 
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
    
// not tested yet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    
    // destructor
    ~Array3D(); 
    
    // static function
    static size_t GetNumVectors();

    
    // ?????????????????????????????? how ???
    /* overload the array access operator 
       so you can do: r[1][2][0] = 7, instead of: r.data[1][2][0] = 7 */
    double **operator[](size_t i) {return data[i];}

    // getter ni, nj, nk
    size_t get_ni() const {return ni;}
    size_t get_nj() const {return nj;}
    size_t get_nk() const {return nk;}
    

};


#endif