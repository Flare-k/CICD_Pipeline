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
const net = os.networkInterfaces();
const res = {};

for (const value of Object.keys(net)) {
    for (const n of net[value]) {
        if (n.family == 'IPv4' && !n.interval) {
            if (!res[value]) {
                res[value] = [];
            }
            res[value].push(n.address);
        }
    }
}

const ip = res['Loopback Pseudo-Interface 1'][0];

function handleListening() {
    console.log(`Listening on: http://${ip}:${PORT} - Server Run at ${date} ${curTime}`);

}

const sayHello = (req, res) => res.send("This is Server Test~!");

/*
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(helmet());
app.use(morgan("dev"));
*/
app.get('/', sayHello);
app.listen(PORT, handleListening); 
