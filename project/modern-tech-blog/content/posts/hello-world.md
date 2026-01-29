+++
title = 'Hello World - Testing Syntax Highlighting'
date = 2026-01-29T15:30:14Z
draft = false
description = 'A test post to verify syntax highlighting works across multiple programming languages'
tags = ['testing', 'programming', 'hugo']
+++

# Welcome to Modern Tech Blog

This is our first post to test that everything is working correctly, especially syntax highlighting for code blocks.

## JavaScript Example

Here's a JavaScript function:

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log("Fibonacci sequence:", [0,1,2,3,4,5].map(fibonacci));
```

## Python Example

And here's the same algorithm in Python:

```python
def fibonacci(n):
    """Calculate fibonacci number recursively"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Generate sequence
sequence = [fibonacci(i) for i in range(6)]
print(f"Fibonacci sequence: {sequence}")
```

## Go Example

Finally, let's see it in Go:

```go
package main

import "fmt"

func fibonacci(n int) int {
    if n <= 1 {
        return n
    }
    return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
    fmt.Print("Fibonacci sequence: ")
    for i := 0; i < 6; i++ {
        fmt.Printf("%d ", fibonacci(i))
    }
    fmt.Println()
}
```

## Conclusion

If you can see syntax highlighting for all three languages above, our Hugo setup is working perfectly!
