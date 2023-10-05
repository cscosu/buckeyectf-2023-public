import { io } from "socket.io-client";
import { GameState } from "../types";

const URL = "https://infinity.chall.pwnoh.io";

const player = io(URL);
const a = io(URL);
const b = io(URL);
const c = io(URL);
const d = io(URL);

function sleep(seconds: number) {
    return new Promise((resolve) => setTimeout(resolve, 1000 * seconds));
}

const score = (state: GameState, socket: { id: string }) => state.scoreboard[socket.id] ?? 0;

player.on("gameState", async (state: GameState) => {
    if (state.correctAnswer === undefined) {
        console.log("\nPlayer score:", score(state, player));
        console.log(state.question.question);
        console.log(state.question.answers);
        a.emit("answer", 0);
        b.emit("answer", 1);
        c.emit("answer", 2);
        d.emit("answer", 3);
        await sleep(1);
        const gg = io(URL);
        gg.once("gameState", (newState: GameState) => {
            const adiff = score(newState, a) - score(state, a);
            const bdiff = score(newState, b) - score(state, b);
            const cdiff = score(newState, c) - score(state, c);
            const ddiff = score(newState, d) - score(state, d);
            const correctAnswer = [adiff, bdiff, cdiff, ddiff].findIndex(x => x == 1);
            console.log("emitting ", correctAnswer);
            player.emit("answer", correctAnswer);
            gg.disconnect();
        })
    } else {
        console.log("correct:", state.correctAnswer);
    }
})

player.on("flag", flag => {
    console.log("FLAG!", flag)
    process.exit();
})