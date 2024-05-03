import express from "express";
import { microPositions } from "./microPositions.js";

const app = express();

let currentIndex = 0;

// Función para incrementar el índice cada 2 segundos
setInterval(() => {
    currentIndex = (currentIndex + 1) % microPositions.length;
}, 2000); // 2000 milisegundos = 2 segundos

app.get("/", (req, res) => {
    // Enviar el objeto actual del arreglo
    res.send([microPositions[currentIndex]]);
});

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
