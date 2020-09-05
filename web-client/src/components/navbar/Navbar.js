import React from 'react';
import { FaFan, FaRegLightbulb, FaRegMap, FaBullhorn } from 'react-icons/fa';
import { GoGraph } from "react-icons/go";
import { GiRadarSweep } from "react-icons/gi";
import { AiFillVideoCamera, AiFillSetting } from "react-icons/ai";

export default class Navbar extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            light_on: false,
            fan_turn: false,
        };
    }

    setFan = () => {
        let fan_turn = !this.state.fan_turn;
        this.setState({fan_turn});
    }

    setLight = () => {
        let light_on = !this.state.light_on;
        this.setState({light_on});
    }

    render(){
        return(
            <div className="navbar_container">
                <FaRegMap size={32} className={`navbar_item`}/>
                <AiFillVideoCamera size={32} className={`navbar_item`}/>
                <GiRadarSweep size={32} className={`navbar_item`}/>
                <GoGraph size={32} className={`navbar_item`}/>
                <FaRegLightbulb size={32} className={`navbar_item light ${this.state.light_on ? "shine" : ""}`} onClick={() => this.setLight()}/>
                <FaFan size={32} className={`navbar_item ${this.state.fan_turn ? "turn" : ""}`} onClick={() => this.setFan()}/>
                <FaBullhorn size={32} className={`navbar_item`}/>
                <AiFillSetting size={32} className={`navbar_item`}/>
            </div>
        )
    }
}