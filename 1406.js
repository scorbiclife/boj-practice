class EditorBuffer {
    constructor({ initialString }) {
        this.beforeStack = [...initialString]
        this.afterStack = []
    }

    getContents() {
        const afterContents = [...this.afterStack].reverse()
        return [...this.beforeStack, ...afterContents].join("")
    }

    moveLeft() {
        if (this.beforeStack.length === 0) {
            return
        }
        this.afterStack.push(this.beforeStack.pop())
    }

    moveRight() {
        if (this.afterStack.length === 0) {
            return
        }
        this.beforeStack.push(this.afterStack.pop())
    }

    deleteOneCharacter() {
        this.beforeStack.pop()
    }

    insertOneCharacter(c) {
        this.beforeStack.push(c)
    }
}

function assert(predicate, ...args) {
    if (predicate(args)) {
        return
    }
    throw new Error("Assertion Error", { cause: { predicate, args } })
}

function read(input) {
    const [initialString, _nCommands, ...commandLines] = input.trim().split("\n")
    const commands = commandLines.map(line => line.split(" "))
    const parsedInput = { initialString, commands }
    return parsedInput
}

function evaluate({ initialString, commands }) {
    const buffer = new EditorBuffer({ initialString })
    for (const [opname, ...args] of commands) {
        switch (opname) {
            case "L":
                buffer.moveLeft()
                break
            case "D":
                buffer.moveRight()
                break
            case "B":
                buffer.deleteOneCharacter()
                break
            case "P":
                assert((args) => args.length === 1, args)
                const [character] = args
                buffer.insertOneCharacter(character)
                break
            default:
                throw new Error("Unreachable!")
        }
    }
    return buffer.getContents()
}

function format(result) {
    return result
}

const fs = require("fs")
const input = fs.readFileSync(0, "utf-8")
const output = format(evaluate(read(input)))
fs.writeFileSync(1, output)

