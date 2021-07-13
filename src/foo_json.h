#pragma once
#include <string>

/**
 * @brief An interface for this static lib
 * 
 */

/**
 * @brief Foo a string: - wrap it in json and return it
 * 
 * Input: "input string"
 * 
 * Output:
 * '{"foo":"input string"}'
 * 
 * @param string_to_foo 
 * @return std::string 
 */
std::string do_the_foo(std::string &string_to_foo);