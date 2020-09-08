import React from 'react';
import moment from 'moment'
import { Capitalize } from '../../utils/utils';
import { Line as ProgressLine} from 'rc-progress';
import { w3cwebsocket as WebSocket } from 'websocket';
import { MdSignalCellularConnectedNoInternet0Bar, MdSignalCellular1Bar, MdSignalCellular2Bar, MdSignalCellular3Bar, MdSignalCellular4Bar } from "react-icons/md";
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from "react-icons/md";

const client = WebSocket('wss://aws.cbarange.ovh:8520');

export default class Home extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            now :  moment(),
            temp: "NaN",
            fuel: Math.floor(Math.random() * Math.floor(100)),
            connect: Math.floor(Math.random() * Math.floor(5))
        }
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ now: moment() }), 500);
        client.onpen = () => {
            console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
            let data = JSON.parse(message.data);
            if(data.type === "UPDATE_SENSOR"){
                if(data.content.id === "DHT11_in"){
                    this.setState({ temp: data.content.value[0].measure });
                }
            }
        };
    }
    
    componentWillUnmount() {
        clearInterval(this.interval);
        client.close(1000, "End of connection");
    }

    getConnection = () => {
        if(this.state.connect === 0){
            return <MdSignalCellularConnectedNoInternet0Bar/>
        }
        else if(this.state.connect === 1) {
            return <MdSignalCellular1Bar/>
        }
        else if(this.state.connect === 2) {
            return <MdSignalCellular2Bar/>
        }
        else if(this.state.connect === 3) {
            return <MdSignalCellular3Bar/>
        }
        else {
            return <MdSignalCellular4Bar/>
        }
    }

    render(){
        return(
            <div className="home_container">
                <div className="home_item left_home_container">
                    <span className="title">Smart 4L - 404L</span>
                    <span className="content">{ this.state.now.format('HH:mm') }</span>
                    <span className="title little">{ Capitalize(this.state.now.format('dddd')) }</span>
                    <span className="content">{ this.state.now.format('DD') } { Capitalize(this.state.now.format('MMMM')) }</span>
                    <span className="title little">Température</span>
                    <span className="content">{ this.state.temp } °C</span>      
                    <span class="circle">
                        <span className="engine">ENGINE</span>
                        <span className="start_stop">START <hr></hr> STOP</span>
                    </span>
                </div>
                <div className="home_item right_home_container">
                    <div className="title little top">3G {this.getConnection()}</div>
                    <div className="speed">
                        <span className="title little head">Vitesse</span>
                        <span className="measure">80</span>
                        <span className="title little unit">km/h</span>
                    </div>
                    <div className="fuel">
                        <span className="head">Essence</span>
                        <ProgressLine percent={ this.state.fuel } trailColor="#263238" strokeColor="#00E5FF" strokeLinecap="butt" className="progress" trailWidth="5" strokeWidth="5"/>
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
    }
}