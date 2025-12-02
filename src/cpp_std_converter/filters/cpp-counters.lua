--[[
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
]]

--[[
cpp-counters.lua

Shared counter module for Pandoc Lua filters.
Provides a factory function to create counter instances with consistent interface.

Usage:
  local Counter = require("cpp-counters")
  local counters = Counter.new({"note", "example"})

  counters:get("note")       -- returns current value (0 initially)
  counters:increment("note") -- increments and returns new value
  counters:set("note", 5)    -- sets to specific value
  counters:reset("note")     -- resets to 0
  counters:reset_all()       -- resets all counters to 0
]]

local M = {}

-- Factory function to create a new counter instance
-- @param types: array of counter type names, e.g., {"note", "example"}
-- @return: counter instance with get/set/increment/reset methods
function M.new(types)
  local counters = {}
  for _, t in ipairs(types) do
    counters[t] = 0
  end

  local instance = {}

  -- Get current value for a counter type
  function instance:get(counter_type)
    return counters[counter_type] or 0
  end

  -- Set value for a counter type
  function instance:set(counter_type, value)
    counters[counter_type] = value
  end

  -- Increment counter and return new value
  function instance:increment(counter_type)
    counters[counter_type] = (counters[counter_type] or 0) + 1
    return counters[counter_type]
  end

  -- Reset a specific counter to 0
  function instance:reset(counter_type)
    counters[counter_type] = 0
  end

  -- Reset all counters to 0
  function instance:reset_all()
    for t in pairs(counters) do
      counters[t] = 0
    end
  end

  return instance
end

-- Capitalize first letter of a string
-- Shared utility used by multiple filters for environment labels
function M.capitalize(s)
  return s:sub(1, 1):upper() .. s:sub(2)
end

return M
