import React,{ useState, useEffect } from 'react';
import ReactCountryFlag from "react-country-flag"
import { ListGroup } from 'react-bootstrap'
import { BiSun,BiMoon } from "react-icons/bi";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import BootstrapSwitchButton from 'bootstrap-switch-button-react'
import Axios from 'axios';
import NumericInput from 'react-numeric-input2';
import env from "react-dotenv";
import { API_URL } from '../../utils/variables';

import '../../assets/css/Settings.css';

export const Settings = () => {


    const [delaiphoto,setdelaiPhoto] =  useState(0)

    useEffect(() => {

        Axios({
            method: "get",
            url:`${API_URL}/interval`,
            timeout: 1000,
          })
            .then(result => {
                setdelaiPhoto(result.data)
                    
            })
            .catch(error => {
              console.log(error);
              console.log("Erreur pas de connexion à l'API Photo")
              const notify = () => toast.error("📷 Erreur pas de connexion à l'API Photo",{position: toast.POSITION.TOP_CENTER,autoClose: 2000});
              notify()
          });

    },[])


    
    const changePhoto = (numPhoto) => {

        Axios({
            method: "post",
            url: `${API_URL}/interval`,
            params: {num : numPhoto},
            timeout: 1000,
          })
            .then(result => {
                    
            })
            .catch(error => {
              console.log(error);
              console.log("Erreur pas de connexion à l'API Photo")
              const notify = () => toast.error("📷 Erreur pas de connexion à l'API Photo",{position: toast.POSITION.TOP_CENTER,autoClose: 2000});
              notify()
              
          });
        
    }

    return (
        <div className="settings_container">
        <div className="settings_top">
            <div className="settings_themes">
                Thème
                <div className="settings_themes_mode">
                <BiSun/>
                <BiMoon/>
                </div>
                
            </div>
            <div className="settings_langues">
                Langues

                <div className="settings_pays">
                <ReactCountryFlag
                countryCode="FR"
                svg
                style={{
                    width: '2em',
                    height: '2em',
                }}
                cdnUrl="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.4.3/flags/1x1/"
                cdnSuffix="svg"
                title="FR"
                />

                <ReactCountryFlag
                countryCode="US"
                svg
                style={{
                    width: '2em',
                    height: '2em',
                }}
                cdnUrl="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.4.3/flags/1x1/"
                cdnSuffix="svg"
                title="US"
            />
                </div>
            </div>

                
            </div>
            <div className="settings_options">
                Options
                <ListGroup>
                <ListGroup.Item>⌛ Delai de synchronisation
                <NumericInput step={1} precision={0} min={1} max={59} value={delaiphoto} onChange={numPhoto=> changePhoto(numPhoto)} mobile className="form-control settings_bouton_dark" />
               
                </ListGroup.Item>
                <ListGroup.Item>🌡️ Delai de mesure (0 désactivé)
                <NumericInput step={1} precision={0} min={1} max={59} value={delaiphoto} onChange={numPhoto=> changePhoto(numPhoto)} mobile className="form-control settings_bouton_dark" />
                
                </ListGroup.Item>
                <ListGroup.Item> 📷 Delai photo (0 désactivé)
                <NumericInput step={1} precision={0} min={1} max={59} value={delaiphoto} onChange={numPhoto=> changePhoto(numPhoto)} mobile className="form-control settings_bouton_dark" />
                </ListGroup.Item>
                <ListGroup.Item className="settings_options_item"> 🤖 Passage en vue radar automatique
                
                <BootstrapSwitchButton 
                checked={false}
                onlabel='ON'
                offlabel='OFF'
                onstyle="info"
                offStyle="danger"
                onChange={status=> console.log(status)}
                />
               
               
                </ListGroup.Item>
                <ListGroup.Item className="settings_options_item"> 💡 Allumage automatique des phares
                <BootstrapSwitchButton 
                checked={false}
                onlabel='ON'
                offlabel='OFF'
                onstyle="info"
                offStyle="danger"
                onChange={status=> console.log(status)}
                />
                </ListGroup.Item>
                <ListGroup.Item className="settings_options_item"> 🔋 Eteindre quand la batterie est faible
                <BootstrapSwitchButton 
                checked={false}
                onlabel='ON'
                offlabel='OFF'
                onstyle="info"
                offStyle="danger"
                onChange={status=> console.log(status)}
                />
                </ListGroup.Item>
                </ListGroup>
            </div>

            <ToastContainer />

        </div>
    )


}