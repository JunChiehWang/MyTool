#include <iostream>
#include <vector>
#include "Array3D.h"

int main() {
    
    /* Set static variables. 
    Each instantiation of class template has its own copy of member static 
    variables. */ 
    Array3D<int>::SetIsVerbose(true);
    Array3D<double>::SetIsVerbose(true);
    
    std::cout << "===================="<< std::endl;
    std::cout << "Constructors"        << std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"constr(2,2,3)\"" << std::endl;
    Array3D<int> constr(2,2,3);
    std::cout << constr << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"constr2(2,2,3,0.5)\"" << std::endl;
    //Array3D constr2(2,2,3,0.5); // works for c++17
    Array3D<double> constr2(2,2,3,0.5);
    std::cout << constr2 << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"*constr_ptr = new Array3D<double>(1,1,4,1.5)\"" << std::endl;
    //Array3D<double> *constr_ptr = new Array3D<double>(1,1,4,1.5);
    auto *constr_ptr = new Array3D<double>(1,1,4,1.5);
    std::cout << (*constr_ptr) << std::endl;
    delete constr_ptr;
    
    std::cout << ' ' << std::endl;
    std::cout << "Constructur: \"const obj: const_obj(1,1,3,0.1)\"" << std::endl;
    const Array3D<double> const_obj(1,1,3,0.1);  // const not working ? unless i use xx.data[][][]   ???????
    std::cout << const_obj << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Copy Constructor: \"constr_copy {constr2}\"" << std::endl;
    auto constr_copy {constr2};
    std::cout << constr_copy << std::endl;
    assert(constr_copy==constr2);
    
    std::cout << ' ' << std::endl;
    std::cout << "Move Constructor: \"Array3D(1,1,4,10)\"" << std::endl;
    std::vector<Array3D<int>> vec_move;
    vec_move.push_back(Array3D<int>(1,1,4,10));
    std::cout << vec_move.at(0) << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Assignment Operators"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Assignment Operator: \"constr2 = 2\'" << std::endl;
    constr2 = 2;
    std::cout << constr2 << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Copy Assignment Operator: \"copy_assignment = constr2\"" << std::endl;
    Array3D<double> copy_assignment;
    copy_assignment = constr2;
    std::cout << copy_assignment << std::endl;
    assert(copy_assignment==constr2);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Move Assignment operator: \"move_assignment = Array3D(1,2,3,10.4)\"" << std::endl;
    Array3D<double> move_assignment;
    move_assignment = Array3D<double>(1,2,3,10.4);
    std::cout << move_assignment << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (Element Wise) +-*/== as Global Function"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ as Global Function (Element Wise): \"plus2arg = constr2 + constr2\"" << std::endl;
    auto plus2arg = constr2 + constr2;
    std::cout << plus2arg << std::endl;
    assert(plus2arg==Array3D<double>(2,2,3,4));

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator- as Global Function (Element Wise): \"minus2arg = constr2 - constr2\"" << std::endl;
    auto minus2arg = constr2 - constr2;
    std::cout << minus2arg << std::endl;
    assert(minus2arg==Array3D<double>(2,2,3,0));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* as Global Function (Element Wise): \"multiply2arg = constr2 * constr2\"" << std::endl;
    auto multiply2arg = constr2 * constr2;
    std::cout << multiply2arg << std::endl;
    assert(multiply2arg==Array3D<double>(2,2,3,4));
       
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator/ as Global Function (Element Wise): \"divide2arg = constr2 / constr2\"" << std::endl;
    auto divide2arg = constr2 / constr2;
    std::cout << divide2arg << std::endl;
    assert(divide2arg==Array3D<double>(2,2,3,1));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator== as Global Function (Element Wise): \"constr2==constr2\"" << std::endl;
    std::cout << std::boolalpha;
    std::cout << (constr2==constr2) << std::endl; 
    assert(constr2==constr2);
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator== as Global Function (Element Wise): \"Array3D(1,1,1)==Array3D(1,1,1,0.1)\"" << std::endl;
    std::cout << std::boolalpha;
    std::cout << (Array3D<double>(1,1,1)==Array3D<double>(1,1,1,0.1)) << std::endl; 
    assert((Array3D<double>(1,1,1)==Array3D<double>(1,1,1,0.1)) == false);

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (By Scaler) +=, -=, *=, /="<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator+= By Scaler: \"add(1,1,5) += 10\"" << std::endl;
    Array3D<int> add(1,1,5);
    add += 10;
    std::cout << add << std::endl;
    assert(add == Array3D<int>(1,1,5,10));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator-= By Scaler: \"sub(1,1,5) -= 10\"" << std::endl;
    Array3D<int> sub(1,1,5);
    sub -= 10;
    std::cout << sub << std::endl;
    assert(sub == Array3D<int>(1,1,5,-10));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator*= By Scaler: \"multiply(1,1,5,1) *= 10\"" << std::endl;
    Array3D<int> multiply(1,1,5,1);
    multiply *= 10;
    std::cout << multiply << std::endl;
    assert(multiply == Array3D<int>(1,1,5,10));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator/= By Scaler: \"divide_d(1,1,5,1) /= 10\"" << std::endl;
    Array3D<double> divide_d(1,1,5,1);
    divide_d /= 10;
    std::cout << divide_d << std::endl;
    assert(divide_d == Array3D<double>(1,1,5,0.1));

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator/= By Scaler: \"divide_i(1,1,5,1) /= 10\"" << std::endl;
    Array3D<int> divide_i(1,1,5,1);
    divide_i /= 10;
    std::cout << divide_i << std::endl;
    assert(divide_i == Array3D<int>(1,1,5,0));
    
    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (By Scaler) +-*/ as Global Function"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ By Scaler as Global Function: \"plus2 = 5 + Array3D(1,1,5,0.1)\": " << std::endl;
    auto plus2 = 5 + Array3D<double>(1,1,5,0.1);
    std::cout << plus2 << std::endl;
    assert(plus2 == Array3D<double>(1,1,5,5.1));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ By Scaler as Global Function: \"plus3 = Array3D(1,1,5,0.1) + 5\": " << std::endl;
    auto plus3 = Array3D<double>(1,1,5,0.1) + 5;
    std::cout << plus3 << std::endl;
    assert(plus3 == Array3D<double>(1,1,5,5.1));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* By Scaler as Global Function: \"multiply2 = 5*Array3D(1,1,5,0.1)\": " << std::endl;
    auto multiply2 = 5*Array3D<double>(1,1,5,0.1);
    std::cout << multiply2 << std::endl;
    assert(multiply2 == Array3D<double>(1,1,5,0.5));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* By Scaler as Global Function: \"multiply3 = Array3D(1,1,5,0.1)*5\": " << std::endl;
    auto multiply3 = Array3D<double>(1,1,5,0.1)*5;
    std::cout << multiply3 << std::endl;
    assert(multiply3 == Array3D<double>(1,1,5,0.5));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator/ By Scaler as Global Function: \"divide2 = Array3D(1,1,5,0.1)/5\": " << std::endl;
    auto divide2 = Array3D<double>(1,1,5,0.1)/5;
    std::cout << divide2 << std::endl;
    assert(divide2 == Array3D<double>(1,1,5,0.02));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator- By Scaler as Global Function: \"sub2 = Array3D(1,1,5,0.1)-5\": " << std::endl;
    auto sub2 = Array3D<double>(1,1,5,0.1)-5;
    std::cout << sub2 << std::endl;
    assert(sub2 == Array3D<double>(1,1,5,-4.9));

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Other Overloading Operators"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 1 arg Operator- as Global Function: \"minus = -constr2\"" << std::endl;
    auto minus = -constr2;
    std::cout << minus << std::endl;
    assert(minus == Array3D<double>(2,2,3,-2));
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Array Access Operator => [0 1]" << std::endl;
    auto aap = Array3D<int>(1,1,2);
    aap[0][0][0] = 9;
    aap[0][0][1] = 9;
    std::cout << aap << std::endl;
    assert(aap == Array3D<int>(1,1,2,9));

    std::cout << ' ' << std::endl;
    return 0;

}