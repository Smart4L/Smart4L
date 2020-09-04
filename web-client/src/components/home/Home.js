import React from 'react';
import moment from 'moment'
import { Capitalize } from '../../utils/utils';

export default class Home extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            now :  moment(),
        }
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ now: moment() }), 500);
    }
    
    componentWillUnmount() {
        clearInterval(this.interval);
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
                    <span className="content">{ Math.floor(Math.random() * Math.floor(30)) } °C</span>      
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