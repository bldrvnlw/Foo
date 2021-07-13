#include <iostream>


#include "Poco/JSON/Object.h"
#include "Poco/JSON/Stringifier.h"

std::string do_the_foo(std::string &string_to_foo) {
    Poco::JSON::Object::Ptr json = new Poco::JSON::Object;
    json->set("foo", string_to_foo);
    std::ostringstream ret_str;
    Poco::JSON::Stringifier::stringify(json, ret_str);
    return ret_str.str();
}
