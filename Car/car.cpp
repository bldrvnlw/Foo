#include <foo_json.h>
#include <iostream>
#include <string>
#include <time.h>

int main() {
    time_t t = time(NULL);
    std::cout << do_the_foo(std::string("Car test - am I foo-ed at: ") + std::string(asctime(localtime(&t)) + std::string("?"))) << std::endl;
}
