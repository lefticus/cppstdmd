"""Test new generic parsing helper functions in cpp-common.lua"""
import subprocess
import pytest
from pathlib import Path


def run_lua_test(lua_code):
    """Helper to run Lua code that tests cpp-common.lua functions"""
    # Create a test script that requires cpp-common and runs the test
    test_script = f"""
package.path = package.path .. ";src/cpp_std_converter/filters/?.lua"
local common = require("cpp-common")

{lua_code}
"""

    result = subprocess.run(
        ["lua"],
        input=test_script,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

    return result.stdout, result.stderr, result.returncode


class TestExtractMultiArgMacro:
    """Test extract_multi_arg_macro() helper function"""

    def test_two_args_simple(self):
        """Test extracting two simple arguments"""
        lua_code = '''
local text = "\\\\unicode{1234}{Greek letter alpha}"
local args, end_pos = common.extract_multi_arg_macro(text, 1, 8, 2)
assert(args ~= nil, "Should extract arguments")
assert(#args == 2, "Should have 2 arguments")
assert(args[1] == "1234", "First arg should be codepoint")
assert(args[2] == "Greek letter alpha", "Second arg should be description")
assert(end_pos == #text + 1, "Should be at end of string")
print("PASS: two_args_simple")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: two_args_simple" in stdout

    def test_two_args_with_nested_braces(self):
        """Test extracting arguments with nested braces"""
        lua_code = '''
local text = "\\\\unicode{03B1}{Greek letter {alpha}}"
local args, end_pos = common.extract_multi_arg_macro(text, 1, 8, 2)
assert(args ~= nil, "Should extract arguments")
assert(#args == 2, "Should have 2 arguments")
assert(args[1] == "03B1", "First arg should be codepoint")
assert(args[2] == "Greek letter {alpha}", "Second arg should preserve nested braces")
print("PASS: two_args_with_nested_braces")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: two_args_with_nested_braces" in stdout

    def test_three_args_with_whitespace(self):
        """Test extracting three arguments with whitespace between them"""
        lua_code = '''
local text = "\\\\foo{arg1}  {arg2}\\n{arg3}"
local args, end_pos = common.extract_multi_arg_macro(text, 1, 4, 3)
assert(args ~= nil, "Should extract arguments")
assert(#args == 3, "Should have 3 arguments")
assert(args[1] == "arg1", "First arg")
assert(args[2] == "arg2", "Second arg")
assert(args[3] == "arg3", "Third arg")
print("PASS: three_args_with_whitespace")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: three_args_with_whitespace" in stdout

    def test_missing_argument(self):
        """Test failure when argument is missing"""
        lua_code = '''
local text = "\\\\unicode{1234}"  -- Only one arg, expecting two
local args, end_pos = common.extract_multi_arg_macro(text, 1, 8, 2)
assert(args == nil, "Should fail when argument missing")
assert(end_pos == nil, "end_pos should be nil on failure")
print("PASS: missing_argument")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: missing_argument" in stdout

    def test_malformed_braces(self):
        """Test failure with unbalanced braces"""
        lua_code = '''
local text = "\\\\foo{arg1}{arg{2}"  -- Unclosed brace in arg2
local args, end_pos = common.extract_multi_arg_macro(text, 1, 4, 2)
assert(args == nil, "Should fail with unbalanced braces")
print("PASS: malformed_braces")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: malformed_braces" in stdout


class TestProcessMacroWithReplacement:
    """Test process_macro_with_replacement() helper function"""

    def test_simple_replacement(self):
        """Test simple macro replacement"""
        lua_code = '''
local text = "This is a \\\\term{definition} here."
local result = common.process_macro_with_replacement(text, "term", function(content)
    return "*" .. content .. "*"
end)
assert(result == "This is a *definition* here.", "Should replace macro with emphasized text")
print("PASS: simple_replacement")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: simple_replacement" in stdout

    def test_multiple_instances(self):
        """Test replacing multiple instances"""
        lua_code = '''
local text = "\\\\defn{foo} and \\\\defn{bar} and \\\\defn{baz}"
local result = common.process_macro_with_replacement(text, "defn", function(content)
    return "**" .. content .. "**"
end)
assert(result == "**foo** and **bar** and **baz**", "Should replace all instances")
print("PASS: multiple_instances")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: multiple_instances" in stdout

    def test_nested_braces_in_content(self):
        """Test handling nested braces in macro content"""
        lua_code = '''
local text = "\\\\impldef{foo{bar}baz}"
local result = common.process_macro_with_replacement(text, "impldef", function(content)
    return "implementation-defined // " .. content
end)
assert(result == "implementation-defined // foo{bar}baz", "Should handle nested braces")
print("PASS: nested_braces_in_content")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: nested_braces_in_content" in stdout

    def test_no_instances(self):
        """Test text with no macro instances"""
        lua_code = '''
local text = "This text has no macros"
local result = common.process_macro_with_replacement(text, "term", function(content)
    return "*" .. content .. "*"
end)
assert(result == text, "Should return unchanged text")
print("PASS: no_instances")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: no_instances" in stdout


class TestExpandNestedMacrosRecursive:
    """Test expand_nested_macros_recursive() helper function"""

    def test_simple_pattern(self):
        """Test simple non-nested pattern expansion"""
        lua_code = '''
local text = "\\\\keyword{noexcept}"
local patterns = {
    {pattern = "\\\\keyword{([^}]*)}", replacement = function(c) return c end}
}
local result = common.expand_nested_macros_recursive(text, patterns, 5)
assert(result == "noexcept", "Should expand keyword macro")
print("PASS: simple_pattern")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: simple_pattern" in stdout

    def test_nested_pattern_two_levels(self):
        """Test nested macros requiring two passes"""
        lua_code = '''
local text = "\\\\tcode{\\\\keyword{noexcept}}"
local patterns = {
    {pattern = "\\\\keyword{([^}]*)}", replacement = function(c) return c end},
    {pattern = "\\\\tcode{([^}]*)}", replacement = function(c) return c end}
}
local result = common.expand_nested_macros_recursive(text, patterns, 5)
assert(result == "noexcept", "Should expand nested macros")
print("PASS: nested_pattern_two_levels")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: nested_pattern_two_levels" in stdout

    def test_deeply_nested(self):
        """Test deeply nested macros requiring multiple passes"""
        lua_code = '''
local text = "\\\\a{\\\\b{\\\\c{content}}}"
local patterns = {
    {pattern = "\\\\a{([^}]*)}", replacement = function(c) return c end},
    {pattern = "\\\\b{([^}]*)}", replacement = function(c) return c end},
    {pattern = "\\\\c{([^}]*)}", replacement = function(c) return c end}
}
local result = common.expand_nested_macros_recursive(text, patterns, 5)
assert(result == "content", "Should expand deeply nested macros")
print("PASS: deeply_nested")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: deeply_nested" in stdout

    def test_early_termination(self):
        """Test early termination when no changes occur"""
        lua_code = '''
local text = "plain text"
local call_count = 0
local patterns = {
    {pattern = "\\\\\\\\keyword{([^}]*)}", replacement = function(c)
        call_count = call_count + 1
        return c
    end}
}
local result = common.expand_nested_macros_recursive(text, patterns, 5)
assert(result == "plain text", "Should return unchanged")
print("PASS: early_termination")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: early_termination" in stdout

    def test_string_replacement(self):
        """Test using string replacement instead of function"""
        lua_code = '''
local text = "foo \\\\seebelow bar"
local patterns = {
    {pattern = "\\\\seebelow", replacement = "see below"}
}
local result = common.expand_nested_macros_recursive(text, patterns, 5)
assert(result == "foo see below bar", "Should do string replacement")
print("PASS: string_replacement")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: string_replacement" in stdout


class TestRemoveMacro:
    """Test remove_macro() helper function"""

    def test_remove_keep_content(self):
        """Test removing macro but keeping content (default)"""
        lua_code = '''
local text = "This is \\\\textrm{roman text} here."
local result = common.remove_macro(text, "textrm")
assert(result == "This is roman text here.", "Should remove macro but keep content")
print("PASS: remove_keep_content")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: remove_keep_content" in stdout

    def test_remove_discard_content(self):
        """Test removing macro and discarding content"""
        lua_code = '''
local text = "This is \\\\textrm{roman text} here."
local result = common.remove_macro(text, "textrm", false)
assert(result == "This is  here.", "Should remove macro and content")
print("PASS: remove_discard_content")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: remove_discard_content" in stdout

    def test_multiple_instances(self):
        """Test removing multiple instances"""
        lua_code = '''
local text = "\\\\emph{one} and \\\\emph{two} and \\\\emph{three}"
local result = common.remove_macro(text, "emph")
assert(result == "one and two and three", "Should remove all instances")
print("PASS: remove_multiple")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: remove_multiple" in stdout

    def test_nested_braces(self):
        """Test removing macro with nested braces in content"""
        lua_code = '''
local text = "\\\\foo{content{nested}more}"
local result = common.remove_macro(text, "foo")
assert(result == "content{nested}more", "Should handle nested braces")
print("PASS: remove_nested_braces")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: remove_nested_braces" in stdout

    def test_no_instances(self):
        """Test text with no macro instances"""
        lua_code = '''
local text = "This text has no macros"
local result = common.remove_macro(text, "textrm")
assert(result == text, "Should return unchanged text")
print("PASS: remove_no_instances")
'''
        stdout, stderr, code = run_lua_test(lua_code)
        assert code == 0
        assert "PASS: remove_no_instances" in stdout
