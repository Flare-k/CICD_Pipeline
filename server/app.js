const express = require("express");
const os = require("os");
/*
import morgan from "morgan";
import helmet from "helmet";
import cookieParser from "cookie-parser";
 import bodyParser from "body-parser";
*/
const app = express();
const PORT = 80;
const time = new Date();
const date = time.getFullYear().toString() + '/' + (time.getMonth() + 1).toString() + '/' + time.getDate().toString(); 
const curTime = time.getHours().toString() + ":" + time.getMinutes().toString();

function handleListening() {
    console.log(`Listening on: http://localhost:${PORT}`);
}

const sayHello = (req, res) => res.send(`This is Server Test~! Server Run at ${date} ${curTime}`);

/*
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(helmet());
app.use(morgan("dev"));
*/
app.get('/', sayHello);
app.listen(PORT, handleListening); 
