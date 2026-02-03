const fs = require("fs")

function read(input) {
    const [header, ...body] = input.trim().split("\n")
    const numbers = body.map(Number)
    return numbers
}

function evaluate(numbers) {
    if (numbers.length === 0) {
        throw new Error("Assertion failed: numbers empty")
    }
    const sorted = [...numbers].sort((a, b) => a - b)
    const ops = []

    const stack = [0]
    let nextNumber = 1

    function top() {
        return stack[stack.length - 1]
    }

    function push() {
        ops.push("+")
        stack.push(nextNumber)
        nextNumber += 1
    }
    
    function pop() {
        ops.push("-")
        return stack.pop()
    }

    for (const n of numbers) {
        if (n < top()) {
            return null
        }
        if (n == top()) {
            pop()
            continue
        }
        // n > top()
        while (n > top()) {
            push()
        }
        // n === top()
        if (n !== top()) {
            throw new Error(`Assertion failed: n !== top(), n=${n}, top()=${top()}`)
        }
        pop()
    }
    return ops
}

function print(output) {
    if (!output) {
        return "NO"
    }
    return output.join("\n")
}

const input = fs.readFileSync(0, "utf-8")
const output = print(evaluate(read(input)))
fs.writeFileSync(1, output)

