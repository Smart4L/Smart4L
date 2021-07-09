import React, { useState, useEffect } from 'react';
import { w3cwebsocket as WebSocket } from 'websocket';
import { HashRouter as Switch, Route, withRouter } from "react-router-dom";

import Home from '../home/Home';
import Stats from '../stats/Stats';
import { Map } from '../map/Map';
import Settings from '../settings/Settings';

const client = WebSocket('wss://smart4l-websockets-mock.herokuapp.com');

export const Main = () => {
    const [speed, setSpeed] = useState(0);
    const [tempExt, setTempExt] = useState(0);
    const [carPosition, setCarPosition] = useState({ lat: 47.218371, lng: -1.553621 });


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
                if(data.label === "GPS longitude" || data.label === "GPS latitude"){
                    let newPosition = {
                        lat: data.measure,
                        lng: data.measure,
                    }
                    setCarPosition(newPosition)
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
            <Route exact path="/map" render={() => <Map carPosition={carPosition} />}/>
            <Route exact path="/settings" component={withRouter(Settings)}/>
            <Route exact path="/" render={() => <Home speed={speed} tempExt={tempExt}/>}/>
        </Switch>
    )
}