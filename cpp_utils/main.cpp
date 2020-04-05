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
    std::cout << constr << std::endl;
    std::cout << "Testing print3Darray(constr)" << std::endl;
    print3Darray(constr);

    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"constr2(2,2,3,0.5)\"" << std::endl;
    Array3D constr2(2,2,3,0.5);
    std::cout << constr2 << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Constructor: \"*constr_ptr = new Array3D(1,1,4,1.5)\"" << std::endl;
    Array3D *constr_ptr = new Array3D(1,1,4,1.5);
    std::cout << (*constr_ptr) << std::endl;
    delete constr_ptr;

    std::cout << ' ' << std::endl;
    std::cout << "Constructur: \"const obj: const_obj(1,1,3,0.1)\"" << std::endl;
    const Array3D const_obj(1,1,3,0.1);  // const not working ? unless i use xx.data[][][]   ???????
    std::cout << const_obj << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Copy Constructor: \"constr_copy {constr2}\"" << std::endl;
    Array3D constr_copy {constr2};
    std::cout << constr_copy << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Move Constructor: \"Array3D(1,1,4,10.5)\"" << std::endl;
    std::vector<Array3D> vec_move;
    vec_move.push_back(Array3D(1,1,4,10.5));
    std::cout << vec_move.at(0) << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Assignment Operators"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Assignment Operator: \"constr2 = 3.5\'" << std::endl;
    constr2 = 3.5;
    std::cout << constr2 << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Copy Assignment Operator: \"copy_assignment = constr2\"" << std::endl;
    Array3D copy_assignment;
    copy_assignment = constr2;
    std::cout << copy_assignment << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Move Assignment operator: \"move_assignment = Array3D(1,2,3,10.4)\"" << std::endl;
    Array3D move_assignment;
    move_assignment = Array3D(1,2,3,10.4);
    std::cout << move_assignment << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (Element Wise) +-*/== as Global Function"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ as Global Function (Element Wise): \"plus2arg = constr2 + constr2\"" << std::endl;
    Array3D plus2arg = constr2 + constr2;
    std::cout << plus2arg << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator- as Global Function (Element Wise): \"minus2arg = constr2 - constr2\"" << std::endl;
    Array3D minus2arg = constr2 - constr2;
    std::cout << minus2arg << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* as Global Function (Element Wise): \"multiply2arg = constr2 * constr2\"" << std::endl;
    Array3D multiply2arg = constr2 * constr2;
    std::cout << multiply2arg << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator/ as Global Function (Element Wise): \"divide2arg = constr2 / constr2\"" << std::endl;
    Array3D divide2arg = constr2 / constr2;
    std::cout << divide2arg << std::endl;

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
    std::cout << add << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator-= By Scaler: \"sub(1,1,5) -= 10\"" << std::endl;
    Array3D sub(1,1,5);
    sub -= 10;
    std::cout << sub << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator*= By Scaler: \"multiply(1,1,5,1) *= 10\"" << std::endl;
    Array3D multiply(1,1,5,1);
    multiply *= 10;
    std::cout << multiply << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading Operator/= By Scaler: \"divide(1,1,5,1) /= 10\"" << std::endl;
    Array3D divide(1,1,5,1);
    divide /= 10;
    std::cout << divide << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Overloading Operators (By Scaler) +-*/ as Global Function"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ By Scaler as Global Function: \"plus2 = 5 + Array3D(1,1,5,0.1)\": " << std::endl;
    Array3D plus2 = 5 + Array3D(1,1,5,0.1);
    std::cout << plus2 << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator+ By Scaler as Global Function: \"plus3 = Array3D(1,1,5,0.1) + 5\": " << std::endl;
    Array3D plus3 = Array3D(1,1,5,0.1) + 5;
    std::cout << plus3 << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* By Scaler as Global Function: \"multiply2 = 5*Array3D(1,1,5,0.1)\": " << std::endl;
    Array3D multiply2 = 5*Array3D(1,1,5,0.1);
    std::cout << multiply2 << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator* By Scaler as Global Function: \"multiply3 = Array3D(1,1,5,0.1)*5\": " << std::endl;
    Array3D multiply3 = Array3D(1,1,5,0.1)*5;
    std::cout << multiply3 << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator/ By Scaler as Global Function: \"divide2 = Array3D(1,1,5,0.1)/5\": " << std::endl;
    Array3D divide2 = Array3D(1,1,5,0.1)/5;
    std::cout << divide2 << std::endl;

    std::cout << ' ' << std::endl;
    std::cout << "Overloading 2 arg Operator- By Scaler as Global Function: \"sub2 = Array3D(1,1,5,0.1)-5\": " << std::endl;
    Array3D sub2 = Array3D(1,1,5,0.1)-5;
    std::cout << sub2 << std::endl;
   
    std::cout << ' ' << std::endl;
    std::cout << "===================="<< std::endl;
    std::cout << "Other Overloading Operators"<< std::endl;
    std::cout << "===================="<< std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading 1 arg Operator- as Global Function: \"minus = -constr2\"" << std::endl;
    Array3D minus = -constr2;
    std::cout << minus << std::endl;
    
    std::cout << ' ' << std::endl;
    std::cout << "Overloading Array Access Operator => [0 1]" << std::endl;
    Array3D aap = Array3D(1,1,2);
    aap[0][0][0] = 0;
    aap[0][0][1] = 1;
    std::cout << aap << std::endl;
    
    //double ***AllocateMemory(size_t ni, size_t nj, size_t nk);
    //double ***dd = AllocateMemory(1,2,1);
    
    std::cout << ' ' << std::endl;
    return 0;
}
