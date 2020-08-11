import React from 'react';

export default class Home extends React.Component{
    render(){
        return(
            <div className="home_container">
                <div className="home_item left_home_container">
                    left
                    <span class="circle">
                        <span className="engine">ENGINE</span>
                        <span className="start_stop">START <hr></hr> STOP</span>
                    </span>
                </div>
                <div className="home_item right_home_container">
                    right
                </div>
            </div>
        )
    }
}