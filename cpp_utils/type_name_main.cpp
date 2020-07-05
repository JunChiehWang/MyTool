#include<iostream>
#include"type_name.h"

class Person {
    private:
    int a {10};    
};

using std::cout;
using std::endl;

int main () {

    int i = 0;
    const int ci = 0;
    int& foo_lref();
    int&& foo_rref();
    int foo_value();
    Person p;
    const Person cp;
        
    std::cout << "decltype(i) is " << type_name<decltype(i)>() << '\n';
    std::cout << "decltype((i)) is " << type_name<decltype((i))>() << '\n';
    std::cout << "decltype(ci) is " << type_name<decltype(ci)>() << '\n';
    std::cout << "decltype((ci)) is " << type_name<decltype((ci))>() << '\n';
    std::cout << "decltype(static_cast<int&>(i)) is " << type_name<decltype(static_cast<int&>(i))>() << '\n';
    std::cout << "decltype(static_cast<int&&>(i)) is " << type_name<decltype(static_cast<int&&>(i))>() << '\n';
    std::cout << "decltype(static_cast<int>(i)) is " << type_name<decltype(static_cast<int>(i))>() << '\n';
    std::cout << "decltype(foo_lref()) is " << type_name<decltype(foo_lref())>() << '\n';
    std::cout << "decltype(foo_rref()) is " << type_name<decltype(foo_rref())>() << '\n';
    std::cout << "decltype(foo_value()) is " << type_name<decltype(foo_value())>() << '\n';

    std::cout << "decltype(p) is " << type_name<decltype(p)>() << '\n';
    std::cout << "decltype(cp) is " << type_name<decltype(cp)>() << '\n';

return 0;
}