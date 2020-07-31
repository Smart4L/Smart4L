import React from 'react';
import { FaFan, FaRegLightbulb, FaRegMap, FaBullhorn } from 'react-icons/fa';
import { GoGraph } from "react-icons/go";
import { GiRadarSweep } from "react-icons/gi";
import { AiFillCamera, AiFillVideoCamera, AiFillSetting } from "react-icons/ai";

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
                <FaRegMap className={`navbar_item`}/>
                <AiFillVideoCamera className={`navbar_item`}/>
                <GiRadarSweep className={`navbar_item`}/>
                <GoGraph className={`navbar_item`}/>
                <FaRegLightbulb className={`navbar_item light ${this.state.light_on ? "shine" : ""}`} onClick={() => this.setLight()}/>
                <FaFan className={`navbar_item ${this.state.fan_turn ? "turn" : ""}`} onClick={() => this.setFan()}/>
                <FaBullhorn className={`navbar_item`}/>
                <AiFillSetting className={`navbar_item`}/>
            </div>
        )
    }
}