import React, { useState, useEffect } from 'react';
import { w3cwebsocket as WebSocket } from 'websocket';
import { HashRouter as Switch, Route, withRouter } from "react-router-dom";

import Home from '../home/Home';
import Stats from '../stats/Stats';
import { Map } from '../map/Map';
import { Video } from '../video/Video';
import { Radar } from '../radar/Radar';
import { Settings } from '../settings/Settings';

const client = WebSocket('ws://172.24.1.2:8082');

export const Main = () => {
    const [speed, setSpeed] = useState(0);
    const [tempExt, setTempExt] = useState(0);
    const [carPosition, setCarPosition] = useState({ lat: 47.218371, lng: -1.553621 });
    const [gyroPosition, setGyroPosition] = useState({ x: 0, y: 0, z:0 });


    useEffect(() => {
        client.onpen = () => {
            console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
            let data = JSON.parse(message.data);
            console.log(data)
            if(data.label === "Vitesse"){
                setSpeed(data.measure)
            }
            if(data.label === "Température extérieure"){
                setTempExt(data.measure)
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
                setTempExt(data.value.temperature)
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
        <Switch>
            <Route exact path="/stats" component={withRouter(Stats)}/>
            <Route exact path="/map" render={() => <Map carPosition={carPosition} speed={speed}/>}/>
            <Route exact path="/video" render={() => <Video />}/>
            <Route exact path="/radar" render={() => <Radar gyroPosition={gyroPosition} />}/>
            <Route exact path="/settings" component={withRouter(Settings)}/>
            <Route exact path="/" render={() => <Home speed={speed} tempExt={tempExt}/>}/>
        </Switch>
    )
}