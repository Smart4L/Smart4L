import React from 'react';
import { w3cwebsocket as WebSocket } from 'websocket';
import { FaTemperatureHigh, FaTools } from "react-icons/fa";
import { IoMdSpeedometer } from "react-icons/io";
import { GiGears } from "react-icons/gi";

const client = WebSocket('wss://aws.cbarange.ovh:8520');

export default class Stats extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            tab: []
        }
    }

    componentDidMount() {
        client.onpen = () => {
            console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
            let data = JSON.parse(message.data);
            console.log(data)
            if(data.type === "UPDATE_SENSOR"){
                let tab =  this.state.tab;
                if(tab.filter(el => el.id === data.content.id).length > 0){
                    console.log('find');
                    let value = data.content.value;
                    this.setState({
                        tab: this.state.tab.map(el => (el.id === data.content.id ? Object.assign({}, el, { value }) : el))
                    });
                } 
                else {
                    console.log('dont find');
                    tab.push(data.content);
                    console.log(tab)
                    this.setState({
                        tab
                    })
                }
            };
        }
    }

    /**
     * 
     * @param {String} name Name of the icon you want
     * @return {Icon} Return the icon
     */
    getIcon = (name) => {
        let str = name.split('_')[1];
        if(str === "temp"){
            return <FaTemperatureHigh size={32}/>;
        } else if(str === "presure"){
            return <IoMdSpeedometer size={32}/>;
        } else if(str === "engine"){
            return <GiGears size={32}/>;
        } else {
            return <FaTools size={32}/>;
        }
    }

    render(){
        return(
            <div className="stats_container">
                { 
                    this.state.tab.map(el => 
                        {
                            return (
                                <div className="stats_item">
                                    <span>{el.id}:</span>
                                    {
                                        el.value.map((item) => {
                                            return(
                                                <span>{item.type}: {item.measure} {item.unit}</span>
                                            )
                                        })
                                    }
                                    <span>{this.getIcon(el.id)}</span>
                                </div>
                            )                        
                        }
                    )
                }
            </div>
        )
    }
}