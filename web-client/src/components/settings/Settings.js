import React from 'react';

export default class Settings extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render(){
        return(
            <div className="settings_container">
                <div className="left_settings_container">
                    <span>Thème</span>
                    <span>Délai synchronisation</span>
                    <span>Délai mesure</span>
                    <span>Délai photo</span>
                    <span>Thème</span>
                </div>
                <div className="right_settings_container">
                    right_settings_container
                </div>
            </div>
        )
    }
}