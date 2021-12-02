import React,{ useState, useEffect, forwardRef } from 'react';
import moment from 'moment'
import { Capitalize } from '../../utils/utils';
import { Line as ProgressLine} from 'rc-progress';
import { MdSignalCellularConnectedNoInternet0Bar, MdSignalCellular1Bar, MdSignalCellular2Bar, MdSignalCellular3Bar, MdSignalCellular4Bar } from "react-icons/md";
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from "react-icons/md";

const axios = require('axios');
const endpoint = 'http://172.20.10.2:8080'

export const Home = forwardRef((props, ref) => {

    const [now, setNow] = useState(moment())
    const [speed, setSpeed] = useState(0)
    const [temperature, setTemperature] = useState(0)
    const [humidityExt, setHumidityExt] = useState(0)
    const [fuel] = useState(Math.floor(Math.random() * Math.floor(100)));
    const [connect] = useState(Math.floor(Math.random() * Math.floor(5)))

    useEffect(() => {
        const timeInterval = setInterval(() => {
          setNow(moment())
        }, 500);
        return () => clearInterval(timeInterval);
      }, []);

    useEffect(() => { setSpeed(props.speed) }, [props.speed])
    useEffect(() => { setTemperature(props.tempExt) }, [props.tempExt])
    useEffect(() => { setHumidityExt(props.humidityExt) }, [props.humidityExt])


    const powerUp = (e) => {
        e.preventDefault();
        axios.post(`${endpoint}/relay/klaxon`)
            .then((response) => {
            })
            .catch(function (error) {
            console.log(error);
            });
    }

    const powerDown = () => {
        axios.delete(`${endpoint}/relay/klaxon`)
            .then((response) => {
            })
            .catch(function (error) {
            console.log(error);
            });
    }

    /**
     * @return {Icon} Return the icon match whith the actual connection level
     */
    const getConnection = () => {
        if(connect === 0){
            return <MdSignalCellularConnectedNoInternet0Bar/>
        }
        else if(connect === 1) {
            return <MdSignalCellular1Bar/>
        }
        else if(connect === 2) {
            return <MdSignalCellular2Bar/>
        }
        else if(connect === 3) {
            return <MdSignalCellular3Bar/>
        }
        else {
            return <MdSignalCellular4Bar/>
        }
    }

    
    return(
        <div className="home_container">
            <div className="home_item left_home_container">
                <span className="title">Smart 4L - 404L</span>
                <span className="content">{ now.format('HH:mm') }</span>
                <span className="title little">{ Capitalize(now.format('dddd')) }</span>
                <span className="content">{ now.format('DD') } { Capitalize(now.format('MMMM')) }</span>
                <span className="title little">Température</span>
                <span className="content">{ temperature } °C</span>
                <span className="title little">Humidité</span>
                <span className="content">{ humidityExt } %</span>
                <span className="circle" onMouseDown={e => powerUp(e)} onMouseUp={() => powerDown() }> 
                    <span className="engine">ENGINE</span>
                    <span className="start_stop">START<hr/>STOP</span>
                </span>
            </div>
            <div className="home_item right_home_container">
                <div className="title little top">3G {getConnection()}</div>
                <div className="speed">
                    <span className="title little head">Vitesse</span>
                    <span className="measure">{ speed }</span>
                    <span className="title little unit">km/h</span>
                </div>
                <div className="fuel">
                    <span className="head">Essence</span>
                    <ProgressLine percent={ fuel } trailColor="#263238" strokeColor="#00E5FF" strokeLinecap="butt" className="progress" trailWidth="5" strokeWidth="5"/>
                </div>
                <div className="carousel">
                    <MdKeyboardArrowLeft size={64} className="arrow"/>
                    <div className="carousel-data">
                        <span className="title little">Compteur</span>
                        <span className="carousel-content">524 km</span>
                    </div>
                    <MdKeyboardArrowRight size={64} className="arrow"/>
                </div>
            </div>
        </div>
    )
    
})