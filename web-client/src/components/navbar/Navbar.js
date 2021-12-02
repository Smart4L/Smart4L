import React,{ useState } from 'react';
import { NavLink } from "react-router-dom";
import { FaFan, FaRegLightbulb, FaRegMap, FaBullhorn } from 'react-icons/fa';
import { GoGraph } from "react-icons/go";
import { GiRadarSweep } from "react-icons/gi";
import { AiFillHome, AiFillVideoCamera, AiFillSetting } from "react-icons/ai";

const axios = require('axios');
const endpoint = 'http://172.20.10.2:8080'

export const Navbar = () => {
    const [isLight, setLight] = useState(false)
    const [fan, setFan] = useState(0)

    const changeFan = () => {
        if(fan === 0){
            axios.post(`${endpoint}/relay/ventilateur1`)
            .then((response) => {
                if(response.status === 200) {
                    if(response.data.status == 'on'){
                        setFan(1)
                    }
                }
              })
              .catch(function (error) {
                console.log(error);
              });
        } else if (fan === 1){
            axios.post(`${endpoint}/relay/ventilateur2`)
            .then((response) => {
                if(response.status === 200) {
                    if(response.data.status == 'on'){
                        setFan(2)
                    }
                }
              })
              .catch(function (error) {
                console.log(error);
              });
        } else {
            let fan_1
            let fan_2
            axios.delete(`${endpoint}/relay/ventilateur1`)
            .then((response) => {
                if(response.status === 200) {
                    if(response.data.status == 'off'){
                        fan_1 = false
                    }
                }
              })
              .catch(function (error) {
                console.log(error);
              });
            axios.delete(`${endpoint}/relay/ventilateur2`)
            .then((response) => {
                if(response.status === 200) {
                    if(response.data.status == 'off'){
                        fan_2 = false
                    }
                }
              })
              .catch(function (error) {
                console.log(error);
              });

            if(!fan_1 && !fan_2){
                setFan(0)
            }
        }
    }

    const changeLight = () => {
        if(isLight){
            axios.delete(`${endpoint}/relay/phare`)
            .then((response) => {
                if(response.status === 200) {
                    if(response.data.status == 'off'){
                        setLight(false)
                    }
                }
              })
              .catch(function (error) {
                console.log(error);
              });
        } else {
            axios.post(`${endpoint}/relay/phare`)
              .then((response) => {
                if(response.status === 200) {
                    if(response.data.status == 'on'){
                        setLight(true);
                    }
                }
              })
              .catch(function (error) {
                console.log(error);
              });
        }
    }

    const klaxonUp = (e) => {
        e.preventDefault();
        axios.post(`${endpoint}/relay/klaxon`)
            .then((response) => {
            })
            .catch(function (error) {
            console.log(error);
            });
    }

    const klaxonDown = () => {
        axios.delete(`${endpoint}/relay/klaxon`)
            .then((response) => {
            })
            .catch(function (error) {
            console.log(error);
            });
    }

    return(
        <div className="navbar_container">
            <NavLink exact to="/" activeClassName="active"><AiFillHome size={32} className={`navbar_item`}/></NavLink>
            <NavLink exact to="/map" activeClassName="active"><FaRegMap size={32} className={`navbar_item`}/></NavLink>
            <NavLink exact to="/video" activeClassName="active"><AiFillVideoCamera size={32} className={`navbar_item`}/></NavLink>
            <NavLink exact to="/radar" activeClassName="active"><GiRadarSweep size={32} className={`navbar_item`}/></NavLink>
            <NavLink exact to="/stats" activeClassName="active"><GoGraph size={32} className={`navbar_item`}/></NavLink>
            <a><FaRegLightbulb size={32} className={`navbar_item light ${isLight ? "shine" : ""}`} onClick={() => changeLight()}/></a>
            <a><FaFan size={32} className={`navbar_item turn-${fan}`} onClick={() => changeFan()}/></a>
            <a><FaBullhorn size={32} className={`navbar_item`} onMouseDown={e => klaxonUp(e)} onMouseUp={() => klaxonDown() } /></a>
            <NavLink exact to="/settings" activeClassName="active"><AiFillSetting size={32} className={`navbar_item`}/></NavLink>
        </div>
    )

}