import React from 'react';
import { NavLink } from "react-router-dom";
import { FaFan, FaRegLightbulb, FaRegMap, FaBullhorn } from 'react-icons/fa';
import { GoGraph } from "react-icons/go";
import { GiRadarSweep } from "react-icons/gi";
import { AiFillHome, AiFillVideoCamera, AiFillSetting } from "react-icons/ai";

export default class Navbar extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            light_on: false,
            fan_turn: 0,
        };
    }

    setFan = () => {
        let fan_turn
        if(this.state.fan_turn < 2){
            fan_turn = this.state.fan_turn + 1;
        } else {
            fan_turn = 0
        }

        // POST http://localhost:80/api/fan-speed/{fan_turn}

        this.setState({fan_turn});
    }

    setLight = () => {
        let light_on = !this.state.light_on;
        this.setState({light_on});
    }

    render(){
        return(
            <div className="navbar_container">
                <NavLink exact to="/" activeClassName="active"><AiFillHome size={32} className={`navbar_item`}/></NavLink>
                <NavLink exact to="/map" activeClassName="active"><FaRegMap size={32} className={`navbar_item`}/></NavLink>
                <NavLink exact to="/video" activeClassName="active"><AiFillVideoCamera size={32} className={`navbar_item`}/></NavLink>
                <NavLink exact to="/radar" activeClassName="active"><GiRadarSweep size={32} className={`navbar_item`}/></NavLink>
                <NavLink exact to="/stats" activeClassName="active"><GoGraph size={32} className={`navbar_item`}/></NavLink>
                <a><FaRegLightbulb size={32} className={`navbar_item light ${this.state.light_on ? "shine" : ""}`} onClick={() => this.setLight()}/></a>
                <a><FaFan size={32} className={`navbar_item turn-${this.state.fan_turn}`} onClick={() => this.setFan()}/></a>
                <NavLink exact to="/" activeClassName="active"><FaBullhorn size={32} className={`navbar_item`}/></NavLink>
                <NavLink exact to="/settings" activeClassName="active"><AiFillSetting size={32} className={`navbar_item`}/></NavLink>
            </div>
        )
    }
}