import express from "express";
import Papa from "papaparse";
import fs from "fs";
import { promisify } from "util";

const app = express();
const readFileAsync = promisify(fs.readFile);

async function loadCSVData(filePath) {
    try {
        const csvString = await readFileAsync(filePath, "utf8");
        return transformCSVtoObjects(csvString);
    } catch (error) {
        console.error("Error reading CSV file:", error);
        throw error;
    }
}

function transformCSVtoObjects(csvString) {
    const parsed = Papa.parse(csvString, {
        header: true,
        skipEmptyLines: true,
    });

    return parsed.data.map((item, index) => ({
        patent: generateRandomPatent(),
        brand: "Koepp Inc",
        model: "Shoes",
        line: parseInt(item.linea, 10),
        currentPosition: {
            latitude: parseFloat(item.cx),
            longitude: parseFloat(item.cy),
        },
        id: index.toString(),
    }));
}

function generateRandomPatent() {
    const characters =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < 10; i++) {
        result += characters.charAt(
            Math.floor(Math.random() * characters.length)
        );
    }
    return result;
}

let currentIndexStart = 0;
let currentIndexEnd = 0; // Será ajustado después de cargar los datos
let microPositions = [];

async function startServer() {
    microPositions = await loadCSVData("./rutas_micros.csv");
    currentIndexEnd = microPositions.length - 1; // Inicializa en el último índice

    app.get("/", (req, res) => {
        const result = [
            microPositions[currentIndexStart],
            microPositions[currentIndexEnd],
        ];

        // Actualizar índices para la próxima solicitud
        currentIndexStart = (currentIndexStart + 2) % microPositions.length;
        currentIndexEnd =
            (currentIndexEnd - 3 + microPositions.length) %
            microPositions.length;

        res.send(result);
    });

    app.listen(3000, () => {
        console.log("Server is running on port 3000");
    });
}

startServer().catch((error) => {
    console.error("Failed to start the server:", error);
});
