const fs = require("fs")

const input = fs.readFileSync(0, "utf8")
const output = String(solve(input))
fs.writeFileSync(1, output)

function solve(input) {
    const parsedInput = parseInput(input)
    const results = parsedInput.map(isVps)
    return results.map(result => result ? "YES" : "NO").join("\n") + "\n"
}

function parseInput(input) {
    const [header, ...body] = input.trim().split("\n")
    return body
}

function isVps(string) {
    const stack = []
    for (const c of string) {
        if (c === "(") {
            stack.push(null)
            continue
        }
        if (c === ")") {
            if (stack.length === 0) {
                return false
            }
            stack.pop()
            continue
        }
        throw new Error(`Assertion failure: expected paren, got other character '${c}'`)
    }
    return stack.length === 0
}
