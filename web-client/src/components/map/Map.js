import React from 'react';
import moment from 'moment';
import Leaflet from 'leaflet';
import L from 'leaflet';
import { Map as LMap, Marker, Popup, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

Leaflet.Icon.Default.imagePath = '../node_modules/leaflet';

delete Leaflet.Icon.Default.prototype._getIconUrl;

Leaflet.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

export const suitcasePoint = new L.Icon({
    iconUrl: require('../../assets/images/4l.png'),
    iconRetinaUrl: require('../../assets/images/4l.png'),
    iconAnchor: [20, 40],
    popupAnchor: [0, -35],
    iconSize: [40, 40],
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    shadowSize: [29, 40],
    shadowAnchor: [7, 40],
})

export default class Map extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            now :  moment(),
            zoom: 13,
            carPosition: {
                lat: 47.218371,
                lng: -1.553621,
            },
            mapPosition:{
                lat: 47.218371,
                lng: -1.553621,
            },
            isCenter: true,
            tab:[
                {
                    lat: 47.185711,
                    lng: -1.521606
                },
                {
                    lat: 47.187578,
                    lng: -1.613617
                },
                {
                    lat: 47.230958,
                    lng: -1.571388
                },
                {
                    lat: 47.228160,
                    lng: -1.527786
                }
            ]
        }
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ now: moment() }), 500);
        this.changePos  =  setInterval( () => this.updateCar(this.state.tab[Math.floor(this.state.tab.length * Math.random())]) , 1500)
    }
    
    componentWillUnmount() {
        clearInterval(this.interval);
        clearInterval(this.changePos);
    }

    updateCar = (newPosition) => {
        console.log('CarUpdate');
        console.log(newPosition);
        this.setState({ 
            carPosition: newPosition
        })
        if(this.state.isCenter){
            this.setState({ 
                mapPosition: newPosition
            })
        }
    }

    getPosition = (obj) => {
        return [obj.lat, obj.lng]
    }

    onMoveEvent = () => {
        console.log('move')
        if(this.state.isCenter){
            this.setState({
                isCenter: false
            })
        }
    }

    recenter = () => {
        this.setState({
            isCenter: true,
        })
    }

    render(){
        let nantes = [47.218371,-1.553621];
        return(
            <div className="map_container">
                <div className="top">
                    <span className="content">
                        { this.state.now.format('HH:mm') }
                    </span>
                </div>
                <div className="leaflet-container">
                    <LMap center={this.getPosition(this.state.mapPosition)} zoom={this.state.zoom}
                        onmouseup={this.onMoveEvent}
                    >
                        <TileLayer
                        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        <Marker position={nantes}>
                            <Popup>
                                Nantes <br/> Une belle ville 
                            </Popup>
                        </Marker>
                        <Marker position={this.getPosition(this.state.carPosition)} icon={suitcasePoint}>
                            <Popup>
                                L'équipage 404L
                            </Popup>
                        </Marker>
                    </LMap>
                </div>
                <div className={`bottom ${this.state.isCenter ? '' : 'show'}`} onClick={this.recenter}>
                    <span className="content">
                        Recentrer
                    </span>
                </div>
            </div>
        )
    }
}