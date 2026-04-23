const fs = require("fs")

const input = fs.readFileSync(0, "utf8")
const output = String(solution(input))
fs.writeFileSync(1, output)

function solution(input) {
    const lines = input.trim().split("\n").slice(1)
    return lines.map(reverseWords).join("\n") + "\n"
}

function reverseWords(line) {
    const words = line.split(" ");
    const reverseWord = (word) => {
        const chars = [...word]
        chars.reverse()
        return chars.join("")
    }
    return words.map(reverseWord).join(" ")
}

