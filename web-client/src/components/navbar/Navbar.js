import React,{ useState } from 'react';
import { NavLink } from "react-router-dom";
import { FaFan, FaKey, FaRegMap, FaBullhorn } from 'react-icons/fa';
import { GoGraph } from "react-icons/go";
import { GiRadarSweep } from "react-icons/gi";
import { AiFillHome, AiFillVideoCamera, AiFillSetting } from "react-icons/ai";
import env from "react-dotenv";

import '../../assets/css/Navbar.css';

const axios = require('axios');

export const Navbar = () => {
    const [isLight, setLight] = useState(false)
    const [fan, setFan] = useState(0)

    const changeFan = () => {
        if(fan === 0){
            axios.post(`${env.api_websocket}/relay/ventilateur1`)
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
            axios.post(`${env.api_websocket}/relay/ventilateur2`)
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
            axios.delete(`${env.api_websocket}/relay/ventilateur1`)
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
            axios.delete(`${env.api_websocket}/relay/ventilateur2`)
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

    const startUp = () => {
        let resultat = window.confirm('Démarrer ?')

        if(resultat){
            axios.post(`${env.api_websocket}/relay/demarreur`)
            .then((response) => {

            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }

    const klaxonUp = (e) => {
        e.preventDefault();
        axios.post(`${env.api_websocket}/relay/klaxon`)
            .then((response) => {
            })
            .catch(function (error) {
            console.log(error);
            });
    }

    const klaxonDown = () => {
        axios.delete(`${env.api_websocket}/relay/klaxon`)
            .then((response) => {
            })
            .catch(function (error) {
            console.log(error);
            });
    }

    return(
        <div className="navbar_container">
            <NavLink to="/" activeClassName="active"><AiFillHome size={32} className={`navbar_item`}/></NavLink>
            <NavLink to="/map" activeClassName="active"><FaRegMap size={32} className={`navbar_item`}/></NavLink>
            <NavLink to="/video" activeClassName="active"><AiFillVideoCamera size={32} className={`navbar_item`}/></NavLink>
            <NavLink to="/radar" activeClassName="active"><GiRadarSweep size={32} className={`navbar_item`}/></NavLink>
            <NavLink to="/stats" activeClassName="active"><GoGraph size={32} className={`navbar_item`}/></NavLink>
            <a href="#light"><FaKey size={32} className={`navbar_item light ${isLight ? "shine" : ""}`} onClick={() => startUp()}/></a>
            <a href="#fan"><FaFan size={32} className={`navbar_item turn-${fan}`} onClick={() => changeFan()}/></a>
            <a href="#horn"><FaBullhorn size={32} className={`navbar_item`} onMouseDown={e => klaxonUp(e)} onMouseUp={() => klaxonDown() } /></a>
            <NavLink to="/settings" activeClassName="active"><AiFillSetting size={32} className={`navbar_item`}/></NavLink>
        </div>
    )

}