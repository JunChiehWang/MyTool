#include <iostream>
#include <vector>
#include "Array3D.h"

int main() {

    std::cout << "===================="<< std::endl;
    std::cout << "Constructors"<< std::endl;
    std::cout << "===================="<< std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"constr(2,2,3)\"" << std::endl;
    Array3D constr(2,2,3);
    print3Darray(constr);

    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"constr2(2,2,3,0.5)\"" << std::endl;
    Array3D constr2(2,2,3,0.5);
    print3Darray(constr2);

    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"*constr_ptr = new Array3D(1,1,4,1.5)\"" << std::endl;
    Array3D *constr_ptr = new Array3D(1,1,4,1.5);
    print3Darray(*constr_ptr);
    delete constr_ptr;

    std::cout << ' ' << std::endl;
    std::cout << "Constructur: \"const obj: const_obj(1,1,3,0.1)\"" << std::endl;
    const Array3D const_obj(1,1,3,0.1);  // const not working ? unless i use xx.data[][][]   ???????
    print3Darray(const_obj);   
    
    std::cout << ' ' << std::endl;
    std::cout << "Copy Constructor: \"constr_copy {constr2}\"" << std::endl;
    Array3D constr_copy {constr2};
    print3Darray(constr_copy);    
    
    std::cout << ' ' << std::endl;
    std::cout << "Move Constructor: \"Array3D(1,1,4,10.5)\"" << std::endl;
    std::vector<Array3D> vec_move;
    vec_move.push_back(Array3D(1,1,4,10.5));
    print3Darray(vec_move.at(0));  

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Assignment Operators"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Assignment Operator: \"constr2 = 3.5\'" << std::endl;
    constr2 = 3.5;
    print3Darray(constr2);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Copy Assignment Operator: \"copy_assignment = constr2\"" << std::endl;
    Array3D copy_assignment;
    copy_assignment = constr2;
    print3Darray(copy_assignment);  

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Move Assignment operator: \"move_assignment = Array3D(1,2,3,10.4)\"" << std::endl;
    Array3D move_assignment;
    move_assignment = Array3D(1,2,3,10.4);
    print3Darray(move_assignment);  

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators???????????"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 1 arg Operator- as Global Function: \"minus = -constr2\"" << std::endl;
    Array3D minus = -constr2;
    print3Darray(minus);    

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (Element Wise) +-*/== as Global Function"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ as Global Function (Element Wise): \"plus2arg = constr2 + constr2\"" << std::endl;
    Array3D plus2arg = constr2 + constr2;
    print3Darray(plus2arg);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator- as Global Function (Element Wise): \"minus2arg = constr2 - constr2\"" << std::endl;
    Array3D minus2arg = constr2 - constr2;
    print3Darray(minus2arg);   

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* as Global Function (Element Wise): \"multiply2arg = constr2 * constr2\"" << std::endl;
    Array3D multiply2arg = constr2 * constr2;
    print3Darray(multiply2arg);   

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator/ as Global Function (Element Wise): \"divide2arg = constr2 / constr2\"" << std::endl;
    Array3D divide2arg = constr2 / constr2;
    print3Darray(divide2arg); 

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator== as Global Function (Element Wise): \"constr2==constr2\"" << std::endl;
    std::cout << std::boolalpha;
    std::cout << (constr2==constr2) << std::endl; 

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator== as Global Function (Element Wise): \"Array3D(1,1,1)==Array3D(1,1,1,0.1)\"" << std::endl;
    std::cout << std::boolalpha;
    std::cout << (Array3D(1,1,1)==Array3D(1,1,1,0.1)) << std::endl; 

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (By Scaler) +=, -=, *=, /="<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator+= By Scaler: \"add(1,1,5) += 10\"" << std::endl;
    Array3D add(1,1,5);
    add += 10;
    print3Darray(add);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator-= By Scaler: \"sub(1,1,5) -= 10\"" << std::endl;
    Array3D sub(1,1,5);
    sub -= 10;
    print3Darray(sub);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator*= By Scaler: \"multiply(1,1,5,1) *= 10\"" << std::endl;
    Array3D multiply(1,1,5,1);
    multiply *= 10;
    print3Darray(multiply);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator/= By Scaler: \"divide(1,1,5,1) /= 10\"" << std::endl;
    Array3D divide(1,1,5,1);
    divide /= 10;
    print3Darray(divide);

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (By Scaler) +-*/ as Global Function"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ By Scaler as Global Function: \"plus2 = 5 + Array3D(1,1,5,0.1)\": " << std::endl;
    Array3D plus2 = 5 + Array3D(1,1,5,0.1);
    print3Darray(plus2);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ By Scaler as Global Function: \"plus3 = Array3D(1,1,5,0.1) + 5\": " << std::endl;
    Array3D plus3 = Array3D(1,1,5,0.1) + 5;
    print3Darray(plus3);
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* By Scaler as Global Function: \"multiply2 = 5*Array3D(1,1,5,0.1)\": " << std::endl;
    Array3D multiply2 = 5*Array3D(1,1,5,0.1);
    print3Darray(multiply2);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* By Scaler as Global Function: \"multiply3 = Array3D(1,1,5,0.1)*5\": " << std::endl;
    Array3D multiply3 = Array3D(1,1,5,0.1)*5;
    print3Darray(multiply3);
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator/ By Scaler as Global Function: \"divide2 = Array3D(1,1,5,0.1)/5\": " << std::endl;
    Array3D divide2 = Array3D(1,1,5,0.1)/5;
    print3Darray(divide2);

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator- By Scaler as Global Function: \"sub2 = Array3D(1,1,5,0.1)-5\": " << std::endl;
    Array3D sub2 = Array3D(1,1,5,0.1)-5;
    print3Darray(sub2);
    
    std::cout << ' ' << std::endl;
    return 0;
}
