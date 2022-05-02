import React, { useState, useEffect } from 'react';
import { w3cwebsocket as WebSocket } from 'websocket';
import { Routes, Route } from "react-router-dom";
import { Home } from '../home/Home';
import { Map } from '../map/Map';
import { Video } from '../video/Video';
import { Radar } from '../radar/Radar';
import { Stats } from '../stats/Stats';
import { Settings } from '../settings/Settings';
import { WS_URL } from '../../utils/variables';

import '../../assets/css/Main.css';

const client = WebSocket(WS_URL);

export const Main = () => {
    const [speed, setSpeed] = useState(0);
    const [humidity, setHumidity] = useState(0);
    const [carPosition, setCarPosition] = useState({ lat: 47.218371, lng: -1.553621 });
    const [gyroPosition, setGyroPosition] = useState({ x: 0, y: 0, z:0 });
    const [waterTemp, setWaterTemp] = useState(0);
    const [oilTemp, setOilTemp] = useState(0);
    const [interiorTemp, setInteriorTemp] = useState(0);
    const [exteriorTemp, setExteriorTemp] = useState(0);
    const [pressure, setPressure] = useState(0);


    useEffect(() => {
        client.onpen = () => {
            console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
            let data = JSON.parse(message.data);
            console.log(data);
            
            if(data.id === "DHT11_25"){
                setHumidity(data.value.humidity)
            }
            if(data.id === "SIM7600G_H_GPS"){
                let newPosition = {
                    lat: data.value.latitude,
                    lng: data.value.longitude,
                }
                setCarPosition(newPosition)
                setSpeed(Math.floor((data.value.speed * 1.852) * 10) / 10)
            }
            if(data.id === "GY521_MPU6050"){
                let newPosition = {
                    x: data.value.gyroscope.X,
                    y: data.value.gyroscope.Y,
                    z: data.value.gyroscope.Z,
                }
                setGyroPosition(newPosition)
            }
            if(data.id === "BMP280"){
                setInteriorTemp(data.value.temperature)
                setPressure(data.value.pressure)
            }
            if(data.id === "DS18B20_BLACK"){
                setWaterTemp(data.value.temperature)
            }
            if(data.id === "DS18B20_RED"){
                setExteriorTemp(data.value.temperature)
            }
            if(data.id === "DS18B20_BLUE"){
                setOilTemp(data.value.temperature)
            }
        };

        client.onclose = function(e) {
            console.log('Disconnected!');
        };

        client.onerror = (message) => {
            console.log(`Error: ${message}`)
        }
    }, [])

    return (
        <Routes>
            <Route path="/" element={<Home speed={speed} exteriorTemp={exteriorTemp} humidity={humidity}/>}/>
            <Route path="/map" element={<Map carPosition={carPosition} speed={speed}/>}/>
            <Route path="/video" element={<Video/>}/>
            <Route path="/radar" element={<Radar gyroPosition={gyroPosition} />}/>
            <Route exact path="/stats" element={<Stats waterTemp={waterTemp} oilTemp={oilTemp} interiorTemp={interiorTemp}
                                                       exteriorTemp={exteriorTemp} humidity={humidity} pressure={pressure}/>}/>
            <Route exact path="/settings" element={<Settings/>}/>
        </Routes>
    )
}