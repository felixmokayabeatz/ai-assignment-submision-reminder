







#include <iostream>
#include <string>

std::string greet(){
    std::string greeting = "Hello World";
    return greeting;
}

int main(){
    std::cout << greet() << std::endl;
    return 0;
}