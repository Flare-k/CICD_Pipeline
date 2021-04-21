
const express = require("express");
const os = require("os");

const app = express();
const PORT = 80;
const time = new Date();
const date = time.getFullYear().toString() + '/' + (time.getMonth() + 1).toString() + '/' + time.getDate().toString(); 
const curTime = time.getHours().toString() + ":" + time.getMinutes().toString();

function handleListening() {
    console.log(`Listening on: http://localhost:${PORT}`);
}

const sayHello = (req, res) => res.send(`This is Server Test~! Server Run at ${date} ${curTime}`);


app.get('/', sayHello);
app.listen(PORT, handleListening); 