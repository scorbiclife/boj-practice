const fs = require("fs")

class Stack {
    constructor() {
        this._stack = []
    }
    
    push(x) {
        this._stack.push(x)
    }

    _isEmpty() {
        return this._stack.length === 0
    }

    pop() {
        return this._isEmpty() ? -1 : this._stack.pop()
    }

    top() {
        return this._isEmpty() ? -1 : this._stack[this._stack.length - 1]
    }

    empty() {
        return this._isEmpty() ? 1 : 0
    }

    size() {
        return this._stack.length
    }
}

const globalStack = new Stack()

const input = fs.readFileSync(0, "utf8")
const output = solve(input)
fs.writeFileSync(1, String(output))

function solve(input) {
    const commands = parseInput(input)
    const results = (
        commands
        .map(command => executeCommand(command))
        .filter(result => result !== undefined))
    return results.join("\n") + "\n"
}

function parseInput(input) {
    const lines = input.trim().split("\n").slice(1).map(line => line.trim())
    return lines.map(parseLine)
}

function parseLine(line) {
    const words = line.trim().split(" ")
    if (words[0] === "push") {
        return ["push", parseInt(words[1], 10)]
    }
    return words
}

function executeCommand(command) {
    const [op, args] = [command[0], command.slice(1)]
    const result = globalStack[op].call(globalStack, ...args)
    return result
}
