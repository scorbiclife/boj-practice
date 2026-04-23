const fs = require("fs")

const [_header, line1, line2, ..._] = (
    fs.readFileSync(0, "utf-8")
        .trim().split("\n"))

const friends = line1.trim().split(/\s+/)
const me = line2.trim()

function solve(friends, me) {
    return friends.filter((f) => f === me).length;
}

const result = solve(friends, me)

fs.writeFileSync(1, `${result}\n`)
