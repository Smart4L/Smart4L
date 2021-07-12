import React ,{ useState, useEffect, forwardRef } from 'react';
import moment from 'moment';
import Leaflet from 'leaflet';
import L from 'leaflet';
import { Map as LMap, Marker, Popup, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

Leaflet.Icon.Default.imagePath = '../node_modules/leaflet';

delete Leaflet.Icon.Default.prototype._getIconUrl;

Leaflet.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

const suitcasePoint = new L.Icon({
    iconUrl: require('../../assets/images/4l-blue.png'),
    iconRetinaUrl: require('../../assets/images/4l-blue.png'),
    iconAnchor: [20, 40],
    popupAnchor: [0, -35],
    iconSize: [40, 40],
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    shadowSize: [29, 40],
    shadowAnchor: [7, 40],
})

export const Map = forwardRef((props, ref) => {
    const [time, setTime] = useState(moment());
    const [zoom, setZoom] = useState(13);
    const [carPosition, setCarPosition] = useState({ lat: 47.218371, lng: -1.553621 });
    const [mapPosition, setMapPosition] = useState({ lat: 47.218371, lng: -1.553621 });
    const [isCenter, setIsCenter] = useState(true);
    const [vehiclePath, setVehiclePath] = useState([]);

    useEffect(() => {
        const interval = setInterval(() => {
          setTime(moment())
        }, 500);
        return () => clearInterval(interval);
      }, []);
    useEffect(() => { updateCar(props.carPosition) }, [props.carPosition])

    const updateCar = (newPosition) => {
        setCarPosition(newPosition)
        setVehiclePath([...vehiclePath, newPosition])
        if(isCenter){
            setMapPosition(newPosition)
        }
    }

    /**
     * 
     * @param {L.LatLng} obj Object you want to get the position
     * @return {[]} Object position in array
     */
    const getPosition = (obj) => {
        try{
            return [obj.lat, obj.lng];
        }
        catch(e){
            console.error(e.message);
            throw new Error(e.message);
        }
    }

    const onMoveEvent = () => {
        if(isCenter){
            setIsCenter(false);
        }
    }

    const recenter = () => {
        let newPosition = {}
        newPosition.lat = mapPosition.lat - 0.0000001
        newPosition.lng = mapPosition.lng - 0.0000001
        setIsCenter(true)
        setMapPosition(newPosition)
    }

    let lineOption = { color: 'lime' };
    let nantes = [47.218371,-1.553621];
  
    return (
        <div className="map_container">
            <div className="top">
                <span className="content">
                    { time.format('HH:mm') }
                </span>
            </div>
            <div className="leaflet-container">
                <LMap center={getPosition(mapPosition)} zoom={zoom}
                    onmouseup={onMoveEvent}
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
                    <Marker position={getPosition(carPosition)} icon={suitcasePoint}>
                        <Popup>
                            L'équipage 404L
                        </Popup>
                    </Marker>
                    <Polyline pathOptions={lineOption} positions={vehiclePath} />
                </LMap>
            </div>
            <div className={`bottom ${isCenter ? '' : 'show'}`} onClick={recenter}>
                <span className="content">
                    Recentrer
                </span>
            </div>
        </div>
        )
  });