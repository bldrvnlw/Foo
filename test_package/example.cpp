#include <foo_json.h>
#include <iostream>
#include <string>
#include <time.h>

int main() {
    time_t t = time(NULL);
    std::cout << do_the_foo(std::string("I've been foo-ed at: ") + asctime(localtime(&t))) << std::endl;
}
